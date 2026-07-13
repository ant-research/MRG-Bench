# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 集合：存在一个由N个物体组成的集合，注意他们不存在位置、前后和大小关系。
# 知识点:   替换影响：将某元素替换为另一元素后，满足条件的元素数量如何变化
# ============================================================

from .base import Game
import random


class AttributeReconstructionGame(Game):

    game_rule_zh = """\
我们来玩一个"属性重构"的推理游戏，规则如下：

游戏设定了一个大小为 {n} 的编号元素集合（编号从 1 到 {n}）。每个元素都有一个固定但未知的二元属性，取值为 0 或 1。这些属性在整个游戏过程中保持不变。

定义"当前计数 C"为所有属性为 1 的元素总数。

你可以反复向我提出以下两类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 总数查询（类型 A）：询问当前计数 C 是多少。回答一个整数（0 到 {n}）。

2. 替换预测查询（类型 B）：给定两个不同的编号 i 和 j，询问"假设将编号 i 的属性改为与编号 j 相同"这一假设情况下，新的计数 C' 以及变化量 Δ（Δ = C' − C）是多少。
   - 如果两者属性本来就相同，则 Δ = 0
   - 如果 i 原属性为 0、j 原属性为 1，则 Δ = +1
   - 如果 i 原属性为 1、j 原属性为 0，则 Δ = -1
   - 注意：此查询仅为假设预测，不会真正改变任何元素的属性

你的目标是通过尽可能少的询问，唯一确定所有元素的完整属性向量。当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 总数查询（类型 A）：
<query_count></query_count>

- 替换预测查询（类型 B，例如询问编号 3 和 5）：
<query_swap>3,5</query_swap>

提交最终答案时，请给出长度为 {n} 的 0/1 序列（按编号 1 到 {n} 顺序，不含空格或分隔符），格式如下：

<answer>010110100101</answer>

其中第 i 位表示编号 i 的属性值。
"""

    game_rule_en = """\
Let's play an "Attribute Reconstruction" deduction game. Here are the rules:

The game has a set of {n} numbered elements (numbered from 1 to {n}). Each element has a fixed but unknown binary attribute, with a value of either 0 or 1. These attributes remain constant throughout the game.

Define "current count C" as the total number of elements with attribute 1.

You can repeatedly ask me two types of questions (one per turn), and I will answer truthfully based on the real setup:

1. Count Query (Type A): Ask what the current count C is. The answer is an integer (from 0 to {n}).

2. Swap Prediction Query (Type B): Given two different IDs i and j, ask "hypothetically, if we set element i's attribute to be the same as element j's, what would the new count C' and the change Δ (Δ = C' − C) be?"
   - If both attributes are already the same, then Δ = 0
   - If i's original attribute is 0 and j's is 1, then Δ = +1
   - If i's original attribute is 1 and j's is 0, then Δ = -1
   - Note: This query is purely hypothetical and does not actually change any attribute

Your goal is to uniquely determine the complete attribute vector of all elements through as few queries as possible. When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Count Query (Type A):
<query_count></query_count>

- Swap Prediction Query (Type B, e.g., asking about IDs 3 and 5):
<query_swap>3,5</query_swap>

When submitting the final answer, provide a 0/1 sequence of length {n} (in order from ID 1 to {n}, with no spaces or separators), using this format:

<answer>010110100101</answer>

where the i-th digit represents the attribute value of element i.
"""

    # ================= 场景化规则新增 =================

    contextualized_rule_zh_1 = """\
欢迎进入城市智能交通管控系统。本系统包含 {n} 个关键交通路口的信号灯控制节点（编号从 1 到 {n}）。每个节点具有一个固定的网络状态：0 代表离线，1 代表在线。这些状态在整个诊断过程中保持不变。

定义“当前在线数 C”为状态为 1 的节点总数。

你可以通过两种指令进行系统排查诊断（每次仅限一个指令）：

1. 全局在线查询（类型 A）：查询当前在线的节点总数 C。回答一个整数（0 到 {n}）。

2. 状态同步预测（类型 B）：给定节点 i 和 j，查询“假设将节点 i 的状态同步为节点 j 的状态”，系统新的在线总数 C' 及变化量 Δ（Δ = C' − C）。
   - 若两节点状态本就一致，则 Δ = 0
   - 若 i 原为 0（离线）、j 原为 1（在线），则 Δ = +1
   - 若 i 原为 1（在线）、j 原为 0（离线），则 Δ = -1
   - 注意：此查询仅为后台沙盒预测，不会真实改变任何节点的状态。

你的目标是以最少的查询次数，精准排查出所有 {n} 个节点的在线/离线状态。收集足够信息后，请提交最终诊断报告。

## 指令与报告提交格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 全局在线查询（类型 A）：
<query_count></query_count>

- 状态同步预测（类型 B，例如预测节点 3 和 5）：
<query_swap>3,5</query_swap>

提交最终诊断报告时，请给出长度为 {n} 的 0/1 序列（按编号 1 到 {n} 顺序，不含空格或分隔符），格式如下：

<answer>010110100101</answer>

其中第 i 位表示节点 i 的实际网络状态。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Urban Intelligent Traffic Control System. This system monitors {n} critical traffic light nodes (numbered 1 to {n}). Each node has a fixed network status: 0 for offline, 1 for online. These statuses remain constant throughout the diagnostic process.

Define "current online count C" as the total number of nodes with status 1.

You can repeatedly issue two types of diagnostic commands (one per turn), and the system will respond truthfully based on the actual setup:

1. Global Online Query (Type A): Ask for the current online count C. The answer is an integer (from 0 to {n}).

2. Status Sync Prediction (Type B): Given two different node IDs i and j, ask "hypothetically, if node i's status is synchronized to match node j's," what would the new online count C' and the change Δ (Δ = C' − C) be?
   - If both statuses are already the same, then Δ = 0
   - If i is offline (0) and j is online (1), then Δ = +1
   - If i is online (1) and j is offline (0), then Δ = -1
   - Note: This query is a sandbox prediction and does not actually change any node's status.

Your goal is to uniquely determine the complete online/offline status vector of all nodes using as few queries as possible. When ready, submit your final diagnostic report.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Global Online Query (Type A):
<query_count></query_count>

- Status Sync Prediction (Type B, e.g., predicting for nodes 3 and 5):
<query_swap>3,5</query_swap>

When submitting the final report, provide a 0/1 sequence of length {n} (in order from ID 1 to {n}, with no spaces or separators), using this format:

<answer>010110100101</answer>

where the i-th digit represents the actual status of node i.
"""

    contextualized_rule_zh_2 = """\
欢迎使用精准医疗基因组分析平台。系统中当前录入了 {n} 份患者生物样本（编号从 1 到 {n}）。每份样本存在一个确定的二元突变标记：0 表示阴性（未发生特定基因突变），1 表示阳性（发生靶点突变）。这些标记在分析期间保持不变。

定义“当前阳性计数 C”为突变标记为 1 的样本总数。

你可以通过两类操作进行临床排查推演（每次仅限一个操作）：

1. 队列阳性统计（类型 A）：查询当前阳性样本总数 C。回答一个整数（0 到 {n}）。

2. 靶点对齐预测（类型 B）：指定样本 i 和 j，查询“假设将样本 i 的突变状态理论校准为与样本 j 一致”，队列中新的阳性总数 C' 及变化量 Δ（Δ = C' − C）。
   - 若两样本状态本就相同，则 Δ = 0
   - 若 i 为阴性(0)、j 为阳性(1)，则 Δ = +1
   - 若 i 为阳性(1)、j 为阴性(0)，则 Δ = -1
   - 注意：此操作仅为推演验证，不改变实际样本的测序数据。

你的目标是以最少推演操作，唯一确定所有样本的阴阳性分布。收集足够信息后，请提交最终病理报告。

## 操作与报告提交格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 队列阳性统计（类型 A）：
<query_count></query_count>

- 靶点对齐预测（类型 B，例如指定样本 3 和 5）：
<query_swap>3,5</query_swap>

提交最终病理报告时，请给出长度为 {n} 的 0/1 序列（按样本编号 1 到 {n} 顺序，不含空格或分隔符），格式如下：

<answer>010110100101</answer>

其中第 i 位表示样本 i 的真实突变标记。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Precision Medicine Genomic Analysis Platform. The system has recorded {n} patient biological samples (numbered 1 to {n}). Each sample has a fixed binary mutation marker: 0 indicates negative (no specific mutation), 1 indicates positive (target mutation present). These markers remain unchanged during analysis.

Define "current positive count C" as the total number of samples with marker 1.

You can perform two types of clinical deduction operations (one per turn):

1. Cohort Positive Query (Type A): Ask for the current positive sample count C. The answer is an integer (from 0 to {n}).

2. Target Alignment Prediction (Type B): Specify samples i and j, and ask "hypothetically, if sample i's mutation status is theoretically calibrated to match sample j's," what the new positive count C' and the change Δ (Δ = C' − C) would be.
   - If both samples have the same status, then Δ = 0
   - If i is negative (0) and j is positive (1), then Δ = +1
   - If i is positive (1) and j is negative (0), then Δ = -1
   - Note: This operation is strictly a computational deduction and does not alter actual sequencing data.

Your goal is to uniquely determine the complete positive/negative distribution of all samples using minimal operations. Submit your final pathology report once you have enough data.

## Query and Report Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Cohort Positive Query (Type A):
<query_count></query_count>

- Target Alignment Prediction (Type B, e.g., for samples 3 and 5):
<query_swap>3,5</query_swap>

When submitting the final report, provide a 0/1 sequence of length {n} (in order from sample 1 to {n}, with no spaces or separators), using this format:

<answer>010110100101</answer>

where the i-th digit represents the true mutation marker of sample i.
"""

    contextualized_rule_zh_3 = """\
欢迎访问智能教学质量评估系统。当前课程规划包含 {n} 个核心评估模块（编号从 1 到 {n}）。每个模块目前的考核结果已经固定：0 表示未达标，1 表示已达标。

定义“达标总量 C”为考核结果为 1 的模块总数。

你可以向系统发起两类评估推演指令（每次仅限一个）：

1. 总达标查询（类型 A）：获取当前达标总量 C。系统返回一个整数（0 到 {n}）。

2. 标准对齐预测（类型 B）：输入模块 i 和 j，查询“假设将模块 i 的评估标准对齐至模块 j 的水平（使得达标状态变为相同）”，预测新的达标总量 C' 及波动值 Δ（Δ = C' − C）。
   - 若两模块状态原本相同，则 Δ = 0
   - 若 i 未达标(0)、j 已达标(1)，则 Δ = +1
   - 若 i 已达标(1)、j 未达标(0)，则 Δ = -1
   - 注意：此功能仅作为教学策略调整沙盒，并不改变现有的实际成绩。

你的目标是高效推导出所有 {n} 个模块的精确达标情况。收集完成评估后，请提交最终的课程质量视图。

## 指令与提交格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 总达标查询（类型 A）：
<query_count></query_count>

- 标准对齐预测（类型 B，例如测试模块 3 和 5）：
<query_swap>3,5</query_swap>

提交最终视图时，请给出长度为 {n} 的 0/1 序列（按模块编号 1 到 {n} 顺序，不含空格或分隔符），格式如下：

<answer>010110100101</answer>

其中第 i 位表示模块 i 的真实达标状态。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Intelligent Teaching Quality Assessment System. The current curriculum consists of {n} core evaluation modules (numbered 1 to {n}). The assessment result for each module is fixed: 0 means below standard, 1 means up to standard.

Define "total standard count C" as the total number of modules with an assessment result of 1.

You can issue two types of assessment deductions to the system (one per turn):

1. Total Standard Query (Type A): Retrieve the current standard count C. The answer is an integer (from 0 to {n}).

2. Standard Alignment Prediction (Type B): Input modules i and j, and ask "hypothetically, if module i's evaluation standard is aligned with module j's (making their statuses identical)," what the new standard count C' and fluctuation Δ (Δ = C' − C) would be.
   - If both modules already have the same status, then Δ = 0
   - If i is below standard (0) and j is up to standard (1), then Δ = +1
   - If i is up to standard (1) and j is below standard (0), then Δ = -1
   - Note: This is purely a pedagogical sandbox feature and does not change actual recorded grades.

Your goal is to efficiently deduce the precise standard status of all {n} modules. Once evaluated, submit the final curriculum quality map.

## Query and Map Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Total Standard Query (Type A):
<query_count></query_count>

- Standard Alignment Prediction (Type B, e.g., testing modules 3 and 5):
<query_swap>3,5</query_swap>

When submitting the final map, provide a 0/1 sequence of length {n} (in order from module 1 to {n}, with no spaces or separators), using this format:

<answer>010110100101</answer>

where the i-th digit represents the actual standard status of module i.
"""

    contextualized_rule_zh_4 = """\
欢迎操作自动化工业质检终端。当前生产批次包含 {n} 个关键零部件（编号从 1 到 {n}）。每个零部件的质量检验结果已在系统中固定：0 代表存在缺陷（不合格），1 代表良品（合格）。

定义“良品总数 C”为状态为 1 的零部件数量。

你可以使用以下两种检测排查指令（每次仅限一个）：

1. 批次良品统计（类型 A）：查询当前批次的良品总数 C。回答一个整数（0 到 {n}）。

2. 工艺复刻预测（类型 B）：指定零部件 i 和 j，查询“假设将零部件 i 的生产工艺完全复刻为零部件 j 的工艺（使得两者良品状态一致）”，系统预测新的良品总数 C' 及偏差量 Δ（Δ = C' − C）。
   - 若两者状态本就一致，则 Δ = 0
   - 若 i 为缺陷(0)、j 为良品(1)，则 Δ = +1
   - 若 i 为良品(1)、j 为缺陷(0)，则 Δ = -1
   - 注意：这只是系统的数字孪生工艺仿真，并不影响流水线上零部件的实物状态。

请以最少的检测次数，完整绘制出该批次所有零部件的质量图谱，并提交系统审核。

## 指令与图谱提交格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 批次良品统计（类型 A）：
<query_count></query_count>

- 工艺复刻预测（类型 B，例如指定部件 3 和 5）：
<query_swap>3,5</query_swap>

提交最终质量图谱时，请给出长度为 {n} 的 0/1 序列（按部件编号 1 到 {n} 顺序，不含空格或分隔符），格式如下：

<answer>010110100101</answer>

其中第 i 位表示零部件 i 的真实质检结果。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the Automated Industrial Quality Inspection Terminal. The current production batch contains {n} critical components (numbered 1 to {n}). The quality inspection result for each component is fixed in the system: 0 indicates defective (unqualified), 1 indicates good (qualified).

Define "total good count C" as the total number of components with status 1.

You can use the following two diagnostic commands (one per turn):

1. Batch Good Query (Type A): Query the current total good count C. The answer is an integer (from 0 to {n}).

2. Process Replication Prediction (Type B): Specify components i and j, and ask "hypothetically, if the production process of component i is completely replicated from component j (so their quality statuses match)," what the new good count C' and variance Δ (Δ = C' − C) would be.
   - If both statuses already match, then Δ = 0
   - If i is defective (0) and j is good (1), then Δ = +1
   - If i is good (1) and j is defective (0), then Δ = -1
   - Note: This is solely a digital twin process simulation and does not affect the physical status of components on the assembly line.

Map out the complete quality profile of all components in this batch using the fewest checks possible, and submit it for review.

## Query and Profile Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Batch Good Query (Type A):
<query_count></query_count>

- Process Replication Prediction (Type B, e.g., for components 3 and 5):
<query_swap>3,5</query_swap>

When submitting the final profile, provide a 0/1 sequence of length {n} (in order from component 1 to {n}, with no spaces or separators), using this format:

<answer>010110100101</answer>

where the i-th digit represents the true inspection result of component i.
"""

    contextualized_rule_zh_5 = """\
欢迎进入数字法务证据质证系统。本案目前已保全了 {n} 份核心证据材料（编号从 1 到 {n}）。每份证据的法律效力已经被法庭初步界定并固定：0 表示无效/不可采信，1 表示有效/可采信。

定义“有效证据数 C”为判定状态为 1 的证据总量。

你可以进行两类法理推演操作（每次仅限一个操作）：

1. 效力总汇（类型 A）：查询当前有效证据的总数 C。回答一个整数（0 到 {n}）。

2. 判例参照预测（类型 B）：指定证据 i 和 j，查询“假设完全依据证据 j 的采信标准来重新界定证据 i 的效力（使两者的效力状态变为相同）”，推演出的新有效证据数 C' 及变化量 Δ（Δ = C' − C）。
   - 若两证据效力原本相同，则 Δ = 0
   - 若 i 不可采信(0)、j 可采信(1)，则 Δ = +1
   - 若 i 可采信(1)、j 不可采信(0)，则 Δ = -1
   - 注意：此推演仅供律师团队用于法庭辩论沙盘模拟，不会更改案卷中已保全证据的真实属性。

你需要通过最少的推演操作，查明所有 {n} 份证据的效力认定结果，并向系统提交完整的质证清单。

## 操作与清单提交格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 效力总汇查询（类型 A）：
<query_count></query_count>

- 判例参照预测（类型 B，例如推演证据 3 和 5）：
<query_swap>3,5</query_swap>

提交最终质证清单时，请给出长度为 {n} 的 0/1 序列（按证据编号 1 到 {n} 顺序，不含空格或分隔符），格式如下：

<answer>010110100101</answer>

其中第 i 位表示证据 i 真实的法律效力状态。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Digital Legal Evidence Cross-examination System. The case currently preserves {n} core pieces of evidence (numbered 1 to {n}). The legal validity of each piece of evidence has been preliminarily determined and fixed: 0 indicates invalid/inadmissible, 1 indicates valid/admissible.

Define "valid evidence count C" as the total number of evidence pieces with status 1.

You can perform two types of jurisprudential deductions (one per turn):

1. Total Validity Query (Type A): Query the current valid evidence count C. The answer is an integer (from 0 to {n}).

2. Precedent Reference Prediction (Type B): Specify evidence i and j, and ask "hypothetically, if evidence i's validity is redefined strictly based on the admissibility standard of evidence j (making their statuses identical)," what the new valid evidence count C' and change Δ (Δ = C' − C) would be.
   - If both pieces already share the same validity, then Δ = 0
   - If i is inadmissible (0) and j is admissible (1), then Δ = +1
   - If i is admissible (1) and j is inadmissible (0), then Δ = -1
   - Note: This deduction is strictly for courtroom debate simulation by the legal team and does not alter the actual attributes of preserved evidence in the dossier.

You must determine the validity outcomes of all {n} pieces of evidence using minimal deductions, and submit a complete cross-examination list to the system.

## Query and List Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Total Validity Query (Type A):
<query_count></query_count>

- Precedent Reference Prediction (Type B, e.g., deducting evidence 3 and 5):
<query_swap>3,5</query_swap>

When submitting the final list, provide a 0/1 sequence of length {n} (in order from evidence 1 to {n}, with no spaces or separators), using this format:

<answer>010110100101</answer>

where the i-th digit represents the true legal validity status of evidence i.
"""

    tags = ["answer", "query_count", "query_swap"]
    
    reasoning_type = "演绎推理"
    data_structure = "集合"

    # 难度说明：
    # 1 (easy)        - N=6,  C=2
    # 2 (medium_low)  - N=8,  C=3
    # 3 (medium_high) - N=10, C=5
    # 4 (hard)        - N=12, C=6
    # 5 (very_hard)   - N=15, C=7

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 6,
                "attributes": "010010",  # 编号2和5为1
            },
            2: {
                "n": 8,
                "attributes": "10100100",  # 编号1,3,6为1
            },
            3: {
                "n": 10,
                "attributes": "0110101010",  # 编号2,3,5,7,9为1
            },
            4: {
                "n": 12,
                "attributes": "101001011010",  # 编号1,3,6,8,9,11为1
            },
            5: {
                "n": 15,
                "attributes": "100101101010100",  # 编号1,4,6,7,9,11,13为1
            },
        },
        "en": {
            1: {
                "n": 6,
                "attributes": "010010",
            },
            2: {
                "n": 8,
                "attributes": "10100100",
            },
            3: {
                "n": 10,
                "attributes": "0110101010",
            },
            4: {
                "n": 12,
                "attributes": "101001011010",
            },
            5: {
                "n": 15,
                "attributes": "100101101010100",
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：设置属性向量 X"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        
        # 解析属性向量（索引从1开始，所以在前面补一个占位符）
        self.attributes = [None] + [int(x) for x in cfg["attributes"]]
        # attributes[i] 表示编号 i 的属性值（i = 1..n）
        
        # 计算当前计数 C
        self.current_count = sum(self.attributes[1:])

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        # 检查长度是否正确
        if len(raw_ans) != self._game_info["n"]:
            return False
        
        # 检查是否全为0或1
        if not all(c in '01' for c in raw_ans):
            return False
        
        # 构造提交的属性向量
        submitted = [int(c) for c in raw_ans]
        
        # 与真实属性向量比较（注意真实向量索引从1开始）
        ground_truth = self.attributes[1:]
        
        return submitted == ground_truth

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑"""
        if self.config.language == "zh":
            error_msg = "错误：查询格式无效。"
            count_prefix = "C = "
            swap_format = "C' = {}, Δ = {}"
        else:
            error_msg = "Error: Invalid query format."
            count_prefix = "C = "
            swap_format = "C' = {}, Δ = {}"

        # 优先级：Count > Swap
        if "query_count" in parsed_info:
            # 类型 A：返回当前计数
            return count_prefix + str(self.current_count)

        elif "query_swap" in parsed_info:
            # 类型 B：替换预测查询
            try:
                raw = parsed_info["query_swap"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_msg
                
                i, j = int(parts[0]), int(parts[1])
                n = self._game_info["n"]
                
                # 检查编号范围和是否相同
                if i < 1 or i > n or j < 1 or j > n or i == j:
                    return error_msg
                
                # 获取 i 和 j 的真实属性
                attr_i = self.attributes[i]
                attr_j = self.attributes[j]
                
                # 计算假设情况下的变化
                if attr_i == attr_j:
                    # 属性相同，无变化
                    delta = 0
                elif attr_i == 0 and attr_j == 1:
                    # i 从 0 变成 1，计数增加
                    delta = 1
                else:  # attr_i == 1 and attr_j == 0
                    # i 从 1 变成 0，计数减少
                    delta = -1
                
                new_count = self.current_count + delta
                
                return swap_format.format(new_count, delta)
                
            except (ValueError, IndexError):
                return error_msg

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """生成错误答案"""
        import re
        
        # 尝试匹配 "C = X" 格式（query_count 的响应）
        count_match = re.match(r'^C\s*=\s*(\d+)$', correct.strip())
        if count_match:
            val = int(count_match.group(1))
            wrong_val = val + 1 if val < self._game_info["n"] else val - 1
            return f"C = {wrong_val}"
        
        # 尝试匹配 "C' = X, Δ = Y" 格式（query_swap 的响应）
        swap_match = re.match(r"C'\s*=\s*(-?\d+),\s*Δ\s*=\s*(-?\d+)", correct.strip())
        if swap_match:
            c_prime = int(swap_match.group(1))
            delta = int(swap_match.group(2))
            # 修改 delta 值来产生错误
            if delta == 0:
                wrong_delta = 1
            elif delta == 1:
                wrong_delta = -1
            else:  # delta == -1
                wrong_delta = 0
            wrong_c_prime = self.current_count + wrong_delta
            return f"C' = {wrong_c_prime}, Δ = {wrong_delta}"
        
        # 若 correct 是纯整数字符串
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 否则替换关键词
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        else:
            # 简单检查 Yes/No，保持大小写风格需要稍微复杂一点的处理，
            # 这里简单处理常见情况，如果更复杂可以用正则
            lower_correct = correct.lower()
            if "yes" in lower_correct:
                if "Yes" in correct: return correct.replace("Yes", "No")
                if "yes" in correct: return correct.replace("yes", "no")
                if "YES" in correct: return correct.replace("YES", "NO")
            elif "no" in lower_correct:
                if "No" in correct: return correct.replace("No", "Yes")
                if "no" in correct: return correct.replace("no", "yes")
                if "NO" in correct: return correct.replace("NO", "YES")
        
        # 若都不匹配，追加 _WRONG
        return correct + "_WRONG"

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
        results = []
        n = self._game_info["n"]
        
        # 1. 总数查询 (query_count)
        # 构造 parsed_info 模拟 parse 结果
        parsed_count = {"query_count": ""}
        # 调用核心逻辑获取正确答案
        ans_count = self._cf_core_produce(parsed_count)
        
        results.append({
            "query": "<query_count></query_count>",
            "answer": ans_count
        })

        # 2. 替换预测查询 (query_swap)
        # 枚举所有 i, j (i != j)
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if i == j:
                    continue
                
                query_content = f"{i},{j}"
                query_str = f"<query_swap>{query_content}</query_swap>"
                
                # 构造 parsed_info
                parsed_swap = {"query_swap": query_content}
                
                # 获取正确答案
                ans_swap = self._cf_core_produce(parsed_swap)
                
                results.append({
                    "query": query_str,
                    "answer": ans_swap
                })
                
        return results