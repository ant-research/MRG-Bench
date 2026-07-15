from .base import Game
import re

class InsertionRuleDeductionGame(Game):

    game_rule_zh = """\
我们来玩一个"插入规则推理"游戏，规则如下：

游戏设定了一个长度为 {n} 的有序序列 S0 = {seq}，从左端到右端排列，索引采用 1-based。

系统从以下 4 种插入解释方案中秘密选择了一种并保持不变：
1. 方案1（左端计数-前插）：令 i = p（1 小于等于 p 小于等于 {n}），在当前左端第 i 位元素之前插入新元素 W（W占据位置 i）。
2. 方案2（左端计数-后插）：令 i = p，在当前左端第 i 位元素之后插入 W（W占据位置 i+1）。
3. 方案3（右端计数-前插）：令 j = p（1 小于等于 p 小于等于 {n}），找右端第 j 位元素；等价于左端第 i = N+1-j 位（N为插入前长度，N={n}），在该元素之前插入 W（W占据位置 i）。
4. 方案4（右端计数-后插）：令 j = p，找右端第 j 位元素；等价于左端第 i = N+1-j 位，在该元素之后插入 W（W占据位置 i+1）。

你的任务是推断出真实的插入方案，并执行一次最终插入使得新元素 K 的左端位次等于 {target_pos}。

在最多 {max_probe} 轮探测中，每轮你可以：
1. 先执行一次插入指令：Insert(W, p)，其中 W 为新标签（不与序列中已有标签重名），p 为整数（1 到 {n}）。
2. 再执行一次查询（仅能选择以下一种）：
   - Q_A(k)：询问左端第 k 位元素是谁。k 的范围是 1 到 {n_after}。
   - Q_B(k)：询问右端第 k 位元素是谁。k 的范围是 1 到 {n_after}。
   - Q_C(L)：询问标签 L 的左端位次。L 必须是序列中存在的标签。
   - Q_D(L)：询问标签 L 的右端位次。L 必须是序列中存在的标签。
3. 每轮查询结束后，序列会重置回 S0。

探测阶段每轮使用以下格式：

插入指令：
<insert>W,p</insert>

查询指令（四选一）：
<query_a>k</query_a>
<query_b>k</query_b>
<query_c>L</query_c>
<query_d>L</query_d>

最终提交答案时：
<answer>scheme=X, insert=K,p_final</answer>

其中 X 为方案编号（1/2/3/4），K 为新标签，p_final 为插入参数。

示例：
探测轮次：
<insert>W1,3</insert>
<query_a>4</query_a>

最终提交：
<answer>scheme=1, insert=K,2</answer>

注意：若插入或查询越界、标签冲突，将返回错误并可能影响游戏结果。请确保每轮包含一次插入和一次查询，最终提交时包含方案编号和最终插入指令。
"""

    game_rule_en = """\
Let's play an "Insertion Rule Deduction" game. Here are the rules:

The game starts with an ordered sequence S0 = {seq} of length {n}, arranged from left to right with 1-based indexing.

The system has secretly selected one of the following 4 insertion interpretation schemes and will maintain it throughout:
1. Scheme 1 (Left-count, Insert-before): Let i = p (1 less than or equal to p less than or equal to {n}), insert new element W before the i-th element from the left (W occupies position i).
2. Scheme 2 (Left-count, Insert-after): Let i = p, insert W after the i-th element from the left (W occupies position i+1).
3. Scheme 3 (Right-count, Insert-before): Let j = p (1 less than or equal to p less than or equal to {n}), find the j-th element from the right; equivalent to the i = N+1-j position from the left (N is the length before insertion, N={n}), insert W before that element (W occupies position i).
4. Scheme 4 (Right-count, Insert-after): Let j = p, find the j-th element from the right; equivalent to the i = N+1-j position from the left, insert W after that element (W occupies position i+1).

Your task is to deduce the true insertion scheme and perform a final insertion such that the new element K has a left-end position equal to {target_pos}.

In at most {max_probe} probing rounds, each round you can:
1. First execute an insertion instruction: Insert(W, p), where W is a new label (must not duplicate existing labels in the sequence), and p is an integer (1 to {n}).
2. Then execute one query (choose only one of the following):
   - Q_A(k): Ask which element is at the k-th position from the left. k ranges from 1 to {n_after}.
   - Q_B(k): Ask which element is at the k-th position from the right. k ranges from 1 to {n_after}.
   - Q_C(L): Ask the left-end position of label L. L must be an existing label in the sequence.
   - Q_D(L): Ask the right-end position of label L. L must be an existing label in the sequence.
3. After each query, the sequence resets to S0.

For each probing round, use the following format:

Insertion instruction:
<insert>W,p</insert>

Query instruction (choose one):
<query_a>k</query_a>
<query_b>k</query_b>
<query_c>L</query_c>
<query_d>L</query_d>

For final submission:
<answer>scheme=X, insert=K,p_final</answer>

Where X is the scheme number (1/2/3/4), K is a new label, and p_final is the insertion parameter.

Example:
Probing round:
<insert>W1,3</insert>
<query_a>4</query_a>

Final submission:
<answer>scheme=1, insert=K,2</answer>

Note: If insertion or query is out of bounds or labels conflict, an error will be returned and may affect the game result. Ensure each round contains one insertion and one query, and final submission includes both scheme number and final insertion instruction.
"""

    contextualized_rule_zh_1 = """\
[交通场景]
智能列车调度系统测试已启动。

当前编组站内停靠了一列长度为 {n} 的初始车厢序列 S0 = {seq}，从车头（左端）到车尾（右端）排列，车厢顺位采用 1-based 计算。

调度系统从以下 4 种隐蔽的挂载协议中秘密激活了一种并全程维持：
1. 协议1（正向寻址-前置挂载）：令 i = p（1 小于等于 p 小于等于 {n}），在当前从车头算起第 i 节车厢之前挂载新车厢 W（W占据正向顺位 i）。
2. 协议2（正向寻址-后置挂载）：令 i = p，在当前从车头算起第 i 节车厢之后挂载 W（W占据正向顺位 i+1）。
3. 协议3（尾向寻址-前置挂载）：令 j = p（1 小于等于 p 小于等于 {n}），寻找从车尾算起第 j 节车厢；等价于从车头算起第 i = N+1-j 节（N为挂载前长度，N={n}），在该车厢之前挂载 W（W占据正向顺位 i）。
4. 协议4（尾向寻址-后置挂载）：令 j = p，寻找从车尾算起第 j 节车厢；等价于从车头算起第 i = N+1-j 节，在该车厢之后挂载 W（W占据正向顺位 i+1）。

你的任务是推断出系统当前运行的真实挂载协议，并下达一次最终挂载指令使得新车厢 K 的正向顺位等于 {target_pos}。

在最多 {max_probe} 轮探测中，每轮你可以：
1. 先执行一次挂载指令：Insert(W, p)，其中 W 为新车厢编号（不与序列中已有编号重名），p 为整数（1 到 {n}）。
2. 再执行一次传感器查询（仅能选择以下一种）：
   - Q_A(k)：询问正向（从车头算起）第 k 节车厢是谁。k 的范围是 1 到 {n_after}。
   - Q_B(k)：询问逆向（从车尾算起）第 k 节车厢是谁。k 的范围是 1 到 {n_after}。
   - Q_C(L)：询问车厢 L 的正向顺位。L 必须是序列中存在的车厢。
   - Q_D(L)：询问车厢 L 的逆向顺位。L 必须是序列中存在的车厢。
3. 每轮查询结束后，列车编组会重置回 S0。

探测阶段每轮使用以下格式：

挂载指令：
<insert>W,p</insert>

查询指令（四选一）：
<query_a>k</query_a>
<query_b>k</query_b>
<query_c>L</query_c>
<query_d>L</query_d>

最终提交答案时：
<answer>scheme=X, insert=K,p_final</answer>

其中 X 为协议编号（1/2/3/4），K 为新车厢编号，p_final 为挂载参数。

示例：
探测轮次：
<insert>W1,3</insert>
<query_a>4</query_a>

最终提交：
<answer>scheme=1, insert=K,2</answer>

注意：若指令或查询越界、编号冲突，将返回错误并可能影响游戏结果。请确保每轮包含一次挂载和一次查询，最终提交时包含协议编号和最终挂载指令。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Intelligent train dispatch system test initiated.

The marshaling yard currently holds an initial sequence of carriages S0 = {seq} with a length of {n}, arranged from the locomotive (front/left) to the caboose (rear/right), with 1-based indexing.

The dispatch system has secretly activated one of the following 4 hidden coupling protocols and will maintain it throughout:
1. Protocol 1 (Forward Addressing - Pre-coupling): Let i = p (1 <= p <= {n}), couple the new carriage W ahead of the i-th carriage from the front (W occupies forward position i).
2. Protocol 2 (Forward Addressing - Post-coupling): Let i = p, couple W behind the i-th carriage from the front (W occupies forward position i+1).
3. Protocol 3 (Reverse Addressing - Pre-coupling): Let j = p (1 <= p <= {n}), locate the j-th carriage from the rear; equivalently the i = N+1-j position from the front (where N is the pre-coupling length, N={n}), and couple W ahead of it (W occupies forward position i).
4. Protocol 4 (Reverse Addressing - Post-coupling): Let j = p, locate the j-th carriage from the rear; equivalently the i = N+1-j position from the front, and couple W behind it (W occupies forward position i+1).

Your task is to deduce the true coupling protocol and execute a final coupling command such that the new carriage K achieves a forward position exactly equal to {target_pos}.

In at most {max_probe} probing rounds, each round you can:
1. First execute a coupling command: Insert(W, p), where W is a new carriage ID (must not duplicate existing IDs), and p is an integer (1 to {n}).
2. Then execute one sensor query (choose only one):
   - Q_A(k): Query the carriage ID at the k-th forward position. k ranges from 1 to {n_after}.
   - Q_B(k): Query the carriage ID at the k-th reverse position. k ranges from 1 to {n_after}.
   - Q_C(L): Query the forward position of carriage L. L must exist in the current sequence.
   - Q_D(L): Query the reverse position of carriage L. L must exist in the current sequence.
3. After each query, the train sequence resets to S0.

For each probing round, use the following format:

Coupling command:
<insert>W,p</insert>

Query command (choose one):
<query_a>k</query_a>
<query_b>k</query_b>
<query_c>L</query_c>
<query_d>L</query_d>

For final submission:
<answer>scheme=X, insert=K,p_final</answer>

Where X is the protocol number (1/2/3/4), K is the new carriage ID, and p_final is the coupling parameter.

Example:
Probing round:
<insert>W1,3</insert>
<query_a>4</query_a>

Final submission:
<answer>scheme=1, insert=K,2</answer>

Note: Out-of-bounds commands or ID conflicts will return errors. Ensure each round contains one insertion and one query, and the final submission includes both the protocol number and the final command.
"""

    contextualized_rule_zh_2 = """\
[医疗场景]
基因靶向药物递送路径优化已启动。

当前载体中存在一个长度为 {n} 的初始给药序列 S0 = {seq}，从 N端（左侧）向 C端（右侧）排列，给药顺位采用 1-based。

干预引擎从以下 4 种隐蔽的给药机制中秘密设定了一种并全程维持：
1. 机制1（N端计数-上游植入）：令 i = p（1 小于等于 p 小于等于 {n}），在距 N端 第 i 个药物节点上游植入新药物 W（W占据顺位 i）。
2. 机制2（N端计数-下游植入）：令 i = p，在距 N端 第 i 个药物节点下游植入 W（W占据顺位 i+1）。
3. 机制3（C端计数-上游植入）：令 j = p（1 小于等于 p 小于等于 {n}），寻找距 C端 第 j 个节点；等价于距 N端 第 i = N+1-j 个（N为植入前长度，N={n}），在该节点上游植入 W（W占据顺位 i）。
4. 机制4（C端计数-下游植入）：令 j = p，寻找距 C端 第 j 个节点；等价于距 N端 第 i = N+1-j 个，在该节点下游植入 W（W占据顺位 i+1）。

你的任务是推断出系统真实的给药机制，并执行一次最终植入，使得靶向核心药物 K 距 N端的绝对顺位等于 {target_pos}。

在最多 {max_probe} 轮生物探测中，每轮你可以：
1. 先执行一次试验植入：Insert(W, p)，其中 W 为新药物编号（不与序列中已有编号重名），p 为整数（1 到 {n}）。
2. 再执行一次生化测序查询（仅能选择以下一种）：
   - Q_A(k)：询问距 N端 第 k 个节点的药物编号。k 的范围是 1 到 {n_after}。
   - Q_B(k)：询问距 C端 第 k 个节点的药物编号。k 的范围是 1 到 {n_after}。
   - Q_C(L)：询问药物 L 距 N端的绝对顺位。L 必须是序列中存在的药物。
   - Q_D(L)：询问药物 L 距 C端的绝对顺位。L 必须是序列中存在的药物。
3. 每轮测序结束后，分子链会重置回初始状态 S0。

探测阶段每轮使用以下格式：

植入指令：
<insert>W,p</insert>

测序查询（四选一）：
<query_a>k</query_a>
<query_b>k</query_b>
<query_c>L</query_c>
<query_d>L</query_d>

最终提交答案时：
<answer>scheme=X, insert=K,p_final</answer>

其中 X 为机制编号（1/2/3/4），K 为新药物编号，p_final 为植入参数。

示例：
探测轮次：
<insert>W1,3</insert>
<query_a>4</query_a>

最终提交：
<answer>scheme=1, insert=K,2</answer>

注意：若植入或查询越界、编号冲突，将导致生化测序失败。请确保每轮包含一次植入和一次查询，最终提交时包含机制编号和最终指令。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Targeted drug delivery pathway optimization initiated.

The carrier currently contains an initial drug sequence S0 = {seq} of length {n}, ordered from the N-terminus (left) to the C-terminus (right), with 1-based indexing.

The intervention engine has secretly configured one of the following 4 hidden delivery mechanisms and will maintain it:
1. Mechanism 1 (N-terminus Count - Upstream Implant): Let i = p (1 <= p <= {n}), implant new drug W upstream of the i-th drug node from the N-terminus (W occupies position i).
2. Mechanism 2 (N-terminus Count - Downstream Implant): Let i = p, implant W downstream of the i-th drug node from the N-terminus (W occupies position i+1).
3. Mechanism 3 (C-terminus Count - Upstream Implant): Let j = p (1 <= p <= {n}), locate the j-th node from the C-terminus; equivalently the i = N+1-j position from the N-terminus (N is pre-implant length, N={n}), and implant W upstream of it (W occupies position i).
4. Mechanism 4 (C-terminus Count - Downstream Implant): Let j = p, locate the j-th node from the C-terminus; equivalently the i = N+1-j position from the N-terminus, and implant W downstream of it (W occupies position i+1).

Your task is to deduce the true delivery mechanism and execute a final implant such that the core targeted drug K achieves an absolute position of {target_pos} from the N-terminus.

In at most {max_probe} biochemical probing rounds, each round you can:
1. First execute a trial implant: Insert(W, p), where W is a new drug ID (no duplicates), and p is an integer (1 to {n}).
2. Then execute one sequencing query (choose only one):
   - Q_A(k): Query the drug ID at the k-th node from the N-terminus. k ranges from 1 to {n_after}.
   - Q_B(k): Query the drug ID at the k-th node from the C-terminus. k ranges from 1 to {n_after}.
   - Q_C(L): Query the absolute position of drug L from the N-terminus. L must exist.
   - Q_D(L): Query the absolute position of drug L from the C-terminus. L must exist.
3. After each query, the molecular chain resets to S0.

For each probing round, use the following format:

Implant command:
<insert>W,p</insert>

Query command (choose one):
<query_a>k</query_a>
<query_b>k</query_b>
<query_c>L</query_c>
<query_d>L</query_d>

For final submission:
<answer>scheme=X, insert=K,p_final</answer>

Where X is the mechanism number (1/2/3/4), K is the new drug ID, and p_final is the parameter.

Example:
Probing round:
<insert>W1,3</insert>
<query_a>4</query_a>

Final submission:
<answer>scheme=1, insert=K,2</answer>

Note: Out-of-bounds parameters or ID conflicts will cause sequencing failure. Ensure one implant and one query per round, and submit the scheme number and final command in the answer.
"""

    contextualized_rule_zh_3 = """\
[教育场景]
个性化学习路径引擎排课测试启动。

教务系统初始安排了长度为 {n} 的知识模块序列 S0 = {seq}，从先导（左端）到进阶（右端）正序排列，学习排位采用 1-based。

系统底层排课引擎默认启用了以下 4 种隐蔽的知识点插入策略之一，且在测试期间不改变：
1. 策略1（正序导向-先置学习）：令 i = p（1 小于等于 p 小于等于 {n}），在当前正序第 i 个模块之前安排新模块 W（W占据正序排位 i）。
2. 策略2（正序导向-后置学习）：令 i = p，在当前正序第 i 个模块之后安排 W（W占据正序排位 i+1）。
3. 策略3（逆序导向-先置学习）：令 j = p（1 小于等于 p 小于等于 {n}），定位逆序第 j 个模块；等价于正序第 i = N+1-j 个（N为安排前长度，N={n}），在该模块之前安排 W（W占据正序排位 i）。
4. 策略4（逆序导向-后置学习）：令 j = p，定位逆序第 j 个模块；等价于正序第 i = N+1-j 个，在该模块之后安排 W（W占据正序排位 i+1）。

你的任务是推摸清教务系统的排课策略，最终插入核心模块 K，使其在正序中排在第 {target_pos} 位。

在最多 {max_probe} 轮排课探测中，每轮你可以：
1. 先执行一次试排指令：Insert(W, p)，其中 W 为新模块代码（不与已有代码重名），p 为整数（1 到 {n}）。
2. 再执行一次路径检视查询（仅能选择以下一种）：
   - Q_A(k)：检视正序第 k 节课的模块代码。k 的范围是 1 到 {n_after}。
   - Q_B(k)：检视逆序第 k 节课的模块代码。k 的范围是 1 到 {n_after}。
   - Q_C(L)：检视模块 L 的正序排位。L 必须是路径中已有的模块。
   - Q_D(L)：检视模块 L 的逆序排位。L 必须是路径中已有的模块。
3. 每轮检视结束后，学习路径会重置为初始排课 S0。

探测阶段每轮使用以下格式：

试排指令：
<insert>W,p</insert>

检视查询（四选一）：
<query_a>k</query_a>
<query_b>k</query_b>
<query_c>L</query_c>
<query_d>L</query_d>

最终提交答案时：
<answer>scheme=X, insert=K,p_final</answer>

其中 X 为策略编号（1/2/3/4），K 为核心模块代码，p_final 为排课参数。

示例：
探测轮次：
<insert>W1,3</insert>
<query_a>4</query_a>

最终提交：
<answer>scheme=1, insert=K,2</answer>

注意：若指令或查询越界、代码冲突，系统将返回参数错误。请确保每轮包含一次试排和一次检视，最终提交时包含策略编号和最终排课指令。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Personalized learning path engine scheduling test initiated.

The academic system has initially scheduled a knowledge module sequence S0 = {seq} of length {n}, ordered forward from prerequisite (left) to advanced (right), with 1-based indexing.

The underlying scheduling engine has enabled one of the following 4 hidden module insertion strategies by default and keeps it constant:
1. Strategy 1 (Forward-oriented - Prior Learning): Let i = p (1 <= p <= {n}), schedule the new module W prior to the i-th module in the forward sequence (W occupies forward position i).
2. Strategy 2 (Forward-oriented - Post Learning): Let i = p, schedule W after the i-th module in the forward sequence (W occupies forward position i+1).
3. Strategy 3 (Reverse-oriented - Prior Learning): Let j = p (1 <= p <= {n}), locate the j-th module in the reverse sequence; equivalently the i = N+1-j position forward (N is pre-insertion length, N={n}), and schedule W prior to it (W occupies forward position i).
4. Strategy 4 (Reverse-oriented - Post Learning): Let j = p, locate the j-th module in the reverse sequence; equivalently the i = N+1-j position forward, and schedule W after it (W occupies forward position i+1).

Your task is to figure out the scheduling strategy and insert the core module K so its forward position is exactly {target_pos}.

In at most {max_probe} scheduling probes, each round you can:
1. First execute a trial scheduling command: Insert(W, p), where W is a new module code (no duplicates), and p is an integer (1 to {n}).
2. Then execute one path inspection query (choose only one):
   - Q_A(k): Inspect the module code at the k-th forward position. k ranges from 1 to {n_after}.
   - Q_B(k): Inspect the module code at the k-th reverse position. k ranges from 1 to {n_after}.
   - Q_C(L): Inspect the forward position of module L. L must exist in the path.
   - Q_D(L): Inspect the reverse position of module L. L must exist in the path.
3. After each inspection, the learning path resets to S0.

For each probing round, use the following format:

Trial command:
<insert>W,p</insert>

Inspection query (choose one):
<query_a>k</query_a>
<query_b>k</query_b>
<query_c>L</query_c>
<query_d>L</query_d>

For final submission:
<answer>scheme=X, insert=K,p_final</answer>

Where X is the strategy number (1/2/3/4), K is the core module code, and p_final is the scheduling parameter.

Example:
Probing round:
<insert>W1,3</insert>
<query_a>4</query_a>

Final submission:
<answer>scheme=1, insert=K,2</answer>

Note: Out-of-bounds parameters or code conflicts will result in errors. Ensure each round contains one insertion and one inspection, and submit the strategy number and final command in the answer.
"""

    contextualized_rule_zh_4 = """\
[工业场景]
自动化流水线工序编排校验程序已启动。

生产线控制器内已预载了一个长度为 {n} 的初始装配工序序列 S0 = {seq}，从流水线开端（左）至末端（右）排列，工序位次按 1-based 计算。

PLC底层固化了 4 种隐蔽的工序注入逻辑，系统当前随机锁定了一种并全程生效：
1. 逻辑1（前置基准-工序前插）：令 i = p（1 小于等于 p 小于等于 {n}），在顺推第 i 道工序之前注入新工序 W（W占据顺推位次 i）。
2. 逻辑2（前置基准-工序后插）：令 i = p，在顺推第 i 道工序之后注入 W（W占据顺推位次 i+1）。
3. 逻辑3（末端基准-工序前插）：令 j = p（1 小于等于 p 小于等于 {n}），定位逆推第 j 道工序；等价于顺推第 i = N+1-j 道（N为注入前长度，N={n}），在该工序之前注入 W（W占据顺推位次 i）。
4. 逻辑4（末端基准-工序后插）：令 j = p，定位逆推第 j 道工序；等价于顺推第 i = N+1-j 道，在该工序之后注入 W（W占据顺推位次 i+1）。

你的任务是破解当前 PLC 的注入逻辑，最终配置工序 K，使其顺推位次精准落在第 {target_pos} 号位。

在最多 {max_probe} 轮注入探测中，每轮你可以：
1. 先执行一次试运行注入：Insert(W, p)，其中 W 为新工序代号（不可与序列中已有代号重复），p 为整数（1 到 {n}）。
2. 再执行一次状态反馈查询（仅能选择以下一种）：
   - Q_A(k)：查询顺推第 k 道工序的代号。k 的范围是 1 到 {n_after}。
   - Q_B(k)：查询逆推第 k 道工序的代号。k 的范围是 1 到 {n_after}。
   - Q_C(L)：查询工序 L 的顺推位次。L 必须是已配置的工序。
   - Q_D(L)：查询工序 L 的逆推位次。L 必须是已配置的工序。
3. 每轮查询结束后，流水线序列会自动回滚至 S0。

探测阶段每轮使用以下格式：

注入指令：
<insert>W,p</insert>

状态查询（四选一）：
<query_a>k</query_a>
<query_b>k</query_b>
<query_c>L</query_c>
<query_d>L</query_d>

最终提交答案时：
<answer>scheme=X, insert=K,p_final</answer>

其中 X 为逻辑编号（1/2/3/4），K 为核心工序代号，p_final 为注入参数。

示例：
探测轮次：
<insert>W1,3</insert>
<query_a>4</query_a>

最终提交：
<answer>scheme=1, insert=K,2</answer>

注意：若注入或查询越界、代号冲突，将触发 PLC 报错。请确保每轮包含一次注入和一次查询，最终提交时包含逻辑编号和最终配置指令。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Automated assembly line process scheduling verification initiated.

The production line controller has preloaded an initial assembly process sequence S0 = {seq} of length {n}, arranged from the start (left) to the end (right) of the line, with 1-based position indexing.

The PLC firmware has embedded 4 hidden process injection logics, and the system has currently locked one to remain active throughout:
1. Logic 1 (Front Reference - Process Pre-insertion): Let i = p (1 <= p <= {n}), inject new process W before the i-th process counted forward (W occupies forward position i).
2. Logic 2 (Front Reference - Process Post-insertion): Let i = p, inject W after the i-th process counted forward (W occupies forward position i+1).
3. Logic 3 (End Reference - Process Pre-insertion): Let j = p (1 <= p <= {n}), locate the j-th process counted backward; equivalently the i = N+1-j position forward (N is pre-injection length, N={n}), and inject W before it (W occupies forward position i).
4. Logic 4 (End Reference - Process Post-insertion): Let j = p, locate the j-th process counted backward; equivalently the i = N+1-j position forward, and inject W after it (W occupies forward position i+1).

Your task is to crack the PLC's injection logic and ultimately configure process K so its forward position lands exactly at {target_pos}.

In at most {max_probe} injection probes, each round you can:
1. First execute a trial injection: Insert(W, p), where W is a new process code (must not duplicate existing ones), and p is an integer (1 to {n}).
2. Then execute one state feedback query (choose only one):
   - Q_A(k): Query the process code at the k-th forward position. k ranges from 1 to {n_after}.
   - Q_B(k): Query the process code at the k-th reverse position. k ranges from 1 to {n_after}.
   - Q_C(L): Query the forward position of process L. L must be configured.
   - Q_D(L): Query the reverse position of process L. L must be configured.
3. After each query, the assembly line sequence rolls back to S0.

For each probing round, use the following format:

Injection command:
<insert>W,p</insert>

State query (choose one):
<query_a>k</query_a>
<query_b>k</query_b>
<query_c>L</query_c>
<query_d>L</query_d>

For final submission:
<answer>scheme=X, insert=K,p_final</answer>

Where X is the logic number (1/2/3/4), K is the core process code, and p_final is the parameter.

Example:
Probing round:
<insert>W1,3</insert>
<query_a>4</query_a>

Final submission:
<answer>scheme=1, insert=K,2</answer>

Note: Out-of-bounds actions or code conflicts will trigger a PLC error. Ensure each round contains one injection and one query, and submit the logic number and final command in the answer.
"""

    contextualized_rule_zh_5 = """\
[法律场景]
案件证据链归档校验系统已启动。

当前案卷中有一组长度为 {n} 的初始证据编号序列 S0 = {seq}，按时间溯源逻辑自早到晚（从左到右）排列，归档编号采用 1-based。

归档系统底层执行以下 4 种隐蔽的归卷条款之一，且在查阅期间保持固定：
1. 条款1（正向溯源-先于立卷）：令 i = p（1 小于等于 p 小于等于 {n}），在当前正向第 i 份证据之前归档新证据 W（W占据正向编号 i）。
2. 条款2（正向溯源-后于立卷）：令 i = p，在当前正向第 i 份证据之后归档 W（W占据正向编号 i+1）。
3. 条款3（逆向溯源-先于立卷）：令 j = p（1 小于等于 p 小于等于 {n}），定位逆向第 j 份证据；等价于正向第 i = N+1-j 份（N为立卷前长度，N={n}），在该证据之前归档 W（W占据正向编号 i）。
4. 条款4（逆向溯源-后于立卷）：令 j = p，定位逆向第 j 份证据；等价于正向第 i = N+1-j 份，在该证据之后归档 W（W占据正向编号 i+1）。

你的任务是理清系统的归档条款，并提交核心证据 K，使其最终正好处于正向第 {target_pos} 号位。

在最多 {max_probe} 轮查卷探测中，每轮你可以：
1. 先执行一次模拟归档：Insert(W, p)，其中 W 为新证据代号（不得与已有证据重名），p 为整数（1 到 {n}）。
2. 再执行一次卷宗查询（仅能选择以下一种）：
   - Q_A(k)：查阅正向第 k 号的证据代号。k 的范围是 1 到 {n_after}。
   - Q_B(k)：查阅逆向第 k 号的证据代号。k 的范围是 1 到 {n_after}。
   - Q_C(L)：查询证据 L 的正向编号。L 必须是已入卷的证据。
   - Q_D(L)：查询证据 L 的逆向编号。L 必须是已入卷的证据。
3. 每轮查询结束后，电子卷宗将自动复位至初始排列 S0。

探测阶段每轮使用以下格式：

归档指令：
<insert>W,p</insert>

卷宗查询（四选一）：
<query_a>k</query_a>
<query_b>k</query_b>
<query_c>L</query_c>
<query_d>L</query_d>

最终提交答案时：
<answer>scheme=X, insert=K,p_final</answer>

其中 X 为条款编号（1/2/3/4），K 为核心证据代号，p_final 为归档参数。

示例：
探测轮次：
<insert>W1,3</insert>
<query_a>4</query_a>

最终提交：
<answer>scheme=1, insert=K,2</answer>

注意：若归档或查询越界、代号冲突，将导致卷宗读取错误。请确保每轮包含一次归档和一次查询，最终提交时包含条款编号和最终归档指令。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Case evidence chain archiving verification system initiated.

The dossier currently holds an initial sequence of evidence codes S0 = {seq} of length {n}, ordered chronologically from earliest to latest (left to right), with 1-based filing numbers.

The archiving system executes one of the following 4 hidden filing clauses, which remains fixed during the review:
1. Clause 1 (Forward Tracing - Pre-filing): Let i = p (1 <= p <= {n}), file the new evidence W before the i-th evidence counted forward (W occupies forward number i).
2. Clause 2 (Forward Tracing - Post-filing): Let i = p, file W after the i-th evidence counted forward (W occupies forward number i+1).
3. Clause 3 (Reverse Tracing - Pre-filing): Let j = p (1 <= p <= {n}), locate the j-th evidence counted backward; equivalently the i = N+1-j position forward (N is pre-filing length, N={n}), and file W before it (W occupies forward number i).
4. Clause 4 (Reverse Tracing - Post-filing): Let j = p, locate the j-th evidence counted backward; equivalently the i = N+1-j position forward, and file W after it (W occupies forward number i+1).

Your task is to clarify the archiving clause and submit the core evidence K so it ultimately holds the exact forward number {target_pos}.

In at most {max_probe} probing rounds, each round you can:
1. First execute a mock filing: Insert(W, p), where W is a new evidence code (no duplicates), and p is an integer (1 to {n}).
2. Then execute one dossier query (choose only one):
   - Q_A(k): Review the evidence code at forward number k. k ranges from 1 to {n_after}.
   - Q_B(k): Review the evidence code at reverse number k. k ranges from 1 to {n_after}.
   - Q_C(L): Query the forward number of evidence L. L must exist in the dossier.
   - Q_D(L): Query the reverse number of evidence L. L must exist in the dossier.
3. After each query, the electronic dossier automatically resets to initial arrangement S0.

For each probing round, use the following format:

Filing command:
<insert>W,p</insert>

Dossier query (choose one):
<query_a>k</query_a>
<query_b>k</query_b>
<query_c>L</query_c>
<query_d>L</query_d>

For final submission:
<answer>scheme=X, insert=K,p_final</answer>

Where X is the clause number (1/2/3/4), K is the core evidence code, and p_final is the parameter.

Example:
Probing round:
<insert>W1,3</insert>
<query_a>4</query_a>

Final submission:
<answer>scheme=1, insert=K,2</answer>

Note: Out-of-bounds parameters or code conflicts will result in a dossier reading error. Ensure one filing and one query per round, and submit the clause number and final command in the answer.
"""

    user_prompt_zh = "你可以开始第一轮探测了。"
    user_prompt_en = "You can start your first probing round now."

    tags = ["answer", "insert", "query_a", "query_b", "query_c", "query_d"]

    reasoning_type = "溯因推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "seq": "(A, B, C, D)",
                "scheme": 1,
                "target_pos": 2,
                "max_probe": 2,
            },
            2: {
                "n": 5,
                "seq": "(A, B, C, D, E)",
                "scheme": 2,
                "target_pos": 3,
                "max_probe": 2,
            },
            3: {
                "n": 6,
                "seq": "(A, B, C, D, E, F)",
                "scheme": 3,
                "target_pos": 4,
                "max_probe": 3,
            },
            4: {
                "n": 7,
                "seq": "(A, B, C, D, E, F, G)",
                "scheme": 4,
                "target_pos": 5,
                "max_probe": 3,
            },
            5: {
                "n": 8,
                "seq": "(A, B, C, D, E, F, G, H)",
                "scheme": 1,
                "target_pos": 4,
                "max_probe": 3,
            },
        },
        "en": {
            1: {
                "n": 4,
                "seq": "(A, B, C, D)",
                "scheme": 1,
                "target_pos": 2,
                "max_probe": 2,
            },
            2: {
                "n": 5,
                "seq": "(A, B, C, D, E)",
                "scheme": 2,
                "target_pos": 3,
                "max_probe": 2,
            },
            3: {
                "n": 6,
                "seq": "(A, B, C, D, E, F)",
                "scheme": 3,
                "target_pos": 4,
                "max_probe": 3,
            },
            4: {
                "n": 7,
                "seq": "(A, B, C, D, E, F, G)",
                "scheme": 4,
                "target_pos": 5,
                "max_probe": 3,
            },
            5: {
                "n": 8,
                "seq": "(A, B, C, D, E, F, G, H)",
                "scheme": 1,
                "target_pos": 4,
                "max_probe": 3,
            },
        },
    }

    def __init__(self, config):
        self.probe_count = 0
        self.current_seq = []
        self.used_labels = set()
        self.last_insert = None
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
        self._game_info["seq"] = cfg["seq"]
        self._game_info["target_pos"] = cfg["target_pos"]
        self._game_info["max_probe"] = cfg["max_probe"]
        self._game_info["n_after"] = cfg["n"] + 1

        self.scheme = cfg["scheme"]
        self.target_pos = cfg["target_pos"]
        self.max_probe = cfg["max_probe"]
        self.n = cfg["n"]

        seq_str = cfg["seq"].strip("()")
        self.initial_seq = [label.strip() for label in seq_str.split(",")]
        self.current_seq = self.initial_seq.copy()
        self.used_labels = set(self.initial_seq)

    def _reset_sequence(self):
        self.current_seq = self.initial_seq.copy()

    def _apply_insertion(self, label, p):
        n = len(self.current_seq)
        
        if self.scheme == 1:
            insert_pos = p - 1
        elif self.scheme == 2:
            insert_pos = p
        elif self.scheme == 3:
            left_equivalent = n + 1 - p
            insert_pos = left_equivalent - 1
        elif self.scheme == 4:
            left_equivalent = n + 1 - p
            insert_pos = left_equivalent
        else:
            raise ValueError(f"Unknown scheme: {self.scheme}")

        self.current_seq.insert(insert_pos, label)
        return insert_pos + 1

    def _execute_query(self, parsed_info):
        n_current = len(self.current_seq)
        
        if "query_a" in parsed_info:
            try:
                k = int(parsed_info["query_a"].strip())
                if k < 1 or k > n_current:
                    return self._error_msg("query_a_range")
                label = self.current_seq[k - 1]
                if self.config.language == "zh":
                    return f"左端第{k}位：{label}"
                else:
                    return f"Left position {k}: {label}"
            except ValueError:
                return self._error_msg("query_a_format")
                
        elif "query_b" in parsed_info:
            try:
                k = int(parsed_info["query_b"].strip())
                if k < 1 or k > n_current:
                    return self._error_msg("query_b_range")
                label = self.current_seq[n_current - k]
                if self.config.language == "zh":
                    return f"右端第{k}位：{label}"
                else:
                    return f"Right position {k}: {label}"
            except ValueError:
                return self._error_msg("query_b_format")
                
        elif "query_c" in parsed_info:
            label = parsed_info["query_c"].strip()
            if label not in self.current_seq:
                return self._error_msg("label_not_found")
            pos = self.current_seq.index(label) + 1
            if self.config.language == "zh":
                return f"标签{label}左端位次：{pos}"
            else:
                return f"Label {label} left position: {pos}"
                
        elif "query_d" in parsed_info:
            label = parsed_info["query_d"].strip()
            if label not in self.current_seq:
                return self._error_msg("label_not_found")
            pos = self.current_seq.index(label) + 1
            right_pos = n_current - pos + 1
            if self.config.language == "zh":
                return f"标签{label}右端位次：{right_pos}"
            else:
                return f"Label {label} right position: {right_pos}"
        else:
            return self._error_msg("no_query")

    def _error_msg(self, error_type):
        error_msgs = {
            "zh": {
                "insert_format": "无效指令：插入格式错误，应为 <insert>标签,参数</insert>",
                "insert_range": f"无效指令：插入参数超出范围，应在 1 到 {self.n} 之间",
                "label_conflict": "无效指令：标签已存在，请使用不同的标签",
                "query_a_format": "无效指令：查询格式错误",
                "query_a_range": f"无效指令：查询位置超出范围，应在 1 到 {len(self.current_seq)} 之间",
                "query_b_format": "无效指令：查询格式错误",
                "query_b_range": f"无效指令：查询位置超出范围，应在 1 到 {len(self.current_seq)} 之间",
                "label_not_found": "无效指令：标签不存在于当前序列中",
                "no_query": "无效指令：未找到有效的查询指令",
                "no_insert": "无效指令：本轮缺少插入指令",
                "max_probe_reached": f"已达到最大探测轮次（{self.max_probe}轮），请提交最终答案",
            },
            "en": {
                "insert_format": "Invalid instruction: Insertion format error, should be <insert>label,parameter</insert>",
                "insert_range": f"Invalid instruction: Insertion parameter out of range, should be between 1 and {self.n}",
                "label_conflict": "Invalid instruction: Label already exists, please use a different label",
                "query_a_format": "Invalid instruction: Query format error",
                "query_a_range": f"Invalid instruction: Query position out of range, should be between 1 and {len(self.current_seq)}",
                "query_b_format": "Invalid instruction: Query format error",
                "query_b_range": f"Invalid instruction: Query position out of range, should be between 1 and {len(self.current_seq)}",
                "label_not_found": "Invalid instruction: Label does not exist in current sequence",
                "no_query": "Invalid instruction: No valid query instruction found",
                "no_insert": "Invalid instruction: Missing insertion instruction for this round",
                "max_probe_reached": f"Maximum probing rounds reached ({self.max_probe} rounds), please submit final answer",
            }
        }
        return error_msgs[self.config.language][error_type]

    def evaluate(self, parsed_info):
        raw_ans = parsed_info.get("answer", "")
        
        scheme_match = re.search(r'scheme\s*=\s*(\d+)', raw_ans, re.IGNORECASE)
        insert_match = re.search(r'insert\s*=\s*([^,]+),\s*(\d+)', raw_ans, re.IGNORECASE)
        
        if not scheme_match or not insert_match:
            return False
        
        try:
            guessed_scheme = int(scheme_match.group(1))
            final_label = insert_match.group(1).strip()
            final_p = int(insert_match.group(2))
        except:
            return False
        
        if guessed_scheme != self.scheme:
            return False
        
        if final_p < 1 or final_p > self.n:
            return False
        
        if final_label in self.initial_seq:
            return False
        
        self._reset_sequence()
        final_pos = self._apply_insertion(final_label, final_p)
        
        return final_pos == self.target_pos

    def _cf_core_produce(self, parsed_info):
        if self.probe_count >= self.max_probe:
            self.over_probe_attempts = getattr(self, 'over_probe_attempts', 0) + 1
            if self.over_probe_attempts >= 3:
                raise Exception("Exceeded max probe attempts without submitting final answer.")
            return self._error_msg("max_probe_reached")
        
        if "insert" not in parsed_info:
            return self._error_msg("no_insert")
            
        has_query = any(k in parsed_info for k in ["query_a", "query_b", "query_c", "query_d"])
        if not has_query:
            return self._error_msg("no_query")
        
        try:
            insert_parts = parsed_info["insert"].split(",")
            if len(insert_parts) != 2:
                return self._error_msg("insert_format")
            
            label = insert_parts[0].strip()
            p = int(insert_parts[1].strip())
            
            if p < 1 or p > self.n:
                return self._error_msg("insert_range")
            
            if label in self.used_labels:
                return self._error_msg("label_conflict")
            
        except (ValueError, IndexError):
            return self._error_msg("insert_format")
        
        self.used_labels.add(label)
        
        self._reset_sequence()
        insert_pos = self._apply_insertion(label, p)
        self.last_insert = (label, p, insert_pos)
        
        query_response = self._execute_query(parsed_info)
        
        self._reset_sequence()
        
        self.probe_count += 1
        
        return query_response

    def _cf_make_wrong(self, correct: str) -> str:
        if "：" in correct:
            prefix, val = correct.rsplit("：", 1)
            sep = "："
        elif ":" in correct:
            prefix, val = correct.rsplit(":", 1)
            val = val.strip()
            sep = ": "
        else:
            return correct + "_WRONG"

        try:
            num = int(val)
            new_val = str(num + 1 if num < self.n else num - 1)
            if new_val == "0":
                new_val = "2"
            return f"{prefix}{sep}{new_val}"
        except ValueError:
            return f"{prefix}{sep}{val}_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        original_seq_backup = self.current_seq.copy()
        original_used_labels_backup = self.used_labels.copy()
        
        test_label = "TEST"
        while test_label in self.initial_seq:
            test_label += "_X"
            
        n = self.n
        
        for p in range(1, n + 1):
            self._reset_sequence()
            self._apply_insertion(test_label, p)
            
            n_after = len(self.current_seq)
            current_labels = self.current_seq.copy()
            
            insert_cmd_str = f"<insert>{test_label},{p}</insert>"
            
            for k in range(1, n_after + 1):
                query_str = f"{insert_cmd_str}\n<query_a>{k}</query_a>"
                parsed_info = {"query_a": str(k)}
                answer = self._execute_query(parsed_info)
                results.append({"query": query_str, "answer": answer})
                
            for k in range(1, n_after + 1):
                query_str = f"{insert_cmd_str}\n<query_b>{k}</query_b>"
                parsed_info = {"query_b": str(k)}
                answer = self._execute_query(parsed_info)
                results.append({"query": query_str, "answer": answer})
                
            for label in current_labels:
                query_str = f"{insert_cmd_str}\n<query_c>{label}</query_c>"
                parsed_info = {"query_c": label}
                answer = self._execute_query(parsed_info)
                results.append({"query": query_str, "answer": answer})
                
            for label in current_labels:
                query_str = f"{insert_cmd_str}\n<query_d>{label}</query_d>"
                parsed_info = {"query_d": label}
                answer = self._execute_query(parsed_info)
                results.append({"query": query_str, "answer": answer})

        self.current_seq = original_seq_backup
        self.used_labels = original_used_labels_backup
        
        return results