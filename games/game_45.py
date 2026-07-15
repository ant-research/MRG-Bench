from .base import Game
import random
import itertools

class SetDisjointnessGame(Game):

    contextualized_rule_zh_1 = """\
我们现在来玩一个"交通路网无冲突推理"系统测试，规则如下：

系统设定了一个包含 {n} 个关键交通枢纽的有限集合。现在有 {m} 条通行路线（对象），每条路线都关联一个长度为 {n} 的二进制串。二进制串的每一位（0或1）代表该路线是否占用对应的关键交通枢纽资源。

【通行路线信息】
{objects_info}

我设定了一个判定规则，可以对任意两条路线进行判断，返回两种结果之一："不相交"（路线完全无冲突）或 "有交集"（路线存在枢纽资源冲突）。你的任务是通过有限次测试，推断出这个判定规则的本质，并对未测试过的路线对进行正确预测。

你可以进行以下操作：

1. 单对测试（会消耗测试次数）
   询问任意两条路线的关系，我会告诉你它们的资源占用是"不相交"还是"有交集"。

2. 查询剩余测试次数（不消耗次数）
   询问你还可以进行多少次测试。

3. 查询历史测试记录（不消耗次数）
   查看你已经测试过的所有路线对及其结果。

4. 提交最终预测（不消耗次数）
   当你认为已经掌握了判定规则后，对 {k} 对未测试过的路线对进行预测。

【重要提示】
- 你需要在尽可能少的测试次数内完成任务
- 最终提交时必须预测恰好 {k} 对未测试过的路线对
- 所有预测必须全部正确才能获胜

每次只能包含一个操作标签：

- 单对测试（例如测试对象 C1 和 C3）：
<test>C1,C3</test>

- 查询剩余测试次数：
<query_quota></query_quota>

- 查询历史测试记录：
<query_history></query_history>

- 提交最终预测（必须恰好 {k} 对，每对一行）：
<answer>
C1,C2=不相交
C3,C4=有交集
C5,C6=不相交
C2,C5=有交集
C1,C4=不相交
C3,C5=有交集
</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play a "Traffic Network Conflict Inference" system test. Here are the rules:

The system involves a finite set containing {n} key traffic hubs. There are {m} transit routes (objects), each associated with a binary string of length {n}. Each bit (0 or 1) in the binary string represents whether the route occupies a specific traffic hub resource.

【Route Information】
{objects_info}

I have established a judgment rule that can evaluate any two routes and return one of two results: "disjoint" (completely conflict-free) or "intersecting" (having resource conflicts). Your task is to infer the essence of this judgment rule through limited tests and make correct predictions for untested route pairs.

You can perform the following operations:

1. Pairwise Test (consumes test quota)
   Ask about the relationship between any two routes, and I will tell you whether their resource occupations are "disjoint" or "intersecting".

2. Query Remaining Test Quota (does not consume quota)
   Ask how many tests you can still perform.

3. Query Test History (does not consume quota)
   View all route pairs you have tested and their results.

4. Submit Final Prediction (does not consume quota)
   When you believe you have mastered the judgment rule, predict {k} untested route pairs.

【Important Notes】
- You need to complete the task with as few tests as possible
- Final submission must predict exactly {k} untested route pairs
- All predictions must be completely correct to win

Each operation must contain only one tag:

- Pairwise Test (e.g., testing objects C1 and C3):
<test>C1,C3</test>

- Query Remaining Test Quota:
<query_quota></query_quota>

- Query Test History:
<query_history></query_history>

- Submit Final Prediction (must be exactly {k} pairs, one per line):
<answer>
C1,C2=disjoint
C3,C4=intersecting
C5,C6=disjoint
C2,C5=intersecting
C1,C4=disjoint
C3,C5=intersecting
</answer>
"""

    contextualized_rule_zh_2 = """\
我们现在来玩一个"医疗药物相互作用推理"系统测试，规则如下：

系统设定了一个包含 {n} 个潜在副作用靶点的有限集合。现在有 {m} 种治疗药物（对象），每种药物都关联一个长度为 {n} 的二进制串。二进制串的每一位（0或1）代表该药物是否作用于对应的靶点。

【药物信息】
{objects_info}

我设定了一个判定规则，可以对任意两种药物进行判断，返回两种结果之一："不相交"（无共同副作用靶点，联合用药安全）或 "有交集"（存在共同靶点，有相互作用风险）。你的任务是通过有限次测试，推断出这个判定规则的本质，并对未测试过的药物对进行正确预测。

你可以进行以下操作：

1. 单对测试（会消耗测试次数）
   询问任意两种药物的关系，我会告诉你它们的副作用靶点是"不相交"还是"有交集"。

2. 查询剩余测试次数（不消耗次数）
   询问你还可以进行多少次测试。

3. 查询历史测试记录（不消耗次数）
   查看你已经测试过的所有药物对及其结果。

4. 提交最终预测（不消耗次数）
   当你认为已经掌握了判定规则后，对 {k} 对未测试过的药物对进行预测。

【重要提示】
- 你需要在尽可能少的测试次数内完成任务
- 最终提交时必须预测恰好 {k} 对未测试过的药物对
- 所有预测必须全部正确才能获胜

每次只能包含一个操作标签：

- 单对测试（例如测试对象 C1 和 C3）：
<test>C1,C3</test>

- 查询剩余测试次数：
<query_quota></query_quota>

- 查询历史测试记录：
<query_history></query_history>

- 提交最终预测（必须恰好 {k} 对，每对一行）：
<answer>
C1,C2=不相交
C3,C4=有交集
C5,C6=不相交
C2,C5=有交集
C1,C4=不相交
C3,C5=有交集
</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Medical Drug Interaction Inference" system test. Here are the rules:

The system involves a finite set containing {n} potential side-effect targets. There are {m} therapeutic drugs (objects), each associated with a binary string of length {n}. Each bit (0 or 1) in the binary string represents whether the drug acts on the specific target.

【Drug Information】
{objects_info}

I have established a judgment rule that can evaluate any two drugs and return one of two results: "disjoint" (no common side-effect targets, safe for combined use) or "intersecting" (having common targets, interaction risk exists). Your task is to infer the essence of this judgment rule through limited tests and make correct predictions for untested drug pairs.

You can perform the following operations:

1. Pairwise Test (consumes test quota)
   Ask about the relationship between any two drugs, and I will tell you whether their side-effect targets are "disjoint" or "intersecting".

2. Query Remaining Test Quota (does not consume quota)
   Ask how many tests you can still perform.

3. Query Test History (does not consume quota)
   View all drug pairs you have tested and their results.

4. Submit Final Prediction (does not consume quota)
   When you believe you have mastered the judgment rule, predict {k} untested drug pairs.

【Important Notes】
- You need to complete the task with as few tests as possible
- Final submission must predict exactly {k} untested drug pairs
- All predictions must be completely correct to win

Each operation must contain only one tag:

- Pairwise Test (e.g., testing objects C1 and C3):
<test>C1,C3</test>

- Query Remaining Test Quota:
<query_quota></query_quota>

- Query Test History:
<query_history></query_history>

- Submit Final Prediction (must be exactly {k} pairs, one per line):
<answer>
C1,C2=disjoint
C3,C4=intersecting
C5,C6=disjoint
C2,C5=intersecting
C1,C4=disjoint
C3,C5=intersecting
</answer>
"""

    contextualized_rule_zh_3 = """\
我们现在来玩一个"教育知识点覆盖推理"系统测试，规则如下：

系统设定了一个包含 {n} 个核心基础概念的有限集合。现在有 {m} 个课程模块（对象），每个模块都关联一个长度为 {n} 的二进制串。二进制串的每一位（0或1）代表该课程模块是否依赖对应的前置概念。

【课程模块信息】
{objects_info}

我设定了一个判定规则，可以对任意两个课程模块进行判断，返回两种结果之一："不相交"（无共同的基础概念依赖）或 "有交集"（共享某些基础概念）。你的任务是通过有限次测试，推断出这个判定规则的本质，并对未测试过的模块对进行正确预测。

你可以进行以下操作：

1. 单对测试（会消耗测试次数）
   询问任意两个课程模块的关系，我会告诉你它们的基础概念依赖是"不相交"还是"有交集"。

2. 查询剩余测试次数（不消耗次数）
   询问你还可以进行多少次测试。

3. 查询历史测试记录（不消耗次数）
   查看你已经测试过的所有模块对及其结果。

4. 提交最终预测（不消耗次数）
   当你认为已经掌握了判定规则后，对 {k} 对未测试过的模块对进行预测。

【重要提示】
- 你需要在尽可能少的测试次数内完成任务
- 最终提交时必须预测恰好 {k} 对未测试过的模块对
- 所有预测必须全部正确才能获胜

每次只能包含一个操作标签：

- 单对测试（例如测试对象 C1 和 C3）：
<test>C1,C3</test>

- 查询剩余测试次数：
<query_quota></query_quota>

- 查询历史测试记录：
<query_history></query_history>

- 提交最终预测（必须恰好 {k} 对，每对一行）：
<answer>
C1,C2=不相交
C3,C4=有交集
C5,C6=不相交
C2,C5=有交集
C1,C4=不相交
C3,C5=有交集
</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play an "Educational Knowledge Coverage Inference" system test. Here are the rules:

The system involves a finite set containing {n} core foundational concepts. There are {m} course modules (objects), each associated with a binary string of length {n}. Each bit (0 or 1) in the binary string represents whether the course module relies on the specific prerequisite concept.

【Course Module Information】
{objects_info}

I have established a judgment rule that can evaluate any two course modules and return one of two results: "disjoint" (no common foundational concepts) or "intersecting" (sharing certain foundational concepts). Your task is to infer the essence of this judgment rule through limited tests and make correct predictions for untested module pairs.

You can perform the following operations:

1. Pairwise Test (consumes test quota)
   Ask about the relationship between any two course modules, and I will tell you whether their foundational concepts are "disjoint" or "intersecting".

2. Query Remaining Test Quota (does not consume quota)
   Ask how many tests you can still perform.

3. Query Test History (does not consume quota)
   View all module pairs you have tested and their results.

4. Submit Final Prediction (does not consume quota)
   When you believe you have mastered the judgment rule, predict {k} untested module pairs.

【Important Notes】
- You need to complete the task with as few tests as possible
- Final submission must predict exactly {k} untested module pairs
- All predictions must be completely correct to win

Each operation must contain only one tag:

- Pairwise Test (e.g., testing objects C1 and C3):
<test>C1,C3</test>

- Query Remaining Test Quota:
<query_quota></query_quota>

- Query Test History:
<query_history></query_history>

- Submit Final Prediction (must be exactly {k} pairs, one per line):
<answer>
C1,C2=disjoint
C3,C4=intersecting
C5,C6=disjoint
C2,C5=intersecting
C1,C4=disjoint
C3,C5=intersecting
</answer>
"""

    contextualized_rule_zh_4 = """\
我们现在来玩一个"工业生产设备排期推理"系统测试，规则如下：

系统设定了一个包含 {n} 种底层共享模具/设备的有限集合。现在有 {m} 个生产工序（对象），每个工序都关联一个长度为 {n} 的二进制串。二进制串的每一位（0或1）代表该工序是否需要调用对应的设备资源。

【生产工序信息】
{objects_info}

我设定了一个判定规则，可以对任意两个生产工序进行判断，返回两种结果之一："不相交"（无设备资源冲突，可并行）或 "有交集"（存在设备冲突，须串行）。你的任务是通过有限次测试，推断出这个判定规则的本质，并对未测试过的工序对进行正确预测。

你可以进行以下操作：

1. 单对测试（会消耗测试次数）
   询问任意两个生产工序的关系，我会告诉你它们的设备资源是"不相交"还是"有交集"。

2. 查询剩余测试次数（不消耗次数）
   询问你还可以进行多少次测试。

3. 查询历史测试记录（不消耗次数）
   查看你已经测试过的所有工序对及其结果。

4. 提交最终预测（不消耗次数）
   当你认为已经掌握了判定规则后，对 {k} 对未测试过的工序对进行预测。

【重要提示】
- 你需要在尽可能少的测试次数内完成任务
- 最终提交时必须预测恰好 {k} 对未测试过的工序对
- 所有预测必须全部正确才能获胜

每次只能包含一个操作标签：

- 单对测试（例如测试对象 C1 和 C3）：
<test>C1,C3</test>

- 查询剩余测试次数：
<query_quota></query_quota>

- 查询历史测试记录：
<query_history></query_history>

- 提交最终预测（必须恰好 {k} 对，每对一行）：
<answer>
C1,C2=不相交
C3,C4=有交集
C5,C6=不相交
C2,C5=有交集
C1,C4=不相交
C3,C5=有交集
</answer>
"""

    contextualized_rule_en_4 = """\
[Industry Scenario]
Let's play an "Industrial Production Equipment Scheduling Inference" system test. Here are the rules:

The system involves a finite set containing {n} underlying shared molds/equipment. There are {m} production processes (objects), each associated with a binary string of length {n}. Each bit (0 or 1) in the binary string represents whether the process requires the specific equipment resource.

【Production Process Information】
{objects_info}

I have established a judgment rule that can evaluate any two production processes and return one of two results: "disjoint" (no equipment conflict, can be parallelized) or "intersecting" (equipment conflict exists, must be serialized). Your task is to infer the essence of this judgment rule through limited tests and make correct predictions for untested process pairs.

You can perform the following operations:

1. Pairwise Test (consumes test quota)
   Ask about the relationship between any two production processes, and I will tell you whether their equipment resources are "disjoint" or "intersecting".

2. Query Remaining Test Quota (does not consume quota)
   Ask how many tests you can still perform.

3. Query Test History (does not consume quota)
   View all process pairs you have tested and their results.

4. Submit Final Prediction (does not consume quota)
   When you believe you have mastered the judgment rule, predict {k} untested process pairs.

【Important Notes】
- You need to complete the task with as few tests as possible
- Final submission must predict exactly {k} untested process pairs
- All predictions must be completely correct to win

Each operation must contain only one tag:

- Pairwise Test (e.g., testing objects C1 and C3):
<test>C1,C3</test>

- Query Remaining Test Quota:
<query_quota></query_quota>

- Query Test History:
<query_history></query_history>

- Submit Final Prediction (must be exactly {k} pairs, one per line):
<answer>
C1,C2=disjoint
C3,C4=intersecting
C5,C6=disjoint
C2,C5=intersecting
C1,C4=disjoint
C3,C5=intersecting
</answer>
"""

    contextualized_rule_zh_5 = """\
我们现在来玩一个"法律条款适用范围推理"系统测试，规则如下：

系统设定了一个包含 {n} 种核心免责情形/管辖权的有限集合。现在有 {m} 项法律条款草案（对象），每项条款都关联一个长度为 {n} 的二进制串。二进制串的每一位（0或1）代表该条款是否适用于对应的情形或管辖权。

【法律条款信息】
{objects_info}

我设定了一个判定规则，可以对任意两项法律条款进行判断，返回两种结果之一："不相交"（管辖范围完全无重叠）或 "有交集"（管辖范围存在重叠/冲突）。你的任务是通过有限次测试，推断出这个判定规则的本质，并对未测试过的条款对进行正确预测。

你可以进行以下操作：

1. 单对测试（会消耗测试次数）
   询问任意两项法律条款的关系，我会告诉你它们的适用范围是"不相交"还是"有交集"。

2. 查询剩余测试次数（不消耗次数）
   询问你还可以进行多少次测试。

3. 查询历史测试记录（不消耗次数）
   查看你已经测试过的所有条款对及其结果。

4. 提交最终预测（不消耗次数）
   当你认为已经掌握了判定规则后，对 {k} 对未测试过的条款对进行预测。

【重要提示】
- 你需要在尽可能少的测试次数内完成任务
- 最终提交时必须预测恰好 {k} 对未测试过的条款对
- 所有预测必须全部正确才能获胜

每次只能包含一个操作标签：

- 单对测试（例如测试对象 C1 和 C3）：
<test>C1,C3</test>

- 查询剩余测试次数：
<query_quota></query_quota>

- 查询历史测试记录：
<query_history></query_history>

- 提交最终预测（必须恰好 {k} 对，每对一行）：
<answer>
C1,C2=不相交
C3,C4=有交集
C5,C6=不相交
C2,C5=有交集
C1,C4=不相交
C3,C5=有交集
</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "Legal Clause Applicability Scope Inference" system test. Here are the rules:

The system involves a finite set containing {n} core exemption scenarios/jurisdictions. There are {m} legal clause drafts (objects), each associated with a binary string of length {n}. Each bit (0 or 1) in the binary string represents whether the clause applies to the specific scenario or jurisdiction.

【Legal Clause Information】
{objects_info}

I have established a judgment rule that can evaluate any two legal clauses and return one of two results: "disjoint" (jurisdictional scopes are completely non-overlapping) or "intersecting" (jurisdictional scopes overlap/conflict). Your task is to infer the essence of this judgment rule through limited tests and make correct predictions for untested clause pairs.

You can perform the following operations:

1. Pairwise Test (consumes test quota)
   Ask about the relationship between any two legal clauses, and I will tell you whether their applicability scopes are "disjoint" or "intersecting".

2. Query Remaining Test Quota (does not consume quota)
   Ask how many tests you can still perform.

3. Query Test History (does not consume quota)
   View all clause pairs you have tested and their results.

4. Submit Final Prediction (does not consume quota)
   When you believe you have mastered the judgment rule, predict {k} untested clause pairs.

【Important Notes】
- You need to complete the task with as few tests as possible
- Final submission must predict exactly {k} untested clause pairs
- All predictions must be completely correct to win

Each operation must contain only one tag:

- Pairwise Test (e.g., testing objects C1 and C3):
<test>C1,C3</test>

- Query Remaining Test Quota:
<query_quota></query_quota>

- Query Test History:
<query_history></query_history>

- Submit Final Prediction (must be exactly {k} pairs, one per line):
<answer>
C1,C2=disjoint
C3,C4=intersecting
C5,C6=disjoint
C2,C5=intersecting
C1,C4=disjoint
C3,C5=intersecting
</answer>
"""

    game_rule_zh = """\
我们现在来玩一个"集合关系推理"游戏，规则如下：

游戏设定了一个包含 {n} 个元素的有限集合。现在有 {m} 个对象，每个对象都关联一个长度为 {n} 的二进制串。二进制串的每一位（0或1）代表某种内部属性。

【对象信息】
{objects_info}

我设定了一个判定规则，可以对任意两个对象进行判断，返回两种结果之一："不相交" 或 "有交集"。你的任务是通过有限次测试，推断出这个判定规则的本质，并对未测试过的对象对进行正确预测。

你可以进行以下操作：

1. 单对测试（会消耗测试次数）
   询问任意两个对象的关系，我会告诉你它们是"不相交"还是"有交集"。

2. 查询剩余测试次数（不消耗次数）
   询问你还可以进行多少次测试。

3. 查询历史测试记录（不消耗次数）
   查看你已经测试过的所有对象对及其结果。

4. 提交最终预测（不消耗次数）
   当你认为已经掌握了判定规则后，对 {k} 对未测试过的对象对进行预测。

【重要提示】
- 你需要在尽可能少的测试次数内完成任务
- 最终提交时必须预测恰好 {k} 对未测试过的对象对
- 所有预测必须全部正确才能获胜

每次只能包含一个操作标签：

- 单对测试（例如测试对象 C1 和 C3）：
<test>C1,C3</test>

- 查询剩余测试次数：
<query_quota></query_quota>

- 查询历史测试记录：
<query_history></query_history>

- 提交最终预测（必须恰好 {k} 对，每对一行）：
<answer>
C1,C2=不相交
C3,C4=有交集
C5,C6=不相交
C2,C5=有交集
C1,C4=不相交
C3,C5=有交集
</answer>
"""

    game_rule_en = """\
Let's play a "Set Relationship Inference" game. Here are the rules:

The game involves a finite set containing {n} elements. There are {m} objects, each associated with a binary string of length {n}. Each bit (0 or 1) in the binary string represents some internal property.

【Object Information】
{objects_info}

I have established a judgment rule that can evaluate any two objects and return one of two results: "disjoint" or "intersecting". Your task is to infer the essence of this judgment rule through limited tests and make correct predictions for untested object pairs.

You can perform the following operations:

1. Pairwise Test (consumes test quota)
   Ask about the relationship between any two objects, and I will tell you whether they are "disjoint" or "intersecting".

2. Query Remaining Test Quota (does not consume quota)
   Ask how many tests you can still perform.

3. Query Test History (does not consume quota)
   View all object pairs you have tested and their results.

4. Submit Final Prediction (does not consume quota)
   When you believe you have mastered the judgment rule, predict {k} untested object pairs.

【Important Notes】
- You need to complete the task with as few tests as possible
- Final submission must predict exactly {k} untested object pairs
- All predictions must be completely correct to win

Each operation must contain only one tag:

- Pairwise Test (e.g., testing objects C1 and C3):
<test>C1,C3</test>

- Query Remaining Test Quota:
<query_quota></query_quota>

- Query Test History:
<query_history></query_history>

- Submit Final Prediction (must be exactly {k} pairs, one per line):
<answer>
C1,C2=disjoint
C3,C4=intersecting
C5,C6=disjoint
C2,C5=intersecting
C1,C4=disjoint
C3,C5=intersecting
</answer>
"""

    tags = ["answer", "test", "query_quota", "query_history"]
    
    reasoning_type = "归纳推理"
    data_structure = "集合"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4, "m": 8, "max_tests": 10, "k": 6,
                "objects": {"C1": "1010", "C2": "0101", "C3": "1100", "C4": "0011", "C5": "1001", "C6": "0110", "C7": "1111", "C8": "0000"}
            },
            2: {
                "n": 5, "m": 10, "max_tests": 10, "k": 6,
                "objects": {"C1": "10100", "C2": "01011", "C3": "11000", "C4": "00110", "C5": "10010", "C6": "01101", "C7": "11110", "C8": "00001", "C9": "10001", "C10": "01010"}
            },
            3: {
                "n": 6, "m": 11, "max_tests": 10, "k": 6,
                "objects": {"C1": "101000", "C2": "010110", "C3": "110001", "C4": "001100", "C5": "100101", "C6": "011010", "C7": "111100", "C8": "000011", "C9": "100010", "C10": "010101", "C11": "101101"}
            },
            4: {
                "n": 6, "m": 12, "max_tests": 10, "k": 6,
                "objects": {"C1": "101001", "C2": "010110", "C3": "110010", "C4": "001101", "C5": "100110", "C6": "011001", "C7": "111000", "C8": "000111", "C9": "100011", "C10": "010100", "C11": "101100", "C12": "011110"}
            },
            5: {
                "n": 7, "m": 13, "max_tests": 10, "k": 6,
                "objects": {"C1": "1010010", "C2": "0101101", "C3": "1100100", "C4": "0011011", "C5": "1001100", "C6": "0110011", "C7": "1111000", "C8": "0000111", "C9": "1000110", "C10": "0101010", "C11": "1011001", "C12": "0110101", "C13": "1101010"}
            },
        },
        "en": {
            1: {
                "n": 4, "m": 8, "max_tests": 10, "k": 6,
                "objects": {"C1": "1010", "C2": "0101", "C3": "1100", "C4": "0011", "C5": "1001", "C6": "0110", "C7": "1111", "C8": "0000"}
            },
            2: {
                "n": 5, "m": 10, "max_tests": 10, "k": 6,
                "objects": {"C1": "10100", "C2": "01011", "C3": "11000", "C4": "00110", "C5": "10010", "C6": "01101", "C7": "11110", "C8": "00001", "C9": "10001", "C10": "01010"}
            },
            3: {
                "n": 6, "m": 11, "max_tests": 10, "k": 6,
                "objects": {"C1": "101000", "C2": "010110", "C3": "110001", "C4": "001100", "C5": "100101", "C6": "011010", "C7": "111100", "C8": "000011", "C9": "100010", "C10": "010101", "C11": "101101"}
            },
            4: {
                "n": 6, "m": 12, "max_tests": 10, "k": 6,
                "objects": {"C1": "101001", "C2": "010110", "C3": "110010", "C4": "001101", "C5": "100110", "C6": "011001", "C7": "111000", "C8": "000111", "C9": "100011", "C10": "010100", "C11": "101100", "C12": "011110"}
            },
            5: {
                "n": 7, "m": 13, "max_tests": 10, "k": 6,
                "objects": {"C1": "1010010", "C2": "0101101", "C3": "1100100", "C4": "0011011", "C5": "1001100", "C6": "0110011", "C7": "1111000", "C8": "0000111", "C9": "1000110", "C10": "0101010", "C11": "1011001", "C12": "0110101", "C13": "1101010"}
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
        
        self._game_info["n"] = cfg["n"]
        self._game_info["m"] = cfg["m"]
        self._game_info["k"] = cfg["k"]
        self.max_tests = cfg["max_tests"]
        
        self.objects = cfg["objects"]
        
        objects_lines = []
        for obj_id, binary_str in self.objects.items():
            objects_lines.append(f"{obj_id}: {binary_str}")
        self._game_info["objects_info"] = "\n".join(objects_lines)
        
        self.test_history = []
        self.remaining_tests = self.max_tests
        
    def _is_disjoint(self, obj1, obj2):
        binary1 = self.objects[obj1]
        binary2 = self.objects[obj2]
        
        for b1, b2 in zip(binary1, binary2):
            if b1 == '1' and b2 == '1':
                return False
        return True
    
    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        lines = [line.strip() for line in raw_ans.split('\n') if line.strip()]
        
        if len(lines) != self._game_info["k"]:
            return False
        
        predictions = []
        for line in lines:
            if '=' not in line:
                return False
            pair_str, result = line.split('=', 1)
            pair_str = pair_str.strip()
            result = result.strip()
            
            if ',' not in pair_str:
                return False
            
            obj1, obj2 = [x.strip() for x in pair_str.split(',')]
            
            if obj1 not in self.objects or obj2 not in self.objects:
                return False
            
            if obj1 == obj2:
                return False
            
            normalized_pair = tuple(sorted([obj1, obj2]))
            
            for hist_obj1, hist_obj2, _ in self.test_history:
                hist_pair = tuple(sorted([hist_obj1, hist_obj2]))
                if normalized_pair == hist_pair:
                    return False
            
            predictions.append((obj1, obj2, result))
        
        normalized_predictions = [tuple(sorted([p[0], p[1]])) for p in predictions]
        if len(normalized_predictions) != len(set(normalized_predictions)):
            return False
        
        if self.config.language == "zh":
            disjoint_str = "不相交"
            intersecting_str = "有交集"
        else:
            disjoint_str = "disjoint"
            intersecting_str = "intersecting"
        
        for obj1, obj2, predicted_result in predictions:
            actual_disjoint = self._is_disjoint(obj1, obj2)
            
            if predicted_result == disjoint_str:
                if not actual_disjoint:
                    return False
            elif predicted_result == intersecting_str:
                if actual_disjoint:
                    return False
            else:
                return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            disjoint_str = "不相交"
            intersecting_str = "有交集"
        else:
            disjoint_str = "disjoint"
            intersecting_str = "intersecting"
        
        if "test" in parsed_info:
            if self.remaining_tests <= 0:
                return "错误：测试次数已用尽。" if self.config.language == "zh" else "Error: No test quota remaining."
            
            try:
                raw = parsed_info["test"].strip()
                obj1, obj2 = [x.strip() for x in raw.split(",")]
                
                if obj1 not in self.objects or obj2 not in self.objects:
                    return "错误：对象不存在。" if self.config.language == "zh" else "Error: Object does not exist."
                
                is_disjoint = self._is_disjoint(obj1, obj2)
                result = disjoint_str if is_disjoint else intersecting_str
                
                self.test_history.append((obj1, obj2, result))
                self.remaining_tests -= 1
                
                return result
                
            except Exception as e:
                return "错误：格式无效。" if self.config.language == "zh" else "Error: Invalid format."
        
        elif "query_quota" in parsed_info:
            return str(self.remaining_tests)
        
        elif "query_history" in parsed_info:
            if not self.test_history:
                return "无测试记录。" if self.config.language == "zh" else "No test history."
            
            lines = []
            for obj1, obj2, result in self.test_history:
                lines.append(f"({obj1}, {obj2}) = {result}")
            return "\n".join(lines)
        
        else:
            raise ValueError("No valid query tag found.")
    
    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        if self.config.language == "zh":
            disjoint_str = "不相交"
            intersecting_str = "有交集"
        else:
            disjoint_str = "disjoint"
            intersecting_str = "intersecting"
            
        obj_keys = sorted(self.objects.keys())
        
        for obj1, obj2 in itertools.combinations(obj_keys, 2):
            is_disjoint = self._is_disjoint(obj1, obj2)
            result = disjoint_str if is_disjoint else intersecting_str
            
            queries.append({
                "query": f"<test>{obj1},{obj2}</test>",
                "answer": result
            })
            
        return queries

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        lang = self.config.language
        if lang == "zh":
            if correct.strip() == "不相交":
                return "有交集"
            elif correct.strip() == "有交集":
                return "不相交"
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        elif lang == "en":
            if correct.strip().lower() == "disjoint":
                return "intersecting"
            elif correct.strip().lower() == "intersecting":
                return "disjoint"
            if "yes" in correct.lower():
                return correct.replace("Yes", "No").replace("yes", "no").replace("YES", "NO")
            elif "no" in correct.lower():
                return correct.replace("No", "Yes").replace("no", "yes").replace("NO", "YES")
        
        return correct + "_WRONG"