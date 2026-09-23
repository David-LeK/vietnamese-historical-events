#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import datetime
import difflib
import io
import json
import os
from pathlib import Path
import re
import shutil
import ssl
import subprocess
import sys
import urllib.request
import uuid

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, simpledialog
    HAS_TKINTER = True
except (ImportError, ModuleNotFoundError):
    HAS_TKINTER = False
    tk = None
    ttk = None
    filedialog = None
    messagebox = None
    simpledialog = None

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    from PIL import ImageTk, ImageGrab
    HAS_PIL_TK = True
except (ImportError, Exception):
    HAS_PIL_TK = False
    ImageTk = None
    ImageGrab = None

BASE_DIR = Path(__file__).parent.resolve()
IMAGES_DIR = BASE_DIR / "images"
VI_FILE = BASE_DIR / "timelines_vi.md"
EN_FILE = BASE_DIR / "timelines_en.md"
JSON_FILE = BASE_DIR / "timeline_images.json"

THUMB_SIZE = (160, 120)


class TimelineImageManager:
    def __init__(self, root=None):
        self.root = root

        self.vi_lines = []
        self.en_lines = []
        self.images_per_line = {}
        self.current_line_num = None
        self.thumb_refs = {}
        self.selected_remove_indices = set()
        self.source_vars = {}
        self.status_var = None

        if self.root is not None:
            if not HAS_TKINTER:
                raise RuntimeError("Tkinter is not installed on this system.")
            self.root.title("Timeline Image Manager")
            self.root.geometry("1300x750")
            self._setup_dark_theme()

        self.git_commit_id = self.get_git_commit_id()
        self.load_timelines()
        self.load_json_with_migration()

        if self.root is not None:
            self.setup_ui()
            self.refresh_line_list()
            self.update_status()

    def _setup_dark_theme(self):
        if self.root is None or not HAS_TKINTER:
            return
        self.root.configure(bg="#2b2b2b")
        style = ttk.Style()
        style.theme_use("clam")
        c = {
            "bg": "#2b2b2b",
            "fg": "#ffffff",
            "text_bg": "#1e1e1e",
            "text_fg": "#d4d4d4",
            "entry_bg": "#3c3c3c",
            "button_bg": "#3c3c3c",
            "select_bg": "#264f78",
            "scrollbar_bg": "#3c3c3c",
            "scrollbar_trough": "#2b2b2b",
        }
        style.configure("TFrame", background=c["bg"])
        style.configure("TLabel", background=c["bg"], foreground=c["fg"])
        style.configure("TButton", background=c["button_bg"], foreground=c["fg"], borderwidth=1, focusthickness=3, focuscolor="none")
        style.map("TButton", background=[("active", "#505050"), ("pressed", "#404040")])
        style.configure("TEntry", fieldbackground=c["entry_bg"], foreground=c["fg"], insertcolor=c["fg"], borderwidth=1)
        style.configure("TLabelFrame", background=c["bg"], foreground=c["fg"], bordercolor="#555555", lightcolor="#555555", darkcolor="#555555")
        style.configure("TLabelframe.Label", background=c["bg"], foreground=c["fg"])
        style.configure("TNotebook", background=c["bg"], tabmargins=[2, 2, 2, 0])
        style.configure("TNotebook.Tab", background=c["button_bg"], foreground=c["fg"], padding=[8, 2], borderwidth=1)
        style.map("TNotebook.Tab", background=[("selected", c["bg"])], expand=[("selected", [1, 1, 1, 0])])
        style.configure("TPanedwindow", background=c["bg"])
        style.configure("Vertical.TScrollbar", background=c["scrollbar_bg"], troughcolor=c["scrollbar_trough"], arrowcolor=c["fg"], bordercolor=c["scrollbar_trough"], lightcolor=c["scrollbar_trough"], darkcolor=c["scrollbar_trough"])
        style.configure("Horizontal.TScrollbar", background=c["scrollbar_bg"], troughcolor=c["scrollbar_trough"], arrowcolor=c["fg"], bordercolor=c["scrollbar_trough"], lightcolor=c["scrollbar_trough"], darkcolor=c["scrollbar_trough"])

    def _git_run(self, args):
        kwargs = {
            "capture_output": True,
            "text": True,
            "encoding": "utf-8",
            "errors": "replace",
            "cwd": BASE_DIR,
        }
        if hasattr(subprocess, "CREATE_NO_WINDOW"):
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        try:
            return subprocess.run(args, **kwargs)
        except Exception:
            return None

    def get_git_commit_id(self):
        r = self._git_run(["git", "rev-parse", "HEAD"])
        if r is not None and r.returncode == 0:
            return r.stdout.strip()
        return "unknown"

    def load_timelines(self):
        if VI_FILE.exists():
            with open(VI_FILE, "r", encoding="utf-8") as f:
                self.vi_lines = [line.rstrip("\n") for line in f.readlines()]
        else:
            self.vi_lines = []
        if EN_FILE.exists():
            with open(EN_FILE, "r", encoding="utf-8") as f:
                self.en_lines = [line.rstrip("\n") for line in f.readlines()]
        else:
            self.en_lines = []

    def build_composite(self, vi, en):
        n = max(len(vi), len(en))
        result = []
        for i in range(n):
            v = vi[i] if i < len(vi) else ""
            e = en[i] if i < len(en) else ""
            result.append(f"{v} \x00 {e}")
        return result

    def commit_exists(self, commit_id):
        r = self._git_run(["git", "cat-file", "-t", commit_id])
        return r is not None and r.returncode == 0 and r.stdout.strip() == "commit"

    def migrate_via_git(self, old_composite, new_composite, old_images, old_commit):
        r = self._git_run(
            ["git", "diff", old_commit, "--", "timelines_vi.md", "timelines_en.md"]
        )
        if r is None or r.returncode != 0:
            return None
        diff_text = r.stdout

        if not diff_text.strip():
            return {k: v for k, v in old_images.items() if k <= len(new_composite)}

        old_to_new = {}
        old_ln = 1
        new_ln = 1

        lines = diff_text.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("@@@"):
                i += 1
                continue
            if line.startswith("@@"):
                m = re.match(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", line)
                if m:
                    hunk_old = int(m.group(1))
                    hunk_new = int(m.group(3))
                    while old_ln < hunk_old and new_ln < hunk_new:
                        old_to_new[old_ln] = new_ln
                        old_ln += 1
                        new_ln += 1
                i += 1
                continue

            if line.startswith("---") or line.startswith("+++"):
                i += 1
                continue
            if line.startswith("diff --git"):
                i += 1
                continue
            if line.startswith("index "):
                i += 1
                continue

            if line.startswith("-") and not line.startswith("---"):
                if (i + 1 < len(lines) and lines[i + 1].startswith("+")
                        and not lines[i + 1].startswith("+++")):
                    old_to_new[old_ln] = new_ln
                    old_ln += 1
                    new_ln += 1
                    i += 2
                else:
                    old_ln += 1
                    i += 1
            elif line.startswith("+") and not line.startswith("+++"):
                new_ln += 1
                i += 1
            elif line.startswith(" ") and len(line) > 1:
                old_to_new[old_ln] = new_ln
                old_ln += 1
                new_ln += 1
                i += 1
            else:
                i += 1

        while old_ln <= len(old_composite) and new_ln <= len(new_composite):
            old_to_new[old_ln] = new_ln
            old_ln += 1
            new_ln += 1

        new_images = {}
        used_new = set()
        for old_ln in sorted(old_images.keys()):
            if old_ln in old_to_new:
                nln = old_to_new[old_ln]
                if nln not in used_new and 1 <= nln <= len(new_composite):
                    new_images[nln] = old_images[old_ln]
                    used_new.add(nln)

        return new_images

    def migrate_via_content(self, old_composite, new_composite, old_images):
        new_by_content = {}
        for i, c in enumerate(new_composite):
            new_by_content.setdefault(c, []).append(i + 1)

        new_images = {}
        used_new = set()
        unhandled = []

        for old_ln in sorted(old_images.keys()):
            if old_ln <= 0 or old_ln > len(old_composite):
                continue
            oc = old_composite[old_ln - 1]
            imgs = old_images[old_ln]
            nln = None

            if oc in new_by_content:
                cands = [ln for ln in new_by_content[oc] if ln not in used_new]
                if cands:
                    nln = cands[0]

            if nln is None:
                best_r, best_n = 0.0, None
                for cln in range(1, len(new_composite) + 1):
                    if cln in used_new:
                        continue
                    r = difflib.SequenceMatcher(None, oc, new_composite[cln - 1]).ratio()
                    if r > best_r:
                        best_r, best_n = r, cln
                if best_n is not None and best_r >= 0.6:
                    nln = best_n

            if nln is not None:
                new_images[nln] = imgs
                used_new.add(nln)
            else:
                unhandled.append((old_ln, oc, imgs))

        for old_ln, oc, imgs in unhandled:
            if old_ln <= len(new_composite) and old_ln not in used_new:
                nc = new_composite[old_ln - 1]
                sim = difflib.SequenceMatcher(None, oc, nc).ratio()
                if sim >= 0.5:
                    new_images[old_ln] = imgs
                    used_new.add(old_ln)

        return new_images

    def migrate_images(self, old_composite, new_composite, old_images, old_commit=""):
        if old_commit and self.commit_exists(old_commit):
            result = self.migrate_via_git(old_composite, new_composite, old_images, old_commit)
            if result is not None:
                return result
        return self.migrate_via_content(old_composite, new_composite, old_images)

    def has_uncommitted_changes(self):
        r = self._git_run(
            ["git", "diff", "HEAD", "--", "timelines_vi.md", "timelines_en.md"]
        )
        return r is not None and r.returncode == 0 and bool(r.stdout.strip())

    def load_json_with_migration(self):
        new_composite = self.build_composite(self.vi_lines, self.en_lines)
        if not JSON_FILE.exists():
            self.images_per_line = {}
            return
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, Exception):
            self.images_per_line = {}
            return

        old_composite = data.get("last_lines", [])
        old_images = data.get("images", {})
        old_images = {int(k): self._upgrade_image_entries(v) for k, v in old_images.items()}
        full_commit = data.get("git_commit_id", "")

        uncommitted = self.has_uncommitted_changes()

        if old_composite != new_composite and not uncommitted:
            self.images_per_line = self.migrate_images(old_composite, new_composite, old_images, full_commit)
            migrated_count = sum(len(v) for v in self.images_per_line.values())
            total_old = sum(len(v) for v in old_images.values())
            status = f"Migrated: {total_old} old images -> {migrated_count} new"
            if self.root is not None:
                self.root.after(100, lambda: self.show_info(f"Lines changed since last save.\n{status}"))
            else:
                self.show_info(f"Lines changed since last save: {status}")
            self.auto_save_json()
        else:
            self.images_per_line = old_images

        self.git_commit_id = full_commit or self.git_commit_id

    @staticmethod
    def _upgrade_image_entries(entries):
        result = []
        for e in entries:
            if isinstance(e, str):
                result.append({"path": e, "source": ""})
            elif isinstance(e, dict) and "path" in e:
                result.append({"path": e["path"], "source": e.get("source", "")})
            else:
                result.append({"path": str(e), "source": ""})
        return result

    def auto_save_json(self):
        self.save_json(silent=True)

    def get_relative_image_path(self, full_path):
        full_path = Path(full_path).resolve()
        try:
            return str(full_path.relative_to(BASE_DIR))
        except ValueError:
            try:
                return str(Path(IMAGES_DIR.name) / full_path.name)
            except Exception:
                return str(full_path.name)

    def save_json(self, silent=False):
        self.git_commit_id = self.get_git_commit_id()
        composite = self.build_composite(self.vi_lines, self.en_lines)
        serializable = {}
        for ln in sorted(self.images_per_line.keys()):
            items = []
            seen = set()
            for entry in self.images_per_line[ln]:
                p = self.get_relative_image_path(entry["path"] if isinstance(entry, dict) else entry)
                s = entry.get("source", "") if isinstance(entry, dict) else ""
                if p not in seen:
                    seen.add(p)
                    items.append({"path": p, "source": s})
            if items:
                serializable[str(ln)] = items

        data = {
            "git_commit_id": self.git_commit_id,
            "last_lines": composite,
            "images": serializable
        }
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.create_or_update_zip()
        if not silent:
            self.show_info("Saved timeline_images.json and updated images/images.zip")
        self.update_status()

    @staticmethod
    def create_or_update_zip(zip_path=None):
        import zipfile
        zip_path = Path(zip_path or (IMAGES_DIR / "images.zip"))
        zip_path.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        if IMAGES_DIR.exists():
            with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
                for f in sorted(os.listdir(IMAGES_DIR)):
                    if f.endswith(".webp"):
                        zf.write(IMAGES_DIR / f, arcname=f)
                        count += 1
        return zip_path, count

    def sync_from_markdown(self):
        """
        Parses timelines_vi.md and timelines_en.md directly to extract embedded images and sources,
        updating timeline_images.json and images.zip.
        """
        self.load_timelines()
        extracted = {}
        current_event_line = None
        event_regex = re.compile(r"^\*\s+\*\*(.*?)(?::\*\*|\*\*:\s*|\*\*\s*:?)")
        img_regex = re.compile(r"^!\[.*?\]\((.*?)\)")
        source_regex = re.compile(r"^\*(?:Nguồn|Source):\s*(.*?)\*?$")
        
        for idx, line in enumerate(self.vi_lines, start=1):
            stripped = line.strip()
            if event_regex.match(line) and not stripped.startswith("![") and not stripped.startswith("*Nguồn") and not stripped.startswith("*Source"):
                current_event_line = idx
            elif img_regex.match(stripped) and current_event_line:
                p = img_regex.match(stripped).group(1).lstrip("/")
                extracted.setdefault(current_event_line, []).append({"path": p, "source": ""})
            elif source_regex.match(stripped) and current_event_line:
                s = source_regex.match(stripped).group(1).rstrip("*").strip()
                if current_event_line in extracted and extracted[current_event_line]:
                    extracted[current_event_line][-1]["source"] = s
                    
        self.images_per_line = extracted
        self.save_json(silent=True)
        return len(extracted)

    def _normalized_image_name(self, ext):
        IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        now = datetime.datetime.now()
        base_name = now.strftime("event_%Y%m%d_%H%M%S")
        fname = base_name + ext
        dest = IMAGES_DIR / fname
        counter = 1
        while dest.exists():
            fname = f"{base_name}_{counter}{ext}"
            dest = IMAGES_DIR / fname
            counter += 1
        return dest

    def process_image(self, img):
        """
        Resizes PIL image to maximum 1200px width (LANCZOS) and saves as WebP quality 80.
        Returns the destination Path in IMAGES_DIR.
        """
        if not HAS_PIL:
            raise RuntimeError("PIL/Pillow is required for processing images.")
        dest = self._normalized_image_name(".webp")
        img_w, img_h = img.size
        if img_w > 1200:
            ratio = 1200.0 / img_w
            resample_filter = getattr(Image, "Resampling", Image).LANCZOS
            img = img.resize((1200, int(img_h * ratio)), resample_filter)

        if img.mode in ("RGBA", "P"):
            img.save(str(dest), "WEBP", quality=80)
        else:
            img.convert("RGB").save(str(dest), "WEBP", quality=80)
        return dest

    def add_image_from_pil(self, line_num, img, source=""):
        dest = self.process_image(img)
        rel_path = self.get_relative_image_path(dest)
        if line_num not in self.images_per_line:
            self.images_per_line[line_num] = []

        for e in self.images_per_line[line_num]:
            curr_path = e["path"] if isinstance(e, dict) else e
            if curr_path == rel_path:
                return e

        entry = {"path": rel_path, "source": source.strip()}
        self.images_per_line[line_num].append(entry)
        self.save_json(silent=True)
        return entry

    def add_image_from_file(self, line_num, file_path, source=""):
        src = Path(file_path)
        if not src.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        if not HAS_PIL:
            raise RuntimeError("PIL/Pillow is required for adding images.")
        with Image.open(src) as img:
            return self.add_image_from_pil(line_num, img, source=source)

    def add_image_from_url(self, line_num, url, source=""):
        if not HAS_PIL:
            raise RuntimeError("PIL/Pillow is required for processing images.")
        headers = {
            "User-Agent": "VietnameseHistoricalEventsManager/1.0 (https://github.com/David-LeK/vietnamese-historical-events; admin@history.vn)",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        }
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            data = resp.read()

        with Image.open(io.BytesIO(data)) as img:
            final_source = source.strip() if source.strip() else url
            return self.add_image_from_pil(line_num, img, source=final_source)

    def remove_image(self, line_num, index=None):
        if line_num not in self.images_per_line:
            return False
        if index is None:
            del self.images_per_line[line_num]
        else:
            if 0 <= index < len(self.images_per_line[line_num]):
                self.images_per_line[line_num].pop(index)
                if not self.images_per_line[line_num]:
                    del self.images_per_line[line_num]
            else:
                return False
        self.save_json(silent=True)
        return True

    def set_image_source(self, line_num, index, source):
        if line_num not in self.images_per_line:
            return False
        images = self.images_per_line[line_num]
        if 0 <= index < len(images):
            entry = images[index]
            if isinstance(entry, str):
                entry = {"path": entry, "source": ""}
                images[index] = entry
            entry["source"] = source.strip()
            self.save_json(silent=True)
            return True
        return False

    def get_line_info(self, line_num):
        if line_num <= 0:
            return None
        max_lines = max(len(self.vi_lines), len(self.en_lines))
        if line_num > max_lines:
            return None
        vi = self.vi_lines[line_num - 1] if line_num <= len(self.vi_lines) else ""
        en = self.en_lines[line_num - 1] if line_num <= len(self.en_lines) else ""
        return {
            "line_num": line_num,
            "vi": vi,
            "en": en,
            "images": self.images_per_line.get(line_num, [])
        }

    def search_lines(self, query):
        query_lower = query.lower()
        max_lines = max(len(self.vi_lines), len(self.en_lines))
        matches = []
        for i in range(max_lines):
            vi = self.vi_lines[i] if i < len(self.vi_lines) else ""
            en = self.en_lines[i] if i < len(self.en_lines) else ""
            if query_lower in vi.lower() or query_lower in en.lower():
                matches.append({
                    "line_num": i + 1,
                    "vi": vi,
                    "en": en,
                    "images": self.images_per_line.get(i + 1, [])
                })
        return matches

    def embed_markdown(self, in_file=None, out_file=None, is_vi=True, use_leading_slash=False):
        in_path = Path(in_file or (VI_FILE if is_vi else EN_FILE))
        out_path = Path(out_file or in_path)

        with open(in_path, "r", encoding="utf-8") as f:
            raw_lines = f.readlines()

        # Clean existing image/source lines from input to prevent duplicates
        clean_lines = []
        img_or_source = re.compile(r"^(?:!\[.*?\]\(.*?\)|(?:\*Nguồn:|\*Source:))", re.IGNORECASE)
        skip_empty_after_img = False
        for line in raw_lines:
            stripped = line.strip()
            if img_or_source.match(stripped):
                skip_empty_after_img = True
                continue
            if stripped == "" and skip_empty_after_img:
                continue
            skip_empty_after_img = False
            clean_lines.append(line.rstrip("\n"))

        result = []
        for lineno, line in enumerate(clean_lines, start=1):
            result.append(line)
            if lineno in self.images_per_line:
                for entry in self.images_per_line[lineno]:
                    img_path = entry["path"] if isinstance(entry, dict) else entry
                    source = entry.get("source", "") if isinstance(entry, dict) else ""
                    norm_path = img_path.replace("\\", "/")
                    if use_leading_slash and not norm_path.startswith("/"):
                        img_link = "/" + norm_path
                    else:
                        img_link = norm_path
                    alt_label = "Hình ảnh tư liệu" if is_vi else "Historical Image"
                    result.append("")
                    result.append(f"![{alt_label}]({img_link})")
                    if source:
                        result.append("")
                        result.append(f"*Nguồn: {source}*" if is_vi else f"*Source: {source}*")
                    result.append("")

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(result) + "\n")
        self.create_or_update_zip()
        return out_path

    # ==========================
    # GUI IMPLEMENTATION
    # ==========================

    def setup_ui(self):
        if self.root is None or not HAS_TKINTER:
            return
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        left_frame = ttk.Frame(main_paned)
        right_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)
        main_paned.add(right_frame, weight=2)

        top_bar = ttk.Frame(self.root)
        top_bar.pack(fill=tk.X, padx=5, pady=(5, 0))
        self.status_var = tk.StringVar()
        status_label = ttk.Label(top_bar, textvariable=self.status_var, font=("Segoe UI", 9))
        status_label.pack(side=tk.LEFT)
        save_btn = ttk.Button(top_bar, text="Save", command=lambda: self.save_json(silent=False))
        save_btn.pack(side=tk.RIGHT, padx=2)

        # Left: line list
        list_frame = ttk.LabelFrame(left_frame, text="Timeline Entries", padding=3)
        list_frame.pack(fill=tk.BOTH, expand=True)

        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill=tk.X, pady=(0, 3))
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *a: self.refresh_line_list())
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(3, 0))

        list_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.line_listbox = tk.Listbox(
            list_frame, yscrollcommand=list_scroll.set,
            font=("Segoe UI", 10), selectmode=tk.SINGLE,
            borderwidth=1, relief=tk.SOLID,
            bg="#1e1e1e", fg="#d4d4d4",
            selectbackground="#264f78", selectforeground="#ffffff",
            highlightbackground="#3c3c3c"
        )
        list_scroll.config(command=self.line_listbox.yview)
        list_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.line_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.line_listbox.bind("<<ListboxSelect>>", self.on_line_select)

        # Right: detail
        detail_frame = ttk.LabelFrame(right_frame, text="Line Detail", padding=5)
        detail_frame.pack(fill=tk.BOTH, expand=True)

        self.detail_notebook = ttk.Notebook(detail_frame)
        self.detail_notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        # VI tab
        vi_frame = ttk.Frame(self.detail_notebook)
        self.detail_notebook.add(vi_frame, text="VI")
        vi_scroll = ttk.Scrollbar(vi_frame, orient=tk.VERTICAL)
        self.vi_text = tk.Text(
            vi_frame, wrap=tk.WORD, font=("Segoe UI", 10),
            yscrollcommand=vi_scroll.set, borderwidth=1, relief=tk.SOLID,
            bg="#1e1e1e", fg="#d4d4d4", insertbackground="#d4d4d4",
            selectbackground="#264f78", selectforeground="#ffffff",
            highlightbackground="#3c3c3c"
        )
        vi_scroll.config(command=self.vi_text.yview)
        vi_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.vi_text.pack(fill=tk.BOTH, expand=True)

        # EN tab
        en_frame = ttk.Frame(self.detail_notebook)
        self.detail_notebook.add(en_frame, text="EN")
        en_scroll = ttk.Scrollbar(en_frame, orient=tk.VERTICAL)
        self.en_text = tk.Text(
            en_frame, wrap=tk.WORD, font=("Segoe UI", 10),
            yscrollcommand=en_scroll.set, borderwidth=1, relief=tk.SOLID,
            bg="#1e1e1e", fg="#d4d4d4", insertbackground="#d4d4d4",
            selectbackground="#264f78", selectforeground="#ffffff",
            highlightbackground="#3c3c3c"
        )
        en_scroll.config(command=self.en_text.yview)
        en_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.en_text.pack(fill=tk.BOTH, expand=True)

        # Image area
        img_area_frame = ttk.LabelFrame(detail_frame, text="Attached Images", padding=5)
        img_area_frame.pack(fill=tk.BOTH, pady=(0, 5))

        img_btn_frame = ttk.Frame(img_area_frame)
        img_btn_frame.pack(fill=tk.X)
        add_img_btn = ttk.Button(img_btn_frame, text="Add Image(s)", command=self.add_images)
        add_img_btn.pack(side=tk.LEFT, padx=(0, 3))
        self.remove_btn = ttk.Button(
            img_btn_frame, text="Remove Selected",
            command=self.remove_selected_images, state=tk.DISABLED
        )
        self.remove_btn.pack(side=tk.LEFT)
        self.remove_all_btn = ttk.Button(
            img_btn_frame, text="Remove All",
            command=self.remove_all_images, state=tk.DISABLED
        )
        self.remove_all_btn.pack(side=tk.LEFT, padx=(3, 0))

        self.img_count_var = tk.StringVar()
        img_count_label = ttk.Label(img_btn_frame, textvariable=self.img_count_var)
        img_count_label.pack(side=tk.RIGHT)

        canvas_frame = ttk.Frame(img_area_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        self.img_canvas = tk.Canvas(canvas_frame, borderwidth=1, relief=tk.SOLID, bg="#2b2b2b", highlightbackground="#3c3c3c")
        img_h_scroll = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.img_canvas.xview)
        img_v_scroll = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.img_canvas.yview)
        self.img_canvas.configure(
            xscrollcommand=img_h_scroll.set,
            yscrollcommand=img_v_scroll.set
        )
        self.img_inner = ttk.Frame(self.img_canvas)
        self.img_inner.bind("<Configure>", lambda e: self.img_canvas.configure(scrollregion=self.img_canvas.bbox("all")))
        self.img_canvas_window = self.img_canvas.create_window((0, 0), window=self.img_inner, anchor="nw")
        self.img_canvas.bind("<Configure>", self._on_canvas_configure)

        img_h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        img_v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.img_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.root.bind("<Control-v>", self.paste_image_from_clipboard)
        self.root.bind("<Control-V>", self.paste_image_from_clipboard)

        paste_hint = ttk.Label(
            img_area_frame,
            text="Tip: Copy an image from your browser, then Ctrl+V here to paste it.",
            font=("Segoe UI", 8), foreground="#888888"
        )
        paste_hint.pack(anchor=tk.W)

        legend_label = ttk.Label(
            img_area_frame,
            text="Click 'Select' on an image to mark it for removal. Selected images have a red border.",
            font=("Segoe UI", 8), foreground="#888888"
        )
        legend_label.pack(anchor=tk.W)

    def _on_canvas_configure(self, event):
        self.img_canvas.itemconfig(self.img_canvas_window, width=event.width)

    def refresh_line_list(self):
        if not hasattr(self, "line_listbox") or self.line_listbox is None:
            return
        self.line_listbox.delete(0, tk.END)
        query = self.search_var.get().lower() if hasattr(self, "search_var") else ""
        max_lines = max(len(self.vi_lines), len(self.en_lines))
        self._line_map = []
        for i in range(max_lines):
            vi = self.vi_lines[i] if i < len(self.vi_lines) else ""
            en = self.en_lines[i] if i < len(self.en_lines) else ""
            display = f"{i+1:4d} | {vi[:80]}"
            match = True
            if query:
                match = query in vi.lower() or query in en.lower()
            if match:
                self._line_map.append(i + 1)
                has_images = "*" if (i + 1) in self.images_per_line and self.images_per_line[i + 1] else " "
                self.line_listbox.insert(tk.END, f"{has_images} {display}")

    def on_line_select(self, event):
        sel = self.line_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        if idx < 0 or idx >= len(self._line_map):
            return
        self.deselect_all_image_thumbs()
        self.current_line_num = self._line_map[idx]
        self.show_line_detail(self.current_line_num)

    def show_line_detail(self, line_num):
        self.vi_text.config(state=tk.NORMAL)
        self.en_text.config(state=tk.NORMAL)
        self.vi_text.delete("1.0", tk.END)
        self.en_text.delete("1.0", tk.END)

        if line_num <= len(self.vi_lines):
            self.vi_text.insert("1.0", self.vi_lines[line_num - 1])
        if line_num <= len(self.en_lines):
            self.en_text.insert("1.0", self.en_lines[line_num - 1])

        self.vi_text.config(state=tk.DISABLED)
        self.en_text.config(state=tk.DISABLED)

        self.display_images(line_num)

    def display_images(self, line_num):
        for w in self.img_inner.winfo_children():
            w.destroy()
        self.thumb_refs.clear()
        self.source_vars.clear()
        self.selected_remove_indices.clear()
        self.remove_btn.config(state=tk.DISABLED)
        self.remove_all_btn.config(state=tk.DISABLED)

        images = self.images_per_line.get(line_num, [])
        if not images:
            self.img_count_var.set("No images")
            return

        self.remove_all_btn.config(state=tk.NORMAL)
        self.img_count_var.set(f"{len(images)} image(s)")

        cols = max(1, (self.img_canvas.winfo_width() or 600) // (THUMB_SIZE[0] + 15))
        row_frame = None

        for i, entry in enumerate(images):
            if isinstance(entry, str):
                entry = {"path": entry, "source": ""}
            img_path = entry["path"]
            source_text = entry.get("source", "")

            if i % cols == 0:
                row_frame = ttk.Frame(self.img_inner)
                row_frame.pack(fill=tk.X, pady=2)

            thumb_frame = ttk.Frame(row_frame, borderwidth=2, relief=tk.RAISED)
            thumb_frame.pack(side=tk.LEFT, padx=3)

            img_full = Path(img_path)
            if not img_full.is_absolute():
                img_full = BASE_DIR / img_path

            thumb = self.load_thumbnail(img_full)
            if thumb is None:
                lbl = ttk.Label(thumb_frame, text=f"[No preview]\n{Path(img_path).name}", foreground="red")
                lbl.pack()
            else:
                lbl = ttk.Label(thumb_frame, image=thumb, cursor="hand2")
                lbl.image = thumb
                lbl.pack()
                self.thumb_refs[id(lbl)] = thumb

            name_label = ttk.Label(thumb_frame, text=Path(img_path).name, font=("Segoe UI", 7), wraplength=THUMB_SIZE[0])
            name_label.pack()

            src_var = tk.StringVar(value=source_text)
            self.source_vars[i] = src_var
            src_entry = ttk.Entry(
                thumb_frame, textvariable=src_var,
                font=("Segoe UI", 7), width=20
            )
            src_entry.pack(fill=tk.X, padx=2, pady=1)
            src_entry.bind("<FocusOut>", lambda e, idx=i: self.save_source(idx))
            src_entry.bind("<Return>", lambda e, idx=i: self.save_source(idx))

            select_btn = ttk.Button(
                thumb_frame, text="Select",
                command=lambda idx=i: self.toggle_image_selection(idx)
            )
            select_btn.pack(pady=1)

    def toggle_image_selection(self, idx):
        if idx in self.selected_remove_indices:
            self.selected_remove_indices.remove(idx)
        else:
            self.selected_remove_indices.add(idx)
        self.remove_btn.config(
            state=tk.NORMAL if self.selected_remove_indices else tk.DISABLED
        )

        children = self.img_inner.winfo_children()
        flat = []
        for rf in children:
            for child in rf.winfo_children():
                flat.append(child)

        for i, frame in enumerate(flat):
            if i == idx:
                if i in self.selected_remove_indices:
                    frame.config(borderwidth=3, relief=tk.SOLID)
                else:
                    frame.config(borderwidth=2, relief=tk.RAISED)

    def deselect_all_image_thumbs(self):
        self.selected_remove_indices.clear()
        if hasattr(self, "remove_btn") and self.remove_btn is not None:
            self.remove_btn.config(state=tk.DISABLED)

    def load_thumbnail(self, path):
        if not path.exists():
            return None
        if not HAS_PIL or not HAS_PIL_TK or ImageTk is None:
            return None
        try:
            img = Image.open(path)
            img.thumbnail(THUMB_SIZE, getattr(Image, "Resampling", Image).LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception:
            return None

    def save_source(self, idx):
        if self.current_line_num is None:
            return
        images = self.images_per_line.get(self.current_line_num, [])
        if 0 <= idx < len(images):
            entry = images[idx]
            if isinstance(entry, str):
                entry = {"path": entry, "source": ""}
                images[idx] = entry
            new_text = self.source_vars.get(idx, tk.StringVar()).get()
            entry["source"] = new_text
            self.save_json(silent=True)

    def add_images(self):
        if self.current_line_num is None:
            self.show_info("Please select a line first.")
            return
        if not HAS_TKINTER:
            return
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.webp *.avif"), ("All files", "*.*")]
        )
        if not files:
            return

        added = 0
        for fpath in files:
            try:
                entry = self.add_image_from_file(self.current_line_num, fpath)
                if entry:
                    added += 1
            except Exception as e:
                print(f"Error adding file {fpath}: {e}")

        if added > 0:
            self.display_images(self.current_line_num)
            self.refresh_line_list()
            self.show_info(f"Added {added} image(s)")
        else:
            self.show_info("No new images were added (duplicates or unsupported formats)")

    def paste_image_from_clipboard(self, event=None):
        if self.current_line_num is None:
            self.show_info("Please select a line first, then paste.")
            return
        if not HAS_PIL or not HAS_PIL_TK or ImageGrab is None:
            self.show_info("Pillow ImageTk/ImageGrab is required for clipboard paste.")
            return
        try:
            img = ImageGrab.grabclipboard()
        except Exception:
            self.show_info("Could not access clipboard.")
            return
        if img is None:
            self.show_info("No image found in clipboard.")
            return

        self.show_paste_dialog(img)

    def show_paste_dialog(self, img):
        if not HAS_TKINTER:
            return
        IMAGES_DIR.mkdir(parents=True, exist_ok=True)

        dialog = tk.Toplevel(self.root)
        dialog.title("Paste Image")
        dialog.geometry("500x580")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg="#2b2b2b")

        preview_size = (460, 360)
        preview = img.copy()
        preview.thumbnail(preview_size, getattr(Image, "Resampling", Image).LANCZOS)
        photo = ImageTk.PhotoImage(preview)

        preview_label = ttk.Label(dialog, image=photo)
        preview_label.image = photo
        preview_label.pack(pady=10)

        info_frame = ttk.Frame(dialog)
        info_frame.pack(fill=tk.X, padx=20)

        ttk.Label(info_frame, text="Source / Credit:").pack(anchor=tk.W)
        source_text_var = tk.StringVar()
        source_entry = ttk.Entry(info_frame, textvariable=source_text_var, font=("Segoe UI", 10))
        source_entry.pack(fill=tk.X, pady=5)
        source_entry.focus_set()

        original_w, original_h = img.size
        ttk.Label(info_frame, text=f"Size: {original_w} x {original_h} px", foreground="#888888").pack(anchor=tk.W)

        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=15)

        def do_ok():
            try:
                line = self.current_line_num
                if line is None:
                    messagebox.showerror("Error", "No line selected.", parent=dialog)
                    return

                src_text = source_text_var.get().strip()
                entry = self.add_image_from_pil(line, img, source=src_text)

                self.display_images(line)
                self.refresh_line_list()
                self.show_info(f"Pasted {Path(entry['path']).name}")
                dialog.destroy()
            except Exception as e:
                import traceback
                traceback.print_exc()
                messagebox.showerror("Error", f"Failed to paste image:\n{e}", parent=dialog)

        ok_btn = ttk.Button(btn_frame, text="OK", command=do_ok, width=12)
        ok_btn.pack(side=tk.LEFT, padx=5)
        cancel_btn = ttk.Button(btn_frame, text="Cancel", command=dialog.destroy, width=12)
        cancel_btn.pack(side=tk.LEFT, padx=5)

        dialog.bind("<Return>", lambda e: do_ok())
        dialog.bind("<Escape>", lambda e: dialog.destroy())

    def remove_selected_images(self):
        if self.current_line_num is None or not self.selected_remove_indices:
            return
        images = self.images_per_line.get(self.current_line_num, [])
        to_remove = sorted(self.selected_remove_indices, reverse=True)
        for idx in to_remove:
            if 0 <= idx < len(images):
                images.pop(idx)
        if not images:
            if self.current_line_num in self.images_per_line:
                del self.images_per_line[self.current_line_num]
        else:
            self.images_per_line[self.current_line_num] = images
        self.display_images(self.current_line_num)
        self.refresh_line_list()
        self.save_json(silent=True)
        self.show_info("Removed selected images")

    def remove_all_images(self):
        if self.current_line_num is None:
            return
        if self.current_line_num in self.images_per_line:
            del self.images_per_line[self.current_line_num]
        self.display_images(self.current_line_num)
        self.refresh_line_list()
        self.save_json(silent=True)

    def update_status(self):
        max_lines = max(len(self.vi_lines), len(self.en_lines))
        total_images = sum(len(v) for v in self.images_per_line.values())
        msg = (
            f"Git: {self.git_commit_id[:12]}  |  "
            f"Lines: {max_lines}  |  "
            f"Lines with images: {len(self.images_per_line)}  |  "
            f"Total images: {total_images}"
        )
        if hasattr(self, "status_var") and self.status_var is not None:
            self.status_var.set(msg)
        return msg

    def show_info(self, msg):
        if hasattr(self, "status_var") and self.status_var is not None:
            self.status_var.set(msg)
        else:
            print(f"[INFO] {msg}")


