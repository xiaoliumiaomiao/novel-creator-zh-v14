"""全局配置常量."""

from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Vault 路径
VAULT_DIR = PROJECT_ROOT / "vault"

# Vault 子目录
VAULT_SUBDIRS = [
    "00_Dashboard/Agent_Traces",
    "01_Projects",
    "02_Characters",
    "03_Worldbuilding",
    "04_Plot",
    "05_Chapters",
    "06_Foreshadowing",
    "07_Timeline",
    "References",
    "Templates",
    "Samples",
]

# 数据目录
DATA_DIR = PROJECT_ROOT / "data"
INDEX_DIR = DATA_DIR / "index"
REPORTS_DIR = PROJECT_ROOT / "reports"

# 章节硬规则
CHAPTER_MIN_WORDS = 2500
CHAPTER_MAX_WORDS = 4000
PARAGRAPH_MAX_CHARS = 180
MAX_ENGLISH_RATIO = 0.01

# 质量门槛
QUALITY_THRESHOLD = 85
MAX_AUTO_FIX_ROUNDS = 2

# 章节状态流
CHAPTER_STATES = [
    "planned",
    "drafted",
    "reviewed",
    "deai",
    "polished",
    "approved",
]

# 打回状态
REJECTION_STATES = [
    "rejected",
    "revision-planned",
    "revised",
]

# 风险类型
RISK_TYPES = [
    "法律风险",
    "政治风险",
    "涉黄风险",
    "赌博风险",
    "毒品风险",
    "暴恐风险",
    "教唆犯罪",
    "侵权",
    "诽谤",
    "隐私泄露",
    "极端血腥虐杀快感",
    "网络暴力引导",
]

# 改编模式
DEAI_MODES = ["expression-only", "detail-light", "dramatic-boost"]

# 评分维度
SCORE_DIMENSIONS = [
    "commercial_score",
    "continuity_score",
    "character_motivation_score",
    "deai_score",
    "risk_status",
]

# 男频题材
MALE_GENRES = ["玄幻", "都市", "脑洞", "悬疑", "历史", "科幻", "游戏", "修仙"]

# 女频题材
FEMALE_GENRES = ["现言", "古言", "重生", "甜宠", "虐恋", "年代", "悬疑", "幻想"]
