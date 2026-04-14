"""
backend/utils/helpers.py
Utility helper functions used across the project.
"""

def fmt_usd(value, decimals=0):
    """Format a number as USD string."""
    if value is None: return '$0'
    return f"${round(value, decimals):,.{decimals}f}"

def fmt_pct(value, decimals=1):
    """Format a number as percentage string."""
    if value is None: return '0%'
    sign = '+' if value >= 0 else ''
    return f"{sign}{round(value, decimals)}%"

def safe_divide(numerator, denominator, default=0):
    """Safe division returning default if denominator is 0."""
    if not denominator:
        return default
    return numerator / denominator

def growth_rate(old_val, new_val, decimals=1):
    """Calculate percentage growth rate."""
    if not old_val:
        return 0
    return round((new_val - old_val) / old_val * 100, decimals)

def classify_demand(growth_pct):
    """Classify demand status from growth percentage."""
    if growth_pct > 5:   return 'Growing'
    if growth_pct < -3:  return 'Declining'
    return 'Stable'

def rows_to_dict(rows):
    """Convert sqlite3.Row list to list of dicts."""
    return [dict(r) for r in rows] if rows else []

def paginate(data, page=1, page_size=20):
    """Paginate a list."""
    start = (page - 1) * page_size
    end   = start + page_size
    return {
        'items': data[start:end],
        'total': len(data),
        'page': page,
        'page_size': page_size,
        'total_pages': -(-len(data) // page_size)
    }

def flatten_country_trend(multi_country_data):
    """Group multi-country trend data by country name."""
    grouped = {}
    for row in multi_country_data:
        name = row['country']
        if name not in grouped:
            grouped[name] = {'country': name, 'code': row['code'], 'years': [], 'values': []}
        grouped[name]['years'].append(row['year'])
        grouped[name]['values'].append(round(row['avg'], 0))
    return list(grouped.values())
