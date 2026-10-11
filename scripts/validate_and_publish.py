#!/usr/bin/env python3
"""Validate the upstream Fanboy uBO render; never overwrite a good list on bad output."""

from __future__ import annotations

import sys
from pathlib import Path

MIN_SCRIPTLETS = 2_000
MIN_COSMETIC_RULES = 30_000
MAX_BYTES = 10 * 1024 * 1024  # Chroma's subscription response-size limit.


def substantive_lines(text: str) -> list[str]:
    # flrender regenerates the build timestamp even when the actual filters do not change.
    return [line for line in text.splitlines() if not line.startswith("! Last modified:")]


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: validate_and_publish.py <candidate.txt> <published.txt>", file=sys.stderr)
        return 2

    candidate = Path(sys.argv[1])
    published = Path(sys.argv[2])
    if not candidate.is_file():
        raise SystemExit(f"Missing build output: {candidate}")

    raw = candidate.read_bytes()
    if not (100_000 < len(raw) <= MAX_BYTES):
        raise SystemExit(f"Rejected: unreasonable list size ({len(raw):,} bytes)")

    text = raw.decode("utf-8-sig")
    lines = text.splitlines()
    if not text.startswith("[Adblock Plus 2.0]"):
        raise SystemExit("Rejected: not a filter-list response")
    if "Fanboy's Annoyance List" not in text[:1500]:
        raise SystemExit("Rejected: unexpected list title")
    if any(line.lstrip().startswith("%include ") for line in lines):
        raise SystemExit("Rejected: unresolved EasyList template includes")

    scriptlets = sum("##+js(" in line for line in lines if not line.startswith("!"))
    cosmetics = sum(
        ("##" in line or "#@#" in line) and "##+js(" not in line
        for line in lines if line and not line.startswith("!")
    )
    print(f"Verified {len(raw):,} bytes; {cosmetics:,} cosmetic filters; {scriptlets:,} scriptlets")

    if scriptlets < MIN_SCRIPTLETS or cosmetics < MIN_COSMETIC_RULES:
        raise SystemExit("Rejected: too few rules; might be an ABP build or truncated download")

    if published.exists():
        previous = published.read_text(encoding="utf-8-sig")
        if substantive_lines(previous) == substantive_lines(text):
            print("Rules unchanged; retaining existing file and original timestamp.")
            candidate.unlink()
            return 0

    candidate.replace(published)
    print(f"Published {published}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
