#!/usr/bin/env python3
"""make.fun entry program for the news-image-20261118 bounty.

The poster is pre-rendered at build time (tools/generate_image.py) and
committed next to this script as entry.png. At run time the container has
no network and no Pillow, so this program only copies the pre-rendered
PNG to the make.fun output directory.

Stdlib only: os, pathlib, shutil. No network access.
"""

import os
import pathlib
import shutil

SOURCE = pathlib.Path(__file__).resolve().parent / "entry.png"
OUTPUT = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")) / "entry.png"


def main() -> int:
    if not SOURCE.is_file():
        raise FileNotFoundError(f"missing poster image: {SOURCE}")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())