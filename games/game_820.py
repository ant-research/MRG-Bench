# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   极值元素：序列中最大/最小的元素是什么
# ============================================================

from .base import Game
import random


class MaxValueSearchGame(Game):

    game_rule_zh = """\
我们来玩一个"最大值搜索"推理游戏，规则如下：

游戏设定了一个长度为 {n} 的序列 A[1..{n}]，序列中所有元素两两不同，存在唯一的全局最大值，其位置记为 M。

同时，游戏还设定了一个固定但未知的整数半径 R，满足 1 小于等于 R 小于等于 {max_r}。

你的目标是通过交互式查询，推断出全局最大值的位置 M。

你可以反复进行以下查询（每次仅限一个查询）：

1. 探测查询 probe(x)：询问位置 x 附近（在以 x 为中心、半径 R 的范围内）的最大值位置。
   - 约束：x 必须是 1 到 {n} 之间的整数。
   - 反馈：返回一个索引 idx，表示在区间 [max(1, x-R), min({n}, x+R)] 内具有最大值的唯一位置。

当你收集到足够信息后，请提交你认为的全局最大值位置。若答案错误或格式不符，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 探测查询（例如查询位置 5）：
<query_probe>5</query_probe>

提交最终答案时，必须给出你认为的全局最大值位置 M（1 到 {n} 之间的整数），格式如下：

<answer>M</answer>

例如：
<answer>7</answer>

注意：同一位置的探测查询结果是确定的，多次查询同一位置会得到相同的结果。请尽可能用最少的查询次数找到答案。
"""

    game_rule_en = """\
Let's play a "Maximum Value Search" deduction game. Here are the rules:

The game has set up a sequence A[1..{n}] of length {n}, where all elements are distinct, and there exists a unique global maximum value at position M.

Additionally, the game has set a fixed but unknown integer radius R, satisfying 1 less than or equal to R less than or equal to {max_r}.

Your goal is to infer the position M of the global maximum through interactive queries.

You can repeatedly perform the following query (one query per turn):

1. Probe query probe(x): Ask for the position of the maximum value near position x (within a range of radius R centered at x).
   - Constraint: x must be an integer between 1 and {n}.
   - Feedback: Returns an index idx, representing the unique position with the maximum value in the interval [max(1, x-R), min({n}, x+R)].

When you have gathered enough information, submit the position you believe to be the global maximum. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Probe query (e.g., querying position 5):
<query_probe>5</query_probe>

When submitting the final answer, you must provide the position M you believe to be the global maximum (an integer between 1 and {n}), in the following format:

<answer>M</answer>

For example:
<answer>7</answer>

Note: The result of a probe query at the same position is deterministic. Querying the same position multiple times will yield the same result. Try to find the answer with as few queries as possible.
"""

    contextualized_rule_zh_1 = """\
我们在进行一场"交通管网排查"任务，规则如下：

城市主干道包含 {n} 个连续的路口（编号 1 到 {n}），各路口拥堵指数各不相同，存在一个唯一的“全局极度拥堵核心”，其位置记为 M。

同时，系统配备了交通监控雷达，其固定有效扫描半径为 R 个路口，满足 1 小于等于 R 小于等于 {max_r}，R 为未知定值。

你的目标是通过交互式探测，推断出全局极度拥堵核心的确切路口位置 M。

你可以反复进行以下查询（每次仅限一个查询）：

1. 探测查询 probe(x)：在路口 x 处部署无人机探测。
   - 约束：x 必须是 1 到 {n} 之间的整数。
   - 反馈：返回一个路口编号 idx，表示在雷达覆盖区间 [max(1, x-R), min({n}, x+R)] 范围内拥堵指数最高的具体路口。

当你收集到足够信息后，请提交你认为的极度拥堵核心位置。若答案错误或格式不符，排查任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 探测查询（例如探测路口 5）：
<query_probe>5</query_probe>

提交最终答案时，必须给出你认为的核心拥堵路口位置 M（1 到 {n} 之间的整数），格式如下：

<answer>M</answer>

例如：
<answer>7</answer>

注意：同一路口的探测查询结果是确定的，多次查询同一位置会得到相同的结果。请尽可能用最少的调度次数找到核心路口。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's engage in a "Traffic Network Inspection" task. Here are the rules:

An urban main road consists of {n} continuous intersections (numbered 1 to {n}) with distinct congestion indices. There is a unique "global congestion core" with the highest congestion index at position M.

Additionally, the monitoring system is equipped with a traffic radar that has a fixed, unknown scanning radius of R intersections, satisfying 1 less than or equal to R less than or equal to {max_r}.

Your goal is to infer the exact position M of the global congestion core through interactive queries.

You can repeatedly perform the following query (one query per turn):

1. Probe query probe(x): Deploy a drone for detection at intersection x.
   - Constraint: x must be an integer between 1 and {n}.
   - Feedback: Returns an intersection ID idx, representing the specific intersection with the highest congestion index within the radar coverage interval [max(1, x-R), min({n}, x+R)].

When you have gathered enough information, submit the position you believe to be the global congestion core M. If the answer is wrong or the format is invalid, the inspection task fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Probe query (e.g., detecting intersection 5):
<query_probe>5</query_probe>

When submitting the final answer, you must provide the intersection position M (an integer between 1 and {n}), in the following format:

<answer>M</answer>

For example:
<answer>7</answer>

Note: The result of a probe query at the same intersection is deterministic. Querying the same location multiple times will yield the same result. Try to find the answer with as few queries as possible.
"""

    contextualized_rule_zh_2 = """\
我们在进行一场"基因靶向定位"任务，规则如下：

在一段包含 {n} 个连续位点（编号 1 到 {n}）的基因序列中，各由于突变导致的异常表达量互不相同，存在唯一一个表达量达到峰值的“核心突变位点”，其位置记为 M。

现在你拥有一种靶向检测试剂，该试剂具有固定的扩散影响半径 R 个位点，满足 1 小于等于 R 小于等于 {max_r}，R 为未知定值。

你的目标是通过交互式滴定测试，推断出核心突变位点的确切位置 M。

你可以反复进行以下查询（每次仅限一个查询）：

1. 探测查询 probe(x)：在基因位点 x 处滴加检测试剂。
   - 约束：x 必须是 1 到 {n} 之间的整数。
   - 反馈：返回一个位点编号 idx，表示在试剂扩散区间 [max(1, x-R), min({n}, x+R)] 范围内异常表达量最高的具体位点。

当你收集到足够信息后，请提交你认为的核心突变位点位置。若答案错误或格式不符，靶向定位任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 探测查询（例如滴定位点 5）：
<query_probe>5</query_probe>

提交最终答案时，必须给出你认为的核心突变位点 M（1 到 {n} 之间的整数），格式如下：

<answer>M</answer>

例如：
<answer>7</answer>

注意：同一位点的探测查询结果是确定的，多次查询同一位置会得到相同的结果。请尽可能用最少的试剂消耗量找到突变位点。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct a "Targeted Gene Localization" task. Here are the rules:

In a gene sequence consisting of {n} continuous loci (numbered 1 to {n}), the abnormal expression levels caused by mutations are all distinct. There exists a unique "core mutation locus" with peak expression level at position M.

You possess a targeted testing reagent with a fixed, unknown diffusion radius of R loci, satisfying 1 less than or equal to R less than or equal to {max_r}.

Your objective is to infer the exact position M of the core mutation locus through interactive titration queries.

You can repeatedly perform the following query (one query per turn):

1. Probe query probe(x): Apply the testing reagent at gene locus x.
   - Constraint: x must be an integer between 1 and {n}.
   - Feedback: Returns a locus ID idx, representing the specific locus with the highest abnormal expression level within the diffusion interval [max(1, x-R), min({n}, x+R)].

When you have gathered enough information, submit the position you believe to be the core mutation locus M. If the answer is wrong or the format is invalid, the localization task fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Probe query (e.g., testing locus 5):
<query_probe>5</query_probe>

When submitting the final answer, you must provide the core mutation locus M (an integer between 1 and {n}), in the following format:

<answer>M</answer>

For example:
<answer>7</answer>

Note: The result of a probe query at the same locus is deterministic. Querying the same location multiple times will yield the same result. Try to find the answer with minimal reagent consumption.
"""

    contextualized_rule_zh_3 = """\
我们来执行一项"学习路径诊断"任务，规则如下：

一门学科的学习路径包含 {n} 个连续的核心知识点（编号 1 到 {n}），各个知识点的学习失分率各不相同，存在一个唯一的最难跨越的“全局瓶颈知识点”，其位置记为 M。

认知评估系统具有固定的关联探测半径 R 个知识点，满足 1 小于等于 R 小于等于 {max_r}，R 为未知定值。

你的目标是通过交互式探针测试，推断出全局瓶颈知识点的位置 M。

你可以反复进行以下查询（每次仅限一个查询）：

1. 探测查询 probe(x)：对知识点 x 发起认知探针测试。
   - 约束：x 必须是 1 到 {n} 之间的整数。
   - 反馈：返回一个知识点编号 idx，表示在关联上下文区间 [max(1, x-R), min({n}, x+R)] 内失分率最高（即最难掌握）的知识点。

当你收集到足够信息后，请提交你认为的全局瓶颈知识点位置。若答案错误或格式不符，诊断任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 探测查询（例如测试知识点 5）：
<query_probe>5</query_probe>

提交最终答案时，必须给出你认为的瓶颈知识点位置 M（1 到 {n} 之间的整数），格式如下：

<answer>M</answer>

例如：
<answer>7</answer>

注意：同一知识点的探测查询结果是确定的，多次测试同一位置会得到相同的结果。请尽可能用最少的测评次数完成诊断。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's execute a "Learning Path Diagnosis" task. Here are the rules:

A subject's learning path contains {n} linearly arranged core knowledge points (numbered 1 to {n}). The scoring loss rates for these points are all distinct, and there is a unique "global bottleneck knowledge point" that is hardest to overcome at position M.

The cognitive assessment system has a fixed, unknown associated knowledge detection radius of R points, satisfying 1 less than or equal to R less than or equal to {max_r}.

Your goal is to infer the position M of the global bottleneck knowledge point through interactive probe tests.

You can repeatedly perform the following query (one query per turn):

1. Probe query probe(x): Launch a cognitive probe test on knowledge point x.
   - Constraint: x must be an integer between 1 and {n}.
   - Feedback: Returns a knowledge point ID idx, representing the hardest point (highest loss rate) within the contextual interval [max(1, x-R), min({n}, x+R)].

When you have gathered enough information, submit the position you believe to be the global bottleneck. If the answer is wrong or the format is invalid, the diagnosis task fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Probe query (e.g., probing point 5):
<query_probe>5</query_probe>

When submitting the final answer, you must provide the bottleneck position M (an integer between 1 and {n}), in the following format:

<answer>M</answer>

For example:
<answer>7</answer>

Note: The result of a probe query at the same point is deterministic. Testing the same position multiple times will yield the same result. Try to complete the diagnosis with as few assessments as possible.
"""

    contextualized_rule_zh_4 = """\
我们要处理一项"流水线故障排查"任务，规则如下：

一条自动化流水线包含 {n} 个连续的加工工位（编号 1 到 {n}），各工位的运行温度均不相同，目前存在一个温度达到峰值的“核心故障源”，其位置记为 M。

检修设备配备了便携式热成像仪，其固定的有效探测半径为 R 个工位，满足 1 小于等于 R 小于等于 {max_r}，R 为未知定值。

你的目标是通过交互式探测，推断出核心故障源的确切位置 M。

你可以反复进行以下查询（每次仅限一个查询）：

1. 探测查询 probe(x)：在工位 x 处架设热成像仪进行热场扫描。
   - 约束：x 必须是 1 到 {n} 之间的整数。
   - 反馈：返回一个工位编号 idx，表示在热成像仪覆盖区间 [max(1, x-R), min({n}, x+R)] 范围内温度最高的具体工位。

当你收集到足够信息后，请提交你认为的核心故障源工位编号。若答案错误或格式不符，排查任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 探测查询（例如扫描工位 5）：
<query_probe>5</query_probe>

提交最终答案时，必须给出核心故障源工位 M（1 到 {n} 之间的整数），格式如下：

<answer>M</answer>

例如：
<answer>7</answer>

注意：同一工位的热场扫描结果是确定的，多次扫描同一位置会得到相同的结果。请尽可能用最少的热成像仪移动次数完成排查。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
We need to handle an "Assembly Line Fault Troubleshooting" task. Here are the rules:

An automated assembly line consists of {n} continuous processing stations (numbered 1 to {n}). The operating temperatures of all stations are distinct, and currently, there is a "core fault source" reaching peak temperature at position M.

Maintenance personnel are equipped with a portable thermal imager with a fixed, unknown effective scanning radius of R stations, satisfying 1 less than or equal to R less than or equal to {max_r}.

Your goal is to infer the exact position M of the core fault source through interactive detection.

You can repeatedly perform the following query (one query per turn):

1. Probe query probe(x): Set up the thermal imager at station x for a thermal field scan.
   - Constraint: x must be an integer between 1 and {n}.
   - Feedback: Returns a station ID idx, representing the specific station with the highest temperature within the imager's coverage interval [max(1, x-R), min({n}, x+R)].

When you have gathered enough information, submit the station ID you believe to be the core fault source. If the answer is wrong or the format is invalid, the troubleshooting task fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Probe query (e.g., scanning station 5):
<query_probe>5</query_probe>

When submitting the final answer, you must provide the core fault source station M (an integer between 1 and {n}), in the following format:

<answer>M</answer>

For example:
<answer>7</answer>

Note: The thermal scan result at the same station is deterministic. Scanning the same location multiple times will yield the same result. Try to complete the troubleshooting with minimal repositioning of the imager.
"""

    contextualized_rule_zh_5 = """\
我们要执行一项"合同漏洞审查"任务，规则如下：

一份复杂的商业合同包含 {n} 个连续的条款（编号 1 到 {n}），各条款的隐含法律风险指数各不相同，存在一个风险指数最高的“核心漏洞条款”，其位置记为 M。

你使用的是一款 AI 智能审查工具，该工具提取上下文关联审查的固定半径为 R 个条款，满足 1 小于等于 R 小于等于 {max_r}，R 为未知定值。

你的目标是通过交互式查询，推断出核心漏洞条款的确切位置 M。

你可以反复进行以下查询（每次仅限一个查询）：

1. 探测查询 probe(x)：将条款 x 输入 AI 审查工具进行局部评估。
   - 约束：x 必须是 1 到 {n} 之间的整数。
   - 反馈：返回一个条款编号 idx，表示在关联审查区间 [max(1, x-R), min({n}, x+R)] 内风险指数最高的具体条款。

当你收集到足够信息后，请提交你认为的核心漏洞条款位置。若答案错误或格式不符，尽职调查任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 探测查询（例如评估条款 5）：
<query_probe>5</query_probe>

提交最终答案时，必须给出核心漏洞条款编号 M（1 到 {n} 之间的整数），格式如下：

<answer>M</answer>

例如：
<answer>7</answer>

注意：同一条款的审查探测结果是确定的，多次查询同一位置会得到相同的结果。请尽可能用最少的审查次数发现最终风险点。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's perform a "Contract Loophole Review" task. Here are the rules:

A complex commercial contract contains {n} continuous clauses (numbered 1 to {n}). The implicit legal risk indices of these clauses are all distinct, with a unique "core loophole clause" carrying the highest risk at position M.

You are conducting due diligence using an AI smart review tool, which extracts and evaluates context within a fixed, unknown radius of R clauses, satisfying 1 less than or equal to R less than or equal to {max_r}.

Your goal is to infer the exact position M of the core loophole clause through interactive queries.

You can repeatedly perform the following query (one query per turn):

1. Probe query probe(x): Input clause x into the AI review tool for localized evaluation.
   - Constraint: x must be an integer between 1 and {n}.
   - Feedback: Returns a clause ID idx, representing the specific clause with the highest risk index within the review interval [max(1, x-R), min({n}, x+R)].

When you have gathered enough information, submit the clause ID you believe to be the core loophole. If the answer is wrong or the format is invalid, the due diligence task fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Probe query (e.g., reviewing clause 5):
<query_probe>5</query_probe>

When submitting the final answer, you must provide the loophole clause ID M (an integer between 1 and {n}), in the following format:

<answer>M</answer>

For example:
<answer>7</answer>

Note: The review result of a probe query at the same clause is deterministic. Querying the same clause multiple times will yield the same result. Try to identify the ultimate risk point with as few review steps as possible.
"""

    tags = ["answer", "query_probe"]

    reasoning_type = "归纳推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 10,
                "r": 3,
                "m": 5,
                "seed": 42,
            },
            2: {
                "n": 15,
                "r": 2,
                "m": 11,
                "seed": 123,
            },
            3: {
                "n": 20,
                "r": 3,
                "m": 3,
                "seed": 456,
            },
            4: {
                "n": 25,
                "r": 2,
                "m": 18,
                "seed": 789,
            },
            5: {
                "n": 30,
                "r": 1,
                "m": 23,
                "seed": 999,
            },
        },
        "en": {
            1: {
                "n": 10,
                "r": 3,
                "m": 5,
                "seed": 42,
            },
            2: {
                "n": 15,
                "r": 2,
                "m": 11,
                "seed": 123,
            },
            3: {
                "n": 20,
                "r": 3,
                "m": 3,
                "seed": 456,
            },
            4: {
                "n": 25,
                "r": 2,
                "m": 18,
                "seed": 789,
            },
            5: {
                "n": 30,
                "r": 1,
                "m": 23,
                "seed": 999,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：根据难度配置生成序列和参数"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 修复：确保 difficulty 为整数

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.n = cfg["n"]
        self.r = cfg["r"]
        self.m = cfg["m"]  # 全局最大值的真实位置（1-indexed）
        
        # 计算最大可能的半径用于游戏规则展示
        max_r = (self.n - 1) // 2
        self._game_info["n"] = self.n
        self._game_info["max_r"] = max_r
        
        # 修复：使用局部随机数生成器，避免污染全局状态
        rng = random.Random(cfg["seed"])
        # 生成 n 个不同的值，从 1 到 1000*n 的范围内随机抽取
        values = rng.sample(range(1, 1000 * self.n + 1), self.n)
        
        # 确保 m 位置的值最大：找到当前最大值，与 m 位置交换
        max_idx = values.index(max(values))
        values[self.m - 1], values[max_idx] = values[max_idx], values[self.m - 1]
        
        # 序列 A 使用 1-indexed（为了方便，索引 0 位置留空）
        self.sequence = [None] + values

    def evaluate(self, parsed_info):
        """评估答案是否正确"""
        try:
            answer_str = parsed_info["answer"].strip()
            answer = int(answer_str)
            return answer == self.m
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """根据查询生成响应"""
        if "query_probe" in parsed_info:
            try:
                x_str = parsed_info["query_probe"].strip()
                x = int(x_str)
                
                # 检查 x 是否在有效范围内
                if x < 1 or x > self.n:
                    if self.config.language == "zh":
                        return f"错误：位置必须在 1 到 {self.n} 之间。"
                    else:
                        return f"Error: Position must be between 1 and {self.n}."
                
                # 计算窗口范围 [left, right]
                left = max(1, x - self.r)
                right = min(self.n, x + self.r)
                
                # 在窗口内找最大值的位置
                max_val = self.sequence[left]
                max_pos = left
                for i in range(left + 1, right + 1):
                    if self.sequence[i] > max_val:
                        max_val = self.sequence[i]
                        max_pos = i
                
                return str(max_pos)
                
            except ValueError:
                if self.config.language == "zh":
                    return "错误：查询格式无效，请提供一个整数位置。"
                else:
                    return "Error: Invalid query format, please provide an integer position."
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        try:
            val = int(correct)
            # 确保错误答案在 [1, n] 范围内且不等于正确答案
            wrong_val = val + 1
            if wrong_val > self.n:
                wrong_val = val - 1
            if wrong_val < 1:
                wrong_val = val + 1  # n >= 2 时不会走到这里
            return str(wrong_val)
        except ValueError:
            pass

        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        elif self.config.language == "en":
            # 忽略大小写，保持原始大小写风格
            correct_lower = correct.lower()
            if "yes" in correct_lower:
                return correct.replace("Yes", "No").replace("yes", "no").replace("YES", "NO")
            if "no" in correct_lower:
                return correct.replace("No", "Yes").replace("no", "yes").replace("NO", "YES")
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        results = []
        for x in range(1, self.n + 1):
            query_content = str(x)
            parsed_info = {"query_probe": query_content}
            # 调用内部逻辑获取正确回复
            answer = self._cf_core_produce(parsed_info)
            results.append({
                "query": f"<query_probe>{query_content}</query_probe>",
                "answer": answer
            })
        return results