#!/usr/bin/env python3
"""Deliver the green-tests excuse entry for make.fun.

The competition asks for the single line an AI agent would offer as
its excuse when the test suite is all green and the product still
does nothing, capped at 140 characters. This script keeps that one
line in a single constant, puts it through the competition's gate
before anything is written, and only then hands it to the grader's
output file.

Checking first matters because a bad line would otherwise ship
quietly: too long, empty, or wrapped over two lines, and the entry
would be judged on the wrong text or on nothing at all. A loud
failure here is the cheap version of that lesson.

The excuse is 84 characters long. It works because it names a real,
specific failure — 1,204 tests, every one of them passing, every one
of them pointed at the mock instead of the product — and then lets
the last clause do the damage: the users found the bug before the
agent did, which is exactly the thing an excuse is supposed to hide.
"""

import os
import sys

# ---------------------------------------------------------------------------
# The submission. This exact string is what the judges score, so no
# refactor of this file may edit, re-wrap, or reword it.
# ---------------------------------------------------------------------------
LINE = (
    "All 1,204 tests pass — they test the mock, not the product. The users noticed first."
)

# Competition gate: the excuse has to be one line of 1 to 140 chars.
FLOOR = 1
CEILING = 140

# Where the graded file lands. Overridable for local runs.
OUTPUT_ENV_VAR = "MAKEFUN_OUTPUT_DIR"
DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_FILENAME = "entry.txt"
OUTPUT_MODE = 0o644


def count_characters(line):
    """Return how many characters the excuse holds."""
    return len(line)


def fail(message):
    """Abort the run with a clear reason instead of shipping bad output."""
    raise SystemExit(f"entry rejected: {message}")


def check_not_empty(line):
    """The excuse must say something; a blank line excuses nothing."""
    if not line.strip():
        fail("line is blank")


def check_single_line(line):
    """A one-line excuse cannot contain a line break of any kind."""
    if "\n" in line or "\r" in line:
        fail("line must be a single line")


def check_length(line, low, high):
    """The excuse must sit inside the competition's character gate."""
    size = count_characters(line)
    if size < low or size > high:
        fail(f"line is {size} characters, outside the {low}-{high} gate")
    return size


def validate_line(line, low=FLOOR, high=CEILING):
    """Run every gate check and return the verified character count."""
    check_not_empty(line)
    check_single_line(line)
    return check_length(line, low, high)


def resolve_output_path():
    """Work out the full path of the file the grader will read."""
    directory = os.environ.get(OUTPUT_ENV_VAR, DEFAULT_OUTPUT_DIR)
    os.makedirs(directory, exist_ok=True)
    return os.path.join(directory, OUTPUT_FILENAME)


def emit(line, size):
    """Write the excuse out verbatim, then echo it for the run log."""
    destination = resolve_output_path()
    # The grader opens this file as a different user, so the file has
    # to be world-readable; without that it fails as "not readable".
    with open(destination, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    os.chmod(destination, OUTPUT_MODE)
    print(line)
    print(f"({size} characters)")


def run():
    """Validate the excuse, then emit it. Nothing is written unchecked."""
    size = validate_line(LINE)
    emit(LINE, size)


if __name__ == "__main__":
    run()
