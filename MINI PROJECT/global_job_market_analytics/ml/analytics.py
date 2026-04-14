"""
ml/analytics.py
Python analytics engine — salary prediction, growth forecasting,
skill gap scoring, cost-adjusted salary, clustering insights.
No external ML libs needed — uses pure math + statistics.
"""
import sqlite3, os, math, statistics
from database import get_connection

# ── SALARY PREDICTOR (Linear regression via least squares) ──────────────────
def predict_salary(country_code, role_id, work_mode='Hybrid', year=2026):
    conn = get_connection()
    rows = conn.execute("""
        SELECT year, avg_salary_usd FROM salary_trends
        WHERE country_code=? AND role_id=?
        ORDER BY year
    """, [country_code, role_id]).fetchall()
    conn.close()
    if len(rows) < 3:
        return None
    xs = [r['year'] for r in rows]
    ys = [r['avg_salary_usd'] for r in rows]
    n  = len(xs)
    mx = sum(xs)/n;  my = sum(ys)/n
    num = sum((x-mx)*(y-my) for x,y in zip(xs,ys))
    den = sum((x-mx)**2 for x in xs)
    if den == 0: return None
    slope = num/den
    intercept = my - slope*mx
    predicted = slope*year + intercept
    mode_factor = {'Onsite':0.96,'Hybrid':1.0,'Remote':1.03}.get(work_mode,1.0)
    return {
        'predicted_salary': round(predicted * mode_factor),
        'year': year,
        'slope_per_year': round(slope,2),
        'growth_rate_pct': round(slope/my*100,2),
        'country_code': country_code,
        'role_id': role_id,
        'work_mode': work_mode,
        'r_squared': _r_squared(xs, ys, slope, intercept)
    }

def _r_squared(xs, ys, slope, intercept):
    y_mean = sum(ys)/len(ys)
    ss_res = sum((y - (slope*x+intercept))**2 for x,y in zip(xs,ys))
    ss_tot = sum((y - y_mean)**2 for y in ys)
    return round(1 - ss_res/ss_tot, 4) if ss_tot else 0

# ── DEMAND FORECASTING (Moving average + trend) ─────────────────────────────
def forecast_demand(country_code, role_id, horizon=3):
    conn = get_connection()
    rows = conn.execute("""
        SELECT year, demand_index, job_postings_thousands FROM demand_trends
        WHERE country_code=? AND role_id=?
        ORDER BY year
    """, [country_code, role_id]).fetchall()
    conn.close()
    if len(rows) < 3:
        return None
    idxs = [r['demand_index'] for r in rows]
    posts = [r['job_postings_thousands'] for r in rows]
    last_year = rows[-1]['year']
    window = 3
    ma = sum(idxs[-window:]) / window
    recent_growth = (idxs[-1] - idxs[-window]) / idxs[-window] / window
    forecasts = []
    for h in range(1, horizon+1):
        proj_idx   = round(ma * (1 + recent_growth)**h, 1)
        proj_posts = round(posts[-1] * (1 + recent_growth)**h, 1)
        forecasts.append({'year': last_year+h, 'demand_index': proj_idx, 'postings_k': proj_posts})
    status = 'Growing' if recent_growth > 0.04 else 'Declining' if recent_growth < -0.02 else 'Stable'
    return {
        'current_index': idxs[-1],
        'growth_rate_pct': round(recent_growth*100, 2),
        'status': status,
        'forecasts': forecasts,
        'confidence': 'High' if len(rows) >= 8 else 'Medium'
    }

# ── COST-ADJUSTED SALARY (Purchasing Power Parity) ──────────────────────────
def cost_adjusted_salary(country_code, role_id, work_mode='Hybrid'):
    conn = get_connection()
    sal = conn.execute("""
        SELECT avg_salary_usd FROM salary_data
        WHERE country_code=? AND role_id=? AND work_mode=?
    """, [country_code, role_id, work_mode]).fetchone()
    col = conn.execute("""
        SELECT col_index, avg_rent_usd, income_tax_rate FROM cost_of_living
        WHERE country_code=?
    """, [country_code]).fetchone()
    conn.close()
    if not sal or not col: return None
    raw = sal['avg_salary_usd']
    after_tax = raw * (1 - col['income_tax_rate'])
    annual_housing = col['avg_rent_usd'] * 12
    disposable = after_tax - annual_housing
    ppp_adjusted = round(raw * 100 / col['col_index'])
    return {
        'raw_salary': round(raw),
        'after_tax': round(after_tax),
        'annual_housing_cost': round(annual_housing),
        'disposable_income': round(disposable),
        'ppp_adjusted_salary': ppp_adjusted,
        'col_index': col['col_index'],
        'income_tax_rate': col['income_tax_rate']
    }

