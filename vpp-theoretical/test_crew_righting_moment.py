import unittest

from crew_righting_moment import crew_moment_nm


class CrewRightingMomentTests(unittest.TestCase):
    def test_sums_mass_times_lever_arm(self):
        result = crew_moment_nm(
            [("helm", 80.0, 0.35), ("crew", 80.0, 1.10)]
        )
        self.assertAlmostEqual(result, 1137.5714, places=3)

    def test_requires_at_least_one_crew_member(self):
        with self.assertRaisesRegex(ValueError, "At least one"):
            crew_moment_nm([])

    def test_rejects_negative_lever_arm(self):
        with self.assertRaisesRegex(ValueError, "cannot be negative"):
            crew_moment_nm([("crew", 80.0, -0.5)])


if __name__ == "__main__":
    unittest.main()
