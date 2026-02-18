# DataFrames for Astronomical Catalogs

## Introduction

Modern astronomy is drowning in data. While AI can help us write code, it can't decide which stars to study. It doesn't know that high proper motion stars might be nearby, or that stars with extreme radial velocities could be escaping the galaxy. These insights require astronomical intuition - and a tool that lets us quickly explore millions to billions of measurements.

That tool is Pandas.

Think of Pandas as Excel on steroids. It handles billions of rows without breaking a sweat. It merges catalogs in seconds. It filters, sorts, and calculates with simple commands. Most importantly, it lets you think about the astronomy instead of fighting with the code.

Today, we'll work with real data from Gaia - the European Space Agency's revolutionary space telescope that's mapping our galaxy in unprecedented detail. You'll search for candidates of stars that are moving fast, identify nearby red dwarfs for exoplanet searches, and learn to manage observational data like a professional astronomer.

By the end of this lecture, you'll understand why Pandas is essential for daily astronomical operations, and you'll have the skills to handle any astronomical catalog in your research.

## The Problem with Lists

Let's start with a familiar scenario. You observed three bright stars last night and recorded their properties. With just a few stars and properties, Python lists seem manageable:

```
import numpy as np
import matplotlib.pyplot as plt

# Three stars observed last night
star_names = ["Vega", "Arcturus", "Sirius"]
ra_values = [279.234, 213.915, 101.287]  # Right ascension in degrees
dec_values = [38.784, 19.182, -16.716]   # Declination in degrees  
magnitudes = [0.03, -0.05, -1.46]        # Apparent magnitude (brightness)
```

Finding specific information requires careful index tracking. In astronomy, remember that smaller (more negative) magnitudes mean brighter stars:

```
# Find brightest (most negative magnitude)
brightest_index = magnitudes.index(min(magnitudes))
brightest_name = star_names[brightest_index]
brightest_ra = ra_values[brightest_index]
brightest_dec = dec_values[brightest_index]

print(f"Brightest star: {brightest_name}")
print(f"  Position: RA={brightest_ra:.3f}°, Dec={brightest_dec:.3f}°")
print(f"  Magnitude: {magnitudes[brightest_index]}")
```

```
Brightest star: Sirius
  Position: RA=101.287°, Dec=-16.716°
  Magnitude: -1.46
```

Real observations involve many more measurements. As you add data throughout the night, managing separate lists becomes unwieldy.

### Dictionaries Don't Solve It Either

You might think dictionaries could keep each star's data together. Let's try that approach:

```
# One dictionary per star
vega = {
    "ra": 279.234, "dec": 38.784, "magnitude": 0.03,
    "b_mag": 0.00, "v_mag": 0.03, "obs_time": "21:30"
}

arcturus = {
    "ra": 213.915, "dec": 19.182, "magnitude": -0.05,
    "b_mag": 0.86, "v_mag": -0.05, "obs_time": "22:15"
}

sirius = {
    "ra": 101.287, "dec": -16.716, "magnitude": -1.46,
    "b_mag": -1.46, "v_mag": -1.44, "obs_time": "23:45"
}

# Put them in a list
stars = [vega, arcturus, sirius]
```

This keeps each star's data together, but creates new problems. Every simple operation now requires writing a loop:

```
# Finding all bright stars requires a loop
bright_stars = []
for star in stars:
    if star["magnitude"] < 0:
        bright_stars.append(star)

print(f"Found {len(bright_stars)} bright stars")
```

```
Found 2 bright stars
```

```
# Getting all magnitudes requires another loop
magnitudes = [star["magnitude"] for star in stars]
print(f"Average magnitude: {np.mean(magnitudes):.2f}")
```

```
Average magnitude: -0.49
```

With 10,000 stars from Gaia, your code becomes:

* **Slow**: Python loops are not optimized for numerical operations
* **Verbose**: So many for loops clutter your code
* **Error-prone**: Easy to mess up the loop logic

This is exactly the problem Pandas solves. It gives you the organization of keeping related data together, with the computational efficiency of vectorized operations.

## Introducing Pandas

Pandas solves these problems elegantly by providing data structures designed for analysis. Let's import it with the standard abbreviation `pd`:

```
import pandas as pd
print(f"Pandas version: {pd.__version__}")
```

```
Pandas version: 2.2.3
```

### Configuring Pandas Display

Before diving in, let's configure how Pandas displays data. By default, Pandas truncates large DataFrames to keep outputs manageable. These settings control what you see when printing DataFrames - crucial for astronomical work where you need to see many columns and precise numerical values:

```
# Set display options for better visibility
pd.set_option('display.max_rows', 100)      # Show up to 100 rows before truncating
pd.set_option('display.max_columns', 20)    # Show up to 20 columns before truncating
pd.set_option('display.width', 120)         # Wider display for more columns
pd.set_option('display.precision', 3)       # Show 3 decimal places
pd.set_option('display.float_format', '{:.3f}'.format)  # Consistent float formatting
```

You can adjust these based on your screen size and preferences. For now, these settings work well for our 5000-star Gaia sample.

### Understanding Series and DataFrames

Pandas has two fundamental data structures. Let's build them from our star data to see how they work.

**A Series** is a single column of data. If you don't provide an index, Pandas automatically creates a default numeric index starting from 0:

```
# Create a Series with default numeric index
magnitudes_default = pd.Series([0.03, -0.05, -1.46, 0.42])
print("Series with default numeric index:")
print(magnitudes_default)
```

```
Series with default numeric index:
0    0.030
1   -0.050
2   -1.460
3    0.420
dtype: float64
```

However, we can also provide custom labels as an index to make our data more meaningful and easier to work with:

```
# Create a Series of stellar magnitudes
magnitudes = pd.Series(
    data=[0.03, -0.05, -1.46, 0.42],  # The actual values
    index=["Vega", "Arcturus", "Sirius", "Betelgeuse"]  # Labels for each value
)
print("Series with star names as index:")
print(magnitudes)
```

```
Series with star names as index:
Vega          0.030
Arcturus     -0.050
Sirius       -1.460
Betelgeuse    0.420
dtype: float64
```

The `pd.Series()` function creates a one-dimensional labeled array. The `data` parameter contains the values (magnitudes), and the `index` parameter provides labels for each value (star names). The left column in the output shows these index labels, and the right column shows the data values.

Now we can access values using these meaningful labels instead of remembering numeric positions:

```
# Access by label - much more readable than numeric indices
print(f"Vega's magnitude: {magnitudes['Vega']}")
print(f"Sirius's magnitude: {magnitudes['Sirius']}")
```

```
Vega's magnitude: 0.03
Sirius's magnitude: -1.46
```

**A DataFrame** is a table - think of it as multiple Series that share the same index, aligned side-by-side:

```
# Create a DataFrame - multiple columns of related data
star_data = {
    "ra": [279.234, 213.915, 101.287, 88.793],
    "dec": [38.784, 19.182, -16.716, 7.407],
    "magnitude": [0.03, -0.05, -1.46, 0.42],
    "spectral_type": ["A0V", "K1.5III", "A1V", "M2Iab"]
}

stars_df = pd.DataFrame(
    star_data,  # Dictionary where keys become column names
    index=["Vega", "Arcturus", "Sirius", "Betelgeuse"]  # Row labels
)
print("DataFrame with star names as index:")
print(stars_df)
print(f"\nDataFrame shape: {stars_df.shape} (rows, columns)")
```

```
DataFrame with star names as index:
                ra     dec  magnitude spectral_type
Vega       279.234  38.784      0.030           A0V
Arcturus   213.915  19.182     -0.050       K1.5III
Sirius     101.287 -16.716     -1.460           A1V
Betelgeuse  88.793   7.407      0.420         M2Iab

DataFrame shape: (4, 4) (rows, columns)
```

The `pd.DataFrame()` function creates a table. We pass a dictionary where:

* **Keys** ("ra", "dec", etc.) become column names
* **Values** (the lists) become the data in each column
* The `index` parameter gives each row a label (star names)

The `.shape` attribute returns a tuple `(n_rows, n_columns)`. Here we have 4 stars (rows) and 4 measurements (columns).

Now all data for each star travels together - sorting, filtering, or selecting automatically keeps everything aligned. This is the key advantage over separate lists!

## Basic DataFrame Operations

Before we tackle Gaia's stars, let's master the fundamentals with our small 4-star DataFrame. Understanding these operations thoroughly will make the real analysis straightforward.

### Selecting Columns

You can extract one or more columns from a DataFrame using square brackets. The syntax is slightly different for single versus multiple columns:

```
# Single column - returns a Series
mags = stars_df['magnitude']
print("Single column (returns a Series):")
print(mags)
print(f"\nType: {type(mags)}")
```

```
Single column (returns a Series):
Vega          0.030
Arcturus     -0.050
Sirius       -1.460
Betelgeuse    0.420
Name: magnitude, dtype: float64

Type: <class 'pandas.core.series.Series'>
```

Using single brackets with one column name `df['column']` extracts that column as a Series. Notice the output has only one column of values with the index labels on the left - this is a Series, not a DataFrame.

```
# Multiple columns - returns a DataFrame
# Note the double brackets: df[['col1', 'col2']]
positions = stars_df[['ra', 'dec']]
print("\nMultiple columns (returns a DataFrame):")
print(positions)
print(f"\nType: {type(positions)}")
```

```
Multiple columns (returns a DataFrame):
                ra     dec
Vega       279.234  38.784
Arcturus   213.915  19.182
Sirius     101.287 -16.716
Betelgeuse  88.793   7.407

Type: <class 'pandas.core.frame.DataFrame'>
```

Using double brackets `df[['col1', 'col2']]` extracts multiple columns as a new DataFrame. The inner brackets create a list of column names, and the outer brackets perform the selection. This is a common source of confusion for beginners!

Single column selection returns a Series (1-dimensional, like a list with labels), while multiple column selection returns a DataFrame (2-dimensional table).

This distinction matters because Series and DataFrames have different methods available.

### Slicing Rows with .iloc[] and .loc[]

Just like with lists and NumPy arrays, you can slice DataFrames to get specific rows. Pandas provides two methods with an important distinction:

* **`.iloc[]`** - "integer location" - select by row/column position (0, 1, 2, ...)
* **`.loc[]`** - "label location" - select by index label names

Let's see how they work:

#### Position-Based Selection with .iloc[]

The `.iloc[]` indexer works exactly like list slicing - you use numeric positions:

```
# Select by position with .iloc[]
# Syntax: .iloc[start:stop] where stop is EXCLUDED (like list slicing)
first_two = stars_df.iloc[0:2]  # Gets positions 0 and 1 only
print("First two stars using .iloc[0:2]:")
print(first_two)
```

```
First two stars using .iloc[0:2]:
              ra    dec  magnitude spectral_type
Vega     279.234 38.784      0.030           A0V
Arcturus 213.915 19.182     -0.050       K1.5III
```

The `.iloc[0:2]` selects rows at positions 0 and 1 (Vega and Arcturus). Just like list slicing, the stop index (2) is excluded. The syntax follows Python's standard slicing convention `[start:stop]` where `start` is included and `stop` is not.

You can also select a single row by position:

```
# Single row by position - returns a Series
first_star = stars_df.iloc[0]
print("First star (returns a Series):")
print(first_star)
print(f"\nType: {type(first_star)}")
```

```
First star (returns a Series):
ra              279.234
dec              38.784
magnitude         0.030
spectral_type       A0V
Name: Vega, dtype: object

Type: <class 'pandas.core.series.Series'>
```

When you select a single row with `.iloc[0]`, Pandas returns a Series where the column names become the index labels and the row's values become the data. This makes it easy to access individual values: `first_star['magnitude']` would give you 0.03.

#### Label-Based Selection with .loc[]

The `.loc[]` indexer uses the index labels instead of positions. This is more readable when you have meaningful labels:

```
# Select by label with .loc[]
# IMPORTANT: .loc[] is INCLUSIVE on both ends!
vega_to_sirius = stars_df.loc['Vega':'Sirius']  # Gets Vega, Arcturus, AND Sirius
print("Vega to Sirius using .loc['Vega':'Sirius']:")
print(vega_to_sirius)
print("\n⚠️ Notice: .loc[] includes BOTH endpoints!")
```

```
Vega to Sirius using .loc['Vega':'Sirius']:
              ra     dec  magnitude spectral_type
Vega     279.234  38.784      0.030           A0V
Arcturus 213.915  19.182     -0.050       K1.5III
Sirius   101.287 -16.716     -1.460           A1V

⚠️ Notice: .loc[] includes BOTH endpoints!
```

This is a crucial difference that trips up many programmers!

* `.iloc[0:2]` gets positions 0 and 1 (stop=2 excluded)
* `.loc['Vega':'Sirius']` gets Vega, Arcturus, AND Sirius (both endpoints included)

The `.loc[]` slicing is inclusive on both ends, unlike standard Python slicing. This makes sense when using labels - if you ask for "Vega to Sirius", you probably want both stars included!

**⚠️ Confusion Alert:** What if you use `.loc[0:2]` with numeric labels?

Consider a DataFrame with the default integer index (0, 1, 2, ...):

* `.loc[0:2]` would get rows **labeled** 0, 1, AND 2 (three rows, inclusive)
* `.iloc[0:2]` would get **positions** 0 and 1 (two rows, exclusive)

```
# Demonstrating the confusion with numeric labels
# Create a DataFrame with integer index to show the difference
demo_df = pd.DataFrame({
    'value': ['A', 'B', 'C', 'D', 'E']
})

print("DataFrame with integer index:")
print(demo_df)

print("\n.iloc[0:2] - Position-based (exclusive stop):")
print(demo_df.iloc[0:2])  # Gets positions 0, 1 (2 rows)

print("\n.loc[0:2] - Label-based (inclusive stop):")
print(demo_df.loc[0:2])  # Gets labels 0, 1, 2 (3 rows!)

print("\n⚠️ Same syntax [0:2], different results!")
print(f"   .iloc[0:2] returned {len(demo_df.iloc[0:2])} rows")
print(f"   .loc[0:2] returned {len(demo_df.loc[0:2])} rows")
```

```
DataFrame with integer index:
  value
0     A
1     B
2     C
3     D
4     E

.iloc[0:2] - Position-based (exclusive stop):
  value
0     A
1     B

.loc[0:2] - Label-based (inclusive stop):
  value
0     A
1     B
2     C

⚠️ Same syntax [0:2], different results!
   .iloc[0:2] returned 2 rows
   .loc[0:2] returned 3 rows
```

#### Selecting Rows AND Columns Together

Both `.loc[]` and `.iloc[]` can select rows and columns simultaneously using the syntax: `[rows, columns]`

```
# Select specific rows AND columns with .loc[]
# Syntax: .loc[row_selection, column_selection]
subset = stars_df.loc['Vega':'Sirius', ['ra', 'magnitude']]
print("Subset of rows and columns:")
print(subset)
```

```
Subset of rows and columns:
              ra  magnitude
Vega     279.234      0.030
Arcturus 213.915     -0.050
Sirius   101.287     -1.460
```

The comma separates row selection from column selection: `.loc[rows, columns]`. Here we select rows from Vega to Sirius (inclusive) and only the 'ra' and 'magnitude' columns. This gives us a smaller DataFrame with just the data we need.

### A Note on Views and Copies

From your earlier lectures on lists and NumPy arrays, you learned about views (windows into existing data) versus copies (independent duplicates). With lists, slicing always created copies. With NumPy, simple slicing created views (efficient, shares memory) while fancy indexing created copies.

With Pandas, the situation is more complex. The behavior depends on many factors including the DataFrame's internal structure, the type of selection you're making, and sometimes even the Pandas version.

Because this is so complicated and can change, we recommend two clear practices:

1. **For independent work:** Always use `.copy()` explicitly
2. **To modify the original:** Use `.loc[]` or `.iloc[]` directly

Let's see both approaches in action:

```
# Safe practice: Explicit .copy() when you want independence
# Filter for bright stars and make an explicit copy
bright_only = stars_df[stars_df['magnitude'] < 0].copy()
# Now we can safely add columns to bright_only
bright_only['very_bright'] = True  

print("Modified copy:")
print(bright_only)
print("\nOriginal DataFrame unchanged:")
print(stars_df)
```

```
Modified copy:
              ra     dec  magnitude spectral_type  very_bright
Arcturus 213.915  19.182     -0.050       K1.5III         True
Sirius   101.287 -16.716     -1.460           A1V         True

Original DataFrame unchanged:
                ra     dec  magnitude spectral_type
Vega       279.234  38.784      0.030           A0V
Arcturus   213.915  19.182     -0.050       K1.5III
Sirius     101.287 -16.716     -1.460           A1V
Betelgeuse  88.793   7.407      0.420         M2Iab
```

The code above:

1. Filters `stars_df` for stars with magnitude < 0 (bright stars)
2. Calls `.copy()` to create an independent DataFrame
3. Adds a new column to the copy
4. The original `stars_df` remains unchanged

The `.copy()` method creates a completely independent duplicate in new memory. Changes to `bright_only` won't affect `stars_df`.

```
# Safe practice: Use .loc[] to modify the original DataFrame directly
# This unambiguously modifies stars_df itself
stars_df.loc[stars_df['magnitude'] < 0, 'is_bright'] = True
stars_df.loc[stars_df['magnitude'] >= 0, 'is_bright'] = False

print("Original DataFrame now modified:")
print(stars_df)
```

```
Original DataFrame now modified:
                ra     dec  magnitude spectral_type is_bright
Vega       279.234  38.784      0.030           A0V     False
Arcturus   213.915  19.182     -0.050       K1.5III      True
Sirius     101.287 -16.716     -1.460           A1V      True
Betelgeuse  88.793   7.407      0.420         M2Iab     False
```

Using `.loc[]` with a boolean condition and column name tells Pandas exactly what to modify. The syntax `.loc[condition, 'column']` means "in the original DataFrame, for rows where condition is True, set this column's value." This explicitly modifies the original DataFrame with no ambiguity about views versus copies.

Throughout this lecture, we'll continue to use these safe practices and point out important cases where you need to be careful About views and copies versus views.

### Boolean Indexing (Filtering)

One of Pandas' most powerful features is filtering rows using boolean (True/False) conditions. This is how you find stars matching specific criteria.

```
# Create a boolean mask
is_bright = stars_df['magnitude'] < 0
print("Boolean mask (True/False for each star):")
print(is_bright)
print(f"\nType: {type(is_bright)}")
```

```
Boolean mask (True/False for each star):
Vega          False
Arcturus       True
Sirius         True
Betelgeuse    False
Name: magnitude, dtype: bool

Type: <class 'pandas.core.series.Series'>
```

The comparison `stars_df['magnitude'] < 0` creates a boolean Series - one True/False value for each row. This is called a "mask" because True values "let through" rows while False values block them.

**About views and copies:** The boolean Series created by the comparison is a **new object** (a copy), not a view of the original data. This means you can safely use it for filtering without worrying about modifying the original DataFrame.

```
# Apply the mask to filter the DataFrame
bright_stars = stars_df[is_bright]
print("Bright stars (magnitude < 0):")
print(bright_stars)
```

```
Bright stars (magnitude < 0):
              ra     dec  magnitude spectral_type is_bright
Arcturus 213.915  19.182     -0.050       K1.5III      True
Sirius   101.287 -16.716     -1.460           A1V      True
```

Placing the boolean mask inside square brackets `stars_df[is_bright]` filters the DataFrame. Only rows where the mask is True appear in the result. This gives us just Arcturus and Sirius - the bright stars.

We can combine the two steps into one line:

```
# Combined: create mask and filter in one step
bright_stars = stars_df[stars_df['magnitude'] < 0]
print("Same result in one line:")
print(bright_stars)
```

```
Same result in one line:
              ra     dec  magnitude spectral_type is_bright
Arcturus 213.915  19.182     -0.050       K1.5III      True
Sirius   101.287 -16.716     -1.460           A1V      True
```

**About views and copies:** Boolean indexing like `stars_df[stars_df['magnitude'] < 0]` creates a **copy** of the data, not a view. This means you can safely modify the filtered DataFrame without affecting the original. However, if you want to modify the original DataFrame based on a condition, you should use `.loc[]` with the boolean mask directly on the original DataFrame.

#### Combining Multiple Conditions

You can combine conditions using logical operators. However, you **must use parentheses** around each condition:

* `&` means AND (both conditions must be True)
* `|` means OR (at least one condition must be True)
* `~` means NOT (inverts True/False)

```
# Combine conditions - parentheses are REQUIRED
# Find stars that are bright AND in northern hemisphere
bright_and_northern = stars_df[(stars_df['magnitude'] < 0) & (stars_df['dec'] > 0)]
print("Bright stars in northern hemisphere (dec > 0):")
print(bright_and_northern)
```

