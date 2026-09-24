#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: verify_sync.py
Description: Cross-platform verification tool for Vietnamese Historical Events timelines.
             Verifies structure, event counts, date extraction, chronological sorting,
             and git modification parity between timelines_vi.md and timelines_en.md.

Usage:
    python verify_sync.py               # Run all structural, event-count, and sort checks
    python verify_sync.py --git-diff    # Compare git-modified lines between VI and EN files
    python verify_sync.py --check-only  # CI mode: strictly verify synchronization and sorting
"""

import sys
import os
import re
import io
import contextlib
import subprocess
from sort_timelines import parse_blocks, extract_date

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

VI_FILE = "timelines_vi.md"
EN_FILE = "timelines_en.md"

class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

# Disable colors on Windows if ANSI is not supported
if sys.platform == "win32" and "WT_SESSION" not in os.environ and "TERM" not in os.environ:
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        Colors.GREEN = ""
        Colors.RED = ""
        Colors.YELLOW = ""
        Colors.BLUE = ""
        Colors.BOLD = ""
        Colors.RESET = ""


def get_git_changed_lines(target_file):
    """
    Parses `git diff -U0` to extract modified line numbers for a given file.
    Returns a list of tuples: (start_line, count, line_str)
    """
    try:
        cmd = ["git", "diff", "-U0", target_file]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding="utf-8", errors="replace")
    except Exception:
        return []

    changes = []
    for line in res.stdout.splitlines():
        if line.startswith("@@"):
            # Header format: @@ -from,len +to,len @@
            m = re.search(r'\+([0-9]+)(?:,([0-9]+))?', line)
            if m:
                start = int(m.group(1))
                count = int(m.group(2)) if m.group(2) is not None else 1
                if count == 0 or count == 1:
                    line_str = f"{start}"
                else:
                    end = start + count - 1
                    line_str = f"{start}->{end}"
                changes.append(line_str)
    return changes


def check_git_diff_parity():
    """
    Compares git diff modified lines between VI and EN files (cross-platform compare.bat).
    """
    print(f"\n{Colors.BOLD}[1/6] Checking Git Diff Parity...{Colors.RESET}")
    changes_vi = get_git_changed_lines(VI_FILE)
    changes_en = get_git_changed_lines(EN_FILE)

    str_vi = ", ".join(changes_vi) if changes_vi else "None"
    str_en = ", ".join(changes_en) if changes_en else "None"

    if str_vi == str_en:
        if str_vi == "None":
            print(f"  {Colors.GREEN}[OK] No uncommitted git changes detected in timeline files.{Colors.RESET}")
        else:
            print(f"  {Colors.GREEN}[OK] Both files have identical modified line ranges: {str_vi}{Colors.RESET}")
        return True
    else:
        print(f"  {Colors.RED}[FAIL] Files have changes on different lines:{Colors.RESET}")
        print(f"    - {VI_FILE}: {str_vi}")
        print(f"    - {EN_FILE}: {str_en}")
        return False


def verify_structure_and_counts():
    """
    Verifies that both timeline files exist, have matching headers, and matching event counts.
    """
    print(f"\n{Colors.BOLD}[2/6] Verifying Section Structure & Event Counts...{Colors.RESET}")
    if not os.path.isfile(VI_FILE):
        print(f"  {Colors.RED}[FAIL] Missing required file: {VI_FILE}{Colors.RESET}")
        return False, [], []
    if not os.path.isfile(EN_FILE):
        print(f"  {Colors.RED}[FAIL] Missing required file: {EN_FILE}{Colors.RESET}")
        return False, [], []

    blocks_vi = parse_blocks(VI_FILE)
    blocks_en = parse_blocks(EN_FILE)

    events_vi = [b for b in blocks_vi if b['type'] == 'event']
    events_en = [b for b in blocks_en if b['type'] == 'event']
    headers_vi = [b for b in blocks_vi if b['type'] == 'header']
    headers_en = [b for b in blocks_en if b['type'] == 'header']

    has_errors = False

    print(f"  - Total events: VI = {len(events_vi)}, EN = {len(events_en)}")
    print(f"  - Total headers: VI = {len(headers_vi)}, EN = {len(headers_en)}")

    if len(events_vi) != len(events_en):
        print(f"  {Colors.RED}[FAIL] Total event count mismatch: VI has {len(events_vi)} events, EN has {len(events_en)} events.{Colors.RESET}")
        has_errors = True
    else:
        print(f"  {Colors.GREEN}[OK] Total event count matches ({len(events_vi)} events).{Colors.RESET}")

    if len(headers_vi) != len(headers_en):
        print(f"  {Colors.RED}[FAIL] Total header count mismatch: VI has {len(headers_vi)} headers, EN has {len(headers_en)} headers.{Colors.RESET}")
        has_errors = True
    else:
        print(f"  {Colors.GREEN}[OK] Total header count matches ({len(headers_vi)} headers).{Colors.RESET}")

    # Section-by-section breakdown
    sections_vi = []
    sections_en = []
    curr_v, curr_e = [], []

    for b in blocks_vi:
        if b['type'] == 'header':
            if curr_v:
                sections_vi.append(curr_v)
            curr_v = [b]
        else:
            curr_v.append(b)
    if curr_v:
        sections_vi.append(curr_v)

    for b in blocks_en:
        if b['type'] == 'header':
            if curr_e:
                sections_en.append(curr_e)
            curr_e = [b]
        else:
            curr_e.append(b)
    if curr_e:
        sections_en.append(curr_e)

    if len(sections_vi) == len(sections_en):
        for idx, (sec_v, sec_e) in enumerate(zip(sections_vi, sections_en)):
            hdr_v = sec_v[0]['lines'][0].strip()
            hdr_e = sec_e[0]['lines'][0].strip()
            ev_v = [b for b in sec_v if b['type'] == 'event']
            ev_e = [b for b in sec_e if b['type'] == 'event']
            if len(ev_v) != len(ev_e):
                print(f"  {Colors.RED}[FAIL] Section {idx + 1} mismatch: VI ({len(ev_v)} events) vs EN ({len(ev_e)} events){Colors.RESET}")
                print(f"    VI Header: {hdr_v}")
                print(f"    EN Header: {hdr_e}")
                has_errors = True
        if not has_errors:
            print(f"  {Colors.GREEN}[OK] All {len(sections_vi)} sections have identical event counts.{Colors.RESET}")
    else:
        has_errors = True

    return not has_errors, blocks_vi, blocks_en


def verify_date_parsing_and_sorting(blocks_vi, blocks_en):
    """
    Verifies that all events have extractable dates and are correctly sorted in chronological order.
    """
    print(f"\n{Colors.BOLD}[3/6] Verifying Date Extraction & Chronological Order...{Colors.RESET}")
    events_vi = [b for b in blocks_vi if b['type'] == 'event']
    events_en = [b for b in blocks_en if b['type'] == 'event']

    has_errors = False

    # 1. Date extraction verification
    for idx, ev in enumerate(events_vi):
        t_str = ev.get('time_str', '').strip()
        if not t_str:
            print(f"  {Colors.RED}[FAIL] VI Event #{idx+1} has empty date header: {ev['lines'][0].strip()}{Colors.RESET}")
            has_errors = True
        try:
            d_val = extract_date(t_str)
        except Exception as ex:
            print(f"  {Colors.RED}[FAIL] VI Event #{idx+1} failed date parsing '{t_str}': {ex}{Colors.RESET}")
            has_errors = True

    for idx, ev in enumerate(events_en):
        t_str = ev.get('time_str', '').strip()
        if not t_str:
            print(f"  {Colors.RED}[FAIL] EN Event #{idx+1} has empty date header: {ev['lines'][0].strip()}{Colors.RESET}")
            has_errors = True
        try:
            d_val = extract_date(t_str)
        except Exception as ex:
            print(f"  {Colors.RED}[FAIL] EN Event #{idx+1} failed date parsing '{t_str}': {ex}{Colors.RESET}")
            has_errors = True

    if not has_errors:
        print(f"  {Colors.GREEN}[OK] All date strings parsed successfully.{Colors.RESET}")

    # 2. Chronological order check
    prev_date = -1e9
    prev_event = None
    unsorted_count = 0

    for idx, ev in enumerate(events_vi):
        d_val = extract_date(ev['time_str'])
        if d_val < prev_date:
            unsorted_count += 1
            if unsorted_count <= 5: # Limit error output to first 5
                print(f"  {Colors.RED}[FAIL] VI Event #{idx+1} out of order:{Colors.RESET}")
                print(f"    Previous ({prev_date}): {prev_event['lines'][0].strip() if prev_event else ''}")
                print(f"    Current  ({d_val}): {ev['lines'][0].strip()}")
        prev_date = d_val
        prev_event = ev

    if unsorted_count > 0:
        print(f"  {Colors.RED}[FAIL] Found {unsorted_count} event(s) out of chronological order in {VI_FILE}.{Colors.RESET}")
        print(f"  {Colors.YELLOW}-> Please run 'python sort_timelines.py' to automatically sort all events.{Colors.RESET}")
        has_errors = True
    else:
        print(f"  {Colors.GREEN}[OK] All events are in strictly non-descending chronological order.{Colors.RESET}")

    return not has_errors


def verify_markdown_syntax(blocks_vi, blocks_en):
    """
    Checks for common markdown formatting issues: bold date formatting, line structure.
    """
    print(f"\n{Colors.BOLD}[4/6] Verifying Markdown Syntax & Format...{Colors.RESET}")
    has_errors = False
    events_vi = [b for b in blocks_vi if b['type'] == 'event']
    events_en = [b for b in blocks_en if b['type'] == 'event']

    for idx, ev in enumerate(events_vi):
        line = ev['lines'][0]
        if not re.match(r'^\*\s+\*\*(.*?):\*\*\s+', line):
            print(f"  {Colors.YELLOW}[WARN] VI Event #{idx+1} missing space after colon or unexpected format: {line.strip()}{Colors.RESET}")

    for idx, ev in enumerate(events_en):
        line = ev['lines'][0]
        if not re.match(r'^\*\s+\*\*(.*?):\*\*\s+', line):
            print(f"  {Colors.YELLOW}[WARN] EN Event #{idx+1} missing space after colon or unexpected format: {line.strip()}{Colors.RESET}")

    print(f"  {Colors.GREEN}[OK] Markdown formatting check completed.{Colors.RESET}")
    return not has_errors


def verify_images_sync(events_vi, events_en):
    """
    Verifies that images embedded in VI and EN events are synchronized.
    """
    img_regex = re.compile(r'!\[.*?\]\((.*?)\)')
    mismatches = 0
    total_imgs_vi = 0
    total_imgs_en = 0
    for idx, (ev_v, ev_e) in enumerate(zip(events_vi, events_en)):
        imgs_v = []
        for l in ev_v['lines']:
            imgs_v.extend(img_regex.findall(l))
        imgs_e = []
        for l in ev_e['lines']:
            imgs_e.extend(img_regex.findall(l))
        total_imgs_vi += len(imgs_v)
        total_imgs_en += len(imgs_e)
        if imgs_v != imgs_e:
            mismatches += 1
            if mismatches <= 5:
                print(f"  {Colors.RED}[FAIL] Event #{idx+1} image mismatch:{Colors.RESET}")
                print(f"    VI images: {imgs_v}")
                print(f"    EN images: {imgs_e}")
    if mismatches > 0:
        print(f"  {Colors.RED}[FAIL] Found {mismatches} event(s) with mismatched images.{Colors.RESET}")
        return False
    if total_imgs_vi > 0:
        print(f"  {Colors.GREEN}[OK] Verified {total_imgs_vi} embedded image(s) across events (VI and EN fully in sync).{Colors.RESET}")
    return True


def verify_event_sources_sync(events_vi, events_en):
    """
    Verifies per-event citations (`[Nguồn: ...]` in VI, `[Source: ...]` in EN).
    Compares PRESENCE only (texts differ by language by design). Events missing
    a source on both sides are allowed (gradual rollout); a source on only one
    side is a [FAIL] bilingual-parity violation.
    """
    print(f"\n{Colors.BOLD}[5/6] Verifying Event Citations ([Nguồn: ...] / [Source: ...])...{Colors.RESET}")
    src_line_re = re.compile(r'^\[(?:Nguồn|Source)\s*:', re.IGNORECASE)
    src_trail_re = re.compile(r'\[(?:Nguồn|Source)\s*:.*?\]\s*$', re.IGNORECASE)

    def has_src(ev):
        for l in ev['lines']:
            s = l.strip() if isinstance(l, str) else ''
            if src_line_re.match(s):
                return True
        first = ev['lines'][0] if ev['lines'] else ''
        if isinstance(first, str) and src_trail_re.search(first):
            return True
        return False

    mismatches = 0
    with_src = 0
    standalone = 0
    for idx, (ev_v, ev_e) in enumerate(zip(events_vi, events_en)):
        for ev, lang in ((ev_v, 'VI'), (ev_e, 'EN')):
            for l in ev['lines']:
                s = l.strip() if isinstance(l, str) else ''
                if src_line_re.match(s):
                    standalone += 1
                    if standalone <= 5:
                        print(f"  {Colors.RED}[FAIL] {lang} event has a standalone citation line (must be inline at end of description):{Colors.RESET}")
                        print(f"    {ev['lines'][0].strip()[:100]}")
                    break
        has_v, has_e = has_src(ev_v), has_src(ev_e)
        if has_v and has_e:
            with_src += 1
        elif has_v != has_e:
            mismatches += 1
            if mismatches <= 5:
                print(f"  {Colors.RED}[FAIL] Event #{idx+1} has a citation on only one side (VI={has_v}, EN={has_e}):{Colors.RESET}")
                print(f"    VI: {ev_v['lines'][0].strip()[:100]}")
                print(f"    EN: {ev_e['lines'][0].strip()[:100]}")
    total = len(events_vi)
    print(f"  - Events with bilingual citations: {with_src}/{total}")
    if mismatches > 0:
        print(f"  {Colors.RED}[FAIL] Found {mismatches} event(s) with one-sided citations. Add the missing `[Nguồn: ...]` / `[Source: ...]` line.{Colors.RESET}")
        return False
    if standalone > 0:
        print(f"  {Colors.RED}[FAIL] Found {standalone} event(s) with standalone citation lines. Move each citation inline to the end of its description line.{Colors.RESET}")
        return False
    print(f"  {Colors.GREEN}[OK] Event citations are in sync (present on both sides or absent on both).{Colors.RESET}")
    return True


def verify_event_ids(events_vi, events_en):
    """
    Verifies stable event IDs (`<!-- id: EVT-XXXX -->`): exactly one per
    event, unique within each file, and identical for paired VI/EN events.
    """
    print(f"\n{Colors.BOLD}[6/6] Verifying Stable Event IDs...{Colors.RESET}")
    id_re = re.compile(r'<!--\s*id:\s*([A-Za-z0-9_-]+)\s*-->')
    has_errors = False
    seen_vi, seen_en = {}, {}
    shown = 0

    def collect(ev):
        out = []
        for l in ev['lines']:
            if isinstance(l, str):
                m = id_re.search(l)
                if m:
                    out.append(m.group(1))
        return out

    for idx, (ev_v, ev_e) in enumerate(zip(events_vi, events_en)):
        ids_v, ids_e = collect(ev_v), collect(ev_e)
        if len(ids_v) != 1 or len(ids_e) != 1:
            has_errors = True
            if shown < 5:
                print(f"  {Colors.RED}[FAIL] Event #{idx+1} must carry exactly one ID comment (VI={ids_v}, EN={ids_e}):{Colors.RESET}")
                print(f"    VI: {ev_v['lines'][0].strip()[:100]}")
                shown += 1
            continue
        for eid, seen, tag in ((ids_v[0], seen_vi, 'VI'), (ids_e[0], seen_en, 'EN')):
            if eid in seen:
                has_errors = True
                if shown < 5:
                    print(f"  {Colors.RED}[FAIL] Duplicate ID {eid} in {tag} (events #{seen[eid]+1} and #{idx+1}).{Colors.RESET}")
                    shown += 1
            else:
                seen[eid] = idx
        if ids_v[0] != ids_e[0]:
            has_errors = True
            if shown < 5:
                print(f"  {Colors.RED}[FAIL] Event #{idx+1} ID mismatch: VI={ids_v[0]}, EN={ids_e[0]}.{Colors.RESET}")
                shown += 1

    print(f"  - Stable IDs: VI = {len(seen_vi)}, EN = {len(seen_en)}")
    if has_errors:
        print(f"  {Colors.RED}[FAIL] Event ID check failed. Use timeline_cli.py to inspect/fix IDs.{Colors.RESET}")
        return False
    print(f"  {Colors.GREEN}[OK] All paired events share one unique stable ID.{Colors.RESET}")
    return True


def run_checks():
    check_only = "--check-only" in sys.argv
    git_diff_only = "--git-diff" in sys.argv

    if git_diff_only:
        return 0 if check_git_diff_parity() else 1

    struct_ok, blocks_vi, blocks_en = verify_structure_and_counts()
    if not struct_ok:
        print(f"\n{Colors.RED}[FAIL] Structure verification FAILED. Please ensure both files have matching events.{Colors.RESET}\n")
        return 1

    sort_ok = verify_date_parsing_and_sorting(blocks_vi, blocks_en)
    syntax_ok = verify_markdown_syntax(blocks_vi, blocks_en)
    events_vi = [b for b in blocks_vi if b['type'] == 'event']
    events_en = [b for b in blocks_en if b['type'] == 'event']
    images_ok = verify_images_sync(events_vi, events_en)
    sources_ok = verify_event_sources_sync(events_vi, events_en)
    ids_ok = verify_event_ids(events_vi, events_en)

    if not check_only:
        check_git_diff_parity()

    if struct_ok and sort_ok and syntax_ok and images_ok and sources_ok and ids_ok:
        print(f"\n{Colors.BOLD}{Colors.GREEN}[SUCCESS] ALL CHECKS PASSED! Timelines are synchronized and valid.{Colors.RESET}\n")
        return 0
    else:
        print(f"\n{Colors.BOLD}{Colors.RED}[FAIL] SOME CHECKS FAILED. Please resolve the errors above.{Colors.RESET}\n")
        return 1


def main():
    quiet = "--quiet" in sys.argv
    if not quiet:
        print(f"{Colors.BOLD}{Colors.BLUE}======================================================{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}   Vietnamese Historical Events - Synchronization Check {Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}======================================================{Colors.RESET}")

    if quiet:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = run_checks()
        for line in buf.getvalue().splitlines():
            if "[OK]" in line:
                continue
            if line.startswith("  - "):
                continue
            print(line)
    else:
        code = run_checks()
    sys.exit(code)


if __name__ == "__main__":
    main()
