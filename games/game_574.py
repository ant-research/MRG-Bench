# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 集合：存在一个由N个物体组成的集合，注意他们不存在位置、前后和大小关系。
# 知识点:   子集包含：某子集是否完全被另一子集包含
# ============================================================

import itertools
from .base import Game

class SetRelationRuleGame(Game):

    game_rule_zh = """\
我们现在来玩一个"集合关系规则推理"游戏，规则如下：

游戏设定了一个有限集合 U = {{A, B, C, D, E, F}}，包含6个不同的元素。

存在一个固定但未知的二元判定规则 f(R,S)，该规则会对任意两个子集 R 和 S 进行判定，返回"开"或"关"。规则只可能是以下四种之一：
- 规则A：当 R 的所有元素都在 S 中时为"开"
- 规则B：当 S 的所有元素都在 R 中时为"开"
- 规则C：当 U 中不在 R 中的所有元素都在 S 中时为"开"
- 规则D：当 S 的所有元素都不在 R 中时为"开"

游戏中有三个公开的目标集合：
- R1 = {{A, B}}
- R2 = {{B, C, D}}
- R3 = {{D, E}}

你的任务分为两步：
1. 通过查询识别出真实规则是 A、B、C、D 中的哪一个
2. 给出一个集合 S*，使得在该规则下，对 R1、R2、R3 的判定都为"开"

你可以进行任意多次查询，每次查询需要指定两个子集 R 和 S（可以是空集，可以包含 U 中的任意元素）。我会根据真实规则返回"开"或"关"。

## 查询与提交答案的格式

每次查询必须包含两个集合 R 和 S，使用以下 XML 格式（集合用逗号分隔元素，空集用 empty 表示）：

<query>R={{A,B}}, S={{B,C}}</query>

或者查询空集：

<query>R={{empty}}, S={{A,B,C}}</query>

提交最终答案时，必须说明规则类型（A、B、C 或 D）并给出集合 S*，格式如下：

<answer>rule=A, S={{A,B,C,D,E}}</answer>

注意：
- 集合元素必须是 A、B、C、D、E、F 中的字母
- 元素顺序不重要，重复元素会被忽略
- 空集用 empty 表示
- 每次只能进行一个查询或提交一个答案
"""

    game_rule_en = """\
Let's play a "Set Relation Rule Inference" game. Here are the rules:

The game has a finite set U = {{A, B, C, D, E, F}} containing 6 distinct elements.

There exists a fixed but unknown binary decision rule f(R,S) that judges any two subsets R and S, returning "open" or "closed". The rule can only be one of the following four:
- Rule A: "open" when all elements of R are in S
- Rule B: "open" when all elements of S are in R
- Rule C: "open" when all elements of U not in R are in S
- Rule D: "open" when all elements of S are not in R

There are three public target sets in the game:
- R1 = {{A, B}}
- R2 = {{B, C, D}}
- R3 = {{D, E}}

Your task has two steps:
1. Identify which rule (A, B, C, or D) is the true rule through queries
2. Provide a set S* such that under this rule, the judgment for R1, R2, R3 are all "open"

You can make any number of queries. Each query specifies two subsets R and S (can be empty sets, can contain any elements from U). I will return "open" or "closed" based on the true rule.

## Query and Answer Format

Each query must contain two sets R and S, using the following XML format (elements separated by commas, empty set represented as empty):

<query>R={{A,B}}, S={{B,C}}</query>

Or query with empty set:

<query>R={{empty}}, S={{A,B,C}}</query>

When submitting the final answer, specify the rule type (A, B, C, or D) and provide set S*, using this format:

<answer>rule=A, S={{A,B,C,D,E}}</answer>

Note:
- Set elements must be letters from A, B, C, D, E, F
- Element order doesn't matter, duplicate elements will be ignored
- Empty set is represented as empty
- Only one query or one answer per turn
"""

    # ================= 场景 1：交通 =================
    contextualized_rule_zh_1 = """\
[交通场景] 我们现在来玩一个“路口通行权限判定”规则推理游戏，规则如下：

城市智能交通信号控制系统设定了一个有限干道集合 U = {{A, B, C, D, E, F}}，代表6条主要干道。

系统存在一个固定但未知的安全通行规则 f(R,S)，该规则会对任意两个干道组 R（当前高流量干道组）和 S（计划开启绿灯的干道组）进行判定，返回"开"（允许通行）或"关"（拒绝通行）。规则只可能是以下四种之一：
- 规则A：当 R 的所有干道都在 S 中时为"开"（高流量干道必须全部绿灯）
- 规则B：当 S 的所有干道都在 R 中时为"开"（绿灯干道必须全部是高流量干道）
- 规则C：当 U 中不在 R 中的所有干道都在 S 中时为"开"（非高流量干道必须全部绿灯）
- 规则D：当 S 的所有干道都不在 R 中时为"开"（绿灯干道必须避开高流量干道）

游戏中有三个公开的高流量干道组测试用例：
- R1 = {{A, B}}
- R2 = {{B, C, D}}
- R3 = {{D, E}}

你的任务分为两步：
1. 通过查询识别出真实规则是 A、B、C、D 中的哪一个
2. 给出一个绿灯干道组 S*，使得在该规则下，对 R1、R2、R3 的判定都为"开"

你可以进行任意多次查询，每次查询需要指定两个干道组 R 和 S（可以是空集，可以包含 U 中的任意干道）。我会根据真实规则返回"开"或"关"。

## 查询与提交答案的格式

每次查询必须包含两个集合 R 和 S，使用以下 XML 格式（集合用逗号分隔元素，空集用 empty 表示）：

<query>R={{A,B}}, S={{B,C}}</query>

或者查询空集：

<query>R={{empty}}, S={{A,B,C}}</query>

提交最终答案时，必须说明规则类型（A、B、C 或 D）并给出集合 S*，格式如下：

<answer>rule=A, S={{A,B,C,D,E}}</answer>

注意：
- 集合元素必须是 A、B、C、D、E、F 中的字母
- 元素顺序不重要，重复元素会被忽略
- 空集用 empty 表示
- 每次只能进行一个查询或提交一个答案
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario] Let's play an "Intersection Access Permission Evaluation" rule inference game. Here are the rules:

The urban intelligent traffic signal control system defines a finite set of arterial roads U = {{A, B, C, D, E, F}} containing 6 main roads.

There exists a fixed but unknown safety access rule f(R,S) that judges any two road sets R (current high-traffic roads) and S (roads planned for green lights), returning "open" (access granted) or "closed" (access denied). The rule can only be one of the following four:
- Rule A: "open" when all roads in R are in S (all high-traffic roads must get green lights)
- Rule B: "open" when all roads in S are in R (green light roads must be exclusively high-traffic roads)
- Rule C: "open" when all roads of U not in R are in S (all non-high-traffic roads must get green lights)
- Rule D: "open" when all roads in S are not in R (green light roads must avoid high-traffic roads)

There are three public test cases of high-traffic road sets:
- R1 = {{A, B}}
- R2 = {{B, C, D}}
- R3 = {{D, E}}

Your task has two steps:
1. Identify which rule (A, B, C, or D) is the true rule through queries
2. Provide a green light road set S* such that under this rule, the judgment for R1, R2, R3 are all "open"

You can make any number of queries. Each query specifies two sets R and S (can be empty sets, can contain any elements from U). I will return "open" or "closed" based on the true rule.

## Query and Answer Format

Each query must contain two sets R and S, using the following XML format (elements separated by commas, empty set represented as empty):

<query>R={{A,B}}, S={{B,C}}</query>

Or query with empty set:

<query>R={{empty}}, S={{A,B,C}}</query>

When submitting the final answer, specify the rule type (A, B, C, or D) and provide set S*, using this format:

<answer>rule=A, S={{A,B,C,D,E}}</answer>

Note:
- Set elements must be letters from A, B, C, D, E, F
- Element order doesn't matter, duplicate elements will be ignored
- Empty set is represented as empty
- Only one query or one answer per turn
"""

    # ================= 场景 2：医疗 =================
    contextualized_rule_zh_2 = """\
[医疗场景] 我们现在来玩一个“新型联合用药方案的安全禁忌审核”规则推理游戏，规则如下：

医疗系统设定了一个有限药物集合 U = {{A, B, C, D, E, F}}，代表6种特效药物分子。

系统存在一个固定但未知的药物相容性评估规则 f(R,S)，该规则会对任意两个药物组 R（患者已服用的药物组）和 S（计划开具的新药组）进行判定，返回"开"（允许开处方）或"关"（拒绝）。规则只可能是以下四种之一：
- 规则A：当 R 的所有药物都在 S 中时为"开"（需开具全套原服用药作为巩固）
- 规则B：当 S 的所有药物都在 R 中时为"开"（新处方只能是原有药物的子集）
- 规则C：当 U 中不在 R 中的所有药物都在 S 中时为"开"（必须补充所有未服用的药物分子）
- 规则D：当 S 的所有药物都不在 R 中时为"开"（新药不能与已服用药物重复）

游戏中有三个公开的患者已服用药物组记录：
- R1 = {{A, B}}
- R2 = {{B, C, D}}
- R3 = {{D, E}}

你的任务分为两步：
1. 通过查询识别出真实规则是 A、B、C、D 中的哪一个
2. 给出一个通用新药组 S*，使得在该规则下，对 R1、R2、R3 的审核判定都为"开"

你可以进行任意多次查询，每次查询需要指定两个药物组 R 和 S（可以是空集，可以包含 U 中的任意元素）。我会根据真实规则返回"开"或"关"。

## 查询与提交答案的格式

每次查询必须包含两个集合 R 和 S，使用以下 XML 格式（集合用逗号分隔元素，空集用 empty 表示）：

<query>R={{A,B}}, S={{B,C}}</query>

或者查询空集：

<query>R={{empty}}, S={{A,B,C}}</query>

提交最终答案时，必须说明规则类型（A、B、C 或 D）并给出集合 S*，格式如下：

<answer>rule=A, S={{A,B,C,D,E}}</answer>

注意：
- 集合元素必须是 A、B、C、D、E、F 中的字母
- 元素顺序不重要，重复元素会被忽略
- 空集用 empty 表示
- 每次只能进行一个查询或提交一个答案
"""

    contextualized_rule_en_2 = """\
[Medical Scenario] Let's play a "Novel Combination Therapy Safety Contraindication Audit" rule inference game. Here are the rules:

The medical system defines a finite set of drugs U = {{A, B, C, D, E, F}} representing 6 specific drug molecules.

There exists a fixed but unknown drug compatibility evaluation rule f(R,S) that judges any two drug sets R (drugs already taken by the patient) and S (new drugs planned to be prescribed), returning "open" (prescription allowed) or "closed" (rejected). The rule can only be one of the following four:
- Rule A: "open" when all drugs in R are in S (the full set of previously taken drugs must be prescribed for consolidation)
- Rule B: "open" when all drugs in S are in R (new prescriptions must exclusively be a subset of original drugs)
- Rule C: "open" when all drugs of U not in R are in S (all un-taken drug molecules must be supplemented)
- Rule D: "open" when all drugs in S are not in R (new drugs must not overlap with already taken drugs)

There are three public patient records of previously taken drug sets:
- R1 = {{A, B}}
- R2 = {{B, C, D}}
- R3 = {{D, E}}

Your task has two steps:
1. Identify which rule (A, B, C, or D) is the true rule through queries
2. Provide a universal new drug set S* such that under this rule, the audit judgments for R1, R2, R3 are all "open"

You can make any number of queries. Each query specifies two sets R and S (can be empty sets, can contain any elements from U). I will return "open" or "closed" based on the true rule.

## Query and Answer Format

Each query must contain two sets R and S, using the following XML format (elements separated by commas, empty set represented as empty):

<query>R={{A,B}}, S={{B,C}}</query>

Or query with empty set:

<query>R={{empty}}, S={{A,B,C}}</query>

When submitting the final answer, specify the rule type (A, B, C, or D) and provide set S*, using this format:

<answer>rule=A, S={{A,B,C,D,E}}</answer>

Note:
- Set elements must be letters from A, B, C, D, E, F
- Element order doesn't matter, duplicate elements will be ignored
- Empty set is represented as empty
- Only one query or one answer per turn
"""

    # ================= 场景 3：教育 =================
    contextualized_rule_zh_3 = """\
[教育场景] 我们现在来玩一个“自适应学习平台课程解锁”规则推理游戏，规则如下：

平台设定了一个有限的知识模块集合 U = {{A, B, C, D, E, F}}，代表6个核心模块。

系统存在一个固定但未知的课程解锁逻辑 f(R,S)，该逻辑会对任意两个模块组 R（学生已掌握的模块）和 S（申请解锁的模块组）进行判定，返回"开"（允许解锁）或"关"（拒绝解锁）。规则只可能是以下四种之一：
- 规则A：当 R 的所有模块都在 S 中时为"开"（申请模块必须涵盖所有已掌握模块作复习）
- 规则B：当 S 的所有模块都在 R 中时为"开"（申请模块必须仅限已掌握模块的进阶巩固）
- 规则C：当 U 中不在 R 中的所有模块都在 S 中时为"开"（必须一次性申请所有未掌握的模块）
- 规则D：当 S 的所有模块都不在 R 中时为"开"（申请模块必须全是新知识，避免重复学习）

游戏中有三个公开的学生画像（已掌握模块记录）：
- R1 = {{A, B}}
- R2 = {{B, C, D}}
- R3 = {{D, E}}

你的任务分为两步：
1. 通过查询识别出真实规则是 A、B、C、D 中的哪一个
2. 给出一个推荐模块组 S*，使得在该规则下，这三类学生申请该模块组的判定都为"开"

你可以进行任意多次查询，每次查询需要指定两个模块组 R 和 S（可以是空集，可以包含 U 中的任意元素）。我会根据真实规则返回"开"或"关"。

## 查询与提交答案的格式

每次查询必须包含两个集合 R 和 S，使用以下 XML 格式（集合用逗号分隔元素，空集用 empty 表示）：

<query>R={{A,B}}, S={{B,C}}</query>

或者查询空集：

<query>R={{empty}}, S={{A,B,C}}</query>

提交最终答案时，必须说明规则类型（A、B、C 或 D）并给出集合 S*，格式如下：

<answer>rule=A, S={{A,B,C,D,E}}</answer>

注意：
- 集合元素必须是 A、B、C、D、E、F 中的字母
- 元素顺序不重要，重复元素会被忽略
- 空集用 empty 表示
- 每次只能进行一个查询或提交一个答案
"""

    contextualized_rule_en_3 = """\
[Education Scenario] Let's play an "Adaptive Learning Platform Course Unlock" rule inference game. Here are the rules:

The platform defines a finite set of knowledge modules U = {{A, B, C, D, E, F}} representing 6 core modules.

There exists a fixed but unknown course unlock logic f(R,S) that evaluates any two module sets R (modules already mastered by the student) and S (modules applied to be unlocked), returning "open" (unlock allowed) or "closed" (unlock denied). The rule can only be one of the following four:
- Rule A: "open" when all modules in R are in S (applied modules must cover all mastered modules for review)
- Rule B: "open" when all modules in S are in R (applied modules must strictly be for advancing previously mastered ones)
- Rule C: "open" when all modules of U not in R are in S (must apply for all unmastered modules at once)
- Rule D: "open" when all modules in S are not in R (applied modules must be entirely new knowledge to avoid redundant learning)

There are three public student profiles showing their mastered modules:
- R1 = {{A, B}}
- R2 = {{B, C, D}}
- R3 = {{D, E}}

Your task has two steps:
1. Identify which rule (A, B, C, or D) is the true rule through queries
2. Provide a recommended module set S* such that under this rule, applications for this set from these three types of students are all "open"

You can make any number of queries. Each query specifies two sets R and S (can be empty sets, can contain any elements from U). I will return "open" or "closed" based on the true rule.

## Query and Answer Format

Each query must contain two sets R and S, using the following XML format (elements separated by commas, empty set represented as empty):

<query>R={{A,B}}, S={{B,C}}</query>

Or query with empty set:

<query>R={{empty}}, S={{A,B,C}}</query>

When submitting the final answer, specify the rule type (A, B, C, or D) and provide set S*, using this format:

<answer>rule=A, S={{A,B,C,D,E}}</answer>

Note:
- Set elements must be letters from A, B, C, D, E, F
- Element order doesn't matter, duplicate elements will be ignored
- Empty set is represented as empty
- Only one query or one answer per turn
"""

    # ================= 场景 4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
