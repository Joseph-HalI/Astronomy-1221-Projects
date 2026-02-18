# Variables and Collections

## Introduction

In astronomy, we deal with diverse data types: brightness measurements from millions of stars, time series of variable objects, spectra with thousands of wavelength points, and catalogs with complex metadata. Python provides the foundation for handling all of this efficiently.

This tutorial covers essential Python concepts you'll use throughout your astronomical career. We'll focus on the basic building blocks: storing data, working with numbers, organizing information, and understanding how Python manages memory. By the end of this lecture, you'll understand the fundamental data types and operations that form the foundation of all astronomical computing.

## Your First Variables

### Creating Variables

Variables are like labeled containers for storing data. Think of them as boxes with names written on them. The `=` sign means "store this value" - it's not about mathematical equality, but about assignment:

```
star_name = "Sirius"
magnitude = -1.46
distance_parsecs = 2.64
```

Each line creates a container (variable) and puts a value inside it. The variable name goes on the left, the value on the right. Once stored, we can use these values by referring to their names.

### How Python Knows the Type

Python automatically determines what type of data you're storing. You don't need to tell Python "this is a number" or "this is text" - it figures it out from the value itself:

```
star_count = 1000        # Integer (whole number)
temperature = 5778.5     # Float (decimal number)  
star_name = "Betelgeuse" # String (text)
```

This automatic type detection makes Python very convenient for scientific computing. No need to declare types in advance - Python is smart enough to understand what you're giving it.

### Variable Names in Astronomy

Choosing good variable names is crucial in scientific computing. Your code should tell a story that other astronomers (including future you) can understand. Here's how to choose good names:

```
# Good astronomical variable names - self-explanatory
right_ascension = 150.5  # degrees - celestial longitude
declination = -30.2      # degrees - celestial latitude
apparent_magnitude = 15.3  # brightness as seen from Earth
absolute_magnitude = -21.5  # intrinsic brightness
redshift = 0.05  # measure of distance for galaxies
```

Compare this to unclear names that require you to remember what they mean:

```
# Bad - unclear what these represent
r = 150.5
d = -30.2
m = 15.3
```

The descriptive names immediately tell you what each number represents. When you're analyzing data from thousands of stars, this clarity becomes essential.

Some naming guidelines for astronomy:

* Use full words rather than abbreviations: `parallax` not `plx`
* Include units in comments: `distance_parsecs = 50.2 # parsecs`
* Be specific: `v_band_magnitude` not just `magnitude`
* Use underscores to separate words: `proper_motion_ra` not `propermotionra`

### Constants and Naming Conventions

Constants are values that never change during your program. In astronomy, these are often physical constants or survey parameters. The Python convention is to use ALL\_CAPITAL\_LETTERS for constants:

```
# Physical constants used in astronomy
SPEED_OF_LIGHT = 299792458    # m/s
SOLAR_MASS = 1.989e30         # kg
PARSEC_TO_METERS = 3.086e16   # meters per parsec
HUBBLE_CONSTANT = 70.0        # km/s/Mpc
```

By using capital letters, you immediately know these values shouldn't change. This helps prevent bugs where you accidentally modify an important constant.

## Working with Numbers

### Basic Operations and Power

Python handles mathematical operations with familiar symbols, plus one special operator for exponentiation:

```
distance = 50.0 * 3.26  # Parsecs to light-years
flux = 10 ** (-0.4 * magnitude)  # The ** means exponentiation
```

The double asterisk `**` is Python's way of writing powers. So `10**2` equals 100, and `2**3` equals 8. This is essential for astronomical calculations where we often work with powers of 10.

### Operator Precedence and Parentheses

Python follows standard mathematical order of operations, but in complex astronomical formulas, always use parentheses to make your intent clear:

```
magnitude = 15.0
extinction = 0.3  # Light absorption by interstellar dust
distance_modulus = 5.0  # Related to distance

# Without parentheses - follows standard order
result1 = magnitude - extinction + distance_modulus
print(f"Without parentheses: {result1}")  # 19.7

# With parentheses to change order
result2 = magnitude - (extinction + distance_modulus)
print(f"With parentheses: {result2}")  # 9.7

# Complex formula with clear parentheses
flux = 10**(-0.4 * (magnitude - extinction))
```

```
Without parentheses: 19.7
With parentheses: 9.7
```

Parentheses make your calculations explicit and prevent order-of-operations errors.

### Import math for Advanced Functions

Basic Python can add, subtract, multiply, and divide. For more advanced math, we need to import the `math` module - think of it as opening a more sophisticated calculator:

