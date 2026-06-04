"""题材预设测试."""

from novel_creator.config import VAULT_DIR
from novel_creator.corpus import generate_all_genre_templates, generate_genre_template
from novel_creator.genre_presets import (
    FEMALE_GENRE_PRESETS,
    MALE_GENRE_PRESETS,
    get_forbidden_content,
    get_genre_preset,
    get_hook_types,
    get_opening_model,
    list_genres,
)


class TestGenrePresets:
    """题材预设测试."""

    def test_male_genres_count(self):
        """男频应有 8 种题材."""
        assert len(MALE_GENRE_PRESETS) == 8

    def test_female_genres_count(self):
        """女频应有 8 种题材."""
        assert len(FEMALE_GENRE_PRESETS) == 8

    def test_male_preset_fields(self):
        """男频每个题材应有必要字段."""
        required = ["name", "target_readers", "chapter_length", "hook_types",
                     "opening_model", "forbidden", "platform_taste"]
        for genre_name, preset in MALE_GENRE_PRESETS.items():
            for field in required:
                assert field in preset, f"{genre_name} 缺少字段: {field}"

    def test_female_preset_fields(self):
        """女频每个题材应有必要字段."""
        required = ["name", "target_readers", "chapter_length", "hook_types",
                     "opening_model", "forbidden", "platform_taste"]
        for genre_name, preset in FEMALE_GENRE_PRESETS.items():
            for field in required:
                assert field in preset, f"{genre_name} 缺少字段: {field}"

    def test_get_genre_preset_valid(self):
        """获取有效题材预设."""
        preset = get_genre_preset("玄幻", "male")
        assert preset is not None
        assert preset["name"] == "玄幻"

    def test_get_genre_preset_invalid(self):
        """获取无效题材预设返回 None."""
        preset = get_genre_preset("不存在的题材", "male")
        assert preset is None

    def test_get_genre_preset_female(self):
        """获取女频题材."""
        preset = get_genre_preset("现言", "female")
        assert preset is not None
        assert preset["name"] == "现言"

    def test_list_male_genres(self):
        """列出男频题材."""
        genres = list_genres("male")
        assert "玄幻" in genres
        assert "都市" in genres
        assert len(genres) == 8

    def test_list_female_genres(self):
        """列出女频题材."""
        genres = list_genres("female")
        assert "现言" in genres
        assert "古言" in genres
        assert len(genres) == 8

    def test_get_opening_model(self):
        """获取开局模型."""
        model = get_opening_model("玄幻", "male")
        assert "穿越" in model or "金手指" in model

    def test_get_hook_types(self):
        """获取钩子类型."""
        hooks = get_hook_types("都市", "male")
        assert len(hooks) >= 3

    def test_get_forbidden_content(self):
        """获取禁写内容."""
        forbidden = get_forbidden_content("历史", "male")
        assert len(forbidden) >= 2


class TestGenreTemplateGeneration:
    """题材模板生成测试."""

    def test_generate_single_template(self):
        """生成单个题材模板."""
        result = generate_genre_template("玄幻", "male")
        assert result == 0
        template_path = VAULT_DIR / "Templates" / "男频-玄幻题材模板.md"
        assert template_path.exists()
        content = template_path.read_text(encoding="utf-8")
        assert "玄幻" in content
        assert "目标读者" in content

    def test_generate_female_template(self):
        """生成女频题材模板."""
        result = generate_genre_template("现言", "female")
        assert result == 0
        template_path = VAULT_DIR / "Templates" / "女频-现言题材模板.md"
        assert template_path.exists()

    def test_generate_invalid_genre(self):
        """生成无效题材返回错误."""
        result = generate_genre_template("不存在", "male")
        assert result == 1

    def test_generate_all_templates(self):
        """生成全部 16 个模板."""
        result = generate_all_genre_templates()
        assert result == 0
        # 检查模板数量
        templates = list((VAULT_DIR / "Templates").glob("*题材模板.md"))
        assert len(templates) >= 16
