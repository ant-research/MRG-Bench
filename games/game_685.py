from .base import Game
import re
import itertools


class SetDisjointnessGame(Game):

    game_rule_zh = """\
我们现在来玩一个"集合互斥判定"的推理游戏，规则如下：

游戏设定了一个编号集合 U = {{1, 2, ..., {n}}}。我已秘密确定了两个隐藏子集 R 和 B，它们都是 U 的子集。每个元素可能处于以下四种状态之一：
1. 仅在 R 中
2. 仅在 B 中
3. 同时在 R 和 B 中
4. 两者都不在

你的目标是判断 R 与 B 是否互斥（即两个集合没有共同元素）。你可以反复进行以下查询（每次一个查询），我会如实回答：

**计数查询**：给定一个测试子集 T（用编号列表表示），我会返回两个数字 (r, b)，其中：
- r = T 与 R 的交集元素个数
- b = T 与 B 的交集元素个数

例如，如果你查询 {{1, 2, 3}}，我可能返回 (2, 1)，表示这三个元素中有 2 个在 R 中，1 个在 B 中。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询时，使用以下 XML 格式，列出要查询的元素编号（用逗号分隔）：

<query>1,2,3</query>

提交最终答案时，必须指明判定结果：

**如果判定两集合互斥**（没有共同元素），使用：
<answer>Disjoint</answer>

**如果判定两集合不互斥**（有共同元素），必须提供一个见证元素（同时在 R 和 B 中的元素编号）：
<answer>Witness=5</answer>

注意：你需要用尽可能少的查询次数完成推理。
"""

    game_rule_en = """\
Let's play a "Set Disjointness Deduction" game. Here are the rules:

There is a set of numbers U = {{1, 2, ..., {n}}}. I have secretly determined two hidden subsets R and B, both subsets of U. Each element may be in one of four states:
1. Only in R
2. Only in B
3. In both R and B
4. In neither

Your goal is to determine whether R and B are disjoint (i.e., they have no common elements). You can repeatedly make the following query (one per turn), and I will answer truthfully:

**Count Query**: Given a test subset T (represented as a list of IDs), I will return two numbers (r, b), where:
- r = the number of elements in the intersection of T and R
- b = the number of elements in the intersection of T and B

For example, if you query {{1, 2, 3}}, I might return (2, 1), meaning among these three elements, 2 are in R and 1 is in B.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

For each query, use the following XML format, listing the element IDs to query (comma-separated):

<query>1,2,3</query>

When submitting the final answer, you must specify your conclusion:

**If you determine the sets are disjoint** (no common elements), use:
<answer>Disjoint</answer>

**If you determine the sets are not disjoint** (have common elements), you must provide a witness element (an ID that is in both R and B):
<answer>Witness=5</answer>

Note: You should complete the reasoning with as few queries as possible.
"""

    contextualized_rule_zh_1 = """\
智能交通系统故障排查：

在我们的城市轨道交通网络中，存在一个由 N 个核心站点组成的集合 U = {{1, 2, ..., {n}}}。最近系统检测到两类隐蔽的风险状况：R（轨道结构受损）和 B（排水系统失效），它们分别影响了 U 的某两个未知子集。每个站点可能处于以下四种状态之一：
1. 仅存在轨道受损（仅在 R 中）
2. 仅存在排水失效（仅在 B 中）
3. 同时存在轨道受损与排水失效（同时在 R 和 B 中）
4. 运行正常（两者都不在）

你的目标是判断 R 与 B 是否互斥（即排查是否存在同时面临两类风险的高危崩溃站点）。你可以反复派遣无人机小队进行以下“区域扫描”（每次一个查询），我会如实返回传感器的读数：

**计数查询**：给定一个测试站点集合 T（用编号列表表示），我会返回两个数字 (r, b)，其中：
- r = T 中存在轨道受损的站点个数
- b = T 中存在排水失效的站点个数

例如，如果你查询 {{1, 2, 3}}，我可能返回 (2, 1)，表示这三个站点中有 2 个轨道受损，1 个排水失效。

当你收集足够信息后，请提交最终排查报告。若报告错误或格式不符，排查任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次派遣无人机查询时，使用以下 XML 格式，列出要查询的站点编号（用逗号分隔）：

<query>1,2,3</query>

提交最终排查报告时，必须指明判定结果：

**如果判定两类风险互斥**（没有同时面临两种风险的站点），使用：
<answer>Disjoint</answer>

**如果判定两类风险不互斥**（存在高危崩溃站点），必须提供一个见证站点（同时在 R 和 B 中的站点编号）：
<answer>Witness=5</answer>

注意：你需要用尽可能少的扫描次数完成排查。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Intelligent Transit System Troubleshooting:

In our urban rail network, there is a set of core stations U = {{1, 2, ..., {n}}}. The system has recently detected two hidden risk factors: R (Track Structural Damage) and B (Drainage System Failure), which affect two unknown subsets of U. Each station may be in one of four states:
1. Only has track damage (Only in R)
2. Only has drainage failure (Only in B)
3. Has both track damage and drainage failure (In both R and B)
4. Operating normally (In neither)

Your goal is to determine whether R and B are disjoint (i.e., whether there are any high-risk stations suffering from both conditions). You can repeatedly dispatch drone squads to conduct the following "zone scans" (one query per turn), and I will provide the truthful sensor readings:

**Count Query**: Given a test set of stations T (represented as a list of IDs), I will return two numbers (r, b), where:
- r = the number of stations in T with track damage
- b = the number of stations in T with drainage failure

For example, if you query {{1, 2, 3}}, I might return (2, 1), meaning among these three stations, 2 have track damage and 1 has drainage failure.

When you have enough information, submit your final diagnostic report. If the answer is wrong or the format is invalid, the mission fails.

## Query and Answer Format (strictly required)

For each drone query, use the following XML format, listing the station IDs to scan (comma-separated):

<query>1,2,3</query>

When submitting the final report, you must specify your conclusion:

**If you determine the risks are disjoint** (no station has both issues), use:
<answer>Disjoint</answer>

**If you determine the risks are not disjoint** (a high-risk station exists), you must provide a witness station (an ID that is in both R and B):
<answer>Witness=5</answer>

Note: You should complete the troubleshooting with as few scans as possible.
"""

    contextualized_rule_zh_2 = """\
临床试验数据分析：

在我们的靶向药临床患者队列中，共有 N 名受试者，集合 U = {{1, 2, ..., {n}}}。研究团队怀疑队列中存在两类隐蔽的生理特征：R（携带基因突变 Alpha）和 B（血清病毒载量 Beta 超标）。每名受试者可能处于以下四种状态之一：
1. 仅携带 Alpha 突变（仅在 R 中）
2. 仅 Beta 载量超标（仅在 B 中）
3. 同时存在 Alpha 突变与 Beta 载量超标（同时在 R 和 B 中）
4. 两项指标均阴性（两者都不在）

你的目标是判断 R 与 B 是否互斥（即排查是否存在两项指标双阳性的高风险患者）。你可以反复进行以下“批次抽血化验”（每次一个查询），我会如实返回实验室的读数：

**计数查询**：给定一个受试者样本子集 T（用编号列表表示），我会返回两个数字 (r, b)，其中：
- r = T 中携带 Alpha 突变的患者人数
- b = T 中 Beta 载量超标的患者人数

例如，如果你查询 {{1, 2, 3}}，我可能返回 (2, 1)，表示这三名患者中有 2 人存在 Alpha 突变，1 人 Beta 载量超标。

当你收集足够信息后，请提交最终医学判定。若判定错误或格式不符，分析任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次提交化验名单时，使用以下 XML 格式，列出要查询的受试者编号（用逗号分隔）：

<query>1,2,3</query>

提交最终医学判定时，必须指明判定结果：

**如果判定两项指标互斥**（没有双阳性患者），使用：
<answer>Disjoint</answer>

**如果判定两项指标不互斥**（存在双阳性患者），必须提供一名见证患者（同时在 R 和 B 中的受试者编号）：
<answer>Witness=5</answer>

注意：由于化验试剂昂贵，你需要用尽可能少的查询次数完成分析。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Clinical Trial Data Analysis:

In our targeted therapy clinical cohort, there are N subjects, forming a set U = {{1, 2, ..., {n}}}. The research team suspects the presence of two hidden physiological traits: R (carrying Genetic Mutation Alpha) and B (elevated Serum Viral Load Beta). Each subject may be in one of four states:
1. Only carries Mutation Alpha (Only in R)
2. Only has elevated Load Beta (Only in B)
3. Has both Mutation Alpha and elevated Load Beta (In both R and B)
4. Negative for both metrics (In neither)

Your goal is to determine whether R and B are disjoint (i.e., whether there are any high-risk dual-positive patients). You can repeatedly conduct the following "batch blood tests" (one query per turn), and I will provide the truthful lab readings:

**Count Query**: Given a test subset of subjects T (represented as a list of IDs), I will return two numbers (r, b), where:
- r = the number of patients in T carrying Mutation Alpha
- b = the number of patients in T with elevated Load Beta

For example, if you query {{1, 2, 3}}, I might return (2, 1), meaning among these three patients, 2 have the Alpha mutation and 1 has an elevated Beta load.

When you have enough information, submit your final medical conclusion. If the conclusion is wrong or the format is invalid, the analysis fails.

## Query and Answer Format (strictly required)

For each batch test query, use the following XML format, listing the subject IDs to test (comma-separated):

<query>1,2,3</query>

When submitting the final conclusion, you must specify your diagnostic result:

**If you determine the metrics are disjoint** (no dual-positive patients), use:
<answer>Disjoint</answer>

**If you determine the metrics are not disjoint** (a dual-positive patient exists), you must provide a witness patient (an ID that is in both R and B):
<answer>Witness=5</answer>

Note: Since test reagents are expensive, you should complete the analysis with as few queries as possible.
"""

    contextualized_rule_zh_3 = """\
学科竞赛集训冲突排查：

在学校选拔的尖子生集合 U = {{1, 2, ..., {n}}} 中，教务处刚刚确立了两份保密的集训名单：R（入选数学奥林匹克集训）和 B（入选物理奥林匹克集训）。每位尖子生可能处于以下四种状态之一：
1. 仅入选数学集训（仅在 R 中）
2. 仅入选物理集训（仅在 B 中）
3. 同时入选两科集训（同时在 R 和 B 中）
4. 两科均未入选（两者都不在）

你的目标是判断 R 与 B 是否互斥（即排查是否存在同时需要参加两科集训，导致时间冲突的学生）。你可以反复向年级主任进行以下“名单核对”（每次一个查询），我会如实返回核对结果：

**计数查询**：给定一个测试学生小组 T（用学号列表表示），我会返回两个数字 (r, b)，其中：
- r = T 中入选数学集训的人数
- b = T 中入选物理集训的人数

例如，如果你查询 {{1, 2, 3}}，我可能返回 (2, 1)，表示这三名学生中有 2 人参加数学集训，1 人参加物理集训。

当你收集足够信息后，请提交最终排查结果。若结果错误或格式不符，排查任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次核对名单时，使用以下 XML 格式，列出要查询的学生学号（用逗号分隔）：

<query>1,2,3</query>

提交最终排查结果时，必须指明判定结果：

**如果判定两份名单互斥**（没有时间冲突的学生），使用：
<answer>Disjoint</answer>

**如果判定两份名单不互斥**（存在时间冲突的学生），必须提供一名见证学生（同时在 R 和 B 中的学生学号）：
<answer>Witness=5</answer>

注意：你需要用尽可能少的核对次数完成排查。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Academic Olympiad Conflict Resolution:

Among the school's elite student pool U = {{1, 2, ..., {n}}}, the academic affairs office has just finalized two confidential training rosters: R (Math Olympiad Camp) and B (Physics Olympiad Camp). Each student may be in one of four states:
1. Only selected for Math (Only in R)
2. Only selected for Physics (Only in B)
3. Selected for both camps (In both R and B)
4. Selected for neither (In neither)

Your goal is to determine whether R and B are disjoint (i.e., whether there are any students facing a schedule conflict by being in both camps). You can repeatedly request a "roster check" from the grade director (one query per turn), and I will provide the truthful check results:

**Count Query**: Given a test group of students T (represented as a list of IDs), I will return two numbers (r, b), where:
- r = the number of students in T selected for the Math camp
- b = the number of students in T selected for the Physics camp

For example, if you query {{1, 2, 3}}, I might return (2, 1), meaning among these three students, 2 are in the Math camp and 1 is in the Physics camp.

When you have enough information, submit your final resolution. If the resolution is wrong or the format is invalid, the task fails.

## Query and Answer Format (strictly required)

For each roster check query, use the following XML format, listing the student IDs (comma-separated):

<query>1,2,3</query>

When submitting the final resolution, you must specify your conclusion:

**If you determine the rosters are disjoint** (no scheduling conflicts), use:
<answer>Disjoint</answer>

**If you determine the rosters are not disjoint** (a student with a conflict exists), you must provide a witness student (an ID that is in both R and B):
<answer>Witness=5</answer>

Note: You should complete the resolution with as few checks as possible.
"""

    contextualized_rule_zh_4 = """\
自动化产线故障诊断：

在我们的核心智能制造流水线中，有 N 台关键机械臂，编号集合 U = {{1, 2, ..., {n}}}。维护中控系统提示可能存在两类潜在的隐患：R（机械轴承磨损超标）和 B（控制固件逻辑异常）。每台机械臂可能处于以下四种状态之一：
1. 仅机械磨损超标（仅在 R 中）
2. 仅固件逻辑异常（仅在 B 中）
3. 同时存在机械磨损与固件异常（同时在 R 和 B 中）
4. 运行正常（两者都不在）

你的目标是判断 R 与 B 是否互斥（即排查这两类故障是否完全独立，或者是否存在同时发生双重故障的瘫痪节点）。你可以反复通过工业物联网总线发送以下“诊断指令”（每次一个查询），我会如实返回底层硬件的自检读数：

**计数查询**：给定一个测试机械臂批次 T（用编号列表表示），我会返回两个数字 (r, b)，其中：
- r = T 中机械磨损超标的机械臂数量
- b = T 中固件逻辑异常的机械臂数量

例如，如果你查询 {{1, 2, 3}}，我可能返回 (2, 1)，表示这三台设备中有 2 台存在机械磨损，1 台存在固件异常。

当你收集足够信息后，请提交最终诊断报告。若报告错误或格式不符，产线将面临停机风险，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次发送诊断指令时，使用以下 XML 格式，列出要查询的设备编号（用逗号分隔）：

<query>1,2,3</query>

提交最终诊断报告时，必须指明判定结果：

**如果判定两类故障互斥**（没有双重故障的设备），使用：
<answer>Disjoint</answer>

**如果判定两类故障不互斥**（存在双重故障的设备），必须提供一台见证设备（同时在 R 和 B 中的机械臂编号）：
<answer>Witness=5</answer>

注意：为了避免产线长时间降级运行，你需要用尽可能少的诊断次数完成推理。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Automated Production Line Diagnostics:

In our core smart manufacturing assembly line, there are N critical robotic arms, forming a set U = {{1, 2, ..., {n}}}. The central maintenance system has flagged two potential underlying faults: R (Mechanical Bearing Wear) and B (Firmware Logic Anomaly). Each robotic arm may be in one of four states:
1. Only has mechanical wear (Only in R)
2. Only has a firmware anomaly (Only in B)
3. Has both mechanical wear and firmware anomaly (In both R and B)
4. Operating normally (In neither)

Your goal is to determine whether R and B are disjoint (i.e., whether these fault types are completely independent, or if there is a crippled node suffering from a dual fault). You can repeatedly send the following "diagnostic commands" via the IIoT bus (one query per turn), and I will provide the truthful hardware self-test readings:

**Count Query**: Given a test batch of robotic arms T (represented as a list of IDs), I will return two numbers (r, b), where:
- r = the number of arms in T with mechanical wear
- b = the number of arms in T with a firmware anomaly

For example, if you query {{1, 2, 3}}, I might return (2, 1), meaning among these three devices, 2 have mechanical wear and 1 has a firmware anomaly.

When you have enough information, submit your final diagnostic report. If the report is wrong or the format is invalid, the production line faces downtime, and the mission fails.

## Query and Answer Format (strictly required)

For each diagnostic query, use the following XML format, listing the device IDs to test (comma-separated):

<query>1,2,3</query>

When submitting the final report, you must specify your conclusion:

**If you determine the faults are disjoint** (no dual-fault devices), use:
<answer>Disjoint</answer>

**If you determine the faults are not disjoint** (a dual-fault device exists), you must provide a witness device (an ID that is in both R and B):
<answer>Witness=5</answer>

Note: To prevent prolonged degraded operations, you should complete the diagnostics with as few queries as possible.
"""

    contextualized_rule_zh_5 = """\
诉讼案认证物证审查：

在一起复杂的商业合规诉讼案中，法庭传唤了 N 份核心商业文档，编号集合 U = {{1, 2, ..., {n}}}。我们的律师团队需要审查其中两类高度敏感的违规内容：R（涉及个人隐私泄露）和 B（包含财务造假证据）。每份文档可能处于以下四种状态之一：
1. 仅涉及隐私泄露（仅在 R 中）
2. 仅包含财务造假（仅在 B 中）
3. 同时存在隐私泄露与财务造假（同时在 R 和 B 中）
4. 内容完全合规（两者都不在）

你的目标是判断 R 与 B 是否互斥（即排查卷宗中是否存在同时坐实两项指控的“铁证”文档）。你可以反复将文档提交给智能法务助手进行“合规扫描”（每次一个查询），我会如实返回审查读数：

**计数查询**：给定一个测试文档批次 T（用编号列表表示），我会返回两个数字 (r, b)，其中：
- r = T 中涉及隐私泄露的文档数量
- b = T 中包含财务造假的文档数量

例如，如果你查询 {{1, 2, 3}}，我可能返回 (2, 1)，表示这三份文档中有 2 份涉及隐私问题，1 份涉及财务问题。

当你收集足够信息后，请提交最终审查意见。若意见错误或格式不符，法庭辩护将陷入被动，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次提交法务扫描时，使用以下 XML 格式，列出要查询的文档编号（用逗号分隔）：

<query>1,2,3</query>

提交最终审查意见时，必须指明判定结果：

**如果判定两类违规互斥**（没有同时坐实两项指控的文档），使用：
<answer>Disjoint</answer>

**如果判定两类违规不互斥**（存在双重违规的“铁证”），必须提供一份见证文档（同时在 R 和 B 中的文档编号）：
<answer>Witness=5</answer>

注意：由于法律审查耗时费力，你需要用尽可能少的扫描次数完成推理。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Litigation Evidence Review:

In a complex commercial compliance lawsuit, the court has subpoenaed N core business documents, forming a set U = {{1, 2, ..., {n}}}. Our legal team must review them for two highly sensitive types of violations: R (Privacy Violation) and B (Financial Fraud Evidence). Each document may be in one of four states:
1. Only involves a privacy violation (Only in R)
2. Only contains financial fraud evidence (Only in B)
3. Contains both privacy violation and financial fraud (In both R and B)
4. Completely compliant (In neither)

Your goal is to determine whether R and B are disjoint (i.e., whether there is any "smoking gun" document in the docket that solidifies both allegations simultaneously). You can repeatedly submit documents to the AI paralegal for a "compliance scan" (one query per turn), and I will provide the truthful review readings:

**Count Query**: Given a test batch of documents T (represented as a list of IDs), I will return two numbers (r, b), where:
- r = the number of documents in T involving privacy violations
- b = the number of documents in T containing financial fraud

For example, if you query {{1, 2, 3}}, I might return (2, 1), meaning among these three documents, 2 involve privacy issues and 1 involves financial fraud.

When you have enough information, submit your final review opinion. If the opinion is wrong or the format is invalid, our court defense will be compromised, and the game fails.

## Query and Answer Format (strictly required)

For each paralegal scan query, use the following XML format, listing the document IDs to scan (comma-separated):

<query>1,2,3</query>

When submitting the final review opinion, you must specify your conclusion:

**If you determine the violations are disjoint** (no document solidifies both allegations), use:
<answer>Disjoint</answer>

**If you determine the violations are not disjoint** (a dual-violation "smoking gun" exists), you must provide a witness document (an ID that is in both R and B):
<answer>Witness=5</answer>

Note: Since legal review is time-consuming, you should complete the deduction with as few scans as possible.
"""

    tags = ["answer", "query"]
    
    reasoning_type = "演绎推理"
    data_structure = "集合"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "R": [1, 2],
                "B": [3, 4],
                "is_disjoint": True,
            },
            2: {
                "n": 6,
                "R": [1, 2, 3],
                "B": [3, 4, 5],
                "is_disjoint": False,
            },
            3: {
                "n": 8,
                "R": [1, 2, 3, 4],
                "B": [5, 6, 7, 8],
                "is_disjoint": True,
            },
            4: {
                "n": 10,
                "R": [1, 2, 3, 4, 5],
                "B": [4, 5, 6, 7, 8],
                "is_disjoint": False,
            },
            5: {
                "n": 12,
                "R": [1, 3, 5, 7, 9, 11],
                "B": [2, 4, 6, 8, 10, 12],
                "is_disjoint": True,
            },
        },
        "en": {
            1: {
                "n": 4,
                "R": [1, 2],
                "B": [3, 4],
                "is_disjoint": True,
            },
            2: {
                "n": 6,
                "R": [1, 2, 3],
                "B": [3, 4, 5],
                "is_disjoint": False,
            },
            3: {
                "n": 8,
                "R": [1, 2, 3, 4],
                "B": [5, 6, 7, 8],
                "is_disjoint": True,
            },
            4: {
                "n": 10,
                "R": [1, 2, 3, 4, 5],
                "B": [4, 5, 6, 7, 8],
                "is_disjoint": False,
            },
            5: {
                "n": 12,
                "R": [1, 3, 5, 7, 9, 11],
                "B": [2, 4, 6, 8, 10, 12],
                "is_disjoint": True,
            },
        },
    }

    def _initialize_game(self):
        """初始化游戏配置，设置隐藏的两个集合 R 和 B"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        
        self.R = set(cfg["R"])
        self.B = set(cfg["B"])
        self.is_disjoint = cfg["is_disjoint"]
        
        self.intersection = self.R & self.B

    def evaluate(self, parsed_info):
        """评估玩家的最终答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        if raw_ans == "Disjoint":
            return self.is_disjoint
        
        witness_match = re.match(r'^Witness\s*=\s*(\d+)$', raw_ans, re.IGNORECASE)
        if witness_match:
            try:
                witness_id = int(witness_match.group(1))
                return not self.is_disjoint and witness_id in self.intersection
            except:
                return False
        
        return False

    def _cf_core_produce(self, parsed_info):
        """处理查询并返回计数的原始核心业务逻辑"""
        if "query" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        raw_query = parsed_info["query"].strip()
        
        if not raw_query:
            if self.config.language == "zh":
                return "错误：查询集合不能为空。"
            else:
                return "Error: Query set cannot be empty."
        
        try:
            query_ids = [int(x.strip()) for x in raw_query.split(",") if x.strip()]
            
            n = self._game_info["n"]
            for qid in query_ids:
                if qid < 1 or qid > n:
                    if self.config.language == "zh":
                        return f"错误：编号 {qid} 超出范围 [1, {n}]。"
                    else:
                        return f"Error: ID {qid} is out of range [1, {n}]."
            
            query_set = set(query_ids)
            r_count = len(query_set & self.R)
            b_count = len(query_set & self.B)
            
            return f"({r_count}, {b_count})"
            
        except ValueError:
            if self.config.language == "zh":
                return "错误：查询格式无效，请使用逗号分隔的数字列表。"
            else:
                return "Error: Invalid query format. Please use comma-separated numbers."

    def get_all_possible_queries(self) -> list[dict]:
        """枚举所有单元素查询并返回对应的正确答案。"""
        results = []
        n = self._game_info["n"]
        
        for i in range(1, n + 1):
            query_set = {i}
            r_count = len(query_set & self.R)
            b_count = len(query_set & self.B)
            answer_str = f"({r_count}, {b_count})"
            
            results.append({
                "query": f"<query>{i}</query>",
                "answer": answer_str
            })
        
        return results

    def _cf_make_wrong(self, correct: str) -> str:
        """根据正确答案生成错误答案"""
        m = re.match(r'^\((\d+),\s*(\d+)\)$', correct.strip())
        if m:
            r_val = int(m.group(1))
            b_val = int(m.group(2))
            # 对 r 值进行扰动：+1 或 -1（保证非负）
            if r_val > 0:
                wrong_r = r_val - 1
            else:
                wrong_r = r_val + 1
            return f"({wrong_r}, {b_val})"
            
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if "是" in correct:
            return correct.replace("是", "否")
        if "否" in correct:
            return correct.replace("否", "是")
            
        lower_correct = correct.lower()
        if "yes" in lower_correct:
            if "Yes" in correct: return correct.replace("Yes", "No")
            if "YES" in correct: return correct.replace("YES", "NO")
            return correct.replace("yes", "no")
        if "no" in lower_correct:
            if "No" in correct: return correct.replace("No", "Yes")
            if "NO" in correct: return correct.replace("NO", "YES")
            return correct.replace("no", "yes")

        return correct + "_WRONG"