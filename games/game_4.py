from .base import Game
import re

class TernaryMarkingEquivalenceGame(Game):

    game_rule_zh = """\
我们来玩一个"三值标记等价判定"的推理游戏，规则如下：

游戏设定了一个包含 {n} 个元素的集合 S，编号为 1 到 {n}。我已秘密为每个元素指定了一个标记值，标记值只有三种可能：1、2 或 3。每个元素恰有且仅有一个标记值，且标记在游戏过程中保持不变。

游戏指定了两个特殊的目标元素：T1（编号 {t1}）和 T2（编号 {t2}）。

你的目标是：判断 T1 和 T2 的标记值是否相同，并给出最终结论。

你可以进行以下查询（每次仅限一个查询）：

**相同性查询**：询问任意两个不同元素 i 和 j 的标记值是否相同。我会回答"是"或"否"。

**重要约束**：你不能直接查询 T1 和 T2 是否标记相同（即禁止查询 Same({t1},{t2})）。除此之外，你可以查询集合中任意其他成对元素的标记关系。

当你收集到足够信息后，请提交最终答案。你的答案必须是逻辑必然的结论，即在所有与已知查询结果一致的标记分配方案中，T1 和 T2 的关系都是确定的。

每次查询请使用以下 XML 格式：

- 相同性查询（例如查询编号 1 和 3 是否标记相同）：
<query_same>1,3</query_same>

提交最终答案时，请说明 T1 和 T2 的标记是否相同，使用以下格式之一：

- 如果认为 T1 和 T2 标记相同：
<answer>Equal</answer>

- 如果认为 T1 和 T2 标记不同：
<answer>NotEqual</answer>
"""

    game_rule_en = """\
Let's play a "Ternary Marking Equivalence" deduction game. Here are the rules:

There is a set S containing {n} elements, numbered from 1 to {n}. I have secretly assigned each element a marking value from three possible values: 1, 2, or 3. Each element has exactly one marking value, and the marking remains constant throughout the game.

The game specifies two special target elements: T1 (ID {t1}) and T2 (ID {t2}).

Your goal is: to determine whether T1 and T2 have the same marking value, and provide a final conclusion.

You can perform the following queries (one per turn):

**Sameness Query**: Ask whether any two different elements i and j have the same marking value. I will answer "Yes" or "No".

**Important Constraint**: You cannot directly query whether T1 and T2 have the same marking (i.e., querying Same({t1},{t2}) is forbidden). Apart from this, you can query the marking relationship between any other pair of elements in the set.

When you have gathered sufficient information, submit your final answer. Your answer must be a logically necessary conclusion, meaning that across all marking assignment schemes consistent with the known query results, the relationship between T1 and T2 is determined.

For each query, use the following XML format:

- Sameness Query (e.g., querying if ID 1 and 3 have the same marking):
<query_same>1,3</query_same>

When submitting the final answer, specify whether T1 and T2 have the same marking, using one of the following formats:

- If you believe T1 and T2 have the same marking:
<answer>Equal</answer>

- If you believe T1 and T2 have different markings:
<answer>NotEqual</answer>
"""

    contextualized_rule_zh_1 = """\
[交通场景]
我们来使用"信号频段诊断系统"进行一项排查任务，规则如下：

交通网络中包含 {n} 个信号灯控制器，编号为 1 到 {n}。我已秘密为每个控制器分配了一个信号频段，频段只有三种可能：频段A、频段B 或 频段C。每个控制器恰有且仅有一个频段，且在排查过程中保持不变。

系统指定了两个关键目标控制器：T1（编号 {t1}）和 T2（编号 {t2}）。

你的目标是：判断 T1 和 T2 是否使用相同的信号频段，并给出最终结论。

你可以进行以下查询（每次仅限一个查询）：

**同频查询**：询问任意两个不同控制器 i 和 j 的信号频段是否相同。我会回答"是"或"否"。

**重要约束**：由于安全隔离限制，你不能直接查询 T1 和 T2 是否同频（即禁止查询 Same({t1},{t2})）。除此之外，你可以查询网络中任意其他成对控制器的频段关系。

当你收集到足够信息后，请提交最终答案。你的答案必须是逻辑必然的结论，即在所有与已知查询结果一致的频段分配方案中，T1 和 T2 的关系都是确定的。

每次查询请使用以下 XML 格式：

- 同频查询（例如查询控制器 1 和 3 是否同频）：
<query_same>1,3</query_same>

提交最终答案时，请说明 T1 和 T2 的频段是否相同，使用以下格式之一：

- 如果认为 T1 和 T2 频段相同：
<answer>Equal</answer>

- 如果认为 T1 和 T2 频段不同：
<answer>NotEqual</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's perform an inspection task using the "Signal Frequency Band Diagnostic System". Here are the rules:

The traffic network contains {n} signal controllers, numbered from 1 to {n}. I have secretly assigned each controller a signal frequency band from three possible networks: Band A, Band B, or Band C. Each controller has exactly one frequency band, and the assignment remains constant throughout the inspection.

The system specifies two critical target controllers: T1 (ID {t1}) and T2 (ID {t2}).

Your goal is: to determine whether T1 and T2 operate on the same signal frequency band, and provide a final conclusion.

You can perform the following queries (one per turn):

**Co-frequency Query**: Ask whether any two different controllers i and j have the same frequency band. I will answer "Yes" or "No".

**Important Constraint**: Due to safety isolation limits, you cannot directly query whether T1 and T2 share the same band (i.e., querying Same({t1},{t2}) is forbidden). Apart from this, you can query the frequency band relationship between any other pair of controllers in the network.

When you have gathered sufficient information, submit your final answer. Your answer must be a logically necessary conclusion, meaning that across all frequency assignment schemes consistent with the known query results, the relationship between T1 and T2 is determined.

For each query, use the following XML format:

- Co-frequency Query (e.g., querying if controllers 1 and 3 share the same band):
<query_same>1,3</query_same>

When submitting the final answer, specify whether T1 and T2 have the same frequency band, using one of the following formats:

- If you believe T1 and T2 share the same band:
<answer>Equal</answer>

- If you believe T1 and T2 have different bands:
<answer>NotEqual</answer>
"""

    contextualized_rule_zh_2 = """\
[医疗场景]
我们来使用"病毒分型交叉比对系统"进行流行病学调查，规则如下：

样本库中包含 {n} 份患者血液样本，编号为 1 到 {n}。我已秘密确认了每份样本中含有的未知病毒分型，分型只有三种可能：型α、型β 或 型γ。每份样本恰好只包含一种病毒分型，且在调查过程中保持不变。

疾控中心指定了两份疑似零号病人的关键样本：T1（编号 {t1}）和 T2（编号 {t2}）。

你的目标是：判断 T1 和 T2 是否感染了相同分型的病毒，并给出最终结论。

你可以进行以下查询（每次仅限一个查询）：

**同型比对查询**：询问任意两份不同样本 i 和 j 的病毒分型是否相同。我会回答"是"或"否"。

**重要约束**：由于试剂排斥风险，你不能直接比对 T1 和 T2 的分型是否相同（即禁止查询 Same({t1},{t2})）。除此之外，你可以比对样本库中任意其他成对样本的分型关系。

当你收集到足够信息后，请提交最终答案。你的答案必须是逻辑必然的结论，即在所有与已知查询结果一致的分型分配方案中，T1 和 T2 的关系都是确定的。

每次查询请使用以下 XML 格式：

- 同型比对查询（例如查询样本 1 和 3 分型是否相同）：
<query_same>1,3</query_same>

提交最终答案时，请说明 T1 和 T2 的病毒分型是否相同，使用以下格式之一：

- 如果认为 T1 和 T2 分型相同：
<answer>Equal</answer>

- 如果认为 T1 和 T2 分型不同：
<answer>NotEqual</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct an epidemiological investigation using the "Viral Strain Cross-Matching System". Here are the rules:

The sample bank contains {n} patient blood samples, numbered from 1 to {n}. I have secretly confirmed the unknown viral strain present in each sample, which can only be one of three types: Type α, Type β, or Type γ. Each sample contains exactly one viral strain, and this remains constant throughout the investigation.

The CDC has designated two critical samples from suspected patient zeros: T1 (ID {t1}) and T2 (ID {t2}).

Your goal is: to determine whether T1 and T2 are infected with the same viral strain, and provide a final conclusion.

You can perform the following queries (one per turn):

**Strain Matching Query**: Ask whether any two different samples i and j contain the same viral strain. I will answer "Yes" or "No".

**Important Constraint**: Due to reagent rejection risks, you cannot directly cross-match T1 and T2 to see if they share the same strain (i.e., querying Same({t1},{t2}) is forbidden). Apart from this, you can query the strain relationship between any other pair of samples in the bank.

When you have gathered sufficient information, submit your final answer. Your answer must be a logically necessary conclusion, meaning that across all strain assignment schemes consistent with the known query results, the relationship between T1 and T2 is determined.

For each query, use the following XML format:

- Strain Matching Query (e.g., querying if samples 1 and 3 share the same strain):
<query_same>1,3</query_same>

When submitting the final answer, specify whether T1 and T2 have the same viral strain, using one of the following formats:

- If you believe T1 and T2 share the same strain:
<answer>Equal</answer>

- If you believe T1 and T2 have different strains:
<answer>NotEqual</answer>
"""

    contextualized_rule_zh_3 = """\
[教育场景]
我们来使用"盲审专家匹配系统"进行学术排查，规则如下：

系统库中包含 {n} 份匿名毕业论文，编号为 1 到 {n}。我已秘密为每份论文分配了盲审专家组，专家组只有三种可能：专家X、专家Y 或 专家Z。每份论文恰有且仅有一位专家进行评阅，且在排查过程中分配关系保持不变。

教务处指定了两份存在异常相似度的目标论文：T1（编号 {t1}）和 T2（编号 {t2}）。

你的目标是：判断 T1 和 T2 是否被分配给了同一位盲审专家，并给出最终结论。

你可以进行以下查询（每次仅限一个查询）：

**同组查询**：询问任意两份不同论文 i 和 j 的盲审专家是否相同。我会回答"是"或"否"。

**重要约束**：为避免打草惊蛇，你不能直接查询 T1 和 T2 是否由同一专家评阅（即禁止查询 Same({t1},{t2})）。除此之外，你可以查询库中任意其他成对论文的专家分配关系。

当你收集到足够信息后，请提交最终答案。你的答案必须是逻辑必然的结论，即在所有与已知查询结果一致的分配方案中，T1 和 T2 的关系都是确定的。

每次查询请使用以下 XML 格式：

- 同组查询（例如查询论文 1 和 3 的专家是否相同）：
<query_same>1,3</query_same>

提交最终答案时，请说明 T1 和 T2 的盲审专家是否相同，使用以下格式之一：

- 如果认为 T1 和 T2 专家相同：
<answer>Equal</answer>

- 如果认为 T1 和 T2 专家不同：
<answer>NotEqual</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct an academic inspection using the "Blind Review Expert Matching System". Here are the rules:

The system repository contains {n} anonymous graduation theses, numbered from 1 to {n}. I have secretly assigned a blind review expert to each thesis from three possible options: Expert X, Expert Y, or Expert Z. Each thesis is reviewed by exactly one expert, and the assignment remains constant throughout the inspection.

The academic affairs office has designated two target theses with abnormal similarities: T1 (ID {t1}) and T2 (ID {t2}).

Your goal is: to determine whether T1 and T2 were assigned to the same blind review expert, and provide a final conclusion.

You can perform the following queries (one per turn):

**Co-reviewer Query**: Ask whether any two different theses i and j share the same blind review expert. I will answer "Yes" or "No".

**Important Constraint**: To avoid alerting the individuals involved, you cannot directly query whether T1 and T2 are reviewed by the same expert (i.e., querying Same({t1},{t2}) is forbidden). Apart from this, you can query the expert assignment relationship between any other pair of theses in the repository.

When you have gathered sufficient information, submit your final answer. Your answer must be a logically necessary conclusion, meaning that across all expert assignment schemes consistent with the known query results, the relationship between T1 and T2 is determined.

For each query, use the following XML format:

- Co-reviewer Query (e.g., querying if theses 1 and 3 share the same expert):
<query_same>1,3</query_same>

When submitting the final answer, specify whether T1 and T2 share the same expert, using one of the following formats:

- If you believe T1 and T2 have the same expert:
<answer>Equal</answer>

- If you believe T1 and T2 have different experts:
<answer>NotEqual</answer>
"""

    contextualized_rule_zh_4 = """\
[制造业/工业场景]
我们来使用"产线批次溯源系统"进行缺陷排查，规则如下：

流水线上包含 {n} 个批次的精密零件，编号为 1 到 {n}。我已秘密记录了每个批次经过的热处理生产线，生产线只有三种可能：产线一、产线二 或 产线三。每个批次恰好只经过一条热处理生产线，且在溯源过程中记录保持不变。

质检部门指定了两个存在潜在缺陷的关键批次：T1（编号 {t1}）和 T2（编号 {t2}）。

你的目标是：判断 T1 和 T2 是否出自同一条热处理生产线，并给出最终结论。

你可以进行以下查询（每次仅限一个查询）：

**同线查询**：询问任意两个不同批次 i 和 j 是否经过了同一条生产线。我会回答"是"或"否"。

**重要约束**：由于数据权限锁定，你不能直接查询 T1 和 T2 是否出自同一产线（即禁止查询 Same({t1},{t2})）。除此之外，你可以查询流水线上任意其他成对批次的产线关系。

当你收集到足够信息后，请提交最终答案。你的答案必须是逻辑必然的结论，即在所有与已知查询结果一致的产线分配方案中，T1 和 T2 的关系都是确定的。

每次查询请使用以下 XML 格式：

- 同线查询（例如查询批次 1 和 3 是否出自同产线）：
<query_same>1,3</query_same>

提交最终答案时，请说明 T1 和 T2 的生产线是否相同，使用以下格式之一：

- 如果认为 T1 和 T2 生产线相同：
<answer>Equal</answer>

- 如果认为 T1 和 T2 生产线不同：
<answer>NotEqual</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's perform a defect troubleshooting using the "Production Line Batch Traceability System". Here are the rules:

The assembly line contains {n} batches of precision parts, numbered from 1 to {n}. I have secretly recorded the heat treatment production line each batch went through, from three possible lines: Line 1, Line 2, or Line 3. Each batch is processed by exactly one heat treatment line, and the record remains constant throughout the traceability process.

The quality control department has designated two critical batches with potential defects: T1 (ID {t1}) and T2 (ID {t2}).

Your goal is: to determine whether T1 and T2 originated from the same heat treatment production line, and provide a final conclusion.

You can perform the following queries (one per turn):

**Co-line Query**: Ask whether any two different batches i and j were processed on the same production line. I will answer "Yes" or "No".

**Important Constraint**: Due to data permission locks, you cannot directly query whether T1 and T2 come from the same line (i.e., querying Same({t1},{t2}) is forbidden). Apart from this, you can query the line relationship between any other pair of batches on the assembly line.

When you have gathered sufficient information, submit your final answer. Your answer must be a logically necessary conclusion, meaning that across all production line assignment schemes consistent with the known query results, the relationship between T1 and T2 is determined.

For each query, use the following XML format:

- Co-line Query (e.g., querying if batches 1 and 3 are from the same line):
<query_same>1,3</query_same>

When submitting the final answer, specify whether T1 and T2 have the same production line, using one of the following formats:

- If you believe T1 and T2 share the same line:
<answer>Equal</answer>

- If you believe T1 and T2 are from different lines:
<answer>NotEqual</answer>
"""

    contextualized_rule_zh_5 = """\
[法律场景]
我们来使用"法庭物证交叉验证系统"进行质证分析，规则如下：

证据清单中包含 {n} 份关键物证，编号为 1 到 {n}。我已秘密确认了负责每份物证的保管员身份，保管员只有三种可能：保管员A、保管员B 或 保管员C。每份物证恰由且仅由一位保管员负责，且在验证过程中该分配关系保持不变。

法庭指定了与核心案情最相关的两份物证：T1（编号 {t1}）和 T2（编号 {t2}）。

你的目标是：判断 T1 和 T2 的保管员是否是同一个人，并给出最终结论。

你可以进行以下查询（每次仅限一个查询）：

**同源查询**：询问任意两份不同物证 i 和 j 的保管员是否相同。我会回答"是"或"否"。

**重要约束**：根据回避原则，你不能直接对 T1 和 T2 的保管关系进行比对（即禁止查询 Same({t1},{t2})）。除此之外，你可以查询证据清单中任意其他成对物证的保管员关系。

当你收集到足够信息后，请提交最终答案。你的答案必须是逻辑必然的结论，即在所有与已知查询结果一致的保管分配方案中，T1 和 T2 的关系都是确定的。

每次查询请使用以下 XML 格式：

- 同源查询（例如查询物证 1 和 3 的保管员是否相同）：
<query_same>1,3</query_same>

提交最终答案时，请说明 T1 和 T2 的保管员是否相同，使用以下格式之一：

- 如果认为 T1 和 T2 保管员相同：
<answer>Equal</answer>

- 如果认为 T1 和 T2 保管员不同：
<answer>NotEqual</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct a cross-examination analysis using the "Court Evidence Cross-Validation System". Here are the rules:

The evidence inventory contains {n} key pieces of physical evidence, numbered from 1 to {n}. I have secretly confirmed the identity of the custodian responsible for each piece of evidence, from three possible custodians: Custodian A, Custodian B, or Custodian C. Each piece of evidence is managed by exactly one custodian, and this assignment remains constant throughout the validation process.

The court has designated two pieces of evidence most relevant to the core case: T1 (ID {t1}) and T2 (ID {t2}).

Your goal is: to determine whether T1 and T2 share the same custodian, and provide a final conclusion.

You can perform the following queries (one per turn):

**Co-custodian Query**: Ask whether any two different pieces of evidence i and j have the same custodian. I will answer "Yes" or "No".

**Important Constraint**: In accordance with the recusal principle, you cannot directly cross-match the custody relationship between T1 and T2 (i.e., querying Same({t1},{t2}) is forbidden). Apart from this, you can query the custodian relationship between any other pair of evidence in the inventory.

When you have gathered sufficient information, submit your final answer. Your answer must be a logically necessary conclusion, meaning that across all custody assignment schemes consistent with the known query results, the relationship between T1 and T2 is determined.

For each query, use the following XML format:

- Co-custodian Query (e.g., querying if evidence 1 and 3 share the same custodian):
<query_same>1,3</query_same>

When submitting the final answer, specify whether T1 and T2 have the same custodian, using one of the following formats:

- If you believe T1 and T2 share the same custodian:
<answer>Equal</answer>

- If you believe T1 and T2 have different custodians:
<answer>NotEqual</answer>
"""

    tags = ["answer", "query_same"]

    reasoning_type = "演绎推理"
    data_structure = "集合"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "t1": "1",
                "t2": "3",
                "assignments": "1=1,2=1,3=2,4=3",
            },
            2: {
                "n": 5,
                "t1": "2",
                "t2": "4",
                "assignments": "1=1,2=2,3=2,4=2,5=3",
            },
            3: {
                "n": 6,
                "t1": "1",
                "t2": "4",
                "assignments": "1=1,2=1,3=2,4=2,5=3,6=3",
            },
            4: {
                "n": 7,
                "t1": "2",
                "t2": "5",
                "assignments": "1=1,2=2,3=2,4=1,5=2,6=3,7=3",
            },
            5: {
                "n": 8,
                "t1": "3",
                "t2": "7",
                "assignments": "1=1,2=1,3=2,4=2,5=3,6=3,7=3,8=1",
            },
        },
        "en": {
            1: {
                "n": 4,
                "t1": "1",
                "t2": "3",
                "assignments": "1=1,2=1,3=2,4=3",
            },
            2: {
                "n": 5,
                "t1": "2",
                "t2": "4",
                "assignments": "1=1,2=2,3=2,4=2,5=3",
            },
            3: {
                "n": 6,
                "t1": "1",
                "t2": "4",
                "assignments": "1=1,2=1,3=2,4=2,5=3,6=3",
            },
            4: {
                "n": 7,
                "t1": "2",
                "t2": "5",
                "assignments": "1=1,2=2,3=2,4=1,5=2,6=3,7=3",
            },
            5: {
                "n": 8,
                "t1": "3",
                "t2": "7",
                "assignments": "1=1,2=1,3=2,4=2,5=3,6=3,7=3,8=1",
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
        self._game_info["t1"] = cfg["t1"]
        self._game_info["t2"] = cfg["t2"]
        
        self.marking_map = {}
        for pair in cfg["assignments"].split(","):
            idx, mark = pair.split("=")
            self.marking_map[idx.strip()] = mark.strip()
        
        self.t1 = cfg["t1"]
        self.t2 = cfg["t2"]
        
        self.ground_truth = (self.marking_map[self.t1] == self.marking_map[self.t2])

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        if raw_ans == "Equal":
            return self.ground_truth is True
        elif raw_ans == "NotEqual":
            return self.ground_truth is False
        else:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：查询格式无效，请使用格式 <query_same>i,j</query_same>"
            error_range = "错误：元素编号超出范围。"
            error_same = "错误：不能查询相同的元素。"
            error_forbidden = "错误：禁止直接查询 T1 和 T2 的关系！"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid query format. Use <query_same>i,j</query_same>"
            error_range = "Error: Element ID out of range."
            error_same = "Error: Cannot query the same element."
            error_forbidden = "Error: Direct query of T1 and T2 is forbidden!"

        if "query_same" in parsed_info:
            try:
                raw = parsed_info["query_same"].strip()
                parts = [x.strip() for x in raw.split(",")]
                
                if len(parts) != 2:
                    return error_format
                
                id1, id2 = parts[0], parts[1]
                
                if id1 not in self.marking_map or id2 not in self.marking_map:
                    return error_range
                
                if id1 == id2:
                    return error_same
                
                if (id1 == self.t1 and id2 == self.t2) or (id1 == self.t2 and id2 == self.t1):
                    return error_forbidden
                
                same = (self.marking_map[id1] == self.marking_map[id2])
                return yes_res if same else no_res
                
            except Exception as e:
                return error_format
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        if correct.lower() == "yes":
            if correct == "Yes": return "No"
            if correct == "YES": return "NO"
            return "no"
        if correct.lower() == "no":
            if correct == "No": return "Yes"
            if correct == "NO": return "YES"
            return "yes"
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        elements = sorted(list(self.marking_map.keys()), key=lambda x: int(x))
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        for i in range(len(elements)):
            for j in range(i + 1, len(elements)):
                id1, id2 = elements[i], elements[j]
                
                if (id1 == self.t1 and id2 == self.t2) or (id1 == self.t2 and id2 == self.t1):
                    continue
                
                is_same = (self.marking_map[id1] == self.marking_map[id2])
                correct_answer = yes_res if is_same else no_res
                
                queries.append({
                    "query": f"<query_same>{id1},{id2}</query_same>",
                    "answer": correct_answer
                })
                
        return queries