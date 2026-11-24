#!/usr/bin/env python3
"""One Letter: Coffee or Tea -- a make.fun bounty entry.

The whole entry is a single letter: A, the vote for coffee. This
program keeps that letter as data, checks it against the competition
gate (exactly one character, valid UTF-8, not whitespace), and writes
it -- with nothing added, not even a newline -- to the entry file the
scorer reads.
"""

import os
import sys

# The ballot: A says coffee, B says tea. This entry stands with coffee,
# the louder, brighter, more awake of the two drinks.
BALLOT = "A"

# The gate allows exactly one character, and it must be a real choice.
ALLOWED = ("A", "B")
MIN_LEN = 1
MAX_LEN = 1


def check_ballot(letter):
    """Return the letter unchanged if it passes the gate, else raise."""
    if letter not in ALLOWED:
        raise ValueError(
            "ballot must be one of %r, got %r" % (ALLOWED, letter)
        )
    if not MIN_LEN <= len(letter) <= MAX_LEN:
        raise ValueError("ballot must be exactly one character long")
    if letter.strip() == "":
        raise ValueError("ballot must not be whitespace")
    letter.encode("utf-8")  # raises if the letter cannot be encoded
    return letter


def entry_path():
    """Where the scorer reads the entry: $MAKEFUN_OUTPUT_DIR/entry.txt."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def verify_written(path, letter):
    """Re-read the entry file and insist its bytes are the letter alone."""
    with open(path, "rb") as handle:
        on_disk = handle.read()
    if on_disk != letter.encode("utf-8"):
        raise IOError(
            "entry file holds %r, expected exactly %r"
            % (on_disk, letter.encode("utf-8"))
        )


def main():
    letter = check_ballot(BALLOT)
    path = entry_path()
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    # newline="" plus no added terminator: the file is the letter alone.
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(letter)
    verify_written(path, letter)
    return 0


if __name__ == "__main__":
    sys.exit(main())
