import re
from .base import Game

class SymmetricDifferenceGame(Game):

    game_rule_zh = """\
我们来玩一个"对称差推理"游戏，规则如下：

游戏设定了一个编号集合 U = {{1, 2, ..., {n}}}。我已秘密设定了三个子集 A、B、C，它们都是 U 的子集。同时，我选定了一个目标集合 S，它必定是以下三者之一：
- A 与 B 的对称差（记为 AB 规则）
- B 与 C 的对称差（记为 BC 规则）
- A 与 C 的对称差（记为 AC 规则）

说明：两个集合的对称差是指恰好属于其中一个集合但不同时属于两个集合的所有元素。

你的目标是推断出目标集合 S 对应的规则类型（AB、BC 或 AC），并给出 S 的完整元素列表。

你可以进行以下查询：

1. 成员标记查询（不限次数）：询问某个编号 i 在三个子集 A、B、C 中的归属情况。我会返回三个布尔值，分别表示 i 是否属于 A、是否属于 B、是否属于 C。

2. 二元目标计数查询（最多 2 次）：询问两个不同的编号 i 和 j 中有多少个属于目标集合 S。我会返回一个整数（0、1 或 2）。

3. 提交最终答案：当你收集到足够信息后，提交你推断的规则类型和目标集合 S 的所有元素。

请尽可能少地使用查询次数来完成推理。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 成员标记查询（例如查询编号 3）：
<query_membership>3</query_membership>

- 二元目标计数查询（例如查询编号 2 和 5）：
<query_pair_count>2,5</query_pair_count>

- 提交最终答案时，必须说明规则类型（AB、BC 或 AC）并列出目标集合 S 的所有元素（用逗号隔开，顺序不限）：
<answer>rule=AB, elements=1,3,5</answer>

注意：若答案错误、格式不符或超出二元计数查询次数限制，游戏将失败。
"""

    game_rule_en = """\
Let's play a "Symmetric Difference Deduction" game. Here are the rules:

There is a set U = {{1, 2, ..., {n}}}. I have secretly defined three subsets A, B, and C, all of which are subsets of U. Additionally, I have selected a target set S, which must be one of the following:
- The symmetric difference of A and B (denoted as AB rule)
- The symmetric difference of B and C (denoted as BC rule)
- The symmetric difference of A and C (denoted as AC rule)

Note: The symmetric difference of two sets consists of all elements that belong to exactly one of the sets but not both.

Your goal is to infer which rule type (AB, BC, or AC) defines the target set S and provide the complete list of elements in S.

You can perform the following queries:

1. Membership Query (unlimited): Ask whether a specific element i belongs to each of the three subsets A, B, and C. I will return three boolean values indicating membership in A, B, and C respectively.

2. Pair Count Query (maximum 2 times): Ask how many of two distinct elements i and j belong to the target set S. I will return an integer (0, 1, or 2).

3. Submit Final Answer: When you have gathered enough information, submit your inferred rule type and all elements in the target set S.

Please use as few queries as possible to complete the deduction.

Each query must contain only one tag. Use the following XML format:

- Membership Query (e.g., querying element 3):
<query_membership>3</query_membership>

- Pair Count Query (e.g., querying elements 2 and 5):
<query_pair_count>2,5</query_pair_count>

- When submitting the final answer, specify the rule type (AB, BC, or AC) and list all elements in target set S (comma-separated, order does not matter):
<answer>rule=AB, elements=1,3,5</answer>

Note: The game will fail if the answer is incorrect, the format is invalid, or the pair count query limit is exceeded.
"""

    contextualized_rule_zh_1 = """\
智能交通管理系统启动。当前辖区内有编号为 1 到 {n} 的交通监控节点（集合 U）。
系统排查出三个具有特定交通状况的节点子集：A（早高峰拥堵节点）、B（事故高发节点）、C（违停高发节点）。
指挥中心已设定一个重点巡逻节点集合 S，该集合必定基于以下三种排查策略之一生成：
- A 与 B 的对称差（记为 AB 规则，即仅属早高峰拥堵或仅属事故高发，不同时具备两者的节点）
- B 与 C 的对称差（记为 BC 规则）
- A 与 C 的对称差（记为 AC 规则）

说明：两个集合的对称差是指恰好属于其中一个集合但不同时属于两个集合的所有元素。

你的目标是推断出重点巡逻集合 S 对应的规则类型（AB、BC 或 AC），并给出 S 的完整节点元素列表。

你可以进行以下查询：

1. 成员标记查询（不限次数）：询问某个编号 i 在三个子集 A、B、C 中的归属情况。我会返回三个布尔值，分别表示 i 是否属于 A、是否属于 B、是否属于 C。

2. 二元目标计数查询（最多 2 次）：询问两个不同的编号 i 和 j 中有多少个属于目标集合 S。我会返回一个整数（0、1 或 2）。

3. 提交最终答案：当你收集到足够信息后，提交你推断的规则类型和目标集合 S 的所有元素。

请尽可能少地使用查询次数来完成推理。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 成员标记查询（例如查询编号 3）：
<query_membership>3</query_membership>

- 二元目标计数查询（例如查询编号 2 和 5）：
<query_pair_count>2,5</query_pair_count>

- 提交最终答案时，必须说明规则类型（AB、BC 或 AC）并列出目标集合 S 的所有元素（用逗号隔开，顺序不限）：
<answer>rule=AB, elements=1,3,5</answer>

注意：若答案错误、格式不符或超出二元计数查询次数限制，游戏将失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Intelligent traffic management system initiated. There is a set of traffic monitoring nodes U = {{1, 2, ..., {n}}}.
The system has identified three subsets with specific traffic conditions: A (morning rush hour congestion), B (high accident frequency), and C (frequent illegal parking).
The command center has designated a priority patrol set S, which must be generated based on one of the following rules:
- The symmetric difference of A and B (denoted as AB rule)
- The symmetric difference of B and C (denoted as BC rule)
- The symmetric difference of A and C (denoted as AC rule)

Note: The symmetric difference of two sets consists of all elements that belong to exactly one of the sets but not both.

Your goal is to infer which rule type (AB, BC, or AC) defines the target set S and provide the complete list of elements in S.

You can perform the following queries:

1. Membership Query (unlimited): Ask whether a specific element i belongs to each of the three subsets A, B, and C. I will return three boolean values indicating membership in A, B, and C respectively.

2. Pair Count Query (maximum 2 times): Ask how many of two distinct elements i and j belong to the target set S. I will return an integer (0, 1, or 2).

3. Submit Final Answer: When you have gathered enough information, submit your inferred rule type and all elements in the target set S.

Please use as few queries as possible to complete the deduction.

Each query must contain only one tag. Use the following XML format:

- Membership Query (e.g., querying element 3):
<query_membership>3</query_membership>

- Pair Count Query (e.g., querying elements 2 and 5):
<query_pair_count>2,5</query_pair_count>

- When submitting the final answer, specify the rule type (AB, BC, or AC) and list all elements in target set S (comma-separated, order does not matter):
<answer>rule=AB, elements=1,3,5</answer>

Note: The game will fail if the answer is incorrect, the format is invalid, or the pair count query limit is exceeded.
"""

    contextualized_rule_zh_2 = """\
精准医疗诊断系统已就绪。当前有一个包含编号为 1 到 {n} 的基因位点集合 U。
病理分析排查出三个阳性标志物的位点子集：A（炎症标志物阳性）、B（自身抗体阳性）、C（异常蛋白表达）。
系统选定了一个用于确认罕见病变异的特异性靶点集合 S，它必定是以下三种机制之一：
- A 与 B 的对称差（记为 AB 规则，即仅具炎症或仅具抗体阳性，但不同时具备的位点）
- B 与 C 的对称差（记为 BC 规则）
- A 与 C 的对称差（记为 AC 规则）

说明：两个集合的对称差是指恰好属于其中一个集合但不同时属于两个集合的所有元素。

你的目标是推断出特异性靶点集合 S 对应的规则类型（AB、BC 或 AC），并给出 S 的完整位点元素列表。

你可以进行以下查询：

1. 成员标记查询（不限次数）：询问某个编号 i 在三个子集 A、B、C 中的归属情况。我会返回三个布尔值，分别表示 i 是否属于 A、是否属于 B、是否属于 C。

2. 二元目标计数查询（最多 2 次）：询问两个不同的编号 i 和 j 中有多少个属于目标集合 S。我会返回一个整数（0、1 或 2）。

3. 提交最终答案：当你收集到足够信息后，提交你推断的规则类型和目标集合 S 的所有元素。

请尽可能少地使用查询次数来完成推理。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 成员标记查询（例如查询编号 3）：
<query_membership>3</query_membership>

- 二元目标计数查询（例如查询编号 2 和 5）：
<query_pair_count>2,5</query_pair_count>

- 提交最终答案时，必须说明规则类型（AB、BC 或 AC）并列出目标集合 S 的所有元素（用逗号隔开，顺序不限）：
<answer>rule=AB, elements=1,3,5</answer>

注意：若答案错误、格式不符或超出二元计数查询次数限制，诊断将失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Precision medical diagnostic system is ready. There is a set of genetic loci U = {{1, 2, ..., {n}}}.
Pathological analysis has identified three subsets of positive markers: A (positive inflammatory markers), B (positive autoantibodies), and C (abnormal protein expression).
The system has selected a specific target set S for confirming a rare disease variant, which must be derived from one of the following mechanisms:
- The symmetric difference of A and B (denoted as AB rule)
- The symmetric difference of B and C (denoted as BC rule)
- The symmetric difference of A and C (denoted as AC rule)

Note: The symmetric difference of two sets consists of all elements that belong to exactly one of the sets but not both.

Your goal is to infer which rule type (AB, BC, or AC) defines the target set S and provide the complete list of elements in S.

You can perform the following queries:

1. Membership Query (unlimited): Ask whether a specific element i belongs to each of the three subsets A, B, and C. I will return three boolean values indicating membership in A, B, and C respectively.

2. Pair Count Query (maximum 2 times): Ask how many of two distinct elements i and j belong to the target set S. I will return an integer (0, 1, or 2).

3. Submit Final Answer: When you have gathered enough information, submit your inferred rule type and all elements in the target set S.

Please use as few queries as possible to complete the deduction.

Each query must contain only one tag. Use the following XML format:

- Membership Query (e.g., querying element 3):
<query_membership>3</query_membership>

- Pair Count Query (e.g., querying elements 2 and 5):
<query_pair_count>2,5</query_pair_count>

- When submitting the final answer, specify the rule type (AB, BC, or AC) and list all elements in target set S (comma-separated, order does not matter):
<answer>rule=AB, elements=1,3,5</answer>

Note: The diagnosis will fail if the answer is incorrect, the format is invalid, or the pair count query limit is exceeded.
"""

    contextualized_rule_zh_3 = """\
智能教研题库系统启动。当前考点库内有编号为 1 到 {n} 的候选题目集合 U。
教研组整理出三个特定维度的题目子集：A（历年易错题）、B（核心考点题）、C（压轴拓展题）。
为了保证测试的区分度，系统选定了一个期末冲刺特训卷题目集合 S，它必定是以下三种选题策略之一：
- A 与 B 的对称差（记为 AB 规则，即仅为易错题或仅为核心考点，不同时具备的边缘题）
- B 与 C 的对称差（记为 BC 规则）
- A 与 C 的对称差（记为 AC 规则）

说明：两个集合的对称差是指恰好属于其中一个集合但不同时属于两个集合的所有元素。

你的目标是推断出期末特训题目集合 S 对应的规则类型（AB、BC 或 AC），并给出 S 的完整题目元素列表。

你可以进行以下查询：

1. 成员标记查询（不限次数）：询问某个编号 i 在三个子集 A、B、C 中的归属情况。我会返回三个布尔值，分别表示 i 是否属于 A、是否属于 B、是否属于 C。

2. 二元目标计数查询（最多 2 次）：询问两个不同的编号 i 和 j 中有多少个属于目标集合 S。我会返回一个整数（0、1 或 2）。

3. 提交最终答案：当你收集到足够信息后，提交你推断的规则类型和目标集合 S 的所有元素。

请尽可能少地使用查询次数来完成推理。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 成员标记查询（例如查询编号 3）：
<query_membership>3</query_membership>

- 二元目标计数查询（例如查询编号 2 和 5）：
<query_pair_count>2,5</query_pair_count>

- 提交最终答案时，必须说明规则类型（AB、BC 或 AC）并列出目标集合 S 的所有元素（用逗号隔开，顺序不限）：
<answer>rule=AB, elements=1,3,5</answer>

注意：若答案错误、格式不符或超出二元计数查询次数限制，组卷将失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Intelligent educational question bank system initiated. There is a set of candidate questions U = {{1, 2, ..., {n}}}.
The teaching research team has compiled three subsets of questions based on specific dimensions: A (historically error-prone questions), B (core knowledge questions), and C (advanced extension questions).
To ensure the test's discriminative power, the system has selected a final sprint training set S, which must be derived from one of the following selection strategies:
- The symmetric difference of A and B (denoted as AB rule)
- The symmetric difference of B and C (denoted as BC rule)
- The symmetric difference of A and C (denoted as AC rule)

Note: The symmetric difference of two sets consists of all elements that belong to exactly one of the sets but not both.

Your goal is to infer which rule type (AB, BC, or AC) defines the target set S and provide the complete list of elements in S.

You can perform the following queries:

1. Membership Query (unlimited): Ask whether a specific element i belongs to each of the three subsets A, B, and C. I will return three boolean values indicating membership in A, B, and C respectively.

2. Pair Count Query (maximum 2 times): Ask how many of two distinct elements i and j belong to the target set S. I will return an integer (0, 1, or 2).

3. Submit Final Answer: When you have gathered enough information, submit your inferred rule type and all elements in the target set S.

Please use as few queries as possible to complete the deduction.

Each query must contain only one tag. Use the following XML format:

- Membership Query (e.g., querying element 3):
<query_membership>3</query_membership>

- Pair Count Query (e.g., querying elements 2 and 5):
<query_pair_count>2,5</query_pair_count>

- When submitting the final answer, specify the rule type (AB, BC, or AC) and list all elements in target set S (comma-separated, order does not matter):
<answer>rule=AB, elements=1,3,5</answer>

Note: The paper generation will fail if the answer is incorrect, the format is invalid, or the pair count query limit is exceeded.
"""

    contextualized_rule_zh_4 = """\
自动化质检系统启动。当前流水线有一批编号为 1 到 {n} 的生产批次集合 U。
经过多重工艺检测，标记出三个存在缺陷特征的批次子集：A（尺寸偏差）、B（材质硬度不足）、C（表面涂层受损）。
质检中心设定了一个触发回炉重造流程的目标批次集合 S，该集合针对的是具备单一缺陷特征的批次，它必定是以下三者之一：
- A 与 B 的对称差（记为 AB 规则，即仅具尺寸偏差或仅具硬度不足的批次）
- B 与 C 的对称差（记为 BC 规则）
- A 与 C 的对称差（记为 AC 规则）

说明：两个集合的对称差是指恰好属于其中一个集合但不同时属于两个集合的所有元素。

你的目标是推断出回炉重造集合 S 对应的规则类型（AB、BC 或 AC），并给出 S 的完整批次元素列表。

你可以进行以下查询：

1. 成员标记查询（不限次数）：询问某个编号 i 在三个子集 A、B、C 中的归属情况。我会返回三个布尔值，分别表示 i 是否属于 A、是否属于 B、是否属于 C。

2. 二元目标计数查询（最多 2 次）：询问两个不同的编号 i 和 j 中有多少个属于目标集合 S。我会返回一个整数（0、1 或 2）。

3. 提交最终答案：当你收集到足够信息后，提交你推断的规则类型和目标集合 S 的所有元素。

请尽可能少地使用查询次数来完成推理。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 成员标记查询（例如查询编号 3）：
<query_membership>3</query_membership>

- 二元目标计数查询（例如查询编号 2 和 5）：
<query_pair_count>2,5</query_pair_count>

- 提交最终答案时，必须说明规则类型（AB、BC 或 AC）并列出目标集合 S 的所有元素（用逗号隔开，顺序不限）：
<answer>rule=AB, elements=1,3,5</answer>

注意：若答案错误、格式不符或超出二元计数查询次数限制，质检将失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Automated quality inspection system initiated. There is a set of production batches U = {{1, 2, ..., {n}}} on the assembly line.
Through multiple process inspections, three subsets of batches with defect features have been identified: A (dimensional deviation), B (insufficient material hardness), and C (damaged surface coating).
The quality control center has designated a target batch set S that triggers the remanufacturing process, which must be one of the following:
- The symmetric difference of A and B (denoted as AB rule)
- The symmetric difference of B and C (denoted as BC rule)
- The symmetric difference of A and C (denoted as AC rule)

Note: The symmetric difference of two sets consists of all elements that belong to exactly one of the sets but not both.

Your goal is to infer which rule type (AB, BC, or AC) defines the target set S and provide the complete list of elements in S.

You can perform the following queries:

1. Membership Query (unlimited): Ask whether a specific element i belongs to each of the three subsets A, B, and C. I will return three boolean values indicating membership in A, B, and C respectively.

2. Pair Count Query (maximum 2 times): Ask how many of two distinct elements i and j belong to the target set S. I will return an integer (0, 1, or 2).

3. Submit Final Answer: When you have gathered enough information, submit your inferred rule type and all elements in the target set S.

Please use as few queries as possible to complete the deduction.

Each query must contain only one tag. Use the following XML format:

- Membership Query (e.g., querying element 3):
<query_membership>3</query_membership>

- Pair Count Query (e.g., querying elements 2 and 5):
<query_pair_count>2,5</query_pair_count>

- When submitting the final answer, specify the rule type (AB, BC, or AC) and list all elements in target set S (comma-separated, order does not matter):
<answer>rule=AB, elements=1,3,5</answer>

Note: The inspection will fail if the answer is incorrect, the format is invalid, or the pair count query limit is exceeded.
"""

    contextualized_rule_zh_5 = """\
智能合规审查系统启动。当前案件包含编号为 1 到 {n} 的待审查合同条款集合 U。
AI法务排查出三个具有法律风险的条款子集：A（违约责任不明确）、B（知识产权侵权风险）、C（商业秘密泄露隐患）。
系统需要移交高级法务委员会一个核心审查条款集合 S，该审查针对的是存在单一争议的条款，它必定是以下三者之一：
- A 与 B 的对称差（记为 AB 规则，即仅存违约责任模糊或仅存知识产权风险的条款）
- B 与 C 的对称差（记为 BC 规则）
- A 与 C 的对称差（记为 AC 规则）

说明：两个集合的对称差是指恰好属于其中一个集合但不同时属于两个集合的所有元素。

你的目标是推断出核心审查集合 S 对应的规则类型（AB、BC 或 AC），并给出 S 的完整条款元素列表。

你可以进行以下查询：

1. 成员标记查询（不限次数）：询问某个编号 i 在三个子集 A、B、C 中的归属情况。我会返回三个布尔值，分别表示 i 是否属于 A、是否属于 B、是否属于 C。

2. 二元目标计数查询（最多 2 次）：询问两个不同的编号 i 和 j 中有多少个属于目标集合 S。我会返回一个整数（0、1 或 2）。

3. 提交最终答案：当你收集到足够信息后，提交你推断的规则类型和目标集合 S 的所有元素。

请尽可能少地使用查询次数来完成推理。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 成员标记查询（例如查询编号 3）：
<query_membership>3</query_membership>

- 二元目标计数查询（例如查询编号 2 和 5）：
<query_pair_count>2,5</query_pair_count>

- 提交最终答案时，必须说明规则类型（AB、BC 或 AC）并列出目标集合 S 的所有元素（用逗号隔开，顺序不限）：
<answer>rule=AB, elements=1,3,5</answer>

注意：若答案错误、格式不符或超出二元计数查询次数限制，审查流转将失败。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Intelligent compliance review system initiated. The current case involves a set of contract clauses pending review U = {{1, 2, ..., {n}}}.
The AI legal assistant has identified three subsets of clauses with legal risks: A (ambiguous breach liabilities), B (intellectual property infringement risks), and C (trade secret leakage hazards).
The system needs to escalate a core review clause set S to the senior legal committee, which must be derived from one of the following logic mechanisms:
- The symmetric difference of A and B (denoted as AB rule)
- The symmetric difference of B and C (denoted as BC rule)
- The symmetric difference of A and C (denoted as AC rule)

Note: The symmetric difference of two sets consists of all elements that belong to exactly one of the sets but not both.

Your goal is to infer which rule type (AB, BC, or AC) defines the target set S and provide the complete list of elements in S.

You can perform the following queries:

1. Membership Query (unlimited): Ask whether a specific element i belongs to each of the three subsets A, B, and C. I will return three boolean values indicating membership in A, B, and C respectively.

2. Pair Count Query (maximum 2 times): Ask how many of two distinct elements i and j belong to the target set S. I will return an integer (0, 1, or 2).

3. Submit Final Answer: When you have gathered enough information, submit your inferred rule type and all elements in the target set S.

Please use as few queries as possible to complete the deduction.

Each query must contain only one tag. Use the following XML format:

- Membership Query (e.g., querying element 3):
<query_membership>3</query_membership>

- Pair Count Query (e.g., querying elements 2 and 5):
<query_pair_count>2,5</query_pair_count>

- When submitting the final answer, specify the rule type (AB, BC, or AC) and list all elements in target set S (comma-separated, order does not matter):
<answer>rule=AB, elements=1,3,5</answer>

Note: The system review will fail if the answer is incorrect, the format is invalid, or the pair count query limit is exceeded.
"""

    tags = ["answer", "query_membership", "query_pair_count"]
    
    reasoning_type = "溯因推理"
    data_structure = "集合"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "set_A": [1, 2],
                "set_B": [2, 3],
                "set_C": [3, 4],
                "rule_type": "AB",
            },
            2: {
                "n": 6,
                "set_A": [1, 2, 3],
                "set_B": [2, 4, 5],
                "set_C": [3, 5, 6],
                "rule_type": "BC",
            },
            3: {
                "n": 8,
                "set_A": [1, 2, 4, 5],
                "set_B": [2, 3, 5, 6],
                "set_C": [1, 3, 6, 7],
                "rule_type": "AC",
            },
            4: {
                "n": 10,
                "set_A": [1, 2, 3, 5, 7],
                "set_B": [2, 4, 5, 6, 8],
                "set_C": [1, 3, 6, 8, 9],
                "rule_type": "AB",
            },
            5: {
                "n": 12,
                "set_A": [1, 2, 4, 5, 7, 9, 10],
                "set_B": [2, 3, 5, 6, 8, 10, 11],
                "set_C": [1, 3, 4, 6, 7, 11, 12],
                "rule_type": "BC",
            },
        },
        "en": {
            1: {
                "n": 5,
                "set_A": [1, 2],
                "set_B": [2, 3],
                "set_C": [3, 4],
                "rule_type": "AB",
            },
            2: {
                "n": 6,
                "set_A": [1, 2, 3],
                "set_B": [2, 4, 5],
                "set_C": [3, 5, 6],
                "rule_type": "BC",
            },
            3: {
                "n": 8,
                "set_A": [1, 2, 4, 5],
                "set_B": [2, 3, 5, 6],
                "set_C": [1, 3, 6, 7],
                "rule_type": "AC",
            },
            4: {
                "n": 10,
                "set_A": [1, 2, 3, 5, 7],
                "set_B": [2, 4, 5, 6, 8],
                "set_C": [1, 3, 6, 8, 9],
                "rule_type": "AB",
            },
            5: {
                "n": 12,
                "set_A": [1, 2, 4, 5, 7, 9, 10],
                "set_B": [2, 3, 5, 6, 8, 10, 11],
                "set_C": [1, 3, 4, 6, 7, 11, 12],
                "rule_type": "BC",
            },
        },
    }

    def __init__(self, config):
        self.pair_count_queries_used = 0
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        
        self.set_A = set(cfg["set_A"])
        self.set_B = set(cfg["set_B"])
        self.set_C = set(cfg["set_C"])
        
        self.rule_type = cfg["rule_type"]
        
        if self.rule_type == "AB":
            self.target_set = self.set_A.symmetric_difference(self.set_B)
        elif self.rule_type == "BC":
            self.target_set = self.set_B.symmetric_difference(self.set_C)
        elif self.rule_type == "AC":
            self.target_set = self.set_A.symmetric_difference(self.set_C)
        else:
            raise ValueError(f"Unknown rule type: {self.rule_type}")

    def evaluate(self, parsed_info):
        raw_ans = parsed_info.get("answer", "")
        
        rule_match = re.search(r'rule\s*=\s*(\w+)', raw_ans, re.IGNORECASE)
        elements_match = re.search(r'elements\s*=\s*([\d\s,]+)', raw_ans, re.IGNORECASE)
        
        if not rule_match or not elements_match:
            return False
        
        rule_val = rule_match.group(1).strip().upper()
        if rule_val != self.rule_type.upper():
            return False
        
        try:
            elements_str = elements_match.group(1).strip()
            model_elements = set(int(x.strip()) for x in elements_str.split(",") if x.strip())
        except (ValueError, TypeError):
            return False
        
        return model_elements == self.target_set

    def produce_response(self, parsed_info):
        if getattr(self, "enable_counterfactual", False):
            self._cf_round_counter += 1

            if self._cf_round_counter == 2:
                saved_count = self.pair_count_queries_used
                correct = self._cf_core_produce(parsed_info)
                self.pair_count_queries_used = saved_count
                self._cf_correct_resp = correct
                self._cf_wrong_resp = self._cf_make_wrong(correct)
                return self._cf_wrong_resp

            elif self._cf_round_counter == 3:
                return self._cf_correction_message()

        return self._cf_core_produce(parsed_info)

    def _cf_core_produce(self, parsed_info):
        n = self._game_info["n"]
        
        if "query_membership" in parsed_info:
            try:
                idx = int(parsed_info["query_membership"].strip())
                if idx < 1 or idx > n:
                    return "错误：编号超出范围。" if self.config.language == "zh" else "Error: ID out of range."
                
                in_A = idx in self.set_A
                in_B = idx in self.set_B
                in_C = idx in self.set_C
                
                if self.config.language == "zh":
                    return f"A: {'是' if in_A else '否'}, B: {'是' if in_B else '否'}, C: {'是' if in_C else '否'}"
                else:
                    return f"A: {'Yes' if in_A else 'No'}, B: {'Yes' if in_B else 'No'}, C: {'Yes' if in_C else 'No'}"
            except (ValueError, TypeError):
                return "错误：格式无效。" if self.config.language == "zh" else "Error: Invalid format."
        
        elif "query_pair_count" in parsed_info:
            if self.pair_count_queries_used >= 2:
                error_msg = ("错误：二元目标计数查询次数已达上限（2次）。" 
                             if self.config.language == "zh" 
                             else "Error: Pair count query limit reached (2 times).")
                raise ValueError(error_msg)
            
            try:
                raw = parsed_info["query_pair_count"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError("Need exactly 2 parts")
                
                i, j = int(parts[0]), int(parts[1])
                
                if i < 1 or i > n or j < 1 or j > n:
                    return "错误：编号超出范围。" if self.config.language == "zh" else "Error: ID out of range."
                
                if i == j:
                    return "错误：两个编号必须不同。" if self.config.language == "zh" else "Error: The two IDs must be different."
                
                count = (i in self.target_set) + (j in self.target_set)
                
                self.pair_count_queries_used += 1
                
                return str(count)
            except (ValueError, TypeError):
                return "错误：格式无效或编号错误。" if self.config.language == "zh" else "Error: Invalid format or ID."
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        import random as _rand
        
        if correct.isdigit():
            val = int(correct)
            candidates = [x for x in [0, 1, 2] if x != val]
            if candidates:
                return str(_rand.choice(candidates))
            return str(val + 1)
        
        if self.config.language == "zh":
            if "是" in correct or "否" in correct:
                return correct.replace("是", "TEMP").replace("否", "是").replace("TEMP", "否")
        else:
            if "Yes" in correct or "No" in correct:
                return correct.replace("Yes", "TEMP").replace("No", "Yes").replace("TEMP", "No")
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        n = self._game_info["n"]
        results = []

        for i in range(1, n + 1):
            query_content = str(i)
            query_xml = f"<query_membership>{query_content}</query_membership>"
            
            in_A = i in self.set_A
            in_B = i in self.set_B
            in_C = i in self.set_C
            
            if self.config.language == "zh":
                ans = f"A: {'是' if in_A else '否'}, B: {'是' if in_B else '否'}, C: {'是' if in_C else '否'}"
            else:
                ans = f"A: {'Yes' if in_A else 'No'}, B: {'Yes' if in_B else 'No'}, C: {'Yes' if in_C else 'No'}"
            
            results.append({"query": query_xml, "answer": ans})

        pair_count = 0
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                if pair_count >= 2:
                    break
                
                query_content = f"{i},{j}"
                query_xml = f"<query_pair_count>{query_content}</query_pair_count>"
                
                count = (i in self.target_set) + (j in self.target_set)
                ans = str(count)
                
                results.append({"query": query_xml, "answer": ans})
                pair_count += 1
            
            if pair_count >= 2:
                break

        return results