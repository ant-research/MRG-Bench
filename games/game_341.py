# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 集合：存在一个由N个物体组成的集合，注意他们不存在位置、前后和大小关系。
# 知识点:   条件计数：满足某给定条件的元素共有多少个
# ============================================================

from .base import Game
import random


class ExactlyOneAttributeGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "集合"

    game_rule_zh = """\
我们来玩一个"属性推理"游戏，规则如下：

游戏设定了一个包含 {n} 个元素的集合。每个元素都可能具有三种属性中的任意组合：属性 A、属性 B、属性 C。每个元素可能具有这些属性中的零个、一个、两个或全部三个。这个属性分配在游戏中是固定的，不会改变。

你可以反复向我提出计数查询，每次查询指定一个或多个属性的组合，我会告诉你"同时具有所有这些属性"的元素数量。

允许的查询类型包括：
- 查询单个属性：询问具有属性 A 的元素数量（记作 |A|）
- 查询单个属性：询问具有属性 B 的元素数量（记作 |B|）
- 查询单个属性：询问具有属性 C 的元素数量（记作 |C|）
- 查询两个属性：询问同时具有属性 A 和 B 的元素数量（记作 |A∧B|）
- 查询两个属性：询问同时具有属性 A 和 C 的元素数量（记作 |A∧C|）
- 查询两个属性：询问同时具有属性 B 和 C 的元素数量（记作 |B∧C|）
- 查询三个属性：询问同时具有属性 A、B 和 C 的元素数量（记作 |A∧B∧C|）

注意：查询返回的是"至少具有所查询的全部属性"的元素数量，不限制元素是否还具有其他属性。

你的目标是：推断出"恰好具有一种属性"的元素总数。也就是说，只具有 A、只具有 B 或只具有 C 中恰好一种的元素总数。

请通过尽可能少的查询次数来推断出答案。

## 查询和提交答案的格式（必须严格遵守）

每次查询请使用以下 XML 格式（只能查询一次）：

- 查询单个属性 A：
<query>A</query>

- 查询单个属性 B：
<query>B</query>

- 查询单个属性 C：
<query>C</query>

- 查询两个属性 A 和 B：
<query>A,B</query>

- 查询两个属性 A 和 C：
<query>A,C</query>

- 查询两个属性 B 和 C：
<query>B,C</query>

- 查询三个属性 A、B 和 C：
<query>A,B,C</query>

提交最终答案时，请给出"恰好具有一种属性"的元素总数（一个非负整数），格式如下：

<answer>5</answer>
"""

    game_rule_en = """\
Let's play an "Attribute Reasoning" game. Here are the rules:

The game involves a set of {n} elements. Each element may have any combination of three attributes: attribute A, attribute B, and attribute C. Each element can have zero, one, two, or all three of these attributes. The attribute assignment is fixed throughout the game and will not change.

You can repeatedly ask me counting queries. Each query specifies one or more attributes, and I will tell you the count of elements that "have all the specified attributes simultaneously".

Allowed query types include:
- Query single attribute: ask for the count of elements with attribute A (denoted as |A|)
- Query single attribute: ask for the count of elements with attribute B (denoted as |B|)
- Query single attribute: ask for the count of elements with attribute C (denoted as |C|)
- Query two attributes: ask for the count of elements with both A and B (denoted as |A∧B|)
- Query two attributes: ask for the count of elements with both A and C (denoted as |A∧C|)
- Query two attributes: ask for the count of elements with both B and C (denoted as |B∧C|)
- Query three attributes: ask for the count of elements with A, B, and C all together (denoted as |A∧B∧C|)

Note: The query returns the count of elements that have "at least all the queried attributes", without restricting whether they have other attributes.

Your goal is: to infer the total number of elements that have "exactly one attribute". That is, the total count of elements that have exactly one of: only A, only B, or only C.

Please infer the answer using as few queries as possible.

## Query and Answer Format (must be strictly followed)

Each query should use the following XML format (only one query per turn):

- Query single attribute A:
<query>A</query>

- Query single attribute B:
<query>B</query>

- Query single attribute C:
<query>C</query>

- Query two attributes A and B:
<query>A,B</query>

- Query two attributes A and C:
<query>A,C</query>

- Query two attributes B and C:
<query>B,C</query>

- Query three attributes A, B, and C:
<query>A,B,C</query>

When submitting the final answer, provide the total number of elements with "exactly one attribute" (a non-negative integer), in this format:

<answer>5</answer>
"""

    # ================= 场景 1：交通 =================
    contextualized_rule_zh_1 = """\
欢迎进入“智慧交通违规稽查”系统，规则如下：

系统内包含 {n} 辆登记在册的车辆。每辆车都可能存在以下三种违规情况中的任意组合：违章记录（属性 A）、逾期未年检（属性 B）、未交强险（属性 C）。每辆车可能没有任何违规，也可能存在一项、两项或全部三项违规。违规状态在稽查期间是固定的，不会改变。

你可以反复向我提出计数查询，每次查询指定一种或多种违规情况的组合，我会告诉你“同时存在所有这些指定违规”的车辆数量。

允许的查询类型包括：
- 查询单项违规：询问存在违章记录的车辆数量（记作 |A|）
- 查询单项违规：询问存在逾期未年检的车辆数量（记作 |B|）
- 查询单项违规：询问存在未交强险的车辆数量（记作 |C|）
- 查询两项违规：询问同时存在违章记录和逾期未年检的车辆数量（记作 |A∧B|）
- 查询两项违规：询问同时存在违章记录和未交强险的车辆数量（记作 |A∧C|）
- 查询两项违规：询问同时存在逾期未年检和未交强险的车辆数量（记作 |B∧C|）
- 查询三项违规：询问同时存在违章、未年检和未交强险的车辆数量（记作 |A∧B∧C|）

注意：查询返回的是“至少存在所查询的全部违规”的车辆数量，不限制车辆是否还存在其他违规。

你的目标是：推断出“恰好存在一项违规情况”的车辆总数。也就是说，只存在违章、只存在未年检或只存在未交强险中恰好一种情况的车辆总数，以便进行针对性的轻微违法警告。

请通过尽可能少的查询次数来推断出答案。

## 查询和提交答案的格式（必须严格遵守）

每次查询请使用以下 XML 格式（只能查询一次），使用 A、B、C 代表对应违规项：

- 查询单项违规 A (违章记录)：
<query>A</query>

- 查询单项违规 B (逾期未年检)：
<query>B</query>

- 查询单项违规 C (未交强险)：
<query>C</query>

- 查询两项违规 A 和 B：
<query>A,B</query>

- 查询两项违规 A 和 C：
<query>A,C</query>

- 查询两项违规 B 和 C：
<query>B,C</query>

- 查询三项违规 A、B 和 C：
<query>A,B,C</query>

提交最终答案时，请给出“恰好存在一项违规情况”的车辆总数（一个非负整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Traffic Violation Audit" simulation system. Here are the rules:

The system involves a set of {n} registered vehicles. Each vehicle may have any combination of three violations: Traffic Violations (Attribute A), Overdue Inspection (Attribute B), and Unpaid Insurance (Attribute C). Each vehicle can have zero, one, two, or all three of these violations. The violation status is fixed throughout the audit and will not change.

You can repeatedly ask me counting queries. Each query specifies one or more violations, and I will tell you the count of vehicles that "have all the specified violations simultaneously".

Allowed query types include:
- Query single violation: ask for the count of vehicles with Traffic Violations (denoted as |A|)
- Query single violation: ask for the count of vehicles with Overdue Inspection (denoted as |B|)
- Query single violation: ask for the count of vehicles with Unpaid Insurance (denoted as |C|)
- Query two violations: ask for the count of vehicles with both A and B (denoted as |A∧B|)
- Query two violations: ask for the count of vehicles with both A and C (denoted as |A∧C|)
- Query two violations: ask for the count of vehicles with both B and C (denoted as |B∧C|)
- Query three violations: ask for the count of vehicles with A, B, and C all together (denoted as |A∧B∧C|)

Note: The query returns the count of vehicles that have "at least all the queried violations", without restricting whether they have other violations.

Your goal is: to infer the total number of vehicles that have "exactly one violation". That is, the total count of vehicles that have exactly one of: only A, only B, or only C. This helps us issue targeted warnings for minor infractions.

Please infer the answer using as few queries as possible.

## Query and Answer Format (must be strictly followed)

Each query should use the following XML format (only one query per turn), using A, B, C for respective violations:

- Query single violation A (Traffic Violations):
<query>A</query>

- Query single violation B (Overdue Inspection):
<query>B</query>

- Query single violation C (Unpaid Insurance):
<query>C</query>

- Query two violations A and B:
<query>A,B</query>

- Query two violations A and C:
<query>A,C</query>

- Query two violations B and C:
<query>B,C</query>

- Query three violations A, B, and C:
<query>A,B,C</query>

When submitting the final answer, provide the total number of vehicles with "exactly one violation" (a non-negative integer), in this format:

<answer>5</answer>
"""

    # ================= 场景 2：医疗 =================
    contextualized_rule_zh_2 = """\
欢迎进入“临床试验患者筛查”系统，规则如下：

系统提取了包含 {n} 名临床试验患者的集合。每名患者都可能具有以下三种并发症或风险的任意组合：高血压并发症（属性 A）、糖尿病并发症（属性 B）、心血管疾病风险（属性 C）。每名患者可能具有零个、一个、两个或全部三个健康风险因素。这些健康状态在筛查评估期间是固定的，不会改变。

你可以反复向我提出计数查询，每次查询指定一种或多种风险因素的组合，我会告诉你“同时存在所有这些指定风险”的患者数量。

允许的查询类型包括：
- 查询单项风险：询问具有高血压并发症的患者数量（记作 |A|）
- 查询单项风险：询问具有糖尿病并发症的患者数量（记作 |B|）
- 查询单项风险：询问具有心血管疾病风险的患者数量（记作 |C|）
- 查询两项风险：询问同时具有高血压并发症和糖尿病并发症的患者数量（记作 |A∧B|）
- 查询两项风险：询问同时具有高血压并发症和心血管风险的患者数量（记作 |A∧C|）
- 查询两项风险：询问同时具有糖尿病并发症和心血管风险的患者数量（记作 |B∧C|）
- 查询三项风险：询问同时具有上述三种并发症及风险的患者数量（记作 |A∧B∧C|）

注意：查询返回的是“至少存在所查询的全部风险”的患者数量，不限制患者是否还存在其他并发症或风险。

你的目标是：推断出“恰好仅有一种并发症/风险”的患者总数。用于开展单一病种的精准靶向治疗试验。

请通过尽可能少的查询次数来推断出答案。

## 查询和提交答案的格式（必须严格遵守）

每次查询请使用以下 XML 格式（只能查询一次），使用 A、B、C 代表对应风险项：

- 查询单项风险 A (高血压并发症)：
<query>A</query>

- 查询单项风险 B (糖尿病并发症)：
<query>B</query>

- 查询单项风险 C (心血管疾病风险)：
<query>C</query>

- 查询两项风险 A 和 B：
<query>A,B</query>

- 查询两项风险 A 和 C：
<query>A,C</query>

- 查询两项风险 B 和 C：
<query>B,C</query>

- 查询三项风险 A、B 和 C：
<query>A,B,C</query>

提交最终答案时，请给出“恰好仅有一种并发症/风险”的患者总数（一个非负整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Clinical Trial Patient Screening" system. Here are the rules:

The system involves a set of {n} patients. Each patient may have any combination of three health conditions/risks: Hypertension Complications (Attribute A), Diabetes Complications (Attribute B), and Cardiovascular Risk (Attribute C). Each patient can have zero, one, two, or all three of these risk factors. These health states are fixed throughout the screening evaluation and will not change.

You can repeatedly ask me counting queries. Each query specifies one or more risk factors, and I will tell you the count of patients that "have all the specified conditions simultaneously".

Allowed query types include:
- Query single risk: ask for the count of patients with Hypertension Complications (denoted as |A|)
- Query single risk: ask for the count of patients with Diabetes Complications (denoted as |B|)
- Query single risk: ask for the count of patients with Cardiovascular Risk (denoted as |C|)
- Query two risks: ask for the count of patients with both A and B (denoted as |A∧B|)
- Query two risks: ask for the count of patients with both A and C (denoted as |A∧C|)
- Query two risks: ask for the count of patients with both B and C (denoted as |B∧C|)
- Query three risks: ask for the count of patients with A, B, and C all together (denoted as |A∧B∧C|)

Note: The query returns the count of patients that have "at least all the queried conditions", without restricting whether they have other risks.

Your goal is: to infer the total number of patients who have "exactly one complication/risk". This metric is crucial for initiating precise targeted therapy trials for single-disease conditions.

Please infer the answer using as few queries as possible.

## Query and Answer Format (must be strictly followed)

Each query should use the following XML format (only one query per turn), using A, B, C for respective risks:

- Query single risk A (Hypertension Complications):
<query>A</query>

- Query single risk B (Diabetes Complications):
<query>B</query>

- Query single risk C (Cardiovascular Risk):
<query>C</query>

- Query two risks A and B:
<query>A,B</query>

- Query two risks A and C:
<query>A,C</query>

- Query two risks B and C:
<query>B,C</query>

- Query three risks A, B, and C:
<query>A,B,C</query>

When submitting the final answer, provide the total number of patients with "exactly one complication/risk" (a non-negative integer), in this format:

<answer>5</answer>
"""

    # ================= 场景 3：教育 =================
    contextualized_rule_zh_3 = """\
欢迎进入“学生综合素质评价”系统，规则如下：

系统记录了包含 {n} 名参与评价的学生集合。每名学生都可能拥有以下三种特长或荣誉的任意组合：获得学术竞赛奖项（属性 A）、参与省级志愿服务（属性 B）、拥有艺术体育特长（属性 C）。每名学生可能拥有零个、一个、两个或全部三个荣誉。这些评价数据在当前统计周期内是固定的，不会改变。

你可以反复向我提出计数查询，每次查询指定一种或多种荣誉的组合，我会告诉你“同时满足所有这些指定条件”的学生数量。

允许的查询类型包括：
- 查询单项荣誉：询问获得学术竞赛奖项的学生数量（记作 |A|）
- 查询单项荣誉：询问参与省级志愿服务的学生数量（记作 |B|）
- 查询单项荣誉：询问拥有艺术体育特长的学生数量（记作 |C|）
- 查询两项荣誉：询问同时获得学术竞赛奖项和参与省级志愿服务的学生数量（记作 |A∧B|）
- 查询两项荣誉：询问同时获得学术竞赛奖项和拥有艺术体育特长的学生数量（记作 |A∧C|）
- 查询两项荣誉：询问同时参与省级志愿服务和拥有艺术体育特长的学生数量（记作 |B∧C|）
- 查询三项荣誉：询问同时满足上述三项特长及荣誉的学生数量（记作 |A∧B∧C|）

注意：查询返回的是“至少拥有所查询的全部荣誉”的学生数量，不限制学生是否还拥有其他荣誉。

你的目标是：推断出“恰好满足一项特长/荣誉”的学生总数。这部分数据将用于发放“专项发展鼓励金”。

请通过尽可能少的查询次数来推断出答案。

## 查询和提交答案的格式（必须严格遵守）

每次查询请使用以下 XML 格式（只能查询一次），使用 A、B、C 代表对应荣誉项：

- 查询单项荣誉 A (学术竞赛奖项)：
<query>A</query>

- 查询单项荣誉 B (省级志愿服务)：
<query>B</query>

- 查询单项荣誉 C (艺术体育特长)：
<query>C</query>

- 查询两项荣誉 A 和 B：
<query>A,B</query>

- 查询两项荣誉 A 和 C：
<query>A,C</query>

- 查询两项荣誉 B 和 C：
<query>B,C</query>

- 查询三项荣誉 A、B 和 C：
<query>A,B,C</query>

提交最终答案时，请给出“恰好满足一项特长/荣誉”的学生总数（一个非负整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Student Comprehensive Quality Evaluation" system. Here are the rules:

The system records a set of {n} students participating in the evaluation. Each student may possess any combination of three achievements/specialties: Academic Competition Awards (Attribute A), Provincial Volunteer Service (Attribute B), and Art/Sports Specialty (Attribute C). Each student can have zero, one, two, or all three of these achievements. The evaluation data is fixed during the current statistical period and will not change.

You can repeatedly ask me counting queries. Each query specifies one or more achievements, and I will tell you the count of students that "meet all the specified conditions simultaneously".

Allowed query types include:
- Query single achievement: ask for the count of students with Academic Competition Awards (denoted as |A|)
- Query single achievement: ask for the count of students with Provincial Volunteer Service (denoted as |B|)
- Query single achievement: ask for the count of students with Art/Sports Specialty (denoted as |C|)
- Query two achievements: ask for the count of students with both A and B (denoted as |A∧B|)
- Query two achievements: ask for the count of students with both A and C (denoted as |A∧C|)
- Query two achievements: ask for the count of students with both B and C (denoted as |B∧C|)
- Query three achievements: ask for the count of students with A, B, and C all together (denoted as |A∧B∧C|)

Note: The query returns the count of students that have "at least all the queried achievements", without restricting whether they possess other honors.

Your goal is: to infer the total number of students who possess "exactly one specialty/achievement". This demographic data will be used to issue the "Specialized Development Grant".

Please infer the answer using as few queries as possible.

## Query and Answer Format (must be strictly followed)

Each query should use the following XML format (only one query per turn), using A, B, C for respective achievements:

- Query single achievement A (Academic Competition Awards):
<query>A</query>

- Query single achievement B (Provincial Volunteer Service):
<query>B</query>

- Query single achievement C (Art/Sports Specialty):
<query>C</query>

- Query two achievements A and B:
<query>A,B</query>

- Query two achievements A and C:
<query>A,C</query>

- Query two achievements B and C:
<query>B,C</query>

- Query three achievements A, B, and C:
<query>A,B,C</query>

When submitting the final answer, provide the total number of students with "exactly one specialty/achievement" (a non-negative integer), in this format:

<answer>5</answer>
"""

    # ================= 场景 4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
