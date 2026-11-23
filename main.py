#!/usr/bin/env python3
"""news-image-20261122 v3 — graded program (pure Python stdlib).

The poster is a pre-rendered illustration (entry.png, bundled in this
repo). This program copies that bundled image to the grader's output
location and verifies the copy byte-for-byte with SHA-256. It does no
rendering itself: the drawing was done at build time with Pillow and
the editorial-illustration library, which the grader does not have.

Output resolution order:
  1. $MAKEFUN_OUTPUT_DIR/entry.png   (grader harness)
  2. /output/entry.png               (container fallback)
  3. output.png                      (local fallback, next to this file)

The source image is looked up next to this file first, then in the
current working directory. The copy is verified by comparing the
SHA-256 of the source and the destination; the program exits non-zero
on any mismatch.
"""

import hashlib
import os
import shutil
import sys

ENTRY_NAME = "entry.png"


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def find_source():
    here = os.path.dirname(os.path.abspath(__file__))
    for cand in (os.path.join(here, ENTRY_NAME),
                 os.path.join(os.getcwd(), ENTRY_NAME)):
        if os.path.isfile(cand):
            return cand
    return None


def main():
    src = find_source()
    if src is None:
        print("error: bundled %s not found next to main.py or in cwd"
              % ENTRY_NAME, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    targets = []
    if out_dir:
        targets.append(os.path.join(out_dir, ENTRY_NAME))
    targets.append("/output/" + ENTRY_NAME)
    targets.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "output.png"))

    want = sha256_of(src)
    size = os.path.getsize(src)
    last_err = None
    for dst in targets:
        try:
            parent = os.path.dirname(dst)
            if parent:
                os.makedirs(parent, exist_ok=True)
            shutil.copyfile(src, dst)
        except OSError as exc:
            last_err = exc
            continue
        got = sha256_of(dst)
        if got != want:
            print("error: sha256 mismatch for %s (want %s, got %s)"
                  % (dst, want, got), file=sys.stderr)
            return 1
        print("wrote %s  %d bytes  sha256 %s" % (dst, size, got))
        return 0

    print("error: could not write any output target: %s" % last_err,
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
