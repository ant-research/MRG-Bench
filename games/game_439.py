from .base import Game
import re
import random as _random

class TreeProbeGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"树节点识别"的推理游戏，规则如下：

游戏设定了一棵有限有序根树，节点用子序号序列标识。根节点为空序列 []。树的完整结构如下：

- [] 的子节点：[1], [2], [3]
  - [1] 的子节点：[1,1], [1,2]
    - [1,1] 的子节点：[1,1,1], [1,1,2]
    - [1,2] 的子节点：[1,2,1]
  - [2] 的子节点：[2,1], [2,2], [2,3]
    - [2,1] 的子节点：[2,1,1]
    - [2,2] 的子节点：[2,2,1], [2,2,2]
      - [2,2,1] 的子节点：[2,2,1,1]
    - [2,3] 无子节点
  - [3] 的子节点：[3,1], [3,2]
    - [3,1] 的子节点：[3,1,1], [3,1,2]
      - [3,1,2] 的子节点：[3,1,2,1]
    - [3,2] 无子节点

定义：
- 节点 X 的深度 d(X) 为其序列长度（例如 [2,1] 的深度为 2）
- 节点 X 与目标节点 T 的公共前缀长度 c(X,T) 为从序列起始处连续相同项的数量

我已秘密选定了一个目标节点 T（深度大于等于 2）和一条反馈法则 L（从 L1、L2、L3、L4 中选择）。

四条法则的定义如下：
- L1: r = c(X,T) 对 3 取模
- L2: r = (d(X) 减 c(X,T)) 对 3 取模
- L3: r = (2 乘 c(X,T) 加 d(X)) 对 3 取模
- L4: r = (c(X,T) 加 1) 对 3 取模

你可以进行以下操作（每次仅限一个操作）：

1. 探测节点：指定一个树中的节点 X，我会根据法则返回一个反馈值 r（0、1 或 2）
2. 查询剩余次数：询问还可以探测多少次
3. 请求树结构：要求重复树的完整结构描述
4. 提交答案：给出你判定的法则编号（L1/L2/L3/L4）和目标节点的完整序列

限制：
- 探测次数上限为 {max_probes} 次
- 除探测操作外，你不能直接询问目标节点位置或其相关信息

你的目标是：在探测次数限制内，推断出正确的法则和目标节点。

每次只能包含一个标签，使用以下 XML 格式：

- 探测节点（例如探测 [2,1]）：
<probe>[2,1]</probe>

- 探测根节点：
<probe>[]</probe>

- 查询剩余次数：
<query_remaining></query_remaining>

- 请求树结构：
<query_tree></query_tree>

- 提交最终答案（例如法则 L3，目标节点 [2,2,1]）：
<answer>rule=L3, target=[2,2,1]</answer>
"""

    game_rule_en = """\
Let's play a "Tree Node Identification" deduction game. Here are the rules:

The game has a finite ordered rooted tree, where nodes are identified by child index sequences. The root node is the empty sequence []. The complete tree structure is:

- [] has children: [1], [2], [3]
  - [1] has children: [1,1], [1,2]
    - [1,1] has children: [1,1,1], [1,1,2]
    - [1,2] has children: [1,2,1]
  - [2] has children: [2,1], [2,2], [2,3]
    - [2,1] has children: [2,1,1]
    - [2,2] has children: [2,2,1], [2,2,2]
      - [2,2,1] has children: [2,2,1,1]
    - [2,3] has no children
  - [3] has children: [3,1], [3,2]
    - [3,1] has children: [3,1,1], [3,1,2]
      - [3,1,2] has children: [3,1,2,1]
    - [3,2] has no children

Definitions:
- Depth d(X) of node X is the length of its sequence (e.g., [2,1] has depth 2)
- Common prefix length c(X,T) between node X and target node T is the number of consecutive matching items from the start

I have secretly chosen a target node T (with depth greater than or equal to 2) and a feedback rule L (chosen from L1, L2, L3, L4).

The four rules are defined as:
- L1: r = c(X,T) mod 3
- L2: r = (d(X) minus c(X,T)) mod 3
- L3: r = (2 times c(X,T) plus d(X)) mod 3
- L4: r = (c(X,T) plus 1) mod 3

You can perform the following operations (one per turn):

1. Probe a node: Specify a node X in the tree, and I will return a feedback value r (0, 1, or 2) according to the rule
2. Query remaining probes: Ask how many probes you have left
3. Request tree structure: Ask for the complete tree structure description
4. Submit answer: Provide your deduced rule number (L1/L2/L3/L4) and the complete sequence of the target node

Constraints:
- Maximum number of probes: {max_probes}
- You cannot directly ask about the target node's location or related information except through probing

Your goal: Within the probe limit, deduce the correct rule and target node.

Each operation must contain only one tag. Use the following XML format:

- Probe a node (e.g., probe [2,1]):
<probe>[2,1]</probe>

- Probe root node:
<probe>[]</probe>

- Query remaining probes:
<query_remaining></query_remaining>

- Request tree structure:
<query_tree></query_tree>

- Submit final answer (e.g., rule L3, target node [2,2,1]):
<answer>rule=L3, target=[2,2,1]</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎进入【城市交通路网故障排查系统】。

