import random
from .base import Game

class ThresholdLocationGame(Game):

    tags = ["query_threshold", "answer"]
    reasoning_type = "演绎推理"
    data_structure = "序列"

    game_rule_zh = """\
我们现在来玩一个"阈值定位"的推理游戏，规则如下：

游戏设定了一个已知的正整数 N = {n}（N 大于等于 3）。我已经秘密选定了一个整数 d，它位于区间 [0, N-1] 内（包含 0 和 N-1）。

你的目标是通过询问来确定 d 的精确值。你可以反复向我提出阈值查询：选择一个整数 t（t 必须在区间 [1, N-1] 内），询问"d 是否大于等于 t？"。我会如实回答"是"或"否"：
- 当 d 大于等于 t 时，回答"是"
- 当 d 小于 t 时，回答"否"

请注意：
1. 每次查询的 t 必须是 [1, N-1] 范围内的整数，否则视为不合法操作
2. 你必须至少完成 2 次合法查询后，才能提交最终答案
3. 最终答案 L 必须是 [0, N-1] 范围内的整数

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 阈值查询（例如询问 d 是否大于等于 5）：
<query_threshold>5</query_threshold>

提交最终答案时，直接给出你推断的 d 值（必须是 [0, N-1] 范围内的整数），格式如下：

<answer>3</answer>
"""

    game_rule_en = """\
Let's play a "Threshold Location" deduction game. Here are the rules:

The game has set a known positive integer N = {n} (N is greater than or equal to 3). I have secretly chosen an integer d in the interval [0, N-1] (inclusive).

Your goal is to determine the exact value of d through queries. You can repeatedly ask me threshold queries: choose an integer t (t must be in the interval [1, N-1]), and ask "Is d greater than or equal to t?". I will answer truthfully with "Yes" or "No":
- When d is greater than or equal to t, the answer is "Yes"
- When d is less than t, the answer is "No"

Please note:
1. Each query's t must be an integer in the range [1, N-1], otherwise it is considered an invalid operation
2. You must complete at least 2 valid queries before submitting your final answer
3. The final answer L must be an integer in the range [0, N-1]

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Threshold Query (e.g., asking if d is greater than or equal to 5):
<query_threshold>5</query_threshold>

When submitting the final answer, directly provide your inferred value of d (must be an integer in [0, N-1]), using this format:

<answer>3</answer>
"""

    contextualized_rule_zh_1 = """\
【交通网络监控场景】
我们现在进行一项"路网拥堵指数"排查任务，规则如下：

系统设定了该路段的最高可能拥堵指数等级为 N-1，已知当前 N = {n}（N 大于等于 3）。监控中心已隐秘记录了当前时刻的真实拥堵等级 d，它位于区间 [0, N-1] 内（包含 0 和 N-1）。

你的目标是通过调取阈值监测数据来确定真实拥堵等级 d 的精确值。你可以反复向我提交监测阈值查询：选择一个整数等级 t（t 必须在区间 [1, N-1] 内），询问"当前拥堵等级 d 是否大于等于阈值 t？"。我会根据传感器数据如实回答"是"或"否"：
- 当真实拥堵等级 d 大于等于 t 时，回答"是"
- 当真实拥堵等级 d 小于 t 时，回答"否"

请注意：
1. 每次查询设定的阈值 t 必须是 [1, N-1] 范围内的整数，否则视为无效指令
2. 你必须至少完成 2 次合法监测查询后，才能提交最终评估报告
3. 最终提交的拥堵等级 L 必须是 [0, N-1] 范围内的整数

当你收集到足够的数据后，请提交最终判定结果。若判定错误或格式不符，排查任务失败。

每次调取数据只能包含一个标签。请使用以下 XML 格式：

- 阈值监测查询（例如询问拥堵等级 d 是否大于等于 5）：
<query_threshold>5</query_threshold>

提交最终判定结果时，直接给出你推断的拥堵等级 d 的值（必须是 [0, N-1] 范围内的整数），格式如下：

<answer>3</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Network Monitoring Scenario]
Let's conduct a "Traffic Congestion Index" assessment task. Here are the protocols:

The system has established a maximum possible congestion index level of N-1 for this road section, with a known positive integer N = {n} (N is greater than or equal to 3). The monitoring center has secretly recorded the true congestion level d at the current moment, which falls within the interval [0, N-1] (inclusive).

Your objective is to pinpoint the exact value of the true congestion level d by retrieving threshold monitoring data. You can repeatedly submit monitoring threshold queries to me: select an integer level t (t must be in the interval [1, N-1]) and ask, "Is the current congestion level d greater than or equal to the threshold t?". I will answer truthfully based on sensor data with "Yes" or "No":
- When the true congestion level d is greater than or equal to t, the answer is "Yes"
- When the true congestion level d is less than t, the answer is "No"

Please note:
1. The threshold t for each query must be an integer in the range [1, N-1]; otherwise, it is considered an invalid command
2. You must complete at least 2 valid monitoring queries before submitting the final assessment report
3. The final submitted congestion level L must be an integer in the range [0, N-1]

When you have collected sufficient data, submit your final assessment. If the result is wrong or the format is invalid, the task fails.

Each data retrieval must contain only one tag. Use the following XML format:

- Threshold Monitoring Query (e.g., asking if congestion level d is greater than or equal to 5):
<query_threshold>5</query_threshold>

When submitting the final assessment, directly provide your inferred value of the congestion level d (must be an integer in [0, N-1]), using this format:

<answer>3</answer>
"""

    contextualized_rule_zh_2 = """\
【临床血液样本分析场景】
我们现在进行一项"病毒载量评级"化验任务，规则如下：

系统设定了该项化验的最高可能病毒载量评级为 N-1，已知当前 N = {n}（N 大于等于 3）。检验科已隐秘得出了样本的真实病毒载量评级 d，它位于区间 [0, N-1] 内（包含 0 和 N-1）。

你的目标是通过调取生化试剂检测结果来确定真实病毒载量评级 d 的精确值。你可以反复向我提交检测阈值查询：选择一个整数评级 t（t 必须在区间 [1, N-1] 内），询问"样本的病毒载量评级 d 是否大于等于检测阈值 t？"。我会根据化验数据如实回答"是"或"否"：
- 当真实病毒载量评级 d 大于等于 t 时，回答"是"
- 当真实病毒载量评级 d 小于 t 时，回答"否"

请注意：
1. 每次查询设定的阈值 t 必须是 [1, N-1] 范围内的整数，否则视为无效指令
2. 你必须至少完成 2 次合法检测查询后，才能提交最终化验报告
3. 最终提交的病毒载量评级 L 必须是 [0, N-1] 范围内的整数

当你收集到足够的数据后，请提交最终判定结果。若判定错误或格式不符，化验任务失败。

每次调取数据只能包含一个标签。请使用以下 XML 格式：

- 阈值检测查询（例如询问病毒载量评级 d 是否大于等于 5）：
<query_threshold>5</query_threshold>

提交最终判定结果时，直接给出你推断的病毒载量评级 d 的值（必须是 [0, N-1] 范围内的整数），格式如下：

<answer>3</answer>
"""

    contextualized_rule_en_2 = """\
[Clinical Blood Sample Analysis Scenario]
Let's conduct a "Viral Load Grading" testing task. Here are the protocols:

The system has established a maximum possible viral load grade of N-1 for this test, with a known positive integer N = {n} (N is greater than or equal to 3). The laboratory has secretly determined the sample's true viral load grade d, which falls within the interval [0, N-1] (inclusive).

Your objective is to pinpoint the exact value of the true viral load grade d by retrieving biochemical reagent test results. You can repeatedly submit detection threshold queries to me: select an integer grade t (t must be in the interval [1, N-1]) and ask, "Is the sample's viral load grade d greater than or equal to the detection threshold t?". I will answer truthfully based on laboratory data with "Yes" or "No":
- When the true viral load grade d is greater than or equal to t, the answer is "Yes"
- When the true viral load grade d is less than t, the answer is "No"

Please note:
1. The threshold t for each query must be an integer in the range [1, N-1]; otherwise, it is considered an invalid command
2. You must complete at least 2 valid detection queries before submitting the final laboratory report
3. The final submitted viral load grade L must be an integer in the range [0, N-1]

When you have collected sufficient data, submit your final assessment. If the result is wrong or the format is invalid, the testing task fails.

Each data retrieval must contain only one tag. Use the following XML format:

- Threshold Detection Query (e.g., asking if viral load grade d is greater than or equal to 5):
<query_threshold>5</query_threshold>

When submitting the final assessment, directly provide your inferred value of the viral load grade d (must be an integer in [0, N-1]), using this format:

<answer>3</answer>
"""

    contextualized_rule_zh_3 = """\
【学生核心素养评估场景】
我们现在进行一项"学科能力等级"评定任务，规则如下：

教育系统设定了该学科的最高可能能力等级为 N-1，已知当前 N = {n}（N 大于等于 3）。测评中心已隐秘评估了该生的真实能力等级 d，它位于区间 [0, N-1] 内（包含 0 和 N-1）。

你的目标是通过调取标准化测试结果来确定真实能力等级 d 的精确值。你可以反复向我提交测试阈值查询：选择一个整数等级 t（t 必须在区间 [1, N-1] 内），询问"该生能力等级 d 是否大于等于测试难度 t？"。我会根据测试数据如实回答"是"或"否"：
- 当真实能力等级 d 大于等于 t 时，回答"是"
- 当真实能力等级 d 小于 t 时，回答"否"

请注意：
1. 每次查询设定的测试难度 t 必须是 [1, N-1] 范围内的整数，否则视为无效指令
2. 你必须至少完成 2 次合法测试查询后，才能提交最终评定报告
3. 最终提交的能力等级 L 必须是 [0, N-1] 范围内的整数

当你收集到足够的数据后，请提交最终评定结果。若评定错误或格式不符，评估任务失败。

每次调取数据只能包含一个标签。请使用以下 XML 格式：

- 阈值测试查询（例如询问能力等级 d 是否大于等于 5）：
<query_threshold>5</query_threshold>

提交最终评定结果时，直接给出你推断的能力等级 d 的值（必须是 [0, N-1] 范围内的整数），格式如下：

<answer>3</answer>
"""

    contextualized_rule_en_3 = """\
[Student Core Competency Assessment Scenario]
Let's conduct a "Subject Proficiency Level" assessment task. Here are the protocols:

The education system has established a maximum possible proficiency level of N-1 for this subject, with a known positive integer N = {n} (N is greater than or equal to 3). The assessment center has secretly evaluated the student's true proficiency level d, which falls within the interval [0, N-1] (inclusive).

Your objective is to pinpoint the exact value of the true proficiency level d by retrieving standardized test results. You can repeatedly submit test threshold queries to me: select an integer level t (t must be in the interval [1, N-1]) and ask, "Is the student's proficiency level d greater than or equal to the test difficulty t?". I will answer truthfully based on test data with "Yes" or "No":
- When the true proficiency level d is greater than or equal to t, the answer is "Yes"
- When the true proficiency level d is less than t, the answer is "No"

Please note:
1. The test difficulty t for each query must be an integer in the range [1, N-1]; otherwise, it is considered an invalid command
2. You must complete at least 2 valid test queries before submitting the final assessment report
3. The final submitted proficiency level L must be an integer in the range [0, N-1]

When you have collected sufficient data, submit your final assessment. If the result is wrong or the format is invalid, the assessment task fails.

Each data retrieval must contain only one tag. Use the following XML format:

- Threshold Test Query (e.g., asking if proficiency level d is greater than or equal to 5):
<query_threshold>5</query_threshold>

When submitting the final assessment, directly provide your inferred value of the proficiency level d (must be an integer in [0, N-1]), using this format:

<answer>3</answer>
"""

    contextualized_rule_zh_4 = """\
【精密零件质量检测场景】
我们现在进行一项"材料疲劳极限"无损检测任务，规则如下：

工业标准设定了该批次零件的最高可能疲劳极限等级为 N-1，已知当前 N = {n}（N 大于等于 3）。质检设备已隐秘测定了目标零件的真实疲劳极限等级 d，它位于区间 [0, N-1] 内（包含 0 和 N-1）。

你的目标是通过调取超声波探伤数据来确定真实疲劳极限等级 d 的精确值。你可以反复向我提交探测阈值查询：选择一个整数等级 t（t 必须在区间 [1, N-1] 内），询问"零件的疲劳极限等级 d 是否大于等于探测阈值 t？"。我会根据传感器反馈如实回答"是"或"否"：
- 当真实疲劳极限等级 d 大于等于 t 时，回答"是"
- 当真实疲劳极限等级 d 小于 t 时，回答"否"

请注意：
1. 每次查询设定的探测阈值 t 必须是 [1, N-1] 范围内的整数，否则视为无效指令
2. 你必须至少完成 2 次合法探测查询后，才能提交最终质检报告
3. 最终提交的疲劳极限等级 L 必须是 [0, N-1] 范围内的整数

当你收集到足够的数据后，请提交最终判定结果。若判定错误或格式不符，检测任务失败。

每次调取数据只能包含一个标签。请使用以下 XML 格式：

- 阈值探测查询（例如询问疲劳极限等级 d 是否大于等于 5）：
<query_threshold>5</query_threshold>

提交最终判定结果时，直接给出你推断的疲劳极限等级 d 的值（必须是 [0, N-1] 范围内的整数），格式如下：

<answer>3</answer>
"""

    contextualized_rule_en_4 = """\
[Precision Parts Quality Inspection Scenario]
Let's conduct a "Material Fatigue Limit" non-destructive testing task. Here are the protocols:

Industrial standards have established a maximum possible fatigue limit grade of N-1 for this batch of parts, with a known positive integer N = {n} (N is greater than or equal to 3). The quality inspection equipment has secretly determined the target part's true fatigue limit grade d, which falls within the interval [0, N-1] (inclusive).

Your objective is to pinpoint the exact value of the true fatigue limit grade d by retrieving ultrasonic flaw detection data. You can repeatedly submit detection threshold queries to me: select an integer grade t (t must be in the interval [1, N-1]) and ask, "Is the part's fatigue limit grade d greater than or equal to the detection threshold t?". I will answer truthfully based on sensor feedback with "Yes" or "No":
- When the true fatigue limit grade d is greater than or equal to t, the answer is "Yes"
- When the true fatigue limit grade d is less than t, the answer is "No"

Please note:
1. The detection threshold t for each query must be an integer in the range [1, N-1]; otherwise, it is considered an invalid command
2. You must complete at least 2 valid detection queries before submitting the final quality inspection report
3. The final submitted fatigue limit grade L must be an integer in the range [0, N-1]

When you have collected sufficient data, submit your final assessment. If the result is wrong or the format is invalid, the testing task fails.

Each data retrieval must contain only one tag. Use the following XML format:

- Threshold Detection Query (e.g., asking if fatigue limit grade d is greater than or equal to 5):
<query_threshold>5</query_threshold>

When submitting the final assessment, directly provide your inferred value of the fatigue limit grade d (must be an integer in [0, N-1]), using this format:

<answer>3</answer>
"""

    contextualized_rule_zh_5 = """\
【司法量刑辅助决策场景】
我们现在进行一项"犯罪社会危害性"定级评估任务，规则如下：

量刑指南设定了该类犯罪的最高可能危害性等级为 N-1，已知当前 N = {n}（N 大于等于 3）。法院案管系统已隐秘核定了本案的真实危害性等级 d，它位于区间 [0, N-1] 内（包含 0 和 N-1）。

你的目标是通过调取类案检索结果来确定真实危害性等级 d 的精确值。你可以反复向我提交参考阈值查询：选择一个整数等级 t（t 必须在区间 [1, N-1] 内），询问"本案的危害性等级 d 是否大于等于参考阈值 t？"。我会根据司法大数据如实回答"是"或"否"：
- 当真实危害性等级 d 大于等于 t 时，回答"是"
- 当真实危害性等级 d 小于 t 时，回答"否"

请注意：
1. 每次查询设定的参考阈值 t 必须是 [1, N-1] 范围内的整数，否则视为无效指令
2. 你必须至少完成 2 次合法检索查询后，才能提交最终评估报告
3. 最终提交的危害性等级 L 必须是 [0, N-1] 范围内的整数

当你收集到足够的数据后，请提交最终定级结果。若定级错误或格式不符，评估任务失败。

每次调取数据只能包含一个标签。请使用以下 XML 格式：

- 阈值参考查询（例如询问危害性等级 d 是否大于等于 5）：
<query_threshold>5</query_threshold>

提交最终定级结果时，直接给出你推断的危害性等级 d 的值（必须是 [0, N-1] 范围内的整数），格式如下：

<answer>3</answer>
"""

    contextualized_rule_en_5 = """\
[Judicial Sentencing Auxiliary Decision Scenario]
Let's conduct a "Crime Social Harmfulness" grading assessment task. Here are the protocols:

The sentencing guidelines have established a maximum possible harmfulness grade of N-1 for this type of crime, with a known positive integer N = {n} (N is greater than or equal to 3). The court case management system has secretly verified the true harmfulness grade d of this case, which falls within the interval [0, N-1] (inclusive).

Your objective is to pinpoint the exact value of the true harmfulness grade d by retrieving similar case search results. You can repeatedly submit reference threshold queries to me: select an integer grade t (t must be in the interval [1, N-1]) and ask, "Is the harmfulness grade d of this case greater than or equal to the reference threshold t?". I will answer truthfully based on judicial big data with "Yes" or "No":
- When the true harmfulness grade d is greater than or equal to t, the answer is "Yes"
- When the true harmfulness grade d is less than t, the answer is "No"

Please note:
1. The reference threshold t for each query must be an integer in the range [1, N-1]; otherwise, it is considered an invalid command
2. You must complete at least 2 valid search queries before submitting the final assessment report
3. The final submitted harmfulness grade L must be an integer in the range [0, N-1]

When you have collected sufficient data, submit your final grading. If the result is wrong or the format is invalid, the assessment task fails.

Each data retrieval must contain only one tag. Use the following XML format:

- Threshold Reference Query (e.g., asking if harmfulness grade d is greater than or equal to 5):
<query_threshold>5</query_threshold>

When submitting the final grading, directly provide your inferred value of the harmfulness grade d (must be an integer in [0, N-1]), using this format:

<answer>3</answer>
"""

    def _initialize_game(self):
        difficulty = int(self.config.difficulty)
        difficulty_map = {
            1: (5, 10),
            2: (10, 20),
            3: (20, 50),
            4: (50, 100),
            5: (100, 200),
        }
        lo, hi = difficulty_map.get(difficulty, (5, 20))
        
        seed = getattr(self.config, 'seed', 42) 
        rng = random.Random(seed + difficulty)
        self.N = rng.randint(lo, hi)
        self.d = rng.randint(0, self.N - 1)
        self._game_info = {"n": self.N}
        self.query_count = 0

    def evaluate(self, parsed_info):
        if self.query_count < 2:
            raise ValueError(
                "提交答案前必须至少完成 2 次合法查询。" 
                if self.config.language == "zh" 
                else "You must complete at least 2 valid queries before submitting your answer."
            )
            
        try:
            ans = int(parsed_info["answer"])
            return ans == self.d
        except (ValueError, KeyError):
            return False

    def _cf_core_produce(self, parsed_info):
        if "query_threshold" in parsed_info:
            try:
                t = int(parsed_info["query_threshold"])
                if not (1 <= t <= self.N - 1):
                    return (f"无效指令：阈值 t 必须是 [1, {self.N - 1}] 范围内的整数。当前输入为 {t}。" 
                            if self.config.language == "zh" 
                            else f"Invalid command: threshold t must be an integer in [1, {self.N - 1}]. Your input was {t}.")
            except ValueError:
                return ("无效指令：阈值 t 必须是整数。" 
                        if self.config.language == "zh" 
                        else "Invalid command: threshold t must be an integer.")
            
            self.query_count += 1
            if self.d >= t:
                return "是" if self.config.language == "zh" else "Yes"
            else:
                return "否" if self.config.language == "zh" else "No"
                
        return "解析错误" if self.config.language == "zh" else "Parse error"

    def get_all_possible_queries(self):
        queries = []
        for t in range(1, self.N):
            query_str = f"<query_threshold>{t}</query_threshold>"
            if self.d >= t:
                answer_str = "Yes" if self.config.language == "en" else "是"
            else:
                answer_str = "No" if self.config.language == "en" else "否"
            queries.append({"query": query_str, "answer": answer_str})
        return queries

    def _cf_make_wrong(self, correct):
        if correct in ["是", "Yes"]:
            return "否" if self.config.language == "zh" else "No"
        else:
            return "是" if self.config.language == "zh" else "Yes"