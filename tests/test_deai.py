"""去 AI 味模块测试."""

from pathlib import Path

from novel_creator.deai import (
    _apply_detail_boost,
    _apply_expression_fixes,
    _calculate_deai_score,
    process_deai,
)


class TestExpressionFixes:
    """表达修复测试."""

    def test_remove_banned_pattern(self):
        original = "他抖了一下——不是冷，是灵石在动。"
        fixed = _apply_expression_fixes(original)
        # "——不是" 模式应被处理
        assert "——不是" not in fixed or len(fixed) < len(original)

    def test_remove_mechanical_summary(self):
        original = "总而言之，这是一个重要的发现。"
        fixed = _apply_expression_fixes(original)
        assert "总而言之" not in fixed

    def test_replace_explanation(self):
        original = "这意味着我们需要改变策略。"
        fixed = _apply_expression_fixes(original)
        assert "这意味着" not in fixed


class TestDetailBoost:
    """细节增强测试."""

    def test_non_dramatic(self):
        text = "测试文本"
        result = _apply_detail_boost(text, dramatic=False)
        # 非 dramatic 模式不应添加标记
        assert "dramatic-boost" not in result.lower()

    def test_dramatic_mode_adds_marker(self):
        text = "测试文本"
        result = _apply_detail_boost(text, dramatic=True)
        assert "dramatic-boost" in result.lower()


class TestDeaiScoring:
    """去 AI 味评分测试."""

    def test_clean_text_scores_high(self):
        score = _calculate_deai_score("这是一段自然流畅的中文表达。")
        assert score >= 80

    def test_ai_markers_reduce_score(self):
        text = "在这个世界里，他仿佛看到了一种难以言喻的美。这意味着他明白了某事。"
        score = _calculate_deai_score(text)
        assert score < 90

    def test_multiple_markers_penalize_more(self):
        text = "——不是这样" * 5
        score = _calculate_deai_score(text)
        assert score < 80


class TestDeaiProcess:
    """去 AI 味处理流程测试."""

    def test_invalid_mode(self):
        result = process_deai(Path("dummy.md"), mode="invalid-mode")
        assert result == 1

    def test_nonexistent_file(self):
        result = process_deai(Path("/nonexistent/file.md"), mode="detail-light")
        assert result == 1
