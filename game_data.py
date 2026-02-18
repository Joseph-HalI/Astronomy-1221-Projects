import json
import os
import random
from typing import Any, Dict

import litellm
import streamlit as st

from config import CUSTOM_API_BASE, GameData

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
        "- 5 categories.\n"
        "- Each category must have 5 clues.\n"
        "- Use increasing values: 200, 400, 600, 800, 1000.\n"
        "- All content must be about astronomy.\n"
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
                    f"Use different wording and examples than previous runs. run_id={run_id}" # The idea of the run ID was so that it would generate random catagories and questions but i dont think it works
                ),
            },
        ],
        api_base=CUSTOM_API_BASE,
        api_key=astro1221_key,
        temperature=0.7, # I dont think that changing this value affects much because of the system prompt.
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

    return validate_game_data(data)
