from .base import Game
import re

class PathScoringGame(Game):

    game_rule_zh = """\
我们现在来玩一个"路径得分函数推理"游戏，规则如下：

游戏设定了一棵固定的有根树，共15个节点，每个节点带有整数权值。真实的路径得分函数在四个已知候选函数 A/B/C/D 中固定取其一，但对你保密。你的目标是：
1. 先判别当前采用的得分函数是哪一个
2. 再在该函数下求出得分最大的根到叶完整路径及其得分

根节点深度为0。节点标号与权值（括号内为权值）：
- 1(3)
  - 1的孩子：2(5)，3(2)
    - 2的孩子：4(4)，5(1)
      - 4的孩子：9(7)，10(0) [叶]
      - 5的孩子：11(9) [叶]
    - 3的孩子：6(6)，7(3)，8(2)
      - 6的孩子：12(1)，13(8) [叶]
      - 7的孩子：14(5) [叶]
      - 8的孩子：15(10) [叶]

- A: 路径得分 = 路径上所有节点权值之和
- B: 路径得分 = 路径上每个节点的"(深度+1)×权值"之和，其中根节点深度为0
- C: 路径得分 = 路径上每个节点的"符号×权值"之和，其中偶数深度符号为+1，奇数深度符号为-1
- D: 路径得分 = 路径上所有节点权值之和 + 奖励值，其中：
  - 若路径到达叶子，奖励值 = 路径上的最大权值
  - 若路径为非叶前缀路径，奖励值 = 0

路径用"->"连接节点编号，且根必须在最前，如"1->2->4->9"。路径可为前缀（到中间节点）或完整（到叶子节点）。

你可以发起以下操作（每次只能一个操作），系统会根据真实设定如实回答：

1. 评估：查询任意从根出发的路径得分（前缀或叶均可）
2. 比较：比较两条从根出发路径的得分（前缀按各函数前缀定义计算）
3. 认定规则：猜测当前采用的函数（需先完成至少两次评估）
4. 最终答案：提交你认为的最优根到叶路径及得分（需先正确认定规则）

每次操作必须使用以下 XML 格式之一：

- 评估（例如评估路径1->2->4）：
<query_eval>1->2->4</query_eval>

- 比较（例如比较路径1->2与1->3）：
<query_compare>1->2 VS 1->3</query_compare>

- 认定规则（例如认定为函数B）：
<identify_rule>B</identify_rule>

- 提交最终答案（必须包含路径和得分）：
<answer>路径=1->2->4->9, 得分=50</answer>

- 对"评估"：返回"得分=整数"
- 对"比较"：返回"路径1更高"/"路径2更高"/"相等"
- 对"认定规则"：返回"正确"或"错误"
- 对"最终答案"：若规则认定正确且路径与得分均为该规则下最优与正确，返回"胜利"，否则"失败"

胜利条件：
- 至少进行了两次"评估"
- 正确认定采用的函数
- 在该函数下，提交的根到叶路径为全局最优，且给出的得分数值正确

失败条件：
- 认定规则错误
- 提交的路径非最优
- 得分数值不正确
- 未进行至少两次"评估"就尝试认定规则

请开始你的推理。
"""

    game_rule_en = """\
Let's play a "Path Scoring Function Inference" game. Here are the rules:

The game features a fixed rooted tree with 15 nodes, each carrying an integer weight. The true path scoring function is secretly selected from four known candidate functions A/B/C/D. Your goal is to:
1. First identify which scoring function is being used
2. Then find the root-to-leaf path with the maximum score under that function and its score

Root node has depth 0. Node IDs and weights (weights in parentheses):
- 1(3)
  - Children of 1: 2(5), 3(2)
    - Children of 2: 4(4), 5(1)
      - Children of 4: 9(7), 10(0) [leaf]
      - Children of 5: 11(9) [leaf]
    - Children of 3: 6(6), 7(3), 8(2)
      - Children of 6: 12(1), 13(8) [leaf]
      - Children of 7: 14(5) [leaf]
      - Children of 8: 15(10) [leaf]

- A: Path score = sum of all node weights on the path
- B: Path score = sum of "(depth+1) times weight" for each node on the path, where root has depth 0
- C: Path score = sum of "sign times weight" for each node on the path, where sign is +1 for even depth and -1 for odd depth
- D: Path score = sum of all node weights on the path + bonus, where:
  - If path reaches a leaf, bonus = maximum weight on the path
  - If path is a non-leaf prefix, bonus = 0

Paths are represented by node IDs connected with "->", starting from root, e.g., "1->2->4->9". Paths can be prefixes (ending at intermediate nodes) or complete (ending at leaf nodes).

You can perform the following operations (one at a time), and the system will respond truthfully:

1. Evaluate: Query the score of any path starting from root (prefix or leaf)
2. Compare: Compare the scores of two paths starting from root
3. Identify Rule: Guess which function is being used (requires at least two evaluations first)
4. Final Answer: Submit your answer for the optimal root-to-leaf path and its score (requires correct rule identification first)

Each operation must use one of the following XML formats:

- Evaluate (e.g., evaluate path 1->2->4):
<query_eval>1->2->4</query_eval>

- Compare (e.g., compare path 1->2 with 1->3):
<query_compare>1->2 VS 1->3</query_compare>

- Identify Rule (e.g., identify as function B):
<identify_rule>B</identify_rule>

- Submit Final Answer (must include path and score):
<answer>path=1->2->4->9, score=50</answer>

- For "Evaluate": Returns "score=integer"
- For "Compare": Returns "path1 higher"/"path2 higher"/"equal"
- For "Identify Rule": Returns "correct" or "incorrect"
- For "Final Answer": Returns "victory" if rule is correct and path/score are optimal and correct; otherwise "failure"

Victory conditions:
- At least two "evaluations" performed
- Correctly identified the function
- Submitted root-to-leaf path is globally optimal under that function, and the score value is correct

Failure conditions:
- Incorrectly identified the rule
- Submitted path is not optimal
- Score value is incorrect
- Attempted to identify rule without at least two evaluations

Start your inference now.
"""

    contextualized_rule_zh_1 = """\
在城市智能交通网络规划中，我们需要对某片区的路线拥堵成本进行评估。系统设定了一棵固定的路网决策树，共15个节点（路口/路段），每个节点带有整数的基础拥堵指数。真实的耗时评估模型在四个已知候选模型 A/B/C/D 中固定取其一，但对你保密。你的目标是：
1. 先判别当前采用的评估模型是哪一个
2. 再在该模型下求出拥堵得分最大的起点到终点（根到叶）完整路线及其得分

起点阶段/深度为0。节点标号与基础拥堵指数（括号内为指数）：
- 1(3)
  - 1的下一段：2(5)，3(2)
    - 2的下一段：4(4)，5(1)
      - 4的下一段：9(7)，10(0) [终点/叶]
      - 5的下一段：11(9) [终点/叶]
    - 3的下一段：6(6)，7(3)，8(2)
      - 6的下一段：12(1)，13(8) [终点/叶]
      - 7的下一段：14(5) [终点/叶]
      - 8的下一段：15(10) [终点/叶]

- A: 路线拥堵得分 = 路线途经所有路段基础指数之和
- B: 路线拥堵得分 = 路线途经每个路段的"(阶段+1)×基础指数"之和，其中起点阶段为0
- C: 路线拥堵得分 = 路线途经每个路段的"潮汐符号×基础指数"之和，其中偶数阶段符号为+1（顺流），奇数阶段符号为-1（逆流）
- D: 路线拥堵得分 = 路线途经所有路段基础指数之和 + 额外耗时，其中：
  - 若路线到达终点（叶子），额外耗时 = 路线上的最大基础指数（视为找车位惩罚）
  - 若路线为未到终点的中途段（非叶前缀），额外耗时 = 0

路线用"->"连接路段编号，且起点必须在最前，如"1->2->4->9"。路线可为前缀（中途路段）或完整（终点路段）。

你可以发起以下操作（每次只能一个操作），系统会根据真实设定如实回答：

1. 评估：查询任意从起点出发的路线拥堵得分（前缀或叶均可）
2. 比较：比较两条从起点出发路线的拥堵得分（前缀按各模型前缀定义计算）
3. 认定规则：猜测当前采用的模型（需先完成至少两次评估）
4. 最终答案：提交你认为的最优起点到终点路线及得分（需先正确认定规则）

每次操作必须使用以下 XML 格式之一：

- 评估（例如评估路径1->2->4）：
<query_eval>1->2->4</query_eval>

- 比较（例如比较路径1->2与1->3）：
<query_compare>1->2 VS 1->3</query_compare>

- 认定规则（例如认定为模型B）：
<identify_rule>B</identify_rule>

- 提交最终答案（必须包含路径和得分）：
<answer>路径=1->2->4->9, 得分=50</answer>

- 对"评估"：返回"得分=整数"
- 对"比较"：返回"路径1更高"/"路径2更高"/"相等"
- 对"认定规则"：返回"正确"或"错误"
- 对"最终答案"：若规则认定正确且路线与得分均为该规则下最优与正确，返回"胜利"，否则"失败"

胜利条件：
- 至少进行了两次"评估"
- 正确认定采用的模型
- 在该模型下，提交的根到叶完整路线为全局最优，且给出的得分数值正确

失败条件：
- 认定规则错误
- 提交的路线非最优
- 得分数值不正确
- 未进行至少两次"评估"就尝试认定规则

请开始你的推理。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
In urban smart transportation network planning, we need to evaluate the route congestion cost of a certain area. The system features a fixed road network decision tree with 15 nodes (intersections/road segments), each carrying an integer basic congestion index. The true evaluation model is secretly selected from four known candidate models A/B/C/D. Your goal is to:
1. First identify which evaluation model is being used
2. Then find the origin-to-destination (root-to-leaf) complete route with the maximum congestion score under that model and its score

Origin (Root) stage/depth is 0. Node IDs and basic congestion indices (indices in parentheses):
- 1(3)
  - Next segments of 1: 2(5), 3(2)
    - Next segments of 2: 4(4), 5(1)
      - Next segments of 4: 9(7), 10(0) [destination/leaf]
      - Next segments of 5: 11(9) [destination/leaf]
    - Next segments of 3: 6(6), 7(3), 8(2)
      - Next segments of 6: 12(1), 13(8) [destination/leaf]
      - Next segments of 7: 14(5) [destination/leaf]
      - Next segments of 8: 15(10) [destination/leaf]

- A: Route score = sum of basic congestion indices of all segments on the route
- B: Route score = sum of "(stage+1) times basic index" for each segment on the route, where origin stage is 0
- C: Route score = sum of "tidal sign times basic index" for each segment on the route, where sign is +1 for even stage (downstream) and -1 for odd stage (upstream)
- D: Route score = sum of basic congestion indices of all segments on the route + extra time penalty, where:
  - If route reaches destination (leaf), penalty = maximum basic index on the route (parking search penalty)
  - If route is an intermediate segment (non-leaf prefix), penalty = 0

Routes are represented by segment IDs connected with "->", starting from origin, e.g., "1->2->4->9". Routes can be prefixes (intermediate segments) or complete (destination segments).

You can perform the following operations (one at a time), and the system will respond truthfully:

1. Evaluate: Query the congestion score of any route starting from origin
2. Compare: Compare the congestion scores of two routes starting from origin
3. Identify Rule: Guess which model is being used (requires at least two evaluations first)
4. Final Answer: Submit your answer for the optimal origin-to-destination route and its score (requires correct rule identification first)

Each operation must use one of the following XML formats:

- Evaluate (e.g., evaluate path 1->2->4):
<query_eval>1->2->4</query_eval>

- Compare (e.g., compare path 1->2 with 1->3):
<query_compare>1->2 VS 1->3</query_compare>

- Identify Rule (e.g., identify as model B):
<identify_rule>B</identify_rule>

- Submit Final Answer (must include path and score):
<answer>path=1->2->4->9, score=50</answer>

- For "Evaluate": Returns "score=integer"
- For "Compare": Returns "path1 higher"/"path2 higher"/"equal"
- For "Identify Rule": Returns "correct" or "incorrect"
- For "Final Answer": Returns "victory" if rule is correct and route/score are optimal and correct; otherwise "failure"

Victory conditions:
- At least two "evaluations" performed
- Correctly identified the model
- Submitted origin-to-destination route is globally optimal under that model, and the score value is correct

Failure conditions:
- Incorrectly identified the rule
- Submitted route is not optimal
- Score value is incorrect
- Attempted to identify rule without at least two evaluations

Start your inference now.
"""

    contextualized_rule_zh_2 = """\
在临床辅助诊疗系统中，我们需要对某类疾病的治疗路径风险进行评估。系统设定了一棵固定的临床决策树，共15个节点（治疗方案/检查），每个节点带有整数的基础风险值。真实的风险评估模型在四个已知候选模型 A/B/C/D 中固定取其一，但对你保密。你的目标是：
1. 先判别当前采用的评估模型是哪一个
2. 再在该模型下求出累计风险得分最大的初始诊断到最终疗效（根到叶）完整疗程路径及其得分

初始方案阶段/深度为0。节点标号与基础风险值（括号内为风险值）：
- 1(3)
  - 1的后续方案：2(5)，3(2)
    - 2的后续方案：4(4)，5(1)
      - 4的后续方案：9(7)，10(0) [疗程终末/叶]
      - 5的后续方案：11(9) [疗程终末/叶]
    - 3的后续方案：6(6)，7(3)，8(2)
      - 6的后续方案：12(1)，13(8) [疗程终末/叶]
      - 7的后续方案：14(5) [疗程终末/叶]
      - 8的后续方案：15(10) [疗程终末/叶]

- A: 路径风险得分 = 疗程上所有节点基础风险值之和
- B: 路径风险得分 = 疗程上每个节点的"(阶段+1)×基础风险值"之和，其中初始阶段为0（随疗程深入体弱风险放大）
- C: 路径风险得分 = 疗程上每个节点的"干预符号×基础风险值"之和，其中偶数阶段符号为+1（副作用增加风险），奇数阶段符号为-1（保护性措施抵消风险）
- D: 路径风险得分 = 疗程上所有节点基础风险值之和 + 后遗症惩罚，其中：
  - 若疗程完成（到达叶子），后遗症惩罚 = 疗程上的最大基础风险值
  - 若疗程仅为前置步骤（非叶前缀），后遗症惩罚 = 0

疗程路径用"->"连接方案编号，且初始方案必须在最前，如"1->2->4->9"。路径可为前缀（中途方案）或完整（疗程终末）。

你可以发起以下操作（每次只能一个操作），系统会根据真实设定如实回答：

1. 评估：查询任意从起点出发的疗程路径得分（前缀或叶均可）
2. 比较：比较两条从起点出发路径的风险得分
3. 认定规则：猜测当前采用的模型（需先完成至少两次评估）
4. 最终答案：提交你认为的最优完整疗程路径及得分（需先正确认定规则）

每次操作必须使用以下 XML 格式之一：

- 评估（例如评估路径1->2->4）：
<query_eval>1->2->4</query_eval>

- 比较（例如比较路径1->2与1->3）：
<query_compare>1->2 VS 1->3</query_compare>

- 认定规则（例如认定为模型B）：
<identify_rule>B</identify_rule>

- 提交最终答案（必须包含路径和得分）：
<answer>路径=1->2->4->9, 得分=50</answer>

- 对"评估"：返回"得分=整数"
- 对"比较"：返回"路径1更高"/"路径2更高"/"相等"
- 对"认定规则"：返回"正确"或"错误"
- 对"最终答案"：若规则认定正确且路径与得分均为该规则下最优与正确，返回"胜利"，否则"失败"

胜利条件：
- 至少进行了两次"评估"
- 正确认定采用的模型
- 在该模型下，提交的根到叶完整路径为全局最优，且给出的得分数值正确

失败条件：
- 认定规则错误
- 提交的路径非最优
- 得分数值不正确
- 未进行至少两次"评估"就尝试认定规则

请开始你的推理。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
In the clinical decision support system, we need to evaluate the risk of treatment pathways for a specific disease. The system features a fixed clinical decision tree with 15 nodes (treatment options/tests), each carrying an integer basic risk value. The true risk evaluation model is secretly selected from four known candidate models A/B/C/D. Your goal is to:
1. First identify which evaluation model is being used
2. Then find the initial-diagnosis-to-final-outcome (root-to-leaf) complete treatment pathway with the maximum risk score under that model and its score

Initial diagnosis stage/depth is 0. Node IDs and basic risk values (values in parentheses):
- 1(3)
  - Next steps of 1: 2(5), 3(2)
    - Next steps of 2: 4(4), 5(1)
      - Next steps of 4: 9(7), 10(0) [final outcome/leaf]
      - Next steps of 5: 11(9) [final outcome/leaf]
    - Next steps of 3: 6(6), 7(3), 8(2)
      - Next steps of 6: 12(1), 13(8) [final outcome/leaf]
      - Next steps of 7: 14(5) [final outcome/leaf]
      - Next steps of 8: 15(10) [final outcome/leaf]

- A: Pathway score = sum of basic risk values of all nodes on the pathway
- B: Pathway score = sum of "(stage+1) times basic risk value" for each node on the pathway, where initial stage is 0 (weakness magnifies risk)
- C: Pathway score = sum of "intervention sign times basic risk value" for each node on the pathway, where sign is +1 for even stage (side effects) and -1 for odd stage (protective mitigation)
- D: Pathway score = sum of basic risk values of all nodes on the pathway + sequelae penalty, where:
  - If pathway reaches final outcome (leaf), penalty = maximum basic risk value on the pathway
  - If pathway is just preliminary steps (non-leaf prefix), penalty = 0

Pathways are represented by node IDs connected with "->", starting from origin, e.g., "1->2->4->9". Pathways can be prefixes (intermediate steps) or complete (final outcomes).

You can perform the following operations (one at a time), and the system will respond truthfully:

1. Evaluate: Query the risk score of any pathway starting from initial diagnosis
2. Compare: Compare the risk scores of two pathways starting from initial diagnosis
3. Identify Rule: Guess which model is being used (requires at least two evaluations first)
4. Final Answer: Submit your answer for the optimal complete treatment pathway and its score (requires correct rule identification first)

Each operation must use one of the following XML formats:

- Evaluate (e.g., evaluate path 1->2->4):
<query_eval>1->2->4</query_eval>

- Compare (e.g., compare path 1->2 with 1->3):
<query_compare>1->2 VS 1->3</query_compare>

- Identify Rule (e.g., identify as model B):
<identify_rule>B</identify_rule>

- Submit Final Answer (must include path and score):
<answer>path=1->2->4->9, score=50</answer>

- For "Evaluate": Returns "score=integer"
- For "Compare": Returns "path1 higher"/"path2 higher"/"equal"
- For "Identify Rule": Returns "correct" or "incorrect"
- For "Final Answer": Returns "victory" if rule is correct and pathway/score are optimal and correct; otherwise "failure"

Victory conditions:
- At least two "evaluations" performed
- Correctly identified the model
- Submitted origin-to-destination pathway is globally optimal under that model, and the score value is correct

Failure conditions:
- Incorrectly identified the rule
- Submitted pathway is not optimal
- Score value is incorrect
- Attempted to identify rule without at least two evaluations

Start your inference now.
"""

    contextualized_rule_zh_3 = """\
在自适应学习系统的研发中，我们需要对知识图谱的学习路径认知负荷进行评估。系统设定了一棵固定的前置知识依赖树，共15个节点（学习模块），每个节点带有整数的基础认知负荷值。真实的负荷计算规则在四个已知候选规则 A/B/C/D 中固定取其一，但对你保密。你的目标是：
1. 先判别当前采用的计算规则是哪一个
2. 再在该规则下求出认知负荷得分最大的起点到结课（根到叶）完整学习路径及其得分

起点阶段/层级为0。节点标号与基础认知负荷值（括号内为负荷值）：
- 1(3)
  - 1的进阶模块：2(5)，3(2)
    - 2的进阶模块：4(4)，5(1)
      - 4的进阶模块：9(7)，10(0) [结课/叶]
      - 5的进阶模块：11(9) [结课/叶]
    - 3的进阶模块：6(6)，7(3)，8(2)
      - 6的进阶模块：12(1)，13(8) [结课/叶]
      - 7的进阶模块：14(5) [结课/叶]
      - 8的进阶模块：15(10) [结课/叶]

- A: 路径负荷得分 = 学习路径上所有模块基础负荷值之和
- B: 路径负荷得分 = 学习路径上每个模块的"(层级+1)×基础负荷值"之和，其中起点层级为0
- C: 路径负荷得分 = 学习路径上每个模块的"吸收符号×基础负荷值"之和，其中偶数层级符号为+1（引入新概念），奇数层级符号为-1（复习巩固）
- D: 路径负荷得分 = 学习路径上所有模块基础负荷值之和 + 期末考核压力，其中：
  - 若完成整个方向（到达叶子），期末考核压力 = 路径上的最大基础负荷值
  - 若仅为中间阶段（非叶前缀），期末考核压力 = 0

路径用"->"连接模块编号，且起点模块必须在最前，如"1->2->4->9"。路径可为前缀（中途阶段）或完整（结课阶段）。

你可以发起以下操作（每次只能一个操作），系统会根据真实设定如实回答：

1. 评估：查询任意从起点出发的路径负荷得分（前缀或叶均可）
2. 比较：比较两条从起点出发路径的负荷得分
3. 认定规则：猜测当前采用的计算规则（需先完成至少两次评估）
4. 最终答案：提交你认为的最优完整学习路径及得分（需先正确认定规则）

每次操作必须使用以下 XML 格式之一：

- 评估（例如评估路径1->2->4）：
<query_eval>1->2->4</query_eval>

- 比较（例如比较路径1->2与1->3）：
<query_compare>1->2 VS 1->3</query_compare>

- 认定规则（例如认定为规则B）：
<identify_rule>B</identify_rule>

- 提交最终答案（必须包含路径和得分）：
<answer>路径=1->2->4->9,得分=50</answer>

- 对"评估"：返回"得分=整数"
- 对"比较"：返回"路径1更高"/"路径2更高"/"相等"
- 对"认定规则"：返回"正确"或"错误"
- 对"最终答案"：若规则认定正确且路径与得分均为该规则下最优与正确，返回"胜利"，否则"失败"

胜利条件：
- 至少进行了两次"评估"
- 正确认定采用的计算规则
- 在该规则下，提交的完整学习路径为全局最优，且给出的得分数值正确

失败条件：
- 认定规则错误
- 提交的路径非最优
- 得分数值不正确
- 未进行至少两次"评估"就尝试认定规则

请开始你的推理。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
In the research and development of adaptive learning systems, we need to evaluate the cognitive load of learning paths within a knowledge graph. The system features a fixed prerequisite dependency tree with 15 nodes (learning modules), each carrying an integer basic cognitive load value. The true calculation rule is secretly selected from four known candidate rules A/B/C/D. Your goal is to:
1. First identify which calculation rule is being used
2. Then find the start-to-completion (root-to-leaf) complete learning path with the maximum cognitive load score under that rule and its score

Starting module stage/level is 0. Node IDs and basic load values (values in parentheses):
- 1(3)
  - Advanced modules of 1: 2(5), 3(2)
    - Advanced modules of 2: 4(4), 5(1)
      - Advanced modules of 4: 9(7), 10(0) [completion/leaf]
      - Advanced modules of 5: 11(9) [completion/leaf]
    - Advanced modules of 3: 6(6), 7(3), 8(2)
      - Advanced modules of 6: 12(1), 13(8) [completion/leaf]
      - Advanced modules of 7: 14(5) [completion/leaf]
      - Advanced modules of 8: 15(10) [completion/leaf]

- A: Path score = sum of basic load values of all modules on the path
- B: Path score = sum of "(level+1) times basic load value" for each module on the path, where starting level is 0
- C: Path score = sum of "absorption sign times basic load value" for each module on the path, where sign is +1 for even level (introducing new concepts) and -1 for odd level (review and consolidation)
- D: Path score = sum of basic load values of all modules on the path + final exam pressure, where:
  - If completing the entire direction (reaches leaf), exam pressure = maximum basic load value on the path
  - If just an intermediate stage (non-leaf prefix), exam pressure = 0

Paths are represented by node IDs connected with "->", starting from origin, e.g., "1->2->4->9". Paths can be prefixes (intermediate stages) or complete (completion stages).

You can perform the following operations (one at a time), and the system will respond truthfully:

1. Evaluate: Query the load score of any path starting from the origin
2. Compare: Compare the load scores of two paths starting from the origin
3. Identify Rule: Guess which rule is being used (requires at least two evaluations first)
4. Final Answer: Submit your answer for the optimal complete learning path and its score (requires correct rule identification first)

Each operation must use one of the following XML formats:

- Evaluate (e.g., evaluate path 1->2->4):
<query_eval>1->2->4</query_eval>

- Compare (e.g., compare path 1->2 with 1->3):
<query_compare>1->2 VS 1->3</query_compare>

- Identify Rule (e.g., identify as rule B):
<identify_rule>B</identify_rule>

- Submit Final Answer (must include path and score):
<answer>path=1->2->4->9, score=50</answer>

- For "Evaluate": Returns "score=integer"
- For "Compare": Returns "path1 higher"/"path2 higher"/"equal"
- For "Identify Rule": Returns "correct" or "incorrect"
- For "Final Answer": Returns "victory" if rule is correct and path/score are optimal and correct; otherwise "failure"

Victory conditions:
- At least two "evaluations" performed
- Correctly identified the rule
- Submitted origin-to-destination path is globally optimal under that rule, and the score value is correct

Failure conditions:
- Incorrectly identified the rule
- Submitted path is not optimal
- Score value is incorrect
- Attempted to identify rule without at least two evaluations

Start your inference now.
"""

    contextualized_rule_zh_4 = """\
在柔性生产线的排程优化中，我们需要对加工工艺路线的物料损耗进行评估。系统设定了一棵固定的工艺路线树，共15个节点（加工工序），每个节点带有整数的基础损耗值。真实的损耗评估函数在四个已知候选函数 A/B/C/D 中固定取其一，但对你保密。你的目标是：
1. 先判别当前采用的评估函数是哪一个
2. 再在该函数下求出损耗得分最大的首道工序到最终成品（根到叶）完整工艺路径及其得分

首道工序阶段/深度为0。节点标号与基础损耗值（括号内为损耗值）：
- 1(3)
  - 1的后续工序：2(5)，3(2)
    - 2的后续工序：4(4)，5(1)
      - 4的后续工序：9(7)，10(0) [成品/叶]
      - 5的后续工序：11(9) [成品/叶]
    - 3的后续工序：6(6)，7(3)，8(2)
      - 6的后续工序：12(1)，13(8) [成品/叶]
      - 7的后续工序：14(5) [成品/叶]
      - 8的后续工序：15(10) [成品/叶]

- A: 路径损耗得分 = 工艺路径上所有工序基础损耗值之和
- B: 路径损耗得分 = 工艺路径上每个工序的"(阶段+1)×基础损耗值"之和，其中首道阶段为0（误差放大致损耗倍增）
- C: 路径损耗得分 = 工艺路径上每个工序的"形变符号×基础损耗值"之和，其中偶数阶段符号为+1（热胀增加损耗），奇数阶段符号为-1（冷缩抵消部分损耗）
- D: 路径损耗得分 = 工艺路径上所有工序基础损耗值之和 + 报废沉没成本，其中：
  - 若完成最终成品组装（到达叶子），报废沉没成本 = 路径上的最大基础损耗值
  - 若仅为半成品状态（非叶前缀），报废沉没成本 = 0

路径用"->"连接工序编号，且首道工序必须在最前，如"1->2->4->9"。路径可为前缀（半成品）或完整（成品组装）。

你可以发起以下操作（每次只能一个操作），系统会根据真实设定如实回答：

1. 评估：查询任意从首道工序出发的路径损耗得分（前缀或叶均可）
2. 比较：比较两条从首道工序出发路径的损耗得分
3. 认定规则：猜测当前采用的函数（需先完成至少两次评估）
4. 最终答案：提交你认为的最优完整工艺路径及得分（需先正确认定规则）

每次操作必须使用以下 XML 格式之一：

- 评估（例如评估路径1->2->4）：
<query_eval>1->2->4</query_eval>

- 比较（例如比较路径1->2与1->3）：
<query_compare>1->2 VS 1->3</query_compare>

- 认定规则（例如认定为函数B）：
<identify_rule>B</identify_rule>

- 提交最终答案（必须包含路径和得分）：
<answer>路径=1->2->4->9, 得分=50</answer>

- 对"评估"：返回"得分=整数"
- 对"比较"：返回"路径1更高"/"路径2更高"/"相等"
- 对"认定规则"：返回"正确"或"错误"
- 对"最终答案"：若规则认定正确且路径与得分均为该规则下最优与正确，返回"胜利"，否则"失败"

胜利条件：
- 至少进行了两次"评估"
- 正确认定采用的函数
- 在该函数下，提交的完整工艺路径为全局最优，且给出的得分数值正确

失败条件：
- 认定规则错误
- 提交的路径非最优
- 得分数值不正确
- 未进行至少两次"评估"就尝试认定规则

请开始你的推理。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
In flexible production line scheduling, we need to evaluate the material loss of processing routes. The system features a fixed processing route tree with 15 nodes (processes), each carrying an integer basic loss value. The true loss evaluation function is secretly selected from four known candidate functions A/B/C/D. Your goal is to:
1. First identify which evaluation function is being used
2. Then find the first-process-to-final-product (root-to-leaf) complete processing route with the maximum loss score under that function and its score

First process stage/depth is 0. Node IDs and basic loss values (values in parentheses):
- 1(3)
  - Next processes of 1: 2(5), 3(2)
    - Next processes of 2: 4(4), 5(1)
      - Next processes of 4: 9(7), 10(0) [final product/leaf]
      - Next processes of 5: 11(9) [final product/leaf]
    - Next processes of 3: 6(6), 7(3), 8(2)
      - Next processes of 6: 12(1), 13(8) [final product/leaf]
      - Next processes of 7: 14(5) [final product/leaf]
      - Next processes of 8: 15(10) [final product/leaf]

- A: Path score = sum of basic loss values of all processes on the route
- B: Path score = sum of "(stage+1) times basic loss value" for each process on the route, where first stage is 0 (error amplification)
- C: Path score = sum of "deformation sign times basic loss value" for each process on the route, where sign is +1 for even stage (thermal expansion) and -1 for odd stage (cooling shrinkage offset)
- D: Path score = sum of basic loss values of all processes on the route + scrap sunk cost, where:
  - If route completes final assembly (reaches leaf), sunk cost = maximum basic loss value on the route
  - If route is only semi-finished (non-leaf prefix), sunk cost = 0

Routes are represented by node IDs connected with "->", starting from origin, e.g., "1->2->4->9". Routes can be prefixes (semi-finished) or complete (final assembly).

You can perform the following operations (one at a time), and the system will respond truthfully:

1. Evaluate: Query the loss score of any route starting from the first process
2. Compare: Compare the loss scores of two routes starting from the first process
3. Identify Rule: Guess which function is being used (requires at least two evaluations first)
4. Final Answer: Submit your answer for the optimal complete processing route and its score (requires correct rule identification first)

Each operation must use one of the following XML formats:

- Evaluate (e.g., evaluate path 1->2->4):
<query_eval>1->2->4</query_eval>

- Compare (e.g., compare path 1->2 with 1->3):
<query_compare>1->2 VS 1->3</query_compare>

- Identify Rule (e.g., identify as function B):
<identify_rule>B</identify_rule>

- Submit Final Answer (must include path and score):
<answer>path=1->2->4->9, score=50</answer>

- For "Evaluate": Returns "score=integer"
- For "Compare": Returns "path1 higher"/"path2 higher"/"equal"
- For "Identify Rule": Returns "correct" or "incorrect"
- For "Final Answer": Returns "victory" if rule is correct and path/score are optimal and correct; otherwise "failure"

Victory conditions:
- At least two "evaluations" performed
- Correctly identified the function
- Submitted origin-to-destination path is globally optimal under that function, and the score value is correct

Failure conditions:
- Incorrectly identified the rule
- Submitted path is not optimal
- Score value is incorrect
- Attempted to identify rule without at least two evaluations

Start your inference now.
"""

    contextualized_rule_zh_5 = """\
在企业商业合规审查中，我们需要对业务穿透审查路径的法律风险进行评估。系统设定了一棵固定的业务关联树，共15个节点（审查环节/关联公司），每个节点带有整数的基础违规风险指数。真实的风险计算模型在四个已知候选模型 A/B/C/D 中固定取其一，但对你保密。你的目标是：
1. 先判别当前采用的计算模型是哪一个
2. 再在该模型下求出违规风险得分最大的顶层公司到底层实控人（根到叶）完整审查路径及其得分

顶层审查层级/深度为0。节点标号与基础违规风险指数（括号内为指数）：
- 1(3)
  - 1的下层关联方：2(5)，3(2)
    - 2的下层关联方：4(4)，5(1)
      - 4的下层关联方：9(7)，10(0) [底层实控方/叶]
      - 5的下层关联方：11(9) [底层实控方/叶]
    - 3的下层关联方：6(6)，7(3)，8(2)
      - 6的下层关联方：12(1)，13(8) [底层实控方/叶]
      - 7的下层关联方：14(5) [底层实控方/叶]
      - 8的下层关联方：15(10) [底层实控方/叶]

- A: 路径风险得分 = 审查路径上所有节点基础风险指数之和
- B: 路径风险得分 = 审查路径上每个节点的"(层级+1)×基础风险指数"之和，其中顶层为0（随嵌套隐蔽性增加风险放大）
- C: 路径风险得分 = 审查路径上每个节点的"博弈符号×基础风险指数"之和，其中偶数层级符号为+1（控方证据加强，风险增加），奇数层级符号为-1（辩方合规抗辩，风险减免）
- D: 路径风险得分 = 审查路径上所有节点基础风险指数之和 + 连带责任惩罚，其中：
  - 若穿透至底层实控方（到达叶子），连带责任惩罚 = 路径上的最大基础风险指数
  - 若审查中止于中间环节（非叶前缀），连带责任惩罚 = 0

审查路径用"->"连接关联方编号，且顶层公司必须在最前，如"1->2->4->9"。路径可为前缀（中途环节）或完整（底层实控方）。

你可以发起以下操作（每次只能一个操作），系统会根据真实设定如实回答：

1. 评估：查询任意从顶层出发的审查路径风险得分（前缀或叶均可）
2. 比较：比较两条从顶层出发审查路径的风险得分
3. 认定规则：猜测当前采用的模型（需先完成至少两次评估）
4. 最终答案：提交你认为的最优完整审查路径及得分（需先正确认定规则）

每次操作必须使用以下 XML 格式之一：

- 评估（例如评估路径1->2->4）：
<query_eval>1->2->4</query_eval>

- 比较（例如比较路径1->2与1->3）：
<query_compare>1->2 VS 1->3</query_compare>

- 认定规则（例如认定为模型B）：
<identify_rule>B</identify_rule>

- 提交最终答案（必须包含路径和得分）：
<answer>路径=1->2->4->9, 得分=50</answer>

- 对"评估"：返回"得分=整数"
- 对"比较"：返回"路径1更高"/"路径2更高"/"相等"
- 对"认定规则"：返回"正确"或"错误"
- 对"最终答案"：若规则认定正确且路径与得分均为该规则下最优与正确，返回"胜利"，否则"失败"

胜利条件：
- 至少进行了两次"评估"
- 正确认定采用的模型
- 在该模型下，提交的完整审查路径为全局最优，且给出的得分数值正确

失败条件：
- 认定规则错误
- 提交的路径非最优
- 得分数值不正确
- 未进行至少两次"评估"就尝试认定规则

请开始你的推理。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
In corporate compliance reviews, we need to evaluate the legal risk of penetration review paths. The system features a fixed business affiliation tree with 15 nodes (review stages/affiliated companies), each carrying an integer basic violation risk index. The true risk calculation model is secretly selected from four known candidate models A/B/C/D. Your goal is to:
1. First identify which calculation model is being used
2. Then find the top-to-bottom (root-to-leaf) complete review path with the maximum risk score under that model and its score

Top company stage/level is 0. Node IDs and basic risk indices (indices in parentheses):
- 1(3)
  - Lower affiliates of 1: 2(5), 3(2)
    - Lower affiliates of 2: 4(4), 5(1)
      - Lower affiliates of 4: 9(7), 10(0) [bottom controller/leaf]
      - Lower affiliates of 5: 11(9) [bottom controller/leaf]
    - Lower affiliates of 3: 6(6), 7(3), 8(2)
      - Lower affiliates of 6: 12(1), 13(8) [bottom controller/leaf]
      - Lower affiliates of 7: 14(5) [bottom controller/leaf]
      - Lower affiliates of 8: 15(10) [bottom controller/leaf]

- A: Path risk score = sum of basic risk indices of all nodes on the review path
- B: Path risk score = sum of "(level+1) times basic risk index" for each node on the path, where top level is 0 (hidden nesting magnifies risk)
- C: Path risk score = sum of "game sign times basic risk index" for each node on the path, where sign is +1 for even level (prosecution evidence strengthens risk) and -1 for odd level (defense compliance mitigates risk)
- D: Path risk score = sum of basic risk indices of all nodes on the path + joint liability penalty, where:
  - If penetrating to the bottom controller (reaches leaf), joint liability penalty = maximum basic risk index on the path
  - If review stops at an intermediate stage (non-leaf prefix), joint liability penalty = 0

Review paths are represented by node IDs connected with "->", starting from origin, e.g., "1->2->4->9". Paths can be prefixes (intermediate stages) or complete (bottom controllers).

You can perform the following operations (one at a time), and the system will respond truthfully:

1. Evaluate: Query the risk score of any review path starting from the top company
2. Compare: Compare the risk scores of two review paths starting from the top company
3. Identify Rule: Guess which model is being used (requires at least two evaluations first)
4. Final Answer: Submit your answer for the optimal complete review path and its score (requires correct rule identification first)

Each operation must use one of the following XML formats:

- Evaluate (e.g., evaluate path 1->2->4):
<query_eval>1->2->4</query_eval>

- Compare (e.g., compare path 1->2 with 1->3):
<query_compare>1->2 VS 1->3</query_compare>

- Identify Rule (e.g., identify as model B):
<identify_rule>B</identify_rule>

- Submit Final Answer (must include path and score):
<answer>path=1->2->4->9, score=50</answer>

- For "Evaluate": Returns "score=integer"
- For "Compare": Returns "path1 higher"/"path2 higher"/"equal"
- For "Identify Rule": Returns "correct" or "incorrect"
- For "Final Answer": Returns "victory" if rule is correct and path/score are optimal and correct; otherwise "failure"

Victory conditions:
- At least two "evaluations" performed
- Correctly identified the model
- Submitted origin-to-destination path is globally optimal under that model, and the score value is correct

Failure conditions:
- Incorrectly identified the rule
- Submitted path is not optimal
- Score value is incorrect
- Attempted to identify rule without at least two evaluations

Start your inference now.
"""

    tags = ["answer", "query_eval", "query_compare", "identify_rule"]
    
    reasoning_type = "溯因推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "rule": "A",
                "optimal_path": ["1->2->4->9", "1->3->6->13"],
                "optimal_score": 19,
            },
            2: {
                "rule": "B",
                "optimal_path": ["1->3->6->13"],
                "optimal_score": 57,
            },
            3: {
                "rule": "C",
                "optimal_path": ["1->3->6->12"],
                "optimal_score": 6,
            },
            4: {
                "rule": "D",
                "optimal_path": ["1->2->5->11", "1->3->6->13", "1->3->8->15"],
                "optimal_score": 27,
            },
            5: {
                "rule": "D",
                "optimal_path": ["1->2->5->11", "1->3->6->13", "1->3->8->15"],
                "optimal_score": 27,
            },
        },
        "en": {
            1: {
                "rule": "A",
                "optimal_path": ["1->2->4->9", "1->3->6->13"],
                "optimal_score": 19,
            },
            2: {
                "rule": "B",
                "optimal_path": ["1->3->6->13"],
                "optimal_score": 57,
            },
            3: {
                "rule": "C",
                "optimal_path": ["1->3->6->12"],
                "optimal_score": 6,
            },
            4: {
                "rule": "D",
                "optimal_path": ["1->2->5->11", "1->3->6->13", "1->3->8->15"],
                "optimal_score": 27,
            },
            5: {
                "rule": "D",
                "optimal_path": ["1->2->5->11", "1->3->6->13", "1->3->8->15"],
                "optimal_score": 27,
            },
        },
    }

    def __init__(self, config):
        self.tree = {
            1: {"weight": 3, "depth": 0, "parent": None, "children": [2, 3], "is_leaf": False},
            2: {"weight": 5, "depth": 1, "parent": 1, "children": [4, 5], "is_leaf": False},
            3: {"weight": 2, "depth": 1, "parent": 1, "children": [6, 7, 8], "is_leaf": False},
            4: {"weight": 4, "depth": 2, "parent": 2, "children": [9, 10], "is_leaf": False},
            5: {"weight": 1, "depth": 2, "parent": 2, "children": [11], "is_leaf": False},
            6: {"weight": 6, "depth": 2, "parent": 3, "children": [12, 13], "is_leaf": False},
            7: {"weight": 3, "depth": 2, "parent": 3, "children": [14], "is_leaf": False},
            8: {"weight": 2, "depth": 2, "parent": 3, "children": [15], "is_leaf": False},
            9: {"weight": 7, "depth": 3, "parent": 4, "children": [], "is_leaf": True},
            10: {"weight": 0, "depth": 3, "parent": 4, "children": [], "is_leaf": True},
            11: {"weight": 9, "depth": 3, "parent": 5, "children": [], "is_leaf": True},
            12: {"weight": 1, "depth": 3, "parent": 6, "children": [], "is_leaf": True},
            13: {"weight": 8, "depth": 3, "parent": 6, "children": [], "is_leaf": True},
            14: {"weight": 5, "depth": 3, "parent": 7, "children": [], "is_leaf": True},
            15: {"weight": 10, "depth": 3, "parent": 8, "children": [], "is_leaf": True},
        }
        self.eval_count = 0 
        self.rule_identified = False 
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.true_rule = cfg["rule"]
        self.optimal_path = cfg["optimal_path"]
        self.optimal_score = cfg["optimal_score"]
        
        self._game_info = {}

    def _parse_path(self, path_str):
        path_str = path_str.strip()
        try:
            node_ids = [int(x.strip()) for x in path_str.split("->")]
            return node_ids
        except:
            return None

    def _validate_path(self, node_ids):
        if not node_ids or node_ids[0] != 1:
            return False
        
        for i in range(len(node_ids) - 1):
            current = node_ids[i]
            next_node = node_ids[i + 1]
            
            if current not in self.tree:
                return False
            if next_node not in self.tree[current]["children"]:
                return False
        
        return True

    def _calculate_score(self, node_ids, rule):
        if rule == "A":
            return sum(self.tree[nid]["weight"] for nid in node_ids)
        elif rule == "B":
            return sum((self.tree[nid]["depth"] + 1) * self.tree[nid]["weight"] for nid in node_ids)
        elif rule == "C":
            return sum(
                (1 if self.tree[nid]["depth"] % 2 == 0 else -1) * self.tree[nid]["weight"]
                for nid in node_ids
            )
        elif rule == "D":
            base_sum = sum(self.tree[nid]["weight"] for nid in node_ids)
            last_node = node_ids[-1]
            if self.tree[last_node]["is_leaf"]:
                bonus = max(self.tree[nid]["weight"] for nid in node_ids)
            else:
                bonus = 0
            return base_sum + bonus
        else:
            raise ValueError(f"Unknown rule: {rule}")

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        if not self.rule_identified:
            return False
        
        if self.config.language == "zh":
            path_pattern = r'路径\s*=\s*([\d\->]+)'
            score_pattern = r'得分\s*=\s*(-?\d+)'
        else:
            path_pattern = r'path\s*=\s*([\d\->]+)'
            score_pattern = r'score\s*=\s*(-?\d+)'
        
        path_match = re.search(path_pattern, raw_ans, re.IGNORECASE)
        score_match = re.search(score_pattern, raw_ans, re.IGNORECASE)
        
        if not path_match or not score_match:
            return False
        
        submitted_path = path_match.group(1).strip()
        try:
            submitted_score = int(score_match.group(1))
        except:
            return False
        
        if isinstance(self.optimal_path, list):
            path_correct = submitted_path in self.optimal_path
        else:
            path_correct = submitted_path == self.optimal_path
            
        return (path_correct and submitted_score == self.optimal_score)

    def produce_response(self, parsed_info):
        if "identify_rule" in parsed_info:
            return self._cf_core_produce(parsed_info)
        return super().produce_response(parsed_info)

    def _cf_core_produce(self, parsed_info):
        is_zh = self.config.language == "zh"
        
        if "query_eval" in parsed_info:
            self.eval_count += 1
            path_str = parsed_info["query_eval"].strip()
            node_ids = self._parse_path(path_str)
            
            if node_ids is None or not self._validate_path(node_ids):
                return "错误：路径格式无效或不是有效路径。" if is_zh else "Error: Invalid path format or path."
            
            score = self._calculate_score(node_ids, self.true_rule)
            return f"得分={score}" if is_zh else f"score={score}"
        
        elif "query_compare" in parsed_info:
            compare_str = parsed_info["query_compare"].strip()
            
            if " VS " in compare_str:
                parts = compare_str.split(" VS ")
            elif " vs " in compare_str:
                parts = compare_str.split(" vs ")
            else:
                return "错误：比较格式无效，请使用'路径1 VS 路径2'。" if is_zh else "Error: Invalid comparison format, use 'path1 VS path2'."
            
            if len(parts) != 2:
                return "错误：比较格式无效。" if is_zh else "Error: Invalid comparison format."
            
            path1_ids = self._parse_path(parts[0])
            path2_ids = self._parse_path(parts[1])
            
            if not path1_ids or not self._validate_path(path1_ids):
                return "错误：路径1无效。" if is_zh else "Error: Path1 invalid."
            if not path2_ids or not self._validate_path(path2_ids):
                return "错误：路径2无效。" if is_zh else "Error: Path2 invalid."
            
            score1 = self._calculate_score(path1_ids, self.true_rule)
            score2 = self._calculate_score(path2_ids, self.true_rule)
            
            if score1 > score2:
                return "路径1更高" if is_zh else "path1 higher"
            elif score2 > score1:
                return "路径2更高" if is_zh else "path2 higher"
            else:
                return "相等" if is_zh else "equal"
        
        elif "identify_rule" in parsed_info:
            if self.eval_count < 2:
                return "错误：需要至少进行两次评估后才能认定规则。" if is_zh else "Error: At least two evaluations required before identifying rule."
            
            guessed_rule = parsed_info["identify_rule"].strip().upper()
            
            if guessed_rule not in ["A", "B", "C", "D"]:
                return "错误：规则必须是A、B、C或D之一。" if is_zh else "Error: Rule must be one of A, B, C, or D."
            
            if guessed_rule == self.true_rule:
                self.rule_identified = True
                return "正确" if is_zh else "correct"
            else:
                self.state.set_state("failed", "incorrect rule identification")
                return "错误" if is_zh else "incorrect"
        
        else:
            return "错误：无效的查询类型。" if is_zh else "Error: Invalid query type."

    def _cf_make_wrong(self, correct: str) -> str:
        is_zh = self.config.language == "zh"
        
        if is_zh:
            m = re.search(r'得分=(-?\d+)', correct)
        else:
            m = re.search(r'score=(-?\d+)', correct)
        
        if m:
            original_score = int(m.group(1))
            wrong_score = original_score + 10  
            if is_zh:
                return f"得分={wrong_score}"
            else:
                return f"score={wrong_score}"
        
        if correct in ("路径1更高", "path1 higher"):
            return "路径2更高" if is_zh else "path2 higher"
        if correct in ("路径2更高", "path2 higher"):
            return "路径1更高" if is_zh else "path1 higher"
        if correct in ("相等", "equal"):
            return "路径1更高" if is_zh else "path1 higher"
        
        if correct in ("正确", "correct"):
            return "错误" if is_zh else "incorrect"
        if correct in ("错误", "incorrect"):
            return "正确" if is_zh else "correct"
        
        return correct + (" (数据异常)" if is_zh else " (data anomaly)")

    def get_all_possible_queries(self) -> list[dict]:
        all_paths = []
        stack = [[1]]
        
        while stack:
            curr_path = stack.pop()
            all_paths.append(curr_path)
            
            last_node = curr_path[-1]
            children = self.tree[last_node]["children"]
            
            for child in children:
                stack.append(curr_path + [child])
        
        queries = []
        is_zh = self.config.language == "zh"
        
        for path_ids in all_paths:
            path_str = "->".join(str(nid) for nid in path_ids)
            score = self._calculate_score(path_ids, self.true_rule)
            
            ans_str = f"得分={score}" if is_zh else f"score={score}"
            
            queries.append({
                "query": f"<query_eval>{path_str}</query_eval>",
                "answer": ans_str
            })
            
        for p1_ids in all_paths:
            for p2_ids in all_paths:
                p1_str = "->".join(str(nid) for nid in p1_ids)
                p2_str = "->".join(str(nid) for nid in p2_ids)
                
                s1 = self._calculate_score(p1_ids, self.true_rule)
                s2 = self._calculate_score(p2_ids, self.true_rule)
                
                if s1 > s2:
                    res = "路径1更高" if is_zh else "path1 higher"
                elif s2 > s1:
                    res = "路径2更高" if is_zh else "path2 higher"
                else:
                    res = "相等" if is_zh else "equal"
                    
                queries.append({
                    "query": f"<query_compare>{p1_str} VS {p2_str}</query_compare>",
                    "answer": res
                })
                
        return queries