```
import math
print(f"Square root of 16: {math.sqrt(16)}")          # 4.0
print(f"Log base 10 of 100: {math.log10(100)}")      # 2.0 (useful for magnitude calculations)
print(f"45 degrees in radians: {math.radians(45)}")  # Convert degrees to radians
```

```
Square root of 16: 4.0
Log base 10 of 100: 2.0
45 degrees in radians: 0.7853981633974483
```

The word `import` loads a toolbox of pre-written functions. The `math.` prefix tells Python to use a function from that toolbox. Python keeps basic operations simple and lets you add complexity only when needed.

### Mathematical Functions

The `math` module provides functions for common astronomical calculations. Let's explore the most useful ones:

```
distance = 50.0
angle_deg = 45.0

# Square roots - essential for distance calculations and error propagation
print(f"Square root: {math.sqrt(distance)}")

# Logarithms - crucial for magnitude calculations
print(f"Natural log: {math.log(distance)}")
print(f"Log base 10: {math.log10(distance)}")

# Other useful functions
print(f"Absolute value: {abs(-25.7)}")

# Rounding for output
print(f"Rounded: {round(15.3456, 2)}")  # 2 decimal places

# Trigonometry - angles must be in radians
angle_rad = math.radians(angle_deg)
print(f"Sine: {math.sin(angle_rad):.3f}")
print(f"Cosine: {math.cos(angle_rad):.3f}")
```

```
Square root: 7.0710678118654755
Natural log: 3.912023005428146
Log base 10: 1.6989700043360187
Absolute value: 25.7
Rounded: 15.35
Sine: 0.707
Cosine: 0.707
```

The `math.radians()` function converts degrees to radians, essential since Python's trig functions expect radians.

## Importing Modules

### Modules are Toolboxes

Modules are collections of pre-written code that add functionality to Python. Think of them as specialized toolboxes - you wouldn't carry every tool you own everywhere, just the ones you need for the job:

```
import math    # Mathematical functions
import sys     # System functions
```

Once imported, you access functions using dot notation:

```
print(f"Square root of 16: {math.sqrt(16)}")  # Use sqrt from the math module
print(f"Pi constant: {math.pi}")              # Constants are available too!
```

```
Square root of 16: 4.0
Pi constant: 3.141592653589793
```

Python starts minimal - you add capabilities as needed by importing modules. This keeps programs efficient and clear about what tools they're using.

## Special Values: None, NaN, inf

### Real Data Has Missing Values

Perfect data doesn't exist in astronomy. Detectors fail, weather interrupts observations, and some measurements are simply impossible. Python provides special values to handle these realities:

```
redshift = None           # Not measured yet
bad_mag = float('nan')    # Failed measurement (Not a Number)
saturated = float('inf')  # Detector overflow (infinity)
negative_inf = float('-inf')  # Negative infinity
```

Display these values to see how they look:

```
print(f"Good: {15.3}")
print(f"Missing: {bad_mag}")
print(f"Saturated: {saturated}")
```

```
Good: 15.3
Missing: nan
Saturated: inf
```

### Testing for Special Values

You can't test for NaN using `==` because NaN is defined to not equal anything, even itself! Use special functions instead:

```
good_magnitude = 15.3
missing_magnitude = float('nan')
saturated = float('inf')

print(f"Is good_magnitude NaN? {math.isnan(good_magnitude)}")  # False
print(f"Is missing_magnitude NaN? {math.isnan(missing_magnitude)}")  # True
print(f"Is saturated infinite? {math.isinf(saturated)}")  # True
```

```
Is good_magnitude NaN? False
Is missing_magnitude NaN? True
Is saturated infinite? True
```

These special values help track data quality issues throughout your analysis pipeline.

### Working with None

`None` is Python's way of representing "nothing" or "missing data". It's different from NaN because None can represent any type of missing information:

```
# Some measurements might not exist
redshift = None
proper_motion = None  # Star's motion across the sky
parallax = 5.2  # This one was measured

print(f"Redshift: {redshift}")
print(f"Proper motion: {proper_motion}")
print(f"Parallax: {parallax}")

# Check for None using 'is'
print(f"Redshift is None: {redshift is None}")  # True
print(f"Parallax is None: {parallax is None}")  # False
```

```
Redshift: None
Proper motion: None
Parallax: 5.2
Redshift is None: True
Parallax is None: False
```

Use `is None` rather than `== None` - it's more reliable and considered better Python style.

## Strings: Text Data

### Storing Text

Strings are sequences of characters enclosed in quotes. They're perfect for storing names, IDs, and any text information:

```
star_name = "Alpha Centauri"
catalog_id = "HD 128620"
notes = "Closest star system"
```

Strings are fundamental because much of our astronomical metadata is text: object names, filter bands, telescope configurations, and observation notes.

