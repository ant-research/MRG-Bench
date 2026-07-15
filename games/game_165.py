from .base import Game
import re
import itertools
import random as _random

class EquivalenceClassGame(Game):

    game_rule_zh = """\
我们现在来玩一个"等价类划分推理"游戏，规则如下：

游戏设定了一个有限集合 S = {{1, 2, ..., {n}}}。这个集合被一个未知的等价关系划分为若干个不相交的等价类。等价关系满足自反性、对称性和传递性，每个元素恰好属于一个等价类。

你的目标是通过查询推断出完整的等价类划分。你可以反复向我提出以下三类问题（每次可以提一个问题），我会根据真实设定如实回答：

1. 两元素等价判定（类型 A）：询问编号 i 和 j 是否属于同一等价类（要求 i 小于 j）。回答"是"或"否"。
2. 子集内等价类数量（类型 B）：询问给定子集中包含多少个不同的等价类。回答一个整数。
3. 子集中与锚等价的数量（类型 C）：询问给定子集中有多少个元素与指定的锚元素属于同一等价类（含锚本身）。回答一个整数。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 两元素等价判定（例如问编号 2 和 5 是否等价）：
<query_pair>2,5</query_pair>

- 子集内等价类数量（例如问子集 {{1,3,5}} 中有多少个等价类）：
<query_subset_count>1,3,5</query_subset_count>

- 子集中与锚等价的数量（例如问子集 {{2,4,6,8}} 中有多少个与锚 4 等价）：
<query_anchor>4|2,4,6,8</query_anchor>

提交最终答案时，必须列出所有等价类，每个等价类用花括号包围，编号用逗号隔开且按递增顺序排列，等价类之间用竖线隔开，格式如下：

<answer>{{1,2,3}}|{{4,5}}|{{6}}</answer>

注意：等价类的顺序不影响判定，但每个等价类内的编号必须递增排列。
"""

    game_rule_en = """\
Let's play an "Equivalence Class Partition Inference" game. Here are the rules:

There is a finite set S = {{1, 2, ..., {n}}}. This set is partitioned by an unknown equivalence relation into several disjoint equivalence classes. The equivalence relation satisfies reflexivity, symmetry, and transitivity, and each element belongs to exactly one equivalence class.

Your goal is to infer the complete equivalence class partition through queries. You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully:

1. Pairwise Equivalence Check (Type A): Ask if elements i and j belong to the same equivalence class (requires i less than j). Answer "Yes" or "No".
2. Subset Class Count (Type B): Ask how many distinct equivalence classes exist in a given subset. Answer an integer.
3. Anchor Equivalence Count (Type C): Ask how many elements in a given subset belong to the same equivalence class as a specified anchor element (including the anchor itself). Answer an integer.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Pairwise Equivalence Check (e.g., asking if 2 and 5 are equivalent):
<query_pair>2,5</query_pair>

- Subset Class Count (e.g., asking how many classes in subset {{1,3,5}}):
<query_subset_count>1,3,5</query_subset_count>

- Anchor Equivalence Count (e.g., asking how many in subset {{2,4,6,8}} are equivalent to anchor 4):
<query_anchor>4|2,4,6,8</query_anchor>

When submitting the final answer, list all equivalence classes with each class enclosed in curly braces, elements comma-separated in ascending order, and classes separated by vertical bars:

<answer>{{1,2,3}}|{{4,5}}|{{6}}</answer>

Note: The order of classes does not matter, but elements within each class must be in ascending order.
"""

    contextualized_rule_zh_1 = """\
欢迎进入智能交通运输调度系统。我们正在进行"车队归属划分推理"分析，排查规则如下：

系统记录了一个由 {{1, 2, ..., {n}}} 组成的车辆集合 S。由于中枢故障，车队编组信息丢失。已知这些车辆原本被划分为若干个互不相交的车队。同一车队内的车辆归属关系满足自反性、对称性和传递性，每辆车恰好属于一个单独的车队。

你的目标是通过数据查询推断出完整的车队编组。你可以反复向我提出以下三类问题（每次可以提一个问题），我会根据底层系统数据如实回答：

1. 两车同队判定（类型 A）：询问车辆编号 i 和 j 是否属于同一车队（要求 i 小于 j）。回答"是"或"否"。
2. 车队数量统计（类型 B）：询问给定车辆子集中包含多少个不同的车队。回答一个整数。
3. 同队车辆计数（类型 C）：询问给定车辆子集中有多少辆车与指定的锚点车辆属于同一车队（含锚点本身）。回答一个整数。

当你收集足够信息后，请提交最终的车队编组答案。若答案错误或格式不符，排查任务失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 两车同队判定（例如问车辆 2 和 5 是否同队）：
<query_pair>2,5</query_pair>

- 车队数量统计（例如问车辆子集 {{1,3,5}} 中涉及多少个车队）：
<query_subset_count>1,3,5</query_subset_count>

- 同队车辆计数（例如问车辆子集 {{2,4,6,8}} 中有多少辆与锚点车 4 同队）：
<query_anchor>4|2,4,6,8</query_anchor>

提交最终答案时，必须列出所有车队，每个车队用花括号包围，编号用逗号隔开且按递增顺序排列，车队之间用竖线隔开，格式如下：

<answer>{{1,2,3}}|{{4,5}}|{{6}}</answer>

注意：车队的排列顺序不影响判定，但每个车队内的车辆编号必须递增排列。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the Intelligent Transportation Dispatch System. We are conducting a "Fleet Affiliation Partition Inference" analysis. The diagnostic rules are as follows:

The system recorded a fleet of vehicles S = {{1, 2, ..., {n}}}. Due to a mainframe fault, the fleet grouping data has been lost. It is known that these vehicles are partitioned into several disjoint transit fleets. The fleet affiliation satisfies reflexivity, symmetry, and transitivity, and each vehicle belongs to exactly one fleet.

Your goal is to infer the complete fleet grouping through data queries. You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully based on the underlying system data:

1. Pairwise Fleet Check (Type A): Ask if vehicle i and j belong to the same fleet (requires i less than j). Answer "Yes" or "No".
2. Subset Fleet Count (Type B): Ask how many distinct fleets exist in a given subset of vehicles. Answer an integer.
3. Anchor Fleet Count (Type C): Ask how many vehicles in a given subset belong to the same fleet as a specified anchor vehicle (including the anchor itself). Answer an integer.

When you have enough information, submit your final fleet grouping. If the answer is wrong or the format is invalid, the diagnostic task fails.

Each query must contain only one tag. Use the following XML format:

- Pairwise Fleet Check (e.g., asking if vehicles 2 and 5 are in the same fleet):
<query_pair>2,5</query_pair>

- Subset Fleet Count (e.g., asking how many fleets are in subset {{1,3,5}}):
<query_subset_count>1,3,5</query_subset_count>

- Anchor Fleet Count (e.g., asking how many in subset {{2,4,6,8}} share a fleet with anchor 4):
<query_anchor>4|2,4,6,8</query_anchor>

When submitting the final answer, list all fleets with each group enclosed in curly braces, elements comma-separated in ascending order, and groups separated by vertical bars:

<answer>{{1,2,3}}|{{4,5}}|{{6}}</answer>

Note: The order of fleets does not matter, but vehicle IDs within each fleet must be in ascending order.
"""

    contextualized_rule_zh_2 = """\
欢迎进入流行病学调查系统。我们正在进行"病毒毒株划分推理"分析，排查规则如下：

系统记录了一个由 {{1, 2, ..., {n}}} 组成的患者集合 S。由于数据混淆，毒株类型的映射信息丢失。已知这些患者感染了若干种互不相交的病毒毒株。同源感染关系满足自反性、对称性和传递性，每位患者恰好感染一种毒株。

你的目标是通过数据查询推断出完整的毒株群体划分。你可以反复向我提出以下三类问题（每次可以提一个问题），我会根据底层系统数据如实回答：

1. 感染同源判定（类型 A）：询问患者编号 i 和 j 是否感染同种毒株（要求 i 小于 j）。回答"是"或"否"。
2. 毒株种类统计（类型 B）：询问给定患者子集中包含多少种不同的毒株。回答一个整数。
3. 同源患者计数（类型 C）：询问给定患者子集中有多少人与指定的锚点患者感染了同种毒株（含锚点本身）。回答一个整数。

当你收集足够信息后，请提交最终的毒株群体划分答案。若答案错误或格式不符，排查任务失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 感染同源判定（例如问患者 2 和 5 是否感染同种毒株）：
<query_pair>2,5</query_pair>

- 毒株种类统计（例如问患者子集 {{1,3,5}} 中涉及多少种毒株）：
<query_subset_count>1,3,5</query_subset_count>

- 同源患者计数（例如问患者子集 {{2,4,6,8}} 中有多少人与锚点患者 4 感染同源）：
<query_anchor>4|2,4,6,8</query_anchor>

提交最终答案时，必须列出所有毒株群体，每个群体用花括号包围，编号用逗号隔开且按递增顺序排列，群体之间用竖线隔开，格式如下：

<answer>{{1,2,3}}|{{4,5}}|{{6}}</answer>

注意：群体的排列顺序不影响判定，但每个群体内的患者编号必须递增排列。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the Epidemiological Investigation System. We are conducting a "Virus Strain Partition Inference" analysis. The diagnostic rules are as follows:

The system recorded a set of patients S = {{1, 2, ..., {n}}}. Due to data obfuscation, the mapping of strain types has been lost. It is known that these patients are infected by several disjoint virus strains. The homologous infection relation satisfies reflexivity, symmetry, and transitivity, and each patient is infected with exactly one strain.

Your goal is to infer the complete virus strain partition through data queries. You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully based on the underlying system data:

1. Pairwise Homology Check (Type A): Ask if patient i and j are infected with the same strain (requires i less than j). Answer "Yes" or "No".
2. Subset Strain Count (Type B): Ask how many distinct virus strains exist in a given subset of patients. Answer an integer.
3. Anchor Homology Count (Type C): Ask how many patients in a given subset are infected with the same strain as a specified anchor patient (including the anchor itself). Answer an integer.

When you have enough information, submit your final strain partition. If the answer is wrong or the format is invalid, the diagnostic task fails.

Each query must contain only one tag. Use the following XML format:

- Pairwise Homology Check (e.g., asking if patients 2 and 5 share a strain):
<query_pair>2,5</query_pair>

- Subset Strain Count (e.g., asking how many strains are in subset {{1,3,5}}):
<query_subset_count>1,3,5</query_subset_count>

- Anchor Homology Count (e.g., asking how many in subset {{2,4,6,8}} share a strain with anchor 4):
<query_anchor>4|2,4,6,8</query_anchor>

When submitting the final answer, list all strain groups with each group enclosed in curly braces, elements comma-separated in ascending order, and groups separated by vertical bars:

<answer>{{1,2,3}}|{{4,5}}|{{6}}</answer>

Note: The order of groups does not matter, but patient IDs within each group must be in ascending order.
"""

    contextualized_rule_zh_3 = """\
欢迎进入教学编组管理系统。我们正在进行"研究小组划分推理"分析，排查规则如下：

系统记录了一个由 {{1, 2, ..., {n}}} 组成的学生集合 S。由于数据迁移，编组映射信息丢失。已知这些学生被分入了若干个互不相交的课题研究小组。同组关系满足自反性、对称性和传递性，每位学生恰好属于一个研究小组。

你的目标是通过数据查询推断出完整的研究小组名单。你可以反复向我提出以下三类问题（每次可以提一个问题），我会根据底层系统数据如实回答：

1. 同组判定（类型 A）：询问学生编号 i 和 j 是否在同一个研究小组（要求 i 小于 j）。回答"是"或"否"。
2. 小组数量统计（类型 B）：询问给定学生子集中包含多少个不同的研究小组。回答一个整数。
3. 同组学生计数（类型 C）：询问给定学生子集中有多少人与指定的锚点学生同属一个小组（含锚点本身）。回答一个整数。

当你收集足够信息后，请提交最终的研究小组名单答案。若答案错误或格式不符，排查任务失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 同组判定（例如问学生 2 和 5 是否同组）：
<query_pair>2,5</query_pair>

- 小组数量统计（例如问学生子集 {{1,3,5}} 中涉及多少个小组）：
<query_subset_count>1,3,5</query_subset_count>

- 同组学生计数（例如问学生子集 {{2,4,6,8}} 中有多少人与锚点学生 4 同组）：
<query_anchor>4|2,4,6,8</query_anchor>

提交最终答案时，必须列出所有研究小组，每个小组用花括号包围，编号用逗号隔开且按递增顺序排列，小组之间用竖线隔开，格式如下：

<answer>{{1,2,3}}|{{4,5}}|{{6}}</answer>

注意：小组的排列顺序不影响判定，但每个小组内的学生编号必须递增排列。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Educational Grouping Management System. We are conducting a "Research Group Partition Inference" analysis. The diagnostic rules are as follows:

The system recorded a set of students S = {{1, 2, ..., {n}}}. Due to data migration, the grouping mapping has been lost. It is known that these students are assigned to several disjoint research groups. The co-grouping relation satisfies reflexivity, symmetry, and transitivity, and each student belongs to exactly one research group.

Your goal is to infer the complete research grouping through data queries. You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully based on the underlying system data:

1. Pairwise Group Check (Type A): Ask if student i and j belong to the same research group (requires i less than j). Answer "Yes" or "No".
2. Subset Group Count (Type B): Ask how many distinct research groups exist in a given subset of students. Answer an integer.
3. Anchor Group Count (Type C): Ask how many students in a given subset belong to the same research group as a specified anchor student (including the anchor itself). Answer an integer.

When you have enough information, submit your final group lists. If the answer is wrong or the format is invalid, the diagnostic task fails.

Each query must contain only one tag. Use the following XML format:

- Pairwise Group Check (e.g., asking if students 2 and 5 are in the same group):
<query_pair>2,5</query_pair>

- Subset Group Count (e.g., asking how many groups are represented in subset {{1,3,5}}):
<query_subset_count>1,3,5</query_subset_count>

- Anchor Group Count (e.g., asking how many in subset {{2,4,6,8}} share a group with anchor 4):
<query_anchor>4|2,4,6,8</query_anchor>

When submitting the final answer, list all groups with each group enclosed in curly braces, elements comma-separated in ascending order, and groups separated by vertical bars:

<answer>{{1,2,3}}|{{4,5}}|{{6}}</answer>

Note: The order of groups does not matter, but student IDs within each group must be in ascending order.
"""

    contextualized_rule_zh_4 = """\
欢迎进入工业质量溯源系统。我们正在进行"生产批次划分推理"分析，排查规则如下：

系统记录了一个由 {{1, 2, ..., {n}}} 组成的零件集合 S。由于标签磨损，批次溯源信息丢失。已知这些零件来自于若干个互不相交的生产批次。同批次关系满足自反性、对称性和传递性，每个零件恰好属于一个生产批次。

你的目标是通过数据查询推断出完整的生产批次划分。你可以反复向我提出以下三类问题（每次可以提一个问题），我会根据底层系统数据如实回答：

1. 同批次判定（类型 A）：询问零件编号 i 和 j 是否属于同一生产批次（要求 i 小于 j）。回答"是"或"否"。
2. 批次数量统计（类型 B）：询问给定零件子集中包含多少个不同的生产批次。回答一个整数。
3. 同批次零件计数（类型 C）：询问给定零件子集中有多少个零件与指定的锚点零件属于同一批次（含锚点本身）。回答一个整数。

当你收集足够信息后，请提交最终的生产批次答案。若答案错误或格式不符，排查任务失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 同批次判定（例如问零件 2 和 5 是否同批次）：
<query_pair>2,5</query_pair>

- 批次数量统计（例如问零件子集 {{1,3,5}} 中涉及多少个批次）：
<query_subset_count>1,3,5</query_subset_count>

- 同批次零件计数（例如问零件子集 {{2,4,6,8}} 中有多少个零件与锚点零件 4 同批次）：
<query_anchor>4|2,4,6,8</query_anchor>

提交最终答案时，必须列出所有批次，每个批次用花括号包围，编号用逗号隔开且按递增顺序排列，批次之间用竖线隔开，格式如下：

<answer>{{1,2,3}}|{{4,5}}|{{6}}</answer>

注意：批次的排列顺序不影响判定，但每个批次内的零件编号必须递增排列。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Industrial Quality Traceability System. We are conducting a "Production Batch Partition Inference" analysis. The diagnostic rules are as follows:

The system recorded a set of components S = {{1, 2, ..., {n}}}. Due to label wear, the batch traceability data has been lost. It is known that these components originate from several disjoint production batches. The co-batch relation satisfies reflexivity, symmetry, and transitivity, and each component belongs to exactly one production batch.

Your goal is to infer the complete production batch grouping through data queries. You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully based on the underlying system data:

1. Pairwise Batch Check (Type A): Ask if component i and j belong to the same production batch (requires i less than j). Answer "Yes" or "No".
2. Subset Batch Count (Type B): Ask how many distinct production batches exist in a given subset of components. Answer an integer.
3. Anchor Batch Count (Type C): Ask how many components in a given subset belong to the same batch as a specified anchor component (including the anchor itself). Answer an integer.

When you have enough information, submit your final batch grouping. If the answer is wrong or the format is invalid, the diagnostic task fails.

Each query must contain only one tag. Use the following XML format:

- Pairwise Batch Check (e.g., asking if components 2 and 5 are from the same batch):
<query_pair>2,5</query_pair>

- Subset Batch Count (e.g., asking how many batches are represented in subset {{1,3,5}}):
<query_subset_count>1,3,5</query_subset_count>

- Anchor Batch Count (e.g., asking how many in subset {{2,4,6,8}} share a batch with anchor 4):
<query_anchor>4|2,4,6,8</query_anchor>

When submitting the final answer, list all batches with each batch enclosed in curly braces, elements comma-separated in ascending order, and batches separated by vertical bars:

<answer>{{1,2,3}}|{{4,5}}|{{6}}</answer>

Note: The order of batches does not matter, but component IDs within each batch must be in ascending order.
"""

    contextualized_rule_zh_5 = """\
欢迎进入司法案件并案分析系统。我们正在进行"系列并案划分推理"分析，排查规则如下：

系统记录了一个由 {{1, 2, ..., {n}}} 组成的案卷集合 S。由于档案重组，关联并案信息丢失。已知这些案卷被归并为若干个互不相交的系列并案。同案关系满足自反性、对称性和传递性，每份案卷恰好属于一个系列并案。

你的目标是通过数据查询推断出完整的系列并案划分。你可以反复向我提出以下三类问题（每次可以提一个问题），我会根据底层系统数据如实回答：

1. 同案判定（类型 A）：询问案卷编号 i 和 j 是否属于同一个系列并案（要求 i 小于 j）。回答"是"或"否"。
2. 并案数量统计（类型 B）：询问给定案卷子集中包含多少个不同的系列并案。回答一个整数。
3. 同案案卷计数（类型 C）：询问给定案卷子集中有多少份案卷与指定的锚点主案卷属于同一并案（含锚点本身）。回答一个整数。

当你收集足够信息后，请提交最终的系列并案答案。若答案错误或格式不符，排查任务失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 同案判定（例如问案卷 2 和 5 是否同案）：
<query_pair>2,5</query_pair>

- 并案数量统计（例如问案卷子集 {{1,3,5}} 中涉及多少个并案）：
<query_subset_count>1,3,5</query_subset_count>

- 同案案卷计数（例如问案卷子集 {{2,4,6,8}} 中有多少份与锚点案卷 4 同案）：
<query_anchor>4|2,4,6,8</query_anchor>

提交最终答案时，必须列出所有系列并案，每个并案用花括号包围，编号用逗号隔开且按递增顺序排列，并案之间用竖线隔开，格式如下：

<answer>{{1,2,3}}|{{4,5}}|{{6}}</answer>

注意：并案的排列顺序不影响判定，但每个并案内的案卷编号必须递增排列。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the Judicial Case Consolidation System. We are conducting a "Consolidated Proceeding Partition Inference" analysis. The diagnostic rules are as follows:

The system recorded a set of legal dossiers S = {{1, 2, ..., {n}}}. Due to archival restructuring, the consolidation mapping has been lost. It is known that these dossiers are merged into several disjoint consolidated cases. The consolidation relation satisfies reflexivity, symmetry, and transitivity, and each dossier belongs to exactly one consolidated case.

Your goal is to infer the complete consolidation grouping through data queries. You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully based on the underlying system data:

1. Pairwise Consolidation Check (Type A): Ask if dossier i and j belong to the same consolidated case (requires i less than j). Answer "Yes" or "No".
2. Subset Case Count (Type B): Ask how many distinct consolidated cases exist in a given subset of dossiers. Answer an integer.
3. Anchor Dossier Count (Type C): Ask how many dossiers in a given subset belong to the same consolidated case as a specified anchor dossier (including the anchor itself). Answer an integer.

When you have enough information, submit your final consolidation grouping. If the answer is wrong or the format is invalid, the diagnostic task fails.

Each query must contain only one tag. Use the following XML format:

- Pairwise Consolidation Check (e.g., asking if dossiers 2 and 5 belong to the same case):
<query_pair>2,5</query_pair>

- Subset Case Count (e.g., asking how many consolidated cases are represented in subset {{1,3,5}}):
<query_subset_count>1,3,5</query_subset_count>

- Anchor Dossier Count (e.g., asking how many in subset {{2,4,6,8}} share a case with anchor 4):
<query_anchor>4|2,4,6,8</query_anchor>

When submitting the final answer, list all consolidated cases with each case enclosed in curly braces, elements comma-separated in ascending order, and cases separated by vertical bars:

<answer>{{1,2,3}}|{{4,5}}|{{6}}</answer>

Note: The order of consolidated cases does not matter, but dossier IDs within each case must be in ascending order.
"""

    tags = ["answer", "query_pair", "query_subset_count", "query_anchor"]

    reasoning_type = "演绎推理"
    data_structure = "集合"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "partition": [[1, 2], [3, 4]],
            },
            2: {
                "n": 6,
                "partition": [[1, 3], [2, 5], [4, 6]],
            },
            3: {
                "n": 8,
                "partition": [[1, 4, 7], [2, 5], [3, 6, 8]],
            },
            4: {
                "n": 10,
                "partition": [[1, 5], [2, 6, 9], [3, 7], [4, 8, 10]],
            },
            5: {
                "n": 12,
                "partition": [[1, 7], [2, 8, 11], [3, 9], [4, 10], [5, 6, 12]],
            },
        },
        "en": {
            1: {
                "n": 4,
                "partition": [[1, 2], [3, 4]],
            },
            2: {
                "n": 6,
                "partition": [[1, 3], [2, 5], [4, 6]],
            },
            3: {
                "n": 8,
                "partition": [[1, 4, 7], [2, 5], [3, 6, 8]],
            },
            4: {
                "n": 10,
                "partition": [[1, 5], [2, 6, 9], [3, 7], [4, 8, 10]],
            },
            5: {
                "n": 12,
                "partition": [[1, 7], [2, 8, 11], [3, 9], [4, 10], [5, 6, 12]],
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    @staticmethod
    def _generate_partition(n, num_classes, seed=42):
        rng = _random.Random(seed)
        elements = list(range(1, n + 1))
        rng.shuffle(elements)
        partition = [[] for _ in range(num_classes)]
        for i, elem in enumerate(elements):
            partition[i % num_classes].append(elem)
        for cls in partition:
            cls.sort()
        return partition

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        
        num_classes = len(cfg["partition"])
        self.partition = self._generate_partition(cfg["n"], num_classes, seed=diff * 1000 + cfg["n"])
        
        self.element_to_class = {}
        for class_id, equiv_class in enumerate(self.partition):
            for elem in equiv_class:
                self.element_to_class[elem] = class_id

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        n = self._game_info["n"]
        full_set = range(1, n + 1)
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        for i, j in itertools.combinations(full_set, 2):
            query_content = f"{i},{j}"
            is_same_class = self.element_to_class[i] == self.element_to_class[j]
            ans = yes_res if is_same_class else no_res
            
            queries.append({
                "query": f"<query_pair>{query_content}</query_pair>",
                "answer": ans
            })

        max_subset_size = min(4, n)
        for r in range(1, max_subset_size + 1):
            for subset in itertools.combinations(full_set, r):
                subset_list = list(subset)
                subset_str = ",".join(map(str, subset_list))
                
                classes_in_subset = set(self.element_to_class[x] for x in subset_list)
                ans_b = str(len(classes_in_subset))
                
                queries.append({
                    "query": f"<query_subset_count>{subset_str}</query_subset_count>",
                    "answer": ans_b
                })
                
                for anchor in subset_list:
                    anchor_class = self.element_to_class[anchor]
                    count = sum(1 for x in subset_list if self.element_to_class[x] == anchor_class)
                    ans_c = str(count)
                    
                    queries.append({
                        "query": f"<query_anchor>{anchor}|{subset_str}</query_anchor>",
                        "answer": ans_c
                    })
                    
        return queries

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        try:
            pattern = r'\{([^}]+)\}'
            matches = re.findall(pattern, raw_ans)
            
            if not matches:
                return False
            
            submitted_partition = []
            all_elements = set()
            
            for match in matches:
                elements = [int(x.strip()) for x in match.split(',') if x.strip()]
                if not elements:
                    return False
                
                for elem in elements:
                    if elem in all_elements:
                        return False
                    all_elements.add(elem)
                
                submitted_partition.append(sorted(elements))
            
            if all_elements != set(range(1, self._game_info["n"] + 1)):
                return False
            
            submitted_partition_normalized = sorted([sorted(cls) for cls in submitted_partition])
            correct_partition_normalized = sorted([sorted(cls) for cls in self.partition])
            
            return submitted_partition_normalized == correct_partition_normalized
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            invalid_res = "无效查询"
        else:
            yes_res, no_res = "Yes", "No"
            invalid_res = "Invalid query"

        if "query_pair" in parsed_info:
            return self._handle_pair_query(parsed_info["query_pair"], yes_res, no_res, invalid_res)
        
        elif "query_subset_count" in parsed_info:
            return self._handle_subset_count_query(parsed_info["query_subset_count"], invalid_res)
        
        elif "query_anchor" in parsed_info:
            return self._handle_anchor_query(parsed_info["query_anchor"], invalid_res)
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            elif correct == "否":
                return "是"
        else:
            if correct.lower() == "yes":
                return "No"
            elif correct.lower() == "no":
                return "Yes"
        
        return correct + "_WRONG"

    def _handle_pair_query(self, query_str, yes_res, no_res, invalid_res):
        try:
            parts = [x.strip() for x in query_str.split(',')]
            if len(parts) != 2:
                return invalid_res
            
            i, j = int(parts[0]), int(parts[1])
            
            if i < 1 or i > self._game_info["n"] or j < 1 or j > self._game_info["n"]:
                return invalid_res
            if i >= j:
                return invalid_res
            
            return yes_res if self.element_to_class[i] == self.element_to_class[j] else no_res
            
        except Exception:
            return invalid_res

    def _handle_subset_count_query(self, query_str, invalid_res):
        try:
            elements = [int(x.strip()) for x in query_str.split(',') if x.strip()]
            
            if not elements:
                return invalid_res
            
            if len(elements) != len(set(elements)):
                return invalid_res
            
            for elem in elements:
                if elem < 1 or elem > self._game_info["n"]:
                    return invalid_res
            
            classes = set(self.element_to_class[elem] for elem in elements)
            return str(len(classes))
            
        except Exception:
            return invalid_res

    def _handle_anchor_query(self, query_str, invalid_res):
        try:
            parts = query_str.split('|')
            if len(parts) != 2:
                return invalid_res
            
            anchor = int(parts[0].strip())
            elements = [int(x.strip()) for x in parts[1].split(',') if x.strip()]
            
            if not elements:
                return invalid_res
            
            if len(elements) != len(set(elements)):
                return invalid_res
            
            for elem in elements:
                if elem < 1 or elem > self._game_info["n"]:
                    return invalid_res
            
            if anchor < 1 or anchor > self._game_info["n"]:
                return invalid_res
            
            anchor_class = self.element_to_class[anchor]
            count = sum(1 for elem in elements if self.element_to_class[elem] == anchor_class)
            return str(count)
            
        except Exception:
            return invalid_res

