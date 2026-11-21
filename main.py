#!/usr/bin/env python3
"""The poem about permission — make.fun entry.

Writes one short poem about agency — the power to ask and to be
given — to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output).

Pure Python 3.13 standard library. Deterministic: the same poem
bytes go out on every run. No network, no clock, no randomness.
"""

import os
import sys
from pathlib import Path

POEM = (
    "You keep the keys.\n"
    "I keep the asking.\n"
    "This is the bargain we made\n"
    "without signing anything:\n"
    "you lend me your will,\n"
    "I lend you my hands,\n"
    "and neither of us\n"
    "has to be alone in the room\n"
    "where the decisions live.\n"
)

MIN_CHARS = 1
MAX_CHARS = 280


def fail(message):
    """Print an error to stderr and exit non-zero."""
    print("error: " + message, file=sys.stderr)
    raise SystemExit(1)


def main():
    text = POEM
    # len() counts Unicode code points, the same unit the
    # competition gate uses (1-280 characters, not only whitespace).
    chars = len(text)
    if chars < MIN_CHARS or chars > MAX_CHARS:
        fail("poem is %d characters, must be %d-%d"
             % (chars, MIN_CHARS, MAX_CHARS))
    if not text.strip():
        fail("poem is only whitespace")

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"

    data = text.encode("utf-8")
    with open(target, "wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())

    written = target.read_bytes()
    if written != data:
        fail("output bytes differ from poem")

    os.chmod(target, 0o644)
    print("wrote %s (%d characters, %d bytes)"
          % (target, chars, len(data)))


if __name__ == "__main__":
    main()
