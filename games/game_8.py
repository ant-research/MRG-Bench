from .base import Game
import random

class TotalOrderDiscoveryGame(Game):

    game_rule_zh = """\
我们来玩一个"全序推断"的游戏，规则如下：

游戏设定了一个包含 {n} 个元素的集合，编号为 1 到 {n}。这些元素存在一个未知的严格全序关系（每个元素都有唯一的排名，没有并列）。

你的目标是通过有限次数的比较查询，推断出集合中的最小元素或最大元素。

你可以进行以下两类操作：

1. **比较查询**：询问两个不同元素 a 和 b 的先后关系。我会告诉你哪个元素在全序中更靠前（排名更小）。每次查询会消耗一次查询次数。

2. **终止宣告**（可选其一，不消耗查询次数）：
   - 宣告最小元素：宣告某个元素是全序中排名第一的元素。
   - 宣告最大元素：宣告某个元素是全序中排名最后的元素。

**约束条件**：
- 比较查询的总次数不能超过 {max_queries} 次。
- 必须在查询次数用尽前做出正确的终止宣告才算成功。
- 如果宣告错误或查询次数超限后未宣告，游戏失败。

每次只能进行一个操作，使用以下 XML 格式：

- 比较查询（例如比较元素 3 和 5）：
<query_compare>3,5</query_compare>

- 宣告最小元素（例如宣告元素 2 是最小元素）：
<answer>type=min, element=2</answer>

- 宣告最大元素（例如宣告元素 7 是最大元素）：
<answer>type=max, element=7</answer>

注意：终止宣告会立即结束游戏并判定成败。
"""

    game_rule_en = """\
Let's play a "Total Order Discovery" game. Here are the rules:

The game is set on a collection of {n} elements, numbered from 1 to {n}. These elements have an unknown strict total order (each element has a unique rank with no ties).

Your goal is to infer either the minimum element or the maximum element in this total order, using a limited number of comparison queries.

You can perform the following two types of operations:

1. **Comparison Query**: Ask about the relative order of two different elements a and b. I will tell you which element comes earlier (has a smaller rank) in the total order. Each query consumes one query count.

2. **Termination Declaration** (choose one, does not consume query count):
   - Declare Minimum: Declare that a specific element is ranked first in the total order.
   - Declare Maximum: Declare that a specific element is ranked last in the total order.

**Constraints**:
- The total number of comparison queries cannot exceed {max_queries}.
- You must make a correct termination declaration before running out of queries to succeed.
- If the declaration is wrong or you exceed the query limit without declaring, the game fails.

Each turn allows only one operation. Use the following XML format:

- Comparison Query (e.g., comparing elements 3 and 5):
<query_compare>3,5</query_compare>

- Declare Minimum (e.g., declaring element 2 as the minimum):
<answer>type=min, element=2</answer>

- Declare Maximum (e.g., declaring element 7 as the maximum):
<answer>type=max, element=7</answer>

Note: A termination declaration immediately ends the game and determines success or failure.
"""

    contextualized_rule_zh_1 = """\
欢迎使用城市交通路口拥堵度评估系统。

系统监控了 {n} 个关键交通路口，编号为 1 到 {n}。这些路口当前的拥堵程度存在一个未知的严格全序关系（每个路口都有唯一的拥堵排名，没有并列）。

你的目标是通过有限次数的对比查询，推断出最畅通（拥堵排名第一）或最拥堵（拥堵排名最后）的路口。

你可以进行以下两类操作：

1. **比较查询**：询问两个不同路口 a 和 b 的拥堵情况。我会告诉你哪个路口相对更畅通（拥堵排名更小，即更靠前）。每次查询会消耗一次查询次数。

2. **终止宣告**（可选其一，不消耗查询次数）：
   - 宣告最畅通路口：宣告某个路口是排名第一（最畅通）的路口。
   - 宣告最拥堵路口：宣告某个路口是排名最后（最拥堵）的路口。

**约束条件**：
- 比较查询的总次数不能超过 {max_queries} 次。
- 必须在查询次数用尽前做出正确的终止宣告才算成功。
- 如果宣告错误或查询次数超限后未宣告，排查任务失败。

每次只能进行一个操作，使用以下 XML 格式：

- 比较查询（例如比较路口 3 和 5）：
<query_compare>3,5</query_compare>

- 宣告最畅通路口（对应 type=min，例如宣告路口 2 最畅通）：
<answer>type=min, element=2</answer>

- 宣告最拥堵路口（对应 type=max，例如宣告路口 7 最拥堵）：
<answer>type=max, element=7</answer>

注意：终止宣告会立即结束排查并判定成败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Urban Traffic Intersection Congestion Assessment System.

The system monitors {n} key traffic intersections, numbered from 1 to {n}. The current congestion levels of these intersections have an unknown strict total order (each intersection has a unique congestion rank with no ties).

Your goal is to infer either the least congested intersection (ranked first) or the most congested intersection (ranked last) using a limited number of comparison queries.

You can perform the following two types of operations:

1. **Comparison Query**: Ask about the congestion of two different intersections a and b. I will tell you which intersection is less congested (has a smaller rank, i.e., comes earlier). Each query consumes one query count.

2. **Termination Declaration** (choose one, does not consume query count):
   - Declare Least Congested: Declare that a specific intersection is ranked first (least congested).
   - Declare Most Congested: Declare that a specific intersection is ranked last (most congested).

**Constraints**:
- The total number of comparison queries cannot exceed {max_queries}.
- You must make a correct termination declaration before running out of queries to succeed.
- If the declaration is wrong or you exceed the query limit without declaring, the task fails.

Each turn allows only one operation. Use the following XML format:

- Comparison Query (e.g., comparing intersections 3 and 5):
<query_compare>3,5</query_compare>

- Declare Least Congested (corresponds to type=min, e.g., declaring intersection 2 is the least congested):
<answer>type=min, element=2</answer>

- Declare Most Congested (corresponds to type=max, e.g., declaring intersection 7 is the most congested):
<answer>type=max, element=7</answer>

Note: A termination declaration immediately ends the task and determines success or failure.
"""

    contextualized_rule_zh_2 = """\
欢迎进入急诊科患者分诊系统。

当前候诊室有 {n} 名待诊患者，编号为 1 到 {n}。这些患者的病情紧急程度存在一个未知的严格全序关系（每名患者都有唯一的紧急度排名，没有并列）。

你的目标是通过有限次数的病情对比查询，推断出病情最紧急（排名第一）或病情最轻微（排名最后）的患者。

你可以进行以下两类操作：

1. **比较查询**：询问两名不同患者 a 和 b 的病情。我会告诉你哪名患者的病情更紧急（紧急度排名更小，即更靠前）。每次查询会消耗一次诊断次数。

2. **终止宣告**（可选其一，不消耗诊断次数）：
   - 宣告最紧急患者：宣告某名患者是排名第一（最紧急）的患者。
   - 宣告最轻微患者：宣告某名患者是排名最后（最轻微）的患者。

**约束条件**：
- 比较查询的总次数不能超过 {max_queries} 次。
- 必须在诊断次数用尽前做出正确的终止宣告才算成功。
- 如果宣告错误或查询次数超限后未宣告，分诊失败。

每次只能进行一个操作，使用以下 XML 格式：

- 比较查询（例如比较患者 3 和 5）：
<query_compare>3,5</query_compare>

- 宣告最紧急患者（对应 type=min，例如宣告患者 2 最紧急）：
<answer>type=min, element=2</answer>

- 宣告最轻微患者（对应 type=max，例如宣告患者 7 最轻微）：
<answer>type=max, element=7</answer>

注意：终止宣告会立即结束分诊并判定成败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Emergency Department Patient Triage System.

There are currently {n} patients waiting, numbered from 1 to {n}. The urgency of these patients' conditions follows an unknown strict total order (each patient has a unique urgency rank with no ties).

Your goal is to infer either the most urgent patient (ranked first) or the least urgent patient (ranked last) using a limited number of comparison queries.

You can perform the following two types of operations:

1. **Comparison Query**: Ask about the condition of two different patients a and b. I will tell you which patient's condition is more urgent (has a smaller rank, i.e., comes earlier). Each query consumes one diagnostic count.

2. **Termination Declaration** (choose one, does not consume diagnostic count):
   - Declare Most Urgent: Declare that a specific patient is ranked first (most urgent).
   - Declare Least Urgent: Declare that a specific patient is ranked last (least urgent).

**Constraints**:
- The total number of comparison queries cannot exceed {max_queries}.
- You must make a correct termination declaration before running out of diagnostic queries to succeed.
- If the declaration is wrong or you exceed the query limit without declaring, the triage fails.

Each turn allows only one operation. Use the following XML format:

- Comparison Query (e.g., comparing patients 3 and 5):
<query_compare>3,5</query_compare>

- Declare Most Urgent (corresponds to type=min, e.g., declaring patient 2 is the most urgent):
<answer>type=min, element=2</answer>

- Declare Least Urgent (corresponds to type=max, e.g., declaring patient 7 is the least urgent):
<answer>type=max, element=7</answer>

Note: A termination declaration immediately ends the triage and determines success or failure.
"""

    contextualized_rule_zh_3 = """\
欢迎使用学术成绩匿名评估系统。

本期评估包含 {n} 份匿名试卷，编号为 1 到 {n}。这些试卷的成绩存在一个未知的严格全序关系（每份试卷都有唯一的成绩排名，没有并列）。

你的目标是通过有限次数的成绩对比查询，推断出成绩最优（排名第一）或成绩最差（排名最后）的试卷。

你可以进行以下两类操作：

1. **比较查询**：询问两份不同试卷 a 和 b 的成绩表现。我会告诉你哪份试卷的成绩更优异（排名更小，即更靠前）。每次查询会消耗一次评估次数。

2. **终止宣告**（可选其一，不消耗评估次数）：
   - 宣告最优试卷：宣告某份试卷是排名第一（成绩最优）的试卷。
   - 宣告最差试卷：宣告某份试卷是排名最后（成绩最差）的试卷。

**约束条件**：
- 比较查询的总次数不能超过 {max_queries} 次。
- 必须在评估次数用尽前做出正确的终止宣告才算成功。
- 如果宣告错误或查询次数超限后未宣告，评估任务失败。

每次只能进行一个操作，使用以下 XML 格式：

- 比较查询（例如比较试卷 3 和 5）：
<query_compare>3,5</query_compare>

- 宣告最优试卷（对应 type=min，例如宣告试卷 2 最优）：
<answer>type=min, element=2</answer>

- 宣告最差试卷（对应 type=max，例如宣告试卷 7 最差）：
<answer>type=max, element=7</answer>

注意：终止宣告会立即结束评估并判定成败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Anonymous Academic Performance Assessment System.

This assessment involves {n} anonymous exam papers, numbered from 1 to {n}. The scores of these papers have an unknown strict total order (each paper has a unique score rank with no ties).

Your goal is to infer either the highest-scoring paper (ranked first) or the lowest-scoring paper (ranked last) using a limited number of comparison queries.

You can perform the following two types of operations:

1. **Comparison Query**: Ask about the performance of two different papers a and b. I will tell you which paper has a better score (has a smaller rank, i.e., comes earlier). Each query consumes one assessment count.

2. **Termination Declaration** (choose one, does not consume assessment count):
   - Declare Highest-Scoring: Declare that a specific paper is ranked first (highest score).
   - Declare Lowest-Scoring: Declare that a specific paper is ranked last (lowest score).

**Constraints**:
- The total number of comparison queries cannot exceed {max_queries}.
- You must make a correct termination declaration before running out of assessment queries to succeed.
- If the declaration is wrong or you exceed the query limit without declaring, the assessment fails.

Each turn allows only one operation. Use the following XML format:

- Comparison Query (e.g., comparing papers 3 and 5):
<query_compare>3,5</query_compare>

- Declare Highest-Scoring (corresponds to type=min, e.g., declaring paper 2 is the highest-scoring):
<answer>type=min, element=2</answer>

- Declare Lowest-Scoring (corresponds to type=max, e.g., declaring paper 7 is the lowest-scoring):
<answer>type=max, element=7</answer>

Note: A termination declaration immediately ends the assessment and determines success or failure.
"""

    contextualized_rule_zh_4 = """\
欢迎使用工业流水线质量控制系统。

当前批次共有 {n} 个生产组件，编号为 1 到 {n}。这些组件的加工精度存在一个未知的严格全序关系（每个组件都有唯一的精度排名，没有并列）。

你的目标是通过有限次数的精度抽检对比，推断出精度最高（排名第一）或精度最低（排名最后）的组件。

你可以进行以下两类操作：

1. **比较查询**：抽检对比两个不同组件 a 和 b。我会告诉你哪个组件的精度更高（排名更小，即更靠前）。每次查询会消耗一次抽检次数。

2. **终止宣告**（可选其一，不消耗抽检次数）：
   - 宣告最高精度组件：宣告某个组件是排名第一（精度最高）的组件。
   - 宣告最低精度组件：宣告某个组件是排名最后（精度最低）的组件。

**约束条件**：
- 比较查询的总次数不能超过 {max_queries} 次。
- 必须在抽检次数用尽前做出正确的终止宣告才算成功。
- 如果宣告错误或查询次数超限后未宣告，质控任务失败。

每次只能进行一个操作，使用以下 XML 格式：

- 比较查询（例如对比组件 3 和 5）：
<query_compare>3,5</query_compare>

- 宣告最高精度组件（对应 type=min，例如宣告组件 2 精度最高）：
<answer>type=min, element=2</answer>

- 宣告最低精度组件（对应 type=max，例如宣告组件 7 精度最低）：
<answer>type=max, element=7</answer>

注意：终止宣告会立即结束质控并判定成败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Industrial Assembly Line Quality Control System.

The current batch consists of {n} production components, numbered from 1 to {n}. The processing precision of these components has an unknown strict total order (each component has a unique precision rank with no ties).

Your goal is to infer either the most precise component (ranked first) or the least precise component (ranked last) using a limited number of precision comparison queries.

You can perform the following two types of operations:

1. **Comparison Query**: Compare the precision of two different components a and b. I will tell you which component has higher precision (has a smaller rank, i.e., comes earlier). Each query consumes one inspection count.

2. **Termination Declaration** (choose one, does not consume inspection count):
   - Declare Most Precise: Declare that a specific component is ranked first (highest precision).
   - Declare Least Precise: Declare that a specific component is ranked last (lowest precision).

**Constraints**:
- The total number of comparison queries cannot exceed {max_queries}.
- You must make a correct termination declaration before running out of inspection queries to succeed.
- If the declaration is wrong or you exceed the query limit without declaring, the quality control task fails.

Each turn allows only one operation. Use the following XML format:

- Comparison Query (e.g., comparing components 3 and 5):
<query_compare>3,5</query_compare>

- Declare Most Precise (corresponds to type=min, e.g., declaring component 2 is the most precise):
<answer>type=min, element=2</answer>

- Declare Least Precise (corresponds to type=max, e.g., declaring component 7 is the least precise):
<answer>type=max, element=7</answer>

Note: A termination declaration immediately ends the quality control task and determines success or failure.
"""

    contextualized_rule_zh_5 = """\
欢迎使用法务证据证明力分析系统。

本案目前收集了 {n} 份关键证据，编号为 1 到 {n}。这些证据的证明力大小存在一个未知的严格全序关系（每份证据都有唯一的证明力排名，没有并列）。

你的目标是通过有限次数的法理对比查询，推断出证明力最强（排名第一）或证明力最弱（排名最后）的证据。

你可以进行以下两类操作：

1. **比较查询**：询问两份不同证据 a 和 b 的效力。我会告诉你哪份证据的证明力更强（排名更小，即更靠前）。每次查询会消耗一次核查次数。

2. **终止宣告**（可选其一，不消耗核查次数）：
   - 宣告最强证据：宣告某份证据是排名第一（证明力最强）的证据。
   - 宣告最弱证据：宣告某份证据是排名最后（证明力最弱）的证据。

**约束条件**：
- 比较查询的总次数不能超过 {max_queries} 次。
- 必须在核查次数用尽前做出正确的终止宣告才算成功。
- 如果宣告错误或查询次数超限后未宣告，证据分析失败。

每次只能进行一个操作，使用以下 XML 格式：

- 比较查询（例如对比证据 3 和 5）：
<query_compare>3,5</query_compare>

- 宣告最强证据（对应 type=min，例如宣告证据 2 证明力最强）：
<answer>type=min, element=2</answer>

- 宣告最弱证据（对应 type=max，例如宣告证据 7 证明力最弱）：
<answer>type=max, element=7</answer>

注意：终止宣告会立即结束证据分析并判定成败。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the Legal Evidence Probative Value Analysis System.

There are currently {n} key pieces of evidence collected for this case, numbered from 1 to {n}. The probative value of these evidence items follows an unknown strict total order (each item has a unique probative rank with no ties).

Your goal is to infer either the evidence with the strongest probative value (ranked first) or the weakest probative value (ranked last) using a limited number of comparative queries.

You can perform the following two types of operations:

1. **Comparison Query**: Ask about the efficacy of two different evidence items a and b. I will tell you which item has stronger probative value (has a smaller rank, i.e., comes earlier). Each query consumes one verification count.

2. **Termination Declaration** (choose one, does not consume verification count):
   - Declare Strongest Evidence: Declare that a specific evidence item is ranked first (strongest probative value).
   - Declare Weakest Evidence: Declare that a specific evidence item is ranked last (weakest probative value).

**Constraints**:
- The total number of comparison queries cannot exceed {max_queries}.
- You must make a correct termination declaration before running out of verification queries to succeed.
- If the declaration is wrong or you exceed the query limit without declaring, the evidence analysis fails.

Each turn allows only one operation. Use the following XML format:

- Comparison Query (e.g., comparing evidence items 3 and 5):
<query_compare>3,5</query_compare>

- Declare Strongest Evidence (corresponds to type=min, e.g., declaring evidence 2 is the strongest):
<answer>type=min, element=2</answer>

- Declare Weakest Evidence (corresponds to type=max, e.g., declaring evidence 7 is the weakest):
<answer>type=max, element=7</answer>

Note: A termination declaration immediately ends the evidence analysis and determines success or failure.
"""

    tags = ["answer", "query_compare"]
    
    reasoning_type = "演绎推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "max_queries": 4,
                "order": [3, 1, 5, 2, 4],
                "target_type": "min",
            },
            2: {
                "n": 8,
                "max_queries": 7,
                "order": [5, 2, 7, 1, 8, 3, 6, 4],
                "target_type": "max",
            },
            3: {
                "n": 10,
                "max_queries": 9,
                "order": [6, 3, 9, 1, 7, 4, 10, 2, 8, 5],
                "target_type": "min",
            },
            4: {
                "n": 15,
                "max_queries": 14,
                "order": [8, 12, 4, 15, 2, 10, 6, 13, 1, 9, 5, 14, 3, 11, 7],
                "target_type": "max",
            },
            5: {
                "n": 20,
                "max_queries": 19,
                "order": [11, 5, 18, 3, 14, 9, 20, 1, 16, 7, 12, 4, 19, 6, 15, 2, 17, 8, 13, 10],
                "target_type": "min",
            },
        },
        "en": {
            1: {
                "n": 5,
                "max_queries": 4,
                "order": [3, 1, 5, 2, 4],
                "target_type": "min",
            },
            2: {
                "n": 8,
                "max_queries": 7,
                "order": [5, 2, 7, 1, 8, 3, 6, 4],
                "target_type": "max",
            },
            3: {
                "n": 10,
                "max_queries": 9,
                "order": [6, 3, 9, 1, 7, 4, 10, 2, 8, 5],
                "target_type": "min",
            },
            4: {
                "n": 15,
                "max_queries": 14,
                "order": [8, 12, 4, 15, 2, 10, 6, 13, 1, 9, 5, 14, 3, 11, 7],
                "target_type": "max",
            },
            5: {
                "n": 20,
                "max_queries": 19,
                "order": [11, 5, 18, 3, 14, 9, 20, 1, 16, 7, 12, 4, 19, 6, 15, 2, 17, 8, 13, 10],
                "target_type": "min",
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0
        self._over_limit_warnings = 0
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        n = cfg["n"]
        max_queries = cfg["max_queries"]
        target_type = cfg["target_type"]

        order = cfg["order"]

        self._game_info["n"] = n
        self._game_info["max_queries"] = max_queries
        
        self.order = order
        self.max_queries = max_queries
        self.target_type = target_type
        
        if self.target_type == "min":
            self.correct_answer = str(self.order.index(1) + 1)
        else:
            self.correct_answer = str(self.order.index(n) + 1)
        
        self.query_count = 0

    def evaluate(self, parsed_info):
        if self.query_count > self.max_queries:
            return False
        
        raw_ans = parsed_info["answer"]
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "type" not in ans_dict or "element" not in ans_dict:
            return False
        
        declared_type = ans_dict["type"]
        declared_element = ans_dict["element"]

        if declared_type == "min":
            correct = str(self.order.index(1) + 1)
            return declared_element == correct
        elif declared_type == "max":
            correct = str(self.order.index(self._game_info["n"]) + 1)
            return declared_element == correct
        else:
            return False

    def _cf_core_produce(self, parsed_info):
        if "query_compare" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        if self.query_count >= self.max_queries:
            self._over_limit_warnings += 1
            if self._over_limit_warnings >= 3:
                self.state.set_state("failed", "repeated queries after limit exceeded")
                if self.config.language == "zh":
                    return "游戏结束：多次超限查询后仍未提交答案。"
                else:
                    return "Game over: Failed to submit answer after repeated queries beyond limit."
            
            if self.config.language == "zh":
                err_msg = f"错误：查询次数已达上限 {self.max_queries} 次，请提交最终答案。"
            else:
                err_msg = f"Error: Query limit of {self.max_queries} reached. Please submit your final answer."
            return err_msg
        
        try:
            raw = parsed_info["query_compare"]
            parts = [x.strip() for x in raw.split(",")]
            if len(parts) != 2:
                raise ValueError("Need exactly two elements")
            
            id1, id2 = parts
            
            if not id1.isdigit() or not id2.isdigit():
                raise ValueError("Invalid element ID")
            
            idx1, idx2 = int(id1), int(id2)
            
            if idx1 < 1 or idx1 > self._game_info["n"] or idx2 < 1 or idx2 > self._game_info["n"]:
                raise ValueError("Element ID out of range")
            
            if idx1 == idx2:
                raise ValueError("Cannot compare an element with itself")
            
            self.query_count += 1
            
            rank1 = self.order[idx1 - 1]
            rank2 = self.order[idx2 - 1]
            
            if rank1 < rank2:
                return id1
            else:
                return id2
            
        except Exception as e:
            if self.config.language == "zh":
                return f"错误：查询格式无效或元素编号错误。({str(e)})"
            else:
                return f"Error: Invalid query format or element ID. ({str(e)})"

    def _cf_make_wrong(self, correct: str) -> str:
        n = self._game_info["n"]
        
        try:
            correct_int = int(correct)
            if 1 <= correct_int <= n:
                wrong = correct_int + 1 if correct_int < n else correct_int - 1
                return str(wrong)
        except ValueError:
            pass
        
        return str(random.randint(1, n))

    def get_all_possible_queries(self) -> list[dict]:
        n = self._game_info["n"]
        queries = []
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                rank1 = self.order[i - 1]
                rank2 = self.order[j - 1]
                
                if rank1 < rank2:
                    ans = str(i)
                else:
                    ans = str(j)
                
                queries.append({
                    "query": f"<query_compare>{i},{j}</query_compare>",
                    "answer": ans
                })
        return queries