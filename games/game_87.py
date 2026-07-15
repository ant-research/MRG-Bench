import math
import re
from collections import deque
from typing import Dict, List, Set, Tuple

from .base import Game

class TreeTraversalDeductionGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"树遍历推理"游戏，规则如下：

游戏设定了一棵包含 {n} 个节点的有根树，每个节点用唯一的大写字母字符串命名（如 A, ROOT, EA, NODE3 等）。

树的结构信息：
- 根节点：{root}
- 树结构：{tree_structure}

字符串字典序规则：按 A 小于 B 小于 ... 小于 Z 的标准字典序逐字符比较；若一字符串为另一字符串的前缀，则较短者更小（例如 AB 小于 ABA）。

隐藏机制：
我已经秘密选择了一种遍历策略和兄弟访问规则，生成了这棵树上所有节点的一个全序（每个节点恰好出现一次）。遍历策略包括：
1. 深度优先先序遍历
2. 深度优先后序遍历  
3. 广度优先层序遍历

同时，对于每个节点的子节点，我选择了以下访问顺序之一：
- 按节点名字典序升序访问
- 按节点名字典序降序访问

这些选择在整个游戏过程中保持固定且全局一致。

你的任务：
推断出完整的节点遍历顺序。你可以通过比较查询来获取信息，但查询次数有限。

查询格式：
使用以下 XML 格式进行比较查询（询问两个节点在遍历顺序中哪个更早）：

<query_compare>X,Y</query_compare>

其中 X 和 Y 是不同的节点名。我会回答在遍历顺序中更早出现的节点。

提交答案格式：
当你准备好提交最终答案时，请按遍历顺序列出所有节点（用逗号分隔）：

<answer>V1,V2,V3,...,V{n}</answer>

注意：
- 请尽可能少地使用查询次数
- 节点必须全部出现且每个节点恰好出现一次
- 答案必须与隐藏的遍历顺序完全一致才算成功
"""

    game_rule_en = """\
Let's play a "Tree Traversal Deduction" game. Here are the rules:

The game has a rooted tree with {n} nodes, each named with a unique uppercase letter string (such as A, ROOT, EA, NODE3, etc.).

Tree structure information:
- Root node: {root}
- Tree structure: {tree_structure}

Lexicographic order rule: Standard dictionary order by A less than B less than ... less than Z, comparing character by character; if one string is a prefix of another, the shorter one is smaller (e.g., AB less than ABA).

Hidden mechanism:
I have secretly chosen a traversal strategy and sibling visiting rule, generating a total order of all nodes in the tree (each node appears exactly once). The traversal strategies include:
1. Depth-first preorder traversal
2. Depth-first postorder traversal
3. Breadth-first level-order traversal

Meanwhile, for each node's children, I chose one of the following visiting orders:
- Visit children in ascending lexicographic order by name
- Visit children in descending lexicographic order by name

These choices remain fixed and globally consistent throughout the game.

Your task:
Deduce the complete node traversal order. You can obtain information through comparison queries, but the number of queries is limited.

Query format:
Use the following XML format for comparison queries (asking which of two nodes appears earlier in the traversal order):

<query_compare>X,Y</query_compare>

Where X and Y are different node names. I will answer which node appears earlier in the traversal order.

Answer submission format:
When you are ready to submit your final answer, list all nodes in traversal order (comma-separated):

<answer>V1,V2,V3,...,V{n}</answer>

Note:
- Please use as few queries as possible
- All nodes must appear exactly once
- The answer must match the hidden traversal order exactly to succeed
"""

    contextualized_rule_zh_1 = """\
欢迎使用智能交通网络调度评估系统。我们来模拟一个"物流分发网络调度"任务，规则如下：

系统设定了一棵包含 {n} 个站点的树形调度网络，每个站点用唯一的大写字母字符串代码命名（如 A, ROOT, EA, NODE3 等）。

网络结构信息：
- 核心枢纽节点：{root}
- 线路结构：{tree_structure}

