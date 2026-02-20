import difflib
import json
import os
import random
from typing import Any, Dict, List

import litellm
import streamlit as st

from config import CUSTOM_API_BASE


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
    if "show_hints" not in st.session_state:
        st.session_state.show_hints = False
    # Multiplayer state
    if "num_players" not in st.session_state:
        st.session_state.num_players = 1
    if "scores" not in st.session_state:
        st.session_state.scores = [0]
    if "current_player" not in st.session_state:
        st.session_state.current_player = 0


def advance_player() -> None:
    """Rotate to the next player/team."""
    if st.session_state.num_players > 1:
        st.session_state.current_player = (
            st.session_state.current_player + 1
        ) % st.session_state.num_players


def mark_answered(cat_idx: int, clue_idx: int) -> None:
    st.session_state.answered_questions.add((cat_idx, clue_idx))


def is_answered(cat_idx: int, clue_idx: int) -> bool:
    return (cat_idx, clue_idx) in st.session_state.answered_questions


def generate_distractors(clue: str, correct_answer: str) -> List[str]:
    """
    Ask the LLM to generate 3 plausible but incorrect answers for this clue.
    Called only when the player actually presses the Hint button.
    Falls back to random board answers if the LLM call fails.
    """
    astro1221_key = os.getenv("ASTRO1221_API_KEY")
    if not astro1221_key:
        return []

    prompt = (
        f"You are helping generate wrong answer choices for a Jeopardy-style game.\n\n"
        f"Clue: {clue}\n"
        f"Correct answer: {correct_answer}\n\n"
        f"Generate exactly 3 plausible but incorrect answers that:\n"
        f"- Are in the same subject area as the correct answer\n"
        f"- Could believably fool someone who doesn't know the topic well\n"
        f"- Are clearly wrong to someone who does know the topic\n"
        f"- Are similar in format and length to the correct answer\n\n"
        f"Return ONLY a JSON object like this: {{\"distractors\": [\"answer1\", \"answer2\", \"answer3\"]}}"
    )

    try:
        resp = litellm.completion(
            model="openai/GPT-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            api_base=CUSTOM_API_BASE,
            api_key=astro1221_key,
            temperature=0.9,
            response_format={"type": "json_object"},
        )
        raw = resp.choices[0].message["content"]
        if isinstance(raw, list):
            raw = "".join(part.get("text", "") for part in raw if isinstance(part, dict))
        data = json.loads(raw)
        distractors = data.get("distractors", [])
        if isinstance(distractors, list) and len(distractors) == 3:
            return [str(d) for d in distractors]
    except Exception:
        pass

    return []


def set_current_clue(cat_idx: int, clue_idx: int) -> None:
    """Sets the active clue instantly — no LLM call here."""
    categories: List[Dict[str, Any]] = st.session_state.game_board["categories"]
    clue = categories[cat_idx]["clues"][clue_idx]

    st.session_state.current_clue = {
        "category_index": cat_idx,
        "clue_index": clue_idx,
        "category_name": categories[cat_idx]["name"],
        "value": clue["value"],
        "clue": clue["clue"],
        "answer": clue["answer"],
        "options": [],  # Populated lazily when the player presses Hint
    }
    st.session_state.answer_input = ""
    st.session_state.show_hints = False


def _normalize_answer(text: str) -> str:
    t = text.strip().lower()

    prefixes = [
        "what is ", "what's ", "whats ",
        "who is ", "who's ", "whos ",
        "where is ", "where's ", "wheres ",
    ]
    for p in prefixes:
        if t.startswith(p):
            t = t[len(p):]
            break

    articles = ("the ", "a ", "an ")
    for a in articles:
        if t.startswith(a):
            t = t[len(a):]
            break

    t = t.strip(" .!?\"'")
    return t


# Known synonyms — if the user's answer or the correct answer matches any entry
# in a group, they're treated as equivalent.
SYNONYMS = [
    {"aurora borealis", "northern lights"},
    {"aurora australis", "southern lights"},
    {"aurora", "aurora borealis", "northern lights"},
    {"sol", "sun"},
    {"terra", "earth"},
    {"luna", "moon"},
    {"h2o", "water"},
    {"electromagnetic radiation", "light"},
    {"hubble", "hubble space telescope"},
    {"iss", "international space station"},
    {"milky way", "milky way galaxy"},
    {"cme", "coronal mass ejection"},
    {"hr diagram", "hertzsprung russell diagram", "hertzsprung-russell diagram"},
    {"tidal locking", "synchronous rotation"},
    {"shooting star", "meteor"},
    {"falling star", "meteor"},
    {"git pull", "pull"},
    {"git push", "push"},
    {"git commit", "commit"},
    {"llm", "large language model"},
    {"api", "application programming interface"},
    {"rag", "retrieval augmented generation"},
]


def _synonyms_match(a: str, b: str) -> bool:
    """Return True if a and b appear together in any synonym group."""
    for group in SYNONYMS:
        if a in group and b in group:
            return True
    return False


def check_answer(user_answer: str, correct_answer: str) -> bool:
    user = _normalize_answer(user_answer)
    correct = _normalize_answer(correct_answer)

    if not user:
        return False

    # Exact match after normalization
    if user == correct:
        return True

    # Synonym match
    if _synonyms_match(user, correct):
        return True

    # Token-based checks: split into individual words
    user_tokens = set(user.split())
    correct_tokens = set(correct.split())

    # If every word the user typed appears in the correct answer, accept it
    # e.g. "schema" matches "function schemas" won't work directly but
    # we also check if any user token is a substring of any correct token
    # e.g. "schema" is a substring of "schemas"
    def tokens_match(user_toks, correct_toks):
        for ut in user_toks:
            if not any(ut in ct or ct in ut for ct in correct_toks):
                return False
        return True

    if tokens_match(user_tokens, correct_tokens):
        return True

    # If the correct answer contains multiple words, also check if the user
    # answer matches any single key word in the correct answer closely
    for correct_token in correct_tokens:
        if len(correct_token) > 3:  # Skip short/common words
            matches = difflib.get_close_matches(user, [correct_token], n=1, cutoff=0.8)
            if matches:
                return True

    # Fallback: fuzzy match the full strings
    matches = difflib.get_close_matches(user, [correct], n=1, cutoff=0.6)
    return bool(matches)