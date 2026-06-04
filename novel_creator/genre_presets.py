"""题材预设模板 — 男频/女频各8种题材的结构参数."""

from __future__ import annotations

# 男频题材预设
MALE_GENRE_PRESETS: dict[str, dict] = {
    "玄幻": {
        "name": "玄幻",
        "target_readers": "18-35岁男性",
        "chapter_length": (2800, 3800),
        "conflict_density": "高",
        "upgrade_curve": "陡峭",
        "hook_types": ["金手指解锁", "强敌出现", "机缘降临", "逆袭时刻"],
        "opening_model": "穿越/重生→废材/底层→金手指→初露锋芒",
        "forbidden": ["大段内心独白", "过度世界设定解释", "主角长期弱势"],
        "platform_taste": "番茄偏好快节奏+系统流，七猫偏好升级感+打脸爽",
    },
    "都市": {
        "name": "都市",
        "target_readers": "20-40岁男性",
        "chapter_length": (2600, 3600),
        "conflict_density": "中高",
        "upgrade_curve": "递进式",
        "hook_types": ["身份反转", "财富升级", "人脉碾压", "美女环绕"],
        "opening_model": "平凡开局→金手指觉醒→小试牛刀→阶层跃升",
        "forbidden": ["过度涉政", "真实地名/企业名", "违法手段详写"],
        "platform_taste": "番茄偏好神豪/神医流，七猫偏好重生逆袭",
    },
    "脑洞": {
        "name": "脑洞",
        "target_readers": "16-28岁",
        "chapter_length": (2500, 3500),
        "conflict_density": "极高",
        "upgrade_curve": "跳跃式",
        "hook_types": ["设定反转", "脑洞展开", "高概念揭示", "规则打破"],
        "opening_model": "高概念抛出→快速展开→规则建立→第一次脑洞释放",
        "forbidden": ["设定前后矛盾", "脑洞无逻辑支撑", "节奏拖沓"],
        "platform_taste": "番茄偏好短平快高概念，七猫偏好脑洞+感情线",
    },
    "悬疑": {
        "name": "悬疑",
        "target_readers": "22-45岁",
        "chapter_length": (2800, 4000),
        "conflict_density": "中",
        "upgrade_curve": "螺旋式",
        "hook_types": ["线索揭露", "反转", "红鲱鱼", "倒计时压力"],
        "opening_model": "谜面抛出→调查展开→第一层真相→更深谜团",
        "forbidden": ["过早揭示真相", "逻辑硬伤", "线索断层"],
        "platform_taste": "番茄偏好短篇/中篇悬疑，七猫偏好长篇刑侦/推理",
    },
    "历史": {
        "name": "历史",
        "target_readers": "25-50岁男性",
        "chapter_length": (3000, 4000),
        "conflict_density": "中",
        "upgrade_curve": "渐进式",
        "hook_types": ["历史预知", "权谋博弈", "技术碾压", "制度变革"],
        "opening_model": "穿越→身份确认→利用历史知识→第一次小胜",
        "forbidden": ["严重篡改历史定论", "涉敏历史事件", "露骨后宫描写"],
        "platform_taste": "番茄偏好轻松种田流，七猫偏好权谋争霸",
    },
    "科幻": {
        "name": "科幻",
        "target_readers": "18-35岁",
        "chapter_length": (2800, 3800),
        "conflict_density": "中高",
        "upgrade_curve": "科技树驱动",
        "hook_types": ["科技突破", "外星文明", "末日危机", "进化变异"],
        "opening_model": "设定建立→技术/能力获得→第一次应用→更大威胁",
        "forbidden": ["伪科学过多无解释", "科技水平前后矛盾", "抄袭知名IP"],
        "platform_taste": "番茄偏好末世/进化流，七猫偏好星际/机甲",
    },
    "游戏": {
        "name": "游戏",
        "target_readers": "16-30岁",
        "chapter_length": (2500, 3500),
        "conflict_density": "高",
        "upgrade_curve": "等级/装备驱动",
        "hook_types": ["稀有掉落", "BOSS战", "排行榜逆袭", "隐藏职业"],
        "opening_model": "进入游戏→获得优势→第一次亮眼表现→更大目标",
        "forbidden": ["数据堆砌无剧情", "纯游戏攻略式写作", "抄袭知名游戏IP"],
        "platform_taste": "番茄偏好全民游戏/末世游戏，七猫偏好电竞/网游",
    },
    "修仙": {
        "name": "修仙",
        "target_readers": "18-40岁男性",
        "chapter_length": (2800, 4000),
        "conflict_density": "中高",
        "upgrade_curve": "层级分明的阶梯式",
        "hook_types": ["突破境界", "法宝获得", "宗门大比", "秘境探索"],
        "opening_model": "灵根测试→入门修炼→第一次突破→越级挑战",
        "forbidden": ["等级体系混乱", "战力崩坏", "修炼无代价"],
        "platform_taste": "番茄偏好境界突破+打脸，七猫偏好修仙+感情线",
    },
}

