from .base import Game
import random
import re
from itertools import combinations

class SetIntersectionReasoningGame(Game):
    reasoning_type = "溯因推理"
    data_structure = "集合"

    game_rule_zh = """\
我们现在来玩一个"集合交集推理"游戏，规则如下：

游戏设定了一个包含 10 个元素的集合 U = {{x1, x2, x3, x4, x5, x6, x7, x8, x9, x10}}。

已知三个固定子集：
- A = {x1, x2, x3, x6}
- B = {x2, x3, x4, x7, x8}
- C = {x1, x3, x5, x8, x9}

我已经从以下四个候选集合中秘密选择了一个作为目标集合 T：
- T1 = {x2, x3}
- T2 = {x1, x3}
- T3 = {x3, x8}
- T4 = {x3}

你的目标是通过查询来确定 T 是哪一个候选集合，并给出该集合的完整元素列表。

你可以发起计数查询，每次查询时提供一个子集 S（S 是 U 的子集），我会告诉你 S 与目标集合 T 的交集中有多少个元素。

查询限制：
- 每次查询的子集 S 必须包含 2 到 6 个元素
- 元素必须来自 U（即 x1 到 x10）
- 你必须进行至少 2 次查询后才能提交答案
- 最多可以进行 6 次查询
- 你需要用尽可能少的查询次数找到答案

每次查询时，使用以下 XML 格式提供元素列表（用逗号分隔）：

<query>x1,x3,x5</query>

我会返回一个整数，表示你查询的集合与目标集合 T 的交集大小。

当你确定答案后，请提交最终答案，格式如下（指定候选编号和完整元素集合）：

<answer>candidate=T1, elements=x2,x3</answer>

注意：
- 候选编号必须是 T1、T2、T3 或 T4 之一
- 元素列表顺序不限，但必须完整且准确
- 如果查询不符合规则（如元素数量不对、包含非法元素）或答案错误，游戏失败
"""

    game_rule_en = """\
Let's play a "Set Intersection Reasoning" game. Here are the rules:

The game involves a universal set U = {{x1, x2, x3, x4, x5, x6, x7, x8, x9, x10}} containing 10 elements.

Three fixed subsets are known:
- A = {x1, x2, x3, x6}
- B = {x2, x3, x4, x7, x8}
- C = {x1, x3, x5, x8, x9}

I have secretly selected one target set T from the following four candidates:
- T1 = {x2, x3}
- T2 = {x1, x3}
- T3 = {x3, x8}
- T4 = {x3}

Your goal is to determine which candidate T is through queries, and provide the complete list of elements in that set.

You can make counting queries. For each query, you provide a subset S (where S is a subset of U), and I will tell you how many elements are in the intersection of S and the target set T.

Query constraints:
- Each query subset S must contain between 2 and 6 elements
- Elements must be from U (i.e., x1 to x10)
- You must make at least 2 queries before submitting an answer
- You can make at most 6 queries
- You should find the answer using as few queries as possible

For each query, use the following XML format to provide the element list (comma-separated):

<query>x1,x3,x5</query>

I will return an integer indicating the size of the intersection between your queried set and the target set T.

When you determine the answer, submit your final answer in this format (specify candidate ID and complete element set):

<answer>candidate=T1, elements=x2,x3</answer>

Notes:
- Candidate ID must be one of T1, T2, T3, or T4
- Element list order doesn't matter, but must be complete and accurate
- If the query violates rules (e.g., wrong number of elements, illegal elements) or the answer is incorrect, the game fails
"""

    contextualized_rule_zh_1 = """\
智能交通管控系统正在进行"关键故障节点排查"任务，规则如下：

辖区内共有 10 个核心交通监控节点，构成全集 U = {{x1, x2, x3, x4, x5, x6, x7, x8, x9, x10}}。

根据系统初步诊断，已知三个固定特征子集：
- A（近期发生拥堵的节点） = {x1, x2, x3, x6}
- B（传感器报警的节点） = {x2, x3, x4, x7, x8}
- C（处于通信异常状态的节点） = {x1, x3, x5, x8, x9}

系统已将引发区域瘫痪的核心故障集合锁定为以下四个候选目标 T 之一：
- T1 = {x2, x3}
- T2 = {x1, x3}
- T3 = {x3, x8}
- T4 = {x3}

你的目标是通过调用"节点交叉探查"指令，确定实际的核心故障集合 T 是哪一个候选集合，并给出该集合的完整节点列表。

你可以发起探查查询，每次提供一个节点子集 S（S 是 U 的子集），系统将返回 S 与目标故障集合 T 的交集中包含了多少个实际故障节点。

探查限制：
- 每次探查的子集 S 必须包含 2 到 6 个节点
- 节点必须来自全集 U（即 x1 到 x10）
- 你必须进行至少 2 次探查后才能提交最终报告
- 最多可以进行 6 次探查
- 你需要用尽可能少的探查次数准确定位故障集合

每次探查时，使用以下 XML 格式提供节点列表（用逗号分隔）：

<query>x1,x3,x5</query>

系统会返回一个整数，表示你探查的集合与目标故障集合 T 的交集大小。

当你确定答案后，请提交最终报告，格式如下（指定候选编号和完整节点集合）：

<answer>candidate=T1, elements=x2,x3</answer>

注意：
- 候选编号必须是 T1、T2、T3 或 T4 之一
- 节点列表顺序不限，但必须完整且准确
- 如果探查不符合规则（如节点数量不对、包含非法节点）或最终报告错误，排查任务失败
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The Intelligent Traffic Control System is conducting a "Critical Failure Node Isolation" task. The rules are as follows:

There are 10 core traffic monitoring nodes in the district, forming the universal set U = {{x1, x2, x3, x4, x5, x6, x7, x8, x9, x10}}.

Based on preliminary system diagnostics, three fixed feature subsets are known:
- A (Nodes with recent congestion) = {x1, x2, x3, x6}
- B (Nodes with sensor alarms) = {x2, x3, x4, x7, x8}
- C (Nodes with communication anomalies) = {x1, x3, x5, x8, x9}

The system has isolated the critical failure set responsible for the regional gridlock to one of the following four candidate targets T:
- T1 = {x2, x3}
- T2 = {x1, x3}
- T3 = {x3, x8}
- T4 = {x3}

Your objective is to determine which candidate T is the actual critical failure set through intersection probes, and provide the complete list of nodes in that set.

You can initiate a probe query. For each query, you provide a subset S (S is a subset of U), and the system will return the number of actual failure nodes in the intersection of S and the target failure set T.

Probe constraints:
- Each probe subset S must contain between 2 and 6 nodes
- Nodes must be from U (i.e., x1 to x10)
- You must make at least 2 probes before submitting the final report
- You can make at most 6 probes
- You should isolate the failure set using as few probes as possible

For each probe, use the following XML format to provide the node list (comma-separated):

<query>x1,x3,x5</query>

The system will return an integer indicating the size of the intersection between your probed set and the target failure set T.

When you have determined the answer, submit your final report in this format (specify candidate ID and complete node set):

<answer>candidate=T1, elements=x2,x3</answer>

Notes:
- Candidate ID must be one of T1, T2, T3, or T4
- Node list order doesn't matter, but must be complete and accurate
- If a probe violates the rules (e.g., wrong number of nodes, illegal nodes) or the final report is incorrect, the isolation task fails
"""

    contextualized_rule_zh_2 = """\
临床决策支持系统正在进行"变异病毒核心感染特征分析"任务，规则如下：

病理学库中共有 10 项初筛临床体征，构成全集 U = {{x1, x2, x3, x4, x5, x6, x7, x8, x9, x10}}。

已知三种已知毒株的典型体征子集：
- A（Alpha 毒株典型体征） = {x1, x2, x3, x6}
- B（Beta 毒株典型体征） = {x2, x3, x4, x7, x8}
- C（Gamma 毒株典型体征） = {x1, x3, x5, x8, x9}

根据最新流行病学调查，已将新型变异毒株的核心特征集合锁定为以下四个候选目标 T 之一：
- T1 = {x2, x3}
- T2 = {x1, x3}
- T3 = {x3, x8}
- T4 = {x3}

你的目标是通过实施"生化靶向检测"，确定新型变异毒株的实际核心特征集合 T 是哪一个候选集合，并给出该集合的完整体征列表。

你可以发起生化检测查询，每次提供一个体征子集 S（S 是 U 的子集），实验室将返回 S 与目标特征集合 T 的交集中包含了多少个实际核心体征。

检测限制：
- 每次检测的子集 S 必须包含 2 到 6 个体征
- 体征必须来自全集 U（即 x1 到 x10）
- 你必须进行至少 2 次检测后才能提交最终诊断
- 最多可以进行 6 次检测
- 你需要用尽可能少的检测次数出具诊断结果

每次检测时，使用以下 XML 格式提供体征列表（用逗号分隔）：

<query>x1,x3,x5</query>

实验室会返回一个整数，表示你检测的集合与目标特征集合 T 的交集大小。

当你确定答案后，请提交最终诊断，格式如下（指定候选编号和完整体征集合）：

<answer>candidate=T1, elements=x2,x3</answer>

注意：
- 候选编号必须是 T1、T2、T3 或 T4 之一
- 体征列表顺序不限，但必须完整且准确
- 如果检测不符合规范（如体征数量不对、包含非法体征）或最终诊断错误，特征分析任务失败
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
The Clinical Decision Support System is conducting a "Mutant Virus Core Infection Feature Analysis" task. The rules are as follows:

There are 10 primary screening clinical signs in the pathology database, forming the universal set U = {{x1, x2, x3, x4, x5, x6, x7, x8, x9, x10}}.

Three known strains exhibit the following typical sign subsets:
- A (Alpha strain signs) = {x1, x2, x3, x6}
- B (Beta strain signs) = {x2, x3, x4, x7, x8}
- C (Gamma strain signs) = {x1, x3, x5, x8, x9}

Based on recent epidemiological surveys, the core feature set of the new mutant strain has been narrowed down to one of the following four candidate targets T:
- T1 = {x2, x3}
- T2 = {x1, x3}
- T3 = {x3, x8}
- T4 = {x3}

Your objective is to determine which candidate T is the actual core feature set of the new mutant strain through "biochemical targeted assays," and provide the complete list of signs in that set.

You can initiate an assay query. For each query, you provide a subset S (where S is a subset of U), and the laboratory will return the number of actual core signs in the intersection of S and the target feature set T.

Assay constraints:
- Each assay subset S must contain between 2 and 6 signs
- Signs must be from U (i.e., x1 to x10)
- You must make at least 2 assays before submitting the final diagnosis
- You can make at most 6 assays
- You should finalize the diagnosis using as few assays as possible

For each assay, use the following XML format to provide the sign list (comma-separated):

<query>x1,x3,x5</query>

The laboratory will return an integer indicating the size of the intersection between your assayed set and the target feature set T.

When you have determined the answer, submit your final diagnosis in this format (specify candidate ID and complete sign set):

<answer>candidate=T1, elements=x2,x3</answer>

Notes:
- Candidate ID must be one of T1, T2, T3, or T4
- Sign list order doesn't matter, but must be complete and accurate
- If an assay violates the protocols (e.g., wrong number of signs, illegal signs) or the final diagnosis is incorrect, the analysis task fails
"""

    contextualized_rule_zh_3 = """\
智能教学测评系统正在进行"期末核心考点预测"任务，规则如下：

本学期的大纲中共包含 10 个基础知识点，构成全集 U = {{x1, x2, x3, x4, x5, x6, x7, x8, x9, x10}}。

已知以往三次模拟测验的高频知识点子集：
- A（模考一高频考点） = {x1, x2, x3, x6}
- B（模考二高频考点） = {x2, x3, x4, x7, x8}
- C（模考三高频考点） = {x1, x3, x5, x8, x9}

根据教学研讨，已将最终期末考试的必考核心知识点集合锁定为以下四个候选目标 T 之一：
- T1 = {x2, x3}
- T2 = {x1, x3}
- T3 = {x3, x8}
- T4 = {x3}

你的目标是通过发起"随堂抽测"，确定期末必考的核心知识点集合 T 是哪一个候选集合，并给出该集合的完整考点列表。

你可以发起抽测查询，每次提供一个知识点子集 S（S 是 U 的子集），系统将返回 S 与目标核心考点集合 T 的交集中包含了多少个实际必考知识点。

抽测限制：
- 每次抽测的子集 S 必须包含 2 到 6 个知识点
- 知识点必须来自全集 U（即 x1 到 x10）
- 你必须进行至少 2 次抽测后才能提交最终预测报告
- 最多可以进行 6 次抽测
- 你需要用尽可能少的抽测次数精准定位必考知识点

每次抽测时，使用以下 XML 格式提供知识点列表（用逗号分隔）：

<query>x1,x3,x5</query>

系统会返回一个整数，表示你抽测的集合与目标必考集合 T 的交集大小。

当你确定答案后，请提交最终预测报告，格式如下（指定候选编号和完整知识点集合）：

<answer>candidate=T1, elements=x2,x3</answer>

注意：
- 候选编号必须是 T1、T2、T3 或 T4 之一
- 知识点列表顺序不限，但必须完整且准确
- 如果抽测不符合规则（如知识点数量不对、包含非法知识点）或最终预测错误，预测任务失败
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The Intelligent Teaching and Assessment System is conducting a "Final Exam Core Topics Prediction" task. The rules are as follows:

The syllabus for this semester contains 10 fundamental knowledge points, forming the universal set U = {{x1, x2, x3, x4, x5, x6, x7, x8, x9, x10}}.

The high-frequency topics from three previous mock exams form the following subsets:
- A (Mock Exam 1 topics) = {x1, x2, x3, x6}
- B (Mock Exam 2 topics) = {x2, x3, x4, x7, x8}
- C (Mock Exam 3 topics) = {x1, x3, x5, x8, x9}

Based on pedagogical reviews, the mandatory core topics for the final exam have been narrowed down to one of the following four candidate targets T:
- T1 = {x2, x3}
- T2 = {x1, x3}
- T3 = {x3, x8}
- T4 = {x3}

Your objective is to determine which candidate T is the actual core topic set for the final exam through "pop quizzes," and provide the complete list of topics in that set.

You can initiate a quiz query. For each query, you provide a subset S (where S is a subset of U), and the system will return the number of actual mandatory topics in the intersection of S and the target core topic set T.

Quiz constraints:
- Each quiz subset S must contain between 2 and 6 topics
- Topics must be from U (i.e., x1 to x10)
- You must administer at least 2 quizzes before submitting the final prediction
- You can administer at most 6 quizzes
- You should accurately pinpoint the mandatory topics using as few quizzes as possible

For each quiz, use the following XML format to provide the topic list (comma-separated):

<query>x1,x3,x5</query>

The system will return an integer indicating the size of the intersection between your quizzed set and the target core topic set T.

When you have determined the answer, submit your final prediction report in this format (specify candidate ID and complete topic set):

<answer>candidate=T1, elements=x2,x3</answer>

Notes:
- Candidate ID must be one of T1, T2, T3, or T4
- Topic list order doesn't matter, but must be complete and accurate
- If a quiz violates the rules (e.g., wrong number of topics, illegal topics) or the final prediction is incorrect, the prediction task fails
"""

    contextualized_rule_zh_4 = """\
工业自动化质检系统正在进行"缺陷零部件批次追溯"任务，规则如下：

流水线上共有 10 种核心零部件批次，构成全集 U = {{x1, x2, x3, x4, x5, x6, x7, x8, x9, x10}}。

已知三个特定供应商批次或工序的子集：
- A（经一号车间加工的批次） = {x1, x2, x3, x6}
- B（由供应商 X 提供的批次） = {x2, x3, x4, x7, x8}
- C（采用旧工艺生产的批次） = {x1, x3, x5, x8, x9}

系统已将引发近期产品不合格的真正缺陷零部件批次集合锁定为以下四个候选目标 T 之一：
- T1 = {x2, x3}
- T2 = {x1, x3}
- T3 = {x3, x8}
- T4 = {x3}

你的目标是通过下发"批次抽样质检"指令，确定真正的缺陷零部件集合 T 是哪一个候选集合，并给出该集合的完整批次列表。

你可以发起抽样查询，每次提供一个零部件批次子集 S（S 是 U 的子集），质检中心将返回 S 与目标缺陷集合 T 的交集中包含了多少个实际缺陷批次。

抽样限制：
- 每次抽样的子集 S 必须包含 2 到 6 个零部件批次
- 批次必须来自全集 U（即 x1 到 x10）
- 你必须进行至少 2 次抽样后才能提交最终追溯报告
- 最多可以进行 6 次抽样
- 你需要用尽可能少的抽样次数完成缺陷批次追溯

每次抽样时，使用以下 XML 格式提供零部件批次列表（用逗号分隔）：

<query>x1,x3,x5</query>

质检中心会返回一个整数，表示你抽样的集合与目标缺陷集合 T 的交集大小。

当你确定答案后，请提交最终追溯报告，格式如下（指定候选编号和完整批次集合）：

<answer>candidate=T1, elements=x2,x3</answer>

注意：
- 候选编号必须是 T1、T2、T3 或 T4 之一
- 批次列表顺序不限，但必须完整且准确
- 如果抽样不符合规范（如批次数量不对、包含非法批次）或最终追溯报告错误，质检追溯任务失败
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
The Industrial Automated Quality Inspection System is conducting a "Defective Component Batch Traceability" task. The rules are as follows:

There are 10 core component batches on the assembly line, forming the universal set U = {{x1, x2, x3, x4, x5, x6, x7, x8, x9, x10}}.

Three specific subsets based on suppliers or processes are known:
- A (Batches processed in Workshop 1) = {x1, x2, x3, x6}
- B (Batches supplied by Vendor X) = {x2, x3, x4, x7, x8}
- C (Batches produced using the old technique) = {x1, x3, x5, x8, x9}

The system has isolated the actual defective component batches causing recent product failures to one of the following four candidate targets T:
- T1 = {x2, x3}
- T2 = {x1, x3}
- T3 = {x3, x8}
- T4 = {x3}

Your objective is to determine which candidate T is the actual set of defective batches through "batch sampling inspections," and provide the complete list of batches in that set.

You can initiate a sampling query. For each query, you provide a subset S (where S is a subset of U), and the QA center will return the number of actual defective batches in the intersection of S and the target defective set T.

Sampling constraints:
- Each sampling subset S must contain between 2 and 6 component batches
- Batches must be from U (i.e., x1 to x10)
- You must conduct at least 2 samplings before submitting the final trace report
- You can conduct at most 6 samplings
- You should complete the traceability task using as few samplings as possible

For each sampling, use the following XML format to provide the batch list (comma-separated):

<query>x1,x3,x5</query>

The QA center will return an integer indicating the size of the intersection between your sampled set and the target defective set T.

When you have determined the answer, submit your final trace report in this format (specify candidate ID and complete batch set):

<answer>candidate=T1, elements=x2,x3</answer>

Notes:
- Candidate ID must be one of T1, T2, T3, or T4
- Batch list order doesn't matter, but must be complete and accurate
- If a sampling violates the protocols (e.g., wrong number of batches, illegal batches) or the final report is incorrect, the traceability task fails
"""

    contextualized_rule_zh_5 = """\
智慧法务辅助系统正在进行"关键定案证据链排查"任务，规则如下：

案卷材料中共有 10 份初步证据，构成全集 U = {{x1, x2, x3, x4, x5, x6, x7, x8, x9, x10}}。

已知三个特定来源的证据子集：
- A（原告方提交的证据） = {x1, x2, x3, x6}
- B（被告方提交的证据） = {x2, x3, x4, x7, x8}
- C（警方现场调取的证据） = {x1, x3, x5, x8, x9}

经过法理分析，已将最终能被法庭采信的核心定案证据集合锁定为以下四个候选目标 T 之一：
- T1 = {x2, x3}
- T2 = {x1, x3}
- T3 = {x3, x8}
- T4 = {x3}

你的目标是通过向合议庭发起"证据预审"，确定核心定案证据集合 T 是哪一个候选集合，并给出该集合的完整证据列表。

你可以发起预审查询，每次提供一个证据子集 S（S 是 U 的子集），合议庭将返回 S 与目标定案集合 T 的交集中包含了多少份实际有效的定案证据。

预审限制：
- 每次预审的子集 S 必须包含 2 到 6 份证据
- 证据必须来自全集 U（即 x1 到 x10）
- 你必须进行至少 2 次预审后才能提交最终法务意见书
- 最多可以进行 6 次预审
- 你需要用尽可能少的预审次数锁定定案证据链

每次预审时，使用以下 XML 格式提供证据列表（用逗号分隔）：

<query>x1,x3,x5</query>

合议庭会返回一个整数，表示你提交预审的集合与目标定案集合 T 的交集大小。

当你确定答案后，请提交最终法务意见书，格式如下（指定候选编号和完整证据集合）：

<answer>candidate=T1, elements=x2,x3</answer>

注意：
- 候选编号必须是 T1、T2、T3 或 T4 之一
- 证据列表顺序不限，但必须完整且准确
- 如果预审不符合规则（如证据数量不对、包含非法证据）或最终意见书错误，证据排查任务失败
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
The Smart Legal Assistant System is conducting a "Decisive Evidence Chain Discovery" task. The rules are as follows:

There are 10 pieces of preliminary evidence in the case file, forming the universal set U = {{x1, x2, x3, x4, x5, x6, x7, x8, x9, x10}}.

Three specific subsets based on their sources are known:
- A (Evidence submitted by the plaintiff) = {x1, x2, x3, x6}
- B (Evidence submitted by the defendant) = {x2, x3, x4, x7, x8}
- C (Evidence collected by the police) = {x1, x3, x5, x8, x9}

Based on jurisprudential analysis, the core set of decisive evidence that will be accepted by the court has been narrowed down to one of the following four candidate targets T:
- T1 = {x2, x3}
- T2 = {x1, x3}
- T3 = {x3, x8}
- T4 = {x3}

Your objective is to determine which candidate T is the actual core decisive evidence set through "preliminary reviews" by the collegiate bench, and provide the complete list of evidence in that set.

You can initiate a preliminary review query. For each query, you provide a subset S (where S is a subset of U), and the collegiate bench will return the number of actually valid decisive pieces of evidence in the intersection of S and the target decisive set T.

Review constraints:
- Each review subset S must contain between 2 and 6 pieces of evidence
- Evidence must be from U (i.e., x1 to x10)
- You must conduct at least 2 reviews before submitting the final legal opinion
- You can conduct at most 6 reviews
- You should lock down the decisive evidence chain using as few reviews as possible

For each review, use the following XML format to provide the evidence list (comma-separated):

<query>x1,x3,x5</query>

The collegiate bench will return an integer indicating the size of the intersection between your reviewed set and the target decisive set T.

When you have determined the answer, submit your final legal opinion in this format (specify candidate ID and complete evidence set):

<answer>candidate=T1, elements=x2,x3</answer>

Notes:
- Candidate ID must be one of T1, T2, T3, or T4
- Evidence list order doesn't matter, but must be complete and accurate
- If a review violates the rules (e.g., wrong number of pieces of evidence, illegal evidence) or the final opinion is incorrect, the evidence discovery task fails
"""

    tags = ["answer", "query"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"target": "T1", "seed": 42},
            2: {"target": "T2", "seed": 43},
            3: {"target": "T3", "seed": 44},
            4: {"target": "T4", "seed": 45},
            5: {"target": "random", "seed": 46},
        },
        "en": {
            1: {"target": "T1", "seed": 42},
            2: {"target": "T2", "seed": 43},
            3: {"target": "T3", "seed": 44},
            4: {"target": "T4", "seed": 45},
            5: {"target": "random", "seed": 46},
        },
    }

    def __init__(self, config):
        self.candidates = {
            "T1": {"x2", "x3"},
            "T2": {"x1", "x3"},
            "T3": {"x3", "x8"},
            "T4": {"x3"},
        }
        
        self.universe = {f"x{i}" for i in range(1, 11)}
        
        self.query_count = 0
        
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        rng = random.Random(cfg["seed"])
        
        if cfg["target"] == "random":
            self.target_key = rng.choice(["T1", "T2", "T3", "T4"])
        else:
            self.target_key = cfg["target"]
        
        self.target_set = self.candidates[self.target_key]
        
        self._game_info = {}

    def evaluate(self, parsed_info):
        if self.query_count < 2:
            return False
        
        raw_ans = parsed_info["answer"]
        
        ans_dict = {}
        
        candidate_match = re.search(r'candidate\s*=\s*(T[1-4])', raw_ans)
        elements_match = re.search(r'elements\s*=\s*(.+)', raw_ans)
        
        if not candidate_match or not elements_match:
            return False
        
        answer_candidate = candidate_match.group(1).strip()
        elements_str = elements_match.group(1).strip()
        
        if answer_candidate not in self.candidates:
            return False
        
        try:
            answer_elements = set(x.strip() for x in elements_str.split(",") if x.strip())
        except:
            return False
        
        return (answer_candidate == self.target_key and 
                answer_elements == self.target_set)

    def _cf_core_produce(self, parsed_info):
        if "query" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        if self.query_count >= 6:
            if self.config.language == "zh":
                raise ValueError("已达到最大查询次数（6次）。")
            else:
                raise ValueError("Maximum number of queries (6) reached.")
        
        raw_query = parsed_info["query"].strip()
        try:
            query_set = set(x.strip() for x in raw_query.split(",") if x.strip())
        except:
            raise ValueError("Invalid query format.")
        
        if len(query_set) < 2 or len(query_set) > 6:
            raise ValueError("Query set must contain between 2 and 6 elements.")
        
        if not query_set.issubset(self.universe):
            invalid_elements = query_set - self.universe
            raise ValueError(f"Query contains invalid elements: {invalid_elements}.")
        
        intersection_size = len(query_set & self.target_set)
        self.query_count += 1
        
        if self.config.language == "zh":
            return f"结果：{intersection_size}"
        else:
            return f"Result: {intersection_size}"

    def _cf_make_wrong(self, correct: str) -> str:
        match = re.search(r'(\d+)', correct)
        if match:
            num = int(match.group(1))
            wrong_num = num + 1
            return correct.replace(match.group(1), str(wrong_num))
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        possible_queries = []
        
        representative_queries = [
            ["x1", "x2"],
            ["x2", "x3"],
            ["x1", "x3", "x8"],
            ["x2", "x8"],
            ["x1", "x3"],
            ["x3", "x8"],
        ]
        
        for combo in representative_queries:
            query_content = ",".join(combo)
            query_str = f"<query>{query_content}</query>"
            query_set = set(combo)
            
            intersection_size = len(query_set & self.target_set)
            
            if self.config.language == "zh":
                ans_str = f"结果：{intersection_size}"
            else:
                ans_str = f"Result: {intersection_size}"
            
            possible_queries.append({
                "query": query_str,
                "answer": ans_str
            })
            
        return possible_queries