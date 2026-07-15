from .base import Game
import re
import itertools

class SetRuleInferenceGame(Game):

    game_rule_zh = """\
我们现在来玩一个"集合规则推理"游戏，规则如下：

游戏设定了一个包含 8 个元素的集合 U，编号为 1 到 8。每个元素具有三个公开的二值属性 A、B、C，取值为 0 或 1。8 个元素覆盖所有属性组合，编号对应如下：
  编号 1: (A=1, B=1, C=1)
  编号 2: (A=1, B=1, C=0)
  编号 3: (A=1, B=0, C=1)
  编号 4: (A=1, B=0, C=0)
  编号 5: (A=0, B=1, C=1)
  编号 6: (A=0, B=1, C=0)
  编号 7: (A=0, B=0, C=1)
  编号 8: (A=0, B=0, C=0)

我已秘密选择了一个判定规则 f，该规则从四个候选规则中选出，定义了集合 U 中"正例"元素的子集 P。四个候选规则公开如下：
  R1: 正例当且仅当 A=1
  R2: 正例当且仅当 B=1
  R3: 正例当且仅当 C=1
  R4: 正例当且仅当 (A + B + C) mod 2 = 1（属性之和为奇数）

你的目标是通过查询推断出实际采用的规则类型以及所有正例元素的编号集合。

你可以反复提出以下三类查询（每次仅限一个查询）：

1. **计数查询**：询问某个子集 S 中有多少个正例元素。我会返回一个非负整数。
2. **存在性查询**：询问某个子集 S 中是否至少存在一个正例元素。我会返回"是"或"否"。
3. **比较查询**：询问两个互不相交的子集 S 和 T 中，哪个包含更多正例元素。我会返回"S更多"、"T更多"或"相等"。

你可以用以下两种方式定义子集：

**方式一：列表式**
直接列出元素编号，例如：S={{1,3,5}}

**方式二：条件式**
用属性的布尔条件定义，支持与、或、非运算，例如：
- "A=1 且 B=0"
- "C=0 或 A=1"
- "非(B=1 且 C=1)"

每次只能包含一个查询标签，使用以下 XML 格式：

- **计数查询**（例如查询编号 1,2,3 组成的子集）：
<query_count>1,2,3</query_count>

或使用条件式：
<query_count>A=1 且 B=1</query_count>

- **存在性查询**（例如查询编号 5,6,7 组成的子集）：
<query_exist>5,6,7</query_exist>

或使用条件式：
<query_exist>C=1</query_exist>

- **比较查询**（例如比较子集 {{1,2}} 和 {{5,6}}）：
<query_compare>S={{1,2}}; T={{5,6}}</query_compare>

或使用条件式：
<query_compare>S={{A=1}}; T={{B=0}}</query_compare>

注意：比较查询中的两个子集必须互不相交。

当你收集到足够信息后，请提交最终答案，格式如下：

<answer>rule=R1, positive=1,2,3,4</answer>

其中 rule 为规则类型（R1、R2、R3 或 R4），positive 为所有正例元素的编号（用逗号分隔，顺序不限）。

若答案错误或格式不符，游戏失败。请尽可能用少的查询次数完成推理。
"""

    game_rule_en = """\
Let's play a "Set Rule Inference" game. Here are the rules:

The game defines a set U containing 8 elements, numbered 1 to 8. Each element has three public binary attributes A, B, C, with values 0 or 1. The 8 elements cover all attribute combinations, with the following mapping:
  ID 1: (A=1, B=1, C=1)
  ID 2: (A=1, B=1, C=0)
  ID 3: (A=1, B=0, C=1)
  ID 4: (A=1, B=0, C=0)
  ID 5: (A=0, B=1, C=1)
  ID 6: (A=0, B=1, C=0)
  ID 7: (A=0, B=0, C=1)
  ID 8: (A=0, B=0, C=0)

I have secretly selected a judgment rule f from four candidate rules, which defines a subset P of "positive" elements in U. The four candidate rules are publicly known:
  R1: Positive if and only if A=1
  R2: Positive if and only if B=1
  R3: Positive if and only if C=1
  R4: Positive if and only if (A + B + C) mod 2 = 1 (sum of attributes is odd)

Your goal is to infer the actual rule type and the set of all positive element IDs through queries.

You can repeatedly make one of the following three types of queries (one query per turn):

1. **Count Query**: Ask how many positive elements are in a subset S. I will return a non-negative integer.
2. **Existence Query**: Ask whether at least one positive element exists in a subset S. I will return "Yes" or "No".
3. **Comparison Query**: Ask which of two disjoint subsets S and T contains more positive elements. I will return "S more", "T more", or "Equal".

You can define subsets in two ways:

**Method 1: List-based**
Directly list element IDs, e.g., S={{1,3,5}}

**Method 2: Condition-based**
Use boolean conditions on attributes, supporting AND, OR, NOT operations, e.g.:
- "A=1 and B=0"
- "C=0 or A=1"
- "not(B=1 and C=1)"

Each turn must contain only one query tag, using the following XML format:

- **Count Query** (e.g., querying subset with IDs 1,2,3):
<query_count>1,2,3</query_count>

Or using conditions:
<query_count>A=1 and B=1</query_count>

- **Existence Query** (e.g., querying subset with IDs 5,6,7):
<query_exist>5,6,7</query_exist>

Or using conditions:
<query_exist>C=1</query_exist>

- **Comparison Query** (e.g., comparing subsets {{1,2}} and {{5,6}}):
<query_compare>S={{1,2}}; T={{5,6}}</query_compare>

Or using conditions:
<query_compare>S={{A=1}}; T={{B=0}}</query_compare>

Note: The two subsets in a comparison query must be disjoint.

When you have gathered enough information, submit your final answer in this format:

<answer>rule=R1, positive=1,2,3,4</answer>

Where rule is the rule type (R1, R2, R3, or R4), and positive lists all positive element IDs (comma-separated, order does not matter).

If the answer is incorrect or the format is invalid, the game fails. Try to complete the inference with as few queries as possible.
"""

    contextualized_rule_zh_1 = """\
欢迎使用【智能交通调度控制系统】。在本系统测试中，你需要推断出当前激活的交通调度策略。

交通管理中心设定了一个包含 8 个受控路口（元素）的集合 U，编号为 1 到 8。每个路口具有三个公开的传感器二值属性 A（主干道）、B（高峰期）、C（优先车辆），取值为 0 或 1。8 个路口覆盖所有状态组合，编号对应如下：
  编号 1: (A=1, B=1, C=1)
  编号 2: (A=1, B=1, C=0)
  编号 3: (A=1, B=0, C=1)
  编号 4: (A=1, B=0, C=0)
  编号 5: (A=0, B=1, C=1)
  编号 6: (A=0, B=1, C=0)
  编号 7: (A=0, B=0, C=1)
  编号 8: (A=0, B=0, C=0)

管理中心已秘密选择了一个判定规则 f，该规则从四个候选规则中选出，定义了集合 U 中触发"绿灯优先放行"（正例）元素的子集 P。四个候选规则公开如下：
  R1: 正例当且仅当 A=1
  R2: 正例当且仅当 B=1
  R3: 正例当且仅当 C=1
  R4: 正例当且仅当 (A + B + C) mod 2 = 1（属性之和为奇数，复杂均衡策略）

你的目标是通过查询推断出实际采用的规则类型以及所有正例元素的编号集合。

你可以反复提出以下三类查询（每次仅限一个查询）：

1. **计数查询**：询问某个子集 S 中有多少个正例元素。我会返回一个非负整数。
2. **存在性查询**：询问某个子集 S 中是否至少存在一个正例元素。我会返回"是"或"否"。
3. **比较查询**：询问两个互不相交的子集 S 和 T 中，哪个包含更多正例元素。我会返回"S更多"、"T更多"或"相等"。

你可以用以下两种方式定义子集：

**方式一：列表式**
直接列出元素编号，例如：S={{1,3,5}}

**方式二：条件式**
用属性的布尔条件定义，支持与、或、非运算，例如：
- "A=1 且 B=0"
- "C=0 或 A=1"
- "非(B=1 且 C=1)"

每次只能包含一个查询标签，使用以下 XML 格式：

- **计数查询**（例如查询编号 1,2,3 组成的子集）：
<query_count>1,2,3</query_count>

或使用条件式：
<query_count>A=1 且 B=1</query_count>

- **存在性查询**（例如查询编号 5,6,7 组成的子集）：
<query_exist>5,6,7</query_exist>

或使用条件式：
<query_exist>C=1</query_exist>

- **比较查询**（例如比较子集 {{1,2}} 和 {{5,6}}）：
<query_compare>S={{1,2}}; T={{5,6}}</query_compare>

或使用条件式：
<query_compare>S={{A=1}}; T={{B=0}}</query_compare>

注意：比较查询中的两个子集必须互不相交。

当你收集到足够信息后，请提交最终答案，格式如下：

<answer>rule=R1, positive=1,2,3,4</answer>

其中 rule 为规则类型（R1、R2、R3 或 R4），positive 为所有正例元素的编号（用逗号分隔，顺序不限）。

若答案错误或格式不符，测试失败。请尽可能用少的查询次数完成推理。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the [Intelligent Traffic Network Dispatch System]. You need to infer the currently active traffic signal control strategy.

The dispatch center defines a set U containing 8 controlled intersections (elements), numbered 1 to 8. Each intersection has three public binary sensor attributes A (Main Road), B (Peak Hour), C (Priority Vehicle), with values 0 or 1. The 8 intersections cover all attribute combinations, with the following mapping:
  ID 1: (A=1, B=1, C=1)
  ID 2: (A=1, B=1, C=0)
  ID 3: (A=1, B=0, C=1)
  ID 4: (A=1, B=0, C=0)
  ID 5: (A=0, B=1, C=1)
  ID 6: (A=0, B=1, C=0)
  ID 7: (A=0, B=0, C=1)
  ID 8: (A=0, B=0, C=0)

The center has secretly selected a judgment rule f from four candidate rules, which defines a subset P of "Green Light Priority" (positive) elements in U. The four candidate rules are publicly known:
  R1: Positive if and only if A=1
  R2: Positive if and only if B=1
  R3: Positive if and only if C=1
  R4: Positive if and only if (A + B + C) mod 2 = 1 (sum of attributes is odd)

Your goal is to infer the actual rule type and the set of all positive element IDs through queries.

You can repeatedly make one of the following three types of queries (one query per turn):

1. **Count Query**: Ask how many positive elements are in a subset S. I will return a non-negative integer.
2. **Existence Query**: Ask whether at least one positive element exists in a subset S. I will return "Yes" or "No".
3. **Comparison Query**: Ask which of two disjoint subsets S and T contains more positive elements. I will return "S more", "T more", or "Equal".

You can define subsets in two ways:

**Method 1: List-based**
Directly list element IDs, e.g., S={{1,3,5}}

**Method 2: Condition-based**
Use boolean conditions on attributes, supporting AND, OR, NOT operations, e.g.:
- "A=1 and B=0"
- "C=0 or A=1"
- "not(B=1 and C=1)"

Each turn must contain only one query tag, using the following XML format:

- **Count Query** (e.g., querying subset with IDs 1,2,3):
<query_count>1,2,3</query_count>

Or using conditions:
<query_count>A=1 and B=1</query_count>

- **Existence Query** (e.g., querying subset with IDs 5,6,7):
<query_exist>5,6,7</query_exist>

Or using conditions:
<query_exist>C=1</query_exist>

- **Comparison Query** (e.g., comparing subsets {{1,2}} and {{5,6}}):
<query_compare>S={{1,2}}; T={{5,6}}</query_compare>

Or using conditions:
<query_compare>S={{A=1}}; T={{B=0}}</query_compare>

Note: The two subsets in a comparison query must be disjoint.

When you have gathered enough information, submit your final answer in this format:

<answer>rule=R1, positive=1,2,3,4</answer>

Where rule is the rule type (R1, R2, R3, or R4), and positive lists all positive element IDs (comma-separated, order does not matter).

If the answer is incorrect or the format is invalid, the game fails. Try to complete the inference with as few queries as possible.
"""

    contextualized_rule_zh_2 = """\
欢迎使用【临床试验智能辅诊系统】。在本场景中，你需要推断出当前靶向药物的临床用药指征规则。

医疗专家组设定了一个包含 8 名临床患者（元素）的集合 U，编号为 1 到 8。每名患者具有三个公开的临床二值属性 A（基因突变阳性）、B（有基础疾病）、C（高龄特征），取值为 0 或 1。8 名患者覆盖所有病理特征组合，编号对应如下：
  编号 1: (A=1, B=1, C=1)
  编号 2: (A=1, B=1, C=0)
  编号 3: (A=1, B=0, C=1)
  编号 4: (A=1, B=0, C=0)
  编号 5: (A=0, B=1, C=1)
  编号 6: (A=0, B=1, C=0)
  编号 7: (A=0, B=0, C=1)
  编号 8: (A=0, B=0, C=0)

专家组已秘密选择了一个判定规则 f，该规则从四个候选规则中选出，定义了集合 U 中符合"特效靶向药用药指征"（正例）元素的子集 P。四个候选规则公开如下：
  R1: 正例当且仅当 A=1
  R2: 正例当且仅当 B=1
  R3: 正例当且仅当 C=1
  R4: 正例当且仅当 (A + B + C) mod 2 = 1（综合风险指数奇数校验）

你的目标是通过查询推断出实际采用的规则类型以及所有正例元素的编号集合。

你可以反复提出以下三类查询（每次仅限一个查询）：

1. **计数查询**：询问某个子集 S 中有多少个正例元素。我会返回一个非负整数。
2. **存在性查询**：询问某个子集 S 中是否至少存在一个正例元素。我会返回"是"或"否"。
3. **比较查询**：询问两个互不相交的子集 S 和 T 中，哪个包含更多正例元素。我会返回"S更多"、"T更多"或"相等"。

你可以用以下两种方式定义子集：

**方式一：列表式**
直接列出元素编号，例如：S={{1,3,5}}

**方式二：条件式**
用属性的布尔条件定义，支持与、或、非运算，例如：
- "A=1 且 B=0"
- "C=0 或 A=1"
- "非(B=1 且 C=1)"

每次只能包含一个查询标签，使用以下 XML 格式：

- **计数查询**（例如查询编号 1,2,3 组成的子集）：
<query_count>1,2,3</query_count>

或使用条件式：
<query_count>A=1 且 B=1</query_count>

- **存在性查询**（例如查询编号 5,6,7 组成的子集）：
<query_exist>5,6,7</query_exist>

或使用条件式：
<query_exist>C=1</query_exist>

- **比较查询**（例如比较子集 {{1,2}} 和 {{5,6}}）：
<query_compare>S={{1,2}}; T={{5,6}}</query_compare>

或使用条件式：
<query_compare>S={{A=1}}; T={{B=0}}</query_compare>

注意：比较查询中的两个子集必须互不相交。

当你收集到足够信息后，请提交最终答案，格式如下：

<answer>rule=R1, positive=1,2,3,4</answer>

其中 rule 为规则类型（R1、R2、R3 或 R4），positive 为所有正例元素的编号（用逗号分隔，顺序不限）。

若答案错误或格式不符，测试失败。请尽可能用少的查询次数完成推理。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the [Clinical Trial Intelligent Diagnosis System]. You need to infer the clinical indication rules for a targeted drug.

The medical expert panel defines a set U containing 8 clinical patients (elements), numbered 1 to 8. Each patient has three public binary clinical attributes A (Gene Mutation Positive), B (Underlying Disease), C (Advanced Age), with values 0 or 1. The 8 patients cover all pathological combinations, with the following mapping:
  ID 1: (A=1, B=1, C=1)
  ID 2: (A=1, B=1, C=0)
  ID 3: (A=1, B=0, C=1)
  ID 4: (A=1, B=0, C=0)
  ID 5: (A=0, B=1, C=1)
  ID 6: (A=0, B=1, C=0)
  ID 7: (A=0, B=0, C=1)
  ID 8: (A=0, B=0, C=0)

The expert panel has secretly selected a judgment rule f from four candidate rules, which defines a subset P of elements meeting the "Targeted Therapy Indication" (positive) elements in U. The four candidate rules are publicly known:
  R1: Positive if and only if A=1
  R2: Positive if and only if B=1
  R3: Positive if and only if C=1
  R4: Positive if and only if (A + B + C) mod 2 = 1 (sum of attributes is odd)

Your goal is to infer the actual rule type and the set of all positive element IDs through queries.

You can repeatedly make one of the following three types of queries (one query per turn):

1. **Count Query**: Ask how many positive elements are in a subset S. I will return a non-negative integer.
2. **Existence Query**: Ask whether at least one positive element exists in a subset S. I will return "Yes" or "No".
3. **Comparison Query**: Ask which of two disjoint subsets S and T contains more positive elements. I will return "S more", "T more", or "Equal".

You can define subsets in two ways:

**Method 1: List-based**
Directly list element IDs, e.g., S={{1,3,5}}

**Method 2: Condition-based**
Use boolean conditions on attributes, supporting AND, OR, NOT operations, e.g.:
- "A=1 and B=0"
- "C=0 or A=1"
- "not(B=1 and C=1)"

Each turn must contain only one query tag, using the following XML format:

- **Count Query** (e.g., querying subset with IDs 1,2,3):
<query_count>1,2,3</query_count>

Or using conditions:
<query_count>A=1 and B=1</query_count>

- **Existence Query** (e.g., querying subset with IDs 5,6,7):
<query_exist>5,6,7</query_exist>

Or using conditions:
<query_exist>C=1</query_exist>

- **Comparison Query** (e.g., comparing subsets {{1,2}} and {{5,6}}):
<query_compare>S={{1,2}}; T={{5,6}}</query_compare>

Or using conditions:
<query_compare>S={{A=1}}; T={{B=0}}</query_compare>

Note: The two subsets in a comparison query must be disjoint.

When you have gathered enough information, submit your final answer in this format:

<answer>rule=R1, positive=1,2,3,4</answer>

Where rule is the rule type (R1, R2, R3, or R4), and positive lists all positive element IDs (comma-separated, order does not matter).

If the answer is incorrect or the format is invalid, the game fails. Try to complete the inference with as few queries as possible.
"""

    contextualized_rule_zh_3 = """\
欢迎使用【在线教育课程推荐平台】。你需要通过测试推断出当前激活的课程智能推荐算法规则。

教研团队设定了一个包含 8 套课程模块（元素）的集合 U，编号为 1 到 8。每个模块具有三个公开的教研二值属性 A（包含互动测验）、B（进阶难度）、C（需前置知识），取值为 0 或 1。8 套课程覆盖所有教学属性组合，编号对应如下：
  编号 1: (A=1, B=1, C=1)
  编号 2: (A=1, B=1, C=0)
  编号 3: (A=1, B=0, C=1)
  编号 4: (A=1, B=0, C=0)
  编号 5: (A=0, B=1, C=1)
  编号 6: (A=0, B=1, C=0)
  编号 7: (A=0, B=0, C=1)
  编号 8: (A=0, B=0, C=0)

系统已秘密选择了一个判定规则 f，该规则从四个候选规则中选出，定义了集合 U 中入选"年度精品推荐"（正例）元素的子集 P。四个候选规则公开如下：
  R1: 正例当且仅当 A=1
  R2: 正例当且仅当 B=1
  R3: 正例当且仅当 C=1
  R4: 正例当且仅当 (A + B + C) mod 2 = 1（多元平衡推荐算法验证）

你的目标是通过查询推断出实际采用的规则类型以及所有正例元素的编号集合。

你可以反复提出以下三类查询（每次仅限一个查询）：

1. **计数查询**：询问某个子集 S 中有多少个正例元素。我会返回一个非负整数。
2. **存在性查询**：询问某个子集 S 中是否至少存在一个正例元素。我会返回"是"或"否"。
3. **比较查询**：询问两个互不相交的子集 S 和 T 中，哪个包含更多正例元素。我会返回"S更多"、"T更多"或"相等"。

你可以用以下两种方式定义子集：

**方式一：列表式**
直接列出元素编号，例如：S={{1,3,5}}

**方式二：条件式**
用属性的布尔条件定义，支持与、或、非运算，例如：
- "A=1 且 B=0"
- "C=0 或 A=1"
- "非(B=1 且 C=1)"

每次只能包含一个查询标签，使用以下 XML 格式：

- **计数查询**（例如查询编号 1,2,3 组成的子集）：
<query_count>1,2,3</query_count>

或使用条件式：
<query_count>A=1 且 B=1</query_count>

- **存在性查询**（例如查询编号 5,6,7 组成的子集）：
<query_exist>5,6,7</query_exist>

或使用条件式：
<query_exist>C=1</query_exist>

- **比较查询**（例如比较子集 {{1,2}} 和 {{5,6}}）：
<query_compare>S={{1,2}}; T={{5,6}}</query_compare>

或使用条件式：
<query_compare>S={{A=1}}; T={{B=0}}</query_compare>

注意：比较查询中的两个子集必须互不相交。

当你收集到足够信息后，请提交最终答案，格式如下：

<answer>rule=R1, positive=1,2,3,4</answer>

其中 rule 为规则类型（R1、R2、R3 或 R4），positive 为所有正例元素的编号（用逗号分隔，顺序不限）。

若答案错误或格式不符，测试失败。请尽可能用少的查询次数完成推理。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the [Online Education Course Recommendation Platform]. You need to infer the currently active smart course recommendation algorithm.

The teaching team defines a set U containing 8 course modules (elements), numbered 1 to 8. Each module has three public binary educational attributes A (Interactive Quiz), B (Advanced Difficulty), C (Prerequisite Required), with values 0 or 1. The 8 courses cover all pedagogical combinations, with the following mapping:
  ID 1: (A=1, B=1, C=1)
  ID 2: (A=1, B=1, C=0)
  ID 3: (A=1, B=0, C=1)
  ID 4: (A=1, B=0, C=0)
  ID 5: (A=0, B=1, C=1)
  ID 6: (A=0, B=1, C=0)
  ID 7: (A=0, B=0, C=1)
  ID 8: (A=0, B=0, C=0)

The system has secretly selected a judgment rule f from four candidate rules, which defines a subset P of modules selected for "Annual Premium Recommendation" (positive) elements in U. The four candidate rules are publicly known:
  R1: Positive if and only if A=1
  R2: Positive if and only if B=1
  R3: Positive if and only if C=1
  R4: Positive if and only if (A + B + C) mod 2 = 1 (sum of attributes is odd)

Your goal is to infer the actual rule type and the set of all positive element IDs through queries.

You can repeatedly make one of the following three types of queries (one query per turn):

1. **Count Query**: Ask how many positive elements are in a subset S. I will return a non-negative integer.
2. **Existence Query**: Ask whether at least one positive element exists in a subset S. I will return "Yes" or "No".
3. **Comparison Query**: Ask which of two disjoint subsets S and T contains more positive elements. I will return "S more", "T more", or "Equal".

You can define subsets in two ways:

**Method 1: List-based**
Directly list element IDs, e.g., S={{1,3,5}}

**Method 2: Condition-based**
Use boolean conditions on attributes, supporting AND, OR, NOT operations, e.g.:
- "A=1 and B=0"
- "C=0 or A=1"
- "not(B=1 and C=1)"

Each turn must contain only one query tag, using the following XML format:

- **Count Query** (e.g., querying subset with IDs 1,2,3):
<query_count>1,2,3</query_count>

Or using conditions:
<query_count>A=1 and B=1</query_count>

- **Existence Query** (e.g., querying subset with IDs 5,6,7):
<query_exist>5,6,7</query_exist>

Or using conditions:
<query_exist>C=1</query_exist>

- **Comparison Query** (e.g., comparing subsets {{1,2}} and {{5,6}}):
<query_compare>S={{1,2}}; T={{5,6}}</query_compare>

Or using conditions:
<query_compare>S={{A=1}}; T={{B=0}}</query_compare>

Note: The two subsets in a comparison query must be disjoint.

When you have gathered enough information, submit your final answer in this format:

<answer>rule=R1, positive=1,2,3,4</answer>

Where rule is the rule type (R1, R2, R3, or R4), and positive lists all positive element IDs (comma-separated, order does not matter).

If the answer is incorrect or the format is invalid, the game fails. Try to complete the inference with as few queries as possible.
"""

    contextualized_rule_zh_4 = """\
欢迎使用【精密智造质量评级系统】。你需要推断出当前批次零件的免检准入检验标准。

质检中心设定了一个包含 8 批次精密加工件（元素）的集合 U，编号为 1 到 8。每个批次具有三个公开的工艺二值属性 A（已热处理）、B（进口刀具加工）、C（含防锈涂层），取值为 0 或 1。8 批次工件覆盖所有工艺组合，编号对应如下：
  编号 1: (A=1, B=1, C=1)
  编号 2: (A=1, B=1, C=0)
  编号 3: (A=1, B=0, C=1)
  编号 4: (A=1, B=0, C=0)
  编号 5: (A=0, B=1, C=1)
  编号 6: (A=0, B=1, C=0)
  编号 7: (A=0, B=0, C=1)
  编号 8: (A=0, B=0, C=0)

质检中心已秘密选择了一个判定规则 f，该规则从四个候选规则中选出，定义了集合 U 中被评级为"航空级免检产品"（正例）元素的子集 P。四个候选规则公开如下：
  R1: 正例当且仅当 A=1
  R2: 正例当且仅当 B=1
  R3: 正例当且仅当 C=1
  R4: 正例当且仅当 (A + B + C) mod 2 = 1（奇偶校验工艺合规标准）

你的目标是通过查询推断出实际采用的规则类型以及所有正例元素的编号集合。

你可以反复提出以下三类查询（每次仅限一个查询）：

1. **计数查询**：询问某个子集 S 中有多少个正例元素。我会返回一个非负整数。
2. **存在性查询**：询问某个子集 S 中是否至少存在一个正例元素。我会返回"是"或"否"。
3. **比较查询**：询问两个互不相交的子集 S 和 T 中，哪个包含更多正例元素。我会返回"S更多"、"T更多"或"相等"。

你可以用以下两种方式定义子集：

**方式一：列表式**
直接列出元素编号，例如：S={{1,3,5}}

**方式二：条件式**
用属性的布尔条件定义，支持与、或、非运算，例如：
- "A=1 且 B=0"
- "C=0 或 A=1"
- "非(B=1 且 C=1)"

每次只能包含一个查询标签，使用以下 XML 格式：

- **计数查询**（例如查询编号 1,2,3 组成的子集）：
<query_count>1,2,3</query_count>

或使用条件式：
<query_count>A=1 且 B=1</query_count>

- **存在性查询**（例如查询编号 5,6,7 组成的子集）：
<query_exist>5,6,7</query_exist>

或使用条件式：
<query_exist>C=1</query_exist>

- **比较查询**（例如比较子集 {{1,2}} 和 {{5,6}}）：
<query_compare>S={{1,2}}; T={{5,6}}</query_compare>

Or using conditions:
<query_compare>S={{A=1}}; T={{B=0}}</query_compare>

注意：比较查询中的两个子集必须互不相交。

当你收集到足够信息后，请提交最终答案，格式如下：

<answer>rule=R1, positive=1,2,3,4</answer>

其中 rule 为规则类型（R1、R2、R3 或 R4），positive 为所有正例元素的编号（用逗号分隔，顺序不限）。

若答案错误或格式不符，测试失败。请尽可能用少的查询次数完成推理。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the [Precision Manufacturing Quality Rating System]. You need to infer the exemption entry standards for the current batch of parts.

The quality control center defines a set U containing 8 batches of precision machined parts (elements), numbered 1 to 8. Each batch has three public binary process attributes A (Heat Treated), B (Processed by Imported Tool), C (Anti-rust Coating), with values 0 or 1. The 8 batches cover all process combinations, with the following mapping:
  ID 1: (A=1, B=1, C=1)
  ID 2: (A=1, B=1, C=0)
  ID 3: (A=1, B=0, C=1)
  ID 4: (A=1, B=0, C=0)
  ID 5: (A=0, B=1, C=1)
  ID 6: (A=0, B=1, C=0)
  ID 7: (A=0, B=0, C=1)
  ID 8: (A=0, B=0, C=0)

The center has secretly selected a judgment rule f from four candidate rules, which defines a subset P of batches rated as "Aviation-Grade Exempt Products" (positive) elements in U. The four candidate rules are publicly known:
  R1: Positive if and only if A=1
  R2: Positive if and only if B=1
  R3: Positive if and only if C=1
  R4: Positive if and only if (A + B + C) mod 2 = 1 (sum of attributes is odd)

Your goal is to infer the actual rule type and the set of all positive element IDs through queries.

You can repeatedly make one of the following three types of queries (one query per turn):

1. **Count Query**: Ask how many positive elements are in a subset S. I will return a non-negative integer.
2. **Existence Query**: Ask whether at least one positive element exists in a subset S. I will return "Yes" or "No".
3. **Comparison Query**: Ask which of two disjoint subsets S and T contains more positive elements. I will return "S more", "T more", or "Equal".

You can define subsets in two ways:

**Method 1: List-based**
Directly list element IDs, e.g., S={{1,3,5}}

**Method 2: Condition-based**
Use boolean conditions on attributes, supporting AND, OR, NOT operations, e.g.:
- "A=1 and B=0"
- "C=0 or A=1"
- "not(B=1 and C=1)"

Each turn must contain only one query tag, using the following XML format:

- **Count Query** (e.g., querying subset with IDs 1,2,3):
<query_count>1,2,3</query_count>

Or using conditions:
<query_count>A=1 and B=1</query_count>

- **Existence Query** (e.g., querying subset with IDs 5,6,7):
<query_exist>5,6,7</query_exist>

Or using conditions:
<query_exist>C=1</query_exist>

- **Comparison Query** (e.g., comparing subsets {{1,2}} and {{5,6}}):
<query_compare>S={{1,2}}; T={{5,6}}</query_compare>

Or using conditions:
<query_compare>S={{A=1}}; T={{B=0}}</query_compare>

Note: The two subsets in a comparison query must be disjoint.

When you have gathered enough information, submit your final answer in this format:

<answer>rule=R1, positive=1,2,3,4</answer>

Where rule is the rule type (R1, R2, R3, or R4), and positive lists all positive element IDs (comma-separated, order does not matter).

If the answer is incorrect or the format is invalid, the game fails. Try to complete the inference with as few queries as possible.
"""

    contextualized_rule_zh_5 = """\
欢迎使用【反垄断审查合规分析系统】。你需要推断出当前商业并购案的强制申报触发规则。

法务审查委员会设定了一个包含 8 份商业并购案卷（元素）的集合 U，编号为 1 到 8。每份案卷具有三个公开的合规二值属性 A（涉外资背景）、B（标的额超限）、C（含核心知识产权转移），取值为 0 或 1。8 份案卷覆盖所有合规属性组合，编号对应如下：
  编号 1: (A=1, B=1, C=1)
  编号 2: (A=1, B=1, C=0)
  编号 3: (A=1, B=0, C=1)
  编号 4: (A=1, B=0, C=0)
  编号 5: (A=0, B=1, C=1)
  编号 6: (A=0, B=1, C=0)
  编号 7: (A=0, B=0, C=1)
  编号 8: (A=0, B=0, C=0)

委员会已秘密选择了一个判定规则 f，该规则从四个候选规则中选出，定义了集合 U 中触发"反垄断强制申报"（正例）元素的子集 P。四个候选规则公开如下：
  R1: 正例当且仅当 A=1
  R2: 正例当且仅当 B=1
  R3: 正例当且仅当 C=1
  R4: 正例当且仅当 (A + B + C) mod 2 = 1（风险属性复合奇校验）

你的目标是通过查询推断出实际采用的规则类型以及所有正例元素的编号集合。

你可以反复提出以下三类查询（每次仅限一个查询）：

1. **计数查询**：询问某个子集 S 中有多少个正例元素。我会返回一个非负整数。
2. **存在性查询**：询问某个子集 S 中是否至少存在一个正例元素。我会返回"是"或"否"。
3. **比较查询**：询问两个互不相交的子集 S 和 T 中，哪个包含更多正例元素。我会返回"S更多"、"T更多"或"相等"。

你可以用以下两种方式定义子集：

**方式一：列表式**
直接列出元素编号，例如：S={{1,3,5}}

**方式二：条件式**
用属性的布尔条件定义，支持与、或、非运算，例如：
- "A=1 且 B=0"
- "C=0 或 A=1"
- "非(B=1 且 C=1)"

每次只能包含一个查询标签，使用以下 XML 格式：

- **计数查询**（例如查询编号 1,2,3 组成的子集）：
<query_count>1,2,3</query_count>

或使用条件式：
<query_count>A=1 且 B=1</query_count>

- **存在性查询**（例如查询编号 5,6,7 组成的子集）：
<query_exist>5,6,7</query_exist>

或使用条件式：
<query_exist>C=1</query_exist>

- **比较查询**（例如比较子集 {{1,2}} 和 {{5,6}}）：
<query_compare>S={{1,2}}; T={{5,6}}</query_compare>

或使用条件式：
<query_compare>S={{A=1}}; T={{B=0}}</query_compare>

注意：比较查询中的两个子集必须互不相交。

当你收集到足够信息后，请提交最终答案，格式如下：

<answer>rule=R1, positive=1,2,3,4</answer>

其中 rule 为规则类型（R1、R2、R3 或 R4），positive 为所有正例元素的编号（用逗号分隔，顺序不限）。

若答案错误或格式不符，测试失败。请尽可能用少的查询次数完成推理。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the [Antitrust Review Compliance Analysis System]. You need to infer the mandatory filing trigger rules for current M&A case files.

The legal review committee defines a set U containing 8 M&A case files (elements), numbered 1 to 8. Each file has three public binary compliance attributes A (Foreign Capital Background), B (Excessive Target Amount), C (Core IP Transfer), with values 0 or 1. The 8 case files cover all compliance combinations, with the following mapping:
  ID 1: (A=1, B=1, C=1)
  ID 2: (A=1, B=1, C=0)
  ID 3: (A=1, B=0, C=1)
  ID 4: (A=1, B=0, C=0)
  ID 5: (A=0, B=1, C=1)
  ID 6: (A=0, B=1, C=0)
  ID 7: (A=0, B=0, C=1)
  ID 8: (A=0, B=0, C=0)

The committee has secretly selected a judgment rule f from four candidate rules, which defines a subset P of cases triggering "Mandatory Antitrust Filing" (positive) elements in U. The four candidate rules are publicly known:
  R1: Positive if and only if A=1
  R2: Positive if and only if B=1
  R3: Positive if and only if C=1
  R4: Positive if and only if (A + B + C) mod 2 = 1 (sum of attributes is odd)

Your goal is to infer the actual rule type and the set of all positive element IDs through queries.

You can repeatedly make one of the following three types of queries (one query per turn):

1. **Count Query**: Ask how many positive elements are in a subset S. I will return a non-negative integer.
2. **Existence Query**: Ask whether at least one positive element exists in a subset S. I will return "Yes" or "No".
3. **Comparison Query**: Ask which of two disjoint subsets S and T contains more positive elements. I will return "S more", "T more", or "Equal".

You can define subsets in two ways:

**Method 1: List-based**
Directly list element IDs, e.g., S={{1,3,5}}

**Method 2: Condition-based**
Use boolean conditions on attributes, supporting AND, OR, NOT operations, e.g.:
- "A=1 and B=0"
- "C=0 or A=1"
- "not(B=1 and C=1)"

Each turn must contain only one query tag, using the following XML format:

- **Count Query** (e.g., querying subset with IDs 1,2,3):
<query_count>1,2,3</query_count>

Or using conditions:
<query_count>A=1 and B=1</query_count>

- **Existence Query** (e.g., querying subset with IDs 5,6,7):
<query_exist>5,6,7</query_exist>

Or using conditions:
<query_exist>C=1</query_exist>

- **Comparison Query** (e.g., comparing subsets {{1,2}} and {{5,6}}):
<query_compare>S={{1,2}}; T={{5,6}}</query_compare>

Or using conditions:
<query_compare>S={{A=1}}; T={{B=0}}</query_compare>

Note: The two subsets in a comparison query must be disjoint.

When you have gathered enough information, submit your final answer in this format:

<answer>rule=R1, positive=1,2,3,4</answer>

Where rule is the rule type (R1, R2, R3, or R4), and positive lists all positive element IDs (comma-separated, order does not matter).

If the answer is incorrect or the format is invalid, the game fails. Try to complete the inference with as few queries as possible.
"""

    tags = ["answer", "query_count", "query_exist", "query_compare"]
    
    reasoning_type = "溯因推理"
    data_structure = "集合"

    
    DIFFICULTY_CONFIG = {
        1: {
            "rule": "R1",
        },
        2: {
            "rule": "R2",
        },
        3: {
            "rule": "R3",
        },
        4: {
            "rule": "R4",
        },
        5: {
            "rule": "R4",
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = self.config.difficulty
        
        if isinstance(diff, str):
            diff = int(diff)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self.rule_type = cfg["rule"]
        
        self.elements = {
            "1": (1, 1, 1),
            "2": (1, 1, 0),
            "3": (1, 0, 1),
            "4": (1, 0, 0),
            "5": (0, 1, 1),
            "6": (0, 1, 0),
            "7": (0, 0, 1),
            "8": (0, 0, 0),
        }
        
        self.positive_set = set()
        for idx, (a, b, c) in self.elements.items():
            if self._is_positive(a, b, c):
                self.positive_set.add(idx)
        
        self._game_info["n"] = 8

    def _is_positive(self, a, b, c):
        if self.rule_type == "R1":
            return a == 1
        elif self.rule_type == "R2":
            return b == 1
        elif self.rule_type == "R3":
            return c == 1
        elif self.rule_type == "R4":
            return (a + b + c) % 2 == 1
        else:
            raise ValueError(f"Unknown rule type: {self.rule_type}")

    def _parse_subset(self, subset_str):
        subset_str = subset_str.strip()
        
        subset_str_clean = subset_str.strip("{}").strip()
        if re.match(r'^[\d\s,]+$', subset_str_clean):
            ids = set()
            for x in subset_str_clean.split(","):
                x = x.strip()
                if x and x in self.elements:
                    ids.add(x)
            return ids
        
        return self._parse_condition(subset_str)

    def _parse_condition(self, condition_str):
        condition_str = condition_str.strip().lower()
        
        condition_str = condition_str.replace("且", "and")
        condition_str = condition_str.replace("或", "or")
        condition_str = condition_str.replace("非", "not")
        
        result_set = set()
        parse_failures = 0
        
        for idx, (a, b, c) in self.elements.items():
            try:
                local_vars = {'a': a, 'b': b, 'c': c}
                
                expr = condition_str
                expr = re.sub(r'\ba\s*=\s*([01])', r'a==\1', expr)
                expr = re.sub(r'\bb\s*=\s*([01])', r'b==\1', expr)
                expr = re.sub(r'\bc\s*=\s*([01])', r'c==\1', expr)
                
                expr = expr.replace('not(', 'not (')
                
                if eval(expr, {"__builtins__": {}}, local_vars):
                    result_set.add(idx)
            except Exception:
                parse_failures += 1
                continue
                
        if parse_failures == len(self.elements):
            raise ValueError(f"Failed to parse condition for all elements: {condition_str}")
        
        return result_set

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        
        rule_match = re.search(r'rule\s*=\s*(R\d)', raw_ans, re.IGNORECASE)
        pos_match = re.search(r'positive\s*=\s*([\d\s,]+)', raw_ans, re.IGNORECASE)
        
        if not rule_match or not pos_match:
            return False
            
        model_rule = rule_match.group(1).strip()
        model_pos_str = pos_match.group(1).strip()
        
        if model_rule != self.rule_type:
            return False
        
        try:
            model_positive = set(
                x.strip() 
                for x in model_pos_str.split(",") 
                if x.strip()
            )
        except:
            return False
        
        return model_positive == self.positive_set

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            more_s, more_t, equal = "S更多", "T更多", "相等"
            error_msg = "错误：查询格式无效或子集定义错误。"
            disjoint_error = "错误：比较查询中的两个子集必须互不相交。"
        else:
            yes_res, no_res = "Yes", "No"
            more_s, more_t, equal = "S more", "T more", "Equal"
            error_msg = "Error: Invalid query format or subset definition."
            disjoint_error = "Error: The two subsets in comparison query must be disjoint."

        try:
            if "query_count" in parsed_info:
                subset_str = parsed_info["query_count"].strip()
                subset = self._parse_subset(subset_str)
                count = len(subset & self.positive_set)
                return str(count)

            elif "query_exist" in parsed_info:
                subset_str = parsed_info["query_exist"].strip()
                subset = self._parse_subset(subset_str)
                exists = len(subset & self.positive_set) >= 1
                return yes_res if exists else no_res

            elif "query_compare" in parsed_info:
                raw = parsed_info["query_compare"]
                
                parts = raw.split(";")
                if len(parts) != 2:
                    return error_msg
                
                s_part = parts[0].strip()
                t_part = parts[1].strip()
                
                s_match = re.search(r'S\s*=\s*\{(.+?)\}', s_part, re.IGNORECASE)
                t_match = re.search(r'T\s*=\s*\{(.+?)\}', t_part, re.IGNORECASE)
                
                if not s_match or not t_match:
                    return error_msg
                
                s_def = s_match.group(1).strip()
                t_def = t_match.group(1).strip()
                
                subset_s = self._parse_subset(s_def)
                subset_t = self._parse_subset(t_def)
                
                if subset_s & subset_t:
                    return disjoint_error
                
                count_s = len(subset_s & self.positive_set)
                count_t = len(subset_t & self.positive_set)
                
                if count_s > count_t:
                    return more_s
                elif count_s < count_t:
                    return more_t
                else:
                    return equal

            else:
                return error_msg

        except Exception as e:
            return error_msg

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            val = int(correct)
            if val == 0:
                return "1"
            else:
                return str(val - 1)
        
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            if correct == "否":
                return "是"
            if correct == "S更多":
                return "T更多"
            if correct == "T更多":
                return "S更多"
            if correct == "相等":
                return "S更多"
        else:
            c_lower = correct.lower()
            if c_lower == "yes":
                return "No"
            if c_lower == "no":
                return "Yes"
            if c_lower == "s more":
                return "T more"
            if c_lower == "t more":
                return "S more"
            if c_lower == "equal":
                return "S more"
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            more_s, more_t, equal_res = "S更多", "T更多", "相等"
        else:
            yes_res, no_res = "Yes", "No"
            more_s, more_t, equal_res = "S more", "T more", "Equal"

        all_ids = sorted(list(self.elements.keys()))

        for r in range(1, 3):
            for subset_tuple in itertools.combinations(all_ids, r):
                subset_ids = set(subset_tuple)
                subset_str = ",".join(subset_tuple)
                pos_count = len(subset_ids & self.positive_set)
                
                queries.append({
                    "query": f"<query_count>{subset_str}</query_count>",
                    "answer": str(pos_count)
                })
                
                ans_exist = yes_res if pos_count >= 1 else no_res
                queries.append({
                    "query": f"<query_exist>{subset_str}</query_exist>",
                    "answer": ans_exist
                })

        full_str = ",".join(all_ids)
        queries.append({
            "query": f"<query_count>{full_str}</query_count>",
            "answer": str(len(self.positive_set))
        })

        for s_id, t_id in itertools.combinations(all_ids, 2):
            s_ids = {s_id}
            t_ids = {t_id}
            
            q_str = f"<query_compare>S={{{s_id}}}; T={{{t_id}}}</query_compare>"
            
            count_s = len(s_ids & self.positive_set)
            count_t = len(t_ids & self.positive_set)
            
            if count_s > count_t:
                ans = more_s
            elif count_s < count_t:
                ans = more_t
            else:
                ans = equal_res
                
            queries.append({
                "query": q_str,
                "answer": ans
            })
            
        return queries