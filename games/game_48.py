from .base import Game
import random

class EquivalenceRuleGame(Game):

    game_rule_zh = """\
我们现在来玩一个"隐藏等价规则"的推理游戏，规则如下：

游戏设定了一个包含 16 个对象的集合，编号为 S01 到 S16。每个对象具有三个离散特征：
- 特征1：取值为 A1, A2, A3, A4 之一
- 特征2：取值为 B1, B2, B3, B4 之一  
- 特征3：取值为 1, 2, 3, 4 之一

所有对象的特征如下：
{objects_description}

我已经秘密设定了一个基于这些特征的判定规则，该规则将 16 个对象划分为若干个互不相交的组。同一组内的对象满足某种特征条件，不同组的对象不满足相同条件。

你的目标是通过提问推断出这个隐藏规则，并能够判断任意两个对象是否属于同一组。

你可以进行以下类型的查询（总次数有限，需尽可能少地使用）：

1. **等价查询**：询问两个对象是否属于同一组
   格式：<query_equiv>Sx,Sy</query_equiv>
   示例：<query_equiv>S01,S05</query_equiv>
   回答：是 或 否

2. **计数查询**：询问给定子集中有多少个对象与指定对象同组
   格式：<query_count>Sx;Sa,Sb,Sc,...</query_count>
   示例：<query_count>S01;S02,S03,S04,S05</query_count>
   回答：一个非负整数

3. **示例查询**：请求给出一个与指定对象同组的其他对象
   格式：<query_example>Sx</query_example>
   示例：<query_example>S01</query_example>
   回答：一个对象编号，或"无"（表示该对象独自成组）

完成学习后，使用以下格式进入挑战阶段：
<enter_challenge></enter_challenge>

系统会给出 {num_challenges} 对对象，你需要判断每一对是否属于同一组。此阶段不能再进行查询。

判定格式：<judge>Sx,Sy,same</judge> 或 <judge>Sx,Sy,different</judge>
示例：<judge>S01,S09,same</judge> 表示认为 S01 和 S09 同组
示例：<judge>S02,S10,different</judge> 表示认为 S02 和 S10 不同组

如果你认为已经完全理解了隐藏规则，可以直接提交规则描述：

<answer>规则描述内容</answer>

规则描述需要用特征1、特征2、特征3的逻辑条件完整表达判定标准。
示例：<answer>特征1的第一个字符与特征2的第一个字符相同的对象为一组</answer>

1. 挑战阶段判定正确数达到 {pass_threshold} 个或以上
2. 规则声明验证通过

1. 挑战阶段判定正确数少于 {pass_threshold} 个
2. 规则声明验证失败
3. 查询格式错误或违反游戏规则
"""

    game_rule_en = """\
Let's play an "Hidden Equivalence Rule" deduction game. Here are the rules:

The game has a set of 16 objects numbered S01 to S16. Each object has three discrete features:
- Feature1: one of A1, A2, A3, A4
- Feature2: one of B1, B2, B3, B4
- Feature3: one of 1, 2, 3, 4

All objects and their features are:
{objects_description}

I have secretly defined a rule based on these features that partitions the 16 objects into several disjoint groups. Objects in the same group satisfy certain feature conditions, while objects in different groups do not.

Your goal is to infer this hidden rule through queries and determine whether any two objects belong to the same group.

You can make the following types of queries (limited total number, use as few as possible):

1. **Equivalence Query**: Ask if two objects belong to the same group
   Format: <query_equiv>Sx,Sy</query_equiv>
   Example: <query_equiv>S01,S05</query_equiv>
   Answer: Yes or No

2. **Count Query**: Ask how many objects in a given subset belong to the same group as a specified object
   Format: <query_count>Sx;Sa,Sb,Sc,...</query_count>
   Example: <query_count>S01;S02,S03,S04,S05</query_count>
   Answer: A non-negative integer

3. **Example Query**: Request an object that belongs to the same group as a specified object
   Format: <query_example>Sx</query_example>
   Example: <query_example>S01</query_example>
   Answer: An object ID, or "None" (if the object forms a singleton group)

After learning, enter the challenge phase with:
<enter_challenge></enter_challenge>

The system will provide {num_challenges} pairs of objects. You must judge whether each pair belongs to the same group. No more queries are allowed in this phase.

Judgment format: <judge>Sx,Sy,same</judge> or <judge>Sx,Sy,different</judge>
Example: <judge>S01,S09,same</judge> means S01 and S09 are in the same group
Example: <judge>S02,S10,different</judge> means S02 and S10 are in different groups

If you believe you fully understand the hidden rule, you can directly submit a rule description:

<answer>Rule description content</answer>

The rule description must fully express the judgment criteria using logical conditions on Feature1, Feature2, and Feature3.
Example: <answer>Objects where the first character of Feature1 matches the first character of Feature2 form a group</answer>

1. At least {pass_threshold} correct judgments in the challenge phase
2. Rule declaration verified as correct

1. Fewer than {pass_threshold} correct judgments in the challenge phase
2. Rule declaration verification failed
3. Query format error or rule violation
"""

    contextualized_rule_zh_1 = """\
欢迎进入智能交通管控系统。我们现在需要进行一项"交通节点协同分组"的配置任务，规则如下：

系统监测到一个包含 16 个交通节点的集合，编号为 S01 到 S16。每个节点具有三个离散特征属性：
- 道路等级（特征1）：取值为 A1, A2, A3, A4 之一
- 信号类型（特征2）：取值为 B1, B2, B3, B4 之一  
- 流量等级（特征3）：取值为 1, 2, 3, 4 之一

所有交通节点的属性如下：
{objects_description}

系统已经秘密生成了一个基于这些特征的协同控制规则，该规则将 16 个交通节点划分为若干个互不相交的协同组。同一组内的节点满足某种特征条件以便进行绿波带联动，不同组的节点不满足相同条件。

你的目标是通过发送探测指令推断出这个隐藏的协同规则，并能够判断任意两个交通节点是否属于同一协同组。

你可以进行以下类型的指令查询（总次数有限，需尽可能少地使用）：

1. **等价查询**：询问两个交通节点是否属于同一协同组
   格式：<query_equiv>Sx,Sy</query_equiv>
   示例：<query_equiv>S01,S05</query_equiv>
   回答：是 或 否

2. **计数查询**：询问给定子集中有多少个交通节点与指定节点同组
   格式：<query_count>Sx;Sa,Sb,Sc,...</query_count>
   示例：<query_count>S01;S02,S03,S04,S05</query_count>
   回答：一个非负整数

3. **示例查询**：请求给出一个与指定交通节点同组的其他节点
   格式：<query_example>Sx</query_example>
   示例：<query_example>S01</query_example>
   回答：一个节点编号，或"无"（表示该节点独自成组）

完成勘测后，使用以下格式进入部署阶段：
<enter_challenge></enter_challenge>

系统会给出 {num_challenges} 对交通节点，你需要判断每一对是否属于同一协同组。此阶段不能再进行查询。

判定格式：<judge>Sx,Sy,same</judge> 或 <judge>Sx,Sy,different</judge>
示例：<judge>S01,S09,same</judge> 表示认为 S01 和 S09 同组
示例：<judge>S02,S10,different</judge> 表示认为 S02 和 S10 不同组

如果你认为已经完全理解了隐藏的协同规则，可以直接提交规则描述：

<answer>规则描述内容</answer>

规则描述需要用特征1、特征2、特征3的逻辑条件完整表达判定标准。
示例：<answer>特征1的第一个字符与特征2的第一个字符相同的节点为一组</answer>

1. 部署阶段判定正确数达到 {pass_threshold} 个或以上
2. 规则声明验证通过

1. 部署阶段判定正确数少于 {pass_threshold} 个
2. 规则声明验证失败
3. 查询格式错误或违反系统规则
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Intelligent Traffic Control System. We need to perform a "Traffic Node Coordinated Grouping" configuration task. The rules are as follows:

The system monitors a set of 16 traffic nodes, numbered S01 to S16. Each node has three discrete feature attributes:
- Road Level (Feature1): one of A1, A2, A3, A4
- Signal Type (Feature2): one of B1, B2, B3, B4
- Traffic Volume Level (Feature3): one of 1, 2, 3, 4

All traffic nodes and their attributes are:
{objects_description}

The system has secretly generated a coordinated control rule based on these features that partitions the 16 nodes into several disjoint coordination groups. Nodes in the same group satisfy certain feature conditions for green wave linkage, while nodes in different groups do not.

Your goal is to infer this hidden coordination rule through probe commands and determine whether any two traffic nodes belong to the same coordination group.

You can make the following types of queries (limited total number, use as few as possible):

1. **Equivalence Query**: Ask if two traffic nodes belong to the same group
   Format: <query_equiv>Sx,Sy</query_equiv>
   Example: <query_equiv>S01,S05</query_equiv>
   Answer: Yes or No

2. **Count Query**: Ask how many nodes in a given subset belong to the same group as a specified node
   Format: <query_count>Sx;Sa,Sb,Sc,...</query_count>
   Example: <query_count>S01;S02,S03,S04,S05</query_count>
   Answer: A non-negative integer

3. **Example Query**: Request a node that belongs to the same group as a specified node
   Format: <query_example>Sx</query_example>
   Example: <query_example>S01</query_example>
   Answer: A node ID, or "None" (if the node forms a singleton group)

After the survey, enter the deployment phase with:
<enter_challenge></enter_challenge>

The system will provide {num_challenges} pairs of traffic nodes. You must judge whether each pair belongs to the same group. No more queries are allowed in this phase.

Judgment format: <judge>Sx,Sy,same</judge> or <judge>Sx,Sy,different</judge>
Example: <judge>S01,S09,same</judge> means S01 and S09 are in the same group
Example: <judge>S02,S10,different</judge> means S02 and S10 are in different groups

If you believe you fully understand the hidden coordination rule, you can directly submit a rule description:

<answer>Rule description content</answer>

The rule description must fully express the judgment criteria using logical conditions on Feature1, Feature2, and Feature3.
Example: <answer>Nodes where the first character of Feature1 matches the first character of Feature2 form a group</answer>

1. At least {pass_threshold} correct judgments in the deployment phase
2. Rule declaration verified as correct

1. Fewer than {pass_threshold} correct judgments in the deployment phase
2. Rule declaration verification failed
3. Query format error or system rule violation
"""

    contextualized_rule_zh_2 = """\
欢迎来到精准医疗研究中心。我们正在进行一项"临床样本同构分组"的病理分析任务，规则如下：

研究库中包含 16 个临床样本，编号为 S01 到 S16。每个样本具有三个离散生物特征：
- 基因表达型（特征1）：取值为 A1, A2, A3, A4 之一
- 蛋白质亚型（特征2）：取值为 B1, B2, B3, B4 之一  
- 临床分期（特征3）：取值为 1, 2, 3, 4 之一

所有样本的特征如下：
{objects_description}

系统已经秘密设定了一个基于这些特征的病理判定规则，该规则将 16 个样本划分为若干个互不相交的治疗靶向组。同一组内的样本满足某种特征条件以适用相同靶向药物，不同组的样本不满足相同条件。

你的目标是通过实验查询推断出这个隐藏的病理规则，并能够判断任意两个样本是否属于同一治疗靶向组。

你可以进行以下类型的化验查询（总次数有限，需尽可能少地使用）：

1. **等价查询**：询问两个样本是否属于同一靶向组
   格式：<query_equiv>Sx,Sy</query_equiv>
   示例：<query_equiv>S01,S05</query_equiv>
   回答：是 或 否

2. **计数查询**：询问给定子集中有多少个样本与指定样本同组
   格式：<query_count>Sx;Sa,Sb,Sc,...</query_count>
   示例：<query_count>S01;S02,S03,S04,S05</query_count>
   回答：一个非负整数

3. **示例查询**：请求给出一个与指定样本同组的其他样本
   格式：<query_example>Sx</query_example>
   示例：<query_example>S01</query_example>
   回答：一个样本编号，或"无"（表示该样本独自成组）

完成化验后，使用以下格式进入诊断阶段：
<enter_challenge></enter_challenge>

系统会给出 {num_challenges} 对样本，你需要判断每一对是否属于同一靶向组。此阶段不能再进行查询。

判定格式：<judge>Sx,Sy,same</judge> 或 <judge>Sx,Sy,different</judge>
示例：<judge>S01,S09,same</judge> 表示认为 S01 和 S09 同组
示例：<judge>S02,S10,different</judge> 表示认为 S02 和 S10 不同组

如果你认为已经完全理解了隐藏的病理规则，可以直接提交规则描述：

<answer>规则描述内容</answer>

规则描述需要用特征1、特征2、特征3的逻辑条件完整表达判定标准。
示例：<answer>特征1的第一个字符与特征2的第一个字符相同的样本为一组</answer>

1. 诊断阶段判定正确数达到 {pass_threshold} 个或以上
2. 规则声明验证通过

1. 诊断阶段判定正确数少于 {pass_threshold} 个
2. 规则声明验证失败
3. 查询格式错误或违反临床规则
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Precision Medicine Research Center. We are conducting a "Clinical Sample Isomorphic Grouping" pathological analysis task. The rules are as follows:

The research repository contains 16 clinical samples, numbered S01 to S16. Each sample has three discrete biological features:
- Gene Expression Type (Feature1): one of A1, A2, A3, A4
- Protein Subtype (Feature2): one of B1, B2, B3, B4
- Clinical Stage (Feature3): one of 1, 2, 3, 4

All samples and their features are:
{objects_description}

The system has secretly established a pathological judgment rule based on these features that partitions the 16 samples into several disjoint targeted therapy groups. Samples in the same group satisfy certain feature conditions for the same targeted drug, while samples in different groups do not.

Your goal is to infer this hidden pathological rule through experimental queries and determine whether any two samples belong to the same targeted therapy group.

You can make the following types of assay queries (limited total number, use as few as possible):

1. **Equivalence Query**: Ask if two samples belong to the same targeted group
   Format: <query_equiv>Sx,Sy</query_equiv>
   Example: <query_equiv>S01,S05</query_equiv>
   Answer: Yes or No

2. **Count Query**: Ask how many samples in a given subset belong to the same group as a specified sample
   Format: <query_count>Sx;Sa,Sb,Sc,...</query_count>
   Example: <query_count>S01;S02,S03,S04,S05</query_count>
   Answer: A non-negative integer

3. **Example Query**: Request a sample that belongs to the same group as a specified sample
   Format: <query_example>Sx</query_example>
   Example: <query_example>S01</query_example>
   Answer: A sample ID, or "None" (if the sample forms a singleton group)

After the assays, enter the diagnostic phase with:
<enter_challenge></enter_challenge>

The system will provide {num_challenges} pairs of samples. You must judge whether each pair belongs to the same group. No more queries are allowed in this phase.

Judgment format: <judge>Sx,Sy,same</judge> or <judge>Sx,Sy,different</judge>
Example: <judge>S01,S09,same</judge> means S01 and S09 are in the same group
Example: <judge>S02,S10,different</judge> means S02 and S10 are in different groups

If you believe you fully understand the hidden pathological rule, you can directly submit a rule description:

<answer>Rule description content</answer>

The rule description must fully express the judgment criteria using logical conditions on Feature1, Feature2, and Feature3.
Example: <answer>Samples where the first character of Feature1 matches the first character of Feature2 form a group</answer>

1. At least {pass_threshold} correct judgments in the diagnostic phase
2. Rule declaration verified as correct

1. Fewer than {pass_threshold} correct judgments in the diagnostic phase
2. Rule declaration verification failed
3. Query format error or clinical rule violation
"""

    contextualized_rule_zh_3 = """\
欢迎来到智慧教育管理平台。我们需要完成一项"学生学习小组分配"的教务编排任务，规则如下：

班级中包含 16 名学生，学号为 S01 到 S16。每位学生具有三个离散维度的学情特征：
- 认知风格（特征1）：取值为 A1, A2, A3, A4 之一
- 优势学科（特征2）：取值为 B1, B2, B3, B4 之一  
- 综合评级（特征3）：取值为 1, 2, 3, 4 之一

所有学生的学情特征如下：
{objects_description}

系统内置了一个基于这些特征的差异化教学分组规则，该规则将 16 名学生划分为若干个互不相交的互助学习组。同一组内的学生满足某种特征条件以达成互补或共振，不同组的学生不满足相同条件。

你的目标是通过教务查询推断出这个隐藏的分组规则，并能够判断任意两名学生是否属于同一互助学习组。

你可以进行以下类型的教务查询（总次数有限，需尽可能少地使用）：

1. **等价查询**：询问两名学生是否属于同一学习组
   格式：<query_equiv>Sx,Sy</query_equiv>
   示例：<query_equiv>S01,S05</query_equiv>
   回答：是 或 否

2. **计数查询**：询问给定子集中有多少名学生与指定学生同组
   格式：<query_count>Sx;Sa,Sb,Sc,...</query_count>
   示例：<query_count>S01;S02,S03,S04,S05</query_count>
   回答：一个非负整数

3. **示例查询**：请求给出一名与指定学生同组的其他学生
   格式：<query_example>Sx</query_example>
   示例：<query_example>S01</query_example>
   回答：一个学生学号，或"无"（表示该学生独自成组）

完成摸底后，使用以下格式进入排课阶段：
<enter_challenge></enter_challenge>

系统会给出 {num_challenges} 对学生，你需要判断每一对是否属于同一学习组。此阶段不能再进行查询。

判定格式：<judge>Sx,Sy,same</judge> 或 <judge>Sx,Sy,different</judge>
示例：<judge>S01,S09,same</judge> 表示认为 S01 和 S09 同组
示例：<judge>S02,S10,different</judge> 表示认为 S02 和 S10 不同组

如果你认为已经完全理解了隐藏的教学分组规则，可以直接提交规则描述：

<answer>规则描述内容</answer>

规则描述需要用特征1、特征2、特征3的逻辑条件完整表达判定标准。
示例：<answer>特征1的第一个字符与特征2的第一个字符相同的学生为一组</answer>

1. 排课阶段判定正确数达到 {pass_threshold} 个或以上
2. 规则声明验证通过

1. 排课阶段判定正确数少于 {pass_threshold} 个
2. 规则声明验证失败
3. 查询格式错误或违反教务规则
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Smart Education Management Platform. We need to complete a "Student Study Group Allocation" pedagogical scheduling task. The rules are as follows:

The class contains 16 students, with student IDs S01 to S16. Each student has three discrete dimensions of learning profile features:
- Cognitive Style (Feature1): one of A1, A2, A3, A4
- Dominant Subject (Feature2): one of B1, B2, B3, B4
- Comprehensive Rating (Feature3): one of 1, 2, 3, 4

All students and their learning profile features are:
{objects_description}

The system has a built-in differentiated instructional grouping rule based on these features that partitions the 16 students into several disjoint peer-learning groups. Students in the same group satisfy certain feature conditions to achieve complementarity or resonance, while students in different groups do not.

Your goal is to infer this hidden grouping rule through pedagogical queries and determine whether any two students belong to the same peer-learning group.

You can make the following types of pedagogical queries (limited total number, use as few as possible):

1. **Equivalence Query**: Ask if two students belong to the same study group
   Format: <query_equiv>Sx,Sy</query_equiv>
   Example: <query_equiv>S01,S05</query_equiv>
   Answer: Yes or No

2. **Count Query**: Ask how many students in a given subset belong to the same group as a specified student
   Format: <query_count>Sx;Sa,Sb,Sc,...</query_count>
   Example: <query_count>S01;S02,S03,S04,S05</query_count>
   Answer: A non-negative integer

3. **Example Query**: Request a student that belongs to the same group as a specified student
   Format: <query_example>Sx</query_example>
   Example: <query_example>S01</query_example>
   Answer: A student ID, or "None" (if the student forms a singleton group)

After the assessment, enter the scheduling phase with:
<enter_challenge></enter_challenge>

The system will provide {num_challenges} pairs of students. You must judge whether each pair belongs to the same group. No more queries are allowed in this phase.

Judgment format: <judge>Sx,Sy,same</judge> or <judge>Sx,Sy,different</judge>
Example: <judge>S01,S09,same</judge> means S01 and S09 are in the same group
Example: <judge>S02,S10,different</judge> means S02 and S10 are in different groups

If you believe you fully understand the hidden instructional grouping rule, you can directly submit a rule description:

<answer>Rule description content</answer>

The rule description must fully express the judgment criteria using logical conditions on Feature1, Feature2, and Feature3.
Example: <answer>Students where the first character of Feature1 matches the first character of Feature2 form a group</answer>

1. At least {pass_threshold} correct judgments in the scheduling phase
2. Rule declaration verified as correct

1. Fewer than {pass_threshold} correct judgments in the scheduling phase
2. Rule declaration verification failed
3. Query format error or pedagogical rule violation
"""

    contextualized_rule_zh_4 = """\
欢迎进入柔性制造执行系统（MES）。我们需要进行一项"零部件装配线批次归类"的任务，规则如下：

待处理区有一个包含 16 个零部件的批次，编号为 S01 到 S16。每个零部件具有三个离散工艺特征：
- 材质规格（特征1）：取值为 A1, A2, A3, A4 之一
- 表面处理工艺（特征2）：取值为 B1, B2, B3, B4 之一  
- 强度等级（特征3）：取值为 1, 2, 3, 4 之一

所有零部件的工艺特征如下：
{objects_description}

系统已经预设了一个基于这些工艺特征的产线分配规则，该规则将 16 个零部件划分为若干个互不相交的生产批次组。同一组内的零部件满足某种特征条件以送往同一条自动化装配线，不同组的零部件则不满足相同条件。

你的目标是通过调用质检接口推断出这个隐藏的分配规则，并能够判断任意两个零部件是否属于同一生产批次组。

你可以调用以下类型的质检接口查询（总调用次数有限，需尽可能少地使用）：

1. **等价查询**：询问两个零部件是否属于同装配线批次
   格式：<query_equiv>Sx,Sy</query_equiv>
   示例：<query_equiv>S01,S05</query_equiv>
   回答：是 或 否

2. **计数查询**：询问给定子集中有多少个零部件与指定零部件同批次
   格式：<query_count>Sx;Sa,Sb,Sc,...</query_count>
   示例：<query_count>S01;S02,S03,S04,S05</query_count>
   回答：一个非负整数

3. **示例查询**：请求给出一个与指定零部件同批次的其他零部件
   格式：<query_example>Sx</query_example>
   示例：<query_example>S01</query_example>
   回答：一个零部件编号，或"无"（表示该零部件单独作为一个批次）

完成抽检后，使用以下格式进入投产阶段：
<enter_challenge></enter_challenge>

系统会给出 {num_challenges} 对零部件，你需要判断每一对是否属于同一生产批次组。此阶段不能再调用查询接口。

判定格式：<judge>Sx,Sy,same</judge> 或 <judge>Sx,Sy,different</judge>
示例：<judge>S01,S09,same</judge> 表示认为 S01 和 S09 同组
示例：<judge>S02,S10,different</judge> 表示认为 S02 和 S10 不同组

如果你认为已经完全解析了隐藏的产线分配规则，可以直接提交规则描述：

<answer>规则描述内容</answer>

规则描述需要用特征1、特征2、特征3的逻辑条件完整表达判定标准。
示例：<answer>特征1的第一个字符与特征2的第一个字符相同的零部件为一组</answer>

1. 投产阶段判定正确数达到 {pass_threshold} 个或以上
2. 规则声明验证通过

1. 投产阶段判定正确数少于 {pass_threshold} 个
2. 规则声明验证失败
3. 接口调用格式错误或违反工艺规则
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Flexible Manufacturing Execution System (MES). We need to perform a "Component Assembly Line Batch Classification" task. The rules are as follows:

The pending area has a batch containing 16 components, numbered S01 to S16. Each component has three discrete process features:
- Material Specification (Feature1): one of A1, A2, A3, A4
- Surface Treatment Process (Feature2): one of B1, B2, B3, B4
- Strength Grade (Feature3): one of 1, 2, 3, 4

All components and their process features are:
{objects_description}

The system has preset a production line allocation rule based on these process features that partitions the 16 components into several disjoint production batch groups. Components in the same group satisfy certain feature conditions to be routed to the same automated assembly line, while components in different groups do not.

Your goal is to infer this hidden allocation rule by invoking quality inspection interfaces and determine whether any two components belong to the same production batch group.

You can invoke the following types of quality inspection interface queries (limited total number, use as few as possible):

1. **Equivalence Query**: Ask if two components belong to the same assembly line batch
   Format: <query_equiv>Sx,Sy</query_equiv>
   Example: <query_equiv>S01,S05</query_equiv>
   Answer: Yes or No

2. **Count Query**: Ask how many components in a given subset belong to the same batch as a specified component
   Format: <query_count>Sx;Sa,Sb,Sc,...</query_count>
   Example: <query_count>S01;S02,S03,S04,S05</query_count>
   Answer: A non-negative integer

3. **Example Query**: Request a component that belongs to the same batch as a specified component
   Format: <query_example>Sx</query_example>
   Example: <query_example>S01</query_example>
   Answer: A component ID, or "None" (if the component forms a singleton batch)

After sampling, enter the production phase with:
<enter_challenge></enter_challenge>

The system will provide {num_challenges} pairs of components. You must judge whether each pair belongs to the same batch. No more queries are allowed in this phase.

Judgment format: <judge>Sx,Sy,same</judge> or <judge>Sx,Sy,different</judge>
Example: <judge>S01,S09,same</judge> means S01 and S09 are in the same group
Example: <judge>S02,S10,different</judge> means S02 and S10 are in different groups

If you believe you fully resolved the hidden production line allocation rule, you can directly submit a rule description:

<answer>Rule description content</answer>

The rule description must fully express the judgment criteria using logical conditions on Feature1, Feature2, and Feature3.
Example: <answer>Components where the first character of Feature1 matches the first character of Feature2 form a group</answer>

1. At least {pass_threshold} correct judgments in the production phase
2. Rule declaration verified as correct

1. Fewer than {pass_threshold} correct judgments in the production phase
2. Rule declaration verification failed
3. Interface call format error or process rule violation
"""

    contextualized_rule_zh_5 = """\
欢迎登录智能司法立案分拨系统。目前需要进行一项"诉讼卷宗管辖归类"的审查任务，规则如下：

待分拨池中包含 16 份诉讼卷宗，案号为 S01 到 S16。每份卷宗包含三个离散案件特征：
- 案由性质（特征1）：取值为 A1, A2, A3, A4 之一
- 核心证据类型（特征2）：取值为 B1, B2, B3, B4 之一  
- 争议标的额度（特征3）：取值为 1, 2, 3, 4 之一

所有卷宗的案件特征如下：
{objects_description}

系统已内置了一套基于上述特征的司法管辖判定规则，该规则将 16 份卷宗划分为若干个互不相交的审理程序组。同一组内的卷宗满足某种特征条件以分配至相同的专项审判庭或适用同一审理程序，不同组的卷宗则不满足相同条件。

你的目标是通过检索司法预案推断出这套隐藏的管辖规则，并能够判断任意两份卷宗是否属于同一审理程序组。

你可以进行以下类型的预案检索（总检索次数有限，需尽可能少地使用）：

1. **等价查询**：询问两份卷宗是否归属同一审理程序组
   格式：<query_equiv>Sx,Sy</query_equiv>
   示例：<query_equiv>S01,S05</query_equiv>
   回答：是 或 否

2. **计数查询**：询问给定子集中有多少份卷宗与指定卷宗同组
   格式：<query_count>Sx;Sa,Sb,Sc,...</query_count>
   示例：<query_count>S01;S02,S03,S04,S05</query_count>
   回答：一个非负整数

3. **示例查询**：请求给出一份与指定卷宗同组的其他卷宗
   格式：<query_example>Sx</query_example>
   示例：<query_example>S01</query_example>
   回答：一个卷宗案号，或"无"（表示该卷宗单独成组）

完成阅卷后，使用以下格式进入立案阶段：
<enter_challenge></enter_challenge>

系统会给出 {num_challenges} 对卷宗，你需要判断每一对是否属于同一审理程序组。此阶段不能再进行检索。

判定格式：<judge>Sx,Sy,same</judge> 或 <judge>Sx,Sy,different</judge>
示例：<judge>S01,S09,same</judge> 表示认为 S01 和 S09 同组
示例：<judge>S02,S10,different</judge> 表示认为 S02 和 S10 不同组

如果你认为已经完全厘清了隐藏的管辖分配规则，可以直接提交规则描述：

<answer>规则描述内容</answer>

规则描述需要用特征1、特征2、特征3的逻辑条件完整表达判定标准。
示例：<answer>特征1的第一个字符与特征2的第一个字符相同的卷宗为一组</answer>

1. 立案阶段判定正确数达到 {pass_threshold} 个或以上
2. 规则声明验证通过

1. 立案阶段判定正确数少于 {pass_threshold} 个
2. 规则声明验证失败
3. 检索格式错误或违反司法程序规则
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Intelligent Judicial Case Filing and Allocation System. We need to perform a "Litigation Dossier Jurisdictional Classification" review task. The rules are as follows:

The pending allocation pool contains 16 litigation dossiers, with case numbers S01 to S16. Each dossier contains three discrete case features:
- Nature of Cause of Action (Feature1): one of A1, A2, A3, A4
- Core Evidence Type (Feature2): one of B1, B2, B3, B4
- Amount in Controversy (Feature3): one of 1, 2, 3, 4

All dossiers and their case features are:
{objects_description}

The system has a built-in judicial jurisdiction judgment rule based on the above features that partitions the 16 dossiers into several disjoint trial procedure groups. Dossiers in the same group satisfy certain feature conditions to be assigned to the same specialized tribunal or apply the same trial procedure, while dossiers in different groups do not.

Your goal is to infer this hidden jurisdictional rule by retrieving judicial precedents and determine whether any two dossiers belong to the same trial procedure group.

You can conduct the following types of precedent retrievals (limited total number, use as few as possible):

1. **Equivalence Query**: Ask if two dossiers belong to the same trial procedure group
   Format: <query_equiv>Sx,Sy</query_equiv>
   Example: <query_equiv>S01,S05</query_equiv>
   Answer: Yes or No

2. **Count Query**: Ask how many dossiers in a given subset belong to the same group as a specified dossier
   Format: <query_count>Sx;Sa,Sb,Sc,...</query_count>
   Example: <query_count>S01;S02,S03,S04,S05</query_count>
   Answer: A non-negative integer

3. **Example Query**: Request a dossier that belongs to the same group as a specified dossier
   Format: <query_example>Sx</query_example>
   Example: <query_example>S01</query_example>
   Answer: A dossier case number, or "None" (if the dossier forms a singleton group)

After reviewing the dossiers, enter the filing phase with:
<enter_challenge></enter_challenge>

The system will provide {num_challenges} pairs of dossiers. You must judge whether each pair belongs to the same trial procedure group. No more retrievals are allowed in this phase.

Judgment format: <judge>Sx,Sy,same</judge> or <judge>Sx,Sy,different</judge>
Example: <judge>S01,S09,same</judge> means S01 and S09 are in the same group
Example: <judge>S02,S10,different</judge> means S02 and S10 are in different groups

If you believe you have fully clarified the hidden jurisdictional allocation rule, you can directly submit a rule description:

<answer>Rule description content</answer>

The rule description must fully express the judgment criteria using logical conditions on Feature1, Feature2, and Feature3.
Example: <answer>Dossiers where the first character of Feature1 matches the first character of Feature2 form a group</answer>

1. At least {pass_threshold} correct judgments in the filing phase
2. Rule declaration verified as correct

1. Fewer than {pass_threshold} correct judgments in the filing phase
2. Rule declaration verification failed
3. Retrieval format error or judicial procedure rule violation
"""

    tags = ["answer", "query_equiv", "query_count", "query_example", "enter_challenge", "judge"]
    
    reasoning_type = "归纳推理"
    data_structure = "集合"

    OBJECTS = {
        "S01": ("A1", "B1", "1"), "S02": ("A1", "B1", "3"),
        "S03": ("A1", "B2", "2"), "S04": ("A1", "B2", "4"),
        "S05": ("A2", "B1", "2"), "S06": ("A2", "B1", "4"),
        "S07": ("A2", "B2", "1"), "S08": ("A2", "B2", "3"),
        "S09": ("A3", "B3", "1"), "S10": ("A3", "B3", "4"),
        "S11": ("A3", "B4", "2"), "S12": ("A3", "B4", "3"),
        "S13": ("A4", "B3", "2"), "S14": ("A4", "B3", "3"),
        "S15": ("A4", "B4", "1"), "S16": ("A4", "B4", "4"),
    }

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "description": "简单难度",
                "rule_func": lambda f1, f2, f3: "odd" if int(f3) % 2 == 1 else "even",
                "rule_text": "特征3为奇数的对象为一组，特征3为偶数的对象为另一组",
                "max_queries": 15,
                "num_challenges": 6,
                "pass_threshold": 5,
            },
            2: {
                "description": "中等偏下难度",
                "rule_func": lambda f1, f2, f3: f1,
                "rule_text": "特征1相同的对象属于同一组",
                "max_queries": 14,
                "num_challenges": 6,
                "pass_threshold": 5,
            },
            3: {
                "description": "中等偏上难度",
                "rule_func": lambda f1, f2, f3: f1[1] + f2[1],
                "rule_text": "特征1的第二个字符与特征2的第二个字符构成的组合相同的对象属于同一组",
                "max_queries": 13,
                "num_challenges": 6,
                "pass_threshold": 5,
            },
            4: {
                "description": "较难难度",
                "rule_func": lambda f1, f2, f3: "odd" if (int(f1[1]) + int(f3)) % 2 == 1 else "even",
                "rule_text": "特征1中的数字与特征3的和为奇数的对象为一组，和为偶数的对象为另一组",
                "max_queries": 12,
                "num_challenges": 6,
                "pass_threshold": 5,
            },
            5: {
                "description": "困难难度",
                "rule_func": lambda f1, f2, f3: str((int(f1[1]) + int(f2[1])) % 3),
                "rule_text": "特征1的数字部分与特征2的数字部分之和除以3的余数相同的对象属于同一组",
                "max_queries": 12,
                "num_challenges": 6,
                "pass_threshold": 6,
            },
        },
        "en": {
            1: {
                "description": "Easy",
                "rule_func": lambda f1, f2, f3: "odd" if int(f3) % 2 == 1 else "even",
                "rule_text": "Objects with odd Feature3 form one group, objects with even Feature3 form another",
                "max_queries": 15,
                "num_challenges": 6,
                "pass_threshold": 5,
            },
            2: {
                "description": "Medium-Easy",
                "rule_func": lambda f1, f2, f3: f1,
                "rule_text": "Objects with the same Feature1 belong to the same group",
                "max_queries": 14,
                "num_challenges": 6,
                "pass_threshold": 5,
            },
            3: {
                "description": "Medium-Hard",
                "rule_func": lambda f1, f2, f3: f1[1] + f2[1],
                "rule_text": "Objects with the same combination of the second character of Feature1 and Feature2 belong to the same group",
                "max_queries": 13,
                "num_challenges": 6,
                "pass_threshold": 5,
            },
            4: {
                "description": "Hard",
                "rule_func": lambda f1, f2, f3: "odd" if (int(f1[1]) + int(f3)) % 2 == 1 else "even",
                "rule_text": "Objects where the digit in Feature1 plus Feature3 is odd form one group, even sum forms another",
                "max_queries": 12,
                "num_challenges": 6,
                "pass_threshold": 5,
            },
            5: {
                "description": "Very Hard",
                "rule_func": lambda f1, f2, f3: str((int(f1[1]) + int(f2[1])) % 3),
                "rule_text": "Objects where the sum of digits in Feature1 and Feature2 modulo 3 is the same belong to the same group",
                "max_queries": 12,
                "num_challenges": 6,
                "pass_threshold": 6,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        if lang == "zh":
            obj_desc = "\n".join([
                f"- {oid}: 特征1={f[0]}, 特征2={f[1]}, 特征3={f[2]}"
                for oid, f in self.OBJECTS.items()
            ])
        else:
            obj_desc = "\n".join([
                f"- {oid}: Feature1={f[0]}, Feature2={f[1]}, Feature3={f[2]}"
                for oid, f in self.OBJECTS.items()
            ])

        self._game_info["objects_description"] = obj_desc
        self._game_info["num_challenges"] = cfg["num_challenges"]
        self._game_info["pass_threshold"] = cfg["pass_threshold"]

        self.rule_func = cfg["rule_func"]
        self.rule_text = cfg["rule_text"]
        self.max_queries = cfg["max_queries"]
        self.num_challenges = cfg["num_challenges"]
        self.pass_threshold = cfg["pass_threshold"]

        self.group_map = {}
        for oid, (f1, f2, f3) in self.OBJECTS.items():
            self.group_map[oid] = self.rule_func(f1, f2, f3)

        self.query_count = 0
        self.in_challenge = False
        self.queried_pairs = set()
        
        self.challenge_pairs = []
        self.challenge_answers = {}
        self.judgments = []

    def _same_group(self, oid1, oid2):
        return self.group_map[oid1] == self.group_map[oid2]

    def _validate_object_id(self, oid):
        return oid in self.OBJECTS

    def _verify_rule(self, rule_description):
        desc_lower = rule_description.lower().strip()
        rule_lower = self.rule_text.lower().strip()
        
        if desc_lower == rule_lower:
            return True
        
        lang = self.config.language
        diff = int(self.config.difficulty)
        
        if diff == 1:
            keywords = ["feature3", "odd", "even", "奇", "偶", "特征3"]
        elif diff == 2:
            keywords = ["feature1", "same", "相同", "特征1"]
        elif diff == 3:
            keywords = ["feature1", "feature2", "second", "character", "第二", "字符", "特征1", "特征2"]
        elif diff == 4:
            keywords = ["feature1", "feature3", "sum", "odd", "even", "和", "奇", "偶"]
        elif diff == 5:
            keywords = ["feature1", "feature2", "mod", "remainder", "余数", "modulo"]
        else:
            keywords = []
        
        if not keywords:
            return False
            
        matched = sum(1 for kw in keywords if kw in desc_lower)
        return matched >= max(1, len(keywords) // 2)

    def evaluate(self, parsed_info):
        rule_desc = parsed_info["answer"].strip()
        return self._verify_rule(rule_desc)

    def _cf_core_produce(self, parsed_info):
        lang = self.config.language
        yes_word = "是" if lang == "zh" else "Yes"
        no_word = "否" if lang == "zh" else "No"
        none_word = "无" if lang == "zh" else "None"
        error_prefix = "错误：" if lang == "zh" else "Error: "
        
        if "enter_challenge" in parsed_info:
            if self.in_challenge:
                return f"{error_prefix}{'已经在挑战阶段' if lang == 'zh' else 'Already in challenge phase'}"
            
            all_ids = list(self.OBJECTS.keys())
            available_pairs = []
            for i in range(len(all_ids)):
                for j in range(i + 1, len(all_ids)):
                    pair = tuple(sorted([all_ids[i], all_ids[j]]))
                    if pair not in self.queried_pairs:
                        available_pairs.append(pair)
            
            if len(available_pairs) < self.num_challenges:
                return f"{error_prefix}{'可用配对不足' if lang == 'zh' else 'Not enough available pairs'}"
            
            rng = random.Random(42)
            rng.shuffle(available_pairs)
            self.challenge_pairs = available_pairs[:self.num_challenges]
            self.in_challenge = True
            
            if lang == "zh":
                pairs_str = "\n".join([f"{i+1}. {p[0]} 与 {p[1]}" for i, p in enumerate(self.challenge_pairs)])
                return f"进入挑战阶段。请对以下配对进行判定：\n{pairs_str}"
            else:
                pairs_str = "\n".join([f"{i+1}. {p[0]} and {p[1]}" for i, p in enumerate(self.challenge_pairs)])
                return f"Entering challenge phase. Please judge the following pairs:\n{pairs_str}"

        if "judge" in parsed_info:
            if not self.in_challenge:
                return f"{error_prefix}{'尚未进入挑战阶段' if lang == 'zh' else 'Not in challenge phase yet'}"
            
            try:
                parts = parsed_info["judge"].split(",")
                if len(parts) != 3:
                    raise ValueError
                oid1, oid2, judgment = parts[0].strip(), parts[1].strip(), parts[2].strip()
                
                if not self._validate_object_id(oid1) or not self._validate_object_id(oid2):
                    raise ValueError
                
                pair = tuple(sorted([oid1, oid2]))
                if pair not in self.challenge_pairs:
                    return f"{error_prefix}{'该配对不在挑战列表中' if lang == 'zh' else 'Pair not in challenge list'}"
                
                if pair in self.challenge_answers:
                    return f"{error_prefix}{'该配对已判定过' if lang == 'zh' else 'Pair already judged'}"
                
                is_same = self._same_group(oid1, oid2)
                if judgment == "same":
                    correct = is_same
                elif judgment == "different":
                    correct = not is_same
                else:
                    raise ValueError
                
                self.challenge_answers[pair] = correct
                self.judgments.append(correct)
                
                if len(self.challenge_answers) == self.num_challenges:
                    correct_count = sum(self.judgments)
                    if correct_count >= self.pass_threshold:
                        self.state.set_state("success", "challenge_passed")
                        if lang == "zh":
                            msg = f"挑战完成！正确 {correct_count}/{self.num_challenges}，游戏胜利！"
                        else:
                            msg = f"Challenge completed! {correct_count}/{self.num_challenges} correct. Victory!"
                    else:
                        self.state.set_state("failed", "challenge_failed")
                        if lang == "zh":
                            msg = f"挑战完成。正确 {correct_count}/{self.num_challenges}，未达到要求，游戏失败。"
                        else:
                            msg = f"Challenge completed. {correct_count}/{self.num_challenges} correct. Failed to meet requirement."
                    return msg
                
                remain = self.num_challenges - len(self.challenge_answers)
                if lang == "zh":
                    return f"判定已记录。剩余 {remain} 个配对待判定。"
                else:
                    return f"Judgment recorded. {remain} pairs remaining."
                
            except:
                return f"{error_prefix}{'判定格式错误' if lang == 'zh' else 'Invalid judgment format'}"

        if self.in_challenge:
            return f"{error_prefix}{'挑战阶段不允许查询' if lang == 'zh' else 'Queries not allowed in challenge phase'}"
        
        if self.query_count >= self.max_queries:
            return f"{error_prefix}{'查询次数已用尽' if lang == 'zh' else 'Query limit reached'}"

        if "query_equiv" in parsed_info:
            try:
                oid1, oid2 = [x.strip() for x in parsed_info["query_equiv"].split(",")]
                if not self._validate_object_id(oid1) or not self._validate_object_id(oid2):
                    raise ValueError
                
                self.query_count += 1
                pair = tuple(sorted([oid1, oid2]))
                self.queried_pairs.add(pair)
                
                result = yes_word if self._same_group(oid1, oid2) else no_word
                remain = self.max_queries - self.query_count
                return f"{result}（{'剩余查询次数' if lang == 'zh' else 'Remaining queries'}: {remain}）"
            except:
                return f"{error_prefix}{'等价查询格式错误' if lang == 'zh' else 'Invalid equivalence query format'}"

        if "query_count" in parsed_info:
            try:
                parts = parsed_info["query_count"].split(";")
                if len(parts) != 2:
                    raise ValueError
                target = parts[0].strip()
                subset = [x.strip() for x in parts[1].split(",")]
                
                if not self._validate_object_id(target):
                    raise ValueError
                for oid in subset:
                    if not self._validate_object_id(oid):
                        raise ValueError
                
                self.query_count += 1
                count = sum(1 for oid in subset if self._same_group(target, oid))
                remain = self.max_queries - self.query_count
                return f"{count}（{'剩余查询次数' if lang == 'zh' else 'Remaining queries'}: {remain}）"
            except:
                return f"{error_prefix}{'计数查询格式错误' if lang == 'zh' else 'Invalid count query format'}"

        if "query_example" in parsed_info:
            try:
                target = parsed_info["query_example"].strip()
                if not self._validate_object_id(target):
                    raise ValueError
                
                self.query_count += 1
                same_group = sorted([oid for oid in self.OBJECTS.keys() 
                             if oid != target and self._same_group(target, oid)])
                
                if not same_group:
                    result = none_word
                else:
                    result = same_group[0]
                
                remain = self.max_queries - self.query_count
                return f"{result}（{'剩余查询次数' if lang == 'zh' else 'Remaining queries'}: {remain}）"
            except:
                return f"{error_prefix}{'示例查询格式错误' if lang == 'zh' else 'Invalid example query format'}"

        return f"{error_prefix}{'未识别的查询类型' if lang == 'zh' else 'Unrecognized query type'}"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        lang = self.config.language
        
        yes_word = "是" if lang == "zh" else "Yes"
        no_word = "否" if lang == "zh" else "No"
        none_word = "无" if lang == "zh" else "None"
        remain_text = "剩余查询次数" if lang == "zh" else "Remaining queries"
        
        objects = sorted(list(self.OBJECTS.keys()))
        
        query_counter = 0
        
        for i in range(len(objects)):
            for j in range(i + 1, len(objects)):
                oid1 = objects[i]
                oid2 = objects[j]
                
                query_content = f"<query_equiv>{oid1},{oid2}</query_equiv>"
                
                is_same = self._same_group(oid1, oid2)
                result = yes_word if is_same else no_word
                query_counter += 1
                remain = self.max_queries - query_counter
                answer = f"{result}（{remain_text}: {remain}）"
                
                queries.append({
                    "query": query_content,
                    "answer": answer
                })
        
        for oid in objects:
            query_content = f"<query_example>{oid}</query_example>"
            
            same_group = sorted([target for target in objects if target != oid and self._same_group(oid, target)])
            
            if not same_group:
                result = none_word
            else:
                result = same_group[0]
                
            query_counter += 1
            remain = self.max_queries - query_counter
            answer = f"{result}（{remain_text}: {remain}）"
            
            queries.append({
                "query": query_content,
                "answer": answer
            })
            
        for oid in objects:
            others = [o for o in objects if o != oid]
            others_str = ",".join(others)
            query_content = f"<query_count>{oid};{others_str}</query_count>"
            
            count = sum(1 for target in others if self._same_group(oid, target))
            query_counter += 1
            remain = self.max_queries - query_counter
            answer = f"{count}（{remain_text}: {remain}）"
            
            queries.append({
                "query": query_content,
                "answer": answer
            })
            
        return queries

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if "是" in correct:
            return correct.replace("是", "否")
        if "否" in correct:
            return correct.replace("否", "是")
            
        if "Yes" in correct:
            return correct.replace("Yes", "No")
        if "No" in correct:
            return correct.replace("No", "Yes")
            
        return correct + "_WRONG"