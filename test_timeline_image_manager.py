#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unit tests for timeline_image_manager.py CLI and core methods.
"""

import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from PIL import Image

import timeline_image_manager
from timeline_image_manager import TimelineImageManager, cli_main


class TestTimelineImageManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.orig_images_dir = timeline_image_manager.IMAGES_DIR
        self.orig_json_file = timeline_image_manager.JSON_FILE
        self.orig_vi_file = timeline_image_manager.VI_FILE
        self.orig_en_file = timeline_image_manager.EN_FILE

        timeline_image_manager.IMAGES_DIR = self.test_dir / "images"
        timeline_image_manager.JSON_FILE = self.test_dir / "timeline_images.json"

        # Create dummy timeline files
        self.test_vi = self.test_dir / "timelines_vi.md"
        self.test_en = self.test_dir / "timelines_en.md"

        self.test_vi.write_text(
            "### I. ERA ONE\n\n* **02/09/1945**: Bac Ho doc Tuyen ngon Doc lap.\n",
            encoding="utf-8"
        )
        self.test_en.write_text(
            "### I. ERA ONE\n\n* **Sep. 2, 1945**: President Ho Chi Minh read Declaration of Independence.\n",
            encoding="utf-8"
        )

        timeline_image_manager.VI_FILE = self.test_vi
        timeline_image_manager.EN_FILE = self.test_en

        self.mgr = TimelineImageManager(root=None)

    def tearDown(self):
        timeline_image_manager.IMAGES_DIR = self.orig_images_dir
        timeline_image_manager.JSON_FILE = self.orig_json_file
        timeline_image_manager.VI_FILE = self.orig_vi_file
        timeline_image_manager.EN_FILE = self.orig_en_file
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_search_lines(self):
        results = self.mgr.search_lines("Tuyen ngon")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["line_num"], 3)
        self.assertIn("Bac Ho", results[0]["vi"])

    def test_add_and_remove_image_from_file(self):
        # Create a small test image
        img_path = self.test_dir / "test_sample.jpg"
        img = Image.new("RGB", (200, 200), color="blue")
        img.save(img_path, "JPEG")

        # Add image
        entry = self.mgr.add_image_from_file(3, img_path, source="Test Source TTXVN")
        self.assertTrue(entry["path"].endswith(".webp"))
        self.assertEqual(entry["source"], "Test Source TTXVN")

        # Verify in memory & json
        self.assertIn(3, self.mgr.images_per_line)
        self.assertEqual(len(self.mgr.images_per_line[3]), 1)
        self.assertTrue(timeline_image_manager.JSON_FILE.exists())

        # Verify status
        status = self.mgr.update_status()
        self.assertIn("Lines with images: 1", status)
        self.assertIn("Total images: 1", status)

        # Update source
        self.mgr.set_image_source(3, 0, "Updated Source")
        self.assertEqual(self.mgr.images_per_line[3][0]["source"], "Updated Source")

        # Remove image
        ok = self.mgr.remove_image(3, 0)
        self.assertTrue(ok)
        self.assertNotIn(3, self.mgr.images_per_line)

    def test_embed_markdown(self):
        img_path = self.test_dir / "test_embed.png"
        img = Image.new("RGB", (100, 100), color="red")
        img.save(img_path, "PNG")

        self.mgr.add_image_from_file(3, img_path, source="Vietnam News Agency")

        out_vi = self.test_dir / "out_vi.md"
        self.mgr.embed_markdown(self.test_vi, out_vi, is_vi=True)

        content = out_vi.read_text(encoding="utf-8")
        self.assertIn("![Image](images/", content)
        self.assertIn("*Nguồn: Vietnam News Agency*", content)

    def test_cli_commands(self):
        # 1. CLI search
        ret = cli_main(["search", "Tuyen"])
        self.assertEqual(ret, 0)

        # 2. CLI status
        ret = cli_main(["status"])
        self.assertEqual(ret, 0)

        # 3. CLI add via file
        img_path = self.test_dir / "test_cli.jpg"
        img = Image.new("RGB", (50, 50), color="green")
        img.save(img_path, "JPEG")

        ret = cli_main(["add", "--line", "3", "--file", str(img_path), "--source", "CLI Photo"])
        self.assertEqual(ret, 0)

        # 4. CLI list with has-images
        ret = cli_main(["list", "--has-images"])
        self.assertEqual(ret, 0)

        # 5. CLI source update
        ret = cli_main(["source", "--line", "3", "--index", "0", "--source", "Updated CLI Photo"])
        self.assertEqual(ret, 0)

        # 6. CLI embed
        out_vi = self.test_dir / "cli_out_vi.md"
        out_en = self.test_dir / "cli_out_en.md"
        ret = cli_main(["embed", "--vi-in", str(self.test_vi), "--vi-out", str(out_vi), "--en-in", str(self.test_en), "--en-out", str(out_en)])
        self.assertEqual(ret, 0)
        self.assertTrue(out_vi.exists())

        # 7. CLI remove
        ret = cli_main(["remove", "--line", "3", "--all"])
        self.assertEqual(ret, 0)

        # 8. CLI zip
        zip_out = self.test_dir / "test_images.zip"
        ret = cli_main(["zip", "--out", str(zip_out)])
        self.assertEqual(ret, 0)
        self.assertTrue(zip_out.exists())

        # 9. CLI sync-md
        ret = cli_main(["sync-md"])
        self.assertEqual(ret, 0)


if __name__ == "__main__":
    unittest.main()
