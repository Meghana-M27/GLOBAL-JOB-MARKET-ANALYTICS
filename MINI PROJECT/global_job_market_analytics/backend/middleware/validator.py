"""
backend/middleware/validator.py
Input validation helpers for all filter parameters.
"""

VALID_COUNTRY_CODES = ['US','IN','GB','CA','DE','AU','SG','JP','NL','AE']
VALID_ROLE_IDS      = list(range(1, 16))
VALID_WORK_MODES    = ['Onsite', 'Hybrid', 'Remote']
VALID_YEARS         = list(range(2015, 2031))

def validate_country(code):
    if code is None or code == '':
        return None, None
    if code not in VALID_COUNTRY_CODES:
        return None, f"Invalid country code '{code}'. Valid: {VALID_COUNTRY_CODES}"
    return code, None

def validate_role(role_id):
    if role_id is None or role_id == '':
        return None, None
    try:
        rid = int(role_id)
    except (ValueError, TypeError):
        return None, f"role_id must be an integer, got '{role_id}'"
    if rid not in VALID_ROLE_IDS:
        return None, f"role_id must be between 1 and 15, got {rid}"
    return rid, None

def validate_work_mode(mode):
    if mode is None or mode == '':
        return 'Hybrid', None
    if mode not in VALID_WORK_MODES:
        return None, f"Invalid work_mode '{mode}'. Valid: {VALID_WORK_MODES}"
    return mode, None

def validate_year(year):
    if year is None:
        return None, None
    try:
        y = int(year)
    except (ValueError, TypeError):
        return None, f"year must be an integer, got '{year}'"
    if y not in VALID_YEARS:
        return None, f"year must be between 2015 and 2030, got {y}"
    return y, None

def validate_filters(country=None, role_id=None, work_mode=None):
    """Validate all three main filters at once. Returns (params_dict, errors_list)."""
    errors = []
    cid, err = validate_country(country);   err and errors.append(err)
    rid, err = validate_role(role_id);      err and errors.append(err)
    mode,err = validate_work_mode(work_mode); err and errors.append(err)
    return {'country_code': cid, 'role_id': rid, 'work_mode': mode or 'Hybrid'}, errors
