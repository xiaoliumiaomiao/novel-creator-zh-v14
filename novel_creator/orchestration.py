"""多 Agent 编排 — 导演调度、Agent Trace 生成、记忆更新."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from rich.console import Console

from novel_creator.config import VAULT_DIR

console = Console()

# 章节创作最小 Agent 链
MINIMUM_AGENT_CHAIN = [
    "Director",
    "Chapter Planner",
    "Character Agent",
    "Drafter",
    "Commercial Reviewer",
    "Continuity Auditor",
    "Anti-AI Voice Editor",
    "Polisher",
    "Obsidian Librarian",
]

# Director 裁决优先级
DECISION_PRIORITY = [
    "商业节奏",
    "法律/政治风险",
    "设定一致性",
    "人物动机",
    "去AI味",
    "文风精修",
]


class AgentTrace:
    """Agent Trace 记录器."""

    def __init__(self, project: str, chapter_no: int, chapter_title: str):
        self.project = project
        self.chapter_no = chapter_no
        self.chapter_title = chapter_title
        self.start_time = datetime.now().isoformat()
        self.entries: list[dict[str, Any]] = []
        self.director_decisions: list[dict[str, Any]] = []
        self.memory_updates: dict[str, list[str]] = {
            "character_changes": [],
            "relationship_changes": [],
            "foreshadowing_new": [],
            "foreshadowing_resolved": [],
            "timeline_events": [],
            "worldbuilding_new": [],
            "worldbuilding_changes": [],
            "pending_user_confirmation": [],
        }

    def record_agent(
        self,
        agent_name: str,
        input_summary: str,
        output_summary: str,
        accepted: bool = True,
        rejected_reason: str | None = None,
    ) -> None:
        """记录一次 Agent 调用."""
        self.entries.append({
            "agent": agent_name,
            "timestamp": datetime.now().isoformat(),
            "input_summary": input_summary,
            "output_summary": output_summary,
            "accepted": accepted,
            "rejected_reason": rejected_reason,
        })

    def record_director_decision(
        self, conflict: str, decision: str, priority: str
    ) -> None:
        """记录 Director 裁决."""
        self.director_decisions.append({
            "conflict": conflict,
            "decision": decision,
            "priority": priority,
            "timestamp": datetime.now().isoformat(),
        })

    def add_memory_update(self, category: str, item: str) -> None:
        """添加待确认记忆更新."""
        if category in self.memory_updates:
            self.memory_updates[category].append(item)

    def generate(self) -> str:
        """生成 Agent Trace 文档."""
        end_time = datetime.now().isoformat()

        trace = f"""---
type: agent-trace
project: {self.project}
chapter_no: {self.chapter_no}
chapter_title: {self.chapter_title}
start_time: {self.start_time}
end_time: {end_time}
agent_count: {len(self.entries)}
---

# Agent Trace: 第{self.chapter_no}章 {self.chapter_title}

## 基本信息

- 项目：{self.project}
- 章节：第{self.chapter_no}章
- 调用时间：{self.start_time} — {end_time}
- 调用 Agent 数：{len(self.entries)}

## Agent 调用记录

"""
        for i, entry in enumerate(self.entries, 1):
            status = "✓ 采纳" if entry["accepted"] else "✗ 拒绝"
            trace += f"""### {i}. {entry['agent']}

- 时间：{entry['timestamp']}
- 状态：{status}
- 输入摘要：{entry['input_summary']}
- 输出摘要：{entry['output_summary']}
"""
            if entry["rejected_reason"]:
                trace += f"- 拒绝原因：{entry['rejected_reason']}\n"

        if self.director_decisions:
            trace += "\n## Director 裁决记录\n\n"
            for i, decision in enumerate(self.director_decisions, 1):
                trace += f"""### 裁决 {i}

- 冲突：{decision['conflict']}
- 裁决：{decision['decision']}
- 优先级依据：{decision['priority']}
- 时间：{decision['timestamp']}