### String Properties

Check string length and type:

```
star_name = "Alpha Centauri"
print(f"Length: {len(star_name)} characters")  # 14 characters
print(f"Type: {type(star_name)}")  # <class 'str'>
```

```
Length: 14 characters
Type: <class 'str'>
```

The `len()` function tells us how many characters are in the string. This is our first encounter with `len()` - it works on any collection of items.

### Common String Mistake

Here's a critical distinction that trips up many beginners. These look similar but are completely different:

```
magnitude_num = 15.3   # This is a number
magnitude_str = "15.3" # This is text!

# You can do math with the number:
print(f"Number addition: {magnitude_num + 5}")  # Works: gives 20.3

# But not with the string:
# magnitude_str + 5    # Error! Can't add text and number

# String multiplication repeats the string!
distance = "50"
result = distance * 3  # "505050" NOT 150!
print(f"String repetition: {result}")
```

```
Number addition: 20.3
String repetition: 505050
```

The quotes make all the difference. With quotes, Python sees text. Without quotes, Python sees a number.

## Type Checking and Conversion

### Finding Out the Type

When unsure about data types, ask Python directly using `type()`:

```
print(f"15.3 is type: {type(15.3)}")     # <class 'float'>
print(f'"15.3" is type: {type("15.3")}')   # <class 'str'>
print(f"15 is type: {type(15)}")       # <class 'int'>
```

```
15.3 is type: <class 'float'>
"15.3" is type: <class 'str'>
15 is type: <class 'int'>
```

This is especially useful when debugging - many errors come from unexpected data types.

### Converting Between Types

Data often arrives in the wrong format, especially when reading from files. Python provides conversion functions:

```
# String to number
magnitude_str = "15.3"
magnitude_num = float(magnitude_str)  # Now it's 15.3 as a number
print(f"String to float: {magnitude_num}")

# Number to string
result = 15.3
result_str = str(result)  # Now it's "15.3" as text
print(f"Number to string: {result_str}")

# String to integer
count_str = "1000"
count_int = int(count_str)  # Now it's 1000 as an integer
print(f"String to integer: {count_int}")

# Integer conversion truncates decimals
print(f"Float to int (truncates!): {int(15.9)}")  # 15 - decimal part removed!
```

```
String to float: 15.3
Number to string: 15.3
String to integer: 1000
Float to int (truncates!): 15
```

Data read from files usually comes as strings, so conversion is essential before calculations.

## The Print Function

### Displaying Results

The `print()` function is your window into what Python is doing. It displays values on screen:

```
star_name = "Sirius"
print(star_name)  # Shows: Sirius

magnitude = -1.46
print(star_name, magnitude)  # Shows: Sirius -1.46
```

```
Sirius
Sirius -1.46
```

Using commas in print automatically adds spaces between items. But for complex output, we need something better...

## F-strings: Formatted Output

### Building Readable Output

F-strings let you embed variables directly in text. Put an `f` before the quotes and wrap variables in curly braces:

```
star_name = "Betelgeuse"
magnitude = 0.42

print(f"The star {star_name} has magnitude {magnitude}")
# Output: The star Betelgeuse has magnitude 0.42
```

```
The star Betelgeuse has magnitude 0.42
```

The `f` tells Python to look inside the string for `{}` and substitute variables. This creates much more readable output than trying to combine strings and numbers manually.

## Formatting Numbers in F-strings

### Controlling Decimal Places

Real measurements have limited precision. F-strings let you control how numbers display:

```
distance = 47.3821
magnitude = 0.42  # Using earlier defined value

# Two decimal places
print(f"Distance: {distance:.2f} pc")
# Output: Distance: 47.38 pc

# Scientific notation
flux = 0.000000123
print(f"Flux: {flux:.2e}")
# Output: Flux: 1.23e-07

# Field width for tables
print(f"Padded: {magnitude:8.3f}")  # 8 characters wide, 3 decimals
```

```
Distance: 47.38 pc
Flux: 1.23e-07
Padded:    0.420
```

After the colon comes the format specification (with rounding):

* `.2f` means "floating point with 2 decimal places"
* `.2e` means "scientific notation with 2 decimal places"
* `8.3f` means "8 characters wide with 3 decimals"

This is essential for creating professional-looking output and data tables.

## Python's Indexing System

### Counting from Zero

Python counts positions starting from 0, not 1. This might seem odd, but it's consistent and has mathematical advantages:

```
Position:  0    1    2    3    4
Element:  1st  2nd  3rd  4th  5th
```

Think of positions as offsets from the beginning. The first element is at offset 0 (the very start), the second is at offset 1, and so on.

### Negative Indices

Python also lets you count backwards from the end using negative numbers:

```
Positive:   0    1    2    3    4
Element:   1st  2nd  3rd  4th  5th
Negative:  -5   -4   -3   -2   -1
```

So `-1` always means "last element", `-2` means "second to last", and so on. This is incredibly useful when you don't know how long a sequence is but need the last few elements.

## Indexing Strings

### Accessing Individual Characters

Apply indexing to extract specific characters from strings:

```
star = "Sirius"
print(f"First character: {star[0]}")   # 'S' - first character
print(f"Second character: {star[1]}")  # 'i' - second character
print(f"Last character: {star[-1]}")   # 's' - last character
print(f"Second to last: {star[-2]}")   # 'u' - second to last
```

```
First character: S
Second character: i
Last character: s
Second to last: u
```

Each character has a position, and you access it using square brackets with the index.

### String Slicing

Extract portions of strings using slice notation `[start:stop]`:

```
catalog = "HD209458"
print(f"First 2 chars: {catalog[:2]}")   # 'HD' - first 2 chars
print(f"From position 2 onward: {catalog[2:]}")   # '209458' - from position 2 onward
print(f"Positions 2, 3, 4: {catalog[2:5]}")  # '209' - positions 2, 3, 4
```

```
First 2 chars: HD
From position 2 onward: 209458
Positions 2, 3, 4: 209
```

Key insight: `[start:stop]` goes from `start` up to but NOT including `stop`. This seems strange but makes the math work out nicely: the number of characters extracted is always `stop - start`.

## String Methods

### Length and Cleaning

Find string length and remove unwanted whitespace:

```
messy = "  VEGA  "
print(f"Length with spaces: {len(messy)}")  # 8 (includes the spaces!)
clean = messy.strip()  # "VEGA" (spaces removed)
print(f"Clean string: {clean}")
print(f"Clean length: {len(clean)}")  # 4
```

```
Length with spaces: 8
Clean string: VEGA
Clean length: 4
```

The `strip()` method removes spaces, tabs, and newlines from both ends only - it does NOT remove spaces between words. This is essential when processing data files where extra spaces often creep in.

### Case Conversion and Replacement

Standardize string formats for consistency:

```
name = "Alpha Centauri"
print(f"Lowercase: {name.lower()}")           # "alpha centauri"
print(f"Uppercase: {name.upper()}")           # "ALPHA CENTAURI"
print(f"With underscores: {name.replace(' ', '_')}") # "Alpha_Centauri"
```

```
Lowercase: alpha centauri
Uppercase: ALPHA CENTAURI
With underscores: Alpha_Centauri
```

These methods don't change the original string - they create new ones. This is because strings are immutable (unchangeable). Since `strip()` only removes spaces from the beginning and end. To remove ALL spaces (including those between words), use `replace(' ', '')`.

### String Split and Join

The `split()` method breaks strings at specified characters:

```
coordinates = "10:23:45.6"
parts = coordinates.split(':')
print(parts)  # ['10', '23', '45.6']
```

```
['10', '23', '45.6']
```

The opposite is `join()` - it combines list elements into a string:

```
values = ['15.3', '14.8', '15.1']
csv_line = ','.join(values)
print(csv_line)  # "15.3,14.8,15.1"
```

```
15.3,14.8,15.1
```

These are essential for parsing and creating data files.

### String Testing Methods

Check string properties to validate data:

```
target = "NGC1234"  # NGC = New General Catalogue
coords = "10:23:45.6"

# Test beginning and end
print(f"Starts with NGC: {target.startswith('NGC')}")  # True
print(f"Ends with '34': {target.endswith('34')}")     # True

# Test character types
print(f"Is uppercase: {target.isupper()}")          # False (has numbers too)
print(f"Is all digits: {target.isdigit()}")          # False (has letters too)
print(f'"1234" is all digits: {"1234".isdigit()}')         # True (all digits)

# Check for substring
print(f"Contains colon: {':' in coords}")            # True
```

```
Starts with NGC: True
Ends with '34': True
Is uppercase: True
Is all digits: False
"1234" is all digits: True
Contains colon: True
```

These return boolean values for filtering and validation.

### Building Filenames and IDs

Combine strings to create standardized names:

```
# Using f-strings for complex names
object_id = "HD"
number = "209458"
full_name = f"{object_id}{number}"
print(full_name)  # "HD209458"

# Create observation filenames
observation_date = "2024-03-15"
target = "M31"  # Andromeda Galaxy
filter_name = "V"  # Visual band

filename = f"{target}_{observation_date}_{filter_name}.fits"
print(filename)  # "M31_2024-03-15_V.fits"
```

```
HD209458
M31_2024-03-15_V.fits
```

