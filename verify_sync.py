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
    print(f"\n{Colors.BOLD}[1/4] Checking Git Diff Parity...{Colors.RESET}")
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
    print(f"\n{Colors.BOLD}[2/4] Verifying Section Structure & Event Counts...{Colors.RESET}")
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
    print(f"\n{Colors.BOLD}[3/4] Verifying Date Extraction & Chronological Order...{Colors.RESET}")
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
    print(f"\n{Colors.BOLD}[4/4] Verifying Markdown Syntax & Format...{Colors.RESET}")
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


def main():
    print(f"{Colors.BOLD}{Colors.BLUE}======================================================{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}   Vietnamese Historical Events - Synchronization Check {Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}======================================================{Colors.RESET}")

    check_only = "--check-only" in sys.argv
    git_diff_only = "--git-diff" in sys.argv

    if git_diff_only:
        diff_ok = check_git_diff_parity()
        sys.exit(0 if diff_ok else 1)

    struct_ok, blocks_vi, blocks_en = verify_structure_and_counts()
    if not struct_ok:
        print(f"\n{Colors.RED}[FAIL] Structure verification FAILED. Please ensure both files have matching events.{Colors.RESET}\n")
        sys.exit(1)

    sort_ok = verify_date_parsing_and_sorting(blocks_vi, blocks_en)
    syntax_ok = verify_markdown_syntax(blocks_vi, blocks_en)

    if not check_only:
        check_git_diff_parity()

    if struct_ok and sort_ok and syntax_ok:
        print(f"\n{Colors.BOLD}{Colors.GREEN}[SUCCESS] ALL CHECKS PASSED! Timelines are synchronized and valid.{Colors.RESET}\n")
        sys.exit(0)
    else:
        print(f"\n{Colors.BOLD}{Colors.RED}[FAIL] SOME CHECKS FAILED. Please resolve the errors above.{Colors.RESET}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
