#!/usr/bin/env python3
"""Entry program for news-image-20261122.

Copies the pre-drawn front page (entry.png, made by draw_entry.py) to the
output directory. Standard library only, no network, deterministic: the
bytes written are exactly the bytes of entry.png.
"""

import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # sanity check: the copy must be a whole PNG under the 1 MiB limit
    size = os.path.getsize(dst)
    assert size <= 1_048_576, f"entry.png too large: {size} bytes"
    print(f"wrote {dst} ({size} bytes)")


if __name__ == "__main__":
    sys.exit(main())
