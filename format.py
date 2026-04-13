#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path
from typing import List, Final


TEX_FILES_FOLDER: Final[str] = "tex/Chapters"
LATEX_FORMAT_FILE: Final[str] = "formatting.yaml"


def run(cmd: List[str]) -> subprocess.CompletedProcess[str]:
    """Run a shell command safely."""
    return subprocess.run(
        cmd, capture_output=True, text=True, check=True, executable="/bin/bash"
    )


def process_file(tex_file: Path, config_path: Path):
    print(f"Processing: {tex_file}")

    # Latexindent (overwrite, no backup)
    _ = run(["latexindent", "-w", "-l", str(config_path), str(tex_file)])

    # Format fmt (overwrite via temp + move)
    # fmt does NOT reliably edit in-place, so we redirect
    result = run(["fmt", "-w", "100", str(tex_file)])
    tex_file.write_text(result.stdout)


def main() -> None:
    root = Path(TEX_FILES_FOLDER)
    config_path = Path(LATEX_FORMAT_FILE)

    tex_files = list(root.rglob("*.tex"))
    if not tex_files:
        print("No .tex files found.")
        return

    for f in tex_files:
        try:
            process_file(f, config_path)
        except subprocess.CalledProcessError as e:
            print(f"Error processing {f}: {e}")


if __name__ == "__main__":
    main()
