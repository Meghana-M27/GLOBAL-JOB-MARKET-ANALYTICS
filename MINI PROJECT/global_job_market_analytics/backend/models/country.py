"""
backend/models/country.py
Country model — queries and data access layer.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.config.db import get_db

class CountryModel:

    @staticmethod
    def get_all():
        conn = get_db()
        rows = conn.execute("SELECT * FROM countries ORDER BY name").fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def get_by_code(code):
        conn = get_db()
        row = conn.execute("SELECT * FROM countries WHERE code=?", [code]).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def get_regions():
        conn = get_db()
        rows = conn.execute("SELECT DISTINCT region FROM countries ORDER BY region").fetchall()
        conn.close()
        return [r['region'] for r in rows]

    @staticmethod
    def get_with_avg_salary(work_mode='Hybrid'):
        conn = get_db()
        rows = conn.execute("""
            SELECT c.code, c.name, c.region, c.gdp_per_capita,
                   AVG(s.avg_salary_usd) as avg_salary,
                   AVG(s.min_salary_usd) as min_salary,
                   AVG(s.max_salary_usd) as max_salary
            FROM countries c
            LEFT JOIN salary_data s ON c.code = s.country_code
            WHERE s.work_mode = ?
            GROUP BY c.code ORDER BY avg_salary DESC
        """, [work_mode]).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def get_cost_of_living(code):
        conn = get_db()
        row = conn.execute("SELECT * FROM cost_of_living WHERE country_code=?", [code]).fetchone()
        conn.close()
        return dict(row) if row else None
