# -------------------------------------------------------------------------------
# --------------------- STEP 1: LOAD & INSPECT THE DATA --------------------------
# -------------------------------------------------------------------------------

import pandas as pd
import numpy as np

# --- load the file I saved locally (safer than using the online source) ---
print("\n" + "-"*80)
print("STEP 1 — Loading dataset from local CSV")
print("-"*80)
df = pd.read_csv(r"D:\Swaleha\Coding\TechAI Tasks\Swaleha_techai_task_2\Meteorite-Landings.csv")   # change filename if yours is different

# --- show columns so I know the exact column names I have to work with ---
print("\n--- Columns in the dataset ---")
print(df.columns.tolist())

# --- preview a few rows so I can visually check formatting (names, examples) ---
print("\n--- First 5 rows (raw data) ---")
print(df.head())

# --- summary info to see types and non-null counts ---
print("\n--- df.info() (data types and non-null counts) ---")
df.info()

# -----------------
# Now extract numeric values from the messy text columns:
#   - 'Mass' looks like: Quantity[4239, "Grams"]
#   - 'Year' looks like: DateObject[{1919}, "Year", ...]
#   - 'Coordinates' looks like: GeoPosition[{32.1, 71.8}]
# I create new numeric columns: Mass_g, Year_num, Latitude, Longitude
# -----------------

print("\n--- Cleaning text columns to numeric columns (Mass, Year, Coordinates) ---")

# Mass: capture the numeric part inside Quantity[ ... , ... ]
# - expand=False returns a Series (one column) instead of a DataFrame
df['Mass_g'] = df['Mass'].str.extract(r'Quantity\[\s*([0-9]+(?:\.[0-9]+)?)\s*,', expand=False)

# convert the extracted strings to floats (so I can do math on them)
df['Mass_g'] = df['Mass_g'].astype(float)

# Year: capture the year from DateObject[{1880}, ...]
df['Year_num'] = df['Year'].str.extract(r'DateObject\[\{\s*(\d{3,4})\s*\}', expand=False)
df['Year_num'] = df['Year_num'].astype(float)

# Coordinates: capture two groups (lat, long) from inside the braces
# Using expand=True returns a DataFrame with 2 columns (group1, group2)
coords = df['Coordinates'].str.extract(r'\{\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\}', expand=True)
df['Latitude']  = coords[0].astype(float)   # coords[0] is the first captured group (latitude)
df['Longitude'] = coords[1].astype(float)   # coords[1] is the second captured group (longitude)

# --- show numeric preview (new columns) ---
print("\n--- Preview of numeric columns I created ---")
print(df[['Name', 'Mass_g', 'Year_num', 'Latitude', 'Longitude']].head())

# --- descriptive statistics for the numeric columns ---
print("\n--- Descriptive statistics for Mass_g, Year_num, Latitude, Longitude ---")
print(df[['Mass_g', 'Year_num', 'Latitude', 'Longitude']].describe())

print("\nSTEP 1 complete — numeric columns created!")
print("-"*80 + "\n")

# -------------------------------------------------------------------------------
# ------------------- STEP 2: CLEANING & PREPARATION -----------------------------
# -------------------------------------------------------------------------------

print("\n" + "-"*80)
print("STEP 2 — Cleaning & preparing the numeric data")
print("-"*80)

# 1) quick missing-value check before cleaning so I can compare later
print("\n--- Missing values BEFORE cleaning (counts per column) ---")
print(df.isna().sum())

# 2) drop rows that have no Mass_g or no Year_num — I need those for main analysis
#    (I keep rows with missing coordinates for now, because some analyses do not need coordinates)
df_before = df.shape[0]
df = df.dropna(subset=['Mass_g', 'Year_num'])
df_after_dropna = df.shape[0]
print(f"\nDropped {df_before - df_after_dropna} rows because Mass or Year was missing.")

# 3) filter unrealistic / invalid values:
#    - mass must be > 0 (mass = 0 makes no sense here)
#    - optionally remove extremely huge values (here I use 6e7 grams = 60,000 kg as an upper sanity limit)
#    - accept only years in a realistic recorded range (860 to 2025)
print("\n--- Filtering unrealistic values ---")
mass_upper_limit = 6e7   # adjust if you want a different cap
df = df[(df['Mass_g'] > 0) & (df['Mass_g'] < mass_upper_limit)]
df = df[(df['Year_num'] >= 860) & (df['Year_num'] <= 2025)]

