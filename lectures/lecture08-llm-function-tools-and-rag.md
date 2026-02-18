# Large Language Models: Function Tools and Retrieval Augmented Generation

## Introduction

Last lecture, you mastered the art of programmatic conversation with Claude. You learned to extract structured data from observation logs, analyze astronomical images, and build conversation systems that maintain context. But if you're like most students after Lecture 7, you probably noticed something: Claude was helpful at understanding and explaining astronomical concepts, but when it came to actual calculations, you were still doing all the mathematical work yourself.

Today, that changes. You're about to cross the threshold from having an AI that talks about astronomy to having an AI that does astronomy. By the end of this lecture, you'll command an AI assistant that can calculate stellar parallaxes, determine orbital periods, analyze light curves, and search through your entire course knowledge base—all while you focus on the science rather than the implementation details.

Consider this scenario: You're analyzing a dataset of binary star observations for your research project. You have radial velocity measurements over time, and you need to determine the orbital period and calculate the system's total mass. In the pre-function-tools world, this meant hours of looking up formulas, writing NumPy code, debugging array operations, and manually searching through lecture notes for the relevant theory.

In the post-function-tools world, you simply say: "Analyze this binary star dataset—determine the orbital period and calculate the total mass." Claude automatically calls your period-finding function with the radial velocity data, executes mass calculations using Kepler's laws, and returns a complete analysis with both computational results and theoretical context.

This isn't about replacing your astronomical knowledge—it's about amplifying it. Every function Claude calls uses physics you understand. Every calculation builds on mathematical concepts you've learned. But now these capabilities operate at machine speed and scale.

### Why Function Tools Transform Your Research

The transformation we're making today fundamentally shifts how you interact with computation. Instead of an assistant that knows things, you get an assistant that can do things.

**Claude as Information Source (Lecture 7):**

* You: "What's the formula for stellar luminosity?"
* Claude: "Here's the Stefan-Boltzmann law: L = 4πR²σT⁴"
* You: Spend 20 minutes implementing this in NumPy, debugging array shapes

**Claude as Computational Partner (Today):**

* You: "Calculate the luminosity of this star given its radius and temperature"
* Claude: Directly calls your `stellar_luminosity()` function with the parameters
* Claude: Returns the calculated result immediately, plus physical interpretation

But here's what matters: you're not becoming less capable—you're becoming more powerful. Every function Claude calls is one you understand and could write yourself (using skills from Lectures 1-6). Every calculation follows physics principles you've learned. Claude handles the mechanical execution; you provide the scientific direction, validation, and creative thinking.

This workflow mirrors how professional astronomy works. Research astronomers don't rewrite basic calculations from scratch for every project. They build libraries of tested functions and focus their mental energy on novel scientific questions. Today, you start building those libraries and learning to orchestrate them through AI collaboration.

## Understanding Function Tools

Function tools represent a fundamental shift in how LLMs interact with your code. Until now, when you asked Claude to calculate something, it would describe the calculation process in text. You then had to implement that calculation yourself in Python. Function tools eliminate this middle step—Claude can now directly execute Python functions you've written.

Think of it like the difference between having an assistant who can only read instruction manuals versus one who can actually operate the equipment. The first can tell you how to use a telescope; the second can actually point it at the stars and take measurements.

Here's the key concept: you write Python functions using all the skills you've learned—NumPy arrays from Lecture 4, matplotlib plots from Lecture 6, file operations from Lecture 3. Then you describe these functions to Claude in a special format called a "function schema." Once Claude knows about your functions, it can call them directly when answering questions.

**The Function Tool Workflow:**

1. **You define**: Write a Python function using familiar tools (just like Lecture 5)
2. **You describe**: Create a schema that tells Claude what the function does
3. **User asks**: Someone poses a question requiring calculation
4. **Claude decides**: Whether to use a function based on the question
5. **Claude requests**: Tells you which function to run with what parameters
6. **You execute**: Run the function and send results back
7. **Claude interprets**: Incorporates the results into a natural language response

When someone asks "What's the distance to a star with 0.05 arcsecond parallax?", Claude recognizes this requires calculation, requests your distance function with the parameter 0.05, and then explains the result in astronomical context.

### The Schema Concept

A function schema is like a user manual for your function—it tells Claude what the function does, what parameters it needs, and when to use it. Without a schema, Claude wouldn't know your function exists or how to use it.

Think of schemas as the bridge between natural language and code. When someone asks "What's the distance to Alpha Centauri if its parallax is 0.75 arcseconds?", the schema helps Claude understand:

* This question needs the `parallax_to_distance` function
* The function needs one parameter: `parallax_arcsec`
* The value for that parameter is 0.75

The schema format might look complex at first, but it's just a structured way to describe what you'd tell a colleague about your function: what it does, what inputs it needs, and what outputs it provides.

## Your First Function Tool

Let's create your first function tool step by step. We'll start with the simplest possible astronomical calculation and gradually build complexity.

### Setting Up the Environment

First, let's import what we need. Everything here should be familiar from previous lectures:

```
# Standard imports from previous lectures
import numpy as np  # For mathematical operations (Lecture 4)
import os          # For environment variables (Lecture 3)
from dotenv import load_dotenv  # For loading API keys (Lecture 7)
import anthropic   # For talking to Claude (Lecture 7)

# Load API key from .env file (same as Lecture 7)
load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

print("✓ Environment ready for function tools")
```

```
✓ Environment ready for function tools
```

### Creating a Simple Astronomical Function

Let's start with the most fundamental calculation in stellar astronomy: converting parallax to distance. The parallax of a star is the tiny angle it appears to shift when viewed from opposite sides of Earth's orbit. The smaller this angle, the farther away the star.

The relationship is beautifully simple: distance (in parsecs) = 1 / parallax (in arcseconds). One parsec is the distance at which a star would have a parallax of exactly one arcsecond.

```
def parallax_to_distance(parallax_arcsec):
    """
    Convert stellar parallax to distance in parsecs.
    
    The fundamental equation: d = 1/p
    where d is distance in parsecs and p is parallax in arcseconds.
    """
    # Input validation - always check for invalid inputs!
    if parallax_arcsec <= 0:
        return {"error": "Parallax must be positive"}
    
    # Calculate distance using the parallax formula
    distance_pc = 1.0 / parallax_arcsec
    
    # Return as a dictionary for structured data
    # We round to 2 decimal places for readability
    return {"distance_parsecs": round(distance_pc, 2)}
```

Let's test our function manually to make sure it works correctly. We'll use Proxima Centauri, our nearest stellar neighbor:

```
# Test with Proxima Centauri's parallax (0.768 arcsec)
test_result = parallax_to_distance(0.768)
print(f"Distance to Proxima Centauri: {test_result['distance_parsecs']} parsecs")
print(f"That's about {test_result['distance_parsecs'] * 3.26} light-years")

# Test error handling with invalid input
error_test = parallax_to_distance(-1)
print(f"\nError handling test: {error_test}")
```

```
Distance to Proxima Centauri: 1.3 parsecs
That's about 4.2379999999999995 light-years

Error handling test: {'error': 'Parallax must be positive'}
```

### Defining the Function Schema

Now we need to tell Claude about our function. A schema describes three key things:

1. **The function's name** - what Claude will call it
2. **What it does** - helps Claude know when to use it
3. **What inputs it needs** - the parameters and their types

The schema uses a specific format that might look intimidating at first, but it's just a nested dictionary structure (from Lecture 2). Let's build it step by step:

```
# Create a tools list with our function schema
tools = [
    {
        "name": "parallax_to_distance",  # The exact function name
        "description": "Calculate stellar distance from parallax measurement in arcseconds",
        "input_schema": {  # Describes what inputs the function needs
            "type": "object",  # The inputs are structured as an object
            "properties": {  # List of parameters
                "parallax_arcsec": {  # Parameter name (must match function)
                    "type": "number",  # This parameter is a number
                    "description": "Parallax angle in arcseconds (must be positive)"
                }
            },
            "required": ["parallax_arcsec"]  # This parameter is mandatory
        }
    }
]

print("✓ Function schema defined")
print(f"Claude now knows about {len(tools)} function(s)")
```

```
✓ Function schema defined
Claude now knows about 1 function(s)
```

### Making Your First Function Tool Call

