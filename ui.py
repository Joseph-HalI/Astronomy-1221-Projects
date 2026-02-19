import time
from typing import Any, Dict, List

import streamlit as st

from game_logic import check_answer, is_answered, mark_answered, set_current_clue


def render_board() -> None:
    categories: List[Dict[str, Any]] = st.session_state.game_board["categories"]  # type: ignore[index]

    st.html(
    """
    <style>
    .stApp {
        background-color: #071277 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #030043 !important;
    }
    [data-testid="stBaseButton-secondary"] {
        background-color: #071277 !important;
        color: #d69f4c !important;
        border: 2px solid #000000 !important;
        font-weight: 900 !important;
        border-radius: 0px !important;
        height: auto !important;
        min-height: 60px !important;
        width: 100px !important;
        white-space: normal !important; 
    }
    [data-testid="stMarkdownContainer"] p strong {
    text-transform: uppercase !important;
    }
    [data-testid="stBaseButton-secondary"] p {
    font-size: 1.5rem !important;
    }
    </style>
    """
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
    # Defines the 3 buttons you can choose from when you have the question show up.
    cols = st.columns(3)
    with cols[0]:
        submitted = st.button("Submit answer") #This as you would expect submits your answer
    with cols[1]:
        give_up = st.button("Show answer / Skip") # This will show you the answer, wait 2 seconds, then go back to the main board. Plan on changing this to "Hint" which will turn this into mutliple choice question
    with cols[2]:
        close = st.button("Close") # This will close the question and not give you any points. We should change this to "Give Up"

    # This is the logic for the submit button when clicked
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

    # This is the logic for the give up button
    elif give_up:
        correct_answer = current["answer"]
        st.info(f"The correct answer was: {correct_answer}")
        mark_answered(current["category_index"], current["clue_index"])
        st.session_state.current_clue = None
        time.sleep(2)
        st.rerun()

        
    # This is the logic for the close button.
    elif close:
        st.session_state.current_clue = None