欢迎进入“工业部件缺陷质检”系统，规则如下：

系统抽样了一个包含 {n} 个下线工业部件的集合。每个部件都可能存在以下三种制造缺陷的任意组合：表面划痕缺陷（属性 A）、尺寸超差（属性 B）、材料硬度不达标（属性 C）。每个部件可能存在零个、一个、两个或全部三个缺陷。这些缺陷状态在抽检确认后是固定的，不会改变。

你可以反复向我提出计数查询，每次查询指定一种或多种缺陷的组合，我会告诉你“同时存在所有这些指定缺陷”的部件数量。

允许的查询类型包括：
- 查询单项缺陷：询问存在表面划痕缺陷的部件数量（记作 |A|）
- 查询单项缺陷：询问存在尺寸超差的部件数量（记作 |B|）
- 查询单项缺陷：询问存在材料硬度不达标的部件数量（记作 |C|）
- 查询两项缺陷：询问同时存在表面划痕和尺寸超差的部件数量（记作 |A∧B|）
- 查询两项缺陷：询问同时存在表面划痕和材料硬度不达标的部件数量（记作 |A∧C|）
- 查询两项缺陷：询问同时存在尺寸超差和材料硬度不达标的部件数量（记作 |B∧C|）
- 查询三项缺陷：询问同时存在上述三种缺陷的部件数量（记作 |A∧B∧C|）

