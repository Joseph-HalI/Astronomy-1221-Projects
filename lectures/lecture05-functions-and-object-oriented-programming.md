# Functions and Object-Oriented Programming

## Introduction

In astronomy, we perform the same calculations repeatedly. Converting magnitudes to fluxes, calculating distances, correcting for atmospheric effects - these operations appear dozens of times in a typical analysis script. Copy-pasting formulas is dangerous: when you need to fix a bug or update a formula, you have to hunt down every copy.

Today we'll learn Python's two main tools for organizing code: **functions** and **classes**. Functions package calculations into reusable units. Classes go further, bundling data and functions together to model objects like stars, observations, or instruments.

## Functions - Packaging Reusable Code

### The Problem with Repetition

Let's start with a real scenario. You're analyzing three stars and need to calculate their absolute magnitudes (how bright they would appear at a standard distance of 10 parsecs).

First, we need to import NumPy for mathematical functions:

```
import numpy as np  # NumPy provides mathematical functions like log10
```

Now let's calculate absolute magnitudes for our stars:

```
# Star 1: Vega
app_mag_1 = 0.03  # Apparent magnitude (how bright it looks from Earth)
distance_1 = 7.68  # Distance in parsecs

# The distance modulus formula
abs_mag_1 = app_mag_1 - 5 * np.log10(distance_1) + 5

print(f"Vega: apparent={app_mag_1:.2f}, absolute={abs_mag_1:.2f}")
```

```
Vega: apparent=0.03, absolute=0.60
```

Now for the second star:

```
# Star 2: Proxima Centauri
app_mag_2 = 11.13  # Much fainter in our sky
distance_2 = 1.30  # But much closer!

abs_mag_2 = app_mag_2 - 5 * np.log10(distance_2) + 5

print(f"Proxima Cen: apparent={app_mag_2:.2f}, absolute={abs_mag_2:.2f}")
```

```
Proxima Cen: apparent=11.13, absolute=15.56
```

And the third:

```
# Star 3: Betelgeuse
app_mag_3 = 0.42
distance_3 = 168  # Much farther away

abs_mag_3 = app_mag_3 - 5 * np.log10(distance_3) + 5

print(f"Betelgeuse: apparent={app_mag_3:.2f}, absolute={abs_mag_3:.2f}")
```

```
Betelgeuse: apparent=0.42, absolute=-5.71
```

We typed the same formula three times. What if we made a typo in one? What if we need to modify the formula later? We'd have to find and change all three copies.

### Creating Your First Function

A function packages code into a reusable unit. Let's understand every part:

```
def apparent_to_absolute(app_mag, distance):
    """Convert apparent magnitude to absolute magnitude."""
    abs_mag = app_mag - 5 * np.log10(distance) + 5
    return abs_mag
```

Let's break down each keyword and symbol:

* `def` - Short for "define". This keyword tells Python we're creating a function
* `apparent_to_absolute` - The function's name. We choose this name. Use descriptive names!
* `(app_mag, distance)` - Parameters inside parentheses. These are the inputs the function needs
* `:` - The colon marks the end of the function header. Everything after must be indented
* `"""..."""` - Triple quotes create a docstring that explains what the function does
* `abs_mag = ...` - The calculation happens inside the function
* `return` - This keyword sends the result back to whoever called the function

### Important: Parameters vs Arguments

These terms are often confused:

* **Parameters** are the variable names in the function definition (`app_mag`, `distance`)
* **Arguments** are the actual values you pass when calling the function (`0.03`, `7.68`)

```
# Parameters are in the definition
def apparent_to_absolute(app_mag, distance):  # app_mag and distance are PARAMETERS
    abs_mag = app_mag - 5 * np.log10(distance) + 5
    return abs_mag

# Arguments are the actual values
vega_abs = apparent_to_absolute(0.03, 7.68)  # 0.03 and 7.68 are ARGUMENTS
```

### Using Your Function

Now we can call our function just like Python's built-in functions:

```
# Call the function for each star
vega_abs = apparent_to_absolute(0.03, 7.68)
print(f"Vega: {vega_abs:.2f}")
```

```
Vega: 0.60
```

```
proxima_abs = apparent_to_absolute(11.13, 1.30)
print(f"Proxima Cen: {proxima_abs:.2f}")
```

```
Proxima Cen: 15.56
```

```
betelgeuse_abs = apparent_to_absolute(0.42, 168)
print(f"Betelgeuse: {betelgeuse_abs:.2f}")
```

```
Betelgeuse: -5.71
```

If we need to fix the formula, we change it in ONE place - inside the function definition.

### Understanding `return`

The `return` keyword is crucial. It's different from `print`:

```
def function_with_print(x):
    """This function only prints."""
    result = x * 2
    print(result)  # Shows on screen but doesn't send back

def function_with_return(x):
    """This function returns a value."""
    result = x * 2
    return result  # Sends the value back
```

Let's see the difference:

```
# With print - can't use the result
value1 = function_with_print(5)  # Prints 10
print(f"value1 is: {value1}")  # value1 is None!
```

```
10
value1 is: None
```

```
# With return - can use the result
value2 = function_with_return(5)  # Doesn't print anything
print(f"value2 is: {value2}")  # value2 is 10
```

```
value2 is: 10
```

### Common Mistake: Forgetting to Return

This is one of the most common beginner errors:

```
def broken_function(x):
    """Forgot to return!"""
    result = x * 2
    # Oops, no return statement!

answer = broken_function(5)
print(f"Answer: {answer}")  # Answer is None!
```

```
Answer: None
```

Always remember: if you want a value back from a function, you must `return` it!

### Functions Can Return Multiple Values

Sometimes we need to calculate several things at once. Python lets us return multiple values:

```
def analyze_color(b_mag, v_mag):
    """
    Calculate color index and estimate temperature.
    
    B-V color tells us about stellar temperature:
    negative = hot blue stars, positive = cooler red stars
    """
    b_v = b_mag - v_mag
    
    # Approximate temperature (simplified formula)
    temp = 7000 - 1000 * b_v  # Very rough approximation
    
    return b_v, temp  # Return TWO values separated by comma
```

When calling a function that returns multiple values:

```
# Capture both values
color, temperature = analyze_color(5.48, 4.83)
print(f"Sun: B-V = {color:.2f}, Temperature ≈ {temperature:.0f} K")
```

```
Sun: B-V = 0.65, Temperature ≈ 6350 K
```

You can also capture them as a tuple:

```
# Returns a tuple (pair of values)
result = analyze_color(5.48, 4.83)
print(f"Color: {result[0]:.2f}, Temperature: {result[1]:.0f}")
```

```
Color: 0.65, Temperature: 6350
```

### Default Parameters

Sometimes parameters have typical values. We can set defaults using the `=` sign:

```
def apparent_to_absolute(app_mag, distance, extinction=0.0):
    """
    Convert apparent to absolute magnitude.
    
    extinction: absorption by dust (default: 0.0 = no dust)
    """
    # Correct for extinction first
    corrected_mag = app_mag - extinction
    
    # Then apply distance modulus
    abs_mag = corrected_mag - 5 * np.log10(distance) + 5
    
    return abs_mag
```

The `extinction=0.0` means: "If no third argument is given, use 0.0". This gives us flexibility:

```
# Two arguments - extinction uses default of 0.0
abs_mag_clear = apparent_to_absolute(10.5, 100)
print(f"Clear (default): {abs_mag_clear:.2f}")
```

```
Clear (default): 5.50
```

```
# Three arguments - we specify extinction
abs_mag_dusty = apparent_to_absolute(10.5, 100, 1.2)
print(f"With extinction: {abs_mag_dusty:.2f}")
```

```
With extinction: 4.30
```

### Keyword Arguments

When calling a function, you can use the parameter names for clarity:

```
# Positional arguments (order matters!)
result1 = apparent_to_absolute(10.5, 100, 0.3)
print(f"Positional: {result1:.2f}")
```

```
Positional: 5.20
```

```
# Keyword arguments (names make it clear)
result2 = apparent_to_absolute(
    app_mag=10.5,
    distance=100,
    extinction=0.3
)
print(f"With keywords: {result2:.2f}")
```

```
With keywords: 5.20
```

```
# You can mix, but positional must come first
result3 = apparent_to_absolute(10.5, 100, extinction=0.3)
print(f"Mixed: {result3:.2f}")
```

```
Mixed: 5.20
```

### Common Mistake: Arguments in Wrong Order

This is a subtle but dangerous error:

```
# WRONG - arguments reversed!
# This treats 100 as magnitude and 10.5 as distance
wrong = apparent_to_absolute(100, 10.5)  
print(f"Wrong order: {wrong:.2f}")

# Using keywords prevents this mistake
right = apparent_to_absolute(distance=100, app_mag=10.5)
print(f"Keywords prevent mistakes: {right:.2f}")
```

```
Wrong order: 99.89
Keywords prevent mistakes: 5.50
```

Using keyword arguments makes your code clearer and prevents order mistakes!

### Understanding Variable Scope

Variables inside functions are **local** - they exist only within the function:

```
def demonstrate_scope():
    """Variables created inside are local."""
    local_variable = 42
    print(f"Inside function: {local_variable}")
    return local_variable * 2

result = demonstrate_scope()
```

```
Inside function: 42
```

Now try to access the local variable outside:

```
# This will cause an error!
try:
    print(local_variable)  # local_variable doesn't exist here!
except NameError:
    print("Error: local_variable is not defined outside the function")
```

```
Error: local_variable is not defined outside the function
```

### Global Variables and Functions

Variables outside functions are **global**. Functions can read global variables:

```
# Global variable
global_value = 100

def use_global():
    """Functions can READ global variables."""
    print(f"Function sees global: {global_value}")
    return global_value * 2

result = use_global()
print(f"Result: {result}")
```

```
Function sees global: 100
Result: 200
```

However, when you try to assign to a variable name inside a function, Python creates a NEW local variable instead of modifying the global:

```
# Global variable
extinction = 2.0
print(f"Global extinction starts as: {extinction}")

def process_magnitude(mag):
    # This creates a NEW local variable called extinction
    extinction = 0.5  # This is LOCAL, not the global one
    corrected = mag - extinction
    print(f"Inside function, extinction = {extinction}")
    return corrected

result = process_magnitude(10.0)
print(f"Global extinction still: {extinction}")  # Unchanged!
```

```
Global extinction starts as: 2.0
Inside function, extinction = 0.5
Global extinction still: 2.0
```

This isolation is actually good - it prevents functions from accidentally messing up your main program's variables! If you really need to modify a global variable (rarely a good idea), you must use the `global` keyword:

```
counter = 0

def increment():
    global counter  # Tell Python to use the global variable
    counter += 1

print(f"Counter before: {counter}")
increment()
print(f"Counter after: {counter}")
```

```
Counter before: 0
Counter after: 1
```

But it's better to avoid modifying global variables - return values instead!

### Documentation and the help() Function

Every function should have a docstring explaining what it does:

```
def airmass_from_altitude(altitude):
    """
    Calculate airmass from altitude.
    
    Higher altitude = less atmosphere = lower airmass.
    Airmass of 1 means looking straight up (zenith).
    """
    zenith_angle = 90 - altitude
    airmass = 1 / np.cos(np.deg2rad(zenith_angle))
    return airmass
```

The docstring helps users understand the function. You can view docstrings using the `help()` function:

```
# To see the docstring:
help(airmass_from_altitude)
```

```
Help on function airmass_from_altitude in module __main__:

airmass_from_altitude(altitude)
    Calculate airmass from altitude.

    Higher altitude = less atmosphere = lower airmass.
    Airmass of 1 means looking straight up (zenith).
```

The `help()` function works on many things in Python:

```
# Works on built-in functions
# help(print)  # Shows how print() works

# Works on modules (we'll learn about these next!)
import math
# help(math.cos)  # Shows how cosine function works

# We'll see later it also works on classes and objects!
print("help() can show documentation for functions, modules, and classes")
```

```
help() can show documentation for functions, modules, and classes
```

### Importing and Organizing Functions

As your projects grow, putting all functions in one file becomes unwieldy. Python lets you organize functions into separate files called **modules**. A module is simply a `.py` file containing Python code.

#### Creating Your Own Module

Let's say you have several astronomy calculations you use frequently. You would create a new file called `astro_tools.py` in your project folder:

```
# File: astro_tools.py
import numpy as np

def apparent_to_absolute(app_mag, distance, extinction=0.0):
    """Convert apparent magnitude to absolute magnitude."""
    corrected_mag = app_mag - extinction
    abs_mag = corrected_mag - 5 * np.log10(distance) + 5
    return abs_mag

def flux_from_magnitude(magnitude):
    """Calculate relative flux from magnitude."""
    return 10**(-0.4 * magnitude)

def airmass_from_altitude(altitude):
    """Calculate airmass from altitude in degrees."""
    zenith_angle = 90 - altitude
    airmass = 1 / np.cos(np.deg2rad(zenith_angle))
    return airmass
```

This file becomes a module that you can import and use in other Python files or notebooks.

#### Importing Your Module

Once you've saved `astro_tools.py` in the same folder as your notebook or script, you can import it and use the functions. Here's how it works:

```
# In your main analysis file or notebook:
import astro_tools

# Now you can use functions from the module
abs_mag = astro_tools.apparent_to_absolute(10.5, 100)
flux = astro_tools.flux_from_magnitude(5.0)

print(f"Absolute magnitude: {abs_mag:.2f}")  # Output: 5.50
print(f"Flux: {flux:.4f}")                   # Output: 0.0100
```

Notice how we use `astro_tools.function_name()` to call the functions - the module name acts as a prefix.

#### Different Ways to Import

Python offers several import styles, each with its own advantages:

**Method 1: Import the entire module (recommended for clarity)**

```
import astro_tools
result = astro_tools.flux_from_magnitude(5.0)
# Clear where the function comes from
```

**Method 2: Import with an alias (useful for long module names)**

