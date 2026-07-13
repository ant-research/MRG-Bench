from .base import Game
import re


class HiddenSequenceSumGame(Game):

    game_rule_zh = """\
我们来玩一个"隐含序列求和"的推理游戏，规则如下：

游戏设定了一个长度为 {n} 的有序二元序列，序列中每个位置的值只能是 0 或 1。你的目标是推断出这个序列中所有 1 的总数。

你可以进行以下两类操作：

1. 区间和查询：选择一个起点位置 l（整数），我会返回从位置 l 开始、连续 {k} 个元素的和。注意：
   - 起点 l 的有效范围是 1 到 {max_start}（即 {n} - {k} + 1）
   - 如果起点超出有效范围，将返回错误提示，但该次查询仍会计入查询次数
   - 返回值是一个 0 到 {k} 之间的整数

2. 最终申报：当你认为已经收集到足够信息后，可以提交你对序列中 1 的总数的答案。

约束条件：
- 你的总查询次数（包括有效和无效查询）不能超过 {max_queries} 次
- 在进行最终申报前，你必须至少完成 2 次有效的区间和查询
- 如果申报答案错误、查询超过限制次数、或在查询次数不足时提前申报，游戏将失败

## 询问与提交答案的格式（必须严格遵守）

每次只能进行一个操作。请使用以下 XML 格式：

- 区间和查询（例如查询起点为 5 的区间）：
<query_range>5</query_range>

- 提交最终答案（例如认为总和是 8）：
<answer>8</answer>

请合理规划你的查询策略，用尽可能少的次数找到正确答案。
"""

    game_rule_en = """\
Let's play a "Hidden Sequence Sum" deduction game. Here are the rules:

There is an ordered binary sequence of length {n}, where each position contains either 0 or 1. Your goal is to infer the total count of 1s in this sequence.

You can perform two types of operations:

1. Range Sum Query: Choose a starting position l (integer), and I will return the sum of {k} consecutive elements starting from position l. Note:
   - The valid range for starting position l is 1 to {max_start} (i.e., {n} - {k} + 1)
   - If the starting position is out of range, an error message will be returned, but it still counts toward your query limit
   - The return value is an integer between 0 and {k}

2. Final Answer Submission: When you believe you have gathered enough information, submit your answer for the total count of 1s in the sequence.

Constraints:
- Your total number of queries (including valid and invalid ones) cannot exceed {max_queries}
- Before submitting your final answer, you must complete at least 2 valid range sum queries
- The game fails if your answer is incorrect, you exceed the query limit, or you submit prematurely with insufficient queries

## Query and Answer Format (strictly required)

You can only perform one operation at a time. Use the following XML format:

- Range Sum Query (e.g., querying range starting at position 5):
<query_range>5</query_range>

- Submit Final Answer (e.g., if you believe the total is 8):
<answer>8</answer>

Plan your query strategy wisely to find the correct answer with as few queries as possible.
"""

    # 场景 1：交通
    contextualized_rule_zh_1 = """\
我们来执行一项"交通拥堵态势排查"任务，规则如下：

一条主干道被划分为 {n} 个连续的监测路段，每个路段的状态仅为拥堵（1）或畅通（0）。你的目标是推断出这条道路上拥堵路段的总数。

你可以进行以下两类操作：

1. 无人机区间巡查：选择一个起始路段编号 l（整数），我会返回从路段 l 开始、连续 {k} 个路段中的拥堵路段数量。注意：
   - 起始编号 l 的有效范围是 1 到 {max_start}（即 {n} - {k} + 1）
   - 如果起始编号超出有效范围，无人机将返回错误提示，但该次指令仍会计入调度次数
   - 返回值是一个 0 到 {k} 之间的整数

2. 最终态势研判：当你认为已经收集到足够信息后，可以提交你对整条道路拥堵路段总数的最终报告。

约束条件：
- 你的总调度次数（包括有效和无效巡查）不能超过 {max_queries} 次
- 在进行最终研判前，你必须至少完成 2 次有效的无人机区间巡查
- 如果研判报告错误、调度超过限制次数、或在巡查次数不足时提前研判，任务将失败

## 询问与提交答案的格式（必须严格遵守）

每次只能进行一个操作。请使用以下 XML 格式：

- 无人机区间巡查（例如从第 5 路段开始巡查）：
<query_range>5</query_range>

- 提交最终态势研判（例如认为拥堵路段总数是 8）：
<answer>8</answer>

请合理规划你的巡查策略，用尽可能少的调度次数准确完成态势排查。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's execute a "Traffic Congestion Profiling" task. Here are the rules:

A main highway is divided into {n} consecutive monitoring segments. Each segment is either congested (1) or clear (0). Your goal is to infer the total number of congested segments on this road.

You can perform two types of operations:

1. Drone Range Inspection: Choose a starting segment number l (integer), and I will return the number of congested segments in {k} consecutive segments starting from segment l. Note:
   - The valid range for starting segment l is 1 to {max_start} (i.e., {n} - {k} + 1)
   - If the starting segment is out of range, the drone will return an error message, but it still counts toward your dispatch limit
   - The return value is an integer between 0 and {k}

2. Final Situation Assessment: When you believe you have gathered enough information, submit your final report for the total number of congested segments.

Constraints:
- Your total number of dispatches (including valid and invalid inspections) cannot exceed {max_queries}
- Before submitting your final assessment, you must complete at least 2 valid drone range inspections
- The task fails if your assessment is incorrect, you exceed the dispatch limit, or you submit prematurely with insufficient inspections

## Query and Answer Format (strictly required)

You can only perform one operation at a time. Use the following XML format:

- Drone Range Inspection (e.g., inspecting range starting at segment 5):
<query_range>5</query_range>

- Submit Final Assessment (e.g., if you believe the total congested segments is 8):
<answer>8</answer>

Plan your inspection strategy wisely to complete the profiling accurately with as few dispatches as possible.
"""

    # 场景 2：医疗
    contextualized_rule_zh_2 = """\
我们来执行一项"基因突变靶点筛查"任务，规则如下：

患者的一段关键靶基因序列包含了 {n} 个连续的检测位点，每个位点的状态仅为突变（1）或正常（0）。你的目标是推断出该序列中突变位点的总数。

你可以进行以下两类操作：

1. 靶向区间测序：选择一个起始位点编号 l（整数），我会返回从位点 l 开始、连续 {k} 个位点中的突变数量。注意：
   - 起始编号 l 的有效范围是 1 到 {max_start}（即 {n} - {k} + 1）
   - 如果起始编号超出有效范围，检测设备将报错，但该次操作仍会计入试剂消耗次数
   - 返回值是一个 0 到 {k} 之间的整数

2. 最终临床报告：当你认为已经收集到足够的测序信息后，可以提交你对序列中突变位点总数的最终结论。

约束条件：
- 你的总测序次数（包括有效和无效测序）不能超过 {max_queries} 次
- 在出具最终临床报告前，你必须至少完成 2 次有效的靶向区间测序
- 如果报告结论错误、测序超过限制次数、或在测序次数不足时提前出具报告，筛查任务将失败

## 询问与提交答案的格式（必须严格遵守）

每次只能进行一个操作。请使用以下 XML 格式：

- 靶向区间测序（例如从第 5 位点开始测序）：
<query_range>5</query_range>

- 提交最终临床报告（例如认为突变位点总数是 8）：
<answer>8</answer>

请合理规划你的测序策略，用尽可能少的试剂消耗准确找到临床答案。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's perform a "Genetic Mutation Loci Screening" task. Here are the rules:

A patient's critical target gene sequence contains {n} consecutive testing loci, where each locus is either mutated (1) or normal (0). Your goal is to infer the total number of mutated loci in this sequence.

You can perform two types of operations:

1. Targeted Range Sequencing: Choose a starting locus number l (integer), and I will return the count of mutated loci within {k} consecutive loci starting from locus l. Note:
   - The valid range for starting locus l is 1 to {max_start} (i.e., {n} - {k} + 1)
   - If the starting locus is out of range, the testing equipment will return an error, but it still counts toward your reagent consumption limit
   - The return value is an integer between 0 and {k}

2. Final Clinical Report: When you believe you have gathered enough sequencing information, submit your final conclusion for the total number of mutated loci in the sequence.

Constraints:
- Your total number of sequencing tests (including valid and invalid ones) cannot exceed {max_queries}
- Before issuing your final clinical report, you must complete at least 2 valid targeted range sequencing tests
- The task fails if your conclusion is incorrect, you exceed the testing limit, or you issue the report prematurely with insufficient testing

## Query and Answer Format (strictly required)

You can only perform one operation at a time. Use the following XML format:

- Targeted Range Sequencing (e.g., sequencing range starting at locus 5):
<query_range>5</query_range>

- Submit Final Clinical Report (e.g., if you believe the total mutated loci is 8):
<answer>8</answer>

Plan your sequencing strategy wisely to accurately reach a clinical conclusion with minimal reagent consumption.
"""

    # 场景 3：教育
    contextualized_rule_zh_3 = """\
我们来执行一项"知识盲区精准诊断"任务，规则如下：

某学科的核心课程被划分为 {n} 个连续的知识模块，学生对每个模块的掌握状态仅为存在盲区（1）或已掌握（0）。你的目标是推断出该学生存在盲区的知识模块总数。

你可以进行以下两类操作：

1. 区间形成性测试：选择一个起始模块编号 l（整数），我会返回从模块 l 开始、连续 {k} 个模块中存在盲区的数量。注意：
   - 起始编号 l 的有效范围是 1 到 {max_start}（即 {n} - {k} + 1）
   - 如果起始编号超出有效范围，系统将返回错误提示，但该次测试仍会计入测试次数
   - 返回值是一个 0 到 {k} 之间的整数

2. 最终学情评估：当你认为已经收集到足够的数据后，可以提交你对该生知识盲区总数的最终评估。

约束条件：
- 你的总测试次数（包括有效和无效测试）不能超过 {max_queries} 次
- 在进行最终学情评估前，你必须至少完成 2 次有效的区间形成性测试
- 如果评估结果错误、测试超过限制次数、或在测试次数不足时提前评估，诊断任务将失败

## 询问与提交答案的格式（必须严格遵守）

每次只能进行一个操作。请使用以下 XML 格式：

- 区间形成性测试（例如从第 5 模块开始测试）：
<query_range>5</query_range>

- 提交最终学情评估（例如认为知识盲区总数是 8）：
<answer>8</answer>

请合理规划你的测试策略，用尽可能少的测试次数准确完成学情诊断，以减轻学生负担。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a "Knowledge Gap Precision Diagnosis" task. Here are the rules:

A core curriculum is divided into {n} consecutive knowledge modules. The student's mastery status for each module is either unmastered (1) or mastered (0). Your goal is to infer the total number of unmastered knowledge modules for this student.

You can perform two types of operations:

1. Range Formative Assessment: Choose a starting module number l (integer), and I will return the number of unmastered modules within {k} consecutive modules starting from module l. Note:
   - The valid range for starting module l is 1 to {max_start} (i.e., {n} - {k} + 1)
   - If the starting module is out of range, the system will return an error prompt, but it still counts toward your assessment limit
   - The return value is an integer between 0 and {k}

2. Final Academic Evaluation: When you believe you have gathered enough data, submit your final evaluation of the total number of unmastered modules.

Constraints:
- Your total number of assessments (including valid and invalid ones) cannot exceed {max_queries}
- Before submitting your final academic evaluation, you must complete at least 2 valid range formative assessments
- The task fails if your evaluation is incorrect, you exceed the assessment limit, or you evaluate prematurely with insufficient assessments

## Query and Answer Format (strictly required)

You can only perform one operation at a time. Use the following XML format:

- Range Formative Assessment (e.g., assessing range starting at module 5):
<query_range>5</query_range>

- Submit Final Academic Evaluation (e.g., if you believe the total unmastered modules is 8):
<answer>8</answer>

Plan your assessment strategy wisely to accurately diagnose the academic status with as few assessments as possible to reduce the student's burden.
"""

    # 场景 4：制造业/工业
    contextualized_rule_zh_4 = """\
我们来执行一项"流水线产品质量抽检"任务，规则如下：

生产线上有一批包含 {n} 个连续工件的流水线批次，每个工件的质量状态仅为次品（1）或合格（0）。你的目标是推断出这批工件中次品的总数。

你可以进行以下两类操作：

1. 区间批量光检：选择一个起始工件编号 l（整数），我会返回从工件 l 开始、连续 {k} 个工件中的次品数量。注意：
   - 起始编号 l 的有效范围是 1 到 {max_start}（即 {n} - {k} + 1）
   - 如果起始编号超出有效范围，检测设备将报警，但该次扫描仍会计入设备损耗次数
   - 返回值是一个 0 到 {k} 之间的整数

2. 最终质检签批：当你认为已经收集到足够的抽检数据后，可以提交你对整批工件次品总数的最终质检结论。

约束条件：
- 你的总扫描次数（包括有效和无效扫描）不能超过 {max_queries} 次
- 在进行最终质检签批前，你必须至少完成 2 次有效的区间批量光检
- 如果质检结论错误、扫描超过限制次数、或在扫描次数不足时提前签批，质检任务将失败

## 询问与提交答案的格式（必须严格遵守）

每次只能进行一个操作。请使用以下 XML 格式：

- 区间批量光检（例如从第 5 工件开始扫描）：
<query_range>5</query_range>

- 提交最终质检签批（例如认为次品总数是 8）：
<answer>8</answer>

请合理规划你的抽检策略，用尽可能少的设备扫描次数准确完成质量排查。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's perform an "Assembly Line Quality Sampling" task. Here are the rules:

An assembly line has produced a batch of {n} consecutive components, where each component's quality status is either defective (1) or qualified (0). Your goal is to infer the total number of defective components in this batch.

You can perform two types of operations:

1. Range Batch Optical Inspection: Choose a starting component number l (integer), and I will return the number of defective components within {k} consecutive components starting from component l. Note:
   - The valid range for starting component l is 1 to {max_start} (i.e., {n} - {k} + 1)
   - If the starting component is out of range, the inspection equipment will trigger an alarm, but it still counts toward your scan limit
   - The return value is an integer between 0 and {k}

2. Final Quality Certification: When you believe you have gathered enough sampling data, submit your final conclusion on the total number of defective components for the entire batch.

Constraints:
- Your total number of scans (including valid and invalid ones) cannot exceed {max_queries}
- Before issuing your final quality certification, you must complete at least 2 valid range batch optical inspections
- The task fails if your conclusion is incorrect, you exceed the scan limit, or you certify prematurely with insufficient scans

## Query and Answer Format (strictly required)

You can only perform one operation at a time. Use the following XML format:

- Range Batch Optical Inspection (e.g., scanning range starting at component 5):
<query_range>5</query_range>

- Submit Final Quality Certification (e.g., if you believe the total defective components is 8):
<answer>8</answer>

Plan your sampling strategy wisely to accurately complete the quality screening with as few equipment scans as possible.
"""

    # 场景 5：法律
    contextualized_rule_zh_5 = """\
我们来执行一项"商业合同合规性审查"任务，规则如下：

一份复杂的商业合同包含了 {n} 个连续的条款，每个条款的合规状态仅为存在法律风险（1）或合法合规（0）。你的目标是推断出这份合同中存在风险的条款总数。

你可以进行以下两类操作：

1. 条款区间审查：选择一个起始条款编号 l（整数），我会返回从条款 l 开始、连续 {k} 个条款中的风险条款数量。注意：
   - 起始编号 l 的有效范围是 1 到 {max_start}（即 {n} - {k} + 1）
   - 如果起始编号超出有效范围，审查系统将报错，但该次操作仍会计入审查调用次数
   - 返回值是一个 0 到 {k} 之间的整数

2. 最终法律意见书：当你认为已经收集到足够的审查证据后，可以提交你对合同风险条款总数的最终认定结论。

约束条件：
- 你的总审查次数（包括有效和无效审查）不能超过 {max_queries} 次
- 在出具最终法律意见书前，你必须至少完成 2 次有效的条款区间审查
- 如果认定结论错误、审查超过限制次数、或在审查次数不足时提前出具意见书，审查任务将失败

## 询问与提交答案的格式（必须严格遵守）

每次只能进行一个操作。请使用以下 XML 格式：

- 条款区间审查（例如从第 5 条款开始审查）：
<query_range>5</query_range>

- 提交最终法律意见书（例如认为风险条款总数是 8）：
<answer>8</answer>

请合理规划你的尽调策略，用尽可能少的审查资源准确完成合同合规排查。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's conduct a "Commercial Contract Compliance Review" task. Here are the rules:

A lengthy commercial contract contains {n} consecutive clauses, where the compliance status of each clause is either at legal risk (1) or legally compliant (0). Your goal is to infer the total number of risky clauses in this contract.

You can perform two types of operations:

1. Range Clause Due Diligence: Choose a starting clause number l (integer), and I will return the number of risky clauses within {k} consecutive clauses starting from clause l. Note:
   - The valid range for starting clause l is 1 to {max_start} (i.e., {n} - {k} + 1)
   - If the starting clause is out of range, the review system will report an error, but it still counts toward your review billable limit
   - The return value is an integer between 0 and {k}

2. Final Legal Opinion: When you believe you have gathered enough review evidence, submit your final conclusion on the total number of risky clauses in the contract.

Constraints:
- Your total number of reviews (including valid and invalid ones) cannot exceed {max_queries}
- Before issuing your final legal opinion, you must complete at least 2 valid range clause due diligence operations
- The task fails if your conclusion is incorrect, you exceed the review limit, or you issue the opinion prematurely with insufficient reviews

## Query and Answer Format (strictly required)

You can only perform one operation at a time. Use the following XML format:

- Range Clause Due Diligence (e.g., reviewing range starting at clause 5):
<query_range>5</query_range>

- Submit Final Legal Opinion (e.g., if you believe the total risky clauses is 8):
<answer>8</answer>

Plan your due diligence strategy wisely to accurately complete the contract compliance screening with minimal review resources.
"""

    tags = ["answer", "query_range"]
    
    reasoning_type = "演绎推理"
    data_structure = "序列"

    # 难度配置说明：
    # 1 (简单)       - N=10, K=5, Q_max=2，最简单的完全覆盖
    # 2 (中等偏下)   - N=12, K=4, Q_max=3，需要简单规划
    # 3 (中等偏上)   - N=16, K=4, Q_max=4，标准分块查询
    # 4 (较难)       - N=20, K=5, Q_max=4，需要优化查询位置
    # 5 (难)         - N=24, K=6, Q_max=4，紧凑的查询预算

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 10,
                "k": 5,
                "sequence": "1,0,1,1,0,0,1,0,1,1",  # sum=6
            },
            2: {
                "n": 12,
                "k": 4,
                "sequence": "1,1,0,1,0,1,1,0,0,1,0,1",  # sum=7
            },
            3: {
                "n": 16,
                "k": 4,
                "sequence": "1,0,1,1,0,0,1,0,1,1,0,1,0,1,1,0",  # sum=9
            },
            4: {
                "n": 20,
                "k": 5,
                "sequence": "1,1,0,1,0,0,1,1,0,1,0,1,0,0,1,1,0,1,0,1",  # sum=11
            },
            5: {
                "n": 24,
                "k": 6,
                "sequence": "1,0,1,1,0,1,0,1,0,1,1,0,1,0,0,1,1,0,1,0,1,1,0,1",  # sum=14
            },
        },
        "en": {
            1: {
                "n": 10,
                "k": 5,
                "sequence": "1,0,1,1,0,0,1,0,1,1",
            },
            2: {
                "n": 12,
                "k": 4,
                "sequence": "1,1,0,1,0,1,1,0,0,1,0,1",
            },
            3: {
                "n": 16,
                "k": 4,
                "sequence": "1,0,1,1,0,0,1,0,1,1,0,1,0,1,1,0",
            },
            4: {
                "n": 20,
                "k": 5,
                "sequence": "1,1,0,1,0,0,1,1,0,1,0,1,0,0,1,1,0,1,0,1",
            },
            5: {
                "n": 24,
                "k": 6,
                "sequence": "1,0,1,1,0,1,0,1,0,1,1,0,1,0,0,1,1,0,1,0,1,1,0,1",
            },
        },
    }

    def __init__(self, config):
        # 先设置占位符，等待 _initialize_game 填充
        self._game_info = {}
        self.query_count = 0
        self.valid_query_count = 0
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏参数和序列"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 解析序列
        self.sequence = [int(x.strip()) for x in cfg["sequence"].split(",")]
        self.n = cfg["n"]
        self.k = cfg["k"]
        
        # 验证配置合法性
        if len(self.sequence) != self.n:
            raise ValueError(f"Sequence length mismatch: expected {self.n}, got {len(self.sequence)}")
        if self.k > self.n or self.n % self.k != 0:
            raise ValueError(f"Invalid K={self.k} for N={self.n}")
        
        # 计算真实答案（序列中1的总数）
        self.target_sum = sum(self.sequence)
        
        # 计算最大查询次数和最大起点
        self.max_queries = self.n // self.k
        self.max_start = self.n - self.k + 1
        
        # 填充游戏信息用于格式化规则文本
        self._game_info = {
            "n": self.n,
            "k": self.k,
            "max_queries": self.max_queries,
            "max_start": self.max_start,
        }
        
        # 初始化查询计数
        self.query_count = 0
        self.valid_query_count = 0

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        # 检查是否满足最小查询次数要求
        if self.valid_query_count < 2:
            return False
        
        try:
            answer = int(parsed_info["answer"].strip())
            return answer == self.target_sum
        except (ValueError, KeyError):
            return False

    def _cf_core_produce(self, parsed_info):
        """原始的处理查询并生成响应逻辑"""
        # 检查是否超过查询限制
        if self.query_count >= self.max_queries:
            if self.config.language == "zh":
                raise ValueError(f"查询次数已达上限 {self.max_queries} 次。")
            else:
                raise ValueError(f"Query limit of {self.max_queries} has been reached.")
        
        # 处理区间和查询
        if "query_range" in parsed_info:
            self.query_count += 1
            
            try:
                start_pos = int(parsed_info["query_range"].strip())
            except ValueError:
                if self.config.language == "zh":
                    return f"无效查询：起点位置必须是整数。（已使用 {self.query_count}/{self.max_queries} 次查询）"
                else:
                    return f"Invalid query: starting position must be an integer. (Query {self.query_count}/{self.max_queries} used)"
            
            # 检查起点是否在有效范围内
            if start_pos < 1 or start_pos > self.max_start:
                if self.config.language == "zh":
                    return f"无效查询：起点 {start_pos} 超出有效范围 [1, {self.max_start}]。（已使用 {self.query_count}/{self.max_queries} 次查询）"
                else:
                    return f"Invalid query: starting position {start_pos} is out of valid range [1, {self.max_start}]. (Query {self.query_count}/{self.max_queries} used)"
            
            # 计算区间和（注意：位置从1开始，但数组索引从0开始）
            range_sum = sum(self.sequence[start_pos - 1 : start_pos - 1 + self.k])
            self.valid_query_count += 1
            
            if self.config.language == "zh":
                return f"{range_sum}（已使用 {self.query_count}/{self.max_queries} 次查询）"
            else:
                return f"{range_sum} (Query {self.query_count}/{self.max_queries} used)"
        
        else:
            # 不应该到达这里，因为 parse 已经验证了标签
            if self.config.language == "zh":
                raise ValueError("无效的操作：未找到有效的查询标签。")
            else:
                raise ValueError("Invalid operation: no valid query tag found.")

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
        queries = []
        # 遍历所有合法的起点位置
        # 有效范围是 [1, max_start]
        for start_pos in range(1, self.max_start + 1):
            # 直接计算区间和，不通过 _cf_core_produce 以避免副作用（如增加查询计数）
            # 注意：位置从1开始，但数组索引从0开始
            range_sum = sum(self.sequence[start_pos - 1 : start_pos - 1 + self.k])
            
            # 构造返回值
            # query 对应 parsed_info["query_range"] 的值
            # answer 为该次查询的正确数值结果字符串
            queries.append({
                "query": str(start_pos),
                "answer": str(range_sum)
            })
            
        return queries

    def _cf_make_wrong(self, correct):
        """生成错误答案"""
        # 若 correct 是纯整数字符串
        if correct.isdigit() or (correct.startswith('-') and correct[1:].isdigit()):
            return str(int(correct) + 1)
        
        # 替换关键词（中文）
        if "是" in correct:
            return correct.replace("是", "否")
        if "否" in correct:
            return correct.replace("否", "是")
        
        # 替换关键词（英文，忽略大小写但保持原格式不太容易完全精确，这里按常见情况处理）
        # 简单处理：如果完全匹配 "Yes" 或 "No"
        if correct.lower() == "yes":
            return "No" if correct[0].isupper() else "no"
        if correct.lower() == "no":
            return "Yes" if correct[0].isupper() else "yes"
            
        # 都不匹配，追加 _WRONG
        return correct + "_WRONG"

    def step(self, response: str) -> "GameState":
        """重写 step 方法以添加额外的验证逻辑"""
        try:
            parsed_info = self.parse(response)
            
            if "answer" in parsed_info:
                # 检查是否满足最小查询次数
                if self.valid_query_count < 2:
                    if self.config.language == "zh":
                        self.state.set_state("failed", "insufficient queries")
                        self.state.add_message("user", f"提交失败：在提交最终答案前，你必须至少完成 2 次有效的区间和查询。当前有效查询次数：{self.valid_query_count}")
                    else:
                        self.state.set_state("failed", "insufficient queries")
                        self.state.add_message("user", f"Submission failed: you must complete at least 2 valid range sum queries before submitting. Current valid queries: {self.valid_query_count}")
                    return self.state
                
                # 评估答案
                is_success = self.evaluate(parsed_info)
                if is_success:
                    res = "答案正确！" if self.config.language == "zh" else "Correct answer!"
                    self.state.set_state("success", "success")
                    self.state.add_message("user", res)
                else:
                    res = f"答案错误。正确答案是 {self.target_sum}。" if self.config.language == "zh" else f"Incorrect answer. The correct answer is {self.target_sum}."
                    self.state.set_state("failed", "incorrect answer")
                    self.state.add_message("user", res)
            else:
                # 处理查询
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))
        
        return self.state