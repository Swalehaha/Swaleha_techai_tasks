=========================================================
                   METEORITE LANDINGS EDA
=========================================================

Project Overview:
-----------------
This project performs an Exploratory Data Analysis (EDA) on a dataset containing
all known meteorite landings on Earth. The goal is to clean, analyze, and visualize
the data to discover patterns about where, when, and what types of meteorites have fallen.

Dataset:
--------
- File: Meteorite_Landings.csv
- Source: Downloaded locally for safety and reliability
- Contains information such as meteorite name, ID, classification, mass, year, fall type,
  and coordinates (latitude and longitude).

Steps Performed:
----------------

STEP 1: Setup & Initial Inspection
- Loaded the CSV file into a Pandas DataFrame.
- Inspected the first few rows using `.head()`.
- Generated summary information with `.info()` and descriptive statistics with `.describe()`.
- Extracted numerical data from complex columns (Mass, Year, Coordinates) using regex.
- Converted columns to appropriate data types (`float`) for analysis.

STEP 2: Data Cleaning & Preparation
- Removed rows with missing or erroneous values in Mass, Year, or Coordinates.
- Converted mass to kilograms for consistency.
- Extracted latitude and longitude from the coordinates column.
- Ensured all numeric columns are ready for analysis.

STEP 3: Analysis & Insights
- Found the 10 heaviest meteorites.
- Counted Fell vs Found meteorites.
- Calculated average mass for the most common meteorite classifications.
- Grouped discoveries by decade to analyze trends over time.
- Performed NumPy operations (mean, median, std, sum, max) on mass data.

STEP 4: Visualization
- Created four well-labeled plots to tell the story:
  1) Histogram of meteorite mass (log scale)
  2) Count of Fell vs Found meteorites
  3) Top 10 most common classifications (bar plot)
  4) Scatter plot of latitude vs longitude to show geographic spread
- Plots include titles, axis labels, legends, and clear styling.


How to Run:
-----------
1) Place `Meteorite_Landings.csv` in the project directory.
2) Open `swaleha_techai_task_2.ipynb` (or .py file) in Jupyter Notebook or VSCode.
3) Ensure Python 3.x is installed with the following libraries:
   - pandas
   - numpy
   - matplotlib
   - seaborn
4) Run the notebook/script step by step (Step 1 → Step 4).

Key Learnings:
--------------
- How to handle and clean messy datasets.
- Extracting numerical data from complex string patterns using regex.
- Performing descriptive statistics and aggregations with Pandas and NumPy.
- Creating meaningful visualizations to discover patterns in data.
- Understanding temporal and geographic trends in meteorite landings.

Contact:
--------
Project created by Swaleha Shaikh
