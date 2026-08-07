import os
from datetime import datetime


OUTPUT = "PROJECT_CONTEXT.md"


IGNORE_DIRS = {
    "venv",
    ".git",
    "__pycache__",
    "node_modules",
    ".idea",
    ".vscode",
    "dist",
    "build",
    ".pytest_cache"
}


IGNORE_FILES = {
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    OUTPUT,
    "export_project.py"
}


INCLUDE_EXTENSIONS = {
    ".py",
    ".tsx",
    ".ts",
    ".jsx",
    ".js",
    ".css",
    ".html",
    ".md",
    ".json",
    ".sql",
    ".env.example"
}


IMPORTANT_FIRST = [
    "README.md",
    "readme.md",
    "requirements.txt",
    "package.json",
    "main.py",
    "database.py",
    "models.py",
    "schemas.py"
]


def should_ignore(path):

    parts = path.replace("\\", "/").split("/")

    for part in parts:
        if part in IGNORE_DIRS:
            return True

    if os.path.basename(path) in IGNORE_FILES:
        return True

    return False



def should_include(path):

    if should_ignore(path):
        return False

    _, ext = os.path.splitext(path)

    return ext in INCLUDE_EXTENSIONS



def get_files():

    files=[]

    for root, dirs, filenames in os.walk("."):

        dirs[:] = [
            d for d in dirs
            if d not in IGNORE_DIRS
        ]

        for filename in filenames:

            path=os.path.join(root,filename)

            if should_include(path):
                files.append(path)


    # important files first
    files.sort(
        key=lambda x:
        (
            0 if os.path.basename(x) in IMPORTANT_FIRST else 1,
            x
        )
    )

    return files



def write_tree(out):

    out.write("# PROJECT STRUCTURE\n\n")

    for file in get_files():

        out.write(
            f"- {file.replace('./','')}\n"
        )



def write_files(out):

    out.write(
        "\n\n# PROJECT FILES\n"
    )


    for file in get_files():

        out.write(
            "\n\n"
            + "="*80
            + "\n"
        )

        out.write(
            f"# FILE: {file}\n"
        )

        out.write(
            "="*80
            + "\n\n"
        )


        try:

            with open(
                file,
                "r",
                encoding="utf-8"
            ) as f:

                content=f.read()


            ext=os.path.splitext(file)[1][1:]

            out.write(
                f"```{ext}\n"
            )


            # add line numbers
            for i,line in enumerate(
                content.splitlines(),
                start=1
            ):
                out.write(
                    f"{i:04} | {line}\n"
                )


            out.write(
                "\n```\n"
            )


        except Exception as e:

            out.write(
                f"ERROR READING FILE: {e}\n"
            )



with open(
    OUTPUT,
    "w",
    encoding="utf-8"
) as out:


    out.write(
f"""
# PROJECT CONTEXT

Generated:
{datetime.now()}

Purpose:
This document contains the complete source code
of the project for AI assistance.

AI ROLE:

Act as a senior developer mentor.

Do not automatically rewrite everything.

Explain:
- architecture
- problems
- possible solutions
- reasoning

Then suggest code for me to implement.

"""


    )


    write_tree(out)

    write_files(out)



print(
    "PROJECT_CONTEXT.md generated"
)