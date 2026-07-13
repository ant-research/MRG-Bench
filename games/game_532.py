# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   最优路径：所有根到叶路径中属性值之和最大的路径是哪条
# ============================================================

import re
import random
from typing import List, Dict
from .base import Game

class OptimalPathIdentificationGame(Game):

    game_rule_zh = """\
我们现在来玩一个"交互式最优路径识别"的推理游戏，规则如下：

游戏设定了一棵深度为3的满三叉树（共40个节点，包含根节点）。每个节点的子节点分别用符号 S、M、T 标记。从根到叶的每条路径可以用一个长度为3的符号序列表示，例如 SMT、SSS 等。

树的结构：
- 根节点深度为0，取值为0（不计入路径和）
- 每个内节点有3个子节点，分别对应符号 S、M、T
- 从根到叶的任意路径长度均为3

节点取值规则：
每个非根节点的取值由以下公式计算：
  v(d, x, prev) = w[x] + Δ[d] + repeat(prev, x) × B

其中：
- d 表示节点深度（1、2 或 3）
- x 表示当前节点的符号（S、M 或 T）
- prev 表示上一步的符号（深度为1时不适用）
- w[S]、w[M]、w[T] 是未知的整数基础权重，范围在 -9 到 9 之间
- Δ[1] = 0（已知），Δ[2]、Δ[3] 是未知的整数深度修正项，范围在 -5 到 5 之间
- B 是未知的整数连续同符号奖励，范围在 -5 到 5 之间
- repeat(prev, x) = 1 当且仅当深度大于等于2且 prev = x，否则为 0

路径值定义：
一条从根到叶的路径（长度为3）的值等于该路径上3个非根节点的取值之和。

你的任务：
通过提出查询来推断哪条长度为3的路径具有最大值（如有并列最大值，任选其一即可）。

你可以提出以下三类查询（每次提交一个查询）：

1. 节点查询：查询某个节点的取值
   格式：<query_node>序列</query_node>
   例如：<query_node>S</query_node> 或 <query_node>SM</query_node> 或 <query_node>SMT</query_node>
   序列长度为1到3，由 S、M、T 组成
   返回：NODE = 整数值

2. 路径查询：查询某条完整路径（长度为3）的总值
   格式：<query_path>序列</query_path>
   例如：<query_path>SMT</query_path>
   序列长度必须为3
   返回：PATH = 整数值

3. 路径比较：比较两条完整路径（长度均为3）的值的大小关系
   格式：<query_compare>序列A,序列B</query_compare>
   例如：<query_compare>SMT,SSS</query_compare>
   返回：A>B 或 A<B 或 A=B

查询预算：
你最多可以进行 {max_queries} 次查询。超过预算后只能提交最终答案。

提交最终答案：
当你确定最优路径后，使用以下格式提交：
<answer>序列</answer>
例如：<answer>SMT</answer>

注意：序列必须是长度为3的由 S、M、T 组成的字符串。
"""

    game_rule_en = """\
Let's play an "Interactive Optimal Path Identification" deduction game. Here are the rules:

The game features a full ternary tree of depth 3 (40 nodes in total, including the root). Each node's children are labeled with symbols S, M, T. Every root-to-leaf path can be represented by a length-3 symbol sequence, such as SMT, SSS, etc.

Tree Structure:
- Root node is at depth 0 with value 0 (not counted in path sum)
- Each internal node has 3 children corresponding to symbols S, M, T
- Any root-to-leaf path has length exactly 3

Node Value Rule:
Each non-root node's value is calculated by the formula:
  v(d, x, prev) = w[x] + Δ[d] + repeat(prev, x) × B

Where:
- d is the node depth (1, 2, or 3)
- x is the current node's symbol (S, M, or T)
- prev is the previous step's symbol (not applicable at depth 1)
- w[S], w[M], w[T] are unknown integer base weights in range -9 to 9
- Δ[1] = 0 (known), Δ[2], Δ[3] are unknown integer depth modifiers in range -5 to 5
- B is the unknown integer consecutive symbol bonus in range -5 to 5
- repeat(prev, x) = 1 if and only if depth is at least 2 and prev = x, otherwise 0

Path Value Definition:
A root-to-leaf path (length 3) has value equal to the sum of the 3 non-root nodes' values along the path.

Your Task:
Through queries, infer which length-3 path has the maximum value (if tied, any of the maximum-value paths is acceptable).

You can make the following three types of queries (submit one query at a time):

1. Node Query: Query the value of a specific node
   Format: <query_node>sequence</query_node>
   Example: <query_node>S</query_node> or <query_node>SM</query_node> or <query_node>SMT</query_node>
   Sequence length is 1 to 3, composed of S, M, T
   Response: NODE = integer value

2. Path Query: Query the total value of a complete path (length 3)
   Format: <query_path>sequence</query_path>
   Example: <query_path>SMT</query_path>
   Sequence length must be 3
   Response: PATH = integer value

3. Path Comparison: Compare the values of two complete paths (both length 3)
   Format: <query_compare>sequenceA,sequenceB</query_compare>
   Example: <query_compare>SMT,SSS</query_compare>
   Response: A>B or A<B or A=B

Query Budget:
You can make at most {max_queries} queries. After exceeding the budget, you can only submit the final answer.

Submit Final Answer:
When you have determined the optimal path, submit using the format:
<answer>sequence</answer>
Example: <answer>SMT</answer>

Note: The sequence must be a length-3 string composed of S, M, T.
"""

    contextualized_rule_zh_1 = """\
智能城市交通系统现在需要您进行"多阶段最优路线规划"。规则如下：

我们的路网规划涉及一个分3个阶段的通行网络。在每个阶段，车辆可以选择三种道路类型：S（Street-街道）、M（Motorway-快速路）、T（Tunnel-隧道）。一条完整的3阶段路线可以用一个长度为3的符号序列表示，例如 SMT、SSS 等。

路线结构：
- 起点为第0阶段，得分为0（不计入路线总得分）
- 在接下来的每个阶段（共3个阶段），都有3种道路类型可供选择（S、M、T）
- 任何完整的路线都会经历刚好3个阶段

效能得分规则：
每个阶段选择某道路类型的单阶段效能得分由以下公式计算：
  v(d, x, prev) = w[x] + Δ[d] + repeat(prev, x) × B

其中：
- d 表示当前所处阶段（1、2 或 3）
- x 表示当前选择的道路类型（S、M 或 T）
- prev 表示上一阶段的道路类型（第1阶段时不适用）
- w[S]、w[M]、w[T] 是未知的特定道路基础效能分，范围在 -9 到 9 之间
- Δ[1] = 0（已知），Δ[2]、Δ[3] 是未知的阶段路况修正项，范围在 -5 到 5 之间
- B 是未知的连续采用同种道路的协同奖励，范围在 -5 到 5 之间
- repeat(prev, x) = 1 当且仅当处于第2或第3阶段且 prev = x，否则为 0

路线总得分定义：
一条完整路线（经历3个阶段）的总得分等于该路线上3个阶段的效能得分之和。

您的任务：
通过向交通路网系统提出查询，推断出哪条3阶段路线具有最大总得分（如有并列最大值，任选其一即可）。

您可以提出以下三类查询（每次提交一个查询）：

1. 节点查询：查询行驶到某个阶段的特定路线节点的单步效能得分
   格式：<query_node>序列</query_node>
   例如：<query_node>S</query_node> 或 <query_node>SM</query_node> 或 <query_node>SMT</query_node>
   序列长度为1到3，由 S、M、T 组成
   返回：NODE = 整数值

2. 路线查询：查询某条完整路线（3个阶段）的总得分
   格式：<query_path>序列</query_path>
   例如：<query_path>SMT</query_path>
   序列长度必须为3
   返回：PATH = 整数值

3. 路线比较：比较两条完整路线（3个阶段）的总得分大小关系
   格式：<query_compare>序列A,序列B</query_compare>
   例如：<query_compare>SMT,SSS</query_compare>
   返回：A>B 或 A<B 或 A=B

查询预算：
您最多可以进行 {max_queries} 次查询。超过预算后只能提交最终答案。

提交最终答案：
当您确定最优路线后，使用以下格式提交：
<answer>序列</answer>
例如：<answer>SMT</answer>

注意：序列必须是长度为3的由 S、M、T 组成的字符串。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
The smart city traffic system now requires you to perform "Multi-stage Optimal Route Planning". The rules are as follows:

Our road network planning involves a 3-stage transit network. At each stage, vehicles can choose among three road types: S (Street), M (Motorway), T (Tunnel). A complete 3-stage route can be represented by a length-3 symbol sequence, such as SMT, SSS, etc.

Route Structure:
- The starting point is stage 0, with a score of 0 (not counted in the total route score).
- In each of the following stages (3 stages in total), 3 road types (S, M, T) are available.
- Any complete route goes through exactly 3 stages.

Efficiency Score Rule:
The efficiency score of a specific road type chosen at a given stage is calculated by:
  v(d, x, prev) = w[x] + Δ[d] + repeat(prev, x) × B

Where:
- d is the current stage (1, 2, or 3).
- x is the currently selected road type (S, M, or T).
- prev is the road type of the previous stage (not applicable at stage 1).
- w[S], w[M], w[T] are unknown base efficiency scores for each road type, ranging from -9 to 9.
- Δ[1] = 0 (known); Δ[2], Δ[3] are unknown stage traffic modifiers, ranging from -5 to 5.
- B is the unknown synergy bonus for consecutively using the same road type, ranging from -5 to 5.
- repeat(prev, x) = 1 if and only if d >= 2 and prev = x; otherwise 0.

Total Route Score Definition:
The total score of a complete route (length 3) is the sum of the efficiency scores from the 3 stages along the route.

Your Task:
Through queries to the traffic system, infer which 3-stage route has the maximum total score (if tied, any optimal route is acceptable).

You can make the following three types of queries (submit one at a time):

1. Node Query: Query the single-step efficiency score at a specific route node.
   Format: <query_node>sequence</query_node>
   Example: <query_node>S</query_node> or <query_node>SM</query_node> or <query_node>SMT</query_node>
   Sequence length is 1 to 3, composed of S, M, T.
   Response: NODE = integer value

2. Route Query: Query the total score of a complete route (length 3).
   Format: <query_path>sequence</query_path>
   Example: <query_path>SMT</query_path>
   Sequence length must be 3.
   Response: PATH = integer value

3. Route Comparison: Compare the total scores of two complete routes (both length 3).
   Format: <query_compare>sequenceA,sequenceB</query_compare>
   Example: <query_compare>SMT,SSS</query_compare>
   Response: A>B or A<B or A=B

Query Budget:
You can make at most {max_queries} queries. After exceeding the budget, you can only submit the final answer.

Submit Final Answer:
When you have determined the optimal route, submit using the format:
<answer>sequence</answer>
Example: <answer>SMT</answer>

Note: The sequence must be a length-3 string composed of S, M, T.
"""

    contextualized_rule_zh_2 = """\
临床多阶段治疗方案优化系统需要您进行"最优治疗路径推断"。规则如下：

疗程分为3个干预阶段。在每个阶段，医生可以选择三种干预手段：S（Surgery-手术）、M（Medication-药物）、T（Therapy-理疗）。一套完整的3阶段治疗方案可以用一个长度为3的符号序列表示，例如 SMT、SSS 等。

方案结构：
- 治疗初始为第0阶段，评分为0（不计入总评分）
- 在接下来的每个阶段（共3个阶段），都有3种干预手段可供选择（S、M、T）
- 任何完整的方案都会经历刚好3个阶段

疗效评分规则：
每个阶段采用特定干预手段的局部疗效评分由以下公式计算：
  v(d, x, prev) = w[x] + Δ[d] + repeat(prev, x) × B

其中：
- d 表示当前干预阶段（1、2 或 3）
- x 表示当前采用的干预手段（S、M 或 T）
- prev 表示上一阶段的干预手段（第1阶段时不适用）
- w[S]、w[M]、w[T] 是未知的特定干预手段基础疗效分，范围在 -9 到 9 之间
- Δ[1] = 0（已知），Δ[2]、Δ[3] 是未知的阶段体征修正项，范围在 -5 到 5 之间
- B 是未知的连续采用同类干预的叠加增益，范围在 -5 到 5 之间
- repeat(prev, x) = 1 当且仅当处于第2或第3阶段且 prev = x，否则为 0

方案总评分定义：
一套完整治疗方案（经历3个阶段）的总评分等于该方案上3个阶段的局部疗效评分之和。

您的任务：
通过向治疗优化系统提出查询，推断出哪套3阶段方案具有最大总评分（如有并列最大值，任选其一即可）。

您可以提出以下三类查询（每次提交一个查询）：

1. 节点查询：查询某个阶段采用特定干预手段的局部疗效评分
   格式：<query_node>序列</query_node>
   例如：<query_node>S</query_node> 或 <query_node>SM</query_node> 或 <query_node>SMT</query_node>
   序列长度为1到3，由 S、M、T 组成
   返回：NODE = 整数值

2. 方案查询：查询某套完整治疗方案（3个阶段）的总评分
   格式：<query_path>序列</query_path>
   例如：<query_path>SMT</query_path>
   序列长度必须为3
   返回：PATH = 整数值

3. 方案比较：比较两套完整治疗方案（3个阶段）的总评分大小关系
   格式：<query_compare>序列A,序列B</query_compare>
   例如：<query_compare>SMT,SSS</query_compare>
   返回：A>B 或 A<B 或 A=B

查询预算：
您最多可以进行 {max_queries} 次查询。超过预算后只能提交最终答案。

提交最终答案：
当您确定最优治疗方案后，使用以下格式提交：
<answer>序列</answer>
例如：<answer>SMT</answer>

注意：序列必须是长度为3的由 S、M、T 组成的字符串。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
The clinical multi-stage treatment optimization system requires you to perform "Optimal Treatment Pathway Inference". The rules are as follows:

The treatment process is divided into 3 intervention stages. At each stage, doctors can choose among three interventions: S (Surgery), M (Medication), T (Therapy). A complete 3-stage treatment pathway can be represented by a length-3 symbol sequence, such as SMT, SSS, etc.

Pathway Structure:
- The initial state is stage 0, with a score of 0 (not counted in the total score).
- In each of the following stages (3 stages in total), 3 interventions (S, M, T) are available.
- Any complete pathway goes through exactly 3 stages.

Efficacy Score Rule:
The single-step efficacy score of a specific intervention chosen at a given stage is calculated by:
  v(d, x, prev) = w[x] + Δ[d] + repeat(prev, x) × B

Where:
- d is the current intervention stage (1, 2, or 3).
- x is the currently selected intervention (S, M, or T).
- prev is the intervention of the previous stage (not applicable at stage 1).
- w[S], w[M], w[T] are unknown base efficacy scores for each intervention, ranging from -9 to 9.
- Δ[1] = 0 (known); Δ[2], Δ[3] are unknown stage physiological modifiers, ranging from -5 to 5.
- B is the unknown stacking bonus for consecutively using the same intervention, ranging from -5 to 5.
- repeat(prev, x) = 1 if and only if d >= 2 and prev = x; otherwise 0.

Total Pathway Score Definition:
The total score of a complete treatment pathway (length 3) is the sum of the efficacy scores from the 3 stages along the pathway.

Your Task:
Through queries to the optimization system, infer which 3-stage pathway has the maximum total score (if tied, any optimal pathway is acceptable).

You can make the following three types of queries (submit one at a time):

1. Node Query: Query the single-step efficacy score at a specific intervention node.
   Format: <query_node>sequence</query_node>
   Example: <query_node>S</query_node> or <query_node>SM</query_node> or <query_node>SMT</query_node>
   Sequence length is 1 to 3, composed of S, M, T.
   Response: NODE = integer value

2. Pathway Query: Query the total score of a complete treatment pathway (length 3).
   Format: <query_path>sequence</query_path>
   Example: <query_path>SMT</query_path>
   Sequence length must be 3.
   Response: PATH = integer value

3. Pathway Comparison: Compare the total scores of two complete pathways (both length 3).
   Format: <query_compare>sequenceA,sequenceB</query_compare>
   Example: <query_compare>SMT,SSS</query_compare>
   Response: A>B or A<B or A=B

Query Budget:
You can make at most {max_queries} queries. After exceeding the budget, you can only submit the final answer.

Submit Final Answer:
When you have determined the optimal treatment pathway, submit using the format:
<answer>sequence</answer>
Example: <answer>SMT</answer>

Note: The sequence must be a length-3 string composed of S, M, T.
"""

    contextualized_rule_zh_3 = """\
个性化学习路径设计系统需要您进行"最优学习策略规划"。规则如下：

学习规划包含3个递进的学习模块。在每个模块，学生可以选择三种学习模式：S（Self-study-自主学习）、M（Mentoring-导师辅导）、T（Teamwork-小组协作）。一套完整的3模块学习策略可以用一个长度为3的符号序列表示，例如 SMT、SSS 等。

策略结构：
- 学习前为第0模块，得分为0（不计入总评分）
- 在接下来的每个模块（共3个模块），都有3种学习模式可供选择（S、M、T）
- 任何完整的策略都会经历刚好3个模块

知识掌握度得分规则：
每个模块采用特定学习模式的单步知识掌握度得分由以下公式计算：
  v(d, x, prev) = w[x] + Δ[d] + repeat(prev, x) × B

其中：
- d 表示当前学习模块（1、2 或 3）
- x 表示当前采用的学习模式（S、M 或 T）
- prev 表示上一模块的学习模式（第1模块时不适用）
- w[S]、w[M]、w[T] 是未知的特定学习模式基础掌握度加分，范围在 -9 到 9 之间
- Δ[1] = 0（已知），Δ[2]、Δ[3] 是未知的模块难度修正项，范围在 -5 到 5 之间
- B 是未知的连续采用同类模式的连贯奖励，范围在 -5 到 5 之间
- repeat(prev, x) = 1 当且仅当处于第2或第3模块且 prev = x，否则为 0

策略总得分定义：
一套完整学习策略（经历3个模块）的总得分等于该策略上3个模块的知识掌握度得分之和。

您的任务：
通过向学习规划系统提出查询，推断出哪套3模块策略具有最大总得分（如有并列最大值，任选其一即可）。

您可以提出以下三类查询（每次提交一个查询）：

1. 节点查询：查询某个学习模块采用特定学习模式的单步得分
   格式：<query_node>序列</query_node>
   例如：<query_node>S</query_node> 或 <query_node>SM</query_node> 或 <query_node>SMT</query_node>
   序列长度为1到3，由 S、M、T 组成
   返回：NODE = 整数值

2. 策略查询：查询某套完整学习策略（3个模块）的总得分
   格式：<query_path>序列</query_path>
   例如：<query_path>SMT</query_path>
   序列长度必须为3
   返回：PATH = 整数值

3. 策略比较：比较两套完整学习策略（3个模块）的总得分大小关系
   格式：<query_compare>序列A,序列B</query_compare>
   例如：<query_compare>SMT,SSS</query_compare>
   返回：A>B 或 A<B 或 A=B

查询预算：
您最多可以进行 {max_queries} 次查询。超过预算后只能提交最终答案。

提交最终答案：
当您确定最优学习策略后，使用以下格式提交：
<answer>序列</answer>
例如：<answer>SMT</answer>

注意：序列必须是长度为3的由 S、M、T 组成的字符串。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The personalized learning pathway design system requires you to perform "Optimal Learning Strategy Planning". The rules are as follows:

The learning plan contains 3 progressive learning modules. In each module, students can choose among three learning modes: S (Self-study), M (Mentoring), T (Teamwork). A complete 3-module learning strategy can be represented by a length-3 symbol sequence, such as SMT, SSS, etc.

Strategy Structure:
- The pre-learning state is module 0, with a score of 0 (not counted in the total score).
- In each of the following modules (3 modules in total), 3 learning modes (S, M, T) are available.
- Any complete strategy goes through exactly 3 modules.

Knowledge Mastery Score Rule:
The single-step knowledge mastery score of a specific learning mode chosen at a given module is calculated by:
  v(d, x, prev) = w[x] + Δ[d] + repeat(prev, x) × B

Where:
- d is the current learning module (1, 2, or 3).
- x is the currently selected learning mode (S, M, or T).
- prev is the learning mode of the previous module (not applicable at module 1).
- w[S], w[M], w[T] are unknown base mastery bonuses for each learning mode, ranging from -9 to 9.
- Δ[1] = 0 (known); Δ[2], Δ[3] are unknown module difficulty modifiers, ranging from -5 to 5.
- B is the unknown coherent bonus for consecutively using the same learning mode, ranging from -5 to 5.
- repeat(prev, x) = 1 if and only if d >= 2 and prev = x; otherwise 0.

Total Strategy Score Definition:
The total score of a complete learning strategy (length 3) is the sum of the mastery scores from the 3 modules along the strategy.

Your Task:
Through queries to the planning system, infer which 3-module strategy has the maximum total score (if tied, any optimal strategy is acceptable).

You can make the following three types of queries (submit one at a time):

1. Node Query: Query the single-step mastery score at a specific module.
   Format: <query_node>sequence</query_node>
   Example: <query_node>S</query_node> or <query_node>SM</query_node> or <query_node>SMT</query_node>
   Sequence length is 1 to 3, composed of S, M, T.
   Response: NODE = integer value

2. Strategy Query: Query the total score of a complete learning strategy (length 3).
   Format: <query_path>sequence</query_path>
   Example: <query_path>SMT</query_path>
   Sequence length must be 3.
   Response: PATH = integer value

3. Strategy Comparison: Compare the total scores of two complete learning strategies (both length 3).
   Format: <query_compare>sequenceA,sequenceB</query_compare>
   Example: <query_compare>SMT,SSS</query_compare>
   Response: A>B or A<B or A=B

Query Budget:
You can make at most {max_queries} queries. After exceeding the budget, you can only submit the final answer.

Submit Final Answer:
When you have determined the optimal learning strategy, submit using the format:
<answer>sequence</answer>
Example: <answer>SMT</answer>

Note: The sequence must be a length-3 string composed of S, M, T.
"""

    contextualized_rule_zh_4 = """\
工业生产流水线控制系统需要您进行"最优工艺流程组合优化"。规则如下：

产品加工包含3道前后衔接的工序。在每道工序中，系统可以选择三种工艺：S（Standard-标准加工）、M（Machining-机加工）、T（Thermal-热处理）。一套完整的3道工序流程可以用一个长度为3的符号序列表示，例如 SMT、SSS 等。

流程结构：
- 加工前为第0道工序，质量加分为0（不计入总评分）
- 在接下来的每道工序中（共3道工序），都有3种工艺可供选择（S、M、T）
- 任何完整的流程都会经历刚好3道工序

质量加分规则：
每道工序采用特定工艺的单步质量加分由以下公式计算：
  v(d, x, prev) = w[x] + Δ[d] + repeat(prev, x) × B

其中：
- d 表示当前加工工序（1、2 或 3）
- x 表示当前采用的工艺（S、M 或 T）
- prev 表示上一道工序的工艺（第1道工序时不适用）
- w[S]、w[M]、w[T] 是未知的特定工艺基础质量加分，范围在 -9 到 9 之间
- Δ[1] = 0（已知），Δ[2]、Δ[3] 是未知的工序环境修正项，范围在 -5 到 5 之间
- B 是未知的连续采用同类工艺的工艺协同加成，范围在 -5 到 5 之间
- repeat(prev, x) = 1 当且仅当处于第2或第3道工序且 prev = x，否则为 0

流程总质量分定义：
一套完整工艺流程（经历3道工序）的总质量分等于该流程上3道工序的质量加分之和。

您的任务：
通过向流水线控制系统提出查询，推断出哪套3道工序流程具有最大总质量分（如有并列最大值，任选其一即可）。

您可以提出以下三类查询（每次提交一个查询）：

1. 节点查询：查询某道工序采用特定工艺的单步质量加分
   格式：<query_node>序列</query_node>
   例如：<query_node>S</query_node> 或 <query_node>SM</query_node> 或 <query_node>SMT</query_node>
   序列长度为1到3，由 S、M、T 组成
   返回：NODE = 整数值

2. 流程查询：查询某套完整工艺流程（3道工序）的总质量分
   格式：<query_path>序列</query_path>
   例如：<query_path>SMT</query_path>
   序列长度必须为3
   返回：PATH = 整数值

3. 流程比较：比较两套完整工艺流程（3道工序）的总质量分大小关系
   格式：<query_compare>序列A,序列B</query_compare>
   例如：<query_compare>SMT,SSS</query_compare>
   返回：A>B 或 A<B 或 A=B

查询预算：
您最多可以进行 {max_queries} 次查询。超过预算后只能提交最终答案。

提交最终答案：
当您确定最优工艺流程后，使用以下格式提交：
<answer>序列</answer>
例如：<answer>SMT</answer>

注意：序列必须是长度为3的由 S、M、T 组成的字符串。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
The industrial production line control system requires you to perform "Optimal Process Flow Optimization". The rules are as follows:

Product manufacturing involves 3 sequential operations. At each operation, the system can choose among three processes: S (Standard), M (Machining), T (Thermal). A complete 3-operation flow can be represented by a length-3 symbol sequence, such as SMT, SSS, etc.

Flow Structure:
- The pre-processing state is operation 0, with a score of 0 (not counted in the total score).
- In each of the following operations (3 operations in total), 3 processes (S, M, T) are available.
- Any complete process flow goes through exactly 3 operations.

Quality Bonus Rule:
The single-step quality bonus of a specific process chosen at a given operation is calculated by:
  v(d, x, prev) = w[x] + Δ[d] + repeat(prev, x) × B

Where:
- d is the current operation stage (1, 2, or 3).
- x is the currently selected process (S, M, or T).
- prev is the process of the previous stage (not applicable at operation 1).
- w[S], w[M], w[T] are unknown base quality bonuses for each process, ranging from -9 to 9.
- Δ[1] = 0 (known); Δ[2], Δ[3] are unknown operational environment modifiers, ranging from -5 to 5.
- B is the unknown synergy bonus for consecutively using the same process, ranging from -5 to 5.
- repeat(prev, x) = 1 if and only if d >= 2 and prev = x; otherwise 0.

Total Flow Quality Score Definition:
The total quality score of a complete process flow (length 3) is the sum of the quality bonuses from the 3 operations along the flow.

Your Task:
Through queries to the control system, infer which 3-operation flow has the maximum total quality score (if tied, any optimal flow is acceptable).

You can make the following three types of queries (submit one at a time):

1. Node Query: Query the single-step quality bonus at a specific operation node.
   Format: <query_node>sequence</query_node>
   Example: <query_node>S</query_node> or <query_node>SM</query_node> or <query_node>SMT</query_node>
   Sequence length is 1 to 3, composed of S, M, T.
   Response: NODE = integer value

2. Flow Query: Query the total quality score of a complete process flow (length 3).
   Format: <query_path>sequence</query_path>
   Example: <query_path>SMT</query_path>
   Sequence length must be 3.
   Response: PATH = integer value

3. Flow Comparison: Compare the total quality scores of two complete process flows (both length 3).
   Format: <query_compare>sequenceA,sequenceB</query_compare>
   Example: <query_compare>SMT,SSS</query_compare>
   Response: A>B or A<B or A=B

Query Budget:
You can make at most {max_queries} queries. After exceeding the budget, you can only submit the final answer.

Submit Final Answer:
When you have determined the optimal process flow, submit using the format:
<answer>sequence</answer>
Example: <answer>SMT</answer>

Note: The sequence must be a length-3 string composed of S, M, T.
"""

    contextualized_rule_zh_5 = """\
智能诉讼策略规划系统需要您进行"多阶段最优庭审策略推演"。规则如下：

案件审理分为3个法庭阶段。在每个阶段，您可以运用三种诉讼策略：S（Statutory-制定法抗辩）、M（Motion-提出动议）、T（Testimony-质证）。一套完整的3阶段庭审策略可以用一个长度为3的符号序列表示，例如 SMT、SSS 等。

策略结构：
- 庭审准备为第0阶段，得分为0（不计入总评分）
- 在接下来的每个阶段（共3个阶段），都有3种诉讼策略可供选择（S、M、T）
- 任何完整的庭审策略组合都会经历刚好3个阶段

法庭优势得分规则：
在某个阶段采用特定策略的单步优势得分由以下公式计算：
  v(d, x, prev) = w[x] + Δ[d] + repeat(prev, x) × B

其中：
- d 表示当前庭审阶段（1、2 或 3）
- x 表示当前采用的诉讼策略（S、M 或 T）
- prev 表示上一阶段的诉讼策略（第1阶段时不适用）
- w[S]、w[M]、w[T] 是未知的特定策略基础优势分，范围在 -9 到 9 之间
- Δ[1] = 0（已知），Δ[2]、Δ[3] 是未知的庭审阶段修正项，范围在 -5 到 5 之间
- B 是未知的连续采用同类策略的法庭效力叠加奖励，范围在 -5 到 5 之间
- repeat(prev, x) = 1 当且仅当处于第2或第3阶段且 prev = x，否则为 0

策略总优势得分定义：
一套完整庭审策略组合（经历3个阶段）的总优势得分等于该组合上3个阶段的单步优势得分之和。

您的任务：
通过向策略规划系统提出查询，推断出哪套3阶段策略组合具有最大总优势得分（如有并列最大值，任选其一即可）。

您可以提出以下三类查询（每次提交一个查询）：

1. 节点查询：查询在某个阶段采用特定策略的单步优势得分
   格式：<query_node>序列</query_node>
   例如：<query_node>S</query_node> 或 <query_node>SM</query_node> 或 <query_node>SMT</query_node>
   序列长度为1到3，由 S、M、T 组成
   返回：NODE = 整数值

2. 策略查询：查询某套完整庭审策略（3个阶段）的总优势得分
   格式：<query_path>序列</query_path>
   例如：<query_path>SMT</query_path>
   序列长度必须为3
   返回：PATH = 整数值

3. 策略比较：比较两套完整庭审策略（3个阶段）的总优势得分大小关系
   格式：<query_compare>序列A,序列B</query_compare>
   例如：<query_compare>SMT,SSS</query_compare>
   返回：A>B 或 A<B 或 A=B

查询预算：
您最多可以进行 {max_queries} 次查询。超过预算后只能提交最终答案。

提交最终答案：
当您确定最优庭审策略后，使用以下格式提交：
<answer>序列</answer>
例如：<answer>SMT</answer>

注意：序列必须是长度为3的由 S、M、T 组成的字符串。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
The smart litigation strategy planning system requires you to perform "Optimal Trial Strategy Deduction". The rules are as follows:

The trial process is divided into 3 court stages. At each stage, you can adopt three litigation strategies: S (Statutory), M (Motion), T (Testimony). A complete 3-stage trial strategy can be represented by a length-3 symbol sequence, such as SMT, SSS, etc.

Strategy Structure:
- The pre-trial state is stage 0, with a score of 0 (not counted in the total score).
- In each of the following stages (3 stages in total), 3 litigation strategies (S, M, T) are available.
- Any complete trial strategy goes through exactly 3 stages.

Court Advantage Score Rule:
The single-step advantage score of a specific strategy adopted at a given stage is calculated by:
  v(d, x, prev) = w[x] + Δ[d] + repeat(prev, x) × B

Where:
- d is the current trial stage (1, 2, or 3).
- x is the currently adopted strategy (S, M, or T).
- prev is the strategy of the previous stage (not applicable at stage 1).
- w[S], w[M], w[T] are unknown base advantage scores for each strategy, ranging from -9 to 9.
- Δ[1] = 0 (known); Δ[2], Δ[3] are unknown trial stage modifiers, ranging from -5 to 5.
- B is the unknown stacking bonus for consecutively using the same strategy, ranging from -5 to 5.
- repeat(prev, x) = 1 if and only if d >= 2 and prev = x; otherwise 0.

Total Strategy Advantage Score Definition:
The total advantage score of a complete trial strategy (length 3) is the sum of the advantage scores from the 3 stages along the strategy.

Your Task:
Through queries to the planning system, infer which 3-stage strategy has the maximum total advantage score (if tied, any optimal strategy is acceptable).

You can make the following three types of queries (submit one at a time):

1. Node Query: Query the single-step advantage score of a specific strategy node.
   Format: <query_node>sequence</query_node>
   Example: <query_node>S</query_node> or <query_node>SM</query_node> or <query_node>SMT</query_node>
   Sequence length is 1 to 3, composed of S, M, T.
   Response: NODE = integer value

2. Strategy Query: Query the total advantage score of a complete trial strategy (length 3).
   Format: <query_path>sequence</query_path>
   Example: <query_path>SMT</query_path>
   Sequence length must be 3.
   Response: PATH = integer value

3. Strategy Comparison: Compare the total advantage scores of two complete trial strategies (both length 3).
   Format: <query_compare>sequenceA,sequenceB</query_compare>
   Example: <query_compare>SMT,SSS</query_compare>
   Response: A>B or A<B or A=B

Query Budget:
You can make at most {max_queries} queries. After exceeding the budget, you can only submit the final answer.

Submit Final Answer:
When you have determined the optimal trial strategy, submit using the format:
<answer>sequence</answer>
Example: <answer>SMT</answer>

Note: The sequence must be a length-3 string composed of S, M, T.
"""

    tags = ["answer", "query_node", "query_path", "query_compare"]
    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "max_queries": 10,
                "w": {"S": 5, "M": 3, "T": 1},
                "delta": {1: 0, 2: 0, 3: 0},
                "B": 0,
            },
            2: {
                "max_queries": 10,
                "w": {"S": 4, "M": 5, "T": 3},
                "delta": {1: 0, 2: 1, 3: 2},
                "B": 1,
            },
            3: {
                "max_queries": 8,
                "w": {"S": -2, "M": 6, "T": 4},
                "delta": {1: 0, 2: -1, 3: 3},
                "B": 2,
            },
            4: {
                "max_queries": 8,
                "w": {"S": 3, "M": -1, "T": 5},
                "delta": {1: 0, 2: 3, 3: -2},
                "B": 4,
            },
            5: {
                "max_queries": 6,
                "w": {"S": -3, "M": 7, "T": 2},
                "delta": {1: 0, 2: -3, 3: 4},
                "B": -3,
            },
        },
        "en": {
            1: {
                "max_queries": 10,
                "w": {"S": 5, "M": 3, "T": 1},
                "delta": {1: 0, 2: 0, 3: 0},
                "B": 0,
            },
            2: {
                "max_queries": 10,
                "w": {"S": 4, "M": 5, "T": 3},
                "delta": {1: 0, 2: 1, 3: 2},
                "B": 1,
            },
            3: {
                "max_queries": 8,
                "w": {"S": -2, "M": 6, "T": 4},
                "delta": {1: 0, 2: -1, 3: 3},
                "B": 2,
            },
            4: {
                "max_queries": 8,
                "w": {"S": 3, "M": -1, "T": 5},
                "delta": {1: 0, 2: 3, 3: -2},
                "B": 4,
            },
            5: {
                "max_queries": 6,
                "w": {"S": -3, "M": 7, "T": 2},
                "delta": {1: 0, 2: -3, 3: 4},
                "B": -3,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏参数和节点值"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 设置查询预算
        self.max_queries = cfg["max_queries"]
        self.query_count = 0
        self._game_info["max_queries"] = self.max_queries
        
        # 设置未知参数
        self.w = cfg["w"]  # w[S], w[M], w[T]
        self.delta = cfg["delta"]  # delta[1]=0, delta[2], delta[3]
        self.B = cfg["B"]  # 连续同符号奖励
        
        # 预计算所有节点的值
        self.node_values = {}
        self._compute_all_node_values()
        
        # 计算所有路径的值并找到最优路径
        self.path_values = {}
        self._compute_all_path_values()
        self._find_optimal_path()

    def _compute_node_value(self, sequence):
        """计算给定序列对应节点的值"""
        if len(sequence) == 0:
            return 0  # 根节点
        
        depth = len(sequence)
        x = sequence[-1]  # 当前符号
        prev = sequence[-2] if depth >= 2 else None  # 前一个符号
        
        # v(d, x, prev) = w[x] + Δ[d] + repeat(prev, x) × B
        value = self.w[x] + self.delta[depth]
        if prev is not None and prev == x:
            value += self.B
            
        return value

    def _compute_all_node_values(self):
        """预计算所有节点的值"""
        symbols = ['S', 'M', 'T']
        
        # 根节点
        self.node_values[''] = 0
        
        # 深度1节点
        for s1 in symbols:
            seq = s1
            self.node_values[seq] = self._compute_node_value(seq)
        
        # 深度2节点
        for s1 in symbols:
            for s2 in symbols:
                seq = s1 + s2
                self.node_values[seq] = self._compute_node_value(seq)
        
        # 深度3节点（叶子节点）
        for s1 in symbols:
            for s2 in symbols:
                for s3 in symbols:
                    seq = s1 + s2 + s3
                    self.node_values[seq] = self._compute_node_value(seq)

    def _compute_all_path_values(self):
        """计算所有长度为3的路径的总值"""
        symbols = ['S', 'M', 'T']
        
        for s1 in symbols:
            for s2 in symbols:
                for s3 in symbols:
                    path = s1 + s2 + s3
                    # 路径值 = 深度1节点 + 深度2节点 + 深度3节点
                    value = (self.node_values[s1] + 
                            self.node_values[s1 + s2] + 
                            self.node_values[s1 + s2 + s3])
                    self.path_values[path] = value

    def _find_optimal_path(self):
        """找到最优路径（最大值）"""
        max_value = max(self.path_values.values())
        self.optimal_paths = [path for path, val in self.path_values.items() if val == max_value]
        self.optimal_value = max_value

    def evaluate(self, parsed_info):
        """评估提交的答案是否正确"""
        answer = parsed_info["answer"].strip().upper()
        
        # 检查格式：长度为3，由S、M、T组成
        if len(answer) != 3:
            return False
        if not all(c in ['S', 'M', 'T'] for c in answer):
            return False
        
        # 检查是否是最优路径之一
        return answer in self.optimal_paths

    def _cf_core_produce(self, parsed_info):
        """原始的响应生成逻辑"""
        # 检查是否超出查询预算
        if self.query_count >= self.max_queries:
            if self.config.language == "zh":
                return "查询预算已用完，请提交最终答案。"
            else:
                return "Query budget exhausted. Please submit your final answer."
        
        # 优先级：query_node > query_path > query_compare
        if "query_node" in parsed_info:
            sequence = parsed_info["query_node"].strip().upper()
            
            # 验证序列格式
            if not all(c in ['S', 'M', 'T'] for c in sequence):
                if self.config.language == "zh":
                    return "错误：序列只能包含 S、M、T。"
                else:
                    return "Error: Sequence can only contain S, M, T."
            
            if len(sequence) < 1 or len(sequence) > 3:
                if self.config.language == "zh":
                    return "错误：序列长度必须为1到3。"
                else:
                    return "Error: Sequence length must be 1 to 3."
            
            self.query_count += 1
            # 返回节点值
            value = self.node_values[sequence]
            return f"NODE = {value}"
        
        elif "query_path" in parsed_info:
            sequence = parsed_info["query_path"].strip().upper()
            
            # 验证序列格式
            if not all(c in ['S', 'M', 'T'] for c in sequence):
                if self.config.language == "zh":
                    return "错误：序列只能包含 S、M、T。"
                else:
                    return "Error: Sequence can only contain S, M, T."
            
            if len(sequence) != 3:
                if self.config.language == "zh":
                    return "错误：路径序列长度必须为3。"
                else:
                    return "Error: Path sequence length must be 3."
            
            self.query_count += 1
            # 返回路径值
            value = self.path_values[sequence]
            return f"PATH = {value}"
        
        elif "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"].strip().upper()
                raw = raw.replace("，", ",")
                parts = [p.strip() for p in raw.split(",")]
                
                if len(parts) != 2:
                    raise ValueError("Must compare exactly two paths")
                
                seq_a, seq_b = parts
                
                # 验证两个序列的格式
                if len(seq_a) != 3 or len(seq_b) != 3:
                    raise ValueError("Both sequences must have length 3")
                
                if not all(c in ['S', 'M', 'T'] for c in seq_a):
                    raise ValueError("Sequence A contains invalid characters")
                
                if not all(c in ['S', 'M', 'T'] for c in seq_b):
                    raise ValueError("Sequence B contains invalid characters")
                
                self.query_count += 1
                
                # 比较路径值
                val_a = self.path_values[seq_a]
                val_b = self.path_values[seq_b]
                
                if val_a > val_b:
                    return "A>B"
                elif val_a < val_b:
                    return "A<B"
                else:
                    return "A=B"
                    
            except Exception as e:
                if self.config.language == "zh":
                    return "错误：比较查询格式无效。应为 <query_compare>序列A,序列B</query_compare>"
                else:
                    return "Error: Invalid comparison query format. Should be <query_compare>seqA,seqB</query_compare>"
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        """根据正确答案生成错误的答案（确定性方式）"""
        correct_str = str(correct).strip()
        
        # NODE = X 格式
        node_match = re.match(r'^NODE\s*=\s*(-?\d+)$', correct_str)
        if node_match:
            val = int(node_match.group(1))
            return f"NODE = {val + 1}"
        
        # PATH = X 格式
        path_match = re.match(r'^PATH\s*=\s*(-?\d+)$', correct_str)
        if path_match:
            val = int(path_match.group(1))
            return f"PATH = {val + 1}"
        
        # 比较结果 A>B, A<B, A=B
        if correct_str == "A>B":
            return "A<B"
        elif correct_str == "A<B":
            return "A>B"
        elif correct_str == "A=B":
            return "A>B"
        
        # 纯整数
        if correct_str.lstrip('-').isdigit():
            return str(int(correct_str) + 1)
        
        # 关键词替换
        if self.config.language == "zh":
            if "是" in correct_str:
                return correct_str.replace("是", "否")
            if "否" in correct_str:
                return correct_str.replace("否", "是")
        else:
            lower_str = correct_str.lower()
            if "yes" in lower_str:
                return re.sub(r'yes', 'No', correct_str, flags=re.IGNORECASE)
            if "no" in lower_str:
                return re.sub(r'no', 'Yes', correct_str, flags=re.IGNORECASE)
        
        # 默认情况：追加 _WRONG
        return correct_str + "_WRONG"

    def get_all_possible_queries(self) -> List[Dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串，与游戏中 parsed_info["query"] 的值格式一致
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        queries = []
        symbols = ['S', 'M', 'T']
        
        # 1. 节点查询 (深度1-3)
        # 生成所有可能的节点序列
        node_sequences = []
        # Depth 1
        for s1 in symbols:
            node_sequences.append(s1)
        # Depth 2
        for s1 in symbols:
            for s2 in symbols:
                node_sequences.append(s1 + s2)
        # Depth 3
        for s1 in symbols:
            for s2 in symbols:
                for s3 in symbols:
                    node_sequences.append(s1 + s2 + s3)
        
        for seq in node_sequences:
            queries.append({
                "query": f"<query_node>{seq}</query_node>",
                "answer": f"NODE = {self.node_values[seq]}"
            })

        # 2. 路径查询 (仅深度3)
        path_sequences = []
        for s1 in symbols:
            for s2 in symbols:
                for s3 in symbols:
                    path_sequences.append(s1 + s2 + s3)
        
        for seq in path_sequences:
            queries.append({
                "query": f"<query_path>{seq}</query_path>",
                "answer": f"PATH = {self.path_values[seq]}"
            })

        # 3. 路径比较 (去掉自身比较，只保留 seq_a < seq_b 的有序对以减少数量)
        for i, seq_a in enumerate(path_sequences):
            for j, seq_b in enumerate(path_sequences):
                if i >= j:
                    continue  # 跳过自身比较和重复对
                val_a = self.path_values[seq_a]
                val_b = self.path_values[seq_b]
                
                if val_a > val_b:
                    res = "A>B"
                elif val_a < val_b:
                    res = "A<B"
                else:
                    res = "A=B"
                
                queries.append({
                    "query": f"<query_compare>{seq_a},{seq_b}</query_compare>",
                    "answer": res
                })

        return queries