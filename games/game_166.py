from .base import Game
import re

class MultisetStatisticsGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "集合"

    game_rule_zh = """\
我们来玩一个"多重集统计量推理"游戏，规则如下：

游戏设定了一个由四种类型物体构成的多重集。每种类型的数量分别记为 c1, c2, c3, c4，均为未知的非负整数。

定义一个统计量 H，它表示同类型物体的无序两两配对数之和。具体计算方式为：对每种类型 i，若该类型有 ci 个物体，则可组成 ci × (ci - 1) / 2 个配对；H 是四种类型配对数的总和。

你的目标是通过提问推断出这四个未知数 c1, c2, c3, c4 的准确值。

你可以进行以下四类提问（每次仅限一个问题）：

1. **查询当前统计量**：询问当前的 H 值。我会回答一个非负整数。

2. **查询临时添加后的统计量**：指定一个类型 i（1到4之间）和一个非负整数 q，询问"如果临时向类型 i 添加 q 个物体后，统计量 H 会变成多少"。我会回答临时添加后的新统计量值 H'。注意：这只是临时计算，不会真正改变原始构成。

3. **查询临时添加的变化量**：指定一个类型 i（1到4之间）和一个非负整数 q，询问"临时向类型 i 添加 q 个物体会使统计量 H 增加多少"。我会回答增加的变化量 Δ。

4. **提交答案**：当你确定答案后，提交你推测的四个数 c1, c2, c3, c4。

请尽可能少地使用提问次数来确定答案。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 查询当前统计量（内容为空）：
<query_h></query_h>

- 查询临时添加后的统计量（例如向类型 2 添加 3 个）：
<query_add_value>type=2, q=3</query_add_value>

- 查询临时添加的变化量（例如向类型 1 添加 1 个）：
<query_add_delta>type=1, q=1</query_add_delta>

- 提交最终答案（四个数用逗号分隔，按 c1, c2, c3, c4 的顺序）：
<answer>c1=5, c2=3, c3=4, c4=2</answer>
"""

    game_rule_en = """\
Let's play a "Multiset Statistics Inference" game. Here are the rules:

The game involves a multiset composed of four types of objects. The quantity of each type is denoted as c1, c2, c3, c4, which are unknown non-negative integers.

A statistic H is defined as the sum of unordered pairwise combinations within each type. Specifically, for each type i with ci objects, the number of pairs is ci × (ci - 1) / 2; H is the total sum of pairs across all four types.

Your goal is to infer the exact values of these four unknown numbers c1, c2, c3, c4 through questioning.

You can ask the following four types of questions (one per turn):

1. **Query Current Statistic**: Ask for the current value of H. I will answer with a non-negative integer.

2. **Query Statistic After Temporary Addition**: Specify a type i (between 1 and 4) and a non-negative integer q, asking "if we temporarily add q objects to type i, what would the statistic H become". I will answer with the new statistic value H' after the temporary addition. Note: This is only a temporary calculation and does not actually change the original composition.

3. **Query Delta of Temporary Addition**: Specify a type i (between 1 and 4) and a non-negative integer q, asking "how much would the statistic H increase if we temporarily add q objects to type i". I will answer with the increase delta Δ.

4. **Submit Answer**: When you are confident, submit your inferred four numbers c1, c2, c3, c4.

Please use as few questions as possible to determine the answer.

Each query must contain only one tag. Use the following XML format:

- Query current statistic (empty content):
<query_h></query_h>

- Query statistic after temporary addition (e.g., adding 3 to type 2):
<query_add_value>type=2, q=3</query_add_value>

- Query delta of temporary addition (e.g., adding 1 to type 1):
<query_add_delta>type=1, q=1</query_add_delta>

- Submit final answer (four numbers comma-separated, in order c1, c2, c3, c4):
<answer>c1=5, c2=3, c3=4, c4=2</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用交通枢纽“同构车辆潜在冲突指数评估系统”。

本枢纽当前停靠了四种类型的车辆（如小客车、公交车、货车、摩托车）。每种车型的数量分别记为 c1, c2, c3, c4，均为未知的非负整数。

为了评估停车区的安全性，系统定义了一个潜在冲突指数 H。它表示同类型车辆之间可能发生的无序两两空间干涉（配对）数之和。具体而言，对每种车型 i，若有 ci 辆车，则存在 ci × (ci - 1) / 2 个潜在冲突对；H 是四种车型的潜在冲突对总和。

你的目标是通过向系统进行参数查询，推断出这四种车型的准确数量 c1, c2, c3, c4。

你可以进行以下四类操作（每次仅限一个操作）：

1. **查询当前冲突指数**：询问当前的 H 值。系统会返回一个非负整数。

2. **查询虚拟调度后的冲突指数**：指定一个车型 i（1到4之间）和一个非负整数 q，询问"如果临时向停车区引流 q 辆车型 i，冲突指数 H 会变成多少"。系统会返回虚拟调度后的新指数 H'。注意：这只是沙盘推演，不改变实际车辆数。

3. **查询虚拟调度的指数变化量**：指定一个车型 i（1到4之间）和一个非负整数 q，询问"临时向停车区引流 q 辆车型 i 会使冲突指数 H 增加多少"。系统会返回增加的差值 Δ。

4. **提交分析报告**：当你确定各车型数量后，提交你推测的四个数 c1, c2, c3, c4。

请尽可能少地使用查询次数来完成评估。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 查询当前冲突指数（内容为空）：
<query_h></query_h>

- 查询虚拟调度后的冲突指数（例如向车型 2 引流 3 辆）：
<query_add_value>type=2, q=3</query_add_value>

- 查询虚拟调度的指数变化量（例如向车型 1 引流 1 辆）：
<query_add_delta>type=1, q=1</query_add_delta>

- 提交最终分析报告（四个数用逗号分隔，按 c1, c2, c3, c4 的顺序）：
<answer>c1=5, c2=3, c3=4, c4=2</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Transit Hub "Homogeneous Vehicle Potential Conflict Index Evaluation System".

The hub currently accommodates four types of vehicles (e.g., cars, buses, trucks, motorcycles). The quantity of each vehicle type is denoted as c1, c2, c3, c4, which are unknown non-negative integers.

To assess the safety of the parking zone, the system defines a potential conflict index H. It represents the sum of unordered pairwise spatial interferences (pairs) among vehicles of the same type. Specifically, for each vehicle type i with ci vehicles, there are ci × (ci - 1) / 2 potential conflict pairs; H is the total sum of conflict pairs across all four vehicle types.

Your objective is to deduce the exact quantities of these four vehicle types, c1, c2, c3, c4, by querying the system parameters.

You can perform the following four types of operations (one per turn):

1. **Query Current Conflict Index**: Ask for the current value of H. The system will return a non-negative integer.

2. **Query Index After Virtual Dispatch**: Specify a vehicle type i (between 1 and 4) and a non-negative integer q, asking "if we virtually route q vehicles of type i into the parking zone, what would the conflict index H become". The system will return the new index H' after the virtual dispatch. Note: This is only a simulation and does not change the actual vehicle count.

3. **Query Index Delta of Virtual Dispatch**: Specify a vehicle type i (between 1 and 4) and a non-negative integer q, asking "how much would the conflict index H increase if we virtually route q vehicles of type i into the zone". The system will return the increase delta Δ.

4. **Submit Analysis Report**: When you are confident in the vehicle counts, submit your inferred four numbers c1, c2, c3, c4.

Please use as few queries as possible to complete the assessment.

Each query must contain only one tag. Use the following XML format:

- Query current conflict index (empty content):
<query_h></query_h>

- Query index after virtual dispatch (e.g., routing 3 vehicles to type 2):
<query_add_value>type=2, q=3</query_add_value>

- Query index delta of virtual dispatch (e.g., routing 1 vehicle to type 1):
<query_add_delta>type=1, q=1</query_add_delta>

- Submit final analysis report (four numbers comma-separated, in order c1, c2, c3, c4):
<answer>c1=5, c2=3, c3=4, c4=2</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎进入医院“同源病原体交叉感染风险评估系统”。

隔离病区目前收治了感染四种不同病原体类型的患者。每种病原体类型的患者人数分别记为 c1, c2, c3, c4，均为未知的非负整数。

为了评估院内感染管控水平，系统定义了一个交叉感染风险基数 H。它表示同类型病原体患者之间可能发生的无序两两接触对数之和。具体而言，对每种病原体类型 i，若有 ci 名患者，则存在 ci × (ci - 1) / 2 个接触配对；H 是四种类型患者的接触配对总和。

你的目标是通过向系统进行参数查询，推断出这四类患者的准确人数 c1, c2, c3, c4。

你可以进行以下四类操作（每次仅限一个操作）：

1. **查询当前风险基数**：询问当前的 H 值。系统会返回一个非负整数。

2. **查询模拟收治后的风险基数**：指定一个病原体类型 i（1到4之间）和一个非负整数 q，询问"如果临时向病区模拟收治 q 名类型 i 的患者，风险基数 H 会变成多少"。系统会返回模拟收治后的新基数 H'。注意：这只是流行病学推演，不改变实际收治人数。

3. **查询模拟收治的基数变化量**：指定一个病原体类型 i（1到4之间）和一个非负整数 q，询问"临时模拟收治 q 名类型 i 的患者会使风险基数 H 增加多少"。系统会返回增加的差值 Δ。

4. **提交流调报告**：当你确定各类型患者人数后，提交你推测的四个数 c1, c2, c3, c4。

请尽可能少地使用查询次数来完成评估。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 查询当前风险基数（内容为空）：
<query_h></query_h>

- 查询模拟收治后的风险基数（例如向类型 2 模拟收治 3 名患者）：
<query_add_value>type=2, q=3</query_add_value>

- 查询模拟收治的基数变化量（例如向类型 1 模拟收治 1 名患者）：
<query_add_delta>type=1, q=1</query_add_delta>

- 提交最终流调报告（四个数用逗号分隔，按 c1, c2, c3, c4 的顺序）：
<answer>c1=5, c2=3, c3=4, c4=2</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Hospital "Homologous Pathogen Cross-Infection Risk Assessment System".

The isolation ward currently admits patients infected with four different types of pathogens. The number of patients for each pathogen type is denoted as c1, c2, c3, c4, which are unknown non-negative integers.

To evaluate the level of nosocomial infection control, the system defines a cross-infection risk baseline H. It represents the sum of unordered pairwise contact combinations among patients with the same pathogen type. Specifically, for each pathogen type i with ci patients, there are ci × (ci - 1) / 2 contact pairs; H is the total sum of contact pairs across all four patient types.

Your objective is to deduce the exact number of patients in these four categories, c1, c2, c3, c4, by querying the system parameters.

You can perform the following four types of operations (one per turn):

1. **Query Current Risk Baseline**: Ask for the current value of H. The system will return a non-negative integer.

2. **Query Baseline After Simulated Admission**: Specify a pathogen type i (between 1 and 4) and a non-negative integer q, asking "if we simulate the admission of q patients of type i to the ward, what would the risk baseline H become". The system will return the new baseline H' after the simulation. Note: This is purely an epidemiological projection and does not change the actual admission numbers.

3. **Query Baseline Delta of Simulated Admission**: Specify a pathogen type i (between 1 and 4) and a non-negative integer q, asking "how much would the risk baseline H increase if we simulate the admission of q patients of type i". The system will return the increase delta Δ.

4. **Submit Epidemiological Report**: When you are confident in the patient counts, submit your inferred four numbers c1, c2, c3, c4.

Please use as few queries as possible to complete the assessment.

Each query must contain only one tag. Use the following XML format:

- Query current risk baseline (empty content):
<query_h></query_h>

- Query baseline after simulated admission (e.g., simulating 3 patients for type 2):
<query_add_value>type=2, q=3</query_add_value>

- Query baseline delta of simulated admission (e.g., simulating 1 patient for type 1):
<query_add_delta>type=1, q=1</query_add_delta>

- Submit final epidemiological report (four numbers comma-separated, in order c1, c2, c3, c4):
<answer>c1=5, c2=3, c3=4, c4=2</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用高校“跨学科交流同侪配对潜力分析系统”。

本次跨学科研讨会招募了来自四个不同学科大类（如文、理、工、商）的学生。每个学科的报名人数分别记为 c1, c2, c3, c4，均为未知的非负整数。

为了评估研讨会的内部学术探讨氛围，系统定义了一个同侪交流基数 H。它表示同专业学生之间能够组成的两人学术讨论小组的无序配对数之和。具体而言，对每个学科 i，若有 ci 名学生，则可组成 ci × (ci - 1) / 2 个同侪配对；H 是四个学科同侪配对数的总和。

你的目标是通过向系统进行参数查询，推断出这四个学科的准确报名人数 c1, c2, c3, c4。

你可以进行以下四类操作（每次仅限一个操作）：

1. **查询当前交流基数**：询问当前的 H 值。系统会返回一个非负整数。

2. **查询预扩招后的交流基数**：指定一个学科 i（1到4之间）和一个非负整数 q，询问"如果临时向学科 i 扩招 q 名学生，交流基数 H 会变成多少"。系统会返回预扩招后的新基数 H'。注意：这只是沙盘推演，不改变实际报名人数。

3. **查询预扩招的基数变化量**：指定一个学科 i（1到4之间）和一个非负整数 q，询问"临时向学科 i 扩招 q 名学生会使交流基数 H 增加多少"。系统会返回增加的差值 Δ。

4. **提交分析报告**：当你确定各学科报名人数后，提交你推测的四个数 c1, c2, c3, c4。

请尽可能少地使用查询次数来完成评估。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 查询当前交流基数（内容为空）：
<query_h></query_h>

- 查询预扩招后的交流基数（例如向学科 2 扩招 3 名学生）：
<query_add_value>type=2, q=3</query_add_value>

- 查询预扩招的基数变化量（例如向学科 1 扩招 1 名学生）：
<query_add_delta>type=1, q=1</query_add_delta>

- 提交最终分析报告（四个数用逗号分隔，按 c1, c2, c3, c4 的顺序）：
<answer>c1=5, c2=3, c3=4, c4=2</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the University "Interdisciplinary Peer Matching Potential Analysis System".

The current interdisciplinary seminar has enrolled students from four different major categories (e.g., Arts, Sciences, Engineering, Business). The number of enrolled students for each major is denoted as c1, c2, c3, c4, which are unknown non-negative integers.

To evaluate the internal academic discussion atmosphere of the seminar, the system defines a peer communication baseline H. It represents the sum of unordered pairwise two-person academic discussion groups that can be formed among students of the same major. Specifically, for each major i with ci students, ci × (ci - 1) / 2 peer pairs can be formed; H is the total sum of peer pairs across all four majors.

Your objective is to deduce the exact enrollment numbers of these four majors, c1, c2, c3, c4, by querying the system parameters.

You can perform the following four types of operations (one per turn):

1. **Query Current Communication Baseline**: Ask for the current value of H. The system will return a non-negative integer.

2. **Query Baseline After Virtual Expansion**: Specify a major i (between 1 and 4) and a non-negative integer q, asking "if we virtually enroll q more students to major i, what would the communication baseline H become". The system will return the new baseline H' after the virtual expansion. Note: This is purely a simulation and does not change the actual enrollment.

3. **Query Baseline Delta of Virtual Expansion**: Specify a major i (between 1 and 4) and a non-negative integer q, asking "how much would the communication baseline H increase if we virtually enroll q more students to major i". The system will return the increase delta Δ.

4. **Submit Analysis Report**: When you are confident in the enrollment numbers, submit your inferred four numbers c1, c2, c3, c4.

Please use as few queries as possible to complete the assessment.

Each query must contain only one tag. Use the following XML format:

- Query current communication baseline (empty content):
<query_h></query_h>

- Query baseline after virtual expansion (e.g., adding 3 students to major 2):
<query_add_value>type=2, q=3</query_add_value>

- Query baseline delta of virtual expansion (e.g., adding 1 student to major 1):
<query_add_delta>type=1, q=1</query_add_delta>

- Submit final analysis report (four numbers comma-separated, in order c1, c2, c3, c4):
<answer>c1=5, c2=3, c3=4, c4=2</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎使用工厂流水线“同型号零件批次兼容性测试评估系统”。

当前库存中存放着四种不同型号的关键零部件。每种型号零件的批次数量分别记为 c1, c2, c3, c4，均为未知的非负整数。

为了保障装配质量，品控部门定义了一个批次兼容性测试指标 H。它表示任意抽取两个同型号零件批次进行无序两两交叉对比测试的总组合数。具体而言，对每种型号 i，若有 ci 个批次，则需要进行 ci × (ci - 1) / 2 次交叉测试；H 是四种型号零件交叉测试次数的总和。

你的目标是通过向系统进行参数查询，推断出这四种型号的准确批次数量 c1, c2, c3, c4。

你可以进行以下四类操作（每次仅限一个操作）：

1. **查询当前测试指标**：询问当前的 H 值。系统会返回一个非负整数。

2. **查询虚拟入库后的测试指标**：指定一个零件型号 i（1到4之间）和一个非负整数 q，询问"如果临时向库房虚拟调拨 q 个批次的型号 i，测试指标 H 会变成多少"。系统会返回虚拟入库后的新指标 H'。注意：这只是品控推演，不改变实际库存批次数。

3. **查询虚拟入库的指标变化量**：指定一个零件型号 i（1到4之间）和一个非负整数 q，询问"临时虚拟调拨 q 个批次的型号 i 会使测试指标 H 增加多少"。系统会返回增加的差值 Δ。

4. **提交品控盘点报告**：当你确定各型号批次数量后，提交你推测的四个数 c1, c2, c3, c4。

请尽可能少地使用查询次数来完成盘点。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 查询当前测试指标（内容为空）：
<query_h></query_h>

- 查询虚拟入库后的测试指标（例如向型号 2 调拨 3 个批次）：
<query_add_value>type=2, q=3</query_add_value>

- 查询虚拟入库的指标变化量（例如向型号 1 调拨 1 个批次）：
<query_add_delta>type=1, q=1</query_add_delta>

- 提交最终品控盘点报告（四个数用逗号分隔，按 c1, c2, c3, c4 的顺序）：
<answer>c1=5, c2=3, c3=4, c4=2</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the Factory Assembly Line "Homogeneous Part Batch Compatibility Testing Evaluation System".

The current inventory holds critical components of four different models. The number of batches for each component model is denoted as c1, c2, c3, c4, which are unknown non-negative integers.

To ensure assembly quality, the quality control (QC) department defines a batch compatibility testing metric H. It represents the total number of unordered pairwise cross-comparison tests that can be conducted by randomly drawing two batches of the same component model. Specifically, for each model i with ci batches, ci × (ci - 1) / 2 cross-tests are required; H is the total sum of cross-tests across all four models.

Your objective is to deduce the exact batch quantities of these four models, c1, c2, c3, c4, by querying the system parameters.

You can perform the following four types of operations (one per turn):

1. **Query Current Testing Metric**: Ask for the current value of H. The system will return a non-negative integer.

2. **Query Metric After Virtual Restocking**: Specify a component model i (between 1 and 4) and a non-negative integer q, asking "if we virtually transfer q batches of model i to the warehouse, what would the testing metric H become". The system will return the new metric H' after the virtual restocking. Note: This is merely a QC projection and does not change the actual inventory.

3. **Query Metric Delta of Virtual Restocking**: Specify a component model i (between 1 and 4) and a non-negative integer q, asking "how much would the testing metric H increase if we virtually transfer q batches of model i". The system will return the increase delta Δ.

4. **Submit QC Inventory Report**: When you are confident in the batch quantities, submit your inferred four numbers c1, c2, c3, c4.

Please use as few queries as possible to complete the inventory check.

Each query must contain only one tag. Use the following XML format:

- Query current testing metric (empty content):
<query_h></query_h>

- Query metric after virtual restocking (e.g., transferring 3 batches of model 2):
<query_add_value>type=2, q=3</query_add_value>

- Query metric delta of virtual restocking (e.g., transferring 1 batch of model 1):
<query_add_delta>type=1, q=1</query_add_delta>

- Submit final QC inventory report (four numbers comma-separated, in order c1, c2, c3, c4):
<answer>c1=5, c2=3, c3=4, c4=2</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎进入法院档案室“同案由卷宗类案比对分析系统”。

档案室目前积压了四种不同案件类型的卷宗（如民事、刑事、行政、经济）。每种类型案件的卷宗数量分别记为 c1, c2, c3, c4，均为未知的非负整数。

为了评估文书审查的工作量，系统定义了一个类案比对基数 H。它表示在同类型卷宗之间进行无序两两交叉比对寻找类案参考的总操作次数。具体而言，对每种案件类型 i，若有 ci 本卷宗，则需进行 ci × (ci - 1) / 2 次交叉比对；H 是四种类型卷宗比对次数的总和。

你的目标是通过向系统进行参数查询，推断出这四类卷宗的准确数量 c1, c2, c3, c4。

你可以进行以下四类操作（每次仅限一个操作）：

1. **查询当前比推基数**：询问当前的 H 值。系统会返回一个非负整数。

2. **查询模拟归档后的比对基数**：指定一个卷宗类型 i（1到4之间）和一个非负整数 q，询问"如果临时向档案室模拟移交 q 本类型 i 的卷宗，比对基数 H 会变成多少"。系统会返回模拟移交后的新基数 H'。注意：这只是算力推演，不改变实际积压的卷宗数。

3. **查询模拟归档的基数变化量**：指定一个卷宗类型 i（1到4之间）和一个非负整数 q，询问"临时模拟移交 q 本类型 i 的卷宗会使比对基数 H 增加多少"。系统会返回增加的差值 Δ。

4. **提交审查排期报告**：当你确定各类型卷宗数量后，提交你推测的四个数 c1, c2, c3, c4。

请尽可能少地使用查询次数来完成评估。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 查询当前比对基数（内容为空）：
<query_h></query_h>

- 查询模拟归档后的比对基数（例如向类型 2 模拟移交 3 本）：
<query_add_value>type=2, q=3</query_add_value>

- 查询模拟归档的基数变化量（例如向类型 1 模拟移交 1 本）：
<query_add_delta>type=1, q=1</query_add_delta>

- 提交最终审查排期报告（四个数用逗号分隔，按 c1, c2, c3, c4 的顺序）：
<answer>c1=5, c2=3, c3=4, c4=2</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Court Archives "Homogeneous Case File Precedent Comparison System".

The archives currently have a backlog of case files from four different legal domains (e.g., Civil, Criminal, Administrative, Economic). The number of files for each domain is denoted as c1, c2, c3, c4, which are unknown non-negative integers.

To evaluate the workload of document review, the system defines a precedent comparison baseline H. It represents the total number of unordered pairwise cross-comparisons performed among files of the same domain to find precedent references. Specifically, for each domain i with ci files, ci × (ci - 1) / 2 cross-comparisons are required; H is the total sum of comparison operations across all four domains.

Your objective is to deduce the exact number of backlogged files in these four domains, c1, c2, c3, c4, by querying the system parameters.

You can perform the following four types of operations (one per turn):

1. **Query Current Comparison Baseline**: Ask for the current value of H. The system will return a non-negative integer.

2. **Query Baseline After Simulated Archiving**: Specify a case domain i (between 1 and 4) and a non-negative integer q, asking "if we simulate the transfer of q files of domain i into the archives, what would the comparison baseline H become". The system will return the new baseline H' after the simulation. Note: This is merely a computational projection and does not change the actual backlog.

3. **Query Baseline Delta of Simulated Archiving**: Specify a case domain i (between 1 and 4) and a non-negative integer q, asking "how much would the comparison baseline H increase if we simulate the transfer of q files of domain i". The system will return the increase delta Δ.

4. **Submit Review Schedule Report**: When you are confident in the file counts, submit your inferred four numbers c1, c2, c3, c4.

Please use as few queries as possible to complete the assessment.

Each query must contain only one tag. Use the following XML format:

- Query current comparison baseline (empty content):
<query_h></query_h>

- Query baseline after simulated archiving (e.g., simulating transfer of 3 files to domain 2):
<query_add_value>type=2, q=3</query_add_value>

- Query baseline delta of simulated archiving (e.g., simulating transfer of 1 file to domain 1):
<query_add_delta>type=1, q=1</query_add_delta>

- Submit final review schedule report (four numbers comma-separated, in order c1, c2, c3, c4):
<answer>c1=5, c2=3, c3=4, c4=2</answer>
"""

    tags = ["answer", "query_h", "query_add_value", "query_add_delta"]

    DIFFICULTY_CONFIG = {
        1: {
            "c1": 2,
            "c2": 3,
            "c3": 2,
            "c4": 1,
        },
        2: {
            "c1": 4,
            "c2": 5,
            "c3": 3,
            "c4": 4,
        },
        3: {
            "c1": 6,
            "c2": 7,
            "c3": 5,
            "c4": 8,
        },
        4: {
            "c1": 0,
            "c2": 10,
            "c3": 8,
            "c4": 12,
        },
        5: {
            "c1": 15,
            "c2": 0,
            "c3": 0,
            "c4": 20,
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)
        
        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")
        
        cfg = self.DIFFICULTY_CONFIG[diff]
        
        self.c1 = cfg["c1"]
        self.c2 = cfg["c2"]
        self.c3 = cfg["c3"]
        self.c4 = cfg["c4"]
        
        self.counts = [0, self.c1, self.c2, self.c3, self.c4]
        
        self.H = self._calculate_h(self.counts)
        
        self._game_info = {}

    def _calculate_h(self, counts):
        h = 0
        for i in range(1, 5):
            ci = counts[i]
            h += ci * (ci - 1) // 2
        return h

    def _parse_type_q(self, content):
        try:
            parts = [x.strip() for x in content.split(",")]
            type_val = None
            q_val = None
            
            for part in parts:
                if "=" in part:
                    key, val = part.split("=", 1)
                    key = key.strip()
                    val = val.strip()
                    if key == "type":
                        type_val = int(val)
                    elif key == "q":
                        q_val = int(val)
            
            if type_val is None or q_val is None:
                raise ValueError("Missing type or q")
            
            if type_val < 1 or type_val > 4:
                raise ValueError("Type must be between 1 and 4")
            
            if q_val < 0:
                raise ValueError("q must be non-negative")
            
            return type_val, q_val
        
        except Exception as e:
            raise ValueError(f"Invalid format for type and q: {str(e)}")

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        try:
            parts = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            
            for part in parts:
                if "=" in part:
                    key, val = part.split("=", 1)
                    key = key.strip()
                    val = val.strip()
                    ans_dict[key] = int(val)
            
            if not all(key in ans_dict for key in ["c1", "c2", "c3", "c4"]):
                return False
            
            return (ans_dict["c1"] == self.c1 and
                    ans_dict["c2"] == self.c2 and
                    ans_dict["c3"] == self.c3 and
                    ans_dict["c4"] == self.c4)
        
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        
        if "query_h" in parsed_info:
            return str(self.H)
        
        elif "query_add_value" in parsed_info:
            try:
                type_idx, q = self._parse_type_q(parsed_info["query_add_value"])
                
                temp_counts = self.counts.copy()
                temp_counts[type_idx] += q
                
                h_prime = self._calculate_h(temp_counts)
                
                return str(h_prime)
            
            except ValueError as e:
                if self.config.language == "zh":
                    return f"错误：{str(e)}"
                else:
                    return f"Error: {str(e)}"
        
        elif "query_add_delta" in parsed_info:
            try:
                type_idx, q = self._parse_type_q(parsed_info["query_add_delta"])
                
                ci = self.counts[type_idx]
                delta = q * ci + q * (q - 1) // 2
                
                return str(delta)
            
            except ValueError as e:
                if self.config.language == "zh":
                    return f"错误：{str(e)}"
                else:
                    return f"Error: {str(e)}"
        
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        queries.append({
            "query": "<query_h></query_h>",
            "answer": str(self.H)
        })
        
        q_range = range(1, 6)
        
        for type_idx in range(1, 5):
            for q in q_range:
                content = f"type={type_idx}, q={q}"
                
                temp_counts = self.counts.copy()
                temp_counts[type_idx] += q
                h_prime = self._calculate_h(temp_counts)
                
                queries.append({
                    "query": f"<query_add_value>{content}</query_add_value>",
                    "answer": str(h_prime)
                })
                
                ci = self.counts[type_idx]
                delta = q * ci + q * (q - 1) // 2
                
                queries.append({
                    "query": f"<query_add_delta>{content}</query_add_delta>",
                    "answer": str(delta)
                })
                
        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        try:
            val = int(correct)
            if val == 0:
                return str(val + 3)
            elif val > 0:
                return str(val + max(3, val // 2))
            else:
                return str(val - max(3, abs(val) // 2))
        except ValueError:
            pass
        
        if "是" in correct:
            return correct.replace("是", "否")
        if "Yes" in correct:
            return correct.replace("Yes", "No")
        if "YES" in correct:
            return correct.replace("YES", "NO")
        if "yes" in correct:
            return correct.replace("yes", "no")
            
        return correct + "_WRONG"