def cli_main(argv=None):
    parser = argparse.ArgumentParser(
        description="Timeline Image Manager CLI - Manage & embed images for Vietnamese Historical Events timelines."
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # search
    search_p = subparsers.add_parser("search", help="Search timeline events by text")
    search_p.add_argument("query", help="Keyword or phrase to search in VI or EN")
    search_p.add_argument("--limit", type=int, default=20, help="Max results to display (default: 20)")

    # list
    list_p = subparsers.add_parser("list", help="List timeline entries")
    list_p.add_argument("--has-images", action="store_true", help="Only list entries that currently have images")
    list_p.add_argument("--line", type=int, help="Specific line number to view")
    list_p.add_argument("--limit", type=int, default=50, help="Limit number of lines shown (default: 50)")

    # add
    add_p = subparsers.add_parser("add", help="Add an image to a timeline entry")
    add_p.add_argument("--line", type=int, required=True, help="1-based line number in timelines_vi.md/timelines_en.md")
    group = add_p.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="Image URL from the internet")
    group.add_argument("--file", help="Path to local image file")
    add_p.add_argument("--source", default="", help="Source credit or citation for the image")

    # remove
    rem_p = subparsers.add_parser("remove", help="Remove image(s) from a timeline entry")
    rem_p.add_argument("--line", type=int, required=True, help="Line number")
    rem_group = rem_p.add_mutually_exclusive_group(required=True)
    rem_group.add_argument("--index", type=int, help="0-based index of image to remove")
    rem_group.add_argument("--all", action="store_true", help="Remove all images for this line")

    # source
    src_p = subparsers.add_parser("source", help="Update source citation for an image")
    src_p.add_argument("--line", type=int, required=True, help="Line number")
    src_p.add_argument("--index", type=int, default=0, help="0-based index of image (default: 0)")
    src_p.add_argument("--source", required=True, help="New source citation text")

    # status
    subparsers.add_parser("status", help="Show summary status of images and commit info")

    # zip
    zip_p = subparsers.add_parser("zip", help="Compress all WebP images in images/ to images/images.zip")
    zip_p.add_argument("--out", default=None, help="Output zip file path (default: images/images.zip)")

    # sync-md
    subparsers.add_parser("sync-md", help="Extract embedded images and sources from timelines_vi.md into timeline_images.json and update images.zip")

    # embed
    embed_p = subparsers.add_parser("embed", help="Embed images directly into markdown timeline files")
    embed_p.add_argument("--vi-in", default=str(VI_FILE), help="Input VI markdown file (default: timelines_vi.md)")
    embed_p.add_argument("--vi-out", default=str(VI_FILE), help="Output VI markdown file (default: timelines_vi.md)")
    embed_p.add_argument("--en-in", default=str(EN_FILE), help="Input EN markdown file (default: timelines_en.md)")
    embed_p.add_argument("--en-out", default=str(EN_FILE), help="Output EN markdown file (default: timelines_en.md)")
    embed_p.add_argument("--use-leading-slash", action="store_true", help="Prepend leading slash to image path (/images/...)")

    # gui
    subparsers.add_parser("gui", help="Launch Tkinter GUI")

    args = parser.parse_args(argv)

    if not args.command or args.command == "gui":
        if not HAS_TKINTER:
            print("[ERROR] Tkinter is not installed on this system.")
            print("To use the Graphical User Interface, install python3-tk (e.g., 'sudo zypper install python313-tk' or 'sudo apt install python3-tk').")
            print("Use 'python timeline_image_manager.py --help' to see all available CLI commands.")
            return 1
        root = tk.Tk()
        app = TimelineImageManager(root)
        root.mainloop()
        return 0

    mgr = TimelineImageManager(root=None)

    if args.command == "search":
        matches = mgr.search_lines(args.query)
        print(f"Found {len(matches)} match(es) for '{args.query}':\n")
        for m in matches[:args.limit]:
            ln = m["line_num"]
            vi = m["vi"]
            en = m["en"]
            imgs = m["images"]
            img_tag = f" [{len(imgs)} image(s)]" if imgs else ""
            print(f"Line {ln:4d}:{img_tag}")
            print(f"  VI: {vi}")
            print(f"  EN: {en}")
            if imgs:
                for idx, entry in enumerate(imgs):
                    p = entry.get("path", "") if isinstance(entry, dict) else entry
                    s = entry.get("source", "") if isinstance(entry, dict) else ""
                    print(f"    [{idx}] {p}  |  Source: {s}")
            print("-" * 60)
        if len(matches) > args.limit:
            print(f"... and {len(matches) - args.limit} more matches (use --limit to show more).")

    elif args.command == "list":
        if args.line:
            info = mgr.get_line_info(args.line)
            if not info:
                print(f"[ERROR] Line {args.line} is out of range.")
                return 1
            print(f"Line {args.line}:")
            print(f"  VI: {info['vi']}")
            print(f"  EN: {info['en']}")
            imgs = info["images"]
            print(f"  Images ({len(imgs)}):")
            for idx, entry in enumerate(imgs):
                p = entry.get("path", "") if isinstance(entry, dict) else entry
                s = entry.get("source", "") if isinstance(entry, dict) else ""
                print(f"    [{idx}] {p}  |  Source: {s}")
        elif args.has_images:
            lines_with_imgs = sorted(mgr.images_per_line.keys())
            print(f"Total lines with images: {len(lines_with_imgs)}\n")
            for ln in lines_with_imgs[:args.limit]:
                info = mgr.get_line_info(ln)
                imgs = info["images"] if info else []
                vi = info["vi"] if info else ""
                print(f"Line {ln:4d} ({len(imgs)} image(s)): {vi[:80]}")
                for idx, entry in enumerate(imgs):
                    p = entry.get("path", "") if isinstance(entry, dict) else entry
                    s = entry.get("source", "") if isinstance(entry, dict) else ""
                    print(f"    [{idx}] {p}  |  Source: {s}")
            if len(lines_with_imgs) > args.limit:
                print(f"... and {len(lines_with_imgs) - args.limit} more lines (use --limit to show more).")
        else:
            max_lines = max(len(mgr.vi_lines), len(mgr.en_lines))
            for ln in range(1, min(max_lines + 1, args.limit + 1)):
                info = mgr.get_line_info(ln)
                imgs = info["images"] if info else []
                vi = info["vi"] if info else ""
                has_star = "*" if imgs else " "
                print(f"{has_star} Line {ln:4d}: {vi[:80]}")

    elif args.command == "add":
        if args.url:
            print(f"Downloading image from URL: {args.url} ...")
            try:
                entry = mgr.add_image_from_url(args.line, args.url, source=args.source)
                print(f"[SUCCESS] Added image to Line {args.line}:")
                print(f"  Path:   {entry['path']}")
                print(f"  Source: {entry['source']}")
            except Exception as e:
                print(f"[ERROR] Failed to add image from URL: {e}")
                return 1
        elif args.file:
            print(f"Processing local image: {args.file} ...")
            try:
                entry = mgr.add_image_from_file(args.line, args.file, source=args.source)
                print(f"[SUCCESS] Added image to Line {args.line}:")
                print(f"  Path:   {entry['path']}")
                print(f"  Source: {entry['source']}")
            except Exception as e:
                print(f"[ERROR] Failed to add image from file: {e}")
                return 1

    elif args.command == "remove":
        idx = None if args.all else args.index
        ok = mgr.remove_image(args.line, index=idx)
        if ok:
            if args.all:
                print(f"[SUCCESS] Removed all images from Line {args.line}.")
            else:
                print(f"[SUCCESS] Removed image [{args.index}] from Line {args.line}.")
        else:
            print(f"[ERROR] Failed to remove image: line or index not found.")
            return 1

    elif args.command == "source":
        ok = mgr.set_image_source(args.line, args.index, args.source)
        if ok:
            print(f"[SUCCESS] Updated source for Line {args.line} [index {args.index}]: {args.source}")
        else:
            print(f"[ERROR] Failed to update source: line or index not found.")
            return 1

    elif args.command == "status":
        msg = mgr.update_status()
        print("=== Timeline Image Manager Status ===")
        print(f"{msg}")
        print(f"Base Directory: {BASE_DIR}")
        print(f"Images Directory: {IMAGES_DIR}")
        print(f"JSON Metadata File: {JSON_FILE}")

    elif args.command == "zip":
        out_path = Path(args.out) if args.out else None
        p, count = mgr.create_or_update_zip(out_path)
        size_kb = os.path.getsize(p) / 1024
        print(f"[SUCCESS] Compressed {count} images into {p} ({size_kb:.1f} KB)")

    elif args.command == "sync-md":
        count = mgr.sync_from_markdown()
        print(f"[SUCCESS] Synced {count} events with images from markdown into {JSON_FILE} and refreshed images/images.zip")

    elif args.command == "embed":
        vi_in = args.vi_in or str(VI_FILE)
        en_in = args.en_in or str(EN_FILE)
        vi_out = args.vi_out or str(VI_FILE)
        en_out = args.en_out or str(EN_FILE)
        print(f"Embedding images into {vi_out} and {en_out}...")
        mgr.embed_markdown(vi_in, vi_out, is_vi=True, use_leading_slash=args.use_leading_slash)
        mgr.embed_markdown(en_in, en_out, is_vi=False, use_leading_slash=args.use_leading_slash)
        print(f"[SUCCESS] Embedded VI -> {vi_out}")
        print(f"[SUCCESS] Embedded EN -> {en_out}")

    return 0


def main():
    if len(sys.argv) > 1 and sys.argv[1] != "gui":
        sys.exit(cli_main())
    elif len(sys.argv) > 1 and sys.argv[1] == "gui":
        sys.exit(cli_main(["gui"]))
    else:
        if HAS_TKINTER:
            root = tk.Tk()
            app = TimelineImageManager(root)
            root.mainloop()
        else:
            sys.exit(cli_main(["--help"]))


if __name__ == "__main__":
    main()