我们正在排查一棵呈有限有序根树结构的交通路网，节点用路由序列标识。总枢纽为 []，完整网络拓扑如下：

- [] 下辖子级枢纽：[1], [2], [3]
  - [1] 下辖：[1,1], [1,2]
    - [1,1] 下辖：[1,1,1], [1,1,2]
    - [1,2] 下辖：[1,2,1]
  - [2] 下辖：[2,1], [2,2], [2,3]
    - [2,1] 下辖：[2,1,1]
    - [2,2] 下辖：[2,2,1], [2,2,2]
      - [2,2,1] 下辖：[2,2,1,1]
    - [2,3] 无下辖子枢纽
  - [3] 下辖：[3,1], [3,2]
    - [3,1] 下辖：[3,1,1], [3,1,2]
      - [3,1,2] 下辖：[3,1,2,1]
    - [3,2] 无下辖子枢纽

系统定义：
- 节点 X 的路由跳数 d(X) 为其序列长度（例如 [2,1] 的路由跳数为 2）
- 节点 X 与故障节点 T 的重合路径段数 c(X,T) 为从序列起始处连续相同项的数量

系统已秘密锁定了一个发生信号灯故障的路口 T（路由跳数大于等于 2），并采用了一种诊断协议 L（从 L1、L2、L3、L4 中选择）。

四种诊断协议的状态反馈码 r（0、1 或 2）计算如下：
- L1: r = c(X,T) 对 3 取模
- L2: r = (d(X) 减 c(X,T)) 对 3 取模
- L3: r = (2 乘 c(X,T) 加 d(X)) 对 3 取模
- L4: r = (c(X,T) 加 1) 对 3 取模

你可以进行以下操作（每次仅限一个操作）：

1. 发送探针：指定网络中的一个节点 X，系统会根据诊断协议返回状态码 r（0、1 或 2）
2. 查询剩余次数：询问还剩余多少次探针发送配额
3. 请求拓扑图：要求重复完整的交通路网结构
4. 提交报告：给出你判定的诊断协议编号（L1/L2/L3/L4）和故障节点的完整路由序列

限制：
- 发送探针的次数上限为 {max_probes} 次
- 除探针诊断外，你不能直接询问故障节点的相关信息

你的目标是：在配额耗尽前，排查出准确的诊断协议和故障节点的路由序列。

每次只能包含一个标签，使用以下 XML 格式：

- 发送探针（例如探测 [2,1]）：
<probe>[2,1]</probe>

- 探测总枢纽：
<probe>[]</probe>

- 查询剩余次数：
<query_remaining></query_remaining>

- 请求拓扑图：
<query_tree></query_tree>

- 提交最终报告（例如协议 L3，故障节点 [2,2,1]）：
<answer>rule=L3, target=[2,2,1]</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Urban Traffic Network Troubleshooting System.

We are inspecting a traffic network structured as a finite ordered rooted tree, where nodes are identified by routing sequences. The central hub is [], and the complete network topology is:

- [] has sub-hubs: [1], [2], [3]
  - [1] has sub-hubs: [1,1], [1,2]
    - [1,1] has sub-hubs: [1,1,1], [1,1,2]
    - [1,2] has sub-hubs: [1,2,1]
  - [2] has sub-hubs: [2,1], [2,2], [2,3]
    - [2,1] has sub-hubs: [2,1,1]
    - [2,2] has sub-hubs: [2,2,1], [2,2,2]
      - [2,2,1] has sub-hubs: [2,2,1,1]
    - [2,3] has no sub-hubs
  - [3] has sub-hubs: [3,1], [3,2]
    - [3,1] has sub-hubs: [3,1,1], [3,1,2]
      - [3,1,2] has sub-hubs: [3,1,2,1]
    - [3,2] has no sub-hubs

System Definitions:
- Routing hop count d(X) of node X is the length of its sequence (e.g., [2,1] has a hop count of 2)
- Overlapping path segment count c(X,T) between node X and the faulty node T is the number of consecutive matching items from the start

The system has secretly locked onto a hidden faulty intersection T (with a hop count >= 2) and applied a diagnostic protocol L (chosen from L1, L2, L3, L4).

The feedback status code r (0, 1, or 2) for the four diagnostic protocols is calculated as:
- L1: r = c(X,T) mod 3
- L2: r = (d(X) minus c(X,T)) mod 3
- L3: r = (2 times c(X,T) plus d(X)) mod 3
- L4: r = (c(X,T) plus 1) mod 3

You can perform the following operations (one per turn):

1. Send probe: Specify a node X in the network, and the system will return a status code r (0, 1, or 2) based on the protocol
2. Query remaining probes: Ask how many diagnostic probe quotas you have left
3. Request topology: Ask for the complete traffic network structure description
4. Submit report: Provide your deduced protocol number (L1/L2/L3/L4) and the complete routing sequence of the faulty intersection

Constraints:
- Maximum number of probes: {max_probes}
- You cannot directly ask about the faulty intersection's location or related information except through diagnostic probing

Your goal: Within the probe quota, deduce the correct diagnostic protocol and the faulty intersection's routing sequence.