# 4) create useful derived columns:
#    - Mass_kg (so numbers are easier to read)
#    - Decade (to group by decades later)
df['Mass_kg'] = df['Mass_g'] / 1000.0
# Year_num is float but now safe to convert to int for decade math (we dropped NaNs)
df['Decade'] = (df['Year_num'].astype(int) // 10) * 10

# 5) reset index for a clean DataFrame after filtering
df.reset_index(drop=True, inplace=True)

# 6) final checks and summaries after cleaning
print("\n--- After cleaning: df.info() ---")
df.info()

print("\n--- After cleaning: descriptive stats (Mass_kg and Year_num) ---")
print(df[['Mass_kg', 'Year_num', 'Latitude', 'Longitude']].describe())

print("\nSTEP 2 complete — dataset cleaned and ready for analysis.")
print("-"*80 + "\n")

# -----------------------------------------------------------
# -----STEP 3: The Detective Work (Analysis & Insights)------
# -----------------------------------------------------------

import numpy as np

# 1) Filtering & Sorting – Find the 10 heaviest meteorites

# I’m sorting the DataFrame in descending order of 'Mass' 
# and then selecting the first 10 rows to see the largest meteorites ever found.
heaviest_meteorites = df.sort_values(by="Mass_g", ascending=False).head(10)

print("\n🔹 Top 10 Heaviest Meteorites:\n")
print(heaviest_meteorites[["Name", "Mass_g", "Year_num", "Latitude", "Longitude"]])
print("\n" + "-"*80 + "\n")

# 2) Grouping & Aggregation – Count Fell vs Found meteorites

# I’m grouping the data by the 'Fall' column which tells whether 
# the meteorite was actually seen falling ('Fell') or found later ('Found').
fall_counts = df["Fall"].value_counts()

print("🔹 Count of Fell vs Found Meteorites:\n")
print(fall_counts)
print("\n" + "-"*80 + "\n")

# Now I also want to see the average mass of meteorites for each classification type.
# 'Classification' tells what type of material/composition the meteorite belongs to.
avg_mass_by_class = df.groupby("Classification")["Mass_g"].mean().sort_values(ascending=False).head(10)

print("🔹 Top 10 Classifications by Average Mass:\n")
print(avg_mass_by_class)
print("\n" + "-"*80 + "\n")

# 3) Time-Based Analysis – Group by decade

# I already created 'Decade' in Step 2, so I can just count occurrences per decade
meteorites_per_decade = df["Decade"].value_counts().sort_index()

print("🔹 Meteorite Discoveries by Decade:\n")
print(meteorites_per_decade)
print("\n" + "-"*80 + "\n")

# 4) NumPy Operations on Mass

# I’m converting the 'Mass_g' column into a NumPy array for numerical calculations.
mass_array = df["Mass_g"].to_numpy()

print("🔹 NumPy Calculations on Meteorite Mass (in grams):\n")
print(f"Mean mass: {np.mean(mass_array):,.2f}")
print(f"Median mass: {np.median(mass_array):,.2f}")
print(f"Standard Deviation: {np.std(mass_array):,.2f}")
print(f"Total mass of all meteorites: {np.sum(mass_array):,.2f}")
print(f"Maximum mass recorded: {np.max(mass_array):,.2f}")
print("\n" + "-"*80 + "\n")

# -------------------------------------------------------------------------------
# --------------------- STEP 4: TELL THE STORY (VISUALIZATION) ------------------
# -------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import seaborn as sns

# Use Seaborn style for nicer plots
sns.set_style("whitegrid")

# 1) Histogram of Meteorite Mass (log scale)
print("\n--- Plot 1: Distribution of Meteorite Mass (log scale) ---")
plt.figure(figsize=(10,6))
sns.histplot(df['Mass_kg'], bins=50, log_scale=True, color='skyblue')
plt.title("Distribution of Meteorite Mass (kg) — Log Scale")
plt.xlabel("Mass (kg)")
plt.ylabel("Count")
plt.show()

# 2) Count of Fell vs Found Meteorites
print("\n--- Plot 2: Fell vs Found Counts ---")
plt.figure(figsize=(6,5))
sns.countplot(x='Fall', data=df, palette='pastel', hue=None)  # Added hue=None to remove FutureWarning
plt.title("Meteorites by Fall Type")
plt.xlabel("Fall Type")
plt.ylabel("Number of Meteorites")
plt.show()

# 3) Top 10 Most Common Classifications (Bar Plot)
print("\n--- Plot 3: Top 10 Meteorite Classifications ---")
top_classes = df['Classification'].value_counts().head(10)
plt.figure(figsize=(10,6))
sns.barplot(x=top_classes.values, y=top_classes.index, palette='viridis', hue=None)  # Added hue=None
plt.title("Top 10 Most Common Meteorite Classifications")
plt.xlabel("Count")
plt.ylabel("Classification")
plt.show()

# 4) Scatter Plot of Latitude vs Longitude (Geographic Spread)
print("\n--- Plot 4: Geographic Distribution of Meteorites ---")
plt.figure(figsize=(12,6))
sns.scatterplot(x='Longitude', y='Latitude', hue='Fall', data=df,
                alpha=0.6, palette='Set1', edgecolor=None)
plt.title("Geographic Distribution of Meteorite Landings")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend(title='Fall Type')
plt.show()

print("\nSTEP 4 complete — four plots generated to visualize the meteorite data.")
print("-"*80 + "\n")