注意：查询返回的是“至少存在所查询的全部缺陷”的部件数量，不限制部件是否还存在其他缺陷。

你的目标是：推断出“恰好只有一种缺陷”的部件总数。这有助于评估有多少部件可以通过相对低成本的单一返工工序进行修复。

请通过尽可能少的查询次数来推断出答案。

## 查询和提交答案的格式（必须严格遵守）

每次查询请使用以下 XML 格式（只能查询一次），使用 A、B、C 代表对应缺陷项：

- 查询单项缺陷 A (表面划痕缺陷)：
<query>A</query>

- 查询单项缺陷 B (尺寸超差)：
<query>B</query>

- 查询单项缺陷 C (材料硬度不达标)：
<query>C</query>

- 查询两项缺陷 A 和 B：
<query>A,B</query>

- 查询两项缺陷 A 和 C：
<query>A,C</query>

- 查询两项缺陷 B 和 C：
<query>B,C</query>

- 查询三项缺陷 A、B 和 C：
<query>A,B,C</query>

提交最终答案时，请给出“恰好只有一种缺陷”的部件总数（一个非负整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the "Industrial Part Defect Inspection" system. Here are the rules:

The system involves a sample set of {n} industrial parts. Each part may have any combination of three manufacturing defects: Surface Scratch Defect (Attribute A), Dimensional Deviation (Attribute B), and Substandard Material Hardness (Attribute C). Each part can have zero, one, two, or all three of these defects. These defect statuses are fixed once sampled and will not change.

