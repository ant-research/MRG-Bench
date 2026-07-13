# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   添加边影响：在两节点间添加一条边后是否产生环
# ============================================================

from .base import Game
import re
import itertools


class HiddenPermutationTreeGame(Game):

    game_rule_zh = """\
我们来玩一个"隐藏置换推理"的游戏，规则如下：

游戏设定了一个固定的无向树 T，顶点集合为 {{A,B,C,D,E,F,G}}，边集为 {{(A,B),(A,C),(B,D),(B,E),(E,F),(E,G)}}。目标顶点是 E。

存在一个未知的标签置换 f，它将你使用的标签映射到树的真实顶点。有四个候选置换方案：
- 方案α：A→A, B→B, C→C, D→D, E→E, F→F, G→G
- 方案β：A→C, C→A, D→E, E→D, B→B, F→F, G→G
- 方案γ：A→B, B→C, C→A, F→G, G→F, D→D, E→E
- 方案δ：B→E, E→B, D→F, F→D, A→A, C→C, G→G

你的任务是通过提问推断出正确的置换方案，并最终添加一条边使得形成的环包含顶点 E。

## 可用的查询类型

每次只能提出一个查询：

1. **试连查询**：询问"如果添加标签 X 和 Y 之间的边，会产生环吗？"
   - 系统会将 X 和 Y 通过隐藏置换 f 映射到真实顶点，判断在当前树 T 上添加这条边是否会产生环
   - 若该边已存在于树中，则不会产生环；否则会产生环
   - 回答"会环"或"不会环"

2. **方案宣告**：宣告你认为的置换方案（α、β、γ 或 δ）
   - 回答"正确"或"错误"

3. **最终加边**：执行最终的加边操作
   - 指定标签对 X 和 Y
   - 系统会报告实际相连的真实顶点对，以及是否成环
   - 若成环，会给出环的路径并说明是否包含顶点 E

## 查询格式

- 试连查询（例如询问标签 A 和 D）：
<query_trial>A,D</query_trial>

- 方案宣告（例如宣告方案 α）：
<query_declare>α</query_declare>

- 最终加边（例如在标签 C 和 F 之间加边）：
<answer>C,F</answer>

## 胜利条件

同时满足以下条件才能获胜：
1. 在执行最终加边之前，已通过方案宣告获得"正确"确认
2. 最终加边形成环，且该环的路径包含顶点 E

## 失败条件

满足以下任一条件即失败：
1. 最终加边未成环，或成环但路径不包含 E
2. 未进行正确的方案宣告就执行最终加边
3. 提问格式不符合要求

请用尽可能少的查询次数完成任务。
"""

    game_rule_en = """\
Let's play a "Hidden Permutation Deduction" game. Here are the rules:

The game has a fixed undirected tree T with vertex set {{A,B,C,D,E,F,G}} and edge set {{(A,B),(A,C),(B,D),(B,E),(E,F),(E,G)}}. The target vertex is E.

There exists an unknown label permutation f that maps the labels you use to the actual vertices in the tree. There are four candidate permutation schemes:
- Scheme α: A→A, B→B, C→C, D→D, E→E, F→F, G→G
- Scheme β: A→C, C→A, D→E, E→D, B→B, F→F, G→G
- Scheme γ: A→B, B→C, C→A, F→G, G→F, D→D, E→E
- Scheme δ: B→E, E→B, D→F, F→D, A→A, C→C, G→G

Your task is to deduce the correct permutation scheme through queries, and finally add an edge such that the resulting cycle contains vertex E.

## Available Query Types

You can make one query at a time:

1. **Trial Connection Query**: Ask "If I add an edge between labels X and Y, will it create a cycle?"
   - The system maps X and Y to actual vertices via the hidden permutation f, and checks if adding this edge to tree T would create a cycle
   - If the edge already exists in the tree, it will not create a cycle; otherwise it will
   - Answer: "Cycle" or "No cycle"

2. **Scheme Declaration**: Declare which permutation scheme you believe is correct (α, β, γ, or δ)
   - Answer: "Correct" or "Incorrect"

3. **Final Edge Addition**: Execute the final edge addition
   - Specify label pair X and Y
   - The system reports the actual vertex pair connected, whether a cycle is formed
   - If a cycle forms, it provides the cycle path and indicates whether it contains vertex E

## Query Format

- Trial connection query (e.g., asking about labels A and D):
<query_trial>A,D</query_trial>

- Scheme declaration (e.g., declaring scheme α):
<query_declare>α</query_declare>

- Final edge addition (e.g., adding edge between labels C and F):
<answer>C,F</answer>

## Victory Conditions

Win by satisfying both:
1. Before executing final edge addition, you have received "Correct" confirmation via scheme declaration
2. Final edge addition forms a cycle, and the cycle path contains vertex E

## Failure Conditions

Fail if any of the following occurs:
1. Final edge addition does not form a cycle, or forms a cycle that does not contain E
2. Execute final edge addition without correct scheme declaration
3. Query format does not meet requirements

Please complete the task with as few queries as possible.
"""

    contextualized_rule_zh_1 = """\
我们来玩一个"隐藏交通网络勘测"游戏，规则如下：

系统内存在一个固定的城际铁路网络图，包含7个核心交通枢纽，真实代号集合为 {{A,B,C,D,E,F,G}}，已有的铁路连线为 {{(A,B),(A,C),(B,D),(B,E),(E,F),(E,G)}}。E 是重点保障枢纽。

由于数据加密，你看到的站点标签被一个未知的置换方案 f 映射到了真实枢纽代号。有四个候选解密方案：
- 方案α：A→A, B→B, C→C, D→D, E→E, F→F, G→G
- 方案β：A→C, C→A, D→E, E→D, B→B, F→F, G→G
- 方案γ：A→B, B→C, C→A, F→G, G→F, D→D, E→E
- 方案δ：B→E, E→B, D→F, F→D, A→A, C→C, G→G

你的任务是通过勘测查询推断出正确的解密方案，并最终规划一条新铁路，使得形成的铁路环线经过重点保障枢纽 E。

## 可用的查询类型

每次只能提出一个查询：

1. **试连查询**：询问"如果在加密标签 X 和 Y 之间规划一条新铁路，是否会与现有网络形成环线？"
   - 系统将自动转化为真实枢纽代号进行模拟检测。如果该连线已存在于路网中，不会成环；否则会成环
   - 回答"会环"或"不会环"

2. **方案宣告**：宣告你认为正确的解密方案（α、β、γ 或 δ）
   - 回答"正确"或"错误"

3. **最终加边**：执行新铁路的最终建设指令
   - 指定标签对 X 和 Y
   - 系统将反馈真实接入的枢纽对，以及是否成环、环线是否包含 E

## 查询格式

- 试连查询（例如询问标签 A 和 D）：
<query_trial>A,D</query_trial>

- 方案宣告（例如宣告方案 α）：
<query_declare>α</query_declare>

- 最终加边（例如在标签 C 和 F 之间修路）：
<answer>C,F</answer>

## 胜利条件

同时满足以下条件才能获胜：
1. 在执行最终加边之前，已通过方案宣告获得"正确"确认
2. 最终加边成功形成铁路环线，且该环线经过枢纽 E

## 失败条件

满足以下任一条件即失败：
1. 最终加边未成环，或成环但环线不包含 E
2. 未进行正确的方案宣告就执行最终加边
3. 提问格式不符合要求

请用尽可能少的查询次数完成任务。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's play a "Hidden Traffic Network Survey" game. Here are the rules:

The system has a fixed intercity railway network graph containing 7 core traffic hubs with actual codes {{A,B,C,D,E,F,G}} and existing railway connections {{(A,B),(A,C),(B,D),(B,E),(E,F),(E,G)}}. Hub E is the critical guarantee hub.

Due to data encryption, the station labels you see are mapped to actual hub codes via an unknown permutation scheme f. There are four candidate decryption schemes:
- Scheme α: A→A, B→B, C→C, D→D, E→E, F→F, G→G
- Scheme β: A→C, C→A, D→E, E→D, B→B, F→F, G→G
- Scheme γ: A→B, B→C, C→A, F→G, G→F, D→D, E→E
- Scheme δ: B→E, E→B, D→F, F→D, A→A, C→C, G→G

Your task is to deduce the correct decryption scheme through survey queries, and finally plan a new railway such that the resulting railway loop passes through the critical guarantee hub E.

## Available Query Types

You can make one query at a time:

1. **Trial Connection Query**: Ask "If I plan a new railway between encrypted labels X and Y, will it create a loop in the current network?"
   - The system checks based on the actual hub codes. If the connection already exists, no loop is formed; otherwise, it creates a loop
   - Answer: "Cycle" or "No cycle"

2. **Scheme Declaration**: Declare which decryption scheme you believe is correct (α, β, γ, or δ)
   - Answer: "Correct" or "Incorrect"

3. **Final Edge Addition**: Execute the final construction directive for the new railway
   - Specify label pair X and Y
   - The system reports the actual hub pair connected, whether a loop is formed, and whether it includes hub E

## Query Format

- Trial connection query (e.g., asking about labels A and D):
<query_trial>A,D</query_trial>

- Scheme declaration (e.g., declaring scheme α):
<query_declare>α</query_declare>

- Final edge addition (e.g., adding railway between labels C and F):
<answer>C,F</answer>

## Victory Conditions

Win by satisfying both:
1. Before executing final edge addition, you have received "Correct" confirmation via scheme declaration
2. Final edge addition forms a railway loop, and the loop path contains hub E

## Failure Conditions

Fail if any of the following occurs:
1. Final edge addition does not form a loop, or forms a loop that does not contain E
2. Execute final edge addition without correct scheme declaration
3. Query format does not meet requirements

Please complete the task with as few queries as possible.
"""

    contextualized_rule_zh_2 = """\
我们来玩一个"隐藏靶向通路推断"游戏，规则如下：

系统内存在一个固定的蛋白质相互作用通路，包含7个关键蛋白，真实代号为 {{A,B,C,D,E,F,G}}，已知的相互作用链路为 {{(A,B),(A,C),(B,D),(B,E),(E,F),(E,G)}}。E 是核心靶向蛋白。

当前实验代号被一个未知的置换方案 f 打乱了对应关系。有四个候选的序列映射方案：
- 方案α：A→A, B→B, C→C, D→D, E→E, F→F, G→G
- 方案β：A→C, C→A, D→E, E→D, B→B, F→F, G→G
- 方案γ：A→B, B→C, C→A, F→G, G→F, D→D, E→E
- 方案δ：B→E, E→B, D→F, F→D, A→A, C→C, G→G

你的任务是通过模拟测试推断出正确的蛋白映射方案，并最终建立一条新的干预路径，使得形成的信号循环通路包含靶向蛋白 E。

## 可用的查询类型

每次只能提出一个查询：

1. **试连查询**：询问"如果在实验代号 X 和 Y 之间建立干预路径，是否会导致信号传导出现循环？"
   - 系统会基于真实的蛋白网络进行验证。若干预路径已存在，则不会产生循环；否则会产生循环
   - 回答"会环"或"不会环"

2. **方案宣告**：宣告你认为正确的序列映射方案（α、β、γ 或 δ）
   - 回答"正确"或"错误"

3. **最终加边**：执行最终的靶向干预操作
   - 指定代号对 X 和 Y
   - 系统会报告实际连接的真实蛋白对，以及是否形成循环、是否经过核心蛋白 E

## 查询格式

- 试连查询（例如询问代号 A 和 D）：
<query_trial>A,D</query_trial>

- 方案宣告（例如宣告方案 α）：
<query_declare>α</query_declare>

- 最终加边（例如在代号 C 和 F 之间建立干预路径）：
<answer>C,F</answer>

## 胜利条件

同时满足以下条件才能获胜：
1. 在执行最终加边之前，已通过方案宣告获得"正确"确认
2. 最终加边成功形成信号传导循环，且该循环包含核心蛋白 E

## 失败条件

满足以下任一条件即失败：
1. 最终加边未产生循环，或循环不包含 E
2. 未进行正确的方案宣告就执行最终加边
3. 提问格式不符合要求

请用尽可能少的查询次数完成任务。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Hidden Targeted Pathway Deduction" game. Here are the rules:

The system contains a fixed protein interaction pathway involving 7 key proteins with actual codes {{A,B,C,D,E,F,G}} and known interaction links {{(A,B),(A,C),(B,D),(B,E),(E,F),(E,G)}}. E is the core target protein.

The current experimental labels are scrambled by an unknown permutation f that maps them to the actual proteins. There are four candidate sequence mapping schemes:
- Scheme α: A→A, B→B, C→C, D→D, E→E, F→F, G→G
- Scheme β: A→C, C→A, D→E, E→D, B→B, F→F, G→G
- Scheme γ: A→B, B→C, C→A, F→G, G→F, D→D, E→E
- Scheme δ: B→E, E→B, D→F, F→D, A→A, C→C, G→G

Your task is to deduce the correct protein mapping scheme through simulation queries, and finally establish a new intervention path such that the resulting signal transduction cycle involves target protein E.

## Available Query Types

You can make one query at a time:

1. **Trial Connection Query**: Ask "If an intervention path is established between experimental labels X and Y, will it cause a signal transduction cycle?"
   - The system validates against the actual protein network. If the path already exists, no cycle is formed; otherwise, it forms a cycle
   - Answer: "Cycle" or "No cycle"

2. **Scheme Declaration**: Declare the correct sequence mapping scheme (α, β, γ, or δ)
   - Answer: "Correct" or "Incorrect"

3. **Final Edge Addition**: Execute the final targeted intervention
   - Specify label pair X and Y
   - The system reports the actual connected protein pair, whether a cycle is formed, and whether it includes target E

## Query Format

- Trial connection query (e.g., asking about labels A and D):
<query_trial>A,D</query_trial>

- Scheme declaration (e.g., declaring scheme α):
<query_declare>α</query_declare>

- Final edge addition (e.g., establishing path between labels C and F):
<answer>C,F</answer>

## Victory Conditions

Win by satisfying both:
1. Before executing final edge addition, you have received "Correct" confirmation via scheme declaration
2. Final edge addition forms a signal transduction cycle, and the cycle path contains target protein E

## Failure Conditions

Fail if any of the following occurs:
1. Final edge addition does not form a cycle, or forms a cycle that does not contain E
2. Execute final edge addition without correct scheme declaration
3. Query format does not meet requirements

Please complete the task with as few queries as possible.
"""

    contextualized_rule_zh_3 = """\
我们来玩一个"隐藏知识图谱构建"游戏，规则如下：

系统内设有一个核心课程的先修依赖树，包含7个知识模块，真实名称为 {{A,B,C,D,E,F,G}}，已有的依赖关联为 {{(A,B),(A,C),(B,D),(B,E),(E,F),(E,G)}}。E 是终极培养目标。

现有的模块编号被未知置换方案 f 进行了脱敏处理。有四个候选的名称对照方案：
- 方案α：A→A, B→B, C→C, D→D, E→E, F→F, G→G
- 方案β：A→C, C→A, D→E, E→D, B→B, F→F, G→G
- 方案γ：A→B, B→C, C→A, F→G, G→F, D→D, E→E
- 方案δ：B→E, E→B, D→F, F→D, A→A, C→C, G→G

你的任务是通过测试推断出正确的名称对照方案，并最终添加一条新的跨模块强关联，使得形成的闭环学习路径能够覆盖培养目标 E。

## 可用的查询类型

每次只能提出一个查询：

1. **试连查询**：询问"如果建立编号 X 和 Y 之间的强关联，是否会导致学习路径出现闭环？"
   - 系统会代入真实知识模块判断。若该关联已存在，不成环；否则会产生闭环
   - 回答"会环"或"不会环"

2. **方案宣告**：宣告你认为正确的名称对照方案（α、β、γ 或 δ）
   - 回答"正确"或"错误"

3. **最终加边**：提交最终的课程大纲修订方案
   - 指定编号对 X 和 Y
   - 系统将反馈真实联结的知识模块，以及是否形成闭环、闭环是否包含目标 E

## 查询格式

- 试连查询（例如询问编号 A 和 D）：
<query_trial>A,D</query_trial>

- 方案宣告（例如宣告方案 α）：
<query_declare>α</query_declare>

- 最终加边（例如在编号 C 和 F 之间建立关联）：
<answer>C,F</answer>

## 胜利条件

同时满足以下条件才能获胜：
1. 在执行最终加边之前，已通过方案宣告获得"正确"确认
2. 最终加边成功形成闭环学习路径，且该闭环包含培养目标 E

## 失败条件

满足以下任一条件即失败：
1. 最终加边未产生闭环，或闭环不包含 E
2. 未进行正确的方案宣告就执行最终加边
3. 提问格式不符合要求

请用尽可能少的查询次数完成任务。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Hidden Knowledge Graph Construction" game. Here are the rules:

The system features a prerequisite dependency tree for a core curriculum, containing 7 knowledge modules with actual names {{A,B,C,D,E,F,G}} and existing dependencies {{(A,B),(A,C),(B,D),(B,E),(E,F),(E,G)}}. E is the ultimate capability objective.

The available module IDs are masked by an unknown permutation scheme f mapping to the actual modules. There are four candidate name matching schemes:
- Scheme α: A→A, B→B, C→C, D→D, E→E, F→F, G→G
- Scheme β: A→C, C→A, D→E, E→D, B→B, F→F, G→G
- Scheme γ: A→B, B→C, C→A, F→G, G→F, D→D, E→E
- Scheme δ: B→E, E→B, D→F, F→D, A→A, C→C, G→G

Your task is to deduce the correct matching scheme through testing queries, and finally add a new strong cross-module association such that the resulting closed-loop learning path covers objective E.

## Available Query Types

You can make one query at a time:

1. **Trial Connection Query**: Ask "If a strong association is added between module IDs X and Y, will it create a closed loop in the learning path?"
   - The system maps this to the actual modules. If the association already exists, no loop is formed; otherwise, it forms a loop
   - Answer: "Cycle" or "No cycle"

2. **Scheme Declaration**: Declare the correct name matching scheme (α, β, γ, or δ)
   - Answer: "Correct" or "Incorrect"

3. **Final Edge Addition**: Submit the final syllabus revision
   - Specify ID pair X and Y
   - The system reports the actual knowledge modules connected, whether a closed loop is formed, and whether it covers objective E

## Query Format

- Trial connection query (e.g., asking about IDs A and D):
<query_trial>A,D</query_trial>

- Scheme declaration (e.g., declaring scheme α):
<query_declare>α</query_declare>

- Final edge addition (e.g., adding association between IDs C and F):
<answer>C,F</answer>

## Victory Conditions

Win by satisfying both:
1. Before executing final edge addition, you have received "Correct" confirmation via scheme declaration
2. Final edge addition forms a closed-loop learning path, and the loop contains objective E

## Failure Conditions

Fail if any of the following occurs:
1. Final edge addition does not form a loop, or forms a loop that does not contain E
2. Execute final edge addition without correct scheme declaration
3. Query format does not meet requirements

Please complete the task with as few queries as possible.
"""

    contextualized_rule_zh_4 = """\
我们来玩一个"隐藏工业管网排查"游戏，规则如下：

工厂内有一套物料流转管网图，包含7个核心车间，真实编号为 {{A,B,C,D,E,F,G}}，现有管线分布为 {{(A,B),(A,C),(B,D),(B,E),(E,F),(E,G)}}。E 是总装质检车间。

出于保密，图纸上的系统编号与实际车间由未知置换方案 f 映射。有四个候选的图纸映射方案：
- 方案α：A→A, B→B, C→C, D→D, E→E, F→F, G→G
- 方案β：A→C, C→A, D→E, E→D, B→B, F→F, G→G
- 方案γ：A→B, B→C, C→A, F→G, G→F, D→D, E→E
- 方案δ：B→E, E→B, D→F, F→D, A→A, C→C, G→G

你的任务是通过工程探测推断出正确的图纸映射方案，并最终铺设一条新管线，使得形成的物料冗余回路经过总装质检车间 E。

## 可用的查询类型

每次只能提出一个查询：

1. **试连查询**：询问"如果在系统编号 X 和 Y 之间铺设管线，是否会形成物料流转回路？"
   - 系统将自动代入真实车间判定。若该管线已存在，不成回路；否则会形成回路（会环）
   - 回答"会环"或"不会环"

2. **方案宣告**：宣告你认为正确的图纸映射方案（α、β、γ 或 δ）
   - 回答"正确"或"错误"

3. **最终加边**：下达最终管线铺设施工作业指令
   - 指定编号对 X 和 Y
   - 系统将反馈真实连接的车间对，以及是否形成回路、回路是否通过车间 E

## 查询格式

- 试连查询（例如询问编号 A 和 D）：
<query_trial>A,D</query_trial>

- 方案宣告（例如宣告方案 α）：
<query_declare>α</query_declare>

- 最终加边（例如在编号 C 和 F 之间铺设管线）：
<answer>C,F</answer>

## 胜利条件

同时满足以下条件才能获胜：
1. 在执行最终加边之前，已通过方案宣告获得"正确"确认
2. 最终加边成功形成物料冗余回路，且该回路经过车间 E

## 失败条件

满足以下任一条件即失败：
1. 最终加边未产生回路，或回路不包含 E
2. 未进行正确的方案宣告就执行最终加边
3. 提问格式不符合要求

请用尽可能少的查询次数完成任务。
"""

    contextualized_rule_en_4 = """\
[Industrial/Manufacturing Scenario]
Let's play a "Hidden Industrial Pipeline Inspection" game. Here are the rules:

The factory has a material flow pipeline network diagram covering 7 core workshops with actual codes {{A,B,C,D,E,F,G}} and existing pipelines {{(A,B),(A,C),(B,D),(B,E),(E,F),(E,G)}}. E is the final assembly and quality inspection workshop.

For confidentiality, the system IDs on the diagram are mapped to actual workshops via an unknown permutation f. There are four candidate blueprint mapping schemes:
- Scheme α: A→A, B→B, C→C, D→D, E→E, F→F, G→G
- Scheme β: A→C, C→A, D→E, E→D, B→B, F→F, G→G
- Scheme γ: A→B, B→C, C→A, F→G, G→F, D→D, E→E
- Scheme δ: B→E, E→B, D→F, F→D, A→A, C→C, G→G

Your task is to deduce the correct blueprint mapping scheme through engineering probes, and finally lay a new pipeline such that the resulting redundant material loop passes through workshop E.

## Available Query Types

You can make one query at a time:

1. **Trial Connection Query**: Ask "If a pipeline is laid between system IDs X and Y, will it form a material flow loop?"
   - The system maps this to the actual workshops. If the pipeline already exists, no loop is formed; otherwise, it forms a loop
   - Answer: "Cycle" or "No cycle"

2. **Scheme Declaration**: Declare the correct blueprint mapping scheme (α, β, γ, or δ)
   - Answer: "Correct" or "Incorrect"

3. **Final Edge Addition**: Issue the final pipeline construction directive
   - Specify ID pair X and Y
   - The system reports the actual workshop pair connected, whether a loop is formed, and whether it passes through workshop E

## Query Format

- Trial connection query (e.g., asking about IDs A and D):
<query_trial>A,D</query_trial>

- Scheme declaration (e.g., declaring scheme α):
<query_declare>α</query_declare>

- Final edge addition (e.g., laying pipeline between IDs C and F):
<answer>C,F</answer>

## Victory Conditions

Win by satisfying both:
1. Before executing final edge addition, you have received "Correct" confirmation via scheme declaration
2. Final edge addition forms a material flow loop, and the loop contains workshop E

## Failure Conditions

Fail if any of the following occurs:
1. Final edge addition does not form a loop, or forms a loop that does not contain E
2. Execute final edge addition without correct scheme declaration
3. Query format does not meet requirements

Please complete the task with as few queries as possible.
"""

    contextualized_rule_zh_5 = """\
我们来玩一个"隐藏资金链追踪"游戏，规则如下：

经侦系统中有一份已确立的资金转移关系图，涉及7个涉案主体，真实身份为 {{A,B,C,D,E,F,G}}，已查明的资金往来链路为 {{(A,B),(A,C),(B,D),(B,E),(E,F),(E,G)}}。E 是本案的核心嫌疑人。

当前卷宗中的代号被未知置换方案 f 进行了掩码处理。有四个候选的身份还原方案：
- 方案α：A→A, B→B, C→C, D→D, E→E, F→F, G→G
-方案β：A→C, C→A, D→E, E→D, B→B, F→F, G→G
- 方案γ：A→B, B→C, C→A, F→G, G→F, D→D, E→E
- 方案δ：B→E, E→B, D→F, F→D, A→A, C→C, G→G

你的任务是通过问询推断出正确的身份还原方案，并最终确立一条隐蔽的资金转移链，使得形成的资金回流闭环将核心嫌疑人 E 卷入其中。

## 可用的查询类型

每次只能提出一个查询：

1. **试连查询**：询问"如果指控代号 X 和 Y 之间存在资金往来，是否会构成资金回流闭环？"
   - 系统将基于真实身份进行推演。若资金往来已在原链路中，不会成环；否则会成环
   - 回答"会环"或"不会环"

2. **方案宣告**：宣告你认为正确的身份还原方案（α、β、γ 或 δ）
   - 回答"正确"或"错误"

3. **最终加边**：提交最终的指控结论
   - 指定代号对 X 和 Y
   - 系统将反馈真实关联的涉案主体，以及是否构成资金闭环、闭环是否涉及核心嫌疑人 E

## 查询格式

- 试连查询（例如询问代号 A 和 D）：
<query_trial>A,D</query_trial>

- 方案宣告（例如宣告方案 α）：
<query_declare>α</query_declare>

- 最终加边（例如指控代号 C 和 F 之间的资金往来）：
<answer>C,F</answer>

## 胜利条件

同时满足以下条件才能获胜：
1. 在执行最终加边之前，已通过方案宣告获得"正确"确认
2. 最终加边成功形成资金回流闭环，且该闭环涉及核心嫌疑人 E

## 失败条件

满足以下任一条件即失败：
1. 最终加边未构成闭环，或闭环不涉及 E
2. 未进行正确的方案宣告就执行最终加边
3. 提问格式不符合要求

请用尽可能少的查询次数完成任务。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "Hidden Fund Chain Tracking" game. Here are the rules:

The economic investigation system has an established fund transfer relationship graph involving 7 entities with actual identities {{A,B,C,D,E,F,G}} and verified financial links {{(A,B),(A,C),(B,D),(B,E),(E,F),(E,G)}}. E is the core suspect of the case.

The codes in the current dossier are masked by an unknown permutation f mapping to the actual identities. There are four candidate identity restoration schemes:
- Scheme α: A→A, B→B, C→C, D→D, E→E, F→F, G→G
- Scheme β: A→C, C→A, D→E, E→D, B→B, F→F, G→G
- Scheme γ: A→B, B→C, C→A, F→G, G→F, D→D, E→E
- Scheme δ: B→E, E→B, D→F, F→D, A→A, C→C, G→G

Your task is to deduce the correct identity restoration scheme through inquiries, and finally establish a concealed fund transfer link such that the resulting fund return loop involves the core suspect E.

## Available Query Types

You can make one query at a time:

1. **Trial Connection Query**: Ask "If a financial transaction is alleged between codes X and Y, will it constitute a fund return loop?"
   - The system simulates based on the actual identities. If the transaction is already in the verified links, no loop is formed; otherwise, it forms a loop
   - Answer: "Cycle" or "No cycle"

2. **Scheme Declaration**: Declare the correct identity restoration scheme (α, β, γ, or δ)
   - Answer: "Correct" or "Incorrect"

3. **Final Edge Addition**: Submit the final accusation conclusion
   - Specify code pair X and Y
   - The system reports the actual connected entities, whether a fund loop is constituted, and whether it involves core suspect E

## Query Format

- Trial connection query (e.g., asking about codes A and D):
<query_trial>A,D</query_trial>

- Scheme declaration (e.g., declaring scheme α):
<query_declare>α</query_declare>

- Final edge addition (e.g., alleging transaction between codes C and F):
<answer>C,F</answer>

## Victory Conditions

Win by satisfying both:
1. Before executing final edge addition, you have received "Correct" confirmation via scheme declaration
2. Final edge addition forms a fund return loop, and the loop contains core suspect E

## Failure Conditions

Fail if any of the following occurs:
1. Final edge addition does not form a loop, or forms a loop that does not contain E
2. Execute final edge addition without correct scheme declaration
3. Query format does not meet requirements

Please complete the task with as few queries as possible.
"""

    tags = ["answer", "query_trial", "query_declare"]
    
    reasoning_type = "溯因推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"scheme": "α"},
            2: {"scheme": "β"},
            3: {"scheme": "γ"},
            4: {"scheme": "δ"},
            5: {"scheme": "β"},
        },
        "en": {
            1: {"scheme": "α"},
            2: {"scheme": "β"},
            3: {"scheme": "γ"},
            4: {"scheme": "δ"},
            5: {"scheme": "β"},
        },
    }

    def __init__(self, config):
        # 定义树结构（边集）
        self.tree_edges = {
            ('A', 'B'), ('B', 'A'),
            ('A', 'C'), ('C', 'A'),
            ('B', 'D'), ('D', 'B'),
            ('B', 'E'), ('E', 'B'),
            ('E', 'F'), ('F', 'E'),
            ('E', 'G'), ('G', 'E'),
        }
        
        # 定义四个置换方案
        self.permutations = {
            'α': {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G'},
            'β': {'A': 'C', 'B': 'B', 'C': 'A', 'D': 'E', 'E': 'D', 'F': 'F', 'G': 'G'},
            'γ': {'A': 'B', 'B': 'C', 'C': 'A', 'D': 'D', 'E': 'E', 'F': 'G', 'G': 'F'},
            'δ': {'A': 'A', 'B': 'E', 'C': 'C', 'D': 'F', 'E': 'B', 'F': 'D', 'G': 'G'},
        }
        
        self.target_vertex = 'E'  # 目标顶点
        self.declared_correct = False  # 是否已正确宣告
        
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：根据难度选择置换方案"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.correct_scheme = cfg["scheme"]
        self.current_permutation = self.permutations[self.correct_scheme]

    def _find_path(self, start, end):
        """使用 BFS 在树中找到从 start 到 end 的路径"""
        if start == end:
            return [start]
        
        # 构建邻接表
        graph = {}
        for u, v in self.tree_edges:
            if u not in graph:
                graph[u] = []
            graph[u].append(v)
        
        # BFS 寻路
        from collections import deque
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            node, path = queue.popleft()
            if node not in graph:
                continue
            for neighbor in graph[node]:
                if neighbor in visited:
                    continue
                new_path = path + [neighbor]
                if neighbor == end:
                    return new_path
                visited.add(neighbor)
                queue.append((neighbor, new_path))
        
        return None

    def _check_cycle_contains_target(self, v1, v2):
        """检查在树中添加边 (v1, v2) 形成的环是否包含目标顶点 E"""
        path = self._find_path(v1, v2)
        if path is None:
            return False, []
        # 形成环：v1 -> ... -> v2，再回到 v1
        cycle = path + [v1]
        contains_e = self.target_vertex in path
        return contains_e, cycle

    def evaluate(self, parsed_info):
        """评估最终答案：检查是否已正确宣告，以及最终加边是否满足条件"""
        # 必须已经正确宣告
        if not self.declared_correct:
            return False
        
        # 解析最终加边：X,Y
        raw_ans = parsed_info["answer"].strip()
        try:
            parts = [x.strip() for x in raw_ans.split(",")]
            if len(parts) != 2:
                return False
            label_x, label_y = parts
            
            # 检查标签是否有效
            if label_x not in self.current_permutation or label_y not in self.current_permutation:
                return False
            
            # 映射到真实顶点
            real_x = self.current_permutation[label_x]
            real_y = self.current_permutation[label_y]
            
            # 检查是否已存在边（如果存在，则不成环，失败）
            if (real_x, real_y) in self.tree_edges:
                return False
            
            # 检查形成的环是否包含 E
            contains_e, cycle = self._check_cycle_contains_target(real_x, real_y)
            return contains_e
            
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑"""
        is_zh = self.config.language == "zh"
        
        # 优先级：试连查询 > 方案宣告
        if "query_trial" in parsed_info:
            return self._handle_trial_query(parsed_info["query_trial"], is_zh)
        elif "query_declare" in parsed_info:
            return self._handle_declaration(parsed_info["query_declare"], is_zh)
        else:
            raise ValueError("No valid query tag found.")

    def _handle_trial_query(self, query_content, is_zh):
        """处理试连查询"""
        try:
            parts = [x.strip() for x in query_content.split(",")]
            if len(parts) != 2:
                raise ValueError
            
            label_x, label_y = parts
            
            # 检查标签是否有效
            if label_x not in self.current_permutation or label_y not in self.current_permutation:
                return "错误：无效的顶点标签。" if is_zh else "Error: Invalid vertex label."
            
            if label_x == label_y:
                return "错误：两个标签必须不同。" if is_zh else "Error: Labels must be different."
            
            # 映射到真实顶点
            real_x = self.current_permutation[label_x]
            real_y = self.current_permutation[label_y]
            
            # 判断：如果边已存在，则不会环；否则会环（树的性质）
            if (real_x, real_y) in self.tree_edges:
                return "不会环" if is_zh else "No cycle"
            else:
                return "会环" if is_zh else "Cycle"
                
        except:
            return "错误：查询格式无效。" if is_zh else "Error: Invalid query format."

    def _handle_declaration(self, declaration, is_zh):
        """处理方案宣告"""
        declared_scheme = declaration.strip()
        
        if declared_scheme not in self.permutations:
            return "错误：无效的方案名称。" if is_zh else "Error: Invalid scheme name."
        
        if declared_scheme == self.correct_scheme:
            self.declared_correct = True
            return "正确" if is_zh else "Correct"
        else:
            return "错误" if is_zh else "Incorrect"

    def _cf_make_wrong(self, correct: str) -> str:
        """生成错误答案"""
        if self.config.language == "zh":
            if correct == "会环":
                return "不会环"
            elif correct == "不会环":
                return "会环"
            elif correct == "正确":
                return "错误"
            elif correct == "错误":
                return "正确"
        else:
            if correct == "Cycle":
                return "No cycle"
            elif correct == "No cycle":
                return "Cycle"
            elif correct == "Correct":
                return "Incorrect"
            elif correct == "Incorrect":
                return "Correct"
        
        # fallback：若是错误提示信息等其他字符串
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
        results = []
        is_zh = self.config.language == "zh"
        
        # 1. 试连查询 (query_trial)
        labels = sorted(self.current_permutation.keys())
        for label_x, label_y in itertools.combinations(labels, 2):
            query_content = f"{label_x},{label_y}"
            ans = self._handle_trial_query(query_content, is_zh)
            results.append({
                "query": f"<query_trial>{query_content}</query_trial>",
                "answer": ans
            })

        # 2. 方案宣告 (query_declare)
        original_declared_status = self.declared_correct
        
        for scheme in sorted(self.permutations.keys()):
            ans = self._handle_declaration(scheme, is_zh)
            results.append({
                "query": f"<query_declare>{scheme}</query_declare>",
                "answer": ans
            })
            
        # 恢复状态，避免污染游戏进程
        self.declared_correct = original_declared_status
        
        return results

    def step(self, response: str) -> 'GameState':
        """处理一轮游戏交互"""
        try:
            parsed_info = self.parse(response)
            
            # 如果是最终答案
            if "answer" in parsed_info:
                is_zh = self.config.language == "zh"
                
                # 解析最终加边
                raw_ans = parsed_info["answer"].strip()
                try:
                    parts = [x.strip() for x in raw_ans.split(",")]
                    if len(parts) != 2:
                        raise ValueError("Invalid format")
                    
                    label_x, label_y = parts
                    
                    # 检查标签有效性
                    if label_x not in self.current_permutation or label_y not in self.current_permutation:
                        self.state.set_state("failed", "invalid labels")
                        msg = "错误：无效的顶点标签。" if is_zh else "Error: Invalid vertex label."
                        self.state.add_message("user", msg)
                        return self.state
                    
                    # 映射到真实顶点
                    real_x = self.current_permutation[label_x]
                    real_y = self.current_permutation[label_y]
                    
                    # 构建反馈信息
                    feedback = ""
                    if is_zh:
                        feedback += f"实际相连的真实节点对：{real_x}-{real_y}\n"
                    else:
                        feedback += f"Actual vertex pair connected: {real_x}-{real_y}\n"
                    
                    # 检查是否成环
                    if (real_x, real_y) in self.tree_edges:
                        # 边已存在，未成环
                        feedback += "未成环（失败）" if is_zh else "No cycle formed (failed)"
                        self.state.set_state("failed", "no cycle formed")
                        self.state.add_message("user", feedback)
                        return self.state
                    
                    # 会成环，找出环路径
                    contains_e, cycle = self._check_cycle_contains_target(real_x, real_y)
                    cycle_str = "→".join(cycle) if is_zh else "→".join(cycle)
                    
                    if is_zh:
                        feedback += f"成环（成功）\n环路径：{cycle_str}\n"
                        feedback += f"是否包含 E：{'是' if contains_e else '否'}"
                    else:
                        feedback += f"Cycle formed (success)\nCycle path: {cycle_str}\n"
                        feedback += f"Contains E: {'Yes' if contains_e else 'No'}"
                    
                    # 评估是否胜利
                    is_success = self.evaluate(parsed_info)
                    
                    if is_success:
                        self.state.set_state("success", "success")
                    else:
                        if not self.declared_correct:
                            feedback += "\n" + ("（但你未进行正确的方案宣告）" if is_zh else "\n(But you did not make correct scheme declaration)")
                        self.state.set_state("failed", "cycle does not contain E or no declaration")
                    
                    self.state.add_message("user", feedback)
                    
                except Exception as e:
                    self.state.set_state("failed", f"parse error: {str(e)}")
                    msg = "错误：最终加边格式无效。" if is_zh else "Error: Invalid final edge format."
                    self.state.add_message("user", msg)
            
            # 如果是查询
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))
        
        return self.state