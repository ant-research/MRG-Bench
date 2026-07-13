# -*- coding: utf-8 -*-
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   区间条件计数：某区间内满足特定条件的元素有多少个
# ============================================================

from .base import Game
import random


class BinarySequenceFindingGame(Game):

    game_rule_zh = """\
我们现在来玩一个"二元序列推理"的游戏，规则如下：

游戏设定了一个长度为 {n} 的二元序列 S，其中恰有 {k} 个位置的值为 1，其余位置为 0。这个序列在游戏过程中保持不变。

你的目标是通过提问确定所有值为 1 的位置。你可以反复向我提出以下类型的问题：

1. 区间计数查询：询问区间 [L, R] 内有多少个 1。其中 L 和 R 是位置编号（从 1 到 {n}），且必须满足 L 小于 R（不允许单点查询）。我会回答该区间内 1 的个数。

当你收集足够信息后，请提交最终答案：列出所有你认为值为 1 的位置编号。若答案错误，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 区间计数查询（例如查询区间 [2, 5]）：
<query_range>2,5</query_range>

提交最终答案时，列出所有值为 1 的位置编号（用逗号隔开，按从小到大的顺序排列），格式如下：

<answer>1,3,7</answer>

注意：请尽可能用较少的查询次数找到答案。
"""

    game_rule_en = """\
Let's play a "Binary Sequence Deduction" game. Here are the rules:

There is a binary sequence S of length {n}, where exactly {k} positions have the value 1, and the rest are 0. This sequence remains constant throughout the game.

Your goal is to determine all positions with value 1 through queries. You can repeatedly ask me the following type of question:

1. Range Count Query: Ask how many 1s are in the range [L, R]. Here L and R are position indices (from 1 to {n}), and must satisfy L less than R (single-point queries are not allowed). I will answer the count of 1s in that range.

When you have enough information, submit your final answer: list all position indices you believe have value 1. If the answer is wrong, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Range Count Query (e.g., querying range [2, 5]):
<query_range>2,5</query_range>

When submitting the final answer, list all position indices with value 1 (comma-separated, in ascending order), using this format:

<answer>1,3,7</answer>

Note: Try to find the answer with as few queries as possible.
"""

    # ==========================================
    # 场景 1：交通
    # ==========================================
    contextualized_rule_zh_1 = """\
我们正在排查城市主干道上的智能交通系统。在这条道路上，沿途依次安装了 {n} 个交通传感器，其中恰好有 {k} 个传感器发生了离线故障（状态为 1，正常为 0）。你的任务是通过诊断系统定位所有故障传感器。这个状态在排查期间保持不变。

你可以发起以下类型的区间诊断请求：

1. 区间故障计数查询：指定路段起点 L 和终点 R（编号 1 到 {n}，且 L 小于 R，不允许单点查询），系统会返回该区间内的故障传感器总数。

当你收集足够信息后，请提交最终答案：列出所有故障传感器的编号。若答案错误，排查失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 区间计数查询（例如查询区间 [2, 5]）：
<query_range>2,5</query_range>

提交最终答案时，列出所有故障传感器的编号（用逗号隔开，按从小到大的顺序排列），格式如下：

<answer>1,3,7</answer>

注意：请尽可能用较少的查询次数找到答案。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
We are troubleshooting the intelligent traffic system on a main city road. There are {n} consecutive traffic sensors installed along the road, exactly {k} of which have gone offline due to a malfunction (status 1, normal is 0). Your task is to locate all faulty sensors through the diagnostic system. This state remains constant during the process.

You can initiate the following type of range diagnostic requests:

1. Range Fault Count Query: Specify the starting point L and ending point R (indices from 1 to {n}, where L is less than R, single-point queries are not allowed). The system will return the total number of faulty sensors in that range.

When you have enough information, submit your final answer: list the indices of all faulty sensors. If the answer is wrong, the troubleshooting fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Range Count Query (e.g., querying range [2, 5]):
<query_range>2,5</query_range>

When submitting the final answer, list all faulty sensor indices (comma-separated, in ascending order), using this format:

<answer>1,3,7</answer>

Note: Try to find the answer with as few queries as possible.
"""

    # ==========================================
    # 场景 2：医疗
    # ==========================================
    contextualized_rule_zh_2 = """\
我们正在进行基因序列的高通量筛查。系统载入了一组长度为 {n} 的基因样本序列，经过初步扫描，确定其中恰好有 {k} 个样本携带特定的罕见突变（状态为 1，正常为 0）。你的任务是精确定位这些突变样本。

你可以使用批量检测仪进行排查：

1. 区间突变计数查询：指定样本编号区间 [L, R]（从 1 到 {n}，且 L 小于 R，不允许单点查询），仪器将返回该区间内携带突变的样本总数。

在锁定所有目标后，请提交所有突变样本的确切编号。若答案错误，筛查失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 区间计数查询（例如查询区间 [2, 5]）：
<query_range>2,5</query_range>

提交最终答案时，列出所有突变样本的编号（用逗号隔开，按从小到大的顺序排列），格式如下：

<answer>1,3,7</answer>

注意：请尽可能用较少的查询次数找到答案。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
We are conducting high-throughput screening on genetic sequences. The system has loaded a sequence of {n} genetic samples. Preliminary scans indicate that exactly {k} samples carry a specific rare mutation (status 1, normal is 0). Your task is to precisely locate these mutated samples.

You can use the batch testing instrument for investigation:

1. Range Mutation Count Query: Specify a sample index range [L, R] (from 1 to {n}, where L is less than R, single-point queries are not allowed), and the instrument will return the total number of mutated samples in that range.

Once you have locked onto all targets, submit the exact indices of all mutated samples. If the answer is wrong, the screening fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Range Count Query (e.g., querying range [2, 5]):
<query_range>2,5</query_range>

When submitting the final answer, list all mutated sample indices (comma-separated, in ascending order), using this format:

<answer>1,3,7</answer>

Note: Try to find the answer with as few queries as possible.
"""

    # ==========================================
    # 场景 3：教育
    # ==========================================
    contextualized_rule_zh_3 = """\
我们正在审核标准化考试的机读答题卡。这是一份包含 {n} 道题目的答题卡序列，系统提示因排版原因，其中恰好有 {k} 道题目存在识别异常（状态为 1，正常为 0）。你的目标是找出所有异常题目的题号。

你可以向智能阅卷系统发出查询指令：

1. 区间异常计数查询：询问第 L 题到第 R 题（题号 1 到 {n}，且 L 必须小于 R，不允许单点查询）之间有多少道异常题目，系统会返回具体的异常题数。

查明真相后，请提交所有识别异常的题目编号。若答案错误，审核失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 区间计数查询（例如查询区间 [2, 5]）：
<query_range>2,5</query_range>

提交最终答案时，列出所有异常题目的编号（用逗号隔开，按从小到大的顺序排列），格式如下：

<answer>1,3,7</answer>

注意：请尽可能用较少的查询次数找到答案。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
We are reviewing optical mark recognition answer sheets for a standardized test. The sheet contains a sequence of {n} questions. The system reports that exactly {k} questions have recognition anomalies due to formatting issues (status 1, normal is 0). Your goal is to identify the question numbers of all anomalous items.

You can issue query commands to the automated grading system:

1. Range Anomaly Count Query: Ask how many anomalous questions exist between question L and question R (from 1 to {n}, where L must be less than R, single-point queries are not allowed). The system will return the specific count.

After ascertaining the facts, submit the indices of all anomalous questions. If the answer is wrong, the review fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Range Count Query (e.g., querying range [2, 5]):
<query_range>2,5</query_range>

When submitting the final answer, list all anomalous question indices (comma-separated, in ascending order), using this format:

<answer>1,3,7</answer>

Note: Try to find the answer with as few queries as possible.
"""

    # ==========================================
    # 场景 4：制造业/工业
    # ==========================================
    contextualized_rule_zh_4 = """\
我们正在监控自动化生产流水线的质量检测环节。当前批次连续下线了 {n} 个精密零部件，质检探头初步预警其中恰有 {k} 个存在微小瑕疵（状态为 1，合格品为 0）。你的任务是找出所有瑕疵品的准确位置。

你可以调用区域扫描仪进行排查：

1. 区间瑕疵计数查询：输入起始编号 L 和终止编号 R（1 到 {n}，需满足 L 小于 R，不允许单点查询），扫描仪会反馈该流水线区间内的瑕疵品总数。

确定所有目标后，请提交所有瑕疵零部件的流水号。若答案错误，质检失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 区间计数查询（例如查询区间 [2, 5]）：
<query_range>2,5</query_range>

提交最终答案时，列出所有瑕疵零部件的编号（用逗号隔开，按从小到大的顺序排列），格式如下：

<answer>1,3,7</answer>

注意：请尽可能用较少的查询次数找到答案。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
We are monitoring the quality inspection process of an automated production line. The current batch has consecutively produced {n} precision components. The inspection probe gave an initial warning that exactly {k} components have minor defects (status 1, normal is 0). Your task is to find the exact positions of all defective items.

You can call the area scanner for investigation:

1. Range Defect Count Query: Input the starting index L and ending index R (from 1 to {n}, strictly L < R, single-point queries are not allowed). The scanner will report the total number of defective components in that assembly line segment.

Once all targets are identified, submit the serial numbers of all defective components. If the answer is wrong, the quality inspection fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Range Count Query (e.g., querying range [2, 5]):
<query_range>2,5</query_range>

When submitting the final answer, list all defective component indices (comma-separated, in ascending order), using this format:

<answer>1,3,7</answer>

Note: Try to find the answer with as few queries as possible.
"""

    # ==========================================
    # 场景 5：法律
    # ==========================================
    contextualized_rule_zh_5 = """\
我们正在使用智能法务系统审查一份总计 {n} 页的商业并购合同。风险评估模型指出，合同中恰好有 {k} 页包含需要人工复核的关键合规漏洞（状态为 1，安全为 0）。你的任务是找出这些存在漏洞的页码。

你可以向系统进行范围检索：

1. 区间风险计数查询：输入起始页码 L 和终止页码 R（1 到 {n}，且 L 小于 R，不允许单页检索），系统会告知该页码区间内包含多少页带有合规漏洞的内容。

完成审查后，请提交所有包含风险漏洞的合同页码。若答案错误，审查失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 区间计数查询（例如查询区间 [2, 5]）：
<query_range>2,5</query_range>

提交最终答案时，列出所有存在风险漏洞的页码（用逗号隔开，按从小到大的顺序排列），格式如下：

<answer>1,3,7</answer>

注意：请尽可能用较少的查询次数找到答案。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
We are using an intelligent legal system to review a commercial M&A contract totaling {n} pages. The risk assessment model indicates that exactly {k} pages contain critical compliance loopholes requiring manual review (status 1, secure is 0). Your task is to identify these vulnerable pages.

You can perform range searches in the system:

1. Range Risk Count Query: Enter the starting page L and ending page R (from 1 to {n}, where L is less than R, single-page queries are not allowed). The system will inform you how many pages within that range contain compliance loopholes.

Upon completing the review, submit the page numbers of all pages containing risk loopholes. If the answer is wrong, the review fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Range Count Query (e.g., querying range [2, 5]):
<query_range>2,5</query_range>

When submitting the final answer, list all vulnerable page indices (comma-separated, in ascending order), using this format:

<answer>1,3,7</answer>

Note: Try to find the answer with as few queries as possible.
"""

    tags = ["answer", "query_range"]
    
    reasoning_type = "演绎推理"
    data_structure = "序列"

    # 难度配置说明：
    # 1 (简单)       - N=5,  K=2
    # 2 (中等偏下)   - N=8,  K=3
    # 3 (中等偏上)   - N=12, K=4
    # 4 (较难)       - N=16, K=5
    # 5 (难)         - N=20, K=6

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "k": 2,
                "positions": [2, 4],  # 值为1的位置
            },
            2: {
                "n": 8,
                "k": 3,
                "positions": [1, 5, 7],
            },
            3: {
                "n": 12,
                "k": 4,
                "positions": [3, 6, 9, 11],
            },
            4: {
                "n": 16,
                "k": 5,
                "positions": [2, 7, 10, 13, 15],
            },
            5: {
                "n": 20,
                "k": 6,
                "positions": [1, 5, 9, 12, 16, 19],
            },
        },
        "en": {
            1: {
                "n": 5,
                "k": 2,
                "positions": [2, 4],
            },
            2: {
                "n": 8,
                "k": 3,
                "positions": [1, 5, 7],
            },
            3: {
                "n": 12,
                "k": 4,
                "positions": [3, 6, 9, 11],
            },
            4: {
                "n": 16,
                "k": 5,
                "positions": [2, 7, 10, 13, 15],
            },
            5: {
                "n": 20,
                "k": 6,
                "positions": [1, 5, 9, 12, 16, 19],
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏，设置序列和目标位置"""
        lang = self.config.language
        diff = self.config.difficulty
        
        # 防御性转换：确保 difficulty 为 int
        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["k"] = cfg["k"]
        
        # 初始化二元序列
        self.n = cfg["n"]
        self.k = cfg["k"]
        self.positions = set(cfg["positions"])  # 值为1的位置集合
        
        # 验证配置有效性
        if len(self.positions) != self.k:
            raise ValueError(f"Position count mismatch: expected {self.k}, got {len(self.positions)}")
        if any(p < 1 or p > self.n for p in self.positions):
            raise ValueError(f"Position out of range [1, {self.n}]")

    def evaluate(self, parsed_info):
        """评估模型提交的答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        # 解析答案
        try:
            if not raw_ans:
                return False
            model_positions = set(int(x.strip()) for x in raw_ans.split(",") if x.strip())
        except:
            return False
        
        # 检查数量是否正确
        if len(model_positions) != self.k:
            return False
        
        # 检查位置是否在有效范围内
        if any(p < 1 or p > self.n for p in model_positions):
            return False
        
        # 检查是否与真实答案完全一致
        if model_positions != self.positions:
            return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        if "query_range" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        raw_query = parsed_info["query_range"].strip()
        
        # 解析区间 [L, R]
        try:
            parts = [x.strip() for x in raw_query.split(",")]
            if len(parts) != 2:
                raise ValueError("Query format error")
            
            L = int(parts[0])
            R = int(parts[1])
            
            # 验证区间有效性
            if L < 1 or R > self.n:
                if self.config.language == "zh":
                    return "错误：区间超出有效范围 [1, {}]。".format(self.n)
                else:
                    return "Error: Range out of valid bounds [1, {}].".format(self.n)
            
            if L >= R:
                if self.config.language == "zh":
                    return "错误：必须满足 L 小于 R（不允许单点查询）。"
                else:
                    return "Error: L must be less than R (single-point queries not allowed)."
            
            # 计算区间内1的个数
            count = sum(1 for p in self.positions if L <= p <= R)
            return str(count)
            
        except ValueError as e:
            if self.config.language == "zh":
                return "错误：查询格式无效。请使用格式：<query_range>L,R</query_range>"
            else:
                return "Error: Invalid query format. Please use format: <query_range>L,R</query_range>"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        合法查询定义：区间 [L, R] 其中 1 <= L < R <= n
        """
        results = []
        # L 从 1 到 n-1
        for L in range(1, self.n):
            # R 从 L+1 到 n
            for R in range(L + 1, self.n + 1):
                query_str = f"<query_range>{L},{R}</query_range>"
                # 计算区间内 1 的个数，逻辑与 _cf_core_produce 保持一致
                count = sum(1 for p in self.positions if L <= p <= R)
                results.append({
                    "query": query_str,
                    "answer": str(count)
                })
        return results

    def _cf_make_wrong(self, correct: str) -> str:
        stripped = correct.strip()
        # 处理纯数字（包括 "0"）
        if stripped.isdigit() or (stripped.startswith('-') and stripped[1:].isdigit()):
            val = int(stripped)
            # 避免返回相同值：如果+1超出合理范围则-1，但确保不等于原值
            wrong_val = val + 1 if val == 0 else val - 1
            return str(wrong_val)
        
        # 否则按规则替换关键词
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        else:
            # English Yes/No swap preserving case style
            lower_c = correct.lower()
            if lower_c == "yes":
                if correct.isupper(): return "NO"
                if correct[0].isupper(): return "No"
                return "no"
            if lower_c == "no":
                if correct.isupper(): return "YES"
                if correct[0].isupper(): return "Yes"
                return "yes"
        
        # 若都不匹配
        return correct + "_WRONG"