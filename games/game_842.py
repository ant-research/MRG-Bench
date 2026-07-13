# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   后缀统计：序列后k个元素的某统计特征是什么
# ============================================================

from .base import Game
import random


class HiddenBijectionReadingGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "序列"

    game_rule_zh = """\
我们现在来玩一个"隐藏双射读数"推理游戏，规则如下：

游戏设定了一个隐藏参数对 (k, g)，其中：
- k 为未知整数，取值范围在 2 到 6 之间。
- g 为未知的双射函数，将集合 {0, 1, ..., k} 映射到自身（即 g 是一个排列）。

系统使用二值序列字母表 {0, 1}。定义读数函数 f 作用于任意序列 S：
- 令 c 为序列 S 的最后 k 位中 1 的个数。
- 如果序列长度小于 k，则视为在左侧用 0 补齐至长度 k。
- 读数结果为 f(S) = g(c)。

系统维护两条序列：
1. 实验序列 S_exp：初始为空，你可以对其进行操作。
2. 官方序列 S_off：长度为 {N}，内容固定且可查询。

你可以通过以下交互来推理隐藏参数：

## 对实验序列的操作与查询

- 追加 1：在 S_exp 末尾追加字符 1。
- 追加 0：在 S_exp 末尾追加字符 0。
- 重置：将 S_exp 清空（等效于最近 k 位全为 0）。
- 读数查询：查询当前 S_exp 的读数值 f(S_exp)。

## 对官方信息的查询

- 官方序列查询：获取完整的官方序列 S_off。
- 官方长度查询：获取官方序列长度 N。

## 提交最终答案

当你收集足够信息后，需要提交三项内容：
1. 参数 k 的值
2. 完整的双射函数 g 的映射表（格式：g(0)=a0, g(1)=a1, ..., g(k)=ak）
3. 官方序列的最终读数值

若三项全部正确，游戏成功；任一项错误，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次只能提出一个查询或操作。请使用以下 XML 格式：

- 追加 1：
<append_one></append_one>

- 追加 0：
<append_zero></append_zero>

- 重置实验序列：
<reset></reset>

- 读数查询：
<query_reading></query_reading>

- 查询官方序列：
<query_official></query_official>

- 查询官方长度：
<query_length></query_length>

- 提交最终答案（注意格式严格，用逗号和空格分隔）：
<answer>k=3, g=g(0)=2 g(1)=0 g(2)=1 g(3)=3, official_reading=2</answer>
"""

    game_rule_en = """\
Let's play a "Hidden Bijection Reading" deduction game. Here are the rules:

The game has set up a hidden parameter pair (k, g), where:
- k is an unknown integer in the range from 2 to 6.
- g is an unknown bijection that maps the set {0, 1, ..., k} to itself (i.e., g is a permutation).

The system uses a binary sequence alphabet {0, 1}. Define a reading function f for any sequence S:
- Let c be the count of 1s in the last k positions of sequence S.
- If the sequence length is less than k, pad with 0s on the left to reach length k.
- The reading result is f(S) = g(c).

The system maintains two sequences:
1. Experimental sequence S_exp: initially empty, you can perform operations on it.
2. Official sequence S_off: length {N}, fixed content that can be queried.

You can deduce the hidden parameters through the following interactions:

## Operations and Queries on Experimental Sequence

- Append 1: append character 1 to the end of S_exp.
- Append 0: append character 0 to the end of S_exp.
- Reset: clear S_exp (equivalent to having the last k bits all 0).
- Reading query: query the current reading value f(S_exp).

## Queries on Official Information

- Official sequence query: get the complete official sequence S_off.
- Official length query: get the length N of the official sequence.

## Submit Final Answer

When you have gathered enough information, submit three items:
1. The value of parameter k
2. The complete mapping table of bijection g (format: g(0)=a0, g(1)=a1, ..., g(k)=ak)
3. The final reading value of the official sequence

If all three items are correct, the game succeeds; if any item is incorrect, the game fails.

## Query and Answer Format (must strictly follow)

Each turn you can only make one query or operation. Use the following XML format:

- Append 1:
<append_one></append_one>

- Append 0:
<append_zero></append_zero>

- Reset experimental sequence:
<reset></reset>

- Reading query:
<query_reading></query_reading>

- Query official sequence:
<query_official></query_official>

- Query official length:
<query_length></query_length>

- Submit final answer (note strict format, separated by commas and spaces):
<answer>k=3, g=g(0)=2 g(1)=0 g(2)=1 g(3)=3, official_reading=2</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用“城市智能交通信号预警控制系统”沙盘推演模块。

系统设定了一个隐藏的交通状态模型 (k, g)，其中：
- k 为未知的时间窗口参数（单位：小时），取值范围在 2 到 6 之间。
- g 为未知的预警等级映射函数，将集合 {0, 1, ..., k}（表示窗口期内发生拥堵的小时数）一一映射到自身预警级别 {0, 1, ..., k}（即 g 是一个排列）。

系统使用二值序列 {0, 1} 记录路口每小时的交通流量状态（0代表畅通，1代表拥堵）。定义预警评估函数 f 作用于任意流量序列 S：
- 令 c 为序列 S 最近 k 个小时内发生拥堵（1）的次数。
- 如果记录时长不足 k 小时，则系统默认在左侧用畅通（0）补齐至长度 k。
- 当前交通预警评估结果为 f(S) = g(c)。

系统维护两条序列：
1. 演练沙盘序列 S_exp：初始为空，你可以向其中注入模拟流量状态。
2. 历史基准序列 S_off：某主干道固化日志，长度为 {N}，内容固定且可查询。

你可以通过以下交互来推理隐藏参数：

## 对演练沙盘序列的操作与查询

- 注入拥堵记录（1）：在 S_exp 末尾追加字符 1（拥堵）。
- 注入畅通记录（0）：在 S_exp 末尾追加字符 0（畅通）。
- 重置演练沙盘：将 S_exp 清空（等效于最近 k 小时全部为畅通 0）。
- 查询当前预警级别：查询当前 S_exp 的预警评估结果 f(S_exp)。

## 对历史基准信息的查询

- 查询基准日志：获取完整的历史基准序列 S_off。
- 查询基准时长：获取历史基准序列长度 N。

## 提交系统参数分析报告

当你收集足够信息后，需要提交三项内容：
1. 时间窗口参数 k 的值
2. 完整的预警映射表 g（格式：g(0)=a0, g(1)=a1, ..., g(k)=ak）
3. 历史基准序列的最终预警评估结果

若三项全部正确，模型校准成功；任一项错误，校准失败。

## 询问与提交答案的格式（必须严格遵守）

每次只能发送一个指令或操作。请使用以下 XML 格式：

- 注入拥堵记录（1）：
<append_one></append_one>

- 注入畅通记录（0）：
<append_zero></append_zero>

- 重置演练沙盘：
<reset></reset>

- 查询当前预警级别：
<query_reading></query_reading>

- 查询基准日志：
<query_official></query_official>

- 查询基准时长：
<query_length></query_length>

- 提交最终报告（注意格式严格，用逗号和空格分隔）：
<answer>k=3, g=g(0)=2 g(1)=0 g(2)=1 g(3)=3, official_reading=2</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Intelligent Traffic Signal Warning Control System" sandbox simulation module.

The system is governed by a hidden traffic state model (k, g), where:
- k is an unknown integer representing the monitoring time window (in hours), ranging from 2 to 6.
- g is an unknown warning level mapping bijection that maps the set {0, 1, ..., k} (representing the number of congested hours in the window) to the warning levels {0, 1, ..., k} (i.e., g is a permutation).

The system uses a binary alphabet {0, 1} to record the hourly traffic flow status (0 for smooth, 1 for congested). Define a warning evaluation function f for any traffic sequence S:
- Let c be the count of congested hours (1s) in the last k positions of sequence S.
- If the sequence length is less than k hours, pad with smooth statuses (0s) on the left to reach length k.
- The current warning evaluation result is f(S) = g(c).

The system maintains two sequences:
1. Experimental Sandbox Sequence S_exp: initially empty, you can simulate traffic statuses on it.
2. Official Baseline Sequence S_off: fixed historical log of a main road with length {N}, which can be queried.

You can deduce the hidden parameters through the following interactions:

## Operations and Queries on Sandbox Sequence

- Inject Congestion (1): append character 1 to the end of S_exp.
- Inject Smooth Traffic (0): append character 0 to the end of S_exp.
- Reset Sandbox: clear S_exp (equivalent to having the last k hours all smooth 0).
- Query Warning Level: query the current warning result f(S_exp).

## Queries on Official Baseline Information

- Query Baseline Log: get the complete official baseline sequence S_off.
- Query Baseline Length: get the length N of the official baseline sequence.

## Submit System Parameter Analysis

When you have gathered enough information, submit three items:
1. The value of the time window parameter k
2. The complete mapping table of warning function g (format: g(0)=a0, g(1)=a1, ..., g(k)=ak)
3. The final warning evaluation result of the official baseline sequence

If all three items are correct, the calibration succeeds; if any item is incorrect, it fails.

## Query and Answer Format (must strictly follow)

Each turn you can only make one query or operation. Use the following XML format:

- Inject Congestion (1):
<append_one></append_one>

- Inject Smooth Traffic (0):
<append_zero></append_zero>

- Reset Sandbox:
<reset></reset>

- Query Warning Level:
<query_reading></query_reading>

- Query Baseline Log:
<query_official></query_official>

- Query Baseline Length:
<query_length></query_length>

- Submit final analysis (note strict format, separated by commas and spaces):
<answer>k=3, g=g(0)=2 g(1)=0 g(2)=1 g(3)=3, official_reading=2</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用“临床生物标志物诊断评估系统”推演模块。

系统设定了一个隐藏的临床诊断模型 (k, g)，其中：
- k 为未知的观察周期参数（表示最近的检测次数），取值范围在 2 到 6 之间。
- g 为未知的临床分期映射函数，将集合 {0, 1, ..., k}（表示周期内阳性检测的次数）一一映射到自身临床分期 {0, 1, ..., k}（即 g 是一个排列）。

系统使用二值序列 {0, 1} 记录病患的单次检测结果（0代表阴性，1代表阳性）。定义临床分期评估函数 f 作用于任意病历序列 S：
- 令 c 为序列 S 最近 k 次检测中呈阳性（1）的次数。
- 如果记录次数不足 k 次，则系统默认在早期用阴性（0）补齐至长度 k。
- 当前临床分期诊断结果为 f(S) = g(c)。

系统维护两条序列：
1. 模拟病历序列 S_exp：初始为空，你可以向其中注入模拟检测结果。
2. 基准标准病历 S_off：某典型病例的固化记录，长度为 {N}，内容固定且可查询。

你可以通过以下交互来推理隐藏诊断参数：

## 对模拟病历序列的操作与查询

- 注入阳性结果（1）：在 S_exp 末尾追加字符 1（阳性）。
- 注入阴性结果（0）：在 S_exp 末尾追加字符 0（阴性）。
- 重置模拟病历：将 S_exp 清空（等效于最近 k 次检测全部为阴性 0）。
- 查询当前临床分期：查询当前 S_exp 的分期诊断结果 f(S_exp)。

## 对基准标准病历的查询

- 查询基准病历：获取完整的基准序列 S_off。
- 查询病历长度：获取基准序列长度 N。

## 提交诊断模型解析报告

当你收集足够信息后，需要提交三项内容：
1. 观察周期参数 k 的值
2. 完整的临床分期映射表 g（格式：g(0)=a0, g(1)=a1, ..., g(k)=ak）
3. 基准标准病历的最终分期诊断结果

若三项全部正确，解析成功；任一项错误，解析失败。

## 询问与提交答案的格式（必须严格遵守）

每次只能发送一个指令或操作。请使用以下 XML 格式：

- 注入阳性结果（1）：
<append_one></append_one>

- 注入阴性结果（0）：
<append_zero></append_zero>

- 重置模拟病历：
<reset></reset>

- 查询当前临床分期：
<query_reading></query_reading>

- 查询基准病历：
<query_official></query_official>

- 查询病历长度：
<query_length></query_length>

- 提交最终报告（注意格式严格，用逗号和空格分隔）：
<answer>k=3, g=g(0)=2 g(1)=0 g(2)=1 g(3)=3, official_reading=2</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Clinical Biomarker Diagnostic Assessment" simulator.

The diagnostic system is governed by a hidden model parameter pair (k, g), where:
- k is an unknown integer representing the observation cycle (number of previous tests), ranging from 2 to 6.
- g is an unknown clinical stage mapping bijection that maps the set {0, 1, ..., k} (count of positive tests in the cycle) to clinical stages {0, 1, ..., k} (i.e., g is a permutation).

The system uses a binary alphabet {0, 1} to record a patient's individual test results (0 for negative, 1 for positive). Define a clinical stage evaluation function f for any patient record sequence S:
- Let c be the count of positive tests (1s) in the last k positions of sequence S.
- If the sequence length is less than k tests, pad with negative results (0s) on the left to reach length k.
- The current clinical diagnostic stage is f(S) = g(c).

The system maintains two sequences:
1. Simulated Patient Record S_exp: initially empty, you can inject simulated test results into it.
2. Standard Baseline Record S_off: fixed clinical history of a typical case with length {N}, which can be queried.

You can deduce the hidden parameters through the following interactions:

## Operations and Queries on Simulated Record

- Inject Positive Result (1): append character 1 to the end of S_exp.
- Inject Negative Result (0): append character 0 to the end of S_exp.
- Reset Simulation: clear S_exp (equivalent to having the last k tests all negative 0).
- Query Clinical Stage: query the current diagnostic stage f(S_exp).

## Queries on Standard Baseline Record

- Query Baseline Record: get the complete standard baseline sequence S_off.
- Query Baseline Length: get the length N of the baseline sequence.

## Submit Diagnostic Model Analysis

When you have gathered enough information, submit three items:
1. The value of the observation cycle parameter k
2. The complete mapping table of clinical stage function g (format: g(0)=a0, g(1)=a1, ..., g(k)=ak)
3. The final clinical diagnostic stage of the standard baseline record

If all three items are correct, the analysis succeeds; if any item is incorrect, it fails.

## Query and Answer Format (must strictly follow)

Each turn you can only make one query or operation. Use the following XML format:

- Inject Positive Result (1):
<append_one></append_one>

- Inject Negative Result (0):
<append_zero></append_zero>

- Reset Simulation:
<reset></reset>

- Query Clinical Stage:
<query_reading></query_reading>

- Query Baseline Record:
<query_official></query_official>

- Query Baseline Length:
<query_length></query_length>

- Submit final analysis (note strict format, separated by commas and spaces):
<answer>k=3, g=g(0)=2 g(1)=0 g(2)=1 g(3)=3, official_reading=2</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎进入“学生学业动态滚动评估系统”沙箱环境。

系统内嵌了一个隐藏的学业评估模型 (k, g)，其中：
- k 为未知的滚动考核窗口参数（表示最近的作业/测验次数），取值范围在 2 到 6 之间。
- g 为未知的综合评级映射函数，将集合 {0, 1, ..., k}（表示窗口期内达标的次数）一一映射到评级档位 {0, 1, ..., k}（即 g 是一个排列）。

系统使用二值序列 {0, 1} 记录学生每次考核的结果（0代表未达标，1代表达标）。定义综合评级函数 f 作用于任意学业记录序列 S：
- 令 c 为序列 S 最近 k 次考核中取得达标（1）的次数。
- 如果记录不足 k 次，则系统默认在早期用未达标（0）补齐至长度 k。
- 当前滚动学业综合评级为 f(S) = g(c)。

系统维护两条成绩序列：
1. 模拟学生档案 S_exp：初始为空，你可以向其中注入模拟的考核结果。
2. 官方基准成绩单 S_off：某毕业生的固化成绩序列，长度为 {N}，内容固定且可查询。

你可以通过以下交互来推导隐藏评估参数：

## 对模拟学生档案的操作与查询

- 录入达标成绩（1）：在 S_exp 末尾追加字符 1（达标）。
- 录入未达标成绩（0）：在 S_exp 末尾追加字符 0（未达标）。
- 重置学生档案：将 S_exp 清空（等效于最近 k 次全部为未达标 0）。
- 查询当前评级：查询当前 S_exp 的综合评级结果 f(S_exp)。

## 对官方基准成绩单的查询

- 查询基准成绩单：获取完整的基准成绩序列 S_off。
- 查询成绩单长度：获取基准成绩序列的总考核次数 N。

## 提交学业评估模型参数

当你收集足够信息后，需要提交三项内容：
1. 滚动考核窗口参数 k 的值
2. 完整的评级映射表 g（格式：g(0)=a0, g(1)=a1, ..., g(k)=ak）
3. 官方基准成绩单的最终综合评级结果

若三项全部正确，模型反推成功；任一项错误，反推失败。

## 询问与提交答案的格式（必须严格遵守）

每次只能发送一个指令或操作。请使用以下 XML 格式：

- 录入达标成绩（1）：
<append_one></append_one>

- 录入未达标成绩（0）：
<append_zero></append_zero>

- 重置学生档案：
<reset></reset>

- 查询当前评级：
<query_reading></query_reading>

- 查询基准成绩单：
<query_official></query_official>

- 查询成绩单长度：
<query_length></query_length>

- 提交最终报告（注意格式严格，用逗号和空格分隔）：
<answer>k=3, g=g(0)=2 g(1)=0 g(2)=1 g(3)=3, official_reading=2</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the sandbox environment of the "Dynamic Rolling Academic Assessment System".

The system embeds a hidden academic evaluation model (k, g), where:
- k is an unknown integer representing the rolling assessment window (number of recent tests/assignments), ranging from 2 to 6.
- g is an unknown comprehensive grading bijection that maps the set {0, 1, ..., k} (representing the number of passed tests in the window) to the grading tiers {0, 1, ..., k} (i.e., g is a permutation).

The system uses a binary alphabet {0, 1} to record a student's result for each assessment (0 for failed, 1 for passed). Define a comprehensive grading function f for any academic record sequence S:
- Let c be the count of passed assessments (1s) in the last k positions of sequence S.
- If the record length is less than k assessments, pad with failed results (0s) on the left to reach length k.
- The current rolling academic grade is f(S) = g(c).

The system maintains two score sequences:
1. Simulated Student Profile S_exp: initially empty, you can inject simulated assessment results into it.
2. Official Baseline Transcript S_off: a fixed score sequence of a graduate with length {N}, which can be queried.

You can deduce the hidden evaluation parameters through the following interactions:

## Operations and Queries on Simulated Profile

- Record Passed Assessment (1): append character 1 to the end of S_exp.
- Record Failed Assessment (0): append character 0 to the end of S_exp.
- Reset Profile: clear S_exp (equivalent to having the last k assessments all failed 0).
- Query Current Grade: query the current academic grade f(S_exp).

## Queries on Official Baseline Transcript

- Query Baseline Transcript: get the complete official baseline sequence S_off.
- Query Transcript Length: get the total number of assessments N in the baseline sequence.

## Submit Evaluation Model Parameters

When you have gathered enough information, submit three items:
1. The value of the assessment window parameter k
2. The complete mapping table of the grading function g (format: g(0)=a0, g(1)=a1, ..., g(k)=ak)
3. The final comprehensive grade of the official baseline transcript

If all three items are correct, the deduction succeeds; if any item is incorrect, it fails.

## Query and Answer Format (must strictly follow)

Each turn you can only make one query or operation. Use the following XML format:

- Record Passed Assessment (1):
<append_one></append_one>

- Record Failed Assessment (0):
<append_zero></append_zero>

- Reset Profile:
<reset></reset>

- Query Current Grade:
<query_reading></query_reading>

- Query Baseline Transcript:
<query_official></query_official>

- Query Transcript Length:
<query_length></query_length>

- Submit final parameters (note strict format, separated by commas and spaces):
<answer>k=3, g=g(0)=2 g(1)=0 g(2)=1 g(3)=3, official_reading=2</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎使用“工业生产线设备状态标定与质检分析”控制台。

系统内置了一个隐藏的设备状态模型 (k, g)，其中：
- k 为未知的质检采样窗口参数（表示最近检验的批次数），取值范围在 2 到 6 之间。
- g 为未知的标定状态函数，将集合 {0, 1, ..., k}（表示采样窗口内发现缺陷批次的数量）一一映射到设备维护代码 {0, 1, ..., k}（即 g 是一个排列）。

系统使用二值序列 {0, 1} 记录每批次产品的质检结果（0代表合格，1代表存在缺陷）。定义设备标定评估函数 f 作用于任意质检序列 S：
- 令 c 为序列 S 最近 k 个批次中存在缺陷（1）的次数。
- 如果质检记录不足 k 个批次，则系统默认在早期用合格（0）补齐至长度 k。
- 当前设备维护代码为 f(S) = g(c)。

系统维护两条质检序列：
1. 测试环境沙箱 S_exp：初始为空，你可以向其中注入模拟质检数据。
2. 生产线基准日志 S_off：某核心机台的固化生产日志，长度为 {N}，内容固定且可查询。

你可以通过以下交互来破解隐藏的标定参数：

## 对测试环境沙箱的操作与查询

- 注入缺陷批次（1）：在 S_exp 末尾追加字符 1（缺陷）。
- 注入合格批次（0）：在 S_exp 末尾追加字符 0（合格）。
- 重置测试沙箱：将 S_exp 清空（等效于最近 k 个批次全部为合格 0）。
- 查询当前维护代码：查询当前 S_exp 的标定评估结果 f(S_exp)。

## 对生产线基准日志的查询

- 查询基准日志：获取完整的基准质检序列 S_off。
- 查询日志长度：获取基准质检序列的总批次数 N。

## 提交设备状态模型参数

当你收集足够信息后，需要提交三项内容：
1. 质检采样窗口参数 k 的值
2. 完整的标定状态映射表 g（格式：g(0)=a0, g(1)=a1, ..., g(k)=ak）
3. 生产线基准日志最终指向的设备维护代码

若三项全部正确，模型破解成功；任一项错误，破解失败。

## 询问与提交答案的格式（必须严格遵守）

每次只能发送一个指令或操作。请使用以下 XML 格式：

- 注入缺陷批次（1）：
<append_one></append_one>

- 注入合格批次（0）：
<append_zero></append_zero>

- 重置测试沙箱：
<reset></reset>

- 查询当前维护代码：
<query_reading></query_reading>

- 查询基准日志：
<query_official></query_official>

- 查询日志长度：
<query_length></query_length>

- 提交最终报告（注意格式严格，用逗号和空格分隔）：
<answer>k=3, g=g(0)=2 g(1)=0 g(2)=1 g(3)=3, official_reading=2</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Industrial Production Line Equipment Calibration and QC Analysis" console.

The system incorporates a hidden equipment state model (k, g), where:
- k is an unknown integer representing the quality control sampling window (number of recent batches), ranging from 2 to 6.
- g is an unknown calibration state bijection that maps the set {0, 1, ..., k} (representing the number of defective batches in the sampling window) to equipment maintenance codes {0, 1, ..., k} (i.e., g is a permutation).

The system uses a binary alphabet {0, 1} to record the QC result of each product batch (0 for normal/qualified, 1 for defective). Define an equipment calibration evaluation function f for any QC sequence S:
- Let c be the count of defective batches (1s) in the last k positions of sequence S.
- If the QC record length is less than k batches, pad with normal statuses (0s) on the left to reach length k.
- The current equipment maintenance code is f(S) = g(c).

The system maintains two QC sequences:
1. Test Sandbox Sequence S_exp: initially empty, you can inject simulated QC data into it.
2. Production Baseline Log S_off: a fixed production log of a core machine with length {N}, which can be queried.

You can crack the hidden calibration parameters through the following interactions:

## Operations and Queries on Test Sandbox

- Inject Defective Batch (1): append character 1 to the end of S_exp.
- Inject Normal Batch (0): append character 0 to the end of S_exp.
- Reset Sandbox: clear S_exp (equivalent to having the last k batches all normal 0).
- Query Maintenance Code: query the current calibration evaluation result f(S_exp).

## Queries on Production Baseline Log

- Query Baseline Log: get the complete baseline QC sequence S_off.
- Query Log Length: get the total number of batches N in the baseline sequence.

## Submit Equipment State Model Parameters

When you have gathered enough information, submit three items:
1. The value of the QC sampling window parameter k
2. The complete mapping table of calibration state function g (format: g(0)=a0, g(1)=a1, ..., g(k)=ak)
3. The final equipment maintenance code derived from the production baseline log

If all three items are correct, the parameters are successfully cracked; if any item is incorrect, it fails.

## Query and Answer Format (must strictly follow)

Each turn you can only make one query or operation. Use the following XML format:

- Inject Defective Batch (1):
<append_one></append_one>

- Inject Normal Batch (0):
<append_zero></append_zero>

- Reset Sandbox:
<reset></reset>

- Query Maintenance Code:
<query_reading></query_reading>

- Query Baseline Log:
<query_official></query_official>

- Query Log Length:
<query_length></query_length>

- Submit final parameters (note strict format, separated by commas and spaces):
<answer>k=3, g=g(0)=2 g(1)=0 g(2)=1 g(3)=3, official_reading=2</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用“司法合规性动态审计与风险裁定系统”。

系统基于一套被封存的法律评估准则 (k, g) 运行，其中：
- k 为未知的法定追溯期参数（表示最近的审查事件数），取值范围在 2 到 6 之间。
- g 为未知的处罚等级映射函数，将集合 {0, 1, ..., k}（表示追溯期内发生的违规次数）一一映射到法律制裁等级 {0, 1, ..., k}（即 g 是一个排列）。

系统使用二值序列 {0, 1} 记录企业每次审查的合规情况（0代表合规，1代表违规）。定义法律风险裁定函数 f 作用于任意审查序列 S：
- 令 c 为序列 S 最近 k 次审查中出现违规（1）的次数。
- 如果历史记录不足 k 次，则系统默认在早期用合规（0）补齐至长度 k。
- 当前法律制裁等级为 f(S) = g(c)。

系统维护两条审查序列：
1. 判例模拟档案 S_exp：初始为空，你可以向其中录入假设的审查记录。
2. 官方司法档案 S_off：某历史企业的固化审查日志，长度为 {N}，内容固定且可查询。

你可以通过以下交互来反推隐藏的法律评估准则：

## 对判例模拟档案的操作与查询

- 录入违规记录（1）：在 S_exp 末尾追加字符 1（违规）。
- 录入合规记录（0）：在 S_exp 末尾追加字符 0（合规）。
- 重置模拟档案：将 S_exp 清空（等效于最近 k 次审查全部为合规 0）。
- 查询当前制裁等级：查询当前 S_exp 的裁定结果 f(S_exp)。

## 对官方司法档案的查询

- 查询司法档案：获取完整的司法审查序列 S_off。
- 查询档案长度：获取司法审查序列的总审查次数 N。

## 提交法律评估准则参数

当你收集足够信息后，需要提交三项内容：
1. 法定追溯期参数 k 的值
2. 完整的处罚等级映射表 g（格式：g(0)=a0, g(1)=a1, ..., g(k)=ak）
3. 官方司法档案最终判定面临的法律制裁等级

若三项全部正确，准则反推成功；任一项错误，反推失败。

## 询问与提交答案的格式（必须严格遵守）

每次只能发送一个指令或操作。请使用以下 XML 格式：

- 录入违规记录（1）：
<append_one></append_one>

- 录入合规记录（0）：
<append_zero></append_zero>

- 重置模拟档案：
<reset></reset>

- 查询当前制裁等级：
<query_reading></query_reading>

- 查询司法档案：
<query_official></query_official>

- 查询档案长度：
<query_length></query_length>

- 提交最终报告（注意格式严格，用逗号和空格分隔）：
<answer>k=3, g=g(0)=2 g(1)=0 g(2)=1 g(3)=3, official_reading=2</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Judicial Compliance Dynamic Auditing and Risk Adjudication System".

The system operates on a sealed legal assessment criteria model (k, g), where:
- k is an unknown integer representing the statutory limitation period (number of recent audits), ranging from 2 to 6.
- g is an unknown penalty severity bijection that maps the set {0, 1, ..., k} (representing the number of violations in the limitation period) to legal sanction levels {0, 1, ..., k} (i.e., g is a permutation).

The system uses a binary alphabet {0, 1} to record the compliance status of a corporate entity during each audit (0 for compliant, 1 for violation). Define a legal risk adjudication function f for any audit sequence S:
- Let c be the count of violations (1s) in the last k positions of sequence S.
- If the historical record is less than k audits, pad with compliant statuses (0s) on the left to reach length k.
- The current legal sanction level is f(S) = g(c).

The system maintains two audit sequences:
1. Precedent Simulator Archive S_exp: initially empty, you can log hypothetical audit records into it.
2. Official Judicial Archive S_off: a fixed audit log of a historical enterprise with length {N}, which can be queried.

You can deduce the hidden legal assessment criteria through the following interactions:

## Operations and Queries on Simulator Archive

- Log Violation (1): append character 1 to the end of S_exp.
- Log Compliant Audit (0): append character 0 to the end of S_exp.
- Reset Simulator: clear S_exp (equivalent to having the last k audits all compliant 0).
- Query Sanction Level: query the current adjudication result f(S_exp).

## Queries on Official Judicial Archive

- Query Judicial Archive: get the complete official audit sequence S_off.
- Query Archive Length: get the total number of audits N in the judicial archive.

## Submit Legal Assessment Criteria

When you have gathered enough information, submit three items:
1. The value of the statutory limitation period k
2. The complete mapping table of the penalty severity function g (format: g(0)=a0, g(1)=a1, ..., g(k)=ak)
3. The final legal sanction level determined for the official judicial archive

If all three items are correct, the deduction succeeds; if any item is incorrect, it fails.

## Query and Answer Format (must strictly follow)

Each turn you can only make one query or operation. Use the following XML format:

- Log Violation (1):
<append_one></append_one>

- Log Compliant Audit (0):
<append_zero></append_zero>

- Reset Simulator:
<reset></reset>

- Query Sanction Level:
<query_reading></query_reading>

- Query Judicial Archive:
<query_official></query_official>

- Query Archive Length:
<query_length></query_length>

- Submit final criteria (note strict format, separated by commas and spaces):
<answer>k=3, g=g(0)=2 g(1)=0 g(2)=1 g(3)=3, official_reading=2</answer>
"""

    tags = ["answer", "append_one", "append_zero", "reset", "query_reading", 
            "query_official", "query_length"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "k": 2,
                "g_map": {0: 1, 1: 2, 2: 0},
                "official_seq": "10110",
                "N": 5,
            },
            2: {
                "k": 3,
                "g_map": {0: 2, 1: 3, 2: 0, 3: 1},
                "official_seq": "11010101",
                "N": 8,
            },
            3: {
                "k": 4,
                "g_map": {0: 3, 1: 1, 2: 4, 3: 0, 4: 2},
                "official_seq": "110101101011",
                "N": 12,
            },
            4: {
                "k": 5,
                "g_map": {0: 4, 1: 2, 2: 5, 3: 1, 4: 3, 5: 0},
                "official_seq": "111010110100101",
                "N": 15,
            },
            5: {
                "k": 6,
                "g_map": {0: 5, 1: 3, 2: 1, 3: 6, 4: 2, 5: 4, 6: 0},
                "official_seq": "11101011010010110101",
                "N": 20,
            },
        },
        "en": {
            1: {
                "k": 2,
                "g_map": {0: 1, 1: 2, 2: 0},
                "official_seq": "10110",
                "N": 5,
            },
            2: {
                "k": 3,
                "g_map": {0: 2, 1: 3, 2: 0, 3: 1},
                "official_seq": "11010101",
                "N": 8,
            },
            3: {
                "k": 4,
                "g_map": {0: 3, 1: 1, 2: 4, 3: 0, 4: 2},
                "official_seq": "110101101011",
                "N": 12,
            },
            4: {
                "k": 5,
                "g_map": {0: 4, 1: 2, 2: 5, 3: 1, 4: 3, 5: 0},
                "official_seq": "111010110100101",
                "N": 15,
            },
            5: {
                "k": 6,
                "g_map": {0: 5, 1: 3, 2: 1, 3: 6, 4: 2, 5: 4, 6: 0},
                "official_seq": "11101011010010110101",
                "N": 20,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏参数"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 设置隐藏参数
        self.k = cfg["k"]
        self.g_map = cfg["g_map"]
        self.official_seq = cfg["official_seq"]
        self.N = cfg["N"]
        
        # 初始化实验序列
        self.exp_seq = ""
        
        # 计算官方序列的最终读数（Ground Truth）
        self.official_reading = self._compute_reading(self.official_seq)
        
        # 用于游戏规则显示
        self._game_info["N"] = self.N

    def _compute_reading(self, seq):
        """计算序列的读数值"""
        # 获取最后 k 位
        if len(seq) < self.k:
            # 左侧补0
            padded = "0" * (self.k - len(seq)) + seq
        else:
            padded = seq[-self.k:]
        
        # 统计1的个数
        count_ones = padded.count("1")
        
        # 返回 g(count_ones)
        return self.g_map[count_ones]

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        try:
            raw_ans = parsed_info["answer"]
            
            # 解析答案：k=X, g=..., official_reading=Y
            parts = raw_ans.split(",")
            ans_dict = {}
            
            for part in parts:
                part = part.strip()
                if part.startswith("k="):
                    ans_dict["k"] = int(part[2:].strip())
                elif part.startswith("g="):
                    ans_dict["g"] = part[2:].strip()
                elif part.startswith("official_reading="):
                    ans_dict["official_reading"] = int(part.split("=")[1].strip())
            
            # 检查是否包含所有必需字段
            if "k" not in ans_dict or "g" not in ans_dict or "official_reading" not in ans_dict:
                return False
            
            # 1. 检查 k 值
            if ans_dict["k"] != self.k:
                return False
            
            # 2. 检查 g 映射表
            # 解析 g 的格式：g(0)=a0 g(1)=a1 ...
            g_str = ans_dict["g"]
            g_entries = g_str.split()
            parsed_g = {}
            
            for entry in g_entries:
                if "=" not in entry:
                    continue
                # 格式：g(i)=val
                left, right = entry.split("=")
                if not left.startswith("g(") or not left.endswith(")"):
                    continue
                idx = int(left[2:-1])
                val = int(right)
                parsed_g[idx] = val
            
            # 检查 g 是否完整且正确
            if len(parsed_g) != self.k + 1:
                return False
            
            for i in range(self.k + 1):
                if i not in parsed_g or parsed_g[i] != self.g_map[i]:
                    return False
            
            # 3. 检查官方序列读数
            if ans_dict["official_reading"] != self.official_reading:
                return False
            
            return True
            
        except Exception as e:
            return False

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        包含足够的实验操作来推断 k 和 g 的完整映射。
        """
        results = []

        # 1. 查询官方序列
        results.append({
            "query": "<query_official></query_official>",
            "answer": self.official_seq
        })

        # 2. 查询官方长度
        results.append({
            "query": "<query_length></query_length>",
            "answer": str(self.N)
        })

        # 3. 通过系统性实验推断 k 和 g
        # 策略：先 reset，然后逐步 append 1 并查询读数
        # 这样可以在 k 未知时，通过观察读数变化推断 k 和 g

        # 保存并隔离实验状态
        saved_exp_seq = self.exp_seq

        # Reset
        self.exp_seq = ""
        results.append({
            "query": "<reset></reset>",
            "answer": "OK" if self.config.language == "en" else "操作成功"
        })

        # 查询空序列读数 -> g(0)
        reading = self._compute_reading(self.exp_seq)
        results.append({
            "query": "<query_reading></query_reading>",
            "answer": str(reading)
        })

        # 逐步 append 1，每次查询读数
        # 最多追加 6 次（k 最大为 6）以覆盖所有可能
        for i in range(6):
            self.exp_seq += "1"
            results.append({
                "query": "<append_one></append_one>",
                "answer": "OK" if self.config.language == "en" else "操作成功"
            })
            reading = self._compute_reading(self.exp_seq)
            results.append({
                "query": "<query_reading></query_reading>",
                "answer": str(reading)
            })

        # 再 reset 并追加 0 来验证 k（追加 0 不改变 count，但推进窗口）
        self.exp_seq = ""
        results.append({
            "query": "<reset></reset>",
            "answer": "OK" if self.config.language == "en" else "操作成功"
        })

        # 追加 k+1 个 1 再追加一个 0，观察窗口滑动效果
        for i in range(3):
            self.exp_seq += "1"
            results.append({
                "query": "<append_one></append_one>",
                "answer": "OK" if self.config.language == "en" else "操作成功"
            })
        
        self.exp_seq += "0"
        results.append({
            "query": "<append_zero></append_zero>",
            "answer": "OK" if self.config.language == "en" else "操作成功"
        })

        reading = self._compute_reading(self.exp_seq)
        results.append({
            "query": "<query_reading></query_reading>",
            "answer": str(reading)
        })

        # 恢复实验序列状态
        self.exp_seq = saved_exp_seq

        return results

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            ok_msg = "操作成功"
        else:
            ok_msg = "OK"
        
        # 按优先级处理操作和查询
        if "append_one" in parsed_info:
            self.exp_seq += "1"
            return ok_msg
        
        elif "append_zero" in parsed_info:
            self.exp_seq += "0"
            return ok_msg
        
        elif "reset" in parsed_info:
            self.exp_seq = ""
            return ok_msg
        
        elif "query_reading" in parsed_info:
            reading = self._compute_reading(self.exp_seq)
            return str(reading)
        
        elif "query_official" in parsed_info:
            return self.official_seq
        
        elif "query_length" in parsed_info:
            return str(self.N)
        
        else:
            raise ValueError("No valid query or operation tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        # 若 correct 是纯数字且长度较短（表示读数值），做+1处理
        if correct.isdigit() and len(correct) <= 2:
            val = int(correct)
            # 确保产生不同的值
            return str(val + 1)
        
        # 若是二进制序列字符串（如官方序列），翻转第一个bit
        if all(c in '01' for c in correct) and len(correct) > 0:
            flipped = '0' if correct[0] == '1' else '1'
            return flipped + correct[1:]
        
        # 中文环境关键词替换
        if self.config.language == "zh":
            if "成功" in correct:
                return correct.replace("成功", "失败")
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        
        # 英文环境关键词替换
        lower_correct = correct.lower()
        if "ok" in lower_correct:
            return "ERROR"
        if "yes" in lower_correct:
            return correct.replace("Yes", "No").replace("yes", "no").replace("YES", "NO")
        elif "no" in lower_correct:
            return correct.replace("No", "Yes").replace("no", "yes").replace("NO", "YES")

        return correct + "_WRONG"