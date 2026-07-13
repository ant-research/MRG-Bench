from .base import Game
import re
import itertools

class TotalOrderGame(Game):

    game_rule_zh = """\
我们来玩一个"隐藏全序推理"游戏，规则如下：

游戏设定了一个包含 {n} 个符号的集合 S={{{symbols}}}。这些符号仅用于区分，它们之间没有任何既定的大小关系。

存在一个在 S 上的隐藏且固定的严格全序关系，但你并不知道。你的目标是通过与我的交互，推断出这个全序关系，并给出按从小到大排列的完整序列。

## 交互方式

你可以进行两种操作：

1. **试探查询**：提交一个长度为 m（2 到 {n} 之间）的序列，序列中的元素来自 S 且两两不同。
   - 我会判断该序列是否满足非降序（即每个元素小于等于下一个元素）。
   - 如果满足，我会回答"是"。
   - 如果不满足，我会回答"否，断点=i"，其中 i 是第一个出现逆序的位置（即第 i 个元素大于第 i+1 个元素）。
   - 如果输入包含重复元素或不在 S 中的元素，我会回答"无效输入"。

2. **最终提交**：提交一个长度为 {n} 的完整序列，包含 S 中所有元素且不重复，表示你猜测的从小到大的排序。
   - 如果与隐藏的全序完全一致，游戏成功。
   - 否则，我会告诉你第一个逆序的位置，游戏失败。

## 约束条件

- 你至少需要进行 4 次试探查询后，才能进行首次最终提交。
- 请尽可能用较少的次数完成推理。

## 格式要求

**试探查询**（例如查询 K1,K3,K2 的顺序）：
<query>K1,K3,K2</query>

**最终提交**（例如提交完整排序）：
<answer>K2,K1,K4,K3,K5,K6</answer>

注意：每次只能包含一个标签（query 或 answer），元素之间用英文逗号分隔，不要有多余空格。
"""

    game_rule_en = """\
Let's play a "Hidden Total Order Inference" game. Here are the rules:

The game defines a set S={{{symbols}}} containing {n} symbols. These symbols are only used for distinction and have no predefined size relationship.

There exists a hidden and fixed strict total order on S, which you don't know. Your goal is to infer this total order through interaction with me and provide the complete sequence sorted from smallest to largest.

## Interaction Methods

You can perform two types of operations:

1. **Probe Query**: Submit a sequence of length m (between 2 and {n}), with elements from S and all distinct.
   - I will judge whether the sequence satisfies non-decreasing order (each element is less than or equal to the next).
   - If satisfied, I will answer "Yes".
   - If not satisfied, I will answer "No, breakpoint=i", where i is the first position where inverse order occurs (the i-th element is greater than the (i+1)-th element).
   - If the input contains duplicate elements or elements not in S, I will answer "Invalid input".

2. **Final Submission**: Submit a complete sequence of length {n}, containing all elements in S without repetition, representing your guessed sorting from smallest to largest.
   - If it completely matches the hidden total order, the game succeeds.
   - Otherwise, I will tell you the first inverse position, and the game fails.

## Constraints

- You need to perform at least 4 probe queries before making your first final submission.
- Please complete the inference with as few attempts as possible.

## Format Requirements

**Probe Query** (e.g., query the order of K1,K3,K2):
<query>K1,K3,K2</query>

**Final Submission** (e.g., submit complete sorting):
<answer>K2,K1,K4,K3,K5,K6</answer>

Note: Each time only one tag (query or answer) can be included, elements are separated by commas without extra spaces.
"""

    # 场景 1：交通
    contextualized_rule_zh_1 = """\
欢迎进入智能交通调度系统。我们要进行一场“路权优先级排查”演练。

系统内包含 {n} 个关键交通节点，代号集合为 S={{{symbols}}}。
这些节点之间存在一个隐藏且严格的“路权优先级”全序关系（从最低优先级到最高优先级排布），你需要通过测试来推断出完整的优先级序列。

## 交互方式

你可以进行两种操作：

1. **试探查询**：提交一个长度为 m（2 到 {n} 之间）的节点序列，序列中的节点必须来自 S 且两两不同。
   - 系统将测试该路径是否满足优先级非降序（即每个节点的优先级小于或等于下一个节点）。
   - 如果测试通过，系统会反馈“是”。
   - 如果发生优先级冲突（即某节点优先级高于下一个节点），系统会反馈“否，断点=i”，其中 i 是第一个出现逆序的节点位置（从 1 开始计数）。
   - 如果输入包含重复节点或不存在的节点，系统会反馈“无效输入”。

2. **最终提交**：提交一个长度为 {n} 的完整路线，包含 S 中所有节点且不重复，代表你推断的从最低到最高优先级的排序。
   - 如果与系统底层的优先级序列完全一致，演练成功。
   - 否则，系统会告诉你第一个发生逆序的位置，演练失败。

## 约束条件

- 在进行首次最终提交前，你至少需要进行 4 次试探查询。
- 请尽可能用较少的查询次数完成调度推断。

## 格式要求

**试探查询**（例如查询 K1,K3,K2 的优先级顺序）：
<query>K1,K3,K2</query>

**最终提交**（例如提交完整的优先级序列）：
<answer>K2,K1,K4,K3,K5,K6</answer>

注意：每次只能包含一个标签（query 或 answer），元素之间用英文逗号分隔，不要有多余空格。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Intelligent Traffic Dispatch System. Let's conduct a "Right-of-Way Priority Inference" drill.

The system contains {n} key traffic nodes, defined by the set S={{{symbols}}}.
There exists a hidden and fixed strict total order of "right-of-way priority" (from lowest to highest) among these nodes. Your objective is to infer this complete priority sequence through testing.

## Interaction Methods

You can perform two types of operations:

1. **Probe Query**: Submit a route sequence of length m (between 2 and {n}), with nodes from S and all distinct.
   - The system will check whether the route satisfies a non-decreasing priority order (each node's priority is less than or equal to the next).
   - If it complies, the system answers "Yes".
   - If a priority conflict occurs (a node has a higher priority than the subsequent one), the system answers "No, breakpoint=i", where i is the first position of the inverse order (1-based index).
   - If the input contains duplicate nodes or nodes not in S, the system answers "Invalid input".

2. **Final Submission**: Submit a complete sequence of length {n}, containing all nodes in S without repetition, representing your inferred sorting from lowest to highest priority.
   - If it perfectly matches the underlying total order, the drill succeeds.
   - Otherwise, the system will notify you of the first inverse position, and the drill fails.

## Constraints

- You must perform at least 4 probe queries before making your first final submission.
- Please complete the priority inference with as few queries as possible.

## Format Requirements

**Probe Query** (e.g., test the priority order of K1,K3,K2):
<query>K1,K3,K2</query>

**Final Submission** (e.g., submit the complete priority sorting):
<answer>K2,K1,K4,K3,K5,K6</answer>

Note: Each time, only one tag (query or answer) is permitted. Elements must be separated by commas with no extra spaces.
"""

    # 场景 2：医疗
    contextualized_rule_zh_2 = """\
欢迎使用临床标准操作流排查系统。我们要进行一次“规范诊疗时序推理”任务。

当前诊疗流程涉及 {n} 项关键医疗操作，代号集合为 S={{{symbols}}}。
这 {n} 项操作在标准临床指南中存在一个隐藏且严格的先后全序关系，你需要通过排查来推断出标准的执行顺序序列。

## 交互方式

你可以进行两种操作：

1. **试探查询**：提交一个长度为 m（2 到 {n} 之间）的操作序列，序列中的操作必须来自 S 且两两不同。
   - 系统将评估该操作序列是否符合临床非降序规范（即每个操作按标准顺序在下一个操作之前或平行）。
   - 如果符合，系统会反馈“是”。
   - 如果违背了顺序要求（即某操作被错误地提前安排），系统会反馈“否，断点=i”，其中 i 是第一个出现倒置的位置。
   - 如果输入包含重复操作或非 S 中的操作，系统会反馈“无效输入”。

2. **最终提交**：提交一个长度为 {n} 的完整诊疗流程，包含 S 中所有操作且不重复，代表你推断出的正确先后排序。
   - 如果与指南全序完全一致，任务成功。
   - 否则，系统会告诉你第一个顺序倒置的位置，任务失败。

## 约束条件

- 在进行首次最终提交前，你至少需要进行 4 次试探查询。
- 请尽可能用较少的次数还原标准操作流。

## 格式要求

**试探查询**（例如查询 K1,K3,K2 的操作顺序）：
<query>K1,K3,K2</query>

**最终提交**（例如提交完整排序）：
<answer>K2,K1,K4,K3,K5,K6</answer>

注意：每次只能包含一个标签（query 或 answer），元素之间用英文逗号分隔，不要有多余空格。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Clinical Standard Operating Procedure (SOP) Validation System. Let's perform a "Normative Diagnostic Sequence Inference" task.

The current diagnostic workflow involves {n} key medical operations, defined by the set S={{{symbols}}}.
According to standard clinical guidelines, there is a hidden strict total order defining their chronological sequence. Your goal is to infer this standard operational sequence through systematic validation.

## Interaction Methods

You can perform two types of operations:

1. **Probe Query**: Submit an operation sequence of length m (between 2 and {n}), with elements from S and all distinct.
   - The system will evaluate whether the sequence complies with standard non-decreasing chronological order (each step precedes or parallels the next).
   - If it complies, the system answers "Yes".
   - If there is a procedural violation (a step is incorrectly advanced), the system answers "No, breakpoint=i", where i is the first position where an inversion occurs.
   - If the input contains duplicate steps or invalid codes, the system answers "Invalid input".

2. **Final Submission**: Submit a complete workflow of length {n}, containing all operations in S without repetition, representing your inferred chronological sorting.
   - If it completely matches the guideline's total order, the task succeeds.
   - Otherwise, the system will pinpoint the first chronological inversion, and the task fails.

## Constraints

- You must conduct at least 4 probe queries prior to your first final submission.
- Please deduce the standard operating flow using the minimum number of attempts.

## Format Requirements

**Probe Query** (e.g., validate the procedural order of K1,K3,K2):
<query>K1,K3,K2</query>

**Final Submission** (e.g., submit the complete SOP sorting):
<answer>K2,K1,K4,K3,K5,K6</answer>

Note: Only one tag (query or answer) may be used per input. Separate elements with commas without extra spaces.
"""

    # 场景 3：教育
    contextualized_rule_zh_3 = """\
欢迎进入智能教务排课系统。我们要完成一项“知识点先修链路推理”任务。

课程知识库中包含 {n} 个核心模块，代号集合为 S={{{symbols}}}。
这些模块之间存在一个隐藏且严格的难度递进与先修全序关系，你需要通过排课试探来推断出从基础到高阶的完整学习序列。

## 交互方式

你可以进行两种操作：

1. **试探查询**：提交一个长度为 m（2 到 {n} 之间）的模块序列，序列中的模块来自 S 且两两不同。
   - 系统会检查该学习路线是否满足非降序（即每个模块的层级不高于其后续模块）。
   - 如果满足，系统会反馈“是”。
   - 如果存在先修逻辑冲突（即某模块难度层级高于后续模块），系统会反馈“否，断点=i”，其中 i 是第一个出现倒置的位置。
   - 如果输入包含重复模块或无效代码，系统会反馈“无效输入”。

2. **最终提交**：提交一个长度为 {n} 的完整教学大纲，包含 S 中所有模块且不重复，代表你推测的从基础到高阶的排序。
   - 如果与隐藏的知识点图谱完全一致，任务成功。
   - 否则，系统会告诉你大纲中第一个先修倒置的位置，任务失败。

## 约束条件

- 你至少需要进行 4 次试探查询后，才能提交最终的教学大纲。
- 请尽可能以最少的试探次数完成先修链路的梳理。

## 格式要求

**试探查询**（例如查询 K1,K3,K2 的先修顺序）：
<query>K1,K3,K2</query>

**最终提交**（例如提交完整教学大纲）：
<answer>K2,K1,K4,K3,K5,K6</answer>

注意：每次只能包含一个标签（query 或 answer），元素之间用英文逗号分隔，不要有多余空格。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Intelligent Academic Scheduling System. Let's complete an "Academic Prerequisite Link Inference" task.

The course knowledge base contains {n} core modules, denoted by the set S={{{symbols}}}.
There is a hidden, strict total order governing their prerequisite sequence (from foundational to advanced). Your objective is to infer the complete learning sequence through scheduling trials.

## Interaction Methods

You can perform two types of operations:

1. **Probe Query**: Submit a module sequence of length m (between 2 and {n}), chosen from S with no duplicates.
   - The system verifies if the learning path satisfies a non-decreasing order (no module has a higher prerequisite level than its successor).
   - If valid, the system answers "Yes".
   - If a prerequisite conflict exists (an advanced module precedes a foundational one incorrectly), the system answers "No, breakpoint=i", where i is the first position of inversion.
   - If the input contains duplicate or invalid modules, the system answers "Invalid input".

2. **Final Submission**: Submit the complete curriculum of length {n}, containing all modules in S without repetition, representing your inferred sorting from foundational to advanced.
   - If it perfectly matches the hidden knowledge graph, the task succeeds.
   - Otherwise, the system identifies the first position of inversion, and the task fails.

## Constraints

- You must perform at least 4 probe queries before submitting your final curriculum.
- Please map out the prerequisite link using the minimum number of attempts.

## Format Requirements

**Probe Query** (e.g., query the prerequisite order of K1,K3,K2):
<query>K1,K3,K2</query>

**Final Submission** (e.g., submit the complete curriculum):
<answer>K2,K1,K4,K3,K5,K6</answer>

Note: Each input must contain only one tag (query or answer), with elements separated by commas and no extra spaces.
"""

    # 场景 4：工业/制造业
    contextualized_rule_zh_4 = """\
欢迎使用智能柔性制造控制系统。我们要进行“工艺装配顺位推理”测试。

当前流水线分配了 {n} 个生产环节，代号集合为 S={{{symbols}}}。
这些环节在工艺标准中存在一个隐藏且严格的装配全序关系，你需要通过工艺测试来推断出这套正确的加工流水线排序。

## 交互方式

你可以进行两种操作：

1. **试探查询**：提交一个长度为 m（2 到 {n} 之间）的工序序列，序列中的环节来自 S 且两两不同。
   - 系统将验证该工序是否满足工艺非降序（即前道工序不会落后于后道工序）。
   - 如果满足，系统会反馈“是”。
   - 如果发生工序冲突（即前序步骤被安排在了不该有的高级阶段），系统会反馈“否，断点=i”，其中 i 是第一个出现逆向装配的位置。
   - 如果输入包含重复环节或不属于 S 的环节，系统会反馈“无效输入”。

2. **最终提交**：提交一个长度为 {n} 的完整工艺流水线，包含 S 中所有环节且不重复，代表你推断的从头到尾的加工排序。
   - 如果与隐藏的工艺全序完全一致，测试成功。
   - 否则，系统会告诉你第一个发生工序逆反的位置，测试失败。

## 约束条件

- 在进行首次最终提交前，你至少需要进行 4 次试探查询。
- 请尽可能用最少的测试次数复原整条工艺流水线。

## 格式要求

**试探查询**（例如测试 K1,K3,K2 的组装顺序）：
<query>K1,K3,K2</query>

**最终提交**（例如提交完整流水线）：
<answer>K2,K1,K4,K3,K5,K6</answer>

注意：每次只能包含一个标签（query 或 answer），元素之间用英文逗号分隔，不要有多余空格。
"""

    contextualized_rule_en_4 = """\
[Industry Scenario]
Welcome to the Intelligent Flexible Manufacturing Control System. Let's conduct a "Process Assembly Sequence Inference" test.

The current assembly line involves {n} production stages, denoted by the set S={{{symbols}}}.
According to manufacturing standards, these stages follow a hidden, strict total order of assembly. Your task is to infer this exact processing sequence through procedural testing.

## Interaction Methods

You can perform two types of operations:

1. **Probe Query**: Submit a process sequence of length m (between 2 and {n}), consisting of distinct stages from S.
   - The system checks if the sequence satisfies a non-decreasing process order (no preceding step is delayed behind a subsequent one).
   - If it complies, the system answers "Yes".
   - If an assembly conflict occurs (a preceding step is wrongly placed in a later phase), the system answers "No, breakpoint=i", indicating the first position of reverse assembly.
   - If the input contains duplicate or invalid stages, the system answers "Invalid input".

2. **Final Submission**: Submit the complete assembly line of length {n}, containing all stages in S without repetition, representing your inferred start-to-finish processing sequence.
   - If it exactly matches the hidden total order, the test succeeds.
   - Otherwise, the system reports the first instance of process inversion, and the test fails.

## Constraints

- You must complete at least 4 probe queries before making your first final submission.
- Please reconstruct the entire assembly line with the fewest possible tests.

## Format Requirements

**Probe Query** (e.g., test the assembly sequence of K1,K3,K2):
<query>K1,K3,K2</query>

**Final Submission** (e.g., submit the complete assembly line):
<answer>K2,K1,K4,K3,K5,K6</answer>

Note: Use only one tag (query or answer) per submission. Separate stages with commas without extra spaces.
"""

    # 场景 5：法律
    contextualized_rule_zh_5 = """\
欢迎进入司法程序辅助审查系统。我们要进行一次“证据链采信顺位推理”演练。

本案卷宗涉及 {n} 个核心证据节点，代号集合为 S={{{symbols}}}。
根据法定审查程序，这些节点存在一个隐藏且严格的采信全序关系，你需要通过程序推演，梳理出合法的审查顺位。

## 交互方式

你可以进行两种操作：

1. **试探查询**：提交一个长度为 m（2 到 {n} 之间）的审查序列，序列中的节点来自 S 且两两不同。
   - 系统将核实该程序是否符合法定顺位非降序（即前置程序的优先级应当低于或等于后置程序）。
   - 如果符合，系统会反馈“是”。
   - 如果发生程序倒置（即高顺位节点被非法前置），系统会反馈“否，断点=i”，其中 i 是第一个程序逆序的节点位置。
   - 如果输入包含重复节点或非本案卷宗的节点，系统会反馈“无效输入”。

2. **最终提交**：提交一个长度为 {n} 的完整审查链条，包含 S 中所有节点且不重复，代表你推断出的法定审查全序。
   - 如果与法定的采信全序完全一致，推演成功。
   - 否则，系统会指出首个程序倒置的节点位置，推演失败。

## 约束条件

- 在进行首次最终证据链提交前，你至少需要进行 4 次试探查询。
- 请在确保程序合法的前提下，以尽可能少的次数完成顺位推理。

## 格式要求

**试探查询**（例如推演 K1,K3,K2 的审查顺序）：
<query>K1,K3,K2</query>

**最终提交**（例如提交完整的证据链审查排序）：
<answer>K2,K1,K4,K3,K5,K6</answer>

注意：每次只能包含一个标签（query 或 answer），元素之间用英文逗号分隔，不要有多余空格。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Judicial Procedural Auxiliary Review System. Let's perform a "Chain of Evidence Admissibility Inference" drill.

This case file involves {n} core evidentiary nodes, represented by the set S={{{symbols}}}.
Under statutory procedures, these nodes possess a hidden, strict total order of admissibility priority. You must deduce the lawful review sequence through procedural deduction.

## Interaction Methods

You can perform two types of operations:

1. **Probe Query**: Submit a review sequence of length m (between 2 and {n}), comprising distinct nodes from S.
   - The system verifies if the procedure adheres to a non-decreasing statutory priority (preceding procedures have a priority lower than or equal to subsequent ones).
   - If lawful, the system answers "Yes".
   - If procedural inversion occurs (a high-priority node is illegally prioritized earlier), the system answers "No, breakpoint=i", pointing to the first invalid position.
   - If the input contains duplicate or non-case-related nodes, the system answers "Invalid input".

2. **Final Submission**: Submit a complete review chain of length {n}, containing all nodes in S without repetition, representing your deduced statutory total order.
   - If it perfectly aligns with the statutory admissibility order, the deduction succeeds.
   - Otherwise, the system points out the first position of procedural inversion, and the drill fails.

## Constraints

- You must conduct at least 4 probe queries before your first final chain submission.
- Please complete the priority inference with the fewest attempts while ensuring procedural legality.

## Format Requirements

**Probe Query** (e.g., deduce the review order of K1,K3,K2):
<query>K1,K3,K2</query>

**Final Submission** (e.g., submit the complete sequence of evidence review):
<answer>K2,K1,K4,K3,K5,K6</answer>

Note: Only one tag (query or answer) is permitted at a time. Elements should be comma-separated with no extraneous spaces.
"""

    tags = ["query", "answer"]
    reasoning_type = "归纳推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "symbols": "A,B,C,D",
                "hidden_order": ["C", "A", "D", "B"],
            },
            2: {
                "n": 5,
                "symbols": "A,B,C,D,E",
                "hidden_order": ["E", "C", "A", "B", "D"],
            },
            3: {
                "n": 6,
                "symbols": "A,B,C,D,E,F",
                "hidden_order": ["B", "F", "D", "A", "C", "E"],
            },
            4: {
                "n": 7,
                "symbols": "A,B,C,D,E,F,G",
                "hidden_order": ["E", "C", "A", "G", "F", "B", "D"],
            },
            5: {
                "n": 8,
                "symbols": "A,B,C,D,E,F,G,H",
                "hidden_order": ["D", "H", "F", "A", "C", "G", "E", "B"],
            },
        },
        "en": {
            1: {
                "n": 4,
                "symbols": "A,B,C,D",
                "hidden_order": ["C", "A", "D", "B"],
            },
            2: {
                "n": 5,
                "symbols": "A,B,C,D,E",
                "hidden_order": ["E", "C", "A", "B", "D"],
            },
            3: {
                "n": 6,
                "symbols": "A,B,C,D,E,F",
                "hidden_order": ["B", "F", "D", "A", "C", "E"],
            },
            4: {
                "n": 7,
                "symbols": "A,B,C,D,E,F,G",
                "hidden_order": ["E", "C", "A", "G", "F", "B", "D"],
            },
            5: {
                "n": 8,
                "symbols": "A,B,C,D,E,F,G,H",
                "hidden_order": ["D", "H", "F", "A", "C", "G", "E", "B"],
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0  # 试探查询次数
        self.answer_count = 0  # 最终提交次数
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏配置"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保 difficulty 为整数

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["symbols"] = cfg["symbols"]
        
        self.symbols = set(s.strip() for s in cfg["symbols"].split(","))
        self.hidden_order = cfg["hidden_order"]
        self.order_index = {sym: idx for idx, sym in enumerate(self.hidden_order)}

    def _validate_sequence(self, seq_str):
        """
        验证序列格式并返回符号列表
        返回：(is_valid, symbols_list, error_message)
        """
        if not seq_str:
            return False, [], "Empty sequence"
        
        symbols = [s.strip() for s in seq_str.split(",")]
        
        # 检查是否有空元素
        if any(not s for s in symbols):
            return False, [], "Empty element in sequence"
        
        # 检查是否所有元素都在符号集合中
        for sym in symbols:
            if sym not in self.symbols:
                return False, [], f"Invalid symbol: {sym}"
        
        # 检查是否有重复元素
        if len(symbols) != len(set(symbols)):
            return False, [], "Duplicate elements"
        
        return True, symbols, ""

    def _check_order(self, symbols_list):
        """
        检查序列是否满足非降序
        返回：(is_ordered, breakpoint_pos)
        breakpoint_pos: 如果有序则为-1，否则为第一个逆序位置（从1开始计数）
        """
        for i in range(len(symbols_list) - 1):
            curr_sym = symbols_list[i]
            next_sym = symbols_list[i + 1]
            
            # 比较当前元素和下一个元素在隐藏全序中的位置
            if self.order_index[curr_sym] > self.order_index[next_sym]:
                return False, i + 1  # 返回1-based索引
        
        return True, -1

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        is_valid, symbols_list, error_msg = self._validate_sequence(raw_ans)
        
        if not is_valid:
            return False
        
        # 检查是否包含所有符号
        if len(symbols_list) != self._game_info["n"]:
            return False
        
        if set(symbols_list) != self.symbols:
            return False
        
        # 检查是否与隐藏的全序完全一致
        return symbols_list == self.hidden_order

    def _cf_core_produce(self, parsed_info):
        """处理试探查询 - 核心逻辑"""
        if "query" not in parsed_info:
            raise ValueError("Invalid query format")
        
        raw_query = parsed_info["query"]
        is_valid, symbols_list, error_msg = self._validate_sequence(raw_query)
        
        # 格式验证
        if not is_valid:
            if self.config.language == "zh":
                return "无效输入"
            else:
                return "Invalid input"
        
        # 长度验证
        if len(symbols_list) < 2 or len(symbols_list) > self._game_info["n"]:
            if self.config.language == "zh":
                return "无效输入"
            else:
                return "Invalid input"
        
        # 记录查询次数
        self.query_count += 1
        
        # 检查顺序
        is_ordered, breakpoint_pos = self._check_order(symbols_list)
        
        if is_ordered:
            return "是" if self.config.language == "zh" else "Yes"
        else:
            if self.config.language == "zh":
                return f"否，断点={breakpoint_pos}"
            else:
                return f"No, breakpoint={breakpoint_pos}"

    def _cf_make_wrong(self, correct: str) -> str:
        """生成一个与正确答案相反的错误回复"""
        if self.config.language == "zh":
            if correct == "是":
                # 正确是有序的，错误改为无序，给一个假断点
                return "否，断点=1"
            if correct.startswith("否"):
                # 正确是无序的，错误改为有序
                return "是"
            if correct == "无效输入":
                return "是"
        else:  # en
            if correct == "Yes":
                return "No, breakpoint=1"
            if correct.startswith("No"):
                return "Yes"
            if correct == "Invalid input":
                return "Yes"
        
        # 不应到达此处，但作为安全回退
        return "Yes" if self.config.language == "en" else "是"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有长度为2的合法查询并返回对应的正确答案。
        仅使用长度2的对（即比较对），足以确定全序且数量可控。
        """
        queries = []
        if not hasattr(self, "symbols") or not self.symbols:
            return []

        symbols_list = sorted(list(self.symbols))
        
        # 仅枚举长度为2的排列，共 P(n,2) = n*(n-1) 个
        for perm in itertools.permutations(symbols_list, 2):
            query_str = ",".join(perm)
            
            seq_list = list(perm)
            is_ordered, breakpoint_pos = self._check_order(seq_list)
            
            if is_ordered:
                ans = "是" if self.config.language == "zh" else "Yes"
            else:
                if self.config.language == "zh":
                    ans = f"否，断点={breakpoint_pos}"
                else:
                    ans = f"No, breakpoint={breakpoint_pos}"
            
            queries.append({
                "query": f"<query>{query_str}</query>",
                "answer": ans
            })
        
        return queries

    def step(self, response: str):
        """处理一轮交互"""
        try:
            parsed_info = self.parse(response)
            
            if "answer" in parsed_info:
                # 检查是否满足最少查询次数要求
                if self.query_count < 4:
                    if self.config.language == "zh":
                        res = f"错误：至少需要进行 4 次试探查询后才能提交最终答案。当前查询次数：{self.query_count}"
                    else:
                        res = f"Error: At least 4 probe queries are required before final submission. Current queries: {self.query_count}"
                    self.state.add_message("user", res)
                else:
                    self.answer_count += 1
                    is_success = self.evaluate(parsed_info)
                    
                    if is_success:
                        res = "答案正确" if self.config.language == "zh" else "Correct answer."
                        self.state.set_state("success", "success")
                        self.state.add_message("user", res)
                    else:
                        raw_ans = parsed_info["answer"]
                        is_valid, symbols_list, _ = self._validate_sequence(raw_ans)
                        
                        if is_valid and len(symbols_list) == self._game_info["n"] and set(symbols_list) == self.symbols:
                            _, breakpoint_pos = self._check_order(symbols_list)
                            if self.config.language == "zh":
                                res = f"答案错误，断点={breakpoint_pos}"
                            else:
                                res = f"Incorrect answer, breakpoint={breakpoint_pos}"
                        else:
                            res = "答案格式错误或元素不完整" if self.config.language == "zh" else "Invalid answer format or incomplete elements"
                        
                        self.state.set_state("failed", "incorrect answer")
                        self.state.add_message("user", res)
                        
            elif "query" in parsed_info:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
            else:
                raise ValueError("No valid tag found")
                
        except Exception as e:
            self.state.set_state("failed", str(e))
        
        return self.state