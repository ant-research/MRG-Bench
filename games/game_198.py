from .base import Game
import re

class PeriodicSequenceGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "序列"

    game_rule_zh = """\
我们现在来玩一个"周期序列推断"游戏，规则如下：

游戏设定了一个长度为 {n} 的序列 S，索引从 1 到 {n}。序列中的每个元素都来自一个大小为 4 的字母表（例如 A、B、C、D）。这个序列具有周期性结构：存在一个最小周期 p（p 不超过 {max_period}），使得序列按照这个周期重复。

你的目标是推断出序列中第 {target_pos} 个位置的元素是什么。

你可以通过以下两种方式向我查询信息（每次仅限一个查询），我会根据真实设定如实回答：

1. 取值查询（最多 {value_queries} 次）：询问某个位置 i 的元素值（但不能直接询问位置 {target_pos}）。我会回答该位置的具体字母。
2. 相等性查询（最多 {equality_queries} 次）：询问位置 i 和位置 j 的元素是否相同。我会回答"是"或"否"。

当你收集到足够信息后，请提交你对位置 {target_pos} 的答案。若答案错误、格式不符或超出查询预算，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 取值查询（例如询问位置 5）：
<query_value>5</query_value>

- 相等性查询（例如询问位置 3 和位置 7 是否相同）：
<query_equal>3,7</query_equal>

提交最终答案时，格式如下（例如你认为答案是 B）：
<answer>B</answer>
"""

    game_rule_en = """\
Let's play a "Periodic Sequence Inference" game. Here are the rules:

There is a sequence S of length {n}, indexed from 1 to {n}. Each element in the sequence comes from an alphabet of size 4 (e.g., A, B, C, D). This sequence has a periodic structure: there exists a minimal period p (where p does not exceed {max_period}), such that the sequence repeats according to this period.

Your goal is to infer the element at position {target_pos} in the sequence.

You can query information in two ways (one query per turn), and I will answer truthfully based on the actual setup:

1. Value Query (at most {value_queries} times): Ask for the element value at position i (but you cannot directly ask about position {target_pos}). I will respond with the specific letter at that position.
2. Equality Query (at most {equality_queries} times): Ask whether the elements at positions i and j are the same. I will answer "Yes" or "No".

When you have gathered enough information, submit your answer for position {target_pos}. If the answer is wrong, the format is invalid, or you exceed the query budget, the game fails.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking about position 5):
<query_value>5</query_value>

- Equality Query (e.g., asking if positions 3 and 7 are the same):
<query_equal>3,7</query_equal>

When submitting the final answer, use this format (e.g., if you think the answer is B):
<answer>B</answer>
"""

    contextualized_rule_zh_1 = """\
智能交通信号调度中心遇到了一个棘手的问题，规则如下：

调度系统为一个关键路口设定了一个长度为 {n} 的放行时间片序列 S，时间片索引从 1 到 {n}。每个时间片内的主要放行方向均来自 4 个预设相位（例如 北向A、南向B、东向C、西向D）。系统配置了一个周期性调度结构：存在一个最小周期 p（p 不超过 {max_period}），使得放行序列严格按照这个周期循环。

你的目标是推断出在第 {target_pos} 个时间片时，系统设定的放行方向是什么。

你可以通过以下两种方式向信号机系统查询信息（每次仅限一个查询），系统将如实返回结果：

1. 取值查询（最多 {value_queries} 次）：询问某一个特定时间片 i 的放行方向（但禁止直接查询目标时间片 {target_pos}）。系统会返回该时间片对应的具体方向代码。
2. 相等性查询（最多 {equality_queries} 次）：询问时间片 i 和时间片 j 的放行方向是否相同。系统会返回"是"或"否"。

当你收集到足够信息后，请提交你对第 {target_pos} 个时间片放行方向的最终推断。若答案错误、格式不符或超出查询预算，任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 取值查询（例如询问第 5 个时间片）：
<query_value>5</query_value>

- 相等性查询（例如询问第 3 和第 7 个时间片是否相同）：
<query_equal>3,7</query_equal>

提交最终答案时，格式如下（例如你认为放行方向是 B）：
<answer>B</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The Intelligent Traffic Signal Control Center is facing a challenging issue. Here are the rules:

The scheduling system has configured a sequence S of release time slots of length {n} for a critical intersection, indexed from 1 to {n}. The primary release direction for each time slot is chosen from 4 preset phases (e.g., Northbound A, Southbound B, Eastbound C, Westbound D). The system follows a periodic scheduling structure: there is a minimal period p (where p does not exceed {max_period}), and the release sequence repeats strictly according to this period.

Your goal is to infer the scheduled release direction for the {target_pos}th time slot.

You can query the signal system in two ways (one query per turn), and the system will return factual results:

1. Value Query (at most {value_queries} times): Ask for the release direction at a specific time slot i (but you cannot directly ask about the target time slot {target_pos}). The system will return the specific direction code for that slot.
2. Equality Query (at most {equality_queries} times): Ask whether the release directions at time slots i and j are the same. The system will answer "Yes" or "No".

Once you have gathered enough information, submit your final inference for the release direction at the {target_pos}th time slot. If the answer is incorrect, the format is invalid, or the query budget is exceeded, the task fails.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking about the 5th time slot):
<query_value>5</query_value>

- Equality Query (e.g., asking if the 3rd and 7th time slots are the same):
<query_equal>3,7</query_equal>

When submitting the final answer, use this format (e.g., if you think the direction is B):
<answer>B</answer>
"""

    contextualized_rule_zh_2 = """\
您正在负责制定一项智能康复理疗方案，规则如下：

医疗系统为一名患者生成了一个长度为 {n} 天的理疗日程序列 S，天数索引从 1 到 {n}。每天的理疗项目选自 4 种特定的康复疗法（例如 针灸A、推拿B、热敷C、电疗D）。此疗程具有严格的周期性结构：存在一个基础疗程周期 p（p 不超过 {max_period}），患者的日程会按照这个最小周期不断循环。

你的目标是推断出在第 {target_pos} 天，系统为患者安排的理疗项目是什么。

你可以通过以下两种方式向医疗数据库查询信息（每次仅限一个查询），数据库会如实返回记录：

1. 取值查询（最多 {value_queries} 次）：询问某一天 i 的具体理疗项目（但不能直接询问第 {target_pos} 天）。系统会返回该天安排的项目代码。
2. 相等性查询（最多 {equality_queries} 次）：询问第 i 天和第 j 天的理疗项目是否相同。系统会返回"是"或"否"。

当你收集到足够信息后，请提交你对第 {target_pos} 天理疗项目的诊断答案。若答案错误、格式不符或超出查询预算，方案评估失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 取值查询（例如询问第 5 天的安排）：
<query_value>5</query_value>

- 相等性查询（例如询问第 3 天和第 7 天的安排是否相同）：
<query_equal>3,7</query_equal>

提交最终答案时，格式如下（例如你认为项目是 B）：
<answer>B</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
You are in charge of designing an intelligent rehabilitation therapy plan. Here are the rules:

The medical system has generated a therapy schedule sequence S of length {n} days for a patient, indexed from 1 to {n}. The daily therapy session is selected from 4 specific rehabilitation treatments (e.g., Acupuncture A, Massage B, Hot Compress C, Electrotherapy D). This regimen has a strict periodic structure: there exists a base treatment period p (where p does not exceed {max_period}), and the patient's schedule repeats according to this minimal period.

Your goal is to infer the assigned therapy treatment on the {target_pos}th day.

You can query the medical database in two ways (one query per turn), and the database will return factual records:

1. Value Query (at most {value_queries} times): Ask for the specific treatment on day i (but you cannot directly ask about the {target_pos}th day). The system will return the treatment code for that day.
2. Equality Query (at most {equality_queries} times): Ask whether the treatments on day i and day j are the same. The system will answer "Yes" or "No".

When you have gathered enough information, submit your diagnostic answer for the {target_pos}th day. If the answer is incorrect, the format is invalid, or you exceed the query budget, the plan evaluation fails.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking about the 5th day):
<query_value>5</query_value>

- Equality Query (e.g., asking if the 3rd and 7th days are the same):
<query_equal>3,7</query_equal>

When submitting the final answer, use this format (e.g., if you think the treatment is B):
<answer>B</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用智能校园排课系统进行教务分析，规则如下：

教务处为某班级安排了一个包含 {n} 节课的课表序列 S，课时索引从 1 到 {n}。每节课的科目均来自 4 门核心课程（例如 语文A、数学B、英语C、科学D）。该课表遵循一种周期性排课规律：存在一个循环小节 p（p 不超过 {max_period}），课表科目会按照这个最小周期持续重复。

你的目标是推断出第 {target_pos} 节课安排的是哪门科目。

你可以通过以下两种方式向教务系统查询排课信息（每次仅限一个查询），系统将返回真实的课表设定：

1. 取值查询（最多 {value_queries} 次）：询问某节课 i 的具体科目（但不能直接询问第 {target_pos} 节课）。系统会回答该节课的科目代码。
2. 相等性查询（最多 {equality_queries} 次）：询问第 i 节课和第 j 节课安排的科目是否相同。系统会回答"是"或"否"。

当你收集到足够信息后，请提交你对第 {target_pos} 节课的科目预测。若答案错误、格式不符或超出查询预算，排课分析失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 取值查询（例如询问第 5 节课）：
<query_value>5</query_value>

- 相等性查询（例如询问第 3 节课和第 7 节课是否相同）：
<query_equal>3,7</query_equal>

提交最终答案时，格式如下（例如你认为科目是 B）：
<answer>B</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Intelligent Campus Scheduling System for academic analysis. Here are the rules:

The academic affairs office has arranged a course schedule sequence S consisting of {n} classes for a certain grade, indexed from 1 to {n}. The subject for each class is drawn from 4 core courses (e.g., Literature A, Math B, English C, Science D). This schedule follows a periodic pattern: there is a recurring block of p classes (where p does not exceed {max_period}), and the subjects repeat based on this minimal period.

Your goal is to infer which subject is scheduled for the {target_pos}th class.

You can query the scheduling system in two ways (one query per turn), and the system will return the actual setup:

1. Value Query (at most {value_queries} times): Ask for the specific subject of class i (but you cannot directly ask about the {target_pos}th class). The system will return the subject code for that class.
2. Equality Query (at most {equality_queries} times): Ask whether the subjects scheduled for class i and class j are the same. The system will answer "Yes" or "No".

When you have collected enough information, submit your subject prediction for the {target_pos}th class. If the answer is incorrect, the format is invalid, or you exceed the query limit, the analysis fails.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking about the 5th class):
<query_value>5</query_value>

- Equality Query (e.g., asking if the 3rd and 7th classes are the same):
<query_equal>3,7</query_equal>

When submitting the final answer, use this format (e.g., if you think the subject is B):
<answer>B</answer>
"""

    contextualized_rule_zh_4 = """\
您正在监控一条自动化柔性生产线的工作状态，规则如下：

控制系统为流水线设定了一个包含 {n} 个生产批次的加工序列 S，批次索引从 1 到 {n}。每个批次的产品类型属于 4 种预设模具配置之一（例如 零件A、零件B、零件C、零件D）。该生产线采用周期性轮替模式运行：存在一个最小循环节 p（p 不超过 {max_period}），使得生产任务按照这个周期严格循环。

你的目标是推断出在第 {target_pos} 个批次时，生产线正在加工哪种类型的产品。

你可以通过以下两种方式向中控机床查询日志（每次仅限一个查询），系统会如实返回传感器读数：

1. 取值查询（最多 {value_queries} 次）：询问第 i 个批次的产品类型（但不能直接查询目标批次 {target_pos}）。中控系统会返回该批次的模具代码。
2. 相等性查询（最多 {equality_queries} 次）：询问第 i 个批次和第 j 个批次加工的产品类型是否相同。系统会返回"是"或"否"。

当你收集到足够信息后，请提交你对第 {target_pos} 个批次产品类型的判定。若答案错误、格式不符或超出查询预算，系统校验将失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 取值查询（例如询问第 5 个批次）：
<query_value>5</query_value>

- 相等性查询（例如询问第 3 个批次和第 7 个批次是否相同）：
<query_equal>3,7</query_equal>

提交最终答案时，格式如下（例如你认为产品类型是 B）：
<answer>B</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
You are monitoring the operational status of an automated flexible production line. Here are the rules:

The control system has configured a processing sequence S consisting of {n} production batches for the assembly line, indexed from 1 to {n}. The product type for each batch belongs to one of 4 preset mold configurations (e.g., Part A, Part B, Part C, Part D). The production line operates on a periodic rotation mode: there is a minimal repeating cycle p (where p does not exceed {max_period}), and the production tasks loop strictly according to this period.

Your goal is to infer which product type is being processed during the {target_pos}th batch.

You can query the central control logs in two ways (one query per turn), and the system will faithfully return sensor readings:

1. Value Query (at most {value_queries} times): Ask for the product type of the ith batch (but you cannot directly query the target batch {target_pos}). The central system will return the mold code for that batch.
2. Equality Query (at most {equality_queries} times): Ask whether the product types processed in the ith and jth batches are the same. The system will answer "Yes" or "No".

Once you have gathered sufficient information, submit your determination for the product type of the {target_pos}th batch. If the answer is incorrect, the format is invalid, or the query budget is exceeded, the system validation will fail.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking about the 5th batch):
<query_value>5</query_value>

- Equality Query (e.g., asking if the 3rd and 7th batches are the same):
<query_equal>3,7</query_equal>

When submitting the final answer, use this format (e.g., if you think the product type is B):
<answer>B</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用法院案件智能排期核查系统，规则如下：

排期系统为某法庭生成了一个涵盖 {n} 个工作日的案件审理序列 S，工作日索引从 1 到 {n}。每日排期的案由类型固定在 4 个司法分类之内（例如 民事A、刑事B、行政C、商事D）。为了平衡法官工作量，该排期具有规律的循环特性：存在一个最小周期 p（p 不超过 {max_period}），案件类型依此周期不断重复。

你的目标是推断出在第 {target_pos} 个工作日，法庭排期的案件属于哪个司法分类。

你可以通过以下两种方式向司法系统调取卷宗信息（每次仅限一个查询），系统将反馈真实的排期记录：

1. 取值查询（最多 {value_queries} 次）：询问第 i 个工作日的案件类型（但禁止直接查询第 {target_pos} 个工作日）。系统会返回当天的案件分类代码。
2. 相等性查询（最多 {equality_queries} 次）：询问第 i 个工作日和第 j 个工作日的案件类型是否相同。系统会返回"是"或"否"。

当你收集到足够信息后，请提交你对第 {target_pos} 个工作日案件类型的审查结论。若答案错误、格式不符或超出查询预算，卷宗核查失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 取值查询（例如询问第 5 个工作日）：
<query_value>5</query_value>

- 相等性查询（例如询问第 3 和第 7 个工作日的案件类型是否相同）：
<query_equal>3,7</query_equal>

提交最终答案时，格式如下（例如你认为案件类型是 B）：
<answer>B</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the Court Case Intelligent Scheduling Verification System. Here are the rules:

The scheduling system has generated a trial sequence S covering {n} working days for a specific courtroom, indexed from 1 to {n}. The cause of action type scheduled for each day is fixed among 4 judicial classifications (e.g., Civil A, Criminal B, Administrative C, Commercial D). To balance the workload of judges, the schedule features a regular looping pattern: there is a minimal period p (where p does not exceed {max_period}), and the case types repeat steadily based on this cycle.

Your goal is to infer which judicial classification is scheduled for the {target_pos}th working day.

You can query the judicial system for docket information in two ways (one query per turn), and the system will provide the actual scheduling records:

1. Value Query (at most {value_queries} times): Ask for the case type on the ith working day (but you are prohibited from directly querying the {target_pos}th day). The system will return the case classification code for that day.
2. Equality Query (at most {equality_queries} times): Ask whether the case types scheduled for the ith and jth working days are the same. The system will answer "Yes" or "No".

When you have obtained sufficient information, submit your review conclusion for the case type on the {target_pos}th working day. If the answer is incorrect, the format is invalid, or the query limit is exceeded, the docket verification fails.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking about the 5th working day):
<query_value>5</query_value>

- Equality Query (e.g., asking if the 3rd and 7th working days are the same):
<query_equal>3,7</query_equal>

When submitting the final answer, use this format (e.g., if you think the case type is B):
<answer>B</answer>
"""

    tags = ["answer", "query_value", "query_equal"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 8,
                "max_period": 4,
                "period": 2,
                "base_pattern": "A,B",
                "target_pos": 3,
                "value_queries": 4,
                "equality_queries": 3,
            },
            2: {
                "n": 12,
                "max_period": 6,
                "period": 3,
                "base_pattern": "C,A,B",
                "target_pos": 7,
                "value_queries": 5,
                "equality_queries": 4,
            },
            3: {
                "n": 16,
                "max_period": 8,
                "period": 4,
                "base_pattern": "D,A,C,B",
                "target_pos": 11,
                "value_queries": 6,
                "equality_queries": 5,
            },
            4: {
                "n": 20,
                "max_period": 10,
                "period": 5,
                "base_pattern": "B,D,A,C,B",
                "target_pos": 13,
                "value_queries": 7,
                "equality_queries": 5,
            },
            5: {
                "n": 24,
                "max_period": 8,
                "period": 8,
                "base_pattern": "A,C,B,D,A,D,C,B",
                "target_pos": 22,
                "value_queries": 8,
                "equality_queries": 6,
            },
        },
        "en": {
            1: {
                "n": 8,
                "max_period": 4,
                "period": 2,
                "base_pattern": "A,B",
                "target_pos": 3,
                "value_queries": 4,
                "equality_queries": 3,
            },
            2: {
                "n": 12,
                "max_period": 6,
                "period": 3,
                "base_pattern": "C,A,B",
                "target_pos": 7,
                "value_queries": 5,
                "equality_queries": 4,
            },
            3: {
                "n": 16,
                "max_period": 8,
                "period": 4,
                "base_pattern": "D,A,C,B",
                "target_pos": 11,
                "value_queries": 6,
                "equality_queries": 5,
            },
            4: {
                "n": 20,
                "max_period": 10,
                "period": 5,
                "base_pattern": "B,D,A,C,B",
                "target_pos": 13,
                "value_queries": 7,
                "equality_queries": 5,
            },
            5: {
                "n": 24,
                "max_period": 8,
                "period": 8,
                "base_pattern": "A,C,B,D,A,D,C,B",
                "target_pos": 22,
                "value_queries": 8,
                "equality_queries": 6,
            },
        },
    }

    def __init__(self, config):
        self.value_query_count = 0
        self.equality_query_count = 0
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
        self._game_info["max_period"] = cfg["max_period"]
        self._game_info["target_pos"] = cfg["target_pos"]
        self._game_info["value_queries"] = cfg["value_queries"]
        self._game_info["equality_queries"] = cfg["equality_queries"]
        
        self.n = cfg["n"]
        self.period = cfg["period"]
        self.target_pos = cfg["target_pos"]
        self.max_value_queries = cfg["value_queries"]
        self.max_equality_queries = cfg["equality_queries"]
        
        base = cfg["base_pattern"].split(",")
        self.sequence = []
        for i in range(1, self.n + 1):
            self.sequence.append(base[(i - 1) % self.period])
        
        self.target_answer = self.sequence[self.target_pos - 1]

    def evaluate(self, parsed_info):
        submitted_answer = parsed_info["answer"].strip().upper()
        return submitted_answer == self.target_answer

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            err_budget_value = f"错误：已超出取值查询次数限制（最多 {self.max_value_queries} 次）。"
            err_budget_equal = f"错误：已超出相等性查询次数限制（最多 {self.max_equality_queries} 次）。"
            err_invalid_pos = "错误：位置编号无效或超出范围。"
            err_target_query = f"错误：不能直接查询目标位置 {self.target_pos}。"
            err_invalid_format = "错误：查询格式无效。"
        else:
            yes_res, no_res = "Yes", "No"
            err_budget_value = f"Error: Value query limit exceeded (max {self.max_value_queries} times)."
            err_budget_equal = f"Error: Equality query limit exceeded (max {self.max_equality_queries} times)."
            err_invalid_pos = "Error: Invalid or out-of-range position."
            err_target_query = f"Error: Cannot directly query the target position {self.target_pos}."
            err_invalid_format = "Error: Invalid query format."

        if "query_value" in parsed_info:
            if self.value_query_count >= self.max_value_queries:
                raise ValueError(err_budget_value)
            
            try:
                pos = int(parsed_info["query_value"].strip())
            except:
                raise ValueError(err_invalid_format)
            
            if pos < 1 or pos > self.n:
                raise ValueError(err_invalid_pos)
            
            if pos == self.target_pos:
                raise ValueError(err_target_query)
            
            self.value_query_count += 1
            return self.sequence[pos - 1]

        elif "query_equal" in parsed_info:
            if self.equality_query_count >= self.max_equality_queries:
                raise ValueError(err_budget_equal)
            
            try:
                raw = parsed_info["query_equal"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                pos1, pos2 = int(parts[0]), int(parts[1])
            except:
                raise ValueError(err_invalid_format)
            
            if pos1 < 1 or pos1 > self.n or pos2 < 1 or pos2 > self.n:
                raise ValueError(err_invalid_pos)
            
            self.equality_query_count += 1
            are_equal = (self.sequence[pos1 - 1] == self.sequence[pos2 - 1])
            return yes_res if are_equal else no_res

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        correct_str = str(correct).strip()
        
        if correct_str == "是":
            return "否"
        if correct_str == "否":
            return "是"
        
        lower_correct = correct_str.lower()
        if lower_correct == "yes":
            return "No" if correct_str[0].isupper() else "no"
        if lower_correct == "no":
            return "Yes" if correct_str[0].isupper() else "yes"
        
        alphabet = ["A", "B", "C", "D"]
        upper_correct = correct_str.upper()
        if upper_correct in alphabet:
            alternatives = [c for c in alphabet if c != upper_correct]
            return alternatives[0]
        
        if correct_str.lstrip('-').isdigit():
            return str(int(correct_str) + 1)
            
        return f"{correct_str}_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        possible_queries = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        for i in range(1, self.n + 1):
            if i == self.target_pos:
                continue
            
            ans = self.sequence[i - 1]
            
            possible_queries.append({
                "query": f"<query_value>{i}</query_value>",
                "answer": str(ans)
            })

        for i in range(1, self.n + 1):
            for j in range(i + 1, self.n + 1):
                is_equal = (self.sequence[i - 1] == self.sequence[j - 1])
                ans = yes_res if is_equal else no_res
                
                possible_queries.append({
                    "query": f"<query_equal>{i},{j}</query_equal>",
                    "answer": str(ans)
                })
        
        return possible_queries