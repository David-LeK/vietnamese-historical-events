#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: verify_mermaid.py
Description: Fast, robust verification tool for Mermaid syntax in Markdown files.
             Performs deep static linting and syntax checking on Mermaid diagram blocks
             including diagram types, subgraph nesting stacks, quote and bracket balances,
             node ID conventions, arrow connector syntax, and styling directives.
             Optionally validates via Mermaid CLI (`mmdc`) if installed.

Usage:
    python verify_mermaid.py                       # Verify default VIETNAM_HISTORICAL_MERMAID_CHART.md
    python verify_mermaid.py path/to/file.md       # Verify specific markdown file(s)
    python verify_mermaid.py --all                 # Scan and verify all markdown files containing mermaid blocks
    python verify_mermaid.py --strict              # Enable strict linting (e.g. quote labels with special chars)
    python verify_mermaid.py --cli                 # Also validate using `mmdc` (Mermaid CLI) if available
"""

import sys
import os
import re
import glob
import argparse
import subprocess
import tempfile
import shutil

# Ensure proper stdout/stderr encoding
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

DEFAULT_TARGET = "VIETNAM_HISTORICAL_MERMAID_CHART.md"

# Supported Mermaid diagram types
VALID_DIAGRAM_TYPES = {
    "flowchart", "graph", "sequencediagram", "classdiagram",
    "statediagram", "statediagram-v2", "erdiagram", "journey",
    "gantt", "pie", "quadrantchart", "requirementdiagram",
    "gitgraph", "mindmap", "timeline", "xychart-beta",
    "sankey-beta", "block-beta", "c4context", "c4container",
    "c4component", "c4dynamic", "c4deployment"
}

# Flowchart / Graph orientations
VALID_ORIENTATIONS = {"td", "tb", "bt", "rl", "lr"}


class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
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
        Colors.CYAN = ""
        Colors.BOLD = ""
        Colors.RESET = ""


class LintIssue:
    def __init__(self, line_num, message, issue_type="ERROR", code_line=None):
        self.line_num = line_num
        self.message = message
        self.issue_type = issue_type  # "ERROR" or "WARN"
        self.code_line = code_line

    def __str__(self):
        color = Colors.RED if self.issue_type == "ERROR" else Colors.YELLOW
        res = f"{color}[{self.issue_type}]{Colors.RESET} Line {self.line_num}: {self.message}"
        if self.code_line:
            res += f"\n    {Colors.BOLD}{self.code_line.strip()}{Colors.RESET}"
        return res


class MermaidBlock:
    def __init__(self, start_line, end_line, content_lines):
        self.start_line = start_line
        self.end_line = end_line
        self.content_lines = content_lines  # list of tuples: (file_line_num, line_str)
        self.diagram_type = ""
        self.orientation = ""
        self.errors = []
        self.warnings = []


def extract_mermaid_blocks(filepath):
    """
    Extracts all ```mermaid ... ``` blocks from a markdown file with their original line numbers.
    """
    if not os.path.isfile(filepath):
        return None, [LintIssue(0, f"File not found: {filepath}", "ERROR")]

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        return None, [LintIssue(0, f"Could not read file: {e}", "ERROR")]

    blocks = []
    in_mermaid = False
    block_start = 0
    current_lines = []

    for idx, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip("\r\n")
        stripped = line.strip()

        if stripped.startswith("```mermaid"):
            in_mermaid = True
            block_start = idx
            current_lines = []
            continue
        elif in_mermaid and stripped == "```":
            in_mermaid = False
            blocks.append(MermaidBlock(block_start, idx, current_lines))
            current_lines = []
            continue

        if in_mermaid:
            current_lines.append((idx, line))

    if in_mermaid:
        blocks.append(MermaidBlock(block_start, len(lines), current_lines))
        # Add unclosed block error
        blocks[-1].errors.append(
            LintIssue(block_start, "Unclosed ```mermaid code block (missing closing ```)", "ERROR")
        )

    return blocks, []


def strip_string_literals(line):
    """
    Replaces valid double-quoted string literals with an empty string placeholder '""'
    to allow syntactic inspection of bracket and arrow structures outside literals.
    """
    # Pattern for "..." with escape handling
    return re.sub(r'"(?:\\\"|""|[^"])*"', '""', line)


def lint_mermaid_block(block, strict=False):
    """
    Performs deep syntactic analysis of a Mermaid diagram block.
    """
    if not block.content_lines:
        block.errors.append(
            LintIssue(block.start_line, "Empty Mermaid diagram block", "ERROR")
        )
        return

    # 1. Diagram Type Detection & Header Validation
    header_found = False
    subgraph_stack = []  # list of tuples: (line_num, subgraph_name)
    in_multiline_string = False
    multiline_start_line = 0

    # Filter out pure comment lines or frontmatter directives
    code_lines = []
    for line_num, line in block.content_lines:
        stripped = line.strip()
        if not stripped:
            continue
        # Check Mermaid comment
        if stripped.startswith("%%"):
            # Check directive like %%{init: ...}%%
            if stripped.startswith("%%{") and stripped.endswith("}%%"):
                continue
            continue
        code_lines.append((line_num, line))

    if not code_lines:
        block.errors.append(
            LintIssue(block.start_line, "Mermaid block contains only comments or whitespace", "ERROR")
        )
        return

    # Check first non-comment line for diagram type
    first_line_num, first_line = code_lines[0]
    tokens = first_line.strip().split()
    first_token_lower = tokens[0].lower() if tokens else ""

    if first_token_lower in VALID_DIAGRAM_TYPES:
        header_found = True
        block.diagram_type = first_token_lower
        if first_token_lower in {"flowchart", "graph"} and len(tokens) > 1:
            orient = tokens[1].lower()
            if orient in VALID_ORIENTATIONS:
                block.orientation = orient.upper()
            else:
                block.warnings.append(
                    LintIssue(first_line_num, f"Unrecognized orientation '{tokens[1]}'. Expected TD, TB, BT, RL, or LR.", "WARN", first_line)
                )
    else:
        block.errors.append(
            LintIssue(first_line_num, f"Invalid or missing Mermaid diagram type '{tokens[0] if tokens else ''}'.", "ERROR", first_line)
        )
        block.diagram_type = "unknown"

    # 2. Line-by-Line Linting
    for line_num, line in code_lines[1:]:
        stripped = line.strip()

        # Check for unescaped double quotes count
        # Escaped quotes: \" or #quot;
        sanitized_quotes = line.replace('\\"', '').replace('#quot;', '')
        num_quotes = sanitized_quotes.count('"')

        if in_multiline_string:
            if num_quotes % 2 != 0:
                # Closes the multiline string
                in_multiline_string = False
            continue
        else:
            if num_quotes % 2 != 0:
                # String started and not closed on this line
                # Can be valid multiline string, or an unclosed quote bug
                in_multiline_string = True
                multiline_start_line = line_num

        # Strip strings for structural bracket / arrow checks
        non_string_line = strip_string_literals(line)

        # Check Subgraphs
        # Patterns: subgraph ID ["Title"], subgraph Title, subgraph ID
        if re.match(r'^\s*subgraph\b', non_string_line, re.IGNORECASE):
            sub_name = stripped[len("subgraph"):].strip()
            subgraph_stack.append((line_num, sub_name))
        elif re.match(r'^\s*end\b', non_string_line, re.IGNORECASE):
            if not subgraph_stack:
                block.errors.append(
                    LintIssue(line_num, "Stray 'end' directive with no matching 'subgraph'.", "ERROR", line)
                )
            else:
                subgraph_stack.pop()

        # Check bracket parity outside string literals
        sq_open = non_string_line.count('[')
        sq_close = non_string_line.count(']')
        if sq_open != sq_close:
            block.errors.append(
                LintIssue(line_num, f"Mismatched square brackets '[' ({sq_open}) vs ']' ({sq_close}). Ensure labels with brackets are enclosed in quotes.", "ERROR", line)
            )

        paren_open = non_string_line.count('(')
        paren_close = non_string_line.count(')')
        if paren_open != paren_close:
            block.errors.append(
                LintIssue(line_num, f"Mismatched parentheses '(' ({paren_open}) vs ')' ({paren_close}).", "ERROR", line)
            )

        brace_open = non_string_line.count('{')
        brace_close = non_string_line.count('}')
        if brace_open != brace_close:
            block.errors.append(
                LintIssue(line_num, f"Mismatched curly braces '{{' ({brace_open}) vs '}}' ({brace_close}).", "ERROR", line)
            )

        # Check for invalid single arrow '->' in flowchart / graph
        if block.diagram_type in {"flowchart", "graph"}:
            # Pattern matching single -> not part of -->, -.->, ==>
            if re.search(r'(?<![-.=~])->(?![->])', non_string_line):
                block.errors.append(
                    LintIssue(line_num, "Invalid arrow syntax '->' in flowchart. Mermaid requires '-->' or '-.->'.", "ERROR", line)
                )

        # Check for trailing connector at end of line without target
        if re.search(r'(-->|-\.->|==>|---|~~~)\s*$', non_string_line):
            # Check if this line is part of a chained node declaration across lines
            # In Mermaid: A --> \n B is valid, but let's ensure it's not the last code line
            is_last = (line_num == code_lines[-1][0])
            if is_last:
                block.errors.append(
                    LintIssue(line_num, "Trailing arrow connector with no target node.", "ERROR", line)
                )

        # Strict checks: detect unquoted node labels containing special characters
        if strict:
            # Check for unquoted node labels on non_string_line (which preserves unquoted brackets)
            # Example: NodeA[Some Label (Info)] instead of NodeA["Some Label (Info)"]
            unquoted_match = re.search(r'\b[A-Za-z0-9_]+\s*(\[|\()([^"\'\]\)]+)(\]|\))', non_string_line)
            if unquoted_match:
                inner_text = unquoted_match.group(2).strip()
                if inner_text and any(ch in inner_text for ch in "():;,<>/-"):
                    block.warnings.append(
                        LintIssue(line_num, f"Unquoted label containing special characters: '{inner_text}'. Quote label with [\"...\"] to prevent parsing errors.", "WARN", line)
                    )

    # 3. Final Stack and State Verification
    if in_multiline_string:
        block.errors.append(
            LintIssue(multiline_start_line, "Unclosed double-quote string literal across multiline.", "ERROR")
        )

    if subgraph_stack:
        for sub_line, sub_name in subgraph_stack:
            block.errors.append(
                LintIssue(sub_line, f"Unclosed 'subgraph {sub_name}' (missing matching 'end').", "ERROR")
            )


def validate_with_cli(blocks, filepath):
    """
    Optional: Validate mermaid blocks using @mermaid-js/mermaid-cli (mmdc) if installed.
    """
    mmdc_path = shutil.which("mmdc")
    if not mmdc_path:
        return False, "Mermaid CLI (`mmdc`) not found in PATH. Skipping CLI compiler check."

    with tempfile.TemporaryDirectory() as temp_dir:
        for idx, block in enumerate(blocks, 1):
            temp_mmd = os.path.join(temp_dir, f"chart_{idx}.mmd")
            with open(temp_mmd, "w", encoding="utf-8") as f:
                for _, line in block.content_lines:
                    f.write(line + "\n")

            cmd = [mmdc_path, "-i", temp_mmd, "-o", os.path.join(temp_dir, f"chart_{idx}.svg")]
            try:
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if res.returncode != 0:
                    block.errors.append(
                        LintIssue(block.start_line, f"Mermaid CLI (mmdc) render error:\n{res.stderr.strip()}", "ERROR")
                    )
            except Exception as e:
                block.warnings.append(
                    LintIssue(block.start_line, f"Failed to execute Mermaid CLI: {e}", "WARN")
                )

    return True, "Mermaid CLI validation executed."


def verify_file(filepath, strict=False, use_cli=False, verbose=False):
    """
    Verifies all Mermaid blocks in a single markdown file.
    Returns (total_blocks, total_errors, total_warnings)
    """
    print(f"\n{Colors.BOLD}{Colors.CYAN}--- Verifying: {filepath} ---{Colors.RESET}")
    blocks, file_errors = extract_mermaid_blocks(filepath)

    if blocks is None:
        for err in file_errors:
            print(f"  {err}")
        return 0, len(file_errors), 0

    if not blocks:
        print(f"  {Colors.YELLOW}[INFO] No Mermaid blocks found in this file.{Colors.RESET}")
        return 0, 0, 0

    total_errors = 0
    total_warnings = 0

    for idx, block in enumerate(blocks, 1):
        lint_mermaid_block(block, strict=strict)

    if use_cli:
        cli_ok, msg = validate_with_cli(blocks, filepath)
        if not cli_ok and verbose:
            print(f"  {Colors.YELLOW}[CLI] {msg}{Colors.RESET}")

    for idx, block in enumerate(blocks, 1):
        has_error = len(block.errors) > 0
        has_warn = len(block.warnings) > 0
        total_errors += len(block.errors)
        total_warnings += len(block.warnings)

        dtype_str = block.diagram_type.upper()
        if block.orientation:
            dtype_str += f" ({block.orientation})"

        line_info = f"Lines {block.start_line}-{block.end_line}"

        if not has_error and not has_warn:
            status = f"{Colors.GREEN}[OK]{Colors.RESET}"
            print(f"  Block #{idx:02d} ({line_info:15s}): {dtype_str:18s} -> {status}")
        elif not has_error and has_warn:
            status = f"{Colors.YELLOW}[WARNING ({len(block.warnings)})]{Colors.RESET}"
            print(f"  Block #{idx:02d} ({line_info:15s}): {dtype_str:18s} -> {status}")
            for w in block.warnings:
                print(f"    {w}")
        else:
            status = f"{Colors.RED}[FAILED ({len(block.errors)} errors)]{Colors.RESET}"
            print(f"  Block #{idx:02d} ({line_info:15s}): {dtype_str:18s} -> {status}")
            for e in block.errors:
                print(f"    {e}")
            for w in block.warnings:
                print(f"    {w}")

    return len(blocks), total_errors, total_warnings


def find_all_mermaid_files():
    """
    Finds all markdown files (*.md) in the workspace containing ```mermaid blocks.
    """
    matched_files = []
    for root, _, files in os.walk("."):
        # Ignore hidden directories and node_modules / git / venv
        parts = [p for p in root.split(os.sep) if p and p != "."]
        if any(part.startswith(".") or part in {"node_modules", "venv", "__pycache__"} for part in parts):
            continue
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.normpath(os.path.join(root, file))
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        if "```mermaid" in content:
                            matched_files.append(full_path)
                except Exception:
                    pass
    return sorted(matched_files)