You can repeatedly ask me counting queries. Each query specifies one or more defects, and I will tell you the count of parts that "have all the specified defects simultaneously".

Allowed query types include:
- Query single defect: ask for the count of parts with Surface Scratch Defect (denoted as |A|)
- Query single defect: ask for the count of parts with Dimensional Deviation (denoted as |B|)
- Query single defect: ask for the count of parts with Substandard Material Hardness (denoted as |C|)
- Query two defects: ask for the count of parts with both A and B (denoted as |A∧B|)
- Query two defects: ask for the count of parts with both A and C (denoted as |A∧C|)
- Query two defects: ask for the count of parts with both B and C (denoted as |B∧C|)
- Query three defects: ask for the count of parts with A, B, and C all together (denoted as |A∧B∧C|)

Note: The query returns the count of parts that have "at least all the queried defects", without restricting whether they have other defects.

Your goal is: to infer the total number of parts that have "exactly one defect". This helps evaluate how many parts can be salvaged through a relatively low-cost, single rework process.

Please infer the answer using as few queries as possible.

## Query and Answer Format (must be strictly followed)

Each query should use the following XML format (only one query per turn), using A, B, C for respective defects:

- Query single defect A (Surface Scratch Defect):
<query>A</query>

- Query single defect B (Dimensional Deviation):
<query>B</query>

