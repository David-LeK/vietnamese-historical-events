#!/usr/bin/env python3
"""
check_duplicate_images.py - Detect duplicate timeline images.

Enforces the repository rule that every historical image may illustrate
at most ONE event per timeline file:
  * each image path in images/ may be referenced at most once in
    timelines_vi.md and at most once in timelines_en.md
    (the same image appears exactly once in VI and once in EN, under the
    paired bilingual events);
  * no two files in images/ may have identical content (byte-identical,
    detected via MD5) or be perceptually identical re-encodes of the same
    picture (detected via 16x16 average hash).

Also reports (as warnings, not failures):
  * orphaned files in images/ that no timeline references;
  * image paths referenced by markdown but missing from disk.

Usage:
    python check_duplicate_images.py [--quiet] [--images-dir DIR]
                                     [--vi FILE] [--en FILE]

Exit code 0 = no duplicates / misuse found, 1 = problems found.
"""

import argparse
import glob
import hashlib
import os
import re
import sys

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    print("[ERROR] Pillow is required (pip install pillow).")
    sys.exit(2)

VI_FILE = "timelines_vi.md"
EN_FILE = "timelines_en.md"
IMAGES_DIR = "images"

IMG_REF_RE = re.compile(r"!\[.*?\]\((images/[^)]+)\)")
HASH_SIZE = 16


