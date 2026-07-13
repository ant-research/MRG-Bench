# -*- coding: utf-8 -*-
# 自动生成
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   遍历相对顺序：两个节点在某种遍历下谁先被访问
# ============================================================

from .base import Game
import re
import itertools


class TreeTraversalDeductionGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"树遍历规则推理"游戏。规则如下：

游戏设定了一棵有序根树，节点与其子节点的固定顺序如下（方括号内为子节点从左到右的顺序）：
{tree_structure}

我已秘密选定了一种遍历规则，该规则从以下四种候选方案中选择：
- 方案A：深度优先先序遍历，子节点按从左到右访问
- 方案B：深度优先先序遍历，子节点按从右到左访问
- 方案C：深度优先后序遍历，子节点按从左到右访问
- 方案D：广度优先遍历，按层从上到下，同层内从左到右

"访问"是指遍历过程中处理该节点的时刻。"X先于Y"表示在遍历序列中X的访问时刻早于Y。

你的目标是通过提问推断出真实的遍历规则。

## 游戏流程

1. **提问阶段**：你可以提出至多{max_queries}个问题，询问"节点X是否先于节点Y被访问？"
   - 每次提问必须指定两个不同的节点
   - 节点必须在集合 {node_set} 中
   - 我会回答"是"或"否"
   - 格式错误或违反约束的提问视为无效

2. **提交推断**：当你收集足够信息后，提交你认为的遍历规则（A、B、C或D）
   - 必须在提交推断前进行至少{min_queries}次有效提问
   - 若推断错误且仍有剩余提问次数，可继续提问后再次提交

3. **最终验证**：推断正确后，我会给出两对你未直接比较过的节点对
   - 对每一对节点，你需要判断哪个节点先被访问
   - 两对判断均正确则游戏成功

## 格式要求

每次只能包含一个标签。请使用以下XML格式：

- 提问节点顺序（例如询问节点R和节点A的顺序）：
<query_order>R,A</query_order>

- 提交遍历规则推断（例如推断为方案A）：
<submit_rule>A</submit_rule>

- 最终验证阶段回答节点顺序（例如第一对选择U1，第二对选择V2）：
<final_answer>U1,V2</final_answer>

## 失败条件

- 在{max_queries}次有效提问内未能正确提交推断
- 正确提交推断后，最终验证的两对判断中任一错误
- 累计三次违反提问约束或格式错误
"""

    game_rule_en = """\
Let's play a "Tree Traversal Deduction" game. Here are the rules:

The game has an ordered rooted tree with nodes and their children in fixed order (brackets show children from left to right):
{tree_structure}

I have secretly selected a traversal rule from four candidate schemes:
- Scheme A: Depth-First Preorder, children visited left-to-right
- Scheme B: Depth-First Preorder, children visited right-to-left
- Scheme C: Depth-First Postorder, children visited left-to-right
- Scheme D: Breadth-First, level-by-level top-to-bottom, same level left-to-right

"Visit" means the moment a node is processed during traversal. "X before Y" means X is visited earlier than Y in the traversal sequence.

Your goal is to deduce the true traversal rule through queries.

## Game Flow

1. **Query Phase**: You can ask up to {max_queries} questions: "Is node X visited before node Y?"
   - Each query must specify two different nodes
   - Nodes must be from the set {node_set}
   - I will answer "Yes" or "No"
   - Invalid format or constraint violations count as errors

2. **Submit Inference**: When you have enough information, submit your inferred rule (A, B, C, or D)
   - You must make at least {min_queries} valid queries before submitting
   - If incorrect and queries remain, you may continue querying and resubmit

3. **Final Verification**: After correct inference, I will provide two node pairs you haven't directly compared
   - For each pair, judge which node is visited first
   - Success requires both judgments to be correct

## Format Requirements

Each turn must contain only one tag. Use the following XML format:

- Query node order (e.g., asking about nodes R and A):
<query_order>R,A</query_order>

- Submit rule inference (e.g., inferring scheme A):
<submit_rule>A</submit_rule>

- Final verification answer (e.g., choosing U1 for first pair, V2 for second pair):
<final_answer>U1,V2</final_answer>

## Failure Conditions

- Unable to correctly submit inference within {max_queries} valid queries
- After correct inference, any error in the two final verification judgments
- Three accumulated constraint violations or format errors
"""

    # 场景 1：交通
    contextualized_rule_zh_1 = """\
欢迎使用“智能路网巡逻策略排查系统”。当前排查的交通枢纽层级网络如下（方括号内为下级路口从左到右的顺序）：
{tree_structure}

系统秘密采用了一种自动巡逻路线生成规则，从以下四种预设方案中选择：
- 方案A：主路优先深度巡逻，分支路口按从左到右排查
- 方案B：主路优先深度巡逻，分支路口按从右到左排查
- 方案C：末端分支优先巡逻，完成后返回主路（后序），从左到右排查
- 方案D：按路网层级广度优先巡逻，同层级内从左到右

“排查”是指巡逻车到达并处理该路口的时刻。“X先于Y”表示在巡逻序列中X的排查时刻早于Y。

你的目标是通过调取监控记录，推断出系统当前运行的真实巡逻规则。

## 系统操作流程

1. **监控调取阶段**：你可以提交至多{max_queries}次查询，询问“路口X是否先于路口Y被排查？”
   - 每次查询必须指定两个不同的路口节点
   - 节点必须在合法集合 {node_set} 中
   - 系统将反馈“是”或“否”
   - 格式错误或违反约束的查询视为无效

