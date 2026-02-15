import json
import difflib
import os
import random
import time
from typing import Any, Dict, List, Tuple

import streamlit as st
from dotenv import load_dotenv
import litellm


GameData = Dict[str, Any]

# URL of Ohio State's LiteLLM proxy server (same as Class-9 exercise)
CUSTOM_API_BASE = "https://litellmproxy.osu-ai.org"


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
        "- 5 categories.\n"
        "- Each category must have 5 clues.\n"
        "- Use increasing values: 200, 400, 600, 800, 1000.\n"
        "- All content must be about astronomy.\n"
        "- Do NOT include any explanation outside the JSON.\n"
        "- Do NOT reuse exactly the same text or exact same set of clues across different calls; "
        "pretend you are sampling from a large bank of possible clues."
    )

    # Use the same pattern as in Class-9-Exercise: OSU LiteLLM proxy + ASTRO1221_API_KEY
    astro1221_key = os.getenv("ASTRO1221_API_KEY")
    if not astro1221_key:
        raise ValueError(
            "ASTRO1221_API_KEY is not set. "
            "Make sure your `.env` file (same folder as this script) defines ASTRO1221_API_KEY."
        )

    # Add a random run ID to discourage proxy-side caching and encourage variety.
    run_id = random.randint(0, 1_000_000_000)

    resp = litellm.completion(
        model="openai/GPT-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    "Generate the game board JSON now. "
                    f"Use different wording and examples than previous runs. run_id={run_id}"
                ),
            },
        ],
        api_base=CUSTOM_API_BASE,
        api_key=astro1221_key,
        temperature=0.7,
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

    # Record token usage (if provided) so we can inspect it in the UI.
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


def init_session_state() -> None:
    if "game_board" not in st.session_state:
        st.session_state.game_board = None
    if "answered_questions" not in st.session_state:
        st.session_state.answered_questions = set()  # type: ignore[assignment]
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "current_clue" not in st.session_state:
        st.session_state.current_clue = None
    if "answer_input" not in st.session_state:
        st.session_state.answer_input = ""
    if "last_token_usage" not in st.session_state:
        st.session_state.last_token_usage = None


def mark_answered(cat_idx: int, clue_idx: int) -> None:
    st.session_state.answered_questions.add((cat_idx, clue_idx))  # type: ignore[union-attr]


def is_answered(cat_idx: int, clue_idx: int) -> bool:
    return (cat_idx, clue_idx) in st.session_state.answered_questions  # type: ignore[union-attr]


def set_current_clue(cat_idx: int, clue_idx: int) -> None:
    categories: List[Dict[str, Any]] = st.session_state.game_board["categories"]  # type: ignore[index]
    clue = categories[cat_idx]["clues"][clue_idx]

    # Build multiple-choice options: correct answer + up to 3 random answers
    # from other clues on the board.
    other_answers: List[str] = []
    for ci, cat in enumerate(categories):
        for qi, c in enumerate(cat["clues"]):
            if ci == cat_idx and qi == clue_idx:
                continue
            ans = c.get("answer")
            if isinstance(ans, str) and ans.strip():
                other_answers.append(ans)

    distractors = random.sample(other_answers, k=min(3, len(other_answers))) if other_answers else []
    options = distractors + [clue["answer"]]
    random.shuffle(options)

    st.session_state.current_clue = {
        "category_index": cat_idx,
        "clue_index": clue_idx,
        "category_name": categories[cat_idx]["name"],
        "value": clue["value"],
        "clue": clue["clue"],
        "answer": clue["answer"],
        "options": options,
    }
    st.session_state.answer_input = ""


def _normalize_answer(text: str) -> str:
    """
    Normalize answers so that Jeopardy-style phrases like
    'what is mars' or 'What is Mars?' become just 'mars'.
    This lets users simply type 'mars' and be marked correct.
    """
    t = text.strip().lower()

    # Strip common Jeopardy-style prefixes
    prefixes = [
        "what is ", "what's ", "whats ",
        "who is ", "who's ", "whos ",
        "where is ", "where's ", "wheres ",
    ]
    for p in prefixes:
        if t.startswith(p):
            t = t[len(p) :]
            break

    # Remove leading articles
    articles = ("the ", "a ", "an ")
    for a in articles:
        if t.startswith(a):
            t = t[len(a) :]
            break

    # Strip punctuation at the ends
    t = t.strip(" .!?\"'")
    return t


def check_answer(user_answer: str, correct_answer: str) -> bool:
    user = _normalize_answer(user_answer)
    correct = _normalize_answer(correct_answer)

    if not user:
        return False

    # Simple forgiving comparison using difflib
    matches = difflib.get_close_matches(user, [correct], n=1, cutoff=0.7)
    return bool(matches)