Each operation must contain only one tag. Use the following XML format:

- Send probe (e.g., probe [2,1]):
<probe>[2,1]</probe>

- Probe central hub:
<probe>[]</probe>

- Query remaining probes:
<query_remaining></query_remaining>

- Request topology:
<query_tree></query_tree>

- Submit final report (e.g., protocol L3, faulty target [2,2,1]):
<answer>rule=L3, target=[2,2,1]</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用【神经中枢病灶定位系统】。

我们正在分析一个呈有限有序根树结构的神经干网络，节点用分支序列标识。大脑主干为 []，完整神经结构如下：

- [] 的下级分支：[1], [2], [3]
  - [1] 的下级分支：[1,1], [1,2]
    - [1,1] 的下级分支：[1,1,1], [1,1,2]
    - [1,2] 的下级分支：[1,2,1]
  - [2] 的下级分支：[2,1], [2,2], [2,3]
    - [2,1] 的下级分支：[2,1,1]
    - [2,2] 的下级分支：[2,2,1], [2,2,2]
      - [2,2,1] 的下级分支：[2,2,1,1]
    - [2,3] 无下级分支
  - [3] 的下级分支：[3,1], [3,2]
    - [3,1] 的下级分支：[3,1,1], [3,1,2]
      - [3,1,2] 的下级分支：[3,1,2,1]
    - [3,2] 无下级分支

医学定义：
- 神经分支 X 的层级深度 d(X) 为其序列长度（例如 [2,1] 的层级深度为 2）
- 神经分支 X 与病变突触 T 的共享神经干长度 c(X,T) 为从序列起始处连续相同项的数量

系统已秘密锁定了一个发生病变的突触 T（层级深度大于等于 2），并采用了一种病理反射机制 L（从 L1、L2、L3、L4 中选择）。

四种反射机制的应激强度等级 r（0、1 或 2）计算如下：
- L1: r = c(X,T) 对 3 取模
- L2: r = (d(X) 减 c(X,T)) 对 3 取模
- L3: r = (2 乘 c(X,T) 加 d(X)) 对 3 取模
- L4: r = (c(X,T) 加 1) 对 3 取模

你可以进行以下操作（每次仅限一个操作）：

1. 施加刺激：指定一个神经分支 X，系统将根据反射机制返回应激强度等级 r（0、1 或 2）
2. 查询剩余次数：询问患者还能承受多少次电刺激
3. 请求结构图：要求重复完整的神经分支结构
4. 提交诊断：给出你判定的反射机制编号（L1/L2/L3/L4）和病变突触的完整序列

限制：
- 电刺激的次数上限为 {max_probes} 次
- 除电刺激外，你不能直接询问病变突触的相关信息

你的目标是：在刺激次数限制内，推断出准确的反射机制和病变突触序列。

每次只能包含一个标签，使用以下 XML 格式：

- 施加刺激（例如刺激 [2,1]）：
<probe>[2,1]</probe>

- 刺激大脑主干：
<probe>[]</probe>

- 查询剩余次数：
<query_remaining></query_remaining>

- 请求结构图：
<query_tree></query_tree>

- 提交最终诊断（例如机制 L3，病变突触 [2,2,1]）：
<answer>rule=L3, target=[2,2,1]</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Neural Center Lesion Localization System.

We are analyzing a neural trunk network structured as a finite ordered rooted tree, where nodes are identified by branch sequences. The main brain trunk is [], and the complete neural structure is:

- [] has lower branches: [1], [2], [3]
  - [1] has lower branches: [1,1], [1,2]
    - [1,1] has lower branches: [1,1,1], [1,1,2]
    - [1,2] has lower branches: [1,2,1]
  - [2] has lower branches: [2,1], [2,2], [2,3]
    - [2,1] has lower branches: [2,1,1]
    - [2,2] has lower branches: [2,2,1], [2,2,2]
      - [2,2,1] has lower branches: [2,2,1,1]
    - [2,3] has no lower branches
  - [3] has lower branches: [3,1], [3,2]
    - [3,1] has lower branches: [3,1,1], [3,1,2]
      - [3,1,2] has lower branches: [3,1,2,1]
    - [3,2] has no lower branches

Medical Definitions:
- Hierarchical depth d(X) of neural branch X is the length of its sequence (e.g., [2,1] has depth 2)
- Shared neural trunk length c(X,T) between neural branch X and lesion synapse T is the number of consecutive matching items from the start

The system has secretly locked onto a lesion synapse T (with depth >= 2) and applied a pathological reflex mechanism L (chosen from L1, L2, L3, L4).

The stress intensity level r (0, 1, or 2) returned by the four reflex mechanisms is calculated as:
- L1: r = c(X,T) mod 3
- L2: r = (d(X) minus c(X,T)) mod 3
- L3: r = (2 times c(X,T) plus d(X)) mod 3
- L4: r = (c(X,T) plus 1) mod 3

You can perform the following operations (one per turn):

1. Apply stimulus: Specify a neural branch X, and the system will return a stress intensity level r (0, 1, or 2) based on the reflex mechanism
2. Query remaining stimuli: Ask how many more electrical stimuli the patient can tolerate
3. Request structure diagram: Ask for the complete neural branch structure description
4. Submit diagnosis: Provide your deduced reflex mechanism number (L1/L2/L3/L4) and the complete sequence of the lesion synapse

