# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   遍历相对顺序：两个节点在某种遍历下谁先被访问
# ============================================================

from .base import Game
import random


class TreeTraversalOrderGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"树遍历顺序推理"游戏，规则如下：

游戏设定了一棵有根树，共有 {n} 个节点，编号为 1 到 {n}，根节点的父节点为 0。树的先序遍历规则为：访问当前节点后，按子节点编号从小到大的顺序依次递归访问每个子节点。

我已选定两个不同的节点 A={a} 和 B={b}。你的目标是判断在先序遍历中，A 和 B 谁先被访问，并给出简明理由。

树的具体结构对你是未知的，但它是固定不变的。你可以反复向我提出以下四类查询（每次仅限一个查询），我会根据真实的树结构如实回答：

1. 上级查询：询问节点 x 的父节点编号。返回整数 p（0 表示 x 是根节点）。
2. 子数查询：询问节点 x 有多少个直属子节点。返回非负整数 c。
3. 定位子节点：询问节点 x 的第 k 个子节点（按编号升序排列）。若 k 合法则返回该子节点编号，否则返回 0。
4. 祖先判定：询问节点 u 是否为节点 v 的祖先（每个节点是其自身祖先）。返回"是"或"否"。

你不能直接询问节点间在先序遍历中的相对先后顺序。

当你收集足够信息后，请提交最终判断和理由。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 上级查询（例如询问节点 5 的父节点）：
<query_parent>5</query_parent>

- 子数查询（例如询问节点 3 有多少个子节点）：
<query_child_count>3</query_child_count>

- 定位子节点（例如询问节点 2 的第 1 个子节点）：
<query_kth_child>2,1</query_kth_child>

- 祖先判定（例如询问节点 1 是否为节点 5 的祖先）：
<query_is_ancestor>1,5</query_is_ancestor>

提交最终答案时，必须说明先访问的节点（A 或 B）并附带简明理由，格式如下：

<answer>first=A, reason=A是B的祖先因此A先于B</answer>
"""

    game_rule_en = """\
Let's play a "Tree Traversal Order Reasoning" game. Here are the rules:

The game is based on a rooted tree with {n} nodes numbered from 1 to {n}, where the root's parent is 0. The preorder traversal rule is: visit the current node first, then recursively visit each child in ascending order of their node numbers.

I have selected two different nodes A={a} and B={b}. Your goal is to determine which one is visited first in the preorder traversal and provide a brief reason.

The tree structure is unknown to you but remains fixed. You can repeatedly ask me four types of queries (one per turn), and I will answer truthfully based on the actual tree structure:

1. Parent Query: Ask for the parent node number of node x. Returns integer p (0 means x is the root).
2. Child Count Query: Ask how many direct children node x has. Returns non-negative integer c.
3. Kth Child Query: Ask for the k-th child of node x (sorted by node number in ascending order). Returns the child's number if k is valid, otherwise 0.
4. Ancestor Query: Ask whether node u is an ancestor of node v (each node is its own ancestor). Returns "Yes" or "No".

You cannot directly ask about the relative order of nodes in the preorder traversal.

When you have enough information, submit your final judgment and reason. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Parent Query (e.g., asking for the parent of node 5):
<query_parent>5</query_parent>

- Child Count Query (e.g., asking how many children node 3 has):
<query_child_count>3</query_child_count>

- Kth Child Query (e.g., asking for the 1st child of node 2):
<query_kth_child>2,1</query_kth_child>

- Ancestor Query (e.g., asking if node 1 is an ancestor of node 5):
<query_is_ancestor>1,5</query_is_ancestor>

When submitting the final answer, specify which node is visited first (A or B) and provide a brief reason, using this format:

<answer>first=A, reason=A is an ancestor of B so A comes before B</answer>
"""

    # ================= 场景 1：交通 =================
    contextualized_rule_zh_1 = """\
欢迎进入物流调度控制系统。

系统内设有一个由 {n} 个中转枢纽和站点组成的物流配送树形网络，编号为 1 到 {n}，总指挥部的父节点为 0。配送车辆的路径规划遵循严格的调度原则：到达当前枢纽后，会按下辖站点编号从小到大的顺序，依次递归巡检其所有下属站点。

我已锁定两个存在异常的站点 A={a} 和 B={b}。你的任务是推断在标准的调度巡检顺序中，调度车会先排查 A 还是 B，并简述理由。

