import difflib
import random
from typing import Any, Dict, List

import streamlit as st

# This saves your progress so that why you can actually play the jeopardy game.
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

# Marks a question as answered by adding it into the answered questions session state
def mark_answered(cat_idx: int, clue_idx: int) -> None:
    st.session_state.answered_questions.add((cat_idx, clue_idx))

# This displays which questions you have answered so you can't try to answer repeat questions
def is_answered(cat_idx: int, clue_idx: int) -> bool:
    return (cat_idx, clue_idx) in st.session_state.answered_questions


def set_current_clue(cat_idx: int, clue_idx: int) -> None:
    categories: List[Dict[str, Any]] = st.session_state.game_board["categories"]
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

# as the name suggests, when this function is called, it checks if the answer is correct.
def check_answer(user_answer: str, correct_answer: str) -> bool:
    user = _normalize_answer(user_answer)
    correct = _normalize_answer(correct_answer)

    if not user:
        return False

    # Simple forgiving comparison using difflib
    matches = difflib.get_close_matches(user, [correct], n=1, cutoff=0.7)
    return bool(matches)
