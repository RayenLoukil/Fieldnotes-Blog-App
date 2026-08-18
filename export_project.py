import os
from datetime import datetime


OUTPUT = "PROJECT_CONTEXT.md"


# ============================================================
# CONFIGURATION
# ============================================================

IGNORE_DIRS = {
    # Python
    "venv",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",

    # Git / IDE
    ".git",
    ".idea",
    ".vscode",

    # JavaScript / Node
    "node_modules",

    # Build / generated
    "dist",
    "build",
    "coverage",
    ".next",
    ".nuxt",
    "out",
    "target",

    # Other caches
    ".cache",
    ".parcel-cache",
}


IGNORE_FILES = {
    # Lock files
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "poetry.lock",

    # This script / output
    OUTPUT,
    "export_project.py",

    # Common generated files
    ".DS_Store",
    "Thumbs.db",
}


# Files that are useful for understanding the project.
INCLUDE_EXTENSIONS = {
    # Python
    ".py",

    # JavaScript / TypeScript
    ".js",
    ".jsx",
    ".ts",
    ".tsx",

    # Web
    ".html",
    ".css",
    ".scss",

    # Backend / database
    ".sql",

    # Documentation
    ".md",

    # Configuration
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",

    # Environment templates
    ".example",
}


# Important files appear first.
IMPORTANT_FIRST = {
    "README.md",
    "readme.md",
    "requirements.txt",
    "pyproject.toml",
    "package.json",
    "main.py",
    "app.py",
    "database.py",
    "models.py",
    "schemas.py",
    "config.py",
    "settings.py",
}


# Files above this size are treated as possible data/generated files.
# IMPORTANT:
# This does NOT limit source-code lines.
# It only prevents accidentally dumping giant data files.
MAX_NON_SOURCE_FILE_MB = 2


# Source-code extensions that should NEVER be size-filtered.
SOURCE_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".html",
    ".css",
    ".scss",
    ".sql",
}


# ============================================================
# HELPERS
# ============================================================

def clean_path(path):
    """Make paths consistent inside the markdown file."""
    return path.replace("\\", "/")


def get_extension(path):
    """Return lowercase file extension."""
    return os.path.splitext(path)[1].lower()


def is_source_file(path):
    """Check whether a file is actual source code."""
    return get_extension(path) in SOURCE_EXTENSIONS


def should_include(path):
    """Determine whether a file should be exported."""

    filename = os.path.basename(path)
    extension = get_extension(path)

    # Ignore specific files
    if filename in IGNORE_FILES:
        return False

    # Ignore unknown extensions
    if extension not in INCLUDE_EXTENSIONS:
        return False

    # Source files are always allowed.
    # We never truncate or size-limit source code.
    if is_source_file(path):
        return True

    # For docs/config/data-like files, avoid enormous files.
    try:
        size_mb = os.path.getsize(path) / (1024 * 1024)

        if size_mb > MAX_NON_SOURCE_FILE_MB:
            return False

    except OSError:
        return False

    return True


# ============================================================
# FIND PROJECT FILES
# ============================================================

def get_files():
    """
    Scan the project once and return all relevant files.
    """

    files = []

    for root, dirs, filenames in os.walk("."):

        # Prevent os.walk from entering ignored directories.
        dirs[:] = [
            directory
            for directory in dirs
            if directory not in IGNORE_DIRS
        ]

        for filename in filenames:

            path = os.path.join(root, filename)

            if should_include(path):
                files.append(path)

    # Important files first,
    # then everything else alphabetically.
    files.sort(
        key=lambda path: (
            0 if os.path.basename(path) in IMPORTANT_FIRST else 1,
            clean_path(path).lower()
        )
    )

    return files


# ============================================================
# PROJECT TREE
# ============================================================

def write_tree(out, files):

    out.write("# PROJECT STRUCTURE\n\n")

    for file in files:

        out.write(
            f"- {clean_path(file)}\n"
        )


# ============================================================
# WRITE FILE
# ============================================================

def write_file(out, path):

    try:

        with open(
            path,
            "r",
            encoding="utf-8",
            errors="replace"
        ) as f:

            # Read the COMPLETE file.
            lines = f.readlines()

    except Exception as error:

        out.write(
            f"ERROR READING FILE: {error}\n"
        )

        return

    # Skip completely empty files.
    if not any(line.strip() for line in lines):
        return

    language = get_extension(path).lstrip(".")

    # --------------------------------------------------------
    # FILE HEADER
    # --------------------------------------------------------

    out.write("\n\n")
    out.write("=" * 80)
    out.write("\n")

    out.write(
        f"# FILE: {clean_path(path)}\n"
    )

    out.write("=" * 80)
    out.write("\n\n")

    # --------------------------------------------------------
    # CODE BLOCK
    # --------------------------------------------------------

    out.write(
        f"```{language}\n"
    )

    # --------------------------------------------------------
    # COMPLETE FILE WITH LINE NUMBERS
    # --------------------------------------------------------

    for line_number, line in enumerate(
        lines,
        start=1
    ):

        line = line.rstrip("\r\n")

        out.write(
            f"{line_number:04} | {line}\n"
        )

    # --------------------------------------------------------
    # END CODE BLOCK
    # --------------------------------------------------------

    out.write(
        "\n```\n"
    )


# ============================================================
# GENERATE CONTEXT
# ============================================================

def generate_context():

    # Scan the project ONLY ONCE.
    files = get_files()

    with open(
        OUTPUT,
        "w",
        encoding="utf-8"
    ) as out:

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        out.write(
            "# PROJECT CONTEXT\n\n"
        )

        out.write(
            "Generated:\n"
        )

        out.write(
            f"{datetime.now()}\n\n"
        )

        out.write(
            "Purpose:\n"
            "This document contains the complete project "
            "structure and source code for AI assistance.\n\n"
        )

        out.write(
            "AI ROLE:\n\n"
            "Act as a senior developer mentor.\n\n"
            "Do not automatically rewrite everything.\n\n"
            "Explain:\n"
            "- architecture\n"
            "- problems\n"
            "- possible solutions\n"
            "- reasoning\n\n"
            "Then suggest code for me to implement.\n"
        )

        # ----------------------------------------------------
        # PROJECT STRUCTURE
        # ----------------------------------------------------

        write_tree(
            out,
            files
        )

        # ----------------------------------------------------
        # PROJECT FILES
        # ----------------------------------------------------

        out.write(
            "\n\n# PROJECT FILES\n"
        )

        for file in files:

            write_file(
                out,
                file
            )

    print(
        "\nPROJECT_CONTEXT.md generated successfully."
    )

    print(
        f"Files included: {len(files)}"
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    generate_context()