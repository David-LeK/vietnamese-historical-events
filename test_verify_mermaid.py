#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for verify_mermaid.py syntax validation engine.
"""

import unittest
from verify_mermaid import MermaidBlock, lint_mermaid_block


class TestMermaidValidator(unittest.TestCase):
    def test_valid_flowchart(self):
        lines = [
            (1, "flowchart TD"),
            (2, "    A[\"Start\"] --> B[\"Process\"]"),
            (3, "    B --> C[\"End\"]")
        ]
        block = MermaidBlock(1, 3, lines)
        lint_mermaid_block(block)
        self.assertEqual(len(block.errors), 0)
        self.assertEqual(block.diagram_type, "flowchart")
        self.assertEqual(block.orientation, "TD")

    def test_subgraph_pairing(self):
        # Balanced subgraphs
        lines = [
            (1, "flowchart LR"),
            (2, "    subgraph Group1 [\"Group 1\"]"),
            (3, "        A[\"Node A\"] --> B[\"Node B\"]"),
            (4, "    end")
        ]
        block = MermaidBlock(1, 4, lines)
        lint_mermaid_block(block)
        self.assertEqual(len(block.errors), 0)

        # Unclosed subgraph
        lines_unclosed = [
            (1, "flowchart LR"),
            (2, "    subgraph Group1 [\"Group 1\"]"),
            (3, "        A --> B")
        ]
        block_unclosed = MermaidBlock(1, 3, lines_unclosed)
        lint_mermaid_block(block_unclosed)
        self.assertTrue(any("Unclosed 'subgraph" in e.message for e in block_unclosed.errors))

        # Stray end
        lines_stray = [
            (1, "flowchart LR"),
            (2, "    A --> B"),
            (3, "    end")
        ]
        block_stray = MermaidBlock(1, 3, lines_stray)
        lint_mermaid_block(block_stray)
        self.assertTrue(any("Stray 'end'" in e.message for e in block_stray.errors))

    def test_quote_and_bracket_mismatch(self):
        # Odd double quotes
        lines_odd_quote = [
            (1, "flowchart TD"),
            (2, "    A[\"Unclosed string] --> B[\"Node\"]")
        ]
        block_odd = MermaidBlock(1, 2, lines_odd_quote)
        lint_mermaid_block(block_odd)
        self.assertTrue(len(block_odd.errors) > 0)

        # Mismatched brackets
        lines_mismatched = [
            (1, "flowchart TD"),
            (2, "    A[\"Label\" --> B[\"Node\"]")
        ]
        block_mismatched = MermaidBlock(1, 2, lines_mismatched)
        lint_mermaid_block(block_mismatched)
        self.assertTrue(any("Mismatched square brackets" in e.message for e in block_mismatched.errors))

    def test_invalid_arrow_in_flowchart(self):
        lines_arrow = [
            (1, "flowchart TD"),
            (2, "    A -> B")
        ]
        block_arrow = MermaidBlock(1, 2, lines_arrow)
        lint_mermaid_block(block_arrow)
        self.assertTrue(any("Invalid arrow syntax" in e.message for e in block_arrow.errors))

    def test_special_characters_in_quoted_labels(self):
        # Valid: characters like parentheses and colons inside double-quoted labels
        lines_vietnamese = [
            (1, "flowchart TD"),
            (2, "    P1[\"1. Vua Hùng (2879 TCN - 258 TCN)<br>Nước Văn Lang\"]:::ancient"),
            (3, "    --> P2[\"2. Nước Âu Lạc (257 TCN - 179 TCN): An Dương Vương\"]:::dyn")
        ]
        block = MermaidBlock(1, 3, lines_vietnamese)
        lint_mermaid_block(block, strict=True)
        self.assertEqual(len(block.errors), 0)
        self.assertEqual(len(block.warnings), 0)


if __name__ == "__main__":
    unittest.main()
