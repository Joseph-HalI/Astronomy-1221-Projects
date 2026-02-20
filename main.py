import os

import streamlit as st
from dotenv import load_dotenv

from game_data import generate_game_data
from game_logic import init_session_state
from ui import inject_global_styles, render_board, render_current_clue


def main() -> None:
    load_dotenv()

    # Apply the Jeopardy theme immediately so every state looks consistent
    inject_global_styles()

    if not os.getenv("ASTRO1221_API_KEY"):
        st.warning(
            "ASTRO1221_API_KEY is not set. "
            "Make sure your `.env` file (same folder as this script) defines ASTRO1221_API_KEY."
        )

    st.title("Astronomy Jeopardy")
    init_session_state()

    st.sidebar.header("Game Controls")

    # Player selection — defaults to 1 (singleplayer) if nothing is chosen
    num_players = st.sidebar.selectbox(
        "Number of teams:",
        options=[1, 2, 3, 4],
        index=st.session_state.num_players - 1,
        format_func=lambda x: "1 (Single player)" if x == 1 else f"{x} Teams",
    )

    if st.sidebar.button("New Game"):
        with st.spinner("Generating a new astronomy Jeopardy board..."):
            try:
                st.session_state.game_board = generate_game_data()
                st.session_state.answered_questions = set()
                st.session_state.num_players = num_players
                st.session_state.scores = [0] * num_players
                st.session_state.current_player = 0
                st.session_state.current_clue = None
            except Exception as exc:
                st.error(f"Failed to generate game data: {exc}")

    # Show scores in sidebar with green indicator for current player
    if st.session_state.num_players == 1:
        st.sidebar.markdown(f"**Score:** ${st.session_state.scores[0]}")
    else:
        st.sidebar.markdown("**Scores:**")
        st.sidebar.html("""
        <style>
        .team-row { display: flex; align-items: center; gap: 8px; margin: 4px 0; color: white; font-size: 0.95rem; }
        .team-indicator { width: 6px; height: 22px; border-radius: 3px; flex-shrink: 0; }
        .team-indicator.active { background-color: #22c55e; }
        .team-indicator.inactive { background-color: transparent; }
        </style>
        """)
        for i, score in enumerate(st.session_state.scores):
            active = "active" if i == st.session_state.current_player else "inactive"
            st.sidebar.html(f"""
            <div class="team-row">
                <div class="team-indicator {active}"></div>
                <span>Team {i + 1}: ${score}</span>
            </div>
            """)

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

    if st.session_state.current_clue is not None:
        render_current_clue()
    else:
        render_board()


if __name__ == "__main__":
    main()