代码字典序规则：按 A 小于 B 小于 ... 小于 Z 的标准字典序逐字符比较；若一字符串为另一字符串的前缀，则较短者更小（例如 AB 小于 ABA）。

隐藏机制：
调度中心秘密选择了一种巡检策略和分支站点访问规则，生成了这棵树上所有站点的一个完整巡检顺序（每个站点恰好出现一次）。巡检策略包括：
1. 深度优先先序巡检
2. 深度优先后序巡检  
3. 广度优先层序巡检

同时，对于每个站点的下级接驳站点，调度中心选择了以下访问顺序之一：
- 按站点代码字典序升序访问
- 按站点代码字典序降序访问

这些选择在整个调度评估过程中保持固定且全局一致。

你的任务：
推断出完整的站点巡检顺序。你可以通过接口比较查询来获取调度信息，但查询配额有限。

查询格式：
使用以下 XML 格式进行比较查询（询问两个站点在巡检顺序中哪个更早被访问）：

<query_compare>X,Y</query_compare>

其中 X 和 Y 是不同的站点代码。调度系统会返回在巡检顺序中更早被访问的站点。

提交答案格式：
当你准备好提交最终调度预案时，请按巡检顺序列出所有站点（用逗号分隔）：

<answer>V1,V2,V3,...,V{n}</answer>

注意：
- 请尽可能少地消耗查询配额
- 站点必须全部出现且每个站点恰好出现一次
- 提交的预案必须与调度中心隐藏的巡检顺序完全一致才算验证通过
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the Intelligent Transit Network Dispatch Evaluation System. Let's simulate a "Logistics Distribution Network Dispatch" task. Here are the rules:

The system has set up a tree-structured dispatch network with {n} stations, each identified by a unique uppercase letter string code (e.g., A, ROOT, EA, NODE3).

Network structure information:
- Core hub node: {root}
- Route structure: {tree_structure}

Lexicographic order rule: Standard dictionary order by A less than B less than ... less than Z, comparing character by character; if one string is a prefix of another, the shorter one is smaller (e.g., AB is less than ABA).

Hidden mechanism:
The dispatch center has secretly selected an inspection strategy and a branch station visiting rule, generating a complete inspection sequence for all stations in this network (each station appears exactly once). The inspection strategies include:
1. Depth-first preorder inspection
2. Depth-first postorder inspection
3. Breadth-first level-order inspection

Meanwhile, for each station's subordinate connecting stations, the center chose one of the following visiting orders:
- Visit in ascending lexicographic order by station code
- Visit in descending lexicographic order by station code

These choices remain fixed and globally consistent throughout the evaluation process.

Your task:
Deduce the complete station inspection sequence. You can obtain scheduling information through comparison queries, but the query quota is limited.

Query format:
Use the following XML format for comparison queries (asking which of two stations is visited earlier in the inspection sequence):

<query_compare>X,Y</query_compare>

Where X and Y are different station codes. The dispatch system will return the station that is visited earlier in the inspection sequence.

Answer submission format:
When you are ready to submit your final dispatch plan, list all stations in the deduced inspection sequence (comma-separated):

<answer>V1,V2,V3,...,V{n}</answer>

Note:
- Please consume as few query quotas as possible
- All stations must appear exactly once
- The submitted plan must match the hidden inspection sequence exactly to pass the verification
"""

    contextualized_rule_zh_2 = """\
欢迎进入临床辅助诊断决策系统。我们来进行一项"医疗诊断决策树解析"任务，规则如下：

系统设定了一棵包含 {n} 个诊断节点的有根决策树，每个节点代表一项特定检测项目或体征，用唯一的大写字母字符串代号命名（如 A, ROOT, EA, NODE3 等）。

诊断结构信息：
- 初始症状节点：{root}
- 诊断推理结构：{tree_structure}

代号字典序规则：按 A 小于 B 小于 ... 小于 Z 的标准字典序逐字符比较；若一字符串为另一字符串的前缀，则较短者更小。

