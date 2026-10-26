import json,subprocess,sys,tempfile,unittest
from pathlib import Path
class BudgetTest(unittest.TestCase):
    def test_accept_reject_and_missing_estimates(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'cost.json'
            for value,expected in [('12.5',0),('55',1),(None,1)]:
                p.write_text(json.dumps({'totalMonthlyCost':value}))
                result=subprocess.run([sys.executable,str(Path(__file__).with_name('budget.py')),str(p),'30'],capture_output=True)
                self.assertEqual(result.returncode,expected)
