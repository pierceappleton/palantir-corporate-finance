"""Post-comparison code corrections: cutoff cash, income-statement identities, award runoff."""
import copy
import unittest

from src.model import bridge, cutoff_cash, existing_award_runoff, forecast, load, value


class CutoffCashTests(unittest.TestCase):
    def setUp(self):
        self.data, self.c = load()
        self.rows = forecast(self.c["cases"]["base"], self.data, self.c)

    def test_second_half_fcff_is_split_with_no_gap_or_overlap(self):
        stub = cutoff_cash(self.rows, self.data, self.c)
        first = self.rows[0]
        self.assertAlmostEqual(first["valued_fcff"] + stub["stub_fcff"], first["fcff"])
        self.assertEqual(stub["stub_days"] + self.c["remaining_days"], self.c["cashflow_days_h2"])

    def test_stub_cash_is_credited_once_in_the_bridge(self):
        stub = cutoff_cash(self.rows, self.data, self.c)
        june = bridge(self.data, self.c)
        rolled = bridge(self.data, self.c, self.rows)
        self.assertAlmostEqual(rolled.cash - june.cash, stub["stub_retained_cash"])
        self.assertAlmostEqual(
            stub["stub_retained_cash"],
            stub["stub_fcff"] + stub["stub_after_tax_interest"] + stub["stub_financing"],
        )

    def test_valuing_from_june_30_needs_no_roll_forward(self):
        c = copy.deepcopy(self.c)
        c["remaining_days"] = c["cashflow_days_h2"]
        rows = forecast(c["cases"]["base"], self.data, c)
        self.assertAlmostEqual(cutoff_cash(rows, self.data, c)["stub_retained_cash"], 0)
        self.assertAlmostEqual(rows[0]["valued_fcff"], rows[0]["fcff"])

    def test_disabled_correction_reproduces_frozen_base(self):
        c = copy.deepcopy(self.c)
        c["corrections"] = {"cutoff_cash_rollforward": False, "award_runoff_schedule": False}
        case = c["cases"]["base"]
        frozen = value(forecast(case, self.data, c), case, self.data, c)["per_share"]
        self.assertAlmostEqual(frozen, 29.756, places=3)


class IncomeStatementIdentityTests(unittest.TestCase):
    def setUp(self):
        self.data, self.c = load()

    def test_displayed_lines_add_to_ebit_and_net_income(self):
        for case in self.c["cases"].values():
            for row in forecast(case, self.data, self.c):
                lines = row["cost_of_revenue"] + row["sales_marketing"] + row["research_development"] + row["general_administrative"]
                self.assertAlmostEqual(row["revenue"] - lines + row["existing_award_service_adjustment"], row["ebit"])
                self.assertAlmostEqual(row["ebit"] + row["annual_interest"] + row["annual_other_income"], row["annual_pretax_income"])
                self.assertAlmostEqual(row["annual_pretax_income"] - row["annual_tax"], row["annual_net_income"])

    def test_expense_allocation_error_fails_loudly(self):
        c = copy.deepcopy(self.c)
        c["presentation"]["sales_share_opex"] = 0.50
        with self.assertRaises(ValueError):
            forecast(c["cases"]["base"], self.data, c)


class AwardRunoffTests(unittest.TestCase):
    def setUp(self):
        self.data, self.c = load()
        self.h = self.data["interim_2026h1"]

    def test_cumulative_amortization_never_exceeds_unrecognized_balance(self):
        for count in [5, 10, 40]:
            schedule = existing_award_runoff(self.data, self.c, count)
            for name, key in [("options", "unrecognized_option_comp"), ("sars", "unrecognized_sar_comp"), ("rsus", "unrecognized_rsu_comp")]:
                total = sum(row[name] for row in schedule)
                self.assertLessEqual(total, self.h[key] + 1e-9)
                if count == 40:
                    self.assertAlmostEqual(total, self.h[key])

    def test_rsu_expense_runs_to_june_2029_not_december_2028(self):
        schedule = existing_award_runoff(self.data, self.c, 5)
        self.assertGreater(schedule[3]["rsus"], 0)
        self.assertEqual(schedule[4]["rsus"], 0)

    def test_longer_service_periods_still_capped(self):
        data = copy.deepcopy(self.data)
        data["interim_2026h1"]["sar_service_years"] = 30
        schedule = existing_award_runoff(data, self.c, 40)
        self.assertAlmostEqual(sum(row["sars"] for row in schedule), self.h["unrecognized_sar_comp"])


class CapexSensitivityTests(unittest.TestCase):
    def setUp(self):
        self.data, self.c = load()

    def test_increased_capex_reduces_fcff_and_value_without_breaking_statements(self):
        self.assertAlmostEqual(self.c["capex_ratio"], 0.012)
        case = copy.deepcopy(self.c["cases"]["base"])
        base_rows = forecast(case, self.data, self.c)
        base_value = value(base_rows, case, self.data, self.c)

        changed_config = copy.deepcopy(self.c)
        changed_config["capex_ratio"] = 0.020
        changed_rows = forecast(case, self.data, changed_config)
        changed_value = value(changed_rows, case, self.data, changed_config)

        self.assertLess(changed_value["per_share"], base_value["per_share"])
        self.assertEqual(changed_value["action"], base_value["action"])
        for base, changed in zip(base_rows, changed_rows):
            self.assertGreater(changed["capex"], base["capex"])
            self.assertLess(changed["fcff"], base["fcff"])
            self.assertAlmostEqual(changed["balance_residual"], 0, places=7)
            self.assertAlmostEqual(changed["cash_residual"], 0, places=7)


if __name__ == "__main__":
    unittest.main()