2. **提交推断**：当你收集足够情报后，提交你认为的巡逻规则（A、B、C或D）
   - 必须在提交推断前进行至少{min_queries}次有效查询
   - 若推断错误且仍有剩余查询次数，可继续查询后再次提交

3. **最终验证**：推断正确后，系统会给出两对你未直接比对过的路口对
   - 对每一对路口，你需要判断哪个路口先被排查
   - 两对判断均正确则排查任务成功

## 格式要求

每次只能包含一个标签。请使用以下XML格式：

- 调取路口排查顺序（例如询问路口R和路口A的顺序）：
<query_order>R,A</query_order>

- 提交巡逻规则推断（例如推断为方案A）：
<submit_rule>A</submit_rule>

- 最终验证阶段回答路口顺序（例如第一对选择U1，第二对选择V2）：
<final_answer>U1,V2</final_answer>

## 失败条件

- 在{max_queries}次有效查询内未能正确提交推断
- 正确提交推断后，最终验证的两对判断中任一错误
- 累计三次违反查询约束或格式错误
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Smart Road Network Patrol Strategy System". The hierarchical traffic routing network is as follows (brackets show downstream intersections from left to right):
{tree_structure}

The system has secretly adopted an automated patrol route generation rule, selected from four preset schemes:
- Scheme A: Main route priority depth-first patrol, branch intersections processed left-to-right
- Scheme B: Main route priority depth-first patrol, branch intersections processed right-to-left
- Scheme C: Terminal branches priority patrol, returning to main route later (postorder), left-to-right
- Scheme D: Level-by-level breadth-first patrol, same level processed left-to-right

"Process" means the moment a patrol vehicle arrives at and handles the intersection. "X before Y" means X is processed earlier than Y in the patrol sequence.

Your goal is to deduce the true patrol rule currently running in the system by checking surveillance records.

## System Operation Flow

1. **Surveillance Query Phase**: You can submit up to {max_queries} queries: "Is intersection X processed before intersection Y?"
   - Each query must specify two different intersection nodes
   - Nodes must be from the valid set {node_set}
   - The system will answer "Yes" or "No"
   - Invalid format or constraint violations count as errors

2. **Submit Inference**: When you have collected enough intelligence, submit your inferred patrol rule (A, B, C, or D)
   - You must make at least {min_queries} valid queries before submitting
   - If incorrect and queries remain, you may continue querying and resubmit

3. **Final Verification**: After a correct inference, the system will provide two intersection pairs you haven't directly compared
   - For each pair, judge which intersection is processed first
   - Success requires both judgments to be correct

## Format Requirements

Each turn must contain only one tag. Use the following XML format:

- Query intersection process order (e.g., asking about intersections R and A):
<query_order>R,A</query_order>

- Submit patrol rule inference (e.g., inferring Scheme A):
<submit_rule>A</submit_rule>

- Final verification answer (e.g., choosing U1 for first pair, V2 for second pair):
<final_answer>U1,V2</final_answer>

## Failure Conditions

- Unable to correctly submit inference within {max_queries} valid queries
- After correct inference, any error in the two final verification judgments
- Three accumulated constraint violations or format errors
"""

    # 场景 2：医疗
    contextualized_rule_zh_2 = """\
欢迎进入“临床路径诊断推理系统”。当前患者的诊断决策树如下（方括号内为后续检查项目从左到右的顺序）：
{tree_structure}

系统秘密采用了一种临床诊断排查规则，从以下四种候选方案中选择：
- 方案A：深度优先逐项检查，同级子项目按从左到右执行
- 方案B：深度优先逐项检查，同级子项目按从右到左执行
- 方案C：底层具体项目优先排查（后序），再进行综合诊断，从左到右执行
- 方案D：广度优先按诊断层级推进，同层级内从左到右执行

“执行”是指在临床路径中实际开展该检查项目的时刻。“X先于Y”表示在诊断序列中X的执行时刻早于Y。

你的目标是通过调阅诊疗记录，推推断出真实的诊断排查规则。

## 系统操作流程

1. **记录调阅阶段**：你可以提出至多{max_queries}次查询，询问“检查项目X是否先于项目Y执行？”
   - 每次查询必须指定两个不同的检查项目节点
   - 节点必须在集合 {node_set} 中
   - 系统将反馈“是”或“否”
   - 格式错误或违反约束的查询视为无效

2. **提交推断**：当你收集足够信息后，提交你推断的诊断规则（A、B、C或D）
   - 必须在提交推断前进行至少{min_queries}次有效查询
   - 若推断错误且仍有剩余查询次数，可继续查询后再次提交

3. **最终验证**：推断正确后，系统会给出两对他未直接对比过的项目对
   - 对每一对项目，你需要判断哪个项目先被执行
   - 两对判断均正确则诊断推理成功

## 格式要求

每次只能包含一个标签。请使用以下XML格式：

- 调阅项目执行顺序（例如询问项目R和项目A的顺序）：
<query_order>R,A</query_order>

- 提交诊断规则推断（例如推断为方案A）：
<submit_rule>A</submit_rule>

- 最终验证阶段回答项目顺序（例如第一对选择U1，第二对选择V2）：
<final_answer>U1,V2</final_answer>

## 失败条件

- 在{max_queries}次有效查询内未能正确提交推断
- 正确提交推断后，最终验证的两对判断中任一错误
- 累计三次违反查询约束或格式错误
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Clinical Pathway Diagnostic Deduction System". The patient's diagnostic decision tree is as follows (brackets show downstream diagnostic steps from left to right):
{tree_structure}

