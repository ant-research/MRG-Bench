from .base import Game
import random

class HiddenTreeHeightGame(Game):

    game_rule_zh = """\
我们来玩一个"隐藏树高度"的推理游戏，规则如下：

游戏设定了一棵含 {n} 个编号节点（1 到 {n}）的有根树，根节点已固定但未知。其中存在唯一的隐藏节点 T（T 不是根节点）。

## 基本定义

节点高度 H(u) 定义为以 u 为根的子树高度：
- 若 u 为叶节点，则 H(u) = 0
- 否则 H(u) = 1 + max(H(v) for all v 是 u 的子节点)

## 结构规律

对于任意节点 u，其完整子节点高度集合应为 {{0, 1, ..., H(u)-1}}（当 H(u)=0 时为空集）。

由于节点 T 被隐藏，系统对每个节点 u 的可见子节点集为：从 u 的真实子节点中移除 T（若 T 是 u 的子节点）。

关键规律：
- 除了 T 的父节点外，所有节点的可见子节点高度集合都完整（即恰为 {{0, 1, ..., H(u)-1}}）
- 在 T 的父节点处，可见子节点高度集合会缺失恰好一个值，该缺失值等于 H(T)

你的目标是通过查询推断出 H(T) 的值。

## 可用操作

你可以进行以下两种查询：

1. 查询高度：询问某个节点 u 的高度 H(u)
   - 约束：u 不能是隐藏节点 T
   - 反馈：返回整数 H(u)，或在 u=T 时返回"拒绝查询"

2. 查询子高度：询问某个节点 u 的所有可见子节点的高度列表
   - 反馈：返回一个升序整数列表，包含 u 的所有可见子节点的高度值（不包含节点编号）
   - 列表可能为空（u 为叶节点或唯一子节点是 T）

## 查询与提交格式

每次只能进行一个操作。请使用以下 XML 格式：

- 查询节点 5 的高度：
<query_height>5</query_height>

- 查询节点 3 的子节点高度列表：
<query_children>3</query_children>

- 提交最终答案（例如猜测 H(T)=2）：
<answer>2</answer>

请尽可能少地使用查询次数，当你确定答案后即可提交。若答案错误或格式不符，游戏失败。
"""

    game_rule_en = """\
Let's play a "Hidden Tree Height" deduction game. Here are the rules:

The game involves a rooted tree with {n} numbered nodes (1 to {n}). The root is fixed but unknown. There exists a unique hidden node T (T is not the root).

## Basic Definition

The height H(u) of a node u is defined as the height of the subtree rooted at u:
- If u is a leaf, then H(u) = 0
- Otherwise H(u) = 1 + max(H(v) for all v that are children of u)

## Structural Pattern

For any node u, its complete set of child heights should be exactly {{0, 1, ..., H(u)-1}} (empty set when H(u)=0).

Since node T is hidden, the system's visible children set for each node u is: the true children of u with T removed (if T is a child of u).

Key pattern:
- Except for T's parent, all nodes have complete visible child height sets (exactly {{0, 1, ..., H(u)-1}})
- At T's parent, the visible child height set will be missing exactly one value, and that missing value equals H(T)

Your goal is to infer the value of H(T) through queries.

## Available Operations

You can perform the following two types of queries:

1. Query Height: Ask for the height H(u) of a node u
   - Constraint: u cannot be the hidden node T
   - Response: Returns integer H(u), or "Query Rejected" when u=T

2. Query Children Heights: Ask for the list of heights of all visible children of node u
   - Response: Returns a sorted integer list containing the heights of all visible children of u (without node IDs)
   - The list may be empty (u is a leaf or its only child is T)

## Query and Answer Format

Only one operation per turn. Use the following XML format:

- Query height of node 5:
<query_height>5</query_height>

- Query children heights of node 3:
<query_children>3</query_children>

- Submit final answer (e.g., guessing H(T)=2):
<answer>2</answer>

Please use as few queries as possible. Submit when you are confident. If the answer is wrong or the format is invalid, the game fails.
"""

    contextualized_rule_zh_1 = """\
这是针对物流系统路由规划的深度探测任务。
当前物流网络被抽象为一棵含 {n} 个站点的有根树（站点编号 1 到 {n}），总调度中心已固定为根节点但具体编号未知。网络中存在唯一的保密中转站 T（T 不是根节点）。

## 基本定义

站点路由深度 H(u) 定义为以 u 为起点的最大下游中转层数：
- 若 u 为末端站点，则 H(u) = 0
- 否则 H(u) = 1 + max(H(v) for all v 是 u 的直接下游站点)

## 结构规律

对于任意站点 u，其完整的直接下游站点的路由深度集合应为 {{0, 1, ..., H(u)-1}}（当 H(u)=0 时为空集）。

由于保密中转站 T 被从常规系统中隐藏，系统对每个站点 u 的可见下游站点集为：从 u 的真实下游站点中移除 T（若 T 是 u 的直接下游）。

关键规律：
- 除了 T 的上级站点外，所有站点的可见下游路由深度集合都完整（即恰为 {{0, 1, ..., H(u)-1}}）
- 在 T 的上级站点处，可见下游路由深度集合会缺失恰好一个值，该缺失值等于 H(T)

你的目标是通过查询推断出保密中转站的路由深度 H(T) 的值。

## 可用操作

你可以进行以下两种查询：

1. 查询路由深度：询问某个站点 u 的深度 H(u)
   - 约束：u 不能是保密中转站 T
   - 反馈：返回整数 H(u)，或在 u=T 时系统提示"拒绝查询"

2. 查询下游深度列表：询问某个站点 u 的所有可见下游站点的路由深度列表
   - 反馈：返回一个升序整数列表，包含 u 的所有可见下游站点的深度值（不包含站点编号）
   - 列表可能为空（u 为末端站点或唯一直接下游是 T）

## 查询与提交格式

每次只能进行一个操作。请使用以下 XML 格式：

- 查询站点 5 的路由深度：
<query_height>5</query_height>

- 查询站点 3 的下游深度列表：
<query_children>3</query_children>

- 提交最终答案（例如猜测 H(T)=2）：
<answer>2</answer>

请尽可能少地使用查询次数，当你确定答案后即可提交。若答案错误或格式不符，任务失败。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
This is a routing depth probe task for a logistics distribution network.
The network is modeled as a rooted tree with {n} stations (numbered 1 to {n}). The main dispatch center is the fixed but unknown root. There exists a unique classified transit hub T (T is not the root).

## Basic Definition

The routing depth H(u) of a station u is defined as the maximum transit levels of the sub-network originating at u:
- If u is a terminal station, then H(u) = 0
- Otherwise H(u) = 1 + max(H(v) for all v that are direct downstream stations of u)

## Structural Pattern

For any station u, its complete set of downstream station depths should be exactly {{0, 1, ..., H(u)-1}} (empty set when H(u)=0).

Since the classified hub T is hidden from the regular system, the visible downstream set for each station u is: the true downstream stations of u with T removed (if T is directly downstream of u).

Key pattern:
- Except for T's immediate upstream station, all stations have complete visible downstream depth sets (exactly {{0, 1, ..., H(u)-1}})
- At T's upstream station, the visible downstream depth set will be missing exactly one value, and that missing value equals H(T)

Your goal is to infer the value of H(T) through system queries.

## Available Operations

You can perform the following two types of queries:

1. Query Routing Depth: Ask for the depth H(u) of a station u
   - Constraint: u cannot be the classified hub T
   - Response: Returns integer H(u), or "Query Rejected" when u=T

2. Query Downstream Depths: Ask for the list of depths of all visible downstream stations of u
   - Response: Returns a sorted integer list containing the depths of all visible downstream stations of u (without station IDs)
   - The list may be empty (u is a terminal or its only downstream is T)

## Query and Answer Format

Only one operation per turn. Use the following XML format:

- Query routing depth of station 5:
<query_height>5</query_height>

- Query downstream depths of station 3:
<query_children>3</query_children>

- Submit final answer (e.g., guessing H(T)=2):
<answer>2</answer>

Please use as few queries as possible. Submit when you are confident. If the answer is wrong or the format is invalid, the task fails.
"""

    contextualized_rule_zh_2 = """\
这是针对传染病变异溯源的流行病学调查任务。
目前掌握的病毒突变传播链被构建为一棵含 {n} 个毒株样本的有根树（样本编号 1 到 {n}），初始起源毒株已固定为根节点但具体编号未知。其中存在一个唯一的未测序零号感染源 T（T 不是初始起源毒株）。

## 基本定义

样本突变深度 H(u) 定义为以 u 为起点的最大后续突变代数：
- 若 u 为末端样本，则 H(u) = 0
- 否则 H(u) = 1 + max(H(v) for all v 是 u 的直接后续突变样本)

## 结构规律

对于任意样本 u，其完整的直接后续样本的突变深度集合应为 {{0, 1, ..., H(u)-1}}（当 H(u)=0 时为空集）。

由于零号感染源 T 未被正式测序收录，系统对每个样本 u 的可见后续样本集为：从 u 的真实后续样本中移除 T（若 T 是 u 的直接后续）。

关键规律：
- 除了 T 的直接前导变异样本外，所有样本的可见后续突变深度集合都完整（即恰为 {{0, 1, ..., H(u)-1}}）
- 在 T 的前导变异样本处，可见后续突变深度集合会缺失恰好一个值，该缺失值等于 H(T)

你的目标是通过查询推断出零号感染源的突变深度 H(T) 的值。

## 可用操作

你可以进行以下两种查询：

1. 查询突变深度：询问某个样本 u 的深度 H(u)
   - 约束：u 不能是未测序样本 T
   - 反馈：返回整数 H(u)，或在 u=T 时系统提示"拒绝查询"

2. 查询后续突变深度列表：询问某个样本 u 的所有可见后续样本的突变深度列表
   - 反馈：返回一个升序整数列表，包含 u 的所有可见后续样本的深度值（不包含样本编号）
   - 列表可能为空（u 为末端样本或唯一直接后续是 T）

## 查询与提交格式

每次只能进行一个操作。请使用以下 XML 格式：

- 查询样本 5 的突变深度：
<query_height>5</query_height>

- 查询样本 3 的后续突变深度列表：
<query_children>3</query_children>

- 提交最终答案（例如猜测 H(T)=2）：
<answer>2</answer>

请尽可能少地使用查询次数，当你确定答案后即可提交。若答案错误或格式不符，任务失败。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
This is an epidemiological investigation for tracing infectious disease mutations.
The known viral mutation transmission chain is structured as a rooted tree with {n} strain samples (numbered 1 to {n}). The initial origin strain is the fixed but unknown root. There exists a unique unsequenced zero-patient variant T (T is not the origin strain).

## Basic Definition

The mutation depth H(u) of a sample u is defined as the maximum subsequent mutation generations originating from u:
- If u is a terminal sample, then H(u) = 0
- Otherwise H(u) = 1 + max(H(v) for all v that are direct subsequent mutations of u)

## Structural Pattern

For any sample u, its complete set of subsequent mutation depths should be exactly {{0, 1, ..., H(u)-1}} (empty set when H(u)=0).

Since variant T is unsequenced and hidden, the visible subsequent sample set for each sample u is: the true subsequent samples of u with T removed (if T is a direct mutation of u).

Key pattern:
- Except for T's immediate predecessor strain, all samples have complete visible subsequent depth sets (exactly {{0, 1, ..., H(u)-1}})
- At T's predecessor strain, the visible subsequent depth set will be missing exactly one value, and that missing value equals H(T)

Your goal is to infer the value of H(T) through system queries.

## Available Operations

You can perform the following two types of queries:

1. Query Mutation Depth: Ask for the depth H(u) of a sample u
   - Constraint: u cannot be the unsequenced variant T
   - Response: Returns integer H(u), or "Query Rejected" when u=T

2. Query Subsequent Depths: Ask for the list of depths of all visible subsequent samples of u
   - Response: Returns a sorted integer list containing the depths of all visible subsequent samples of u (without sample IDs)
   - The list may be empty (u is a terminal or its only subsequent mutation is T)

## Query and Answer Format

Only one operation per turn. Use the following XML format:

- Query mutation depth of sample 5:
<query_height>5</query_height>

- Query subsequent depths of sample 3:
<query_children>3</query_children>

- Submit final answer (e.g., guessing H(T)=2):
<answer>2</answer>

Please use as few queries as possible. Submit when you are confident. If the answer is wrong or the format is invalid, the task fails.
"""

    contextualized_rule_zh_3 = """\
这是针对核心教学体系的课程前置依赖分析任务。
该课程网络被设计为一棵含 {n} 个课程模块的有根树（模块编号 1 到 {n}），基础导论课已固定为根节点但具体编号未知。其中存在唯一的保密级核心课程 T（T 不是基础导论课）。

## 基本定义

课程后续深度 H(u) 定义为以 u 为前置条件的最大后续课程层级数：
- 若 u 为顶点课程（无后续），则 H(u) = 0
- 否则 H(u) = 1 + max(H(v) for all v 是以 u 为直接前置的课程)

## 结构规律

对于任意课程 u，其完整的直接后续课程的深度集合应为 {{0, 1, ..., H(u)-1}}（当 H(u)=0 时为空集）。

由于保密级核心课程 T 被从公开大纲中隐藏，系统对每个课程 u 的可见后续课程集为：从 u 的真实后续课程中移除 T（若 T 的直接前置是 u）。

关键规律：
- 除了 T 的直接前置课程外，所有课程的可见后续深度集合都完整（即恰为 {{0, 1, ..., H(u)-1}}）
- 在 T 的前置课程处，可见后续深度集合会缺失恰好一个值，该缺失值等于 H(T)

你的目标是通过查询推断出保密核心课程的后续深度 H(T) 的值。

## 可用操作

你可以进行以下两种查询：

1. 查询课程后续深度：询问某个课程 u 的深度 H(u)
   - 约束：u 不能是保密核心课程 T
   - 反馈：返回整数 H(u)，或在 u=T 时系统提示"拒绝查询"

2. 查询直接后续深度列表：询问某个课程 u 的所有可见后续课程的深度列表
   - 反馈：返回一个升序整数列表，包含 u 的所有可见后续课程的深度值（不包含课程编号）
   - 列表可能为空（u 为顶点课程或唯一直接后续是 T）

## 查询与提交格式

每次只能进行一个操作。请使用以下 XML 格式：

- 查询课程 5 的后续深度：
<query_height>5</query_height>

- 查询课程 3 的直接后续深度列表：
<query_children>3</query_children>

- 提交最终答案（例如猜测 H(T)=2）：
<answer>2</answer>

请尽可能少地使用查询次数，当你确定答案后即可提交。若答案错误或格式不符，任务失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
This is a core course prerequisite dependency analysis task.
The curriculum network is designed as a rooted tree with {n} course modules (numbered 1 to {n}). The foundational introductory course is the fixed but unknown root. There exists a unique restricted core course T (T is not the foundational course).

## Basic Definition

The follow-up depth H(u) of a course u is defined as the maximum levels of subsequent courses requiring u as a prerequisite:
- If u is a capstone course (no follow-ups), then H(u) = 0
- Otherwise H(u) = 1 + max(H(v) for all v that are direct subsequent courses of u)

## Structural Pattern

For any course u, its complete set of subsequent course depths should be exactly {{0, 1, ..., H(u)-1}} (empty set when H(u)=0).

Since the restricted course T is hidden from the public syllabus, the visible subsequent course set for each course u is: the true subsequent courses of u with T removed (if u is a direct prerequisite of T).

Key pattern:
- Except for T's immediate prerequisite course, all courses have complete visible subsequent depth sets (exactly {{0, 1, ..., H(u)-1}})
- At T's prerequisite course, the visible subsequent depth set will be missing exactly one value, and that missing value equals H(T)

Your goal is to infer the value of H(T) through system queries.

## Available Operations

You can perform the following two types of queries:

1. Query Follow-up Depth: Ask for the depth H(u) of a course u
   - Constraint: u cannot be the restricted course T
   - Response: Returns integer H(u), or "Query Rejected" when u=T

2. Query Subsequent Depths: Ask for the list of depths of all visible subsequent courses of u
   - Response: Returns a sorted integer list containing the depths of all visible subsequent courses of u (without course IDs)
   - The list may be empty (u is a capstone or its only subsequent is T)

## Query and Answer Format

Only one operation per turn. Use the following XML format:

- Query follow-up depth of course 5:
<query_height>5</query_height>

- Query subsequent depths of course 3:
<query_children>3</query_children>

- Submit final answer (e.g., guessing H(T)=2):
<answer>2</answer>

Please use as few queries as possible. Submit when you are confident. If the answer is wrong or the format is invalid, the task fails.
"""

    contextualized_rule_zh_4 = """\
这是针对复杂工业装备的 BOM（物料清单）层级解析任务。
装备组件结构被拆解为一棵含 {n} 个组件的有根树（组件编号 1 到 {n}），总装成品已固定为根节点但具体编号未知。其中存在唯一的受商业机密保护的核心自研组件 T（T 不是总装成品）。

## 基本定义

组件子装配深度 H(u) 定义为以 u 为顶层组件的最大向下嵌套装配层数：
- 若 u 为底层基础零件，则 H(u) = 0
- 否则 H(u) = 1 + max(H(v) for all v 是 u 的直接子组件)

## 结构规律

对于任意组件 u，其完整的直接子组件装配深度集合应为 {{0, 1, ..., H(u)-1}}（当 H(u)=0 时为空集）。

由于机密组件 T 被从常规图纸中隐藏，系统对每个组件 u 的可见子组件集为：从 u 的真实子组件中移除 T（若 T 是 u 的直接子组件）。

关键规律：
- 除了 T 的父级装配体外，所有组件的可见子组件深度集合都完整（即恰为 {{0, 1, ..., H(u)-1}}）
- 在 T 的父级装配体处，可见子组件深度集合会缺失恰好一个值，该缺失值等于 H(T)

你的目标是通过查询推断出机密组件的子装配深度 H(T) 的值。

## 可用操作

你可以进行以下两种查询：

1. 查询子装配深度：询问某个组件 u 的深度 H(u)
   - 约束：u 不能是机密组件 T
   - 反馈：返回整数 H(u)，或在 u=T 时系统提示"拒绝查询"

2. 查询子组件深度列表：询问某个组件 u 的所有可见子组件的深度列表
   - 反馈：返回一个升序整数列表，包含 u 的所有可见子组件的深度值（不包含组件编号）
   - 列表可能为空（u 为基础零件或唯一直接子组件是 T）

## 查询与提交格式

每次只能进行一个操作。请使用以下 XML 格式：

- 查询组件 5 的子装配深度：
<query_height>5</query_height>

- 查询组件 3 的子组件深度列表：
<query_children>3</query_children>

- 提交最终答案（例如猜测 H(T)=2）：
<answer>2</answer>

请尽可能少地使用查询次数，当你确定答案后即可提交。若答案错误或格式不符，任务失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
This is a BOM (Bill of Materials) level analysis task for complex industrial equipment.
The equipment component structure is disassembled into a rooted tree with {n} components (numbered 1 to {n}). The final assembled product is the fixed but unknown root. There exists a unique proprietary confidential component T (T is not the final product).

## Basic Definition

The sub-assembly depth H(u) of a component u is defined as the maximum nested assembly levels downward from u:
- If u is a base part (no sub-components), then H(u) = 0
- Otherwise H(u) = 1 + max(H(v) for all v that are direct sub-components of u)

## Structural Pattern

For any component u, its complete set of sub-component depths should be exactly {{0, 1, ..., H(u)-1}} (empty set when H(u)=0).

Since the proprietary component T is hidden from standard blueprints, the visible sub-component set for each component u is: the true sub-components of u with T removed (if T is a direct sub-component of u).

Key pattern:
- Except for T's parent assembly, all components have complete visible sub-component depth sets (exactly {{0, 1, ..., H(u)-1}})
- At T's parent assembly, the visible sub-component depth set will be missing exactly one value, and that missing value equals H(T)

Your goal is to infer the value of H(T) through system queries.

## Available Operations

You can perform the following two types of queries:

1. Query Sub-assembly Depth: Ask for the depth H(u) of a component u
   - Constraint: u cannot be the proprietary component T
   - Response: Returns integer H(u), or "Query Rejected" when u=T

2. Query Sub-component Depths: Ask for the list of depths of all visible sub-components of u
   - Response: Returns a sorted integer list containing the depths of all visible sub-components of u (without component IDs)
   - The list may be empty (u is a base part or its only sub-component is T)

## Query and Answer Format

Only one operation per turn. Use the following XML format:

- Query sub-assembly depth of component 5:
<query_height>5</query_height>

- Query sub-component depths of component 3:
<query_children>3</query_children>

- Submit final answer (e.g., guessing H(T)=2):
<answer>2</answer>

Please use as few queries as possible. Submit when you are confident. If the answer is wrong or the format is invalid, the task fails.
"""

    contextualized_rule_zh_5 = """\
这是针对跨境洗钱网络的股权穿透调查任务。
涉案的商业帝国被重构为一棵含 {n} 个企业实体的有根树（实体编号 1 到 {n}），最终控股集团已固定为根节点但具体编号未知。其中隐藏着唯一的离岸空壳公司 T（T 不是最终控股集团）。

## 基本定义

实体控股深度 H(u) 定义为以 u 为母公司的最大向下嵌套控股层数：
- 若 u 为底层业务实体（无子公司），则 H(u) = 0
- 否则 H(u) = 1 + max(H(v) for all v 是 u 的直接控股子公司)

## 结构规律

对于任意实体 u，其完整的直接子公司的控股深度集合应为 {{0, 1, ..., H(u)-1}}（当 H(u)=0 时为空集）。

由于离岸空壳公司 T 被跨国协议掩盖，系统对每个实体 u 的可见子公司集为：从 u 的真实子公司中移除 T（若 T 是 u 的直接子公司）。

关键规律：
- 除了 T 的直接母公司外，所有实体的可见子公司深度集合都完整（即恰为 {{0, 1, ..., H(u)-1}}）
- 在 T 的母公司处，可见子公司深度集合会缺失恰好一个值，该缺失值等于 H(T)

你的目标是通过查询推断出离岸空壳公司的控股深度 H(T) 的值。

## 可用操作

你可以进行以下两种查询：

1. 查询控股深度：询问某个实体 u 的深度 H(u)
   - 约束：u 不能是离岸空壳公司 T
   - 反馈：返回整数 H(u)，或在 u=T 时系统提示"拒绝查询"

2. 查询子公司深度列表：询问某个实体 u 的所有可见子公司的控股深度列表
   - 反馈：返回一个升序整数列表，包含 u 的所有可见子公司的深度值（不包含实体编号）
   - 列表可能为空（u 为底层实体或唯一直接子公司是 T）

## 查询与提交格式

每次只能进行一个操作。请使用以下 XML 格式：

- 查询实体 5 的控股深度：
<query_height>5</query_height>

- 查询实体 3 的子公司深度列表：
<query_children>3</query_children>

- 提交最终答案（例如猜测 H(T)=2）：
<answer>2</answer>

请尽可能少地使用查询次数，当你确定答案后即可提交。若答案错误或格式不符，调查失败。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
This is an equity penetration investigation into a cross-border money laundering network.
The involved business empire is reconstructed as a rooted tree with {n} corporate entities (numbered 1 to {n}). The ultimate holding group is the fixed but unknown root. There exists a unique offshore hidden shell company T (T is not the ultimate holding group).

## Basic Definition

The subsidiary depth H(u) of an entity u is defined as the maximum nested holding levels downward from u:
- If u is a bottom-level operational entity (no subsidiaries), then H(u) = 0
- Otherwise H(u) = 1 + max(H(v) for all v that are direct subsidiaries of u)

## Structural Pattern

For any entity u, its complete set of subsidiary depths should be exactly {{0, 1, ..., H(u)-1}} (empty set when H(u)=0).

Since the offshore shell company T is obscured by transnational agreements, the visible subsidiary set for each entity u is: the true subsidiaries of u with T removed (if T is a direct subsidiary of u).

Key pattern:
- Except for T's immediate parent company, all entities have complete visible subsidiary depth sets (exactly {{0, 1, ..., H(u)-1}})
- At T's parent company, the visible subsidiary depth set will be missing exactly one value, and that missing value equals H(T)

Your goal is to infer the value of H(T) through system queries.

## Available Operations

You can perform the following two types of queries:

1. Query Subsidiary Depth: Ask for the depth H(u) of an entity u
   - Constraint: u cannot be the offshore shell company T
   - Response: Returns integer H(u), or "Query Rejected" when u=T

2. Query Subsidiary Depths List: Ask for the list of depths of all visible subsidiaries of entity u
   - Response: Returns a sorted integer list containing the depths of all visible subsidiaries of u (without entity IDs)
   - The list may be empty (u is a bottom-level entity or its only subsidiary is T)

## Query and Answer Format

Only one operation per turn. Use the following XML format:

- Query subsidiary depth of entity 5:
<query_height>5</query_height>

- Query subsidiary depths of entity 3:
<query_children>3</query_children>

- Submit final answer (e.g., guessing H(T)=2):
<answer>2</answer>

Please use as few queries as possible. Submit when you are confident. If the answer is wrong or the format is invalid, the investigation fails.
"""

    tags = ["answer", "query_height", "query_children"]
    
    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        1: {
            "n": 4,
            "edges": [(1, 2), (1, 3), (3, 4)],
            "root": 1,
            "hidden": 2,
        },
        2: {
            "n": 8,
            "edges": [(1, 2), (1, 3), (1, 4), (3, 5), (4, 6), (4, 7), (7, 8)],
            "root": 1,
            "hidden": 4,
        },
        3: {
            "n": 8,
            "edges": [(1, 2), (1, 3), (1, 4), (3, 5), (4, 6), (4, 7), (7, 8)],
            "root": 1,
            "hidden": 3,
        },
        4: {
            "n": 16,
            "edges": [
                (1, 2), (1, 3), (1, 4), (1, 5),
                (3, 6),
                (4, 7), (4, 8),
                (8, 9),
                (5, 10), (5, 11), (5, 12),
                (11, 13),
                (12, 14), (12, 15),
                (15, 16)
            ],
            "root": 1,
            "hidden": 12,
        },
        5: {
            "n": 16,
            "edges": [
                (1, 2), (1, 3), (1, 4), (1, 5),
                (3, 6),
                (4, 7), (4, 8),
                (8, 9),
                (5, 10), (5, 11), (5, 12),
                (11, 13),
                (12, 14), (12, 15),
                (15, 16)
            ],
            "root": 1,
            "hidden": 5,
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏状态，构建树结构并计算所有节点高度"""
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self._game_info["n"] = cfg["n"]
        
        # 构建树结构
        self.n = cfg["n"]
        
        # 节点编号随机映射
        nodes = list(range(1, self.n + 1))
        random.shuffle(nodes)
        mapping = {i: nodes[i-1] for i in range(1, self.n + 1)}
        
        self.root = mapping[cfg["root"]]
        self.hidden = mapping[cfg["hidden"]]
        
        # 构建邻接表（父->子）
        self.children = {i: [] for i in range(1, self.n + 1)}
        for parent, child in cfg["edges"]:
            self.children[mapping[parent]].append(mapping[child])
            
        # 找到隐藏节点的父节点
        self.hidden_parent = None
        for parent, child in cfg["edges"]:
            if child == cfg["hidden"]:
                self.hidden_parent = mapping[parent]
                break
        
        # 计算所有节点的真实高度
        self.heights = {}
        self._compute_heights(self.root)
        
        # 存储答案：隐藏节点的高度
        self.answer = self.heights[self.hidden]

        # 验证树结构不变量
        for u in range(1, self.n + 1):
            child_heights = set()
            for v in self.children[u]:
                child_heights.add(self.heights[v])
            
            expected = set(range(self.heights[u]))
            assert child_heights == expected, f"Node {u} true child heights {child_heights} != expected {expected}"
            
            visible = set(self._get_visible_children_heights(u))
            if u == self.hidden_parent:
                expected_missing = self.heights[self.hidden]
                assert expected_missing not in visible
                expected_visible = expected - {expected_missing}
                assert visible == expected_visible
            else:
                assert visible == expected

    def _compute_heights(self, node):
        """递归计算节点高度"""
        if not self.children[node]:  # 叶节点
            self.heights[node] = 0
            return 0
        
        max_child_height = -1
        for child in self.children[node]:
            child_height = self._compute_heights(child)
            max_child_height = max(max_child_height, child_height)
        
        self.heights[node] = max_child_height + 1
        return self.heights[node]

    def _get_visible_children_heights(self, node):
        """获取节点的可见子节点高度列表（排除隐藏节点T）"""
        visible_heights = []
        for child in self.children[node]:
            if child != self.hidden:
                visible_heights.append(self.heights[child])
        return sorted(visible_heights)

    def evaluate(self, parsed_info):
        """评估玩家提交的答案是否正确"""
        try:
            guessed_height = int(parsed_info["answer"].strip())
            return guessed_height == self.answer
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑：根据玩家的查询生成响应"""
        if self.config.language == "zh":
            reject_msg = "拒绝查询"
            error_msg = "错误：节点编号超出范围。"
        else:
            reject_msg = "Query Rejected"
            error_msg = "Error: Node ID out of range."

        # 优先处理 query_height
        if "query_height" in parsed_info:
            try:
                node = int(parsed_info["query_height"].strip())
                if node < 1 or node > self.n:
                    return error_msg
                if node == self.hidden:
                    return reject_msg
                return str(self.heights[node])
            except:
                return error_msg

        # 处理 query_children
        elif "query_children" in parsed_info:
            try:
                node = int(parsed_info["query_children"].strip())
                if node < 1 or node > self.n:
                    return error_msg
                heights_list = self._get_visible_children_heights(node)
                return str(heights_list)
            except:
                return error_msg

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        """根据正确答案生成一个明显不同的错误答案"""
        stripped = correct.strip()
        
        # 尝试纯整数（高度查询的返回）
        try:
            val = int(stripped)
            return str(val + 1)
        except ValueError:
            pass
        
        # 尝试列表格式（子节点高度查询的返回，如 "[0, 1, 2]"）
        if stripped.startswith("[") and stripped.endswith("]"):
            try:
                import ast
                lst = ast.literal_eval(stripped)
                if isinstance(lst, list):
                    # 添加一个不存在的高度值来制造错误
                    wrong_lst = lst + [max(lst) + 1] if lst else [0]
                    return str(sorted(wrong_lst))
            except:
                pass
        
        # 拒绝查询类消息
        if self.config.language == "zh":
            if "拒绝" in stripped:
                return "0"  # 返回一个假的正常高度
            if "是" in stripped:
                return stripped.replace("是", "否")
            if "否" in stripped:
                return stripped.replace("否", "是")
        else:
            if "rejected" in stripped.lower():
                return "0"  # 返回一个假的正常高度
            correct_lower = stripped.lower()
            if "yes" in correct_lower:
                return stripped.replace("Yes", "No").replace("yes", "no")
            if "no" in correct_lower:
                return stripped.replace("No", "Yes").replace("no", "yes")
        
        # 兜底
        return stripped + "_WRONG"

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
        results = []
        for i in range(1, self.n + 1):
            # 1. Query Height — 包括隐藏节点（会被拒绝）
            query_str = f"<query_height>{i}</query_height>"
            if i == self.hidden:
                if self.config.language == "zh":
                    answer_str = "拒绝查询"
                else:
                    answer_str = "Query Rejected"
            else:
                answer_str = str(self.heights[i])
            results.append({
                "query": query_str,
                "answer": answer_str
            })
            
            # 2. Query Children — 所有节点均可查询
            query_str = f"<query_children>{i}</query_children>"
            children_heights = self._get_visible_children_heights(i)
            answer_str = str(children_heights)
            results.append({
                "query": query_str,
                "answer": answer_str
            })
            
        return results