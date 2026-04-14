"""
python_api/api.py
Standalone REST API layer for the Global Job Market Analysis System.
Exposes all analytics as HTTP JSON endpoints.
Run: python python_api/api.py
Endpoints available at: http://localhost:8000/api/...
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from database import init_db
from backend.routes import (
    handle_salary_countries, handle_salary_roles, handle_salary_workmodes,
    handle_salary_trend, handle_demand_trend, handle_demand_by_role,
    handle_predict_salary, handle_forecast_demand, handle_ppp_salary,
    handle_skill_gap, handle_benchmark,
    handle_get_countries, handle_postings, handle_company_stats
)
from backend.middleware import log_request

PORT = 8000

ROUTES = {
    '/api/countries':            lambda p: handle_get_countries(),
    '/api/salary/countries':     lambda p: handle_salary_countries(p.get('country',''), p.get('role',''), p.get('mode','Hybrid')),
    '/api/salary/roles':         lambda p: handle_salary_roles(p.get('country',''), p.get('role',''), p.get('mode','Hybrid')),
    '/api/salary/workmodes':     lambda p: handle_salary_workmodes(p.get('country',''), p.get('role','')),
    '/api/trends/salary':        lambda p: handle_salary_trend(p.get('country',''), p.get('role','')),
    '/api/trends/demand':        lambda p: handle_demand_trend(p.get('country',''), p.get('role','')),
    '/api/trends/demand-by-role':lambda p: handle_demand_by_role(int(p.get('year',2025))),
    '/api/ml/predict':           lambda p: handle_predict_salary(p.get('country','US'), p.get('role',1), p.get('mode','Hybrid'), int(p.get('year',2026))),
    '/api/ml/forecast':          lambda p: handle_forecast_demand(p.get('country','US'), p.get('role',1), int(p.get('horizon',3))),
    '/api/ml/ppp':               lambda p: handle_ppp_salary(p.get('country','US'), p.get('role',1), p.get('mode','Hybrid')),
    '/api/ml/benchmark':         lambda p: handle_benchmark(p.get('role',1), p.get('mode','Hybrid')),
    '/api/postings':             lambda p: handle_postings(int(p.get('limit',50)), int(p.get('offset',0))),
    '/api/postings/companies':   lambda p: handle_company_stats(),
}

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = {k: v[0] for k, v in parse_qs(parsed.query).items()}
        handler = ROUTES.get(parsed.path)

        if not handler:
            self._respond(404, {'error': f'Endpoint {parsed.path} not found', 'available': list(ROUTES.keys())})
            return

        try:
            result = handler(params)
            self._respond(200, result)
        except Exception as e:
            self._respond(500, {'error': str(e)})

    def _respond(self, code, data):
        body = json.dumps(data, default=str, indent=2).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(body))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        log_request(self.path)

def run():
    init_db()
    print(f"[API] Global Job Market REST API running at http://localhost:{PORT}/api/")
    print(f"[API] Available endpoints:")
    for route in ROUTES:
        print(f"       GET {route}")
    HTTPServer(('0.0.0.0', PORT), APIHandler).serve_forever()

if __name__ == '__main__':
    run()
