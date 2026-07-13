# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   区间聚合：某区间内所有元素的和/最大值/最小值是多少
# ============================================================

from .base import Game
import re


class SequenceReconstructionGame(Game):

    game_rule_zh = """\
我们现在来玩一个"序列重构"的推理游戏，规则如下：

游戏设定了一个长度为 {n} 的有序序列，序列中每个位置的值是 0 到 9 之间的整数（包含 0 和 9）。你的任务是通过查询来推断出这个完整的序列。

## 已知信息

1. 序列长度为 {n}
2. 序列所有元素的总和为 {total_sum}

## 查询规则

你可以进行区间和查询，每次查询需要指定一个连续区间的左端点 L 和右端点 R（位置编号从 1 到 {n}），我会告诉你这个区间内所有元素的和。

查询限制：
- 左端点 L 必须严格小于右端点 R
- 不能查询整个序列（即不能同时 L=1 且 R={n}）
- 请尽可能少地使用查询次数

## 查询格式

使用以下 XML 格式进行区间和查询：

<query>L,R</query>

例如，查询位置 2 到位置 5 的区间和：
<query>2,5</query>

## 提交答案格式

当你确定了完整序列后，请按顺序提交所有位置的值（用逗号分隔）：

<answer>x1,x2,x3,...,x{n}</answer>

例如，对于长度为 5 的序列：
<answer>3,1,4,1,5</answer>

注意：答案必须完全正确才算成功，任何位置的错误都会导致游戏失败。
"""

    game_rule_en = """\
Let's play a "Sequence Reconstruction" deduction game. Here are the rules:

A sequence of length {n} has been set up, where each position contains an integer between 0 and 9 (inclusive). Your task is to infer the complete sequence through queries.

## Given Information

1. The sequence has length {n}
2. The sum of all elements in the sequence is {total_sum}

## Query Rules

You can perform range sum queries. Each query requires specifying a left endpoint L and a right endpoint R of a continuous range (positions numbered from 1 to {n}), and I will tell you the sum of all elements in that range.

Query constraints:
- Left endpoint L must be strictly less than right endpoint R
- You cannot query the entire sequence (i.e., L=1 and R={n} simultaneously is not allowed)
- Please use as few queries as possible

## Query Format

Use the following XML format for range sum queries:

<query>L,R</query>

For example, to query the range sum from position 2 to position 5:
<query>2,5</query>

## Answer Submission Format

When you have determined the complete sequence, submit all position values in order (comma-separated):

<answer>x1,x2,x3,...,x{n}</answer>

For example, for a sequence of length 5:
<answer>3,1,4,1,5</answer>

Note: The answer must be completely correct to succeed. Any error in any position will result in game failure.
"""

    # ================= 场景 1：交通 =================
    contextualized_rule_zh_1 = """\
这是一套用于城市干线交通监控的智能系统。
系统正在监控一条由 {n} 个连续路段组成的快速路。每个路段的“拥堵指数”评级为 0 到 9 的整数。你的任务是通过调用区间监控接口，推断出每个路段的具体拥堵指数。

## 已知信息

1. 监控线路总共包含 {n} 个路段（编号从 1 到 {n}）
2. 整条线路的所有路段拥堵指数总和为 {total_sum}

## 查询规则

你可以调用区间聚合传感接口，每次查询需要指定一个连续路段的起点 L 和终点 R（位置编号从 1 到 {n}），系统会返回该区间内所有路段的拥堵指数之和。

查询限制：
- 起点 L 必须严格小于终点 R
- 接口不支持一次性查询整条线路（即不能同时 L=1 且 R={n}）
- 请尽可能少地消耗系统查询配额

## 查询格式

使用以下 XML 格式进行查询：

<query>L,R</query>

例如，查询第 2 路段到第 5 路段的拥堵指数之和：
<query>2,5</query>

## 提交答案格式

当排查出所有路段的拥堵指数后，请按顺序提交完整的数据序列（用逗号分隔）：

<answer>x1,x2,x3,...,x{n}</answer>

例如，对于长度为 5 的线路：
<answer>3,1,4,1,5</answer>

注意：上报的数据必须完全正确，任何一个路段的误判都将导致调度失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
This is an intelligent system for monitoring urban arterial traffic.
The system is monitoring an expressway consisting of {n} consecutive road segments. The "congestion index" for each segment is an integer ranging from 0 to 9. Your task is to deduce the exact congestion index of each segment by invoking the range monitoring interface.

## Given Information

1. The monitored route contains a total of {n} segments (numbered from 1 to {n})
2. The sum of the congestion indices for all segments on the route is {total_sum}

## Query Rules

You can invoke the range aggregation sensor interface. Each query requires specifying a starting point L and an ending point R (position numbers from 1 to {n}) of a continuous section, and the system will return the sum of the congestion indices for all segments in that range.

Query constraints:
- Starting point L must be strictly less than ending point R
- The interface does not support querying the entire route at once (i.e., L=1 and R={n} simultaneously is not allowed)
- Please consume as few system query quotas as possible

## Query Format

Use the following XML format for queries:

<query>L,R</query>

For example, to query the sum of congestion indices from segment 2 to segment 5:
<query>2,5</query>

## Answer Submission Format

Once you have determined the congestion indices for all segments, submit the complete data sequence in order (comma-separated):

<answer>x1,x2,x3,...,x{n}</answer>

For example, for a route of length 5:
<answer>3,1,4,1,5</answer>

Note: The reported data must be completely correct. Any misjudgment on any segment will result in a system dispatch failure.
"""

    # ================= 场景 2：医疗 =================
    contextualized_rule_zh_2 = """\
这是一套用于连续生理指标监测的辅助诊断系统。
系统记录了患者在连续的 {n} 个时间窗口内的生理监测数据。每个时间窗口的“异常指数”评定为 0 到 9 的整数。你的任务是通过调用区间聚合接口，精确推断出每个时间窗口的异常指数，以排查病因。

## 已知信息

1. 监测周期总共包含 {n} 个时间窗口（编号从 1 到 {n}）
2. 整个周期的异常指数总和为 {total_sum}

## 查询规则

你可以调用区间诊断接口，每次查询需要指定一个连续时间段的起始窗口 L 和结束窗口 R（编号从 1 到 {n}），系统会返回该时间段内所有窗口的异常指数之和。

查询限制：
- 起始窗口 L 必须严格小于结束窗口 R
- 接口不支持一次性查询整个周期（即不能同时 L=1 且 R={n}）
- 请尽可能少地消耗系统诊断次数

## 查询格式

使用以下 XML 格式进行查询：

<query>L,R</query>

例如，查询第 2 到第 5 窗口的异常指数之和：
<query>2,5</query>

## 提交答案格式

当推断出所有窗口的异常指数后，请按顺序提交完整的分析序列（用逗号分隔）：

<answer>x1,x2,x3,...,x{n}</answer>

例如，对于周期长度为 5 的监测：
<answer>3,1,4,1,5</answer>

注意：诊断结论必须完全正确，任何一个时间窗口的误判都将导致辅助诊断失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
This is an auxiliary diagnostic system for continuous physiological monitoring.
The system has recorded patient data over {n} consecutive time windows. The "anomaly index" for each window is evaluated as an integer from 0 to 9. Your task is to precisely deduce the anomaly index of each time window by querying the range aggregation interface to identify the underlying cause.

## Given Information

1. The monitoring period contains a total of {n} time windows (numbered from 1 to {n})
2. The total sum of anomaly indices across the entire period is {total_sum}

## Query Rules

You can invoke the range diagnostic interface. Each query requires specifying a starting window L and an ending window R (position numbers from 1 to {n}) of a continuous timeframe, and the system will return the sum of anomaly indices within that range.

Query constraints:
- Starting window L must be strictly less than ending window R
- The interface does not support querying the entire period at once (i.e., L=1 and R={n} simultaneously is not allowed)
- Please minimize the use of system diagnostic queries

## Query Format

Use the following XML format for queries:

<query>L,R</query>

For example, to query the sum of anomaly indices from window 2 to window 5:
<query>2,5</query>

## Answer Submission Format

Once you have deduced the anomaly indices for all windows, submit the complete analysis sequence in order (comma-separated):

<answer>x1,x2,x3,...,x{n}</answer>

For example, for a period of length 5:
<answer>3,1,4,1,5</answer>

Note: The diagnostic conclusion must be entirely correct. Any misjudgment in any time window will lead to the failure of the auxiliary diagnosis.
"""

    # ================= 场景 3：教育 =================
    contextualized_rule_zh_3 = """\
这是一套自适应学习路径规划的评估系统。
系统分析了学生在 {n} 个连续学习模块中的表现。每个模块遗留的“知识缺陷点”数量在 0 到 9 之间。你的任务是通过阶段性测试查询接口，推断出每个模块的具体缺陷点数量，以为学生定制补救计划。

## 已知信息

1. 学习路径总共包含 {n} 个模块（编号从 1 到 {n}）
2. 所有模块的知识缺陷点总和为 {total_sum}

## 查询规则

你可以调用阶段性综合测试接口，每次查询需要指定一个连续学习阶段的起始模块 L 和结束模块 R（编号从 1 到 {n}），系统会返回该阶段内的知识缺陷点之和。

查询限制：
- 起始模块 L 必须严格小于结束模块 R
- 不能一次性测试所有的模块（即不能同时 L=1 且 R={n}）
- 为了避免学生过度疲劳，请尽可能少地进行测试查询

## 查询格式

使用以下 XML 格式进行查询：

<query>L,R</query>

例如，查询第 2 模块到第 5 模块的缺陷点之和：
<query>2,5</query>

## 提交答案格式

当明确了所有模块的缺陷点后，请按顺序提交完整的评估序列（用逗号分隔）：

<answer>x1,x2,x3,...,x{n}</answer>

例如，对于包含 5 个模块的路径：
<answer>3,1,4,1,5</answer>

注意：评估结果必须完全正确，任何一个模块的遗漏都会影响最终的个性化学习方案。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
This is an evaluation system for adaptive learning path planning.
The system analyzes a student's performance across {n} consecutive learning modules. The number of lingering "knowledge deficits" per module ranges from 0 to 9. Your task is to deduce the exact number of deficits for each module using the phase-test query interface to customize a remedial plan for the student.

## Given Information

1. The learning path contains a total of {n} modules (numbered from 1 to {n})
2. The sum of knowledge deficits across all modules is {total_sum}

## Query Rules

You can invoke the comprehensive phase-test interface. Each query requires specifying a starting module L and an ending module R (position numbers from 1 to {n}) of a continuous phase, and the system will return the sum of knowledge deficits in that range.

Query constraints:
- Starting module L must be strictly less than ending module R
- You cannot test all modules at once (i.e., L=1 and R={n} simultaneously is not allowed)
- To avoid test fatigue for the student, please minimize the number of queries

## Query Format

Use the following XML format for queries:

<query>L,R</query>

For example, to query the total deficits from module 2 to module 5:
<query>2,5</query>

## Answer Submission Format

Once you have clearly identified the deficits for all modules, submit the complete evaluation sequence in order (comma-separated):

<answer>x1,x2,x3,...,x{n}</answer>

For example, for a path consisting of 5 modules:
<answer>3,1,4,1,5</answer>

Note: The evaluation must be perfectly accurate. Missing out on any module's deficit will compromise the final personalized learning plan.
"""

    # ================= 场景 4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
