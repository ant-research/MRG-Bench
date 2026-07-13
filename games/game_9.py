# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 集合：存在一个由N个物体组成的集合，注意他们不存在位置、前后和大小关系。
# 知识点:   子集包含：某子集是否完全被另一子集包含
# ============================================================

from .base import Game
import random


class SubsetInclusionGame(Game):

    game_rule_zh = """\
我们现在来玩一个"子集包含推理"游戏，规则如下：

游戏设定了一个不可见的全集 U 和 {m} 个带标签的子集 S1, S2, ..., S{m}，它们都是 U 的子集。此外，还有一个不可见的目标子集 K（K 也是 U 的子集）。

你的任务是：通过提问推断出每个子集 Si 是否被 K 包含（即 Si 是否是 K 的子集），并在使用尽可能少的目标查询次数的情况下提交完整的判定结果。

你可以进行以下两种查询：

1. 子集包含查询（不限次数）：询问 Si 是否是 Sj 的子集。我会回答"是"或"否"。
2. 目标包含查询（请尽量节约使用）：询问 Si 是否是目标集合 K 的子集。我会回答"是"或"否"，并告知你剩余的查询额度。

注意：
- 你当前的目标查询额度为 {budget} 次。
- 所有回答都基于固定的集合结构，且遵循集合论的逻辑规则。
- 你可以利用传递性等逻辑推理来减少目标查询次数。

## 查询与提交答案的格式（必须严格遵守）

每次只能提出一个查询。请使用以下 XML 格式：

- 子集包含查询（例如询问 S1 是否是 S2 的子集）：
<query_subset>1,2</query_subset>

- 目标包含查询（例如询问 S3 是否是 K 的子集）：
<query_target>3</query_target>

提交最终答案时，必须列出所有子集的判定结果（用逗号隔开，顺序为 S1 到 S{m}，每个位置填 1 表示"是 K 的子集"，填 0 表示"不是 K 的子集"），格式如下：

<answer>1,0,1,0</answer>
"""

    game_rule_en = """\
Let's play a "Subset Inclusion Reasoning" game. Here are the rules:

The game involves an invisible universal set U and {m} labeled subsets S1, S2, ..., S{m}, all of which are subsets of U. Additionally, there is an invisible target subset K (K is also a subset of U).

Your task is: through queries, determine whether each subset Si is contained in K (i.e., whether Si is a subset of K), and submit the complete judgment results using as few target queries as possible.

You can make the following two types of queries:

1. Subset Inclusion Query (unlimited): Ask whether Si is a subset of Sj. I will answer "Yes" or "No".
2. Target Inclusion Query (please use sparingly): Ask whether Si is a subset of the target set K. I will answer "Yes" or "No" and inform you of the remaining query quota.

Note:
- Your current target query quota is {budget} times.
- All answers are based on a fixed set structure and follow the logical rules of set theory.
- You can use transitivity and other logical reasoning to reduce the number of target queries.

## Query and Answer Format (must be strictly followed)

You can only make one query at a time. Use the following XML format:

- Subset Inclusion Query (e.g., asking if S1 is a subset of S2):
<query_subset>1,2</query_subset>

- Target Inclusion Query (e.g., asking if S3 is a subset of K):
<query_target>3</query_target>

When submitting the final answer, you must list the judgment results for all subsets (comma-separated, in order from S1 to S{m}, with 1 indicating "is a subset of K" and 0 indicating "is not a subset of K"), in the following format:

<answer>1,0,1,0</answer>
"""

    contextualized_rule_zh_1 = """\
我们现在来玩一个“交通路网包含关系推理”系统。

系统设定了一个不可见的城市整体交通路网 U，以及 {m} 个带标签的局部交通区域 S1, S2, ..., S{m}，它们都是 U 的子区域（子集）。此外，还有一个不可见的“重度拥堵核心区” K（K 也是 U 的子区域）。

你的任务是：通过提问推断出每个交通区域 Si 是否完全落在拥堵核心区 K 内（即 Si 是否是 K 的子集），并在使用尽可能少的核心区查询次数的情况下提交完整的判定结果。

你可以进行以下两种查询：

1. 区域包含查询（不限次数）：询问区域 Si 是否完全被区域 Sj 包含（即 Si 是否是 Sj 的子集）。我会回答“是”或“否”。
2. 核心区包含查询（请尽量节约使用）：询问区域 Si 是否完全落在拥堵核心区 K 内。我会回答“是”或“否”，并告知你剩余的查询额度。

注意：
- 你当前的核心区查询额度为 {budget} 次。
- 所有回答都基于固定的路网结构，且遵循集合论的空间逻辑规则。
- 你可以利用传递性等空间逻辑推理来减少核心区查询次数。

## 查询与提交答案的格式（必须严格遵守）

每次只能提出一个查询。请使用以下 XML 格式：

- 区域包含查询（例如询问 S1 是否在 S2 内）：
<query_subset>1,2</query_subset>

- 核心区包含查询（例如询问 S3 是否在 K 内）：
<query_target>3</query_target>

提交最终答案时，必须列出所有区域的判定结果（用逗号隔开，顺序为 S1 到 S{m}，每个位置填 1 表示“完全在 K 内”，填 0 表示“不完全在 K 内”），格式如下：

<answer>1,0,1,0</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's use the "Traffic Network Inclusion Reasoning" system.

The system involves an invisible comprehensive city traffic network U and {m} labeled local traffic zones S1, S2, ..., S{m}, all of which are sub-zones (subsets) of U. Additionally, there is an invisible "Severe Congestion Core" K (K is also a sub-zone of U).

Your task is: through queries, determine whether each traffic zone Si is completely contained within the Congestion Core K (i.e., whether Si is a subset of K), and submit the complete judgment results using as few core queries as possible.

You can make the following two types of queries:

1. Zone Inclusion Query (unlimited): Ask whether zone Si is completely contained within zone Sj. I will answer "Yes" or "No".
2. Core Inclusion Query (please use sparingly): Ask whether zone Si is completely within the Congestion Core K. I will answer "Yes" or "No" and inform you of the remaining query quota.

Note:
- Your current core query quota is {budget} times.
- All answers are based on a fixed spatial structure and follow the logical rules of set theory.
- You can use transitivity and other spatial logical reasoning to reduce the number of core queries.

## Query and Answer Format (must be strictly followed)

You can only make one query at a time. Use the following XML format:

- Zone Inclusion Query (e.g., asking if S1 is within S2):
<query_subset>1,2</query_subset>

- Core Inclusion Query (e.g., asking if S3 is within K):
<query_target>3</query_target>

When submitting the final answer, you must list the judgment results for all zones (comma-separated, in order from S1 to S{m}, with 1 indicating "completely within K" and 0 indicating "not completely within K"), in the following format:

<answer>1,0,1,0</answer>
"""

    contextualized_rule_zh_2 = """\
我们现在来使用“临床症状群组包含推理”系统。

系统设定了一个不可见的人类全量症状库 U，以及 {m} 个带标签的特定综合征症状群 S1, S2, ..., S{m}，它们都是 U 的子集。此外，还有一个不可见的“新型突发病毒症状谱” K（K 也是 U 的子集）。

你的任务是：通过提问推断出每个综合征的症状群 Si 是否完全被该新型病毒症状谱 K 包含（即 Si 是否是 K 的子集），并在使用尽可能少的病毒谱查询次数的情况下提交完整的判定结果。

你可以进行以下两种查询：

1. 症状群包含查询（不限次数）：询问综合征 Si 的所有症状是否都包含在综合征 Sj 中。我会回答“是”或“否”。
2. 病毒谱包含查询（请尽量节约使用）：询问综合征 Si 的所有症状是否均出现在新型病毒症状谱 K 中。我会回答“是”或“否”，并告知你剩余的查询额度。

注意：
- 你当前的病毒谱查询额度为 {budget} 次。
- 所有回答都基于固定的病理学结构，且遵循集合论的逻辑规则。
- 你可以利用传递性等医学逻辑推理来减少病毒谱查询次数。

## 查询与提交答案的格式（必须严格遵守）

每次只能提出一个查询。请使用以下 XML 格式：

- 症状群包含查询（例如询问 S1 的症状是否都被 S2 包含）：
<query_subset>1,2</query_subset>

- 病毒谱包含查询（例如询问 S3 的症状是否都在 K 中）：
<query_target>3</query_target>

提交最终答案时，必须列出所有综合征的判定结果（用逗号隔开，顺序为 S1 到 S{m}，每个位置填 1 表示“完全在 K 中”，填 0 表示“不完全在 K 中”），格式如下：

<answer>1,0,1,0</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's use the "Clinical Symptom Cluster Inclusion Reasoning" system.

The system involves an invisible comprehensive human symptom database U and {m} labeled specific syndrome symptom clusters S1, S2, ..., S{m}, all of which are subsets of U. Additionally, there is an invisible "Novel Viral Strain Symptom Profile" K (K is also a subset of U).

Your task is: through queries, determine whether each syndrome's symptom cluster Si is completely contained within the novel viral profile K (i.e., whether Si is a subset of K), and submit the complete judgment results using as few viral profile queries as possible.

You can make the following two types of queries:

1. Symptom Cluster Inclusion Query (unlimited): Ask whether all symptoms of syndrome Si are included in syndrome Sj. I will answer "Yes" or "No".
2. Viral Profile Inclusion Query (please use sparingly): Ask whether all symptoms of syndrome Si are present in the novel viral profile K. I will answer "Yes" or "No" and inform you of the remaining query quota.

Note:
- Your current viral profile query quota is {budget} times.
- All answers are based on a fixed pathological structure and follow the logical rules of set theory.
- You can use transitivity and other medical logical reasoning to reduce the number of viral profile queries.

## Query and Answer Format (must be strictly followed)

You can only make one query at a time. Use the following XML format:

- Symptom Cluster Inclusion Query (e.g., asking if S1's symptoms are all in S2):
<query_subset>1,2</query_subset>

- Viral Profile Inclusion Query (e.g., asking if S3's symptoms are all in K):
<query_target>3</query_target>

When submitting the final answer, you must list the judgment results for all syndromes (comma-separated, in order from S1 to S{m}, with 1 indicating "completely within K" and 0 indicating "not completely within K"), in the following format:

<answer>1,0,1,0</answer>
"""

    contextualized_rule_zh_3 = """\
我们现在来进行“课程知识点包含逻辑推理”。

系统设定了一个不可见的全学科知识图谱 U，以及 {m} 个带标签的特定课程知识模块 S1, S2, ..., S{m}，它们都是 U 的子模块（子集）。此外，还有一个不可见的“毕业核心考核要求” K（K 也是 U 的子模块）。

你的任务是：通过提问推断出每个知识模块 Si 是否完全被毕业考核要求 K 涵盖（即 Si 是否是 K 的子集），并在使用尽可能少的考核要求查询次数的情况下提交完整的判定结果。

你可以进行以下两种查询：

1. 模块包含查询（不限次数）：询问知识模块 Si 是否完全是模块 Sj 的前置基础（即 Si 的所有考点都被 Sj 包含）。我会回答“是”或“否”。
2. 考核要求包含查询（请尽量节约使用）：询问知识模块 Si 是否完全落在毕业考核要求 K 的范围内。我会回答“是”或“否”，并告知你剩余的查询额度。

注意：
- 你当前的考核要求查询额度为 {budget} 次。
- 所有回答都基于固定的课程体系结构，且遵循集合论的逻辑规则。
- 你可以利用传递性等教育逻辑推理来减少考核要求查询次数。

## 查询与提交答案的格式（必须严格遵守）

每次只能提出一个查询。请使用以下 XML 格式：

- 模块包含查询（例如询问 S1 的考点是否都在 S2 中）：
<query_subset>1,2</query_subset>

- 考核要求包含查询（例如询问 S3 的考点是否都在 K 中）：
<query_target>3</query_target>

提交最终答案时，必须列出所有知识模块的判定结果（用逗号隔开，顺序为 S1 到 S{m}，每个位置填 1 表示“完全在 K 中”，填 0 表示“不完全在 K 中”），格式如下：

<answer>1,0,1,0</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct the "Curriculum Knowledge Inclusion Logical Reasoning".

The system involves an invisible comprehensive interdisciplinary knowledge graph U and {m} labeled specific curriculum knowledge modules S1, S2, ..., S{m}, all of which are sub-modules (subsets) of U. Additionally, there is an invisible "Core Graduation Requirement" K (K is also a sub-module of U).

Your task is: through queries, determine whether each knowledge module Si is completely covered by the graduation requirement K (i.e., whether Si is a subset of K), and submit the complete judgment results using as few requirement queries as possible.

You can make the following two types of queries:

1. Module Inclusion Query (unlimited): Ask whether knowledge module Si is completely included in module Sj. I will answer "Yes" or "No".
2. Requirement Inclusion Query (please use sparingly): Ask whether knowledge module Si falls completely within the Core Graduation Requirement K. I will answer "Yes" or "No" and inform you of the remaining query quota.

Note:
- Your current requirement query quota is {budget} times.
- All answers are based on a fixed curriculum structure and follow the logical rules of set theory.
- You can use transitivity and other educational logical reasoning to reduce the number of requirement queries.

## Query and Answer Format (must be strictly followed)

You can only make one query at a time. Use the following XML format:

- Module Inclusion Query (e.g., asking if S1's points are all in S2):
<query_subset>1,2</query_subset>

- Requirement Inclusion Query (e.g., asking if S3's points are all in K):
<query_target>3</query_target>

When submitting the final answer, you must list the judgment results for all knowledge modules (comma-separated, in order from S1 to S{m}, with 1 indicating "completely within K" and 0 indicating "not completely within K"), in the following format:

<answer>1,0,1,0</answer>
"""

    contextualized_rule_zh_4 = """\
我们现在来执行“工业流水线工序包含推理”系统。

系统设定了一个不可见的完整生产工艺总集 U，以及 {m} 个带标签的局部装配工序 S1, S2, ..., S{m}，它们都是 U 的子集。此外，还有一个不可见的“高频次品风险特征库” K（K 也是 U 的子集）。

你的任务是：通过提问推断出每个装配工序 Si 的所有操作步骤是否都属于次品风险特征库 K（即 Si 是否是 K 的子集），并在使用尽可能少的特征库查询次数的情况下提交完整的排查结果。

你可以进行以下两种查询：

1. 工序包含查询（不限次数）：询问工序 Si 的所有步骤是否都包含在工序 Sj 内。我会回答“是”或“否”。
2. 风险库包含查询（请尽量节约使用）：询问工序 Si 的所有步骤是否均命中了高频次品风险特征库 K。我会回答“是”或“否”，并告知你剩余的查询额度。

注意：
- 你当前的风险库查询额度为 {budget} 次。
- 所有回答都基于固定的流水线工艺结构，且遵循集合论的逻辑规则。
- 你可以利用传递性等工艺流逻辑推理来减少风险库查询次数。

## 查询与提交答案的格式（必须严格遵守）

每次只能提出一个查询。请使用以下 XML 格式：

- 工序包含查询（例如询问 S1 是否被 S2 包含）：
<query_subset>1,2</query_subset>

- 风险库包含查询（例如询问 S3 是否完全命中 K）：
<query_target>3</query_target>

提交最终答案时，必须列出所有工序的判定结果（用逗号隔开，顺序为 S1 到 S{m}，每个位置填 1 表示“完全在 K 中”，填 0 表示“不完全在 K 中”），格式如下：

<answer>1,0,1,0</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's execute the "Industrial Assembly Line Procedure Inclusion Reasoning" system.

The system involves an invisible complete manufacturing process catalog U and {m} labeled local assembly procedures S1, S2, ..., S{m}, all of which are subsets of U. Additionally, there is an invisible "High-Frequency Defect Risk Profile" K (K is also a subset of U).

Your task is: through queries, determine whether all operational steps of each assembly procedure Si belong to the Defect Risk Profile K (i.e., whether Si is a subset of K), and submit the complete inspection results using as few risk profile queries as possible.

You can make the following two types of queries:

1. Procedure Inclusion Query (unlimited): Ask whether all steps of procedure Si are included within procedure Sj. I will answer "Yes" or "No".
2. Risk Profile Inclusion Query (please use sparingly): Ask whether all steps of procedure Si fully match the High-Frequency Defect Risk Profile K. I will answer "Yes" or "No" and inform you of the remaining query quota.

Note:
- Your current risk profile query quota is {budget} times.
- All answers are based on a fixed assembly line structure and follow the logical rules of set theory.
- You can use transitivity and other process logic reasoning to reduce the number of risk profile queries.

## Query and Answer Format (must be strictly followed)

You can only make one query at a time. Use the following XML format:

- Procedure Inclusion Query (e.g., asking if S1 is included in S2):
<query_subset>1,2</query_subset>

- Risk Profile Inclusion Query (e.g., asking if S3 fully matches K):
<query_target>3</query_target>

When submitting the final answer, you must list the judgment results for all procedures (comma-separated, in order from S1 to S{m}, with 1 indicating "completely within K" and 0 indicating "not completely within K"), in the following format:

<answer>1,0,1,0</answer>
"""

    contextualized_rule_zh_5 = """\
我们现在来进行“法条与司法管辖权包含推理”。

系统设定了一个不可见的完整国家法律法典 U，以及 {m} 个带标签的具体司法条款集 S1, S2, ..., S{m}，它们都是 U 的子集。此外，还有一个不可见的“地标性案件适用管辖权框架” K（K 也是 U 的子集）。

你的任务是：通过提问推断出每个条款集 Si 是否完全落入该案件适用管辖权框架 K 内（即 Si 是否是 K 的子集），并在使用尽可能少的管辖权查询次数的情况下提交完整的判定结果。

你可以进行以下两种查询：

1. 条款包含查询（不限次数）：询问条款集 Si 的所有规定是否都被条款集 Sj 所涵盖（即 Si 是否是 Sj 的子集）。我会回答“是”或“否”。
2. 管辖权包含查询（请尽量节约使用）：询问条款集 Si 是否完全落入地标性案件管辖权框架 K 内。我会回答“是”或“否”，并告知你剩余的查询额度。

注意：
- 你当前的管辖权查询额度为 {budget} 次。
- 所有回答都基于固定的法理从属结构，且遵循集合论的逻辑规则。
- 你可以利用传递性等法理逻辑推理来减少管辖权查询次数。

## 查询与提交答案的格式（必须严格遵守）

每次只能提出一个查询。请使用以下 XML 格式：

- 条款包含查询（例如询问 S1 的规定是否被 S2 涵盖）：
<query_subset>1,2</query_subset>

- 管辖权包含查询（例如询问 S3 是否完全落入 K 内）：
<query_target>3</query_target>

提交最终答案时，必须列出所有条款集的判定结果（用逗号隔开，顺序为 S1 到 S{m}，每个位置填 1 表示“完全在 K 内”，填 0 表示“不完全在 K 内”），格式如下：

<answer>1,0,1,0</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct the "Statute and Jurisdiction Inclusion Reasoning".

The system involves an invisible complete national legal corpus U and {m} labeled specific statute sets S1, S2, ..., S{m}, all of which are subsets of U. Additionally, there is an invisible "Applicable Jurisdiction Framework for Landmark Case" K (K is also a subset of U).

Your task is: through queries, determine whether each statute set Si falls completely within the applicable jurisdiction framework K (i.e., whether Si is a subset of K), and submit the complete judgment results using as few jurisdiction queries as possible.

You can make the following two types of queries:

1. Statute Inclusion Query (unlimited): Ask whether all provisions of statute set Si are subsumed under statute set Sj (i.e., whether Si is a subset of Sj). I will answer "Yes" or "No".
2. Jurisdiction Inclusion Query (please use sparingly): Ask whether statute set Si falls completely within the landmark case jurisdiction framework K. I will answer "Yes" or "No" and inform you of the remaining query quota.

Note:
- Your current jurisdiction query quota is {budget} times.
- All answers are based on a fixed jurisprudential subordination structure and follow the logical rules of set theory.
- You can use transitivity and other legal logical reasoning to reduce the number of jurisdiction queries.

## Query and Answer Format (must be strictly followed)

You can only make one query at a time. Use the following XML format:

- Statute Inclusion Query (e.g., asking if S1 is subsumed under S2):
<query_subset>1,2</query_subset>

- Jurisdiction Inclusion Query (e.g., asking if S3 falls completely within K):
<query_target>3</query_target>

When submitting the final answer, you must list the judgment results for all statute sets (comma-separated, in order from S1 to S{m}, with 1 indicating "completely within K" and 0 indicating "not completely within K"), in the following format:

<answer>1,0,1,0</answer>
"""

    tags = ["answer", "query_subset", "query_target"]
    reasoning_type = "演绎推理"
    data_structure = "集合"

    # 难度配置：
    # 1 (简单)        - M=4, 链式结构, L充足
    # 2 (中等偏下)    - M=5, 部分独立, L中等
    # 3 (中等偏上)    - M=6, 多分支, L较紧
    # 4 (较难)        - M=7, 复杂关系, L紧张
    # 5 (难)          - M=8, 高度复杂, L很紧

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "m": 4,
                "budget": 3,
                "subset_relations": [
                    (1, 2), (2, 3)
                ],
                "target_containment": [1, 1, 0, 0]
            },
            2: {
                "m": 5,
                "budget": 4,
                "subset_relations": [
                    (1, 2), (3, 4)
                ],
                "target_containment": [1, 1, 1, 0, 0]
            },
            3: {
                "m": 6,
                "budget": 4,
                "subset_relations": [
                    (1, 2), (2, 4), (3, 4), (5, 6)
                ],
                "target_containment": [1, 1, 1, 0, 0, 0]
            },
            4: {
                "m": 7,
                "budget": 5,
                "subset_relations": [
                    (1, 2), (2, 5), (3, 5), (4, 6)
                ],
                "target_containment": [1, 0, 1, 1, 0, 0, 0]
            },
            5: {
                "m": 8,
                "budget": 5,
                "subset_relations": [
                    (1, 3), (2, 3), (3, 6), (4, 7), (5, 7)
                ],
                "target_containment": [1, 1, 0, 0, 1, 0, 0, 0]
            },
        },
        "en": {
            1: {
                "m": 4,
                "budget": 3,
                "subset_relations": [
                    (1, 2), (2, 3)
                ],
                "target_containment": [1, 1, 0, 0]
            },
            2: {
                "m": 5,
                "budget": 4,
                "subset_relations": [
                    (1, 2), (3, 4)
                ],
                "target_containment": [1, 1, 1, 0, 0]
            },
            3: {
                "m": 6,
                "budget": 4,
                "subset_relations": [
                    (1, 2), (2, 4), (3, 4), (5, 6)
                ],
                "target_containment": [1, 1, 1, 0, 0, 0]
            },
            4: {
                "m": 7,
                "budget": 5,
                "subset_relations": [
                    (1, 2), (2, 5), (3, 5), (4, 6)
                ],
                "target_containment": [1, 0, 1, 1, 0, 0, 0]
            },
            5: {
                "m": 8,
                "budget": 5,
                "subset_relations": [
                    (1, 3), (2, 3), (3, 6), (4, 7), (5, 7)
                ],
                "target_containment": [1, 1, 0, 0, 1, 0, 0, 0]
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏状态和真实数据结构"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 防御性转换为整数

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 基本参数
        self.m = cfg["m"]
        self.budget = cfg["budget"]
        self.remaining_budget = self.budget
        
        # 存储游戏规则中需要的信息
        self._game_info["m"] = self.m
        self._game_info["budget"] = self.budget
        
        # 子集包含关系：subset_relations存储 (i,j) 表示 Si ⊆ Sj
        self.subset_relations = set(cfg["subset_relations"])
        
        # 计算传递闭包（用于快速查询）
        self._compute_transitive_closure()
        
        # 目标包含关系的真实答案
        self.target_containment = cfg["target_containment"]

    def _compute_transitive_closure(self):
        """计算子集包含关系的传递闭包"""
        # 初始化：每个集合包含自己
        self.closure = {i: {i} for i in range(1, self.m + 1)}
        
        # 添加直接关系
        for i, j in self.subset_relations:
            self.closure[i].add(j)
        
        # Floyd-Warshall算法计算传递闭包
        for k in range(1, self.m + 1):
            for i in range(1, self.m + 1):
                for j in range(1, self.m + 1):
                    if k in self.closure[i] and j in self.closure[k]:
                        self.closure[i].add(j)

    def _is_subset_of(self, i, j):
        """判断 Si 是否是 Sj 的子集"""
        return j in self.closure[i]

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        try:
            # 解析答案：应该是逗号分隔的0/1序列
            answer_list = [int(x.strip()) for x in raw_ans.split(",")]
            
            # 检查长度是否正确
            if len(answer_list) != self.m:
                return False
            
            # 检查每个值是否为0或1
            if not all(x in [0, 1] for x in answer_list):
                return False
            
            # 与真实答案比较
            return answer_list == self.target_containment
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始的响应生成逻辑"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：格式无效或索引超出范围。"
            error_budget = "错误：目标查询次数已用尽。"
            budget_info = "剩余目标查询额度：{}"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid format or index out of range."
            error_budget = "Error: Target query quota exhausted."
            budget_info = "Remaining target query quota: {}"

        # 优先处理 query_subset
        if "query_subset" in parsed_info:
            try:
                raw = parsed_info["query_subset"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                i, j = int(parts[0]), int(parts[1])
                
                if i < 1 or i > self.m or j < 1 or j > self.m:
                    return error_format
                
                # 判断 Si 是否是 Sj 的子集
                result = yes_res if self._is_subset_of(i, j) else no_res
                return result
                
            except Exception:
                return error_format

        # 处理 query_target
        elif "query_target" in parsed_info:
            # 检查额度
            if self.remaining_budget <= 0:
                return error_budget
            
            try:
                raw = parsed_info["query_target"].strip()
                i = int(raw)
                
                if i < 1 or i > self.m:
                    return error_format
                
                # 消耗一次查询额度
                self.remaining_budget -= 1
                
                # 判断 Si 是否是 K 的子集（索引从0开始）
                result = yes_res if self.target_containment[i - 1] == 1 else no_res
                budget_msg = budget_info.format(self.remaining_budget)
                
                return f"{result}\n{budget_msg}"
                
            except Exception:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """根据正确答案生成一个明显不同的错误答案"""
        if correct.isdigit():
            return str(int(correct) + 1)
            
        lines = correct.split("\n")
        if lines[0] == "是":
            lines[0] = "否"
        elif lines[0] == "否":
            lines[0] = "是"
        elif lines[0] == "Yes":
            lines[0] = "No"
        elif lines[0] == "No":
            lines[0] = "Yes"
        else:
            lines[0] = lines[0] + "_WRONG"
            
        return "\n".join(lines)

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
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            budget_info_tpl = "剩余目标查询额度：{}"
        else:
            yes_res, no_res = "Yes", "No"
            budget_info_tpl = "Remaining target query quota: {}"
            
        # 1. 枚举子集包含查询 (Si ⊆ Sj)
        for i in range(1, self.m + 1):
            for j in range(1, self.m + 1):
                query_xml = f"<query_subset>{i},{j}</query_subset>"
                
                # 逻辑判断：Si 是否是 Sj 的子集
                is_subset = self._is_subset_of(i, j)
                ans = yes_res if is_subset else no_res
                
                queries.append({
                    "query": query_xml,
                    "answer": ans
                })
        
        # 2. 枚举目标包含查询 (Si ⊆ K)
        # 模拟递减的 budget 以保持一致性
        simulated_budget = self.budget
        for i in range(1, self.m + 1):
            query_xml = f"<query_target>{i}</query_target>"
            
            # 逻辑判断：Si 是否是 K 的子集
            in_target = (self.target_containment[i - 1] == 1)
            result = yes_res if in_target else no_res
            
            simulated_budget -= 1
            budget_msg = budget_info_tpl.format(simulated_budget)
            
            ans = f"{result}\n{budget_msg}"
            
            queries.append({
                "query": query_xml,
                "answer": ans
            })
            
        return queries