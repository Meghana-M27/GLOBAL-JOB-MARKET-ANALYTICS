"""
tests/test_analytics.py
Unit tests for the ML analytics engine.
Run: python -m pytest tests/test_analytics.py -v
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from database import init_db
from ml.analytics import (
    predict_salary, forecast_demand, cost_adjusted_salary,
    skill_gap_score, salary_benchmark, top_paying_roles,
    company_insights, summary_stats
)
from backend.utils.statistics import (
    mean, median, std_dev, linear_regression,
    moving_average, normalize, z_score, correlation, summary_statistics
)


class TestPredictSalary(unittest.TestCase):
    def setUp(self): init_db()

    def test_returns_valid_dict(self):
        result = predict_salary('US', 1, 'Hybrid', 2026)
        self.assertIsNotNone(result)
        self.assertIn('predicted_salary', result)

    def test_predicted_salary_positive(self):
        result = predict_salary('US', 1, 'Hybrid', 2026)
        self.assertGreater(result['predicted_salary'], 0)

    def test_r_squared_between_0_and_1(self):
        result = predict_salary('US', 3, 'Hybrid', 2026)
        self.assertGreaterEqual(result['r_squared'], 0)
        self.assertLessEqual(result['r_squared'], 1)

    def test_remote_higher_than_onsite(self):
        onsite = predict_salary('US', 5, 'Onsite', 2026)['predicted_salary']
        remote = predict_salary('US', 5, 'Remote', 2026)['predicted_salary']
        self.assertGreater(remote, onsite)

    def test_2030_higher_than_2026(self):
        near  = predict_salary('US', 1, 'Hybrid', 2026)['predicted_salary']
        far   = predict_salary('US', 1, 'Hybrid', 2030)['predicted_salary']
        self.assertGreater(far, near)

    def test_us_higher_than_india(self):
        us = predict_salary('US', 1, 'Hybrid', 2026)['predicted_salary']
        in_ = predict_salary('IN', 1, 'Hybrid', 2026)['predicted_salary']
        self.assertGreater(us, in_)


class TestForecastDemand(unittest.TestCase):
    def setUp(self): init_db()

    def test_returns_valid_dict(self):
        result = forecast_demand('US', 1, 3)
        self.assertIn('status', result)
        self.assertIn('forecasts', result)

    def test_forecast_length_matches_horizon(self):
        for h in [1, 3, 5]:
            result = forecast_demand('US', 1, h)
            self.assertEqual(len(result['forecasts']), h)

    def test_status_is_valid(self):
        result = forecast_demand('US', 5, 3)
        self.assertIn(result['status'], ['Growing', 'Stable', 'Declining'])

    def test_ai_engineer_growing(self):
        result = forecast_demand('US', 5, 3)
        self.assertEqual(result['status'], 'Growing')

    def test_forecast_years_sequential(self):
        result = forecast_demand('US', 1, 3)
        years = [f['year'] for f in result['forecasts']]
        self.assertEqual(years, [2026, 2027, 2028])


class TestCostAdjustedSalary(unittest.TestCase):
    def setUp(self): init_db()

    def test_returns_valid_dict(self):
        result = cost_adjusted_salary('US', 1, 'Hybrid')
        self.assertIn('raw_salary', result)
        self.assertIn('ppp_adjusted_salary', result)

    def test_india_ppp_higher_than_raw_ratio(self):
        us = cost_adjusted_salary('US', 1, 'Hybrid')
        in_ = cost_adjusted_salary('IN', 1, 'Hybrid')
        us_ratio  = us['ppp_adjusted_salary']  / us['raw_salary']
        in_ratio  = in_['ppp_adjusted_salary'] / in_['raw_salary']
        self.assertGreater(in_ratio, us_ratio)

    def test_after_tax_less_than_raw(self):
        result = cost_adjusted_salary('GB', 1, 'Hybrid')
        self.assertLess(result['after_tax'], result['raw_salary'])


class TestSkillGapScore(unittest.TestCase):
    def setUp(self): init_db()

    def test_full_match_returns_100(self):
        from backend.models import RoleModel
        skills = [s['skill_name'] for s in RoleModel.get_skills(1)]
        result = skill_gap_score(1, skills)
        self.assertAlmostEqual(result['match_score'], 100.0, delta=1.0)

    def test_no_match_returns_low_score(self):
        result = skill_gap_score(1, ['Dancing', 'Cooking'])
        self.assertLess(result['match_score'], 20)

    def test_partial_match(self):
        result = skill_gap_score(3, ['Python', 'SQL'])
        self.assertGreater(result['match_score'], 0)
        self.assertLess(result['match_score'], 100)

    def test_readiness_levels(self):
        from backend.models import RoleModel
        all_skills = [s['skill_name'] for s in RoleModel.get_skills(1)]
        high   = skill_gap_score(1, all_skills)['readiness']
        none_  = skill_gap_score(1, [])['readiness']
        self.assertEqual(high, 'High')
        self.assertEqual(none_, 'Low')


class TestSalaryBenchmark(unittest.TestCase):
    def setUp(self): init_db()

    def test_returns_10_countries(self):
        result = salary_benchmark(1, 'Hybrid')
        self.assertEqual(len(result['rankings']), 10)

    def test_us_is_top(self):
        result = salary_benchmark(1, 'Hybrid')
        self.assertEqual(result['top_country']['country'], 'United States')

    def test_global_avg_between_min_max(self):
        result = salary_benchmark(1, 'Hybrid')
        self.assertGreater(result['global_avg'], result['global_min'])
        self.assertLess(result['global_avg'], result['global_max'])


class TestStatisticsUtils(unittest.TestCase):

    def test_mean(self):
        self.assertEqual(mean([10, 20, 30]), 20)

    def test_median_odd(self):
        self.assertEqual(median([1, 3, 5]), 3)

    def test_median_even(self):
        self.assertEqual(median([1, 2, 3, 4]), 2.5)

    def test_std_dev(self):
        self.assertAlmostEqual(std_dev([2, 4, 4, 4, 5, 5, 7, 9]), 2.0, places=0)

    def test_linear_regression(self):
        xs = [1, 2, 3, 4, 5]
        ys = [2, 4, 6, 8, 10]
        slope, intercept, r2 = linear_regression(xs, ys)
        self.assertAlmostEqual(slope, 2.0, places=2)
        self.assertAlmostEqual(r2, 1.0, places=2)

    def test_moving_average(self):
        self.assertEqual(moving_average([10, 20, 30], 3), 20)

    def test_normalize(self):
        result = normalize([0, 50, 100])
        self.assertEqual(result[0], 0)
        self.assertEqual(result[-1], 100)

    def test_correlation_perfect(self):
        xs = [1, 2, 3, 4, 5]
        ys = [2, 4, 6, 8, 10]
        self.assertAlmostEqual(correlation(xs, ys), 1.0, places=3)

    def test_summary_statistics(self):
        vals = [10, 20, 30, 40, 50]
        stats = summary_statistics(vals)
        self.assertEqual(stats['count'], 5)
        self.assertEqual(stats['mean'], 30)
        self.assertEqual(stats['min'], 10)
        self.assertEqual(stats['max'], 50)


class TestSummaryStats(unittest.TestCase):
    def setUp(self): init_db()

    def test_summary_stats(self):
        stats = summary_stats()
        self.assertEqual(stats['total_countries'], 10)
        self.assertEqual(stats['total_roles'], 15)
        self.assertGreaterEqual(stats['total_postings'], 500)
        self.assertGreater(stats['global_avg_salary'], 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
