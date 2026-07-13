from .base import Game
import math

class PeakFindingGame(Game):

    game_rule_zh = """\
我们现在来玩一个"寻找极大值"的推理游戏，规则如下：

游戏设定了一个长度为 {n} 的整数序列 V[1..{n}]，序列中的所有元素两两不相等。我已秘密设定好这个序列，在整个游戏过程中它保持不变。

你的目标是找到序列中值最大的元素所在的位置。你可以通过查询来获取信息，但查询次数是有限的。

## 可用的查询类型

1. **比较查询**：询问位置 i 和位置 j 的元素哪个更大（i 和 j 必须不同，且在 1 到 {n} 范围内）。
   我会回答"位置 i 更大"或"位置 j 更大"。

2. **声明答案**：当你确定答案后，声明你认为的极大值位置。此操作只能执行一次，执行后游戏结束。

## 查询与答案格式（必须严格遵守）

- 比较查询（例如比较位置 3 和位置 5）：
<query_compare>3,5</query_compare>

- 声明答案（例如认为位置 7 是极大值）：
<answer>7</answer>

## 游戏目标

请尽可能用少的比较查询次数找到极大值位置。如果比较查询次数过多或声明的答案错误，游戏将失败。
"""

    game_rule_en = """\
Let's play a "Peak Finding" deduction game. Here are the rules:

There is a sequence V[1..{n}] of {n} integers. All elements in the sequence are distinct. I have secretly set up this sequence, and it remains unchanged throughout the game.

Your goal is to find the position of the element with the maximum value in the sequence. You can obtain information through queries, but the number of queries is limited.

## Available Query Types

1. **Comparison Query**: Ask which element is larger between position i and position j (i and j must be different and within the range 1 to {n}).
   I will answer "Position i is larger" or "Position j is larger".

2. **Declare Answer**: When you are certain, declare the position you believe to be the maximum. This operation can only be performed once, and the game ends after execution.

## Query and Answer Format (strictly required)

- Comparison Query (e.g., comparing position 3 and position 5):
<query_compare>3,5</query_compare>

- Declare Answer (e.g., believing position 7 is the maximum):
<answer>7</answer>

## Game Objective

Please find the maximum value position using as few comparison queries as possible. If you use too many comparison queries or declare an incorrect answer, the game will fail.
"""

    contextualized_rule_zh_1 = """\
我们现在来进行一项"定位拥堵中心"的交通网络分析任务，规则如下：

交通指挥系统监控着一条主干道上连续分布的 {n} 个监控节点，编号为 1 到 {n}，形成序列 V[1..{n}]。每个节点的实时车流量各不相同。我已在系统中锁定了这些节点的车流量数据，在此次排查过程中数据保持不变。

你的目标是找到车流量最大的监控节点（即绝对拥堵中心）所在的位置编号。你可以通过调用系统查询来比较节点数据，但系统查询接口的调用次数是有限的。

## 可用的查询类型

1. **比较查询**：询问位置 i 和位置 j 的节点哪一个车流量更大（i 和 j 必须不同，且在 1 到 {n} 范围内）。
   系统会反馈"位置 i 更大"或"位置 j 更大"。

2. **声明答案**：当你确定拥堵中心后，声明你认为的车流量最大的节点位置。此操作只能执行一次，执行后排查任务结束。

## 查询与答案格式（必须严格遵守）

- 比较查询（例如比较位置 3 和位置 5 的车流量）：
<query_compare>3,5</query_compare>

- 声明答案（例如认为位置 7 是拥堵中心）：
<answer>7</answer>

## 任务目标

请尽可能用少的比较查询次数找到拥堵中心位置。如果比较查询次数超过系统预算或声明的位置错误，任务将失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's conduct a "Locate the Congestion Center" traffic network analysis task. Here are the rules:

The traffic command system monitors {n} consecutive surveillance nodes along a main road, numbered 1 to {n}, forming a sequence V[1..{n}]. The real-time traffic volume at each node is distinct. I have locked the traffic data of these nodes in the system, and it remains unchanged throughout this investigation.

Your goal is to find the position number of the monitoring node with the maximum traffic volume (the absolute congestion center). You can obtain information by querying the system to compare node data, but the number of API calls for system queries is limited.

## Available Query Types

1. **Comparison Query**: Ask which node has a larger traffic volume between position i and position j (i and j must be different and within the range 1 to {n}).
   The system will answer "Position i is larger" or "Position j is larger".

2. **Declare Answer**: When you are certain of the congestion center, declare the position you believe to have the maximum traffic volume. This operation can only be performed once, and the task ends after execution.

## Query and Answer Format (strictly required)

- Comparison Query (e.g., comparing traffic volume at position 3 and position 5):
<query_compare>3,5</query_compare>

- Declare Answer (e.g., believing position 7 is the congestion center):
<answer>7</answer>

## Task Objective

Please find the congestion center position using as few comparison queries as possible. If you use too many comparison queries or declare an incorrect position, the task will fail.
"""

    contextualized_rule_zh_2 = """\
我们现在来进行一项"寻找抗体浓度峰值"的医疗生化分析任务，规则如下：

实验室中有一组按时间顺序连续采样的 {n} 个血液样本，编号为 1 到 {n}，形成序列 V[1..{n}]。每个样本中某种关键抗体的浓度各不相同。我已记录了这些样本的真实浓度数据，在整个分析过程中该数据保持不变。

你的目标是找到抗体浓度最高的样本（即峰值点）所在的编号位置。你可以通过生化测试仪进行比对查询，但测试仪器的使用次数是有限的。

## 可用的查询类型

1. **比较查询**：测试位置 i 和位置 j 的样本哪一个抗体浓度更高（i 和 j 必须不同，且在 1 到 {n} 范围内）。
   测试仪会反馈"位置 i 更大"或"位置 j 更大"。

2. **声明答案**：当你确定抗体浓度最高的样本后，声明你认为的峰值点位置。此操作只能执行一次，执行后分析任务结束。

## 查询与答案格式（必须严格遵守）

- 比较查询（例如比较位置 3 和位置 5 的样本浓度）：
<query_compare>3,5</query_compare>

- 声明答案（例如认为位置 7 是浓度峰值）：
<answer>7</answer>

## 任务目标

请尽可能用少的比较查询次数找到抗体浓度最高的样本位置。如果比较查询次数超过测试预算或声明的样本位置错误，分析将宣告失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct a "Find the Antibody Concentration Peak" medical biochemical analysis task. Here are the rules:

The laboratory has a set of {n} consecutive blood samples collected in chronological order, numbered 1 to {n}, forming a sequence V[1..{n}]. The concentration of a critical antibody in each sample is distinct. I have recorded the true concentration data of these samples, and it remains unchanged throughout the analysis.

Your goal is to find the position number of the sample with the maximum antibody concentration (the peak point). You can conduct comparison queries using a biochemical tester, but the number of tests is limited.

## Available Query Types

1. **Comparison Query**: Test which sample has a higher antibody concentration between position i and position j (i and j must be different and within the range 1 to {n}).
   The tester will answer "Position i is larger" or "Position j is larger".

2. **Declare Answer**: When you are certain of the sample with the highest concentration, declare the position you believe to be the peak point. This operation can only be performed once, and the task ends after execution.

## Query and Answer Format (strictly required)

- Comparison Query (e.g., comparing sample concentration at position 3 and position 5):
<query_compare>3,5</query_compare>

- Declare Answer (e.g., believing position 7 is the concentration peak):
<answer>7</answer>

## Task Objective

Please find the position of the sample with the highest antibody concentration using as few comparison queries as possible. If you use too many comparison queries or declare an incorrect position, the analysis will fail.
"""

    contextualized_rule_zh_3 = """\
我们现在来进行一项"寻找最优干预班级"的教育评估任务，规则如下：

教育系统中有一组按干预强度排序的 {n} 个测试班级，编号为 1 到 {n}，形成序列 V[1..{n}]。每个班级的平均成绩提升幅度各不相同。我已在后台锁定了这些班级的成绩评估数据，在整个评估过程中数据保持不变。

你的目标是找到成绩提升幅度最大的班级（即最优干预班级）所在的位置编号。你可以通过调取评估系统查询数据对比，但系统的调用次数是有限的。

## 可用的查询类型

1. **比较查询**：询问位置 i 和位置 j 的班级哪一个成绩提升幅度更大（i 和 j 必须不同，且在 1 到 {n} 范围内）。
   系统会反馈"位置 i 更大"或"位置 j 更大"。

2. **声明答案**：当你确定最优干预班级后，声明你认为提升幅度最大的班级位置。此操作只能执行一次，执行后评估任务结束。

## 查询与答案格式（必须严格遵守）

- 比较查询（例如比较位置 3 和位置 5 的班级提升幅度）：
<query_compare>3,5</query_compare>

- 声明答案（例如认为位置 7 是最优干预班级）：
<answer>7</answer>

## 任务目标

请尽可能用少的比较查询次数找到成绩提升最大的班级位置。如果比较查询次数超过系统限制或声明的班级位置错误，评估任务将失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct an "Identify the Optimal Intervention Class" educational evaluation task. Here are the rules:

The educational system includes a set of {n} test classes sorted by intervention intensity, numbered 1 to {n}, forming a sequence V[1..{n}]. The average score improvement magnitude of each class is distinct. I have locked the performance evaluation data of these classes in the backend, and it remains unchanged throughout the evaluation process.

Your goal is to find the position number of the class with the maximum score improvement magnitude (the optimal intervention class). You can query the evaluation system for data comparison, but the number of system calls is limited.

## Available Query Types

1. **Comparison Query**: Ask which class has a larger score improvement magnitude between position i and position j (i and j must be different and within the range 1 to {n}).
   The system will answer "Position i is larger" or "Position j is larger".

2. **Declare Answer**: When you are certain of the optimal intervention class, declare the position you believe to have the maximum improvement. This operation can only be performed once, and the evaluation task ends after execution.

## Query and Answer Format (strictly required)

- Comparison Query (e.g., comparing score improvement between position 3 and position 5):
<query_compare>3,5</query_compare>

- Declare Answer (e.g., believing position 7 is the optimal intervention class):
<answer>7</answer>

## Task Objective

Please find the position of the class with the highest score improvement using as few comparison queries as possible. If you use too many comparison queries or declare an incorrect class position, the evaluation task will fail.
"""

    contextualized_rule_zh_4 = """\
我们现在来进行一项"定位核心热区"的工业流水线故障排查任务，规则如下：

一条精密合金制造流水线上有 {n} 个连续分布的温度控制区域，编号为 1 到 {n}，形成序列 V[1..{n}]。每个区域的实时炉温各不相同。我已通过传感器记录了这些区域的温度分布数据，在排查过程中该状态保持不变。

你的目标是找到炉温最高的区域（即核心热区）所在的位置编号。你可以使用温差传感设备对比区域温度，但设备的探测次数是有限的。

## 可用的查询类型

1. **比较查询**：探测位置 i 和位置 j 的温控区域哪一个炉温更高（i 和 j 必须不同，且在 1 到 {n} 范围内）。
   传感设备会反馈"位置 i 更大"或"位置 j 更大"。

2. **声明答案**：当你确定核心热区后，声明你认为的炉温最高区域位置。此操作只能执行一次，执行后排查任务结束。

## 查询与答案格式（必须严格遵守）

- 比较查询（例如探测位置 3 和位置 5 的温度高低）：
<query_compare>3,5</query_compare>

- 声明答案（例如认为位置 7 是核心热区）：
<answer>7</answer>

## 任务目标

请尽可能用少的比较查询次数找到核心热区的位置。如果比较查询次数超过探测预算或声明的区域位置错误，排查任务将失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's conduct a "Locate the Core Hot Zone" industrial pipeline troubleshooting task. Here are the rules:

A precision alloy manufacturing pipeline has {n} consecutive temperature control zones, numbered 1 to {n}, forming a sequence V[1..{n}]. The real-time furnace temperature of each zone is distinct. I have recorded the temperature distribution data of these zones via sensors, and this state remains unchanged during the troubleshooting process.

Your goal is to find the position number of the zone with the maximum furnace temperature (the core hot zone). You can use temperature differential sensing equipment to compare zone temperatures, but the number of equipment detections is limited.

## Available Query Types

1. **Comparison Query**: Detect which temperature control zone has a higher furnace temperature between position i and position j (i and j must be different and within the range 1 to {n}).
   The sensing equipment will answer "Position i is larger" or "Position j is larger".

2. **Declare Answer**: When you are certain of the core hot zone, declare the position you believe to have the highest furnace temperature. This operation can only be performed once, and the troubleshooting task ends after execution.

## Query and Answer Format (strictly required)

- Comparison Query (e.g., detecting temperature differences between position 3 and position 5):
<query_compare>3,5</query_compare>

- Declare Answer (e.g., believing position 7 is the core hot zone):
<answer>7</answer>

## Task Objective

Please find the core hot zone position using as few comparison queries as possible. If you use too many comparison queries or declare an incorrect zone position, the troubleshooting task will fail.
"""

    contextualized_rule_zh_5 = """\
我们现在来进行一项"锁定核心侵权证据"的知识产权案件取证任务，规则如下：

案件卷宗中有一系列按时间顺序编号的 {n} 份关键通讯记录，编号为 1 到 {n}，形成序列 V[1..{n}]。每份记录中包含的商业机密泄露敏感度评分各不相同。我已在加密法务系统中确立了这些记录的敏感度评分，在整个取证过程中评分保持不变。

你的目标是找到敏感度评分最高的通讯记录（即核心侵权证据）所在的位置编号。你可以通过调用法律分析工具进行评分对比，但工具的查询调用次数是有限的。

## 可用的查询类型

1. **比较查询**：对比位置 i 和位置 j 的通讯记录哪一个敏感度评分更高（i 和 j 必须不同，且在 1 到 {n} 范围内）。
   分析工具会反馈"位置 i 更大"或"位置 j 更大"。

2. **声明答案**：当你确定核心侵权证据后，声明你认为敏感度最高记录的位置。此操作只能执行一次，执行后取证任务结束。

## 查询与答案格式（必须严格遵守）

- 比较查询（例如对比位置 3 和位置 5 的敏感度评分）：
<query_compare>3,5</query_compare>

- 声明答案（例如认为位置 7 是核心侵权证据）：
<answer>7</answer>

## 任务目标

请尽可能用少的比较查询次数找到核心侵权证据的位置。如果比较查询次数超过工具使用限制或声明的记录位置错误，取证任务将面临失败。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct a "Lock the Core Infringement Evidence" evidence collection task for an intellectual property case. Here are the rules:

The case file contains a series of {n} key communication records numbered in chronological order from 1 to {n}, forming a sequence V[1..{n}]. The leakage sensitivity score of trade secrets contained in each record is distinct. I have established the sensitivity scores of these records in the encrypted legal system, and they remain unchanged throughout the evidence collection process.

Your goal is to find the position number of the communication record with the maximum sensitivity score (the core infringement evidence). You can use legal analysis tools to compare scores, but the number of queries is limited.

## Available Query Types

1. **Comparison Query**: Compare which communication record has a higher sensitivity score between position i and position j (i and j must be different and within the range 1 to {n}).
   The analysis tool will answer "Position i is larger" or "Position j is larger".

2. **Declare Answer**: When you are certain of the core infringement evidence, declare the position you believe to have the highest sensitivity score. This operation can only be performed once, and the evidence collection task ends after execution.

## Query and Answer Format (strictly required)

- Comparison Query (e.g., comparing sensitivity scores between position 3 and position 5):
<query_compare>3,5</query_compare>

- Declare Answer (e.g., believing position 7 is the core infringement evidence):
<answer>7</answer>

## Task Objective

Please find the position of the core infringement evidence using as few comparison queries as possible. If you use too many comparison queries or declare an incorrect record position, the evidence collection task will fail.
"""

    tags = ["answer", "query_compare"]
    reasoning_type = "归纳推理"
    data_structure = "序列"

    # 难度配置说明：
    # 1 (简单)       - N=7,  预算=6  (ceil(log2(7)) + 3 = 3 + 3)
    # 2 (中等偏下)   - N=10, 预算=7  (ceil(log2(10)) + 3 = 4 + 3)
    # 3 (中等偏上)   - N=15, 预算=7  (ceil(log2(15)) + 3 = 4 + 3)
    # 4 (较难)       - N=20, 预算=8  (ceil(log2(20)) + 3 = 5 + 3)
    # 5 (难)         - N=30, 预算=8  (ceil(log2(30)) + 3 = 5 + 3)

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 7,
                "sequence": [10, 25, 40, 55, 45, 30, 15],  # 峰值在位置4
                "peak_position": 4,
            },
            2: {
                "n": 10,
                "sequence": [5, 12, 23, 38, 50, 62, 55, 40, 28, 10],  # 峰值在位置6
                "peak_position": 6,
            },
            3: {
                "n": 15,
                "sequence": [8, 15, 24, 35, 48, 63, 80, 99, 85, 70, 58, 45, 33, 20, 10],  # 峰值在位置8
                "peak_position": 8,
            },
            4: {
                "n": 20,
                "sequence": [3, 9, 17, 28, 41, 56, 73, 92, 113, 136, 160, 145, 128, 110, 91, 71, 50, 35, 18, 5],  # 峰值在位置11
                "peak_position": 11,
            },
            5: {
                "n": 30,
                "sequence": [2, 7, 14, 23, 34, 47, 62, 79, 98, 119, 142, 167, 194, 223, 254, 287, 260, 235, 212, 191, 172, 155, 140, 127, 116, 107, 100, 95, 92, 91],  # 峰值在位置16
                "peak_position": 16,
            },
        },
        "en": {
            1: {
                "n": 7,
                "sequence": [10, 25, 40, 55, 45, 30, 15],
                "peak_position": 4,
            },
            2: {
                "n": 10,
                "sequence": [5, 12, 23, 38, 50, 62, 55, 40, 28, 10],
                "peak_position": 6,
            },
            3: {
                "n": 15,
                "sequence": [8, 15, 24, 35, 48, 63, 80, 99, 85, 70, 58, 45, 33, 20, 10],
                "peak_position": 8,
            },
            4: {
                "n": 20,
                "sequence": [3, 9, 17, 28, 41, 56, 73, 92, 113, 136, 160, 145, 128, 110, 91, 71, 50, 35, 18, 5],
                "peak_position": 11,
            },
            5: {
                "n": 30,
                "sequence": [2, 7, 14, 23, 34, 47, 62, 79, 98, 119, 142, 167, 194, 223, 254, 287, 260, 235, 212, 191, 172, 155, 140, 127, 116, 107, 100, 95, 92, 91],
                "peak_position": 16,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：根据语言和难度设置序列和峰值位置"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        
        # 设置序列和真实峰值位置
        self.sequence = cfg["sequence"]
        self.peak_position = cfg["peak_position"]
        
        # 计算查询预算：ceil(log2(N)) + 3
        self.budget = math.ceil(math.log2(cfg["n"])) + 3
        self.query_count = 0  # 当前已使用的查询次数

    def evaluate(self, parsed_info):
        """评估答案是否正确"""
        try:
            # 解析答案：应该是一个整数位置
            raw_ans = parsed_info["answer"].strip()
            declared_position = int(raw_ans)
            
            # 检查位置是否在有效范围内
            if declared_position < 1 or declared_position > self._game_info["n"]:
                return False
            
            # 检查是否是真实的峰值位置
            return declared_position == self.peak_position
            
        except (ValueError, KeyError):
            return False

    def _cf_core_produce(self, parsed_info):
        """原始的业务逻辑处理方法"""
        if self.config.language == "zh":
            budget_exceeded = f"查询次数超过限制（{self.budget}次）。游戏失败。"
            invalid_format = "错误：格式无效。比较查询需要两个不同的位置，格式为 i,j"
            out_of_range = "错误：位置超出范围或相同。"
            pos_larger_template = "位置 {pos} 更大"
        else:
            budget_exceeded = f"Query limit exceeded ({self.budget} queries). Game failed."
            invalid_format = "Error: Invalid format. Comparison query requires two different positions in format i,j"
            out_of_range = "Error: Position out of range or identical."
            pos_larger_template = "Position {pos} is larger"

        # 处理比较查询
        if "query_compare" in parsed_info:
            # 检查是否超过预算
            if self.query_count >= self.budget:
                self.state.set_state("failed", "query budget exceeded")
                return budget_exceeded
            
            try:
                raw = parsed_info["query_compare"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                
                i, j = int(parts[0]), int(parts[1])
                
                # 验证位置有效性
                n = self._game_info["n"]
                if i < 1 or i > n or j < 1 or j > n or i == j:
                    return out_of_range
                
                # 增加查询计数
                self.query_count += 1
                
                # 执行比较（注意：序列索引从0开始，但位置从1开始）
                if self.sequence[i - 1] > self.sequence[j - 1]:
                    return pos_larger_template.format(pos=i)
                else:
                    return pos_larger_template.format(pos=j)
                    
            except (ValueError, IndexError):
                return invalid_format
        
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
        queries = []
        n = self._game_info["n"]
        
        # 预先定义模版以匹配 _cf_core_produce 中的逻辑
        if self.config.language == "zh":
            pos_larger_template = "位置 {pos} 更大"
        else:
            pos_larger_template = "Position {pos} is larger"
            
        # 只枚举 i < j 的无序对，减少冗余
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                # 构造查询字符串 "<query_compare>i,j</query_compare>" (对应 query_compare 标签的内容)
                query_content = f"<query_compare>{i},{j}</query_compare>"
                
                # 模拟逻辑计算答案
                # 注意：self.sequence 是 0-indexed，但查询位置是 1-indexed
                val_i = self.sequence[i - 1]
                val_j = self.sequence[j - 1]
                
                if val_i > val_j:
                    ans = pos_larger_template.format(pos=i)
                else:
                    ans = pos_larger_template.format(pos=j)
                
                queries.append({
                    "query": query_content,
                    "answer": ans
                })
                
        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        """根据正确的比较结果生成一个翻转的错误结果"""
        import re
        
        # 中文格式："位置 X 更大"
        zh_match = re.search(r'位置\s*(\d+)\s*更大', correct)
        if zh_match:
            correct_pos = int(zh_match.group(1))
            # 需要找到这次比较的另一个位置
            # 由于我们无法直接从 correct 中得知另一个位置，
            # 简单地将位置替换为一个不同的位置
            wrong_pos = correct_pos + 1 if correct_pos < self._game_info["n"] else correct_pos - 1
            return f"位置 {wrong_pos} 更大"
        
        # 英文格式："Position X is larger"
        en_match = re.search(r'Position\s*(\d+)\s*is larger', correct)
        if en_match:
            correct_pos = int(en_match.group(1))
            wrong_pos = correct_pos + 1 if correct_pos < self._game_info["n"] else correct_pos - 1
            return f"Position {wrong_pos} is larger"
        
        # fallback
        return correct + "_WRONG"

    def step(self, response: str):
        """重写step方法以添加预算检查"""
        try:
            parsed_info = self.parse(response)
            if "answer" in parsed_info:
                is_success = self.evaluate(parsed_info)
                if is_success:
                    res = "答案正确" if self.config.language == "zh" else "Correct answer."
                    self.state.set_state("success", "success")
                    self.state.add_message("user", res)
                else:
                    res = "答案错误" if self.config.language == "zh" else "Incorrect answer."
                    self.state.set_state("failed", "incorrect answer")
                    self.state.add_message("user", res)
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))    
        
        return self.state