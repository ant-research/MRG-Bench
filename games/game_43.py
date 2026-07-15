from .base import Game
import re
import itertools

class BooleanFunctionInferenceGame(Game):

    game_rule_zh = """\
我们现在来玩一个"布尔函数推断"游戏，规则如下：

游戏设定了一个全集 U，包含 16 个元素，每个元素由四个二值属性 x1, x2, x3, x4 组成（每个属性取值为 0 或 1）。例如元素 [0,1,0,1] 表示 x1=0, x2=1, x3=0, x4=1。

存在一个固定但未知的布尔函数 g，它将 U 中的每个元素映射为 0 或 1。函数 g 定义了一个子集 S，包含所有使得 g(x)=1 的元素 x。

游戏开始时，我会给你一个目标元素 e*，它的四个属性值已明确给出：
目标元素 e* = {target}

你的任务是通过查询来推断 g(e*) 的值（即目标元素是否属于集合 S）。

你可以反复向我提出以下两类查询（每次仅限一个查询）：

1. **单点成员查询**：询问某个元素 x（x 不能是 e*）是否属于 S。我会回答"是"或"否"。
2. **批量计数查询**：询问一个元素集合 Q（1到8个元素，不含 e*，元素不重复）中有多少个属于 S。我会回答一个非负整数。

- 任何查询都不得包含目标元素 e*
- 在提交最终答案前，至少需进行 6 次有效查询
- 你的查询记录中必须确证既存在属于 S 的样本，也存在不属于 S 的样本

每次只能包含一个查询标签。请使用以下 XML 格式：

- 单点成员查询（例如询问元素 [0,1,0,1]）：
<query_member>0,1,0,1</query_member>

- 批量计数查询（例如询问三个元素）：
<query_count>0,0,0,0;1,1,1,1;0,1,0,1</query_count>

注意：批量查询中多个元素用分号分隔，每个元素的四个属性用逗号分隔。

当你收集足够信息后，请提交最终答案。格式如下：

<answer>prediction=1, explanation=你对函数g的归纳性假设描述</answer>

或

<answer>prediction=0, explanation=你对函数g的归纳性假设描述</answer>

其中 prediction 为 0 或 1，explanation 需简要说明你推断出的函数 g 的规律或特征。
"""

    game_rule_en = """\
Let's play a "Boolean Function Inference" game. Here are the rules:

The game defines a universe U containing 16 elements, each consisting of four binary attributes x1, x2, x3, x4 (each taking value 0 or 1). For example, element [0,1,0,1] means x1=0, x2=1, x3=0, x4=1.

There exists a fixed but unknown boolean function g that maps each element in U to either 0 or 1. Function g defines a subset S containing all elements x where g(x)=1.

At the start, I will give you a target element e* with its four attribute values explicitly provided:
Target element e* = {target}

Your task is to infer the value of g(e*) (whether the target element belongs to set S) through queries.

You can repeatedly ask me the following two types of queries (one query per turn):

1. **Single Member Query**: Ask whether an element x (x cannot be e*) belongs to S. I will answer "Yes" or "No".
2. **Batch Count Query**: Ask how many elements in a set Q (1 to 8 elements, excluding e*, no duplicates) belong to S. I will answer a non-negative integer.

- No query may include the target element e*
- At least 6 valid queries must be made before submitting the final answer
- Your query history must demonstrate evidence of both elements that belong to S and elements that do not

Each turn must contain only one query tag. Use the following XML format:

- Single Member Query (e.g., querying element [0,1,0,1]):
<query_member>0,1,0,1</query_member>

- Batch Count Query (e.g., querying three elements):
<query_count>0,0,0,0;1,1,1,1;0,1,0,1</query_count>

Note: In batch queries, multiple elements are separated by semicolons, and the four attributes of each element are separated by commas.

When you have gathered sufficient information, submit your final answer in this format:

<answer>prediction=1, explanation=your inductive hypothesis about function g</answer>

or

<answer>prediction=0, explanation=your inductive hypothesis about function g</answer>

Where prediction is 0 or 1, and explanation should briefly describe the pattern or characteristics you inferred about function g.
"""

    contextualized_rule_zh_1 = """\
我们现在来玩一个“交通拥堵干预推断”系统评估游戏，规则如下：

系统设定了一个路口状态全集 U，包含 16 种不同的交通情况，每种情况由四个二值属性 x1, x2, x3, x4 组成（每个属性取值为 0 或 1，分别代表：早晚高峰、主干道拥堵、恶劣天气、发生事故）。例如状态 [0,1,0,1] 表示非高峰期、主干道拥堵、天气良好且发生事故。

交通控制中心存在一个固定但未知的自动化调度规则 g，它将 U 中的每种状态映射为 0 或 1。规则 g 定义了一个必须开启“紧急疏导模式”的状态子集 S，包含所有使得 g(x)=1 的交通状态 x。

评估开始时，我会给你一个当前目标路口的状态 e*，它的四个属性值已明确给出：
目标路口状态 e* = {target}

你的任务是通过系统查询来推断 g(e*) 的值（即当前目标路口是否需要开启紧急疏导模式，属于集合 S）。

你可以反复向我提出以下两类系统查询（每次仅限一个查询）：

1. **单点状态查询**：询问某种特定交通状态 x（x 不能是 e*）是否会触发紧急疏导（即是否属于 S）。我会回答"是"或"否"。
2. **批量状态计数查询**：询问一个状态集合 Q（1到8种状态，不含 e*，状态不重复）中有多少种情况会触发紧急疏导。我会回答一个非负整数。

- 任何查询都不得包含目标状态 e*
- 在提交最终评估报告前，至少需进行 6 次有效查询
- 你的查询记录中必须确证既存在触发紧急疏导的样本，也存在不触发的样本

每次只能包含一个查询标签。请使用以下 XML 格式：

- 单点状态查询（例如询问状态 [0,1,0,1]）：
<query_member>0,1,0,1</query_member>

- 批量状态计数查询（例如询问三种状态）：
<query_count>0,0,0,0;1,1,1,1;0,1,0,1</query_count>

注意：批量查询中多个状态用分号分隔，每个状态的四个属性用逗号分隔。

当你收集足够信息后，请提交最终评估决定。格式如下：

<answer>prediction=1, explanation=你对调度规则g的归纳性假设描述</answer>

或

<answer>prediction=0, explanation=你对调度规则g的归纳性假设描述</answer>

其中 prediction 为 0 或 1，explanation 需简要说明你推断出的触发紧急疏导的交通规则或特征。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play a "Traffic Congestion Intervention Inference" system evaluation game. Here are the rules:

The system defines a complete set of intersection states U containing 16 elements, each consisting of four binary attributes x1, x2, x3, x4 (each taking value 0 or 1, representing: rush hour, main road congestion, severe weather, and traffic accident, respectively). For example, state [0,1,0,1] means non-rush hour, main road congestion, clear weather, and an accident occurred.

The traffic control center has a fixed but unknown automated scheduling rule g that maps each state in U to either 0 or 1. Rule g defines a subset S containing all states x that trigger the "Emergency Evacuation Mode" (i.e., where g(x)=1).

At the start, I will give you a target intersection state e* with its four attribute values explicitly provided:
Target intersection state e* = {target}

Your task is to infer the value of g(e*) (whether the target state requires emergency evacuation and belongs to set S) through system queries.

You can repeatedly ask me the following two types of queries (one query per turn):

1. **Single State Query**: Ask whether a specific traffic state x (x cannot be e*) triggers emergency evacuation (belongs to S). I will answer "Yes" or "No".
2. **Batch State Count Query**: Ask how many states in a set Q (1 to 8 states, excluding e*, no duplicates) trigger emergency evacuation. I will answer a non-negative integer.

- No query may include the target state e*
- At least 6 valid queries must be made before submitting the final evaluation report
- Your query history must demonstrate evidence of both states that trigger the mode and states that do not

Each turn must contain only one query tag. Use the following XML format:

- Single State Query (e.g., querying state [0,1,0,1]):
<query_member>0,1,0,1</query_member>

- Batch State Count Query (e.g., querying three states):
<query_count>0,0,0,0;1,1,1,1;0,1,0,1</query_count>

Note: In batch queries, multiple states are separated by semicolons, and the four attributes of each state are separated by commas.

When you have gathered sufficient information, submit your final evaluation decision in this format:

<answer>prediction=1, explanation=your inductive hypothesis about scheduling rule g</answer>

or

<answer>prediction=0, explanation=your inductive hypothesis about scheduling rule g</answer>

Where prediction is 0 or 1, and explanation should briefly describe the pattern or characteristics you inferred about the emergency evacuation triggering rule.
"""

    contextualized_rule_zh_2 = """\
我们现在来玩一个“临床诊断标准推断”游戏，规则如下：

医学知识库设定了一个患者症状图谱全集 U，包含 16 种不同的症状体征组合，每种组合由四个二值属性 x1, x2, x3, x4 组成（每个属性取值为 0 或 1，分别代表：发烧、剧烈咳嗽、呼吸困难、异常乏力）。例如体征组合 [0,1,0,1] 表示无发烧、有剧烈咳嗽、无呼吸困难且异常乏力。

医疗系统中存在一个固定但未知的临床诊断标准 g，它将 U 中的每种体征组合映射为 0 或 1。标准 g 定义了一个确诊特定罕见呼吸道综合征的患者子集 S，包含所有使得 g(x)=1 的体征组合 x。

会诊开始时，我会给你一个目标患者的体征组合 e*，它的四个属性值已明确给出：
目标患者体征组合 e* = {target}

你的任务是通过调阅历史病历来推断 g(e*) 的值（即该目标患者是否满足确诊标准，属于确诊集合 S）。

你可以反复向我提出以下两类病历查询（每次仅限一个查询）：

1. **单点病例查询**：询问某种特定的体征组合 x（x 不能是 e*）是否会被确诊（即是否属于 S）。我会回答"是"或"否"。
2. **批量病例计数查询**：询问一个体征组合集合 Q（1到8种组合，不含 e*，组合不重复）中有多少种情况会被确诊。我会回答一个非负整数。

- 任何查询都不得包含目标患者体征组合 e*
- 在提交最终诊断结论前，至少需进行 6 次有效查询
- 你的查询记录中必须确证既存在被确诊的体征组合，也存在未被确诊的体征组合

每次只能包含一个查询标签。请使用以下 XML 格式：

- 单点病例查询（例如询问体征组合 [0,1,0,1]）：
<query_member>0,1,0,1</query_member>

- 批量病例计数查询（例如询问三种体征组合）：
<query_count>0,0,0,0;1,1,1,1;0,1,0,1</query_count>

注意：批量查询中多个体征组合用分号分隔，每个组合的四个属性用逗号分隔。

当你收集足够信息后，请提交最终诊断结论。格式如下：

<answer>prediction=1, explanation=你对临床诊断标准g的归纳性假设描述</answer>

或

<answer>prediction=0, explanation=你对临床诊断标准g的归纳性假设描述</answer>

其中 prediction 为 0 或 1，explanation 需简要说明你推断出的该疾病的确诊规律或核心临床特征。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Clinical Diagnostic Criteria Inference" game. Here are the rules:

The medical knowledge base defines a complete universe of patient symptom profiles U containing 16 different combinations, each consisting of four binary attributes x1, x2, x3, x4 (each taking value 0 or 1, representing: fever, severe cough, shortness of breath, and abnormal fatigue, respectively). For example, profile [0,1,0,1] means no fever, severe cough present, no shortness of breath, and abnormal fatigue present.

There exists a fixed but unknown clinical diagnostic criterion g in the medical system that maps each symptom profile in U to either 0 or 1. Criterion g defines a subset S of confirmed patients for a specific respiratory syndrome, containing all profiles x where g(x)=1.

At the start of the consultation, I will give you a target patient's symptom profile e* with its four attribute values explicitly provided:
Target patient profile e* = {target}

Your task is to infer the value of g(e*) (whether the target patient meets the diagnostic criteria and belongs to the confirmed set S) by reviewing historical medical records.

You can repeatedly ask me the following two types of medical record queries (one query per turn):

1. **Single Case Query**: Ask whether a specific symptom profile x (x cannot be e*) is diagnosed as positive (belongs to S). I will answer "Yes" or "No".
2. **Batch Case Count Query**: Ask how many profiles in a set Q (1 to 8 profiles, excluding e*, no duplicates) are diagnosed as positive. I will answer a non-negative integer.

- No query may include the target patient profile e*
- At least 6 valid queries must be made before submitting the final diagnostic conclusion
- Your query history must demonstrate evidence of both positive and negative diagnosed profiles

Each turn must contain only one query tag. Use the following XML format:

- Single Case Query (e.g., querying profile [0,1,0,1]):
<query_member>0,1,0,1</query_member>

- Batch Case Count Query (e.g., querying three profiles):
<query_count>0,0,0,0;1,1,1,1;0,1,0,1</query_count>

Note: In batch queries, multiple profiles are separated by semicolons, and the four attributes of each profile are separated by commas.

When you have gathered sufficient information, submit your final diagnostic conclusion in this format:

<answer>prediction=1, explanation=your inductive hypothesis about the diagnostic criterion g</answer>

or

<answer>prediction=0, explanation=your inductive hypothesis about the diagnostic criterion g</answer>

Where prediction is 0 or 1, and explanation should briefly describe the diagnostic pattern or core clinical characteristics you inferred.
"""

    contextualized_rule_zh_3 = """\
我们现在来玩一个“奖学金评定规则推断”游戏，规则如下：

教务系统设定了一个学生表现画像全集 U，包含 16 种不同的表现组合，每种组合由四个二值属性 x1, x2, x3, x4 组成（每个属性取值为 0 或 1，分别代表：核心课程优秀、参与竞赛获奖、担任学生干部、志愿服务达标）。例如画像 [0,1,0,1] 表示核心课程未获优秀、有竞赛获奖、未担任干部且志愿服务达标。

评优委员会存在一个固定但未公开的奖学金评定规则 g，它将 U 中的每种学生画像映射为 0 或 1。规则 g 定义了一个获得“卓越之星”奖学金的画像子集 S，包含所有使得 g(x)=1 的画像 x。

评选开始时，我会给你一个目标候选学生的画像 e*，它的四个属性值已明确给出：
目标学生画像 e* = {target}

你的任务是通过查询历史评审结果来推断 g(e*) 的值（即该目标学生是否符合“卓越之星”的评定标准，属于集合 S）。

你可以反复向我提出以下两类评审查询（每次仅限一个查询）：

1. **单点画像查询**：询问某种特定的学生画像 x（x 不能是 e*）是否能获得奖学金（即是否属于 S）。我会回答"是"或"否"。
2. **批量画像计数查询**：询问一个画像集合 Q（1到8种画像，不含 e*，画像不重复）中有多少种情况能获得奖学金。我会回答一个非负整数。

- 任何查询都不得包含目标学生画像 e*
- 在提交最终评定意见前，至少需进行 6 次有效查询
- 你的查询记录中必须确证既存在获奖的画像样本，也存在未获奖的画像样本

每次只能包含一个查询标签。请使用以下 XML 格式：

- 单点画像查询（例如询问画像 [0,1,0,1]）：
<query_member>0,1,0,1</query_member>

- 批量画像计数查询（例如询问三种画像）：
<query_count>0,0,0,0;1,1,1,1;0,1,0,1</query_count>

注意：批量查询中多个画像用分号分隔，每个画像的四个属性用逗号分隔。

当你收集足够信息后，请提交最终评定意见。格式如下：

<answer>prediction=1, explanation=你对奖学金评定规则g的归纳性假设描述</answer>

或

<answer>prediction=0, explanation=你对奖学金评定规则g的归纳性假设描述</answer>

其中 prediction 为 0 或 1，explanation 需简要说明你推断出的奖学金发放规律或侧重考察的教育指标。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Scholarship Evaluation Criteria Inference" game. Here are the rules:

The academic system defines a complete universe of student performance profiles U containing 16 different combinations, each consisting of four binary attributes x1, x2, x3, x4 (each taking value 0 or 1, representing: core course excellence, competition award winner, student leader role, and volunteer service fulfilled, respectively). For example, profile [0,1,0,1] means no core course excellence, won a competition, no leadership role, and fulfilled volunteer service.

The evaluation committee uses a fixed but unpublished scholarship awarding rule g that maps each student profile in U to either 0 or 1. Rule g defines a subset S of profiles that receive the "Star of Excellence" scholarship, containing all profiles x where g(x)=1.

At the start of the evaluation, I will give you a target candidate student's profile e* with its four attribute values explicitly provided:
Target student profile e* = {target}

Your task is to infer the value of g(e*) (whether the target student meets the scholarship criteria and belongs to set S) by querying historical review results.

You can repeatedly ask me the following two types of review queries (one query per turn):

1. **Single Profile Query**: Ask whether a specific student profile x (x cannot be e*) is awarded the scholarship (belongs to S). I will answer "Yes" or "No".
2. **Batch Profile Count Query**: Ask how many profiles in a set Q (1 to 8 profiles, excluding e*, no duplicates) are awarded the scholarship. I will answer a non-negative integer.

- No query may include the target student profile e*
- At least 6 valid queries must be made before submitting the final evaluation recommendation
- Your query history must demonstrate evidence of both awarded profiles and unawarded profiles

Each turn must contain only one query tag. Use the following XML format:

- Single Profile Query (e.g., querying profile [0,1,0,1]):
<query_member>0,1,0,1</query_member>

- Batch Profile Count Query (e.g., querying three profiles):
<query_count>0,0,0,0;1,1,1,1;0,1,0,1</query_count>

Note: In batch queries, multiple profiles are separated by semicolons, and the four attributes of each profile are separated by commas.

When you have gathered sufficient information, submit your final evaluation recommendation in this format:

<answer>prediction=1, explanation=your inductive hypothesis about the scholarship evaluation rule g</answer>

or

<answer>prediction=0, explanation=your inductive hypothesis about the scholarship evaluation rule g</answer>

Where prediction is 0 or 1, and explanation should briefly describe the awarding pattern or core educational metrics you inferred.
"""

    contextualized_rule_zh_4 = """\
我们现在来玩一个“生产线缺陷根因推断”游戏，规则如下：

工厂质检系统设定了一个工艺参数配置全集 U，包含 16 种不同的配置组合，每种组合由四个二值属性 x1, x2, x3, x4 组成（每个属性取值为 0 或 1，分别代表：熔炉温度偏高、舱室压力异常、传输带降速、使用备用原料批次）。例如配置 [0,1,0,1] 表示温度正常、压力异常、带速正常且使用了备用原料。

生产线上存在一个固定但未知的物理缺陷触发机制 g，它将 U 中的每种参数配置映射为 0 或 1。机制 g 定义了一个导致产品被判定为“次品”的配置子集 S，包含所有使得 g(x)=1 的参数组合 x。

排查开始时，我会给你一个当前目标批次的工艺配置 e*，它的四个属性值已明确给出：
目标工艺配置 e* = {target}

你的任务是通过质检测试记录来推断 g(e*) 的值（即该目标配置是否会生产出次品，属于缺陷集合 S）。

你可以反复向我提出以下两类质检查询（每次仅限一个查询）：

1. **单点配置查询**：询问某种特定的工艺配置 x（x 不能是 e*）是否会导致次品（即是否属于 S）。我会回答"是"或"否"。
2. **批量配置计数查询**：询问一个配置集合 Q（1到8种配置，不含 e*，配置不重复）中有多少种情况会导致次品。我会回答一个非负整数。

- 任何查询都不得包含目标工艺配置 e*
- 在提交最终排查报告前，至少需进行 6 次有效查询
- 你的查询记录中必须确证既存在导致次品的配置，也存在生产良品的配置

每次只能包含一个查询标签。请使用以下 XML 格式：

- 单点配置查询（例如询问配置 [0,1,0,1]）：
<query_member>0,1,0,1</query_member>

- 批量配置计数查询（例如询问三种配置）：
<query_count>0,0,0,0;1,1,1,1;0,1,0,1</query_count>

注意：批量查询中多个配置用分号分隔，每个配置的四个属性用逗号分隔。

当你收集足够信息后，请提交最终排查报告。格式如下：

<answer>prediction=1, explanation=你对缺陷触发机制g的归纳性假设描述</answer>

或

<answer>prediction=0, explanation=你对缺陷触发机制g的归纳性假设描述</answer>

其中 prediction 为 0 或 1，explanation 需简要说明你推断出的导致产品缺陷的核心工艺参数规律。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's play a "Production Line Defect Root Cause Inference" game. Here are the rules:

The factory quality control system defines a complete universe of process parameter configurations U containing 16 different combinations, each consisting of four binary attributes x1, x2, x3, x4 (each taking value 0 or 1, representing: elevated furnace temperature, abnormal chamber pressure, conveyor belt slowdown, and use of backup raw material batch, respectively). For example, configuration [0,1,0,1] means normal temperature, abnormal pressure, normal belt speed, and backup material used.

There exists a fixed but unknown physical defect triggering mechanism g on the production line that maps each parameter configuration in U to either 0 or 1. Mechanism g defines a subset S of configurations that result in the product being classified as "defective", containing all configurations x where g(x)=1.

At the start of the troubleshooting, I will give you a target batch's process configuration e* with its four attribute values explicitly provided:
Target process configuration e* = {target}

Your task is to infer the value of g(e*) (whether the target configuration will produce a defective product and belongs to the defect set S) by querying QC test records.

You can repeatedly ask me the following two types of QC queries (one query per turn):

1. **Single Configuration Query**: Ask whether a specific process configuration x (x cannot be e*) causes a defect (belongs to S). I will answer "Yes" or "No".
2. **Batch Configuration Count Query**: Ask how many configurations in a set Q (1 to 8 configurations, excluding e*, no duplicates) cause defects. I will answer a non-negative integer.

- No query may include the target process configuration e*
- At least 6 valid queries must be made before submitting the final troubleshooting report
- Your query history must demonstrate evidence of both defective configurations and defect-free configurations

Each turn must contain only one query tag. Use the following XML format:

- Single Configuration Query (e.g., querying configuration [0,1,0,1]):
<query_member>0,1,0,1</query_member>

- Batch Configuration Count Query (e.g., querying three configurations):
<query_count>0,0,0,0;1,1,1,1;0,1,0,1</query_count>

Note: In batch queries, multiple configurations are separated by semicolons, and the four attributes of each configuration are separated by commas.

When you have gathered sufficient information, submit your final troubleshooting report in this format:

<answer>prediction=1, explanation=your inductive hypothesis about the defect triggering mechanism g</answer>

or

<answer>prediction=0, explanation=your inductive hypothesis about the defect triggering mechanism g</answer>

Where prediction is 0 or 1, and explanation should briefly describe the core process parameter pattern you inferred that leads to product defects.
"""

    contextualized_rule_zh_5 = """\
我们现在来玩一个“合规审查与违规裁定推断”游戏，规则如下：

监管法规库设定了一个企业商业行为特征全集 U，包含 16 种不同的行为画像，每种画像由四个二值属性 x1, x2, x3, x4 组成（每个属性取值为 0 或 1，分别代表：涉及跨境资金流动、缺乏独立审计、数据未匿名化处理、隐瞒实际控制人）。例如行为画像 [0,1,0,1] 表示无跨境资金、无独立审计、数据已匿名化且隐瞒了实际控制人。

监管机构执行着一套固定但未完全公开的执法裁量标准 g，它将 U 中的每种行为画像映射为 0 或 1。标准 g 定义了一个被判定为“高风险违规”的行为子集 S，包含所有使得 g(x)=1 的行为画像 x。

合规审查开始时，我会给你一个目标企业的当前行为画像 e*，它的四个属性值已明确给出：
目标企业行为画像 e* = {target}

你的任务是通过检索过往处罚案例来推断 g(e*) 的值（即该目标企业的行为是否构成高风险违规，属于违规集合 S）。

你可以反复向我提出以下两类法务检索查询（每次仅限一个查询）：

1. **单点案例查询**：询问某种特定的行为画像 x（x 不能是 e*）是否会被判定违规（即是否属于 S）。我会回答"是"或"否"。
2. **批量案例计数查询**：询问一个行为画像集合 Q（1到8种画像，不含 e*，画像不重复）中有多少种情况会被判定违规。我会回答一个非负整数。

- 任何查询都不得包含目标企业行为画像 e*
- 在提交最终合规意见书前，至少需进行 6 次有效查询
- 你的查询记录中必须确证既存在被罚的违规画像，也存在合规免罚的画像

每次只能包含一个查询标签。请使用以下 XML 格式：

- 单点案例查询（例如询问行为画像 [0,1,0,1]）：
<query_member>0,1,0,1</query_member>

- 批量案例计数查询（例如询问三种行为画像）：
<query_count>0,0,0,0;1,1,1,1;0,1,0,1</query_count>

注意：批量查询中多个画像用分号分隔，每个画像的四个属性用逗号分隔。

当你收集足够信息后，请提交最终合规意见书。格式如下：

<answer>prediction=1, explanation=你对执法裁量标准g的归纳性假设描述</answer>

或

<answer>prediction=0, explanation=你对执法裁量标准g的归纳性假设描述</answer>

其中 prediction 为 0 或 1，explanation 需简要说明你推断出的违规判定规律或核心法律特征。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "Compliance Review and Violation Adjudication Inference" game. Here are the rules:

The regulatory framework defines a complete universe of corporate business behavior profiles U containing 16 different combinations, each consisting of four binary attributes x1, x2, x3, x4 (each taking value 0 or 1, representing: involves cross-border capital flows, lacks independent auditing, data not anonymized, and conceals actual controllers, respectively). For example, profile [0,1,0,1] means no cross-border funds, no independent audit, data anonymized, and actual controllers concealed.

The regulatory authority enforces a fixed but not fully public enforcement discretion standard g that maps each behavior profile in U to either 0 or 1. Standard g defines a subset S of behaviors deemed "High-Risk Violations", containing all profiles x where g(x)=1.

At the start of the compliance review, I will give you a target company's current behavior profile e* with its four attribute values explicitly provided:
Target corporate behavior profile e* = {target}

Your task is to infer the value of g(e*) (whether the target company's behavior constitutes a high-risk violation and belongs to the violation set S) by retrieving past penalty cases.

You can repeatedly ask me the following two types of legal retrieval queries (one query per turn):

1. **Single Case Query**: Ask whether a specific behavior profile x (x cannot be e*) is judged as a violation (belongs to S). I will answer "Yes" or "No".
2. **Batch Case Count Query**: Ask how many profiles in a set Q (1 to 8 profiles, excluding e*, no duplicates) are judged as violations. I will answer a non-negative integer.

- No query may include the target behavior profile e*
- At least 6 valid queries must be made before submitting the final compliance opinion
- Your query history must demonstrate evidence of both penalized violation profiles and compliant profiles

Each turn must contain only one query tag. Use the following XML format:

- Single Case Query (e.g., querying profile [0,1,0,1]):
<query_member>0,1,0,1</query_member>

- Batch Case Count Query (e.g., querying three profiles):
<query_count>0,0,0,0;1,1,1,1;0,1,0,1</query_count>

Note: In batch queries, multiple profiles are separated by semicolons, and the four attributes of each profile are separated by commas.

When you have gathered sufficient information, submit your final compliance opinion in this format:

<answer>prediction=1, explanation=your inductive hypothesis about the enforcement discretion standard g</answer>

or

<answer>prediction=0, explanation=your inductive hypothesis about the enforcement discretion standard g</answer>

Where prediction is 0 or 1, and explanation should briefly describe the violation judgment pattern or core legal characteristics you inferred.
"""

    tags = ["answer", "query_member", "query_count"]

    reasoning_type = "归纳推理"
    data_structure = "集合"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "target": "[1,0,1,0]",
                "target_vector": [1, 0, 1, 0],
                "function_type": "first_attr",
                "true_value": 1,
            },
            2: {
                "target": "[1,1,0,1]",
                "target_vector": [1, 1, 0, 1],
                "function_type": "and_first_two",
                "true_value": 1,
            },
            3: {
                "target": "[0,1,0,1]",
                "target_vector": [0, 1, 0, 1],
                "function_type": "at_least_two",
                "true_value": 1,
            },
            4: {
                "target": "[1,0,0,1]",
                "target_vector": [1, 0, 0, 1],
                "function_type": "odd_sum",
                "true_value": 0,
            },
            5: {
                "target": "[1,1,1,0]",
                "target_vector": [1, 1, 1, 0],
                "function_type": "xor_and_or",
                "true_value": 0,
            },
        },
        "en": {
            1: {
                "target": "[1,0,1,0]",
                "target_vector": [1, 0, 1, 0],
                "function_type": "first_attr",
                "true_value": 1,
            },
            2: {
                "target": "[1,1,0,1]",
                "target_vector": [1, 1, 0, 1],
                "function_type": "and_first_two",
                "true_value": 1,
            },
            3: {
                "target": "[0,1,0,1]",
                "target_vector": [0, 1, 0, 1],
                "function_type": "at_least_two",
                "true_value": 1,
            },
            4: {
                "target": "[1,0,0,1]",
                "target_vector": [1, 0, 0, 1],
                "function_type": "odd_sum",
                "true_value": 0,
            },
            5: {
                "target": "[1,1,1,0]",
                "target_vector": [1, 1, 1, 0],
                "function_type": "xor_and_or",
                "true_value": 0,
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0
        self.has_positive = False
        self.has_negative = False
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["target"] = cfg["target"]
        self.target_vector = cfg["target_vector"]
        self.function_type = cfg["function_type"]
        self.true_value = cfg["true_value"]

    def _evaluate_function(self, vector):
        x1, x2, x3, x4 = vector

        if self.function_type == "first_attr":
            return x1

        elif self.function_type == "and_first_two":
            return 1 if (x1 == 1 and x2 == 1) else 0

        elif self.function_type == "at_least_two":
            return 1 if sum(vector) >= 2 else 0

        elif self.function_type == "odd_sum":
            return 1 if sum(vector) % 2 == 1 else 0

        elif self.function_type == "xor_and_or":
            xor_part = 1 if x1 != x2 else 0
            or_part = 1 if (x3 == 1 or x4 == 1) else 0
            return 1 if (xor_part == 1 and or_part == 1) else 0

        else:
            raise ValueError(f"Unknown function type: {self.function_type}")

    def _parse_vector(self, vec_str):
        try:
            parts = [int(x.strip()) for x in vec_str.split(",")]
            if len(parts) != 4:
                raise ValueError
            if not all(x in [0, 1] for x in parts):
                raise ValueError
            return parts
        except:
            raise ValueError("Invalid vector format")

    def evaluate(self, parsed_info):
        if self.query_count < 6:
            return False
        if not (self.has_positive and self.has_negative):
            return False

        raw_ans = parsed_info["answer"]
        
        prediction_match = re.search(r'prediction\s*=\s*([01])', raw_ans, re.IGNORECASE)
        explanation_match = re.search(r'explanation\s*=\s*(.+)', raw_ans, re.IGNORECASE)
        
        if not prediction_match:
            return False
        
        prediction = int(prediction_match.group(1))
        
        if not explanation_match:
            return False

        return prediction == self.true_value

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        universe = []
        for x1 in range(2):
            for x2 in range(2):
                for x3 in range(2):
                    for x4 in range(2):
                        universe.append([x1, x2, x3, x4])
        
        available_elements = [x for x in universe if x != self.target_vector]
        
        def vec_to_str(v):
            return ",".join(str(x) for x in v)

        if self.config.language == "zh":
            yes_resp, no_resp = "是", "否"
        else:
            yes_resp, no_resp = "Yes", "No"

        for vec in available_elements:
            vec_str = vec_to_str(vec)
            
            res = self._evaluate_function(vec)
            ans = yes_resp if res == 1 else no_resp
            
            queries.append({
                "query": f"<query_member>{vec_str}</query_member>",
                "answer": ans
            })

        
        for r in range(1, 3):
            for batch in itertools.combinations(available_elements, r):
                batch_str = ";".join(vec_to_str(v) for v in batch)
                
                count = sum(self._evaluate_function(v) for v in batch)
                
                queries.append({
                    "query": f"<query_count>{batch_str}</query_count>",
                    "answer": str(count)
                })
                
        return queries

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_target = "错误：查询不能包含目标元素。"
            error_format = "错误：格式无效。"
            error_range = "错误：属性值必须为0或1。"
            error_batch_size = "错误：批量查询元素数量必须在1到8之间。"
            error_duplicate = "错误：批量查询中存在重复元素。"
        else:
            yes_res, no_res = "Yes", "No"
            error_target = "Error: Query cannot include the target element."
            error_format = "Error: Invalid format."
            error_range = "Error: Attribute values must be 0 or 1."
            error_batch_size = "Error: Batch query must contain 1 to 8 elements."
            error_duplicate = "Error: Duplicate elements in batch query."

        if "query_member" in parsed_info:
            try:
                vector = self._parse_vector(parsed_info["query_member"])
                
                if vector == self.target_vector:
                    return error_target
                
                result = self._evaluate_function(vector)
                self.query_count += 1
                
                if result == 1:
                    self.has_positive = True
                else:
                    self.has_negative = True
                
                return yes_res if result == 1 else no_res
                
            except ValueError:
                return error_format

        elif "query_count" in parsed_info:
            try:
                raw = parsed_info["query_count"].strip()
                if not raw:
                    return error_format
                
                vec_strs = raw.split(";")
                if len(vec_strs) < 1 or len(vec_strs) > 8:
                    return error_batch_size
                
                vectors = []
                for vec_str in vec_strs:
                    vector = self._parse_vector(vec_str.strip())
                    
                    if vector == self.target_vector:
                        return error_target
                    
                    vectors.append(vector)
                
                if len(vectors) != len(set(tuple(v) for v in vectors)):
                    return error_duplicate
                
                count = sum(self._evaluate_function(v) for v in vectors)
                self.query_count += 1
                
                if count > 0:
                    self.has_positive = True
                if count < len(vectors):
                    self.has_negative = True
                
                return str(count)
                
            except ValueError:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        mapping = {
            "是": "否",
            "否": "是",
            "Yes": "No",
            "No": "Yes",
            "yes": "no",
            "no": "yes"
        }
        
        if correct in mapping:
            return mapping[correct]
            
        return correct + "_WRONG"