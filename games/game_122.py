from .base import Game
import re

class TrafficMultisetRuleInferenceGame(Game):

    contextualized_rule_zh_1 = """\
欢迎进入【智能交通路网测试系统】。

本系统正在监控一个十字路口的车辆通行记录（集合 M）。共有 10 种类型的车辆（编号 0 到 9，分别代表轿车、货车、公交车等）。系统仅记录各车辆类型通过的数量，不记录通行顺序。

路网控制中枢会根据一个保密算法 f，计算出当前的“交通负荷指数” v（取值范围 0 到 9），计算结果对 10 取模。该保密算法 f 必然是以下四种模型之一：

- 规则 A（权重累加模10）：负荷指数等于所有已通行车辆的类型编号之和，对 10 取模
- 规则 B（车型种数模10）：负荷指数等于已通行过的不同车辆种类数，对 10 取模
- 规则 C（特殊车型计数模10）：负荷指数等于奇数编号车型（1、3、5、7、9）的总通行辆数，对 10 取模
- 规则 D（偶次通行车型模10）：负荷指数等于通行次数为正偶数的车辆种类数，对 10 取模；未通行（次数为0）的车型不计入

初始状态会告知你：
- 当前各类型车辆（0 到 9）的通行次数
- 当前交通负荷指数 v
- 目标交通负荷指数 T

你的任务是：
1. 准确推断出系统实际采用的保密算法（A、B、C 或 D）
2. 通过添加数字操作（录入特定类型的车辆），使交通负荷指数达到目标值 T
3. 提供充分的观测证据以支持你的推断

你可以进行以下系统操作（每次只能进行一种操作）：

1. **添加操作**：向集合中添加一个数字 d（0 到 9），代表一辆对应编号的车辆通行，该车型的计数加 1，系统会自动更新负荷指数
   格式：<add>d</add>
   例如：<add>5</add>

2. **数值查询**：查询当前的交通负荷指数 v
   格式：<query_value></query_value>

3. **差值判定**：询问当前负荷指数是否等于上一次已知指数加上 k（对 10 取模），其中 k 的范围是 -9 到 9
   格式：<query_delta>k</query_delta>
   例如：<query_delta>3</query_delta>

4. **状态回顾**：查询当前各车型通过的总次数
   格式：<query_counts></query_counts>

当你准备好提交调查报告时，请使用以下格式：

<answer>rule=X, evidence=你的证据描述</answer>

其中 X 为 A、B、C 或 D 之一。证据部分需说明你是如何通过观测排除其他模型的，至少包含两条独立的观测证据。

注意事项：
- 所有计算均对 10 取模
- 请尽可能少地使用添加操作
- 如果模型推断错误，或指数未达到目标值，或证据不足，测试将失败

初始状态：
- 各车型通行次数：{initial_counts}
- 当前负荷指数：{initial_value}
- 目标负荷指数：{target_value}
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the [Smart Traffic Network Testing System].

The system is monitoring vehicle pass records (multiset M) at an intersection. There are 10 types of vehicles (codes 0 to 9, representing sedans, trucks, buses, etc.). The system only records the pass counts for each vehicle type, ignoring the passing order.

The network control center calculates the current "Traffic Load Index" v (ranging from 0 to 9) using a secret algorithm f, modulo 10. The secret algorithm f is strictly one of the following four models:

- Rule A (Code sum modulo 10): Load index equals the sum of the codes of all passed vehicles, modulo 10
- Rule B (Distinct types modulo 10): Load index equals the number of distinct vehicle types that have passed, modulo 10
- Rule C (Odd-code count modulo 10): Load index equals the total passing count of odd-coded vehicles (1, 3, 5, 7, 9), modulo 10
- Rule D (Even-occurrence types modulo 10): Load index equals the count of vehicle types that have passed a positive even number of times, modulo 10; types with zero occurrences are excluded

Initial information provided:
- Current pass counts for each vehicle type (0 to 9)
- Current Traffic Load Index v
- Target Traffic Load Index T

Your tasks are:
1. Accurately infer the actual secret algorithm used (A, B, C, or D)
2. Make the Load Index reach the target value T by adding digits (logging specific vehicle types)
3. Provide sufficient observational evidence to support your inference

You can perform the following system operations (one per turn):

1. **Add operation**: Add a digit d (0 to 9) to the set, representing a vehicle passing. Its count increments by 1, and the system updates the load index.
   Format: <add>d</add>
   Example: <add>5</add>

2. **Value query**: Query the current Traffic Load Index v
   Format: <query_value></query_value>

3. **Delta query**: Ask if the current load index equals the last known index plus k (modulo 10), where k is from -9 to 9
   Format: <query_delta>k</query_delta>
   Example: <query_delta>3</query_delta>

4. **Counts query**: Query the current pass counts of all vehicle types
   Format: <query_counts></query_counts>

When ready to submit your report, use the following format:

<answer>rule=X, evidence=your evidence description</answer>

Where X is A, B, C, or D. The evidence part must explain how you ruled out other models and include at least two independent observational pieces of evidence.

Notes:
- All calculations are modulo 10
- Use as few add operations as possible
- The test fails if the rule inference is wrong, the index misses the target, or evidence is insufficient

Initial state:
- Vehicle pass counts: {initial_counts}
- Current Load Index: {initial_value}
- Target Load Index: {target_value}
"""

    contextualized_rule_zh_2 = """\
欢迎使用【临床生化指标评估系统】。

本系统正在分析一份患者的生物标志物检测档案（集合 M）。共有 10 种生物标志物（编号 0 到 9，分别代表血糖、血脂、转氨酶等）。系统仅记录各标志物出现的阳性频次，没有时序概念。

医疗AI会根据一个保密诊断模型 f，计算出当前的“健康风险评分” v（取值范围 0 到 9），计算结果对 10 取模。该保密模型 f 是以下四种机制之一：

- 规则 A（指标编号和模10）：风险评分等于所有检出的标志物编号之和，对 10 取模
- 规则 B（异常种类数模10）：风险评分等于检出阳性的不同标志物种类数，对 10 取模
- 规则 C（奇数指标计数模10）：风险评分等于奇数编号标志物（1、3、5、7、9）的检出总次数，对 10 取模
- 规则 D（偶数频次种类模10）：风险评分等于检出次数为正偶数的标志物种类数，对 10 取模；未检出（次数为0）的不计入

初始状态会告知你：
- 各标志物（0 到 9）当前的检出频次
- 当前风险评分 v
- 目标风险评分 T

你的任务是：
1. 准确推断出AI实际采用的诊断模型（A、B、C 或 D）
2. 通过添加数字操作（追加检测特定标志物），使风险评分达到目标值 T
3. 提供充分的临床观测证据以支持你的推断

你可以进行以下系统操作（每次只能进行一种操作）：

1. **添加操作**：向档案中添加一次编号为 d（0 到 9）的标志物检出记录，该指标频次加 1，系统会自动更新风险评分
   格式：<add>d</add>
   例如：<add>5</add>

2. **数值查询**：查询当前的健康风险评分 v
   格式：<query_value></query_value>

3. **差值判定**：询问当前评分是否等于上一次已知评分加上 k（对 10 取模），其中 k 的范围是 -9 到 9
   格式：<query_delta>k</query_delta>
   例如：<query_delta>3</query_delta>

4. **状态回顾**：查询当前各标志物的检出总频次
   格式：<query_counts></query_counts>

当你准备好提交诊断报告时，请使用以下格式：

<answer>rule=X, evidence=你的证据描述</answer>

其中 X 为 A、B、C 或 D 之一。证据部分需说明你是如何通过观测排除其他模型的，至少包含两条独立的观测证据。

注意事项：
- 所有计算均对 10 取模
- 请尽可能少地使用添加操作以节约医疗资源
- 如果模型推断错误，或评分未达到目标值，或证据不足，评估将失败

初始状态：
- 各标志物检出频次：{initial_counts}
- 当前风险评分：{initial_value}
- 目标风险评分：{target_value}
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the [Clinical Biochemical Indicator Assessment System].

The system is analyzing a patient's biomarker detection profile (multiset M). There are 10 biomarkers (codes 0 to 9, representing glucose, lipids, transaminase, etc.). The system records only the positive occurrence counts for each biomarker, without any chronological order.

The medical AI calculates the current "Health Risk Score" v (ranging from 0 to 9) based on a secret diagnostic model f, modulo 10. The secret model f is exclusively one of the following four mechanisms:

- Rule A (Indicator sum modulo 10): Risk score equals the sum of the codes of all detected biomarkers, modulo 10
- Rule B (Distinct abnormalities modulo 10): Risk score equals the number of distinct biomarkers detected, modulo 10
- Rule C (Odd-indicator count modulo 10): Risk score equals the total occurrence count of odd-coded biomarkers (1, 3, 5, 7, 9), modulo 10
- Rule D (Even-frequency types modulo 10): Risk score equals the count of biomarker types detected a positive even number of times, modulo 10; undetected ones (count 0) are excluded

Initial information provided:
- Current detection counts for each biomarker (0 to 9)
- Current Health Risk Score v
- Target Health Risk Score T

Your tasks are:
1. Accurately infer the actual diagnostic model used by the AI (A, B, C, or D)
2. Make the Risk Score reach the target value T by adding digits (appending biomarker detections)
3. Provide sufficient clinical observational evidence to support your inference

You can perform the following system operations (one per turn):

1. **Add operation**: Add a detection record for biomarker d (0 to 9) to the profile. Its count increments by 1, and the system updates the risk score.
   Format: <add>d</add>
   Example: <add>5</add>

2. **Value query**: Query the current Health Risk Score v
   Format: <query_value></query_value>

3. **Delta query**: Ask if the current score equals the last known score plus k (modulo 10), where k is from -9 to 9
   Format: <query_delta>k</query_delta>
   Example: <query_delta>3</query_delta>

4. **Counts query**: Query the current detection counts of all biomarkers
   Format: <query_counts></query_counts>

When ready to submit your diagnostic report, use the following format:

<answer>rule=X, evidence=your evidence description</answer>

Where X is A, B, C, or D. The evidence part must explain how you ruled out other models and include at least two independent clinical observational pieces of evidence.

Notes:
- All calculations are modulo 10
- Minimize add operations to conserve medical resources
- The assessment fails if the rule inference is wrong, the score misses the target, or evidence is insufficient

Initial state:
- Biomarker detection counts: {initial_counts}
- Current Risk Score: {initial_value}
- Target Risk Score: {target_value}
"""

    contextualized_rule_zh_3 = """\
欢迎登录【学生核心素养评价系统】。

本系统正在追踪一名学生的课外技能学习记录（集合 M）。共有 10 门课外技能（编号 0 到 9，分别代表编程、绘画、演讲等）。系统仅汇总各技能的完成课时数，不考虑学习先后顺序。

教务后台会通过一个隐藏的评估公式 f，计算出该生当前的“综合素养等级” v（取值范围 0 到 9），计算结果对 10 取模。该公式 f 必定是以下四种评价标准之一：

- 规则 A（模块编号和模10）：素养等级等于所有已学技能模块编号之和，对 10 取模
- 规则 B（涉猎广度模10）：素养等级等于已学习过的不同技能种类数，对 10 取模
- 规则 C（特定技能计数模10）：素养等级等于奇数编号技能（1、3、5、7、9）的总完成课时数，对 10 取模
- 规则 D（偶数课时技能模10）：素养等级等于完成课时数为正偶数的技能种类数，对 10 取模；未学习（课时为0）的技能不计入

初始状态会告知你：
- 当前各门技能（0 到 9）的完成课时数
- 当前综合素养等级 v
- 目标综合素养等级 T

你的任务是：
1. 准确推断出教务系统实际采用的评估公式（A、B、C 或 D）
2. 通过添加数字操作（为该生额外安排特定技能课时），使综合素养等级达到目标值 T
3. 提供充分的评估依据以支持你的推断

你可以进行以下系统操作（每次只能进行一种操作）：

1. **添加操作**：为编号 d（0 到 9）的技能增加 1 个课时记录，系统将自动更新素养等级
   格式：<add>d</add>
   例如：<add>5</add>

2. **数值查询**：查询当前的综合素养等级 v
   格式：<query_value></query_value>

3. **差值判定**：询问当前等级是否等于上一次已知等级加上 k（对 10 取模），其中 k 的范围是 -9 到 9
   格式：<query_delta>k</query_delta>
   例如：<query_delta>3</query_delta>

4. **状态回顾**：查询当前各技能的累计完成课时数
   格式：<query_counts></query_counts>

当你准备好提交评价报告时，请使用以下格式：

<answer>rule=X, evidence=你的证据描述</answer>

其中 X 为 A、B、C 或 D 之一。证据部分需说明你是如何通过观测排除其他公式的，至少包含两条独立的学情观测证据。

注意事项：
- 所有计算均对 10 取模
- 请尽量以最少的额外添加操作完成目标，减轻学生负担
- 如果公式推断错误，或等级未达标，或证据不足，评价流程将中止

初始状态：
- 各技能完成课时：{initial_counts}
- 当前综合素养等级：{initial_value}
- 目标综合素养等级：{target_value}
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the [Student Core Competency Evaluation System].

The system tracks a student's extracurricular skill learning records (multiset M). There are 10 extracurricular skills (codes 0 to 9, representing programming, drawing, public speaking, etc.). The system aggregates the completed session counts for each skill, ignoring the learning sequence.

The academic backend calculates the current "Comprehensive Competency Grade" v (ranging from 0 to 9) using a hidden evaluation formula f, modulo 10. The formula f is strictly one of the following four evaluation rubrics:

- Rule A (Module code sum modulo 10): Grade equals the sum of the codes of all learned skill modules, modulo 10
- Rule B (Learning breadth modulo 10): Grade equals the number of distinct skills learned, modulo 10
- Rule C (Specific skill count modulo 10): Grade equals the total completed session count of odd-coded skills (1, 3, 5, 7, 9), modulo 10
- Rule D (Even-session skills modulo 10): Grade equals the count of skill types completed a positive even number of times, modulo 10; unlearned skills (0 sessions) are excluded

Initial information provided:
- Current completed session counts for each skill (0 to 9)
- Current Comprehensive Competency Grade v
- Target Comprehensive Competency Grade T

Your tasks are:
1. Accurately infer the actual evaluation formula used by the academic system (A, B, C, or D)
2. Make the Competency Grade reach the target value T by adding digits (assigning additional skill sessions)
3. Provide sufficient evaluation evidence to support your inference

You can perform the following system operations (one per turn):

1. **Add operation**: Add 1 session record for skill d (0 to 9). The system will automatically update the competency grade.
   Format: <add>d</add>
   Example: <add>5</add>

2. **Value query**: Query the current Comprehensive Competency Grade v
   Format: <query_value></query_value>

3. **Delta query**: Ask if the current grade equals the last known grade plus k (modulo 10), where k is from -9 to 9
   Format: <query_delta>k</query_delta>
   Example: <query_delta>3</query_delta>

4. **Counts query**: Query the current cumulative session counts of all skills
   Format: <query_counts></query_counts>

When ready to submit your evaluation report, use the following format:

<answer>rule=X, evidence=your evidence description</answer>

Where X is A, B, C, or D. The evidence part must explain how you ruled out other formulas and include at least two independent pieces of academic observational evidence.

Notes:
- All calculations are modulo 10
- Minimize add operations to reduce student workload
- The evaluation fails if the formula inference is wrong, the grade misses the target, or evidence is insufficient

Initial state:
- Skill completed sessions: {initial_counts}
- Current Competency Grade: {initial_value}
- Target Competency Grade: {target_value}
"""

    contextualized_rule_zh_4 = """\
欢迎接入【工业柔性产线标定系统】。

本系统正在校验一个装配站的零部件消耗清单（集合 M）。共有 10 种工业零部件（编号 0 到 9，分别代表齿轮、轴承、传感器等）。系统仅统计每种零部件的消耗件数，不考虑装配工序先后。

中控PLC会根据一个专有标定协议 f，计算出当前产线的“系统校准参数” v（取值范围 0 到 9），计算结果对 10 取模。该标定协议 f 一定是以下四种逻辑之一：

- 规则 A（物料批号和模10）：校准参数等于所有已消耗零部件编号之和，对 10 取模
- 规则 B（物料种数模10）：校准参数等于产线消耗的不同零部件种类数，对 10 取模
- 规则 C（特定物料计数模10）：校准参数等于奇数编号零部件（1、3、5、7、9）的消耗总件数，对 10 取模
- 规则 D（偶数件数物料模10）：校准参数等于消耗件数为正偶数的零部件种类数，对 10 取模；未消耗（件数为0）的零部件不计入

初始状态会告知你：
- 当前各零部件（0 到 9）的消耗件数
- 当前系统校准参数 v
- 目标系统校准参数 T

你的任务是：
1. 准确推断出PLC实际采用的标定协议（A、B、C 或 D）
2. 通过添加数字操作（向产线投料特定零部件），使校准参数达到目标值 T
3. 提供充分的生产测试证据以支持你的推断

你可以进行以下系统操作（每次只能进行一种操作）：

1. **添加操作**：向装配站投放一件编号为 d（0 到 9）的零部件，该物料消耗加 1，PLC将自动刷新校准参数
   格式：<add>d</add>
   例如：<add>5</add>

2. **数值查询**：查询当前的系统校准参数 v
   格式：<query_value></query_value>

3. **差值判定**：询问当前参数是否等于上一次已知参数加上 k（对 10 取模），其中 k 的范围是 -9 到 9
   格式：<query_delta>k</query_delta>
   例如：<query_delta>3</query_delta>

4. **状态回顾**：查询当前各零部件的累计消耗件数
   格式：<query_counts></query_counts>

当你准备好输出校准报告时，请使用以下格式：

<answer>rule=X, evidence=你的证据描述</answer>

其中 X 为 A、B、C 或 D 之一。证据部分需说明你是如何通过测试排除其他逻辑的，至少包含两条独立的投料测试证据。

注意事项：
- 所有计算均对 10 取模
- 请尽可能少地使用添加操作以免造成物料浪费
- 如果协议推断错误，或参数未达标，或证据不足，产线标定将失败

初始状态：
- 各零部件消耗件数：{initial_counts}
- 当前系统校准参数：{initial_value}
- 目标系统校准参数：{target_value}
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the [Industrial Flexible Assembly Line Calibration System].

The system is verifying a parts consumption list (multiset M) at an assembly station. There are 10 industrial components (codes 0 to 9, representing gears, bearings, sensors, etc.). The system aggregates only the consumed quantities of each component, independent of the assembly sequence.

The central PLC calculates the current "System Calibration Parameter" v (ranging from 0 to 9) based on a proprietary calibration protocol f, modulo 10. The calibration protocol f is strictly one of the following four logics:

- Rule A (Material code sum modulo 10): Calibration parameter equals the sum of the codes of all consumed components, modulo 10
- Rule B (Material types modulo 10): Calibration parameter equals the number of distinct components consumed, modulo 10
- Rule C (Specific material count modulo 10): Calibration parameter equals the total consumed quantity of odd-coded components (1, 3, 5, 7, 9), modulo 10
- Rule D (Even-quantity materials modulo 10): Calibration parameter equals the count of component types consumed in a positive even quantity, modulo 10; unconsumed ones (quantity 0) are excluded

Initial information provided:
- Current consumption quantities for each component (0 to 9)
- Current System Calibration Parameter v
- Target System Calibration Parameter T

Your tasks are:
1. Accurately infer the actual calibration protocol used by the PLC (A, B, C, or D)
2. Make the Calibration Parameter reach the target value T by adding digits (feeding specific components)
3. Provide sufficient production test evidence to support your inference

You can perform the following system operations (one per turn):

1. **Add operation**: Feed one component of code d (0 to 9) to the station. Its consumption increments by 1, and the PLC refreshes the parameter.
   Format: <add>d</add>
   Example: <add>5</add>

2. **Value query**: Query the current System Calibration Parameter v
   Format: <query_value></query_value>

3. **Delta query**: Ask if the current parameter equals the last known parameter plus k (modulo 10), where k is from -9 to 9
   Format: <query_delta>k</query_delta>
   Example: <query_delta>3</query_delta>

4. **Counts query**: Query the current cumulative consumption of all components
   Format: <query_counts></query_counts>

When ready to export your calibration report, use the following format:

<answer>rule=X, evidence=your evidence description</answer>

Where X is A, B, C, or D. The evidence part must explain how you ruled out other logics and include at least two independent feeding test pieces of evidence.

Notes:
- All calculations are modulo 10
- Minimize add operations to prevent material waste
- The calibration fails if the protocol inference is wrong, the parameter misses the target, or evidence is insufficient

Initial state:
- Component consumption quantities: {initial_counts}
- Current Calibration Parameter: {initial_value}
- Target Calibration Parameter: {target_value}
"""

    contextualized_rule_zh_5 = """\
欢迎进入【司法案件证据链分析系统】。

本系统正在处理一宗案件的电子证据卷宗（集合 M）。共有 10 类法定证据（编号 0 到 9，分别代表证人证言、物证、书证、视听资料等）。系统仅汇总各类证据的提交份数，不包含提交时间的先后。

智能审判辅助系统会根据一项内置的评定规则 f，计算出该案当前的“案件复杂程度评级” v（取值范围 0 到 9），计算结果对 10 取模。该评定规则 f 必然是以下四种机制之一：

- 规则 A（法条编号和模10）：复杂评级等于所有已提交证据的分类编号之和，对 10 取模
- 规则 B（证据广度模10）：复杂评级等于卷宗中包含的不同证据种类数，对 10 取模
- 规则 C（特定质证计数模10）：复杂评级等于奇数编号证据（1、3、5、7、9）的提交总份数，对 10 取模
- 规则 D（偶数份数证据模10）：复杂评级等于提交份数为正偶数的证据种类数，对 10 取模；未提交（份数为0）的证据类型不计入

初始状态会告知你：
- 当前各类证据（0 到 9）的提交份数
- 当前案件复杂程度评级 v
- 目标案件复杂程度评级 T

你的任务是：
1. 准确推断出系统实际采用的评定规则（A、B、C 或 D）
2. 通过添加数字操作（向卷宗补充特定类别的证据），使复杂程度评级达到目标值 T
3. 提供充分的法理和逻辑证据以支持你的推断

你可以进行以下系统操作（每次只能进行一种操作）：

1. **添加操作**：向卷宗中录入一份编号为 d（0 到 9）的证据，该类型证据份数加 1，系统将重算复杂评级
   格式：<add>d</add>
   例如：<add>5</add>

2. **数值查询**：查询当前的案件复杂程度评级 v
   格式：<query_value></query_value>

3. **差值判定**：询问当前评级是否等于上一次已知评级加上 k（对 10 取模），其中 k 的范围是 -9 到 9
   格式：<query_delta>k</query_delta>
   例如：<query_delta>3</query_delta>

4. **状态回顾**：查询当前各类证据的累计提交份数
   格式：<query_counts></query_counts>

当你准备好提交分析意见书时，请使用以下格式：

<answer>rule=X, evidence=你的证据描述</answer>

其中 X 为 A、B、C 或 D 之一。证据部分需说明你是如何通过质证排除其他机制的，至少包含两条独立的卷宗测试证据。

注意事项：
- 所有计算均对 10 取模
- 请尽可能少地使用添加操作以维护卷宗的严谨性
- 如果规则推断错误，或评级未达标，或证据不足，分析流程将被驳回

初始状态：
- 各类证据提交份数：{initial_counts}
- 当前复杂程度评级：{initial_value}
- 目标复杂程度评级：{target_value}
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the [Judicial Case Evidence Chain Analysis System].

The system is processing the electronic evidence dossier for a case (multiset M). There are 10 categories of legal evidence (codes 0 to 9, representing witness statements, physical evidence, documentary evidence, audio/video data, etc.). The system aggregates the submitted item counts for each category, ignoring submission chronological order.

The intelligent trial assistance system calculates the current "Case Complexity Rating" v (ranging from 0 to 9) using a built-in assessment rule f, modulo 10. The rule f is strictly one of the following four mechanisms:

- Rule A (Statute code sum modulo 10): Complexity rating equals the sum of the category codes of all submitted evidence items, modulo 10
- Rule B (Evidence breadth modulo 10): Complexity rating equals the number of distinct evidence categories in the dossier, modulo 10
- Rule C (Specific evidence count modulo 10): Complexity rating equals the total item count of odd-coded evidence (1, 3, 5, 7, 9), modulo 10
- Rule D (Even-item evidence modulo 10): Complexity rating equals the count of evidence categories submitted in a positive even number of items, modulo 10; unsubmitted ones (item count 0) are excluded

Initial information provided:
- Current submitted item counts for each evidence category (0 to 9)
- Current Case Complexity Rating v
- Target Case Complexity Rating T

Your tasks are:
1. Accurately infer the actual assessment rule used by the system (A, B, C, or D)
2. Make the Complexity Rating reach the target value T by adding digits (supplementing specific categories of evidence)
3. Provide sufficient legal and logical evidence to support your inference

You can perform the following system operations (one per turn):

1. **Add operation**: Log an evidence item of category d (0 to 9) into the dossier. Its item count increments by 1, and the system recalculates the rating.
   Format: <add>d</add>
   Example: <add>5</add>

2. **Value query**: Query the current Case Complexity Rating v
   Format: <query_value></query_value>

3. **Delta query**: Ask if the current rating equals the last known rating plus k (modulo 10), where k is from -9 to 9
   Format: <query_delta>k</query_delta>
   Example: <query_delta>3</query_delta>

4. **Counts query**: Query the current cumulative item counts of all evidence categories
   Format: <query_counts></query_counts>

When ready to submit your analysis opinion, use the following format:

<answer>rule=X, evidence=your evidence description</answer>

Where X is A, B, C, or D. The evidence part must explain how you ruled out other mechanisms and include at least two independent pieces of dossier testing evidence.

Notes:
- All calculations are modulo 10
- Minimize add operations to maintain the rigor of the dossier
- The analysis will be rejected if the rule inference is wrong, the rating misses the target, or evidence is insufficient

Initial state:
- Evidence item counts: {initial_counts}
- Current Complexity Rating: {initial_value}
- Target Complexity Rating: {target_value}
"""

    game_rule_zh = """\
我们来玩一个"多重集合规则推理"游戏。规则如下：

游戏设定了一个由数字 0 到 9 构成的多重集合 M，每个数字可以出现多次。集合仅以各数字的出现次数来刻画，没有顺序或位置的概念。

系统维护一个显示值 v（取值范围 0 到 9），它由集合 M 按照某个秘密规则 f 计算得出，计算结果对 10 取模。秘密规则 f 从以下四种候选规则中选择一种：

- 规则 A（和的模10）：显示值等于集合中所有元素数值之和，对 10 取模
- 规则 B（不同种数的模10）：显示值等于集合中出现过的不同数字的种类数，对 10 取模
- 规则 C（奇数元素计数的模10）：显示值等于集合中奇数字（1、3、5、7、9）元素的总个数，对 10 取模
- 规则 D（偶次出现的种类数的模10）：显示值等于出现次数为正且为偶数的数字种类个数，对 10 取模；未出现（次数为0）的数字不计入

初始状态会告知你：
- 各数字（0 到 9）的当前出现次数
- 当前显示值 v
- 目标显示值 T

你的任务是：
1. 正确推断出实际采用的秘密规则（A、B、C 或 D）
2. 通过添加数字操作，使显示值达到目标值 T
3. 提供充分的证据支持你的推断

你可以进行以下操作（每次只能进行一种操作）：

1. **添加操作**：向集合中添加一个数字 d（0 到 9），该数字的计数会加 1，显示值会根据秘密规则更新
   格式：<add>d</add>
   例如：<add>5</add>

2. **数值查询**：查询当前的显示值 v
   格式：<query_value></query_value>

3. **差值判定**：询问当前显示值是否等于上一次已知显示值加上 k（对 10 取模），其中 k 的范围是 -9 到 9
   格式：<query_delta>k</query_delta>
   例如：<query_delta>3</query_delta>

4. **状态回顾**：查询当前各数字的出现次数
   格式：<query_counts></query_counts>

当你准备好提交答案时，请使用以下格式：

<answer>rule=X, evidence=你的证据描述</answer>

其中 X 为 A、B、C 或 D 之一。证据部分需要说明你是如何通过观测排除其他候选规则的，至少包含两条独立的观测证据。

注意事项：
- 所有计算均对 10 取模
- 请尽可能少地使用添加操作
- 如果规则推断错误，或显示值未达到目标值，或证据不足，游戏将失败

初始状态：
- 各数字出现次数：{initial_counts}
- 当前显示值：{initial_value}
- 目标显示值：{target_value}
"""

    game_rule_en = """\
Let's play a "Multiset Rule Inference" game. Here are the rules:

The game has a multiset M consisting of digits 0 to 9, where each digit can appear multiple times. The set is characterized only by the occurrence count of each digit, with no notion of order or position.

The system maintains a display value v (ranging from 0 to 9), which is computed from the multiset M according to a secret rule f, with the result taken modulo 10. The secret rule f is selected from one of the following four candidate rules:

- Rule A (sum modulo 10): display value equals the sum of all element values in the set, modulo 10
- Rule B (distinct count modulo 10): display value equals the number of distinct digit types present in the set, modulo 10
- Rule C (odd count modulo 10): display value equals the total count of odd digits (1, 3, 5, 7, 9) in the set, modulo 10
- Rule D (even-occurrence types modulo 10): display value equals the count of digit types that appear a positive even number of times, modulo 10; digits with zero occurrences are not counted

Initial information provided:
- Current occurrence count for each digit (0 to 9)
- Current display value v
- Target display value T

Your tasks are:
1. Correctly infer the actual secret rule (A, B, C, or D)
2. Make the display value reach the target value T by adding digits
3. Provide sufficient evidence to support your inference

You can perform the following operations (one operation per turn):

1. **Add operation**: Add a digit d (0 to 9) to the set, incrementing its count by 1, and the display value will be updated according to the secret rule
   Format: <add>d</add>
   Example: <add>5</add>

2. **Value query**: Query the current display value v
   Format: <query_value></query_value>

3. **Delta query**: Ask whether the current display value equals the last known display value plus k (modulo 10), where k ranges from -9 to 9
   Format: <query_delta>k</query_delta>
   Example: <query_delta>3</query_delta>

4. **Counts query**: Query the current occurrence counts of all digits
   Format: <query_counts></query_counts>

When you are ready to submit your answer, use the following format:

<answer>rule=X, evidence=your evidence description</answer>

Where X is one of A, B, C, or D. The evidence part should explain how you ruled out other candidate rules through observations, and must include at least two independent pieces of evidence.

Notes:
- All calculations are modulo 10
- Use as few add operations as possible
- The game fails if the rule inference is incorrect, the display value does not reach the target, or the evidence is insufficient

Initial state:
- Digit occurrence counts: {initial_counts}
- Current display value: {initial_value}
- Target display value: {target_value}
"""

    user_prompt_zh = "你可以开始操作了。"
    user_prompt_en = "You can start now."

    tags = ["answer", "add", "query_value", "query_delta", "query_counts"]

    reasoning_type = "溯因推理"
    data_structure = "集合"

    DIFFICULTY_CONFIG = {
        1: {
            "initial_counts": [2, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            "rule": "A",
            "target_value": 7,
            "initial_value": 1,
        },
        2: {
            "initial_counts": [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            "rule": "B",
            "target_value": 5,
            "initial_value": 3,
        },
        3: {
            "initial_counts": [2, 1, 2, 1, 0, 0, 0, 0, 0, 0],
            "rule": "C",
            "target_value": 6,
            "initial_value": 2,
        },
        4: {
            "initial_counts": [2, 3, 2, 1, 2, 1, 0, 0, 0, 0],
            "rule": "D",
            "target_value": 1,
            "initial_value": 3,
        },
        5: {
            "initial_counts": [1, 2, 3, 2, 1, 1, 0, 0, 0, 0],
            "rule": "A",
            "target_value": 8,
            "initial_value": 3,
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        
        self.counts = cfg["initial_counts"][:]
        self.rule = cfg["rule"]
        self.target_value = cfg["target_value"]
        self.current_value = cfg["initial_value"]
        self.last_queried_value = cfg["initial_value"]
        self.add_count = 0
        self.max_adds = 8
        
        self._game_info["initial_counts"] = self._format_counts(self.counts)
        self._game_info["initial_value"] = self.current_value
        self._game_info["target_value"] = self.target_value

    def _format_counts(self, counts):
        return "[" + ", ".join(f"{i}:{counts[i]}" for i in range(10)) + "]"

    def _compute_value(self, counts):
        if self.rule == "A":
            total = sum(i * counts[i] for i in range(10))
            return total % 10
        elif self.rule == "B":
            distinct = sum(1 for c in counts if c > 0)
            return distinct % 10
        elif self.rule == "C":
            odd_count = sum(counts[i] for i in [1, 3, 5, 7, 9])
            return odd_count % 10
        elif self.rule == "D":
            even_occurrence = sum(1 for c in counts if c > 0 and c % 2 == 0)
            return even_occurrence % 10
        else:
            raise ValueError(f"Unknown rule: {self.rule}")

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        rule_match = re.search(r'rule\s*=\s*([A-D])', raw_ans, re.IGNORECASE)
        evidence_match = re.search(r'evidence\s*=\s*(.+)', raw_ans, re.IGNORECASE | re.DOTALL)
        
        if not rule_match:
            return False
        
        inferred_rule = rule_match.group(1).upper()
        evidence = evidence_match.group(1).strip() if evidence_match else ""
        
        if inferred_rule != self.rule:
            return False
            
        if self.current_value != self.target_value and self.add_count != 0:
            return False
            
        if len(evidence) < 20:
            return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        if "add" in parsed_info:
            return self._handle_add(parsed_info["add"])
        elif "query_value" in parsed_info:
            return self._handle_query_value()
        elif "query_delta" in parsed_info:
            return self._handle_query_delta(parsed_info["query_delta"])
        elif "query_counts" in parsed_info:
            return self._handle_query_counts()
        else:
            raise ValueError("No valid operation found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit() and len(correct) <= 2:
            val = int(correct)
            wrong_val = (val + 1) % 10
            return str(wrong_val)
        
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            elif correct == "否":
                return "是"
        else:
            lower_c = correct.lower()
            if lower_c == "yes":
                if correct.isupper(): return "NO"
                if correct.istitle(): return "No"
                return "no"
            elif lower_c == "no":
                if correct.isupper(): return "YES"
                if correct.istitle(): return "Yes"
                return "yes"
        
        return f"{correct}_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        is_zh = self.config.language == "zh"

        queries.append({
            "query": "<query_value></query_value>",
            "answer": str(self.current_value)
        })

        queries.append({
            "query": "<query_counts></query_counts>",
            "answer": self._format_counts(self.counts)
        })

        for k in range(-9, 10):
            expected = (self.last_queried_value + k) % 10
            is_equal = (self.current_value == expected)
            
            if is_zh:
                ans = "是" if is_equal else "否"
            else:
                ans = "Yes" if is_equal else "No"
            
            queries.append({
                "query": f"<query_delta>{k}</query_delta>",
                "answer": ans
            })

        temp_counts = self.counts[:]
        temp_value = self.current_value
        temp_add_count = 0
        
        while temp_value != self.target_value and temp_add_count < self.max_adds:
            best_digit = None
            for d in range(10):
                trial_counts = temp_counts[:]
                trial_counts[d] += 1
                trial_value = self._compute_value(trial_counts)
                if trial_value == self.target_value:
                    best_digit = d
                    break
            
            if best_digit is None:
                best_digit = 1
            
            temp_counts[best_digit] += 1
            temp_value = self._compute_value(temp_counts)
            temp_add_count += 1
            
            if is_zh:
                ans = f"已添加数字 {best_digit}。当前已使用 {temp_add_count} 次添加操作。"
            else:
                ans = f"Added digit {best_digit}. Used {temp_add_count} add operation(s)."
            
            queries.append({
                "query": f"<add>{best_digit}</add>",
                "answer": ans
            })

        queries.append({
            "query": "<query_value></query_value>",
            "answer": str(temp_value)
        })

        queries.append({
            "query": "<query_counts></query_counts>",
            "answer": self._format_counts(temp_counts)
        })

        return queries

    def _handle_add(self, digit_str):
        try:
            digit = int(digit_str.strip())
            if digit < 0 or digit > 9:
                raise ValueError
        except:
            if self.config.language == "zh":
                return "错误：数字必须在 0 到 9 之间。"
            else:
                return "Error: Digit must be between 0 and 9."
        
        if self.add_count >= self.max_adds:
            if self.config.language == "zh":
                return f"错误：已达到最大添加次数限制（{self.max_adds}次）。"
            else:
                return f"Error: Maximum add operations ({self.max_adds}) reached."
        
        self.counts[digit] += 1
        self.add_count += 1
        
        self.current_value = self._compute_value(self.counts)
        
        if self.config.language == "zh":
            return f"已添加数字 {digit}。当前已使用 {self.add_count} 次添加操作。"
        else:
            return f"Added digit {digit}. Used {self.add_count} add operation(s)."

    def _handle_query_value(self):
        self.last_queried_value = self.current_value
        return str(self.current_value)

    def _handle_query_delta(self, k_str):
        try:
            k = int(k_str.strip())
            if k < -9 or k > 9:
                raise ValueError
        except:
            if self.config.language == "zh":
                return "错误：k 必须在 -9 到 9 之间。"
            else:
                return "Error: k must be between -9 and 9."
        
        expected = (self.last_queried_value + k) % 10
        
        if self.config.language == "zh":
            return "是" if self.current_value == expected else "否"
        else:
            return "Yes" if self.current_value == expected else "No"

    def _handle_query_counts(self):
        return self._format_counts(self.counts)