# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   删除节点影响：删除某节点后，树分裂为几棵独立的树
# ============================================================

from .base import Game
import random


class HiddenTreeStructureGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "树"

    game_rule_zh = """\
我们现在来玩一个"隐藏树结构推理"游戏，规则如下：

游戏设定了一棵特殊结构的树，该树有 {n} 个节点，编号为 1 到 {n}。这棵树具有以下隐藏性质：

1. **树的结构**：树由一条"骨干路径"和若干"叶子节点"组成。骨干路径是一条长度为 M 的节点序列，骨干上的每个节点可以附加若干叶子节点。

2. **隐藏的编号映射规则**：
   - 存在一个未知的模数 p（p 大于等于 2）和一个未知的余数 r0（0 小于等于 r0 小于 p）。
   - 所有编号中，满足"编号除以 p 余 r0"的编号，按从小到大的顺序依次对应骨干路径上的节点。
   - 其余编号则对应叶子节点，按照骨干节点的顺序依次分配（先分配第一个骨干节点的所有叶子，再分配第二个骨干节点的所有叶子，以此类推）。

3. **隐藏的周期性规律**：
   - 每个骨干节点附加的叶子数量按照一个未知的周期 q（q 大于等于 1）重复。
   - 存在一个长度为 q 的基础序列，骨干节点的叶子数量按此序列周期性重复。

你的目标是通过询问节点的度数（即与该节点相连的边的数量），推断出完整的树结构规律，并给出一个预测规则。

## 可用操作

你可以反复进行以下操作：

1. **度数查询**：询问某个编号的节点的度数。格式如下：
   <query_degree>编号</query_degree>
   例如，查询编号 5 的度数：
   <query_degree>5</query_degree>

2. **提交预测规则**：当你认为已经推断出规律后，提交你的预测规则。格式如下：
   <answer>p=模数值, r0=余数值, q=周期值, pattern=叶子数序列</answer>
   
   其中：
   - p：编号到骨干的模数
   - r0：编号到骨干的余数
   - q：叶子数量的周期长度
   - pattern：长度为 q 的叶子数量序列，用逗号分隔
   
   例如：
   <answer>p=3, r0=1, q=2, pattern=1,2</answer>

## 评估说明

- 你最多可以进行 {max_queries} 次度数查询。
- 提交预测规则后，系统会在 {test_samples} 个未被查询过的编号上测试你的规则。
- 只有当所有测试编号的预测度数都正确时，游戏才算成功。
- 如果超过最大查询次数未提交答案，或预测规则错误，游戏失败。

## 提示

- 骨干路径两端的节点度数会比中间骨干节点少 1（因为端点只连接一个骨干邻居）。
- 所有叶子节点的度数都是 1。
- 请尽可能少地使用查询次数来推断规律。
"""

    game_rule_en = """\
Let's play a "Hidden Tree Structure Inference" game. Here are the rules:

The game involves a specially structured tree with {n} nodes, numbered from 1 to {n}. This tree has the following hidden properties:

1. **Tree Structure**: The tree consists of a "backbone path" and several "leaf nodes". The backbone path is a sequence of M nodes, and each backbone node can have several leaf nodes attached.

2. **Hidden Numbering Mapping Rule**:
   - There exists an unknown modulus p (p greater than or equal to 2) and an unknown remainder r0 (0 less than or equal to r0 less than p).
   - Among all node IDs, those satisfying "ID modulo p equals r0" are mapped to backbone nodes in ascending order.
   - The remaining IDs correspond to leaf nodes, allocated sequentially according to backbone node order (first all leaves of the first backbone node, then all leaves of the second backbone node, and so on).

3. **Hidden Periodic Pattern**:
   - The number of leaves attached to each backbone node repeats with an unknown period q (q greater than or equal to 1).
   - There exists a base sequence of length q, and the leaf counts of backbone nodes repeat periodically according to this sequence.

Your goal is to infer the complete tree structure pattern by querying node degrees (the number of edges connected to a node), and provide a prediction rule.

## Available Operations

You can repeatedly perform the following operations:

1. **Degree Query**: Ask for the degree of a node with a specific ID. Format:
   <query_degree>ID</query_degree>
   For example, to query the degree of node 5:
   <query_degree>5</query_degree>

2. **Submit Prediction Rule**: When you believe you have inferred the pattern, submit your prediction rule. Format:
   <answer>p=modulus_value, r0=remainder_value, q=period_value, pattern=leaf_count_sequence</answer>
   
   Where:
   - p: modulus for ID-to-backbone mapping
   - r0: remainder for ID-to-backbone mapping
   - q: period length of leaf counts
   - pattern: sequence of leaf counts of length q, comma-separated
   
   Example:
   <answer>p=3, r0=1, q=2, pattern=1,2</answer>

## Evaluation

- You can make up to {max_queries} degree queries.
- After submitting your prediction rule, the system will test it on {test_samples} IDs that have not been queried.
- The game succeeds only if all predicted degrees for the test IDs are correct.
- The game fails if you exceed the maximum number of queries without submitting an answer, or if your prediction rule is incorrect.

## Notes

- Endpoint nodes of the backbone path have degree 1 less than middle backbone nodes (as endpoints connect to only one backbone neighbor).
- All leaf nodes have degree 1.
- Try to use as few queries as possible to infer the pattern.
"""

    contextualized_rule_zh_1 = """\
智慧城市交通规划局正在分析一个"隐藏的路网结构"，规则如下：

该城市的路网形成了一棵特殊的树状拓扑结构，共有 {n} 个交通路口，编号为 1 到 {n}。路网具有以下隐藏性质：

1. **路网结构**：整个路网由一条"主干道"和若干"社区支路"组成。主干道是一条由路口组成的骨干路径，主干道上的每个路口都可以连接若干个仅有一个出口的社区支路端点（叶子节点）。

2. **隐藏的编号规划规则**：
   - 存在一个未知的模数 p（p 大于等于 2）和一个未知的余数 r0（0 小于等于 r0 小于 p）。
   - 所有编号中，满足"编号除以 p 余 r0"的路口，按从小到大的顺序依次组成主干道。
   - 其余编号则对应社区支路的端点，按照主干道路口的顺序依次分配（先分配第一个主干道路口的所有支路端点，再分配第二个，以此类推）。

3. **隐藏的周期性规律**：
   - 每个主干道路口连接的社区支路数量按照一个未知的周期 q（q 大于等于 1）重复。
   - 存在一个长度为 q 的基础序列，主干道路口连接的支路数按此序列周期性重复。

你的目标是通过询问路口的连通道路数（即度数），推断出完整的路网结构规律，并给出一个预测规则。

## 可用操作

你可以反复进行以下操作：

1. **连通数查询**：询问某个编号路口的连通道路数。格式如下：
   <query_degree>路口编号</query_degree>
   例如，查询编号 5 的路口连通数：
   <query_degree>5</query_degree>

2. **提交预测规则**：当你认为已经推断出路网规划规律后，提交你的预测规则。格式如下：
   <answer>p=模数值, r0=余数值, q=周期值, pattern=支路数序列</answer>
   
   其中：
   - p：编号到主干道的模数
   - r0：编号到主干道的余数
   - q：支路数量的周期长度
   - pattern：长度为 q 的支路数量序列，用逗号分隔
   
   例如：
   <answer>p=3, r0=1, q=2, pattern=1,2</answer>

## 评估说明

- 你最多可以进行 {max_queries} 次连通数查询。
- 提交预测规则后，系统会在 {test_samples} 个未被查询过的路口上测试你的规则。
- 只有当所有测试路口的预测连通数都正确时，任务才算成功。
- 如果超过最大查询次数未提交答案，或预测规则错误，任务失败。

## 提示

- 主干道两端的路口连通数会比中间主干道路口少 1（因为两端点只连接一个主干道邻居）。
- 所有社区支路端点的连通数都是 1。
- 请尽可能少地使用查询次数来推断规律。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The Smart City Traffic Planning Bureau is analyzing a "Hidden Road Network Structure". The rules are as follows:

The city's road network forms a special tree-like topology with {n} traffic intersections, numbered from 1 to {n}. The network has the following hidden properties:

1. **Network Structure**: The network consists of a "main avenue" and several "community branch endpoints". The main avenue is a backbone sequence of intersections. Each intersection on the main avenue can connect to several community branch endpoints (leaf nodes with only one exit).

2. **Hidden Numbering Rule**:
   - There exists an unknown modulus p (p >= 2) and an unknown remainder r0 (0 <= r0 < p).
   - Intersections with IDs satisfying "ID modulo p equals r0" form the main avenue in ascending order.
   - The remaining IDs correspond to community branch endpoints, allocated sequentially according to the order of intersections on the main avenue.

3. **Hidden Periodic Pattern**:
   - The number of branches attached to each main avenue intersection repeats with an unknown period q (q >= 1).
   - There exists a base sequence of length q, and the branch counts repeat periodically according to this sequence.

Your goal is to infer the complete road network pattern by querying the number of connected roads (i.e., the degree) of intersections, and provide a prediction rule.

## Available Operations

You can repeatedly perform the following operations:

1. **Connection Query**: Ask for the number of connected roads for a specific intersection ID. Format:
   <query_degree>Intersection ID</query_degree>
   For example, to query the connections of intersection 5:
   <query_degree>5</query_degree>

2. **Submit Prediction Rule**: When you believe you have inferred the pattern, submit your prediction rule. Format:
   <answer>p=modulus_value, r0=remainder_value, q=period_value, pattern=branch_count_sequence</answer>
   
   Where:
   - p: modulus for ID-to-main-avenue mapping
   - r0: remainder for ID-to-main-avenue mapping
   - q: period length of branch counts
   - pattern: sequence of branch counts of length q, comma-separated
   
   Example:
   <answer>p=3, r0=1, q=2, pattern=1,2</answer>

## Evaluation

- You can make up to {max_queries} connection queries.
- After submitting your prediction rule, the system will test it on {test_samples} IDs that have not been queried.
- The task succeeds only if all predicted connections for the test IDs are correct.
- The task fails if you exceed the maximum number of queries without submitting an answer, or if your prediction rule is incorrect.

## Notes

- Endpoint intersections of the main avenue have 1 less connection than middle intersections (as endpoints connect to only one main avenue neighbor).
- All community branch endpoints have exactly 1 connection.
- Try to use as few queries as possible to infer the pattern.
"""

    contextualized_rule_zh_2 = """\
疾控中心正在追踪一个"隐藏的疾病传播接触链"，规则如下：

该次疫情的接触网络形成了一棵特殊的树状拓扑结构，共有 {n} 名接触者（节点），编号为 1 到 {n}。传播链具有以下隐藏性质：

1. **网络结构**：整个网络由一条"核心传播链"和若干"偶发感染者"组成。核心传播链是一条由高危接触者组成的骨干路径，链上的每个人都可以直接传染给若干个偶发感染者（叶子节点，且不再往下传播）。

2. **隐藏的编号映射规则**：
   - 存在一个未知的模数 p（p 大于等于 2）和一个未知的余数 r0（0 小于等于 r0 小于 p）。
   - 所有编号中，满足"编号除以 p 余 r0"的接触者，按从小到大的顺序依次组成核心传播链。
   - 其余编号则对应偶发感染者，按照核心传播链的顺序依次分配（先分配第一个核心接触者的所有偶发感染者，以此类推）。

3. **隐藏的周期性规律**：
   - 每个核心接触者直接传染的偶发感染者数量按照一个未知的周期 q（q 大于等于 1）重复。
   - 存在一个长度为 q 的基础序列，核心接触者的传染数按此序列周期性重复。

你的目标是通过询问某个人的直接接触人数（即度数），推断出完整的接触链规律，并给出一个预测规则。

## 可用操作

你可以反复进行以下操作：

1. **接触人数查询**：询问某个编号的接触者的直接接触人数。格式如下：
   <query_degree>接触者编号</query_degree>
   例如，查询编号 5 的接触人数：
   <query_degree>5</query_degree>

2. **提交预测规则**：当你认为已经推断出传播链规律后，提交你的预测规则。格式如下：
   <answer>p=模数值, r0=余数值, q=周期值, pattern=传染数序列</answer>
   
   其中：
   - p：编号到核心传播链的模数
   - r0：编号到核心传播链的余数
   - q：偶发感染者数量的周期长度
   - pattern：长度为 q 的偶发感染者传染数序列，用逗号分隔
   
   例如：
   <answer>p=3, r0=1, q=2, pattern=1,2</answer>

## 评估说明

- 你最多可以进行 {max_queries} 次接触人数查询。
- 提交预测规则后，系统会在 {test_samples} 个未被查询过的接触者上测试你的规则。
- 只有当所有测试者的预测接触人数都正确时，任务才算成功。
- 如果超过最大查询次数未提交答案，或预测规则错误，任务失败。

## 提示

- 核心传播链两端的人员直接接触人数会比中间节点少 1（因为两端点只连接一个核心邻居）。
- 所有偶发感染者的接触人数都是 1。
- 请尽可能少地使用查询次数来推断规律。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
The CDC is tracking a "Hidden Disease Transmission Contact Chain". The rules are as follows:

The contact network of this outbreak forms a special tree-like topology with {n} contacts (nodes), numbered from 1 to {n}. The transmission chain has the following hidden properties:

1. **Network Structure**: The entire network consists of a "core transmission chain" and several "sporadic cases". The core transmission chain is a backbone sequence of high-risk contacts, and each person on the chain can directly infect several sporadic cases (leaf nodes, who do not transmit further).

2. **Hidden Numbering Rule**:
   - There exists an unknown modulus p (p >= 2) and an unknown remainder r0 (0 <= r0 < p).
   - Contacts with IDs satisfying "ID modulo p equals r0" form the core transmission chain in ascending order.
   - The remaining IDs correspond to sporadic cases, allocated sequentially according to the order of core contacts.

3. **Hidden Periodic Pattern**:
   - The number of sporadic cases directly infected by each core contact repeats with an unknown period q (q >= 1).
   - There exists a base sequence of length q, and the infection counts repeat periodically according to this sequence.

Your goal is to infer the complete transmission chain pattern by querying a person's direct contact count (i.e., the degree), and provide a prediction rule.

## Available Operations

You can repeatedly perform the following operations:

1. **Contact Count Query**: Ask for the direct contact count of a specific contact ID. Format:
   <query_degree>Contact ID</query_degree>
   For example, to query the contact count of person 5:
   <query_degree>5</query_degree>

2. **Submit Prediction Rule**: When you believe you have inferred the transmission chain pattern, submit your prediction rule. Format:
   <answer>p=modulus_value, r0=remainder_value, q=period_value, pattern=infection_count_sequence</answer>
   
   Where:
   - p: modulus for ID-to-core-chain mapping
   - r0: remainder for ID-to-core-chain mapping
   - q: period length of sporadic case counts
   - pattern: sequence of sporadic case counts of length q, comma-separated
   
   Example:
   <answer>p=3, r0=1, q=2, pattern=1,2</answer>

## Evaluation

- You can make up to {max_queries} contact count queries.
- After submitting your prediction rule, the system will test it on {test_samples} IDs that have not been queried.
- The task succeeds only if all predicted contact counts for the test IDs are correct.
- The task fails if you exceed the maximum number of queries without submitting an answer, or if your prediction rule is incorrect.

## Notes

- Endpoint persons on the core transmission chain have 1 less direct contact than middle core nodes (as endpoints connect to only one core neighbor).
- All sporadic cases have exactly 1 contact count.
- Try to use as few queries as possible to infer the pattern.
"""

    contextualized_rule_zh_3 = """\
教务处正在构建一个"隐藏的课程前置依赖图谱"，规则如下：

某专业的知识点拓扑形成了一棵特殊的树状结构，共有 {n} 个知识模块，编号为 1 到 {n}。该图谱具有以下隐藏性质：

1. **图谱结构**：图谱由一条"核心必修主干"和若干"选修拓展模块"组成。必修主干是一条前后相继的知识序列，主干上的每个模块可以外挂若干个独立的选修拓展模块（叶子节点）。

2. **隐藏的编号分配规则**：
   - 存在一个未知的模数 p（p 大于等于 2）和一个未知的余数 r0（0 小于等于 r0 小于 p）。
   - 所有编号中，满足"编号除以 p 余 r0"的知识模块，按从小到大的顺序依次组成核心必修主干。
   - 其余编号则对应选修拓展模块，按照必修主干模块的顺序依次分配（先分配第一个必修模块的所有拓展模块，以此类推）。

3. **隐藏的周期性规律**：
   - 每个必修模块挂载的选修拓展模块数量按照一个未知的周期 q（q 大于等于 1）重复。
   - 存在一个长度为 q 的基础序列，必修模块的拓展数按此序列周期性重复。

你的目标是通过询问知识模块的前置/后续依赖总数（即图中的度数），推断出完整的课程图谱规律，并给出一个预测规则。

## 可用操作

你可以反复进行以下操作：

1. **依赖数查询**：询问某个编号模块的总依赖数。格式如下：
   <query_degree>模块编号</query_degree>
   例如，查询编号 5 的依赖数：
   <query_degree>5</query_degree>

2. **提交预测规则**：当你认为已经推断出课程图谱规律后，提交你的预测规则。格式如下：
   <answer>p=模数值, r0=余数值, q=周期值, pattern=拓展模块数序列</answer>
   
   其中：
   - p：编号到核心必修主干的模数
   - r0：编号到核心必修主干的余数
   - q：拓展模块数量的周期长度
   - pattern：长度为 q 的拓展模块数量序列，用逗号分隔
   
   例如：
   <answer>p=3, r0=1, q=2, pattern=1,2</answer>

## 评估说明

- 你最多可以进行 {max_queries} 次依赖数查询。
- 提交预测规则后，系统会在 {test_samples} 个未被查询过的模块上测试你的规则。
- 只有当所有测试模块的预测依赖数都正确时，任务才算成功。
- 如果超过最大查询次数未提交答案，或预测规则错误，任务失败。

## 提示

- 核心必修主干两端的模块依赖数会比中间模块少 1（因为两端点只连接一个主干邻居）。
- 所有选修拓展模块的依赖数都是 1。
- 请尽可能少地使用查询次数来推断规律。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The Academic Affairs Office is constructing a "Hidden Course Prerequisite Dependency Graph". The rules are as follows:

The knowledge topology of a major forms a special tree-like structure with {n} knowledge modules, numbered from 1 to {n}. The graph has the following hidden properties:

1. **Graph Structure**: The graph consists of a "core compulsory backbone" and several "elective expansion modules". The compulsory backbone is a sequential knowledge path, and each module on the backbone can attach several independent elective expansion modules (leaf nodes).

2. **Hidden Numbering Rule**:
   - There exists an unknown modulus p (p >= 2) and an unknown remainder r0 (0 <= r0 < p).
   - Modules with IDs satisfying "ID modulo p equals r0" form the core compulsory backbone in ascending order.
   - The remaining IDs correspond to elective expansion modules, allocated sequentially according to the order of compulsory backbone modules.

3. **Hidden Periodic Pattern**:
   - The number of expansion modules attached to each compulsory module repeats with an unknown period q (q >= 1).
   - There exists a base sequence of length q, and the expansion counts repeat periodically according to this sequence.

Your goal is to infer the complete course graph pattern by querying a module's total number of prerequisite/subsequent dependencies (i.e., the degree), and provide a prediction rule.

## Available Operations

You can repeatedly perform the following operations:

1. **Dependency Count Query**: Ask for the total dependency count of a specific module ID. Format:
   <query_degree>Module ID</query_degree>
   For example, to query the dependency count of module 5:
   <query_degree>5</query_degree>

2. **Submit Prediction Rule**: When you believe you have inferred the course graph pattern, submit your prediction rule. Format:
   <answer>p=modulus_value, r0=remainder_value, q=period_value, pattern=expansion_module_count_sequence</answer>
   
   Where:
   - p: modulus for ID-to-compulsory-backbone mapping
   - r0: remainder for ID-to-compulsory-backbone mapping
   - q: period length of expansion module counts
   - pattern: sequence of expansion module counts of length q, comma-separated
   
   Example:
   <answer>p=3, r0=1, q=2, pattern=1,2</answer>

## Evaluation

- You can make up to {max_queries} dependency queries.
- After submitting your prediction rule, the system will test it on {test_samples} IDs that have not been queried.
- The task succeeds only if all predicted dependencies for the test IDs are correct.
- The task fails if you exceed the maximum number of queries without submitting an answer, or if your prediction rule is incorrect.

## Notes

- Endpoint modules on the core compulsory backbone have 1 less dependency than middle backbone modules (as endpoints connect to only one backbone neighbor).
- All elective expansion modules have exactly 1 dependency.
- Try to use as few queries as possible to infer the pattern.
"""

    contextualized_rule_zh_4 = """\
智能制造工厂正在调试一条"隐藏的装配流水线"，规则如下：

该装配网络形成了一棵特殊的树状拓扑结构，共有 {n} 个加工工位，编号为 1 到 {n}。该流水线具有以下隐藏性质：

1. **网络结构**：流水线由一条"主装配线"和若干"预处理工位"组成。主装配线是一条工位序列，线上的每个工位可以连接若干个独立的预处理工位（叶子节点）。

2. **隐藏的编号规划规则**：
   - 存在一个未知的模数 p（p 大于等于 2）和一个未知的余数 r0（0 小于等于 r0 小于 p）。
   - 所有编号中，满足"编号除以 p 余 r0"的工位，按从小到大的顺序依次组成主装配线。
   - 其余编号则对应预处理工位，按照主装配线工位的顺序依次分配。

3. **隐藏的周期性规律**：
   - 每个主装配线工位连接的预处理工位数量按照一个未知的周期 q（q 大于等于 1）重复。
   - 存在一个长度为 q 的基础序列，主装配线工位的连接数按此序列周期性重复。

你的目标是通过询问某个工位的传送带物理连接总数（即度数），推断出完整的装配线设计规律，并给出一个预测规则。

## 可用操作

你可以反复进行以下操作：

1. **连接数查询**：询问某个编号工位的传送带连接总数。格式如下：
   <query_degree>工位编号</query_degree>
   例如，查询编号 5 的连接数：
   <query_degree>5</query_degree>

2. **提交预测规则**：当你认为已经推断出装配线设计规律后，提交你的预测规则。格式如下：
   <answer>p=模数值, r0=余数值, q=周期值, pattern=预处理工位数序列</answer>
   
   其中：
   - p：编号到主装配线的模数
   - r0：编号到主装配线的余数
   - q：预处理工位数量的周期长度
   - pattern：长度为 q 的预处理工位数量序列，用逗号分隔
   
   例如：
   <answer>p=3, r0=1, q=2, pattern=1,2</answer>

## 评估说明

- 你最多可以进行 {max_queries} 次连接数查询。
- 提交预测规则后，系统会在 {test_samples} 个未被查询过的工位上测试你的规则。
- 只有当所有测试工位的预测连接数都正确时，任务才算成功。
- 如果超过最大查询次数未提交答案，或预测规则错误，任务失败。

## 提示

- 主装配线两端的工位连接数会比中间工位少 1（因为两端点只连接一个主装配线邻居）。
- 所有预处理工位的连接数都是 1。
- 请尽可能少地使用查询次数来推断规律。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
A smart manufacturing factory is debugging a "Hidden Assembly Line Network". The rules are as follows:

The assembly network forms a special tree-like topology with {n} processing stations, numbered from 1 to {n}. The assembly line has the following hidden properties:

1. **Network Structure**: The line consists of a "main assembly line" and several "pre-processing stations". The main assembly line is a sequence of stations, and each station on the line can connect to several independent pre-processing stations (leaf nodes).

2. **Hidden Numbering Rule**:
   - There exists an unknown modulus p (p >= 2) and an unknown remainder r0 (0 <= r0 < p).
   - Stations with IDs satisfying "ID modulo p equals r0" form the main assembly line in ascending order.
   - The remaining IDs correspond to pre-processing stations, allocated sequentially according to the order of main assembly line stations.

3. **Hidden Periodic Pattern**:
   - The number of pre-processing stations connected to each main assembly station repeats with an unknown period q (q >= 1).
   - There exists a base sequence of length q, and the connection counts repeat periodically according to this sequence.

Your goal is to infer the complete assembly line design pattern by querying a station's total conveyor physical connections (i.e., the degree), and provide a prediction rule.

## Available Operations

You can repeatedly perform the following operations:

1. **Connection Query**: Ask for the total conveyor connections of a specific station ID. Format:
   <query_degree>Station ID</query_degree>
   For example, to query the connections of station 5:
   <query_degree>5</query_degree>

2. **Submit Prediction Rule**: When you believe you have inferred the assembly line design pattern, submit your prediction rule. Format:
   <answer>p=modulus_value, r0=remainder_value, q=period_value, pattern=pre_processing_station_count_sequence</answer>
   
   Where:
   - p: modulus for ID-to-main-assembly-line mapping
   - r0: remainder for ID-to-main-assembly-line mapping
   - q: period length of pre-processing station counts
   - pattern: sequence of pre-processing station counts of length q, comma-separated
   
   Example:
   <answer>p=3, r0=1, q=2, pattern=1,2</answer>

## Evaluation

- You can make up to {max_queries} connection queries.
- After submitting your prediction rule, the system will test it on {test_samples} IDs that have not been queried.
- The task succeeds only if all predicted connection counts for the test IDs are correct.
- The task fails if you exceed the maximum number of queries without submitting an answer, or if your prediction rule is incorrect.

## Notes

- Endpoint stations of the main assembly line have 1 less connection than middle stations (as endpoints connect to only one main assembly line neighbor).
- All pre-processing stations have exactly 1 connection.
- Try to use as few queries as possible to infer the pattern.
"""

    contextualized_rule_zh_5 = """\
商业合规调查局正在穿透一个"隐藏的公司控制权网络"，规则如下：

该控制权网络形成了一棵特殊的树状拓扑结构，共有 {n} 个法律实体（公司），编号为 1 到 {n}。网络具有以下隐藏性质：

1. **网络结构**：网络由一条"核心控股链"和若干"外围壳公司"组成。核心控股链是一条由层层控制的核心平台组成的序列，每个核心平台可以横向控制若干个独立的壳公司（叶子节点）。

2. **隐藏的编号映射规则**：
   - 存在一个未知的模数 p（p 大于等于 2）和一个未知的余数 r0（0 小于等于 r0 小于 p）。
   - 所有编号中，满足"编号除以 p 余 r0"的实体，按从小到大的顺序依次组成核心控股链。
   - 其余编号则对应壳公司，按照控股链核心平台的顺序依次分配。

3. **隐藏的周期性规律**：
   - 每个核心平台控制的壳公司数量按照一个未知的周期 q（q 大于等于 1）重复。
   - 存在一个长度为 q 的基础序列，核心平台控制的壳公司数按此序列周期性重复。

你的目标是通过询问某个法律实体的直接关联企业总数（即控制与被控制的边数度数），推断出完整的控制网络规律，并给出一个预测规则。

## 可用操作

你可以反复进行以下操作：

1. **关联企业数查询**：询问某个编号实体的直接关联企业数。格式如下：
   <query_degree>实体编号</query_degree>
   例如，查询编号 5 的实体关联数：
   <query_degree>5</query_degree>

2. **提交预测规则**：当你认为已经推断出控制网络规律后，提交你的预测规则。格式如下：
   <answer>p=模数值, r0=余数值, q=周期值, pattern=壳公司数量序列</answer>
   
   其中：
   - p：编号到核心控股链的模数
   - r0：编号到核心控股链的余数
   - q：壳公司数量的周期长度
   - pattern：长度为 q 的壳公司数量序列，用逗号分隔
   
   例如：
   <answer>p=3, r0=1, q=2, pattern=1,2</answer>

## 评估说明

- 你最多可以进行 {max_queries} 次关联企业数查询。
- 提交预测规则后，系统会在 {test_samples} 个未被查询过的实体上测试你的规则。
- 只有当所有测试实体的预测关联企业数都正确时，任务才算成功。
- 如果超过最大查询次数未提交答案，或预测规则错误，任务失败。

## 提示

- 核心控股链两端的平台关联企业数会比中间平台少 1（因为两端点只连接一个核心平台邻居）。
- 所有壳公司的关联企业数都是 1。
- 请尽可能少地使用查询次数来推断规律。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
The Commercial Compliance Bureau is penetrating a "Hidden Corporate Control Network". The rules are as follows:

The control network forms a special tree-like topology with {n} legal entities (companies), numbered from 1 to {n}. The network has the following hidden properties:

1. **Network Structure**: The network consists of a "core holding chain" and several "peripheral shell companies". The core holding chain is a sequence of core platforms with cascading control. Each core platform can laterally control several independent shell companies (leaf nodes).

2. **Hidden Numbering Rule**:
   - There exists an unknown modulus p (p >= 2) and an unknown remainder r0 (0 <= r0 < p).
   - Entities with IDs satisfying "ID modulo p equals r0" form the core holding chain in ascending order.
   - The remaining IDs correspond to shell companies, allocated sequentially according to the order of core platforms on the holding chain.

3. **Hidden Periodic Pattern**:
   - The number of shell companies controlled by each core platform repeats with an unknown period q (q >= 1).
   - There exists a base sequence of length q, and the shell company counts repeat periodically according to this sequence.

Your goal is to infer the complete control network pattern by querying an entity's total direct associated entities (i.e., the degree of control edges), and provide a prediction rule.

## Available Operations

You can repeatedly perform the following operations:

1. **Associated Entities Query**: Ask for the number of direct associated entities for a specific entity ID. Format:
   <query_degree>Entity ID</query_degree>
   For example, to query the associated entities of entity 5:
   <query_degree>5</query_degree>

2. **Submit Prediction Rule**: When you believe you have inferred the control network pattern, submit your prediction rule. Format:
   <answer>p=modulus_value, r0=remainder_value, q=period_value, pattern=shell_company_count_sequence</answer>
   
   Where:
   - p: modulus for ID-to-core-holding-chain mapping
   - r0: remainder for ID-to-core-holding-chain mapping
   - q: period length of shell company counts
   - pattern: sequence of shell company counts of length q, comma-separated
   
   Example:
   <answer>p=3, r0=1, q=2, pattern=1,2</answer>

## Evaluation

- You can make up to {max_queries} associated entities queries.
- After submitting your prediction rule, the system will test it on {test_samples} IDs that have not been queried.
- The task succeeds only if all predicted associated entities for the test IDs are correct.
- The task fails if you exceed the maximum number of queries without submitting an answer, or if your prediction rule is incorrect.

## Notes

- Endpoint platforms of the core holding chain have 1 less associated entity than middle platforms (as endpoints connect to only one core platform neighbor).
- All shell companies have exactly 1 associated entity.
- Try to use as few queries as possible to infer the pattern.
"""

    tags = ["answer", "query_degree"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 10,
                "p": 2,
                "r0": 1,
                "q": 1,
                "pattern": [1],
                "max_queries": 20,
                "test_samples": 5,
            },
            2: {
                "n": 14,
                "p": 3,
                "r0": 1,
                "q": 2,
                "pattern": [1, 3],
                "max_queries": 25,
                "test_samples": 6,
            },
            3: {
                "n": 19,
                "p": 4,
                "r0": 1,
                "q": 2,
                "pattern": [2, 4],
                "max_queries": 30,
                "test_samples": 8,
            },
            4: {
                "n": 24,
                "p": 4,
                "r0": 0,
                "q": 3,
                "pattern": [2, 3, 4],
                "max_queries": 35,
                "test_samples": 10,
            },
            5: {
                "n": 30,
                "p": 5,
                "r0": 2,
                "q": 3,
                "pattern": [3, 4, 5],
                "max_queries": 40,
                "test_samples": 12,
            },
        },
        "en": {
            1: {
                "n": 10,
                "p": 2,
                "r0": 1,
                "q": 1,
                "pattern": [1],
                "max_queries": 20,
                "test_samples": 5,
            },
            2: {
                "n": 14,
                "p": 3,
                "r0": 1,
                "q": 2,
                "pattern": [1, 3],
                "max_queries": 25,
                "test_samples": 6,
            },
            3: {
                "n": 19,
                "p": 4,
                "r0": 1,
                "q": 2,
                "pattern": [2, 4],
                "max_queries": 30,
                "test_samples": 8,
            },
            4: {
                "n": 24,
                "p": 4,
                "r0": 0,
                "q": 3,
                "pattern": [2, 3, 4],
                "max_queries": 35,
                "test_samples": 10,
            },
            5: {
                "n": 30,
                "p": 5,
                "r0": 2,
                "q": 3,
                "pattern": [3, 4, 5],
                "max_queries": 40,
                "test_samples": 12,
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0
        self.queried_ids = set()
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：构建隐藏的树结构"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.n = cfg["n"]
        self.p = cfg["p"]
        self.r0 = cfg["r0"]
        self.q = cfg["q"]
        self.pattern = cfg["pattern"]
        self.max_queries = cfg["max_queries"]
        self.test_samples = cfg["test_samples"]

        self._game_info = {
            "n": self.n,
            "max_queries": self.max_queries,
            "test_samples": self.test_samples,
        }

        self._build_tree_structure()

    def _build_tree_structure(self):
        """根据参数构建树的度数映射"""
        backbone_ids = []
        for i in range(1, self.n + 1):
            if i % self.p == self.r0:
                backbone_ids.append(i)
        
        self.backbone_ids = backbone_ids
        self.m = len(backbone_ids)
        
        self.backbone_leaf_counts = []
        for j in range(self.m):
            pattern_idx = j % self.q
            leaf_count = self.pattern[pattern_idx]
            self.backbone_leaf_counts.append(leaf_count)
        
        self.id_to_degree = {}
        
        for j in range(self.m):
            node_id = backbone_ids[j]
            leaf_count = self.backbone_leaf_counts[j]
            
            if j == 0:
                degree = 1 + leaf_count
            elif j == self.m - 1:
                degree = 1 + leaf_count
            else:
                degree = 2 + leaf_count
            
            self.id_to_degree[node_id] = degree
        
        leaf_ids = []
        for i in range(1, self.n + 1):
            if i not in backbone_ids:
                leaf_ids.append(i)
        
        for leaf_id in leaf_ids:
            self.id_to_degree[leaf_id] = 1

    def _compute_degree(self, node_id):
        """计算给定编号的节点度数"""
        if node_id < 1 or node_id > self.n:
            return None
        return self.id_to_degree.get(node_id, None)

    def _predict_degree_from_rule(self, node_id, p, r0, q, pattern):
        """根据给定的规则预测节点度数"""
        if node_id % p == r0:
            backbone_ids = [i for i in range(1, self.n + 1) if i % p == r0]
            backbone_ids.sort()
            
            if node_id not in backbone_ids:
                return None
            
            j = backbone_ids.index(node_id)
            m = len(backbone_ids)
            
            pattern_idx = j % q
            if pattern_idx >= len(pattern):
                return None
            leaf_count = pattern[pattern_idx]
            
            if j == 0:
                degree = 1 + leaf_count
            elif j == m - 1:
                degree = 1 + leaf_count
            else:
                degree = 2 + leaf_count
            
            return degree
        else:
            return 1

    def evaluate(self, parsed_info):
        """评估提交的预测规则"""
        try:
            raw_ans = parsed_info["answer"]
            kv_pairs = [x.strip() for x in raw_ans.split(",")]
            
            ans_dict = {}
            current_key = None
            current_value = []
            
            for kv in kv_pairs:
                if "=" in kv:
                    if current_key is not None:
                        ans_dict[current_key] = ",".join(current_value).strip()
                    
                    k, v = kv.split("=", 1)
                    current_key = k.strip()
                    current_value = [v.strip()]
                else:
                    if current_key is not None:
                        current_value.append(kv.strip())
            
            if current_key is not None:
                ans_dict[current_key] = ",".join(current_value).strip()
            
            if "p" not in ans_dict or "r0" not in ans_dict or "q" not in ans_dict or "pattern" not in ans_dict:
                return False
            
            pred_p = int(ans_dict["p"])
            pred_r0 = int(ans_dict["r0"])
            pred_q = int(ans_dict["q"])
            pred_pattern = [int(x.strip()) for x in ans_dict["pattern"].split(",") if x.strip()]
            
            unqueried_ids = [i for i in range(1, self.n + 1) if i not in self.queried_ids]
            
            if len(unqueried_ids) < self.test_samples:
                test_ids = random.sample(range(1, self.n + 1), min(self.test_samples, self.n))
            else:
                test_ids = random.sample(unqueried_ids, self.test_samples)
            
            all_correct = True
            for test_id in test_ids:
                true_degree = self._compute_degree(test_id)
                pred_degree = self._predict_degree_from_rule(test_id, pred_p, pred_r0, pred_q, pred_pattern)
                
                if true_degree != pred_degree:
                    all_correct = False
                    break
            
            return all_correct
            
        except Exception as e:
            return False

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑"""
        if "query_degree" in parsed_info:
            if self.query_count >= self.max_queries:
                if self.config.language == "zh":
                    raise ValueError(f"已超过最大查询次数 {self.max_queries}")
                else:
                    raise ValueError(f"Maximum query limit {self.max_queries} exceeded")
            
            try:
                node_id = int(parsed_info["query_degree"].strip())
            except:
                if self.config.language == "zh":
                    return "错误：编号格式无效。"
                else:
                    return "Error: Invalid ID format."
            
            if node_id < 1 or node_id > self.n:
                if self.config.language == "zh":
                    return f"错误：编号必须在 1 到 {self.n} 之间。"
                else:
                    return f"Error: ID must be between 1 and {self.n}."
            
            self.query_count += 1
            self.queried_ids.add(node_id)
            
            degree = self._compute_degree(node_id)
            return str(degree)
        else:
            if self.config.language == "zh":
                raise ValueError("无效的查询标签。")
            else:
                raise ValueError("Invalid query tag.")

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        queries = []
        for i in range(1, self.n + 1):
            query_content = str(i)
            degree = self._compute_degree(i)
            answer_content = str(degree)
            
            queries.append({
                "query": query_content,
                "answer": answer_content
            })
        return queries

    def _cf_make_wrong(self, correct):
        """生成错误答案"""
        if correct.isdigit():
            return str(int(correct) + 1)
        
        lower_correct = correct.lower()
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        else:
            if "yes" in lower_correct:
                return correct.replace("Yes", "No").replace("yes", "no")
            if "no" in lower_correct:
                return correct.replace("No", "Yes").replace("no", "yes")
        
        return correct + "_WRONG"