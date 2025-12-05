import pandas as pd

df = pd.read_csv("student_data.csv")

df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace(" ", "_")
)

df["name"] = df["name"].astype(str)

df["name"] = (
    df["name"]
      .str.replace("’", "'", regex=False)
      .str.replace("‘", "'", regex=False)
)

df["name"] = df["name"].str.strip()

df["name"] = df["name"].str.replace(r"\s+", " ", regex=True)

df["name"] = df["name"].str.replace(r'^[\"\' ]+', "", regex=True)
df["name"] = df["name"].str.replace(r'[\"\'., ]+$', "", regex=True)

df["name"] = df["name"].str.title()

name_split = df["name"].str.rsplit(" ", n=1, expand=True)
df["first_name"] = name_split[0]
df["last_name"] = name_split[1]

other_cols = [c for c in df.columns if c not in ["name", "first_name", "last_name"]]
df = df[["last_name", "first_name"] + other_cols]

df["grade"] = df["grade"].astype(str).str.strip()
df["grade"] = df["grade"].replace({"": pd.NA, "nan": pd.NA})
df.loc[df["grade"].notna(), "grade"] = df.loc[df["grade"].notna(), "grade"].str.upper()

df["attendance"] = df["attendance"].astype(str).str.strip()
df["attendance"] = df["attendance"].str.replace("%", "", regex=False)
df["attendance"] = df["attendance"].str.strip()

df["attendance_numeric"] = pd.to_numeric(df["attendance"], errors="coerce")
df["attendance"] = df["attendance_numeric"]
df = df.drop(columns=["attendance_numeric"])

df["comments"] = df["comments"].astype(str).str.strip()
df["comments"] = df["comments"].replace({"": pd.NA, "nan": pd.NA})
df["comments"] = df["comments"].fillna("No comments")

df["comments"] = df["comments"].str.replace(r'^[\"\']+', "", regex=True)
df["comments"] = df["comments"].str.replace(r'[\"\']+$', "", regex=True)

df["comments"] = df["comments"].str.replace(r'\"{2,}', '"', regex=True)
df["comments"] = df["comments"].str.replace(r"\'{2,}", "'", regex=True)

df["comments"] = df["comments"].str.replace(r'^[\"\']', "", regex=True)
df["comments"] = df["comments"].str.replace(r'[\"\']$', "", regex=True)

before_rows = len(df)
df = df.dropna(subset=["grade", "attendance"])
after_rows = len(df)
print(f"Dropped {before_rows - after_rows} rows due to missing grade/attendance.")

before_dupes = len(df)
df = df.drop_duplicates()
after_dupes = len(df)
print(f"Removed {before_dupes - after_dupes} duplicate rows.")

assert df["grade"].isna().sum() == 0, "There are still missing grades."
assert pd.api.types.is_numeric_dtype(df["attendance"]), "Attendance is not numeric."
assert df.duplicated().sum() == 0, "There are still duplicate rows."

print("Validation checks passed.")

df.to_csv("student_data_cleaned.csv", index=False)
print("Cleaned data saved to student_data_cleaned.csv")