Constraints:
- Maximum number of electrical stimuli: {max_probes}
- You cannot directly ask about the lesion synapse's location or related information except through electrical stimulation

Your goal: Within the stimulus limit, deduce the correct reflex mechanism and the lesion synapse's sequence.

Each operation must contain only one tag. Use the following XML format:

- Apply stimulus (e.g., probe [2,1]):
<probe>[2,1]</probe>

- Stimulate main brain trunk:
<probe>[]</probe>

- Query remaining stimuli:
<query_remaining></query_remaining>

- Request structure diagram:
<query_tree></query_tree>

- Submit final diagnosis (e.g., mechanism L3, lesion target [2,2,1]):
<answer>rule=L3, target=[2,2,1]</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用【学生知识图谱薄弱点分析系统】。

我们正在分析一棵呈有限有序根树结构的学科知识大纲，知识节点用层级序列标识。核心素养根节点为 []，完整的知识图谱结构如下：

- [] 的下级概念：[1], [2], [3]
  - [1] 的下级概念：[1,1], [1,2]
    - [1,1] 的下级概念：[1,1,1], [1,1,2]
    - [1,2] 的下级概念：[1,2,1]
  - [2] 的下级概念：[2,1], [2,2], [2,3]
    - [2,1] 的下级概念：[2,1,1]
    - [2,2] 的下级概念：[2,2,1], [2,2,2]
      - [2,2,1] 的下级概念：[2,2,1,1]
    - [2,3] 无下级概念
  - [3] 的下级概念：[3,1], [3,2]
    - [3,1] 的下级概念：[3,1,1], [3,1,2]
      - [3,1,2] 的下级概念：[3,1,2,1]
    - [3,2] 无下级概念

教研定义：
- 知识节点 X 的深度 d(X) 为其序列长度（例如 [2,1] 的深度为 2）
- 知识节点 X 与薄弱节点 T 的共同前置概念数 c(X,T) 为从序列起始处连续相同项的数量

系统已秘密锁定了一个学生存在严重认知偏差的薄弱知识节点 T（深度大于等于 2），并采用了一种认知诊断模型 L（从 L1、L2、L3、L4 中选择）。

四种诊断模型返回的能力差异代码 r（0、1 或 2）计算如下：
- L1: r = c(X,T) 对 3 取模
- L2: r = (d(X) 减 c(X,T)) 对 3 取模
- L3: r = (2 乘 c(X,T) 加 d(X)) 对 3 取模
- L4: r = (c(X,T) 加 1) 对 3 取模

你可以进行以下操作（每次仅限一个操作）：

1. 推送测试：指定一个知识节点 X，系统将根据诊断模型返回能力差异代码 r（0、1 或 2）
2. 查询剩余题量：询问为避免学生疲劳还能推送多少道测试题
3. 请求图谱结构：要求重复完整的知识图谱大纲
4. 提交干预方案：给出你判定的诊断模型编号（L1/L2/L3/L4）和薄弱知识节点的完整序列

限制：
- 测试推送的次数上限为 {max_probes} 次
- 除推送诊断题外，你不能直接询问薄弱节点的相关信息

你的目标是：在推送题量限制内，推断出准确的诊断模型和薄弱知识节点序列。

每次只能包含一个标签，使用以下 XML 格式：

- 推送测试（例如推送 [2,1]）：
<probe>[2,1]</probe>

- 推送核心素养根节点：
<probe>[]</probe>

- 查询剩余题量：
<query_remaining></query_remaining>

- 请求图谱结构：
<query_tree></query_tree>

- 提交干预方案（例如模型 L3，薄弱节点 [2,2,1]）：
<answer>rule=L3, target=[2,2,1]</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Student Knowledge Graph Weakness Analysis System.

We are analyzing a subject knowledge syllabus structured as a finite ordered rooted tree, where knowledge nodes are identified by hierarchical sequences. The core competency root node is [], and the complete knowledge graph structure is:

- [] has subordinate concepts: [1], [2], [3]
  - [1] has subordinate concepts: [1,1], [1,2]
    - [1,1] has subordinate concepts: [1,1,1], [1,1,2]
    - [1,2] has subordinate concepts: [1,2,1]
  - [2] has subordinate concepts: [2,1], [2,2], [2,3]
    - [2,1] has subordinate concepts: [2,1,1]
    - [2,2] has subordinate concepts: [2,2,1], [2,2,2]
      - [2,2,1] has subordinate concepts: [2,2,1,1]
    - [2,3] has no subordinate concepts
  - [3] has subordinate concepts: [3,1], [3,2]
    - [3,1] has subordinate concepts: [3,1,1], [3,1,2]
      - [3,1,2] has subordinate concepts: [3,1,2,1]
    - [3,2] has no subordinate concepts

Pedagogical Definitions:
- Depth d(X) of knowledge node X is the length of its sequence (e.g., [2,1] has depth 2)
- Common prerequisite concepts count c(X,T) between node X and weak node T is the number of consecutive matching items from the start

