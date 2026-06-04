#!/usr/bin/env python3
"""Git 同步脚本 — 命令行独立运行版本."""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def git_sync() -> int:
    """安全 Git 同步."""
    print("Git 同步...")

    # 1. 运行测试
    print("[1/3] 运行测试...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--tb=short"],
        capture_output=True, text=True, cwd=str(PROJECT_ROOT),
    )
    if result.returncode != 0:
        print("测试未通过，停止同步")
        return 1
    print("  ✓ 测试通过")

    # 2. 检查分支
    print("[2/3] 检查分支...")
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True, text=True, cwd=str(PROJECT_ROOT),
    )
    branch = result.stdout.strip()
    if branch in ("main", "master"):
        print("禁止直推主干！")
        return 1
    print(f"  ✓ 分支: {branch}")

    # 3. 提交和推送
    print("[3/3] 提交推送...")
    subprocess.run(["git", "add", "."], cwd=str(PROJECT_ROOT))
    subprocess.run(["git", "commit", "-m", f"更新 — {branch}"], cwd=str(PROJECT_ROOT))
    subprocess.run(["git", "push", "origin", branch], cwd=str(PROJECT_ROOT))

    print("✓ Git 同步完成")
    return 0


if __name__ == "__main__":
    sys.exit(git_sync())
