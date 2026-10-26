import json, os, subprocess, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class CLITest(unittest.TestCase):
    def test_integrity_exit_codes_and_baseline_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            base=Path(temp); source=base/'files';source.mkdir();(source/'a').write_text('original'); baseline=base/'baseline.json'
            def run(action):
                return subprocess.run([os.sys.executable,str(ROOT/'03.tools/integrity.py'),action,str(source),str(baseline)],capture_output=True,text=True)
            self.assertEqual(run('record').returncode,0)
            self.assertEqual(run('check').returncode,0)
            self.assertNotEqual(run('record').returncode,0)
            (source/'a').write_text('tampered')
            result=run('check');self.assertEqual(result.returncode,1);self.assertEqual(json.loads(result.stdout)['modified'],['a'])
    def test_backup_failure_never_leaves_completed_file(self):
        with tempfile.TemporaryDirectory() as temp:
            base=Path(temp); bindir=base/'bin';bindir.mkdir();docker=bindir/'docker'
            docker.write_text('#!/bin/sh\nprintf "partial dump"\nexit 7\n');docker.chmod(0o755)
            dest=base/'backups'
            result=subprocess.run(['bash',str(ROOT/'03.tools/backup-db.sh'),str(dest)],env={**os.environ,'PATH':str(bindir)+':'+os.environ['PATH']},capture_output=True)
            self.assertNotEqual(result.returncode,0);self.assertEqual(list(dest.iterdir()),[])
    def test_backup_success_commits_dump_and_restricts_permissions(self):
        with tempfile.TemporaryDirectory() as temp:
            base=Path(temp);bindir=base/'bin';bindir.mkdir();docker=bindir/'docker'
            docker.write_text('#!/bin/sh\nprintf "valid lab dump"\n');docker.chmod(0o755)
            result=subprocess.run(['bash',str(ROOT/'03.tools/backup-db.sh'),str(base/'backups')],env={**os.environ,'PATH':str(bindir)+':'+os.environ['PATH']},capture_output=True,text=True,check=True)
            output=Path(result.stdout.strip());self.assertEqual(output.read_text(),'valid lab dump');self.assertEqual(output.stat().st_mode & 0o777,0o600)
    @unittest.skipUnless(Path('/proc/meminfo').exists(),'Linux /proc required')
    def test_linux_stats(self):
        result=subprocess.run([os.sys.executable,str(ROOT/'03.tools/server_stats.py')],capture_output=True,text=True,check=True)
        stats=json.loads(result.stdout)
        self.assertEqual(len(stats['load_average_1_5_15m']),3)
        self.assertGreater(stats['memory_total_bytes'],stats['memory_available_bytes'])
        self.assertGreater(stats['disk_total_bytes'],stats['disk_used_bytes'])