The system has secretly locked onto a weak knowledge node T where the student has severe cognitive bias (with depth >= 2) and applied a cognitive diagnostic model L (chosen from L1, L2, L3, L4).

The capability gap code r (0, 1, or 2) returned by the four diagnostic models is calculated as:
- L1: r = c(X,T) mod 3
- L2: r = (d(X) minus c(X,T)) mod 3
- L3: r = (2 times c(X,T) plus d(X)) mod 3
- L4: r = (c(X,T) plus 1) mod 3

You can perform the following operations (one per turn):

1. Push test: Specify a knowledge node X, and the system will return a capability gap code r (0, 1, or 2) based on the diagnostic model
2. Query remaining questions: Ask how many more test questions can be pushed before student fatigue
3. Request graph structure: Ask for the complete knowledge graph syllabus description
4. Submit intervention plan: Provide your deduced diagnostic model number (L1/L2/L3/L4) and the complete sequence of the weak knowledge node

Constraints:
- Maximum number of test pushes: {max_probes}
- You cannot directly ask about the weak node's location or related information except through pushing diagnostic tests

Your goal: Within the test push limit, deduce the correct diagnostic model and the weak knowledge node's sequence.

Each operation must contain only one tag. Use the following XML format:

- Push test (e.g., probe [2,1]):
<probe>[2,1]</probe>

- Probe core competency root node:
<probe>[]</probe>

- Query remaining questions:
<query_remaining></query_remaining>

- Request graph structure:
<query_tree></query_tree>

- Submit final intervention plan (e.g., model L3, weak target [2,2,1]):
<answer>rule=L3, target=[2,2,1]</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎进入【流水线层级质量追溯系统】。

我们正在排查一个呈有限有序根树结构的生产工艺网，工序节点用加工序列标识。产品总装车间为 []，完整的生产流程层级如下：

- [] 的下级工序：[1], [2], [3]
  - [1] 的下级工序：[1,1], [1,2]
    - [1,1] 的下级工序：[1,1,1], [1,1,2]
    - [1,2] 的下级工序：[1,2,1]
  - [2] 的下级工序：[2,1], [2,2], [2,3]
    - [2,1] 的下级工序：[2,1,1]
    - [2,2] 的下级工序：[2,2,1], [2,2,2]
      - [2,2,1] 的下级工序：[2,2,1,1]
    - [2,3] 无下级工序
  - [3] 的下级工序：[3,1], [3,2]
    - [3,1] 的下级工序：[3,1,1], [3,1,2]
      - [3,1,2] 的下级工序：[3,1,2,1]
    - [3,2] 无下级工序

质量控制定义：
- 工序 X 的加工层级 d(X) 为其序列长度（例如 [2,1] 的加工层级为 2）
- 工序 X 与缺陷根源工序 T 的共同加工链路长度 c(X,T) 为从序列起始处连续相同项的数量

系统已秘密锁定了一个导致产品缺陷的根源工序 T（加工层级大于等于 2），并采用了一种质量检测算法 L（从 L1、L2、L3、L4 中选择）。

四种检测算法反馈的偏差指示码 r（0、1 或 2）计算如下：
- L1: r = c(X,T) 对 3 取模
- L2: r = (d(X) 减 c(X,T)) 对 3 取模
- L3: r = (2 乘 c(X,T) 加 d(X)) 对 3 取模
- L4: r = (c(X,T) 加 1) 对 3 取模

你可以进行以下操作（每次仅限一个操作）：

1. 抽样检测：指定一个工序节点 X，系统将根据检测算法返回偏差指示码 r（0、1 或 2）
2. 查询剩余批次：询问还能进行多少次抽样检测
3. 请求工艺流程：要求重复完整的生产流程图
4. 提交追溯报告：给出你判定的检测算法编号（L1/L2/L3/L4）和缺陷根源工序的完整序列

限制：
- 抽样检测的次数上限为 {max_probes} 次
- 除抽检外，你不能直接询问缺陷工序的相关信息

你的目标是：在抽检批次耗尽前，排查出准确的检测算法和缺陷根源工序序列。

每次只能包含一个标签，使用以下 XML 格式：

- 抽样检测（例如抽检 [2,1]）：
<probe>[2,1]</probe>

- 抽检总装车间：
<probe>[]</probe>

- 查询剩余批次：
<query_remaining></query_remaining>

- 请求工艺流程：
<query_tree></query_tree>

- 提交追溯报告（例如算法 L3，缺陷工序 [2,2,1]）：
<answer>rule=L3, target=[2,2,1]</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the Assembly Line Quality Traceability System.

We are inspecting a production process network structured as a finite ordered rooted tree, where process nodes are identified by processing sequences. The main assembly workshop is [], and the complete production process hierarchy is:

- [] has subsequent processes: [1], [2], [3]
  - [1] has subsequent processes: [1,1], [1,2]
    - [1,1] has subsequent processes: [1,1,1], [1,1,2]
    - [1,2] has subsequent processes: [1,2,1]
  - [2] has subsequent processes: [2,1], [2,2], [2,3]
    - [2,1] has subsequent processes: [2,1,1]
    - [2,2] has subsequent processes: [2,2,1], [2,2,2]
      - [2,2,1] has subsequent processes: [2,2,1,1]
    - [2,3] has no subsequent processes
  - [3] has subsequent processes: [3,1], [3,2]
    - [3,1] has subsequent processes: [3,1,1], [3,1,2]
      - [3,1,2] has subsequent processes: [3,1,2,1]
    - [3,2] has no subsequent processes

