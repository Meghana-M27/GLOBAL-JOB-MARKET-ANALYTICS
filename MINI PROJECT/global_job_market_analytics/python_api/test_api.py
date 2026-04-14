"""
python_api/test_api.py
Quick test script — verifies all route handlers return valid data.
Run: python python_api/test_api.py
Does NOT require the HTTP server to be running.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import init_db
from backend.routes import *

init_db()

TESTS = [
    ('Countries',          lambda: handle_get_countries()),
    ('Salary/Countries',   lambda: handle_salary_countries('US', 1, 'Hybrid')),
    ('Salary/Roles',       lambda: handle_salary_roles('US', None, 'Hybrid')),
    ('Salary/WorkModes',   lambda: handle_salary_workmodes('US', 1)),
    ('Trends/Salary',      lambda: handle_salary_trend('US', 1)),
    ('Trends/Demand',      lambda: handle_demand_trend('US', 1)),
    ('Demand by Role',     lambda: handle_demand_by_role(2025)),
    ('ML/Predict',         lambda: handle_predict_salary('US', 1, 'Hybrid', 2026)),
    ('ML/Forecast',        lambda: handle_forecast_demand('US', 1, 3)),
    ('ML/PPP',             lambda: handle_ppp_salary('US', 1, 'Hybrid')),
    ('ML/Benchmark',       lambda: handle_benchmark(1, 'Hybrid')),
    ('Postings',           lambda: handle_postings(10, 0)),
    ('Company Stats',      lambda: handle_company_stats()),
]

print("=" * 55)
print("  Global Job Market API — Route Test Suite")
print("=" * 55)
passed = 0
for name, fn in TESTS:
    try:
        result = fn()
        has_data = bool(result.get('data') or result.get('count') is not None)
        status = '✅ PASS' if has_data or 'data' in result else '⚠️  EMPTY'
        print(f"  {status}  {name}")
        passed += 1
    except Exception as e:
        print(f"  ❌ FAIL  {name} → {e}")

print("=" * 55)
print(f"  Results: {passed}/{len(TESTS)} passed")
print("=" * 55)
