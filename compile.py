#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Final, List

import tqdm

# Constants
FOLDER: Final[str] = "tex"
OUT: Final[str] = "main"
MODULE: Final[str] = "main"
TARGET: Final[str] = "main"
TEX_FILE_PATH: Final[str] = os.path.join(FOLDER, f"{MODULE}.tex")

COLOR_RESET: Final[str] = "\033[0m"
COLOR_GREEN: Final[str] = "\033[1m\033[38;2;11;218;81m"
COLOR_YELLOW: Final[str] = "\033[1m\033[38;2;250;208;44m"


def run_command(cmd: List[str]) -> subprocess.CompletedProcess[str]:
    """Run a shell command and return completed process."""
    cmd = " && ".join(cmd)
    return subprocess.run(cmd, shell=True, check=True, text=True, executable="/bin/bash", capture_output=True)


def compile_pdf() -> subprocess.CompletedProcess[str]:
    return run_command(
        [
            f"cd {FOLDER}",
            f"pdflatex -shell-escape -halt-on-error -jobname={OUT} {TARGET}.tex",
        ]
    )


def clean() -> None:
    """Remove LaTeX auxiliary files."""
    paths = [
        os.path.join(FOLDER, f"_minted-{OUT}"),
        os.path.join(FOLDER, f"{OUT}.aux"),
        os.path.join(FOLDER, f"{OUT}.log"),
        os.path.join(FOLDER, f"{OUT}.out"),
        os.path.join(FOLDER, f"{OUT}.toc"),
        os.path.join(FOLDER, f"{OUT}.blg"),
        os.path.join(FOLDER, f"{OUT}.bbl"),
    ]

    for path in paths:
        p = Path(path)
        if p.is_dir():
            shutil.rmtree(p, ignore_errors=True)
        elif p.exists():
            p.unlink()


def count_warnings(output: str) -> int:
    """Count LaTeX warnings in output."""
    count: int = 0
    for line in output.splitlines():
        if "Warning" in line or (":" in line and any(char.isdigit() for char in line)):
            print(line)
            count += 1
    return count


def compile_latex() -> None:
    """Full LaTeX + BibTeX compilation pipeline."""

    if not Path(TEX_FILE_PATH).exists():
        print(f"Error: {TEX_FILE_PATH} not found.")
        sys.exit(1)

    # First pass
    _ = compile_pdf()

    # BibTeX
    run_command([f"cd {FOLDER}", f"bibtex {OUT}"])

    # Multiple passes
    for _ in tqdm.tqdm(range(3), desc="Compiling PDF..."):
        _ = compile_pdf()

    # Final pass with captured output
    result = compile_pdf()

    warnings: int = count_warnings(result.stdout)
    if warnings > 0:
        print(
            f"{COLOR_YELLOW}Number of warnings during this compilation: "
            f"{warnings}{COLOR_RESET}"
        )

        return

    print(
        f"{COLOR_GREEN}Successful compilation, no warnings were generated!{COLOR_RESET}"
    )


def main(argv: List[str]) -> None:
    """CLI entry point."""

    compile_latex()
    clean()


if __name__ == "__main__":
    main(sys.argv)
