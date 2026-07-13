# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   条件首末位：满足某条件的第一个/最后一个元素在哪个位置
# ============================================================

from .base import Game
import math


class BoundaryDeductionGame(Game):

    game_rule_zh = """\
我们现在来玩一个"边界推理"游戏，规则如下：

游戏设定了一个有序索引集合 1 到 {n}。存在一个未知的边界位置 B，该边界将集合分为两部分：
- 所有小于 B 的位置，值为 False
- 所有大于等于 B 的位置，值为 True

你的目标是通过提问找出边界位置 B 的准确值。你可以进行以下两种操作：

1. 观察型提问：询问从位置 1 到位置 k 的范围内是否存在 True 值
   - 如果 k 大于等于边界 B，回答"是"
   - 如果 k 小于边界 B，回答"否"

2. 最终宣告：当你确定边界位置后，提交你的答案

注意：观察型提问的次数是有限的，请尽可能高效地找出边界位置。若提交的答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次只能包含一个操作标签。请使用以下 XML 格式：

- 观察型提问（例如询问位置 5）：
<query_observe>5</query_observe>

- 提交最终答案（例如边界位置为 7）：
<answer>7</answer>
"""

    game_rule_en = """\
Let's play a "Boundary Deduction" game. Here are the rules:

The game has an ordered index set from 1 to {n}. There exists an unknown boundary position B that divides the set into two parts:
- All positions less than B have the value False
- All positions greater than or equal to B have the value True

Your goal is to find the exact boundary position B through queries. You can perform the following two types of operations:

1. Observation Query: Ask whether there exists a True value in the range from position 1 to position k
   - If k is greater than or equal to boundary B, answer "Yes"
   - If k is less than boundary B, answer "No"

2. Final Declaration: When you have determined the boundary position, submit your answer

Note: The number of observation queries is limited, so please find the boundary position as efficiently as possible. If the submitted answer is incorrect or the format is invalid, the game fails.

## Query and Answer Format (must be strictly followed)

Each turn must contain only one operation tag. Use the following XML format:

- Observation Query (e.g., asking about position 5):
<query_observe>5</query_observe>

- Submit Final Answer (e.g., boundary position is 7):
<answer>7</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎进入智能交通调度系统。

我们监控的一条主干道被划分为连续的监测路段，编号从 1 到 {n}。系统检测到由于某处发生交通事故，导致形成了一个拥堵分界点 B。
- 在路段 B 之前的路段（即编号小于 B），交通状况畅通（视为 False）。
- 从路段 B 开始及之后的所有路段（即编号大于等于 B），均发生严重连环拥堵（视为 True）。

你的任务是通过最少次数的无人机巡查，精准定位拥堵起始路段 B 的编号，以便派遣交警处理。你可以进行以下两种系统指令：

1. 无人机巡查（观察型提问）：派遣无人机沿路巡查从路段 1 到路段 k 的范围，询问该范围内是否拍到了拥堵画面。
   - 如果巡查范围覆盖或超过了分界点 B（即 k 大于等于 B），系统反馈"是"（发现拥堵）。
   - 如果巡查范围完全在畅通路段（即 k 小于 B），系统反馈"否"（未发现拥堵）。

2. 事故定位（最终宣告）：当你确定了拥堵起始路段的位置后，提交该路段编号。

注意：受电池电量限制，无人机巡查次数有限，请高效排查。若提交的事故路段错误或指令格式不符，调度任务将失败。

## 系统指令与提交格式（必须严格遵守）

每次只能包含一个操作标签。请使用以下 XML 格式：

- 无人机巡查（例如巡查至第 5 路段）：
<query_observe>5</query_observe>

- 提交事故路段（例如拥堵始于第 7 路段）：
<answer>7</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Intelligent Traffic Dispatch System.

A main arterial road we are monitoring is divided into sequential segments indexed from 1 to {n}. The system detects that due to a traffic incident, a congestion boundary B has formed.
- All road segments before boundary B (index less than B) are clear and flowing normally (False).
- Starting from segment B and all subsequent segments (index greater than or equal to B), severe chain-reaction congestion has occurred (True).

Your task is to accurately pinpoint the index of the starting congestion segment B using the minimum number of drone patrols, so that traffic police can be dispatched. You can perform the following two system commands:

1. Drone Patrol (Observation Query): Deploy a drone to patrol the range from segment 1 to segment k, and ask whether congested conditions were captured in this range.
   - If the patrol range reaches or passes the boundary B (k >= B), the system answers "Yes" (congestion found).
   - If the patrol range is entirely within the clear segments (k < B), the system answers "No" (no congestion).

2. Incident Localization (Final Declaration): Once you have determined the exact starting segment of the congestion, submit its index.

Note: Due to battery constraints, drone patrol queries are limited. Please identify the incident segment efficiently. If the submitted segment is incorrect or the format is invalid, the dispatch mission fails.

## Command and Submission Format (must be strictly followed)

Each turn must contain only one operation tag. Use the following XML format:

- Drone Patrol (e.g., patrolling up to segment 5):
<query_observe>5</query_observe>

- Submit Incident Segment (e.g., congestion starts at segment 7):
<answer>7</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用临床靶向筛查系统。

患者的一条主要血管被划分为连续的监测节点，编号从 1 到 {n}。病理分析表明，存在一个病变起始节点 B。
- 在节点 B 之前的部位（编号小于 B），组织细胞反应正常（视为 False）。
- 从节点 B 开始及之后的所有节点（编号大于等于 B），均表现出病理性阻塞或异常反应（视为 True）。

你的目标是通过微创造影排查，精准定位病变起始节点 B 的位置，以制定手术方案。你可以执行以下两种操作：

1. 造影扫描（观察型提问）：对从节点 1 到节点 k 的血管段注入造影剂并扫描，询问该范围内是否检测到异常反应。
   - 如果扫描范围触及或越过了病变起点 B（即 k 大于等于 B），系统反馈"是"（检测到异常）。
   - 如果扫描范围完全处于健康组织（即 k 小于 B），系统反馈"否"（一切正常）。

2. 确诊病灶（最终宣告）：当你确定病变起始节点后，提交该节点编号。

注意：为防止造影剂过量，扫描次数有严格的上限，请以最高效率找出病灶。若提交的诊断错误或格式不规范，系统将判定医疗失误。

## 操作与提交格式（必须严格遵守）

每次只能包含一个操作标签。请使用以下 XML 格式：

- 造影扫描（例如扫描至节点 5）：
<query_observe>5</query_observe>

- 提交确诊节点（例如病灶始于节点 7）：
<answer>7</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Clinical Targeted Screening System.

A major blood vessel of the patient is divided into sequential monitoring nodes, indexed from 1 to {n}. Pathological analysis indicates there is a lesion starting node B.
- Tissues before node B (index less than B) show normal cellular responses (False).
- Starting from node B and all subsequent nodes (index greater than or equal to B), pathological obstruction or abnormal reactions are present (True).

Your goal is to accurately pinpoint the lesion starting node B through minimally invasive contrast imaging to formulate a surgical plan. You can perform two types of operations:

1. Contrast Imaging (Observation Query): Inject contrast agent and scan the vessel segment from node 1 to node k, asking if abnormal reactions are detected in this range.
   - If the scan range reaches or exceeds the lesion starting point B (k >= B), the system answers "Yes" (abnormality detected).
   - If the scan range is entirely within healthy tissue (k < B), the system answers "No" (all normal).

2. Diagnosis Confirmation (Final Declaration): Once you have determined the lesion starting node, submit its index.

Note: To prevent contrast agent overdose, the number of scans is strictly limited. Please locate the lesion with maximum efficiency. If the submitted diagnosis is incorrect or the format is invalid, it will be considered a medical error.

## Operation and Submission Format (must be strictly followed)

Each turn must contain only one operation tag. Use the following XML format:

- Contrast Imaging (e.g., scanning up to node 5):
<query_observe>5</query_observe>

- Submit Diagnosed Node (e.g., lesion starts at node 7):
<answer>7</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用自适应认知图谱系统。

本次测试包含一系列难度严格递增的题目，编号从 1 到 {n}。根据教育学模型，学生的知识掌握度存在一个确切的认知边界题号 B。
- 对于编号小于 B 的题目，学生都能完全理解并正确作答（视为 False）。
- 从编号 B 开始及其之后的所有更难题目，超出了学生的掌握范围，均会出现作答错误（视为 True）。

你的目标是通过抽查答题卡，精准找出该学生的认知边界题号 B。你可以进行以下两种操作：

1. 答题卡抽查（观察型提问）：批改从第 1 题到第 k 题的答卷，询问这一区间内是否出现了作答错误。
   - 如果批改范围包含了认知边界 B 及以上的题目（即 k 大于等于 B），系统反馈"是"（发现错误）。
   - 如果批改范围仅包含学生已掌握的简单题（即 k 小于 B），系统反馈"否"（全对，无错误）。

2. 边界判定（最终宣告）：当你准确定位到学生的认知边界后，提交该题号。

注意：为了提高评估效率，允许抽查的次数是有限的。若提交的认知边界错误或系统指令格式不符，评估任务将失败。

## 抽查与提交格式（必须严格遵守）

每次只能包含一个操作标签。请使用以下 XML 格式：

- 答题卡抽查（例如批阅至第 5 题）：
<query_observe>5</query_observe>

- 提交认知边界（例如边界题号为 7）：
<answer>7</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Adaptive Cognitive Mapping System.

This assessment contains a series of questions with strictly increasing difficulty, indexed from 1 to {n}. According to the educational model, the student's knowledge mastery has a specific cognitive boundary question B.
- For questions before B (index less than B), the student fully understands and answers them correctly (error status is False).
- Starting from question B and all subsequent harder questions, they exceed the student's mastery level, resulting in incorrect answers (error status is True).

Your goal is to accurately find the student's cognitive boundary B by spot-checking the answer sheets. You can perform the following two operations:

1. Answer Sheet Spot-check (Observation Query): Grade the responses from question 1 to question k, and ask whether any errors occurred within this range.
   - If the graded range includes the boundary B or beyond (k >= B), the system answers "Yes" (errors found).
   - If the graded range only contains simple questions the student has mastered (k < B), the system answers "No" (all correct, no errors).

2. Boundary Determination (Final Declaration): Once you have pinpointed the student's cognitive boundary, submit the question number.

Note: To improve assessment efficiency, the number of spot-checks is limited. If the submitted boundary is incorrect or the command format is invalid, the assessment task fails.

## Spot-check and Submission Format (must be strictly followed)

Each turn must contain only one operation tag. Use the following XML format:

- Answer Sheet Spot-check (e.g., grading up to question 5):
<query_observe>5</query_observe>

- Submit Cognitive Boundary (e.g., boundary question is 7):
<answer>7</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎访问工业流水线故障追踪系统。

本厂的自动化流水线包含按顺序执行的加工工序，编号从 1 到 {n}。质检部门报告，某道工序的设备发生偏移（故障点 B），导致连锁反应。
- 在故障工序 B 之前的环节（编号小于 B），加工出的半成品均符合标准（瑕疵状态为 False）。
- 从工序 B 开始，受故障设备影响，后续所有工序产出的产品均带有特定的超差瑕疵（瑕疵状态为 True）。

你的目标是通过在流水线上设置临时抽检点，快速定位出故障的起始工序 B。你可以进行以下两种操作：

1. 抽样检测（观察型提问）：在第 k 道工序后进行抽样（检验从工序 1 到 k 的累积加工结果），询问其中是否检测到了超差瑕疵。
   - 如果抽检点位于故障点 B 之后或正好在 B 处（即 k 大于等于 B），系统反馈"是"（发现瑕疵）。
   - 如果抽检点完全在正常工序阶段（即 k 小于 B），系统反馈"否"（产品合格）。

2. 锁定故障源（最终宣告）：当你确定了导致问题的原始工序后，提交该工序编号以便维修。

注意：每次抽检都需要暂停局部流水线，因此抽检次数有严格限制。若提交的故障点错误或指令不规范，排故任务失败。

## 抽检与报修格式（必须严格遵守）

每次只能包含一个操作标签。请使用以下 XML 格式：

- 抽样检测（例如在第 5 道工序后抽检）：
<query_observe>5</query_observe>

- 提交故障工序（例如故障源于第 7 道工序）：
<answer>7</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Industrial Assembly Line Fault Tracking System.

Our automated assembly line consists of sequential manufacturing processes, indexed from 1 to {n}. The quality control department reports that equipment at a specific process B has malfunctioned (fault point B), causing a chain reaction.
- For processes before B (index less than B), the semi-finished products meet the quality standards (defect status is False).
- Starting from process B, affected by the faulty equipment, all subsequent processes produce products with specific out-of-tolerance defects (defect status is True).

Your goal is to quickly locate the originating faulty process B by setting up temporary sampling points on the assembly line. You can perform two operations:

1. Sampling Inspection (Observation Query): Sample after the k-th process (inspecting the cumulative result from process 1 to k) and ask if out-of-tolerance defects are detected.
   - If the sampling point is at or after the fault point B (k >= B), the system answers "Yes" (defect found).
   - If the sampling point is entirely within the normal process stages (k < B), the system answers "No" (products qualified).

2. Fault Source Lock-in (Final Declaration): Once you have determined the original process causing the issue, submit its index for maintenance.

Note: Since each inspection requires pausing a section of the line, sampling queries are strictly limited. If the submitted fault point is incorrect or the command is invalid, the troubleshooting mission fails.

## Inspection and Maintenance Submission Format (must be strictly followed)

Each turn must contain only one operation tag. Use the following XML format:

- Sampling Inspection (e.g., sampling after process 5):
<query_observe>5</query_observe>

- Submit Faulty Process (e.g., fault originates at process 7):
<answer>7</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用智能法务卷宗审计系统。

本案涉及一份长达 {n} 页的商业合同，页面按条款时间顺序编号从 1 到 {n}。经举报，该合同被人在某一页（篡改起始页 B）开始恶意植入了隐藏的非法霸王条款。
- 在页面 B 之前的内容（页码小于 B），所有条款均合规合法（非法状态为 False）。
- 从页面 B 开始及之后的补充页（页码大于等于 B），均包含了衍生出的非法条款内容（非法状态为 True）。

作为法务审计员，你需要通过关键词检索，找出篡改发生的起始页码 B。你可以进行以下两种操作：

1. 卷宗检索（观察型提问）：使用系统检索从第 1 页到第 k 页的内容，询问该区间是否命中了非法条款的特征词。
   - 如果检索范围覆盖了被篡改的页面（即 k 大于等于 B），系统反馈"是"（命中非法内容）。
   - 如果检索范围完全是合规的早期页面（即 k 小于 B），系统反馈"否"（内容合规）。

2. 举证指控（最终宣告）：当你锁定第一处被篡改的页码后，提交该页码作为法庭证据。

注意：由于系统算力限制，高强度检索的次数是有限的。若提交的证据页码错误或格式不符合法务标准，审计将宣告失败。

## 检索与举证格式（必须严格遵守）

每次只能包含一个操作标签。请使用以下 XML 格式：

- 卷宗检索（例如检索前 5 页）：
<query_observe>5</query_observe>

- 提交非法起始页（例如篡改始于第 7 页）：
<answer>7</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Intelligent Legal Case Audit System.

This case involves a {n}-page commercial contract, with pages indexed chronologically from 1 to {n}. A whistleblower claims that hidden, illegal unfair terms were maliciously inserted starting from a specific page B.
- All content before page B (index less than B) is fully compliant and legal (illegal status is False).
- Starting from page B and all subsequent supplementary pages (index greater than or equal to B), the content contains derivative illegal terms (illegal status is True).

As a legal auditor, you must find the starting page B where the tampering occurred through keyword retrieval. You can perform the following two operations:

1. Case File Retrieval (Observation Query): Use the system to scan the content from page 1 to page k, asking if this range matches the characteristics of the illegal terms.
   - If the retrieval range covers the tampered pages (k >= B), the system answers "Yes" (illegal content matched).
   - If the retrieval range consists entirely of early compliant pages (k < B), the system answers "No" (content compliant).

2. Evidence Submission (Final Declaration): Once you have locked in the first tampered page, submit its index as court evidence.

Note: Due to system computing limits, high-intensity retrieval queries are limited. If the submitted evidence page is incorrect or the format does not meet legal standards, the audit will be declared a failure.

## Retrieval and Evidence Submission Format (must be strictly followed)

Each turn must contain only one operation tag. Use the following XML format:

- Case File Retrieval (e.g., scanning the first 5 pages):
<query_observe>5</query_observe>

- Submit Illegal Starting Page (e.g., tampering starts at page 7):
<answer>7</answer>
"""

    tags = ["answer", "query_observe"]
    
    reasoning_type = "演绎推理"
    data_structure = "序列"

    # 难度配置说明：
    # 1 (简单)       - N=8,  B=5,  Q=5 (log2(8)+2=5)
    # 2 (中等偏下)   - N=16, B=11, Q=6 (log2(16)+2=6)
    # 3 (中等偏上)   - N=32, B=20, Q=7 (log2(32)+2=7)
    # 4 (较难)       - N=64, B=47, Q=8 (log2(64)+2=8)
    # 5 (难)         - N=128,B=89, Q=9 (log2(128)+2=9)

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"n": 8, "boundary": 5},
            2: {"n": 16, "boundary": 11},
            3: {"n": 32, "boundary": 20},
            4: {"n": 64, "boundary": 47},
            5: {"n": 128, "boundary": 89},
        },
        "en": {
            1: {"n": 8, "boundary": 5},
            2: {"n": 16, "boundary": 11},
            3: {"n": 32, "boundary": 20},
            4: {"n": 64, "boundary": 47},
            5: {"n": 128, "boundary": 89},
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏配置和内部状态"""
        lang = self.config.language
        diff = self.config.difficulty

        # 防御性转换：确保 difficulty 是整数
        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        
        # 设置边界位置（Ground Truth）
        self.boundary = cfg["boundary"]
        
        # 计算最大允许的观察次数：Q = ceil(log2(N)) + 2
        self.max_queries = math.ceil(math.log2(cfg["n"])) + 2
        
        # 当前已使用的观察次数
        self.query_count = 0

    def evaluate(self, parsed_info):
        """
        评估最终答案是否正确
        答案格式：<answer>x</answer>，其中 x 是边界位置
        """
        try:
            answer = parsed_info["answer"].strip()
            # 尝试将答案解析为整数
            declared_boundary = int(answer)
            
            # 检查答案是否在有效范围内
            if declared_boundary < 1 or declared_boundary > self._game_info["n"]:
                return False
            
            # 检查答案是否正确
            return declared_boundary == self.boundary
            
        except (ValueError, KeyError):
            return False

    def _cf_core_produce(self, parsed_info):
        """
        原始的业务逻辑，从 produce_response 提取而来
        （基类的 produce_response 会调用此方法）
        """
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_limit = f"观察次数已达上限（{self.max_queries}次），无法继续观察。请直接提交你的最终答案。"
            error_range = f"错误：位置超出有效范围 [1, {self._game_info['n']}]。"
        else:
            yes_res, no_res = "Yes", "No"
            error_limit = f"Observation query limit ({self.max_queries}) reached. No more observations allowed. Please submit your final answer."
            error_range = f"Error: Position out of valid range [1, {self._game_info['n']}]."

        if "query_observe" in parsed_info:
            # 检查是否超过最大查询次数 —— 返回提示而非抛异常
            if self.query_count >= self.max_queries:
                return error_limit
            
            try:
                k = int(parsed_info["query_observe"].strip())
                
                # 检查位置是否在有效范围内
                if k < 1 or k > self._game_info["n"]:
                    return error_range
                
                # 增加查询计数
                self.query_count += 1
                
                # 根据边界规则返回结果
                # 如果 k >= B，说明范围 [1, k] 中存在 True（从 B 开始都是 True）
                # 如果 k < B，说明范围 [1, k] 中全是 False
                if k >= self.boundary:
                    return yes_res
                else:
                    return no_res
                    
            except ValueError:
                if self.config.language == "zh":
                    return "错误：无效的位置格式，请提供一个整数。"
                else:
                    return "Error: Invalid position format, please provide an integer."
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        """
        根据正确答案生成一个明显不同的错误答案
        """
        # 关键词替换（中文）
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        # 关键词替换（英文，忽略大小写但保持原格式）
        lower_correct = correct.lower()
        if lower_correct == "yes":
            return "No" if correct[0].isupper() else "no"
        if lower_correct == "no":
            return "Yes" if correct[0].isupper() else "yes"
            
        # 都不匹配，追加 _WRONG
        return correct + "_WRONG"

    def get_all_possible_queries(self):
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        possible_queries = []
        n = self._game_info["n"]
        
        # 预定义回答文本
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        for k in range(1, n + 1):
            # 逻辑核心：如果 k >= B，返回 Yes，否则返回 No
            if k >= self.boundary:
                ans = yes_res
            else:
                ans = no_res
            
            entry = {
                "query": f"<query_observe>{k}</query_observe>",
                "answer": ans
            }
            possible_queries.append(entry)
            
        return possible_queries