Systematic naming ensures your files are organized and easily identified.

## Booleans

### Why Booleans Matter

So far we've stored numbers and text. But astronomy is full of yes/no questions:

* Is this star bright enough to observe?
* Does this measurement look valid?
* Is this object in the northern sky?

Booleans store these `True`/`False` decisions, and they're essential for filtering and analyzing data.

## Boolean Values: True and False

### Defining Booleans

Create boolean variables using `True` and `False` (note the capital letters!):

```
is_bright = True
is_variable = False  
has_companion = True
```

These values help track binary properties of astronomical objects - characteristics that are either present or absent.

## Creating Booleans with Comparisons

### Comparison Operators

Most booleans come from comparing values:

```
magnitude = 15.3

# Test different conditions
print(f"Brighter than mag 10? {magnitude < 10}")     # False - not brighter than 10
print(f"Fainter than mag 20? {magnitude > 20}")      # False - not fainter than 20
print(f"Exactly mag 15.3? {magnitude == 15.3}")      # True - exactly 15.3
```

```
Brighter than mag 10? False
Fainter than mag 20? False
Exactly mag 15.3? True
```

### Critical Distinction: = vs ==

This confuses many beginners:

* Single `=` means "store this value" (assignment)
* Double `==` means "are these equal?" (comparison)

```
magnitude = 15.3   # ASSIGNS 15.3 to magnitude
print(f"Is magnitude equal to 15.3? {magnitude == 15.3}")  # TESTS if magnitude equals 15.3
```

```
Is magnitude equal to 15.3? True
```

Mixing these up is a common source of bugs!

## Logical Operators: and, or, not

### Combining Conditions

Real astronomical queries often involve multiple criteria:

```
magnitude = 11.5
declination = 30.2  # Positive = northern sky

# BOTH must be true (and)
northern_and_bright = (declination > 0) and (magnitude < 12)
print(northern_and_bright)  # True

# AT LEAST ONE must be true (or)
interesting = (magnitude < 5) or (declination > 80)
print(interesting)  # False

# Flip the result (not)
not_too_faint = not (magnitude > 15)
print(not_too_faint)  # True
```

```
True
False
True
```

These operators let you build complex selection criteria from simple comparisons.

## Bitwise Operators: & and |

### Similar but Different

Bitwise operators look similar to `and`/`or` but have crucial differences:

```
# Requires parentheses around comparisons!
bright = (magnitude < 12) & (declination > 0)
special = (magnitude < 5) | (declination > 80)
```

Why learn both? When you work with NumPy arrays later, only `&` and `|` work element-wise. The parentheses are essential because `&` and `|` have different precedence than comparisons.

## Lists: Storing Multiple Values

### Creating Lists

In astronomy, we rarely work with single numbers. Lists store sequences of related values:

```
magnitudes = [15.2, 15.3, 15.1, 15.4, 15.2]
star_names = ["Sirius", "Vega", "Betelgeuse"]
```

Square brackets `[]` create lists. Items are separated by commas. Lists can hold any type of data, even mixed types.

### Accessing List Elements

Lists use the same zero-based indexing we learned:

```
print(magnitudes[0])   # 15.2 - first observation
print(magnitudes[-1])  # 15.2 - last observation
print(magnitudes[2])   # 15.1 - third observation
```

```
15.2
15.2
15.1
```

Think of the index as telling Python how many positions to count from the start (or from the end if negative).

## Lists are Mutable (Changeable)

### Modifying Existing Elements

Unlike strings, you can change list contents after creation:

```
observations = [15.2, 15.3, 15.1]
print(f"Original: {observations}")

observations[0] = 15.0  # Change first element
print(f"After change: {observations}")
```

```
Original: [15.2, 15.3, 15.1]
After change: [15.0, 15.3, 15.1]
```

This mutability makes lists perfect for accumulating data during observations or processing.

### Adding Elements

Grow lists dynamically as new data arrives:

```
observations.append(15.4)  # Add to the end
print(f"After append: {observations}")
```

```
After append: [15.0, 15.3, 15.1, 15.4]
```

The `append()` method is how you build up lists one element at a time - essential for reading data files line by line.

## List Methods

### Insertion and Removal

Control exactly where elements go and which ones to remove:

```
mags = [15.2, 15.3, 15.1]
mags.insert(1, 15.25)  # Insert at position 1
print(mags)  # [15.2, 15.25, 15.3, 15.1]

deleted = mags.pop()   # Remove and return last element  
print(f"Deleted: {deleted}")
print(f"Remaining: {mags}")
```

```
[15.2, 15.25, 15.3, 15.1]
Deleted: 15.1
Remaining: [15.2, 15.25, 15.3]
```

