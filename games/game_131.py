from .base import Game
import re

class PermutationSortingGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "序列"

    game_rule_zh = """\
我们来进行一场"隐藏排列识别与最优排序"任务，规则如下：

当前有 {n} 个不同的元素，用标识 {labels} 区分。

初始排列：{initial_sequence}

系统已设定了一个目标排列 R*（从 {k} 个候选排列中选出，但你不知道具体是哪一个）。你的任务是：
1. 通过查询识别出真实的目标排列 R*
2. 通过尽可能少的对调操作将当前排列变换为目标排列

你可以进行以下操作（每次只能执行一个）：

1. **询问距离**：查询当前排列到目标排列所需的最少对调次数
   格式：<query_distance></query_distance>

2. **试探互换**：假设对调位置 i 和 j 的元素，查询对调后的距离（不改变真实排列）
   格式：<test_swap>i,j</test_swap>
   示例：<test_swap>1,3</test_swap> 表示试探互换位置1和位置3的元素

3. **执行互换**：真实对调位置 i 和 j 的元素（会改变当前排列状态）
   格式：<do_swap>i,j</do_swap>
   示例：<do_swap>2,4</do_swap> 表示真实互换位置2和位置4的元素

4. **查看当前排列**：查看当前元素的真实排列状态
   格式：<query_sequence></query_sequence>

5. **提交答案**：当你确定目标排列后，提交最终方案
   格式：<answer>标识1,标识2,...,标识{n}</answer>
   示例：<answer>{example_answer}</answer>

- 正确识别目标排列 R*
- 使用的真实互换次数等于初始的最小对调次数（最优次数）

- 提交错误的目标排列
- 使用的真实互换次数超过初始最小对调次数
- 格式错误

注意：位置编号从 1 到 {n}。
"""

    game_rule_en = """\
Let's play a "Hidden Permutation Identification and Optimal Sorting" task. Rules:

There are {n} distinct elements, identified by labels: {labels}

Initial sequence: {initial_sequence}

The system has set a target permutation R* (chosen from {k} candidates, but you don't know which one). Your tasks are:
1. Identify the true target permutation R* through queries
2. Transform the current sequence into the target permutation using as few swaps as possible

You can perform the following operations (one at a time):

1. **Query Distance**: Get the minimum number of swaps needed from the current sequence to the target
   Format: <query_distance></query_distance>

2. **Test Swap**: Hypothetically swap elements at positions i and j, query the resulting distance (does not change current sequence)
   Format: <test_swap>i,j</test_swap>
   Example: <test_swap>1,3</test_swap> means test swapping position 1 and position 3

3. **Execute Swap**: Actually swap elements at positions i and j (changes current sequence)
   Format: <do_swap>i,j</do_swap>
   Example: <do_swap>2,4</do_swap> means actually swap position 2 and position 4

4. **Query Current Sequence**: View the current element sequence state
   Format: <query_sequence></query_sequence>

5. **Submit Answer**: Submit your final plan when you've identified the target permutation
   Format: <answer>label1,label2,...,label{n}</answer>
   Example: <answer>{example_answer}</answer>

- Correctly identify the target permutation R*
- Number of actual swaps equals the initial minimum swap count (optimal count)

- Submit the wrong target permutation
- Number of actual swaps exceeds the initial minimum count
- Format error

Note: Position indices range from 1 to {n}.
"""

    contextualized_rule_zh_1 = """\
作为智能列车调度员，我们来进行一场"隐藏编组识别与最优重构"任务，规则如下：

调度站内目前有 {n} 节不同的车厢，用标识 {labels} 区分。

当前初始编组状态：{initial_sequence}

系统已下达了一个机密的最终目标编组 R*（从 {k} 个候选安全编组中选出，但你目前权限无法直接获取）。你的任务是：
1. 通过排查识别出真实的目标编组 R*
2. 通过尽可能少的车厢对调操作（即道岔切换）将当前编组重构为目标编组

你可以进行以下操作（每次只能执行一个）：

1. **询问调度步数**：查询当前编组到目标编组所需的最少对调次数
   格式：<query_distance></query_distance>

2. **试探互换**：在沙盘中假设对调位置 i 和 j 的车厢，查询对调后的步数（不改变真实编组）
   格式：<test_swap>i,j</test_swap>
   示例：<test_swap>1,3</test_swap> 表示试探互换位置1和位置3的车厢

3. **执行互换**：在轨道上真实对调位置 i 和 j 的车厢（会改变当前编组状态）
   格式：<do_swap>i,j</do_swap>
   示例：<do_swap>2,4</do_swap> 表示真实互换位置2和位置4的车厢

4. **查看当前编组**：查看当前车厢的真实排列状态
   格式：<query_sequence></query_sequence>

5. **宣告目标编组**：当你确定目标编组后，提交最终方案
   格式：<answer>标识1,标识2,...,标识{n}</answer>
   示例：<answer>{example_answer}</answer>

- 正确识别目标编组 R*
- 使用的真实互换次数等于初始的最小调度步数（最优次数）

- 宣告错误的目标编组
- 使用的真实互换次数超过初始最小调度步数
- 格式错误

注意：位置编号从 1 到 {n}。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
As an intelligent train dispatcher, let's play a "Hidden Formation Identification and Optimal Restructuring" task. Rules:

The shunting yard has {n} distinct train carriages, identified by labels: {labels}

Initial formation sequence: {initial_sequence}

The system has issued a classified target formation R* (chosen from {k} candidate safe formations, but you don't know which one). Your tasks are:
1. Identify the true target formation R*
2. Transform the current formation into the target formation using as few carriage position swaps (track switches) as possible

You can perform the following operations (one at a time):

1. **Query Switching Steps**: Get the minimum number of swaps needed from the current formation to the target
   Format: <query_distance></query_distance>

2. **Test Swap**: Hypothetically swap carriages at positions i and j in the sandbox, query the resulting steps (does not change current sequence)
   Format: <test_swap>i,j</test_swap>
   Example: <test_swap>1,3</test_swap> means test swapping position 1 and position 3

3. **Execute Swap**: Actually swap carriages at positions i and j on the tracks (changes current formation)
   Format: <do_swap>i,j</do_swap>
   Example: <do_swap>2,4</do_swap> means actually swap position 2 and position 4

4. **Query Current Formation**: View the current carriage sequence state
   Format: <query_sequence></query_sequence>

5. **Declare Target Formation**: Submit your final plan when you've identified the target formation
   Format: <answer>label1,label2,...,label{n}</answer>
   Example: <answer>{example_answer}</answer>

- Correctly identify the target formation R*
- Number of actual swaps equals the initial minimum switching steps (optimal count)

- Declare the wrong target formation
- Number of actual swaps exceeds the initial minimum steps
- Format error

Note: Position indices range from 1 to {n}.
"""

    contextualized_rule_zh_2 = """\
作为基因组学专家，我们来进行一场"隐藏健康基因组识别与最优编辑"任务，规则如下：

当前样本存在 {n} 个关键的基因片段，用标签 {labels} 标示。

初始基因序列为：{initial_sequence}

系统已匹配到一个理想的健康目标序列 R*（从 {k} 个已知健康候选变体中选出，但你尚不知晓具体是哪一个）。你的任务是：
1. 识别出真实的健康目标序列 R*
2. 通过尽可能少的片段重组（即对调）操作将当前序列修复为目标序列

你可以进行以下操作（每次只能执行一个）：

1. **询问干预次数**：查询当前序列达到目标序列所需的最少对调次数
   格式：<query_distance></query_distance>

2. **试探重组**：在模拟器中假设对调位置 i 和 j 的片段，查询重组后的次数（不改变真实序列）
   格式：<test_swap>i,j</test_swap>
   示例：<test_swap>1,3</test_swap> 表示试探重组位置1和位置3的基因片段

3. **执行重组**：在样本中真实对调位置 i 和 j 的片段（会改变当前序列）
   格式：<do_swap>i,j</do_swap>
   示例：<do_swap>2,4</do_swap> 表示真实对调位置2和位置4的基因片段

4. **查看当前序列**：查看当前基因序列状态
   格式：<query_sequence></query_sequence>

5. **宣告目标序列**：当你确定健康目标序列后，提交最终答案
   格式：<answer>标签1,标签2,...,标签{n}</answer>
   示例：<answer>{example_answer}</answer>

- 正确识别目标序列 R*
- 使用的真实重组次数等于初始的最小干预次数（最优次数）

- 宣告错误的目标序列
- 使用的真实重组次数超过初始最少干预次数
- 格式错误

注意：位置编号从 1 到 {n}。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
As a genomics expert, let's play a "Hidden Healthy Genome Identification and Optimal Editing" task. Rules:

The sample contains {n} key gene segments, indicated by labels: {labels}

Initial genetic sequence: {initial_sequence}

The system has matched an ideal healthy target sequence R* (chosen from {k} known healthy candidate variants, but you don't know which one). Your tasks are:
1. Identify the true healthy target sequence R*
2. Repair the current sequence into the target sequence using as few segment recombinations (swaps) as possible

You can perform the following operations (one at a time):

1. **Query Intervention Steps**: Get the minimum number of swaps needed from the current sequence to the target
   Format: <query_distance></query_distance>

2. **Test Recombination**: Hypothetically swap segments at positions i and j in the simulator, query the resulting steps (does not change current sequence)
   Format: <test_swap>i,j</test_swap>
   Example: <test_swap>1,3</test_swap> means test swapping gene segments at position 1 and position 3

3. **Execute Recombination**: Actually swap segments at positions i and j in the sample (changes current sequence)
   Format: <do_swap>i,j</do_swap>
   Example: <do_swap>2,4</do_swap> means actually swap gene segments at position 2 and position 4

4. **Query Current Sequence**: View the current genetic sequence state
   Format: <query_sequence></query_sequence>

5. **Declare Target Sequence**: Submit your final answer when you've identified the healthy target sequence
   Format: <answer>label1,label2,...,label{n}</answer>
   Example: <answer>{example_answer}</answer>

- Correctly identify the target sequence R*
- Number of actual recombinations equals the initial minimum intervention steps (optimal count)

- Declare the wrong target sequence
- Number of actual recombinations exceeds the initial minimum steps
- Format error

Note: Position indices range from 1 to {n}.
"""

    contextualized_rule_zh_3 = """\
作为课程规划主管，我们来进行一场"隐藏最佳大纲识别与最优课表调整"任务，规则如下：

本学期包含 {n} 个核心教学模块，用标签 {labels} 区分。

当前初始课程序列：{initial_sequence}

教研组已秘密确立了一个最优的教学大纲 R*（从 {k} 个候选大纲中选出，但你不知道具体是哪个）。你的任务是：
1. 识别出真实的最优教学大纲 R*
2. 通过尽可能少的模块调换操作，将当前课表调整为最优大纲顺序

你可以进行以下操作（每次只能执行一个）：

1. **询问调整次数**：查询当前课表达到目标大纲所需的最少调换次数
   格式：<query_distance></query_distance>

2. **试探调换**：假设调换排期 i 和 j 的教学模块，查询调换后的次数（不改变当前课表）
   格式：<test_swap>i,j</test_swap>
   示例：<test_swap>1,3</test_swap> 表示试探调换排期1和排期3的模块

3. **执行调换**：真实调换排期 i 和 j 的教学模块（会改变当前课表）
   格式：<do_swap>i,j</do_swap>
   示例：<do_swap>2,4</do_swap> 表示真实调换排期2和排期4的模块

4. **查看当前课表**：查看当前的教学模块序列
   格式：<query_sequence></query_sequence>

5. **宣告目标大纲**：当你确定最优大纲后，提交方案
   格式：<answer>标签1,标签2,...,标签{n}</answer>
   示例：<answer>{example_answer}</answer>

- 正确识别最优教学大纲 R*
- 使用的真实调换次数等于初始的最小调整次数（最优次数）

- 宣告错误的目标大纲
- 使用的真实调换次数超过初始最小调换次数
- 格式错误

注意：排期位置编号从 1 到 {n}。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
As a curriculum planning director, let's play a "Hidden Optimal Syllabus Identification and Schedule Adjustment" task. Rules:

This semester includes {n} core teaching modules, identified by labels: {labels}

Initial course sequence: {initial_sequence}

The faculty committee has secretly established an optimal syllabus R* (chosen from {k} candidate syllabi, but you don't know which one). Your tasks are:
1. Identify the true optimal syllabus R*
2. Adjust the current schedule into the optimal syllabus using as few module swaps as possible

You can perform the following operations (one at a time):

1. **Query Adjustment Steps**: Get the minimum number of swaps needed from the current schedule to the target syllabus
   Format: <query_distance></query_distance>

2. **Test Swap**: Hypothetically swap teaching modules at periods i and j, query the resulting steps (does not change current schedule)
   Format: <test_swap>i,j</test_swap>
   Example: <test_swap>1,3</test_swap> means test swapping modules at period 1 and period 3

3. **Execute Swap**: Actually swap teaching modules at periods i and j (changes current schedule)
   Format: <do_swap>i,j</do_swap>
   Example: <do_swap>2,4</do_swap> means actually swap modules at period 2 and period 4

4. **Query Current Schedule**: View the current teaching module sequence
   Format: <query_sequence></query_sequence>

5. **Declare Target Syllabus**: Submit your plan when you've identified the optimal syllabus
   Format: <answer>label1,label2,...,label{n}</answer>
   Example: <answer>{example_answer}</answer>

- Correctly identify the optimal syllabus R*
- Number of actual swaps equals the initial minimum adjustment steps (optimal count)

- Declare the wrong target syllabus
- Number of actual swaps exceeds the initial minimum steps
- Format error

Note: Period indices range from 1 to {n}.
"""

    contextualized_rule_zh_4 = """\
作为智能制造工程师，我们来进行一场"隐藏最优蓝图识别与流水线重构"任务，规则如下：

工厂当前分配了 {n} 个不同的加工工序，用标签 {labels} 区分。

初始流水线配置为：{initial_sequence}

系统预设了一个最优的流水线蓝图 R*（从 {k} 个经验证的候选蓝图中选出，但你处于盲测状态）。你的任务是：
1. 识别出真实的流水线蓝图 R*
2. 通过尽可能少的机械臂工序对调操作将当前流水线重构为目标蓝图

你可以进行以下操作（每次只能执行一个）：

1. **询问重构步数**：查询当前配置达到目标蓝图所需的最少对调次数
   格式：<query_distance></query_distance>

2. **试探对调**：在控制台中假设对调位置 i 和 j 的工序，查询重构步数（不改变真实流水线）
   格式：<test_swap>i,j</test_swap>
   示例：<test_swap>1,3</test_swap> 表示试探对调工位1和工位3的工序

3. **执行对调**：在车间真实对调位置 i 和 j 的工序（会改变当前流水线配置）
   格式：<do_swap>i,j</do_swap>
   示例：<do_swap>2,4</do_swap> 表示真实对调工位2和工位4的工序

4. **查看当前配置**：查看真实的流水线工序状态
   格式：<query_sequence></query_sequence>

5. **宣告目标配置**：当你确定目标蓝图后，提交最终配置方案
   格式：<answer>标签1,标签2,...,标签{n}</answer>
   示例：<answer>{example_answer}</answer>

- 正确识别目标蓝图 R*
- 使用的真实对调次数等于初始的最小重构步数（最优次数）

- 宣告错误的目标配置
- 使用的真实对调次数超过初始最少重构步数
- 格式错误

注意：工位编号从 1 到 {n}。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
As a smart manufacturing engineer, let's play a "Hidden Optimal Blueprint Identification and Pipeline Reconfiguration" task. Rules:

The factory currently has {n} distinct manufacturing processes, identified by labels: {labels}

Initial pipeline configuration: {initial_sequence}

The system has preset an optimal pipeline blueprint R* (chosen from {k} validated candidate blueprints, but you are in a blind test). Your tasks are:
1. Identify the true optimal blueprint R*
2. Reconfigure the current pipeline into the target blueprint using as few robotic arm process swaps as possible

You can perform the following operations (one at a time):

1. **Query Reconfiguration Steps**: Get the minimum number of swaps needed from the current configuration to the blueprint
   Format: <query_distance></query_distance>

2. **Test Swap**: Hypothetically swap processes at stations i and j in the console, query the resulting steps (does not change real pipeline)
   Format: <test_swap>i,j</test_swap>
   Example: <test_swap>1,3</test_swap> means test swapping processes at station 1 and station 3

3. **Execute Swap**: Actually swap processes at stations i and j on the shop floor (changes current configuration)
   Format: <do_swap>i,j</do_swap>
   Example: <do_swap>2,4</do_swap> means actually swap processes at station 2 and station 4

4. **Query Current Configuration**: View the real pipeline process state
   Format: <query_sequence></query_sequence>

5. **Declare Target Configuration**: Submit your final plan when you've identified the optimal blueprint
   Format: <answer>label1,label2,...,label{n}</answer>
   Example: <answer>{example_answer}</answer>

- Correctly identify the optimal blueprint R*
- Number of actual swaps equals the initial minimum reconfiguration steps (optimal count)

- Declare the wrong target configuration
- Number of actual swaps exceeds the initial minimum steps
- Format error

Note: Station indices range from 1 to {n}.
"""

    contextualized_rule_zh_5 = """\
作为首席庭审调查员，我们来进行一场"隐藏证据链重构与最优梳理"任务，规则如下：

案件目前收集了 {n} 份关键证据卷宗，用标签 {labels} 标示。

初始卷宗提交顺序为：{initial_sequence}

检方已推导出一个最符合逻辑的真实事件时间线 R*（从 {k} 个可能的时间线假设中选出，但尚未向你公开）。你的任务是：
1. 识别出真实的事件时间线 R*
2. 通过尽可能少的卷宗位置对调操作将当前卷宗顺序重组为真实时间线

你可以进行以下操作（每次只能执行一个）：

1. **询问重组步数**：查询当前卷宗达到真实时间线所需的最少对调次数
   格式：<query_distance></query_distance>

2. **试探对调**：在案情板上假设对调位置 i 和 j 的卷宗，查询重组后的步数（不改变实际卷宗顺序）
   格式：<test_swap>i,j</test_swap>
   示例：<test_swap>1,3</test_swap> 表示试探对调位置1和位置3的证据卷宗

3. **执行对调**：在档案库中真实对调位置 i 和 j 的卷宗（会改变当前提交顺序）
   格式：<do_swap>i,j</do_swap>
   示例：<do_swap>2,4</do_swap> 表示真实对调位置2和位置4的证据卷宗

4. **查看当前证据链**：查看当前卷宗的排列顺序
   格式：<query_sequence></query_sequence>

5. **宣告目标顺序**：当你确定真实的时间线后，提交最终卷宗顺序
   格式：<answer>标签1,标签2,...,标签{n}</answer>
   示例：<answer>{example_answer}</answer>

- 正确识别真实的事件时间线 R*
- 使用的真实对调次数等于初始的最小重组步数（最优次数）

- 宣告错误的时间线顺序
- 使用的真实对调次数超过初始最少重组步数
- 格式错误

注意：卷宗位置编号从 1 到 {n}。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
As a chief trial investigator, let's play a "Hidden Evidence Chain Reconstruction and Optimal Sorting" task. Rules:

The case currently has {n} key evidence files, indicated by labels: {labels}

Initial file presentation sequence: {initial_sequence}

The prosecution has derived the most logical true chronological timeline R* (chosen from {k} possible timeline hypotheses, but it is not yet disclosed to you). Your tasks are:
1. Identify the true chronological timeline R*
2. Reorder the current files into the true timeline using as few file position swaps as possible

You can perform the following operations (one at a time):

1. **Query Restructuring Steps**: Get the minimum number of swaps needed from the current sequence to the true timeline
   Format: <query_distance></query_distance>

2. **Test Swap**: Hypothetically swap files at positions i and j on the case board, query the resulting steps (does not change actual file sequence)
   Format: <test_swap>i,j</test_swap>
   Example: <test_swap>1,3</test_swap> means test swapping evidence files at position 1 and position 3

3. **Execute Swap**: Actually swap files at positions i and j in the archives (changes current presentation sequence)
   Format: <do_swap>i,j</do_swap>
   Example: <do_swap>2,4</do_swap> means actually swap evidence files at position 2 and position 4

4. **Query Current Evidence Chain**: View the current file arrangement sequence
   Format: <query_sequence></query_sequence>

5. **Declare Target Timeline**: Submit your final file sequence when you've identified the true timeline
   Format: <answer>label1,label2,...,label{n}</answer>
   Example: <answer>{example_answer}</answer>

- Correctly identify the true chronological timeline R*
- Number of actual swaps equals the initial minimum restructuring steps (optimal count)

- Declare the wrong timeline sequence
- Number of actual swaps exceeds the initial minimum steps
- Format error

Note: File position indices range from 1 to {n}.
"""

    tags = ["answer", "query_distance", "test_swap", "do_swap", "query_sequence"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "labels": ["A", "B", "C", "D"],
                "initial": ["D", "B", "C", "A"],
                "candidates": [
                    ["A", "B", "C", "D"],
                    ["B", "A", "D", "C"],
                    ["C", "D", "A", "B"],
                ],
                "target_index": 0,
            },
            2: {
                "n": 5,
                "labels": ["A", "B", "C", "D", "E"],
                "initial": ["E", "D", "C", "B", "A"],
                "candidates": [
                    ["A", "B", "C", "D", "E"],
                    ["C", "B", "A", "E", "D"],
                    ["B", "D", "C", "A", "E"],
                    ["A", "E", "C", "D", "B"],
                ],
                "target_index": 3,
            },
            3: {
                "n": 5,
                "labels": ["P", "Q", "R", "S", "T"],
                "initial": ["S", "R", "Q", "P", "T"],
                "candidates": [
                    ["P", "Q", "R", "S", "T"],
                    ["Q", "P", "S", "R", "T"],
                    ["T", "R", "Q", "S", "P"],
                    ["P", "R", "Q", "T", "S"],
                ],
                "target_index": 0,
            },
            4: {
                "n": 6,
                "labels": ["X", "Y", "Z", "U", "V", "W"],
                "initial": ["W", "V", "U", "Z", "Y", "X"],
                "candidates": [
                    ["X", "Y", "Z", "U", "V", "W"],
                    ["Y", "X", "U", "Z", "W", "V"],
                    ["Z", "Y", "X", "W", "V", "U"],
                    ["X", "Z", "Y", "V", "U", "W"],
                    ["U", "V", "W", "X", "Y", "Z"],
                ],
                "target_index": 1,
            },
            5: {
                "n": 6,
                "labels": ["M", "N", "O", "P", "Q", "R"],
                "initial": ["R", "Q", "P", "O", "N", "M"],
                "candidates": [
                    ["M", "N", "O", "P", "Q", "R"],
                    ["N", "M", "P", "O", "R", "Q"],
                    ["O", "P", "M", "N", "R", "Q"],
                    ["M", "P", "O", "R", "N", "Q"],
                    ["P", "O", "N", "M", "Q", "R"],
                ],
                "target_index": 2,
            },
        },
        "en": {
            1: {
                "n": 4,
                "labels": ["A", "B", "C", "D"],
                "initial": ["D", "B", "C", "A"],
                "candidates": [
                    ["A", "B", "C", "D"],
                    ["B", "A", "D", "C"],
                    ["C", "D", "A", "B"],
                ],
                "target_index": 0,
            },
            2: {
                "n": 5,
                "labels": ["A", "B", "C", "D", "E"],
                "initial": ["E", "D", "C", "B", "A"],
                "candidates": [
                    ["A", "B", "C", "D", "E"],
                    ["C", "B", "A", "E", "D"],
                    ["B", "D", "C", "A", "E"],
                    ["A", "E", "C", "D", "B"],
                ],
                "target_index": 3,
            },
            3: {
                "n": 5,
                "labels": ["P", "Q", "R", "S", "T"],
                "initial": ["S", "R", "Q", "P", "T"],
                "candidates": [
                    ["P", "Q", "R", "S", "T"],
                    ["Q", "P", "S", "R", "T"],
                    ["T", "R", "Q", "S", "P"],
                    ["P", "R", "Q", "T", "S"],
                ],
                "target_index": 0,
            },
            4: {
                "n": 6,
                "labels": ["X", "Y", "Z", "U", "V", "W"],
                "initial": ["W", "V", "U", "Z", "Y", "X"],
                "candidates": [
                    ["X", "Y", "Z", "U", "V", "W"],
                    ["Y", "X", "U", "Z", "W", "V"],
                    ["Z", "Y", "X", "W", "V", "U"],
                    ["X", "Z", "Y", "V", "U", "W"],
                    ["U", "V", "W", "X", "Y", "Z"],
                ],
                "target_index": 1,
            },
            5: {
                "n": 6,
                "labels": ["M", "N", "O", "P", "Q", "R"],
                "initial": ["R", "Q", "P", "O", "N", "M"],
                "candidates": [
                    ["M", "N", "O", "P", "Q", "R"],
                    ["N", "M", "P", "O", "R", "Q"],
                    ["O", "P", "M", "N", "R", "Q"],
                    ["M", "P", "O", "R", "N", "Q"],
                    ["P", "O", "N", "M", "Q", "R"],
                ],
                "target_index": 2,
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
        self._game_info["labels"] = ", ".join(cfg["labels"])
        self._game_info["k"] = len(cfg["candidates"])
        self._game_info["initial_sequence"] = ", ".join(cfg["initial"])
        self._game_info["example_answer"] = ",".join(cfg["initial"][:cfg["n"]])
        
        self.labels = cfg["labels"]
        self.current_sequence = cfg["initial"][:]
        self.target_sequence = cfg["candidates"][cfg["target_index"]]
        self.candidates = cfg["candidates"]
        
        self.initial_distance = self._compute_swap_distance(cfg["initial"], self.target_sequence)
        self.swap_count = 0
        self.has_queried_initial_distance = False

    def _compute_swap_distance(self, seq1, seq2):
        if len(seq1) != len(seq2):
            return -1
        
        n = len(seq1)
        pos_in_target = {label: i for i, label in enumerate(seq2)}
        
        perm = []
        for label in seq1:
            if label not in pos_in_target:
                return -1
            perm.append(pos_in_target[label])
        
        visited = [False] * n
        cycle_count = 0
        
        for i in range(n):
            if not visited[i]:
                cycle_count += 1
                j = i
                while not visited[j]:
                    visited[j] = True
                    j = perm[j]
        
        return n - cycle_count

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        try:
            model_sequence = [x.strip() for x in raw_ans.split(",")]
        except:
            return False
        
        if model_sequence != self.target_sequence:
            return False
        
        if self.swap_count != self.initial_distance:
            return False
        
        if self.current_sequence != self.target_sequence:
            return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            lang = "zh"
        else:
            lang = "en"
        
        if "query_distance" in parsed_info:
            distance = self._compute_swap_distance(self.current_sequence, self.target_sequence)
            
            if not self.has_queried_initial_distance and self.swap_count == 0:
                self.initial_distance = distance
                self.has_queried_initial_distance = True
            
            if lang == "zh":
                return f"距离 = {distance}"
            else:
                return f"Distance = {distance}"
        
        elif "test_swap" in parsed_info:
            try:
                raw = parsed_info["test_swap"].strip()
                parts = raw.split(",")
                if len(parts) != 2:
                    raise ValueError
                i, j = int(parts[0].strip()), int(parts[1].strip())
                
                if i > j:
                    i, j = j, i
                
                if i < 1 or j > self._game_info["n"] or i == j:
                    raise ValueError
                
                temp_seq = self.current_sequence[:]
                temp_seq[i-1], temp_seq[j-1] = temp_seq[j-1], temp_seq[i-1]
                
                test_distance = self._compute_swap_distance(temp_seq, self.target_sequence)
                
                if lang == "zh":
                    return f"若对调({i},{j})，距离 = {test_distance}"
                else:
                    return f"If swap({i},{j}), distance = {test_distance}"
                
            except:
                if lang == "zh":
                    return "错误：格式无效或位置编号错误。"
                else:
                    return "Error: Invalid format or position index."
        
        elif "do_swap" in parsed_info:
            try:
                raw = parsed_info["do_swap"].strip()
                parts = raw.split(",")
                if len(parts) != 2:
                    raise ValueError
                i, j = int(parts[0].strip()), int(parts[1].strip())
                
                if i > j:
                    i, j = j, i
                
                if i < 1 or j > self._game_info["n"] or i == j:
                    raise ValueError
                
                self.current_sequence[i-1], self.current_sequence[j-1] = \
                    self.current_sequence[j-1], self.current_sequence[i-1]
                self.swap_count += 1
                
                new_distance = self._compute_swap_distance(self.current_sequence, self.target_sequence)
                
                if self.initial_distance is not None and self.swap_count > self.initial_distance:
                    if lang == "zh":
                        return f"已对调({i},{j})。新距离 = {new_distance}。当前序列 = {self.current_sequence}。警告：对调次数已超过初始距离！"
                    else:
                        return f"Swapped({i},{j}). New distance = {new_distance}. Current sequence = {self.current_sequence}. Warning: Swap count exceeded initial distance!"
                
                if lang == "zh":
                    return f"已对调({i},{j})。新距离 = {new_distance}。当前序列 = {self.current_sequence}"
                else:
                    return f"Swapped({i},{j}). New distance = {new_distance}. Current sequence = {self.current_sequence}"
                
            except:
                if lang == "zh":
                    return "错误：格式无效或位置编号错误。"
                else:
                    return "Error: Invalid format or position index."
        
        elif "query_sequence" in parsed_info:
            if lang == "zh":
                return f"当前序列 = {self.current_sequence}"
            else:
                return f"Current sequence = {self.current_sequence}"
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        import re as _re
        
        def _replace_number(match):
            num = int(match.group(0))
            return str(num + 1)
        
        if _re.search(r'\d+', correct):
            wrong = _re.sub(r'\d+', _replace_number, correct, count=1)
            if wrong != correct:
                return wrong
        
        if "sequence" in correct.lower() or "序列" in correct:
            list_match = _re.search(r"\[([^\]]+)\]", correct)
            if list_match:
                items = [x.strip().strip("'\"") for x in list_match.group(1).split(",")]
                if len(items) >= 2:
                    items[0], items[1] = items[1], items[0]
                    new_list = "[" + ", ".join(f"'{x}'" for x in items) + "]"
                    return correct[:list_match.start()] + new_list + correct[list_match.end():]
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        n = self._game_info["n"]
        lang = self.config.language
        
        dist = self._compute_swap_distance(self.current_sequence, self.target_sequence)
        if lang == "zh":
            ans_dist = f"距离 = {dist}"
        else:
            ans_dist = f"Distance = {dist}"
        results.append({
            "query": "<query_distance></query_distance>",
            "answer": ans_dist
        })
        
        seq_str = str(self.current_sequence)
        if lang == "zh":
            ans_seq = f"当前序列 = {seq_str}"
        else:
            ans_seq = f"Current sequence = {seq_str}"
        results.append({
            "query": "<query_sequence></query_sequence>",
            "answer": ans_seq
        })
        
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                temp_seq = self.current_sequence[:]
                temp_seq[i-1], temp_seq[j-1] = temp_seq[j-1], temp_seq[i-1]
                test_dist = self._compute_swap_distance(temp_seq, self.target_sequence)
                
                if lang == "zh":
                    ans_test = f"若对调({i},{j})，距离 = {test_dist}"
                else:
                    ans_test = f"If swap({i},{j}), distance = {test_dist}"
                
                results.append({
                    "query": f"<test_swap>{i},{j}</test_swap>",
                    "answer": ans_test
                })
        
        target = self.target_sequence
        pos_in_target = {label: idx for idx, label in enumerate(target)}
        
        for i in range(n):
            while self.current_sequence[i] != target[i]:
                correct_pos = pos_in_target[self.current_sequence[i]]
                idx1, idx2 = i + 1, correct_pos + 1
                if idx1 > idx2:
                    idx1, idx2 = idx2, idx1
                
                ans_do = self._cf_core_produce({"do_swap": f"{idx1},{idx2}"})
                results.append({
                    "query": f"<do_swap>{idx1},{idx2}</do_swap>",
                    "answer": ans_do
                })
        
        return results