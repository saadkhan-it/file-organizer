"""
Command-line entry point for the file organizer.

Run `python main.py --help` for usage details.
"""

import argparse
import sys
from pathlib import Path

from organizer import Organizer


def parse_args(argv=None) -> argparse.Namespace:
    """Build and parse the CLI argument list."""
    parser = argparse.ArgumentParser(
        description="Organize the files in a directory into subfolders by extension."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Directory to organize (defaults to current directory).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without moving any files.",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable debug-level logging.",
    )
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    target = Path(args.path)

    try:
        organizer = Organizer(target, dry_run=args.dry_run, verbose=args.verbose)
        result = organizer.organize()
    except (NotADirectoryError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    # Non-zero exit if any file failed to move — useful for shell scripting.
    return 0 if not result.errors else 2


if __name__ == "__main__":
    sys.exit(main())
