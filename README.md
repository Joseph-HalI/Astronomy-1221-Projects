


## Astronomy Jeopardy: Project Overview

This project implements an interactive, **Jeopardy-style quiz game** designed for an introductory astronomy and computing class. Built with **Streamlit** and powered by **LLM-generated content**, the application offers a dynamic and engaging educational experience.

### Architecture & Components

- **`main.py`**: Serves as the application's entry point, configuring the Streamlit interface, initializing the game state, and toggling between the main game board and active clue views.
- **`game_data.py`**: Leverages an LLM (via LiteLLM) alongside a Retrieval-Augmented Generation (RAG) pipeline to dynamically generate Jeopardy board data from course lecture notes.
- **`game_logic.py`**: Manages the session state—tracking scores, answered questions, and active clues—while systematically evaluating user responses for accuracy.
- **`ui.py`**: Renders the visual components, including the interactive Jeopardy board and clue views, and wires user interactions (clicks, text input, and buttons) back to the underlying game logic.
- **`config.py`**: Centralizes shared configurations, such as the API base URL for the model proxy.

### Game Flow

1. **Initialization and Setup**
   - Executing `streamlit run main.py` triggers the `main()` function, which loads environment variables from `.env` and verifies the presence of the `ASTRO1221_API_KEY`.
   - The `init_session_state()` function (from `game_logic.py`) populates `st.session_state` with required default values, including the `game_board` structure, a set of `answered_questions`, the user's `score`, the `current_clue`, the `answer_input`, and `last_token_usage` for LLM token tracking.
   - Users can initiate a session via the **"New Game"** button in the sidebar, invoking `generate_game_data()` to construct a new board and reset all progress.

2. **Dynamic Board Generation**
   - **Standard Categories**: `generate_game_data()` builds a system prompt directing the LLM to generate four astronomy-themed categories. Each category contains five clues with escalating point values ($200, $400, $600, $800, $1000). The prompt prohibits overly basic topics (e.g., generic "Solar System / Planets" questions) and strictly enforces a JSON-only response matching a precise `"categories"` schema. The model is invoked via LiteLLM using `response_format={"type": "json_object"}`, and the output is parsed and validated by `validate_game_data()`.
   - **Lecture-Specific Category**: Independently, `generate_lectures_category()` utilizes `search_chunks()` (from `rag_lectures.py`) to retrieve relevant segments from course lecture notes. These chunks—truncated at natural sentence boundaries—form the context for a secondary LLM prompt, which generates a fifth "Lectures" category featuring five appropriately valued clues.
   - **Consolidation**: The four LLM-generated categories and the single RAG-powered category are merged, re-validated, and securely stored in `st.session_state.game_board`.

3. **Data Representation**
   - The generated `game_board` dictionary consists of a `"categories"` array.
   - Each category object contains a `"name"` (title) and a `"clues"` array.
   - Individual clues are represented as objects containing a `"value"` (integer), `"clue"` (the question string), and `"answer"` (the correct response string).

4. **Board Rendering**
   - Rendered by `render_board()` in `ui.py`, the interface benefits from global CSS enhancements injected via `inject_global_styles()`.
   - The board displays as a grid, featuring category headers across the top row and corresponding point-value buttons directly below.
   - Unanswered clues display their dollar value (e.g., `$200`). Once answered, the button updates to "—" and is disabled.
   - Clicking an active point value triggers `set_current_clue()` and refreshes the UI to display the clue view.

5. **Clue Selection and Display**
   - `set_current_clue(cat_idx, clue_idx)` isolates the selected clue from the `game_board`.
   - It constructs a `current_clue` dictionary that captures category details, the clue's text and value, the correct answer, and a dynamically generated list of multiple-choice options. These options combine the correct answer with up to three randomized distractors sourced from other clues, which are then shuffled.
   - Streamlit subsequently replaces the main board with `render_current_clue()`.

6. **Answer Evaluation**
   - The clue view presents the category, point value, and text, alongside a free-response input field.
   - Available actions include **"Submit answer"**, **"💡 Hint"** (which switches the input to a multiple-choice radio button format based on the generated distractors), and **"Give Up"**.
   - **Submitting an Answer**: `check_answer()` normalizes both the user's input and the correct answer by removing standard Jeopardy prefixes (e.g., "what is", "who is"), dropping leading articles ("the", "a", "an"), and standardizing punctuation and casing. It then utilizes `difflib.get_close_matches` with a similarity cutoff to seamlessly accommodate minor typos.
     - *Correct Answer*: Displays a success message and adds the clue's value to the score.
     - *Incorrect Answer*: Reveals the correct response and deducts the corresponding points.
   - **Giving Up**: Directly reveals the correct answer without adjusting the score, marks the clue as answered, and clears the active clue.
   - Post-evaluation, the system updates `answered_questions`, clears the clue state, pauses briefly, and triggers `st.rerun()` to return the user to the main board.

7. **State Persistence**
   - Streamlit's `st.session_state` ensures complete continuity across reruns, safely retaining the `game_board`, `answered_questions`, `score`, `current_clue`, `show_hints` toggle, and `last_token_usage` metrics throughout the lifecycle of the application.

### Running the Application

1. Create a `.env` file in the project's root directory and configure your API key:
   ```env
   ASTRO1221_API_KEY=<your_key_here>
   ```
2. Install the necessary dependencies (minimum requirements: `streamlit`, `litellm`, `sentence_transformers`, and `python-dotenv`).
3. Launch the application from your terminal:
   ```bash
   streamlit run main.py
   ```
4. Open the provided local URL in your web browser, click **New Game**, and enjoy the quiz!