完整的网络拓扑结构对你是保密的，但它是固定不变的。你可以通过系统接口向我发起以下四类情报查询（每次仅限一次），我会基于真实的调度网络如实反馈：

1. 上级枢纽查询：询问站点 x 的直接上级调度中心编号。返回整数 p（0 表示 x 是最高级枢纽）。
2. 下辖站点数查询：询问站点 x 有多少个直属下级站点。返回非负整数 c。
3. 定位下辖站点：询问站点 x 的第 k 个直属下属站点（按编号升序排列）。若 k 合法则返回该站点编号，否则返回 0。
4. 管辖权判定：询问站点 u 是否为站点 v 的上级管辖枢纽（每个站点视为受自己管辖）。返回"是"或"否"。

你不能直接询问两个站在巡检路径上的相对先后顺序。
当你收集足够的情报后，请提交最终判定和理由。若答案错误或格式不符，排查任务失败。

## 系统查询与提交格式（必须严格遵守系统协议）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 上级枢纽查询（如查询站点 5 的上级）：
<query_parent>5</query_parent>

- 下辖站点数查询（如查询站点 3 的下级数量）：
<query_child_count>3</query_child_count>

- 定位下辖站点（如查询站点 2 的第 1 个下辖站点）：
<query_kth_child>2,1</query_kth_child>

- 管辖权判定（如查询站点 1 是否管辖站点 5）：
<query_is_ancestor>1,5</query_is_ancestor>

提交最终结果时，必须明确先巡检的站点（A 或 B）并附带简明推导逻辑，格式如下：
<answer>first=A, reason=A是B的上级管辖枢纽，因此巡检车必定先到达A</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the Logistics Scheduling Control System.

The system features a distribution network tree with {n} transit hubs and stations, numbered from 1 to {n}, where the general command center's parent is 0. The delivery vehicle's route planning follows a strict dispatch rule: it visits the current hub first, then recursively inspects each subordinate station in ascending order of their node numbers.

I have locked onto two specific anomalous stations A={a} and B={b}. Your goal is to determine which one is visited first during the standard inspection sequence, and provide a brief reason.

The complete network structure is hidden from you but remains fixed. You can repeatedly submit four types of intelligence queries to me (one per turn), and I will answer truthfully based on the actual scheduling network:

1. Parent Hub Query: Ask for the direct parent hub number of station x. Returns integer p (0 means x is the top hub).
2. Subordinate Count Query: Ask how many direct subordinate stations station x has. Returns non-negative integer c.
3. Kth Subordinate Query: Ask for the k-th direct subordinate of station x (sorted by station number in ascending order). Returns the station's number if k is valid, otherwise 0.
4. Jurisdiction Query: Ask whether station u has jurisdiction over station v as a higher-level hub (each station has jurisdiction over itself). Returns "Yes" or "No".

You cannot directly ask about the relative order of stations in the inspection route.
When you have enough intelligence, submit your final judgment and reason. If the answer is wrong or the format is invalid, the operation fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Parent Hub Query (e.g., asking for the parent hub of station 5):
<query_parent>5</query_parent>

- Subordinate Count Query (e.g., asking how many subordinates station 3 has):
<query_child_count>3</query_child_count>

- Kth Subordinate Query (e.g., asking for the 1st subordinate of station 2):
<query_kth_child>2,1</query_kth_child>

- Jurisdiction Query (e.g., asking if station 1 has jurisdiction over station 5):
<query_is_ancestor>1,5</query_is_ancestor>

When submitting the final answer, specify which station is inspected first (A or B) and provide a brief logical deduction, using this format:
<answer>first=A, reason=A has jurisdiction over B so A is inspected before B</answer>
"""

    # ================= 场景 2：医疗 =================
    contextualized_rule_zh_2 = """\
欢迎使用医疗资源排查系统。

目前有一家包含 {n} 个科室和病区的医院，编号 1 到 {n} 构成一棵层级结构树，院级管理中枢的父节点为 0。医院专家查房遵循固定的协议标准：到达当前科室后，会按内部科室编号从小到大依次递归查房其所有直属下级病区。

我已锁定两个需要重点督导的科室 A={a} 和 B={b}。你的任务是推断在标准的查房顺序中，专家组会先督导 A 还是 B，并简述理由。

医院的完整科室编制架构对你保密，但它是固定不变的。你可以通过信息系统发起以下四类架构查询（每次仅限一次），我会基于真实的院内编制如实反馈：

