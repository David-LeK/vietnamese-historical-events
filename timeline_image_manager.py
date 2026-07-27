#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import json
import os
import subprocess
import shutil
import difflib
import re
import uuid
import io
import datetime
from pathlib import Path

try:
    from PIL import Image, ImageTk, ImageGrab
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

BASE_DIR = Path(__file__).parent.resolve()
IMAGES_DIR = BASE_DIR / "images"
VI_FILE = BASE_DIR / "timelines_vi.md"
EN_FILE = BASE_DIR / "timelines_en.md"
JSON_FILE = BASE_DIR / "timeline_images.json"

THUMB_SIZE = (160, 120)


class TimelineImageManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Timeline Image Manager")
        self.root.geometry("1300x750")

        self.vi_lines = []
        self.en_lines = []
        self.images_per_line = {}
        self.current_line_num = None
        self.thumb_refs = {}
        self.selected_remove_indices = set()
        self.source_vars = {}

        self.git_commit_id = self.get_git_commit_id()
        self.load_timelines()
        self.load_json_with_migration()
        self.setup_ui()
        self.refresh_line_list()
        self.update_status()

    def _git_run(self, args):
        try:
            return subprocess.run(
                args, capture_output=True, text=True, encoding="utf-8", errors="replace",
                cwd=BASE_DIR, creationflags=subprocess.CREATE_NO_WINDOW
            )
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
            self.root.after(100, lambda: self.show_info(f"Lines changed since last save.\n{status}"))
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
            serializable[str(ln)] = items

        data = {
            "git_commit_id": self.git_commit_id,
            "last_lines": composite,
            "images": serializable
        }
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        if not silent:
            self.show_info("Saved timeline_images.json")
        self.update_status()

    def setup_ui(self):
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
            borderwidth=1, relief=tk.SOLID
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
            yscrollcommand=vi_scroll.set, borderwidth=1, relief=tk.SOLID
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
            yscrollcommand=en_scroll.set, borderwidth=1, relief=tk.SOLID
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
        self.img_canvas = tk.Canvas(canvas_frame, borderwidth=1, relief=tk.SOLID)
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
            font=("Segoe UI", 8), foreground="gray"
        )
        paste_hint.pack(anchor=tk.W)

        legend_label = ttk.Label(
            img_area_frame,
            text="Click 'Select' on an image to mark it for removal. Selected images have a red border.",
            font=("Segoe UI", 8), foreground="gray"
        )
        legend_label.pack(anchor=tk.W)

    def _on_canvas_configure(self, event):
        self.img_canvas.itemconfig(self.img_canvas_window, width=event.width)

    def refresh_line_list(self):
        self.line_listbox.delete(0, tk.END)
        query = self.search_var.get().lower()
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
        self.remove_btn.config(state=tk.DISABLED)

    def load_thumbnail(self, path):
        if not path.exists():
            return None
        if not HAS_PIL:
            return None
        try:
            img = Image.open(path)
            img.thumbnail(THUMB_SIZE, Image.LANCZOS)
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
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.webp"), ("All files", "*.*")]
        )
        if not files:
            return

        IMAGES_DIR.mkdir(parents=True, exist_ok=True)

        if self.current_line_num not in self.images_per_line:
            self.images_per_line[self.current_line_num] = []

        added = 0
        for fpath in files:
            src = Path(fpath)
            ext = src.suffix.lower()
            if ext not in (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"):
                continue
            new_name = src.name
            dest = IMAGES_DIR / new_name
            counter = 1
            while dest.exists():
                stem = src.stem
                new_name = f"{stem}_{counter}{ext}"
                dest = IMAGES_DIR / new_name
                counter += 1
            shutil.copy2(str(src), str(dest))
            rel_path = str(dest.relative_to(BASE_DIR))
            existing = [e for e in self.images_per_line[self.current_line_num]
                        if (e["path"] if isinstance(e, dict) else e) == rel_path]
            if not existing:
                self.images_per_line[self.current_line_num].append({"path": rel_path, "source": ""})
                added += 1

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
        if not HAS_PIL:
            self.show_info("PIL/Pillow required for clipboard paste.")
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
        IMAGES_DIR.mkdir(parents=True, exist_ok=True)

        dialog = tk.Toplevel(self.root)
        dialog.title("Paste Image")
        dialog.geometry("500x580")
        dialog.transient(self.root)
        dialog.grab_set()

        preview_size = (460, 360)
        preview = img.copy()
        preview.thumbnail(preview_size, Image.LANCZOS)
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
        ttk.Label(info_frame, text=f"Size: {original_w} x {original_h} px", foreground="gray").pack(anchor=tk.W)

        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=15)

        def do_ok():
            try:
                line = self.current_line_num
                if line is None:
                    messagebox.showerror("Error", "No line selected.", parent=dialog)
                    return

                save_img = img
                ext = ".png"
                try:
                    if save_img.mode == "RGBA":
                        ext = ".png"
                    elif save_img.mode == "RGB":
                        ext = ".jpg"
                    else:
                        save_img = save_img.convert("RGB")
                        ext = ".jpg"
                except Exception:
                    ext = ".png"

                now = datetime.datetime.now()
                base_name = now.strftime("pasted_%Y%m%d_%H%M%S")
                fname = base_name + ext
                dest = IMAGES_DIR / fname
                counter = 1
                while dest.exists():
                    fname = f"{base_name}_{counter}{ext}"
                    dest = IMAGES_DIR / fname
                    counter += 1

                if ext == ".jpg":
                    save_img.convert("RGB").save(str(dest), "JPEG", quality=92)
                else:
                    save_img.save(str(dest))

                rel_path = str(dest.relative_to(BASE_DIR))
                src_text = source_text_var.get().strip()

                if line not in self.images_per_line:
                    self.images_per_line[line] = []
                self.images_per_line[line].append({"path": rel_path, "source": src_text})

                self.display_images(line)
                self.refresh_line_list()
                self.save_json(silent=True)
                self.show_info(f"Pasted {fname}")
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
        self.status_var.set(
            f"Git: {self.git_commit_id[:12]}  |  "
            f"Lines: {max_lines}  |  "
            f"Lines with images: {len(self.images_per_line)}  |  "
            f"Total images: {total_images}"
        )

    def show_info(self, msg):
        self.status_var.set(msg)


def main():
    root = tk.Tk()
    app = TimelineImageManager(root)
    root.mainloop()


if __name__ == "__main__":
    main()