[制造业场景] 我们现在来玩一个“自动化流水线零件质检放行”规则推理游戏，规则如下：

质检系统设定了一个有限的关键零部件集合 U = {{A, B, C, D, E, F}}，代表6种核心组件。

系统存在一个固定但未知的批次合格判定规则 f(R,S)，该规则会对任意两个零件组 R（抽检发现缺陷的零件组）和 S（计划重装的零件组）进行判定，返回"开"（允许重装放行）或"关"（驳回）。规则只可能是以下四种之一：
- 规则A：当 R 的所有零件都在 S 中时为"开"（所有缺陷零件必须包含在重装组中进行替换）
- 规则B：当 S 的所有零件都在 R 中时为"开"（重装的零件必须全部是已确认缺陷的零件）
- 规则C：当 U 中不在 R 中的所有零件都在 S 中时为"开"（未发现缺陷的零件必须全部重装进行二次验证）
- 规则D：当 S 的所有零件都不在 R 中时为"开"（重装的零件必须完全避开有缺陷的零件）

游戏中有三次历史检验批次的缺陷记录：
- R1 = {{A, B}}
- R2 = {{B, C, D}}
- R3 = {{D, E}}

你的任务分为两步：
1. 通过查询识别出真实规则是 A、B、C、D 中的哪一个
2. 给出一个标准重装零件组 S*，使得在该规则下，这三种缺陷情况的放行测试结果都为"开"

