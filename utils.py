"""
Pure helper functions used by the organizer.

Kept free of side effects so they're easy to unit test in isolation.
"""

from pathlib import Path
from typing import Dict

from config import DEFAULT_CATEGORY, EXTENSION_MAP


def build_extension_lookup(extension_map: Dict[str, list]) -> Dict[str, str]:
    """Flatten the category->extensions map into an extension->category lookup.

    Returns a dict keyed by lowercase extension (no leading dot).
    """
    lookup: Dict[str, str] = {}
    for category, extensions in extension_map.items():
        for ext in extensions:
            lookup[ext.lower().lstrip(".")] = category
    return lookup


def category_for(file_path: Path, lookup: Dict[str, str]) -> str:
    """Return the destination category for a given file path.

    Falls back to DEFAULT_CATEGORY when the extension is unknown or missing.
    """
    # Path.suffix includes the leading dot, e.g. ".PNG" — normalize it.
    ext = file_path.suffix.lower().lstrip(".")
    return lookup.get(ext, DEFAULT_CATEGORY)


def resolve_collision(destination: Path) -> Path:
    """If `destination` already exists, return a non-colliding variant.

    Appends " (1)", " (2)", ... to the filename stem until a free name is found.
    This preserves the original extension.
    """
    if not destination.exists():
        return destination

    stem, suffix, parent = destination.stem, destination.suffix, destination.parent
    counter = 1
    while True:
        candidate = parent / f"{stem} ({counter}){suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


# Convenience: a ready-to-use lookup built from the config at import time.
EXTENSION_LOOKUP = build_extension_lookup(EXTENSION_MAP)
