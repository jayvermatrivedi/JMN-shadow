"""Run all supported figure reproductions in one command."""

from __future__ import annotations

import os
import subprocess
import sys


EXAMPLE_SCRIPTS = [
    "reproduce_figure2a.py",
    "reproduce_figure2b.py",
    "reproduce_figure2c.py",
    "reproduce_figure2d.py",
]


def main() -> None:
    examples_dir = os.path.dirname(os.path.abspath(__file__))
    for script_name in EXAMPLE_SCRIPTS:
        script_path = os.path.join(examples_dir, script_name)
        print(f"Running {script_name} ...")
        subprocess.run([sys.executable, script_path], check=True)
    print("All supported figures were generated in the figures/ directory.")


if __name__ == "__main__":
    main()