隐藏机制：
主治医师已秘密确立了一种评估策略和并发检测项的访问规则，生成了针对该病例所有诊断节点的一个完整评估顺序（每个节点恰好评估一次）。评估策略包括：
1. 深度优先先序评估
2. 深度优先后序评估  
3. 广度优先层序评估

同时，针对同一上级指征下的并发子节点，医师选择了以下执行顺序之一：
- 按检测项代号字典序升序执行
- 按检测项代号字典序降序执行

这些决策在本次病案解析过程中保持绝对一致。

你的任务：
推断出完整的医疗诊断评估顺序。你可以通过系统接口进行对比查询获取信息，但系统存在调用次数限制。

查询格式：
使用以下 XML 格式进行比较查询（询问两项检测在评估顺序中哪一项更早进行）：

<query_compare>X,Y</query_compare>

其中 X 和 Y 是不同的节点代号。系统会提示在评估顺序中较早执行的节点。

提交答案格式：
当你准备好出具最终诊断评估路径时，请按顺序列出所有节点代号（用逗号分隔）：

<answer>V1,V2,V3,...,V{n}</answer>

注意：
- 提倡以最少查询次数完成路径解析
- 诊断节点必须全部包含，且每个节点仅出现一次
- 最终路径必须与主治医师隐藏的评估顺序完全吻合方为成功
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the Clinical Decision Support System. Let's conduct a "Medical Diagnostic Decision Tree Analysis" task. Here are the rules:

The system provides a rooted decision tree with {n} diagnostic nodes, each representing a specific test item or vital sign, named with a unique uppercase letter string code (e.g., A, ROOT, EA, NODE3).

Diagnostic structure information:
- Initial symptom node: {root}
- Diagnostic reasoning structure: {tree_structure}

Lexicographic order rule: Standard dictionary order by A less than B less than ... less than Z, comparing character by character; if one string is a prefix of another, the shorter one is smaller.

Hidden mechanism:
The attending physician has secretly established an evaluation strategy and a concurrent test visiting rule, generating a complete evaluation sequence for all diagnostic nodes in this case (each node evaluated exactly once). The evaluation strategies include:
1. Depth-first preorder evaluation
2. Depth-first postorder evaluation
3. Breadth-first level-order evaluation

Meanwhile, for concurrent child nodes under the same parent indicator, the physician chose one of the following execution orders:
- Execute in ascending lexicographic order by test code
- Execute in descending lexicographic order by test code

These decisions remain absolutely consistent throughout this case analysis.

Your task:
Deduce the complete medical diagnostic evaluation sequence. You can obtain information through comparison queries via the system interface, but there is a limit on the number of calls.

Query format:
Use the following XML format for comparison queries (asking which of two tests is conducted earlier in the evaluation sequence):

<query_compare>X,Y</query_compare>

Where X and Y are different node codes. The system will prompt which node is executed earlier in the evaluation sequence.

Answer submission format:
When you are ready to issue the final diagnostic evaluation path, list all node codes in the deduced sequence (comma-separated):

<answer>V1,V2,V3,...,V{n}</answer>

Note:
- It is encouraged to complete the path analysis with the fewest queries
- All diagnostic nodes must be included exactly once
- The final path must perfectly match the physician's hidden evaluation sequence to be successful
"""

    contextualized_rule_zh_3 = """\
欢迎使用智能教学辅助平台。我们来规划一个"知识图谱学习路径"任务，规则如下：

课程体系设定了一棵包含 {n} 个知识模块的树形逻辑结构，每个模块用唯一的大写字母字符串编号命名（如 A, ROOT, EA, NODE3 等）。

课程结构信息：
- 基础前置模块：{root}
- 知识依赖图谱：{tree_structure}

编号字典序规则：按 A 小于 B 小于 ... 小于 Z 的标准字典序逐字符比较；若一字符串为另一字符串的前缀，则较短者更小。

隐藏机制：
教研组秘密选定了一种教学策略和同级模块的讲授规则，生成了这棵树上所有知识模块的标准学习顺序（每个模块恰好学习一次）。教学策略包括：
1. 深度优先先序教学
2. 深度优先后序教学  
3. 广度优先层序教学

