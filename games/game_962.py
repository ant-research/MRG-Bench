# -*- coding: utf-8 -*-

from .base import Game
import re

class TreePermutationLCAGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "树"

    game_rule_zh = """\
我们现在来玩一个"置换树 LCA 推断"游戏，规则如下：

游戏设定了一棵有根树，共有 11 个节点，节点的标签集合为：R（根）、A、B、C、D、E、F、G、H、I、J。

我已经在内部确定了一个标签到真实节点的对应关系（称为"置换规则"），但我不会告诉你具体是哪一种。当你使用标签查询时，我会根据这个置换规则在真实树上计算结果，然后将结果映射回标签空间返回给你。

你的任务是：
1. 通过查询推断出当前采用的置换规则编号（1、2、3 或 4）；
2. 针对给定的一对目标标签 ({target_u}, {target_v})，找出它们的最近公共祖先标签。

你可以反复向我提出以下五类查询（每次仅限一个查询）：

1. 父节点查询：询问标签 X 的父节点是谁。如果 X 是根节点，返回"无"。
2. 祖先判定查询：询问标签 X 是否是标签 Y 的祖先。返回"是"或"否"。
3. 子节点查询：询问标签 X 的所有子节点标签列表（按字母顺序排列）。
4. 深度查询：询问标签 X 在树中的深度（根节点深度为 0）。
5. 距离查询：询问标签 X 和 Y 之间的最短路径边数。

注意：你不能直接询问最近公共祖先，必须通过上述查询推断。

## 查询与提交答案的格式

每次查询只能包含一个标签。请使用以下 XML 格式：

- 父节点查询（例如查询标签 A）：
<query_parent>A</query_parent>

- 祖先判定查询（例如查询 A 是否是 E 的祖先）：
<query_ancestor>A,E</query_ancestor>

- 子节点查询（例如查询标签 R）：
<query_children>R</query_children>

- 深度查询（例如查询标签 C）：
<query_depth>C</query_depth>

- 距离查询（例如查询 A 和 B 的距离）：
<query_distance>A,B</query_distance>

提交最终答案时，必须说明置换规则编号（1、2、3 或 4）和最近公共祖先标签，格式如下：

<answer>permutation=2, lca=A</answer>
"""

    game_rule_en = """\
Let's play a "Permuted Tree LCA Inference" game. Here are the rules:

The game is set on a rooted tree with 11 nodes, labeled as: R (root), A, B, C, D, E, F, G, H, I, J.

I have internally determined a mapping from labels to actual nodes (called a "permutation rule"), but I won't tell you which one. When you query using labels, I will compute results on the real tree according to this permutation rule, then map the results back to the label space.

Your task is to:
1. Infer which permutation rule is currently used (1, 2, 3, or 4) through queries;
2. Find the label of the Lowest Common Ancestor (LCA) for the given target pair ({target_u}, {target_v}).

You can repeatedly ask me five types of queries (one per turn):

1. Parent Query: Ask for the parent node of label X. Returns "None" if X is the root.
2. Ancestor Query: Ask whether label X is an ancestor of label Y. Returns "Yes" or "No".
3. Children Query: Ask for all children labels of X (sorted alphabetically).
4. Depth Query: Ask for the depth of label X in the tree (root has depth 0).
5. Distance Query: Ask for the number of edges in the shortest path between labels X and Y.

Note: You cannot directly ask for the LCA; you must infer it through the above queries.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Parent Query (e.g., querying label A):
<query_parent>A</query_parent>

- Ancestor Query (e.g., asking if A is ancestor of E):
<query_ancestor>A,E</query_ancestor>

- Children Query (e.g., querying label R):
<query_children>R</query_children>

- Depth Query (e.g., querying label C):
<query_depth>C</query_depth>

- Distance Query (e.g., querying distance between A and B):
<query_distance>A,B</query_distance>

When submitting the final answer, specify the permutation rule number (1, 2, 3, or 4) and the LCA label, using this format:

<answer>permutation=2, lca=A</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用城市轨道交通网络盲测排查系统。

系统设定了一个包含 11 个核心枢纽站的树状线网结构，站点代号集合为：R（总枢纽）、A、B、C、D、E、F、G、H、I、J。

系统内部已自动选定了一套"线网路由映射方案"（共 4 种可能的方案，即置换规则），但我不会直接告诉你当前使用的是哪一套。当你输入站点代号进行网络查询时，我会根据该隐秘方案在真实线网物理层进行计算，再将结果转化为代号返回给你。

你的任务是：
1. 通过探测查询，逆向推断出当前生效的路由方案编号（1、2、3 或 4）；
2. 针对系统指定的两个目标站点 ({target_u}, {target_v})，找出它们最近的"公共换乘枢纽"（最近公共祖先节点）。

你可以反复发起以下五种探测查询（每次仅限一种）：

1. 上游枢纽查询：询问站点 X 的直接上游枢纽。若 X 为总枢纽则返回"无"。
2. 主干判定查询：询问站点 X 是否为站点 Y 的主干线路上游（即祖先）。返回"是"或"否"。
3. 下游分支查询：询问站点 X 的所有直接下游站点代号列表（按字母排列）。
4. 换乘层级查询：询问站点 X 在线网中的深度（总枢纽深度为 0）。
5. 站点距离查询：询问站点 X 和 Y 之间的最短通达站数（最短路径边数）。

注意：你不能直接询问最近公共换乘枢纽，必须通过上述探测信息自行推演。

## 查询与提交答案的格式

每次查询只能包含一个站点代号。请严格使用以下 XML 格式：

- 上游枢纽查询（如查询站点 A）：
<query_parent>A</query_parent>

- 主干判定查询（如查询 A 是否为 E 的上游）：
<query_ancestor>A,E</query_ancestor>

- 下游分支查询（如查询总枢纽 R）：
<query_children>R</query_children>

- 换乘层级查询（如查询站点 C）：
<query_depth>C</query_depth>

- 站点距离查询（如查询 A 和 B 的距离）：
<query_distance>A,B</query_distance>

提交最终报告时，必须明确路由方案编号（1、2、3 或 4）以及最近公共换乘枢纽代号，格式如下：

<answer>permutation=2, lca=A</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the Urban Rail Transit Network Blind-Test System.

The system features a tree-like transit network comprising 11 core hub stations, labeled as: R (Main Hub), A, B, C, D, E, F, G, H, I, J.

The system has secretly selected a "network routing map version" (one of 4 possible mapping permutations), but I will not directly reveal which one is active. When you query the network using station labels, I will compute the result on the actual physical routing map and return the corresponding mapped labels to you.

Your task is to:
1. Infer the currently active routing map version (1, 2, 3, or 4) through exploratory queries;
2. Find the nearest "Common Transfer Hub" (Lowest Common Ancestor) for the target station pair ({target_u}, {target_v}).

You can repeatedly issue the following five types of queries (one per turn):

1. Upstream Hub Query: Ask for the immediate upstream hub of station X. Returns "None" if X is the Main Hub.
2. Mainline Ancestor Query: Ask whether station X is an upstream mainline ancestor of station Y. Returns "Yes" or "No".
3. Downstream Branch Query: Ask for all immediate downstream station labels of X (sorted alphabetically).
4. Transfer Tier Query: Ask for the depth of station X in the network (Main Hub has depth 0).
5. Station Distance Query: Ask for the shortest number of stops (edges) between stations X and Y.

Note: You cannot directly ask for the common transfer hub; you must deduce it from the queried information.

## Query and Answer Format

Each query must contain only one label. Please strictly use the following XML format:

- Upstream Hub Query (e.g., querying station A):
<query_parent>A</query_parent>

- Mainline Ancestor Query (e.g., asking if A is upstream of E):
<query_ancestor>A,E</query_ancestor>

- Downstream Branch Query (e.g., querying Main Hub R):
<query_children>R</query_children>

- Transfer Tier Query (e.g., querying station C):
<query_depth>C</query_depth>

- Station Distance Query (e.g., querying distance between A and B):
<query_distance>A,B</query_distance>

When submitting your final report, you must specify the routing map version (1, 2, 3, or 4) and the nearest Common Transfer Hub label, using this format:

<answer>permutation=2, lca=A</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用智能分级诊疗溯源系统。

系统设定了一个包含 11 个诊疗科室层级的树状结构，科室代号集合为：R（总院核心科室）、A、B、C、D、E、F、G、H、I、J。

系统内部已隐秘加载了一套"诊疗分级标准版本"（共 4 种可能的架构即置换规则），但我不会告诉你当前启用的是哪一套。当你输入代号进行查询时，我会根据真实的科室层级关系计算结果，再将其转换为对应代号返回。

你的任务是：
1. 通过问询推断出当前启用的诊疗分级标准版本号（1、2、3 或 4）；
2. 针对指定的目标科室对 ({target_u}, {target_v})，找出它们的最低层级"公共上级科室"（最近公共祖先节点）。

你可以反复发起以下五种问询（每次仅限一种）：

1. 上级科室查询：询问科室 X 的直接上级科室。若 X 为总院核心则返回"无"。
2. 归属判定查询：询问科室 X 是否为科室 Y 的宏观上级归属（即祖先）。返回"是"或"否"。
3. 下属分支查询：询问科室 X 的所有直接下属科室代号列表（按字母排列）。
4. 分级深度查询：询问科室 X 在分级体系中的深度（总院深度为 0）。
5. 跨科室距离查询：询问科室 X 和 Y 之间的最少转诊层级数（最短路径边数）。

注意：你不能直接询问公共上级科室，必须通过上述问询推演得出。

## 查询与提交答案的格式

每次查询只能包含一个科室代号。请使用以下 XML 格式：

- 上级科室查询（例如查询科室 A）：
<query_parent>A</query_parent>

- 归属判定查询（例如查询 A 是否为 E 的上级）：
<query_ancestor>A,E</query_ancestor>

- 下属分支查询（例如查询总院 R）：
<query_children>R</query_children>

- 分级深度查询（例如查询科室 C）：
<query_depth>C</query_depth>

- 跨科室距离查询（例如查询 A 和 B 的转诊层级数）：
<query_distance>A,B</query_distance>

提交最终报告时，必须明确分级标准版本（1、2、3 或 4）和公共上级科室代号，格式如下：

<answer>permutation=2, lca=A</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the Intelligent Hierarchical Medical Referral Traceability System.

The system features a hierarchical tree structure of 11 medical departments, with department codes: R (Core General Hospital), A, B, C, D, E, F, G, H, I, J.

The system has securely loaded a "Diagnostic Protocol Version" (one of 4 possible architectural mapping rules), but which version is active is hidden from you. When you query using codes, I will compute the outcome based on the authentic hierarchical medical relationships and return the mapped codes to you.

Your task is to:
1. Infer the currently active Diagnostic Protocol Version (1, 2, 3, or 4) through inquiries;
2. Find the lowest-level "Common Superior Department" (Lowest Common Ancestor) for the target department pair ({target_u}, {target_v}).

You may repeatedly submit the following five types of inquiries (one per turn):

1. Superior Department Query: Ask for the immediate superior department of code X. Returns "None" if X is the Core General Hospital.
2. Broad Category Inclusion Query: Ask whether department X is a macro-level superior (ancestor) of department Y. Returns "Yes" or "No".
3. Sub-department Query: Ask for all immediate sub-department codes under X (sorted alphabetically).
4. Specificity Level Query: Ask for the depth of department X in the referral system (Core General Hospital has depth 0).
5. Cross-department Referral Query: Ask for the minimum number of referral steps (edges) between departments X and Y.

Note: You cannot directly query the Common Superior Department; you must deduce it from the inquiry results.

## Query and Answer Format

Each query must contain only one department code. Please strictly use the following XML format:

- Superior Department Query (e.g., querying department A):
<query_parent>A</query_parent>

- Broad Category Inclusion Query (e.g., asking if A is superior to E):
<query_ancestor>A,E</query_ancestor>

- Sub-department Query (e.g., querying Core General Hospital R):
<query_children>R</query_children>

- Specificity Level Query (e.g., querying department C):
<query_depth>C</query_depth>

- Cross-department Referral Query (e.g., querying steps between A and B):
<query_distance>A,B</query_distance>

Upon finalizing your diagnostic trace, you must specify the Protocol Version (1, 2, 3, or 4) and the Common Superior Department code, formatted as follows:

<answer>permutation=2, lca=A</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎进入自适应学习图谱分析平台。

系统构建了一棵包含 11 个知识点模块的树状前置依赖图谱，模块代号为：R（核心基础模块）、A、B、C、D、E、F、G、H、I、J。

系统内部套用了一种特定的"课程大纲映射方案"（共 4 种版本即置换规则），但我不会透露当前的大纲版本。你在图谱中进行检索时，系统将基于隐秘大纲的真实逻辑计算出结果，再折算回原代号反馈给你。

你的任务是：
1. 经过检索推断出当前的课程大纲版本号（1、2、3 或 4）；
2. 针对给定的两个目标知识点 ({target_u}, {target_v})，找出它们的最深入"公共前置基础模块"（最近公共祖先节点）。

你可以随时进行以下五类检索查询（每次仅限一个）：

1. 直接前置查询：询问模块 X 的直接前置模块。若 X 为核心基础则返回"无"。
2. 基础依赖判定查询：询问模块 X 是否为模块 Y 的根本前置依赖（即祖先）。返回"是"或"否"。
3. 后续分支查询：询问模块 X 解锁的所有直接后续模块列表（按字母顺序）。
4. 知识点层级查询：询问模块 X 在图谱体系内的深度（核心基础深度为 0）。
5. 学习路径跨度查询：询问模块 X 和 Y 在图谱中的最短推导步数（边数）。

注意：你不能直接询问公共前置基础，必须利用检索数据逐步推理。

## 查询与提交答案的格式

每次查询只能包含一个模块代号。请使用以下 XML 格式：

- 直接前置查询（例如查询模块 A）：
<query_parent>A</query_parent>

- 基础依赖判定查询（例如查询 A 是否是 E 的前置）：
<query_ancestor>A,E</query_ancestor>

- 后续分支查询（例如查询模块 R）：
<query_children>R</query_children>

- 知识点层级查询（例如查询模块 C）：
<query_depth>C</query_depth>

- 学习路径跨度查询（例如查询 A 和 B 的跨度）：
<query_distance>A,B</query_distance>

提交最终答案时，必须注明课程大纲版本号（1、2、3 或 4）和公共前置基础模块代号，格式如下：

<answer>permutation=2, lca=A</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Adaptive Learning Knowledge Graph Analytics Platform.

The platform relies on a prerequisite dependency tree mapping 11 knowledge modules, labeled as: R (Core Foundation), A, B, C, D, E, F, G, H, I, J.

A specific "Curriculum Blueprint Version" (one of 4 mapping permutations) is applied in the background. The active version is concealed. For any graph search using module labels, the system relies on the hidden syllabus logic to process the query, then translates the result back to your labels.

Your task is to:
1. Deduce the current Curriculum Blueprint Version (1, 2, 3, or 4) via structural retrievals;
2. Identify the most advanced "Common Prerequisite Module" (Lowest Common Ancestor) for the target module pair ({target_u}, {target_v}).

You may conduct the following five types of searches at any time (one per turn):

1. Immediate Prerequisite Query: Ask for the direct prerequisite of module X. Returns "None" if X is the Core Foundation.
2. Foundational Dependency Query: Ask whether module X is a foundational prerequisite (ancestor) of module Y. Returns "Yes" or "No".
3. Follow-up Branch Query: Ask for all immediate follow-up modules unlocked by X (sorted alphabetically).
4. Module Level Query: Ask for the depth of module X within the knowledge graph (Core Foundation has depth 0).
5. Learning Path Span Query: Ask for the minimum number of deductive steps (edges) between modules X and Y.

Note: You cannot ask for the common prerequisite directly; it must be mapped out using retrieval queries.

## Query and Answer Format

Each query is strictly limited to one module label. Apply the following XML format:

- Immediate Prerequisite Query (e.g., querying module A):
<query_parent>A</query_parent>

- Foundational Dependency Query (e.g., asking if A is a prerequisite for E):
<query_ancestor>A,E</query_ancestor>

- Follow-up Branch Query (e.g., querying Core Foundation R):
<query_children>R</query_children>

- Module Level Query (e.g., querying module C):
<query_depth>C</query_depth>

- Learning Path Span Query (e.g., querying the span between A and B):
<query_distance>A,B</query_distance>

When submitting your final blueprint mapping, denote the Curriculum Blueprint Version (1, 2, 3, or 4) and the Common Prerequisite Module label, in this exact format:

<answer>permutation=2, lca=A</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎使用工业 BOM（物料清单）拓扑分析终端。

本终端维护了一套具有 11 个组件节点的装配拓扑树，组件代号为：R（顶层总成）、A、B、C、D、E、F、G、H、I、J。

后台采用了一种未公开的"装配图纸版本"（有 4 种备选配置即置换规则）将代号映射为物理组件。所有基于代号的探测，系统都会在底层的物理装配逻辑上计算，再映射回对应的代号空间呈现给你。

你的任务是：
1. 通过结构探测还原出当前的装配图纸版本号（1、2、3 或 4）；
2. 针对指定的目标组件 ({target_u}, {target_v})，找出它们最低层级的"公共父装配体"（最近公共祖先节点）。

你可以向终端提交以下五种探查指令（每次限用一条）：

1. 父装配体查询：询问组件 X 的直接父装配体。若 X 为顶层总成则返回"无"。
2. 包含关系判定查询：询问组件 X 是否是包含组件 Y 的上级装配体（即祖先）。返回"是"或"否"。
3. 子组件查询：询问组件 X 下一层包含的所有直接子组件代号（按字母排列）。
4. 装配层级查询：询问组件 X 在 BOM 树中的层级深度（顶层总成为 0）。
5. BOM 距离查询：询问组件 X 和 Y 在层级结构中的最短结构跨度（边数）。

注意：你不能直接查询公共父装配体，必须依赖分析指令反推。

## 查询与提交答案的格式

每次探测仅限一个组件代号。指令需符合以下 XML 规范：

- 父装配体查询（例如查询组件 A）：
<query_parent>A</query_parent>

- 包含关系判定查询（例如判定 A 是否包含 E）：
<query_ancestor>A,E</query_ancestor>

- 子组件查询（例如查询组件 R）：
<query_children>R</query_children>

- 装配层级查询（例如查询组件 C）：
<query_depth>C</query_depth>

- BOM 距离查询（例如查询 A 和 B 的结构跨度）：
<query_distance>A,B</query_distance>

分析结束输出结论时，必须给出装配图纸版本（1、2、3 或 4）及公共父装配体代号：

<answer>permutation=2, lca=A</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Industrial Bill of Materials (BOM) Topology Analysis Terminal.

This terminal accesses an assembly topology tree with 11 component nodes, labeled as: R (Top-Level Assembly), A, B, C, D, E, F, G, H, I, J.

The backend uses an undisclosed "Assembly Blueprint Version" (one of 4 alternate BOM permutations) to map physical components to these labels. Any structural probe you send will be evaluated against the underlying physical assembly tree, and the output mapped back to your designated labels.

Your task is to:
1. Reverse-engineer the active Assembly Blueprint Version (1, 2, 3, or 4) through topological probing;
2. Determine the lowest-tier "Common Parent Assembly" (Lowest Common Ancestor) for the given component pair ({target_u}, {target_v}).

You can submit the following five types of diagnostic probes (one per turn):

1. Parent Assembly Query: Ask for the immediate parent assembly of component X. Returns "None" if X is the Top-Level Assembly.
2. Component Containment Query: Ask whether component X is a macro-assembly encompassing component Y (i.e., ancestor). Returns "Yes" or "No".
3. Subcomponent Query: Ask for all direct subcomponents contained within X (sorted alphabetically).
4. Assembly Tier Query: Ask for the depth of component X in the BOM tree (Top-Level Assembly has depth 0).
5. BOM Distance Query: Ask for the shortest structural span (number of edges) between components X and Y.

Note: The system restricts direct lookup of the Common Parent Assembly; you must infer it through component probes.

## Query and Answer Format

Each probe must only target one component label. Ensure queries conform to this XML syntax:

- Parent Assembly Query (e.g., probing component A):
<query_parent>A</query_parent>

- Component Containment Query (e.g., determining if A contains E):
<query_ancestor>A,E</query_ancestor>

- Subcomponent Query (e.g., probing Top-Level Assembly R):
<query_children>R</query_children>

- Assembly Tier Query (e.g., probing component C):
<query_depth>C</query_depth>

- BOM Distance Query (e.g., probing distance between A and B):
<query_distance>A,B</query_distance>

To conclude the analysis, state the Assembly Blueprint Version (1, 2, 3, or 4) and the Common Parent Assembly label:

<answer>permutation=2, lca=A</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用法律条款层级适用性核查系统。

系统设定了一部包含 11 个条文节点的法典层级树，条款代号为：R（核心基本法）、A、B、C、D、E、F、G、H、I、J。

法典库当前应用了一种"法典编纂架构"（从 4 种生效版本即置换规则中选用），版本对你是保密的。所有针对条款的质询，系统均依据底层的法理统辖关系进行判定，并将结果转化回代号反馈。

你的任务是：
1. 利用质询手段查明当前生效的法典编纂架构编号（1、2、3 或 4）；
2. 针对两项待释明的条款 ({target_u}, {target_v})，找出它们最具体的"公共上位法条款"（最近公共祖先节点）。

你可以随时提请以下五类法定质询（每次仅限一类）：

1. 直接上位法查询：询问条款 X 的直接上位统辖条款。若 X 为核心基本法则返回"无"。
2. 统辖关系判定查询：询问条款 X 是否为统辖条款 Y 的宏观上位法（即祖先）。返回"是"或"否"。
3. 下属细则查询：询问条款 X 授权衍生的所有直接下属条款代号（按字母顺序）。
4. 条款层级查询：询问条款 X 在法典中的层级深度（核心基本法为 0）。
5. 交叉引用距离查询：询问条款 X 和 Y 之间的最短法理推导步数（逻辑边数）。

注意：系统拒绝直接告知公共上位法，你必须通过上述程序推导。

## 查询与提交答案的格式

每次质询限于一个法条代号。文书需符合以下 XML 格式：

- 直接上位法查询（例如质询条款 A）：
<query_parent>A</query_parent>

- 统辖关系判定查询（例如确认 A 是否统辖 E）：
<query_ancestor>A,E</query_ancestor>

- 下属细则查询（例如质询条款 R）：
<query_children>R</query_children>

- 条款层级查询（例如质询条款 C）：
<query_depth>C</query_depth>

- 交叉引用距离查询（例如确认 A 和 B 的推导步数）：
<query_distance>A,B</query_distance>

在最终裁定报告中，须明确法典编纂架构编号（1、2、3 或 4）与公共上位法条款代号，格式为：

<answer>permutation=2, lca=A</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the Legal Provision Hierarchy Applicability Review System.

The system hosts a codified legal tree comprising 11 statutory nodes, denoted as: R (Core Constitutional Statute), A, B, C, D, E, F, G, H, I, J.

A specific "Legal Codification Framework" (chosen from 4 active mapping permutations) governs the jurisprudence repository. This version is classified. All queries submitted using codes are adjudicated against the root jurisprudential logic, with outcomes systematically returned via their mapped labels.

Your task is to:
1. Investigate and identify the prevailing Legal Codification Framework version (1, 2, 3, or 4);
2. Ascertain the most specific "Common Governing Statute" (Lowest Common Ancestor) for the paired provisions ({target_u}, {target_v}).

You may raise the following five types of statutory inquiries (one per turn):

1. Superseding Clause Query: Ask for the direct superseding provision of clause X. Returns "None" if X is the Core Constitutional Statute.
2. Statutory Jurisdiction Query: Ask whether clause X serves as a macro-level governing statute (ancestor) over clause Y. Returns "Yes" or "No".
3. Sub-clause Query: Ask for all immediate derived sub-clauses under clause X (sorted alphabetically).
4. Specificity Tier Query: Ask for the depth of clause X in the codification framework (Core Statute has depth 0).
5. Cross-reference Distance Query: Ask for the shortest jurisprudential derivation steps (edges) between clauses X and Y.

Note: Direct querying of the Common Governing Statute is procedurally prohibited; you must arrive at it through logical statutory deduction.

## Query and Answer Format

Each inquiry is restricted to one statutory code. Submissions must adhere to the XML format below:

- Superseding Clause Query (e.g., inquiring about clause A):
<query_parent>A</query_parent>

- Statutory Jurisdiction Query (e.g., confirming if A governs E):
<query_ancestor>A,E</query_ancestor>

- Sub-clause Query (e.g., inquiring about Core Statute R):
<query_children>R</query_children>

- Specificity Tier Query (e.g., inquiring about clause C):
<query_depth>C</query_depth>

- Cross-reference Distance Query (e.g., calculating derivation steps between A and B):
<query_distance>A,B</query_distance>

In your final ruling report, state the Legal Codification Framework version (1, 2, 3, or 4) alongside the Common Governing Statute label, strictly formatted as:

<answer>permutation=2, lca=A</answer>
"""

    tags = ["answer", "query_parent", "query_ancestor", "query_children", "query_depth", "query_distance"]

    # 真实树结构（固定）
    TRUE_TREE = {
        'R': {'parent': None, 'children': ['A', 'B'], 'depth': 0},
        'A': {'parent': 'R', 'children': ['C', 'D'], 'depth': 1},
        'B': {'parent': 'R', 'children': ['G', 'H'], 'depth': 1},
        'C': {'parent': 'A', 'children': ['E'], 'depth': 2},
        'D': {'parent': 'A', 'children': ['F'], 'depth': 2},
        'E': {'parent': 'C', 'children': [], 'depth': 3},
        'F': {'parent': 'D', 'children': [], 'depth': 3},
        'G': {'parent': 'B', 'children': ['I'], 'depth': 2},
        'H': {'parent': 'B', 'children': ['J'], 'depth': 2},
        'I': {'parent': 'G', 'children': [], 'depth': 3},
        'J': {'parent': 'H', 'children': [], 'depth': 3},
    }

    # 四种置换规则
    PERMUTATIONS = {
        1: {'R': 'R', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G', 'H': 'H', 'I': 'I', 'J': 'J'},  # α: 恒等
        2: {'R': 'R', 'A': 'B', 'B': 'A', 'C': 'G', 'D': 'H', 'E': 'I', 'F': 'J', 'G': 'C', 'H': 'D', 'I': 'E', 'J': 'F'},  # β: 大分支互换
        3: {'R': 'R', 'A': 'B', 'B': 'A', 'C': 'D', 'D': 'C', 'E': 'F', 'F': 'E', 'G': 'H', 'H': 'G', 'I': 'J', 'J': 'I'},  # γ: 同层兄弟互换
        4: {'R': 'R', 'A': 'A', 'B': 'B', 'C': 'H', 'D': 'G', 'E': 'J', 'F': 'I', 'G': 'D', 'H': 'C', 'I': 'F', 'J': 'E'},  # δ: β 与 γ 的合成
    }

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"permutation_id": 1, "target_u": "E", "target_v": "F"},
            2: {"permutation_id": 2, "target_u": "C", "target_v": "G"},
            3: {"permutation_id": 3, "target_u": "E", "target_v": "J"},
            4: {"permutation_id": 4, "target_u": "D", "target_v": "H"},
            5: {"permutation_id": 2, "target_u": "I", "target_v": "J"},
        },
        "en": {
            1: {"permutation_id": 1, "target_u": "E", "target_v": "F"},
            2: {"permutation_id": 2, "target_u": "C", "target_v": "G"},
            3: {"permutation_id": 3, "target_u": "E", "target_v": "J"},
            4: {"permutation_id": 4, "target_u": "D", "target_v": "H"},
            5: {"permutation_id": 2, "target_u": "I", "target_v": "J"},
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.permutation_id = cfg["permutation_id"]
        self.target_u = cfg["target_u"]
        self.target_v = cfg["target_v"]

        # 当前使用的置换映射
        self.permutation = self.PERMUTATIONS[self.permutation_id]
        # 构建逆映射
        self.inverse_permutation = {v: k for k, v in self.permutation.items()}

        # 计算正确的 LCA
        real_u = self.permutation[self.target_u]
        real_v = self.permutation[self.target_v]
        real_lca = self._compute_lca(real_u, real_v)
        self.correct_lca = self.inverse_permutation[real_lca]

        # 用于 game_rule 中的占位符
        self._game_info["target_u"] = self.target_u
        self._game_info["target_v"] = self.target_v

    def _compute_lca(self, node1, node2):
        """在真实树上计算两个节点的最近公共祖先"""
        # 获取 node1 的所有祖先（包括自己）
        ancestors1 = set()
        current = node1
        while current is not None:
            ancestors1.add(current)
            current = self.TRUE_TREE[current]['parent']
        
        # 从 node2 向上找第一个在 ancestors1 中的节点
        current = node2
        while current is not None:
            if current in ancestors1:
                return current
            current = self.TRUE_TREE[current]['parent']
        
        return None

    def _is_ancestor(self, ancestor, descendant):
        """判断 ancestor 是否是 descendant 的祖先（在真实树上）"""
        current = descendant
        while current is not None:
            if current == ancestor:
                return True
            current = self.TRUE_TREE[current]['parent']
        return False

    def _compute_distance(self, node1, node2):
        """计算两个节点之间的距离（边数）"""
        lca = self._compute_lca(node1, node2)
        dist1 = self.TRUE_TREE[node1]['depth'] - self.TRUE_TREE[lca]['depth']
        dist2 = self.TRUE_TREE[node2]['depth'] - self.TRUE_TREE[lca]['depth']
        return dist1 + dist2

    def evaluate(self, parsed_info):
        """评估答案是否正确"""
        raw_ans = parsed_info["answer"]
        # 解析格式: permutation=X, lca=Y
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        for kv in kv_pairs:
            if "=" not in kv:
                continue
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "permutation" not in ans_dict or "lca" not in ans_dict:
            return False
        
        # 检查置换规则编号
        try:
            model_perm = int(ans_dict["permutation"])
        except:
            return False
        
        if model_perm != self.permutation_id:
            return False
        
        # 检查 LCA
        model_lca = ans_dict["lca"].strip()
        return model_lca == self.correct_lca

    def _cf_core_produce(self, parsed_info):
        """根据查询生成响应"""
        if self.config.language == "zh":
            yes_res, no_res, none_res = "是", "否", "无"
            error_format = "错误：格式无效或标签错误。"
            error_range = "错误：标签超出范围。"
        else:
            yes_res, no_res, none_res = "Yes", "No", "None"
            error_format = "Error: Invalid format or label."
            error_range = "Error: Label out of range."

        # 父节点查询
        if "query_parent" in parsed_info:
            label = parsed_info["query_parent"].strip()
            if label not in self.permutation:
                return error_range
            real_node = self.permutation[label]
            real_parent = self.TRUE_TREE[real_node]['parent']
            if real_parent is None:
                return none_res
            return self.inverse_permutation[real_parent]

        # 祖先判定查询
        elif "query_ancestor" in parsed_info:
            try:
                raw = parsed_info["query_ancestor"]
                label1, label2 = [x.strip() for x in raw.split(",")]
                if label1 not in self.permutation or label2 not in self.permutation:
                    return error_range
                real_node1 = self.permutation[label1]
                real_node2 = self.permutation[label2]
                is_anc = self._is_ancestor(real_node1, real_node2)
                return yes_res if is_anc else no_res
            except:
                return error_format

        # 子节点查询
        elif "query_children" in parsed_info:
            label = parsed_info["query_children"].strip()
            if label not in self.permutation:
                return error_range
            real_node = self.permutation[label]
            real_children = self.TRUE_TREE[real_node]['children']
            label_children = [self.inverse_permutation[c] for c in real_children]
            label_children.sort()
            return ",".join(label_children) if label_children else (none_res if self.config.language == "zh" else "None")

        # 深度查询
        elif "query_depth" in parsed_info:
            label = parsed_info["query_depth"].strip()
            if label not in self.permutation:
                return error_range
            real_node = self.permutation[label]
            return str(self.TRUE_TREE[real_node]['depth'])

        # 距离查询
        elif "query_distance" in parsed_info:
            try:
                raw = parsed_info["query_distance"]
                label1, label2 = [x.strip() for x in raw.split(",")]
                if label1 not in self.permutation or label2 not in self.permutation:
                    return error_range
                real_node1 = self.permutation[label1]
                real_node2 = self.permutation[label2]
                dist = self._compute_distance(real_node1, real_node2)
                return str(dist)
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")
    
    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        results = []
        labels = ['R', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        
        # 根据语言设定返回值
        if self.config.language == "zh":
            yes_res, no_res, none_res = "是", "否", "无"
        else:
            yes_res, no_res, none_res = "Yes", "No", "None"

        for label in labels:
            # 1. 父节点查询
            query_parent = f"<query_parent>{label}</query_parent>"
            real_node = self.permutation[label]
            real_parent = self.TRUE_TREE[real_node]['parent']
            if real_parent is None:
                ans_parent = none_res
            else:
                ans_parent = self.inverse_permutation[real_parent]
            results.append({"query": query_parent, "answer": ans_parent})

            # 3. 子节点查询
            query_children = f"<query_children>{label}</query_children>"
            real_node = self.permutation[label]
            real_children = self.TRUE_TREE[real_node]['children']
            label_children = [self.inverse_permutation[c] for c in real_children]
            label_children.sort()
            if label_children:
                ans_children = ",".join(label_children)
            else:
                ans_children = none_res if self.config.language == "zh" else "None"
            results.append({"query": query_children, "answer": ans_children})

            # 4. 深度查询
            query_depth = f"<query_depth>{label}</query_depth>"
            real_node = self.permutation[label]
            ans_depth = str(self.TRUE_TREE[real_node]['depth'])
            results.append({"query": query_depth, "answer": ans_depth})

        # 2. 祖先判定查询 & 5. 距离查询
        for l1 in labels:
            for l2 in labels:
                # 祖先
                query_ancestor = f"<query_ancestor>{l1},{l2}</query_ancestor>"
                real_node1 = self.permutation[l1]
                real_node2 = self.permutation[l2]
                is_anc = self._is_ancestor(real_node1, real_node2)
                ans_ancestor = yes_res if is_anc else no_res
                results.append({"query": query_ancestor, "answer": ans_ancestor})

                # 距离
                query_distance = f"<query_distance>{l1},{l2}</query_distance>"
                dist = self._compute_distance(real_node1, real_node2)
                ans_distance = str(dist)
                results.append({"query": query_distance, "answer": ans_distance})
                
        return results

    def _cf_make_wrong(self, correct: str) -> str:
        """将正确的查询响应篡改为错误值，用于反事实干预"""
        is_zh = self.config.language == "zh"
        yes_res = "是" if is_zh else "Yes"
        no_res = "否" if is_zh else "No"
        none_res = "无" if is_zh else "None"

        # 处理祖先判定查询：是/否互换
        if correct == yes_res:
            return no_res
        if correct == no_res:
            return yes_res

        # 处理深度/距离查询：数字加1
        try:
            val = int(correct)
            return str(val + 1)
        except ValueError:
            pass

        # 处理父节点查询：若返回"无"则伪造一个标签；若返回标签则改为另一个
        if correct == none_res:
            return "A"  # 伪造一个父节点

        # 处理子节点查询：若返回标签列表则打乱第一个
        all_labels = ['R', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        if correct in all_labels:
            # 父节点查询返回单个标签的情况
            others = [l for l in all_labels if l != correct]
            return others[0]

        # 子节点列表（逗号分隔）
        if "," in correct:
            parts = correct.split(",")
            # 删除第一个子节点作为错误答案
            return ",".join(parts[1:]) if len(parts) > 1 else none_res

        return correct + "_WRONG"