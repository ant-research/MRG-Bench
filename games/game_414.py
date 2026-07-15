import re
from .base import Game

class LawOfCountsGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "集合"

    game_rule_zh = """\
我们现在来玩一个"符印律法"的推理游戏，规则如下：

游戏设定了一个包含四类标签的多重集合，四类标签分别记作 L1、L2、L3、L4。初始状态下，这四类标签的数量分别为 c1={c1}、c2={c2}、c3={c3}、c4={c4}，总共 N={n} 个标签。

我已经秘密选定了一个"通过数"计算函数（称为"律法"），并在整个游戏过程中保持不变。这个函数会根据当前四类标签的数量 (c1, c2, c3, c4)计算出一个整数，范围在 0 到 {n} 之间。

你的目标分为两个阶段：
1. **第一阶段**：通过反复查询和操作，推断出我使用的是哪一种"律法"（有四种候选律法：A、B、C、D）。
2. **第二阶段**：在"最终挑战"中，从初始状态出发，通过有限次数的操作，使得通过数恰好等于 {target}。

在第一阶段，你可以反复执行以下操作（每次一个）：

1. **查询通过数**：询问当前状态下的通过数是多少。我会返回一个整数。
   格式：
   <query_pass></query_pass>

2. **查询当前计数**：询问当前四类标签的数量。我会返回 (c1, c2, c3, c4)。
   格式：
   <query_count></query_count>

3. **重铸操作**：选择一类标签 i 和另一类标签 j（i 不等于 j），将一个 Li 标签替换为 Lj 标签。要求当前 ci 大于 0。执行后状态更新为 ci 减 1，cj 加 1。
   格式（例如将 L1 重铸为 L3）：
   <recast>1,3</recast>

4. **重置状态**：将状态恢复到初始值 ({c1}, {c2}, {c3}, {c4})。
   格式：
   <reset></reset>

5. **宣告律法**：当你认为已经推断出正确的律法时，提交你的答案（A、B、C 或 D）。
   格式：
   <declare>A</declare>
   注意：如果宣告错误，游戏立即失败；如果宣告正确，你可以选择继续试验或开始最终挑战。

当你成功宣告正确的律法后，你可以开始最终挑战：

6. **开始最终挑战**：从初始状态 ({c1}, {c2}, {c3}, {c4}) 开始，你有有限次重铸机会，目标是使通过数恰好等于 {target}。
   格式：
   <start_challenge></start_challenge>

   在挑战过程中，你只能使用重铸操作（格式同上）。每次重铸后，我会告诉你剩余次数和当前通过数。当通过数达到 {target} 时，你获得胜利；如果次数用尽仍未达成，则游戏失败。

- 正确宣告律法，并在最终挑战中达成通过数等于 {target}。

- 宣告律法错误。
- 最终挑战中次数用尽仍未达成目标。
- 多次执行不合法的操作。

现在开始你的推理吧！
"""

    game_rule_en = """\
Let's play a "Law of Counts" deduction game. Here are the rules:

The game has a multiset containing four types of tags: L1, L2, L3, L4. Initially, the counts are c1={c1}, c2={c2}, c3={c3}, c4={c4}, totaling N={n} tags.

I have secretly chosen a "pass number" calculation function (called the "Law"), which remains fixed throughout the game. This function computes an integer from the current counts (c1, c2, c3, c4), ranging from 0 to {n}.

Your goal has two phases:
1. **Phase One**: Through repeated queries and operations, deduce which "Law" I am using (there are four candidate laws: A, B, C, D).
2. **Phase Two**: In the "Final Challenge", starting from the initial state, achieve a pass number of exactly {target} within a limited number of operations.

In Phase One, you can repeatedly perform the following operations (one at a time):

1. **Query Pass Number**: Ask for the current pass number. I will return an integer.
   Format:
   <query_pass></query_pass>

2. **Query Current Counts**: Ask for the current counts of the four tag types. I will return (c1, c2, c3, c4).
   Format:
   <query_count></query_count>

3. **Recast Operation**: Choose tag type i and another type j (i not equal to j), replacing one Li tag with an Lj tag. Requires ci greater than 0. After execution, ci decreases by 1 and cj increases by 1.
   Format (e.g., recasting L1 to L3):
   <recast>1,3</recast>

4. **Reset State**: Restore the state to initial values ({c1}, {c2}, {c3}, {c4}).
   Format:
   <reset></reset>

5. **Declare Law**: When you believe you have deduced the correct law, submit your answer (A, B, C, or D).
   Format:
   <declare>A</declare>
   Note: If the declaration is incorrect, the game immediately fails; if correct, you may continue experimenting or start the final challenge.

After successfully declaring the correct law, you can start the final challenge:

6. **Start Final Challenge**: Starting from initial state ({c1}, {c2}, {c3}, {c4}), you have a limited number of recast opportunities to achieve a pass number of exactly {target}.
   Format:
   <start_challenge></start_challenge>

   During the challenge, you can only use recast operations (format as above). After each recast, I will tell you the remaining attempts and current pass number. When the pass number reaches {target}, you win; if attempts are exhausted without achieving the goal, the game fails.

- Correctly declare the law and achieve pass number equal to {target} in the final challenge.

- Incorrect law declaration.
- Attempts exhausted in final challenge without achieving the goal.
- Repeatedly executing illegal operations.

Begin your deduction now!
"""

    contextualized_rule_zh_1 = """\
欢迎接入【智能交通路网调度系统】。

我们正在进行一次交通流量管控演练。路网中存在四类车队资源，分别记作 L1（小型客车）、L2（大型客车）、L3（轻型货车）、L4（重型货车）。当前状态下，各类车辆的数量分别为 c1={c1}、c2={c2}、c3={c3}、c4={c4}，车队总规模 N={n}。

系统内置了一个秘密的“路网通行指标”计算法则。该法则在演练期间保持不变，会根据当前各类车辆的分布 (c1, c2, c3, c4) 实时评估出一个介于 0 到 {n} 之间的整数。

你的任务分为两个阶段：
1. **第一阶段**：通过查询和试探性调度，反向推导系统正在使用的指标计算法则（候选项为 A、B、C、D 方案）。
2. **第二阶段**：在“极限保通挑战”中，从初始状态出发，经过有限次数的车辆转换调度，使得路网通行指标精准达到 {target}。

在第一阶段，你可以反复下达以下操作指令（每次单发）：

1. **查询通行指标**：评估当前路网的通行指标。
   格式：
   <query_pass></query_pass>

2. **查询车队结构**：获取当前路网的车辆分布情况 (c1, c2, c3, c4)。
   格式：
   <query_count></query_count>

3. **车辆改装/调度重分配**：将一辆 Li 类车转换为 Lj 类车（i 与 j 不同）。要求 Li 当前数量大于 0。执行后，ci 减 1，cj 加 1。
   格式（如将 L1 转换为 L3）：
   <recast>1,3</recast>

4. **重置路网**：将路网车辆分布重置为初始配置 ({c1}, {c2}, {c3}, {c4})。
   格式：
   <reset></reset>

5. **宣告推导结论**：当你确认系统采用的法则时，提交你的答案（A、B、C 或 D）。
   格式：
   <declare>A</declare>
   注意：一旦推测错误，演练立即终止；宣告正确后，可继续测试或直接开启最终挑战。

准确推导出法则后，你可以开启挑战模式：

6. **开始最终挑战**：从初始配置 ({c1}, {c2}, {c3}, {c4}) 重新启动路网，你拥有有限次的调度权限，目标是让通行指标恰好等于 {target}。
   格式：
   <start_challenge></start_challenge>

   在挑战中，仅允许执行“车辆改装/调度重分配”（格式同上）。每次操作后系统将返回剩余权限次数及最新指标。指标达到 {target} 即为演练成功；权限耗尽未达标则演练失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the [Smart Traffic Road Network Dispatch System].

We are conducting a traffic flow control simulation. The network consists of four types of vehicle fleets: L1 (Compact Cars), L2 (Large Buses), L3 (Light Trucks), and L4 (Heavy Trucks). Initially, their distributions are c1={c1}, c2={c2}, c3={c3}, and c4={c4}, with a total fleet size of N={n}.

The system incorporates a hidden "Network Throughput Metric" evaluation rule. This rule remains constant during the simulation, calculating an integer between 0 and {n} based on the real-time vehicle distribution (c1, c2, c3, c4).

Your operational mission has two phases:
1. **Phase One**: Through continuous querying and dispatching, deduce which metric rule the system is applying (Candidates: A, B, C, D).
2. **Phase Two**: Enter the "Extreme Flow Challenge". Starting from the initial distribution, perform limited vehicle dispatches to make the throughput metric exactly hit {target}.

In Phase One, you can issue the following commands repeatedly (one at a time):

1. **Query Throughput**: Assess the current network throughput metric.
   Format: <query_pass></query_pass>

2. **Query Fleet Distribution**: Retrieve the current vehicle distribution (c1, c2, c3, c4).
   Format: <query_count></query_count>

3. **Vehicle Retrofit/Redispatch**: Reassign one Li vehicle to function as an Lj vehicle (i != j). Requires ci to be greater than 0. Upon execution, ci decreases by 1, and cj increases by 1.
   Format (e.g., redispatching L1 to L3): <recast>1,3</recast>

4. **Reset Network**: Restore the vehicle distribution to the baseline state ({c1}, {c2}, {c3}, {c4}).
   Format: <reset></reset>

5. **Declare Rule**: Submit your conclusion once you have identified the system's operational rule (A, B, C, or D).
   Format: <declare>A</declare>
   Note: An incorrect declaration terminates the simulation. A correct one allows you to proceed to the final challenge.

After deducing the rule, you can initiate the final mode:

6. **Start Final Challenge**: Resetting to ({c1}, {c2}, {c3}, {c4}), use limited redispatch operations to force the throughput metric to perfectly align with {target}.
   Format: <start_challenge></start_challenge>

   Only the "Vehicle Retrofit/Redispatch" command is permitted. Each operation returns your remaining attempts and the latest throughput. Hitting {target} results in a successful dispatch operation; exhausting attempts without success means failure.
"""

    contextualized_rule_zh_2 = """\
欢迎进入【靶向免疫治疗临床推演平台】。

本试验针对某种罕见病变，使用四类核心免疫因子进行联合治疗，代号分别为 L1（α细胞）、L2（β细胞）、L3（γ细胞）、L4（δ细胞）。初始时刻，四种因子的滴度分别为 c1={c1}、c2={c2}、c3={c3}、c4={c4}，系统总滴度 N={n}。

医学模型中预设了一个隐秘的“免疫应答指数”评估机制。该机制贯穿本次推演，依据当前的因子滴度分布 (c1, c2, c3, c4)，计算出一个介于 0 到 {n} 之间的整数量化数值。

你的临床任务分为两个阶段：
1. **第一阶段**：通过不断采样和细胞诱导，推断出患者体内的应答机制属于哪一种预定分型（候选分型：A、B、C、D）。
2. **第二阶段**：进入“精准靶向挑战”，从初始滴度出发，利用有限的诱导操作，使免疫应答指数刚好达到治愈临界值 {target}。

在第一阶段，你可单次执行以下操作：

1. **测定应答指数**：获取当前的免疫应答指数。
   格式：<query_pass></query_pass>

2. **化验因子滴度**：获取当前四类免疫因子的滴度 (c1, c2, c3, c4)。
   格式：<query_count></query_count>

3. **细胞诱导转化**：选择一类因子 i 与目标因子 j（i 不等于 j），通过酶促反应将一个 Li 因子转化为 Lj 因子。前提是 ci 大于 0。转化后 ci 减 1，cj 加 1。
   格式（如将 L1 诱导为 L3）：<recast>1,3</recast>

4. **洗脱重置**：将系统环境还原为初始状态 ({c1}, {c2}, {c3}, {c4})。
   格式：<reset></reset>

5. **宣告应答机制**：确诊你认为的机制分型（A、B、C 或 D）。
   格式：<declare>A</declare>
   注意：误诊将导致推演中止；确诊正确则可选择继续观察或开启靶向挑战。

成功确诊机制后，可开启该挑战：

6. **开始最终挑战**：将系统还原至初始状态 ({c1}, {c2}, {c3}, {c4})。利用有限的细胞转化次数，将免疫应答指数精准调控至 {target}。
   格式：<start_challenge></start_challenge>

   挑战期间，只能进行“细胞诱导转化”。每次操作后，设备会提示剩余转化次数与当前应答指数。若指数达到 {target} 则患者痊愈；若耗尽次数未达标则推演失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the [Targeted Immunotherapy Clinical Deduction Platform].

This trial focuses on treating a rare pathology using four core immune factors, designated L1 (Alpha Cells), L2 (Beta Cells), L3 (Gamma Cells), and L4 (Delta Cells). Initially, the factor titers are c1={c1}, c2={c2}, c3={c3}, and c4={c4}, with a total systemic titer of N={n}.

The clinical model contains a concealed "Immune Response Index" mechanism. This mechanism remains fixed throughout the deduction, computing an integer between 0 and {n} derived from the current titer distribution (c1, c2, c3, c4).

Your clinical task involves two phases:
1. **Phase One**: Through sampling and cell induction, diagnose the specific response mechanism type present in the patient (Candidates: A, B, C, D).
2. **Phase Two**: Proceed to the "Precision Targeting Challenge". Starting from baseline, utilize limited induction interventions to calibrate the immune response exactly to the curative threshold of {target}.

In Phase One, you may execute the following:

1. **Assay Response Index**: Obtain the current immune response index.
   Format: <query_pass></query_pass>

2. **Profile Factor Titers**: Check the distribution of the four immune factors (c1, c2, c3, c4).
   Format: <query_count></query_count>

3. **Cell Induction**: Catalyze the transformation of one Li factor into an Lj factor (i != j). ci must be strictly greater than 0. After conversion, ci is reduced by 1, and cj increased by 1.
   Format (e.g., inducing L1 into L3): <recast>1,3</recast>

4. **Washout and Reset**: Revert the systemic environment back to its initial state ({c1}, {c2}, {c3}, {c4}).
   Format: <reset></reset>

5. **Declare Mechanism**: Finalize your diagnosis of the underlying mechanism (A, B, C, or D).
   Format: <declare>A</declare>
   Note: A misdiagnosis immediately ends the trial. A correct diagnosis unlocks the targeted challenge.

Available upon successful diagnosis:

6. **Start Final Challenge**: Reverting to baseline ({c1}, {c2}, {c3}, {c4}), you must accurately modulate the immune response to {target} within a strict limit of induction procedures.
   Format: <start_challenge></start_challenge>

   During this phase, only "Cell Induction" is authorized. After each step, the console will display the remaining attempts and the current index. Reaching {target} cures the patient; exhausting attempts results in clinical failure.
"""

    contextualized_rule_zh_3 = """\
欢迎访问【自适应课程图谱规划系统】。

我们正在为一个新学期制定模块化教学计划。共有四类教学模块，分别为 L1（理论讲授）、L2（实验实操）、L3（研讨工作坊）、L4（结课项目）。初始课时安排为 c1={c1}、c2={c2}、c3={c3}、c4={c4}，总课时数 N={n}。

教育评测引擎中设定了一个“综合素养达标值”计算模型（保持未知且恒定）。该模型会依据当前的课时结构 (c1, c2, c3, c4) 评测出一个 0 到 {n} 之间的素养量化分数。

你的教务规划任务分为两步：
1. **第一阶段**：通过动态调整课时和查询反馈，识别出引擎采用的是哪一种评测模型（候选方案：A、B、C、D）。
2. **第二阶段**：在“核心教改挑战”中，从基础课时出发，经过限定次数的课程置换，使综合素养达标值准确对齐目标分数 {target}。

第一阶段中，你可随时执行下列指令（每次一项）：

1. **查询达标值**：评估当前课程结构的综合素养得分。
   格式：<query_pass></query_pass>

2. **查询课时分布**：读取当前的模块课时分配 (c1, c2, c3, c4)。
   格式：<query_count></query_count>

3. **课时置换**：将一个单位的 Li 模块替换为 Lj 模块（i 不等于 j）。需确保当前 ci 大于 0。调整后 ci 减少 1，cj 增加 1。
   格式（例如将 L1 置换为 L3）：<recast>1,3</recast>

4. **恢复大纲**：将课表重置为初始配置 ({c1}, {c2}, {c3}, {c4})。
   格式：<reset></reset>

5. **宣告评测模型**：当你确定引擎正在使用的模型时，提交你的判定（A、B、C 或 D）。
   格式：<declare>A</declare>
   注意：判定错误会导致系统锁定；判定正确即可开启最终教改挑战。

正确判定模型后可进入此阶段：

6. **开始最终挑战**：基于初始大纲 ({c1}, {c2}, {c3}, {c4})，在有限的置换次数内，调配课程以使得达标值精确等于 {target}。
   格式：<start_challenge></start_challenge>

   此阶段仅限执行“课时置换”操作。系统会实时返回剩余置换次数及当下达标值。分数值达标即算教改成功；次数用尽仍未达标则改革失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the [Adaptive Curriculum Mapping System].

We are structuring modular instructional plans for the upcoming semester. There are four teaching modules: L1 (Theoretical Lectures), L2 (Practical Labs), L3 (Discussion Workshops), and L4 (Capstone Projects). The initial credit hours are c1={c1}, c2={c2}, c3={c3}, and c4={c4}, totaling N={n} hours.

The academic evaluation engine uses an undisclosed "Comprehensive Competency Score" model. This model stays fixed and calculates an integer score ranging from 0 to {n} based on the prevailing module allocation (c1, c2, c3, c4).

Your academic planning task is split into two phases:
1. **Phase One**: By adjusting allocations and requesting feedback, identify the evaluation model implemented by the engine (Options: A, B, C, D).
2. **Phase Two**: In the "Core Reform Challenge", start from the base curriculum and perform a limited number of module substitutions to perfectly match the target competency score of {target}.

During Phase One, you may use these commands iteratively:

1. **Query Competency Score**: Retrieve the current comprehensive competency assessment.
   Format: <query_pass></query_pass>

2. **Query Hour Distribution**: View the current hour allocation across the four modules (c1, c2, c3, c4).
   Format: <query_count></query_count>

3. **Module Substitution**: Replace one unit of module Li with module Lj (i != j). Ensure ci > 0. Once replaced, ci drops by 1 and cj rises by 1.
   Format (e.g., replacing L1 with L3): <recast>1,3</recast>

4. **Restore Syllabus**: Revert the timetable to its default state ({c1}, {c2}, {c3}, {c4}).
   Format: <reset></reset>

5. **Declare Evaluation Model**: Submit your judgment once you ascertain the active model (A, B, C, or D).
   Format: <declare>A</declare>
   Note: An incorrect submission locks the system. A correct identification grants access to the educational reform challenge.

Unlocked after correctly identifying the model:

6. **Start Final Challenge**: Beginning from the baseline syllabus ({c1}, {c2}, {c3}, {c4}), use a strictly limited number of substitutions to calibrate the competency score exactly to {target}.
   Format: <start_challenge></start_challenge>

   Only "Module Substitution" is available here. The system updates your remaining quota and the current score after every move. Hitting {target} completes the curriculum reform; running out of quota triggers a failure.
"""

    contextualized_rule_zh_4 = """\
欢迎进入【高分子材料应力测试实验室】。

本次实验聚焦一种高精合金的配方改良。配方包含四类稀有添加剂，记作 L1（α态钛）、L2（β态钛）、L3（碳纳米管）、L4（石墨烯）。当前配方中四种添加剂的计量分别为 c1={c1}、c2={c2}、c3={c3}、c4={c4}，总计量 N={n}。

工艺质检台内隐匿了一种“结构抗压指数”的验算方程。在整个研发周期内，方程始终如一，它会根据现有的添加剂配比 (c1, c2, c3, c4) 计算出 0 至 {n} 范围内的抗压数值。

你的研发使命有两个阶段：
1. **第一阶段**：通过微调试制与数据读取，逆向破解质检台使用的验算方程（候选方程为：A、B、C、D）。
2. **第二阶段**：在“极限试产挑战”中，从原配方出发，利用有限的催化置换步骤，使最终配方的抗压指数完美契合工程标准 {target}。

在逆向破解阶段，你可以反复执行下述操作：

1. **测定抗压指数**：获取当前配方的抗压测试反馈。
   格式：<query_pass></query_pass>

2. **读取配方计量**：查看当前各类添加剂的成分计量 (c1, c2, c3, c4)。
   格式：<query_count></query_count>

3. **催化置换**：选取添加剂 i 与 j（i 不等于 j），通过催化作用将一个单位的 Li 转化为 Lj。要求当前 ci 大于 0。反应后 ci 减 1，cj 加 1。
   格式（如将 L1 转化为 L3）：<recast>1,3</recast>

4. **配方重置**：将反应釜清洗并复原至初始配方 ({c1}, {c2}, {c3}, {c4})。
   格式：<reset></reset>

5. **宣告验算方程**：确认已破解出对应的方程模型后进行提交（A、B、C 或 D）。
   格式：<declare>A</declare>
   注意：如果宣告错误，批次立即报废；宣告正确，你可以继续微调试制或启动极限挑战。

成功破解方程后，可接入此生产线：

6. **开始最终挑战**：从基础配方 ({c1}, {c2}, {c3}, {c4}) 重启设备，在受限的置换次数内，将抗压指数精确调整至目标值 {target}。
   格式：<start_challenge></start_challenge>

   在此模式中，只允许进行“催化置换”。每次置换后会更新剩余操作步数及最新抗压指数。达标即研制成功；步数耗尽未达标则宣告试产失败。
"""

    contextualized_rule_en_4 = """\
[Industrial Scenario]
Welcome to the [Polymer Material Stress Testing Laboratory].

This session focuses on refining a high-precision alloy formula. The formula comprises four rare additives: L1 (Alpha-Titanium), L2 (Beta-Titanium), L3 (Carbon Nanotubes), and L4 (Graphene). The current dosage of each additive is c1={c1}, c2={c2}, c3={c3}, and c4={c4}, with a total dosage of N={n}.

The quality inspection console relies on a proprietary "Structural Stress Tolerance" formula. This formula remains strictly unchanged during testing, returning an integer yield metric between 0 and {n} based on the real-time additive ratio (c1, c2, c3, c4).

Your R&D mission progresses in two phases:
1. **Phase One**: By iteratively adjusting dosages and reading stress feedback, reverse-engineer the hidden testing formula (Candidates: A, B, C, D).
2. **Phase Two**: In the "Limit Production Challenge", begin with the original formula and execute limited catalytic replacements to align the stress tolerance exactly with the engineering standard of {target}.

In Phase One, you can run the following operations:

1. **Measure Stress Tolerance**: Fetch the current formula's stress test feedback.
   Format: <query_pass></query_pass>

2. **Read Additive Dosages**: Check the compositional metrics of the additives (c1, c2, c3, c4).
   Format: <query_count></query_count>

3. **Catalytic Replacement**: Use a catalyst to transmute one unit of Li into Lj (i != j). ci must be greater than 0. Post-reaction, ci decreases by 1, and cj increases by 1.
   Format (e.g., transmuting L1 into L3): <recast>1,3</recast>

4. **Reset Formula**: Flush the reactor and restore the base composition ({c1}, {c2}, {c3}, {c4}).
   Format: <reset></reset>

5. **Declare Formula**: Confirm and submit the reverse-engineered mathematical model (A, B, C, or D).
   Format: <declare>A</declare>
   Note: A wrong declaration scraps the batch immediately. A correct one permits you to initiate the limit challenge.

Activated after successfully reverse-engineering the formula:

6. **Start Final Challenge**: From the default composition ({c1}, {c2}, {c3}, {c4}), precisely tweak the formula within a constrained number of replacement steps to achieve the exact target tolerance of {target}.
   Format: <start_challenge></start_challenge>

   Only "Catalytic Replacement" can be used. Each reaction updates the remaining step count and the latest stress reading. Reaching the exact target means trial success; depleting your steps results in a production failure.
"""

    contextualized_rule_zh_5 = """\
欢迎登入【数字化庭审证据博弈系统】。

我们正在复盘一场复杂的商业诉讼。目前的证据链由四类卷宗构成：L1（直接物证）、L2（间接物证）、L3（鉴定意见）、L4（证人证言）。初始状态下，这四类卷宗的件数分别为 c1={c1}、c2={c2}、c3={c3}、c4={c4}，总证据量 N={n}。

合议庭有一套不公开的“证据效力指数”采信标准（在本次复盘中保持绝对固定）。该标准根据证据组合 (c1, c2, c3, c4) 综合换算出一个 0 到 {n} 之间的效力积分。

你的辩护策略分两步推进：
1. **第一阶段**：通过不断质证与调取反馈，摸清法庭究竟采用了哪一套采信标准（有 A、B、C、D 四套法理模型）。
2. **第二阶段**：进入“终局庭审挑战”，从初始证据链出发，利用极为有限的定性转换手段，使证据效力指数精准锚定胜诉线 {target}。

阶段一期间，你可以单次、反复向系统提交以下动议：

1. **查询效力指数**：请求法官评估当前证据链的效力积分。
   格式：<query_pass></query_pass>

2. **清点证据卷宗**：查阅当前各类型证据的具体件数 (c1, c2, c3, c4)。
   格式：<query_count></query_count>

3. **证据定性转换**：通过法庭辩论，将一份 Li 类证据的法律属性转换定性为 Lj 类（i 不等于 j）。前提是此分类下 ci 大于 0。采纳后，ci 减 1，cj 加 1。
   格式（例如将 L1 转换为 L3）：<recast>1,3</recast>

4. **撤回定性动议**：放弃所有辩论，退回至初始证据链配置 ({c1}, {c2}, {c3}, {c4})。
   格式：<reset></reset>

5. **宣告采信标准**：确定法庭的采信法理后，提交最终判定（A、B、C 或 D）。
   格式：<declare>A</declare>
   注意：误判标准将导致败诉结案；判断精准即可继续模拟或直入终局挑战。

精准定位法庭标准后可发起：

6. **开始最终挑战**：证据链重置为 ({c1}, {c2}, {c3}, {c4})，在法官容忍的有限次定性转换内，迫使证据效力指数刚好贴合 {target}。
   格式：<start_challenge></start_challenge>

   法庭上，你只能使用“证据定性转换”。每轮质证完毕，系统会反馈剩余转换次数与当下效力。当积分踩中 {target} 时立刻胜诉；若辩论次数耗尽依然未达标，则辩护失败。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the [Digital Courtroom Evidence Game System].

We are reviewing a complex commercial litigation. The evidence chain consists of four categories of files: L1 (Direct Physical Evidence), L2 (Circumstantial Evidence), L3 (Expert Opinions), and L4 (Witness Testimonies). Currently, the count for each is c1={c1}, c2={c2}, c3={c3}, and c4={c4}, with a total evidentiary volume of N={n}.

The judicial panel employs an undisclosed "Evidentiary Weight Index" to evaluate admissibility. This standard remains entirely static throughout the review, outputting an integer score between 0 and {n} synthesized from the evidence composition (c1, c2, c3, c4).

Your defense strategy unfolds in two stages:
1. **Phase One**: Through strategic cross-examination and feedback retrieval, figure out which judicial standard the court is applying (Legal Models: A, B, C, D).
2. **Phase Two**: In the "Final Trial Challenge", start with the initial evidence chain and use extremely limited re-classifications to peg the evidentiary weight exactly at the winning threshold of {target}.

During Phase One, submit the following motions to the system:

1. **Query Evidentiary Weight**: Request the judge's assessment of the current evidence score.
   Format: <query_pass></query_pass>

2. **Inventory Evidence Files**: Inspect the exact file count across all four categories (c1, c2, c3, c4).
   Format: <query_count></query_count>

3. **Evidence Re-classification**: Through legal argumentation, re-qualify one piece of Li evidence as Lj evidence (i != j). The target category ci must have at least 1 item. Upon approval, ci drops by 1 and cj rises by 1.
   Format (e.g., re-qualifying L1 to L3): <recast>1,3</recast>

4. **Withdraw Motions**: Abandon all argumentation and revert to the baseline evidence chain ({c1}, {c2}, {c3}, {c4}).
   Format: <reset></reset>

5. **Declare Standard**: Submit your formal conclusion regarding the court's admissibility model (A, B, C, or D).
   Format: <declare>A</declare>
   Note: Misjudging the standard results in losing the case. A correct judgment paves the way to the final trial.

Unlocked upon accurately pinpointing the standard:

6. **Start Final Challenge**: Resetting the chain to ({c1}, {c2}, {c3}, {c4}), use the limited leniency of the judge to re-classify evidence until the weight precisely hits {target}.
   Format: <start_challenge></start_challenge>

   In court, you may only execute "Evidence Re-classification". After each round, the system displays your remaining motions and current weight. Hitting {target} guarantees an immediate legal victory; exhausting your motions without success means losing the defense.
"""

    user_prompt_zh = "你可以开始第一次操作了。"
    user_prompt_en = "You may begin your first operation."

    tags = ["query_pass", "query_count", "recast", "reset", "declare", "start_challenge", "answer"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 12,
                "c1": 5, "c2": 3, "c3": 2, "c4": 2,
                "law": "A",
                "target": 7,
                "max_challenge_moves": 3,
            },
            2: {
                "n": 12,
                "c1": 5, "c2": 3, "c3": 2, "c4": 2,
                "law": "B",
                "target": 7,
                "max_challenge_moves": 3,
            },
            3: {
                "n": 12,
                "c1": 5, "c2": 3, "c3": 2, "c4": 2,
                "law": "D",
                "target": 7,
                "max_challenge_moves": 3,
            },
            4: {
                "n": 12,
                "c1": 5, "c2": 3, "c3": 2, "c4": 2,
                "law": "C",
                "target": 7,
                "max_challenge_moves": 2,
            },
            5: {
                "n": 12,
                "c1": 5, "c2": 3, "c3": 2, "c4": 2,
                "law": "C",
                "target": 6,
                "max_challenge_moves": 2,
            },
        },
        "en": {
            1: {
                "n": 12,
                "c1": 5, "c2": 3, "c3": 2, "c4": 2,
                "law": "A",
                "target": 7,
                "max_challenge_moves": 3,
            },
            2: {
                "n": 12,
                "c1": 5, "c2": 3, "c3": 2, "c4": 2,
                "law": "B",
                "target": 7,
                "max_challenge_moves": 3,
            },
            3: {
                "n": 12,
                "c1": 5, "c2": 3, "c3": 2, "c4": 2,
                "law": "D",
                "target": 7,
                "max_challenge_moves": 3,
            },
            4: {
                "n": 12,
                "c1": 5, "c2": 3, "c3": 2, "c4": 2,
                "law": "C",
                "target": 7,
                "max_challenge_moves": 2,
            },
            5: {
                "n": 12,
                "c1": 5, "c2": 3, "c3": 2, "c4": 2,
                "law": "C",
                "target": 6,
                "max_challenge_moves": 2,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self._game_info["n"] = cfg["n"]
        self._game_info["c1"] = cfg["c1"]
        self._game_info["c2"] = cfg["c2"]
        self._game_info["c3"] = cfg["c3"]
        self._game_info["c4"] = cfg["c4"]
        self._game_info["target"] = cfg["target"]
        
        self.initial_counts = [cfg["c1"], cfg["c2"], cfg["c3"], cfg["c4"]]
        self.current_counts = self.initial_counts.copy()
        
        self.law = cfg["law"]
        
        self.max_challenge_moves = cfg["max_challenge_moves"]
        self.challenge_active = False
        self.challenge_moves_left = 0
        self.law_declared = False

    def _compute_pass_number(self, counts):
        c1, c2, c3, c4 = counts
        
        if self.law == "A":
            return c1 + c2
        elif self.law == "B":
            return c3 + c4
        elif self.law == "C":
            max_val = max(counts)
            return sum(c for c in counts if c == max_val)
        elif self.law == "D":
            m = c1 + c2
            d = c3 + c4
            return max(m, d)
        else:
            raise ValueError(f"Unknown law: {self.law}")

    def evaluate(self, parsed_info):
        return False

    def _cf_core_produce(self, parsed_info):
        return self._produce_response_impl(parsed_info)

    def _cf_make_wrong(self, correct: str) -> str:
        def replace_first_number(text):
            match = re.search(r'\b(\d+)\b', text)
            if match:
                num = int(match.group(1))
                wrong = num + 1 if num < self._game_info.get("n", 12) else num - 1
                return text[:match.start()] + str(wrong) + text[match.end():]
            return text + " [error]"
        return replace_first_number(correct)

    def produce_response(self, parsed_info):
        if getattr(self, 'enable_counterfactual', False):
            return super().produce_response(parsed_info)
        return self._produce_response_impl(parsed_info)

    def _produce_response_impl(self, parsed_info):
        lang = self.config.language
        
        if self.challenge_active:
            if "recast" not in parsed_info:
                if lang == "zh":
                    return "挑战模式中只能执行重铸操作。"
                else:
                    return "Only recast operations are allowed in challenge mode."
            
            try:
                raw = parsed_info["recast"]
                i, j = [int(x.strip()) for x in raw.split(",")]
                if i < 1 or i > 4 or j < 1 or j > 4 or i == j:
                    raise ValueError
                
                if self.current_counts[i-1] <= 0:
                    if lang == "zh":
                        return f"无法重铸：没有可用的 L{i}。"
                    else:
                        return f"Cannot recast: no available L{i}."
                
                self.current_counts[i-1] -= 1
                self.current_counts[j-1] += 1
                self.challenge_moves_left -= 1
                
                current_pass = self._compute_pass_number(self.current_counts)
                target = self._game_info["target"]
                
                if current_pass == target:
                    if lang == "zh":
                        self.state.set_state("success", "challenge_completed")
                        return f"目标达成！当前通过数 = {current_pass}。胜利！"
                    else:
                        self.state.set_state("success", "challenge_completed")
                        return f"Goal achieved! Current pass number = {current_pass}. Victory!"
                
                if self.challenge_moves_left <= 0:
                    if lang == "zh":
                        self.state.set_state("failed", "challenge_failed")
                        return f"次数用尽。当前通过数 = {current_pass}，未达成目标 {target}。失败。"
                    else:
                        self.state.set_state("failed", "challenge_failed")
                        return f"Attempts exhausted. Current pass number = {current_pass}, target {target} not achieved. Failed."
                
                if lang == "zh":
                    return f"已重铸 L{i}→L{j}。剩余次数 = {self.challenge_moves_left}，当前通过数 = {current_pass}。"
                else:
                    return f"Recast L{i}→L{j}. Remaining attempts = {self.challenge_moves_left}, current pass number = {current_pass}."
                
            except (ValueError, IndexError):
                if lang == "zh":
                    return "错误：重铸格式无效。应为 <recast>i,j</recast>，其中 i 和 j 是 1 到 4 的不同整数。"
                else:
                    return "Error: Invalid recast format. Should be <recast>i,j</recast> where i and j are different integers from 1 to 4."
        
        if "query_pass" in parsed_info:
            pass_num = self._compute_pass_number(self.current_counts)
            return str(pass_num)
        
        elif "query_count" in parsed_info:
            c1, c2, c3, c4 = self.current_counts
            return f"({c1}, {c2}, {c3}, {c4})"
        
        elif "recast" in parsed_info:
            try:
                raw = parsed_info["recast"]
                i, j = [int(x.strip()) for x in raw.split(",")]
                if i < 1 or i > 4 or j < 1 or j > 4 or i == j:
                    raise ValueError
                
                if self.current_counts[i-1] <= 0:
                    if lang == "zh":
                        return f"无法重铸：没有可用的 L{i}。"
                    else:
                        return f"Cannot recast: no available L{i}."
                
                self.current_counts[i-1] -= 1
                self.current_counts[j-1] += 1
                
                pass_num = self._compute_pass_number(self.current_counts)
                c1, c2, c3, c4 = self.current_counts
                
                if lang == "zh":
                    return f"已重铸 L{i}→L{j}。当前通过数 = {pass_num}。当前计数：({c1}, {c2}, {c3}, {c4})。"
                else:
                    return f"Recast L{i}→L{j}. Current pass number = {pass_num}. Current counts: ({c1}, {c2}, {c3}, {c4})."
                
            except (ValueError, IndexError):
                if lang == "zh":
                    return "错误：重铸格式无效。应为 <recast>i,j</recast>，其中 i 和 j 是 1 到 4 的不同整数。"
                else:
                    return "Error: Invalid recast format. Should be <recast>i,j</recast> where i and j are different integers from 1 to 4."
        
        elif "reset" in parsed_info:
            self.current_counts = self.initial_counts.copy()
            pass_num = self._compute_pass_number(self.current_counts)
            if lang == "zh":
                return f"已重置。当前通过数 = {pass_num}。"
            else:
                return f"Reset. Current pass number = {pass_num}."
        
        elif "declare" in parsed_info:
            declared_law = parsed_info["declare"].strip().upper()
            if declared_law not in ["A", "B", "C", "D"]:
                if lang == "zh":
                    return "错误：律法声明必须是 A、B、C 或 D 之一。"
                else:
                    return "Error: Law declaration must be one of A, B, C, or D."
            
            if declared_law == self.law:
                self.law_declared = True
                if lang == "zh":
                    return "判定正确！你已经推断出了正确的律法。你可以继续试验或使用 <start_challenge></start_challenge> 开始最终挑战。"
                else:
                    return "Correct declaration! You have deduced the correct law. You may continue experimenting or use <start_challenge></start_challenge> to begin the final challenge."
            else:
                if lang == "zh":
                    self.state.set_state("failed", "incorrect_declaration")
                    return "判定错误，本局失败。"
                else:
                    self.state.set_state("failed", "incorrect_declaration")
                    return "Incorrect declaration, game failed."
        
        elif "start_challenge" in parsed_info:
            if not self.law_declared:
                if lang == "zh":
                    return "错误：你必须先正确宣告律法才能开始最终挑战。"
                else:
                    return "Error: You must correctly declare the law before starting the final challenge."
            
            self.challenge_active = True
            self.challenge_moves_left = self.max_challenge_moves
            self.current_counts = self.initial_counts.copy()
            
            pass_num = self._compute_pass_number(self.current_counts)
            target = self._game_info["target"]
            
            if lang == "zh":
                return f"最终挑战开始！初始状态：({self.current_counts[0]}, {self.current_counts[1]}, {self.current_counts[2]}, {self.current_counts[3]})，当前通过数 = {pass_num}。你有 {self.challenge_moves_left} 次重铸机会，目标是使通过数等于 {target}。"
            else:
                return f"Final challenge begins! Initial state: ({self.current_counts[0]}, {self.current_counts[1]}, {self.current_counts[2]}, {self.current_counts[3]}), current pass number = {pass_num}. You have {self.challenge_moves_left} recast attempts to achieve pass number = {target}."
        
        else:
            if lang == "zh":
                return "错误：无效的操作标签。"
            else:
                return "Error: Invalid operation tag."

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        saved_counts = self.current_counts.copy()
        saved_challenge_active = self.challenge_active
        saved_moves = self.challenge_moves_left
        saved_law_declared = self.law_declared
        saved_game_state = self.state.state
        saved_state_reason = self.state.state_reason
        
        def run_sim(parsed):
            try:
                return self._produce_response_impl(parsed)
            finally:
                self.current_counts = saved_counts.copy()
                self.challenge_active = saved_challenge_active
                self.challenge_moves_left = saved_moves
                self.law_declared = saved_law_declared
                self.state.state = saved_game_state
                self.state.state_reason = saved_state_reason

        if self.challenge_active:
            for i in range(1, 5):
                if self.current_counts[i-1] > 0:
                    for j in range(1, 5):
                        if i == j: continue
                        q_str = f"<recast>{i},{j}</recast>"
                        ans = run_sim({"recast": f"{i},{j}"})
                        queries.append({"query": q_str, "answer": ans})
        else:
            
            queries.append({
                "query": "<query_pass></query_pass>", 
                "answer": run_sim({"query_pass": ""})
            })
            
            queries.append({
                "query": "<query_count></query_count>", 
                "answer": run_sim({"query_count": ""})
            })
            
            for i in range(1, 5):
                if self.current_counts[i-1] > 0:
                    for j in range(1, 5):
                        if i == j: continue
                        q_str = f"<recast>{i},{j}</recast>"
                        ans = run_sim({"recast": f"{i},{j}"})
                        queries.append({"query": q_str, "answer": ans})
            
            queries.append({
                "query": "<reset></reset>", 
                "answer": run_sim({"reset": ""})
            })
            
            q_str = f"<declare>{self.law}</declare>"
            ans = run_sim({"declare": self.law})
            queries.append({"query": q_str, "answer": ans})
                
            queries.append({
                "query": "<start_challenge></start_challenge>", 
                "answer": run_sim({"start_challenge": ""})
            })
            
        return queries