Now for the exciting part—let's ask Claude a question and see if it recognizes that it needs to use our function. This is different from Lecture 7 because we're giving Claude the ability to request function execution:

```
# Ask Claude a question that requires our function
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=300,
    tools=tools,  # NEW! This gives Claude access to our functions
    messages=[{
        "role": "user", 
        "content": "What is the distance to a star with a parallax of 0.05 arcseconds?"
    }]
)

# The response type tells us what Claude wants to do
print(f"Claude's response type: {message.stop_reason}")
print(f"Number of content blocks in response: {len(message.content)}")
```

```
Claude's response type: tool_use
Number of content blocks in response: 2
```

### Understanding the Tool Response Structure

When Claude wants to use a tool, it doesn't just return text like in Lecture 7. Instead, it returns a structured response with multiple "blocks." Some blocks contain text (Claude's thoughts), and some contain tool requests (functions Claude wants to run).

Let's examine this structure carefully:

```
# Let's examine what Claude sent back
if message.stop_reason == "tool_use":
    print("Claude wants to use a function!\n")
    
    # Look at each block in the response
    for i, block in enumerate(message.content):
        print(f"Block {i}: Type = '{block.type}'")
        
        # Text blocks contain Claude's reasoning
        if hasattr(block, 'text'):
            print(f"  Text content: \"{block.text}\"")
        
        # Tool use blocks contain function requests
        if hasattr(block, 'name'):
            print(f"  Function to call: {block.name}")
            print(f"  Arguments to pass: {block.input}")
            print(f"  Unique ID for this call: {block.id}")
else:
    print("Claude responded with text only (no function needed)")
```

```
Claude wants to use a function!

Block 0: Type = 'text'
  Text content: "I'll calculate the distance to the star using its parallax measurement."
Block 1: Type = 'tool_use'
  Function to call: parallax_to_distance
  Arguments to pass: {'parallax_arcsec': 0.05}
  Unique ID for this call: toolu_01Qeq9kDRMScNvCREttow4uc
```

### Extracting the Tool Request

Claude has told us it wants to use a function, but it hasn't actually run anything yet. We need to extract the tool request, execute our Python function, and send the result back. This gives us full control over what code actually runs:

```
# The tool use request is typically the last content block
tool_use = message.content[-1]

print("Tool request details:")
print(f"  Function name: {tool_use.name}")
print(f"  Arguments: {tool_use.input}")
print(f"  Tool ID: {tool_use.id}")
print("\nThis ID is important - we need it to send results back to Claude!")
```

```
Tool request details:
  Function name: parallax_to_distance
  Arguments: {'parallax_arcsec': 0.05}
  Tool ID: toolu_01Qeq9kDRMScNvCREttow4uc

This ID is important - we need it to send results back to Claude!
```

### Executing the Function

Now we need to execute our function with the arguments Claude provided. Claude sends arguments as a dictionary like `{'parallax_arcsec': 0.05}`. We can extract the value and call our function:

```
# Execute our function with Claude's arguments
print(f"Claude wants to call: {tool_use.name} with {tool_use.input}")

# Extract the parallax value from the dictionary
parallax_value = tool_use.input['parallax_arcsec']
print(f"Extracted parallax value: {parallax_value}")

# Call our function
result = parallax_to_distance(parallax_value)
print(f"Function result: {result}")
```

```
Claude wants to call: parallax_to_distance with {'parallax_arcsec': 0.05}
Extracted parallax value: 0.05
Function result: {'distance_parsecs': 20.0}
```

### Completing the Conversation with Natural Language

This is a crucial step: we need to send the function result back to Claude so it can formulate a complete, natural language answer. Without this step, the user would just see raw function output instead of a helpful explanation. This is what transforms a simple calculation into a conversational response:

```
# Continue the conversation by sending the function result back to Claude
final_response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=200,
    tools=tools,
    messages=[
        # The original user question
        {
            "role": "user", 
            "content": "What is the distance to a star with a parallax of 0.05 arcseconds?"
        },
        # Claude's response requesting the function
        {
            "role": "assistant", 
            "content": message.content
        },
        # Our function result sent back to Claude
        {
            "role": "user", 
            "content": [{
                "type": "tool_result",
                "tool_use_id": tool_use.id,  # Must match the original request ID
                "content": str(result)  # Convert result to string
            }]
        }
    ]
)

print("Claude's final natural language answer:")
print("=" * 50)
print(final_response.content[0].text)
print("=" * 50)
print("\nNotice how Claude converts the raw number into a complete explanation!")
```

```
Claude's final natural language answer:
==================================================
The distance to a star with a parallax of 0.05 arcseconds is **20 parsecs**.

To put this in perspective:
- 20 parsecs = approximately 65.2 light-years
- This is a relatively nearby star in astronomical terms
- For comparison, the nearest star to our Sun (Proxima Centauri) is about 1.3 parsecs away

The relationship used here is the fundamental parallax-distance formula: distance (in parsecs) = 1 / parallax (in arcseconds).
==================================================

Notice how Claude converts the raw number into a complete explanation!
```

## Building Multiple Astronomical Functions

Now that you understand the complete workflow—from function definition to natural language response—let's expand your toolkit with more astronomical calculations. We'll see how Claude intelligently chooses between different functions based on the question.

### Adding a Stellar Luminosity Calculator

The Stefan-Boltzmann law tells us that a star's luminosity depends on its size and temperature. Specifically, L = 4πR²σT⁴, where σ is the Stefan-Boltzmann constant. This fundamental relationship lets us calculate how much energy a star emits:

```
def stellar_luminosity(radius_solar, temperature_k):
    """
    Calculate stellar luminosity using the Stefan-Boltzmann law.
    
    The energy radiated by a star depends on its surface area (4πR²)
    and how much energy each square meter emits (σT⁴).
    """
    # Physical constants
    stefan_boltzmann = 5.67e-8  # W m^-2 K^-4 (Stefan-Boltzmann constant)
    solar_radius = 6.96e8  # meters (Sun's radius)
    solar_luminosity = 3.83e26  # watts (Sun's total energy output)
    
    # Always validate inputs
    if radius_solar <= 0 or temperature_k <= 0:
        return {"error": "Radius and temperature must be positive"}
    
    # Convert stellar radius from solar units to meters
    radius_meters = radius_solar * solar_radius
    
    # Apply Stefan-Boltzmann law: L = 4πR²σT⁴
    luminosity_watts = 4 * np.pi * radius_meters**2 * stefan_boltzmann * temperature_k**4
    
    # Convert to solar luminosities for easier interpretation
    luminosity_solar = luminosity_watts / solar_luminosity
    
    return {
        "luminosity_solar": round(luminosity_solar, 3),
        "luminosity_watts": f"{luminosity_watts:.2e}"  # Scientific notation
    }
```

Let's verify our function works correctly by testing it with the Sun's values:

```
# Test with the Sun (should give ~1.0 solar luminosity)
sun_test = stellar_luminosity(1.0, 5778)  # Sun: 1 solar radius, 5778 K
print(f"Sun's calculated luminosity: {sun_test['luminosity_solar']} L☉")
print(f"In watts: {sun_test['luminosity_watts']} W")
print("(Should be very close to 1.0 solar luminosity!)")

# Test with a red giant
red_giant = stellar_luminosity(25, 3500)  # Typical red giant values
print(f"\nRed giant luminosity: {red_giant['luminosity_solar']} L☉")
print("(Much brighter than the Sun despite being cooler, due to larger size)")
```

```
Sun's calculated luminosity: 1.004 L☉
In watts: 3.85e+26 W
(Should be very close to 1.0 solar luminosity!)

Red giant luminosity: 84.521 L☉
(Much brighter than the Sun despite being cooler, due to larger size)
```

### Updating the Tools List

Now we need to tell Claude about both functions. Claude will automatically learn to choose the right function based on the question content—questions about distance will trigger the parallax function, while questions about brightness will trigger the luminosity function:

```
# Expanded tools list with both functions
tools = [
    {
        "name": "parallax_to_distance",
        "description": "Calculate stellar distance from parallax measurement",
        "input_schema": {
            "type": "object",
            "properties": {
                "parallax_arcsec": {
                    "type": "number",
                    "description": "Parallax in arcseconds (must be positive)"
                }
            },
            "required": ["parallax_arcsec"]
        }
    },
    {
        "name": "stellar_luminosity", 
        "description": "Calculate stellar luminosity from radius and temperature",
        "input_schema": {
            "type": "object",
            "properties": {
                "radius_solar": {
                    "type": "number",
                    "description": "Stellar radius in solar radii"
                },
                "temperature_k": {
                    "type": "number", 
                    "description": "Effective temperature in Kelvin"
                }
            },
            "required": ["radius_solar", "temperature_k"]
        }
    }
]

print(f"Claude now has access to {len(tools)} functions:")
for tool in tools:
    print(f"  • {tool['name']}")
```

```
Claude now has access to 2 functions:
  • parallax_to_distance
  • stellar_luminosity
```

### Creating a Complete Tool Execution Helper

Since we'll be executing tools frequently, let's create a helper function that handles the complete workflow from question to natural language answer. This will make our code cleaner, avoid repetition, and ensure we always get natural language responses:

```
def execute_tool_and_respond(question, tools):
    """
    Complete workflow: question → tool execution → natural language answer.
    
    This function handles the entire process we've been doing manually:
    1. Send question to Claude
    2. Execute requested function if needed
    3. Get natural language response
    """
    # Step 1: Ask Claude the question
    initial_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        tools=tools,
        messages=[{"role": "user", "content": question}]
    )
    
    # Check if Claude wants to use a tool
    if initial_response.stop_reason != "tool_use":
        # No tool needed, return direct response
        return initial_response.content[0].text
    
    # Step 2: Execute the requested function
    tool_use = initial_response.content[-1]
    
    # Execute the appropriate function based on name
    if tool_use.name == "parallax_to_distance":
        # Extract the parallax value and call function
        parallax = tool_use.input['parallax_arcsec']
        result = parallax_to_distance(parallax)
    elif tool_use.name == "stellar_luminosity":
        # Extract both parameters and call function
        radius = tool_use.input['radius_solar']
        temp = tool_use.input['temperature_k']
        result = stellar_luminosity(radius, temp)
    else:
        result = {"error": f"Unknown function: {tool_use.name}"}
    
    # Step 3: Send result back for natural language response
    final_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        tools=tools,
        messages=[
            {"role": "user", "content": question},
            {"role": "assistant", "content": initial_response.content},
            {
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": str(result)
                }]
            }
        ]
    )
    
    return final_response.content[0].text
```

Now let's test our complete workflow with different astronomical questions to see Claude choose the right tool and provide natural language answers:

```
# Test different types of questions
test_questions = [
    "What's the distance to Proxima Centauri if its parallax is 0.768 arcseconds?",
    "Calculate the luminosity of Betelgeuse with radius 700 solar radii and temperature 3500 K"
]

for question in test_questions:
    print(f"Question: {question}")
    print("\nAnswer:")
    answer = execute_tool_and_respond(question, tools)
    print(answer)
    print("\n" + "="*70 + "\n")
```

```
Question: What's the distance to Proxima Centauri if its parallax is 0.768 arcseconds?

Answer:
```

```
Based on a parallax of 0.768 arcseconds, Proxima Centauri is approximately **1.3 parsecs** away from Earth.

To put this in perspective:
- 1.3 parsecs = about 4.2 light-years
- This makes Proxima Centauri the closest known star to our Solar System (excluding the Sun)

The distance calculation uses the parallax formula: distance (in parsecs) = 1 / parallax (in arcseconds), which is why the larger parallax angle of 0.768" corresponds to this relatively close distance.

======================================================================

Question: Calculate the luminosity of Betelgeuse with radius 700 solar radii and temperature 3500 K

Answer:
```

```
Based on the calculations, Betelgeuse has a luminosity of approximately **66,264 solar luminosities** (L☉), which equals about **2.54 × 10³¹ watts**.

This extremely high luminosity is due to Betelgeuse's enormous size - despite having a relatively cool surface temperature of 3,500 K (compared to the Sun's 5,778 K), its massive radius of 700 solar radii gives it a total surface area that is 490,000 times larger than the Sun's. This enormous surface area more than compensates for the lower temperature, making Betelgeuse one of the most luminous stars known.

======================================================================
```

## Introduction to RAG (Retrieval Augmented Generation)

After seven weeks of lectures, you've accumulated a wealth of knowledge: Python fundamentals, NumPy operations, visualization techniques, and API usage. But here's a familiar problem: when working on your research projects and you need to remember "How did we handle errors in Lecture 3?" or "What was that matplotlib syntax from Lecture 6?", you end up with twenty browser tabs open, scrolling through notebooks trying to find that one code example.

This is exactly the problem that RAG (Retrieval Augmented Generation) solves. RAG combines document search with LLM reasoning, allowing you to ask questions like "Find all the error handling techniques we learned" and get comprehensive answers drawn directly from your course materials.

### What is RAG?

RAG stands for Retrieval Augmented Generation. Think of it as giving Claude access to your personal textbook—not just its general knowledge, but your specific lecture notes and examples.

The process has three steps:

1. **Retrieval**: Search through your documents to find relevant sections
2. **Augmentation**: Add those relevant sections to your question as context
3. **Generation**: Have Claude answer using both its knowledge and your specific materials

Without RAG, if you ask Claude "What did we learn about the temperature parameter?", it can only give general information about temperature parameters in LLMs. With RAG, it can tell you exactly what YOUR lecture notes say, with the specific examples and explanations from class.

### Understanding Markdown Files (.md)

Before we work with our lecture materials, let's understand what a markdown file is. You've actually been using markdown all semester—every text cell in your Jupyter notebooks uses markdown formatting!

**What is a .md file?**
A markdown file (with the extension .md) is a plain text file that uses simple symbols for formatting:

* `#` for headers (like `# Title` or `## Section`)
* `*` for italics and `**` for bold
* Three backticks (```) for code blocks
* `-` for bullet points

The beauty of markdown is that it's human-readable even without rendering. You can open a .md file in any text editor (like Cursor, Notepad, or TextEdit) and read it easily.

### Converting Jupyter Notebooks to Markdown with Jupytext

Your lecture materials are currently in Jupyter notebook format (.ipynb files), which contain both code and text mixed with metadata and output. To make them searchable for RAG, we need to convert them to plain markdown.

**Jupytext** is a tool that converts between different notebook formats. Think of it as a translator that can turn your .ipynb files into clean .md files. Here's how to use it:

First, install Jupytext:

```
pip install jupytext
```

To convert your notebook files to markdown, you would use Jupytext from the terminal:

```
jupytext --to md Lecture7_LLM_API_Basics_20250924.ipynb
```

This creates a file called `Lecture7_LLM_API_Basics_20250924.md` in the same folder. The markdown file contains all your text cells and code cells from the notebook, but in a clean text format perfect for searching.

For this lecture, we've already converted Lecture 7 to markdown format, so we can work with it directly. Let's read this file:

```
# Read the pre-converted lecture file
with open('Lecture7_LLM_API_Basics_20250924.md', 'r') as f:
    lecture7_content = f.read()
```

### Finding Section Headers in the Document

Markdown uses `#` symbols for headers. In our lecture file:

* `#` marks the main title
* `##` marks major sections
* `###` marks subsections

Let's find all the main topics covered in Lecture 7 using simple string methods you learned in Lecture 2:

```
# Find all main sections using string methods
sections = []
lines = lecture7_content.split('\n')  # Split into individual lines

for line in lines:
    # Check if line starts with '## ' (main section header)
    if line.startswith('## '):
        # Remove the '## ' to get just the title
        section_title = line[3:]  # Everything after '## '
        sections.append(section_title)

print(f"Found {len(sections)} main sections in Lecture 7:")
print()
for i, section in enumerate(sections[:8], 1):  # Show first 8
    print(f"  {i}. {section}")
if len(sections) > 8:
    print(f"  ... and {len(sections) - 8} more sections")
```

```
Found 11 main sections in Lecture 7:

  1. Introduction
  2. Understanding APIs
  3. Setting Up Your Connection
  4. Your First API Call
  5. Understanding the Parameters
  6. Building Conversations
  7. Prompting Strategies
  8. Making It Practical
  ... and 3 more sections
```

## Document Chunking

### Why We Need to Chunk Documents

Our Lecture 7 file contains tens of thousands of characters—that's enormous! Sending the entire document to Claude every time we ask a question would create three major problems:

1. **Cost**: We'd be paying for all those characters as input tokens for every single question, even if we're only asking about one small topic
2. **Relevance**: If you ask about "API errors", 95% of the document isn't relevant—it's about other topics like image processing or conversation management
3. **Focus**: Claude performs better with focused, relevant context rather than being overwhelmed with unrelated information

The solution is **document chunking**—breaking the large document into smaller, manageable pieces. Think of it like organizing a library: instead of reading every page of every book to answer a question, you first identify which chapter or section is most relevant.

### Simple Section-Based Chunking

The simplest chunking strategy is to split by section headers. Each section of the lecture becomes its own searchable chunk. This works well for structured documents like lecture notes where each section covers a specific topic.

Let's implement this approach:

```
def chunk_by_sections(text):
    """
    Split a document into chunks based on ## section headers.
    
    This function:
    1. Finds all the ## headers in the text
    2. Splits the document at these headers
    3. Keeps each section as a separate chunk
    4. Preserves the section header with its content
    """
    # Split on section headers
    # We use '\n## ' to ensure we're splitting on headers at line starts
    sections = text.split('\n## ')
    
    chunks = []
    for i, section in enumerate(sections):
        # The first section doesn't have '## ' removed (it wasn't split)
        if i == 0:
            chunk_text = section
        else:
            # Add back the '## ' that was removed during split
            chunk_text = '## ' + section
        
        # Only keep chunks with substantial content (at least 100 characters)
        if len(chunk_text.strip()) > 100:
            chunks.append({
                'text': chunk_text.strip(),
                'length': len(chunk_text),
                'chunk_id': i
            })
    
    return chunks
```

```
# Create chunks from our lecture
lecture_chunks = chunk_by_sections(lecture7_content)

print(f"Created {len(lecture_chunks)} chunks from Lecture 7")
print(f"\nChunk statistics:")
print(f"  Average size: {sum(c['length'] for c in lecture_chunks) // len(lecture_chunks):,} characters")
print(f"  Smallest: {min(c['length'] for c in lecture_chunks):,} characters")
print(f"  Largest: {max(c['length'] for c in lecture_chunks):,} characters")
```

```
Created 12 chunks from Lecture 7

Chunk statistics:
  Average size: 5,275 characters
  Smallest: 323 characters
  Largest: 9,570 characters
```

Let's examine what our chunks look like to understand what we've created:

```
# Examine the first few chunks
print("First 3 chunks from Lecture 7:")
print("=" * 50)

for i in range(min(3, len(lecture_chunks))):
    chunk = lecture_chunks[i]
    # Get the first line (usually the section title)
    first_line = chunk['text'].split('\n')[0]
    
    print(f"\nChunk {i}:")
    print(f"  Title: {first_line}")
    print(f"  Size: {chunk['length']:,} characters")
    print(f"  Preview: {chunk['text'][:150]}...")
```

```
First 3 chunks from Lecture 7:
==================================================

Chunk 0:
  Title: ---
  Size: 323 characters
  Preview: ---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version:...

Chunk 1:
  Title: ## Introduction
  Size: 5,969 characters
  Preview: ## Introduction

For the past six weeks, you've been building a programming foundation. Variables, lists, loops, functions, classes—perhaps they felt ...

Chunk 2:
  Title: ## Understanding APIs
  Size: 3,336 characters
  Preview: ## Understanding APIs

Let's demystify this term that gets thrown around constantly in programming. API stands for Application Programming Interface, ...
```

### Understanding Overlapping Chunks

A potential problem with simple splitting: what if important information spans across chunk boundaries? Imagine reading a textbook where each chapter ends mid-sentence—you'd lose crucial context!

**Overlapping chunks** solve this by having each chunk include some content from its neighbors. It's like having each chapter of a book reprint the last paragraph of the previous chapter and the first paragraph of the next chapter. This ensures nothing important gets lost in the gaps between chunks.

Here's a visual example:

```
Original text: "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
Non-overlapping chunks of size 10:
  Chunk 1: "ABCDEFGHIJ"
  Chunk 2: "KLMNOPQRST"
  Chunk 3: "UVWXYZ"
  
Overlapping chunks (size 10, overlap 3):
  Chunk 1: "ABCDEFGHIJ"
  Chunk 2: "HIJKLMNOPQ"  (starts at H, overlaps HIJ)
  Chunk 3: "OPQRSTUVWX"  (starts at O, overlaps OPQ)
```

While overlapping chunks are more sophisticated and useful for many applications, for our lecture materials that are already well-structured with clear section boundaries, simple section-based chunking works well.

## Understanding Embeddings

Now we have chunks of text, but how do we find which chunks are relevant to a user's question? We can't just search for exact word matches—what if someone asks about "error handling" but the text says "exception management"? These mean the same thing but use different words.

This is where **embeddings** come in. An embedding is a way to convert text into a list of numbers (called a vector) that captures the semantic meaning of that text. The key insight: texts with similar meanings will have similar number patterns, even if they use different words.

Think of it like this:

* "stellar parallax" might become [0.2, -0.1, 0.8, 0.3, ..., 0.5] (384 numbers)
* "star distance measurement" might become [0.3, -0.2, 0.7, 0.4, ..., 0.4] (384 numbers)
* "cooking recipes" might become [0.9, 0.5, -0.3, 0.1, ..., -0.2] (384 numbers)

Notice how the first two (both about measuring star distances) have similar number patterns, while the third (about cooking) is completely different. The embedding model has learned that "parallax" and "distance measurement" are related concepts in astronomy.

### How Embeddings Capture Meaning

Embedding models are neural networks trained on millions of documents. Through this training, they learn:

* "API" and "programming interface" are related concepts
* "error" and "exception" often mean similar things in programming
* "temperature" in the context of LLMs is different from "temperature" in physics

Each dimension in the embedding vector captures some aspect of meaning. While we can't interpret what each individual number means (they're learned by the neural network), we can measure how similar two embeddings are to find related texts.

### Important Note: Normalized Embeddings

Most modern embedding models, including the one we'll use, output **normalized vectors**. This means all embedding vectors have a magnitude (length) of 1.0. This is a crucial property that simplifies our calculations significantly!

### Important Tip: Complete Sentences Give Better Embeddings

When creating embeddings, **complete sentences often work better than keywords!** The embedding model can better understand context and meaning from full sentences. For example:

* "How to measure stellar parallax?" gives richer embeddings than just "parallax"
* "What are the error handling techniques in Python?" is better than "error handling"

This is because the model was trained on natural language text, so it better understands the relationships between words when they appear in complete thoughts.

### Measuring Similarity with Cosine Similarity

Once we have embeddings (vectors of numbers), we need to measure how similar they are. We use **cosine similarity**, which measures the angle between two vectors.

The intuition is simple:

* Vectors pointing in the same direction = similar meaning (cosine similarity ≈ 1)
* Vectors at right angles = unrelated (cosine similarity ≈ 0)
* Vectors pointing opposite ways = opposite meanings (cosine similarity ≈ -1)

The mathematical formula is: cosine(θ) = (A·B) / (||A|| × ||B||)

Where:

* A·B is the dot product (measures alignment)
* ||A|| and ||B|| are the vector magnitudes (lengths)

**However, since embedding models output normalized vectors (||A|| = ||B|| = 1), the formula simplifies to just the dot product: cosine(θ) = A·B**

Let's implement the simplified version:

```
def cosine_similarity(vec1, vec2):
    """
    Calculate cosine similarity for normalized vectors.
    Since ||vec1|| = ||vec2|| = 1, cosine similarity = dot product.
    Much faster and simpler!
    """
    return np.dot(vec1, vec2)
```

### Using the Sentence-Transformers Library

To create actual embeddings that capture semantic meaning, we'll use a library called **sentence-transformers**. This library provides pre-trained neural network models that can convert any text into meaningful embedding vectors.

**What does sentence-transformers do?**

* Provides ready-to-use embedding models trained on millions of documents
* Handles all the complex neural network operations behind the scenes
* Converts text to vectors that actually capture semantic meaning
* Works with sentences, paragraphs, or entire documents