这是一套用于精密装配流水线的质量控制系统。
一条装配线由 {n} 个连续的加工工位组成，每个工位在加工时会引入 0 到 9 微米的“加工微量偏差”。你的任务是通过调用激光区间测距接口，推断出每一个工位产生的具体偏差值，以便指导机床校准。

## 已知信息

1. 装配线共有 {n} 个工位（编号从 1 到 {n}）
2. 经过所有工位后，成品的累计偏差总量为 {total_sum} 微米

## 查询规则

你可以调用激光累计测量接口，每次查询需要指定测量的起始工位 L 和结束工位 R（编号从 1 到 {n}），测量仪会返回该区间段内所有工位引入的偏差之和。

查询限制：
- 起始工位 L 必须严格小于结束工位 R
- 测量仪受限于轨道结构，不能直接测量整条产线的偏差（即不能同时 L=1 且 R={n}）
- 激光测量成本较高，请尽可能少地进行查询

## 查询格式

使用以下 XML 格式进行查询：

<query>L,R</query>

例如，测量第 2 工位到第 5 工位的累计偏差：
<query>2,5</query>

## 提交答案格式

当推断出所有工位的独立偏差后，请按顺序提交完整的偏差序列（用逗号分隔）：

<answer>x1,x2,x3,...,x{n}</answer>