Quality Control Definitions:
- Processing level d(X) of process X is the length of its sequence (e.g., [2,1] has a processing level of 2)
- Common processing link length c(X,T) between process X and root cause defect process T is the number of consecutive matching items from the start

The system has secretly locked onto a root cause process T causing product defects (with processing level >= 2) and applied a quality detection algorithm L (chosen from L1, L2, L3, L4).

The deviation indicator code r (0, 1, or 2) for the four detection algorithms is calculated as:
- L1: r = c(X,T) mod 3
- L2: r = (d(X) minus c(X,T)) mod 3
- L3: r = (2 times c(X,T) plus d(X)) mod 3
- L4: r = (c(X,T) plus 1) mod 3

You can perform the following operations (one per turn):

1. Sample test: Specify a process node X, and the system will return a deviation indicator code r (0, 1, or 2) based on the detection algorithm
2. Query remaining batches: Ask how many more sampling test batches you can perform
3. Request process flow: Ask for the complete production process hierarchy description
4. Submit traceability report: Provide your deduced detection algorithm number (L1/L2/L3/L4) and the complete sequence of the root cause defect process

Constraints:
- Maximum number of sampling tests: {max_probes}
- You cannot directly ask about the defect process's location or related information except through sampling tests

Your goal: Within the test batch limit, deduce the correct detection algorithm and the root cause defect process's sequence.

Each operation must contain only one tag. Use the following XML format:

- Sample test (e.g., probe [2,1]):
<probe>[2,1]</probe>

- Sample test main assembly workshop:
<probe>[]</probe>

- Query remaining batches:
<query_remaining></query_remaining>

- Request process flow:
<query_tree></query_tree>

- Submit traceability report (e.g., algorithm L3, defect target [2,2,1]):
<answer>rule=L3, target=[2,2,1]</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用【股权架构及合规穿透调查系统】。

我们正在审查一个呈有限有序根树结构的公司股权控制网，公司实体用投资层级序列标识。顶层控股母公司为 []，已知的股权架构如下：

- [] 的控股子公司：[1], [2], [3]
  - [1] 的控股子公司：[1,1], [1,2]
    - [1,1] 的控股子公司：[1,1,1], [1,1,2]
    - [1,2] 的控股子公司：[1,2,1]
  - [2] 的控股子公司：[2,1], [2,2], [2,3]
    - [2,1] 的控股子公司：[2,1,1]
    - [2,2] 的控股子公司：[2,2,1], [2,2,2]
      - [2,2,1] 的控股子公司：[2,2,1,1]
    - [2,3] 无控股子公司
  - [3] 的控股子公司：[3,1], [3,2]
    - [3,1] 的控股子公司：[3,1,1], [3,1,2]
      - [3,1,2] 的控股子公司：[3,1,2,1]
    - [3,2] 无控股子公司

审计定义：
- 公司 X 的投资层级 d(X) 为其序列长度（例如 [2,1] 的投资层级为 2）
- 公司 X 与违规公司 T 的共同控股上级数量 c(X,T) 为从序列起始处连续相同项的数量

系统已秘密锁定了一个存在资金违规流转的底层公司 T（投资层级大于等于 2），并采用了一种资金穿透审查标准 L（从 L1、L2、L3、L4 中选择）。

四种审查标准返回的风险特征码 r（0、1 或 2）计算如下：
- L1: r = c(X,T) 对 3 取模
- L2: r = (d(X) 减 c(X,T)) 对 3 取模
- L3: r = (2 乘 c(X,T) 加 d(X)) 对 3 取模
- L4: r = (c(X,T) 加 1) 对 3 取模

你可以进行以下操作（每次仅限一个操作）：

1. 穿透审计：指定一个公司节点 X，系统将根据审查标准返回风险特征码 r（0、1 或 2）
2. 查询剩余授权：询问还可以发起多少次穿透审计
3. 请求架构图：要求重复完整的股权架构图
4. 提交调查报告：给出你判定的审查标准编号（L1/L2/L3/L4）和违规底层公司的完整序列

限制：
- 穿透审计的授权次数上限为 {max_probes} 次
- 除穿透审计外，你不能直接询问违规公司的相关信息

你的目标是：在授权次数限制内，推断出准确的审查标准和违规底层公司序列。

每次只能包含一个标签，使用以下 XML 格式：

- 穿透审计（例如审计 [2,1]）：
<probe>[2,1]</probe>

- 审计顶层母公司：
<probe>[]</probe>

- 查询剩余授权：
<query_remaining></query_remaining>

- 请求架构图：
<query_tree></query_tree>

- 提交调查报告（例如审查标准 L3，违规公司 [2,2,1]）：
<answer>rule=L3, target=[2,2,1]</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Equity Architecture and Compliance Penetration Investigation System.

We are reviewing a corporate equity control network structured as a finite ordered rooted tree, where corporate entities are identified by investment hierarchy sequences. The top-level holding parent company is [], and the known equity architecture is:

- [] has holding subsidiaries: [1], [2], [3]
  - [1] has holding subsidiaries: [1,1], [1,2]
    - [1,1] has holding subsidiaries: [1,1,1], [1,1,2]
    - [1,2] has holding subsidiaries: [1,2,1]
  - [2] has holding subsidiaries: [2,1], [2,2], [2,3]
    - [2,1] has holding subsidiaries: [2,1,1]
    - [2,2] has holding subsidiaries: [2,2,1], [2,2,2]
      - [2,2,1] has holding subsidiaries: [2,2,1,1]
    - [2,3] has no holding subsidiaries
  - [3] has holding subsidiaries: [3,1], [3,2]
    - [3,1] has holding subsidiaries: [3,1,1], [3,1,2]
      - [3,1,2] has holding subsidiaries: [3,1,2,1]
    - [3,2] has no holding subsidiaries

Auditing Definitions:
- Investment hierarchy d(X) of company X is the length of its sequence (e.g., [2,1] has a hierarchy of 2)
- Common holding superiors count c(X,T) between company X and the non-compliant company T is the number of consecutive matching items from the start

The system has secretly locked onto a bottom-level company T involved in illegal fund transfers (with investment hierarchy >= 2) and applied a fund penetration review standard L (chosen from L1, L2, L3, L4).

The risk feature code r (0, 1, or 2) returned by the four review standards is calculated as:
- L1: r = c(X,T) mod 3
- L2: r = (d(X) minus c(X,T)) mod 3
- L3: r = (2 times c(X,T) plus d(X)) mod 3
- L4: r = (c(X,T) plus 1) mod 3

You can perform the following operations (one per turn):

1. Penetration audit: Specify a company node X, and the system will return a risk feature code r (0, 1, or 2) based on the review standard
2. Query remaining authorizations: Ask how many more penetration audits you are authorized to initiate
3. Request architecture: Ask for the complete equity architecture description
4. Submit investigation report: Provide your deduced review standard number (L1/L2/L3/L4) and the complete sequence of the non-compliant bottom-level company

Constraints:
- Maximum number of penetration audits: {max_probes}
- You cannot directly ask about the non-compliant company's location or related information except through penetration audits

Your goal: Within the authorization limit, deduce the correct review standard and the non-compliant bottom-level company's sequence.

Each operation must contain only one tag. Use the following XML format:

- Penetration audit (e.g., probe [2,1]):
<probe>[2,1]</probe>

- Penetration audit top-level parent company:
<probe>[]</probe>

- Query remaining authorizations:
<query_remaining></query_remaining>

- Request architecture:
<query_tree></query_tree>

