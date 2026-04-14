"""
backend/config/settings.py
Application-wide settings and constants.
"""

APP_NAME    = "Global Job Market Analysis System"
VERSION     = "2.0.0"
DESCRIPTION = "Enterprise Job Market Intelligence Platform"

# Countries
COUNTRIES = [
    {'code':'US','name':'United States','region':'North America','currency':'USD'},
    {'code':'IN','name':'India','region':'Asia','currency':'INR'},
    {'code':'GB','name':'United Kingdom','region':'Europe','currency':'GBP'},
    {'code':'CA','name':'Canada','region':'North America','currency':'CAD'},
    {'code':'DE','name':'Germany','region':'Europe','currency':'EUR'},
    {'code':'AU','name':'Australia','region':'Oceania','currency':'AUD'},
    {'code':'SG','name':'Singapore','region':'Asia','currency':'SGD'},
    {'code':'JP','name':'Japan','region':'Asia','currency':'JPY'},
    {'code':'NL','name':'Netherlands','region':'Europe','currency':'EUR'},
    {'code':'AE','name':'United Arab Emirates','region':'Middle East','currency':'AED'},
]

# Work modes
WORK_MODES = ['Onsite', 'Hybrid', 'Remote']
MODE_FACTORS = {'Onsite': 0.96, 'Hybrid': 1.0, 'Remote': 1.03}

# Trend years
TREND_YEARS = list(range(2015, 2026))
YEAR_MULTIPLIERS = [0.72,0.76,0.80,0.85,0.90,0.87,0.92,0.97,1.05,1.12,1.20]

# Demand classification thresholds
DEMAND_GROWING_THRESHOLD  =  5.0   # % year-on-year growth
DEMAND_DECLINING_THRESHOLD = -3.0  # % year-on-year decline

# ML settings
FORECAST_WINDOW    = 3    # years for moving average
MAX_FORECAST_YEARS = 5    # max prediction horizon
MIN_DATA_POINTS    = 3    # min rows needed for regression

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE     = 100
