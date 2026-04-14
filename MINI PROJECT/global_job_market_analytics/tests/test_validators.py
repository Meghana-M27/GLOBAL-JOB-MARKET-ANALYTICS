"""
tests/test_validators.py
Unit tests for input validation middleware.
Run: python -m pytest tests/test_validators.py -v
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from backend.middleware.validator import (
    validate_country, validate_role, validate_work_mode,
    validate_year, validate_filters
)


class TestValidateCountry(unittest.TestCase):

    def test_valid_code(self):
        code, err = validate_country('US')
        self.assertEqual(code, 'US')
        self.assertIsNone(err)

    def test_all_10_valid(self):
        for c in ['US','IN','GB','CA','DE','AU','SG','JP','NL','AE']:
            code, err = validate_country(c)
            self.assertIsNone(err, f"Expected no error for {c}")

    def test_invalid_code(self):
        code, err = validate_country('XX')
        self.assertIsNone(code)
        self.assertIsNotNone(err)

    def test_empty_string(self):
        code, err = validate_country('')
        self.assertIsNone(code)
        self.assertIsNone(err)

    def test_none(self):
        code, err = validate_country(None)
        self.assertIsNone(code)
        self.assertIsNone(err)


class TestValidateRole(unittest.TestCase):

    def test_valid_role_1_to_15(self):
        for i in range(1, 16):
            rid, err = validate_role(i)
            self.assertEqual(rid, i)
            self.assertIsNone(err)

    def test_string_integer(self):
        rid, err = validate_role('5')
        self.assertEqual(rid, 5)
        self.assertIsNone(err)

    def test_out_of_range(self):
        _, err = validate_role(99)
        self.assertIsNotNone(err)

    def test_zero(self):
        _, err = validate_role(0)
        self.assertIsNotNone(err)

    def test_none(self):
        rid, err = validate_role(None)
        self.assertIsNone(rid)
        self.assertIsNone(err)

    def test_non_numeric(self):
        rid, err = validate_role('abc')
        self.assertIsNone(rid)
        self.assertIsNotNone(err)


class TestValidateWorkMode(unittest.TestCase):

    def test_valid_modes(self):
        for m in ['Onsite', 'Hybrid', 'Remote']:
            mode, err = validate_work_mode(m)
            self.assertEqual(mode, m)
            self.assertIsNone(err)

    def test_invalid_mode(self):
        mode, err = validate_work_mode('WFH')
        self.assertIsNone(mode)
        self.assertIsNotNone(err)

    def test_none_defaults_to_hybrid(self):
        mode, err = validate_work_mode(None)
        self.assertEqual(mode, 'Hybrid')
        self.assertIsNone(err)

    def test_empty_defaults_to_hybrid(self):
        mode, err = validate_work_mode('')
        self.assertEqual(mode, 'Hybrid')
        self.assertIsNone(err)


class TestValidateYear(unittest.TestCase):

    def test_valid_years(self):
        for y in [2015, 2020, 2025, 2026, 2030]:
            yr, err = validate_year(y)
            self.assertEqual(yr, y)
            self.assertIsNone(err)

    def test_string_year(self):
        yr, err = validate_year('2026')
        self.assertEqual(yr, 2026)

    def test_out_of_range(self):
        _, err = validate_year(2040)
        self.assertIsNotNone(err)

    def test_none(self):
        yr, err = validate_year(None)
        self.assertIsNone(yr)
        self.assertIsNone(err)


class TestValidateFilters(unittest.TestCase):

    def test_all_valid(self):
        params, errors = validate_filters('US', 1, 'Hybrid')
        self.assertEqual(errors, [])
        self.assertEqual(params['country_code'], 'US')
        self.assertEqual(params['role_id'], 1)
        self.assertEqual(params['work_mode'], 'Hybrid')

    def test_all_none(self):
        params, errors = validate_filters(None, None, None)
        self.assertEqual(errors, [])
        self.assertEqual(params['work_mode'], 'Hybrid')

    def test_invalid_country_returns_error(self):
        params, errors = validate_filters('ZZ', 1, 'Hybrid')
        self.assertGreater(len(errors), 0)

    def test_invalid_role_returns_error(self):
        params, errors = validate_filters('US', 99, 'Hybrid')
        self.assertGreater(len(errors), 0)

    def test_invalid_mode_returns_error(self):
        params, errors = validate_filters('US', 1, 'PJamas')
        self.assertGreater(len(errors), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