例如，对于拥有 5 个工位的流水线：
<answer>3,1,4,1,5</answer>

注意：校准数据必须完全正确，任何一个工位的误判都将导致产品直接报废。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
This is a quality control system for a precision assembly line.
The assembly line consists of {n} consecutive processing stations. Each station introduces a "micro-machining deviation" between 0 and 9 micrometers. Your task is to deduce the exact deviation produced at each individual station by querying the laser range measurement interface, which will guide the machine calibration.

## Given Information

1. The assembly line has a total of {n} stations (numbered from 1 to {n})
2. After passing through all stations, the cumulative deviation of the final product is {total_sum} micrometers

## Query Rules

You can invoke the cumulative laser measurement interface. Each query requires specifying a starting station L and an ending station R (position numbers from 1 to {n}), and the instrument will return the total deviation accumulated within that segment.

Query constraints:
- Starting station L must be strictly less than ending station R
- Constrained by the track layout, the instrument cannot measure the entire assembly line at once (i.e., L=1 and R={n} simultaneously is not allowed)
- Laser measurements are costly; please minimize the number of queries

## Query Format

Use the following XML format for queries:

<query>L,R</query>

For example, to measure the cumulative deviation from station 2 to station 5:
<query>2,5</query>

## Answer Submission Format

Once you have deduced the independent deviations for all stations, submit the complete deviation sequence in order (comma-separated):

