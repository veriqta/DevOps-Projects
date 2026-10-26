import unittest
from evaluate import violations
class PolicyTest(unittest.TestCase):
    def test_fixed_high_blocks(self):self.assertEqual(violations({'Results':[{'Vulnerabilities':[{'VulnerabilityID':'LAB-1','Severity':'HIGH','FixedVersion':'2'}]}]}),['LAB-1'])
    def test_lower_severity_and_unfixed_are_report_only(self):self.assertEqual(violations({'Results':[{'Vulnerabilities':[{'VulnerabilityID':'LAB-2','Severity':'LOW','FixedVersion':'2'},{'VulnerabilityID':'LAB-3','Severity':'HIGH'}]}]}),[])

    def test_missing_report_fails_closed(self):
        with self.assertRaises(ValueError):violations({})
