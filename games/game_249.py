from .base import Game
import random

class PermutedGraphNeighborGame(Game):
    
    reasoning_type = "归纳推理"
    data_structure = "图"

    game_rule_zh = """\
我们来玩一个"置换图邻域推理"游戏，规则如下：

游戏设定了一个标号集合 V，包含编号 1 到 {n}。存在一个未知的无向简单图 G，其节点集合为 V。同时存在一个未知的一一置换映射 M，将 V 中的每个节点映射到 V 中的另一个节点。

定义可观测邻域函数 F(v) 为：F(v) 等于图 G 中节点 M(v) 的真实邻居集合（不包含 M(v) 自身）。

你的目标是推断出指定目标节点 T = {target} 在真实图 G 中的邻居集合。

你可以反复向我提出以下三类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 集合读取查询：询问节点 a 的可观测邻域，返回 F(a) 的完整集合（不含 M(a)）。
2. 成员判定查询：询问元素 b 是否属于 F(a)，返回"是"或"否"。
3. 交集计数查询：询问 F(a) 与 F(b) 的交集大小，返回一个非负整数。

注意：图 G 和置换 M 在整个游戏过程中固定不变，重复相同的查询将得到相同的答案。图 G 的结构足以区分各个节点，通过对多个节点的可观测邻域进行比较和分析，你可以推断出置换关系，从而确定目标节点的真实邻居集合。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 集合读取查询（例如查询节点 3）：
<query_set>3</query_set>

- 成员判定查询（例如询问节点 5 是否在节点 2 的可观测邻域中）：
<query_member>2,5</query_member>

- 交集计数查询（例如询问节点 1 和节点 4 的可观测邻域交集大小）：
<query_intersect>1,4</query_intersect>

提交最终答案时，列出目标节点 T 在真实图 G 中的所有邻居编号（用逗号隔开，顺序不限），格式如下：

<answer>1,3,5</answer>

如果目标节点没有邻居，提交空集：

<answer></answer>
"""

    game_rule_en = """\
Let's play a "Permuted Graph Neighbor" deduction game. Here are the rules:

There is a labeled set V containing numbers from 1 to {n}. There exists an unknown undirected simple graph G with node set V. Additionally, there exists an unknown one-to-one permutation mapping M that maps each node in V to another node in V.

Define the observable neighborhood function F(v) as: F(v) equals the true neighbor set of node M(v) in graph G (excluding M(v) itself).

Your goal is to infer the neighbor set of the specified target node T = {target} in the true graph G.

You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully based on the true setting:

1. Set Read Query: Ask for the observable neighborhood of node a, returns the complete set F(a) (excluding M(a)).
2. Membership Query: Ask whether element b belongs to F(a), returns "Yes" or "No".
3. Intersection Count Query: Ask for the size of the intersection between F(a) and F(b), returns a non-negative integer.

Note: Graph G and permutation M remain fixed throughout the game; repeated identical queries will yield identical answers. The structure of graph G is sufficient to distinguish individual nodes. By comparing and analyzing the observable neighborhoods of multiple nodes, you can infer the permutation relationship and thus determine the true neighbor set of the target node.

When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Set Read Query (e.g., querying node 3):
<query_set>3</query_set>

- Membership Query (e.g., asking if node 5 is in the observable neighborhood of node 2):
<query_member>2,5</query_member>

- Intersection Count Query (e.g., asking for the intersection size of observable neighborhoods of nodes 1 and 4):
<query_intersect>1,4</query_intersect>

When submitting the final answer, list all neighbor IDs of target node T in the true graph G (comma-separated, order does not matter), using this format:

<answer>1,3,5</answer>

If the target node has no neighbors, submit an empty set:

<answer></answer>
"""

    contextualized_rule_zh_1 = """\
我们来解决一个“轨道交通信号错位推理”问题。

系统内有 1 到 {n} 编号的地铁站点集合 V。这些站点之间存在一个未知的真实物理连接网络 G。由于系统升级故障，控制台产生了一个未知的终端映射 M，使得在控制终端上查询站点 v 时，实际上返回的是另一个站点 M(v) 的数据。

定义终端 v 的可观测相邻站集合 F(v) 为：真实网络 G 中站点 M(v) 的物理相连站点集合（不含 M(v) 自身）。

你的任务是：推断出目标站点 T = {target} 在真实物理网络 G 中的所有直接相连站点。

你可以反复向我提出以下三类数据查询（每次仅限一个问题），我会根据真实设定如实回答：

1. 集合读取查询：询问终端 a 的可观测相邻站，返回 F(a) 的完整集合。
2. 成员判定查询：询问站点 b 是否属于终端 a 的可观测相邻站 F(a)，返回“是”或“否”。
3. 交集计数查询：询问终端 a 和终端 b 的可观测相邻站集合 F(a) 与 F(b) 的交集大小，返回一个非负整数。

注意：物理网络 G 和映射 M 是固定的，重复相同的查询将得到相同的答案。网络 G 的结构足以区分各个站点，通过比对多个终端的可观测相邻站，你可以反推出映射关系，从而定位目标站点的真实连接。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 集合读取查询（例如查询终端 3）：
<query_set>3</query_set>

- 成员判定查询（例如询问站点 5 是否在终端 2 的可观测相邻站中）：
<query_member>2,5</query_member>

- 交集计数查询（例如询问终端 1 和终端 4 的可观测相邻站交集大小）：
<query_intersect>1,4</query_intersect>

提交最终答案时，列出目标站点 T 在真实物理网络 G 中的所有直接相连站点编号（用逗号隔开，顺序不限），格式如下：

<answer>1,3,5</answer>

如果目标站点没有相邻站点，提交空集：

<answer></answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's resolve a "Subway Signal Misalignment Deduction" problem.

There is a set V of subway stations numbered 1 to {n}. An unknown true physical rail network G exists among these stations. Due to a system upgrade failure, an unknown terminal mapping M occurred, meaning that querying station v on the control terminal actually returns data for another station M(v).

Define the observable adjacent stations F(v) for terminal v as: the set of physically connected adjacent stations of M(v) in the true network G (excluding M(v) itself).

Your task is to infer the true physically connected adjacent stations of the target station T = {target} in the true network G.

You can repeatedly ask me three types of data queries (one per turn), and I will answer truthfully based on the true setting:

1. Set Read Query: Ask for the observable adjacent stations of terminal a, returns the complete set F(a).
2. Membership Query: Ask if station b belongs to the observable adjacent stations F(a) of terminal a, returns "Yes" or "No".
3. Intersection Count Query: Ask for the intersection size between F(a) and F(b) of terminals a and b, returns a non-negative integer.

Note: Network G and mapping M remain fixed throughout the game; repeated identical queries will yield identical answers. The structure of network G is sufficient to distinguish individual stations. By comparing and analyzing the observable adjacent stations across multiple terminals, you can deduce the mapping relationship and determine the true connections of the target station.

When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Set Read Query (e.g., querying terminal 3):
<query_set>3</query_set>

- Membership Query (e.g., asking if station 5 is in the observable adjacent stations of terminal 2):
<query_member>2,5</query_member>

- Intersection Count Query (e.g., asking for the intersection size of observable adjacent stations of terminals 1 and 4):
<query_intersect>1,4</query_intersect>

When submitting the final answer, list all adjacent station IDs of target station T in the true network G (comma-separated, order does not matter), using this format:

<answer>1,3,5</answer>

If the target station has no adjacent stations, submit an empty set:

<answer></answer>
"""

    contextualized_rule_zh_2 = """\
我们来进行一项“流行病接触者追踪”分析。

某社区有编号 1 到 {n} 的个体集合 V，他们之间存在一个未知的真实密切接触网络 G。由于档案系统数据损坏，发生了一次未知的档案错乱映射 M，导致调取编号为 v 的档案时，实际显示的是个体 M(v) 的接触记录。

定义档案 v 的可观测接触者集合 F(v) 为：个体 M(v) 在真实接触网络 G 中的直接接触者集合（不含 M(v) 本人）。

你的目标是：推断出目标个体 T = {target} 在真实网络 G 中的所有密切接触者。

你可以进行以下三种流调查询（每次仅限一个问题），我会根据真实设定如实回答：

1. 集合读取查询：调取档案 a 的可观测接触者，返回 F(a) 的完整集合。
2. 成员判定查询：询问个体 b 是否存在于档案 a 的可观测接触者 F(a) 中，返回“是”或“否”。
3. 交集计数查询：询问档案 a 和档案 b 的可观测接触者集合 F(a) 与 F(b) 共同包含的个体数量，返回一个非负整数。

注意：接触网络 G 和错乱映射 M 固定不变，重复相同的查询将得到相同的答案。你需要通过分析不同档案暴露出的接触群体结构指纹，破解错乱映射，从而找到目标个体的真实接触者。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 集合读取查询（例如查询档案 3）：
<query_set>3</query_set>

- 成员判定查询（例如询问个体 5 是否在档案 2 的可观测接触者中）：
<query_member>2,5</query_member>

- 交集计数查询（例如询问档案 1 和档案 4 的可观测接触者交集大小）：
<query_intersect>1,4</query_intersect>

提交最终答案时，列出目标个体 T 在真实网络 G 中的所有密切接触者编号（用逗号隔开，顺序不限），格式如下：

<answer>1,3,5</answer>

如果目标个体没有密切接触者，提交空集：

<answer></answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct an "Epidemiological Contact Tracing" analysis.

There is a set V of individuals numbered 1 to {n} in a community, with an unknown true close-contact network G among them. Due to data corruption in the records system, an unknown file scramble mapping M occurred, causing the file labeled v to actually display the contact records of individual M(v).

Define the observable contact set F(v) for file v as: the true close contacts of individual M(v) in network G (excluding M(v) itself).

Your goal is to infer all true close contacts of the target individual T = {target} in the real network G.

You can perform the following three types of epidemiological queries (one per turn), and I will answer truthfully based on the true setting:

1. Set Read Query: Retrieve the observable contacts of file a, returns the complete set F(a).
2. Membership Query: Ask if individual b exists in the observable contacts F(a) of file a, returns "Yes" or "No".
3. Intersection Count Query: Ask for the number of common individuals between F(a) and F(b) of files a and b, returns a non-negative integer.

Note: Network G and mapping M remain fixed throughout the game; repeated identical queries will yield identical answers. You must deduce the scramble mapping by analyzing the contact structures exposed in different files to identify the true contacts of the target individual.

When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Set Read Query (e.g., querying file 3):
<query_set>3</query_set>

- Membership Query (e.g., asking if individual 5 is in the observable contacts of file 2):
<query_member>2,5</query_member>

- Intersection Count Query (e.g., asking for the intersection size of observable contacts of files 1 and 4):
<query_intersect>1,4</query_intersect>

When submitting the final answer, list all close contact IDs of target individual T in the true network G (comma-separated, order does not matter), using this format:

<answer>1,3,5</answer>

If the target individual has no close contacts, submit an empty set:

<answer></answer>
"""

    contextualized_rule_zh_3 = """\
我们来处理一个“学习互助小组网络重建”任务。

班级里有编号 1 到 {n} 的学生集合 V，存在一个未知的真实课后互助网络 G。由于在线学习平台数据库索引错误，学生的账号登录产生了一个未知的错位映射 M，导致用账号 v 登录后，系统显示的实际上是学生 M(v) 的互助伙伴名单。

定义账号 v 的可观测伙伴集合 F(v) 为：学生 M(v) 在真实互助网络 G 中的学习伙伴集合（不含 M(v) 自身）。

你的任务是：推断出目标学生 T = {target} 在真实互助网络 G 中的所有学习伙伴。

你可以向系统发起以下三种查询（每次仅限一个问题），我会根据真实设定如实回答：

1. 集合读取查询：查询账号 a 的可观测伙伴名单，返回 F(a) 的完整集合。
2. 成员判定查询：询问学生 b 是否在账号 a 的可观测伙伴名单 F(a) 中，返回“是”或“否”。
3. 交集计数查询：询问账号 a 和账号 b 的可观测伙伴名单 F(a) 与 F(b) 的重合人数，返回一个非负整数。

注意：互助网络 G 和错位映射 M 固定不变，重复相同的查询将得到相同的答案。通过交叉验证不同账号展示的伙伴结构特征，推导出真实的账号对应关系，从而还原目标学生的真实伙伴。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 集合读取查询（例如查询账号 3）：
<query_set>3</query_set>

- 成员判定查询（例如询问学生 5 是否在账号 2 的可观测伙伴名单中）：
<query_member>2,5</query_member>

- 交集计数查询（例如询问账号 1 和账号 4 的可观测伙伴交集大小）：
<query_intersect>1,4</query_intersect>

提交最终答案时，列出目标学生 T 在真实互助网络 G 中的所有学习伙伴编号（用逗号隔开，顺序不限），格式如下：

<answer>1,3,5</answer>

如果目标学生没有学习伙伴，提交空集：

<answer></answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's process a "Study Group Network Reconstruction" task.

There is a set V of students numbered 1 to {n} in a class, sharing an unknown true after-school study network G. Due to an index error in the online learning platform's database, an unknown account login mapping M occurred. Consequently, logging in with account v actually displays the study partners of student M(v).

Define the observable partner set F(v) for account v as: the study partners of student M(v) in the true network G (excluding M(v) itself).

Your task is to infer all true study partners of the target student T = {target} in the real network G.

You can query the system with the following three methods (one per turn), and I will answer truthfully based on the true setting:

1. Set Read Query: Query the observable partner list of account a, returns the complete set F(a).
2. Membership Query: Ask whether student b is in the observable partner list F(a) of account a, returns "Yes" or "No".
3. Intersection Count Query: Ask for the number of overlapping students between F(a) and F(b) of accounts a and b, returns a non-negative integer.

Note: Network G and mapping M remain fixed throughout the game; repeated identical queries will yield identical answers. By cross-referencing partner lists across different accounts, deduce the true account ownership mapping to restore the target student's real partners.

When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Set Read Query (e.g., querying account 3):
<query_set>3</query_set>

- Membership Query (e.g., asking if student 5 is in the observable partner list of account 2):
<query_member>2,5</query_member>

- Intersection Count Query (e.g., asking for the intersection size of observable partner lists of accounts 1 and 4):
<query_intersect>1,4</query_intersect>

When submitting the final answer, list all study partner IDs of target student T in the true network G (comma-separated, order does not matter), using this format:

<answer>1,3,5</answer>

If the target student has no study partners, submit an empty set:

<answer></answer>
"""

    contextualized_rule_zh_4 = """\
我们来执行一次“工业传感器拓扑校验”任务。

智能车间内有编号 1 到 {n} 的传感器集合 V，它们之间存在一个未知的真实物理依赖拓扑 G。由于接线面板标签贴错，产生了一个未知的端口映射 M，使得在测试端口 v 时，读取到的实际上是传感器 M(v) 的依赖数据。

定义端口 v 的可观测邻接传感器集合 F(v) 为：传感器 M(v) 在真实拓扑 G 中的相邻传感器集合（不含 M(v) 自身）。

你的目标是：推断出目标传感器 T = {target} 在真实拓扑 G 中的所有相邻传感器。

你可以使用测试仪进行以下三种诊断查询（每次仅限一个问题），我会根据真实设定如实回答：

1. 集合读取查询：读取端口 a 的可观测邻接传感器，返回 F(a) 的完整集合。
2. 成员判定查询：询问传感器 b 是否存在于端口 a 的可观测邻接集合 F(a) 中，返回“是”或“否”。
3. 交集计数查询：询问端口 a 和端口 b 的可观测邻接集合 F(a) 与 F(b) 的共用传感器数量，返回一个非负整数。

注意：拓扑 G 和端口映射 M 固定不变，重复相同的查询将得到相同的答案。依靠不同端口返回的拓扑指纹差异，反向推导接线映射，最终确定目标传感器的真实邻接关系。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 集合读取查询（例如读取端口 3）：
<query_set>3</query_set>

- 成员判定查询（例如询问传感器 5 是否在端口 2 的可观测邻接集合中）：
<query_member>2,5</query_member>

- 交集计数查询（例如询问端口 1 和端口 4 的可观测邻接集合交集大小）：
<query_intersect>1,4</query_intersect>

提交最终答案时，列出目标传感器 T 在真实拓扑 G 中的所有相邻传感器编号（用逗号隔开，顺序不限），格式如下：

<answer>1,3,5</answer>

如果目标传感器没有相邻传感器，提交空集：

<answer></answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's execute an "Industrial Sensor Topology Verification" task.

In a smart workshop, there is a set V of sensors numbered 1 to {n}, with an unknown true physical dependency topology G among them. Due to mislabeled patch panels, an unknown port mapping M was created, causing tests on port v to actually read the dependency data of sensor M(v).

Define the observable adjacent sensor set F(v) for port v as: the neighboring sensors of M(v) in the true topology G (excluding M(v) itself).

Your goal is to infer all true neighboring sensors of the target sensor T = {target} in the true topology G.

You can use the diagnostic tester to perform three types of queries (one per turn), and I will answer truthfully based on the true setting:

1. Set Read Query: Read the observable adjacent sensors of port a, returns the complete set F(a).
2. Membership Query: Ask if sensor b exists in the observable adjacent set F(a) of port a, returns "Yes" or "No".
3. Intersection Count Query: Ask for the number of shared sensors between F(a) and F(b) of ports a and b, returns a non-negative integer.

Note: Topology G and port mapping M remain fixed throughout the game; repeated identical queries will yield identical answers. Relying on the differences in topology fingerprints returned by various ports, reverse-engineer the wiring mapping to ultimately determine the target sensor's true adjacent relations.

When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Set Read Query (e.g., querying port 3):
<query_set>3</query_set>

- Membership Query (e.g., asking if sensor 5 is in the observable adjacent set of port 2):
<query_member>2,5</query_member>

- Intersection Count Query (e.g., asking for the intersection size of observable adjacent sets of ports 1 and 4):
<query_intersect>1,4</query_intersect>

When submitting the final answer, list all adjacent sensor IDs of target sensor T in the true topology G (comma-separated, order does not matter), using this format:

<answer>1,3,5</answer>

If the target sensor has no adjacent sensors, submit an empty set:

<answer></answer>
"""

    contextualized_rule_zh_5 = """\
我们来展开一场“空壳公司资金网络审计”行动。

离岸金融中心有编号 1 到 {n} 的账户集合 V，它们之间构成了未知的真实资金往来网络 G。洗钱组织建立了一个未知的代理掩护映射 M，当你对审查目标 v 发起审计时，系统实际返回的是代理账户 M(v) 的交易记录。

定义审查目标 v 的可观测交易对手集合 F(v) 为：账户 M(v) 在真实资金网络 G 中的交易对手集合（不含 M(v) 自身）。

你的目标是：查明目标账户 T = {target} 在真实资金网络 G 中的所有实际交易对手。

你可以向金融监管数据库提交以下三种问询（每次仅限一个问题），我会根据真实设定如实回答：

1. 集合读取查询：提取审查目标 a 的可观测交易对手名单，返回 F(a) 的完整集合。
2. 成员判定查询：询问账户 b 是否出现在审查目标 a 的可观测交易对手 F(a) 中，返回“是”或“否”。
3. 交集计数查询：询问审查目标 a 和审查目标 b 的可观测交易对手集合 F(a) 与 F(b) 的重合账户数量，返回一个非负整数。

注意：资金网络 G 和代理映射 M 期间内保持固定，重复相同的查询将得到相同的答案。借助多个审查目标暴露的交易网络特征，穿透代理映射迷雾，准确锁定目标账户的真实交易网络。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 集合读取查询（例如查询审查目标 3）：
<query_set>3</query_set>

- 成员判定查询（例如询问账户 5 是否在审查目标 2 的可观测交易对手中）：
<query_member>2,5</query_member>

- 交集计数查询（例如询问审查目标 1 和审查目标 4 的可观测交易对手交集大小）：
<query_intersect>1,4</query_intersect>

提交最终答案时，列出目标账户 T 在真实资金网络 G 中的所有实际交易对手编号（用逗号隔开，顺序不限），格式如下：

<answer>1,3,5</answer>

如果目标账户没有实际交易对手，提交空集：

<answer></answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's launch a "Shell Company Fund Network Audit" operation.

In an offshore financial center, there is a set V of accounts numbered 1 to {n}, forming an unknown true fund transfer network G. A money laundering syndicate has established an unknown proxy smokescreen mapping M. When you initiate an audit on target v, the system actually returns the transaction records of proxy account M(v).

Define the observable counterparty set F(v) for audit target v as: the transaction counterparties of account M(v) in the true fund network G (excluding M(v) itself).

Your goal is to identify all true transaction counterparties of the target account T = {target} in the real fund network G.

You can submit three types of inquiries to the financial regulatory database (one per turn), and I will answer truthfully based on the true setting:

1. Set Read Query: Extract the observable counterparty list of audit target a, returns the complete set F(a).
2. Membership Query: Ask whether account b appears in the observable counterparty list F(a) of audit target a, returns "Yes" or "No".
3. Intersection Count Query: Ask for the number of overlapping accounts between F(a) and F(b) of audit targets a and b, returns a non-negative integer.

Note: Fund network G and proxy mapping M remain fixed throughout the game; repeated identical queries will yield identical answers. By leveraging transaction patterns exposed by multiple audit targets, pierce through the proxy mapping fog to accurately pinpoint the true transaction network of the target account.

When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Set Read Query (e.g., querying audit target 3):
<query_set>3</query_set>

- Membership Query (e.g., asking if account 5 is in the observable counterparties of audit target 2):
<query_member>2,5</query_member>

- Intersection Count Query (e.g., asking for the intersection size of observable counterparties of audit targets 1 and 4):
<query_intersect>1,4</query_intersect>

When submitting the final answer, list all actual counterparty IDs of target account T in the true fund network G (comma-separated, order does not matter), using this format:

<answer>1,3,5</answer>

If the target account has no counterparties, submit an empty set:

<answer></answer>
"""

    tags = ["answer", "query_set", "query_member", "query_intersect"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "target": 2,
                "graph": {1: [2], 2: [1, 3], 3: [2, 4], 4: [3]},
                "permutation": {1: 3, 2: 1, 3: 4, 4: 2}
            },
            2: {
                "n": 5,
                "target": 1,
                "graph": {1: [2, 3, 4, 5], 2: [1], 3: [1], 4: [1], 5: [1]},
                "permutation": {1: 2, 2: 1, 3: 5, 4: 3, 5: 4}
            },
            3: {
                "n": 6,
                "target": 3,
                "graph": {1: [2, 6], 2: [1, 3], 3: [2, 4], 4: [3, 5], 5: [4, 6], 6: [5, 1]},
                "permutation": {1: 4, 2: 5, 3: 1, 4: 6, 5: 2, 6: 3}
            },
            4: {
                "n": 7,
                "target": 4,
                "graph": {
                    1: [2, 3, 4], 2: [1, 3], 3: [1, 2, 5], 4: [1, 6, 7],
                    5: [3, 6], 6: [4, 5, 7], 7: [4, 6]
                },
                "permutation": {1: 5, 2: 7, 3: 2, 4: 3, 5: 1, 6: 4, 7: 6}
            },
            5: {
                "n": 8,
                "target": 5,
                "graph": {
                    1: [2, 4, 5], 2: [1, 3, 6], 3: [2, 4, 7], 4: [1, 3, 8],
                    5: [1, 6, 8], 6: [2, 5, 7], 7: [3, 6, 8], 8: [4, 5, 7]
                },
                "permutation": {1: 6, 2: 3, 3: 8, 4: 2, 5: 7, 6: 1, 7: 4, 8: 5}
            },
        },
        "en": {
            1: {
                "n": 4,
                "target": 2,
                "graph": {1: [2], 2: [1, 3], 3: [2, 4], 4: [3]},
                "permutation": {1: 3, 2: 1, 3: 4, 4: 2}
            },
            2: {
                "n": 5,
                "target": 1,
                "graph": {1: [2, 3, 4, 5], 2: [1], 3: [1], 4: [1], 5: [1]},
                "permutation": {1: 2, 2: 1, 3: 5, 4: 3, 5: 4}
            },
            3: {
                "n": 6,
                "target": 3,
                "graph": {1: [2, 6], 2: [1, 3], 3: [2, 4], 4: [3, 5], 5: [4, 6], 6: [5, 1]},
                "permutation": {1: 4, 2: 5, 3: 1, 4: 6, 5: 2, 6: 3}
            },
            4: {
                "n": 7,
                "target": 4,
                "graph": {
                    1: [2, 3, 4], 2: [1, 3], 3: [1, 2, 5], 4: [1, 6, 7],
                    5: [3, 6], 6: [4, 5, 7], 7: [4, 6]
                },
                "permutation": {1: 5, 2: 7, 3: 2, 4: 3, 5: 1, 6: 4, 7: 6}
            },
            5: {
                "n": 8,
                "target": 5,
                "graph": {
                    1: [2, 4, 5], 2: [1, 3, 6], 3: [2, 4, 7], 4: [1, 3, 8],
                    5: [1, 6, 8], 6: [2, 5, 7], 7: [3, 6, 8], 8: [4, 5, 7]
                },
                "permutation": {1: 6, 2: 3, 3: 8, 4: 2, 5: 7, 6: 1, 7: 4, 8: 5}
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
        self._game_info["n"] = cfg["n"]
        self._game_info["target"] = cfg["target"]
        
        self.graph = cfg["graph"]
        self.permutation = cfg["permutation"]
        self.target_node = cfg["target"]
        self.correct_neighbors = set(self.graph.get(self.target_node, []))

    def _compute_observable_neighborhood(self, query_node):
        real_node = self.permutation[query_node]
        return set(self.graph.get(real_node, []))

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        if not raw_ans:
            model_neighbors = set()
        else:
            try:
                model_neighbors = set(int(x.strip()) for x in raw_ans.split(",") if x.strip())
            except:
                return False
        
        return model_neighbors == self.correct_neighbors

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        n = self._game_info["n"]
        
        is_zh = self.config.language == "zh"
        yes_res = "是" if is_zh else "Yes"
        no_res = "否" if is_zh else "No"
        
        for i in range(1, n + 1):
            query_tag = f"<query_set>{i}</query_set>"
            obs = self._compute_observable_neighborhood(i)
            if not obs:
                ans = "{}"
            else:
                ans = "{" + ",".join(map(str, sorted(obs))) + "}"
            results.append({"query": query_tag, "answer": ans})
            
        for a in range(1, n + 1):
            for b in range(1, n + 1):
                query_tag = f"<query_member>{a},{b}</query_member>"
                obs_a = self._compute_observable_neighborhood(a)
                ans = yes_res if b in obs_a else no_res
                results.append({"query": query_tag, "answer": ans})
        
        for a in range(1, n + 1):
            for b in range(a, n + 1):
                query_tag = f"<query_intersect>{a},{b}</query_intersect>"
                obs_a = self._compute_observable_neighborhood(a)
                obs_b = self._compute_observable_neighborhood(b)
                ans = str(len(obs_a & obs_b))
                results.append({"query": query_tag, "answer": ans})
                
        return results

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：格式无效或节点编号超出范围。"
            error_outofrange = "错误：节点编号超出范围。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid format or node ID out of range."
            error_outofrange = "Error: Node ID out of range."

        if "query_set" in parsed_info:
            try:
                node = int(parsed_info["query_set"].strip())
                if node < 1 or node > self._game_info["n"]:
                    return error_outofrange
                
                obs_neighborhood = self._compute_observable_neighborhood(node)
                if not obs_neighborhood:
                    return "{}" if self.config.language == "en" else "{}"
                
                return "{" + ",".join(map(str, sorted(obs_neighborhood))) + "}"
            except:
                return error_format

        elif "query_member" in parsed_info:
            try:
                raw = parsed_info["query_member"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                
                node_a, node_b = int(parts[0]), int(parts[1])
                if node_a < 1 or node_a > self._game_info["n"] or \
                   node_b < 1 or node_b > self._game_info["n"]:
                    return error_outofrange
                
                obs_neighborhood = self._compute_observable_neighborhood(node_a)
                return yes_res if node_b in obs_neighborhood else no_res
            except:
                return error_format

        elif "query_intersect" in parsed_info:
            try:
                raw = parsed_info["query_intersect"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                
                node_a, node_b = int(parts[0]), int(parts[1])
                if node_a < 1 or node_a > self._game_info["n"] or \
                   node_b < 1 or node_b > self._game_info["n"]:
                    return error_outofrange
                
                obs_a = self._compute_observable_neighborhood(node_a)
                obs_b = self._compute_observable_neighborhood(node_b)
                intersection_size = len(obs_a & obs_b)
                return str(intersection_size)
            except:
                return error_format
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct.lstrip('-').isdigit():
            val = int(correct)
            return str(val + 1)
        
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            elif correct == "否":
                return "是"
        else:
            if correct.lower() == "yes":
                if correct == "Yes": return "No"
                if correct == "YES": return "NO"
                return "no"
            if correct.lower() == "no":
                if correct == "No": return "Yes"
                if correct == "NO": return "YES"
                return "yes"
        
        if correct.startswith("{") and correct.endswith("}"):
            inner = correct[1:-1].strip()
            if not inner:
                return "{1}"
            else:
                elements = [x.strip() for x in inner.split(",") if x.strip()]
                if len(elements) > 1:
                    return "{" + ",".join(elements[1:]) + "}"
                else:
                    return "{}"
        
        return correct + "_WRONG"