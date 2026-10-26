"""Interactive developer entry point using the same validated generator."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'automation'))
from generate import generate
if __name__=='__main__':
    name=input('Service name (for example orders-api): ').strip()
    team=input('Owning team (payments or platform): ').strip()
    try:print(generate(name,team,'.generated'))
    except ValueError as error:raise SystemExit(str(error))
