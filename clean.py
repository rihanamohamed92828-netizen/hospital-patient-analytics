"""Step 1: clean the raw data and load it into SQLite."""
import sqlite3
import pandas as pd

raw = pd.read_csv("data/healthcare_dataset.csv")
print("raw rows:", len(raw))
df = raw.copy()
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
df["name"] = df["name"].str.strip().str.title()          # fix inconsistent capitalization
df["doctor"] = df["doctor"].str.strip()
df["hospital"] = df["hospital"].str.strip().str.replace(r"^and\s+|,$", "", regex=True)
df["date_of_admission"] = pd.to_datetime(df["date_of_admission"])
df["discharge_date"] = pd.to_datetime(df["discharge_date"])
dups = df.duplicated().sum()
df = df.drop_duplicates()
df["billing_amount"] = df["billing_amount"].round(2)
bad_bill = (df["billing_amount"] < 0).sum()
df = df[df["billing_amount"] >= 0]                        # negative bills are invalid
df["length_of_stay"] = (df["discharge_date"] - df["date_of_admission"]).dt.days
df = df[df["length_of_stay"] >= 0]
df["age_group"] = pd.cut(df["age"], [0, 17, 34, 49, 64, 120],
                         labels=["0-17", "18-34", "35-49", "50-64", "65+"])
print(f"duplicates removed: {dups}, negative bills removed: {bad_bill}")
print("missing values:", int(df.isna().sum().sum()), "| clean rows:", len(df))

out = df.copy()
for c in ["date_of_admission", "discharge_date"]:
    out[c] = out[c].dt.strftime("%Y-%m-%d")
out["age_group"] = out["age_group"].astype(str)
out.to_csv("data/cleaned_patients.csv", index=False)
with sqlite3.connect("hospital.db") as con:
    out.to_sql("admissions", con, if_exists="replace", index=False)
print("loaded into hospital.db table 'admissions'")