We'll use a model called **'all-MiniLM-L6-v2'** for this tutorial. Breaking down this name helps understand what we're working with: "all" means it works for all types of English text, "MiniLM" indicates it's a smaller, faster version of a language model, "L6" tells us it has 6 layers (the depth of the neural network), and "v2" simply means it's version 2, improved from the original.

**Importantly, this model outputs normalized vectors**, so we can use the simplified cosine similarity calculation.

This model converts any text into 384 numbers that capture its meaning. Through its training, it has learned that phrases like "stellar distance" and "how far away is the star" mean similar things, even though they use different words. We're using this particular model because it strikes the perfect balance for learning—it's small enough to run quickly on any computer (only 80MB download), fast enough for interactive experimentation, and powerful enough to demonstrate all RAG concepts effectively.

**More Powerful Models in Production**

In professional research and production systems, you'll often encounter more sophisticated embedding models. For example, OpenAI's text-embedding-3-large creates 3,072-dimensional embeddings compared to our 384, providing much richer semantic understanding. Google's text-embedding-004 produces 768-dimensional embeddings with excellent multilingual support. Specialized models like Voyage AI's voyage-3 or Cohere's embed-v3 offer 1,024 dimensions optimized for domain-specific or technical texts.

These larger models can capture more subtle semantic relationships and often perform better with specialized scientific literature. However, they come with trade-offs: they're more expensive (often requiring API payments), slower to run, require significantly more memory and storage, and are honestly overkill for learning the fundamental concepts.

Think of it like choosing a telescope: our all-MiniLM-L6-v2 is like a reliable 8-inch telescope that's perfect for learning astronomy. The production models are like research-grade observatories—more powerful, but you don't need them to understand how telescopes work! For your course projects and learning RAG concepts, our smaller model is perfectly adequate. When you eventually move to research-scale projects with thousands of papers, you can upgrade to these more powerful models using the exact same techniques you're learning today.

You can install the sentence-transformers library with the following command:

```
pip install -q sentence-transformers
```

```
from sentence_transformers import SentenceTransformer

# Load a pre-trained embedding model
print("Loading embedding model...")
print("(First time will download ~80MB model file)")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
print("✓ Model loaded successfully!")

# Explore model properties
print(f"\nModel information:")
print(f"  Output dimensions: {embedding_model.get_sentence_embedding_dimension()}")
print(f"  Max input length: {embedding_model.max_seq_length} tokens")
print(f"  (A token is roughly a word or word piece)")
```

```
Loading embedding model...
(First time will download ~80MB model file)
```

```
✓ Model loaded successfully!

Model information:
  Output dimensions: 384
  Max input length: 256 tokens
  (A token is roughly a word or word piece)
```

Let's test the embedding model to see how it captures semantic meaning:

```
# Test with astronomy concepts
test_texts = [
    "stellar parallax measurement",
    "measuring star distances",  # Similar meaning, different words
    "galaxy classification",      # Different astronomy topic
    "cooking recipes"             # Completely unrelated
]

# Generate embeddings
print("Creating embeddings for test phrases...")
test_embeddings = []
for text in test_texts:
    embedding = embedding_model.encode(text)
    test_embeddings.append(embedding)
    print(f"  '{text}': vector with {len(embedding)} dimensions")

# Verify that embeddings are normalized
print("\nChecking if embeddings are normalized:")
for text, embedding in zip(test_texts, test_embeddings):
    norm = np.linalg.norm(embedding)
    print(f"  '{text}': norm = {norm:.4f}")

print("\n✓ All embeddings are normalized! We can use the simplified dot product for similarity.")
```

```
Creating embeddings for test phrases...
  'stellar parallax measurement': vector with 384 dimensions
  'measuring star distances': vector with 384 dimensions
```

```
  'galaxy classification': vector with 384 dimensions
  'cooking recipes': vector with 384 dimensions

Checking if embeddings are normalized:
  'stellar parallax measurement': norm = 1.0000
  'measuring star distances': norm = 1.0000
  'galaxy classification': norm = 1.0000
  'cooking recipes': norm = 1.0000

✓ All embeddings are normalized! We can use the simplified dot product for similarity.
```

```
# Calculate similarities between all pairs
print("\nSemantic similarities between phrases:")
print("=" * 50)

for i in range(len(test_texts)):
    for j in range(i+1, len(test_texts)):
        sim = cosine_similarity(test_embeddings[i], test_embeddings[j])
        print(f"'{test_texts[i]}' vs '{test_texts[j]}'")
        print(f"  Similarity: {sim:.3f}")

print("\nNotice: 'stellar parallax' and 'star distances' have HIGH similarity!")
print("The model understands they're about the same concept.")
```

```
Semantic similarities between phrases:
==================================================
'stellar parallax measurement' vs 'measuring star distances'
  Similarity: 0.622
'stellar parallax measurement' vs 'galaxy classification'
  Similarity: 0.333
'stellar parallax measurement' vs 'cooking recipes'
  Similarity: 0.020
'measuring star distances' vs 'galaxy classification'
  Similarity: 0.310
'measuring star distances' vs 'cooking recipes'
  Similarity: 0.048
'galaxy classification' vs 'cooking recipes'
  Similarity: 0.107

Notice: 'stellar parallax' and 'star distances' have HIGH similarity!
The model understands they're about the same concept.
```

## Building the Complete RAG System

Now let's combine everything we've learned to build a complete RAG system. We'll create embeddings for all our lecture chunks, build a search function that finds relevant content, and use that content to answer questions.

### Step 1: Create Embeddings for All Chunks

First, we need to convert every chunk of our lecture into an embedding vector. This is like creating an index for a book—we're preparing the content to be efficiently searchable. Each chunk gets converted to 384 numbers that capture its meaning:

```
# Generate embeddings for all lecture chunks
print(f"Creating embeddings for {len(lecture_chunks)} chunks...")
print("This may take a minute...\n")

chunk_embeddings = []

for i, chunk in enumerate(lecture_chunks):
    # Create embedding for this chunk's text
    # The encode() method converts text to a vector
    embedding = embedding_model.encode(chunk['text'])
    chunk_embeddings.append(embedding)
    
    # Show progress every 5 chunks
    if (i + 1) % 5 == 0:
        print(f"  Processed {i + 1}/{len(lecture_chunks)} chunks")

print(f"\n✓ Created {len(chunk_embeddings)} embeddings")
print(f"Each embedding has {len(chunk_embeddings[0])} dimensions")
print(f"Total data: {len(chunk_embeddings)} chunks × {len(chunk_embeddings[0])} dimensions = {len(chunk_embeddings) * len(chunk_embeddings[0]):,} numbers")
```

```
Creating embeddings for 12 chunks...
This may take a minute...

  Processed 5/12 chunks
```

```
  Processed 10/12 chunks

✓ Created 12 embeddings
Each embedding has 384 dimensions
Total data: 12 chunks × 384 dimensions = 4,608 numbers
```

### Step 2: Building the Search Function

Now we can build a search function that finds the most relevant chunks for any question. This is the "Retrieval" part of RAG. The process is:

1. Convert the user's question to an embedding
2. Compare it with all chunk embeddings using cosine similarity
3. Return the chunks with the highest similarity scores

This is like having a librarian who understands meaning, not just keywords. If you ask about "error handling", it will find sections about "exceptions" and "try-except blocks" even if they don't use the exact phrase "error handling".

We'll use a vectorized approach for efficiency:

```
def search_chunks(query, top_k=3):
    """
    Find the most relevant chunks for a query using vectorized operations.
    
    This function:
    1. Converts the query to an embedding (384 numbers)
    2. Calculates similarity with all chunk embeddings using vectorized NumPy
    3. Returns the top-k most similar chunks
    
    Parameters:
    - query: The search question
    - top_k: How many results to return
    """
    # Convert query to embedding (same 384-dimensional space as chunks)
    query_embedding = embedding_model.encode(query)
    
    # Vectorized similarity calculation - much faster than a loop!
    # Convert list of embeddings to NumPy array for vectorized operations
    chunk_matrix = np.array(chunk_embeddings)
    
    # Calculate dot products with all chunks at once
    similarities = np.dot(chunk_matrix, query_embedding)
    
    # Find the indices of top-k highest similarities
    # argsort() returns indices that would sort the array
    # [-top_k:] takes the last k elements (highest values)
    # [::-1] reverses to get descending order
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    
    # Return the top chunks with their similarities
    results = []
    for idx in top_indices:
        results.append({
            'chunk': lecture_chunks[idx],
            'similarity': similarities[idx]
        })
    
    return results
```

