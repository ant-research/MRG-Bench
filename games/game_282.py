import random
import re
from .base import Game

class HiddenStatisticsRuleGame(Game):

    game_rule_zh = """\
我们来玩一个"隐藏统计规则"的推理游戏，规则如下：

游戏设定了一个有限集合 U，包含 N 个元素（N 未知）。每个元素具有两种二元属性：
- 属性 A，取值为 A1 或 A2
- 属性 B，取值为 B1 或 B2

已知四种组合（A1且B1、A1且B2、A2且B1、A2且B2）的元素数量均大于 0。

我已秘密选定了一种"应答方案"，对你的所有查询都将按照同一方案计算。方案共有四种可能（具体定义保密），不同方案会对相同查询给出不同的比例值。

你的目标是通过提问推断出我使用的是哪一种方案，并给出验证。

你可以反复向我提出以下两类问题（每次仅限一个问题）：

1. **数值查询**：指定一个目标条件 X 和一个过滤条件 F。
   - X 可以是：A1、A2、B1、B2、A1且B1、A1且B2、A2且B1、A2且B2
   - F 只能是：A1、A2、B1、B2
   - 我会返回一个比例值（以分数或小数形式）

2. **相等性查询**：指定两个数值查询，询问它们的结果是否相等。
   - 我会返回"是"或"否"

注意：若某查询导致分母为 0（如过滤条件对应的元素数为 0），我会返回"不可用"，该次查询不计入有效次数。

每次只能包含一个查询标签，使用以下 XML 格式：

- 数值查询（例如目标为 A1且B1，过滤为 A1）：
<query_value>X=A1且B1, F=A1</query_value>

- 相等性查询（例如询问两个数值查询是否相等）：
<query_equal>Q1=(X=A1, F=B1), Q2=(X=B1, F=A1)</query_equal>

当你确定方案后，请按以下格式提交：

<answer>方案=A, 验证查询=X=A1, F=B1, 计算式=|A1且B1|/|B1|, 历史值=0.5</answer>

其中：
- **方案**：填写 A、B、C 或 D
- **验证查询**：从你之前的某一条数值查询中选择一条（用 X=..., F=... 表示）
- **计算式**：给出该查询在你判定的方案下的形式化表达式（用集合计数符号表示）
- **历史值**：该查询当时我返回的数值

验证将检查：
1. 方案是否正确
2. 计算式是否符合该方案的定义
3. 根据计算式推导的结果是否与历史值一致
"""

    game_rule_en = """\
Let's play a "Hidden Statistics Rule" deduction game. Here are the rules:

There is a finite set U containing N elements (N is unknown). Each element has two binary attributes:
- Attribute A, valued as A1 or A2
- Attribute B, valued as B1 or B2

It is known that all four combinations (A1 and B1, A1 and B2, A2 and B1, A2 and B2) have positive counts.

I have secretly selected a "response scheme" that will be used consistently for all your queries. There are four possible schemes (definitions kept secret), and different schemes will return different ratio values for the same query.

Your goal is to deduce which scheme I am using through queries, and provide verification.

You can repeatedly ask me the following two types of questions (one per turn):

1. **Value Query**: Specify a target condition X and a filter condition F.
   - X can be: A1, A2, B1, B2, A1 and B1, A1 and B2, A2 and B1, A2 and B2
   - F can only be: A1, A2, B1, B2
   - I will return a ratio value (as a fraction or decimal)

2. **Equality Query**: Specify two value queries and ask if their results are equal.
   - I will return "Yes" or "No"

Note: If a query causes a zero denominator (e.g., the filter condition has no elements), I will return "Unavailable", and this query will not count toward the limit.

Each turn must contain only one query tag, using the following XML format:

- Value Query (e.g., target is A1 and B1, filter is A1):
<query_value>X=A1 and B1, F=A1</query_value>

- Equality Query (e.g., asking if two value queries are equal):
<query_equal>Q1=(X=A1, F=B1), Q2=(X=B1, F=A1)</query_equal>

When you determine the scheme, submit in the following format:

<answer>scheme=A, verification_query=X=A1, F=B1, formula=|A1 and B1|/|B1|, historical_value=0.5</answer>

Where:
- **scheme**: Fill in A, B, C, or D
- **verification_query**: Select one of your previous value queries (expressed as X=..., F=...)
- **formula**: Provide the formal expression for this query under your determined scheme (using set cardinality notation)
- **historical_value**: The numerical value I returned for that query

Verification will check:
1. Whether the scheme is correct
2. Whether the formula matches the scheme's definition
3. Whether the result derived from the formula is consistent with the historical value
"""

    contextualized_rule_zh_1 = """\
欢迎接入智慧交通流量监控系统。本系统旨在通过多维数据下钻，分析城市路网中不同车辆的分布特征。

系统当前框定了一个特定时段的车流集合 U，包含 N 辆车（N 未知）。每辆车具有两种二元属性：
- 属性 A（车型），取值为 A1（小型车） 或 A2（大型车）
- 属性 B（动力），取值为 B1（新能源） 或 B2（燃油）

已知四种组合（A1且B1、A1且B2、A2且B1、A2且B2）的车辆数量均大于 0。

系统底层已秘密选定了一种"统计核算方案"，对你的所有查询都将按照同一方案计算占比。方案共有四种可能（具体定义保密），不同方案会对相同查询给出不同的比例值。

你的目标是通过提问推断出系统使用的是哪一种方案，并给出验证。

你可以反复向我提出以下两类问题（每次仅限一个问题）：

1. **数值查询**：指定一个目标条件 X 和一个过滤条件 F。
   - X 可以是：A1、A2、B1、B2、A1且B1、A1且B2、A2且B1、A2且B2
   - F 只能是：A1、A2、B1、B2
   - 我会返回一个比例值（以分数或小数形式）

2. **相等性查询**：指定两个数值查询，询问它们的结果是否相等。
   - 我会返回"是"或"否"

注意：若某查询导致分母为 0（如过滤条件对应的元素数为 0），我会返回"不可用"，该次查询不计入有效次数。

每次只能包含一个查询标签，使用以下 XML 格式：

- 数值查询（例如目标为 A1且B1，过滤为 A1）：
<query_value>X=A1且B1, F=A1</query_value>

- 相等性查询（例如询问两个数值查询是否相等）：
<query_equal>Q1=(X=A1, F=B1), Q2=(X=B1, F=A1)</query_equal>

当你确定方案后，请按以下格式提交：

<answer>方案=A, 验证查询=X=A1, F=B1, 计算式=|A1且B1|/|B1|, 历史值=0.5</answer>

其中：
- **方案**：填写 A、B、C 或 D
- **验证查询**：从你之前的某一条数值查询中选择一条（用 X=..., F=... 表示）
- **计算式**：给出该查询在你判定的方案下的形式化表达式（用集合计数符号表示）
- **历史值**：该查询当时我返回的数值

验证将检查：
1. 方案是否正确
2. 计算式是否符合该方案的定义
3. 根据计算式推导的结果是否与历史值一致
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Smart Traffic Flow Monitoring System. This system is designed to analyze the distribution characteristics of different vehicles in the urban road network through multi-dimensional data drill-down.

The system has configured a finite set U containing N vehicles (N is unknown). Each vehicle has two binary attributes:
- Attribute A (Vehicle Type), valued as A1 (Compact) or A2 (Heavy)
- Attribute B (Power Source), valued as B1 (EV) or B2 (ICE)

It is known that all four combinations (A1 and B1, A1 and B2, A2 and B1, A2 and B2) have positive counts.

The system has secretly selected a "statistical accounting scheme" that will be used consistently for all your queries. There are four possible schemes (definitions kept secret), and different schemes will return different ratio values for the same query.

Your goal is to deduce which scheme the system is using through queries, and provide verification.

You can repeatedly ask me the following two types of questions (one per turn):

1. **Value Query**: Specify a target condition X and a filter condition F.
   - X can be: A1, A2, B1, B2, A1 and B1, A1 and B2, A2 and B1, A2 and B2
   - F can only be: A1, A2, B1, B2
   - I will return a ratio value (as a fraction or decimal)

2. **Equality Query**: Specify two value queries and ask if their results are equal.
   - I will return "Yes" or "No"

Note: If a query causes a zero denominator (e.g., the filter condition has no elements), I will return "Unavailable", and this query will not count toward the limit.

Each turn must contain only one query tag, using the following XML format:

- Value Query (e.g., target is A1 and B1, filter is A1):
<query_value>X=A1 and B1, F=A1</query_value>

- Equality Query (e.g., asking if two value queries are equal):
<query_equal>Q1=(X=A1, F=B1), Q2=(X=B1, F=A1)</query_equal>

When you determine the scheme, submit in the following format:

<answer>scheme=A, verification_query=X=A1, F=B1, formula=|A1 and B1|/|B1|, historical_value=0.5</answer>

Where:
- **scheme**: Fill in A, B, C, or D
- **verification_query**: Select one of your previous value queries (expressed as X=..., F=...)
- **formula**: Provide the formal expression for this query under your determined scheme (using set cardinality notation)
- **historical_value**: The numerical value I returned for that query

Verification will check:
1. Whether the scheme is correct
2. Whether the formula matches the scheme's definition
3. Whether the result derived from the formula is consistent with the historical value
"""

    contextualized_rule_zh_2 = """\
欢迎使用医疗数据双盲分析系统。本模块用于评估不同亚群患者的治疗结果与临床特征的相关性。

系统加载了一个临床研究队列 U，包含 N 名患者病例（N 未知）。每个病例具有两种二元属性：
- 属性 A（家族史），取值为 A1（有家族史） 或 A2（无家族史）
- 属性 B（治疗结果），取值为 B1（治愈） 或 B2（未愈）

已知四种组合（A1且B1、A1且B2、A2且B1、A2且B2）的病例数量均大于 0。

系统底层已秘密选定了一种"基准换算方案"，对你的所有查询都将按照同一方案计算占比。方案共有四种可能（具体定义保密），不同方案会对相同查询给出不同的比例值。

你的目标是通过提问推断出系统使用的是哪一种方案，并给出验证。

你可以反复向我提出以下两类问题（每次仅限一个问题）：

1. **数值查询**：指定一个目标条件 X 和一个过滤条件 F。
   - X 可以是：A1、A2、B1、B2、A1且B1、A1且B2、A2且B1、A2且B2
   - F 只能是：A1、A2、B1、B2
   - 我会返回一个比例值（以分数或小数形式）

2. **相等性查询**：指定两个数值查询，询问它们的结果是否相等。
   - 我会返回"是"或"否"

注意：若某查询导致分母为 0（如过滤条件对应的元素数为 0），我会返回"不可用"，该次查询不计入有效次数。

每次只能包含一个查询标签，使用以下 XML 格式：

- 数值查询（例如目标为 A1且B1，过滤为 A1）：
<query_value>X=A1且B1, F=A1</query_value>

- 相等性查询（例如询问两个数值查询是否相等）：
<query_equal>Q1=(X=A1, F=B1), Q2=(X=B1, F=A1)</query_equal>

当你确定方案后，请按以下格式提交：

<answer>方案=A, 验证查询=X=A1, F=B1, 计算式=|A1且B1|/|B1|, 历史值=0.5</answer>

其中：
- **方案**：填写 A、B、C 或 D
- **验证查询**：从你之前的某一条数值查询中选择一条（用 X=..., F=... 表示）
- **计算式**：给出该查询在你判定的方案下的形式化表达式（用集合计数符号表示）
- **历史值**：该查询当时我返回的数值

验证将检查：
1. 方案是否正确
2. 计算式是否符合该方案的定义
3. 根据计算式推导的结果是否与历史值一致
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Medical Double-Blind Data Analysis System. This module is used to evaluate the correlation between treatment outcomes and clinical characteristics in different patient subpopulations.

The system has configured a finite set U containing N patient cases (N is unknown). Each patient case has two binary attributes:
- Attribute A (Family History), valued as A1 (Has Family History) or A2 (No Family History)
- Attribute B (Treatment Outcome), valued as B1 (Cured) or B2 (Uncured)

It is known that all four combinations (A1 and B1, A1 and B2, A2 and B1, A2 and B2) have positive counts.

The system has secretly selected a "baseline conversion scheme" that will be used consistently for all your queries. There are four possible schemes (definitions kept secret), and different schemes will return different ratio values for the same query.

Your goal is to deduce which scheme the system is using through queries, and provide verification.

You can repeatedly ask me the following two types of questions (one per turn):

1. **Value Query**: Specify a target condition X and a filter condition F.
   - X can be: A1, A2, B1, B2, A1 and B1, A1 and B2, A2 and B1, A2 and B2
   - F can only be: A1, A2, B1, B2
   - I will return a ratio value (as a fraction or decimal)

2. **Equality Query**: Specify two value queries and ask if their results are equal.
   - I will return "Yes" or "No"

Note: If a query causes a zero denominator (e.g., the filter condition has no elements), I will return "Unavailable", and this query will not count toward the limit.

Each turn must contain only one query tag, using the following XML format:

- Value Query (e.g., target is A1 and B1, filter is A1):
<query_value>X=A1 and B1, F=A1</query_value>

- Equality Query (e.g., asking if two value queries are equal):
<query_equal>Q1=(X=A1, F=B1), Q2=(X=B1, F=A1)</query_equal>

When you determine the scheme, submit in the following format:

<answer>scheme=A, verification_query=X=A1, F=B1, formula=|A1 and B1|/|B1|, historical_value=0.5</answer>

Where:
- **scheme**: Fill in A, B, C, or D
- **verification_query**: Select one of your previous value queries (expressed as X=..., F=...)
- **formula**: Provide the formal expression for this query under your determined scheme (using set cardinality notation)
- **historical_value**: The numerical value I returned for that query

Verification will check:
1. Whether the scheme is correct
2. Whether the formula matches the scheme's definition
3. Whether the result derived from the formula is consistent with the historical value
"""

    contextualized_rule_zh_3 = """\
欢迎登录教育质量追踪平台。本系统通过抽样数据，对比不同学习方式对学生成绩表现的潜在影响。

系统抽取了一个学生样本池 U，包含 N 名学生（N 未知）。每名学生具有两种二元属性：
- 属性 A（学习方式），取值为 A1（线上） 或 A2（线下）
- 属性 B（成绩表现），取值为 B1（达标） 或 B2（未达标）

已知四种组合（A1且B1、A1且B2、A2且B1、A2且B2）的学生数量均大于 0。

系统底层已秘密选定了一种"统计核算方案"，对你的所有查询都将按照同一方案计算占比。方案共有四种可能（具体定义保密），不同方案会对相同查询给出不同的比例值。

你的目标是通过提问推断出系统使用的是哪一种方案，并给出验证。

你可以反复向我提出以下两类问题（每次仅限一个问题）：

1. **数值查询**：指定一个目标条件 X 和一个过滤条件 F。
   - X 可以是：A1、A2、B1、B2、A1且B1、A1且B2、A2且B1、A2且B2
   - F 只能是：A1、A2、B1、B2
   - 我会返回一个比例值（以分数或小数形式）

2. **相等性查询**：指定两个数值查询，询问它们的结果是否相等。
   - 我会返回"是"或"否"

注意：若某查询导致分母为 0（如过滤条件对应的元素数为 0），我会返回"不可用"，该次查询不计入有效次数。

每次只能包含一个查询标签，使用以下 XML 格式：

- 数值查询（例如目标为 A1且B1，过滤为 A1）：
<query_value>X=A1且B1, F=A1</query_value>

- 相等性查询（例如询问两个数值查询是否相等）：
<query_equal>Q1=(X=A1, F=B1), Q2=(X=B1, F=A1)</query_equal>

当你确定方案后，请按以下格式提交：

<answer>方案=A, 验证查询=X=A1, F=B1, 计算式=|A1且B1|/|B1|, 历史值=0.5</answer>

其中：
- **方案**：填写 A、B、C 或 D
- **验证查询**：从你之前的某一条数值查询中选择一条（用 X=..., F=... 表示）
- **计算式**：给出该查询在你判定的方案下的形式化表达式（用集合计数符号表示）
- **历史值**：该查询当时我返回的数值

验证将检查：
1. 方案是否正确
2. 计算式是否符合该方案的定义
3. 根据计算式推导的结果是否与历史值一致
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Education Quality Tracking Platform. This system contrasts the potential impact of different learning modalities on students' performance using sampled data.

The system has configured a finite set U containing N student samples (N is unknown). Each student sample has two binary attributes:
- Attribute A (Learning Modality), valued as A1 (Online) or A2 (Offline)
- Attribute B (Performance), valued as B1 (Passed) or B2 (Failed)

It is known that all four combinations (A1 and B1, A1 and B2, A2 and B1, A2 and B2) have positive counts.

The system has secretly selected a "statistical accounting scheme" that will be used consistently for all your queries. There are four possible schemes (definitions kept secret), and different schemes will return different ratio values for the same query.

Your goal is to deduce which scheme the system is using through queries, and provide verification.

You can repeatedly ask me the following two types of questions (one per turn):

1. **Value Query**: Specify a target condition X and a filter condition F.
   - X can be: A1, A2, B1, B2, A1 and B1, A1 and B2, A2 and B1, A2 and B2
   - F can only be: A1, A2, B1, B2
   - I will return a ratio value (as a fraction or decimal)

2. **Equality Query**: Specify two value queries and ask if their results are equal.
   - I will return "Yes" or "No"

Note: If a query causes a zero denominator (e.g., the filter condition has no elements), I will return "Unavailable", and this query will not count toward the limit.

Each turn must contain only one query tag, using the following XML format:

- Value Query (e.g., target is A1 and B1, filter is A1):
<query_value>X=A1 and B1, F=A1</query_value>

- Equality Query (e.g., asking if two value queries are equal):
<query_equal>Q1=(X=A1, F=B1), Q2=(X=B1, F=A1)</query_equal>

When you determine the scheme, submit in the following format:

<answer>scheme=A, verification_query=X=A1, F=B1, formula=|A1 and B1|/|B1|, historical_value=0.5</answer>

Where:
- **scheme**: Fill in A, B, C, or D
- **verification_query**: Select one of your previous value queries (expressed as X=..., F=...)
- **formula**: Provide the formal expression for this query under your determined scheme (using set cardinality notation)
- **historical_value**: The numerical value I returned for that query

Verification will check:
1. Whether the scheme is correct
2. Whether the formula matches the scheme's definition
3. Whether the result derived from the formula is consistent with the historical value
"""

    contextualized_rule_zh_4 = """\
欢迎访问工业良率分析终端。本系统用于深挖不同生产线体和质检批次之间的数据关联，以定位潜在的产能瓶颈。

系统缓存了一个批次的生产部件集合 U，包含 N 个部件（N 未知）。每个部件具有两种二元属性：
- 属性 A（生产线），取值为 A1（自动化线） 或 A2（人工线）
- 属性 B（质检结果），取值为 B1（合格） 或 B2（瑕疵）

已知四种组合（A1且B1、A1且B2、A2且B1、A2且B2）的部件数量均大于 0。

系统底层已秘密选定了一种"良率基准核算方案"，对你的所有查询都将按照同一方案计算占比。方案共有四种可能（具体定义保密），不同方案会对相同查询给出不同的比例值。

你的目标是通过提问推断出系统使用的是哪一种方案，并给出验证。

你可以反复向我提出以下两类问题（每次仅限一个问题）：

1. **数值查询**：指定一个目标条件 X 和一个过滤条件 F。
   - X 可以是：A1、A2、B1、B2、A1且B1、A1且B2、A2且B1、A2且B2
   - F 只能是：A1、A2、B1、B2
   - 我会返回一个比例值（以分数或小数形式）

2. **相等性查询**：指定两个数值查询，询问它们的结果是否相等。
   - 我会返回"是"或"否"

注意：若某查询导致分母为 0（如过滤条件对应的元素数为 0），我会返回"不可用"，该次查询不计入有效次数。

每次只能包含一个查询标签，使用以下 XML 格式：

- 数值查询（例如目标为 A1且B1，过滤为 A1）：
<query_value>X=A1且B1, F=A1</query_value>

- 相等性查询（例如询问两个数值查询是否相等）：
<query_equal>Q1=(X=A1, F=B1), Q2=(X=B1, F=A1)</query_equal>

当你确定方案后，请按以下格式提交：

<answer>方案=A, 验证查询=X=A1, F=B1, 计算式=|A1且B1|/|B1|, 历史值=0.5</answer>

其中：
- **方案**：填写 A、B、C 或 D
- **验证查询**：从你之前的某一条数值查询中选择一条（用 X=..., F=... 表示）
- **计算式**：给出该查询在你判定的方案下的形式化表达式（用集合计数符号表示）
- **历史值**：该查询当时我返回的数值

验证将检查：
1. 方案是否正确
2. 计算式是否符合该方案的定义
3. 根据计算式推导的结果是否与历史值一致
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the Industrial Yield Analysis Terminal. This system is used to mine data associations between different production lines and quality inspection batches to locate potential capacity bottlenecks.

The system has configured a finite set U containing N production components (N is unknown). Each production component has two binary attributes:
- Attribute A (Production Line), valued as A1 (Auto Line) or A2 (Manual Line)
- Attribute B (Inspection Result), valued as B1 (Passed) or B2 (Defective)

It is known that all four combinations (A1 and B1, A1 and B2, A2 and B1, A2 and B2) have positive counts.

The system has secretly selected a "yield baseline accounting scheme" that will be used consistently for all your queries. There are four possible schemes (definitions kept secret), and different schemes will return different ratio values for the same query.

Your goal is to deduce which scheme the system is using through queries, and provide verification.

You can repeatedly ask me the following two types of questions (one per turn):

1. **Value Query**: Specify a target condition X and a filter condition F.
   - X can be: A1, A2, B1, B2, A1 and B1, A1 and B2, A2 and B1, A2 and B2
   - F can only be: A1, A2, B1, B2
   - I will return a ratio value (as a fraction or decimal)

2. **Equality Query**: Specify two value queries and ask if their results are equal.
   - I will return "Yes" or "No"

Note: If a query causes a zero denominator (e.g., the filter condition has no elements), I will return "Unavailable", and this query will not count toward the limit.

Each turn must contain only one query tag, using the following XML format:

- Value Query (e.g., target is A1 and B1, filter is A1):
<query_value>X=A1 and B1, F=A1</query_value>

- Equality Query (e.g., asking if two value queries are equal):
<query_equal>Q1=(X=A1, F=B1), Q2=(X=B1, F=A1)</query_equal>

When you determine the scheme, submit in the following format:

<answer>scheme=A, verification_query=X=A1, F=B1, formula=|A1 and B1|/|B1|, historical_value=0.5</answer>

Where:
- **scheme**: Fill in A, B, C, or D
- **verification_query**: Select one of your previous value queries (expressed as X=..., F=...)
- **formula**: Provide the formal expression for this query under your determined scheme (using set cardinality notation)
- **historical_value**: The numerical value I returned for that query

Verification will check:
1. Whether the scheme is correct
2. Whether the formula matches the scheme's definition
3. Whether the result derived from the formula is consistent with the historical value
"""

    contextualized_rule_zh_5 = """\
欢迎进入司法判例检索系统。本系统基于海量卷宗，协助您计算特定前置条件组合下的判决比率。

系统筛选了一个特定领域的过往案例库 U，包含 N 份卷宗（N 未知）。每份卷宗具有两种二元属性：
- 属性 A（案件类型），取值为 A1（民事纠纷） 或 A2（刑事诉讼）
- 属性 B（判决结果），取值为 B1（胜诉） 或 B2（败诉）

已知四种组合（A1且B1、A1且B2、A2且B1、A2且B2）的卷宗数量均大于 0。

系统底层已秘密选定了一种"判例比率统计方案"，对你的所有查询都将按照同一方案计算占比。方案共有四种可能（具体定义保密），不同方案会对相同查询给出不同的比例值。

你的目标是通过提问推断出系统使用的是哪一种方案，并给出验证。

你可以反复向我提出以下两类问题（每次仅限一个问题）：

1. **数值查询**：指定一个目标条件 X 和一个过滤条件 F。
   - X 可以是：A1、A2、B1、B2、A1且B1、A1且B2、A2且B1、A2且B2
   - F 只能是：A1、A2、B1、B2
   - 我会返回一个比例值（以分数或小数形式）

2. **相等性查询**：指定两个数值查询，询问它们的结果是否相等。
   - 我会返回"是"或"否"

注意：若某查询导致分母为 0（如过滤条件对应的元素数为 0），我会返回"不可用"，该次查询不计入有效次数。

每次只能包含一个查询标签，使用以下 XML 格式：

- 数值查询（例如目标为 A1且B1，过滤为 A1）：
<query_value>X=A1且B1, F=A1</query_value>

- 相等性查询（例如询问两个数值查询是否相等）：
<query_equal>Q1=(X=A1, F=B1), Q2=(X=B1, F=A1)</query_equal>

当你确定方案后，请按以下格式提交：

<answer>方案=A, 验证查询=X=A1, F=B1, 计算式=|A1且B1|/|B1|, 历史值=0.5</answer>

其中：
- **方案**：填写 A、B、C 或 D
- **验证查询**：从你之前的某一条数值查询中选择一条（用 X=..., F=... 表示）
- **计算式**：给出该查询在你判定的方案下的形式化表达式（用集合计数符号表示）
- **历史值**：该查询当时我返回的数值

验证将检查：
1. 方案是否正确
2. 计算式是否符合该方案的定义
3. 根据计算式推导的结果是否与历史值一致
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Judicial Case Retrieval System. This system assists you in calculating the judgment ratios under specific combinations of preconditions based on massive case files.

The system has configured a finite set U containing N case files (N is unknown). Each case file has two binary attributes:
- Attribute A (Case Type), valued as A1 (Civil Dispute) or A2 (Criminal Proceeding)
- Attribute B (Judgment Result), valued as B1 (Won) or B2 (Lost)

It is known that all four combinations (A1 and B1, A1 and B2, A2 and B1, A2 and B2) have positive counts.

The system has secretly selected a "case ratio statistics scheme" that will be used consistently for all your queries. There are four possible schemes (definitions kept secret), and different schemes will return different ratio values for the same query.

Your goal is to deduce which scheme the system is using through queries, and provide verification.

You can repeatedly ask me the following two types of questions (one per turn):

1. **Value Query**: Specify a target condition X and a filter condition F.
   - X can be: A1, A2, B1, B2, A1 and B1, A1 and B2, A2 and B1, A2 and B2
   - F can only be: A1, A2, B1, B2
   - I will return a ratio value (as a fraction or decimal)

2. **Equality Query**: Specify two value queries and ask if their results are equal.
   - I will return "Yes" or "No"

Note: If a query causes a zero denominator (e.g., the filter condition has no elements), I will return "Unavailable", and this query will not count toward the limit.

Each turn must contain only one query tag, using the following XML format:

- Value Query (e.g., target is A1 and B1, filter is A1):
<query_value>X=A1 and B1, F=A1</query_value>

- Equality Query (e.g., asking if two value queries are equal):
<query_equal>Q1=(X=A1, F=B1), Q2=(X=B1, F=A1)</query_equal>

When you determine the scheme, submit in the following format:

<answer>scheme=A, verification_query=X=A1, F=B1, formula=|A1 and B1|/|B1|, historical_value=0.5</answer>

Where:
- **scheme**: Fill in A, B, C, or D
- **verification_query**: Select one of your previous value queries (expressed as X=..., F=...)
- **formula**: Provide the formal expression for this query under your determined scheme (using set cardinality notation)
- **historical_value**: The numerical value I returned for that query

Verification will check:
1. Whether the scheme is correct
2. Whether the formula matches the scheme's definition
3. Whether the result derived from the formula is consistent with the historical value
"""

    tags = ["answer", "query_value", "query_equal"]
    
    reasoning_type = "溯因推理"
    data_structure = "集合"

    DIFFICULTY_CONFIG = {
        1: {
            "N": 12,
            "counts": {"A1_B1": 3, "A1_B2": 3, "A2_B1": 3, "A2_B2": 3},
            "scheme": "A",
        },
        2: {
            "N": 20,
            "counts": {"A1_B1": 4, "A1_B2": 6, "A2_B1": 5, "A2_B2": 5},
            "scheme": "B",
        },
        3: {
            "N": 24,
            "counts": {"A1_B1": 6, "A1_B2": 4, "A2_B1": 8, "A2_B2": 6},
            "scheme": "C",
        },
        4: {
            "N": 30,
            "counts": {"A1_B1": 8, "A1_B2": 7, "A2_B1": 6, "A2_B2": 9},
            "scheme": "D",
        },
        5: {
            "N": 40,
            "counts": {"A1_B1": 12, "A1_B2": 8, "A2_B1": 10, "A2_B2": 10},
            "scheme": "B",
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)
        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self.N = cfg["N"]
        self.counts = cfg["counts"]
        self.scheme = cfg["scheme"]

        self.count_A1 = self.counts["A1_B1"] + self.counts["A1_B2"]
        self.count_A2 = self.counts["A2_B1"] + self.counts["A2_B2"]
        self.count_B1 = self.counts["A1_B1"] + self.counts["A2_B1"]
        self.count_B2 = self.counts["A1_B2"] + self.counts["A2_B2"]

        self.query_history = []

        self._game_info = {}

    def _parse_condition(self, cond_str):
        cond_str = cond_str.strip()

        if "且" in cond_str:
            parts = cond_str.split("且")
        elif " and " in cond_str.lower():
            parts = cond_str.lower().split(" and ")
        else:
            return ("simple", cond_str.upper())

        if len(parts) == 2:
            attr_a = parts[0].strip().upper()
            attr_b = parts[1].strip().upper()
            if attr_a.startswith("B") and attr_b.startswith("A"):
                attr_a, attr_b = attr_b, attr_a
            return ("conj", (attr_a, attr_b))
        else:
            raise ValueError(f"Invalid condition format: {cond_str}")

    def _get_count(self, cond_type, cond_val):
        if cond_type == "simple":
            attr = cond_val
            if attr == "A1":
                return self.count_A1
            elif attr == "A2":
                return self.count_A2
            elif attr == "B1":
                return self.count_B1
            elif attr == "B2":
                return self.count_B2
            else:
                raise ValueError(f"Unknown attribute: {attr}")
        elif cond_type == "conj":
            attr_a, attr_b = cond_val
            key = f"{attr_a}_{attr_b}"
            if key in self.counts:
                return self.counts[key]
            else:
                raise ValueError(f"Unknown conjunction: {key}")
        else:
            raise ValueError(f"Unknown condition type: {cond_type}")

    def _calculate_value(self, X_type, X_val, F_type, F_val):
        count_X = self._get_count(X_type, X_val)
        count_F = self._get_count(F_type, F_val)

        count_X_intersect_F = self._calculate_intersection(X_type, X_val, F_type, F_val)

        count_not_F = self.N - count_F

        count_X_intersect_not_F = count_X - count_X_intersect_F

        if self.scheme == "A":
            if self.N == 0:
                return None, "unavailable"
            return count_X / self.N, "ok"

        elif self.scheme == "B":
            if count_F == 0:
                return None, "unavailable"
            return count_X_intersect_F / count_F, "ok"

        elif self.scheme == "C":
            if count_X == 0:
                return None, "unavailable"
            return count_X_intersect_F / count_X, "ok"

        elif self.scheme == "D":
            if count_not_F == 0:
                return None, "unavailable"
            return count_X_intersect_not_F / count_not_F, "ok"

        else:
            raise ValueError(f"Unknown scheme: {self.scheme}")

    def _calculate_intersection(self, X_type, X_val, F_type, F_val):
        if X_type == "simple" and F_type == "simple":
            X_attr = X_val
            F_attr = F_val

            if X_attr[0] == F_attr[0]:
                if X_attr == F_attr:
                    return self._get_count(X_type, X_val)
                else:
                    return 0
            else:
                if X_attr.startswith("A"):
                    key = f"{X_attr}_{F_attr}"
                else:
                    key = f"{F_attr}_{X_attr}"
                return self.counts.get(key, 0)

        elif X_type == "conj" and F_type == "simple":
            attr_a, attr_b = X_val
            F_attr = F_val

            if F_attr == attr_a or F_attr == attr_b:
                return self._get_count(X_type, X_val)
            elif F_attr[0] == attr_a[0]:
                return 0
            elif F_attr[0] == attr_b[0]:
                return 0
            else:
                return 0

        else:
            raise ValueError(f"Unexpected condition types: X_type={X_type}, F_type={F_type}")

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]

        is_zh = self.config.language == "zh"

        if is_zh:
            scheme_pattern = r'方案\s*=\s*([A-Da-d])'
            verify_pattern = r'验证查询\s*=\s*(X\s*=\s*.+?,\s*F\s*=\s*\S+)'
            formula_pattern = r'计算式\s*=\s*(.+?)(?:,\s*历史值|$)'
            history_pattern = r'历史值\s*=\s*([\d.]+)'
        else:
            scheme_pattern = r'scheme\s*=\s*([A-Da-d])'
            verify_pattern = r'verification_query\s*=\s*(X\s*=\s*.+?,\s*F\s*=\s*\S+)'
            formula_pattern = r'formula\s*=\s*(.+?)(?:,\s*historical_value|$)'
            history_pattern = r'historical_value\s*=\s*([\d.]+)'

        scheme_match = re.search(scheme_pattern, raw_ans, re.IGNORECASE)
        verify_match = re.search(verify_pattern, raw_ans, re.IGNORECASE)
        formula_match = re.search(formula_pattern, raw_ans, re.IGNORECASE)
        history_match = re.search(history_pattern, raw_ans, re.IGNORECASE)

        if not all([scheme_match, verify_match, formula_match, history_match]):
            return False

        claimed_scheme = scheme_match.group(1).strip().upper()
        verify_query_str = verify_match.group(1).strip()
        claimed_formula = formula_match.group(1).strip()
        try:
            claimed_history_val = float(history_match.group(1).strip())
        except:
            return False

        if claimed_scheme != self.scheme:
            return False

        norm_verify = re.sub(r'\s+', '', verify_query_str)
        found = False
        for hist_query, hist_value in self.query_history:
            norm_hist = re.sub(r'\s+', '', hist_query)
            if norm_hist == norm_verify and abs(hist_value - claimed_history_val) < 1e-4:
                found = True
                break

        if not found:
            return False

        formula = claimed_formula.replace(" ", "").upper()
        if self.scheme == "A":
            if "/N" not in formula and "/|U|" not in formula:
                return False
        elif self.scheme == "B":
            if "/" not in formula:
                return False
        elif self.scheme == "C":
            if "/" not in formula:
                return False
        elif self.scheme == "D":
            if "/" not in formula:
                return False

        return True

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        atoms = ["A1", "A2", "B1", "B2"]
        filters = atoms
        
        targets_simple = atoms
        
        targets_conj = []
        is_zh = self.config.language == "zh"
        conn = "且" if is_zh else " and "
        
        for a in ["A1", "A2"]:
            for b in ["B1", "B2"]:
                targets_conj.append((f"{a}{conn}{b}", ("conj", (a, b))))

        for x_str in targets_simple:
            x_type, x_val = "simple", x_str
            for f_str in filters:
                f_type, f_val = "simple", f_str
                
                query_content = f"X={x_str}, F={f_str}"
                full_query = f"<query_value>{query_content}</query_value>"
                
                val, status = self._calculate_value(x_type, x_val, f_type, f_val)
                
                if status == "unavailable":
                    ans = "不可用" if is_zh else "Unavailable"
                else:
                    ans = f"{val:.4f}"
                    
                results.append({"query": full_query, "answer": ans})
                
        for x_str, (x_type, x_val) in targets_conj:
            for f_str in filters:
                f_type, f_val = "simple", f_str
                
                query_content = f"X={x_str}, F={f_str}"
                full_query = f"<query_value>{query_content}</query_value>"
                
                val, status = self._calculate_value(x_type, x_val, f_type, f_val)
                
                if status == "unavailable":
                    ans = "不可用" if is_zh else "Unavailable"
                else:
                    ans = f"{val:.4f}"
                    
                results.append({"query": full_query, "answer": ans})
                
        return results

    def _cf_core_produce(self, parsed_info):
        if "query_value" in parsed_info:
            return self._handle_value_query(parsed_info["query_value"])
        elif "query_equal" in parsed_info:
            return self._handle_equal_query(parsed_info["query_equal"])
        else:
            raise ValueError("No valid query tag found.")

    def _handle_value_query(self, query_str):
        try:
            match = re.match(r'(.+?),\s*F\s*=\s*(.+)', query_str)
            if not match:
                raise ValueError("Value query must have X and F")

            X_part = match.group(1).strip()
            F_str = match.group(2).strip()

            if not X_part.startswith("X="):
                raise ValueError("Value query format error: missing X=")

            X_str = X_part[2:].strip()

            X_type, X_val = self._parse_condition(X_str)
            F_type, F_val = self._parse_condition(F_str)

            if F_type != "simple":
                raise ValueError("Filter condition F must be atomic")

            result, status = self._calculate_value(X_type, X_val, F_type, F_val)

            if status == "unavailable":
                return "不可用" if self.config.language == "zh" else "Unavailable"

            self.query_history.append((query_str, result))

            return f"{result:.4f}"

        except Exception as e:
            return f"错误：查询格式无效 ({str(e)})" if self.config.language == "zh" else f"Error: Invalid query format ({str(e)})"

    def _handle_equal_query(self, query_str):
        try:
            if "Q1=" not in query_str or "Q2=" not in query_str:
                raise ValueError("Equal query must have Q1 and Q2")

            q1_start = query_str.find("Q1=") + 3
            q2_start = query_str.find("Q2=") + 3

            if q2_start < q1_start:
                q2_start, q1_start = q1_start - 3, q2_start - 3
                q1_str = query_str[q1_start + 3:].strip()
                q2_str = query_str[q2_start + 3:q1_start].strip()
            else:
                q1_str = query_str[q1_start:q2_start - 3].strip()
                q2_str = query_str[q2_start:].strip()

            q1_str = q1_str.strip("() ")
            q2_str = q2_str.strip("() ")

            if q1_str.endswith(","):
                q1_str = q1_str[:-1].strip()
            if q2_str.endswith(","):
                q2_str = q2_str[:-1].strip()

            val1, status1 = self._parse_and_calculate_query(q1_str)
            val2, status2 = self._parse_and_calculate_query(q2_str)

            if status1 == "unavailable" or status2 == "unavailable":
                return "不可用" if self.config.language == "zh" else "Unavailable"

            is_equal = abs(val1 - val2) < 1e-6

            if self.config.language == "zh":
                return "是" if is_equal else "否"
            else:
                return "Yes" if is_equal else "No"

        except Exception as e:
            if self.config.language == "zh":
                return f"错误：查询格式无效 ({str(e)})"
            else:
                return f"Error: Invalid query format ({str(e)})"

    def _parse_and_calculate_query(self, query_str):
        match = re.match(r'(.+?),\s*F\s*=\s*(.+)', query_str)
        if not match:
            raise ValueError("Query must have X and F")

        X_part = match.group(1).strip()
        F_str = match.group(2).strip()

        if not X_part.startswith("X="):
            raise ValueError("Query format error")

        X_str = X_part[2:].strip()

        X_type, X_val = self._parse_condition(X_str)
        F_type, F_val = self._parse_condition(F_str)

        if F_type != "simple":
            raise ValueError("Filter F must be atomic")

        return self._calculate_value(X_type, X_val, F_type, F_val)

    def _cf_make_wrong(self, correct):
        if correct in ["是", "Yes"]:
            return "否" if self.config.language == "zh" else "No"
        elif correct in ["否", "No"]:
            return "是" if self.config.language == "zh" else "Yes"
        elif correct in ["不可用", "Unavailable"]:
            return "0.1234"
        elif correct.startswith("错误") or correct.startswith("Error"):
            return "0.1234"
        else:
            try:
                val = float(correct)
                wrong_val = val + 0.1
                if wrong_val > 1.0:
                    wrong_val = val - 0.1
                return f"{wrong_val:.4f}"
            except:
                return "不可用" if self.config.language == "zh" else "Unavailable"