同时，对于依赖同一前置知识的多个衍生模块，教研组选择了以下讲授顺序之一：
- 按模块编号字典序升序讲授
- 按模块编号字典序降序讲授

这些教研设定在整个规划过程中保持稳定且全局一致。

你的任务：
推演得出完整的标准学习顺序。你可以向系统发起对比查询来摸索规律，但查询额度受到严格限制。

查询格式：
使用以下 XML 格式进行比较查询（询问两个模块在学习顺序中哪个需要更早掌握）：

<query_compare>X,Y</query_compare>

其中 X 和 Y 是不同的模块编号。系统会提示在学习顺序中更早授课的模块。

提交答案格式：
当你准备好提交最终课程大纲时，请按学习顺序列出所有知识模块（用逗号分隔）：

<answer>V1,V2,V3,...,V{n}</answer>

注意：
- 请节约系统的查询额度
- 知识模块必须全部涵盖且无重复
- 提交的大纲必须与教研组隐藏的学习顺序严丝合缝才能通过审核
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Intelligent Tutoring System. Let's plan a "Knowledge Graph Learning Path" task. Here are the rules:

The curriculum sets up a tree-structured logical diagram containing {n} knowledge modules, each named with a unique uppercase letter string ID (e.g., A, ROOT, EA, NODE3).

Course structure information:
- Foundational prerequisite module: {root}
- Knowledge dependency graph: {tree_structure}

Lexicographic order rule: Standard dictionary order by A less than B less than ... less than Z, comparing character by character; if one string is a prefix of another, the shorter one is smaller.

Hidden mechanism:
The academic research group has secretly selected a teaching strategy and a rule for presenting peer modules, generating a standard learning sequence for all knowledge modules in this tree (each module learned exactly once). The teaching strategies include:
1. Depth-first preorder teaching
2. Depth-first postorder teaching
3. Breadth-first level-order teaching

Meanwhile, for multiple derivative modules depending on the same prerequisite knowledge, the group chose one of the following presentation orders:
- Teach in ascending lexicographic order by module ID
- Teach in descending lexicographic order by module ID

These pedagogical settings remain stable and globally consistent throughout the planning process.

Your task:
Deduce the complete standard learning sequence. You can initiate comparison queries to the system to explore the pattern, but the query quota is strictly limited.

Query format:
Use the following XML format for comparison queries (asking which of two modules must be mastered earlier in the learning sequence):

<query_compare>X,Y</query_compare>

Where X and Y are different module IDs. The system will prompt the module taught earlier in the sequence.

Answer submission format:
When you are ready to submit the final course syllabus, list all knowledge modules in the deduced learning sequence (comma-separated):

<answer>V1,V2,V3,...,V{n}</answer>

Note:
- Please conserve the system's query quota
- All knowledge modules must be covered without duplication
- The submitted syllabus must perfectly match the hidden learning sequence of the research group to pass the review
"""

    contextualized_rule_zh_4 = """\
欢迎进入智能制造车间控制系统。我们来执行一个"产品物料清单(BOM)装配"推演任务，规则如下：

工厂设定了一棵包含 {n} 个组件节点的BOM树，每个组件用唯一的大写字母字符串物料号命名（如 A, ROOT, EA, NODE3 等）。

物料结构信息：
- 最终成品节点：{root}
- BOM层级结构：{tree_structure}

物料号字典序规则：按 A 小于 B 小于 ... 小于 Z 的标准字典序逐字符比较；若一字符串为另一字符串的前缀，则较短者更小。

隐藏机制：
工艺工程师秘密制定了一种装配策略和同级零件的处理规则，生成了这棵BOM树上所有组件的完整流水线装配顺序（每个组件恰好经历一次装配动作）。装配策略包括：
1. 深度优先先序装配
2. 深度优先后序装配  
3. 广度优先层序装配

同时，针对属于同一父级总成的多个子零件，工程师选择了以下上线顺序之一：
- 按物料号字典序升序上线
- 按物料号字典序降序上线

