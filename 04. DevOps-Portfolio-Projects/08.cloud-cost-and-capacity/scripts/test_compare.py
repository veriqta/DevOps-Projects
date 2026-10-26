import unittest
from compare import compare
class ComparisonTest(unittest.TestCase):
    def test_rejects_candidate_that_breaks_slo(self):
        def report(latency):return {'metrics':{'http_req_duration':{'p(95)':latency},'http_req_failed':{'value':0},'http_reqs':{'count':100}}}
        self.assertFalse(compare(report(100),report(600))['candidate_passes_slo'])
        self.assertTrue(compare(report(100),report(200))['candidate_passes_slo'])

    def test_structured_k6_metrics(self):
        report={'metrics':{'http_req_duration':{'values':{'p(95)':120}},'http_req_failed':{'values':{'rate':0}},'http_reqs':{'values':{'count':100}}}}
        self.assertTrue(compare(report,report)['candidate_passes_slo'])
