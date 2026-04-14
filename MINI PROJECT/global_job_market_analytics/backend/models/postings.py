"""
backend/models/postings.py
Job postings model — individual listing data access.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.config.db import get_db

class PostingsModel:

    @staticmethod
    def get_all(limit=50, offset=0):
        conn = get_db()
        rows = conn.execute("""
            SELECT jp.*, c.name as country_name, r.title as role_title
            FROM job_postings jp
            JOIN countries c ON jp.country_code=c.code
            JOIN job_roles r ON jp.role_id=r.id
            ORDER BY jp.posted_date DESC LIMIT ? OFFSET ?
        """, [limit, offset]).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def get_by_country(country_code, limit=20):
        conn = get_db()
        rows = conn.execute("""
            SELECT jp.*, r.title as role_title
            FROM job_postings jp JOIN job_roles r ON jp.role_id=r.id
            WHERE jp.country_code=? ORDER BY jp.salary_usd DESC LIMIT ?
        """, [country_code, limit]).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def company_stats(limit=20):
        conn = get_db()
        rows = conn.execute("""
            SELECT company, COUNT(*) as postings,
                   AVG(salary_usd) as avg_salary,
                   MAX(salary_usd) as max_salary,
                   AVG(applicants)  as avg_applicants
            FROM job_postings GROUP BY company
            ORDER BY avg_salary DESC LIMIT ?
        """, [limit]).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def by_experience_level():
        conn = get_db()
        rows = conn.execute("""
            SELECT experience_level, COUNT(*) as count,
                   AVG(salary_usd) as avg_salary
            FROM job_postings GROUP BY experience_level
            ORDER BY avg_salary DESC
        """).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def monthly_timeline():
        conn = get_db()
        rows = conn.execute("""
            SELECT substr(posted_date,1,7) as month,
                   COUNT(*) as count, AVG(salary_usd) as avg_salary
            FROM job_postings GROUP BY month ORDER BY month
        """).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def total_count():
        conn = get_db()
        n = conn.execute("SELECT COUNT(*) as n FROM job_postings").fetchone()['n']
        conn.close()
        return n
