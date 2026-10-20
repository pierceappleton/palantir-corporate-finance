"""Peer multiple denominator checks."""
import copy
import json
import unittest
from pathlib import Path

from src.peers import multiples


def first_peer():
    return copy.deepcopy(json.loads(Path("data/processed/peer_inputs.json").read_text(encoding="utf8"))[0])


class PeerTests(unittest.TestCase):
    def test_nonpositive_gaap_earnings_are_not_a_pe(self):
        p = first_peer()
        p["annual_ni"] = 0
        p["current_h1_ni"] = 0
        p["prior_h1_ni"] = 1
        self.assertIsNone(multiples(p)["pe"])

    def test_tiny_earnings_marked_not_meaningful_not_dropped(self):
        p = first_peer()
        p["annual_ni"] = 10
        p["current_h1_ni"] = 0
        p["prior_h1_ni"] = 0
        row = multiples(p, {"pe_min_net_margin": 0.05})
        self.assertIsNone(row["pe"])
        self.assertTrue(row["pe_status"].startswith("not meaningful"))
        self.assertIsNotNone(row["ev_revenue"])

    def test_negative_revenue_denominator_rejected(self):
        p = first_peer()
        p["prior_h1_revenue"] = p["annual_revenue"] + p["current_h1_revenue"] + 1
        with self.assertRaises(ValueError):
            multiples(p)


if __name__ == "__main__":
    unittest.main()
