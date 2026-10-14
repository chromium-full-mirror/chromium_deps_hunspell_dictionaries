#!/usr/bin/env python3
# Copyright 2026 The Chromium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""Regenerates every .bdic file from its .aff, .dic and .dic_delta files.

Usage: convert_dictionaries.py path/to/convert_dict
"""

import os
import subprocess
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent

# Dictionaries whose sources are not named after them.
SOURCES = {
    "af-ZA": "af_ZA/af-ZA",
    "de-DE": "de_DE_neu",
    "fo-FO": "fo_FO/fo_FO",
}


def source(lang):
    if lang in SOURCES:
        return DIR / SOURCES[lang]
    # Try the name with an underscore (en_US), as is (hu-HU), then the
    # language alone (tr for tr-TR).
    for name in (lang.replace("-", "_"), lang, lang.split("-")[0]):
        if (DIR / f"{name}.dic").exists():
            return DIR / name
    sys.exit(f"No source found for {lang}")


def main(argv):
    if len(argv) != 1:
        sys.exit(f"usage: {__file__} path/to/convert_dict")
    for bdic in sorted(DIR.glob("*.bdic")):
        src = source(bdic.stem.rsplit("-", 2)[0])
        print(f"{bdic.name} <- {src.relative_to(DIR)}")
        subprocess.run([argv[0], src], check=True, stdout=subprocess.DEVNULL)
        os.replace(src.with_name(src.name + ".bdic"), bdic)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