# 女频题材预设
FEMALE_GENRE_PRESETS: dict[str, dict] = {
    "现言": {
        "name": "现言",
        "target_readers": "18-35岁女性",
        "chapter_length": (2500, 3500),
        "romance_density": "高",
        "relationship_curve": "慢热递进",
        "hook_types": ["身份反差", "强强对决", "温柔攻陷", "误会反转"],
        "opening_model": "相遇→身份张力→日常互动→感情萌芽",
        "forbidden": ["女主无独立人格", "男主标签化霸总", "感情无递进"],
        "platform_taste": "番茄偏好甜宠+双强，七猫偏好细腻感情线+职场",
    },
    "古言": {
        "name": "古言",
        "target_readers": "20-45岁女性",
        "chapter_length": (2800, 3800),
        "romance_density": "中高",
        "relationship_curve": "循序渐进",
        "hook_types": ["身份揭露", "权谋博弈", "英雄救美", "宅斗反击"],
        "opening_model": "入府/入宫→身份定位→第一次冲突→暗流涌动",
        "forbidden": ["脱离历史背景的现代行为", "女性角色完全被动", "过度宅斗循环"],
        "platform_taste": "番茄偏好重生古言+反击，七猫偏好权谋+感情",
    },
    "重生": {
        "name": "重生",
        "target_readers": "18-40岁女性",
        "chapter_length": (2500, 3600),
        "romance_density": "高",
        "relationship_curve": "重新选择",
        "hook_types": ["前世记忆验证", "渣男/渣女打脸", "真命相遇", "人生翻盘"],
        "opening_model": "死亡→重生→利用前世记忆→第一次改变命运",
        "forbidden": ["复仇过度血腥", "前世今生时间线混乱", "人物关系脸谱化"],
        "platform_taste": "番茄偏好快节奏打脸+甜宠，七猫偏好细腻复仇+感情纠葛",
    },
    "甜宠": {
        "name": "甜宠",
        "target_readers": "16-30岁女性",
        "chapter_length": (2500, 3200),
        "romance_density": "极高",
        "relationship_curve": "快速升温",
        "hook_types": ["高甜互动", "身份反差萌", "独占宣言", "危机守护"],
        "opening_model": "相遇（契约/意外）→亲密接触→甜度升级→关系确认",
        "forbidden": ["虐心过度（不符合甜宠定位）", "男主中央空调", "甜而无剧情推进"],
        "platform_taste": "番茄偏好短篇高甜，七猫偏好长篇甜宠+成长",
    },
    "虐恋": {
        "name": "虐恋",
        "target_readers": "20-40岁女性",
        "chapter_length": (2800, 3800),
        "romance_density": "极高",
        "relationship_curve": "虐→甜→虐→HE",
        "hook_types": ["误会深化", "身份真相", "牺牲守护", "追妻火葬场"],
        "opening_model": "虐的起因→关系恶化→虐点爆发→转机出现→追回",
        "forbidden": ["为虐而虐无逻辑", "伤害行为美化为爱", "结局强行HE不合理"],
        "platform_taste": "番茄偏好短虐+反转，七猫偏好长篇虐恋+最终HE",
    },
    "年代": {
        "name": "年代",
        "target_readers": "25-55岁女性",
        "chapter_length": (2800, 3800),
        "romance_density": "中",
        "relationship_curve": "时代感慢热",
        "hook_types": ["时代机遇", "家庭纠葛", "身份转变", "创业逆袭"],
        "opening_model": "年代背景→家庭状况→第一次机遇→命运转折",
        "forbidden": ["年代细节错误", "人物价值观脱离时代", "过度美化或丑化"],
        "platform_taste": "番茄偏好重生年代+致富，七猫偏好年代情感+家庭",
    },
    "悬疑": {
        "name": "悬疑",
        "target_readers": "18-35岁女性",
        "chapter_length": (2800, 3800),
        "romance_density": "中",
        "relationship_curve": "悬疑中推进感情",
        "hook_types": ["案件反转", "感情揭露", "双线叙事", "真相逼近"],
        "opening_model": "谜面→调查搭档→感情萌芽→案中案",
        "forbidden": ["感情线压倒悬疑线", "逻辑硬伤", "凶手过早暴露"],
        "platform_taste": "番茄偏好悬疑+甜宠，七猫偏好悬疑+感情纠葛",
    },
    "幻想": {
        "name": "幻想",
        "target_readers": "16-28岁女性",
        "chapter_length": (2500, 3600),
        "romance_density": "高",
        "relationship_curve": "奇幻设定下的感情发展",
        "hook_types": ["魔法/异能的浪漫应用", "种族/身份禁忌", "命运羁绊", "奇幻冒险"],
        "opening_model": "奇幻世界建立→能力/身份揭示→第一次相遇→共同冒险",
        "forbidden": ["世界观过于复杂掩盖感情线", "魔法体系前后矛盾", "抄袭知名IP"],
        "platform_taste": "番茄偏好西幻/异世+甜宠，七猫偏好仙侠/奇幻+长篇感情",
    },
}


def get_genre_preset(genre: str, track: str = "male") -> dict | None:
    """获取题材预设.

    Args:
        genre: 题材名称.
        track: male 或 female.

    Returns:
        题材预设字典，不存在时返回 None.
    """
    presets = MALE_GENRE_PRESETS if track == "male" else FEMALE_GENRE_PRESETS
    return presets.get(genre)


def list_genres(track: str = "male") -> list[str]:
    """列出所有题材.

    Args:
        track: male 或 female.

    Returns:
        题材名称列表.
    """
    presets = MALE_GENRE_PRESETS if track == "male" else FEMALE_GENRE_PRESETS
    return list(presets.keys())


def get_opening_model(genre: str, track: str = "male") -> str:
    """获取题材的开局模型."""
    preset = get_genre_preset(genre, track)
    return preset["opening_model"] if preset else "通用开局模型"


def get_hook_types(genre: str, track: str = "male") -> list[str]:
    """获取题材的钩子类型."""
    preset = get_genre_preset(genre, track)
    return preset.get("hook_types", []) if preset else []


def get_forbidden_content(genre: str, track: str = "male") -> list[str]:
    """获取题材的禁写内容."""
    preset = get_genre_preset(genre, track)
    return preset.get("forbidden", []) if preset else []
