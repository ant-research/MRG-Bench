# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 集合：存在一个由N个物体组成的集合，注意他们不存在位置、前后和大小关系。
# 知识点:   多条件子集：同时满足多个条件的元素构成的子集是什么
# ============================================================

from .base import Game
import re
import itertools
from typing import List, Dict


class AttributeDeductionGame(Game):

    game_rule_zh = """\
我们现在来玩一个"属性推理"游戏，规则如下：

游戏设定了一个包含 {n} 个元素的集合 U，元素分别以 {elements} 标识。每个元素具有四个二元属性 α, β, γ, δ，每个属性的取值为 0 或 1，但具体取值是隐藏的。

你的目标是找出满足特定目标条件 T 的所有元素。目标条件 T 定义为：α=1 且 β=0 且 γ=1 且 δ=0。

你可以通过 COUNT 查询来获取信息，每次查询需要指定一个子集和一些条件，系统会告诉你该子集中有多少元素满足这些条件。当你收集足够信息后，请提交最终答案。

## COUNT 查询格式

每次 COUNT 查询需要指定：
1. 一个子集 S，包含至少 3 个元素
2. 一个条件集 L，由 1 或 2 条原子条件构成，每条原子条件形如 "α=0"、"β=1"、"γ=0"、"δ=1" 等

查询格式如下：
<query_count>
S = A,B,C
CONDITIONS = α=1
</query_count>

或者使用两个条件：
<query_count>
S = A,B,C,D
CONDITIONS = α=1,β=0
</query_count>

系统会返回一个非负整数，表示子集 S 中满足所有指定条件的元素数量。

注意事项：
- 子集 S 必须包含至少 3 个元素
- 条件集 L 最多包含 2 条原子条件
- 属性名必须是 α, β, γ, δ 之一
- 属性值必须是 0 或 1

## 提交答案格式

当你准备好提交答案时，请列出所有满足目标条件 T 的元素（用逗号分隔，顺序不限）：

<answer>A,C,E</answer>

如果你认为没有元素满足条件，请提交空集：

<answer></answer>

请尽可能用最少的查询次数找到正确答案。
"""

    game_rule_en = """\
Let's play an "Attribute Deduction" game. Here are the rules:

The game has a set U containing {n} elements, identified as {elements}. Each element has four binary attributes α, β, γ, δ, where each attribute takes value 0 or 1, but the specific values are hidden.

Your goal is to find all elements that satisfy a specific target condition T. The target condition T is defined as: α=1 and β=0 and γ=1 and δ=0.

You can obtain information through COUNT queries. Each query requires specifying a subset and some conditions, and the system will tell you how many elements in that subset satisfy those conditions. When you have collected enough information, submit your final answer.

## COUNT Query Format

Each COUNT query needs to specify:
1. A subset S containing at least 3 elements
2. A condition set L consisting of 1 or 2 atomic conditions, each atomic condition is like "α=0", "β=1", "γ=0", "δ=1", etc.

Query format:
<query_count>
S = A,B,C
CONDITIONS = α=1
</query_count>

Or using two conditions:
<query_count>
S = A,B,C,D
CONDITIONS = α=1,β=0
</query_count>

The system will return a non-negative integer indicating the number of elements in subset S that satisfy all specified conditions.

Notes:
- Subset S must contain at least 3 elements
- Condition set L can contain at most 2 atomic conditions
- Attribute names must be one of α, β, γ, δ
- Attribute values must be 0 or 1

## Answer Submission Format

When you are ready to submit your answer, list all elements that satisfy the target condition T (comma-separated, order does not matter):

<answer>A,C,E</answer>

If you believe no elements satisfy the condition, submit an empty set:

<answer></answer>

Please try to find the correct answer with the minimum number of queries.
"""

    contextualized_rule_zh_1 = """\
我们现在来进行一项"自动驾驶风险排查"任务，规则如下：

系统记录了一个包含 {n} 辆自动驾驶测试车辆的集合 U，车辆分别以 {elements} 标识。每辆车具有四个二元配置属性 α, β, γ, δ，每个属性的状态为 0 或 1，具体状态被系统加密隐藏。

你的目标是找出满足高风险目标条件 T 的所有车辆。目标条件 T 定义为：α=1 且 β=0 且 γ=1 且 δ=0。

你可以通过 COUNT 查询来获取批量数据，每次查询需要指定一个车辆子集和一些条件，系统会告诉你该子集中有多少辆车满足这些条件。当你收集足够信息后，请提交最终的排查结果。

## COUNT 查询格式

每次 COUNT 查询需要指定：
1. 一个车辆子集 S，包含至少 3 辆车
2. 一个条件集 L，由 1 或 2 条原子条件构成，每条原子条件形如 "α=0"、"β=1"、"γ=0"、"δ=1" 等

查询格式如下：
<query_count>
S = A,B,C
CONDITIONS = α=1
</query_count>

或者使用两个条件：
<query_count>
S = A,B,C,D
CONDITIONS = α=1,β=0
</query_count>

系统会返回一个非负整数，表示子集 S 中满足所有指定条件的车辆数量。

注意事项：
- 车辆子集 S 必须包含至少 3 辆车
- 条件集 L 最多包含 2 条原子条件
- 属性名必须是 α, β, γ, δ 之一
- 属性值必须是 0 或 1

## 提交答案格式

当你准备好提交排查结果时，请列出所有满足目标条件 T 的车辆（用逗号分隔，顺序不限）：

<answer>A,C,E</answer>

如果你认为没有任何车辆满足条件，请提交空集：

<answer></answer>

请尽可能用最少的查询次数找到所有高风险车辆。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's perform an "Autonomous Driving Risk Assessment" task. Here are the rules:

The system has logged a set U containing {n} autonomous test vehicles, identified as {elements}. Each vehicle has four binary configuration attributes α, β, γ, δ, where each attribute takes a state of 0 or 1, but the specific states are encrypted and hidden.

Your goal is to find all vehicles that satisfy the high-risk target condition T. The target condition T is defined as: α=1 and β=0 and γ=1 and δ=0.

You can obtain batch data through COUNT queries. Each query requires specifying a subset of vehicles and some conditions, and the system will tell you how many vehicles in that subset satisfy those conditions. When you have collected enough information, submit your final assessment result.

## COUNT Query Format

Each COUNT query needs to specify:
1. A vehicle subset S containing at least 3 vehicles
2. A condition set L consisting of 1 or 2 atomic conditions, each atomic condition is like "α=0", "β=1", "γ=0", "δ=1", etc.

Query format:
<query_count>
S = A,B,C
CONDITIONS = α=1
</query_count>

Or using two conditions:
<query_count>
S = A,B,C,D
CONDITIONS = α=1,β=0
</query_count>

The system will return a non-negative integer indicating the number of vehicles in subset S that satisfy all specified conditions.

Notes:
- Vehicle subset S must contain at least 3 vehicles
- Condition set L can contain at most 2 atomic conditions
- Attribute names must be one of α, β, γ, δ
- Attribute values must be 0 or 1

## Answer Submission Format

When you are ready to submit your assessment result, list all vehicles that satisfy the target condition T (comma-separated, order does not matter):

<answer>A,C,E</answer>

If you believe no vehicles satisfy the condition, submit an empty set:

<answer></answer>

Please try to find all high-risk vehicles with the minimum number of queries.
"""

    contextualized_rule_zh_2 = """\
我们现在来进行一项"罕见综合征确诊"任务，规则如下：

医疗数据库中包含一个有 {n} 份患者病历的集合 U，病历分别以 {elements} 标识。每份病历记录了四个二元临床指标 α, β, γ, δ，每个指标的检验结果为 0 或 1，但具体结果目前被隐藏。

你的目标是找出满足确诊目标条件 T 的所有病历。确诊条件 T 定义为：α=1 且 β=0 且 γ=1 且 δ=0。

你可以通过 COUNT 抽查来获取统计信息，每次查询需要指定一个病历子集和一些指标条件，系统会告诉你该子集中有多少份病历满足这些条件。当你收集足够信息后，请提交最终的确诊名单。

## COUNT 查询格式

每次 COUNT 查询需要指定：
1. 一个病历子集 S，包含至少 3 份病历
2. 一个条件集 L，由 1 或 2 条原子条件构成，每条原子条件形如 "α=0"、"β=1"、"γ=0"、"δ=1" 等

查询格式如下：
<query_count>
S = A,B,C
CONDITIONS = α=1
</query_count>

或者使用两个条件：
<query_count>
S = A,B,C,D
CONDITIONS = α=1,β=0
</query_count>

系统会返回一个非负整数，表示子集 S 中满足所有指定条件的病历数量。

注意事项：
- 病历子集 S 必须包含至少 3 份病历
- 条件集 L 最多包含 2 条原子条件
- 属性名必须是 α, β, γ, δ 之一
- 属性值必须是 0 或 1

## 提交答案格式

当你准备好提交确诊名单时，请列出所有满足目标条件 T 的病历（用逗号分隔，顺序不限）：

<answer>A,C,E</answer>

如果你认为没有任何病历满足条件，请提交空集：

<answer></answer>

请尽可能用最少的查询次数找到所有确诊病历。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's perform a "Rare Syndrome Diagnosis" task. Here are the rules:

The medical database has a set U containing {n} patient records, identified as {elements}. Each record has four binary clinical indicators α, β, γ, δ, where each indicator takes a result of 0 or 1, but the specific results are currently hidden.

Your goal is to find all records that satisfy the diagnostic target condition T. The target condition T is defined as: α=1 and β=0 and γ=1 and δ=0.

You can obtain statistical information through COUNT queries. Each query requires specifying a subset of medical records and some indicator conditions, and the system will tell you how many records in that subset satisfy those conditions. When you have collected enough information, submit your final diagnostic list.

## COUNT Query Format

Each COUNT query needs to specify:
1. A medical record subset S containing at least 3 records
2. A condition set L consisting of 1 or 2 atomic conditions, each atomic condition is like "α=0", "β=1", "γ=0", "δ=1", etc.

Query format:
<query_count>
S = A,B,C
CONDITIONS = α=1
</query_count>

Or using two conditions:
<query_count>
S = A,B,C,D
CONDITIONS = α=1,β=0
</query_count>

The system will return a non-negative integer indicating the number of records in subset S that satisfy all specified conditions.

Notes:
- Medical record subset S must contain at least 3 records
- Condition set L can contain at most 2 atomic conditions
- Attribute names must be one of α, β, γ, δ
- Attribute values must be 0 or 1

## Answer Submission Format

When you are ready to submit your diagnostic list, list all records that satisfy the target condition T (comma-separated, order does not matter):

<answer>A,C,E</answer>

If you believe no records satisfy the condition, submit an empty set:

<answer></answer>

Please try to find all confirmed records with the minimum number of queries.
"""

    contextualized_rule_zh_3 = """\
我们现在来进行一项"创新潜能学生筛查"任务，规则如下：

教育系统中包含一个有 {n} 名学生档案的集合 U，学生分别以 {elements} 标识。每名学生拥有四个二元能力指标 α, β, γ, δ，每个指标的评估等级为 0 或 1，但具体评估结果处于保密状态。

你的目标是找出满足潜能开发目标条件 T 的所有学生。目标条件 T 定义为：α=1 且 β=0 且 γ=1 且 δ=0。

你可以通过 COUNT 评估来获取群体分析信息，每次查询需要指定一个学生子集和一些指标条件，系统会告诉你该子集中有多少名学生满足这些条件。当你收集足够信息后，请提交最终的入选名单。

## COUNT 查询格式

每次 COUNT 查询需要指定：
1. 一个学生子集 S，包含至少 3 名学生
2. 一个条件集 L，由 1 或 2 条原子条件构成，每条原子条件形如 "α=0"、"β=1"、"γ=0"、"δ=1" 等

查询格式如下：
<query_count>
S = A,B,C
CONDITIONS = α=1
</query_count>

或者使用两个条件：
<query_count>
S = A,B,C,D
CONDITIONS = α=1,β=0
</query_count>

系统会返回一个非负整数，表示子集 S 中满足所有指定条件的学生数量。

注意事项：
- 学生子集 S 必须包含至少 3 名学生
- 条件集 L 最多包含 2 条原子条件
- 属性名必须是 α, β, γ, δ 之一
- 属性值必须是 0 或 1

## 提交答案格式

当你准备好提交入选名单时，请列出所有满足目标条件 T 的学生（用逗号分隔，顺序不限）：

<answer>A,C,E</answer>

如果你认为没有任何学生满足条件，请提交空集：

<answer></answer>

请尽可能用最少的查询次数找到所有具备潜能的学生。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's perform an "Innovative Potential Student Screening" task. Here are the rules:

The education system has a set U containing {n} student profiles, identified as {elements}. Each student has four binary ability indicators α, β, γ, δ, where each indicator takes an evaluation level of 0 or 1, but the specific evaluation results are classified.

Your goal is to find all students that satisfy the potential development target condition T. The target condition T is defined as: α=1 and β=0 and γ=1 and δ=0.

You can obtain cohort analysis information through COUNT queries. Each query requires specifying a subset of students and some indicator conditions, and the system will tell you how many students in that subset satisfy those conditions. When you have collected enough information, submit your final shortlist.

## COUNT Query Format

Each COUNT query needs to specify:
1. A student subset S containing at least 3 students
2. A condition set L consisting of 1 or 2 atomic conditions, each atomic condition is like "α=0", "β=1", "γ=0", "δ=1", etc.

Query format:
<query_count>
S = A,B,C
CONDITIONS = α=1
</query_count>

Or using two conditions:
<query_count>
S = A,B,C,D
CONDITIONS = α=1,β=0
</query_count>

The system will return a non-negative integer indicating the number of students in subset S that satisfy all specified conditions.

Notes:
- Student subset S must contain at least 3 students
- Condition set L can contain at most 2 atomic conditions
- Attribute names must be one of α, β, γ, δ
- Attribute values must be 0 or 1

## Answer Submission Format

When you are ready to submit your shortlist, list all students that satisfy the target condition T (comma-separated, order does not matter):

<answer>A,C,E</answer>

If you believe no students satisfy the condition, submit an empty set:

<answer></answer>

Please try to find all qualified students with the minimum number of queries.
"""

    contextualized_rule_zh_4 = """\
我们现在来进行一项"装配线缺陷零件排查"任务，规则如下：

质检系统锁定了一个包含 {n} 个关键零部件的集合 U，零部件分别以 {elements} 标识。每个零部件具有四个二元工艺属性 α, β, γ, δ，每个属性的检测值为 0 或 1，但具体检测结果尚未直接公开。

你的目标是找出满足特定缺陷目标条件 T 的所有零部件。缺陷条件 T 定义为：α=1 且 β=0 且 γ=1 且 δ=0。

你可以通过 COUNT 质检来获取抽样反馈，每次查询需要指定一个零部件子集和一些工艺条件，系统会告诉你该子集中有多少个零部件满足这些条件。当你收集足够信息后，请提交最终的缺陷零件清单。

## COUNT 查询格式

每次 COUNT 查询需要指定：
1. 一个零部件子集 S，包含至少 3 个零部件
2. 一个条件集 L，由 1 或 2 条原子条件构成，每条原子条件形如 "α=0"、"β=1"、"γ=0"、"δ=1" 等

查询格式如下：
<query_count>
S = A,B,C
CONDITIONS = α=1
</query_count>

或者使用两个条件：
<query_count>
S = A,B,C,D
CONDITIONS = α=1,β=0
</query_count>

系统会返回一个非负整数，表示子集 S 中满足所有指定条件的零部件数量。

注意事项：
- 零部件子集 S 必须包含至少 3 个零部件
- 条件集 L 最多包含 2 条原子条件
- 属性名必须是 α, β, γ, δ 之一
- 属性值必须是 0 或 1

## 提交答案格式

当你准备好提交清单时，请列出所有满足目标条件 T 的零部件（用逗号分隔，顺序不限）：

<answer>A,C,E</answer>

如果你认为没有任何零部件满足条件，请提交空集：

<answer></answer>

请尽可能用最少的查询次数找到所有缺陷零部件。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's perform an "Assembly Line Defective Parts Troubleshooting" task. Here are the rules:

The quality control system has a set U containing {n} key components, identified as {elements}. Each component has four binary process attributes α, β, γ, δ, where each attribute takes a test value of 0 or 1, but the specific test results are not yet directly disclosed.

Your goal is to find all components that satisfy the specific defect target condition T. The target condition T is defined as: α=1 and β=0 and γ=1 and δ=0.

You can obtain sampling feedback through COUNT queries. Each query requires specifying a subset of components and some process conditions, and the system will tell you how many components in that subset satisfy those conditions. When you have collected enough information, submit your final defective parts list.

## COUNT Query Format

Each COUNT query needs to specify:
1. A component subset S containing at least 3 components
2. A condition set L consisting of 1 or 2 atomic conditions, each atomic condition is like "α=0", "β=1", "γ=0", "δ=1", etc.

Query format:
<query_count>
S = A,B,C
CONDITIONS = α=1
</query_count>

Or using two conditions:
<query_count>
S = A,B,C,D
CONDITIONS = α=1,β=0
</query_count>

The system will return a non-negative integer indicating the number of components in subset S that satisfy all specified conditions.

Notes:
- Component subset S must contain at least 3 components
- Condition set L can contain at most 2 atomic conditions
- Attribute names must be one of α, β, γ, δ
- Attribute values must be 0 or 1

## Answer Submission Format

When you are ready to submit your list, list all components that satisfy the target condition T (comma-separated, order does not matter):

<answer>A,C,E</answer>

If you believe no components satisfy the condition, submit an empty set:

<answer></answer>

Please try to find all defective components with the minimum number of queries.
"""

    contextualized_rule_zh_5 = """\
我们现在来进行一项"连环商业诈骗案嫌疑公司锁定"任务，规则如下：

工商稽查库中包含一个有 {n} 家嫌疑公司的集合 U，公司分别以 {elements} 标识。每家公司涉及四个二元工商财务特征 α, β, γ, δ，每个特征的判定值为 0 或 1，但具体档案处于封存状态。

你的目标是找出满足高嫌疑目标条件 T 的所有公司。高嫌疑条件 T 定义为：α=1 且 β=0 且 γ=1 且 δ=0。

你可以通过 COUNT 核查来获取协查通报，每次查询需要指定一个公司子集和一些特征条件，系统会告诉你该子集中有多少家公司满足这些条件。当你收集足够信息后，请提交最终的嫌疑公司名单。

## COUNT 查询格式

每次 COUNT 查询需要指定：
1. 一个公司子集 S，包含至少 3 家公司
2. 一个条件集 L，由 1 或 2 条原子条件构成，每条原子条件形如 "α=0"、"β=1"、"γ=0"、"δ=1" 等

查询格式如下：
<query_count>
S = A,B,C
CONDITIONS = α=1
</query_count>

或者使用两个条件：
<query_count>
S = A,B,C,D
CONDITIONS = α=1,β=0
</query_count>

系统会返回一个非负整数，表示子集 S 中满足所有指定条件的公司数量。

注意事项：
- 公司子集 S 必须包含至少 3 家公司
- 条件集 L 最多包含 2 条原子条件
- 属性名必须是 α, β, γ, δ 之一
- 属性值必须是 0 或 1

## 提交答案格式

当你准备好提交名单时，请列出所有满足目标条件 T 的公司（用逗号分隔，顺序不限）：

<answer>A,C,E</answer>

如果你认为没有任何公司满足条件，请提交空集：

<answer></answer>

请尽可能用最少的查询次数锁定所有嫌疑公司。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's perform a "Serial Commercial Fraud Suspect Company Targeting" task. Here are the rules:

The business inspection database has a set U containing {n} suspect companies, identified as {elements}. Each company involves four binary business and financial features α, β, γ, δ, where each feature takes a judgment value of 0 or 1, but the specific files are sealed.

Your goal is to find all companies that satisfy the high-suspicion target condition T. The target condition T is defined as: α=1 and β=0 and γ=1 and δ=0.

You can obtain inspection bulletins through COUNT queries. Each query requires specifying a subset of companies and some feature conditions, and the system will tell you how many companies in that subset satisfy those conditions. When you have collected enough information, submit your final suspect company list.

## COUNT Query Format

Each COUNT query needs to specify:
1. A company subset S containing at least 3 companies
2. A condition set L consisting of 1 or 2 atomic conditions, each atomic condition is like "α=0", "β=1", "γ=0", "δ=1", etc.

Query format:
<query_count>
S = A,B,C
CONDITIONS = α=1
</query_count>

Or using two conditions:
<query_count>
S = A,B,C,D
CONDITIONS = α=1,β=0
</query_count>

The system will return a non-negative integer indicating the number of companies in subset S that satisfy all specified conditions.

Notes:
- Company subset S must contain at least 3 companies
- Condition set L can contain at most 2 atomic conditions
- Attribute names must be one of α, β, γ, δ
- Attribute values must be 0 or 1

## Answer Submission Format

When you are ready to submit your list, list all companies that satisfy the target condition T (comma-separated, order does not matter):

<answer>A,C,E</answer>

If you believe no companies satisfy the condition, submit an empty set:

<answer></answer>

Please try to find all suspect companies with the minimum number of queries.
"""

    tags = ["answer", "query_count"]
    
    reasoning_type = "演绎推理"
    data_structure = "集合"

    # 难度说明：
    # 1 (简单)      - 12个元素，2个满足目标条件
    # 2 (中等偏下)  - 12个元素，3个满足目标条件
    # 3 (中等偏上)  - 12个元素，1个满足目标条件
    # 4 (较难)      - 12个元素，4个满足目标条件
    # 5 (难)        - 12个元素，0个满足目标条件

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 12,
                "elements": "A,B,C,D,E,F,G,H,I,J,K,L",
                # 目标条件：α=1 且 β=0 且 γ=1 且 δ=0
                "attributes": {
                    "A": {"α": 1, "β": 0, "γ": 1, "δ": 0},  # 满足
                    "B": {"α": 0, "β": 0, "γ": 1, "δ": 0},
                    "C": {"α": 1, "β": 1, "γ": 1, "δ": 0},
                    "D": {"α": 1, "β": 0, "γ": 0, "δ": 0},
                    "E": {"α": 1, "β": 0, "γ": 1, "δ": 1},
                    "F": {"α": 1, "β": 0, "γ": 1, "δ": 0},  # 满足
                    "G": {"α": 0, "β": 1, "γ": 0, "δ": 1},
                    "H": {"α": 1, "β": 1, "γ": 0, "δ": 0},
                    "I": {"α": 0, "β": 0, "γ": 0, "δ": 1},
                    "J": {"α": 1, "β": 0, "γ": 0, "δ": 1},
                    "K": {"α": 0, "β": 1, "γ": 1, "δ": 0},
                    "L": {"α": 1, "β": 1, "γ": 1, "δ": 1},
                }
            },
            2: {
                "n": 12,
                "elements": "A,B,C,D,E,F,G,H,I,J,K,L",
                "attributes": {
                    "A": {"α": 1, "β": 0, "γ": 1, "δ": 0},  # 满足
                    "B": {"α": 0, "β": 1, "γ": 0, "δ": 1},
                    "C": {"α": 1, "β": 0, "γ": 1, "δ": 0},  # 满足
                    "D": {"α": 1, "β": 1, "γ": 1, "δ": 0},
                    "E": {"α": 0, "β": 0, "γ": 0, "δ": 1},
                    "F": {"α": 1, "β": 0, "γ": 0, "δ": 0},
                    "G": {"α": 0, "β": 1, "γ": 1, "δ": 1},
                    "H": {"α": 1, "β": 0, "γ": 1, "δ": 0},  # 满足
                    "I": {"α": 1, "β": 1, "γ": 0, "δ": 0},
                    "J": {"α": 0, "β": 0, "γ": 1, "δ": 1},
                    "K": {"α": 1, "β": 0, "γ": 0, "δ": 1},
                    "L": {"α": 0, "β": 1, "γ": 0, "δ": 0},
                }
            },
            3: {
                "n": 12,
                "elements": "A,B,C,D,E,F,G,H,I,J,K,L",
                "attributes": {
                    "A": {"α": 0, "β": 1, "γ": 0, "δ": 1},
                    "B": {"α": 1, "β": 1, "γ": 1, "δ": 0},
                    "C": {"α": 0, "β": 0, "γ": 0, "δ": 1},
                    "D": {"α": 1, "β": 0, "γ": 0, "δ": 0},
                    "E": {"α": 0, "β": 1, "γ": 1, "δ": 1},
                    "F": {"α": 1, "β": 0, "γ": 1, "δ": 1},
                    "G": {"α": 1, "β": 0, "γ": 1, "δ": 0},  # 满足
                    "H": {"α": 0, "β": 1, "γ": 0, "δ": 0},
                    "I": {"α": 1, "β": 1, "γ": 0, "δ": 1},
                    "J": {"α": 0, "β": 0, "γ": 1, "δ": 0},
                    "K": {"α": 1, "β": 1, "γ": 1, "δ": 1},
                    "L": {"α": 0, "β": 0, "γ": 0, "δ": 0},
                }
            },
            4: {
                "n": 12,
                "elements": "A,B,C,D,E,F,G,H,I,J,K,L",
                "attributes": {
                    "A": {"α": 1, "β": 0, "γ": 1, "δ": 0},  # 满足
                    "B": {"α": 1, "β": 1, "γ": 0, "δ": 1},
                    "C": {"α": 1, "β": 0, "γ": 1, "δ": 0},  # 满足
                    "D": {"α": 0, "β": 1, "γ": 0, "δ": 0},
                    "E": {"α": 1, "β": 0, "γ": 1, "δ": 0},  # 满足
                    "F": {"α": 0, "β": 0, "γ": 1, "δ": 1},
                    "G": {"α": 1, "β": 1, "γ": 1, "δ": 1},
                    "H": {"α": 0, "β": 1, "γ": 0, "δ": 1},
                    "I": {"α": 1, "β": 0, "γ": 0, "δ": 0},
                    "J": {"α": 1, "β": 0, "γ": 1, "δ": 0},  # 满足
                    "K": {"α": 0, "β": 0, "γ": 0, "δ": 1},
                    "L": {"α": 1, "β": 1, "γ": 0, "δ": 0},
                }
            },
            5: {
                "n": 12,
                "elements": "A,B,C,D,E,F,G,H,I,J,K,L",
                "attributes": {
                    "A": {"α": 0, "β": 1, "γ": 0, "δ": 1},
                    "B": {"α": 1, "β": 1, "γ": 1, "δ": 1},
                    "C": {"α": 0, "β": 0, "γ": 0, "δ": 0},
                    "D": {"α": 1, "β": 1, "γ": 0, "δ": 0},
                    "E": {"α": 0, "β": 1, "γ": 1, "δ": 1},
                    "F": {"α": 1, "β": 0, "γ": 0, "δ": 1},
                    "G": {"α": 0, "β": 0, "γ": 1, "δ": 1},
                    "H": {"α": 1, "β": 1, "γ": 0, "δ": 1},
                    "I": {"α": 0, "β": 1, "γ": 0, "δ": 0},
                    "J": {"α": 1, "β": 0, "γ": 0, "δ": 0},
                    "K": {"α": 1, "β": 1, "γ": 1, "δ": 0},
                    "L": {"α": 0, "β": 0, "γ": 0, "δ": 1},
                }
            },
        },
        "en": {
            1: {
                "n": 12,
                "elements": "A,B,C,D,E,F,G,H,I,J,K,L",
                "attributes": {
                    "A": {"α": 1, "β": 0, "γ": 1, "δ": 0},  # satisfies
                    "B": {"α": 0, "β": 0, "γ": 1, "δ": 0},
                    "C": {"α": 1, "β": 1, "γ": 1, "δ": 0},
                    "D": {"α": 1, "β": 0, "γ": 0, "δ": 0},
                    "E": {"α": 1, "β": 0, "γ": 1, "δ": 1},
                    "F": {"α": 1, "β": 0, "γ": 1, "δ": 0},  # satisfies
                    "G": {"α": 0, "β": 1, "γ": 0, "δ": 1},
                    "H": {"α": 1, "β": 1, "γ": 0, "δ": 0},
                    "I": {"α": 0, "β": 0, "γ": 0, "δ": 1},
                    "J": {"α": 1, "β": 0, "γ": 0, "δ": 1},
                    "K": {"α": 0, "β": 1, "γ": 1, "δ": 0},
                    "L": {"α": 1, "β": 1, "γ": 1, "δ": 1},
                }
            },
            2: {
                "n": 12,
                "elements": "A,B,C,D,E,F,G,H,I,J,K,L",
                "attributes": {
                    "A": {"α": 1, "β": 0, "γ": 1, "δ": 0},  # satisfies
                    "B": {"α": 0, "β": 1, "γ": 0, "δ": 1},
                    "C": {"α": 1, "β": 0, "γ": 1, "δ": 0},  # satisfies
                    "D": {"α": 1, "β": 1, "γ": 1, "δ": 0},
                    "E": {"α": 0, "β": 0, "γ": 0, "δ": 1},
                    "F": {"α": 1, "β": 0, "γ": 0, "δ": 0},
                    "G": {"α": 0, "β": 1, "γ": 1, "δ": 1},
                    "H": {"α": 1, "β": 0, "γ": 1, "δ": 0},  # satisfies
                    "I": {"α": 1, "β": 1, "γ": 0, "δ": 0},
                    "J": {"α": 0, "β": 0, "γ": 1, "δ": 1},
                    "K": {"α": 1, "β": 0, "γ": 0, "δ": 1},
                    "L": {"α": 0, "β": 1, "γ": 0, "δ": 0},
                }
            },
            3: {
                "n": 12,
                "elements": "A,B,C,D,E,F,G,H,I,J,K,L",
                "attributes": {
                    "A": {"α": 0, "β": 1, "γ": 0, "δ": 1},
                    "B": {"α": 1, "β": 1, "γ": 1, "δ": 0},
                    "C": {"α": 0, "β": 0, "γ": 0, "δ": 1},
                    "D": {"α": 1, "β": 0, "γ": 0, "δ": 0},
                    "E": {"α": 0, "β": 1, "γ": 1, "δ": 1},
                    "F": {"α": 1, "β": 0, "γ": 1, "δ": 1},
                    "G": {"α": 1, "β": 0, "γ": 1, "δ": 0},  # satisfies
                    "H": {"α": 0, "β": 1, "γ": 0, "δ": 0},
                    "I": {"α": 1, "β": 1, "γ": 0, "δ": 1},
                    "J": {"α": 0, "β": 0, "γ": 1, "δ": 0},
                    "K": {"α": 1, "β": 1, "γ": 1, "δ": 1},
                    "L": {"α": 0, "β": 0, "γ": 0, "δ": 0},
                }
            },
            4: {
                "n": 12,
                "elements": "A,B,C,D,E,F,G,H,I,J,K,L",
                "attributes": {
                    "A": {"α": 1, "β": 0, "γ": 1, "δ": 0},  # satisfies
                    "B": {"α": 1, "β": 1, "γ": 0, "δ": 1},
                    "C": {"α": 1, "β": 0, "γ": 1, "δ": 0},  # satisfies
                    "D": {"α": 0, "β": 1, "γ": 0, "δ": 0},
                    "E": {"α": 1, "β": 0, "γ": 1, "δ": 0},  # satisfies
                    "F": {"α": 0, "β": 0, "γ": 1, "δ": 1},
                    "G": {"α": 1, "β": 1, "γ": 1, "δ": 1},
                    "H": {"α": 0, "β": 1, "γ": 0, "δ": 1},
                    "I": {"α": 1, "β": 0, "γ": 0, "δ": 0},
                    "J": {"α": 1, "β": 0, "γ": 1, "δ": 0},  # satisfies
                    "K": {"α": 0, "β": 0, "γ": 0, "δ": 1},
                    "L": {"α": 1, "β": 1, "γ": 0, "δ": 0},
                }
            },
            5: {
                "n": 12,
                "elements": "A,B,C,D,E,F,G,H,I,J,K,L",
                "attributes": {
                    "A": {"α": 0, "β": 1, "γ": 0, "δ": 1},
                    "B": {"α": 1, "β": 1, "γ": 1, "δ": 1},
                    "C": {"α": 0, "β": 0, "γ": 0, "δ": 0},
                    "D": {"α": 1, "β": 1, "γ": 0, "δ": 0},
                    "E": {"α": 0, "β": 1, "γ": 1, "δ": 1},
                    "F": {"α": 1, "β": 0, "γ": 0, "δ": 1},
                    "G": {"α": 0, "β": 0, "γ": 1, "δ": 1},
                    "H": {"α": 1, "β": 1, "γ": 0, "δ": 1},
                    "I": {"α": 0, "β": 1, "γ": 0, "δ": 0},
                    "J": {"α": 1, "β": 0, "γ": 0, "δ": 0},
                    "K": {"α": 1, "β": 1, "γ": 1, "δ": 0},
                    "L": {"α": 0, "β": 0, "γ": 0, "δ": 1},
                }
            },
        }
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：根据语言和难度选择配置"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["elements"] = cfg["elements"]
        
        # 存储每个元素的属性
        self.attributes = cfg["attributes"]
        
        # 计算满足目标条件 T (α=1 且 β=0 且 γ=1 且 δ=0) 的元素集合
        self.target_elements = set()
        for elem, attrs in self.attributes.items():
            if attrs["α"] == 1 and attrs["β"] == 0 and attrs["γ"] == 1 and attrs["δ"] == 0:
                self.target_elements.add(elem)

    def _parse_query_count(self, query_str):
        """
        解析 COUNT 查询字符串
        返回：(subset, conditions) 或抛出异常
        """
        lines = [line.strip() for line in query_str.strip().split('\n') if line.strip()]
        
        subset = None
        conditions = None
        
        for line in lines:
            if line.startswith("S =") or line.startswith("S="):
                subset_str = line.split('=', 1)[1].strip()
                subset = set(e.strip() for e in subset_str.split(',') if e.strip())
            elif line.startswith("CONDITIONS =") or line.startswith("CONDITIONS="):
                cond_str = line.split('=', 1)[1].strip()
                conditions = [c.strip() for c in cond_str.split(',') if c.strip()]
        
        if subset is None or conditions is None:
            raise ValueError("Query format error: missing S or CONDITIONS")
        
        return subset, conditions

    def _validate_and_count(self, subset, conditions):
        """
        验证查询并返回计数结果
        """
        # 验证子集大小
        if len(subset) < 3:
            if self.config.language == "zh":
                return "INVALID: 子集 S 必须包含至少 3 个元素"
            else:
                return "INVALID: Subset S must contain at least 3 elements"
        
        # 验证元素是否有效
        for elem in subset:
            if elem not in self.attributes:
                if self.config.language == "zh":
                    return f"INVALID: 元素 {elem} 不在集合 U 中"
                else:
                    return f"INVALID: Element {elem} is not in set U"
        
        # 验证条件数量
        if len(conditions) == 0 or len(conditions) > 2:
            if self.config.language == "zh":
                return "INVALID: 条件数量必须为 1 或 2"
            else:
                return "INVALID: Number of conditions must be 1 or 2"
        
        # 属性名归一化映射：支持多种可能的输入形式
        ATTR_NORMALIZE = {
            'α': 'α', 'alpha': 'α', 'ɑ': 'α',
            'β': 'β', 'beta': 'β',
            'γ': 'γ', 'gamma': 'γ',
            'δ': 'δ', 'delta': 'δ',
        }
        
        # 解析并验证条件
        parsed_conditions = []
        for cond in conditions:
            # 更宽松的匹配：允许各种属性名写法
            match = re.match(r'^(\S+)\s*=\s*([01])$', cond.strip())
            if not match:
                if self.config.language == "zh":
                    return f"INVALID: 条件格式错误: {cond}"
                else:
                    return f"INVALID: Invalid condition format: {cond}"
            raw_attr, attr_value = match.groups()
            normalized_attr = ATTR_NORMALIZE.get(raw_attr.lower(), raw_attr)
            
            if normalized_attr not in ['α', 'β', 'γ', 'δ']:
                if self.config.language == "zh":
                    return f"INVALID: 未知的属性名: {raw_attr}"
                else:
                    return f"INVALID: Unknown attribute name: {raw_attr}"
            
            parsed_conditions.append((normalized_attr, int(attr_value)))
        
        # 计算满足条件的元素数量
        count = 0
        for elem in subset:
            elem_attrs = self.attributes[elem]
            satisfies_all = True
            for attr_name, attr_value in parsed_conditions:
                if elem_attrs[attr_name] != attr_value:
                    satisfies_all = False
                    break
            if satisfies_all:
                count += 1
        
        return str(count)

    def evaluate(self, parsed_info):
        """评估提交的答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        # 处理空答案
        if not raw_ans:
            submitted_elements = set()
        else:
            submitted_elements = set(e.strip() for e in raw_ans.split(',') if e.strip())
        
        # 检查提交的元素是否都在集合 U 中
        for elem in submitted_elements:
            if elem not in self.attributes:
                return False
        
        # 比较提交的集合与真实的目标集合
        return submitted_elements == self.target_elements

    def _cf_core_produce(self, parsed_info):
        """原始的 produce_response 逻辑"""
        if "query_count" in parsed_info:
            query_str = parsed_info["query_count"]
            try:
                subset, conditions = self._parse_query_count(query_str)
                result = self._validate_and_count(subset, conditions)
                return result
            except Exception as e:
                if self.config.language == "zh":
                    return f"INVALID: 查询解析错误 - {str(e)}"
                else:
                    return f"INVALID: Query parsing error - {str(e)}"
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        """根据正确答案生成错误答案"""
        if correct.startswith("INVALID"):
            return correct + "_WRONG"
            
        # 若 correct 是纯整数字符串
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 否则替换关键词
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        else:
            # 简单的大小写不敏感匹配替换（这里简化处理，因为本游戏主要返回数字）
            if re.search(r'(?i)yes', correct):
                return re.sub(r'(?i)yes', 'No', correct)
            elif re.search(r'(?i)no', correct):
                return re.sub(r'(?i)no', 'Yes', correct)
        
        # 若都不匹配
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> List[Dict]:
        """
        枚举具有代表性的合法查询并返回对应的正确答案。
        
        使用不同子集和条件组合来提供足够的信息，
        使得可以唯一确定每个元素的属性值。
        """
        queries = []
        
        elements = [e.strip() for e in self._game_info["elements"].split(',')]
        
        attrs = ['α', 'β', 'γ', 'δ']
        vals = [0, 1]
        
        # 为每个属性生成一系列能区分各元素的查询
        # 策略：使用大小为 3 的滑动窗口子集，对每个属性进行单条件查询
        subsets_to_query = []
        n = len(elements)
        # 使用大小为 3 的连续子集
        for i in range(n - 2):
            subsets_to_query.append(elements[i:i+3])
        # 额外添加一些跨越式子集以增加区分度
        for i in range(0, n, 3):
            end = min(i + 3, n)
            if end - i >= 3:
                subsets_to_query.append(elements[i:end])
        # 去重
        seen = set()
        unique_subsets = []
        for s in subsets_to_query:
            key = tuple(s)
            if key not in seen:
                seen.add(key)
                unique_subsets.append(s)
        
        # 对每个子集，查询每个属性=1的计数
        for subset_list in unique_subsets:
            subset_set = set(subset_list)
            subset_str = ",".join(subset_list)
            for attr in attrs:
                cond = f"{attr}=1"
                query_text = f"S = {subset_str}\nCONDITIONS = {cond}"
                full_query = f"<query_count>\n{query_text}\n</query_count>"
                
                try:
                    ans = self._validate_and_count(subset_set, [cond])
                except Exception:
                    ans = "0"
                
                queries.append({
                    "query": full_query,
                    "answer": ans
                })
        
        # 同时保留全集的双条件查询（目标条件组合），用于直接推理
        full_subset_set = set(elements)
        full_subset_str = ",".join(elements)
        target_conds = [
            ["α=1", "β=0"],
            ["α=1", "γ=1"],
            ["α=1", "δ=0"],
            ["β=0", "γ=1"],
            ["β=0", "δ=0"],
            ["γ=1", "δ=0"],
        ]
        for conds in target_conds:
            cond_str = ",".join(conds)
            query_text = f"S = {full_subset_str}\nCONDITIONS = {cond_str}"
            full_query = f"<query_count>\n{query_text}\n</query_count>"
            
            try:
                ans = self._validate_and_count(full_subset_set, conds)
            except Exception:
                ans = "0"
            
            queries.append({
                "query": full_query,
                "answer": ans
            })
        
        return queries

