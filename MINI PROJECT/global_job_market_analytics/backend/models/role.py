"""
backend/models/role.py
Job role model — role data and skills access.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.config.db import get_db

class RoleModel:

    @staticmethod
    def get_all():
        conn = get_db()
        rows = conn.execute("SELECT * FROM job_roles ORDER BY title").fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def get_by_id(role_id):
        conn = get_db()
        row = conn.execute("SELECT * FROM job_roles WHERE id=?", [role_id]).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def get_categories():
        conn = get_db()
        rows = conn.execute("SELECT DISTINCT category FROM job_roles ORDER BY category").fetchall()
        conn.close()
        return [r['category'] for r in rows]

    @staticmethod
    def get_skills(role_id):
        conn = get_db()
        rows = conn.execute("""
            SELECT skill_name, skill_type, percentage
            FROM skills WHERE role_id=? ORDER BY percentage DESC
        """, [role_id]).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def get_top_by_salary(country_code=None, work_mode='Hybrid', limit=10):
        conn = get_db()
        sql = """SELECT r.title, r.category, AVG(s.avg_salary_usd) as avg_salary
                 FROM salary_data s JOIN job_roles r ON s.role_id=r.id
                 WHERE s.work_mode=?"""
        params = [work_mode]
        if country_code: sql += " AND s.country_code=?"; params.append(country_code)
        sql += f" GROUP BY r.id ORDER BY avg_salary DESC LIMIT {limit}"
        rows = conn.execute(sql, params).fetchall()
        conn.close()
        return [dict(r) for r in rows]
