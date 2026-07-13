# -*- coding: utf-8 -*-
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   路径枚举：两个给定节点之间所有可能的简单路径有哪些
# ============================================================

from .base import Game
import re


class GraphPathEnumerationGame(Game):

    game_rule_zh = """\
我们来玩一个"图路径枚举"推理游戏，规则如下：

游戏设定了一个未知边集的有限无向简单图 G，节点集合 V 由若干个唯一大写字母构成（如 A、B、C 等）。图中无自环、无重边，每个节点的度数不超过 4。

我已指定了起点 S 和终点 T（均属于 V），并保证至少存在一条从 S 到 T 的路径。

你的目标是通过查询，精确枚举并提交从 S 到 T 的全部且仅有的简单路径集合（简单路径指不含重复节点的路径）。路径不可重复，必须均为合法路径。

## 可用的查询类型

每次可以提出最多 3 个问题（每个问题单独书写，使用以下格式）：

1. **邻居查询**：询问节点 X 的所有相邻节点
   格式：<query_neighbor>X</query_neighbor>
   
2. **边存在查询**：询问节点 X 与 Y 是否直接相连
   格式：<query_edge>X,Y</query_edge>
   
3. **度数查询**：询问节点 X 的度数
   格式：<query_degree>X</query_degree>
   
4. **路径校验**：检验给定路径是否合法
   格式：<query_verify>X1-X2-X3-...</query_verify>
   
5. **前缀可扩展查询**：询问从给定前缀路径可以扩展的下一步节点
   格式：<query_expand>X1-X2-X3-...</query_expand>

注意：你应该尽可能高效地使用查询次数。

## 提交答案格式

当你收集到足够信息后，可以提交你找到的所有从 S 到 T 的简单路径。每条路径用"-"连接节点，多条路径用";"分隔。

格式：<answer>S-A-T; S-B-C-T; S-D-E-F-T</answer>

如果答案不正确，系统会告诉你错误原因。你最多可以提交 3 次答案。

## 游戏信息

- 起点：{start}
- 终点：{end}
- 节点集合：{vertices}
"""

    game_rule_en = """\
Let's play a "Graph Path Enumeration" deduction game with the following rules:

The game features a finite undirected simple graph G with an unknown edge set. The vertex set V consists of several unique uppercase letters (such as A, B, C, etc.). The graph has no self-loops, no multiple edges, and each node has a degree of at most 4.

I have specified a start node S and an end node T (both in V), and guarantee that at least one path exists from S to T.

Your goal is to precisely enumerate and submit the complete set of all simple paths from S to T through queries (a simple path is one without repeated nodes). Paths must not be duplicated and must all be valid.

## Available Query Types

You can ask up to 3 questions per turn (each question written separately, using the following formats):

1. **Neighbor Query**: Ask for all neighbors of node X
   Format: <query_neighbor>X</query_neighbor>
   
2. **Edge Existence Query**: Ask if nodes X and Y are directly connected
   Format: <query_edge>X,Y</query_edge>
   
3. **Degree Query**: Ask for the degree of node X
   Format: <query_degree>X</query_degree>
   
4. **Path Verification**: Verify if a given path is valid
   Format: <query_verify>X1-X2-X3-...</query_verify>
   
5. **Prefix Expansion Query**: Ask which nodes can extend a given path prefix
   Format: <query_expand>X1-X2-X3-...</query_expand>

Note: You should use queries as efficiently as possible.

## Answer Submission Format

When you have gathered enough information, submit all simple paths from S to T that you have found. Connect nodes in each path with "-", and separate multiple paths with ";".

Format: <answer>S-A-T; S-B-C-T; S-D-E-F-T</answer>

If your answer is incorrect, the system will tell you why. You may submit up to 3 times.

## Game Information

- Start: {start}
- End: {end}
- Vertices: {vertices}
"""

    # 场景 1：交通
    contextualized_rule_zh_1 = """\
我们在交通物流场景中进行一项“物流管网路径枚举”任务，规则如下：

系统设定了一个包含未知通车路线的有限无向运输网络 G，中转枢纽集合 V 由若干个唯一大写字母构成（如 A、B、C 等）。网络中无自环、无重边，每个枢纽的直连路线不超过 4 条。

我已指定了发货起点 S 和收货终点 T（均属于 V），并保证至少存在一条从 S 到 T 的可用运输路线。

你的目标是通过查询，精确枚举并提交从 S 到 T 的全部且仅有的简单流转路线集合（简单路线指不含重复枢纽的路线）。路线不可重复，必须均为合法路线。

## 可用的查询类型

每次可以提出最多 3 个问题（每个问题单独书写，使用以下格式）：

1. **邻居查询**：询问枢纽 X 的所有直连中转枢纽
   格式：<query_neighbor>X</query_neighbor>
   
2. **边存在查询**：询问枢纽 X 与 Y 是否直接通车
   格式：<query_edge>X,Y</query_edge>
   
3. **度数查询**：询问枢纽 X 的直连路线数量
   格式：<query_degree>X</query_degree>
   
4. **路径校验**：检验给定运输路线是否合法
   格式：<query_verify>X1-X2-X3-...</query_verify>
   
5. **前缀可扩展查询**：询问从给定前缀路线可以扩展驶往的下一站枢纽
   格式：<query_expand>X1-X2-X3-...</query_expand>

注意：你应该尽可能高效地使用查询次数。

## 提交答案格式

当你收集到足够信息后，可以提交你找到的所有从 S 到 T 的简单路线。每条路线用"-"连接枢纽，多条路线用";"分隔。

格式：<answer>S-A-T; S-B-C-T; S-D-E-F-T</answer>

如果答案不正确，系统会告诉你错误原因。你最多可以提交 3 次答案。

## 任务信息

- 起点：{start}
- 终点：{end}
- 枢纽集合：{vertices}
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's perform a "Logistics Network Path Enumeration" task in a transportation context with the following rules:

The system features a finite undirected transport network G with an unknown set of routes. The transit hub set V consists of several unique uppercase letters (such as A, B, C, etc.). The network has no self-loops, no multiple routes between the same hubs, and each hub connects to at most 4 direct routes.

I have specified a dispatch start warehouse S and a receiving destination depot T (both in V), and guarantee that at least one viable transport route exists from S to T.

Your goal is to precisely enumerate and submit the complete set of all simple routes from S to T through queries (a simple route is one without repeated transit hubs). Routes must not be duplicated and must all be valid transport routes.

## Available Query Types

You can ask up to 3 questions per turn (each question written separately, using the following formats):

1. **Neighbor Query**: Ask for all directly connected transit hubs of hub X
   Format: <query_neighbor>X</query_neighbor>
   
2. **Edge Existence Query**: Ask if hubs X and Y are directly connected by a route
   Format: <query_edge>X,Y</query_edge>
   
3. **Degree Query**: Ask for the number of direct routes connected to hub X
   Format: <query_degree>X</query_degree>
   
4. **Path Verification**: Verify if a given transport route is valid
   Format: <query_verify>X1-X2-X3-...</query_verify>
   
5. **Prefix Expansion Query**: Ask which transit hubs can extend a given route prefix
   Format: <query_expand>X1-X2-X3-...</query_expand>

Note: You should use queries as efficiently as possible.

## Answer Submission Format

When you have gathered enough information, submit all simple routes from S to T that you have found. Connect hubs in each route with "-", and separate multiple routes with ";".

Format: <answer>S-A-T; S-B-C-T; S-D-E-F-T</answer>

If your answer is incorrect, the system will tell you why. You may submit up to 3 times.

## Task Information

- Start Hub: {start}
- End Hub: {end}
- Hubs: {vertices}
"""

    # 场景 2：医疗
    contextualized_rule_zh_2 = """\
我们在医疗场景中进行一项“临床诊疗路径枚举”任务，规则如下：

系统设定了一个包含未知转诊规则的有限无向诊疗流转网络 G，科室/阶段集合 V 由若干个唯一大写字母构成（如 A、B、C 等）。网络中无自环、无重边，每个科室的合理流转方向不超过 4 个。

我已指定了初诊起点 S 和康复终点 T（均属于 V），并保证至少存在一条从 S 到 T 的完整诊疗流转路径。

你的目标是通过查询，精确枚举并提交从 S 到 T 的全部且仅有的简单临床路径集合（简单路径指不含重复流转科室的路径）。路径不可重复，必须均为符合医疗规范的路径。

## 可用的查询类型

每次可以提出最多 3 个问题（每个问题单独书写，使用以下格式）：

1. **邻居查询**：询问科室 X 的所有合规转诊科室
   格式：<query_neighbor>X</query_neighbor>
   
2. **边存在查询**：询问科室 X 与 Y 之间是否可以直接转诊流转
   格式：<query_edge>X,Y</query_edge>
   
3. **度数查询**：询问科室 X 的允许转诊方向数量
   格式：<query_degree>X</query_degree>
   
4. **路径校验**：检验给定的临床流转路径是否合规
   格式：<query_verify>X1-X2-X3-...</query_verify>
   
5. **前缀可扩展查询**：询问基于当前已走过的诊疗阶段，下一步可扩展推进的科室
   格式：<query_expand>X1-X2-X3-...</query_expand>

注意：你应该尽可能高效地使用查询次数。

## 提交答案格式

当你收集到足够信息后，可以提交你找到的所有从 S 到 T 的简单临床流转路径。每条路径用"-"连接科室，多条路径用";"分隔。

格式：<answer>S-A-T; S-B-C-T; S-D-E-F-T</answer>

如果答案不正确，系统会告诉你错误原因。你最多可以提交 3 次答案。

## 任务信息

- 起点：{start}
- 终点：{end}
- 科室集合：{vertices}
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's perform a "Clinical Pathway Enumeration" task in a medical context with the following rules:

The system features a finite undirected clinical transition network G with an unknown set of referral rules. The medical department/stage set V consists of several unique uppercase letters (such as A, B, C, etc.). The network has no self-loops, no multiple transition routes between the same departments, and each department has at most 4 valid referral directions.

I have specified an initial diagnosis start stage S and a recovery end stage T (both in V), and guarantee that at least one complete clinical pathway exists from S to T.

Your goal is to precisely enumerate and submit the complete set of all simple clinical pathways from S to T through queries (a simple pathway is one without repeated medical departments). Pathways must not be duplicated and must all comply with clinical transition protocols.

## Available Query Types

You can ask up to 3 questions per turn (each question written separately, using the following formats):

1. **Neighbor Query**: Ask for all valid referral departments of department X
   Format: <query_neighbor>X</query_neighbor>
   
2. **Edge Existence Query**: Ask if a direct transition is allowed between departments X and Y
   Format: <query_edge>X,Y</query_edge>
   
3. **Degree Query**: Ask for the number of allowed transition directions for department X
   Format: <query_degree>X</query_degree>
   
4. **Path Verification**: Verify if a given clinical transition pathway is valid
   Format: <query_verify>X1-X2-X3-...</query_verify>
   
5. **Prefix Expansion Query**: Ask which departments can legitimately follow a given clinical pathway prefix
   Format: <query_expand>X1-X2-X3-...</query_expand>

Note: You should use queries as efficiently as possible.

## Answer Submission Format

When you have gathered enough information, submit all simple clinical pathways from S to T that you have found. Connect departments in each pathway with "-", and separate multiple pathways with ";".

Format: <answer>S-A-T; S-B-C-T; S-D-E-F-T</answer>

If your answer is incorrect, the system will tell you why. You may submit up to 3 times.

## Task Information

- Initial Diagnosis: {start}
- Recovery: {end}
- Departments: {vertices}
"""

    # 场景 3：教育
    contextualized_rule_zh_3 = """\
我们在教育学习场景中进行一项“知识图谱进阶路径枚举”任务，规则如下：

系统设定了一个隐藏相互依赖关系的有限无向知识网络 G，知识模块集合 V 由若干个唯一大写字母构成（如 A、B、C 等）。网络中无自环、无重复依赖，每个知识模块的直接关联模块不超过 4 个。

我已指定了基础概念起点 S 和掌握目标终点 T（均属于 V），并保证至少存在一条从 S 进阶到 T 的合理学习路径。

你的目标是通过查询，精确枚举并提交从 S 到 T 的全部且仅有的简单学习路径集合（简单路径指不含重复学习模块的进阶过程）。学习路径不可重复，必须均为逻辑连贯的合法顺序。

## 可用的查询类型

每次可以提出最多 3 个问题（每个问题单独书写，使用以下格式）：

1. **邻居查询**：询问知识模块 X 的所有直接关联模块
   格式：<query_neighbor>X</query_neighbor>
   
2. **边存在查询**：询问知识模块 X 与 Y 之间是否存在直接依赖关系
   格式：<query_edge>X,Y</query_edge>
   
3. **度数查询**：询问知识模块 X 的直接关联模块数量
   格式：<query_degree>X</query_degree>
   
4. **路径校验**：检验给定的学习序列是否连贯合法
   格式：<query_verify>X1-X2-X3-...</query_verify>
   
5. **前缀可扩展查询**：询问在学完当前模块序列后，可以平滑过渡学习的下一个知识模块
   格式：<query_expand>X1-X2-X3-...</query_expand>

注意：你应该尽可能高效地使用查询次数。

## 提交答案格式

当你收集到足够信息后，可以提交你找到的所有从 S 到 T 的简单学习路径。每条路径用"-"连接知识模块，多条路径用";"分隔。

格式：<answer>S-A-T; S-B-C-T; S-D-E-F-T</answer>

如果答案不正确，系统会告诉你错误原因。你最多可以提交 3 次答案。

## 任务信息

- 起点：{start}
- 终点：{end}
- 模块集合：{vertices}
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's perform a "Learning Knowledge Graph Path Enumeration" task in an educational context with the following rules:

The system features a finite undirected knowledge network G with hidden interdependence relationships. The knowledge module set V consists of several unique uppercase letters (such as A, B, C, etc.). The network has no self-loops, no redundant dependencies, and each knowledge module has at most 4 directly associated modules.

I have specified a baseline concept start S and a mastery goal end T (both in V), and guarantee that at least one logical learning progression exists from S to T.

Your goal is to precisely enumerate and submit the complete set of all simple learning paths from S to T through queries (a simple learning path is a progression without repeated study modules). Paths must not be duplicated and must all be coherent and valid sequences.

## Available Query Types

You can ask up to 3 questions per turn (each question written separately, using the following formats):

1. **Neighbor Query**: Ask for all directly associated modules of knowledge module X
   Format: <query_neighbor>X</query_neighbor>
   
2. **Edge Existence Query**: Ask if a direct dependency relationship exists between modules X and Y
   Format: <query_edge>X,Y</query_edge>
   
3. **Degree Query**: Ask for the number of directly associated modules for knowledge module X
   Format: <query_degree>X</query_degree>
   
4. **Path Verification**: Verify if a given learning sequence is coherent and valid
   Format: <query_verify>X1-X2-X3-...</query_verify>
   
5. **Prefix Expansion Query**: Ask which knowledge modules can smoothly follow a given learned sequence prefix
   Format: <query_expand>X1-X2-X3-...</query_expand>

Note: You should use queries as efficiently as possible.

## Answer Submission Format

When you have gathered enough information, submit all simple learning paths from S to T that you have found. Connect knowledge modules in each path with "-", and separate multiple paths with ";".

Format: <answer>S-A-T; S-B-C-T; S-D-E-F-T</answer>

If your answer is incorrect, the system will tell you why. You may submit up to 3 times.

## Task Information

- Baseline Start: {start}
- Mastery Goal: {end}
- Modules: {vertices}
"""

    # 场景 4：制造业/工业
    contextualized_rule_zh_4 = """\
我们在工业制造场景中进行一项“柔性制造工艺路线枚举”任务，规则如下：

系统设定了一个具备未知流转工序的有限无向车间加工网络 G，工作站集合 V 由若干个唯一大写字母构成（如 A、B、C 等）。网络中无自环、无重边，每个工作站的物料对接链路不超过 4 条。

我已指定了原料投料起点 S 和成品下线终点 T（均属于 V），并保证至少存在一条从 S 到 T 的可贯通加工路线。

你的目标是通过查询，精确枚举并提交从 S 到 T 的全部且仅有的简单工艺流转路线集合（简单路线指不含重复返工作站的路线）。流转路线不可重复，必须均为符合工艺约束的合法工序。

## 可用的查询类型

每次可以提出最多 3 个问题（每个问题单独书写，使用以下格式）：

1. **邻居查询**：询问工作站 X 的所有对接流转工作站
   格式：<query_neighbor>X</query_neighbor>
   
2. **边存在查询**：询问工作站 X 与 Y 之间是否可以直接传递物料
   格式：<query_edge>X,Y</query_edge>
   
3. **度数查询**：询问工作站 X 的物料对接链路总数
   格式：<query_degree>X</query_degree>
   
4. **路径校验**：检验给定的连续加工工序路线是否可行
   格式：<query_verify>X1-X2-X3-...</query_verify>
   
5. **前缀可扩展查询**：询问基于当前已完成的加工流转序列，下一步可分发的对接工作站
   格式：<query_expand>X1-X2-X3-...</query_expand>

注意：你应该尽可能高效地使用查询次数。

## 提交答案格式

当你收集到足够信息后，可以提交你找到的所有从 S 到 T 的简单工艺流转路线。每条路线用"-"连接工作站，多条路线用";"分隔。

格式：<answer>S-A-T; S-B-C-T; S-D-E-F-T</answer>

如果答案不正确，系统会告诉你错误原因。你最多可以提交 3 次答案。

## 任务信息

- 起点：{start}
- 终点：{end}
- 工作站集合：{vertices}
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's perform a "Flexible Manufacturing Process Routing Enumeration" task in an industrial context with the following rules:

The system features a finite undirected workshop processing network G with an unknown set of transfer workflows. The workstation set V consists of several unique uppercase letters (such as A, B, C, etc.). The network has no self-loops, no multiple material transfer links between the same workstations, and each workstation connects to at most 4 material routing links.

I have specified a raw material input start S and a finished product output end T (both in V), and guarantee that at least one viable processing route exists from S to T.

Your goal is to precisely enumerate and submit the complete set of all simple process routing flows from S to T through queries (a simple flow is a processing route without repeated workstations or rework). Routes must not be duplicated and must all comply with valid manufacturing constraints.

## Available Query Types

You can ask up to 3 questions per turn (each question written separately, using the following formats):

1. **Neighbor Query**: Ask for all routing-compatible workstations of workstation X
   Format: <query_neighbor>X</query_neighbor>
   
2. **Edge Existence Query**: Ask if materials can be transferred directly between workstations X and Y
   Format: <query_edge>X,Y</query_edge>
   
3. **Degree Query**: Ask for the total number of material routing links for workstation X
   Format: <query_degree>X</query_degree>
   
4. **Path Verification**: Verify if a given sequential processing flow is operationally feasible
   Format: <query_verify>X1-X2-X3-...</query_verify>
   
5. **Prefix Expansion Query**: Ask which workstations can receive materials as the next step of a given processing flow prefix
   Format: <query_expand>X1-X2-X3-...</query_expand>

Note: You should use queries as efficiently as possible.

## Answer Submission Format

When you have gathered enough information, submit all simple processing flows from S to T that you have found. Connect workstations in each flow with "-", and separate multiple flows with ";".

Format: <answer>S-A-T; S-B-C-T; S-D-E-F-T</answer>

If your answer is incorrect, the system will tell you why. You may submit up to 3 times.

## Task Information

- Raw Material Input: {start}
- Product Output: {end}
- Workstations: {vertices}
"""

    # 场景 5：法律
    contextualized_rule_zh_5 = """\
我们在司法实务场景中进行一项“法定程序流转路径枚举”任务，规则如下：

系统设定了一个包含未知审理推进步骤的有限无向司法程序网络 G，法定环节集合 V 由若干个唯一大写字母构成（如 A、B、C 等）。网络中无自环、无重复的法律环节过渡规则，每个法定环节的程序流转分支不超过 4 个。

我已指定了立案申请起点 S 和结案执行终点 T（均属于 V），并保证至少存在一套从 S 到 T 的完整合法程序推进路径。

你的目标是通过查询，精确枚举并提交从 S 到 T 的全部且仅有的简单程序流转路径集合（简单路径指不含重复审核或倒退环节的合法路径）。路径不可重复，必须均为符合法定程序的步骤序列。

## 可用的查询类型

每次可以提出最多 3 个问题（每个问题单独书写，使用以下格式）：

1. **邻居查询**：询问法定环节 X 的所有合法前后置接续环节
   格式：<query_neighbor>X</query_neighbor>
   
2. **边存在查询**：询问法定环节 X 与 Y 之间是否可以直接进行程序流转
   格式：<query_edge>X,Y</query_edge>
   
3. **度数查询**：询问法定环节 X 拥有的合法程序流转分支数量
   格式：<query_degree>X</query_degree>
   
4. **路径校验**：检验给定的司法程序流转序列是否合法合规
   格式：<query_verify>X1-X2-X3-...</query_verify>
   
5. **前缀可扩展查询**：询问基于当前已走完的程序步骤，下一步可发起的法定推进环节
   格式：<query_expand>X1-X2-X3-...</query_expand>

注意：你应该尽可能高效地使用查询次数。

## 提交答案格式

当你收集到足够信息后，可以提交你找到的所有从 S 到 T 的简单法定程序流转路径。每条路径用"-"连接环节，多条路径用";"分隔。

格式：<answer>S-A-T; S-B-C-T; S-D-E-F-T</answer>

如果答案不正确，系统会告诉你错误原因。你最多可以提交 3 次答案。

## 任务信息

- 起点：{start}
- 终点：{end}
- 法定环节集合：{vertices}
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's perform a "Judicial Procedure Flow Path Enumeration" task in a legal context with the following rules:

The system features a finite undirected judicial procedure network G with unknown procedural advancement rules. The statutory steps set V consists of several unique uppercase letters (such as A, B, C, etc.). The network has no self-loops, no redundant legal step transitions, and each statutory step has at most 4 valid procedural transition branches.

I have specified a case filing start S and a final enforcement end T (both in V), and guarantee that at least one complete, lawful procedural advancement path exists from S to T.

Your goal is to precisely enumerate and submit the complete set of all simple procedural transition paths from S to T through queries (a simple path is a lawful sequence without repeated review steps or regressive loops). Paths must not be duplicated and must all be statutory-compliant sequences.

## Available Query Types

You can ask up to 3 questions per turn (each question written separately, using the following formats):

1. **Neighbor Query**: Ask for all valid preceding or succeeding statutory steps of step X
   Format: <query_neighbor>X</query_neighbor>
   
2. **Edge Existence Query**: Ask if a direct procedural transition is allowed between steps X and Y
   Format: <query_edge>X,Y</query_edge>
   
3. **Degree Query**: Ask for the number of valid procedural transition branches for statutory step X
   Format: <query_degree>X</query_degree>
   
4. **Path Verification**: Verify if a given sequence of judicial procedure flows is lawful and compliant
   Format: <query_verify>X1-X2-X3-...</query_verify>
   
5. **Prefix Expansion Query**: Ask which statutory steps can legally follow a given completed procedural sequence prefix
   Format: <query_expand>X1-X2-X3-...</query_expand>

Note: You should use queries as efficiently as possible.

## Answer Submission Format

When you have gathered enough information, submit all simple statutory transition paths from S to T that you have found. Connect statutory steps in each path with "-", and separate multiple paths with ";".

Format: <answer>S-A-T; S-B-C-T; S-D-E-F-T</answer>

If your answer is incorrect, the system will tell you why. You may submit up to 3 times.

## Task Information

- Case Filing: {start}
- Final Enforcement: {end}
- Statutory Steps: {vertices}
"""

    tags = ["answer", "query_neighbor", "query_edge", "query_degree", "query_verify", "query_expand"]
    
    # 新增类属性
    reasoning_type = "演绎推理"
    data_structure = "图"

    # 难度配置：
    # 1 (简单)       - 6个节点，线性+分支结构，2条路径
    # 2 (中等偏下)   - 7个节点，多分支，3条路径
    # 3 (中等偏上)   - 8个节点，网状结构，5条路径
    # 4 (较难)       - 9个节点，复杂网络，8条路径
    # 5 (难)         - 9个节点，高度互联，12条路径

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "vertices": ["A", "B", "C", "D", "E", "F"],
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E"), ("E", "F")],
                "start": "A",
                "end": "F"
            },
            2: {
                "vertices": ["A", "B", "C", "D", "E", "F", "G"],
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("C", "E"), ("D", "F"), ("E", "F"), ("F", "G")],
                "start": "A",
                "end": "G"
            },
            3: {
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "E"), ("C", "F"), ("D", "G"), ("E", "G"), ("E", "H"), ("F", "H"), ("G", "H")],
                "start": "A",
                "end": "H"
            },
            4: {
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
                "edges": [("A", "B"), ("A", "C"), ("A", "D"), ("B", "E"), ("B", "F"), ("C", "F"), ("C", "G"), ("D", "G"), ("E", "H"), ("F", "H"), ("F", "I"), ("G", "I"), ("H", "I")],
                "start": "A",
                "end": "I"
            },
            5: {
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
                "edges": [("A", "B"), ("A", "C"), ("A", "D"), ("B", "E"), ("B", "F"), ("C", "E"), ("C", "F"), ("C", "G"), ("D", "F"), ("D", "G"), ("E", "H"), ("F", "H"), ("F", "I"), ("G", "H"), ("G", "I"), ("H", "I")],
                "start": "A",
                "end": "I"
            }
        },
        "en": {
            1: {
                "vertices": ["A", "B", "C", "D", "E", "F"],
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E"), ("E", "F")],
                "start": "A",
                "end": "F"
            },
            2: {
                "vertices": ["A", "B", "C", "D", "E", "F", "G"],
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("C", "E"), ("D", "F"), ("E", "F"), ("F", "G")],
                "start": "A",
                "end": "G"
            },
            3: {
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "E"), ("C", "F"), ("D", "G"), ("E", "G"), ("E", "H"), ("F", "H"), ("G", "H")],
                "start": "A",
                "end": "H"
            },
            4: {
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
                "edges": [("A", "B"), ("A", "C"), ("A", "D"), ("B", "E"), ("B", "F"), ("C", "F"), ("C", "G"), ("D", "G"), ("E", "H"), ("F", "H"), ("F", "I"), ("G", "I"), ("H", "I")],
                "start": "A",
                "end": "I"
            },
            5: {
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
                "edges": [("A", "B"), ("A", "C"), ("A", "D"), ("B", "E"), ("B", "F"), ("C", "E"), ("C", "F"), ("C", "G"), ("D", "F"), ("D", "G"), ("E", "H"), ("F", "H"), ("F", "I"), ("G", "H"), ("G", "I"), ("H", "I")],
                "start": "A",
                "end": "I"
            }
        }
    }

    def __init__(self, config):
        self.query_count = 0  # 查询计数（不含提交）
        self.submission_count = 0  # 提交计数
        self.max_queries = 40
        self.max_submissions = 3
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：构建图结构并计算所有简单路径"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 设置游戏信息
        self.vertices = set(cfg["vertices"])
        self.edges = set()
        self.adj_list = {v: set() for v in self.vertices}
        
        # 构建邻接表（无向图）
        for u, v in cfg["edges"]:
            self.edges.add((min(u, v), max(u, v)))  # 标准化边的表示
            self.adj_list[u].add(v)
            self.adj_list[v].add(u)
        
        self.start = cfg["start"]
        self.end = cfg["end"]
        
        # 计算所有从 start 到 end 的简单路径（标准答案）
        self.all_paths = self._find_all_simple_paths(self.start, self.end)
        
        # 用于格式化游戏信息
        self._game_info["start"] = self.start
        self._game_info["end"] = self.end
        self._game_info["vertices"] = ", ".join(sorted(self.vertices))

    def _find_all_simple_paths(self, start, end):
        """使用DFS找到所有简单路径"""
        all_paths = []
        
        def dfs(current, target, path, visited):
            if current == target:
                all_paths.append(list(path))
                return
            
            for neighbor in sorted(self.adj_list[current]):  # 按字母顺序
                if neighbor not in visited:
                    visited.add(neighbor)
                    path.append(neighbor)
                    dfs(neighbor, target, path, visited)
                    path.pop()
                    visited.remove(neighbor)
        
        dfs(start, end, [start], {start})
        return all_paths

    def _normalize_path(self, path_str):
        """标准化路径字符串为节点列表"""
        return [n.strip() for n in path_str.split("-") if n.strip()]

    def _is_valid_path(self, nodes):
        """检查节点序列是否构成有效的简单路径"""
        is_zh = self.config.language == "zh"
        
        if len(nodes) < 2:
            return False, "路径长度不足" if is_zh else "Path too short"
        
        # 检查是否有重复节点
        if len(nodes) != len(set(nodes)):
            for i, node in enumerate(nodes):
                if node in nodes[:i]:
                    if is_zh:
                        return False, f"重复节点，位置=第{i+1}步"
                    else:
                        return False, f"Duplicate node at position {i+1}"
        
        # 检查所有节点是否存在
        for i, node in enumerate(nodes):
            if node not in self.vertices:
                if is_zh:
                    return False, f"不存在的节点，位置=第{i+1}步"
                else:
                    return False, f"Invalid node at position {i+1}"
        
        # 检查相邻节点之间是否有边
        for i in range(len(nodes) - 1):
            edge = (min(nodes[i], nodes[i+1]), max(nodes[i], nodes[i+1]))
            if edge not in self.edges:
                if is_zh:
                    return False, f"不存在的边，位置=第{i+1}步"
                else:
                    return False, f"Invalid edge at position {i+1}"
        
        return True, ""

    def evaluate(self, parsed_info):
        """评估最终答案提交，仅返回 True/False，不操作 state 消息"""
        self.submission_count += 1
        
        if self.submission_count > self.max_submissions:
            return False
        
        raw_ans = parsed_info["answer"].strip()
        
        # 解析提交的路径列表
        submitted_paths = []
        if raw_ans:
            path_strs = [p.strip() for p in raw_ans.split(";") if p.strip()]
            for path_str in path_strs:
                nodes = self._normalize_path(path_str)
                submitted_paths.append(nodes)
        
        # 标准化提交的路径集合（用于比较）
        submitted_set = set()
        invalid_indices = []
        duplicate_indices = []
        
        for i, path in enumerate(submitted_paths):
            path_tuple = tuple(path)
            
            # 检查是否重复
            if path_tuple in submitted_set:
                duplicate_indices.append(i + 1)
                continue
            
            # 检查是否有效
            is_valid, _ = self._is_valid_path(path)
            if not is_valid:
                invalid_indices.append(i + 1)
                continue
            
            # 检查是否是 S-T 路径
            if len(path) < 2 or path[0] != self.start or path[-1] != self.end:
                invalid_indices.append(i + 1)
                continue
            
            submitted_set.add(path_tuple)
        
        # 标准答案集合
        answer_set = set(tuple(path) for path in self.all_paths)
        
        # 检查是否完全正确
        if submitted_set == answer_set and not invalid_indices and not duplicate_indices:
            return True
        
        # 存储反馈信息供 step() 使用
        valid_count = len(submitted_set)
        missing_count = len(answer_set - submitted_set)
        extra_count = len(submitted_set - answer_set)
        
        if self.config.language == "zh":
            feedback = f"提交结果: 未通过\n"
            feedback += f"合法且唯一的路径数: {valid_count}\n"
            if duplicate_indices:
                feedback += f"重复的路径索引: {duplicate_indices}\n"
            if invalid_indices:
                feedback += f"非法的路径索引: {invalid_indices}\n"
            feedback += f"距离完整还差: {missing_count} 条\n"
            if extra_count > 0:
                feedback += f"多余的路径: {extra_count} 条"
        else:
            feedback = f"Submission result: Failed\n"
            feedback += f"Valid and unique paths: {valid_count}\n"
            if duplicate_indices:
                feedback += f"Duplicate path indices: {duplicate_indices}\n"
            if invalid_indices:
                feedback += f"Invalid path indices: {invalid_indices}\n"
            feedback += f"Missing paths: {missing_count}\n"
            if extra_count > 0:
                feedback += f"Extra paths: {extra_count}"
        
        self._last_feedback = feedback
        return False

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑：根据查询类型产生响应"""
        responses = []
        
        # 统计本轮查询数量
        query_count_this_turn = 0
        for tag in ["query_neighbor", "query_edge", "query_degree", "query_verify", "query_expand"]:
            if tag in parsed_info:
                query_count_this_turn += 1
        
        # 更新总查询数
        self.query_count += query_count_this_turn
        
        # 检查是否超过最大查询数
        if self.query_count > self.max_queries:
            if self.config.language == "zh":
                raise ValueError(f"查询次数超过限制（{self.max_queries}次）")
            else:
                raise ValueError(f"Query count exceeded limit ({self.max_queries})")
        
        # 处理邻居查询
        if "query_neighbor" in parsed_info:
            node = parsed_info["query_neighbor"].strip()
            if node not in self.vertices:
                if self.config.language == "zh":
                    responses.append(f"邻居({node}): 无效节点")
                else:
                    responses.append(f"Neighbor({node}): Invalid node")
            else:
                neighbors = sorted(self.adj_list[node])
                if self.config.language == "zh":
                    responses.append(f"邻居({node}): [{', '.join(neighbors)}]")
                else:
                    responses.append(f"Neighbor({node}): [{', '.join(neighbors)}]")
        
        # 处理边存在查询
        if "query_edge" in parsed_info:
            try:
                parts = parsed_info["query_edge"].split(",")
                if len(parts) != 2:
                    raise ValueError
                u, v = parts[0].strip(), parts[1].strip()
                
                if u not in self.vertices or v not in self.vertices:
                    if self.config.language == "zh":
                        responses.append(f"有边({u},{v}): 无效节点")
                    else:
                        responses.append(f"HasEdge({u},{v}): Invalid node")
                else:
                    edge = (min(u, v), max(u, v))
                    exists = edge in self.edges
                    if self.config.language == "zh":
                        responses.append(f"有边({u},{v}): {'是' if exists else '否'}")
                    else:
                        responses.append(f"HasEdge({u},{v}): {'Yes' if exists else 'No'}")
            except:
                if self.config.language == "zh":
                    responses.append("有边查询格式错误")
                else:
                    responses.append("Edge query format error")
        
        # 处理度数查询
        if "query_degree" in parsed_info:
            node = parsed_info["query_degree"].strip()
            if node not in self.vertices:
                if self.config.language == "zh":
                    responses.append(f"度({node}): 无效节点")
                else:
                    responses.append(f"Degree({node}): Invalid node")
            else:
                degree = len(self.adj_list[node])
                if self.config.language == "zh":
                    responses.append(f"度({node}): {degree}")
                else:
                    responses.append(f"Degree({node}): {degree}")
        
        # 处理路径校验
        if "query_verify" in parsed_info:
            path_str = parsed_info["query_verify"].strip()
            nodes = self._normalize_path(path_str)
            is_valid, reason = self._is_valid_path(nodes)
            
            if self.config.language == "zh":
                if is_valid:
                    is_st_path = (len(nodes) >= 2 and nodes[0] == self.start and nodes[-1] == self.end)
                    responses.append(f"校验路径: 合法\n是否为 S-T: {'是' if is_st_path else '否'}")
                else:
                    responses.append(f"校验路径: 不合法({reason})")
            else:
                if is_valid:
                    is_st_path = (len(nodes) >= 2 and nodes[0] == self.start and nodes[-1] == self.end)
                    responses.append(f"Verify path: Valid\nIs S-T path: {'Yes' if is_st_path else 'No'}")
                else:
                    responses.append(f"Verify path: Invalid({reason})")
        
        # 处理前缀可扩展查询
        if "query_expand" in parsed_info:
            path_str = parsed_info["query_expand"].strip()
            nodes = self._normalize_path(path_str)
            
            # 检查前缀是否有效
            if not nodes:
                if self.config.language == "zh":
                    responses.append("可扩展: 无效前缀(原因=空路径)")
                else:
                    responses.append("Expandable: Invalid prefix(reason=empty path)")
            elif len(nodes) != len(set(nodes)):
                if self.config.language == "zh":
                    responses.append("可扩展: 无效前缀(原因=包含重复节点)")
                else:
                    responses.append("Expandable: Invalid prefix(reason=contains duplicate nodes)")
            elif any(n not in self.vertices for n in nodes):
                if self.config.language == "zh":
                    responses.append("可扩展: 无效前缀(原因=包含无效节点)")
                else:
                    responses.append("Expandable: Invalid prefix(reason=contains invalid nodes)")
            else:
                # 检查前缀路径的边连续性
                prefix_valid = True
                for i in range(len(nodes) - 1):
                    edge = (min(nodes[i], nodes[i+1]), max(nodes[i], nodes[i+1]))
                    if edge not in self.edges:
                        prefix_valid = False
                        break
                
                if not prefix_valid:
                    if self.config.language == "zh":
                        responses.append("可扩展: 无效前缀(原因=路径中存在不连通的边)")
                    else:
                        responses.append("Expandable: Invalid prefix(reason=path contains disconnected edges)")
                else:
                    # 找到可以扩展的节点（排除已访问的节点）
                    last_node = nodes[-1]
                    visited = set(nodes)
                    candidates = sorted([n for n in self.adj_list[last_node] if n not in visited])
                    
                    if self.config.language == "zh":
                        responses.append(f"可扩展: [{', '.join(candidates)}]")
                    else:
                        responses.append(f"Expandable: [{', '.join(candidates)}]")
        
        if self.config.language == "zh":
            return "\n\n".join(responses) if responses else "无有效查询"
        else:
            return "\n\n".join(responses) if responses else "No valid query"

    def _cf_make_wrong(self, correct: str) -> str:
        """根据正确答案生成错误答案"""
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 检查是否包含关键词并进行替换
        wrong = correct
        replaced = False
        
        # 中文替换
        if "是" in wrong or "否" in wrong:
            # 使用临时占位符避免重复替换
            wrong = wrong.replace("是", "TEMP_TRUE").replace("否", "是").replace("TEMP_TRUE", "否")
            replaced = True
            
        # 英文替换 (忽略大小写, 保持风格)
        lower_wrong = wrong.lower()
        if "yes" in lower_wrong or "no" in lower_wrong:
            # 针对常见的 "Yes"/"No" 大小写情况处理
            wrong = wrong.replace("Yes", "TEMP_YES").replace("No", "Yes").replace("TEMP_YES", "No")
            wrong = wrong.replace("yes", "TEMP_yes").replace("no", "yes").replace("TEMP_yes", "no")
            # 简单处理全大写情况（如果有）
            wrong = wrong.replace("YES", "TEMP_YES_CAP").replace("NO", "YES").replace("TEMP_YES_CAP", "NO")
            replaced = True
            
        if replaced:
            return wrong
            
        # 都不匹配则追加后缀
        return correct + "_WRONG"

    def step(self, response: str):
        """执行一步游戏"""
        try:
            parsed_info = self.parse(response)
            
            # 如果是答案提交
            if "answer" in parsed_info:
                is_success = self.evaluate(parsed_info)
                if is_success:
                    if self.config.language == "zh":
                        res = "提交结果: 通过\n答案完全正确！"
                    else:
                        res = "Submission result: Passed\nAnswer is completely correct!"
                    self.state.set_state("success", "success")
                    self.state.add_message("user", res)
                else:
                    if self.submission_count >= self.max_submissions:
                        feedback = getattr(self, '_last_feedback', '')
                        if self.config.language == "zh":
                            self.state.add_message("user", feedback + "\n已达到最大提交次数，游戏失败。")
                        else:
                            self.state.add_message("user", feedback + "\nMaximum submissions reached. Game failed.")
                        self.state.set_state("failed", "max submissions exceeded")
                    else:
                        feedback = getattr(self, '_last_feedback', '')
                        self.state.add_message("user", feedback)
            else:
                # 处理普通查询
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))
        
        return self.state

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        queries = []
        lang = self.config.language
        
        # 1. 邻居查询 (Neighbor Query)
        for v in sorted(self.vertices):
            q_str = f"<query_neighbor>{v}</query_neighbor>"
            neighbors = sorted(self.adj_list[v])
            if lang == "zh":
                ans = f"邻居({v}): [{', '.join(neighbors)}]"
            else:
                ans = f"Neighbor({v}): [{', '.join(neighbors)}]"
            queries.append({"query": q_str, "answer": ans})

        # 2. 度数查询 (Degree Query)
        for v in sorted(self.vertices):
            q_str = f"<query_degree>{v}</query_degree>"
            degree = len(self.adj_list[v])
            if lang == "zh":
                ans = f"度({v}): {degree}"
            else:
                ans = f"Degree({v}): {degree}"
            queries.append({"query": q_str, "answer": ans})

        # 3. 边存在查询 (Edge Existence Query)
        # 枚举所有唯一的节点对 (u, v) 其中 u < v
        verts = sorted(list(self.vertices))
        for i in range(len(verts)):
            for j in range(i + 1, len(verts)):
                u, v = verts[i], verts[j]
                q_str = f"<query_edge>{u},{v}</query_edge>"
                exists = (u, v) in self.edges  # self.edges 存储的是 (min, max)
                if lang == "zh":
                    ans = f"有边({u},{v}): {'是' if exists else '否'}"
                else:
                    ans = f"HasEdge({u},{v}): {'Yes' if exists else 'No'}"
                queries.append({"query": q_str, "answer": ans})

        # 4. 路径相关查询 (Path Verify & Expand)
        # 枚举从起点 S 开始的所有简单路径
        # 由于图规模较小，直接DFS枚举是可行的
        all_simple_paths_from_start = []
        
        def dfs(current_node, current_path, visited):
            all_simple_paths_from_start.append(list(current_path))
            
            for neighbor in sorted(self.adj_list[current_node]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    current_path.append(neighbor)
                    dfs(neighbor, current_path, visited)
                    current_path.pop()
                    visited.remove(neighbor)
        
        dfs(self.start, [self.start], {self.start})
        
        for path in all_simple_paths_from_start:
            path_str = "-".join(path)
            
            # 4.1 路径校验 (Query Verify)
            # 既然是从图中遍历出来的，必然是 Valid 的
            # 只需判断是否为 S-T 路径
            is_st = (len(path) >= 2 and path[0] == self.start and path[-1] == self.end)
            q_verify = f"<query_verify>{path_str}</query_verify>"
            
            if lang == "zh":
                ans_verify = f"校验路径: 合法\n是否为 S-T: {'是' if is_st else '否'}"
            else:
                ans_verify = f"Verify path: Valid\nIs S-T path: {'Yes' if is_st else 'No'}"
            queries.append({"query": q_verify, "answer": ans_verify})
            
            # 4.2 前缀扩展 (Query Expand)
            # 计算可扩展的下一跳节点
            last_node = path[-1]
            visited_set = set(path)
            candidates = sorted([n for n in self.adj_list[last_node] if n not in visited_set])
            
            q_expand = f"<query_expand>{path_str}</query_expand>"
            if lang == "zh":
                ans_expand = f"可扩展: [{', '.join(candidates)}]"
            else:
                ans_expand = f"Expandable: [{', '.join(candidates)}]"
            queries.append({"query": q_expand, "answer": ans_expand})

        return queries