1. 上级科室查询：询问科室 x 的直接上级科室编号。返回整数 p（0 表示 x 是最高管理层）。
2. 下辖病区数查询：询问科室 x 有多少个直属下级科室/病区。返回非负整数 c。
3. 定位下属科室：询问科室 x 的第 k 个下属科室（按编号升序排列）。若 k 合法则返回该科室编号，否则返回 0。
4. 隶属关系判定：询问科室 u 是否为科室 v 的上级统筹科室（每个科室视为隶属于自己）。返回"是"或"否"。

你不能直接询问专家组查房时的相对先后顺序。
当你收集足够的信息后，请提交最终判定和理由。若答案错误或格式不符，排查任务失败。

## 系统查询与提交格式（必须严格遵守系统协议）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 上级科室查询（如查询科室 5 的上级）：
<query_parent>5</query_parent>

- 下辖病区数查询（如查询科室 3 的下属数量）：
<query_child_count>3</query_child_count>

- 定位下属科室（如查询科室 2 的第 1 个下属）：
<query_kth_child>2,1</query_kth_child>

- 隶属关系判定（如查询科室 1 是否统筹科室 5）：
<query_is_ancestor>1,5</query_is_ancestor>

提交最终结果时，必须明确先查房的科室（A 或 B）并附带简明推导逻辑，格式如下：
<answer>first=A, reason=A是B的上级科室，因此查房组必然先到达A</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the Medical Resource Tracing System.

The hospital has an organizational tree comprising {n} departments and wards, numbered from 1 to {n}, where the hospital management board's parent is 0. Expert ward rounds follow a strict clinical protocol: the team assesses the current department first, then recursively visits each subordinate ward in ascending order of their department numbers.

I have highlighted two specific departments requiring priority supervision, A={a} and B={b}. Your task is to determine which one the expert team will visit first during the standard rounds, and provide a brief reason.

The complete hospital departmental structure is hidden from you but remains fixed. You can repeatedly submit four types of structural queries to the system (one per turn), and I will answer truthfully based on the actual medical hierarchy:

1. Parent Department Query: Ask for the direct parent department number of department x. Returns integer p (0 means x is the top board).
2. Subordinate Ward Count Query: Ask how many direct subordinate wards/departments department x has. Returns non-negative integer c.
3. Kth Subordinate Query: Ask for the k-th direct subordinate of department x (sorted by number in ascending order). Returns the department's number if k is valid, otherwise 0.
4. Affiliation Query: Ask whether department u is an overarching higher-level department of department v (each department is affiliated with itself). Returns "Yes" or "No".

You cannot directly ask about the relative order of departments in the ward rounds.
When you have gathered enough structural intelligence, submit your final judgment and reason. If the answer is wrong or the format is invalid, the tracing operation fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Parent Department Query (e.g., asking for the parent of department 5):
<query_parent>5</query_parent>

- Subordinate Ward Count Query (e.g., asking how many subordinate wards department 3 has):
<query_child_count>3</query_child_count>

- Kth Subordinate Query (e.g., asking for the 1st subordinate of department 2):
<query_kth_child>2,1</query_kth_child>

- Affiliation Query (e.g., asking if department 1 is overarching department 5):
<query_is_ancestor>1,5</query_is_ancestor>

When submitting the final answer, specify which department is visited first (A or B) and provide a brief logical deduction, using this format:
<answer>first=A, reason=A is an overarching department of B so A is visited before B</answer>
"""

    # ================= 场景 3：教育 =================
    contextualized_rule_zh_3 = """\
欢迎使用自适应学习辅导系统。

本教学大纲包含 {n} 个相互依赖的知识点，编号 1 到 {n} 构成一棵知识树，学科核心根基的父节点为 0。教学引擎的授课顺序严格遵循认知规律：讲解当前主知识点后，按照细分节点编号从小到大的顺序，依次递归讲解其所有的细分衍生知识点。

我已选定两个存在理解难点的知识点 A={a} 和 B={b}。你的任务是推断在标准的大纲授课顺序中，系统会先讲解 A 还是 B，并简述理由。

大纲的完整知识图谱对你是隐藏的，但其层级结构固定不变。你可以通过教学接口向我发起以下四类探究查询（每次仅限一次），我会基于真实的大纲结构如实反馈：

