# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   排序结果：序列排序后第k位的元素是什么
# ============================================================

from .base import Game
import random
import itertools


class KthElementGame(Game):

    game_rule_zh = """\
我们现在来玩一个"第 k 大元素推理"游戏，规则如下：

游戏设定了一个包含 {n} 个元素的集合，每个元素都有唯一的标签（编号 1 到 {n}）。我已经在心中为这些元素确定了一个严格的全序关系（没有任何两个元素相等），但这个顺序对你是隐藏的。你的目标是推断出这个序列中**第 {k} 大**的元素是哪一个。

你可以通过以下两种查询方式来收集信息（每次只能提出一个查询），我会根据隐藏的全序如实回答：

1. **成对比较查询**：询问两个元素 A 和 B 哪个更大。我会回答"A > B"或"B > A"。
2. **三元中位数查询**：询问三个元素 A、B、C 中哪个是中位数（按大小排序后居中的元素）。我会回答其中一个元素的标签。

当你收集到足够信息后，请提交你的最终答案。若答案错误或格式不符，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 成对比较查询（例如比较元素 1 和 3）：
<query_compare>1,3</query_compare>

- 三元中位数查询（例如查询元素 1、3、5 的中位数）：
<query_median>1,3,5</query_median>

提交最终答案时，直接给出你认为第 {k} 大的元素标签，格式如下：

<answer>5</answer>
"""

    game_rule_en = """\
Let's play a "k-th Element Inference" game. Here are the rules:

There is a set of {n} elements, each with a unique label (IDs from 1 to {n}). I have established a strict total order over these elements in my mind (no two elements are equal), but this order is hidden from you. Your goal is to infer which element is the **{k}-th largest** in this sequence.

You can collect information through the following two types of queries (one query per turn), and I will answer truthfully based on the hidden total order:

1. **Pairwise Comparison Query**: Ask which of two elements A and B is larger. I will answer "A > B" or "B > A".
2. **Ternary Median Query**: Ask which of three elements A, B, C is the median (the middle element when sorted by size). I will answer with one of the element labels.

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Pairwise Comparison Query (e.g., comparing elements 1 and 3):
<query_compare>1,3</query_compare>

- Ternary Median Query (e.g., querying the median of elements 1, 3, 5):
<query_median>1,3,5</query_median>

When submitting the final answer, directly provide the label of the element you believe is the {k}-th largest, using this format:

<answer>5</answer>
"""

    contextualized_rule_zh_1 = """\
我们现在来进行"路口拥堵度评估"任务，规则如下：

系统监控了 {n} 个关键交通路口（编号 1 到 {n}）。根据当前的实时车流量，这些路口存在一个严格的拥堵度排名（没有任何两个路口拥堵度完全相同），但具体排名对你是隐藏的。你的目标是排查出拥堵严重程度排在**第 {k} 位**的路口编号，以便合理调度交警。

你可以通过以下两种查询方式调用交通控制中心的大数据系统（每次只能提出一个查询），系统会如实返回结果：

1. **成对比较查询**：对比路口 A 和 B 哪个更拥堵。系统会回答"A > B"或"B > A"。
2. **三元中位数查询**：输入三个路口 A、B、C，系统会评估并回答这三个路口中拥堵度处于中间水平的路口编号。

当你收集到足够信息后，请提交你的最终答案。若答案错误或格式不符，排查失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个编号。请使用以下 XML 格式：

- 成对比较查询（例如对比路口 1 和 3）：
<query_compare>1,3</query_compare>

- 三元中位数查询（例如查询路口 1、3、5 的中位路口）：
<query_median>1,3,5</query_median>

提交最终答案时，直接给出你认为符合条件的编号，格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's execute the "Intersection Congestion Assessment" task. Here are the rules:

The system is monitoring {n} key traffic intersections (IDs from 1 to {n}). Based on real-time traffic volume, there is a strict congestion ranking among them (no two intersections have the exact same congestion level), but this ranking is hidden from you. Your goal is to identify the intersection with the **{k}-th highest** congestion level to dispatch traffic police efficiently.

You can query the traffic control center's big data system using the following two methods (one query per turn), and the system will answer truthfully:

1. **Pairwise Comparison Query**: Compare intersections A and B to see which is more congested. The system will answer "A > B" or "B > A".
2. **Ternary Median Query**: Input three intersections A, B, C, and the system will evaluate and answer with the ID of the intersection with the median congestion level among them.

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the assessment fails.

## Query and Answer Format (strictly required)

Each query must contain only one ID. Use the following XML format:

- Pairwise Comparison Query (e.g., comparing intersections 1 and 3):
<query_compare>1,3</query_compare>

- Ternary Median Query (e.g., querying the median of intersections 1, 3, 5):
<query_median>1,3,5</query_median>

When submitting the final answer, directly provide the ID you believe meets the criteria, using this format:

<answer>5</answer>
"""

    contextualized_rule_zh_2 = """\
我们现在来进行"急诊患者分诊排队"任务，规则如下：

急诊室当前接诊了 {n} 名患者（编号 1 到 {n}）。医疗系统根据患者的生命体征计算出了一个严格的病情危重度排名（没有任何两名患者危重度完全相同），但具体顺序对你是隐藏的。你的目标是推断出危重程度排在**第 {k} 位**的患者编号，以安排对应级别的抢救资源。

你可以通过以下两种方式向主治医师或专家组发起咨询（每次只能提出一个查询），系统会如实返回结果：

1. **成对比较查询**：询问患者 A 和 B 谁的病情更危重。系统会回答"A > B"或"B > A"。
2. **三元中位数查询**：提交三名患者 A、B、C，专家组会评估并回答这三人中危重度居中的患者编号。

当你收集到足够信息后，请提交你的最终答案。若答案错误或格式不符，分诊失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个编号。请使用以下 XML 格式：

- 成对比较查询（例如对比患者 1 和 3）：
<query_compare>1,3</query_compare>

- 三元中位数查询（例如查询患者 1、3、5 的中位患者）：
<query_median>1,3,5</query_median>

提交最终答案时，直接给出你认为符合条件的编号，格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's execute the "ER Patient Triage Priority" task. Here are the rules:

There are currently {n} patients (IDs from 1 to {n}) waiting in the emergency room. The medical system has calculated a strict critical severity ranking based on their vital signs (no two patients have the exact same severity), but this ranking is hidden from you. Your goal is to infer the ID of the patient with the **{k}-th highest** critical severity to allocate appropriate resuscitation resources.

You can consult the lead physician or expert panel through the following two methods (one query per turn), and the system will answer truthfully:

1. **Pairwise Comparison Query**: Ask which of patient A and B is in a more critical condition. The system will answer "A > B" or "B > A".
2. **Ternary Median Query**: Submit three patients A, B, C, and the panel will evaluate and answer with the ID of the patient with the median severity among them.

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the triage fails.

## Query and Answer Format (strictly required)

Each query must contain only one ID. Use the following XML format:

- Pairwise Comparison Query (e.g., comparing patients 1 and 3):
<query_compare>1,3</query_compare>

- Ternary Median Query (e.g., querying the median of patients 1, 3, 5):
<query_median>1,3,5</query_median>

When submitting the final answer, directly provide the ID you believe meets the criteria, using this format:

<answer>5</answer>
"""

    contextualized_rule_zh_3 = """\
我们现在来进行"学生成绩位次推断"任务，规则如下：

在最近的一次标准化模考中，有 {n} 名学生（学号 1 到 {n}）参加了考试。教务系统记录了他们严格的总分排名（没有任何两名学生总分相同），但为了隐私保护，具体排名对你是隐藏的。你的目标是推断出总成绩排在**第 {k} 名**的学生学号，以进行针对性的学术辅导。

你可以通过以下两种查询方式调用教务系统的分析接口（每次只能提出一个查询），系统会如实返回结果：

1. **成对比较查询**：对比学生 A 和 B 谁的成绩更好。系统会回答"A > B"或"B > A"。
2. **三元中位数查询**：输入三名学生 A、B、C，系统会评估并回答这三人中成绩处于中位数的学生学号。

当你收集到足够信息后，请提交你的最终答案。若答案错误或格式不符，推断失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个学号。请使用以下 XML 格式：

- 成对比较查询（例如对比学生 1 和 3）：
<query_compare>1,3</query_compare>

- 三元中位数查询（例如查询学生 1、3、5 的中位学号）：
<query_median>1,3,5</query_median>

提交最终答案时，直接给出你认为符合条件的学号，格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's execute the "Student Academic Rank Inference" task. Here are the rules:

In a recent standardized mock exam, {n} students (IDs from 1 to {n}) participated. The academic system has recorded their strict total score ranking (no two students have the exact same total score), but for privacy reasons, this ranking is hidden from you. Your goal is to infer the ID of the student who ranks **{k}-th** overall to provide targeted academic tutoring.

You can call the academic system's analysis interface using the following two query methods (one query per turn), and the system will answer truthfully:

1. **Pairwise Comparison Query**: Compare student A and B to see who has a better score. The system will answer "A > B" or "B > A".
2. **Ternary Median Query**: Input three students A, B, C, and the system will evaluate and answer with the ID of the student with the median score among them.

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the inference fails.

## Query and Answer Format (strictly required)

Each query must contain only one ID. Use the following XML format:

- Pairwise Comparison Query (e.g., comparing students 1 and 3):
<query_compare>1,3</query_compare>

- Ternary Median Query (e.g., querying the median of students 1, 3, 5):
<query_median>1,3,5</query_median>

When submitting the final answer, directly provide the ID you believe meets the criteria, using this format:

<answer>5</answer>
"""

    contextualized_rule_zh_4 = """\
我们现在来进行"生产批次次品率溯源"任务，规则如下：

质检部门抽取了 {n} 个生产批次的产品（批次编号 1 到 {n}）。根据抽检结果，这些批次存在一个严格的次品率排名（没有任何两个批次次品率完全相等），但具体的缺陷分布顺序对你是隐藏的。你的目标是排查出次品率高居**第 {k} 位**的生产批次，以便进行工艺复盘。

你可以通过以下两种查询方式调用质量控制实验室的复测接口（每次只能提出一个查询），系统会如实返回结果：

1. **成对比较查询**：对比批次 A 和 B 哪个次品率更高。系统会回答"A > B"或"B > A"。
2. **三元中位数查询**：送检三个批次 A、B、C，实验室会评估并回答这三个批次中次品率居中的批次编号。

当你收集到足够信息后，请提交你的最终答案。若答案错误或格式不符，溯源失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个编号。请使用以下 XML 格式：

- 成对比较查询（例如对比批次 1 和 3）：
<query_compare>1,3</query_compare>

- 三元中位数查询（例如查询批次 1、3、5 的中位批次）：
<query_median>1,3,5</query_median>

提交最终答案时，直接给出你认为符合条件的编号，格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's execute the "Production Batch Defect Rate Tracing" task. Here are the rules:

The quality inspection department has sampled products from {n} production batches (Batch IDs from 1 to {n}). Based on the inspection results, there is a strict defect rate ranking among these batches (no two batches have the exact same defect rate), but the specific distribution order is hidden from you. Your goal is to identify the batch with the **{k}-th highest** defect rate for process review.

You can call the quality control laboratory's retesting interface using the following two query methods (one query per turn), and the system will answer truthfully:

1. **Pairwise Comparison Query**: Compare batch A and B to see which has a higher defect rate. The system will answer "A > B" or "B > A".
2. **Ternary Median Query**: Submit three batches A, B, C, and the laboratory will evaluate and answer with the ID of the batch with the median defect rate among them.

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the tracing fails.

## Query and Answer Format (strictly required)

Each query must contain only one ID. Use the following XML format:

- Pairwise Comparison Query (e.g., comparing batches 1 and 3):
<query_compare>1,3</query_compare>

- Ternary Median Query (e.g., querying the median of batches 1, 3, 5):
<query_median>1,3,5</query_median>

When submitting the final answer, directly provide the ID you believe meets the criteria, using this format:

<answer>5</answer>
"""

    contextualized_rule_zh_5 = """\
我们现在来进行"诉讼证据证明力评估"任务，规则如下：

在当前的复杂商业诉讼中，原被告双方共提交了 {n} 份关键证据（证据编号 1 到 {n}）。合议庭已在内部对这些证据的确证力（证明力）形成了严格的权重排名（没有任何两份证据权重完全等同），但该排名目前属于审判机密，对你是隐藏的。你的目标是推断出证明力排在**第 {k} 位**的证据编号，以优化我方的质证策略。

你可以通过以下两种查询方式向模拟法庭系统进行推演（每次只能提出一个查询），系统会如实返回结果：

1. **成对比较查询**：对比证据 A 和 B 哪个证明力更强。系统会回答"A > B"或"B > A"。
2. **三元中位数查询**：提交三份证据 A、B、C，模拟法庭会评估并回答这三份证据中证明力居中的证据编号。

当你收集到足够信息后，请提交你的最终答案。若答案错误或格式不符，评估失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个编号。请使用以下 XML 格式：

- 成对比较查询（例如对比证据 1 和 3）：
<query_compare>1,3</query_compare>

- 三元中位数查询（例如查询证据 1、3、5 的中位证据）：
<query_median>1,3,5</query_median>

提交最终答案时，直接给出你认为符合条件的编号，格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's execute the "Litigation Evidence Probative Value Assessment" task. Here are the rules:

In the current complex commercial litigation, the plaintiff and defendant have submitted a total of {n} key pieces of evidence (Evidence IDs from 1 to {n}). The collegial panel has internally formed a strict weight ranking of the probative value of these exhibits (no two exhibits have the exact same weight), but this ranking is currently a trial secret and hidden from you. Your goal is to infer the evidence ID with the **{k}-th highest** probative value to optimize our cross-examination strategy.

You can run deductions through the moot court system using the following two query methods (one query per turn), and the system will answer truthfully:

1. **Pairwise Comparison Query**: Compare evidence A and B to see which has stronger probative value. The system will answer "A > B" or "B > A".
2. **Ternary Median Query**: Submit three exhibits A, B, C, and the moot court will evaluate and answer with the ID of the exhibit with the median probative value among them.

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the assessment fails.

## Query and Answer Format (strictly required)

Each query must contain only one ID. Use the following XML format:

- Pairwise Comparison Query (e.g., comparing evidence 1 and 3):
<query_compare>1,3</query_compare>

- Ternary Median Query (e.g., querying the median of evidence 1, 3, 5):
<query_median>1,3,5</query_median>

When submitting the final answer, directly provide the ID you believe meets the criteria, using this format:

<answer>5</answer>
"""

    tags = ["answer", "query_compare", "query_median"]
    
    reasoning_type = "演绎推理"
    data_structure = "序列"

    # 难度说明：
    # 1 (简单)      - N=5, k=3 (中位数，最容易定位)
    # 2 (中等偏下)  - N=7, k=2 (次大元素)
    # 3 (中等偏上)  - N=9, k=5 (中等大小集合的中位数)
    # 4 (较难)      - N=12, k=4 (较大集合，非中位位置)
    # 5 (难)        - N=15, k=11 (大集合，靠后位置)

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "k": 3,
                "order": [3, 1, 5, 2, 4],  # 从大到小的顺序，第3大是5
            },
            2: {
                "n": 7,
                "k": 2,
                "order": [4, 6, 2, 7, 1, 3, 5],  # 第2大是6
            },
            3: {
                "n": 9,
                "k": 5,
                "order": [7, 3, 9, 2, 5, 1, 8, 4, 6],  # 第5大是5
            },
            4: {
                "n": 12,
                "k": 4,
                "order": [8, 11, 3, 7, 1, 9, 12, 5, 2, 10, 4, 6],  # 第4大是7
            },
            5: {
                "n": 15,
                "k": 11,
                "order": [12, 7, 14, 3, 9, 1, 15, 6, 11, 4, 8, 13, 2, 5, 10],  # 第11大是8
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
                "order": [4, 6, 2, 7, 1, 3, 5],
            },
            3: {
                "n": 9,
                "k": 5,
                "order": [7, 3, 9, 2, 5, 1, 8, 4, 6],
            },
            4: {
                "n": 12,
                "k": 4,
                "order": [8, 11, 3, 7, 1, 9, 12, 5, 2, 10, 4, 6],
            },
            5: {
                "n": 15,
                "k": 11,
                "order": [12, 7, 14, 3, 9, 1, 15, 6, 11, 4, 8, 13, 2, 5, 10],
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
        self._game_info["n"] = cfg["n"]
        self._game_info["k"] = cfg["k"]
        
        # order[i] 表示第 i+1 大的元素标签
        # 例如 order = [3, 1, 5] 表示：最大的是3，第二大是1，第三大是5
        self.order = cfg["order"]
        
        # 构建排名字典：element -> rank (1-indexed, 1是最大)
        self.rank_map = {}
        for rank, element in enumerate(self.order, start=1):
            self.rank_map[element] = rank
        
        # 第k大的答案
        self.correct_answer = self.order[cfg["k"] - 1]

    def evaluate(self, parsed_info):
        # 解析答案
        try:
            answer = int(parsed_info["answer"].strip())
        except:
            return False
        
        # 检查答案是否正确
        return answer == self.correct_answer

    def _cf_core_produce(self, parsed_info):
        # 优先处理成对比较查询
        if "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError("Expected exactly 2 elements")
                
                id1, id2 = int(parts[0]), int(parts[1])
                
                # 检查元素是否在有效范围内
                if id1 not in self.rank_map or id2 not in self.rank_map:
                    return "错误：元素标签超出范围。" if self.config.language == "zh" else "Error: Element label out of range."
                
                if id1 == id2:
                    return "错误：不能比较相同的元素。" if self.config.language == "zh" else "Error: Cannot compare the same element."
                
                # 比较：rank越小表示越大
                if self.rank_map[id1] < self.rank_map[id2]:
                    return f"{id1} > {id2}"
                else:
                    return f"{id2} > {id1}"
                    
            except (ValueError, TypeError, KeyError):
                return "错误：格式无效或元素标签错误。" if self.config.language == "zh" else "Error: Invalid format or element label."
        
        # 处理三元中位数查询
        elif "query_median" in parsed_info:
            try:
                raw = parsed_info["query_median"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 3:
                    raise ValueError("Expected exactly 3 elements")
                
                id1, id2, id3 = int(parts[0]), int(parts[1]), int(parts[2])
                
                # 检查元素是否在有效范围内
                if id1 not in self.rank_map or id2 not in self.rank_map or id3 not in self.rank_map:
                    return "错误：元素标签超出范围。" if self.config.language == "zh" else "Error: Element label out of range."
                
                # 检查是否有重复
                if len(set([id1, id2, id3])) != 3:
                    return "错误：三个元素必须各不相同。" if self.config.language == "zh" else "Error: Three elements must be distinct."
                
                # 找到中位数：按rank排序后取中间的
                elements = [(self.rank_map[id1], id1), (self.rank_map[id2], id2), (self.rank_map[id3], id3)]
                elements.sort()  # 按rank排序
                median_element = elements[1][1]  # 取中间的元素标签
                
                if self.config.language == "zh":
                    return f"中位：{median_element}"
                else:
                    return f"Median: {median_element}"
                    
            except (ValueError, TypeError, KeyError):
                return "错误：格式无效或元素标签错误。" if self.config.language == "zh" else "Error: Invalid format or element label."
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        # 处理成对比较响应，形如 "A > B"
        if " > " in correct:
            parts = correct.split(" > ")
            if len(parts) == 2:
                # 反转比较结果
                return f"{parts[1]} > {parts[0]}"
        
        # 处理中位数响应
        # 中文格式: "中位：X"
        if correct.startswith("中位："):
            median_val = correct[len("中位："):].strip()
            try:
                val = int(median_val)
                # 选一个不同的有效元素作为错误中位数
                candidates = [e for e in self.rank_map.keys() if e != val]
                if candidates:
                    wrong_val = random.choice(candidates)
                    return f"中位：{wrong_val}"
            except ValueError:
                pass
        
        # 英文格式: "Median: X"
        if correct.startswith("Median: "):
            median_val = correct[len("Median: "):].strip()
            try:
                val = int(median_val)
                candidates = [e for e in self.rank_map.keys() if e != val]
                if candidates:
                    wrong_val = random.choice(candidates)
                    return f"Median: {wrong_val}"
            except ValueError:
                pass
        
        # 若都不匹配
        return correct + "_WRONG"

    def get_all_possible_queries(self):
        queries = []
        # 获取所有元素ID并排序，保证顺序一致性
        ids = sorted(list(self.rank_map.keys()))
        
        # 1. 成对比较查询
        # 枚举所有由不同元素组成的对
        for a, b in itertools.combinations(ids, 2):
            # 构造内部处理所需的解析信息
            query_content = f"{a},{b}"
            parsed_info = {"query_compare": query_content}
            # 调用核心逻辑获取正确答案
            answer = self._cf_core_produce(parsed_info)
            # 构造完整的XML查询字符串
            query_str = f"<query_compare>{query_content}</query_compare>"
            
            queries.append({
                "query": query_str,
                "answer": answer
            })
        
        # 2. 三元中位数查询
        # 枚举所有由三个不同元素组成的组合
        for a, b, c in itertools.combinations(ids, 3):
            query_content = f"{a},{b},{c}"
            parsed_info = {"query_median": query_content}
            answer = self._cf_core_produce(parsed_info)
            query_str = f"<query_median>{query_content}</query_median>"
            
            queries.append({
                "query": query_str,
                "answer": answer
            })
            
        return queries