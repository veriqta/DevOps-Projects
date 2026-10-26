#!/usr/bin/env python3
import argparse, collections, json, re
PATTERN = re.compile(r'^(\S+) \S+ \S+ \[[^\]]+\] "\S+ ([^ ]+) [^"]+" (\d{3}) (?:\d+|-)')

def analyse(lines):
    clients, paths, statuses = (collections.Counter() for _ in range(3))
    malformed = 0
    for line in lines:
        match = PATTERN.match(line)
        if not match:
            malformed += 1; continue
        client, path, status = match.groups()
        clients[client] += 1; paths[path] += 1; statuses[status] += 1
    return {'requests': sum(statuses.values()), 'malformed': malformed,
            'statuses': dict(statuses), 'top_clients': clients.most_common(10),
            'top_paths': paths.most_common(10)}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('log')
    args = parser.parse_args()
    with open(args.log, errors='replace') as source:
        print(json.dumps(analyse(source), indent=2))