- Submit investigation report (e.g., review standard L3, non-compliant target [2,2,1]):
<answer>rule=L3, target=[2,2,1]</answer>
"""

    tags = ["answer", "probe", "query_remaining", "query_tree"]

    TREE_NODES = {
        "[]": [],
        "[1]": [1],
        "[2]": [2],
        "[3]": [3],
        "[1,1]": [1, 1],
        "[1,2]": [1, 2],
        "[2,1]": [2, 1],
        "[2,2]": [2, 2],
        "[2,3]": [2, 3],
        "[3,1]": [3, 1],
        "[3,2]": [3, 2],
        "[1,1,1]": [1, 1, 1],
        "[1,1,2]": [1, 1, 2],
        "[1,2,1]": [1, 2, 1],
        "[2,1,1]": [2, 1, 1],
        "[2,2,1]": [2, 2, 1],
        "[2,2,2]": [2, 2, 2],
        "[3,1,1]": [3, 1, 1],
        "[3,1,2]": [3, 1, 2],
        "[2,2,1,1]": [2, 2, 1, 1],
        "[3,1,2,1]": [3, 1, 2, 1],
    }

    CANDIDATE_TARGETS = [
        [1, 1], [1, 2], [2, 1], [2, 2], [2, 3], [3, 1], [3, 2],
        [1, 1, 1], [1, 1, 2], [1, 2, 1], [2, 1, 1], [2, 2, 1], [2, 2, 2],
        [3, 1, 1], [3, 1, 2],
        [2, 2, 1, 1], [3, 1, 2, 1],
    ]

    DIFFICULTY_CONFIG = {
        1: {
            "min_depth": 2, "max_depth": 2,
            "rules": ["L1", "L2"],
            "max_probes": 12,
        },
        2: {
            "min_depth": 2, "max_depth": 2,
            "rules": ["L1", "L2", "L3", "L4"],
            "max_probes": 12,
        },
        3: {
            "min_depth": 2, "max_depth": 3,
            "rules": ["L1", "L2", "L3", "L4"],
            "max_probes": 12,
        },
        4: {
            "min_depth": 3, "max_depth": 4,
            "rules": ["L1", "L2", "L3", "L4"],
            "max_probes": 12,
        },
        5: {
            "min_depth": 3, "max_depth": 4,
            "rules": ["L3", "L4"],
            "max_probes": 12,
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = self.config.difficulty
        if isinstance(diff, str):
            diff = int(diff)
            
        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")
        
        cfg = self.DIFFICULTY_CONFIG[diff]
        
        rng = _random.Random()
        candidates = [t for t in self.CANDIDATE_TARGETS
                      if cfg["min_depth"] <= len(t) <= cfg["max_depth"]]
        
        self.target_node = rng.choice(candidates)
        self.rule = rng.choice(cfg["rules"])
        self.max_probes = cfg["max_probes"]
        self.probe_count = 0
        
        self._game_info["max_probes"] = self.max_probes

    def _compute_common_prefix_length(self, x, t):
        c = 0
        for i in range(min(len(x), len(t))):
            if x[i] == t[i]:
                c += 1
            else:
                break
        return c

    def _apply_rule(self, x_seq):
        d_x = len(x_seq)
        c_xt = self._compute_common_prefix_length(x_seq, self.target_node)
        
        if self.rule == "L1":
            r = c_xt % 3
        elif self.rule == "L2":
            r = (d_x - c_xt) % 3
        elif self.rule == "L3":
            r = (2 * c_xt + d_x) % 3
        elif self.rule == "L4":
            r = (c_xt + 1) % 3
        else:
            raise ValueError(f"Unknown rule: {self.rule}")
        
        return r

    def _parse_node_sequence(self, node_str):
        node_str = node_str.strip()
        if node_str == "[]":
            return []
        
        match = re.match(r'\[([\d,\s]+)\]', node_str)
        if match:
            nums_str = match.group(1)
            return [int(x.strip()) for x in nums_str.split(',')]
        
        raise ValueError(f"Invalid node format: {node_str}")

    def _format_node(self, seq):
        if not seq:
            return "[]"
        return "[" + ",".join(map(str, seq)) + "]"

    def evaluate(self, parsed_info):
        raw_ans = parsed_info.get("answer", "")
        
        try:
            rule_match = re.search(r'rule\s*=\s*(L[1-4])', raw_ans, re.IGNORECASE)
            target_match = re.search(r'target\s*=\s*(\[[^\]]*\])', raw_ans)
            
            if not rule_match or not target_match:
                return False
            
            ans_rule = rule_match.group(1).upper()
            if ans_rule != self.rule:
                return False
            
            target_seq = self._parse_node_sequence(target_match.group(1))
            return target_seq == self.target_node
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        is_zh = self.config.language == "zh"
        
        if "probe" in parsed_info:
            if self.probe_count >= self.max_probes:
                raise ValueError("Probe limit exceeded." if not is_zh else "探测次数已用尽。")
            
            try:
                node_str = parsed_info["probe"].strip()
                node_seq = self._parse_node_sequence(node_str)
                
                node_key = self._format_node(node_seq)
                if node_key not in self.TREE_NODES:
                    self.probe_count += 1
                    return "错误：该节点不在树中。" if is_zh else "Error: Node not in tree."
                
                self.probe_count += 1
                
                feedback = self._apply_rule(node_seq)
                
                return str(feedback)
                
            except ValueError:
                raise
            except Exception as e:
                return f"错误：节点格式无效。" if is_zh else f"Error: Invalid node format."
        
        elif "query_remaining" in parsed_info:
            remaining = self.max_probes - self.probe_count
            return str(remaining)
        
        elif "query_tree" in parsed_info:
            if is_zh:
                return """树结构：
- [] 的子节点：[1], [2], [3]
  - [1] 的子节点：[1,1], [1,2]
    - [1,1] 的子节点：[1,1,1], [1,1,2]
    - [1,2] 的子节点：[1,2,1]
  - [2] 的子节点：[2,1], [2,2], [2,3]
    - [2,1] 的子节点：[2,1,1]
    - [2,2] 的子节点：[2,2,1], [2,2,2]
      - [2,2,1] 的子节点：[2,2,1,1]
    - [2,3] 无子节点
  - [3] 的子节点：[3,1], [3,2]
    - [3,1] 的子节点：[3,1,1], [3,1,2]
      - [3,1,2] 的子节点：[3,1,2,1]
    - [3,2] 无子节点"""
            else:
                return """Tree structure:
- [] has children: [1], [2], [3]
  - [1] has children: [1,1], [1,2]
    - [1,1] has children: [1,1,1], [1,1,2]
    - [1,2] has children: [1,2,1]
  - [2] has children: [2,1], [2,2], [2,3]
    - [2,1] has children: [2,1,1]
    - [2,2] has children: [2,2,1], [2,2,2]
      - [2,2,1] has children: [2,2,1,1]
    - [2,3] has no children
  - [3] has children: [3,1], [3,2]
    - [3,1] has children: [3,1,1], [3,1,2]
      - [3,1,2] has children: [3,1,2,1]
    - [3,2] has no children"""
        
        else:
            raise ValueError("No valid operation tag found.")

    def _cf_make_wrong(self, correct):
        if correct in ["0", "1", "2"]:
            correct_val = int(correct)
            wrong_val = (correct_val + 1) % 3
            return str(wrong_val)
        return correct

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        for node_str, node_seq in self.TREE_NODES.items():
            result = self._apply_rule(node_seq)
            queries.append({
                "query": f"<probe>{node_str}</probe>",
                "answer": str(result)
            })
        return queries