```
import astro_tools as astro
result = astro.flux_from_magnitude(5.0)
# Shorter to type, still clear
```

**Method 3: Import specific functions (convenient but can cause confusion)**

```
from astro_tools import flux_from_magnitude, airmass_from_altitude
result = flux_from_magnitude(5.0)  # No module prefix needed
# Convenient but less clear about the source
```

It's important to understand that in all three import methods above, Python reads the entire module into memory. The differences are only in how you access the functions afterward. Method 1 has the advantage of being simple and straightforward - you always know exactly which module a function comes from when you see `astro_tools.function_name()` in your code. Method 2 works exactly the same way, but becomes useful when the module filename is long and you want something shorter and easier to type repeatedly in your code.

Method 3 might appear to only load specific functions, but Python still reads the entire module behind the scenes. We choose to import only certain function names for different reasons: sometimes the module contains many functions and we only want to use a few of them, or we want to avoid function name conflicts and confusion that could arise if multiple modules have functions with the same names. This approach also makes our code cleaner since we don't need to use the module prefix every time. Even though Python reads the entire module regardless of which import method we use, Method 3 gives us more control over our namespace and can make our code more readable.

#### Why Use Modules?

Modules provide several benefits:

1. **Organization** - Group related functions together
2. **Reusability** - Use the same functions across multiple projects
3. **Maintainability** - Update functions in one place
4. **Namespace** - Avoid naming conflicts (you can have `astro_tools.calculate()` and `math_tools.calculate()`)

#### Module Search Path

When you write `import astro_tools`, Python looks for `astro_tools.py` in:

1. The current directory (where your script/notebook is)
2. Python's standard library directories
3. Installed packages (like NumPy, matplotlib, etc.)

If your module is in the same folder as your notebook, it will be found automatically!

#### Real-World Example

Here's how you might organize a real astronomy project:

```
my_astronomy_project/
│
├── analysis.ipynb          # Your main notebook
├── astro_tools.py         # Module with calculation functions
├── plotting_tools.py      # Module with plotting functions
└── data_processing.py     # Module with data cleaning functions
```

In your notebook, you could then import all these modules:

```
import astro_tools
import plotting_tools as plot
from data_processing import clean_observations

# Now you have access to all your organized functions!
abs_mag = astro_tools.apparent_to_absolute(10.5, 100)
plot.light_curve(times, magnitudes)
clean_data = clean_observations(raw_data)
```

This organization makes your code much easier to manage as projects grow larger!

### Lambda Functions (Anonymous Functions)

Sometimes you need a tiny function for one quick use. **Lambda functions** provide a shortcut. They're called "lambda" after the Greek letter λ (lambda) used in mathematical logic to denote functions.

They're also called **anonymous functions** because they don't have a name - you don't use `def function_name`, you just write the function directly where you need it.

```
# Traditional named function
def square(x):
    return x**2

# Lambda (anonymous) function - no name!
square_lambda = lambda x: x**2

print(f"Traditional: {square(5)}")
print(f"Lambda: {square_lambda(5)}")
```

```
Traditional: 25
Lambda: 25
```

The syntax is: `lambda parameters: expression`

The word "lambda" is just a keyword (like "def") that tells Python "here comes a function". After the colon, you write what the function returns. The lambda automatically returns whatever the expression evaluates to.

```
# More lambda examples
add = lambda x, y: x + y
is_bright = lambda mag: mag < 6.0

print(f"Add: {add(3, 4)}")
print(f"Is mag 5 bright? {is_bright(5.0)}")
print(f"Is mag 10 bright? {is_bright(10.0)}")
```

```
Add: 7
Is mag 5 bright? True
Is mag 10 bright? False
```

Why use lambda functions? They're perfect when you need a simple function just once and don't want to write a full `def` statement. However, they're limited - you can only write a single expression, not multiple statements.

## Object-Oriented Programming

### You've Already Been Using Objects!

Every time you use the dot (`.`) notation, you're working with objects. Let's think about strings for a moment:

```
# Strings are objects
star_name = "betelgeuse"
print(star_name.upper())  # .upper() is a method of the string object
print(star_name.count('e'))  # .count() counts occurrences
print(star_name.replace('e', '*'))  # .replace() is another method
```

```
BETELGEUSE
4
b*t*lg*us*
```

Why is this convenient? The string object bundles the data (the actual text) with functions (methods) that know how to work with that data. You don't need separate functions like `make_uppercase(star_name)` - the string knows how to uppercase itself!

Have you ever wondered why `print()` works with so many different things?

```
print("Hello")  # Prints a string
print(42)       # Prints a number
print([1, 2, 3])  # Prints a list
```

```
Hello
42
[1, 2, 3]
```

This works because each type of object knows how to convert itself to a string for printing. This lecture explains how to create your own objects that work just as smoothly!