这些工艺规范在整个排产推演过程中保持固定且全局一致。

你的任务：
反推出完整的工艺装配顺序。你可以通过比对指令来获取工序信息，但指令下发次数有限。

查询格式：
使用以下 XML 格式进行指令比对（询问两个组件在流水线装配中哪个更早执行）：

<query_compare>X,Y</query_compare>

其中 X 和 Y 是不同的物料号。控制系统会返回在装配顺序中优先处理的物料。

提交答案格式：
当你准备好输出最终排产SOP时，请按装配顺序列出所有物料号（用逗号分隔）：

<answer>V1,V2,V3,...,V{n}</answer>

注意：
- 请尽量减少无谓的指令下发
- 所有组件必须全部包含且不发生重漏
- 排产SOP必须与工艺工程师定下的装配顺序分毫不差方能下线生产
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Smart Factory Shop Floor Control System. Let's execute a "Bill of Materials (BOM) Assembly" deduction task. Here are the rules:

The factory specifies a BOM tree containing {n} component nodes, each named with a unique uppercase letter string part number (e.g., A, ROOT, EA, NODE3).

Material structure information:
- Final product node: {root}
- BOM hierarchical structure: {tree_structure}

Lexicographic order rule: Standard dictionary order by A less than B less than ... less than Z, comparing character by character; if one string is a prefix of another, the shorter one is smaller.

Hidden mechanism:
The process engineer has secretly formulated an assembly strategy and a processing rule for peer parts, generating a complete assembly line sequence for all components in this BOM tree (each component undergoes exactly one assembly action). The assembly strategies include:
1. Depth-first preorder assembly
2. Depth-first postorder assembly
3. Breadth-first level-order assembly

Meanwhile, for multiple sub-parts belonging to the same parent assembly, the engineer chose one of the following feeding orders:
- Feed in ascending lexicographic order by part number
- Feed in descending lexicographic order by part number

These process specifications remain fixed and globally consistent throughout the production scheduling deduction.

Your task:
Reverse-engineer the complete process assembly sequence. You can obtain routing information through comparison commands, but the number of command issues is limited.

Query format:
Use the following XML format for comparison commands (asking which of two components is executed earlier in the pipeline assembly):

<query_compare>X,Y</query_compare>

Where X and Y are different part numbers. The control system will return the material processed earlier in the assembly sequence.

Answer submission format:
When you are ready to output the final scheduling SOP, list all part numbers in the assembly sequence (comma-separated):

<answer>V1,V2,V3,...,V{n}</answer>

Note:
- Please minimize unnecessary command issues
- All components must be included without duplication or omission
- The scheduling SOP must match the engineer's exact assembly sequence to be cleared for production
"""

    contextualized_rule_zh_5 = """\
欢迎使用法律逻辑推演与证据链梳理平台。我们来梳理一个"法庭证据链推演"任务，规则如下：

案件的诉讼逻辑构成了一棵包含 {n} 个证据节点的树形图，每个节点用唯一的大写字母字符串卷宗号命名（如 A, ROOT, EA, NODE3 等）。

证据链结构信息：
- 核心控诉节点：{root}
- 证据衍生结构：{tree_structure}

卷宗号字典序规则：按 A 小于 B 小于 ... 小于 Z 的标准字典序逐字符比较；若一字符串为另一字符串的前缀，则较短者更小。

隐藏机制：
首席出庭律师已在内部秘密敲定了一种质证策略和并列证据的出示规则，生成了所有证据在庭审阶段的一个完整出示顺序（每份证据恰好出示一次）。质证策略包括：
1. 深度优先先序质证
2. 深度优先后序质证  
3. 广度优先层序质证

同时，对于支撑同一论点的多份并列子证据，律师选择了以下庭审出示顺序之一：
- 按卷宗号字典序升序出示
- 按卷宗号字典序降序出示

这些庭审战术在整个推演流程中保持高度一致，不会更改。