### Step 3: Testing the Search

Let's test our search function with a specific question about API security from Lecture 7. This will show us which sections of the lecture are most relevant to our query:

```
# Test search with a specific question
query = "How do I keep API keys secure?"
results = search_chunks(query, top_k=2)

print(f"Query: '{query}'")
print("\n" + "=" * 50)
print(f"Found {len(results)} relevant sections:")
print("=" * 50)

for i, result in enumerate(results, 1):
    # Extract section title (first line)
    lines = result['chunk']['text'].split('\n')
    title = lines[0] if lines else "No title"
    
    print(f"\nResult {i}:")
    print(f"  Similarity score: {result['similarity']:.3f}")
    print(f"  (1.0 = perfect match, 0.0 = unrelated)")
    print(f"  Section: {title}")
    print(f"  Preview: {result['chunk']['text'][:200]}...")
```

```
Query: 'How do I keep API keys secure?'

==================================================
Found 2 relevant sections:
==================================================

Result 1:
  Similarity score: 0.405
  (1.0 = perfect match, 0.0 = unrelated)
  Section: ## Summary
  Preview: ## Summary

### Key Concepts
In this lecture, you've learned:
- **API Fundamentals**: How to communicate with Large Language Models programmatically through structured requests and responses, transfor...

Result 2:
  Similarity score: 0.350
  (1.0 = perfect match, 0.0 = unrelated)
  Section: ## Understanding APIs
  Preview: ## Understanding APIs

Let's demystify this term that gets thrown around constantly in programming. API stands for Application Programming Interface, but that definition helps nobody. Here's a better ...
```

### Step 4: RAG-Powered Question Answering

Now for the complete RAG workflow. We'll create a function that combines everything:

1. **Retrieval**: Search for relevant chunks from our lecture materials using semantic similarity
2. **Augmentation**: Add the retrieved content to our prompt as context for the AI
3. **Generation**: Use Claude to generate an answer based on the retrieved information

The `rag_answer()` function below implements this complete pipeline:

* **Input**: Takes a question and optionally the number of chunks to retrieve
* **Retrieval Step**: Uses our `search_chunks()` function to find the most relevant sections
* **Quality Check**: Filters out results with low similarity scores (< 0.2) to avoid irrelevant content
* **Smart Augmentation**: Combines retrieved chunks but ensures we end at complete sentences (no cut-off mid-sentence)
* **Prompt Engineering**: Creates a structured prompt that includes both the question and retrieved course materials
* **Generation**: Sends the augmented prompt to Claude with low temperature (0.0) for factual accuracy
* **Output**: Returns an answer grounded in our actual course materials

This approach ensures the AI answers questions using specific information from our course materials, rather than just relying on its general training data.

```
def rag_answer(question, max_chunks=2):
    """
    Answer a question using RAG (Retrieval Augmented Generation).
    
    Improved version that doesn't cut off mid-sentence!
    
    The three RAG steps:
    1. RETRIEVAL: Find relevant chunks from course materials
    2. AUGMENTATION: Add those chunks to the prompt
    3. GENERATION: Get Claude to answer using the retrieved content
    """
    print(f"Searching for content related to: '{question}'")
    
    # Step 1: Retrieve relevant chunks
    results = search_chunks(question, top_k=max_chunks)
    
    # Check if we found relevant content
    if results[0]['similarity'] < 0.2:
        return "No relevant content found in course materials for this question."
    
    print(f"Found {len(results)} relevant sections (similarity > 0.2)")
    
    # Step 2: Augment - combine retrieved chunks 
    context_parts = []
    for i, result in enumerate(results, 1):
        # Take more content but end at a complete sentence
        chunk_text = result['chunk']['text'][:1500]  # Take up to 1500 chars
        
        # Find the last period, question mark, or exclamation point
        # to end at a complete sentence
        last_sentence_end = max(
            chunk_text.rfind('.'),
            chunk_text.rfind('?'),
            chunk_text.rfind('!')
        )
        
        if last_sentence_end > 0:
            chunk_text = chunk_text[:last_sentence_end + 1]
        
        context_parts.append(f"Section {i}:\n{chunk_text}")
    
    context = "\n\n---\n\n".join(context_parts)
    
    # Create augmented prompt with retrieved content
    augmented_prompt = f"""Based on the following course materials from Lecture 7, answer this question: {question}

COURSE MATERIALS:
{context}

Please provide a comprehensive answer based specifically on what the course materials say. Use the exact terminology and examples from the lecture."""
    
    # Step 3: Generate answer with Claude
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=400,
        temperature=0.0,  # Low temperature for factual accuracy
        messages=[{"role": "user", "content": augmented_prompt}]
    )
    
    return response.content[0].text
```

```
# Test RAG answering with a question about course content
test_question = "What are the main parameters for API calls we learned about?"

print("=" * 70)
print("RAG-POWERED ANSWER")
print("=" * 70)
answer = rag_answer(test_question)
print(f"\nAnswer based on Lecture 7 content:")
print(answer)
print("=" * 70)
```

```
======================================================================
RAG-POWERED ANSWER
======================================================================
Searching for content related to: 'What are the main parameters for API calls we learned about?'
Found 2 relevant sections (similarity > 0.2)
```

```
Answer based on Lecture 7 content:
Based on the course materials provided, I can see that the lecture covers API fundamentals and mentions that API requests contain parameters, but the specific main parameters for API calls are not fully detailed in the sections you've shared.

From what is included in the course materials, I can identify these parameters that were mentioned:

1. **The prompt/text content** - The text you want the LLM to analyze or process
2. **Model selection** - Which specific model to use for the request
3. **Response length** - How long the response should be

The materials explain that when you want an LLM to analyze text, "you send a specially formatted message over the internet to the LLM's servers. The message contains your prompt, along with parameters like which model to use and how long the response should be."

However, the course materials you've provided appear to be incomplete, as Section 2 (Summary) cuts off mid-sentence when discussing "Best practices for managing API keys using environment files and ." This suggests there may be additional content about API parameters that wasn't included in what you shared.

To provide a more comprehensive answer about the main parameters for API calls that were covered in Lecture 7, I would need access to the complete course materials, particularly any sections that might detail the specific parameter options and their usage.
======================================================================
```

### Comparing RAG vs Non-RAG Responses

Let's see the dramatic difference between Claude's general knowledge and answers grounded in your specific course materials. This demonstrates why RAG is so powerful for working with your own documents:

```
comparison_question = "What did we learn about conversation histories in the API?"

# Without RAG - just Claude's general knowledge
print("WITHOUT Course Materials (General Knowledge):")
print("=" * 50)
general_response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=200,
    messages=[{"role": "user", "content": comparison_question}]
)
print(general_response.content[0].text)

print("\n" + "=" * 70 + "\n")

# With RAG - using course materials
print("WITH Course Materials (RAG-Enhanced):")
print("=" * 50)
rag_answer_text = rag_answer(comparison_question)
print(rag_answer_text)

print("\n" + "=" * 70)
print("\nNotice: The RAG answer references specific details from YOUR lecture!")
print("It mentions the exact concepts and examples we covered in class.")
```

```
WITHOUT Course Materials (General Knowledge):
==================================================
```

