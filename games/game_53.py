# -*- coding: utf-8 -*-
from .base import Game
import random

class TreeDepthQueryGame(Game):
    tags = ["query_parent", "query_children", "query_subtree", "answer"]
    reasoning_type = "演绎推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"树深度推理"游戏，规则如下：

游戏设定了一棵固定的有根树，节点编号为 1 到 {n}。根节点为 {root}，根的深度定义为 0。目标节点为 {target}。

节点的深度定义为：从根节点到该节点的唯一路径上的边数。

你的目标是推断出目标节点 {target} 的深度。你可以反复向我提出以下三类查询（每次仅限一个查询），我会根据树的真实结构如实回答：

1. 父节点查询：询问节点 u 的父节点是谁。
   - 若 u 不是根节点，回答其父节点编号（一个整数）。
   - 若 u 是根节点，回答"NONE"。

2. 子节点列表查询：询问节点 u 有哪些子节点。
   - 回答 u 的所有子节点编号列表（可能为空）。

3. 子树包含关系查询：询问节点 x 是否在以节点 u 为根的子树中（包含 u 本身）。
   - 若 x 在 u 的子树中，回答"YES"。
   - 否则回答"NO"。

注意：所有回答仅基于树的局部结构，不会直接提供深度或距离信息。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 父节点查询（例如查询节点 5 的父节点）：
<query_parent>5</query_parent>

- 子节点列表查询（例如查询节点 3 的子节点）：
<query_children>3</query_children>

- 子树包含关系查询（例如查询节点 2 的子树是否包含节点 7，格式为 u,x）：
<query_subtree>2,7</query_subtree>

提交最终答案时，直接给出目标节点的深度（一个非负整数），格式如下：

<answer>5</answer>
"""

    game_rule_en = """\
Let's play a "Tree Depth Reasoning" game. Here are the rules:

The game features a fixed rooted tree with nodes numbered from 1 to {n}. The root node is {root}, and the root's depth is defined as 0. The target node is {target}.

A node's depth is defined as: the number of edges on the unique path from the root to that node.

Your goal is to determine the depth of the target node {target}. You can repeatedly ask me three types of queries (one per turn), and I will answer truthfully based on the tree's actual structure:

1. Parent Query: Ask for the parent of node u.
   - If u is not the root, answer with its parent's node number (an integer).
   - If u is the root, answer "NONE".

2. Children Query: Ask for the children of node u.
   - Answer with the list of all child node numbers of u (may be empty).

3. Subtree Containment Query: Ask whether node x is in the subtree rooted at node u (including u itself).
   - If x is in u's subtree, answer "YES".
   - Otherwise answer "NO".

Note: All answers are based solely on the tree's local structure and do not directly provide depth or distance information.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Parent Query (e.g., query parent of node 5):
<query_parent>5</query_parent>

- Children Query (e.g., query children of node 3):
<query_children>3</query_children>

- Subtree Containment Query (e.g., query if subtree of node 2 contains node 7, format is u,x):
<query_subtree>2,7</query_subtree>

When submitting the final answer, provide the depth of the target node (a non-negative integer) in this format:

<answer>5</answer>
"""

    # ==========================================
    # 场景 1：交通
    # ==========================================
    contextualized_rule_zh_1 = """\
欢迎来到"轨道交通路网测算系统"。

本系统记录了一个呈严格树形发散的轨道交通网，站点编号为 1 到 {n}。中央枢纽站为 {root}，其区段层级定义为 0。你需要定位的目标站点为 {target}。

站点的区段层级定义为：从中央枢纽站到该站点的唯一线路上的区间数（边数）。

你的任务是推断出目标站点 {target} 的区段层级。你可以反复向系统提出以下三类查询（每次仅限一个查询），系统将根据真实路网结构如实反馈：

1. 上一级站点查询：询问站点 u 向中央枢纽方向相邻的站点是谁。
   - 若 u 不是中央枢纽站，返回其上一级站点编号（一个整数）。
   - 若 u 是中央枢纽站，返回"NONE"。

2. 下一级站点列表查询：询问站点 u 有哪些远离中央枢纽方向的直接相邻站点。
   - 返回 u 的所有下一级站点编号列表（可能为空）。

3. 分支路网包含关系查询：询问站点 x 是否在以站点 u 为起点的分支路网中（包含 u 本身）。
   - 若 x 在 u 的分支路网中，返回"YES"。
   - 否则返回"NO"。