你可以进行任意多次查询，每次查询需要指定两个零件组 R 和 S（可以是空集，可以包含 U 中的任意元素）。我会根据真实规则返回"开"或"关"。

## 查询与提交答案的格式

每次查询必须包含两个集合 R 和 S，使用以下 XML 格式（集合用逗号分隔元素，空集用 empty 表示）：

<query>R={{A,B}}, S={{B,C}}</query>

或者查询空集：

<query>R={{empty}}, S={{A,B,C}}</query>

提交最终答案时，必须说明规则类型（A、B、C 或 D）并给出集合 S*，格式如下：

<answer>rule=A, S={{A,B,C,D,E}}</answer>

注意：
- 集合元素必须是 A、B、C、D、E、F 中的字母
- 元素顺序不重要，重复元素会被忽略
- 空集用 empty 表示
- 每次只能进行一个查询或提交一个答案
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario] Let's play an "Automated Assembly Line Part Quality Inspection Clearance" rule inference game. Here are the rules:

The quality inspection system defines a finite set of key components U = {{A, B, C, D, E, F}} representing 6 core parts.

There exists a fixed but unknown batch qualification evaluation rule f(R,S) that judges any two part sets R (defective parts found in spot checks) and S (parts planned to be reinstalled), returning "open" (clearance granted) or "closed" (rejected). The rule can only be one of the following four:
- Rule A: "open" when all parts in R are in S (all defective parts must be included in the reinstall set for replacement)
- Rule B: "open" when all parts in S are in R (reinstalled parts must be strictly limited to confirmed defective ones)
- Rule C: "open" when all parts of U not in R are in S (all non-defective parts must be reinstalled for secondary verification)
- Rule D: "open" when all parts in S are not in R (reinstalled parts must completely avoid the defective ones)

