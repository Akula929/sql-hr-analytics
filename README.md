# HR Analytics Dashboard | SQL + Python

End-to-end HR data analytics pipeline using SQL, Python, and Pandas with an interactive Matplotlib/Seaborn dashboard.

---

## Overview

This project analyzes a company's HR dataset to uncover insights around:
- Attrition patterns — who is leaving and why
- Salary distributions by department and role
- Performance vs. satisfaction correlation
- Department headcount trends over time

Built with a real-world pipeline: raw CSV → SQLite → SQL analytics → Python visualizations → exportable dashboard.

---

## Project Structure

```
sql-hr-analytics/
├── data/
│   └── employees.csv          # Synthetic HR dataset (1000 employees)
├── sql/
│   ├── schema.sql             # Table definitions
│   └── queries.sql            # All analytics queries
├── src/
│   ├── load_data.py           # CSV → SQLite ingestion
│   ├── analytics.py           # Python analytics layer
│   └── dashboard.py          # Visualization dashboard
├── requirements.txt
└── README.md
```

---

## Key SQL Queries

- Attrition rate by department
- Average salary by role and gender
- Top 10 highest performers by department
- Employees at risk of leaving (low satisfaction + high workload)

---

## Visualizations

| Chart | Insight |
|---|---|
| Attrition Rate Bar | Which depts have highest turnover |
| Salary Heatmap | Pay equity across roles |
| Performance Distribution | Bell curve of ratings |
| Tenure vs Satisfaction | Correlation scatter |

---

## Setup

```bash
git clone https://github.com/Akula929/sql-hr-analytics
cd sql-hr-analytics
pip install -r requirements.txt
python src/load_data.py       # Load data into SQLite
python src/analytics.py       # Run SQL analytics
python src/dashboard.py       # Launch dashboard
```

---

## Tech Stack

- Python 3.10
- SQLite3
- Pandas
- Matplotlib
- Seaborn
- SQL

---

## What I Learned

- Writing complex SQL (CTEs, window functions, GROUP BY)
- Building ETL pipelines from raw CSV to structured DB
- Visualizing business insights from structured data
