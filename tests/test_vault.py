"""Vault 模块测试."""

from novel_creator.config import VAULT_DIR
from novel_creator.vault import ensure_vault_exists, init_vault


def test_init_vault():
    """测试 vault 初始化."""
    result = init_vault()
    assert result == 0
    assert VAULT_DIR.exists()
    assert (VAULT_DIR / "00_Dashboard").exists()
    assert (VAULT_DIR / "Templates").exists()
    assert (VAULT_DIR / "Samples").exists()
    assert (VAULT_DIR / "References" / "README.md").exists()


def test_ensure_vault_exists():
    """测试 vault 存在性检查."""
    assert ensure_vault_exists() is True


def test_dashboard_file():
    """测试仪表盘文件是否生成."""
    dashboard = VAULT_DIR / "00_Dashboard" / "Dashboard.md"
    assert dashboard.exists()
    content = dashboard.read_text(encoding="utf-8")
    assert "创作仪表盘" in content


def test_sample_male_exists():
    """测试男频样例."""
    sample = VAULT_DIR / "Samples" / "sample-male" / "第1章 初入局中.md"
    assert sample.exists()
    content = sample.read_text(encoding="utf-8")
    assert "type: chapter" in content
    assert "track: male" in content


def test_sample_female_exists():
    """测试女频样例."""
    sample = VAULT_DIR / "Samples" / "sample-female" / "第1章 重生归来.md"
    assert sample.exists()
    content = sample.read_text(encoding="utf-8")
    assert "type: chapter" in content
    assert "track: female" in content


def test_templates_exist():
    """测试模板文件."""
    templates = VAULT_DIR / "Templates"
    assert (templates / "章节模板.md").exists()
    assert (templates / "人物卡模板.md").exists()
    assert (templates / "世界观模板.md").exists()
    assert (templates / "章纲模板.md").exists()


def test_references_readme():
    """测试参考库 README 内容."""
    ref_readme = VAULT_DIR / "References" / "README.md"
    content = ref_readme.read_text(encoding="utf-8")
    assert "不提交 Git" in content
    assert "禁止" in content