"""

        trace += "\n## 待确认记忆更新\n\n"
        for category, items in self.memory_updates.items():
            if items:
                label = {
                    "character_changes": "人物变化",
                    "relationship_changes": "关系变化",
                    "foreshadowing_new": "伏笔新增",
                    "foreshadowing_resolved": "伏笔回收",
                    "timeline_events": "时间线事件",
                    "worldbuilding_new": "设定新增",
                    "worldbuilding_changes": "设定变更",
                    "pending_user_confirmation": "待用户确认问题",
                }.get(category, category)
                trace += f"### {label}\n\n"
                for item in items:
                    trace += f"- [ ] {item}\n"
                trace += "\n"

        trace += f"\n---\n*Agent Trace 自动生成于 {end_time}*"

        return trace

    def save(self) -> Path:
        """保存 Agent Trace 到 vault."""
        trace_dir = VAULT_DIR / "00_Dashboard" / "Agent_Traces"
        trace_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{self.project}-ch{self.chapter_no:03d}-trace.md"
        filepath = trace_dir / filename
        filepath.write_text(self.generate(), encoding="utf-8")

        return filepath


def validate_agent_chain(agents_called: list[str]) -> tuple[bool, list[str]]:
    """验证是否满足最小 Agent 链要求.

    Args:
        agents_called: 已调用的 Agent 列表.

    Returns:
        (是否通过, 缺失的 Agent 列表).
    """
    called_set = {a.lower() for a in agents_called}
    missing = []

    for required in MINIMUM_AGENT_CHAIN:
        if required.lower() not in called_set:
            missing.append(required)

    return len(missing) == 0, missing


def director_resolve(
    conflicts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Director 冲突裁决（自动化裁决引擎）.

    按优先级排序：
    商业节奏 > 法律/政治风险 > 设定一致性 > 人物动机 > 去AI味 > 文风精修

    Args:
        conflicts: 冲突列表，每项包含 type, description, options.

    Returns:
        裁决结果列表.
    """
    priority_map = {p: i for i, p in enumerate(DECISION_PRIORITY)}

    decisions = []
    for conflict in conflicts:
        conflict_type = conflict.get("type", "")
        options = conflict.get("options", [])

        # 按优先级选择
        selected = options[0] if options else "无可用选项"
        priority_score = priority_map.get(conflict_type, 99)

        decisions.append({
            "conflict": conflict.get("description", ""),
            "decision": selected,
            "priority": conflict_type,
            "priority_score": priority_score,
            "reason": f"按 Director 裁决优先级：{conflict_type}（优先级{priority_score}）",
        })

    # 按优先级排序
    decisions.sort(key=lambda d: d["priority_score"])

    return decisions


def create_trace(project: str, chapter_no: int, chapter_title: str) -> AgentTrace:
    """创建新的 Agent Trace 实例."""
    return AgentTrace(project, chapter_no, chapter_title)


# ---- 编排合同验证 ----

# 不可违反的合同条款
CONTRACT_TERMS = {
    "multi_agent": "不得单 Agent 完整生成章节",
    "director_required": "不得跳过 Director",
    "commercial_review_required": "不得跳过 Commercial Reviewer",
    "continuity_audit_required": "不得跳过 Continuity Auditor",
    "deai_required": "不得跳过 Anti-AI Voice Editor",
    "librarian_required": "不得跳过 Obsidian Librarian",
    "trace_required": "不得跳过 Agent Trace",
    "memory_update_required": "必须完成记忆更新",
    "user_approval_required": "进入 approved 前必须用户确认",
}


def validate_orchestration_contract(
    agents_called: list[str],
    trace_generated: bool = False,
    memory_updated: bool = False,
    user_approved: bool = False,
) -> dict[str, bool]:
    """验证编排合同遵守情况.

    Args:
        agents_called: 被调用的 Agent 名称列表.
        trace_generated: Agent Trace 是否已生成.
        memory_updated: 记忆是否已更新.
        user_approved: 用户是否已确认.

    Returns:
        合同条款遵守情况字典，{条款: 是否通过}.
    """
    called_lower = {a.lower() for a in agents_called}
    results: dict[str, bool] = {}

    # 多 Agent 检查
    results["multi_agent"] = len(agents_called) >= 3

    # 必须 Agent 检查
    results["director_required"] = any(
        "director" in a for a in called_lower
    )
    results["commercial_review_required"] = any(
        "commercial" in a and "review" in a for a in called_lower
    )
    results["continuity_audit_required"] = any(
        "continuity" in a for a in called_lower
    )
    results["deai_required"] = any(
        "deai" in a or "anti-ai" in a for a in called_lower
    )
    results["librarian_required"] = any(
        "librarian" in a for a in called_lower
    )

    # Trace 和记忆更新
    results["trace_required"] = trace_generated
    results["memory_update_required"] = memory_updated
    results["user_approval_required"] = user_approved

    return results


def check_contract_compliance(
    contract_results: dict[str, bool],
) -> tuple[bool, list[str]]:
    """检查合同合规状态.

    Args:
        contract_results: validate_orchestration_contract 的返回值.

    Returns:
        (全部通过, 违规条款列表).
    """
    violations = []
    for term, passed in contract_results.items():
        if not passed:
            violations.append(CONTRACT_TERMS.get(term, term))
    return len(violations) == 0, violations


def list_traces(project: str | None = None) -> list[Path]:
    """列出所有 Agent Trace.

    Args:
        project: 可选，过滤项目名.

    Returns:
        Trace 文件路径列表（按时间倒序）.
    """
    trace_dir = VAULT_DIR / "00_Dashboard" / "Agent_Traces"
    if not trace_dir.exists():
        return []

    traces = sorted(trace_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)

    if project:
        traces = [t for t in traces if project in t.name]

    return traces


def format_contract_report(contract_results: dict[str, bool]) -> str:
    """格式化合同验证报告.

    Args:
        contract_results: validate_orchestration_contract 的返回值.

    Returns:
        格式化的报告文本.
    """
    lines = ["## 编排合同验证报告", ""]
    all_pass = True

    for term, passed in contract_results.items():
        label = CONTRACT_TERMS.get(term, term)
        status = "✓ 通过" if passed else "✗ 违规"
        lines.append(f"- [{status}] {label}")
        if not passed:
            all_pass = False

    lines.append("")
    if all_pass:
        lines.append("**结果: 全部通过**")
    else:
        lines.append("**结果: 存在违规项，章节不得进入 approved 状态**")

    return "\n".join(lines)
