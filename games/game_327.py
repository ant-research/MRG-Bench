from .base import Game
import re

class MonotonicThresholdGame(Game):

    game_rule_zh = """\
我们来玩一个"单调阈值定位"的推理游戏，规则如下：

游戏设定了一个有序索引集合 {{1, 2, ..., {n}}}。存在唯一的阈值 K，它定义了一个布尔谓词 P(i)，满足：
- 当 i 小于 K 时，P(i) 为 False
- 当 i 大于等于 K 时，P(i) 为 True

这是一条从 False 到 True 的单调转变。保证至少存在一个 True（即 K 存在且唯一）。

你的目标是确定这个阈值 K（即满足 P(i) 为 True 的最小索引）。你可以向我进行以下操作：

1. 查询操作：查询某个索引 i 的谓词值 P(i)。我会回答 "True" 或 "False"。如果索引超出范围，我会回答 "非法索引"。
2. 提交操作：当你确定答案后，提交你认为的阈值 K。

请尽可能用最少的查询次数找到正确答案。

- 查询索引 i 的谓词值（例如查询索引 5）：
<query>{query_idx}</query>

- 提交最终答案（例如提交阈值为 7）：
<answer>{answer_value}</answer>

每次只能包含一个标签。
"""

    game_rule_en = """\
Let's play a "Monotonic Threshold Locating" deduction game. Here are the rules:

The game has an ordered index set {{1, 2, ..., {n}}}. There exists a unique threshold K that defines a boolean predicate P(i), satisfying:
- When i is less than K, P(i) is False
- When i is greater than or equal to K, P(i) is True

This is a monotonic transition from False to True. It is guaranteed that at least one True exists (i.e., K exists and is unique).

Your goal is to determine this threshold K (the minimum index where P(i) is True). You can perform the following operations:

1. Query Operation: Query the predicate value P(i) for a certain index i. I will answer "True" or "False". If the index is out of range, I will answer "Invalid index".
2. Submit Operation: When you are confident, submit your answer for the threshold K.

Try to find the correct answer with as few queries as possible.

- Query the predicate value of index i (e.g., querying index 5):
<query>{query_idx}</query>

- Submit final answer (e.g., submitting threshold as 7):
<answer>{answer_value}</answer>

Only one tag is allowed per turn.
"""

    contextualized_rule_zh_1 = """\
【交通场景】
我们来执行一项“道路结冰临界点定位”任务，规则如下：

沿盘山高速公路有一系列海拔递增的监测点，编号集合为 {{1, 2, ..., {n}}}。存在唯一的结冰临界点 K，它定义了路面状态 P(i)，满足：
- 当监测点编号 i 小于 K 时，P(i) 为 False（未结冰，路面畅通）
- 当监测点编号 i 大于等于 K 时，P(i) 为 True（已结冰，存在隐患）

这是一条从 False 到 True 的单调转变。保证至少存在一个 True（即临界点 K 必定存在）。

你的目标是用最少的查询次数，排查出这个结冰临界点 K（即出现结冰现象的最小监测点编号）。你可以向我进行以下操作：

1. 查询操作：查询某个监测点 i 的状态 P(i)。我会回答 "True" 或 "False"。如果编号超出范围，我会回答 "非法索引"。
2. 提交操作：当你确定答案后，提交你认为的结冰临界点 K。

- 查询监测点 i 的状态（例如查询监测点 5）：
<query>{query_idx}</query>

- 提交最终答案（例如提交临界点为 7）：
<answer>{answer_value}</answer>

每次只能包含一个标签。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's perform a "Road Icing Critical Point Locating" task. Here are the rules:

Along a winding mountain highway, there is a set of monitoring stations with increasing altitude, indexed as {{1, 2, ..., {n}}}. There exists a unique icing critical point K that defines the road surface state P(i), satisfying:
- When station index i is less than K, P(i) is False (no ice, road clear)
- When station index i is greater than or equal to K, P(i) is True (iced, hazard present)

This is a monotonic transition from False to True. It is guaranteed that at least one True exists (i.e., critical point K exists and is unique).

Your goal is to determine this critical point K (the minimum index where P(i) is True) with as few queries as possible. You can perform the following operations:

1. Query Operation: Query the state P(i) of a certain station i. I will answer "True" or "False". If the index is out of range, I will answer "Invalid index".
2. Submit Operation: When you are confident, submit your answer for the critical point K.

- Query the state of station i (e.g., querying station 5):
<query>{query_idx}</query>

- Submit final answer (e.g., submitting critical point as 7):
<answer>{answer_value}</answer>

Only one tag is allowed per turn.
"""

    contextualized_rule_zh_2 = """\
【医疗场景】
我们来执行一项“最小有效给药剂量测定”任务，规则如下：

在某新型药物的临床试验中，设定了有序递增的给药剂量等级集合 {{1, 2, ..., {n}}}。存在唯一的起效临界等级 K，它定义了受试者的临床反应 P(i)，满足：
- 当剂量等级 i 小于 K 时，P(i) 为 False（未见效，无显著体征改善）
- 当剂量等级 i 大于等于 K 时，P(i) 为 True（已见效，达到靶向治疗指标）

这是一条从 False 到 True 的单调转变。保证至少存在一个 True（即有效剂量等级 K 必定存在）。

你的目标是确定这个最小有效给药剂量等级 K。你可以向我进行以下操作：

1. 查询操作：查询某个剂量等级 i 的临床反应 P(i)。我会回答 "True" 或 "False"。如果等级超出范围，我会回答 "非法索引"。
2. 提交操作：当你确定答案后，提交你认为的起效临界等级 K。

请尽可能用最少的查询次数完成测定。

- 查询剂量等级 i 的临床反应（例如查询等级 5）：
<query>{query_idx}</query>

- 提交最终答案（例如提交起效等级为 7）：
<answer>{answer_value}</answer>

每次只能包含一个标签。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's perform a "Minimum Effective Drug Dose Determination" task. Here are the rules:

In a clinical trial for a novel medication, there is an ordered set of increasing dosage levels {{1, 2, ..., {n}}}. There exists a unique effective critical level K that defines the subject's clinical response P(i), satisfying:
- When dosage level i is less than K, P(i) is False (ineffective, no significant clinical improvement)
- When dosage level i is greater than or equal to K, P(i) is True (effective, targeted therapeutic metrics achieved)

This is a monotonic transition from False to True. It is guaranteed that at least one True exists (i.e., critical dose K exists and is unique).

Your goal is to determine this minimum effective dosage level K. You can perform the following operations:

1. Query Operation: Query the clinical response P(i) for a certain dosage level i. I will answer "True" or "False". If the index is out of range, I will answer "Invalid index".
2. Submit Operation: When you are confident, submit your answer for the effective critical level K.

Try to complete the determination with as few queries as possible.

- Query the response of dosage level i (e.g., querying level 5):
<query>{query_idx}</query>

- Submit final answer (e.g., submitting effective level as 7):
<answer>{answer_value}</answer>

Only one tag is allowed per turn.
"""

    contextualized_rule_zh_3 = """\
【教育场景】
我们来执行一项“自适应认知边界评估”任务，规则如下：

计算机自适应测试系统为你准备了按难度排序的题库等级集合 {{1, 2, ..., {n}}}。针对该名学生，存在唯一的认知边界等级 K，它定义了学生的解答情况 P(i)，满足：
- 当题目难度等级 i 小于 K 时，P(i) 为 False（未超出认知边界，能够顺利解答）
- 当题目难度等级 i 大于等于 K 时，P(i) 为 True（已超出认知边界，无法解答）

这是一条从 False 到 True 的单调转变。保证至少存在一个 True（即边界等级 K 必定存在）。

你的目标是精准评估出该学生的认知边界等级 K（即无法解答的最小题目难度等级）。你可以向我进行以下操作：

1. 查询操作：查询该生对某个难度等级 i 的解答情况 P(i)。我会回答 "True" 或 "False"。如果等级超出范围，我会回答 "非法索引"。
2. 提交操作：当你确定答案后，提交你认为的认知边界等级 K。

请尽可能用最少的查询次数找到正确答案。

- 查询难度等级 i 的解答情况（例如查询等级 5）：
<query>{query_idx}</query>

- 提交最终答案（例如提交认知边界等级为 7）：
<answer>{answer_value}</answer>

每次只能包含一个标签。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's perform an "Adaptive Cognitive Boundary Assessment" task. Here are the rules:

The computerized adaptive testing system provides a set of item difficulty levels ordered ascendingly as {{1, 2, ..., {n}}}. For a specific student, there exists a unique cognitive boundary level K that defines the student's performance P(i), satisfying:
- When item difficulty level i is less than K, P(i) is False (within cognitive limits, able to solve correctly)
- When item difficulty level i is greater than or equal to K, P(i) is True (exceeds cognitive limits, unable to solve)

This is a monotonic transition from False to True. It is guaranteed that at least one True exists (i.e., boundary level K exists and is unique).

Your goal is to precisely assess this cognitive boundary level K (the minimum difficulty level the student cannot solve). You can perform the following operations:

1. Query Operation: Query the performance P(i) for a certain difficulty level i. I will answer "True" or "False". If the index is out of range, I will answer "Invalid index".
2. Submit Operation: When you are confident, submit your answer for the cognitive boundary level K.

Try to find the correct answer with as few queries as possible.

- Query the performance at difficulty level i (e.g., querying level 5):
<query>{query_idx}</query>

- Submit final answer (e.g., submitting cognitive boundary as 7):
<answer>{answer_value}</answer>

Only one tag is allowed per turn.
"""

    contextualized_rule_zh_4 = """\
【制造业/工业场景】
我们来执行一项“材料屈服强度临界点测试”任务，规则如下：

在机械抗压疲劳测试中，设备提供了一组递增的施压档位集合 {{1, 2, ..., {n}}}。针对该批次材料，存在唯一的临界屈服档位 K，它定义了材料的形变状态 P(i)，满足：
- 当施压档位 i 小于 K 时，P(i) 为 False（未发生塑性形变，结构完好）
- 当施压档位 i 大于等于 K 时，P(i) 为 True（发生不可逆塑性形变甚至断裂）

这是一条从 False 到 True 的单调转变。保证至少存在一个 True（即临界屈服档位 K 必定存在）。

你的目标是排查出这个临界屈服档位 K。你可以向我进行以下操作：

1. 查询操作：查询某个施压档位 i 的材料形变状态 P(i)。我会回答 "True" 或 "False"。如果档位超出范围，我会回答 "非法索引"。
2. 提交操作：当你确定答案后，提交你认为的临界屈服档位 K。

请尽可能用最少的查询次数完成测试。

- 查询施压档位 i 的形变状态（例如查询档位 5）：
<query>{query_idx}</query>

- 提交最终答案（例如提交临界档位为 7）：
<answer>{answer_value}</answer>

每次只能包含一个标签。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's perform a "Material Yield Strength Critical Point Testing" task. Here are the rules:

In a mechanical compressive fatigue test, the equipment provides a set of increasing pressure gear settings {{1, 2, ..., {n}}}. For this batch of materials, there exists a unique critical yield gear K that defines the material's deformation state P(i), satisfying:
- When pressure gear i is less than K, P(i) is False (no plastic deformation, structurally intact)
- When pressure gear i is greater than or equal to K, P(i) is True (irreversible plastic deformation or fracture occurred)

This is a monotonic transition from False to True. It is guaranteed that at least one True exists (i.e., critical yield gear K exists and is unique).

Your goal is to determine this critical yield gear K. You can perform the following operations:

1. Query Operation: Query the deformation state P(i) for a certain pressure gear i. I will answer "True" or "False". If the index is out of range, I will answer "Invalid index".
2. Submit Operation: When you are confident, submit your answer for the critical yield gear K.

Try to complete the test with as few queries as possible.

- Query the deformation state at pressure gear i (e.g., querying gear 5):
<query>{query_idx}</query>

- Submit final answer (e.g., submitting critical gear as 7):
<answer>{answer_value}</answer>

Only one tag is allowed per turn.
"""

    contextualized_rule_zh_5 = """\
【法律场景】
我们来执行一项“财务违规时间节点审查”任务，规则如下：

在对某涉案企业的专项审计中，我们锁定了按时间顺序排列的账目周期集合 {{1, 2, ..., {n}}}。存在唯一的首个违规周期 K，它定义了该周期的合规判定状态 P(i)，满足：
- 当账目周期 i 小于 K 时，P(i) 为 False（审计合规，未见异常操作）
- 当账目周期 i 大于等于 K 时，P(i) 为 True（审计违规，自此引入并延续了非法避税手段）

这是一条从 False 到 True 的单调转变。保证至少存在一个 True（即开始违规的周期 K 必定存在）。

你的目标是精准定位这起经济案件的起始违规点 K。你可以向我进行以下操作：

1. 查询操作：查询某个账目周期 i 的合规判定状态 P(i)。我会回答 "True" 或 "False"。如果周期索引超出范围，我会回答 "非法索引"。
2. 提交操作：当你获取充分证据后，提交你认为的首个违规周期 K。

请尽可能用最少的查询次数查明真相。

- 查询账目周期 i 的判定状态（例如查询周期 5）：
<query>{query_idx}</query>

- 提交最终答案（例如提交违规起始周期为 7）：
<answer>{answer_value}</answer>

每次只能包含一个标签。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's perform a "Financial Violation Timeline Audit" task. Here are the rules:

In a specialized audit of a suspected enterprise, we have targeted a chronologically ordered set of accounting periods {{1, 2, ..., {n}}}. There exists a unique initial violation period K that defines the compliance status P(i) for that period, satisfying:
- When accounting period i is less than K, P(i) is False (audit compliant, no irregular operations found)
- When accounting period i is greater than or equal to K, P(i) is True (audit violation, illegal tax evasion methods were introduced and continued from then on)

This is a monotonic transition from False to True. It is guaranteed that at least one True exists (i.e., initial violation period K exists and is unique).

Your goal is to precisely locate the starting point of the violation K for this economic case. You can perform the following operations:

1. Query Operation: Query the compliance status P(i) for a certain accounting period i. I will answer "True" or "False". If the period index is out of range, I will answer "Invalid index".
2. Submit Operation: When you have gathered sufficient evidence, submit your answer for the initial violation period K.

Try to uncover the truth with as few queries as possible.

- Query the compliance status for accounting period i (e.g., querying period 5):
<query>{query_idx}</query>

- Submit final answer (e.g., submitting initial violation period as 7):
<answer>{answer_value}</answer>

Only one tag is allowed per turn.
"""

    tags = ["answer", "query"]
    
    reasoning_type = "演绎推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "k": 3,
            },
            2: {
                "n": 8,
                "k": 5,
            },
            3: {
                "n": 16,
                "k": 10,
            },
            4: {
                "n": 32,
                "k": 20,
            },
            5: {
                "n": 64,
                "k": 45,
            },
        },
        "en": {
            1: {
                "n": 4,
                "k": 3,
            },
            2: {
                "n": 8,
                "k": 5,
            },
            3: {
                "n": 16,
                "k": 10,
            },
            4: {
                "n": 32,
                "k": 20,
            },
            5: {
                "n": 64,
                "k": 45,
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
        self._game_info["query_idx"] = "i"
        self._game_info["answer_value"] = "k"
        
        self.threshold_k = cfg["k"]
        
        self.query_count = 0

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        try:
            submitted_k = int(raw_ans)
        except ValueError:
            return False
        
        return submitted_k == self.threshold_k

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            true_res = "True"
            false_res = "False"
            invalid_res = "非法索引"
        else:
            true_res = "True"
            false_res = "False"
            invalid_res = "Invalid index"

        if "query" in parsed_info:
            raw_query = parsed_info["query"].strip()
            
            try:
                query_idx = int(raw_query)
            except ValueError:
                return invalid_res
            
            n = self._game_info["n"]
            if query_idx < 1 or query_idx > n:
                return invalid_res
            
            self.query_count += 1
            
            if query_idx >= self.threshold_k:
                return true_res
            else:
                return false_res
        else:
            raise ValueError("No valid query tag found.")
            
    def get_all_possible_queries(self):
        n = self._game_info["n"]
        results = []
        
        if self.config.language == "zh":
            true_res = "True"
            false_res = "False"
        else:
            true_res = "True"
            false_res = "False"
            
        for i in range(1, n + 1):
            query_val = str(i)
            ans = true_res if i >= self.threshold_k else false_res
            
            results.append({
                "query": f"<query>{query_val}</query>",
                "answer": ans
            })
            
        return results

    def _cf_make_wrong(self, correct):
        if correct == "True":
            return "False"
        if correct == "False":
            return "True"
        
        if correct in ("非法索引", "Invalid index"):
            return "True"
            
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        elif self.config.language == "en":
            low_c = correct.lower()
            if low_c == "yes":
                if correct.isupper(): return "NO"
                if correct.istitle(): return "No"
                return "no"
            if low_c == "no":
                if correct.isupper(): return "YES"
                if correct.istitle(): return "Yes"
                return "yes"
        
        return correct + "_WRONG"