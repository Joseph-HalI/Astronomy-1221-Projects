# Streamlit: From Python Scripts to Web Apps

## Introduction:

It's office hours. Your classmate walks in, excited: "I heard you built that amazing large language model system for searching through astronomy papers! Can I try it?"

"Of course!" you reply confidently. "Let me show you how to use it."

What happens next turns your confidence into mild panic:

"First, install Python 3.8 or higher... wait, do you have pip? Okay, now pip install anthropic, but actually use pip3 if... hold on, you need sentence-transformers too, that's pip install sentence-transformers. Oh, you're getting an error? Right, you need to upgrade pip first. Now create a .env file—no, that's dot-E-N-V—and add your API key... actually, you need to get an API key first from... wait, why is numpy failing to install? Let me check your Python version again..."

Twenty minutes later, your classmate politely says they'll "try it later" and leaves. Your powerful tool, which could have helped them find relevant papers in seconds, never got the chance to shine.

This scenario repeats itself constantly in astronomy research. You build something useful—a magnitude calculator, a FITS file viewer, a period-finding tool—but sharing it requires your users to become system administrators first.

Today, we fix this problem forever.

### From Terminal to Browser

Over the past nine lectures, you've built an impressive toolkit. You started with variables and loops, mastered NumPy arrays that slice through data like a hot knife through butter, created visualizations that revealed hidden patterns, and just last week, you learned to preserve your code forever on GitHub. You even taught LLMs to execute calculations and search through documents with the sophistication of a research assistant.

But here's the uncomfortable truth: all of that power is trapped inside your terminal.

Today, you'll learn to break your code free from the terminal and deliver it directly to anyone with a web browser. No installation. No configuration. No terminal commands. Just a link they can click and a beautiful interface they can use immediately.

By the end of this lecture, your Python systems will run in a browser with elegant interfaces. Your complete AI assistant—the one that chooses between calculations and document search—will work through a chat-like interface. And here's the best part: you'll do all of this with just Python. No HTML, no CSS, no JavaScript—just the Python you already know, plus a magical library called Streamlit.

Let's transform your scripts into apps.

## Understanding Streamlit

Streamlit is a Python library that performs a specific kind of magic: it turns your Python scripts into interactive web applications, automatically. No web development knowledge required. No servers to configure. No databases to set up. Just Python code that becomes a living, breathing web interface.

Think of Streamlit as a translator between two worlds. In one world, you have your Python code—functions, variables, calculations, all the things you've learned over nine lectures. In the other world, you have web browsers expecting HTML, CSS, and JavaScript. Streamlit stands between these worlds and translates everything automatically. You speak Python; your users see a beautiful web application.

Streamlit was created by machine learning engineers who were frustrated with the exact problem you face. They had powerful Python tools—data processing pipelines, machine learning models, visualization scripts—but sharing them required either teaching everyone to code or hiring web developers. Neither option was good. So they built Streamlit to solve their own problem, and now we all benefit.

### Streamlit vs Jupyter Notebooks

You might wonder: "I already use Jupyter notebooks, which run in a browser. Why do I need Streamlit?"

Jupyter notebooks are incredible for development and analysis—that's why we've used them all semester. But they're designed for people who write code. Your users see code cells, error messages, import statements, and all the scaffolding of programming. It's like inviting someone to dinner and making them watch you cook—interesting for some, overwhelming for most.

Streamlit apps hide all the code complexity. Your users see only the interface: buttons to click, text to enter, results to view. It's like serving the finished meal—they enjoy the result without seeing the kitchen chaos.

Here's a visual comparison:

* **Jupyter**: Code visible → User must understand Python → Can break things → Requires installation
* **Streamlit**: Code hidden → User just interacts → Can't break things → Runs in any browser

But there's a deeper difference that matters for scientific applications. Jupyter notebooks are stateful—each cell execution changes the kernel's state, and you can run cells out of order. This is powerful for exploration but confusing for users. Streamlit apps run top to bottom on every interaction, ensuring consistent behavior. Your users can't accidentally break the app by clicking things in the wrong order.

## Building Your First Streamlit App

### Installation and Setup

Let's stop talking about Streamlit and start using it. We'll create the simplest possible app, run it, and then gradually add features. This hands-on approach will make everything concrete.

