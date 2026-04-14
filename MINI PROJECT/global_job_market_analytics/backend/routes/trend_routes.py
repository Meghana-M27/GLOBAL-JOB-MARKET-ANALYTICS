"""
backend/routes/trend_routes.py
Trend route handlers — salary and demand trends.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.models     import TrendModel
from backend.middleware import validate_filters, log_request, Timer

def handle_salary_trend(country_code=None, role_id=None):
    with Timer() as t:
        params, errors = validate_filters(country_code, role_id)
        if errors:
            return {'error': errors, 'data': []}
        data = TrendModel.salary_trend(params['country_code'], params['role_id'])
        growth = TrendModel.growth_rate(params['country_code'], params['role_id'])
    log_request('trends/salary', params, t.ms)
    return {'data': data, 'growth_rate_pct': growth, 'years': len(data)}

def handle_demand_trend(country_code=None, role_id=None):
    with Timer() as t:
        params, errors = validate_filters(country_code, role_id)
        if errors:
            return {'error': errors, 'data': []}
        data = TrendModel.demand_trend(params['country_code'], params['role_id'])
    log_request('trends/demand', params, t.ms)
    return {'data': data, 'years': len(data)}

def handle_demand_by_role(year=2025):
    data = TrendModel.demand_by_role(year)
    log_request('trends/demand-by-role', {'year': year})
    return {'data': data, 'year': year}

def handle_multi_country_trend(role_id=None):
    params, errors = validate_filters(role_id=role_id)
    if errors:
        return {'error': errors, 'data': []}
    data = TrendModel.salary_trend_by_country(params['role_id'])
    log_request('trends/multi-country', params)
    return {'data': data}
