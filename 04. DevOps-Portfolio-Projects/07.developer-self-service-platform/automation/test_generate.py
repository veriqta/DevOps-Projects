import tempfile,unittest
from pathlib import Path
from generate import generate
class GeneratorTest(unittest.TestCase):
    def test_complete_service_and_duplicate_protection(self):
        with tempfile.TemporaryDirectory() as temp:
            generate('orders-api','payments',temp)
            self.assertTrue((Path(temp)/'orders-api/.github/workflows/check.yml').exists())
            self.assertNotIn('@@NAME@@',(Path(temp)/'orders-api/server.py').read_text())
            with self.assertRaises(ValueError):generate('orders-api','payments',temp)
    def test_invalid_input_and_team(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):generate('../../escape','payments',temp)
            with self.assertRaises(ValueError):generate('orders-api','unknown',temp)
    def test_failed_request_does_not_publish_partial_service(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(RuntimeError):generate('orders-api','payments',temp,fail=True)
            self.assertEqual(list(Path(temp).iterdir()),[])
    def test_dry_run_does_not_publish(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertTrue(generate('orders-api','payments',temp,dry_run=True)['files'])
            self.assertEqual(list(Path(temp).iterdir()),[])
