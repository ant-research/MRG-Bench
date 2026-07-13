# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   定位查询：序列中第k个位置的元素是什么
# ============================================================

from .base import Game
import random
import re


class PermutationDeductionGame(Game):

    game_rule_zh = """\
我们来玩一个"置换推理"游戏，规则如下：

游戏设定了一个长度为 8 的有序序列 S，其元素两两不同且顺序已知。当前序列 S = [{sequence_str}]。

同时，存在一个隐藏的置换函数 f，它会重新排列索引位置。我已从以下四种候选置换中选择了一种：
- 候选1：保持原顺序
- 候选2：完全反转
- 候选3：部分交换版本1
- 候选4：部分交换版本2

具体选择了哪种置换是保密的。此外，我还秘密选定了一个目标索引 K（K = {target_k}）。

你的目标是：推断出目标位置经过置换后的元素值，即 S[f(K)]。

你可以通过两类查询来收集信息：

1. A类查询：查询索引 i 的元素值，其中 i 只能是 1、4、5 或 8 之一。每局游戏最多使用 1 次。
2. B类查询：查询索引 i 的元素值，其中 i 只能是 2、3、6 或 7 之一。每局游戏至少使用 1 次，至多使用 2 次。

每次查询我会返回该位置经过置换后的元素值。

当你收集到足够信息后，请提交最终答案。你需要给出目标位置的元素值。可选地，你也可以同时声明你推断出的置换类型（候选1到4）。

## 查询与提交答案的格式

每次查询只能包含一个标签。请使用以下 XML 格式：

- A类查询（例如查询索引 1）：
<query_a>1</query_a>

- B类查询（例如查询索引 2）：
<query_b>2</query_b>

提交最终答案时，必须给出目标位置的元素值。格式如下：

仅答案（必须）：
<answer>{{answer_value}}</answer>

或带置换类型（可选）：
<answer>value={{answer_value}}, permutation={{permutation_id}}</answer>

其中 answer_value 是你推断的目标元素，permutation_id 是 1、2、3 或 4。

注意：
- 查询次数有限，请尽可能少地使用查询
- 超出查询限制或格式错误将导致游戏失败
"""

    game_rule_en = """\
Let's play a "Permutation Deduction" game. Here are the rules:

The game has set an ordered sequence S of length 8, with all elements distinct and in a known order. The actual sequence is: S = [{sequence_str}].

Additionally, there exists a hidden permutation function f that rearranges index positions. I have selected one of the following four candidate permutations:
- Candidate 1: Keep original order
- Candidate 2: Complete reversal
- Candidate 3: Partial swap version 1
- Candidate 4: Partial swap version 2

Which permutation was chosen is kept secret. Furthermore, I have secretly selected a target index K (K = {target_k}).

Your goal is: deduce the element value at the target position after permutation, i.e., S[f(K)].

You can collect information through two types of queries:

1. Type A Query: Query the element value at index i, where i can only be 1, 4, 5, or 8. Maximum 1 use per game.
2. Type B Query: Query the element value at index i, where i can only be 2, 3, 6, or 7. Minimum 1 use, maximum 2 uses per game.

Each query will return the element value at that position after permutation.

When you have collected enough information, please submit your final answer. You need to provide the element value at the target position. Optionally, you may also declare the permutation type you deduced (candidate 1 to 4).

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Type A Query (e.g., querying index 1):
<query_a>1</query_a>

- Type B Query (e.g., querying index 2):
<query_b>2</query_b>

When submitting the final answer, you must provide the target position's element value. Format as follows:

Answer only (required):
<answer>{{answer_value}}</answer>

Or with permutation type (optional):
<answer>value={{answer_value}}, permutation={{permutation_id}}</answer>

Where answer_value is your deduced target element, and permutation_id is 1, 2, 3, or 4.

Note:
- Query count is limited, use queries as sparingly as possible
- Exceeding query limits or format errors will result in game failure
"""

    contextualized_rule_zh_1 = """\
欢迎使用“智能交通调度推演系统”。

系统已载入一条包含 8 个关键站点的公交/物流干线 S，各站点元素按已知顺序排列。当前序列 S = [{sequence_str}]。

由于突发路况，指挥中心启用了一个隐藏的调度重排预案 f，它会重新映射各站点的到达顺序。目前有四种候选预案：
- 候选1：保持原路线顺序
- 候选2：完全反向行驶
- 候选3：局部绕行换位预案1
- 候选4：局部绕行换位预案2

具体执行了哪种预案目前属于保密状态。同时，系统后台已锁定了一个高优追踪目标的时间节点 K（K = {target_k}）。

你的任务是：推断出在该目标节点下，实际途径的站点名称，即推算 S[f(K)]。

你可以通过调用两组路网监控来收集线索：

1. A类监控（外围探头）：查询索引 i 的站点元素，其中 i 只能是 1、4、5 或 8 之一。受限于带宽，每局推演最多调用 1 次。
2. B类监控（核心探头）：查询索引 i 的站点元素，其中 i 只能是 2、3、6 或 7 之一。必须至少调用 1 次以确保追踪精度，至多调用 2 次。

每次调用监控，系统会返回该调度节点下实际到达的站点元素。

当你收集到足够信息后，请提交最终推断。你需要给出目标节点的实际站点元素。可选地，你也可以同时声明你推测出的调度预案类型（候选1到4）。

## 查询与提交答案的格式

每次调用监控只能包含一个标签。请使用以下 XML 格式：

- A类监控（例如查询节点 1）：
<query_a>1</query_a>

- B类监控（例如查询节点 2）：
<query_b>2</query_b>

提交最终推断时，必须给出目标节点的站点元素。格式如下：

仅提交结果（必须）：
<answer>{{answer_value}}</answer>

或附带预案类型（可选）：
<answer>value={{answer_value}}, permutation={{permutation_id}}</answer>

其中 answer_value 是你推断的站点元素，permutation_id 是 1、2、3 或 4。

注意：
- 监控调用次数有限，请合理规划
- 超出调用限制或格式错误将导致推演失败
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Intelligent Traffic Dispatch Deduction System".

The system has loaded a transit/logistics main line S containing 8 key stations, arranged in a known order. The actual sequence is: S = [{sequence_str}].

Due to sudden traffic conditions, the command center has activated a hidden routing rearrangement plan f, which alters the arrival sequence of the stations. There are four candidate plans:
- Candidate 1: Keep original route order
- Candidate 2: Complete reverse operation
- Candidate 3: Partial detour swap plan 1
- Candidate 4: Partial detour swap plan 2

Which plan was actually executed is kept secret. Furthermore, the system has locked onto a high-priority tracking target's schedule node K (K = {target_k}).

Your task is: deduce the actual station element reached at the target node, i.e., S[f(K)].

You can collect clues by accessing two groups of network monitors:

1. Type A Monitor (Peripheral Cameras): Query the station element at index i, where i can only be 1, 4, 5, or 8. Due to limited bandwidth, maximum 1 use per deduction.
2. Type B Monitor (Core Cameras): Query the station element at index i, where i can only be 2, 3, 6, or 7. Required to maintain tracking precision (minimum 1 use), maximum 2 uses per deduction.

Each query will return the actual station element at that rearranged node.

When you have collected enough information, please submit your final deduction. You need to provide the station element at the target node. Optionally, you may also declare the dispatch plan type you deduced (candidate 1 to 4).

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Type A Monitor (e.g., querying node 1):
<query_a>1</query_a>

- Type B Monitor (e.g., querying node 2):
<query_b>2</query_b>

When submitting the final deduction, you must provide the target node's station element. Format as follows:

Result only (required):
<answer>{{answer_value}}</answer>

Or with plan type (optional):
<answer>value={{answer_value}}, permutation={{permutation_id}}</answer>

Where answer_value is your deduced station element, and permutation_id is 1, 2, 3, or 4.

Note:
- Monitor queries are limited, use them wisely
- Exceeding query limits or format errors will result in deduction failure
"""

    contextualized_rule_zh_2 = """\
欢迎使用“临床基因序列重组分析系统”。

系统载入了一段长度为 8 的标准基因/蛋白序列 S，序列元素两两不同且原始排序已知。当前序列 S = [{sequence_str}]。

由于样本发生变异，存在一个隐藏的序列重组机制 f，它重新排列了位点索引。目前推测有四种候选突变类型：
- 候选1：保持野生型排序
- 候选2：序列完全倒置
- 候选3：局部易位突变一型
- 候选4：局部易位突变二型

具体发生了哪种重组属于未知状态。此外，系统秘密指定了一个关键的靶向药物结合位点 K（K = {target_k}）。

你的任务是：推断靶向位点突变后的实际氨基酸/碱基元素，即 S[f(K)]。

你可以通过两类测序检验来收集数据：

1. A类检验（外周测序）：查询索引 i 的序列元素，其中 i 只能是 1、4、5 或 8 之一。因试剂昂贵且耗时，每局最多进行 1 次。
2. B类检验（核心靶点测序）：查询索引 i 的序列元素，其中 i 只能是 2、3、6 或 7 之一。为保证诊断准确，每局至少进行 1 次，至多 2 次。

每次测序系统会返回该位点变异后的实际序列元素。

收集足够信息后，请提交最终诊断结论。你需要给出目标靶向位点上的实际元素。可选地，你也可声明你推测的突变类型（候选1到4）。

## 检验与提交结论的格式

每次检验只能包含一个标签。请使用以下 XML 格式：

- A类检验（例如检验位点 1）：
<query_a>1</query_a>

- B类检验（例如检验位点 2）：
<query_b>2</query_b>

提交最终诊断时，必须给出目标位点元素。格式如下：

仅结论（必须）：
<answer>{{answer_value}}</answer>

或附带突变类型（可选）：
<answer>value={{answer_value}}, permutation={{permutation_id}}</answer>

其中 answer_value 是你推断的实际序列元素，permutation_id 是 1、2、3 或 4。

注意：
- 测序次数有限，请审慎选择位点
- 超出检验限制或格式错误将导致分析失败
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Clinical Genomic Sequence Recombination Analysis System".

The system has loaded a standard genetic/protein sequence S of length 8, with distinct elements and a known original order. The actual sequence is: S = [{sequence_str}].

Due to sample mutation, there exists a hidden sequence recombination mechanism f that rearranged the site indices. There are four candidate mutation types:
- Candidate 1: Keep wild-type order
- Candidate 2: Complete sequence inversion
- Candidate 3: Partial translocation type 1
- Candidate 4: Partial translocation type 2

Which recombination occurred is unknown. Furthermore, the system has secretly designated a critical targeted drug binding site K (K = {target_k}).

Your task is: deduce the actual amino acid/base element at the target site after mutation, i.e., S[f(K)].

You can collect data through two types of sequencing assays:

1. Type A Assay (Peripheral Sequencing): Query the sequence element at index i, where i can only be 1, 4, 5, or 8. Due to expensive reagents, maximum 1 use per analysis.
2. Type B Assay (Core Target Sequencing): Query the sequence element at index i, where i can only be 2, 3, 6, or 7. Required for accurate diagnosis (minimum 1 use), maximum 2 uses per analysis.

Each assay will return the actual sequence element at that mutated site.

When you have collected enough data, please submit your final diagnostic conclusion. You need to provide the actual element at the target site. Optionally, you may declare the mutation type you deduced (candidate 1 to 4).

## Assay and Conclusion Format

Each assay must contain only one tag. Use the following XML format:

- Type A Assay (e.g., assaying site 1):
<query_a>1</query_a>

- Type B Assay (e.g., assaying site 2):
<query_b>2</query_b>

When submitting the final diagnosis, you must provide the target site's element. Format as follows:

Conclusion only (required):
<answer>{{answer_value}}</answer>

Or with mutation type (optional):
<answer>value={{answer_value}}, permutation={{permutation_id}}</answer>

Where answer_value is your deduced sequence element, and permutation_id is 1, 2, 3, or 4.

Note:
- Sequencing assays are limited, choose sites carefully
- Exceeding assay limits or format errors will result in analysis failure
"""

    contextualized_rule_zh_3 = """\
欢迎使用“教学计划动态排课系统”。

系统内预设了一学期包含 8 个模块的教学大纲 S，各模块按标准进度排列。当前序列 S = [{sequence_str}]。

为了适应特殊节假日安排，教务处启用了一个隐藏的课表调整方案 f，它打乱了原有的授课周次。目前有四种候选方案：
- 候选1：维持原定教学大纲
- 候选2：完全倒序授课
- 候选3：局部模块对调方案1
- 候选4：局部模块对调方案2

具体选用了哪套方案并未公开。同时，教务处秘密指定了一个作为期中标准考核的教学周次 K（K = {target_k}）。

你的任务是：推断在目标考核周次实际进行的教学模块是什么，即 S[f(K)]。

你可以通过两种形式的教研摸底来收集信息：

1. A类摸底（选修课调研）：查询周次 i 的教学模块，其中 i 只能是 1、4、5 或 8 之一。为免干扰正常教学，最多调研 1 次。
2. B类摸底（核心课检查）：查询周次 i 的教学模块，其中 i 只能是 2、3、6 或 7 之一。此为对齐进度的必要环节，至少进行 1 次，至多 2 次。

每次摸底系统会返回该周次实际排布的教学模块。

摸底结束后，请提交最终推断。你需要明确指出考核周次的实际教学模块。可选地，你也可以声明你推导出的课表调整方案（候选1到4）。

## 摸底与提交格式

每次调研只能包含一个标签。请使用以下 XML 格式：

- A类摸底（例如调研周次 1）：
<query_a>1</query_a>

- B类摸底（例如调研周次 2）：
<query_b>2</query_b>

提交最终结论时，必须给出目标周次的教学模块。格式如下：

仅结论（必须）：
<answer>{{answer_value}}</answer>

或附带调整方案（可选）：
<answer>value={{answer_value}}, permutation={{permutation_id}}</answer>

其中 answer_value 是你推断的教学模块，permutation_id 是 1、2、3 或 4。

注意：
- 摸底次数有限，请合理规划
- 超出调研限制或格式错误将导致排课推演失败
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Dynamic Curriculum Scheduling System".

The system has preset a semester's syllabus S containing 8 teaching modules, arranged in a standard progression. The actual sequence is: S = [{sequence_str}].

To accommodate special holidays, the academic office has activated a hidden schedule adjustment plan f, which rearranges the teaching weeks. There are four candidate plans:
- Candidate 1: Maintain original syllabus
- Candidate 2: Complete reverse teaching order
- Candidate 3: Partial module swap plan 1
- Candidate 4: Partial module swap plan 2

Which plan was actually selected is undisclosed. Meanwhile, the academic office has secretly designated a specific teaching week K as the standardized midterm assessment (K = {target_k}).

Your task is: deduce the actual teaching module conducted during the target assessment week, i.e., S[f(K)].

You can gather information through two types of teaching surveys:

1. Type A Survey (Elective Module Polling): Query the teaching module at week i, where i can only be 1, 4, 5, or 8. To avoid disrupting normal teaching, maximum 1 use.
2. Type B Survey (Core Subject Inspection): Query the teaching module at week i, where i can only be 2, 3, 6, or 7. Required to align progress (minimum 1 use), maximum 2 uses.

Each survey will return the actual teaching module scheduled for that week.

After completing the surveys, please submit your final deduction. You need to identify the exact teaching module for the assessment week. Optionally, you may declare the schedule adjustment plan you deduced (candidate 1 to 4).

## Survey and Conclusion Format

Each survey must contain only one tag. Use the following XML format:

- Type A Survey (e.g., polling week 1):
<query_a>1</query_a>

- Type B Survey (e.g., polling week 2):
<query_b>2</query_b>

When submitting the final conclusion, you must provide the target week's module. Format as follows:

Conclusion only (required):
<answer>{{answer_value}}</answer>

Or with adjustment plan (optional):
<answer>value={{answer_value}}, permutation={{permutation_id}}</answer>

Where answer_value is your deduced teaching module, and permutation_id is 1, 2, 3, or 4.

Note:
- Survey count is limited, plan wisely
- Exceeding survey limits or format errors will result in scheduling deduction failure
"""

    contextualized_rule_zh_4 = """\
欢迎登陆“柔性生产线工序追踪终端”。

系统正监控着一条包含 8 个标准化装配工位的流水线 S，各工序按标准工艺要求排列。当前序列 S = [{sequence_str}]。

因设备维护，产线启用了一个隐藏的工序重排配置 f，改变了流转顺序。有以下四种候选配置：
- 候选1：保持标准流水线配置
- 候选2：完全逆向装配配置
- 候选3：局部工位旁路方案A
- 候选4：局部工位旁路方案B

当前启用的配置是隐藏的。同时，系统设定了一个需要执行高精度质量抽检（QC）的目标工位节点 K（K = {target_k}）。

你的任务是：推算在该质检节点实际加工的工序内容，即推断 S[f(K)].

你可以通过两种质检指令来获取产线数据：

1. A类质检（缓冲区抽检）：查询工位 i 的实际工序，其中 i 只能是 1、4、5 或 8 之一。因影响生产节拍，每批次最多允许 1 次抽检。
2. B类质检（核心加工区审核）：查询工位 i 的实际工序，其中 i 只能是 2、3、6 或 7 之一。作为必检项，至少进行 1 次，至多 2 次。

每次指令返回后，系统将显示该工位实际流转的工序。

确认产线状态后，请提交最终报告。你需要给出目标质检节点上的实际加工工序。可选地，也可上报你推测的产线配置类型（候选1到4）。

## 指令与提交流程格式

每次输入指令只能包含一个标签。请使用以下 XML 格式：

- A类质检（例如抽检工位 1）：
<query_a>1</query_a>

- B类质检（例如抽检工位 2）：
<query_b>2</query_b>

提交最终报告时，必须明确目标节点的实际工序。格式如下：

仅填报工序（必须）：
<answer>{{answer_value}}</answer>

或附带配置类型（可选）：
<answer>value={{answer_value}}, permutation={{permutation_id}}</answer>

其中 answer_value 是你推断的工序内容，permutation_id 是 1、2、3 或 4。

注意：
- 质检指令有限，请避免无意义的停机抽检
- 越权操作或格式错误将导致追踪任务失败
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Flexible Assembly Line Tracking Terminal".

The system is monitoring a production line S containing 8 standardized assembly stations, with processes arranged according to standard requirements. The actual sequence is: S = [{sequence_str}].

Due to equipment maintenance, the line has activated a hidden process rearrangement configuration f, altering the workflow order. There are four candidate configurations:
- Candidate 1: Maintain standard line configuration
- Candidate 2: Complete reverse assembly configuration
- Candidate 3: Partial station bypass plan A
- Candidate 4: Partial station bypass plan B

The active configuration is hidden. Meanwhile, the system has designated a specific station node K for high-precision quality control (QC) sampling (K = {target_k}).

Your task is: deduce the actual process being handled at the target QC node, i.e., S[f(K)].

You can obtain line data through two types of QC commands:

1. Type A QC (Buffer Zone Sampling): Query the actual process at station i, where i can only be 1, 4, 5, or 8. Since it affects production rhythm, maximum 1 sample per batch.
2. Type B QC (Core Processing Area Audit): Query the actual process at station i, where i can only be 2, 3, 6, or 7. As a mandatory check, minimum 1 use, maximum 2 uses.

After each command, the system will display the actual process flowing through that station.

Once the line status is confirmed, please submit your final report. You need to provide the actual process at the target QC node. Optionally, you may also report the line configuration type you deduced (candidate 1 to 4).

## Command and Report Format

Each command must contain only one tag. Use the following XML format:

- Type A QC (e.g., sampling station 1):
<query_a>1</query_a>

- Type B QC (e.g., sampling station 2):
<query_b>2</query_b>

When submitting the final report, you must specify the target node's actual process. Format as follows:

Process only (required):
<answer>{{answer_value}}</answer>

Or with configuration type (optional):
<answer>value={{answer_value}}, permutation={{permutation_id}}</answer>

Where answer_value is your deduced process, and permutation_id is 1, 2, 3, or 4.

Note:
- QC commands are limited, avoid unnecessary line halts
- Unauthorized operations or format errors will result in tracking failure
"""

    contextualized_rule_zh_5 = """\
欢迎进入“合同条款动态审查系统”。

案卷中目前包含一份有 8 项核心条款的法律协议 S，初始条文的优先顺序已知。当前序列 S = [{sequence_str}]。

对方律师提交了一版带有隐藏重排修定的草案 f，调整了条款的绝对顺位。目前排查出四种可能的修定模式：
- 候选1：维持原草案格式
- 候选2：优先权完全倒置
- 候选3：局部条款重组版本1
- 候选4：局部条款重组版本2

实际采用的修定模式尚未核实。同时，我方合伙人秘密锁定了一个极具争议的条款序号 K（K = {target_k}），作为谈判突破口。

你的任务是：推断在对方修定后的草案中，落入争议序号 K 的实际条款内容是什么，即明确 S[f(K)]。

你可以通过调取两类法务尽职调查程序来审核草案：

1. A类审查（格式条款审查）：调阅序号 i 的条款内容，其中 i 只能是 1、4、5 或 8 之一。受限于计费工时，最多仅允许调阅 1 次。
2. B类审查（实质条款尽调）：调阅序号 i 的条款内容，其中 i 只能是 2、3、6 或 7 之一。此为尽调必要程序，必须至少调阅 1 次，至多 2 次。

系统将按指令返回修定后草案中对应序号下的具体条款。

查清法务事实后，请出具最终审查结论。你必须给出目标争议序号下的实际条款。可选地，也可附加上你确定的修定模式（候选1到4）。

## 审查与结论出具格式

每次调阅只能使用一个标签。请使用以下 XML 格式：

- A类审查（例如审查序号 1）：
<query_a>1</query_a>

- B类审查（例如审查序号 2）：
<query_b>2</query_b>

出具最终审查结论时，必须提供目标序号下的条款。格式如下：

仅核心条款（必须）：
<answer>{{answer_value}}</answer>

或附带修定模式（可选）：
<answer>value={{answer_value}}, permutation={{permutation_id}}</answer>

其中 answer_value 是你推断的条款内容，permutation_id 是 1、2、3 或 4。

注意：
- 审查次数受到法务预算限制，请精简调阅
- 违反审查程序或格式错误将导致系统闭卷并判定审查失败
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Dynamic Contract Clause Review System".

The dossier currently contains a legal agreement S with 8 core clauses, where the initial priority order is known. The actual sequence is: S = [{sequence_str}].

Opposing counsel has submitted a draft f with hidden rearrangement revisions, altering the absolute priority of the clauses. We have identified four possible revision patterns:
- Candidate 1: Maintain original draft format
- Candidate 2: Complete inversion of priorities
- Candidate 3: Partial clause reorganization version 1
- Candidate 4: Partial clause reorganization version 2

The actual revision pattern applied is unverified. Meanwhile, our managing partner has secretly locked onto a highly disputed clause index K (K = {target_k}) as a negotiation breakthrough point.

Your task is: deduce the actual clause content falling under the disputed index K in the revised draft, i.e., pinpoint S[f(K)].

You can audit the draft by invoking two types of legal due diligence procedures:

1. Type A Review (Boilerplate Clause Review): Retrieve the clause content at index i, where i can only be 1, 4, 5, or 8. Due to billable hour limits, maximum 1 retrieval allowed.
2. Type B Review (Substantive Clause Due Diligence): Retrieve the clause content at index i, where i can only be 2, 3, 6, or 7. As a mandatory diligence step, minimum 1 retrieval, maximum 2 retrievals.

The system will return the specific clause at that index in the revised draft based on your command.

Once the legal facts are clear, please issue your final review conclusion. You must provide the actual clause under the target disputed index. Optionally, you may append the revision pattern you determined (candidate 1 to 4).

## Review and Conclusion Format

Each retrieval must use only one tag. Use the following XML format:

- Type A Review (e.g., reviewing index 1):
<query_a>1</query_a>

- Type B Review (e.g., reviewing index 2):
<query_b>2</query_b>

When issuing the final review conclusion, you must provide the clause under the target index. Format as follows:

Core clause only (required):
<answer>{{answer_value}}</answer>

Or with revision pattern (optional):
<answer>value={{answer_value}}, permutation={{permutation_id}}</answer>

Where answer_value is your deduced clause content, and permutation_id is 1, 2, 3, or 4.

Note:
- Review actions are limited by the legal budget, keep retrievals concise
- Violating review procedures or format errors will close the dossier and result in review failure
"""

    tags = ["answer", "query_a", "query_b"]
    
    reasoning_type = "溯因推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "sequence": ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛"],
                "target_k": 2,
                "permutation": 1,  # f1 = [1,2,3,4,5,6,7,8]
            },
            2: {
                "sequence": ["春", "夏", "秋", "冬", "梅", "兰", "竹", "菊"],
                "target_k": 3,
                "permutation": 2,  # f2 = [8,7,6,5,4,3,2,1]
            },
            3: {
                "sequence": ["子", "丑", "寅", "卯", "辰", "巳", "午", "未"],
                "target_k": 6,
                "permutation": 3,  # f3 = [1,3,2,4,5,7,6,8]
            },
            4: {
                "sequence": ["金", "木", "水", "火", "土", "日", "月", "星"],
                "target_k": 7,
                "permutation": 4,  # f4 = [8,6,7,5,4,2,3,1]
            },
            5: {
                "sequence": ["天", "地", "玄", "黄", "宇", "宙", "洪", "荒"],
                "target_k": 6,
                "permutation": 4,  # f4 = [8,6,7,5,4,2,3,1]
            },
        },
        "en": {
            1: {
                "sequence": ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta"],
                "target_k": 2,
                "permutation": 1,
            },
            2: {
                "sequence": ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"],
                "target_k": 3,
                "permutation": 2,
            },
            3: {
                "sequence": ["Red", "Orange", "Yellow", "Green", "Blue", "Indigo", "Violet", "Purple"],
                "target_k": 6,
                "permutation": 3,
            },
            4: {
                "sequence": ["Diamond", "Heart", "Club", "Spade", "King", "Queen", "Jack", "Ace"],
                "target_k": 7,
                "permutation": 4,
            },
            5: {
                "sequence": ["North", "South", "East", "West", "Up", "Down", "Left", "Right"],
                "target_k": 6,
                "permutation": 4,
            },
        },
    }

    # 定义四种置换函数
    PERMUTATIONS = {
        1: [1, 2, 3, 4, 5, 6, 7, 8],      # f1: 保持原顺序
        2: [8, 7, 6, 5, 4, 3, 2, 1],      # f2: 完全反转
        3: [1, 3, 2, 4, 5, 7, 6, 8],      # f3: 部分交换版本1
        4: [8, 6, 7, 5, 4, 2, 3, 1],      # f4: 部分交换版本2
    }

    def __init__(self, config):
        # 查询计数器初始化
        self.query_a_count = 0
        self.query_b_count = 0
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 设置序列、目标索引和置换
        self.sequence = cfg["sequence"]  # S[1..8]，索引从1开始
        self.target_k = cfg["target_k"]  # 目标索引 K
        self.permutation_id = cfg["permutation"]  # 置换类型
        self.permutation = self.PERMUTATIONS[self.permutation_id]  # 实际置换映射
        
        # 计算正确答案：S[f(K)]
        # 注意：序列索引从0开始，但游戏中索引从1开始
        permuted_index = self.permutation[self.target_k - 1]  # f(K)
        self.correct_answer = self.sequence[permuted_index - 1]  # S[f(K)]
        
        # 游戏信息用于格式化规则
        self._game_info["n"] = len(self.sequence)
        self._game_info["sequence_str"] = ", ".join(self.sequence)
        self._game_info["target_k"] = self.target_k

    def evaluate(self, parsed_info):
        """评估答案是否正确"""
        if self.query_b_count < 1:
            raise ValueError("insufficient B queries")

        raw_ans = parsed_info["answer"].strip()
        
        # 尝试解析带置换类型的答案格式
        if "value=" in raw_ans:
            try:
                parts = [x.strip() for x in raw_ans.split(",")]
                ans_dict = {}
                for part in parts:
                    if "=" in part:
                        k, v = part.split("=", 1)
                        ans_dict[k.strip()] = v.strip()
                
                answer_value = ans_dict.get("value", "")
                permutation_claim = ans_dict.get("permutation", "")
                
                # 检查答案值
                if answer_value != self.correct_answer:
                    return False
                
                # 如果声明了置换类型，也检查（可选，不影响主要判定）
                if permutation_claim:
                    try:
                        perm_id = int(permutation_claim)
                        if perm_id != self.permutation_id:
                            # 置换类型错误不影响主要答案的正确性，但可以记录
                            pass
                    except:
                        pass
                
                return True
            except:
                return False
        else:
            # 简单答案格式，直接比较
            return raw_ans == self.correct_answer

    def _cf_core_produce(self, parsed_info):
        """处理查询并返回响应（原始逻辑）"""
        lang = self.config.language
        
        # 处理 A 类查询
        if "query_a" in parsed_info:
            try:
                idx = int(parsed_info["query_a"].strip())
            except:
                raise ValueError("错误：索引格式无效。" if lang == "zh" else "Error: Invalid index format.")
            
            # 检查索引是否在允许范围内
            if idx not in [1, 4, 5, 8]:
                raise ValueError("错误：A类查询索引必须是 1、4、5 或 8。" if lang == "zh" else "Error: Type A query index must be 1, 4, 5, or 8.")
            
            # 检查查询次数限制
            if self.query_a_count >= 1:
                raise ValueError("exceeded A query limit")
            
            self.query_a_count += 1
            
            # 返回 S[f(idx)]
            permuted_idx = self.permutation[idx - 1]
            element = self.sequence[permuted_idx - 1]
            
            return f"索引 {idx} 的元素是：{element}" if lang == "zh" else f"Element at index {idx}: {element}"
        
        # 处理 B 类查询
        elif "query_b" in parsed_info:
            try:
                idx = int(parsed_info["query_b"].strip())
            except:
                raise ValueError("错误：索引格式无效。" if lang == "zh" else "Error: Invalid index format.")
            
            # 检查索引是否在允许范围内
            if idx not in [2, 3, 6, 7]:
                raise ValueError("错误：B类查询索引必须是 2、3、6 或 7。" if lang == "zh" else "Error: Type B query index must be 2, 3, 6, or 7.")
            
            # 检查查询次数限制
            if self.query_b_count >= 2:
                raise ValueError("exceeded B query limit")
            
            self.query_b_count += 1
            
            # 返回 S[f(idx)]
            permuted_idx = self.permutation[idx - 1]
            element = self.sequence[permuted_idx - 1]
            
            return f"索引 {idx} 的元素是：{element}" if lang == "zh" else f"Element at index {idx}: {element}"
        
        else:
            raise ValueError("No valid query tag found.")

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
        lang = self.config.language

        # A类查询允许的索引
        indices_a = [1, 4, 5, 8]
        # B类查询允许的索引
        indices_b = [2, 3, 6, 7]

        # 枚举 A 类查询
        for idx in indices_a:
            query_str = f"<query_a>{idx}</query_a>"
            
            # 逻辑计算：S[f(idx)]
            permuted_idx = self.permutation[idx - 1]
            element = self.sequence[permuted_idx - 1]
            
            if lang == "zh":
                ans = f"索引 {idx} 的元素是：{element}"
            else:
                ans = f"Element at index {idx}: {element}"
            
            results.append({
                "query": query_str,
                "answer": ans
            })

        # 枚举 B 类查询
        for idx in indices_b:
            query_str = f"<query_b>{idx}</query_b>"
            
            # 逻辑计算：S[f(idx)]
            permuted_idx = self.permutation[idx - 1]
            element = self.sequence[permuted_idx - 1]
            
            if lang == "zh":
                ans = f"索引 {idx} 的元素是：{element}"
            else:
                ans = f"Element at index {idx}: {element}"
            
            results.append({
                "query": query_str,
                "answer": ans
            })

        return results

    def _cf_make_wrong(self, correct: str) -> str:
        lang = self.config.language
        
        # 从响应中提取实际元素
        if lang == "zh":
            # 格式："索引 X 的元素是：ELEMENT"
            match = re.search(r'：(.+)$', correct)
        else:
            # 格式："Element at index X: ELEMENT"
            match = re.search(r':\s*(.+)$', correct)
        
        if match:
            actual_element = match.group(1).strip()
            # 从序列中选一个不同的元素
            candidates = [e for e in self.sequence if e != actual_element]
            if candidates:
                wrong_element = random.choice(candidates)
                return correct.replace(actual_element, wrong_element)
        
        # fallback
        return correct + "_WRONG"