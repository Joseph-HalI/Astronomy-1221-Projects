import os

import streamlit as st
from dotenv import load_dotenv

from game_data import generate_game_data
from game_logic import init_session_state
from ui import render_board, render_current_clue


def main() -> None:
    #This loads the .env file so you can get the API key without leaking it to github.
    load_dotenv()

    if not os.getenv("ASTRO1221_API_KEY"):
        st.warning(
            "ASTRO1221_API_KEY is not set. "
            "Make sure your `.env` file (same folder as this script) defines ASTRO1221_API_KEY."
        )

    st.title("Astronomy Jeopardy")
    init_session_state()

    # This generates the main starting page and the loading page. It also generates the sidebar that shows tokens and cash amount you have.
    st.sidebar.header("Game Controls")
    if st.sidebar.button("New Game"):
        with st.spinner("Generating a new astronomy Jeopardy board..."):
            try:
                st.session_state.game_board = generate_game_data()
                st.session_state.answered_questions = set()
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
