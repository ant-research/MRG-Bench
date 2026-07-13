from .base import Game
import re
import itertools


class SetCoverMinimizationGame(Game):

    game_rule_zh = """\
我们来玩一个"最小集合覆盖"推理游戏，规则如下：

游戏设定了一个基础元素集合 E = {{e1, e2, e3, e4, e5, e6, e7, e8}}，以及一个子集族 S = {{S1, S2, S3, S4, S5, S6, S7}}，其中每个 Si 都是 E 的子集。这些子集的具体成员构成是隐藏的，你需要通过查询来推断。

游戏约束：
1. 每个元素至少被一个子集包含，且至多被三个子集包含
2. 每个子集 Si 的大小在 2 到 5 个元素之间
3. 存在一个由子集索引组成的集合，能够覆盖所有元素 E
4. 最小覆盖规模 K 满足：2 小于等于 K 小于等于 4

你的目标：
找出最小覆盖规模 K，并给出一个大小为 K 的索引集合 H，使得这些子集的并集恰好等于 E。

你可以使用以下三种查询方式（每次查询计入总次数）：

1. **成员关系查询**：询问某个子集 Si 是否包含元素 ej
   - 格式：<query_member>Si,ej</query_member>
   - 示例：<query_member>S1,e3</query_member>
   - 返回：是 或 否

2. **覆盖检验查询**：给定一组子集索引，查询哪些元素未被覆盖
   - 格式：<query_coverage>S1,S2,S3</query_coverage>
   - 示例：<query_coverage>S1,S3</query_coverage>
   - 返回：未覆盖元素列表（按升序），若全部覆盖则返回"无"

3. **不可或缺性查询**：询问某个子集 Si 是否不可或缺（即是否存在仅由它覆盖的元素）
   - 格式：<query_essential>Si</query_essential>
   - 示例：<query_essential>S5</query_essential>
   - 返回：若不可或缺，返回"是：{...}"（括号内列出至少一个仅由该子集覆盖的元素）；否则返回"否"

提交最终答案时，需要说明最小覆盖规模 K 和具体的子集索引集合 H（用逗号分隔），格式如下：

<answer>K=3, H=S1,S4,S6</answer>

注意：
- 请尽可能少地使用查询次数
- 查询格式必须严格遵守上述 XML 格式
- 答案必须是真正的最小覆盖（不存在更小的覆盖方案）
"""

    game_rule_en = """\
Let's play a "Minimum Set Cover" deduction game. Here are the rules:

The game has a base element set E = {{e1, e2, e3, e4, e5, e6, e7, e8}}, and a family of subsets S = {{S1, S2, S3, S4, S5, S6, S7}}, where each Si is a subset of E. The specific membership of these subsets is hidden, and you need to infer through queries.

Game constraints:
1. Each element is covered by at least one subset and at most three subsets
2. Each subset Si has a size between 2 and 5 elements
3. There exists a set of subset indices that can cover all elements in E
4. The minimum coverage size K satisfies: 2 less than or equal to K less than or equal to 4

Your goal:
Find the minimum coverage size K and provide an index set H of size K, such that the union of these subsets equals E.

You can use the following three types of queries (each query counts toward the total):

1. **Membership Query**: Ask if a subset Si contains element ej
   - Format: <query_member>Si,ej</query_member>
   - Example: <query_member>S1,e3</query_member>
   - Returns: Yes or No

2. **Coverage Check Query**: Given a set of subset indices, query which elements are not covered
   - Format: <query_coverage>S1,S2,S3</query_coverage>
   - Example: <query_coverage>S1,S3</query_coverage>
   - Returns: List of uncovered elements (in ascending order), or "None" if all covered

3. **Essentiality Query**: Ask if a subset Si is essential (i.e., whether there exists an element covered only by it)
   - Format: <query_essential>Si</query_essential>
   - Example: <query_essential>S5</query_essential>
   - Returns: If essential, return "Yes: {...}" (with at least one witness element); otherwise return "No"

When submitting the final answer, specify the minimum coverage size K and the specific subset index set H (comma-separated), using this format:

<answer>K=3, H=S1,S4,S6</answer>

Notes:
- Try to minimize the number of queries used
- Query format must strictly follow the XML format above
- The answer must be a true minimum cover (no smaller coverage solution exists)
"""

    contextualized_rule_zh_1 = """\
为了优化城市公共交通，我们来进行一项"公交线路最小覆盖"规划任务，规则如下：

任务设定了一个核心居民区集合 E = {{e1, e2, e3, e4, e5, e6, e7, e8}}，以及一个候选公交线路集合 S = {{S1, S2, S3, S4, S5, S6, S7}}，其中每条线路 Si 覆盖 E 中的部分居民区。这些线路的具体停靠站点是隐藏的，你需要通过查询来推断。

规划约束：
1. 每个居民区至少被一条线路包含，且至多被三条线路包含
2. 每条公交线路 Si 的覆盖范围在 2 到 5 个居民区之间
3. 存在一个由线路索引组成的集合，能够覆盖所有居民区 E
4. 最少公交线路数 K 满足：2 小于等于 K 小于等于 4（注：即 K 介于 2 到 4 之间）

你的目标：
找出最少公交线路数 K，并给出一个大小为 K 的线路索引集合 H，使得这些线路的停靠站点并集恰好涵盖所有居民区 E。

你可以使用以下三种查询方式（每次查询计入总次数）：

1. **停靠关系查询**：询问某条线路 Si 是否停靠居民区 ej
   - 格式：<query_member>Si,ej</query_member>
   - 示例：<query_member>S1,e3</query_member>
   - 返回：是 或 否

2. **覆盖检验查询**：给定一组线路索引，查询哪些居民区未被覆盖
   - 格式：<query_coverage>S1,S2,S3</query_coverage>
   - 示例：<query_coverage>S1,S3</query_coverage>
   - 返回：未覆盖居民区列表（按升序），若全部覆盖则返回"无"

3. **不可或缺性查询**：询问某条线路 Si 是否不可或缺（即是否存在仅由它覆盖的居民区）
   - 格式：<query_essential>Si</query_essential>
   - 示例：<query_essential>S5</query_essential>
   - 返回：若不可或缺，返回"是：{...}"（括号内列出至少一个仅由该线路覆盖的居民区）；否则返回"否"

提交最终答案时，需要说明最少公交线路数 K 和具体的线路索引集合 H（用逗号分隔），格式如下：

<answer>K=3, H=S1,S4,S6</answer>

注意：
- 请尽可能少地使用查询次数
- 查询格式必须严格遵守上述 XML 格式
- 答案必须是真正的最小覆盖（不存在更少线路的规划方案）
"""

    contextualized_rule_en_1 = """\
[Urban Transportation Scenario]
To optimize urban public transit, let's conduct a "Minimum Bus Route Coverage" planning task. Here are the rules:

The task involves a set of core residential areas E = {{e1, e2, e3, e4, e5, e6, e7, e8}}, and a set of candidate bus routes S = {{S1, S2, S3, S4, S5, S6, S7}}, where each route Si covers a subset of E. The specific stops of these routes are hidden, and you need to infer them through queries.

Planning constraints:
1. Each residential area is covered by at least one route and at most three routes
2. Each bus route Si covers between 2 and 5 residential areas
3. There exists a set of route indices that can cover all areas in E
4. The minimum number of routes K satisfies: 2 less than or equal to K less than or equal to 4

Your goal:
Find the minimum number of routes K and provide an index set H of size K, such that the union of their stops covers E completely.

You can use the following three types of queries (each query counts toward the total):

1. **Stop Query**: Ask if a route Si stops at residential area ej
   - Format: <query_member>Si,ej</query_member>
   - Example: <query_member>S1,e3</query_member>
   - Returns: Yes or No

2. **Coverage Check Query**: Given a set of route indices, query which areas are not covered
   - Format: <query_coverage>S1,S2,S3</query_coverage>
   - Example: <query_coverage>S1,S3</query_coverage>
   - Returns: List of uncovered areas (in ascending order), or "None" if all covered

3. **Essentiality Query**: Ask if a route Si is essential (i.e., whether there exists an area covered only by it)
   - Format: <query_essential>Si</query_essential>
   - Example: <query_essential>S5</query_essential>
   - Returns: If essential, return "Yes: {...}" (with at least one witness area); otherwise return "No"

When submitting the final answer, specify the minimum number of routes K and the specific route index set H (comma-separated), using this format:

<answer>K=3, H=S1,S4,S6</answer>

Notes:
- Try to minimize the number of queries used
- Query format must strictly follow the XML format above
- The answer must be a true minimum cover (no smaller route plan exists)
"""

    contextualized_rule_zh_2 = """\
为了制定精准的联合用药方案，我们来进行一项"最小药物覆盖"的医学推理任务，规则如下：

系统设定了一个病原体/症状集合 E = {{e1, e2, e3, e4, e5, e6, e7, e8}}，以及一个候选药物集合 S = {{S1, S2, S3, S4, S5, S6, S7}}，其中每种药物 Si 都能抑制 E 中的部分靶点。这些药物的具体抗菌谱是隐藏的，你需要通过查询来推断。

用药约束：
1. 每种病原体至少被一种药物覆盖，且至多被三种药物覆盖
2. 每种药物 Si 的有效覆盖范围在 2 到 5 种病原体之间
3. 存在一个由药物索引组成的集合，能够覆盖所有病原体 E
4. 最少联合药物数 K 满足：2 小于等于 K 小于等于 4（注：即 K 介于 2 到 4 之间）

你的目标：
找出最少联合药物数 K，并给出一个大小为 K 的药物索引集合 H，使得这些药物的抗菌谱并集恰好覆盖所有病原体 E。

你可以使用以下三种查询方式（每次查询计入总次数）：

1. **抑制效用查询**：询问某药物 Si 是否能有效抑制病原体 ej
   - 格式：<query_member>Si,ej</query_member>
   - 示例：<query_member>S1,e3</query_member>
   - 返回：是 或 否

2. **覆盖检验查询**：给定一组药物组合，查询哪些病原体仍未被抑制
   - 格式：<query_coverage>S1,S2,S3</query_coverage>
   - 示例：<query_coverage>S1,S3</query_coverage>
   - 返回：未覆盖病原体列表（按升序），若全部抑制则返回"无"

3. **不可或缺性查询**：询问某药物 Si 是否不可或缺（即是否存在仅能由它抑制的病原体）
   - 格式：<query_essential>Si</query_essential>
   - 示例：<query_essential>S5</query_essential>
   - 返回：若不可或缺，返回"是：{...}"（括号内列出至少一个仅由该药物抑制的病原体）；否则返回"否"

提交最终答案时，需要说明最少联合药物数 K 和具体的药物索引集合 H（用逗号分隔），格式如下：

<answer>K=3, H=S1,S4,S6</answer>

注意：
- 请尽可能少地使用查询次数
- 查询格式必须严格遵守上述 XML 格式
- 答案必须是真正的最小覆盖（不存在更少药物的联合方案）
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
To design a precise combination therapy, let's conduct a "Minimum Drug Coverage" deduction task. Here are the rules:

The system has a set of pathogens/symptoms E = {{e1, e2, e3, e4, e5, e6, e7, e8}}, and a set of candidate drugs S = {{S1, S2, S3, S4, S5, S6, S7}}, where each drug Si can inhibit a subset of targets in E. The specific antimicrobial spectrum of these drugs is hidden, and you need to infer it through queries.

Prescription constraints:
1. Each pathogen is covered by at least one drug and at most three drugs
2. Each drug Si covers between 2 and 5 pathogens
3. There exists a set of drug indices that can cover all pathogens in E
4. The minimum number of combined drugs K satisfies: 2 less than or equal to K less than or equal to 4

Your goal:
Find the minimum number of combined drugs K and provide an index set H of size K, such that the union of their antimicrobial spectra covers E completely.

You can use the following three types of queries (each query counts toward the total):

1. **Inhibition Query**: Ask if a drug Si can effectively inhibit pathogen ej
   - Format: <query_member>Si,ej</query_member>
   - Example: <query_member>S1,e3</query_member>
   - Returns: Yes or No

2. **Coverage Check Query**: Given a set of combined drugs, query which pathogens are still not inhibited
   - Format: <query_coverage>S1,S2,S3</query_coverage>
   - Example: <query_coverage>S1,S3</query_coverage>
   - Returns: List of uncovered pathogens (in ascending order), or "None" if all inhibited

3. **Essentiality Query**: Ask if a drug Si is essential (i.e., whether there exists a pathogen that can only be inhibited by it)
   - Format: <query_essential>Si</query_essential>
   - Example: <query_essential>S5</query_essential>
   - Returns: If essential, return "Yes: {...}" (with at least one witness pathogen); otherwise return "No"

When submitting the final answer, specify the minimum number of drugs K and the specific drug index set H (comma-separated), using this format:

<answer>K=3, H=S1,S4,S6</answer>

Notes:
- Try to minimize the number of queries used
- Query format must strictly follow the XML format above
- The answer must be a true minimum cover (no combination with fewer drugs exists)
"""

    contextualized_rule_zh_3 = """\
为了组建高效的跨学科教研团队，我们来进行一项"最少师资覆盖"的规划任务，规则如下：

本次教研涉及一个核心教学模块集合 E = {{e1, e2, e3, e4, e5, e6, e7, e8}}，以及一个候选复合型教师集合 S = {{S1, S2, S3, S4, S5, S6, S7}}，其中每位教师 Si 都能胜任 E 中的部分教学模块。这些教师的具体专业领域是隐藏的，你需要通过查询来推断。

排课约束：
1. 每个教学模块至少被一位教师覆盖，且至多被三位教师覆盖
2. 每位教师 Si 的胜任范围在 2 到 5 个教学模块之间
3. 存在一个由教师索引组成的集合，能够覆盖所有教学模块 E
4. 最少教师人数 K 满足：2 小于等于 K 小于等于 4（注：即 K 介于 2 到 4 之间）

你的目标：
找出所需的最少教师人数 K，并给出一个大小为 K 的教师索引集合 H，使得这些教师的专业领域并集恰好覆盖所有教学模块 E。

你可以使用以下三种查询方式（每次查询计入总次数）：

1. **胜任力查询**：询问某位教师 Si 是否能胜任教学模块 ej
   - 格式：<query_member>Si,ej</query_member>
   - 示例：<query_member>S1,e3</query_member>
   - 返回：是 或 否

2. **师资检验查询**：给定一组候选教师组合，查询哪些教学模块仍存在师资空白
   - 格式：<query_coverage>S1,S2,S3</query_coverage>
   - 示例：<query_coverage>S1,S3</query_coverage>
   - 返回：空白教学模块列表（按升序），若全部覆盖则返回"无"

3. **不可或缺性查询**：询问某位教师 Si 是否不可或缺（即是否存在仅能由他胜任的教学模块）
   - 格式：<query_essential>Si</query_essential>
   - 示例：<query_essential>S5</query_essential>
   - 返回：若不可或缺，返回"是：{...}"（括号内列出至少一个仅由该教师胜任的模块）；否则返回"否"

提交最终答案时，需要说明最少教师人数 K 和具体的教师索引集合 H（用逗号分隔），格式如下：

<answer>K=3, H=S1,S4,S6</answer>

注意：
- 请尽可能少地使用查询次数
- 查询格式必须严格遵守上述 XML 格式
- 答案必须是真正的最小覆盖（不存在聘用更少教师的方案）
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
To form an efficient cross-disciplinary teaching team, let's conduct a "Minimum Faculty Coverage" planning task. Here are the rules:

The curriculum involves a set of core teaching modules E = {{e1, e2, e3, e4, e5, e6, e7, e8}}, and a set of candidate versatile teachers S = {{S1, S2, S3, S4, S5, S6, S7}}, where each teacher Si can handle a subset of modules in E. Their specific areas of expertise are hidden, and you need to infer them through queries.

Scheduling constraints:
1. Each teaching module is covered by at least one teacher and at most three teachers
2. Each teacher Si is competent in between 2 and 5 teaching modules
3. There exists a set of teacher indices that can cover all teaching modules in E
4. The minimum number of teachers K satisfies: 2 less than or equal to K less than or equal to 4

Your goal:
Find the minimum number of teachers K and provide an index set H of size K, such that the union of their expertise covers E completely.

You can use the following three types of queries (each query counts toward the total):

1. **Competency Query**: Ask if a teacher Si can handle teaching module ej
   - Format: <query_member>Si,ej</query_member>
   - Example: <query_member>S1,e3</query_member>
   - Returns: Yes or No

2. **Faculty Check Query**: Given a set of teachers, query which teaching modules still lack instructors
   - Format: <query_coverage>S1,S2,S3</query_coverage>
   - Example: <query_coverage>S1,S3</query_coverage>
   - Returns: List of uncovered teaching modules (in ascending order), or "None" if all covered

3. **Essentiality Query**: Ask if a teacher Si is essential (i.e., whether there exists a module that can only be taught by them)
   - Format: <query_essential>Si</query_essential>
   - Example: <query_essential>S5</query_essential>
   - Returns: If essential, return "Yes: {...}" (with at least one witness module); otherwise return "No"

When submitting the final answer, specify the minimum number of teachers K and the specific teacher index set H (comma-separated), using this format:

<answer>K=3, H=S1,S4,S6</answer>

Notes:
- Try to minimize the number of queries used
- Query format must strictly follow the XML format above
- The answer must be a true minimum cover (no plan with fewer teachers exists)
"""

    contextualized_rule_zh_4 = """\
为了优化柔性生产线配置，我们来进行一项"最小加工刀具覆盖"的排产推演任务，规则如下：

生产任务要求完成一组复杂加工工序 E = {{e1, e2, e3, e4, e5, e6, e7, e8}}，我们有一批候选的多功能复合刀具 S = {{S1, S2, S3, S4, S5, S6, S7}}，其中每把刀具 Si 能执行 E 中的部分工序。这些刀具的具体适用范围是隐藏的，你需要通过查询来排查。

生产约束：
1. 每道工序至少可由一把刀具完成，且至多可由三把刀具完成
2. 每把多功能刀具 Si 可执行的工序在 2 到 5 道之间
3. 存在一种刀具配置方案，能够完成所有加工工序 E
4. 最少需要的刀具种类数 K 满足：2 小于等于 K 小于等于 4（注：即 K 介于 2 到 4 之间）

你的目标：
找出最少需要的刀具种类数 K，并给出一个包含 K 把刀具的索引集合 H，使得这些刀具的功能总和恰好覆盖全部工序 E。

你可以使用以下三种查询方式（每次查询计入总次数）：

1. **加工能力查询**：询问刀具 Si 是否能执行工序 ej
   - 格式：<query_member>Si,ej</query_member>
   - 示例：<query_member>S1,e3</query_member>
   - 返回：是 或 否

2. **工序检验查询**：给定一组刀具组合，查询哪些工序仍无法完成
   - 格式：<query_coverage>S1,S2,S3</query_coverage>
   - 示例：<query_coverage>S1,S3</query_coverage>
   - 返回：无法完成的工序列表（按升序），若全部覆盖则返回"无"

3. **不可或缺性查询**：询问某把刀具 Si 是否不可或缺（即是否存在只能由它执行的工序）
   - 格式：<query_essential>Si</query_essential>
   - 示例：<query_essential>S5</query_essential>
   - 返回：若不可或缺，返回"是：{...}"（括号内列出至少一道仅由该刀具执行的工序）；否则返回"否"

提交最终答案时，需要说明最少刀具种类数 K 和具体的刀具索引集合 H（用逗号分隔），格式如下：

<answer>K=3, H=S1,S4,S6</answer>

注意：
- 请尽可能少地使用查询次数
- 查询格式必须严格遵守上述 XML 格式
- 答案必须是真正的最小覆盖（不存在使用更少刀具的配置方案）
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
To optimize a flexible production line, let's conduct a "Minimum Tool Coverage" scheduling task. Here are the rules:

The production task requires completing a set of complex machining operations E = {{e1, e2, e3, e4, e5, e6, e7, e8}}, and we have a batch of candidate multi-functional cutting tools S = {{S1, S2, S3, S4, S5, S6, S7}}, where each tool Si can perform a subset of operations in E. The specific capabilities of these tools are hidden, and you need to investigate through queries.

Production constraints:
1. Each operation can be performed by at least one tool and at most three tools
2. Each multi-functional tool Si can perform between 2 and 5 operations
3. There exists a tool configuration that can complete all machining operations in E
4. The minimum number of tool types K satisfies: 2 less than or equal to K less than or equal to 4

Your goal:
Find the minimum number of tool types K and provide an index set H of size K, such that the sum of their capabilities covers all operations E.

You can use the following three types of queries (each query counts toward the total):

1. **Machining Capability Query**: Ask if a tool Si can perform operation ej
   - Format: <query_member>Si,ej</query_member>
   - Example: <query_member>S1,e3</query_member>
   - Returns: Yes or No

2. **Operation Check Query**: Given a set of tool combinations, query which operations are still unable to be completed
   - Format: <query_coverage>S1,S2,S3</query_coverage>
   - Example: <query_coverage>S1,S3</query_coverage>
   - Returns: List of incomplete operations (in ascending order), or "None" if all covered

3. **Essentiality Query**: Ask if a tool Si is essential (i.e., whether there exists an operation that can only be performed by it)
   - Format: <query_essential>Si</query_essential>
   - Example: <query_essential>S5</query_essential>
   - Returns: If essential, return "Yes: {...}" (with at least one witness operation); otherwise return "No"

When submitting the final answer, specify the minimum number of tool types K and the specific tool index set H (comma-separated), using this format:

<answer>K=3, H=S1,S4,S6</answer>

Notes:
- Try to minimize the number of queries used
- Query format must strictly follow the XML format above
- The answer must be a true minimum cover (no configuration using fewer tools exists)
"""

    contextualized_rule_zh_5 = """\
为保障企业合规并控制法务预算，我们来进行一项"最小外部审计团队覆盖"的排查规划，规则如下：

公司梳理了一个核心法律风险点集合 E = {{e1, e2, e3, e4, e5, e6, e7, e8}}，以及一组专业的第三方候选审计团队 S = {{S1, S2, S3, S4, S5, S6, S7}}，其中每个团队 Si 具备排查 E 中部分风险点的资质。各团队擅长的确切排查领域是隐藏的，你需要通过查询来确认。

合规约束：
1. 每个风险点至少被一个团队排查，且至多被三个团队排查
2. 每个团队 Si 的专业排查范围在 2 到 5 个风险点之间
3. 存在一种由部分审计团队组成的方案，能够覆盖所有风险点 E
4. 最少需要雇佣的团队数量 K 满足：2 小于等于 K 小于等于 4（注：即 K 介于 2 到 4 之间）

你的目标：
找出最少雇佣团队数 K，并给出一个包含 K 个团队的索引集合 H，使得这些团队排查资质的并集恰好覆盖全部风险点 E。

你可以使用以下三种查询方式（每次查询计入总次数）：

1. **资质核查查询**：询问团队 Si 是否具备排查风险点 ej 的资质
   - 格式：<query_member>Si,ej</query_member>
   - 示例：<query_member>S1,e3</query_member>
   - 返回：是 或 否

2. **风险盲区检验**：给定一组候选团队，查询哪些风险点仍处于无人排查的盲区
   - 格式：<query_coverage>S1,S2,S3</query_coverage>
   - 示例：<query_coverage>S1,S3</query_coverage>
   - 返回：盲区风险点列表（按升序），若全部覆盖则返回"无"

3. **不可替代性查询**：询问某个团队 Si 是否不可替代（即是否存在只能由它负责排查的风险点）
   - 格式：<query_essential>Si</query_essential>
   - 示例：<query_essential>S5</query_essential>
   - 返回：若不可替代，返回"是：{...}"（括号内列出至少一个仅由该团队排查的风险点）；否则返回"否"

提交最终答案时，需要说明最少雇佣团队数 K 和具体的团队索引集合 H（用逗号分隔），格式如下：

<answer>K=3, H=S1,S4,S6</answer>

注意：
- 请尽可能少地使用查询次数
- 查询格式必须严格遵守上述 XML 格式
- 答案必须是真正的最小覆盖（不存在雇佣更少团队的方案）
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
To ensure corporate compliance and control the legal budget, let's conduct a "Minimum Audit Team Coverage" planning task. Here are the rules:

The company has identified a set of core legal risk points E = {{e1, e2, e3, e4, e5, e6, e7, e8}}, and a set of professional third-party candidate audit teams S = {{S1, S2, S3, S4, S5, S6, S7}}, where each team Si is qualified to review a subset of risks in E. The exact areas of expertise for each team are hidden, and you need to confirm them through queries.

Compliance constraints:
1. Each risk point is covered by at least one team and at most three teams
2. Each team Si is qualified to review between 2 and 5 risk points
3. There exists a plan using a subset of audit teams that can cover all risk points in E
4. The minimum number of hired teams K satisfies: 2 less than or equal to K less than or equal to 4

Your goal:
Find the minimum number of hired teams K and provide an index set H of size K, such that the union of their review qualifications covers all risk points E perfectly.

You can use the following three types of queries (each query counts toward the total):

1. **Qualification Query**: Ask if team Si is qualified to review risk point ej
   - Format: <query_member>Si,ej</query_member>
   - Example: <query_member>S1,e3</query_member>
   - Returns: Yes or No

2. **Blind Spot Check Query**: Given a set of candidate teams, query which risk points remain in unreviewed blind spots
   - Format: <query_coverage>S1,S2,S3</query_coverage>
   - Example: <query_coverage>S1,S3</query_coverage>
   - Returns: List of unreviewed risk points (in ascending order), or "None" if all covered

3. **Irreplaceability Query**: Ask if a team Si is irreplaceable (i.e., whether there exists a risk point that can only be reviewed by them)
   - Format: <query_essential>Si</query_essential>
   - Example: <query_essential>S5</query_essential>
   - Returns: If irreplaceable, return "Yes: {...}" (with at least one witness risk point); otherwise return "No"

When submitting the final answer, specify the minimum number of hired teams K and the specific team index set H (comma-separated), using this format:

<answer>K=3, H=S1,S4,S6</answer>

Notes:
- Try to minimize the number of queries used
- Query format must strictly follow the XML format above
- The answer must be a true minimum cover (no plan hiring fewer teams exists)
"""

    tags = ["answer", "query_member", "query_coverage", "query_essential"]
    
    # 新增类属性
    reasoning_type = "演绎推理"
    data_structure = "集合"

    DIFFICULTY_CONFIG = {
        1: {
            "subsets": {
                "S1": ["e1", "e2", "e3", "e4"],
                "S2": ["e5", "e6", "e7", "e8"],
                "S3": ["e1", "e5"],
                "S4": ["e2", "e6"],
                "S5": ["e3", "e7"],
                "S6": ["e4", "e8"],
                "S7": ["e1", "e2"],
            },
            "min_k": 2,
            "min_solutions": [["S1", "S2"]],
        },
        2: {
            "subsets": {
                "S1": ["e1", "e2", "e3", "e4", "e5"],
                "S2": ["e1", "e2", "e6"],
                "S3": ["e6", "e7", "e8"],
                "S4": ["e3", "e4", "e7"],
                "S5": ["e1", "e5", "e8"],
                "S6": ["e2", "e3"],
                "S7": ["e4", "e5"],
            },
            "min_k": 2,
            "min_solutions": [["S1", "S3"]],
        },
        3: {
            "subsets": {
                "S1": ["e1", "e2", "e3"],
                "S2": ["e1", "e4", "e7"],
                "S3": ["e2", "e5", "e8"],
                "S4": ["e4", "e5", "e6"],
                "S5": ["e3", "e6", "e7"],
                "S6": ["e7", "e8"],
                "S7": ["e1", "e2", "e4", "e5"],
            },
            "min_k": 3,
            "min_solutions": [["S1", "S4", "S6"]],
        },
        4: {
            "subsets": {
                "S1": ["e1", "e2", "e5"],
                "S2": ["e1", "e2", "e3", "e4"],
                "S3": ["e3", "e6", "e7"],
                "S4": ["e4", "e5", "e8"],
                "S5": ["e5", "e6"],
                "S6": ["e1", "e7", "e8"],
                "S7": ["e7", "e8"],
            },
            "min_k": 3,
            "min_solutions": [["S2", "S5", "S7"]],
        },
        5: {
            "subsets": {
                "S1": ["e1", "e2", "e3"],
                "S2": ["e2", "e4", "e5"],
                "S3": ["e3", "e5", "e6"],
                "S4": ["e1", "e7"],
                "S5": ["e4", "e8"],
                "S6": ["e6", "e7"],
                "S7": ["e1", "e8"],
            },
            "min_k": 4,
            "min_solutions": [["S1", "S2", "S6", "S7"], ["S1", "S3", "S4", "S5"]],
        },
    }

    def __init__(self, config):
        # 查询计数器
        self.query_count = 0
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏，根据难度选择配置"""
        diff = self.config.difficulty

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        
        # 存储子集配置
        self.subsets = cfg["subsets"]
        self.min_k = cfg["min_k"]
        self.min_solutions = cfg["min_solutions"]
        
        # 所有元素
        self.all_elements = {"e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8"}
        
        # 初始化游戏信息（用于格式化规则文本，这里不需要）
        self._game_info = {}

    def _compute_coverage(self, subset_indices):
        """计算给定子集索引列表的覆盖情况，返回未覆盖元素集合"""
        covered = set()
        for idx in subset_indices:
            if idx in self.subsets:
                covered.update(self.subsets[idx])
        uncovered = self.all_elements - covered
        return uncovered

    def _is_essential(self, subset_idx):
        """
        判断子集是否不可或缺
        返回 (bool, list): (是否不可或缺, 见证元素列表)
        """
        if subset_idx not in self.subsets:
            return False, []
        
        elements_in_si = set(self.subsets[subset_idx])
        witness_elements = []
        
        # 检查每个元素是否仅被该子集覆盖
        for elem in elements_in_si:
            covered_by = [s for s, members in self.subsets.items() if elem in members]
            if len(covered_by) == 1:  # 仅被当前子集覆盖
                witness_elements.append(elem)
        
        return len(witness_elements) > 0, witness_elements

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案: K=X, H=S1,S2,...
        try:
            parts = [x.strip() for x in raw_ans.split(",")]
            k_part = None
            h_parts = None
            
            for part in parts:
                if "=" in part:
                    key, val = part.split("=", 1)
                    key = key.strip()
                    val = val.strip()
                    if key == "K":
                        k_part = int(val)
                    elif key == "H":
                        h_parts = [x.strip() for x in val.split(",") if x.strip()]
                else:
                    # 可能是 H 的后续部分
                    if h_parts is not None:
                        h_parts.append(part.strip())
            
            if k_part is None or not h_parts:
                return False
            
            # 检查 K 是否等于 H 的大小
            if k_part != len(h_parts):
                return False
            
            # 检查 K 是否是最小值
            if k_part != self.min_k:
                return False
            
            # 检查 H 是否能覆盖所有元素
            uncovered = self._compute_coverage(h_parts)
            if len(uncovered) > 0:
                return False
            
            # 检查 H 是否是有效的最小覆盖解之一
            h_set = set(h_parts)
            for solution in self.min_solutions:
                if h_set == set(solution):
                    return True
            
            # 如果不在预定义解中，但满足最小性和覆盖性，也算正确
            # （这里已经检查过 k_part == min_k 和 uncovered 为空）
            return True
            
        except Exception as e:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始的查询处理逻辑"""
        lang = self.config.language
        yes_word = "是" if lang == "zh" else "Yes"
        no_word = "否" if lang == "zh" else "No"
        none_word = "无" if lang == "zh" else "None"
        
        # 增加查询计数
        self.query_count += 1
        
        # Q1: 成员关系查询
        if "query_member" in parsed_info:
            try:
                raw = parsed_info["query_member"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError("Invalid format")
                
                subset_idx, element = parts[0], parts[1]
                
                if subset_idx not in self.subsets:
                    error_msg = "错误：子集索引无效。" if lang == "zh" else "Error: Invalid subset index."
                    return error_msg
                
                if element not in self.all_elements:
                    error_msg = "错误：元素标签无效。" if lang == "zh" else "Error: Invalid element label."
                    return error_msg
                
                if element in self.subsets[subset_idx]:
                    return yes_word
                else:
                    return no_word
                    
            except Exception as e:
                error_msg = "错误：查询格式无效。" if lang == "zh" else "Error: Invalid query format."
                return error_msg
        
        # Q2: 覆盖检验查询
        elif "query_coverage" in parsed_info:
            try:
                raw = parsed_info["query_coverage"].strip()
                subset_indices = [x.strip() for x in raw.split(",") if x.strip()]
                
                if not subset_indices:
                    error_msg = "错误：必须提供至少一个子集索引。" if lang == "zh" else "Error: Must provide at least one subset index."
                    return error_msg
                
                # 检查所有索引是否有效
                for idx in subset_indices:
                    if idx not in self.subsets:
                        error_msg = f"错误：子集索引 {idx} 无效。" if lang == "zh" else f"Error: Invalid subset index {idx}."
                        return error_msg
                
                uncovered = self._compute_coverage(subset_indices)
                
                if not uncovered:
                    return none_word
                else:
                    # 按升序排列
                    sorted_uncovered = sorted(list(uncovered), key=lambda x: int(x[1:]))
                    return ", ".join(sorted_uncovered)
                    
            except Exception as e:
                error_msg = "错误：查询格式无效。" if lang == "zh" else "Error: Invalid query format."
                return error_msg
        
        # Q3: 不可或缺性查询
        elif "query_essential" in parsed_info:
            try:
                subset_idx = parsed_info["query_essential"].strip()
                
                if subset_idx not in self.subsets:
                    error_msg = "错误：子集索引无效。" if lang == "zh" else "Error: Invalid subset index."
                    return error_msg
                
                is_essential, witnesses = self._is_essential(subset_idx)
                
                if is_essential:
                    # 返回至少一个见证元素
                    witness_str = ", ".join(sorted(witnesses, key=lambda x: int(x[1:])))
                    return f"{yes_word}: {{{witness_str}}}"
                else:
                    return no_word
                    
            except Exception as e:
                error_msg = "错误：查询格式无效。" if lang == "zh" else "Error: Invalid query format."
                return error_msg
        
        else:
            error_msg = "错误：未识别的查询类型。请使用 query_member、query_coverage 或 query_essential。" \
                if lang == "zh" else "Error: Unrecognized query type. Please use query_member, query_coverage, or query_essential."
            raise ValueError(error_msg)

    def _cf_make_wrong(self, correct):
        """生成错误答案"""
        if correct.isdigit():
            return str(int(correct) + 1)
        
        lang = self.config.language
        yes_word = "是" if lang == "zh" else "Yes"
        no_word = "否" if lang == "zh" else "No"
        none_word = "无" if lang == "zh" else "None"
        
        if lang == "zh":
            if correct == "是":
                return "否"
            if correct == "否":
                return "是"
        else:
            if correct == "Yes":
                return "No"
            if correct == "No":
                return "Yes"
            if correct.lower() == "yes":
                return "No" if correct[0].isupper() else "no"
            if correct.lower() == "no":
                return "Yes" if correct[0].isupper() else "yes"
        
        # 覆盖查询返回 "None"/"无" 时，伪造一个未覆盖元素
        if correct == none_word:
            return "e1"
            
        # 如果是不可或缺性查询返回的 "是: {xxx}" 或 "Yes: {xxx}"
        if correct.startswith(f"{yes_word}:"):
            return no_word
            
        # 对于覆盖查询返回的未覆盖元素列表，或者其他，末尾追加 _WRONG
        return f"{correct}_WRONG"
    
    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串，与游戏中 parsed_info["query"] 的值格式一致
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        results = []
        lang = self.config.language
        
        # 定义回答模板
        yes_word = "是" if lang == "zh" else "Yes"
        no_word = "否" if lang == "zh" else "No"
        none_word = "无" if lang == "zh" else "None"

        # 获取排序后的键列表，确保顺序确定性
        subset_keys = sorted(self.subsets.keys(), key=lambda x: int(x[1:]))
        element_keys = sorted(list(self.all_elements), key=lambda x: int(x[1:]))

        # 1. 成员关系查询 (query_member)
        for s_idx in subset_keys:
            for e_idx in element_keys:
                # 构造查询 XML
                query_content = f"{s_idx},{e_idx}"
                query_xml = f"<query_member>{query_content}</query_member>"
                
                # 计算逻辑
                if e_idx in self.subsets[s_idx]:
                    ans = yes_word
                else:
                    ans = no_word
                
                results.append({"query": query_xml, "answer": ans})

        # 2. 覆盖检验查询 (query_coverage)
        # 枚举所有非空子集组合 (S1..S7 的非空子集)
        # 因为 |S|=7，组合总数 2^7-1=127，可以直接全量枚举
        for r in range(1, len(subset_keys) + 1):
            for combo in itertools.combinations(subset_keys, r):
                # combo 是如 ('S1', 'S3') 的元组
                query_content = ",".join(combo)
                query_xml = f"<query_coverage>{query_content}</query_coverage>"
                
                # 计算逻辑
                uncovered = self._compute_coverage(combo)
                if not uncovered:
                    ans = none_word
                else:
                    sorted_uncovered = sorted(list(uncovered), key=lambda x: int(x[1:]))
                    ans = ", ".join(sorted_uncovered)
                
                results.append({"query": query_xml, "answer": ans})

        # 3. 不可或缺性查询 (query_essential)
        for s_idx in subset_keys:
            query_content = s_idx
            query_xml = f"<query_essential>{query_content}</query_essential>"
            
            # 计算逻辑
            is_essential, witnesses = self._is_essential(s_idx)
            if is_essential:
                witness_str = ", ".join(sorted(witnesses, key=lambda x: int(x[1:])))
                ans = f"{yes_word}: {{{witness_str}}}"
            else:
                ans = no_word
                
            results.append({"query": query_xml, "answer": ans})

        return results