def md5_of_file(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def average_hash(path, size=HASH_SIZE):
    """16x16 average hash (256-bit string). Exact matches only are used."""
    with Image.open(path) as im:
        im = im.convert("L").resize((size, size), Image.BILINEAR)
        pixels = list(im.get_flattened_data())
    avg = sum(pixels) / len(pixels)
    return "".join("1" if px > avg else "0" for px in pixels)


def difference_hash(path, size=HASH_SIZE):
    """16x16 difference hash (256-bit string).

    Compares each pixel with its right neighbour instead of using absolute
    brightness, so global edits (brighter/darker, contrast, gamma,
    re-compression, resizing) only flip a few bits. Two pictures of the
    same scene typically differ by ~0-12 bits, while unrelated pictures
    differ by ~100+ bits, leaving a wide safety margin for a threshold.
    """
    with Image.open(path) as im:
        im = im.convert("L").resize((size + 1, size), Image.BILINEAR)
        pixels = list(im.get_flattened_data())
    bits = []
    for row in range(size):
        for col in range(size):
            left = pixels[row * (size + 1) + col]
            right = pixels[row * (size + 1) + col + 1]
            bits.append("1" if left > right else "0")
    return "".join(bits)


def hamming_distance(hash_a, hash_b):
    return sum(c1 != c2 for c1, c2 in zip(hash_a, hash_b))


def collect_references(md_file):
    """Return {image_path: [line_numbers]} for every embedded image."""
    refs = {}
    with open(md_file, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            for path in IMG_REF_RE.findall(line):
                refs.setdefault(path, []).append(lineno)
    return refs


def find_duplicate_files(images_dir, near_threshold=16):
    """Return (byte_dup_groups, perceptual_dup_groups, near_dup_pairs,
    unreadable, files).

    * byte/perceptual groups are sorted lists of filenames with identical
      content (failures);
    * near_dup_pairs is a list of (file_a, file_b, distance) with
      0 < dHash distance <= near_threshold: slightly edited copies of the
      same picture (brighter, contrast, recompressed...). Reported for
      human review because heavy crops of different photos can rarely
      collide.
    """
    files = sorted(glob.glob(os.path.join(images_dir, "*.webp")))
    by_md5, by_ahash, dhashes = {}, {}, {}
    unreadable = []
    for path in files:
        name = os.path.basename(path)
        by_md5.setdefault(md5_of_file(path), []).append(name)
        try:
            by_ahash.setdefault(average_hash(path), []).append(name)
            dhashes[name] = difference_hash(path)
        except Exception:
            unreadable.append(name)
    byte_dups = sorted([sorted(g) for g in by_md5.values() if len(g) > 1])
    byte_sets = {tuple(g) for g in byte_dups}
    perceptual_dups = sorted(
        [sorted(g) for g in by_ahash.values() if len(g) > 1
         and tuple(sorted(g)) not in byte_sets]
    )
    known = set(byte_sets) | {tuple(g) for g in perceptual_dups}
    near_dups = []
    names = sorted(dhashes)
    for idx, name_a in enumerate(names):
        for name_b in names[idx + 1:]:
            dist = hamming_distance(dhashes[name_a], dhashes[name_b])
            if 0 < dist <= near_threshold:
                pair = tuple(sorted((name_a, name_b)))
                if pair not in known:
                    near_dups.append((pair[0], pair[1], dist))
    near_dups.sort(key=lambda item: (item[2], item[0], item[1]))
    return byte_dups, perceptual_dups, near_dups, unreadable, files


def check(images_dir=IMAGES_DIR, vi_file=VI_FILE, en_file=EN_FILE,
          quiet=False, near_threshold=16, strict=False):
    """Run all duplicate checks. Returns True when the tree is clean."""
    errors, warnings = [], []

    byte_dups, perceptual_dups, near_dups, unreadable, files = \
        find_duplicate_files(images_dir, near_threshold=near_threshold)
    for group in byte_dups:
        errors.append("Byte-identical files: " + ", ".join(group))
    for group in perceptual_dups:
        errors.append("Perceptually identical files (re-encoded copy): "
                      + ", ".join(group))
    for name_a, name_b, dist in near_dups:
        msg = ("Near-duplicate suspects (dHash distance %d, possibly a "
               "slightly edited copy - brighter, contrast, recompressed): "
               "%s <=> %s" % (dist, name_a, name_b))
        (errors if strict else warnings).append(msg)
    for name in unreadable:
        errors.append("Unreadable image file: %s" % name)

    refs_vi = collect_references(vi_file)
    refs_en = collect_references(en_file)

    for path, lines in sorted(refs_vi.items()):
        if len(lines) > 1:
            errors.append(
                "%s referenced %dx in %s (lines %s): one image may "
                "illustrate only one event" % (
                    path, len(lines), vi_file, lines))
    for path, lines in sorted(refs_en.items()):
        if len(lines) > 1:
            errors.append(
                "%s referenced %dx in %s (lines %s): one image may "
                "illustrate only one event" % (
                    path, len(lines), en_file, lines))

    set_vi, set_en = set(refs_vi), set(refs_en)
    for path in sorted(set_vi - set_en):
        errors.append("%s referenced in %s but missing in %s"
                      % (path, vi_file, en_file))
    for path in sorted(set_en - set_vi):
        errors.append("%s referenced in %s but missing in %s"
                      % (path, en_file, vi_file))

    on_disk = {os.path.join(images_dir, os.path.basename(p))
               for p in glob.glob(os.path.join(images_dir, "*.webp"))}
    md_base = os.path.dirname(os.path.abspath(vi_file))

    def exists_on_disk(path):
        return (os.path.isfile(path)
                or os.path.isfile(os.path.join(md_base, path)))

    for path in sorted(set_vi | set_en):
        if not exists_on_disk(path):
            errors.append("Referenced image missing from disk: %s" % path)
    for path in sorted(on_disk):
        rel = os.path.relpath(path).replace(os.sep, "/")
        if rel not in set_vi and rel not in set_en:
            warnings.append("Orphaned file (referenced by no timeline): %s"
                            % rel)

    if not quiet or errors or warnings:
        print("Checked %d image file(s), %d VI reference(s), "
              "%d EN reference(s)." % (len(files), sum(len(v) for v in
                                                       refs_vi.values()),
                                       sum(len(v) for v in
                                           refs_en.values())))
        for msg in errors:
            print("  [FAIL] " + msg)
        for msg in warnings:
            print("  [WARN] " + msg)
    if errors:
        print("[FAIL] DUPLICATE IMAGE CHECK FAILED (%d problem(s))."
              % len(errors))
        return False
    if warnings and not quiet:
        print("[SUCCESS] NO DUPLICATE IMAGES FOUND "
              "(%d orphan warning(s) to review)." % len(warnings))
    else:
        print("[SUCCESS] NO DUPLICATE IMAGES FOUND!")
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Detect duplicate / multiply-used timeline images.")
    parser.add_argument("--quiet", action="store_true",
                        help="Print only the final verdict.")
    parser.add_argument("--images-dir", default=IMAGES_DIR)
    parser.add_argument("--vi", default=VI_FILE)
    parser.add_argument("--en", default=EN_FILE)
    parser.add_argument("--near-threshold", type=int, default=16,
                        help="Max dHash Hamming distance (of 256 bits) to "
                             "report a pair as near-duplicate suspects "
                             "(default: 16).")
    parser.add_argument("--strict", action="store_true",
                        help="Treat near-duplicate suspects as failures "
                             "instead of warnings.")
    args = parser.parse_args(argv)
    ok = check(images_dir=args.images_dir, vi_file=args.vi, en_file=args.en,
               quiet=args.quiet, near_threshold=args.near_threshold,
               strict=args.strict)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