- Query single defect C (Substandard Material Hardness):
<query>C</query>

- Query two defects A and B:
<query>A,B</query>

- Query two defects A and C:
<query>A,C</query>

- Query two defects B and C:
<query>B,C</query>

- Query three defects A, B, and C:
<query>A,B,C</query>

When submitting the final answer, provide the total number of parts with "exactly one defect" (a non-negative integer), in this format:

<answer>5</answer>
"""

    # ================= 场景 5：法律 =================
    contextualized_rule_zh_5 = """\
欢迎进入“企业合规审计”系统，规则如下：

系统提取了包含 {n} 个企业合规审计案件的集合。每个案件都可能存在以下三种违规情况的任意组合：税务申报异常（属性 A）、劳动合同违规（属性 B）、环保资质缺失（属性 C）。每个案件可能存在零个、一个、两个或全部三个违规情况。这些案件的违规事实在归档后是固定的，不会改变。

你可以反复向我提出计数查询，每次查询指定一种或多种违规情况的组合，我会告诉你“同时存在所有这些指定违规”的案件数量。

允许的查询类型包括：
- 查询单项违规：询问存在税务申报异常的案件数量（记作 |A|）
- 查询单项违规：询问存在劳动合同违规的案件数量（记作 |B|）
- 查询单项违规：询问存在环保资质缺失的案件数量（记作 |C|）
- 查询两项违规：询问同时存在税务申报异常和劳动合同违规的案件数量（记作 |A∧B|）
- 查询两项违规：询问同时存在税务申报异常和环保资质缺失的案件数量（记作 |A∧C|）
- 查询两项违规：询问同时存在劳动合同违规和环保资质缺失的案件数量（记作 |B∧C|）
- 查询三项违规：询问同时存在上述三项违规情况的案件数量（记作 |A∧B∧C|）

