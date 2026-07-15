from .base import Game
import random

class RangeMaxQueryGame(Game):

    game_rule_zh = """\
我们来玩一个"区间最大值推理"游戏，规则如下：

游戏设定了一个长度为 {n} 的整数序列 H[1..{n}]，序列中所有元素两两不相等。序列的具体数值已被隐藏，但你知道序列长度为 {n}。

你的目标是：找出序列中全局最大值的位置 k（位置编号从 1 到 {n}）。全局最大值的位置是唯一的。

你可以通过以下两种查询方式来收集信息（查询次数不限，但应尽可能少）：

1. 区间最大值查询（MAX 查询）：
   - 询问区间 [L, R] 内的最大值是多少。
   - L 和 R 必须满足：1 小于等于 L 小于等于 R 小于等于 {n}。
   - 我会返回该区间内的最大值。

2. 区间比较查询（CMP 查询）：
   - 询问两个不相交区间 [L1, R1] 和 [L2, R2] 的最大值哪个更大。
   - 要求：1 小于等于 L1 小于等于 R1 小于 L2 小于等于 R2 小于等于 {n}（左区间必须完全在右区间左侧且不相交）。
   - 我会返回 LEFT（左区间最大值更大）或 RIGHT（右区间最大值更大）。

如果查询格式错误或越界，我会返回 INVALID。

当你确定了全局最大值的位置后，请提交你的最终答案。

每次只能进行一个查询或提交一个答案。请使用以下 XML 格式：

- 区间最大值查询（例如查询区间 [2, 5]）：
<query_max>2,5</query_max>

- 区间比较查询（例如比较区间 [1, 3] 和 [5, 7]）：
<query_cmp>1,3,5,7</query_cmp>

- 提交最终答案（例如认为位置 3 是全局最大值位置）：
<answer>3</answer>
"""

    game_rule_en = """\
Let's play a "Range Max Query" deduction game. Here are the rules:

There is a hidden integer sequence H[1..{n}] of length {n}, where all elements are distinct. The specific values are hidden, but you know the sequence length is {n}.

Your goal is: Find the position k (indexed from 1 to {n}) of the global maximum value in the sequence. The position of the global maximum is unique.

You can collect information through the following two types of queries (unlimited queries, but try to use as few as possible):

1. Range Maximum Query (MAX query):
   - Ask for the maximum value in the range [L, R].
   - L and R must satisfy: 1 less than or equal to L less than or equal to R less than or equal to {n}.
   - I will return the maximum value in that range.

2. Range Comparison Query (CMP query):
   - Ask which of two non-overlapping ranges [L1, R1] and [L2, R2] has a larger maximum value.
   - Requirements: 1 less than or equal to L1 less than or equal to R1 less than L2 less than or equal to R2 less than or equal to {n} (left range must be completely to the left of and disjoint from right range).
   - I will return LEFT (left range has larger maximum) or RIGHT (right range has larger maximum).

If the query format is invalid or out of bounds, I will return INVALID.

When you have determined the position of the global maximum, please submit your final answer.

Each turn can only contain one query or one answer. Use the following XML format:

- Range Maximum Query (e.g., query range [2, 5]):
<query_max>2,5</query_max>

- Range Comparison Query (e.g., compare ranges [1, 3] and [5, 7]):
<query_cmp>1,3,5,7</query_cmp>

- Submit final answer (e.g., position 3 is the global maximum position):
<answer>3</answer>
"""

    contextualized_rule_zh_1 = """\
智慧交通路网指挥中心启动。系统已接入高速公路上 {n} 个连续的交通流量监测点（编号 1 到 {n}），各监测点的实时拥堵指数两两不同。为了及时疏导交通，你需要找出全局拥堵指数最高的核心拥堵点位置 k。

你可以通过以下两种查询方式来收集路况信息（查询次数不限，但应尽可能高效）：

1. 路段峰值查询（MAX 查询）：
   - 询问监测点区间 [L, R] 内的最高拥堵指数。
   - L 和 R 必须满足：1 小于等于 L 小于等于 R 小于等于 {n}。
   - 系统会返回该路段内的最高指数。

2. 路段峰值比较（CMP 查询）：
   - 询问两个不相交路段 [L1, R1] 和 [L2, R2] 哪个路段的最高拥堵指数更大。
   - 要求：1 小于等于 L1 小于等于 R1 小于 L2 小于等于 R2 小于等于 {n}（左路段必须完全在右路段左侧且不相交）。
   - 系统会返回 LEFT（左路段峰值更高）或 RIGHT（右路段峰值更高）。

如果查询格式错误或越界，系统会返回 INVALID。

当你确定了核心拥堵点的确切位置后，请提交最终答案。

每次只能进行一个查询或提交一个答案。请使用以下 XML 格式：

- 路段峰值查询（例如查询区间 [2, 5]）：
<query_max>2,5</query_max>

- 路段峰值比较（例如比较区间 [1, 3] 和 [5, 7]）：
<query_cmp>1,3,5,7</query_cmp>

- 提交最终答案（例如认为位置 3 是核心拥堵点）：
<answer>3</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Smart Traffic Network Command Center activated. The system is connected to {n} consecutive traffic flow monitoring points (numbered 1 to {n}) on a highway. The real-time congestion indices of these points are all distinct. To efficiently manage traffic, you need to find the exact position k of the core congestion point with the highest global congestion index.

You can collect traffic information through the following two types of queries (unlimited queries, but try to use as few as possible):

1. Range Peak Query (MAX query):
   - Ask for the highest congestion index in the monitoring point range [L, R].
   - L and R must satisfy: 1 less than or equal to L less than or equal to R less than or equal to {n}.
   - The system will return the highest index in that range.

2. Range Peak Comparison (CMP query):
   - Ask which of two non-overlapping ranges [L1, R1] and [L2, R2] has a larger peak congestion index.
   - Requirements: 1 less than or equal to L1 less than or equal to R1 less than L2 less than or equal to R2 less than or equal to {n} (left range must be completely to the left of and disjoint from right range).
   - The system will return LEFT (left range has a larger peak) or RIGHT (right range has a larger peak).

If the query format is invalid or out of bounds, the system will return INVALID.

When you have determined the exact position of the core congestion point, please submit your final answer.

Each turn can only contain one query or one answer. Use the following XML format:

- Range Peak Query (e.g., query range [2, 5]):
<query_max>2,5</query_max>

- Range Peak Comparison (e.g., compare ranges [1, 3] and [5, 7]):
<query_cmp>1,3,5,7</query_cmp>

- Submit final answer (e.g., position 3 is the core congestion point):
<answer>3</answer>
"""

    contextualized_rule_zh_2 = """\
神经内科脑电波分析系统就绪。患者的连续脑电波记录被划分为 {n} 个时间片段（编号 1 到 {n}），每个片段记录到的最高电位均不相同。你的任务是定位出全局最高异常电位出现的确切时间片段位置 k。

你可以通过以下两种查询方式来收集脑电信息（查询次数不限，但应尽可能少）：

1. 窗口峰值查询（MAX 查询）：
   - 询问时间片段区间 [L, R] 内的最大电位。
   - L 和 R 必须满足：1 小于等于 L 小于等于 R 小于等于 {n}。
   - 系统会返回该区间内的最大电位。

2. 窗口峰值比较（CMP 查询）：
   - 询问两个不相交时间窗口 [L1, R1] 和 [L2, R2] 哪个窗口的最大电位更高。
   - 要求：1 小于等于 L1 小于等于 R1 小于 L2 小于等于 R2 小于等于 {n}（左窗口必须完全在右窗口左侧且不相交）。
   - 系统会返回 LEFT（左窗口峰值更高）或 RIGHT（右窗口峰值更高）。

如果查询格式错误或越界，系统会返回 INVALID。

当你确定了最高异常电位的时间片段位置后，请提交最终诊断答案。

每次只能进行一个查询或提交一个诊断答案。请使用以下 XML 格式：

- 窗口峰值查询（例如查询区间 [2, 5]）：
<query_max>2,5</query_max>

- 窗口峰值比较（例如比较区间 [1, 3] 和 [5, 7]）：
<query_cmp>1,3,5,7</query_cmp>

- 提交最终答案（例如认为时间片段 3 出现全局最高异常电位）：
<answer>3</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Neurology EEG analysis system ready. The patient's continuous EEG recording is divided into {n} time segments (numbered 1 to {n}), and the maximum electrical potential recorded in each segment is distinct. Your task is to locate the exact time segment position k where the global maximum abnormal potential occurs.

You can collect EEG information through the following two types of queries (unlimited queries, but try to use as few as possible):

1. Window Peak Query (MAX query):
   - Ask for the maximum potential in the time segment range [L, R].
   - L and R must satisfy: 1 less than or equal to L less than or equal to R less than or equal to {n}.
   - The system will return the maximum potential in that range.

2. Window Peak Comparison (CMP query):
   - Ask which of two non-overlapping time windows [L1, R1] and [L2, R2] has a higher maximum potential.
   - Requirements: 1 less than or equal to L1 less than or equal to R1 less than L2 less than or equal to R2 less than or equal to {n} (left window must be completely to the left of and disjoint from right window).
   - The system will return LEFT (left window has a higher peak) or RIGHT (right window has a higher peak).

If the query format is invalid or out of bounds, the system will return INVALID.

When you have located the time segment position of the maximum abnormal potential, please submit your final diagnostic answer.

Each turn can only contain one query or one answer. Use the following XML format:

- Window Peak Query (e.g., query range [2, 5]):
<query_max>2,5</query_max>

- Window Peak Comparison (e.g., compare ranges [1, 3] and [5, 7]):
<query_cmp>1,3,5,7</query_cmp>

- Submit final answer (e.g., segment 3 is the location of the highest potential):
<answer>3</answer>
"""

    contextualized_rule_zh_3 = """\
区域教育质量评估系统已启动。学区内有 {n} 所连续编号的试点学校（编号 1 到 {n}），每所学校的综合教学评估分数互不相等。你的目标是：找出整个学区中综合评估分数最高的示范学校编号 k。

你可以通过以下两种调研方式来收集数据（查询次数不限，但应尽可能少）：

1. 学区区间峰值查询（MAX 查询）：
   - 询问学校区间 [L, R] 内的最高评估分。
   - L 和 R 必须满足：1 小于等于 L 小于等于 R 小于等于 {n}。
   - 系统会返回该区间内的最高分。

2. 学区区间比较（CMP 查询）：
   - 询问两组不相交学校区间 [L1, R1] 和 [L2, R2] 中，哪组的最高评估分更大。
   - 要求：1 小于等于 L1 小于等于 R1 小于 L2 小于等于 R2 小于等于 {n}（左侧学校组必须完全在右侧学校组编号之前且不相交）。
   - 系统会返回 LEFT（左区间最高分更大）或 RIGHT（右区间最高分更大）。

如果查询格式错误或越界，系统会返回 INVALID。

当你确定了得分最高的示范学校编号后，请提交你的最终答案。

每次只能进行一个查询或提交一个答案。请使用以下 XML 格式：

- 学区区间峰值查询（例如查询学校区间 [2, 5]）：
<query_max>2,5</query_max>

- 学区区间比较（例如比较学校区间 [1, 3] 和 [5, 7]）：
<query_cmp>1,3,5,7</query_cmp>

- 提交最终答案（例如认为学校 3 是得分最高的示范校）：
<answer>3</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Regional education quality assessment system activated. There are {n} consecutively numbered pilot schools (numbered 1 to {n}) in the district, and the comprehensive teaching evaluation score of each school is distinct. Your goal is: Find the position k of the model school with the highest comprehensive evaluation score in the entire district.

You can collect assessment data through the following two types of queries (unlimited queries, but try to use as few as possible):

1. District Range Peak Query (MAX query):
   - Ask for the highest evaluation score within the school range [L, R].
   - L and R must satisfy: 1 less than or equal to L less than or equal to R less than or equal to {n}.
   - The system will return the highest score in that range.

2. District Range Comparison (CMP query):
   - Ask which of two non-overlapping school ranges [L1, R1] and [L2, R2] has a larger maximum score.
   - Requirements: 1 less than or equal to L1 less than or equal to R1 less than L2 less than or equal to R2 less than or equal to {n} (left range must be completely before and disjoint from right range).
   - The system will return LEFT (left range has a larger maximum) or RIGHT (right range has a larger maximum).

If the query format is invalid or out of bounds, the system will return INVALID.

When you have determined the school number with the highest score, please submit your final answer.

Each turn can only contain one query or one answer. Use the following XML format:

- District Range Peak Query (e.g., query range [2, 5]):
<query_max>2,5</query_max>

- District Range Comparison (e.g., compare ranges [1, 3] and [5, 7]):
<query_cmp>1,3,5,7</query_cmp>

- Submit final answer (e.g., school 3 is the top model school):
<answer>3</answer>
"""

    contextualized_rule_zh_4 = """\
自动化流水线故障排查系统启动。当前生产线上有 {n} 个连续的质检工位（编号 1 到 {n}），各个工位统计出的零件缺陷率数值两两不同。你的任务是：精准定位出缺陷率最高的故障源头工位位置 k。

你可以通过以下两种检测指令收集工位数据（查询次数不限，但应尽可能高效）：

1. 工序区间峰值查询（MAX 查询）：
   - 询问工位区间 [L, R] 内的最高缺陷率数值。
   - L 和 R 必须满足：1 小于等于 L 小于等于 R 小于等于 {n}。
   - 系统会返回该区间内的最大值。

2. 工序区间比较（CMP 查询）：
   - 询问两段不相交工位区间 [L1, R1] 和 [L2, R2] 哪个区间的最高缺陷率更大。
   - 要求：1 小于等于 L1 小于等于 R1 小于 L2 小于等于 R2 小于等于 {n}（左侧区间必须完全在右侧区间前段且不相交）。
   - 系统会返回 LEFT（左区间峰值更大）或 RIGHT（右区间峰值更大）。

如果查询格式错误或越界，系统会返回 INVALID。

当你确定了缺陷率最高的故障工位后，请提交最终排查结果。

每次只能进行一个查询或提交一个答案。请使用以下 XML 格式：

- 工序区间峰值查询（例如查询区间 [2, 5]）：
<query_max>2,5</query_max>

- 工序区间比较（例如比较区间 [1, 3] 和 [5, 7]）：
<query_cmp>1,3,5,7</query_cmp>

- 提交最终答案（例如认为工位 3 是故障源头）：
<answer>3</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Automated assembly line troubleshooting system initiated. There are {n} consecutive quality inspection stations (numbered 1 to {n}) on the current production line, and the defect rate values detected at each station are all distinct. Your task is: Pinpoint the exact station position k with the highest defect rate as the source of the fault.

You can collect station data through the following two types of queries (unlimited queries, but try to use as few as possible):

1. Process Range Peak Query (MAX query):
   - Ask for the highest defect rate value in the station range [L, R].
   - L and R must satisfy: 1 less than or equal to L less than or equal to R less than or equal to {n}.
   - The system will return the maximum value in that range.

2. Process Range Comparison (CMP query):
   - Ask which of two non-overlapping station ranges [L1, R1] and [L2, R2] has a larger peak defect rate.
   - Requirements: 1 less than or equal to L1 less than or equal to R1 less than L2 less than or equal to R2 less than or equal to {n} (left range must be completely prior to and disjoint from right range).
   - The system will return LEFT (left range has a larger peak) or RIGHT (right range has a larger peak).

If the query format is invalid or out of bounds, the system will return INVALID.

When you have determined the faulty station with the highest defect rate, please submit your final troubleshooting result.

Each turn can only contain one query or one answer. Use the following XML format:

- Process Range Peak Query (e.g., query range [2, 5]):
<query_max>2,5</query_max>

- Process Range Comparison (e.g., compare ranges [1, 3] and [5, 7]):
<query_cmp>1,3,5,7</query_cmp>

- Submit final answer (e.g., station 3 is the source of the fault):
<answer>3</answer>
"""

    contextualized_rule_zh_5 = """\
经济犯罪案件审计系统就绪。在调查某企业的财务造假案中，我们锁定了 {n} 个连续月份的财务流水记录（月份编号 1 到 {n}），且每个月的最大单笔异常转移金额均不相同。你的目标是：找出全局异常转移金额最高的核心案发月份编号 k。

你可以通过以下两种审计手段来调取卷宗（查询次数不限，但应尽可能隐蔽）：

1. 审计区间峰值查询（MAX 查询）：
   - 询问月份区间 [L, R] 内的最高单笔异常金额。
   - L 和 R 必须满足：1 小于等于 L 小于等于 R 小于等于 {n}。
   - 系统会返回该区间内的最高金额。

2. 审计区间比较（CMP 查询）：
   - 比较两段不相交月份区间 [L1, R1] 和 [L2, R2]，询问哪段区间内存在更高的单笔异常金额。
   - 要求：1 小于等于 L1 小于等于 R1 小于 L2 小于等于 R2 小于等于 {n}（较早月份区间必须完全在较晚月份区间之前且不相交）。
   - 系统会返回 LEFT（左侧较早区间金额更高）或 RIGHT（右侧较晚区间金额更高）。

如果查询格式错误或越界，系统会返回 INVALID。

当你锁定核心案发月份后，请提交你的最终指控答案。

每次只能进行一个查询或提交一个答案。请使用以下 XML 格式：

- 审计区间峰值查询（例如查询月份区间 [2, 5]）：
<query_max>2,5</query_max>

- 审计区间比较（例如比较月份区间 [1, 3] 和 [5, 7]）：
<query_cmp>1,3,5,7</query_cmp>

- 提交最终答案（例如认为第 3 个月是核心案发月份）：
<answer>3</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Economic crime audit system ready. During the investigation of a corporate financial fraud case, we have secured {n} consecutive months of financial transaction records (numbered 1 to {n}), and the maximum single abnormal transfer amount in each month is distinct. Your goal is: Find the specific month position k with the global highest abnormal transfer amount.

You can retrieve files through the following two auditing methods (unlimited queries, but try to remain as discreet as possible):

1. Audit Range Peak Query (MAX query):
   - Ask for the highest single abnormal transfer amount within the month range [L, R].
   - L and R must satisfy: 1 less than or equal to L less than or equal to R less than or equal to {n}.
   - The system will return the highest amount in that range.

2. Audit Range Comparison (CMP query):
   - Compare two non-overlapping month ranges [L1, R1] and [L2, R2] to ask which range contains a higher single abnormal amount.
   - Requirements: 1 less than or equal to L1 less than or equal to R1 less than L2 less than or equal to R2 less than or equal to {n} (earlier month range must be completely before and disjoint from later month range).
   - The system will return LEFT (left/earlier range has a higher amount) or RIGHT (right/later range has a higher amount).

If the query format is invalid or out of bounds, the system will return INVALID.

When you have locked onto the core incident month, please submit your final accusatory answer.

Each turn can only contain one query or one answer. Use the following XML format:

- Audit Range Peak Query (e.g., query range [2, 5]):
<query_max>2,5</query_max>

- Audit Range Comparison (e.g., compare ranges [1, 3] and [5, 7]):
<query_cmp>1,3,5,7</query_cmp>

- Submit final answer (e.g., month 3 is the core incident month):
<answer>3</answer>
"""

    tags = ["answer", "query_max", "query_cmp"]
    
    reasoning_type = "演绎推理（明确的规则系统）"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "sequence": [10, 25, 15, 8, 12],
            },
            2: {
                "n": 8,
                "sequence": [34, 67, 23, 89, 45, 12, 56, 78],
            },
            3: {
                "n": 12,
                "sequence": [45, 67, 89, 34, 23, 91, 56, 78, 12, 43, 88, 76],
            },
            4: {
                "n": 16,
                "sequence": [45, 67, 23, 89, 34, 91, 56, 78, 93, 43, 88, 76, 54, 32, 65, 87],
            },
            5: {
                "n": 20,
                "sequence": [45, 67, 23, 89, 34, 91, 56, 78, 93, 43, 88, 76, 54, 98, 32, 65, 87, 71, 49, 82],
            },
        },
        "en": {
            1: {
                "n": 5,
                "sequence": [10, 25, 15, 8, 12],
            },
            2: {
                "n": 8,
                "sequence": [34, 67, 23, 89, 45, 12, 56, 78],
            },
            3: {
                "n": 12,
                "sequence": [45, 67, 89, 34, 23, 91, 56, 78, 12, 43, 88, 76],
            },
            4: {
                "n": 16,
                "sequence": [45, 67, 23, 89, 34, 91, 56, 78, 93, 43, 88, 76, 54, 32, 65, 87],
            },
            5: {
                "n": 20,
                "sequence": [45, 67, 23, 89, 34, 91, 56, 78, 93, 43, 88, 76, 54, 98, 32, 65, 87, 71, 49, 82],
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        
        self.sequence = cfg["sequence"]
        self.n = cfg["n"]
        
        max_val = max(self.sequence)
        self.max_position = self.sequence.index(max_val) + 1

    def evaluate(self, parsed_info):
        try:
            answer = parsed_info["answer"].strip()
            predicted_pos = int(answer)
            
            if predicted_pos < 1 or predicted_pos > self.n:
                return False
            
            return predicted_pos == self.max_position
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if "query_max" in parsed_info:
            return self._handle_max_query(parsed_info["query_max"])
        elif "query_cmp" in parsed_info:
            return self._handle_cmp_query(parsed_info["query_cmp"])
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        import re

        m = re.search(r'=\s*(\d+)', correct)
        if m:
            val = int(m.group(1))
            wrong_val = val + 1
            return correct[:m.start(1)] + str(wrong_val) + correct[m.end(1):]

        m = re.search(r'最大值为\s*(\d+)', correct)
        if m:
            val = int(m.group(1))
            wrong_val = val + 1
            return correct[:m.start(1)] + str(wrong_val) + correct[m.end(1):]

        if "LEFT" in correct:
            return correct.replace("LEFT", "RIGHT")
        if "RIGHT" in correct:
            return correct.replace("RIGHT", "LEFT")

        return correct + "_WRONG"

    def _handle_max_query(self, query_str):
        try:
            parts = [x.strip() for x in query_str.split(",")]
            if len(parts) != 2:
                return "INVALID"
            
            L, R = int(parts[0]), int(parts[1])
            
            if L < 1 or R > self.n or L > R:
                return "INVALID"
            
            max_val = max(self.sequence[L-1:R])
            
            if self.config.language == "zh":
                return f"区间 [{L}, {R}] 的最大值为 {max_val}"
            else:
                return f"MAX [{L}, {R}] = {max_val}"
                
        except:
            return "INVALID"

    def _handle_cmp_query(self, query_str):
        try:
            parts = [x.strip() for x in query_str.split(",")]
            if len(parts) != 4:
                return "INVALID"
            
            L1, R1, L2, R2 = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])
            
            if L1 < 1 or R2 > self.n or L1 > R1 or L2 > R2 or R1 >= L2:
                return "INVALID"
            
            max_left = max(self.sequence[L1-1:R1])
            max_right = max(self.sequence[L2-1:R2])
            
            if max_left > max_right:
                result = "LEFT"
            else:
                result = "RIGHT"
            
            if self.config.language == "zh":
                return f"区间 [{L1}, {R1}] 与 [{L2}, {R2}] 比较结果: {result}"
            else:
                return f"CMP [{L1}, {R1}] vs [{L2}, {R2}]: {result}"
                
        except:
            return "INVALID"

    def get_all_possible_queries(self) -> list:
        queries = []

        for L in range(1, self.n + 1):
            for R in range(L, self.n + 1):
                answer = self._handle_max_query(f"{L},{R}")
                queries.append({
                    "query":  f"<query_max>{L},{R}</query_max>",
                    "answer": answer,
                })

        for L1 in range(1, self.n):
            for R1 in range(L1, self.n):
                for L2 in range(R1 + 1, self.n + 1):
                    for R2 in range(L2, self.n + 1):
                        answer = self._handle_cmp_query(f"{L1},{R1},{L2},{R2}")
                        queries.append({
                            "query":  f"<query_cmp>{L1},{R1},{L2},{R2}</query_cmp>",
                            "answer": answer,
                        })

        return queries