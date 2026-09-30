import os
import re

ignore_dirs = {'.venv', 'staticfiles', '__pycache__', 'scratch'}
matches = []

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('.git')]
    for file in files:
        if file.endswith(('.py', '.html', '.css', '.js')):
            p = os.path.join(root, file)
            with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                for ln, l in enumerate(f, 1):
                    for m in re.finditer(r'http://[^\s\'"\>\)]+', l):
                        url = m.group(0)
                        if not any(safe in url for safe in ('localhost', '127.0.0.1', 'w3.org', 'schema.org')):
                            matches.append((p, ln, url))

if matches:
    print('Found http:// URLs:')
    for p, ln, u in matches:
        print(f'  {p}:{ln}: {u}')
else:
    print('Zero insecure http:// external resource URLs found!')
