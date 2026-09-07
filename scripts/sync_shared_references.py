#!/usr/bin/env python3
"""Bundle shared workflow references for standalone skill installation."""

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REFERENCE = Path("references/long-running-work.md")
SOURCE = ROOT / "byte-auto" / REFERENCE
CONSUMERS = ("byte-build", "byte-do", "byte-plan", "byte-research", "byte-status")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Report missing or stale copies without writing")
    args = parser.parse_args()
    if not SOURCE.is_file():
        parser.error(f"Missing canonical reference: {SOURCE}")
    content = SOURCE.read_bytes()
    stale = []
    for name in CONSUMERS:
        target = ROOT / name / REFERENCE
        if target.is_file() and target.read_bytes() == content:
            continue
        stale.append(name)
        if not args.check:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
    if args.check and stale:
        print("Missing or stale shared references: " + ", ".join(stale))
        print("Run python3 scripts/sync_shared_references.py")
        return 1
    print("Shared references match canonical source." if args.check else f"Updated {len(stale)} shared references.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
