#!/bin/env python3

import argparse
import re
from pathlib import Path


def generate_toc_from_contents(contents: str):
    headers = re.findall(r"#{2,6} .+", contents)
    toc = "\n## Table of Contents\n\n"
    for header in headers:
        toc += format_toc_line_for_header(header)
    return toc


def format_toc_line_for_header(header: str):
    level = header.count("#")
    text = header.replace("#", "").strip()
    link = "#" + "-".join(text.lower().split())
    return f"{'    '*(level-2)}-   [{text}]({link})\n"


def remove_toc_if_present(contents: str) -> str:
    return re.sub(
        r"\n## Table of Contents\n\n([^#]|\(#)+\n\n", "\n", contents, flags=re.MULTILINE
    )


def add_or_renew_toc_in_contents(old_contents: str) -> str:
    old_tocless_contents = remove_toc_if_present(old_contents)
    toc = generate_toc_from_contents(old_tocless_contents)
    return insert_toc_into_contents(toc, old_tocless_contents)


def insert_toc_into_contents(toc: str, contents: str) -> str:
    return re.sub(r"\n(?=## )", toc + "\n", contents, count=1, flags=re.MULTILINE)


def add_or_renew_toc_in_file(file_path: Path):
    old_contents = file_path.read_text(encoding="utf-8")
    new_contents = add_or_renew_toc_in_contents(old_contents)

    if old_contents == new_contents:
        print(f"{file_path}: Already contains the correct table of contents")
    else:
        file_path.write_text(new_contents, encoding="utf-8")
        print(f"{file_path}: Added table of contents.")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Add a table of contents to one or more markdown files."
    )
    parser.add_argument(
        "file_paths", type=Path, nargs="*", help="Path to the markdown file."
    )
    return parser.parse_args()


def main():
    args = parse_args()
    for md in args.file_paths:
        add_or_renew_toc_in_file(md)


if __name__ == "__main__":
    main()
