#!/usr/bin/env python3
"""make.fun entry for news-image-20261120: "The World in One Day".

The graded program. It places the finished front-page image that ships
in this repository at /output/entry.png.

The picture was drawn at build time by gen_image.py (Pillow + DejaVu)
from the verified world news of Friday 20 November 2026: Trump pushing
the Iran war decision to 2027, the Trump-Putin-Xi peace declaration,
Cyclone Akvan's landfall on the Odisha coast, Anthropic's 17% jump on
its market debut, GTA VI passing $1.8 billion in sales, and a tanker
catching fire after hitting a mine east of the Strait of Hormuz.

This program does no drawing and needs no network: it copies fixed
bytes, so the two graded runs write identical output. Standard
library only; the output directory comes from MAKEFUN_OUTPUT_DIR
outside the grader, or /output inside it.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGE_NAME = "entry.png"


def run():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, IMAGE_NAME)
    dst = os.path.join(out_dir, IMAGE_NAME)
    if not os.path.isfile(src):
        print("entry image missing:", src, file=sys.stderr)
        return 1
    shutil.copyfile(src, dst)
    src_size = os.path.getsize(src)
    if os.path.getsize(dst) != src_size:
        print("incomplete copy:", dst, file=sys.stderr)
        return 1
    print("wrote", dst, src_size, "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(run())
