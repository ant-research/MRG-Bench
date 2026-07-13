# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   节点深度：某给定节点位于树的第几层
# ============================================================

from .base import Game
import random


class TreeNodeDepthInferenceGame(Game):

    # [BUG FIX] 原问题：字符串包含 {depth_value}，base.py 调用 .format() 时将其误认为是待替换变量，导致 KeyError: 'depth_value'。
    # 修改：将 {depth_value} 转义为 {{depth_value}}，使其在 format 后保持为原义字符。
    game_rule_zh = """\
我们现在来玩一个"树节点深度推断"的游戏，规则如下：

游戏设定了一棵固定的有根树，节点由唯一ID标识（如 A, B, C 等）。根节点的深度为 0，任意节点的深度定义为从根到该节点的路径长度。

存在一个未知但固定的函数 f，它将节点深度映射到一个正整数响应值。该函数对所有节点一致，仅依赖节点深度，且严格递增（深度越大，响应值越大）。每个节点 X 关联一个响应值 m(X) 等于 f(该节点深度)。

游戏指定了一个目标节点 T。你的任务是推断出目标节点 T 的深度。

你可以进行以下查询：

**对所有节点可用的查询：**
1. 测量查询：查询节点 X 的响应值 m(X)。
2. 比较查询：比较节点 X 和 Y 的响应值大小关系。

**仅对非目标节点可用的结构查询（对目标节点 T 使用将被拒绝）：**
3. 列出节点：获取所有节点ID列表。
4. 父节点查询：查询节点 X 的父节点ID。
5. 子节点查询：查询节点 X 的所有子节点ID列表。
6. 根节点判断：判断节点 X 是否为根节点。

注意：对目标节点 T，除了测量和比较查询外，任何结构查询都将被拒绝。

## 查询与提交答案的格式（必须严格遵守）

每次只能进行一个查询。请使用以下 XML 格式：

- 列出所有节点（内容为空）：
<query_list_nodes></query_list_nodes>

- 测量查询（例如查询节点 A）：
<query_measure>A</query_measure>

- 比较查询（例如比较节点 A 和 B）：
<query_compare>A,B</query_compare>

- 父节点查询（例如查询节点 B 的父节点）：
<query_parent>B</query_parent>

- 子节点查询（例如查询节点 A 的子节点）：
<query_children>A</query_children>

- 根节点判断（例如判断节点 A 是否为根）：
<query_is_root>A</query_is_root>

提交最终答案时，必须说明目标节点 T 的深度（一个非负整数），格式如下：

<answer>depth={{depth_value}}</answer>

例如：
<answer>depth=3</answer>
"""

    game_rule_en = """\
Let's play a "Tree Node Depth Inference" game. Here are the rules:

The game features a fixed rooted tree with nodes identified by unique IDs (such as A, B, C, etc.). The root node has depth 0, and the depth of any node is defined as the length of the path from the root to that node.

There exists an unknown but fixed function f that maps node depth to a positive integer response value. This function is consistent across all nodes, depends only on node depth, and is strictly increasing (greater depth yields greater response value). Each node X is associated with a response value m(X) equal to f(depth of X).

The game specifies a target node T. Your task is to infer the depth of target node T.

You can perform the following queries:

**Queries available for all nodes:**
1. Measure query: Query the response value m(X) of node X.
2. Compare query: Compare the response values of nodes X and Y.

**Structure queries available only for non-target nodes (will be rejected for target node T):**
3. List nodes: Get the list of all node IDs.
4. Parent query: Query the parent node ID of node X.
5. Children query: Query the list of all children node IDs of node X.
6. Root check: Check whether node X is the root node.

Note: For target node T, any structure query except measure and compare will be rejected.

## Query and Answer Format (must be strictly followed)

Each turn allows only one query. Use the following XML format:

- List all nodes (empty content):
<query_list_nodes></query_list_nodes>

- Measure query (e.g., query node A):
<query_measure>A</query_measure>

- Compare query (e.g., compare nodes A and B):
<query_compare>A,B</query_compare>

- Parent query (e.g., query parent of node B):
<query_parent>B</query_parent>

- Children query (e.g., query children of node A):
<query_children>A</query_children>

- Root check (e.g., check if node A is root):
<query_is_root>A</query_is_root>

When submitting the final answer, specify the depth of target node T (a non-negative integer) using this format:

<answer>depth={{depth_value}}</answer>

For example:
<answer>depth=3</answer>
"""

    # 场景 1：交通
    contextualized_rule_zh_1 = """\
欢迎进入“城市交通调度网层级推断”系统。

系统设定了一个固定的呈树状辐射的公共交通调度网，每个调度节点（枢纽/路口）由唯一ID标识（如 A, B, C 等）。总调度中心（根节点）的层级深度为 0，任意节点的深度定义为从总中心到该节点的通讯链路跳数。

存在一个未知的信号衰减函数 f，它将节点深度映射为一个正整数的“信号传输延迟值”作为响应值。该函数对所有节点一致，仅依赖节点深度，且严格递增（层级越深，延迟越大）。每个节点 X 关联一个响应值 m(X) 等于 f(该节点深度)。

系统指定了一个发生异常的目标节点 T。你的任务是推断出该目标节点 T 的深度层级。

你可以进行以下查询：

**对所有节点可用的查询：**
1. 测量查询：查询节点 X 的延迟响应值 m(X)。
2. 比较查询：比较节点 X 和 Y 的延迟响应值大小关系。

**仅对非目标节点可用的结构查询（对异常目标节点 T 使用将被拒绝）：**
3. 列出节点：获取所有调度节点ID列表。
4. 父节点查询：查询节点 X 的直属上级节点ID。
5. 子节点查询：查询节点 X 的所有直属下级节点ID列表。
6. 根节点判断：判断节点 X 是否为总调度中心（根节点）。

注意：对目标节点 T，除了测量和比较查询外，任何结构查询都将被拒绝。

## 查询与提交答案的格式（必须严格遵守）

每次只能进行一个查询。请使用以下 XML 格式：

- 列出所有节点（内容为空）：
<query_list_nodes></query_list_nodes>

- 测量查询（例如测量枢纽 A 的延迟）：
<query_measure>A</query_measure>

- 比较查询（例如比较枢纽 A 和 B）：
<query_compare>A,B</query_compare>

- 父节点查询（例如查询枢纽 B 的上级）：
<query_parent>B</query_parent>

- 子节点查询（例如查询枢纽 A 的下级）：
<query_children>A</query_children>

- 根节点判断（例如判断枢纽 A 是否为总控中心）：
<query_is_root>A</query_is_root>

提交最终答案时，必须说明目标节点 T 的深度（一个非负整数），格式如下：

<answer>depth={{depth_value}}</answer>

例如：
<answer>depth=3</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Traffic Dispatch Network Tier Inference" system.

The system features a fixed public transit dispatch network radiating like a rooted tree, with dispatch nodes (hubs/intersections) identified by unique IDs (such as A, B, C, etc.). The central dispatch hub (root node) has a tier depth of 0, and the depth of any node is defined as the number of communication hops from the central hub to that node.

There exists an unknown but fixed function f that maps node depth to a positive integer "signal transmission delay" response value. This function is consistent across all nodes, depends only on node depth, and is strictly increasing (deeper depth yields greater delay). Each node X is associated with a response value m(X) equal to f(depth of X).

The system specifies an anomalous target node T. Your task is to infer the tier depth of target node T.

You can perform the following queries:

**Queries available for all nodes:**
1. Measure query: Query the delay response value m(X) of node X.
2. Compare query: Compare the delay response values of nodes X and Y.

**Structure queries available only for non-target nodes (will be rejected for target node T):**
3. List nodes: Get the list of all node IDs.
4. Parent query: Query the direct upstream (parent) node ID of node X.
5. Children query: Query the list of all direct downstream (children) node IDs of node X.
6. Root check: Check whether node X is the central hub (root node).

Note: For target node T, any structure query except measure and compare will be rejected.

## Query and Answer Format (must be strictly followed)

Each turn allows only one query. Use the following XML format:

- List all nodes (empty content):
<query_list_nodes></query_list_nodes>

- Measure query (e.g., query delay of hub A):
<query_measure>A</query_measure>

- Compare query (e.g., compare hubs A and B):
<query_compare>A,B</query_compare>

- Parent query (e.g., query parent of hub B):
<query_parent>B</query_parent>

- Children query (e.g., query children of hub A):
<query_children>A</query_children>

- Root check (e.g., check if hub A is the central hub):
<query_is_root>A</query_is_root>

When submitting the final answer, specify the depth of target node T (a non-negative integer) using this format:

<answer>depth={{depth_value}}</answer>

For example:
<answer>depth=3</answer>
"""

    # 场景 2：医疗
    contextualized_rule_zh_2 = """\
欢迎使用“疾病传染演化树溯源”分析工具。

系统建模了一棵固定的病毒演化/感染追踪有根树，每位患者/医疗追踪点由唯一ID标识（如 A, B, C 等）。零号病人（根节点）的感染代数深度为 0，任意患者的深度定义为从零号病人传播到该患者的感染代数。

存在一个未知但固定的函数 f，它将感染深度映射为一个正整数的“病毒变异标记物浓度”响应值。该函数对所有感染者一致，仅依赖感染代数深度，且严格递增（传播代数越深，标记物浓度越高）。每位患者 X 关联一个响应浓度 m(X) 等于 f(该患者深度)。

系统锁定了一个确诊的目标患者 T。你的任务是推断出目标患者 T 的感染代数（即深度）。

你可以进行以下查询：

**对所有患者可用的查询：**
1. 测量查询：查询患者 X 的标记物浓度响应值 m(X)。
2. 比较查询：比较患者 X 和 Y 的标记物浓度大小关系。

**仅对非目标患者可用的结构查询（由于隐私保护，对目标患者 T 使用将被拒绝）：**
3. 列出节点：获取所有收录的患者ID列表。
4. 父节点查询：查询患者 X 的直接传染源（父节点）ID。
5. 子节点查询：查询患者 X 传染的所有二代病例（子节点）ID列表。
6. 根节点判断：判断患者 X 是否为零号病人（根节点）。

注意：对目标患者 T，除了测量和比较查询外，任何结构查询都将被拒绝。

## 查询与提交答案的格式（必须严格遵守）

每次只能进行一个查询。请使用以下 XML 格式：

- 列出所有节点（内容为空）：
<query_list_nodes></query_list_nodes>

- 测量查询（例如测量患者 A 的浓度）：
<query_measure>A</query_measure>

- 比较查询（例如比较患者 A 和 B）：
<query_compare>A,B</query_compare>

- 父节点查询（例如查询患者 B 的传染源）：
<query_parent>B</query_parent>

- 子节点查询（例如查询患者 A 的被传染者）：
<query_children>A</query_children>

- 根节点判断（例如判断患者 A 是否为零号病人）：
<query_is_root>A</query_is_root>

提交最终答案时，必须说明目标患者 T 的感染代数深度（一个非负整数），格式如下：

<answer>depth={{depth_value}}</answer>

例如：
<answer>depth=3</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Infectious Disease Evolution Tree Tracing" analysis tool.

The system models a fixed rooted tree for virus evolution and infection tracking, with each patient/tracking node identified by a unique ID (such as A, B, C, etc.). Patient Zero (the root node) has an infection generation depth of 0, and the depth of any patient is defined as the number of transmission generations from Patient Zero.

There exists an unknown but fixed function f that maps infection depth to a positive integer "viral mutation marker concentration" response value. This function is consistent across all patients, depends only on the infection generation depth, and is strictly increasing (deeper transmission generations yield higher marker concentration). Each patient X is associated with a response concentration m(X) equal to f(depth of X).

The system has locked onto a confirmed target patient T. Your task is to infer the infection generation depth of target patient T.

You can perform the following queries:

**Queries available for all patients:**
1. Measure query: Query the marker concentration response value m(X) of patient X.
2. Compare query: Compare the marker concentration values of patients X and Y.

**Structure queries available only for non-target patients (will be rejected for target patient T due to privacy protocols):**
3. List nodes: Get the list of all recorded patient IDs.
4. Parent query: Query the direct infection source (parent node) ID of patient X.
5. Children query: Query the list of all secondary cases (children node) IDs infected by patient X.
6. Root check: Check whether patient X is Patient Zero (root node).

Note: For target patient T, any structure query except measure and compare will be rejected.

## Query and Answer Format (must be strictly followed)

Each turn allows only one query. Use the following XML format:

- List all nodes (empty content):
<query_list_nodes></query_list_nodes>

- Measure query (e.g., query concentration of patient A):
<query_measure>A</query_measure>

- Compare query (e.g., compare patients A and B):
<query_compare>A,B</query_compare>

- Parent query (e.g., query infection source of patient B):
<query_parent>B</query_parent>

- Children query (e.g., query secondary cases of patient A):
<query_children>A</query_children>

- Root check (e.g., check if patient A is Patient Zero):
<query_is_root>A</query_is_root>

When submitting the final answer, specify the infection generation depth of target patient T (a non-negative integer) using this format:

<answer>depth={{depth_value}}</answer>

For example:
<answer>depth=3</answer>
"""

    # 场景 3：教育
    contextualized_rule_zh_3 = """\
欢迎进入“知识图谱前置依赖网络”评估系统。

本系统包含一棵固定的知识体系前置依赖有根树，每门课程/知识模块由唯一ID标识（如 A, B, C 等）。核心基座课程（根节点）的学习阶段深度为 0，任意课程的深度定义为从基础模块到该课程的先修链阶段数。

存在一个未知的认知评估函数 f，它将课程深度映射为一个正整数的“认知负荷指数”响应值。该函数对所有课程一致，仅依赖学习阶段深度，且严格递增（先修链越长，认知负荷越大）。每门课程 X 关联一个响应指数 m(X) 等于 f(该课程深度)。

教务系统指定了一门待评估的新增目标课程 T。你的任务是推断出该目标课程 T 的所处阶段深度。

你可以进行以下查询：

**对所有课程可用的查询：**
1. 测量查询：查询课程 X 的认知负荷响应值 m(X)。
2. 比较查询：比较课程 X 和 Y 的认知负荷指数大小关系。

**仅对非目标课程可用的结构查询（对待评估的目标课程 T 暂不开放）：**
3. 列出节点：获取所有课程模块ID列表。
4. 父节点查询：查询课程 X 的直接先修课程（父节点）ID。
5. 子节点查询：查询以课程 X 为直接先修课的所有后续课程（子节点）ID列表。
6. 根节点判断：判断课程 X 是否为核心基座课程（根节点）。

注意：对目标课程 T，除了测量和比较查询外，任何结构查询都将被拒绝。

## 查询与提交答案的格式（必须严格遵守）

每次只能进行一个查询。请使用以下 XML 格式：

- 列出所有节点（内容为空）：
<query_list_nodes></query_list_nodes>

- 测量查询（例如测量课程 A 的认知负荷）：
<query_measure>A</query_measure>

- 比较查询（例如比较课程 A 和 B）：
<query_compare>A,B</query_compare>

- 父节点查询（例如查询课程 B 的先修课）：
<query_parent>B</query_parent>

- 子节点查询（例如查询课程 A 的后续课）：
<query_children>A</query_children>

- 根节点判断（例如判断课程 A 是否为基座课）：
<query_is_root>A</query_is_root>

提交最终答案时，必须说明目标课程 T 的阶段深度（一个非负整数），格式如下：

<answer>depth={{depth_value}}</answer>

例如：
<answer>depth=3</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Knowledge Graph Prerequisite Dependency Network" assessment system.

This system features a fixed rooted tree representing a prerequisite dependency network, with each course/knowledge module identified by a unique ID (such as A, B, C, etc.). The core foundation course (root node) has a learning stage depth of 0, and the depth of any course is defined as the number of prerequisite chain stages from the foundation to that course.

There exists an unknown but fixed cognitive assessment function f that maps course depth to a positive integer "cognitive load index" response value. This function is consistent across all courses, depends only on the learning stage depth, and is strictly increasing (longer prerequisite chains yield greater cognitive load). Each course X is associated with a response index m(X) equal to f(depth of X).

The academic system has designated a newly added target course T for assessment. Your task is to infer the stage depth of target course T.

You can perform the following queries:

**Queries available for all courses:**
1. Measure query: Query the cognitive load response value m(X) of course X.
2. Compare query: Compare the cognitive load index of courses X and Y.

**Structure queries available only for non-target courses (currently restricted for the assessed target course T):**
3. List nodes: Get the list of all course module IDs.
4. Parent query: Query the direct prerequisite course (parent node) ID of course X.
5. Children query: Query the list of all subsequent course (children node) IDs that require course X as a direct prerequisite.
6. Root check: Check whether course X is the core foundation course (root node).

Note: For target course T, any structure query except measure and compare will be rejected.

## Query and Answer Format (must be strictly followed)

Each turn allows only one query. Use the following XML format:

- List all nodes (empty content):
<query_list_nodes></query_list_nodes>

- Measure query (e.g., query cognitive load of course A):
<query_measure>A</query_measure>

- Compare query (e.g., compare courses A and B):
<query_compare>A,B</query_compare>

- Parent query (e.g., query prerequisite of course B):
<query_parent>B</query_parent>

- Children query (e.g., query subsequent courses of course A):
<query_children>A</query_children>

- Root check (e.g., check if course A is a foundation course):
<query_is_root>A</query_is_root>

When submitting the final answer, specify the stage depth of target course T (a non-negative integer) using this format:

<answer>depth={{depth_value}}</answer>

For example:
<answer>depth=3</answer>
"""

    # 场景 4：制造业/工业
    contextualized_rule_zh_4 = """\
欢迎进入“产品BOM结构层级推断”诊断系统。

系统设定了一棵固定的产品BOM（物料清单）拆解有根树，每个装配组件/底层零件由唯一ID标识（如 A, B, C 等）。最终总装成品（根节点）的拆解层级深度为 0，任意零件的深度定义为从成品拆解到该零件所需的级数。

存在一个未知但固定的加工容错函数 f，它将零件深度映射为一个正整数的“累计加工公差”响应值。该函数对所有组件一致，仅依赖拆解层级深度，且严格递增（所处拆解层级越深，累积加工公差越大）。每个零件 X 关联一个响应公差 m(X) 等于 f(该零件深度)。

质检流程中发现了一个存在隐患的目标零件 T。你的任务是推断出目标零件 T 所在的拆解层级深度。

你可以进行以下查询：

**对所有零件可用的查询：**
1. 测量查询：测定零件 X 的累计公差响应值 m(X)。
2. 比较查询：比较零件 X 和 Y 的累计公差大小关系。

**仅对非目标零件可用的结构查询（由于目标零件 T 图纸受限，对其使用将被拒绝）：**
3. 列出节点：获取所有产品BOM节点的ID列表。
4. 父节点查询：查询零件 X 的直属上游装配体（父节点）ID。
5. 子节点查询：查询装配体 X 的所有下级组成零件（子节点）ID列表。
6. 根节点判断：判断节点 X 是否为最终总装成品（根节点）。

注意：对目标零件 T，除了测量和比较查询外，任何结构查询都将被拒绝。

## 查询与提交答案的格式（必须严格遵守）

每次只能进行一个查询。请使用以下 XML 格式：

- 列出所有节点（内容为空）：
<query_list_nodes></query_list_nodes>

- 测量查询（例如测量零件 A 的公差）：
<query_measure>A</query_measure>

- 比较查询（例如比较零件 A 和 B）：
<query_compare>A,B</query_compare>

- 父节点查询（例如查询零件 B 的上游装配）：
<query_parent>B</query_parent>

- 子节点查询（例如查询组件 A 的下级零件）：
<query_children>A</query_children>

- 根节点判断（例如判断节点 A 是否为最终成品）：
<query_is_root>A</query_is_root>

提交最终答案时，必须说明目标零件 T 的层级深度（一个非负整数），格式如下：

<answer>depth={{depth_value}}</answer>

例如：
<answer>depth=3</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the "Product BOM Structure Tier Inference" diagnostic system.

The system features a fixed product BOM (Bill of Materials) rooted disassembly tree, with each assembly component/underlying part identified by a unique ID (such as A, B, C, etc.). The final assembled product (root node) has a disassembly tier depth of 0, and the depth of any part is defined as the number of disassembly steps from the final product to that part.

There exists an unknown but fixed machining tolerance function f that maps part depth to a positive integer "cumulative machining tolerance" response value. This function is consistent across all components, depends only on the disassembly tier depth, and is strictly increasing (deeper disassembly tier yields greater cumulative tolerance). Each part X is associated with a response tolerance m(X) equal to f(depth of X).

The quality inspection process has identified a target part T containing hidden defects. Your task is to infer the disassembly tier depth of target part T.

You can perform the following queries:

**Queries available for all parts:**
1. Measure query: Measure the cumulative tolerance response value m(X) of part X.
2. Compare query: Compare the cumulative tolerance values of parts X and Y.

**Structure queries available only for non-target parts (will be rejected for target part T due to restricted blueprints):**
3. List nodes: Get the list of all product BOM node IDs.
4. Parent query: Query the direct upstream assembly (parent node) ID of part X.
5. Children query: Query the list of all direct sub-component (children node) IDs of assembly X.
6. Root check: Check whether node X is the final assembled product (root node).

Note: For target part T, any structure query except measure and compare will be rejected.

## Query and Answer Format (must be strictly followed)

Each turn allows only one query. Use the following XML format:

- List all nodes (empty content):
<query_list_nodes></query_list_nodes>

- Measure query (e.g., query tolerance of part A):
<query_measure>A</query_measure>

- Compare query (e.g., compare parts A and B):
<query_compare>A,B</query_compare>

- Parent query (e.g., query upstream assembly of part B):
<query_parent>B</query_parent>

- Children query (e.g., query sub-components of assembly A):
<query_children>A</query_children>

- Root check (e.g., check if node A is the final product):
<query_is_root>A</query_is_root>

When submitting the final answer, specify the tier depth of target part T (a non-negative integer) using this format:

<answer>depth={{depth_value}}</answer>

For example:
<answer>depth=3</answer>
"""

    # 场景 5：法律
    contextualized_rule_zh_5 = """\
欢迎使用“企业股权穿透与层级评估”分析工具。

系统展示了一棵固定的公司股权穿透有根树，每家实体企业/壳公司由唯一ID标识（如 A, B, C 等）。最终控股集团母公司（根节点）的投资层级深度为 0，任意公司的深度定义为从母公司到该实体的股权代数。

存在一个未知但固定的行政职能函数 f，它将公司投资深度映射为一个正整数的“行政审批耗时指数”响应值。该函数对所有注册公司一致，仅依赖投资层级深度，且严格递增（股权结构越深，审批耗时指数越大）。每家公司 X 关联一个响应指数 m(X) 等于 f(该公司的层级深度)。

经侦部门锁定了一家涉案的目标空壳公司 T。你的任务是推断出该目标公司 T 隐藏在股权网络中的层级深度。

你可以进行以下查询：

**对所有公司可用的查询：**
1. 测量查询：评估公司 X 的耗时指数响应值 m(X)。
2. 比较查询：比较公司 X 和 Y 的耗时指数大小关系。

**仅对非目标公司可用的结构查询（由于目标公司 T 账目冻结，对其穿透查询将被拒绝）：**
3. 列出节点：获取工商名录中所有公司ID的列表。
4. 父节点查询：查询公司 X 的直接控股股东（父节点）ID。
5. 子节点查询：查询公司 X 旗下直接投资的所有子公司（子节点）ID列表。
6. 根节点判断：判断公司 X 是否为最终控股集团（根节点）。

注意：对目标公司 T，除了测量和比较查询外，任何结构查询都将被拒绝。

## 查询与提交答案的格式（必须严格遵守）

每次只能进行一个查询。请使用以下 XML 格式：

- 列出所有节点（内容为空）：
<query_list_nodes></query_list_nodes>

- 测量查询（例如评估公司 A 的耗时指数）：
<query_measure>A</query_measure>

- 比较查询（例如比较公司 A 和 B）：
<query_compare>A,B</query_compare>

- 父节点查询（例如查询公司 B 的控股股东）：
<query_parent>B</query_parent>

- 子节点查询（例如查询公司 A 的子公司）：
<query_children>A</query_children>

- 根节点判断（例如判断公司 A 是否为集团母公司）：
<query_is_root>A</query_is_root>

提交最终答案时，必须说明目标公司 T 的层级深度（一个非负整数），格式如下：

<answer>depth={{depth_value}}</answer>

例如：
<answer>depth=3</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Corporate Equity Penetration and Tier Assessment" analysis tool.

The system displays a fixed rooted tree representing corporate equity penetration, with each business entity/shell company identified by a unique ID (such as A, B, C, etc.). The ultimate holding group (root node) has an investment tier depth of 0, and the depth of any company is defined as the number of equity generations from the holding group to that entity.

There exists an unknown but fixed administrative function f that maps company investment depth to a positive integer "administrative approval time index" response value. This function is consistent across all registered companies, depends only on the investment tier depth, and is strictly increasing (deeper equity structure yields greater approval time index). Each company X is associated with a response index m(X) equal to f(depth of X).

The economic investigation department has locked onto an involved target shell company T. Your task is to infer the tier depth of target company T hidden within the equity network.

You can perform the following queries:

**Queries available for all companies:**
1. Measure query: Assess the time index response value m(X) of company X.
2. Compare query: Compare the time index values of companies X and Y.

**Structure queries available only for non-target companies (penetration queries will be rejected for target company T due to frozen accounts):**
3. List nodes: Get the list of all company IDs in the registry.
4. Parent query: Query the direct controlling shareholder (parent node) ID of company X.
5. Children query: Query the list of all direct subsidiary (children node) IDs invested in by company X.
6. Root check: Check whether company X is the ultimate holding group (root node).

Note: For target company T, any structure query except measure and compare will be rejected.

## Query and Answer Format (must be strictly followed)

Each turn allows only one query. Use the following XML format:

- List all nodes (empty content):
<query_list_nodes></query_list_nodes>

- Measure query (e.g., assess time index of company A):
<query_measure>A</query_measure>

- Compare query (e.g., compare companies A and B):
<query_compare>A,B</query_compare>

- Parent query (e.g., query controlling shareholder of company B):
<query_parent>B</query_parent>

- Children query (e.g., query subsidiaries of company A):
<query_children>A</query_children>

- Root check (e.g., check if company A is the holding group):
<query_is_root>A</query_is_root>

When submitting the final answer, specify the tier depth of target company T (a non-negative integer) using this format:

<answer>depth={{depth_value}}</answer>

For example:
<answer>depth=3</answer>
"""

    tags = ["answer", "query_list_nodes", "query_measure", "query_compare", 
            "query_parent", "query_children", "query_is_root"]
    
    # 新增类属性
    reasoning_type = "归纳推理"
    data_structure = "树"

    # 难度说明：
    # 1 (简单)       - 小树，深度较浅，函数简单
    # 2 (中等偏下)   - 中等树，深度适中
    # 3 (中等偏上)   - 较大树，深度较深
    # 4 (较难)       - 大树，深度更深，结构复杂
    # 5 (难)         - 最大树，最深深度，结构最复杂

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                # 树结构: A(根) -> B, C; B -> D
                # 深度: A=0, B=1, C=1, D=2
                "tree": {
                    "A": {"parent": None, "children": ["B", "C"]},
                    "B": {"parent": "A", "children": ["D"]},
                    "C": {"parent": "A", "children": []},
                    "D": {"parent": "B", "children": []},
                },
                "target": "D",
                "depth_function": lambda d: d * 10 + 5,  # 5, 15, 25, ...
            },
            2: {
                # 树结构: A -> B, C; B -> D, E; C -> F
                # 深度: A=0, B=1, C=1, D=2, E=2, F=2
                "tree": {
                    "A": {"parent": None, "children": ["B", "C"]},
                    "B": {"parent": "A", "children": ["D", "E"]},
                    "C": {"parent": "A", "children": ["F"]},
                    "D": {"parent": "B", "children": []},
                    "E": {"parent": "B", "children": []},
                    "F": {"parent": "C", "children": []},
                },
                "target": "F",
                "depth_function": lambda d: d * d + 10,  # 10, 11, 14, 19, ...
            },
            3: {
                # 树结构: A -> B, C; B -> D, E; D -> G, H; C -> F; F -> I
                # 深度: A=0, B=1, C=1, D=2, E=2, F=2, G=3, H=3, I=3
                "tree": {
                    "A": {"parent": None, "children": ["B", "C"]},
                    "B": {"parent": "A", "children": ["D", "E"]},
                    "C": {"parent": "A", "children": ["F"]},
                    "D": {"parent": "B", "children": ["G", "H"]},
                    "E": {"parent": "B", "children": []},
                    "F": {"parent": "C", "children": ["I"]},
                    "G": {"parent": "D", "children": []},
                    "H": {"parent": "D", "children": []},
                    "I": {"parent": "F", "children": []},
                },
                "target": "H",
                "depth_function": lambda d: 2 ** d + d,  # 1, 3, 6, 11, 20, ...
            },
            4: {
                # 树结构: A -> B, C; B -> D, E; C -> F, G; D -> H, I; E -> J; G -> K, L
                # 深度: A=0, B=1, C=1, D=2, E=2, F=2, G=2, H=3, I=3, J=3, K=3, L=3
                "tree": {
                    "A": {"parent": None, "children": ["B", "C"]},
                    "B": {"parent": "A", "children": ["D", "E"]},
                    "C": {"parent": "A", "children": ["F", "G"]},
                    "D": {"parent": "B", "children": ["H", "I"]},
                    "E": {"parent": "B", "children": ["J"]},
                    "F": {"parent": "C", "children": []},
                    "G": {"parent": "C", "children": ["K", "L"]},
                    "H": {"parent": "D", "children": []},
                    "I": {"parent": "D", "children": []},
                    "J": {"parent": "E", "children": []},
                    "K": {"parent": "G", "children": []},
                    "L": {"parent": "G", "children": []},
                },
                "target": "K",
                "depth_function": lambda d: d * d * 2 + d + 7,  # 7, 10, 17, 28, 43, ...
            },
            5: {
                # 树结构: 更复杂的树，深度到4
                # A -> B, C; B -> D, E; C -> F, G; D -> H, I; E -> J, K; G -> L, M; 
                # H -> N; I -> O; L -> P, Q
                # 深度: A=0, B=1, C=1, D=2, E=2, F=2, G=2, H=3, I=3, J=3, K=3, L=3, M=3,
                #       N=4, O=4, P=4, Q=4
                "tree": {
                    "A": {"parent": None, "children": ["B", "C"]},
                    "B": {"parent": "A", "children": ["D", "E"]},
                    "C": {"parent": "A", "children": ["F", "G"]},
                    "D": {"parent": "B", "children": ["H", "I"]},
                    "E": {"parent": "B", "children": ["J", "K"]},
                    "F": {"parent": "C", "children": []},
                    "G": {"parent": "C", "children": ["L", "M"]},
                    "H": {"parent": "D", "children": ["N"]},
                    "I": {"parent": "D", "children": ["O"]},
                    "J": {"parent": "E", "children": []},
                    "K": {"parent": "E", "children": []},
                    "L": {"parent": "G", "children": ["P", "Q"]},
                    "M": {"parent": "G", "children": []},
                    "N": {"parent": "H", "children": []},
                    "O": {"parent": "I", "children": []},
                    "P": {"parent": "L", "children": []},
                    "Q": {"parent": "L", "children": []},
                },
                "target": "P",
                "depth_function": lambda d: d * d * d + 5,  # 5, 6, 13, 32, 69, ...
            },
        },
        "en": {
            1: {
                "tree": {
                    "A": {"parent": None, "children": ["B", "C"]},
                    "B": {"parent": "A", "children": ["D"]},
                    "C": {"parent": "A", "children": []},
                    "D": {"parent": "B", "children": []},
                },
                "target": "D",
                "depth_function": lambda d: d * 10 + 5,
            },
            2: {
                "tree": {
                    "A": {"parent": None, "children": ["B", "C"]},
                    "B": {"parent": "A", "children": ["D", "E"]},
                    "C": {"parent": "A", "children": ["F"]},
                    "D": {"parent": "B", "children": []},
                    "E": {"parent": "B", "children": []},
                    "F": {"parent": "C", "children": []},
                },
                "target": "F",
                "depth_function": lambda d: d * d + 10,
            },
            3: {
                "tree": {
                    "A": {"parent": None, "children": ["B", "C"]},
                    "B": {"parent": "A", "children": ["D", "E"]},
                    "C": {"parent": "A", "children": ["F"]},
                    "D": {"parent": "B", "children": ["G", "H"]},
                    "E": {"parent": "B", "children": []},
                    "F": {"parent": "C", "children": ["I"]},
                    "G": {"parent": "D", "children": []},
                    "H": {"parent": "D", "children": []},
                    "I": {"parent": "F", "children": []},
                },
                "target": "H",
                "depth_function": lambda d: 2 ** d + d,
            },
            4: {
                "tree": {
                    "A": {"parent": None, "children": ["B", "C"]},
                    "B": {"parent": "A", "children": ["D", "E"]},
                    "C": {"parent": "A", "children": ["F", "G"]},
                    "D": {"parent": "B", "children": ["H", "I"]},
                    "E": {"parent": "B", "children": ["J"]},
                    "F": {"parent": "C", "children": []},
                    "G": {"parent": "C", "children": ["K", "L"]},
                    "H": {"parent": "D", "children": []},
                    "I": {"parent": "D", "children": []},
                    "J": {"parent": "E", "children": []},
                    "K": {"parent": "G", "children": []},
                    "L": {"parent": "G", "children": []},
                },
                "target": "K",
                "depth_function": lambda d: d * d * 2 + d + 7,
            },
            5: {
                "tree": {
                    "A": {"parent": None, "children": ["B", "C"]},
                    "B": {"parent": "A", "children": ["D", "E"]},
                    "C": {"parent": "A", "children": ["F", "G"]},
                    "D": {"parent": "B", "children": ["H", "I"]},
                    "E": {"parent": "B", "children": ["J", "K"]},
                    "F": {"parent": "C", "children": []},
                    "G": {"parent": "C", "children": ["L", "M"]},
                    "H": {"parent": "D", "children": ["N"]},
                    "I": {"parent": "D", "children": ["O"]},
                    "J": {"parent": "E", "children": []},
                    "K": {"parent": "E", "children": []},
                    "L": {"parent": "G", "children": ["P", "Q"]},
                    "M": {"parent": "G", "children": []},
                    "N": {"parent": "H", "children": []},
                    "O": {"parent": "I", "children": []},
                    "P": {"parent": "L", "children": []},
                    "Q": {"parent": "L", "children": []},
                },
                "target": "P",
                "depth_function": lambda d: d * d * d + 5,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 保存树结构
        self.tree = cfg["tree"]
        self.target_node = cfg["target"]
        self.depth_function = cfg["depth_function"]
        
        # 计算所有节点的深度
        self.node_depths = {}
        self._compute_depths()
        
        # 计算所有节点的响应值
        self.node_responses = {}
        for node, depth in self.node_depths.items():
            self.node_responses[node] = self.depth_function(depth)
        
        # 获取目标节点深度（正确答案）
        self.target_depth = self.node_depths[self.target_node]
        
        # 游戏信息（用于格式化规则文本，如有需要）
        self._game_info = {}

    def _compute_depths(self):
        """计算所有节点的深度"""
        # 找到根节点
        root = None
        for node, info in self.tree.items():
            if info["parent"] is None:
                root = node
                break
        
        if root is None:
            raise ValueError("No root node found in tree")
        
        # BFS 计算深度
        queue = [(root, 0)]
        while queue:
            node, depth = queue.pop(0)
            self.node_depths[node] = depth
            for child in self.tree[node]["children"]:
                queue.append((child, depth + 1))

    def evaluate(self, parsed_info):
        """评估答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        # 解析 depth=X 格式
        if not raw_ans.startswith("depth="):
            return False
        
        try:
            depth_str = raw_ans.split("=", 1)[1].strip()
            submitted_depth = int(depth_str)
        except (IndexError, ValueError):
            return False
        
        return submitted_depth == self.target_depth

    def _cf_core_produce(self, parsed_info):
        """根据查询生成响应（原始逻辑）"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            none_res = "无"
            reject_msg = "拒绝：目标节点结构不可见"
            invalid_node_msg = "错误：无效的节点ID"
            invalid_format_msg = "错误：格式无效"
        else:
            yes_res, no_res = "Yes", "No"
            none_res = "None"
            reject_msg = "Rejected: target node structure not visible"
            invalid_node_msg = "Error: Invalid node ID"
            invalid_format_msg = "Error: Invalid format"

        # 优先级顺序处理查询
        if "query_list_nodes" in parsed_info:
            # 返回所有节点ID列表
            node_list = sorted(self.tree.keys())
            return str(node_list)

        elif "query_measure" in parsed_info:
            # 测量查询
            node = parsed_info["query_measure"].strip()
            if node not in self.tree:
                return invalid_node_msg
            return str(self.node_responses[node])

        elif "query_compare" in parsed_info:
            # 比较查询
            try:
                raw = parsed_info["query_compare"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return invalid_format_msg
                node1, node2 = parts
                if node1 not in self.tree or node2 not in self.tree:
                    return invalid_node_msg
                
                resp1 = self.node_responses[node1]
                resp2 = self.node_responses[node2]
                
                if resp1 < resp2:
                    return "<"
                elif resp1 == resp2:
                    return "="
                else:
                    return ">"
            except Exception:
                return invalid_format_msg

        elif "query_parent" in parsed_info:
            # 父节点查询
            node = parsed_info["query_parent"].strip()
            if node not in self.tree:
                return invalid_node_msg
            # 如果是目标节点，拒绝
            if node == self.target_node:
                return reject_msg
            parent = self.tree[node]["parent"]
            return none_res if parent is None else parent

        elif "query_children" in parsed_info:
            # 子节点查询
            node = parsed_info["query_children"].strip()
            if node not in self.tree:
                return invalid_node_msg
            # 如果是目标节点，拒绝
            if node == self.target_node:
                return reject_msg
            children = self.tree[node]["children"]
            return str(children)

        elif "query_is_root" in parsed_info:
            # 根节点判断
            node = parsed_info["query_is_root"].strip()
            if node not in self.tree:
                return invalid_node_msg
            # 如果是目标节点，拒绝
            if node == self.target_node:
                return reject_msg
            is_root = self.tree[node]["parent"] is None
            return yes_res if is_root else no_res

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """根据正确答案生成一个明显不同的错误答案"""
        # 布尔类中文
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"

        # 布尔类英文
        lower_correct = correct.lower()
        if lower_correct == "yes":
            return "No" if correct[0].isupper() else "no"
        if lower_correct == "no":
            return "Yes" if correct[0].isupper() else "yes"

        # 比较符号
        if correct == "<":
            return ">"
        if correct == ">":
            return "<"
        if correct == "=":
            return ">"

        # 纯数字（含可能的负号）
        try:
            val = int(correct)
            return str(val + 1)
        except ValueError:
            pass

        # None 类
        if correct in ("None", "无"):
            return "A_WRONG"

        # 其他（列表字符串等）
        return correct + "_WRONG"

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
        queries = []
        all_nodes = sorted(list(self.tree.keys()))

        # 1. query_list_nodes
        queries.append({
            "query": "<query_list_nodes></query_list_nodes>",
            "answer": self._cf_core_produce({"query_list_nodes": ""})
        })

        # 2. query_measure
        for node in all_nodes:
            queries.append({
                "query": f"<query_measure>{node}</query_measure>",
                "answer": self._cf_core_produce({"query_measure": node})
            })

        # 3. query_compare
        # 只枚举不同节点对（避免自比较），且只取有序对减少冗余
        for i, n1 in enumerate(all_nodes):
            for n2 in all_nodes[i+1:]:
                content = f"{n1},{n2}"
                queries.append({
                    "query": f"<query_compare>{content}</query_compare>",
                    "answer": self._cf_core_produce({"query_compare": content})
                })

        # 4. query_parent (非目标节点)
        for node in all_nodes:
            if node == self.target_node:
                continue
            queries.append({
                "query": f"<query_parent>{node}</query_parent>",
                "answer": self._cf_core_produce({"query_parent": node})
            })

        # 5. query_children (非目标节点)
        for node in all_nodes:
            if node == self.target_node:
                continue
            queries.append({
                "query": f"<query_children>{node}</query_children>",
                "answer": self._cf_core_produce({"query_children": node})
            })

        # 6. query_is_root (非目标节点)
        for node in all_nodes:
            if node == self.target_node:
                continue
            queries.append({
                "query": f"<query_is_root>{node}</query_is_root>",
                "answer": self._cf_core_produce({"query_is_root": node})
            })
            
        return queries