from .base import Game
import re

class GraphTransformGame(Game):

    game_rule_zh = """\
我们现在来玩一个"交互式图变换识别与安全对构造"游戏，规则如下：

有一个简单无向连通图，初始为一棵树，节点为 1 到 9，根为节点 1。

初始边集为：(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (6,8), (6,9)

树的结构信息（以1为根）：
- 父节点关系：pa(1)=1; pa(2)=1; pa(3)=1; pa(4)=2; pa(5)=2; pa(6)=3; pa(7)=3; pa(8)=6; pa(9)=6
- 深度关系：depth(1)=0; depth(2)=1; depth(3)=1; depth(4)=2; depth(5)=2; depth(6)=2; depth(7)=2; depth(8)=3; depth(9)=3

固定置换 p 的定义：p(1)=1; p(2)=3; p(3)=2; p(4)=5; p(5)=4; p(6)=7; p(7)=6; p(8)=9; p(9)=8

系统已秘密选择了一个改写函数 R，它有四种可能（B、C、D、E），具体定义如下：

- 函数 B：R(a,b) = (pa(a), pa(b))
- 函数 C：R(a,b) = (lca(a,b), b)，其中 lca 表示最近公共祖先
- 函数 D：R(a,b) = (g(a), g(b))，其中 g(x) = x（若 depth(x) 为偶数），g(x) = pa(x)（若 depth(x) 为奇数）
- 函数 E：R(a,b) = (p(a), p(b))，其中 p 为上述固定置换

当前边集初始为上述树边。当你提交一个查询 (a,b)（a 不等于 b）时：

1. 系统计算 (a', b') = R(a,b)
2. 如果 a' = b'（形成自环）或边 {{a', b'}} 已在当前边集中，系统反馈 0，不添加新边
3. 否则反馈 1，并将边 {{a', b'}} 加入当前边集

你可以进行以下三类操作：

1. 测试查询：询问"连接 a b"（a, b 为 1 到 9 之间的不同节点）
   - 系统反馈 0 或 1

2. 宣告猜测：提交你认为的改写函数类型（B、C、D 或 E）
   - 系统反馈"正确"或"错误"
   - 注意：必须先完成至少 2 次测试查询后才能宣告

3. 状态查询：
   - 询问剩余可触发反馈 1 的次数
   - 询问已完成的测试查询次数

- 全局至多允许 2 次反馈为 1 的情况；若出现第 3 次反馈 1，游戏失败
- 在正确宣告改写函数后，你需要连续提交 3 个测试查询，每个查询的 (a,b) 必须满足：
  * a 和 b 在初始树中不相邻
  * a 不等于 b
  * 每次反馈必须为 0

1. 通过测试查询推断出隐藏的改写函数类型
2. 正确宣告改写函数
3. 在宣告后连续 3 次提交满足条件的查询，且每次反馈均为 0

每次只能包含一个操作标签：

- 测试查询（例如查询节点 1 和 4）：
<query_test>1,4</query_test>

- 宣告猜测（例如猜测是函数 B）：
<query_guess>B</query_guess>

- 查询剩余可触发 1 的次数：
<query_remain></query_remain>

- 查询已完成的测试次数：
<query_count></query_count>

- 正确宣告改写函数类型
- 宣告后连续 3 次测试查询反馈均为 0
- 全程反馈 1 的总次数不超过 2
"""

    game_rule_en = """\
Let's play a "Graph Transform Identification and Safe Pair Construction" game. Here are the rules:

There is a simple undirected connected graph, initially a tree with nodes 1 to 9, rooted at node 1.

Initial edge set: (1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (6,8), (6,9)

Tree structure (rooted at 1):
- Parent relationship: pa(1)=1; pa(2)=1; pa(3)=1; pa(4)=2; pa(5)=2; pa(6)=3; pa(7)=3; pa(8)=6; pa(9)=6
- Depth relationship: depth(1)=0; depth(2)=1; depth(3)=1; depth(4)=2; depth(5)=2; depth(6)=2; depth(7)=2; depth(8)=3; depth(9)=3

Fixed permutation p: p(1)=1; p(2)=3; p(3)=2; p(4)=5; p(5)=4; p(6)=7; p(7)=6; p(8)=9; p(9)=8

The system has secretly selected a rewrite function R from four possibilities (B, C, D, E):

- Function B: R(a,b) = (pa(a), pa(b))
- Function C: R(a,b) = (lca(a,b), b), where lca is the lowest common ancestor
- Function D: R(a,b) = (g(a), g(b)), where g(x) = x (if depth(x) is even), g(x) = pa(x) (if depth(x) is odd)
- Function E: R(a,b) = (p(a), p(b)), where p is the fixed permutation above

The current edge set starts with the tree edges. When you submit a query (a,b) where a is not equal to b:

1. System computes (a', b') = R(a,b)
2. If a' = b' (forming a self-loop) or edge {{a', b'}} is already in the current edge set, system returns 0 and does not add a new edge
3. Otherwise returns 1 and adds edge {{a', b'}} to the current edge set

You can perform three types of operations:

1. Test Query: Ask "connect a b" (a, b are different nodes from 1 to 9)
   - System returns 0 or 1

2. Declare Guess: Submit your believed rewrite function type (B, C, D, or E)
   - System returns "Correct" or "Incorrect"
   - Note: Must complete at least 2 test queries before declaring

3. Status Query:
   - Ask for remaining count of feedback 1 allowed
   - Ask for completed test query count

- Maximum 2 feedbacks of 1 allowed globally; if a 3rd feedback of 1 occurs, game fails
- After correctly declaring the rewrite function, you need to submit 3 consecutive test queries, each (a,b) must satisfy:
  * a and b are not adjacent in the initial tree
  * a is not equal to b
  * Each feedback must be 0

1. Infer the hidden rewrite function type through test queries
2. Correctly declare the rewrite function
3. After declaration, submit 3 consecutive queries meeting the conditions with feedback 0 each time

Each turn must contain only one operation tag:

- Test Query (e.g., querying nodes 1 and 4):
<query_test>1,4</query_test>

- Declare Guess (e.g., guessing function B):
<query_guess>B</query_guess>

- Query remaining feedback 1 count:
<query_remain></query_remain>

- Query completed test count:
<query_count></query_count>

- Correctly declare the rewrite function type
- After declaration, 3 consecutive test queries all return 0
- Total feedback 1 count does not exceed 2 throughout the game
"""

    contextualized_rule_zh_1 = """\
[交通场景] 我们现在来使用"智能交通网络改造与安全扩展评估系统"，规则如下：

有一个连通的交通网络，初始为一棵默认干线树，包含交通枢纽 1 到 9，国家级总枢纽为节点 1。

初始路线集（现有干线）：(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (6,8), (6,9)

交通网络的结构信息（以总枢纽 1 为根）：
- 上级汇聚枢纽关系：pa(1)=1; pa(2)=1; pa(3)=1; pa(4)=2; pa(5)=2; pa(6)=3; pa(7)=3; pa(8)=6; pa(9)=6
- 枢纽级别（深度）：depth(1)=0; depth(2)=1; depth(3)=1; depth(4)=2; depth(5)=2; depth(6)=2; depth(7)=2; depth(8)=3; depth(9)=3

互备枢纽映射 p 的定义：p(1)=1; p(2)=3; p(3)=2; p(4)=5; p(5)=4; p(6)=7; p(7)=6; p(8)=9; p(9)=8

系统秘密选择了一种调度策略 R，它有四种可能（B、C、D、E），具体定义如下：

- 策略 B：R(a,b) = (pa(a), pa(b))
- 策略 C：R(a,b) = (lca(a,b), b)，其中 lca 表示最近共同中转枢纽
- 策略 D：R(a,b) = (g(a), g(b))，其中 g(x) = x（若 depth(x) 为偶数），g(x) = pa(x)（若 depth(x) 为奇数）
- 策略 E：R(a,b) = (p(a), p(b))，其中 p 为上述互备映射

当前路线集初始为上述干线树。当你提交一个规划请求 (a,b)（a 不等于 b）时：

1. 系统计算受策略影响的实际需求 (a', b') = R(a,b)
2. 如果 a' = b'（形成内部循环）或直达路线 {{a', b'}} 已在当前路线集中，系统反馈 0，表示无需新建路线
3. 否则反馈 1，表示批准新建，并将路线 {{a', b'}} 加入当前路线集

你可以进行以下三类操作：

1. 测试查询：询问"连接 a b"（a, b 为 1 到 9 之间的不同枢纽）
   - 系统反馈 0 或 1

2. 宣告猜测：提交你认为的调度策略类型（B、C、D 或 E）
   - 系统反馈"正确"或"错误"
   - 注意：必须先完成至少 2 次测试查询后才能宣告

3. 状态查询：
   - 询问剩余可触发新建路线（反馈 1）的次数
   - 询问已完成的测试查询次数

- 全局至多允许 2 次反馈为 1 的情况；若出现第 3 次反馈 1，评估失败
- 在正确宣告调度策略后，你需要连续提交 3 个测试查询，每个查询的 (a,b) 必须满足：
  * a 和 b 在初始干线树中不相邻
  * a 不等于 b
  * 每次反馈必须为 0

1. 通过测试查询推断出隐藏的调度策略类型
2. 正确宣告该调度策略
3. 在宣告后连续 3 次提交满足条件的查询，且每次反馈均为 0

每次只能包含一个操作标签：

- 测试查询（例如查询枢纽 1 和 4）：
<query_test>1,4</query_test>

- 宣告猜测（例如猜测是策略 B）：
<query_guess>B</query_guess>

- 查询剩余可触发 1 的次数：
<query_remain></query_remain>

- 查询已完成的测试次数：
<query_count></query_count>

- 正确宣告调度策略类型
- 宣告后连续 3 次测试查询反馈均为 0
- 全程反馈 1 的总次数不超过 2
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario] Let's use the "Intelligent Transport Network Transformation and Safety Expansion System". Here are the rules:

There is a connected transport network, initially a default arterial tree, containing hubs 1 to 9, with the national central hub at node 1.

Initial route set (existing arterials): (1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (6,8), (6,9)

Network structure (rooted at hub 1):
- Superior convergent hub relationship: pa(1)=1; pa(2)=1; pa(3)=1; pa(4)=2; pa(5)=2; pa(6)=3; pa(7)=3; pa(8)=6; pa(9)=6
- Hub level (depth): depth(1)=0; depth(2)=1; depth(3)=1; depth(4)=2; depth(5)=2; depth(6)=2; depth(7)=2; depth(8)=3; depth(9)=3

Strategic backup hub mapping p: p(1)=1; p(2)=3; p(3)=2; p(4)=5; p(5)=4; p(6)=7; p(7)=6; p(8)=9; p(9)=8

The system has secretly selected a dispatch strategy R from four possibilities (B, C, D, E):

- Strategy B: R(a,b) = (pa(a), pa(b))
- Strategy C: R(a,b) = (lca(a,b), b), where lca is the lowest common transfer hub
- Strategy D: R(a,b) = (g(a), g(b)), where g(x) = x (if depth(x) is even), g(x) = pa(x) (if depth(x) is odd)
- Strategy E: R(a,b) = (p(a), p(b)), where p is the strategic backup mapping above

The current route set starts with the arterial tree. When you submit a route planning query (a,b) where a is not equal to b:

1. System computes the actual requirement (a', b') = R(a,b)
2. If a' = b' (forming an internal loop) or the direct route {{a', b'}} is already in the current route set, system returns 0, meaning no new route is needed.
3. Otherwise returns 1 and adds the route {{a', b'}} to the current route set.

You can perform three types of operations:

1. Test Query: Ask "connect a b" (a, b are different hubs from 1 to 9)
   - System returns 0 or 1

2. Declare Guess: Submit your believed strategy type (B, C, D, or E)
   - System returns "Correct" or "Incorrect"
   - Note: Must complete at least 2 test queries before declaring

3. Status Query:
   - Ask for remaining count of feedback 1 allowed
   - Ask for completed test query count

- Maximum 2 feedbacks of 1 allowed globally; if a 3rd feedback of 1 occurs, the evaluation fails
- After correctly declaring the strategy, you need to submit 3 consecutive test queries, each (a,b) must satisfy:
  * a and b are not adjacent in the initial arterial tree
  * a is not equal to b
  * Each feedback must be 0

1. Infer the hidden strategy type through test queries
2. Correctly declare the strategy
3. After declaration, submit 3 consecutive queries meeting the conditions with feedback 0 each time

Each turn must contain only one operation tag:

- Test Query (e.g., querying hubs 1 and 4):
<query_test>1,4</query_test>

- Declare Guess (e.g., guessing strategy B):
<query_guess>B</query_guess>

- Query remaining feedback 1 count:
<query_remain></query_remain>

- Query completed test count:
<query_count></query_count>

- Correctly declare the strategy type
- After declaration, 3 consecutive test queries all return 0
- Total feedback 1 count does not exceed 2 throughout the task
"""

    contextualized_rule_zh_2 = """\
[医疗场景] 我们现在来使用"跨级医疗转诊与安全通道构建系统"，规则如下：

有一个连通的医疗网络，初始为一棵常规逐级转诊树，包含医疗机构 1 到 9，国家中心医院为节点 1。

初始转诊通道集（现有网络）：(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (6,8), (6,9)

网络结构信息（以中心医院 1 为根）：
- 上级指导医院关系：pa(1)=1; pa(2)=1; pa(3)=1; pa(4)=2; pa(5)=2; pa(6)=3; pa(7)=3; pa(8)=6; pa(9)=6
- 医院级别（深度）：depth(1)=0; depth(2)=1; depth(3)=1; depth(4)=2; depth(5)=2; depth(6)=2; depth(7)=2; depth(8)=3; depth(9)=3

专科帮扶映射 p 的定义：p(1)=1; p(2)=3; p(3)=2; p(4)=5; p(5)=4; p(6)=7; p(7)=6; p(8)=9; p(9)=8

系统秘密选择了一种跨级转诊分配算法 R，它有四种可能（B、C、D、E），具体定义如下：

- 算法 B：R(a,b) = (pa(a), pa(b))
- 算法 C：R(a,b) = (lca(a,b), b)，其中 lca 表示最近共同上级医院
- 算法 D：R(a,b) = (g(a), g(b))，其中 g(x) = x（若 depth(x) 为偶数），g(x) = pa(x)（若 depth(x) 为奇数）
- 算法 E：R(a,b) = (p(a), p(b))，其中 p 为上述专科帮扶映射

当前转诊通道集初始为上述转诊树。当你提交一个转诊查询 (a,b)（a 不等于 b）时：

1. 系统计算受算法影响的实际接收方 (a', b') = R(a,b)
2. 如果 a' = b'（机构内流转）或通道 {{a', b'}} 已在当前网络中，系统反馈 0，表示无需新建通道
3. 否则反馈 1，表示建立紧急转诊通道，并将通道 {{a', b'}} 加入当前网络

你可以进行以下三类操作：

1. 测试查询：询问"连接 a b"（a, b 为 1 到 9 之间的不同医疗机构）
   - 系统反馈 0 或 1

2. 宣告猜测：提交你认为的转诊算法类型（B、C、D 或 E）
   - 系统反馈"正确"或"错误"
   - 注意：必须先完成至少 2 次测试查询后才能宣告

3. 状态查询：
   - 询问剩余可触发新建通道（反馈 1）的次数
   - 询问已完成的测试查询次数

- 全局至多允许 2 次反馈为 1 的情况；若出现第 3 次反馈 1，任务失败
- 在正确宣告转诊算法后，你需要连续提交 3 个测试查询，每个查询的 (a,b) 必须满足：
  * a 和 b 在初始转诊树中不相邻
  * a 不等于 b
  * 每次反馈必须为 0

1. 通过测试查询推断出隐藏的转诊算法类型
2. 正确宣告该转诊算法
3. 在宣告后连续 3 次提交满足条件的查询，且每次反馈均为 0

每次只能包含一个操作标签：

- 测试查询（例如查询机构 1 和 4）：
<query_test>1,4</query_test>

- 宣告猜测（例如猜测是算法 B）：
<query_guess>B</query_guess>

- 查询剩余可触发 1 的次数：
<query_remain></query_remain>

- 查询已完成的测试次数：
<query_count></query_count>

- 正确宣告转诊算法类型
- 宣告后连续 3 次测试查询反馈均为 0
- 全程反馈 1 的总次数不超过 2
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario] Let's use the "Cross-level Medical Referral and Safety Channel Construction System". Here are the rules:

There is a connected healthcare network, initially a conventional hierarchical referral tree, containing medical institutions 1 to 9, with the national central hospital at node 1.

Initial referral channel set (existing network): (1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (6,8), (6,9)

Network structure (rooted at central hospital 1):
- Superior guiding hospital relationship: pa(1)=1; pa(2)=1; pa(3)=1; pa(4)=2; pa(5)=2; pa(6)=3; pa(7)=3; pa(8)=6; pa(9)=6
- Hospital level (depth): depth(1)=0; depth(2)=1; depth(3)=1; depth(4)=2; depth(5)=2; depth(6)=2; depth(7)=2; depth(8)=3; depth(9)=3

Specialty support mapping p: p(1)=1; p(2)=3; p(3)=2; p(4)=5; p(5)=4; p(6)=7; p(7)=6; p(8)=9; p(9)=8

The system has secretly selected a cross-level referral allocation algorithm R from four possibilities (B, C, D, E):

- Algorithm B: R(a,b) = (pa(a), pa(b))
- Algorithm C: R(a,b) = (lca(a,b), b), where lca is the lowest common superior hospital
- Algorithm D: R(a,b) = (g(a), g(b)), where g(x) = x (if depth(x) is even), g(x) = pa(x) (if depth(x) is odd)
- Algorithm E: R(a,b) = (p(a), p(b)), where p is the specialty support mapping above

The current referral channel set starts with the conventional referral tree. When you submit a referral query (a,b) where a is not equal to b:

1. System computes the actual receiver (a', b') = R(a,b)
2. If a' = b' (intra-institution routing) or the channel {{a', b'}} is already in the current network, system returns 0, meaning no new channel is needed.
3. Otherwise returns 1 and adds the emergency channel {{a', b'}} to the current network.

You can perform three types of operations:

1. Test Query: Ask "connect a b" (a, b are different institutions from 1 to 9)
   - System returns 0 or 1

2. Declare Guess: Submit your believed referral algorithm type (B, C, D, or E)
   - System returns "Correct" or "Incorrect"
   - Note: Must complete at least 2 test queries before declaring

3. Status Query:
   - Ask for remaining count of feedback 1 allowed
   - Ask for completed test query count

- Maximum 2 feedbacks of 1 allowed globally; if a 3rd feedback of 1 occurs, the task fails
- After correctly declaring the algorithm, you need to submit 3 consecutive test queries, each (a,b) must satisfy:
  * a and b are not adjacent in the initial referral tree
  * a is not equal to b
  * Each feedback must be 0

1. Infer the hidden referral algorithm type through test queries
2. Correctly declare the referral algorithm
3. After declaration, submit 3 consecutive queries meeting the conditions with feedback 0 each time

Each turn must contain only one operation tag:

- Test Query (e.g., querying institutions 1 and 4):
<query_test>1,4</query_test>

- Declare Guess (e.g., guessing algorithm B):
<query_guess>B</query_guess>

- Query remaining feedback 1 count:
<query_remain></query_remain>

- Query completed test count:
<query_count></query_count>

- Correctly declare the referral algorithm type
- After declaration, 3 consecutive test queries all return 0
- Total feedback 1 count does not exceed 2 throughout the task
"""

    contextualized_rule_zh_3 = """\
[教育场景] 我们现在来使用"跨学科知识图谱联结与教学路径探索系统"，规则如下：

有一个连通的知识网络，初始为一棵学科前置依赖树，包含知识模块 1 到 9，核心基础理论为节点 1。

初始知识关联集（现有依赖）：(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (6,8), (6,9)

网络结构信息（以基础理论 1 为根）：
- 直接先导模块关系：pa(1)=1; pa(2)=1; pa(3)=1; pa(4)=2; pa(5)=2; pa(6)=3; pa(7)=3; pa(8)=6; pa(9)=6
- 知识进阶深度：depth(1)=0; depth(2)=1; depth(3)=1; depth(4)=2; depth(5)=2; depth(6)=2; depth(7)=2; depth(8)=3; depth(9)=3

跨领域类比映射 p 的定义：p(1)=1; p(2)=3; p(3)=2; p(4)=5; p(5)=4; p(6)=7; p(7)=6; p(8)=9; p(9)=8

系统秘密选择了一种认知关联规则 R，它有四种可能（B、C、D、E），具体定义如下：

- 规则 B：R(a,b) = (pa(a), pa(b))
- 规则 C：R(a,b) = (lca(a,b), b)，其中 lca 表示两者的最近共同先导模块
- 规则 D：R(a,b) = (g(a), g(b))，其中 g(x) = x（若 depth(x) 为偶数），g(x) = pa(x)（若 depth(x) 为奇数）
- 规则 E：R(a,b) = (p(a), p(b))，其中 p 为上述类比映射

当前知识关联集初始为上述依赖树。当你提交一个关联查询 (a,b)（a 不等于 b）时：

1. 系统计算受规则影响的实际关联点 (a', b') = R(a,b)
2. 如果 a' = b'（自身闭环）或桥梁 {{a', b'}} 已在当前网络中，系统反馈 0，表示桥梁已存在或无需新建
3. 否则反馈 1，表示建立新知识桥梁，并将桥梁 {{a', b'}} 加入当前网络

你可以进行以下三类操作：

1. 测试查询：询问"连接 a b"（a, b 为 1 到 9 之间的不同知识模块）
   - 系统反馈 0 或 1

2. 宣告猜测：提交你认为的关联规则类型（B、C、D 或 E）
   - 系统反馈"正确"或"错误"
   - 注意：必须先完成至少 2 次测试查询后才能宣告

3. 状态查询：
   - 询问剩余可触发新建桥梁（反馈 1）的次数
   - 询问已完成的测试查询次数

- 全局至多允许 2 次反馈为 1 的情况；若出现第 3 次反馈 1，任务失败
- 在正确宣告关联规则后，你需要连续提交 3 个测试查询，每个查询的 (a,b) 必须满足：
  * a 和 b 在初始依赖树中不相邻
  * a 不等于 b
  * 每次反馈必须为 0

1. 通过测试查询推断出隐藏的关联规则类型
2. 正确宣告该关联规则
3. 在宣告后连续 3 次提交满足条件的查询，且每次反馈均为 0

每次只能包含一个操作标签：

- 测试查询（例如查询模块 1 和 4）：
<query_test>1,4</query_test>

- 宣告猜测（例如猜测是规则 B）：
<query_guess>B</query_guess>

- 查询剩余可触发 1 的次数：
<query_remain></query_remain>

- 查询已完成的测试次数：
<query_count></query_count>

- 正确宣告关联规则类型
- 宣告后连续 3 次测试查询反馈均为 0
- 全程反馈 1 的总次数不超过 2
"""

    contextualized_rule_en_3 = """\
[Education Scenario] Let's use the "Cross-disciplinary Knowledge Graph Connection and Teaching Path Exploration System". Here are the rules:

There is a connected knowledge network, initially a pre-requisite dependency tree, containing modules 1 to 9, with the core foundational theory at node 1.

Initial knowledge connection set (existing dependencies): (1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (6,8), (6,9)

Network structure (rooted at node 1):
- Pre-requisite module relationship: pa(1)=1; pa(2)=1; pa(3)=1; pa(4)=2; pa(5)=2; pa(6)=3; pa(7)=3; pa(8)=6; pa(9)=6
- Knowledge advancement depth: depth(1)=0; depth(2)=1; depth(3)=1; depth(4)=2; depth(5)=2; depth(6)=2; depth(7)=2; depth(8)=3; depth(9)=3

Cross-domain analogy mapping p: p(1)=1; p(2)=3; p(3)=2; p(4)=5; p(5)=4; p(6)=7; p(7)=6; p(8)=9; p(9)=8

The system has secretly selected a cognitive association rule R from four possibilities (B, C, D, E):

- Rule B: R(a,b) = (pa(a), pa(b))
- Rule C: R(a,b) = (lca(a,b), b), where lca is the lowest common pre-requisite module
- Rule D: R(a,b) = (g(a), g(b)), where g(x) = x (if depth(x) is even), g(x) = pa(x) (if depth(x) is odd)
- Rule E: R(a,b) = (p(a), p(b)), where p is the analogy mapping above

The current connection set starts with the dependency tree. When you submit an association query (a,b) where a is not equal to b:

1. System computes the actual associated points (a', b') = R(a,b)
2. If a' = b' (self-looping) or the bridge {{a', b'}} is already in the current network, system returns 0, meaning the bridge exists or is unneeded.
3. Otherwise returns 1 and adds the new knowledge bridge {{a', b'}} to the current network.

You can perform three types of operations:

1. Test Query: Ask "connect a b" (a, b are different modules from 1 to 9)
   - System returns 0 or 1

2. Declare Guess: Submit your believed rule type (B, C, D, or E)
   - System returns "Correct" or "Incorrect"
   - Note: Must complete at least 2 test queries before declaring

3. Status Query:
   - Ask for remaining count of feedback 1 allowed
   - Ask for completed test query count

- Maximum 2 feedbacks of 1 allowed globally; if a 3rd feedback of 1 occurs, the task fails
- After correctly declaring the rule, you need to submit 3 consecutive test queries, each (a,b) must satisfy:
  * a and b are not adjacent in the initial dependency tree
  * a is not equal to b
  * Each feedback must be 0

1. Infer the hidden rule type through test queries
2. Correctly declare the association rule
3. After declaration, submit 3 consecutive queries meeting the conditions with feedback 0 each time

Each turn must contain only one operation tag:

- Test Query (e.g., querying modules 1 and 4):
<query_test>1,4</query_test>

- Declare Guess (e.g., guessing rule B):
<query_guess>B</query_guess>

- Query remaining feedback 1 count:
<query_remain></query_remain>

- Query completed test count:
<query_count></query_count>

- Correctly declare the rule type
- After declaration, 3 consecutive test queries all return 0
- Total feedback 1 count does not exceed 2 throughout the task
"""

    contextualized_rule_zh_4 = """\
[制造业/工业场景] 我们现在来使用"供应链韧性重构与兼容性匹配测试系统"，规则如下：

有一个连通的生产装配图，初始为一棵物料清单(BOM)依赖树，包含生产节点 1 到 9，最终装配线为节点 1。

初始直接组装集（现有BOM）：(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (6,8), (6,9)

供应链结构信息（以最终装配线 1 为根）：
- 上游装配节点关系：pa(1)=1; pa(2)=1; pa(3)=1; pa(4)=2; pa(5)=2; pa(6)=3; pa(7)=3; pa(8)=6; pa(9)=6
- 供应链层级（深度）：depth(1)=0; depth(2)=1; depth(3)=1; depth(4)=2; depth(5)=2; depth(6)=2; depth(7)=2; depth(8)=3; depth(9)=3

平行替代组件映射 p 的定义：p(1)=1; p(2)=3; p(3)=2; p(4)=5; p(5)=4; p(6)=7; p(7)=6; p(8)=9; p(9)=8

系统秘密选择了一种重构匹配逻辑 R，它有四种可能（B、C、D、E），具体定义如下：

- 逻辑 B：R(a,b) = (pa(a), pa(b))
- 逻辑 C：R(a,b) = (lca(a,b), b)，其中 lca 表示最近共同上游装配节点
- 逻辑 D：R(a,b) = (g(a), g(b))，其中 g(x) = x（若 depth(x) 为偶数），g(x) = pa(x)（若 depth(x) 为奇数）
- 逻辑 E：R(a,b) = (p(a), p(b))，其中 p 为上述替代组件映射

当前组装集初始为上述BOM依赖树。当你提交一个兼容性测试 (a,b)（a 不等于 b）时：

1. 系统计算受重构逻辑影响的实际对接节点 (a', b') = R(a,b)
2. 如果 a' = b'（节点自环）或链路 {{a', b'}} 已在当前图谱中，系统反馈 0，表示链路已闭合或无需新增
3. 否则反馈 1，表示新增直接供应链，并将链路 {{a', b'}} 加入当前图谱

你可以进行以下三类操作：

1. 测试查询：询问"连接 a b"（a, b 为 1 到 9 之间的不同节点）
   - 系统反馈 0 或 1

2. 宣告猜测：提交你认为的重构逻辑类型（B、C、D 或 E）
   - 系统反馈"正确"或"错误"
   - 注意：必须先完成至少 2 次测试查询后才能宣告

3. 状态查询：
   - 询问剩余可触发新增链路（反馈 1）的次数
   - 询问已完成的测试查询次数

- 全局至多允许 2 次反馈为 1 的情况；若出现第 3 次反馈 1，任务失败
- 在正确宣告重构逻辑后，你需要连续提交 3 个测试查询，每个查询的 (a,b) 必须满足：
  * a 和 b 在初始依赖树中不相邻
  * a 不等于 b
  * 每次反馈必须为 0

1. 通过测试查询推断出隐藏的重构逻辑类型
2. 正确宣告该重构逻辑
3. 在宣告后连续 3 次提交满足条件的查询，且每次反馈均为 0

每次只能包含一个操作标签：

- 测试查询（例如查询节点 1 和 4）：
<query_test>1,4</query_test>

- 宣告猜测（例如猜测是逻辑 B）：
<query_guess>B</query_guess>

- 查询剩余可触发 1 的次数：
<query_remain></query_remain>

- 查询已完成的测试次数：
<query_count></query_count>

- 正确宣告重构逻辑类型
- 宣告后连续 3 次测试查询反馈均为 0
- 全程反馈 1 的总次数不超过 2
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario] Let's use the "Supply Chain Resilience Reconstruction and Compatibility Matching System". Here are the rules:

There is a connected assembly graph, initially a Bill of Materials (BOM) dependency tree, containing nodes 1 to 9, with the final assembly line at node 1.

Initial direct assembly set (existing BOM): (1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (6,8), (6,9)

Supply chain structure (rooted at assembly line 1):
- Upstream assembly node relationship: pa(1)=1; pa(2)=1; pa(3)=1; pa(4)=2; pa(5)=2; pa(6)=3; pa(7)=3; pa(8)=6; pa(9)=6
- Supply chain level (depth): depth(1)=0; depth(2)=1; depth(3)=1; depth(4)=2; depth(5)=2; depth(6)=2; depth(7)=2; depth(8)=3; depth(9)=3

Parallel substitute component mapping p: p(1)=1; p(2)=3; p(3)=2; p(4)=5; p(5)=4; p(6)=7; p(7)=6; p(8)=9; p(9)=8

The system has secretly selected a reconstruction logic R from four possibilities (B, C, D, E):

- Logic B: R(a,b) = (pa(a), pa(b))
- Logic C: R(a,b) = (lca(a,b), b), where lca is the lowest common upstream assembly node
- Logic D: R(a,b) = (g(a), g(b)), where g(x) = x (if depth(x) is even), g(x) = pa(x) (if depth(x) is odd)
- Logic E: R(a,b) = (p(a), p(b)), where p is the substitute mapping above

The current assembly set starts with the BOM tree. When you submit a compatibility query (a,b) where a is not equal to b:

1. System computes the actual interface nodes (a', b') = R(a,b)
2. If a' = b' (self-looping) or the supply link {{a', b'}} is already in the current graph, system returns 0, meaning the link is closed or no addition is needed.
3. Otherwise returns 1 and adds the new supply link {{a', b'}} to the current graph.

You can perform three types of operations:

1. Test Query: Ask "connect a b" (a, b are different nodes from 1 to 9)
   - System returns 0 or 1

2. Declare Guess: Submit your believed logic type (B, C, D, or E)
   - System returns "Correct" or "Incorrect"
   - Note: Must complete at least 2 test queries before declaring

3. Status Query:
   - Ask for remaining count of feedback 1 allowed
   - Ask for completed test query count

- Maximum 2 feedbacks of 1 allowed globally; if a 3rd feedback of 1 occurs, the task fails
- After correctly declaring the logic, you need to submit 3 consecutive test queries, each (a,b) must satisfy:
  * a and b are not adjacent in the initial BOM tree
  * a is not equal to b
  * Each feedback must be 0

1. Infer the hidden reconstruction logic type through test queries
2. Correctly declare the logic
3. After declaration, submit 3 consecutive queries meeting the conditions with feedback 0 each time

Each turn must contain only one operation tag:

- Test Query (e.g., querying nodes 1 and 4):
<query_test>1,4</query_test>

- Declare Guess (e.g., guessing logic B):
<query_guess>B</query_guess>

- Query remaining feedback 1 count:
<query_remain></query_remain>

- Query completed test count:
<query_count></query_count>

- Correctly declare the logic type
- After declaration, 3 consecutive test queries all return 0
- Total feedback 1 count does not exceed 2 throughout the task
"""

    contextualized_rule_zh_5 = """\
[法律场景] 我们现在来使用"法规冲突适用与司法解释链接系统"，规则如下：

有一个连通的法条体系，初始为一棵法律效力从属树，包含法律规范文件 1 到 9，宪法/基本法为节点 1。

初始从属关联集（现有体系）：(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (6,8), (6,9)

法律结构信息（以基本法 1 为根）：
- 上位法关系：pa(1)=1; pa(2)=1; pa(3)=1; pa(4)=2; pa(5)=2; pa(6)=3; pa(7)=3; pa(8)=6; pa(9)=6
- 法律效力级别（深度）：depth(1)=0; depth(2)=1; depth(3)=1; depth(4)=2; depth(5)=2; depth(6)=2; depth(7)=2; depth(8)=3; depth(9)=3

法系内类推映射 p 的定义：p(1)=1; p(2)=3; p(3)=2; p(4)=5; p(5)=4; p(6)=7; p(7)=6; p(8)=9; p(9)=8

系统秘密选择了一种冲突解决适用原则 R，它有四种可能（B、C、D、E），具体定义如下：

- 原则 B：R(a,b) = (pa(a), pa(b))
- 原则 C：R(a,b) = (lca(a,b), b)，其中 lca 表示最近共同上位法
- 原则 D：R(a,b) = (g(a), g(b))，其中 g(x) = x（若 depth(x) 为偶数），g(x) = pa(x)（若 depth(x) 为奇数）
- 原则 E：R(a,b) = (p(a), p(b))，其中 p 为上述类推映射

当前解释链接集初始为上述从属树。当你提交一个适用冲突查询 (a,b)（a 不等于 b）时：

1. 系统计算受原则约束的实际适用法条 (a', b') = R(a,b)
2. 如果 a' = b'（内部吸收）或链接 {{a', b'}} 已在当前体系中，系统反馈 0，表示无需补充解释链接
3. 否则反馈 1，表示创设新解释链接，并将链接 {{a', b'}} 加入当前体系

你可以进行以下三类操作：

1. 测试查询：询问"连接 a b"（a, b 为 1 到 9 之间的不同法规文件）
   - 系统反馈 0 或 1

2. 宣告猜测：提交你认为的冲突解决原则（B、C、D 或 E）
   - 系统反馈"正确"或"错误"
   - 注意：必须先完成至少 2 次测试查询后才能宣告

3. 状态查询：
   - 询问剩余可触发创设链接（反馈 1）的次数
   - 询问已完成的测试查询次数

- 全局至多允许 2 次反馈为 1 的情况；若出现第 3 次反馈 1，评估失败
- 在正确宣告冲突解决原则后，你需要连续提交 3 个测试查询，每个查询的 (a,b) 必须满足：
  * a 和 b 在初始从属树中不相邻
  * a 不等于 b
  * 每次反馈必须为 0

1. 通过测试查询推断出隐藏的冲突解决原则
2. 正确宣告该原则
3. 在宣告后连续 3 次提交满足条件的查询，且每次反馈均为 0

每次只能包含一个操作标签：

- 测试查询（例如查询法条 1 和 4）：
<query_test>1,4</query_test>

- 宣告猜测（例如猜测是原则 B）：
<query_guess>B</query_guess>

- 查询剩余可触发 1 的次数：
<query_remain></query_remain>

- 查询已完成的测试次数：
<query_count></query_count>

- 正确宣告原则类型
- 宣告后连续 3 次测试查询反馈均为 0
- 全程反馈 1 的总次数不超过 2
"""

    contextualized_rule_en_5 = """\
[Legal Scenario] Let's use the "Regulation Conflict Application and Judicial Interpretation Linking System". Here are the rules:

There is a connected legal system, initially a subordination tree of legal effects, containing regulatory documents 1 to 9, with the Constitution/Basic Law at node 1.

Initial subordination set (existing hierarchy): (1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (6,8), (6,9)

Legal structure (rooted at Basic Law 1):
- Superior law relationship: pa(1)=1; pa(2)=1; pa(3)=1; pa(4)=2; pa(5)=2; pa(6)=3; pa(7)=3; pa(8)=6; pa(9)=6
- Legal effect level (depth): depth(1)=0; depth(2)=1; depth(3)=1; depth(4)=2; depth(5)=2; depth(6)=2; depth(7)=2; depth(8)=3; depth(9)=3

Intra-system analogical mapping p: p(1)=1; p(2)=3; p(3)=2; p(4)=5; p(5)=4; p(6)=7; p(7)=6; p(8)=9; p(9)=8

The system has secretly selected an application principle R from four possibilities (B, C, D, E):

- Principle B: R(a,b) = (pa(a), pa(b))
- Principle C: R(a,b) = (lca(a,b), b), where lca is the lowest common superior law
- Principle D: R(a,b) = (g(a), g(b)), where g(x) = x (if depth(x) is even), g(x) = pa(x) (if depth(x) is odd)
- Principle E: R(a,b) = (p(a), p(b)), where p is the analogical mapping above

The current interpretation link set starts with the subordination tree. When you submit a conflict query (a,b) where a is not equal to b:

1. System computes the actual applicable law under the principle (a', b') = R(a,b)
2. If a' = b' (internal absorption) or the interpretation link {{a', b'}} is already in the current system, system returns 0, meaning no supplementary link is needed.
3. Otherwise returns 1 and adds the new interpretation link {{a', b'}} to the current system.

You can perform three types of operations:

1. Test Query: Ask "connect a b" (a, b are different documents from 1 to 9)
   - System returns 0 or 1

2. Declare Guess: Submit your believed principle type (B, C, D, or E)
   - System returns "Correct" or "Incorrect"
   - Note: Must complete at least 2 test queries before declaring

3. Status Query:
   - Ask for remaining count of feedback 1 allowed
   - Ask for completed test query count

- Maximum 2 feedbacks of 1 allowed globally; if a 3rd feedback of 1 occurs, the task fails
- After correctly declaring the principle, you need to submit 3 consecutive test queries, each (a,b) must satisfy:
  * a and b are not adjacent in the initial subordination tree
  * a is not equal to b
  * Each feedback must be 0

1. Infer the hidden conflict resolution principle through test queries
2. Correctly declare the principle
3. After declaration, submit 3 consecutive queries meeting the conditions with feedback 0 each time

Each turn must contain only one operation tag:

- Test Query (e.g., querying documents 1 and 4):
<query_test>1,4</query_test>

- Declare Guess (e.g., guessing principle B):
<query_guess>B</query_guess>

- Query remaining feedback 1 count:
<query_remain></query_remain>

- Query completed test count:
<query_count></query_count>

- Correctly declare the principle type
- After declaration, 3 consecutive test queries all return 0
- Total feedback 1 count does not exceed 2 throughout the task
"""

    tags = ["answer", "query_test", "query_remain", "query_count", "query_guess"]
    
    reasoning_type = "溯因推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"rule_type": "B"},
            2: {"rule_type": "E"},
            3: {"rule_type": "D"},
            4: {"rule_type": "C"},
            5: {"rule_type": "C"},
        },
        "en": {
            1: {"rule_type": "B"},
            2: {"rule_type": "E"},
            3: {"rule_type": "D"},
            4: {"rule_type": "C"},
            5: {"rule_type": "C"},
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        self.initial_edges = {(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (6,8), (6,9)}
        self.initial_edges_normalized = {tuple(sorted([a,b])) for a,b in self.initial_edges}
        
        self.pa = {1:1, 2:1, 3:1, 4:2, 5:2, 6:3, 7:3, 8:6, 9:6}
        self.depth = {1:0, 2:1, 3:1, 4:2, 5:2, 6:2, 7:2, 8:3, 9:3}
        self.perm = {1:1, 2:3, 3:2, 4:5, 5:4, 6:7, 7:6, 8:9, 9:8}
        
        self.current_edges = set(self.initial_edges_normalized)
        self.feedback_one_count = 0
        self.test_query_count = 0
        self.declared = False
        self.declaration_correct = False
        self.final_phase_count = 0

        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.rule_type = cfg["rule_type"]
        self._game_info = {}

    def _lca(self, a, b):
        while self.depth[a] > self.depth[b]:
            a = self.pa[a]
        while self.depth[b] > self.depth[a]:
            b = self.pa[b]
        while a != b:
            a = self.pa[a]
            b = self.pa[b]
        return a

    def _apply_rewrite(self, a, b):
        if self.rule_type == "B":
            return self.pa[a], self.pa[b]
        elif self.rule_type == "C":
            lca = self._lca(a, b)
            return lca, b
        elif self.rule_type == "D":
            def g(x):
                return x if self.depth[x] % 2 == 0 else self.pa[x]
            return g(a), g(b)
        elif self.rule_type == "E":
            return self.perm[a], self.perm[b]
        else:
            raise ValueError(f"Unknown rule type: {self.rule_type}")

    def _process_test_query(self, a, b):
        if a == b:
            raise ValueError("a and b must be different")
        if a < 1 or a > 9 or b < 1 or b > 9:
            raise ValueError("Nodes must be between 1 and 9")
        
        self.test_query_count += 1
        
        a_prime, b_prime = self._apply_rewrite(a, b)
        
        if a_prime == b_prime:
            return 0
        
        edge_normalized = tuple(sorted([a_prime, b_prime]))
        if edge_normalized in self.current_edges:
            return 0
        
        self.current_edges.add(edge_normalized)
        self.feedback_one_count += 1
        
        if self.feedback_one_count > 2:
            if self.config.language == "zh":
                raise ValueError("反馈 1 的次数超过 2 次，游戏失败")
            else:
                raise ValueError("Feedback 1 count exceeded 2, game failed")
        
        return 1

    def evaluate(self, parsed_info):
        if self.state.state == "success":
            return True
            
        answer = parsed_info["answer"].strip().upper()
        
        if self.test_query_count < 2:
            return False
            
        if self.declared and self.declaration_correct and self.final_phase_count >= 3:
            return answer == self.rule_type
            
        return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        if "query_remain" in parsed_info:
            remain = 2 - self.feedback_one_count
            return str(remain)
        
        if "query_count" in parsed_info:
            return str(self.test_query_count)
        
        if "query_guess" in parsed_info:
            guess = parsed_info["query_guess"].strip().upper()
            
            if self.test_query_count < 2:
                if self.config.language == "zh":
                    raise ValueError("必须先完成至少 2 次测试查询才能宣告")
                else:
                    raise ValueError("Must complete at least 2 test queries before declaring")
            
            self.declared = True
            self.declaration_correct = (guess == self.rule_type)
            
            if self.declaration_correct:
                if self.config.language == "zh":
                    return "宣告正确。请继续进行 3 次验证查询（<query_test>）。"
                else:
                    return "Declaration correct. Please proceed with 3 validation queries (<query_test>)."
            else:
                if self.config.language == "zh":
                    raise ValueError("宣告错误，游戏失败。")
                else:
                    raise ValueError("Incorrect declaration, game failed.")

        if "query_test" in parsed_info:
            try:
                raw = parsed_info["query_test"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError("Invalid format")
                a, b = int(parts[0]), int(parts[1])
                
                if self.declared and self.declaration_correct:
                    edge_check = tuple(sorted([a, b]))
                    if edge_check in self.initial_edges_normalized:
                        if self.config.language == "zh":
                            raise ValueError("最终阶段的查询节点在初始树中不能相邻")
                        else:
                            raise ValueError("Final phase query nodes cannot be adjacent in initial tree")
                    
                    feedback = self._process_test_query(a, b)
                    self.final_phase_count += 1
                    
                    if feedback == 1:
                        if self.config.language == "zh":
                            raise ValueError("最终阶段不能出现反馈 1，游戏失败")
                        else:
                            raise ValueError("Feedback 1 not allowed in final phase, game failed")
                    
                    if self.final_phase_count >= 3:
                        self.state.set_state("success", "completed all final tests")
                        if self.config.language == "zh":
                            return "反馈：0。恭喜！你已完成所有任务。"
                        else:
                            return "Feedback: 0. Congratulations! You have completed all tasks."
                    
                    return f"反馈：{feedback}" if self.config.language == "zh" else f"Feedback: {feedback}"
                else:
                    feedback = self._process_test_query(a, b)
                    return f"反馈：{feedback}" if self.config.language == "zh" else f"Feedback: {feedback}"
                
            except ValueError as e:
                raise e
            except Exception as e:
                if self.config.language == "zh":
                    raise ValueError(f"查询格式错误：{str(e)}")
                else:
                    raise ValueError(f"Invalid query format: {str(e)}")
        
        raise ValueError("No valid operation tag found")

    def _cf_make_wrong(self, correct):
        correct_str = str(correct)
        if correct_str.isdigit():
            return str(int(correct_str) + 1)
        
        if self.config.language == "zh":
            if "是" in correct_str:
                return correct_str.replace("是", "否")
            if "否" in correct_str:
                return correct_str.replace("否", "是")
        
        if self.config.language == "en":
            if "Yes" in correct_str:
                return correct_str.replace("Yes", "No")
            if "No" in correct_str:
                return correct_str.replace("No", "Yes")
            if "yes" in correct_str:
                return correct_str.replace("yes", "no")
            if "no" in correct_str:
                return correct_str.replace("no", "yes")

        return correct_str + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        is_zh = (self.config.language == "zh")

        temp_edges = set(self.current_edges)
        temp_feedback_one_count = self.feedback_one_count

        for a in range(1, 10):
            for b in range(1, 10):
                if a == b:
                    continue
                
                query_content = f"{a},{b}"
                
                try:
                    a_prime, b_prime = self._apply_rewrite(a, b)
                    
                    feedback = 1
                    
                    if a_prime == b_prime:
                        feedback = 0
                    else:
                        edge_normalized = tuple(sorted([a_prime, b_prime]))
                        if edge_normalized in temp_edges:
                            feedback = 0
                        else:
                            temp_feedback_one_count += 1
                            if temp_feedback_one_count > 2:
                                feedback = 1
                            temp_edges.add(edge_normalized)
                    
                    if is_zh:
                        ans_str = f"反馈：{feedback}"
                    else:
                        ans_str = f"Feedback: {feedback}"
                    
                    results.append({
                        "query": f"<query_test>{query_content}</query_test>",
                        "answer": ans_str
                    })
                    
                except Exception:
                    continue
        
        return results