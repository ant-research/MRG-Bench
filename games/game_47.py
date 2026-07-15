from .base import Game
import re

class HiddenSubsetRuleGame(Game):

    game_rule_zh = """\
我们现在来玩一个"隐藏子集推理"游戏，规则如下：

游戏设定了一个包含12个元素的有限集合，编号为 1 到 12。每个元素都附带若干标签，标签来自集合 {{A,B,C,D,E,F,G,H}}。

元素与标签的对应关系如下（公开信息）：
- 1: A,B,E,G
- 2: A,C,D,F
- 3: B,C,E,H
- 4: A,D,E,F,H
- 5: B,D,F,G
- 6: C,E,F,G
- 7: A,B,C,H
- 8: B,E,F,H
- 9: A,C,E,G
- 10: D,E,G,H
- 11: A,F,H
- 12: B,C,D,G

我已秘密选定了两个隐藏的标签子集 S正 和 S负，它们互不相交。目标集合 T 由那些"包含 S正 中所有标签且不含 S负 中任何标签"的元素构成。你的任务是通过提问推断出 S正 和 S负。

你可以使用以下三种提问方式：

1. 筛选-计数查询：给定两个标签子集 I正 和 I负，我会告诉你两个数字：
   - 总数：有多少个元素同时包含 I正 中所有标签且不含 I负 中任何标签
   - 目标数：上述元素中有多少个属于目标集合 T

2. 个体归属查询：询问指定编号的元素是否属于目标集合 T，我会回答"是"或"否"。

3. 终局声明：当你认为已经找到答案时，提交你推断的 S正 和 S负。我会判断是否正确。

每次提问只能包含一个标签。请使用以下 XML 格式：

- 筛选-计数查询（例如 I正={{A,B}}，I负={{C}}）：
<query_filter>include=A,B;exclude=C</query_filter>

如果 I正 或 I负 为空，可以省略或留空：
<query_filter>include=A,B;exclude=</query_filter>
<query_filter>include=;exclude=C</query_filter>
<query_filter>include=A;exclude=</query_filter>

- 个体归属查询（例如询问编号 5）：
<query_member>5</query_member>

- 终局声明（例如 S正={{A,E}}，S负={{C}}）：
<answer>S+=A,E;S-=C</answer>

如果 S正 或 S负 为空：
<answer>S+=A;S-=</answer>
<answer>S+=;S-=C</answer>

注意：请尽可能用最少的提问次数找到答案。
"""

    game_rule_en = """\
Let's play a "Hidden Subset Deduction" game. Here are the rules:

The game has a finite set of 12 elements, numbered 1 to 12. Each element has several tags from the set {{A,B,C,D,E,F,G,H}}.

The element-tag mapping is as follows (public information):
- 1: A,B,E,G
- 2: A,C,D,F
- 3: B,C,E,H
- 4: A,D,E,F,H
- 5: B,D,F,G
- 6: C,E,F,G
- 7: A,B,C,H
- 8: B,E,F,H
- 9: A,C,E,G
- 10: D,E,G,H
- 11: A,F,H
- 12: B,C,D,G

I have secretly selected two disjoint tag subsets S_pos and S_neg. The target set T consists of elements that "contain all tags in S_pos and contain none of the tags in S_neg". Your task is to deduce S_pos and S_neg through queries.

You can use the following three types of queries:

1. Filter-Count Query: Given two tag subsets I_pos and I_neg, I will tell you two numbers:
   - Total count: how many elements contain all tags in I_pos and contain none in I_neg
   - Target count: among the above elements, how many belong to the target set T

2. Membership Query: Ask if a specific element belongs to the target set T. I will answer "Yes" or "No".

3. Final Declaration: When you think you have found the answer, submit your deduced S_pos and S_neg. I will judge if it is correct.

Each query must contain only one tag. Use the following XML format:

- Filter-Count Query (e.g., I_pos={{A,B}}, I_neg={{C}}):
<query_filter>include=A,B;exclude=C</query_filter>

If I_pos or I_neg is empty, you can omit or leave it blank:
<query_filter>include=A,B;exclude=</query_filter>
<query_filter>include=;exclude=C</query_filter>
<query_filter>include=A;exclude=</query_filter>

- Membership Query (e.g., asking about element 5):
<query_member>5</query_member>

- Final Declaration (e.g., S_pos={{A,E}}, S_neg={{C}}):
<answer>S+=A,E;S-=C</answer>

If S_pos or S_neg is empty:
<answer>S+=A;S-=</answer>
<answer>S+=;S-=C</answer>

Note: Try to find the answer with as few queries as possible.
"""

    contextualized_rule_zh_1 = """\
欢迎使用城市交通路网智能分析系统。我们需要排查出符合特定通行逻辑的目标路线。

系统当前监控了 12 条核心交通路线，编号为 1 到 12。每条路线都具备特定的路况与规划特征，特征代码均来自集合 {{A,B,C,D,E,F,G,H}}。

各路线与特征代码的公开对应关系如下：
- 1: A,B,E,G
- 2: A,C,D,F
- 3: B,C,E,H
- 4: A,D,E,F,H
- 5: B,D,F,G
- 6: C,E,F,G
- 7: A,B,C,H
- 8: B,E,F,H
- 9: A,C,E,G
- 10: D,E,G,H
- 11: A,F,H
- 12: B,C,D,G

系统后台秘密设定了导致高危拥堵的“必有特征组合”(S正) 和能够缓解拥堵的“豁免特征组合”(S负)，两者互不相交。目标拥堵路线集 T 由那些“完全包含 S正 特征，且不含任何 S负 特征”的路线构成。你的任务是通过交互提问，推断出 S正 和 S负。

你可以使用以下三种提问方式：

1. 筛选-计数查询：指定关注的特征 I正 和需排除的特征 I负，系统将返回：
   - 总数：符合上述特征筛选的路线总数
   - 目标数：上述路线中属于高危拥堵路线集 T 的数量

2. 个体归属查询：询问指定编号的路线是否属于目标拥堵路线集 T，系统回答“是”或“否”。

3. 终局声明：提交你推断的 S正 和 S负，系统将校验是否准确。

每次提问只能包含一个特征代码。请使用以下 XML 格式：

- 筛选-计数查询（例如 I正={{A,B}}，I负={{C}}）：
<query_filter>include=A,B;exclude=C</query_filter>

- 个体归属查询（例如询问路线 5）：
<query_member>5</query_member>

- 终局声明（例如 S正={{A,E}}，S负={{C}}）：
<answer>S+=A,E;S-=C</answer>

(空值留白格式与通用规则一致，尽量减少提问次数以节约系统算力。)
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Urban Traffic Network Intelligent Analysis System. We need to identify target routes that match specific transit logic.

The system currently monitors 12 core traffic routes, numbered 1 to 12. Each route possesses specific traffic and planning features, with feature codes from the set {{A,B,C,D,E,F,G,H}}.

The public mapping between routes and feature codes is as follows:
- 1: A,B,E,G
- 2: A,C,D,F
- 3: B,C,E,H
- 4: A,D,E,F,H
- 5: B,D,F,G
- 6: C,E,F,G
- 7: A,B,C,H
- 8: B,E,F,H
- 9: A,C,E,G
- 10: D,E,G,H
- 11: A,F,H
- 12: B,C,D,G

The system has secretly designated a "necessary feature combination" (S_pos) that causes high-risk congestion, and an "exemption feature combination" (S_neg) that alleviates it. The two sets are disjoint. The target congested route set T consists of routes that "contain all features in S_pos and none in S_neg". Your task is to deduce S_pos and S_neg via queries.

You can use three query types:

1. Filter-Count Query: Specify included features I_pos and excluded features I_neg. The system returns:
   - Total count: How many routes match this filter
   - Target count: Among those, how many belong to the target set T

2. Membership Query: Ask if a specific route belongs to the target set T. The system will answer "Yes" or "No".

3. Final Declaration: Submit your deduced S_pos and S_neg for validation.

Each query must contain only one feature code. Use the following XML format:

- Filter-Count Query (e.g., I_pos={{A,B}}, I_neg={{C}}):
<query_filter>include=A,B;exclude=C</query_filter>

- Membership Query (e.g., asking about route 5):
<query_member>5</query_member>

- Final Declaration (e.g., S_pos={{A,E}}, S_neg={{C}}):
<answer>S+=A,E;S-=C</answer>

(Omission rules for empty sets are identical to the base rules. Please optimize your queries.)
"""

    contextualized_rule_zh_2 = """\
欢迎使用疑难重症靶点筛查系统。您需要通过基因测序数据锁定某种罕见病的致病靶点规则。

样本库中存有 12 份临床疑难病历，编号 1 到 12。每份病历的测序结果表现出特定的基因靶标，靶标代码取自集合 {{A,B,C,D,E,F,G,H}}。

病历与检出靶标的公开数据如下：
- 1: A,B,E,G
- 2: A,C,D,F
- 3: B,C,E,H
- 4: A,D,E,F,H
- 5: B,D,F,G
- 6: C,E,F,G
- 7: A,B,C,H
- 8: B,E,F,H
- 9: A,C,E,G
- 10: D,E,G,H
- 11: A,F,H
- 12: B,C,D,G

医学数据库中记录了该病症的“确诊必具阳性靶标”(S正) 和“排除该病的阴性靶标”(S负)，二者互不重叠。确诊患有该罕见病的病例集合 T 由“包含所有 S正 靶标，且不含任何 S负 靶标”的病历组成。请通过检索推断出 S正 和 S负。

您可执行三种检索操作：

1. 筛选-计数查询：输入需包含的靶标 I正 与需排除的靶标 I负，系统返回：
   - 总数：符合该基因表达特征的病历总数
   - 目标数：其中属于确诊集合 T 的病历数

2. 个体归属查询：查询指定编号病历是否确诊属于集合 T，系统回答“是”或“否”。

3. 终局声明：提交您锁定的阳性与阴性靶标集合 S正 和 S负。

每次提问只能包含一个靶标代码。请使用以下 XML 格式：

- 筛选-计数查询（例如 I正={{A,B}}，I负={{C}}）：
<query_filter>include=A,B;exclude=C</query_filter>

- 个体归属查询（例如询问病历 5）：
<query_member>5</query_member>

- 终局声明（例如 S正={{A,E}}，S负={{C}}）：
<answer>S+=A,E;S-=C</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Critical Illness Target Screening System. You need to identify the pathogenic target rules for a rare disease using genomic sequencing data.

The database contains 12 clinical case files, numbered 1 to 12. Each case exhibits specific genetic targets from the set {{A,B,C,D,E,F,G,H}}.

The public data for cases and detected targets is as follows:
- 1: A,B,E,G
- 2: A,C,D,F
- 3: B,C,E,H
- 4: A,D,E,F,H
- 5: B,D,F,G
- 6: C,E,F,G
- 7: A,B,C,H
- 8: B,E,F,H
- 9: A,C,E,G
- 10: D,E,G,H
- 11: A,F,H
- 12: B,C,D,G

The medical database records the "mandatory positive targets" (S_pos) and "excluding negative targets" (S_neg) for this disease; the two sets are disjoint. The confirmed patient set T consists of cases that "contain all S_pos targets and none of the S_neg targets". Deduce S_pos and S_neg via retrieval queries.

You can perform three types of operations:

1. Filter-Count Query: Input included targets I_pos and excluded targets I_neg. System returns:
   - Total count: Total cases matching this genetic profile
   - Target count: Cases among them that belong to the confirmed set T

2. Membership Query: Ask if a specific case is confirmed in set T. System answers "Yes" or "No".

3. Final Declaration: Submit your identified S_pos and S_neg.

Each query must contain only one target. Use the following XML format:

- Filter-Count Query:
<query_filter>include=A,B;exclude=C</query_filter>

- Membership Query (e.g., case 5):
<query_member>5</query_member>

- Final Declaration:
<answer>S+=A,E;S-=C</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎进入教务编排与课程评估系统。我们需要为下一代拔尖人才计划筛选出符合特定知识架构的目标课程模块。

教务处预备了 12 个核心教学模块，编号 1 到 12。每个模块都侧重于特定能力维度的培养，维度标签取自集合 {{A,B,C,D,E,F,G,H}}。

各教学模块的能力维度分布情况公开如下：
- 1: A,B,E,G
- 2: A,C,D,F
- 3: B,C,E,H
- 4: A,D,E,F,H
- 5: B,D,F,G
- 6: C,E,F,G
- 7: A,B,C,H
- 8: B,E,F,H
- 9: A,C,E,G
- 10: D,E,G,H
- 11: A,F,H
- 12: B,C,D,G

委员会为拔尖项目隐秘设定了“必修维度指标”(S正) 与“不纳入考查的维度指标”(S负)，二者不重叠。最终入选该拔尖项目的模块集合 T 必须“全面覆盖 S正 中的维度，且绝对不涉及 S负 中的维度”。您需要通过系统质询，反推 S正 和 S负。

可选的三种质询方式如下：

1. 筛选-计数查询：设定必须包含的维度 I正 和需剔除的维度 I负，教务系统将反馈：
   - 总数：符合该条件限制的模块总数
   - 目标数：其中成功入选拔尖项目集合 T 的模块数

2. 个体归属查询：验证特定编号的教学模块是否入选了集合 T，系统回答“是”或“否”。

3. 终局声明：提交您反推的 S正 与 S负，系统将评定准确性。

每次提问只能包含一个能力维度标签。请使用以下 XML 格式：

- 筛选-计数查询（例如 I正={{A,B}}，I负={{C}}）：
<query_filter>include=A,B;exclude=C</query_filter>

- 个体归属查询（例如询问模块 5）：
<query_member>5</query_member>

- 终局声明（例如 S正={{A,E}}，S负={{C}}）：
<answer>S+=A,E;S-=C</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Academic Scheduling and Course Evaluation System. We need to filter target course modules that fit a specific knowledge framework for the next-generation talent program.

The Academic Affairs Office has prepared 12 core teaching modules, numbered 1 to 12. Each module focuses on specific competency dimensions from the set {{A,B,C,D,E,F,G,H}}.

The public distribution of competency dimensions for each module is:
- 1: A,B,E,G
- 2: A,C,D,F
- 3: B,C,E,H
- 4: A,D,E,F,H
- 5: B,D,F,G
- 6: C,E,F,G
- 7: A,B,C,H
- 8: B,E,F,H
- 9: A,C,E,G
- 10: D,E,G,H
- 11: A,F,H
- 12: B,C,D,G

The committee has secretly established "mandatory required dimensions" (S_pos) and "excluded assessment dimensions" (S_neg), which do not overlap. The final selected module set T for the program must "cover all dimensions in S_pos and avoid any in S_neg". Reverse-engineer S_pos and S_neg via inquiries.

You have three inquiry methods:

1. Filter-Count Query: Set included dimensions I_pos and excluded dimensions I_neg. The system responds with:
   - Total count: Total modules matching this constraint
   - Target count: Among them, the number of modules successfully selected into set T

2. Membership Query: Verify if a specific module ID is selected into set T. System answers "Yes" or "No".

3. Final Declaration: Submit your deduced S_pos and S_neg for validation.

Each query must contain only one competency dimension. Use the following XML format:

- Filter-Count Query:
<query_filter>include=A,B;exclude=C</query_filter>

- Membership Query (e.g., module 5):
<query_member>5</query_member>

- Final Declaration:
<answer>S+=A,E;S-=C</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎进入工业制造良率溯源系统。近日产线出现一批极高标准的特级良品，我们需要找出导致这一结果的核心工艺组合。

当前系统记录了 12 批次核心晶圆物料，编号从 1 到 12。每个批次都经过了特定的工艺参数处理，参数代码集合为 {{A,B,C,D,E,F,G,H}}。

批次与所受工艺参数的对应关系（已公开）：
- 1: A,B,E,G
- 2: A,C,D,F
- 3: B,C,E,H
- 4: A,D,E,F,H
- 5: B,D,F,G
- 6: C,E,F,G
- 7: A,B,C,H
- 8: B,E,F,H
- 9: A,C,E,G
- 10: D,E,G,H
- 11: A,F,H
- 12: B,C,D,G

品控部门锁定了达成特级良率的“核心赋能工艺”(S正) 以及导致良率劣化的“冲突工艺”(S负)，二者无交集。产出特级良品的物料集合 T 严格遵循“叠加了全部 S正 工艺，且未暴露于任何 S负 工艺”的条件。你的任务是推演排查出 S正 与 S负。

支持以下三种数据探查指令：

1. 筛选-计数查询：选定叠加的工艺 I正 和排查的工艺 I负，系统将告知：
   - 总数：经过对应筛选条件处理的物料批次总数
   - 目标数：其中达到了特级良品标准（属于集合 T）的批次数量

2. 个体归属查询：针对单一物料批次，查询其是否属于良品集合 T，系统反馈“是”或“否”。

3. 终局声明：上传你锁定的核心赋能与冲突工艺参数 S正 和 S负。

每次探查只能包含一个工艺代码。请使用以下 XML 格式：

- 筛选-计数查询（例如 I正={{A,B}}，I负={{C}}）：
<query_filter>include=A,B;exclude=C</query_filter>

- 个体归属查询（例如询问批次 5）：
<query_member>5</query_member>

- 终局声明（例如 S正={{A,E}}，S负={{C}}）：
<answer>S+=A,E;S-=C</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Industrial Manufacturing Yield Traceability System. We need to identify the core process combination that results in premium-grade products.

The system currently logs 12 batches of core wafer materials, numbered 1 to 12. Each batch underwent specific processing parameters, coded from the set {{A,B,C,D,E,F,G,H}}.

The public mapping between batches and applied processes is:
- 1: A,B,E,G
- 2: A,C,D,F
- 3: B,C,E,H
- 4: A,D,E,F,H
- 5: B,D,F,G
- 6: C,E,F,G
- 7: A,B,C,H
- 8: B,E,F,H
- 9: A,C,E,G
- 10: D,E,G,H
- 11: A,F,H
- 12: B,C,D,G

Quality Control has pinpointed "core enabling processes" (S_pos) that achieve premium yield and "conflicting processes" (S_neg) that degrade it. The two sets are disjoint. The premium-grade material set T strictly includes batches that "underwent all S_pos processes and were never exposed to any S_neg processes". Your task is to trace and deduce S_pos and S_neg.

Three data probing commands are supported:

1. Filter-Count Query: Select applied processes I_pos and excluded processes I_neg. The system replies with:
   - Total count: Number of batches meeting this filtering criteria
   - Target count: Number of batches among them that achieved premium grade (belong to set T)

2. Membership Query: Ask if a specific batch ID belongs to the premium set T. System responds "Yes" or "No".

3. Final Declaration: Upload your deduced core enabling and conflicting processes S_pos and S_neg.

Each probe must contain only one process code. Use the following XML format:

- Filter-Count Query:
<query_filter>include=A,B;exclude=C</query_filter>

- Membership Query (e.g., batch 5):
<query_member>5</query_member>

- Final Declaration:
<answer>S+=A,E;S-=C</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎进入智能司法类案检索系统。您的任务是基于历史卷宗，归纳出法院在特定争议中适用特殊保全措施的法定要件组合。

系统收录了 12 宗重点商业纠纷判例，编号为 1 到 12。每宗判例均具备若干核心证据要素，要素代码选自集合 {{A,B,C,D,E,F,G,H}}。

判例编号与提取证据要素的公开映射如下：
- 1: A,B,E,G
- 2: A,C,D,F
- 3: B,C,E,H
- 4: A,D,E,F,H
- 5: B,D,F,G
- 6: C,E,F,G
- 7: A,B,C,H
- 8: B,E,F,H
- 9: A,C,E,G
- 10: D,E,G,H
- 11: A,F,H
- 12: B,C,D,G

根据内部司法裁判尺度，法院裁定保全措施时遵循一套隐性准则：必须具备“支持财产保全的法定要件”(S正)，且不能触发“阻却事由要件”(S负)，两要件集合互不交叉。最终准予保全的判例集合 T 必然“囊括 S正 的全部要素，并排除一切 S负 要素”。请通过法理检索查明 S正 与 S负。

您可以通过以下方式进行类案检索：

1. 筛选-计数查询：限定检索包含要素 I正 及排除要素 I负，卷宗系统将显示：
   - 总数：案情符合上述证据要素结构的判例总数
   - 目标数：其中法院裁定准予特殊保全（归属集合 T）的判例数

2. 个体归属查询：核实某指定卷宗编号是否属于准予保全的判例集 T，系统回答“是”或“否”。

3. 终局声明：提交您归纳的法定要件 S正 及阻却事由 S负 进行权威检验。

每次检索仅限附带一个证据要素代码。请使用以下 XML 格式：

- 筛选-计数查询（例如 I正={{A,B}}，I负={{C}}）：
<query_filter>include=A,B;exclude=C</query_filter>

- 个体归属查询（例如询问卷宗 5）：
<query_member>5</query_member>

- 终局声明（例如 S正={{A,E}}，S负={{C}}）：
<answer>S+=A,E;S-=C</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Intelligent Judicial Case Retrieval System. Your task is to deduce the combination of statutory elements required for the court to apply special preservation measures in specific disputes based on historical files.

The system incorporates 12 key commercial dispute precedents, numbered 1 to 12. Each precedent contains several core evidentiary elements coded from the set {{A,B,C,D,E,F,G,H}}.

The public mapping between case precedents and their evidentiary elements is:
- 1: A,B,E,G
- 2: A,C,D,F
- 3: B,C,E,H
- 4: A,D,E,F,H
- 5: B,D,F,G
- 6: C,E,F,G
- 7: A,B,C,H
- 8: B,E,F,H
- 9: A,C,E,G
- 10: D,E,G,H
- 11: A,F,H
- 12: B,C,D,G

According to internal judicial standards, the court follows a hidden principle when ruling on preservation measures: it must include the "statutory elements supporting preservation" (S_pos) and must not trigger any "blocking factors" (S_neg). The two sets do not intersect. The set of precedents granted preservation T naturally "encompasses all elements in S_pos and excludes all elements in S_neg". Conduct legal retrieval to ascertain S_pos and S_neg.

You may conduct case retrieval via the following methods:

1. Filter-Count Query: Restrict the search to include elements I_pos and exclude elements I_neg. The case file system displays:
   - Total count: Total precedents matching this evidentiary structure
   - Target count: Number of precedents among them where the court granted special preservation (belong to set T)

2. Membership Query: Verify whether a specific case file ID belongs to the granted preservation set T. System answers "Yes" or "No".

3. Final Declaration: Submit your deduced statutory elements S_pos and blocking factors S_neg for authoritative validation.

Each query is strictly limited to one evidentiary element code. Use the following XML format:

- Filter-Count Query:
<query_filter>include=A,B;exclude=C</query_filter>

- Membership Query (e.g., case 5):
<query_member>5</query_member>

- Final Declaration:
<answer>S+=A,E;S-=C</answer>
"""

    tags = ["answer", "query_filter", "query_member"]
    reasoning_type = "归纳推理"
    data_structure = "集合"

    ELEMENT_TAGS = {
        1: {"A", "B", "E", "G"},
        2: {"A", "C", "D", "F"},
        3: {"B", "C", "E", "H"},
        4: {"A", "D", "E", "F", "H"},
        5: {"B", "D", "F", "G"},
        6: {"C", "E", "F", "G"},
        7: {"A", "B", "C", "H"},
        8: {"B", "E", "F", "H"},
        9: {"A", "C", "E", "G"},
        10: {"D", "E", "G", "H"},
        11: {"A", "F", "H"},
        12: {"B", "C", "D", "G"},
    }

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "S+": {"A"},
                "S-": set(),
            },
            2: {
                "S+": {"B", "E"},
                "S-": set(),
            },
            3: {
                "S+": {"E", "G"},
                "S-": {"C"},
            },
            4: {
                "S+": {"E", "F"},
                "S-": {"D"},
            },
            5: {
                "S+": {"E", "G"},
                "S-": {"A", "D"},
            },
        },
        "en": {
            1: {
                "S+": {"A"},
                "S-": set(),
            },
            2: {
                "S+": {"B", "E"},
                "S-": set(),
            },
            3: {
                "S+": {"E", "G"},
                "S-": {"C"},
            },
            4: {
                "S+": {"E", "F"},
                "S-": {"D"},
            },
            5: {
                "S+": {"E", "G"},
                "S-": {"A", "D"},
            },
        },
    }

    def __init__(self, config):
        self.query_filter_count = 0
        self.query_member_count = 0
        self.answer_count = 0
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.S_pos = cfg["S+"]
        self.S_neg = cfg["S-"]
        
        self.target_set = set()
        for elem_id, tags in self.ELEMENT_TAGS.items():
            if self.S_pos.issubset(tags) and tags.isdisjoint(self.S_neg):
                self.target_set.add(elem_id)
        
        self._game_info["n"] = 12

    def _check_element_match(self, elem_id, include_tags, exclude_tags):
        tags = self.ELEMENT_TAGS[elem_id]
        return include_tags.issubset(tags) and tags.isdisjoint(exclude_tags)

    def evaluate(self, parsed_info):
        if self.answer_count >= 2:
            return False

        self.answer_count += 1

        raw_ans = parsed_info["answer"]
        
        try:
            parts = raw_ans.split(";")
            s_plus_str = ""
            s_minus_str = ""
            
            for part in parts:
                part = part.strip()
                if part.startswith("S+"):
                    s_plus_str = part.split("=", 1)[1].strip()
                elif part.startswith("S-"):
                    s_minus_str = part.split("=", 1)[1].strip()
            
            if s_plus_str:
                model_s_plus = set(tag.strip() for tag in s_plus_str.split(",") if tag.strip())
            else:
                model_s_plus = set()
                
            if s_minus_str:
                model_s_minus = set(tag.strip() for tag in s_minus_str.split(",") if tag.strip())
            else:
                model_s_minus = set()
            
            for elem_id, tags in self.ELEMENT_TAGS.items():
                real_in_target = elem_id in self.target_set
                
                model_in_target = (model_s_plus.issubset(tags) and 
                                 tags.isdisjoint(model_s_minus))
                
                if real_in_target != model_in_target:
                    return False
            
            return True
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            quota_exceed_filter = "错误：筛选-计数查询次数已用尽。请使用其他查询方式。"
            quota_exceed_member = "错误：个体归属查询次数已用尽。请使用其他查询方式。"
            invalid_format = "错误：格式无效。"
            invalid_elem   = "错误：元素编号超出范围（应为1-12）。"
        else:
            yes_res, no_res = "Yes", "No"
            quota_exceed_filter = "Error: Filter-count query quota exceeded. Please use another query type."
            quota_exceed_member = "Error: Membership query quota exceeded. Please use another query type."
            invalid_format = "Error: Invalid format."
            invalid_elem   = "Error: Element ID out of range (should be 1-12)."

        if "query_filter" in parsed_info:
            if self.query_filter_count >= 12:
                return quota_exceed_filter

            self.query_filter_count += 1

            try:
                raw = parsed_info["query_filter"]
                include_tags = set()
                exclude_tags = set()

                parts = raw.split(";")
                for part in parts:
                    part = part.strip()
                    if part.startswith("include="):
                        tags_str = part.split("=", 1)[1].strip()
                        if tags_str:
                            include_tags = set(tag.strip() for tag in tags_str.split(",") if tag.strip())
                    elif part.startswith("exclude="):
                        tags_str = part.split("=", 1)[1].strip()
                        if tags_str:
                            exclude_tags = set(tag.strip() for tag in tags_str.split(",") if tag.strip())

                total_count = 0
                target_count = 0

                for elem_id in range(1, 13):
                    if self._check_element_match(elem_id, include_tags, exclude_tags):
                        total_count += 1
                        if elem_id in self.target_set:
                            target_count += 1

                if self.config.language == "zh":
                    return f"总数：{total_count}，目标数：{target_count}"
                else:
                    return f"Total count: {total_count}, Target count: {target_count}"

            except Exception:
                return invalid_format

        elif "query_member" in parsed_info:
            if self.query_member_count >= 3:
                return quota_exceed_member

            self.query_member_count += 1

            try:
                elem_id = int(parsed_info["query_member"].strip())
                if elem_id < 1 or elem_id > 12:
                    return invalid_elem

                return yes_res if elem_id in self.target_set else no_res

            except Exception:
                return invalid_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        lang = self.config.language

        if correct in ("是", "否"):
            return "否" if correct == "是" else "是"
        if correct in ("Yes", "No"):
            return "No" if correct == "Yes" else "Yes"

        if lang == "zh":
            m = re.search(r'目标数：(\d+)', correct)
            if m:
                wrong_val = int(m.group(1)) + 1
                return re.sub(r'目标数：\d+', f'目标数：{wrong_val}', correct)
        else:
            m = re.search(r'Target count: (\d+)', correct)
            if m:
                wrong_val = int(m.group(1)) + 1
                return re.sub(r'Target count: \d+', f'Target count: {wrong_val}', correct)

        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        for elem_id in range(1, 13):
            query_str = f"<query_member>{elem_id}</query_member>"
            
            is_in_target = elem_id in self.target_set
            if self.config.language == "zh":
                ans = "是" if is_in_target else "否"
            else:
                ans = "Yes" if is_in_target else "No"
                
            queries.append({"query": query_str, "answer": ans})

        all_tags = ["A", "B", "C", "D", "E", "F", "G", "H"]
        
        for tag in all_tags:
            q_inc = f"<query_filter>include={tag};exclude=</query_filter>"
            
            total_count = 0
            target_count = 0
            tag_set = {tag}
            
            for elem_id in range(1, 13):
                elem_tags = self.ELEMENT_TAGS[elem_id]
                if tag_set.issubset(elem_tags):
                    total_count += 1
                    if elem_id in self.target_set:
                        target_count += 1
            
            if self.config.language == "zh":
                ans_inc = f"总数：{total_count}，目标数：{target_count}"
            else:
                ans_inc = f"Total count: {total_count}, Target count: {target_count}"
                
            queries.append({"query": q_inc, "answer": ans_inc})
            
            q_exc = f"<query_filter>include=;exclude={tag}</query_filter>"
            
            total_count = 0
            target_count = 0
            
            for elem_id in range(1, 13):
                elem_tags = self.ELEMENT_TAGS[elem_id]
                if elem_tags.isdisjoint(tag_set):
                    total_count += 1
                    if elem_id in self.target_set:
                        target_count += 1

            if self.config.language == "zh":
                ans_exc = f"总数：{total_count}，目标数：{target_count}"
            else:
                ans_exc = f"Total count: {total_count}, Target count: {target_count}"
                
            queries.append({"query": q_exc, "answer": ans_exc})
            
        return queries