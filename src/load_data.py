# load_data.py - Generate synthetic HR dataset and load into SQLite
import sqlite3
import pandas as pd
import numpy as np
import os
import random

DEPARTMENTS = ['Engineering', 'Sales', 'HR', 'Finance', 'Marketing', 'Operations']

JOB_ROLES = {
    'Engineering': ['Software Engineer', 'QA Engineer', 'DevOps Engineer', 'Data Analyst'],
    'Sales': ['Sales Executive', 'Account Manager', 'Sales Lead'],
    'HR': ['HR Specialist', 'Recruiter', 'HR Manager'],
    'Finance': ['Financial Analyst', 'Accountant', 'Finance Manager'],
    'Marketing': ['Marketing Analyst', 'Content Writer', 'Brand Manager'],
    'Operations': ['Operations Analyst', 'Supply Chain Lead', 'Logistics Coordinator']
}

GENDERS = ['Male', 'Female']

NAMES = [
    'Priya Sharma', 'Rahul Verma', 'Anita Singh', 'Kiran Patel', 'Suresh Rao',
    'Meena Nair', 'Arjun Reddy', 'Divya Kumar', 'Ravi Iyer', 'Sneha Gupta',
    'Vijay Pillai', 'Rekha Joshi', 'Arun Desai', 'Kavya Bhat', 'Manish Shah',
    'Deepa Menon', 'Sanjay Mishra', 'Lakshmi Rao', 'Rohit Saxena', 'Pooja Tiwari'
]


def generate_dataset(n=1000, seed=42):
    np.random.seed(seed)
    random.seed(seed)
    rows = []
    for i in range(n):
        dept = random.choice(DEPARTMENTS)
        role = random.choice(JOB_ROLES[dept])
        gender = random.choice(GENDERS)
        age = int(np.random.normal(35, 8))
        age = max(22, min(60, age))
        base_salary = {
            'Engineering': 75000, 'Finance': 70000, 'Sales': 55000,
            'HR': 50000, 'Marketing': 52000, 'Operations': 48000
        }[dept]
        salary = round(base_salary + np.random.normal(0, 12000), 2)
        salary = max(30000, salary)
        years = int(np.random.exponential(4))
        years = max(0, min(25, years))
        perf = round(np.clip(np.random.normal(3.5, 0.8), 1.0, 5.0), 1)
        sat = round(np.clip(np.random.normal(3.2, 0.9), 1.0, 5.0), 1)
        wlb = random.choices([1, 2, 3, 4], weights=[10, 25, 40, 25])[0]
        overtime = 'Yes' if sat < 2.5 or perf > 4.2 else random.choice(['Yes', 'No'])
        hours = int(np.random.normal(170, 20))
        hours = max(120, min(250, hours))
        p_leave = 0.05
        if sat < 2.5: p_leave += 0.25
        if overtime == 'Yes': p_leave += 0.10
        if years < 2: p_leave += 0.10
        attrition = 'Yes' if random.random() < p_leave else 'No'
        rows.append({
            'name': random.choice(NAMES),
            'age': age,
            'gender': gender,
            'department': dept,
            'job_role': role,
            'salary': salary,
            'years_at_company': years,
            'performance_score': perf,
            'satisfaction_score': sat,
            'work_life_balance': wlb,
            'overtime': overtime,
            'attrition': attrition,
            'monthly_hours': hours
        })
    return pd.DataFrame(rows)


def load_to_sqlite(df, db_path='hr_analytics.db'):
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/employees.csv', index=False)
    print(f'CSV saved: data/employees.csv ({len(df)} records)')
    conn = sqlite3.connect(db_path)
    with open('sql/schema.sql') as f:
        conn.executescript(f.read())
    df.to_sql('employees', conn, if_exists='replace', index_label='emp_id')
    conn.commit()
    count = conn.execute('SELECT COUNT(*) FROM employees').fetchone()[0]
    conn.close()
    print(f'SQLite loaded: {db_path} ({count} rows in employees table)')


if __name__ == '__main__':
    print('Generating HR dataset...')
    df = generate_dataset(1000)
    load_to_sqlite(df)
    print('Dataset preview:')
    print(df.describe())
