import re, subprocess, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class DocumentationTest(unittest.TestCase):
    def test_local_links_resolve(self):
        for path in ROOT.rglob('*.md'):
            if '.terraform' in path.parts: continue
            for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
                if '://' in link or link.startswith('#'): continue
                with self.subTest(path=path,link=link):
                    self.assertTrue((path.parent/link.split('#')[0]).exists())
    def test_every_project_has_followalong_and_cleanup(self):
        projects=list((ROOT/'01.projects').glob('*/README.md'))
        self.assertEqual(len(projects),34)
        for path in projects:
            text=path.read_text()
            with self.subTest(project=path.parent.name):
                for section in ['## Prerequisites','## Walkthrough','## Verify completion','## Troubleshooting','## Cleanup']:
                    self.assertIn(section,text)
                self.assertIn('```bash',text)
    def test_all_bash_blocks_parse(self):
        for path in ROOT.rglob('*.md'):
            if '.terraform' in path.parts: continue
            for index,code in enumerate(re.findall(r'```bash\n(.*?)```',path.read_text(),re.S)):
                with self.subTest(path=path,block=index):
                    result=subprocess.run(['bash','-n'],input=code,text=True,capture_output=True)
                    self.assertEqual(result.returncode,0,result.stderr)