### Why Object-Oriented Programming?

Object-Oriented Programming (OOP) is a powerful way to organize code. While beginners often just use functions (which is fine!), understanding OOP will help you read and debug other people's code (most Python libraries use OOP), create more organized and reusable code, and model real-world things naturally.

Think of objects as containers that store both data (called attributes) and functions that work on that data (called methods). This bundling of related data and functionality makes code more intuitive and easier to work with.

Let's explore more built-in objects:

```
# Lists are objects with useful methods
magnitudes = [10.5, 11.2, 9.8]
magnitudes.append(12.1)  # The list knows how to add items to itself
magnitudes.sort()  # The list knows how to sort itself
print(magnitudes)
```

```
[9.8, 10.5, 11.2, 12.1]
```

```
# Numbers have methods too
magnitude = 10.567
print(magnitude.is_integer())  # False
print(int(magnitude))  # Convert to integer
```

```
False
10
```

### Creating Your Own Objects with Classes

A **class** is a blueprint for creating objects. Think of it like a form or template:

```
class Star:
    """A simple star class."""
    
    def __init__(self, name, magnitude):
        """Initialize a new star."""
        self.name = name
        self.magnitude = magnitude
```

Let's understand every part:

* `class` - Keyword that starts a class definition
* `Star` - The class name (use CapitalCase for classes)
* `:` - Colon, then everything indented belongs to the class
* `def __init__(self, ...)` - Magic method that runs when creating a new object
* `self` - Refers to the object being created (required first parameter)
* `self.name = name` - Stores the name in the object

### Understanding `self`

The `self` parameter is probably the most confusing part of classes for beginners. Let's break it down step by step.

#### What is `self`?

`self` is a reference to the current object - the specific star you're working with. Think of it like "this particular star" or "my":

```
class Star:
    def __init__(self, name, magnitude):
        # self = the specific star being created
        self.name = name  # THIS star's name
        self.magnitude = magnitude  # THIS star's magnitude
```

#### Why do we need `self`?

Without `self`, Python wouldn't know which star's data to use:

```
# Imagine we have two stars
vega = Star("Vega", 0.03)
sirius = Star("Sirius", -1.46)

# When we access vega.name, Python needs to know we want VEGA's name, not Sirius's
# That's what self does - it refers to the specific object
```

#### How `self` works when creating objects

Let's trace through what happens step by step:

```
class Star:
    def __init__(self, name, magnitude):
        print(f"Creating star: {name}")
        self.name = name
        self.magnitude = magnitude
```

```
# When we write this:
vega = Star("Vega", 0.03)

# Python does this behind the scenes:
# 1. Creates a new empty Star object
# 2. Calls Star.__init__(new_object, "Vega", 0.03)
# 3. Inside __init__, self = new_object
# 4. Stores "Vega" in new_object.name
# 5. Stores 0.03 in new_object.magnitude
# 6. Returns new_object, which gets stored in vega
```

```
Creating star: Vega
```

#### `self` in methods

Every method needs `self` as its first parameter. This is how the method knows which object's data to use:

```
class Star:
    def __init__(self, name, magnitude):
        self.name = name
        self.magnitude = magnitude
    
    def describe(self):
        # self lets us access THIS star's data
        print(f"{self.name} has magnitude {self.magnitude}")
```

When you call a method, Python automatically passes the object as `self`:

```
vega = Star("Vega", 0.03)

# When you write:
vega.describe()
```

```
Vega has magnitude 0.03
```

What actually happens behind the scenes:

```
# Python actually calls:
Star.describe(vega)  # vega becomes self inside the describe method
```

```
Vega has magnitude 0.03
```

This is why every method needs `self` - it's how the method receives the object to work on!

### Common Mistake: Forgetting `self`

This is the most common error when learning classes. Let's see what goes wrong:

```
# WRONG VERSION - Missing self
class BrokenStar:
    def __init__(self, name, magnitude):
        name = name  # This just assigns name to itself!
        magnitude = magnitude  # Same problem
    
    def show(self):
        print(name)  # Error! What's name?
```

The problem: without `self`, we're just creating local variables that disappear!

```
# Let's see the error:
try:
    broken = BrokenStar("Test", 10.0)
    broken.show()
except NameError as e:
    print(f"Error: {e}")
```

```
Error: name 'name' is not defined
```

Here's the correct version:

```
# CORRECT VERSION - Using self
class WorkingStar:
    def __init__(self, name, magnitude):
        self.name = name  # Store in the object
        self.magnitude = magnitude  # Store in the object
    
    def show(self):
        print(f"{self.name}: {self.magnitude}")  # Access from the object

# This works!
working = WorkingStar("Test", 10.0)
working.show()
```

```
Test: 10.0
```

### Creating and Using Objects

