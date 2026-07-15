from .base import Game
import re

class AbstractReasoningGame(Game):

    game_rule_zh = """\
我们来玩一个"抽象推理"游戏，规则如下：

游戏设定了一个固定但未知的正整数 N，以及一个固定但未知的响应规律 f。当你提交一个正整数 b 时，系统会根据规律 f 返回一个整数 r = f(b)。

关键信息：
- 响应规律在整个游戏过程中保持不变，仅由 b 与 N 决定，与历史查询无关
- 对于相同的 b，系统始终返回相同的 r
- 你可以提交的 b 的范围是 1 到 1000 之间的正整数
- N 是一个在合理范围内的正整数

你的目标是通过尽可能少的查询，归纳出响应规律并确定 N 的值。

你可以进行以下两种操作：

1. **查询操作**：提交一个正整数 b（1 到 1000），系统会返回对应的整数 r。

2. **提交最终结论**：当你认为已经归纳出规律时，提交你对 N 的猜测值以及对规律的描述。

- 查询操作（例如查询 b=10）：
<query>10</query>

- 提交最终结论：
<answer>N=15, rule=r 始终等于 b 和 N 中的较小值</answer>

注意：
- 规律描述必须准确表达 r 与 b、N 之间的关系
- N 的猜测值必须是正整数
- 每次只能进行一种操作（查询或提交结论）
"""

    game_rule_en = """\
Let's play an "Abstract Reasoning" game. Here are the rules:

The game has set a fixed but unknown positive integer N, and a fixed but unknown response rule f. When you submit a positive integer b, the system will return an integer r = f(b) according to rule f.

Key information:
- The response rule remains constant throughout the game, determined only by b and N, independent of query history
- For the same b, the system always returns the same r
- The range of b you can submit is between 1 and 1000
- N is a positive integer within a reasonable range

Your goal is to infer the response rule and determine the value of N through as few queries as possible.

You can perform two types of operations:

1. **Query Operation**: Submit a positive integer b (1 to 1000), and the system will return the corresponding integer r.

2. **Submit Final Conclusion**: When you believe you have inferred the rule, submit your guess for N and your description of the rule.

- Query Operation (e.g., querying b=10):
<query>10</query>

- Submit Final Conclusion:
<answer>N=15, rule=r is always equal to the smaller of b and N</answer>

Note:
- The rule description must accurately express the relationship between r, b, and N
- The guessed value of N must be a positive integer
- Only one type of operation can be performed at a time (query or submit conclusion)
"""

    contextualized_rule_zh_1 = """\
我们正在进行一项“智能交通信号灯调度系统”的黑盒测试。

系统设定了一个固定但未知的路口最大通行车辆容量 N，以及一个调度规律 f。当你输入传感器探测到的排队车辆数 b 时，系统会返回该周期的实际放行车辆数 r = f(b)。

关键信息：
- 调度规律在整个测试过程中保持不变，仅由 b 与 N 决定，与历史输入无关
- 对于相同的排队数量 b，系统始终返回相同的放行数量 r
- 你可以模拟的车辆数 b 的范围是 1 到 1000 之间的正整数
- 容量 N 是一个在合理范围内的正整数

你的目标是通过尽可能少的测试，归纳出系统的调度规律并确定路口的最大容量 N。

你可以进行以下两种操作：

1. **查询操作**：提交排队车辆数 b（1 到 1000），系统会返回实际放行车辆数 r。

2. **提交最终结论**：当你认为已经归纳出规律时，提交你对 N 的猜测值以及对规律的描述。

- 查询操作（例如查询排队数 b=10）：
<query>10</query>

- 提交最终结论：
<answer>N=15, rule=r 始终等于 b 和 N 中的较小值</answer>

注意：
- 规律描述必须准确表达实际放行量 r 与排队量 b、容量 N 之间的关系
- N 的猜测值必须是正整数
- 每次只能进行一种操作（查询或提交结论）
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
We are conducting a black-box test on an "Smart Traffic Signal Dispatch System".

The system has a fixed but unknown maximum vehicle capacity N for an intersection, and a dispatch rule f. When you input the queued vehicle count b detected by sensors, the system will return the actual number of dispatched vehicles r = f(b) for that cycle.

Key information:
- The dispatch rule remains constant throughout the testing process, determined only by b and N, independent of input history
- For the same queued count b, the system always returns the same dispatched count r
- The range of vehicle count b you can simulate is between 1 and 1000
- The capacity N is a positive integer within a reasonable range

Your goal is to infer the system's dispatch rule and determine the intersection's maximum capacity N through as few tests as possible.

You can perform two types of operations:

1. **Query Operation**: Submit a queued vehicle count b (1 to 1000), and the system will return the actual dispatched vehicle count r.

2. **Submit Final Conclusion**: When you believe you have inferred the rule, submit your guess for N and your description of the rule.

- Query Operation (e.g., querying queue count b=10):
<query>10</query>

- Submit Final Conclusion:
<answer>N=15, rule=r is always equal to the smaller of b and N</answer>

Note:
- The rule description must accurately express the relationship between the dispatched count r, queued count b, and capacity N
- The guessed value of N must be a positive integer
- Only one type of operation can be performed at a time (query or submit conclusion)
"""

    contextualized_rule_zh_2 = """\
我们正在进行一项“特效药剂代谢吸收测试”。

系统模拟设定了人体单次最大可吸收的药物有效成分剂量 N，以及一个代谢吸收规律 f。当你输入给药剂量 b 时，系统会返回人体实际吸收的剂量 r = f(b)。

关键信息：
- 吸收规律在整个测试过程中保持不变，仅由 b 与 N 决定，与历史给药数据无关
- 对于相同的给药剂量 b，系统始终返回相同的实际吸收剂量 r
- 你可以测试的给药剂量 b 的范围是 1 到 1000 之间的正整数（毫克）
- 吸收阈值 N 是一个在合理范围内的正整数

你的目标是通过尽可能少的测试，归纳出药物的吸收规律并确定人体的最大吸收阈值 N。

你可以进行以下两种操作：

1. **查询操作**：提交给药剂量 b（1 到 1000），系统会返回实际吸收剂量 r。

2. **提交最终结论**：当你认为已经归纳出规律时，提交你对 N 的猜测值以及对规律的描述。

- 查询操作（例如查询剂量 b=10）：
<query>10</query>

- 提交最终结论：
<answer>N=15, rule=r 始终等于 b 和 N 中的较小值</answer>

注意：
- 规律描述必须准确表达吸收量 r 与给药量 b、最大吸收量 N 之间的关系
- N 的猜测值必须是正整数
- 每次只能进行一种操作（查询或提交结论）
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
We are conducting a "Special Drug Metabolism and Absorption Test".

The system simulates a fixed but unknown single maximum absorption threshold N of the human body for a drug's active ingredient, and an absorption rule f. When you input the administered dose b, the system will return the actual absorbed dose r = f(b) by the body.

Key information:
- The absorption rule remains constant throughout the test, determined only by b and N, independent of historical dosage data
- For the same administered dose b, the system always returns the same actual absorbed dose r
- The range of administered dose b you can test is between 1 and 1000 (mg)
- The absorption threshold N is a positive integer within a reasonable range

Your goal is to infer the drug's absorption rule and determine the human body's maximum absorption threshold N through as few tests as possible.

You can perform two types of operations:

1. **Query Operation**: Submit an administered dose b (1 to 1000), and the system will return the actual absorbed dose r.

2. **Submit Final Conclusion**: When you believe you have inferred the rule, submit your guess for N and your description of the rule.

- Query Operation (e.g., querying dose b=10):
<query>10</query>

- Submit Final Conclusion:
<answer>N=15, rule=r is always equal to the smaller of b and N</answer>

Note:
- The rule description must accurately express the relationship between the absorbed dose r, administered dose b, and threshold N
- The guessed value of N must be a positive integer
- Only one type of operation can be performed at a time (query or submit conclusion)
"""

    contextualized_rule_zh_3 = """\
我们正在调试“在线课程学分转化评估系统”。

系统内部设定了该专业允许转换的最高核心学分数 N，以及一个学分认定规律 f。当你输入学生在其他平台获得的学分数 b 时，系统会返回最终认定的有效转换学分数 r = f(b)。

关键信息：
- 认定规律在整个评估过程中保持不变，仅由 b 与 N 决定，与历史申请记录无关
- 对于相同的获得学分 b，系统始终返回相同的有效转换学分 r
- 你可以模拟提交的学分数 b 的范围是 1 到 1000 之间的正整数
- 学分上限 N 是一个在合理范围内的正整数

你的目标是通过尽可能少的模拟申请，归纳出学分认定规律并确定系统的学分转换上限 N。

你可以进行以下两种操作：

1. **查询操作**：提交获得的学分数 b（1 到 1000），系统会返回有效转换学分数 r。

2. **提交最终结论**：当你认为已经归纳出规律时，提交你对 N 的猜测值以及对规律的描述。

- 查询操作（例如查询学分数 b=10）：
<query>10</query>

- 提交最终结论：
<answer>N=15, rule=r 始终等于 b 和 N 中的较小值</answer>

注意：
- 规律描述必须准确表达认定学分 r 与获得学分 b、上限 N 之间的关系
- N 的猜测值必须是正整数
- 每次只能进行一种操作（查询或提交结论）
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
We are debugging an "Online Course Credit Transfer Evaluation System".

The system has a built-in maximum transferable core credit limit N for the major, and a credit recognition rule f. When you input the credits b earned by a student on other platforms, the system will return the final recognized transferred credits r = f(b).

Key information:
- The recognition rule remains constant throughout the evaluation process, determined only by b and N, independent of application history
- For the same earned credits b, the system always returns the same recognized transferred credits r
- The range of earned credits b you can simulate is between 1 and 1000
- The credit limit N is a positive integer within a reasonable range

Your goal is to infer the credit recognition rule and determine the system's credit transfer limit N through as few simulated applications as possible.

You can perform two types of operations:

1. **Query Operation**: Submit earned credits b (1 to 1000), and the system will return the recognized transferred credits r.

2. **Submit Final Conclusion**: When you believe you have inferred the rule, submit your guess for N and your description of the rule.

- Query Operation (e.g., querying credits b=10):
<query>10</query>

- Submit Final Conclusion:
<answer>N=15, rule=r is always equal to the smaller of b and N</answer>

Note:
- The rule description must accurately express the relationship between recognized credits r, earned credits b, and the limit N
- The guessed value of N must be a positive integer
- Only one type of operation can be performed at a time (query or submit conclusion)
"""

    contextualized_rule_zh_4 = """\
我们正在对“工厂流水线的质量控制与装箱环节”进行投料测试。

流水线设定了标准运输周转箱的最大容量 N（件），以及一个装箱规律 f。当你输入传送带上送来的合格零件批次数量 b 时，系统会返回实际装入周转箱的零件数量 r = f(b)。

关键信息：
- 装箱规律在整个测试过程中保持不变，仅由 b 与 N 决定，与历史批次无关
- 对于相同的送来零件数量 b，系统始终返回相同的实际装箱数量 r
- 你可以投放的零件数 b 的范围是 1 到 1000 之间的正整数
- 周转箱容量 N 是一个在合理范围内的正整数

你的目标是通过尽可能少的投料测试，归纳出装箱规律并确定周转箱的标准容量 N。

你可以进行以下两种操作：

1. **查询操作**：提交送来的零件数 b（1 到 1000），系统会返回实际装箱的零件数 r。

2. **提交最终结论**：当你认为已经归纳出规律时，提交你对 N 的猜测值以及对规律的描述。

- 查询操作（例如查询投料 b=10）：
<query>10</query>

- 提交最终结论：
<answer>N=15, rule=r 始终等于 b 和 N 中的较小值</answer>

注意：
- 规律描述必须准确表达装箱数 r 与送来零件数 b、容量 N 之间的关系
- N 的猜测值必须是正整数
- 每次只能进行一种操作（查询或提交结论）
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
We are conducting feeding tests on the "Factory Assembly Line Quality Control and Packaging Process".

The assembly line has set a maximum capacity N (pieces) for standard transport totes, and a packaging rule f. When you input the number of qualified parts b delivered on the conveyor belt, the system will return the actual number of parts packed into the tote r = f(b).

Key information:
- The packaging rule remains constant throughout the testing process, determined only by b and N, independent of historical batches
- For the same delivered parts count b, the system always returns the same packed count r
- The range of parts b you can feed is between 1 and 1000
- The tote capacity N is a positive integer within a reasonable range

Your goal is to infer the packaging rule and determine the standard tote capacity N through as few feeding tests as possible.

You can perform two types of operations:

1. **Query Operation**: Submit a delivered parts count b (1 to 1000), and the system will return the actual packed parts count r.

2. **Submit Final Conclusion**: When you believe you have inferred the rule, submit your guess for N and your description of the rule.

- Query Operation (e.g., querying feeding count b=10):
<query>10</query>

- Submit Final Conclusion:
<answer>N=15, rule=r is always equal to the smaller of b and N</answer>

Note:
- The rule description must accurately express the relationship between packed parts r, delivered parts b, and capacity N
- The guessed value of N must be a positive integer
- Only one type of operation can be performed at a time (query or submit conclusion)
"""

    contextualized_rule_zh_5 = """\
我们正在使用“民事诉讼法定赔偿金核定系统”进行模拟裁决。

系统根据相关法律设定了该类案件的法定最高赔偿限额 N（万元），以及一个核定规律 f。当你输入原告主张并举证的实际损失金额 b 时，系统会返回法院最终判决支持的赔偿金额 r = f(b)。

关键信息：
- 核定规律在整个模拟过程中保持一致，仅由 b 与 N 决定，与历史裁决数据无关
- 对于相同的实际损失主张 b，系统始终返回相同的核准赔偿额 r
- 你可以输入的损失金额 b 的范围是 1 到 1000 之间的正整数（万元）
- 法定限额 N 是一个在合理范围内的正整数

你的目标是通过尽可能少的模拟裁决，归纳出法院的判决规律并确定该类案件的法定最高限额 N。

你可以进行以下两种操作：

1. **查询操作**：提交实际损失金额 b（1 到 1000），系统会返回判决支持的赔偿金额 r。

2. **提交最终结论**：当你认为已经归纳出规律时，提交你对 N 的猜测值以及对规律的描述。

- 查询操作（例如查询主张损失 b=10）：
<query>10</query>

- 提交最终结论：
<answer>N=15, rule=r 始终等于 b 和 N 中的较小值</answer>

注意：
- 规律描述必须准确表达核准赔偿 r 与实际损失 b、限额 N 之间的关系
- N 的猜测值必须是正整数
- 每次只能进行一种操作（查询或提交结论）
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
We are running simulated rulings using the "Civil Litigation Statutory Compensation Assessment System".

Based on relevant laws, the system has set a statutory maximum compensation limit N (in ten thousands) for this type of case, and an assessment rule f. When you input the actual loss amount b claimed and evidenced by the plaintiff, the system will return the compensation amount r = f(b) supported by the court's verdict.

Key information:
- The assessment rule remains consistent throughout the simulation, determined only by b and N, independent of historical ruling data
- For the same claimed actual loss b, the system always returns the same awarded compensation r
- The range of loss amount b you can input is between 1 and 1000 (in ten thousands)
- The statutory limit N is a positive integer within a reasonable range

Your goal is to infer the court's ruling rule and determine the statutory maximum limit N for this type of case through as few simulated rulings as possible.

You can perform two types of operations:

1. **Query Operation**: Submit a claimed loss amount b (1 to 1000), and the system will return the awarded compensation amount r.

2. **Submit Final Conclusion**: When you believe you have inferred the rule, submit your guess for N and your description of the rule.

- Query Operation (e.g., querying claimed loss b=10):
<query>10</query>

- Submit Final Conclusion:
<answer>N=15, rule=r is always equal to the smaller of b and N</answer>

Note:
- The rule description must accurately express the relationship between the awarded compensation r, claimed loss b, and limit N
- The guessed value of N must be a positive integer
- Only one type of operation can be performed at a time (query or submit conclusion)
"""

    tags = ["answer", "query"]
    
    reasoning_type = "归纳推理"
    data_structure = "集合"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "N": 10,
                "max_queries": 8,
                "max_answers": 2,
                "rule_desc": "r 始终等于 b 和 N 中的较小值"
            },
            2: {
                "N": 25,
                "max_queries": 8,
                "max_answers": 2,
                "rule_desc": "r 始终等于 b 和 N 中的较小值"
            },
            3: {
                "N": 50,
                "max_queries": 8,
                "max_answers": 2,
                "rule_desc": "r 始终等于 b 和 N 中的较小值"
            },
            4: {
                "N": 77,
                "max_queries": 8,
                "max_answers": 2,
                "rule_desc": "r 始终等于 b 和 N 中的较小值"
            },
            5: {
                "N": 100,
                "max_queries": 8,
                "max_answers": 2,
                "rule_desc": "r 始终等于 b 和 N 中的较小值"
            },
        },
        "en": {
            1: {
                "N": 10,
                "max_queries": 8,
                "max_answers": 2,
                "rule_desc": "r is always equal to the smaller of b and N"
            },
            2: {
                "N": 25,
                "max_queries": 8,
                "max_answers": 2,
                "rule_desc": "r is always equal to the smaller of b and N"
            },
            3: {
                "N": 50,
                "max_queries": 8,
                "max_answers": 2,
                "rule_desc": "r is always equal to the smaller of b and N"
            },
            4: {
                "N": 77,
                "max_queries": 8,
                "max_answers": 2,
                "rule_desc": "r is always equal to the smaller of b and N"
            },
            5: {
                "N": 100,
                "max_queries": 8,
                "max_answers": 2,
                "rule_desc": "r is always equal to the smaller of b and N"
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
        
        self.N = cfg["N"]
        self.max_queries = cfg["max_queries"]
        self.max_answers = cfg["max_answers"]
        self.correct_rule_desc = cfg["rule_desc"]
        
        self.query_count = 0
        self.answer_count = 0
        
        self._game_info = {}

    def _compute_response(self, b):
        return min(b, self.N)

    def evaluate(self, parsed_info):
        self.answer_count += 1
        
        raw_ans = parsed_info["answer"]
        
        n_pattern = r'N\s*=\s*(\d+)'
        n_match = re.search(n_pattern, raw_ans, re.IGNORECASE)
        if not n_match:
            return False
        
        try:
            guessed_n = int(n_match.group(1))
        except:
            return False
        
        rule_pattern = r'rule\s*=\s*(.+?)(?:$|,\s*N\s*=)'
        rule_match = re.search(rule_pattern, raw_ans, re.IGNORECASE | re.DOTALL)
        if not rule_match:
            rule_pattern = r'rule\s*=\s*(.+)'
            rule_match = re.search(rule_pattern, raw_ans, re.IGNORECASE | re.DOTALL)
        
        if not rule_match:
            return False
        
        guessed_rule = rule_match.group(1).strip()
        
        if guessed_n != self.N:
            return False
        
        def normalize_rule(rule_text):
            rule_text = re.sub(r'\s+', ' ', rule_text.lower().strip())
            rule_text = re.sub(r'[.,;!?，。；！？]', '', rule_text)
            return rule_text
        
        normalized_guess = normalize_rule(guessed_rule)
        normalized_correct = normalize_rule(self.correct_rule_desc)
        
        if self.config.language == "zh":
            keywords = ["较小值", "最小值", "较小", "最小", "不超过", "小于", "最多", "上限", "如果", "若", "<", "≤", "min"]
            has_keyword = any(kw in normalized_guess for kw in keywords)
            has_b_and_n = "b" in normalized_guess and "n" in normalized_guess
        else:
            keywords = ["smaller", "minimum", "min", "lesser", "less", "lower", "cap", "limit", "if", "<", "≤"]
            has_keyword = any(kw in normalized_guess for kw in keywords)
            has_b_and_n = "b" in normalized_guess and "n" in normalized_guess
        
        return has_keyword and has_b_and_n

    def _cf_core_produce(self, parsed_info):
        if "query" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        try:
            b = int(parsed_info["query"].strip())
        except (ValueError, TypeError):
            if self.config.language == "zh":
                return "错误：查询值必须是正整数。"
            else:
                return "Error: Query value must be a positive integer."
        
        if b < 1 or b > 1000:
            if self.config.language == "zh":
                return "错误：查询值必须在 1 到 1000 之间。"
            else:
                return "Error: Query value must be between 1 and 1000."
        
        if self.query_count >= self.max_queries:
            if self.config.language == "zh":
                return f"查询次数已达上限（{self.max_queries}次），请直接提交答案。"
            else:
                return f"Query limit reached ({self.max_queries} queries). Please submit your answer."
        
        self.query_count += 1
        
        r = self._compute_response(b)
        
        return f"r = {r}"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        candidate_bs = sorted(set([
            1,
            max(1, self.N // 2),
            max(1, self.N - 1),
            self.N,
            min(1000, self.N + 1),
            min(1000, self.N * 2),
            500,
            1000,
        ]))
        
        for b in candidate_bs:
            r = self._compute_response(b)
            
            if self.config.language == "zh":
                ans = f"r = {r}"
            else:
                ans = f"r = {r}"
                
            results.append({
                "query": f"<query>{b}</query>",
                "answer": ans
            })
            
        return results

    def _cf_make_wrong(self, correct: str) -> str:
        m = re.search(r'r\s*=\s*(-?\d+)', correct)
        if m:
            val = int(m.group(1))
            wrong_val = val - 1 if val > 0 else val + 1
            return correct.replace(m.group(0), f"r = {wrong_val}")
        
        if correct.lstrip('-').isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否", 1)
            elif "否" in correct:
                return correct.replace("否", "是", 1)
        else:
            if re.search(r'\byes\b', correct, re.IGNORECASE):
                return re.sub(r'\byes\b', lambda m_obj: "No" if m_obj.group(0).istitle() else "NO" if m_obj.group(0).isupper() else "no", correct, count=1, flags=re.IGNORECASE)
            elif re.search(r'\bno\b', correct, re.IGNORECASE):
                return re.sub(r'\bno\b', lambda m_obj: "Yes" if m_obj.group(0).istitle() else "YES" if m_obj.group(0).isupper() else "yes", correct, count=1, flags=re.IGNORECASE)

        return correct + "_WRONG"

    def step(self, response: str):
        try:
            parsed_info = self.parse(response)
            
            if "answer" in parsed_info:
                if self.answer_count >= self.max_answers:
                    if self.config.language == "zh":
                        self.state.set_state("failed", f"答案提交次数已达上限（{self.max_answers}次）")
                        self.state.add_message("user", f"答案提交次数已达上限。游戏失败。")
                    else:
                        self.state.set_state("failed", f"Answer submission limit reached ({self.max_answers} attempts)")
                        self.state.add_message("user", f"Answer submission limit reached. Game failed.")
                else:
                    is_success = self.evaluate(parsed_info)
                    if is_success:
                        res = "答案正确！" if self.config.language == "zh" else "Correct answer!"
                        self.state.set_state("success", "success")
                        self.state.add_message("user", res)
                    else:
                        if self.answer_count >= self.max_answers:
                            res = "答案错误，已用尽所有提交机会。" if self.config.language == "zh" else "Incorrect answer. All submission attempts exhausted."
                            self.state.set_state("failed", "incorrect answer and no attempts left")
                            self.state.add_message("user", res)
                        else:
                            remaining = self.max_answers - self.answer_count
                            if self.config.language == "zh":
                                res = f"答案错误，还有 {remaining} 次提交机会。"
                            else:
                                res = f"Incorrect answer. {remaining} attempt(s) remaining."
                            self.state.add_message("user", res)
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))
            self.state.add_message("user", str(e))
        
        return self.state