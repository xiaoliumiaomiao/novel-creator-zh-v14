"""Lint 模块测试."""

from pathlib import Path

from novel_creator.config import VAULT_DIR
from novel_creator.linting import (
    _check_file,
    _count_effective_chars,
    _extract_body,
    _parse_frontmatter,
    run_lint,
)


class TestEffectiveCharCount:
    """有效字数统计测试."""

    def test_chinese_only(self):
        assert _count_effective_chars("这是一段中文测试") == 8

    def test_chinese_and_digits(self):
        assert _count_effective_chars("第1章 测试") == 5  # 第、1、章、测、试

    def test_ignore_punctuation(self):
        assert _count_effective_chars("你好，世界！") == 4

    def test_ignore_whitespace(self):
        assert _count_effective_chars("你好 世界") == 4

    def test_ignore_english(self):
        assert _count_effective_chars("Hello世界ABC") == 2  # 世界 = 2


class TestFrontmatterParsing:
    """YAML frontmatter 解析测试."""

    def test_valid_frontmatter(self):
        content = "---\ntype: chapter\nstatus: drafted\n---\n\n正文"
        metadata = _parse_frontmatter(content)
        assert metadata == {"type": "chapter", "status": "drafted"}

    def test_missing_frontmatter(self):
        content = "# 没有 frontmatter\n\n正文"
        metadata = _parse_frontmatter(content)
        assert metadata == {}

    def test_empty_frontmatter(self):
        content = "---\n---\n\n正文"
        metadata = _parse_frontmatter(content)
        assert metadata == {}


class TestBodyExtraction:
    """正文提取测试."""

    def test_extract_body(self):
        content = "---\ntype: chapter\n---\n\n# 第1章 标题\n\n正文内容"
        body = _extract_body(content)
        assert "正文内容" in body
        assert "---" not in body

    def test_no_frontmatter(self):
        content = "# 直接正文\n\n内容"
        body = _extract_body(content)
        assert body == content


class TestFileCheck:
    """文件检查测试."""

    def test_valid_chapter(self):
        """测试有效章节文件."""
        chapter_path = VAULT_DIR / "Samples" / "sample-male" / "第1章 初入局中.md"
        issues = _check_file(chapter_path)
        # 验证函数不崩溃，返回 issue 列表
        assert isinstance(issues, list)

    def test_check_nonexistent_file(self):
        """测试不存在的文件."""
        issues = _check_file(Path("/nonexistent/file.md"))
        assert len(issues) > 0


class TestRunLint:
    """完整 lint 运行测试."""

    def test_run_lint(self):
        result = run_lint()
        # lint 应该可以运行完成
        assert result in (0, 1)


class TestStyleBlacklist:
    """禁用句式测试."""

    def test_banned_pattern_detected(self):
        """测试 "A——不是B" 模式被检测到."""
        # 直接验证 linting 逻辑中的正则
        from novel_creator.linting import BANNED_PATTERNS
        pattern = BANNED_PATTERNS[0][0]
        assert pattern.search("他抖了一下——不是冷，是灵石在动。")