# ── SKILL GAP SCORE ─────────────────────────────────────────────────────────
def skill_gap_score(role_id, user_skills: list):
    conn = get_connection()
    required = conn.execute(
        "SELECT skill_name, skill_type, percentage FROM skills WHERE role_id=?", [role_id]
    ).fetchall()
    conn.close()
    if not required: return None
    user_lower = [s.lower() for s in user_skills]
    matched = []; missing = []; total_weight = 0; matched_weight = 0
    for row in required:
        w = row['percentage']
        total_weight += w
        if any(row['skill_name'].lower() in u or u in row['skill_name'].lower() for u in user_lower):
            matched.append({'skill': row['skill_name'], 'weight': w, 'type': row['skill_type']})
            matched_weight += w
        else:
            missing.append({'skill': row['skill_name'], 'weight': w, 'type': row['skill_type']})
    score = round(matched_weight / total_weight * 100, 1) if total_weight else 0
    return {
        'match_score': score,
        'matched_skills': matched,
        'missing_skills': missing,
        'readiness': 'High' if score >= 70 else 'Medium' if score >= 40 else 'Low'
    }

# ── SALARY BENCHMARKING ──────────────────────────────────────────────────────
def salary_benchmark(role_id, work_mode='Hybrid'):
    conn = get_connection()
    rows = conn.execute("""
        SELECT s.avg_salary_usd, c.name as country, c.region
        FROM salary_data s JOIN countries c ON s.country_code=c.code
        WHERE s.role_id=? AND s.work_mode=?
        ORDER BY s.avg_salary_usd DESC
    """, [role_id, work_mode]).fetchall()
    conn.close()
    if not rows: return None
    vals = [r['avg_salary_usd'] for r in rows]
    return {
        'global_avg': round(statistics.mean(vals)),
        'global_median': round(statistics.median(vals)),
        'global_max': round(max(vals)),
        'global_min': round(min(vals)),
        'std_dev': round(statistics.stdev(vals)) if len(vals) > 1 else 0,
        'top_country': dict(rows[0]),
        'rankings': [{'country': r['country'], 'region': r['region'], 'salary': round(r['avg_salary_usd'])} for r in rows]
    }

# ── TOP PAYING ROLES ─────────────────────────────────────────────────────────
def top_paying_roles(country_code=None, work_mode='Hybrid', limit=10):
    conn = get_connection()
    sql = """
        SELECT r.title, r.category, AVG(s.avg_salary_usd) as avg_sal,
               AVG(s.max_salary_usd) as max_sal
        FROM salary_data s JOIN job_roles r ON s.role_id=r.id
        WHERE s.work_mode=?
    """
    p = [work_mode]
    if country_code: sql += " AND s.country_code=?"; p.append(country_code)
    sql += f" GROUP BY r.id ORDER BY avg_sal DESC LIMIT {limit}"
    rows = conn.execute(sql, p).fetchall()
    conn.close()
    return [{'role': r['title'], 'category': r['category'],
             'avg_salary': round(r['avg_sal']), 'max_salary': round(r['max_sal'])} for r in rows]

# ── COMPANY INSIGHTS (from job postings) ────────────────────────────────────
def company_insights(limit=10):
    conn = get_connection()
    rows = conn.execute("""
        SELECT company, COUNT(*) as postings, AVG(salary_usd) as avg_sal,
               AVG(applicants) as avg_applicants
        FROM job_postings
        GROUP BY company ORDER BY avg_sal DESC LIMIT ?
    """, [limit]).fetchall()
    conn.close()
    return [{'company': r['company'], 'postings': r['postings'],
             'avg_salary': round(r['avg_sal']), 'avg_applicants': round(r['avg_applicants'])} for r in rows]

# ── SUMMARY STATS ────────────────────────────────────────────────────────────
def summary_stats():
    conn = get_connection()
    total_postings   = conn.execute("SELECT COUNT(*) as n FROM job_postings").fetchone()['n']
    total_countries  = conn.execute("SELECT COUNT(*) as n FROM countries").fetchone()['n']
    total_roles      = conn.execute("SELECT COUNT(*) as n FROM job_roles").fetchone()['n']
    global_avg_sal   = conn.execute("SELECT AVG(avg_salary_usd) as v FROM salary_data WHERE work_mode='Hybrid'").fetchone()['v']
    highest_sal_role = conn.execute("""
        SELECT r.title, AVG(s.avg_salary_usd) as avg FROM salary_data s
        JOIN job_roles r ON s.role_id=r.id WHERE s.work_mode='Hybrid'
        GROUP BY r.id ORDER BY avg DESC LIMIT 1
    """).fetchone()
    conn.close()
    return {
        'total_postings': total_postings,
        'total_countries': total_countries,
        'total_roles': total_roles,
        'global_avg_salary': round(global_avg_sal or 0),
        'highest_paying_role': dict(highest_sal_role) if highest_sal_role else {}
    }

if __name__ == '__main__':
    print("=== ANALYTICS TEST ===")
    print("Predict US SWE 2026:", predict_salary('US',1,'Hybrid',2026))
    print("Demand forecast IN DS:", forecast_demand('IN',3))
    print("PPP US AI Eng:", cost_adjusted_salary('US',5,'Hybrid'))
    print("Skill gap score:", skill_gap_score(3, ['Python','SQL','Communication']))
    print("Benchmark SWE Hybrid:", salary_benchmark(1,'Hybrid'))
    print("Summary:", summary_stats())