To create an object, call the class like a function:

```
# Create star objects (instances of the Star class)
vega = Star("Vega", 0.03)
sirius = Star("Sirius", -1.46)
```

Each object is independent - they each have their own separate data:

```
print(f"{vega.name} has magnitude {vega.magnitude}")
print(f"{sirius.name} has magnitude {sirius.magnitude}")
```

```
Vega has magnitude 0.03
Sirius has magnitude -1.46
```

You can modify one without affecting the other, just like with strings:

```
# Our objects work similarly
vega.magnitude = 0.00  # Change Vega's magnitude
print(f"Vega: {vega.magnitude}")
print(f"Sirius: {sirius.magnitude}")  # Unchanged!
```

```
Vega: 0.0
Sirius: -1.46
```

### Adding Methods (Functions in Classes)

Methods are functions that belong to objects. They always take `self` as the first parameter so they can access the object's data.

Why are methods useful? Think about strings again - having `star_name.upper()` is much more natural than `make_uppercase(star_name)`. The same principle applies to our custom objects:

```
class Star:
    def __init__(self, name, magnitude):
        self.name = name
        self.magnitude = magnitude
    
    def flux(self):
        """Calculate relative flux from magnitude."""
        # Use self to access this star's magnitude
        return 10**(-0.4 * self.magnitude)
    
    def info(self):
        """Return information string."""
        return f"{self.name}: magnitude {self.magnitude}"
```

Using methods:

```
vega = Star("Vega", 0.03)

# Call methods with dot notation
print(vega.info())
print(f"Flux: {vega.flux():.2f}")
```

```
Vega: magnitude 0.03
Flux: 0.97
```

When you call `vega.flux()`, Python automatically passes `vega` as the `self` parameter to the `flux` method.

### Building a Class Step by Step

Let's build a more complex class gradually to understand how pieces fit together:

#### Step 1: Basic storage

Start with just storing data:

```
class Observation:
    def __init__(self, target, magnitude):
        self.target = target
        self.magnitude = magnitude
```

Test what we have:

```
obs = Observation("Jupiter", -2.5)
print(f"Observed {obs.target} at magnitude {obs.magnitude}")
```

```
Observed Jupiter at magnitude -2.5
```

#### Step 2: Add a simple method

Now let's add functionality:

```
class Observation:
    def __init__(self, target, magnitude):
        self.target = target
        self.magnitude = magnitude
    
    def is_bright(self):
        """Check if brighter than magnitude 6 (naked eye limit)."""
        return self.magnitude < 6.0
```

Test the new method:

```
jupiter = Observation("Jupiter", -2.5)
asteroid = Observation("Vesta", 7.2)

print(f"Jupiter visible? {jupiter.is_bright()}")
print(f"Vesta visible? {asteroid.is_bright()}")
```

```
Jupiter visible? True
Vesta visible? False
```

#### Step 3: Add more attributes and methods

Continue building up functionality:

```
class Observation:
    def __init__(self, target, magnitude, time):
        self.target = target
        self.magnitude = magnitude
        self.time = time  # New attribute
    
    def is_bright(self):
        return self.magnitude < 6.0
    
    def summary(self):
        """Create a summary string."""
        visibility = "visible" if self.is_bright() else "telescopic"
        return f"{self.time}: {self.target} (mag {self.magnitude}, {visibility})"
```

Test the expanded class:

```
obs1 = Observation("Saturn", 0.5, "21:30")
obs2 = Observation("Neptune", 7.8, "22:15")

print(obs1.summary())
print(obs2.summary())
```

```
21:30: Saturn (mag 0.5, visible)
22:15: Neptune (mag 7.8, telescopic)
```

Notice how each method can use `self` to access all the object's data and even call other methods!

### Using help() with Classes

The `help()` function works with our custom classes too:

```
# Get help on the class
# help(Observation)

# Get help on a specific method
# help(Observation.is_bright)

print("help() works with our custom classes and methods!")
```

```
help() works with our custom classes and methods!
```

### Magic Methods: Customizing Object Behavior

Python has magic methods (also called "dunder methods" for "double underscore") that customize how objects work with Python's built-in operations. They always start and end with double underscores.

#### The `__str__` Method - Controlling print()

Without `__str__`, printing an object shows something unhelpful:

```
class StarWithoutStr:
    def __init__(self, name):
        self.name = name

star = StarWithoutStr("Vega")
print(star)  # <__main__.StarWithoutStr object at 0x...>
```

```
<__main__.StarWithoutStr object at 0x109225be0>
```

The `__str__` method defines what `print()` shows. When Python needs to convert your object to a string (like when printing), it calls this method:

