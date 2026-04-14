# 🌍 Global Job Market Analysis System — Enterprise Edition

## Quick Start
```bash
pip install streamlit plotly pandas
python run.py          # → http://localhost:8501
python run.py --api    # → http://localhost:8000/api/
python run.py --test   # Run 82 unit tests
python run.py --info   # Show full project structure
```

## Project Structure — 60+ Files, Zero Empty Folders

```
gjm_enterprise/
├── run.py                    ← Master entry point
├── app.py                    ← Streamlit dashboard (8 tabs)
├── database.py               ← SQLite engine
├── requirements.txt
├── README.md
│
├── ml/
│   └── analytics.py          ← ML engine: predict, forecast, PPP, skill gap
│
├── backend/
│   ├── config/db.py          ← DB connection config
│   ├── config/settings.py    ← App constants
│   ├── models/country.py     ← Country data access
│   ├── models/salary.py      ← Salary queries
│   ├── models/role.py        ← Role + skills queries
│   ├── models/trends.py      ← Trend data queries
│   ├── models/postings.py    ← Job postings queries
│   ├── middleware/logger.py  ← Request logging
│   ├── middleware/validator.py ← Input validation
│   ├── middleware/cache.py   ← In-memory cache
│   ├── routes/salary_routes.py
│   ├── routes/trend_routes.py
│   ├── routes/ml_routes.py
│   ├── routes/country_routes.py
│   ├── utils/helpers.py      ← Format, paginate, classify
│   ├── utils/statistics.py   ← Mean, median, regression, correlation
│   └── utils/formatters.py   ← CSV/JSON export, display helpers
│
├── frontend/
│   ├── public/css/main.css   ← Full design system stylesheet
│   ├── public/css/charts.css ← Chart-specific styles
│   ├── public/js/charts.js   ← Chart.js factory functions
│   ├── public/js/filters.js  ← Filter state management
│   ├── public/js/utils.js    ← DOM + data utilities
│   ├── views/salary_view.html
│   ├── views/trends_view.html
│   ├── views/ml_view.html
│   └── views/overview_view.html
│
├── python_api/
│   ├── api.py                ← REST API (13 endpoints, port 8000)
│   └── test_api.py           ← Route tester
│
├── tests/
│   ├── test_models.py        ← 30 unit tests — DB models
│   ├── test_analytics.py     ← 32 unit tests — ML engine
│   └── test_validators.py    ← 20 unit tests — validators
│
└── data/
    ├── generate_csv.py
    ├── sql/schema.sql         ← Full SQL schema + 7 indexes
    ├── job_market.db          ← SQLite DB (auto-created)
    └── csv/                   ← 8 datasets, 4,396 total rows
        ├── countries.csv      (10 rows)
        ├── job_roles.csv      (15 rows)
        ├── salary_data.csv    (450 rows)
        ├── salary_trends.csv  (1,650 rows)
        ├── demand_trends.csv  (1,650 rows)
        ├── skills.csv         (111 rows)
        ├── job_postings.csv   (500 rows)
        └── cost_of_living.csv (10 rows)
```

## Technology Stack
| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Dashboard | Streamlit |
| Database | SQLite (sqlite3) |
| Charts | Plotly |
| Data | Pandas |
| ML Engine | Custom Python (no sklearn) |
| REST API | http.server (built-in) |
| Tests | unittest (82 tests) |

## ML Analytics (`ml/analytics.py`)
| Function | Algorithm |
|----------|-----------|
| predict_salary() | Linear Regression |
| forecast_demand() | Moving Average |
| cost_adjusted_salary() | PPP Calculator |
| skill_gap_score() | Weighted Matching |
| salary_benchmark() | Statistical Summary |

## REST API Endpoints (port 8000)
GET /api/countries · /api/salary/countries · /api/salary/roles
GET /api/salary/workmodes · /api/trends/salary · /api/trends/demand
GET /api/ml/predict · /api/ml/forecast · /api/ml/ppp · /api/ml/benchmark
GET /api/postings · /api/postings/companies · /api/trends/demand-by-role
