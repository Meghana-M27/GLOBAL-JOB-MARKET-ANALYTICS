"""
backend/utils/formatters.py
Data formatting and export utilities.
"""
import csv
import io
import json

def to_csv_string(data: list, fieldnames=None):
    """Convert a list of dicts to a CSV string."""
    if not data: return ''
    keys = fieldnames or list(data[0].keys())
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=keys, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(data)
    return buf.getvalue()

def to_json_string(data, indent=2):
    """Convert data to formatted JSON string."""
    return json.dumps(data, indent=indent, default=str)

def salary_display(value_usd, currency='USD', exchange_rates=None):
    """Display salary in local currency if exchange rate provided."""
    if not exchange_rates or currency == 'USD':
        return f"${round(value_usd):,} USD"
    rate = exchange_rates.get(currency, 1)
    local = round(value_usd * rate)
    return f"{local:,} {currency} (~${round(value_usd):,} USD)"

def trend_label(year):
    """Return event label for significant years."""
    labels = {
        2020: '📉 COVID-19',
        2022: '🔄 Recovery',
        2023: '🤖 AI Surge',
        2025: '📈 2025 Peak',
    }
    return labels.get(year, str(year))

def demand_color(status):
    """Return hex color for demand status."""
    return {'Growing': '#10b981', 'Stable': '#f59e0b', 'Declining': '#ef4444'}.get(status, '#6b84a8')

def skill_type_label(skill_type):
    return {'Technical': '⚙️ Technical', 'Soft': '🤝 Soft Skill'}.get(skill_type, skill_type)

def rank_badge(rank):
    """Return emoji badge for top 3 ranks."""
    return {1: '🥇', 2: '🥈', 3: '🥉'}.get(rank, f'#{rank}')

def summarize_insight(demand_status, salary_growth, remote_premium, role_name):
    """Generate a one-line academic insight summary."""
    return (
        f"{role_name} shows {demand_status.lower()} demand with "
        f"{'+' if salary_growth >= 0 else ''}{salary_growth}% salary growth "
        f"over 2015–2025. Remote premium stands at "
        f"{'+' if remote_premium >= 0 else ''}{remote_premium}%."
    )
