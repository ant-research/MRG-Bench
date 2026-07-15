import re
from collections import deque
from typing import List, Dict, Set, Tuple
from .base import Game

class TreeIsomorphismGame(Game):

    game_rule_zh = """\
我们来玩一个"树结构推理"游戏。规则如下：

给定一棵有根树 T，包含 {n} 个节点，编号从 1 到 {n}，根节点为 1。树的完整结构如下：

{tree_structure}

注意：这是一棵无序有根树，即每个节点的孩子之间没有顺序关系。

系统内部对任意两个不同节点 u 和 v 有一个固定的二元判定 R(u, v)，返回"是"或"否"。你的目标是通过有限次查询归纳出这个判定规则，并在最终挑战中正确预测给定节点对的判定结果。

游戏分为两个阶段：

你可以进行以下操作（请尽可能少地使用查询次数）：

- **试验查询**：询问节点对 (u, v) 是否满足判定 R，其中 u 不等于 v。系统会返回"是"或"否"。

你需要对以下 {k} 对节点对预测判定结果：
{challenge_pairs_text}

你需要：
- 对每一对节点直接预测判定结果（"是"或"否"），不能再进行试验查询。
- 可选：给出你归纳出的判定规则的描述（一句话）。

- 对挑战阶段的所有节点对预测完全正确。
- 如果提供规则描述，则该描述需要与真实判定规则等价。

每次只能包含一个标签，请严格使用以下 XML 格式：

- **试验查询**（例如询问节点 2 和 5）：
<query_test>2,5</query_test>

- **查看树结构**（可随时请求，不计入查询次数）：
<query_structure></query_structure>

- **提交挑战答案**（当你认为已掌握规则时即可提交）：
<answer>predictions=是,否,是,否,是; rule=你归纳的规则描述</answer>

其中 predictions 包含 {k} 个预测结果（用逗号分隔，顺序对应系统给出的节点对顺序），rule 为可选项。

注意：在探索阶段请先进行若干次试验查询以归纳规律，当你认为已掌握规则时，可以直接提交答案。如果达到查询次数上限，系统会自动进入挑战阶段。
"""

    game_rule_en = """\
Let's play a "Tree Structure Reasoning" game. Here are the rules:

You are given a rooted tree T with {n} nodes, numbered from 1 to {n}, with node 1 as the root. The complete tree structure is as follows:

{tree_structure}

Note: This is an unordered rooted tree, meaning the children of each node have no particular order.

The system has a fixed binary predicate R(u, v) for any two distinct nodes u and v, returning "Yes" or "No". Your goal is to infer this predicate through limited queries and correctly predict the results for given node pairs in the final challenge.

The game consists of two phases:

You can perform the following operations (use as few queries as possible):

- **Test Query**: Ask whether a node pair (u, v) satisfies predicate R, where u is not equal to v. The system will return "Yes" or "No".

You will need to predict the result for the following {k} node pairs:
{challenge_pairs_text}

You need to:
- Directly predict the result ("Yes" or "No") for each pair without making further test queries.
- Optional: Provide a one-sentence description of the rule you've inferred.

- All predictions for the challenge phase node pairs must be correct.
- If a rule description is provided, it must be equivalent to the true predicate.

Each turn must contain only one tag. Strictly use the following XML format:

- **Test Query** (e.g., asking about nodes 2 and 5):
<query_test>2,5</query_test>

- **View Tree Structure** (can be requested anytime, does not count toward query limit):
<query_structure></query_structure>

- **Submit Challenge Answer** (when you are ready):
<answer>predictions=Yes,No,Yes,No,Yes; rule=Your inferred rule description</answer>

The predictions field contains {k} results (comma-separated, in the order of the node pairs listed above), and rule is optional.

Note: During the exploration phase, please conduct several test queries to infer the pattern. When you are confident, submit your answer. If you reach the maximum query limit, the system will automatically enter the challenge phase.
"""

    contextualized_rule_zh_1 = """\
我们来使用"路网拓扑结构分析"系统。规则如下：

给定一个交通路网的级联监控树 T，包含 {n} 个节点（站点），编号从 1 到 {n}，总控中心节点为 1。监控网络的完整结构如下：

{tree_structure}

注意：这是一棵无序有根树，即每个站点的下级监控分支之间没有特定的顺序关系。

交通系统内部对任意两个不同的监控节点 u 和 v 有一个固定的二元判定 R(u, v)（用于评估其下游拓扑结构是否完全一致，以便进行流量控制方案的直接复用），返回"是"或"否"。你的目标是通过有限次查询归纳出这个判定规则，并在最终挑战中正确预测给定节点对的判定结果。

操作分为两个阶段：

你可以进行以下操作（请尽可能少地使用查询次数）：

- **试验查询**：询问节点对 (u, v) 是否满足判定 R，其中 u 不等于 v。系统会返回"是"或"否"。

你需要对以下 {k} 对节点对预测判定结果：
{challenge_pairs_text}

你需要：
- 对每一对监控节点直接预测判定结果（"是"或"否"），不能再进行试验查询。
- 可选：给出你归纳出的判定规则的描述（一句话）。

- 对挑战阶段的所有节点对预测完全正确。
- 如果提供规则描述，则该描述需要与真实的拓扑判定规则等价。

每次只能包含一个标签，请严格使用以下 XML 格式：

- **试验查询**（例如询问监控节点 2 和 5）：
<query_test>2,5</query_test>

- **查看树结构**（可随时请求，不计入查询次数）：
<query_structure></query_structure>

- **提交挑战答案**（当你认为已掌握规则时即可提交）：
<answer>predictions=是,否,是,否,是; rule=你归纳的规则描述</answer>

其中 predictions 包含 {k} 个预测结果（用逗号分隔，顺序对应系统给出的节点对顺序），rule 为可选项。

注意：在探索阶段请先进行若干次试验查询以归纳规律，当你认为已掌握规则时，可以直接提交答案。如果达到查询次数上限，系统会自动进入挑战阶段。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's use the "Road Network Topology Analysis" system. Here are the rules:

You are managing a cascaded traffic monitoring tree network T with {n} nodes (stations), numbered from 1 to {n}, with the main control center as node 1. The complete network structure is as follows:

{tree_structure}

Note: This is an unordered rooted tree, meaning the downstream monitoring branches of each station have no particular order.

The traffic system has a fixed binary predicate R(u, v) for any two distinct monitoring nodes u and v (used to evaluate if their downstream topologies are completely identical for the direct reuse of traffic flow scheduling plans), returning "Yes" or "No". Your goal is to infer this predicate through limited queries and correctly predict the results for given node pairs in the final challenge.

The operation consists of two phases:

You can perform the following operations (use as few queries as possible):

- **Test Query**: Ask whether a node pair (u, v) satisfies predicate R, where u is not equal to v. The system will return "Yes" or "No".

You will need to predict the result for the following {k} node pairs:
{challenge_pairs_text}

You need to:
- Directly predict the result ("Yes" or "No") for each monitoring node pair without making further test queries.
- Optional: Provide a one-sentence description of the rule you've inferred.

- All predictions for the challenge phase node pairs must be correct.
- If a rule description is provided, it must be equivalent to the true topology predicate.

Each turn must contain only one tag. Strictly use the following XML format:

- **Test Query** (e.g., asking about monitoring nodes 2 and 5):
<query_test>2,5</query_test>

- **View Tree Structure** (can be requested anytime, does not count toward query limit):
<query_structure></query_structure>

- **Submit Challenge Answer** (when you are ready):
<answer>predictions=Yes,No,Yes,No,Yes; rule=Your inferred rule description</answer>

The predictions field contains {k} results (comma-separated, in the order of the system-provided node pairs), and rule is optional.

Note: During the exploration phase, please conduct several test queries to infer the pattern. When you are confident, submit your answer. If you reach the maximum query limit, the system will automatically enter the challenge phase.
"""

    contextualized_rule_zh_2 = """\
我们来使用"病毒变异溯源与演化结构分析"系统。规则如下：

给定一棵病毒变异演化树 T，包含 {n} 个节点（代表不同的病毒变异株），编号从 1 到 {n}，原始毒株为节点 1。变异株的完整演化级联如下：

{tree_structure}

注意：这是一棵无序有根树，即每个变异株的下游衍生分支之间没有特定的顺序关系。

医疗分析系统内部对任意两个不同的变异株节点 u 和 v 有一个固定的二元判定 R(u, v)（用于评估其衍生变异分支结构是否完全相同，以决定是否可以使用相同的广谱疫苗策略），返回"是"或"否"。你的目标是通过有限次查询归纳出这个判定规则，并在最终挑战中正确预测给定节点对的判定结果。

操作分为两个阶段：

你可以进行以下操作（请尽可能少地使用查询次数）：

- **试验查询**：询问节点对 (u, v) 是否满足判定 R，其中 u 不等于 v。系统会返回"是"或"否"。

你需要对以下 {k} 对节点对预测判定结果：
{challenge_pairs_text}

你需要：
- 对每一对变异株节点直接预测判定结果（"是"或"否"），不能再进行试验查询。
- 可选：给出你归纳出的判定规则的描述（一句话）。

- 对挑战阶段的所有节点对预测完全正确。
- 如果提供规则描述，则该描述需要与真实的衍生演化判定规则等价。

每次只能包含一个标签，请严格使用以下 XML 格式：

- **试验查询**（例如询问变异株节点 2 和 5）：
<query_test>2,5</query_test>

- **查看树结构**（可随时请求，不计入查询次数）：
<query_structure></query_structure>

- **提交挑战答案**（当你认为已掌握规则时即可提交）：
<answer>predictions=是,否,是,否,是; rule=你归纳的规则描述</answer>

其中 predictions 包含 {k} 个预测结果（用逗号分隔，顺序对应系统给出的节点对顺序），rule 为可选项。

注意：在探索阶段请先进行若干次试验查询以归纳规律，当你认为已掌握规则时，可以直接提交答案。如果达到查询次数上限，系统会自动进入挑战阶段。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's use the "Viral Mutation Tracking and Evolutionary Structure Analysis" system. Here are the rules:

You are provided with a viral mutation evolutionary tree T, containing {n} nodes (representing different viral strains), numbered from 1 to {n}, with the original strain as node 1. The complete evolutionary cascade of the strains is as follows:

{tree_structure}

Note: This is an unordered rooted tree, meaning the downstream derivative branches of each strain have no particular order.

The medical analysis system has a fixed binary predicate R(u, v) for any two distinct strain nodes u and v (used to evaluate if their downstream mutation branch structures are completely identical to determine whether the same broad-spectrum vaccine strategies can be reused), returning "Yes" or "No". Your goal is to infer this predicate through limited queries and correctly predict the results for given node pairs in the final challenge.

The operation consists of two phases:

You can perform the following operations (use as few queries as possible):

- **Test Query**: Ask whether a node pair (u, v) satisfies predicate R, where u is not equal to v. The system will return "Yes" or "No".

You will need to predict the result for the following {k} node pairs:
{challenge_pairs_text}

You need to:
- Directly predict the result ("Yes" or "No") for each strain node pair without making further test queries.
- Optional: Provide a one-sentence description of the rule you've inferred.

- All predictions for the challenge phase node pairs must be correct.
- If a rule description is provided, it must be equivalent to the true evolutionary derivative predicate.

Each turn must contain only one tag. Strictly use the following XML format:

- **Test Query** (e.g., asking about strain nodes 2 and 5):
<query_test>2,5</query_test>

- **View Tree Structure** (can be requested anytime, does not count toward query limit):
<query_structure></query_structure>

- **Submit Challenge Answer** (when you are ready):
<answer>predictions=Yes,No,Yes,No,Yes; rule=Your inferred rule description</answer>

The predictions field contains {k} results (comma-separated, in the order of the system-provided node pairs), and rule is optional.

Note: During the exploration phase, please conduct several test queries to infer the pattern. When you are confident, submit your answer. If you reach the maximum query limit, the system will automatically enter the challenge phase.
"""

    contextualized_rule_zh_3 = """\
我们来使用"学科知识网络结构图谱"分析系统。规则如下：

给定一棵学科知识树 T，包含 {n} 个节点（代表不同的知识点），编号从 1 到 {n}，核心基础概念为节点 1。知识图谱的完整前置依赖关系如下：

{tree_structure}

注意：这是一棵无序有根树，即每个知识点的后续衍生知识分支之间没有特定的先后顺序关系。

教研系统内部对任意两个不同的知识点节点 u 和 v 有一个固定的二元判定 R(u, v)（用于评估这两个知识点的后续延展知识体系结构是否完全相同，以便直接复用教学大纲模板），返回"是"或"否"。你的目标是通过有限次查询归纳出这个判定规则，并在最终挑战中正确预测给定节点对的判定结果。

操作分为两个阶段：

你可以进行以下操作（请尽可能少地使用查询次数）：

- **试验查询**：询问节点对 (u, v) 是否满足判定 R，其中 u 不等于 v。系统会返回"是"或"否"。

你需要对以下 {k} 对节点对预测判定结果：
{challenge_pairs_text}

你需要：
- 对每一对知识点节点直接预测判定结果（"是"或"否"），不能再进行试验查询。
- 可选：给出你归纳出的判定规则的描述（一句话）。

- 对挑战阶段的所有节点对预测完全正确。
- 如果提供规则描述，则该描述需要与真实的知识体系图谱判定规则等价。

每次只能包含一个标签，请严格使用以下 XML 格式：

- **试验查询**（例如询问知识点节点 2 和 5）：
<query_test>2,5</query_test>

- **查看树结构**（可随时请求，不计入查询次数）：
<query_structure></query_structure>

- **提交挑战答案**（当你认为已掌握规则时即可提交）：
<answer>predictions=是,否,是,否,是; rule=你归纳的规则描述</answer>

其中 predictions 包含 {k} 个预测结果（用逗号分隔，顺序对应系统给出的节点对顺序），rule 为可选项。

注意：在探索阶段请先进行若干次试验查询以归纳规律，当你认为已掌握规则时，可以直接提交答案。如果达到查询次数上限，系统会自动进入挑战阶段。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's use the "Subject Knowledge Network Structure Graph" analysis system. Here are the rules:

You are provided with an academic knowledge tree T containing {n} nodes (representing different knowledge points), numbered from 1 to {n}, with the core fundamental concept as node 1. The complete prerequisite dependency relationships of the knowledge graph are as follows:

{tree_structure}

Note: This is an unordered rooted tree, meaning the subsequent derivative knowledge branches of each knowledge point have no particular order.

The educational research system has a fixed binary predicate R(u, v) for any two distinct knowledge nodes u and v (used to evaluate if their subsequent extended knowledge architectures are completely identical, allowing direct reuse of curriculum templates), returning "Yes" or "No". Your goal is to infer this predicate through limited queries and correctly predict the results for given node pairs in the final challenge.

The operation consists of two phases:

You can perform the following operations (use as few queries as possible):

- **Test Query**: Ask whether a node pair (u, v) satisfies predicate R, where u is not equal to v. The system will return "Yes" or "No".

You will need to predict the result for the following {k} node pairs:
{challenge_pairs_text}

You need to:
- Directly predict the result ("Yes" or "No") for each knowledge node pair without making further test queries.
- Optional: Provide a one-sentence description of the rule you've inferred.

- All predictions for the challenge phase node pairs must be correct.
- If a rule description is provided, it must be equivalent to the true knowledge graph predicate.

Each turn must contain only one tag. Strictly use the following XML format:

- **Test Query** (e.g., asking about knowledge nodes 2 and 5):
<query_test>2,5</query_test>

- **View Tree Structure** (can be requested anytime, does not count toward query limit):
<query_structure></query_structure>

- **Submit Challenge Answer** (when you are ready):
<answer>predictions=Yes,No,Yes,No,Yes; rule=Your inferred rule description</answer>

The predictions field contains {k} results (comma-separated, in the order of the system-provided node pairs), and rule is optional.

Note: During the exploration phase, please conduct several test queries to infer the pattern. When you are confident, submit your answer. If you reach the maximum query limit, the system will automatically enter the challenge phase.
"""

    contextualized_rule_zh_4 = """\
我们来使用"产品BOM(物料清单)装配层级分析"系统。规则如下：

给定一棵产品装配树 T，包含 {n} 个节点（代表组件或零件），编号从 1 到 {n}，顶层成品总成节点为 1。产品的完整向下拆解结构如下：

{tree_structure}

注意：这是一棵无序有根树，即每个组件的下级子部件拆解之间没有特定的装配顺序关系。

制造系统内部对任意两个不同的组件节点 u 和 v 有一个固定的二元判定 R(u, v)（用于评估这两个组件的向下拆解装配结构是否完全相同，以决定是否能共用同一套自动化装配流水线），返回"是"或"否"。你的目标是通过有限次查询归纳出这个判定规则，并在最终挑战中正确预测给定节点对的判定结果。

操作分为两个阶段：

你可以进行以下操作（请尽可能少地使用查询次数）：

- **试验查询**：询问节点对 (u, v) 是否满足判定 R，其中 u 不等于 v。系统会返回"是"或"否"。

你需要对以下 {k} 对节点对预测判定结果：
{challenge_pairs_text}

你需要：
- 对每一对组件节点直接预测判定结果（"是"或"否"），不能再进行试验查询。
- 可选：给出你归纳出的判定规则的描述（一句话）。

- 对挑战阶段的所有节点对预测完全正确。
- 如果提供规则描述，则该描述需要与真实的BOM装配结构判定规则等价。

每次只能包含一个标签，请严格使用以下 XML 格式：

- **试验查询**（例如询问组件节点 2 和 5）：
<query_test>2,5</query_test>

- **查看树结构**（可随时请求，不计入查询次数）：
<query_structure></query_structure>

- **提交挑战答案**（当你认为已掌握规则时即可提交）：
<answer>predictions=是,否,是,否,是; rule=你归纳的规则描述</answer>

其中 predictions 包含 {k} 个预测结果（用逗号分隔，顺序对应系统给出的节点对顺序），rule 为可选项。

注意：在探索阶段请先进行若干次试验查询以归纳规律，当你认为已掌握规则时，可以直接提交答案。如果达到查询次数上限，系统会自动进入挑战阶段。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's use the "Product BOM (Bill of Materials) Assembly Hierarchy Analysis" system. Here are the rules:

You are provided with a product assembly tree T containing {n} nodes (representing components or parts), numbered from 1 to {n}, with the top-level final product assembly as node 1. The complete downward teardown structure of the product is as follows:

{tree_structure}

Note: This is an unordered rooted tree, meaning the lower-level subcomponents of each assembly have no particular assembly sequence relationship.

The manufacturing system has a fixed binary predicate R(u, v) for any two distinct component nodes u and v (used to evaluate if their downward teardown assembly structures are completely identical, to determine if they can share the same automated assembly line), returning "Yes" or "No". Your goal is to infer this predicate through limited queries and correctly predict the results for given node pairs in the final challenge.

The operation consists of two phases:

You can perform the following operations (use as few queries as possible):

- **Test Query**: Ask whether a node pair (u, v) satisfies predicate R, where u is not equal to v. The system will return "Yes" or "No".

You will need to predict the result for the following {k} node pairs:
{challenge_pairs_text}

You need to:
- Directly predict the result ("Yes" or "No") for each component node pair without making further test queries.
- Optional: Provide a one-sentence description of the rule you've inferred.

- All predictions for the challenge phase node pairs must be correct.
- If a rule description is provided, it must be equivalent to the true BOM assembly structure predicate.

Each turn must contain only one tag. Strictly use the following XML format:

- **Test Query** (e.g., asking about component nodes 2 and 5):
<query_test>2,5</query_test>

- **View Tree Structure** (can be requested anytime, does not count toward query limit):
<query_structure></query_structure>

- **Submit Challenge Answer** (when you are ready):
<answer>predictions=Yes,No,Yes,No,Yes; rule=Your inferred rule description</answer>

The predictions field contains {k} results (comma-separated, in the order of the system-provided node pairs), and rule is optional.

Note: During the exploration phase, please conduct several test queries to infer the pattern. When you are confident, submit your answer. If you reach the maximum query limit, the system will automatically enter the challenge phase.
"""

    contextualized_rule_zh_5 = """\
我们来使用"司法判例派生关系拓扑分析"系统。规则如下：

给定一棵判例引用派生树 T，包含 {n} 个节点（代表不同的司法判例），编号从 1 到 {n}，最初始的基准先例节点为 1。判例体系的完整派生关系如下：

{tree_structure}

注意：这是一棵无序有根树，即每个判例衍生出的后续引用案例之间没有特定的顺序关系。

司法分析系统内部对任意两个不同的判例节点 u 和 v 有一个固定的二元判定 R(u, v)（用于评估这两个判例的后续派生法理演变结构是否完全一致，以确认它们在法理适用与裁量标准上的等效性），返回"是"或"否"。你的目标是通过有限次查询归纳出这个判定规则，并在最终挑战中正确预测给定节点对的判定结果。

操作分为两个阶段：

你可以进行以下操作（请尽可能少地使用查询次数）：

- **试验查询**：询问节点对 (u, v) 是否满足判定 R，其中 u 不等于 v。系统会返回"是"或"否"。

你需要对以下 {k} 对节点对预测判定结果：
{challenge_pairs_text}

你需要：
- 对每一对判例节点直接预测判定结果（"是"或"否"），不能再进行试验查询。
- 可选：给出你归纳出的判定规则的描述（一句话）。

- 对挑战阶段的所有节点对预测完全正确。
- 如果提供规则描述，则该描述需要与真实的法理派生判定规则等价。

每次只能包含一个标签，请严格使用以下 XML 格式：

- **试验查询**（例如询问判例节点 2 和 5）：
<query_test>2,5</query_test>

- **查看树结构**（可随时请求，不计入查询次数）：
<query_structure></query_structure>

- **提交挑战答案**（当你认为已掌握规则时即可提交）：
<answer>predictions=是,否,是,否,是; rule=你归纳的规则描述</answer>

其中 predictions 包含 {k} 个预测结果（用逗号分隔，顺序对应系统给出的节点对顺序），rule 为可选项。

注意：在探索阶段请先进行若干次试验查询以归纳规律，当你认为已掌握规则时，可以直接提交答案。如果达到查询次数上限，系统会自动进入挑战阶段。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's use the "Judicial Precedent Derivation Topology Analysis" system. Here are the rules:

You are provided with a precedent citation derivation tree T containing {n} nodes (representing different judicial precedents), numbered from 1 to {n}, with the initial benchmark precedent as node 1. The complete derivation relations of the precedent system are as follows:

{tree_structure}

Note: This is an unordered rooted tree, meaning the subsequent cited cases derived from each precedent have no particular order.

The judicial analysis system has a fixed binary predicate R(u, v) for any two distinct precedent nodes u and v (used to evaluate if their subsequent derived jurisprudential evolution structures are completely identical, confirming their equivalence in legal application and discretionary standards), returning "Yes" or "No". Your goal is to infer this predicate through limited queries and correctly predict the results for given node pairs in the final challenge.

The operation consists of two phases:

You can perform the following operations (use as few queries as possible):

- **Test Query**: Ask whether a node pair (u, v) satisfies predicate R, where u is not equal to v. The system will return "Yes" or "No".

You will need to predict the result for the following {k} node pairs:
{challenge_pairs_text}

You need to:
- Directly predict the result ("Yes" or "No") for each precedent node pair without making further test queries.
- Optional: Provide a one-sentence description of the rule you've inferred.

- All predictions for the challenge phase node pairs must be correct.
- If a rule description is provided, it must be equivalent to the true jurisprudential derivation predicate.

Each turn must contain only one tag. Strictly use the following XML format:

- **Test Query** (e.g., asking about precedent nodes 2 and 5):
<query_test>2,5</query_test>

- **View Tree Structure** (can be requested anytime, does not count toward query limit):
<query_structure></query_structure>

- **Submit Challenge Answer** (when you are ready):
<answer>predictions=Yes,No,Yes,No,Yes; rule=Your inferred rule description</answer>

The predictions field contains {k} results (comma-separated, in the order of the system-provided node pairs), and rule is optional.

Note: During the exploration phase, please conduct several test queries to infer the pattern. When you are confident, submit your answer. If you reach the maximum query limit, the system will automatically enter the challenge phase.
"""

    tags = ["answer", "query_test", "query_structure"]

    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 12,
                "q": 10,
                "k": 5,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (4, 9), (6, 10), (6, 11), (5, 12)],
                "challenge_pairs": [(4, 6), (2, 3), (8, 10), (5, 7), (4, 5)],
            },
            2: {
                "n": 15,
                "q": 10,
                "k": 6,
                "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (3, 8), (4, 9), (5, 10), (5, 11), (7, 12), (7, 13), (9, 14), (9, 15)],
                "challenge_pairs": [(2, 3), (5, 7), (10, 12), (6, 8), (2, 4), (5, 9)],
            },
            3: {
                "n": 18,
                "q": 10,
                "k": 6,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (2, 6), (3, 7), (3, 8), (4, 9), (4, 10), (5, 11), (7, 12), (7, 13), (8, 14), (9, 15), (9, 16), (12, 17), (12, 18)],
                "challenge_pairs": [(4, 7), (9, 12), (5, 8), (2, 3), (4, 9), (7, 12)],
            },
            4: {
                "n": 22,
                "q": 9,
                "k": 7,
                "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (3, 8), (3, 9), (4, 10), (5, 11), (5, 12), (6, 13), (7, 14), (7, 15), (8, 16), (10, 17), (10, 18), (11, 19), (11, 20), (14, 21), (14, 22)],
                "challenge_pairs": [(5, 7), (11, 14), (2, 3), (5, 10), (6, 8), (11, 7), (19, 21)],
            },
            5: {
                "n": 25,
                "q": 8,
                "k": 8,
                "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (2, 7), (3, 8), (3, 9), (4, 10), (4, 11), (5, 12), (5, 13), (6, 14), (8, 15), (8, 16), (9, 17), (10, 18), (10, 19), (11, 20), (12, 21), (12, 22), (15, 23), (15, 24), (18, 25)],
                "challenge_pairs": [(5, 8), (12, 15), (2, 3), (5, 10), (6, 9), (12, 8), (13, 16), (2, 4)],
            },
        },
        "en": {
            1: {
                "n": 12,
                "q": 10,
                "k": 5,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (4, 9), (6, 10), (6, 11), (5, 12)],
                "challenge_pairs": [(4, 6), (2, 3), (8, 10), (5, 7), (4, 5)],
            },
            2: {
                "n": 15,
                "q": 10,
                "k": 6,
                "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (3, 8), (4, 9), (5, 10), (5, 11), (7, 12), (7, 13), (9, 14), (9, 15)],
                "challenge_pairs": [(2, 3), (5, 7), (10, 12), (6, 8), (2, 4), (5, 9)],
            },
            3: {
                "n": 18,
                "q": 10,
                "k": 6,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (2, 6), (3, 7), (3, 8), (4, 9), (4, 10), (5, 11), (7, 12), (7, 13), (8, 14), (9, 15), (9, 16), (12, 17), (12, 18)],
                "challenge_pairs": [(4, 7), (9, 12), (5, 8), (2, 3), (4, 9), (7, 12)],
            },
            4: {
                "n": 22,
                "q": 9,
                "k": 7,
                "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (3, 8), (3, 9), (4, 10), (5, 11), (5, 12), (6, 13), (7, 14), (7, 15), (8, 16), (10, 17), (10, 18), (11, 19), (11, 20), (14, 21), (14, 22)],
                "challenge_pairs": [(5, 7), (11, 14), (2, 3), (5, 10), (6, 8), (11, 7), (19, 21)],
            },
            5: {
                "n": 25,
                "q": 8,
                "k": 8,
                "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (2, 7), (3, 8), (3, 9), (4, 10), (4, 11), (5, 12), (5, 13), (6, 14), (8, 15), (8, 16), (9, 17), (10, 18), (10, 19), (11, 20), (12, 21), (12, 22), (15, 23), (15, 24), (18, 25)],
                "challenge_pairs": [(5, 8), (12, 15), (2, 3), (5, 10), (6, 9), (12, 8), (13, 16), (2, 4)],
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0
        self.max_queries = 0
        self.challenge_mode = False
        self.challenge_pairs = []
        self.children = {}
        self.tree_structure_text = ""
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self._game_info["n"] = cfg["n"]
        self._game_info["k"] = cfg["k"]
        self.max_queries = cfg["q"]
        
        edges = cfg["edges"]
        self.children = {i: [] for i in range(1, cfg["n"] + 1)}
        for parent, child in edges:
            self.children[parent].append(child)
        
        self._build_tree_structure_text()
        self._game_info["tree_structure"] = self.tree_structure_text
        
        self.challenge_pairs = cfg["challenge_pairs"]
        
        self._game_info["challenge_pairs_text"] = self._format_challenge_pairs()
        
        self._compute_isomorphism()

    def _build_tree_structure_text(self):
        lines = []
        for node in sorted(self.children.keys()):
            if self.children[node]:
                children_str = ", ".join(map(str, sorted(self.children[node])))
                if self.config.language == "zh":
                    lines.append(f"节点 {node} 的孩子：{children_str}")
                else:
                    lines.append(f"Node {node}'s children: {children_str}")
            else:
                if self.config.language == "zh":
                    lines.append(f"节点 {node} 是叶子节点")
                else:
                    lines.append(f"Node {node} is a leaf")
        self.tree_structure_text = "\n".join(lines)

    def _get_subtree_signature(self, node: int) -> Tuple:
        if not self.children[node]:
            return (0,)
        
        child_sigs = []
        for child in self.children[node]:
            child_sigs.append(self._get_subtree_signature(child))
        
        child_sigs.sort()
        return (1, tuple(child_sigs))

    def _compute_isomorphism(self):
        self.isomorphism_map = {}
        n = self._game_info["n"]
        
        signatures = {}
        for node in range(1, n + 1):
            signatures[node] = self._get_subtree_signature(node)
        
        for u in range(1, n + 1):
            for v in range(1, n + 1):
                if u != v:
                    self.isomorphism_map[(u, v)] = (signatures[u] == signatures[v])

    def evaluate(self, parsed_info):
        if not self.challenge_mode:
            self.challenge_mode = True
        
        raw_ans = parsed_info["answer"]
        
        parts = raw_ans.split(";")
        predictions_str = ""
        rule_str = ""
        
        for part in parts:
            part = part.strip()
            if part.startswith("predictions="):
                predictions_str = part.split("=", 1)[1].strip()
            elif part.startswith("rule="):
                rule_str = part.split("=", 1)[1].strip()
        
        if not predictions_str:
            return False
        
        try:
            predictions = [p.strip() for p in predictions_str.split(",")]
            if len(predictions) != len(self.challenge_pairs):
                return False
            
            yes_answers = {"是", "yes", "Yes", "YES"}
            no_answers = {"否", "no", "No", "NO"}
            
            for i, (u, v) in enumerate(self.challenge_pairs):
                pred = predictions[i]
                actual = self.isomorphism_map.get((u, v), False)
                
                if pred in yes_answers:
                    pred_bool = True
                elif pred in no_answers:
                    pred_bool = False
                else:
                    return False
                
                if pred_bool != actual:
                    return False
            
            return True
            
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        if "query_structure" in parsed_info:
            return self.tree_structure_text

        if "query_test" in parsed_info:
            if self.challenge_mode:
                return "错误：已进入挑战阶段，不能再进行试验查询。" if self.config.language == "zh" else "Error: Already in challenge phase, no more test queries allowed."
            
            self.query_count += 1
            
            try:
                raw = parsed_info["query_test"]
                u, v = [int(x.strip()) for x in raw.split(",")]
                
                n = self._game_info["n"]
                if u < 1 or u > n or v < 1 or v > n or u == v:
                    return "错误：节点编号无效或相同。" if self.config.language == "zh" else "Error: Invalid or identical node IDs."
                
                result = yes_res if self.isomorphism_map.get((u, v), False) else no_res
                
                if self.query_count >= self.max_queries:
                    self.challenge_mode = True
                    challenge_text = self._format_challenge_pairs()
                    if self.config.language == "zh":
                        return f"{result}\n\n你已达到最大查询次数。现在进入挑战阶段，请对以下节点对进行预测：\n{challenge_text}"
                    else:
                        return f"{result}\n\nYou have reached the maximum number of queries. Now entering challenge phase. Please predict for the following node pairs:\n{challenge_text}"
                
                return result
                
            except Exception:
                return "错误：查询格式无效。" if self.config.language == "zh" else "Error: Invalid query format."

        if self.config.language == "zh":
            return "错误：未识别的查询标签，请使用 <query_test> 或 <query_structure>。"
        else:
            return "Error: Unrecognized query tag. Please use <query_test> or <query_structure>."

    def _cf_make_wrong(self, correct: str) -> str:
        lines = correct.split("\n", 1)
        first_line = lines[0].strip()
        
        mapping = {
            "是": "否", "否": "是",
            "Yes": "No", "No": "Yes",
            "YES": "NO", "NO": "YES",
            "yes": "no", "no": "yes"
        }
        
        if first_line in mapping:
            flipped = mapping[first_line]
            if len(lines) > 1:
                return flipped + "\n" + lines[1]
            return flipped
        
        if first_line.isdigit():
            flipped = str(int(first_line) + 1)
            if len(lines) > 1:
                return flipped + "\n" + lines[1]
            return flipped
        
        return correct + "_WRONG"

    def _format_challenge_pairs(self) -> str:
        lines = []
        for i, (u, v) in enumerate(self.challenge_pairs, 1):
            lines.append(f"{i}. ({u}, {v})")
        return "\n".join(lines)

    def get_all_possible_queries(self) -> List[Dict]:
        queries = []
        n = self._game_info["n"]
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        for u in range(1, n + 1):
            for v in range(1, n + 1):
                if u == v:
                    continue
                
                query_content = f"<query_test>{u},{v}</query_test>"
                
                is_isomorphic = self.isomorphism_map.get((u, v), False)
                ans = yes_res if is_isomorphic else no_res
                
                queries.append({
                    "query": query_content,
                    "answer": ans
                })
        
        return queries