The `insert()` method takes two arguments: where to insert and what to insert. The `pop()` method both removes and returns an element, letting you save it if needed.

## List Slicing and Functions

### Extracting Portions

Use slicing to analyze subsequences:

```
mags = [10.5, 11.2, 9.8, 12.3, 10.7]
first_three = mags[:3]   # [10.5, 11.2, 9.8]
last_two = mags[-2:]     # [12.3, 10.7]
print(f"First three: {first_three}")
print(f"Last two: {last_two}")
```

```
First three: [10.5, 11.2, 9.8]
Last two: [12.3, 10.7]
```

### Built-in Analysis Functions

Python provides essential statistical functions:

```
print(f"Count: {len(mags)}")    # 5 - count elements
print(f"Brightest (min): {min(mags)}")   # 9.8 - brightest (smallest magnitude)
print(f"Faintest (max): {max(mags)}")    # 12.3 - faintest
print(f"Sum: {sum(mags)}")      # 54.5 - total

# Calculate average
average = sum(mags) / len(mags)
print(f"Average: {average}")
```

```
Count: 5
Brightest (min): 9.8
Faintest (max): 12.3
Sum: 54.5
Average: 10.9
```

Remember: in astronomy, smaller magnitude means brighter!

## List Search and Sort

### Finding Elements

Locate and count specific values:

```
mags = [10.5, 11.2, 9.8, 12.3, 9.8]

print(f"Position of first 9.8: {mags.index(9.8)}")   # 2 - position of FIRST 9.8
print(f"How many 9.8 values: {mags.count(9.8)}")   # 2 - number of times 9.8 appears
mags.remove(9.8)  # Removes FIRST 9.8 only
print(f"After removing first 9.8: {mags}")
```

```
Position of first 9.8: 2
How many 9.8 values: 2
After removing first 9.8: [10.5, 11.2, 12.3, 9.8]
```

### Sorting Without Destruction

The `sorted()` function creates a new sorted list, preserving the original:

```
original = [10.5, 11.2, 9.8, 12.3, 10.7]
bright_to_faint = sorted(original)
faint_to_bright = sorted(original, reverse=True)

print(f"Original unchanged: {original}")
print(f"Sorted: {bright_to_faint}")
```

```
Original unchanged: [10.5, 11.2, 9.8, 12.3, 10.7]
Sorted: [9.8, 10.5, 10.7, 11.2, 12.3]
```

This preserves time-ordering while allowing magnitude-based analysis.

## Lists: Reference vs Copy

### The Hidden Danger

This behavior surprises many beginners. Assignment doesn't copy lists - it creates another name for the SAME list:

```
list1 = [15.2, 15.3, 15.1]
list2 = list1  # NOT a copy - same list, different name!

list2[0] = 99.9
print(list1)  # [99.9, 15.3, 15.1] - list1 changed too!
```

```
[99.9, 15.3, 15.1]
```

Both variables point to the same list in memory. Changing one changes both!

### Creating True Copies

Use `.copy()` when you need independent lists:

```
list1 = [15.2, 15.3, 15.1]
list2 = list1.copy()  # TRUE copy

list2[0] = 99.9
print(list1)  # [15.2, 15.3, 15.1] - unchanged!
print(list2)  # [99.9, 15.3, 15.1] - only this changed
```

```
[15.2, 15.3, 15.1]
[99.9, 15.3, 15.1]
```

Always use `.copy()` when you want to modify a list without affecting the original. This prevents subtle bugs that can be hard to track down.

## Tuples: Immutable Sequences

### Creating Unchangeable Sequences

Tuples are like lists that can't be modified. Perfect for data that should stay constant:

```
coords = (101.287, -16.716)  # RA and Dec in degrees
star_info = ("Vega", 0.03, "A0V")  # name, magnitude, spectral type
```

