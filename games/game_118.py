from .base import Game
import re

class GAME230(Game):

    game_rule_zh = """\
我们现在来玩一个"函数与参数推断"游戏，规则如下：

游戏设定了一个未知的非负整数 N 以及一个未知的计算函数 f。该函数从以下四个候选中选取：
- f_A(N, K) = 向下取整((N + K) / 2)
- f_B(N, K) = 向上取整((N + K) / 2)
- f_C(N, K) = 向下取整((N + K) / 3)
- f_D(N, K) = 向上取整((N + K) / 3)

在整个游戏过程中，N 和 f 保持不变。你的目标是通过多次测试，推断出所使用的函数类型以及 N 的确切值。

每轮测试中，你可以选择一个非负整数 K 作为参数，并发起以下三类查询之一：

1. **读数查询**：请求返回 R = f(N, K) 的具体值（一个非负整数）。
2. **阈值比较查询**：给定一个非负整数 t，询问 R 是否大于等于 t。回答"是"或"否"。
3. **等值比较查询**：给定一个非负整数 t，询问 R 是否等于 t。回答"是"或"否"。

其中 R 始终按所选函数 f 和当前参数 K 计算得到。K 和 t 可根据先前查询的反馈自适应选择。

每次只能提交一个查询。请使用以下 XML 格式：

- 读数查询（例如 K=10）：
<query_read>10</query_read>

- 阈值比较查询（例如 K=10, t=15）：
<query_threshold>K=10, t=15</query_threshold>

- 等值比较查询（例如 K=10, t=15）：
<query_equal>K=10, t=15</query_equal>

当你收集了足够的信息后，请提交最终答案。答案必须包含函数类型（f_A、f_B、f_C 或 f_D）和 N 的值。格式如下：

<answer>function=f_A, N=5</answer>

注意：必须至少进行 3 次测试后才能提交答案，否则游戏失败。若答案错误或格式不符，游戏同样失败。
"""

    game_rule_en = """\
Let's play a "Function and Parameter Inference" game. Here are the rules:

The game has set an unknown non-negative integer N and an unknown computation function f. The function is selected from the following four candidates:
- f_A(N, K) = floor((N + K) / 2)
- f_B(N, K) = ceil((N + K) / 2)
- f_C(N, K) = floor((N + K) / 3)
- f_D(N, K) = ceil((N + K) / 3)

Throughout the game, N and f remain constant. Your goal is to infer the function type and the exact value of N through multiple tests.

In each test round, you can choose a non-negative integer K as a parameter and make one of the following three types of queries:

1. **Read Query**: Request the exact value of R = f(N, K) (a non-negative integer).
2. **Threshold Comparison Query**: Given a non-negative integer t, ask whether R is greater than or equal to t. Answer "Yes" or "No".
3. **Equality Comparison Query**: Given a non-negative integer t, ask whether R equals t. Answer "Yes" or "No".

Where R is always calculated using the selected function f and current parameter K. K and t can be adaptively chosen based on feedback from previous queries.

Only one query can be submitted at a time. Use the following XML format:

- Read Query (e.g., K=10):
<query_read>10</query_read>

- Threshold Comparison Query (e.g., K=10, t=15):
<query_threshold>K=10, t=15</query_threshold>

- Equality Comparison Query (e.g., K=10, t=15):
<query_equal>K=10, t=15</query_equal>

When you have gathered enough information, submit your final answer. The answer must include the function type (f_A, f_B, f_C, or f_D) and the value of N. Format as follows:

<answer>function=f_A, N=5</answer>

Note: You must perform at least 3 tests before submitting an answer, otherwise the game fails. If the answer is incorrect or the format is invalid, the game also fails.
"""

    contextualized_rule_zh_1 = """\
欢迎使用"智能路网核心调度算法推断"系统。

系统当前已锁定某个片区的初始拥堵基数 N（未知的非负整数），并隐式挂载了调度分配函数 f。该函数从以下四种预设控制策略中选取：
- f_A(N, K) = 向下取整((N + K) / 2)
- f_B(N, K) = 向上取整((N + K) / 2)
- f_C(N, K) = 向下取整((N + K) / 3)
- f_D(N, K) = 向上取整((N + K) / 3)

在整个诊断过程中，N 和 f 保持不变。你的目标是通过输入模拟数据，推测出系统正在使用的策略类型（f）以及真实的拥堵基数（N）。

每轮测试中，你可以设定一个非负整数 K 作为"新增汇入车流量"参数，并发起以下三类查询之一：

1. **读数查询**：请求返回系统计算出的最终等效负荷 R = f(N, K) 的具体值（一个非负整数）。
2. **阈值比较查询**：给定一个非负整数 t（预警阈值），询问 R 是否大于等于 t。系统反馈"是"或"否"。
3. **等值比较查询**：给定一个非负整数 t（特定匹配值），询问 R 是否等于 t。系统反馈"是"或"否"。

其中，R 始终按所选策略 f 和当前参数 K 计算得到。K 和 t 可根据先前查询的反馈动态调整。

每次只能提交一个查询。请使用以下 XML 格式与终端交互：

- 读数查询（例如模拟汇入车流量 K=10）：
<query_read>10</query_read>

- 阈值比较查询（例如 K=10, t=15）：
<query_threshold>K=10, t=15</query_threshold>

- 等值比较查询（例如 K=10, t=15）：
<query_equal>K=10, t=15</query_equal>

当你收集了足够的数据后，请提交最终结论。答案必须包含策略类型（f_A、f_B、f_C 或 f_D）和拥堵基数 N 的值。格式如下：

<answer>function=f_A, N=5</answer>

注意：必须至少进行 3 次模拟测试后才能提交结论，否则诊断失败。若答案错误或格式不符，同样判定为失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Smart Road Network Core Dispatch Algorithm Inference" system.

The system has locked onto an initial congestion baseline N (an unknown non-negative integer) for a specific zone and implicitly mounted a dispatch allocation function f. The function is selected from the following four preset control strategies:
- f_A(N, K) = floor((N + K) / 2)
- f_B(N, K) = ceil((N + K) / 2)
- f_C(N, K) = floor((N + K) / 3)
- f_D(N, K) = ceil((N + K) / 3)

Throughout the diagnostic process, N and f remain constant. Your goal is to infer the strategy type (f) and the exact value of the congestion baseline (N) through data simulations.

In each test round, you can set a non-negative integer K as the "additional incoming traffic volume" parameter and make one of the following three types of queries:

1. **Read Query**: Request the exact value of the final equivalent load R = f(N, K) (a non-negative integer).
2. **Threshold Comparison Query**: Given a non-negative integer t (warning threshold), ask whether R is greater than or equal to t. The system answers "Yes" or "No".
3. **Equality Comparison Query**: Given a non-negative integer t (specific match value), ask whether R equals t. The system answers "Yes" or "No".

Here, R is always calculated using the selected strategy f and current parameter K. K and t can be adaptively adjusted based on feedback from previous queries.

Only one query can be submitted at a time. Use the following XML format to interact with the terminal:

- Read Query (e.g., incoming volume K=10):
<query_read>10</query_read>

- Threshold Comparison Query (e.g., K=10, t=15):
<query_threshold>K=10, t=15</query_threshold>

- Equality Comparison Query (e.g., K=10, t=15):
<query_equal>K=10, t=15</query_equal>

When you have gathered enough data, submit your final conclusion. The answer must include the strategy type (f_A, f_B, f_C, or f_D) and the value of N. Format as follows:

<answer>function=f_A, N=5</answer>

Note: You must perform at least 3 simulation tests before submitting a conclusion; otherwise, the diagnosis fails. If the answer is incorrect or the format is invalid, it also results in a failure.
"""

    contextualized_rule_zh_2 = """\
欢迎进入"靶向药物药代动力学分析"系统。

系统当前设定了一个未知的患者基础代谢负荷 N（未知的非负整数），以及一个未知的药代动力学反应模型 f。该模型从以下四种预设代谢模型中选取：
- f_A(N, K) = 向下取整((N + K) / 2)
- f_B(N, K) = 向上取整((N + K) / 2)
- f_C(N, K) = 向下取整((N + K) / 3)
- f_D(N, K) = 向上取整((N + K) / 3)

在整个盲测过程中，N 和 f 保持不变。你的目标是通过输入给药方案，推测出系统正在使用的代谢模型类型（f）以及真实的基础代谢负荷（N）。

每轮测试中，你可以设定一个非负整数 K 作为"额外干预剂量"参数，并发起以下三类查询之一：

1. **读数查询**：请求返回系统计算出的峰值生理指标 R = f(N, K) 的具体值（一个非负整数）。
2. **阈值比较查询**：给定一个非负整数 t，询问 R 是否大于等于 t。系统反馈"是"或"否"。
3. **等值比较查询**：给定一个非负整数 t，询问 R 是否等于 t。系统反馈"是"或"否"。

其中，R 始终按所选模型 f 和当前参数 K 计算得到。K 和 t 可根据先前查询的反馈动态调整。

每次只能提交一个查询。请使用以下 XML 格式与终端交互：

- 读数查询（例如干预剂量 K=10）：
<query_read>10</query_read>

- 阈值比较查询（例如 K=10, t=15）：
<query_threshold>K=10, t=15</query_threshold>

- 等值比较查询（例如 K=10, t=15）：
<query_equal>K=10, t=15</query_equal>

当你收集了足够的数据后，请提交最终结论。答案必须包含代谢模型类型（f_A、f_B、f_C 或 f_D）和基础代谢负荷 N 的值。格式如下：

<answer>function=f_A, N=5</answer>

注意：必须至少进行 3 次模拟测试后才能提交结论，否则分析失败。若答案错误或格式不符，同样判定为失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Targeted Drug Pharmacokinetics Analysis" system.

The system has set an unknown patient basal metabolic load N (an unknown non-negative integer) and an unknown pharmacokinetic reaction model f. The model is selected from the following four preset metabolic models:
- f_A(N, K) = floor((N + K) / 2)
- f_B(N, K) = ceil((N + K) / 2)
- f_C(N, K) = floor((N + K) / 3)
- f_D(N, K) = ceil((N + K) / 3)

Throughout the blind testing process, N and f remain constant. Your goal is to infer the metabolic model type (f) and the exact value of the basal metabolic load (N) by inputting dosing regimens.

In each test round, you can set a non-negative integer K as the "additional intervention dosage" parameter and make one of the following three types of queries:

1. **Read Query**: Request the exact value of the peak physiological index R = f(N, K) (a non-negative integer).
2. **Threshold Comparison Query**: Given a non-negative integer t, ask whether R is greater than or equal to t. The system answers "Yes" or "No".
3. **Equality Comparison Query**: Given a non-negative integer t, ask whether R equals t. The system answers "Yes" or "No".

Here, R is always calculated using the selected model f and current parameter K. K and t can be adaptively adjusted based on feedback from previous queries.

Only one query can be submitted at a time. Use the following XML format to interact with the terminal:

- Read Query (e.g., intervention dosage K=10):
<query_read>10</query_read>

- Threshold Comparison Query (e.g., K=10, t=15):
<query_threshold>K=10, t=15</query_threshold>

- Equality Comparison Query (e.g., K=10, t=15):
<query_equal>K=10, t=15</query_equal>

When you have gathered enough data, submit your final conclusion. The answer must include the metabolic model type (f_A, f_B, f_C, or f_D) and the value of N. Format as follows:

<answer>function=f_A, N=5</answer>

Note: You must perform at least 3 simulation tests before submitting a conclusion; otherwise, the analysis fails. If the answer is incorrect or the format is invalid, it also results in a failure.
"""

    contextualized_rule_zh_3 = """\
欢迎使用"学情评估与量化分析"终端。

系统当前设定了一个未知的学生基础学力指数 N（未知的非负整数），以及一个未知的教学评估模型 f。该模型从以下四种预设评估基准中选取：
- f_A(N, K) = 向下取整((N + K) / 2)
- f_B(N, K) = 向上取整((N + K) / 2)
- f_C(N, K) = 向下取整((N + K) / 3)
- f_D(N, K) = 向上取整((N + K) / 3)

在整个分析过程中，N 和 f 保持不变。你的目标是通过输入模拟干预方案，推测出系统正在使用的评估模型类型（f）以及真实的基础学力指数（N）。

每轮测试中，你可以设定一个非负整数 K 作为"额外辅导训练强度"参数，并发起以下三类查询之一：

1. **读数查询**：请求返回系统计算出的标准化考核等效分 R = f(N, K) 的具体值（一个非负整数）。
2. **阈值比较查询**：给定一个非负整数 t，询问 R 是否大于等于 t。系统反馈"是"或"否"。
3. **等值比较查询**：给定一个非负整数 t，询问 R 是否等于 t。系统反馈"是"或"否"。

其中，R 始终按所选模型 f 和当前参数 K 计算得到。K 和 t 可根据先前查询的反馈动态调整。

每次只能提交一个查询。请使用以下 XML 格式与终端交互：

- 读数查询（例如训练强度 K=10）：
<query_read>10</query_read>

- 阈值比较查询（例如 K=10, t=15）：
<query_threshold>K=10, t=15</query_threshold>

- 等值比较查询（例如 K=10, t=15）：
<query_equal>K=10, t=15</query_equal>

当你收集了足够的数据后，请提交最终结论。答案必须包含评估模型类型（f_A、f_B、f_C 或 f_D）和基础学力指数 N 的值。格式如下：

<answer>function=f_A, N=5</answer>

注意：必须至少进行 3 次模拟测试后才能提交结论，否则分析失败。若答案错误或格式不符，同样判定为失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Student Performance Quantitative Analysis" terminal.

The system has set an unknown student foundational competence score N (an unknown non-negative integer) and an unknown pedagogical evaluation model f. The model is selected from the following four preset evaluation baselines:
- f_A(N, K) = floor((N + K) / 2)
- f_B(N, K) = ceil((N + K) / 2)
- f_C(N, K) = floor((N + K) / 3)
- f_D(N, K) = ceil((N + K) / 3)

Throughout the analysis process, N and f remain constant. Your goal is to infer the evaluation model type (f) and the exact value of the foundational competence score (N) by inputting simulated intervention plans.

In each test round, you can set a non-negative integer K as the "additional tutoring intensity" parameter and make one of the following three types of queries:

1. **Read Query**: Request the exact value of the standardized assessment metric R = f(N, K) (a non-negative integer).
2. **Threshold Comparison Query**: Given a non-negative integer t, ask whether R is greater than or equal to t. The system answers "Yes" or "No".
3. **Equality Comparison Query**: Given a non-negative integer t, ask whether R equals t. The system answers "Yes" or "No".

Here, R is always calculated using the selected model f and current parameter K. K and t can be adaptively adjusted based on feedback from previous queries.

Only one query can be submitted at a time. Use the following XML format to interact with the terminal:

- Read Query (e.g., tutoring intensity K=10):
<query_read>10</query_read>

- Threshold Comparison Query (e.g., K=10, t=15):
<query_threshold>K=10, t=15</query_threshold>

- Equality Comparison Query (e.g., K=10, t=15):
<query_equal>K=10, t=15</query_equal>

When you have gathered enough data, submit your final conclusion. The answer must include the evaluation model type (f_A, f_B, f_C, or f_D) and the value of N. Format as follows:

<answer>function=f_A, N=5</answer>

Note: You must perform at least 3 simulation tests before submitting a conclusion; otherwise, the analysis fails. If the answer is incorrect or the format is invalid, it also results in a failure.
"""

    contextualized_rule_zh_4 = """\
欢迎操作"精密制造材料应力测试"控制台。

系统当前设定了一个未知的材料初始内应力系数 N（未知的非负整数），以及一个未知的形变计算模型 f。该模型从以下四种预设演算标准中选取：
- f_A(N, K) = 向下取整((N + K) / 2)
- f_B(N, K) = 向上取整((N + K) / 2)
- f_C(N, K) = 向下取整((N + K) / 3)
- f_D(N, K) = 向上取整((N + K) / 3)

在整个测试过程中，N 和 f 保持不变。你的目标是通过施加外部压力，推测出系统正在使用的形变计算模型类型（f）以及真实的初始内应力系数（N）。

每轮测试中，你可以设定一个非负整数 K 作为"额外施加压强"参数，并发起以下三类查询之一：

1. **读数查询**：请求返回系统计算出的结构形变指数 R = f(N, K) 的具体值（一个非负整数）。
2. **阈值比较查询**：给定一个非负整数 t，询问 R 是否大于等于 t。系统反馈"是"或"否"。
3. **等值比较查询**：给定一个非负整数 t，询问 R 是否等于 t。系统反馈"是"或"否"。

其中，R 始终按所选模型 f 和当前参数 K 计算得到。K 和 t可根据先前查询的反馈动态调整。

每次只能提交一个查询。请使用以下 XML 格式与终端交互：

- 读数查询（例如施加压强 K=10）：
<query_read>10</query_read>

- 阈值比较查询（例如 K=10, t=15）：
<query_threshold>K=10, t=15</query_threshold>

- 等值比较查询（例如 K=10, t=15）：
<query_equal>K=10, t=15</query_equal>

当你收集了足够的数据后，请提交最终结论。答案必须包含计算模型类型（f_A、f_B、f_C 或 f_D）和初始内应力系数 N 的值。格式如下：

<answer>function=f_A, N=5</answer>

注意：必须至少进行 3 次模拟测试后才能提交结论，否则测试失败。若答案错误或格式不符，同样判定为失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Precision Manufacturing Material Stress Test" console.

The system has set an unknown inherent baseline stress coefficient N (an unknown non-negative integer) and an unknown deformation calculation model f for the material. The model is selected from the following four preset calculation standards:
- f_A(N, K) = floor((N + K) / 2)
- f_B(N, K) = ceil((N + K) / 2)
- f_C(N, K) = floor((N + K) / 3)
- f_D(N, K) = ceil((N + K) / 3)

Throughout the testing process, N and f remain constant. Your goal is to infer the deformation calculation model type (f) and the exact value of the inherent baseline stress coefficient (N) by applying external pressure.

In each test round, you can set a non-negative integer K as the "applied external pressure units" parameter and make one of the following three types of queries:

1. **Read Query**: Request the exact value of the structural deformation index R = f(N, K) (a non-negative integer).
2. **Threshold Comparison Query**: Given a non-negative integer t, ask whether R is greater than or equal to t. The system answers "Yes" or "No".
3. **Equality Comparison Query**: Given a non-negative integer t, ask whether R equals t. The system answers "Yes" or "No".

Here, R is always calculated using the selected model f and current parameter K. K and t can be adaptively adjusted based on feedback from previous queries.

Only one query can be submitted at a time. Use the following XML format to interact with the terminal:

- Read Query (e.g., applied pressure K=10):
<query_read>10</query_read>

- Threshold Comparison Query (e.g., K=10, t=15):
<query_threshold>K=10, t=15</query_threshold>

- Equality Comparison Query (e.g., K=10, t=15):
<query_equal>K=10, t=15</query_equal>

When you have gathered enough data, submit your final conclusion. The answer must include the calculation model type (f_A, f_B, f_C, or f_D) and the value of N. Format as follows:

<answer>function=f_A, N=5</answer>

Note: You must perform at least 3 simulation tests before submitting a conclusion; otherwise, the test fails. If the answer is incorrect or the format is invalid, it also results in a failure.
"""

    contextualized_rule_zh_5 = """\
欢迎登录"量刑辅助计算反推"系统。

系统当前设定了一个未知的法定基准刑期（月） N，以及一个未知的综合裁量函数 f。该函数从以下四种预设裁量准则中选取：
- f_A(N, K) = 向下取整((N + K) / 2)
- f_B(N, K) = 向上取整((N + K) / 2)
- f_C(N, K) = 向下取整((N + K) / 3)
- f_D(N, K) = 向上取整((N + K) / 3)

在整个诊断过程中，N 和 f 保持不变。你的目标是通过输入模拟数据，推测出系统正在使用的裁量函数类型（f）以及真实的基准刑期（N）。

每轮测试中，你可以设定一个非负整数 K 作为"法定加重情节权重"参数，并发起以下三类查询之一：

1. **读数查询**：请求返回系统计算出的最终宣告刑期（月） R = f(N, K) 的具体值（一个非负整数）。
2. **阈值比较查询**：给定一个非负整数 t，询问 R 是否大于等于 t。系统反馈"是"或"否"。
3. **等值比较查询**：给定一个非负整数 t，询问 R 是否等于 t。系统反馈"是"或"否"。

其中，R 始终按所选函数 f 和当前参数 K 计算得到。K 和 t 可根据先前查询的反馈动态调整。

每次只能提交一个查询。请使用以下 XML 格式与终端交互：

- 读数查询（例如 K=10）：
<query_read>10</query_read>

- 阈值比较查询（例如 K=10, t=15）：
<query_threshold>K=10, t=15</query_threshold>

- 等值比较查询（例如 K=10, t=15）：
<query_equal>K=10, t=15</query_equal>

当你收集了足够的数据后，请提交最终结论。答案必须包含裁量函数类型（f_A、f_B、f_C 或 f_D）和基准刑期 N 的值。格式如下：

<answer>function=f_A, N=5</answer>

注意：必须至少进行 3 次模拟测试后才能提交结论，否则推断失败。若答案错误或格式不符，同样判定为失败。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Sentencing Auxiliary Calculation Reverse-Engineering" system.

The system has set an unknown statutory baseline sentence length (in months) N and an unknown comprehensive discretionary function f. The function is selected from the following four preset discretionary guidelines:
- f_A(N, K) = floor((N + K) / 2)
- f_B(N, K) = ceil((N + K) / 2)
- f_C(N, K) = floor((N + K) / 3)
- f_D(N, K) = ceil((N + K) / 3)

Throughout the diagnostic process, N and f remain constant. Your goal is to infer the discretionary function type (f) and the exact value of the baseline sentence length (N) by inputting simulated data.

In each test round, you can set a non-negative integer K as the "aggravating circumstances weight" parameter and make one of the following three types of queries:

1. **Read Query**: Request the exact value of the final adjudicated term (in months) R = f(N, K) (a non-negative integer).
2. **Threshold Comparison Query**: Given a non-negative integer t, ask whether R is greater than or equal to t. The system answers "Yes" or "No".
3. **Equality Comparison Query**: Given a non-negative integer t, ask whether R equals t. The system answers "Yes" or "No".

Here, R is always calculated using the selected function f and current parameter K. K and t can be adaptively adjusted based on feedback from previous queries.

Only one query can be submitted at a time. Use the following XML format to interact with the terminal:

- Read Query (e.g., weight K=10):
<query_read>10</query_read>

- Threshold Comparison Query (e.g., K=10, t=15):
<query_threshold>K=10, t=15</query_threshold>

- Equality Comparison Query (e.g., K=10, t=15):
<query_equal>K=10, t=15</query_equal>

When you have gathered enough data, submit your final conclusion. The answer must include the discretionary function type (f_A, f_B, f_C, or f_D) and the value of N. Format as follows:

<answer>function=f_A, N=5</answer>

Note: You must perform at least 3 simulation tests before submitting a conclusion; otherwise, the inference fails. If the answer is incorrect or the format is invalid, it also results in a failure.
"""

    tags = ["answer", "query_read", "query_threshold", "query_equal"]
    
    reasoning_type = "溯因推理"
    data_structure = "集合"

    DIFFICULTY_CONFIG = {
        1: {"N": 5, "function": "f_A"},
        2: {"N": 7, "function": "f_B"},
        3: {"N": 10, "function": "f_C"},
        4: {"N": 13, "function": "f_D"},
        5: {"N": 20, "function": "f_C"},
    }

    def __init__(self, config):
        self.query_count = 0
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)
        
        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")
        
        cfg = self.DIFFICULTY_CONFIG[diff]
        self.N = cfg["N"]
        self.function_type = cfg["function"]
        
        self._game_info["n"] = self.N

    def _compute_function(self, K):
        sum_val = self.N + K
        
        if self.function_type == "f_A":
            return sum_val // 2
        elif self.function_type == "f_B":
            return (sum_val + 1) // 2
        elif self.function_type == "f_C":
            return sum_val // 3
        elif self.function_type == "f_D":
            return (sum_val + 2) // 3
        else:
            raise ValueError(f"Unknown function type: {self.function_type}")

    def evaluate(self, parsed_info):
        
        raw_ans = parsed_info["answer"]
        
        ans_dict = {}
        for part in raw_ans.split(","):
            part = part.strip()
            if "=" in part:
                k, v = part.split("=", 1)
                ans_dict[k.strip()] = v.strip()
        
        if "function" not in ans_dict or "N" not in ans_dict:
            return False
        
        if ans_dict["function"] != self.function_type:
            return False
        
        try:
            model_N = int(ans_dict["N"])
        except (ValueError, TypeError):
            return False
        
        return model_N == self.N

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        representative_ks = [0, 1, 2, 5, 10]
        
        if self.config.language == "zh":
            yes_str, no_str = "是", "否"
        else:
            yes_str, no_str = "Yes", "No"
        
        for K in representative_ks:
            R = self._compute_function(K)
            
            q_read = f"<query_read>{K}</query_read>"
            queries.append({"query": q_read, "answer": str(R)})
            
            for t in [0, R - 1, R, R + 1]:
                if t < 0:
                    continue
                ans_thresh = yes_str if R >= t else no_str
                q_thresh = f"<query_threshold>K={K}, t={t}</query_threshold>"
                queries.append({"query": q_thresh, "answer": ans_thresh})
                
                ans_eq = yes_str if R == t else no_str
                q_eq = f"<query_equal>K={K}, t={t}</query_equal>"
                queries.append({"query": q_eq, "answer": ans_eq})
        
        return queries

    def _cf_make_wrong(self, correct):
        if self.config.language == "zh":
            yes_str, no_str = "是", "否"
        else:
            yes_str, no_str = "Yes", "No"

        if correct == yes_str:
            return no_str
        elif correct == no_str:
            return yes_str

        try:
            val = int(correct)
            wrong_val = val + 1
            return str(wrong_val)
        except (ValueError, TypeError):
            pass

        return correct + "_wrong"

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：格式无效或参数错误。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid format or parameter."
        
        if "query_read" in parsed_info:
            try:
                K = int(parsed_info["query_read"].strip())
                if K < 0:
                    return error_format
                self.query_count += 1
                R = self._compute_function(K)
                return str(R)
            except Exception:
                return error_format
        
        elif "query_threshold" in parsed_info:
            try:
                raw = parsed_info["query_threshold"]
                parts = {}
                for item in raw.split(","):
                    item = item.strip()
                    if "=" in item:
                        k, v = item.split("=", 1)
                        parts[k.strip()] = v.strip()
                
                K = int(parts.get("K", ""))
                t = int(parts.get("t", ""))
                
                if K < 0 or t < 0:
                    return error_format
                
                self.query_count += 1
                R = self._compute_function(K)
                return yes_res if R >= t else no_res
            except Exception:
                return error_format
        
        elif "query_equal" in parsed_info:
            try:
                raw = parsed_info["query_equal"]
                parts = {}
                for item in raw.split(","):
                    item = item.strip()
                    if "=" in item:
                        k, v = item.split("=", 1)
                        parts[k.strip()] = v.strip()
                
                K = int(parts.get("K", ""))
                t = int(parts.get("t", ""))
                
                if K < 0 or t < 0:
                    return error_format
                
                self.query_count += 1
                R = self._compute_function(K)
                return yes_res if R == t else no_res
            except Exception:
                return error_format
        
        else:
            raise ValueError("No valid query tag found.")