There are three historical inspection batches showing defective part sets:
- R1 = {{A, B}}
- R2 = {{B, C, D}}
- R3 = {{D, E}}

Your task has two steps:
1. Identify which rule (A, B, C, or D) is the true rule through queries
2. Provide a standard reinstall part set S* such that under this rule, the clearance test results for these three defective situations are all "open"

You can make any number of queries. Each query specifies two sets R and S (can be empty sets, can contain any elements from U). I will return "open" or "closed" based on the true rule.

## Query and Answer Format

Each query must contain two sets R and S, using the following XML format (elements separated by commas, empty set represented as empty):

<query>R={{A,B}}, S={{B,C}}</query>

Or query with empty set:

<query>R={{empty}}, S={{A,B,C}}</query>

When submitting the final answer, specify the rule type (A, B, C, or D) and provide set S*, using this format:

<answer>rule=A, S={{A,B,C,D,E}}</answer>

Note:
- Set elements must be letters from A, B, C, D, E, F
- Element order doesn't matter, duplicate elements will be ignored
- Empty set is represented as empty
- Only one query or one answer per turn
"""

    # ================= 场景 5：法律 =================
    contextualized_rule_zh_5 = """\
[法律场景] 我们现在来玩一个“企业合规性自动审查系统豁免条款”判定规则推理游戏，规则如下：