注意：查询返回的是“至少存在所查询的全部违规”的案件数量，不限制案件是否还涉及其他违规点。

你的目标是：推断出“恰好仅存在一项违规情况”的案件总数。以便将这类案情相对单一的案卷分配给单法务领域的初级律师跟进处理。

请通过尽可能少的查询次数来推断出答案。

## 查询和提交答案的格式（必须严格遵守）

每次查询请使用以下 XML 格式（只能查询一次），使用 A、B、C 代表对应违规项：

- 查询单项违规 A (税务申报异常)：
<query>A</query>

- 查询单项违规 B (劳动合同违规)：
<query>B</query>

- 查询单项违规 C (环保资质缺失)：
<query>C</query>

- 查询两项违规 A 和 B：
<query>A,B</query>

- 查询两项违规 A 和 C：
<query>A,C</query>

- 查询两项违规 B 和 C：
<query>B,C</query>

- 查询三项违规 A、B 和 C：
<query>A,B,C</query>

提交最终答案时，请给出“恰好仅存在一项违规情况”的案件总数（一个非负整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Corporate Compliance Audit" system. Here are the rules:

The system involves a set of {n} enterprise audit cases. Each case may have any combination of three violations: Tax Declaration Anomalies (Attribute A), Labor Contract Violations (Attribute B), and Missing Environmental Qualifications (Attribute C). Each case can have zero, one, two, or all three of these violations. The violation facts are fixed once archived and will not change.

