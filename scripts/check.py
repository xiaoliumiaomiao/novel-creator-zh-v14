#!/usr/bin/env python3
"""Novel Creator ZH V14 — 质量检查脚本 (Python)."""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CHECKS = [
    ("Ruff lint", ["ruff", "check", "."]),
    ("Unit tests", [sys.executable, "-m", "pytest", "--tb=short"]),
    ("CLI smoke", [sys.executable, "-m", "novel_creator.cli", "--help"]),
    ("Markdown/YAML lint", [sys.executable, "-m", "novel_creator.cli", "lint"]),
    ("Dashboard", [sys.executable, "-m", "novel_creator.cli", "dashboard"]),
    ("Publish check", [sys.executable, "-m", "novel_creator.cli", "publish-check"]),
    ("Package build", [sys.executable, "-m", "build"]),
]


def run_check(name: str, cmd: list[str]) -> bool:
    """Run a single check, return True if passed."""
    print(f"\n{'='*50}")
    print(f"  {name}")
    print(f"{'='*50}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
            timeout=120,
        )
        if result.returncode == 0:
            print("  ✓ PASS")
            return True
        else:
            print(f"  ✗ FAIL (exit code {result.returncode})")
            if result.stdout:
                print(result.stdout[-300:])
            if result.stderr:
                print(result.stderr[-300:])
            return False
    except FileNotFoundError:
        print("  ⊘ SKIP (tool not found)")
        return True  # Not a failure if tool missing
    except subprocess.TimeoutExpired:
        print("  ✗ TIMEOUT")
        return False


def main() -> int:
    print("=" * 50)
    print("  Novel Creator ZH V14 — 质量检查")
    print("=" * 50)

    all_passed = True
    for name, cmd in CHECKS:
        if not run_check(name, cmd):
            all_passed = False

    print(f"\n{'='*50}")
    if all_passed:
        print("  全部通过 ✓")
        print(f"{'='*50}")
        return 0
    else:
        print("  存在问题 ✗")
        print(f"{'='*50}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