1. 前置主节点查询：询问知识点 x 的直接前置主知识点编号。返回整数 p（0 表示 x 是学科核心）。
2. 细分节点数查询：询问知识点 x 有多少个直属细分衍生知识点。返回非负整数 c。
3. 定位细分节点：询问知识点 x 的第 k 个直属细分知识点（按节点编号升序排列）。若 k 合法则返回该知识点编号，否则返回 0。
4. 知识归属判定：询问知识点 u 是否为知识点 v 的宏观上位概念（每个知识点被视作自身的宏观概念）。返回"是"或"否"。

你不能直接询问两个知识点在授课时间轴上的先后顺序。
当你梳理出足够的前置关系后，请提交最终判定和理由。若答案错误或格式不符，学习规划将中断。

## 系统查询与提交格式（必须严格遵守系统协议）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 前置主节点查询（如查询知识点 5 的主知识点）：
<query_parent>5</query_parent>

- 细分节点数查询（如查询知识点 3 的细分节点数量）：
<query_child_count>3</query_child_count>

- 定位细分节点（如查询知识点 2 的第 1 个细分节点）：
<query_kth_child>2,1</query_kth_child>

- 知识归属判定（如查询知识点 1 是否涵盖知识点 5）：
<query_is_ancestor>1,5</query_is_ancestor>

提交最终结果时，必须明确先授课的知识点（A 或 B）并附带简明推导逻辑，格式如下：
<answer>first=A, reason=A是B的宏观上位概念，因此按照认知规律必然先讲解A</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Adaptive Learning System.

The syllabus consists of a knowledge tree with {n} interdependent concepts, numbered from 1 to {n}, where the subject's core foundation parent is 0. The teaching engine's instructional sequence strictly follows cognitive progression: it teaches the current main concept first, then recursively covers each specialized sub-concept in ascending order of their concept numbers.

I have selected two specific challenging concepts A={a} and B={b}. Your goal is to determine which one the system will teach first in the standard syllabus sequence, and provide a brief reason.

The complete knowledge graph is hidden from you but remains strictly fixed. You can repeatedly submit four types of inquiry queries to the teaching interface (one per turn), and I will answer truthfully based on the actual syllabus structure:

1. Prerequisite Concept Query: Ask for the direct prerequisite main concept number of concept x. Returns integer p (0 means x is the subject core).
2. Sub-concept Count Query: Ask how many direct specialized sub-concepts concept x has. Returns non-negative integer c.
3. Kth Sub-concept Query: Ask for the k-th direct sub-concept of concept x (sorted by concept number in ascending order). Returns the concept's number if k is valid, otherwise 0.
4. Taxonomic Inclusion Query: Ask whether concept u is a macroscopic overarching concept of concept v (each concept conceptually includes itself). Returns "Yes" or "No".

You cannot directly ask about the relative order of concepts on the instructional timeline.
When you have uncovered sufficient structural dependencies, submit your final judgment and reason. If the answer is wrong or the format is invalid, the learning plan fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Prerequisite Concept Query (e.g., asking for the prerequisite of concept 5):
<query_parent>5</query_parent>

- Sub-concept Count Query (e.g., asking how many sub-concepts concept 3 has):
<query_child_count>3</query_child_count>

- Kth Sub-concept Query (e.g., asking for the 1st sub-concept of concept 2):
<query_kth_child>2,1</query_kth_child>

- Taxonomic Inclusion Query (e.g., asking if concept 1 conceptually includes concept 5):
<query_is_ancestor>1,5</query_is_ancestor>

