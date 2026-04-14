"""
backend/routes/salary_routes.py
Salary data route handlers — called by app.py or REST layer.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.models  import SalaryModel
from backend.middleware import validate_filters, log_request, Timer

def handle_salary_countries(country_code=None, role_id=None, work_mode='Hybrid'):
    with Timer() as t:
        params, errors = validate_filters(country_code, role_id, work_mode)
        if errors:
            return {'error': errors, 'data': []}
        data = SalaryModel.country_comparison(params['role_id'], params['work_mode'])
    log_request('salary/countries', params, t.ms)
    return {'data': data, 'count': len(data), 'work_mode': work_mode}

def handle_salary_roles(country_code=None, role_id=None, work_mode='Hybrid'):
    with Timer() as t:
        params, errors = validate_filters(country_code, role_id, work_mode)
        if errors:
            return {'error': errors, 'data': []}
        data = SalaryModel.role_comparison(params['country_code'], params['work_mode'])
    log_request('salary/roles', params, t.ms)
    return {'data': data, 'count': len(data)}

def handle_salary_workmodes(country_code=None, role_id=None):
    with Timer() as t:
        params, errors = validate_filters(country_code, role_id)
        if errors:
            return {'error': errors, 'data': []}
        data = SalaryModel.workmode_comparison(params['country_code'], params['role_id'])
    log_request('salary/workmodes', params, t.ms)
    return {'data': data}

def handle_salary_global_stats(work_mode='Hybrid'):
    data = SalaryModel.global_stats(work_mode)
    log_request('salary/stats', {'work_mode': work_mode})
    return {'data': data}
