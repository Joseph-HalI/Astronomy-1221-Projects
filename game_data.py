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
    # Anything inside triple quotations is just an explaination to the LLM what the function should be doing.
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
    # This is just making sure we're generating everything properly. if not, it'll will break things and sends out an error.
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
    
    # Search for the most relevant chunk for each topic and collect them
    all_chunks = []
    for topic in astronomy_topics:
        results = search_chunks(topic, top_k=1)  # Only grab the single best match per topic
        # Only include chunks that are actually relevant (similarity score >= 0.2)
        if results and results[0]['similarity'] >= 0.2:
            all_chunks.append(results[0]['chunk']['text'])
    
    # If RAG didn't find enough content, try broader fallback search terms
    if len(all_chunks) < 3:
        fallback_topics = ["astronomy", "coding", "LLM", "data science"]
        for topic in fallback_topics:
            if len(all_chunks) >= 5:  # Stop once we have enough chunks
                break
            results = search_chunks(topic, top_k=1)
            if results and results[0]['similarity'] >= 0.2:
                chunk_text = results[0]['chunk']['text']
                if chunk_text not in all_chunks:  # Avoid adding duplicate chunks
                    all_chunks.append(chunk_text)
    
    # Build the context string from collected chunks, respecting a total length limit
    context_parts = []
    total_length = 0
    max_context_length = 3000  # Cap context size to avoid exceeding LLM token limits
    
    for chunk in all_chunks[:5]:  # Use at most 5 chunks regardless of how many we found
        chunk_text = chunk[:800]  # Truncate each chunk to 800 chars to save space
        
        # Find the last complete sentence so we don't cut off mid-sentence
        last_sentence_end = max(
            chunk_text.rfind('.'),
            chunk_text.rfind('?'),
            chunk_text.rfind('!')
        )
        if last_sentence_end > 0:
            chunk_text = chunk_text[:last_sentence_end + 1]  # Trim to last complete sentence
        
        # Stop adding chunks if we'd exceed our total context length limit
        if total_length + len(chunk_text) > max_context_length:
            break
        context_parts.append(chunk_text)
        total_length += len(chunk_text)
    
    # Join all chunks with a separator so the LLM knows where one section ends and another begins
    context = "\n\n---\n\n".join(context_parts)
    
    # Fall back to a generic description if no relevant lecture content was found
    if not context:
        context = "General astronomy topics from the course lectures."
    
    # System prompt tells the LLM its role and defines the exact JSON format we expect back
    system_prompt = (
        "You are generating Jeopardy-style questions based on course lecture materials. "
        "Create questions that test understanding of the specific content from the lectures. "
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
        "- Do NOT include any explanation outside the JSON.\n"
        "- Ensure answers are specific facts from the lecture materials."
    )
    
    # User prompt provides the actual lecture content for the LLM to base questions on
    user_prompt = f"""Generate 5 Jeopardy-style clues based on the following course lecture materials:

LECTURE MATERIALS:
{context}

Create clues that test knowledge of the specific concepts, facts, and terminology from these lectures."""

    # Call the LLM via LiteLLM with json_object mode to guarantee valid JSON back
    resp = litellm.completion(
        model="openai/GPT-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        api_base=CUSTOM_API_BASE,
        api_key=astro1221_key,
        temperature=1,  # Slightly creative but still mostly factual
        response_format={"type": "json_object"},  # Forces the LLM to return valid JSON
    )
    
    # Extract the text content from the response (handles both string and list formats)
    raw_content = resp.choices[0].message["content"]
    if isinstance(raw_content, list):
        # Some models return content as a list of parts - join them into a single string
        raw_content = "".join(part.get("text", "") for part in raw_content if isinstance(part, dict))
    
    # Parse the JSON string into a Python dictionary
    try:
        clues_data = json.loads(raw_content)
    except Exception as exc:
        raise ValueError(f"Failed to parse JSON from LLM for Lectures category: {exc}") from exc
    
    # Extract the clues list and validate we got exactly 5
    clues = clues_data.get("clues", [])
    if not isinstance(clues, list) or len(clues) != 5:
        raise ValueError(f"Expected 5 clues, got {len(clues) if isinstance(clues, list) else 'non-list'}")
    
    # Overwrite the values the LLM returned to guarantee they're exactly 200-1000
    # (LLM might return wrong values despite being told, so we enforce them here)
    expected_values = [200, 400, 600, 800, 1000]
    for i, clue in enumerate(clues):
        if not isinstance(clue, dict):
            raise ValueError(f"Clue {i} is not a dictionary")
        clue["value"] = expected_values[i]
    
    # Return the completed category in the format the game board expects
    return {
        "name": "Lectures",
        "clues": clues
    }


def generate_game_data() -> GameData:
    """
    Call an LLM via LiteLLM to generate game data, returning a strictly validated JSON object.
    Uses environment variables for API keys (handled by LiteLLM).
    """
    # This essentially just tells the API how to behave when generating the jeopardy board.
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

    # This calls the API key from the .env file without exposing it to the entire world. If the key isn't there, it will let us know.
    astro1221_key = os.getenv("ASTRO1221_API_KEY")
    if not astro1221_key:
        raise ValueError(
            "ASTRO1221_API_KEY is not set. "
            "Make sure your `.env` file (same folder as this script) defines ASTRO1221_API_KEY."
        )

    # Add a random run ID to discourage proxy-side caching and encourage variety. Sadly I don't think this actually works
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
        temperature=1, # I dont think that changing this value affects much because of the system prompt.
        response_format={"type": "json_object"},
    )

    raw_content = resp.choices[0].message["content"]  # type: ignore[index]
    if isinstance(raw_content, list):
        # Some providers may return a list of content parts
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
        # Fallback: approximate tokens from character length of prompt/completion.
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
    
    # Validate the combined result
    return validate_game_data({"categories": combined_categories})