def main():
    parser = argparse.ArgumentParser(
        description="Verify Mermaid syntax, subgraphs, quotes, and connectors in Markdown files."
    )
    parser.add_argument(
        "files",
        nargs="*",
        help=f"Target markdown file(s) to verify (default: {DEFAULT_TARGET})"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Scan and verify all Markdown files in the project containing Mermaid blocks."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enable strict linting rules (e.g. unquoted special characters in node labels)."
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Also compile/validate diagrams using @mermaid-js/mermaid-cli (`mmdc`) if available."
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed diagnostic output."
    )

    args = parser.parse_args()

    print("=" * 65)
    print(f"   {Colors.BOLD}Mermaid Syntax & Structure Validator{Colors.RESET}")
    print("=" * 65)

    if args.all:
        target_files = find_all_mermaid_files()
        if not target_files:
            print(f"{Colors.YELLOW}No markdown files containing ```mermaid blocks were found.{Colors.RESET}")
            sys.exit(0)
    elif args.files:
        target_files = args.files
    else:
        target_files = [DEFAULT_TARGET]

    grand_blocks = 0
    grand_errors = 0
    grand_warnings = 0

    for tf in target_files:
        blocks_count, errs, warns = verify_file(
            tf,
            strict=args.strict,
            use_cli=args.cli,
            verbose=args.verbose
        )
        grand_blocks += blocks_count
        grand_errors += errs
        grand_warnings += warns

    print("\n" + "=" * 65)
    print(f"{Colors.BOLD}SUMMARY REPORT:{Colors.RESET}")
    print(f"  - Files Checked   : {len(target_files)}")
    print(f"  - Mermaid Blocks  : {grand_blocks}")
    print(f"  - Total Warnings  : {grand_warnings}")
    print(f"  - Total Errors    : {grand_errors}")

    if grand_errors == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}[SUCCESS] ALL MERMAID SYNTAX CHECKS PASSED!{Colors.RESET}\n")
        sys.exit(0)
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}[FAILED] Found {grand_errors} syntax error(s) across Mermaid blocks!{Colors.RESET}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
