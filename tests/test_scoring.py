"""评分模块测试."""

from pathlib import Path

import pytest

from novel_creator.config import (
    CHAPTER_MIN_WORDS,
    PARAGRAPH_MAX_CHARS,
    VAULT_DIR,
)
from novel_creator.scoring import (
    _calc_english_ratio,
    _check_empty_lines,
    _check_paragraphs,
    _estimate_deai_score,
    _score_word_count,
    score_chapter,
)


class TestWordScoring:
    """字数字评分测试."""

    def test_optimal_range(self):
        assert _score_word_count(3000) == 100.0

    def test_too_short(self):
        assert _score_word_count(1000) < 100.0

    def test_too_long(self):
        assert _score_word_count(5000) < 100.0

    def test_minimum_boundary(self):
        assert _score_word_count(CHAPTER_MIN_WORDS) == 100.0


class TestEnglishRatio:
    """英文比例测试."""

    def test_pure_chinese(self):
        assert _calc_english_ratio("纯中文测试内容") == 0.0

    def test_mixed_content(self):
        ratio = _calc_english_ratio("Hello世界ABC测试")
        assert 0.3 < ratio < 0.7

    def test_empty_text(self):
        assert _calc_english_ratio("") == 0.0


class TestParagraphCheck:
    """段落检查测试."""

    def test_normal_paragraph(self):
        issues = _check_paragraphs("短段落。\n也很短。")
        assert len(issues) == 0

    def test_long_paragraph(self):
        long_text = "测" * (PARAGRAPH_MAX_CHARS + 10)
        issues = _check_paragraphs(long_text)
        assert len(issues) >= 1

    def test_multiple_paragraphs(self):
        text = "第一段内容。\n第二段内容。\n第三段内容。"
        issues = _check_paragraphs(text)
        assert len(issues) == 0


class TestEmptyLines:
    """空行检查测试."""

    def test_no_empty_lines(self):
        issues = _check_empty_lines("行一\n行二\n行三")
        assert len(issues) == 0

    def test_consecutive_empty_lines(self):
        issues = _check_empty_lines("行一\n\n\n行二")
        assert len(issues) > 0


class TestScoreChapter:
    """章节评分测试."""

    def test_score_sample_male(self):
        path = VAULT_DIR / "Samples" / "sample-male" / "第1章 初入局中.md"
        if path.exists():
            result = score_chapter(path)
            # 迷你样例字数不足2500，评分函数正确返回未通过
            assert result == 1
        else:
            pytest.skip("样例文件不存在")

    def test_score_sample_female(self):
        path = VAULT_DIR / "Samples" / "sample-female" / "第1章 重生归来.md"
        if path.exists():
            result = score_chapter(path)
            # 迷你样例字数不足2500，评分函数正确返回未通过
            assert result == 1
        else:
            pytest.skip("样例文件不存在")

    def test_score_nonexistent_file(self):
        result = score_chapter(Path("/nonexistent/file.md"))
        assert result == 1


class TestDeaiEstimation:
    """去 AI 味评分估算测试."""

    def test_clean_text(self):
        score = _estimate_deai_score("这是一段自然的中文段落，没有AI腔。")
        assert score >= 80

    def test_banned_pattern_detected(self):
        score = _estimate_deai_score("他抖了一下——不是冷，是灵石在动。")
        assert score < 70  # 应该被扣分

    def test_over_explain_detected(self):
        score = _estimate_deai_score("这意味着我们需要重新考虑。总而言之，事情就是这样。")
        assert score < 85
