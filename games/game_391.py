from .base import Game
import re

class TreePathDecryptionGame(Game):

    game_rule_zh = """\
我们现在来玩一个"树路径解密"的推理游戏，规则如下：

游戏设定了一棵有根树，根节点编号为 1。每个非叶节点都有若干子节点，这些子节点按顺序编号为 1, 2, 3, ...。整棵树的结构已知且固定。

树的结构如下：
{tree_structure}

我已秘密选择了一个目标节点 S，并记录了从根到 S 的路径。这条路径用子序号序列表示，例如 (2, 1, 3) 表示从根出发，选第 2 个子节点，再选它的第 1 个子节点，再选它的第 3 个子节点。

同时，我设定了一个秘密的符号映射 f，它将所有可能的子序号（1, 2, 3, ...）一一对应到一组符号（如字母 A, B, C, ...）。这个映射在整棵树中保持一致。另外，我还定义了一个特殊符号 END，表示已经到达目标节点。

你的目标是：
1. 推断出从根到目标节点 S 的完整路径（用子序号序列表示）。
2. 推断出在游戏过程中出现的所有符号到子序号的映射关系（包括 END 符号）。

你可以进行以下操作：

**探路查询**：
提交一个子序号序列，从根节点开始依次选择子节点。例如 (1, 2) 表示先选根的第 1 个子节点，再选它的第 2 个子节点。注意每一步的子序号必须在当前节点的有效范围内。

我会返回：
- 如果你的路径与目标路径完全一致，返回"到达：成功"。
- 否则，我会告诉你：
  - 共同步数（你的路径与目标路径有多少步是相同的）
  - 提示符号（一个加密后的符号，表示下一步正确的子序号；如果已经到达目标，则返回 END）

**提交最终答案**：
当你收集足够信息后，需要同时提交两项内容：
1. 目标路径的完整子序号序列
2. 所有历史反馈中出现过的符号到子序号的映射关系（必须包含 END 表示终点）

只有当路径和映射都正确时，游戏才算成功。

**探路查询**（提交子序号序列，用逗号分隔）：
<query_path>1,2,3</query_path>

**提交最终答案**（同时提交路径和映射）：
<answer>path=1,2,3; mapping=A->1,B->2,C->3,END->终点</answer>

注意：
- 路径用逗号分隔的子序号表示
- 映射用"符号->子序号"的格式，多个映射用逗号分隔
- END 必须映射到"终点"
- 请尽可能用最少的查询次数完成任务
"""

    game_rule_en = """\
Let's play a "Tree Path Decryption" reasoning game. Here are the rules:

A rooted tree is set up with root node numbered 1. Each non-leaf node has several child nodes, numbered in order as 1, 2, 3, ... The tree structure is known and fixed.

The tree structure is as follows:
{tree_structure}

I have secretly chosen a target node S and recorded the path from root to S. This path is represented as a sequence of child indices, e.g., (2, 1, 3) means starting from root, choose the 2nd child, then its 1st child, then its 3rd child.

Additionally, I have set up a secret symbol mapping f, which creates a one-to-one correspondence between all possible child indices (1, 2, 3, ...) and a set of symbols (such as letters A, B, C, ...). This mapping remains consistent throughout the entire tree. Furthermore, I have defined a special symbol END, indicating that the target node has been reached.

Your goals are:
1. Infer the complete path from root to target node S (represented as a sequence of child indices).
2. Infer the mapping from all symbols that appeared during the game to their corresponding child indices (including the END symbol).

You can perform the following operations:

**Path Query**:
Submit a sequence of child indices, starting from the root node and selecting children step by step. For example, (1, 2) means first select the 1st child of root, then select its 2nd child. Note that each step's child index must be within the valid range of the current node.

I will return:
- If your path exactly matches the target path, return "Reached: Success".
- Otherwise, I will tell you:
  - Common steps (how many steps your path shares with the target path)
  - Hint symbol (an encrypted symbol representing the correct child index for the next step; if already at target, return END)

**Submit Final Answer**:
When you have gathered enough information, you need to submit two items simultaneously:
1. The complete child index sequence of the target path
2. The mapping from all symbols that appeared in historical feedback to their child indices (must include END representing the endpoint)

The game succeeds only when both the path and mapping are correct.

**Path Query** (submit child index sequence, comma-separated):
<query_path>1,2,3</query_path>

**Submit Final Answer** (submit both path and mapping):
<answer>path=1,2,3; mapping=A->1,B->2,C->3,END->endpoint</answer>

Notes:
- Path is represented by comma-separated child indices
- Mapping uses "symbol->index" format, multiple mappings separated by commas
- END must map to "endpoint"
- Please complete the task with as few queries as possible
"""

    contextualized_rule_zh_1 = """\
我们现在来进行一项“交通路网事故追踪”任务，规则如下：

城市交通路网被建模为一棵有根树，根节点（交通枢纽）编号为 1。每个非叶节点代表一个交叉路口，通往若干子路口，这些岔路按顺序编号为 1, 2, 3, ...。整棵路网树的结构已知且固定。

路网结构如下：
{tree_structure}

系统已记录了发生事故的隐蔽路段 S，并记录了从枢纽到 S 的路径。这条路径用岔路编号序列表示，例如 (2, 1, 3) 表示从枢纽出发，选第 2 个岔路，再选它的第 1 个岔路，再选它的第 3 个岔路。

同时，道路监测系统设定了一个秘密的代号映射 f，它将所有可能的岔路编号（1, 2, 3, ...）一一对应到一组特征代号（如字母 A, B, C, ...）。这个映射在整个路网中保持一致。另外，系统定义了一个特殊代号 END，表示已经到达事故终点。

你的目标是：
1. 推断出从枢纽到事故路段 S 的完整路径（用岔路编号序列表示）。
2. 推断出在追踪过程中出现的所有特征代号到岔路编号的映射关系（包括 END 代号）。

你可以进行以下操作：

**无人机探路查询**：
提交一个岔路编号序列，从枢纽节点开始依次选择路口。例如 (1, 2) 表示先选枢纽的第 1 个岔路，再选它的第 2 个岔路。注意每一步的岔路编号必须在当前路口的有效范围内。

我会返回：
- 如果你的追踪路径与事故路径完全一致，返回"到达：成功"。
- 否则，我会告诉你：
  - 共同步数（你的路径与事故路径有多少步是吻合的）
  - 提示符号（一个加密后的特征代号，表示下一步正确的岔路编号；如果已经到达事故深度，则返回 END）

**提交最终报告**：
当你收集足够信息后，需要同时提交两项内容：
1. 事故路径的完整岔路编号序列
2. 所有历史反馈中出现过的特征代号到岔路编号的映射关系（必须包含 END 表示终点）

只有当路径和映射都正确时，任务才算成功。

**无人机探路查询**（提交岔路编号序列，用逗号分隔）：
<query_path>1,2,3</query_path>

**提交最终报告**（同时提交路径和映射）：
<answer>path=1,2,3; mapping=A->1,B->2,C->3,END->终点</answer>

注意：
- 路径用逗号分隔的岔路编号表示
- 映射用"特征代号->岔路编号"的格式，多个映射用逗号分隔
- END 必须映射到"终点"
- 请尽可能用最少的探路次数完成排查
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's conduct a "Traffic Network Incident Tracking" task. Here are the rules:

The urban traffic network is modeled as a rooted tree, with the root node (transportation hub) numbered 1. Each non-leaf node represents an intersection leading to several branch roads, which are numbered in order as 1, 2, 3, ... The structure of the entire network tree is known and fixed.

The network structure is as follows:
{tree_structure}

The system has secretly recorded an incident road segment S, and the path from the hub to S. This path is represented as a sequence of branch numbers, e.g., (2, 1, 3) means starting from the hub, taking the 2nd branch, then its 1st branch, then its 3rd branch.

Meanwhile, the road monitoring system has set up a secret code mapping f, which creates a one-to-one correspondence between all possible branch numbers (1, 2, 3, ...) and a set of feature codes (such as letters A, B, C, ...). This mapping remains consistent throughout the entire network. Furthermore, the system has defined a special code END, indicating that the incident endpoint has been reached.

Your goals are:
1. Infer the complete path from the hub to incident segment S (represented as a sequence of branch numbers).
2. Infer the mapping from all feature codes that appeared during the tracking to their corresponding branch numbers (including the END code).

You can perform the following operations:

**Drone Path Query**:
Submit a sequence of branch numbers, starting from the hub node and selecting intersections step by step. For example, (1, 2) means first selecting the 1st branch of the hub, then its 2nd branch. Note that each step's branch number must be within the valid range of the current intersection.

I will return:
- If your tracking path exactly matches the incident path, return "Reached: Success".
- Otherwise, I will tell you:
  - Common steps (how many steps your path shares with the incident path)
  - Hint symbol (an encrypted feature code representing the correct branch number for the next step; if already at the incident depth, return END)

**Submit Final Report**:
When you have gathered enough information, you need to submit two items simultaneously:
1. The complete branch number sequence of the incident path
2. The mapping from all feature codes that appeared in historical feedback to their branch numbers (must include END representing the endpoint)

The task succeeds only when both the path and mapping are correct.

**Drone Path Query** (submit branch number sequence, comma-separated):
<query_path>1,2,3</query_path>

**Submit Final Report** (submit both path and mapping):
<answer>path=1,2,3; mapping=A->1,B->2,C->3,END->endpoint</answer>

Notes:
- Path is represented by comma-separated branch numbers
- Mapping uses "feature code->branch number" format, multiple mappings separated by commas
- END must map to "endpoint"
- Please complete the inspection with as few queries as possible
"""

    contextualized_rule_zh_2 = """\
我们现在来进行一项“临床决策树病因确诊”任务，规则如下：

疾病排查流程被建模为一棵有根树，根节点（初始症状）编号为 1。每个非叶节点代表一个医疗诊断阶段，拥有若干排查测试选项，这些选项按顺序编号为 1, 2, 3, ...。整个决策树的结构已知且固定。

决策树结构如下：
{tree_structure}

系统已记录了一个罕见病症节点 S，并记录了从初始症状到 S 的确诊路径。这条路径用测试选项序列表示，例如 (2, 1, 3) 表示从初始症状出发，选第 2 个测试，再选其分支下的第 1 个测试，再选第 3 个测试。

同时，医疗系统设定了一个秘密的编码映射 f，它将所有可能的测试选项序号（1, 2, 3, ...）一一对应到一组临床生物标志物代码（如字母 A, B, C, ...）。这个映射在整个决策树中保持一致。另外，系统定义了一个特殊代码 END，表示已经确诊到达目标节点。

你的目标是：
1. 推断出从初始症状到确诊节点 S 的完整路径（用测试选项序列表示）。
2. 推断出在诊断过程中出现的所有生物标志物代码到测试选项序号的映射关系（包括 END 代码）。

你可以进行以下操作：

**临床排查查询**：
提交一个测试选项序列，从初始节点开始依次选择测试。例如 (1, 2) 表示先选初始的第 1 个测试，再选其分支的第 2 个测试。注意每一步的测试序号必须在当前节点的有效范围内。

我会返回：
- 如果你的排查路径与确诊路径完全一致，返回"到达：成功"。
- 否则，我会告诉你：
  - 共同步数（你的排查路径与确诊路径有多少步是一致的）
  - 提示符号（一个加密后的生物标志物代码，表示下一步正确的测试选项；如果已经到达确诊深度，则返回 END）

**提交最终诊断报告**：
当你收集足够临床信息后，需要同时提交两项内容：
1. 确诊路径的完整测试选项序列
2. 所有历史反馈中出现过的代码到测试选项序号的映射关系（必须包含 END 表示终点）

只有当路径和映射都正确时，诊断才算成功。

**临床排查查询**（提交测试选项序列，用逗号分隔）：
<query_path>1,2,3</query_path>

**提交最终诊断报告**（同时提交路径和映射）：
<answer>path=1,2,3; mapping=A->1,B->2,C->3,END->终点</answer>

注意：
- 路径用逗号分隔的测试选项序号表示
- 映射用"标志物代码->选项序号"的格式，多个映射用逗号分隔
- END 必须映射到"终点"
- 请尽可能用最少的排查次数完成确诊
"""

    contextualized_rule_en_2 = """\
[Medical/Healthcare Scenario]
Let's conduct a "Clinical Decision Tree Etiology Diagnosis" task. Here are the rules:

The disease screening process is modeled as a rooted tree, with the root node (initial symptom) numbered 1. Each non-leaf node represents a medical diagnostic stage with several screening test options, numbered in order as 1, 2, 3, ... The structure of the entire decision tree is known and fixed.

The decision tree structure is as follows:
{tree_structure}

The system has recorded a rare disease node S, and the diagnostic path from the initial symptom to S. This path is represented as a sequence of test options, e.g., (2, 1, 3) means starting from the initial symptom, choosing the 2nd test, then its 1st test branch, then the 3rd test.

Meanwhile, the medical system has set up a secret code mapping f, which creates a one-to-one correspondence between all possible test option indices (1, 2, 3, ...) and a set of clinical biomarker codes (such as letters A, B, C, ...). This mapping remains consistent throughout the entire decision tree. Furthermore, the system has defined a special code END, indicating that the target diagnostic endpoint has been reached.

Your goals are:
1. Infer the complete path from the initial symptom to the confirmed diagnosis node S (represented as a sequence of test option indices).
2. Infer the mapping from all biomarker codes that appeared during the diagnosis to their corresponding test option indices (including the END code).

You can perform the following operations:

**Clinical Screening Query**:
Submit a sequence of test option indices, starting from the initial node and selecting tests step by step. For example, (1, 2) means first selecting the 1st test of the initial node, then the 2nd test of its branch. Note that each step's test index must be within the valid range of the current node.

I will return:
- If your screening path exactly matches the diagnostic path, return "Reached: Success".
- Otherwise, I will tell you:
  - Common steps (how many steps your screening path shares with the diagnostic path)
  - Hint symbol (an encrypted biomarker code representing the correct test option for the next step; if already at the diagnostic depth, return END)

**Submit Final Diagnostic Report**:
When you have gathered enough clinical information, you need to submit two items simultaneously:
1. The complete test option index sequence of the diagnostic path
2. The mapping from all codes that appeared in historical feedback to their test option indices (must include END representing the endpoint)

The diagnosis succeeds only when both the path and mapping are correct.

**Clinical Screening Query** (submit test option sequence, comma-separated):
<query_path>1,2,3</query_path>

**Submit Final Diagnostic Report** (submit both path and mapping):
<answer>path=1,2,3; mapping=A->1,B->2,C->3,END->endpoint</answer>

Notes:
- Path is represented by comma-separated test option indices
- Mapping uses "biomarker code->test index" format, multiple mappings separated by commas
- END must map to "endpoint"
- Please complete the diagnosis with as few queries as possible
"""

    contextualized_rule_zh_3 = """\
我们现在来进行一项“学习路径薄弱点溯源”任务，规则如下：

知识图谱被建模为一棵有根树，根节点（基础概念）编号为 1。每个非叶节点代表一个知识领域，拥有若干子知识点分支，这些分支按顺序编号为 1, 2, 3, ...。整棵图谱树的结构已知且固定。

知识树结构如下：
{tree_structure}

系统已评估出学生的核心薄弱知识节点 S，并记录了从基础概念到 S 的学习路径。这条路径用分支序号序列表示，例如 (2, 1, 3) 表示从基础概念出发，选第 2 个分支，再选它的第 1 个分支，再选它的第 3 个分支。

同时，教育系统设定了一个秘密的评估映射 f，它将所有可能的分支序号（1, 2, 3, ...）一一对应到一组考核代号（如字母 A, B, C, ...）。这个映射在整棵树中保持一致。另外，系统定义了一个特殊代号 END，表示已经到达薄弱点终点。

你的目标是：
1. 推断出从基础概念到薄弱节点 S 的完整学习路径（用分支序号序列表示）。
2. 推断出在溯源过程中出现的所有考核代号到分支序号的映射关系（包括 END 代号）。

你可以进行以下操作：

**学习路径测评查询**：
提交一个分支序号序列，从基础节点开始依次选择分支。例如 (1, 2) 表示先选基础概念的第 1 个分支，再选它的第 2 个分支。注意每一步的分支序号必须在当前节点的有效范围内。

我会返回：
- 如果你的测评路径与薄弱点路径完全一致，返回"到达：成功"。
- 否则，我会告诉你：
  - 共同步数（你的路径与薄弱点路径有多少步是相同的）
  - 提示符号（一个加密后的考核代号，表示下一步正确的分支序号；如果已经到达薄弱点深度，则返回 END）

**提交最终分析报告**：
当你收集足够评估信息后，需要同时提交两项内容：
1. 薄弱点路径的完整分支序号序列
2. 所有历史反馈中出现过的考核代号到分支序号的映射关系（必须包含 END 表示终点）

只有当路径和映射都正确时，溯源才算成功。

**学习路径测评查询**（提交分支序号序列，用逗号分隔）：
<query_path>1,2,3</query_path>

**提交最终分析报告**（同时提交路径和映射）：
<answer>path=1,2,3; mapping=A->1,B->2,C->3,END->终点</answer>

注意：
- 路径用逗号分隔的分支序号表示
- 映射用"考核代号->分支序号"的格式，多个映射用逗号分隔
- END 必须映射到"终点"
- 请尽可能用最少的测评次数完成溯源
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a "Learning Path Weakness Tracing" task. Here are the rules:

The knowledge graph is modeled as a rooted tree, with the root node (basic concept) numbered 1. Each non-leaf node represents a knowledge domain with several sub-knowledge branches, numbered in order as 1, 2, 3, ... The structure of the entire graph tree is known and fixed.

The knowledge tree structure is as follows:
{tree_structure}

The system has evaluated a core weakness node S for the student, and recorded the learning path from the basic concept to S. This path is represented as a sequence of branch indices, e.g., (2, 1, 3) means starting from the basic concept, choosing the 2nd branch, then its 1st branch, then its 3rd branch.

Meanwhile, the educational system has set up a secret evaluation mapping f, which creates a one-to-one correspondence between all possible branch indices (1, 2, 3, ...) and a set of assessment codes (such as letters A, B, C, ...). This mapping remains consistent throughout the entire tree. Furthermore, the system has defined a special code END, indicating that the weakness endpoint has been reached.

Your goals are:
1. Infer the complete learning path from the basic concept to weakness node S (represented as a sequence of branch indices).
2. Infer the mapping from all assessment codes that appeared during the tracing to their corresponding branch indices (including the END code).

You can perform the following operations:

**Learning Path Assessment Query**:
Submit a sequence of branch indices, starting from the basic concept and selecting branches step by step. For example, (1, 2) means first selecting the 1st branch of the basic concept, then its 2nd branch. Note that each step's branch index must be within the valid range of the current node.

I will return:
- If your assessment path exactly matches the weakness path, return "Reached: Success".
- Otherwise, I will tell you:
  - Common steps (how many steps your path shares with the weakness path)
  - Hint symbol (an encrypted assessment code representing the correct branch index for the next step; if already at the weakness depth, return END)

**Submit Final Analysis Report**:
When you have gathered enough evaluation information, you need to submit two items simultaneously:
1. The complete branch index sequence of the weakness path
2. The mapping from all assessment codes that appeared in historical feedback to their branch indices (must include END representing the endpoint)

The tracing succeeds only when both the path and mapping are correct.

**Learning Path Assessment Query** (submit branch index sequence, comma-separated):
<query_path>1,2,3</query_path>

**Submit Final Analysis Report** (submit both path and mapping):
<answer>path=1,2,3; mapping=A->1,B->2,C->3,END->endpoint</answer>

Notes:
- Path is represented by comma-separated branch indices
- Mapping uses "assessment code->branch index" format, multiple mappings separated by commas
- END must map to "endpoint"
- Please complete the tracing with as few queries as possible
"""

    contextualized_rule_zh_4 = """\
我们现在来进行一项“精密设备故障链路排查”任务，规则如下：

设备的模块层级被建模为一棵有根树，根节点（设备主板）编号为 1。每个非叶节点代表一个组件，包含若干下级接口，这些接口按顺序编号为 1, 2, 3, ...。整棵设备树的结构已知且固定。

设备层级结构如下：
{tree_structure}

系统已检测到一个核心故障模块 S，并记录了从主板到 S 的信号链路。这条链路用接口编号序列表示，例如 (2, 1, 3) 表示从主板出发，选第 2 个接口，再选它的第 1 个下级接口，再选它的第 3 个下级接口。

同时，工业检测系统设定了一个秘密的协议映射 f，它将所有可能的接口编号（1, 2, 3, ...）一一对应到一组信号特征码（如字母 A, B, C, ...）。这个映射在整个设备树中保持一致。另外，系统定义了一个特殊特征码 END，表示已经到达故障终点。

你的目标是：
1. 推断出从主板到故障模块 S 的完整链路路径（用接口编号序列表示）。
2. 推断出在排查过程中出现的所有信号特征码到接口编号的映射关系（包括 END 特征码）。

你可以进行以下操作：

**注入检测信号查询**：
提交一个接口编号序列，从主板开始依次穿透模块。例如 (1, 2) 表示先测主板的第 1 个接口，再测它的第 2 个下级接口。注意每一步的接口编号必须在当前组件的有效范围内。

我会返回：
- 如果你的测试链路与故障链路完全一致，返回"到达：成功"。
- 否则，我会告诉你：
  - 共同步数（你的链路与故障链路有多少级是匹配的）
  - 提示符号（一个加密后的信号特征码，表示下一级正确的接口编号；如果已经穿透至故障模块深度，则返回 END）

**提交最终诊断报告**：
当你收集足够检测信息后，需要同时提交两项内容：
1. 故障链路的完整接口编号序列
2. 所有历史反馈中出现过的信号特征码到接口编号的映射关系（必须包含 END 表示终点）

只有当链路和映射都正确时，排查才算成功。

**注入检测信号查询**（提交接口编号序列，用逗号分隔）：
<query_path>1,2,3</query_path>

**提交最终诊断报告**（同时提交路径和映射）：
<answer>path=1,2,3; mapping=A->1,B->2,C->3,END->终点</answer>

注意：
- 链路用逗号分隔的接口编号表示
- 映射用"特征码->接口编号"的格式，多个映射用逗号分隔
- END 必须映射到"终点"
- 请尽可能用最少的检测次数完成排查
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's conduct a "Precision Equipment Fault Link Troubleshooting" task. Here are the rules:

The module hierarchy of the equipment is modeled as a rooted tree, with the root node (mainboard) numbered 1. Each non-leaf node represents a component containing several lower-level interfaces, numbered in order as 1, 2, 3, ... The structure of the entire equipment tree is known and fixed.

The equipment hierarchy structure is as follows:
{tree_structure}

The system has detected a core faulty module S, and recorded the signal link from the mainboard to S. This link is represented as a sequence of interface numbers, e.g., (2, 1, 3) means starting from the mainboard, selecting the 2nd interface, then its 1st lower-level interface, then its 3rd lower-level interface.

Meanwhile, the industrial detection system has set up a secret protocol mapping f, which creates a one-to-one correspondence between all possible interface numbers (1, 2, 3, ...) and a set of signal feature codes (such as letters A, B, C, ...). This mapping remains consistent throughout the entire equipment tree. Furthermore, the system has defined a special code END, indicating that the fault endpoint has been reached.

Your goals are:
1. Infer the complete link path from the mainboard to faulty module S (represented as a sequence of interface numbers).
2. Infer the mapping from all signal feature codes that appeared during the troubleshooting to their corresponding interface numbers (including the END code).

You can perform the following operations:

**Injected Signal Detection Query**:
Submit a sequence of interface numbers, penetrating modules step by step starting from the mainboard. For example, (1, 2) means first testing the 1st interface of the mainboard, then its 2nd lower-level interface. Note that each step's interface number must be within the valid range of the current component.

I will return:
- If your testing link exactly matches the fault link, return "Reached: Success".
- Otherwise, I will tell you:
  - Common steps (how many stages your link shares with the fault link)
  - Hint symbol (an encrypted signal feature code representing the correct interface number for the next stage; if already penetrated to the fault module depth, return END)

**Submit Final Diagnostic Report**:
When you have gathered enough detection information, you need to submit two items simultaneously:
1. The complete interface number sequence of the fault link
2. The mapping from all signal feature codes that appeared in historical feedback to their interface numbers (must include END representing the endpoint)

The troubleshooting succeeds only when both the link and mapping are correct.

**Injected Signal Detection Query** (submit interface number sequence, comma-separated):
<query_path>1,2,3</query_path>

**Submit Final Diagnostic Report** (submit both path and mapping):
<answer>path=1,2,3; mapping=A->1,B->2,C->3,END->endpoint</answer>

Notes:
- Link is represented by comma-separated interface numbers
- Mapping uses "feature code->interface number" format, multiple mappings separated by commas
- END must map to "endpoint"
- Please complete the troubleshooting with as few detection queries as possible
"""

    contextualized_rule_zh_5 = """\
我们现在来进行一项“司法裁判证据链推演”任务，规则如下：

案件判决逻辑被建模为一棵有根树，根节点（基本案由）编号为 1。每个非叶节点代表一个法律要件，包含若干判定条件分支，这些条件按顺序编号为 1, 2, 3, ...。整棵推理树的结构已知且固定。

裁判逻辑树结构如下：
{tree_structure}

系统已确立了最终的裁判依据节点 S，并记录了从基本案由到 S 的推演路径。这条路径用条件序号序列表示，例如 (2, 1, 3) 表示从案由出发，认定第 2 个条件，再认定它的第 1 个下级条件，再认定它的第 3 个下级条件。

同时，司法卷宗系统设定了一个秘密的索引映射 f，它将所有可能的条件序号（1, 2, 3, ...）一一对应到一组法典索引码（如字母 A, B, C, ...）。这个映射在整棵推演树中保持一致。另外，系统定义了一个特殊索引码 END，表示已经得出最终裁决结果。

你的目标是：
1. 推断出从基本案由到裁决节点 S 的完整推演路径（用条件序号序列表示）。
2. 推断出在推演过程中出现的所有法典索引码到条件序号的映射关系（包括 END 索引码）。

你可以进行以下操作：

**庭审逻辑推演查询**：
提交一个条件序号序列，从基本案由开始依次认定要件。例如 (1, 2) 表示先认定第 1 个条件，再认定它的第 2 个下级条件。注意每一步的条件序号必须在当前要件的有效范围内。

我会返回：
- 如果你的推演路径与实际裁决路径完全一致，返回"到达：成功"。
- 否则，我会告诉你：
  - 共同步数（你的逻辑与实际裁决逻辑有多少步是一致的）
  - 提示符号（一个加密后的法典索引码，表示下一步正确的条件序号；如果已经到达裁决深度，则返回 END）

**提交最终判决书**：
当你收集足够卷宗信息后，需要同时提交两项内容：
1. 裁决路径的完整条件序号序列
2. 所有历史反馈中出现过的法典索引码到条件序号的映射关系（必须包含 END 表示终点）

只有当路径和映射都正确时，推演才算成功。

**庭审逻辑推演查询**（提交条件序号序列，用逗号分隔）：
<query_path>1,2,3</query_path>

**提交最终判决书**（同时提交路径和映射）：
<answer>path=1,2,3; mapping=A->1,B->2,C->3,END->终点</answer>

注意：
- 路径用逗号分隔的条件序号表示
- 映射用"索引码->条件序号"的格式，多个映射用逗号分隔
- END 必须映射到"终点"
- 请尽可能用最少的推演次数完成任务
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct a "Judicial Adjudication Evidence Chain Deduction" task. Here are the rules:

The logic of the case judgment is modeled as a rooted tree, with the root node (basic cause of action) numbered 1. Each non-leaf node represents a legal requisite containing several judging condition branches, numbered in order as 1, 2, 3, ... The structure of the entire deduction tree is known and fixed.

The logic tree of adjudication is as follows:
{tree_structure}

The system has established the final adjudication basis node S, and recorded the deduction path from the basic cause of action to S. This path is represented as a sequence of condition indices, e.g., (2, 1, 3) means starting from the cause of action, affirming the 2nd condition, then its 1st lower-level condition, then its 3rd lower-level condition.

Meanwhile, the judicial dossier system has set up a secret index mapping f, which creates a one-to-one correspondence between all possible condition indices (1, 2, 3, ...) and a set of legal index codes (such as letters A, B, C, ...). This mapping remains consistent throughout the entire deduction tree. Furthermore, the system has defined a special code END, indicating that the final adjudication result has been reached.

Your goals are:
1. Infer the complete deduction path from the basic cause of action to adjudication node S (represented as a sequence of condition indices).
2. Infer the mapping from all legal index codes that appeared during the deduction to their corresponding condition indices (including the END code).

You can perform the following operations:

**Trial Logic Deduction Query**:
Submit a sequence of condition indices, affirming requisites step by step starting from the basic cause of action. For example, (1, 2) means first affirming the 1st condition, then its 2nd lower-level condition. Note that each step's condition index must be within the valid range of the current requisite.

I will return:
- If your deduction path exactly matches the actual adjudication path, return "Reached: Success".
- Otherwise, I will tell you:
  - Common steps (how many steps your logic shares with the actual adjudication logic)
  - Hint symbol (an encrypted legal index code representing the correct condition index for the next step; if already at the adjudication depth, return END)

**Submit Final Judgment**:
When you have gathered enough dossier information, you need to submit two items simultaneously:
1. The complete condition index sequence of the adjudication path
2. The mapping from all legal index codes that appeared in historical feedback to their condition indices (must include END representing the endpoint)

The deduction succeeds only when both the path and mapping are correct.

**Trial Logic Deduction Query** (submit condition index sequence, comma-separated):
<query_path>1,2,3</query_path>

**Submit Final Judgment** (submit both path and mapping):
<answer>path=1,2,3; mapping=A->1,B->2,C->3,END->endpoint</answer>

Notes:
- Path is represented by comma-separated condition indices
- Mapping uses "index code->condition index" format, multiple mappings separated by commas
- END must map to "endpoint"
- Please complete the deduction with as few queries as possible
"""

    tags = ["answer", "query_path"]
    
    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "tree": {
                    "1": ["2", "3"],
                    "2": ["4", "5"],
                    "3": ["6", "7"],
                    "4": [],
                    "5": [],
                    "6": [],
                    "7": [],
                },
                "target_path": [2, 1],
                "max_degree": 2,
                "symbol_mapping": {1: "A", 2: "B"},
                "end_symbol_zh": "终点",
                "end_symbol_en": "endpoint",
            },
            2: {
                "tree": {
                    "1": ["2", "3"],
                    "2": ["4", "5", "6"],
                    "3": ["7", "8"],
                    "4": [],
                    "5": [],
                    "6": [],
                    "7": [],
                    "8": [],
                },
                "target_path": [1, 3],
                "max_degree": 3,
                "symbol_mapping": {1: "X", 2: "Y", 3: "Z"},
                "end_symbol_zh": "终点",
                "end_symbol_en": "endpoint",
            },
            3: {
                "tree": {
                    "1": ["2", "3", "4"],
                    "2": ["5", "6", "7"],
                    "3": ["8", "9", "10"],
                    "4": ["11", "12", "13"],
                    "5": [],
                    "6": [],
                    "7": [],
                    "8": [],
                    "9": [],
                    "10": [],
                    "11": [],
                    "12": [],
                    "13": [],
                },
                "target_path": [3, 2],
                "max_degree": 3,
                "symbol_mapping": {1: "P", 2: "Q", 3: "R"},
                "end_symbol_zh": "终点",
                "end_symbol_en": "endpoint",
            },
            4: {
                "tree": {
                    "1": ["2", "3"],
                    "2": ["4", "5", "6"],
                    "3": ["7", "8"],
                    "4": ["9", "10"],
                    "5": ["11", "12", "13"],
                    "6": [],
                    "7": [],
                    "8": ["14", "15"],
                    "9": [],
                    "10": [],
                    "11": [],
                    "12": [],
                    "13": [],
                    "14": [],
                    "15": [],
                },
                "target_path": [1, 2, 3],
                "max_degree": 3,
                "symbol_mapping": {1: "M", 2: "N", 3: "O"},
                "end_symbol_zh": "终点",
                "end_symbol_en": "endpoint",
            },
            5: {
                "tree": {
                    "1": ["2", "3", "4"],
                    "2": ["5", "6", "7", "8"],
                    "3": ["9", "10", "11"],
                    "4": ["12", "13", "14"],
                    "5": ["15", "16", "17"],
                    "6": ["18", "19", "20"],
                    "7": [],
                    "8": [],
                    "9": ["21", "22"],
                    "10": [],
                    "11": [],
                    "12": [],
                    "13": [],
                    "14": [],
                    "15": ["23", "24", "25"],
                    "16": [],
                    "17": [],
                    "18": [],
                    "19": [],
                    "20": [],
                    "21": [],
                    "22": [],
                    "23": [],
                    "24": [],
                    "25": [],
                },
                "target_path": [1, 1, 1, 2],
                "max_degree": 4,
                "symbol_mapping": {1: "α", 2: "β", 3: "γ", 4: "δ"},
                "end_symbol_zh": "终点",
                "end_symbol_en": "endpoint",
            },
        },
        "en": {
            1: {
                "tree": {
                    "1": ["2", "3"],
                    "2": ["4", "5"],
                    "3": ["6", "7"],
                    "4": [],
                    "5": [],
                    "6": [],
                    "7": [],
                },
                "target_path": [2, 1],
                "max_degree": 2,
                "symbol_mapping": {1: "A", 2: "B"},
                "end_symbol_zh": "终点",
                "end_symbol_en": "endpoint",
            },
            2: {
                "tree": {
                    "1": ["2", "3"],
                    "2": ["4", "5", "6"],
                    "3": ["7", "8"],
                    "4": [],
                    "5": [],
                    "6": [],
                    "7": [],
                    "8": [],
                },
                "target_path": [1, 3],
                "max_degree": 3,
                "symbol_mapping": {1: "X", 2: "Y", 3: "Z"},
                "end_symbol_zh": "终点",
                "end_symbol_en": "endpoint",
            },
            3: {
                "tree": {
                    "1": ["2", "3", "4"],
                    "2": ["5", "6", "7"],
                    "3": ["8", "9", "10"],
                    "4": ["11", "12", "13"],
                    "5": [],
                    "6": [],
                    "7": [],
                    "8": [],
                    "9": [],
                    "10": [],
                    "11": [],
                    "12": [],
                    "13": [],
                },
                "target_path": [3, 2],
                "max_degree": 3,
                "symbol_mapping": {1: "P", 2: "Q", 3: "R"},
                "end_symbol_zh": "终点",
                "end_symbol_en": "endpoint",
            },
            4: {
                "tree": {
                    "1": ["2", "3"],
                    "2": ["4", "5", "6"],
                    "3": ["7", "8"],
                    "4": ["9", "10"],
                    "5": ["11", "12", "13"],
                    "6": [],
                    "7": [],
                    "8": ["14", "15"],
                    "9": [],
                    "10": [],
                    "11": [],
                    "12": [],
                    "13": [],
                    "14": [],
                    "15": [],
                },
                "target_path": [1, 2, 3],
                "max_degree": 3,
                "symbol_mapping": {1: "M", 2: "N", 3: "O"},
                "end_symbol_zh": "终点",
                "end_symbol_en": "endpoint",
            },
            5: {
                "tree": {
                    "1": ["2", "3", "4"],
                    "2": ["5", "6", "7", "8"],
                    "3": ["9", "10", "11"],
                    "4": ["12", "13", "14"],
                    "5": ["15", "16", "17"],
                    "6": ["18", "19", "20"],
                    "7": [],
                    "8": [],
                    "9": ["21", "22"],
                    "10": [],
                    "11": [],
                    "12": [],
                    "13": [],
                    "14": [],
                    "15": ["23", "24", "25"],
                    "16": [],
                    "17": [],
                    "18": [],
                    "19": [],
                    "20": [],
                    "21": [],
                    "22": [],
                    "23": [],
                    "24": [],
                    "25": [],
                },
                "target_path": [1, 1, 1, 2],
                "max_degree": 4,
                "symbol_mapping": {1: "α", 2: "β", 3: "γ", 4: "δ"},
                "end_symbol_zh": "终点",
                "end_symbol_en": "endpoint",
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
        
        self.tree = cfg["tree"]
        self.target_path = cfg["target_path"]
        self.max_degree = cfg["max_degree"]
        self.symbol_mapping = cfg["symbol_mapping"]
        self.end_symbol = cfg["end_symbol_zh"] if lang == "zh" else cfg["end_symbol_en"]
        
        self.observed_symbols = set()
        
        tree_desc = self._generate_tree_description()
        self._game_info["tree_structure"] = tree_desc

    def _generate_tree_description(self):
        lines = []
        if self.config.language == "zh":
            lines.append("节点及其子节点：")
            for node, children in sorted(self.tree.items(), key=lambda x: int(x[0])):
                if children:
                    lines.append(f"  节点 {node} 的子节点：{', '.join(children)}")
                else:
                    lines.append(f"  节点 {node} 是叶节点")
        else:
            lines.append("Nodes and their children:")
            for node, children in sorted(self.tree.items(), key=lambda x: int(x[0])):
                if children:
                    lines.append(f"  Node {node} has children: {', '.join(children)}")
                else:
                    lines.append(f"  Node {node} is a leaf node")
        return "\n".join(lines)

    def _compute_lcp(self, path1, path2):
        lcp = 0
        for i in range(min(len(path1), len(path2))):
            if path1[i] == path2[i]:
                lcp += 1
            else:
                break
        return lcp

    def _validate_path(self, path):
        current = "1"
        for step_idx, child_idx in enumerate(path):
            children = self.tree.get(current, [])
            if not children:
                return False, f"Node {current} is a leaf node, cannot go further at step {step_idx + 1}"
            if child_idx < 1 or child_idx > len(children):
                return False, f"Step {step_idx + 1}: child index {child_idx} out of range (node {current} has {len(children)} children)"
            current = children[child_idx - 1]
        return True, current

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        try:
            parts = raw_ans.split(";")
            path_part = None
            mapping_part = None
            
            for part in parts:
                part = part.strip()
                if part.startswith("path="):
                    path_part = part[5:].strip()
                elif part.startswith("mapping="):
                    mapping_part = part[8:].strip()
            
            if not path_part or not mapping_part:
                return False
            
            try:
                submitted_path = [int(x.strip()) for x in path_part.split(",")]
            except:
                return False
            
            submitted_mapping = {}
            try:
                mappings = [m.strip() for m in mapping_part.split(",")]
                for m in mappings:
                    if "->" not in m:
                        return False
                    symbol, target = m.split("->", 1)
                    symbol = symbol.strip()
                    target = target.strip()
                    submitted_mapping[symbol] = target
            except:
                return False
            
            if submitted_path != self.target_path:
                return False
            
            if "END" not in submitted_mapping:
                return False
            if submitted_mapping["END"] != self.end_symbol:
                return False
            
            for symbol in self.observed_symbols:
                if symbol == "END":
                    continue
                if symbol not in submitted_mapping:
                    return False
                correct_idx = None
                for idx, sym in self.symbol_mapping.items():
                    if sym == symbol:
                        correct_idx = idx
                        break
                if correct_idx is None:
                    return False
                try:
                    submitted_idx = int(submitted_mapping[symbol])
                    if submitted_idx != correct_idx:
                        return False
                except:
                    return False
            
            for symbol, target in submitted_mapping.items():
                if symbol == "END":
                    continue
                found = False
                for idx, sym in self.symbol_mapping.items():
                    if sym == symbol:
                        found = True
                        try:
                            if int(target) != idx:
                                return False
                        except:
                            return False
                        break
                if not found:
                    return False
            
            return True
            
        except Exception as e:
            return False

    def _cf_core_produce(self, parsed_info):
        if "query_path" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        raw_path = parsed_info["query_path"].strip()
        
        try:
            if not raw_path:
                path = []
            else:
                path = [int(x.strip()) for x in raw_path.split(",")]
        except:
            if self.config.language == "zh":
                return "错误：路径格式无效，请使用逗号分隔的数字。"
            else:
                return "Error: Invalid path format. Please use comma-separated numbers."
        
        valid, result = self._validate_path(path)
        if not valid:
            if self.config.language == "zh":
                return f"错误：{result}"
            else:
                return f"Error: {result}"
        
        if path == self.target_path:
            if self.config.language == "zh":
                return "到达：成功"
            else:
                return "Reached: Success"
        
        lcp = self._compute_lcp(path, self.target_path)
        
        if lcp < len(self.target_path):
            next_correct_idx = self.target_path[lcp]
            hint_symbol = self.symbol_mapping[next_correct_idx]
            self.observed_symbols.add(hint_symbol)
        else:
            hint_symbol = "END"
            self.observed_symbols.add("END")
        
        if self.config.language == "zh":
            return f"共同步数：{lcp}；提示符号：{hint_symbol}"
        else:
            return f"Common steps: {lcp}; Hint symbol: {hint_symbol}"

    def _cf_make_wrong(self, correct):
        if self.config.language == "zh":
            match = re.search(r'共同步数：(\d+)', correct)
            if match:
                old_val = int(match.group(1))
                new_val = old_val + 1
                return correct.replace(f'共同步数：{old_val}', f'共同步数：{new_val}')
            match = re.search(r'提示符号：(\S+)', correct)
            if match:
                old_sym = match.group(1)
                all_syms = list(self.symbol_mapping.values()) + ["END"]
                for s in all_syms:
                    if s != old_sym:
                        return correct.replace(f'提示符号：{old_sym}', f'提示符号：{s}')
        else:
            match = re.search(r'Common steps: (\d+)', correct)
            if match:
                old_val = int(match.group(1))
                new_val = old_val + 1
                return correct.replace(f'Common steps: {old_val}', f'Common steps: {new_val}')
            match = re.search(r'Hint symbol: (\S+)', correct)
            if match:
                old_sym = match.group(1)
                all_syms = list(self.symbol_mapping.values()) + ["END"]
                for s in all_syms:
                    if s != old_sym:
                        return correct.replace(f'Hint symbol: {old_sym}', f'Hint symbol: {s}')
        
        return correct + "_WRONG"

    def get_all_possible_queries(self):
        results = []
        queue = [("1", [])]
        
        while queue:
            curr_node, curr_path = queue.pop(0)
            
            children = self.tree.get(curr_node, [])
            
            for i, child_node in enumerate(children):
                child_idx = i + 1
                new_path = curr_path + [child_idx]
                
                query_str = "<query_path>" + ",".join(map(str, new_path)) + "</query_path>"
                
                response = ""
                
                if new_path == self.target_path:
                    if self.config.language == "zh":
                        response = "到达：成功"
                    else:
                        response = "Reached: Success"
                else:
                    lcp = 0
                    min_len = min(len(new_path), len(self.target_path))
                    for k in range(min_len):
                        if new_path[k] == self.target_path[k]:
                            lcp += 1
                        else:
                            break
                    
                    if lcp < len(self.target_path):
                        next_correct_idx = self.target_path[lcp]
                        hint_symbol = self.symbol_mapping[next_correct_idx]
                    else:
                        hint_symbol = "END"
                    
                    if self.config.language == "zh":
                        response = f"共同步数：{lcp}；提示符号：{hint_symbol}"
                    else:
                        response = f"Common steps: {lcp}; Hint symbol: {hint_symbol}"
                
                results.append({
                    "query": query_str,
                    "answer": response
                })
                
                queue.append((child_node, new_path))
        
        return results