You can repeatedly ask me counting queries. Each query specifies one or more violations, and I will tell you the count of cases that "have all the specified violations simultaneously".

Allowed query types include:
- Query single violation: ask for the count of cases with Tax Declaration Anomalies (denoted as |A|)
- Query single violation: ask for the count of cases with Labor Contract Violations (denoted as |B|)
- Query single violation: ask for the count of cases with Missing Environmental Qualifications (denoted as |C|)
- Query two violations: ask for the count of cases with both A and B (denoted as |A∧B|)
- Query two violations: ask for the count of cases with both A and C (denoted as |A∧C|)
- Query two violations: ask for the count of cases with both B and C (denoted as |B∧C|)
- Query three violations: ask for the count of cases with A, B, and C all together (denoted as |A∧B∧C|)

Note: The query returns the count of cases that have "at least all the queried violations", without restricting whether they involve other legal issues.

Your goal is: to infer the total number of cases that have "exactly one violation". This allows us to assign these relatively straightforward, single-domain cases to junior lawyers for follow-up.

Please infer the answer using as few queries as possible.

## Query and Answer Format (must be strictly followed)

Each query should use the following XML format (only one query per turn), using A, B, C for respective violations:

- Query single violation A (Tax Declaration Anomalies):
<query>A</query>

- Query single violation B (Labor Contract Violations):
<query>B</query>

- Query single violation C (Missing Environmental Qualifications):
<query>C</query>

- Query two violations A and B:
<query>A,B</query>

- Query two violations A and C:
<query>A,C</query>

- Query two violations B and C:
<query>B,C</query>

- Query three violations A, B, and C:
<query>A,B,C</query>

When submitting the final answer, provide the total number of cases with "exactly one violation" (a non-negative integer), in this format:

<answer>5</answer>
"""

    tags = ["answer", "query"]

    # 难度说明：
    # 1 (简单)       - N=10, 答案较小，分布简单
    # 2 (中等偏下)   - N=15, 答案中等
    # 3 (中等偏上)   - N=20, 分布较复杂
    # 4 (较难)       - N=25, 分布复杂
    # 5 (难)         - N=30, 分布最复杂

    DIFFICULTY_CONFIG = {
        1: {
            "n": 10,
            # 元素属性：用二进制表示 (A, B, C)
            # 000=无属性, 001=C, 010=B, 011=B∧C, 100=A, 101=A∧C, 110=A∧B, 111=A∧B∧C
            "attributes": [
                (1, 0, 0), (1, 0, 0),      # 2个只有A
                (0, 1, 0), (0, 1, 0),      # 2个只有B
                (0, 0, 1),                  # 1个只有C
                (1, 1, 0),                  # 1个A∧B
                (1, 0, 1),                  # 1个A∧C
                (0, 1, 1),                  # 1个B∧C
                (1, 1, 1),                  # 1个A∧B∧C
                (0, 0, 0),                  # 1个无属性
            ],
        },
        2: {
            "n": 15,
            "attributes": [
                (1, 0, 0), (1, 0, 0), (1, 0, 0),  # 3个只有A
                (0, 1, 0), (0, 1, 0),              # 2个只有B
                (0, 0, 1), (0, 0, 1),              # 2个只有C
                (1, 1, 0), (1, 1, 0),              # 2个A∧B
                (1, 0, 1), (1, 0, 1),              # 2个A∧C
                (0, 1, 1),                         # 1个B∧C
                (1, 1, 1),                         # 1个A∧B∧C
                (0, 0, 0), (0, 0, 0),              # 2个无属性
            ],
        },
        3: {
            "n": 20,
            "attributes": [
                (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0),  # 4个只有A
                (0, 1, 0), (0, 1, 0), (0, 1, 0),             # 3个只有B
                (0, 0, 1), (0, 0, 1),                        # 2个只有C
                (1, 1, 0), (1, 1, 0), (1, 1, 0),             # 3个A∧B
                (1, 0, 1), (1, 0, 1),                        # 2个A∧C
                (0, 1, 1), (0, 1, 1),                        # 2个B∧C
                (1, 1, 1), (1, 1, 1),                        # 2个A∧B∧C
                (0, 0, 0), (0, 0, 0),                        # 2个无属性
            ],
        },
        4: {
            "n": 25,
            "attributes": [
                (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0),  # 5个只有A
                (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0),             # 4个只有B
                (0, 0, 1), (0, 0, 1), (0, 0, 1),                        # 3个只有C
                (1, 1, 0), (1, 1, 0), (1, 1, 0), (1, 1, 0),             # 4个A∧B
                (1, 0, 1), (1, 0, 1), (1, 0, 1),                        # 3个A∧C
                (0, 1, 1), (0, 1, 1),                                   # 2个B∧C
                (1, 1, 1), (1, 1, 1),                                   # 2个A∧B∧C
                (0, 0, 0), (0, 0, 0),                                   # 2个无属性
            ],
        },
        5: {
            "n": 30,
            "attributes": [
                (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0),  # 6个只有A
                (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0),             # 5个只有B
                (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1),                        # 4个只有C
                (1, 1, 0), (1, 1, 0), (1, 1, 0), (1, 1, 0), (1, 1, 0),             # 5个A∧B
                (1, 0, 1), (1, 0, 1), (1, 0, 1),                                   # 3个A∧C
                (0, 1, 1), (0, 1, 1), (0, 1, 1),                                   # 3个B∧C
                (1, 1, 1), (1, 1, 1), (1, 1, 1),                                   # 3个A∧B∧C
                (0, 0, 0),                                                         # 1个无属性
            ],
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self._game_info["n"] = cfg["n"]
        
        # 存储每个元素的属性 (A, B, C)，元组形式
        self.attributes = cfg["attributes"]
        
        # 计算正确答案：恰好有一个属性为真的元素数量
        self.correct_answer = sum(
            1 for (a, b, c) in self.attributes
            if (a + b + c) == 1  # 恰好一个属性为真
        )

    def get_all_possible_queries(self) -> list[dict]:
        # 定义所有合法的查询组合
        # 单属性
        queries = ["A", "B", "C"]
        # 双属性
        queries.extend(["A,B", "A,C", "B,C"])
        # 三属性
        queries.append("A,B,C")
        
        results = []
        for q in queries:
            # 构造 parsed_info
            parsed_info = {"query": q}
            # 复用核心计算逻辑计算正确答案
            ans = self._cf_core_produce(parsed_info)
            results.append({
                "query": f"<query>{q}</query>",
                "answer": ans
            })
        
        return results

    def evaluate(self, parsed_info):
        # 解析答案：应该是一个非负整数
        try:
            answer = int(parsed_info["answer"].strip())
            return answer == self.correct_answer
        except:
            return False

    def _cf_make_wrong(self, correct):
        """将正确的计数结果篡改为错误值"""
        try:
            correct_val = int(correct)
            # 随机偏移 1~3，确保不为负且与正确值不同
            offset = random.choice([-3, -2, -1, 1, 2, 3])
            wrong_val = correct_val + offset
            if wrong_val < 0:
                wrong_val = correct_val + abs(offset)
            return str(wrong_val)
        except (ValueError, TypeError):
            return correct + " [error]"

    def _cf_core_produce(self, parsed_info):
        # 解析查询内容
        if "query" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        query_str = parsed_info["query"].strip().upper()
        
        # 解析查询的属性列表
        if not query_str:
            return "Error: Empty query." if self.config.language == "en" else "错误：查询为空。"
        
        # 分割并标准化属性名
        attrs = [x.strip() for x in query_str.split(",")]
        
        # 验证属性名有效性
        valid_attrs = {"A", "B", "C"}
        for attr in attrs:
            if attr not in valid_attrs:
                return "Error: Invalid attribute name." if self.config.language == "en" else "错误：无效的属性名。"
        
        # 去重并排序（保证一致性）
        attrs = sorted(set(attrs))
        
        # 检查查询是否为允许的类型
        if len(attrs) == 0 or len(attrs) > 3:
            return "Error: Invalid query format." if self.config.language == "en" else "错误：无效的查询格式。"
        
        # 统计满足条件的元素数量
        count = 0
        for (a, b, c) in self.attributes:
            attr_dict = {"A": a, "B": b, "C": c}
            # 检查是否所有查询的属性都为真
            if all(attr_dict[attr] == 1 for attr in attrs):
                count += 1
        
        return str(count)