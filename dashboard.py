"""Step 2: run the SQL queries and build an HTML dashboard."""
import base64, io, re, sqlite3
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

sql = open("queries.sql").read()
parts = re.split(r"-- name: (\w+)\n", sql)[1:]
queries = dict(zip(parts[::2], parts[1::2]))
con = sqlite3.connect("hospital.db")
r = {k: pd.read_sql(q, con) for k, q in queries.items()}
for k in ("kpis", "by_condition", "by_admission_type"):
    print(k); print(r[k].to_string(index=False))

def img(fig, name):
    fig.tight_layout()
    fig.savefig(f"results/{name}.png", dpi=130)
    buf = io.BytesIO(); fig.savefig(buf, format="png", dpi=110)
    plt.close(fig)
    return f'<img src="data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}">'

C = "#2a6f97"
f, a = plt.subplots(figsize=(7, 4)); d = r["by_condition"]
a.barh(d.medical_condition, d.admissions, color=C); a.invert_yaxis(); a.set_title("Admissions by condition")
h1 = img(f, "admissions_by_condition")
f, a = plt.subplots(figsize=(7, 4)); d = r["monthly"].iloc[1:-1]  # drop partial first and last months
a.plot(pd.to_datetime(d.month), d.admissions, color=C); a.set_title("Monthly admissions")
h2 = img(f, "monthly_admissions")
f, a = plt.subplots(figsize=(7, 4)); d = r["by_condition"]
a.barh(d.medical_condition, d.avg_bill, color="#e07a5f"); a.invert_yaxis(); a.set_title("Average bill by condition ($)")
h3 = img(f, "avg_bill_by_condition")
f, a = plt.subplots(figsize=(7, 4)); d = r["by_age_group"]
a.bar(d.age_group, d.admissions, color=C); a.set_title("Admissions by age group")
h4 = img(f, "admissions_by_age_group")
f, a = plt.subplots(figsize=(7, 4)); d = r["by_admission_type"]
a.pie(d.admissions, labels=d.admission_type, autopct="%1.0f%%"); a.set_title("Admission type")
h5 = img(f, "admission_type")
f, a = plt.subplots(figsize=(7, 4)); d = r["by_insurer"]
a.bar(d.insurance_provider, d.billing_millions, color="#81b29a"); a.set_title("Total billing by insurer ($M)")
h6 = img(f, "billing_by_insurer")

k = r["kpis"].iloc[0]
cards = "".join(f'<div class="card"><b>{v}</b><span>{l}</span></div>' for l, v in [
    ("Admissions", f"{int(k.admissions):,}"), ("Avg length of stay (days)", k.avg_length_of_stay),
    ("Avg bill ($)", f"{int(k.avg_bill):,}"), ("Total billing ($M)", k.total_billing_millions)])
html = f"""<!doctype html><meta charset=utf-8><title>Hospital Patient Analytics</title>
<style>body{{font-family:Arial;background:#f4f6f8;margin:24px}}h1{{color:#1b4965}}
.cards{{display:flex;gap:16px}}.card{{background:#fff;padding:16px 24px;border-radius:8px;flex:1}}
.card b{{display:block;font-size:26px;color:#2a6f97}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px}}
.grid div{{background:#fff;padding:8px;border-radius:8px}}img{{width:100%}}</style>
<h1>Hospital Patient Analytics Dashboard</h1><div class=cards>{cards}</div>
<div class=grid><div>{h1}</div><div>{h2}</div><div>{h3}</div><div>{h4}</div><div>{h5}</div><div>{h6}</div></div>"""
open("results/dashboard.html", "w").write(html)
print("dashboard written")