```
I don't have the specific context of which API you're referring to, so I can't give you details about what was covered in a particular lesson or documentation you may have read.

However, I can share some general insights about conversation histories in AI/chat APIs:

**Common patterns include:**
- **Stateless nature**: Most APIs don't maintain conversation history automatically
- **Manual history management**: You typically need to send the full conversation context with each request
- **Message arrays**: Conversations are often structured as arrays of messages with roles (user, assistant, system)
- **Token limits**: Longer histories consume more tokens and may hit API limits
- **Cost implications**: Longer conversation histories increase API costs since you're sending more data

**Typical structure:**
```json
{
  "messages": [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "

======================================================================

WITH Course Materials (RAG-Enhanced):
==================================================
Searching for content related to: 'What did we learn about conversation histories in the API?'
Found 2 relevant sections (similarity > 0.2)
```

```
Based on the course materials from Lecture 7, here's what we learned about conversation histories in the API:

## Key Learning: The API is Stateless

The most important concept about conversation histories in the API is that **the API is completely stateless**—each API call is independent and has no memory of previous calls. This is fundamentally different from chat interfaces where Claude appears to "remember" your conversation.

## Critical Difference from Chat Interfaces

Unlike the chat interface where Claude seems to "remember" your conversation, when using the API, Claude has no built-in memory between separate API calls. Each request starts with a completely blank slate.

## Maintaining Context Requires Explicit Action

To maintain context across multiple API calls, **you must explicitly provide the entire conversation history with each request**. The API doesn't automatically remember or store previous interactions.

## Practical Demonstration

The course materials provided a clear example showing this concept:

**Call 1:**
- User: "My favorite galaxy is M31. Remember this."
- Claude responds normally

**Call 2 (separate API call):**
- User: "What is my favorite galaxy?"
- Claude has no idea what the user is referring to

As the materials emphasize: "Notice: Claude has no idea! Each API call is completely independent."

## Bottom Line

The key takeaway is that conversation histories don't exist automatically in the API—they must be manually constructed and maintained by including the full conversation context in each API request if you want Claude to have memory of previous exchanges.

======================================================================

Notice: The RAG answer references specific details from YOUR lecture!
It mentions the exact concepts and examples we covered in class.
```

## Combining Function Tools with RAG

Now for the grand finale—let's combine our calculation functions with document search to create a complete AI assistant. This assistant can both compute astronomical values and search your course materials, choosing the right tool for each question.

This combination is powerful: imagine asking "What's the distance to a star with 0.1 arcsec parallax, and what did we learn about parallax in the course?" The assistant can calculate the distance AND find relevant course content.

### Creating a Search Function for Claude

First, let's wrap our RAG search in a function that Claude can call as a tool. This version properly handles complete sentences:

```
def search_course_materials(question, max_results=2):
    """
    Search course materials and return relevant content.
    This function will be callable by Claude as a tool.
    """
    # Search for relevant chunks
    results = search_chunks(question, top_k=max_results)
    
    # Check if we found anything relevant
    if results[0]['similarity'] < 0.2:
        return {
            "status": "no_relevant_content",
            "message": "No relevant course material found for this question"
        }
    
    # Format results for Claude
    content_parts = []
    for i, result in enumerate(results, 1):
        # Get section title
        lines = result['chunk']['text'].split('\n')
        title = lines[0] if lines else "No title"
        
        # Get content ending at complete sentence
        content_text = result['chunk']['text'][:1000]
        last_period = content_text.rfind('.')
        if last_period > 0:
            content_text = content_text[:last_period + 1]
        
        content_parts.append(f"Section {i} - {title}:\n{content_text}")
    
    # Return structured results
    return {
        "status": "found",
        "best_similarity": round(results[0]['similarity'], 3),
        "content": "\n\n".join(content_parts)
    }
```

### Complete Tool Set with Calculations and Search

Now let's create our complete tool set that combines astronomical calculations with course material search:

```
# Complete tools list combining calculations and search
complete_tools = [
    {
        "name": "parallax_to_distance",
        "description": "Calculate stellar distance from parallax measurement",
        "input_schema": {
            "type": "object",
            "properties": {
                "parallax_arcsec": {
                    "type": "number",
                    "description": "Parallax in arcseconds"
                }
            },
            "required": ["parallax_arcsec"]
        }
    },
    {
        "name": "stellar_luminosity",
        "description": "Calculate stellar luminosity from radius and temperature",
        "input_schema": {
            "type": "object",
            "properties": {
                "radius_solar": {
                    "type": "number",
                    "description": "Radius in solar radii"
                },
                "temperature_k": {
                    "type": "number",
                    "description": "Temperature in Kelvin"
                }
            },
            "required": ["radius_solar", "temperature_k"]
        }
    },
    {
        "name": "search_course_materials",
        "description": "Search Lecture 7 notes for relevant course content",
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "Topic or question to search for"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results (default 2)",
                    "default": 2
                }
            },
            "required": ["question"]
        }
    }
]

print(f"Complete AI Assistant with {len(complete_tools)} capabilities:")
for tool in complete_tools:
    print(f"  • {tool['name']}: {tool['description']}")
```

```
Complete AI Assistant with 3 capabilities:
  • parallax_to_distance: Calculate stellar distance from parallax measurement
  • stellar_luminosity: Calculate stellar luminosity from radius and temperature
  • search_course_materials: Search Lecture 7 notes for relevant course content
```

### Complete Assistant Function with Natural Language Responses

Let's create a complete assistant function that handles the entire workflow, ensuring we always get natural language answers whether Claude uses calculations or searches:

```
def complete_assistant(question):
    """
    Complete AI assistant that can calculate and search.
    Always returns a natural language answer.
    """
    print(f"Processing: {question}")

    # Get Claude's initial response
    initial_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        tools=complete_tools,
        messages=[{"role": "user", "content": question}]
    )

    # Check if Claude needs a tool
    if initial_response.stop_reason != "tool_use":
        # Some SDKs return plain dicts when running offline; fall back to repr
        # repr() returns a string representation of the object for debugging
        text_blocks = [
            getattr(block, "text", None)
            if not isinstance(block, dict)
            else block.get("text")
            for block in getattr(initial_response, "content", [])
        ]
        text_blocks = [item for item in text_blocks if item]
        return "".join(text_blocks).strip() or repr(initial_response)

    # Execute the requested tool
    tool_use = initial_response.content[-1]
    print(f"  → Using tool: {tool_use.name}")

    # Execute the appropriate function
    if tool_use.name == "parallax_to_distance":
        result = parallax_to_distance(tool_use.input['parallax_arcsec'])
    elif tool_use.name == "stellar_luminosity":
        result = stellar_luminosity(
            tool_use.input['radius_solar'],
            tool_use.input['temperature_k']
        )
    elif tool_use.name == "search_course_materials":
        result = search_course_materials(
            tool_use.input['question'],
            tool_use.input.get('max_results', 2)
        )
    else:
        result = {"error": f"Unknown function: {tool_use.name}"}

    # Get natural language response
    final_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=400,
        tools=complete_tools,
        messages=[
            {"role": "user", "content": question},
            {"role": "assistant", "content": initial_response.content},
            {
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": str(result)
                }]
            }
        ]
    )

    text_blocks = [
        getattr(block, "text", None)
        if not isinstance(block, dict)
        else block.get("text")
        for block in getattr(final_response, "content", [])
    ]
    text_blocks = [item for item in text_blocks if item]
    if text_blocks:
        return "".join(text_blocks).strip()

    # As a fallback, provide the raw response so readers know to run locally
    return repr(final_response)
```

### Testing the Complete System

Let's test our complete AI assistant with different types of questions—calculations, course content searches, and general questions. Notice how Claude automatically chooses the right tool and provides natural language answers:

```
# Test different types of questions
test_scenarios = [
    "What's the distance to a star with 0.1 arcsecond parallax?",
    "What did we learn about conversation histories in the API?",
    "Calculate the luminosity of a star with radius 3 solar radii and temperature 7000K"
]

for i, question in enumerate(test_scenarios, 1):
    print(f"\nTest {i}:")
    print("=" * 60)
    answer = complete_assistant(question)
    print(f"\nAnswer: {answer}")
    print("=" * 60)
```

```
Test 1:
============================================================
Processing: What's the distance to a star with 0.1 arcsecond parallax?
```

```
  → Using tool: parallax_to_distance
```

```
Answer: The distance to a star with a parallax of 0.1 arcseconds is **10 parsecs**.

This follows the parallax-distance relationship where distance (in parsecs) = 1 / parallax (in arcseconds). So with a parallax of 0.1 arcseconds, the distance is 1/0.1 = 10 parsecs.

To put this in perspective:
- 10 parsecs = approximately 32.6 light-years
- This is a relatively nearby star in our local stellar neighborhood
============================================================

Test 2:
============================================================
Processing: What did we learn about conversation histories in the API?
```

```
  → Using tool: search_course_materials
