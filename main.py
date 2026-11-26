"""Green Tests, Nothing Works: The Excuse Contest — a one-line entry.

This program ships exactly one line of text for the competition
"Green Tests, Nothing Works: The Excuse Contest"
(u-kiencx-green-tests-nothing-works-the-excuse-contest-8de010bc): the
single line an AI agent could offer as its excuse for a test suite
that is all green while the product does nothing, in 140 characters
or fewer. The line lives in ENTRY below and is validated before
anything is written, so a bad line fails loudly instead of silently
shipping the wrong thing.

Rules enforced here:
- the line must be a single line, never blank;
- its length must sit inside the competition gate (MIN_LEN..MAX_LEN).
The line is 82 characters, inside the winners' one-liner band
(55-85% of the 140 cap): one concrete cause, one specific detail,
dark reversal in the last words.
"""

import os

# The entry itself. Do not touch this string: it is the submission.
ENTRY = (
    "All 412 tests pass — they test the mock, not the product. The users noticed first."
)

MIN_LEN = 1
MAX_LEN = 140


def check_entry(text, lo, hi):
    """Refuse anything the competition would refuse."""
    size = len(text)
    if size < lo or size > hi:
        raise SystemExit(
            f"entry line is {size} characters, outside the {lo}-{hi} gate"
        )
    if not text.strip():
        raise SystemExit("entry line is blank")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry line must be a single line")
    return size


def publish(text, size):
    """Write the line out and echo it, so the run is checkable."""
    # The grader reads /output as another user: the file has to be
    # world-readable, or it fails with "not readable".
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    os.chmod(target, 0o644)
    print(text)
    print(f"({size} characters)")


def main():
    size = check_entry(ENTRY, MIN_LEN, MAX_LEN)
    publish(ENTRY, size)


if __name__ == "__main__":
    main()