你的任务：
推演并还原出完整的庭审证据出示顺序。你可以向律所系统提交质询以验证线索，但允许的质询次数有限。

查询格式：
使用以下 XML 格式进行对比质询（询问两份证据在庭审顺序中哪份更早呈堂）：

<query_compare>X,Y</query_compare>

其中 X 和 Y 是不同的卷宗号。系统会反馈在出示顺序中更先呈递的卷宗。

提交答案格式：
当你准备好定稿最终出庭预案时，请按庭审出示顺序列出所有卷宗号（用逗号分隔）：

<answer>V1,V2,V3,...,V{n}</answer>

注意：
- 请以极简的质询次数完成案情推演
- 必须穷尽所有证据节点且不得重复
- 最终定稿的出庭预案必须与首席律师隐藏的战术顺序严丝合缝才能确立
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the Legal Logic Deduction and Evidence Chain Profiling Platform. Let's outline a "Court Evidence Chain Deduction" task. Here are the rules:

The litigation logic of the case constitutes a tree diagram containing {n} evidence nodes, each named with a unique uppercase letter string dossier number (e.g., A, ROOT, EA, NODE3).

Evidence chain structure information:
- Core allegation node: {root}
- Evidence derivative structure: {tree_structure}

Lexicographic order rule: Standard dictionary order by A less than B less than ... less than Z, comparing character by character; if one string is a prefix of another, the shorter one is smaller.

Hidden mechanism:
The lead trial attorney has secretly finalized a cross-examination strategy and a presentation rule for parallel evidence, generating a complete presentation sequence for all evidence during the trial phase (each piece of evidence presented exactly once). The cross-examination strategies include:
1. Depth-first preorder cross-examination
2. Depth-first postorder cross-examination
3. Breadth-first level-order cross-examination

Meanwhile, for multiple parallel sub-evidences supporting the same argument, the attorney chose one of the following trial presentation orders:
- Present in ascending lexicographic order by dossier number
- Present in descending lexicographic order by dossier number

These trial tactics remain highly consistent and unchanged throughout the deduction process.

Your task:
Deduce and reconstruct the complete trial evidence presentation sequence. You can submit inquiries to the firm's system to verify clues, but the allowed number of inquiries is limited.

Query format:
Use the following XML format for comparison inquiries (asking which of two pieces of evidence is presented earlier in the trial sequence):

<query_compare>X,Y</query_compare>

Where X and Y are different dossier numbers. The system will feedback the dossier submitted earlier in the presentation sequence.

Answer submission format:
When you are ready to finalize the trial preparation plan, list all dossier numbers in the trial presentation sequence (comma-separated):

<answer>V1,V2,V3,...,V{n}</answer>

