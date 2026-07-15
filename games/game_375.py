import random
from itertools import product
from .base import Game

class StringOrderingGame(Game):

    game_rule_zh = """\
我们来玩一个"字符串排序规则推理"游戏。规则如下：

1. 字母表包含四个字符：A、B、C、D。
2. 存在一个固定集合 S，包含 {n} 个长度为 3 的字符串（例如：AAA、ABC、DCA 等），所有字符串互不相同。
3. 我已经秘密设定了一个比较规则 C，它能对 S 中任意两个不同的字符串给出唯一的先后关系（无并列）。
4. 这个比较规则由以下隐藏参数决定：
   - 字符优先级：四个字符 A、B、C、D 有一个优先级排序，映射到数值 0、1、2、3
   - 读取方向：从左到右 或 从右到左
   - 聚合模式：字典序 或 加权和模式
     * 字典序：按读取方向逐位比较，首个不同位置用字符优先级决定先后
     * 加权和模式：三个位置各有权重（1、2 或 3），计算每个字符串的加权分数，分数小的在前；若分数相同则用字典序打破平手

通过查询推断出这个隐藏的比较规则，使你能够正确预测任意两个字符串的先后关系。

你可以反复提出比较查询：询问集合 S 中两个不同字符串的先后关系。

**比较查询格式**（询问字符串 x 和 y 的先后关系）：
<query_compare>x,y</query_compare>

例如：
<query_compare>AAB,CDC</query_compare>

系统会回答"x在前"或"y在前"。

注意：
- x 和 y 必须是 S 中的有效字符串且互不相同
- 无效请求会返回错误提示
- 尽可能用最少的查询次数推断出规则

当你认为已经掌握了规则，提交准备就绪信号：
<query_ready></query_ready>

进入评测后：
1. 系统会给出 {test_size} 个测试对，每对包含两个你在探索阶段未直接比较过的字符串
2. 对每一对，系统会显示测试对编号和两个字符串
3. 你需要按顺序回答每一对的先后关系

**回答格式**（回答第 k 对测试，认为字符串 x 在前）：
<answer_test>k:x</answer_test>

例如，对于第 1 对测试 (AAB, CDC)，如果你认为 AAB 在前：
<answer_test>1:AAB</answer_test>

评测规则：
- 必须按测试编号顺序逐一回答（从 1 到 {test_size}）
- 任何一题答错，游戏立即失败
- 全部答对则游戏成功

{string_list}
"""

    game_rule_en = """\
Let's play a "String Ordering Rule Inference" game. Here are the rules:

1. The alphabet contains four characters: A, B, C, D.
2. There is a fixed set S containing {n} distinct strings of length 3 (e.g., AAA, ABC, DCA, etc.).
3. I have secretly established a comparison rule C that provides a unique ordering (no ties) for any two different strings in S.
4. This comparison rule is determined by the following hidden parameters:
   - Character priority: The four characters A, B, C, D have a priority ordering, mapped to values 0, 1, 2, 3
   - Reading direction: left-to-right or right-to-left
   - Aggregation mode: lexicographic or weighted sum mode
     * Lexicographic: Compare position by position in reading direction; at the first differing position, use character priority to decide order
     * Weighted sum mode: Each of the three positions has a weight (1, 2, or 3); calculate the weighted score for each string, smaller score comes first; if scores tie, use lexicographic order to break the tie

Infer the hidden comparison rule through queries so you can correctly predict the ordering of any two strings.

You can repeatedly make comparison queries: ask about the ordering of two different strings in set S.

**Comparison query format** (asking about the order of strings x and y):
<query_compare>x,y</query_compare>

For example:
<query_compare>AAB,CDC</query_compare>

The system will answer "x comes first" or "y comes first".

Notes:
- x and y must be valid strings in S and must be different
- Invalid requests will return error messages
- Try to infer the rule with as few queries as possible

When you believe you have mastered the rule, submit a ready signal:
<query_ready></query_ready>

After entering evaluation:
1. The system will present {test_size} test pairs, each containing two strings you have not directly compared in the exploration phase
2. For each pair, the system will show the test number and the two strings
3. You need to answer the ordering for each pair in sequence

**Answer format** (answering test pair k, believing string x comes first):
<answer_test>k:x</answer_test>

For example, for test pair 1 (AAB, CDC), if you believe AAB comes first:
<answer_test>1:AAB</answer_test>

Evaluation rules:
- You must answer in order by test number (from 1 to {test_size})
- Any incorrect answer causes immediate game failure
- Answering all correctly results in game success

{string_list}
"""

    contextualized_rule_zh_1 = """\
这是交通调度“路线规划优先级测试”系统。规则如下：

1. 交通网包含四种基础道路类型：A（主干道）、B（次干道）、C（辅路）、D（小巷）。
2. 存在一个固定集合 S，包含 {n} 个由 3 段道路组成的“通勤路线”（例如：AAA、ABC、DCA 等），所有路线互不相同。
3. 交通控制中心秘密设定了一套调度比较规则 C，能对 S 中任意两条不同路线给出唯一的通行优先级先后关系（无并列）。
4. 这个比较规则由以下隐藏参数决定：
   - 道路优先级：四种道路 A、B、C、D 有一个拥堵评估优先级，映射到数值 0、1、2、3
   - 评估方向：沿途正向评估（从左到右） 或 逆向回溯评估（从右到左）
   - 聚合模式：瓶颈比对（字典序） 或 综合拥堵分数（加权和模式）
     * 瓶颈比对：按评估方向逐段比对，首个不同路段用道路优先级决定先后
     * 综合拥堵分数：三段路各有通行权重（1、2 或 3），计算每条路线的加权分数，分数小的优先通行；若分数相同则用瓶颈比对打破平手

通过查询推断出这个隐藏的调度规则，使你能够正确预测任意两条路线的优先先后关系。

你可以反复提出比较查询：询问集合 S 中两条不同路线的先后关系。

**比较查询格式**（询问路线 x 和 y 的先后关系）：
<query_compare>x,y</query_compare>

例如：
<query_compare>AAB,CDC</query_compare>

系统会回答"x在前"或"y在前"（代表优先级高低）。

注意：
- x 和 y 必须是 S 中的有效路线且互不相同
- 无效请求会返回错误提示
- 尽可能用最少的查询次数推断出规则

当你认为已经掌握了规则，提交准备就绪信号：
<query_ready></query_ready>

进入评测后：
1. 系统会给出 {test_size} 个测试对，每对包含两个你在探索阶段未直接比较过的路线
2. 对每一对，系统会显示测试对编号和两条路线
3. 你需要按顺序回答每一对的先后关系

**回答格式**（回答第 k 对测试，认为路线 x 在前）：
<answer_test>k:x</answer_test>

例如，对于第 1 对测试 (AAB, CDC)，如果你认为 AAB 优先级在前：
<answer_test>1:AAB</answer_test>

评测规则：
- 必须按测试编号顺序逐一回答（从 1 到 {test_size}）
- 任何一题答错，测试立即失败
- 全部答对则测试成功

{string_list}
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Traffic Dispatch "Route Planning Priority Test" system. Here are the rules:

1. The traffic network contains four basic road types: A (Arterial), B (Collector), C (Local), D (Alley).
2. There is a fixed set S containing {n} distinct "commute routes" composed of 3 road segments (e.g., AAA, ABC, DCA, etc.).
3. The Traffic Control Center has secretly established a dispatch comparison rule C that provides a unique priority ordering (no ties) for any two different routes in S.
4. This comparison rule is determined by the following hidden parameters:
   - Road priority: The four road types A, B, C, D have a congestion evaluation priority ordering, mapped to values 0, 1, 2, 3
   - Evaluation direction: Forward along the route (left-to-right) or backward tracing (right-to-left)
   - Aggregation mode: Bottleneck comparison (lexicographic) or Comprehensive congestion score (weighted sum mode)
     * Bottleneck comparison: Compare segment by segment in the evaluation direction; at the first differing segment, use road priority to decide order
     * Comprehensive congestion score: Each of the three segments has a traffic weight (1, 2, or 3); calculate the weighted score for each route, smaller score comes first; if scores tie, use bottleneck comparison to break the tie

Infer the hidden dispatch rule through queries so you can correctly predict the priority ordering of any two routes.

You can repeatedly make comparison queries: ask about the ordering of two different routes in set S.

**Comparison query format** (asking about the order of routes x and y):
<query_compare>x,y</query_compare>

For example:
<query_compare>AAB,CDC</query_compare>

The system will answer "x comes first" or "y comes first" (indicating higher priority).

Notes:
- x and y must be valid routes in S and must be different
- Invalid requests will return error messages
- Try to infer the rule with as few queries as possible

When you believe you have mastered the rule, submit a ready signal:
<query_ready></query_ready>

After entering evaluation:
1. The system will present {test_size} test pairs, each containing two routes you have not directly compared in the exploration phase
2. For each pair, the system will show the test number and the two routes
3. You need to answer the ordering for each pair in sequence

**Answer format** (answering test pair k, believing route x comes first):
<answer_test>k:x</answer_test>

For example, for test pair 1 (AAB, CDC), if you believe AAB comes first:
<answer_test>1:AAB</answer_test>

Evaluation rules:
- You must answer in order by test number (from 1 to {test_size})
- Any incorrect answer causes immediate test failure
- Answering all correctly results in test success

{string_list}
"""

    contextualized_rule_zh_2 = """\
这是医疗系统“治疗方案疗效评估”系统。规则如下：

1. 处方库包含四种基础药物成分：A、B、C、D。
2. 存在一个固定集合 S，包含 {n} 个由 3 个用药周期组成的“复合处方”（例如：AAA、ABC、DCA 等），所有处方互不相同。
3. 医疗AI系统秘密设定了一套疗效比较规则 C，能对 S 中任意两个不同处方给出唯一的优先级先后关系（无并列）。
4. 这个比较规则由以下隐藏参数决定：
   - 药效优先级：四种药物 A、B、C、D 有一个起效优先级，映射到数值 0、1、2、3
   - 观察方向：初期到后期正向观察（从左到右） 或 逆向回溯观察（从右到左）
   - 聚合模式：关键期优先比对（字典序） 或 综合毒副作用得分（加权和模式）
     * 关键期优先比对：按观察方向逐周期比对，首个不同周期的药物用药效优先级决定先后
     * 综合毒副作用得分：三个周期各有生理权重（1、2 或 3），计算每个处方的加权分数，分数小的优先推荐；若分数相同则用关键期优先比对打破平手

通过查询推断出这个隐藏的疗效评估规则，使你能够正确预测任意两个处方的优先先后关系。

你可以反复提出比较查询：询问集合 S 中两个不同处方的先后关系。

**比较查询格式**（询问处方 x 和 y 的先后关系）：
<query_compare>x,y</query_compare>

例如：
<query_compare>AAB,CDC</query_compare>

系统会回答"x在前"或"y在前"（代表疗效或安全性优先级更高）。

注意：
- x 和 y 必须是 S 中的有效处方且互不相同
- 无效请求会返回错误提示
- 尽可能用最少的查询次数推断出规则

当你认为已经掌握了规则，提交准备就绪信号：
<query_ready></query_ready>

进入评测后：
1. 系统会给出 {test_size} 个测试对，每对包含两个你在探索阶段未直接比较过的处方
2. 对每一对，系统会显示测试对编号和两个处方
3. 你需要按顺序回答每一对的先后关系

**回答格式**（回答第 k 对测试，认为处方 x 在前）：
<answer_test>k:x</answer_test>

例如，对于第 1 对测试 (AAB, CDC)，如果你认为 AAB 在前：
<answer_test>1:AAB</answer_test>

评测规则：
- 必须按测试编号顺序逐一回答（从 1 到 {test_size}）
- 任何一题答错，测试立即失败
- 全部答对则测试成功

{string_list}
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Medical System "Treatment Plan Efficacy Evaluation" system. Here are the rules:

1. The prescription database contains four basic drug molecules: A, B, C, D.
2. There is a fixed set S containing {n} distinct "compound prescriptions" composed of 3 medication cycles (e.g., AAA, ABC, DCA, etc.).
3. The Medical AI system has secretly established an efficacy comparison rule C that provides a unique priority ordering (no ties) for any two different prescriptions in S.
4. This comparison rule is determined by the following hidden parameters:
   - Efficacy priority: The four drugs A, B, C, D have an onset priority, mapped to values 0, 1, 2, 3
   - Observation direction: Initial to late stage (left-to-right) or retrospective observation (right-to-left)
   - Aggregation mode: Critical stage comparison (lexicographic) or Comprehensive toxicity score (weighted sum mode)
     * Critical stage comparison: Compare cycle by cycle in the observation direction; at the first differing cycle, use efficacy priority to decide order
     * Comprehensive toxicity score: Each of the three cycles has a physiological weight (1, 2, or 3); calculate the weighted score for each prescription, smaller score comes first; if scores tie, use critical stage comparison to break the tie

Infer the hidden efficacy evaluation rule through queries so you can correctly predict the priority ordering of any two prescriptions.

You can repeatedly make comparison queries: ask about the ordering of two different prescriptions in set S.

**Comparison query format** (asking about the order of prescriptions x and y):
<query_compare>x,y</query_compare>

For example:
<query_compare>AAB,CDC</query_compare>

The system will answer "x comes first" or "y comes first" (indicating higher efficacy or safety priority).

Notes:
- x and y must be valid prescriptions in S and must be different
- Invalid requests will return error messages
- Try to infer the rule with as few queries as possible

When you believe you have mastered the rule, submit a ready signal:
<query_ready></query_ready>

After entering evaluation:
1. The system will present {test_size} test pairs, each containing two prescriptions you have not directly compared in the exploration phase
2. For each pair, the system will show the test number and the two prescriptions
3. You need to answer the ordering for each pair in sequence

**Answer format** (answering test pair k, believing prescription x comes first):
<answer_test>k:x</answer_test>

For example, for test pair 1 (AAB, CDC), if you believe AAB comes first:
<answer_test>1:AAB</answer_test>

Evaluation rules:
- You must answer in order by test number (from 1 to {test_size})
- Any incorrect answer causes immediate test failure
- Answering all correctly results in test success

{string_list}
"""

    contextualized_rule_zh_3 = """\
这是教务系统“学生综合素养评级”系统。规则如下：

1. 考核指标包含四个评级：A（优秀）、B（良好）、C（中等）、D（及格）。
2. 存在一个固定集合 S，包含 {n} 个由 3 个学期表现组成的“成绩记录”（例如：AAA、ABC、DCA 等），所有记录互不相同。
3. 教务系统秘密设定了一套综合比较规则 C，能对 S 中任意两条不同成绩记录给出唯一的排位先后关系（无并列）。
4. 这个比较规则由以下隐藏参数决定：
   - 评级含金量：四个评级 A、B、C、D 有一个含金量优先级，映射到数值 0、1、2、3
   - 关注顺序：顺着学期看（从左到右） 或 看最近表现回溯（从右到左）
   - 聚合模式：偏科筛选（字典序） 或 综合绩点分（加权和模式）
     * 偏科筛选：按关注顺序逐学期比对，首个不同学期用评级含金量决定先后
     * 综合绩点分：三个学期各有学分权重（1、2 或 3），计算每条记录的加权分数，分数小的排名在前；若分数相同则用偏科筛选打破平手

通过查询推断出这个隐藏的综合排位规则，使你能够正确预测任意两条成绩记录的排位先后关系。

你可以反复提出比较查询：询问集合 S 中两条不同成绩记录的先后关系。

**比较查询格式**（询问记录 x 和 y 的先后关系）：
<query_compare>x,y</query_compare>

例如：
<query_compare>AAB,CDC</query_compare>

系统会回答"x在前"或"y在前"。

注意：
- x 和 y 必须是 S 中的有效记录且互不相同
- 无效请求会返回错误提示
- 尽可能用最少的查询次数推断出规则

当你认为已经掌握了规则，提交准备就绪信号：
<query_ready></query_ready>

进入评测后：
1. 系统会给出 {test_size} 个测试对，每对包含两个你在探索阶段未直接比较过的成绩记录
2. 对每一对，系统会显示测试对编号和两条成绩记录
3. 你需要按顺序回答每一对的先后关系

**回答格式**（回答第 k 对测试，认为记录 x 在前）：
<answer_test>k:x</answer_test>

例如，对于第 1 对测试 (AAB, CDC)，如果你认为 AAB 在前：
<answer_test>1:AAB</answer_test>

评测规则：
- 必须按测试编号顺序逐一回答（从 1 到 {test_size}）
- 任何一题答错，测试立即失败
- 全部答对则测试成功

{string_list}
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Educational Administration "Student Comprehensive Literacy Rating" system. Here are the rules:

1. The assessment indicators contain four grading levels: A (Excellent), B (Good), C (Average), D (Pass).
2. There is a fixed set S containing {n} distinct "academic records" composed of 3 semesters of performance (e.g., AAA, ABC, DCA, etc.).
3. The administration system has secretly established a comprehensive comparison rule C that provides a unique ranking ordering (no ties) for any two different academic records in S.
4. This comparison rule is determined by the following hidden parameters:
   - Grade value priority: The four grades A, B, C, D have a value priority ordering, mapped to values 0, 1, 2, 3
   - Focus sequence: Sequential by semester (left-to-right) or backtracking from recent performance (right-to-left)
   - Aggregation mode: Subject imbalance screening (lexicographic) or Comprehensive GPA score (weighted sum mode)
     * Subject imbalance screening: Compare semester by semester in the focus sequence; at the first differing semester, use grade priority to decide order
     * Comprehensive GPA score: Each of the three semesters has a credit weight (1, 2, or 3); calculate the weighted score for each record, smaller score comes first; if scores tie, use subject imbalance screening to break the tie

Infer the hidden ranking rule through queries so you can correctly predict the ranking order of any two academic records.

You can repeatedly make comparison queries: ask about the ordering of two different academic records in set S.

**Comparison query format** (asking about the order of records x and y):
<query_compare>x,y</query_compare>

For example:
<query_compare>AAB,CDC</query_compare>

The system will answer "x comes first" or "y comes first".

Notes:
- x and y must be valid records in S and must be different
- Invalid requests will return error messages
- Try to infer the rule with as few queries as possible

When you believe you have mastered the rule, submit a ready signal:
<query_ready></query_ready>

After entering evaluation:
1. The system will present {test_size} test pairs, each containing two academic records you have not directly compared in the exploration phase
2. For each pair, the system will show the test number and the two records
3. You need to answer the ordering for each pair in sequence

**Answer format** (answering test pair k, believing record x comes first):
<answer_test>k:x</answer_test>

For example, for test pair 1 (AAB, CDC), if you believe AAB comes first:
<answer_test>1:AAB</answer_test>

Evaluation rules:
- You must answer in order by test number (from 1 to {test_size})
- Any incorrect answer causes immediate test failure
- Answering all correctly results in test success

{string_list}
"""

    contextualized_rule_zh_4 = """\
这是工业制造“产品质量检验批次排序”系统。规则如下：

1. 检测标准包含四个质量等级：A（优品）、B（良品）、C（次品）、D（废品）。
2. 存在一个固定集合 S，包含 {n} 个由 3 个检测点构成的“质检流水号”（例如：AAA、ABC、DCA 等），所有流水号互不相同。
3. 质检系统秘密设定了一套出厂优先级规则 C，能对 S 中任意两个不同流水号给出唯一的先后关系（无并列）。
4. 这个比较规则由以下隐藏参数决定：
   - 质量权重：四个等级 A、B、C、D 有一个严重度优先级，映射到数值 0、1、2、3
   - 检测顺序：正向流水线检测（从左到右） 或 逆向复核确认（从右到左）
   - 聚合模式：首发缺陷淘汰制（字典序） 或 整体不良率得分（加权和模式）
     * 首发缺陷淘汰制：按检测顺序逐节点比对，首个不同节点用严重度优先级决定先后
     * 整体不良率得分：三个节点各有风险权重（1、2 或 3），计算每个流水号的加权分数，分数小的优先出厂；若分数相同则用首发缺陷淘汰制打破平手

通过查询推断出这个隐藏的出厂调度规则，使你能够正确预测任意两个流水号的优先先后关系。

你可以反复提出比较查询：询问集合 S 中两个不同流水号的先后关系。

**比较查询格式**（询问流水号 x 和 y 的先后关系）：
<query_compare>x,y</query_compare>

例如：
<query_compare>AAB,CDC</query_compare>

系统会回答"x在前"或"y在前"（代表出厂或处理优先级更高）。

注意：
- x 和 y 必须是 S 中的有效流水号且互不相同
- 无效请求会返回错误提示
- 尽可能用最少的查询次数推断出规则

当你认为已经掌握了规则，提交准备就绪信号：
<query_ready></query_ready>

进入评测后：
1. 系统会给出 {test_size} 个测试对，每对包含两个你在探索阶段未直接比较过的流水号
2. 对每一对，系统会显示测试对编号和两个流水号
3. 你需要按顺序回答每一对的先后关系

**回答格式**（回答第 k 对测试，认为流水号 x 在前）：
<answer_test>k:x</answer_test>

例如，对于第 1 对测试 (AAB, CDC), 如果你认为 AAB 在前：
<answer_test>1:AAB</answer_test>

评测规则：
- 必须按测试编号顺序逐一回答（从 1 到 {test_size}）
- 任何一题答错，测试立即失败
- 全部答对则测试成功

{string_list}
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Industrial Manufacturing "Product Quality Inspection Batch Sorting" system. Here are the rules:

1. The inspection standards contain four quality levels: A (Premium), B (Good), C (Defective), D (Scrap).
2. There is a fixed set S containing {n} distinct "inspection serial numbers" composed of 3 inspection points (e.g., AAA, ABC, DCA, etc.).
3. The quality inspection system has secretly established a factory priority rule C that provides a unique ordering (no ties) for any two different serial numbers in S.
4. This comparison rule is determined by the following hidden parameters:
   - Quality weight priority: The four levels A, B, C, D have a severity priority ordering, mapped to values 0, 1, 2, 3
   - Inspection sequence: Forward pipeline inspection (left-to-right) or reverse verification (right-to-left)
   - Aggregation mode: First defect elimination (lexicographic) or Overall defect rate score (weighted sum mode)
     * First defect elimination: Compare point by point in the inspection sequence; at the first differing point, use severity priority to decide order
     * Overall defect rate score: Each of the three points has a risk weight (1, 2, or 3); calculate the weighted score for each serial number, smaller score comes first; if scores tie, use first defect elimination to break the tie

Infer the hidden factory priority rule through queries so you can correctly predict the ordering of any two serial numbers.

You can repeatedly make comparison queries: ask about the ordering of two different serial numbers in set S.

**Comparison query format** (asking about the order of serial numbers x and y):
<query_compare>x,y</query_compare>

For example:
<query_compare>AAB,CDC</query_compare>

The system will answer "x comes first" or "y comes first" (indicating higher factory processing priority).

Notes:
- x and y must be valid serial numbers in S and must be different
- Invalid requests will return error messages
- Try to infer the rule with as few queries as possible

When you believe you have mastered the rule, submit a ready signal:
<query_ready></query_ready>

After entering evaluation:
1. The system will present {test_size} test pairs, each containing two serial numbers you have not directly compared in the exploration phase
2. For each pair, the system will show the test number and the two serial numbers
3. You need to answer the ordering for each pair in sequence

**Answer format** (answering test pair k, believing serial number x comes first):
<answer_test>k:x</answer_test>

For example, for test pair 1 (AAB, CDC), if you believe AAB comes first:
<answer_test>1:AAB</answer_test>

Evaluation rules:
- You must answer in order by test number (from 1 to {test_size})
- Any incorrect answer causes immediate test failure
- Answering all correctly results in test success

{string_list}
"""

    contextualized_rule_zh_5 = """\
这是司法审判“案件卷宗审查优先级”系统。规则如下：

1. 证据库包含四种效力级别：A（直接证据）、B（间接证据）、C（辅助证据）、D（传闻证据）。
2. 存在一个固定集合 S，包含 {n} 个由 3 轮庭审取证组成的“证据链代码”（例如：AAA、ABC、DCA 等），所有代码互不相同。
3. 法院排期系统秘密设定了一套审查规则 C，能对 S 中任意两条不同证据链给出唯一的排期先后关系（无并列）。
4. 这个比较规则由以下隐藏参数决定：
   - 效力优先级：四种证据级别 A、B、C、D 有一个采信优先级，映射到数值 0、1、2、3
   - 审查视角：顺向取证推演（从左到右） 或 逆向回溯推演（从右到左）
   - 聚合模式：核心证据一票否决制（字典序） 或 自由心证综合评分（加权和模式）
     * 核心证据一票否决制：按审查视角逐轮比对，首轮不同的证据级别用采信优先级决定先后
     * 自由心证综合评分：三轮庭审各有法理权重（1、2 或 3），计算每条证据链的加权分数，分数小的优先排期审查；若分数相同则用核心证据一票否决制打破平手

通过查询推断出这个隐藏的排期规则，使你能够正确预测任意两条证据链的排期先后关系。

你可以反复提出比较查询：询问集合 S 中两条不同证据链代码的先后关系。

**比较查询格式**（询问证据链 x 和 y 的先后关系）：
<query_compare>x,y</query_compare>

例如：
<query_compare>AAB,CDC</query_compare>

系统会回答"x在前"或"y在前"（代表排期顺位靠前）。

注意：
- x 和 y 必须是 S 中的有效证据链且互不相同
- 无效请求会返回错误提示
- 尽可能用最少的查询次数推断出规则

当你认为已经掌握了规则，提交准备就绪信号：
<query_ready></query_ready>

进入评测后：
1. 系统会给出 {test_size} 个测试对，每对包含两个你在探索阶段未直接比较过的证据链代码
2. 对每一对，系统会显示测试对编号和两条证据链代码
3. 你需要按顺序回答每一对的先后关系

**回答格式**（回答第 k 对测试，认为证据链 x 在前）：
<answer_test>k:x</answer_test>

例如，对于第 1 对测试 (AAB, CDC)，如果你认为 AAB 在前：
<answer_test>1:AAB</answer_test>

评测规则：
- 必须按测试编号顺序逐一回答（从 1 到 {test_size}）
- 任何一题答错，测试立即失败
- 全部答对则测试成功

{string_list}
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Judicial System "Case File Review Priority" system. Here are the rules:

1. The evidence database contains four validity levels: A (Direct Evidence), B (Circumstantial Evidence), C (Corroborating Evidence), D (Hearsay).
2. There is a fixed set S containing {n} distinct "evidence chain codes" composed of 3 rounds of court hearings (e.g., AAA, ABC, DCA, etc.).
3. The court scheduling system has secretly established a review rule C that provides a unique scheduling ordering (no ties) for any two different evidence chains in S.
4. This comparison rule is determined by the following hidden parameters:
   - Validity priority: The four evidence levels A, B, C, D have an admissibility priority ordering, mapped to values 0, 1, 2, 3
   - Review perspective: Forward evidential deduction (left-to-right) or backward backtracking (right-to-left)
   - Aggregation mode: Core evidence veto (lexicographic) or Free evaluation of evidence score (weighted sum mode)
     * Core evidence veto: Compare round by round in the review perspective; at the first differing round, use validity priority to decide order
     * Free evaluation of evidence score: Each of the three rounds has a jurisprudential weight (1, 2, or 3); calculate the weighted score for each evidence chain, smaller score comes first; if scores tie, use core evidence veto to break the tie

Infer the hidden scheduling rule through queries so you can correctly predict the priority ordering of any two evidence chains.

You can repeatedly make comparison queries: ask about the ordering of two different evidence chains in set S.

**Comparison query format** (asking about the order of evidence chains x and y):
<query_compare>x,y</query_compare>

For example:
<query_compare>AAB,CDC</query_compare>

The system will answer "x comes first" or "y comes first" (indicating higher scheduling priority).

Notes:
- x and y must be valid evidence chains in S and must be different
- Invalid requests will return error messages
- Try to infer the rule with as few queries as possible

When you believe you have mastered the rule, submit a ready signal:
<query_ready></query_ready>

After entering evaluation:
1. The system will present {test_size} test pairs, each containing two evidence chains you have not directly compared in the exploration phase
2. For each pair, the system will show the test number and the two evidence chains
3. You need to answer the ordering for each pair in sequence

**Answer format** (answering test pair k, believing evidence chain x comes first):
<answer_test>k:x</answer_test>

For example, for test pair 1 (AAB, CDC), if you believe AAB comes first:
<answer_test>1:AAB</answer_test>

Evaluation rules:
- You must answer in order by test number (from 1 to {test_size})
- Any incorrect answer causes immediate test failure
- Answering all correctly results in test success

{string_list}
"""

    tags = ["query_compare", "query_ready", "answer_test"]
    
    reasoning_type = "归纳推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 12,
                "strings": ["AAA", "AAB", "ABA", "ABB", "BAA", "BAB", "BBA", "BBB", "CAA", "CAB", "CBA", "DAA"],
                "priority": {"A": 0, "B": 1, "C": 2, "D": 3},
                "direction": "left_to_right",
                "mode": "lexicographic",
                "weights": None,
                "test_size": 5
            },
            2: {
                "n": 15,
                "strings": ["AAA", "AAB", "ABA", "ABB", "BAA", "BAB", "BBA", "BBB", "CAA", "CAB", "CBA", "CBB", "DAA", "DAB", "DBA"],
                "priority": {"A": 0, "B": 1, "C": 2, "D": 3},
                "direction": "right_to_left",
                "mode": "lexicographic",
                "weights": None,
                "test_size": 6
            },
            3: {
                "n": 18,
                "strings": ["AAA", "AAB", "AAC", "ABA", "ABB", "ABC", "BAA", "BAB", "BAC", "BBA", "BBB", "BBC", "CAA", "CAB", "CBA", "CBB", "DAA", "DBA"],
                "priority": {"A": 0, "B": 1, "C": 2, "D": 3},
                "direction": "left_to_right",
                "mode": "weighted",
                "weights": [1, 1, 1],
                "test_size": 7
            },
            4: {
                "n": 20,
                "strings": ["AAA", "AAB", "AAC", "ABA", "ABB", "ABC", "ACA", "BAA", "BAB", "BAC", "BBA", "BBB", "BBC", "BCA", "CAA", "CAB", "CBA", "CBB", "DAA", "DBA"],
                "priority": {"A": 0, "B": 2, "C": 1, "D": 3},
                "direction": "left_to_right",
                "mode": "weighted",
                "weights": [3, 2, 1],
                "test_size": 8
            },
            5: {
                "n": 24,
                "strings": ["AAA", "AAB", "AAC", "AAD", "ABA", "ABB", "ABC", "ACA", "ACB", "BAA", "BAB", "BAC", "BBA", "BBB", "BBC", "BCA", "CAA", "CAB", "CBA", "CBB", "DAA", "DAB", "DBA", "DBB"],
                "priority": {"A": 3, "B": 1, "C": 2, "D": 0},
                "direction": "right_to_left",
                "mode": "weighted",
                "weights": [2, 3, 1],
                "test_size": 10
            }
        },
        "en": {
            1: {
                "n": 12,
                "strings": ["AAA", "AAB", "ABA", "ABB", "BAA", "BAB", "BBA", "BBB", "CAA", "CAB", "CBA", "DAA"],
                "priority": {"A": 0, "B": 1, "C": 2, "D": 3},
                "direction": "left_to_right",
                "mode": "lexicographic",
                "weights": None,
                "test_size": 5
            },
            2: {
                "n": 15,
                "strings": ["AAA", "AAB", "ABA", "ABB", "BAA", "BAB", "BBA", "BBB", "CAA", "CAB", "CBA", "CBB", "DAA", "DAB", "DBA"],
                "priority": {"A": 0, "B": 1, "C": 2, "D": 3},
                "direction": "right_to_left",
                "mode": "lexicographic",
                "weights": None,
                "test_size": 6
            },
            3: {
                "n": 18,
                "strings": ["AAA", "AAB", "AAC", "ABA", "ABB", "ABC", "BAA", "BAB", "BAC", "BBA", "BBB", "BBC", "CAA", "CAB", "CBA", "CBB", "DAA", "DBA"],
                "priority": {"A": 0, "B": 1, "C": 2, "D": 3},
                "direction": "left_to_right",
                "mode": "weighted",
                "weights": [1, 1, 1],
                "test_size": 7
            },
            4: {
                "n": 20,
                "strings": ["AAA", "AAB", "AAC", "ABA", "ABB", "ABC", "ACA", "BAA", "BAB", "BAC", "BBA", "BBB", "BBC", "BCA", "CAA", "CAB", "CBA", "CBB", "DAA", "DBA"],
                "priority": {"A": 0, "B": 2, "C": 1, "D": 3},
                "direction": "left_to_right",
                "mode": "weighted",
                "weights": [3, 2, 1],
                "test_size": 8
            },
            5: {
                "n": 24,
                "strings": ["AAA", "AAB", "AAC", "AAD", "ABA", "ABB", "ABC", "ACA", "ACB", "BAA", "BAB", "BAC", "BBA", "BBB", "BBC", "BCA", "CAA", "CAB", "CBA", "CBB", "DAA", "DAB", "DBA", "DBB"],
                "priority": {"A": 3, "B": 1, "C": 2, "D": 0},
                "direction": "right_to_left",
                "mode": "weighted",
                "weights": [2, 3, 1],
                "test_size": 10
            }
        }
    }

    def __init__(self, config):
        self.in_evaluation = False
        self.test_pairs = []
        self.current_test_index = 0
        self.queried_pairs = set()
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
        self._game_info["test_size"] = cfg["test_size"]
        self.strings = cfg["strings"]
        self._game_info["string_list"] = ", ".join(self.strings)
        
        self.priority = cfg["priority"]
        self.direction = cfg["direction"]
        self.mode = cfg["mode"]
        self.weights = cfg["weights"]
        self.test_size = cfg["test_size"]
        
        self._prepare_test_pairs()

    def _prepare_test_pairs(self):
        all_pairs = []
        for i in range(len(self.strings)):
            for j in range(i + 1, len(self.strings)):
                all_pairs.append((self.strings[i], self.strings[j]))
        
        rng = random.Random(42)
        rng.shuffle(all_pairs)
        self.candidate_test_pairs = all_pairs[:self.test_size * 3]

    def _compare(self, s1, s2):
        if self.direction == "left_to_right":
            chars1 = list(s1)
            chars2 = list(s2)
        else:
            chars1 = list(reversed(s1))
            chars2 = list(reversed(s2))
        
        if self.mode == "lexicographic":
            for c1, c2 in zip(chars1, chars2):
                if self.priority[c1] < self.priority[c2]:
                    return True
                elif self.priority[c1] > self.priority[c2]:
                    return False
            return False
        
        else:
            score1 = sum(w * self.priority[c] for w, c in zip(self.weights, chars1))
            score2 = sum(w * self.priority[c] for w, c in zip(self.weights, chars2))
            
            if score1 < score2:
                return True
            elif score1 > score2:
                return False
            else:
                for c1, c2 in zip(chars1, chars2):
                    if self.priority[c1] < self.priority[c2]:
                        return True
                    elif self.priority[c1] > self.priority[c2]:
                        return False
                return False

    def evaluate(self, parsed_info):
        return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            invalid_format = "无效：格式错误"
            invalid_string = "无效：字符串不在集合中"
            invalid_same = "无效：两个字符串必须不同"
            invalid_phase = "无效：已进入评测阶段，不能再进行比较查询"
            comes_first = "{}在前"
            ready_response = "准备就绪。现在开始评测，共 {} 题。\n\n第 {} 题：请比较 {} 和 {}，回答格式 <answer_test>{}:字符串</answer_test>"
            invalid_test_format = "无效：答案格式错误，应为 <answer_test>编号:字符串</answer_test>"
            invalid_test_number = "无效：当前应回答第 {} 题"
            invalid_test_string = "无效：答案必须是测试对中的一个字符串"
            correct_continue = "正确！\n\n第 {} 题：请比较 {} 和 {}，回答格式 <answer_test>{}:字符串</answer_test>"
            incorrect = "错误！正确答案是 {}。"
        else:
            invalid_format = "Invalid: format error"
            invalid_string = "Invalid: string not in set"
            invalid_same = "Invalid: two strings must be different"
            invalid_phase = "Invalid: already in evaluation phase, cannot make comparison queries"
            comes_first = "{} comes first"
            ready_response = "Ready. Evaluation begins, {} questions in total.\n\nQuestion {}: Please compare {} and {}, answer format <answer_test>{}:string</answer_test>"
            invalid_test_format = "Invalid: answer format error, should be <answer_test>number:string</answer_test>"
            invalid_test_number = "Invalid: should answer question {} now"
            invalid_test_string = "Invalid: answer must be one of the strings in the test pair"
            correct_continue = "Correct!\n\nQuestion {}: Please compare {} and {}, answer format <answer_test>{}:string</answer_test>"
            incorrect = "Incorrect! The correct answer is {}."

        if "query_compare" in parsed_info:
            if self.in_evaluation:
                return invalid_phase
            
            try:
                raw = parsed_info["query_compare"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return invalid_format
                
                s1, s2 = parts
                if s1 not in self.strings or s2 not in self.strings:
                    return invalid_string
                if s1 == s2:
                    return invalid_same
                
                pair = tuple(sorted([s1, s2]))
                self.queried_pairs.add(pair)
                
                if self._compare(s1, s2):
                    return comes_first.format(s1)
                else:
                    return comes_first.format(s2)
            except:
                return invalid_format

        elif "query_ready" in parsed_info:
            if self.in_evaluation:
                return "Invalid: already in evaluation phase" if self.config.language == "en" else "无效：已经在评测阶段"
            
            self.in_evaluation = True
            
            self.test_pairs = []
            for pair in self.candidate_test_pairs:
                sorted_pair = tuple(sorted([pair[0], pair[1]]))
                if sorted_pair not in self.queried_pairs:
                    self.test_pairs.append(pair)
                    if len(self.test_pairs) >= self.test_size:
                        break
            
            if len(self.test_pairs) < self.test_size:
                for i in range(len(self.strings)):
                    for j in range(i + 1, len(self.strings)):
                        pair = (self.strings[i], self.strings[j])
                        sorted_pair = tuple(sorted([pair[0], pair[1]]))
                        if sorted_pair not in self.queried_pairs and pair not in self.test_pairs:
                            self.test_pairs.append(pair)
                            if len(self.test_pairs) >= self.test_size:
                                break
                    if len(self.test_pairs) >= self.test_size:
                        break
            
            self.current_test_index = 1
            s1, s2 = self.test_pairs[0]
            return ready_response.format(self.test_size, 1, s1, s2, 1)

        elif "answer_test" in parsed_info:
            if not self.in_evaluation:
                return "Invalid: not in evaluation phase yet" if self.config.language == "en" else "无效：尚未进入评测阶段"
            
            try:
                raw = parsed_info["answer_test"]
                if ":" not in raw:
                    return invalid_test_format
                
                num_str, answer_str = raw.split(":", 1)
                test_num = int(num_str.strip())
                answer = answer_str.strip()
                
                if test_num != self.current_test_index:
                    return invalid_test_number.format(self.current_test_index)
                
                s1, s2 = self.test_pairs[test_num - 1]
                if answer not in [s1, s2]:
                    return invalid_test_string
                
                correct_first = s1 if self._compare(s1, s2) else s2
                
                if answer != correct_first:
                    self.state.set_state("failed", "incorrect answer in evaluation")
                    return incorrect.format(correct_first)
                
                if self.current_test_index < self.test_size:
                    self.current_test_index += 1
                    s1, s2 = self.test_pairs[self.current_test_index - 1]
                    return correct_continue.format(self.current_test_index, s1, s2, self.current_test_index)
                else:
                    self.state.set_state("success", "all tests passed")
                    return "Correct! All tests passed!" if self.config.language == "en" else "正确！全部通过！"
                
            except:
                return invalid_test_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        elif self.config.language == "en":
            if "yes" in correct.lower():
                return correct.replace("Yes", "No").replace("yes", "no").replace("YES", "NO")
            elif "no" in correct.lower():
                return correct.replace("No", "Yes").replace("no", "yes").replace("NO", "YES")
        
        return correct + "_WRONG"

    def get_all_possible_queries(self):
        results = []
        
        if self.config.language == "zh":
            comes_first = "{}在前"
        else:
            comes_first = "{} comes first"

        for i in range(len(self.strings)):
            for j in range(i + 1, len(self.strings)):
                s1, s2 = self.strings[i], self.strings[j]
                
                query_content = f"<query_compare>{s1},{s2}</query_compare>"
                
                if self._compare(s1, s2):
                    ans = comes_first.format(s1)
                else:
                    ans = comes_first.format(s2)
                
                results.append({
                    "query": query_content,
                    "answer": ans
                })
        
        return results