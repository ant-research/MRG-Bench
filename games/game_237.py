from .base import Game
import re

class TreeTraversalInferenceGame(Game):

    game_rule_zh = """\
我们来玩一个"树遍历推理"游戏。规则如下：

游戏设定了一棵有根树，包含 {n} 个节点，编号为 1 到 {n}，根节点为 {root}。树的结构（每个节点的孩子集合）已完全告知如下：

{tree_structure}

隐藏参数：存在一个未知起点 K（1 到 {n} 之间的某个整数），在整个游戏过程中固定不变。

全局环序：定义一个全局循环序列 C(K) = [K, K+1, ..., {n}, 1, 2, ..., K-1]（按整数模 {n} 递增循环）。对于任意父节点 p，其孩子集合会按照 C(K) 在该集合上的相对次序进行排序。

访问过程：采用先序深度优先遍历：
  - 到达节点 x 时先访问 x 本身
  - 然后按上述排序后的顺序，依次递归访问其每个孩子
这样会在所有节点上诱导出一个总的访问先后次序。

你的目标：通过提问推断出隐藏起点 K（或等价地，重建由 C(K) 诱导的各父节点孩子排序），从而能对任意节点对的访问先后做出正确判断。

你可以进行以下三种操作（每次只能选择一种）：

1. Compare(a, b)：询问在完整访问序列中，节点 a 和节点 b 谁先被访问。我会回答 a 或 b。

2. SiblingCompare(p, c1, c2)：前提是 c1 和 c2 都是节点 p 的孩子。询问在访问 p 后、对其孩子排序中，c1 和 c2 谁更靠前。我会回答 c1 或 c2。

3. Challenge(m)：请求给出 m 对未曾比较过的节点对，你需要一次性提交对每对节点的先后预测。如果所有预测都正确，游戏成功；否则会告知错误情况，你可以继续提问后再次发起 Challenge（每次 m 至少为 8）。

每次只能包含一个操作标签。请使用以下 XML 格式：

- Compare 查询（例如询问节点 1 和节点 3）：
<query_compare>1,3</query_compare>

- SiblingCompare 查询（例如询问父节点 2 的孩子 4 和 5）：
<query_sibling>2,4,5</query_sibling>

- Challenge 提交（例如预测 3 对节点）：
<answer>1,2:1;3,4:4;5,6:5</answer>

其中 answer 格式为：每对用分号分隔，每对内部格式为 "节点a,节点b:预测结果"。预测结果必须是 a 或 b 之一。
"""

    game_rule_en = """\
Let's play a "Tree Traversal Inference" game. Here are the rules:

The game has a rooted tree with {n} nodes, numbered from 1 to {n}, with root node {root}. The tree structure (each node's children set) is fully known as follows:

{tree_structure}

Hidden parameter: There exists an unknown starting point K (an integer between 1 and {n}), which remains fixed throughout the game.

Global cyclic order: Define a global cyclic sequence C(K) = [K, K+1, ..., {n}, 1, 2, ..., K-1] (incrementing modulo {n}). For any parent node p, its children set will be sorted according to the relative order of C(K) on that set.

Traversal process: Pre-order depth-first traversal is used:
  - When reaching node x, visit x itself first
  - Then recursively visit each child in the sorted order described above
This induces a total order on all nodes (visitation order).

Your goal: Through queries, infer the hidden starting point K (or equivalently, reconstruct the children ordering induced by C(K) for each parent node), so you can correctly judge the visitation order for any pair of nodes.

You can perform the following three types of operations (one per turn):

1. Compare(a, b): Ask which of node a and node b is visited first in the complete visitation sequence. I will answer a or b.

2. SiblingCompare(p, c1, c2): Prerequisite: both c1 and c2 are children of node p. Ask which of c1 and c2 comes first in the sorted children order after visiting p. I will answer c1 or c2.

3. Challenge(m): Request m previously uncompared node pairs, and submit your predictions for each pair's order at once. If all predictions are correct, you win; otherwise, error information will be provided, and you can continue querying before issuing another Challenge (each Challenge must have m at least 8).

Each turn must contain only one operation tag. Use the following XML format:

- Compare query (e.g., asking about node 1 and node 3):
<query_compare>1,3</query_compare>

- SiblingCompare query (e.g., asking about children 4 and 5 of parent node 2):
<query_sibling>2,4,5</query_sibling>

- Challenge submission (e.g., predicting 3 pairs):
<answer>1,2:1;3,4:4;5,6:5</answer>

The answer format is: pairs separated by semicolons, each pair formatted as "nodeA,nodeB:prediction". The prediction must be either A or B.
"""

    contextualized_rule_zh_1 = """\
【交通网络调度巡检系统】
我们来运行"调度巡查推理"程序。规则如下：

系统设定了一棵有根调度树，包含 {n} 个交通枢纽（在系统中表示为“节点”），编号为 1 到 {n}，总调度中心为 {root}。网络层级（每个枢纽的下级站点集合，表示为该节点的“孩子”）已完全告知如下：

{tree_structure}

隐藏参数：存在一个未知的首要优先级站点 K（1 到 {n} 之间的某个整数），在整个调度周期内固定不变。

全局环序：定义一个全局循环优先级序列 C(K) = [K, K+1, ..., {n}, 1, 2, ..., K-1]（按整数模 {n} 递增循环）。对于任意上级枢纽 p，其下级站点集合会按照 C(K) 在该集合上的相对次序进行排序。

巡查过程：采用先序深度优先巡查路线：
  - 到达枢纽 x 时先巡查 x 本身
  - 然后按上述排序后的优先级顺序，依次递归巡查其每个下级站点
这样会在所有枢纽上诱导出一个总的巡查先后次序。

你的目标：通过查询推断出隐藏的首要站点 K（或等价地，重建由 C(K) 诱导的各级站点优先级排序），从而能对任意站点对的巡查先后做出正确判断。

你可以进行以下三种操作（每次只能选择一种）：

1. Compare(a, b)：查询在完整巡查序列中，枢纽 a 和枢纽 b 谁先被巡查。我会返回 a 或 b。

2. SiblingCompare(p, c1, c2)：前提是 c1 和 c2 都是枢纽 p 的直属下级。查询在巡查 p 后、对下级优先排序中，c1 和 c2 谁更靠前。我会返回 c1 或 c2。

3. Challenge(m)：请求给出 m 对未曾比较过的枢纽对，你需要一次性提交对每对枢纽巡查先后的预测。如果所有预测都正确，系统校验成功；否则会告知错误情况，你可以继续查询后再次发起 Challenge（每次 m 至少为 8）。

每次只能包含一个操作标签。请使用以下 XML 格式：

- Compare 查询（例如查询枢纽 1 和枢纽 3）：
<query_compare>1,3</query_compare>

- SiblingCompare 查询（例如查询上级枢纽 2 的下级 4 和 5）：
<query_sibling>2,4,5</query_sibling>

- Challenge 提交（例如预测 3 对枢纽）：
<answer>1,2:1;3,4:4;5,6:5</answer>

其中 answer 格式为：每对用分号分隔，每对内部格式为 "枢纽a,枢纽b:预测结果"。预测结果必须是 a 或 b 之一。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's run the "Scheduling Patrol Inference" program. Here are the rules:

The system defines a rooted scheduling tree with {n} transport hubs (represented as "nodes" in the system), numbered from 1 to {n}, with the main control center at {root}. The network hierarchy (each hub's subordinate stations, represented as "children") is fully known as follows:

{tree_structure}

Hidden parameter: There exists an unknown primary priority station K (an integer between 1 and {n}), which remains fixed throughout the scheduling cycle.

Global cyclic order: Define a global cyclic priority sequence C(K) = [K, K+1, ..., {n}, 1, 2, ..., K-1] (incrementing modulo {n}). For any superior hub p, its subordinate stations will be sorted according to the relative order of C(K).

Patrol process: Pre-order depth-first patrol route is used:
  - When reaching hub x, patrol x itself first
  - Then recursively patrol each subordinate station in the sorted priority order described above
This induces a total patrol order on all hubs.

Your goal: Through queries, infer the hidden primary station K (or equivalently, reconstruct the subordinate ordering induced by C(K) for each hub), so you can correctly judge the patrol order for any pair of stations.

You can perform the following three types of operations (one per turn):

1. Compare(a, b): Ask which of hub a and hub b is patrolled first in the complete patrol sequence. I will return a or b.

2. SiblingCompare(p, c1, c2): Prerequisite: both c1 and c2 are direct subordinates of hub p. Ask which of c1 and c2 comes first in the priority order after patrolling p. I will return c1 or c2.

3. Challenge(m): Request m previously uncompared hub pairs, and submit your predictions for each pair's patrol order at once. If all predictions are correct, system validation succeeds; otherwise, error information will be provided, and you can continue querying before issuing another Challenge (each Challenge must have m at least 8).

Each turn must contain only one operation tag. Use the following XML format:

- Compare query (e.g., querying hub 1 and hub 3):
<query_compare>1,3</query_compare>

- SiblingCompare query (e.g., querying subordinates 4 and 5 of hub 2):
<query_sibling>2,4,5</query_sibling>

- Challenge submission (e.g., predicting 3 pairs):
<answer>1,2:1;3,4:4;5,6:5</answer>

The answer format is: pairs separated by semicolons, each pair formatted as "hubA,hubB:prediction". The prediction must be either A or B.
"""

    contextualized_rule_zh_2 = """\
【医疗查房与物资调度系统】
我们来运行"查房调度推理"程序。规则如下：

系统设定了一棵有根医疗管理树，包含 {n} 个科室或病房（在系统中表示为“节点”），编号为 1 到 {n}，医疗主控台为 {root}。医院分布层级（每个科室的下级单位集合，表示为该节点的“孩子”）已完全告知如下：

{tree_structure}

隐藏参数：存在一个未知的首要重点科室 K（1 到 {n} 之间的某个整数），在整个查房周期内固定不变。

全局环序：定义一个全局循环响应序列 C(K) = [K, K+1, ..., {n}, 1, 2, ..., K-1]（按整数模 {n} 递增循环）。对于任意上级科室 p，其下级单位集合会按照 C(K) 在该集合上的相对次序进行排序。

查房过程：采用先序深度优先查房路径：
  - 到达科室 x 时先检查 x 本身
  - 然后按上述排序后的响应顺序，依次递归检查其每个下级单位
这样会在所有科室上诱导出一个总的查房先后次序。

你的目标：通过查询推断出隐藏的首要重点科室 K（或等价地，重建由 C(K) 诱导的各级单位响应排序），从而能对任意科室对的查房先后做出正确判断。

你可以进行以下三种操作（每次只能选择一种）：

1. Compare(a, b)：查询在完整查房序列中，科室 a 和科室 b 谁先被检查。我会返回 a 或 b。

2. SiblingCompare(p, c1, c2)：前提是 c1 和 c2 都是科室 p 的直属下级。查询在检查 p 后、对下级响应排序中，c1 和 c2 谁更靠前。我会返回 c1 或 c2。

3. Challenge(m)：请求给出 m 对未曾比较过的科室对，你需要一次性提交对每对科室查房先后的预测。如果所有预测都正确，系统校验成功；否则会告知错误情况，你可以继续查询后再次发起 Challenge（每次 m 至少为 8）。

每次只能包含一个操作标签。请使用以下 XML 格式：

- Compare 查询（例如查询科室 1 和科室 3）：
<query_compare>1,3</query_compare>

- SiblingCompare 查询（例如查询上级科室 2 的下级 4 和 5）：
<query_sibling>2,4,5</query_sibling>

- Challenge 提交（例如预测 3 对科室）：
<answer>1,2:1;3,4:4;5,6:5</answer>

其中 answer 格式为：每对用分号分隔，每对内部格式为 "科室a,科室b:预测结果"。预测结果必须是 a 或 b 之一。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's run the "Ward Round Scheduling Inference" program. Here are the rules:

The system defines a rooted medical management tree with {n} departments or wards (represented as "nodes" in the system), numbered from 1 to {n}, with the main medical console at {root}. The hospital hierarchy (each department's subordinate units, represented as "children") is fully known as follows:

{tree_structure}

Hidden parameter: There exists an unknown primary focus department K (an integer between 1 and {n}), which remains fixed throughout the ward round cycle.

Global cyclic order: Define a global cyclic response sequence C(K) = [K, K+1, ..., {n}, 1, 2, ..., K-1] (incrementing modulo {n}). For any superior department p, its subordinate units will be sorted according to the relative order of C(K).

Ward round process: Pre-order depth-first round route is used:
  - When reaching department x, inspect x itself first
  - Then recursively inspect each subordinate unit in the sorted response order described above
This induces a total ward round order on all departments.

Your goal: Through queries, infer the hidden primary department K (or equivalently, reconstruct the subordinate ordering induced by C(K) for each department), so you can correctly judge the round order for any pair of departments.

You can perform the following three types of operations (one per turn):

1. Compare(a, b): Ask which of department a and department b is inspected first in the complete round sequence. I will return a or b.

2. SiblingCompare(p, c1, c2): Prerequisite: both c1 and c2 are direct subordinates of department p. Ask which of c1 and c2 comes first in the response order after inspecting p. I will return c1 or c2.

3. Challenge(m): Request m previously uncompared department pairs, and submit your predictions for each pair's round order at once. If all predictions are correct, system validation succeeds; otherwise, error information will be provided, and you can continue querying before issuing another Challenge (each Challenge must have m at least 8).

Each turn must contain only one operation tag. Use the following XML format:

- Compare query (e.g., querying department 1 and 3):
<query_compare>1,3</query_compare>

- SiblingCompare query (e.g., querying subordinates 4 and 5 of department 2):
<query_sibling>2,4,5</query_sibling>

- Challenge submission (e.g., predicting 3 pairs):
<answer>1,2:1;3,4:4;5,6:5</answer>

The answer format is: pairs separated by semicolons, each pair formatted as "departmentA,departmentB:prediction". The prediction must be either A or B.
"""

    contextualized_rule_zh_3 = """\
【教学大纲与知识点推导系统】
我们来运行"知识点教学进度推理"程序。规则如下：

系统设定了一棵有根教学依赖树，包含 {n} 个知识模块（在系统中表示为“节点”），编号为 1 到 {n}，核心前置模块为 {root}。大纲结构（每个模块的衍生子模块集合，表示为该节点的“孩子”）已完全告知如下：

{tree_structure}

隐藏参数：存在一个未知的新学期重点起始模块 K（1 到 {n} 之间的某个整数），在整个教学周期内固定不变。

全局环序：定义一个全局循环教学序列 C(K) = [K, K+1, ..., {n}, 1, 2, ..., K-1]（按整数模 {n} 递增循环）。对于任意父模块 p，其衍生子模块集合会按照 C(K) 在该集合上的相对次序进行授课排序。

教学过程：采用先序深度优先教学进度：
  - 到达模块 x 时先讲授 x 本身
  - 然后按上述排序后的授课顺序，依次递归讲授其每个衍生子模块
这样会在所有模块上诱导出一个总的教学先后次序。

你的目标：通过查询推断出隐藏的重点起始模块 K（或等价地，重建由 C(K) 诱导的各衍生模块教学排序），从而能对任意模块对的教学先后做出正确判断。

你可以进行以下三种操作（每次只能选择一种）：

1. Compare(a, b)：查询在完整教学序列中，模块 a 和模块 b 谁先被讲授。我会返回 a 或 b。

2. SiblingCompare(p, c1, c2)：前提是 c1 和 c2 都是模块 p 的衍生子模块。查询在讲授 p 后、对子模块授课排序中，c1 和 c2 谁更靠前。我会返回 c1 或 c2。

3. Challenge(m)：请求给出 m 对未曾比较过的模块对，你需要一次性提交对每对模块教学先后的预测。如果所有预测都正确，系统评估成功；否则会告知错误情况，你可以继续查询后再次发起 Challenge（每次 m 至少为 8）。

每次只能包含一个操作标签。请使用以下 XML 格式：

- Compare 查询（例如查询模块 1 和模块 3）：
<query_compare>1,3</query_compare>

- SiblingCompare 查询（例如查询父模块 2 的子模块 4 和 5）：
<query_sibling>2,4,5</query_sibling>

- Challenge 提交（例如预测 3 对模块）：
<answer>1,2:1;3,4:4;5,6:5</answer>

其中 answer 格式为：每对用分号分隔，每对内部格式为 "模块a,模块b:预测结果"。预测结果必须是 a 或 b 之一。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's run the "Knowledge Module Teaching Progress Inference" program. Here are the rules:

The system defines a rooted teaching dependency tree with {n} knowledge modules (represented as "nodes" in the system), numbered from 1 to {n}, with the core prerequisite module at {root}. The syllabus structure (each module's derived sub-modules, represented as "children") is fully known as follows:

{tree_structure}

Hidden parameter: There exists an unknown key starting module K (an integer between 1 and {n}), which remains fixed throughout the teaching cycle.

Global cyclic order: Define a global cyclic teaching sequence C(K) = [K, K+1, ..., {n}, 1, 2, ..., K-1] (incrementing modulo {n}). For any parent module p, its derived sub-modules will be sorted according to the relative order of C(K).

Teaching process: Pre-order depth-first teaching progress is used:
  - When reaching module x, teach x itself first
  - Then recursively teach each derived sub-module in the sorted order described above
This induces a total teaching order on all modules.

Your goal: Through queries, infer the hidden key starting module K (or equivalently, reconstruct the derived module ordering induced by C(K) for each parent module), so you can correctly judge the teaching order for any pair of modules.

You can perform the following three types of operations (one per turn):

1. Compare(a, b): Ask which of module a and module b is taught first in the complete teaching sequence. I will return a or b.

2. SiblingCompare(p, c1, c2): Prerequisite: both c1 and c2 are derived sub-modules of module p. Ask which of c1 and c2 comes first in the teaching order after teaching p. I will return c1 or c2.

3. Challenge(m): Request m previously uncompared module pairs, and submit your predictions for each pair's teaching order at once. If all predictions are correct, system assessment succeeds; otherwise, error information will be provided, and you can continue querying before issuing another Challenge (each Challenge must have m at least 8).

Each turn must contain only one operation tag. Use the following XML format:

- Compare query (e.g., querying module 1 and 3):
<query_compare>1,3</query_compare>

- SiblingCompare query (e.g., querying sub-modules 4 and 5 of module 2):
<query_sibling>2,4,5</query_sibling>

- Challenge submission (e.g., predicting 3 pairs):
<answer>1,2:1;3,4:4;5,6:5</answer>

The answer format is: pairs separated by semicolons, each pair formatted as "moduleA,moduleB:prediction". The prediction must be either A or B.
"""

    contextualized_rule_zh_4 = """\
【工业生产线巡检与设备启动系统】
我们来运行"生产设备巡检推理"程序。规则如下：

系统设定了一棵有根生产依赖树，包含 {n} 台工业设备或工序（在系统中表示为“节点”），编号为 1 到 {n}，主控调度室为 {root}。生产线层级（每个设备的下游联动设备集合，表示为该节点的“孩子”）已完全告知如下：

{tree_structure}

隐藏参数：存在一个未知的首发核心设备 K（1 到 {n} 之间的某个整数），在整个生产批次中固定不变。

全局环序：定义一个全局循环启动优先级序列 C(K) = [K, K+1, ..., {n}, 1, 2, ..., K-1]（按整数模 {n} 递增循环）。对于任意上游设备 p，其下游联动设备集合会按照 C(K) 在该集合上的相对次序进行排序。

巡检过程：采用先序深度优先维护巡检路线：
  - 到达设备 x 时先检测 x 本身
  - 然后按上述排序后的优先级顺序，依次递归检测其每个下游联动设备
这样会在所有设备上诱导出一个总的巡检先后次序。

你的目标：通过查询推断出隐藏的首发核心设备 K（或等价地，重建由 C(K) 诱导的各联动设备优先级排序），从而能对任意设备对的巡检先后做出正确判断。

你可以进行以下三种操作（每次只能选择一种）：

1. Compare(a, b)：查询在完整巡检序列中，设备 a 和设备 b 哪台先被检测。我会返回 a 或 b。

2. SiblingCompare(p, c1, c2)：前提是 c1 和 c2 都是设备 p 的直属下游设备。查询在检测 p 后、对下游优先级排序中，c1 和 c2 谁更靠前。我会返回 c1 或 c2。

3. Challenge(m)：请求给出 m 对未曾比较过的设备对，你需要一次性提交对每对设备巡检先后的预测。如果所有预测都正确，系统验证成功；否则会告知故障情况，你可以继续查询后再次发起 Challenge（每次 m 至少为 8）。

每次只能包含一个操作标签。请使用以下 XML 格式：

- Compare 查询（例如查询设备 1 和设备 3）：
<query_compare>1,3</query_compare>

- SiblingCompare 查询（例如查询上游设备 2 的下游设备 4 和 5）：
<query_sibling>2,4,5</query_sibling>

- Challenge 提交（例如预测 3 对设备）：
<answer>1,2:1;3,4:4;5,6:5</answer>

其中 answer 格式为：每对用分号分隔，每对内部格式为 "设备a,设备b:预测结果"。预测结果必须是 a 或 b 之一。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's run the "Production Equipment Patrol Inference" program. Here are the rules:

The system defines a rooted production dependency tree with {n} industrial devices or processes (represented as "nodes" in the system), numbered from 1 to {n}, with the main control room at {root}. The production line hierarchy (each device's downstream linked devices, represented as "children") is fully known as follows:

{tree_structure}

Hidden parameter: There exists an unknown primary core device K (an integer between 1 and {n}), which remains fixed throughout the production batch.

Global cyclic order: Define a global cyclic startup priority sequence C(K) = [K, K+1, ..., {n}, 1, 2, ..., K-1] (incrementing modulo {n}). For any upstream device p, its downstream linked devices will be sorted according to the relative order of C(K).

Patrol process: Pre-order depth-first maintenance patrol route is used:
  - When reaching device x, inspect x itself first
  - Then recursively inspect each downstream linked device in the sorted priority order described above
This induces a total patrol order on all devices.

Your goal: Through queries, infer the hidden primary core device K (or equivalently, reconstruct the downstream ordering induced by C(K) for each device), so you can correctly judge the patrol order for any pair of devices.

You can perform the following three types of operations (one per turn):

1. Compare(a, b): Ask which of device a and device b is inspected first in the complete patrol sequence. I will return a or b.

2. SiblingCompare(p, c1, c2): Prerequisite: both c1 and c2 are direct downstream devices of device p. Ask which of c1 and c2 comes first in the priority order after inspecting p. I will return c1 or c2.

3. Challenge(m): Request m previously uncompared device pairs, and submit your predictions for each pair's patrol order at once. If all predictions are correct, system validation succeeds; otherwise, error information will be provided, and you can continue querying before issuing another Challenge (each Challenge must have m at least 8).

Each turn must contain only one operation tag. Use the following XML format:

- Compare query (e.g., querying device 1 and 3):
<query_compare>1,3</query_compare>

- SiblingCompare query (e.g., querying downstream devices 4 and 5 of device 2):
<query_sibling>2,4,5</query_sibling>

- Challenge submission (e.g., predicting 3 pairs):
<answer>1,2:1;3,4:4;5,6:5</answer>

The answer format is: pairs separated by semicolons, each pair formatted as "deviceA,deviceB:prediction". The prediction must be either A or B.
"""

    contextualized_rule_zh_5 = """\
【司法卷宗管辖与审查系统】
我们来运行"司法审查顺位推理"程序。规则如下：

系统设定了一棵有根司法管辖树，包含 {n} 个案件卷宗（在系统中表示为“节点”），编号为 1 到 {n}，核心指导案件为 {root}。管辖衍生层级（每个案件的衍生关联子案件集合，表示为该节点的“孩子”）已完全告知如下：

{tree_structure}

隐藏参数：存在一个未知的首要焦点案件 K（1 到 {n} 之间的某个整数），在整个司法审查阶段内固定不变。

全局环序：定义一个全局循环审查顺位序列 C(K) = [K, K+1, ..., {n}, 1, 2, ..., K-1]（按整数模 {n} 递增循环）。对于任意主案件 p，其衍生关联子案件集合会按照 C(K) 在该集合上的相对次序进行审查排序。

审查过程：采用先序深度优先审查流程：
  - 调阅到案件 x 时先审查 x 本身
  - 然后按上述排序后的顺位顺序，依次递归审查其每个衍生关联子案件
这样会在所有案件上诱导出一个总的卷宗审查先后次序。

你的目标：通过查询推断出隐藏的首要焦点案件 K（或等价地，重建由 C(K) 诱导的各衍生案件顺位排序），从而能对任意案件对的审查先后做出正确判断。

你可以进行以下三种操作（每次只能选择一种）：

1. Compare(a, b)：查询在完整审查序列中，案件 a 和案件 b 哪个先被审查。我会返回 a 或 b。

2. SiblingCompare(p, c1, c2)：前提是 c1 和 c2 都是主案件 p 的衍生子案件。查询在审查 p 后、对子案件顺位排序中，c1 和 c2 哪个更靠前。我会返回 c1 或 c2。

3. Challenge(m)：请求给出 m 对未曾比较过的案件对，你需要一次性提交对每对案件审查先后的预测。如果所有预测都正确，庭审推理成功；否则会告知驳回情况，你可以继续查询后再次发起 Challenge（每次 m 至少为 8）。

每次只能包含一个操作标签。请使用以下 XML 格式：

- Compare 查询（例如查询案件 1 和案件 3）：
<query_compare>1,3</query_compare>

- SiblingCompare 查询（例如查询主案件 2 的子案件 4 和 5）：
<query_sibling>2,4,5</query_sibling>

- Challenge 提交（例如预测 3 对案件）：
<answer>1,2:1;3,4:4;5,6:5</answer>

其中 answer 格式为：每对用分号分隔，每对内部格式为 "案件a,案件b:预测结果"。预测结果必须是 a 或 b 之一。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's run the "Judicial Review Sequence Inference" program. Here are the rules:

The system defines a rooted judicial jurisdiction tree with {n} case files (represented as "nodes" in the system), numbered from 1 to {n}, with the core guiding case at {root}. The derivative hierarchy (each case's derived associated sub-cases, represented as "children") is fully known as follows:

{tree_structure}

Hidden parameter: There exists an unknown primary focus case K (an integer between 1 and {n}), which remains fixed throughout the judicial review phase.

Global cyclic order: Define a global cyclic review sequence C(K) = [K, K+1, ..., {n}, 1, 2, ..., K-1] (incrementing modulo {n}). For any principal case p, its derived associated sub-cases will be sorted according to the relative order of C(K).

Review process: Pre-order depth-first review procedure is used:
  - When accessing case x, review x itself first
  - Then recursively review each derived associated sub-case in the sorted sequence described above
This induces a total review order on all cases.

Your goal: Through queries, infer the hidden primary focus case K (or equivalently, reconstruct the sub-case ordering induced by C(K) for each principal case), so you can correctly judge the review order for any pair of cases.

You can perform the following three types of operations (one per turn):

1. Compare(a, b): Ask which of case a and case b is reviewed first in the complete review sequence. I will return a or b.

2. SiblingCompare(p, c1, c2): Prerequisite: both c1 and c2 are derived sub-cases of principal case p. Ask which of c1 and c2 comes first in the sequence after reviewing p. I will return c1 or c2.

3. Challenge(m): Request m previously uncompared case pairs, and submit your predictions for each pair's review order at once. If all predictions are correct, court inference succeeds; otherwise, rejection information will be provided, and you can continue querying before issuing another Challenge (each Challenge must have m at least 8).

Each turn must contain only one operation tag. Use the following XML format:

- Compare query (e.g., querying case 1 and 3):
<query_compare>1,3</query_compare>

- SiblingCompare query (e.g., querying sub-cases 4 and 5 of case 2):
<query_sibling>2,4,5</query_sibling>

- Challenge submission (e.g., predicting 3 pairs):
<answer>1,2:1;3,4:4;5,6:5</answer>

The answer format is: pairs separated by semicolons, each pair formatted as "caseA,caseB:prediction". The prediction must be either A or B.
"""

    tags = ["answer", "query_compare", "query_sibling"]
    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 7,
                "root": 1,
                "tree": {
                    1: [2, 3],
                    2: [4, 5],
                    3: [6, 7],
                    4: [], 5: [], 6: [], 7: []
                },
                "k": 3,
            },
            2: {
                "n": 10,
                "root": 1,
                "tree": {
                    1: [2, 3, 4],
                    2: [5, 6],
                    3: [7],
                    4: [8, 9, 10],
                    5: [], 6: [], 7: [], 8: [], 9: [], 10: []
                },
                "k": 5,
            },
            3: {
                "n": 13,
                "root": 1,
                "tree": {
                    1: [2, 3, 4],
                    2: [5, 6, 7],
                    3: [8, 9],
                    4: [10],
                    5: [11],
                    6: [12, 13],
                    7: [], 8: [], 9: [], 10: [], 11: [], 12: [], 13: []
                },
                "k": 7,
            },
            4: {
                "n": 16,
                "root": 1,
                "tree": {
                    1: [2, 3, 4, 5],
                    2: [6, 7],
                    3: [8, 9, 10],
                    4: [11],
                    5: [12, 13],
                    6: [14],
                    7: [15, 16],
                    8: [], 9: [], 10: [], 11: [], 12: [], 13: [], 14: [], 15: [], 16: []
                },
                "k": 9,
            },
            5: {
                "n": 20,
                "root": 1,
                "tree": {
                    1: [2, 3, 4],
                    2: [5, 6, 7, 8],
                    3: [9, 10],
                    4: [11, 12, 13],
                    5: [14],
                    6: [15, 16],
                    7: [],
                    8: [17],
                    9: [18],
                    10: [19, 20],
                    11: [], 12: [], 13: [], 14: [], 15: [], 16: [], 17: [], 18: [], 19: [], 20: []
                },
                "k": 11,
            },
        },
        "en": {
            1: {
                "n": 7,
                "root": 1,
                "tree": {
                    1: [2, 3],
                    2: [4, 5],
                    3: [6, 7],
                    4: [], 5: [], 6: [], 7: []
                },
                "k": 3,
            },
            2: {
                "n": 10,
                "root": 1,
                "tree": {
                    1: [2, 3, 4],
                    2: [5, 6],
                    3: [7],
                    4: [8, 9, 10],
                    5: [], 6: [], 7: [], 8: [], 9: [], 10: []
                },
                "k": 5,
            },
            3: {
                "n": 13,
                "root": 1,
                "tree": {
                    1: [2, 3, 4],
                    2: [5, 6, 7],
                    3: [8, 9],
                    4: [10],
                    5: [11],
                    6: [12, 13],
                    7: [], 8: [], 9: [], 10: [], 11: [], 12: [], 13: []
                },
                "k": 7,
            },
            4: {
                "n": 16,
                "root": 1,
                "tree": {
                    1: [2, 3, 4, 5],
                    2: [6, 7],
                    3: [8, 9, 10],
                    4: [11],
                    5: [12, 13],
                    6: [14],
                    7: [15, 16],
                    8: [], 9: [], 10: [], 11: [], 12: [], 13: [], 14: [], 15: [], 16: []
                },
                "k": 9,
            },
            5: {
                "n": 20,
                "root": 1,
                "tree": {
                    1: [2, 3, 4],
                    2: [5, 6, 7, 8],
                    3: [9, 10],
                    4: [11, 12, 13],
                    5: [14],
                    6: [15, 16],
                    7: [],
                    8: [17],
                    9: [18],
                    10: [19, 20],
                    11: [], 12: [], 13: [], 14: [], 15: [], 16: [], 17: [], 18: [], 19: [], 20: []
                },
                "k": 11,
            },
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
        self.n = cfg["n"]
        self.root = cfg["root"]
        self.tree = cfg["tree"]
        self.k = cfg["k"]
        
        self.cyclic_order = list(range(self.k, self.n + 1)) + list(range(1, self.k))
        
        self.sorted_children = {}
        for parent, children in self.tree.items():
            if children:
                sorted_child = sorted(children, key=lambda x: self.cyclic_order.index(x))
                self.sorted_children[parent] = sorted_child
            else:
                self.sorted_children[parent] = []
        
        self.traversal_order = []
        self._dfs_traversal(self.root)
        
        self.node_position = {node: idx for idx, node in enumerate(self.traversal_order)}
        
        self.compared_pairs = set()
        
        tree_desc = self._build_tree_description()
        
        self._game_info = {
            "n": self.n,
            "root": self.root,
            "tree_structure": tree_desc
        }

    def _dfs_traversal(self, node):
        self.traversal_order.append(node)
        for child in self.sorted_children[node]:
            self._dfs_traversal(child)

    def _build_tree_description(self):
        if self.config.language == "zh":
            lines = []
            for node in sorted(self.tree.keys()):
                if self.tree[node]:
                    children_str = ", ".join(map(str, self.tree[node]))
                    lines.append(f"  节点 {node} 的孩子: [{children_str}]")
                else:
                    lines.append(f"  节点 {node} 的孩子: []")
            return "\n".join(lines)
        else:
            lines = []
            for node in sorted(self.tree.keys()):
                if self.tree[node]:
                    children_str = ", ".join(map(str, self.tree[node]))
                    lines.append(f"  Node {node}'s children: [{children_str}]")
                else:
                    lines.append(f"  Node {node}'s children: []")
            return "\n".join(lines)

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        try:
            pairs = raw_ans.split(";")
            if len(pairs) < 8:
                return False
            
            all_correct = True
            for pair_str in pairs:
                pair_str = pair_str.strip()
                if not pair_str:
                    continue
                    
                parts = pair_str.split(":")
                if len(parts) != 2:
                    return False
                
                nodes_part, prediction = parts[0].strip(), parts[1].strip()
                node_parts = nodes_part.split(",")
                if len(node_parts) != 2:
                    return False
                
                a, b = int(node_parts[0].strip()), int(node_parts[1].strip())
                pred = int(prediction.strip())
                
                if a < 1 or a > self.n or b < 1 or b > self.n:
                    return False
                
                if pred != a and pred != b:
                    return False
                
                pair_key = tuple(sorted([a, b]))
                if pair_key in self.compared_pairs:
                    return False
                
                correct_answer = self._compare_nodes(a, b)
                if pred != correct_answer:
                    all_correct = False
            
            return all_correct
            
        except Exception:
            return False

    def _compare_nodes(self, a, b):
        if self.node_position[a] < self.node_position[b]:
            return a
        else:
            return b

    def _compare_siblings(self, parent, c1, c2):
        if parent not in self.sorted_children:
            raise ValueError("Invalid parent node")
        
        children = self.sorted_children[parent]
        if c1 not in children or c2 not in children:
            raise ValueError("Nodes are not children of the parent")
        
        idx1 = children.index(c1)
        idx2 = children.index(c2)
        
        return c1 if idx1 < idx2 else c2

    def _cf_core_produce(self, parsed_info):
        try:
            if "query_compare" in parsed_info:
                raw = parsed_info["query_compare"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError("Invalid compare query format")
                
                a, b = int(parts[0]), int(parts[1])
                
                if a < 1 or a > self.n or b < 1 or b > self.n:
                    if self.config.language == "zh":
                        return "错误：节点编号超出范围。"
                    else:
                        return "Error: Node ID out of range."
                
                pair_key = tuple(sorted([a, b]))
                self.compared_pairs.add(pair_key)
                
                result = self._compare_nodes(a, b)
                return str(result)
            
            elif "query_sibling" in parsed_info:
                raw = parsed_info["query_sibling"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 3:
                    raise ValueError("Invalid sibling query format")
                
                p, c1, c2 = int(parts[0]), int(parts[1]), int(parts[2])
                
                if p < 1 or p > self.n or c1 < 1 or c1 > self.n or c2 < 1 or c2 > self.n:
                    if self.config.language == "zh":
                        return "错误：节点编号超出范围。"
                    else:
                        return "Error: Node ID out of range."
                
                result = self._compare_siblings(p, c1, c2)
                return str(result)
            
            else:
                raise ValueError("No valid query tag found.")
                
        except ValueError as e:
            if self.config.language == "zh":
                return f"错误：{str(e)}"
            else:
                return f"Error: {str(e)}"
        except Exception:
            if self.config.language == "zh":
                return "错误：查询格式无效。"
            else:
                return "Error: Invalid query format."

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if "是" in correct:
            return correct.replace("是", "否")
        elif "否" in correct:
            return correct.replace("否", "是")
        elif "Yes" in correct:
             return re.sub(r'Yes', 'No', correct, flags=re.IGNORECASE)
        elif "No" in correct:
             return re.sub(r'No', 'Yes', correct, flags=re.IGNORECASE)
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        for a in range(1, self.n + 1):
            for b in range(a + 1, self.n + 1):
                ans = self._compare_nodes(a, b)
                queries.append({
                    "query": f"<query_compare>{a},{b}</query_compare>",
                    "answer": str(ans)
                })

        for parent, children in self.tree.items():
            if len(children) < 2:
                continue
            
            sorted_kids = sorted(children)
            for i in range(len(sorted_kids)):
                for j in range(i + 1, len(sorted_kids)):
                    c1 = sorted_kids[i]
                    c2 = sorted_kids[j]
                    ans = self._compare_siblings(parent, c1, c2)
                    queries.append({
                        "query": f"<query_sibling>{parent},{c1},{c2}</query_sibling>",
                        "answer": str(ans)
                    })
                    
        return queries