```
Bright stars in northern hemisphere (dec > 0):
              ra    dec  magnitude spectral_type is_bright
Arcturus 213.915 19.182     -0.050       K1.5III      True
```

### Adding New Columns

You can add calculated columns to a DataFrame using simple assignment. The calculations apply to all rows simultaneously (vectorized operations - fast!):

```
# Add a new column with calculations
# This is a simplified example - real absolute magnitude calculation is more complex
stars_df['abs_magnitude_simple'] = stars_df['magnitude'] - 5
print("DataFrame with new column:")
print(stars_df)
```

```
DataFrame with new column:
                ra     dec  magnitude spectral_type is_bright  abs_magnitude_simple
Vega       279.234  38.784      0.030           A0V     False                -4.970
Arcturus   213.915  19.182     -0.050       K1.5III      True                -5.050
Sirius     101.287 -16.716     -1.460           A1V      True                -6.460
Betelgeuse  88.793   7.407      0.420         M2Iab     False                -4.580
```

The syntax `df['new_column'] = calculation` creates a new column. Here, `stars_df['magnitude'] - 5` subtracts 5 from every row's magnitude value simultaneously. This vectorized operation is much faster than looping through rows.

**Important:** When you assign to a new column like this (`stars_df['new_column'] = ...`), you're modifying the original DataFrame directly - no copy is created. The calculation on the right side (`stars_df['magnitude'] - 5`) creates a temporary Series, but the assignment adds the column to the existing DataFrame in place. The new column `abs_magnitude_simple` now appears in our DataFrame, aligned with all other columns.

## Loading Real Astronomical Data

Now that you understand the basics with our 4-star example, let's apply everything to real astronomical data from the Gaia mission. This is where Pandas truly shines - handling thousands of measurements effortlessly.

### The Gaia Mission

Gaia is a space telescope launched by the European Space Agency in 2013, currently orbiting at the L2 Lagrange point, about 1.5 million kilometers from Earth. Its mission: create the most detailed 3D map of our Milky Way galaxy ever made.

Gaia measures:

* **Positions**: Where stars are on the sky, with microarcsecond precision (that's a millionth of a millionth of a degree!)
* **Parallaxes**: The apparent shift in star positions as Earth orbits the Sun - this gives us distances
* **Proper Motions**: How fast stars move across the sky, in milliarcseconds per year
* **Radial Velocities**: How fast stars move toward or away from us, in kilometers per second
* **Photometry**: Brightness in multiple filters (G-band, blue, and red passbands)

The Gaia mission has measured nearly 2 billion stars - about 1% of all stars in our galaxy! The data releases have revolutionized our understanding of the Milky Way's structure, stellar evolution, and even helped discover new star clusters and streams.

Today we'll work with a manageable sample: 5000 nearby stars with high-quality measurements from Data Release 3 (DR3, published in 2022).

```
# Load Gaia DR3 data
# pd.read_csv() reads a CSV (Comma-Separated Values) file
gaia = pd.read_csv('data_gaia_dr3.csv')

print(f"Loaded {len(gaia)} stars from Gaia catalog")
print(f"DataFrame shape: {gaia.shape} (rows, columns)")
```

```
Loaded 5000 stars from Gaia catalog
DataFrame shape: (5000, 15) (rows, columns)
```

### Setting Source ID as Index

Each Gaia star has a unique `source_id` - a 64-bit integer identifier. We could use this as our DataFrame index instead of the default 0, 1, 2, ... numeric index. This would let us select stars directly by their Gaia ID. There are two ways to do this:

**Option 1: Set index when reading the file**

```
# Read CSV and immediately set source_id as index
gaia_indexed = pd.read_csv('data_gaia_dr3.csv', index_col='source_id')
print("DataFrame with source_id as index:")
print(gaia_indexed.head(3))
```

```
DataFrame with source_id as index:
                         ra     dec  parallax  parallax_error    pmra  pmra_error   pmdec  pmdec_error  \
source_id                                                                                                
3075955904089799552 132.105   2.271    12.599           0.018   4.014       0.019  66.102        0.015   
5927744094804268288 251.098 -56.960    11.304           0.013 -35.372       0.014 -99.374        0.011   
2845253659931962368 346.967  26.856    11.486           0.022 -36.025       0.025  17.657        0.018   

                     radial_velocity  radial_velocity_error  phot_g_mean_mag  phot_bp_mean_mag  phot_rp_mean_mag  ruwe  
source_id                                                                                                               
3075955904089799552           35.984                  0.303           11.123            11.695            10.409 0.973  
5927744094804268288            6.397                  1.140           12.686            13.585            11.754 0.937  
2845253659931962368           11.243                  2.568           14.446            15.624            13.370 1.047
```

The `index_col='source_id'` parameter tells Pandas to use the source\_id column as the index instead of creating a default numeric index.

**Option 2: Set index after loading**

```
# Load normally, then set index
gaia_temp = pd.read_csv('data_gaia_dr3.csv')
gaia_temp = gaia_temp.set_index('source_id')
print("\nDataFrame after setting index:")
print(gaia_temp.head(3))
```

```
DataFrame after setting index:
                         ra     dec  parallax  parallax_error    pmra  pmra_error   pmdec  pmdec_error  \
source_id                                                                                                
3075955904089799552 132.105   2.271    12.599           0.018   4.014       0.019  66.102        0.015   
5927744094804268288 251.098 -56.960    11.304           0.013 -35.372       0.014 -99.374        0.011   
2845253659931962368 346.967  26.856    11.486           0.022 -36.025       0.025  17.657        0.018   

                     radial_velocity  radial_velocity_error  phot_g_mean_mag  phot_bp_mean_mag  phot_rp_mean_mag  ruwe  
source_id                                                                                                               
3075955904089799552           35.984                  0.303           11.123            11.695            10.409 0.973  
5927744094804268288            6.397                  1.140           12.686            13.585            11.754 0.937  
2845253659931962368           11.243                  2.568           14.446            15.624            13.370 1.047
```

The `.set_index('column')` method returns a new DataFrame with the specified column as the index.

However, for this tutorial we'll stick with the default numeric index (0, 1, 2, ...) because source IDs are very long numbers (like 4295806720) that aren't human-readable, the numeric index is simpler for learning, and you can always access source\_id as a regular column when needed.

If you ever want to reset back to a numeric index:

```
# Reset index back to default numeric (0, 1, 2, ...)
gaia_reset = gaia_indexed.reset_index()
print("\nDataFrame with numeric index restored:")
print(gaia_reset.head(3))
print("\nNotice: source_id is now a regular column again")
```

```
DataFrame with numeric index restored:
             source_id      ra     dec  parallax  parallax_error    pmra  pmra_error   pmdec  pmdec_error  \
0  3075955904089799552 132.105   2.271    12.599           0.018   4.014       0.019  66.102        0.015   
1  5927744094804268288 251.098 -56.960    11.304           0.013 -35.372       0.014 -99.374        0.011   
2  2845253659931962368 346.967  26.856    11.486           0.022 -36.025       0.025  17.657        0.018   

   radial_velocity  radial_velocity_error  phot_g_mean_mag  phot_bp_mean_mag  phot_rp_mean_mag  ruwe  
0           35.984                  0.303           11.123            11.695            10.409 0.973  
1            6.397                  1.140           12.686            13.585            11.754 0.937  
2           11.243                  2.568           14.446            15.624            13.370 1.047  

Notice: source_id is now a regular column again
```

The `.reset_index()` method moves the current index back to a regular column and creates a new default numeric index. The `drop=True` parameter (not shown) would discard the old index instead of keeping it as a column.

For the rest of this lecture, we'll use `gaia` with its default numeric index.

The `pd.read_csv()` function reads data from a CSV file and creates a DataFrame. CSV files are common in astronomy - they're plain text files where each row represents one object and commas separate the different measurements.

The `len(gaia)` gives us the number of rows (stars), and `gaia.shape` returns `(n_rows, n_columns)`. Our sample has 5000 stars with 17 different measurements each.

### First Look at the Data

Always start by examining your data structure. The `.head()` method shows the first few rows:

```
# Look at first few rows
# .head(n) shows the first n rows (default is 5)
gaia.head(3)
```

.dataframe tbody tr th:only-of-type {
vertical-align: middle;
}
.dataframe tbody tr th {
vertical-align: top;
}
.dataframe thead th {
text-align: right;
}

|  | source\_id | ra | dec | parallax | parallax\_error | pmra | pmra\_error | pmdec | pmdec\_error | radial\_velocity | radial\_velocity\_error | phot\_g\_mean\_mag | phot\_bp\_mean\_mag | phot\_rp\_mean\_mag | ruwe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 3075955904089799552 | 132.105 | 2.271 | 12.599 | 0.018 | 4.014 | 0.019 | 66.102 | 0.015 | 35.984 | 0.303 | 11.123 | 11.695 | 10.409 | 0.973 |
| 1 | 5927744094804268288 | 251.098 | -56.960 | 11.304 | 0.013 | -35.372 | 0.014 | -99.374 | 0.011 | 6.397 | 1.140 | 12.686 | 13.585 | 11.754 | 0.937 |
| 2 | 2845253659931962368 | 346.967 | 26.856 | 11.486 | 0.022 | -36.025 | 0.025 | 17.657 | 0.018 | 11.243 | 2.568 | 14.446 | 15.624 | 13.370 | 1.047 |

The `.head(3)` method displays the first 3 rows of our DataFrame.

```
# The .tail() method shows the last few rows
# Useful for checking if the file loaded completely
gaia.tail(3)
```

.dataframe tbody tr th:only-of-type {
vertical-align: middle;
}
.dataframe tbody tr th {
vertical-align: top;
}
.dataframe thead th {
text-align: right;
}

|  | source\_id | ra | dec | parallax | parallax\_error | pmra | pmra\_error | pmdec | pmdec\_error | radial\_velocity | radial\_velocity\_error | phot\_g\_mean\_mag | phot\_bp\_mean\_mag | phot\_rp\_mean\_mag | ruwe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4997 | 6018556569741729408 | 247.513 | -37.917 | 14.257 | 0.016 | -136.447 | 0.019 | 2.268 | 0.015 | -37.688 | 3.371 | 13.128 | 14.105 | 12.147 | 1.035 |
| 4998 | 654467017782614784 | 119.256 | 14.284 | 14.288 | 0.022 | -8.641 | 0.019 | -62.411 | 0.014 | 19.389 | 0.239 | 10.845 | 11.416 | 10.130 | 0.956 |
| 4999 | 5196092086568670080 | 129.588 | -81.810 | 17.387 | 0.020 | 93.620 | 0.026 | 626.163 | 0.024 | 88.946 | 5.532 | 14.934 | 16.268 | 13.798 | 1.050 |

The `.tail(3)` method shows the last 3 rows.

```
# List all column names
print("Gaia data columns:")
for i, col in enumerate(gaia.columns, 1):
    print(f"{i:2d}. {col}")
```

```
Gaia data columns:
 1. source_id
 2. ra
 3. dec
 4. parallax
 5. parallax_error
 6. pmra
 7. pmra_error
 8. pmdec
 9. pmdec_error
10. radial_velocity
11. radial_velocity_error
12. phot_g_mean_mag
13. phot_bp_mean_mag
14. phot_rp_mean_mag
15. ruwe
```

The `gaia.columns` attribute contains all column names.

Let's understand these key columns:

**Identification:**

* `source_id`: Unique identifier - a 64-bit integer encoding sky position and detection details

**Position:**

* `ra`: Right Ascension in degrees (0-360°) - like celestial longitude
* `dec`: Declination in degrees (-90° to +90°) - like celestial latitude
* `parallax`: Annual position shift in milliarcseconds as Earth orbits - inversely related to distance!

**Motion:**

* `pmra`: Proper motion in RA (milliarcseconds/year) - sky motion in the RA direction
* `pmdec`: Proper motion in Dec (milliarcseconds/year) - sky motion in the Dec direction
* `radial_velocity`: Motion toward/away from us (km/s) - positive means receding, negative approaching

**Brightness:**

* `phot_g_mean_mag`: G-band magnitude (Gaia's broad optical filter, similar to visual magnitude)
* `phot_bp_mean_mag`: Blue passband magnitude (bluer/shorter wavelengths)
* `phot_rp_mean_mag`: Red passband magnitude (redder/longer wavelengths)

**Quality:**

* `ruwe`: Renormalized Unit Weight Error - quality indicator where ~1.0 is good, >1.4 suggests potential problems
* Error columns (`*_error`): Measurement uncertainties for various quantities

```
# Get comprehensive overview of the dataset
# .info() shows column names, types, non-null counts, and memory usage
gaia.info()
```

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 5000 entries, 0 to 4999
Data columns (total 15 columns):
 #   Column                 Non-Null Count  Dtype  
---  ------                 --------------  -----  
 0   source_id              5000 non-null   int64  
 1   ra                     5000 non-null   float64
 2   dec                    5000 non-null   float64
 3   parallax               5000 non-null   float64
 4   parallax_error         5000 non-null   float64
 5   pmra                   5000 non-null   float64
 6   pmra_error             5000 non-null   float64
 7   pmdec                  5000 non-null   float64
 8   pmdec_error            5000 non-null   float64
 9   radial_velocity        5000 non-null   float64
 10  radial_velocity_error  5000 non-null   float64
 11  phot_g_mean_mag        5000 non-null   float64
 12  phot_bp_mean_mag       4960 non-null   float64
 13  phot_rp_mean_mag       4960 non-null   float64
 14  ruwe                   5000 non-null   float64
dtypes: float64(14), int64(1)
memory usage: 586.1 KB
```

The `.info()` method provides a comprehensive summary.

### Visualizing Our Sample on the Sky

Before diving into analysis, let's visualize where our stars are located. A Mollweide projection shows the entire celestial sphere in an ellipse, preserving area relationships:

```
# Create all-sky map using Mollweide projection
fig = plt.figure(figsize=(12, 6))
ax = plt.subplot(111, projection='mollweide')

# Convert RA to radians and shift to [-pi, pi] range
# Mollweide projection expects longitude from -π to π
ra_rad = np.radians(gaia['ra'] - 180)
dec_rad = np.radians(gaia['dec'])

# Plot with color representing magnitude (brightness)
scatter = ax.scatter(ra_rad, dec_rad, 
                    c=gaia['phot_g_mean_mag'],  # Color by magnitude
                    s=1,                          # Small point size
                    cmap='viridis_r',            # Reversed viridis colormap
                    vmin=0, vmax=15)             # Magnitude range

ax.set_xlabel('Right Ascension')
ax.set_ylabel('Declination')
ax.grid(True, alpha=0.3)
plt.colorbar(scatter, label='G Magnitude (smaller = brighter)')
plt.title('Our Gaia Sample: 5000 Nearby Stars')
plt.tight_layout()
plt.show()
```

The plot shows our stars are distributed across the entire sky, because Gaia is a space satellite surveying the entire sky.

### Understanding Data Types

Different columns have different data types, which affects what operations you can perform and how much memory they use:

```
# Check data types for each column
# The .dtypes attribute shows the type of each column
print("Data types in Gaia DataFrame:")
print(gaia.dtypes)
```

```
Data types in Gaia DataFrame:
source_id                  int64
ra                       float64
dec                      float64
parallax                 float64
parallax_error           float64
pmra                     float64
pmra_error               float64
pmdec                    float64
pmdec_error              float64
radial_velocity          float64
radial_velocity_error    float64
phot_g_mean_mag          float64
phot_bp_mean_mag         float64
phot_rp_mean_mag         float64
ruwe                     float64
dtype: object
```

#### Converting Data Types with .astype()

Sometimes you need to convert between types. The `.astype()` method handles this:

```
# Example: Convert source_id to string for display or categorization
# .astype(type) converts the Series to a new type
source_id_str = gaia['source_id'].astype(str)

print(f"Original type: {gaia['source_id'].dtype}")
print(f"Converted type: {source_id_str.dtype}")
print(f"\nFirst value as string: '{source_id_str.iloc[0]}'")
print(f"First value as integer: {gaia['source_id'].iloc[0]}")
```

```
Original type: int64
Converted type: object

First value as string: '3075955904089799552'
First value as integer: 3075955904089799552
```

The `.astype(str)` method converts each integer source ID to a string.

Note that `.astype()` returns a **copy** (a new Series) with converted values - it doesn't modify the original `gaia['source_id']` column unless you explicitly reassign it.

```
# Statistical summary of all numeric columns
# .describe() calculates count, mean, std, min, quartiles, max
gaia.describe()
```

.dataframe tbody tr th:only-of-type {
vertical-align: middle;
}
.dataframe tbody tr th {
vertical-align: top;
}
.dataframe thead th {
text-align: right;
}

|  | source\_id | ra | dec | parallax | parallax\_error | pmra | pmra\_error | pmdec | pmdec\_error | radial\_velocity | radial\_velocity\_error | phot\_g\_mean\_mag | phot\_bp\_mean\_mag | phot\_rp\_mean\_mag | ruwe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| count | 5000.000 | 5000.000 | 5000.000 | 5000.000 | 5000.000 | 5000.000 | 5000.000 | 5000.000 | 5000.000 | 5000.000 | 5000.000 | 5000.000 | 4960.000 | 4960.000 | 5000.000 |
| mean | 3507186880638553600.000 | 182.755 | -0.670 | 16.042 | 0.021 | -0.954 | 0.021 | -41.248 | 0.019 | 1.198 | 1.824 | 12.237 | 13.194 | 11.300 | 1.090 |
| std | 1994877187678150400.000 | 105.238 | 39.376 | 8.385 | 0.012 | 121.648 | 0.014 | 111.911 | 0.012 | 34.174 | 3.006 | 2.352 | 2.771 | 2.102 | 0.120 |
| min | 2058736739430272.000 | 0.033 | -88.527 | 10.000 | 0.008 | -874.382 | 0.006 | -1279.562 | 0.008 | -347.181 | 0.113 | 4.154 | 4.347 | 3.713 | 0.616 |
| 25% | 1840827067582235136.000 | 91.269 | -31.209 | 11.381 | 0.015 | -55.329 | 0.015 | -84.488 | 0.014 | -18.214 | 0.268 | 10.566 | 11.082 | 9.869 | 1.014 |
| 50% | 3441117304952764928.000 | 184.508 | -0.642 | 13.364 | 0.018 | -1.181 | 0.019 | -29.229 | 0.017 | 0.891 | 0.951 | 12.969 | 14.042 | 11.919 | 1.087 |
| 75% | 5263322042876719104.000 | 276.676 | 29.478 | 17.265 | 0.023 | 54.551 | 0.024 | 13.351 | 0.021 | 19.492 | 2.465 | 14.195 | 15.540 | 13.036 | 1.161 |
| max | 6917476324098466816.000 | 359.985 | 88.702 | 107.802 | 0.244 | 1254.687 | 0.308 | 897.030 | 0.255 | 345.388 | 39.210 | 15.000 | 17.302 | 13.926 | 1.400 |

The `.describe()` method provides quick statistics for each numeric column. This gives you an instant feel for your data's range and distribution.

### Categorizing Continuous Data with pd.cut()

Sometimes we want to bin continuous measurements into discrete categories. For example, let's categorize stars by their observability - can you see them with your naked eye, binoculars, or do you need a telescope?

The `pd.cut()` function divides a continuous variable into bins:

```
# Bin magnitudes into observability categories
# pd.cut() divides continuous data into discrete bins
gaia['brightness_category'] = pd.cut(
    gaia['phot_g_mean_mag'],  # The column to bin
    bins=[0, 6, 10, 15, 20],  # Bin edges: 0-6, 6-10, 10-15, 15-20
    labels=['Naked eye', 'Binocular', 'Small telescope', 'Large telescope']
)

print("First 10 stars with their brightness categories:")
print(gaia[['phot_g_mean_mag', 'brightness_category']].head(10))
```

```
First 10 stars with their brightness categories:
```

```
   phot_g_mean_mag brightness_category
0           11.123     Small telescope
1           12.686     Small telescope
2           14.446     Small telescope
3           14.480     Small telescope
4           14.491     Small telescope
5           13.889     Small telescope
6           13.549     Small telescope
7           12.368     Small telescope
8           10.958     Small telescope
9            6.351           Binocular
```

The `pd.cut()` function works like this:

1. **Takes continuous data**: `gaia['phot_g_mean_mag']` contains decimal magnitude values
2. **Divides into bins**: The `bins=[0, 6, 10, 15, 20]` parameter creates 4 bins:
   * Bin 1: 0 to 6 (naked eye visible)
   * Bin 2: 6 to 10 (binoculars needed)
   * Bin 3: 10 to 15 (small telescope)
   * Bin 4: 15 to 20 (large telescope)
3. **Assigns labels**: The `labels` parameter gives each bin a descriptive name
4. **Creates categorical column**: Returns a categorical Series with these labels

### Counting Categories with .value\_counts()

Now that we've created categories, let's count how many stars fall in each one using the `.value_counts()` method:

```
# Count occurrences of each category
# .value_counts() returns counts of unique values, sorted by frequency
category_counts = gaia['brightness_category'].value_counts()
print("Observability distribution:")
print(category_counts)
print(f"\nTotal: {category_counts.sum()} stars")
```

```
Observability distribution:
brightness_category
Small telescope    4009
Binocular           934
Naked eye            57
Large telescope       0
Name: count, dtype: int64

Total: 5000 stars
```

The `.value_counts()` method counts how many times each unique value appears in a Series. It returns a new Series with unique values as the index and counts as the data. By default, results are sorted by frequency (most common first), making it easy to identify the dominant categories in your data.

```
# Get proportions instead of raw counts
# normalize=True converts counts to fractions (sum to 1.0)
category_props = gaia['brightness_category'].value_counts(normalize=True)
print("As percentages:")
for category, prop in category_props.items():
    print(f"  {category}: {prop*100:.1f}%")
```

```
As percentages:
  Small telescope: 80.2%
  Binocular: 18.7%
  Naked eye: 1.1%
  Large telescope: 0.0%
```

Adding `normalize=True` to `.value_counts()` converts raw counts to proportions (fractions that sum to 1.0). We multiply by 100 to display as percentages. This is useful for comparing distributions across different-sized datasets.

### Random Sampling with .sample()

When working with large catalogs, random samples help you quickly explore data quality without processing everything. The `.sample()` method provides this capability:

```
# Get a random sample of stars
# .sample(n=5) returns 5 randomly selected rows
# random_state=42 ensures reproducibility (same "random" sample each time)
random_sample = gaia.sample(n=5, random_state=42)
print("Random sample of 5 stars:")
print(random_sample[['ra', 'dec', 'phot_g_mean_mag', 'parallax']])
```

```
Random sample of 5 stars:
          ra     dec  phot_g_mean_mag  parallax
1501 241.755  -1.624           14.650    10.652
2586 231.924 -67.117           12.580    11.851
2653  56.614 -29.338            5.894    10.192
1055 212.968   4.389           14.595    12.923
705  117.078  51.831           11.963    11.252
```

The `.sample()` method randomly selects rows from your DataFrame:

* **`n=5`** parameter: Return 5 random rows
* **`random_state=42`** parameter: Seeds the random number generator

Random sampling is useful for:

* Quick data quality checks across your entire dataset
* Prototyping analysis code on a small subset before running on full data
* Creating training/test splits for machine learning

```
# Sample a fraction of the data
# frac=0.1 returns 10% of rows (500 stars)
ten_percent = gaia.sample(frac=0.1, random_state=42)
print(f"10% sample contains {len(ten_percent)} stars")
print(f"Mean magnitude in sample: {ten_percent['phot_g_mean_mag'].mean():.2f}")
print(f"Mean magnitude in full data: {gaia['phot_g_mean_mag'].mean():.2f}")
```

```
10% sample contains 500 stars
Mean magnitude in sample: 12.16
Mean magnitude in full data: 12.24
```

Instead of specifying an exact number of rows with `n`, you can use `frac` to sample a fraction.

## Selecting and Filtering Gaia Data

Now let's apply our selection and filtering skills to find interesting stars in the Gaia catalog. This is where you'll spend most of your time in real research - finding objects that meet specific scientific criteria.

### Selecting Specific Columns

With 17 columns, we often want to focus on just a few relevant measurements:

```
# Select just positions and magnitudes
sky_positions = gaia[['ra', 'dec', 'phot_g_mean_mag']]
print("First 5 star positions:")
print(sky_positions.head())
```

```
First 5 star positions:
       ra     dec  phot_g_mean_mag
0 132.105   2.271           11.123
1 251.098 -56.960           12.686
2 346.967  26.856           14.446
3 117.376 -12.201           14.480
4 159.829  15.979           14.491
```

**About views and copies:** When you select columns like this, Pandas may return a view or a copy depending on internal details. Since we're just displaying data here, it doesn't matter. But if you plan to modify `sky_positions`, call `.copy()` explicitly to ensure independence from `gaia`.

### Finding Bright Stars

Let's find all bright stars (magnitude < 10) in our sample using boolean indexing:

```
# Filter for bright stars
# Boolean indexing creates a new DataFrame
bright_stars = gaia[gaia['phot_g_mean_mag'] < 10].copy()

print(f"Found {len(bright_stars)} bright stars out of {len(gaia)} total")
print(f"That's {100 * len(bright_stars) / len(gaia):.1f}% of our sample")
```

```
Found 991 bright stars out of 5000 total
That's 19.8% of our sample
```

**About views and copies:** Boolean indexing always creates a new DataFrame (selecting non-contiguous rows requires creating new data). The explicit `.copy()` here is technically redundant but makes our intent crystal clear - we want an independent DataFrame. This is a good habit for code clarity.

### Combining Multiple Conditions

Find nearby (high parallax) AND bright stars by combining conditions:

```
# Find stars that are BOTH nearby AND bright
# High parallax = nearby (parallax measured in milliarcseconds)
# Remember: MUST use parentheses around each condition
nearby_bright = gaia[(gaia['parallax'] > 20) & (gaia['phot_g_mean_mag'] < 8)].copy()

print(f"Nearby AND bright stars: {len(nearby_bright)}")
if len(nearby_bright) > 0:
    print("\nFirst 5 examples:")
    print(nearby_bright[['parallax', 'phot_g_mean_mag']].head())
```

```
Nearby AND bright stars: 84

First 5 examples:
     parallax  phot_g_mean_mag
9      37.895            6.351
19     75.569            6.919
88     44.825            6.073
91     30.081            7.431
166    27.392            7.768
```

The `&` operator performs element-wise AND on two boolean Series.

**About views and copies:** Again, boolean indexing creates a new DataFrame, and we explicitly `.copy()` for clarity and safety.

### The .query() Method for Readable Filtering

For complex conditions, the `.query()` method offers cleaner syntax. It lets you write conditions as strings (like SQL):

```
# Same filter using .query() - more readable!
# Write the condition as a string
nearby_bright_query = gaia.query('parallax > 20 & phot_g_mean_mag < 8').copy()

print(f"Using .query(): Found {len(nearby_bright_query)} stars")
print("Advantages: No need for parentheses, no repeated DataFrame name, cleaner syntax!")
```

```
Using .query(): Found 84 stars
Advantages: No need for parentheses, no repeated DataFrame name, cleaner syntax!
```

The `.query()` method:

* Takes a string containing the condition
* Column names used directly (no `gaia['column']` needed)
* Use `&` for AND, `|` for OR, `~` for NOT (same operators, no parentheses needed)
* More readable for complex multi-condition filters
* Can reference Python variables with `@variable` syntax

Compare:

```
# Boolean indexing - verbose
df[(df['col1'] > 10) & (df['col2'] < 5) & (df['col3'] == 'value')]

# .query() - cleaner
df.query('col1 > 10 & col2 < 5 & col3 == "value"')
```

**About views and copies:** The `.query()` method also returns a new DataFrame (filtered rows), so our explicit `.copy()` is technically redundant but reinforces our intent.

### Membership Testing with .isin()

Sometimes you need to check if values are in a specific list. This is common when cross-matching catalogs or selecting specific objects of interest:

```
# Select specific stars by their source IDs
# Let's pick a few interesting stars from our sample
interesting_ids = [
    gaia['source_id'].iloc[0],
    gaia['source_id'].iloc[10], 
    gaia['source_id'].iloc[100]
]

# Find these specific stars using .isin()
selected_stars = gaia[gaia['source_id'].isin(interesting_ids)].copy()
print(f"Found {len(selected_stars)} of our {len(interesting_ids)} target stars")
print("\nSelected stars:")
print(selected_stars[['source_id', 'ra', 'dec', 'phot_g_mean_mag']])
```

```
Found 3 of our 3 target stars

Selected stars:
               source_id      ra     dec  phot_g_mean_mag
0    3075955904089799552 132.105   2.271           11.123
10   4669477522111051904  56.543 -66.564           12.932
100   486137834885588480  84.715  70.767           14.322
```

**About views and copies:** As with all boolean indexing, `.isin()` creates a boolean mask, and applying it creates a new DataFrame. We `.copy()` for explicit independence.

## Transforming Gaia Data

Raw Gaia measurements are useful, but we often need derived quantities. Let's calculate physically meaningful values like distances, absolute magnitudes, and colors.

### Adding Distance Column

Parallax gives us distance through a simple relationship:

**distance (parsecs) = 1000 / parallax (milliarcseconds)**

This comes from the definition of parallax: at 1 parsec distance, a star shows 1 arcsecond of parallax as Earth orbits the Sun.

```
# Calculate distance in parsecs from parallax
# Vectorized operation applies to all 5000 stars simultaneously
gaia['distance_pc'] = 1000 / gaia['parallax']

print("Parallax to distance conversion (first 5 stars):")
print(gaia[['parallax', 'distance_pc']].head())
```

```
Parallax to distance conversion (first 5 stars):
   parallax  distance_pc
0    12.599       79.369
1    11.304       88.462
2    11.486       87.063
3    14.341       69.733
4    20.903       47.840
```

```
# Check for problematic parallax values
# Negative or zero parallax causes division problems
bad_parallax = (gaia['parallax'] <= 0).sum()
if bad_parallax > 0:
    print(f"⚠️ Warning: {bad_parallax} stars with non-positive parallax")
    print("These stars will have negative or infinite distances - data quality issue!")
else:
    print("✓ All parallax values are positive")
```

```
✓ All parallax values are positive
```

The comparison `gaia['parallax'] <= 0` creates a boolean Series, and `.sum()` counts True values (Python treats True as 1, False as 0, so summing a boolean Series counts the Trues).

### Absolute Magnitude

Apparent magnitude tells us how bright a star *appears* from Earth. Absolute magnitude tells us how bright it *truly* is - how bright it would appear at a standard distance of 10 parsecs.

The distance modulus formula:

$M = m - 5 \log\_{10}(d/10)$

where:

* $M$ = absolute magnitude (intrinsic brightness)
* $m$ = apparent magnitude (observed brightness)
* $d$ = distance in parsecs

```
# Calculate absolute G-band magnitude
# Another vectorized operation across all stars
gaia['abs_g_mag'] = gaia['phot_g_mean_mag'] - 5 * np.log10(gaia['distance_pc']/10)

print("Apparent vs Absolute magnitude (first 5 stars):")
comparison = gaia[['phot_g_mean_mag', 'abs_g_mag', 'distance_pc']].head()
print(comparison)
```

```
Apparent vs Absolute magnitude (first 5 stars):
   phot_g_mean_mag  abs_g_mag  distance_pc
0           11.123      6.625       79.369
1           12.686      7.953       88.462
2           14.446      9.747       87.063
3           14.480     10.263       69.733
4           14.491     11.092       47.840
```

Absolute magnitude lets us compare stellar luminosities directly, regardless of distance. A giant star 1000 pc away might have the same apparent magnitude as a nearby dwarf, but very different absolute magnitudes!

### Stellar Color

The color of a star tells us its temperature. Gaia measures brightness in blue (BP) and red (RP) filters. The difference gives us a color index:

**BP - RP = blue magnitude - red magnitude**

* Small or negative values → blue stars → hot (O, B, A types)
* Large positive values → red stars → cool (K, M types)

```
# Calculate BP-RP color index
gaia['bp_rp'] = gaia['phot_bp_mean_mag'] - gaia['phot_rp_mean_mag']

print("Color distribution statistics:")
print(gaia['bp_rp'].describe())
print("\nInterpretation:")
print("  BP-RP < 0.5: Blue (hot) stars")
print("  BP-RP 0.5-1.5: Yellow-white (Sun-like) stars")
print("  BP-RP > 2.0: Red (cool) stars")
```

```
Color distribution statistics:
count   4960.000
mean       1.893
std        0.725
min       -0.104
25%        1.211
50%        2.095
75%        2.489
max        3.769
Name: bp_rp, dtype: float64

Interpretation:
  BP-RP < 0.5: Blue (hot) stars
  BP-RP 0.5-1.5: Yellow-white (Sun-like) stars
  BP-RP > 2.0: Red (cool) stars
```

The `.describe()` output shows our sample ranges from BP-RP ≈ -0.1 to 3.7, spanning the full stellar sequence from hot blue stars to cool red dwarfs!

```
# Classify stars by color
blue_stars = gaia[gaia['bp_rp'] < 0.5].copy()
red_stars = gaia[gaia['bp_rp'] > 2.0].copy()

print(f"Blue stars (BP-RP < 0.5): {len(blue_stars)}")
print("  Likely spectral types: O, B, A (hot, massive, luminous)")
print(f"\nRed stars (BP-RP > 2.0): {len(red_stars)}")
print("  Likely spectral types: K, M (cool, low-mass, long-lived)")
```

```
Blue stars (BP-RP < 0.5): 62
  Likely spectral types: O, B, A (hot, massive, luminous)

Red stars (BP-RP > 2.0): 2672
  Likely spectral types: K, M (cool, low-mass, long-lived)
```

### Avoiding Chained Assignment

**Chained assignment** is a common error where you try to set values through multiple bracket operations in one statement. This confuses Pandas because it can't tell if you're working with a view or a copy.

**Bad example (DON'T DO THIS):**

```
gaia[gaia['magnitude'] < 5]['new_column'] = value
```

What happens:

1. `gaia[gaia['magnitude'] < 5]` creates a filtered DataFrame (might be view or copy - ambiguous!)
2. `['new_column'] = value` tries to set a column on this ambiguous object
3. Pandas doesn't know if you want to modify the original `gaia` or just the filtered result
4. You'll get a `SettingWithCopyWarning` and unpredictable behavior

**Good example (DO THIS):**

```
gaia.loc[gaia['magnitude'] < 5, 'new_column'] = value
```

Let's see the right way:

```
# Correct way: Use .loc[] for conditional assignment
# This unambiguously modifies the original gaia DataFrame
gaia.loc[gaia['phot_g_mean_mag'] < 5, 'very_bright'] = True
gaia.loc[gaia['phot_g_mean_mag'] >= 5, 'very_bright'] = False

print(f"Marked {gaia['very_bright'].sum()} very bright stars (mag < 5)")
print("\n✓ This clearly modifies gaia in-place, no ambiguity!")
```

```
Marked 19 very bright stars (mag < 5)

✓ This clearly modifies gaia in-place, no ambiguity!
```

The `.loc[]` syntax makes your intent explicit: `gaia.loc[rows, column]` clearly means "in the gaia DataFrame, for rows where condition is True, in this column, set the value." No ambiguity about whether you're modifying the original or a copy.

No ambiguity, no warnings, clear intent. Always use `.loc[]` or `.iloc[]` when modifying based on conditions! We're modifying `gaia` in-place by adding a new boolean column. The `.loc[]` indexer ensures this modification happens directly on the original DataFrame.

## Sorting and Finding Extremes

One of the most common tasks in astronomical analysis is finding extreme values - the nearest stars, the brightest objects, the fastest movers. Pandas makes this easy.

### Finding Nearest Stars with .sort\_values()

The `.sort_values()` method arranges rows based on a column's values:

```
# Sort by distance (ascending order - nearest first)
# .sort_values('column') sorts by that column, smallest to largest by default
nearest = gaia.sort_values('distance_pc')

print("The 3 nearest stars:")
print(nearest[['distance_pc', 'phot_g_mean_mag']].head(3))

# Convert nearest star to light-years for context
nearest_pc = nearest.iloc[0]['distance_pc']
nearest_ly = nearest_pc * 3.26  # 1 parsec ≈ 3.26 light-years
print(f"\nNearest star in our sample: {nearest_pc:.1f} parsecs")
print(f"                           = {nearest_ly:.1f} light-years")
```

```
The 3 nearest stars:
      distance_pc  phot_g_mean_mag
1509        9.276            4.656
3937        9.497           13.082
2344        9.860            8.671

Nearest star in our sample: 9.3 parsecs
                           = 30.2 light-years
```

**About views and copies:** `.sort_values()` returns a new DataFrame with rows in different order. This is always a copy (can't rearrange rows in-place without copying). The original `gaia` DataFrame keeps its original row order.

### Direct Access to Extremes: .nlargest() and .nsmallest()

If you just want the extreme values without sorting everything, `.nlargest()` and `.nsmallest()` are more efficient. These methods use specialized algorithms (like heaps) that can find the top N values without sorting the entire dataset:

```
# Get 5 nearest stars directly without full sort
# .nsmallest(n, 'column') returns the n rows with smallest values in that column
closest_five = gaia.nsmallest(5, 'distance_pc')
print("5 nearest stars:")
print(closest_five[['distance_pc', 'phot_g_mean_mag', 'bp_rp']])
```

```
5 nearest stars:
      distance_pc  phot_g_mean_mag  bp_rp
1509        9.276            4.656  0.859
3937        9.497           13.082  3.671
2344        9.860            8.671  2.175
4287       10.361            5.812  1.060
3500       10.764            9.619  2.483
```

**About views and copies:** `.nsmallest()` returns a new DataFrame containing copies of the selected rows.

```
# Stars with highest radial velocity (receding fastest)
# .nlargest(n, 'column') returns the n rows with largest values
fastest_away = gaia.nlargest(3, 'radial_velocity')
print("Stars receding fastest (highest positive radial velocity):")
print(fastest_away[['radial_velocity', 'distance_pc', 'phot_g_mean_mag']])
```

```
Stars receding fastest (highest positive radial velocity):
      radial_velocity  distance_pc  phot_g_mean_mag
547           345.388       44.119           12.934
2060          345.012       69.902           14.107
4837          320.019       79.928           10.700
```

**About views and copies:** Like `.nsmallest()`, this returns a new DataFrame with copies of the selected rows.

## Handling Missing Data

Real astronomical data always has gaps. Instruments fail, weather interrupts observations, some measurements are harder to obtain than others. Learning to handle missing data properly is crucial for honest science.

```
# Count missing values in each column
# .isna() creates a boolean DataFrame (True where values are missing)
# .sum() counts the True values in each column
missing_counts = gaia.isna().sum()
missing_with_values = missing_counts[missing_counts > 0]

if len(missing_with_values) > 0:
    print("Columns with missing data:")
    print(missing_with_values)
    print("\nCompleteness percentages:")
    for col, count in missing_with_values.items():
        percent = 100 * (len(gaia) - count) / len(gaia)
        print(f"  {col}: {percent:.1f}% complete")
else:
    print("✓ No missing data!")
```

```
Columns with missing data:
phot_bp_mean_mag    40
phot_rp_mean_mag    40
bp_rp               40
dtype: int64

Completeness percentages:
  phot_bp_mean_mag: 99.2% complete
  phot_rp_mean_mag: 99.2% complete
  bp_rp: 99.2% complete
```

The `.isna()` method returns a boolean DataFrame with the same shape as the original, where True indicates missing values (NaN) and False indicates present values.

### Strategy 1: Filter for Complete Data

The `.dropna()` method removes rows with missing values. You can specify which columns must be complete:

```
# Keep only stars with complete photometry (BP and RP measurements)
# .dropna(subset=[...]) removes rows where ANY of the specified columns has NaN
has_colors = gaia.dropna(subset=['phot_bp_mean_mag', 'phot_rp_mean_mag']).copy()
print(f"Stars with complete BP and RP photometry: {len(has_colors)}")
print(f"Removed {len(gaia) - len(has_colors)} stars with missing color data")
```

```
Stars with complete BP and RP photometry: 4960
Removed 40 stars with missing color data
```

**About views and copies:** `.dropna()` returns a new DataFrame (subset of rows), so it's always a copy. We explicitly `.copy()` anyway for code clarity - we intend to work with this subset independently.

### Strategy 2: Create Data Quality Flags

Instead of removing stars, keep them all but track what data is available. This preserves your full sample while allowing selective analysis. The `.notna()` method is the opposite of `.isna()` - it returns True where data exists and False where it's missing:

```
# Create boolean flags indicating data availability
# .notna() is the opposite of .isna() - True where data EXISTS
gaia['has_rv'] = gaia['radial_velocity'].notna()
gaia['has_colors'] = gaia['phot_bp_mean_mag'].notna() & gaia['phot_rp_mean_mag'].notna()

print("Data availability in full sample:")
print(f"  Has radial velocity: {gaia['has_rv'].sum()} stars ({100*gaia['has_rv'].sum()/len(gaia):.1f}%)")
print(f"  Has BP/RP colors: {gaia['has_colors'].sum()} stars ({100*gaia['has_colors'].sum()/len(gaia):.1f}%)")
print(f"  Has both: {(gaia['has_rv'] & gaia['has_colors']).sum()} stars")
```

```
Data availability in full sample:
  Has radial velocity: 5000 stars (100.0%)
  Has BP/RP colors: 4960 stars (99.2%)
  Has both: 4960 stars
```

The `.notna()` method returns a boolean Series where True indicates the value exists (is not NaN) and False indicates it's missing. This is the logical opposite of `.isna()`, making it useful for creating availability flags.

We create new columns in `gaia`:

* `has_rv`: True for stars with radial velocity measurements
* `has_colors`: True for stars with both BP and RP photometry

**About modifying:** We're adding new columns to the original `gaia` DataFrame. This is direct modification (no view/copy ambiguity) using simple assignment.

## Handling Duplicates

Catalogs sometimes have duplicate entries from multiple observations, cross-matching errors, or data processing issues. Let's check our Gaia sample:

```
# Check for duplicate source IDs
# .duplicated() returns boolean Series: True for duplicate rows (keeping first occurrence)
duplicates = gaia['source_id'].duplicated().sum()
print(f"Duplicate source_ids: {duplicates}")

if duplicates == 0:
    print("✓ No duplicates - each star appears exactly once")
    print("  This is expected for Gaia DR3 data")
else:
    print(f"⚠️ Found {duplicates} duplicate entries - investigation needed!")
```

```
Duplicate source_ids: 0
✓ No duplicates - each star appears exactly once
  This is expected for Gaia DR3 data
```

The `.duplicated()` method returns a boolean Series identifying duplicate rows in your data. For each row, it checks if that exact combination of values has appeared before in the DataFrame. The method marks the first occurrence as False (not a duplicate) and all subsequent occurrences as True (duplicates). This asymmetric behavior is deliberate and useful - it lets you easily keep the first observation while identifying which later rows are redundant.

### Handling Duplicates When They Occur

If you had duplicates (common when combining catalogs or working with time-series observations), here's how to handle them:

```
# Example with synthetic duplicates
# Imagine multiple observations of the same stars
example = pd.DataFrame({
    'star_id': [1, 2, 2, 3, 3, 3],
    'magnitude': [10.5, 11.2, 11.3, 9.8, 9.9, 9.7],
    'observation_date': ['2023-01-01', '2023-01-05', '2023-02-10', 
                        '2023-01-03', '2023-01-15', '2023-02-20'],
    'quality': [0.9, 0.8, 0.95, 0.7, 0.9, 0.85]
})

print("Example data with multiple observations per star:")
print(example)
```

```
Example data with multiple observations per star:
   star_id  magnitude observation_date  quality
0        1     10.500       2023-01-01    0.900
1        2     11.200       2023-01-05    0.800
2        2     11.300       2023-02-10    0.950
3        3      9.800       2023-01-03    0.700
4        3      9.900       2023-01-15    0.900
5        3      9.700       2023-02-20    0.850
```

This synthetic example shows a common situation: the same star observed multiple times with slightly different measurements. Stars 2 and 3 have multiple entries.

```
# Strategy 1: Keep first observation
# .drop_duplicates(subset=[...]) removes duplicate rows based on specified columns
# keep='first' retains the first occurrence (default behavior)
first_only = example.drop_duplicates(subset=['star_id'], keep='first')
print("Keeping first observation per star:")
print(first_only)
```

```
Keeping first observation per star:
   star_id  magnitude observation_date  quality
0        1     10.500       2023-01-01    0.900
1        2     11.200       2023-01-05    0.800
3        3      9.800       2023-01-03    0.700
```

The `.drop_duplicates()` method:

* **`subset=['col']`**: Identifies duplicates based on these columns
* **`keep='first'`**: Keeps first occurrence, removes later ones
* Returns new DataFrame with duplicates removed

This simple approach keeps chronologically first observations (assuming data is ordered by time).

**About views and copies:** `.drop_duplicates()` returns a new DataFrame (subset of rows), always a copy.

```
# Strategy 2: Keep best quality observation
# Sort by quality first, then drop duplicates (keeping first = best)
best_quality = (example
                .sort_values('quality', ascending=False)  # Highest quality first
                .drop_duplicates(subset=['star_id'], keep='first')  # Keep first = best
                .sort_values('star_id'))  # Re-sort by ID for readability
print("\nKeeping highest quality observation per star:")
print(best_quality)
```

```
Keeping highest quality observation per star:
   star_id  magnitude observation_date  quality
0        1     10.500       2023-01-01    0.900
2        2     11.300       2023-02-10    0.950
4        3      9.900       2023-01-15    0.900
```

This sophisticated approach:

1. **Sorts by quality** (descending) - highest quality first
2. **Drops duplicates keeping first** - retains highest quality observation
3. **Re-sorts by star\_id** - makes output readable

Each method (`.sort_values()`, `.drop_duplicates()`) returns a new DataFrame, so we chain them with parentheses for readability.

This is common in astronomy: when you have multiple observations, keep the one with best seeing conditions, highest signal-to-noise ratio, or most complete data.

**About views and copies:** Each operation in the chain returns a new DataFrame (copies). The final result is independent.

### Converting to NumPy Arrays

Sometimes you need NumPy arrays for specific calculations, plotting, or interfacing with other libraries. The `.to_numpy()` method handles this conversion:

```
# Extract positions as a NumPy array
# .to_numpy() converts DataFrame or Series to NumPy array
positions_array = gaia[['ra', 'dec']].to_numpy()
print(f"NumPy array shape: {positions_array.shape}")
print(f"Type: {type(positions_array)}")
print(f"\nFirst 3 positions (rows):")
print(positions_array[:3])
```

```
NumPy array shape: (5000, 2)
Type: <class 'numpy.ndarray'>

First 3 positions (rows):
[[132.10459271   2.2710516 ]
 [251.09760694 -56.96010036]
 [346.96675822  26.85576486]]
```

The `.to_numpy()` method converts a DataFrame or Series to a NumPy array. For DataFrames, it returns a 2D array with shape (rows × columns), while for Series it returns a 1D array. The resulting array has an appropriate dtype (float64 in this case).

The resulting array has shape (5000, 2) - 5000 stars, 2 coordinates each. You can now use this with NumPy functions, matplotlib, or other tools that expect arrays.

```
# Example: Convert sky positions to Cartesian unit vectors
# This is useful for calculating angular separations
ra_rad = np.radians(positions_array[:, 0])  # Column 0 = RA
dec_rad = np.radians(positions_array[:, 1])  # Column 1 = Dec

# Cartesian unit vectors on celestial sphere
x = np.cos(dec_rad) * np.cos(ra_rad)
y = np.cos(dec_rad) * np.sin(ra_rad)
z = np.sin(dec_rad)

unit_vectors = np.column_stack([x, y, z])
print(f"\nUnit vectors shape: {unit_vectors.shape}")
print(f"First star unit vector: {unit_vectors[0]}")
print(f"Magnitude check (should be 1.0): {np.linalg.norm(unit_vectors[0]):.6f}")
```

```
Unit vectors shape: (5000, 3)
First star unit vector: [-0.66995945  0.74133935  0.03962695]
Magnitude check (should be 1.0): 1.000000
```

## Practical Analysis: Finding Interesting Objects

Let's bring everything together to find scientifically interesting stars. This demonstrates how real astronomical research uses these Pandas operations.

### High-Velocity Stars

Stars moving fast enough to potentially escape the galaxy are rare and scientifically valuable. They might have been:

* Ejected by the supermassive black hole at the galactic center
* Thrown out by supernova explosions in binary systems
* Remnants from disrupted dwarf galaxies

To find them, we need to calculate total 3D velocity from Gaia's measurements.

```
# Get stars with complete kinematic data (all three velocity components)
# Need proper motions (pmra, pmdec) AND radial velocity
has_kinematics = gaia.dropna(subset=['pmra', 'pmdec', 'radial_velocity']).copy()

print(f"Stars with complete 3D velocities: {len(has_kinematics)}")
print(f"That's {100 * len(has_kinematics) / len(gaia):.1f}% of our sample")
print(f"\nLost {len(gaia) - len(has_kinematics)} stars due to missing radial velocities")
```

```
Stars with complete 3D velocities: 5000
That's 100.0% of our sample

Lost 0 stars due to missing radial velocities
```

We filter to stars with all three velocity components

```
# Calculate total space velocity from proper motions and radial velocity

# Step 1: Total proper motion (combining RA and Dec components)
has_kinematics['pm_total'] = np.sqrt(
    has_kinematics['pmra']**2 + has_kinematics['pmdec']**2
)

# Step 2: Convert proper motion to tangential velocity
# v_tangential (km/s) = 4.74 × μ (mas/yr) × d (pc)
# The factor 4.74 comes from unit conversions
has_kinematics['v_tan'] = 4.74 * has_kinematics['pm_total'] * has_kinematics['distance_pc']

# Step 3: Combine tangential and radial velocities
# Pythagorean theorem in 3D: v_total = √(v_tan² + v_radial²)
has_kinematics['v_total'] = np.sqrt(
    has_kinematics['v_tan']**2 + has_kinematics['radial_velocity']**2
)

print("Velocity calculation complete!")
print("\nVelocity statistics:")
print(has_kinematics['v_total'].describe())
```

```
Velocity calculation complete!

Velocity statistics:
count     5000.000
mean     36925.872
std      27396.126
min        229.289
25%      18522.879
50%      30624.537
75%      49227.127
max     352281.893
Name: v_total, dtype: float64
```

All calculations are vectorized (applied to entire columns at once) - fast and efficient!

```
# Find high-velocity candidates
# Threshold: 350 km/s is significantly above typical stellar velocities
high_velocity = has_kinematics.query('v_total > 350').copy()

print(f"High-velocity star candidates: {len(high_velocity)}")

if len(high_velocity) > 0:
    # Show the fastest stars
    fastest = high_velocity.nlargest(3, 'v_total')
    print("\n3 Fastest stars:")
    print(fastest[['v_total', 'radial_velocity', 'v_tan', 'distance_pc']])
    
    print(f"\nContext for interpretation:")
    print(f"  Sun's orbital velocity around galaxy: ~230 km/s")
    print(f"  Typical stellar velocities: 20-100 km/s")
    print(f"  Galactic escape velocity: ~550 km/s")
    print(f"  Maximum velocity in our sample: {high_velocity['v_total'].max():.0f} km/s")
else:
    print("\nNo high-velocity stars found in this sample.")
    print("Hypervelocity stars are extremely rare!")
```

```
High-velocity star candidates: 4999

3 Fastest stars:
        v_total  radial_velocity      v_tan  distance_pc
1633 352281.893            4.070 352281.893       95.465
3872 341064.426           37.531 341064.424       58.801
764  340222.366           -2.369 340222.366       92.216

Context for interpretation:
  Sun's orbital velocity around galaxy: ~230 km/s
  Typical stellar velocities: 20-100 km/s
  Galactic escape velocity: ~550 km/s
  Maximum velocity in our sample: 352282 km/s
```

The `.query()` filters for velocities > 350 km/s. Finding even one genuine hypervelocity star would be exciting! They're extremely rare - only a few dozen confirmed in the entire galaxy.

### Nearby Red Dwarfs for Exoplanet Searches

Red dwarfs (M-type stars) are ideal targets for finding habitable exoplanets because:

1. **Most common stars**: ~75% of all stars are red dwarfs
2. **Low mass**: Planets cause larger wobble (easier radial velocity detection)
3. **Small radius**: Planets block more light (deeper transits)
4. **Close habitable zone**: Planets orbit closer and faster (shorter observation time)
5. **Long-lived**: Burn slowly, giving life billions of years to develop

Let's find nearby red dwarf candidates:

```
# Identify nearby red dwarfs using multiple criteria
# Criteria:
#   - Close: distance < 20 pc (easier to observe)
#   - Red: BP-RP > 2 (cool, indicative of M-type)
#   - Intrinsically faint: abs_g_mag > 8 (low luminosity, characteristic of red dwarfs)
red_dwarfs = gaia.query(
    'distance_pc < 20 & bp_rp > 2 & abs_g_mag > 8'
).copy()

print(f"Nearby red dwarf candidates: {len(red_dwarfs)}")
print(f"That's {100 * len(red_dwarfs) / len(gaia):.1f}% of our sample")

if len(red_dwarfs) > 0:
    print("\nThese are excellent exoplanet search targets!")
```

```
Nearby red dwarf candidates: 38
That's 0.8% of our sample

These are excellent exoplanet search targets!
```

The `.query()` combines three criteria:

**distance\_pc < 20**: Within 20 parsecs (~65 light-years)
**bp\_rp > 2**: Red color index
**abs\_g\_mag > 8**: Intrinsically faint

```
if len(red_dwarfs) > 0:
    # Find the nearest red dwarfs and prioritize them
    nearest_red = red_dwarfs.nsmallest(5, 'distance_pc').copy()
    
    # Calculate priority score based on multiple factors
    # Higher score = better target
    nearest_red['priority'] = (
        (1 / nearest_red['distance_pc']) *       # Closer is better (easier to observe)
        nearest_red['bp_rp'] *                    # Redder is better (cooler = more M-type)
        (1 / nearest_red['phot_g_mean_mag'])     # Brighter is better (better signal)
    )
    
    print("\nTop 5 red dwarf targets (sorted by priority):")
    result = nearest_red.sort_values('priority', ascending=False)
    print(result[['distance_pc', 'phot_g_mean_mag', 'bp_rp', 'priority']])
    
    print("\nPriority score factors:")
    print("  - Closer stars score higher (easier observation)")
    print("  - Redder stars score higher (cooler = more M-type)")
    print("  - Brighter stars score higher (better signal-to-noise)")
```

```
Top 5 red dwarf targets (sorted by priority):
      distance_pc  phot_g_mean_mag  bp_rp  priority
3937        9.497           13.082  3.671     0.030
2344        9.860            8.671  2.175     0.025
3500       10.764            9.619  2.483     0.024
4768       12.127           13.250  3.332     0.021
3661       11.949            9.938  2.285     0.019

Priority score factors:
  - Closer stars score higher (easier observation)
  - Redder stars score higher (cooler = more M-type)
  - Brighter stars score higher (better signal-to-noise)
```

Multiplying these factors gives a combined priority. The star with highest score is your best target for an exoplanet search campaign!

## Saving Your Results

After analysis, save your findings for future use, publication, or sharing with collaborators:

```
# Define columns to save (keep it focused on key measurements)
save_cols = ['source_id', 'ra', 'dec', 'distance_pc', 
             'phot_g_mean_mag', 'abs_g_mag', 'bp_rp']

# Save high-velocity stars if we found any
if len(high_velocity) > 0:
    # Add velocity columns to save list for this catalog
    hv_cols = save_cols + ['radial_velocity', 'v_total', 'v_tan']
    high_velocity[hv_cols].to_csv('high_velocity_stars.csv', index=False)
    print(f"✓ Saved {len(high_velocity)} high-velocity stars to 'high_velocity_stars.csv'")

# Save red dwarf candidates
if len(red_dwarfs) > 0:
    red_dwarfs[save_cols].to_csv('red_dwarf_targets.csv', index=False)
    print(f"✓ Saved {len(red_dwarfs)} red dwarf candidates to 'red_dwarf_targets.csv'")
```

```
✓ Saved 4999 high-velocity stars to 'high_velocity_stars.csv'
✓ Saved 38 red dwarf candidates to 'red_dwarf_targets.csv'
```

The `.to_csv()` method takes a filename as its first argument and saves the DataFrame to that file. The `index=False` parameter tells Pandas not to save the DataFrame's index column (which would appear as the first column if `index=True`, the default). Since our index is just sequential numbers (0, 1, 2...) with no meaningful information, we skip it to keep the output files clean and focused on the actual data.

### Saving to Different Formats

While CSV files are universal and human-readable, Pandas supports many other formats. Each has advantages for different use cases:

```
# JSON format - preserves data types and nested structures
if len(red_dwarfs) > 0:
    # Save as JSON with nice formatting
    red_dwarfs[save_cols].to_json('red_dwarf_targets.json', 
                                   orient='records',  # List of dictionaries
                                   indent=2)          # Pretty printing
    print(f"✓ Saved to JSON format: 'red_dwarf_targets.json'")
    
# Excel format - useful for sharing with collaborators
if len(red_dwarfs) > 0:
    red_dwarfs[save_cols].to_excel('red_dwarf_targets.xlsx', 
                                    index=False,
                                    sheet_name='Red Dwarfs')
    print(f"✓ Saved to Excel format: 'red_dwarf_targets.xlsx'")
    
# Parquet format - efficient binary format for large datasets
if len(gaia) > 0:
    gaia.to_parquet('gaia_processed.parquet')
    print(f"✓ Saved to Parquet format: 'gaia_processed.parquet'")
```

```
✓ Saved to JSON format: 'red_dwarf_targets.json'
```

```
✓ Saved to Excel format: 'red_dwarf_targets.xlsx'
```

```
✓ Saved to Parquet format: 'gaia_processed.parquet'
```

**When to use each format:**

* **CSV**: Universal compatibility, human-readable, good for archiving
* **JSON**: Web applications, preserving nested structures, configuration files
* **Excel**: Sharing with non-programmers, adding formatted tables and charts
* **Parquet**: Large datasets, fast I/O, preserving complex data types

You can reload any of these formats:

* `pd.read_csv('file.csv')`
* `pd.read_json('file.json')`
* `pd.read_excel('file.xlsx')`
* `pd.read_parquet('file.parquet')`

## Summary

### Key Concepts

In this lecture, you've learned:

* **Series and DataFrames**: How Pandas organizes tabular data with labeled rows and columns, solving the synchronization problems of managing multiple lists and providing efficient vectorized operations for astronomical catalogs
* **Selection Methods**: How to extract specific data using column notation `[]`, position-based indexing with `.iloc[]`, and label-based indexing with `.loc[]`, understanding the critical difference that `.iloc[]` excludes the endpoint while `.loc[]` includes it
* **Boolean Filtering**: How to create boolean masks with comparison operators, combine them with `&`, `|`, and `~` (always with parentheses), and use `.query()` for readable complex filters or `.isin()` for membership testing
* **Column Transformations**: How to add calculated columns using vectorized operations that apply to entire columns simultaneously, making distance and velocity calculations much faster than Python loops
* **Sorting and Extremes**: How to reorder DataFrames with `.sort_values()` or efficiently find extreme values with `.nlargest()` and `.nsmallest()` without sorting the entire dataset
* **Missing Data and Duplicate Management**: How to identify missing values with `.isna()` and `.notna()`, remove incomplete rows with `.dropna()`, detect duplicates with `.duplicated()`, remove them with `.drop_duplicates()`, and implement strategies for keeping the best observation when multiple measurements exist while tracking data quality
* **Views versus Copies**: Why some operations share memory (views) while others create independent data (copies), and the safe practices of using explicit `.copy()` when you need independence or `.loc[]` when modifying the original DataFrame to avoid subtle bugs

### What You Can Now Do

After working through this material, you should be able to:

* Load any astronomical catalog and immediately explore its structure, data types, and statistical properties
* Filter catalogs efficiently to find stars matching complex criteria like distance, brightness, color, and velocity
* Calculate derived quantities like absolute magnitudes, distances from parallaxes, and total space velocities for vast numbers of stars simultaneously
* Identify scientifically interesting objects like high-velocity stars and nearby red dwarf exoplanet hosts
* Handle real-world data problems including missing measurements, duplicate entries, and measurement quality variations
* Save your processed results to CSV files for further analysis, publication, or sharing with collaborators

### Practice Suggestions

To solidify these concepts:

1. Find all naked-eye stars (magnitude < 6) within 10 parsecs and calculate their absolute magnitudes
2. Identify candidate binary stars by finding pairs with similar positions but different radial velocities
3. Calculate tangential velocities for all stars with proper motions and create a histogram showing the velocity distribution
4. Build a color-magnitude diagram separating main sequence stars, giants, and white dwarfs using BP-RP color and absolute magnitude
5. Write a single chained operation finding the 10 nearest G-type Sun-like stars (0.6 < BP-RP < 0.8) with measured radial velocities

### Looking Ahead

Next lecture, we'll build on these foundations to explore advanced Pandas operations for multi-dimensional analysis. The selection, filtering, and transformation techniques you've practiced today will be essential for more sophisticated research tasks. You'll learn to use GroupBy operations to compute statistics separately for different stellar populations, and create pivot tables for analyzing how properties vary across multiple dimensions. We'll handle time-series data for variable star studies and observation planning, and work with multi-index DataFrames for hierarchical astronomical data structures. You'll also learn to merge multiple catalogs together to cross-match observations from different surveys. These advanced techniques form the backbone of modern astronomical research pipelines, from exoplanet detection to gravitational wave follow-up campaigns.
