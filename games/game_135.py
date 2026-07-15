from .base import Game
import re

class TreeMappingInferenceGame(Game):

    game_rule_zh = """\
我们来玩一个"树映射推理"游戏，规则如下：

游戏设定了一棵有根树，最大深度为3（根深度为0），共19个节点。节点标识及父子关系如下：
- 深度0：r
- 深度1：r 的子节点为 a1, a2, a3
- 深度2：
  - a1 的子节点：b11, b12
  - a2 的子节点：b21
  - a3 的子节点：b31, b32, b33
- 深度3（叶）：
  - b11 的子节点：c111, c112
  - b12 的子节点：c121
  - b21 的子节点：c211, c212
  - b31 的子节点：c311
  - b32 的子节点：c321, c322
  - b33 的子节点：c331

存在一个特殊的目标节点T（你需要推断出它）。

游戏已秘密选择了一个二值映射方案 g(d)，作用于节点深度 d，四种候选方案如下（确切采用其一）：
- 方案A（奇偶）：g(d) = d 对 2 取模的结果
- 方案B（中层）：g(d) = 1 当且仅当 d 属于集合 1或2，否则为 0
- 方案C（下层）：g(d) = 1 当且仅当 d 属于集合 2或3，否则为 0
- 方案D（全零）：g(d) = 0 对所有 d

你的目标是：
1. 确定真实采用的映射方案（A/B/C/D）
2. 确定目标节点 T 的深度（0/1/2/3）

你可以反复向我提出以下四类查询（每次仅限一个查询），我会根据真实设定如实回答：

1. 采样输出：询问某个节点在映射方案下的输出值。回答"输出=0"或"输出=1"，等于 g(该节点的深度)。
2. 查询子节点：询问某个节点的所有子节点列表。回答"子节点=[...]"。注意：若查询对象为目标节点T，会返回"拒绝：目标结构不可查"。
3. 是否叶子：询问某个节点是否为叶子节点。回答"是"或"否"（允许对T进行此查询）。
4. 是否同层：询问两个节点是否在相同深度。回答"是"或"否"。注意：若任一参数为目标节点T，会返回"拒绝：目标不得参与此比较"。

当你收集足够信息后，请提交最终答案。答案需包含：
1. 采用的映射方案（A/B/C/D）
2. 至少两次针对非目标节点的采样记录（节点与对应输出），并基于各深度输出特征排除其余方案的逻辑推理
3. 目标节点T的深度（0/1/2/3），并基于已确定方案与对T的允许查询进行论证

若答案错误、格式不符或推理依据不足，游戏失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 采样输出（例如查询节点 r）：
<query_sample>r</query_sample>

- 查询子节点（例如查询节点 a1）：
<query_children>a1</query_children>

- 是否叶子（例如查询节点 c111）：
<query_leaf>c111</query_leaf>

- 是否同层（例如比较节点 a1 和 a2）：
<query_same_depth>a1,a2</query_same_depth>

提交最终答案时，必须说明映射方案、采样证据、目标节点T的深度及推理过程，格式如下：

<answer>
方案=A
证据1=节点:r,输出:0
证据2=节点:a1,输出:1
排除逻辑=深度0输出0排除了无效方案，深度1输出1结合深度特征可确定方案A
目标深度=3
目标推理=通过采样T得到输出1，结合方案A中深度3对应输出1，且T为叶子节点，确定T深度为3
</answer>
"""

    game_rule_en = """\
Let's play a "Tree Mapping Inference" game. Here are the rules:

The game features a rooted tree with a maximum depth of 3 (root has depth 0) and 19 nodes total. Node identifiers and parent-child relationships are as follows:
- Depth 0: r
- Depth 1: r has children a1, a2, a3
- Depth 2:
  - a1 has children: b11, b12
  - a2 has child: b21
  - a3 has children: b31, b32, b33
- Depth 3 (leaves):
  - b11 has children: c111, c112
  - b12 has child: c121
  - b21 has children: c211, c212
  - b31 has child: c311
  - b32 has children: c321, c322
  - b33 has child: c331

There exists a special target node T (which you need to infer).

The game has secretly selected a binary mapping scheme g(d) that acts on node depth d. There are four candidate schemes (exactly one is used):
- Scheme A (Parity): g(d) = d modulo 2
- Scheme B (Middle): g(d) = 1 if and only if d is in the set 1 or 2, otherwise 0
- Scheme C (Lower): g(d) = 1 if and only if d is in the set 2 or 3, otherwise 0
- Scheme D (All Zero): g(d) = 0 for all d

Your goals are:
1. Determine the actual mapping scheme used (A/B/C/D)
2. Determine the depth of target node T (0/1/2/3)

You can repeatedly ask me four types of queries (one per turn), and I will answer truthfully based on the actual setup:

1. Sample Output: Ask for the output value of a node under the mapping scheme. Answer "Output=0" or "Output=1", equal to g(depth of that node).
2. Query Children: Ask for the list of all child nodes of a node. Answer "Children=[...]". Note: If the query target is T, returns "Rejected: Target structure not queryable".
3. Is Leaf: Ask if a node is a leaf node. Answer "Yes" or "No" (this query is allowed for T).
4. Same Depth: Ask if two nodes are at the same depth. Answer "Yes" or "No". Note: If either parameter is target node T, returns "Rejected: Target cannot participate in this comparison".

When you have collected enough information, submit your final answer. The answer must include:
1. The mapping scheme used (A/B/C/D)
2. At least two sampling records for non-target nodes (node and corresponding output), with logical reasoning to exclude other schemes based on depth-output characteristics
3. The depth of target node T (0/1/2/3), with justification based on the determined scheme and allowed queries for T

If the answer is incorrect, format is invalid, or reasoning is insufficient, the game fails.

Each query must contain only one tag. Use the following XML format:

- Sample Output (e.g., querying node r):
<query_sample>r</query_sample>

- Query Children (e.g., querying node a1):
<query_children>a1</query_children>

- Is Leaf (e.g., querying node c111):
<query_leaf>c111</query_leaf>

- Same Depth (e.g., comparing nodes a1 and a2):
<query_same_depth>a1,a2</query_same_depth>

When submitting the final answer, you must specify the mapping scheme, sampling evidence, target node T's depth, and reasoning process, using this format:

<answer>
Scheme=A
Evidence1=Node:r,Output:0
Evidence2=Node:a1,Output:1
Exclusion_Logic=Depth 0 output 0 excludes invalid schemes, depth 1 output 1 combined with depth characteristics confirms Scheme A
Target_Depth=3
Target_Reasoning=Sampling T yields output 1, combined with Scheme A where depth 3 corresponds to output 1, and T is a leaf node, confirming T depth is 3
</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎进入“智能交通路网排查系统”。这是一场基于路网拓扑的溯因推理排查游戏，规则如下：

系统设定了一棵区域路网层级树，最大深度为3（根枢纽深度为0），共19个路网节点。节点标识及层级（父子）关系如下：
- 深度0（核心枢纽）：r
- 深度1（主干道）：r 的下级节点为 a1, a2, a3
- 深度2（次干道）：
  - a1 的下级节点：b11, b12
  - a2 的下级节点：b21
  - a3 的下级节点：b31, b32, b33
- 深度3（支路/叶子节点）：
  - b11 的下级节点：c111, c112
  - b12 的下级节点：c121
  - b21 的下级节点：c211, c212
  - b31 的下级节点：c311
  - b32 的下级节点：c321, c322
  - b33 的下级节点：c331

存在一个发生未知拥堵的特殊目标节点 T（你需要推断出它的深度层级）。

交管局已秘密实施了一套针对路段深度 d 的二值限行方案 g(d)，四种预案如下（确切采用其一）：
- 方案A（奇偶限行）：g(d) = d 对 2 取模的结果
- 方案B（中层限行）：g(d) = 1 当且仅当 d 属于集合 1或2，否则为 0
- 方案C（基层限行）：g(d) = 1 当且仅当 d 属于集合 2或3，否则为 0
- 方案D（全网放行）：g(d) = 0 对所有 d

你的目标是：
1. 确定真实采用的限行方案（A/B/C/D）
2. 确定拥堵目标节点 T 的深度（0/1/2/3）

你可以反复向我提出以下四类查询（每次仅限一个查询），我会根据系统真实设定如实回答：

1. 采样输出：询问某个节点在当前方案下的输出值（即限行状态）。回答"输出=0"（未限行）或"输出=1"（限行），等于 g(该节点的深度)。
2. 查询子节点：询问某个节点的所有下级子节点列表。回答"子节点=[...]"。注意：若查询对象为目标节点T，会返回"拒绝：目标结构不可查"。
3. 是否叶子：询问某个节点是否为最底层的支路（叶子节点）。回答"是"或"否"（允许对T进行此查询）。
4. 是否同层：询问两个节点是否在相同深度层级。回答"是"或"否"。注意：若任一参数为目标节点T，会返回"拒绝：目标不得参与此比较"。

当你收集足够信息后，请提交最终排查报告。答案需包含：
1. 采用的方案（A/B/C/D）
2. 至少两次针对非目标节点的采样记录（节点与对应输出），并基于各深度输出特征排除其余方案的逻辑推理
3. 目标节点 T 的深度（0/1/2/3），并基于已确定方案与对T的允许查询进行论证

若答案错误、格式不符或推理依据不足，排查失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 采样输出（例如查询节点 r）：
<query_sample>r</query_sample>

- 查询子节点（例如查询节点 a1）：
<query_children>a1</query_children>

- 是否叶子（例如查询节点 c111）：
<query_leaf>c111</query_leaf>

- 是否同层（例如比较节点 a1 和 a2）：
<query_same_depth>a1,a2</query_same_depth>

提交最终答案时，必须说明映射方案、采样证据、目标节点T的深度及推理过程，格式如下：

<answer>
方案=A
证据1=节点:r,输出:0
证据2=节点:a1,输出:1
排除逻辑=深度0输出0排除了无效方案，深度1输出1结合深度特征可确定方案A
目标深度=3
目标推理=通过采样T得到输出1，结合方案A中深度3对应输出1，且T为叶子节点，确定T深度为3
</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Intelligent Traffic Network Inspection System". Let's play a topological mapping inference game. Here are the rules:

The system features a regional road network modeled as a rooted tree with a maximum depth of 3 (root hub has depth 0) and 19 nodes total. Node identifiers and hierarchical (parent-child) relationships are as follows:
- Depth 0 (Core Hub): r
- Depth 1 (Arterial Roads): r has children a1, a2, a3
- Depth 2 (Collector Roads):
  - a1 has children: b11, b12
  - a2 has child: b21
  - a3 has children: b31, b32, b33
- Depth 3 (Local Roads/Leaves):
  - b11 has children: c111, c112
  - b12 has child: c121
  - b21 has children: c211, c212
  - b31 has child: c311
  - b32 has children: c321, c322
  - b33 has child: c331

There exists a special congested target node T (whose depth you need to infer).

The traffic authority has secretly implemented a binary traffic control scheme g(d) based on the road depth d. There are four candidate schemes (exactly one is used):
- Scheme A (Parity Restriction): g(d) = d modulo 2
- Scheme B (Mid-Level Restriction): g(d) = 1 if and only if d is in the set 1 or 2, otherwise 0
- Scheme C (Local Restriction): g(d) = 1 if and only if d is in the set 2 or 3, otherwise 0
- Scheme D (No Restriction): g(d) = 0 for all d

Your goals are:
1. Determine the actual control scheme used (A/B/C/D)
2. Determine the depth of target node T (0/1/2/3)

You can repeatedly ask me four types of queries (one per turn), and I will answer truthfully based on the system setup:

1. Sample Output: Ask for the restriction output value of a node. Answer "Output=0" or "Output=1", equal to g(depth of that node).
2. Query Children: Ask for the list of all subordinate child nodes. Answer "Children=[...]". Note: If the query target is T, returns "Rejected: Target structure not queryable".
3. Is Leaf: Ask if a node is a terminal local road (leaf node). Answer "Yes" or "No" (this query is allowed for T).
4. Same Depth: Ask if two nodes are at the same depth. Answer "Yes" or "No". Note: If either parameter is target node T, returns "Rejected: Target cannot participate in this comparison".

When you have collected enough information, submit your final report. The answer must include:
1. The scheme used (A/B/C/D)
2. At least two sampling records for non-target nodes (node and corresponding output), with logical reasoning to exclude other schemes based on depth-output characteristics
3. The depth of target node T (0/1/2/3), with justification based on the determined scheme and allowed queries for T

If the answer is incorrect, format is invalid, or reasoning is insufficient, the inspection fails.

Each query must contain only one tag. Use the following XML format:

- Sample Output (e.g., querying node r):
<query_sample>r</query_sample>

- Query Children (e.g., querying node a1):
<query_children>a1</query_children>

- Is Leaf (e.g., querying node c111):
<query_leaf>c111</query_leaf>

- Same Depth (e.g., comparing nodes a1 and a2):
<query_same_depth>a1,a2</query_same_depth>

When submitting the final answer, you must specify the scheme, sampling evidence, target node T's depth, and reasoning process, using this format:

<answer>
Scheme=A
Evidence1=Node:r,Output:0
Evidence2=Node:a1,Output:1
Exclusion_Logic=Depth 0 output 0 excludes invalid schemes, depth 1 output 1 combined with depth characteristics confirms Scheme A
Target_Depth=3
Target_Reasoning=Sampling T yields output 1, combined with Scheme A where depth 3 corresponds to output 1, and T is a leaf node, confirming T depth is 3
</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用“病原体溯源与基因表达检测系统”。这是一场基于分类进化树的溯因推理排查游戏，规则如下：

系统设定了一棵病原体分类演化树，最大演化深度为3（根系病原体深度为0），共19个分类节点。节点标识及进化（父子）关系如下：
- 深度0（根系病原体）：r
- 深度1（亚型分支）：r 的下级节点为 a1, a2, a3
- 深度2（变异株系）：
  - a1 的下级节点：b11, b12
  - a2 的下级节点：b21
  - a3 的下级节点：b31, b32, b33
- 深度3（终端序列/叶子节点）：
  - b11 的下级节点：c111, c112
  - b12 的下级节点：c121
  - b21 的下级节点：c211, c212
  - b31 的下级节点：c311
  - b32 的下级节点：c321, c322
  - b33 的下级节点：c331

存在一个发生未知突变的特殊目标节点 T（你需要推断出它的深度层级）。

疾控中心已秘密确认了一套针对演化深度 d 的二值基因标记表达方案 g(d)，四种预案如下（确切采用其一）：
- 方案A（奇偶表达）：g(d) = d 对 2 取模的结果
- 方案B（中层表达）：g(d) = 1 当且仅当 d 属于集合 1或2，否则为 0
- 方案C（终端表达）：g(d) = 1 当且仅当 d 属于集合 2或3，否则为 0
- 方案D（全阴性）：g(d) = 0 对所有 d

你的目标是：
1. 确定真实采用的表达方案（A/B/C/D）
2. 确定突变目标节点 T 的深度（0/1/2/3）

你可以反复向我提出以下四类查询（每次仅限一个查询），我会根据系统真实设定如实回答：

1. 采样输出：询问某个节点在当前方案下的输出值（基因表达状态）。回答"输出=0"（阴性）或"输出=1"（阳性），等于 g(该节点的深度)。
2. 查询子节点：询问某个节点的所有演化下级节点列表。回答"子节点=[...]"。注意：若查询对象为目标节点T，会返回"拒绝：目标结构不可查"。
3. 是否叶子：询问某个节点是否为最底层的终端序列（叶子节点）。回答"是"或"否"（允许对T进行此查询）。
4. 是否同层：询问两个节点是否在相同演化深度。回答"是"或"否"。注意：若任一参数为目标节点T，会返回"拒绝：目标不得参与此比较"。

当你收集足够信息后，请提交最终排查报告。答案需包含：
1. 采用的方案（A/B/C/D）
2. 至少两次针对非目标节点的采样记录（节点与对应输出），并基于各深度输出特征排除其余方案的逻辑推理
3. 目标节点 T 的深度（0/1/2/3），并基于已确定方案与对T的允许查询进行论证

若答案错误、格式不符或推理依据不足，排查失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 采样输出（例如查询节点 r）：
<query_sample>r</query_sample>

- 查询子节点（例如查询节点 a1）：
<query_children>a1</query_children>

- 是否叶子（例如查询节点 c111）：
<query_leaf>c111</query_leaf>

- 是否同层（例如比较节点 a1 和 a2）：
<query_same_depth>a1,a2</query_same_depth>

提交最终答案时，必须说明映射方案、采样证据、目标节点T的深度及推理过程，格式如下：

<answer>
方案=A
证据1=节点:r,输出:0
证据2=节点:a1,输出:1
排除逻辑=深度0输出0排除了无效方案，深度1输出1结合深度特征可确定方案A
目标深度=3
目标推理=通过采样T得到输出1，结合方案A中深度3对应输出1，且T为叶子节点，确定T深度为3
</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Pathogen Traceability and Gene Expression Detection System". Let's play a taxonomic mapping inference game. Here are the rules:

The system features a pathogen taxonomy tree with a maximum depth of 3 (root pathogen has depth 0) and 19 nodes total. Node identifiers and evolutionary (parent-child) relationships are as follows:
- Depth 0 (Root Pathogen): r
- Depth 1 (Sub-type Branch): r has children a1, a2, a3
- Depth 2 (Variant Strain):
  - a1 has children: b11, b12
  - a2 has child: b21
  - a3 has children: b31, b32, b33
- Depth 3 (Terminal Sequence/Leaves):
  - b11 has children: c111, c112
  - b12 has child: c121
  - b21 has children: c211, c212
  - b31 has child: c311
  - b32 has children: c321, c322
  - b33 has child: c331

There exists a special mutated target node T (whose depth you need to infer).

The CDC has secretly confirmed a binary gene marker expression scheme g(d) based on the evolutionary depth d. There are four candidate schemes (exactly one is used):
- Scheme A (Parity Expression): g(d) = d modulo 2
- Scheme B (Mid-Level Expression): g(d) = 1 if and only if d is in the set 1 or 2, otherwise 0
- Scheme C (Terminal Expression): g(d) = 1 if and only if d is in the set 2 or 3, otherwise 0
- Scheme D (All Negative): g(d) = 0 for all d

Your goals are:
1. Determine the actual expression scheme used (A/B/C/D)
2. Determine the depth of target node T (0/1/2/3)

You can repeatedly ask me four types of queries (one per turn), and I will answer truthfully based on the system setup:

1. Sample Output: Ask for the expression output value of a node. Answer "Output=0" (Negative) or "Output=1" (Positive), equal to g(depth of that node).
2. Query Children: Ask for the list of all evolutionary child nodes. Answer "Children=[...]". Note: If the query target is T, returns "Rejected: Target structure not queryable".
3. Is Leaf: Ask if a node is a terminal sequence (leaf node). Answer "Yes" or "No" (this query is allowed for T).
4. Same Depth: Ask if two nodes are at the same evolutionary depth. Answer "Yes" or "No". Note: If either parameter is target node T, returns "Rejected: Target cannot participate in this comparison".

When you have collected enough information, submit your final report. The answer must include:
1. The scheme used (A/B/C/D)
2. At least two sampling records for non-target nodes (node and corresponding output), with logical reasoning to exclude other schemes based on depth-output characteristics
3. The depth of target node T (0/1/2/3), with justification based on the determined scheme and allowed queries for T

If the answer is incorrect, format is invalid, or reasoning is insufficient, the inspection fails.

Each query must contain only one tag. Use the following XML format:

- Sample Output (e.g., querying node r):
<query_sample>r</query_sample>

- Query Children (e.g., querying node a1):
<query_children>a1</query_children>

- Is Leaf (e.g., querying node c111):
<query_leaf>c111</query_leaf>

- Same Depth (e.g., comparing nodes a1 and a2):
<query_same_depth>a1,a2</query_same_depth>

When submitting the final answer, you must specify the scheme, sampling evidence, target node T's depth, and reasoning process, using this format:

<answer>
Scheme=A
Evidence1=Node:r,Output:0
Evidence2=Node:a1,Output:1
Exclusion_Logic=Depth 0 output 0 excludes invalid schemes, depth 1 output 1 combined with depth characteristics confirms Scheme A
Target_Depth=3
Target_Reasoning=Sampling T yields output 1, combined with Scheme A where depth 3 corresponds to output 1, and T is a leaf node, confirming T depth is 3
</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用“知识图谱与课程考核分析系统”。这是一场基于知识点依赖树的溯因推理排查游戏，规则如下：

系统设定了一棵学科知识图谱树，最大深度为3（核心学科深度为0），共19个图谱节点。节点标识及依赖（父子）关系如下：
- 深度0（核心学科）：r
- 深度1（主干模块）：r 的下级节点为 a1, a2, a3
- 深度2（单元节点）：
  - a1 的下级节点：b11, b12
  - a2 的下级节点：b21
  - a3 的下级节点：b31, b32, b33
- 深度3（具体考点/叶子节点）：
  - b11 的下级节点：c111, c112
  - b12 的下级节点：c121
  - b21 的下级节点：c211, c212
  - b31 的下级节点：c311
  - b32 的下级节点：c321, c322
  - b33 的下级节点：c331

存在一个导致学生认知障碍的特殊缺失节点 T（你需要推断出它的深度层级）。

教研组已秘密部署了一套针对知识深度 d 的二值考核覆盖方案 g(d)，四种预案如下（确切采用其一）：
- 方案A（奇偶考核）：g(d) = d 对 2 取模的结果
- 方案B（中层考核）：g(d) = 1 当且仅当 d 属于集合 1或2，否则为 0
- 方案C（细节考核）：g(d) = 1 当且仅当 d 属于集合 2或3，否则为 0
- 方案D（无新增考核）：g(d) = 0 对所有 d

你的目标是：
1. 确定真实采用的考核方案（A/B/C/D）
2. 确定缺失目标节点 T 的深度（0/1/2/3）

你可以反复向我提出以下四类查询（每次仅限一个查询），我会根据系统真实设定如实回答：

1. 采样输出：询问某个节点在当前方案下的输出值（即考核状态）。回答"输出=0"（未考核）或"输出=1"（已考核），等于 g(该节点的深度)。
2. 查询子节点：询问某个节点的所有依赖下级节点列表。回答"子节点=[...]"。注意：若查询对象为目标节点T，会返回"拒绝：目标结构不可查"。
3. 是否叶子：询问某个节点是否为最底层的具体考点（叶子节点）。回答"是"或"否"（允许对T进行此查询）。
4. 是否同层：询问两个节点是否在相同知识层级深度。回答"是"或"否"。注意：若任一参数为目标节点T，会返回"拒绝：目标不得参与此比较"。

当你收集足够信息后，请提交最终排查报告。答案需包含：
1. 采用的方案（A/B/C/D）
2. 至少两次针对非目标节点的采样记录（节点与对应输出），并基于各深度输出特征排除其余方案的逻辑推理
3. 目标节点 T 的深度（0/1/2/3），并基于已确定方案与对T的允许查询进行论证

若答案错误、格式不符或推理依据不足，排查失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 采样输出（例如查询节点 r）：
<query_sample>r</query_sample>

- 查询子节点（例如查询节点 a1）：
<query_children>a1</query_children>

- 是否叶子（例如查询节点 c111）：
<query_leaf>c111</query_leaf>

- 是否同层（例如比较节点 a1 和 a2）：
<query_same_depth>a1,a2</query_same_depth>

提交最终答案时，必须说明映射方案、采样证据、目标节点T的深度及推理过程，格式如下：

<answer>
方案=A
证据1=节点:r,输出:0
证据2=节点:a1,输出:1
排除逻辑=深度0输出0排除了无效方案，深度1输出1结合深度特征可确定方案A
目标深度=3
目标推理=通过采样T得到输出1，结合方案A中深度3对应输出1，且T为叶子节点，确定T深度为3
</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Knowledge Graph and Curriculum Assessment Analysis System". Let's play a concept dependency mapping inference game. Here are the rules:

The system features a subject knowledge graph tree with a maximum depth of 3 (core subject has depth 0) and 19 nodes total. Node identifiers and dependency (parent-child) relationships are as follows:
- Depth 0 (Core Subject): r
- Depth 1 (Main Module): r has children a1, a2, a3
- Depth 2 (Unit Node):
  - a1 has children: b11, b12
  - a2 has child: b21
  - a3 has children: b31, b32, b33
- Depth 3 (Specific Topic/Leaves):
  - b11 has children: c111, c112
  - b12 has child: c121
  - b21 has children: c211, c212
  - b31 has child: c311
  - b32 has children: c321, c322
  - b33 has child: c331

There exists a special missing target node T causing cognitive barriers (whose depth you need to infer).

The teaching research group has secretly deployed a binary assessment coverage scheme g(d) based on the knowledge depth d. There are four candidate schemes (exactly one is used):
- Scheme A (Parity Assessment): g(d) = d modulo 2
- Scheme B (Mid-Level Assessment): g(d) = 1 if and only if d is in the set 1 or 2, otherwise 0
- Scheme C (Detailed Assessment): g(d) = 1 if and only if d is in the set 2 or 3, otherwise 0
- Scheme D (No Assessment): g(d) = 0 for all d

Your goals are:
1. Determine the actual assessment scheme used (A/B/C/D)
2. Determine the depth of target node T (0/1/2/3)

You can repeatedly ask me four types of queries (one per turn), and I will answer truthfully based on the system setup:

1. Sample Output: Ask for the assessment output value of a node. Answer "Output=0" (Not assessed) or "Output=1" (Assessed), equal to g(depth of that node).
2. Query Children: Ask for the list of all subordinate knowledge nodes. Answer "Children=[...]". Note: If the query target is T, returns "Rejected: Target structure not queryable".
3. Is Leaf: Ask if a node is a terminal specific topic (leaf node). Answer "Yes" or "No" (this query is allowed for T).
4. Same Depth: Ask if two nodes are at the same knowledge depth. Answer "Yes" or "No". Note: If either parameter is target node T, returns "Rejected: Target cannot participate in this comparison".

When you have collected enough information, submit your final report. The answer must include:
1. The scheme used (A/B/C/D)
2. At least two sampling records for non-target nodes (node and corresponding output), with logical reasoning to exclude other schemes based on depth-output characteristics
3. The depth of target node T (0/1/2/3), with justification based on the determined scheme and allowed queries for T

If the answer is incorrect, format is invalid, or reasoning is insufficient, the inspection fails.

Each query must contain only one tag. Use the following XML format:

- Sample Output (e.g., querying node r):
<query_sample>r</query_sample>

- Query Children (e.g., querying node a1):
<query_children>a1</query_children>

- Is Leaf (e.g., querying node c111):
<query_leaf>c111</query_leaf>

- Same Depth (e.g., comparing nodes a1 and a2):
<query_same_depth>a1,a2</query_same_depth>

When submitting the final answer, you must specify the scheme, sampling evidence, target node T's depth, and reasoning process, using this format:

<answer>
Scheme=A
Evidence1=Node:r,Output:0
Evidence2=Node:a1,Output:1
Exclusion_Logic=Depth 0 output 0 excludes invalid schemes, depth 1 output 1 combined with depth characteristics confirms Scheme A
Target_Depth=3
Target_Reasoning=Sampling T yields output 1, combined with Scheme A where depth 3 corresponds to output 1, and T is a leaf node, confirming T depth is 3
</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎进入“工业BOM追溯与质检排查系统”。这是一场基于装配拓扑的溯因推理排查游戏，规则如下：

系统设定了一棵产品BOM（物料清单）装配树，最大深度为3（最终产品深度为0），共19个装配节点。节点标识及包含（父子）关系如下：
- 深度0（最终产品）：r
- 深度1（核心组件）：r 的下级节点为 a1, a2, a3
- 深度2（子模块）：
  - a1 的下级节点：b11, b12
  - a2 的下级节点：b21
  - a3 的下级节点：b31, b32, b33
- 深度3（基础零件/叶子节点）：
  - b11 的下级节点：c111, c112
  - b12 的下级节点：c121
  - b21 的下级节点：c211, c212
  - b31 的下级节点：c311
  - b32 的下级节点：c321, c322
  - b33 的下级节点：c331

存在一个具有隐患的特殊缺陷目标节点 T（你需要推断出它在BOM树中的深度层级）。

质检部已秘密实施了一套针对装配深度 d 的二值质检方案 g(d)，四种预案如下（确切采用其一）：
- 方案A（奇偶质检）：g(d) = d 对 2 取模的结果
- 方案B（中层质检）：g(d) = 1 当且仅当 d 属于集合 1或2，否则为 0
- 方案C（底层质检）：g(d) = 1 当且仅当 d 属于集合 2或3，否则为 0
- 方案D（免检放行）：g(d) = 0 对所有 d

你的目标是：
1. 确定真实采用的质检方案（A/B/C/D）
2. 确定缺陷目标节点 T 的深度（0/1/2/3）

你可以反复向我提出以下四类查询（每次仅限一个查询），我会根据系统真实设定如实回答：

1. 采样输出：询问某个节点在当前方案下的输出值（即质检状态）。回答"输出=0"（免检）或"输出=1"（必检），等于 g(该节点的深度)。
2. 查询子节点：询问某个节点的所有下级组成节点列表。回答"子节点=[...]"。注意：若查询对象为目标节点T，会返回"拒绝：目标结构不可查"。
3. 是否叶子：询问某个节点是否为最底层的基础零件（叶子节点）。回答"是"或"否"（允许对T进行此查询）。
4. 是否同层：询问两个节点是否在相同BOM层级。回答"是"或"否"。注意：若任一参数为目标节点T，会返回"拒绝：目标不得参与此比较"。

当你收集足够信息后，请提交最终排查报告。答案需包含：
1. 采用的方案（A/B/C/D）
2. 至少两次针对非目标节点的采样记录（节点与对应输出），并基于各深度输出特征排除其余方案的逻辑推理
3. 目标节点 T 的深度（0/1/2/3），并基于已确定方案与对T的允许查询进行论证

若答案错误、格式不符或推理依据不足，排查失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 采样输出（例如查询节点 r）：
<query_sample>r</query_sample>

- 查询子节点（例如查询节点 a1）：
<query_children>a1</query_children>

- 是否叶子（例如查询节点 c111）：
<query_leaf>c111</query_leaf>

- 是否同层（例如比较节点 a1 和 a2）：
<query_same_depth>a1,a2</query_same_depth>

提交最终答案时，必须说明映射方案、采样证据、目标节点T的深度及推理过程，格式如下：

<answer>
方案=A
证据1=节点:r,输出:0
证据2=节点:a1,输出:1
排除逻辑=深度0输出0排除了无效方案，深度1输出1结合深度特征可确定方案A
目标深度=3
目标推理=通过采样T得到输出1，结合方案A中深度3对应输出1，且T为叶子节点，确定T深度为3
</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Industrial BOM Traceability and Quality Inspection System". Let's play an assembly mapping inference game. Here are the rules:

The system features a product Bill of Materials (BOM) modeled as a rooted tree with a maximum depth of 3 (final product has depth 0) and 19 nodes total. Node identifiers and inclusion (parent-child) relationships are as follows:
- Depth 0 (Final Product): r
- Depth 1 (Core Assembly): r has children a1, a2, a3
- Depth 2 (Sub-module):
  - a1 has children: b11, b12
  - a2 has child: b21
  - a3 has children: b31, b32, b33
- Depth 3 (Base Component/Leaves):
  - b11 has children: c111, c112
  - b12 has child: c121
  - b21 has children: c211, c212
  - b31 has child: c311
  - b32 has children: c321, c322
  - b33 has child: c331

There exists a special defective target node T (whose depth you need to infer).

The Quality Control Department has secretly implemented a binary inspection protocol g(d) based on the assembly depth d. There are four candidate protocols (exactly one is used):
- Scheme A (Parity Inspection): g(d) = d modulo 2
- Scheme B (Mid-Level Inspection): g(d) = 1 if and only if d is in the set 1 or 2, otherwise 0
- Scheme C (Lower-Level Inspection): g(d) = 1 if and only if d is in the set 2 or 3, otherwise 0
- Scheme D (No Inspection): g(d) = 0 for all d

Your goals are:
1. Determine the actual inspection protocol used (A/B/C/D)
2. Determine the depth of target node T (0/1/2/3)

You can repeatedly ask me four types of queries (one per turn), and I will answer truthfully based on the system setup:

1. Sample Output: Ask for the inspection output value of a node. Answer "Output=0" (Skipped) or "Output=1" (Inspected), equal to g(depth of that node).
2. Query Children: Ask for the list of all sub-component nodes. Answer "Children=[...]". Note: If the query target is T, returns "Rejected: Target structure not queryable".
3. Is Leaf: Ask if a node is a terminal base component (leaf node). Answer "Yes" or "No" (this query is allowed for T).
4. Same Depth: Ask if two nodes are at the same BOM depth. Answer "Yes" or "No". Note: If either parameter is target node T, returns "Rejected: Target cannot participate in this comparison".

When you have collected enough information, submit your final report. The answer must include:
1. The scheme used (A/B/C/D)
2. At least two sampling records for non-target nodes (node and corresponding output), with logical reasoning to exclude other schemes based on depth-output characteristics
3. The depth of target node T (0/1/2/3), with justification based on the determined scheme and allowed queries for T

If the answer is incorrect, format is invalid, or reasoning is insufficient, the inspection fails.

Each query must contain only one tag. Use the following XML format:

- Sample Output (e.g., querying node r):
<query_sample>r</query_sample>

- Query Children (e.g., querying node a1):
<query_children>a1</query_children>

- Is Leaf (e.g., querying node c111):
<query_leaf>c111</query_leaf>

- Same Depth (e.g., comparing nodes a1 and a2):
<query_same_depth>a1,a2</query_same_depth>

When submitting the final answer, you must specify the scheme, sampling evidence, target node T's depth, and reasoning process, using this format:

<answer>
Scheme=A
Evidence1=Node:r,Output:0
Evidence2=Node:a1,Output:1
Exclusion_Logic=Depth 0 output 0 excludes invalid schemes, depth 1 output 1 combined with depth characteristics confirms Scheme A
Target_Depth=3
Target_Reasoning=Sampling T yields output 1, combined with Scheme A where depth 3 corresponds to output 1, and T is a leaf node, confirming T depth is 3
</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎进入“法律条文层级与适用性审查系统”。这是一场基于条文层级结构的溯因推理排查游戏，规则如下：

系统设定了一部法律的条文层级树，最大深度为3（基本法/宪法为0），共19个架构节点。节点标识及从属（父子）关系如下：
- 深度0（基本法）：r
- 深度1（编/章）：r 的下级节点为 a1, a2, a3
- 深度2（节）：
  - a1 的下级节点：b11, b12
  - a2 的下级节点：b21
  - a3 的下级节点：b31, b32, b33
- 深度3（条/款/叶子节点）：
  - b11 的下级节点：c111, c112
  - b12 的下级节点：c121
  - b21 的下级节点：c211, c212
  - b31 的下级节点：c311
  - b32 的下级节点：c321, c322
  - b33 的下级节点：c331

存在一个存在司法争议的特殊目标条文节点 T（你需要推断出它在法律框架中的深度层级）。

立法委员会已秘密设定了一套针对条文深度 d 的二值修正案适用规则 g(d)，四种预案如下（确切采用其一）：
- 方案A（奇偶适用）：g(d) = d 对 2 取模的结果
- 方案B（中层适用）：g(d) = 1 当且仅当 d 属于集合 1或2，否则为 0
- 方案C（基层适用）：g(d) = 1 当且仅当 d 属于集合 2或3，否则为 0
- 方案D（不适用）：g(d) = 0 对所有 d

你的目标是：
1. 确定真实采用的修正案适用规则（A/B/C/D）
2. 确定争议目标条文 T 的深度（0/1/2/3）

你可以反复向我提出以下四类查询（每次仅限一个查询），我会根据系统真实设定如实回答：

1. 采样输出：询问某个节点在当前规则下的适用状态。回答"输出=0"（不适用）或"输出=1"（适用），等于 g(该节点的深度)。
2. 查询子节点：询问某个节点的所有下属条文节点列表。回答"子节点=[...]"。注意：若查询对象为目标节点T，会返回"拒绝：目标结构不可查"。
3. 是否叶子：询问某个节点是否为最底层的具体条款（叶子节点）。回答"是"或"否"（允许对T进行此查询）。
4. 是否同层：询问两个法律节点是否在相同条文层级。回答"是"或"否"。注意：若任一参数为目标节点T，会返回"拒绝：目标不得参与此比较"。

当你收集足够信息后，请提交最终排查报告。答案需包含：
1. 采用的方案（A/B/C/D）
2. 至少两次针对非目标节点的采样记录（节点与对应输出），并基于各深度输出特征排除其余方案的逻辑推理
3. 目标节点 T 的深度（0/1/2/3），并基于已确定方案与对T的允许查询进行论证

若答案错误、格式不符或推理依据不足，排查失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 采样输出（例如查询节点 r）：
<query_sample>r</query_sample>

- 查询子节点（例如查询节点 a1）：
<query_children>a1</query_children>

- 是否叶子（例如查询节点 c111）：
<query_leaf>c111</query_leaf>

- 是否同层（例如比较节点 a1 和 a2）：
<query_same_depth>a1,a2</query_same_depth>

提交最终答案时，必须说明映射方案、采样证据、目标节点T的深度及推理过程，格式如下：

<answer>
方案=A
证据1=节点:r,输出:0
证据2=节点:a1,输出:1
排除逻辑=深度0输出0排除了无效方案，深度1输出1结合深度特征可确定方案A
目标深度=3
目标推理=通过采样T得到输出1，结合方案A中深度3对应输出1，且T为叶子节点，确定T深度为3
</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Legal Provision Hierarchy and Applicability Review System". Let's play a legal framework mapping inference game. Here are the rules:

The system features a legal code hierarchy modeled as a rooted tree with a maximum depth of 3 (basic law has depth 0) and 19 nodes total. Node identifiers and subordinate (parent-child) relationships are as follows:
- Depth 0 (Basic Law/Constitution): r
- Depth 1 (Chapter): r has children a1, a2, a3
- Depth 2 (Section):
  - a1 has children: b11, b12
  - a2 has child: b21
  - a3 has children: b31, b32, b33
- Depth 3 (Article/Clause/Leaves):
  - b11 has children: c111, c112
  - b12 has child: c121
  - b21 has children: c211, c212
  - b31 has child: c311
  - b32 has children: c321, c322
  - b33 has child: c331

There exists a special disputed target node T (whose depth you need to infer).

The Legislative Committee has secretly established a binary amendment applicability rule g(d) based on the provision depth d. There are four candidate rules (exactly one is used):
- Scheme A (Parity Applicability): g(d) = d modulo 2
- Scheme B (Mid-Tier Applicability): g(d) = 1 if and only if d is in the set 1 or 2, otherwise 0
- Scheme C (Specific-Tier Applicability): g(d) = 1 if and only if d is in the set 2 or 3, otherwise 0
- Scheme D (Not Applicable): g(d) = 0 for all d

Your goals are:
1. Determine the actual applicability rule used (A/B/C/D)
2. Determine the depth of target node T (0/1/2/3)

You can repeatedly ask me four types of queries (one per turn), and I will answer truthfully based on the system setup:

1. Sample Output: Ask for the applicability output value of a node. Answer "Output=0" (Not applicable) or "Output=1" (Applicable), equal to g(depth of that node).
2. Query Children: Ask for the list of all subordinate provision nodes. Answer "Children=[...]". Note: If the query target is T, returns "Rejected: Target structure not queryable".
3. Is Leaf: Ask if a node is a terminal clause (leaf node). Answer "Yes" or "No" (this query is allowed for T).
4. Same Depth: Ask if two provision nodes are at the same legislative depth. Answer "Yes" or "No". Note: If either parameter is target node T, returns "Rejected: Target cannot participate in this comparison".

When you have collected enough information, submit your final report. The answer must include:
1. The scheme used (A/B/C/D)
2. At least two sampling records for non-target nodes (node and corresponding output), with logical reasoning to exclude other schemes based on depth-output characteristics
3. The depth of target node T (0/1/2/3), with justification based on the determined scheme and allowed queries for T

If the answer is incorrect, format is invalid, or reasoning is insufficient, the review fails.

Each query must contain only one tag. Use the following XML format:

- Sample Output (e.g., querying node r):
<query_sample>r</query_sample>

- Query Children (e.g., querying node a1):
<query_children>a1</query_children>

- Is Leaf (e.g., querying node c111):
<query_leaf>c111</query_leaf>

- Same Depth (e.g., comparing nodes a1 and a2):
<query_same_depth>a1,a2</query_same_depth>

When submitting the final answer, you must specify the scheme, sampling evidence, target node T's depth, and reasoning process, using this format:

<answer>
Scheme=A
Evidence1=Node:r,Output:0
Evidence2=Node:a1,Output:1
Exclusion_Logic=Depth 0 output 0 excludes invalid schemes, depth 1 output 1 combined with depth characteristics confirms Scheme A
Target_Depth=3
Target_Reasoning=Sampling T yields output 1, combined with Scheme A where depth 3 corresponds to output 1, and T is a leaf node, confirming T depth is 3
</answer>
"""

    tags = ["answer", "query_sample", "query_children", "query_leaf", "query_same_depth"]
    
    reasoning_type = "溯因推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"scheme": "D", "target": "c111"},
            2: {"scheme": "B", "target": "c211"},
            3: {"scheme": "A", "target": "c322"},
            4: {"scheme": "C", "target": "c321"},
            5: {"scheme": "A", "target": "c331"},
        },
        "en": {
            1: {"scheme": "D", "target": "c111"},
            2: {"scheme": "B", "target": "c211"},
            3: {"scheme": "A", "target": "c322"},
            4: {"scheme": "C", "target": "c321"},
            5: {"scheme": "A", "target": "c331"},
        },
    }

    def __init__(self, config):
        self.tree_structure = {
            "r": {"depth": 0, "children": ["a1", "a2", "a3"]},
            "a1": {"depth": 1, "children": ["b11", "b12"]},
            "a2": {"depth": 1, "children": ["b21"]},
            "a3": {"depth": 1, "children": ["b31", "b32", "b33"]},
            "b11": {"depth": 2, "children": ["c111", "c112"]},
            "b12": {"depth": 2, "children": ["c121"]},
            "b21": {"depth": 2, "children": ["c211", "c212"]},
            "b31": {"depth": 2, "children": ["c311"]},
            "b32": {"depth": 2, "children": ["c321", "c322"]},
            "b33": {"depth": 2, "children": ["c331"]},
            "c111": {"depth": 3, "children": []},
            "c112": {"depth": 3, "children": []},
            "c121": {"depth": 3, "children": []},
            "c211": {"depth": 3, "children": []},
            "c212": {"depth": 3, "children": []},
            "c311": {"depth": 3, "children": []},
            "c321": {"depth": 3, "children": []},
            "c322": {"depth": 3, "children": []},
            "c331": {"depth": 3, "children": []},
        }
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.scheme = cfg["scheme"]
        self.target_node = cfg["target"]

        self.scheme_functions = {
            "A": lambda d: d % 2,
            "B": lambda d: 1 if d in [1, 2] else 0,
            "C": lambda d: 1 if d in [2, 3] else 0,
            "D": lambda d: 0,
        }

        self._game_info = {}

    def _get_node_output(self, node):
        if node not in self.tree_structure:
            return None
        depth = self.tree_structure[node]["depth"]
        return self.scheme_functions[self.scheme](depth)

    def _is_leaf(self, node):
        if node not in self.tree_structure:
            return None
        return len(self.tree_structure[node]["children"]) == 0

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        ans_dict = {}
        
        patterns_zh = {
            "scheme": r"方案\s*=\s*([A-D])",
            "evidence1": r"证据1\s*=\s*节点\s*:\s*(\w+)\s*,\s*输出\s*:\s*([01])",
            "evidence2": r"证据2\s*=\s*节点\s*:\s*(\w+)\s*,\s*输出\s*:\s*([01])",
            "target_depth": r"目标深度\s*=\s*([0-3])",
        }
        
        patterns_en = {
            "scheme": r"Scheme\s*=\s*([A-D])",
            "evidence1": r"Evidence1\s*=\s*Node\s*:\s*(\w+)\s*,\s*Output\s*:\s*([01])",
            "evidence2": r"Evidence2\s*=\s*Node\s*:\s*(\w+)\s*,\s*Output\s*:\s*([01])",
            "target_depth": r"Target_Depth\s*=\s*([0-3])",
        }
        
        for key, pattern in patterns_zh.items():
            match = re.search(pattern, raw_ans, re.IGNORECASE)
            if match:
                ans_dict[key] = match.groups()
        
        if len(ans_dict) < 4:
            ans_dict = {}
            for key, pattern in patterns_en.items():
                match = re.search(pattern, raw_ans, re.IGNORECASE)
                if match:
                    ans_dict[key] = match.groups()
        
        if len(ans_dict) < 4:
            return False
        
        if ans_dict["scheme"][0] != self.scheme:
            return False
        
        evidence_nodes = []
        for ev_key in ["evidence1", "evidence2"]:
            if ev_key in ans_dict:
                node, output = ans_dict[ev_key][0], ans_dict[ev_key][1]
                if node == self.target_node:
                    return False
                if node not in self.tree_structure:
                    return False
                expected_output = str(self._get_node_output(node))
                if output != expected_output:
                    return False
                evidence_nodes.append(node)
        
        if len(set(evidence_nodes)) < 2:
            return False
        
        target_depth = int(ans_dict["target_depth"][0])
        expected_depth = self.tree_structure[self.target_node]["depth"]
        if target_depth != expected_depth:
            return False
        
        return True

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        nodes = list(self.tree_structure.keys())
        
        for node in nodes:
            query_tag = "query_sample"
            query_content = node
            xml_query = f"<{query_tag}>{query_content}</{query_tag}>"
            parsed_info = {query_tag: query_content}
            answer = self._cf_core_produce(parsed_info)
            queries.append({"query": xml_query, "answer": answer})

        for node in nodes:
            query_tag = "query_children"
            query_content = node
            xml_query = f"<{query_tag}>{query_content}</{query_tag}>"
            parsed_info = {query_tag: query_content}
            answer = self._cf_core_produce(parsed_info)
            queries.append({"query": xml_query, "answer": answer})

        for node in nodes:
            query_tag = "query_leaf"
            query_content = node
            xml_query = f"<{query_tag}>{query_content}</{query_tag}>"
            parsed_info = {query_tag: query_content}
            answer = self._cf_core_produce(parsed_info)
            queries.append({"query": xml_query, "answer": answer})

        for i, n1 in enumerate(nodes):
            for j, n2 in enumerate(nodes):
                if i >= j:
                    continue
                if n1 == self.target_node or n2 == self.target_node:
                    continue
                query_tag = "query_same_depth"
                query_content = f"{n1},{n2}"
                xml_query = f"<{query_tag}>{query_content}</{query_tag}>"
                parsed_info = {query_tag: query_content}
                answer = self._cf_core_produce(parsed_info)
                queries.append({"query": xml_query, "answer": answer})
        
        return queries

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            reject_structure = "拒绝：目标结构不可查"
            reject_compare = "拒绝：目标不得参与此比较"
            error_node = "错误：节点不存在"
        else:
            yes_res, no_res = "Yes", "No"
            reject_structure = "Rejected: Target structure not queryable"
            reject_compare = "Rejected: Target cannot participate in this comparison"
            error_node = "Error: Node does not exist"

        if "query_sample" in parsed_info:
            node = parsed_info["query_sample"].strip()
            if node not in self.tree_structure:
                return error_node
            output = self._get_node_output(node)
            return f"输出={output}" if self.config.language == "zh" else f"Output={output}"

        elif "query_children" in parsed_info:
            node = parsed_info["query_children"].strip()
            if node not in self.tree_structure:
                return error_node
            if node == self.target_node:
                return reject_structure
            children = self.tree_structure[node]["children"]
            children_str = ",".join(children) if children else ""
            return f"子节点=[{children_str}]" if self.config.language == "zh" else f"Children=[{children_str}]"

        elif "query_leaf" in parsed_info:
            node = parsed_info["query_leaf"].strip()
            if node not in self.tree_structure:
                return error_node
            is_leaf = self._is_leaf(node)
            return yes_res if is_leaf else no_res

        elif "query_same_depth" in parsed_info:
            try:
                raw = parsed_info["query_same_depth"]
                node1, node2 = [x.strip() for x in raw.split(",")]
                
                if node1 not in self.tree_structure or node2 not in self.tree_structure:
                    return error_node
                
                if node1 == self.target_node or node2 == self.target_node:
                    return reject_compare
                
                depth1 = self.tree_structure[node1]["depth"]
                depth2 = self.tree_structure[node2]["depth"]
                return yes_res if depth1 == depth2 else no_res
            except Exception:
                return error_node

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        sample_match = re.search(r'[=]\s*([01])\s*$', correct)
        if sample_match:
            val = sample_match.group(1)
            wrong_val = "1" if val == "0" else "0"
            return correct[:sample_match.start(1)] + wrong_val + correct[sample_match.end(1):]

        if correct.strip().isdigit():
            return str(int(correct.strip()) + 1)

        if self.config.language == "zh":
            if correct.strip() == "是":
                return "否"
            elif correct.strip() == "否":
                return "是"
        else:
            stripped = correct.strip()
            if stripped == "Yes":
                return "No"
            elif stripped == "No":
                return "Yes"
            elif stripped == "yes":
                return "no"
            elif stripped == "no":
                return "yes"

        children_match = re.search(r'(Children=\[|子节点=\[)(.*?)(\])', correct)
        if children_match:
            prefix = children_match.group(1)
            content = children_match.group(2)
            suffix = children_match.group(3)
            if content.strip():
                return prefix + content + ",fake_node" + suffix
            else:
                return prefix + "fake_node" + suffix

        return correct + "_WRONG"