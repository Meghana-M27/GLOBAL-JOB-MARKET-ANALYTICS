"""
database.py — Python DB layer
Reads schema.sql + loads all CSVs into SQLite
"""
import sqlite3, csv, os

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE, 'data', 'job_market.db')
SQL_PATH = os.path.join(BASE, 'data', 'sql', 'schema.sql')
CSV_DIR  = os.path.join(BASE, 'data', 'csv')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn

def _load_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_connection()
    c = conn.cursor()

    with open(SQL_PATH) as f:
        c.executescript(f.read())

    # Load countries
    rows = _load_csv(f'{CSV_DIR}/countries.csv')
    c.executemany(
        "INSERT OR IGNORE INTO countries VALUES (?,?,?,?,?,?,datetime('now'))",
        [(r['code'],r['name'],r['region'],r['currency'],float(r['gdp_per_capita']),int(r['population'])) for r in rows]
    )

    # Load job_roles
    rows = _load_csv(f'{CSV_DIR}/job_roles.csv')
    c.executemany(
        "INSERT OR IGNORE INTO job_roles VALUES (?,?,?,?,?,datetime('now'))",
        [(int(r['id']),r['title'],r['category'],r['experience_level'],int(r['avg_years_exp'])) for r in rows]
    )

    # Load salary_data
    rows = _load_csv(f'{CSV_DIR}/salary_data.csv')
    c.executemany(
        "INSERT OR IGNORE INTO salary_data(country_code,role_id,work_mode,avg_salary_usd,min_salary_usd,max_salary_usd,avg_bonus_usd) VALUES (?,?,?,?,?,?,?)",
        [(r['country_code'],int(r['role_id']),r['work_mode'],float(r['avg_salary_usd']),float(r['min_salary_usd']),float(r['max_salary_usd']),float(r['avg_bonus_usd'])) for r in rows]
    )

    # Load salary_trends
    rows = _load_csv(f'{CSV_DIR}/salary_trends.csv')
    c.executemany(
        "INSERT OR IGNORE INTO salary_trends(country_code,role_id,year,avg_salary_usd,q3_salary_usd,q1_salary_usd) VALUES (?,?,?,?,?,?)",
        [(r['country_code'],int(r['role_id']),int(r['year']),float(r['avg_salary_usd']),float(r['q3_salary_usd']),float(r['q1_salary_usd'])) for r in rows]
    )

    # Load demand_trends
    rows = _load_csv(f'{CSV_DIR}/demand_trends.csv')
    c.executemany(
        "INSERT OR IGNORE INTO demand_trends(country_code,role_id,year,demand_index,job_postings_thousands,remote_postings_thousands) VALUES (?,?,?,?,?,?)",
        [(r['country_code'],int(r['role_id']),int(r['year']),float(r['demand_index']),float(r['job_postings_thousands']),float(r['remote_postings_thousands'])) for r in rows]
    )

    # Load skills
    rows = _load_csv(f'{CSV_DIR}/skills.csv')
    c.executemany(
        "INSERT OR IGNORE INTO skills(role_id,skill_name,skill_type,percentage) VALUES (?,?,?,?)",
        [(int(r['role_id']),r['skill_name'],r['skill_type'],float(r['percentage'])) for r in rows]
    )

    # Load job_postings
    rows = _load_csv(f'{CSV_DIR}/job_postings.csv')
    c.executemany(
        "INSERT OR IGNORE INTO job_postings(company,country_code,role_id,work_mode,salary_usd,experience_level,posted_date,applicants) VALUES (?,?,?,?,?,?,?,?)",
        [(r['company'],r['country_code'],int(r['role_id']),r['work_mode'],float(r['salary_usd']),r['experience_level'],r['posted_date'],int(r['applicants'])) for r in rows]
    )

    # Load cost_of_living
    rows = _load_csv(f'{CSV_DIR}/cost_of_living.csv')
    c.executemany(
        "INSERT OR IGNORE INTO cost_of_living VALUES (?,?,?,?,?,?)",
        [(r['country_code'],float(r['col_index']),float(r['avg_rent_usd']),float(r['meal_cost_usd']),float(r['transport_monthly_usd']),float(r['income_tax_rate'])) for r in rows]
    )

    conn.commit()
    conn.close()
    print("Database initialised from CSVs.")

if __name__ == '__main__':
    init_db()
