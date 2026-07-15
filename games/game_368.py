from .base import Game
import random

class ParityRuleGame(Game):

    game_rule_zh = """\
我们来玩一个"隐藏奇偶规则"的推理游戏，规则如下：

游戏设定了一个包含 {n} 个元素的集合，每个元素有唯一的编号（O1 到 O{n}）和一个类型标签（从 t1 到 t{num_types} 中选取）。初始集合的元素类型分配如下：
{assignment_display}

存在一个隐藏的二值判定规则 B，它仅依赖于各类型元素的计数。初始集合满足 B 为真。

你的目标是推断出这个隐藏规则的本质。你可以进行以下操作：

1. 单元素删除询问：询问"如果从初始集合中移除元素 Oi，判定规则 B 是否仍为真？"我会回答"是"或"否"。每次询问后，集合会自动重置为初始状态。

2. 提交规律假设：当你认为已经找到规律时，可以提交你的假设。你需要明确指出哪些类型的集合被标记（即移除这些类型的元素会导致 B 变为假）。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 删除询问（例如询问移除元素 O5）：
<query_remove>O5</query_remove>

- 提交最终答案时，列出所有被标记的类型（用逗号隔开，顺序不限）：
<answer>t1,t3</answer>

如果没有类型被标记（即移除任何元素都不影响 B），则提交：
<answer>none</answer>

注意：你需要尽可能少地询问次数来找出规律。
"""

    game_rule_en = """\
Let's play a "Hidden Parity Rule" deduction game. Here are the rules:

The game has a set containing {n} elements, each with a unique ID (O1 to O{n}) and a type label (chosen from t1 to t{num_types}). The initial type assignment is:
{assignment_display}

There exists a hidden binary judgment rule B that depends only on the count of each type. The initial set satisfies B equals true.

Your goal is to infer the essence of this hidden rule. You can perform the following operations:

1. Single Element Removal Query: Ask "If element Oi is removed from the initial set, will rule B still be true?" I will answer "Yes" or "No". After each query, the set automatically resets to the initial state.

2. Submit Rule Hypothesis: When you believe you have found the pattern, you can submit your hypothesis. You need to explicitly state which types are marked (i.e., removing elements of these types will make B false).

Each query must contain only one tag. Use the following XML format:

- Removal Query (e.g., asking about removing element O5):
<query_remove>O5</query_remove>

- When submitting the final answer, list all marked types (comma-separated, order does not matter):
<answer>t1,t3</answer>

If no types are marked (i.e., removing any element does not affect B), submit:
<answer>none</answer>

Note: You should try to find the pattern with as few queries as possible.
"""

    contextualized_rule_zh_1 = """\
这是交通流量控制中心的一个排查任务。
我们监控的封闭路网系统包含 {n} 辆自动驾驶车辆，每辆车有唯一的识别码（O1 到 O{n}），并且属于特定车型标签（从 t1 到 t{num_types} 中选取）。当前路网的车辆分布如下：
{assignment_display}

目前，路网处于“完美动态平衡”状态（判定规则 B 为真），不会发生拥堵。这得益于某些车型的车辆在调度算法中严格遵循“双向配对”运行（即数量必须是偶数）。

你的目标是推断出哪些车型被算法设置为必须双向配对。你可以进行以下操作：

1. 抽离测试：询问“如果从路网中临时抽离车辆 Oi，路网是否仍能保持动态平衡？”我会回答“是”或“否”。每次测试后，路网会重置为初始平衡状态。

2. 提交规律假设：当你找出规律后，请明确指出哪些车型标签受到“双向配对”限制（即抽离这些车型的任意一辆会导致平衡打破）。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 抽离测试（例如询问抽离车辆 O5）：
<query_remove>O5</query_remove>

- 提交最终答案时，列出所有必须配对的车型（用逗号隔开，顺序不限）：
<answer>t1,t3</answer>

如果没有车型受此限制（即抽离任何车辆都不影响平衡），则提交：
<answer>none</answer>

注意：你需要尽可能少地测试次数来找出规律。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
This is an anomaly detection task in the traffic flow control center.
Our monitored closed road network system contains {n} autonomous vehicles, each with a unique ID (O1 to O{n}) and a specific vehicle type tag (chosen from t1 to t{num_types}). The current vehicle distribution is as follows:
{assignment_display}

Currently, the road network is in a state of "perfect dynamic balance" (judgment rule B is true), meaning no congestion occurs. This is because certain vehicle types strictly follow "bidirectional pairing" in the scheduling algorithm (i.e., their count must be even).

Your goal is to infer which vehicle types are configured by the algorithm to require bidirectional pairing. You can perform the following operations:

1. Removal Test: Ask "If vehicle Oi is temporarily removed from the road network, will the network still maintain its dynamic balance?" I will answer "Yes" or "No". After each test, the network automatically resets to the initial balanced state.

2. Submit Pattern Hypothesis: When you have found the pattern, explicitly state which vehicle type tags are restricted by bidirectional pairing (i.e., removing any single vehicle of these types will break the balance).

Each query must contain only one tag. Use the following XML format:

- Removal Test (e.g., asking about removing vehicle O5):
<query_remove>O5</query_remove>

- When submitting the final answer, list all paired vehicle types (comma-separated, order does not matter):
<answer>t1,t3</answer>

If no vehicle types are restricted (i.e., removing any vehicle does not affect the balance), submit:
<answer>none</answer>

Note: You should minimize the number of tests needed to find the pattern.
"""

    contextualized_rule_zh_2 = """\
欢迎使用临床免疫系统分析沙盒。
当前患者血液样本的微环境中包含 {n} 个关键免疫细胞，每个细胞有独立编号（O1 到 O{n}）以及分化类型标签（从 t1 到 t{num_types} 中选取）。样本中细胞类型分布如下：
{assignment_display}

目前，该微环境处于“免疫稳态”（判定规则 B 为真）。研究表明，某些特定类型的免疫细胞必须以二聚体或配对形式发挥作用（即总数为偶数），才能维持微环境的稳定。

你的目标是鉴定出哪些类型的免疫细胞具有这种配对依赖性。你可以进行以下操作：

1. 细胞敲除模拟：询问“如果从微环境中移除细胞 Oi，样本是否仍能保持免疫稳态？”系统会返回“是”或“否”。每次模拟后，微环境会自动恢复到初始状态。

2. 提交规律假设：当你确定了具有配对依赖性的细胞类型时，请提交你的结论（即移除这些类型中的任意一个细胞会导致稳态破坏）。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 细胞敲除模拟（例如询问移除细胞 O5）：
<query_remove>O5</query_remove>

- 提交最终答案时，列出所有具有配对依赖性的细胞类型（用逗号隔开，顺序不限）：
<answer>t1,t3</answer>

如果没有细胞类型受此限制（即移除任何细胞都不影响稳态），则提交：
<answer>none</answer>

注意：请在尽可能少的模拟次数内找出关键细胞类型。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Clinical Immune System Analysis Sandbox.
The microenvironment of the current patient's blood sample contains {n} key immune cells, each with a unique ID (O1 to O{n}) and a differentiation type tag (chosen from t1 to t{num_types}). The cell type distribution is:
{assignment_display}

Currently, the microenvironment is in "immune homeostasis" (judgment rule B is true). Research shows that certain specific types of immune cells must function in dimers or pairs (i.e., the total number must be even) to maintain this stability.

Your goal is to identify which types of immune cells have this pairing dependency. You can perform the following operations:

1. Knockout Simulation: Ask "If cell Oi is removed from the microenvironment, will the sample still maintain immune homeostasis?" The system will answer "Yes" or "No". After each simulation, the microenvironment automatically restores to its initial state.

2. Submit Pattern Hypothesis: When you have identified the pair-dependent cell types, submit your conclusion (i.e., removing any single cell of these types will disrupt the homeostasis).

Each query must contain only one tag. Use the following XML format:

- Knockout Simulation (e.g., asking about removing cell O5):
<query_remove>O5</query_remove>

- When submitting the final answer, list all pair-dependent cell types (comma-separated, order does not matter):
<answer>t1,t3</answer>

If no cell types are restricted by this dependency, submit:
<answer>none</answer>

Note: Try to find the critical cell types with as few simulations as possible.
"""

    contextualized_rule_zh_3 = """\
这里是教学行为分析系统。
在当前的协同学习活动中，有 {n} 名学生参与，每名学生拥有唯一的学号（O1 到 O{n}）和特定的认知风格标签（从 t1 到 t{num_types} 中选取）。学生类型分布如下：
{assignment_display}

当前学习小组处于“高效协作”状态（判定规则 B 为真）。这是因为某些认知风格的学生在当前课程任务中必须进行“结对编程”或“双人互助”（即人数必须为偶数）。

你的任务是分析出哪些认知风格标签被要求强制结对。你可以进行以下操作：

1. 请假模拟：询问“如果让学生 Oi 临时请假离开，小组是否仍能保持高效协作？”我会回答“是”或“否”。每次模拟后，学生名单会恢复为初始状态。

2. 提交规律假设：当你发现规律后，请提交你的结论，指出哪些认知风格的学生属于强制结对类型（即缺少其中一人会导致协作失败）。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 请假模拟（例如询问学生 O5 请假）：
<query_remove>O5</query_remove>

- 提交最终答案时，列出所有需要强制结对的认知风格（用逗号隔开，顺序不限）：
<answer>t1,t3</answer>

如果没有风格受此限制，则提交：
<answer>none</answer>

注意：你需要通过尽可能少的模拟次数找出规律。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
This is the Teaching Behavior Analysis System.
In the current collaborative learning activity, there are {n} participating students, each with a unique student ID (O1 to O{n}) and a specific cognitive style tag (chosen from t1 to t{num_types}). The student type distribution is:
{assignment_display}

The study group is currently in a state of "high-efficiency collaboration" (judgment rule B is true). This is because students with certain cognitive styles are required to engage in "pair programming" or "dyadic mutual assistance" (i.e., their count must be even) in this task.

Your task is to analyze which cognitive style tags require forced pairing. You can perform the following operations:

1. Absence Simulation: Ask "If student Oi takes a temporary leave, will the group still maintain high-efficiency collaboration?" I will answer "Yes" or "No". After each simulation, the student roster resets to the initial state.

2. Submit Pattern Hypothesis: Once you discover the pattern, submit your conclusion indicating which cognitive styles require forced pairing (i.e., missing one person of these types causes collaboration failure).

Each query must contain only one tag. Use the following XML format:

- Absence Simulation (e.g., asking about student O5 taking leave):
<query_remove>O5</query_remove>

- When submitting the final answer, list all cognitive styles that require forced pairing (comma-separated, order does not matter):
<answer>t1,t3</answer>

If no styles are subject to this restriction, submit:
<answer>none</answer>

Note: You should figure out the pattern using the fewest possible simulations.
"""

    contextualized_rule_zh_4 = """\
进入工业自动化产线的容错测试系统。
当前核心控制主板上装载了 {n} 个电子元器件，每个元器件有唯一的序列号（O1 到 O{n}）以及组件类型标签（从 t1 到 t{num_types} 中选取）。元器件分布如下：
{assignment_display}

目前，主板可以通过“全功率自检”（判定规则 B 为真）。在电路设计中，某些特定类型的元器件采用了“双冗余并联”设计（即该类型的元件总数必须为偶数），以保证电流回路的完整性。

你的目标是逆向推导并找出所有采用双冗余设计的元器件类型。你可以进行以下操作：

1. 熔断测试：询问“如果将元器件 Oi 熔断（移除），主板是否仍能通过全功率自检？”系统会回答“是”或“否”。每次测试后，电路会自动重置为完好状态。

2. 提交规律假设：当你确认了设计规律时，请提交你的结论，指出哪些类型的元器件采用了双冗余设计（即移除其中一个会导致自检失败）。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 熔断测试（例如询问熔断元器件 O5）：
<query_remove>O5</query_remove>

- 提交最终答案时，列出所有采用双冗余设计的类型（用逗号隔开，顺序不限）：
<answer>t1,t3</answer>

如果没有元件采用此设计，则提交：
<answer>none</answer>

注意：请尽量减少破坏性测试的次数来找出设计规律。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Entering the fault-tolerance testing system of the industrial automated production line.
The core control motherboard currently houses {n} electronic components, each with a unique serial number (O1 to O{n}) and a component type tag (chosen from t1 to t{num_types}). The component distribution is:
{assignment_display}

Currently, the motherboard passes the "full-power self-test" (judgment rule B is true). In the circuit design, certain specific types of components employ a "dual-redundant parallel" architecture (i.e., the total count of these components must be even) to ensure the integrity of the current loop.

Your goal is to reverse-engineer and find all component types that use this dual-redundant design. You can perform the following operations:

1. Blowout Test: Ask "If component Oi is blown (removed), will the motherboard still pass the full-power self-test?" The system will answer "Yes" or "No". After each test, the circuit automatically resets to the intact state.

2. Submit Pattern Hypothesis: When you have confirmed the design pattern, submit your conclusion indicating which component types use dual-redundancy (i.e., removing one of them causes the self-test to fail).

Each query must contain only one tag. Use the following XML format:

- Blowout Test (e.g., asking about blowing out component O5):
<query_remove>O5</query_remove>

- When submitting the final answer, list all dual-redundant component types (comma-separated, order does not matter):
<answer>t1,t3</answer>

If no components use this design, submit:
<answer>none</answer>

Note: Please minimize the number of destructive tests to uncover the design pattern.
"""

    contextualized_rule_zh_5 = """\
欢迎进入智能法务逻辑审查系统。
在一份复杂的并购合同中，包含 {n} 条核心条款，每条条款有唯一编号（O1 到 O{n}）和对应的法律性质标签（从 t1 到 t{num_types} 中选取）。条款性质分布如下：
{assignment_display}

当前合同的整体逻辑处于“严密无懈可击”的状态（判定规则 B 为真）。这依赖于某些特定性质的条款在起草时严格遵循了“权利义务对等”原则（即这类条款必须成对出现，数量为偶数）。

你的目标是审查出哪些法律性质的条款受到了对等原则的约束。你可以进行以下操作：

1. 剔除推演：询问“如果从合同中剔除条款 Oi，合同的整体逻辑是否依然严密？”我会回答“是”或“否”。每次推演后，合同文本会自动恢复原状。

2. 提交规律假设：当你找出起草规律后，请明确指出哪些性质的条款被设定为必须成对出现（即剔除其中任意一条会导致合同逻辑破裂）。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 剔除推演（例如询问剔除条款 O5）：
<query_remove>O5</query_remove>

- 提交最终答案时，列出所有必须成对出现的条款性质（用逗号隔开，顺序不限）：
<answer>t1,t3</answer>

如果没有条款性质受此原则约束，则提交：
<answer>none</answer>

注意：你需要通过最少的推演次数来完成法务审查。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the Intelligent Legal Logic Review System.
A complex M&A contract contains {n} core clauses, each with a unique identifier (O1 to O{n}) and a corresponding legal nature tag (chosen from t1 to t{num_types}). The clause nature distribution is as follows:
{assignment_display}

The overall logic of the current contract is "watertight" (judgment rule B is true). This relies on the fact that clauses of certain specific natures strictly follow the principle of "equivalence of rights and obligations" during drafting (i.e., they must appear in pairs, meaning an even count).

Your goal is to review and identify which legal natures of clauses are bound by this equivalence principle. You can perform the following operations:

1. Exclusion Deduction: Ask "If clause Oi is excluded from the contract, does the overall logic remain watertight?" I will answer "Yes" or "No". After each deduction, the contract text automatically restores.

2. Submit Pattern Hypothesis: When you find the drafting pattern, explicitly state which clause natures are set to appear in pairs (i.e., excluding any single clause of these natures causes the legal logic to break).

Each query must contain only one tag. Use the following XML format:

- Exclusion Deduction (e.g., asking about excluding clause O5):
<query_remove>O5</query_remove>

- When submitting the final answer, list all clause natures that must appear in pairs (comma-separated, order does not matter):
<answer>t1,t3</answer>

If no clause natures are bound by this principle, submit:
<answer>none</answer>

Note: You need to complete the legal review with the minimum number of deductions.
"""

    tags = ["answer", "query_remove"]
    
    reasoning_type = "归纳推理"
    data_structure = "集合"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 10,
                "num_types": 3,
                "assignments": "O1:t1,O2:t2,O3:t3,O4:t1,O5:t2,O6:t3,O7:t1,O8:t2,O9:t1,O10:t3",
                "marked_types": ["t1"],
            },
            2: {
                "n": 12,
                "num_types": 4,
                "assignments": "O1:t1,O2:t2,O3:t3,O4:t4,O5:t1,O6:t2,O7:t3,O8:t1,O9:t4,O10:t2,O11:t1,O12:t3",
                "marked_types": ["t1", "t4"],
            },
            3: {
                "n": 14,
                "num_types": 5,
                "assignments": "O1:t1,O2:t2,O3:t3,O4:t4,O5:t1,O6:t5,O7:t2,O8:t3,O9:t1,O10:t4,O11:t2,O12:t4,O13:t1,O14:t5",
                "marked_types": ["t1", "t5"],
            },
            4: {
                "n": 16,
                "num_types": 5,
                "assignments": "O1:t1,O2:t2,O3:t3,O4:t4,O5:t5,O6:t1,O7:t2,O8:t3,O9:t4,O10:t1,O11:t2,O12:t3,O13:t1,O14:t2,O15:t4,O16:t5",
                "marked_types": ["t1", "t2", "t5"],
            },
            5: {
                "n": 18,
                "num_types": 6,
                "assignments": "O1:t1,O2:t2,O3:t3,O4:t4,O5:t5,O6:t6,O7:t1,O8:t2,O9:t3,O10:t5,O11:t1,O12:t2,O13:t4,O14:t5,O15:t1,O16:t3,O17:t5,O18:t6",
                "marked_types": ["t1", "t4", "t5"],
            },
        },
        "en": {
            1: {
                "n": 10,
                "num_types": 3,
                "assignments": "O1:t1,O2:t2,O3:t3,O4:t1,O5:t2,O6:t3,O7:t1,O8:t2,O9:t1,O10:t3",
                "marked_types": ["t1"],
            },
            2: {
                "n": 12,
                "num_types": 4,
                "assignments": "O1:t1,O2:t2,O3:t3,O4:t4,O5:t1,O6:t2,O7:t3,O8:t1,O9:t4,O10:t2,O11:t1,O12:t3",
                "marked_types": ["t1", "t4"],
            },
            3: {
                "n": 14,
                "num_types": 5,
                "assignments": "O1:t1,O2:t2,O3:t3,O4:t4,O5:t1,O6:t5,O7:t2,O8:t3,O9:t1,O10:t4,O11:t2,O12:t4,O13:t1,O14:t5",
                "marked_types": ["t1", "t5"],
            },
            4: {
                "n": 16,
                "num_types": 5,
                "assignments": "O1:t1,O2:t2,O3:t3,O4:t4,O5:t5,O6:t1,O7:t2,O8:t3,O9:t4,O10:t1,O11:t2,O12:t3,O13:t1,O14:t2,O15:t4,O16:t5",
                "marked_types": ["t1", "t2", "t5"],
            },
            5: {
                "n": 18,
                "num_types": 6,
                "assignments": "O1:t1,O2:t2,O3:t3,O4:t4,O5:t5,O6:t6,O7:t1,O8:t2,O9:t3,O10:t5,O11:t1,O12:t2,O13:t4,O14:t5,O15:t1,O16:t3,O17:t5,O18:t6",
                "marked_types": ["t1", "t4", "t5"],
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0
        self.max_queries = 30
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty
        
        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["num_types"] = cfg["num_types"]
        
        self.id_to_type = {}
        for pair in cfg["assignments"].split(","):
            oid, otype = pair.split(":")
            self.id_to_type[oid.strip()] = otype.strip()
        
        assignment_display = ", ".join([f"{k}:{v}" for k, v in self.id_to_type.items()])
        self._game_info["assignment_display"] = assignment_display
        
        self.marked_types = set(cfg["marked_types"])
        
        self.type_counts = {}
        for otype in self.id_to_type.values():
            self.type_counts[otype] = self.type_counts.get(otype, 0) + 1
        
        for marked_type in self.marked_types:
            if self.type_counts.get(marked_type, 0) % 2 != 0:
                raise ValueError(f"Marked type {marked_type} has odd initial count!")

    def _check_b_after_removal(self, element_id):
        if element_id not in self.id_to_type:
            return None
        
        removed_type = self.id_to_type[element_id]
        
        if removed_type in self.marked_types:
            return False
        else:
            return True

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        if raw_ans.lower() == "none":
            return len(self.marked_types) == 0
        
        try:
            submitted_types = set(t.strip() for t in raw_ans.split(",") if t.strip())
        except:
            return False
        
        return submitted_types == self.marked_types

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_invalid_id = "错误：元素编号无效。"
        else:
            yes_res, no_res = "Yes", "No"
            error_invalid_id = "Error: Invalid element ID."

        if "query_remove" in parsed_info:
            if self.query_count >= self.max_queries:
                raise ValueError(
                    f"Maximum query limit reached ({self.max_queries} queries)."
                )
            
            element_id = parsed_info["query_remove"].strip()
            result = self._check_b_after_removal(element_id)
            
            if result is None:
                return error_invalid_id
            
            self.query_count += 1
            return yes_res if result else no_res
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if correct == "是": return "否"
            if correct == "否": return "是"
        else:
            lower_correct = correct.lower()
            if lower_correct == "yes": return "No"
            if lower_correct == "no": return "Yes"
            
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        possible_queries = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        sorted_ids = sorted(self.id_to_type.keys(), key=lambda x: int(x[1:]) if x[1:].isdigit() else x)
        
        for element_id in sorted_ids:
            is_valid = self._check_b_after_removal(element_id)
            
            if is_valid is not None:
                ans_str = yes_res if is_valid else no_res
                
                possible_queries.append({
                    "query": f"<query_remove>{element_id}</query_remove>",
                    "answer": ans_str
                })
                
        return possible_queries