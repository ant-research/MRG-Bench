from .base import Game
import re
import itertools

class PermutationReconstructionGame(Game):

    game_rule_zh = """\
我们现在来玩一个"排列重构"的推理游戏，规则如下：

游戏设定了一个长度为 {n} 的位置序列（位置编号为 1 到 {n}），以及 {n} 个互不相同的元素（元素标识为 {elements}）。我已秘密确定了一个目标排列 S，将每个元素放置到某个位置上（每个位置恰好一个元素），这个排列在整个游戏过程中保持不变。

你的目标是通过查询推断出这个未知的目标排列 S。你可以进行以下两类查询：

1. **完整排列查询**：提交一个完整的排列 X（将所有元素分配到所有位置）。我会返回一个非负整数 k，表示将排列 X 通过最少的"两两交换"次数变换为目标排列 S 所需的步数。两两交换是指选择两个位置并交换其上的元素。

2. **交换查询**：基于你最近一次提交的完整排列 X，指定交换其中两个位置 i 和 j 上的元素，我会返回交换后新排列的 k 值（即新排列到目标排列的最少交换次数）。

每次查询都会消耗 1 次查询预算。当你确信已推断出目标排列时，可以提交最终答案进行宣告。宣告操作不消耗查询预算。

**关于反馈值 k 的数学定义**：
反馈值 k 等于将你的排列 X 变换为目标排列 S 所需的最少两两交换次数。从数学上讲，这等于 N 减去从 X 到 S 的位置映射置换的环数量。当 k = 0 时，表示你的排列与目标排列完全一致。

每次只能包含一个查询或答案标签。请使用以下 XML 格式：

- 完整排列查询（例如提交排列：位置1放元素A，位置2放元素B，位置3放元素C）：
<query_full>A,B,C</query_full>

- 交换查询（例如交换位置 1 和位置 3 的元素）：
<query_swap>1,3</query_swap>

- 提交最终答案（例如宣告目标排列为：位置1放元素A，位置2放元素B，位置3放元素C）：
<answer>A,B,C</answer>

注意：
- 排列格式为逗号分隔的元素序列，按位置顺序排列
- 位置编号从 1 开始
- 交换查询必须在至少进行过一次完整排列查询之后才能使用
- 请尽可能少地使用查询次数来找到目标排列
"""

    game_rule_en = """\
Let's play a "Permutation Reconstruction" deduction game. Here are the rules:

The game has a position sequence of length {n} (positions numbered 1 to {n}), and {n} distinct elements (element identifiers: {elements}). I have secretly determined a target permutation S, placing each element at a specific position (exactly one element per position). This permutation remains unchanged throughout the game.

Your goal is to infer this unknown target permutation S through queries. You can perform two types of queries:

1. **Full Permutation Query**: Submit a complete permutation X (assigning all elements to all positions). I will return a non-negative integer k, representing the minimum number of "pairwise swaps" needed to transform permutation X into the target permutation S. A pairwise swap means selecting two positions and swapping the elements on them.

2. **Swap Query**: Based on your most recently submitted full permutation X, specify two positions i and j to swap their elements. I will return the k value for the new permutation (i.e., the minimum swap count from the new permutation to the target permutation).

Each query consumes 1 query budget. When you are confident you have inferred the target permutation, you can submit a final answer for declaration. The declaration operation does not consume query budget.

**Mathematical definition of feedback value k**:
The feedback value k equals the minimum number of pairwise swaps needed to transform your permutation X into the target permutation S. Mathematically, this equals N minus the number of cycles in the position mapping permutation from X to S. When k = 0, it means your permutation is identical to the target permutation.

Each submission must contain only one query or answer tag. Use the following XML format:

- Full Permutation Query (e.g., submitting permutation: element A at position 1, element B at position 2, element C at position 3):
<query_full>A,B,C</query_full>

- Swap Query (e.g., swapping elements at positions 1 and 3):
<query_swap>1,3</query_swap>

- Submit Final Answer (e.g., declaring target permutation: element A at position 1, element B at position 2, element C at position 3):
<answer>A,B,C</answer>

Notes:
- Permutation format is a comma-separated sequence of elements, ordered by position
- Position numbering starts from 1
- Swap queries can only be used after at least one full permutation query has been performed
- Please use as few queries as possible to find the target permutation
"""

    contextualized_rule_zh_1 = """\
我们现在进行一项"列车编组重构"的调度推理任务，规则如下：

调度中心设定了一个长度为 {n} 的车厢位序列（位置编号为 1 到 {n}），以及 {n} 节特殊物资车厢（车厢标识为 {elements}）。中心已秘密确定了一个最佳安全编组 S，将每节车厢停放到特定位置上（每个位置恰好一节车厢），这个编组在整个调度期间保持绝对不变。

你的目标是通过模拟调度推断出这个未知的最佳编组 S。你可以发送以下两类调度指令：

1. **完整编组模拟**：提交一个完整的编组方案 X。系统会返回一个非负整数 k，表示将当前方案 X 通过最少的"两两车厢调换"操作变换为最佳编组 S 所需的调车步数。两两调换是指选择两个位置并对调其上的车厢。

2. **调换测试**：基于你最近一次提交的完整方案 X，指定调换其中两个位置 i 和 j 上的车厢，系统会返回新方案所需的调车步数 k。

每次指令都会消耗 1 次调度预算。当你确信已推断出最佳编组时，可以提交最终方案进行执行。执行操作不消耗调度预算。

**关于反馈值 k 的数学定义**：
反馈值 k 等于将方案 X 变换为最佳编组 S 所需的最少车厢对调次数。从数学上讲，这等于 N 减去从 X 到 S 的位置映射置换的环数量。当 k = 0 时，表示方案完全符合安全要求。

每次只能包含一个指令或答案标签。请使用以下 XML 格式：

- 完整编组模拟（例如位置1停靠A，位置2停靠B，位置3停靠C）：
<query_full>A,B,C</query_full>

- 调换测试（例如对调位置 1 和位置 3 的车厢）：
<query_swap>1,3</query_swap>

- 提交最终方案：
<answer>A,B,C</answer>

注意：
- 编组格式为逗号分隔的车厢序列，按位置顺序排列
- 位置编号从 1 开始
- 调换测试必须在至少进行过一次完整编组模拟之后才能使用
- 请尽可能少地使用预算来确定最佳编组
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's conduct a "Train Consist Reconstruction" dispatch task. Here are the rules:

The dispatch center has set a sequence of {n} carriage slots (slots numbered 1 to {n}), and {n} special cargo carriages (identifiers: {elements}). The center has secretly determined an optimal safety configuration S, assigning each carriage to a specific slot (exactly one per slot). This configuration remains completely unchanged throughout the operation.

Your goal is to infer this unknown optimal configuration S through dispatch simulations. You can issue two types of commands:

1. **Full Consist Simulation**: Submit a complete configuration X. The system will return a non-negative integer k, representing the minimum number of "pairwise carriage swaps" (shunting operations) needed to transform configuration X into the optimal configuration S.

2. **Swap Test**: Based on your most recently submitted full configuration X, specify two slots i and j to swap their carriages. The system will return the k value for the new configuration.

Each simulation consumes 1 dispatch budget. When you are confident you have inferred the optimal configuration, you can submit the final plan for execution. The execution operation does not consume budget.

**Mathematical definition of feedback value k**:
The feedback value k equals the minimum number of pairwise swaps needed to transform configuration X into the optimal configuration S. Mathematically, this equals N minus the number of cycles in the carriage mapping permutation from X to S. When k = 0, your configuration perfectly meets safety requirements.

Each submission must contain only one command or answer tag. Use the following XML format:

- Full Consist Simulation:
<query_full>A,B,C</query_full>

- Swap Test:
<query_swap>1,3</query_swap>

- Submit Final Plan:
<answer>A,B,C</answer>

Notes:
- Format is a comma-separated sequence of carriage identifiers, ordered by slot
- Slot numbering starts from 1
- Swap tests can only be used after at least one full consist simulation
- Please minimize the use of dispatch budgets
"""

    contextualized_rule_zh_2 = """\
我们现在进行一项"靶向基因重组"的医学分析任务，规则如下：

实验室设定了一个长度为 {n} 的基因座序列（编号从 1 到 {n}），以及 {n} 个特定的有效基因片段（标识为 {elements}）。系统已隐性锁定了一个健康的靶向序列 S，将每个基因片段定位到特定基因座上，此靶序列在分析中保持绝对稳定。

你的目标是通过化验测序推断出这个未知的靶向序列 S。你可以进行两类化验：

1. **全序列测序**：提交一个完整的基因序列样本 X。仪器会返回一个非负整数 k，表示将样本 X 通过最少的"基因位点两两互换"（移码修复）变换为靶序列 S 所需的生化反应步数。

2. **靶向互换化验**：基于你最近一次提交的全序列 X，指定诱发其中两个基因座 i 和 j 上的片段发生互换，仪器会返回新序列的修复步数 k。

每次化验消耗 1 次反应预算。确信推断出靶向序列时，可提交最终报告。最终提交不消耗预算。

**关于反馈值 k 的数学定义**：
反馈值 k 等于将样本 X 变换为靶序列 S 所需的最少互换次数。从数学上讲，这等于 N 减去从 X 到 S 的基因座映射置换的环数量。当 k = 0 时，代表样本完全健康。

每次只能包含一个化验或答案标签。请使用以下 XML 格式：

- 全序列测序（例如基因座1置换A，基因座2置换B，基因座3置换C）：
<query_full>A,B,C</query_full>

- 靶向互换化验（例如互换基因座 1 和基因座 3 的片段）：
<query_swap>1,3</query_swap>

- 提交最终靶向序列报告：
<answer>A,B,C</answer>

注意：
- 序列格式为逗号分隔的片段组合，按基因座顺序排列
- 基因座编号从 1 开始
- 互换化验必须在至少进行过一次全序列测序之后才能使用
- 请尽可能少地消耗预算以得出结果
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct a "Targeted Gene Recombination" medical analysis task. Here are the rules:

The laboratory has set a locus sequence of length {n} (numbered 1 to {n}), and {n} specific effective gene segments (identifiers: {elements}). The system has secretly locked a healthy target sequence S, mapping each gene segment to a specific locus. This target sequence remains completely stable during analysis.

Your goal is to infer this unknown target sequence S through assays. You can perform two types of assays:

1. **Full Sequence Assay**: Submit a complete genetic sequence sample X. The instrument will return a non-negative integer k, representing the minimum number of "pairwise locus swaps" (frameshift repairs) needed to transform sample X into the healthy target sequence S.

2. **Targeted Swap Assay**: Based on your most recently submitted full sequence X, specify two loci i and j to induce a segment swap. The instrument will return the repair steps k for the new sequence.

Each assay consumes 1 reaction budget. When you are confident you have inferred the target sequence, you can submit the final report. The final submission does not consume budget.

**Mathematical definition of feedback value k**:
The feedback value k equals the minimum number of pairwise swaps needed to transform sample X into the target S. Mathematically, this equals N minus the number of cycles in the locus mapping permutation from X to S. When k = 0, the sample is perfectly healthy.

Each submission must contain only one assay or answer tag. Use the following XML format:

- Full Sequence Assay:
<query_full>A,B,C</query_full>

- Targeted Swap Assay:
<query_swap>1,3</query_swap>

- Submit Final Report:
<answer>A,B,C</answer>

Notes:
- Sequence format is a comma-separated list of segments, ordered by locus
- Locus numbering starts from 1
- Swap assays can only be used after at least one full sequence assay
- Please minimize the use of budgets to find the target sequence
"""

    contextualized_rule_zh_3 = """\
我们现在进行一项"教务课程排表"的优化推理任务，规则如下：

教务处设定了一个长度为 {n} 的每日课时序列（节次编号 1 到 {n}），以及 {n} 门核心学科（学科标识为 {elements}）。专家组已秘密制定了一个符合学生认知规律的最优课表 S，将每门学科安排在特定的节次，该最优解在整个排课演算过程中保持不变。

你的目标是通过系统排演推断出这个最优课表 S。你可以进行以下两类排演：

1. **全天候排表查询**：提交一个完整的日课表方案 X。评估系统会返回一个非负整数 k，表示将方案 X 通过最少的"两门课程对调"次数变换为最优课表 S 所需的调整步数。

2. **调课查询**：基于你最近一次提交的全天候课表 X，指定对调其中两个节次 i 和 j 上的学科，系统会返回新课表所需的调整步数 k。

每次排演查询会消耗 1 次算力预算。当你确信已推断出最优课表时，可提交最终定稿。定稿提交不消耗预算。

**关于反馈值 k 的数学定义**：
反馈值 k 等于将方案 X 变换为最优课表 S 所需的最少课程对调次数。从数学上讲，这等于 N 减去从 X 到 S 的课时映射置换的环数量。当 k = 0 时，表示排表完美契合认知规律。

每次只能包含一个查询或答案标签。请使用以下 XML 格式：

- 全天候排表查询（例如第1节安排A，第2节安排B，第3节安排C）：
<query_full>A,B,C</query_full>

- 调课查询（例如对调第 1 节和第 3 节的课程）：
<query_swap>1,3</query_swap>

- 提交最终定稿：
<answer>A,B,C</answer>

注意：
- 课表格式为逗号分隔的学科序列，按节次顺序排列
- 节次编号从 1 开始
- 调课查询必须在至少进行过一次全天候排表查询之后才能使用
- 请用尽可能少的算力找到最优课表
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's perform a "Curriculum Scheduling" optimization deduction task. Here are the rules:

The academic office has set a daily period sequence of length {n} (numbered 1 to {n}), and {n} core subjects (identifiers: {elements}). The expert panel has secretly established a cognitively optimal schedule S, assigning each subject to a specific period. This optimal schedule remains unchanged throughout the evaluation process.

Your goal is to infer this unknown optimal schedule S through system rehearsals. You can perform two types of queries:

1. **Full-Day Schedule Query**: Submit a complete daily schedule X. The evaluation system will return a non-negative integer k, representing the minimum number of "pairwise subject swaps" needed to transform schedule X into the optimal schedule S.

2. **Class Swap Query**: Based on your most recently submitted schedule X, specify two periods i and j to swap their subjects. The system will return the adjustment steps k for the new schedule.

Each query consumes 1 computational budget. When you are confident you have inferred the optimal schedule, you can submit the finalized draft. Final submission does not consume budget.

**Mathematical definition of feedback value k**:
The feedback value k equals the minimum number of pairwise swaps needed to transform schedule X into the optimal schedule S. Mathematically, this equals N minus the number of cycles in the period mapping permutation from X to S. When k = 0, the schedule perfectly matches cognitive rules.

Each submission must contain only one query or answer tag. Use the following XML format:

- Full-Day Schedule Query:
<query_full>A,B,C</query_full>

- Class Swap Query:
<query_swap>1,3</query_swap>

- Submit Finalized Draft:
<answer>A,B,C</answer>

Notes:
- Schedule format is a comma-separated sequence of subjects, ordered by period
- Period numbering starts from 1
- Swap queries can only be used after at least one full schedule query
- Please minimize the use of budgets to find the optimal schedule
"""

    contextualized_rule_zh_4 = """\
我们现在进行一项"柔性装配线重构"的工程调试任务，规则如下：

车间设定了一个长度为 {n} 的工位序列（工位编号 1 到 {n}），以及 {n} 台专用自动化设备（设备标识为 {elements}）。总工程师秘密预设了一个零缺陷的理想节拍布局 S，将每台设备安置在特定工位上，该布局在调试阶段保持绝对恒定。

你的目标是通过测试推断出这个理想布局 S。你可以进行两类测试操作：

1. **全产线调试**：提交一个完整的产线布局方案 X。控制中枢会返回一个非负整数 k，表示将布局 X 通过最少的"两两设备搬移对调"次数变换为理想布局 S 所需的物理重构步数。

2. **局部对调测试**：基于你最近一次提交的全产线布局 X，指定对调其中两个工位 i 和 j 上的设备，中枢将返回新布局的重构步数 k。

每次测试会消耗 1 次试产配额。确信掌握理想布局时，可提交最终蓝图。最终提交不消耗试产配额。

**关于反馈值 k 的数学定义**：
反馈值 k 等于将布局 X 变换为理想布局 S 所需的最少设备对调次数。从数学上讲，这等于 N 减去从 X 到 S 的设备映射置换的环数量。当 k = 0 时，产线达到零缺陷节拍。

每次只能包含一个测试或蓝图标签。请使用以下 XML 格式：

- 全产线调试（例如工位1放A，工位2放B，工位3放C）：
<query_full>A,B,C</query_full>

- 局部对调测试（例如对调工位 1 和工位 3 的设备）：
<query_swap>1,3</query_swap>

- 提交最终蓝图：
<answer>A,B,C</answer>

注意：
- 布局格式为逗号分隔的设备序列，按工位顺序排列
- 工位编号从 1 开始
- 局部对调测试必须在至少进行过一次全产线调试之后才能使用
- 请尽可能少地消耗试产配额找到最佳节拍
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's conduct a "Flexible Assembly Line Reconstruction" engineering debug task. Here are the rules:

The workshop has set a sequence of {n} workstations (numbered 1 to {n}), and {n} specialized automated machines (identifiers: {elements}). The chief engineer has secretly preset a zero-defect ideal takt layout S, installing each machine at a specific workstation. This layout remains absolutely constant during the debug phase.

Your goal is to infer this ideal layout S through testing. You can perform two types of tests:

1. **Full-Line Debug**: Submit a complete line layout X. The control hub will return a non-negative integer k, representing the minimum number of "pairwise machine relocations" needed to transform layout X into the ideal layout S.

2. **Local Swap Test**: Based on your most recently submitted full layout X, specify two workstations i and j to swap their machines. The hub will return the reconstruction steps k for the new layout.

Each test consumes 1 trial quota. When you are confident you have mastered the ideal layout, you can submit the final blueprint. Blueprint submission does not consume quota.

**Mathematical definition of feedback value k**:
The feedback value k equals the minimum number of pairwise swaps needed to transform layout X into the ideal layout S. Mathematically, this equals N minus the number of cycles in the machine mapping permutation from X to S. When k = 0, the assembly line reaches a zero-defect takt.

Each submission must contain only one test or blueprint tag. Use the following XML format:

- Full-Line Debug:
<query_full>A,B,C</query_full>

- Local Swap Test:
<query_swap>1,3</query_swap>

- Submit Final Blueprint:
<answer>A,B,C</answer>

Notes:
- Layout format is a comma-separated sequence of machines, ordered by workstation
- Workstation numbering starts from 1
- Local swap tests can only be used after at least one full-line debug
- Please minimize the use of trial quotas
"""

    contextualized_rule_zh_5 = """\
我们现在进行一项"法庭证据链重构"的推理分析任务，规则如下：

卷宗中记录了一个长度为 {n} 的案发时间节点序列（节点编号 1 到 {n}），以及 {n} 份决定性的关键证据（证据标识为 {elements}）。法庭已基于绝对事实秘密确立了一条客观真相序列 S，将每份证据归位到特定的时间节点上，该事实真相在整个庭审推演中不可动摇。

你的目标是通过质证推断出这条真相序列 S。你可以进行两类质证申请：

1. **完整证据链推演**：提交一个完整的证据排序假设 X。法官会返回一个非负整数 k，表示将假设 X 通过最少的"两份证据位置互换"次数纠正为真相序列 S 所需的逻辑重构步数。

2. **倒转质证**：基于你最近一次提交的完整假设 X，指定互换其中两个节点 i 和 j 上的证据，法官会返回新假设所需的逻辑重构步数 k。

每次质证申请消耗 1 次庭审质证权利。当你确信彻底还原了事实真相时，可提交最终结论。提交最终结论不消耗权利。

**关于反馈值 k 的数学定义**：
反馈值 k 等于将假设 X 变换为真相序列 S 所需的最少证据互换次数。从数学上讲，这等于 N 减去从 X 到 S 的节点映射置换的环数量。当 k = 0 时，代表证据链完美还原真相。

每次只能包含一个质证申请或结论标签。请使用以下 XML 格式：

- 完整证据链推演（例如节点1提交A，节点2提交B，节点3提交C）：
<query_full>A,B,C</query_full>

- 倒转质证（例如互换节点 1 和节点 3 上的证据）：
<query_swap>1,3</query_swap>

- 提交最终法庭结论：
<answer>A,B,C</answer>

注意：
- 序列格式为逗号分隔的证据组合，按时间节点顺序排列
- 节点编号从 1 开始
- 倒转质证必须在至少进行过一次完整证据链推演之后才能使用
- 请以最精简的质证次数找回案发真相
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's conduct a "Court Evidence Chain Reconstruction" analytical task. Here are the rules:

The case file contains a sequence of length {n} chronological event nodes (numbered 1 to {n}), and {n} decisive pieces of evidence (identifiers: {elements}). The court has secretly established an objective truth sequence S based on absolute facts, anchoring each evidence to a specific event node. This factual truth remains unshakable throughout the trial.

Your goal is to infer this truth sequence S through cross-examination. You can apply for two types of examinations:

1. **Full Chain Deduction**: Submit a complete hypothetical evidence sequence X. The judge will return a non-negative integer k, representing the minimum number of "pairwise evidence swaps" needed to correct hypothesis X into the truth sequence S.

2. **Reversal Examination**: Based on your most recently submitted hypothesis X, specify two nodes i and j to swap their evidence. The judge will return the logical correction steps k for the new hypothesis.

Each application consumes 1 examination right. When you are confident you have fully restored the facts, you can submit the final conclusion. Submitting the conclusion does not consume your rights.

**Mathematical definition of feedback value k**:
The feedback value k equals the minimum number of evidence swaps needed to transform hypothesis X into truth sequence S. Mathematically, this equals N minus the number of cycles in the node mapping permutation from X to S. When k = 0, the evidence chain perfectly restores the truth.

Each submission must contain only one application or conclusion tag. Use the following XML format:

- Full Chain Deduction:
<query_full>A,B,C</query_full>

- Reversal Examination:
<query_swap>1,3</query_swap>

- Submit Final Conclusion:
<answer>A,B,C</answer>

Notes:
- Sequence format is a comma-separated list of evidence, ordered by event node
- Node numbering starts from 1
- Reversal examinations can only be used after at least one full chain deduction
- Please resolve the case using minimal cross-examinations
"""

    tags = ["answer", "query_full", "query_swap"]
    
    reasoning_type = "归纳推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 3,
                "elements": "A,B,C",
                "target": "B,C,A",
            },
            2: {
                "n": 4,
                "elements": "A,B,C,D",
                "target": "C,A,D,B",
            },
            3: {
                "n": 5,
                "elements": "A,B,C,D,E",
                "target": "D,B,E,A,C",
            },
            4: {
                "n": 6,
                "elements": "A,B,C,D,E,F",
                "target": "E,C,A,F,B,D",
            },
            5: {
                "n": 7,
                "elements": "A,B,C,D,E,F,G",
                "target": "F,D,B,G,A,E,C",
            },
        },
        "en": {
            1: {
                "n": 3,
                "elements": "A,B,C",
                "target": "B,C,A",
            },
            2: {
                "n": 4,
                "elements": "A,B,C,D",
                "target": "C,A,D,B",
            },
            3: {
                "n": 5,
                "elements": "A,B,C,D,E",
                "target": "D,B,E,A,C",
            },
            4: {
                "n": 6,
                "elements": "A,B,C,D,E,F",
                "target": "E,C,A,F,B,D",
            },
            5: {
                "n": 7,
                "elements": "A,B,C,D,E,F,G",
                "target": "F,D,B,G,A,E,C",
            },
        },
    }

    def __init__(self, config):
        self.last_permutation = None
        self.query_count = 0
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["elements"] = cfg["elements"]
        
        self.target_permutation = [x.strip() for x in cfg["target"].split(",")]
        self.element_set = set(x.strip() for x in cfg["elements"].split(","))
        
        if len(self.target_permutation) != cfg["n"]:
            raise ValueError("Target permutation length mismatch")
        if set(self.target_permutation) != self.element_set:
            raise ValueError("Target permutation contains invalid elements")

    def _compute_min_swaps(self, perm):
        n = len(perm)
        perm_pos = {elem: i for i, elem in enumerate(perm)}
        
        visited = [False] * n
        num_cycles = 0
        
        for i in range(n):
            if not visited[i]:
                num_cycles += 1
                j = i
                while not visited[j]:
                    visited[j] = True
                    target_elem = self.target_permutation[j]
                    j = perm_pos[target_elem]
        
        return n - num_cycles

    def _validate_permutation(self, perm_str):
        try:
            perm_list = [x.strip() for x in perm_str.split(",")]
            
            if len(perm_list) != self._game_info["n"]:
                return False, None, f"Invalid length: expected {self._game_info['n']}, got {len(perm_list)}"
            
            perm_set = set(perm_list)
            if perm_set != self.element_set:
                return False, None, "Invalid elements in permutation"
            
            if len(perm_set) != len(perm_list):
                return False, None, "Duplicate elements in permutation"
            
            return True, perm_list, None
            
        except Exception as e:
            return False, None, str(e)

    def evaluate(self, parsed_info):
        answer_str = parsed_info["answer"].strip()
        is_valid, perm_list, error_msg = self._validate_permutation(answer_str)
        
        if not is_valid:
            return False
        
        return perm_list == self.target_permutation

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            error_no_prev = "错误：必须先进行至少一次完整排列查询才能使用交换查询。"
            error_format = "错误：格式无效。"
            error_position = "错误：位置编号超出范围或无效。"
        else:
            error_no_prev = "Error: Must perform at least one full permutation query before using swap query."
            error_format = "Error: Invalid format."
            error_position = "Error: Position number out of range or invalid."

        if "query_full" in parsed_info:
            perm_str = parsed_info["query_full"].strip()
            is_valid, perm_list, error_msg = self._validate_permutation(perm_str)
            
            if not is_valid:
                return f"{error_format} {error_msg}"
            
            k = self._compute_min_swaps(perm_list)
            self.last_permutation = perm_list
            self.query_count += 1
            
            return str(k)

        elif "query_swap" in parsed_info:
            if self.last_permutation is None:
                return error_no_prev
            
            try:
                swap_str = parsed_info["query_swap"].strip()
                positions = [int(x.strip()) for x in swap_str.split(",")]
                
                if len(positions) != 2:
                    return error_format
                
                pos1, pos2 = positions
                n = self._game_info["n"]
                
                if not (1 <= pos1 <= n and 1 <= pos2 <= n):
                    return error_position
                
                new_perm = self.last_permutation.copy()
                new_perm[pos1 - 1], new_perm[pos2 - 1] = new_perm[pos2 - 1], new_perm[pos1 - 1]
                
                k = self._compute_min_swaps(new_perm)
                self.last_permutation = new_perm
                self.query_count += 1
                
                return str(k)
                
            except ValueError:
                return error_format
            except Exception as e:
                return f"{error_format} {str(e)}"

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        elements = self._game_info["elements"].split(",")
        
        for p in itertools.permutations(elements):
            perm_list = list(p)
            perm_str = ",".join(perm_list)
            
            k = self._compute_min_swaps(perm_list)
            
            results.append({
                "query": f"<query_full>{perm_str}</query_full>",
                "answer": str(k)
            })
            
        return results

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        else:
            if "Yes" in correct:
                return correct.replace("Yes", "No")
            if "yes" in correct:
                return correct.replace("yes", "no")
            if "No" in correct:
                return correct.replace("No", "Yes")
            if "no" in correct:
                return correct.replace("no", "yes")

        return correct + "_WRONG"