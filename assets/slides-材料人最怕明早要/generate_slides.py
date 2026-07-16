#!/usr/bin/env python3
"""Thin wrapper: regenerate Douyin slides via Chrome + render.html."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent


def main() -> int:
    script = DIR / "render_chrome.sh"
    result = subprocess.run(["bash", str(script)], cwd=DIR)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
