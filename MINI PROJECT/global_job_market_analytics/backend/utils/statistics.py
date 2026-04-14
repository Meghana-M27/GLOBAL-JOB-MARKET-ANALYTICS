"""
backend/utils/statistics.py
Statistical utility functions used by ML analytics.
"""
import math

def mean(values):
    if not values: return 0
    return sum(values) / len(values)

def median(values):
    if not values: return 0
    s = sorted(values)
    n = len(s)
    return (s[n//2-1] + s[n//2]) / 2 if n % 2 == 0 else s[n//2]

def std_dev(values):
    if len(values) < 2: return 0
    m = mean(values)
    variance = sum((v - m) ** 2 for v in values) / (len(values) - 1)
    return math.sqrt(variance)

def percentile(values, p):
    """Return the p-th percentile (0-100) of a sorted list."""
    if not values: return 0
    s = sorted(values)
    idx = (p / 100) * (len(s) - 1)
    lo, hi = int(idx), min(int(idx) + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (idx - lo)

def linear_regression(xs, ys):
    """Least-squares linear regression. Returns slope, intercept, r_squared."""
    n = len(xs)
    if n < 2: return 0, 0, 0
    mx, my = mean(xs), mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    if den == 0: return 0, my, 0
    slope = num / den
    intercept = my - slope * mx
    ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - my) ** 2 for y in ys)
    r2 = 1 - ss_res / ss_tot if ss_tot else 0
    return round(slope, 4), round(intercept, 4), round(r2, 4)

def moving_average(values, window=3):
    """Simple moving average over a window."""
    if len(values) < window: return mean(values)
    return mean(values[-window:])

def normalize(values, new_min=0, new_max=100):
    """Min-max normalize a list to [new_min, new_max]."""
    mn, mx = min(values), max(values)
    if mx == mn: return [new_min] * len(values)
    return [round(new_min + (v - mn) / (mx - mn) * (new_max - new_min), 2) for v in values]

def z_score(value, values):
    """Z-score of a single value relative to a list."""
    m, s = mean(values), std_dev(values)
    if s == 0: return 0
    return round((value - m) / s, 3)

def correlation(xs, ys):
    """Pearson correlation coefficient between two lists."""
    if len(xs) != len(ys) or len(xs) < 2: return 0
    mx, my = mean(xs), mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    return round(num / den, 4) if den else 0

def summary_statistics(values):
    """Return a full stats dict for a list of numbers."""
    if not values:
        return {'count': 0, 'mean': 0, 'median': 0, 'std_dev': 0, 'min': 0, 'max': 0, 'q1': 0, 'q3': 0}
    return {
        'count':   len(values),
        'mean':    round(mean(values), 2),
        'median':  round(median(values), 2),
        'std_dev': round(std_dev(values), 2),
        'min':     round(min(values), 2),
        'max':     round(max(values), 2),
        'q1':      round(percentile(values, 25), 2),
        'q3':      round(percentile(values, 75), 2),
    }