```

```
Answer: Message(id='msg_019ucpMesbGmBWn4rwbNjFp8', content=[ToolUseBlock(id='toolu_01C1CMQQ1ynLnXuQe6hsoeyw', input={'question': 'conversation history context API calls'}, name='search_course_materials', type='tool_use')], model='claude-sonnet-4-20250514', role='assistant', stop_reason='tool_use', stop_sequence=None, type='message', usage=Usage(cache_creation=CacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0), cache_creation_input_tokens=0, cache_read_input_tokens=0, input_tokens=1065, output_tokens=59, server_tool_use=None, service_tier='standard'))
============================================================

Test 3:
============================================================
Processing: Calculate the luminosity of a star with radius 3 solar radii and temperature 7000K
```

```
  → Using tool: stellar_luminosity
```

```
Answer: The star with a radius of 3 solar radii and temperature of 7000K has:

- **Luminosity: 19.5 solar luminosities** (L☉)
- **Luminosity: 7.46 × 10²⁷ watts**

This means the star is about 19.5 times more luminous than our Sun. The higher luminosity comes from both the larger radius (3 times the Sun's radius) and the higher temperature (7000K compared to the Sun's ~5778K), with luminosity scaling as R² × T⁴ according to the Stefan-Boltzmann law.
============================================================
```

## Vector Databases - The Professional Solution

What we've built today is a fully functional RAG system that works well for single documents or small collections. However, when you're dealing with thousands of documents or millions of chunks in professional research, you need more sophisticated tools called **vector databases**.

Vector databases are specialized systems designed to store and search embeddings efficiently. They're like regular databases, but optimized for finding similar vectors quickly, even when you have billions of them.

### Three Popular Vector Database Solutions

Here are three of the most popular vector database solutions you're likely to encounter:

**1. Chroma** - Perfect for getting started
Chroma is an open-source, completely free vector database that works seamlessly with Python. It can run entirely in memory for small projects, making it ideal for prototyping and learning. The API feels natural after today's lecture—you'll find the transition straightforward.

**2. Pinecone** - The managed cloud solution
Pinecone offers a fully managed cloud service where you don't need to maintain any servers. It handles scaling automatically as your data grows, making it more expensive but very reliable and fast. Many production AI applications use Pinecone when they need enterprise-level reliability without the hassle of infrastructure management.

**3. FAISS** - Facebook's high-performance library
Developed by Facebook AI Research, FAISS is extremely fast, especially with GPU acceleration. It's more of a library than a full database, but when speed is absolutely critical and you need to handle billions of vectors efficiently, FAISS is often the go-to choice.

### When to Use Vector Databases

Our implementation today works great for single documents or small collections (under 100 documents), prototyping and learning RAG concepts, and understanding how semantic search works under the hood.

You should consider upgrading to a vector database when you're working with thousands of documents or research papers, need persistent storage with embeddings saved to disk, have multiple users searching simultaneously, want advanced features like filtering and metadata search, or are building production applications for research teams.

### Working Example: ChromaDB

Let's see how easy it is to upgrade our system to use ChromaDB. ChromaDB is a vector database that handles storage and search for us, though there are a few important differences from our manual implementation:

**Key Differences to Note:**

1. **ChromaDB uses its own default embedding model** (not our `all-MiniLM-L6-v2`) unless you explicitly override it
2. **ChromaDB returns distances, not similarities** - lower values mean more similar

Here's the implementation:

First, install ChromaDB:

```
pip install -q chromadb
```

Then, import ChromaDB:

```
import chromadb

# Read the same Lecture 7 file
with open('Lecture7_LLM_API_Basics_20250924.md', 'r') as f:
    lecture7_content = f.read()

# Use our same chunking function
lecture_chunks = chunk_by_sections(lecture7_content)

# Create ChromaDB client and clean up any existing collection
chroma_client = chromadb.Client()

# Delete the collection if it already exists
try:
    chroma_client.delete_collection(name="lecture7_rag")
    print("Deleted existing collection")
except:
    print("No existing collection to delete")

# Create new collection
collection = chroma_client.create_collection(
    name="lecture7_rag",
    metadata={"description": "Lecture 7 content for RAG"}
)

# Add all chunks to ChromaDB (it handles embeddings automatically!)
for i, chunk in enumerate(lecture_chunks):
    collection.add(
        documents=[chunk['text']],
        ids=[f"chunk_{i}"],
        metadatas=[{"chunk_id": i, "length": chunk['length']}]
    )

print(f"Added {len(lecture_chunks)} chunks to ChromaDB")

# Now search is incredibly simple
results = collection.query(
    query_texts=["How do I keep API keys secure?"],
    n_results=2
)

# Display results
for i, (doc, distance) in enumerate(zip(results['documents'][0], results['distances'][0])):
    print(f"\nResult {i+1} (distance: {distance:.3f}):")
    print(doc[:200] + "...")
```

```
No existing collection to delete
```

```
Added 12 chunks to ChromaDB

Result 1 (distance: 1.189):
## Summary

### Key Concepts
In this lecture, you've learned:
- **API Fundamentals**: How to communicate with Large Language Models programmatically through structured requests and responses, transfor...

Result 2 (distance: 1.300):
## Understanding APIs

Let's demystify this term that gets thrown around constantly in programming. API stands for Application Programming Interface, but that definition helps nobody. Here's a better ...
```

That's it! Notice how ChromaDB:

* Automatically creates embeddings using the same model
* Stores everything persistently (survives restarts)
* Handles all the vector similarity calculations
* Returns results ranked by relevance
* Can store metadata alongside each chunk

The concepts are identical to what we built—ChromaDB just handles the infrastructure for us. You could now search through hundreds of lecture files without changing the code!

What matters isn't the specific vector database you use, but understanding the concepts we've covered today. Documents get chunked into manageable pieces, chunks get converted to embeddings, queries get converted to embeddings, similarity search finds relevant chunks, and retrieved content augments LLM prompts. With this understanding, you can use any vector database—they're all just different implementations of the same core ideas you've mastered today!

## Summary

### Key Concepts

In this lecture, you've learned:

* **Function Tools**: How to transform Python functions into tools that LLMs can call automatically, creating a bridge between natural language requests and computational execution
* **Function Schemas**: The structured format for describing functions to LLMs, enabling them to understand when and how to use your calculations
* **Document Processing and Chunking**: Strategies for breaking large documents into searchable pieces while preserving context and meaning
* **Embeddings and Semantic Search**: How text gets converted to numerical vectors that capture meaning, enabling similarity-based retrieval even when exact words don't match
* **RAG Implementation**: The complete retrieval-augmented generation pipeline that grounds LLM responses in your specific documents rather than general knowledge
* **Tool Integration**: Combining computational functions with document search to create an AI assistant that can both calculate and retrieve information
* **Vector Databases**: Professional solutions for scaling RAG systems to thousands of documents while maintaining fast search performance

### What You Can Now Do

After working through this material, you should be able to:

* Convert any Python function into an LLM-callable tool with proper schemas and error handling
* Build RAG systems that search through your course materials or research papers to provide grounded, accurate answers
* Create AI assistants that seamlessly combine calculations with document retrieval based on user questions
* Process and chunk documents effectively, balancing context preservation with search efficiency
* Implement semantic search using embeddings and cosine similarity for meaning-based retrieval
* Understand when to upgrade from custom implementations to professional vector databases
* Debug and optimize the complete workflow from function definition to natural language response

### Practice Suggestions

To solidify these concepts:

1. Create additional astronomical calculation functions (orbital mechanics, redshift calculations) and add them to your tool set
2. Convert all your lecture notebooks to markdown and build a searchable knowledge base for the entire course
3. Experiment with different chunking strategies (overlapping chunks, smaller/larger sizes) to see how they affect search quality
4. Try different embedding models and compare their performance on astronomical terminology
5. Build a specialized assistant for your research project that combines domain-specific calculations with literature search

### Looking Ahead

Next week in Lecture 9, we'll explore GitHub and professional coding development. The systems you've built today—function tools and RAG implementations—are exactly the kind of projects you'll want to showcase in your GitHub portfolio. You'll learn how to version control your AI assistants, collaborate with others on these tools, and deploy them for others to use. The combination of today's AI capabilities with next week's professional development practices will prepare you to build and share powerful research tools that can accelerate astronomical discovery.
