from .base import Game
import re

class SetRelationInferenceGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "集合"
    enable_counterfactual = False

    game_rule_zh = """\
我们来玩一个"集合关系推断"游戏。规则如下：

游戏设定了一个宇宙集合 U = {{1,2,3,4,5,6,7,8}}。系统已秘密选定了一个布尔判定函数 f，该函数接受两个集合参数 (L, R)，其中 L 和 R 都是 U 的子集（可以为空集）。

隐藏的判定函数 f 是从以下5个候选规则中选取的：
1. H1: f(L,R)=1 当且仅当 L 与 R 无交集（L 交 R 为空集）
2. H2: f(L,R)=1 当且仅当 L 与 R 有交集（L 交 R 非空）
3. H3: f(L,R)=1 当且仅当 L 是 R 的子集（L 的所有元素都在 R 中）
4. H4: f(L,R)=1 当且仅当 R 是 L 的子集（R 的所有元素都在 L 中）
5. H5: f(L,R)=1 当且仅当 L 与 R 的并集等于全集 U（L 和 R 合起来覆盖所有元素）

你的目标是通过尽可能少的提问来推断出隐藏的规则，并通过两次验证查询来证明你的推断。

每次提问时，你需要给出一对子集 (L, R)，系统会返回"是"或"否"：
- "是"表示 f(L,R)=1
- "否"表示 f(L,R)=0

提问格式使用 XML 标签（L 和 R 中的元素用逗号分隔，可为空）：

<query>L=1,2,3;R=4,5</query>

或空集示例：

<query>L=;R=1,2,3</query>

注意：
- 元素必须是1到8之间的整数
- 同一集合中不能有重复元素
- 格式不正确的提问会返回"格式错误"

当你确定答案后，需要提交：
1. 你推断的规则编号（H1、H2、H3、H4 或 H5）
2. 两次验证查询：
   - 验证A：一对 (L,R)，你认为在该规则下 f(L,R)=1
   - 验证B：一对 (L,R)，你认为在该规则下 f(L,R)=0

答案格式如下：

<answer>rule=H3, verifyA_L=1,2;verifyA_R=1,2,3,4;verifyA_expect=1, verifyB_L=5,6;verifyB_R=1,2;verifyB_expect=0</answer>

其中：
- rule 为你推断的规则编号
- verifyA_L 和 verifyA_R 为验证A的两个集合
- verifyA_expect 为你认为验证A应该返回的值（必须为1）
- verifyB_L 和 verifyB_R 为验证B的两个集合
- verifyB_expect 为你认为验证B应该返回的值（必须为0）

只有当规则编号正确，且两次验证查询的结果都与你的预期一致时，游戏才算成功。
"""

    game_rule_en = """\
Let's play a "Set Relation Inference" game. Here are the rules:

The game defines a universe set U = {{1,2,3,4,5,6,7,8}}. The system has secretly selected a boolean judgment function f that takes two set parameters (L, R), where both L and R are subsets of U (can be empty sets).

The hidden judgment function f is selected from the following 5 candidate rules:
1. H1: f(L,R)=1 if and only if L and R are disjoint (L intersect R is empty)
2. H2: f(L,R)=1 if and only if L and R have intersection (L intersect R is non-empty)
3. H3: f(L,R)=1 if and only if L is a subset of R (all elements of L are in R)
4. H4: f(L,R)=1 if and only if R is a subset of L (all elements of R are in L)
5. H5: f(L,R)=1 if and only if the union of L and R equals the universe U (L and R together cover all elements)

Your goal is to infer the hidden rule through as few queries as possible and prove your inference with two verification queries.

For each query, you need to provide a pair of subsets (L, R), and the system will return "Yes" or "No":
- "Yes" means f(L,R)=1
- "No" means f(L,R)=0

Query format uses XML tags (elements in L and R are comma-separated, can be empty):

<query>L=1,2,3;R=4,5</query>

Or empty set example:

<query>L=;R=1,2,3</query>

Note:
- Elements must be integers between 1 and 8
- No duplicate elements within the same set
- Incorrectly formatted queries will return "Format Error"

When you determine the answer, you need to submit:
1. The rule number you inferred (H1, H2, H3, H4, or H5)
2. Two verification queries:
   - Verification A: a pair (L,R) where you believe f(L,R)=1 under this rule
   - Verification B: a pair (L,R) where you believe f(L,R)=0 under this rule

Answer format:

<answer>rule=H3, verifyA_L=1,2;verifyA_R=1,2,3,4;verifyA_expect=1, verifyB_L=5,6;verifyB_R=1,2;verifyB_expect=0</answer>

Where:
- rule is the rule number you inferred
- verifyA_L and verifyA_R are the two sets for verification A
- verifyA_expect is the value you think verification A should return (must be 1)
- verifyB_L and verifyB_R are the two sets for verification B
- verifyB_expect is the value you think verification B should return (must be 0)

The game succeeds only when the rule number is correct and both verification query results match your expectations.
"""

    contextualized_rule_zh_1 = """\
欢迎进入“城市交通路网调度系统”。
我们管理着城市核心区的 8 个主要交通枢纽，集合 U = {{1,2,3,4,5,6,7,8}}。
系统后台已配置了一项秘密的“路网协同判定规则” f，该规则接受两个车队的覆盖枢纽集合 (L, R) 作为参数，L 和 R 均为 U 的子集（可为空）。

后台判定规则 f 必然是以下 5 种协同模式之一：
1. H1: f(L,R)=1 当且仅当 两车队服务范围无重叠（L 与 R 无交集）
2. H2: f(L,R)=1 当且仅当 两车队有共享换乘枢纽（L 与 R 有交集）
3. H3: f(L,R)=1 当且仅当 车队 L 的服务范围被车队 R 完全覆盖（L 是 R 的子集）
4. H4: f(L,R)=1 当且仅当 车队 R 的服务范围被车队 L 完全覆盖（R 是 L 的子集）
5. H5: f(L,R)=1 当且仅当 两车队联运可覆盖所有枢纽（L 与 R 的并集等于全集 U）

你的目标是通过尽量少的测试来推断出当前的协同模式，并通过两次验证查询来证明你的结论。

每次测试时，你需要提交一对服务子集 (L, R)，系统会返回"是"或"否"：
- "是"表示 f(L,R)=1
- "否"表示 f(L,R)=0

测试格式使用 XML 标签（元素用逗号分隔，可为空）：
<query>L=1,2,3;R=4,5</query>
或空集示例：
<query>L=;R=1,2,3</query>

注意：
- 枢纽编号必须为 1 到 8 之间的整数
- 同一集合中不能有重复枢纽
- 格式不正确的测试会返回"格式错误"

当你确定判定规则后，需要提交：
1. 你推断的协同模式编号（H1、H2、H3、H4 或 H5）
2. 两次验证查询：
   - 验证A：一对 (L,R)，你认为在该规则下 f(L,R)=1
   - 验证B：一对 (L,R)，你认为在该规则下 f(L,R)=0

答案格式如下：
<answer>rule=H3, verifyA_L=1,2;verifyA_R=1,2,3,4;verifyA_expect=1, verifyB_L=5,6;verifyB_R=1,2;verifyB_expect=0</answer>

只有当协同模式编号正确，且两次验证查询的结果都符合预期时，调度系统才会成功解锁。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Urban Traffic Network Dispatch System."
We manage 8 major transit hubs in the city core, forming the universe set U = {{1,2,3,4,5,6,7,8}}.
The system backend has configured a secret "Network Synergy Rule" f, which takes the service coverage of two fleets (L, R) as parameters. L and R are subsets of U (can be empty).

The synergy rule f is selected from the following 5 operational patterns:
1. H1: f(L,R)=1 if and only if the two fleets' service areas do not overlap (L and R are disjoint)
2. H2: f(L,R)=1 if and only if the two fleets share transfer hubs (L and R have an intersection)
3. H3: f(L,R)=1 if and only if fleet L's service area is entirely covered by fleet R (L is a subset of R)
4. H4: f(L,R)=1 if and only if fleet R's service area is entirely covered by fleet L (R is a subset of L)
5. H5: f(L,R)=1 if and only if the two fleets jointly cover the entire grid (the union of L and R equals U)

Your objective is to infer the current synergy pattern with as few tests as possible and prove it using two verification queries.

For each test, submit a pair of service subsets (L, R). The system will return "Yes" or "No":
- "Yes" means f(L,R)=1
- "No" means f(L,R)=0

Query format uses XML tags (hub IDs are comma-separated, can be empty):
<query>L=1,2,3;R=4,5</query>

Note:
- Hub IDs must be integers between 1 and 8.
- No duplicate hubs in a single set.
- Incorrectly formatted tests will return "Format Error."

Once determined, you must submit:
1. The inferred pattern number (H1, H2, H3, H4, or H5).
2. Two verification queries:
   - Verification A: A pair (L,R) where you expect f(L,R)=1.
   - Verification B: A pair (L,R) where you expect f(L,R)=0.

Answer format:
<answer>rule=H3, verifyA_L=1,2;verifyA_R=1,2,3,4;verifyA_expect=1, verifyB_L=5,6;verifyB_R=1,2;verifyB_expect=0</answer>

The system will only unlock if the pattern number is correct and both verifications match the expectations.
"""

    contextualized_rule_zh_2 = """\
欢迎使用“精准医疗靶点分析系统”。
已知某罕见病包含 8 个关键基因靶点，构成靶点集合 U = {{1,2,3,4,5,6,7,8}}。
系统目前预设了一个未知的“药物联合响应函数” f，用于评估两组靶向药物 (L, R) 的相互作用，其中 L 和 R 分别代表两组药物覆盖的靶点子集（可为空）。

响应函数 f 是从以下 5 种药理机制中选定的：
1. H1: f(L,R)=1 当且仅当 两组药物无交叉靶点（L 与 R 无交集，无竞争禁忌）
2. H2: f(L,R)=1 当且仅当 两组药物存在共同靶点（L 与 R 有交集，产生叠加效应）
3. H3: f(L,R)=1 当且仅当 药物 L 的靶点完全包含在 药物 R 中（L 是 R 的子集）
4. H4: f(L,R)=1 当且仅当 药物 R 的靶点完全包含在 药物 L 中（R 是 L 的子集）
5. H5: f(L,R)=1 当且仅当 两组药物联合能覆盖所有致病靶点（L 与 R 的并集等于全集 U）

你的目标是通过尽可能少的临床前测试推断出隐藏的药理机制，并用两次验证查询证明你的推断。

每次测试需输入一对靶点子集 (L, R)，系统返回"是"或"否"：
- "是"表示 f(L,R)=1（符合该机制）
- "否"表示 f(L,R)=0（不符合该机制）

测试格式使用 XML 标签（靶点编号用逗号分隔，可为空）：
<query>L=1,2,3;R=4,5</query>

注意：
- 靶点编号为 1 到 8 之间的整数
- 集合内不能有重复靶点
- 格式不正确返回"格式错误"

当你确定药理机制后，需提交：
1. 推断的机制编号（H1、H2、H3、H4 或 H5）
2. 两次验证查询：
   - 验证A：一对 (L,R)，预期 f(L,R)=1
   - 验证B：一对 (L,R)，预期 f(L,R)=0

答案格式：
<answer>rule=H3, verifyA_L=1,2;verifyA_R=1,2,3,4;verifyA_expect=1, verifyB_L=5,6;verifyB_R=1,2;verifyB_expect=0</answer>

只有规则编号正确且验证查询均符合预期，分析方可完成。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Precision Medicine Target Analysis System."
A rare disease is known to involve 8 key genetic targets, forming the target set U = {{1,2,3,4,5,6,7,8}}.
The system has preset an unknown "Drug Combination Response Function" f to evaluate the interaction of two targeted drugs (L, R), where L and R represent the subsets of targets each drug covers (can be empty).

The response function f is selected from the following 5 pharmacological mechanisms:
1. H1: f(L,R)=1 if and only if the two drugs have no cross-targets (L and R are disjoint, no competitive contraindication).
2. H2: f(L,R)=1 if and only if the two drugs share common targets (L and R have an intersection, producing additive effects).
3. H3: f(L,R)=1 if and only if drug L's targets are completely subsumed by drug R's (L is a subset of R).
4. H4: f(L,R)=1 if and only if drug R's targets are completely subsumed by drug L's (R is a subset of L).
5. H5: f(L,R)=1 if and only if the combination of the two drugs covers all disease targets (the union of L and R equals U).

Your goal is to deduce the hidden pharmacological mechanism through minimal preclinical testing and prove your deduction with two verification queries.

For each test, input a pair of target subsets (L, R). The system returns "Yes" or "No":
- "Yes" means f(L,R)=1
- "No" means f(L,R)=0

Query format uses XML tags (target IDs are comma-separated, can be empty):
<query>L=1,2,3;R=4,5</query>

Note:
- Target IDs must be integers between 1 and 8.
- No duplicate targets in a set.
- Incorrect formats return "Format Error."

Once determined, submit:
1. The inferred mechanism number (H1, H2, H3, H4, or H5).
2. Two verification queries:
   - Verification A: A pair (L,R) expected to yield f(L,R)=1.
   - Verification B: A pair (L,R) expected to yield f(L,R)=0.

Answer format:
<answer>rule=H3, verifyA_L=1,2;verifyA_R=1,2,3,4;verifyA_expect=1, verifyB_L=5,6;verifyB_R=1,2;verifyB_expect=0</answer>

Analysis is complete only when the mechanism number and both verification queries are absolutely correct.
"""

    contextualized_rule_zh_3 = """\
欢迎进入“智能课程体系建设平台”。
我们定义了 8 项学生核心素养模块，构成全集 U = {{1,2,3,4,5,6,7,8}}。
教务系统内置了一个隐藏的“课程评估指标” f，用于校验两套教学大纲 (L, R) 的结构关系，L 和 R 分别代表大纲覆盖的素养子集（可为空）。

隐藏指标 f 取自以下 5 种教学设计理念：
1. H1: f(L,R)=1 当且仅当 两套大纲内容完全独立（L 与 R 无交集）
2. H2: f(L,R)=1 当且仅当 两套大纲有跨学科融合（L 与 R 有交集）
3. H3: f(L,R)=1 当且仅当 大纲 L 是 大纲 R 的先修基础（L 是 R 的子集）
4. H4: f(L,R)=1 当且仅当 大纲 R 是 大纲 L 的先修基础（R 是 L 的子集）
5. H5: f(L,R)=1 当且仅当 两套大纲联合实现了全人教育（L 与 R 的并集涵盖了全集 U）

你的目标是通过最少的教务查询来推断出当前的教学设计理念，并通过两次验证加以证明。

每次查询提供两套素养子集 (L, R)，系统返回"是"或"否"：
- "是"表示 f(L,R)=1
- "否"表示 f(L,R)=0

查询格式使用 XML 标签（模块编号逗号分隔，可为空）：
<query>L=1,2,3;R=4,5</query>

注意：
- 模块必须为 1 到 8 的整数
- 集合无重复元素
- 错误格式返回"格式错误"

确定设计理念后，需提交：
1. 推断的理念编号（H1、H2、H3、H4 或 H5）
2. 两次验证查询：
   - 验证A：一对 (L,R)，预期 f(L,R)=1
   - 验证B：一对 (L,R)，预期 f(L,R)=0

答案格式如下：
<answer>rule=H3, verifyA_L=1,2;verifyA_R=1,2,3,4;verifyA_expect=1, verifyB_L=5,6;verifyB_R=1,2;verifyB_expect=0</answer>

规则编号与两次验证全对，方可保存课程体系。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Intelligent Curriculum Development Platform."
We have defined 8 core student competency modules, constituting the universal set U = {{1,2,3,4,5,6,7,8}}.
The academic system features a hidden "Curriculum Evaluation Metric" f to verify the structural relationship between two syllabi (L, R), where L and R represent the competency subsets covered by each syllabus (can be empty).

The metric f is drawn from 5 instructional design philosophies:
1. H1: f(L,R)=1 if and only if the two syllabi are completely independent (L and R are disjoint).
2. H2: f(L,R)=1 if and only if the two syllabi feature interdisciplinary integration (L and R have an intersection).
3. H3: f(L,R)=1 if and only if syllabus L is a prerequisite foundation for syllabus R (L is a subset of R).
4. H4: f(L,R)=1 if and only if syllabus R is a prerequisite foundation for syllabus L (R is a subset of L).
5. H5: f(L,R)=1 if and only if the two syllabi jointly achieve holistic education (the union of L and R equals U).

Your goal is to deduce the active design philosophy through minimal academic queries and substantiate it with two verifications.

Provide two competency subsets (L, R) per query. The system returns "Yes" or "No":
- "Yes" means f(L,R)=1
- "No" means f(L,R)=0

Query format uses XML tags (module IDs are comma-separated, can be empty):
<query>L=1,2,3;R=4,5</query>

Note:
- Module IDs must be integers from 1 to 8.
- No duplicates within a set.
- Formatting errors yield "Format Error."

Upon confirming the philosophy, submit:
1. The philosophy number (H1, H2, H3, H4, or H5).
2. Two verifications:
   - Verification A: (L,R) where you expect f(L,R)=1.
   - Verification B: (L,R) where you expect f(L,R)=0.

Answer format:
<answer>rule=H3, verifyA_L=1,2;verifyA_R=1,2,3,4;verifyA_expect=1, verifyB_L=5,6;verifyB_R=1,2;verifyB_expect=0</answer>

The curriculum framework will only be saved if the philosophy number is correct and both verifications pass.
"""

    contextualized_rule_zh_4 = """\
欢迎登录“工业流水线效能检测系统”。
当前自动化车间包含 8 个关键加工工位，构成资源池 U = {{1,2,3,4,5,6,7,8}}。
系统设定了一个隐藏的“工序调度规则” f，接受两个生产批次的资源占用需求 (L, R)，其中 L 和 R 均为 U 的子集（可为空）。

调度规则 f 取自以下 5 种工艺要求：
1. H1: f(L,R)=1 当且仅当 两批次可安全并行（L 与 R 无交集，无资源冲突）
2. H2: f(L,R)=1 当且仅当 两批次存在资源争抢（L 与 R 有交集）
3. H3: f(L,R)=1 当且仅当 批次 L 的工位需求被 批次 R 完全包含（L 是 R 的子集）
4. H4: f(L,R)=1 当且仅当 批次 R 的工位需求被 批次 L 完全包含（R 是 L 的子集）
5. H5: f(L,R)=1 当且仅当 两批次联机运行可激活全产线（L 与 R 的并集覆盖全集 U）

你的目标是通过试运行指令，推断出车间当前的调度规则，并进行两次验证。

每次输入一对资源需求 (L, R)，系统返回"是"或"否"：
- "是"表示符合当前规则 f(L,R)=1
- "否"表示不符合 f(L,R)=0

指令格式使用 XML 标签（工位编号逗号分隔）：
<query>L=1,2,3;R=4,5</query>

注意：
- 工位编号为 1 到 8 的整数
- 集合内不可重复
- 格式错误将打回

确定后，需提交：
1. 规则编号（H1、H2、H3、H4 或 H5）
2. 两次验证指令：
   - 验证A：预期返回1的 (L,R)
   - 验证B：预期返回0的 (L,R)

答案格式：
<answer>rule=H3, verifyA_L=1,2;verifyA_R=1,2,3,4;verifyA_expect=1, verifyB_L=5,6;verifyB_R=1,2;verifyB_expect=0</answer>

推断准确且验证通过，系统将正式下达生产指令。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the "Industrial Assembly Line Efficiency Monitoring System."
The automated workshop comprises 8 critical workstations, forming the resource pool U = {{1,2,3,4,5,6,7,8}}.
The system utilizes a hidden "Process Scheduling Rule" f, accepting the resource demands of two production batches (L, R), where both L and R are subsets of U (can be empty).

The scheduling rule f is based on 1 of 5 operational requirements:
1. H1: f(L,R)=1 if and only if the two batches can run safely in parallel (L and R are disjoint, no resource conflicts).
2. H2: f(L,R)=1 if and only if there is resource contention between the batches (L and R intersect).
3. H3: f(L,R)=1 if and only if the workstation demands of batch L are entirely contained within batch R (L is a subset of R).
4. H4: f(L,R)=1 if and only if the workstation demands of batch R are entirely contained within batch L (R is a subset of L).
5. H5: f(L,R)=1 if and only if the joint operation of both batches activates the entire production line (the union of L and R covers U).

Your task is to deduce the current scheduling rule via trial-run commands and perform two validations.

Submit a pair of resource demands (L, R), and the system returns "Yes" or "No":
- "Yes" means the condition is met, f(L,R)=1.
- "No" means the condition is not met, f(L,R)=0.

Command format uses XML tags (workstation IDs comma-separated, can be empty):
<query>L=1,2,3;R=4,5</query>

Note:
- IDs must be integers from 1 to 8.
- No duplicate IDs in a set.
- Incorrect formats will be rejected.

Once identified, submit:
1. The rule number (H1, H2, H3, H4, or H5).
2. Two validation commands:
   - Validation A: Expected to return 1 for (L,R).
   - Validation B: Expected to return 0 for (L,R).

Format:
<answer>rule=H3, verifyA_L=1,2;verifyA_R=1,2,3,4;verifyA_expect=1, verifyB_L=5,6;verifyB_R=1,2;verifyB_expect=0</answer>

Production instructions will only be officially issued upon accurate deduction and successful validation.
"""

    contextualized_rule_zh_5 = """\
欢迎使用“法务合规与专利排查系统”。
某技术领域共划分出 8 项核心专利权利要求，构成保护域 U = {{1,2,3,4,5,6,7,8}}。
审查系统内置了一个秘密的“侵权/合规判定标准” f，用于比对两份技术方案 (L, R) 的权利主张，L 和 R 分别是 U 的子集（可为空）。

判定标准 f 为以下 5 种法律适用情形之一：
1. H1: f(L,R)=1 当且仅当 两方案互不侵权（L 与 R 的权利要求无交集）
2. H2: f(L,R)=1 当且仅当 两方案存在知识产权纠纷（L 与 R 有交集）
3. H3: f(L,R)=1 当且仅当 方案 L 属于 方案 R 的从属专利（L 是 R 的子集）
4. H4: f(L,R)=1 当且仅当 方案 R 属于 方案 L 的从属专利（R 是 L 的子集）
5. H5: f(L,R)=1 当且仅当 两方案构成了该领域的完整技术壁垒（L 与 R 的并集等于全集 U）

你的目标是通过最少的法务检索，推测出当前的判定标准，并通过两次举证完成排查。

每次检索需提交一对权利子集 (L, R)，系统反馈"是"或"否"：
- "是"表示 f(L,R)=1
- "否"表示 f(L,R)=0

检索格式使用 XML 标签（条款编号逗号分隔）：
<query>L=1,2,3;R=4,5</query>

注意：
- 编号限 1 到 8 的整数
- 集合无重复元素
- 格式错误将驳回

查明标准后提交：
1. 适用的标准编号（H1、H2、H3、H4 或 H5）
2. 两次举证验证：
   - 验证A：一对预期 f(L,R)=1 的 (L,R)
   - 验证B：一对预期 f(L,R)=0 的 (L,R)

格式示例：
<answer>rule=H3, verifyA_L=1,2;verifyA_R=1,2,3,4;verifyA_expect=1, verifyB_L=5,6;verifyB_R=1,2;verifyB_expect=0</answer>

判定正确且举证无误，合规排查方告结案。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Legal Compliance & Patent Screening System."
A specific technological domain is defined by 8 core patent claims, forming the scope of protection U = {{1,2,3,4,5,6,7,8}}.
The examination system operates on a confidential "Infringement/Compliance Judgment Standard" f, which compares the claims of two technical solutions (L, R). L and R are subsets of U (can be empty).

The judgment standard f falls under 1 of 5 legal scenarios:
1. H1: f(L,R)=1 if and only if the solutions are mutually non-infringing (L and R are disjoint).
2. H2: f(L,R)=1 if and only if there is an IP conflict between the solutions (L and R intersect).
3. H3: f(L,R)=1 if and only if solution L is a dependent patent of solution R (L is a subset of R).
4. H4: f(L,R)=1 if and only if solution R is a dependent patent of solution L (R is a subset of L).
5. H5: f(L,R)=1 if and only if the two solutions jointly establish a complete patent thicket in the domain (the union of L and R equals U).

Your objective is to infer the active standard through minimal legal queries and finalize the screening with two evidentiary proofs.

Submit a pair of claim subsets (L, R) for each query. The system replies "Yes" or "No":
- "Yes" means f(L,R)=1.
- "No" means f(L,R)=0.

Query format uses XML tags (clause numbers comma-separated, can be empty):
<query>L=1,2,3;R=4,5</query>

Note:
- Numbers must be integers from 1 to 8.
- Sets cannot contain duplicates.
- Formatting errors will result in rejection.

Upon confirming the standard, submit:
1. The applicable standard number (H1, H2, H3, H4, or H5).
2. Two evidentiary proofs:
   - Verification A: A pair (L,R) expected to yield f(L,R)=1.
   - Verification B: A pair (L,R) expected to yield f(L,R)=0.

Answer format:
<answer>rule=H3, verifyA_L=1,2;verifyA_R=1,2,3,4;verifyA_expect=1, verifyB_L=5,6;verifyB_R=1,2;verifyB_expect=0</answer>

The compliance screening will only be closed if the judgment is accurate and the evidence is flawless.
"""

    tags = ["answer", "query"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"rule": "H1"},
            2: {"rule": "H2"},
            3: {"rule": "H3"},
            4: {"rule": "H4"},
            5: {"rule": "H5"},
        },
        "en": {
            1: {"rule": "H1"},
            2: {"rule": "H2"},
            3: {"rule": "H3"},
            4: {"rule": "H4"},
            5: {"rule": "H5"},
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
        self.hidden_rule = cfg["rule"]
        self.universe = set(range(1, 9))
        self.query_count = 0
        self._game_info["n"] = 8

        self._cf_round_counter = 0
        self._cf_correct_resp  = None
        self._cf_wrong_resp    = None

    def _evaluate_rule(self, L: set, R: set) -> bool:
        if self.hidden_rule == "H1":
            return len(L & R) == 0
        elif self.hidden_rule == "H2":
            return len(L & R) > 0
        elif self.hidden_rule == "H3":
            return L.issubset(R)
        elif self.hidden_rule == "H4":
            return R.issubset(L)
        elif self.hidden_rule == "H5":
            return (L | R) == self.universe
        else:
            raise ValueError(f"Unknown rule: {self.hidden_rule}")

    def _parse_set(self, s: str) -> set:
        s = s.strip()
        if not s:
            return set()
        elements = []
        for elem in s.split(","):
            elem = elem.strip()
            if not elem:
                continue
            try:
                num = int(elem)
                if num < 1 or num > 8:
                    raise ValueError(f"Element out of range: {num}")
                if num in elements:
                    raise ValueError(f"Duplicate element: {num}")
                elements.append(num)
            except ValueError as e:
                raise ValueError(f"Invalid element: {elem}") from e
        return set(elements)

    def evaluate(self, parsed_info):
        raw_ans = parsed_info.get("answer", "")
        
        try:
            rule_match = re.search(r'rule\s*=\s*(H[1-5])', raw_ans, re.IGNORECASE)
            if not rule_match:
                return False
            
            submitted_rule = rule_match.group(1).strip().upper()
            if submitted_rule != self.hidden_rule:
                return False
            
            verifyA_L_match = re.search(r'verifyA_L\s*=\s*([^;]*)', raw_ans, re.IGNORECASE)
            verifyA_R_match = re.search(r'verifyA_R\s*=\s*([^;]*)', raw_ans, re.IGNORECASE)
            verifyA_expect_match = re.search(r'verifyA_expect\s*=\s*(\d+)', raw_ans, re.IGNORECASE)
            verifyB_L_match = re.search(r'verifyB_L\s*=\s*([^;]*)', raw_ans, re.IGNORECASE)
            verifyB_R_match = re.search(r'verifyB_R\s*=\s*([^;]*)', raw_ans, re.IGNORECASE)
            verifyB_expect_match = re.search(r'verifyB_expect\s*=\s*(\d+)', raw_ans, re.IGNORECASE)
            
            if not all([verifyA_L_match, verifyA_R_match, verifyA_expect_match,
                         verifyB_L_match, verifyB_R_match, verifyB_expect_match]):
                return False
            
            def _clean_set_str(s):
                s = s.strip().rstrip(',').strip()
                tokens = s.split(',')
                clean_tokens = []
                for t in tokens:
                    t = t.strip()
                    if t.isdigit() and 1 <= int(t) <= 8:
                        clean_tokens.append(t)
                    elif t == '':
                        continue
                    else:
                        break
                return ','.join(clean_tokens)
            
            verifyA_L = self._parse_set(_clean_set_str(verifyA_L_match.group(1)))
            verifyA_R = self._parse_set(_clean_set_str(verifyA_R_match.group(1)))
            verifyA_expect = int(verifyA_expect_match.group(1))
            
            verifyB_L = self._parse_set(_clean_set_str(verifyB_L_match.group(1)))
            verifyB_R = self._parse_set(_clean_set_str(verifyB_R_match.group(1)))
            verifyB_expect = int(verifyB_expect_match.group(1))
            
            if verifyA_expect != 1 or verifyB_expect != 0:
                return False
            
            verifyA_actual = 1 if self._evaluate_rule(verifyA_L, verifyA_R) else 0
            verifyB_actual = 1 if self._evaluate_rule(verifyB_L, verifyB_R) else 0
            
            return (verifyA_actual == verifyA_expect) and (verifyB_actual == verifyB_expect)
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        if "query" not in parsed_info:
            raise ValueError("No query found in request.")
        
        query_str = parsed_info["query"].strip()
        
        try:
            parts = query_str.split(";")
            if len(parts) != 2:
                raise ValueError("Query must contain exactly two parts separated by ';'")
            
            L_part = parts[0].strip()
            R_part = parts[1].strip()
            
            if not L_part.upper().startswith("L="):
                raise ValueError("First part must start with 'L='")
            if not R_part.upper().startswith("R="):
                raise ValueError("Second part must start with 'R='")
            
            L_str = L_part[2:].strip()
            R_str = R_part[2:].strip()
            
            L = self._parse_set(L_str)
            R = self._parse_set(R_str)
            
        except Exception as e:
            error_msg = "格式错误" if self.config.language == "zh" else "Format Error"
            return error_msg
        
        result = self._evaluate_rule(L, R)
        self.query_count += 1
        
        if self.config.language == "zh":
            return "是" if result else "否"
        else:
            return "Yes" if result else "No"

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            elif correct == "否":
                return "是"
        else:
            if correct.lower() == "yes":
                return "No"
            elif correct.lower() == "no":
                return "Yes"
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        import itertools
        import random as _random

        universe_elements = sorted(list(self.universe))
        
        representative = [
            (),
            (1,),
            (1, 2),
            (1, 2, 3, 4),
            (5, 6, 7, 8),
            (1, 2, 3, 4, 5, 6, 7, 8)
        ]
        
        processed_subsets = []
        for s_tuple in representative:
            s_set = set(s_tuple)
            if not s_tuple:
                s_str = ""
            else:
                s_str = ",".join(map(str, s_tuple))
            processed_subsets.append((s_set, s_str))
            
        results = []
        is_zh = (self.config.language == "zh")
        
        for l_set, l_str in processed_subsets:
            for r_set, r_str in processed_subsets:
                query_content = f"L={l_str};R={r_str}"
                
                is_true = self._evaluate_rule(l_set, r_set)
                
                if is_zh:
                    ans = "是" if is_true else "否"
                else:
                    ans = "Yes" if is_true else "No"
                
                results.append({
                    "query": f"<query>{query_content}</query>",
                    "answer": ans
                })
                
        return results