合规系统设定了一个有限的关键商业资质集合 U = {{A, B, C, D, E, F}}，代表6项核心资质。

系统存在一个固定但未知的合规豁免规则 f(R,S)，该规则会对任意两个资质组 R（企业缺失的资质组）和 S（企业提交的补偿性材料覆盖的资质组）进行判定，返回"开"（通过审查）或"关"（不通过）。规则只可能是以下四种之一：
- 规则A：当 R 的所有资质都在 S 中时为"开"（缺失的资质必须全部提供补偿材料）
- 规则B：当 S 的所有资质都在 R 中时为"开"（提交的补偿材料必须仅针对缺失的资质）
- 规则C：当 U 中不在 R 中的所有资质都在 S 中时为"开"（未缺失的资质也必须提供全套材料证明）
- 规则D：当 S 的所有资质都不在 R 中时为"开"（提供的材料必须完全不涉及缺失资质，用其他担保代替）

游戏中有三个公开的受审企业档案（记录了缺失资质组）：
- R1 = {{A, B}}
- R2 = {{B, C, D}}
- R3 = {{D, E}}

你的任务分为两步：
1. 通过查询识别出真实规则是 A、B、C、D 中的哪一个
2. 设计一套标准补偿性材料涵盖的资质组 S*，使得在该规则下，这三种情况的企业都能通过审查（即判定为"开"）

