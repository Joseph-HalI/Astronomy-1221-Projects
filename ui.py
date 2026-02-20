import random
import time
from typing import Any, Dict, List

import streamlit as st

from game_logic import advance_player, check_answer, generate_distractors, is_answered, mark_answered, set_current_clue


def inject_global_styles() -> None:
    """Global styles applied to every view so the theme is consistent."""
    st.html("""
    <style>
    .stApp {
        background-color: #071277 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #030043 !important;
    }
    [data-testid="stMarkdownContainer"] p strong {
        text-transform: uppercase !important;
    }
    /* Sidebar button: always themed, fixed size regardless of which view is active */
    [data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] {
        background-color: #071277 !important;
        color: #d69f4c !important;
        border: 2px solid #000000 !important;
        font-weight: 900 !important;
        border-radius: 8px !important;
        width: auto !important;
        min-height: 40px !important;
        height: auto !important;
        white-space: nowrap !important;
    }
    [data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] p {
        font-size: 1rem !important;
    }
    </style>
    """)


def render_board() -> None:
    categories: List[Dict[str, Any]] = st.session_state.game_board["categories"]  # type: ignore[index]

    inject_global_styles()

    st.html("""
    <style>
    [data-testid="stBaseButton-secondary"] {
        background-color: #071277 !important;
        color: #d69f4c !important;
        border: 2px solid #000000 !important;
        font-weight: 900 !important;
        border-radius: 8px !important;
        height: auto !important;
        min-height: 60px !important;
        width: 100px !important;
        white-space: normal !important;
    }
    [data-testid="stBaseButton-secondary"] p {
        font-size: 1.5rem !important;
    }
    </style>
    """)

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
                    with st.container():
                        st.markdown('<div class="jeopardy-button">', unsafe_allow_html=True)
                        if st.button(label, key=key, disabled=disabled):
                            set_current_clue(cat_idx, clue_idx)
                            st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.write("")


def render_current_clue() -> None:
    current = st.session_state.current_clue
    if not current:
        return

    inject_global_styles()

    st.html("""
    <style>
    [data-testid="stBaseButton-secondary"] {
        background-color: #071277 !important;
        color: #d69f4c !important;
        border: 2px solid #000000 !important;
        font-weight: 900 !important;
        width: auto !important;
        min-height: 40px !important;
        height: auto !important;
        white-space: nowrap !important;
        border-radius: 8px !important;
    }
    [data-testid="stBaseButton-secondary"] p {
        font-size: 1rem !important;
    }
    .main .block-container {
        max-width: 100% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    </style>
    """)

    st.header("Astronomy Jeopardy Question")
    st.markdown(f"**Category:** {current['category_name']}")
    st.markdown(f"**Value:** ${current['value']}")
    st.write(current["clue"])

    show_hints: bool = st.session_state.get("show_hints", False)

    if not show_hints:
        user_answer = st.text_input("Your answer:", key="answer_input")
    else:
        st.caption("💡 Hint: choose an option below.")
        options: List[str] = current.get("options", [current["answer"]])
        user_answer = st.radio("Choose your answer:", options, key="answer_radio")

    # --- Action buttons ---
    cols = st.columns(3)
    with cols[0]:
        submitted = st.button("Submit answer")
    with cols[1]:
        hint = st.button("💡 Hint", disabled=show_hints)
    with cols[2]:
        give_up = st.button("Give Up")

    # --- Button logic ---

    if submitted:
        correct_answer = current["answer"]
        cat_idx = current["category_index"]
        clue_idx = current["clue_index"]
        value = current["value"]
        num_players = st.session_state.get("num_players", 1)
        current_player = st.session_state.get("current_player", 0)

        if check_answer(user_answer, correct_answer):
            team_label = f"Team {current_player + 1}" if num_players > 1 else "You"
            verb = "earned" if num_players > 1 else "earned"
            st.success(f"Correct! {team_label} earned ${value}.")
            st.session_state.scores[current_player] += value
        else:
            st.error(f"Not quite. The correct answer was: {correct_answer}")
            st.session_state.scores[current_player] -= value

        mark_answered(cat_idx, clue_idx)
        st.session_state.current_clue = None
        st.session_state.show_hints = False
        advance_player()
        time.sleep(2)
        st.rerun()

    elif hint:
        with st.spinner("Generating hints..."):
            distractors = generate_distractors(current["clue"], current["answer"])

        if len(distractors) < 3:
            categories: List[Dict[str, Any]] = st.session_state.game_board["categories"]
            other_answers = []
            for ci, cat in enumerate(categories):
                for qi, c in enumerate(cat["clues"]):
                    if ci == current["category_index"] and qi == current["clue_index"]:
                        continue
                    ans = c.get("answer")
                    if isinstance(ans, str) and ans.strip():
                        other_answers.append(ans)
            distractors = random.sample(other_answers, k=min(3, len(other_answers)))

        options = distractors + [current["answer"]]
        random.shuffle(options)
        st.session_state.current_clue["options"] = options
        st.session_state.show_hints = True
        st.rerun()

    elif give_up:
        correct_answer = current["answer"]
        st.info(f"The correct answer was: {correct_answer}")
        mark_answered(current["category_index"], current["clue_index"])
        st.session_state.current_clue = None
        st.session_state.show_hints = False
        advance_player()
        time.sleep(2)
        st.rerun()