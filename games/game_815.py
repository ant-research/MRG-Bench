# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   条件首末位：满足某条件的第一个/最后一个元素在哪个位置
# ============================================================

from .base import Game
import re


class PeriodicBinarySequenceGame(Game):

    game_rule_zh = """\
我们来玩一个"周期性二值序列推理"游戏，规则如下：

游戏设定了一个长度为 {n} 的有序二值序列 S，索引范围为 1 到 {n}。序列中每个位置的值为 0 或 1。

这个序列由一个隐藏的周期性生成机制确定，该机制由三个未知参数控制：
- 周期 P：一个 3 到 12 之间的整数
- 亮段长度 K：一个 1 到 P-1 之间的整数
- 相位偏移 A：一个 1 到 P 之间的整数

生成规则如下：
- 在无限整数线上，周期起点为 A, A+P, A+2P, ...
- 每个周期区间内，前 K 个位置为 1，其余为 0
- 序列 S 是这个无限周期序列在索引 1 到 {n} 范围内的截取

保证条件：
- 在 1 到 {n} 范围内至少包含两个完整周期起点
- 序列中至少存在一个位置的值为 1

你可以通过以下三种查询来探索序列（总查询次数应尽可能少）：

1. 单点查询：询问某个索引 i 的值是否为 1
2. 区间首个 1 查询：询问某个区间 [l, r] 内第一个值为 1 的索引位置
3. 区间计数查询：询问某个区间 [l, r] 内有多少个位置的值为 1

你的目标是：找出序列 S 中最后一个值为 1 的位置（即最大的索引 i 使得 S[i] = 1）。

## 查询和提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 单点查询（例如查询索引 5）：
<query_point>5</query_point>

- 区间首个 1 查询（例如查询区间 [3, 10]）：
<query_first>3,10</query_first>

- 区间计数查询（例如查询区间 [1, 20]）：
<query_count>1,20</query_count>

提交最终答案时，请直接给出你认为最后一个值为 1 的索引（一个整数），格式如下：

<answer>42</answer>
"""

    game_rule_en = """\
Let's play a "Periodic Binary Sequence Deduction" game. Here are the rules:

The game defines an ordered binary sequence S of length {n}, with indices ranging from 1 to {n}. Each position in the sequence has a value of either 0 or 1.

This sequence is determined by a hidden periodic generation mechanism controlled by three unknown parameters:
- Period P: an integer between 3 and 12
- Bright segment length K: an integer between 1 and P-1
- Phase offset A: an integer between 1 and P

Generation rules:
- On an infinite integer line, period starting points are at A, A+P, A+2P, ...
- Within each period interval, the first K positions are 1, and the rest are 0
- Sequence S is the truncation of this infinite periodic sequence within the index range 1 to {n}

Guaranteed conditions:
- The range 1 to {n} contains at least two complete period starting points
- At least one position in the sequence has a value of 1

You can explore the sequence through three types of queries (total number of queries should be minimized):

1. Point Query: ask whether the value at index i is 1
2. Interval First-1 Query: ask for the first index position with value 1 in interval [l, r]
3. Interval Count Query: ask how many positions have value 1 in interval [l, r]

Your goal is: find the last position with value 1 in sequence S (i.e., the maximum index i such that S[i] = 1).

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Point Query (e.g., querying index 5):
<query_point>5</query_point>

- Interval First-1 Query (e.g., querying interval [3, 10]):
<query_first>3,10</query_first>

- Interval Count Query (e.g., querying interval [1, 20]):
<query_count>1,20</query_count>

When submitting the final answer, directly provide the index you believe is the last position with value 1 (an integer), using this format:

<answer>42</answer>
"""

    contextualized_rule_zh_1 = """\
智能交通信号灯周期推理系统：

系统记录了某关键路口在时间序列 1 到 {n} 范围内的信号灯状态。每个时间片段的值为 0 或 1，其中 1 代表“绿灯通行”，0 代表“红灯禁行”。

该路口的信号灯受一个隐藏的固定周期控制机制调节：
- 周期 P：3 到 12 之间的整数
- 绿灯时长 K：1 到 P-1 之间的整数
- 初始相位 A：1 到 P 之间的整数（周期起点的偏移量）

规则：
- 周期起点位于 A, A+P, A+2P, ...
- 每个周期内，前 K 个时间片段为绿灯（1），其余为红灯（0）
- 该序列是截取自索引 1 到 {n} 的实际交通记录

保证条件：至少包含两个完整的信号周期起点，且至少有一次绿灯通行状态。

您可以通过以下三种指令查询信号记录（请尽量减少查询次数）：
1. 单点查询：询问时间片段 i 是否为绿灯
<query_point>i</query_point>
2. 区间首次绿灯查询：询问时间区间 [l, r] 内第一次出现绿灯的时间点
<query_first>l,r</query_first>
3. 区间绿灯计数查询：询问时间区间 [l, r] 内共有多少个绿灯时间片段
<query_count>l,r</query_count>

您的目标是：找出该记录中【最后一次为绿灯】的时间片段索引。
提交最终答案的格式：
<answer>42</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Intelligent Traffic Signal Periodic Deduction System:

The system logs the traffic light status at a key intersection over a time sequence from 1 to {n}. Each time interval is recorded as 0 or 1, where 1 indicates "Green Light (Pass)" and 0 indicates "Red Light (Stop)".

The traffic signal is regulated by a hidden fixed-cycle mechanism:
- Cycle length P: an integer between 3 and 12
- Green light duration K: an integer between 1 and P-1
- Phase offset A: an integer between 1 and P (start of the cycle)

Rules:
- Cycle start points occur at A, A+P, A+2P, ...
- Within each cycle, the first K intervals are green (1), and the rest are red (0)
- The sequence is a real traffic log truncated to indices 1 to {n}

Guarantees: The sequence contains at least two full cycle starts and at least one green light interval.

You can query the signal log using three commands (minimize your queries):
1. Point Query: ask if interval i was green
<query_point>i</query_point>
2. Interval First-Green Query: ask for the first green light interval in [l, r]
<query_first>l,r</query_first>
3. Interval Green Count Query: ask how many green intervals occurred in [l, r]
<query_count>l,r</query_count>

Your goal is: find the last time interval that was green (the maximum index i where S[i] = 1).
Submit your final answer as:
<answer>42</answer>
"""

    contextualized_rule_zh_2 = """\
靶向药物有效浓度监测系统：

系统记录了患者在监测窗口 1 到 {n} 范围内的血药浓度状态。每个监测窗口的值为 0 或 1，其中 1 代表“浓度达标（有效）”，0 代表“浓度未达标（无效）”。

药物在体内的代谢受一个隐藏的周期性生物节律控制：
- 代谢周期 P：3 到 12 之间的整数
- 药效维持时长 K：1 到 P-1 之间的整数
- 初始起效相位 A：1 到 P 之间的整数（周期起点的偏移量）

规则：
- 周期起点位于 A, A+P, A+2P, ...
- 每个周期内，前 K 个监测窗口药物浓度达标（1），其余未达标（0）
- 该序列是截取自索引 1 到 {n} 的实际监测记录

保证条件：至少包含两个完整的代谢周期起点，且至少有一次浓度达标状态。

您可以通过以下三种指令查询浓度记录（请尽量减少查询次数）：
1. 单点查询：询问监测窗口 i 浓度是否达标
<query_point>i</query_point>
2. 区间首次达标查询：询问窗口区间 [l, r] 内第一次出现浓度达标的时间点
<query_first>l,r</query_first>
3. 区间达标计数查询：询问窗口区间 [l, r] 内共有多少个浓度达标的窗口
<query_count>l,r</query_count>

您的目标是：找出该记录中【最后一次浓度达标】的监测窗口索引。
提交最终答案的格式：
<answer>42</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Targeted Drug Concentration Monitoring System:

The system logs a patient's blood drug concentration status over monitoring windows from 1 to {n}. Each window is recorded as 0 or 1, where 1 indicates "Target Concentration Reached (Effective)" and 0 indicates "Target Not Reached (Ineffective)".

The drug's metabolism is controlled by a hidden periodic biorhythm mechanism:
- Metabolism cycle P: an integer between 3 and 12
- Effective duration K: an integer between 1 and P-1
- Initial onset phase A: an integer between 1 and P (start of the cycle)

Rules:
- Cycle start points occur at A, A+P, A+2P, ...
- Within each cycle, the first K windows are effective (1), and the rest are ineffective (0)
- The sequence is a real monitoring log truncated to indices 1 to {n}

Guarantees: The sequence contains at least two full metabolism cycle starts and at least one effective window.

You can query the concentration log using three commands (minimize your queries):
1. Point Query: ask if window i was effective
<query_point>i</query_point>
2. Interval First-Effective Query: ask for the first effective window in [l, r]
<query_first>l,r</query_first>
3. Interval Effective Count Query: ask how many effective windows occurred in [l, r]
<query_count>l,r</query_count>

Your goal is: find the last monitoring window that was effective (the maximum index i where S[i] = 1).
Submit your final answer as:
<answer>42</answer>
"""

    contextualized_rule_zh_3 = """\
学生课堂专注度追踪系统：

系统记录了某学生在课程时间序列 1 到 {n} 分钟内的状态。每一分钟的值为 0 或 1，其中 1 代表“高度专注”，0 代表“注意力分散”。

学生的注意力受一个隐藏的周期性生理规律控制：
- 专注周期 P：3 到 12 之间的整数
- 专注维持时长 K：1 到 P-1 之间的整数
- 初始清醒相位 A：1 到 P 之间的整数（周期起点的偏移量）

规则：
- 周期起点位于 A, A+P, A+2P, ...
- 每个周期内，前 K 分钟处于高度专注（1），其余时间注意力分散（0）
- 该序列是截取自索引 1 到 {n} 的实际课堂记录

保证条件：至少包含两个完整的专注周期起点，且至少有一次高度专注状态。

您可以通过以下三种指令查询专注度记录（请尽量减少查询次数）：
1. 单点查询：询问第 i 分钟是否高度专注
<query_point>i</query_point>
2. 区间首次专注查询：询问时间区间 [l, r] 内第一次出现高度专注的时间点
<query_first>l,r</query_first>
3. 区间专注计数查询：询问时间区间 [l, r] 内共有多少分钟处于高度专注
<query_count>l,r</query_count>

您的目标是：找出该记录中【最后一次处于高度专注】的分钟索引。
提交最终答案的格式：
<answer>42</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Student Classroom Focus Tracking System:

The system logs a student's attention status over class minutes from 1 to {n}. Each minute is recorded as 0 or 1, where 1 indicates "Highly Focused" and 0 indicates "Distracted".

The student's attention is controlled by a hidden periodic physiological rhythm:
- Focus cycle P: an integer between 3 and 12
- Focus sustained duration K: an integer between 1 and P-1
- Initial awake phase A: an integer between 1 and P (start of the cycle)

Rules:
- Cycle start points occur at A, A+P, A+2P, ...
- Within each cycle, the first K minutes are highly focused (1), and the rest are distracted (0)
- The sequence is a real classroom log truncated to indices 1 to {n}

Guarantees: The sequence contains at least two full focus cycle starts and at least one highly focused minute.

You can query the focus log using three commands (minimize your queries):
1. Point Query: ask if minute i was highly focused
<query_point>i</query_point>
2. Interval First-Focus Query: ask for the first highly focused minute in [l, r]
<query_first>l,r</query_first>
3. Interval Focus Count Query: ask how many highly focused minutes occurred in [l, r]
<query_count>l,r</query_count>

Your goal is: find the last minute that was highly focused (the maximum index i where S[i] = 1).
Submit your final answer as:
<answer>42</answer>
"""

    contextualized_rule_zh_4 = """\
自动化数控机床作业周期分析系统：

系统记录了某机床在工作序列 1 到 {n} 个节拍内的运行状态。每个节拍的值为 0 或 1，其中 1 代表“激活加工状态”，0 代表“冷却待机状态”。

机床的运行受一个隐藏的自动化周期控制程序设定：
- 工作周期 P：3 到 12 之间的整数
- 连续加工时长 K：1 到 P-1 之间的整数
- 初始启动相位 A：1 到 P 之间的整数（周期起点的偏移量）

规则：
- 周期起点位于 A, A+P, A+2P, ...
- 每个周期内，前 K 个节拍处于激活加工状态（1），其余处于冷却待机状态（0）
- 该序列是截取自索引 1 到 {n} 的实际机床遥测记录

保证条件：至少包含两个完整的工作周期起点，且至少有一次处于激活加工状态。

您可以通过以下三种指令查询机床记录（请尽量减少查询次数）：
1. 单点查询：询问节拍 i 是否处于激活加工状态
<query_point>i</query_point>
2. 区间首次加工查询：询问区间 [l, r] 内第一次出现激活加工状态的节拍
<query_first>l,r</query_first>
3. 区间加工计数查询：询问区间 [l, r] 内共有多少个节拍处于激活加工状态
<query_count>l,r</query_count>

您的目标是：找出该记录中【最后一次处于激活加工状态】的节拍索引。
提交最终答案的格式：
<answer>42</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Automated CNC Machine Operation Cycle Analysis System:

The system logs a machine's operational status over production beats from 1 to {n}. Each beat is recorded as 0 or 1, where 1 indicates "Active Processing State" and 0 indicates "Cooling Standby State".

The machine's operation is controlled by a hidden periodic automation protocol:
- Working cycle P: an integer between 3 and 12
- Continuous processing duration K: an integer between 1 and P-1
- Initial startup phase A: an integer between 1 and P (start of the cycle)

Rules:
- Cycle start points occur at A, A+P, A+2P, ...
- Within each cycle, the first K beats are in active processing (1), and the rest are in cooling standby (0)
- The sequence is a real telemetry log truncated to indices 1 to {n}

Guarantees: The sequence contains at least two full working cycle starts and at least one active processing beat.

You can query the telemetry log using three commands (minimize your queries):
1. Point Query: ask if beat i was actively processing
<query_point>i</query_point>
2. Interval First-Processing Query: ask for the first active processing beat in [l, r]
<query_first>l,r</query_first>
3. Interval Processing Count Query: ask how many active processing beats occurred in [l, r]
<query_count>l,r</query_count>

Your goal is: find the last beat that was in active processing (the maximum index i where S[i] = 1).
Submit your final answer as:
<answer>42</answer>
"""

    contextualized_rule_zh_5 = """\
专利授权动态有效性核验系统：

系统记录了某核心专利在审查序列 1 到 {n} 个自然月内的授权状态。每个月份的值为 0 或 1，其中 1 代表“处于合法有效状态”，0 代表“处于中止审查或失效期”。

该专利的有效性受一个隐藏的周期性法律续展规则控制：
- 续展周期 P：3 到 12 之间的整数
- 有效期窗口 K：1 到 P-1 之间的整数
- 初始核准相位 A：1 到 P 之间的整数（周期起点的偏移量）

规则：
- 周期起点位于 A, A+P, A+2P, ...
- 每个周期内，前 K 个月专利处于合法有效状态（1），其余月份失效（0）
- 该序列是截取自索引 1 到 {n} 的实际法律档案记录

保证条件：至少包含两个完整的续展周期起点，且至少有一次处于合法有效状态。

您可以通过以下三种指令查询专利记录（请尽量减少查询次数）：
1. 单点查询：询问月份 i 是否合法有效
<query_point>i</query_point>
2. 区间首次有效查询：询问区间 [l, r] 内第一次出现合法有效状态的月份
<query_first>l,r</query_first>
3. 区间有效计数查询：询问区间 [l, r] 内共有多少个月份处于合法有效状态
<query_count>l,r</query_count>

您的目标是：找出该档案中【最后一次处于合法有效状态】的月份序列号。
提交最终答案的格式：
<answer>42</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Patent Licensing Dynamic Validity Verification System:

The system logs a core patent's licensing status over review months from 1 to {n}. Each month is recorded as 0 or 1, where 1 indicates "Legally Valid State" and 0 indicates "Suspended Review / Expired State".

The patent's validity is controlled by a hidden periodic legal renewal mechanism:
- Renewal cycle P: an integer between 3 and 12
- Valid window duration K: an integer between 1 and P-1
- Initial approval phase A: an integer between 1 and P (start of the cycle)

Rules:
- Cycle start points occur at A, A+P, A+2P, ...
- Within each cycle, the first K months are legally valid (1), and the rest are expired/suspended (0)
- The sequence is a real legal archive log truncated to indices 1 to {n}

Guarantees: The sequence contains at least two full renewal cycle starts and at least one legally valid month.

You can query the archive log using three commands (minimize your queries):
1. Point Query: ask if month i was legally valid
<query_point>i</query_point>
2. Interval First-Valid Query: ask for the first legally valid month in [l, r]
<query_first>l,r</query_first>
3. Interval Valid Count Query: ask how many legally valid months occurred in [l, r]
<query_count>l,r</query_count>

Your goal is: find the last month that was legally valid (the maximum index i where S[i] = 1).
Submit your final answer as:
<answer>42</answer>
"""

    tags = ["answer", "query_point", "query_first", "query_count"]
    
    reasoning_type = "归纳推理"
    data_structure = "序列"

    # 难度配置说明：
    # 1 (简单)      - N=30, P=5, K=2, A=2 （周期短，亮段短，容易定位）
    # 2 (中等偏下)  - N=50, P=7, K=3, A=4 （周期稍长，需要更多查询）
    # 3 (中等偏上)  - N=80, P=9, K=4, A=5 （序列更长，周期更复杂）
    # 4 (较难)      - N=100, P=11, K=5, A=7 （大周期，需要精确定位）
    # 5 (难)        - N=120, P=12, K=6, A=3 （最大周期，长序列，高难度）

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 30,
                "P": 5,
                "K": 2,
                "A": 2,
            },
            2: {
                "n": 50,
                "P": 7,
                "K": 3,
                "A": 4,
            },
            3: {
                "n": 80,
                "P": 9,
                "K": 4,
                "A": 5,
            },
            4: {
                "n": 100,
                "P": 11,
                "K": 5,
                "A": 7,
            },
            5: {
                "n": 120,
                "P": 12,
                "K": 6,
                "A": 3,
            },
        },
        "en": {
            1: {
                "n": 30,
                "P": 5,
                "K": 2,
                "A": 2,
            },
            2: {
                "n": 50,
                "P": 7,
                "K": 3,
                "A": 4,
            },
            3: {
                "n": 80,
                "P": 9,
                "K": 4,
                "A": 5,
            },
            4: {
                "n": 100,
                "P": 11,
                "K": 5,
                "A": 7,
            },
            5: {
                "n": 120,
                "P": 12,
                "K": 6,
                "A": 3,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏参数和序列"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        
        import random as _rng
        rng = _rng.Random()
        
        # 隐藏参数
        self.P = cfg["P"]  # 周期
        self.K = cfg["K"]  # 亮段长度
        # 对 A 引入随机性，保证每次游戏不同
        self.A = rng.randint(1, self.P)
        self.N = cfg["n"]  # 序列长度
        
        # 生成完整序列
        self.sequence = self._generate_sequence()
        
        # 计算正确答案：最后一个值为 1 的索引
        self.correct_answer = None
        for i in range(self.N, 0, -1):
            if self.sequence[i] == 1:
                self.correct_answer = i
                break
        
        # 查询计数器
        self.query_count = 0
        self.max_queries = 20

    def _generate_sequence(self):
        """根据周期参数生成二值序列"""
        sequence = {}
        for i in range(1, self.N + 1):
            offset = (i - self.A) % self.P
            if offset < self.K:
                sequence[i] = 1
            else:
                sequence[i] = 0
        return sequence

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        try:
            answer = int(parsed_info["answer"].strip())
            return answer == self.correct_answer
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始的响应生成逻辑"""
        # 检查是否超过最大查询次数
        if self.query_count >= self.max_queries:
            if self.config.language == "zh":
                return "错误：已超过最大查询次数限制。"
            else:
                return "Error: Maximum number of queries exceeded."
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            none_res = "无"
            invalid_res = "无效询问"
        else:
            yes_res, no_res = "Yes", "No"
            none_res = "None"
            invalid_res = "Invalid query"

        # 单点查询
        if "query_point" in parsed_info:
            try:
                i = int(parsed_info["query_point"].strip())
                if i < 1 or i > self.N:
                    return invalid_res
                self.query_count += 1
                return yes_res if self.sequence[i] == 1 else no_res
            except:
                return invalid_res

        # 区间首个 1 查询
        elif "query_first" in parsed_info:
            try:
                raw = parsed_info["query_first"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return invalid_res
                l, r = int(parts[0]), int(parts[1])
                if l < 1 or r > self.N or l > r:
                    return invalid_res
                self.query_count += 1
                
                # 查找区间内第一个值为 1 的索引
                for i in range(l, r + 1):
                    if self.sequence[i] == 1:
                        return str(i)
                return none_res
            except:
                return invalid_res

        # 区间计数查询
        elif "query_count" in parsed_info:
            try:
                raw = parsed_info["query_count"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return invalid_res
                l, r = int(parts[0]), int(parts[1])
                if l < 1 or r > self.N or l > r:
                    return invalid_res
                self.query_count += 1
                
                # 统计区间内值为 1 的个数
                count = sum(1 for i in range(l, r + 1) if self.sequence[i] == 1)
                return str(count)
            except:
                return invalid_res

        else:
            return invalid_res

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举有代表性的合法查询并返回对应的正确答案。
        为避免查询数量爆炸，区间查询只采样部分有代表性的区间。
        """
        results = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            none_res = "无"
        else:
            yes_res, no_res = "Yes", "No"
            none_res = "None"

        # 1. 单点查询（全部枚举，数量为 N）
        for i in range(1, self.N + 1):
            query_str = f"<query_point>{i}</query_point>"
            ans = yes_res if self.sequence[i] == 1 else no_res
            results.append({"query": query_str, "answer": ans})

        # 2. 采样有代表性的区间查询
        # 包括：整个区间、前半/后半、按周期长度划分的区间、以及一些随机区间
        import random as _rng
        rng = _rng.Random(42)
        sampled_intervals = set()
        
        # 关键区间
        sampled_intervals.add((1, self.N))
        sampled_intervals.add((1, self.N // 2))
        sampled_intervals.add((self.N // 2 + 1, self.N))
        
        # 按周期步长滑动的区间
        step = max(1, self.P)
        for start in range(1, self.N + 1, step):
            end = min(start + step - 1, self.N)
            sampled_intervals.add((start, end))
            end2 = min(start + 2 * step - 1, self.N)
            sampled_intervals.add((start, end2))
        
        # 随机采样一些区间
        for _ in range(min(30, self.N)):
            l = rng.randint(1, self.N)
            r = rng.randint(l, self.N)
            if l > r:
                l, r = r, l
            sampled_intervals.add((l, r))

        for l, r in sorted(sampled_intervals):
            # 区间首个 1 查询
            q_first_str = f"<query_first>{l},{r}</query_first>"
            first_idx = None
            for k in range(l, r + 1):
                if self.sequence[k] == 1:
                    first_idx = k
                    break
            ans_first = str(first_idx) if first_idx is not None else none_res
            results.append({"query": q_first_str, "answer": ans_first})

            # 区间计数查询
            q_count_str = f"<query_count>{l},{r}</query_count>"
            count_val = sum(1 for k in range(l, r + 1) if self.sequence[k] == 1)
            results.append({"query": q_count_str, "answer": str(count_val)})

        return results

    def _cf_make_wrong(self, correct):
        # 如果是纯整数字符串
        if correct.isdigit():
            return str(int(correct) + 1)
            
        # 处理 None / 无 
        if correct == "无":
            return "1"
        if correct.lower() == "none":
            return "1"
        
        # 中文是非判断
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        # 英文Yes/No (忽略大小写，保持风格)
        lower_correct = correct.lower()
        if lower_correct == "yes":
            if correct.isupper():
                return "NO"
            elif correct.islower():
                return "no"
            else:
                return "No"
        if lower_correct == "no":
            if correct.isupper():
                return "YES"
            elif correct.islower():
                return "yes"
            else:
                return "Yes"
        
        # 其他情况
        return correct + "_WRONG"