你可以进行任意多次查询，每次查询需要指定两个资质组 R 和 S（可以是空集，可以包含 U 中的任意元素）。我会根据真实规则返回"开"或"关"。

## 查询与提交答案的格式

每次查询必须包含两个集合 R 和 S，使用以下 XML 格式（集合用逗号分隔元素，空集用 empty 表示）：

<query>R={{A,B}}, S={{B,C}}</query>

或者查询空集：

<query>R={{empty}}, S={{A,B,C}}</query>

提交最终答案时，必须说明规则类型（A、B、C 或 D）并给出集合 S*，格式如下：

<answer>rule=A, S={{A,B,C,D,E}}</answer>

注意：
- 集合元素必须是 A、B、C、D、E、F 中的字母
- 元素顺序不重要，重复元素会被忽略
- 空集用 empty 表示
- 每次只能进行一个查询或提交一个答案
"""

    contextualized_rule_en_5 = """\
[Legal Scenario] Let's play an "Enterprise Compliance Automated Review System Exemption Clause" judgment rule inference game. Here are the rules:

The compliance system defines a finite set of key business qualifications U = {{A, B, C, D, E, F}} representing 6 core qualifications.

There exists a fixed but unknown compliance exemption rule f(R,S) that evaluates any two qualification sets R (qualifications the enterprise lacks) and S (qualifications covered by the submitted compensatory materials), returning "open" (review passed) or "closed" (review failed). The rule can only be one of the following four:
- Rule A: "open" when all qualifications in R are in S (all lacking qualifications must be covered by compensatory materials)
- Rule B: "open" when all qualifications in S are in R (compensatory materials must strictly target only the lacking qualifications)
- Rule C: "open" when all qualifications of U not in R are in S (all non-lacking qualifications must also have full supporting materials)
- Rule D: "open" when all qualifications in S are not in R (submitted materials must strictly avoid lacking qualifications, serving as alternative guarantees)

