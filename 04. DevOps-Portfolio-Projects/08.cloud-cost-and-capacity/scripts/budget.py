import json,sys
from pathlib import Path
report=json.loads(Path(sys.argv[1]).read_text());cost=report.get('totalMonthlyCost')
if cost is None:raise SystemExit('No estimate available: refusing to treat missing cost as zero')
limit=float(sys.argv[2]);actual=float(cost)
print(json.dumps({'estimated_monthly_usd':actual,'budget_usd':limit,'within_budget':actual<=limit}))
raise SystemExit(0 if actual<=limit else 1)
