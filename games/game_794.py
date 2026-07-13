# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 集合：存在一个由N个物体组成的集合，注意他们不存在位置、前后和大小关系。
# 知识点:   条件定位：哪个/哪些元素满足某给定属性
# ============================================================

from .base import Game
import re


class BooleanConceptGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "集合"

    game_rule_zh = """\
我们来玩一个"布尔概念识别"的推理游戏，规则如下：

游戏中有12个对象，编号为 #01 到 #12。每个对象由4个二元属性 A1, A2, A3, A4 描述，每个属性的取值为 0 或 1。

这些对象的属性向量如下：
- #01: (1,1,1,1)
- #02: (1,1,1,0)
- #03: (1,1,0,1)
- #04: (1,0,1,1)
- #05: (0,1,1,1)
- #06: (1,0,0,0)
- #07: (0,0,1,1)
- #08: (0,1,0,1)
- #09: (0,0,0,1)
- #10: (0,1,1,0)
- #11: (1,1,0,0)
- #12: (0,0,1,0)

我已秘密选择了一个布尔谓词 f，该谓词依赖这4个属性 A1, A2, A3, A4，对每个对象返回 0 或 1（即该对象是否满足谓词）。该谓词可由原子命题（Ai=0 或 Ai=1）通过逻辑运算符 AND、OR、NOT 组成，且表达式的布尔深度不超过2层，总文字数不超过4个。

你的目标是通过查询推断出这个隐藏的布尔谓词，并预测哪些对象满足该谓词（即 f 返回 1 的对象集合）。

你可以进行以下两种查询：

1. **子集计数查询**（限定次数）：
   指定一个对象子集 S，我会告诉你：
   - m: 子集 S 的大小
   - k: 子集 S 中满足谓词 f 的对象数量
   - 剩余查询次数
   
   你可以用两种方式指定子集：
   - 显式列举对象编号（如 #01,#03,#05）
   - 提供布尔筛选表达式（如 A1=1 AND A2=0），系统会自动筛选满足条件的对象

2. **成员查询**（限定次数）：
   询问特定对象 #i 是否满足谓词 f。我会回答"是"或"否"，并告知剩余查询次数。

当你收集到足够信息后，请提交最终答案，包括：
- 布尔表达式：描述谓词 f 的逻辑结构
- 正例集合：你预测满足 f 的所有对象编号

## 查询与提交格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 子集计数查询（显式列举）：
<query_subset>#01,#03,#05</query_subset>

- 子集计数查询（布尔表达式）：
<query_subset>A1=1 AND A2=0</query_subset>

- 成员查询（例如询问对象 #05）：
<query_member>#05</query_member>

- 提交最终答案：
<answer>expression=A1=1 AND A2=1, positive_set=#01,#02,#03</answer>

注意：
- 布尔表达式中使用 AND、OR、NOT 作为逻辑运算符
- 对象编号必须带 # 前缀
- 答案中 expression 和 positive_set 必须同时提供且用逗号分隔
- 请尽可能少地使用查询次数来推断谓词
"""

    game_rule_en = """\
Let's play a "Boolean Concept Identification" deduction game. Here are the rules:

There are 12 objects in the game, numbered #01 to #12. Each object is described by 4 binary attributes A1, A2, A3, A4, where each attribute has a value of 0 or 1.

The attribute vectors for these objects are:
- #01: (1,1,1,1)
- #02: (1,1,1,0)
- #03: (1,1,0,1)
- #04: (1,0,1,1)
- #05: (0,1,1,1)
- #06: (1,0,0,0)
- #07: (0,0,1,1)
- #08: (0,1,0,1)
- #09: (0,0,0,1)
- #10: (0,1,1,0)
- #11: (1,1,0,0)
- #12: (0,0,1,0)

I have secretly chosen a Boolean predicate f that depends on these 4 attributes A1, A2, A3, A4 and returns 0 or 1 for each object (whether the object satisfies the predicate). This predicate can be composed of atomic propositions (Ai=0 or Ai=1) using logical operators AND, OR, NOT, with Boolean depth no more than 2 layers and total literals no more than 4.

Your goal is to infer this hidden Boolean predicate through queries and predict which objects satisfy the predicate (i.e., the set of objects where f returns 1).

You can perform the following two types of queries:

1. **Subset Count Query** (limited quota):
   Specify a subset S of objects, and I will tell you:
   - m: the size of subset S
   - k: the number of objects in S that satisfy predicate f
   - remaining query count
   
   You can specify the subset in two ways:
   - Explicitly list object IDs (e.g., #01,#03,#05)
   - Provide a Boolean filter expression (e.g., A1=1 AND A2=0), and the system will automatically filter objects meeting the condition

2. **Membership Query** (limited quota):
   Ask whether a specific object #i satisfies predicate f. I will answer "Yes" or "No" and tell you the remaining query count.

When you have collected enough information, submit your final answer, including:
- Boolean expression: describing the logical structure of predicate f
- Positive set: all object IDs you predict satisfy f

## Query and Submission Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Subset count query (explicit list):
<query_subset>#01,#03,#05</query_subset>

- Subset count query (Boolean expression):
<query_subset>A1=1 AND A2=0</query_subset>

- Membership query (e.g., asking about object #05):
<query_member>#05</query_member>

- Submit final answer:
<answer>expression=A1=1 AND A2=1, positive_set=#01,#02,#03</answer>

Notes:
- Use AND, OR, NOT as logical operators in Boolean expressions
- Object IDs must have # prefix
- Both expression and positive_set must be provided in the answer, separated by comma
- Try to use as few queries as possible to infer the predicate
"""

    contextualized_rule_zh_1 = """\
我们来玩一个"自动驾驶高危场景识别"的推理游戏，规则如下：

作为自动驾驶安全测试工程师，你需要排查12个测试对象（即测试场景），编号为 #01 到 #12。每个对象由4个二元属性 A1, A2, A3, A4 描述，每个属性的取值为 0 或 1（0 代表否，1 代表是）：
- A1: 道路处于高峰期车流
- A2: 存在行人穿越斑马线
- A3: 处于恶劣天气条件
- A4: 前方路口信号灯故障

这些对象的属性向量如下：
- #01: (1,1,1,1)
- #02: (1,1,1,0)
- #03: (1,1,0,1)
- #04: (1,0,1,1)
- #05: (0,1,1,1)
- #06: (1,0,0,0)
- #07: (0,0,1,1)
- #08: (0,1,0,1)
- #09: (0,0,0,1)
- #10: (0,1,1,0)
- #11: (1,1,0,0)
- #12: (0,0,1,0)

系统已秘密设置了一个布尔谓词 f（即触发"人工接管"的安全判定规则），该谓词依赖这4个属性 A1, A2, A3, A4，对每个对象返回 0 或 1（即该对象是否满足谓词，触发接管）。该谓词可由原子命题（Ai=0 或 Ai=1）通过逻辑运算符 AND、OR、NOT 组成，且表达式的布尔深度不超过2层，总文字数不超过4个。

你的目标是通过查询推断出这个隐藏的布尔谓词，并预测哪些对象满足该谓词（即 f 返回 1 的接管场景集合）。

你可以进行以下两种查询：

1. **子集计数查询**（限定次数）：
   指定一个对象子集 S，我会告诉你：
   - m: 子集 S 的大小
   - k: 子集 S 中满足谓词 f 的对象数量
   - 剩余查询次数
   
   你可以用两种方式指定子集：
   - 显式列举对象编号（如 #01,#03,#05）
   - 提供布尔筛选表达式（如 A1=1 AND A2=0），系统会自动筛选满足条件的对象

2. **成员查询**（限定次数）：
   询问特定对象 #i 是否满足谓词 f。我会回答"是"或"否"，并告知剩余查询次数。

当你收集到足够信息后，请提交最终答案，包括：
- 布尔表达式：描述谓词 f 的逻辑结构
- 正例集合：你预测满足 f 的所有对象编号

## 查询与提交格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 子集计数查询（显式列举）：
<query_subset>#01,#03,#05</query_subset>

- 子集计数查询（布尔表达式）：
<query_subset>A1=1 AND A2=0</query_subset>

- 成员查询（例如询问对象 #05）：
<query_member>#05</query_member>

- 提交最终答案：
<answer>expression=A1=1 AND A2=1, positive_set=#01,#02,#03</answer>

注意：
- 布尔表达式中使用 AND、OR、NOT 作为逻辑运算符
- 对象编号必须带 # 前缀
- 答案中 expression 和 positive_set 必须同时提供且用逗号分隔
- 请尽可能少地使用查询次数来推断谓词
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play an "Autonomous Driving Risk Identification" deduction game. Here are the rules:

As an autonomous driving safety test engineer, you need to evaluate 12 test objects (i.e., driving scenarios), numbered #01 to #12. Each object is described by 4 binary attributes A1, A2, A3, A4, where each attribute has a value of 0 or 1 (0 for False, 1 for True):
- A1: High traffic volume on the road
- A2: Pedestrian crossing the zebra crossing
- A3: Severe weather conditions present
- A4: Traffic light failure at the intersection ahead

The attribute vectors for these objects are:
- #01: (1,1,1,1)
- #02: (1,1,1,0)
- #03: (1,1,0,1)
- #04: (1,0,1,1)
- #05: (0,1,1,1)
- #06: (1,0,0,0)
- #07: (0,0,1,1)
- #08: (0,1,0,1)
- #09: (0,0,0,1)
- #10: (0,1,1,0)
- #11: (1,1,0,0)
- #12: (0,0,1,0)

I have secretly chosen a Boolean predicate f (the safety rule triggering "manual takeover") that depends on these 4 attributes A1, A2, A3, A4 and returns 0 or 1 for each object (whether the object satisfies the predicate and requires takeover). This predicate can be composed of atomic propositions (Ai=0 or Ai=1) using logical operators AND, OR, NOT, with Boolean depth no more than 2 layers and total literals no more than 4.

Your goal is to infer this hidden Boolean predicate through queries and predict which objects satisfy the predicate (i.e., the set of objects where f returns 1).

You can perform the following two types of queries:

1. **Subset Count Query** (limited quota):
   Specify a subset S of objects, and I will tell you:
   - m: the size of subset S
   - k: the number of objects in S that satisfy predicate f
   - remaining query count
   
   You can specify the subset in two ways:
   - Explicitly list object IDs (e.g., #01,#03,#05)
   - Provide a Boolean filter expression (e.g., A1=1 AND A2=0), and the system will automatically filter objects meeting the condition

2. **Membership Query** (limited quota):
   Ask whether a specific object #i satisfies predicate f. I will answer "Yes" or "No" and tell you the remaining query count.

When you have collected enough information, submit your final answer, including:
- Boolean expression: describing the logical structure of predicate f
- Positive set: all object IDs you predict satisfy f

## Query and Submission Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Subset count query (explicit list):
<query_subset>#01,#03,#05</query_subset>

- Subset count query (Boolean expression):
<query_subset>A1=1 AND A2=0</query_subset>

- Membership query (e.g., asking about object #05):
<query_member>#05</query_member>

- Submit final answer:
<answer>expression=A1=1 AND A2=1, positive_set=#01,#02,#03</answer>

Notes:
- Use AND, OR, NOT as logical operators in Boolean expressions
- Object IDs must have # prefix
- Both expression and positive_set must be provided in the answer, separated by comma
- Try to use as few queries as possible to infer the predicate
"""

    contextualized_rule_zh_2 = """\
我们来玩一个"心血管高危患者筛查"的推理游戏，规则如下：

作为临床心血管学专家，你需要评估12个临床对象（即患者病例），编号为 #01 到 #12。每个对象由4个二元属性 A1, A2, A3, A4 描述，每个属性的取值为 0 或 1（0 代表阴性/无，1 代表阳性/有）：
- A1: 患有重度高血压
- A2: 空腹血糖指标异常
- A3: 有心脏病家族史
- A4: 低密度脂蛋白胆固醇偏高

这些对象的属性向量如下：
- #01: (1,1,1,1)
- #02: (1,1,1,0)
- #03: (1,1,0,1)
- #04: (1,0,1,1)
- #05: (0,1,1,1)
- #06: (1,0,0,0)
- #07: (0,0,1,1)
- #08: (0,1,0,1)
- #09: (0,0,0,1)
- #10: (0,1,1,0)
- #11: (1,1,0,0)
- #12: (0,0,1,0)

我已秘密选择了一个布尔谓词 f（即判定为"心血管疾病高危"的诊断规则），该谓词依赖这4个属性 A1, A2, A3, A4，对每个对象返回 0 或 1（即该对象是否满足谓词，被确诊为高危）。该谓词可由原子命题（Ai=0 或 Ai=1）通过逻辑运算符 AND、OR、NOT 组成，且表达式的布尔深度不超过2层，总文字数不超过4个。

你的目标是通过查询推断出这个隐藏的布尔谓词，并预测哪些对象满足该谓词（即 f 返回 1 的高危患者集合）。

你可以进行以下两种查询：

1. **子集计数查询**（限定次数）：
   指定一个对象子集 S，我会告诉你：
   - m: 子集 S 的大小
   - k: 子集 S 中满足谓词 f 的对象数量
   - 剩余查询次数
   
   你可以用两种方式指定子集：
   - 显式列举对象编号（如 #01,#03,#05）
   - 提供布尔筛选表达式（如 A1=1 AND A2=0），系统会自动筛选满足条件的对象

2. **成员查询**（限定次数）：
   询问特定对象 #i 是否满足谓词 f。我会回答"是"或"否"，并告知剩余查询次数。

当你收集到足够信息后，请提交最终答案，包括：
- 布尔表达式：描述谓词 f 的逻辑结构
- 正例集合：你预测满足 f 的所有对象编号

## 查询与提交格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 子集计数查询（显式列举）：
<query_subset>#01,#03,#05</query_subset>

- 子集计数查询（布尔表达式）：
<query_subset>A1=1 AND A2=0</query_subset>

- 成员查询（例如询问对象 #05）：
<query_member>#05</query_member>

- 提交最终答案：
<answer>expression=A1=1 AND A2=1, positive_set=#01,#02,#03</answer>

注意：
- 布尔表达式中使用 AND、OR、NOT 作为逻辑运算符
- 对象编号必须带 # 前缀
- 答案中 expression 和 positive_set 必须同时提供且用逗号分隔
- 请尽可能少地使用查询次数来推断谓词
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Cardiovascular Risk Screening" deduction game. Here are the rules:

As a clinical cardiologist, you need to evaluate 12 clinical objects (i.e., patient cases), numbered #01 to #12. Each object is described by 4 binary attributes A1, A2, A3, A4, where each attribute has a value of 0 or 1 (0 for Negative/No, 1 for Positive/Yes):
- A1: Severe hypertension present
- A2: Abnormal fasting blood glucose
- A3: Family history of heart disease
- A4: Elevated LDL cholesterol levels

The attribute vectors for these objects are:
- #01: (1,1,1,1)
- #02: (1,1,1,0)
- #03: (1,1,0,1)
- #04: (1,0,1,1)
- #05: (0,1,1,1)
- #06: (1,0,0,0)
- #07: (0,0,1,1)
- #08: (0,1,0,1)
- #09: (0,0,0,1)
- #10: (0,1,1,0)
- #11: (1,1,0,0)
- #12: (0,0,1,0)

I have secretly chosen a Boolean predicate f (the diagnostic rule for "high cardiovascular risk") that depends on these 4 attributes A1, A2, A3, A4 and returns 0 or 1 for each object (whether the object satisfies the predicate and is diagnosed as high risk). This predicate can be composed of atomic propositions (Ai=0 or Ai=1) using logical operators AND, OR, NOT, with Boolean depth no more than 2 layers and total literals no more than 4.

Your goal is to infer this hidden Boolean predicate through queries and predict which objects satisfy the predicate (i.e., the set of objects where f returns 1).

You can perform the following two types of queries:

1. **Subset Count Query** (limited quota):
   Specify a subset S of objects, and I will tell you:
   - m: the size of subset S
   - k: the number of objects in S that satisfy predicate f
   - remaining query count
   
   You can specify the subset in two ways:
   - Explicitly list object IDs (e.g., #01,#03,#05)
   - Provide a Boolean filter expression (e.g., A1=1 AND A2=0), and the system will automatically filter objects meeting the condition

2. **Membership Query** (limited quota):
   Ask whether a specific object #i satisfies predicate f. I will answer "Yes" or "No" and tell you the remaining query count.

When you have collected enough information, submit your final answer, including:
- Boolean expression: describing the logical structure of predicate f
- Positive set: all object IDs you predict satisfy f

## Query and Submission Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Subset count query (explicit list):
<query_subset>#01,#03,#05</query_subset>

- Subset count query (Boolean expression):
<query_subset>A1=1 AND A2=0</query_subset>

- Membership query (e.g., asking about object #05):
<query_member>#05</query_member>

- Submit final answer:
<answer>expression=A1=1 AND A2=1, positive_set=#01,#02,#03</answer>

Notes:
- Use AND, OR, NOT as logical operators in Boolean expressions
- Object IDs must have # prefix
- Both expression and positive_set must be provided in the answer, separated by comma
- Try to use as few queries as possible to infer the predicate
"""

    contextualized_rule_zh_3 = """\
我们来玩一个"学业风险预警系统"的推理游戏，规则如下：

作为高校辅导员或教务人员，你需要分析12个评估对象（即学生档案），编号为 #01 到 #12。每个对象由4个二元属性 A1, A2, A3, A4 描述，每个属性的取值为 0 或 1（0 代表否，1 代表是）：
- A1: 本学期出勤率低于80%
- A2: 期中考试存在不及格科目
- A3: 连续两次未提交课程作业
- A4: 课堂互动参与度极低

这些对象的属性向量如下：
- #01: (1,1,1,1)
- #02: (1,1,1,0)
- #03: (1,1,0,1)
- #04: (1,0,1,1)
- #05: (0,1,1,1)
- #06: (1,0,0,0)
- #07: (0,0,1,1)
- #08: (0,1,0,1)
- #09: (0,0,0,1)
- #10: (0,1,1,0)
- #11: (1,1,0,0)
- #12: (0,0,1,0)

我已秘密选择了一个布尔谓词 f（即触发"学业预警"的判定规则），该谓词依赖这4个属性 A1, A2, A3, A4，对每个对象返回 0 或 1（即该对象是否满足谓词，需要介入辅导）。该谓词可由原子命题（Ai=0 或 Ai=1）通过逻辑运算符 AND、OR、NOT 组成，且表达式的布尔深度不超过2层，总文字数不超过4个。

你的目标是通过查询推断出这个隐藏的布尔谓词，并预测哪些对象满足该谓词（即 f 返回 1 的预警学生集合）。

你可以进行以下两种查询：

1. **子集计数查询**（限定次数）：
   指定一个对象子集 S，我会告诉你：
   - m: 子集 S 的大小
   - k: 子集 S 中满足谓词 f 的对象数量
   - 剩余查询次数
   
   你可以用两种方式指定子集：
   - 显式列举对象编号（如 #01,#03,#05）
   - 提供布尔筛选表达式（如 A1=1 AND A2=0），系统会自动筛选满足条件的对象

2. **成员查询**（限定次数）：
   询问特定对象 #i 是否满足谓词 f。我会回答"是"或"否"，并告知剩余查询次数。

当你收集到足够信息后，请提交最终答案，包括：
- 布尔表达式：描述谓词 f 的逻辑结构
- 正例集合：你预测满足 f 的所有对象编号

## 查询与提交格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 子集计数查询（显式列举）：
<query_subset>#01,#03,#05</query_subset>

- 子集计数查询（布尔表达式）：
<query_subset>A1=1 AND A2=0</query_subset>

- 成员查询（例如询问对象 #05）：
<query_member>#05</query_member>

- 提交最终答案：
<answer>expression=A1=1 AND A2=1, positive_set=#01,#02,#03</answer>

注意：
- 布尔表达式中使用 AND、OR、NOT 作为逻辑运算符
- 对象编号必须带 # 前缀
- 答案中 expression 和 positive_set 必须同时提供且用逗号分隔
- 请尽可能少地使用查询次数来推断谓词
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play an "Academic Risk Warning System" deduction game. Here are the rules:

As a university counselor or academic advisor, you need to analyze 12 evaluation objects (i.e., student profiles), numbered #01 to #12. Each object is described by 4 binary attributes A1, A2, A3, A4, where each attribute has a value of 0 or 1 (0 for False, 1 for True):
- A1: Attendance rate below 80% this semester
- A2: Failed subjects in midterm exams
- A3: Missed course assignments twice consecutively
- A4: Extremely low participation in class activities

The attribute vectors for these objects are:
- #01: (1,1,1,1)
- #02: (1,1,1,0)
- #03: (1,1,0,1)
- #04: (1,0,1,1)
- #05: (0,1,1,1)
- #06: (1,0,0,0)
- #07: (0,0,1,1)
- #08: (0,1,0,1)
- #09: (0,0,0,1)
- #10: (0,1,1,0)
- #11: (1,1,0,0)
- #12: (0,0,1,0)

I have secretly chosen a Boolean predicate f (the determination rule triggering "academic warning") that depends on these 4 attributes A1, A2, A3, A4 and returns 0 or 1 for each object (whether the object satisfies the predicate and requires intervention). This predicate can be composed of atomic propositions (Ai=0 or Ai=1) using logical operators AND, OR, NOT, with Boolean depth no more than 2 layers and total literals no more than 4.

Your goal is to infer this hidden Boolean predicate through queries and predict which objects satisfy the predicate (i.e., the set of objects where f returns 1).

You can perform the following two types of queries:

1. **Subset Count Query** (limited quota):
   Specify a subset S of objects, and I will tell you:
   - m: the size of subset S
   - k: the number of objects in S that satisfy predicate f
   - remaining query count
   
   You can specify the subset in two ways:
   - Explicitly list object IDs (e.g., #01,#03,#05)
   - Provide a Boolean filter expression (e.g., A1=1 AND A2=0), and the system will automatically filter objects meeting the condition

2. **Membership Query** (limited quota):
   Ask whether a specific object #i satisfies predicate f. I will answer "Yes" or "No" and tell you the remaining query count.

When you have collected enough information, submit your final answer, including:
- Boolean expression: describing the logical structure of predicate f
- Positive set: all object IDs you predict satisfy f

## Query and Submission Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Subset count query (explicit list):
<query_subset>#01,#03,#05</query_subset>

- Subset count query (Boolean expression):
<query_subset>A1=1 AND A2=0</query_subset>

- Membership query (e.g., asking about object #05):
<query_member>#05</query_member>

- Submit final answer:
<answer>expression=A1=1 AND A2=1, positive_set=#01,#02,#03</answer>

Notes:
- Use AND, OR, NOT as logical operators in Boolean expressions
- Object IDs must have # prefix
- Both expression and positive_set must be provided in the answer, separated by comma
- Try to use as few queries as possible to infer the predicate
"""

    contextualized_rule_zh_4 = """\
我们来玩一个"工业生产次品排查"的推理游戏，规则如下：

作为产线质量控制（QC）工程师，你需要检测12个生产对象（即产品批次），编号为 #01 到 #12。每个对象由4个二元属性 A1, A2, A3, A4 描述，每个属性的取值为 0 或 1（0 代表正常，1 代表异常）：
- A1: 生产过程中核心炉温超标
- A2: 机床加工时震动幅度过大
- A3: 投入的原材料含有微量杂质
- A4: 单件加工周期超出标准时长

这些对象的属性向量如下：
- #01: (1,1,1,1)
- #02: (1,1,1,0)
- #03: (1,1,0,1)
- #04: (1,0,1,1)
- #05: (0,1,1,1)
- #06: (1,0,0,0)
- #07: (0,0,1,1)
- #08: (0,1,0,1)
- #09: (0,0,0,1)
- #10: (0,1,1,0)
- #11: (1,1,0,0)
- #12: (0,0,1,0)

我已秘密选择了一个布尔谓词 f（即判定为"残次品需报废"的质检规则），该谓词依赖这4个属性 A1, A2, A3, A4，对每个对象返回 0 或 1（即该对象是否满足谓词，被判定为次品）。该谓词可由原子命题（Ai=0 或 Ai=1）通过逻辑运算符 AND、OR、NOT 组成，且表达式的布尔深度不超过2层，总文字数不超过4个。

你的目标是通过查询推断出这个隐藏的布尔谓词，并预测哪些对象满足该谓词（即 f 返回 1 的次品批次集合）。

你可以进行以下两种查询：

1. **子集计数查询**（限定次数）：
   指定一个对象子集 S，我会告诉你：
   - m: 子集 S 的大小
   - k: 子集 S 中满足谓词 f 的对象数量
   - 剩余查询次数
   
   你可以用两种方式指定子集：
   - 显式列举对象编号（如 #01,#03,#05）
   - 提供布尔筛选表达式（如 A1=1 AND A2=0），系统会自动筛选满足条件的对象

2. **成员查询**（限定次数）：
   询问特定对象 #i 是否满足谓词 f。我会回答"是"或"否"，并告知剩余查询次数。

当你收集到足够信息后，请提交最终答案，包括：
- 布尔表达式：描述谓词 f 的逻辑结构
- 正例集合：你预测满足 f 的所有对象编号

## 查询与提交格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 子集计数查询（显式列举）：
<query_subset>#01,#03,#05</query_subset>

- 子集计数查询（布尔表达式）：
<query_subset>A1=1 AND A2=0</query_subset>

- 成员查询（例如询问对象 #05）：
<query_member>#05</query_member>

- 提交最终答案：
<answer>expression=A1=1 AND A2=1, positive_set=#01,#02,#03</answer>

注意：
- 布尔表达式中使用 AND、OR、NOT 作为逻辑运算符
- 对象编号必须带 # 前缀
- 答案中 expression 和 positive_set 必须同时提供且用逗号分隔
- 请尽可能少地使用查询次数来推断谓词
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's play an "Industrial Defect Troubleshooting" deduction game. Here are the rules:

As a production Quality Control (QC) engineer, you need to inspect 12 production objects (i.e., product batches), numbered #01 to #12. Each object is described by 4 binary attributes A1, A2, A3, A4, where each attribute has a value of 0 or 1 (0 for Normal, 1 for Abnormal):
- A1: Core furnace temperature exceeded limits during production
- A2: Excessive vibration during machining
- A3: Trace impurities detected in raw materials
- A4: Cycle time for single part exceeded standard duration

The attribute vectors for these objects are:
- #01: (1,1,1,1)
- #02: (1,1,1,0)
- #03: (1,1,0,1)
- #04: (1,0,1,1)
- #05: (0,1,1,1)
- #06: (1,0,0,0)
- #07: (0,0,1,1)
- #08: (0,1,0,1)
- #09: (0,0,0,1)
- #10: (0,1,1,0)
- #11: (1,1,0,0)
- #12: (0,0,1,0)

I have secretly chosen a Boolean predicate f (the quality inspection rule determining "defective to be scrapped") that depends on these 4 attributes A1, A2, A3, A4 and returns 0 or 1 for each object (whether the object satisfies the predicate and is deemed defective). This predicate can be composed of atomic propositions (Ai=0 or Ai=1) using logical operators AND, OR, NOT, with Boolean depth no more than 2 layers and total literals no more than 4.

Your goal is to infer this hidden Boolean predicate through queries and predict which objects satisfy the predicate (i.e., the set of objects where f returns 1).

You can perform the following two types of queries:

1. **Subset Count Query** (limited quota):
   Specify a subset S of objects, and I will tell you:
   - m: the size of subset S
   - k: the number of objects in S that satisfy predicate f
   - remaining query count
   
   You can specify the subset in two ways:
   - Explicitly list object IDs (e.g., #01,#03,#05)
   - Provide a Boolean filter expression (e.g., A1=1 AND A2=0), and the system will automatically filter objects meeting the condition

2. **Membership Query** (limited quota):
   Ask whether a specific object #i satisfies predicate f. I will answer "Yes" or "No" and tell you the remaining query count.

When you have collected enough information, submit your final answer, including:
- Boolean expression: describing the logical structure of predicate f
- Positive set: all object IDs you predict satisfy f

## Query and Submission Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Subset count query (explicit list):
<query_subset>#01,#03,#05</query_subset>

- Subset count query (Boolean expression):
<query_subset>A1=1 AND A2=0</query_subset>

- Membership query (e.g., asking about object #05):
<query_member>#05</query_member>

- Submit final answer:
<answer>expression=A1=1 AND A2=1, positive_set=#01,#02,#03</answer>

Notes:
- Use AND, OR, NOT as logical operators in Boolean expressions
- Object IDs must have # prefix
- Both expression and positive_set must be provided in the answer, separated by comma
- Try to use as few queries as possible to infer the predicate
"""

    contextualized_rule_zh_5 = """\
我们来玩一个"刑事加重处罚情节认定"的推理游戏，规则如下：

作为资深法官或检察官，你需要审查12个司法对象（即刑事案卷），编号为 #01 到 #12。每个对象由4个二元属性 A1, A2, A3, A4 描述，每个属性的取值为 0 或 1（0 代表不具备，1 代表具备）：
- A1: 犯罪嫌疑人存在明显主观故意
- A2: 违法行为造成了严重社会危害后果
- A3: 犯罪嫌疑人曾有刑事受罚前科
- A4: 案发现场缺乏直接目击证人

这些对象的属性向量如下：
- #01: (1,1,1,1)
- #02: (1,1,1,0)
- #03: (1,1,0,1)
- #04: (1,0,1,1)
- #05: (0,1,1,1)
- #06: (1,0,0,0)
- #07: (0,0,1,1)
- #08: (0,1,0,1)
- #09: (0,0,0,1)
- #10: (0,1,1,0)
- #11: (1,1,0,0)
- #12: (0,0,1,0)

我已秘密选择了一个布尔谓词 f（即适用"加重处罚"的法律量刑规则），该谓词依赖这4个属性 A1, A2, A3, A4，对每个对象返回 0 或 1（即该对象是否满足谓词，应当加重量刑）。该谓词可由原子命题（Ai=0 或 Ai=1）通过逻辑运算符 AND、OR、NOT 组成，且表达式的布尔深度不超过2层，总文字数不超过4个。

你的目标是通过查询推断出这个隐藏的布尔谓词，并预测哪些对象满足该谓词（即 f 返回 1 的加重处罚案卷集合）。

你可以进行以下两种查询：

1. **子集计数查询**（限定次数）：
   指定一个对象子集 S，我会告诉你：
   - m: 子集 S 的大小
   - k: 子集 S 中满足谓词 f 的对象数量
   - 剩余查询次数
   
   你可以用两种方式指定子集：
   - 显式列举对象编号（如 #01,#03,#05）
   - 提供布尔筛选表达式（如 A1=1 AND A2=0），系统会自动筛选满足条件的对象

2. **成员查询**（限定次数）：
   询问特定对象 #i 是否满足谓词 f。我会回答"是"或"否"，并告知剩余查询次数。

当你收集到足够信息后，请提交最终答案，包括：
- 布尔表达式：描述谓词 f 的逻辑结构
- 正例集合：你预测满足 f 的所有对象编号

## 查询与提交格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 子集计数查询（显式列举）：
<query_subset>#01,#03,#05</query_subset>

- 子集计数查询（布尔表达式）：
<query_subset>A1=1 AND A2=0</query_subset>

- 成员查询（例如询问对象 #05）：
<query_member>#05</query_member>

- 提交最终答案：
<answer>expression=A1=1 AND A2=1, positive_set=#01,#02,#03</answer>

注意：
- 布尔表达式中使用 AND、OR、NOT 作为逻辑运算符
- 对象编号必须带 # 前缀
- 答案中 expression 和 positive_set 必须同时提供且用逗号分隔
- 请尽可能少地使用查询次数来推断谓词
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's play an "Aggravated Sentencing Circumstances" deduction game. Here are the rules:

As a senior judge or prosecutor, you need to review 12 judicial objects (i.e., criminal case files), numbered #01 to #12. Each object is described by 4 binary attributes A1, A2, A3, A4, where each attribute has a value of 0 or 1 (0 for Absent, 1 for Present):
- A1: Suspect exhibited obvious subjective intent
- A2: Illegal behavior caused severe social harm
- A3: Suspect has a prior criminal record
- A4: Lack of direct eyewitnesses at the crime scene

The attribute vectors for these objects are:
- #01: (1,1,1,1)
- #02: (1,1,1,0)
- #03: (1,1,0,1)
- #04: (1,0,1,1)
- #05: (0,1,1,1)
- #06: (1,0,0,0)
- #07: (0,0,1,1)
- #08: (0,1,0,1)
- #09: (0,0,0,1)
- #10: (0,1,1,0)
- #11: (1,1,0,0)
- #12: (0,0,1,0)

I have secretly chosen a Boolean predicate f (the sentencing rule applying "aggravated punishment") that depends on these 4 attributes A1, A2, A3, A4 and returns 0 or 1 for each object (whether the object satisfies the predicate and should receive an aggravated sentence). This predicate can be composed of atomic propositions (Ai=0 or Ai=1) using logical operators AND, OR, NOT, with Boolean depth no more than 2 layers and total literals no more than 4.

Your goal is to infer this hidden Boolean predicate through queries and predict which objects satisfy the predicate (i.e., the set of objects where f returns 1).

You can perform the following two types of queries:

1. **Subset Count Query** (limited quota):
   Specify a subset S of objects, and I will tell you:
   - m: the size of subset S
   - k: the number of objects in S that satisfy predicate f
   - remaining query count
   
   You can specify the subset in two ways:
   - Explicitly list object IDs (e.g., #01,#03,#05)
   - Provide a Boolean filter expression (e.g., A1=1 AND A2=0), and the system will automatically filter objects meeting the condition

2. **Membership Query** (limited quota):
   Ask whether a specific object #i satisfies predicate f. I will answer "Yes" or "No" and tell you the remaining query count.

When you have collected enough information, submit your final answer, including:
- Boolean expression: describing the logical structure of predicate f
- Positive set: all object IDs you predict satisfy f

## Query and Submission Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Subset count query (explicit list):
<query_subset>#01,#03,#05</query_subset>

- Subset count query (Boolean expression):
<query_subset>A1=1 AND A2=0</query_subset>

- Membership query (e.g., asking about object #05):
<query_member>#05</query_member>

- Submit final answer:
<answer>expression=A1=1 AND A2=1, positive_set=#01,#02,#03</answer>

Notes:
- Use AND, OR, NOT as logical operators in Boolean expressions
- Object IDs must have # prefix
- Both expression and positive_set must be provided in the answer, separated by comma
- Try to use as few queries as possible to infer the predicate
"""

    tags = ["answer", "query_subset", "query_member"]

    # 难度配置：
    # 1 (简单)        - 单属性谓词: A1=1, 子集查询9次, 成员查询3次
    # 2 (中等偏下)    - 简单AND: A1=1 AND A2=1, 子集查询8次, 成员查询3次
    # 3 (中等偏上)    - OR组合: A1=1 OR A3=1, 子集查询7次, 成员查询2次
    # 4 (较难)        - 带NOT: A1=1 AND (NOT A2=1), 子集查询6次, 成员查询2次
    # 5 (难)          - 复杂组合: (A1=1 OR A2=1) AND (A3=1 OR A4=1), 子集查询5次, 成员查询1次

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "expression": "A1=1",
                "positive_set": ["#01", "#02", "#03", "#04", "#06", "#11"],
                "max_subset_queries": 9,
                "max_member_queries": 3,
            },
            2: {
                "expression": "A1=1 AND A2=1",
                "positive_set": ["#01", "#02", "#03", "#11"],
                "max_subset_queries": 8,
                "max_member_queries": 3,
            },
            3: {
                "expression": "A1=1 OR A3=1",
                "positive_set": ["#01", "#02", "#03", "#04", "#05", "#06", "#07", "#10", "#11", "#12"],
                "max_subset_queries": 7,
                "max_member_queries": 2,
            },
            4: {
                "expression": "A1=1 AND (NOT A2=1)",
                "positive_set": ["#04", "#06"],
                "max_subset_queries": 6,
                "max_member_queries": 2,
            },
            5: {
                "expression": "(A1=1 OR A2=1) AND (A3=1 OR A4=1)",
                "positive_set": ["#01", "#02", "#03", "#04", "#05", "#07", "#08", "#10"],
                "max_subset_queries": 5,
                "max_member_queries": 1,
            },
        },
        "en": {
            1: {
                "expression": "A1=1",
                "positive_set": ["#01", "#02", "#03", "#04", "#06", "#11"],
                "max_subset_queries": 9,
                "max_member_queries": 3,
            },
            2: {
                "expression": "A1=1 AND A2=1",
                "positive_set": ["#01", "#02", "#03", "#11"],
                "max_subset_queries": 8,
                "max_member_queries": 3,
            },
            3: {
                "expression": "A1=1 OR A3=1",
                "positive_set": ["#01", "#02", "#03", "#04", "#05", "#06", "#07", "#10", "#11", "#12"],
                "max_subset_queries": 7,
                "max_member_queries": 2,
            },
            4: {
                "expression": "A1=1 AND (NOT A2=1)",
                "positive_set": ["#04", "#06"],
                "max_subset_queries": 6,
                "max_member_queries": 2,
            },
            5: {
                "expression": "(A1=1 OR A2=1) AND (A3=1 OR A4=1)",
                "positive_set": ["#01", "#02", "#03", "#04", "#05", "#07", "#08", "#10"],
                "max_subset_queries": 5,
                "max_member_queries": 1,
            },
        },
    }

    # 固定的12个对象的属性向量
    OBJECTS = {
        "#01": (1, 1, 1, 1),
        "#02": (1, 1, 1, 0),
        "#03": (1, 1, 0, 1),
        "#04": (1, 0, 1, 1),
        "#05": (0, 1, 1, 1),
        "#06": (1, 0, 0, 0),
        "#07": (0, 0, 1, 1),
        "#08": (0, 1, 0, 1),
        "#09": (0, 0, 0, 1),
        "#10": (0, 1, 1, 0),
        "#11": (1, 1, 0, 0),
        "#12": (0, 0, 1, 0),
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏配置"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 防御性类型转换

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 设置真实的布尔表达式和正例集合
        self.true_expression = cfg["expression"]
        self.true_positive_set = set(cfg["positive_set"])
        
        # 初始化查询次数限制
        self.max_subset_queries = cfg["max_subset_queries"]
        self.max_member_queries = cfg["max_member_queries"]
        self.subset_query_count = 0
        self.member_query_count = 0
        
        # 基类 _init_rule 需要用到 _game_info
        self._game_info = {}

    def _evaluate_expression(self, expr: str, obj_id: str) -> bool:
        """
        计算布尔表达式对指定对象的值
        expr: 布尔表达式字符串，如 "A1=1 AND A2=0"
        obj_id: 对象编号，如 "#01"
        返回: True 或 False
        """
        if obj_id not in self.OBJECTS:
            raise ValueError(f"Invalid object ID: {obj_id}")
        
        attrs = self.OBJECTS[obj_id]
        
        # 替换属性值（从大到小替换避免 A1 匹配 A10 之类的问题）
        eval_expr = expr
        for i in range(4, 0, -1):
            eval_expr = eval_expr.replace(f"A{i}", str(attrs[i - 1]))
        
        # 替换逻辑运算符（先替换大写，保留已有小写）
        eval_expr = eval_expr.replace("AND", "and")
        eval_expr = eval_expr.replace("OR", "or")
        eval_expr = eval_expr.replace("NOT", "not")
        
        # 使用正则精确替换单个 = 为 ==，避免把已有的 == 变成 ====
        eval_expr = re.sub(r'(?<!=)=(?!=)', '==', eval_expr)
        
        try:
            result = eval(eval_expr)
            return bool(result)
        except Exception:
            raise ValueError(f"Invalid expression: {expr}")

    def _parse_subset(self, subset_str: str) -> set:
        """
        解析子集字符串，支持显式列举和布尔表达式两种方式
        返回: 对象编号的集合
        """
        subset_str = subset_str.strip()
        
        # 检查是否是显式列举（包含 # 符号）
        if "#" in subset_str:
            # 显式列举模式
            ids = [s.strip() for s in subset_str.split(",")]
            result = set()
            for obj_id in ids:
                if obj_id not in self.OBJECTS:
                    raise ValueError(f"Invalid object ID: {obj_id}")
                result.add(obj_id)
            return result
        else:
            # 布尔表达式模式
            result = set()
            for obj_id in self.OBJECTS:
                try:
                    if self._evaluate_expression(subset_str, obj_id):
                        result.add(obj_id)
                except:
                    raise ValueError(f"Invalid boolean expression: {subset_str}")
            return result

    def _check_expression_equivalence(self, expr: str) -> bool:
        """
        检查两个布尔表达式在所有12个对象上是否等价
        """
        try:
            for obj_id in self.OBJECTS:
                if self._evaluate_expression(expr, obj_id) != (obj_id in self.true_positive_set):
                    return False
            return True
        except:
            return False

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        # 解析答案: expression=..., positive_set=...
        parts = raw_ans.split(",")
        ans_dict = {}
        
        current_key = None
        current_value = []
        
        for part in parts:
            if "=" in part and current_key is None:
                # 首次遇到键值对
                k, v = part.split("=", 1)
                current_key = k.strip()
                current_value = [v.strip()]
            elif "=" in part and current_key is not None:
                # 新的键值对，保存之前的
                ans_dict[current_key] = ",".join(current_value)
                k, v = part.split("=", 1)
                current_key = k.strip()
                current_value = [v.strip()]
            else:
                # 继续当前值
                if current_key:
                    current_value.append(part.strip())
        
        # 保存最后一个键值对
        if current_key:
            ans_dict[current_key] = ",".join(current_value)
        
        if "expression" not in ans_dict or "positive_set" not in ans_dict:
            return False
        
        submitted_expr = ans_dict["expression"].strip()
        submitted_set_str = ans_dict["positive_set"].strip()
        
        # 解析提交的正例集合
        submitted_set = set()
        for obj_id in submitted_set_str.split(","):
            obj_id = obj_id.strip()
            if obj_id:
                submitted_set.add(obj_id)
        
        # 检查表达式等价性
        expr_correct = self._check_expression_equivalence(submitted_expr)
        
        # 检查正例集合
        set_correct = (submitted_set == self.true_positive_set)
        
        return expr_correct and set_correct

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        # 优先处理子集计数查询
        if "query_subset" in parsed_info:
            if self.subset_query_count >= self.max_subset_queries:
                if self.config.language == "zh":
                    return f"错误：子集计数查询次数已用尽（{self.max_subset_queries}/{self.max_subset_queries}）"
                else:
                    return f"Error: Subset count queries exhausted ({self.max_subset_queries}/{self.max_subset_queries})"
            
            try:
                subset_str = parsed_info["query_subset"].strip()
                subset = self._parse_subset(subset_str)
                
                if not subset:
                    if self.config.language == "zh":
                        return "错误：子集为空"
                    else:
                        return "Error: Subset is empty"
                
                # 计算满足谓词的对象数
                m = len(subset)
                k = sum(1 for obj_id in subset if obj_id in self.true_positive_set)
                
                self.subset_query_count += 1
                remaining = self.max_subset_queries - self.subset_query_count
                
                if self.config.language == "zh":
                    return f"子集大小 m={m}，满足谓词的对象数 k={k}。剩余子集查询次数：{remaining}"
                else:
                    return f"Subset size m={m}, objects satisfying predicate k={k}. Remaining subset queries: {remaining}"
                    
            except Exception as e:
                if self.config.language == "zh":
                    return f"错误：{str(e)}"
                else:
                    return f"Error: {str(e)}"

        # 处理成员查询
        elif "query_member" in parsed_info:
            if self.member_query_count >= self.max_member_queries:
                if self.config.language == "zh":
                    return f"错误：成员查询次数已用尽（{self.max_member_queries}/{self.max_member_queries}）"
                else:
                    return f"Error: Membership queries exhausted ({self.max_member_queries}/{self.max_member_queries})"
            
            obj_id = parsed_info["query_member"].strip()
            
            if obj_id not in self.OBJECTS:
                if self.config.language == "zh":
                    return "错误：对象编号无效"
                else:
                    return "Error: Invalid object ID"
            
            result = yes_res if obj_id in self.true_positive_set else no_res
            self.member_query_count += 1
            remaining = self.max_member_queries - self.member_query_count
            
            if self.config.language == "zh":
                return f"{result}。剩余成员查询次数：{remaining}"
            else:
                return f"{result}. Remaining membership queries: {remaining}"

        else:
            raise ValueError("No valid query tag found.")
    
    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        注意：剩余次数使用递减方式模拟真实对话。
        """
        results = []
        is_zh = self.config.language == "zh"
        yes_str = "是" if is_zh else "Yes"
        no_str = "否" if is_zh else "No"
        
        member_idx = 0
        subset_idx = 0
        
        # 1. 枚举所有成员查询 (Membership Query)
        for obj_id in sorted(self.OBJECTS.keys()):
            query = f"<query_member>{obj_id}</query_member>"
            
            is_positive = obj_id in self.true_positive_set
            res_txt = yes_str if is_positive else no_str
            
            rem_mem = max(0, self.max_member_queries - member_idx - 1)
            member_idx += 1
            
            if is_zh:
                ans = f"{res_txt}。剩余成员查询次数：{rem_mem}"
            else:
                ans = f"{res_txt}. Remaining membership queries: {rem_mem}"
                
            results.append({"query": query, "answer": ans})

        # 2. 枚举典型子集查询 (Subset Query)
        # 2.1 枚举单对象显式列表
        for obj_id in sorted(self.OBJECTS.keys()):
            query = f"<query_subset>{obj_id}</query_subset>"
            m = 1
            k = 1 if obj_id in self.true_positive_set else 0
            
            rem_sub = max(0, self.max_subset_queries - subset_idx - 1)
            subset_idx += 1
            
            if is_zh:
                ans = f"子集大小 m={m}，满足谓词的对象数 k={k}。剩余子集查询次数：{rem_sub}"
            else:
                ans = f"Subset size m={m}, objects satisfying predicate k={k}. Remaining subset queries: {rem_sub}"
                
            results.append({"query": query, "answer": ans})
            
        # 2.2 枚举原子布尔属性表达式
        for i in range(1, 5):
            for val in [0, 1]:
                expr = f"A{i}={val}"
                query = f"<query_subset>{expr}</query_subset>"
                
                try:
                    subset = self._parse_subset(expr)
                    m = len(subset)
                    k = sum(1 for oid in subset if oid in self.true_positive_set)
                    
                    rem_sub = max(0, self.max_subset_queries - subset_idx - 1)
                    subset_idx += 1
                    
                    if is_zh:
                        ans = f"子集大小 m={m}，满足谓词的对象数 k={k}。剩余子集查询次数：{rem_sub}"
                    else:
                        ans = f"Subset size m={m}, objects satisfying predicate k={k}. Remaining subset queries: {rem_sub}"
                        
                    results.append({"query": query, "answer": ans})
                except:
                    continue

        return results

    def _cf_make_wrong(self, correct: str) -> str:
        """生成错误的响应用于反事实干预"""
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct and "否" not in correct:
                return correct.replace("是", "否", 1)
            elif "否" in correct and "是" not in correct:
                return correct.replace("否", "是", 1)
        else:
            if re.search(r'\bYes\b', correct) and not re.search(r'\bNo\b', correct):
                return re.sub(r'\bYes\b', 'No', correct, count=1)
            elif re.search(r'\bNo\b', correct) and not re.search(r'\bYes\b', correct):
                return re.sub(r'\bNo\b', 'Yes', correct, count=1)
        
        # 对于子集计数查询，修改 k 值
        k_match = re.search(r'k=(\d+)', correct)
        if k_match:
            old_k = int(k_match.group(1))
            new_k = old_k + 1 if old_k == 0 else old_k - 1
            return correct.replace(f"k={old_k}", f"k={new_k}", 1)
        
        return correct + "_WRONG"