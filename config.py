"""
Configuration for the file organizer.

Maps category names to a list of file extensions that belong to each category.
Extensions are matched case-insensitively and should be written without the
leading dot.
"""

# Mapping: category folder name -> list of extensions that belong in it.
EXTENSION_MAP = {
    "Images":       ["jpg", "jpeg", "png", "gif", "bmp", "svg", "webp", "ico", "tiff"],
    "Documents":    ["pdf", "doc", "docx", "txt", "rtf", "odt", "tex", "md"],
    "Spreadsheets": ["xls", "xlsx", "csv", "ods"],
    "Presentations":["ppt", "pptx", "odp", "key"],
    "Audio":        ["mp3", "wav", "flac", "aac", "ogg", "m4a", "wma"],
    "Video":        ["mp4", "mkv", "mov", "avi", "wmv", "flv", "webm"],
    "Archives":     ["zip", "rar", "7z", "tar", "gz", "bz2", "xz"],
    "Code":         ["py", "js", "ts", "html", "css", "java", "c", "cpp", "h",
                     "rs", "go", "rb", "php", "json", "xml", "yaml", "yml", "sh"],
    "Executables":  ["exe", "msi", "msix", "bat", "cmd", "app", "dmg", "deb", "rpm"],
    "Fonts":        ["ttf", "otf", "woff", "woff2"],
}

# Catch-all folder for extensions that don't match any category above.
DEFAULT_CATEGORY = "Other"

# Files that should never be moved (compared by exact filename, case-insensitive).
IGNORED_FILES = {
    ".ds_store",
    "thumbs.db",
    "desktop.ini",
}