注意：所有回答仅基于路网的局部连接结构，不会直接提供层级或距离信息。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，测算失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 上一级站点查询（例如查询站点 5 的上一级站点）：
<query_parent>5</query_parent>

- 下一级站点列表查询（例如查询站点 3 的下一级站点）：
<query_children>3</query_children>

- 分支路网包含关系查询（例如查询站点 2 的分支路网是否包含站点 7，格式为 u,x）：
<query_subtree>2,7</query_subtree>

提交最终答案时，直接给出目标站点的区段层级（一个非负整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic/Transportation Scenario]
Welcome to the "Rail Transit Network Calculation System".

This system records a strictly tree-shaped rail transit network with stations numbered from 1 to {n}. The central hub station is {root}, and its section level is defined as 0. The target station you need to locate is {target}.

A station's section level is defined as: the number of sections (edges) on the unique route from the central hub to that station.

Your task is to deduce the section level of the target station {target}. You can repeatedly ask the system three types of queries (one per turn), and the system will answer truthfully based on the actual network structure:

1. Upstream Station Query: Ask for the station adjacent to u in the direction of the central hub.
   - If u is not the central hub, answer with its upstream station number (an integer).
   - If u is the central hub, answer "NONE".

2. Downstream Stations Query: Ask for the stations directly adjacent to u in the direction away from the central hub.
   - Answer with the list of all downstream station numbers of u (may be empty).

3. Branch Network Containment Query: Ask whether station x is in the branch network starting at station u (including u itself).
   - If x is in u's branch network, answer "YES".
   - Otherwise answer "NO".

Note: All answers are based solely on the network's local connection structure and do not directly provide level or distance information.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the calculation fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Upstream Station Query (e.g., query upstream station of node 5):
<query_parent>5</query_parent>

- Downstream Stations Query (e.g., query downstream stations of node 3):
<query_children>3</query_children>

- Branch Network Containment Query (e.g., query if the branch of node 2 contains node 7, format is u,x):
<query_subtree>2,7</query_subtree>

When submitting the final answer, provide the section level of the target station (a non-negative integer) in this format:

<answer>5</answer>
"""

    # ==========================================
    # 场景 2：医疗
    # ==========================================
    contextualized_rule_zh_2 = """\
欢迎进入"流行病传播链追踪系统"。

本系统记录了一次呈树状发散的传染病传播事件，已知感染者编号为 1 到 {n}。零号病人（最初感染源）为 {root}，其传播代数定义为 0 代。你需要分析的目标感染者为 {target}。

感染者的传播代数定义为：从零号病人到该感染者的唯一传播路径上的传染次数。

你的任务是推断出目标感染者 {target} 的传播代数。你可以反复向我提出以下三类查询（每次仅限一个查询），我会根据真实的流行病学调查数据如实回答：

1. 传染源查询：询问感染者 u 是被谁直接传染的。
   - 若 u 不是零号病人，回答其传染源编号（一个整数）。
   - 若 u 是零号病人，回答"NONE"。

2. 直接传播对象列表查询：询问感染者 u 直接传染了哪些人。
   - 回答 u 的所有直接传播对象编号列表（可能为空）。

3. 传播链包含关系查询：询问感染者 x 是否在以感染者 u 为起点的后续传播链中（包含 u 本身）。
   - 若 x 在 u 的传播链中，回答"YES"。
   - 否则回答"NO"。

注意：所有回答仅基于局部的传染接触关系，不会直接提供代数或整体路径信息。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，追踪失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 传染源查询（例如查询感染者 5 的传染源）：
<query_parent>5</query_parent>

- 直接传播对象列表查询（例如查询感染者 3 的传播对象）：
<query_children>3</query_children>

- 传播链包含关系查询（例如查询感染者 2 的传播链是否包含感染者 7，格式为 u,x）：
<query_subtree>2,7</query_subtree>