The system has secretly adopted a clinical diagnostic screening rule, selected from four candidate schemes:
- Scheme A: Depth-first step-by-step examination, sub-steps executed left-to-right
- Scheme B: Depth-first step-by-step examination, sub-steps executed right-to-left
- Scheme C: Bottom-level specific tests first (postorder) before comprehensive diagnosis, left-to-right
- Scheme D: Breadth-first level-by-level screening, same level executed left-to-right

"Execute" means the moment a diagnostic step is actually conducted in the clinical pathway. "X before Y" means X is executed earlier than Y in the diagnostic sequence.

Your goal is to deduce the true diagnostic screening rule by reviewing medical records.

## System Operation Flow

1. **Record Review Phase**: You can submit up to {max_queries} queries: "Is diagnostic step X executed before step Y?"
   - Each query must specify two different diagnostic step nodes
   - Nodes must be from the valid set {node_set}
   - The system will answer "Yes" or "No"
   - Invalid format or constraint violations count as errors

2. **Submit Inference**: When you have collected enough information, submit your inferred diagnostic rule (A, B, C, or D)
   - You must make at least {min_queries} valid queries before submitting
   - If incorrect and queries remain, you may continue querying and resubmit

3. **Final Verification**: After correct inference, the system will provide two step pairs you haven't directly compared
   - For each pair, judge which step is executed first
   - Success requires both judgments to be correct

## Format Requirements

Each turn must contain only one tag. Use the following XML format:

- Query step execution order (e.g., asking about steps R and A):
<query_order>R,A</query_order>

- Submit diagnostic rule inference (e.g., inferring Scheme A):
<submit_rule>A</submit_rule>

- Final verification answer (e.g., choosing U1 for first pair, V2 for second pair):
<final_answer>U1,V2</final_answer>

## Failure Conditions

- Unable to correctly submit inference within {max_queries} valid queries
- After correct inference, any error in the two final verification judgments
- Three accumulated constraint violations or format errors
"""

    # 场景 3：教育
    contextualized_rule_zh_3 = """\
欢迎使用“自适应教学顺序逆向分析系统”。当前的知识点层级体系如下（方括号内为子知识点从左到右的顺序）：
{tree_structure}

系统秘密采用了一种教学进度规划规则，从以下四种候选方案中选择：
- 方案A：核心概念优先，随后深入子知识点，按从左到右讲授
- 方案B：核心概念优先，随后深入子知识点，按从右到左讲授
- 方案C：先掌握所有子知识点，再总结核心概念（后序），从左到右推进
- 方案D：按知识层级广度优先讲授，同层级内从左到右推进

“讲授”是指在课堂上实际教授该知识点的时刻。“X先于Y”表示在教学序列中X的讲授时刻早于Y。

你的目标是通过分析随堂测试记录，推断出真实的教学顺序规则。

## 系统操作流程

1. **记录分析阶段**：你可以提出至多{max_queries}次查询，询问“知识点X是否先于知识点Y被讲授？”
   - 每次查询必须指定两个不同的知识点节点
   - 节点必须在集合 {node_set} 中
   - 系统将反馈“是”或“否”
   - 格式错误或违反约束的查询视为无效

2. **提交推断**：当你收集足够信息后，提交你推断的教学规则（A、B、C或D）
   - 必须在提交推断前进行至少{min_queries}次有效查询
   - 若推断错误且仍有剩余查询次数，可继续查询后再次提交

3. **最终验证**：推断正确后，系统会给出两对你未直接对比过的知识点对
   - 对每一对知识点，你需要判断哪个知识点先被讲授
   - 两对判断均正确则分析任务成功

## 格式要求

每次只能包含一个标签。请使用以下XML格式：

- 查询讲授顺序（例如询问知识点R和知识点A的顺序）：
<query_order>R,A</query_order>

- 提交教学规则推断（例如推断为方案A）：
<submit_rule>A</submit_rule>

- 最终验证阶段回答知识点顺序（例如第一对选择U1，第二对选择V2）：
<final_answer>U1,V2</final_answer>

## 失败条件

- 在{max_queries}次有效查询内未能正确提交推断
- 正确提交推断后，最终验证的两对判断中任一错误
- 累计三次违反查询约束或格式错误
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Adaptive Teaching Sequence Reverse-Analysis System". The current knowledge concept hierarchy is as follows (brackets show sub-concepts from left to right):
{tree_structure}

The system has secretly adopted a teaching schedule rule, selected from four candidate schemes:
- Scheme A: Core concept first, then dive into sub-concepts left-to-right
- Scheme B: Core concept first, then dive into sub-concepts right-to-left
- Scheme C: Master sub-concepts before summarizing the core concept (postorder), left-to-right
- Scheme D: Breadth-first teaching by knowledge level, same level taught left-to-right

"Teach" means the moment a knowledge concept is actually instructed in class. "X before Y" means X is taught earlier than Y in the teaching sequence.

Your goal is to deduce the true teaching sequence rule by analyzing quiz records.

## System Operation Flow

1. **Record Analysis Phase**: You can submit up to {max_queries} queries: "Is concept X taught before concept Y?"
   - Each query must specify two different concept nodes
   - Nodes must be from the valid set {node_set}
   - The system will answer "Yes" or "No"
   - Invalid format or constraint violations count as errors

2. **Submit Inference**: When you have enough information, submit your inferred teaching rule (A, B, C, or D)
   - You must make at least {min_queries} valid queries before submitting
   - If incorrect and queries remain, you may continue querying and resubmit

