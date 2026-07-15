from .base import Game

class SequenceInferenceGame(Game):

    game_rule_zh = """\
我们现在来玩一个"序列推断"游戏，规则如下：

游戏设定了一个长度为 {n} 的有序整数序列 V = [v1, v2, ..., v{n}]，其中每个元素 vi 的取值范围是 0 到 9 的整数。序列的具体内容是隐藏的，你需要通过查询来推断。

系统定义了一个公开的统计量函数：
H(V) = 1·v1 + 2·v2 + 3·v3 + ... + {n}·v{n}

也就是说，H(V) 等于每个位置的索引乘以该位置的值，然后求和。

你可以进行以下操作：

1. **临时替换查询**：选择一个位置 i（1 到 {n}）和一个替换值 x（0 到 9），系统会告诉你如果将位置 i 的值临时替换为 x，统计量 H 会变化多少。注意：这只是临时计算，不会真正改变序列。

2. **提交答案**：当你认为已经推断出完整序列时，可以提交你的猜测。系统会告诉你是否完全正确{error_feedback}。

你的目标是用尽可能少的查询次数，准确推断出隐藏的序列。

每次查询时，使用以下 XML 格式：

- 临时替换查询（例如查询位置 3，替换值为 5）：
<query>3,5</query>

提交最终答案时，列出完整序列，用逗号分隔（例如序列为 [2,0,3,1,4]）：
<answer>2,0,3,1,4</answer>
"""

    game_rule_en = """\
Let's play a "Sequence Inference" game. Here are the rules:

The game has set up an ordered integer sequence V = [v1, v2, ..., v{n}] of length {n}, where each element vi is an integer ranging from 0 to 9. The specific content of the sequence is hidden, and you need to infer it through queries.

The system defines a public statistic function:
H(V) = 1·v1 + 2·v2 + 3·v3 + ... + {n}·v{n}

That is, H(V) equals the sum of each position's index multiplied by the value at that position.

You can perform the following operations:

1. **Temporary Replacement Query**: Select a position i (1 to {n}) and a replacement value x (0 to 9). The system will tell you how much the statistic H would change if the value at position i were temporarily replaced with x. Note: This is only a temporary calculation and does not actually change the sequence.

2. **Submit Answer**: When you believe you have inferred the complete sequence, you can submit your guess. The system will tell you whether it is completely correct{error_feedback}.

Your goal is to accurately infer the hidden sequence using as few queries as possible.

When querying, use the following XML format:

- Temporary Replacement Query (e.g., query position 3 with replacement value 5):
<query>3,5</query>

When submitting the final answer, list the complete sequence, comma-separated (e.g., sequence is [2,0,3,1,4]):
<answer>2,0,3,1,4</answer>
"""

    contextualized_rule_zh_1 = """\
交通信号流优化系统

我们现在来执行一项交通流推断任务，规则如下：

一条城市主干道上有 {n} 个连续的交通信号灯路口，编号 1 到 {n}。每个路口的红灯等待时间等级为 0 到 9 的整数。当前的各路口等级序列是隐藏的，你需要通过模拟测试来推断。

交通管理系统监控一个名为“加权拥堵指数 (H)”的指标。由于距离市中心越远，路口的流量堆积影响越大，因此权重等于路口编号：
H(V) = 1·v1 + 2·v2 + 3·v3 + ... + {n}·v{n}

也就是说，H(V) 等于每个路口的编号乘以该路口的红灯等级，然后求和。

你可以进行以下操作：

1. **模拟调整查询**：选择一个路口编号 i（1 到 {n}）和一个假设调整的红灯等级 x（0 到 9），系统会告诉你如果将路口 i 的红灯等级临时替换为 x，加权拥堵指数 H 会变化多少。注意：这只是模拟计算，不会真正改变路口的实际配置。

2. **提交答案**：当你认为已经推断出真实的等级序列时，可以提交你的结论。系统会告诉你是否完全正确{error_feedback}。

你的目标是用尽可能少的查询次数，准确推断出隐藏的红灯等级序列。

每次查询时，使用以下 XML 格式：

- 模拟调整查询（例如查询路口 3，替换等级为 5）：
<query>3,5</query>

提交最终答案时，列出完整序列，用逗号分隔（例如序列为 [2,0,3,1,4]）：
<answer>2,0,3,1,4</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Traffic Signal Flow Optimization System

Let's perform a traffic flow inference task. Here are the rules:

There are {n} consecutive traffic light intersections on a main city road, numbered 1 to {n}. Each intersection has a red light waiting time level, which is an integer ranging from 0 to 9. The current sequence of these levels is hidden, and you need to infer it through simulation tests.

The traffic management system monitors an indicator called the "Weighted Congestion Index (H)". Since the traffic accumulation effect is more significant further from the city center, the weight equals the intersection number:
H(V) = 1·v1 + 2·v2 + 3·v3 + ... + {n}·v{n}

That is, H(V) equals the sum of each intersection's number multiplied by its red light level.

You can perform the following operations:

1. **Temporary Replacement Query**: Select an intersection number i (1 to {n}) and a hypothetical red light level x (0 to 9). The system will tell you how much the Weighted Congestion Index H would change if the level at intersection i were temporarily replaced with x. Note: This is only a simulation calculation and does not change the actual configuration.

2. **Submit Answer**: When you believe you have inferred the true level sequence, you can submit your conclusion. The system will tell you whether it is completely correct{error_feedback}.

Your goal is to accurately infer the hidden red light level sequence using as few queries as possible.

When querying, use the following XML format:

- Temporary Replacement Query (e.g., query intersection 3 with replacement level 5):
<query>3,5</query>

When submitting the final answer, list the complete sequence, comma-separated (e.g., sequence is [2,0,3,1,4]):
<answer>2,0,3,1,4</answer>
"""

    contextualized_rule_zh_2 = """\
临床剂量综合评估系统

我们现在来执行一项临床药物推断任务，规则如下：

一名患者的靶向联合处方包含 {n} 种按顺序给药的药物，编号 1 到 {n}。每种药物的给药剂量等级为 0 到 9 的整数。当前的具体给药序列是隐藏的，你需要通过辅助分析来推断。

医疗系统采用一种名为“综合毒性负荷 (H)”的指标。由于药物在体内的累积效应增强，后给药物的毒性权重等同于其给药顺序编号：
H(V) = 1·v1 + 2·v2 + 3·v3 + ... + {n}·v{n}

也就是说，H(V) 等于每种药物的顺序编号乘以该药物的剂量等级，然后求和。

你可以进行以下操作：

1. **临时替换查询**：选择一个药物给药顺序 i（1 到 {n}）和一个假设的剂量等级 x（0 到 9），系统会告诉你如果将第 i 种药物的剂量等级临时替换为 x，综合毒性负荷 H 会变化多少。注意：这只是虚拟计算，不会真正修改患者的处方。

2. **提交答案**：当你认为已经推断出完整的给药剂量序列时，可以提交你的结论。系统会告诉你是否完全正确{error_feedback}。

你的目标是用尽可能少的查询次数，准确推断出隐藏的药物剂量序列。

每次查询时，使用以下 XML 格式：

- 临时替换查询（例如查询第 3 种药物，替换剂量为 5）：
<query>3,5</query>

提交最终答案时，列出完整序列，用逗号分隔（例如序列为 [2,0,3,1,4]）：
<answer>2,0,3,1,4</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Clinical Dose Comprehensive Evaluation System

Let's perform a clinical drug inference task. Here are the rules:

A patient's targeted combination prescription contains {n} sequentially administered drugs, numbered 1 to {n}. The dosage level of each drug is an integer ranging from 0 to 9. The current specific dosage sequence is hidden, and you need to infer it through auxiliary analysis.

The medical system uses an indicator called the "Comprehensive Toxicity Load (H)". Due to the enhanced cumulative effect of drugs in the body, the toxicity weight of subsequently administered drugs equals their administration order number:
H(V) = 1·v1 + 2·v2 + 3·v3 + ... + {n}·v{n}

That is, H(V) equals the sum of each drug's order number multiplied by its dosage level.

You can perform the following operations:

1. **Temporary Replacement Query**: Select a drug administration order i (1 to {n}) and a hypothetical dosage level x (0 to 9). The system will tell you how much the Comprehensive Toxicity Load H would change if the dosage level of the i-th drug were temporarily replaced with x. Note: This is only a virtual calculation and does not actually modify the patient's prescription.

2. **Submit Answer**: When you believe you have inferred the complete dosage sequence, you can submit your conclusion. The system will tell you whether it is completely correct{error_feedback}.

Your goal is to accurately infer the hidden drug dosage sequence using as few queries as possible.

When querying, use the following XML format:

- Temporary Replacement Query (e.g., query the 3rd drug with replacement dosage 5):
<query>3,5</query>

When submitting the final answer, list the complete sequence, comma-separated (e.g., sequence is [2,0,3,1,4]):
<answer>2,0,3,1,4</answer>
"""

    contextualized_rule_zh_3 = """\
课程认知负荷评估系统

我们现在来执行一项课程设计推断任务，规则如下：

一份标准化测试大纲包含 {n} 个难度递增的模块，编号 1 到 {n}。每个模块分配的考核知识点数量为 0 到 9 的整数。当前的知识点分配序列是隐藏的，你需要通过试算推演来推断。

系统计算该测试大纲的“综合认知负荷指数 (H)”指标。由于后置模块涉及的思维深度更高，其负荷权重等同于模块的编号：
H(V) = 1·v1 + 2·v2 + 3·v3 + ... + {n}·v{n}

也就是说，H(V) 等于每个模块的编号乘以该模块的知识点数量，然后求和。

你可以进行以下操作：

1. **临时替换查询**：选择一个模块编号 i（1 到 {n}）和一个假设的知识点数量 x（0 到 9），系统会告诉你如果将模块 i 的知识点数量临时替换为 x，综合认知负荷指数 H 会变化多少。注意：这只是试算推演，不会真正修改课程大纲。

2. **提交答案**：当你认为已经推断出完整的知识点分配序列时，可以提交你的结论。系统会告诉你是否完全正确{error_feedback}。

你的目标是用尽可能少的查询次数，准确推断出隐藏的知识点分配序列。

每次查询时，使用以下 XML 格式：

- 临时替换查询（例如查询模块 3，替换知识点数量为 5）：
<query>3,5</query>

提交最终答案时，列出完整序列，用逗号分隔（例如序列为 [2,0,3,1,4]）：
<answer>2,0,3,1,4</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Course Cognitive Load Assessment System

Let's perform a course design inference task. Here are the rules:

A standardized test syllabus contains {n} modules of increasing difficulty, numbered 1 to {n}. The number of assessed knowledge points allocated to each module is an integer ranging from 0 to 9. The current allocation sequence is hidden, and you need to infer it through trial calculations.

The system calculates the "Comprehensive Cognitive Load Index (H)" of the syllabus. Because later modules involve deeper thinking, their load weight equals the module's number:
H(V) = 1·v1 + 2·v2 + 3·v3 + ... + {n}·v{n}

That is, H(V) equals the sum of each module's number multiplied by its number of knowledge points.

You can perform the following operations:

1. **Temporary Replacement Query**: Select a module number i (1 to {n}) and a hypothetical number of knowledge points x (0 to 9). The system will tell you how much the Comprehensive Cognitive Load Index H would change if the knowledge point quantity of module i were temporarily replaced with x. Note: This is only a trial calculation and does not actually modify the course syllabus.

2. **Submit Answer**: When you believe you have inferred the complete allocation sequence, you can submit your conclusion. The system will tell you whether it is completely correct{error_feedback}.

Your goal is to accurately infer the hidden knowledge point allocation sequence using as few queries as possible.

When querying, use the following XML format:

- Temporary Replacement Query (e.g., query module 3 with replacement knowledge points 5):
<query>3,5</query>

When submitting the final answer, list the complete sequence, comma-separated (e.g., sequence is [2,0,3,1,4]):
<answer>2,0,3,1,4</answer>
"""

    contextualized_rule_zh_4 = """\
流水线热应力监控系统

我们现在来执行一项自动化流水线干预测试任务，规则如下：

一条自动化生产线上有 {n} 个按顺序排列的工位，编号 1 到 {n}。每个工位的设备能耗等级为 0 到 9 的整数。当前的各工位能耗配置是隐藏的，你需要通过系统接口来推断。

工厂监控系统记录了一个“累积热应力指数 (H)”。随着流水线向后推进，产品携带的基础温度增加，导致后置工位的热应力权重恰好等于其工位编号：
H(V) = 1·v1 + 2·v2 + 3·v3 + ... + {n}·v{n}

也就是说，H(V) 等于每个工位的编号乘以该工位的能耗等级，然后求和。

你可以进行以下操作：

1. **干预测试查询**：选择一个工位编号 i（1 到 {n}）和一个假设的能耗等级 x（0 到 9），系统会告诉你如果将工位 i 的能耗等级临时修改为 x，累积热应力指数 H 会变化多少。注意：这只是干预测试，不会真正改变实际的硬件配置。

2. **提交答案**：当你认为已经推断出完整的能耗等级序列时，可以提交你的结论。系统会告诉你是否完全正确{error_feedback}。

你的目标是用尽可能少的查询次数，准确推断出隐藏的能耗配置序列。

每次查询时，使用以下 XML 格式：

- 干预测试查询（例如查询工位 3，假设能耗等级为 5）：
<query>3,5</query>

提交最终答案时，列出完整序列，用逗号分隔（例如序列为 [2,0,3,1,4]）：
<answer>2,0,3,1,4</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Assembly Line Thermal Stress Monitoring System

Let's perform an automated assembly line intervention test task. Here are the rules:

An automated production line has {n} sequential workstations, numbered 1 to {n}. The equipment energy consumption level of each workstation is an integer ranging from 0 to 9. The current energy configuration sequence is hidden, and you need to infer it through the system interface.

The factory monitoring system records a "Cumulative Thermal Stress Index (H)". As the line progresses, the baseline temperature carried by the product increases, causing the thermal stress weight of subsequent workstations to exactly equal their workstation number:
H(V) = 1·v1 + 2·v2 + 3·v3 + ... + {n}·v{n}

That is, H(V) equals the sum of each workstation's number multiplied by its energy consumption level.

You can perform the following operations:

1. **Intervention Test Query**: Select a workstation number i (1 to {n}) and a hypothetical energy consumption level x (0 to 9). The system will tell you how much the Cumulative Thermal Stress Index H would change if the energy level of workstation i were temporarily replaced with x. Note: This is only an intervention test and does not actually change the hardware configuration.

2. **Submit Answer**: When you believe you have inferred the complete energy level sequence, you can submit your conclusion. The system will tell you whether it is completely correct{error_feedback}.

Your goal is to accurately infer the hidden energy configuration sequence using as few queries as possible.

When querying, use the following XML format:

- Intervention Test Query (e.g., query workstation 3 with hypothetical level 5):
<query>3,5</query>

When submitting the final answer, list the complete sequence, comma-separated (e.g., sequence is [2,0,3,1,4]):
<answer>2,0,3,1,4</answer>
"""

    contextualized_rule_zh_5 = """\
法庭证据合规审查系统

我们现在来执行一项证据链密级核查任务，规则如下：

在一起复杂的经济案件中，证据链由 {n} 份按时间顺序排列的关键文件组成，编号 1 到 {n}。每份文件的机密级别为 0 到 9 的整数。当前的各文件密级是封存隐藏的，你需要通过质询系统来推断。

审查系统设定了一个“综合保密合规得分 (H)”。由于较晚生成的文件通常包含前置文件的背景信息，其合规权重随时间递增，且等于文件编号：
H(V) = 1·v1 + 2·v2 + 3·v3 + ... + {n}·v{n}

也就是说，H(V) 等于每份文件的编号乘以该文件的机密级别，然后求和。

你可以进行以下操作：

1. **假设性质询查询**：选择一个文件编号 i（1 到 {n}）和一个假设的机密级别 x（0 到 9），系统会告诉你如果将文件 i 的机密级别临时修改为 x，综合保密合规得分 H 会变化多少。注意：这只是假设性审查，不会真正解密或篡改法庭档案。

2. **提交答案**：当你认为已经查明完整的机密级别序列时，可以提交你的结论。系统会告诉你证据密级是否核实完全正确{error_feedback}。

你的目标是用尽可能少的查询次数，准确推断出隐藏的机密级别序列。

每次查询时，使用以下 XML 格式：

- 假设性质询查询（例如质询文件 3，假设机密级别为 5）：
<query>3,5</query>

提交最终答案时，列出完整序列，用逗号分隔（例如序列为 [2,0,3,1,4]）：
<answer>2,0,3,1,4</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Court Evidence Compliance Review System

Let's perform an evidence chain clearance verification task. Here are the rules:

In a complex economic case, the evidence chain consists of {n} key documents arranged in chronological order, numbered 1 to {n}. The confidentiality level of each document is an integer ranging from 0 to 9. The current sequence of clearance levels is sealed and hidden, and you need to infer it through the inquiry system.

The review system has established a "Comprehensive Confidentiality Compliance Score (H)". Since later documents usually contain background information from earlier ones, their compliance weight increases over time and equals the document number:
H(V) = 1·v1 + 2·v2 + 3·v3 + ... + {n}·v{n}

That is, H(V) equals the sum of each document's number multiplied by its confidentiality level.

You can perform the following operations:

1. **Hypothetical Inquiry Query**: Select a document number i (1 to {n}) and a hypothetical confidentiality level x (0 to 9). The system will tell you how much the Comprehensive Confidentiality Compliance Score H would change if the confidentiality level of document i were temporarily replaced with x. Note: This is only a hypothetical review and does not actually decrypt or alter court records.

2. **Submit Answer**: When you believe you have verified the complete clearance sequence, you can submit your conclusion. The system will tell you whether the evidence levels are verified completely correct{error_feedback}.

Your goal is to accurately infer the hidden confidentiality level sequence using as few queries as possible.

When querying, use the following XML format:

- Hypothetical Inquiry Query (e.g., query document 3 with replacement level 5):
<query>3,5</query>

When submitting the final answer, list the complete sequence, comma-separated (e.g., sequence is [2,0,3,1,4]):
<answer>2,0,3,1,4</answer>
"""

    user_prompt_zh = "你可以开始查询或提交答案了。"
    user_prompt_en = "You can start querying or submit your answer now."

    tags = ["answer", "query"]
    
    reasoning_type = "演绎推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 3,
                "sequence": [2, 0, 5],
                "max_submit_attempts": None,
                "error_feedback": False,
            },
            2: {
                "n": 5,
                "sequence": [1, 4, 0, 3, 2],
                "max_submit_attempts": None,
                "error_feedback": False,
            },
            3: {
                "n": 7,
                "sequence": [3, 1, 4, 1, 5, 9, 2],
                "max_submit_attempts": None,
                "error_feedback": False,
            },
            4: {
                "n": 8,
                "sequence": [2, 7, 1, 8, 2, 8, 1, 8],
                "max_submit_attempts": 3,
                "error_feedback": True,
            },
            5: {
                "n": 10,
                "sequence": [3, 1, 4, 1, 5, 9, 2, 6, 5, 3],
                "max_submit_attempts": 3,
                "error_feedback": True,
            },
        },
        "en": {
            1: {
                "n": 3,
                "sequence": [2, 0, 5],
                "max_submit_attempts": None,
                "error_feedback": False,
            },
            2: {
                "n": 5,
                "sequence": [1, 4, 0, 3, 2],
                "max_submit_attempts": None,
                "error_feedback": False,
            },
            3: {
                "n": 7,
                "sequence": [3, 1, 4, 1, 5, 9, 2],
                "max_submit_attempts": None,
                "error_feedback": False,
            },
            4: {
                "n": 8,
                "sequence": [2, 7, 1, 8, 2, 8, 1, 8],
                "max_submit_attempts": 3,
                "error_feedback": True,
            },
            5: {
                "n": 10,
                "sequence": [3, 1, 4, 1, 5, 9, 2, 6, 5, 3],
                "max_submit_attempts": 3,
                "error_feedback": True,
            },
        },
    }

    def __init__(self, config):
        self.submit_count = 0
        super().__init__(config)

    def _initialize_game(self):
        import random as _random

        lang = self.config.language
        diff = int(self.config.difficulty)

        DIFFICULTY_N = {1: 3, 2: 5, 3: 7, 4: 8, 5: 10}
        DIFFICULTY_ERROR_FEEDBACK = {1: False, 2: False, 3: False, 4: True, 5: True}
        DIFFICULTY_MAX_SUBMIT = {1: None, 2: None, 3: None, 4: 3, 5: 3}

        if diff not in DIFFICULTY_N:
            raise KeyError(f"Unsupported difficulty: {diff}")

        n = DIFFICULTY_N[diff]
        rng = _random.Random(f"seq_inference_{lang}_{diff}_v1")
        sequence = [rng.randint(0, 9) for _ in range(n)]

        self._game_info["n"] = n
        self.sequence = sequence
        self.max_submit_attempts = DIFFICULTY_MAX_SUBMIT[diff]
        self.error_feedback = DIFFICULTY_ERROR_FEEDBACK[diff]

        if self.error_feedback:
            if lang == "zh":
                self._game_info["error_feedback"] = "。如果错误，系统会告诉你有多少个位置的值猜错了"
            else:
                self._game_info["error_feedback"] = ". If incorrect, the system will tell you how many positions have wrong values"
        else:
            self._game_info["error_feedback"] = ""

        self.original_h = sum((i + 1) * v for i, v in enumerate(self.sequence))

    def evaluate(self, parsed_info):
        self.submit_count += 1
        
        raw_ans = parsed_info["answer"].strip()
        try:
            submitted_seq = [int(x.strip()) for x in raw_ans.split(",")]
        except Exception:
            return False
        
        if len(submitted_seq) != len(self.sequence):
            return False
        
        if not all(0 <= x <= 9 for x in submitted_seq):
            return False
        
        is_correct = submitted_seq == self.sequence
        
        if not is_correct and self.error_feedback:
            wrong_count = sum(1 for i in range(len(self.sequence)) 
                            if submitted_seq[i] != self.sequence[i])
            
            if self.config.language == "zh":
                self._last_feedback = f"答案错误。有 {wrong_count} 个位置的值不正确。"
            else:
                self._last_feedback = f"Incorrect answer. {wrong_count} position(s) have wrong values."
        else:
            self._last_feedback = None
        
        return is_correct

    def get_all_possible_queries(self):
        queries = []
        n = len(self.sequence)
        
        for i in range(1, n + 1):
            for x in range(10):
                query_str = f"<query>{i},{x}</query>"
                
                original_value = self.sequence[i - 1]
                delta_h = (x - original_value) * i
                
                if self.config.language == "zh":
                    answer_str = f"统计量变化：{delta_h:+d}"
                else:
                    answer_str = f"Statistic change: {delta_h:+d}"
                
                queries.append({
                    "query": query_str,
                    "answer": answer_str
                })
        
        return queries

    def _cf_core_produce(self, parsed_info):
        if "query" in parsed_info:
            raw_query = parsed_info["query"].strip()
            try:
                parts = [x.strip() for x in raw_query.split(",")]
                if len(parts) != 2:
                    raise ValueError("Invalid query format")
                
                position = int(parts[0])
                replacement = int(parts[1])
                
                if position < 1 or position > len(self.sequence):
                    if self.config.language == "zh":
                        return f"错误：位置必须在 1 到 {len(self.sequence)} 之间。"
                    else:
                        return f"Error: Position must be between 1 and {len(self.sequence)}."
                
                if replacement < 0 or replacement > 9:
                    if self.config.language == "zh":
                        return "错误：替换值必须在 0 到 9 之间。"
                    else:
                        return "Error: Replacement value must be between 0 and 9."
                
                original_value = self.sequence[position - 1]
                delta_h = (replacement - original_value) * position
                
                if self.config.language == "zh":
                    return f"统计量变化：{delta_h:+d}"
                else:
                    return f"Statistic change: {delta_h:+d}"
                
            except ValueError:
                if self.config.language == "zh":
                    return "错误：查询格式无效。应为：<query>位置,替换值</query>"
                else:
                    return "Error: Invalid query format. Should be: <query>position,replacement_value</query>"
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        import re as _re
        match = _re.search(r'[+\-]?\d+', correct)
        if match:
            val = int(match.group())
            wrong_val = val + 3 if val <= 5 else val - 3
            wrong_str = f"{wrong_val:+d}" if ('+' in match.group() or '-' in match.group()) else str(wrong_val)
            return correct[:match.start()] + wrong_str + correct[match.end():]
        
        return correct + "_WRONG"

    def step(self, response: str):
        try:
            parsed_info = self.parse(response)
            
            if "answer" in parsed_info:
                is_success = self.evaluate(parsed_info)
                
                if is_success:
                    res = "答案正确！" if self.config.language == "zh" else "Correct answer!"
                    self.state.set_state("success", "success")
                    self.state.add_message("user", res)
                else:
                    if self.max_submit_attempts is None:
                        has_attempts_left = True
                    else:
                        has_attempts_left = self.submit_count < self.max_submit_attempts

                    if has_attempts_left:
                        if self.error_feedback and getattr(self, '_last_feedback', None):
                            res = self._last_feedback
                        else:
                            res = "答案错误，请继续尝试。" if self.config.language == "zh" else "Incorrect answer. Please try again."
                        
                        if self.max_submit_attempts is not None:
                            if self.config.language == "zh":
                                res += f" 你还有 {self.max_submit_attempts - self.submit_count} 次提交机会。"
                            else:
                                res += f" You have {self.max_submit_attempts - self.submit_count} submission attempt(s) remaining."
                        
                        self.state.add_message("user", res)
                    else:
                        if getattr(self, '_last_feedback', None):
                            res = self._last_feedback
                        else:
                            res = "答案错误。" if self.config.language == "zh" else "Incorrect answer."

                        if self.max_submit_attempts is not None:
                            if self.config.language == "zh":
                                res += f" 你已用完 {self.max_submit_attempts} 次提交机会。"
                            else:
                                res += f" You have used all {self.max_submit_attempts} submission attempts."

                        self.state.set_state("failed", "incorrect answer")
                        self.state.add_message("user", res)
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))
        
        return self.state