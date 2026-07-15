import re
from .base import Game

class TopologicalOrderInferenceGame(Game):

    game_rule_zh = """\
我们来玩一个"有向图推理"游戏，规则如下：

游戏设定了6个元素，标号为 A, B, C, D, E, F。存在一个隐藏的有向图，顶点集为这6个元素。该图必定是下列四个候选有向边集合之一（且仅此四种）：
- S1 边集：A→C, B→C, C→D, C→F, D→E, E→F
- S2 边集：A→C, B→C, C→D, C→F, D→F, F→E
- S3 边集：A→C, B→C, C→D, C→F, D→E, E→D, E→F
- S4 边集：A→C, B→C, C→D, C→F, F→D, D→E

初始状态下，已选择集合为空集。

**状态与操作规则：**
- 选择操作：若在隐藏图中指向某元素 X 的所有直接前驱已全部在当前已选择集合中，则可成功选择 X，并将 X 加入已选择集合；否则操作失败，状态不变。
- 已选择的元素不会被移除，除非执行重置操作。

**你可以发起的交互请求：**

1. 动作类（改变状态）：
   - 选择 X（X 为 A, B, C, D, E, F 中的一个）
   - 重置（将已选择集合清空）

2. 查询类（不改变状态）：
   - 询问当前可选择的数量（返回满足直接前驱已全部被选择的顶点个数）

3. 最终宣告：
   - 指定候选图 Si（i 为 1, 2, 3, 4），并给出一个覆盖全部6个顶点的有效拓扑序列；或
   - 指定候选图 Si，并宣告该图不存在完整拓扑序（即图中存在环）

**询问与提交答案的格式（必须严格遵守）：**

每次询问只能包含一个标签，使用以下 XML 格式：

- 选择元素（例如选择 A）：
<action_select>A</action_select>

- 重置状态：
<action_reset></action_reset>

- 查询当前可选择数量：
<query_count></query_count>

- 提交最终答案时，必须指定候选图编号（1, 2, 3, 4）和拓扑序列（若存在），格式如下：
<answer>graph=1, sequence=A,B,C,D,E,F</answer>

- 若认为图中存在环，无法完成完整拓扑序，则格式如下：
<answer>graph=3, has_cycle=true</answer>

**你的目标：**
通过尽可能少的选择尝试和查询，推断出真实的隐藏图，并给出正确的最终宣告。
"""

    game_rule_en = """\
Let's play a "Directed Graph Inference" game. Here are the rules:

There are 6 elements labeled A, B, C, D, E, F. A hidden directed graph exists with these elements as vertices. The graph is exactly one of the following four candidate edge sets (and only these four):
- S1 edges: A→C, B→C, C→D, C→F, D→E, E→F
- S2 edges: A→C, B→C, C→D, C→F, D→F, F→E
- S3 edges: A→C, B→C, C→D, C→F, D→E, E→D, E→F
- S4 edges: A→C, B→C, C→D, C→F, F→D, D→E

Initially, the selected set is empty.

**State and Operation Rules:**
- Select operation: If all direct predecessors of element X in the hidden graph are already in the current selected set, then X can be successfully selected and added to the selected set; otherwise, the operation fails and the state remains unchanged.
- Selected elements are not removed unless a reset operation is performed.

**Interactions you can initiate:**

1. Action type (changes state):
   - Select X (where X is one of A, B, C, D, E, F)
   - Reset (clear the selected set)

2. Query type (does not change state):
   - Ask for the count of currently selectable elements (returns the number of vertices whose direct predecessors have all been selected)

3. Final declaration:
   - Specify candidate graph Si (i is 1, 2, 3, or 4) and provide a valid topological sequence covering all 6 vertices; or
   - Specify candidate graph Si and declare that no complete topological order exists (i.e., the graph contains a cycle)

**Query and Answer Format (must be strictly followed):**

Each query must contain only one tag, using the following XML format:

- Select an element (e.g., select A):
<action_select>A</action_select>

- Reset state:
<action_reset></action_reset>

- Query current selectable count:
<query_count></query_count>

- Submit final answer with graph ID (1, 2, 3, 4) and topological sequence (if exists):
<answer>graph=1, sequence=A,B,C,D,E,F</answer>

- If you believe the graph contains a cycle and no complete topological order exists:
<answer>graph=3, has_cycle=true</answer>

**Your objective:**
Through as few selection attempts and queries as possible, infer the true hidden graph and provide the correct final declaration.
"""

    contextualized_rule_zh_1 = """\
欢迎进入“城市交通路网拓扑分析系统”。我们需要排查交通枢纽之间的单向通行依赖限制。
系统设定了6个交通枢纽，标号为 A, B, C, D, E, F。存在一个隐藏的单向路线图，顶点集为这6个枢纽。该路线图必定是下列四个候选有向边集合之一（且仅此四种）：
- S1 边集：A→C, B→C, C→D, C→F, D→E, E→F
- S2 边集：A→C, B→C, C→D, C→F, D→F, F→E
- S3 边集：A→C, B→C, C→D, C→F, D→E, E→D, E→F
- S4 边集：A→C, B→C, C→D, C→F, F→D, D→E

初始状态下，已放行枢纽集合为空集。

**状态与操作规则：**
- 放行操作（选择）：若在隐藏路线图中指向某枢纽 X 的所有直接上游枢纽已全部在当前已放行集合中，则可成功放行 X，并将 X 加入已放行集合；否则操作失败，状态不变。
- 已放行的枢纽不会被移除，除非执行重置操作。

**你可以发起的交互请求：**

1. 动作类（改变状态）：
   - 选择 X（X 为 A, B, C, D, E, F 中的一个，代表尝试放行该枢纽）
   - 重置（将已放行集合清空，即重新封锁所有枢纽）

2. 查询类（不改变状态）：
   - 询问当前可放行的数量（返回满足直接上游已全部被放行的枢纽个数）

3. 最终宣告：
   - 指定候选路线图 Si（i 为 1, 2, 3, 4），并给出一个覆盖全部6个枢纽的有效拓扑序列（即放行顺序）；或
   - 指定候选路线图 Si，并宣告该图中存在死锁环（不存在完整拓扑序）

**询问与提交答案的格式（必须严格遵守）：**

每次询问只能包含一个标签，使用以下 XML 格式：

- 选择枢纽（例如选择 A）：
<action_select>A</action_select>

- 重置状态：
<action_reset></action_reset>

- 查询当前可放行数量：
<query_count></query_count>

- 提交最终答案时，必须指定候选图编号（1, 2, 3, 4）和拓扑序列（若存在），格式如下：
<answer>graph=1, sequence=A,B,C,D,E,F</answer>

- 若认为路线图中存在环导致死锁，无法完成完整拓扑序，则格式如下：
<answer>graph=3, has_cycle=true</answer>

**你的目标：**
通过尽可能少的尝试和查询，推断出真实的隐藏路线图，并给出正确的最终宣告。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Urban Traffic Network Topology Analysis System". We need to determine the one-way transit dependencies between traffic hubs.
The system defines 6 transit hubs, labeled A, B, C, D, E, F. A hidden one-way route graph exists with these hubs as vertices. The route graph is exactly one of the following four candidate directed edge sets (and only these four):
- S1 edges: A→C, B→C, C→D, C→F, D→E, E→F
- S2 edges: A→C, B→C, C→D, C→F, D→F, F→E
- S3 edges: A→C, B→C, C→D, C→F, D→E, E→D, E→F
- S4 edges: A→C, B→C, C→D, C→F, F→D, D→E

Initially, the cleared hub set is empty.

**State and Operation Rules:**
- Dispatch operation (Select): If all direct upstream hubs of hub X in the hidden route graph are already in the currently cleared set, then X can be successfully dispatched and added to the cleared set; otherwise, the operation fails and the state remains unchanged.
- Cleared hubs are not removed unless a reset operation is performed.

**Interactions you can initiate:**

1. Action type (changes state):
   - Select X (where X is one of A, B, C, D, E, F, attempting to dispatch this hub)
   - Reset (clear the cleared set, effectively locking all hubs again)

2. Query type (does not change state):
   - Ask for the count of currently dispatchable hubs (returns the number of hubs whose upstream dependencies have all been cleared)

3. Final declaration:
   - Specify candidate graph Si (i is 1, 2, 3, or 4) and provide a valid topological sequence (dispatch order) covering all 6 hubs; or
   - Specify candidate graph Si and declare that a deadlock cycle exists (no complete topological order exists)

**Query and Answer Format (must be strictly followed):**

Each query must contain only one tag, using the following XML format:

- Select a hub (e.g., select A):
<action_select>A</action_select>

- Reset state:
<action_reset></action_reset>

- Query current dispatchable count:
<query_count></query_count>

- Submit final answer with graph ID (1, 2, 3, 4) and topological sequence (if exists):
<answer>graph=1, sequence=A,B,C,D,E,F</answer>

- If you believe the route graph contains a deadlock cycle and no complete topological order exists:
<answer>graph=3, has_cycle=true</answer>

**Your objective:**
Through as few attempts and queries as possible, infer the true hidden route graph and provide the correct final declaration.
"""

    contextualized_rule_zh_2 = """\
欢迎进入“临床路径依赖分析系统”。我们需要梳理医疗流程节点之间的先决条件。
系统设定了6个医疗流程，标号为 A, B, C, D, E, F。存在一个隐藏的流程依赖图，顶点集为这6个流程。该流程图必定是下列四个候选有向边集合之一（且仅此四种）：
- S1 边集：A→C, B→C, C→D, C→F, D→E, E→F
- S2 边集：A→C, B→C, C→D, C→F, D→F, F→E
- S3 边集：A→C, B→C, C→D, C→F, D→E, E→D, E→F
- S4 边集：A→C, B→C, C→D, C→F, F→D, D→E

初始状态下，已执行流程集合为空集。

**状态与操作规则：**
- 执行操作（选择）：若在隐藏流程图中指向某流程 X 的所有直接前置流程已全部在当前已执行集合中，则可成功执行 X，并将 X 加入已执行集合；否则操作失败，状态不变。
- 已执行的流程不会被撤销，除非执行重置操作。

**你可以发起的交互请求：**

1. 动作类（改变状态）：
   - 选择 X（X 为 A, B, C, D, E, F 中的一个，代表尝试执行该流程）
   - 重置（将已执行集合清空）

2. 查询类（不改变状态）：
   - 询问当前可执行的数量（返回满足直接前置已全部被执行的流程个数）

3. 最终宣告：
   - 指定候选流程图 Si（i 为 1, 2, 3, 4），并给出一个覆盖全部6个流程的有效拓扑序列（即执行顺序）；或
   - 指定候选流程图 Si，并宣告该图中存在循环依赖（不存在完整拓扑序）

**询问与提交答案的格式（必须严格遵守）：**

每次询问只能包含一个标签，使用以下 XML 格式：

- 选择流程（例如选择 A）：
<action_select>A</action_select>

- 重置状态：
<action_reset></action_reset>

- 查询当前可执行数量：
<query_count></query_count>

- 提交最终答案时，必须指定候选图编号（1, 2, 3, 4）和拓扑序列（若存在），格式如下：
<answer>graph=1, sequence=A,B,C,D,E,F</answer>

- 若认为流程图中存在循环依赖，无法完成完整拓扑序，则格式如下：
<answer>graph=3, has_cycle=true</answer>

**你的目标：**
通过尽可能少的尝试和查询，推断出真实的隐藏流程图，并给出正确的最终宣告。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Clinical Pathway Dependency Analysis System". We need to map out the prerequisites between medical procedures.
The system defines 6 medical procedures, labeled A, B, C, D, E, F. A hidden procedure dependency graph exists with these procedures as vertices. The dependency graph is exactly one of the following four candidate directed edge sets (and only these four):
- S1 edges: A→C, B→C, C→D, C→F, D→E, E→F
- S2 edges: A→C, B→C, C→D, C→F, D→F, F→E
- S3 edges: A→C, B→C, C→D, C→F, D→E, E→D, E→F
- S4 edges: A→C, B→C, C→D, C→F, F→D, D→E

Initially, the completed procedure set is empty.

**State and Operation Rules:**
- Execution operation (Select): If all direct prerequisite procedures of procedure X in the hidden dependency graph are already in the currently completed set, then X can be successfully executed and added to the completed set; otherwise, the operation fails and the state remains unchanged.
- Completed procedures are not revoked unless a reset operation is performed.

**Interactions you can initiate:**

1. Action type (changes state):
   - Select X (where X is one of A, B, C, D, E, F, attempting to execute this procedure)
   - Reset (clear the completed set)

2. Query type (does not change state):
   - Ask for the count of currently executable procedures (returns the number of procedures whose prerequisites have all been completed)

3. Final declaration:
   - Specify candidate graph Si (i is 1, 2, 3, or 4) and provide a valid topological sequence (execution order) covering all 6 procedures; or
   - Specify candidate graph Si and declare that a circular dependency exists (no complete topological order exists)

**Query and Answer Format (must be strictly followed):**

Each query must contain only one tag, using the following XML format:

- Select a procedure (e.g., select A):
<action_select>A</action_select>

- Reset state:
<action_reset></action_reset>

- Query current executable count:
<query_count></query_count>

- Submit final answer with graph ID (1, 2, 3, 4) and topological sequence (if exists):
<answer>graph=1, sequence=A,B,C,D,E,F</answer>

- If you believe the dependency graph contains a circular dependency and no complete topological order exists:
<answer>graph=3, has_cycle=true</answer>

**Your objective:**
Through as few attempts and queries as possible, infer the true hidden dependency graph and provide the correct final declaration.
"""

    contextualized_rule_zh_3 = """\
欢迎使用“课程先修体系分析系统”。我们需要排查核心课程模块之间的先决选课限制。
系统设定了6个课程模块，标号为 A, B, C, D, E, F。存在一个隐藏的先修关系图，顶点集为这6个课程。该关系图必定是下列四个候选有向边集合之一（且仅此四种）：
- S1 边集：A→C, B→C, C→D, C→F, D→E, E→F
- S2 边集：A→C, B→C, C→D, C→F, D→F, F→E
- S3 边集：A→C, B→C, C→D, C→F, D→E, E→D, E→F
- S4 边集：A→C, B→C, C→D, C→F, F→D, D→E

初始状态下，已修读课程集合为空集。

**状态与操作规则：**
- 修读操作（选择）：若在隐藏关系图中指向某课程 X 的所有直接先修课程已全部在当前已修读集合中，则可成功修读 X，并将 X 加入已修读集合；否则操作失败，状态不变。
- 已修读的课程不会被移除，除非执行重置操作。

**你可以发起的交互请求：**

1. 动作类（改变状态）：
   - 选择 X（X 为 A, B, C, D, E, F 中的一个，代表尝试修读该课程）
   - 重置（将已修读集合清空）

2. 查询类（不改变状态）：
   - 询问当前可修读的数量（返回满足直接先修课程已全部被修读的课程个数）

3. 最终宣告：
   - 指定候选关系图 Si（i 为 1, 2, 3, 4），并给出一个覆盖全部6个课程的有效拓扑序列（即修读顺序）；或
   - 指定候选关系图 Si，并宣告该图中存在先修死循环（不存在完整拓扑序）

**询问与提交答案的格式（必须严格遵守）：**

每次询问只能包含一个标签，使用以下 XML 格式：

- 选择课程（例如选择 A）：
<action_select>A</action_select>

- 重置状态：
<action_reset></action_reset>

- 查询当前可修读数量：
<query_count></query_count>

- 提交最终答案时，必须指定候选图编号（1, 2, 3, 4）和拓扑序列（若存在），格式如下：
<answer>graph=1, sequence=A,B,C,D,E,F</answer>

- 若认为关系图中存在死循环，无法完成完整拓扑序，则格式如下：
<answer>graph=3, has_cycle=true</answer>

**你的目标：**
通过尽可能少的尝试和查询，推断出真实的隐藏关系图，并给出正确的最终宣告。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Curriculum Prerequisite Analysis System". We need to verify the enrollment prerequisites among core course modules.
The system defines 6 course modules, labeled A, B, C, D, E, F. A hidden prerequisite graph exists with these courses as vertices. The prerequisite graph is exactly one of the following four candidate directed edge sets (and only these four):
- S1 edges: A→C, B→C, C→D, C→F, D→E, E→F
- S2 edges: A→C, B→C, C→D, C→F, D→F, F→E
- S3 edges: A→C, B→C, C→D, C→F, D→E, E→D, E→F
- S4 edges: A→C, B→C, C→D, C→F, F→D, D→E

Initially, the passed course set is empty.

**State and Operation Rules:**
- Enrollment operation (Select): If all direct prerequisite courses of course X in the hidden graph are already in the currently passed set, then X can be successfully enrolled and added to the passed set; otherwise, the operation fails and the state remains unchanged.
- Passed courses are not removed unless a reset operation is performed.

**Interactions you can initiate:**

1. Action type (changes state):
   - Select X (where X is one of A, B, C, D, E, F, attempting to enroll in this course)
   - Reset (clear the passed set)

2. Query type (does not change state):
   - Ask for the count of currently enrollable courses (returns the number of courses whose prerequisites have all been passed)

3. Final declaration:
   - Specify candidate graph Si (i is 1, 2, 3, or 4) and provide a valid topological sequence (enrollment order) covering all 6 courses; or
   - Specify candidate graph Si and declare that a prerequisite loop exists (no complete topological order exists)

**Query and Answer Format (must be strictly followed):**

Each query must contain only one tag, using the following XML format:

- Select a course (e.g., select A):
<action_select>A</action_select>

- Reset state:
<action_reset></action_reset>

- Query current enrollable count:
<query_count></query_count>

- Submit final answer with graph ID (1, 2, 3, 4) and topological sequence (if exists):
<answer>graph=1, sequence=A,B,C,D,E,F</answer>

- If you believe the prerequisite graph contains a loop and no complete topological order exists:
<answer>graph=3, has_cycle=true</answer>

**Your objective:**
Through as few attempts and queries as possible, infer the true hidden prerequisite graph and provide the correct final declaration.
"""

    contextualized_rule_zh_4 = """\
欢迎使用“工业流水线工艺排程系统”。我们需要排查生产工序之间的加工依赖关系。
系统设定了6个生产工序，标号为 A, B, C, D, E, F。存在一个隐藏的工艺流程图，顶点集为这6个工序。该流程图必定是下列四个候选有向边集合之一（且仅此四种）：
- S1 边集：A→C, B→C, C→D, C→F, D→E, E→F
- S2 边集：A→C, B→C, C→D, C→F, D→F, F→E
- S3 边集：A→C, B→C, C→D, C→F, D→E, E→D, E→F
- S4 边集：A→C, B→C, C→D, C→F, F→D, D→E

初始状态下，已完成工序集合为空集。

**状态与操作规则：**
- 投产操作（选择）：若在隐藏流程图中指向某工序 X 的所有直接前置工序已全部在当前已完成集合中，则可成功投产 X，并将 X 加入已完成集合；否则操作失败，状态不变。
- 已完成的工序不会被重置，除非执行生产线复位（重置）操作。

**你可以发起的交互请求：**

1. 动作类（改变状态）：
   - 选择 X（X 为 A, B, C, D, E, F 中的一个，代表尝试投产该工序）
   - 重置（将已完成集合清空）

2. 查询类（不改变状态）：
   - 询问当前可投产的数量（返回满足直接前置工序已全部完成的工序个数）

3. 最终宣告：
   - 指定候选流程图 Si（i 为 1, 2, 3, 4），并给出一个覆盖全部6个工序的有效拓扑序列（即投产顺序）；或
   - 指定候选流程图 Si，并宣告该图存在工艺死锁（不存在完整拓扑序）

**询问与提交答案的格式（必须严格遵守）：**

每次询问只能包含一个标签，使用以下 XML 格式：

- 选择工序（例如选择 A）：
<action_select>A</action_select>

- 重置状态：
<action_reset></action_reset>

- 查询当前可投产数量：
<query_count></query_count>

- 提交最终答案时，必须指定候选图编号（1, 2, 3, 4）和拓扑序列（若存在），格式如下：
<answer>graph=1, sequence=A,B,C,D,E,F</answer>

- 若认为流程图中存在工艺死锁，无法完成完整拓扑序，则格式如下：
<answer>graph=3, has_cycle=true</answer>

**你的目标：**
通过尽可能少的尝试和查询，推断出真实的隐藏流程图，并给出正确的最终宣告。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Assembly Line Workflow Scheduling System". We need to determine the processing dependencies between production stages.
The system defines 6 production stages, labeled A, B, C, D, E, F. A hidden workflow graph exists with these stages as vertices. The workflow graph is exactly one of the following four candidate directed edge sets (and only these four):
- S1 edges: A→C, B→C, C→D, C→F, D→E, E→F
- S2 edges: A→C, B→C, C→D, C→F, D→F, F→E
- S3 edges: A→C, B→C, C→D, C→F, D→E, E→D, E→F
- S4 edges: A→C, B→C, C→D, C→F, F→D, D→E

Initially, the completed stage set is empty.

**State and Operation Rules:**
- Production operation (Select): If all direct preceding stages of stage X in the hidden workflow graph are already in the currently completed set, then X can be successfully executed and added to the completed set; otherwise, the operation fails and the state remains unchanged.
- Completed stages are not reset unless a reset operation is performed.

**Interactions you can initiate:**

1. Action type (changes state):
   - Select X (where X is one of A, B, C, D, E, F, attempting to execute this stage)
   - Reset (clear the completed set)

2. Query type (does not change state):
   - Ask for the count of currently executable stages (returns the number of stages whose preceding stages have all been completed)

3. Final declaration:
   - Specify candidate graph Si (i is 1, 2, 3, or 4) and provide a valid topological sequence (production order) covering all 6 stages; or
   - Specify candidate graph Si and declare that a workflow deadlock exists (no complete topological order exists)

**Query and Answer Format (must be strictly followed):**

Each query must contain only one tag, using the following XML format:

- Select a stage (e.g., select A):
<action_select>A</action_select>

- Reset state:
<action_reset></action_reset>

- Query current executable count:
<query_count></query_count>

- Submit final answer with graph ID (1, 2, 3, 4) and topological sequence (if exists):
<answer>graph=1, sequence=A,B,C,D,E,F</answer>

- If you believe the workflow graph contains a deadlock and no complete topological order exists:
<answer>graph=3, has_cycle=true</answer>

**Your objective:**
Through as few attempts and queries as possible, infer the true hidden workflow graph and provide the correct final declaration.
"""

    contextualized_rule_zh_5 = """\
欢迎进入“司法程序依赖推理系统”。我们需要梳理法律案件中各项诉讼程序的前置条件。
系统设定了6个法定程序，标号为 A, B, C, D, E, F。存在一个隐藏的程序依赖图，顶点集为这6个程序。该依赖图必定是下列四个候选有向边集合之一（且仅此四种）：
- S1 边集：A→C, B→C, C→D, C→F, D→E, E→F
- S2 边集：A→C, B→C, C→D, C→F, D→F, F→E
- S3 边集：A→C, B→C, C→D, C→F, D→E, E→D, E→F
- S4 边集：A→C, B→C, C→D, C→F, F→D, D→E

初始状态下，已执行程序集合为空集。

**状态与操作规则：**
- 执行操作（选择）：若在隐藏依赖图中指向某程序 X 的所有直接前置程序已全部在当前已执行集合中，则可成功执行 X，并将 X 加入已执行集合；否则操作失败，状态不变。
- 已执行的程序不会被撤销，除非执行重置操作。

**你可以发起的交互请求：**

1. 动作类（改变状态）：
   - 选择 X（X 为 A, B, C, D, E, F 中的一个，代表尝试执行该法定程序）
   - 重置（将已执行程序集合清空）

2. 查询类（不改变状态）：
   - 询问当前可执行的数量（返回满足直接前置程序已全部被执行的法定程序个数）

3. 最终宣告：
   - 指定候选依赖图 Si（i 为 1, 2, 3, 4），并给出一个覆盖全部6个程序的有效拓扑序列（即执行顺序）；或
   - 指定候选依赖图 Si，并宣告该图中存在程序死循环（不存在完整拓扑序）

**询问与提交答案的格式（必须严格遵守）：**

每次询问只能包含一个标签，使用以下 XML 格式：

- 选择程序（例如选择 A）：
<action_select>A</action_select>

- 重置状态：
<action_reset></action_reset>

- 查询当前可执行数量：
<query_count></query_count>

- 提交最终答案时，必须指定候选图编号（1, 2, 3, 4）和拓扑序列（若存在），格式如下：
<answer>graph=1, sequence=A,B,C,D,E,F</answer>

- 若认为依赖图中存在死循环，无法完成完整拓扑序，则格式如下：
<answer>graph=3, has_cycle=true</answer>

**你的目标：**
通过尽可能少的尝试和查询，推断出真实的隐藏依赖图，并给出正确的最终宣告。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Judicial Procedure Dependency Inference System". We need to organize the procedural prerequisites in a legal case.
The system defines 6 legal procedures, labeled A, B, C, D, E, F. A hidden procedural dependency graph exists with these procedures as vertices. The dependency graph is exactly one of the following four candidate directed edge sets (and only these four):
- S1 edges: A→C, B→C, C→D, C→F, D→E, E→F
- S2 edges: A→C, B→C, C→D, C→F, D→F, F→E
- S3 edges: A→C, B→C, C→D, C→F, D→E, E→D, E→F
- S4 edges: A→C, B→C, C→D, C→F, F→D, D→E

Initially, the executed procedure set is empty.

**State and Operation Rules:**
- Execution operation (Select): If all direct prerequisite procedures of procedure X in the hidden dependency graph are already in the currently executed set, then X can be successfully executed and added to the executed set; otherwise, the operation fails and the state remains unchanged.
- Executed procedures are not revoked unless a reset operation is performed.

**Interactions you can initiate:**

1. Action type (changes state):
   - Select X (where X is one of A, B, C, D, E, F, attempting to execute this legal procedure)
   - Reset (clear the executed set)

2. Query type (does not change state):
   - Ask for the count of currently executable procedures (returns the number of procedures whose prerequisites have all been executed)

3. Final declaration:
   - Specify candidate graph Si (i is 1, 2, 3, or 4) and provide a valid topological sequence (execution order) covering all 6 procedures; or
   - Specify candidate graph Si and declare that a procedural loop exists (no complete topological order exists)

**Query and Answer Format (must be strictly followed):**

Each query must contain only one tag, using the following XML format:

- Select a procedure (e.g., select A):
<action_select>A</action_select>

- Reset state:
<action_reset></action_reset>

- Query current executable count:
<query_count></query_count>

- Submit final answer with graph ID (1, 2, 3, 4) and topological sequence (if exists):
<answer>graph=1, sequence=A,B,C,D,E,F</answer>

- If you believe the dependency graph contains a loop and no complete topological order exists:
<answer>graph=3, has_cycle=true</answer>

**Your objective:**
Through as few attempts and queries as possible, infer the true hidden dependency graph and provide the correct final declaration.
"""

    tags = ["answer", "action_select", "action_reset", "query_count"]
    
    reasoning_type = "溯因推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "graph_id": 1,
                "edges": [("A", "C"), ("B", "C"), ("C", "D"), ("C", "F"), ("D", "E"), ("E", "F")],
                "has_cycle": False,
            },
            2: {
                "graph_id": 2,
                "edges": [("A", "C"), ("B", "C"), ("C", "D"), ("C", "F"), ("D", "F"), ("F", "E")],
                "has_cycle": False,
            },
            3: {
                "graph_id": 4,
                "edges": [("A", "C"), ("B", "C"), ("C", "D"), ("C", "F"), ("F", "D"), ("D", "E")],
                "has_cycle": False,
            },
            4: {
                "graph_id": 3,
                "edges": [("A", "C"), ("B", "C"), ("C", "D"), ("C", "F"), ("D", "E"), ("E", "D"), ("E", "F")],
                "has_cycle": True,
            },
            5: {
                "graph_id": 3,
                "edges": [("A", "C"), ("B", "C"), ("C", "D"), ("C", "F"), ("D", "E"), ("E", "D"), ("E", "F")],
                "has_cycle": True,
            },
        },
        "en": {
            1: {
                "graph_id": 1,
                "edges": [("A", "C"), ("B", "C"), ("C", "D"), ("C", "F"), ("D", "E"), ("E", "F")],
                "has_cycle": False,
            },
            2: {
                "graph_id": 2,
                "edges": [("A", "C"), ("B", "C"), ("C", "D"), ("C", "F"), ("D", "F"), ("F", "E")],
                "has_cycle": False,
            },
            3: {
                "graph_id": 4,
                "edges": [("A", "C"), ("B", "C"), ("C", "D"), ("C", "F"), ("F", "D"), ("D", "E")],
                "has_cycle": False,
            },
            4: {
                "graph_id": 3,
                "edges": [("A", "C"), ("B", "C"), ("C", "D"), ("C", "F"), ("D", "E"), ("E", "D"), ("E", "F")],
                "has_cycle": True,
            },
            5: {
                "graph_id": 3,
                "edges": [("A", "C"), ("B", "C"), ("C", "D"), ("C", "F"), ("D", "E"), ("E", "D"), ("E", "F")],
                "has_cycle": True,
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
        
        self.true_graph_id = cfg["graph_id"]
        self.edges = cfg["edges"]
        self.has_cycle = cfg["has_cycle"]
        
        self.vertices = {"A", "B", "C", "D", "E", "F"}
        self.predecessors = {v: set() for v in self.vertices}
        for src, dst in self.edges:
            self.predecessors[dst].add(src)
        
        self.selected = set()
        
        self._game_info = {}

    def _can_select(self, vertex):
        if vertex in self.selected:
            return False
        required = self.predecessors[vertex]
        return required.issubset(self.selected)

    def _get_selectable_count(self):
        count = 0
        for v in self.vertices:
            if self._can_select(v):
                count += 1
        return count

    def evaluate(self, parsed_info):
        if "answer" not in parsed_info:
            return False
            
        raw_ans = parsed_info["answer"].strip()
        
        ans_dict = {}
        
        graph_match = re.search(r'graph\s*=\s*(\d+)', raw_ans)
        if graph_match:
            ans_dict["graph"] = graph_match.group(1)
        
        cycle_match = re.search(r'has_cycle\s*=\s*(\w+)', raw_ans)
        if cycle_match:
            ans_dict["has_cycle"] = cycle_match.group(1)
        
        seq_match = re.search(r'sequence\s*=\s*([A-Fa-f,\s]+)', raw_ans)
        if seq_match:
            ans_dict["sequence"] = seq_match.group(1).strip().rstrip(",")
        
        if "graph" not in ans_dict:
            return False
        
        try:
            graph_id = int(ans_dict["graph"])
        except Exception:
            return False
        
        if graph_id != self.true_graph_id:
            return False
        
        if "has_cycle" in ans_dict:
            declared_has_cycle = ans_dict["has_cycle"].lower() in ["true", "yes", "是"]
            if declared_has_cycle != self.has_cycle:
                return False
            if declared_has_cycle:
                return True
        
        if "sequence" not in ans_dict:
            if not self.has_cycle:
                return False
            return False
        
        try:
            sequence = [x.strip().upper() for x in ans_dict["sequence"].split(",") if x.strip()]
        except Exception:
            return False
        
        if set(sequence) != self.vertices or len(sequence) != 6:
            return False
        
        if not self._is_valid_topological_order(sequence):
            return False
        
        if self.has_cycle:
            return False
        
        return True

    def _is_valid_topological_order(self, sequence):
        pos = {v: i for i, v in enumerate(sequence)}
        
        for src, dst in self.edges:
            if pos[src] >= pos[dst]:
                return False
        
        return True

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        lang = self.config.language
        
        if lang == "zh":
            success_prefix = "成功；当前已选择："
            fail_prefix = "失败；当前已选择："
        else:
            success_prefix = "Success; currently selected: "
            fail_prefix = "Failed; currently selected: "

        sim_selected = set()
        sorted_vertices = sorted(list(self.vertices))
        
        count = sum(1 for v in self.vertices 
                    if v not in sim_selected and self.predecessors[v].issubset(sim_selected))
        results.append({
            "query": "<query_count></query_count>",
            "answer": str(count)
        })
        
        max_iterations = 12
        iteration = 0
        while iteration < max_iterations:
            selectable = [v for v in sorted_vertices 
                          if v not in sim_selected and self.predecessors[v].issubset(sim_selected)]
            
            if not selectable:
                remaining = [v for v in sorted_vertices if v not in sim_selected]
                if remaining:
                    v = remaining[0]
                    current_str = ",".join(sorted(sim_selected)) if sim_selected else ""
                    resp = f"{fail_prefix}{{{current_str}}}"
                    results.append({
                        "query": f"<action_select>{v}</action_select>",
                        "answer": resp
                    })
                break
            
            v = selectable[0]
            sim_selected.add(v)
            current_str = ",".join(sorted(sim_selected))
            resp = f"{success_prefix}{{{current_str}}}"
            results.append({
                "query": f"<action_select>{v}</action_select>",
                "answer": resp
            })
            
            count = sum(1 for vtx in self.vertices 
                        if vtx not in sim_selected and self.predecessors[vtx].issubset(sim_selected))
            results.append({
                "query": "<query_count></query_count>",
                "answer": str(count)
            })
            
            iteration += 1
            
            if len(sim_selected) == len(self.vertices):
                break
        
        return results

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            success_prefix = "成功；当前已选择："
            fail_prefix = "失败；当前已选择："
            reset_prefix = "已重置；当前已选择："
            invalid_vertex = "错误：无效的元素标号。"
            current_selected = "{{{}}}".format(",".join(sorted(self.selected)) if self.selected else "")
        else:
            success_prefix = "Success; currently selected: "
            fail_prefix = "Failed; currently selected: "
            reset_prefix = "Reset; currently selected: "
            invalid_vertex = "Error: Invalid vertex label."
            current_selected = "{{{}}}".format(",".join(sorted(self.selected)) if self.selected else "")

        if "action_select" in parsed_info:
            vertex = parsed_info["action_select"].strip().upper()
            if vertex not in self.vertices:
                return invalid_vertex
            
            if self._can_select(vertex):
                self.selected.add(vertex)
                current_selected = "{{{}}}".format(",".join(sorted(self.selected)))
                return success_prefix + current_selected
            else:
                return fail_prefix + current_selected

        elif "action_reset" in parsed_info:
            self.selected = set()
            return reset_prefix + "{}"

        elif "query_count" in parsed_info:
            count = self._get_selectable_count()
            return str(count)

        else:
            raise ValueError("No valid action or query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.strip().isdigit():
            return str(int(correct.strip()) + 1)

        lang = self.config.language

        if lang == "zh":
            if correct.startswith("成功"):
                return correct.replace("成功", "失败", 1)
            if correct.startswith("失败"):
                return correct.replace("失败", "成功", 1)
            if correct.startswith("已重置"):
                return correct + "_WRONG"
        else:
            if correct.startswith("Success"):
                return correct.replace("Success", "Failed", 1)
            if correct.startswith("Failed"):
                return correct.replace("Failed", "Success", 1)
            if correct.startswith("Reset"):
                return correct + "_WRONG"

        return correct + "_WRONG"