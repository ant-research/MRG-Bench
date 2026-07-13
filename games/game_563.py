# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   最小顶点覆盖：覆盖所有边所需的最少节点数是多少
# ============================================================

from .base import Game
import re
import itertools


class MinimalVertexCoverGame(Game):

    game_rule_zh = """\
我们现在来玩一个"隐藏图的最小顶点覆盖"推理游戏，规则如下：

游戏设定了一个顶点集合 V = {{A, B, C, D, E, F, G, H}}。我已秘密构建了一个简单无向图（无自环、无重边），边集合 E 完全隐藏。

**顶点覆盖定义**：给定顶点子集 S，若图中每条边的至少一个端点在 S 中，则称 S 覆盖了所有边。

你的目标是找到最小的顶点覆盖集合 S，并提供证据证明其最优性。你可以通过以下四种操作与我交互（每次只能选择一种）：

**1. 顶点集测试 (CoverTest)**
测试给定顶点集是否覆盖所有边。
格式：
<cover_test>A B C</cover_test>

响应：
- 若覆盖所有边：Covered: YES | Size: [集合大小]
- 若未覆盖：Covered: NO | UncoveredCount: [未覆盖边数] | ExampleEdge: [一条未覆盖的边，如 A-B]
  注意：返回的示例边会被加入你的"已知边集合"，供后续使用。

**2. 下界验证 (LowerBound)**
提交一组已知边，验证它们是否构成匹配（两两不共享端点），以此确立最小覆盖规模的下界。
格式：
<lower_bound>A-B; C-D; E-F</lower_bound>

响应：
- 若有效：LowerBoundValid: YES | Bound: [匹配边数]（会更新已确立的下界）
- 若无效：LowerBoundValid: NO | Reason: [NotEdges 或 NotDisjoint]

注意：只能使用"已知边集合"中的边。

**3. 查看已知边 (ShowKnown)**
查看当前通过 CoverTest 获得的所有已知边。
格式：
<show_known></show_known>

响应：
KnownEdges: [按字母序排列的边列表]

**4. 提交最优答案 (ClaimMinimal)**
提交你认为的最小顶点覆盖集合及其最优性证据。
格式：
<claim_minimal>S=A B C || Evidence=A-D; B-E; C-F</claim_minimal>

校验条件：
1) S 必须覆盖所有边
2) Evidence 中的边必须已通过 LowerBound 验证，且规模为 m
3) S 的大小必须等于 m

响应：
- 若全部满足：Win: YES | MinimalSize: [m] | OneOptimalSet: [S]
- 否则：Win: NO | Reason: [NotCovered / EvidenceInvalid / SizeMismatch]

**提示**：
- 图结构完全隐藏，需要通过测试失败来逐步发现边
- 匹配的规模给出了最小覆盖的下界
- 你需要尽可能少的交互次数找到答案
"""

    game_rule_en = """\
Let's play a "Hidden Graph Minimal Vertex Cover" deduction game. Here are the rules:

The game has a fixed vertex set V = {{A, B, C, D, E, F, G, H}}. I have secretly constructed a simple undirected graph (no self-loops, no multiple edges) with a completely hidden edge set E.

**Vertex Cover Definition**: Given a vertex subset S, if at least one endpoint of every edge in the graph is in S, then S covers all edges.

Your goal is to find the minimal vertex cover set S and provide evidence proving its optimality. You can interact with me through four types of operations (one at a time):

**1. Cover Test (CoverTest)**
Test whether a given vertex set covers all edges.
Format:
<cover_test>A B C</cover_test>

Response:
- If it covers all edges: Covered: YES | Size: [size of the set]
- If not covered: Covered: NO | UncoveredCount: [number of uncovered edges] | ExampleEdge: [an uncovered edge, e.g., A-B]
  Note: The returned example edge will be added to your "known edge set" for future use.

**2. Lower Bound Verification (LowerBound)**
Submit a set of known edges to verify if they form a matching (pairwise disjoint), establishing a lower bound on the minimal cover size.
Format:
<lower_bound>A-B; C-D; E-F</lower_bound>

Response:
- If valid: LowerBoundValid: YES | Bound: [number of matching edges] (updates the established lower bound)
- If invalid: LowerBoundValid: NO | Reason: [NotEdges or NotDisjoint]

Note: Only edges from the "known edge set" can be used.

**3. Show Known Edges (ShowKnown)**
View all edges currently discovered through CoverTest.
Format:
<show_known></show_known>

Response:
KnownEdges: [list of edges in alphabetical order]

**4. Claim Minimal Solution (ClaimMinimal)**
Submit your proposed minimal vertex cover set and optimality evidence.
Format:
<claim_minimal>S=A B C || Evidence=A-D; B-E; C-F</claim_minimal>

Verification conditions:
1) S must cover all edges
2) Evidence edges must be previously verified via LowerBound with size m
3) Size of S must equal m

Response:
- If all satisfied: Win: YES | MinimalSize: [m] | OneOptimalSet: [S]
- Otherwise: Win: NO | Reason: [NotCovered / EvidenceInvalid / SizeMismatch]

**Notes**:
- The graph structure is completely hidden; you discover edges through failed tests
- The size of a matching provides a lower bound for the minimal cover
- You should find the answer with as few interactions as possible
"""

    contextualized_rule_zh_1 = """\
欢迎来到“城市交通盲区监测”规划系统。

城市中设定了8个关键交通枢纽 V = {{A, B, C, D, E, F, G, H}}。根据交通大数据显示，枢纽之间存在若干条隐蔽的“高危拥堵路段”（无自环、无重边），这些路段的集合 E 目前对你是隐藏的。

**监测覆盖定义**：给定一个被部署了监控基站的枢纽子集 S，如果路网中每一条高危路段的至少一个端点枢纽位于 S 中，我们就称 S 实现了对所有高危路段的有效监测覆盖。

你的目标是找到部署监控基站的最少枢纽集合 S，并提供证据证明其是最优的（成本最低）。你可以通过以下四种操作与系统交互（每次只能选择一种）：

**1. 部署测试 (CoverTest)**
测试给定的一组枢纽是否能覆盖所有高危路段。
格式：
<cover_test>A B C</cover_test>

响应：
- 若覆盖所有路段：Covered: YES | Size: [集合大小]
- 若未覆盖：Covered: NO | UncoveredCount: [未覆盖路段数] | ExampleEdge: [一条未覆盖的路段，如 A-B]
  注意：返回的示例路段会被加入你的“已知高危路段库”，供后续使用。

**2. 下界验证 (LowerBound)**
提交一组已知路段，验证它们是否构成物理上相互独立的路段（两两不共享端点枢纽），以此确立最少基站规模的理论下界。
格式：
<lower_bound>A-B; C-D; E-F</lower_bound>

响应：
- 若有效：LowerBoundValid: YES | Bound: [独立路段数]（会更新已确立的下界）
- 若无效：LowerBoundValid: NO | Reason: [NotEdges 或 NotDisjoint]

注意：只能使用“已知高危路段库”中的路段。

**3. 查看已知路段 (ShowKnown)**
查看当前通过部署测试失败而揭露的所有已知高危路段。
格式：
<show_known></show_known>

响应：
KnownEdges: [按字母序排列的路段列表]

**4. 提交最优方案 (ClaimMinimal)**
提交你认为的最少监控部署枢纽集合及其最优性证据。
格式：
<claim_minimal>S=A B C || Evidence=A-D; B-E; C-F</claim_minimal>

校验条件：
1) S 必须覆盖所有高危路段
2) Evidence 中的独立路段必须已通过 LowerBound 验证，且规模为 m
3) S 的大小必须等于 m

响应：
- 若全部满足：Win: YES | MinimalSize: [m] | OneOptimalSet: [S]
- 否则：Win: NO | Reason: [NotCovered / EvidenceInvalid / SizeMismatch]

**提示**：
- 路网高危状态完全隐藏，需要通过试错式部署来逐步排查
- 相互独立的拥堵路段数量决定了监控成本的下界
- 你需要尽可能少的交互次数找到最佳规划策略
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Urban Traffic Blind Spot Monitoring" planning system.

The city network comprises 8 key traffic hubs V = {{A, B, C, D, E, F, G, H}}. According to traffic big data, there are several hidden "high-risk congested routes" (no self-loops, no multiple edges) between these hubs. The set of these routes E is completely hidden from you.

**Monitoring Cover Definition**: Given a subset of hubs S deployed with monitoring stations, if at least one endpoint hub of every high-risk route is in S, then S effectively covers all high-risk routes.

Your goal is to find the minimal hub set S to deploy monitoring stations and provide evidence proving its optimality (lowest cost). You can interact with the system through four types of operations (one at a time):

**1. Deployment Test (CoverTest)**
Test whether a given set of hubs covers all high-risk routes.
Format:
<cover_test>A B C</cover_test>

Response:
- If it covers all routes: Covered: YES | Size: [size of the set]
- If not covered: Covered: NO | UncoveredCount: [number of uncovered routes] | ExampleEdge: [an uncovered route, e.g., A-B]
  Note: The returned example route will be added to your "known route repository" for future use.

**2. Lower Bound Verification (LowerBound)**
Submit a set of known routes to verify if they are physically independent (pairwise disjoint, sharing no endpoint hubs), establishing a theoretical lower bound on the minimal monitoring size.
Format:
<lower_bound>A-B; C-D; E-F</lower_bound>

Response:
- If valid: LowerBoundValid: YES | Bound: [number of independent routes] (updates the established lower bound)
- If invalid: LowerBoundValid: NO | Reason: [NotEdges or NotDisjoint]

Note: Only routes from the "known route repository" can be used.

**3. Show Known Routes (ShowKnown)**
View all high-risk routes currently discovered through failed deployment tests.
Format:
<show_known></show_known>

Response:
KnownEdges: [list of routes in alphabetical order]

**4. Claim Minimal Solution (ClaimMinimal)**
Submit your proposed minimal monitoring hub set and optimality evidence.
Format:
<claim_minimal>S=A B C || Evidence=A-D; B-E; C-F</claim_minimal>

Verification conditions:
1) S must cover all high-risk routes
2) Evidence routes must be previously verified via LowerBound with size m
3) Size of S must equal m

Response:
- If all satisfied: Win: YES | MinimalSize: [m] | OneOptimalSet: [S]
- Otherwise: Win: NO | Reason: [NotCovered / EvidenceInvalid / SizeMismatch]

**Notes**:
- The high-risk network topology is completely hidden; you discover routes through failed tests
- The number of mutually independent congested routes provides a lower bound for the minimal deployment cost
- You should find the answer with as few interactions as possible
"""

    contextualized_rule_zh_2 = """\
欢迎使用“致病蛋白相互作用”靶向干预系统。

病理模型中标记了8种关键蛋白 V = {{A, B, C, D, E, F, G, H}}。医学研究表明，这些蛋白之间存在若干隐蔽的“致病相互作用”（无自相互作用、无重复作用），这些病理级联反应的集合 E 目前完全隐藏。

**干预覆盖定义**：给定作为靶向抑制剂标靶的蛋白子集 S，如果每一次致病相互作用中至少有一种蛋白位于 S 中（从而被抑制），则称 S 成功阻断了所有致病相互作用。

你的目标是筛选出最少的靶向蛋白组合 S，并提供生化层面相互独立的证据来证明其是最优靶点组合。你可以通过以下四种操作与系统交互（每次只能选择一种）：

**1. 干预测试 (CoverTest)**
测试给定的靶向蛋白组合是否能阻断所有致病相互作用。
格式：
<cover_test>A B C</cover_test>

响应：
- 若阻断所有作用：Covered: YES | Size: [集合大小]
- 若未完全阻断：Covered: NO | UncoveredCount: [未阻断的作用数] | ExampleEdge: [一条未被阻断的相互作用，如 A-B]
  注意：返回的示例相互作用会被加入你的“已知致病作用库”，供后续使用。

**2. 下界验证 (LowerBound)**
提交一组已知的致病作用，验证它们是否构成完全独立的病理反应（两两不共享参与蛋白），以此确立最少抑制剂数量的下界。
格式：
<lower_bound>A-B; C-D; E-F</lower_bound>

响应：
- 若有效：LowerBoundValid: YES | Bound: [独立作用数]（会更新已确立的下界）
- 若无效：LowerBoundValid: NO | Reason: [NotEdges 或 NotDisjoint]

注意：只能使用“已知致病作用库”中的相互作用。

**3. 查看已知相互作用 (ShowKnown)**
查看当前通过干预测试失败而捕获的所有已知致病相互作用。
格式：
<show_known></show_known>

响应：
KnownEdges: [按字母序排列的作用列表]

**4. 提交最优方案 (ClaimMinimal)**
提交你认为的最优靶向蛋白集合及其最优性证据。
格式：
<claim_minimal>S=A B C || Evidence=A-D; B-E; C-F</claim_minimal>

校验条件：
1) S 必须阻断所有致病相互作用
2) Evidence 中的独立作用必须已通过 LowerBound 验证，且规模为 m
3) S 的大小必须等于 m

响应：
- 若全部满足：Win: YES | MinimalSize: [m] | OneOptimalSet: [S]
- 否则：Win: NO | Reason: [NotCovered / EvidenceInvalid / SizeMismatch]

**提示**：
- 完整的病理网络完全隐藏，需要通过药物测试失败来逐步暴露致病机制
- 相互独立的致病反应数量给出了联合用药规模的下界
- 你需要尽可能少的交互次数找到答案
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Pathogenic Protein Interaction" targeted intervention system.

The pathological model identifies 8 key proteins V = {{A, B, C, D, E, F, G, H}}. Medical research indicates there are several hidden "pathogenic interactions" (no self-interactions, no redundant links) between these proteins. The set of these pathological cascades E is completely hidden from you.

**Intervention Cover Definition**: Given a subset of targeted proteins S to be inhibited, if at least one protein in every pathogenic interaction is in S (thus inhibited), then S successfully blocks all pathogenic interactions.

Your goal is to screen for the minimal targeted protein combination S and provide biochemically independent evidence proving its optimality. You can interact with the system through four types of operations (one at a time):

**1. Intervention Test (CoverTest)**
Test whether a given combination of targeted proteins blocks all pathogenic interactions.
Format:
<cover_test>A B C</cover_test>

Response:
- If all interactions blocked: Covered: YES | Size: [size of the set]
- If not fully blocked: Covered: NO | UncoveredCount: [number of unblocked interactions] | ExampleEdge: [an unblocked interaction, e.g., A-B]
  Note: The returned example interaction will be added to your "known pathological interaction repository" for future use.

**2. Lower Bound Verification (LowerBound)**
Submit a set of known interactions to verify if they form completely independent pathological reactions (pairwise disjoint, sharing no proteins), establishing a lower bound on the minimal number of inhibitors required.
Format:
<lower_bound>A-B; C-D; E-F</lower_bound>

Response:
- If valid: LowerBoundValid: YES | Bound: [number of independent interactions] (updates the established lower bound)
- If invalid: LowerBoundValid: NO | Reason: [NotEdges or NotDisjoint]

Note: Only interactions from the "known pathological interaction repository" can be used.

**3. Show Known Interactions (ShowKnown)**
View all pathogenic interactions currently captured through failed intervention tests.
Format:
<show_known></show_known>

Response:
KnownEdges: [list of interactions in alphabetical order]

**4. Claim Minimal Solution (ClaimMinimal)**
Submit your proposed optimal targeted protein set and optimality evidence.
Format:
<claim_minimal>S=A B C || Evidence=A-D; B-E; C-F</claim_minimal>

Verification conditions:
1) S must block all pathogenic interactions
2) Evidence interactions must be previously verified via LowerBound with size m
3) Size of S must equal m

Response:
- If all satisfied: Win: YES | MinimalSize: [m] | OneOptimalSet: [S]
- Otherwise: Win: NO | Reason: [NotCovered / EvidenceInvalid / SizeMismatch]

**Notes**:
- The complete pathological network is hidden; you discover mechanisms through failed drug tests
- The number of mutually independent pathogenic reactions provides a lower bound for combination therapy size
- You should find the answer with as few interactions as possible
"""

    contextualized_rule_zh_3 = """\
欢迎进入“认知盲区诊断与辅导”教学系统。

本课程共有8个核心知识模块 V = {{A, B, C, D, E, F, G, H}}。教育评估表明，模块之间存在若干隐蔽的“交叉认知断层”（无单一模块内部断层，无重复断层），这些认知断层的集合 E 目前对你是未知的。

**辅导覆盖定义**：给定一个指派了专项辅导的知识模块子集 S，如果每一个认知断层涉及的两个模块中至少有一个被纳入了 S 的辅导范围，我们就称 S 弥补了所有的认知断层。

你的目标是制定最精简的专项辅导模块清单 S，并提供证据证明其是最优策略（避免过度增加学生负担）。你可以通过以下四种操作与系统交互：

**1. 教学测试 (CoverTest)**
测试给定的一组辅导模块是否能弥补所有认知断层。
格式：
<cover_test>A B C</cover_test>

响应：
- 若弥补所有断层：Covered: YES | Size: [集合大小]
- 若未完全弥补：Covered: NO | UncoveredCount: [未弥补的断层数] | ExampleEdge: [一个未弥补的断层，如 A-B]
  注意：返回的示例认知断层会被加入你的“已知薄弱环节库”，供后续使用。

**2. 下界验证 (LowerBound)**
提交一组已知的认知断层，验证它们是否是完全无关的断层（两两不共享知识模块），以此确立最少辅导模块数量的下界。
格式：
<lower_bound>A-B; C-D; E-F</lower_bound>

响应：
- 若有效：LowerBoundValid: YES | Bound: [独立断层数]（会更新已确立的下界）
- 若无效：LowerBoundValid: NO | Reason: [NotEdges 或 NotDisjoint]

注意：只能使用“已知薄弱环节库”中的断层。

**3. 查看已知断层 (ShowKnown)**
查看当前通过教学测试失败而诊断出的所有已知认知断层。
格式：
<show_known></show_known>

响应：
KnownEdges: [按字母序排列的断层列表]

**4. 提交最优方案 (ClaimMinimal)**
提交你认为的最精简专项辅导清单及其最优性证据。
格式：
<claim_minimal>S=A B C || Evidence=A-D; B-E; C-F</claim_minimal>

校验条件：
1) S 必须弥补所有认知断层
2) Evidence 中的独立断层必须已通过 LowerBound 验证，且规模为 m
3) S 的大小必须等于 m

响应：
- 若全部满足：Win: YES | MinimalSize: [m] | OneOptimalSet: [S]
- 否则：Win: NO | Reason: [NotCovered / EvidenceInvalid / SizeMismatch]

**提示**：
- 认知障碍网络完全隐藏，需要通过测试反馈来逐步揭示交叉弱点
- 完全无关的断层数量直接决定了必须开启的专项辅导模块的下界
- 你需要尽可能少的交互次数找到答案
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Cognitive Gap Diagnosis and Tutoring" teaching system.

This course consists of 8 core knowledge modules V = {{A, B, C, D, E, F, G, H}}. Educational assessments indicate there are several hidden "cross-module cognitive gaps" (no single-module internal gaps, no redundant gaps). The set of these cognitive gaps E is currently unknown to you.

**Tutoring Cover Definition**: Given a subset of knowledge modules S assigned for specialized tutoring, if at least one of the two modules involved in every cognitive gap is included in S's tutoring scope, then S successfully addresses all cognitive gaps.

Your goal is to formulate the most streamlined specialized tutoring module list S and provide evidence proving its optimality (avoiding excessive burden on students). You can interact with the system through four types of operations:

**1. Teaching Test (CoverTest)**
Test whether a given set of tutoring modules addresses all cognitive gaps.
Format:
<cover_test>A B C</cover_test>

Response:
- If all gaps addressed: Covered: YES | Size: [size of the set]
- If not fully addressed: Covered: NO | UncoveredCount: [number of unaddressed gaps] | ExampleEdge: [an unaddressed gap, e.g., A-B]
  Note: The returned example cognitive gap will be added to your "known weak links repository" for future use.

**2. Lower Bound Verification (LowerBound)**
Submit a set of known cognitive gaps to verify if they are completely unrelated gaps (pairwise disjoint, sharing no modules), establishing a lower bound on the minimum number of tutoring modules required.
Format:
<lower_bound>A-B; C-D; E-F</lower_bound>

Response:
- If valid: LowerBoundValid: YES | Bound: [number of independent gaps] (updates the established lower bound)
- If invalid: LowerBoundValid: NO | Reason: [NotEdges or NotDisjoint]

Note: Only gaps from the "known weak links repository" can be used.

**3. Show Known Gaps (ShowKnown)**
View all cognitive gaps currently diagnosed through failed teaching tests.
Format:
<show_known></show_known>

Response:
KnownEdges: [list of gaps in alphabetical order]

**4. Claim Minimal Solution (ClaimMinimal)**
Submit your proposed streamlined specialized tutoring list and optimality evidence.
Format:
<claim_minimal>S=A B C || Evidence=A-D; B-E; C-F</claim_minimal>

Verification conditions:
1) S must address all cognitive gaps
2) Evidence gaps must be previously verified via LowerBound with size m
3) Size of S must equal m

Response:
- If all satisfied: Win: YES | MinimalSize: [m] | OneOptimalSet: [S]
- Otherwise: Win: NO | Reason: [NotCovered / EvidenceInvalid / SizeMismatch]

**Notes**:
- The cognitive obstacle network is hidden; you reveal cross-weaknesses through test feedback
- The number of completely unrelated gaps directly dictates the lower bound of required specialized modules
- You should find the answer with as few interactions as possible
"""

    contextualized_rule_zh_4 = """\
欢迎使用“工业生产线级联故障隐患”排查系统。

车间内有8个核心生产工作站 V = {{A, B, C, D, E, F, G, H}}。设备运行日志显示，工作站之间潜伏着若干“机械耦合故障隐患”（无单机故障、无重复故障），这些级联隐患的集合 E 对你是不可见的。

**维保覆盖定义**：给定一个派驻了维修工程师的工作站子集 S，如果每一对级联故障隐患中至少有一端的工作站位于 S 中（得到彻底排查），我们就认为 S实现了对全线故障隐患的阻断覆盖。

你的任务是制定最少派驻工程师的排班方案 S，并提供现场数据证明人员配置的极限下界。你可以通过四种操作与系统交互：

**1. 排查测试 (CoverTest)**
测试给定派驻工程师的工作站组合是否能阻断全线故障隐患。
格式：
<cover_test>A B C</cover_test>

响应：
- 若阻断全线隐患：Covered: YES | Size: [集合大小]
- 若未阻断：Covered: NO | UncoveredCount: [漏检的级联隐患数] | ExampleEdge: [一条漏检的故障隐患，如 A-B]
  注意：返回的示例隐患会被记录到你的“已知隐患工单库”中。

**2. 下界验证 (LowerBound)**
提交一组已知的故障隐患，验证它们是否属于各自孤立的机械失效（两两不共享工作站），以此计算最少维修人员需求的物理下界。
格式：
<lower_bound>A-B; C-D; E-F</lower_bound>

响应：
- 若有效：LowerBoundValid: YES | Bound: [孤立隐患数]（会更新已确立的下界）
- 若无效：LowerBoundValid: NO | Reason: [NotEdges 或 NotDisjoint]

注意：只能调用“已知隐患工单库”中的记录。

**3. 查看已知隐患 (ShowKnown)**
调取当前因排查测试未通过而暴露出的一切已知级联隐患。
格式：
<show_known></show_known>

响应：
KnownEdges: [按字母序排列的隐患列表]

**4. 提交最优方案 (ClaimMinimal)**
提交你认为最低成本的维保派驻组合及下界支撑证据。
格式：
<claim_minimal>S=A B C || Evidence=A-D; B-E; C-F</claim_minimal>

校验条件：
1) S 必须覆盖所有级联故障隐患
2) Evidence 中的孤立隐患必须已通过 LowerBound 验证，且规模为 m
3) S 的大小必须等于 m

响应：
- 若全部满足：Win: YES | MinimalSize: [m] | OneOptimalSet: [S]
- 否则：Win: NO | Reason: [NotCovered / EvidenceInvalid / SizeMismatch]

**提示**：
- 隐藏的隐患拓扑需要借助漏检反馈来持续拼凑
- 完全孤立的失效点数量构成了维保人力配置的硬性底线
- 你需要用最少的测试操作推导出最优方案
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the "Industrial Assembly Line Cascading Fault Risk" inspection system.

The workshop houses 8 core production workstations V = {{A, B, C, D, E, F, G, H}}. Equipment logs indicate there are latent "mechanical coupling fault risks" (no single-machine faults, no redundant faults) between workstations. The set of these cascading risks E is invisible to you.

**Maintenance Cover Definition**: Given a subset of workstations S deployed with maintenance engineers, if at least one workstation from every cascading fault pair is in S (and thoroughly inspected), we consider S to have effectively blocked all line fault risks.

Your task is to develop a scheduling plan S deploying the fewest engineers, and provide field data to prove the baseline personnel requirements. You can interact with the system via four operations:

**1. Inspection Test (CoverTest)**
Test whether a given combination of workstations manned by engineers blocks all fault risks.
Format:
<cover_test>A B C</cover_test>

Response:
- If all risks blocked: Covered: YES | Size: [size of the set]
- If not completely blocked: Covered: NO | UncoveredCount: [number of missed cascading risks] | ExampleEdge: [a missed fault risk, e.g., A-B]
  Note: The returned example risk will be recorded in your "known risk work order repository".

**2. Lower Bound Verification (LowerBound)**
Submit a set of known fault risks to verify if they are isolated mechanical failures (pairwise disjoint, sharing no workstations), calculating the physical lower bound for minimum maintenance personnel required.
Format:
<lower_bound>A-B; C-D; E-F</lower_bound>

Response:
- If valid: LowerBoundValid: YES | Bound: [number of isolated risks] (updates the established lower bound)
- If invalid: LowerBoundValid: NO | Reason: [NotEdges or NotDisjoint]

Note: You can only invoke records from the "known risk work order repository".

**3. Show Known Risks (ShowKnown)**
Retrieve all known cascading risks exposed thus far through failed inspection tests.
Format:
<show_known></show_known>

Response:
KnownEdges: [list of risks in alphabetical order]

**4. Claim Minimal Solution (ClaimMinimal)**
Submit your proposed lowest-cost maintenance deployment combination and its lower-bound supporting evidence.
Format:
<claim_minimal>S=A B C || Evidence=A-D; B-E; C-F</claim_minimal>

Verification conditions:
1) S must cover all cascading fault risks
2) Evidence risks must be previously verified via LowerBound with size m
3) Size of S must equal m

Response:
- If all satisfied: Win: YES | MinimalSize: [m] | OneOptimalSet: [S]
- Otherwise: Win: NO | Reason: [NotCovered / EvidenceInvalid / SizeMismatch]

**Notes**:
- The hidden risk topology must be pieced together continuously via missed inspection feedback
- The number of completely isolated failure points constitutes the hard baseline for maintenance manpower allocation
- You should deduce the optimal solution with the fewest test operations
"""

    contextualized_rule_zh_5 = """\
欢迎接入“经侦专案组非法利益输送”分析网络。

案件卷宗锁定了8名核心嫌疑主体 V = {{A, B, C, D, E, F, G, H}}。情报显示，这些主体之间存在若干隐蔽的“双向非法利益输送”（无内部自洗钱，无重复立案记录），完整的输送网络 E 目前被严密伪装。

**调查覆盖定义**：给定一个被采取深度审查措施的嫌疑主体子集 S，如果每一笔非法利益输送交易中，至少有一方的涉案主体被列入 S 中进行突击审讯，则称 S 成功暴露了所有的非法输送链条。

你的目标是精准圈定最少需要启动调查的嫌疑名单 S，并出具确凿的资金链路证明该名单已是最小打击范围。你可以通过以下四种指令展开侦查：

**1. 传唤测试 (CoverTest)**
测试对给定的一组主体发起审查是否足以暴露所有的利益输送。
格式：
<cover_test>A B C</cover_test>

响应：
- 若暴露出所有链条：Covered: YES | Size: [集合大小]
- 若有链条漏网：Covered: NO | UncoveredCount: [未暴露的输送网络数] | ExampleEdge: [一条未暴露的利益输送，如 A-B]
  注意：暴露出的示例交易记录将并入你的“已知犯罪事实库”。

**2. 下界验证 (LowerBound)**
提交一组已知的利益输送交易，验证它们是否属于绝对孤立的作案动作（两两不涉及同一嫌疑主体），借此确定抓捕范围的硬性下限。
格式：
<lower_bound>A-B; C-D; E-F</lower_bound>

响应：
- 若有效：LowerBoundValid: YES | Bound: [孤立交易数]（会更新已确立的下限）
- 若无效：LowerBoundValid: NO | Reason: [NotEdges 或 NotDisjoint]

注意：必须且只能引用“已知犯罪事实库”中的交易。

**3. 查看已知交易 (ShowKnown)**
调阅当前侦查过程中因未达到完全覆盖而被迫浮出水面的所有已知交易记录。
格式：
<show_known></show_known>

响应：
KnownEdges: [按字母序排列的交易列表]

**4. 提交最优方案 (ClaimMinimal)**
提交你认定的最小审查嫌疑名单及支持其不可删减的独立案件证据。
格式：
<claim_minimal>S=A B C || Evidence=A-D; B-E; C-F</claim_minimal>

校验条件：
1) S 必须暴露所有的利益输送网络
2) Evidence 中的孤立交易必须已通过 LowerBound 验证，且规模为 m
3) S 的大小必须等于 m

响应：
- 若全部满足：Win: YES | MinimalSize: [m] | OneOptimalSet: [S]
- 否则：Win: NO | Reason: [NotCovered / EvidenceInvalid / SizeMismatch]

**提示**：
- 洗钱利益网极具隐蔽性，必须通过传唤覆盖失败来钓出关联线索
- 平行作案（互不交叉）的数量锚定了必须审查的最少嫌疑人数
- 专案组资源有限，请用最精简的侦查动作破局
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Economic Crime Task Force Illicit Transaction" analysis network.

The case file locks onto 8 key suspects/legal entities V = {{A, B, C, D, E, F, G, H}}. Intelligence indicates hidden "two-way illicit transactions" (no internal self-laundering, no duplicate case records) exist among these entities. The complete transaction network E is currently heavily disguised.

**Investigation Cover Definition**: Given a subset of suspect entities S subjected to deep investigative measures, if at least one involved entity in every illicit transaction is included in S for a surprise interrogation, then S successfully exposes all illicit transaction chains.

Your goal is to precisely delineate the minimal suspect list S requiring investigation, and issue conclusive financial linkage evidence proving this list is the absolute minimum strike scope. You can conduct reconnaissance via four commands:

**1. Subpoena Test (CoverTest)**
Test whether launching investigations against a given set of entities is sufficient to expose all illicit transactions.
Format:
<cover_test>A B C</cover_test>

Response:
- If all chains exposed: Covered: YES | Size: [size of the set]
- If any chains slip through: Covered: NO | UncoveredCount: [number of unexposed networks] | ExampleEdge: [an unexposed illicit transaction, e.g., A-B]
  Note: The exposed example transaction record will be merged into your "known criminal facts repository".

**2. Lower Bound Verification (LowerBound)**
Submit a set of known illicit transactions to verify if they are absolutely isolated criminal acts (pairwise disjoint, involving no shared suspects), thereby establishing the strict lower limit for the arrest scope.
Format:
<lower_bound>A-B; C-D; E-F</lower_bound>

Response:
- If valid: LowerBoundValid: YES | Bound: [number of isolated transactions] (updates the established lower limit)
- If invalid: LowerBoundValid: NO | Reason: [NotEdges or NotDisjoint]

Note: You must strictly reference transactions from the "known criminal facts repository".

**3. Show Known Transactions (ShowKnown)**
Review all known transaction records currently forced to surface due to incomplete investigation coverage.
Format:
<show_known></show_known>

Response:
KnownEdges: [list of transactions in alphabetical order]

**4. Claim Minimal Solution (ClaimMinimal)**
Submit your identified minimal suspect interrogation list and the independent case evidence supporting its irreducibility.
Format:
<claim_minimal>S=A B C || Evidence=A-D; B-E; C-F</claim_minimal>

Verification conditions:
1) S must expose all illicit transaction networks
2) Evidence isolated transactions must be previously verified via LowerBound with size m
3) Size of S must equal m

Response:
- If all satisfied: Win: YES | MinimalSize: [m] | OneOptimalSet: [S]
- Otherwise: Win: NO | Reason: [NotCovered / EvidenceInvalid / SizeMismatch]

**Notes**:
- The laundering interest network is highly elusive; associated clues must be lured out through failed subpoena coverages
- The number of parallel (non-intersecting) crimes anchors the minimum number of suspects that must be investigated
- Task force resources are limited; please break the case with the most streamlined investigative moves
"""

    tags = ["cover_test", "lower_bound", "show_known", "claim_minimal", "answer"]
    reasoning_type = "归纳推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "edges": [
                    ("A", "B"),
                    ("A", "C"),
                    ("A", "D"),
                ],
                "min_cover_size": 1,
                "one_solution": ["A"],
            },
            2: {
                "edges": [
                    ("A", "B"),
                    ("A", "C"),
                    ("B", "C"),
                    ("D", "E"),
                    ("D", "F"),
                    ("E", "F"),
                ],
                "min_cover_size": 3,
                "one_solution": ["A", "C", "D"],
            },
            3: {
                "edges": [
                    ("A", "B"),
                    ("A", "C"),
                    ("B", "D"),
                    ("C", "D"),
                    ("E", "F"),
                    ("E", "G"),
                    ("F", "H"),
                    ("G", "H"),
                ],
                "min_cover_size": 4,
                "one_solution": ["A", "D", "E", "H"],
            },
            4: {
                "edges": [
                    ("A", "B"),
                    ("A", "C"),
                    ("A", "D"),
                    ("B", "E"),
                    ("C", "F"),
                    ("D", "G"),
                    ("E", "H"),
                    ("F", "H"),
                    ("G", "H"),
                ],
                "min_cover_size": 4,
                "one_solution": ["A", "E", "F", "G"],
            },
            5: {
                "edges": [
                    ("A", "B"),
                    ("A", "E"),
                    ("B", "C"),
                    ("B", "F"),
                    ("C", "D"),
                    ("C", "G"),
                    ("D", "H"),
                    ("E", "F"),
                    ("F", "G"),
                    ("G", "H"),
                ],
                "min_cover_size": 4,
                "one_solution": ["B", "C", "E", "H"],
            },
        },
        "en": {
            1: {
                "edges": [
                    ("A", "B"),
                    ("A", "C"),
                    ("A", "D"),
                ],
                "min_cover_size": 1,
                "one_solution": ["A"],
            },
            2: {
                "edges": [
                    ("A", "B"),
                    ("A", "C"),
                    ("B", "C"),
                    ("D", "E"),
                    ("D", "F"),
                    ("E", "F"),
                ],
                "min_cover_size": 3,
                "one_solution": ["A", "C", "D"],
            },
            3: {
                "edges": [
                    ("A", "B"),
                    ("A", "C"),
                    ("B", "D"),
                    ("C", "D"),
                    ("E", "F"),
                    ("E", "G"),
                    ("F", "H"),
                    ("G", "H"),
                ],
                "min_cover_size": 4,
                "one_solution": ["A", "D", "E", "H"],
            },
            4: {
                "edges": [
                    ("A", "B"),
                    ("A", "C"),
                    ("A", "D"),
                    ("B", "E"),
                    ("C", "F"),
                    ("D", "G"),
                    ("E", "H"),
                    ("F", "H"),
                    ("G", "H"),
                ],
                "min_cover_size": 4,
                "one_solution": ["A", "E", "F", "G"],
            },
            5: {
                "edges": [
                    ("A", "B"),
                    ("A", "E"),
                    ("B", "C"),
                    ("B", "F"),
                    ("C", "D"),
                    ("C", "G"),
                    ("D", "H"),
                    ("E", "F"),
                    ("F", "G"),
                    ("G", "H"),
                ],
                "min_cover_size": 4,
                "one_solution": ["B", "C", "E", "H"],
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏，加载对应难度的图"""
        lang = self.config.language
        diff = self.config.difficulty
        
        # 确保 difficulty 是 int 类型
        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 存储图的边集（规范化为有序对）
        self.edges = set()
        for u, v in cfg["edges"]:
            self.edges.add(tuple(sorted([u, v])))
        
        self.min_cover_size = cfg["min_cover_size"]
        self.one_solution = set(cfg["one_solution"])
        
        self.known_edges = set()
        self.verified_lower_bounds = {}
        self.established_lower_bound = 0
        self.returned_edges = set()
        
        # 设置 _game_info（基类 _init_rule 会用到）
        self._game_info = {}

    def _normalize_edge(self, u, v):
        """将边规范化为字典序排列"""
        return tuple(sorted([u.strip().upper(), v.strip().upper()]))

    def _parse_vertex_set(self, s):
        """解析顶点集合字符串，返回顶点集合"""
        if not s or not s.strip():
            return set()
        return set(v.strip().upper() for v in s.split() if v.strip())

    def _parse_edge_list(self, s):
        """解析边列表字符串，返回边集合"""
        if not s or not s.strip():
            return set()
        edges = set()
        for edge_str in s.split(";"):
            edge_str = edge_str.strip()
            if "-" in edge_str:
                parts = edge_str.split("-")
                if len(parts) == 2:
                    edges.add(self._normalize_edge(parts[0], parts[1]))
        return edges

    def _check_cover(self, vertex_set):
        """检查给定顶点集是否覆盖所有边"""
        uncovered = []
        for edge in self.edges:
            u, v = edge
            if u not in vertex_set and v not in vertex_set:
                uncovered.append(edge)
        return uncovered

    def _get_example_edge(self, uncovered_edges):
        """从未覆盖边中选择一条作为示例，优先选择玩家未知的边"""
        # 优先返回玩家未知的边
        for edge in uncovered_edges:
            if edge not in self.known_edges:
                return edge
        # 如果都已知，返回第一条
        return uncovered_edges[0] if uncovered_edges else None

    def _check_matching(self, edge_set):
        """检查边集是否构成匹配（两两不共享端点）"""
        used_vertices = set()
        for edge in edge_set:
            u, v = edge
            if u in used_vertices or v in used_vertices:
                return False
            used_vertices.add(u)
            used_vertices.add(v)
        return True

    def step(self, response: str):
        """重写 step，使 claim_minimal 也被当作 answer 处理"""
        try:
            parsed_info = self.parse(response)
            # claim_minimal 等同于 answer 提交
            if "claim_minimal" in parsed_info:
                parsed_info["answer"] = parsed_info["claim_minimal"]
            
            if "answer" in parsed_info:
                is_success = self.evaluate(parsed_info)
                if is_success:
                    res = "答案正确" if self.config.language == "zh" else "Correct answer."
                    self.state.set_state("success", "success")
                    self.state.add_message("user", res)
                else:
                    res = "答案错误" if self.config.language == "zh" else "Incorrect answer."
                    self.state.set_state("failed", "incorrect answer")
                    self.state.add_message("user", res)
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))    
        
        return self.state

    def evaluate(self, parsed_info):
        """评估 claim_minimal 答案"""
        raw_ans = parsed_info.get("claim_minimal") or parsed_info.get("answer", "")
        
        # 使用 || 分隔
        parts = raw_ans.split("||")
        if len(parts) != 2:
            return False
        
        s_part = parts[0].strip()
        evidence_part = parts[1].strip()
        
        # 解析 S
        if not s_part.startswith("S="):
            return False
        s_str = s_part[2:].strip()
        proposed_cover = self._parse_vertex_set(s_str)
        
        # 解析 Evidence
        if not evidence_part.startswith("Evidence="):
            return False
        evidence_str = evidence_part[9:].strip()
        evidence_edges = self._parse_edge_list(evidence_str)
        
        # 校验1: S 是否覆盖所有边
        uncovered = self._check_cover(proposed_cover)
        if uncovered:
            return False
        
        # 校验2: Evidence 是否已验证且规模为 m
        m = len(evidence_edges)
        if m == 0 or m not in self.verified_lower_bounds:
            return False
        if evidence_edges != self.verified_lower_bounds[m]:
            return False
        
        # 校验3: |S| 是否等于 m
        if len(proposed_cover) != m:
            return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑"""
        lang = self.config.language
        
        # 处理 cover_test
        if "cover_test" in parsed_info:
            s_str = parsed_info["cover_test"]
            vertex_set = self._parse_vertex_set(s_str)
            uncovered = self._check_cover(vertex_set)
            
            if not uncovered:
                return f"Covered: YES | Size: {len(vertex_set)}"
            else:
                example_edge = self._get_example_edge(uncovered)
                if example_edge:
                    self.known_edges.add(example_edge)
                    self.returned_edges.add(example_edge)
                    u, v = example_edge
                    return f"Covered: NO | UncoveredCount: {len(uncovered)} | ExampleEdge: {u}-{v}"
                else:
                    return f"Covered: NO | UncoveredCount: {len(uncovered)}"
        
        # 处理 lower_bound
        elif "lower_bound" in parsed_info:
            edge_str = parsed_info["lower_bound"]
            edge_set = self._parse_edge_list(edge_str)
            
            # 检查所有边是否都在已知边集合中
            if not edge_set.issubset(self.known_edges):
                return "LowerBoundValid: NO | Reason: NotEdges"
            
            # 检查是否构成匹配
            if not self._check_matching(edge_set):
                return "LowerBoundValid: NO | Reason: NotDisjoint"
            
            # 验证成功，更新下界
            m = len(edge_set)
            self.verified_lower_bounds[m] = edge_set
            self.established_lower_bound = max(self.established_lower_bound, m)
            return f"LowerBoundValid: YES | Bound: {m}"
        
        # 处理 show_known
        elif "show_known" in parsed_info:
            if not self.known_edges:
                return "KnownEdges: []"
            sorted_edges = sorted(self.known_edges)
            edge_strs = [f"{u}-{v}" for u, v in sorted_edges]
            return f"KnownEdges: [{', '.join(edge_strs)}]"
        
        # 处理 claim_minimal
        elif "claim_minimal" in parsed_info:
            # 这里不应该被调用，因为 claim_minimal 会进入 evaluate
            # 但为了完整性，提供一个默认响应
            raw_ans = parsed_info["claim_minimal"]
            parts = raw_ans.split("||")
            if len(parts) != 2:
                return "Win: NO | Reason: InvalidFormat"
            
            s_part = parts[0].strip()
            evidence_part = parts[1].strip()
            
            if not s_part.startswith("S=") or not evidence_part.startswith("Evidence="):
                return "Win: NO | Reason: InvalidFormat"
            
            s_str = s_part[2:].strip()
            evidence_str = evidence_part[9:].strip()
            
            proposed_cover = self._parse_vertex_set(s_str)
            evidence_edges = self._parse_edge_list(evidence_str)
            
            # 检查覆盖
            uncovered = self._check_cover(proposed_cover)
            if uncovered:
                return "Win: NO | Reason: NotCovered"
            
            # 检查证据
            m = len(evidence_edges)
            if m == 0 or m not in self.verified_lower_bounds or evidence_edges != self.verified_lower_bounds[m]:
                return "Win: NO | Reason: EvidenceInvalid"
            
            # 检查规模
            if len(proposed_cover) != m:
                return "Win: NO | Reason: SizeMismatch"
            
            # 全部通过
            return f"Win: YES | MinimalSize: {m} | OneOptimalSet: {{{', '.join(sorted(proposed_cover))}}}"
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 中文
        if "是" in correct:
            return correct.replace("是", "否")
        if "否" in correct:
            return correct.replace("否", "是")
            
        # 英文 (包括 YES/NO, Yes/No, yes/no)
        # 考虑到本游戏主要返回大写的 YES/NO
        if "YES" in correct:
            return correct.replace("YES", "NO")
        if "NO" in correct:
            return correct.replace("NO", "YES")
        if "Yes" in correct:
            return correct.replace("Yes", "No")
        if "No" in correct:
            return correct.replace("No", "Yes")
            
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        queries = []
        vertices = ["A", "B", "C", "D", "E", "F", "G", "H"]
        
        # 1. Enumerate all subsets for cover_test
        for r in range(len(vertices) + 1):
            for subset in itertools.combinations(vertices, r):
                query_content = " ".join(subset)
                query_str = f"<cover_test>{query_content}</cover_test>"
                
                vertex_set = set(subset)
                uncovered = self._check_cover(vertex_set)
                
                if not uncovered:
                    ans = f"Covered: YES | Size: {len(vertex_set)}"
                else:
                    # 使用确定性排序选择第一条未覆盖边
                    sorted_uncovered = sorted(uncovered)
                    example_edge = sorted_uncovered[0]
                    u, v = example_edge
                    ans = f"Covered: NO | UncoveredCount: {len(uncovered)} | ExampleEdge: {u}-{v}"
                
                queries.append({
                    "query": query_str,
                    "answer": ans
                })
        
        # 2. show_known query
        queries.append({
            "query": "<show_known></show_known>",
            "answer": "KnownEdges: []"
        })
        
        # 3. Enumerate some lower_bound queries using actual edges
        # For each subset of edges that forms a valid matching
        edge_list = sorted(self.edges)
        for r in range(1, len(edge_list) + 1):
            for edge_subset in itertools.combinations(edge_list, r):
                edge_set = set(edge_subset)
                if self._check_matching(edge_set):
                    edge_strs = "; ".join(f"{u}-{v}" for u, v in sorted(edge_set))
                    query_str = f"<lower_bound>{edge_strs}</lower_bound>"
                    # Answer assumes all edges are known
                    ans = f"LowerBoundValid: YES | Bound: {len(edge_set)}"
                    queries.append({
                        "query": query_str,
                        "answer": ans
                    })
        
        return queries