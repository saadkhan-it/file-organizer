"""
Core file-organizing logic.

The Organizer class scans a directory, decides where each file belongs based on
its extension, and either moves it (default) or reports what *would* happen
(dry run).
"""

import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from config import IGNORED_FILES
from logger import get_logger
from utils import EXTENSION_LOOKUP, category_for, resolve_collision


@dataclass
class OrganizeResult:
    """Summary returned after an organize() run, useful for tests and reports."""
    moved: List[Path] = field(default_factory=list)
    skipped: List[Path] = field(default_factory=list)
    errors: List[tuple] = field(default_factory=list)  # (path, exception)


class Organizer:
    def __init__(self, target_dir: Path, dry_run: bool = False, verbose: bool = False):
        """Create an organizer bound to a specific directory.

        Args:
            target_dir: Directory whose top-level files should be sorted.
            dry_run: If True, log intended moves without touching the filesystem.
            verbose: Enable debug-level logging.
        """
        self.target_dir = Path(target_dir).expanduser().resolve()
        self.dry_run = dry_run
        self.log = get_logger(verbose=verbose)

    def organize(self) -> OrganizeResult:
        """Walk the target directory and sort files into category subfolders."""
        if not self.target_dir.is_dir():
            raise NotADirectoryError(f"Not a directory: {self.target_dir}")

        # Snapshot the directory listing first so we don't recurse into folders
        # we create while iterating.
        entries = list(self.target_dir.iterdir())
        # Remember category folder names so we never move them into themselves.
        category_dirs = {c for c in EXTENSION_LOOKUP.values()} | {"Other"}

        result = OrganizeResult()
        self.log.info("Organizing %s (dry_run=%s)", self.target_dir, self.dry_run)

        for entry in entries:
            if self._should_skip(entry, category_dirs):
                self.log.debug("Skipping %s", entry.name)
                result.skipped.append(entry)
                continue

            try:
                new_path = self._move_file(entry)
                result.moved.append(new_path)
            except OSError as exc:
                # Permission errors, file-in-use, cross-device moves, etc.
                self.log.error("Failed to move %s: %s", entry.name, exc)
                result.errors.append((entry, exc))

        self.log.info(
            "Done. moved=%d skipped=%d errors=%d",
            len(result.moved), len(result.skipped), len(result.errors),
        )
        return result

    def _should_skip(self, entry: Path, category_dirs: set) -> bool:
        """Decide whether a directory entry should be left alone."""
        if entry.is_dir():
            # Don't touch existing folders, including ones we may have created.
            return True
        if entry.name.lower() in IGNORED_FILES:
            return True
        # Skip hidden files (Unix convention) — safer default.
        if entry.name.startswith("."):
            return True
        # Avoid moving a file that lives in a category folder already (defensive).
        if entry.parent.name in category_dirs:
            return True
        return False

    def _move_file(self, source: Path) -> Path:
        """Move a single file into its category folder, returning the new path."""
        category = category_for(source, EXTENSION_LOOKUP)
        dest_dir = self.target_dir / category
        destination = resolve_collision(dest_dir / source.name)

        if self.dry_run:
            self.log.info("[dry-run] %s -> %s", source.name, destination)
            return destination

        dest_dir.mkdir(exist_ok=True)
        # shutil.move handles cross-filesystem moves; Path.rename does not.
        shutil.move(str(source), str(destination))
        self.log.info("Moved %s -> %s/%s", source.name, category, destination.name)
        return destination
