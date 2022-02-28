#!/usr/bin/env python3
# Copyright 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""A simple script for downloading latest dictionaries."""

import glob
import os
from pathlib import Path
import sys
import tempfile
import urllib.request
import zipfile


DIR = Path(__file__).resolve().parent


DICTIONARIES = (
    "https://sourceforge.net/projects/wordlist/files/speller/2019.10.06/"
    "hunspell-en_US-2019.10.06.zip",
    "https://sourceforge.net/projects/wordlist/files/speller/2019.10.06/"
    "hunspell-en_CA-2019.10.06.zip",
    "https://sourceforge.net/projects/wordlist/files/speller/2019.10.06/"
    "hunspell-en_GB-ise-2019.10.06.zip",
    "https://sourceforge.net/projects/wordlist/files/speller/2019.10.06/"
    "hunspell-en_GB-ize-2019.10.06.zip",
    "https://sourceforge.net/projects/wordlist/files/speller/2019.10.06/"
    "hunspell-en_AU-2019.10.06.zip",
    "https://github.com/b00f/lilak/releases/latest/download/fa-IR.zip",
    # NOTE: need to remove IGNORE from uk_UA.aff
    "https://github.com/brown-uk/dict_uk/releases/latest/download/"
    "hunspell-uk_UA.zip",
)


def main(argv):
    if argv:
        sys.exit(f"{__file__}: script takes no args")
    os.chdir(DIR)

    for url in DICTIONARIES:
        print(f"Downloading {url}")
        with tempfile.NamedTemporaryFile() as tmp:
            with urllib.request.urlopen(url) as response:
                tmp.write(response.read())
            tmp.flush()
            zipfile.ZipFile(tmp.name).extractall()

        for name in glob.glob("*en_GB-ise*"):
            os.rename(name, name.replace("-ise", ""))
        for name in glob.glob("*en_GB-ize*"):
            os.rename(name, name.replace("-ize", "_oxendict"))
        for name in glob.glob("*fa-IR.*"):
            os.rename(name, name.replace("-", "_"))

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
