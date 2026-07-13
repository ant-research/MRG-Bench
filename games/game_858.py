# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   前序遍历顺序：某节点在前序遍历中是第几个被访问
# ============================================================

import re
import itertools
from typing import List, Dict, Set, Tuple
from .base import Game


class TreeTraversalOrderGame(Game):
    """
    树前序遍历顺序推理游戏
    
    玩家需要通过询问兄弟节点的先后顺序，推断出目标节点在前序遍历中的访问序号。
    """

    game_rule_zh = """\
我们来玩一个"树遍历顺序推理"游戏，规则如下：

游戏设定了一棵固定的有根树 T，共有 {n} 个节点，根节点为 R。每个节点都有一个长度为 3 的符号串标签，符号取自集合 {{★, ◆, ●}}。

隐藏机制：存在一个对这三个符号的严格全序（优先级顺序），该顺序未知但全局一致。在每个父节点处，其孩子按各自标签在该全序下的字典序排序；整棵树按该孩子顺序进行前序遍历（访问父节点后，依序递归访问各子树）。

已知信息：
- 树结构（无序的孩子集合）：{tree_structure}
- 节点标签：{node_labels}
- 各子树大小（含自身）：{subtree_sizes}

你的目标是推断出节点 {target_node} 在整棵树前序遍历中的访问序号（1 到 {n} 之间的整数）。

你可以反复提问，每次询问只能包含一个问题：

兄弟先后比较：在父节点 P 处，询问其两个不同的直接孩子 X 与 Y 中，哪一个对应的子树在前序中先被访问。
- 约束：X、Y 必须是同一父节点 P 的直接孩子，且 X 不等于 Y。

## 询问与提交答案的格式（必须严格遵守）

询问兄弟先后顺序（例如询问父节点 R 的孩子 A 和 B）：
<query>R,A,B</query>

提交最终答案时，给出目标节点的访问序号（1 到 {n} 的整数）：
<answer>5</answer>

注意：请尽可能用最少的询问次数完成推理。
"""

    game_rule_en = """\
Let's play a "Tree Traversal Order Deduction" game. Here are the rules:

The game features a fixed rooted tree T with {n} nodes, where the root is R. Each node has a label consisting of a 3-symbol string, with symbols from the set {{★, ◆, ●}}.

Hidden mechanism: There exists a strict total order (priority ranking) over these three symbols, which is unknown but globally consistent. At each parent node, its children are sorted by the lexicographic order of their labels under this hidden order; the entire tree is traversed in preorder (visiting the parent node first, then recursively visiting each subtree in order).

Known information:
- Tree structure (unordered child sets): {tree_structure}
- Node labels: {node_labels}
- Subtree sizes (including self): {subtree_sizes}

Your goal is to infer the preorder visit number of node {target_node} in the entire tree (an integer between 1 and {n}).

You can repeatedly ask questions, with one question per query:

Sibling ordering comparison: At parent node P, ask which of its two distinct direct children X and Y has its subtree visited first in preorder.
- Constraint: X and Y must be direct children of the same parent node P, and X must not equal Y.

## Query and Answer Format (must strictly follow)

Query sibling order (e.g., asking about children A and B of parent R):
<query>R,A,B</query>

Submit final answer by providing the visit number of the target node (an integer from 1 to {n}):
<answer>5</answer>

Note: Please complete the deduction with as few queries as possible.
"""

    contextualized_rule_zh_1 = """\
欢迎使用“城市路网监控节点排查系统”。我们需要确定特定监控节点的巡查顺序。

当前系统包含一个层级路网树 T，共有 {n} 个监控节点，总控中心（根节点）为 R。每个节点都有一个长度为 3 的风险评估标记串，符号取自集合 {{★, ◆, ●}}。

隐藏排查机制：针对这些风险符号存在一个未知的、全局一致的严重程度优先级全序。在每一级路口（父节点）处，通向的各个下级路段（孩子节点）将严格依据其标记串在该优先级下的字典序进行排序；排查车队会按照整棵树的前序遍历顺序进行巡查（先巡查父节点路口，再依序深入巡查各分支子树的节点）。

已知系统参数：
- 路网树层级结构（未排序的下级路口集合）：{tree_structure}
- 监控节点风险标记：{node_labels}
- 各分支子网节点总数（含该路口自身）：{subtree_sizes}

你的排查任务是推断出目标监控节点 {target_node} 是第几个被巡查的（1 到 {n} 之间的整数）。

你可以通过系统接口反复提交查询，每次查询只能包含一个请求：

下级路口巡查顺序比较：在指定的父节点 P 处，询问其直属的两个不同下级路段节点 X 与 Y，哪一个对应的分支子网会优先被巡查。
- 约束条件：X、Y 必须是同一父节点 P 的直接下级节点，且 X 不等于 Y。

## 查询与提交结果格式（必须严格遵守）

查询下级节点的巡查先后顺序（例如查询父节点 R 的下级节点 A 和 B）：
<query>R,A,B</query>

提交最终推断时，给出目标节点的巡查序号（1 到 {n} 的整数）：
<answer>5</answer>

注意：为了保证排查效率，请尽可能用最少的查询次数完成推算。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Road Network Monitoring Node Inspection System". We need to determine the inspection sequence for a specific monitoring node.

The system features a hierarchical road network tree T with {n} monitoring nodes, where the main control center (root node) is R. Each node has a 3-symbol risk assessment tag, with symbols drawn from the set {{★, ◆, ●}}.

Hidden Inspection Mechanism: There exists an unknown but globally consistent severity priority total order for these risk symbols. At each intersection (parent node), its connecting subordinate road segments (child nodes) are sorted by the lexicographic order of their tags under this priority ranking. The inspection fleet will then traverse the entire tree in a preorder sequence (inspecting the parent intersection first, then recursively patrolling each branch's subtree).

Known system parameters:
- Road network hierarchy (unordered sets of subordinate nodes): {tree_structure}
- Node risk tags: {node_labels}
- Total nodes in each branch subnetwork (including the node itself): {subtree_sizes}

Your inspection task is to deduce the exact inspection sequence number of the target monitoring node {target_node} (an integer between 1 and {n}).

You can repeatedly query the system interface, with one request per query:

Subordinate route inspection comparison: At a specified parent node P, ask which of its two distinct direct subordinate nodes X and Y will have its branch subnetwork inspected first.
- Constraint: X and Y must be direct subordinate nodes of the same parent node P, and X must not equal Y.

## Query and Submission Format (must strictly follow)

Query the inspection order of subordinate nodes (e.g., asking about nodes A and B under parent R):
<query>R,A,B</query>

Submit the final deduction by providing the inspection sequence number of the target node (an integer from 1 to {n}):
<answer>5</answer>

Note: To ensure inspection efficiency, please complete the deduction with as few queries as possible.
"""

    contextualized_rule_zh_2 = """\
欢迎进入“病毒变异株进化路径追踪系统”。本次任务需要推断特定变异株的测序归档顺位。

研究设定了一棵固定的病毒变异树 T，共有 {n} 个变异株节点，初始毒株（根节点）为 R。每个节点都有一个长度为 3 的基因突变位点序列标签，符号取自集合 {{★, ◆, ●}}。

隐藏表达机制：存在一个针对这三个突变位点符号的活性优先级全序，该顺序未知但全局一致。在每个父毒株节点处，其衍生的各个子毒株节点按各自标签在该活性优先级下的字典序进行排序；测序系统按该子毒株顺序对整棵进化树进行前序遍历（先测序父毒株，再依序递归测序各衍生分支的变异株）。

已知研究数据：
- 变异株层级结构（未排序的子毒株集合）：{tree_structure}
- 变异株突变标签：{node_labels}
- 各分支变异株总数（含当前毒株自身）：{subtree_sizes}

你的追踪目标是推断出目标变异株 {target_node} 在全局前序遍历测序中的确切顺位（1 到 {n} 之间的整数）。

你可以向数据库反复提问，每次提问只能包含一个问题：

衍生变异株测序先后比较：在父毒株 P 处，询问其衍生的两个不同直接子毒株 X 与 Y 中，哪一个对应的衍生分支先被测序。
- 约束：X、Y 必须是同一父毒株 P 的直接衍生节点，且 X 不等于 Y。

## 询问与提交答案的格式（必须严格遵守）

查询测序先后顺序（例如询问父毒株 R 的衍生株 A 和 B）：
<query>R,A,B</query>

提交最终结论时，给出目标变异株的测序顺位序号（1 到 {n} 的整数）：
<answer>5</answer>

注意：请尽可能用最少的提问次数完成推断，以节约计算资源。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Viral Mutant Strain Evolution Tracking System". This task requires you to infer the sequencing and archiving order of a specific mutant strain.

The research defines a fixed viral evolution tree T with {n} mutant strain nodes, starting from the initial strain (root node) R. Each node possesses a 3-symbol genetic mutation locus sequence tag, with symbols from the set {{★, ◆, ●}}.

Hidden Expression Mechanism: There is a strict total order of activity priority among these three mutation locus symbols, which is unknown but globally consistent. At each parent strain node, its derived direct child strains are sorted by the lexicographic order of their tags under this activity priority. The sequencing system then processes the entire evolutionary tree in a preorder traversal (sequencing the parent strain node first, then recursively sequencing each derived branch).

Known research data:
- Mutant strain hierarchy (unordered sets of child strains): {tree_structure}
- Strain mutation tags: {node_labels}
- Total strains in each branch (including the strain itself): {subtree_sizes}

Your tracking goal is to infer the exact preorder sequencing position of the target mutant strain {target_node} in the global sequencing process (an integer between 1 and {n}).

You can repeatedly query the database, with one question per query:

Derived strain sequencing comparison: At parent strain P, ask which of its two distinct direct child strains X and Y has its derived branch sequenced first.
- Constraint: X and Y must be direct child strains of the same parent strain P, and X must not equal Y.

## Query and Answer Format (must strictly follow)

Query the sequencing order (e.g., asking about child strains A and B derived from parent R):
<query>R,A,B</query>

Submit the final conclusion by providing the sequencing sequence number of the target strain (an integer from 1 to {n}):
<answer>5</answer>

Note: To save computational resources, please complete the inference with as few queries as possible.
"""

    contextualized_rule_zh_3 = """\
欢迎使用“知识图谱教学路径规划系统”。您的任务是推断特定知识点的排课顺序。

系统构建了一棵层级化的知识点依赖树 T，共有 {n} 个知识节点，基础核心概念（根节点）为 R。每个知识点都有一个长度为 3 的教学属性标签，符号取自集合 {{★, ◆, ●}}。

隐藏排课机制：针对这三种教学属性符号存在一个严格的教学优先级全序，该顺序未知但全局一致。在每个父级知识点处，其下属的子知识点按属性标签在该优先级下的字典序排序；授课系统随后对整棵知识树执行前序遍历生成大纲（先讲解父知识点，然后依序深入讲解各子分支模块）。

已知课程大纲信息：
- 知识树结构（未排序的子知识点集合）：{tree_structure}
- 知识点属性标签：{node_labels}
- 各模块知识点总数（含父节点自身）：{subtree_sizes}

你的规划目标是推断出特定知识点 {target_node} 在完整大纲中排在第几节课讲解（1 到 {n} 之间的整数）。

你可以反复调用排课咨询接口，每次只能包含一个查询：

子模块讲解先后比较：在父知识点 P 处，询问其两个不同的直接子知识点 X 与 Y 中，哪一个对应的分支模块在大纲中先被讲解。
- 约束：X、Y 必须是同一父知识点 P 的直接子节点，且 X 不等于 Y。

## 查询与提交答案的格式（必须严格遵守）

查询子模块先后顺序（例如查询父概念 R 的子节点 A 和 B）：
<query>R,A,B</query>

提交最终答案时，给出目标知识点的授课序号（1 到 {n} 的整数）：
<answer>5</answer>

注意：为了优化排课效率，请尽可能用最少的查询次数完成推算。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Knowledge Graph Teaching Path Planning System". Your task is to infer the lecture scheduling sequence of a specific knowledge node.

The system constructs a hierarchical knowledge dependency tree T with {n} knowledge nodes, where the core foundational concept (root node) is R. Each node is assigned a 3-symbol teaching attribute tag, with symbols from the set {{★, ◆, ●}}.

Hidden Scheduling Mechanism: A strict teaching priority total order exists for these three attribute symbols, which is unknown but globally consistent. At each parent knowledge node, its subordinate child nodes are sorted by the lexicographic order of their attribute tags under this priority. The teaching system then generates the course syllabus by executing a preorder traversal of the entire tree (lecturing on the parent node first, then recursively delving into each child branch).

Known syllabus information:
- Knowledge tree structure (unordered sets of child nodes): {tree_structure}
- Node attribute tags: {node_labels}
- Total nodes in each module (including the parent node itself): {subtree_sizes}

Your planning goal is to deduce the exact lecture sequence number of the target knowledge node {target_node} in the complete syllabus (an integer between 1 and {n}).

You may repeatedly query the scheduling consultation interface, with one request per query:

Child module lecture sequence comparison: At parent node P, ask which of its two distinct direct child nodes X and Y has its branch module lectured first in the syllabus.
- Constraint: X and Y must be direct child nodes of the same parent knowledge node P, and X must not equal Y.

## Query and Submission Format (must strictly follow)

Query the lecture sequence of child modules (e.g., asking about child nodes A and B under parent concept R):
<query>R,A,B</query>

Submit the final answer by providing the lecture sequence number of the target node (an integer from 1 to {n}):
<answer>5</answer>

Note: To optimize scheduling efficiency, please complete the deduction with as few queries as possible.
"""

    contextualized_rule_zh_4 = """\
欢迎进入“复杂产品 BOM 装配流程与质检扫略系统”。你需要计算出指定组件的质检顺位。

本次分析的装配树 T 共有 {n} 个组件节点，最终成品（根节点）为 R。每个组件均持有一个长度为 3 的工艺参数标签，符号取自集合 {{★, ◆, ●}}。

隐藏扫略机制：对于这三种工艺参数存在一个严密的工艺安全优先级全序，该顺序对分析员未知但全局一致。在每个父级组件处，其包含的直接子组件按各自工艺标签在该全序下的字典序排序；自动化质检机器人将根据该子组件顺序对整棵装配树进行前序遍历扫描（先质检父级组件整体，再依次递归扫略各子组件树）。

已知产品工程数据：
- 装配树结构（未排序的子组件清单）：{tree_structure}
- 组件工艺标签：{node_labels}
- 各分支组件总规模（含父组件自身）：{subtree_sizes}

你的检测目标是精确计算出目标组件 {target_node} 在整个质检扫略流程中是第几个被扫描的（1 到 {n} 之间的整数）。

你可以反复查询系统日志，每次查询仅限一个对比项：

同级组件扫略先后比较：在父组件 P 处，询问其包含的两个不同直接子组件 X 与 Y 中，哪一个对应的组件树优先被扫略。
- 约束：X、Y 必须属于同一父组件 P 的直接下级，且 X 不等于 Y。

## 查询与提交结果的格式（必须严格遵守）

查询组件质检先后顺序（例如询问父组件 R 的子组件 A 和 B）：
<query>R,A,B</query>

提交最终结果时，给出目标组件的质检顺位序号（1 到 {n} 的整数）：
<answer>5</answer>

注意：为了加速诊断，请尽可能用最少的查询次数完成计算。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the "Complex Product BOM Assembly and Quality Inspection Scanning System". You need to calculate the inspection sequence of a specified component.

The analyzed assembly tree T consists of {n} component nodes, where the final product (root node) is R. Each component possesses a 3-symbol process parameter tag, utilizing symbols from the set {{★, ◆, ●}}.

Hidden Scanning Mechanism: A strict process safety priority total order exists among these three parameter symbols, which is unknown to the analyst but globally consistent. At each parent component, its direct sub-components are sorted by the lexicographic order of their process tags under this priority. The automated inspection robot will then perform a preorder traversal scan of the entire assembly tree (inspecting the overall parent component first, then recursively scanning each sub-component tree).

Known product engineering data:
- Assembly tree structure (unordered sub-component lists): {tree_structure}
- Component process tags: {node_labels}
- Scale of each component branch (including the parent component itself): {subtree_sizes}

Your inspection goal is to accurately calculate the exact scanning sequence number of the target component {target_node} during the comprehensive inspection process (an integer between 1 and {n}).

You can repeatedly query the system logs, limited to one comparison per query:

Sibling component scanning comparison: At parent component P, ask which of its two distinct direct sub-components X and Y will have its component tree scanned first.
- Constraint: X and Y must be direct sub-components of the same parent component P, and X must not equal Y.

## Query and Submission Format (must strictly follow)

Query the scanning sequence of components (e.g., asking about sub-components A and B under parent R):
<query>R,A,B</query>

Submit the final result by providing the inspection sequence number of the target component (an integer from 1 to {n}):
<answer>5</answer>

Note: To accelerate the diagnostic process, please complete the calculation with as few queries as possible.
"""

    contextualized_rule_zh_5 = """\
欢迎使用“案件证据链与法理审查排期系统”。本次任务是预判特定证据节点的审查顺位。

本案构建了一棵争议焦点和证据层级树 T，共计 {n} 个审查节点，核心争议（根节点）为 R。每个证据节点带有长度为 3 的审查维度标签，符号取自集合 {{★, ◆, ●}}。

隐藏庭审机制：这些审查维度符号背后存在一个严格的法理审查优先级全序，该顺序未知但全局统一。针对同一父焦点，法庭会将其下属的各项直接子证据/焦点按其维度标签在该优先级全序下的字典序排列排期；庭审推进将对这棵证据树执行前序遍历（首先审查父级焦点，随后依次展开审理各个分支的子证据链）。

已知案卷信息：
- 证据链层级结构（未排序的子证据集合）：{tree_structure}
- 证据审查维度标签：{node_labels}
- 各分支证据链规模（含该焦点自身）：{subtree_sizes}

你的预判目标是推算出目标证据节点 {target_node} 在完整庭审环节中是第几个被出示审查的（1 到 {n} 之间的整数）。

你可以向法庭程序接口反复发起申请，每次申请限提一个请求：

同级证据审查先后比较：在父焦点 P 下，询问其两项不同的直接子证据 X 与 Y 中，哪一项对应的子证据链在庭审中优先被审查。
- 约束：X、Y 必须隶属于同一父焦点 P，且 X 不等于 Y。

## 询问与提交答案的格式（必须严格遵守）

查询证据审查先后顺序（例如询问父焦点 R 的下属证据 A 和 B）：
<query>R,A,B</query>

提交最终预判时，给出目标证据的庭审审查序号（1 到 {n} 的整数）：
<answer>5</answer>

注意：为了节省司法资源，请尽可能用最少的询问次数完成推演。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Case Evidence Chain and Jurisprudential Review Scheduling System". Your task is to forecast the review sequence of a specific evidence node.

This case constructs a controversial focus and evidence hierarchical tree T, totaling {n} review nodes, with the core controversy (root node) being R. Each evidence node carries a 3-symbol review dimension tag, drawn from the set {{★, ◆, ●}}.

Hidden Trial Mechanism: A strict jurisprudential review priority total order lies behind these dimension symbols, which is unknown but globally unified. Under the same parent focus, the court will schedule its subordinate direct child evidence/focuses sorted by the lexicographic order of their dimension tags under this priority order. The trial progression will then execute a preorder traversal of this evidence tree (reviewing the parent focus first, then sequentially examining each branch's child evidence chain).

Known case file information:
- Evidence chain hierarchy (unordered sets of child evidence): {tree_structure}
- Evidence review dimension tags: {node_labels}
- Scale of each evidence branch (including the focus itself): {subtree_sizes}

Your forecasting goal is to calculate the precise trial review sequence number of the target evidence node {target_node} in the complete hearing process (an integer between 1 and {n}).

You may repeatedly submit applications to the court procedural interface, with one request per application:

Sibling evidence review comparison: Under parent focus P, ask which of its two distinct direct child evidence nodes X and Y will have its sub-evidence chain reviewed first in the trial.
- Constraint: X and Y must belong to the same parent focus P, and X must not equal Y.

## Query and Submission Format (must strictly follow)

Query the review sequence of evidence (e.g., asking about child evidence A and B under parent focus R):
<query>R,A,B</query>

Submit your final forecast by providing the trial review sequence number of the target evidence (an integer from 1 to {n}):
<answer>5</answer>

Note: To conserve judicial resources, please complete the deduction with as few queries as possible.
"""

    tags = ["answer", "query"]
    
    # 类属性定义
    reasoning_type = "归纳推理"
    data_structure = "树"

    # 难度配置
    # 难度 1 (简单): 小树，目标节点路径简单
    # 难度 2 (中等偏下): 目标节点需要部分兄弟比较
    # 难度 3 (中等偏上): 需要推断多个分支的顺序
    # 难度 4 (较难): 目标节点在较深位置，需要多次推理
    # 难度 5 (难): 复杂树结构，目标节点需要完整推理链
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 13,
                "tree": {
                    "R": ["A", "B", "C"],
                    "A": ["D", "E"],
                    "B": ["F"],
                    "C": ["G", "H", "I"],
                    "E": ["J"],
                    "I": ["K", "L"],
                },
                "labels": {
                    "R": "★◆●", "A": "◆★●", "B": "●★◆", "C": "★●◆",
                    "D": "◆●★", "E": "●◆★", "F": "●●★",
                    "G": "★◆★", "H": "◆◆★", "I": "★●●",
                    "J": "◆★◆", "K": "●◆◆", "L": "★★★",
                },
                "target": "D",
                "symbol_order": ["★", "◆", "●"],  # 隐藏的符号优先级
            },
            2: {
                "n": 13,
                "tree": {
                    "R": ["A", "B", "C"],
                    "A": ["D", "E"],
                    "B": ["F"],
                    "C": ["G", "H", "I"],
                    "E": ["J"],
                    "I": ["K", "L"],
                },
                "labels": {
                    "R": "★◆●", "A": "◆★●", "B": "●★◆", "C": "★●◆",
                    "D": "◆●★", "E": "●◆★", "F": "●●★",
                    "G": "★◆★", "H": "◆◆★", "I": "★●●",
                    "J": "◆★◆", "K": "●◆◆", "L": "★★★",
                },
                "target": "F",
                "symbol_order": ["◆", "★", "●"],
            },
            3: {
                "n": 13,
                "tree": {
                    "R": ["A", "B", "C"],
                    "A": ["D", "E"],
                    "B": ["F"],
                    "C": ["G", "H", "I"],
                    "E": ["J"],
                    "I": ["K", "L"],
                },
                "labels": {
                    "R": "★◆●", "A": "◆★●", "B": "●★◆", "C": "★●◆",
                    "D": "◆●★", "E": "●◆★", "F": "●●★",
                    "G": "★◆★", "H": "◆◆★", "I": "★●●",
                    "J": "◆★◆", "K": "●◆◆", "L": "★★★",
                },
                "target": "J",
                "symbol_order": ["●", "◆", "★"],
            },
            4: {
                "n": 13,
                "tree": {
                    "R": ["A", "B", "C"],
                    "A": ["D", "E"],
                    "B": ["F"],
                    "C": ["G", "H", "I"],
                    "E": ["J"],
                    "I": ["K", "L"],
                },
                "labels": {
                    "R": "★◆●", "A": "◆★●", "B": "●★◆", "C": "★●◆",
                    "D": "◆●★", "E": "●◆★", "F": "●●★",
                    "G": "★◆★", "H": "◆◆★", "I": "★●●",
                    "J": "◆★◆", "K": "●◆◆", "L": "★★★",
                },
                "target": "K",
                "symbol_order": ["◆", "●", "★"],
            },
            5: {
                "n": 13,
                "tree": {
                    "R": ["A", "B", "C"],
                    "A": ["D", "E"],
                    "B": ["F"],
                    "C": ["G", "H", "I"],
                    "E": ["J"],
                    "I": ["K", "L"],
                },
                "labels": {
                    "R": "★◆●", "A": "◆★●", "B": "●★◆", "C": "★●◆",
                    "D": "◆●★", "E": "●◆★", "F": "●●★",
                    "G": "★◆★", "H": "◆◆★", "I": "★●●",
                    "J": "◆★◆", "K": "●◆◆", "L": "★★★",
                },
                "target": "L",
                "symbol_order": ["●", "★", "◆"],
            },
        },
        "en": {
            1: {
                "n": 13,
                "tree": {
                    "R": ["A", "B", "C"],
                    "A": ["D", "E"],
                    "B": ["F"],
                    "C": ["G", "H", "I"],
                    "E": ["J"],
                    "I": ["K", "L"],
                },
                "labels": {
                    "R": "★◆●", "A": "◆★●", "B": "●★◆", "C": "★●◆",
                    "D": "◆●★", "E": "●◆★", "F": "●●★",
                    "G": "★◆★", "H": "◆◆★", "I": "★●●",
                    "J": "◆★◆", "K": "●◆◆", "L": "★★★",
                },
                "target": "D",
                "symbol_order": ["★", "◆", "●"],
            },
            2: {
                "n": 13,
                "tree": {
                    "R": ["A", "B", "C"],
                    "A": ["D", "E"],
                    "B": ["F"],
                    "C": ["G", "H", "I"],
                    "E": ["J"],
                    "I": ["K", "L"],
                },
                "labels": {
                    "R": "★◆●", "A": "◆★●", "B": "●★◆", "C": "★●◆",
                    "D": "◆●★", "E": "●◆★", "F": "●●★",
                    "G": "★◆★", "H": "◆◆★", "I": "★●●",
                    "J": "◆★◆", "K": "●◆◆", "L": "★★★",
                },
                "target": "F",
                "symbol_order": ["◆", "★", "●"],
            },
            3: {
                "n": 13,
                "tree": {
                    "R": ["A", "B", "C"],
                    "A": ["D", "E"],
                    "B": ["F"],
                    "C": ["G", "H", "I"],
                    "E": ["J"],
                    "I": ["K", "L"],
                },
                "labels": {
                    "R": "★◆●", "A": "◆★●", "B": "●★◆", "C": "★●◆",
                    "D": "◆●★", "E": "●◆★", "F": "●●★",
                    "G": "★◆★", "H": "◆◆★", "I": "★●●",
                    "J": "◆★◆", "K": "●◆◆", "L": "★★★",
                },
                "target": "J",
                "symbol_order": ["●", "◆", "★"],
            },
            4: {
                "n": 13,
                "tree": {
                    "R": ["A", "B", "C"],
                    "A": ["D", "E"],
                    "B": ["F"],
                    "C": ["G", "H", "I"],
                    "E": ["J"],
                    "I": ["K", "L"],
                },
                "labels": {
                    "R": "★◆●", "A": "◆★●", "B": "●★◆", "C": "★●◆",
                    "D": "◆●★", "E": "●◆★", "F": "●●★",
                    "G": "★◆★", "H": "◆◆★", "I": "★●●",
                    "J": "◆★◆", "K": "●◆◆", "L": "★★★",
                },
                "target": "K",
                "symbol_order": ["◆", "●", "★"],
            },
            5: {
                "n": 13,
                "tree": {
                    "R": ["A", "B", "C"],
                    "A": ["D", "E"],
                    "B": ["F"],
                    "C": ["G", "H", "I"],
                    "E": ["J"],
                    "I": ["K", "L"],
                },
                "labels": {
                    "R": "★◆●", "A": "◆★●", "B": "●★◆", "C": "★●◆",
                    "D": "◆●★", "E": "●◆★", "F": "●●★",
                    "G": "★◆★", "H": "◆◆★", "I": "★●●",
                    "J": "◆★◆", "K": "●◆◆", "L": "★★★",
                },
                "target": "L",
                "symbol_order": ["●", "★", "◆"],
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏配置"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保 difficulty 为整数

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 基本信息
        self.n = cfg["n"]
        self.tree = cfg["tree"]
        self.labels = cfg["labels"]
        self.target_node = cfg["target"]
        self.symbol_order = cfg["symbol_order"]
        
        # 计算子树大小
        self.subtree_sizes = self._compute_subtree_sizes()
        
        # 计算真实的前序遍历序号
        self.true_preorder_position = self._compute_true_position()
        
        # 准备游戏信息用于规则展示
        self._game_info["n"] = self.n
        self._game_info["target_node"] = self.target_node
        self._game_info["tree_structure"] = self._format_tree_structure()
        self._game_info["node_labels"] = self._format_node_labels()
        self._game_info["subtree_sizes"] = self._format_subtree_sizes()

    def _compute_subtree_sizes(self) -> Dict[str, int]:
        """计算每个节点的子树大小（含自身）"""
        sizes = {}
        
        def dfs(node: str) -> int:
            if node in sizes:
                return sizes[node]
            
            size = 1  # 自身
            if node in self.tree:
                for child in self.tree[node]:
                    size += dfs(child)
            sizes[node] = size
            return size
        
        dfs("R")
        return sizes

    def _format_tree_structure(self) -> str:
        """格式化树结构信息"""
        lines = []
        for parent, children in sorted(self.tree.items()):
            children_str = ", ".join(sorted(children))
            lines.append(f"{parent} 的孩子: {{{children_str}}}" if self.config.language == "zh" 
                        else f"{parent}'s children: {{{children_str}}}")
        return "; ".join(lines)

    def _format_node_labels(self) -> str:
        """格式化节点标签信息"""
        items = [f"{node}: {label}" for node, label in sorted(self.labels.items())]
        return ", ".join(items)

    def _format_subtree_sizes(self) -> str:
        """格式化子树大小信息"""
        items = [f"size({node})={size}" for node, size in sorted(self.subtree_sizes.items())]
        return ", ".join(items)

    def _compare_labels(self, label1: str, label2: str) -> int:
        """
        根据隐藏的符号优先级比较两个标签的字典序
        返回: -1 如果 label1 < label2, 0 如果相等, 1 如果 label1 > label2
        """
        priority = {sym: i for i, sym in enumerate(self.symbol_order)}
        for c1, c2 in zip(label1, label2):
            if priority[c1] < priority[c2]:
                return -1
            elif priority[c1] > priority[c2]:
                return 1
        return 0

    def _get_sorted_children(self, parent: str) -> List[str]:
        """获取父节点的孩子按标签字典序排序后的列表"""
        if parent not in self.tree:
            return []
        children = self.tree[parent]
        return sorted(children, key=lambda child: (
            [self.symbol_order.index(c) for c in self.labels[child]]
        ))

    def _compute_true_position(self) -> int:
        """计算目标节点在前序遍历中的真实位置"""
        position = [0]  # 使用列表以便在闭包中修改
        found = [False]
        
        def preorder(node: str) -> bool:
            position[0] += 1
            if node == self.target_node:
                found[0] = True
                return True
            
            if node in self.tree:
                for child in self._get_sorted_children(node):
                    if preorder(child):
                        return True
            return False
        
        preorder("R")
        if not found[0]:
            raise ValueError(f"Target node {self.target_node} not found in the tree.")
        return position[0]

    def evaluate(self, parsed_info: Dict[str, str]) -> bool:
        """评估玩家提交的答案是否正确"""
        try:
            answer_str = parsed_info["answer"].strip()
            answer = int(answer_str)
            return answer == self.true_preorder_position
        except (ValueError, KeyError):
            return False

    def _cf_core_produce(self, parsed_info: Dict[str, str]) -> str:
        """核心业务逻辑：处理玩家的查询并返回响应"""
        if "query" not in parsed_info:
            if self.config.language == "zh":
                return "错误：未找到有效的查询标签。"
            else:
                return "Error: No valid query tag found."
        
        query_str = parsed_info["query"].strip()
        parts = [p.strip() for p in query_str.split(",")]
        
        # 验证查询格式：应该是 parent,child1,child2
        if len(parts) != 3:
            if self.config.language == "zh":
                return "错误：查询格式无效。应为：父节点,孩子1,孩子2"
            else:
                return "Error: Invalid query format. Expected: parent,child1,child2"
        
        parent, child1, child2 = parts
        
        # 验证节点存在性
        if parent not in self.tree:
            if self.config.language == "zh":
                return f"错误：节点 {parent} 不是父节点或不存在。"
            else:
                return f"Error: Node {parent} is not a parent or does not exist."
        
        # 验证两个孩子是否都是该父节点的直接孩子
        children_set = set(self.tree[parent])
        if child1 not in children_set or child2 not in children_set:
            if self.config.language == "zh":
                return f"错误：{child1} 和 {child2} 不都是 {parent} 的直接孩子。"
            else:
                return f"Error: {child1} and {child2} are not both direct children of {parent}."
        
        # 验证两个孩子不相同
        if child1 == child2:
            if self.config.language == "zh":
                return "错误：两个孩子节点必须不同。"
            else:
                return "Error: The two children must be different."
        
        # 比较两个孩子的标签字典序
        label1 = self.labels[child1]
        label2 = self.labels[child2]
        cmp_result = self._compare_labels(label1, label2)
        
        # 返回哪个孩子在前
        if cmp_result < 0:
            return child1
        elif cmp_result > 0:
            return child2
        else:
            # 理论上不应该出现标签完全相同的情况
            return child1

    def _cf_make_wrong(self, correct: str) -> str:
        """
        根据正确答案生成一个明显不同的错误答案。
        规则：
        - 若 correct 是纯整数字符串：返回 str(int(correct) + 1)
        - 否则按以下规则替换关键词：
            中文："是" ↔ "否"
            英文："Yes" ↔ "No"（忽略大小写，保持原始大小写风格）
        - 若都不匹配：在字符串末尾追加 "_WRONG"
        """
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        elif self.config.language == "en":
            lower_correct = correct.lower()
            if "yes" in lower_correct:
                # 保持原大小写风格
                if correct[0].isupper():
                    return correct.replace("Yes", "No").replace("YES", "NO")
                return correct.replace("yes", "no")
            if "no" in lower_correct:
                if correct[0].isupper():
                    return correct.replace("No", "Yes").replace("NO", "YES")
                return correct.replace("no", "yes")

        return correct + "_WRONG"

    def get_all_possible_queries(self) -> List[Dict[str, str]]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 合法的 XML 标签字符串
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        queries = []
        for parent, children in self.tree.items():
            if len(children) < 2:
                continue
            # 对任意两个不同的孩子生成查询
            for c1, c2 in itertools.combinations(children, 2):
                # 构造查询内容，格式为 XML 标签
                query_content = f"<query>{parent},{c1},{c2}</query>"
                
                # 直接复用内部比较逻辑计算答案，不经过 produce_response 以避免副作用
                label1 = self.labels[c1]
                label2 = self.labels[c2]
                cmp_result = self._compare_labels(label1, label2)
                
                # 根据比较结果确定答案
                if cmp_result < 0:
                    ans = c1
                elif cmp_result > 0:
                    ans = c2
                else:
                    # 理论上不会相等，若相等则默认为 c1
                    ans = c1
                
                queries.append({
                    "query": query_content,
                    "answer": ans
                })
        return queries