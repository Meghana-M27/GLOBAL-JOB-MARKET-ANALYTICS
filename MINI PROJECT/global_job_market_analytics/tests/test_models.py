"""
tests/test_models.py
Unit tests for all database models.
Run: python -m pytest tests/ -v
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from database import init_db
from backend.models import CountryModel, SalaryModel, RoleModel, TrendModel, PostingsModel

class TestCountryModel(unittest.TestCase):
    def setUp(self): init_db()

    def test_get_all_returns_10(self):
        rows = CountryModel.get_all()
        self.assertEqual(len(rows), 10)

    def test_get_by_code_us(self):
        c = CountryModel.get_by_code('US')
        self.assertIsNotNone(c)
        self.assertEqual(c['name'], 'United States')

    def test_get_by_code_invalid(self):
        c = CountryModel.get_by_code('XX')
        self.assertIsNone(c)

    def test_get_regions(self):
        regions = CountryModel.get_regions()
        self.assertIn('Asia', regions)
        self.assertIn('Europe', regions)

    def test_get_with_avg_salary(self):
        rows = CountryModel.get_with_avg_salary('Hybrid')
        self.assertTrue(all('avg_salary' in r for r in rows))

    def test_get_cost_of_living(self):
        col = CountryModel.get_cost_of_living('US')
        self.assertIsNotNone(col)
        self.assertIn('col_index', col)


class TestSalaryModel(unittest.TestCase):
    def setUp(self): init_db()

    def test_country_comparison_returns_data(self):
        rows = SalaryModel.country_comparison(work_mode='Hybrid')
        self.assertEqual(len(rows), 10)
        self.assertTrue(all('avg_salary' in r for r in rows))

    def test_country_comparison_with_role(self):
        rows = SalaryModel.country_comparison(role_id=1, work_mode='Hybrid')
        self.assertEqual(len(rows), 10)

    def test_role_comparison(self):
        rows = SalaryModel.role_comparison(work_mode='Hybrid')
        self.assertEqual(len(rows), 15)

    def test_workmode_comparison(self):
        rows = SalaryModel.workmode_comparison('US', 1)
        modes = [r['work_mode'] for r in rows]
        self.assertIn('Onsite', modes)
        self.assertIn('Hybrid', modes)
        self.assertIn('Remote', modes)

    def test_us_salary_higher_than_india(self):
        us = SalaryModel.country_comparison(role_id=1, work_mode='Hybrid')
        salaries = {r['country']: r['avg_salary'] for r in us}
        self.assertGreater(salaries['United States'], salaries['India'])

    def test_global_stats(self):
        stats = SalaryModel.global_stats('Hybrid')
        self.assertIn('global_avg', stats)
        self.assertGreater(stats['global_avg'], 0)


class TestRoleModel(unittest.TestCase):
    def setUp(self): init_db()

    def test_get_all_returns_15(self):
        rows = RoleModel.get_all()
        self.assertEqual(len(rows), 15)

    def test_get_by_id(self):
        role = RoleModel.get_by_id(1)
        self.assertEqual(role['title'], 'Software Engineer')

    def test_get_skills(self):
        skills = RoleModel.get_skills(1)
        self.assertGreater(len(skills), 0)
        self.assertTrue(all('skill_name' in s for s in skills))

    def test_skill_percentages_sum_100(self):
        skills = RoleModel.get_skills(5)
        total = sum(s['percentage'] for s in skills)
        self.assertAlmostEqual(total, 100.0, delta=1.0)

    def test_top_by_salary(self):
        top = RoleModel.get_top_by_salary(work_mode='Hybrid', limit=5)
        self.assertEqual(len(top), 5)
        salaries = [r['avg_salary'] for r in top]
        self.assertEqual(salaries, sorted(salaries, reverse=True))


class TestTrendModel(unittest.TestCase):
    def setUp(self): init_db()

    def test_salary_trend_years(self):
        rows = TrendModel.salary_trend('US', 1)
        years = [r['year'] for r in rows]
        self.assertEqual(years, list(range(2015, 2026)))

    def test_salary_growth_positive(self):
        rate = TrendModel.growth_rate('US', 1)
        self.assertGreater(rate, 0)

    def test_demand_trend_returns_11_years(self):
        rows = TrendModel.demand_trend('US', 1)
        self.assertEqual(len(rows), 11)

    def test_demand_by_role_2025(self):
        rows = TrendModel.demand_by_role(2025)
        self.assertEqual(len(rows), 15)
        idxs = [r['idx'] for r in rows]
        self.assertEqual(idxs, sorted(idxs, reverse=True))

    def test_2025_salary_higher_than_2015(self):
        rows = TrendModel.salary_trend('US', 5)
        self.assertGreater(rows[-1]['avg'], rows[0]['avg'])


class TestPostingsModel(unittest.TestCase):
    def setUp(self): init_db()

    def test_get_all(self):
        rows = PostingsModel.get_all(limit=10)
        self.assertEqual(len(rows), 10)

    def test_total_count(self):
        n = PostingsModel.total_count()
        self.assertGreaterEqual(n, 500)

    def test_company_stats(self):
        rows = PostingsModel.company_stats(limit=5)
        self.assertEqual(len(rows), 5)
        self.assertTrue(all('avg_salary' in r for r in rows))

    def test_experience_levels(self):
        rows = PostingsModel.by_experience_level()
        levels = [r['experience_level'] for r in rows]
        self.assertIn('Senior', levels)
        self.assertIn('Entry', levels)

    def test_monthly_timeline(self):
        rows = PostingsModel.monthly_timeline()
        self.assertGreater(len(rows), 0)
        self.assertTrue(all('month' in r for r in rows))


if __name__ == '__main__':
    unittest.main(verbosity=2)
