"""
backend/routes/country_routes.py
Country and job postings route handlers.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.models     import CountryModel, PostingsModel
from backend.middleware import log_request, Timer

def handle_get_countries():
    data = CountryModel.get_all()
    return {'data': data, 'count': len(data)}

def handle_country_detail(code):
    with Timer() as t:
        country = CountryModel.get_by_code(code)
        col     = CountryModel.get_cost_of_living(code)
    log_request(f'countries/{code}', None, t.ms)
    if not country:
        return {'error': f'Country {code} not found'}
    return {'data': {**country, 'cost_of_living': col}}

def handle_postings(limit=50, offset=0):
    with Timer() as t:
        data  = PostingsModel.get_all(limit=limit, offset=offset)
        total = PostingsModel.total_count()
    log_request('postings', {'limit': limit, 'offset': offset}, t.ms)
    return {'data': data, 'total': total, 'limit': limit, 'offset': offset}

def handle_company_stats():
    data = PostingsModel.company_stats()
    return {'data': data}

def handle_postings_timeline():
    data = PostingsModel.monthly_timeline()
    return {'data': data}

def handle_experience_stats():
    data = PostingsModel.by_experience_level()
    return {'data': data}