Note:
- Please complete the case deduction with the minimum number of inquiries
- All evidence nodes must be exhausted without duplication
- The finalized trial preparation plan must seamlessly match the lead attorney's hidden tactical sequence to be established
"""

    user_prompt_zh = "请开始你的推理。你可以进行比较查询或直接提交答案。"
    user_prompt_en = "Please start your deduction. You can make comparison queries or submit your answer directly."

    tags = ["answer", "query_compare"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "root": "A",
                "tree": {
                    "A": ["B", "C"],
                    "B": ["D"],
                    "C": [],
                    "D": []
                },
                "traversal_type": "preorder",
                "sibling_order": "asc"
            },
            2: {
                "n": 6,
                "root": "ROOT",
                "tree": {
                    "ROOT": ["A", "B"],
                    "A": ["C", "D"],
                    "B": ["E"],
                    "C": [],
                    "D": [],
                    "E": []
                },
                "traversal_type": "bfs",
                "sibling_order": "asc"
            },
            3: {
                "n": 8,
                "root": "R",
                "tree": {
                    "R": ["A", "B", "C"],
                    "A": ["D", "E"],
                    "B": [],
                    "C": ["F"],
                    "D": [],
                    "E": ["G"],
                    "F": [],
                    "G": []
                },
                "traversal_type": "postorder",
                "sibling_order": "asc"
            },
            4: {
                "n": 10,
                "root": "ROOT",
                "tree": {
                    "ROOT": ["A", "B"],
                    "A": ["C", "D", "E"],
                    "B": ["F", "G"],
                    "C": ["H"],
                    "D": [],
                    "E": ["I"],
                    "F": [],
                    "G": [],
                    "H": [],
                    "I": []
                },
                "traversal_type": "preorder",
                "sibling_order": "desc"
            },
            5: {
                "n": 12,
                "root": "R",
                "tree": {
                    "R": ["A", "B", "C"],
                    "A": ["D", "E"],
                    "B": ["F", "G", "H"],
                    "C": ["I"],
                    "D": ["J"],
                    "E": [],
                    "F": [],
                    "G": ["K"],
                    "H": [],
                    "I": [],
                    "J": [],
                    "K": []
                },
                "traversal_type": "postorder",
                "sibling_order": "desc"
            }
        },
        "en": {
            1: {
                "n": 4,
                "root": "A",
                "tree": {
                    "A": ["B", "C"],
                    "B": ["D"],
                    "C": [],
                    "D": []
                },
                "traversal_type": "preorder",
                "sibling_order": "asc"
            },
            2: {
                "n": 6,
                "root": "ROOT",
                "tree": {
                    "ROOT": ["A", "B"],
                    "A": ["C", "D"],
                    "B": ["E"],
                    "C": [],
                    "D": [],
                    "E": []
                },
                "traversal_type": "bfs",
                "sibling_order": "asc"
            },
            3: {
                "n": 8,
                "root": "R",
                "tree": {
                    "R": ["A", "B", "C"],
                    "A": ["D", "E"],
                    "B": [],
                    "C": ["F"],
                    "D": [],
                    "E": ["G"],
                    "F": [],
                    "G": []
                },
                "traversal_type": "postorder",
                "sibling_order": "asc"
            },
            4: {
                "n": 10,
                "root": "ROOT",
                "tree": {
                    "ROOT": ["A", "B"],
                    "A": ["C", "D", "E"],
                    "B": ["F", "G"],
                    "C": ["H"],
                    "D": [],
                    "E": ["I"],
                    "F": [],
                    "G": [],
                    "H": [],
                    "I": []
                },
                "traversal_type": "preorder",
                "sibling_order": "desc"
            },
            5: {
                "n": 12,
                "root": "R",
                "tree": {
                    "R": ["A", "B", "C"],
                    "A": ["D", "E"],
                    "B": ["F", "G", "H"],
                    "C": ["I"],
                    "D": ["J"],
                    "E": [],
                    "F": [],
                    "G": ["K"],
                    "H": [],
                    "I": [],
                    "J": [],
                    "K": []
                },
                "traversal_type": "postorder",
                "sibling_order": "desc"
            }
        }
    }

    def __init__(self, config):
        self.query_count = 0
        self.max_queries = 0
        self._last_query_nodes = None
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty
        
        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self._game_info["n"] = cfg["n"]
        self._game_info["root"] = cfg["root"]
        
        tree_desc = self._format_tree_structure(cfg["tree"])
        self._game_info["tree_structure"] = tree_desc
        
        self.tree = cfg["tree"]
        self.root = cfg["root"]
        self.traversal_type = cfg["traversal_type"]
        self.sibling_order = cfg["sibling_order"]
        
        n = cfg["n"]
        self.max_queries = 2 * math.ceil(math.log2(n)) + 6
        
        self.correct_order = self._generate_traversal()
        
        self.query_count = 0

    def _format_tree_structure(self, tree: Dict[str, List[str]]) -> str:
        lines = []
        for node, children in sorted(tree.items()):
            if children:
                children_str = ", ".join(sorted(children))
                lines.append(f"{node} 的子节点: [{children_str}]" if self.config.language == "zh" 
                           else f"Children of {node}: [{children_str}]")
            else:
                lines.append(f"{node} 的子节点: []" if self.config.language == "zh"
                           else f"Children of {node}: []")
        return "; ".join(lines)

    def _generate_traversal(self) -> List[str]:
        if self.traversal_type == "preorder":
            return self._dfs_preorder()
        elif self.traversal_type == "postorder":
            return self._dfs_postorder()
        elif self.traversal_type == "bfs":
            return self._bfs()
        else:
            raise ValueError(f"Unknown traversal type: {self.traversal_type}")

    def _get_sorted_children(self, node: str) -> List[str]:
        children = self.tree.get(node, [])
        if self.sibling_order == "asc":
            return sorted(children)
        else:
            return sorted(children, reverse=True)

    def _dfs_preorder(self) -> List[str]:
        result = []
        
        def dfs(node):
            result.append(node)
            for child in self._get_sorted_children(node):
                dfs(child)
        
        dfs(self.root)
        return result

    def _dfs_postorder(self) -> List[str]:
        result = []
        
        def dfs(node):
            for child in self._get_sorted_children(node):
                dfs(child)
            result.append(node)
        
        dfs(self.root)
        return result

    def _bfs(self) -> List[str]:
        result = []
        queue = deque([self.root])
        
        while queue:
            node = queue.popleft()
            result.append(node)
            for child in self._get_sorted_children(node):
                queue.append(child)
        
        return result

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        try:
            submitted_order = [x.strip() for x in raw_ans.split(",") if x.strip()]
        except:
            return False
        
        if len(submitted_order) != len(self.correct_order):
            return False
        
        return submitted_order == self.correct_order

    def _cf_core_produce(self, parsed_info):
        if "query_compare" not in parsed_info:
            return "Error: Invalid query." if self.config.language == "en" else "错误：无效的查询。"
        
        if self.query_count >= self.max_queries:
            if self.config.language == "en":
                return f"Error: Query limit exceeded (max {self.max_queries} queries). Please submit your answer now."
            else:
                return f"错误：超过查询次数上限（最多 {self.max_queries} 次查询）。请直接提交你的答案。"
        
        try:
            raw = parsed_info["query_compare"].strip()
            parts = [x.strip() for x in raw.split(",")]
            
            if len(parts) != 2:
                raise ValueError("Invalid format")
            
            node1, node2 = parts
            
            if node1 not in self.tree or node2 not in self.tree:
                return "Error: Node not found." if self.config.language == "en" else "错误：节点不存在。"
            
            if node1 == node2:
                return "Error: Nodes must be different." if self.config.language == "en" else "错误：节点必须不同。"
            
            self.query_count += 1
            
            idx1 = self.correct_order.index(node1)
            idx2 = self.correct_order.index(node2)
            
            earlier = node1 if idx1 < idx2 else node2
            
            self._last_query_nodes = (node1, node2)
            
            return f"Earlier: {earlier}"
            
        except ValueError as e:
            return "Error: Invalid query format." if self.config.language == "en" else "错误：查询格式无效。"
        except Exception as e:
            return "Error: Invalid query." if self.config.language == "en" else "错误：无效的查询。"

    def _cf_make_wrong(self, correct: str) -> str:
        match = re.match(r'^Earlier:\s*(\S+)$', correct)
        if match and getattr(self, '_last_query_nodes', None) is not None:
            earlier_node = match.group(1)
            node1, node2 = self._last_query_nodes
            wrong_node = node2 if earlier_node == node1 else node1
            return f"Earlier: {wrong_node}"
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> List[Dict[str, str]]:
        queries = []
        nodes = sorted(self.tree.keys())
        
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                node1, node2 = nodes[i], nodes[j]
                
                query_str = f"<query_compare>{node1},{node2}</query_compare>"
                
                try:
                    idx1 = self.correct_order.index(node1)
                    idx2 = self.correct_order.index(node2)
                    
                    earlier = node1 if idx1 < idx2 else node2
                    
                    answer = f"Earlier: {earlier}"
                    
                    queries.append({
                        "query": query_str,
                        "answer": answer
                    })
                except ValueError:
                    continue
                    
        return queries