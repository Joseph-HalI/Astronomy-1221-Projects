import json
import os
import random
from typing import Any, Dict

import litellm
import streamlit as st

from config import CUSTOM_API_BASE, GameData
from rag_lectures import search_chunks

# This makes sure that the data we get is what we expect.
def validate_game_data(data: Any) -> GameData:
    """
    Strictly validate that data matches the expected schema:

    {
        "categories": [
            {
                "name": "Category Name",
                "clues": [
                    {"value": 200, "clue": "text", "answer": "text"},
                    ...
                ]
            },
            ...
        ]
    }
    """
    if not isinstance(data, dict):
        raise ValueError("Game data must be a JSON object.")

    categories = data.get("categories")
    if not isinstance(categories, list) or len(categories) == 0:
        raise ValueError("`categories` must be a non-empty list.")

    for c_idx, category in enumerate(categories):
        if not isinstance(category, dict):
            raise ValueError(f"Category {c_idx} must be an object.")
        name = category.get("name")
        clues = category.get("clues")

        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"Category {c_idx} has invalid name.")
        if not isinstance(clues, list) or len(clues) == 0:
            raise ValueError(f"Category {c_idx} must have a non-empty `clues` list.")

        for q_idx, clue in enumerate(clues):
            if not isinstance(clue, dict):
                raise ValueError(f"Clue {q_idx} in category {c_idx} must be an object.")
            if not isinstance(clue.get("value"), int):
                raise ValueError(f"Clue {q_idx} in category {c_idx} must have integer `value`.")
            if not isinstance(clue.get("clue"), str) or not clue.get("clue").strip():
                raise ValueError(f"Clue {q_idx} in category {c_idx} must have non-empty `clue` text.")
            if not isinstance(clue.get("answer"), str) or not clue.get("answer").strip():
                raise ValueError(f"Clue {q_idx} in category {c_idx} must have non-empty `answer` text.")

    return {"categories": categories}


