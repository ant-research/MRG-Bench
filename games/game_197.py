from .base import Game
import re


class HiddenFunctionDeductionGame(Game):

    game_rule_zh = """\
我们现在来玩一个"隐藏函数推理"游戏，规则如下：

游戏设定了一个有限集合 V = {{A, B, C, D, E, F, G, H}}，每个元素都有一个公开的三位数字编码：
- A: {code_A}
- B: {code_B}
- C: {code_C}
- D: {code_D}
- E: {code_E}
- F: {code_F}
- G: {code_G}
- H: {code_H}

在这个集合上定义了一个无向完全图，任意两个不同元素之间都存在一条边。每条边都有一个权值，由一个隐藏的确定性对称函数 f 计算得出：边权 w(X,Y) = f(code(X), code(Y)).

该函数 f 具有以下性质：
1. 对称性：f(x,y) = f(y,x)
2. 输出为非负整数
3. 函数在整个游戏过程中保持不变，仅依赖于两端点的三位数字编码

你的目标是通过有限次的查询，推断出隐藏函数 f 的规律，并在挑战阶段准确预测5条未查询过的边的权值。

## 可用操作

1. **边权查询**：查询任意两个不同节点之间的边权值
2. **余量查询**：查询剩余可用的边权查询次数
3. **发起挑战**：随时可以发起，系统会给出5对未被查询过的节点对，你需要预测它们的边权
4. **最终预测提交**：对挑战阶段给出的5对节点，提交你预测的边权值

## 操作格式（必须严格遵守）

**边权查询**（查询节点 X 和 Y 之间的边权，X 和 Y 必须不同且都在 {{A,B,C,D,E,F,G,H}} 中）：
<query_edge>X,Y</query_edge>

**余量查询**（查询剩余查询次数）：
<query_remaining></query_remaining>

**发起挑战**（请求系统给出5对待预测的节点对）：
<request_challenge></request_challenge>

**最终预测提交**（对挑战给出的5对节点预测边权，格式为"节点1 节点2 = 权值"，用分号分隔）：
<answer>X1 Y1 = v1; X2 Y2 = v2; X3 Y3 = v3; X4 Y4 = v4; X5 Y5 = v5</answer>

## 资源限制

- 边权查询总次数上限：{max_queries} 次
- 必须在用尽查询次数前发起挑战

## 成功与失败条件

**成功**：在挑战阶段对5条目标边全部预测正确（5/5）

**失败**（任一条件成立即失败）：
1. 用尽所有边权查询次数仍未发起挑战
2. 挑战后的5条预测未全部命中
3. 在挑战阶段尝试继续进行边权查询
4. 查询格式错误或查询无效节点

## 游戏流程示例

1. 你可以先进行若干次边权查询，例如：<query_edge>A,B</query_edge>
2. 系统返回边权值，例如："边 A-B 的权值为 5"
3. 你可以随时查询余量：<query_remaining></query_remaining>
4. 当你认为已经掌握规律时，发起挑战：<request_challenge></request_challenge>
5. 系统给出5对节点，例如："(B,E), (C,H), (A,G), (D,F), (E,G)"
6. 你提交预测：<answer>B E = 10; C H = 7; A G = 3; D F = 8; E G = 12</answer>
7. 系统判定是否全部正确

注意：查询设计应覆盖多种编码差异模式，以提高对隐藏函数的辨识度。尽可能用最少的查询次数找出规律。
"""

    game_rule_en = """\
Let's play a "Hidden Function Deduction" game. Here are the rules:

The game defines a finite set V = {{A, B, C, D, E, F, G, H}}, where each element has a public three-digit code:
- A: {code_A}
- B: {code_B}
- C: {code_C}
- D: {code_D}
- E: {code_E}
- F: {code_F}
- G: {code_G}
- H: {code_H}

An undirected complete graph is defined on this set, with an edge between any two different elements. Each edge has a weight calculated by a hidden deterministic symmetric function f: w(X,Y) = f(code(X), code(Y)).

The function f has the following properties:
1. Symmetry: f(x,y) = f(y,x)
2. Outputs non-negative integers
3. The function remains constant throughout the game and depends only on the three-digit codes of the endpoints

Your goal is to infer the pattern of the hidden function f through limited queries, and accurately predict the weights of 5 unqueried edges in the challenge phase.

## Available Operations

1. **Edge Weight Query**: Query the edge weight between any two different nodes
2. **Remaining Query**: Check the number of remaining edge weight queries
3. **Request Challenge**: Can be initiated at any time; the system will provide 5 pairs of unqueried node pairs for prediction
4. **Final Prediction Submission**: Submit your predicted edge weights for the 5 pairs given in the challenge phase

## Operation Format (must be strictly followed)

**Edge Weight Query** (query edge weight between nodes X and Y, where X and Y must be different and both in {{A,B,C,D,E,F,G,H}}):
<query_edge>X,Y</query_edge>

**Remaining Query** (check remaining query count):
<query_remaining></query_remaining>

**Request Challenge** (request system to provide 5 pairs of nodes to predict):
<request_challenge></request_challenge>

**Final Prediction Submission** (predict edge weights for the 5 pairs given in challenge, format "node1 node2 = weight", separated by semicolons):
<answer>X1 Y1 = v1; X2 Y2 = v2; X3 Y3 = v3; X4 Y4 = v4; X5 Y5 = v5</answer>

## Resource Limits

- Maximum edge weight queries: {max_queries}
- Must request challenge before exhausting all queries

## Success and Failure Conditions

**Success**: All 5 predictions in the challenge phase are correct (5/5)

**Failure** (game fails if any condition is met):
1. All edge weight queries exhausted without requesting challenge
2. Not all 5 predictions in challenge phase are correct
3. Attempting to continue edge weight queries during challenge phase
4. Query format error or querying invalid nodes

## Example Game Flow

1. You can start with several edge weight queries, e.g.: <query_edge>A,B</query_edge>
2. System returns edge weight, e.g.: "Edge A-B has weight 5"
3. You can check remaining queries anytime: <query_remaining></query_remaining>
4. When you think you've found the pattern, request challenge: <request_challenge></request_challenge>
5. System provides 5 pairs, e.g.: "(B,E), (C,H), (A,G), (D,F), (E,G)"
6. You submit predictions: <answer>B E = 10; C H = 7; A G = 3; D F = 8; E G = 12</answer>
7. System determines if all predictions are correct

Note: Query design should cover various encoding difference patterns to improve identification of the hidden function. Try to find the pattern with as few queries as possible.
"""

    contextualized_rule_zh_1 = """\
欢迎使用“区域交通通行阻抗评估系统”。
本系统设定了有限的交通枢纽集合 V = {{A, B, C, D, E, F, G, H}}，每个枢纽都有一个公开的三位枢纽特征码（代表流量、密度、路网等级等）：
- 枢纽 A: {code_A}
- 枢纽 B: {code_B}
- 枢纽 C: {code_C}
- 枢纽 D: {code_D}
- 枢纽 E: {code_E}
- 枢纽 F: {code_F}
- 枢纽 G: {code_G}
- 枢纽 H: {code_H}

在规划网络中，任意两个不同枢纽之间都存在一条直达连线。每条连线的建设成本/通行阻抗由一个隐藏的确定性对称评估模型 f 计算得出：通行阻抗 w(X,Y) = f(code(X), code(Y)).

该模型 f 具有以下性质：
1. 对称性：f(x,y) = f(y,x)
2. 输出为非负整数
3. 评估模型在整个规划过程中保持不变，仅依赖于两端点的三位枢纽特征码

你的目标是通过有限次的评估查询，推断出隐藏评估模型 f 的规律，并在挑战阶段准确预测5条未查询过的连线的通行阻抗。

## 可用操作

1. **阻抗查询**：查询任意两个不同枢纽之间的通行阻抗
2. **余量查询**：查询剩余可用的查询次数
3. **发起挑战**：随时可以发起，系统会给出5对未被查询过的枢纽对，你需要预测它们的阻抗
4. **最终预测提交**：对挑战阶段给出的5对枢纽，提交你预测的通行阻抗值

## 操作格式（必须严格遵守）

**阻抗查询**（查询枢纽 X 和 Y 之间的阻抗，X 和 Y 必须不同且都在 {{A,B,C,D,E,F,G,H}} 中）：
<query_edge>X,Y</query_edge>

**余量查询**（查询剩余查询次数）：
<query_remaining></query_remaining>

**发起挑战**（请求系统给出5对待预测的枢纽对）：
<request_challenge></request_challenge>

**最终预测提交**（对挑战给出的5对枢纽预测阻抗，格式为"枢纽1 枢纽2 = 阻抗值"，用分号分隔）：
<answer>X1 Y1 = v1; X2 Y2 = v2; X3 Y3 = v3; X4 Y4 = v4; X5 Y5 = v5</answer>

## 资源限制

- 阻抗查询总次数上限：{max_queries} 次
- 必须在用尽查询次数前发起挑战

## 成功与失败条件

**成功**：在挑战阶段对5条目标连线全部预测正确（5/5）

**失败**（任一条件成立即失败）：
1. 用尽所有阻抗查询次数仍未发起挑战
2. 挑战后的5条预测未全部命中
3. 在挑战阶段尝试继续进行阻抗查询
4. 查询格式错误或查询无效枢纽

## 游戏流程示例

1. 你可以先进行若干次阻抗查询，例如：<query_edge>A,B</query_edge>
2. 系统返回阻抗值，例如："边 A-B 的权值为 5"
3. 你可以随时查询余量：<query_remaining></query_remaining>
4. 当你认为已经掌握规律时，发起挑战：<request_challenge></request_challenge>
5. 系统给出5对枢纽，例如："(B,E), (C,H), (A,G), (D,F), (E,G)"
6. 你提交预测：<answer>B E = 10; C H = 7; A G = 3; D F = 8; E G = 12</answer>
7. 系统判定是否全部正确

注意：查询设计应覆盖多种特征码差异模式，以提高对隐藏评估模型的辨识度。尽可能用最少的查询次数找出规律。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Regional Traffic Impedance Assessment System".

The system defines a finite set of traffic hubs V = {{A, B, C, D, E, F, G, H}}, where each hub has a public three-digit feature code (representing traffic volume, density, road network level, etc.):
- Hub A: {code_A}
- Hub B: {code_B}
- Hub C: {code_C}
- Hub D: {code_D}
- Hub E: {code_E}
- Hub F: {code_F}
- Hub G: {code_G}
- Hub H: {code_H}

In the planning network, there is a direct link between any two different hubs. The construction cost / traffic impedance of each link is calculated by a hidden deterministic symmetric assessment model f: impedance w(X,Y) = f(code(X), code(Y)).

The model f has the following properties:
1. Symmetry: f(x,y) = f(y,x)
2. Outputs non-negative integers
3. The assessment model remains constant throughout the planning process and depends only on the three-digit feature codes of the endpoints

Your goal is to infer the pattern of the hidden assessment model f through limited queries, and accurately predict the impedances of 5 unqueried links in the challenge phase.

## Available Operations

1. **Impedance Query**: Query the traffic impedance between any two different hubs
2. **Remaining Query**: Check the number of remaining impedance queries
3. **Request Challenge**: Can be initiated at any time; the system will provide 5 pairs of unqueried hubs for prediction
4. **Final Prediction Submission**: Submit your predicted impedances for the 5 pairs given in the challenge phase

## Operation Format (must be strictly followed)

**Impedance Query** (query impedance between hubs X and Y, where X and Y must be different and both in {{A,B,C,D,E,F,G,H}}):
<query_edge>X,Y</query_edge>

**Remaining Query** (check remaining query count):
<query_remaining></query_remaining>

**Request Challenge** (request system to provide 5 pairs of hubs to predict):
<request_challenge></request_challenge>

**Final Prediction Submission** (predict impedances for the 5 pairs given in challenge, format "hub1 hub2 = impedance", separated by semicolons):
<answer>X1 Y1 = v1; X2 Y2 = v2; X3 Y3 = v3; X4 Y4 = v4; X5 Y5 = v5</answer>

## Resource Limits

- Maximum impedance queries: {max_queries}
- Must request challenge before exhausting all queries

## Success and Failure Conditions

**Success**: All 5 predictions in the challenge phase are correct (5/5)

**Failure** (game fails if any condition is met):
1. All impedance queries exhausted without requesting challenge
2. Not all 5 predictions in challenge phase are correct
3. Attempting to continue impedance queries during challenge phase
4. Query format error or querying invalid hubs

## Example Game Flow

1. You can start with several impedance queries, e.g.: <query_edge>A,B</query_edge>
2. System returns impedance, e.g.: "Edge A-B has weight 5"
3. You can check remaining queries anytime: <query_remaining></query_remaining>
4. When you think you've found the pattern, request challenge: <request_challenge></request_challenge>
5. System provides 5 pairs, e.g.: "(B,E), (C,H), (A,G), (D,F), (E,G)"
6. You submit predictions: <answer>B E = 10; C H = 7; A G = 3; D F = 8; E G = 12</answer>
7. System determines if all predictions are correct

Note: Query design should cover various encoding difference patterns to improve identification of the hidden assessment model. Try to find the pattern with as few queries as possible.
"""

    contextualized_rule_zh_2 = """\
欢迎进入“靶点药物相互作用测算平台”。
系统筛选出一个包含核心候选药物分子/靶点蛋白的集合 V = {{A, B, C, D, E, F, G, H}}，每个分子都有一个公开的三位分子特征指纹（代表疏水性、极性、分子量指标）：
- 分子 A: {code_A}
- 分子 B: {code_B}
- 分子 C: {code_C}
- 分子 D: {code_D}
- 分子 E: {code_E}
- 分子 F: {code_F}
- 分子 G: {code_G}
- 分子 H: {code_H}

在这个药理反应网络中，任意两个不同分子之间都存在潜在的相互作用。每次相互作用的强度/协同效能由一个隐藏的确定性对称效能测算机制 f 计算得出：作用强度 w(X,Y) = f(code(X), code(Y)).

该机制 f 具有以下性质：
1. 对称性：f(x,y) = f(y,x)
2. 输出为非负整数
3. 测算机制在整个研发过程中保持不变，仅依赖于作用两端的三位分子特征指纹

你的目标是通过有限次的实验测定查询，推断出隐藏效能测算机制 f 的规律，并在挑战阶段准确预测5对未查询过的分子间的相互作用强度。

## 可用操作

1. **效能查询**：查询任意两个不同分子之间的协同作用强度
2. **余量查询**：查询剩余可用的查询次数
3. **发起挑战**：随时可以发起，系统会给出5对未被查询过的分子对，你需要预测它们的相互作用强度
4. **最终预测提交**：对挑战阶段给出的5对分子，提交你预测的协同效能值

## 操作格式（必须严格遵守）

**效能查询**（查询分子 X 和 Y 之间的强度，X 和 Y 必须不同且都在 {{A,B,C,D,E,F,G,H}} 中）：
<query_edge>X,Y</query_edge>

**余量查询**（查询剩余查询次数）：
<query_remaining></query_remaining>

**发起挑战**（请求系统给出5对待预测的分子对）：
<request_challenge></request_challenge>

**最终预测提交**（对挑战给出的5对分子预测强度，格式为"分子1 分子2 = 强度值"，用分号分隔）：
<answer>X1 Y1 = v1; X2 Y2 = v2; X3 Y3 = v3; X4 Y4 = v4; X5 Y5 = v5</answer>

## 资源限制

- 效能查询总次数上限：{max_queries} 次
- 必须在用尽查询次数前发起挑战

## 成功与失败条件

**成功**：在挑战阶段对5对目标分子相互作用强度全部预测正确（5/5）

**失败**（任一条件成立即失败）：
1. 用尽所有效能查询次数仍未发起挑战
2. 挑战后的5条预测未全部命中
3. 在挑战阶段尝试继续进行效能查询
4. 查询格式错误或查询无效分子

## 游戏流程示例

1. 你可以先进行若干次效能查询，例如：<query_edge>A,B</query_edge>
2. 系统返回效能值，例如："边 A-B 的权值为 5"
3. 你可以随时查询余量：<query_remaining></query_remaining>
4. 当你认为已经掌握规律时，发起挑战：<request_challenge></request_challenge>
5. 系统给出5对分子，例如："(B,E), (C,H), (A,G), (D,F), (E,G)"
6. 你提交预测：<answer>B E = 10; C H = 7; A G = 3; D F = 8; E G = 12</answer>
7. 系统判定是否全部正确

注意：查询设计应覆盖多种特征指纹差异模式，以提高对隐藏效能测算机制的辨识度。尽可能用最少的查询次数找出规律。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Target-Drug Interaction Assessment Platform".

The system has screened a core set of candidate drug molecules / target proteins V = {{A, B, C, D, E, F, G, H}}, where each molecule has a public three-digit molecular feature fingerprint (representing hydrophobicity, polarity, and molecular weight indicators):
- Molecule A: {code_A}
- Molecule B: {code_B}
- Molecule C: {code_C}
- Molecule D: {code_D}
- Molecule E: {code_E}
- Molecule F: {code_F}
- Molecule G: {code_G}
- Molecule H: {code_H}

In this pharmacological reaction network, there is potential interaction between any two different molecules. The interaction strength / synergistic efficacy is calculated by a hidden deterministic symmetric efficacy calculation mechanism f: interaction strength w(X,Y) = f(code(X), code(Y)).

The mechanism f has the following properties:
1. Symmetry: f(x,y) = f(y,x)
2. Outputs non-negative integers
3. The calculation mechanism remains constant throughout the R&D process and depends only on the three-digit molecular feature fingerprints of the two interacting ends

Your goal is to infer the pattern of the hidden efficacy calculation mechanism f through limited experimental queries, and accurately predict the interaction strengths of 5 unqueried molecular pairs in the challenge phase.

## Available Operations

1. **Efficacy Query**: Query the interaction strength between any two different molecules
2. **Remaining Query**: Check the number of remaining efficacy queries
3. **Request Challenge**: Can be initiated at any time; the system will provide 5 pairs of unqueried molecules for prediction
4. **Final Prediction Submission**: Submit your predicted interaction strengths for the 5 pairs given in the challenge phase

## Operation Format (must be strictly followed)

**Efficacy Query** (query interaction strength between molecules X and Y, where X and Y must be different and both in {{A,B,C,D,E,F,G,H}}):
<query_edge>X,Y</query_edge>

**Remaining Query** (check remaining query count):
<query_remaining></query_remaining>

**Request Challenge** (request system to provide 5 pairs of molecules to predict):
<request_challenge></request_challenge>

**Final Prediction Submission** (predict interaction strengths for the 5 pairs given in challenge, format "molecule1 molecule2 = strength", separated by semicolons):
<answer>X1 Y1 = v1; X2 Y2 = v2; X3 Y3 = v3; X4 Y4 = v4; X5 Y5 = v5</answer>

## Resource Limits

- Maximum efficacy queries: {max_queries}
- Must request challenge before exhausting all queries

## Success and Failure Conditions

**Success**: All 5 predictions in the challenge phase are correct (5/5)

**Failure** (game fails if any condition is met):
1. All efficacy queries exhausted without requesting challenge
2. Not all 5 predictions in challenge phase are correct
3. Attempting to continue efficacy queries during challenge phase
4. Query format error or querying invalid molecules

## Example Game Flow

1. You can start with several efficacy queries, e.g.: <query_edge>A,B</query_edge>
2. System returns efficacy value, e.g.: "Edge A-B has weight 5"
3. You can check remaining queries anytime: <query_remaining></query_remaining>
4. When you think you've found the pattern, request challenge: <request_challenge></request_challenge>
5. System provides 5 pairs, e.g.: "(B,E), (C,H), (A,G), (D,F), (E,G)"
6. You submit predictions: <answer>B E = 10; C H = 7; A G = 3; D F = 8; E G = 12</answer>
7. System determines if all predictions are correct

Note: Query design should cover various feature fingerprint difference patterns to improve identification of the hidden efficacy calculation mechanism. Try to find the pattern with as few queries as possible.
"""

    contextualized_rule_zh_3 = """\
欢迎体验“课程体系认知迁移图谱”。
本系统构建了核心的知识模块集合 V = {{A, B, C, D, E, F, G, H}}，每个模块都有一个公开的三位模块维度系数（分别代表难度、理论性、实践性）：
- 模块 A: {code_A}
- 模块 B: {code_B}
- 模块 C: {code_C}
- 模块 D: {code_D}
- 模块 E: {code_E}
- 模块 F: {code_F}
- 模块 G: {code_G}
- 模块 H: {code_H}

在学习路径图中，任意两个不同模块之间都可进行跨度衔接。两个模块之间的知识迁移成本/学习过渡难度由一个隐藏的确定性对称认知距离函数 f 计算得出：迁移成本 w(X,Y) = f(code(X), code(Y)).

该函数 f 具有以下性质：
1. 对称性：f(x,y) = f(y,x)
2. 输出为非负整数
3. 认知距离函数在整个测评过程中保持不变，仅依赖于两端点的三位模块维度系数

你的目标是通过有限次的测评查询，推断出隐藏认知距离函数 f 的规律，并在挑战阶段准确预测5对未查询过的模块的知识迁移成本。

## 可用操作

1. **迁移成本查询**：查询任意两个不同模块之间的知识迁移成本
2. **余量查询**：查询剩余可用的查询次数
3. **发起挑战**：随时可以发起，系统会给出5对未被查询过的模块对，你需要预测它们的迁移成本
4. **最终预测提交**：对挑战阶段给出的5对模块，提交你预测的迁移成本值

## 操作格式（必须严格遵守）

**迁移成本查询**（查询模块 X 和 Y 之间的成本，X 和 Y 必须不同且都在 {{A,B,C,D,E,F,G,H}} 中）：
<query_edge>X,Y</query_edge>

**余量查询**（查询剩余查询次数）：
<query_remaining></query_remaining>

**发起挑战**（请求系统给出5对待预测的模块对）：
<request_challenge></request_challenge>

**最终预测提交**（对挑战给出的5对模块预测成本，格式为"模块1 模块2 = 成本值"，用分号分隔）：
<answer>X1 Y1 = v1; X2 Y2 = v2; X3 Y3 = v3; X4 Y4 = v4; X5 Y5 = v5</answer>

## 资源限制

- 成本查询总次数上限：{max_queries} 次
- 必须在用尽查询次数前发起挑战

## 成功与失败条件

**成功**：在挑战阶段对5对目标模块迁移成本全部预测正确（5/5）

**失败**（任一条件成立即失败）：
1. 用尽所有成本查询次数仍未发起挑战
2. 挑战后的5条预测未全部命中
3. 在挑战阶段尝试继续进行成本查询
4. 查询格式错误或查询无效模块

## 游戏流程示例

1. 你可以先进行若干次成本查询，例如：<query_edge>A,B</query_edge>
2. 系统返回成本值，例如："边 A-B 的权值为 5"
3. 你可以随时查询余量：<query_remaining></query_remaining>
4. 当你认为已经掌握规律时，发起挑战：<request_challenge></request_challenge>
5. 系统给出5对模块，例如："(B,E), (C,H), (A,G), (D,F), (E,G)"
6. 你提交预测：<answer>B E = 10; C H = 7; A G = 3; D F = 8; E G = 12</answer>
7. 系统判定是否全部正确

注意：查询设计应覆盖多种维度系数差异模式，以提高对隐藏认知距离函数的辨识度。尽可能用最少的查询次数找出规律。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Curriculum System Cognitive Transfer Graph".

The system constructs a core set of knowledge modules V = {{A, B, C, D, E, F, G, H}}, where each module has a public three-digit module dimensional coefficient (representing difficulty, theoretical depth, and practicality respectively):
- Module A: {code_A}
- Module B: {code_B}
- Module C: {code_C}
- Module D: {code_D}
- Module E: {code_E}
- Module F: {code_F}
- Module G: {code_G}
- Module H: {code_H}

In the learning path graph, any two different modules can be bridged. The knowledge transfer cost / learning transition difficulty between two modules is calculated by a hidden deterministic symmetric cognitive distance function f: transfer cost w(X,Y) = f(code(X), code(Y)).

The function f has the following properties:
1. Symmetry: f(x,y) = f(y,x)
2. Outputs non-negative integers
3. The cognitive distance function remains constant throughout the assessment process and depends only on the three-digit module dimensional coefficients of the endpoints

Your goal is to infer the pattern of the hidden cognitive distance function f through limited assessment queries, and accurately predict the knowledge transfer costs of 5 unqueried module pairs in the challenge phase.

## Available Operations

1. **Transfer Cost Query**: Query the knowledge transfer cost between any two different modules
2. **Remaining Query**: Check the number of remaining cost queries
3. **Request Challenge**: Can be initiated at any time; the system will provide 5 pairs of unqueried modules for prediction
4. **Final Prediction Submission**: Submit your predicted transfer costs for the 5 pairs given in the challenge phase

## Operation Format (must be strictly followed)

**Transfer Cost Query** (query transfer cost between modules X and Y, where X and Y must be different and both in {{A,B,C,D,E,F,G,H}}):
<query_edge>X,Y</query_edge>

**Remaining Query** (check remaining query count):
<query_remaining></query_remaining>

**Request Challenge** (request system to provide 5 pairs of modules to predict):
<request_challenge></request_challenge>

**Final Prediction Submission** (predict transfer costs for the 5 pairs given in challenge, format "module1 module2 = cost", separated by semicolons):
<answer>X1 Y1 = v1; X2 Y2 = v2; X3 Y3 = v3; X4 Y4 = v4; X5 Y5 = v5</answer>

## Resource Limits

- Maximum transfer cost queries: {max_queries}
- Must request challenge before exhausting all queries

## Success and Failure Conditions

**Success**: All 5 predictions in the challenge phase are correct (5/5)

**Failure** (game fails if any condition is met):
1. All cost queries exhausted without requesting challenge
2. Not all 5 predictions in challenge phase are correct
3. Attempting to continue cost queries during challenge phase
4. Query format error or querying invalid modules

## Example Game Flow

1. You can start with several cost queries, e.g.: <query_edge>A,B</query_edge>
2. System returns cost value, e.g.: "Edge A-B has weight 5"
3. You can check remaining queries anytime: <query_remaining></query_remaining>
4. When you think you've found the pattern, request challenge: <request_challenge></request_challenge>
5. System provides 5 pairs, e.g.: "(B,E), (C,H), (A,G), (D,F), (E,G)"
6. You submit predictions: <answer>B E = 10; C H = 7; A G = 3; D F = 8; E G = 12</answer>
7. System determines if all predictions are correct

Note: Query design should cover various coefficient difference patterns to improve identification of the hidden cognitive distance function. Try to find the pattern with as few queries as possible.
"""

    contextualized_rule_zh_4 = """\
欢迎进入“智能制造工序切换耗损测算系统”。
本系统定义了关键生产工序的集合 V = {{A, B, C, D, E, F, G, H}}，每个工序都有一个公开的三位工序参数（分别代表加工温度、运行压力、标准时间）：
- 工序 A: {code_A}
- 工序 B: {code_B}
- 工序 C: {code_C}
- 工序 D: {code_D}
- 工序 E: {code_E}
- 工序 F: {code_F}
- 工序 G: {code_G}
- 工序 H: {code_H}

在柔性生产线上，任意两个不同工序之间都可以进行产线切换。每次切换产生的物流损耗/切换成本由一个隐藏的确定性对称损耗计算函数 f 评估得出：切换损耗 w(X,Y) = f(code(X), code(Y)).

该损耗计算函数 f 具有以下性质：
1. 对称性：f(x,y) = f(y,x)
2. 输出为非负整数
3. 损耗计算函数在整个排产过程中保持不变，仅依赖于两端工序的三位工序参数

你的目标是通过有限次的损耗查询，推断出隐藏损耗计算函数 f 的规律，并在挑战阶段准确预测5对未查询过的工序切换损耗。

## 可用操作

1. **损耗查询**：查询任意两个不同工序之间的切换损耗
2. **余量查询**：查询剩余可用的查询次数
3. **发起挑战**：随时可以发起，系统会给出5对未被查询过的工序对，你需要预测它们的切换损耗
4. **最终预测提交**：对挑战阶段给出的5对工序，提交你预测的切换损耗值

## 操作格式（必须严格遵守）

**损耗查询**（查询工序 X 和 Y 之间的损耗，X 和 Y 必须不同且都在 {{A,B,C,D,E,F,G,H}} 中）：
<query_edge>X,Y</query_edge>

**余量查询**（查询剩余查询次数）：
<query_remaining></query_remaining>

**发起挑战**（请求系统给出5对待预测的工序对）：
<request_challenge></request_challenge>

**最终预测提交**（对挑战给出的5对工序预测损耗，格式为"工序1 工序2 = 损耗值"，用分号分隔）：
<answer>X1 Y1 = v1; X2 Y2 = v2; X3 Y3 = v3; X4 Y4 = v4; X5 Y5 = v5</answer>

## 资源限制

- 损耗查询总次数上限：{max_queries} 次
- 必须在用尽查询次数前发起挑战

## 成功与失败条件

**成功**：在挑战阶段对5对目标工序切换损耗全部预测正确（5/5）

**失败**（任一条件成立即失败）：
1. 用尽所有损耗查询次数仍未发起挑战
2. 挑战后的5条预测未全部命中
3. 在挑战阶段尝试继续进行损耗查询
4. 查询格式错误或查询无效工序

## 游戏流程示例

1. 你可以先进行若干次损耗查询，例如：<query_edge>A,B</query_edge>
2. 系统返回损耗值，例如："边 A-B 的权值为 5"
3. 你可以随时查询余量：<query_remaining></query_remaining>
4. 当你认为已经掌握规律时，发起挑战：<request_challenge></request_challenge>
5. 系统给出5对工序，例如："(B,E), (C,H), (A,G), (D,F), (E,G)"
6. 你提交预测：<answer>B E = 10; C H = 7; A G = 3; D F = 8; E G = 12</answer>
7. 系统判定是否全部正确

注意：查询设计应覆盖多种工序参数差异模式，以提高对隐藏损耗计算函数的辨识度。尽可能用最少的查询次数找出规律。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the "Smart Manufacturing Process Changeover Loss Calculation System".

The system defines a set of key production processes V = {{A, B, C, D, E, F, G, H}}, where each process has a public three-digit process parameter (representing processing temperature, operating pressure, and standard time respectively):
- Process A: {code_A}
- Process B: {code_B}
- Process C: {code_C}
- Process D: {code_D}
- Process E: {code_E}
- Process F: {code_F}
- Process G: {code_G}
- Process H: {code_H}

On a flexible production line, changeovers can be made between any two different processes. The material loss / changeover cost incurred by each changeover is evaluated by a hidden deterministic symmetric loss calculation function f: changeover loss w(X,Y) = f(code(X), code(Y)).

The loss calculation function f has the following properties:
1. Symmetry: f(x,y) = f(y,x)
2. Outputs non-negative integers
3. The loss calculation function remains constant throughout the scheduling process and depends only on the three-digit process parameters of the two end processes

Your goal is to infer the pattern of the hidden loss calculation function f through limited loss queries, and accurately predict the changeover losses of 5 unqueried process pairs in the challenge phase.

## Available Operations

1. **Loss Query**: Query the changeover loss between any two different processes
2. **Remaining Query**: Check the number of remaining loss queries
3. **Request Challenge**: Can be initiated at any time; the system will provide 5 pairs of unqueried processes for prediction
4. **Final Prediction Submission**: Submit your predicted changeover losses for the 5 pairs given in the challenge phase

## Operation Format (must be strictly followed)

**Loss Query** (query loss between processes X and Y, where X and Y must be different and both in {{A,B,C,D,E,F,G,H}}):
<query_edge>X,Y</query_edge>

**Remaining Query** (check remaining query count):
<query_remaining></query_remaining>

**Request Challenge** (request system to provide 5 pairs of processes to predict):
<request_challenge></request_challenge>

**Final Prediction Submission** (predict losses for the 5 pairs given in challenge, format "process1 process2 = loss", separated by semicolons):
<answer>X1 Y1 = v1; X2 Y2 = v2; X3 Y3 = v3; X4 Y4 = v4; X5 Y5 = v5</answer>

## Resource Limits

- Maximum loss queries: {max_queries}
- Must request challenge before exhausting all queries

## Success and Failure Conditions

**Success**: All 5 predictions in the challenge phase are correct (5/5)

**Failure** (game fails if any condition is met):
1. All loss queries exhausted without requesting challenge
2. Not all 5 predictions in challenge phase are correct
3. Attempting to continue loss queries during challenge phase
4. Query format error or querying invalid processes

## Example Game Flow

1. You can start with several loss queries, e.g.: <query_edge>A,B</query_edge>
2. System returns loss value, e.g.: "Edge A-B has weight 5"
3. You can check remaining queries anytime: <query_remaining></query_remaining>
4. When you think you've found the pattern, request challenge: <request_challenge></request_challenge>
5. System provides 5 pairs, e.g.: "(B,E), (C,H), (A,G), (D,F), (E,G)"
6. You submit predictions: <answer>B E = 10; C H = 7; A G = 3; D F = 8; E G = 12</answer>
7. System determines if all predictions are correct

Note: Query design should cover various parameter difference patterns to improve identification of the hidden loss calculation function. Try to find the pattern with as few queries as possible.
"""

    contextualized_rule_zh_5 = """\
欢迎使用“司法判例适用冲突分析引擎”。
系统录入了有限的核心司法判例集合 V = {{A, B, C, D, E, F, G, H}}，每个判例都有一个公开的三位案例特征向量（代表涉案金额级别、情节严重度、社会影响指数）：
- 判例 A: {code_A}
- 判例 B: {code_B}
- 判例 C: {code_C}
- 判例 D: {code_D}
- 判例 E: {code_E}
- 判例 F: {code_F}
- 判例 G: {code_G}
- 判例 H: {code_H}

在法理推演网络中，任意两个不同判例之间都存在潜在的适用交叉。这两个判例之间的适用冲突指数/逻辑关联度由一个隐藏的确定性对称冲突评估法则 f 计算得出：冲突指数 w(X,Y) = f(code(X), code(Y)).

该冲突评估法则 f 具有以下性质：
1. 对称性：f(x,y) = f(y,x)
2. 输出为非负整数
3. 评估法则在整个分析过程中保持不变，仅依赖于两端点判例的三位案例特征向量

你的目标是通过有限次的冲突指数查询，推断出隐藏冲突评估法则 f 的规律，并在挑战阶段准确预测5对未查询过判例的适用冲突指数。

## 可用操作

1. **冲突查询**：查询任意两个不同判例之间的适用冲突指数
2. **余量查询**：查询剩余可用的查询次数
3. **发起挑战**：随时可以发起，系统会给出5对未被查询过的判例对，你需要预测它们的冲突指数
4. **最终预测提交**：对挑战阶段给出的5对判例，提交你预测的适用冲突指数值

## 操作格式（必须严格遵守）

**冲突查询**（查询判例 X 和 Y 之间的冲突指数，X 和 Y 必须不同且都在 {{A,B,C,D,E,F,G,H}} 中）：
<query_edge>X,Y</query_edge>

**余量查询**（查询剩余查询次数）：
<query_remaining></query_remaining>

**发起挑战**（请求系统给出5对待预测的判例对）：
<request_challenge></request_challenge>

**最终预测提交**（对挑战给出的5对判例预测冲突指数，格式为"判例1 判例2 = 指数值"，用分号分隔）：
<answer>X1 Y1 = v1; X2 Y2 = v2; X3 Y3 = v3; X4 Y4 = v4; X5 Y5 = v5</answer>

## 资源限制

- 冲突查询总次数上限：{max_queries} 次
- 必须在用尽查询次数前发起挑战

## 成功与失败条件

**成功**：在挑战阶段对5对目标判例适用冲突指数全部预测正确（5/5）

**失败**（任一条件成立即失败）：
1. 用尽所有冲突查询次数仍未发起挑战
2. 挑战后的5条预测未全部命中
3. 在挑战阶段尝试继续进行冲突查询
4. 查询格式错误或查询无效判例

## 游戏流程示例

1. 你可以先进行若干次冲突查询，例如：<query_edge>A,B</query_edge>
2. 系统返回冲突指数，例如："边 A-B 的权值为 5"
3. 你可以随时查询余量：<query_remaining></query_remaining>
4. 当你认为已经掌握规律时，发起挑战：<request_challenge></request_challenge>
5. 系统给出5对判例，例如："(B,E), (C,H), (A,G), (D,F), (E,G)"
6. 你提交预测：<answer>B E = 10; C H = 7; A G = 3; D F = 8; E G = 12</answer>
7. 系统判定是否全部正确

注意：查询设计应覆盖多种特征向量差异模式，以提高对隐藏冲突评估法则的辨识度。尽可能用最少的查询次数找出规律。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Judicial Precedent Application Conflict Analysis Engine".

The system has logged a finite set of core judicial precedents V = {{A, B, C, D, E, F, G, H}}, where each precedent has a public three-digit case feature vector (representing the level of involved amount, severity of circumstances, and social impact index):
- Precedent A: {code_A}
- Precedent B: {code_B}
- Precedent C: {code_C}
- Precedent D: {code_D}
- Precedent E: {code_E}
- Precedent F: {code_F}
- Precedent G: {code_G}
- Precedent H: {code_H}

In the jurisprudential deduction network, there is potential application overlap between any two different precedents. The application conflict index / logical relevance between these two precedents is calculated by a hidden deterministic symmetric conflict assessment rule f: conflict index w(X,Y) = f(code(X), code(Y)).

The conflict assessment rule f has the following properties:
1. Symmetry: f(x,y) = f(y,x)
2. Outputs non-negative integers
3. The assessment rule remains constant throughout the analysis process and depends only on the three-digit case feature vectors of the two end precedents

Your goal is to infer the pattern of the hidden conflict assessment rule f through limited conflict queries, and accurately predict the application conflict indices of 5 unqueried precedent pairs in the challenge phase.

## Available Operations

1. **Conflict Query**: Query the application conflict index between any two different precedents
2. **Remaining Query**: Check the number of remaining conflict queries
3. **Request Challenge**: Can be initiated at any time; the system will provide 5 pairs of unqueried precedents for prediction
4. **Final Prediction Submission**: Submit your predicted application conflict indices for the 5 pairs given in the challenge phase

## Operation Format (must be strictly followed)

**Conflict Query** (query conflict index between precedents X and Y, where X and Y must be different and both in {{A,B,C,D,E,F,G,H}}):
<query_edge>X,Y</query_edge>

**Remaining Query** (check remaining query count):
<query_remaining></query_remaining>

**Request Challenge** (request system to provide 5 pairs of precedents to predict):
<request_challenge></request_challenge>

**Final Prediction Submission** (predict conflict indices for the 5 pairs given in challenge, format "precedent1 precedent2 = index", separated by semicolons):
<answer>X1 Y1 = v1; X2 Y2 = v2; X3 Y3 = v3; X4 Y4 = v4; X5 Y5 = v5</answer>

## Resource Limits

- Maximum conflict queries: {max_queries}
- Must request challenge before exhausting all queries

## Success and Failure Conditions

**Success**: All 5 predictions in the challenge phase are correct (5/5)

**Failure** (game fails if any condition is met):
1. All conflict queries exhausted without requesting challenge
2. Not all 5 predictions in challenge phase are correct
3. Attempting to continue conflict queries during challenge phase
4. Query format error or querying invalid precedents

## Example Game Flow

1. You can start with several conflict queries, e.g.: <query_edge>A,B</query_edge>
2. System returns conflict index, e.g.: "Edge A-B has weight 5"
3. You can check remaining queries anytime: <query_remaining></query_remaining>
4. When you think you've found the pattern, request challenge: <request_challenge></request_challenge>
5. System provides 5 pairs, e.g.: "(B,E), (C,H), (A,G), (D,F), (E,G)"
6. You submit predictions: <answer>B E = 10; C H = 7; A G = 3; D F = 8; E G = 12</answer>
7. System determines if all predictions are correct

Note: Query design should cover various feature vector difference patterns to improve identification of the hidden conflict assessment rule. Try to find the pattern with as few queries as possible.
"""

    tags = ["answer", "query_edge", "query_remaining", "request_challenge"]
    
    reasoning_type = "归纳推理"
    data_structure = "图"
    enable_counterfactual = False   # 设为 True 时开启反事实干预模式

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "codes": {"A": "307", "B": "842", "C": "519", "D": "773", 
                         "E": "066", "F": "190", "G": "421", "H": "258"},
                "function": "sum_digit_diff",
                "max_queries": 12,
            },
            2: {
                "codes": {"A": "123", "B": "456", "C": "789", "D": "234",
                         "E": "567", "F": "890", "G": "345", "H": "678"},
                "function": "number_diff",
                "max_queries": 10,
            },
            3: {
                "codes": {"A": "111", "B": "999", "C": "246", "D": "135",
                         "E": "579", "F": "802", "G": "963", "H": "420"},
                "function": "sum_of_digits_diff",
                "max_queries": 8,
            },
            4: {
                "codes": {"A": "203", "B": "715", "C": "928", "D": "401",
                         "E": "536", "F": "649", "G": "872", "H": "184"},
                "function": "sum_square_diff",
                "max_queries": 7,
            },
            5: {
                "codes": {"A": "321", "B": "654", "C": "987", "D": "432",
                         "E": "765", "F": "198", "G": "543", "H": "876"},
                "function": "sum_product",
                "max_queries": 6,
            },
        },
        "en": {
            1: {
                "codes": {"A": "307", "B": "842", "C": "519", "D": "773",
                         "E": "066", "F": "190", "G": "421", "H": "258"},
                "function": "sum_digit_diff",
                "max_queries": 12,
            },
            2: {
                "codes": {"A": "123", "B": "456", "C": "789", "D": "234",
                         "E": "567", "F": "890", "G": "345", "H": "678"},
                "function": "number_diff",
                "max_queries": 10,
            },
            3: {
                "codes": {"A": "111", "B": "999", "C": "246", "D": "135",
                         "E": "579", "F": "802", "G": "963", "H": "420"},
                "function": "sum_of_digits_diff",
                "max_queries": 8,
            },
            4: {
                "codes": {"A": "203", "B": "715", "C": "928", "D": "401",
                         "E": "536", "F": "649", "G": "872", "H": "184"},
                "function": "sum_square_diff",
                "max_queries": 7,
            },
            5: {
                "codes": {"A": "321", "B": "654", "C": "987", "D": "432",
                         "E": "765", "F": "198", "G": "543", "H": "876"},
                "function": "sum_product",
                "max_queries": 6,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：设置节点编码、隐藏函数、查询上限等"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 设置节点编码
        self.codes = cfg["codes"]
        for node, code in self.codes.items():
            self._game_info[f"code_{node}"] = code
        
        # 设置隐藏函数类型和查询上限
        self.function_type = cfg["function"]
        self.max_queries = cfg["max_queries"]
        self._game_info["max_queries"] = self.max_queries
        
        # 初始化游戏状态
        self.queries_used = 0
        self.queried_edges = set()  # 记录已查询的边
        self.challenge_mode = False  # 是否进入挑战模式
        self.challenge_pairs = []  # 挑战阶段的5对节点

        # 反事实干扰初始化
        self._cf_round_counter = 0          # produce_response 调用轮次计数
        self._cf_correct_resp  = None       # 第 2 轮的正确答案（暂存）
        self._cf_wrong_resp    = None       # 第 2 轮注入的错误答案（暂存）

    def _compute_edge_weight(self, node1, node2):
        """根据隐藏函数计算两个节点之间的边权"""
        code1 = self.codes[node1]
        code2 = self.codes[node2]
        
        if self.function_type == "sum_digit_diff":
            # |d1_x - d1_y| + |d2_x - d2_y| + |d3_x - d3_y|
            return sum(abs(int(code1[i]) - int(code2[i])) for i in range(3))
        
        elif self.function_type == "number_diff":
            # |整数值(x) - 整数值(y)|
            return abs(int(code1) - int(code2))
        
        elif self.function_type == "sum_of_digits_diff":
            # |sum(digits_x) - sum(digits_y)|
            sum1 = sum(int(d) for d in code1)
            sum2 = sum(int(d) for d in code2)
            return abs(sum1 - sum2)
        
        elif self.function_type == "sum_square_diff":
            # (d1_x - d1_y)^2 + (d2_x - d2_y)^2 + (d3_x - d3_y)^2
            return sum((int(code1[i]) - int(code2[i])) ** 2 for i in range(3))
        
        elif self.function_type == "sum_product":
            # d1_x*d1_y + d2_x*d2_y + d3_x*d3_y
            return sum(int(code1[i]) * int(code2[i]) for i in range(3))
        
        else:
            raise ValueError(f"Unknown function type: {self.function_type}")

    def _normalize_edge(self, node1, node2):
        """将边标准化为排序后的元组，确保边的唯一性"""
        return tuple(sorted([node1, node2]))

    def _generate_challenge_pairs(self):
        """生成5对未被查询过的节点对作为挑战"""
        import random
        rng = random.Random(42 + self.config.difficulty)
        
        nodes = list(self.codes.keys())
        all_pairs = []
        
        # 生成所有可能的边
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                edge = self._normalize_edge(nodes[i], nodes[j])
                if edge not in self.queried_edges:
                    all_pairs.append(edge)
        
        # 如果未查询的边少于5条，游戏失败
        if len(all_pairs) < 5:
            return None
        
        # 随机选择5对
        selected = rng.sample(all_pairs, 5)
        return selected

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        if not self.challenge_mode:
            return False
        
        raw_ans = parsed_info.get("answer", "")
        
        # 解析答案格式：X1 Y1 = v1; X2 Y2 = v2; ...
        predictions = {}
        try:
            pairs = [p.strip() for p in raw_ans.split(";") if p.strip()]
            if len(pairs) != 5:
                return False
            
            for pair in pairs:
                if "=" not in pair:
                    return False
                left, right = pair.split("=", 1)
                nodes_part = left.strip().split()
                if len(nodes_part) != 2:
                    return False
                node1, node2 = nodes_part[0].strip().upper(), nodes_part[1].strip().upper()
                weight = int(right.strip())
                
                edge = self._normalize_edge(node1, node2)
                predictions[edge] = weight
        except:
            return False
        
        # 检查是否所有挑战边都被预测
        challenge_edges = set(self.challenge_pairs)
        if set(predictions.keys()) != challenge_edges:
            return False
        
        # 检查每个预测是否正确
        for edge, predicted_weight in predictions.items():
            actual_weight = self._compute_edge_weight(edge[0], edge[1])
            if predicted_weight != actual_weight:
                return False
        
        return True

    def _cf_make_wrong(self, correct: str) -> str:
        """
        将正确的回复篡改为错误回复，用于反事实干预模式。
        策略：如果回复中包含数字（边权），将其替换为错误值（+1）。
        """
        import re as _re
        # 尝试找到回复中的权值数字并修改
        match = _re.search(r'(\d+)', correct)
        if match:
            original_val = int(match.group(1))
            wrong_val = original_val + 1
            return correct.replace(match.group(1), str(wrong_val), 1)
        else:
            # 如果无法找到数字，直接在末尾加标记
            return correct + " [MODIFIED]"

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑 - 不再直接修改 game state"""
        lang = self.config.language
        
        if "query_edge" in parsed_info:
            if self.challenge_mode:
                raise ValueError("Edge queries not allowed during challenge phase." if lang == "en" else "挑战阶段不允许继续查询边权。")
            
            if self.queries_used >= self.max_queries:
                raise ValueError("Query limit exhausted without requesting challenge." if lang == "en" else "查询次数已用尽，游戏失败。")
            
            raw = parsed_info["query_edge"]
            parts = [p.strip() for p in raw.split(",")]
            if len(parts) != 2:
                raise ValueError("Invalid query format." if lang == "en" else "查询格式无效。")
            
            node1, node2 = parts[0].upper(), parts[1].upper()
            
            if node1 not in self.codes or node2 not in self.codes:
                raise ValueError("Invalid node." if lang == "en" else "节点不存在。")
            
            if node1 == node2:
                raise ValueError("Cannot query edge between same nodes." if lang == "en" else "不能查询相同节点之间的边。")
            
            edge = self._normalize_edge(node1, node2)
            self.queried_edges.add(edge)
            self.queries_used += 1
            
            weight = self._compute_edge_weight(node1, node2)
            
            if lang == "zh":
                resp = f"边 {node1}-{node2} 的权值为 {weight}。"
            else:
                resp = f"Edge {node1}-{node2} has weight {weight}."
            
            # 如果查询次数用尽且未挑战，在返回结果后追加警告
            if self.queries_used >= self.max_queries and not self.challenge_mode:
                warning = "（警告：查询次数已全部用尽，请立即发起挑战！）" if lang == "zh" else " (Warning: All queries exhausted. Please request challenge immediately!)"
                resp += warning
            
            return resp
        
        elif "query_remaining" in parsed_info:
            remaining = self.max_queries - self.queries_used
            if lang == "zh":
                return f"剩余查询次数：{remaining}"
            else:
                return f"Remaining queries: {remaining}"
        
        elif "request_challenge" in parsed_info:
            if self.challenge_mode:
                raise ValueError("Already in challenge mode." if lang == "en" else "已经在挑战模式中。")
            
            challenge_pairs = self._generate_challenge_pairs()
            if challenge_pairs is None:
                raise ValueError("Insufficient unqueried edges for challenge." if lang == "en" else "未查询的边数量不足，无法生成挑战。")
            
            self.challenge_mode = True
            self.challenge_pairs = challenge_pairs
            
            pairs_str = ", ".join([f"({p[0]},{p[1]})" for p in challenge_pairs])
            if lang == "zh":
                return f"挑战开始！请预测以下5对节点之间的边权：{pairs_str}"
            else:
                return f"Challenge initiated! Please predict edge weights for: {pairs_str}"
        
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        
        返回:
            list[dict]: 包含 'query' (查询内容) 和 'answer' (正确回复) 的字典列表
        """
        queries = []
        lang = self.config.language
        nodes = list(self.codes.keys())
        
        # 按照字母顺序排序节点，保证确定性
        nodes.sort()
        
        # 遍历所有可能的节点对 (C(8,2) = 28 种组合)
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                node1 = nodes[i]
                node2 = nodes[j]
                
                # query 必须是合法的 XML 标签字符串
                query_payload = f"<query_edge>{node1},{node2}</query_edge>"
                
                # 直接调用内部计算逻辑，计算正确边权，不依赖/修改游戏状态
                weight = self._compute_edge_weight(node1, node2)
                
                # 构造标准回复字符串，格式需与 produce_response 保持一致
                if lang == "zh":
                    answer = f"边 {node1}-{node2} 的权值为 {weight}。"
                else:
                    answer = f"Edge {node1}-{node2} has weight {weight}."
                
                queries.append({
                    "query": query_payload,
                    "answer": answer
                })
                
        return queries