Parentheses create tuples (though they're sometimes optional). Once created, the contents cannot change.

### Accessing but Not Modifying

Access tuple elements just like lists:

```
ra = coords[0]
dec = coords[1]
print(f"RA: {ra}, Dec: {dec}")

# But you cannot modify:
# coords[0] = 102.0  # TypeError! Tuples are immutable
```

```
RA: 101.287, Dec: -16.716
```

Use tuples for coordinate pairs, RGB colors, or any data that represents a fixed set of related values.

## Tuple Unpacking

### Elegant Value Extraction

One of Python's most beautiful features - extract all tuple values at once:

```
ra, dec = coords  # Unpack both values
print(f"RA: {ra}, Dec: {dec}")

# Works with any number of elements
name, magnitude, spectral_type = star_info
print(f"{name}: magnitude {magnitude}, type {spectral_type}")
```

```
RA: 101.287, Dec: -16.716
Vega: magnitude 0.03, type A0V
```

This makes code more readable by giving meaningful names to each component.

### Multiple Assignment

Tuples enable assigning multiple variables in one line:

```
# Create multiple variables at once
star_name, magnitude, distance = "Sirius", -1.46, 2.64
print(f"{star_name}: {magnitude} mag at {distance} pc")
```

```
Sirius: -1.46 mag at 2.64 pc
```

This is actually creating a tuple on the right and unpacking it on the left.

### Value Swapping Magic

Tuple unpacking enables elegant variable swapping:

```
mag1 = 15.3
mag2 = 14.8
print(f"Before: mag1={mag1}, mag2={mag2}")

mag1, mag2 = mag2, mag1  # Swap in one line!
print(f"After: mag1={mag1}, mag2={mag2}")
```

```
Before: mag1=15.3, mag2=14.8
After: mag1=14.8, mag2=15.3
```

No temporary variable needed! Python creates a tuple on the right, then unpacks it on the left.

## Dictionaries: Labeled Data

### From Positions to Names

Lists store data by position, but astronomical objects have named properties. Dictionaries use descriptive keys instead of numeric positions:

```
star = {
    "name": "Betelgeuse",
    "magnitude": 0.42,
    "type": "M1-2Ia-Ib"
}
```

Curly braces `{}` create dictionaries. Each entry pairs a key (label) with a value (data).

### Comparing Lists and Dictionaries

Consider storing information about a star:

```
# Using a list - hard to remember what each position means
star_list = ["Betelgeuse", 88.793, 7.407, 0.42]  # name, RA, Dec, magnitude

# Using a dictionary - self-documenting
star_dict = {
    'name': 'Betelgeuse',
    'ra': 88.793,
    'dec': 7.407,
    'magnitude': 0.42
}

# Compare accessing data
print(star_list[0])      # What's at position 0 again?
print(star_dict['name'])  # Obviously the name!
```

```
Betelgeuse
Betelgeuse
```

Dictionaries make your code self-documenting.

## Dictionary Keys and Values

### Understanding Key-Value Pairs

Each dictionary entry has two parts:

```
"magnitude": 0.42
    ↑         ↑
   KEY     VALUE
```

Access values using their keys:

```
print(star["name"])       # "Betelgeuse"
print(star["magnitude"])  # 0.42

# Modify values
star["magnitude"] = 0.45  # Betelgeuse is variable!

# Add new key-value pairs
star["distance"] = 197    # parsecs
```

```
Betelgeuse
0.42
```

Keys are like labels on filing folders - they tell you what's inside without having to remember positions.

## Safe Dictionary Access

### Handling Missing Keys

Accessing a non-existent key causes an error. Use `.get()` for safe access with a default:

```
star = {"name": "Vega", "mag": 0.03}

# This would error:
# print(star["distance"])  # KeyError!

# Safe access with default
distance = star.get("distance", "unknown")
print(distance)  # "unknown"

# When key exists, get returns the actual value
magnitude = star.get("mag", 99)
print(magnitude)  # 0.03 (not 99)
```

```
unknown
0.03
```

The second argument to `.get()` is the default value returned if the key doesn't exist.

### Checking for Keys

Test if a key exists before using it:

```
print(f"'mag' in star: {'mag' in star}")       # True - key exists
print(f"'distance' in star: {'distance' in star}")  # False - key doesn't exist
```

```
'mag' in star: True
'distance' in star: False
```

This returns a boolean you can use in if-statements (which you'll learn next lecture).

## Dictionary Methods

### Exploring Dictionary Structure

Extract and analyze dictionary components:

```
star = {"name": "Vega", "mag": 0.03, "type": "A0V"}

print(f"Keys: {list(star.keys())}")    # ["name", "mag", "type"]
print(f"Values: {list(star.values())}")  # ["Vega", 0.03, "A0V"]
print(f"Items: {list(star.items())}")   # [("name", "Vega"), ("mag", 0.03), ("type", "A0V")]

print(f"Number of entries: {len(star)}")  # 3 - counts key-value pairs
```

```
Keys: ['name', 'mag', 'type']
Values: ['Vega', 0.03, 'A0V']
Items: [('name', 'Vega'), ('mag', 0.03), ('type', 'A0V')]
Number of entries: 3
```

These methods help you understand and process dictionary contents programmatically.

## Nested Dictionaries

### Building Complex Catalogs

Dictionaries can contain other dictionaries, perfect for star catalogs:

```
catalog = {
    "sirius": {
        "mag": -1.46,
        "dist": 2.64,
        "type": "A1V"
    },
    "vega": {
        "mag": 0.03,
        "dist": 7.68,
        "type": "A0V"
    }
}

# Access nested data with multiple brackets
sirius_mag = catalog["sirius"]["mag"]  # -1.46
vega_dist = catalog["vega"]["dist"]    # 7.68

print(f"Sirius magnitude: {sirius_mag}")
print(f"Vega distance: {vega_dist} parsecs")
```

```
Sirius magnitude: -1.46
Vega distance: 7.68 parsecs
```

Each bracket level goes deeper into the structure. First bracket gets the star, second bracket gets the property.

### Dictionary References

Like lists, dictionaries use references:

```
star = {"name": "Vega"}
backup = star  # Reference, not copy!
star["mag"] = 0.03
print(len(backup))  # 2 - backup changed too!
```

```
2
```

Use `.copy()` for dictionaries too when you need independence.

## Practical Examples

### Example 1: Complete Coordinate Conversion

Let's combine string processing, type conversion, and calculation to convert right ascension from hours:minutes:seconds to decimal degrees:

```
ra_hms = "14:23:15.2"
print(f"Converting {ra_hms} to decimal degrees")

# Split at colons and unpack
h, m, s = ra_hms.split(':')
print(f"Components: h={h}, m={m}, s={s}")

# Convert strings to numbers
hours = float(h)
minutes = float(m)
seconds = float(s)

# Calculate decimal hours
decimal_hours = hours + minutes/60 + seconds/3600
print(f"Decimal hours: {decimal_hours:.6f}")

# Convert to degrees (Earth rotates 360° in 24 hours)
decimal_degrees = decimal_hours * 15
print(f"Result: {decimal_degrees:.4f} degrees")
```

```
Converting 14:23:15.2 to decimal degrees
Components: h=14, m=23, s=15.2
Decimal hours: 14.387556
Result: 215.8133 degrees
```

This example integrates string methods, type conversion, arithmetic, and formatted output - all essential skills for processing astronomical data.

### Example 2: Building and Analyzing a Star Catalog

Create a multi-level data structure and extract statistics:

```
stars = {
    'sirius': {'mag': -1.46, 'distance_pc': 2.64, 'type': 'A1V'},
    'vega': {'mag': 0.03, 'distance_pc': 7.68, 'type': 'A0V'},
    'betelgeuse': {'mag': 0.42, 'distance_pc': 197, 'type': 'M1-2Ia-Ib'}
}

# Extract all star names
star_names = list(stars.keys())
print(f"Stars in catalog: {star_names}")

# Build magnitude list
magnitudes = []
for name in star_names:
    magnitudes.append(stars[name]['mag'])
print(f"Magnitudes: {magnitudes}")

# Find brightest (minimum magnitude)
brightest_mag = min(magnitudes)
brightest_idx = magnitudes.index(brightest_mag)
brightest_star = star_names[brightest_idx]
print(f"Brightest: {brightest_star} at magnitude {brightest_mag}")

# Calculate statistics
mean_mag = sum(magnitudes) / len(magnitudes)
mag_range = max(magnitudes) - min(magnitudes)
print(f"Mean magnitude: {mean_mag:.2f}")
print(f"Magnitude range: {mag_range:.2f}")
```

```
Stars in catalog: ['sirius', 'vega', 'betelgeuse']
Magnitudes: [-1.46, 0.03, 0.42]
Brightest: sirius at magnitude -1.46
Mean magnitude: -0.34
Magnitude range: 1.88
```

This demonstrates how dictionaries, lists, and built-in functions work together to organize and analyze astronomical data.

## Summary

### Key Concepts

In this lecture, you've learned:

* **Variables and data types**: How Python stores numbers, text, and logical values for astronomical calculations
* **Collections**: Lists for sequences, tuples for fixed data, and dictionaries for labeled properties
* **String manipulation**: Essential methods for processing text-based astronomical data and catalogs
* **Type conversion and special values**: Handling real-world data with missing values and format conversions

### What You Can Now Do

After working through this material, you should be able to:

* Store and manipulate astronomical measurements using appropriate data types
* Process string-based coordinate formats and convert between representations
* Build and analyze collections of stellar data using lists and dictionaries
* Handle missing data and special values common in observational astronomy

### Practice Suggestions

To solidify these concepts:

1. Create a dictionary catalog of your favorite astronomical objects with their properties
2. Practice converting between different coordinate formats (HMS/DMS to decimal)
3. Build lists of magnitude measurements and calculate basic statistics

### Looking Ahead

Next lecture, we'll build on these foundations to explore control structures (if/else statements and loops) and functions. The data structures you've mastered today—especially lists and dictionaries—will be essential for automating complex astronomical analysis workflows and processing large datasets efficiently.
