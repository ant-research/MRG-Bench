import random
import math
import re
from .base import Game

class SymmetricFunctionGame(Game):

    game_rule_zh = """\
我们来玩一个"对称函数推理"游戏，规则如下：

游戏设定了一个标签集合 V = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}。我已秘密选择了一个对称函数 f，该函数接受两个不同的标签作为输入，返回一个非负整数。这个函数在整个游戏过程中保持不变。

你的目标是通过尽可能少的查询次数，推断出这个函数的规则，并能够正确预测未查询过的输入对的函数值。

你可以反复向我提出函数值查询（每次仅限一个问题）：

- 函数值查询：询问 f(a, b) 的值是多少，其中 a 和 b 是 V 中的不同元素。我会返回一个精确的整数值。

当你认为已经收集到足够信息后，请提交最终答案。答案需要包含对 {k} 个未查询过的输入对的函数值预测。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 函数值查询（例如查询 f(3, 7)）：
<query>3,7</query>

提交最终答案时，我会给出 {k} 个未查询过的输入对，你需要对每个输入对给出函数值预测。格式如下：

<answer>value1,value2,value3</answer>

其中 value1, value2, value3 等是你预测的函数值，按照我给出的输入对顺序依次列出，用逗号分隔。

- 查询的两个标签必须不同（a 不等于 b）
- 函数是对称的，即 f(a, b) = f(b, a)
- 验证阶段的输入对保证未被你直接查询过
"""

    game_rule_en = """\
Let's play a "Symmetric Function Inference" game. Here are the rules:

There is a label set V = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}. I have secretly chosen a symmetric function f that takes two different labels as input and returns a non-negative integer. This function remains constant throughout the game.

Your goal is to infer the function's rule through as few queries as possible, and correctly predict the function values for unqueried input pairs.

You can repeatedly ask me function value queries (one per turn):

- Function Value Query: Ask what the value of f(a, b) is, where a and b are different elements in V. I will return an exact integer value.

When you believe you have gathered enough information, submit your final answer. The answer must include predictions for {k} unqueried input pairs' function values.

Each query must contain only one tag. Use the following XML format:

- Function Value Query (e.g., querying f(3, 7)):
<query>3,7</query>

When submitting the final answer, I will provide {k} unqueried input pairs, and you need to predict the function value for each. The format is:

<answer>value1,value2,value3</answer>

where value1, value2, value3, etc. are your predicted function values, listed in the order of the input pairs I provide, separated by commas.

- The two labels in a query must be different (a not equal to b)
- The function is symmetric, meaning f(a, b) = f(b, a)
- Input pairs in the verification phase are guaranteed to be unqueried by you
"""

    contextualized_rule_zh_1 = """\
交通指挥中心正在进行"核心枢纽通行损耗评估"。

系统中设定了 10 个核心交通枢纽，编号为 V = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}。系统内置了一个秘密的对称评估模型 f，用于计算任意两个不同枢纽之间的通行损耗指数（返回值为非负整数）。该评估模型在整个路网分析过程中保持不变。

你的目标是通过尽可能少的探测次数，推断出这个通行损耗指数的计算规则，并能够正确预测未探测过的枢纽对的通行损耗。

你可以反复向我提出通行损耗探测（每次仅限一个探测）：

- 损耗指数探测：询问枢纽 a 和 b 之间的损耗指数 f(a, b) 是多少，其中 a 和 b 是 V 中的不同枢纽编号。我会返回一个精确的整数值。

当你认为已经收集到足够信息后，请提交最终分析报告。报告需要包含对 {k} 个未探测过的枢纽对的损耗指数预测。

每次探测只能包含一对枢纽编号。请使用以下 XML 格式：

- 损耗指数探测（例如探测枢纽 3 和 7 之间的损耗）：
<query>3,7</query>

提交最终报告时，我会给出 {k} 个未探测过的枢纽对，你需要对每个枢纽对给出损耗指数预测。格式如下：

<answer>value1,value2,value3</answer>

其中 value1, value2, value3 等是你预测的损耗指数值，按照我给出的枢纽对顺序依次列出，用逗号分隔。

- 探测的两个枢纽编号必须不同（a 不等于 b）
- 枢纽间的通行损耗是对称的，即 f(a, b) = f(b, a)
- 验证阶段的枢纽对保证未被你直接探测过
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The Traffic Command Center is conducting a "Core Hub Traffic Loss Assessment".

The system defines 10 core traffic hubs, labeled V = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}. The system has a built-in secret symmetric assessment model f, which calculates the traffic loss index (a non-negative integer) between any two different hubs. This assessment model remains constant throughout the entire network analysis process.

Your goal is to infer the calculation rule of this traffic loss index with as few probes as possible, and correctly predict the traffic loss for unprobed hub pairs.

You can repeatedly ask me for traffic loss probes (one probe per turn):

- Loss Index Probe: Ask what the loss index f(a, b) is between hub a and hub b, where a and b are different hub labels in V. I will return an exact integer value.

When you believe you have gathered enough information, please submit your final analysis report. The report must include predictions for {k} unprobed hub pairs' loss indices.

Each probe must contain only one pair of hub labels. Use the following XML format:

- Loss Index Probe (e.g., probing the loss between hub 3 and 7):
<query>3,7</query>

When submitting the final report, I will provide {k} unprobed hub pairs, and you need to predict the loss index for each pair. The format is:

<answer>value1,value2,value3</answer>

where value1, value2, value3, etc. are your predicted loss index values, listed in the order of the hub pairs I provide, separated by commas.

- The two hub labels in a probe must be different (a not equal to b)
- The traffic loss between hubs is symmetric, meaning f(a, b) = f(b, a)
- Hub pairs in the verification phase are guaranteed to be unprobed directly by you
"""

    contextualized_rule_zh_2 = """\
临床实验室正在进行"药物相互作用指数分析"。

系统中收录了 10 种基础化合物，编号为 V = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}。系统内隐藏了一个秘密的对称评估函数 f，用于计算任意两种不同化合物混合时的相互作用指数（返回值为非负整数）。该指数计算规则在整个实验过程中保持不变。

你的目标是通过尽可能少的临床测试次数，推断出这个相互作用指数的隐藏规律，并能够正确预测未测试过的化合物组合的相互作用指数。

你可以反复向我提出相互作用测试（每次仅限一组测试）：

- 相互作用测试：询问化合物 a 和 b 之间的相互作用指数 f(a, b) 是多少，其中 a 和 b 是 V 中的不同化合物编号。我会返回一个精确的整数值。

当你认为已经收集到足够信息后，请提交最终的临床预测报告。报告需要包含对 {k} 组未测试过的化合物组合的相互作用指数预测。

每次测试只能包含一对化合物编号。请使用以下 XML 格式：

- 相互作用测试（例如测试化合物 3 和 7）：
<query>3,7</query>

提交最终报告时，我会给出 {k} 组未测试过的化合物组合，你需要对每组组合给出相互作用指数预测。格式如下：

<answer>value1,value2,value3</answer>

其中 value1, value2, value3 等是你预测的相互作用指数，按照我给出的组合顺序依次列出，用逗号分隔。

- 测试的两个化合物编号必须不同（a 不等于 b）
- 化合物间的相互作用是对称的，即 f(a, b) = f(b, a)
- 验证阶段的化合物组合保证未被你直接测试过
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
The clinical laboratory is conducting a "Drug Interaction Index Analysis".

The system includes 10 basic compounds, labeled V = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}. A secret symmetric evaluation function f is hidden in the system, which calculates the interaction index (a non-negative integer) when any two different compounds are mixed. This index calculation rule remains constant throughout the experiment.

Your goal is to infer the hidden pattern of this interaction index with as few clinical tests as possible, and correctly predict the interaction indices for untested compound combinations.

You can repeatedly ask me for interaction tests (one test per turn):

- Interaction Test: Ask what the interaction index f(a, b) is between compound a and b, where a and b are different compound labels in V. I will return an exact integer value.

When you believe you have gathered enough information, please submit your final clinical prediction report. The report must include predictions for {k} untested compound combinations' interaction indices.

Each test must contain only one pair of compound labels. Use the following XML format:

- Interaction Test (e.g., testing compound 3 and 7):
<query>3,7</query>

When submitting the final report, I will provide {k} untested compound combinations, and you need to predict the interaction index for each. The format is:

<answer>value1,value2,value3</answer>

where value1, value2, value3, etc. are your predicted interaction indices, listed in the order of the combinations I provide, separated by commas.

- The two compound labels in a test must be different (a not equal to b)
- The interaction between compounds is symmetric, meaning f(a, b) = f(b, a)
- Compound combinations in the verification phase are guaranteed to be untested directly by you
"""

    contextualized_rule_zh_3 = """\
教育研究中心正在进行"学科模块关联度评估"。

知识图谱中设定了 10 个核心知识模块，编号为 V = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}。系统内置了一个秘密的对称评估机制 f，用于量化任意两个不同模块之间的知识关联度（返回值为非负整数）。该评估机制在整个分析过程中保持不变。

你的目标是通过尽可能少的查询次数，推断出这个知识关联度的计算规则，并能够正确预测未查询过的模块对的关联度。

你可以反复向我提出关联度查询（每次仅限一个查询）：

- 关联度查询：询问模块 a 和 b 之间的关联度 f(a, b) 是多少，其中 a 和 b 是 V 中的不同模块编号。我会返回一个精确的整数值。

当你认为已经收集到足够信息后，请提交最终的课程体系规划。规划需要包含对 {k} 个未查询过的模块对的关联度预测。

每次查询只能包含一对模块编号。请使用以下 XML 格式：

- 关联度查询（例如查询模块 3 和 7 的关联度）：
<query>3,7</query>

提交最终规划时，我会给出 {k} 个未查询过的模块对，你需要对每个模块对给出关联度预测。格式如下：

<answer>value1,value2,value3</answer>

其中 value1, value2, value3 等是你预测的关联度数值，按照我给出的模块对顺序依次列出，用逗号分隔。

- 查询的两个模块编号必须不同（a 不等于 b）
- 模块间的关联度是对称的，即 f(a, b) = f(b, a)
- 验证阶段的模块对保证未被你直接查询过
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The Education Research Center is conducting a "Subject Module Correlation Assessment".

The knowledge graph defines 10 core knowledge modules, labeled V = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}. The system has a built-in secret symmetric evaluation mechanism f to quantify the knowledge correlation (a non-negative integer) between any two different modules. This evaluation mechanism remains constant throughout the analysis.

Your goal is to infer the calculation rule of this knowledge correlation with as few queries as possible, and correctly predict the correlations for unqueried module pairs.

You can repeatedly ask me for correlation queries (one query per turn):

- Correlation Query: Ask what the correlation f(a, b) is between module a and b, where a and b are different module labels in V. I will return an exact integer value.

When you believe you have gathered enough information, please submit your final curriculum plan. The plan must include predictions for {k} unqueried module pairs' correlations.

Each query must contain only one pair of module labels. Use the following XML format:

- Correlation Query (e.g., querying modules 3 and 7):
<query>3,7</query>

When submitting the final plan, I will provide {k} unqueried module pairs, and you need to predict the correlation for each pair. The format is:

<answer>value1,value2,value3</answer>

where value1, value2, value3, etc. are your predicted correlation values, listed in the order of the module pairs I provide, separated by commas.

- The two module labels in a query must be different (a not equal to b)
- The correlation between modules is symmetric, meaning f(a, b) = f(b, a)
- Module pairs in the verification phase are guaranteed to be unqueried directly by you
"""

    contextualized_rule_zh_4 = """\
智能制造控制中心正在进行"工序兼容性系数测定"。

精密加工流水线中设定了 10 个装配工序节点，编号为 V = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}。系统内隐含了一个秘密的对称匹配函数 f，用于计算任意两个不同工序节点之间的兼容性系数（返回值为非负整数）。该匹配函数在整个系统调试过程中保持不变。

你的目标是通过尽可能少的系统测试次数，推断出这个兼容性系数的分布规则，并能够正确预测未测试过的工序对的兼容性系数。

你可以反复向我提出兼容性测试（每次仅限一组测试）：

- 兼容性测试：询问工序 a 和 b 之间的兼容性系数 f(a, b) 是多少，其中 a 和 b 是 V 中的不同工序编号。我会返回一个精确的整数值。

当你认为已经收集到足够信息后，请提交最终的工艺优化方案。方案需要包含对 {k} 个未测试过的工序对的兼容性系数预测。

每次测试只能包含一对工序编号。请使用以下 XML 格式：

- 兼容性测试（例如测试工序 3 和 7 的兼容性）：
<query>3,7</query>

提交最终方案时，我会给出 {k} 个未测试过的工序对，你需要对每个工序对给出兼容性系数预测。格式如下：

<answer>value1,value2,value3</answer>

其中 value1, value2, value3 等是你预测的兼容性系数，按照我给出的工序对顺序依次列出，用逗号分隔。

- 测试的两个工序编号必须不同（a 不等于 b）
- 工序间的兼容性是对称的，即 f(a, b) = f(b, a)
- 验证阶段的工序对保证未被你直接测试过
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
The Smart Manufacturing Control Center is conducting a "Process Compatibility Coefficient Determination".

The precision machining assembly line defines 10 assembly process nodes, labeled V = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}. A secret symmetric matching function f is implicit in the system, which calculates the compatibility coefficient (a non-negative integer) between any two different process nodes. This matching function remains constant throughout the system debugging.

Your goal is to infer the distribution rule of this compatibility coefficient with as few system tests as possible, and correctly predict the compatibility coefficients for untested process pairs.

You can repeatedly ask me for compatibility tests (one test per turn):

- Compatibility Test: Ask what the compatibility coefficient f(a, b) is between process a and b, where a and b are different process labels in V. I will return an exact integer value.

When you believe you have gathered enough information, please submit your final process optimization scheme. The scheme must include predictions for {k} untested process pairs' compatibility coefficients.

Each test must contain only one pair of process labels. Use the following XML format:

- Compatibility Test (e.g., testing processes 3 and 7):
<query>3,7</query>

When submitting the final scheme, I will provide {k} untested process pairs, and you need to predict the compatibility coefficient for each pair. The format is:

<answer>value1,value2,value3</answer>

where value1, value2, value3, etc. are your predicted compatibility coefficients, listed in the order of the process pairs I provide, separated by commas.

- The two process labels in a test must be different (a not equal to b)
- The compatibility between processes is symmetric, meaning f(a, b) = f(b, a)
- Process pairs in the verification phase are guaranteed to be untested directly by you
"""

    contextualized_rule_zh_5 = """\
司法AI辅助系统正在进行"法条竞合冲突指数分析"。

法律知识库中重点标注了 10 个法条类目，编号为 V = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}。系统内隐式定义了一个秘密的对称裁量模型 f，用于判定任意两个不同法条类目间的冲突指数（返回值为非负整数）。该裁量模型在整个案件审查过程中保持不变。

你的目标是通过尽可能少的检索查询次数，推断出这个冲突指数的判别规律，并能够正确预测未查询过的法条类目组合的冲突指数。

你可以反复向我提出冲突检索（每次仅限一次检索）：

- 冲突检索：询问法条类目 a 和 b 之间的冲突指数 f(a, b) 是多少，其中 a 和 b 是 V 中的不同法条编号。我会返回一个精确的整数值。

当你认为已经收集到足够信息后，请提交最终的法律适用意见书。意见书需要包含对 {k} 组未查询过的法条类目组合的冲突指数预测。

每次检索只能包含一对法条编号。请使用以下 XML 格式：

- 冲突检索（例如检索法条类目 3 和 7 之间的冲突）：
<query>3,7</query>

提交最终意见书时，我会给出 {k} 组未查询过的法条类目组合，你需要对每组组合给出冲突指数预测。格式如下：

<answer>value1,value2,value3</answer>

其中 value1, value2, value3 等是你预测的冲突指数值，按照我给出的法条组合顺序依次列出，用逗号分隔。

- 检索的两个法条编号必须不同（a 不等于 b）
- 法条间的冲突指数是对称的，即 f(a, b) = f(b, a)
- 验证阶段的法条组合保证未被你直接检索过
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
The Judicial AI Assistant System is conducting a "Legal Provision Concurrence Conflict Index Analysis".

The legal knowledge base highlights 10 categories of legal provisions, labeled V = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}. A secret symmetric discretion model f is implicitly defined in the system to determine the conflict index (a non-negative integer) between any two different provision categories. This discretion model remains constant throughout the case review process.

Your goal is to infer the discrimination pattern of this conflict index with as few retrieval queries as possible, and correctly predict the conflict indices for unqueried provision category combinations.

You can repeatedly ask me for conflict retrievals (one retrieval per turn):

- Conflict Retrieval: Ask what the conflict index f(a, b) is between provision category a and b, where a and b are different provision labels in V. I will return an exact integer value.

When you believe you have gathered enough information, please submit your final legal application opinion. The opinion must include predictions for {k} unqueried provision category combinations' conflict indices.

Each retrieval must contain only one pair of provision labels. Use the following XML format:

- Conflict Retrieval (e.g., retrieving the conflict between provisions 3 and 7):
<query>3,7</query>

When submitting the final opinion, I will provide {k} unqueried provision category combinations, and you need to predict the conflict index for each combination. The format is:

<answer>value1,value2,value3</answer>

where value1, value2, value3, etc. are your predicted conflict index values, listed in the order of the combinations I provide, separated by commas.

- The two provision labels in a retrieval must be different (a not equal to b)
- The conflict index between provisions is symmetric, meaning f(a, b) = f(b, a)
- Provision combinations in the verification phase are guaranteed to be unqueried directly by you
"""

    tags = ["answer", "query"]
    
    reasoning_type = "归纳推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        1: {
            "function_id": 4,
            "query_budget": 20,
            "verify_count": 3,
        },
        2: {
            "function_id": 1,
            "query_budget": 18,
            "verify_count": 4,
        },
        3: {
            "function_id": 5,
            "query_budget": 16,
            "verify_count": 4,
        },
        4: {
            "function_id": 3,
            "query_budget": 14,
            "verify_count": 5,
        },
        5: {
            "function_id": 6,
            "query_budget": 12,
            "verify_count": 5,
        },
    }

    def __init__(self, config):
        self.query_history = set()
        self.query_count = 0
        self.verification_pairs = []
        self.in_verification = False
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)
        
        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self.function_id = cfg["function_id"]
        self.query_budget = cfg["query_budget"]
        self.verify_count = cfg["verify_count"]
        
        self._game_info["k"] = self.verify_count
        
        self.functions = {
            1: lambda a, b: (a + b) % 10,
            2: lambda a, b: abs(a - b),
            3: lambda a, b: (a * b) % 10,
            4: lambda a, b: min(a, b),
            5: lambda a, b: max(a, b),
            6: lambda a, b: bin(a ^ b).count('1'),
            7: lambda a, b: math.gcd(a, b),
        }
        
        self.target_function = self.functions[self.function_id]
        
        self.all_pairs = [(a, b) for a in range(10) for b in range(a + 1, 10)]
        rng = random.Random(42)
        rng.shuffle(self.all_pairs)

    def _compute_function(self, a, b):
        return self.target_function(a, b)

    def _normalize_pair(self, a, b):
        return (min(a, b), max(a, b))

    def evaluate(self, parsed_info):
        if not self.verification_pairs:
            available_pairs = [p for p in self.all_pairs if p not in self.query_history]
            if len(available_pairs) < self.verify_count:
                available_pairs = list(self.all_pairs)
            self.verification_pairs = available_pairs[:self.verify_count]

        raw_ans = parsed_info.get("answer", "").strip()
        try:
            predicted_values = [int(x.strip()) for x in raw_ans.split(",")]
        except:
            return False

        if len(predicted_values) != self.verify_count:
            return False

        for i, (a, b) in enumerate(self.verification_pairs):
            expected = self._compute_function(a, b)
            if predicted_values[i] != expected:
                return False

        return True

    def _cf_core_produce(self, parsed_info):
        if "query" not in parsed_info:
            if self.config.language == "zh":
                return "错误：未找到有效的查询标签。"
            else:
                return "Error: No valid query tag found."
        
        if self.query_count >= self.query_budget:
            if self.config.language == "zh":
                return "错误：已达到查询次数上限。请提交最终答案。"
            else:
                return "Error: Query budget exhausted. Please submit your final answer."
        
        try:
            raw = parsed_info["query"].strip()
            parts = [x.strip() for x in raw.split(",")]
            
            if len(parts) != 2:
                raise ValueError("Query must contain exactly two values")
            
            a, b = int(parts[0]), int(parts[1])
            
            if a < 0 or a > 9 or b < 0 or b > 9:
                if self.config.language == "zh":
                    return "错误：标签必须在 0 到 9 之间。"
                else:
                    return "Error: Labels must be between 0 and 9."
            
            if a == b:
                if self.config.language == "zh":
                    return "错误：查询的两个标签必须不同。"
                else:
                    return "Error: The two labels in a query must be different."
            
            normalized_pair = self._normalize_pair(a, b)
            self.query_history.add(normalized_pair)
            self.query_count += 1
            
            result = self._compute_function(a, b)
            
            remaining = self.query_budget - self.query_count
            if self.config.language == "zh":
                return f"{result}（剩余查询次数：{remaining}）"
            else:
                return f"{result} (Remaining queries: {remaining})"
            
        except ValueError as e:
            if self.config.language == "zh":
                return "错误：查询格式无效。请使用格式 <query>a,b</query>，其中 a 和 b 是 0 到 9 之间的不同整数。"
            else:
                return "Error: Invalid query format. Use <query>a,b</query> where a and b are different integers between 0 and 9."
        except Exception as e:
            if self.config.language == "zh":
                return f"错误：{str(e)}"
            else:
                return f"Error: {str(e)}"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        simulated_count = 0
        for a in range(10):
            for b in range(a + 1, 10):
                query_str = f"<query>{a},{b}</query>"
                val = self._compute_function(a, b)
                simulated_count += 1
                remaining = self.query_budget - simulated_count
                if self.config.language == "zh":
                    answer_str = f"{val}（剩余查询次数：{remaining}）"
                else:
                    answer_str = f"{val} (Remaining queries: {remaining})"
                queries.append({
                    "query": query_str,
                    "answer": answer_str,
                })
        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        match = re.match(r'^(\d+)', correct.strip())
        if match:
            num = int(match.group(1))
            wrong_num = (num + random.randint(1, 9)) % 20
            if wrong_num == num:
                wrong_num = num + 1
            return correct.replace(match.group(1), str(wrong_num), 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        else:
            correct_lower = correct.lower()
            if "yes" in correct_lower:
                return correct.replace("Yes", "No").replace("YES", "NO").replace("yes", "no")
            elif "no" in correct_lower:
                return correct.replace("No", "Yes").replace("NO", "YES").replace("no", "yes")
        
        return correct + "_WRONG"

    def step(self, response: str):
        try:
            parsed_info = self.parse(response)
            
            if "answer" in parsed_info:
                if not self.verification_pairs:
                    available_pairs = [p for p in self.all_pairs if p not in self.query_history]
                    if len(available_pairs) < self.verify_count:
                        available_pairs = list(self.all_pairs)
                    self.verification_pairs = available_pairs[:self.verify_count]
                    
                    if self.config.language == "zh":
                        pair_strs = [f"f({a}, {b})" for a, b in self.verification_pairs]
                        prompt = (f"好的，现在进入验证阶段。请预测以下 {self.verify_count} 个输入对的函数值："
                                  + ", ".join(pair_strs)
                                  + "\n使用格式：<answer>value1,value2,...</answer>")
                    else:
                        pair_strs = [f"f({a}, {b})" for a, b in self.verification_pairs]
                        prompt = (f"OK, entering verification phase. Please predict the function values for the following {self.verify_count} input pairs: "
                                  + ", ".join(pair_strs)
                                  + "\nUse format: <answer>value1,value2,...</answer>")
                    
                    self.state.add_message("user", prompt)
                    return self.state
                
                is_success = self.evaluate(parsed_info)
                if is_success:
                    res = "所有预测正确！游戏成功。" if self.config.language == "zh" else "All predictions correct! Game success."
                    self.state.set_state("success", "success")
                    self.state.add_message("user", res)
                else:
                    res = "预测错误，游戏失败。" if self.config.language == "zh" else "Incorrect prediction. Game failed."
                    self.state.set_state("failed", "incorrect prediction")
                    self.state.add_message("user", res)
            else:
                game_response = self.produce_response(parsed_info)
                
                if self.query_count >= self.query_budget and not self.verification_pairs:
                    available_pairs = [p for p in self.all_pairs if p not in self.query_history]
                    if len(available_pairs) < self.verify_count:
                        available_pairs = list(self.all_pairs)
                    self.verification_pairs = available_pairs[:self.verify_count]
                    
                    if self.config.language == "zh":
                        pair_strs = [f"f({a}, {b})" for a, b in self.verification_pairs]
                        budget_prompt = (f"\n\n查询次数已用完。现在请预测以下 {self.verify_count} 个输入对的函数值："
                                         + ", ".join(pair_strs)
                                         + "\n使用格式：<answer>value1,value2,...</answer>")
                    else:
                        pair_strs = [f"f({a}, {b})" for a, b in self.verification_pairs]
                        budget_prompt = (f"\n\nQuery budget exhausted. Now predict the function values for the following {self.verify_count} input pairs: "
                                         + ", ".join(pair_strs)
                                         + "\nUse format: <answer>value1,value2,...</answer>")
                    
                    self.state.add_message("user", game_response + budget_prompt)
                else:
                    self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))
        
        return self.state