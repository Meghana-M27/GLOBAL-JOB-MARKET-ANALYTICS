"""
backend/routes/ml_routes.py
ML prediction route handlers.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ml.analytics       import predict_salary, forecast_demand, cost_adjusted_salary, skill_gap_score, salary_benchmark
from backend.middleware import validate_filters, validate_year, log_request, Timer

def handle_predict_salary(country_code, role_id, work_mode='Hybrid', year=2026):
    with Timer() as t:
        params, errors = validate_filters(country_code, role_id, work_mode)
        yr, err = validate_year(year)
        if err: errors.append(err)
        if errors:
            return {'error': errors}
        result = predict_salary(params['country_code'], params['role_id'], params['work_mode'], yr or 2026)
    log_request('ml/predict-salary', {**params, 'year': yr}, t.ms)
    return {'data': result}

def handle_forecast_demand(country_code, role_id, horizon=3):
    with Timer() as t:
        params, errors = validate_filters(country_code, role_id)
        try:
            h = max(1, min(5, int(horizon)))
        except:
            h = 3
        if errors:
            return {'error': errors}
        result = forecast_demand(params['country_code'], params['role_id'], h)
    log_request('ml/forecast-demand', {**params, 'horizon': h}, t.ms)
    return {'data': result}

def handle_ppp_salary(country_code, role_id, work_mode='Hybrid'):
    params, errors = validate_filters(country_code, role_id, work_mode)
    if errors:
        return {'error': errors}
    result = cost_adjusted_salary(params['country_code'], params['role_id'], params['work_mode'])
    log_request('ml/ppp', params)
    return {'data': result}

def handle_skill_gap(role_id, user_skills: list):
    params, errors = validate_filters(role_id=role_id)
    if errors:
        return {'error': errors}
    result = skill_gap_score(params['role_id'], user_skills)
    log_request('ml/skill-gap', {'role_id': role_id, 'skills': user_skills})
    return {'data': result}

def handle_benchmark(role_id, work_mode='Hybrid'):
    params, errors = validate_filters(role_id=role_id, work_mode=work_mode)
    if errors:
        return {'error': errors}
    result = salary_benchmark(params['role_id'], params['work_mode'])
    log_request('ml/benchmark', params)
    return {'data': result}