When submitting the final answer, specify which concept is taught first (A or B) and provide a brief logical deduction, using this format:
<answer>first=A, reason=A is the macroscopic overarching concept of B so A is taught before B</answer>
"""

    # ================= 场景 4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
欢迎访问智能制造装配排程系统。

某项工业产品由一棵包含 {n} 个组件的物料清单（BOM）树构成，编号 1 到 {n}，最终成品总成的父节点为 0。质量检测机器人在执行产品合规扫描时，遵循标准的自顶向下工序：扫描当前总成组件后，按子组件物料编号从小到大的顺序，依次递归扫描所有的底层子组件。

我已提取两个存在装配公差风险的组件 A={a} 和 B={b}。你的任务是推断在标准质检工序中，机器人会先扫描 A 还是 B，并简述理由。

完整的 BOM 展开层级对你不可见，但它是固定标准的。你可以通过控制终端向我发起以下四类工程查询（每次仅限一次），我会基于真实的 BOM 结构如实反馈：

1. 所属父组件查询：询问组件 x 的直接所属父组件编号。返回整数 p（0 表示 x 是最终成品）。
2. 直属子组件数查询：询问组件 x 包含多少个直属下一级子组件。返回非负整数 c。
3. 定位子组件：询问组件 x 的第 k 个直属子组件（按物料编号升序排列）。若 k 合法则返回该组件编号，否则返回 0。
4. 包含关系判定：询问组件 u 是否在装配结构上包含组件 v（每个组件被视作包含自身）。返回"是"或"否"。

你不能直接询问质检机器人扫描时的先后工序。
当你解析出足够的装配关系后，请提交最终判定和理由。若答案错误或格式不符，排程模拟将中断。

## 系统查询与提交格式（必须严格遵守系统协议）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 所属父组件查询（如查询组件 5 的父组件）：
<query_parent>5</query_parent>

- 直属子组件数查询（如查询组件 3 的子组件数量）：
<query_child_count>3</query_child_count>

- 定位子组件（如查询组件 2 的第 1 个子组件）：
<query_kth_child>2,1</query_kth_child>

- 包含关系判定（如查询组件 1 是否包含组件 5）：
<query_is_ancestor>1,5</query_is_ancestor>

提交最终结果时，必须明确先扫描的组件（A 或 B）并附带简明推导逻辑，格式如下：
<answer>first=A, reason=A在装配结构上包含B，因此质检探头必然先扫描A</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing / Industry Scenario]
Welcome to the Smart Manufacturing Assembly Scheduling System.

An industrial product consists of a Bill of Materials (BOM) tree containing {n} components, numbered from 1 to {n}, where the final product assembly's parent is 0. The Quality Inspection Robot executes product compliance scans following a standard top-down procedure: it scans the current assembly first, then recursively scans all underlying sub-components in ascending order of their part numbers.

I have extracted two components with potential assembly tolerance risks, A={a} and B={b}. Your task is to determine which one the robot will scan first during the standard inspection process, and provide a brief reason.

The complete BOM hierarchical expansion is hidden from you but strictly fixed. You can repeatedly submit four types of engineering queries to the control terminal (one per turn), and I will answer truthfully based on the actual BOM structure:

1. Parent Component Query: Ask for the direct parent component number of component x. Returns integer p (0 means x is the final product).
2. Sub-component Count Query: Ask how many direct next-level sub-components component x contains. Returns non-negative integer c.
3. Kth Sub-component Query: Ask for the k-th direct sub-component of component x (sorted by part number in ascending order). Returns the component's number if k is valid, otherwise 0.
4. Structural Inclusion Query: Ask whether component u structurally encompasses component v in the assembly (each component encompasses itself). Returns "Yes" or "No".

You cannot directly ask about the relative order of components in the scanning sequence.
When you have resolved enough assembly relations, submit your final judgment and reason. If the answer is wrong or the format is invalid, the scheduling simulation will abort.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Parent Component Query (e.g., asking for the parent of component 5):
<query_parent>5</query_parent>

- Sub-component Count Query (e.g., asking how many sub-components component 3 has):
<query_child_count>3</query_child_count>

- Kth Sub-component Query (e.g., asking for the 1st sub-component of component 2):
<query_kth_child>2,1</query_kth_child>

- Structural Inclusion Query (e.g., asking if component 1 encompasses component 5):
<query_is_ancestor>1,5</query_is_ancestor>

When submitting the final answer, specify which component is scanned first (A or B) and provide a brief logical deduction, using this format:
<answer>first=A, reason=A structurally encompasses B so the inspection probe scans A before B</answer>
"""

    # ================= 场景 5：法律 =================
    contextualized_rule_zh_5 = """\
欢迎使用合规法务审查系统。

本审查涉及一个由 {n} 项法律条款组成的层级结构树，编号为 1 到 {n}，法典根基总则的父节点为 0。法务AI在进行合规审核时遵循严格的法理阅读顺序：解析当前条款后，按法条编号从小到大的顺序依次递归审查其所有的下位附属条款。

我已选定两项存在冲突疑点的条款 A={a} 和 B={b}。你的任务是推断在法务AI的审查顺序中，A 和 B 谁会先被处理，并给出简明法理依据。

法条的完整层级网络对你是未知的，但它是固定不变的。你可以反复向我提出以下四类审查探针（每次仅限一次），我会根据真实的法律结构如实回答：

1. 上位条款查询：询问条款 x 的直接上位条款编号。返回整数 p（0 表示 x 是最高总则）。
2. 下位条款数查询：询问条款 x 拥有多少个直属下位条款。返回非负整数 c。
3. 定位下位条款：询问条款 x 的第 k 个直属下位条款（按法条编号升序排列）。若 k 合法则返回该条款编号，否则返回 0。
4. 法理效力包含判定：询问条款 u 是否在法理效力上涵盖条款 v（每个条款在效力上涵盖自身）。返回"是"或"否"。

你不能直接询问法务AI审查这两个法条的绝对先后顺序。
当你梳理出足够的法理脉络后，请提交最终判定和理由。若答案错误或格式不符，合规审查任务失败。

## 系统查询与提交格式（必须严格遵守系统协议）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 上位条款查询（如查询条款 5 的直接上位条款）：
<query_parent>5</query_parent>

- 下位条款数查询（如查询条款 3 的下位条款数量）：
<query_child_count>3</query_child_count>

- 定位下位条款（如查询条款 2 的第 1 个下位条款）：
<query_kth_child>2,1</query_kth_child>

- 法理效力包含判定（如查询条款 1 的效力是否涵盖条款 5）：
<query_is_ancestor>1,5</query_is_ancestor>

提交最终结果时，必须明确先审查的条款（A 或 B）并附带简明推导逻辑，格式如下：
<answer>first=A, reason=A在法理效力上涵盖B，因此AI必然先审查上位条款A</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the Legal Compliance Review System.

This audit involves a hierarchical tree of {n} legal provisions, numbered from 1 to {n}, where the root general code's parent is 0. The Legal AI follows a strict jurisprudential reading sequence during compliance checks: it analyzes the current provision first, then recursively reviews all of its subordinate provisions in ascending order of their provision numbers.

I have selected two specific provisions with potential conflicts, A={a} and B={b}. Your task is to deduce which one the Legal AI will process first in its review sequence, and provide a brief legal rationale.

The complete legal hierarchy is unknown to you but remains fixed. You can repeatedly deploy four types of review probes to me (one per turn), and I will answer truthfully based on the actual legal structure:

1. Superior Provision Query: Ask for the direct superior provision number of provision x. Returns integer p (0 means x is the overarching general code).
2. Subordinate Provision Count Query: Ask how many direct subordinate provisions provision x has. Returns non-negative integer c.
3. Kth Subordinate Provision Query: Ask for the k-th direct subordinate of provision x (sorted by provision number in ascending order). Returns the provision's number if k is valid, otherwise 0.
4. Jurisdictional Inclusion Query: Ask whether provision u encompasses provision v in legal jurisdiction/authority (each provision encompasses itself). Returns "Yes" or "No".

You cannot directly ask about the absolute order in which the AI reviews these two provisions.
When you have mapped out sufficient legal frameworks, submit your final judgment and rationale. If the answer is wrong or the format is invalid, the compliance audit fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Superior Provision Query (e.g., asking for the superior provision of provision 5):
<query_parent>5</query_parent>

- Subordinate Provision Count Query (e.g., asking how many subordinate provisions provision 3 has):
<query_child_count>3</query_child_count>

- Kth Subordinate Provision Query (e.g., asking for the 1st subordinate of provision 2):
<query_kth_child>2,1</query_kth_child>

- Jurisdictional Inclusion Query (e.g., asking if provision 1 legally encompasses provision 5):
<query_is_ancestor>1,5</query_is_ancestor>

When submitting the final answer, specify which provision is reviewed first (A or B) and provide a brief logical deduction, using this format:
<answer>first=A, reason=A legally encompasses B so the AI must review the superior provision A first</answer>
"""

    tags = ["answer", "query_parent", "query_child_count", "query_kth_child", "query_is_ancestor"]

    # 难度配置：
    # 1 (简单)       - N=5, 简单的树结构，A是B的直接祖先
    # 2 (中等偏下)   - N=7, A和B有共同祖先，需简单推理
    # 3 (中等偏上)   - N=10, 需要找到LCA并比较分支
    # 4 (较难)       - N=12, 更深的树，需要多次查询定位
    # 5 (难)         - N=15, 复杂树结构，需要完整的LCA分析

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "tree": {1: 0, 2: 1, 3: 2, 4: 1, 5: 1},
                "a": 2,
                "b": 3,
                "answer": "A"
            },
            2: {
                "n": 7,
                "tree": {1: 0, 2: 1, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3},
                "a": 5,
                "b": 7,
                "answer": "A"
            },
            3: {
                "n": 10,
                "tree": {1: 0, 2: 1, 3: 2, 4: 2, 5: 1, 6: 5, 7: 6, 8: 5, 9: 8, 10: 8},
                "a": 4,
                "b": 9,
                "answer": "A"
            },
            4: {
                "n": 12,
                "tree": {1: 0, 2: 1, 3: 2, 4: 2, 5: 3, 6: 1, 7: 6, 8: 7, 9: 6, 10: 9, 11: 9, 12: 10},
                "a": 8,
                "b": 12,
                "answer": "A"
            },
            5: {
                "n": 15,
                "tree": {1: 0, 2: 1, 3: 2, 4: 3, 5: 2, 6: 5, 7: 5, 8: 1, 9: 8, 10: 9, 11: 9, 12: 8, 13: 12, 14: 12, 15: 13},
                "a": 7,
                "b": 11,
                "answer": "A"
            },
        },
        "en": {
            1: {
                "n": 5,
                "tree": {1: 0, 2: 1, 3: 2, 4: 1, 5: 1},
                "a": 2,
                "b": 3,
                "answer": "A"
            },
            2: {
                "n": 7,
                "tree": {1: 0, 2: 1, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3},
                "a": 5,
                "b": 7,
                "answer": "A"
            },
            3: {
                "n": 10,
                "tree": {1: 0, 2: 1, 3: 2, 4: 2, 5: 1, 6: 5, 7: 6, 8: 5, 9: 8, 10: 8},
                "a": 4,
                "b": 9,
                "answer": "A"
            },
            4: {
                "n": 12,
                "tree": {1: 0, 2: 1, 3: 2, 4: 2, 5: 3, 6: 1, 7: 6, 8: 7, 9: 6, 10: 9, 11: 9, 12: 10},
                "a": 8,
                "b": 12,
                "answer": "A"
            },
            5: {
                "n": 15,
                "tree": {1: 0, 2: 1, 3: 2, 4: 3, 5: 2, 6: 5, 7: 5, 8: 1, 9: 8, 10: 9, 11: 9, 12: 8, 13: 12, 14: 12, 15: 13},
                "a": 7,
                "b": 11,
                "answer": "A"
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏，根据难度随机生成树结构"""
        lang = self.config.language
        diff = self.config.difficulty if isinstance(self.config.difficulty, int) else int(self.config.difficulty)

        # 难度对应的节点数
        n_map = {1: 5, 2: 7, 3: 10, 4: 12, 5: 15}
        if diff not in n_map:
            raise KeyError(f"Unsupported difficulty: {diff}")

        n = n_map[diff]
        rng = random.Random()  # 如果需要可复现性，可传入固定种子

        # 随机生成树：对于节点 2..n，随机选择一个编号小于它的节点作为父节点
        parent_map = {1: 0}
        for node in range(2, n + 1):
            parent_map[node] = rng.randint(1, node - 1)

        # 随机选择两个不同的节点作为 A 和 B
        a, b = rng.sample(range(1, n + 1), 2)

        # 构建 children_map
        children_map = {}
        for node, parent in parent_map.items():
            if parent not in children_map:
                children_map[parent] = []
            children_map[parent].append(node)
        for parent in children_map:
            children_map[parent].sort()

        # 计算先序遍历以确定正确答案
        def preorder(node):
            result = [node]
            for child in children_map.get(node, []):
                result.extend(preorder(child))
            return result

        order = preorder(1)
        pos_a = order.index(a)
        pos_b = order.index(b)
        correct_answer = "A" if pos_a < pos_b else "B"

        self._game_info["n"] = n
        self._game_info["a"] = a
        self._game_info["b"] = b
        self.parent_map = parent_map
        self.children_map = children_map
        self.correct_answer = correct_answer

    def _is_ancestor(self, u, v):
        """判断u是否为v的祖先（包括u==v的情况）"""
        current = v
        while current != 0:
            if current == u:
                return True
            current = self.parent_map.get(current, 0)
        return False

    def evaluate(self, parsed_info):
        """评估玩家提交的答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案: first=A/B, reason=...
        kv_pairs = [x.strip() for x in raw_ans.split(",", 1)]
        ans_dict = {}
        for kv in kv_pairs:
            if "=" in kv:
                k, v = kv.split("=", 1)
                ans_dict[k.strip()] = v.strip()
        
        if "first" not in ans_dict:
            return False
        
        # 检查答案是否正确（不要求理由正确，只要求first字段正确）
        return ans_dict["first"].upper() == self.correct_answer

    def _cf_core_produce(self, parsed_info):
        """原始的响应生成逻辑"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_invalid = "错误：查询格式无效或节点编号错误。"
            error_out_of_range = "错误：节点编号超出范围。"
        else:
            yes_res, no_res = "Yes", "No"
            error_invalid = "Error: Invalid query format or node number."
            error_out_of_range = "Error: Node number out of range."

        # 优先级：parent > child_count > kth_child > is_ancestor
        if "query_parent" in parsed_info:
            try:
                node = int(parsed_info["query_parent"].strip())
                if node < 1 or node > self._game_info["n"]:
                    return error_out_of_range
                return str(self.parent_map.get(node, 0))
            except:
                return error_invalid

        elif "query_child_count" in parsed_info:
            try:
                node = int(parsed_info["query_child_count"].strip())
                if node < 1 or node > self._game_info["n"]:
                    return error_out_of_range
                return str(len(self.children_map.get(node, [])))
            except:
                return error_invalid

        elif "query_kth_child" in parsed_info:
            try:
                raw = parsed_info["query_kth_child"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_invalid
                node = int(parts[0])
                k = int(parts[1])
                if node < 1 or node > self._game_info["n"]:
                    return error_out_of_range
                children = self.children_map.get(node, [])
                if k < 1 or k > len(children):
                    return "0"
                return str(children[k - 1])
            except:
                return error_invalid

        elif "query_is_ancestor" in parsed_info:
            try:
                raw = parsed_info["query_is_ancestor"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_invalid
                u = int(parts[0])
                v = int(parts[1])
                if u < 1 or u > self._game_info["n"] or v < 1 or v > self._game_info["n"]:
                    return error_out_of_range
                return yes_res if self._is_ancestor(u, v) else no_res
            except:
                return error_invalid

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        """生成错误的答案"""
        # 若 correct 是纯整数字符串（如 "0", "1", "2"）
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 否则按以下规则替换关键词（区分语言）
        if correct == "是":
            return "否"
        elif correct == "否":
            return "是"
        elif correct.lower() == "yes":
            # 保持原始大小写风格，这里简单处理，假设 correct 是 "Yes"
            if correct == "Yes": return "No"
            if correct == "YES": return "NO"
            return "no"
        elif correct.lower() == "no":
            if correct == "No": return "Yes"
            if correct == "NO": return "YES"
            return "yes"
        
        # 若都不匹配：在字符串末尾追加 "_WRONG"
        return correct + "_WRONG"

    def get_all_possible_queries(self):
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        queries = []
        n = self._game_info["n"]
        lang = self.config.language
        
        # 预计算布尔值对应的文本
        if lang == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        # 1. 上级查询: 1~N
        for x in range(1, n + 1):
            query = f"<query_parent>{x}</query_parent>"
            answer = str(self.parent_map.get(x, 0))
            queries.append({"query": query, "answer": answer})

        # 2. 子数查询: 1~N
        for x in range(1, n + 1):
            query = f"<query_child_count>{x}</query_child_count>"
            answer = str(len(self.children_map.get(x, [])))
            queries.append({"query": query, "answer": answer})

        # 3. 定位子节点: 1~N, k=1~len(children)
        # 仅生成有效的k，以提供正向的结构信息
        for x in range(1, n + 1):
            children = self.children_map.get(x, [])
            for k in range(1, len(children) + 1):
                query = f"<query_kth_child>{x},{k}</query_kth_child>"
                answer = str(children[k - 1])
                queries.append({"query": query, "answer": answer})

        # 4. 祖先判定: 所有节点对 (u, v)
        for u in range(1, n + 1):
            for v in range(1, n + 1):
                query = f"<query_is_ancestor>{u},{v}</query_is_ancestor>"
                is_anc = self._is_ancestor(u, v)
                answer = yes_res if is_anc else no_res
                queries.append({"query": query, "answer": answer})

        return queries