<answer>x1,x2,x3,...,x{n}</answer>

For example, for an assembly line with 5 stations:
<answer>3,1,4,1,5</answer>

Note: The calibration data must be absolutely exact. Any miscalculation at any station will cause the product to be scrapped.
"""

    # ================= 场景 5：法律 =================
    contextualized_rule_zh_5 = """\
这是一套用于追踪金融犯罪资金链的司法审计系统。
案卷显示，嫌疑人在连续的 {n} 个月内进行了非法资金转移。每个月的“非法转移金额”（单位：百万元）均为 0 到 9 的整数。你的任务是通过调取区间银行流水接口，推断出每个月确切的转移金额，完善检方的诉讼时间线。

## 已知信息

1. 调查周期共跨越 {n} 个月（编号从 1 到 {n}）
2. 整个涉案期间的非法转移资金总计为 {total_sum} 百万元

## 查询规则

你可以向司法接口提交流水协查请求，每次查询需要指定连续月份的起始月 L 和结束月 R（编号从 1 到 {n}），银行将反馈该周期内的非法转移总额。

查询限制：
- 起始月 L 必须严格小于结束月 R
- 受限于搜查令权限，不能一次性调取整个涉案周期的流水（即不能同时 L=1 且 R={n}）
- 调证流程繁琐，请尽可能精简查询次数

## 查询格式

使用以下 XML 格式进行查询：

<query>L,R</query>

例如，调取第 2 个月到第 5 个月的转移总计：
<query>2,5</query>

## 提交答案格式

当查实了所有月份的具体涉案金额后，请按时间顺序提交完整的资金序列（用逗号分隔）：

<answer>x1,x2,x3,...,x{n}</answer>

例如，对于周期为 5 个月的案件：
<answer>3,1,4,1,5</answer>

注意：审计报告的金额必须完全准确，任何一处的误差都会成为辩方推翻证据链的突破口。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
This is a forensic auditing system used to track the capital chains in financial crimes.
The case files indicate that the suspect made illegal fund transfers over {n} consecutive months. The "illegal transfer amount" (in millions) for each month is an integer from 0 to 9. Your task is to deduce the exact transfer amount for each month by subpoenaing range-based bank records to complete the prosecution's timeline.

## Given Information

1. The investigation period spans {n} months (numbered from 1 to {n})
2. The total sum of illegally transferred funds over the entire period is {total_sum} million

