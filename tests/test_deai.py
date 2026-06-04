"""去 AI 味模块测试."""

from pathlib import Path

from novel_creator.config import VAULT_DIR
from novel_creator.deai import (
    _analyze_ai_voice,
    _apply_detail_enhancements,
    _apply_dramatic_boost,
    _apply_expression_fixes,
    _checklist_score,
    _dual_scoring,
    _reader_perspective_score,
    process_deai,
    process_deai_batch,
)


class TestExpressionFixes:
    """表达修复测试."""

    def test_remove_banned_pattern(self):
        original = "他抖了一下——不是冷，是灵石在动。"
        fixed = _apply_expression_fixes(original)
        assert "——不是" not in fixed or len(fixed) < len(original)

    def test_remove_explanation_marker(self):
        original = "这意味着，我们需要改变策略。"
        fixed = _apply_expression_fixes(original)
        assert "这意味着" not in fixed

    def test_preserve_meaning(self):
        """修复后应保留基本含义."""
        original = "他心想：这事不简单。这背后一定有问题。"
        fixed = _apply_expression_fixes(original)
        assert "这事不简单" in fixed
        assert "背后" in fixed


class TestDetailEnhancements:
    """细节增强测试."""

    def test_detail_enhancement(self):
        text = '她说：“我知道了。”'
        result = _apply_detail_enhancements(text, dramatic=False)
        # 不改变原文核心
        assert "我知道了" in result

    def test_dramatic_boost(self):
        text = "测试段落。"
        result = _apply_dramatic_boost(text)
        assert "dramatic-boost" in result.lower()
        assert "测试段落" in result


class TestAIVoiceAnalysis:
    """AI 腔分析测试."""

    def test_analyze_clean_text(self):
        analysis = _analyze_ai_voice("这是一段自然的中文写作。没有AI腔的特征。")
        assert analysis["total_sentences"] > 0
        assert analysis["banned_found"] == []

    def test_analyze_banned_pattern(self):
        analysis = _analyze_ai_voice("他抖了一下——不是冷，是灵石在动。")
        assert len(analysis["banned_found"]) > 0

    def test_analyze_over_explain(self):
        analysis = _analyze_ai_voice(
            "他知道自己必须这样做。他意识到这很重要。他决定采取行动。"
        )
        assert analysis["over_explain_count"] >= 3

    def test_analyze_suspect_words(self):
        analysis = _analyze_ai_voice("仿佛某种力量在推动，似乎一切都不一样了。")
        suspect_total = sum(analysis["suspect_words"].values())
        assert suspect_total >= 3

    def test_avg_sentence_length(self):
        text = "短句。也短。这是一句比较长的句子用来测试平均句长计算是否准确。"
        analysis = _analyze_ai_voice(text)
        assert 5 < analysis["avg_sentence_length"] < 30


class TestDualScoring:
    """双评分测试."""

    def test_dual_scoring_returns_dict(self):
        scores = _dual_scoring("自然的中文表达。有对话和节奏。")
        assert "checklist" in scores
        assert "reader" in scores
        assert "overall" in scores

    def test_checklist_clean_text(self):
        score = _checklist_score("这是一段自然流畅的中文表达，没有任何AI腔特征。")
        assert score >= 80

    def test_checklist_banned_penalty(self):
        clean = _checklist_score("自然流畅的文本。")
        banned = _checklist_score("他抖了一下——不是冷，是灵石在动。总而言之，这是关键。")
        # 禁用句式应导致扣分
        assert banned < clean

    def test_reader_clean_text(self):
        score = _reader_perspective_score("他说：“你好。”她回应：“你好。”两人相视一笑。")
        assert score >= 80

    def test_reader_banned_heavy_penalty(self):
        clean = _reader_perspective_score("自然流畅的段落。有对白和动作。")
        banned = _reader_perspective_score("他抖了一下——不是冷，是灵石在动。")
        # 禁用句式应从读者视角扣分更重
        assert banned < clean


class TestDeaiProcess:
    """去 AI 味处理流程测试."""

    def test_invalid_mode(self):
        result = process_deai(Path("dummy.md"), mode="invalid-mode")
        assert result == 1

    def test_nonexistent_file(self):
        result = process_deai(Path("/nonexistent/file.md"), mode="detail-light")
        assert result == 1

    def test_process_sample_male(self):
        """处理男频样例."""
        path = VAULT_DIR / "Samples" / "sample-male" / "第1章 初入局中.md"
        if not path.exists():
            return
        result = process_deai(path, mode="expression-only")
        assert result == 0
        # 检查三稿生成
        for suffix in [".original.md", ".natural.md", ".web-serial.md"]:
            out = path.parent / f"{path.stem}{suffix}"
            assert out.exists(), f"缺少: {out.name}"
            out.unlink()  # 清理

    def test_process_sample_female(self):
        """处理女频样例."""
        path = VAULT_DIR / "Samples" / "sample-female" / "第1章 重生归来.md"
        if not path.exists():
            return
        result = process_deai(path, mode="detail-light")
        assert result == 0
        for suffix in [".original.md", ".natural.md", ".web-serial.md"]:
            out = path.parent / f"{path.stem}{suffix}"
            assert out.exists()
            out.unlink()

    def test_batch_mode(self):
        """批量模式."""
        paths = [
            VAULT_DIR / "Samples" / "sample-male" / "第1章 初入局中.md",
            VAULT_DIR / "Samples" / "sample-female" / "第1章 重生归来.md",
        ]
        existing = [p for p in paths if p.exists()]
        if not existing:
            return
        result = process_deai_batch(existing, mode="expression-only")
        assert result == 0
        # 清理
        for p in existing:
            for suffix in [".original.md", ".natural.md", ".web-serial.md"]:
                out = p.parent / f"{p.stem}{suffix}"
                if out.exists():
                    out.unlink()