There are three public profiles of enterprises under review (showing their lacking qualification sets):
- R1 = {{A, B}}
- R2 = {{B, C, D}}
- R3 = {{D, E}}

Your task has two steps:
1. Identify which rule (A, B, C, or D) is the true rule through queries
2. Design a standard set of qualifications covered by compensatory materials S* such that under this rule, these three types of enterprises can all pass the review ("open")

You can make any number of queries. Each query specifies two sets R and S (can be empty sets, can contain any elements from U). I will return "open" or "closed" based on the true rule.

## Query and Answer Format

Each query must contain two sets R and S, using the following XML format (elements separated by commas, empty set represented as empty):

<query>R={{A,B}}, S={{B,C}}</query>

Or query with empty set:

<query>R={{empty}}, S={{A,B,C}}</query>

When submitting the final answer, specify the rule type (A, B, C, or D) and provide set S*, using this format:

<answer>rule=A, S={{A,B,C,D,E}}</answer>

Note:
- Set elements must be letters from A, B, C, D, E, F
- Element order doesn't matter, duplicate elements will be ignored
- Empty set is represented as empty
- Only one query or one answer per turn
"""

    tags = ["answer", "query"]
    
    reasoning_type = "溯因推理"
    data_structure = "集合"

    # 难度配置说明：
    # 1 (简单)       - 规则A，答案明显
    # 2 (中等偏下)   - 规则D，需要理解补集和交集
    # 3 (中等偏上)   - 规则C，需要理解补集
    # 4 (较难)       - 规则B，答案为空集
    # 5 (难)         - 规则B，答案为空集

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "rule": "A",  # R⊆S，答案 = R1∪R2∪R3 = {A,B,C,D,E}
                "answer_set": {"A", "B", "C", "D", "E"},
            },
            2: {
                "rule": "D",  # S⊆U\R，答案 = {F}（只有F不在任何R中）
                "answer_set": {"F"},
            },
            3: {
                "rule": "C",  # U\R⊆S，答案 = U = {A,B,C,D,E,F}
                "answer_set": {"A", "B", "C", "D", "E", "F"},
            },
            4: {
                "rule": "B",  # S⊆R，答案 = ∅（需要理解交集为空）
                "answer_set": set(),
            },
            5: {
                "rule": "B",  # S⊆R，答案 = ∅，与难度4相同规则
                "answer_set": set(),
            },
        },
        "en": {
            1: {
                "rule": "A",
                "answer_set": {"A", "B", "C", "D", "E"},
            },
            2: {
                "rule": "D",
                "answer_set": {"F"},
            },
            3: {
                "rule": "C",
                "answer_set": {"A", "B", "C", "D", "E", "F"},
            },
            4: {
                "rule": "B",
                "answer_set": set(),
            },
            5: {
                "rule": "B",
                "answer_set": set(),
            },
        },
    }

    def __init__(self, config):
        # 定义固定的目标集合
        self.R1 = {"A", "B"}
        self.R2 = {"B", "C", "D"}
        self.R3 = {"D", "E"}
        self.U = {"A", "B", "C", "D", "E", "F"}
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏，设置规则和答案"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.rule = cfg["rule"]
        self.correct_answer_set = cfg["answer_set"]
        
        # 用于format游戏规则的信息（如果需要）
        self._game_info = {}

    def _parse_set(self, set_str):
        """解析集合字符串，返回set对象"""
        set_str = set_str.strip()
        # 去除可能的花括号
        set_str = set_str.strip('{}')
        set_str = set_str.strip()
        
        if set_str.lower() == "empty" or set_str == "":
            return set()
        
        elements = [x.strip().upper() for x in set_str.split(",") if x.strip()]
        # 验证元素是否合法
        for elem in elements:
            if elem not in self.U:
                raise ValueError(f"Invalid element: {elem}")
        return set(elements)

    def _check_rule(self, R, S):
        """根据当前规则检查 f(R,S) 是否为"开" """
        if self.rule == "A":
            # R⊆S: R的所有元素都在S中
            return R.issubset(S)
        elif self.rule == "B":
            # S⊆R: S的所有元素都在R中
            return S.issubset(R)
        elif self.rule == "C":
            # U\R⊆S: U中不在R中的元素都在S中
            U_minus_R = self.U - R
            return U_minus_R.issubset(S)
        elif self.rule == "D":
            # S⊆U\R: S的所有元素都不在R中
            U_minus_R = self.U - R
            return S.issubset(U_minus_R)
        else:
            raise ValueError(f"Unknown rule: {self.rule}")

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        try:
            # 解析答案格式: rule=X, S={...}
            parts = raw_ans.split(",", 1)
            if len(parts) != 2:
                return False
            
            rule_part = parts[0].strip()
            s_part = parts[1].strip()
            
            # 解析规则
            if not rule_part.startswith("rule="):
                return False
            model_rule = rule_part.split("=", 1)[1].strip().upper()
            
            # 解析S*
            if not s_part.startswith("S="):
                return False
            s_str = s_part.split("=", 1)[1].strip()
            model_S = self._parse_set(s_str)
            
            # 检查规则是否正确
            if model_rule != self.rule:
                return False
            
            # 检查S*是否对R1、R2、R3都满足规则
            for R in [self.R1, self.R2, self.R3]:
                if not self._check_rule(R, model_S):
                    return False
            
            return True
            
        except Exception as e:
            return False

    def get_all_possible_queries(self) -> list[dict]:
        """
        返回一组有代表性的查询，用于冗余性评估。
        选取关键的子集组合而非穷举所有4096种，以避免上下文过长。
        """
        # 选取有代表性的子集（空集、单元素、目标集、全集等）
        representative_sets = [
            set(),
            {"A"}, {"B"}, {"C"}, {"D"}, {"E"}, {"F"},
            {"A", "B"},        # = R1
            {"B", "C", "D"},   # = R2
            {"D", "E"},        # = R3
            {"A", "B", "C"},
            {"C", "D", "E", "F"},
            {"A", "B", "C", "D", "E"},  # R1∪R2∪R3
            {"A", "B", "C", "D", "E", "F"},  # U
        ]
        
        queries = []
        
        def format_set_str(s):
            if not s:
                return "empty"
            return "{" + ",".join(sorted(list(s))) + "}"

        for R in representative_sets:
            r_str = format_set_str(R)
            for S in representative_sets:
                s_str = format_set_str(S)
                
                query_content = f"R={r_str}, S={s_str}"
                query_xml = f"<query>{query_content}</query>"
                
                result = self._check_rule(R, S)
                
                if self.config.language == "zh":
                    ans_str = "开" if result else "关"
                else:
                    ans_str = "open" if result else "closed"
                
                queries.append({
                    "query": query_xml,
                    "answer": ans_str
                })
                
        return queries

    def _cf_core_produce(self, parsed_info):
        """原始的查询响应生成逻辑"""
        if "query" not in parsed_info:
            raise ValueError("No query tag found.")
        
        query_str = parsed_info["query"]
        
        # 解析查询格式: R={...}, S={...}
        parts = query_str.split(",", 1)
        if len(parts) != 2:
            raise ValueError("Query must contain both R and S separated by a comma.")
        
        r_part = parts[0].strip()
        s_part = parts[1].strip()
        
        # 解析R
        if not r_part.startswith("R="):
            raise ValueError("Query must start with R=")
        r_str = r_part.split("=", 1)[1].strip()
        R = self._parse_set(r_str)
        
        # 解析S
        if not s_part.startswith("S="):
            raise ValueError("Query must contain S=")
        s_str = s_part.split("=", 1)[1].strip()
        S = self._parse_set(s_str)
        
        # 检查规则并返回结果
        result = self._check_rule(R, S)
        
        if self.config.language == "zh":
            return "开" if result else "关"
        else:
            return "open" if result else "closed"

    def _cf_make_wrong(self, correct):
        """将正确的开/关响应翻转为错误的"""
        if self.config.language == "zh":
            if correct == "开":
                return "关"
            elif correct == "关":
                return "开"
        else:
            if correct.lower() == "open":
                return "closed"
            elif correct.lower() == "closed":
                return "open"
        
        # fallback
        return correct + "_WRONG"