提交最终答案时，直接给出目标感染者的传播代数（一个非负整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_2 = """\
[Medical/Epidemiology Scenario]
Welcome to the "Epidemic Transmission Chain Tracking System".

This system records an infectious disease outbreak that spread in a tree-like structure, with known infected individuals numbered from 1 to {n}. Patient Zero (the initial source) is {root}, and their transmission generation is defined as generation 0. The target infected individual you need to analyze is {target}.

An individual's transmission generation is defined as: the number of infection events on the unique transmission path from Patient Zero to that individual.

Your task is to deduce the transmission generation of the target individual {target}. You can repeatedly ask me three types of queries (one per turn), and I will answer truthfully based on the actual epidemiological investigation data:

1. Source of Infection Query: Ask who directly infected individual u.
   - If u is not Patient Zero, answer with their source's number (an integer).
   - If u is Patient Zero, answer "NONE".

2. Direct Transmittees Query: Ask whom individual u directly infected.
   - Answer with the list of all individual numbers directly infected by u (may be empty).

3. Transmission Chain Containment Query: Ask whether individual x is in the subsequent transmission chain starting from individual u (including u itself).
   - If x is in u's transmission chain, answer "YES".
   - Otherwise answer "NO".

Note: All answers are based solely on local infection contact relationships and do not directly provide generation or overall path information.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the tracking fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Source of Infection Query (e.g., query the source of individual 5):
<query_parent>5</query_parent>

- Direct Transmittees Query (e.g., query the transmittees of individual 3):
<query_children>3</query_children>

- Transmission Chain Containment Query (e.g., query if the transmission chain of individual 2 contains individual 7, format is u,x):
<query_subtree>2,7</query_subtree>

When submitting the final answer, provide the transmission generation of the target individual (a non-negative integer) in this format:

<answer>5</answer>
"""

    # ==========================================
    # 场景 3：教育
    # ==========================================
    contextualized_rule_zh_3 = """\
欢迎进入"学科知识图谱解析系统"。

本系统记录了一个呈严格树形发散的知识体系架构，知识模块编号为 1 到 {n}。核心基础学科模块为 {root}，其知识深度层级定义为 0。你需要评估的目标知识模块为 {target}。

知识模块的深度层级定义为：从核心基础学科到该模块的唯一前置依赖路径上的衍生次数（边数）。

你的任务是推断出目标知识模块 {target} 的深度层级。你可以反复向系统提出以下三类查询（每次仅限一个查询），系统将根据真实的知识图谱结构如实反馈：

1. 前置模块查询：询问知识模块 u 的直接前置（上一级）模块是谁。
   - 若 u 不是核心基础模块，返回其前置模块编号（一个整数）。
   - 若 u 是核心基础模块，返回"NONE"。

2. 衍生细分模块列表查询：询问知识模块 u 有哪些直接衍生的下一级模块。
   - 返回 u 的所有直接衍生模块编号列表（可能为空）。

3. 知识分支包含关系查询：询问模块 x 是否在以模块 u 为起点的知识体系分支中（包含 u 本身）。
   - 若 x 在 u 的知识分支中，返回"YES"。
   - 否则返回"NO"。

注意：所有回答仅基于知识点之间的局部依赖结构，不会直接提供深度或跨度信息。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，解析失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 前置模块查询（例如查询模块 5 的前置模块）：
<query_parent>5</query_parent>

- 衍生细分模块列表查询（例如查询模块 3 的衍生模块）：
<query_children>3</query_children>

- 知识分支包含关系查询（例如查询模块 2 的知识分支是否包含模块 7，格式为 u,x）：
<query_subtree>2,7</query_subtree>

提交最终答案时，直接给出目标知识模块的深度层级（一个非负整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Curriculum Knowledge Graph Parsing System".

This system records a knowledge architecture that diverges in a strict tree structure, with knowledge module numbers ranging from 1 to {n}. The core foundation discipline module is {root}, and its knowledge depth level is defined as 0. The target knowledge module you need to evaluate is {target}.

The depth level of a knowledge module is defined as: the number of derivations (edges) on the unique prerequisite dependency path from the core foundation discipline to that module.

Your task is to deduce the depth level of the target module {target}. You can repeatedly ask the system three types of queries (one per turn), and the system will answer truthfully based on the actual knowledge graph structure:

1. Prerequisite Module Query: Ask which is the direct prerequisite (upstream) module of knowledge module u.
   - If u is not the core foundation module, answer with its prerequisite module number (an integer).
   - If u is the core foundation module, answer "NONE".

2. Derivative Sub-modules Query: Ask what directly derivative downstream modules knowledge module u has.
   - Answer with the list of all direct derivative module numbers of u (may be empty).

3. Knowledge Branch Containment Query: Ask whether module x is in the knowledge system branch starting from module u (including u itself).
   - If x is in u's knowledge branch, answer "YES".
   - Otherwise answer "NO".

Note: All answers are based solely on local dependency structures between knowledge points and do not directly provide depth or span information.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the parsing fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Prerequisite Module Query (e.g., query prerequisite of module 5):
<query_parent>5</query_parent>

- Derivative Sub-modules Query (e.g., query derivatives of module 3):
<query_children>3</query_children>

- Knowledge Branch Containment Query (e.g., query if the branch of module 2 contains module 7, format is u,x):
<query_subtree>2,7</query_subtree>

When submitting the final answer, provide the depth level of the target knowledge module (a non-negative integer) in this format:

<answer>5</answer>
"""

    # ==========================================
    # 场景 4：制造业/工业
    # ==========================================
    contextualized_rule_zh_4 = """\
欢迎使用"产品 BOM (物料清单) 架构分析系统"。

本系统记录了一个呈严格树形发散的复杂产品装配结构，零部件编号为 1 到 {n}。最终总成（顶层产品）为 {root}，其装配层级定义为 0。你需要定位的目标零部件为 {target}。

零部件的装配层级定义为：从最终总成往下分解到该零部件的唯一装配路径上的层级跨度数（边数）。

你的任务是推断出目标零部件 {target} 的装配层级。你可以反复向系统提出以下三类查询（每次仅限一个查询），系统将根据真实的 BOM 结构如实反馈：

1. 所属上级组件查询：询问零部件 u 直接拼装到哪个上级组件中。
   - 若 u 不是最终总成，返回其上级组件编号（一个整数）。
   - 若 u 是最终总成，返回"NONE"。

2. 下级子零件列表查询：询问组件 u 直接包含了哪些下级子零件。
   - 返回 u 直接包含的所有子零件编号列表（可能为空）。

3. 装配子树包含关系查询：询问零部件 x 是否属于以组件 u 为根节点的装配子系统（包含 u 本身）。
   - 若 x 在 u 的装配子系统中，返回"YES"。
   - 否则返回"NO"。

注意：所有回答仅基于局部的装配拆解关系，不会直接提供具体层级或深度信息。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，分析失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 所属上级组件查询（例如查询零部件 5 的上级组件）：
<query_parent>5</query_parent>

- 下级子零件列表查询（例如查询组件 3 的直接子零件）：
<query_children>3</query_children>

- 装配子树包含关系查询（例如查询组件 2 的装配子系统是否包含零部件 7，格式为 u,x）：
<query_subtree>2,7</query_subtree>

提交最终答案时，直接给出目标零部件的装配层级（一个非负整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the "Product BOM Architecture Analysis System".

This system records a complex product assembly structure that diverges in a strict tree form, with component numbers ranging from 1 to {n}. The final assembly (top-level product) is {root}, and its assembly level is defined as 0. The target component you need to locate is {target}.

The assembly level of a component is defined as: the number of level spans (edges) on the unique assembly path breaking down from the final assembly to that component.

Your task is to deduce the assembly level of the target component {target}. You can repeatedly ask the system three types of queries (one per turn), and the system will answer truthfully based on the actual BOM structure:

1. Upstream Component Query: Ask which upstream component the part u is directly assembled into.
   - If u is not the final assembly, answer with its upstream component number (an integer).
   - If u is the final assembly, answer "NONE".

2. Direct Sub-parts Query: Ask which subordinate sub-parts the component u directly includes.
   - Answer with the list of all direct sub-part numbers included in u (may be empty).

3. Assembly Subsystem Containment Query: Ask whether component x belongs to the assembly subsystem rooted at component u (including u itself).
   - If x is in u's assembly subsystem, answer "YES".
   - Otherwise answer "NO".

Note: All answers are based solely on local assembly breakdown relationships and do not directly provide specific level or depth information.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the analysis fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Upstream Component Query (e.g., query upstream component of part 5):
<query_parent>5</query_parent>

- Direct Sub-parts Query (e.g., query direct sub-parts of component 3):
<query_children>3</query_children>

- Assembly Subsystem Containment Query (e.g., query if the assembly subsystem of component 2 contains part 7, format is u,x):
<query_subtree>2,7</query_subtree>

When submitting the final answer, provide the assembly level of the target component (a non-negative integer) in this format:

<answer>5</answer>
"""

    # ==========================================
    # 场景 5：法律
    # ==========================================
    contextualized_rule_zh_5 = """\
欢迎使用"法律法规渊源结构审查系统"。

本系统记录了一个呈严格树形发散的法律条文渊源体系，法条编号为 1 到 {n}。该体系的根本大法（基准法条）为 {root}，其法理层级定义为 0。你需要审查的目标法条为 {target}。

法条的法理层级定义为：从根本大法推演细化到该法条的唯一法理路径上的衍生次数（边数）。

你的任务是推断出目标法条 {target} 的法理层级。你可以反复向系统提出以下三类查询（每次仅限一个查询），系统将根据真实的法律从属结构如实反馈：

1. 上位法查询：询问法条 u 的直接上位法（授权来源）是谁。
   - 若 u 不是根本大法，返回其直接上位法编号（一个整数）。
   - 若 u 是根本大法，返回"NONE"。

2. 下位细则列表查询：询问法条 u 直接授权衍生了哪些下位细则。
   - 返回 u 的所有直接下位法条编号列表（可能为空）。

3. 适用范围包含关系查询：询问法条 x 是否在以法条 u 为法理依据的衍生法律适用范围内（包含 u 本身）。
   - 若 x 在 u 的衍生适用范围内，返回"YES"。
   - 否则返回"NO"。

注意：所有回答仅基于局部的法理授权关系，不会直接提供层级或距离信息。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，审查失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 上位法查询（例如查询法条 5 的上位法）：
<query_parent>5</query_parent>

- 下位细则列表查询（例如查询法条 3 的下位法条）：
<query_children>3</query_children>

- 适用范围包含关系查询（例如查询法条 2 的适用范围是否包含法条 7，格式为 u,x）：
<query_subtree>2,7</query_subtree>

提交最终答案时，直接给出目标法条的法理层级（一个非负整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Legal Provisions Hierarchy Review System".

This system records a hierarchy of legal provisions that diverges in a strict tree form, with provision numbers ranging from 1 to {n}. The fundamental basic law of this system is {root}, and its jurisprudential level is defined as 0. The target legal provision you need to review is {target}.

The jurisprudential level of a provision is defined as: the number of derivations (edges) on the unique jurisprudential path from the basic law to that provision.

Your task is to deduce the jurisprudential level of the target provision {target}. You can repeatedly ask the system three types of queries (one per turn), and the system will answer truthfully based on the actual legal subordination structure:

1. Superior Law Query: Ask what is the direct superior law (source of authorization) of provision u.
   - If u is not the basic law, answer with its direct superior provision number (an integer).
   - If u is the basic law, answer "NONE".

2. Subordinate Rules Query: Ask which subordinate rules were directly authorized and derived by provision u.
   - Answer with the list of all direct subordinate provision numbers of u (may be empty).

3. Application Scope Containment Query: Ask whether provision x falls within the scope of derived laws legally based on provision u (including u itself).
   - If x is in u's derived application scope, answer "YES".
   - Otherwise answer "NO".

Note: All answers are based solely on local jurisprudential authorization relationships and do not directly provide level or distance information.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the review fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Superior Law Query (e.g., query superior law of provision 5):
<query_parent>5</query_parent>

- Subordinate Rules Query (e.g., query subordinate rules of provision 3):
<query_children>3</query_children>

- Application Scope Containment Query (e.g., query if the application scope of provision 2 contains provision 7, format is u,x):
<query_subtree>2,7</query_subtree>

When submitting the final answer, provide the jurisprudential level of the target provision (a non-negative integer) in this format:

<answer>5</answer>
"""

    def _initialize_game(self):
        # 使用基于配置的确定性种子以提高可复现性
        seed = hash((self.config.difficulty, getattr(self.config, 'seed', 42))) % (2**32)
        rng = random.Random(seed)
        
        try:
            difficulty = int(self.config.difficulty)
        except AttributeError:
            difficulty = 1

        if difficulty == 1:
            n = rng.randint(10, 15)
            min_depth = 2
        elif difficulty == 2:
            n = rng.randint(15, 25)
            min_depth = 3
        elif difficulty == 3:
            n = rng.randint(20, 30)
            min_depth = 4
        elif difficulty == 4:
            n = rng.randint(25, 40)
            min_depth = 5
        else:
            n = rng.randint(30, 50)
            min_depth = 6

        for _ in range(100):
            nodes = list(range(1, n + 1))
            rng.shuffle(nodes)
            root = nodes[0]
            
            self.parent_map = {root: "NONE"}
            self.children_map = {node: [] for node in nodes}
            
            added_nodes = [root]
            for node in nodes[1:]:
                parent = rng.choice(added_nodes)
                self.parent_map[node] = parent
                self.children_map[parent].append(node)
                added_nodes.append(node)
                
            self.depth_map = {root: 0}
            queue = [root]
            while queue:
                curr = queue.pop(0)
                for child in self.children_map[curr]:
                    self.depth_map[child] = self.depth_map[curr] + 1
                    queue.append(child)
            
            candidates = [nd for nd in nodes[1:] if self.depth_map[nd] >= min_depth]
            if candidates:
                target = rng.choice(candidates)
                break
        else:
            target = max(nodes[1:], key=lambda nd: self.depth_map[nd])
            
        self.subtree_map = {node: set() for node in nodes}
        def dfs(u):
            self.subtree_map[u].add(u)
            for v in self.children_map[u]:
                self.subtree_map[u].update(dfs(v))
            return self.subtree_map[u]
        dfs(root)
        
        self._game_info = {
            "n": n,
            "root": root,
            "target": target
        }

    def evaluate(self, parsed_info):
        try:
            ans = int(parsed_info.get("answer", -1))
            return ans == self.depth_map[self._game_info["target"]]
        except ValueError:
            return False

    def _cf_core_produce(self, parsed_info):
        if "query_parent" in parsed_info:
            try:
                u = int(parsed_info["query_parent"])
                if u not in self.parent_map:
                    return "Invalid node."
                return str(self.parent_map[u])
            except ValueError:
                return "Invalid format."
                
        if "query_children" in parsed_info:
            try:
                u = int(parsed_info["query_children"])
                if u not in self.children_map:
                    return "Invalid node."
                return str(self.children_map[u])
            except ValueError:
                return "Invalid format."
                
        if "query_subtree" in parsed_info:
            try:
                parts = parsed_info["query_subtree"].split(',')
                if len(parts) != 2:
                    return "Invalid format."
                u = int(parts[0].strip())
                x = int(parts[1].strip())
                if u not in self.subtree_map or x not in self.parent_map:
                    return "Invalid node."
                if x in self.subtree_map[u]:
                    return "YES"
                else:
                    return "NO"
            except ValueError:
                return "Invalid format."
        return "Invalid query."

    def get_all_possible_queries(self):
        queries = []
        for u in self.parent_map.keys():
            query_str = f"<query_parent>{u}</query_parent>"
            answer_str = str(self.parent_map[u])
            queries.append({"query": query_str, "answer": answer_str})
            
            query_str = f"<query_children>{u}</query_children>"
            answer_str = str(self.children_map[u])
            queries.append({"query": query_str, "answer": answer_str})
        
        target = self._game_info["target"]
        root = self._game_info["root"]
        
        # YES cases: ancestors of target
        node = target
        while node != root:
            parent = self.parent_map[node]
            query_str = f"<query_subtree>{parent},{target}</query_subtree>"
            answer_str = "YES"
            queries.append({"query": query_str, "answer": answer_str})
            node = parent
        
        # NO cases: pick some nodes that are NOT ancestors of target
        ancestors = set()
        node = target
        while node != root:
            node = self.parent_map[node]
            ancestors.add(node)
        ancestors.add(root)
        
        non_ancestors = [nd for nd in self.parent_map if nd not in ancestors and nd != target]
        # Add a few NO subtree queries for diversity
        for nd in non_ancestors[:min(5, len(non_ancestors))]:
            if target not in self.subtree_map.get(nd, set()):
                query_str = f"<query_subtree>{nd},{target}</query_subtree>"
                answer_str = "NO"
                queries.append({"query": query_str, "answer": answer_str})
        
        return queries

    def _cf_make_wrong(self, correct):
        if correct == "YES":
            return "NO"
        elif correct == "NO":
            return "YES"
        elif correct == "NONE":
            for node in self.parent_map:
                if node != self._game_info["root"]:
                    return str(node)
            return "1"
        elif correct.startswith("["):
            if correct == "[]":
                some_node = self._game_info["target"]
                return f"[{some_node}]"
            else:
                return "[]"
        else:
            try:
                correct_int = int(correct)
                for node in self.parent_map:
                    if node != correct_int:
                        return str(node)
            except ValueError:
                pass
            return "1" if correct != "1" else "2"