3. **Final Verification**: After correct inference, the system will provide two concept pairs you haven't directly compared
   - For each pair, judge which concept is taught first
   - Success requires both judgments to be correct

## Format Requirements

Each turn must contain only one tag. Use the following XML format:

- Query teaching order (e.g., asking about concepts R and A):
<query_order>R,A</query_order>

- Submit teaching rule inference (e.g., inferring Scheme A):
<submit_rule>A</submit_rule>

- Final verification answer (e.g., choosing U1 for first pair, V2 for second pair):
<final_answer>U1,V2</final_answer>

## Failure Conditions

- Unable to correctly submit inference within {max_queries} valid queries
- After correct inference, any error in the two final verification judgments
- Three accumulated constraint violations or format errors
"""

    # 场景 4：制造业/工业
    contextualized_rule_zh_4 = """\
欢迎进入“自动化装配工序溯源系统”。当前产品的物料清单(BOM)装配树如下（方括号内为子组件从左到右的顺序）：
{tree_structure}

系统秘密采用了一种自动化装配调度规则，从以下四种候选方案中选择：
- 方案A：自顶向下分解装配，子组件按从左到右组装处理
- 方案B：自顶向下分解装配，子组件按从右到左组装处理
- 方案C：自底向上装配，完成所有子组件后再组装主件（后序），从左到右推进
- 方案D：按BOM层级广度优先阶段性推进，同层级内从左到右处理

“处理”是指流水线上实际加工或组装该组件的时刻。“X先于Y”表示在工序序列中X的处理时刻早于Y。

你的目标是通过查询流水线日志，推断出真实的装配工序规则。

## 系统操作流程

1. **日志查询阶段**：你可以提出至多{max_queries}次查询，询问“组件X是否先于组件Y被处理？”
   - 每次查询必须指定两个不同的组件节点
   - 节点必须在集合 {node_set} 中
   - 系统将反馈“是”或“否”
   - 格式错误或违反约束的查询视为无效

2. **提交推断**：当你收集足够信息后，提交你推断的装配规则（A、B、C或D）
   - 必须在提交推断前进行至少{min_queries}次有效查询
   - 若推断错误且仍有剩余查询次数，可继续查询后再次提交

3. **最终验证**：推断正确后，系统会给出两对你未直接对比过的组件对
   - 对每一对组件，你需要判断哪个组件先被处理
   - 两对判断均正确则溯源任务成功

## 格式要求

每次只能包含一个标签。请使用以下XML格式：

- 查询工序先后顺序（例如询问组件R和组件A的顺序）：
<query_order>R,A</query_order>

- 提交装配规则推断（例如推断为方案A）：
<submit_rule>A</submit_rule>

- 最终验证阶段回答组件顺序（例如第一对选择U1，第二对选择V2）：
<final_answer>U1,V2</final_answer>

## 失败条件

- 在{max_queries}次有效查询内未能正确提交推断
- 正确提交推断后，最终验证的两对判断中任一错误
- 累计三次违反查询约束或格式错误
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Automated Assembly Process Traceability System". The product's Bill of Materials (BOM) assembly tree is as follows (brackets show sub-components from left to right):
{tree_structure}

The system has secretly adopted an automated assembly scheduling rule, selected from four candidate schemes:
- Scheme A: Top-down breakdown assembly, sub-components processed left-to-right
- Scheme B: Top-down breakdown assembly, sub-components processed right-to-left
- Scheme C: Bottom-up assembly, finishing all sub-components before the main assembly (postorder), left-to-right
- Scheme D: Phased breadth-first processing by BOM level, same level processed left-to-right

"Process" means the moment a component is actually machined or assembled on the production line. "X before Y" means X is processed earlier than Y in the workflow sequence.

Your goal is to deduce the true assembly sequence rule by querying the production line logs.

## System Operation Flow

1. **Log Query Phase**: You can submit up to {max_queries} queries: "Is component X processed before component Y?"
   - Each query must specify two different component nodes
   - Nodes must be from the valid set {node_set}
   - The system will answer "Yes" or "No"
   - Invalid format or constraint violations count as errors

2. **Submit Inference**: When you have enough information, submit your inferred assembly rule (A, B, C, or D)
   - You must make at least {min_queries} valid queries before submitting
   - If incorrect and queries remain, you may continue querying and resubmit

3. **Final Verification**: After correct inference, the system will provide two component pairs you haven't directly compared
   - For each pair, judge which component is processed first
   - Success requires both judgments to be correct

## Format Requirements

Each turn must contain only one tag. Use the following XML format:

- Query processing order (e.g., asking about components R and A):
<query_order>R,A</query_order>

- Submit assembly rule inference (e.g., inferring Scheme A):
<submit_rule>A</submit_rule>

- Final verification answer (e.g., choosing U1 for first pair, V2 for second pair):
<final_answer>U1,V2</final_answer>

## Failure Conditions

- Unable to correctly submit inference within {max_queries} valid queries
- After correct inference, any error in the two final verification judgments
- Three accumulated constraint violations or format errors
"""

    # 场景 5：法律
    contextualized_rule_zh_5 = """\
欢迎进入“司法证据链逻辑审查系统”。当前案件的法理逻辑树如下（方括号内为下级证据点/条款从左到右的顺序）：
{tree_structure}

系统秘密采用了一种逻辑审查推进规则，从以下四种候选方案中选择：
- 方案A：主导原则优先审查，随后逐条深入具体细节，按从左到右排查
- 方案B：主导原则优先审查，随后逐条深入具体细节，按从右到左排查
- 方案C：先确证所有底层细节，再确立主导原则（后序），从左到右推进
- 方案D：按逻辑层级广度优先审查，同层级事实证据从左到右排查

