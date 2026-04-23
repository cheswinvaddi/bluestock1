import pandas as pd
import glob
import os

# -----------------------------
# STEP 1: Load all Excel files
# -----------------------------
files = glob.glob("data/*.xls")   # reads all xls files in folder

all_data=[]

for file in files:
    print(f"Reading {file}")
    df = pd.read_excel(file)

    # Add source file name
    df["source_file"]=os.path.basename(file)

    all_data.append(df)

# Merge all states data
df = pd.concat(all_data, ignore_index=True)

print("\nAll files merged successfully.")
print("Total rows:",len(df))


# -----------------------------
# STEP 2 View Columns
# -----------------------------
print("\nColumns:")
print(df.columns)


# Change names below if your column names differ
STATE_COL="STATE NAME"
DIST_COL="DISTRICT NAME"
SUBDIST_COL="SUB-DISTRICT NAME"
VILLAGE_COL="Area Name"


# -----------------------------
# STEP 3 Data Profiling
# -----------------------------
print("\n--- DATA PROFILE ---")

print("States:",
      df[STATE_COL].nunique())

print("Districts:",
      df[DIST_COL].nunique())

print("Subdistricts:",
      df[SUBDIST_COL].nunique())

print("Villages:",
      df[VILLAGE_COL].nunique())

print("\nMissing Values:")
print(
df[
[STATE_COL,DIST_COL,SUBDIST_COL,VILLAGE_COL]
].isnull().sum()
)


# duplicates
duplicates=df.duplicated().sum()
print("\nDuplicate Rows:",duplicates)



# -----------------------------
# STEP 4 Clean Data
# -----------------------------
print("\nCleaning data...")

# remove duplicates
df=df.drop_duplicates()

# remove blank rows
df=df.dropna(
subset=[
STATE_COL,
DIST_COL,
SUBDIST_COL,
VILLAGE_COL
]
)

# remove spaces
for col in [STATE_COL,DIST_COL,SUBDIST_COL,VILLAGE_COL]:
    df[col]=df[col].astype(str).str.strip()

# standardize capitalization
for col in [STATE_COL,DIST_COL,SUBDIST_COL,VILLAGE_COL]:
    df[col]=df[col].str.title()


print("Cleaning completed.")
print("Rows after cleaning:",len(df))


# -----------------------------
# STEP 5 Analysis
# -----------------------------

# Villages per district
district_counts=(
df.groupby(DIST_COL)[VILLAGE_COL]
.nunique()
.sort_values(ascending=False)
)

print("\nTop 10 Districts by villages")
print(
district_counts.head(10)
)


# villages per state
state_counts=(
df.groupby(STATE_COL)[VILLAGE_COL]
.nunique()
.sort_values(ascending=False)
)

print("\nVillages per State")
print(
state_counts
)



# -----------------------------
# STEP 6 Create separate tables
# (for database normalization)
# -----------------------------

states=df[[STATE_COL]].drop_duplicates()

df = df[df["MDDS PLCN"] != 0]

# remove junk unnamed columns
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# keep actual village rows only
df = df[df["MDDS PLCN"] != 0]

districts=df[
[STATE_COL,DIST_COL]
].drop_duplicates()

subdistricts=df[
[DIST_COL,SUBDIST_COL]
].drop_duplicates()

villages=df[
[SUBDIST_COL,VILLAGE_COL]
].drop_duplicates()


# -----------------------------
# STEP 7 Export files
# -----------------------------

df.to_csv(
"cleaned_villages_master.csv",
index=False
)

states.to_csv(
"states.csv",
index=False
)

districts.to_csv(
"districts.csv",
index=False
)

subdistricts.to_csv(
"subdistricts.csv",
index=False
)

villages.to_csv(
"villages.csv",
index=False
)
df=df.loc[:, ~df.columns.str.contains('^Unnamed')]


print("\nFiles exported successfully.")
print("""
Generated:
cleaned_villages_master.csv
states.csv
districts.csv
subdistricts.csv
villages.csv
""")