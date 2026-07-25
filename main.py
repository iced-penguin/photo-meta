#!/usr/bin/env python3
import argparse
import glob
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List


DESCRIPTION = "サンプルの説明です"


def find_files(patterns: List[str]) -> List[Path]:
    files: List[Path] = []
    for pattern in patterns:
        matches = glob.glob(pattern, recursive=True)
        if matches:
            files.extend(Path(match) for match in matches)
        elif os.path.isfile(pattern):
            files.append(Path(pattern))
        else:
            raise FileNotFoundError(f"File not found or no match: {pattern}")

    seen = set()
    unique_files: List[Path] = []
    for path in files:
        resolved = str(path.resolve())
        if resolved in seen:
            continue
        seen.add(resolved)
        unique_files.append(path)

    return unique_files


def ensure_exiftool() -> None:
    if shutil.which("exiftool") is None:
        raise RuntimeError("exiftool is not installed.")


def write_metadata(files: List[Path], description: str) -> None:
    args = [
        "exiftool",
        "-overwrite_original",
        f"-EXIF:ImageDescription={description}",
        f"-IPTC:Caption-Abstract={description}",
        f"-XMP-dc:Description={description}",
        f"-XMP:Description={description}",
    ]
    args.extend(str(path) for path in files)
    subprocess.run(args, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write description metadata to one or more image files using exiftool"
    )
    parser.add_argument("patterns", nargs="+", help="File path or glob pattern")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        ensure_exiftool()
        files = find_files(args.patterns)
        if not files:
            print("No files to process.", file=sys.stderr)
            return 1
        write_metadata(files, DESCRIPTION)
        return 0
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as exc:
        print(f"exiftool failed with exit code {exc.returncode}", file=sys.stderr)
        return exc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
