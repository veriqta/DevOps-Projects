import importlib.util, tempfile, tarfile, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / '03.tools' / (name + '.py'))
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module
archive = load('archive_logs').archive
analyse = load('analyse_nginx').analyse
integrity = load('integrity')
class ToolsTest(unittest.TestCase):
    def test_archive_roundtrip_and_source_retained(self):
        with tempfile.TemporaryDirectory() as temp:
            base=Path(temp); source=base/'logs'; source.mkdir(); (source/'app.log').write_text('hello')
            first=archive(source,base/'archives'); second=archive(source,base/'archives')
            self.assertNotEqual(first,second)
            with tarfile.open(first) as stored:
                self.assertEqual(stored.extractfile('logs/app.log').read(), b'hello')
            self.assertEqual((source/'app.log').read_text(),'hello')
            with self.assertRaises(ValueError): archive(source,source/'archives')
    def test_log_counts_and_malformed_input(self):
        lines=(ROOT/'05.fixtures/access.log').read_text().splitlines()+['bad line']
        result=analyse(lines)
        self.assertEqual(result['requests'],3); self.assertEqual(result['statuses'],{'200':2,'404':1})
        self.assertEqual(result['malformed'],1)
    def test_integrity_detects_each_change(self):
        with tempfile.TemporaryDirectory() as temp:
            base=Path(temp); (base/'a').write_text('old'); (base/'b').write_text('delete')
            before=integrity.manifest(base)
            (base/'a').write_text('new'); (base/'b').unlink(); (base/'c').write_text('add')
            self.assertEqual(integrity.changes(before,integrity.manifest(base)),{'missing':['b'],'added':['c'],'modified':['a']})
    def test_integrity_rejects_symlinks(self):
        with tempfile.TemporaryDirectory() as temp:
            base=Path(temp); (base/'link').symlink_to('/etc/hosts')
            with self.assertRaises(ValueError): integrity.manifest(base)
if __name__ == '__main__': unittest.main()