“审查”是指合议庭在卷宗中实际核对该证据点/条款的时刻。“X先于Y”表示在审查序列中X的核对时刻早于Y。

你的目标是通过调阅庭审笔录，推断出真实的审查逻辑规则。

## 系统操作流程

1. **笔录调阅阶段**：你可以提出至多{max_queries}次查询，询问“证据点X是否先于证据点Y被审查？”
   - 每次查询必须指定两个不同的证据节点
   - 节点必须在集合 {node_set} 中
   - 系统将反馈“是”或“否”
   - 格式错误或违反约束的查询视为无效

2. **提交推断**：当你收集足够信息后，提交你推断的审查规则（A、B、C或D）
   - 必须在提交推断前进行至少{min_queries}次有效查询
   - 若推断错误且仍有剩余查询次数，可继续查询后再次提交

3. **最终验证**：推断正确后，系统会给出两对你未直接对比过的证据点对
   - 对每一对证据点，你需要判断哪个证据点先被审查
   - 两对判断均正确则逻辑溯源成功

## 格式要求

每次只能包含一个标签。请使用以下XML格式：

- 查询审查先后顺序（例如询问证据点R和证据点A的顺序）：
<query_order>R,A</query_order>

- 提交审查规则推断（例如推断为方案A）：
<submit_rule>A</submit_rule>

- 最终验证阶段回答证据点顺序（例如第一对选择U1，第二对选择V2）：
<final_answer>U1,V2</final_answer>

## 失败条件

- 在{max_queries}次有效查询内未能正确提交推断
- 正确提交推断后，最终验证的两对判断中任一错误
- 累计三次违反查询约束或格式错误
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Judicial Evidence Chain Logical Review System". The legal logic tree of the current case is as follows (brackets show sub-evidence points/clauses from left to right):
{tree_structure}

The system has secretly adopted a logic review progression rule, selected from four candidate schemes:
- Scheme A: Guiding principle reviewed first, then diving into specific details left-to-right
- Scheme B: Guiding principle reviewed first, then diving into specific details right-to-left
- Scheme C: Corroborate all bottom-level details before establishing the guiding principle (postorder), left-to-right
- Scheme D: Breadth-first review by logical tier, same level factual evidence processed left-to-right

"Review" means the moment the collegial panel actually verifies the evidence point/clause in the dossier. "X before Y" means X is verified earlier than Y in the review sequence.

Your goal is to deduce the true review logic rule by checking the trial transcripts.

## System Operation Flow

1. **Transcript Query Phase**: You can submit up to {max_queries} queries: "Is evidence point X reviewed before point Y?"
   - Each query must specify two different evidence nodes
   - Nodes must be from the valid set {node_set}
   - The system will answer "Yes" or "No"
   - Invalid format or constraint violations count as errors

2. **Submit Inference**: When you have enough information, submit your inferred review rule (A, B, C, or D)
   - You must make at least {min_queries} valid queries before submitting
   - If incorrect and queries remain, you may continue querying and resubmit

3. **Final Verification**: After correct inference, the system will provide two evidence pairs you haven't directly compared
   - For each pair, judge which evidence point is reviewed first
   - Success requires both judgments to be correct

## Format Requirements

Each turn must contain only one tag. Use the following XML format:

- Query review order (e.g., asking about points R and A):
<query_order>R,A</query_order>

- Submit review rule inference (e.g., inferring Scheme A):
<submit_rule>A</submit_rule>

- Final verification answer (e.g., choosing U1 for first pair, V2 for second pair):
<final_answer>U1,V2</final_answer>

## Failure Conditions

