from .base import Game
import re

class HiddenOrderDeductionGame(Game):

    game_rule_zh = """\
我们现在来玩一个"隐藏顺序推理"游戏，规则如下：

游戏设定了一个由 {n} 个不同元素组成的集合 S = {elements}，系统已为这些元素确定了一个隐藏的全序关系（即一个从小到大的标准排列），但你无法直接看到。

初始状态下，你会看到这些元素的一个打乱的排列。你的目标是通过有限的操作，推断出隐藏的全序关系，并使当前排列按照该隐藏顺序完全递增排列。

系统内部维护了一个"整齐度"指标，它表示当前排列中有多少对元素的相对位置符合隐藏顺序。当整齐度达到最大值时，当前排列就是完全有序的。

每次你可以执行以下操作之一（使用 XML 格式）：

1. **交换相邻元素**：交换位置 i 和 i+1 的元素（i 从 1 开始计数，1 <= i < {n}）
   系统会告诉你交换后是"更整齐"还是"更混乱"，并显示交换后的新排列。
   格式：<swap>i</swap>
   示例：<swap>3</swap> 表示交换位置 3 和位置 4 的元素

2. **查询当前排列**：查看当前的元素排列（不改变状态）
   格式：<query_queue></query_queue>

3. **查询是否完全有序**：询问当前排列是否已经完全有序
   格式：<query_ordered></query_ordered>

4. **提交最终答案**：提交你推断出的隐藏全序（从小到大的排列）
   格式：<answer>元素1,元素2,...,元素{n}</answer>
   示例：<answer>A,C,B,D</answer>

满足以下任一条件即为成功：
- 使当前排列达到完全有序状态，并提交与之一致的答案
- 直接提交与隐藏全序完全一致的答案

- 提交的答案不正确
- 操作格式不符合要求

请尽可能用较少的操作次数找出隐藏的全序关系。
"""

    game_rule_en = """\
Let's play a "Hidden Order Deduction" game. Here are the rules:

The game has a set S consisting of {n} distinct elements: {elements}. The system has determined a hidden total order (i.e., a standard sequence from smallest to largest) for these elements, but you cannot see it directly.

Initially, you will see a shuffled arrangement of these elements. Your goal is to deduce the hidden total order through limited operations and make the current arrangement fully sorted according to that hidden order.

The system maintains an internal "tidiness" metric, which represents how many pairs of elements in the current arrangement are in the correct relative position according to the hidden order. When tidiness reaches its maximum value, the current arrangement is fully sorted.

Each turn you can perform one of the following operations (using XML format):

1. **Swap adjacent elements**: Swap elements at positions i and i+1 (i starts from 1, 1 <= i < {n})
   The system will tell you whether the swap made it "tidier" or "messier", and show the new arrangement.
   Format: <swap>i</swap>
   Example: <swap>3</swap> means swap elements at positions 3 and 4

2. **Query current queue**: View the current element arrangement (does not change state)
   Format: <query_queue></query_queue>

3. **Query if fully ordered**: Ask whether the current arrangement is fully sorted
   Format: <query_ordered></query_ordered>

4. **Submit final answer**: Submit your deduced hidden total order (arrangement from smallest to largest)
   Format: <answer>element1,element2,...,element{n}</answer>
   Example: <answer>A,C,B,D</answer>

Success is achieved if any of the following is met:
- Make the current arrangement fully ordered and submit an answer consistent with it
- Directly submit an answer that is completely consistent with the hidden total order

- The submitted answer is incorrect
- Operation format does not meet requirements

Please try to find the hidden total order with as few operations as possible.
"""

    contextualized_rule_zh_1 = """\
欢迎使用智能交通调度系统。请根据规则进行车辆放行序列的优化：

调度中心检测到由 {n} 辆特种车辆组成的队列，标识为 S = {elements}。基于紧急程度和路线规划，系统预设了一个隐藏的最佳放行序列（即优先级从高到低的标准排列），但由于网络故障你无法直接获取该序列。

初始状态下，你会看到这些车辆的一个随机初始调度队列。你的目标是通过有限的调度指令，推断出隐藏的最佳放行序列，并使当前队列完全符合该标准优先级排列。

系统内部实时计算一个"顺畅度指标"，它表示当前队列中有多少对车辆的相对位置符合预设的最佳放行优先级。当顺畅度达到最大值时，当前队列即为最佳调度状态。

每次你可以执行以下操作之一（使用 XML 格式）：

1. **调整相邻车辆**：交换队列中位置 i 和 i+1 的车辆（i 从 1 开始计数，1 <= i < {n}）
   系统会反馈调度后顺畅度是"更整齐"还是"更混乱"，并显示最新的队列状态。
   格式：<swap>i</swap>
   示例：<swap>3</swap> 表示交换位置 3 和位置 4 的车辆

2. **查询当前队列**：查看当前车辆的排队顺序（不改变状态）
   格式：<query_queue></query_queue>

3. **查询是否达到最佳调度**：询问当前队列是否已完全符合最佳放行序列
   格式：<query_ordered></query_ordered>

4. **提交最终方案**：提交你推断出的最佳放行序列（按优先级从高到低排列）
   格式：<answer>车辆1,车辆2,...,车辆{n}</answer>
   示例：<answer>A,C,B,D</answer>

满足以下任一条件即为成功调度：
- 使当前队列达到最佳调度状态，并提交与之一致的最终方案
- 直接提交与预设最佳放行序列完全一致的方案

- 提交的最终方案不正确
- 调度指令格式不符合要求

请在保证道路网络不崩溃的前提下，用最少的调度指令找出最佳放行序列。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Intelligent Traffic Dispatch System. Please optimize the vehicle release sequence according to the following rules:

The dispatch center has detected a queue consisting of {n} special vehicles, identified as S = {elements}. Based on urgency and route planning, the system has determined a hidden optimal release sequence (i.e., a standard arrangement from highest to lowest priority), but you cannot access it directly due to a network glitch.

Initially, you will see a randomized initial dispatch queue of these vehicles. Your objective is to deduce the hidden optimal release sequence through limited dispatch commands and make the current queue fully comply with that standard priority arrangement.

The system maintains an internal "smoothness metric" in real-time, representing how many pairs of vehicles in the current queue are in the correct relative position according to the optimal release priority. When the smoothness metric reaches its peak, the current queue is in the optimal dispatch state.

Each turn you can perform one of the following operations (using XML format):

1. **Swap adjacent vehicles**: Swap vehicles at positions i and i+1 in the queue (i starts from 1, 1 <= i < {n})
   The system will report whether the swap made the smoothness "Tidier" or "Messier", and show the updated queue state.
   Format: <swap>i</swap>
   Example: <swap>3</swap> means swap vehicles at positions 3 and 4

2. **Query current queue**: View the current vehicle queuing order (does not change state)
   Format: <query_queue></query_queue>

3. **Query if optimal**: Ask whether the current queue fully complies with the optimal release sequence
   Format: <query_ordered></query_ordered>

4. **Submit final plan**: Submit your deduced optimal release sequence (arranged from highest to lowest priority)
   Format: <answer>vehicle1,vehicle2,...,vehicle{n}</answer>
   Example: <answer>A,C,B,D</answer>

Successful dispatch is achieved if any of the following is met:
- Make the current queue reach the optimal dispatch state and submit a plan consistent with it
- Directly submit a plan that perfectly matches the hidden optimal release sequence

- The submitted final plan is incorrect
- Command format does not meet requirements

Please try to deduce the optimal release sequence with the minimum number of dispatch commands to prevent traffic gridlock.
"""

    contextualized_rule_zh_2 = """\
欢迎进入智能临床药学辅助系统，请按医疗规程进行急救药物的配伍排序：

当前处方涉及 {n} 种不同的急救药物，编号集合为 S = {elements}。根据最新的药代动力学指南，系统已生成这些药物的一个隐藏标准配伍顺序（即副作用最小、疗效最佳的安全注射序列），但因权限限制你不可见。

初始状态下，你会看到一个存在风险的随机注射队列。你的目标是通过有限的调整操作，推断出隐藏的标准配伍顺序，并使当前的药物注射队列完全符合该安全序列。

系统内部实时监控一个"疗效预期指标"，它表示当前队列中有多少对药物的相对给药顺序符合标准配伍规范。当该指标达到最大值时，当前给药队列即为最安全的完全有序状态。

每次你可以执行以下操作之一（使用 XML 格式）：

1. **调换相邻药物**：调换注射队列中位置 i 和 i+1 的药物（i 从 1 开始计数，1 <= i < {n}）
   系统会根据药理学模型评估调整后是"更整齐"（预期提升）还是"更混乱"（预期下降），并显示最新给药队列。
   格式：<swap>i</swap>
   示例：<swap>3</swap> 表示调换位置 3 和位置 4 的药物

2. **核对当前队列**：查看目前的药物给药顺序（不改变状态）
   格式：<query_queue></query_queue>

3. **查询是否合规**：询问当前注射队列是否已完全符合标准配伍顺序
   格式：<query_ordered></query_ordered>

4. **提交最终方案**：提交你推断出的标准配伍顺序
   格式：<answer>药物1,药物2,...,药物{n}</answer>
   示例：<answer>A,C,B,D</answer>

满足以下任一条件即可完成抢救准备：
- 将当前注射队列调整至完全合规状态，并提交一致的方案
- 直接提交与隐藏标准配伍顺序完全一致的答案

- 提交的配伍方案存在医疗错误
- 操作指令格式不符合系统要求

抢救时间宝贵，请尽可能用最少的调换次数推断出正确的标准配伍顺序。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Intelligent Clinical Pharmacy Assist System. Please sequence the emergency medications according to medical protocols:

The current prescription involves {n} distinct emergency medications, identified by the set S = {elements}. Based on the latest pharmacokinetic guidelines, the system has generated a hidden standard compounding sequence (i.e., the safest injection order with minimal side effects and optimal efficacy), but it is invisible to you due to access restrictions.

Initially, you will see a randomized and potentially risky injection queue. Your objective is to deduce the hidden standard compounding sequence through limited adjustments and make the current medication injection queue fully compliant with this safe sequence.

The system monitors an internal "efficacy expectation metric" in real-time, which represents how many pairs of medications in the current queue have relative administration orders that comply with standard compounding protocols. When this metric reaches its peak, the current administration queue is in the safest, fully ordered state.

Each turn you can perform one of the following operations (using XML format):

1. **Swap adjacent medications**: Swap medications at positions i and i+1 in the injection queue (i starts from 1, 1 <= i < {n})
   The system will evaluate via pharmacological models whether the adjustment made it "Tidier" (expected improvement) or "Messier" (expected decline), and display the updated queue.
   Format: <swap>i</swap>
   Example: <swap>3</swap> means swap medications at positions 3 and 4

2. **Verify current queue**: Review the current medication administration order (does not change state)
   Format: <query_queue></query_queue>

3. **Query if compliant**: Ask whether the current injection queue is fully compliant with the standard compounding sequence
   Format: <query_ordered></query_ordered>

4. **Submit final regimen**: Submit your deduced standard compounding sequence
   Format: <answer>med1,med2,...,med{n}</answer>
   Example: <answer>A,C,B,D</answer>

Preparation for resuscitation is complete if any of the following is met:
- Adjust the current injection queue to a fully compliant state and submit a regimen consistent with it
- Directly submit a regimen that perfectly matches the hidden standard compounding sequence

- The submitted compounding regimen contains medical errors
- Operation format does not meet system requirements

Resuscitation time is critical. Please deduce the correct standard compounding sequence with the minimum number of swaps.
"""

    contextualized_rule_zh_3 = """\
欢迎使用智能教学教案编排系统，请完成课程知识点大纲的优化：

本单元包含了 {n} 个核心教学模块，集合 S = {elements}。基于教育心理学，系统内部已构建了一条隐藏的认知递进序列（即由浅入深、逻辑自洽的标准教学顺序），但作为测验，当前对你屏蔽。

初始状态下，你会看到一份打乱的授课大纲草案。你的目标是通过有限的大纲微调，推断出这条隐藏的认知递进序列，并使当前的授课大纲完全按照该标准顺序排列。

系统内部通过学习曲线模型计算"认知连贯度"，它反映当前大纲中有多少对教学模块的先后关系符合标准的认知递进逻辑。当连贯度达到最大值时，当前的教学大纲即为完全科学的有序状态。

每次你可以执行以下操作之一（使用 XML 格式）：

1. **调换相邻模块**：交换授课大纲中位置 i 和 i+1 的教学模块（i 从 1 开始计数，1 <= i < {n}）
   系统会告诉你调整后大纲的连贯度是"更整齐"还是"更混乱"，并展示更新后的大纲。
   格式：<swap>i</swap>
   示例：<swap>3</swap> 表示交换位置 3 和位置 4 的模块

2. **审阅当前大纲**：查看目前的教学模块排列（不改变状态）
   格式：<query_queue></query_queue>

3. **查询是否科学**：询问当前大纲是否已经完全符合认知递进序列
   格式：<query_ordered></query_ordered>

4. **提交最终教案**：提交你推断出的标准教学顺序
   格式：<answer>模块1,模块2,...,模块{n}</answer>
   示例：<answer>A,C,B,D</answer>

满足以下任一条件即为备课成功：
- 使当前大纲达到完全有序的科学状态，并提交与之一致的教案
- 直接提交与隐藏的认知递进序列完全一致的教案

- 提交的教案逻辑顺序错误
- 教研操作格式不符合规范

请高效利用测试反馈，用尽量少的调换步骤理清教学知识点的隐藏脉络。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Intelligent Lesson Planning System. Please optimize the course knowledge syllabus:

This unit contains {n} core teaching modules, denoted as set S = {elements}. Based on educational psychology, the system has constructed a hidden cognitive progression sequence (i.e., a standard teaching order from basic to advanced with coherent logic), but it is currently masked from you as a pedagogical test.

Initially, you will see a shuffled draft of the teaching syllabus. Your goal is to deduce this hidden cognitive progression sequence through limited syllabus adjustments and arrange the current syllabus to fully follow this standard order.

The system calculates a "cognitive coherence metric" using learning curve models, reflecting how many pairs of teaching modules in the current syllabus have preceding-succeeding relationships that align with standard cognitive progression logic. When coherence is maximized, the current syllabus is in a scientifically fully ordered state.

Each turn you can perform one of the following operations (using XML format):

1. **Swap adjacent modules**: Swap teaching modules at positions i and i+1 in the syllabus (i starts from 1, 1 <= i < {n})
   The system will tell you whether the adjusted syllabus coherence is "Tidier" or "Messier", and display the updated syllabus.
   Format: <swap>i</swap>
   Example: <swap>3</swap> means swap modules at positions 3 and 4

2. **Review current syllabus**: Check the current arrangement of teaching modules (does not change state)
   Format: <query_queue></query_queue>

3. **Query if scientific**: Ask whether the current syllabus fully conforms to the cognitive progression sequence
   Format: <query_ordered></query_ordered>

4. **Submit final lesson plan**: Submit your deduced standard teaching order
   Format: <answer>module1,module2,...,module{n}</answer>
   Example: <answer>A,C,B,D</answer>

Lesson preparation is successful if any of the following is met:
- Bring the current syllabus to a scientifically fully ordered state and submit a lesson plan consistent with it
- Directly submit a lesson plan perfectly matching the hidden cognitive progression sequence

- The submitted lesson plan has an incorrect logical order
- Pedagogical operation format violates specifications

Please effectively utilize test feedback to clarify the hidden threads of teaching knowledge points with as few swap steps as possible.
"""

    contextualized_rule_zh_4 = """\
欢迎登录柔性制造控制系统，当前正进行自动化产线的工序排程：

本次装配任务包含 {n} 个核心生产工序，工单集合 S = {elements}。工艺数据库中存储了针对该批次产品的一套隐藏的黄金工艺流（即能最小化损耗的标准装配顺序），但未对当前操作终端公开。

初始状态下，流水线被配置为一个未经验证的随机工序序列。你的目标是通过有限的调试操作，逆向推断出隐藏的黄金工艺流，并将当前的流水线完全调整为该标准顺序。

系统后台内置了一个"良率评估值"，它代表当前流水线中有多少对工序的先后执行逻辑符合黄金工艺流的标准。当该评估值达到峰值时，表明当前流水线已达到无损耗的完全有序状态。

每次你可以执行以下操作之一（使用 XML 格式）：

1. **交换相邻工序**：对流水线上位置 i 和 i+1 的工序进行换位（i 从 1 开始计数，1 <= i < {n}）
   系统仿真将反馈换位后的良率是"更整齐"（良率上升）还是"更混乱"（良率下降），并输出新序列。
   格式：<swap>i</swap>
   示例：<swap>3</swap> 表示将第 3 道与第 4 道工序换位

2. **读取当前序列**：查看流水线当前的工序排布（不改变状态）
   格式：<query_queue></query_queue>

3. **查询是否达标**：询问当前流水线是否已经完全吻合黄金工艺流
   格式：<query_ordered></query_ordered>

4. **提交最终工艺**：提交你推断出的标准装配顺序
   格式：<answer>工序1,工序2,...,工序{n}</answer>
   示例：<answer>A,C,B,D</answer>

满足以下任一条件即为排程成功：
- 使当前流水线达到完全有序的标准状态，并提交一致的工艺参数
- 直接提交与隐藏黄金工艺流完全一致的答案

- 提交的工艺参数会导致生产事故（顺序错误）
- 调试指令语法不符合设备规范

为节约设备空转成本，请用最小的换位测试次数精准锁定黄金工艺流。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Flexible Manufacturing Control System. Currently scheduling processes for the automated production line:

This assembly task involves {n} core production processes, with the work order set S = {elements}. The process database stores a hidden golden workflow (i.e., a standard assembly sequence minimizing yield loss) for this batch, which is unpublished to the current operating terminal.

Initially, the assembly line is configured with an unverified, randomized sequence of processes. Your goal is to reverse-engineer the hidden golden workflow through limited debugging operations and completely adjust the current assembly line to this standard order.

The system backend incorporates a "yield evaluation metric" representing how many pairs of processes in the current assembly line have execution logics conforming to the golden workflow standard. When this metric peaks, the current assembly line has reached a loss-free, fully ordered state.

Each turn you can perform one of the following operations (using XML format):

1. **Swap adjacent processes**: Transpose processes at positions i and i+1 on the assembly line (i starts from 1, 1 <= i < {n})
   System simulation will report whether the transposed yield is "Tidier" (yield increase) or "Messier" (yield decrease), and output the new sequence.
   Format: <swap>i</swap>
   Example: <swap>3</swap> means transpose the 3rd and 4th processes

2. **Read current sequence**: View the current process layout of the assembly line (does not change state)
   Format: <query_queue></query_queue>

3. **Query if compliant**: Ask whether the current assembly line completely matches the golden workflow
   Format: <query_ordered></query_ordered>

4. **Submit final process**: Submit your deduced standard assembly sequence
   Format: <answer>process1,process2,...,process{n}</answer>
   Example: <answer>A,C,B,D</answer>

Scheduling is successful if any of the following is met:
- Bring the current assembly line to the fully ordered standard state and submit consistent process parameters
- Directly submit an answer perfectly matching the hidden golden workflow

- Submitted process parameters lead to a production failure (incorrect sequence)
- Debugging command syntax violates equipment specifications

To save equipment idling costs, please precisely lock onto the golden workflow using the minimum number of transposition tests.
"""

    contextualized_rule_zh_5 = """\
欢迎使用司法案卷审查辅助系统。请协助完成复杂案件的证据链梳理：

本案包含 {n} 份核心证据材料，卷宗编号为 S = {elements}。基于警方已掌握的机密线索，系统内部已确认了这些证据在真实案发时间线上的隐藏全序（即案情发展的客观发生顺序），但因调查阶段保密你需要独立进行推理。

初始状态下，你会拿到一份顺序杂乱的案卷汇总。你的目标是通过有限的卷宗比对，推断出证据的真实时间线，并使当前的案卷材料完全按照客观顺序归档排列。

系统利用法理模型计算案卷的"逻辑自洽度"，它指示当前材料排序中有多少对证据的前后因果关系符合真实时间线。当自洽度达到顶峰时，当前的案卷排序即为还原真相的完全有序状态。

每次你可以执行以下操作之一（使用 XML 格式）：

1. **对调相邻材料**：对调案卷中位置 i 和 i+1 的两份证据材料（i 从 1 开始计数，1 <= i < {n}）
   系统会基于机密数据库反馈调整后案卷是"更整齐"（逻辑更顺畅）还是"更混乱"（出现矛盾），并展示新的排序。
   格式：<swap>i</swap>
   示例：<swap>3</swap> 表示对调位置 3 和位置 4 的材料

2. **查阅当前案卷**：查看目前的案卷材料排序（不改变状态）
   格式：<query_queue></query_queue>

3. **查询是否闭环**：询问当前案卷顺序是否已完全契合真实时间线
   格式：<query_ordered></query_ordered>

4. **提交最终调查结论**：提交你推断出的真实案情时间线
   格式：<answer>证据1,证据2,...,证据{n}</answer>
   示例：<answer>A,C,B,D</answer>

满足以下任一条件即为成功破卷：
- 将当前案卷整理至完全契合客观真相的状态，并提交相同的材料顺序
- 直接提交与隐藏真实时间线完全一致的调查结论

- 提交的调查结论与真相存在出入
- 梳理操作的指令格式不符合系统规范

为保证司法效率，请尽量以最少的对调次数还原事实真相。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Judicial Case File Review Assist System. Please assist in organizing the chain of evidence for a complex case:

This case involves {n} core evidence materials, with file identifiers S = {elements}. Based on classified clues already secured by the police, the system has internally verified the hidden total order of this evidence on the true timeline of the incident (i.e., the objective sequence of events), but you must deduce it independently due to confidentiality during the investigation phase.

Initially, you will receive a disorganized summary of the case files. Your goal is to deduce the true timeline of evidence through limited file comparisons and archive the current case materials completely according to the objective sequence.

The system utilizes legal models to calculate the "logical consistency metric" of the case files, indicating how many pairs of evidence in the current sorting have preceding-succeeding causal relationships aligning with the true timeline. When consistency peaks, the current file sorting is in a fully ordered state that restores the truth.

Each turn you can perform one of the following operations (using XML format):

1. **Swap adjacent materials**: Swap two evidence materials at positions i and i+1 in the case files (i starts from 1, 1 <= i < {n})
   The system will report via the classified database whether the adjusted files are "Tidier" (smoother logic) or "Messier" (contradictions appear), and show the new sorting.
   Format: <swap>i</swap>
   Example: <swap>3</swap> means swap materials at positions 3 and 4

2. **Review current files**: Check the current sorting of case materials (does not change state)
   Format: <query_queue></query_queue>

3. **Query if closed-loop**: Ask whether the current file sequence completely aligns with the true timeline
   Format: <query_ordered></query_ordered>

4. **Submit final investigation conclusion**: Submit your deduced true timeline of the case
   Format: <answer>evidence1,evidence2,...,evidence{n}</answer>
   Example: <answer>A,C,B,D</answer>

Successfully breaking the case is achieved if any of the following is met:
- Organize the current case files into a state that perfectly aligns with the objective truth and submit the identical material sequence
- Directly submit an investigation conclusion perfectly matching the hidden true timeline

- The submitted investigation conclusion contains discrepancies with the truth
- The formatting of organizing operations violates system specifications

To ensure judicial efficiency, please restore the objective truth with the minimum number of swaps.
"""

    tags = ["answer", "swap", "query_queue", "query_ordered"]

    reasoning_type = "归纳推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "elements": "A, B, C, D",
                "hidden_order": ["C", "A", "D", "B"],
                "initial_queue": ["A", "B", "C", "D"],
            },
            2: {
                "n": 5,
                "elements": "A, B, C, D, E",
                "hidden_order": ["B", "E", "A", "D", "C"],
                "initial_queue": ["A", "B", "C", "D", "E"],
            },
            3: {
                "n": 6,
                "elements": "A, B, C, D, E, F",
                "hidden_order": ["D", "B", "F", "A", "E", "C"],
                "initial_queue": ["A", "B", "C", "D", "E", "F"],
            },
            4: {
                "n": 7,
                "elements": "A, B, C, D, E, F, G",
                "hidden_order": ["E", "C", "G", "A", "F", "B", "D"],
                "initial_queue": ["A", "B", "C", "D", "E", "F", "G"],
            },
            5: {
                "n": 8,
                "elements": "A, B, C, D, E, F, G, H",
                "hidden_order": ["H", "C", "F", "A", "E", "G", "B", "D"],
                "initial_queue": ["A", "B", "C", "D", "E", "F", "G", "H"],
            },
        },
        "en": {
            1: {
                "n": 4,
                "elements": "A, B, C, D",
                "hidden_order": ["C", "A", "D", "B"],
                "initial_queue": ["A", "B", "C", "D"],
            },
            2: {
                "n": 5,
                "elements": "A, B, C, D, E",
                "hidden_order": ["B", "E", "A", "D", "C"],
                "initial_queue": ["A", "B", "C", "D", "E"],
            },
            3: {
                "n": 6,
                "elements": "A, B, C, D, E, F",
                "hidden_order": ["D", "B", "F", "A", "E", "C"],
                "initial_queue": ["A", "B", "C", "D", "E", "F"],
            },
            4: {
                "n": 7,
                "elements": "A, B, C, D, E, F, G",
                "hidden_order": ["E", "C", "G", "A", "F", "B", "D"],
                "initial_queue": ["A", "B", "C", "D", "E", "F", "G"],
            },
            5: {
                "n": 8,
                "elements": "A, B, C, D, E, F, G, H",
                "hidden_order": ["H", "C", "F", "A", "E", "G", "B", "D"],
                "initial_queue": ["A", "B", "C", "D", "E", "F", "G", "H"],
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
        self._game_info["n"] = cfg["n"]
        self._game_info["elements"] = cfg["elements"]
        
        self.hidden_order = cfg["hidden_order"]
        self.current_queue = cfg["initial_queue"].copy()
        self.order_map = {elem: idx for idx, elem in enumerate(self.hidden_order)}
        self.current_tidiness = self._calculate_tidiness()

    def _calculate_tidiness(self):
        count = 0
        n = len(self.current_queue)
        for i in range(n):
            for j in range(i + 1, n):
                elem_i = self.current_queue[i]
                elem_j = self.current_queue[j]
                if self.order_map[elem_i] < self.order_map[elem_j]:
                    count += 1
        return count

    def _is_fully_ordered(self):
        return self.current_queue == self.hidden_order

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        try:
            submitted_order = [x.strip() for x in raw_ans.split(",")]
            if len(submitted_order) != len(self.hidden_order):
                return False
            return submitted_order == self.hidden_order
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            tidier_msg = "更整齐"
            messier_msg = "更混乱"
            queue_prefix = "当前队列: "
            ordered_yes = "是"
            ordered_no = "否"
            invalid_pos = "错误：位置超出范围。"
            invalid_format = "错误：格式无效。"
        else:
            tidier_msg = "Tidier"
            messier_msg = "Messier"
            queue_prefix = "Current queue: "
            ordered_yes = "Yes"
            ordered_no = "No"
            invalid_pos = "Error: Position out of range."
            invalid_format = "Error: Invalid format."

        if "swap" in parsed_info:
            try:
                pos = int(parsed_info["swap"].strip())
                if pos < 1 or pos >= len(self.current_queue):
                    return invalid_pos
                
                old_tidiness = self.current_tidiness
                idx = pos - 1
                self.current_queue[idx], self.current_queue[idx + 1] = \
                    self.current_queue[idx + 1], self.current_queue[idx]
                
                new_tidiness = self._calculate_tidiness()
                self.current_tidiness = new_tidiness
                
                if new_tidiness > old_tidiness:
                    feedback = tidier_msg
                else: 
                    feedback = messier_msg
                
                queue_str = ", ".join(self.current_queue)
                return f"{feedback}\n{queue_prefix}[{queue_str}]"
                
            except (ValueError, IndexError):
                return invalid_format

        elif "query_queue" in parsed_info:
            queue_str = ", ".join(self.current_queue)
            return f"{queue_prefix}[{queue_str}]"

        elif "query_ordered" in parsed_info:
            return ordered_yes if self._is_fully_ordered() else ordered_no

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if self.config.language == "zh":
            if "更整齐" in correct:
                return correct.replace("更整齐", "更混乱")
            elif "更混乱" in correct:
                return correct.replace("更混乱", "更整齐")
            if correct.strip() == "是":
                return "否"
            if correct.strip() == "否":
                return "是"
        else:
            if "Tidier" in correct:
                return correct.replace("Tidier", "Messier")
            elif "Messier" in correct:
                return correct.replace("Messier", "Tidier")
            lower_correct = correct.strip().lower()
            if lower_correct == "yes":
                return "No"
            if lower_correct == "no":
                return "Yes"

        if "Current queue:" in correct or "当前队列:" in correct:
            import re as _re
            match = _re.search(r'\[(.+?)\]', correct)
            if match:
                elements = [e.strip() for e in match.group(1).split(',')]
                elements.reverse()
                reversed_str = ", ".join(elements)
                return correct.replace(match.group(1), reversed_str)

        if correct.isdigit():
            return str(int(correct) + 1)
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        if self.config.language == "zh":
            tidier_msg = "更整齐"
            messier_msg = "更混乱"
            queue_prefix = "当前队列: "
            ordered_yes = "是"
            ordered_no = "否"
        else:
            tidier_msg = "Tidier"
            messier_msg = "Messier"
            queue_prefix = "Current queue: "
            ordered_yes = "Yes"
            ordered_no = "No"

        backup_queue = self.current_queue.copy()
        backup_tidiness = self.current_tidiness

        n = len(self.current_queue)

        for pos in range(1, n):
            idx = pos - 1
            
            self.current_queue[idx], self.current_queue[idx + 1] = \
                self.current_queue[idx + 1], self.current_queue[idx]
            
            new_tidiness = self._calculate_tidiness()
            
            if new_tidiness > backup_tidiness:
                feedback = tidier_msg
            else:
                feedback = messier_msg
            
            queue_str = ", ".join(self.current_queue)
            answer = f"{feedback}\n{queue_prefix}[{queue_str}]"
            
            results.append({
                "query": f"<swap>{pos}</swap>",
                "answer": answer
            })
            
            self.current_queue = backup_queue.copy()
            self.current_tidiness = backup_tidiness

        queue_str = ", ".join(self.current_queue)
        results.append({
            "query": "<query_queue></query_queue>",
            "answer": f"{queue_prefix}[{queue_str}]"
        })

        is_ordered = self._is_fully_ordered()
        results.append({
            "query": "<query_ordered></query_ordered>",
            "answer": ordered_yes if is_ordered else ordered_no
        })

        return results