```
class Star:
    def __init__(self, name, magnitude):
        self.name = name
        self.magnitude = magnitude
    
    def __str__(self):
        """This method is called when you print the object."""
        return f"{self.name} (magnitude {self.magnitude:.2f})"
```

Now printing is much more useful:

```
vega = Star("Vega", 0.03)
print(vega)  # Vega (magnitude 0.03)

# You can also call str() explicitly
star_string = str(vega)
print(f"String representation: {star_string}")
```

```
Vega (magnitude 0.03)
String representation: Vega (magnitude 0.03)
```

#### The `__len__` Method - Making len() work

The `__len__` method tells Python what to return when someone calls `len()` on your object:

```
class ObservationSession:
    def __init__(self, date):
        self.date = date
        self.targets = []  # List of targets observed
    
    def add_target(self, target):
        """Add a target to the session."""
        self.targets.append(target)
    
    def __len__(self):
        """Return the number of targets when len() is called."""
        return len(self.targets)
    
    def __str__(self):
        return f"Session on {self.date}: {len(self)} targets"
```

Now `len()` works naturally with our objects:

```
session = ObservationSession("2024-03-15")
session.add_target("Jupiter")
session.add_target("Saturn")
session.add_target("M42")

print(session)  # Uses __str__
print(f"Number of targets: {len(session)}")  # Uses __len__
```

```
Session on 2024-03-15: 3 targets
Number of targets: 3
```

Python calls `session.__len__()` when you write `len(session)`.

#### The `__eq__` Method - Defining Equality

By default, Python checks if two variables refer to the exact same object in memory:

```
class StarWithoutEq:
    def __init__(self, name):
        self.name = name

star1 = StarWithoutEq("Vega")
star2 = StarWithoutEq("Vega")

print(star1 == star2)  # False! Different objects in memory
```

```
False
```

Even though both stars have the name "Vega", they're different objects in memory, so Python says they're not equal.

The `__eq__` method lets you define what equality means for your objects:

```
class Star:
    def __init__(self, name, magnitude):
        self.name = name
        self.magnitude = magnitude
    
    def __eq__(self, other):
        """Two stars are equal if they have the same name."""
        return self.name == other.name
    
    def __str__(self):
        return self.name
```

Now equality works the way we want:

```
star1 = Star("Vega", 0.03)
star2 = Star("Vega", 0.03)
star3 = Star("Sirius", -1.46)

print(f"{star1} == {star2}? {star1 == star2}")  # True - same name
print(f"{star1} == {star3}? {star1 == star3}")  # False - different names
```

```
Vega == Vega? True
Vega == Sirius? False
```

#### The `__lt__` Method - Enabling Sorting

The `__lt__` (less than) method tells Python how to compare objects with `<`. Once Python knows how to use `<`, it can automatically figure out sorting:

```
class Star:
    def __init__(self, name, magnitude):
        self.name = name
        self.magnitude = magnitude
    
    def __str__(self):
        return f"{self.name} ({self.magnitude:.1f})"
    
    def __lt__(self, other):
        """For sorting: remember smaller magnitude = brighter!"""
        return self.magnitude < other.magnitude
```

Now we can sort stars by brightness:

```
stars = [
    Star("Sirius", -1.46),
    Star("Betelgeuse", 0.42),
    Star("Vega", 0.03),
    Star("Proxima", 11.13)
]

# Sort uses __lt__ to compare stars
stars.sort()

print("Stars from brightest to faintest:")
for star in stars:
    print(f"  {star}")
```

```
Stars from brightest to faintest:
  Sirius (-1.5)
  Vega (0.0)
  Betelgeuse (0.4)
  Proxima (11.1)
```

Python calls `star1.__lt__(star2)` when it needs to know if `star1 < star2` during sorting.

#### The `__contains__` Method - The `in` Operator

The `__contains__` method lets you use the `in` operator with your objects:

```
class Constellation:
    def __init__(self, name):
        self.name = name
        self.stars = []
    
    def add_star(self, star_name):
        self.stars.append(star_name)
    
    def __contains__(self, star_name):
        """Check if a star is in this constellation."""
        return star_name in self.stars
    
    def __str__(self):
        return f"{self.name} with {len(self.stars)} stars"
```

Now we can use `in` naturally:

```
orion = Constellation("Orion")
orion.add_star("Betelgeuse")
orion.add_star("Rigel")
orion.add_star("Bellatrix")

# Uses __contains__
print("Betelgeuse" in orion)  # True
print("Vega" in orion)  # False

if "Rigel" in orion:
    print("Rigel is in Orion!")
```

```
True
False
Rigel is in Orion!
```

When Python sees `"Rigel" in orion`, it calls `orion.__contains__("Rigel")`.

### Combining Everything: A Practical Example

Let's build a simple but complete class that uses everything we've learned. We'll create a star catalog that can store and search for stars:

```
class StarCatalog:
    """A catalog of stars with search capabilities."""
    
    def __init__(self, name):
        """Initialize an empty catalog."""
        self.name = name
        self.stars = {}  # Dictionary: star name -> magnitude
    
    def add_star(self, name, magnitude):
        """Add a star to the catalog."""
        self.stars[name] = magnitude
        print(f"Added {name} to {self.name}")
    
    def get_magnitude(self, name):
        """Get a star's magnitude."""
        if name in self.stars:
            return self.stars[name]
        else:
            return None
    
    def brightest_star(self):
        """Find the brightest star in the catalog."""
        if len(self.stars) == 0:
            return None
        
        # Find minimum magnitude (remember: smaller = brighter)
        brightest_name = None
        brightest_mag = float('inf')  # Start with infinity
        
        for name, mag in self.stars.items():
            if mag < brightest_mag:
                brightest_mag = mag
                brightest_name = name
        
        return brightest_name, brightest_mag
    
    def visible_stars(self):
        """Return list of stars visible to naked eye (mag < 6)."""
        visible = []
        for name, mag in self.stars.items():
            if mag < 6.0:
                visible.append(name)
        return visible
    
    def __len__(self):
        """Number of stars in catalog."""
        return len(self.stars)
    
    def __contains__(self, star_name):
        """Check if a star is in the catalog."""
        return star_name in self.stars
    
    def __str__(self):
        """String representation."""
        return f"{self.name}: {len(self)} stars"
```

Let's use our catalog class:

```
# Create a catalog
catalog = StarCatalog("Bright Stars")

# Add some stars
catalog.add_star("Sirius", -1.46)
catalog.add_star("Vega", 0.03)
catalog.add_star("Betelgeuse", 0.42)
catalog.add_star("Proxima Centauri", 11.13)

print(f"\n{catalog}")  # Uses __str__
```

```
Added Sirius to Bright Stars
Added Vega to Bright Stars
Added Betelgeuse to Bright Stars
Added Proxima Centauri to Bright Stars

Bright Stars: 4 stars
```

Test searching for stars:

```
# Search using 'in' operator
if "Vega" in catalog:  # Uses __contains__
    mag = catalog.get_magnitude("Vega")
    print(f"Vega magnitude: {mag}")

if "Mars" not in catalog:
    print("Mars is not in the catalog (it's a planet!)")
```

```
Vega magnitude: 0.03
Mars is not in the catalog (it's a planet!)
```

Find the brightest star:

```
# Find brightest
name, mag = catalog.brightest_star()
print(f"Brightest star: {name} at magnitude {mag}")
```

```
Brightest star: Sirius at magnitude -1.46
```

Find all visible stars:

```
# Find visible stars
visible = catalog.visible_stars()
print(f"Visible to naked eye: {visible}")
print(f"That's {len(visible)} out of {len(catalog)} stars")  # Uses __len__
```

```
Visible to naked eye: ['Sirius', 'Vega', 'Betelgeuse']
That's 3 out of 4 stars
```

## Summary

### Key Concepts

In this lecture, you've learned:

* **Functions**: How to package reusable code with parameters and return values, avoiding repetition and making your astronomical calculations more reliable
* **Variable Scope**: How local and global variables work, and why function isolation prevents bugs in complex analysis scripts
* **Modules and Organization**: How to organize functions into separate files for better project management and code reuse across different astronomical analyses
* **Classes and Objects**: How to model astronomical entities (stars, observations, catalogs) as objects that bundle data with related functionality
* **The `self` Concept**: Why every method needs `self` and how it refers to the specific object instance you're working with
* **Magic Methods**: How to customize object behavior with Python's built-in operations like `print()`, `len()`, and sorting

### What You Can Now Do

After working through this material, you should be able to:

* Write functions to encapsulate common astronomical calculations like magnitude conversions and coordinate transformations
* Organize your analysis code into modules that can be imported and reused across different observation sessions
* Create classes to model astronomical objects with appropriate attributes and methods
* Use magic methods to make your custom objects work naturally with Python's built-in functions
* Debug issues related to variable scope and understand error messages about missing `self` parameters

### Practice Suggestions

To solidify these concepts:

1. Create a function library for your most common astronomical calculations (parallax to distance, flux to magnitude, etc.)
2. Build a `Telescope` class with methods for calculating field of view and limiting magnitude
3. Design an `ObservationNight` class that tracks multiple targets and automatically calculates optimal observation times

### Looking Ahead

Next lecture, we'll build on these foundations to explore data visualization with Matplotlib. The concepts you've practiced today—especially functions and classes—will be essential for creating reusable plotting functions and managing complex multi-panel figures. You'll learn to create publication-quality plots of your astronomical data, from simple light curves to sophisticated sky maps.
