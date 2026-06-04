"""编排模块测试."""

from novel_creator.orchestration import (
    DECISION_PRIORITY,
    MINIMUM_AGENT_CHAIN,
    check_contract_compliance,
    create_trace,
    director_resolve,
    format_contract_report,
    list_traces,
    validate_agent_chain,
    validate_orchestration_contract,
)


class TestAgentChainValidation:
    """Agent 链验证测试."""

    def test_complete_chain(self):
        """测试完整 Agent 链通过验证."""
        passed, missing = validate_agent_chain(MINIMUM_AGENT_CHAIN)
        assert passed is True
        assert len(missing) == 0

    def test_incomplete_chain(self):
        """测试不完整 Agent 链被检测."""
        partial = ["Director", "Drafter"]
        passed, missing = validate_agent_chain(partial)
        assert passed is False
        assert len(missing) > 0

    def test_case_insensitive(self):
        """测试大小写不敏感."""
        lower_chain = [a.lower() for a in MINIMUM_AGENT_CHAIN]
        passed, missing = validate_agent_chain(lower_chain)
        assert passed is True

    def test_only_director(self):
        """测试只有 Director 的情况."""
        passed, missing = validate_agent_chain(["Director"])
        assert passed is False
        assert "Drafter" in missing


class TestDirectorResolve:
    """Director 裁决测试."""

    def test_priority_order(self):
        """测试按优先级排序."""
        conflicts = [
            {
                "type": "文风精修",
                "description": "用词选择",
                "options": ["选项A", "选项B"],
            },
            {
                "type": "商业节奏",
                "description": "冲突密度",
                "options": ["选项A"],
            },
            {
                "type": "法律/政治风险",
                "description": "敏感表述",
                "options": ["修改"],
            },
        ]
        decisions = director_resolve(conflicts)
        # 商业节奏应在最前面（最高优先级）
        assert decisions[0]["priority"] == "商业节奏"
        # 文风精修应在最后（最低优先级）
        assert decisions[-1]["priority"] == "文风精修"

    def test_empty_conflicts(self):
        """测试空冲突列表."""
        decisions = director_resolve([])
        assert len(decisions) == 0

    def test_single_conflict(self):
        """测试单个冲突."""
        conflicts = [
            {
                "type": "人物动机",
                "description": "主角行为不一致",
                "options": ["按新动机重写"],
            }
        ]
        decisions = director_resolve(conflicts)
        assert len(decisions) == 1
        assert decisions[0]["decision"] == "按新动机重写"


class TestAgentTrace:
    """Agent Trace 测试."""

    def test_create_trace(self):
        """测试创建 Agent Trace."""
        trace = create_trace("test-project", 1, "测试章节")
        assert trace.project == "test-project"
        assert trace.chapter_no == 1
        assert trace.chapter_title == "测试章节"
        assert len(trace.entries) == 0

    def test_record_agent(self):
        """测试记录 Agent 调用."""
        trace = create_trace("test", 1, "测试")
        trace.record_agent(
            "Director",
            "读取项目记忆和章纲",
            "拆解任务，调度 Agent",
            accepted=True,
        )
        assert len(trace.entries) == 1
        assert trace.entries[0]["agent"] == "Director"
        assert trace.entries[0]["accepted"] is True

    def test_record_rejected_agent(self):
        """测试记录被拒绝的 Agent."""
        trace = create_trace("test", 1, "测试")
        trace.record_agent(
            "Drafter",
            "章纲输入",
            "生成初稿",
            accepted=False,
            rejected_reason="节奏过慢",
        )
        assert trace.entries[0]["accepted"] is False
        assert trace.entries[0]["rejected_reason"] == "节奏过慢"

    def test_record_director_decision(self):
        """测试记录 Director 裁决."""
        trace = create_trace("test", 1, "测试")
        trace.record_director_decision(
            "商业节奏 vs 文风精修",
            "采用商业节奏优先方案",
            "商业节奏",
        )
        assert len(trace.director_decisions) == 1
        assert "商业节奏" in trace.director_decisions[0]["conflict"]

    def test_add_memory_update(self):
        """测试记忆更新."""
        trace = create_trace("test", 1, "测试")
        trace.add_memory_update("character_changes", "主角获得新能力")
        trace.add_memory_update("foreshadowing_new", "第三章伏笔：神秘玉佩")
        assert "主角获得新能力" in trace.memory_updates["character_changes"]
        assert "神秘玉佩" in trace.memory_updates["foreshadowing_new"][0]

    def test_generate_trace(self):
        """测试生成 Trace 文档."""
        trace = create_trace("test-project", 5, "决战")
        trace.record_agent("Director", "读入上下文", "拆解完成", accepted=True)
        trace.record_director_decision("冲突A", "决策A", "商业节奏")
        trace.add_memory_update("character_changes", "主角升级")

        doc = trace.generate()
        assert "# Agent Trace: 第5章 决战" in doc
        assert "test-project" in doc
        assert "Director" in doc
        assert "主角升级" in doc
        assert "冲突A" in doc

    def test_save_trace(self):
        """测试保存 Trace 到文件."""
        trace = create_trace("unittest", 0, "测试保存")
        trace.record_agent("TestAgent", "input", "output", accepted=True)

        filepath = trace.save()
        assert filepath.exists()
        content = filepath.read_text(encoding="utf-8")
        assert "unittest" in content
        assert "TestAgent" in content

        # 清理
        filepath.unlink()