def generate_lectures_category() -> Dict[str, Any]:
    """
    Generate a "Lectures" category using RAG to retrieve relevant content from lecture notes.
    Returns a category dictionary with 5 clues based on lecture content.
    """
    astro1221_key = os.getenv("ASTRO1221_API_KEY")
    if not astro1221_key:
        raise ValueError(
            "ASTRO1221_API_KEY is not set. "
            "Make sure your `.env` file (same folder as this script) defines ASTRO1221_API_KEY."
        )

    # Topics from our lectures - used to search for relevant chunks via RAG
    astronomy_topics = [
        "variables and data collections",
        "control flow and file operations",
        "numerical computing",
        "functions and object oriented programming",
        "data visualization",
        "LLM API basics and parameters",
        "LLM function tools and RAG retrieval augmented generation",
        "GitHub and version control",
        "Streamlit app deployment",
        "Pandas data analysis",
    ]
    
    # Shuffle topics and pick a random subset so each game sees different material
    shuffled_topics = random.sample(astronomy_topics, min(6, len(astronomy_topics)))
    
    # Search for relevant chunks - use top_k > 1 then randomly pick to add retrieval randomness
    all_chunks = []
    seen_chunk_ids = set()
    for topic in shuffled_topics:
        results = search_chunks(topic, top_k=3)
        valid = [r for r in results if r['similarity'] >= 0.2]
        if valid:
            chosen = random.choice(valid)
            chunk = chosen['chunk']
            chunk_id = chunk.get('chunk_id', id(chunk))
            if chunk_id not in seen_chunk_ids:
                seen_chunk_ids.add(chunk_id)
                all_chunks.append(chunk['text'])
    
    # If RAG didn't find enough content, try broader fallback search terms
    if len(all_chunks) < 3:
        fallback_topics = ["astronomy", "coding", "LLM", "data science"]
        random.shuffle(fallback_topics)
        for topic in fallback_topics:
            if len(all_chunks) >= 5:
                break
            results = search_chunks(topic, top_k=3)
            valid = [r for r in results if r['similarity'] >= 0.2]
            if valid:
                chosen = random.choice(valid)
                chunk = chosen['chunk']
                chunk_id = chunk.get('chunk_id', id(chunk))
                if chunk_id not in seen_chunk_ids:
                    seen_chunk_ids.add(chunk_id)
                    all_chunks.append(chunk['text'])
    
    # Build the context string from collected chunks, respecting a total length limit
    context_parts = []
    total_length = 0
    max_context_length = 3000
    
    for chunk in all_chunks[:5]:
        chunk_text = chunk[:800]
        
        last_sentence_end = max(
            chunk_text.rfind('.'),
            chunk_text.rfind('?'),
            chunk_text.rfind('!')
        )
        if last_sentence_end > 0:
            chunk_text = chunk_text[:last_sentence_end + 1]
        
        if total_length + len(chunk_text) > max_context_length:
            break
        context_parts.append(chunk_text)
        total_length += len(chunk_text)
    
    random.shuffle(context_parts)
    context = "\n\n---\n\n".join(context_parts)
    
    if not context:
        context = "General astronomy topics from the course lectures."
    
    # ---- UPDATED system prompt: enforces short, Jeopardy-style answers ----
    system_prompt = (
        "You are generating Jeopardy-style questions based on course lecture materials. "
        "In Jeopardy, the CLUE is a description or hint, and the ANSWER is a short, specific term, name, or phrase. "
        "Answers must be 1-5 words maximum — never a full sentence or explanation. "
        "The clue should describe or define the answer, not ask an open-ended question like 'Why is X important?'. "
        "Each time you are called, pick different concepts and facts to quiz on — avoid reusing similar clues.\n\n"
        "Good example: {\"clue\": \"This Git command syncs your local repo with the latest remote changes\", \"answer\": \"git pull\"}\n"
        "Bad example: {\"clue\": \"Why is pulling important before starting work?\", \"answer\": \"Because you may have worked on multiple computers...\"}\n\n"
        "Return ONLY a JSON object with this structure:\n"
        '{\"clues\": [\n'
        '  {\"value\": 200, \"clue\": \"text\", \"answer\": \"text\"},\n'
        '  {\"value\": 400, \"clue\": \"text\", \"answer\": \"text\"},\n'
        '  {\"value\": 600, \"clue\": \"text\", \"answer\": \"text\"},\n'
        '  {\"value\": 800, \"clue\": \"text\", \"answer\": \"text\"},\n'
        '  {\"value\": 1000, \"clue\": \"text\", \"answer\": \"text\"}\n'
        ']}\n\n'
        "Requirements:\n"
        "- Generate exactly 5 clues with values 200, 400, 600, 800, 1000.\n"
        "- Base clues on the provided lecture content.\n"
        "- Use increasing difficulty: 200=easiest, 1000=hardest.\n"
        "- Answers must be a specific term, name, or short phrase (5 words max) — never a sentence.\n"
        "- Clues must describe or define the answer, not ask open-ended questions.\n"
        "- Do NOT include any explanation outside the JSON."
    )
    
    run_id = random.randint(0, 1_000_000_000)
    
    user_prompt = f"""Generate 5 Jeopardy-style clues based on the following course lecture materials:

LECTURE MATERIALS:
{context}

Remember: clues describe the answer, answers are short terms or phrases (5 words max). Vary which facts and concepts you quiz on. run_id={run_id}"""

    resp = litellm.completion(
        model="openai/GPT-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        api_base=CUSTOM_API_BASE,
        api_key=astro1221_key,
        temperature=1,
        response_format={"type": "json_object"},
    )
    
    raw_content = resp.choices[0].message["content"]
    if isinstance(raw_content, list):
        raw_content = "".join(part.get("text", "") for part in raw_content if isinstance(part, dict))
    
    try:
        clues_data = json.loads(raw_content)
    except Exception as exc:
        raise ValueError(f"Failed to parse JSON from LLM for Lectures category: {exc}") from exc
    
    clues = clues_data.get("clues", [])
    if not isinstance(clues, list) or len(clues) != 5:
        raise ValueError(f"Expected 5 clues, got {len(clues) if isinstance(clues, list) else 'non-list'}")
    
    expected_values = [200, 400, 600, 800, 1000]
    for i, clue in enumerate(clues):
        if not isinstance(clue, dict):
            raise ValueError(f"Clue {i} is not a dictionary")
        clue["value"] = expected_values[i]
    
    return {
        "name": "Lectures",
        "clues": clues
    }


