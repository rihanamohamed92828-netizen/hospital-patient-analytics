# Hospital Patient Analytics Dashboard

Python and SQL pipeline that cleans hospital admission records, loads them into a SQLite database, answers business questions with SQL, and builds an HTML dashboard.

## Problem
Hospital admin teams need a clear view of admissions, length of stay and billing to plan staffing, beds and revenue. Raw records have duplicates, invalid bills and inconsistent text, so they have to be cleaned first.

## Dataset
"Healthcare Dataset" (Kaggle, 55,500 admission records, 15 columns: age, gender, medical condition, admission and discharge dates, doctor, hospital, insurer, billing amount, admission type, medication, test results). It is a **synthetic** public dataset, so it contains no real patient data. A copy is in `data/healthcare_dataset.csv`.

## Approach
1. **Clean (Python/pandas, `clean.py`)**: standardize column names and name capitalization, trim text, parse dates, remove 534 duplicate rows, remove 106 rows with negative billing amounts, check discharge is not before admission, add `length_of_stay` and `age_group`. 54,860 clean rows remain.
2. **Store**: load into SQLite (`hospital.db`, table `admissions`).
3. **Analyze (SQL, `queries.sql`)**: KPIs, admissions and cost by condition, admission type, age group and insurer, monthly trend, test results, busiest doctors.
4. **Dashboard (`dashboard.py`)**: runs the queries and writes `results/dashboard.html` plus PNG charts.

## Results
- 54,860 admissions, average stay 15.5 days, average bill about $25,595, total billing about $1.4B.
- The six conditions are almost evenly split (about 9,100 to 9,200 admissions each).
- Monthly admissions are steady at about 900 (first and last months are partial and left out of the trend chart).
- Admission types are balanced: Elective 18,437, Urgent 18,353, Emergency 18,070.
- Average bill and length of stay vary very little between groups. This is expected for a synthetic dataset, so the value of the project is the pipeline and dashboard, not clinical findings.

Open `results/dashboard.html` in a browser to see the dashboard. Chart images are in `results/`.

## Dashboard note
The dashboard is an HTML page built with matplotlib instead of Power BI, so it runs without extra software.

## How to run
```bash
git clone <this-repo-url>
cd hospital-patient-analytics
pip install -r requirements.txt
python clean.py        # cleans data, creates hospital.db
python dashboard.py    # runs the SQL and builds results/dashboard.html
```

## Tech
Python, pandas, SQL (SQLite), matplotlib, HTML/CSS.
