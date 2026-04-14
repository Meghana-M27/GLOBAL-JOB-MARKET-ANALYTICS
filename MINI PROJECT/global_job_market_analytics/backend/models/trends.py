"""
backend/models/trends.py
Trend model — salary and demand trend data access.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.config.db import get_db

class TrendModel:

    @staticmethod
    def salary_trend(country_code=None, role_id=None):
        conn = get_db()
        sql = "SELECT year, AVG(avg_salary_usd) as avg, AVG(q1_salary_usd) as q1, AVG(q3_salary_usd) as q3 FROM salary_trends WHERE 1=1"
        params = []
        if country_code: sql += " AND country_code=?"; params.append(country_code)
        if role_id:      sql += " AND role_id=?";      params.append(role_id)
        sql += " GROUP BY year ORDER BY year"
        rows = conn.execute(sql, params).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def salary_trend_by_country(role_id=None):
        conn = get_db()
        sql = """SELECT t.year, AVG(t.avg_salary_usd) as avg, c.name as country, c.code
                 FROM salary_trends t JOIN countries c ON t.country_code=c.code WHERE 1=1"""
        params = []
        if role_id: sql += " AND t.role_id=?"; params.append(role_id)
        sql += " GROUP BY t.year, t.country_code ORDER BY t.year"
        rows = conn.execute(sql, params).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def demand_trend(country_code=None, role_id=None):
        conn = get_db()
        sql = """SELECT year, AVG(demand_index) as idx,
                        AVG(job_postings_thousands) as postings,
                        AVG(remote_postings_thousands) as remote_postings
                 FROM demand_trends WHERE 1=1"""
        params = []
        if country_code: sql += " AND country_code=?"; params.append(country_code)
        if role_id:      sql += " AND role_id=?";      params.append(role_id)
        sql += " GROUP BY year ORDER BY year"
        rows = conn.execute(sql, params).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def demand_by_role(year=2025):
        conn = get_db()
        rows = conn.execute("""
            SELECT r.title as role, r.category,
                   AVG(d.demand_index) as idx,
                   AVG(d.job_postings_thousands) as postings
            FROM demand_trends d JOIN job_roles r ON d.role_id=r.id
            WHERE d.year=? GROUP BY d.role_id ORDER BY idx DESC
        """, [year]).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def growth_rate(country_code=None, role_id=None):
        rows = TrendModel.salary_trend(country_code, role_id)
        if len(rows) < 2:
            return 0
        first = rows[0]['avg']
        last  = rows[-1]['avg']
        return round((last - first) / first * 100, 1) if first else 0