def generate_game_data() -> GameData:
    """
    Call an LLM via LiteLLM to generate game data, returning a strictly validated JSON object.
    Uses environment variables for API keys (handled by LiteLLM).
    """
    system_prompt = (
        "You are generating Jeopardy-style questions for an introductory astronomy class. "
        "Every time you are called, you MUST vary the specific wording of clues and, when reasonable, "
        "the specific facts used, so that repeated calls do NOT return an identical board.\n\n"
        "Return ONLY a JSON object with this structure:\n"
        '{\"categories\": [\n'
        '  {\"name\": \"Category Name\", \"clues\": [\n'
        '    {\"value\": 200, \"clue\": \"text\", \"answer\": \"text\"},\n'
        "    ...\n"
        "  ]}\n"
        "]}\n\n"
        "Requirements (must follow these exactly):\n"
        "- 4 categories.\n"
        "- Each category must have 5 clues.\n"
        "- Use increasing values: 200, 400, 600, 800, 1000.\n"
        "- Within each category, difficulty must increase with value: 200=easiest (recall), 400=moderate, 600=application, 800=harder, 1000=hardest (synthesis or obscure facts).\n"
        "- All content must be about astronomy.\n"
        "- Do NOT use categories like 'Solar System Basics', 'Solar System', 'Planets', or other basic solar system topics.\n"
        "- Do NOT include any explanation outside the JSON.\n"
        "- Do NOT reuse exactly the same text or exact same set of clues across different calls; "
        "pretend you are sampling from a large bank of possible clues."
    )

    astro1221_key = os.getenv("ASTRO1221_API_KEY")
    if not astro1221_key:
        raise ValueError(
            "ASTRO1221_API_KEY is not set. "
            "Make sure your `.env` file (same folder as this script) defines ASTRO1221_API_KEY."
        )

    run_id = random.randint(0, 1_000_000_000)

    resp = litellm.completion(
        model="openai/GPT-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    "Generate the game board JSON now. "
                    "In each category, make the 200 clue easiest and the 1000 clue hardest. "
                    "Avoid categories about basic solar system topics (like 'Solar System Basics' or 'Planets'). "
                    f"Use different wording and examples than previous runs. run_id={run_id}"
                ),
            },
        ],
        api_base=CUSTOM_API_BASE,
        api_key=astro1221_key,
        temperature=1,
        response_format={"type": "json_object"},
    )

    raw_content = resp.choices[0].message["content"]  # type: ignore[index]
    if isinstance(raw_content, list):
        raw_content = "".join(part.get("text", "") for part in raw_content if isinstance(part, dict))

    try:
        data = json.loads(raw_content)
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"Failed to parse JSON from LLM: {exc}") from exc

    # Displays the amount of tokens used when generating the game board
    usage = None
    if isinstance(resp, dict):
        usage = resp.get("usage")
    if usage is None:
        prompt_text = (
            system_prompt
            + " "
            + "Generate the game board JSON now. "
            + "In each category, make the 200 clue easiest and the 1000 clue hardest. "
            + "Avoid categories about basic solar system topics (like 'Solar System Basics' or 'Planets'). "
            + f"Use different wording and examples than previous runs. run_id={run_id}"
        )
        approx_prompt_tokens = max(1, len(prompt_text) // 4)
        approx_completion_tokens = max(1, len(raw_content) // 4)
        usage = {
            "prompt_tokens": approx_prompt_tokens,
            "completion_tokens": approx_completion_tokens,
            "total_tokens": approx_prompt_tokens + approx_completion_tokens,
            "approximate": True,
        }

    st.session_state.last_token_usage = usage

    # Validate the 4 LLM-generated categories
    llm_data = validate_game_data(data)
    
    # Generate the 5th category using RAG
    lectures_category = generate_lectures_category()
    
    # Combine the 4 LLM categories with the 1 RAG category
    combined_categories = llm_data["categories"] + [lectures_category]
    
    return validate_game_data({"categories": combined_categories})