def render_board() -> None:
    categories: List[Dict[str, Any]] = st.session_state.game_board["categories"]  # type: ignore[index]

    #st.subheader("Astronomy Jeopardy")
    st.markdown(
        """
        <style>
        .jeopardy-button button[kind="secondary"] {
            background-color: #1e3a8a !important; /* deep blue */
            color: #facc15 !important;            /* gold */
            border-radius: 6px !important;
            border: 1px solid #facc15 !important;
            font-weight: 700 !important;
        }
        .jeopardy-button button[kind="secondary"]:disabled {
            background-color: #111827 !important;
            color: #6b7280 !important;
            border-color: #374151 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    num_categories = len(categories)
    num_clues = max(len(cat["clues"]) for cat in categories)

    # Header row: category names
    cols = st.columns(num_categories)
    for idx, cat in enumerate(categories):
        with cols[idx]:
            st.markdown(f"**{cat['name']}**")

    # Value rows
    for clue_idx in range(num_clues):
        cols = st.columns(num_categories)
        for cat_idx, cat in enumerate(categories):
            clues = cat["clues"]
            with cols[cat_idx]:
                if clue_idx < len(clues):
                    clue = clues[clue_idx]
                    value = clue["value"]
                    key = f"btn-{cat_idx}-{clue_idx}"
                    disabled = is_answered(cat_idx, clue_idx)
                    label = f"${value}" if not disabled else "—"
                    # Wrap button so we can style via CSS
                    with st.container():
                        st.markdown('<div class="jeopardy-button">', unsafe_allow_html=True)
                        if st.button(label, key=key, disabled=disabled):
                            set_current_clue(cat_idx, clue_idx)
                        st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.write("")


def render_current_clue() -> None:
    current = st.session_state.current_clue
    if not current:
        return

    # Full-page style view: hide the board and show just the question + options.
    st.header("Astronomy Jeopardy Question")
    st.markdown(f"**Category:** {current['category_name']}")
    st.markdown(f"**Value:** ${current['value']}")
    st.write(current["clue"])

    options: List[str] = current.get("options", [current["answer"]])
    selected_option = st.radio(
        "Choose your answer:",
        options,
        key="answer_radio",
    )

    cols = st.columns(3)
    with cols[0]:
        submitted = st.button("Submit answer")
    with cols[1]:
        give_up = st.button("Show answer / Skip")
    with cols[2]:
        close = st.button("Close")

    if submitted:
        user_answer = selected_option
        correct_answer = current["answer"]
        cat_idx = current["category_index"]
        clue_idx = current["clue_index"]
        value = current["value"]

        if check_answer(user_answer, correct_answer):
            st.success(f"Correct! You earn ${value}.")
            st.session_state.score += value
        else:
            st.error(f"Not quite. The correct answer was: {correct_answer}")
            st.session_state.score -= value

        mark_answered(cat_idx, clue_idx)
        st.session_state.current_clue = None
        # Pause briefly so the player can see the feedback,
        # then automatically close the question view.
        time.sleep(2)
        st.rerun()

    elif give_up:
        correct_answer = current["answer"]
        st.info(f"The correct answer was: {correct_answer}")
        mark_answered(current["category_index"], current["clue_index"])
        st.session_state.current_clue = None
        time.sleep(2)
        st.rerun()

    elif close:
        st.session_state.current_clue = None


def main() -> None:
    # Load environment variables from a .env file (if present),
    # so ASTRO1221_API_KEY is available for the OSU LiteLLM proxy.
    load_dotenv()

    if not os.getenv("ASTRO1221_API_KEY"):
        st.warning(
            "ASTRO1221_API_KEY is not set. "
            "Make sure your `.env` file (same folder as this script) defines ASTRO1221_API_KEY."
        )

    st.title("Astronomy Jeopardy")
    init_session_state()

    st.sidebar.header("Game Controls")
    if st.sidebar.button("New Game"):
        with st.spinner("Generating a new astronomy Jeopardy board..."):
            try:
                st.session_state.game_board = generate_game_data()
                st.session_state.answered_questions = set()  # type: ignore[assignment]
                st.session_state.score = 0
                st.session_state.current_clue = None
            except Exception as exc:  # noqa: BLE001
                st.error(f"Failed to generate game data: {exc}")

    st.sidebar.markdown(f"**Score:** ${st.session_state.score}")

    # Show token usage info if available
    usage = st.session_state.last_token_usage
    if usage:
        prompt_tokens = usage.get("prompt_tokens") or usage.get("input_tokens")
        completion_tokens = usage.get("completion_tokens") or usage.get("output_tokens")
        total_tokens = usage.get("total_tokens") or (
            (prompt_tokens or 0) + (completion_tokens or 0)
        )
        st.sidebar.markdown(
            f"**Last board tokens**  \n"
            f"Prompt: {prompt_tokens or '—'}, "
            f"Completion: {completion_tokens or '—'}, "
            f"Total: {total_tokens or '—'}"
        )

    if st.session_state.game_board is None:
        st.info("Click **New Game** in the sidebar to generate an astronomy Jeopardy board.")
        return

    # Always render the board so buttons remain clickable,
    # then, if a clue is active, render the question view as well.
    # This avoids the need to click twice to open a question.
    render_board()
    if st.session_state.current_clue is not None:
        render_current_clue()


if __name__ == "__main__":
    main()