Install Streamlit (run this in your terminal or notebook):

```
pip install streamlit
```

That's it. No complex setup, no configuration files, no servers to install. Just one package. Behind the scenes, this installs Streamlit and its dependencies—a web server (Tornado), a communication protocol (WebSockets), and various utilities. But you don't need to know about any of that.

### Creating Your First App

In Cursor, create a new file called `hello_streamlit.py`. Important: this must be a regular Python file (`.py`), not a Jupyter notebook (`.ipynb`)! Streamlit runs Python scripts, not notebooks. This distinction matters because notebooks have cells and state, while scripts run linearly from top to bottom—exactly what Streamlit expects.

Add these lines:

```
# hello_streamlit.py
import streamlit as st

st.write("# Welcome to Astronomy Tools")
st.write("This is my first Streamlit app!")

# Let's add some astronomy content
parallax = 0.768  # Proxima Centauri's parallax in arcseconds
distance = 1.0 / parallax
st.write(f"Distance to Proxima Centauri: {distance:.2f} parsecs")
```

Notice something beautiful here: `st.write()` is intelligent. It accepts markdown (the `#` becomes a header), plain text, formatted strings, numbers, DataFrames, plots—almost anything. It figures out what you're giving it and displays it appropriately. This is Streamlit's philosophy: make the common case easy.

Save this file in a folder you can easily find—perhaps create a new folder called `streamlit_apps` on your Desktop.

### Running Your App

We need to run Streamlit from the terminal. The easiest way is to use Cursor's built-in terminal:

1. In Cursor, click **Terminal** → **New Terminal** in the top menu
2. A terminal panel opens at the bottom of Cursor
3. Navigate to your file's folder using `cd` (if needed)
4. Run your app:

```
streamlit run hello_streamlit.py
```

Press Enter, and magic happens:

* Your default browser opens automatically (if it doesn't, look in the terminal for a URL)
* You see your app running at `http://localhost:8501`
* Your Python code has become a web page!

What does `localhost:8501` mean? `localhost` means "this computer"—your app is running on your own machine, not on the internet. `8501` is the port number—think of it as the specific door through which your browser talks to Streamlit. This is important: your app is completely private right now. No one else can see it unless they're using your computer.

To stop the app later, press `Ctrl+C` in the terminal.

### The Live Reload Experience

Keep your browser open showing your app. Now go back to your code and change something:

```
st.write("This is my first Streamlit app! 🌟")  # Added a star emoji
```

Save the file (`Cmd+S` or `Ctrl+S`). Look at your browser—Streamlit detected the change! A message appears saying "Source file changed". You can either:

* Click "Rerun" to update immediately
* Click "Always rerun" to make updates automatic

This live reload feature transforms development. You can tweak your interface, adjust calculations, fix bugs—all while seeing results instantly. It's like having a conversation with your code.

## Interactive Components

### Understanding Script Reruns

Streamlit has a radically simple execution model: your entire script runs from top to bottom on every interaction. Every. Single. Time. This isn't a bug or inefficiency—it's the core design principle that makes Streamlit so easy to reason about.

Let's prove this empirically:

```
# rerun_demo.py
import streamlit as st
import datetime

st.title("Understanding Reruns")
st.write(f"Script ran at: {datetime.datetime.now().strftime('%H:%M:%S.%f')}")

temperature = st.slider("Temperature (K):", 3000, 10000, 5778)
st.write(f"Selected: {temperature}K")
```

Run this and move the slider—the timestamp changes every time! Your entire script reruns with each interaction.

This rerun behavior has profound implications. In traditional GUI programming, you attach callbacks to events: "when button clicked, run this function." In web development, you handle events: "on form submit, process data." Streamlit inverts this model entirely. There are no callbacks, no event handlers, no listeners. Just a script that runs repeatedly with current widget values.

This is why Streamlit code reads like a story. You don't write "when the user changes the temperature slider, recalculate the Wien peak." You write "get the temperature from the slider, calculate the Wien peak." The calculation happens automatically whenever the temperature changes because the script reruns.

The mental shift is significant. Stop thinking about events and start thinking about state. Your widgets hold state. Your script reads that state and produces output. When state changes, the script runs again with new state. It's functional programming applied to user interfaces—pure functions (your script) operating on immutable state (widget values).

### Text Input: The Foundation

The simplest widget accepts text from users:

```
# text_input.py
import streamlit as st

name = st.text_input("Star name:", "Vega")
st.write(f"You entered: {name}")
```

The text input returns its current value directly. No callbacks, no event handlers—just a simple assignment. The second parameter ("Vega") is the default value.

### Number Input: Precision Matters

Scientific computing demands numerical precision:

```
# number_input.py
import streamlit as st
import numpy as np

magnitude = st.number_input("Apparent magnitude:", value=0.03, step=0.01)
# Calculating absolute magnitude assuming distance to Vega (7.68 parsecs)
distance = 7.68  # parsecs
absolute_mag = magnitude - 5 * np.log10(distance/10)
st.write(f"Absolute magnitude at 10pc: {absolute_mag:.2f}")
```

The `step` parameter controls the increment/decrement buttons, essential for fine-tuning scientific values.

### Sliders: Exploration Through Motion

Sliders transform parameter exploration into a visceral experience:

```
# slider.py
import streamlit as st

radius = st.slider("Radius (R☉):", 0.1, 10.0, 1.0)
volume = (4/3) * 3.14159 * radius**3
st.write(f"Volume: {volume:.2f} V☉")
```

The slider shows min, max, and default value. Users can click or drag to select.

### Checkboxes: Binary Decisions

Not all choices are continuous. Checkboxes handle binary decisions elegantly:

```
# checkbox.py
import streamlit as st

show_details = st.checkbox("Show calculation details")
result = 42
st.write(f"Answer: {result}")

if show_details:
    st.write("Calculation: 6 × 7 = 42")
```

Checkboxes return `True` when checked, `False` when unchecked. They maintain their state between reruns. The power of checkboxes lies in conditional display—they let users control interface complexity: simple by default, detailed on demand.

### Selectboxes: Discrete Choices

When options are discrete but not binary, selectboxes provide structure:

```
# selectbox.py
import streamlit as st

star_type = st.selectbox(
    "Stellar class:",
    ["O", "B", "A", "F", "G", "K", "M"]
)
st.write(f"You selected a {star_type}-type star")
```

Selectboxes enforce valid choices. Users can't enter "Z-type star"—they must choose from provided options. This validation happens automatically, preventing errors downstream.

### Buttons: The Trigger Paradigm

Buttons are fundamentally different from other widgets:

```
# button_behavior.py
import streamlit as st

if st.button("Calculate"):
    st.write("Button clicked! This disappears on next interaction.")
    st.balloons()  # Fun animation!
```

Buttons are `True` only when clicked, returning to `False` on the next rerun. This transient behavior makes buttons perfect for triggering actions rather than maintaining state.

Why this special behavior? Consider the alternative. If buttons stayed `True` after clicking, every rerun would re-execute the button's action. Click "Send Email" once, emails send forever! The transient nature prevents repeated actions.

To see the contrast:

```
# button_vs_checkbox.py
import streamlit as st

if st.button("Temporary"):
    st.write("I disappear!")

if st.checkbox("Persistent"):
    st.write("I stay visible!")
```

The button returns to `False` after the script reruns, while the checkbox maintains its state.

### Layout with Columns

Professional interfaces need spatial organization:

```
# columns.py
import streamlit as st

col1, col2 = st.columns(2)

with col1:
    st.header("Input")
    temp = st.slider("Temperature:", 3000, 10000)

with col2:
    st.header("Output")
    st.write(f"Wien peak: {2.898e6/temp:.0f} nm")
```

Columns create logical groupings and visual relationships. Input on the left, output on the right—a pattern users understand intuitively. The context manager syntax (`with col1:`) is pythonic and clear. Everything within the context appears in that column.

You can specify relative widths:

```
# column_widths.py
col1, col2, col3 = st.columns([2, 1, 2])  # 2:1:2 ratio
```

This fine control lets you create information hierarchies. Wide columns for primary content, narrow columns for controls or metadata.

## Handling Data and Performance

### The Hidden Cost of Simplicity

Streamlit's rerun model makes development beautifully simple—your script runs top to bottom, widgets return values, everything updates automatically. But this simplicity has a cost that becomes painfully obvious when you add slow operations to your app.

Imagine you're building a stellar catalog analyzer. Loading the catalog takes a few seconds—reading from disk, parsing formats, building indices. In a traditional script, you load once and analyze many times. In Streamlit's rerun model, without intervention, you'd reload on every single interaction.

Let's see this problem in action:

```
# slow_problem.py
import streamlit as st
import time

def load_data():
    time.sleep(2)  # Simulates slow loading
    return "Large dataset"

data = load_data()  # This runs EVERY time!
slider = st.slider("Any value:", 1, 10)
```

Try this app—every slider movement triggers a 2-second wait! This is completely unusable.

The problem compounds with real scientific data. Loading a Gaia catalog might take 10 seconds. Complex calculations on that data might take another 5. Image processing might add more. Without a solution, your app would spend minutes reloading data that hasn't changed.

This isn't a flaw in Streamlit's design—it's a trade-off. The rerun model eliminates complexity around state management, event handling, and synchronization. But it requires us to explicitly mark expensive operations that shouldn't repeat.

### The Caching Solution

Streamlit's answer to the performance problem is memoization—remembering function results and reusing them when appropriate. The `@st.cache_data` decorator implements this pattern elegantly:

```
# caching_solution.py
import streamlit as st
import time

@st.cache_data  # Magic happens here!
def load_data():
    time.sleep(2)  # Only runs once!
    return "Large dataset"

data = load_data()  # Instant after first call
slider = st.slider("Any value:", 1, 10)
```

The transformation is dramatic. The first run still takes 2 seconds—data must load initially. But subsequent runs return instantly. Moving the slider no longer triggers a reload. The app feels responsive.

### Caching with Parameters

Real functions take parameters. Caching handles this naturally—each unique parameter combination gets its own cache entry:

```
# cache_params.py
import streamlit as st

@st.cache_data
def compute_expensive(n):
    # Each value of n gets cached separately
    return n ** 2

value = st.slider("N:", 1, 100)
result = compute_expensive(value)  # Only computed once per value
st.write(f"{value}² = {result}")
```

This creates up to 100 cache entries—one per slider position. Memory is cheap compared to computation time. If users frequently revisit certain values (common in exploration), they get instant results.

### Caching File Operations

File I/O is notoriously slow—network latency, disk seeking, parsing overhead. Always cache file operations:

```
# cache_files.py
import streamlit as st

@st.cache_data
def load_catalog(filename):
    with open(filename) as f:
        return f.read().splitlines()

# This only reads the file once
stars = load_catalog("stars.csv")
st.write(f"Loaded {len(stars)} stars")
```

This pattern is essential for scientific applications. Astronomical catalogs can be gigabytes. FITS files require complex parsing. CSV files need type inference. Without caching, every interaction would re-read, re-parse, re-process. With caching, you pay the cost once per session.

### Knowing When NOT to Cache

Caching isn't free. It uses memory, adds overhead, and complicates debugging. Don't cache simple operations:

```
# no_cache_needed.py
# ❌ Don't cache this - it's instant
def calculate_distance(parallax):
    return 1.0 / parallax

# ✅ Do cache this - it's slow
@st.cache_data
def load_huge_catalog():
    # Expensive operation
    pass
```

Simple rule: If it feels slow when using the app, add `@st.cache_data`.

Common operations that DON'T need caching:

* Simple math calculations
* String formatting
* List comprehensions under 1000 items
* Dictionary lookups
* Most NumPy operations on small arrays

Common operations that DO need caching:

* File I/O of any size
* Network requests
* Database queries
* Machine learning predictions
* Image processing
* Large matrix operations
* Parsing complex formats

### Manual Cache Management

Sometimes you need explicit control over the cache:

```
# clear_cache.py
import streamlit as st

if st.button("Clear all cache"):
    st.cache_data.clear()
    st.success("Cache cleared!")
```

This nuclear option clears everything when needed—useful for debugging or when external data sources update.

## Visualizations and File Handling

Scientific data demands visualization. Numbers in tables reveal patterns slowly; plots reveal them instantly. Throughout this course, you've created matplotlib figures in Jupyter notebooks, carefully crafting visualizations that illuminate your data. Now we need those same visualizations in our web apps, responsive to user input and beautifully integrated into the interface.

The challenge is that matplotlib was designed for static output—papers, presentations, notebooks. Streamlit bridges this gap, taking your matplotlib figures and embedding them seamlessly into web interfaces. Your plotting knowledge transfers directly; only the display mechanism changes.

### Basic Matplotlib Integration

The integration between Streamlit and matplotlib is beautifully simple. Create your figure exactly as you learned, then hand it to Streamlit:

```
# basic_plot.py
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()
x = np.linspace(0, 2*np.pi, 100)
ax.plot(x, np.sin(x))
st.pyplot(fig)
```

The key is passing the figure object to `st.pyplot()`.

This single function, `st.pyplot()`, performs considerable magic. It captures the matplotlib figure, converts it to a web-friendly format (PNG or SVG), embeds it in the HTML stream. All the complexity of web image handling vanishes behind one function call.

### Interactive Plots

Static plots inform; interactive plots engage. Combining Streamlit widgets with matplotlib creates dynamic visualizations:

```
# interactive_plot.py
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

freq = st.slider("Frequency:", 1, 10, 3)

fig, ax = plt.subplots()
x = np.linspace(0, 2*np.pi, 100)
ax.plot(x, np.sin(freq * x))
st.pyplot(fig)
```

The plot updates automatically when the slider moves! This automatic update is Streamlit's rerun model at its best. Moving the slider triggers a rerun, the script executes with the new frequency value, matplotlib generates a new figure, and Streamlit displays it.

This pattern scales to complex visualizations. Imagine a Hertzsprung-Russell diagram where users adjust stellar population parameters, or a light curve where users test different periods. The same pattern—widget changes value, plot uses value, display updates—handles any complexity.

### File Uploads: Bringing User Data

Your app shouldn't be limited to built-in datasets. Real scientific work requires analyzing user data—their observations, their measurements, their discoveries:

```
# file_upload.py
import streamlit as st

uploaded = st.file_uploader("Choose a file", type="txt")

if uploaded is not None:
    content = uploaded.read().decode('utf-8')
    st.write(f"File contains {len(content)} characters")
    st.text(content[:500])  # Show first 500 chars
```

The uploader returns `None` until a file is selected, then a file-like object. This object behaves like a file opened with Python's `open()`—you can `.read()` it, seek through it, or get its name and size.

The `type` parameter accepts single extensions (`"txt"`), lists (`["csv", "txt"]`), or None (any file). This filtering happens browser-side, guiding users to appropriate files.

### Enabling Downloads

Analysis without export is incomplete. Users need to save results, share findings, and preserve outputs:

```
# download.py
import streamlit as st

result = "star,magnitude\nVega,0.03\nSirius,-1.46"

st.download_button(
    label="Download CSV",
    data=result,
    file_name="stars.csv",
    mime="text/csv"
)
```

The download button generates files client-side, triggers browser's download dialog, and names files appropriately. The `mime` type tells browsers how to handle the file—`text/csv` for CSVs, `text/plain` for text, `application/pdf` for PDFs.

This completes the data cycle: upload, process, download. Your app becomes part of their workflow, not a dead end.

### Progress Indicators: Managing Expectations

Humans hate uncertainty more than waiting. Progress indicators transform frustrating waits into acceptable pauses:

```
# spinner.py
import streamlit as st
import time

if st.button("Process"):
    with st.spinner("Working..."):
        time.sleep(2)
    st.success("Done!")
```

The spinner shows while the code inside the `with` block runs. The message should be informative ("Processing 1000 stars...") not generic ("Loading...").

### Progress Bars for Known Operations

When you know the steps, show the progress:

```
# progress_bar.py
import streamlit as st
import time

if st.button("Analyze"):
    progress = st.progress(0)
    for i in range(100):
        progress.progress(i + 1)
        time.sleep(0.01)
```

Progress bars transform anxiety into anticipation. Users see movement, estimate completion time, and feel the app is working.

### Communicating with Status Messages

Different situations require different messaging:

```
# messages.py
import streamlit as st

st.info("ℹ️ Upload a file to begin")
st.success("✅ File processed successfully")
st.warning("⚠️ Large file may be slow")
st.error("❌ Invalid file format")
```

Each creates a colored box with appropriate styling. Info (blue) provides guidance without alarm. Success (green) confirms positive outcomes. Warning (yellow) alerts to potential issues without blocking progress. Error (red) indicates failure requiring action.

## Building Chat Interfaces

Chat applications present a unique challenge in Streamlit's rerun model. Conversations are inherently stateful—each message builds on previous ones. But Streamlit reruns your entire script on every interaction, resetting all variables to their initial values.

Let's see why this is problematic:

```
# broken_chat.py - This WON'T work!
import streamlit as st

messages = []  # Resets on every rerun!
user_input = st.text_input("Say something:")
if user_input:
    messages.append(user_input)
    st.write(messages)  # Only shows one message
```

Every time you type a new message, the script reruns from the top. The `messages` list is recreated empty, your new message is added to that empty list, and you see only the latest message. The conversation history vanishes with each interaction.

### Understanding Session State

Session state is Streamlit's answer to the persistence problem. Think of it as a notebook that Streamlit keeps for each user session, preserving information between script reruns:

```
# session_state_intro.py
import streamlit as st

# Initialize once per session
if "counter" not in st.session_state:
    st.session_state.counter = 0

if st.button("Increment"):
    st.session_state.counter += 1

st.write(f"Count: {st.session_state.counter}")
```

The counter survives reruns! Session state is a dictionary that persists until the user refreshes the page.

The pattern `if "key" not in st.session_state:` is crucial—it means "initialize this only if it doesn't exist yet." This pattern appears in almost every Streamlit app that needs memory.

### Building Chat Memory

With session state understood, we can build functioning chat memory:

```
# chat_memory.py
import streamlit as st

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("Message:")
if user_input:
    st.session_state.messages.append(user_input)

for msg in st.session_state.messages:
    st.write(f"• {msg}")
```

Now messages accumulate! This simple pattern—initialize once, append new data, display everything—forms the foundation of all Streamlit chat interfaces.

### Chat-Specific UI Components

Streamlit provides specialized components that create professional chat interfaces:

```
# chat_display.py
import streamlit as st

with st.chat_message("user"):
    st.write("Hello!")

with st.chat_message("assistant"):
    st.write("Hi there!")
```

This creates chat bubbles with avatars. The `st.chat_message()` context manager creates:

* **Avatar**: Automatic icon based on role (user/assistant/system)
* **Alignment**: User messages typically right-aligned, assistant left
* **Styling**: Professional chat bubble appearance
* **Containment**: Everything inside the context appears in the bubble

### The Chat Input Widget

Standard text inputs work for chat, but Streamlit's dedicated chat input is better:

```
# chat_input.py
import streamlit as st

if prompt := st.chat_input("Say something"):
    st.write(f"You said: {prompt}")
```

The walrus operator (`:=`) assigns and checks in one line—it assigns the input to `prompt` AND checks if it's not empty. This is perfect for chat interfaces where you only want to react to actual messages.

The chat input appears at the bottom of the screen (like messaging apps), submits on Enter (no button needed), and clears after submission.

### Assembling a Complete Chat Interface

Combining these pieces creates a functioning chat system:

```
# simple_chat.py
import streamlit as st

# Initialize
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Handle input
if prompt := st.chat_input("Type here"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Add response
    response = f"Echo: {prompt}"
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
```

Notice the message structure: dictionaries with "role" and "content" keys. This format matches what most AI APIs expect (OpenAI, Anthropic, Google).

### Security Considerations for API Keys

Chat interfaces often connect to AI services requiring API keys. Security is paramount:

```
# secure_key.py
import streamlit as st

api_key = st.text_input("API Key:", type="password")

if api_key:
    st.success("✅ Key provided")
else:
    st.warning("⚠️ Enter API key to continue")
```

The `type="password"` hides the input as dots—keys are masked, excluded from autofill, and treated as sensitive by browsers.

### Patterns for API Integration

When integrating with AI services:

```
# api_pattern.py
import streamlit as st

api_key = st.sidebar.text_input("API Key", type="password")

if prompt := st.chat_input("Ask something"):
    if not api_key:
        st.error("Please add API key")
    else:
        with st.spinner("Thinking..."):
            # Make API call here
            response = "API response"
        st.write(response)
```

Placing the API key in the sidebar keeps it accessible but out of the way. The spinner provides crucial feedback during API calls.

### Complete Claude Integration

Here's how everything combines for a real AI chat:

```
# claude_minimal.py
import streamlit as st
from anthropic import Anthropic

st.title("Claude Chat")

api_key = st.sidebar.text_input("Claude API Key", type="password")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input and response
if prompt := st.chat_input("Message"):
    if api_key:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get Claude response
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=200,
            messages=st.session_state.messages
        )
        
        # Add assistant message
        answer = response.content[0].text
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
        # Display
        with st.chat_message("assistant"):
            st.write(answer)
```

This minimal implementation maintains conversation history, handles the full message cycle, and integrates cleanly with Claude's API.

## Deployment to the Cloud

Right now, your app runs at `localhost:8501`. This should look familiar—you've seen `localhost` URLs before when running Jupyter notebooks! Just like Jupyter runs at `localhost:8888`, Streamlit uses `localhost:8501`. When you run `streamlit run app.py`, your computer becomes a web server, but it's a private party. The `localhost` part means "this computer only." The `:8501` is the port number—the specific door Streamlit uses to communicate (different from Jupyter's `:8888` port). Even if you send the `localhost:8501` link to a friend, they'll get an error, just like they would with your Jupyter notebook URLs. Your app is trapped on your machine.

To share your app with the world, we need to deploy it to the cloud. Streamlit provides free hosting that makes deployment take just minutes.

### The Deployment

The path from local app to live website has three stages: prepare your files, push to GitHub, and deploy to Streamlit Cloud.

**Step 1: Prepare Your Project**

Your repository should look like this:

```
stellar-magnitude-calculator/
├── app.py                     # Your main Streamlit app
├── requirements.txt           # Tells Streamlit what packages to install
├── .gitignore                 # Files to keep private
└── README.md                  # Optional but professional
```

The critical file is `requirements.txt`. This tells Streamlit's servers what packages your app needs:

```
streamlit
numpy
matplotlib
anthropic  # Only include if you're using Claude
```

You also need a `.gitignore` file to keep sensitive files off GitHub. This is crucial for security.

**Step 2: Push to GitHub**

Using Cursor's Source Control panel (you learned this in Lecture 9), commit your files with a meaningful message like "Initial Streamlit app for stellar classification" and push to a new repository.

When naming your repository, choose something descriptive: `stellar-classifier` is better than `project1`. Your code must be on GitHub for Streamlit Cloud to access it.

**Step 3: Deploy to Streamlit Cloud**

Navigate to [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account. Click "New app" and you'll see a deployment form with:

* **Repository**: Select your repo from the dropdown
* **Branch**: Usually `main` (sometimes `master` for older repos)
* **Main file path**: The path to your `.py` file (usually just `app.py`)

Consider the advanced settings—you can choose a custom URL like `stellar-calculator.streamlit.app` instead of a random string. Choose wisely; this URL becomes permanent!

Click "Deploy!" and watch the magic happen. Streamlit spins up a container, installs Python, reads your `requirements.txt`, installs all packages, and runs your app. In 2-3 minutes, your app is live. Anyone, anywhere in the world, can visit your URL and use your app. They don't need Python. They just click your link.

### Managing API Keys in Production

When your app uses APIs, you need to handle API keys carefully. There are two approaches:

#### Approach 1: Users Bring Their Own Keys

Most common for tools using expensive APIs:

```
api_key = st.text_input("Enter your API key:", type="password")

if not api_key:
    st.info("👈 Please enter your API key to continue")
    st.stop()
    
# Use their key for API calls
client = Anthropic(api_key=api_key)
```

Users control their own usage and costs. Your app becomes a tool that helps them use their API access more effectively.

#### Approach 2: You Provide the API Access

Sometimes you want to provide API access as part of your service. Streamlit Secrets lets you store API keys securely. In your app's dashboard (after deployment), navigate to Settings → Secrets and add your keys in TOML format:

```
ANTHROPIC_API_KEY = "sk-ant-api03-your-actual-key-here"
NASA_API_KEY = "your-nasa-key"
```

In your code:

```
import streamlit as st

api_key = st.secrets["ANTHROPIC_API_KEY"]
client = Anthropic(api_key=api_key)
```

For local development, create `.streamlit/secrets.toml` in your project with the same format. This file should NEVER go to GitHub—ensure it's in your `.gitignore`!

### The Magic of Continuous Deployment

Once deployed, your app updates automatically whenever you push changes to GitHub. Edit your code, commit and push using Source Control, and within seconds, Streamlit detects the change and rebuilds your app. Users see the updates in about a minute. No manual redeployment. No downtime.

This continuous deployment transforms how you develop. You can iterate quickly, fix issues immediately, and gradually improve your app based on user feedback.

## Professional Polish

The difference between a script and a professional application often comes down to small details. Users form opinions in seconds—a polished interface builds trust, while a rough one suggests unreliability.

### Page Configuration

Every Streamlit app should start with page configuration. This must be the first Streamlit command in your script:

```
# page_config.py
import streamlit as st

st.set_page_config(
    page_title="Star Analyzer",
    page_icon="🌟",
    layout="wide"
)
```

The `page_title` appears in the browser tab—crucial for users with many tabs open. The `page_icon` (favicon) can be an emoji or image file. The `layout` parameter fundamentally changes your app's appearance: "centered" for simple apps, "wide" for analytical tools.

### Custom Theme

Colors and typography dramatically affect perception. Create `.streamlit/config.toml` for custom colors:

```
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

Dark themes work well for astronomy apps—they reduce eye strain during night observing sessions.

### Multi-Page Apps

Complex applications need organization. Multi-page apps divide functionality into logical sections:

```
app/
├── Home.py
└── pages/
    ├── 1_Analysis.py
    └── 2_Help.py
```

Pages appear in the sidebar automatically. Files are sorted alphanumerically—hence the number prefixes. Each page is a complete Streamlit script with its own logic. Session state is shared across pages, enabling powerful workflows.

### Tooltips

Every field doesn't need a manual. Tooltips provide context without cluttering:

```
# tooltips.py
import streamlit as st

period = st.slider(
    "Period (days)",
    0.1, 100.0,
    help="Orbital or rotation period"
)
```

Good tooltips answer "What should I enter here?" without requiring users to leave the interface.

### Performance Tips Summary

Performance isn't just speed—it's perceived responsiveness:

1. **Cache expensive operations** with `@st.cache_data`
2. **Limit displayed data** - Show summaries first, details on demand
3. **Use progress indicators** for long operations
4. **Lazy load** with tabs and expanders
5. **Store results** in session state

These aren't optimizations—they're requirements for professional apps.

## Summary

### Key Concepts

In this lecture, you've learned:

* **Streamlit fundamentals**: How this Python library transforms scripts into interactive web applications without requiring web development knowledge
* **The rerun paradigm**: Streamlit's unique execution model where your entire script runs top-to-bottom on every interaction, simplifying state management
* **Interactive widgets and layouts**: Building user interfaces with sliders, buttons, text inputs, and columns that make your astronomical calculations accessible to non-programmers
* **Performance optimization**: Using `@st.cache_data` to prevent expensive operations from repeating and keep your apps responsive
* **Session state management**: Preserving data between reruns to build conversational interfaces and maintain application memory
* **Cloud deployment**: Publishing your apps to Streamlit Cloud through GitHub, making them globally accessible with automatic updates

### What You Can Now Do

After working through this material, you should be able to:

* Transform any Python analysis script into an interactive web application that runs in browsers without installation
* Create professional interfaces with widgets, visualizations, and file upload/download capabilities for astronomical data processing
* Build chat interfaces with memory that integrate with AI services like Claude for intelligent astronomical assistants
* Deploy applications to the cloud with proper API key management and continuous deployment from GitHub
* Optimize performance using caching strategies and progress indicators for computationally intensive astronomical calculations
* Design multi-page applications with professional polish including custom themes and tooltips

### Practice Suggestions

To solidify these concepts:

1. Convert your project into a Streamlit app with a chat interface, allowing users to interact with your AI assistant through their browser
2. Create an interactive stellar classification tool where users can upload observational data and see real-time classification results
3. Deploy at least one app to Streamlit Cloud, share the link with classmates, and iterate based on their feedback

### Looking Ahead

In the second half of this semester, you'll dive deep into **Pandas for astronomical data analysis**. The Streamlit skills you've mastered today will become even more powerful when combined with DataFrames—you'll build apps that load astronomical catalogs, perform complex queries, and visualize millions of stars interactively. Your ability to transform data analysis scripts into shareable web applications positions you to create tools that could enable the next great astronomical discovery.
