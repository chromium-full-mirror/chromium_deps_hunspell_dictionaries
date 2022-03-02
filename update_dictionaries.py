#!/usr/bin/env python3
# Copyright 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""A simple script for downloading latest dictionaries."""

import glob
import os
from pathlib import Path
import shutil
import sys
import urllib.request
import zipfile


DIR = Path(__file__).resolve().parent
CACHE_DIR = DIR / "cache"


DICTIONARIES = (
    "https://sourceforge.net/projects/wordlist/files/speller/2020.12.07/"
    "hunspell-en_US-2020.12.07.zip",
    "https://sourceforge.net/projects/wordlist/files/speller/2020.12.07/"
    "hunspell-en_CA-2020.12.07.zip",
    "https://sourceforge.net/projects/wordlist/files/speller/2020.12.07/"
    "hunspell-en_GB-ise-2020.12.07.zip",
    "https://sourceforge.net/projects/wordlist/files/speller/2020.12.07/"
    "hunspell-en_GB-ize-2020.12.07.zip",
    "https://sourceforge.net/projects/wordlist/files/speller/2020.12.07/"
    "hunspell-en_AU-2020.12.07.zip",
    "https://github.com/b00f/lilak/releases/latest/download/fa-IR.zip",
    # NOTE: need to remove IGNORE from uk_UA.aff
    # TODO: This archive no longer exists.
    # "https://github.com/brown-uk/dict_uk/releases/latest/download/"
    # "hunspell-uk_UA.zip",
)


def main(argv):
    if argv:
        sys.exit(f"{__file__}: script takes no args")
    os.chdir(DIR)

    CACHE_DIR.mkdir(exist_ok=True)

    for url in DICTIONARIES:
        cache = CACHE_DIR / url.rsplit("/", 1)[1]
        if not cache.exists():
            print(f"Downloading {url} to cache {cache}")
            tmp = cache.with_suffix(".tmp")
            with urllib.request.urlopen(url) as response:
                tmp.write_bytes(response.read())
            tmp.rename(cache)

        print(f"Extracting {cache.name}")
        zipfile.ZipFile(cache).extractall()

    for name in glob.glob("*en_GB-ise*"):
        os.rename(name, name.replace("-ise", ""))
    for name in glob.glob("*en_GB-ize*"):
        os.rename(name, name.replace("-ize", "_oxendict"))
    for name in glob.glob("fa-IR/*fa-IR.*"):
        os.rename(name, os.path.basename(name.replace("-", "_")))
    shutil.rmtree("fa-IR")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
