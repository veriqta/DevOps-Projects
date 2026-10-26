#!/usr/bin/env python3
import argparse, tarfile, tempfile
from datetime import datetime, timezone
from pathlib import Path

def archive(source, destination):
    source, destination = Path(source).resolve(), Path(destination).resolve()
    if not source.is_dir():
        raise ValueError('source must be a directory')
    if destination == source or source in destination.parents:
        raise ValueError('destination must be outside source')
    destination.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    # Exclusive creation prevents accidental replacement of another archive.
    with tempfile.NamedTemporaryFile(prefix=f'logs-{stamp}-', suffix='.tar.gz', dir=destination, delete=False) as temp:
        target = Path(temp.name)
    try:
        with tarfile.open(target, 'w:gz', dereference=False) as output:
            output.add(source, arcname=source.name)
    except BaseException:
        target.unlink(missing_ok=True)
        raise
    return target

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Archive a directory without deleting it')
    parser.add_argument('source'); parser.add_argument('destination')
    args = parser.parse_args()
    print(archive(args.source, args.destination))
