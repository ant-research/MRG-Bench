# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   排序结果：序列排序后第k位的元素是什么
# ============================================================

import re
import random
from typing import List, Dict
# [BUG FIX] 原问题：Python 3 的 sorted() 不支持 cmp 参数，需要使用 functools.cmp_to_key 将比较函数转换为 key
from functools import cmp_to_key
from .base import Game


class HiddenComparatorGame(Game):

    game_rule_zh = """\
我们来玩一个"隐藏比较器推理"游戏，规则如下：

游戏设定了一个隐藏的比较规则，用于对四位十进制数字进行排序。每个元素由四位数字构成，记为 (d1, d2, d3, d4)，每位数字在 0 到 9 之间，允许前导 0。

隐藏比较器包含：
1. 一个优先位序 P：即对四个位置 (1, 2, 3, 4) 的某一排列，决定比较时先看哪一位。
2. 每个优先位的比较方向：可以是"升序"或"降序"。
   - 升序：数字小的排在前面
   - 降序：数字大的排在前面

比较两个元素时，按优先位序 P 逐位比较对应位置的数字，遇到第一个不相等的位时，按该位的比较方向决定先后顺序。若四位数字完全相同则视为相同（但游戏中不会出现这种情况）。

游戏分为两个阶段：

## 训练阶段
你可以通过查询来推断隐藏的比较规则。提供两种查询方式：

1. 成对比较查询（COMPARE）
   - 提交两个元素，每个元素包含一个自定义 ID 和四位数字
   - 我会告诉你这两个元素按隐藏比较器的先后关系
   - 格式：
   <query_compare>ID1:d1d2d3d4,ID2:d1d2d3d4</query_compare>
   例如：<query_compare>A:1234,B:5678</query_compare>

2. 排位查询（SORT-K）
   - 提交一个练习序列（3 到 12 个元素），每个元素包含 ID 和四位数字，以及一个位置 k
   - 我会告诉你该序列按隐藏比较器排序后第 k 位是哪个元素的 ID
   - 格式：
   <query_sort>k=位置数;ID1:d1d2d3d4,ID2:d1d2d3d4,...</query_sort>
   例如：<query_sort>k=2;A:1234,B:5678,C:9012</query_sort>

注意：
- 所有查询中的四位数字组合必须两两不同
- 查询次数有限，请尽可能高效地推断规则
- 当前已使用查询次数：将在每次反馈后告知

## 决胜阶段
当你认为已经推断出比较规则后，我会给你一个正式序列（包含 {n} 个元素）和一个目标位置 k。你需要直接给出该序列按隐藏比较器排序后第 k 位元素的 ID，不能再进行任何查询。

提交最终答案的格式：
<answer>ID</answer>

例如：<answer>A</answer>

如果答案错误或格式不符，游戏失败。
"""

    game_rule_en = """\
Let's play a "Hidden Comparator Inference" game. Here are the rules:

The game has a hidden comparison rule for sorting four-digit decimal numbers. Each element consists of four digits, denoted as (d1, d2, d3, d4), where each digit is between 0 and 9, with leading zeros allowed.

The hidden comparator contains:
1. A priority position sequence P: a permutation of the four positions (1, 2, 3, 4), determining which digit to compare first.
2. A comparison direction for each priority position: either "ascending" or "descending".
   - Ascending: smaller digits come first
   - Descending: larger digits come first

When comparing two elements, we compare the digits at each position following the priority sequence P. At the first position where digits differ, the comparison direction of that position determines the order. If all four digits are identical, they are considered equal (but this won't happen in the game).

The game has two phases:

## Training Phase
You can infer the hidden comparison rule through queries. Two types of queries are available:

1. Pairwise Comparison Query (COMPARE)
   - Submit two elements, each with a custom ID and four digits
   - I will tell you the ordering of these two elements according to the hidden comparator
   - Format:
   <query_compare>ID1:d1d2d3d4,ID2:d1d2d3d4</query_compare>
   Example: <query_compare>A:1234,B:5678</query_compare>

2. Position Query (SORT-K)
   - Submit a practice sequence (3 to 12 elements), each with an ID and four digits, plus a position k
   - I will tell you which element's ID is at position k after sorting the sequence by the hidden comparator
   - Format:
   <query_sort>k=position;ID1:d1d2d3d4,ID2:d1d2d3d4,...</query_sort>
   Example: <query_sort>k=2;A:1234,B:5678,C:9012</query_sort>

Note:
- All four-digit combinations in queries must be distinct
- Query budget is limited, please infer the rule efficiently
- Current query count will be provided after each feedback

## Final Phase
When you believe you have inferred the comparison rule, I will give you a formal sequence (containing {n} elements) and a target position k. You must directly provide the ID of the element at position k after sorting by the hidden comparator, without making any further queries.

Final answer format:
<answer>ID</answer>

Example: <answer>A</answer>

If the answer is incorrect or the format is invalid, the game fails.
"""

    # -----------------------------------------------------
    # 新增场景化规则 1：交通
    # -----------------------------------------------------
    contextualized_rule_zh_1 = """\
我们来使用"隐藏路况评估系统"进行推理，规则如下：

交通管理中心设定了一个隐藏的道路拥堵度比较规则，用于对各个路段的通行状况进行排序。每个路段样本由四项交通流指标的量化值构成，记为 (d1, d2, d3, d4)，每位指标值在 0 到 9 之间，允许前导 0。

隐藏评估器包含：
1. 一个指标优先位序 P：即对四个维度位置 (1, 2, 3, 4) 的某一排列，决定比较时优先考察哪一项交通流指标。
2. 每个优先指标的比较方向：可以是"升序"或"降序"。
   - 升序：指标数值小的排在前面（即拥堵度更低，优先级更前）
   - 降序：指标数值大的排在前面

比较两个路段时，按优先位序 P 逐项比较对应位置的指标值，遇到第一个不相等的指标时，按该项的比较方向决定先后顺序。若四项指标完全相同则视为相同（但在本次测试中不会出现）。

系统测试分为两个阶段：

## 训练阶段
你可以通过系统查询来推断隐藏的路况评估规则。提供两种查询方式：

1. 成对比较查询（COMPARE）
   - 提交两个路段样本，每个样本包含一个自定义 ID 和四位交通流指标
   - 系统会反馈这两个样本按隐藏评估器的先后关系
   - 格式：
   <query_compare>ID1:d1d2d3d4,ID2:d1d2d3d4</query_compare>
   例如：<query_compare>A:1234,B:5678</query_compare>

2. 排位查询（SORT-K）
   - 提交一个测试序列（3 到 12 个样本），每个样本包含 ID 和四位指标，以及一个位置 k
   - 系统会反馈该序列按隐藏评估器排序后第 k 位是哪个样本的 ID
   - 格式：
   <query_sort>k=位置数;ID1:d1d2d3d4,ID2:d1d2d3d4,...</query_sort>
   例如：<query_sort>k=2;A:1234,B:5678,C:9012</query_sort>

注意：
- 所有查询中的四位指标组合必须两两不同
- 查询预算有限，请尽可能高效地推断规则
- 当前已使用查询次数：将在每次反馈后告知

## 决胜阶段
当你认为已经推断出评估规则后，系统会给出一个正式的监测序列（包含 {n} 个路段样本）和一个目标位置 k。你需要直接给出该序列按隐藏评估器排序后第 k 位样本的 ID，不能再进行任何查询。

提交最终答案的格式：
<answer>ID</answer>

例如：<answer>A</answer>

如果答案错误或格式不符，测试失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's use the 'Hidden Traffic Assessment System' for our inference task. Here are the rules:

The Traffic Management Center has set a hidden comparison rule for sorting the traffic congestion status of various road segments. Each road segment sample consists of quantified values for four traffic flow indicators, denoted as (d1, d2, d3, d4), where each indicator value is between 0 and 9, with leading zeros allowed.

The hidden evaluator contains:
1. A priority indicator sequence P: a permutation of the four dimension positions (1, 2, 3, 4), determining which traffic flow indicator is evaluated first.
2. A comparison direction for each priority indicator: either "ascending" or "descending".
   - Ascending: smaller indicator values come first (lower congestion, higher priority)
   - Descending: larger indicator values come first

When comparing two road segments, the system compares the indicator values at each position following the priority sequence P. At the first position where values differ, the comparison direction of that indicator determines the order. If all four indicators are identical, they are considered equal (but this won't happen in the test).

The test has two phases:

## Training Phase
You can infer the hidden assessment rule through system queries. Two types of queries are available:

1. Pairwise Comparison Query (COMPARE)
   - Submit two road segment samples, each with a custom ID and four traffic flow indicators
   - The system will tell you the ordering of these two samples according to the hidden evaluator
   - Format:
   <query_compare>ID1:d1d2d3d4,ID2:d1d2d3d4</query_compare>
   Example: <query_compare>A:1234,B:5678</query_compare>

2. Position Query (SORT-K)
   - Submit a test sequence (3 to 12 samples), each with an ID and four indicators, plus a position k
   - The system will tell you which sample's ID is at position k after sorting the sequence by the hidden evaluator
   - Format:
   <query_sort>k=position;ID1:d1d2d3d4,ID2:d1d2d3d4,...</query_sort>
   Example: <query_sort>k=2;A:1234,B:5678,C:9012</query_sort>

Note:
- All four-digit indicator combinations in queries must be distinct
- Query budget is limited, please infer the rule efficiently
- Current query count will be provided after each feedback

## Final Phase
When you believe you have inferred the assessment rule, the system will give you a formal monitoring sequence (containing {n} road segment samples) and a target position k. You must directly provide the ID of the sample at position k after sorting by the hidden evaluator, without making any further queries.

Final answer format:
<answer>ID</answer>

Example: <answer>A</answer>

If the answer is incorrect or the format is invalid, the test fails.
"""

    # -----------------------------------------------------
    # 新增场景化规则 2：医疗
    # -----------------------------------------------------
    contextualized_rule_zh_2 = """\
我们来进行"隐藏生命体征分诊"推理演练，规则如下：

急救中心设定了一个隐藏的危重度评估规则，用于对急诊病患的优先级别进行排序。每个病患样本由四项生命体征异常度的量化值构成，记为 (d1, d2, d3, d4)，每项异常值在 0 到 9 之间，允许前导 0。

隐藏评估器包含：
1. 一个体征优先位序 P：即对四个体征位置 (1, 2, 3, 4) 的某一排列，决定分诊时优先考察哪一项生命体征。
2. 每个优先体征的比较方向：可以是"升序"或"降序"。
   - 升序：异常数值小的病患排在前面
   - 降序：异常数值大的病患排在前面

比较两名病患时，按优先位序 P 逐项比较对应位置的体征异常值，遇到第一个不相等的数值时，按该项的比较方向决定先后顺序。若四项数值完全相同则视为相同（但在演练中不会出现）。

演练分为两个阶段：

## 训练阶段
你可以通过系统查询来推断隐藏的分诊规则。提供两种查询方式：

1. 成对比较查询（COMPARE）
   - 提交两个病患样本，每个包含一个自定义 ID 和四位生命体征异常值
   - 系统会反馈这两个样本按隐藏评估器的先后关系
   - 格式：
   <query_compare>ID1:d1d2d3d4,ID2:d1d2d3d4</query_compare>
   例如：<query_compare>A:1234,B:5678</query_compare>

2. 排位查询（SORT-K）
   - 提交一个测试序列（3 到 12 个病患），每个包含 ID 和四位异常值，以及一个位置 k
   - 系统会反馈该序列按隐藏评估器排序后第 k 位是哪个病患的 ID
   - 格式：
   <query_sort>k=位置数;ID1:d1d2d3d4,ID2:d1d2d3d4,...</query_sort>
   例如：<query_sort>k=2;A:1234,B:5678,C:9012</query_sort>

注意：
- 所有查询中的四位数值组合必须两两不同
- 查询预算有限，请尽可能高效地推断规则
- 当前已使用查询次数：将在每次反馈后告知

## 决胜阶段
当你认为已经推断出分诊规则后，系统会给出一个正式的待诊序列（包含 {n} 名病患）和一个目标位置 k。你需要直接给出该序列按隐藏评估器排序后第 k 位病患的 ID，不能再进行任何查询。

提交最终答案的格式：
<answer>ID</answer>

例如：<answer>A</answer>

如果答案错误或格式不符，演练失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct the 'Hidden Vitals Triage' inference drill. Here are the rules:

The Emergency Center has set a hidden severity assessment rule for sorting the priority levels of emergency patients. Each patient sample consists of quantified values for four vital sign abnormalities, denoted as (d1, d2, d3, d4), where each value is between 0 and 9, with leading zeros allowed.

The hidden evaluator contains:
1. A vitals priority sequence P: a permutation of the four vital positions (1, 2, 3, 4), determining which vital sign is evaluated first during triage.
2. A comparison direction for each priority vital: either "ascending" or "descending".
   - Ascending: patients with smaller abnormality values come first
   - Descending: patients with larger abnormality values come first

When comparing two patients, the system compares the abnormality values at each position following the priority sequence P. At the first position where values differ, the comparison direction of that vital determines the order. If all four values are identical, they are considered equal (but this won't happen in the drill).

The drill has two phases:

## Training Phase
You can infer the hidden triage rule through system queries. Two types of queries are available:

1. Pairwise Comparison Query (COMPARE)
   - Submit two patient samples, each with a custom ID and four vital sign abnormality values
   - The system will tell you the ordering of these two samples according to the hidden evaluator
   - Format:
   <query_compare>ID1:d1d2d3d4,ID2:d1d2d3d4</query_compare>
   Example: <query_compare>A:1234,B:5678</query_compare>

2. Position Query (SORT-K)
   - Submit a test sequence (3 to 12 patients), each with an ID and four abnormality values, plus a position k
   - The system will tell you which patient's ID is at position k after sorting the sequence by the hidden evaluator
   - Format:
   <query_sort>k=position;ID1:d1d2d3d4,ID2:d1d2d3d4,...</query_sort>
   Example: <query_sort>k=2;A:1234,B:5678,C:9012</query_sort>

Note:
- All four-digit value combinations in queries must be distinct
- Query budget is limited, please infer the rule efficiently
- Current query count will be provided after each feedback

## Final Phase
When you believe you have inferred the triage rule, the system will give you a formal waiting list sequence (containing {n} patients) and a target position k. You must directly provide the ID of the patient at position k after sorting by the hidden evaluator, without making any further queries.

Final answer format:
<answer>ID</answer>

Example: <answer>A</answer>

If the answer is incorrect or the format is invalid, the drill fails.
"""

    # -----------------------------------------------------
    # 新增场景化规则 3：教育
    # -----------------------------------------------------
    contextualized_rule_zh_3 = """\
我们来进行"隐藏素质评价体系"的推理挑战，规则如下：

教育局设定了一个隐藏的学生综合素质比较规则，用于对学生的各维表现进行排序。每个学生档案由四个素养模块（如德、智、体、美）的量化评分构成，记为 (d1, d2, d3, d4)，每项评分在 0 到 9 之间，允许前导 0。

隐藏评估器包含：
1. 一个素养优先位序 P：即对四个模块位置 (1, 2, 3, 4) 的某一排列，决定评价时优先考察哪一项素养。
2. 每个优先素养的比较方向：可以是"升序"或"降序"。
   - 升序：评分数值小的学生排在前面
   - 降序：评分数值大的学生排在前面

比较两名学生时，按优先位序 P 逐项比较对应位置的评分，遇到第一个不相等的评分时，按该项的比较方向决定先后顺序。若四项评分完全相同则视为相同（但在挑战中不会出现）。

挑战分为两个阶段：

## 训练阶段
你可以通过系统查询来推断隐藏的评价规则。提供两种查询方式：

1. 成对比较查询（COMPARE）
   - 提交两名学生档案，每个档案包含一个自定义 ID 和四位素养评分
   - 系统会反馈这两名学生按隐藏评估器的先后关系
   - 格式：
   <query_compare>ID1:d1d2d3d4,ID2:d1d2d3d4</query_compare>
   例如：<query_compare>A:1234,B:5678</query_compare>

2. 排位查询（SORT-K）
   - 提交一个测试序列（3 到 12 名学生），每个档案包含 ID 和四位评分，以及一个位置 k
   - 系统会反馈该序列按隐藏评估器排序后第 k 位是哪名学生的 ID
   - 格式：
   <query_sort>k=位置数;ID1:d1d2d3d4,ID2:d1d2d3d4,...</query_sort>
   例如：<query_sort>k=2;A:1234,B:5678,C:9012</query_sort>

注意：
- 所有查询中的四位评分组合必须两两不同
- 查询预算有限，请尽可能高效地推断规则
- 当前已使用查询次数：将在每次反馈后告知

## 决胜阶段
当你认为已经推断出评价规则后，系统会给出一个正式的考察序列（包含 {n} 名学生）和一个目标位置 k。你需要直接给出该序列按隐藏评估器排序后第 k 位学生的 ID，不能再进行任何查询。

提交最终答案的格式：
<answer>ID</answer>

例如：<answer>A</answer>

如果答案错误或格式不符，挑战失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's take on the 'Hidden Competency Evaluation System' inference challenge. Here are the rules:

The Board of Education has set a hidden comprehensive quality comparison rule for sorting students' multidimensional performances. Each student profile consists of quantified scores for four competency modules (e.g., morality, intellect, physique, aesthetics), denoted as (d1, d2, d3, d4), where each score is between 0 and 9, with leading zeros allowed.

The hidden evaluator contains:
1. A competency priority sequence P: a permutation of the four module positions (1, 2, 3, 4), determining which competency is evaluated first.
2. A comparison direction for each priority competency: either "ascending" or "descending".
   - Ascending: students with smaller score values come first
   - Descending: students with larger score values come first

When comparing two students, the system compares the scores at each position following the priority sequence P. At the first position where scores differ, the comparison direction of that competency determines the order. If all four scores are identical, they are considered equal (but this won't happen in the challenge).

The challenge has two phases:

## Training Phase
You can infer the hidden evaluation rule through system queries. Two types of queries are available:

1. Pairwise Comparison Query (COMPARE)
   - Submit two student profiles, each with a custom ID and four competency scores
   - The system will tell you the ordering of these two students according to the hidden evaluator
   - Format:
   <query_compare>ID1:d1d2d3d4,ID2:d1d2d3d4</query_compare>
   Example: <query_compare>A:1234,B:5678</query_compare>

2. Position Query (SORT-K)
   - Submit a test sequence (3 to 12 students), each with an ID and four scores, plus a position k
   - The system will tell you which student's ID is at position k after sorting the sequence by the hidden evaluator
   - Format:
   <query_sort>k=position;ID1:d1d2d3d4,ID2:d1d2d3d4,...</query_sort>
   Example: <query_sort>k=2;A:1234,B:5678,C:9012</query_sort>

Note:
- All four-digit score combinations in queries must be distinct
- Query budget is limited, please infer the rule efficiently
- Current query count will be provided after each feedback

## Final Phase
When you believe you have inferred the evaluation rule, the system will give you a formal assessment sequence (containing {n} students) and a target position k. You must directly provide the ID of the student at position k after sorting by the hidden evaluator, without making any further queries.

Final answer format:
<answer>ID</answer>

Example: <answer>A</answer>

If the answer is incorrect or the format is invalid, the challenge fails.
"""

    # -----------------------------------------------------
    # 新增场景化规则 4：制造业/工业
    # -----------------------------------------------------
    contextualized_rule_zh_4 = """\
我们来操作"隐藏良率质检系统"进行推理，规则如下：

自动化工厂设定了一个隐藏的零件质量评估规则，用于对各批次零件的合格优先级进行排序。每个零件批次样本由四项公差缺陷参数的量化值构成，记为 (d1, d2, d3, d4)，每项参数值在 0 到 9 之间，允许前导 0。

隐藏评估器包含：
1. 一个参数优先位序 P：即对四个公差位置 (1, 2, 3, 4) 的某一排列，决定质检时优先考察哪一项缺陷参数。
2. 每个优先参数的比较方向：可以是"升序"或"降序"。
   - 升序：缺陷参数数值小的批次排在前面（质量相对更优）
   -降序：缺陷参数数值大的批次排在前面

比较两个零件批次时，按优先位序 P 逐项比较对应位置的缺陷参数值，遇到第一个不相等的参数时，按该项的比较方向决定先后顺序。若四项参数完全相同则视为相同（但在测试中不会出现）。

测试分为两个阶段：

## 训练阶段
你可以通过系统查询来推断隐藏的质检规则。提供两种查询方式：

1. 成对比较查询（COMPARE）
   - 提交两个零件批次样本，每个样本包含一个自定义 ID 和四位公差缺陷参数
   - 系统会反馈这两个样本按隐藏评估器的先后关系
   - 格式：
   <query_compare>ID1:d1d2d3d4,ID2:d1d2d3d4</query_compare>
   例如：<query_compare>A:1234,B:5678</query_compare>

2. 排位查询（SORT-K）
   - 提交一个测试序列（3 到 12 个批次），每个包含 ID 和四位参数值，以及一个位置 k
   - 系统会反馈该序列按隐藏评估器排序后第 k 位是哪个批次的 ID
   - 格式：
   <query_sort>k=位置数;ID1:d1d2d3d4,ID2:d1d2d3d4,...</query_sort>
   例如：<query_sort>k=2;A:1234,B:5678,C:9012</query_sort>

注意：
- 所有查询中的四位参数组合必须两两不同
- 查询预算有限，请尽可能高效地推断规则
- 当前已使用查询次数：将在每次反馈后告知

## 决胜阶段
当你认为已经推断出质检规则后，系统会给出一个正式的检验序列（包含 {n} 个零件批次）和一个目标位置 k。你需要直接给出该序列按隐藏评估器排序后第 k 位批次的 ID，不能再进行任何查询。

提交最终答案的格式：
<answer>ID</answer>

例如：<answer>A</answer>

如果答案错误或格式不符，测试失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's operate the 'Hidden Yield Quality Inspection System' for this inference task. Here are the rules:

The automated factory has set a hidden parts quality assessment rule for sorting the qualification priority of various part batches. Each part batch sample consists of quantified values for four tolerance defect parameters, denoted as (d1, d2, d3, d4), where each parameter value is between 0 and 9, with leading zeros allowed.

The hidden evaluator contains:
1. A parameter priority sequence P: a permutation of the four tolerance positions (1, 2, 3, 4), determining which defect parameter is evaluated first during inspection.
2. A comparison direction for each priority parameter: either "ascending" or "descending".
   - Ascending: batches with smaller defect parameter values come first (relatively better quality)
   - Descending: batches with larger defect parameter values come first

When comparing two part batches, the system compares the defect parameter values at each position following the priority sequence P. At the first position where values differ, the comparison direction of that parameter determines the order. If all four parameters are identical, they are considered equal (but this won't happen in the test).

The test has two phases:

## Training Phase
You can infer the hidden inspection rule through system queries. Two types of queries are available:

1. Pairwise Comparison Query (COMPARE)
   - Submit two part batch samples, each with a custom ID and four tolerance defect parameters
   - The system will tell you the ordering of these two samples according to the hidden evaluator
   - Format:
   <query_compare>ID1:d1d2d3d4,ID2:d1d2d3d4</query_compare>
   Example: <query_compare>A:1234,B:5678</query_compare>

2. Position Query (SORT-K)
   - Submit a test sequence (3 to 12 batches), each with an ID and four parameter values, plus a position k
   - The system will tell you which batch's ID is at position k after sorting the sequence by the hidden evaluator
   - Format:
   <query_sort>k=position;ID1:d1d2d3d4,ID2:d1d2d3d4,...</query_sort>
   Example: <query_sort>k=2;A:1234,B:5678,C:9012</query_sort>

Note:
- All four-digit parameter combinations in queries must be distinct
- Query budget is limited, please infer the rule efficiently
- Current query count will be provided after each feedback

## Final Phase
When you believe you have inferred the inspection rule, the system will give you a formal inspection sequence (containing {n} part batches) and a target position k. You must directly provide the ID of the batch at position k after sorting by the hidden evaluator, without making any further queries.

Final answer format:
<answer>ID</answer>

Example: <answer>A</answer>

If the answer is incorrect or the format is invalid, the test fails.
"""

    # -----------------------------------------------------
    # 新增场景化规则 5：法律
    # -----------------------------------------------------
    contextualized_rule_zh_5 = """\
我们来解析"隐藏案卷排期系统"的逻辑，规则如下：

法院审判管理系统设定了一个隐藏的案件审理优先级比较规则，用于对各案件卷宗进行排期排序。每个案件卷宗由四项案情关键因子（如涉案金额、社会影响等）的量化指标构成，记为 (d1, d2, d3, d4)，每项指标值在 0 到 9 之间，允许前导 0。

隐藏评估器包含：
1. 一个因子优先位序 P：即对四个关键因子位置 (1, 2, 3, 4) 的某一排列，决定排期时优先考察哪一项案件因子。
2. 每个优先因子的比较方向：可以是"升序"或"降序"。
   - 升序：指标数值小的案件排在前面
   - 降序：指标数值大的案件排在前面

比较两个案件卷宗时，按优先位序 P 逐项比较对应位置的指标值，遇到第一个不相等的指标时，按该项的比较方向决定先后顺序。若四项指标完全相同则视为相同（但在解析中不会出现）。

解析分为两个阶段：

## 训练阶段
你可以通过系统查询来推断隐藏的排期规则。提供两种查询方式：

1. 成对比较查询（COMPARE）
   - 提交两个案件卷宗，每个包含一个自定义 ID 和四位案情关键指标
   - 系统会反馈这两个案卷按隐藏评估器的先后关系
   - 格式：
   <query_compare>ID1:d1d2d3d4,ID2:d1d2d3d4</query_compare>
   例如：<query_compare>A:1234,B:5678</query_compare>

2. 排位查询（SORT-K）
   - 提交一个测试序列（3 到 12 个案卷），每个包含 ID 和四位指标，以及一个位置 k
   - 系统会反馈该序列按隐藏评估器排序后第 k 位是哪个案卷的 ID
   - 格式：
   <query_sort>k=位置数;ID1:d1d2d3d4,ID2:d1d2d3d4,...</query_sort>
   例如：<query_sort>k=2;A:1234,B:5678,C:9012</query_sort>

注意：
- 所有查询中的四位指标组合必须两两不同
- 查询预算有限，请尽可能高效地推断规则
- 当前已使用查询次数：将在每次反馈后告知

## 决胜阶段
当你认为已经推断出排期规则后，系统会给出一个正式的庭审序列（包含 {n} 个案件卷宗）和一个目标位置 k。你需要直接给出该序列按隐藏评估器排序后第 k 位案卷的 ID，不能再进行任何查询。

提交最终答案的格式：
<answer>ID</answer>

例如：<answer>A</answer>

如果答案错误或格式不符，解析失败。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's decode the logic of the 'Hidden Case Scheduling System'. Here are the rules:

The Court Trial Management System has set a hidden case trial priority comparison rule for scheduling and sorting various case files. Each case file consists of quantified indicators for four key case factors (e.g., involved amount, social impact), denoted as (d1, d2, d3, d4), where each indicator value is between 0 and 9, with leading zeros allowed.

The hidden evaluator contains:
1. A factor priority sequence P: a permutation of the four key factor positions (1, 2, 3, 4), determining which case factor is evaluated first during scheduling.
2. A comparison direction for each priority factor: either "ascending" or "descending".
   - Ascending: cases with smaller indicator values come first
   - Descending: cases with larger indicator values come first

When comparing two case files, the system compares the indicator values at each position following the priority sequence P. At the first position where values differ, the comparison direction of that factor determines the order. If all four indicators are identical, they are considered equal (but this won't happen during decoding).

The decoding has two phases:

## Training Phase
You can infer the hidden scheduling rule through system queries. Two types of queries are available:

1. Pairwise Comparison Query (COMPARE)
   - Submit two case files, each with a custom ID and four key case indicators
   - The system will tell you the ordering of these two files according to the hidden evaluator
   - Format:
   <query_compare>ID1:d1d2d3d4,ID2:d1d2d3d4</query_compare>
   Example: <query_compare>A:1234,B:5678</query_compare>

2. Position Query (SORT-K)
   - Submit a test sequence (3 to 12 files), each with an ID and four indicators, plus a position k
   - The system will tell you which file's ID is at position k after sorting the sequence by the hidden evaluator
   - Format:
   <query_sort>k=position;ID1:d1d2d3d4,ID2:d1d2d3d4,...</query_sort>
   Example: <query_sort>k=2;A:1234,B:5678,C:9012</query_sort>

Note:
- All four-digit indicator combinations in queries must be distinct
- Query budget is limited, please infer the rule efficiently
- Current query count will be provided after each feedback

## Final Phase
When you believe you have inferred the scheduling rule, the system will give you a formal trial sequence (containing {n} case files) and a target position k. You must directly provide the ID of the file at position k after sorting by the hidden evaluator, without making any further queries.

Final answer format:
<answer>ID</answer>

Example: <answer>A</answer>

If the answer is incorrect or the format is invalid, the decoding fails.
"""

    tags = ["answer", "query_compare", "query_sort"]
    
    # 新增类属性
    reasoning_type = "归纳推理"
    data_structure = "序列"

    # 难度配置说明：
    # 1 (简单)        - 序列长度 6, 查询预算 15, 比较器: P=[1,2,3,4], dir=[升,升,升,升]
    # 2 (中等偏下)    - 序列长度 7, 查询预算 12, 比较器: P=[2,1,3,4], dir=[升,降,升,升]
    # 3 (中等偏上)    - 序列长度 8, 查询预算 10, 比较器: P=[3,1,2,4], dir=[降,升,降,升]
    # 4 (较难)        - 序列长度 10, 查询预算 8, 比较器: P=[4,2,1,3], dir=[升,降,升,降]
    # 5 (难)          - 序列长度 12, 查询预算 6, 比较器: P=[2,4,3,1], dir=[降,降,升,升]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 6,
                "query_budget": 15,
                "priority": [1, 2, 3, 4],  # 位置优先级
                "directions": ["asc", "asc", "asc", "asc"],  # 每个优先位的方向
                "final_sequence": "A:1234,B:2345,C:3456,D:4567,E:5678,F:6789",
                "final_k": 3,
            },
            2: {
                "n": 7,
                "query_budget": 12,
                "priority": [2, 1, 3, 4],
                "directions": ["asc", "desc", "asc", "asc"],
                "final_sequence": "A:1234,B:1345,C:2234,D:2345,E:3234,F:3345,G:4234",
                "final_k": 4,
            },
            3: {
                "n": 8,
                "query_budget": 10,
                "priority": [3, 1, 2, 4],
                "directions": ["desc", "asc", "desc", "asc"],
                "final_sequence": "A:1194,B:1294,C:1394,D:2194,E:2294,F:2394,G:3194,H:3294",
                "final_k": 5,
            },
            4: {
                "n": 10,
                "query_budget": 8,
                "priority": [4, 2, 1, 3],
                "directions": ["asc", "desc", "asc", "desc"],
                "final_sequence": "A:1231,B:1241,C:1251,D:2231,E:2241,F:2251,G:3231,H:3241,I:3251,J:4231",
                "final_k": 6,
            },
            5: {
                "n": 12,
                "query_budget": 6,
                "priority": [2, 4, 3, 1],
                "directions": ["desc", "desc", "asc", "asc"],
                "final_sequence": "A:1911,B:1921,C:1931,D:2911,E:2921,F:2931,G:3911,H:3921,I:3931,J:4911,K:4921,L:4931",
                "final_k": 7,
            },
        },
        "en": {
            1: {
                "n": 6,
                "query_budget": 15,
                "priority": [1, 2, 3, 4],
                "directions": ["asc", "asc", "asc", "asc"],
                "final_sequence": "A:1234,B:2345,C:3456,D:4567,E:5678,F:6789",
                "final_k": 3,
            },
            2: {
                "n": 7,
                "query_budget": 12,
                "priority": [2, 1, 3, 4],
                "directions": ["asc", "desc", "asc", "asc"],
                "final_sequence": "A:1234,B:1345,C:2234,D:2345,E:3234,F:3345,G:4234",
                "final_k": 4,
            },
            3: {
                "n": 8,
                "query_budget": 10,
                "priority": [3, 1, 2, 4],
                "directions": ["desc", "asc", "desc", "asc"],
                "final_sequence": "A:1194,B:1294,C:1394,D:2194,E:2294,F:2394,G:3194,H:3294",
                "final_k": 5,
            },
            4: {
                "n": 10,
                "query_budget": 8,
                "priority": [4, 2, 1, 3],
                "directions": ["asc", "desc", "asc", "desc"],
                "final_sequence": "A:1231,B:1241,C:1251,D:2231,E:2241,F:2251,G:3231,H:3241,I:3251,J:4231",
                "final_k": 6,
            },
            5: {
                "n": 12,
                "query_budget": 6,
                "priority": [2, 4, 3, 1],
                "directions": ["desc", "desc", "asc", "asc"],
                "final_sequence": "A:1911,B:1921,C:1931,D:2911,E:2921,F:2931,G:3911,H:3921,I:3931,J:4911,K:4921,L:4931",
                "final_k": 7,
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0
        self.is_final_phase = False
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏配置"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        
        # 隐藏比较器的配置
        self.priority = cfg["priority"]  # 如 [2, 1, 3, 4] 表示先比较第2位，再第1位...
        self.directions = cfg["directions"]  # 如 ["asc", "desc", "asc", "asc"]
        self.query_budget = cfg["query_budget"]
        
        # 决胜阶段的序列和目标
        self.final_sequence_str = cfg["final_sequence"]
        self.final_k = cfg["final_k"]
        
        # 解析决胜序列
        self.final_elements = self._parse_sequence(self.final_sequence_str)
        
        # 计算正确答案
        self.correct_answer = self._compute_kth_element(self.final_elements, self.final_k)

    def _parse_sequence(self, seq_str):
        """解析序列字符串，返回 [(ID, digits), ...] 列表"""
        elements = []
        for item in seq_str.split(","):
            item = item.strip()
            if ":" not in item:
                continue
            id_part, digits_part = item.split(":", 1)
            elements.append((id_part.strip(), digits_part.strip()))
        return elements

    def _compare(self, digits1, digits2):
        """
        使用隐藏比较器比较两个四位数字
        返回: -1 (digits1 < digits2), 0 (相等), 1 (digits1 > digits2)
        """
        if len(digits1) != 4 or len(digits2) != 4:
            raise ValueError("Digits must be exactly 4 characters")
        
        # 按优先位序比较
        for pos_idx in self.priority:
            # pos_idx 是 1-based，转换为 0-based
            idx = pos_idx - 1
            d1 = int(digits1[idx])
            d2 = int(digits2[idx])
            
            if d1 != d2:
                # 找到第一个不同的位，根据该位的方向决定
                direction = self.directions[self.priority.index(pos_idx)]
                if direction == "asc":
                    return -1 if d1 < d2 else 1
                else:  # desc
                    return -1 if d1 > d2 else 1
        
        return 0  # 完全相同

    def _compute_kth_element(self, elements, k):
        """计算排序后第 k 位的元素 ID"""
        # [BUG FIX] 原问题：Python 3 的 sorted/sort 移除了 'cmp' 参数，会导致 TypeError。
        # 同时，原代码 lambda a, b: self._compare(a, b) 试图比较整个元素(ID, digits)，
        # 但 _compare 只接受 digits 字符串。
        # 修改：使用 functools.cmp_to_key，并正确提取元素的 digits部分 (item[1]) 传递给 _compare。
        sorted_elements = sorted(
            elements,
            key=cmp_to_key(lambda item1, item2: self._compare(item1[1], item2[1]))
        )
        
        if k < 1 or k > len(sorted_elements):
            raise ValueError(f"k={k} out of range")
        return sorted_elements[k - 1][0]

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        if not self.is_final_phase:
            # 模型在未收到决胜序列的情况下提交答案
            # 这种情况下模型不知道 final_sequence 和 final_k，不可能答对
            # 返回 False
            return False

        model_answer = parsed_info["answer"].strip()
        return model_answer == self.correct_answer

    def _final_phase_message(self, lang):
        """生成决胜阶段提示信息"""
        if lang == "zh":
            response = f"查询预算已用完（{self.query_count}/{self.query_budget}）。\n\n"
            response += "现在进入决胜阶段！\n"
            response += f"正式序列：{self.final_sequence_str}\n"
            response += f"目标位置 k = {self.final_k}\n\n"
            response += "请直接给出该序列按隐藏比较器排序后第 k 位元素的 ID。"
        else:
            response = f"Query budget exhausted ({self.query_count}/{self.query_budget}).\n\n"
            response += "Now entering final phase!\n"
            response += f"Formal sequence: {self.final_sequence_str}\n"
            response += f"Target position k = {self.final_k}\n\n"
            response += "Please directly provide the ID of the element at position k after sorting by the hidden comparator."
        return response

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑（原 produce_response 的内容）"""
        lang = self.config.language

        # 检查是否已进入决胜阶段
        if self.is_final_phase:
            if lang == "zh":
                return "错误：已进入决胜阶段，不能再进行查询。请提交最终答案。"
            else:
                return "Error: Final phase has begun. No more queries allowed. Please submit your final answer."

        # 检查查询预算（在处理查询之前就已耗尽的情况）
        if self.query_count >= self.query_budget:
            self.is_final_phase = True
            return self._final_phase_message(lang)

        # 处理 query_compare
        if "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"].strip()
                parts = raw.split(",")
                if len(parts) != 2:
                    raise ValueError("Expected exactly 2 elements")

                elem1 = parts[0].strip().split(":")
                elem2 = parts[1].strip().split(":")

                if len(elem1) != 2 or len(elem2) != 2:
                    raise ValueError("Invalid element format")

                id1, digits1 = elem1[0].strip(), elem1[1].strip()
                id2, digits2 = elem2[0].strip(), elem2[1].strip()

                if len(digits1) != 4 or len(digits2) != 4:
                    raise ValueError("Digits must be exactly 4 characters")

                if not digits1.isdigit() or not digits2.isdigit():
                    raise ValueError("Digits must be numeric")

                if digits1 == digits2:
                    if lang == "zh":
                        return "错误：两个元素的四位数字完全相同，该比较不被接受。"
                    else:
                        return "Error: The two elements have identical digits. This comparison is not accepted."

                cmp_result = self._compare(digits1, digits2)
                self.query_count += 1

                if lang == "zh":
                    result_str = f"{id1}<{id2}" if cmp_result < 0 else f"{id1}>{id2}"
                    response = f"{result_str}\n（已使用查询次数：{self.query_count}/{self.query_budget}）"
                else:
                    result_str = f"{id1}<{id2}" if cmp_result < 0 else f"{id1}>{id2}"
                    response = f"{result_str}\n(Query count: {self.query_count}/{self.query_budget})"

                # 如果这次查询后预算耗尽，附带决胜阶段信息
                if self.query_count >= self.query_budget:
                    self.is_final_phase = True
                    response += "\n\n" + self._final_phase_message(lang)

                return response

            except Exception as e:
                if lang == "zh":
                    return f"错误：query_compare 格式无效。应为 ID1:dddd,ID2:dddd 格式。详情：{str(e)}"
                else:
                    return f"Error: Invalid query_compare format. Expected ID1:dddd,ID2:dddd. Details: {str(e)}"

        # 处理 query_sort
        elif "query_sort" in parsed_info:
            try:
                raw = parsed_info["query_sort"].strip()
                if ";" not in raw:
                    raise ValueError("Expected ';' separator")

                k_part, seq_part = raw.split(";", 1)

                if not k_part.strip().startswith("k="):
                    raise ValueError("Expected k= prefix")
                k = int(k_part.strip()[2:])

                elements = self._parse_sequence(seq_part)

                if len(elements) < 3 or len(elements) > 12:
                    raise ValueError("Sequence length must be between 3 and 12")

                if k < 1 or k > len(elements):
                    raise ValueError(f"k={k} out of range for sequence of length {len(elements)}")

                digits_set = set()
                for _, digits in elements:
                    if len(digits) != 4 or not digits.isdigit():
                        raise ValueError("Invalid digits format")
                    if digits in digits_set:
                        if lang == "zh":
                            return "错误：序列中存在重复的四位数字组合。"
                        else:
                            return "Error: Duplicate digit combinations in sequence."
                    digits_set.add(digits)

                kth_id = self._compute_kth_element(elements, k)
                self.query_count += 1

                if lang == "zh":
                    response = f"第 {k} 位是：{kth_id}\n（已使用查询次数：{self.query_count}/{self.query_budget}）"
                else:
                    response = f"Position {k} is: {kth_id}\n(Query count: {self.query_count}/{self.query_budget})"

                # 如果这次查询后预算耗尽，附带决胜阶段信息
                if self.query_count >= self.query_budget:
                    self.is_final_phase = True
                    response += "\n\n" + self._final_phase_message(lang)

                return response

            except Exception as e:
                if lang == "zh":
                    return f"错误：query_sort 格式无效。应为 k=数字;ID1:dddd,ID2:dddd,... 格式。详情：{str(e)}"
                else:
                    return f"Error: Invalid query_sort format. Expected k=number;ID1:dddd,ID2:dddd,... Details: {str(e)}"

        else:
            if lang == "zh":
                return "错误：未找到有效的查询标签。"
            else:
                return "Error: No valid query tag found."

    def _cf_make_wrong(self, correct):
        """生成错误答案"""
        # 1. 若 correct 是纯整数字符串
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 2. 关键词替换
        original_correct = correct
        
        if self.config.language == "zh":
            if "是" in correct:
                correct = correct.replace("是", "否")
            elif "否" in correct:
                correct = correct.replace("否", "是")
        else:
            # 英文：Yes ↔ No (忽略大小写，保持原始风格)
            def swap_yes_no(match):
                word = match.group(0)
                lower = word.lower()
                if lower == "yes":
                    return "No" if word[0].isupper() else "no"
                if lower == "no":
                    return "Yes" if word[0].isupper() else "yes"
                return word
            
            correct = re.sub(r'\b(Yes|No)\b', swap_yes_no, correct, flags=re.IGNORECASE)

        # 如果发生了替换，直接返回
        if correct != original_correct:
            return correct

        # 3. 都不匹配：在字符串末尾追加 "_WRONG"
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> List[Dict]:
        """
        枚举一组代表性的合法查询并返回对应的正确答案。
        查询数量限制在 query_budget 以内。
        """
        queries = []

        if self.is_final_phase or self.query_count >= self.query_budget:
            return queries

        lang = self.config.language
        # 基础探针：用于测试每一位的权重和方向
        probes = ["1111", "2111", "1211", "1121", "1112"]

        simulated_count = 0  # 从 0 开始，表示新游戏的模拟计数

        # 1. 生成成对比较查询 (COMPARE) —— 只生成关键的探针对
        # 用 1111 作为基准，与其他 4 个探针分别比较
        compare_pairs = []
        for i in range(1, len(probes)):
            compare_pairs.append((probes[0], probes[i]))
        # 再加上相邻探针的比较
        for i in range(1, len(probes) - 1):
            compare_pairs.append((probes[i], probes[i+1]))

        for d1, d2 in compare_pairs:
            if simulated_count >= self.query_budget:
                break
            
            id1, id2 = "A", "B"
            query_content = f"{id1}:{d1},{id2}:{d2}"
            query_str = f"<query_compare>{query_content}</query_compare>"
            
            cmp_result = self._compare(d1, d2)
            simulated_count += 1
            
            if lang == "zh":
                result_str = f"{id1}<{id2}" if cmp_result < 0 else f"{id1}>{id2}"
                ans = f"{result_str}\n（已使用查询次数：{simulated_count}/{self.query_budget}）"
            else:
                result_str = f"{id1}<{id2}" if cmp_result < 0 else f"{id1}>{id2}"
                ans = f"{result_str}\n(Query count: {simulated_count}/{self.query_budget})"
                
            if simulated_count >= self.query_budget:
                temp_query_count = self.query_count
                self.query_count = simulated_count
                ans += "\n\n" + self._final_phase_message(lang)
                self.query_count = temp_query_count

            queries.append({
                "query": query_str,
                "answer": ans
            })

        # 2. 生成排位查询 (SORT-K)
        # 如果模拟还没有达到 budget，再生成 SORT-K 查询
        if simulated_count < self.query_budget:
            subset = probes[:3]  # 1111, 2111, 1211
            subset_ids = ["A", "B", "C"]
            seq_parts = [f"{subset_ids[i]}:{subset[i]}" for i in range(3)]
            seq_str = ",".join(seq_parts)
            elements = list(zip(subset_ids, subset))

            for k in range(1, 4):
                if simulated_count >= self.query_budget:
                    break
                query_content = f"k={k};{seq_str}"
                query_str = f"<query_sort>{query_content}</query_sort>"
                
                kth_id = self._compute_kth_element(elements, k)
                simulated_count += 1
                
                if lang == "zh":
                    ans = f"第 {k} 位是：{kth_id}\n（已使用查询次数：{simulated_count}/{self.query_budget}）"
                else:
                    ans = f"Position {k} is: {kth_id}\n(Query count: {simulated_count}/{self.query_budget})"
                    
                if simulated_count >= self.query_budget:
                    temp_query_count = self.query_count
                    self.query_count = simulated_count
                    ans += "\n\n" + self._final_phase_message(lang)
                    self.query_count = temp_query_count

                queries.append({
                    "query": query_str,
                    "answer": ans
                })

        return queries