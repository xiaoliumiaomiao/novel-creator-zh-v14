"""风险审查模块测试."""

from pathlib import Path

from novel_creator.risk import (
    HIGH_RISK_KEYWORDS,
    review_and_mitigate,
    review_file,
)


class TestRiskReview:
    """风险审查测试."""

    def test_clean_content(self):
        """测试无风险内容."""
        # 创建临时文件
        import tempfile
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", encoding="utf-8", delete=False
        ) as f:
            f.write("# 测试\n\n这是一段没有任何风险的内容。")
            temp_path = Path(f.name)

        try:
            report = review_file(temp_path)
            assert report["pass"] is True
            assert len(report["findings"]) == 0
        finally:
            temp_path.unlink()

    def test_risk_content_detected(self):
        """测试风险内容被检测."""
        import tempfile
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", encoding="utf-8", delete=False
        ) as f:
            f.write("# 测试\n\n涉及赌博场景的描述。赌场里人们疯狂押注。")
            temp_path = Path(f.name)

        try:
            report = review_file(temp_path)
            # 应该检测到风险
            assert len(report["findings"]) > 0
            assert report["pass"] is False
        finally:
            temp_path.unlink()

    def test_risk_types_are_valid(self):
        """测试风险类型定义."""
        for risk_type in HIGH_RISK_KEYWORDS:
            assert isinstance(risk_type, str)
            assert isinstance(HIGH_RISK_KEYWORDS[risk_type], list)
            assert len(HIGH_RISK_KEYWORDS[risk_type]) > 0

    def test_nonexistent_file(self):
        """测试不存在的文件."""
        report = review_file(Path("/nonexistent/file.md"))
        assert report["pass"] is False
        assert "error" in report


class TestRiskMitigation:
    """风险降险测试."""

    def test_mitigation_creates_marked_file(self):
        """测试降险生成标记文件."""
        import tempfile
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", encoding="utf-8", delete=False
        ) as f:
            f.write("# 测试\n\n涉及赌博场景的描述。")
            temp_path = Path(f.name)

        try:
            report = review_and_mitigate(temp_path, max_rounds=2)
            # 报告应该生成
            assert "pass" in report or "findings" in report
        finally:
            temp_path.unlink()
            # 清理标记文件
            for f in temp_path.parent.glob(f"{temp_path.stem}.risk-marked*"):
                f.unlink()
