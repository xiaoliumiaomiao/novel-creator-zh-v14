"""CLI smoke tests."""

import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Ensure subprocess uses UTF-8 on Windows
_ENV = os.environ.copy()
_ENV["PYTHONIOENCODING"] = "utf-8"


def _run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(PROJECT_ROOT),
        env=_ENV,
    )


def test_cli_help():
    """验证 novelctl --help 可运行."""
    result = _run([sys.executable, "-m", "novel_creator.cli", "--help"])
    assert result.returncode == 0, f"CLI help failed: {result.stderr}"
    assert "novelctl" in result.stdout


def test_cli_version():
    """验证 novelctl --version 可运行."""
    result = _run([sys.executable, "-m", "novel_creator.cli", "--version"])
    assert result.returncode == 0
    assert "novelctl v14" in result.stdout


def test_cli_unknown_command():
    """验证未知命令返回非零码."""
    result = _run([sys.executable, "-m", "novel_creator.cli", "nonexistent-cmd"])
    assert result.returncode != 0


def test_cli_init_vault(tmp_path):
    """验证 init-vault 命令."""
    result = _run([sys.executable, "-m", "novel_creator.cli", "init-vault"])
    assert result.returncode == 0, f"init-vault failed: {result.stderr}"
    assert "初始化" in result.stdout


def test_cli_lint():
    """验证 lint 命令."""
    result = _run([sys.executable, "-m", "novel_creator.cli", "lint"])
    # lint 可能在成功时返回 0 或失败时返回 1
    assert result.returncode in (0, 1)


def test_cli_dashboard():
    """验证 dashboard 命令."""
    result = _run([sys.executable, "-m", "novel_creator.cli", "dashboard"])
    assert result.returncode == 0, f"dashboard failed: {result.stderr}"
