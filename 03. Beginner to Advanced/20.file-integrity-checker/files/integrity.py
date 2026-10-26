#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path

def manifest(directory):
    directory = Path(directory).resolve()
    if not directory.is_dir():
        raise ValueError('directory does not exist')
    result = {}
    for path in sorted(directory.rglob('*')):
        if path.is_symlink():
            raise ValueError(f'symlink not supported: {path}')
        if path.is_file():
            digest = hashlib.sha256()
            with path.open('rb') as stream:
                for chunk in iter(lambda: stream.read(65536), b''):
                    digest.update(chunk)
            result[str(path.relative_to(directory))] = digest.hexdigest()
    return result

def changes(expected, actual):
    return {'missing': sorted(expected.keys() - actual.keys()),
            'added': sorted(actual.keys() - expected.keys()),
            'modified': sorted(k for k in expected.keys() & actual.keys() if expected[k] != actual[k])}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['record', 'check'])
    parser.add_argument('directory'); parser.add_argument('baseline')
    args = parser.parse_args()
    directory, baseline = Path(args.directory).resolve(), Path(args.baseline).resolve()
    if baseline == directory or directory in baseline.parents:
        parser.error('baseline must be outside the monitored directory')
    actual = manifest(directory)
    if args.action == 'record':
        with baseline.open('x') as out:
            json.dump(actual, out, indent=2)
    else:
        report = changes(json.loads(baseline.read_text()), actual)
        print(json.dumps(report, indent=2))
        raise SystemExit(1 if any(report.values()) else 0)
