import os
import re
from pathlib import Path

static_dir = Path('static')
existing_static_files = set()
for root, dirs, files in os.walk(static_dir):
    for f in files:
        rel = Path(root, f).relative_to(static_dir).as_posix()
        existing_static_files.add(rel)

template_dir = Path('templates')
static_refs = []
static_pattern = re.compile(r"""{%\s*static\s+['"]([^'"]+)['"]\s*%}""")

for root, dirs, files in os.walk(template_dir):
    for f in files:
        if f.endswith('.html'):
            p = Path(root, f)
            with open(p, 'r', encoding='utf-8') as fh:
                content = fh.read()
                for match in static_pattern.finditer(content):
                    static_refs.append((p.as_posix(), match.group(1)))

errors = []
for tmpl, ref in static_refs:
    if ref not in existing_static_files:
        errors.append((tmpl, ref))

if errors:
    print('Static references NOT found or case mismatch:')
    for t, r in errors:
        print(f'  {t} -> {r}')
else:
    print(f'All {len(static_refs)} static references in templates match files on disk with exact case!')

# Check template extends / includes
existing_templates = set()
for root, dirs, files in os.walk(template_dir):
    for f in files:
        rel = Path(root, f).relative_to(template_dir).as_posix()
        existing_templates.add(rel)

tmpl_pattern = re.compile(r"""{%\s*(?:extends|include)\s+['"]([^'"]+)['"]\s*%}""")
tmpl_refs = []
for root, dirs, files in os.walk(template_dir):
    for f in files:
        if f.endswith('.html'):
            p = Path(root, f)
            with open(p, 'r', encoding='utf-8') as fh:
                content = fh.read()
                for match in tmpl_pattern.finditer(content):
                    tmpl_refs.append((p.as_posix(), match.group(1)))

tmpl_errors = []
for tmpl, ref in tmpl_refs:
    if ref not in existing_templates:
        tmpl_errors.append((tmpl, ref))

if tmpl_errors:
    print('Template extends/includes NOT found or case mismatch:')
    for t, r in tmpl_errors:
        print(f'  {t} -> {r}')
else:
    print(f'All {len(tmpl_refs)} template extends/includes match files on disk with exact case!')

