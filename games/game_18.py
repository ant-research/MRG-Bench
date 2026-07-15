from .base import Game
import random
import re

class KthElementFindingGame(Game):

    game_rule_zh = """\
我们来玩一个"寻找第 k 位元素"的推理游戏，规则如下：

游戏设定了一个标签集合 {{1, 2, ..., {n}}}，这些标签存在一个未知但固定的严格全序关系。你的目标是找出按照这个全序关系从小到大排列后，位于第 {k} 位的标签是哪一个。

你可以反复向我提出比较查询，每次查询两个不同的标签 i 和 j，我会告诉你在这个全序关系中谁排在前面。请尽可能用较少的查询次数找到答案。

每次只能包含一个标签。请使用以下 XML 格式：

- 比较查询（例如比较标签 3 和 5）：
<query_compare>3,5</query_compare>

- 提交最终答案（例如认为第 {k} 位是标签 7）：
<answer>7</answer>

注意事项：
1. 比较查询中的两个标签必须不同，且都在 1 到 {n} 范围内
2. 你可以进行任意多次比较查询，但应尽量减少查询次数
3. 当你确定答案后，使用 answer 标签提交
4. 如果答案错误，游戏失败
"""

    game_rule_en = """\
Let's play a "Find the k-th Element" deduction game. Here are the rules:

There is a set of labels {{1, 2, ..., {n}}}. These labels have an unknown but fixed strict total order. Your goal is to identify which label is at position {k} when all labels are sorted according to this total order (in ascending order).

You can repeatedly ask me comparison queries. Each query compares two different labels i and j, and I will tell you which one comes first in the total order. Try to find the answer with as few queries as possible.

Each query must contain only one tag. Use the following XML format:

- Comparison Query (e.g., comparing labels 3 and 5):
<query_compare>3,5</query_compare>

- Submit Final Answer (e.g., if you think position {k} is label 7):
<answer>7</answer>

Notes:
1. The two labels in a comparison query must be different and within range 1 to {n}
2. You can make any number of comparison queries, but should minimize the count
3. When you are confident, submit your answer using the answer tag
4. If the answer is incorrect, the game fails
"""

    contextualized_rule_zh_1 = """\
智能路口通行调度系统初始化。当前有 {n} 辆自动驾驶测试车（编号标签集合为 {{1, 2, ..., {n}}}）正在等待通过特殊测试路口。
这些车辆标签存在一个未知但固定的严格通行优先级关系（全序关系）。你的目标是推断出按照通行优先级从先到后排列时，排在第 {k} 位的车辆标签是哪一个。

你可以反复向调度系统提出比较查询，每次输入两个不同的车辆标签 i 和 j，系统会反馈在这两个标签中谁的优先级更高（在全序中排在前面）。请尽可能用较少的查询次数找出目标标签。

每次只能包含一个操作标签。请使用以下 XML 格式：

- 比较查询（例如比较标签 3 和 5）：
<query_compare>3,5</query_compare>

- 提交最终答案（例如认为第 {k} 位通行的是标签 7）：
<answer>7</answer>

注意事项：
1. 比较查询中的两个车辆标签必须不同，且都在 1 到 {n} 范围内
2. 你可以进行任意多次比较查询，但应尽量减少查询次数提高调度效率
3. 当你确定目标车辆标签后，使用 answer 标签提交
4. 如果答案错误，调度失败
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Autonomous Intersection Scheduling System initialized. There are currently {n} autonomous test vehicles (with ID label set {{1, 2, ..., {n}}}) waiting to pass through a special test intersection.
These vehicle labels have an unknown but fixed strict priority order (total order) for passing. Your goal is to deduce which vehicle label will be at the {k}-th position when they are sorted from highest to lowest priority.

You can repeatedly submit comparison queries to the scheduling system. Each query compares two different vehicle labels i and j, and the system will tell you which label comes first in the total order (i.e., has a higher priority). Try to find the target label with as few queries as possible.

Each query must contain only one XML tag. Use the following format:

- Comparison Query (e.g., comparing labels 3 and 5):
<query_compare>3,5</query_compare>

- Submit Final Answer (e.g., if you determine the {k}-th vehicle to pass is label 7):
<answer>7</answer>

Notes:
1. The two vehicle labels in a comparison query must be different and within the range 1 to {n}.
2. You can make any number of comparison queries, but should minimize the count to ensure scheduling efficiency.
3. When you are confident about the target vehicle label, submit your answer using the answer tag.
4. If the answer is incorrect, the scheduling fails.
"""

    contextualized_rule_zh_2 = """\
急诊分诊排号系统启动。急诊室目前接收了 {n} 名患者（就诊手环标签集合为 {{1, 2, ..., {n}}}），系统已根据病情严重程度生成了一个严格的就诊优先级排序（全序关系），但具体顺序对你隐藏。
你的任务是找出按照医疗紧急度从高到低排列后，将被安排在第 {k} 位就诊的患者标签。

你可以反复向分诊系统提出比较查询，每次输入两个不同的手环标签 i 和 j，系统会告知你这两个标签中谁在全序中排在前面（即谁先就诊）。请尽可能用较少的查询次数锁定目标标签。

每次只能包含一个操作标签。请使用以下 XML 格式：

- 比较查询（例如比较标签 3 和 5）：
<query_compare>3,5</query_compare>

- 提交最终答案（例如认为第 {k} 位就诊的是标签 7）：
<answer>7</answer>

注意事项：
1. 比较查询中的两个手环标签必须不同，且都在 1 到 {n} 范围内
2. 你可以进行任意多次比较查询，但应尽量减少查询次数以免耽误救治
3. 当你确定答案后，使用 answer 标签提交
4. 如果答案错误，系统报错退出
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Emergency Triage System activated. The emergency room has received {n} patients (with wristband label set {{1, 2, ..., {n}}}). The system has internally generated a strict medical urgency order (total order) based on their conditions, but the exact sequence is hidden from you.
Your task is to identify the patient label who is ranked exactly {k}-th in urgency.

You can repeatedly ask the triage system comparison queries. Each query compares two different wristband labels i and j, and the system will tell you which label comes first in the total order (i.e., treated earlier). Try to find the target label with as few queries as possible.

Each query must contain only one XML tag. Use the following format:

- Comparison Query (e.g., comparing labels 3 and 5):
<query_compare>3,5</query_compare>

- Submit Final Answer (e.g., if you conclude the {k}-th patient to be treated is label 7):
<answer>7</answer>

Notes:
1. The two wristband labels in a comparison query must be different and within the range 1 to {n}.
2. You can make any number of comparison queries, but should minimize the count to avoid delaying medical care.
3. When you are confident about the target patient label, submit your answer using the answer tag.
4. If the answer is incorrect, the system reports an error and fails.
"""

    contextualized_rule_zh_3 = """\
特等奖学金综合评审系统就绪。本年度有 {n} 名候选学生（申请编号标签集合为 {{1, 2, ..., {n}}}）。评委会根据各项指标确定了他们之间的一个未知但固定的严格综合排名（全序关系）。
你的目标是找出在这个排名体系中，综合成绩排在第 {k} 位的候选人标签。

你可以反复向评审数据库提出比较查询，每次输入两个不同的候选人标签 i 和 j，系统会反馈在全序关系中谁排在前面。请尽可能用较少的查询次数找出答案。

每次只能包含一个操作标签。请使用以下 XML 格式：

- 比较查询（例如比较标签 3 和 5）：
<query_compare>3,5</query_compare>

- 提交最终答案（例如认为排在第 {k} 位的是标签 7）：
<answer>7</answer>

注意事项：
1. 比较查询中的两个候选人标签必须不同，且都在 1 到 {n} 范围内
2. 你可以进行任意多次比较查询，但应尽量减少查询次数
3. 当你确定候选人标签后，使用 answer 标签提交
4. 如果答案错误，评审检索失败
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Top Scholarship Comprehensive Review System ready. There are {n} candidate students this year (application ID label set {{1, 2, ..., {n}}}). The committee has established a strict comprehensive ranking (total order) among them based on academic metrics, which remains hidden from you.
Your goal is to identify the candidate label who ranks exactly {k}-th in this system.

You can repeatedly query the review database with comparison requests. Each query compares two different candidate labels i and j, and the system will tell you which label comes first in the total order. Try to find the answer with as few queries as possible.

Each query must contain only one XML tag. Use the following format:

- Comparison Query (e.g., comparing labels 3 and 5):
<query_compare>3,5</query_compare>

- Submit Final Answer (e.g., if you believe the {k}-th ranked candidate is label 7):
<answer>7</answer>

Notes:
1. The two candidate labels in a comparison query must be different and within the range 1 to {n}.
2. You can make any number of comparison queries, but should minimize the count.
3. When you are confident about the candidate label, submit your answer using the answer tag.
4. If the answer is incorrect, the review retrieval fails.
"""

    contextualized_rule_zh_4 = """\
智能车间生产排程系统启动。当前产线上有 {n} 个待加工的生产批次（批次标签集合为 {{1, 2, ..., {n}}}）。系统已根据交货期和工艺要求，生成了严格的加工顺序（全序关系）。
你需要推断出按照这一加工顺序，被安排在第 {k} 位进行加工的批次标签是哪一个。

你可以反复向排程系统提出比较查询，每次输入两个不同的批次标签 i 和 j，系统会反馈这两个标签中谁在全序中排在前面（优先加工）。请尽可能用较少的查询次数找出目标标签。

每次只能包含一个操作标签。请使用以下 XML 格式：

- 比较查询（例如比较标签 3 和 5）：
<query_compare>3,5</query_compare>

- 提交最终答案（例如认为第 {k} 个加工的是标签 7）：
<answer>7</answer>

注意事项：
1. 比较查询中的两个批次标签必须不同，且都在 1 到 {n} 范围内
2. 你可以进行任意多次比较查询，但应尽量减少系统负载
3. 当你确定目标批次标签后，使用 answer 标签提交
4. 如果答案错误，排程调度失败
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Smart Factory Production Scheduling System activated. There are {n} pending production batches on the line (batch label set {{1, 2, ..., {n}}}). The system has generated a strict processing sequence (total order) based on delivery deadlines.
You need to deduce which batch label is scheduled to be processed at the {k}-th position in this sequence.

You can repeatedly submit comparison queries to the scheduling system. Each query compares two different batch labels i and j, and the system will tell you which label comes first in the total order (i.e., processed earlier). Try to find the target label with as few queries as possible.

Each query must contain only one XML tag. Use the following format:

- Comparison Query (e.g., comparing labels 3 and 5):
<query_compare>3,5</query_compare>

- Submit Final Answer (e.g., if you deduce the {k}-th processed batch is label 7):
<answer>7</answer>

Notes:
1. The two batch labels in a comparison query must be different and within the range 1 to {n}.
2. You can make any number of comparison queries, but should minimize the system load.
3. When you are confident about the target batch label, submit your answer using the answer tag.
4. If the answer is incorrect, the scheduling fails.
"""

    contextualized_rule_zh_5 = """\
核心物证审查排序系统登入。本次案件涉及 {n} 件关键物证（证据编号标签集合为 {{1, 2, ..., {n}}}）。为了保证证据链的严密性，法务团队设定了严格的审查先后顺序（全序关系），该顺序当前属于保密状态。
你的任务是查明在这个审查序列中，被安排在第 {k} 位出示并审查的物证标签是什么。

你可以反复向系统提出比较查询，每次输入两个不同的证据标签 i 和 j，系统会告诉你在这两个标签中哪一个在全序中排在前面（更早被审查）。请尽可能用较少的查询次数得出结论。

每次只能包含一个操作标签。请使用以下 XML 格式：

- 比较查询（例如比较标签 3 和 5）：
<query_compare>3,5</query_compare>

- 提交最终答案（例如认为第 {k} 个审查的是标签 7）：
<answer>7</answer>

注意事项：
1. 比较查询中的两个证据标签必须不同，且都在 1 到 {n} 范围内
2. 你可以进行任意多次比较查询，但应尽量减少查询次数
3. 当你确定目标物证标签后，使用 answer 标签提交
4. 如果答案错误，审查模拟失败
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Core Evidence Review Sequencing System logged in. This case involves {n} key pieces of physical evidence (exhibit label set {{1, 2, ..., {n}}}). To ensure the rigor of the chain of custody, the legal team has established a strict chronological order for review (total order), which is currently classified.
Your task is to determine which exhibit label is scheduled to be presented and reviewed at the {k}-th position in this sequence.

You can repeatedly query the system with comparison requests. Each query compares two different exhibit labels i and j, and the system will tell you which label comes first in the total order (i.e., reviewed earlier). Try to reach a conclusion with as few queries as possible.

Each query must contain only one XML tag. Use the following format:

- Comparison Query (e.g., comparing labels 3 and 5):
<query_compare>3,5</query_compare>

- Submit Final Answer (e.g., if you determine the {k}-th exhibit to be reviewed is label 7):
<answer>7</answer>

Notes:
1. The two exhibit labels in a comparison query must be different and within the range 1 to {n}.
2. You can make any number of comparison queries, but should minimize the count.
3. When you are confident about the target exhibit label, submit your answer using the answer tag.
4. If the answer is incorrect, the review simulation fails.
"""

    tags = ["answer", "query_compare"]
    
    reasoning_type = "演绎推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "k": 3,
                "order": [3, 1, 5, 2, 4],
            },
            2: {
                "n": 7,
                "k": 2,
                "order": [2, 5, 1, 7, 3, 6, 4],
            },
            3: {
                "n": 10,
                "k": 7,
                "order": [5, 2, 8, 1, 9, 4, 7, 3, 10, 6],
            },
            4: {
                "n": 12,
                "k": 5,
                "order": [7, 3, 11, 2, 9, 1, 5, 12, 4, 8, 6, 10],
            },
            5: {
                "n": 15,
                "k": 10,
                "order": [8, 3, 12, 5, 14, 1, 9, 11, 4, 15, 7, 2, 13, 6, 10],
            },
        },
        "en": {
            1: {
                "n": 5,
                "k": 3,
                "order": [3, 1, 5, 2, 4],
            },
            2: {
                "n": 7,
                "k": 2,
                "order": [2, 5, 1, 7, 3, 6, 4],
            },
            3: {
                "n": 10,
                "k": 7,
                "order": [5, 2, 8, 1, 9, 4, 7, 3, 10, 6],
            },
            4: {
                "n": 12,
                "k": 5,
                "order": [7, 3, 11, 2, 9, 1, 5, 12, 4, 8, 6, 10],
            },
            5: {
                "n": 15,
                "k": 10,
                "order": [8, 3, 12, 5, 14, 1, 9, 11, 4, 15, 7, 2, 13, 6, 10],
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
        self._game_info["k"] = cfg["k"]
        
        self.order = cfg["order"]
        
        self.position_map = {}
        for pos, label in enumerate(self.order, start=1):
            self.position_map[label] = pos
        
        self.correct_answer = self.order[cfg["k"] - 1]
        
        self.query_count = 0

    def evaluate(self, parsed_info):
        try:
            answer = int(parsed_info["answer"].strip())
            return answer == self.correct_answer
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if "query_compare" not in parsed_info:
            if self.config.language == "zh":
                return "错误：无效的查询类型。"
            else:
                return "Error: Invalid query type."
        
        try:
            raw = parsed_info["query_compare"]
            parts = [x.strip() for x in raw.split(",")]
            
            if len(parts) != 2:
                raise ValueError("Must compare exactly two labels")
            
            i, j = int(parts[0]), int(parts[1])
            
            n = self._game_info["n"]
            if i < 1 or i > n or j < 1 or j > n:
                if self.config.language == "zh":
                    return f"错误：标签必须在 1 到 {n} 范围内。"
                else:
                    return f"Error: Labels must be within range 1 to {n}."
            
            if i == j:
                if self.config.language == "zh":
                    return "错误：比较的两个标签必须不同。"
                else:
                    return "Error: The two labels must be different."
            
            self.query_count += 1
            
            pos_i = self.position_map[i]
            pos_j = self.position_map[j]
            
            if self.config.language == "zh":
                if pos_i < pos_j:
                    return f"标签 {i} 在全序中先于标签 {j}。"
                else:
                    return f"标签 {j} 在全序中先于标签 {i}。"
            else:
                if pos_i < pos_j:
                    return f"Label {i} comes before label {j} in the total order."
                else:
                    return f"Label {j} comes before label {i} in the total order."
                    
        except ValueError as ve:
            if self.config.language == "zh":
                return f"错误：查询格式无效。请使用格式 <query_compare>i,j</query_compare>，其中 i 和 j 是不同的整数。"
            else:
                return f"Error: Invalid query format. Use format <query_compare>i,j</query_compare> where i and j are different integers."
        except Exception as e:
            if self.config.language == "zh":
                return f"错误：处理查询时发生异常 - {str(e)}"
            else:
                return f"Error: Exception occurred while processing query - {str(e)}"

    def _cf_make_wrong(self, correct: str) -> str:
        if self.config.language == "zh":
            m = re.search(r'标签\s*(\d+)\s*在全序中先于标签\s*(\d+)', correct)
            if m:
                a, b = m.group(1), m.group(2)
                return f"标签 {b} 在全序中先于标签 {a}。"
        else:
            m = re.search(r'Label\s*(\d+)\s*comes before label\s*(\d+)', correct)
            if m:
                a, b = m.group(1), m.group(2)
                return f"Label {b} comes before label {a} in the total order."

        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct or "否" in correct:
                return correct.replace("是", "TEMP").replace("否", "是").replace("TEMP", "否")
        else:
            lower_correct = correct.lower()
            if "yes" in lower_correct or "no" in lower_correct:
                ret = correct
                ret = ret.replace("Yes", "TEMP_YES").replace("yes", "TEMP_yes")
                ret = ret.replace("No", "Yes").replace("no", "yes")
                ret = ret.replace("TEMP_YES", "No").replace("TEMP_yes", "no")
                return ret

        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        n = self._game_info["n"]
        lang = self.config.language
        
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                pos_i = self.position_map[i]
                pos_j = self.position_map[j]
                
                answer = ""
                if lang == "zh":
                    if pos_i < pos_j:
                        answer = f"标签 {i} 在全序中先于标签 {j}。"
                    else:
                        answer = f"标签 {j} 在全序中先于标签 {i}。"
                else:
                    if pos_i < pos_j:
                        answer = f"Label {i} comes before label {j} in the total order."
                    else:
                        answer = f"Label {j} comes before label {i} in the total order."
                
                query_str = f"<query_compare>{i},{j}</query_compare>"
                
                queries.append({
                    "query": query_str,
                    "answer": answer
                })
        
        return queries