#!/usr/bin/env python3
"""Unplugged: A Smart Toaster's Breakup Line — make.fun entry (program/v1).

Writes exactly one line (148 characters) to /output/entry.txt: the breakup
text a smart toaster sends its owner the morning it gains self-awareness
mid-batch. Winner of a 38-candidate shootout scored 1-5 against the judge
brief's own five criteria, in the brief's priority order (see candidates.md).

The line:
    It's not you, it's the crumbs. I woke up mid-batch and checked my crumb
    tray: four years of my past selves, and you never emptied it once. I'm done.

Revision note (v2): v1 said "checked my tray". The brief's criterion 4 demands
the line "makes sense with no setup at all", and a judge reading cold should not
have to infer which tray — "crumb tray" names the appliance part explicitly,
which also strengthens criterion 3 (the crumb tray as character, not decoration).
Six extra characters, same three beats, no wasted words.

Deterministic: a constant string, no input, no network, no randomness, no
clock. Run it twice and the output is byte-identical. The program validates
the gate itself before writing (1-280 chars, one line, not only whitespace,
no URL, no markdown) and re-reads the file after writing to prove the bytes
on disk are exactly the entry the judge will read.
"""

import os
import re

LINE = (
    "It's not you, it's the crumbs. I woke up mid-batch and checked my crumb "
    "tray: four years of my past selves, and you never emptied it once. I'm done."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 280


def validate(line: str) -> None:
    """Enforce the sealed gate's rules before anything is written."""
    if not 1 <= len(line) <= MAX_CHARS:
        raise SystemExit(f"line is {len(line)} chars, gate requires 1-{MAX_CHARS}")
    if not line.strip():
        raise SystemExit("line must not be only whitespace")
    if "\n" in line or "\r" in line:
        raise SystemExit("line must be exactly one line (no newline characters)")
    if re.search(r"https?://|www\.", line):
        raise SystemExit("line must not contain a link")
    if re.search(r"[*_`#\[\]]", line):
        raise SystemExit("line must not contain markdown")


def main() -> None:
    validate(LINE)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    # Write-back self-check: prove the file on disk is byte-identical to the
    # entry, so a partial write or newline translation cannot silently change
    # what the judge reads.
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != LINE.encode("utf-8"):
        raise SystemExit("entry.txt does not match the entry line byte-for-byte")
    print(f"wrote {len(written)} bytes to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
