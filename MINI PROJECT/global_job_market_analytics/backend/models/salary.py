"""
backend/models/salary.py
Salary model — all salary data access methods.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.config.db import get_db

class SalaryModel:

    @staticmethod
    def get_by_country_role_mode(country_code=None, role_id=None, work_mode='Hybrid'):
        conn = get_db()
        sql = """SELECT s.*, c.name as country_name, r.title as role_title
                 FROM salary_data s
                 JOIN countries c ON s.country_code = c.code
                 JOIN job_roles r ON s.role_id = r.id
                 WHERE s.work_mode = ?"""
        params = [work_mode]
        if country_code: sql += " AND s.country_code=?"; params.append(country_code)
        if role_id:      sql += " AND s.role_id=?";      params.append(role_id)
        rows = conn.execute(sql, params).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def country_comparison(role_id=None, work_mode='Hybrid'):
        conn = get_db()
        sql = """SELECT c.name as country, c.code, c.region,
                        AVG(s.avg_salary_usd) as avg_salary,
                        AVG(s.min_salary_usd) as min_salary,
                        AVG(s.max_salary_usd) as max_salary,
                        AVG(s.avg_bonus_usd)  as avg_bonus
                 FROM salary_data s JOIN countries c ON s.country_code=c.code
                 WHERE s.work_mode=?"""
        params = [work_mode]
        if role_id: sql += " AND s.role_id=?"; params.append(role_id)
        sql += " GROUP BY c.code ORDER BY avg_salary DESC"
        rows = conn.execute(sql, params).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def role_comparison(country_code=None, work_mode='Hybrid'):
        conn = get_db()
        sql = """SELECT r.title as role, r.category,
                        AVG(s.avg_salary_usd) as avg_salary,
                        AVG(s.min_salary_usd) as min_salary,
                        AVG(s.max_salary_usd) as max_salary
                 FROM salary_data s JOIN job_roles r ON s.role_id=r.id
                 WHERE s.work_mode=?"""
        params = [work_mode]
        if country_code: sql += " AND s.country_code=?"; params.append(country_code)
        sql += " GROUP BY r.id ORDER BY avg_salary DESC"
        rows = conn.execute(sql, params).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def workmode_comparison(country_code=None, role_id=None):
        conn = get_db()
        sql = """SELECT work_mode,
                        AVG(avg_salary_usd) as avg_salary,
                        AVG(min_salary_usd) as min_salary,
                        AVG(max_salary_usd) as max_salary,
                        AVG(avg_bonus_usd)  as avg_bonus
                 FROM salary_data WHERE 1=1"""
        params = []
        if country_code: sql += " AND country_code=?"; params.append(country_code)
        if role_id:      sql += " AND role_id=?";      params.append(role_id)
        sql += " GROUP BY work_mode ORDER BY avg_salary DESC"
        rows = conn.execute(sql, params).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def global_stats(work_mode='Hybrid'):
        conn = get_db()
        row = conn.execute("""
            SELECT AVG(avg_salary_usd) as global_avg,
                   MAX(avg_salary_usd) as global_max,
                   MIN(avg_salary_usd) as global_min
            FROM salary_data WHERE work_mode=?
        """, [work_mode]).fetchone()
        conn.close()
        return dict(row) if row else {}