## Query Rules

You can submit a transaction verification request to the judicial interface. Each query requires specifying a starting month L and an ending month R (position numbers from 1 to {n}) of a continuous period, and the bank will return the total illicit transfer sum for that timeframe.

Query constraints:
- Starting month L must be strictly less than ending month R
- Restricted by the search warrant limits, you cannot subpoena the entire investigation period at once (i.e., L=1 and R={n} simultaneously is not allowed)
- The evidence retrieval process is tedious; please minimize the number of queries

## Query Format

Use the following XML format for queries:

<query>L,R</query>

For example, to query the total transfers from month 2 to month 5:
<query>2,5</query>

## Answer Submission Format

Once the precise amounts for all months are verified, submit the complete financial sequence chronologically (comma-separated):

<answer>x1,x2,x3,...,x{n}</answer>

For example, for a 5-month investigation:
<answer>3,1,4,1,5</answer>

Note: The audit report amounts must be completely accurate. Any discrepancy will serve as a loophole for the defense to invalidate the chain of evidence.
"""

    tags = ["answer", "query"]
    
    reasoning_type = "演绎推理"
    data_structure = "序列"

    # 难度配置（保留供外部调用参考，但不直接用于序列生成）
    # 1 (简单)      - N=4, 简单序列
    # 2 (中等偏下)  - N=6, 中等复杂度
    # 3 (中等偏上)  - N=8, 需要更多推理
    # 4 (较难)      - N=10, 复杂序列
    # 5 (难)        - N=12, 最复杂

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "sequence": [2, 5, 1, 3],  # 总和 11
            },
            2: {
                "n": 6,
                "sequence": [3, 1, 4, 1, 5, 9],  # 总和 23
            },
            3: {
                "n": 8,
                "sequence": [2, 7, 1, 8, 2, 8, 1, 8],  # 总和 37
            },
            4: {
                "n": 10,
                "sequence": [5, 3, 8, 9, 7, 9, 3, 2, 3, 8],  # 总和 57
            },
            5: {
                "n": 12,
                "sequence": [6, 2, 8, 3, 1, 8, 5, 3, 0, 9, 7, 4],  # 总和 56
            },
        },
        "en": {
            1: {
                "n": 4,
                "sequence": [2, 5, 1, 3],
            },
            2: {
                "n": 6,
                "sequence": [3, 1, 4, 1, 5, 9],
            },
            3: {
                "n": 8,
                "sequence": [2, 7, 1, 8, 2, 8, 1, 8],
            },
            4: {
                "n": 10,
                "sequence": [5, 3, 8, 9, 7, 9, 3, 2, 3, 8],
            },
            5: {
                "n": 12,
                "sequence": [6, 2, 8, 3, 1, 8, 5, 3, 0, 9, 7, 4],
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """
        根据配置初始化游戏：使用确定性种子生成序列，避免硬编码
        """
        import random as _random
        
        lang = self.config.language
        diff = int(self.config.difficulty)
        
        # 难度对应的序列长度
        DIFFICULTY_TO_N = {1: 4, 2: 6, 3: 8, 4: 10, 5: 12}
        
        if diff not in DIFFICULTY_TO_N:
            raise KeyError(f"Unsupported difficulty: {diff}")
        
        self.n = DIFFICULTY_TO_N[diff]
        
        # 使用确定性种子生成序列（每次相同难度+语言产生相同序列）
        seed = hash((lang, diff, "SequenceReconstructionGame")) % (2**32)
        rng = _random.Random(seed)
        self.sequence = [rng.randint(0, 9) for _ in range(self.n)]
        self.total_sum = sum(self.sequence)
        
        # 初始化查询计数器
        self.query_count = 0
        
        # 设置游戏信息用于规则模板
        self._game_info["n"] = self.n
        self._game_info["total_sum"] = self.total_sum

    def evaluate(self, parsed_info):
        """
        评估模型提交的答案是否正确
        答案格式：<answer>x1,x2,...,xn</answer>
        """
        raw_ans = parsed_info["answer"].strip()
        
        try:
            # 解析答案：逗号分隔的数字列表
            answer_list = [int(x.strip()) for x in raw_ans.split(",")]
            
            # 检查长度是否匹配
            if len(answer_list) != self.n:
                return False
            
            # 检查每个值是否在 0-9 范围内
            if not all(0 <= x <= 9 for x in answer_list):
                return False
            
            # 检查是否完全匹配目标序列
            return answer_list == self.sequence
            
        except (ValueError, AttributeError):
            return False

    def _cf_core_produce(self, parsed_info):
        if "query" not in parsed_info:
            if self.config.language == "zh":
                return "错误：未找到有效的查询标签。"
            else:
                return "Error: No valid query tag found."
        
        try:
            # 解析查询参数
            query_str = parsed_info["query"].strip()
            parts = [x.strip() for x in query_str.split(",")]
            
            if len(parts) != 2:
                raise ValueError("Query format error")
            
            L = int(parts[0])
            R = int(parts[1])
            
        except (ValueError, AttributeError):
            if self.config.language == "zh":
                return f"错误：查询格式无效。请使用格式 <query>L,R</query>，其中 L 和 R 是整数。"
            else:
                return f"Error: Invalid query format. Please use format <query>L,R</query> where L and R are integers."
        except Exception as e:
            if self.config.language == "zh":
                return f"错误：处理查询时发生异常。"
            else:
                return f"Error: Exception occurred while processing query."

        # 验证查询的合法性
        # 1. L 必须严格小于 R
        if L >= R:
            if self.config.language == "zh":
                return "错误：左端点必须严格小于右端点。"
            else:
                return "Error: Left endpoint must be strictly less than right endpoint."
        
        # 2. 端点必须在有效范围内
        if L < 1 or R > self.n:
            if self.config.language == "zh":
                return f"错误：查询范围必须在 1 到 {self.n} 之间。"
            else:
                return f"Error: Query range must be between 1 and {self.n}."
        
        # 3. 不能查询整个序列
        if L == 1 and R == self.n:
            if self.config.language == "zh":
                return "错误：不能查询整个序列。"
            else:
                return "Error: Cannot query the entire sequence."
        
        # 计算区间和（注意：序列索引从0开始，但查询位置从1开始）
        range_sum = sum(self.sequence[L-1:R])
        
        # 增加查询计数
        self.query_count += 1
        
        # 返回结果
        if self.config.language == "zh":
            return f"区间 [{L},{R}] 的和为：{range_sum}"
        else:
            return f"Sum of range [{L},{R}]: {range_sum}"

    def _cf_make_wrong(self, correct):
        import re as _re
        
        # 尝试找到响应中的数值并修改
        def _alter_number(m):
            val = int(m.group(0))
            return str(val + 1)

        # 找到最后一个独立数字（即结果部分）并修改
        if self.config.language == "zh":
            pattern = r'(?<=的和为：)\d+'
        else:
            pattern = r'(?<=: )\d+'

        new_resp = _re.sub(pattern, _alter_number, correct)
        if new_resp != correct:
            return new_resp

        # fallback：如果上面的模式没有匹配到，回退到通用逻辑
        match = list(_re.finditer(r'\d+', correct))
        if match:
            last = match[-1]
            altered_val = str(int(last.group(0)) + 1)
            return correct[:last.start()] + altered_val + correct[last.end():]

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
        possible_queries = []
        
        # L 从 1 遍历到 N-1
        # R 从 L+1 遍历到 N
        for L in range(1, self.n):
            for R in range(L + 1, self.n + 1):
                # 排除游戏规则禁止的“整个序列查询”
                if L == 1 and R == self.n:
                    continue
                
                # 构造查询字符串 (需要是合法的 XML 标签字符串)
                query_str = f"<query>{L},{R}</query>"
                
                # 计算正确答案（复用内部逻辑，不调用 produce_response 以避免增加计数器）
                range_sum = sum(self.sequence[L-1:R])
                
                if self.config.language == "zh":
                    answer_str = f"区间 [{L},{R}] 的和为：{range_sum}"
                else:
                    answer_str = f"Sum of range [{L},{R}]: {range_sum}"
                
                possible_queries.append({
                    "query": query_str,
                    "answer": answer_str
                })
        
        return possible_queries