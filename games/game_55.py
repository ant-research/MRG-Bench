from .base import Game
import random

class QuadraticSequenceMaxGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "序列"

    game_rule_zh = """\
我们来玩一个"二次序列最大值"推理游戏，规则如下：

游戏设定了一个长度为 {n} 的数字序列 S，每个位置 i（i 从 1 到 {n}）的值遵循一个固定但未知的二次函数规则：
S[i] = a·i² + b·i + c

其中 a, b, c 是整数系数，并且 a 不等于 0。该序列在所有位置中存在唯一的最大值。

你的目标是找出这个最大值所在的位置编号。你可以通过以下两种方式向我提问（每次只能问一个问题）：

1. 值查询：询问某个位置 i 的具体数值。我会告诉你 S[i] 的值。
2. 比较查询：询问两个位置 i 和 j 的大小关系。我会回答：
   - "i大于j" 表示 S[i] 大于 S[j]
   - "i小于j" 表示 S[i] 小于 S[j]
   - "相等" 表示 S[i] 等于 S[j]

请尽可能少地使用查询次数来找出答案。当你确定答案后，请提交最大值所在的位置编号。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 值查询（例如询问位置 5 的值）：
<query_value>5</query_value>

- 比较查询（例如比较位置 3 和 7）：
<query_compare>3,7</query_compare>

提交最终答案时，请给出最大值所在的位置编号，格式如下：
<answer>5</answer>
"""

    game_rule_en = """\
Let's play a "Quadratic Sequence Maximum" deduction game. Here are the rules:

A sequence S of length {n} has been set up. Each position i (i from 1 to {n}) follows a fixed but unknown quadratic function rule:
S[i] = a·i² + b·i + c

where a, b, c are integer coefficients, and a is not equal to 0. The sequence has a unique maximum value among all positions.

Your goal is to find the position index where this maximum value occurs. You can ask me questions in the following two ways (one question at a time):

1. Value Query: Ask for the specific value at position i. I will tell you the value of S[i].
2. Comparison Query: Ask about the relationship between positions i and j. I will answer:
   - "i greater than j" means S[i] is greater than S[j]
   - "i less than j" means S[i] is less than S[j]
   - "equal" means S[i] equals S[j]

Please use as few queries as possible to find the answer. When you are confident, submit the position index of the maximum value.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking for value at position 5):
<query_value>5</query_value>

- Comparison Query (e.g., comparing positions 3 and 7):
<query_compare>3,7</query_compare>

When submitting the final answer, provide the position index of the maximum value in this format:
<answer>5</answer>
"""

    contextualized_rule_zh_1 = """\
我们来进行一项"交通拥堵瓶颈"排查任务，规则如下：

在城市主干道上，设定了 {n} 个连续的智能红绿灯路口（编号从 1 到 {n}）。受车流分布和信号波的时空特性影响，每个路口 i 的"车流拥堵指数"遵循一个固定但未知的二次函数规律：
拥堵指数[i] = a·i² + b·i + c

其中 a, b, c 是整数系数，并且 a 不等于 0。该主干道上存在唯一的拥堵指数最高的路口（即车流瓶颈）。

你的目标是找出这个最高拥堵指数所在的路口编号。你可以通过以下两种方式向控制中心提问（每次只能问一个问题）：

1. 值查询：询问某个路口 i 的具体拥堵指数。我会告诉你该路口的指数值。
2. 比较查询：询问两个路口 i 和 j 的拥堵指数高低关系。我会回答：
   - "i大于j" 表示路口 i 的指数大于路口 j
   - "i小于j" 表示路口 i 的指数小于路口 j
   - "相等" 表示两路口指数相等

请尽可能少地使用查询次数来找出答案。当你确定答案后，请提交拥堵指数最高的路口编号。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 值查询（例如询问路口 5 的指数）：
<query_value>5</query_value>

- 比较查询（例如比较路口 3 和 7）：
<query_compare>3,7</query_compare>

提交最终答案时，请给出指数最高的路口编号，格式如下：
<answer>5</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's conduct a "Traffic Congestion Bottleneck" investigation task. Here are the rules:

On a main city road, there are {n} consecutive smart traffic light intersections (numbered 1 to {n}). Due to traffic flow distribution and signal wave spatiotemporal characteristics, the "traffic congestion index" at each intersection i follows a fixed but unknown quadratic function rule:
Congestion Index[i] = a·i² + b·i + c

where a, b, c are integer coefficients, and a is not equal to 0. There is a unique intersection with the highest congestion index (the traffic bottleneck) on this road.

Your goal is to find the intersection number where this maximum congestion index occurs. You can query the control center in the following two ways (one query at a time):

1. Value Query: Ask for the specific congestion index at intersection i. I will tell you the index value.
2. Comparison Query: Ask about the relationship between the congestion indices of intersections i and j. I will answer:
   - "i greater than j" means intersection i's index is greater than j's
   - "i less than j" means intersection i's index is less than j's
   - "equal" means the indices are equal

Please use as few queries as possible to find the answer. When you are confident, submit the intersection number with the highest congestion index.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking for the index at intersection 5):
<query_value>5</query_value>

- Comparison Query (e.g., comparing intersections 3 and 7):
<query_compare>3,7</query_compare>

When submitting the final answer, provide the intersection number with the highest congestion index in this format:
<answer>5</answer>
"""

    contextualized_rule_zh_2 = """\
我们来进行一项"最佳药物剂量"探索任务，规则如下：

在一种新型靶向药的临床试验中，设定了 {n} 个连续的剂量梯度（编号从 1 到 {n}）。患者的"有效缓解评分"与剂量梯度 i 之间遵循一个未知的二次函数药效动力学曲线：
缓解评分[i] = a·i² + b·i + c

其中 a, b, c 是整数系数，并且 a 不等于 0。试验中存在唯一的一个最佳剂量梯度，能使有效缓解评分达到峰值。

你的目标是找出有效缓解评分最高的那个剂量梯度编号。你可以通过以下两种方式向系统提问（每次只能问一个问题）：

1. 值查询：测试某个剂量梯度 i 的具体缓解评分。我会告诉你该评分值。
2. 比较查询：对比两个剂量梯度 i 和 j 的评分高低关系。我会回答：
   - "i大于j" 表示剂量梯度 i 的评分大于剂量梯度 j
   - "i小于j" 表示剂量梯度 i 的评分小于剂量梯度 j
   - "相等" 表示两梯度评分相等

请尽可能少地使用查询次数来找出答案。当你确定答案后，请提交有效缓解评分最高的剂量梯度编号。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 值查询（例如测试剂量梯度 5 的评分）：
<query_value>5</query_value>

- 比较查询（例如对比剂量梯度 3 和 7）：
<query_compare>3,7</query_compare>

提交最终答案时，请给出评分最高的剂量梯度编号，格式如下：
<answer>5</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct an "Optimal Drug Dosage" exploration task. Here are the rules:

In a clinical trial for a new targeted drug, {n} consecutive dosage gradients are set (numbered 1 to {n}). The patients' "effective relief score" at dosage gradient i follows an unknown quadratic pharmacodynamic curve:
Relief Score[i] = a·i² + b·i + c

where a, b, c are integer coefficients, and a is not equal to 0. There is a unique optimal dosage gradient that makes the effective relief score reach its peak.

Your goal is to find the dosage gradient number where this maximum relief score occurs. You can query the system in the following two ways (one query at a time):

1. Value Query: Ask for the specific relief score at dosage gradient i. I will tell you the score value.
2. Comparison Query: Ask about the relationship between the relief scores of gradients i and j. I will answer:
   - "i greater than j" means gradient i's score is greater than j's
   - "i less than j" means gradient i's score is less than j's
   - "equal" means the scores are equal

Please use as few queries as possible to find the answer. When you are confident, submit the dosage gradient number with the highest relief score.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking for the score at dosage gradient 5):
<query_value>5</query_value>

- Comparison Query (e.g., comparing dosage gradients 3 and 7):
<query_compare>3,7</query_compare>

When submitting the final answer, provide the dosage gradient number with the highest relief score in this format:
<answer>5</answer>
"""

    contextualized_rule_zh_3 = """\
我们来进行一项"自适应学习系统"评估任务，规则如下：

在一门核心课程中，系统划分了 {n} 个连续的难度层级（编号从 1 到 {n}）。根据认知负荷理论，学生的"知识吸收效率"与难度层级 i 之间呈现一个未知的二次函数关系：
吸收效率[i] = a·i² + b·i + c

其中 a, b, c 是整数系数，并且 a 不等于 0。存在唯一的一个难度层级，能使学生的吸收效率最大化。

你的目标是找出知识吸收效率达到最大值的那个难度层级编号。你可以通过以下两种方式向系统提问（每次只能问一个问题）：

1. 值查询：评估某个难度层级 i 的具体吸收效率。我会告诉你该效率值。
2. 比较查询：对比两个难度层级 i 和 j 的效率高低关系。我会回答：
   - "i大于j" 表示层级 i 的效率大于层级 j
   - "i小于j" 表示层级 i 的效率小于层级 j
   - "相等" 表示两层级效率相等

请尽可能少地使用查询次数来找出答案。当你确定答案后，请提交吸收效率最大的难度层级编号。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 值查询（例如评估难度层级 5 的效率）：
<query_value>5</query_value>

- 比较查询（例如对比难度层级 3 和 7）：
<query_compare>3,7</query_compare>

提交最终答案时，请给出吸收效率最大的难度层级编号，格式如下：
<answer>5</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct an "Adaptive Learning System" evaluation task. Here are the rules:

In a core course, the system has divided {n} consecutive difficulty levels (numbered 1 to {n}). According to cognitive load theory, the students' "knowledge absorption efficiency" at difficulty level i shows an unknown quadratic relationship:
Absorption Efficiency[i] = a·i² + b·i + c

where a, b, c are integer coefficients, and a is not equal to 0. There is a unique difficulty level that maximizes the students' absorption efficiency.

Your goal is to find the difficulty level number where this maximum absorption efficiency occurs. You can query the system in the following two ways (one query at a time):

1. Value Query: Ask for the specific absorption efficiency at difficulty level i. I will tell you the efficiency value.
2. Comparison Query: Ask about the relationship between the efficiencies of levels i and j. I will answer:
   - "i greater than j" means level i's efficiency is greater than j's
   - "i less than j" means level i's efficiency is less than j's
   - "equal" means the efficiencies are equal

Please use as few queries as possible to find the answer. When you are confident, submit the difficulty level number with the maximum absorption efficiency.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking for the efficiency at level 5):
<query_value>5</query_value>

- Comparison Query (e.g., comparing levels 3 and 7):
<query_compare>3,7</query_compare>

When submitting the final answer, provide the difficulty level number with the maximum absorption efficiency in this format:
<answer>5</answer>
"""

    contextualized_rule_zh_4 = """\
我们来进行一项"精密合金锻造工艺"优化任务，规则如下：

在热处理车间，退火温度被设定为 {n} 个连续的温度档位（编号从 1 到 {n}）。根据热力学规律，合金的"抗拉强度"与退火温度档位 i 之间遵循一个未知的二次函数演变关系：
抗拉强度[i] = a·i² + b·i + c

其中 a, b, c 是整数系数，并且 a 不等于 0。该工艺参数范围内存在唯一的一个最佳温度档位，能使合金的抗拉强度达到极值（最大值）。

你的目标是找出能使抗拉强度达到最大的温度档位编号。你可以通过以下两种方式向控制台提问（每次只能问一个问题）：

1. 值查询：检测某个温度档位 i 下合金的具体抗拉强度。我会告诉你该强度值。
2. 比较查询：对比两个温度档位 i 和 j 的抗拉强度大小关系。我会回答：
   - "i大于j" 表示档位 i 的强度大于档位 j
   - "i小于j" 表示档位 i 的强度小于档位 j
   - "相等" 表示两档位强度相等

请尽可能少地使用查询次数来找出答案。当你确定最佳工艺参数后，请提交抗拉强度最大的温度档位编号。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 值查询（例如检测温度档位 5 的抗拉强度）：
<query_value>5</query_value>

- 比较查询（例如对比温度档位 3 和 7）：
<query_compare>3,7</query_compare>

提交最终答案时，请给出抗拉强度最大的温度档位编号，格式如下：
<answer>5</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's conduct a "Precision Alloy Forging Process" optimization task. Here are the rules:

In the heat treatment workshop, the annealing temperature is set to {n} consecutive temperature gears (numbered 1 to {n}). According to thermodynamic principles, the alloy's "tensile strength" at temperature gear i follows an unknown quadratic evolution relationship:
Tensile Strength[i] = a·i² + b·i + c

where a, b, c are integer coefficients, and a is not equal to 0. Within this process parameter range, there is a unique optimal temperature gear that maximizes the alloy's tensile strength.

Your goal is to find the temperature gear number where this maximum tensile strength occurs. You can query the control console in the following two ways (one query at a time):

1. Value Query: Ask for the specific tensile strength at temperature gear i. I will tell you the strength value.
2. Comparison Query: Ask about the relationship between the tensile strengths at gears i and j. I will answer:
   - "i greater than j" means gear i's strength is greater than j's
   - "i less than j" means gear i's strength is less than j's
   - "equal" means the strengths are equal

Please use as few queries as possible to find the answer. When you are confident about the optimal process parameter, submit the temperature gear number with the maximum tensile strength.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking for the tensile strength at gear 5):
<query_value>5</query_value>

- Comparison Query (e.g., comparing gears 3 and 7):
<query_compare>3,7</query_compare>

When submitting the final answer, provide the temperature gear number with the maximum tensile strength in this format:
<answer>5</answer>
"""

    contextualized_rule_zh_5 = """\
我们来进行一项"隐匿资金链"追踪追溯任务，规则如下：

在一起复杂的经济纠纷案件中，司法鉴定机构对一笔连续变动的资金进行了追踪，划分了 {n} 个连续的追溯时间节点（编号从 1 到 {n}）。根据资金流向模型，每个时间节点 i 的"资金沉淀风险值"呈现出未知的二次函数演变规律：
风险值[i] = a·i² + b·i + c

其中 a, b, c 是整数系数，并且 a 不等于 0。在这些时间节点中，存在唯一的一个节点，其资金沉淀风险值最高，是案件突破的关键。

你的目标是找出资金沉淀风险值最高的那个时间节点编号。你可以通过以下两种方式向案件数据库提问（每次只能问一个问题）：

1. 值查询：调取某个时间节点 i 的具体风险值。我会告诉你该风险值。
2. 比较查询：比对两个时间节点 i 和 j 的风险值高低关系。我会回答：
   - "i大于j" 表示节点 i 的风险值大于节点 j
   - "i小于j" 表示节点 i 的风险值小于节点 j
   - "相等" 表示两节点风险值相等

请尽可能少地使用查询次数来找出答案。当你锁定案件突破口后，请提交风险值最高的时间节点编号。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 值查询（例如调取时间节点 5 的风险值）：
<query_value>5</query_value>

- 比较查询（例如比对时间节点 3 和 7）：
<query_compare>3,7</query_compare>

提交最终答案时，请给出风险值最高的时间节点编号，格式如下：
<answer>5</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct a "Hidden Capital Chain" tracking and tracing task. Here are the rules:

In a complex economic dispute case, forensic experts are tracking continuously changing funds and have divided the timeline into {n} consecutive tracing time nodes (numbered 1 to {n}). Based on the capital flow model, the "fund settlement risk value" at each time node i shows an unknown quadratic evolution pattern:
Risk Value[i] = a·i² + b·i + c

where a, b, c are integer coefficients, and a is not equal to 0. Among these time nodes, there is a unique node with the highest fund settlement risk value, which is the key breakthrough point of the case.

Your goal is to find the time node number where this maximum risk value occurs. You can query the case database in the following two ways (one query at a time):

1. Value Query: Ask for the specific risk value at time node i. I will tell you the risk value.
2. Comparison Query: Ask about the relationship between the risk values at nodes i and j. I will answer:
   - "i greater than j" means node i's risk value is greater than j's
   - "i less than j" means node i's risk value is less than j's
   - "equal" means the risk values are equal

Please use as few queries as possible to find the answer. When you have locked onto the breakthrough point, submit the time node number with the highest risk value.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking for the risk value at node 5):
<query_value>5</query_value>

- Comparison Query (e.g., comparing nodes 3 and 7):
<query_compare>3,7</query_compare>

When submitting the final answer, provide the time node number with the highest risk value in this format:
<answer>5</answer>
"""

    tags = ["answer", "query_value", "query_compare"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 12,
                "a": -2,
                "b": 24,
                "c": 10,
            },
            2: {
                "n": 15,
                "a": -3,
                "b": 30,
                "c": 20,
            },
            3: {
                "n": 20,
                "a": -1,
                "b": 20,
                "c": 100,
            },
            4: {
                "n": 25,
                "a": -1,
                "b": 40,
                "c": 50,
            },
            5: {
                "n": 30,
                "a": -2,
                "b": 60,
                "c": 500,
            },
        },
        "en": {
            1: {
                "n": 12,
                "a": -2,
                "b": 24,
                "c": 10,
            },
            2: {
                "n": 15,
                "a": -3,
                "b": 30,
                "c": 20,
            },
            3: {
                "n": 20,
                "a": -1,
                "b": 20,
                "c": 100,
            },
            4: {
                "n": 25,
                "a": -1,
                "b": 40,
                "c": 50,
            },
            5: {
                "n": 30,
                "a": -2,
                "b": 60,
                "c": 500,
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        
        self.a = cfg["a"]
        self.b = cfg["b"]
        self.c = cfg["c"]
        self.n = cfg["n"]

        if self.a >= 0:
            raise ValueError("Coefficient 'a' must be negative to ensure a unique maximum.")
        vertex = -self.b / (2 * self.a)
        if not (1 <= vertex <= self.n):
            raise ValueError(f"Vertex {vertex} is not within the sequence range [1, {self.n}].")
        
        self.sequence = {}
        for i in range(1, self.n + 1):
            self.sequence[i] = self.a * (i ** 2) + self.b * i + self.c
        
        max_value = max(self.sequence.values())
        self.max_position = None
        for i, val in self.sequence.items():
            if val == max_value:
                self.max_position = i
                break
        
        self.max_value = max_value

    def evaluate(self, parsed_info):
        try:
            submitted_pos = int(parsed_info["answer"].strip())
            return submitted_pos == self.max_position
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        self.query_count += 1
        
        if self.query_count > 5:
            if self.config.language == "zh":
                self.state.set_state("failed", "exceeded max queries")
                raise ValueError("已超过最大查询次数限制（5次）。")
            else:
                self.state.set_state("failed", "exceeded max queries")
                raise ValueError("Exceeded maximum query limit (5 queries).")
        
        if "query_value" in parsed_info:
            try:
                i = int(parsed_info["query_value"].strip())
                if i < 1 or i > self.n:
                    if self.config.language == "zh":
                        return f"错误：位置超出范围。有效范围是 1 到 {self.n}。"
                    else:
                        return f"Error: Position out of range. Valid range is 1 to {self.n}."
                return str(self.sequence[i])
            except ValueError:
                if self.config.language == "zh":
                    return "错误：无效的位置格式。"
                else:
                    return "Error: Invalid position format."
        
        elif "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                i, j = int(parts[0]), int(parts[1])
                
                if i < 1 or i > self.n or j < 1 or j > self.n:
                    if self.config.language == "zh":
                        return f"错误：位置超出范围。有效范围是 1 到 {self.n}。"
                    else:
                        return f"Error: Position out of range. Valid range is 1 to {self.n}."
                
                val_i = self.sequence[i]
                val_j = self.sequence[j]
                
                if self.config.language == "zh":
                    if val_i > val_j:
                        return "i大于j"
                    elif val_i < val_j:
                        return "i小于j"
                    else:
                        return "相等"
                else:
                    if val_i > val_j:
                        return "i greater than j"
                    elif val_i < val_j:
                        return "i less than j"
                    else:
                        return "equal"
            except:
                if self.config.language == "zh":
                    return "错误：无效的比较查询格式。请使用格式：<query_compare>i,j</query_compare>"
                else:
                    return "Error: Invalid comparison query format. Use format: <query_compare>i,j</query_compare>"
        
        else:
            if self.config.language == "zh":
                raise ValueError("未找到有效的查询标签。")
            else:
                raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        for i in range(1, self.n + 1):
            query_content = f"<query_value>{i}</query_value>"
            answer = str(self.sequence[i])
            results.append({
                "query": query_content,
                "answer": answer
            })

        for i in range(1, self.n + 1):
            for j in range(1, self.n + 1):
                query_content = f"<query_compare>{i},{j}</query_compare>"
                
                val_i = self.sequence[i]
                val_j = self.sequence[j]
                
                if self.config.language == "zh":
                    if val_i > val_j:
                        answer = "i大于j"
                    elif val_i < val_j:
                        answer = "i小于j"
                    else:
                        answer = "相等"
                else:
                    if val_i > val_j:
                        answer = "i greater than j"
                    elif val_i < val_j:
                        answer = "i less than j"
                    else:
                        answer = "equal"
                
                results.append({
                    "query": query_content,
                    "answer": answer
                })
                
        return results

    def _cf_make_wrong(self, correct: str) -> str:
        try:
            val = int(correct)
            return str(val + 1)
        except ValueError:
            pass

        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        else:
            correct_lower = correct.lower()
            if "yes" in correct_lower:
                return correct.replace("Yes", "No").replace("yes", "no").replace("YES", "NO")
            elif "no" in correct_lower:
                return correct.replace("No", "Yes").replace("no", "yes").replace("NO", "YES")
        
        return correct + "_WRONG"