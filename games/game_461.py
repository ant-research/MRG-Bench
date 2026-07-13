# -*- coding: utf-8 -*-
from .base import Game
import re
import itertools

class HiddenSubsetRuleGame(Game):

    contextualized_rule_zh_1 = """\
我们现在来进行一项"智能交通路网枢纽识别"的测试任务，规则如下：

系统设定了一个有限的交通节点集合 U，由 {n} 个互不重复的节点组成，节点标记为 {elements}。集合为无序、无位置，提交的测试节点集合不允许重复。

存在一个隐藏的核心交通枢纽子集 C（C 是 U 的子集），以及一个隐藏的流量管控法则 L。对任意你提交的测试路网节点集合 T（T 是 U 的子集），系统会返回二元反馈：「接受」或「拒绝」，该反馈仅由 T 与 C 的子集包含关系决定。法则 L 不依赖于节点的名称或其他现实地理语义。

法则 L 的定义范围：L 是仅以谓词「C 是否为 T 的子集」与「T 是否为 C 的子集」为输入的布尔函数。换言之，反馈只取决于 T 与 C 之间的包含关系类别，共有四类：
1. T 等于 C
2. T 是 C 的真子集（T 严格包含于 C）
3. T 是 C 的真超集（T 严格包含 C）
4. 两者皆否（既非子集也非超集）

你的目标是在尽可能少的查询次数内，正确识别隐藏的枢纽子集 C 以及隐藏的管控法则 L。

## 允许的查询类型

你可以反复向我提出以下三类查询（每次仅限一个），我会根据真实路网设定如实回答：

1. 判定查询：提交一个测试节点集合 T（T 是 U 的子集），系统返回依据管控法则 L 的二元反馈（「接受」或「拒绝」）。
   格式示例：
   <query_test>A,B,C</query_test>

2. 包含比较查询：就两个具体节点集合 S 和 T 提问「S 是否包含 T」（即 T 的所有节点是否都在 S 中）。系统返回「是」或「否」。
   格式示例：
   <query_contain>A,B,C|D,E</query_contain>
   （表示询问集合 {{A,B,C}} 是否包含集合 {{D,E}}）

3. 最终断言：给出对法则 L 的明确描述，以及给出具体的枢纽子集 C。
   格式示例：
   <answer>rule=当 T 等于 C 时接受, target=A,B,C</answer>
   
   rule 字段必须是以下四种之一：
   - "当 T 等于 C 时接受"
   - "当 T 是 C 的真子集时接受"
   - "当 T 是 C 的真超集时接受"
   - "当 T 与 C 既非子集也非超集时接受"

## 注意事项

- 集合中的元素用逗号分隔，顺序不影响结果
- 空集用空字符串表示（如 <query_test></query_test>）
- 每次只能提交一个查询标签
- 若答案错误或格式不符，测试失败
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's conduct a "Smart Traffic Network Hub Identification" testing task. Here are the rules:

The system defines a finite traffic node set U, consisting of {n} distinct elements labeled as {elements}. Sets are unordered and do not allow duplicate nodes.

There exists a hidden core traffic hub subset C (C is a subset of U) and a hidden traffic control rule L. For any test network node set T you submit (T is a subset of U), the system will return binary feedback: "Accept" or "Reject", determined solely by the subset containment relationship between T and C. Rule L does not depend on node names or other geographical semantics.

Definition scope of rule L: L is a boolean function that takes as input only the predicates "whether C is a subset of T" and "whether T is a subset of C". In other words, feedback depends only on the containment relationship category between T and C. There are four categories:
1. T equals C
2. T is a proper subset of C (T is strictly contained in C)
3. T is a proper superset of C (T strictly contains C)
4. Neither (neither a subset nor a superset)

Your goal is to correctly identify the hidden hub subset C and the hidden control rule L using as few queries as possible.

## Allowed Query Types

You can repeatedly ask me the following three types of questions (one per turn), and I will answer truthfully based on the network settings:

1. Test Query: Submit a node set T (T is a subset of U), and the system returns binary feedback ("Accept" or "Reject") according to rule L.
   Format example:
   <query_test>A,B,C</query_test>

2. Containment Comparison Query: Ask whether set S contains set T (i.e., whether all nodes of T are in S). The system returns "Yes" or "No".
   Format example:
   <query_contain>A,B,C|D,E</query_contain>
   (Asking whether set {{A,B,C}} contains set {{D,E}})

3. Final Assertion: Provide a clear description of rule L and specify the concrete hub subset C.
   Format example:
   <answer>rule=Accept when T equals C, target=A,B,C</answer>
   
   The rule field must be exactly one of the following four:
   - "Accept when T equals C"
   - "Accept when T is a proper subset of C"
   - "Accept when T is a proper superset of C"
   - "Accept when T and C are neither subset nor superset"

## Notes

- Elements in a set are separated by commas; order does not matter
- Empty set is represented by empty string (e.g., <query_test></query_test>)
- Only one query tag can be submitted each time
- If the answer is wrong or the format is invalid, the test fails
"""

    contextualized_rule_zh_2 = """\
我们现在来进行一项"联合用药方案筛选"的临床前测试任务，规则如下：

系统设定了一个有限的候选药物分子集合 U，由 {n} 个互不重复的分子组成，标记为 {elements}。集合为无序，提交的联合用药方案不允许重复包含同一分子。

存在一个隐藏的核心靶向组合 C（C 是 U 的子集），以及一个隐藏的临床药理协同法则 L。对任意你提交的用药组合 T（T 是 U 的子集），系统会返回二元临床反馈：「接受」或「拒绝」，该反馈仅由 T 与 C 的子集包含关系决定。法则 L 不依赖于分子的化学名称或其他实际药理语义。

法则 L 的定义范围：L 是仅以谓词「C 是否为 T 的子集」与「T 是否为 C 的子集」为输入的布尔函数。换言之，反馈只取决于 T 与 C 之间的包含关系类别，共有四类：
1. T 等于 C
2. T 是 C 的真子集（T 严格包含于 C）
3. T 是 C 的真超集（T 严格包含 C）
4. 两者皆否（既非子集也非超集）

你的目标是在尽可能少的临床筛选测试内，正确识别隐藏的靶向组合 C 以及隐藏的协同法则 L。

## 允许的查询类型

你可以反复向我提出以下三类查询（每次仅限一个），我会根据真实的模拟药理数据如实回答：

1. 判定查询：提交一个联合用药组合 T（T 是 U 的子集），系统返回依据协同法则 L 的二元反馈（「接受」或「拒绝」）。
   格式示例：
   <query_test>A,B,C</query_test>

2. 包含比较查询：就两个具体组合 S 和 T 提问「S 是否包含 T」（即 T 的所有分子是否都在 S 中）。系统返回「是」或「否」。
   格式示例：
   <query_contain>A,B,C|D,E</query_contain>
   （表示询问集合 {{A,B,C}} 是否包含集合 {{D,E}}）

3. 最终断言：给出对法则 L 的明确描述，以及给出具体的靶向组合 C。
   格式示例：
   <answer>rule=当 T 等于 C 时接受, target=A,B,C</answer>
   
   rule 字段必须是以下四种之一：
   - "当 T 等于 C 时接受"
   - "当 T 是 C 的真子集时接受"
   - "当 T 是 C 的真超集时接受"
   - "当 T 与 C 既非子集也非超集时接受"

## 注意事项

- 集合中的元素用逗号分隔，顺序不影响结果
- 空集用空字符串表示（如 <query_test></query_test>）
- 每次只能提交一个查询标签
- 若答案错误或格式不符，筛选失败
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct a "Combination Therapy Screening" preclinical testing task. Here are the rules:

The system defines a finite candidate drug molecule pool U, consisting of {n} distinct elements labeled as {elements}. Sets are unordered and do not allow duplicate molecules in the submitted combination therapy.

There exists a hidden core target combination C (C is a subset of U) and a hidden clinical synergy rule L. For any drug combination T you submit (T is a subset of U), the system will return binary clinical feedback: "Accept" or "Reject", determined solely by the subset containment relationship between T and C. Rule L does not depend on molecule names or other pharmacological semantics.

Definition scope of rule L: L is a boolean function that takes as input only the predicates "whether C is a subset of T" and "whether T is a subset of C". In other words, feedback depends only on the containment relationship category between T and C. There are four categories:
1. T equals C
2. T is a proper subset of C (T is strictly contained in C)
3. T is a proper superset of C (T strictly contains C)
4. Neither (neither a subset nor a superset)

Your goal is to correctly identify the hidden target combination C and the hidden clinical synergy rule L using as few screening tests as possible.

## Allowed Query Types

You can repeatedly ask me the following three types of questions (one per turn), and I will answer truthfully based on the simulated pharmacological data:

1. Test Query: Submit a drug combination T (T is a subset of U), and the system returns binary feedback ("Accept" or "Reject") according to rule L.
   Format example:
   <query_test>A,B,C</query_test>

2. Containment Comparison Query: Ask whether combination S contains combination T (i.e., whether all molecules of T are in S). The system returns "Yes" or "No".
   Format example:
   <query_contain>A,B,C|D,E</query_contain>
   (Asking whether set {{A,B,C}} contains set {{D,E}})

3. Final Assertion: Provide a clear description of rule L and specify the concrete target combination C.
   Format example:
   <answer>rule=Accept when T equals C, target=A,B,C</answer>
   
   The rule field must be exactly one of the following four:
   - "Accept when T equals C"
   - "Accept when T is a proper subset of C"
   - "Accept when T is a proper superset of C"
   - "Accept when T and C are neither subset nor superset"

## Notes

- Molecules in a set are separated by commas; order does not matter
- Empty set is represented by empty string (e.g., <query_test></query_test>)
- Only one query tag can be submitted each time
- If the answer is wrong or the format is invalid, the screening fails
"""

    contextualized_rule_zh_3 = """\
我们现在来进行一项"自适应学习路径规划"的评估任务，规则如下：

系统设定了一个有限的知识点模块集合 U，由 {n} 个互不重复的模块组成，标记为 {elements}。集合为无序、无位置，提交的学习方案不允许包含重复的知识点模块。

存在一个隐藏的核心必修知识库 C（C 是 U 的子集），以及一个隐藏的课程解锁校验规则 L。对任意你提交的学习规划集合 T（T 是 U 的子集），系统会返回二元反馈：「接受」或「拒绝」，该反馈仅由 T 与 C 的子集包含关系决定。规则 L 不依赖于模块名称或实际学科语义。

规则 L 的定义范围：L 是仅以谓词「C 是否为 T 的子集」与「T 是否为 C 的子集」为输入的布尔函数。换言之，反馈只取决于 T 与 C 之间的包含关系类别，共有四类：
1. T 等于 C
2. T 是 C 的真子集（T 严格包含于 C）
3. T 是 C 的真超集（T 严格包含 C）
4. 两者皆否（既非子集也非超集）

你的目标是在尽可能少的查询次数内，正确识别隐藏的核心必修库 C 以及隐藏的解锁校验规则 L。

## 允许的查询类型

你可以反复向我提出以下三类查询（每次仅限一个），我会根据真实教学大纲如实回答：

1. 判定查询：提交一个学习规划集合 T（T 是 U 的子集），系统返回依据校验规则 L 的二元反馈（「接受」或「拒绝」）。
   格式示例：
   <query_test>A,B,C</query_test>

2. 包含比较查询：就两个具体模块集合 S 和 T 提问「S 是否包含 T」（即 T 的所有模块是否都在 S 中）。系统返回「是」或「否」。
   格式示例：
   <query_contain>A,B,C|D,E</query_contain>
   （表示询问集合 {{A,B,C}} 是否包含集合 {{D,E}}）

3. 最终断言：给出对规则 L 的明确描述，以及给出具体的核心必修库 C。
   格式示例：
   <answer>rule=当 T 等于 C 时接受, target=A,B,C</answer>
   
   rule 字段必须是以下四种之一：
   - "当 T 等于 C 时接受"
   - "当 T 是 C 的真子集时接受"
   - "当 T 是 C 的真超集时接受"
   - "当 T 与 C 既非子集也非超集时接受"

## 注意事项

- 集合中的元素用逗号分隔，顺序不影响结果
- 空集用空字符串表示（如 <query_test></query_test>）
- 每次只能提交一个查询标签
- 若答案错误或格式不符，评估失败
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct an "Adaptive Learning Path Planning" evaluation task. Here are the rules:

The system defines a finite knowledge module set U, consisting of {n} distinct elements labeled as {elements}. Sets are unordered and do not allow duplicate modules in the submitted learning plan.

There exists a hidden core prerequisite knowledge base C (C is a subset of U) and a hidden course unlocking validation rule L. For any learning plan set T you submit (T is a subset of U), the system will return binary feedback: "Accept" or "Reject", determined solely by the subset containment relationship between T and C. Rule L does not depend on module names or actual academic semantics.

Definition scope of rule L: L is a boolean function that takes as input only the predicates "whether C is a subset of T" and "whether T is a subset of C". In other words, feedback depends only on the containment relationship category between T and C. There are four categories:
1. T equals C
2. T is a proper subset of C (T is strictly contained in C)
3. T is a proper superset of C (T strictly contains C)
4. Neither (neither a subset nor a superset)

Your goal is to correctly identify the hidden prerequisite base C and the hidden unlocking rule L using as few queries as possible.

## Allowed Query Types

You can repeatedly ask me the following three types of questions (one per turn), and I will answer truthfully based on the syllabus settings:

1. Test Query: Submit a learning plan set T (T is a subset of U), and the system returns binary feedback ("Accept" or "Reject") according to rule L.
   Format example:
   <query_test>A,B,C</query_test>

2. Containment Comparison Query: Ask whether module set S contains module set T (i.e., whether all modules of T are in S). The system returns "Yes" or "No".
   Format example:
   <query_contain>A,B,C|D,E</query_contain>
   (Asking whether set {{A,B,C}} contains set {{D,E}})

3. Final Assertion: Provide a clear description of rule L and specify the concrete core prerequisite base C.
   Format example:
   <answer>rule=Accept when T equals C, target=A,B,C</answer>
   
   The rule field must be exactly one of the following four:
   - "Accept when T equals C"
   - "Accept when T is a proper subset of C"
   - "Accept when T is a proper superset of C"
   - "Accept when T and C are neither subset nor superset"

## Notes

- Modules in a set are separated by commas; order does not matter
- Empty set is represented by empty string (e.g., <query_test></query_test>)
- Only one query tag can be submitted each time
- If the answer is wrong or the format is invalid, the evaluation fails
"""

    contextualized_rule_zh_4 = """\
我们现在来进行一项"精密组件装配自动化质检"验证任务，规则如下：

系统设定了一个有限的生产线可用标准化组件集合 U，由 {n} 个互不重复的组件组成，标记为 {elements}。集合为无序，提交的装配清单不允许重复包含相同的组件。

存在一个隐藏的核心公差适配组件库 C（C 是 U 的子集），以及一个隐藏的自动化质检放行规则 L。对任意你提交的试装配组件清单 T（T 是 U 的子集），系统会返回二元质检反馈：「接受」或「拒绝」，该反馈仅由 T 与 C 的子集包含关系决定。规则 L 不依赖于组件的名称或实际物理属性。

规则 L 的定义范围：L 是仅以谓词「C 是否为 T 的子集」与「T 是否为 C 的子集」为输入的布尔函数。换言之，反馈只取决于 T 与 C 之间的包含关系类别，共有四类：
1. T 等于 C
2. T 是 C 的真子集（T 严格包含于 C）
3. T 是 C 的真超集（T 严格包含 C）
4. 两者皆否（既非子集也非超集）

你的目标是在尽可能少的查询次数内，正确识别隐藏的核心适配组件库 C 以及隐藏的自动化质检放行规则 L。

## 允许的查询类型

你可以反复向我提出以下三类查询（每次仅限一个），我会根据真实的装配质检系统参数如实回答：

1. 判定查询：提交一个试装配组件清单 T（T 是 U 的子集），系统返回依据质检规则 L 的二元反馈（「接受」或「拒绝」）。
   格式示例：
   <query_test>A,B,C</query_test>

2. 包含比较查询：就两个具体组件清单 S 和 T 提问「S 是否包含 T」（即 T 的所有组件是否都在 S 中）。系统返回「是」或「否」。
   格式示例：
   <query_contain>A,B,C|D,E</query_contain>
   （表示询问集合 {{A,B,C}} 是否包含集合 {{D,E}}）

3. 最终断言：给出对规则 L 的明确描述，以及给出具体的核心适配组件库 C。
   格式示例：
   <answer>rule=当 T 等于 C 时接受, target=A,B,C</answer>
   
   rule 字段必须是以下四种之一：
   - "当 T 等于 C 时接受"
   - "当 T 是 C 的真子集时接受"
   - "当 T 是 C 的真超集时接受"
   - "当 T 与 C 既非子集也非超集时接受"

## 注意事项

- 集合中的元素用逗号分隔，顺序不影响结果
- 空集用空字符串表示（如 <query_test></query_test>）
- 每次只能提交一个查询标签
- 若答案错误或格式不符，验证任务失败
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's conduct a "Precision Component Assembly Automated Quality Inspection" validation task. Here are the rules:

The system defines a finite available standardized component set U on the production line, consisting of {n} distinct elements labeled as {elements}. Sets are unordered and do not allow duplicate components in the submitted assembly list.

There exists a hidden core tolerance-adaptive component library C (C is a subset of U) and a hidden automated inspection clearance rule L. For any trial assembly component list T you submit (T is a subset of U), the system will return binary quality feedback: "Accept" or "Reject", determined solely by the subset containment relationship between T and C. Rule L does not depend on component names or actual physical attributes.

Definition scope of rule L: L is a boolean function that takes as input only the predicates "whether C is a subset of T" and "whether T is a subset of C". In other words, feedback depends only on the containment relationship category between T and C. There are four categories:
1. T equals C
2. T is a proper subset of C (T is strictly contained in C)
3. T is a proper superset of C (T strictly contains C)
4. Neither (neither a subset nor a superset)

Your goal is to correctly identify the hidden core adaptive component library C and the hidden inspection clearance rule L using as few queries as possible.

## Allowed Query Types

You can repeatedly ask me the following three types of questions (one per turn), and I will answer truthfully based on the inspection system parameters:

1. Test Query: Submit an assembly component list T (T is a subset of U), and the system returns binary feedback ("Accept" or "Reject") according to inspection rule L.
   Format example:
   <query_test>A,B,C</query_test>

2. Containment Comparison Query: Ask whether component list S contains component list T (i.e., whether all components of T are in S). The system returns "Yes" or "No".
   Format example:
   <query_contain>A,B,C|D,E</query_contain>
   (Asking whether set {{A,B,C}} contains set {{D,E}})

3. Final Assertion: Provide a clear description of rule L and specify the concrete core adaptive component library C.
   Format example:
   <answer>rule=Accept when T equals C, target=A,B,C</answer>
   
   The rule field must be exactly one of the following four:
   - "Accept when T equals C"
   - "Accept when T is a proper subset of C"
   - "Accept when T is a proper superset of C"
   - "Accept when T and C are neither subset nor superset"

## Notes

- Components in a set are separated by commas; order does not matter
- Empty set is represented by empty string (e.g., <query_test></query_test>)
- Only one query tag can be submitted each time
- If the answer is wrong or the format is invalid, the validation fails
"""

    contextualized_rule_zh_5 = """\
我们现在来进行一项"智能合规审查验证"推演任务，规则如下：

系统设定了一个有限的适用法律条款集合 U，由 {n} 个互不重复的条款组成，标记为 {elements}。集合为无序，提交的审查清单不允许包含重复条款。

存在一个隐藏的核心红线条款子集 C（C 是 U 的子集），以及一个隐藏的合规审查裁决规则 L。对任意你提交的适用条款清单 T（T 是 U 的子集），系统会返回二元审查反馈：「接受」或「拒绝」，该反馈仅由 T 与 C 的子集包含关系决定。规则 L 不依赖于条款的具体名称或法律条文内容。

规则 L 的定义范围：L 是仅以谓词「C 是否为 T 的子集」与「T 是否为 C 的子集」为输入的布尔函数。换言之，反馈只取决于 T 与 C 之间的包含关系类别，共有四类：
1. T 等于 C
2. T 是 C 的真子集（T 严格包含于 C）
3. T 是 C 的真超集（T 严格包含 C）
4. 两者皆否（既非子集也非超集）

你的目标是在尽可能少的合规问询次数内，正确识别隐藏的核心红线条款子集 C 以及隐藏的合规裁决规则 L。

## 允许的查询类型

你可以反复向我提出以下三类查询（每次仅限一个），我会根据真实的合规逻辑系统如实回答：

1. 判定查询：提交一个适用条款清单 T（T 是 U 的子集），系统返回依据合规规则 L 的二元反馈（「接受」或「拒绝」）。
   格式示例：
   <query_test>A,B,C</query_test>

2. 包含比较查询：就两个具体条款清单 S 和 T 提问「S 是否包含 T」（即 T 的所有条款是否都在 S 中）。系统返回「是」或「否」。
   格式示例：
   <query_contain>A,B,C|D,E</query_contain>
   （表示询问集合 {{A,B,C}} 是否包含集合 {{D,E}}）

3. 最终断言：给出对规则 L 的明确描述，以及给出具体的核心红线条款子集 C。
   格式示例：
   <answer>rule=当 T 等于 C 时接受, target=A,B,C</answer>
   
   rule 字段必须是以下四种之一：
   - "当 T 等于 C 时接受"
   - "当 T 是 C 的真子集时接受"
   - "当 T 是 C 的真超集时接受"
   - "当 T 与 C 既非子集也非超集时接受"

## 注意事项

- 集合中的元素用逗号分隔，顺序不影响结果
- 空集用空字符串表示（如 <query_test></query_test>）
- 每次只能提交一个查询标签
- 若答案错误或格式不符，验证任务失败
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct a "Smart Compliance Review Validation" simulation task. Here are the rules:

The system defines a finite applicable legal clause set U, consisting of {n} distinct elements labeled as {elements}. Sets are unordered and do not allow duplicate clauses in the submitted review list.

There exists a hidden core redline clause subset C (C is a subset of U) and a hidden compliance review adjudication rule L. For any applicable clause list T you submit (T is a subset of U), the system will return binary review feedback: "Accept" or "Reject", determined solely by the subset containment relationship between T and C. Rule L does not depend on clause names or actual legal text semantics.

Definition scope of rule L: L is a boolean function that takes as input only the predicates "whether C is a subset of T" and "whether T is a subset of C". In other words, feedback depends only on the containment relationship category between T and C. There are four categories:
1. T equals C
2. T is a proper subset of C (T is strictly contained in C)
3. T is a proper superset of C (T strictly contains C)
4. Neither (neither a subset nor a superset)

Your goal is to correctly identify the hidden core redline clause subset C and the hidden compliance adjudication rule L using as few inquiries as possible.

## Allowed Query Types

You can repeatedly ask me the following three types of questions (one per turn), and I will answer truthfully based on the simulated compliance logic system:

1. Test Query: Submit an applicable clause list T (T is a subset of U), and the system returns binary feedback ("Accept" or "Reject") according to adjudication rule L.
   Format example:
   <query_test>A,B,C</query_test>

2. Containment Comparison Query: Ask whether clause list S contains clause list T (i.e., whether all clauses of T are in S). The system returns "Yes" or "No".
   Format example:
   <query_contain>A,B,C|D,E</query_contain>
   (Asking whether set {{A,B,C}} contains set {{D,E}})

3. Final Assertion: Provide a clear description of rule L and specify the concrete core redline clause subset C.
   Format example:
   <answer>rule=Accept when T equals C, target=A,B,C</answer>
   
   The rule field must be exactly one of the following four:
   - "Accept when T equals C"
   - "Accept when T is a proper subset of C"
   - "Accept when T is a proper superset of C"
   - "Accept when T and C are neither subset nor superset"

## Notes

- Clauses in a set are separated by commas; order does not matter
- Empty set is represented by empty string (e.g., <query_test></query_test>)
- Only one query tag can be submitted each time
- If the answer is wrong or the format is invalid, the validation fails
"""

    game_rule_zh = """\
我们现在来玩一个"隐藏子集规则"的推理游戏，规则如下：

游戏设定了一个有限集合 U，由 {n} 个互不重复的元素组成，元素标记为 {elements}。集合为无序、无位置，提交集合不允许重复元素。

存在一个隐藏的目标子集 C（C 是 U 的子集），以及一个隐藏的二元决策法则 L。对任意你提交的集合 T（T 是 U 的子集），系统会返回二元反馈：「接受」或「拒绝」，该反馈仅由 T 与 C 的子集包含关系决定。法则 L 不依赖于元素的名称或其他语义。

法则 L 的定义范围：L 是仅以谓词「C 是否为 T 的子集」与「T 是否为 C 的子集」为输入的布尔函数。换言之，反馈只取决于 T 与 C 之间的包含关系类别，共有四类：
1. T 等于 C
2. T 是 C 的真子集（T 严格包含于 C）
3. T 是 C 的真超集（T 严格包含 C）
4. 两者皆否（既非子集也非超集）

你的目标是在尽可能少的查询次数内，正确识别隐藏子集 C 以及隐藏法则 L。

## 允许的查询类型

你可以反复向我提出以下三类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 判定查询：提交一个集合 T（T 是 U 的子集），系统返回依据隐藏法则 L 的二元反馈（「接受」或「拒绝」）。
   格式示例：
   <query_test>A,B,C</query_test>

2. 包含比较查询：就两个具体集合 S 和 T 提问「S 是否包含 T」（即 T 的所有元素是否都在 S 中）。系统返回「是」或「否」。
   格式示例：
   <query_contain>A,B,C|D,E</query_contain>
   （表示询问集合 {{A,B,C}} 是否包含集合 {{D,E}}）

3. 最终断言：给出对法则 L 的明确描述（须使用"等于"、"真子集"、"真超集"、"两者皆否"等术语表述），以及给出具体的目标子集 C。
   格式示例：
   <answer>rule=当 T 等于 C 时接受, target=A,B,C</answer>
   
   rule 字段必须是以下四种之一：
   - "当 T 等于 C 时接受"
   - "当 T 是 C 的真子集时接受"
   - "当 T 是 C 的真超集时接受"
   - "当 T 与 C 既非子集也非超集时接受"

## 注意事项

- 集合中的元素用逗号分隔，顺序不影响结果
- 空集用空字符串表示（如 <query_test></query_test>）
- 每次只能提交一个查询标签
- 若答案错误或格式不符，游戏失败
"""

    game_rule_en = """\
Let's play a "Hidden Subset Rule" deduction game. Here are the rules:

The game defines a finite set U consisting of {n} distinct elements, labeled as {elements}. Sets are unordered and do not allow duplicate elements.

There exists a hidden target subset C (C is a subset of U) and a hidden binary decision rule L. For any set T you submit (T is a subset of U), the system will return binary feedback: "Accept" or "Reject", determined solely by the subset containment relationship between T and C. Rule L does not depend on element names or other semantics.

Definition scope of rule L: L is a boolean function that takes as input only the predicates "whether C is a subset of T" and "whether T is a subset of C". In other words, feedback depends only on the containment relationship category between T and C. There are four categories:
1. T equals C
2. T is a proper subset of C (T is strictly contained in C)
3. T is a proper superset of C (T strictly contains C)
4. Neither (neither a subset nor a superset)

Your goal is to correctly identify the hidden subset C and the hidden rule L using as few queries as possible.

## Allowed Query Types

You can repeatedly ask me the following three types of questions (one per turn), and I will answer truthfully:

1. Test Query: Submit a set T (T is a subset of U), and the system returns binary feedback ("Accept" or "Reject") according to the hidden rule L.
   Format example:
   <query_test>A,B,C</query_test>

2. Containment Comparison Query: Ask whether set S contains set T (i.e., whether all elements of T are in S). The system returns "Yes" or "No".
   Format example:
   <query_contain>A,B,C|D,E</query_contain>
   (Asking whether set {{A,B,C}} contains set {{D,E}})

3. Final Assertion: Provide a clear description of rule L (must use terms like "equals", "proper subset", "proper superset", "neither") and specify the concrete target subset C.
   Format example:
   <answer>rule=Accept when T equals C, target=A,B,C</answer>
   
   The rule field must be one of the following four:
   - "Accept when T equals C"
   - "Accept when T is a proper subset of C"
   - "Accept when T is a proper superset of C"
   - "Accept when T and C are neither subset nor superset"

## Notes

- Elements in a set are separated by commas; order does not matter
- Empty set is represented by empty string (e.g., <query_test></query_test>)
- Only one query tag can be submitted each time
- If the answer is wrong or the format is invalid, the game fails
"""

    tags = ["answer", "query_test", "query_contain"]
    
    reasoning_type = "归纳推理"
    data_structure = "集合"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "elements": "A, B, C, D, E",
                "target": "A,B",
                "rule": "equal",
            },
            2: {
                "n": 6,
                "elements": "A, B, C, D, E, F",
                "target": "A,B,C,D",
                "rule": "proper_subset",
            },
            3: {
                "n": 8,
                "elements": "A, B, C, D, E, F, G, H",
                "target": "A,B,C",
                "rule": "proper_superset",
            },
            4: {
                "n": 10,
                "elements": "A, B, C, D, E, F, G, H, I, J",
                "target": "A,B,C,D,E",
                "rule": "neither",
            },
            5: {
                "n": 10,
                "elements": "A, B, C, D, E, F, G, H, I, J",
                "target": "B,D,F,H,J",
                "rule": "equal",
            },
        },
        "en": {
            1: {
                "n": 5,
                "elements": "A, B, C, D, E",
                "target": "A,B",
                "rule": "equal",
            },
            2: {
                "n": 6,
                "elements": "A, B, C, D, E, F",
                "target": "A,B,C,D",
                "rule": "proper_subset",
            },
            3: {
                "n": 8,
                "elements": "A, B, C, D, E, F, G, H",
                "target": "A,B,C",
                "rule": "proper_superset",
            },
            4: {
                "n": 10,
                "elements": "A, B, C, D, E, F, G, H, I, J",
                "target": "A,B,C,D,E",
                "rule": "neither",
            },
            5: {
                "n": 10,
                "elements": "A, B, C, D, E, F, G, H, I, J",
                "target": "B,D,F,H,J",
                "rule": "equal",
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0
        self.max_queries = 20
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["elements"] = cfg["elements"]
        
        self.target_set = set()
        if cfg["target"]:
            self.target_set = set(x.strip() for x in cfg["target"].split(","))
        
        self.rule_type = cfg["rule"]
        self.universal_set = set(x.strip() for x in cfg["elements"].split(","))

    def _parse_set(self, set_str):
        if not set_str or set_str.strip() == "":
            return set()
        return set(x.strip() for x in set_str.split(",") if x.strip())

    def _check_rule(self, test_set):
        t_equals_c = test_set == self.target_set
        t_subset_c = test_set < self.target_set
        t_superset_c = test_set > self.target_set
        
        if self.rule_type == "equal":
            return t_equals_c
        elif self.rule_type == "proper_subset":
            return t_subset_c
        elif self.rule_type == "proper_superset":
            return t_superset_c
        elif self.rule_type == "neither":
            return not (test_set <= self.target_set or test_set >= self.target_set)
        else:
            raise ValueError(f"Unknown rule type: {self.rule_type}")

    def _parse_rule_description(self, rule_str):
        rule_str = rule_str.strip().lower()
        
        if self.config.language == "zh":
            if "等于" in rule_str and "接受" in rule_str:
                return "equal"
            elif "真子集" in rule_str and "接受" in rule_str:
                return "proper_subset"
            elif "真超集" in rule_str and "接受" in rule_str:
                return "proper_superset"
            elif "既非" in rule_str and "接受" in rule_str:
                return "neither"
        else:
            if "equals" in rule_str and "accept" in rule_str:
                return "equal"
            elif "proper subset" in rule_str and "accept" in rule_str:
                return "proper_subset"
            elif "proper superset" in rule_str and "accept" in rule_str:
                return "proper_superset"
            elif "neither" in rule_str and "accept" in rule_str:
                return "neither"
        
        return None

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        # 使用更稳健的方法来分离 rule 和 target，兼容可能存在的中英文逗号及各种格式偏差
        parts = re.split(r',\s*(?=target=)|，\s*(?=target=)', raw_ans, maxsplit=1)
        if len(parts) < 2:
            parts = raw_ans.split(",", 1)
            
        if len(parts) < 2:
            return False
        
        ans_dict = {}
        for part in parts:
            if "=" in part:
                k, v = part.split("=", 1)
                ans_dict[k.strip()] = v.strip()
        
        if "rule" not in ans_dict or "target" not in ans_dict:
            return False
        
        model_rule = self._parse_rule_description(ans_dict["rule"])
        if model_rule is None or model_rule != self.rule_type:
            return False
        
        model_target = self._parse_set(ans_dict["target"])
        return model_target == self.target_set

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            accept_res, reject_res = "接受", "拒绝"
            yes_res, no_res = "是", "否"
            error_out_of_budget = f"错误：已超过判定查询次数上限（{self.max_queries}次）。"
            error_invalid_element = "错误：集合中包含无效元素。"
            error_duplicate = "错误：集合中存在重复元素。"
            error_invalid_format = "错误：格式无效。"
        else:
            accept_res, reject_res = "Accept", "Reject"
            yes_res, no_res = "Yes", "No"
            error_out_of_budget = f"Error: Exceeded the maximum number of test queries ({self.max_queries})."
            error_invalid_element = "Error: Set contains invalid elements."
            error_duplicate = "Error: Set contains duplicate elements."
            error_invalid_format = "Error: Invalid format."

        if "query_test" in parsed_info:
            if self.query_count >= self.max_queries:
                self.state.set_state("failed", "exceeded max queries")
                return error_out_of_budget
            
            self.query_count += 1
            
            test_str = parsed_info["query_test"].strip()
            test_set = self._parse_set(test_str)
            
            if not test_set.issubset(self.universal_set):
                return error_invalid_element
            
            if test_str:
                input_elements = [x.strip() for x in test_str.split(",") if x.strip()]
                if len(input_elements) != len(test_set):
                    return error_duplicate
            
            is_accept = self._check_rule(test_set)
            return accept_res if is_accept else reject_res

        elif "query_contain" in parsed_info:
            try:
                raw = parsed_info["query_contain"].strip()
                parts = raw.split("|")
                if len(parts) != 2:
                    return error_invalid_format
                
                set_s = self._parse_set(parts[0])
                set_t = self._parse_set(parts[1])
                
                if not set_s.issubset(self.universal_set) or not set_t.issubset(self.universal_set):
                    return error_invalid_element
                
                contains = set_t.issubset(set_s)
                return yes_res if contains else no_res
            except:
                return error_invalid_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if self.config.language == "zh":
            if correct == "接受":
                return "拒绝"
            elif correct == "拒绝":
                return "接受"
            elif correct == "是":
                return "否"
            elif correct == "否":
                return "是"
        else:
            if correct == "Accept":
                return "Reject"
            elif correct == "Reject":
                return "Accept"
            elif correct == "Yes":
                return "No"
            elif correct == "No":
                return "Yes"
        return correct + " [WRONG]"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        if self.config.language == "zh":
            accept_res, reject_res = "接受", "拒绝"
        else:
            accept_res, reject_res = "Accept", "Reject"
            
        elements = sorted(list(self.universal_set))
        n = len(elements)
        
        for r in range(n + 1):
            for combo in itertools.combinations(elements, r):
                query_content = ",".join(combo)
                test_set = set(combo)
                
                is_accept = self._check_rule(test_set)
                ans = accept_res if is_accept else reject_res
                
                queries.append({
                    "query": f"<query_test>{query_content}</query_test>",
                    "answer": ans
                })
                
        return queries