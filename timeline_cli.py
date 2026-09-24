#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cheap, token-friendly accessor for the bilingual timelines.

Usage:
    python timeline_cli.py get EVT-0001 [--lang vi|en|both]
    python timeline_cli.py list-missing-source [--limit 30 | --all]
    python timeline_cli.py set-source EVT-0001 --vi "[Nguồn: ...]" --en "[Source: ...]"
    python timeline_cli.py add --date-vi "..." --date-en "..." --vi "..." --en "..." [--source-vi ...] [--source-en ...]

Conventions (see AGENTS.md):
  - Simple one-line events carry the citation inline at the end of the
    description line: `... mô tả. [Nguồn: ...]`.
  - Events with sub-items/images keep the citation on its own line at the
    end of the block (before the ID comment).
  - Every event ends with `<!-- id: EVT-XXXX -->`; IDs are never reused.
    New events receive max(existing)+1.
"""

import argparse
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sort_timelines import parse_blocks  # noqa: E402

DEFAULT_VI = 'timelines_vi.md'
DEFAULT_EN = 'timelines_en.md'

ID_RE = re.compile(r'<!--\s*id:\s*([A-Za-z0-9_-]+)\s*-->')
CITE_LINE = re.compile(r'^\[(?:Nguồn|Source)\s*:\s*(.*?)\]\s*$', re.IGNORECASE)
CITE_TRAIL = re.compile(r'\[(?:Nguồn|Source)\s*:.*?\]\s*$', re.IGNORECASE)
IMG_RE = re.compile(r'!\[.*?\]\(.*?\)')
EVENT_START = re.compile(r'^\*\s+\*\*')


def find_block_lines(lines, eid):
    """Return (start, end) 0-based line span of the event block carrying eid."""
    id_idx = next((i for i, l in enumerate(lines) if ID_RE.search(l)
                   and ID_RE.search(l).group(1) == eid), None)
    if id_idx is None:
        return None
    start = id_idx
    while start > 0 and not EVENT_START.match(lines[start]):
        start -= 1
    if not EVENT_START.match(lines[start]):
        return None
    end = id_idx + 1
    while end < len(lines):
        if EVENT_START.match(lines[end]) or lines[end].lstrip().startswith('###'):
            break
        end += 1
    while end > start and lines[end - 1].strip() == '':
        end -= 1
    return start, end


def cmd_get(args):
    for tag, path in (('VI', args.vi), ('EN', args.en)):
        if args.lang != 'both' and args.lang != tag.lower():
            continue
        with open(path, encoding='utf-8') as f:
            lines = f.readlines()
        span = find_block_lines(lines, args.eid)
        if span is None:
            print('%s: %s not found in %s' % (tag, args.eid, path))
            continue
        print('--- %s %s (%s lines %d-%d) ---' % (tag, args.eid, path, span[0] + 1, span[1]))
        for i in range(span[0], span[1]):
            print('%d: %s' % (i + 1, lines[i].rstrip('\n')))


def iter_events(path):
    blocks = parse_blocks(path)
    return [b for b in blocks if b['type'] == 'event']


def block_has_citation(block):
    if any(CITE_LINE.match((l.strip() if isinstance(l, str) else '')) for l in block['lines']):
        return True
    first = block['lines'][0] if block['lines'] else ''
    return bool(isinstance(first, str) and CITE_TRAIL.search(first))


def cmd_list_missing(args):
    evs = iter_events(args.vi)
    missing = []
    for b in evs:
        m = ID_RE.search(''.join(b['lines']))
        eid = m.group(1) if m else '?'
        if not block_has_citation(b):
            date = b.get('time_str', '?')
            first = b['lines'][0].strip() if b['lines'] else ''
            missing.append((eid, date, first[:90]))
    print('Events without citation: %d/%d' % (len(missing), len(evs)))
    show = missing if args.all else missing[:args.limit]
    for eid, date, first in show:
        print('%s | %s | %s' % (eid, date, first))


def block_is_complex(block):
    for l in block['lines'][1:]:
        s = l.strip() if isinstance(l, str) else ''
        if IMG_RE.search(s):
            return True
        if isinstance(l, str) and l.startswith((' ', '\t')) and s.startswith('*'):
            return True
    return False


def set_citation_in_block(block, cite, is_vi):
    """Replace existing citation (inline or standalone) or insert a new one.
    Returns True if the block was modified."""
    lines = block['lines']
    # 1. Drop standalone citation line(s).
    kept = [l for l in lines
            if not (isinstance(l, str) and CITE_LINE.match(l.strip()))]
    dropped = len(kept) != len(lines)
    # 2. Strip inline trailing citation from the description line.
    first = kept[0] if kept else ''
    m = CITE_TRAIL.search(first) if isinstance(first, str) else None
    if m:
        kept[0] = first[:m.start()].rstrip() + '\n'
        dropped = True
    # 3. Insert the new citation.
    new_block = {'type': 'event', 'time_str': block.get('time_str', ''), 'lines': kept}
    if block_is_complex(new_block):
        id_idx = next((i for i, l in enumerate(kept)
                       if isinstance(l, str) and ID_RE.search(l)), None)
        if id_idx is None:
            kept.extend(['\n', cite + '\n'])
        else:
            kept.insert(id_idx, cite + '\n')
            kept.insert(id_idx, '\n')
    else:
        kept[0] = kept[0].rstrip('\n').rstrip() + ' ' + cite.strip() + '\n'
    block['lines'] = kept
    return True


def cmd_set_source(args):
    for path, cite in ((args.vi, args.vi_cite), (args.en, args.en_cite)):
        if cite is None:
            continue
        blocks = parse_blocks(path)
        evs = [b for b in blocks if b['type'] == 'event']
        target = next((b for b in evs
                       if any(isinstance(l, str) and ID_RE.search(l)
                              and ID_RE.search(l).group(1) == args.eid
                              for l in b['lines'])), None)
        if target is None:
            print('%s not found in %s' % (args.eid, path))
            return 1
        set_citation_in_block(target, cite.strip(), path == args.vi)
        with open(path, 'w', encoding='utf-8') as f:
            for b in blocks:
                f.writelines(b['lines'])
        print('Updated citation for %s in %s' % (args.eid, path))
    run_quiet_verify()
    return 0


def next_id(vi_path, en_path):
    taken = set()
    for path in (vi_path, en_path):
        with open(path, encoding='utf-8') as f:
            for m in ID_RE.finditer(f.read()):
                taken.add(m.group(1))
    nums = [int(m.group(1)) for m in
            (re.match(r'EVT-(\d+)$', t) for t in taken) if m]
    return 'EVT-%04d' % ((max(nums) if nums else 0) + 1)


def cmd_add(args):
    eid = next_id(args.vi, args.en)
    for path, date, desc, src in ((args.vi, args.date_vi, args.desc_vi, args.source_vi),
                                  (args.en, args.date_en, args.desc_en, args.source_en)):
        with open(path, encoding='utf-8') as f:
            content = f.read()
        if not content.endswith('\n'):
            content += '\n'
        block = '*   **%s:** %s\n' % (date, desc)
        if src:
            # Simple new events carry the citation inline on the same line.
            block = block.rstrip('\n').rstrip() + ' ' + src.strip() + '\n'
        block += '\n<!-- id: %s -->\n' % eid
        content += '\n' + block
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Added %s to %s' % (eid, path))
    from sort_timelines import sort_timelines
    sort_timelines(args.vi, args.en, across_periods=True)
    run_quiet_verify()
    return 0


def run_quiet_verify():
    r = subprocess.run([sys.executable, 'verify_sync.py', '--quiet'],
                       capture_output=True, text=True)
    if r.stdout.strip():
        print(r.stdout.strip())
    if r.returncode != 0:
        print(r.stderr.strip())
        print('[timeline_cli] verify_sync FAILED — please inspect.')
    else:
        print('[timeline_cli] verify_sync passed.')
    return r.returncode


def main(argv=None):
    p = argparse.ArgumentParser(description='Token-friendly timeline accessor')
    p.add_argument('--vi', default=DEFAULT_VI)
    p.add_argument('--en', default=DEFAULT_EN)
    sub = p.add_subparsers(dest='cmd', required=True)

    g = sub.add_parser('get', help='Print one event block by stable ID')
    g.add_argument('eid')
    g.add_argument('--lang', choices=['vi', 'en', 'both'], default='both')

    lm = sub.add_parser('list-missing-source', help='List events without citation')
    lm.add_argument('--limit', type=int, default=30)
    lm.add_argument('--all', action='store_true')

    ss = sub.add_parser('set-source', help='Set/replace citation (inline or standalone)')
    ss.add_argument('eid')
    ss.add_argument('--vi-cite', default=None)
    ss.add_argument('--en-cite', default=None)

    ad = sub.add_parser('add', help='Add a new event pair, then sort + verify')
    ad.add_argument('--date-vi', required=True)
    ad.add_argument('--date-en', required=True)
    ad.add_argument('--desc-vi', required=True)
    ad.add_argument('--desc-en', required=True)
    ad.add_argument('--source-vi', default=None)
    ad.add_argument('--source-en', default=None)

    args = p.parse_args(argv)
    if args.cmd == 'get':
        cmd_get(args)
    elif args.cmd == 'list-missing-source':
        cmd_list_missing(args)
    elif args.cmd == 'set-source':
        if args.vi_cite is None and args.en_cite is None:
            print('Provide --vi-cite and/or --en-cite.')
            return 1
        return cmd_set_source(args)
    elif args.cmd == 'add':
        return cmd_add(args)
    return 0


if __name__ == '__main__':
    sys.exit(main())