- Unable to correctly submit inference within {max_queries} valid queries
- After correct inference, any error in the two final verification judgments
- Three accumulated constraint violations or format errors
"""

    tags = ["query_order", "submit_rule", "final_answer"]

    # 五种难度配置
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {  # 简单：小树，明显的先序遍历
                "tree_structure": "- R: [A, B]\n- A: [C]\n- B: [D]\n- C: []\n- D: []",
                "nodes": ["R", "A", "B", "C", "D"],
                "children": {
                    "R": ["A", "B"],
                    "A": ["C"],
                    "B": ["D"],
                    "C": [],
                    "D": []
                },
                "rule": "A",  # DFS先序左到右
                "max_queries": 8,
                "min_queries": 2,
                "final_pairs": [("A", "B"), ("C", "D")]
            },
            2: {  # 中等偏下：中等树，后序遍历
                "tree_structure": "- R: [A, B, C]\n- A: [D, E]\n- B: [F]\n- C: []\n- D: []\n- E: []\n- F: []",
                "nodes": ["R", "A", "B", "C", "D", "E", "F"],
                "children": {
                    "R": ["A", "B", "C"],
                    "A": ["D", "E"],
                    "B": ["F"],
                    "C": [],
                    "D": [],
                    "E": [],
                    "F": []
                },
                "rule": "C",  # DFS后序左到右
                "max_queries": 10,
                "min_queries": 3,
                "final_pairs": [("D", "E"), ("F", "C")]
            },
            3: {  # 中等偏上：题目中的树，广度优先
                "tree_structure": "- R: [A, B, C]\n- A: [D, E]\n- B: [F]\n- C: [G, H]\n- D: []\n- E: [I]\n- F: []\n- G: []\n- H: [J]\n- I: []\n- J: []",
                "nodes": ["R", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                "children": {
                    "R": ["A", "B", "C"],
                    "A": ["D", "E"],
                    "B": ["F"],
                    "C": ["G", "H"],
                    "D": [],
                    "E": ["I"],
                    "F": [],
                    "G": [],
                    "H": ["J"],
                    "I": [],
                    "J": []
                },
                "rule": "D",  # BFS
                "max_queries": 12,
                "min_queries": 3,
                "final_pairs": [("D", "F"), ("I", "J")]
            },
            4: {  # 较难：较大树，右到左先序
                "tree_structure": "- R: [A, B, C]\n- A: [D, E]\n- B: [F, G]\n- C: [H]\n- D: [I]\n- E: []\n- F: []\n- G: [J, K]\n- H: []\n- I: []\n- J: []\n- K: []",
                "nodes": ["R", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
                "children": {
                    "R": ["A", "B", "C"],
                    "A": ["D", "E"],
                    "B": ["F", "G"],
                    "C": ["H"],
                    "D": ["I"],
                    "E": [],
                    "F": [],
                    "G": ["J", "K"],
                    "H": [],
                    "I": [],
                    "J": [],
                    "K": []
                },
                "rule": "B",  # DFS先序右到左
                "max_queries": 12,
                "min_queries": 4,
                "final_pairs": [("I", "E"), ("J", "F")]
            },
            5: {  # 难：大树，后序遍历
                "tree_structure": "- R: [A, B, C]\n- A: [D, E, F]\n- B: [G, H]\n- C: [I]\n- D: [J]\n- E: []\n- F: [K]\n- G: []\n- H: [L, M]\n- I: [N]\n- J: []\n- K: []\n- L: []\n- M: []\n- N: []",
                "nodes": ["R", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"],
                "children": {
                    "R": ["A", "B", "C"],
                    "A": ["D", "E", "F"],
                    "B": ["G", "H"],
                    "C": ["I"],
                    "D": ["J"],
                    "E": [],
                    "F": ["K"],
                    "G": [],
                    "H": ["L", "M"],
                    "I": ["N"],
                    "J": [],
                    "K": [],
                    "L": [],
                    "M": [],
                    "N": []
                },
                "rule": "C",  # DFS后序左到右
                "max_queries": 15,
                "min_queries": 5,
                "final_pairs": [("J", "E"), ("L", "N")]
            }
        },
        "en": {
            1: {
                "tree_structure": "- R: [A, B]\n- A: [C]\n- B: [D]\n- C: []\n- D: []",
                "nodes": ["R", "A", "B", "C", "D"],
                "children": {
                    "R": ["A", "B"],
                    "A": ["C"],
                    "B": ["D"],
                    "C": [],
                    "D": []
                },
                "rule": "A",
                "max_queries": 8,
                "min_queries": 2,
                "final_pairs": [("A", "B"), ("C", "D")]
            },
            2: {
                "tree_structure": "- R: [A, B, C]\n- A: [D, E]\n- B: [F]\n- C: []\n- D: []\n- E: []\n- F: []",
                "nodes": ["R", "A", "B", "C", "D", "E", "F"],
                "children": {
                    "R": ["A", "B", "C"],
                    "A": ["D", "E"],
                    "B": ["F"],
                    "C": [],
                    "D": [],
                    "E": [],
                    "F": []
                },
                "rule": "C",
                "max_queries": 10,
                "min_queries": 3,
                "final_pairs": [("D", "E"), ("F", "C")]
            },
            3: {
                "tree_structure": "- R: [A, B, C]\n- A: [D, E]\n- B: [F]\n- C: [G, H]\n- D: []\n- E: [I]\n- F: []\n- G: []\n- H: [J]\n- I: []\n- J: []",
                "nodes": ["R", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                "children": {
                    "R": ["A", "B", "C"],
                    "A": ["D", "E"],
                    "B": ["F"],
                    "C": ["G", "H"],
                    "D": [],
                    "E": ["I"],
                    "F": [],
                    "G": [],
                    "H": ["J"],
                    "I": [],
                    "J": []
                },
                "rule": "D",
                "max_queries": 12,
                "min_queries": 3,
                "final_pairs": [("D", "F"), ("I", "J")]
            },
            4: {
                "tree_structure": "- R: [A, B, C]\n- A: [D, E]\n- B: [F, G]\n- C: [H]\n- D: [I]\n- E: []\n- F: []\n- G: [J, K]\n- H: []\n- I: []\n- J: []\n- K: []",
                "nodes": ["R", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
                "children": {
                    "R": ["A", "B", "C"],
                    "A": ["D", "E"],
                    "B": ["F", "G"],
                    "C": ["H"],
                    "D": ["I"],
                    "E": [],
                    "F": [],
                    "G": ["J", "K"],
                    "H": [],
                    "I": [],
                    "J": [],
                    "K": []
                },
                "rule": "B",
                "max_queries": 12,
                "min_queries": 4,
                "final_pairs": [("I", "E"), ("J", "F")]
            },
            5: {
                "tree_structure": "- R: [A, B, C]\n- A: [D, E, F]\n- B: [G, H]\n- C: [I]\n- D: [J]\n- E: []\n- F: [K]\n- G: []\n- H: [L, M]\n- I: [N]\n- J: []\n- K: []\n- L: []\n- M: []\n- N: []",
                "nodes": ["R", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"],
                "children": {
                    "R": ["A", "B", "C"],
                    "A": ["D", "E", "F"],
                    "B": ["G", "H"],
                    "C": ["I"],
                    "D": ["J"],
                    "E": [],
                    "F": ["K"],
                    "G": [],
                    "H": ["L", "M"],
                    "I": ["N"],
                    "J": [],
                    "K": [],
                    "L": [],
                    "M": [],
                    "N": []
                },
                "rule": "C",
                "max_queries": 15,
                "min_queries": 5,
                "final_pairs": [("J", "E"), ("L", "N")]
            }
        }
    }

    def __init__(self, config):
        # 游戏阶段：query（提问）、inferred（已推断正确）、final（最终验证）
        self.phase = "query"
        # 提问计数和错误计数
        self.query_count = 0
        self.error_count = 0
        # 记录已查询过的节点对
        self.queried_pairs = set()
        # 最终验证阶段的节点对
        self.final_verification_pairs = None
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：加载难度配置，生成遍历序列"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 树结构信息
        self._game_info["tree_structure"] = cfg["tree_structure"]
        self._game_info["node_set"] = "{" + ", ".join(cfg["nodes"]) + "}"
        self._game_info["max_queries"] = cfg["max_queries"]
        self._game_info["min_queries"] = cfg["min_queries"]
        
        self.nodes = cfg["nodes"]
        self.children = cfg["children"]
        self.rule = cfg["rule"]
        self.max_queries = cfg["max_queries"]
        self.min_queries = cfg["min_queries"]
        self.final_pairs = cfg["final_pairs"]
        
        # 生成真实的遍历序列
        self.traversal_order = self._generate_traversal(self.rule)
        # 创建节点到位置的映射，用于快速判断顺序
        self.node_position = {node: i for i, node in enumerate(self.traversal_order)}

    def _generate_traversal(self, rule):
        """根据遍历规则生成节点访问序列"""
        if rule == "A":
            # DFS先序，左到右
            return self._dfs_preorder("R", False)
        elif rule == "B":
            # DFS先序，右到左
            return self._dfs_preorder("R", True)
        elif rule == "C":
            # DFS后序，左到右
            return self._dfs_postorder("R", False)
        elif rule == "D":
            # BFS
            return self._bfs("R")
        else:
            raise ValueError(f"Unknown rule: {rule}")

    def _dfs_preorder(self, node, reverse):
        """深度优先先序遍历"""
        result = [node]
        children = self.children[node]
        if reverse:
            children = children[::-1]
        for child in children:
            result.extend(self._dfs_preorder(child, reverse))
        return result

    def _dfs_postorder(self, node, reverse):
        """深度优先后序遍历"""
        result = []
        children = self.children[node]
        if reverse:
            children = children[::-1]
        for child in children:
            result.extend(self._dfs_postorder(child, reverse))
        result.append(node)
        return result

    def _bfs(self, root):
        """广度优先遍历"""
        result = []
        queue = [root]
        while queue:
            node = queue.pop(0)
            result.append(node)
            queue.extend(self.children[node])
        return result

    def _is_before(self, node1, node2):
        """判断node1是否在node2之前被访问"""
        return self.node_position[node1] < self.node_position[node2]

    def evaluate(self, parsed_info):
        """评估最终答案（提交推断或最终验证）"""
        if "submit_rule" in parsed_info:
            # 提交遍历规则推断
            submitted_rule = parsed_info["submit_rule"].strip().upper()
            if submitted_rule == self.rule:
                # 推断正确，进入最终验证阶段
                self.phase = "inferred"
                return True
            else:
                return False
        
        elif "final_answer" in parsed_info:
            # 最终验证阶段的答案
            if self.phase != "inferred" or self.final_verification_pairs is None:
                return False
            
            try:
                answers = [x.strip() for x in parsed_info["final_answer"].split(",")]
                if len(answers) != 2:
                    return False
                
                # 检查每一对的答案
                for i, (node1, node2) in enumerate(self.final_verification_pairs):
                    answer = answers[i]
                    if answer not in [node1, node2]:
                        return False
                    # 判断答案是否正确
                    if self._is_before(node1, node2):
                        correct_answer = node1
                    else:
                        correct_answer = node2
                    if answer != correct_answer:
                        return False
                
                return True
            except:
                return False
        
        return False

    def _cf_core_produce(self, parsed_info):
        """处理 query_order 查询并生成回复"""
        is_zh = self.config.language == "zh"
        if "query_order" in parsed_info:
            if self.phase != "query":
                return "错误：当前阶段不允许提问。" if is_zh else "Error: Queries not allowed in current phase."
            if self.query_count >= self.max_queries:
                return (f"错误：已达到最大提问次数{self.max_queries}次。" if is_zh
                        else f"Error: Maximum query limit {self.max_queries} reached.")
            try:
                nodes = [x.strip() for x in parsed_info["query_order"].split(",")]
                if len(nodes) != 2:
                    raise ValueError("Must provide exactly 2 nodes")
                node1, node2 = nodes[0], nodes[1]
                if node1 not in self.nodes or node2 not in self.nodes:
                    self.error_count += 1
                    return "无效：节点不在有效集合中。" if is_zh else "Invalid: Node not in valid set."
                if node1 == node2:
                    self.error_count += 1
                    return "无效：必须询问两个不同的节点。" if is_zh else "Invalid: Must query two different nodes."
                pair = tuple(sorted([node1, node2]))
                self.queried_pairs.add(pair)
                self.query_count += 1
                if self._is_before(node1, node2):
                    return "是" if is_zh else "Yes"
                else:
                    return "否" if is_zh else "No"
            except Exception:
                self.error_count += 1
                return "无效：格式错误或参数无效。" if is_zh else "Invalid: Format error or invalid parameters."
        raise ValueError("No valid query tag found.")

    def step(self, response: str):
        """处理一轮交互，保留基类反事实逻辑"""
        if self.error_count >= 3:
            self.state.set_state("failed",
                "累计三次违反约束或格式错误" if self.config.language == "zh" else "Three accumulated errors")
            return self.state

        try:
            parsed_info = self.parse(response)
            is_zh = self.config.language == "zh"

            if "submit_rule" in parsed_info:
                if self.query_count < self.min_queries:
                    msg = (f"错误：必须先进行至少{self.min_queries}次有效提问。" if is_zh
                           else f"Error: Must make at least {self.min_queries} valid queries first.")
                    self.state.add_message("user", msg)
                    return self.state

                submitted_rule = parsed_info["submit_rule"].strip().upper()
                if submitted_rule not in ["A", "B", "C", "D"]:
                    self.error_count += 1
                    msg = "无效：规则必须是A、B、C或D之一。" if is_zh else "Invalid: Rule must be one of A, B, C, or D."
                    self.state.add_message("user", msg)
                    return self.state

                if submitted_rule == self.rule:
                    self.phase = "inferred"
                    self.final_verification_pairs = self._select_final_pairs()
                    if self.final_verification_pairs and len(self.final_verification_pairs) >= 2:
                        pairs_str = ""
                        for i, (n1, n2) in enumerate(self.final_verification_pairs, 1):
                            pairs_str += (f"第{i}对：<{n1}, {n2}>\n" if is_zh
                                          else f"Pair {i}: <{n1}, {n2}>\n")
                        msg = (f"推断正确！现在进入最终验证阶段。\n请对以下两对节点判断哪个先被访问：\n{pairs_str}"
                               f"请用<final_answer>标签提交答案，格式如：<final_answer>节点1,节点2</final_answer>"
                               if is_zh else
                               f"Correct inference! Now entering final verification.\n"
                               f"For the following two pairs, judge which node is visited first:\n{pairs_str}"
                               f"Submit with <final_answer> tag, format: <final_answer>node1,node2</final_answer>")
                        self.state.add_message("user", msg)
                    else:
                        self.state.set_state("success",
                            "推断正确且无需最终验证" if is_zh else "Correct inference, no verification needed")
                        msg = "推断正确！" if is_zh else "Correct inference!"
                        self.state.add_message("user", msg)
                else:
                    msg = "推断错误。" if is_zh else "Incorrect inference."
                    if self.query_count < self.max_queries:
                        msg += "你可以继续提问。" if is_zh else " You may continue querying."
                    else:
                        self.state.set_state("failed",
                            "推断错误且无剩余提问次数" if is_zh else "Incorrect inference with no queries remaining")
                        self.state.add_message("user", msg)

            elif "final_answer" in parsed_info:
                is_correct = self.evaluate(parsed_info)
                if is_correct:
                    self.state.set_state("success",
                        "最终验证成功" if is_zh else "Final verification successful")
                    msg = "最终验证成功！游戏胜利！" if is_zh else "Final verification successful! You win!"
                    self.state.add_message("user", msg)
                else:
                    self.state.set_state("failed",
                        "最终验证失败" if is_zh else "Final verification failed")
                    msg = "最终验证失败。" if is_zh else "Final verification failed."
                    self.state.add_message("user", msg)

            else:
                # 普通查询 —— 调用基类的 produce_response 以保持反事实兼容
                game_response = self.produce_response(parsed_info)
                if game_response:
                    self.state.add_message("user", game_response)

                if self.query_count >= self.max_queries and self.phase == "query":
                    msg = (f"已达到最大提问次数{self.max_queries}次，请提交推断。" if is_zh
                           else f"Maximum query limit {self.max_queries} reached. Please submit inference.")
                    self.state.add_message("user", msg)

        except Exception as e:
            self.error_count += 1
            if self.error_count >= 3:
                self.state.set_state("failed",
                    "累计三次违反约束或格式错误" if self.config.language == "zh" else "Three accumulated errors")
            # 不设 failed，允许继续（除非已达3次）

        return self.state

    def _select_final_pairs(self):
        """选择两对未被直接查询过的节点对用于最终验证"""
        # 使用配置中的固定节点对
        result = []
        for pair in self.final_pairs:
            sorted_pair = tuple(sorted(pair))
            if sorted_pair not in self.queried_pairs:
                result.append(pair)
        
        # 返回前两对（如果有的话）
        return result[:2] if len(result) >= 2 else result

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串，与游戏中 parsed_info["query"] 的值格式一致
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        possible_queries = []
        is_zh = self.config.language == "zh"
        
        # 排除无效节点，只对有效节点集合进行排列组合
        # 提问格式要求：<query_order>A,B</query_order>
        # 这里返回的 query 字段对应 parsed_info["query_order"] 的值，即 "A,B"
        
        for n1, n2 in itertools.permutations(self.nodes, 2):
            # 构造查询字符串
            query_str = f"{n1},{n2}"
            
            # 获取正确答案 (直接调用内部逻辑，不增加计数器)
            if self._is_before(n1, n2):
                ans = "是" if is_zh else "Yes"
            else:
                ans = "否" if is_zh else "No"
                
            possible_queries.append({
                "query": query_str,
                "answer": ans
            })
            
        return possible_queries

    def _cf_make_wrong(self, correct: str) -> str:
        """将正确答案替换为错误答案"""
        is_zh = self.config.language == "zh"
        if is_zh:
            if correct == "是":
                return "否"
            if correct == "否":
                return "是"
        else:
            if correct == "Yes":
                return "No"
            if correct == "No":
                return "Yes"
        return correct + "_WRONG"