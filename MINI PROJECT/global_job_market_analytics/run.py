"""
run.py
Master entry point for the Global Job Market Analysis System.
Usage:
  python run.py           → Start Streamlit dashboard (default)
  python run.py --api     → Start REST API server on port 8000
  python run.py --test    → Run all unit tests
  python run.py --init    → Reinitialise database from CSV files
  python run.py --info    → Show project info and file structure
"""
import sys, os, subprocess

BASE = os.path.dirname(os.path.abspath(__file__))

def banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║    🌍  Global Job Market Analysis System — Enterprise v2.0  ║
║    Python · SQLite · Streamlit · ML Analytics · REST API    ║
╚══════════════════════════════════════════════════════════════╝
""")

def start_dashboard():
    banner()
    print("  Starting Streamlit dashboard...")
    print("  → http://localhost:8501\n")
    subprocess.run([sys.executable, '-m', 'streamlit', 'run',
                    os.path.join(BASE, 'app.py')], cwd=BASE)

def start_api():
    banner()
    print("  Starting REST API server...")
    print("  → http://localhost:8000/api/\n")
    subprocess.run([sys.executable, os.path.join(BASE, 'python_api', 'api.py')], cwd=BASE)

def run_tests():
    banner()
    print("  Running test suite (82 unit tests)...\n")
    result = subprocess.run(
        [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
        cwd=BASE, env={**os.environ, 'PYTHONPATH': BASE}
    )
    sys.exit(result.returncode)

def init_database():
    banner()
    sys.path.insert(0, BASE)
    from database import init_db
    print("  Reinitialising database from CSV files...")
    init_db()
    print("  ✅ Database ready.\n")

def show_info():
    banner()
    print("  📁 Project Structure:")
    structure = [
        ("app.py",                     "Main Streamlit application (8 tabs)"),
        ("database.py",                "SQLite engine — reads CSVs into DB"),
        ("run.py",                     "Master entry point (this file)"),
        ("requirements.txt",           "Python dependencies"),
        ("README.md",                  "Full documentation"),
        ("",                           ""),
        ("ml/analytics.py",            "Python ML engine — 7 analytics functions"),
        ("",                           ""),
        ("backend/config/",            "DB config + app settings"),
        ("backend/models/",            "5 data models (country, salary, role, trends, postings)"),
        ("backend/middleware/",        "Logger, validator, cache"),
        ("backend/routes/",            "4 route handler modules"),
        ("backend/utils/",             "Helpers, statistics, formatters"),
        ("",                           ""),
        ("frontend/public/css/",       "main.css + charts.css"),
        ("frontend/public/js/",        "charts.js + filters.js + utils.js"),
        ("frontend/views/",            "HTML view snippets for all 4 major tabs"),
        ("",                           ""),
        ("python_api/api.py",          "Standalone REST API (13 endpoints)"),
        ("python_api/test_api.py",     "API route tester"),
        ("",                           ""),
        ("tests/test_models.py",       "Unit tests — database models"),
        ("tests/test_analytics.py",    "Unit tests — ML analytics engine"),
        ("tests/test_validators.py",   "Unit tests — input validators"),
        ("",                           ""),
        ("data/csv/",                  "8 CSV datasets (4,300+ rows total)"),
        ("data/sql/schema.sql",        "Full SQL schema with indexes"),
        ("data/job_market.db",         "SQLite database (auto-generated)"),
    ]
    for path, desc in structure:
        if not path:
            print()
        else:
            print(f"    {path:<38} {desc}")

    print("""
  📊 Data Summary:
    Countries    :  10    Work Modes    :  3
    Job Roles    :  15    Trend Years   :  2015–2025 (11 years)
    Salary Rows  :  450   Trend Rows    :  1,650
    Demand Rows  :  1,650 Job Postings  :  500+
    Skills       :  111   CoL Records   :  10

  🔗 Run Options:
    python run.py           Start dashboard at localhost:8501
    python run.py --api     Start REST API  at localhost:8000
    python run.py --test    Run 82 unit tests
    python run.py --init    Reinitialise database
""")

if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv) > 1 else ''
    if arg == '--api':   start_api()
    elif arg == '--test': run_tests()
    elif arg == '--init': init_database()
    elif arg == '--info': show_info()
    else: start_dashboard()
