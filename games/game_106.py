from .base import Game
import random

class BinaryReachabilityGame(Game):

    game_rule_zh = """\
我们来玩一个"二进制可达性推理"游戏，规则如下：

游戏设定了一个元素集合 S，包含全部 8 个三位二进制串：000, 001, 010, 011, 100, 101, 110, 111。

我已经秘密选择了一个隐藏的判定函数 f，它会将每个元素标记为 0 或 1。基于这个函数，我们定义"互相可达"关系：两个不同的元素 u 和 v 互相可达，当且仅当 f(u) 等于 f(v)。

现在给你 6 个目标对需要判断：
{target_pairs}

你的任务是推断出这 6 个目标对中，哪些是"互相可达"的，哪些不是。

为了帮助你推断，你可以进行试探查询（最多 {max_queries} 次）。每次查询的格式是询问某个有序对 (u, v) 是否满足 f(u) 等于 f(v)，我会回答"是"或"否"。

查询限制：
1. 不能查询相同的元素对，即 u 必须不等于 v
2. 不能查询任何一个目标对（即使顺序相反）
3. 查询 (u, v) 和 (v, u) 视为两次不同的查询

当你收集了足够信息后（或用完查询次数后），请提交你对全部 6 个目标对的判断结果。

每次询问使用以下 XML 格式（例如询问 000 和 011）：
<query>000,011</query>

提交最终答案时，必须对全部 6 个目标对按顺序给出判断（用 1 表示互相可达，0 表示不可达），用逗号分隔：
<answer>1,0,1,0,1,0</answer>

注意：答案必须恰好包含 6 个数字（0 或 1），顺序与目标对列表一致。
"""

    game_rule_en = """\
Let's play a "Binary Reachability Inference" game. Here are the rules:

The game defines an element set S containing all 8 three-bit binary strings: 000, 001, 010, 011, 100, 101, 110, 111.

I have secretly chosen a hidden decision function f that labels each element as 0 or 1. Based on this function, we define a "mutually reachable" relation: two distinct elements u and v are mutually reachable if and only if f(u) equals f(v).

Now you are given 6 target pairs to judge:
{target_pairs}

Your task is to infer which of these 6 target pairs are "mutually reachable" and which are not.

To help you infer, you can make probe queries (up to {max_queries} times). Each query asks whether an ordered pair (u, v) satisfies f(u) equals f(v), and I will answer "Yes" or "No".

Query restrictions:
1. Cannot query the same element pair, i.e., u must not equal v
2. Cannot query any target pair (even in reverse order)
3. Queries (u, v) and (v, u) are considered two different queries

When you have collected enough information (or exhausted your queries), please submit your judgment for all 6 target pairs.

Each query uses the following XML format (e.g., querying 000 and 011):
<query>000,011</query>

When submitting the final answer, you must provide judgments for all 6 target pairs in order (use 1 for mutually reachable, 0 for not reachable), separated by commas:
<answer>1,0,1,0,1,0</answer>

Note: The answer must contain exactly 6 digits (0 or 1), in the same order as the target pairs list.
"""

    contextualized_rule_zh_1 = """\
欢迎使用城市智能交通路口配置测试系统，我们将对不同路口通行模式的拥堵情况进行排查。

系统设定了一个方案集合 S，包含全部 8 个三位二进制编号：000, 001, 010, 011, 100, 101, 110, 111。

系统秘密选择了一个隐藏的评估函数 f，它会将每个方案评估为 0 或 1。基于这个函数，我们定义"同质通行模式"关系：两个不同的方案 u 和 v 是同质通行模式的（互相可达），当且仅当 f(u) 等于 f(v)。

现在给你 6 个目标对需要评估：
{target_pairs}

你的任务是推断出这 6 个目标对中，哪些是"同质通行模式"的，哪些不是。

为了帮助你推断，你可以进行试探查询（最多 {max_queries} 次）。每次查询的格式是询问某个有序对 (u, v) 是否满足 f(u) 等于 f(v)，我会回答"是"或"否"。

查询限制：
1. 不能查询相同的方案对，即 u 必须不等于 v
2. 不能查询任何一个目标对（即使顺序相反）
3. 查询 (u, v) 和 (v, u) 视为两次不同的查询

当你收集了足够信息后（或用完查询次数后），请提交你对全部 6 个目标对的判断结果。

每次询问使用以下 XML 格式（例如询问 000 和 011）：
<query>000,011</query>

提交最终答案时，必须对全部 6 个目标对按顺序给出判断（用 1 表示同质通行模式，0 表示不同质通行模式），用逗号分隔：
<answer>1,0,1,0,1,0</answer>

注意：答案必须恰好包含 6 个数字（0 或 1），顺序与目标对列表一致。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Urban Intelligent Traffic Intersection Configuration Testing System. We will examine the congestion status of different intersection traffic patterns.

The system defines a scheme set S containing all 8 three-bit binary codes: 000, 001, 010, 011, 100, 101, 110, 111.

The system has secretly chosen a hidden evaluation function f that evaluates each scheme as 0 or 1. Based on this function, we define a "Homogeneous Traffic Patterns" relation: two distinct schemes u and v are Homogeneous Traffic Patterns (mutually reachable) if and only if f(u) equals f(v).

Now you are given 6 target pairs to evaluate:
{target_pairs}

Your task is to infer which of these 6 target pairs are "Homogeneous Traffic Patterns" and which are not.

To help you infer, you can make probe queries (up to {max_queries} times). Each query asks whether an ordered pair (u, v) satisfies f(u) equals f(v), and I will answer "Yes" or "No".

Query restrictions:
1. Cannot query the same scheme pair, i.e., u must not equal v
2. Cannot query any target pair (even in reverse order)
3. Queries (u, v) and (v, u) are considered two different queries

When you have collected enough information (or exhausted your queries), please submit your judgment for all 6 target pairs.

Each query uses the following XML format (e.g., querying 000 and 011):
<query>000,011</query>

When submitting the final answer, you must provide judgments for all 6 target pairs in order (use 1 for Homogeneous Traffic Patterns, 0 for not Homogeneous Traffic Patterns), separated by commas:
<answer>1,0,1,0,1,0</answer>

Note: The answer must contain exactly 6 digits (0 or 1), in the same order as the target pairs list.
"""

    contextualized_rule_zh_2 = """\
欢迎使用罕见病靶向药物配方临床试验分析系统，我们需要筛选出药效一致的配方组合。

系统设定了一个方案集合 S，包含全部 8 个三位二进制编号：000, 001, 010, 011, 100, 101, 110, 111。

系统秘密选择了一个隐藏的评估函数 f，它会将每个方案评估为 0 或 1。基于这个函数，我们定义"等效配方"关系：两个不同的方案 u 和 v 是等效配方的（互相可达），当且仅当 f(u) 等于 f(v)。

现在给你 6 个目标对需要评估：
{target_pairs}

你的任务是推断出这 6 个目标对中，哪些是"等效配方"的，哪些不是。

为了帮助你推断，你可以进行试探查询（最多 {max_queries} 次）。每次查询的格式是询问某个有序对 (u, v) 是否满足 f(u) 等于 f(v)，我会回答"是"或"否"。

查询限制：
1. 不能查询相同的方案对，即 u 必须不等于 v
2. 不能查询任何一个目标对（即使顺序相反）
3. 查询 (u, v) 和 (v, u) 视为两次不同的查询

当你收集了足够信息后（或用完查询次数后），请提交你对全部 6 个目标对的判断结果。

每次询问使用以下 XML 格式（例如询问 000 和 011）：
<query>000,011</query>

提交最终答案时，必须对全部 6 个目标对按顺序给出判断（用 1 表示等效配方，0 表示不等效配方），用逗号分隔：
<answer>1,0,1,0,1,0</answer>

注意：答案必须恰好包含 6 个数字（0 或 1），顺序与目标对列表一致。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Rare Disease Targeted Drug Formulation Clinical Trial Analysis System. We need to screen out formulation combinations with consistent clinical efficacy.

The system defines a scheme set S containing all 8 three-bit binary codes: 000, 001, 010, 011, 100, 101, 110, 111.

The system has secretly chosen a hidden evaluation function f that evaluates each scheme as 0 or 1. Based on this function, we define an "Equivalent Formulations" relation: two distinct schemes u and v are Equivalent Formulations (mutually reachable) if and only if f(u) equals f(v).

Now you are given 6 target pairs to evaluate:
{target_pairs}

Your task is to infer which of these 6 target pairs are "Equivalent Formulations" and which are not.

To help you infer, you can make probe queries (up to {max_queries} times). Each query asks whether an ordered pair (u, v) satisfies f(u) equals f(v), and I will answer "Yes" or "No".

Query restrictions:
1. Cannot query the same scheme pair, i.e., u must not equal v
2. Cannot query any target pair (even in reverse order)
3. Queries (u, v) and (v, u) are considered two different queries

When you have collected enough information (or exhausted your queries), please submit your judgment for all 6 target pairs.

Each query uses the following XML format (e.g., querying 000 and 011):
<query>000,011</query>

When submitting the final answer, you must provide judgments for all 6 target pairs in order (use 1 for Equivalent Formulations, 0 for not Equivalent Formulations), separated by commas:
<answer>1,0,1,0,1,0</answer>

Note: The answer must contain exactly 6 digits (0 or 1), in the same order as the target pairs list.
"""

    contextualized_rule_zh_3 = """\
欢迎进入个性化教学干预策略评估系统，我们将分析不同教学方案对学生成绩提升的内在一致性。

系统设定了一个方案集合 S，包含全部 8 个三位二进制编号：000, 001, 010, 011, 100, 101, 110, 111。

系统秘密选择了一个隐藏的评估函数 f，它会将每个方案评估为 0 或 1。基于这个函数，我们定义"同效策略"关系：两个不同的方案 u 和 v 是同效策略的（互相可达），当且仅当 f(u) 等于 f(v)。

现在给你 6 个目标对需要评估：
{target_pairs}

你的任务是推断出这 6 个目标对中，哪些是"同效策略"的，哪些不是。

为了帮助你推断，你可以进行试探查询（最多 {max_queries} 次）。每次查询的格式是询问某个有序对 (u, v) 是否满足 f(u) 等于 f(v)，我会回答"是"或"否"。

查询限制：
1. 不能查询相同的方案对，即 u 必须不等于 v
2. 不能查询任何一个目标对（即使顺序相反）
3. 查询 (u, v) 和 (v, u) 视为两次不同的查询

当你收集了足够信息后（或用完查询次数后），请提交你对全部 6 个目标对的判断结果。

每次询问使用以下 XML 格式（例如询问 000 和 011）：
<query>000,011</query>

提交最终答案时，必须对全部 6 个目标对按顺序给出判断（用 1 表示同效策略，0 表示不同效策略），用逗号分隔：
<answer>1,0,1,0,1,0</answer>

注意：答案必须恰好包含 6 个数字（0 或 1），顺序与目标对列表一致。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Personalized Teaching Intervention Strategy Evaluation System. We will analyze the internal consistency of different teaching schemes on students' academic improvement.

The system defines a scheme set S containing all 8 three-bit binary codes: 000, 001, 010, 011, 100, 101, 110, 111.

The system has secretly chosen a hidden evaluation function f that evaluates each scheme as 0 or 1. Based on this function, we define an "Iso-effective Strategies" relation: two distinct schemes u and v are Iso-effective Strategies (mutually reachable) if and only if f(u) equals f(v).

Now you are given 6 target pairs to evaluate:
{target_pairs}

Your task is to infer which of these 6 target pairs are "Iso-effective Strategies" and which are not.

To help you infer, you can make probe queries (up to {max_queries} times). Each query asks whether an ordered pair (u, v) satisfies f(u) equals f(v), and I will answer "Yes" or "No".

Query restrictions:
1. Cannot query the same scheme pair, i.e., u must not equal v
2. Cannot query any target pair (even in reverse order)
3. Queries (u, v) and (v, u) are considered two different queries

When you have collected enough information (or exhausted your queries), please submit your judgment for all 6 target pairs.

Each query uses the following XML format (e.g., querying 000 and 011):
<query>000,011</query>

When submitting the final answer, you must provide judgments for all 6 target pairs in order (use 1 for Iso-effective Strategies, 0 for not Iso-effective Strategies), separated by commas:
<answer>1,0,1,0,1,0</answer>

Note: The answer must contain exactly 6 digits (0 or 1), in the same order as the target pairs list.
"""

    contextualized_rule_zh_4 = """\
欢迎访问新型合金材料热处理工艺参数优化平台，我们将对不同工艺组合下的产品良率进行分析。

系统设定了一个方案集合 S，包含全部 8 个三位二进制编号：000, 001, 010, 011, 100, 101, 110, 111。

系统秘密选择了一个隐藏的评估函数 f，它会将每个方案评估为 0 或 1。基于这个函数，我们定义"等效工艺"关系：两个不同的方案 u 和 v 是等效工艺的（互相可达），当且仅当 f(u) 等于 f(v)。

现在给你 6 个目标对需要评估：
{target_pairs}

你的任务是推断出这 6 个目标对中，哪些是"等效工艺"的，哪些不是。

为了帮助你推断，你可以进行试探查询（最多 {max_queries} 次）。每次查询的格式是询问某个有序对 (u, v) 是否满足 f(u) 等于 f(v)，我会回答"是"或"否"。

查询限制：
1. 不能查询相同的方案对，即 u 必须不等于 v
2. 不能查询任何一个目标对（即使顺序相反）
3. 查询 (u, v) 和 (v, u) 视为两次不同的查询

当你收集了足够信息后（或用完查询次数后），请提交你对全部 6 个目标对的判断结果。

每次询问使用以下 XML 格式（例如询问 000 和 011）：
<query>000,011</query>

提交最终答案时，必须对全部 6 个目标对按顺序给出判断（用 1 表示等效工艺，0 表示不等效工艺），用逗号分隔：
<answer>1,0,1,0,1,0</answer>

注意：答案必须恰好包含 6 个数字（0 或 1），顺序与目标对列表一致。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the New Alloy Material Heat Treatment Process Parameter Optimization Platform. We will analyze the product yield under different process combinations.

The system defines a scheme set S containing all 8 three-bit binary codes: 000, 001, 010, 011, 100, 101, 110, 111.

The system has secretly chosen a hidden evaluation function f that evaluates each scheme as 0 or 1. Based on this function, we define an "Equivalent Processes" relation: two distinct schemes u and v are Equivalent Processes (mutually reachable) if and only if f(u) equals f(v).

Now you are given 6 target pairs to evaluate:
{target_pairs}

Your task is to infer which of these 6 target pairs are "Equivalent Processes" and which are not.

To help you infer, you can make probe queries (up to {max_queries} times). Each query asks whether an ordered pair (u, v) satisfies f(u) equals f(v), and I will answer "Yes" or "No".

Query restrictions:
1. Cannot query the same scheme pair, i.e., u must not equal v
2. Cannot query any target pair (even in reverse order)
3. Queries (u, v) and (v, u) are considered two different queries

When you have collected enough information (or exhausted your queries), please submit your judgment for all 6 target pairs.

Each query uses the following XML format (e.g., querying 000 and 011):
<query>000,011</query>

When submitting the final answer, you must provide judgments for all 6 target pairs in order (use 1 for Equivalent Processes, 0 for not Equivalent Processes), separated by commas:
<answer>1,0,1,0,1,0</answer>

Note: The answer must contain exactly 6 digits (0 or 1), in the same order as the target pairs list.
"""

    contextualized_rule_zh_5 = """\
欢迎使用商业合同争议条款司法裁判效力预测系统，我们需要评估各条款组合在司法实践中的效力一致性。

系统设定了一个方案集合 S，包含全部 8 个三位二进制编号：000, 001, 010, 011, 100, 101, 110, 111。

系统秘密选择了一个隐藏的评估函数 f，它会将每个方案评估为 0 或 1。基于这个函数，我们定义"同等法律效力"关系：两个不同的方案 u 和 v 是同等法律效力的（互相可达），当且仅当 f(u) 等于 f(v)。

现在给你 6 个目标对需要评估：
{target_pairs}

你的任务是推断出这 6 个目标对中，哪些是"同等法律效力"的，哪些不是。

为了帮助你推断，你可以进行试探查询（最多 {max_queries} 次）。每次查询的格式是询问某个有序对 (u, v) 是否满足 f(u) 等于 f(v)，我会回答"是"或"否"。

查询限制：
1. 不能查询相同的方案对，即 u 必须不等于 v
2. 不能查询任何一个目标对（即使顺序相反）
3. 查询 (u, v) 和 (v, u) 视为两次不同的查询

当你收集了足够信息后（或用完查询次数后），请提交你对全部 6 个目标对的判断结果。

每次询问使用以下 XML 格式（例如询问 000 和 011）：
<query>000,011</query>

提交最终答案时，必须对全部 6 个目标对按顺序给出判断（用 1 表示同等法律效力，0 表示不同等法律效力），用逗号分隔：
<answer>1,0,1,0,1,0</answer>

注意：答案必须恰好包含 6 个数字（0 或 1），顺序与目标对列表一致。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Commercial Contract Dispute Clause Judicial Adjudication Validity Prediction System. We need to evaluate the validity consistency of various clause combinations in judicial practice.

The system defines a scheme set S containing all 8 three-bit binary codes: 000, 001, 010, 011, 100, 101, 110, 111.

The system has secretly chosen a hidden evaluation function f that evaluates each scheme as 0 or 1. Based on this function, we define an "Equivalent Legal Validity" relation: two distinct schemes u and v are Equivalent Legal Validity (mutually reachable) if and only if f(u) equals f(v).

Now you are given 6 target pairs to evaluate:
{target_pairs}

Your task is to infer which of these 6 target pairs are "Equivalent Legal Validity" and which are not.

To help you infer, you can make probe queries (up to {max_queries} times). Each query asks whether an ordered pair (u, v) satisfies f(u) equals f(v), and I will answer "Yes" or "No".

Query restrictions:
1. Cannot query the same scheme pair, i.e., u must not equal v
2. Cannot query any target pair (even in reverse order)
3. Queries (u, v) and (v, u) are considered two different queries

When you have collected enough information (or exhausted your queries), please submit your judgment for all 6 target pairs.

Each query uses the following XML format (e.g., querying 000 and 011):
<query>000,011</query>

When submitting the final answer, you must provide judgments for all 6 target pairs in order (use 1 for Equivalent Legal Validity, 0 for not Equivalent Legal Validity), separated by commas:
<answer>1,0,1,0,1,0</answer>

Note: The answer must contain exactly 6 digits (0 or 1), in the same order as the target pairs list.
"""

    tags = ["answer", "query"]
    reasoning_type = "归纳推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "w": (1, 0, 0),
                "delta": 0,
                "target_pairs": [
                    ("000", "001"),
                    ("010", "011"),
                    ("100", "101"),
                    ("000", "100"),
                    ("001", "101"),
                    ("010", "110"),
                ],
                "max_queries": 5,
            },
            2: {
                "w": (1, 1, 0),
                "delta": 0,
                "target_pairs": [
                    ("000", "011"),
                    ("001", "010"),
                    ("100", "111"),
                    ("000", "001"),
                    ("010", "100"),
                    ("011", "111"),
                ],
                "max_queries": 5,
            },
            3: {
                "w": (1, 0, 1),
                "delta": 1,
                "target_pairs": [
                    ("000", "010"),
                    ("001", "011"),
                    ("100", "110"),
                    ("000", "001"),
                    ("010", "011"),
                    ("100", "101"),
                ],
                "max_queries": 5,
            },
            4: {
                "w": (1, 1, 1),
                "delta": 0,
                "target_pairs": [
                    ("000", "011"),
                    ("001", "010"),
                    ("100", "111"),
                    ("000", "001"),
                    ("011", "101"),
                    ("110", "111"),
                ],
                "max_queries": 5,
            },
            5: {
                "w": (0, 1, 1),
                "delta": 1,
                "target_pairs": [
                    ("000", "011"),
                    ("001", "010"),
                    ("100", "111"),
                    ("000", "001"),
                    ("010", "100"),
                    ("011", "110"),
                ],
                "max_queries": 5,
            },
        },
        "en": {
            1: {
                "w": (1, 0, 0),
                "delta": 0,
                "target_pairs": [
                    ("000", "001"),
                    ("010", "011"),
                    ("100", "101"),
                    ("000", "100"),
                    ("001", "101"),
                    ("010", "110"),
                ],
                "max_queries": 5,
            },
            2: {
                "w": (1, 1, 0),
                "delta": 0,
                "target_pairs": [
                    ("000", "011"),
                    ("001", "010"),
                    ("100", "111"),
                    ("000", "001"),
                    ("010", "100"),
                    ("011", "111"),
                ],
                "max_queries": 5,
            },
            3: {
                "w": (1, 0, 1),
                "delta": 1,
                "target_pairs": [
                    ("000", "010"),
                    ("001", "011"),
                    ("100", "110"),
                    ("000", "001"),
                    ("010", "011"),
                    ("100", "101"),
                ],
                "max_queries": 5,
            },
            4: {
                "w": (1, 1, 1),
                "delta": 0,
                "target_pairs": [
                    ("000", "011"),
                    ("001", "010"),
                    ("100", "111"),
                    ("000", "001"),
                    ("011", "101"),
                    ("110", "111"),
                ],
                "max_queries": 5,
            },
            5: {
                "w": (0, 1, 1),
                "delta": 1,
                "target_pairs": [
                    ("000", "011"),
                    ("001", "010"),
                    ("100", "111"),
                    ("000", "001"),
                    ("010", "100"),
                    ("011", "110"),
                ],
                "max_queries": 5,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self.w = cfg["w"]
        self.delta = cfg["delta"]
        
        self.target_pairs = cfg["target_pairs"]
        self.max_queries = cfg["max_queries"]
        
        if lang == "zh":
            pairs_str = "\n".join([f"  {i+1}. ({a}, {b})" for i, (a, b) in enumerate(self.target_pairs)])
        else:
            pairs_str = "\n".join([f"  {i+1}. ({a}, {b})" for i, (a, b) in enumerate(self.target_pairs)])
        
        self._game_info["target_pairs"] = pairs_str
        self._game_info["max_queries"] = self.max_queries
        
        self.target_pairs_set = set()
        for a, b in self.target_pairs:
            self.target_pairs_set.add(frozenset([a, b]))
        
        self.ground_truth = []
        for a, b in self.target_pairs:
            reachable = (self._compute_f(a) == self._compute_f(b))
            self.ground_truth.append(1 if reachable else 0)
        
        self.query_count = 0

    def _compute_f(self, x):
        x1, x2, x3 = int(x[0]), int(x[1]), int(x[2])
        result = (self.w[0] * x1) ^ (self.w[1] * x2) ^ (self.w[2] * x3) ^ self.delta
        return result

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        try:
            answers = [int(x.strip()) for x in raw_ans.split(",")]
        except:
            return False
        
        if len(answers) != 6:
            return False
        
        if not all(ans in [0, 1] for ans in answers):
            return False
        
        return answers == self.ground_truth

    def _cf_core_produce(self, parsed_info):
        if "query" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        if self.query_count >= self.max_queries:
            if self.config.language == "zh":
                return "错误：已达到最大查询次数限制。"
            else:
                return "Error: Maximum query limit reached."
        
        try:
            raw_query = parsed_info["query"].strip()
            parts = [x.strip() for x in raw_query.split(",")]
            if len(parts) != 2:
                raise ValueError("Invalid format")
            u, v = parts[0], parts[1]
        except:
            if self.config.language == "zh":
                return "错误：查询格式无效，应为 <query>u,v</query>。"
            else:
                return "Error: Invalid query format, should be <query>u,v</query>."
        
        valid_elements = {"000", "001", "010", "011", "100", "101", "110", "111"}
        if u not in valid_elements or v not in valid_elements:
            if self.config.language == "zh":
                return "错误：查询的元素必须是三位二进制串（000-111）。"
            else:
                return "Error: Query elements must be three-bit binary strings (000-111)."
        
        if u == v:
            if self.config.language == "zh":
                return "错误：不能查询相同的元素。"
            else:
                return "Error: Cannot query the same element."
        
        query_set = frozenset([u, v])
        if query_set in self.target_pairs_set:
            if self.config.language == "zh":
                return "错误：不能查询目标对中的任何一对。"
            else:
                return "Error: Cannot query any of the target pairs."
        
        self.query_count += 1
        
        f_u = self._compute_f(u)
        f_v = self._compute_f(v)
        
        if self.config.language == "zh":
            result = "是" if f_u == f_v else "否"
            return f"查询 {self.query_count}/{self.max_queries}：{result}"
        else:
            result = "Yes" if f_u == f_v else "No"
            return f"Query {self.query_count}/{self.max_queries}: {result}"

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        
        if "Yes" in correct:
            return correct.replace("Yes", "No")
        if "No" in correct:
            return correct.replace("No", "Yes")
        
        return correct + "_WRONG"

    def get_all_possible_queries(self):
        elements = ["{:03b}".format(i) for i in range(8)]
        results = []
        
        simulated_count = 1
        
        for u in elements:
            for v in elements:
                if u == v:
                    continue
                
                if frozenset([u, v]) in self.target_pairs_set:
                    continue
                
                f_u = self._compute_f(u)
                f_v = self._compute_f(v)
                
                if self.config.language == "zh":
                    result_val = "是" if f_u == f_v else "否"
                    answer_str = f"查询 {simulated_count}/{self.max_queries}：{result_val}"
                else:
                    result_val = "Yes" if f_u == f_v else "No"
                    answer_str = f"Query {simulated_count}/{self.max_queries}: {result_val}"
                
                results.append({
                    "query": f"<query>{u},{v}</query>",
                    "answer": answer_str
                })
                
        return results