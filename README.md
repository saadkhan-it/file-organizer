# File Organizer

A small Python automation tool that tidies up a folder by sorting its files
into subfolders based on file extension. Useful for cleaning out `Downloads/`,
`Desktop/`, or any directory that has become a dumping ground.

## Features

- Categorizes files into folders like `Images`, `Documents`, `Audio`, `Video`,
  `Archives`, `Code`, and more.
- Unknown extensions land in an `Other/` folder so nothing is ever lost.
- Filename collisions are handled automatically (`report.pdf` →
  `report (1).pdf`).
- Built-in **dry-run** mode previews every move before you commit.
- Verbose logging for debugging or audit trails.
- Pure-stdlib — no third-party dependencies.

## Project layout

```
file_organizer/
├── main.py        # CLI entry point
├── organizer.py   # Core Organizer class and move logic
├── config.py      # Category -> extension mapping
├── utils.py       # Pure helpers (lookup table, collision resolver)
├── logger.py      # Logging setup
└── README.md
```

## Requirements

- Python 3.8 or newer (uses `pathlib`, dataclasses, and f-strings).

## Usage

From inside the `file_organizer/` directory:

```bash
# Organize a specific folder
python main.py "C:\Users\Saad\Downloads"

# Preview what would happen without touching any files
python main.py "C:\Users\Saad\Downloads" --dry-run

# Organize the current directory with verbose logging
python main.py -v
```

### Exit codes

| Code | Meaning                                  |
|------|------------------------------------------|
| 0    | All files moved (or dry-run) successfully|
| 1    | Bad path / not a directory               |
| 2    | One or more files failed to move         |

## How categorization works

Edit `config.py` to customize. The `EXTENSION_MAP` dictionary maps a category
name (which becomes the folder name) to a list of extensions:

```python
EXTENSION_MAP = {
    "Images": ["jpg", "jpeg", "png", ...],
    "Documents": ["pdf", "docx", "txt", ...],
    # add your own categories here
}
```

Anything not listed in any category ends up in `Other/`.

## Safety notes

- The organizer only touches **top-level files** in the target directory; it
  never recurses into subfolders, so existing structure is preserved.
- Hidden files (`.foo`) and system files (`Thumbs.db`, `.DS_Store`,
  `desktop.ini`) are skipped by default.
- Always try `--dry-run` first on an important folder.

## Extending

- **Add a new category:** add an entry to `EXTENSION_MAP` in `config.py`.
- **Ignore additional filenames:** add them to `IGNORED_FILES` in `config.py`.
- **Change destination logic:** override `_move_file` on the `Organizer` class
  in `organizer.py`.