class TestDecisionPriority:
    """裁决优先级测试."""

    def test_priority_order(self):
        """验证正确的优先级顺序."""
        assert DECISION_PRIORITY[0] == "商业节奏"
        assert DECISION_PRIORITY[1] == "法律/政治风险"
        assert DECISION_PRIORITY[2] == "设定一致性"
        assert "去AI味" in DECISION_PRIORITY
        assert DECISION_PRIORITY[-1] == "文风精修"

    def test_minimum_chain_order(self):
        """验证 Agent 链包含关键角色."""
        assert "Director" in MINIMUM_AGENT_CHAIN
        assert "Drafter" in MINIMUM_AGENT_CHAIN
        assert "Commercial Reviewer" in MINIMUM_AGENT_CHAIN
        assert "Continuity Auditor" in MINIMUM_AGENT_CHAIN
        assert "Anti-AI Voice Editor" in MINIMUM_AGENT_CHAIN
        assert "Polisher" in MINIMUM_AGENT_CHAIN
        assert "Obsidian Librarian" in MINIMUM_AGENT_CHAIN


class TestOrchestrationContract:
    """编排合同验证测试."""

    def test_full_chain_compliant(self):
        """完整 Agent 链应该通过合同验证."""
        results = validate_orchestration_contract(
            MINIMUM_AGENT_CHAIN,
            trace_generated=True,
            memory_updated=True,
            user_approved=True,
        )
        assert results["multi_agent"] is True
        assert results["director_required"] is True
        assert results["commercial_review_required"] is True
        assert results["trace_required"] is True

    def test_single_agent_violation(self):
        """单 Agent 应违反多 Agent 条款."""
        results = validate_orchestration_contract(["Director"])
        assert results["multi_agent"] is False

    def test_missing_required_agents(self):
        """缺少必须 Agent 应被检测."""
        results = validate_orchestration_contract(
            ["Director", "Drafter"],  # 缺少 Commercial Reviewer 等
        )
        assert results["commercial_review_required"] is False
        assert results["continuity_audit_required"] is False

    def test_missing_trace(self):
        """缺少 Agent Trace 应被检测."""
        results = validate_orchestration_contract(
            MINIMUM_AGENT_CHAIN,
            trace_generated=False,
        )
        assert results["trace_required"] is False

    def test_missing_memory_update(self):
        """缺少记忆更新应被检测."""
        results = validate_orchestration_contract(
            MINIMUM_AGENT_CHAIN,
            memory_updated=False,
        )
        assert results["memory_update_required"] is False

    def test_check_violations(self):
        """check_contract_compliance 应返回违规列表."""
        results = validate_orchestration_contract(
            ["Director"],  # 明显违规
            trace_generated=False,
            memory_updated=False,
            user_approved=False,
        )
        passed, violations = check_contract_compliance(results)
        assert passed is False
        assert len(violations) > 0
        assert "不得单 Agent 完整生成章节" in violations

    def test_check_all_compliant(self):
        """全合规应返回无违规."""
        results = validate_orchestration_contract(
            MINIMUM_AGENT_CHAIN,
            trace_generated=True,
            memory_updated=True,
            user_approved=True,
        )
        passed, violations = check_contract_compliance(results)
        assert passed is True
        assert len(violations) == 0

    def test_format_contract_report(self):
        """合同报告格式化."""
        results = validate_orchestration_contract(
            MINIMUM_AGENT_CHAIN,
            trace_generated=True,
            memory_updated=True,
            user_approved=True,
        )
        report = format_contract_report(results)
        assert "编排合同验证报告" in report
        assert "全部通过" in report

    def test_format_violation_report(self):
        """违规报告应显示违规项."""
        results = validate_orchestration_contract(
            ["Director"],
            trace_generated=False,
        )
        report = format_contract_report(results)
        assert "违规" in report
        assert "不得单 Agent 完整生成章节" in report


class TestTraceListing:
    """Trace 列出测试."""

    def test_list_traces_empty(self):
        """空 Trace 目录."""
        traces = list_traces()
        # Trace 目录可能存在也可能不存在，测试函数不崩溃即可
        assert isinstance(traces, list)

    def test_list_traces_with_trace(self):
        """有 Trace 时列出."""
        trace = create_trace("unittest-contract", 1, "测试合同")
        trace.record_agent("Director", "input", "output", accepted=True)
        trace.save()

        traces = list_traces("unittest-contract")
        assert len(traces) >= 1
        assert any("unittest-contract" in t.name for t in traces)

        # 清理
        for t in traces:
            t.unlink()
