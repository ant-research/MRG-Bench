# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   后缀统计：序列后k个元素的某统计特征是什么
# ============================================================

from .base import Game
import re

class SequenceFunctionGame(Game):

    game_rule_zh = """\
我们来玩一个"序列函数推理"游戏，规则如下：

游戏设定了一个初始为空的序列，每个元素取自 {{0, 1, 2}}。你可以逐步在序列末尾追加元素，序列最大长度为 12。

我已秘密选定了一个函数 f，它的输入是序列的"后 4 位窗口"（若当前长度不足 4，则在左侧用 0 填充至 4 位），输出为 {{0, 1, 2}} 中的一个数值。这个函数在整个游戏过程中保持不变，且来自以下四个候选之一：

- 律A：后 4 位元素之和对 3 取模
- 律B：后 4 位的加权和对 3 取模，权重从旧到新依次为 [1, 2, 1, 2]
- 律C：后 4 位中最新一位的数值
- 律D：后 4 位中出现次数最多的数值；若有并列，则选最近一次出现位置更靠后的数值

你的目标是：
1. 推断出正确的函数（律A/律B/律C/律D）
2. 在序列长度达到 12 时，使得函数在最终后 4 位窗口上的输出等于 {target}

你可以反复进行以下操作（每次仅限一个操作）：

1. 投掷操作：向序列末尾追加一个元素（0、1 或 2）。系统返回当前序列长度。
2. 听回声：查询函数在当前后 4 位窗口上的输出值。系统返回 0、1 或 2。
3. 查询长度：询问当前序列长度及剩余可追加次数。系统返回相关信息。
4. 提交结论：提交你推断的函数类型。系统判定正确性；若此时长度已达 12，同时判定终局目标是否达成。

当序列长度达到 12 时，游戏进入终局判定。你需要同时满足：
- 提交的函数类型正确
- 函数在最终后 4 位窗口的输出等于 {target}

## 操作格式（必须严格遵守）

每次操作只能包含一个标签。请使用以下 XML 格式：

- 投掷操作（例如追加元素 1）：
<throw>1</throw>

- 听回声：
<echo></echo>

- 查询长度：
<query_length></query_length>

- 提交结论（例如判断为律C）：
<answer>C</answer>

注意：请尽可能少地使用操作次数来完成推理和目标。
"""

    game_rule_en = """\
Let's play a "Sequence Function Deduction" game. Here are the rules:

There is an initially empty sequence where each element is from {{0, 1, 2}}. You can append elements to the end of the sequence step by step, with a maximum length of 12.

I have secretly selected a function f that takes the "last 4 positions window" of the sequence as input (if the current length is less than 4, pad with 0s on the left to make it 4 positions) and outputs a value from {{0, 1, 2}}. This function remains constant throughout the game and is one of the following four candidates:

- Rule A: Sum of the last 4 elements modulo 3
- Rule B: Weighted sum of the last 4 elements modulo 3, with weights [1, 2, 1, 2] from oldest to newest
- Rule C: The value of the newest element in the last 4 positions
- Rule D: The most frequent value in the last 4 positions; if tied, choose the one with the most recent occurrence

Your goals are:
1. Deduce the correct function (Rule A/B/C/D)
2. When the sequence length reaches 12, ensure the function's output on the final last 4 positions equals {target}

You can repeatedly perform the following operations (one per turn):

1. Throw: Append an element (0, 1, or 2) to the end of the sequence. The system returns the current sequence length.
2. Echo: Query the function's output on the current last 4 positions window. The system returns 0, 1, or 2.
3. Query Length: Ask for the current sequence length and remaining append operations. The system returns relevant information.
4. Submit Answer: Submit your deduced function type. The system judges correctness; if the length has reached 12, it also judges whether the end goal is achieved.

When the sequence length reaches 12, the game enters final judgment. You need to satisfy both:
- The submitted function type is correct
- The function's output on the final last 4 positions equals {target}

## Operation Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Throw operation (e.g., appending element 1):
<throw>1</throw>

- Echo:
<echo></echo>

- Query length:
<query_length></query_length>

- Submit answer (e.g., deducing Rule C):
<answer>C</answer>

Note: Try to use as few operations as possible to complete the deduction and achieve the goal.
"""

    # 场景1：交通
    contextualized_rule_zh_1 = """\
欢迎进入“智控交管系统”演练平台。本平台用于推演不同路段的交通演变规律并预测流量负荷。
目前分配给你一个未定初始状态的监测路段，你可以逐步录入历史时段交通状态代码（可选代码：0=畅通，1=缓行，2=拥堵），最多可建立包含 12 个时段的演进序列。

系统搭载了一个核心的“拥堵预测引擎” f，其输入为最近 4 个时段的状态序列（不足 4 位则在历史侧用代码 0 填充），输出为 {{0, 1, 2}} 预警负荷等级之一。该引擎的评估法则在全程保持不变，且必然是以下四种预设算法之一：

- 律A：近 4 个状态代码之和对 3 取模。
- 律B：近 4 个状态代码的加权和对 3 取模，从旧到新权重依次为 [1, 2, 1, 2]。
- 律C：完全取决于最新一个时段的交通状态代码。
- 律D：近 4 个状态中出现频次最高的代码；若频次并列，则取时间上最近发生的一个。

你的任务目标：
1. 分析并推断出当前后台运作的正确引擎算法（律A/律B/律C/律D）。
2. 在录入总时段达到 12 个时，使得引擎对最后 4 位窗口的负荷预测值严格等于 {target}。

你可以反复执行以下控制端指令（每次仅限一个）：

1. 录入记录：向序列追加一个状态代码（0、1或2），系统返回当前已建立总时段数。
2. 运行引擎：读取预测引擎基于当前末尾 4 位给出的负荷预估值，系统返回0、1或2。
3. 进度核查：查询序列当前长度与剩余操作配额。
4. 提交报告：提交你推断的算法型号，若此时总时段已达 12，系统将一并核对终局负荷目标。

当序列长度达到 12 时，演练自动结算，你必须同时达成：
- 提交的引擎型号正确。
- 最终后 4 位窗口的预测负荷等于 {target}。

## 操作格式（必须严格遵守以下XML规范）

- 录入记录（例如追加状态 1）：
<throw>1</throw>

- 运行引擎：
<echo></echo>

- 进度核查：
<query_length></query_length>

- 提交报告（例如认定为律C）：
<answer>C</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Intelligent Traffic Control System" drill platform. This platform simulates traffic progression and predicts flow load patterns.
You are assigned a monitoring segment with an initially empty sequence. You can iteratively log historical traffic status codes (0=Clear, 1=Slow, 2=Congested), building an evolution sequence up to 12 periods.

The system is equipped with a core "Congestion Prediction Engine" f, which takes the sequence's last 4 periods as input (padded with 0s on the older side if under 4) and outputs an alert load level from {{0, 1, 2}}. Its evaluation algorithm remains constant and operates strictly under one of four predetermined models:

- Rule A: Sum of the last 4 status codes modulo 3.
- Rule B: Weighted sum of the last 4 status codes modulo 3, with historical weights [1, 2, 1, 2] from oldest to newest.
- Rule C: Completely dependent on the traffic status code of the most recent period.
- Rule D: The most frequent status code in the last 4 periods; if tied, it defaults to the most recent occurrence.

Your objectives:
1. Deduce the correct background engine algorithm (Rule A/B/C/D).
2. Ensure that when the total logged periods reach 12, the engine's predicted load on the final 4-period window exactly equals {target}.

You can repeatedly execute the following terminal directives (one per operation):

1. Log Record: Append a status code (0, 1, or 2). System returns the current sequence length.
2. Run Engine: Query the load prediction based on the current 4-period window. System returns 0, 1, or 2.
3. Check Progress: Query current sequence length and remaining quota.
4. Submit Report: Submit your deduced algorithm model. If the sequence length is exactly 12, the final target objective is also evaluated.

At sequence length 12, the drill concludes. You must ensure:
- The submitted algorithm model is correct.
- The predicted load on the final 4-period window equals {target}.

## Operation Format (Strictly XML)

- Log Record (e.g., logging status 1):
<throw>1</throw>

- Run Engine:
<echo></echo>

- Check Progress:
<query_length></query_length>

- Submit Report (e.g., deducing Rule C):
<answer>C</answer>
"""

    # 场景2：医疗
    contextualized_rule_zh_2 = """\
欢迎进入“ICU生命体征监护系统”调参测试环境。
本系统负责长效跟踪患者体征序列并自动触发医疗预警。目前序列为空，你需要逐个周期录入患者生命体征综合评估代码（0=正常，1=轻微波动，2=警报），最多录入 12 个监控周期。

系统核心的“健康风险预警机制” f 依赖患者最近 4 个周期的体征序列（不足 4 期则往前补测算基线 0），并输出 {{0, 1, 2}} 预警动作等级之一。该机制的触发逻辑全程固定，必定为以下四类之一：

- 律A：近 4 个周期体征代码之和对 3 取模。
- 律B：近 4 个周期代码的加权和对 3 取模，早晚期权重依次为 [1, 2, 1, 2]。
- 律C：完全以最新一期体征评估代码为准。
- 律D：近 4 期中最常出现的体征代码；若存在并列，则采信距离当前最近的一期记录。

你的任务目标：
1. 诊断出该监护仪启用的正确预警机制（律A/律B/律C/律D）。
2. 在监控周期达到满额 12 期时，使该预警机制对最后 4 期的评估输出正好等于预设值 {target}。

测试阶段支持以下操作（每次独立调取）：

1. 录入体征：向系统追加一个周期评估代码（0、1或2），系统返回当前建档的周期数。
2. 试运行机制：获取当前 4 期体征窗口的风险预警计算结果，返回0、1或2。
3. 查验周期：问询建档进度及可供修改录入的余量。
4. 提交诊断：确认你的判定逻辑型号，若周期已达 12，系统将核对整体临床处置是否达标。

录满 12 个周期时测试结束，需同步满足：
- 机制研判正确。
- 最终 4 期数据的预警输出精确等于 {target}。

## 交互格式要求（遵循系统接口规范）

- 录入体征（例如录入1）：
<throw>1</throw>

- 试运行机制：
<echo></echo>

- 查验周期：
<query_length></query_length>

- 提交诊断（例如指定机制C）：
<answer>C</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the parameter tuning environment of the "ICU Vital Signs Monitoring System."
This system tracks patient vital sequences to trigger medical warnings. Starting with an empty sequence, you will log patient composite vital sign codes period by period (0=Normal, 1=Mild Fluctuation, 2=Alert), up to 12 monitoring periods.

The core "Health Risk Warning Mechanism" f processes the latest 4 periods of vital data (padded with baseline 0s if fewer than 4) to output an alert action level from {{0, 1, 2}}. The mechanism logic is strictly fixed throughout the test and is definitively one of the following four:

- Rule A: Sum of the last 4 period codes modulo 3.
- Rule B: Weighted sum of the last 4 codes modulo 3, with early-to-late weights [1, 2, 1, 2].
- Rule C: Driven entirely by the vital code of the most recent period.
- Rule D: The most frequently occurring code in the last 4 periods; if tied, the most recent record takes precedence.

Your objectives:
1. Diagnose the correct warning mechanism active on the monitor (Rule A/B/C/D).
2. When the monitoring sequence reaches exactly 12 periods, ensure the mechanism's assessment of the final 4-period window equals the target value {target}.

The test phase supports the following actions (one per call):

1. Log Vitals: Append a period code (0, 1, or 2), returning the current total logged periods.
2. Trial Mechanism: Obtain the current computed risk warning level for the 4-period window (returns 0, 1, or 2).
3. Check Periods: Query the charting progress and remaining capacity.
4. Submit Diagnosis: Confirm your determined mechanism model. If periods reach 12, overall clinical handling goals will be evaluated.

At 12 periods, the test concludes. You must achieve both:
- Correct mechanism diagnosis.
- The final 4-period warning output precisely matches {target}.

## Interface Format Requirements

- Log Vitals (e.g., logging 1):
<throw>1</throw>

- Trial Mechanism:
<echo></echo>

- Check Periods:
<query_length></query_length>

- Submit Diagnosis (e.g., declaring Rule C):
<answer>C</answer>
"""

    # 场景3：教育
    contextualized_rule_zh_3 = """\
欢迎使用“自适应学习行为分析器”干预配置后台。
本模块专门针对学生学习过程中的阶段专注度建立考察序列。当前序列留空，你需要按教学切片分步录入学生状态代码（0=走神，1=一般，2=高度集中），完整跟踪档案的最大深度为 12 个节点。

系统后台运作着一个“学情干预评估器” f，它提取序列最新 4 个切片（节点不足则在前端默认以 0 补齐）进行测算，并输出 {{0, 1, 2}} 中一种干预触发级别。测算模型一经设定不再变动，包含以下四种基准框架：

- 律A：最新 4 个状态代码加总并对 3 取模。
- 律B：最新 4 个状态代码的加权计算并对 3 取模，按时间轴赋予权重 [1, 2, 1, 2]。
- 律C：评估完全对应距离当前最近切片的状态代码。
- 律D：最新 4 个状态里出现频次居首的代码；若遇并列，采纳时间离现在更近的反馈。

你的任务目标：
1. 鉴定当前所采用的干预测算模型（律A/律B/律C/律D）。
2. 在切片记录数累积到 12 步时，调控录入节奏使最后 4 位窗口的干预触发级别准确等于 {target}。

你可以实施下列配置指令（每次单发指令）：

1. 追加记录：录入一个切片代码（0、1或2），接口回复当前录入的总节点数。
2. 请求测算：拉取评估器针对当前 4 位序列的试算结果，回复0、1或2。
3. 状态检视：查看已记录切片进度及剩余节点数。
4. 交付校验：递交你对模型的分析结论。到达 12 个节点时同步检查干预引导目标是否吻合。

累计录入达到 12 切片时锁定评估，需双线达标：
- 递交模型判断准确。
- 结案时后 4 位输出触发值等同 {target}。

## 规范指令报文格式

- 追加记录（示例：录入状态1）：
<throw>1</throw>

- 请求测算：
<echo></echo>

- 状态检视：
<query_length></query_length>

- 交付校验（示例：判定为律C）：
<answer>C</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the backend configuration for the "Adaptive Learning Behavior Analyzer."
This module builds an observational sequence of student focus levels across learning stages. Starting with an empty sequence, you log stage status codes sequentially (0=Distracted, 1=Normal, 2=Highly Focused), with the complete tracking profile capped at 12 nodes.

A background "Learning Intervention Evaluator" f processes the newest 4 sequence slices (padding the front with 0s if insufficient) to calculate an intervention trigger level from {{0, 1, 2}}. The evaluation model is fixed upon initiation and relies on one of four baseline frameworks:

- Rule A: Sum of the newest 4 status codes modulo 3.
- Rule B: Weighted sum of the newest 4 codes modulo 3, with timeline weights assigned as [1, 2, 1, 2].
- Rule C: The evaluation directly mirrors the status code of the most recent slice.
- Rule D: The most frequently observed code in the newest 4 slices; if tied, it adopts the more recent feedback.

Your objectives:
1. Identify the active intervention evaluation model (Rule A/B/C/D).
2. Through your logging sequence, ensure that at the 12th node, the calculated intervention trigger on the final 4-slice window exactly equals {target}.

You may issue the following configuration commands (single command per turn):

1. Append Record: Log a slice code (0, 1, or 2). The interface returns the total logged nodes.
2. Request Calculation: Pull the evaluator's trial result for the current 4-slice sequence, returning 0, 1, or 2.
3. Check Status: View recorded progress and remaining node allowance.
4. Deliver Verification: Submit your analytical conclusion of the model. When 12 nodes are reached, the final intervention goal is assessed.

Locking evaluation occurs at 12 logged slices. You must ensure:
- The submitted model judgment is correct.
- The final 4-slice trigger output matches {target}.

## Standardized Command Formats

- Append Record (e.g., logging status 1):
<throw>1</throw>

- Request Calculation:
<echo></echo>

- Check Status:
<query_length></query_length>

- Deliver Verification (e.g., assessing Rule C):
<answer>C</answer>
"""

    # 场景4：制造业/工业
    contextualized_rule_zh_4 = """\
欢迎登录“智能高精产线质检”控制终端。
你的任务是对流水线抽检批次进行记录和算法逆推。你需逐个批次登记初筛品质等级代码（0=合格，1=次品，2=废品）以形成质检序列，系统最多接受 12 个批次的检测流。

终端内核集成了“产线停机复检算法” f，它持续监控最近 4 批的抽检序列（遇长度不足则在序列头端填 0 补偿），并抛出 {{0, 1, 2}} 以指导下一环节的操作定级。该算法版本已锁定不变，属于以下四大检控逻辑之一：

- 律A：近 4 个批次品质代码之和对 3 取模。
- 律B：近 4 个代码的加权叠加并对 3 取模，从先至后权值为 [1, 2, 1, 2]。
- 律C：检控等级严格对齐最新一批的品质代码。
- 律D：近 4 批中出现频次最高的品质代码；倘若并列，则以刚完成检验的那批为准。

你的任务目标：
1. 鉴定目前在线服役的检控逻辑类别（律A/律B/律C/律D）。
2. 在总送检批次达到上限 12 时，使得最终 4 批组成的窗口能触发目标定级值 {target}。

测试面板可用指令（一次单一调用）：

1. 登记代码：将单个品质代码（0、1或2）录入流转线，获取当前登记的批次数。
2. 试算定级：调取目前最近 4 批的检控反馈预估，返回0、1或2。
3. 容量盘查：核对已有检控序列长度和产线可操作额度。
4. 归档结论：递交检控逻辑判定，若登记满 12 批则立刻核销最终目标控制的准确率。

累计达 12 个批次进入清算验收，要求必须做到：
- 逻辑判定选项正确。
- 末端 4 位检测窗的预估定级锁定为 {target}。

## 终端调用报文（严格遵循标记语言）

- 登记代码（例：录入次品1）：
<throw>1</throw>

- 试算定级：
<echo></echo>

- 容量盘查：
<query_length></query_length>

- 归档结论（例：鉴别为律C）：
<answer>C</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Smart High-Precision Line QC" control terminal.
Your task is to record sampling batches and reverse-engineer the automated algorithms. You will register preliminary quality codes batch by batch (0=Pass, 1=Defective, 2=Scrap) to form a quality control sequence, capping at 12 testing batches.

The terminal core runs the "Line Downtime Inspection Algorithm" f, which constantly monitors the latest 4-batch sequence (padding the start with 0s if short) to output an operational rating from {{0, 1, 2}} for downstream handling. This algorithm version is permanently locked and strictly follows one of four logics:

- Rule A: Sum of the last 4 batch quality codes modulo 3.
- Rule B: Weighted superposition of the last 4 codes modulo 3, with early-to-late weights [1, 2, 1, 2].
- Rule C: The operational rating strictly aligns with the quality code of the newest batch.
- Rule D: The most frequently occurring quality code in the last 4 batches; if tied, defaults to the most recently inspected batch.

Your objectives:
1. Identify the active inspection logic category on the line (Rule A/B/C/D).
2. Manage your entries so that when the submitted batches max out at 12, the final 4-batch window triggers the target operational rating {target}.

Available test panel commands (one call at a time):

1. Register Code: Feed a quality code (0, 1, or 2) into the line and receive the current registered batch count.
2. Trial Rating: Extract the algorithm's anticipated rating for the current 4-batch window, returning 0, 1, or 2.
3. Capacity Check: Audit the existing sequence length and available operational quota.
4. Archive Conclusion: Submit your logic deduction. Upon reaching 12 batches, the final operational target accuracy is instantly validated.

Auditing commences once 12 batches accumulate, requiring that:
- The logic deduction is correct.
- The trial rating for the terminal 4-position window locks at {target}.

## Terminal Call Tags (Strictly Markup Language)

- Register Code (e.g., registering Defective 1):
<throw>1</throw>

- Trial Rating:
<echo></echo>

- Capacity Check:
<query_length></query_length>

- Archive Conclusion (e.g., identifying Rule C):
<answer>C</answer>
"""

    # 场景5：法律
    contextualized_rule_zh_5 = """\
欢迎使用“司法量刑辅助决策系统”逻辑比弹沙盒。
本工具旨在梳理违法当事人的历史卷宗，模拟前科记录的复合权重。你可以在案卷序列中逐步增设记录代码（0=无异议，1=轻微违规，2=严重违法），卷宗最大允许溯及 12 宗。

在系统暗箱中设有一个“法定量刑从重基准”测算程式 f，它抓取案卷列表中最近 4 宗记录（如履历不足 4 宗，则用代表无罪的 0 补位至四件），并给出一个量刑调整指数，其值落于 {{0, 1, 2}}。此程式的测算基准不可变更，且必定吻合以下四个量刑法则之一：

- 律A：近 4 宗记录代码加总并对 3 取模。
- 律B：近 4 宗记录代码依时间做加权计和并对 3 取模，早晚权重系数为 [1, 2, 1, 2]。
- 律C：完全以最近发生的那一宗案卷违法等级为裁量准绳。
- 律D：近 4 宗记录里最常出现的前科代码；在同等频次下，按距离目前最近的一次事实为准。

你的任务目标：
1. 从反馈中剖析出沙盒当下引用的法则类型（律A/律B/律C/律D）。
2. 在卷宗记录恰好积攒至 12 宗时，引导测算程式在末尾 4 宗数据下的量刑调整指数稳稳命中目标 {target}。

你可以执行以下调查指令（单次提交一条指令）：

1. 录入卷宗：在末尾追加新的记录代码（0、1或2），获取总在案宗数。
2. 试算法理：向程式索要基于最新 4 宗案卷的量刑调整指数，获取到0、1或2。
3. 盘查卷宗号：检索当前记录长度以及还可添加的案卷条数。
4. 归档起诉书：敲定你推测的测算法则类别，当序列长度满 12 时，交由最终裁判进行核验。

序列积满 12 宗便进入结案审查阶段，你必须两全其美：
- 提交的法则断案无误。
- 最终 4 宗案卷对应的测算指数恰好符合要求：{target}。

## 程序指令包规范（必须使用XML格式套件）

- 录入卷宗（例：新增案卷1）：
<throw>1</throw>

- 试算法理：
<echo></echo>

- 盘查卷宗号：
<query_length></query_length>

- 归档起诉书（例：判明为律C）：
<answer>C</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the logic alignment sandbox of the "Judicial Sentencing Auxiliary Decision System."
This tool organizes an offender's historical case files to simulate the compounded weight of prior records. You incrementally append record codes into the case sequence (0=No Objection, 1=Minor Violation, 2=Serious Offense), with the dossier retrospectively capped at 12 items.

Operating in the background is a "Statutory Sentencing Aggravation Baseline" program f, which extracts the 4 most recent records (padding with 0s for 'innocence' if under 4 cases) to output a sentencing adjustment index valued in {{0, 1, 2}}. This baseline calculation is immutable and adheres exactly to one of four sentencing rules:

- Rule A: Sum of the newest 4 record codes modulo 3.
- Rule B: Chronologically weighted sum of the newest 4 codes modulo 3, with early-to-late weight factors [1, 2, 1, 2].
- Rule C: Sentenced strictly on the violation severity of the most recent individual case.
- Rule D: The most habitual prior record code in the newest 4 cases; upon frequency tie, the temporally nearest factual offense prevails.

Your objectives:
1. Deduce from the feedback which rule type the sandbox is presently referencing (Rule A/B/C/D).
2. As the dossier accumulates exactly to 12 records, steer the calculation program to hit the definitive target index {target} across the terminal 4-case span.

You may execute these investigative directives (one per submission):

1. Enter File: Append a new record code (0, 1, or 2) to the end, receiving the total cataloged cases.
2. Trial Jurisprudence: Request the sentencing adjustment index from the program based on the current 4-case window, retrieving 0, 1, or 2.
3. Check Docket: Retrieve the current sequence tally and remaining case entry quota.
4. Archive Indictment: Confirm your presumed calculation rule category. When the length reaches 12, it is submitted for the ultimate adjudicative review.

At a full 12 cases, case closure review activates, requiring dual success:
- Accurate rule deduction submitted.
- The adjustment index for the final 4 cases exactly fulfills the mandate: {target}.

## Routine Command Syntax (Mandatory XML formatting)

- Enter File (e.g., adding file 1):
<throw>1</throw>

- Trial Jurisprudence:
<echo></echo>

- Check Docket:
<query_length></query_length>

- Archive Indictment (e.g., establishing Rule C):
<answer>C</answer>
"""

    tags = ["answer", "throw", "echo", "query_length"]
    
    reasoning_type = "溯因推理"
    data_structure = "序列"

    # 难度配置：
    # 1 (简单)       - 律C (最简单的规则)，目标值 2
    # 2 (中等偏下)   - 律A (求和模3)，目标值 2
    # 3 (中等偏上)   - 律B (加权和模3)，目标值 1
    # 4 (较难)       - 律D (最频繁值)，目标值 0
    # 5 (难)         - 律D (最频繁值)，目标值 2

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "rule_type": "C",
                "target": 2,
            },
            2: {
                "rule_type": "A",
                "target": 2,
            },
            3: {
                "rule_type": "B",
                "target": 1,
            },
            4: {
                "rule_type": "D",
                "target": 0,
            },
            5: {
                "rule_type": "D",
                "target": 2,
            },
        },
        "en": {
            1: {
                "rule_type": "C",
                "target": 2,
            },
            2: {
                "rule_type": "A",
                "target": 2,
            },
            3: {
                "rule_type": "B",
                "target": 1,
            },
            4: {
                "rule_type": "D",
                "target": 0,
            },
            5: {
                "rule_type": "D",
                "target": 2,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏状态"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 游戏核心参数
        self.max_length = 12
        self.window_size = 4
        self.rule_type = cfg["rule_type"]
        self.target_value = cfg["target"]
        
        # 存储到 _game_info 用于格式化规则文本
        self._game_info["target"] = self.target_value
        
        # 当前序列状态
        self.sequence = []
        
        # 是否已提交答案
        self.submitted_rule = None

    def _get_window(self):
        """获取当前的后4位窗口，不足4位时左侧补0"""
        if len(self.sequence) >= self.window_size:
            return self.sequence[-self.window_size:]
        else:
            padding = [0] * (self.window_size - len(self.sequence))
            return padding + self.sequence

    def _compute_function(self, window):
        """根据真实的规则类型计算函数输出"""
        if self.rule_type == "A":
            # 律A：后4位元素之和对3取模
            return sum(window) % 3
        elif self.rule_type == "B":
            # 律B：加权和对3取模，权重 [1,2,1,2]
            weights = [1, 2, 1, 2]
            weighted_sum = sum(w * v for w, v in zip(weights, window))
            return weighted_sum % 3
        elif self.rule_type == "C":
            # 律C：最新一位的数值
            return window[-1]
        elif self.rule_type == "D":
            # 律D：出现次数最多的数值；若并列，选最近出现位置更靠后的
            from collections import Counter
            counter = Counter(window)
            max_count = max(counter.values())
            # 找出所有出现次数最多的值
            candidates = [v for v, c in counter.items() if c == max_count]
            # 如果只有一个候选，直接返回
            if len(candidates) == 1:
                return candidates[0]
            # 否则找最近出现位置更靠后的
            last_positions = {}
            for i, v in enumerate(window):
                last_positions[v] = i
            # 在候选中选择最后出现位置最大的
            return max(candidates, key=lambda v: last_positions[v])
        else:
            raise ValueError(f"Unknown rule type: {self.rule_type}")

    def evaluate(self, parsed_info):
        """
        评估最终答案。
        - 如果序列长度已达12：需同时满足规则正确 + 目标值匹配
        - 如果序列长度未达12：只检查规则是否正确
          (规则正确则返回True，表示成功推断；规则错误则返回False)
        """
        submitted = parsed_info["answer"].strip().upper()
        
        # 检查提交的规则类型是否正确
        if submitted != self.rule_type:
            return False
        
        # 记录已提交的规则
        self.submitted_rule = submitted
        
        # 如果序列长度已达到12，同时检查终局目标
        if len(self.sequence) >= self.max_length:
            window = self._get_window()
            output = self._compute_function(window)
            return output == self.target_value
        else:
            # 序列未满12时，规则正确即算成功
            return True

    def _cf_core_produce(self, parsed_info):
        """原始的业务逻辑"""
        # 投掷操作：追加元素
        if "throw" in parsed_info:
            if len(self.sequence) >= self.max_length:
                return "错误：序列已达到最大长度。" if self.config.language == "zh" else "Error: Sequence has reached maximum length."
            
            try:
                value = int(parsed_info["throw"].strip())
                if value not in [0, 1, 2]:
                    raise ValueError
            except:
                return "错误：投掷的值必须是 0、1 或 2。" if self.config.language == "zh" else "Error: Throw value must be 0, 1, or 2."
            
            self.sequence.append(value)
            
            if self.config.language == "zh":
                return f"已追加 {value}，当前序列长度：{len(self.sequence)}"
            else:
                return f"Appended {value}, current sequence length: {len(self.sequence)}"

        # 听回声：查询当前函数输出
        elif "echo" in parsed_info:
            window = self._get_window()
            output = self._compute_function(window)
            
            if self.config.language == "zh":
                return f"回声：{output}"
            else:
                return f"Echo: {output}"

        # 查询长度
        elif "query_length" in parsed_info:
            current_length = len(self.sequence)
            remaining = self.max_length - current_length
            
            if self.config.language == "zh":
                return f"当前序列长度：{current_length}，剩余可追加次数：{remaining}"
            else:
                return f"Current sequence length: {current_length}, remaining appends: {remaining}"

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list:
        """
        枚举所有合法查询并返回对应的正确答案。
        注意：throw 操作会修改序列状态，在 redundancy 评估中不适合作为独立查询。
        因此只返回无副作用的查询类型。
        """
        results = []
        
        # 1. 投掷操作 (0, 1, 2) - 需要安全地模拟
        original_sequence = list(self.sequence)
        
        for val in [0, 1, 2]:
            query_xml = f"<throw>{val}</throw>"
            parsed_info = {"throw": str(val)}
            response = self._cf_core_produce(parsed_info)
            results.append({
                "query": query_xml,
                "answer": response
            })
            # 恢复状态
            self.sequence = list(original_sequence)
        
        # 2. 听回声
        query_xml = "<echo></echo>"
        parsed_info = {"echo": ""}
        response = self._cf_core_produce(parsed_info)
        results.append({
            "query": query_xml,
            "answer": response
        })
        
        # 3. 查询长度
        query_xml = "<query_length></query_length>"
        parsed_info = {"query_length": ""}
        response = self._cf_core_produce(parsed_info)
        results.append({
            "query": query_xml,
            "answer": response
        })
        
        return results

    def _cf_make_wrong(self, correct: str) -> str:
        """将正确响应篡改为错误响应，主要针对其中的数字进行修改"""
        import re as _re
        
        # 尝试找到响应中的关键数字并篡改
        # 针对 echo 响应（如 "Echo: 1" 或 "回声：1"），篡改输出值
        # 针对 throw 响应（如 "Appended 1, current sequence length: 3"），篡改长度
        # 针对 query_length 响应，篡改数字
        
        def _alter_number(match):
            num = int(match.group(0))
            # 对于 0/1/2 范围的值，循环偏移
            if 0 <= num <= 2:
                return str((num + 1) % 3)
            # 对于更大的数字（如序列长度），加减 1
            return str(num + 1)
        
        # 查找字符串中的所有数字，替换最后一个（通常是关键值）
        numbers = list(_re.finditer(r'\d+', correct))
        if numbers:
            last_match = numbers[-1]
            original_num = int(last_match.group(0))
            if 0 <= original_num <= 2:
                wrong_num = (original_num + 1) % 3
            else:
                wrong_num = original_num + 1
            return correct[:last_match.start()] + str(wrong_num) + correct[last_match.end():]
        
        # 若无数字可替换，附加标记
        return correct + " [WRONG]"