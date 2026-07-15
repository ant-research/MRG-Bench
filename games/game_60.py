from .base import Game
import re

class HiddenSequenceRuleGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "序列"
    enable_counterfactual = False

    game_rule_zh = """\
我们现在来玩一个"隐藏序列规则"的推理游戏，规则如下：

游戏设定了一个有序序列 S，初始为 [1, 2, ..., {n}]。每个元素的标签等于其初始位置编号。位置索引从左到右为 1 到当前长度 L。

核心机制：存在一个隐藏的确定性函数 F(p, L')，每当你删除位置 p 的元素后，序列长度变为 L' = L - 1，系统会自动删除位置 q = F(p, L') 的元素，长度再次减 1。删除后，右侧元素会自动左移填补空位。

你的目标是通过交互推断出隐藏函数 F 的规律，并在验证操作中证明你已掌握该规律。

1. COUNT：查询当前序列长度
   格式：<count></count>
   返回：Length = 具体数字

2. PEEK：查询指定位置的元素标签
   格式：<peek>位置索引</peek>
   返回：Pos 位置 = 标签 或 Invalid index

3. PLUCK：删除指定位置的元素（触发系统的连锁删除）
   格式：<pluck>位置索引</pluck>
   返回：You removed = 标签A; System removed = 标签B; New length = 新长度
   注意：序列长度必须大于等于 2 才能执行

4. CHALLENGE：验证性操作，需要预测系统删除的元素及最终状态
   格式：<challenge>p=位置, system=预测的系统删除标签, pos=位置1:预测标签1,位置2:预测标签2</challenge>
   说明：
   - p：你要删除的位置
   - system：预测系统将删除的元素标签
   - pos：预测最终序列中至少 2 个位置的标签（用逗号分隔）
   返回：Check system = Yes/No; Pos 位置 check = Yes/No (多个); Resulting length = 新长度

5. ANSWER：满足所有条件后提交最终答案
   格式：<answer>完成</answer>
   系统会检查是否满足成功条件。

1. 至少执行过 3 次 PLUCK 操作
2. 至少一次 CHALLENGE 中：
   - 系统删除的标签预测正确
   - 且至少 2 个位置的标签预测全部正确

- 序列长度小于 2 时无法继续操作，且未满足成功条件
- 指令格式错误

请尽可能少地使用操作次数来完成推理。
"""

    game_rule_en = """\
Let's play a "Hidden Sequence Rule" deduction game. Here are the rules:

The game sets up an ordered sequence S, initially [1, 2, ..., {n}]. Each element's label equals its initial position number. Position indices range from 1 to the current length L, left to right.

Core mechanism: There exists a hidden deterministic function F(p, L'). Whenever you remove an element at position p, the sequence length becomes L' = L - 1, then the system automatically removes the element at position q = F(p, L'), reducing the length by 1 again. After removal, elements to the right shift left to fill gaps.

Your goal is to infer the hidden function F through interaction and prove your understanding in a verification operation.

1. COUNT: Query current sequence length
   Format: <count></count>
   Returns: Length = number

2. PEEK: Query the element label at a specific position
   Format: <peek>position_index</peek>
   Returns: Pos position = label OR Invalid index

3. PLUCK: Remove element at specified position (triggers system's chain removal)
   Format: <pluck>position_index</pluck>
   Returns: You removed = labelA; System removed = labelB; New length = new_length
   Note: Sequence length must be at least 2 to execute

4. CHALLENGE: Verification operation, requires predicting system removal and final state
   Format: <challenge>p=position, system=predicted_system_label, pos=pos1:pred_label1,pos2:pred_label2</challenge>
   Explanation:
   - p: position you want to remove
   - system: predicted label of element system will remove
   - pos: predict at least 2 positions' labels in final sequence (comma-separated)
   Returns: Check system = Yes/No; Pos position check = Yes/No (multiple); Resulting length = new_length

5. ANSWER: Submit your final answer after meeting all conditions
   Format: <answer>done</answer>
   The game will check if success conditions are met.

1. At least 3 PLUCK operations executed
2. At least one CHALLENGE where:
   - System removal label prediction is correct
   - AND at least 2 position label predictions are all correct

- Sequence length less than 2 prevents further operations, and success conditions not met
- Invalid command format

Please use as few operations as possible to complete the deduction.
"""

    contextualized_rule_zh_1 = """\
我们现在来玩一个“列车车厢联动调度”推理游戏，规则如下：

游戏设定了一列编组为 S 的列车，初始有 [1, 2, ..., {n}] 节车厢。每节车厢的出厂编号等于其初始位置。位置索引从列车头到尾为 1 到当前长度 L。

核心机制：列车控制系统存在一个隐藏的确定性安全函数 F(p, L')。每当你解编（删除）位置 p 的车厢后，列车长度变为 L' = L - 1，系统会自动启动连锁协议，解编位置 q = F(p, L') 的车厢，长度再次减 1。解编后，后方车厢会自动向前补齐连挂。

你的目标是通过交互测试推断出隐藏函数 F 的安全调度规律，并在验证操作中证明你已掌握该规律。

1. COUNT：查询当前序列长度
   格式：<count></count>
   返回：Length = 具体数字

2. PEEK：查询指定位置的车厢编号
   格式：<peek>位置索引</peek>
   返回：Pos 位置 = 编号 或 Invalid index

3. PLUCK：解编指定位置的车厢（触发系统的连锁解编）
   格式：<pluck>位置索引</pluck>
   返回：You removed = 编号A; System removed = 编号B; New length = 新长度
   注意：列车长度必须大于等于 2 才能执行

4. CHALLENGE：验证性操作，需要预测系统解编的车厢及最终状态
   格式：<challenge>p=位置, system=预测的系统解编编号, pos=位置1:预测编号1,位置2:预测编号2</challenge>
   说明：
   - p：你要解编的位置
   - system：预测系统将解编的车厢编号
   - pos：预测最终列车中至少 2 个位置的编号（用逗号分隔）
   返回：Check system = Yes/No; Pos 位置 check = Yes/No (多个); Resulting length = 新长度

5. ANSWER：满足所有条件后提交最终答案
   格式：<answer>完成</answer>
   系统会检查是否满足成功条件。

1. 至少执行过 3 次 PLUCK 操作
2. 至少一次 CHALLENGE 中：
   - 系统解编的编号预测正确
   - 且至少 2 个位置的编号预测全部正确

- 序列长度小于 2 时无法继续操作，且未满足成功条件
- 指令格式错误

请尽可能少地使用操作次数来完成推理。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play a "Train Car Linked Dispatching" deduction game. Here are the rules:

The game sets up a train composition S, initially with [1, 2, ..., {n}] cars. Each car's factory ID equals its initial position. Position indices range from head to tail as 1 to the current length L.

Core mechanism: The train control system has a hidden deterministic safety function F(p, L'). Whenever you uncouple (remove) the car at position p, the length becomes L' = L - 1, and the system automatically triggers a chain protocol to uncouple the car at position q = F(p, L'), reducing the length by 1 again. After removal, rear cars automatically shift forward to couple and fill gaps.

Your goal is to infer the hidden safety function F through interaction and prove your understanding in a verification operation.

1. COUNT: Query current sequence length
   Format: <count></count>
   Returns: Length = number

2. PEEK: Query the car's factory ID at a specific position
   Format: <peek>position_index</peek>
   Returns: Pos position = ID OR Invalid index

3. PLUCK: Uncouple car at specified position (triggers system's chain uncoupling)
   Format: <pluck>position_index</pluck>
   Returns: You removed = ID_A; System removed = ID_B; New length = new_length
   Note: Sequence length must be at least 2 to execute

4. CHALLENGE: Verification operation, requires predicting system uncoupling and final state
   Format: <challenge>p=position, system=predicted_system_ID, pos=pos1:pred_ID1,pos2:pred_ID2</challenge>
   Explanation:
   - p: position you want to uncouple
   - system: predicted ID of car system will uncouple
   - pos: predict at least 2 positions' IDs in final sequence (comma-separated)
   Returns: Check system = Yes/No; Pos position check = Yes/No (multiple); Resulting length = new_length

5. ANSWER: Submit your final answer after meeting all conditions
   Format: <answer>done</answer>
   The game will check if success conditions are met.

1. At least 3 PLUCK operations executed
2. At least one CHALLENGE where:
   - System uncoupling ID prediction is correct
   - AND at least 2 position ID predictions are all correct

- Sequence length less than 2 prevents further operations, and success conditions not met
- Invalid command format

Please use as few operations as possible to complete the deduction.
"""

    contextualized_rule_zh_2 = """\
我们现在来玩一个“试剂联动损耗”推理游戏，规则如下：

游戏设定了一批排列在检测槽 S 中的试剂管，初始为 [1, 2, ..., {n}]。每管试剂的批次号等于其初始位置编号。槽位索引从左到右为 1 到当前剩余数量 L。

核心机制：检测台内嵌了一个隐藏的确定性防污染函数 F(p, L')。每当你移出（删除）位置 p 的试剂管后，剩余总数变为 L' = L - 1，系统会自动销毁位置 q = F(p, L') 的试剂管以防交叉污染，总数再次减 1。移出后，右侧试剂管会自动被机械臂左移填补空位。

你的目标是通过交互推断出隐藏函数 F 的防污染规律，并在验证操作中证明你已掌握该规律。

1. COUNT：查询当前试剂管总数
   格式：<count></count>
   返回：Length = 具体数字

2. PEEK：查询指定槽位的试剂批次号
   格式：<peek>槽位索引</peek>
   返回：Pos 槽位 = 批次号 或 Invalid index

3. PLUCK：移出指定槽位的试剂管（触发系统的连锁销毁）
   格式：<pluck>槽位索引</pluck>
   返回：You removed = 批次号A; System removed = 批次号B; New length = 新总数
   注意：试剂管总数必须大于等于 2 才能执行

4. CHALLENGE：验证性操作，需要预测系统销毁的试剂管及最终状态
   格式：<challenge>p=槽位, system=预测的系统销毁批次号, pos=槽位1:预测批次号1,槽位2:预测批次号2</challenge>
   说明：
   - p：你要移出的槽位
   - system：预测系统将销毁的试剂批次号
   - pos：预测最终检测槽中至少 2 个槽位的批次号（用逗号分隔）
   返回：Check system = Yes/No; Pos 槽位 check = Yes/No (多个); Resulting length = 新总数

5. ANSWER：满足所有条件后提交最终答案
   格式：<answer>完成</answer>
   系统会检查是否满足成功条件。

1. 至少执行过 3 次 PLUCK 操作
2. 至少一次 CHALLENGE 中：
   - 系统销毁的批次号预测正确
   - 且至少 2 个槽位的批次号预测全部正确

- 试剂管总数小于 2 时无法继续操作，且未满足成功条件
- 指令格式错误

请尽可能少地使用操作次数来完成推理。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Reagent Linked Depletion" deduction game. Here are the rules:

The game sets up a batch of reagent tubes in detection slots S, initially [1, 2, ..., {n}]. Each tube's batch number equals its initial position number. Slot indices range from left to right as 1 to the current remaining quantity L.

Core mechanism: The detection platform embeds a hidden deterministic anti-contamination function F(p, L'). Whenever you extract (remove) the tube at position p, the remaining total becomes L' = L - 1, and the system automatically destroys the tube at position q = F(p, L') to prevent cross-contamination, reducing the total by 1 again. After extraction, tubes to the right are automatically shifted left by robotic arms to fill gaps.

Your goal is to infer the hidden anti-contamination function F through interaction and prove your understanding in a verification operation.

1. COUNT: Query current remaining quantity of tubes
   Format: <count></count>
   Returns: Length = number

2. PEEK: Query the tube's batch number at a specific slot
   Format: <peek>slot_index</peek>
   Returns: Pos slot = batch_number OR Invalid index

3. PLUCK: Extract tube at specified slot (triggers system's chain destruction)
   Format: <pluck>slot_index</pluck>
   Returns: You removed = batch_number_A; System removed = batch_number_B; New length = new_length
   Note: Remaining quantity must be at least 2 to execute

4. CHALLENGE: Verification operation, requires predicting system destruction and final state
   Format: <challenge>p=slot, system=predicted_system_batch_number, pos=slot1:pred_batch_number1,slot2:pred_batch_number2</challenge>
   Explanation:
   - p: slot you want to extract
   - system: predicted batch number of tube system will destroy
   - pos: predict at least 2 slots' batch numbers in final sequence (comma-separated)
   Returns: Check system = Yes/No; Pos slot check = Yes/No (multiple); Resulting length = new_length

5. ANSWER: Submit your final answer after meeting all conditions
   Format: <answer>done</answer>
   The game will check if success conditions are met.

1. At least 3 PLUCK operations executed
2. At least one CHALLENGE where:
   - System destruction batch number prediction is correct
   - AND at least 2 slot batch number predictions are all correct

- Remaining quantity less than 2 prevents further operations, and success conditions not met
- Invalid command format

Please use as few operations as possible to complete the deduction.
"""

    contextualized_rule_zh_3 = """\
我们现在来玩一个“智能考位联动”推理游戏，规则如下：

游戏设定了一排按序就坐的考生 S，初始考号为 [1, 2, ..., {n}]。每个考生的考号等于其初始座位编号。座位索引从前到后为 1 到当前人数 L。

核心机制：考务系统存在一个隐藏的确定性防作弊函数 F(p, L')。每当你取消（删除）位置 p 考生的资格后，剩余人数变为 L' = L - 1，系统会自动按防作弊规则取消位置 q = F(p, L') 考生的资格，人数再次减 1。空位产生后，后方考生会自动向前挪动填补座位。

你的目标是通过交互推断出隐藏函数 F 的联动取消规律，并在验证操作中证明你已掌握该规律。

1. COUNT：查询当前剩余考生人数
   格式：<count></count>
   返回：Length = 具体数字

2. PEEK：查询指定座位的考生考号
   格式：<peek>座位索引</peek>
   返回：Pos 座位 = 考号 或 Invalid index

3. PLUCK：取消指定座位考生的资格（触发系统的连锁取消）
   格式：<pluck>座位索引</pluck>
   返回：You removed = 考号A; System removed = 考号B; New length = 新人数
   注意：考生人数必须大于等于 2 才能执行

4. CHALLENGE：验证性操作，需要预测系统取消资格的考生及最终状态
   格式：<challenge>p=座位, system=预测的系统取消考号, pos=座位1:预测考号1,座位2:预测考号2</challenge>
   说明：
   - p：你要取消资格的座位
   - system：预测系统将取消的考生考号
   - pos：预测最终队列中至少 2 个座位的考号（用逗号分隔）
   返回：Check system = Yes/No; Pos 座位 check = Yes/No (多个); Resulting length = 新人数

5. ANSWER：满足所有条件后提交最终答案
   格式：<answer>完成</answer>
   系统会检查是否满足成功条件。

1. 至少执行过 3 次 PLUCK 操作
2. 至少一次 CHALLENGE 中：
   - 系统取消的考号预测正确
   - 且至少 2 个座位的考号预测全部正确

- 考生人数小于 2 时无法继续操作，且未满足成功条件
- 指令格式错误

请尽可能少地使用操作次数来完成推理。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Smart Seat Linked Cancellation" deduction game. Here are the rules:

The game sets up a row of sequentially seated candidates S, with initial exam numbers [1, 2, ..., {n}]. Each candidate's exam number equals their initial seat number. Seat indices range from front to back as 1 to the current number of people L.

Core mechanism: The exam administration system has a hidden deterministic anti-cheating function F(p, L'). Whenever you cancel (remove) the qualification of the candidate at position p, the remaining count becomes L' = L - 1, and the system automatically cancels the candidate at position q = F(p, L') based on anti-cheating rules, reducing the count by 1 again. Once a gap appears, candidates behind automatically move forward to fill the seats.

Your goal is to infer the hidden linked cancellation function F through interaction and prove your understanding in a verification operation.

1. COUNT: Query current remaining number of candidates
   Format: <count></count>
   Returns: Length = number

2. PEEK: Query the candidate's exam number at a specific seat
   Format: <peek>seat_index</peek>
   Returns: Pos seat = exam_number OR Invalid index

3. PLUCK: Cancel candidate at specified seat (triggers system's chain cancellation)
   Format: <pluck>seat_index</pluck>
   Returns: You removed = exam_number_A; System removed = exam_number_B; New length = new_count
   Note: Number of candidates must be at least 2 to execute

4. CHALLENGE: Verification operation, requires predicting system cancellation and final state
   Format: <challenge>p=seat, system=predicted_system_exam_number, pos=seat1:pred_exam_number1,seat2:pred_exam_number2</challenge>
   Explanation:
   - p: seat of the candidate you want to cancel
   - system: predicted exam number of candidate system will cancel
   - pos: predict at least 2 seats' exam numbers in final row (comma-separated)
   Returns: Check system = Yes/No; Pos seat check = Yes/No (multiple); Resulting length = new_count

5. ANSWER: Submit your final answer after meeting all conditions
   Format: <answer>done</answer>
   The game will check if success conditions are met.

1. At least 3 PLUCK operations executed
2. At least one CHALLENGE where:
   - System cancellation exam number prediction is correct
   - AND at least 2 seat exam number predictions are all correct

- Number of candidates less than 2 prevents further operations, and success conditions not met
- Invalid command format

Please use as few operations as possible to complete the deduction.
"""

    contextualized_rule_zh_4 = """\
我们现在来玩一个“流水线零件联动剔除”推理游戏，规则如下：

游戏设定了一条组装流水线上的零件序列 S，初始批号为 [1, 2, ..., {n}]。每个零件的批号等于其初始位置编号。位置索引从上游到下游为 1 到当前零件数 L。

核心机制：品控系统内置了一个隐藏的确定性算法 F(p, L')。每当你人工剔除（删除）位置 p 的零件后，剩余零件数变为 L' = L - 1，自动机械臂会依据算法联动剔除位置 q = F(p, L') 的零件，零件数再次减 1。剔除后，传送带会将右侧零件左移填补空缺。

你的目标是通过抽样交互推断出隐藏算法 F 的联动剔除规律，并在验证操作中证明你已掌握该规律。

1. COUNT：查询当前流水线上零件总数
   格式：<count></count>
   返回：Length = 具体数字

2. PEEK：查询指定位置的零件批号
   格式：<peek>位置索引</peek>
   返回：Pos 位置 = 批号 或 Invalid index

3. PLUCK：剔除指定位置的零件（触发系统的联动剔除）
   格式：<pluck>位置索引</pluck>
   返回：You removed = 批号A; System removed = 批号B; New length = 新零件数
   注意：零件总数必须大于等于 2 才能执行

4. CHALLENGE：验证性操作，需要预测系统联动剔除的零件及最终状态
   格式：<challenge>p=位置, system=预测的系统剔除批号, pos=位置1:预测批号1,位置2:预测批号2</challenge>
   说明：
   - p：你要人工剔除的位置
   - system：预测系统将联动剔除的零件批号
   - pos：预测最终流水线上至少 2 个位置的批号（用逗号分隔）
   返回：Check system = Yes/No; Pos 位置 check = Yes/No (多个); Resulting length = 新零件数

5. ANSWER：满足所有条件后提交最终答案
   格式：<answer>完成</answer>
   系统会检查是否满足成功条件。

1. 至少执行过 3 次 PLUCK 操作
2. 至少一次 CHALLENGE 中：
   - 系统剔除的批号预测正确
   - 且至少 2 个位置的批号预测全部正确

- 零件总数小于 2 时无法继续操作，且未满足成功条件
- 指令格式错误

请尽可能少地使用操作次数来完成推理。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's play an "Assembly Line Linked Rejection" deduction game. Here are the rules:

The game sets up a sequence of parts S on an assembly line, with initial batch numbers [1, 2, ..., {n}]. Each part's batch number equals its initial position number. Position indices range from upstream to downstream as 1 to the current number of parts L.

Core mechanism: The quality control system incorporates a hidden deterministic algorithm F(p, L'). Whenever you manually reject (remove) the part at position p, the remaining parts count becomes L' = L - 1, and the automated robotic arm correspondingly rejects the part at position q = F(p, L') based on the algorithm, reducing the count by 1 again. After rejection, the conveyor belt shifts parts on the right to the left to fill gaps.

Your goal is to infer the hidden algorithm F's linked rejection rule through interaction and prove your understanding in a verification operation.

1. COUNT: Query current total number of parts on the line
   Format: <count></count>
   Returns: Length = number

2. PEEK: Query the part's batch number at a specific position
   Format: <peek>position_index</peek>
   Returns: Pos position = batch_number OR Invalid index

3. PLUCK: Reject part at specified position (triggers system's linked rejection)
   Format: <pluck>position_index</pluck>
   Returns: You removed = batch_number_A; System removed = batch_number_B; New length = new_count
   Note: Total parts must be at least 2 to execute

4. CHALLENGE: Verification operation, requires predicting system linked rejection and final state
   Format: <challenge>p=position, system=predicted_system_batch_number, pos=position1:pred_batch_number1,position2:pred_batch_number2</challenge>
   Explanation:
   - p: position of the part you want to manually reject
   - system: predicted batch number of part the system will reject
   - pos: predict at least 2 positions' batch numbers in final sequence (comma-separated)
   Returns: Check system = Yes/No; Pos position check = Yes/No (multiple); Resulting length = new_count

5. ANSWER: Submit your final answer after meeting all conditions
   Format: <answer>done</answer>
   The game will check if success conditions are met.

1. At least 3 PLUCK operations executed
2. At least one CHALLENGE where:
   - System rejection batch number prediction is correct
   - AND at least 2 position batch number predictions are all correct

- Total parts less than 2 prevents further operations, and success conditions not met
- Invalid command format

Please use as few operations as possible to complete the deduction.
"""

    contextualized_rule_zh_5 = """\
我们现在来玩一个“连带证据排除”推理游戏，规则如下：

游戏设定了一组呈堂的有序证据链 S，初始编号为 [1, 2, ..., {n}]。每项证据的标识码等于其初始顺位编号。证据索引从主要到次要为 1 到当前剩余数量 L。

核心机制：法庭采信程序中存在一个隐藏的确定性排除法则 F(p, L')。每当你撤回（删除）位置 p 的证据后，剩余证据数变为 L' = L - 1，法庭会自动依据法则排除位置 q = F(p, L') 的连带证据，数量再次减 1。排除后，后置证据的顺位会自动向前递补。

你的目标是通过质证交互推断出隐藏法则 F 的连带排除规律，并在验证操作中证明你已掌握该规律。

1. COUNT：查询当前剩余证据数量
   格式：<count></count>
   返回：Length = 具体数字

2. PEEK：查询指定顺位的证据标识码
   格式：<peek>顺位索引</peek>
   返回：Pos 顺位 = 标识码 或 Invalid index

3. PLUCK：撤回指定顺位的证据（触发法庭的连带排除）
   格式：<pluck>顺位索引</pluck>
   返回：You removed = 标识码A; System removed = 标识码B; New length = 新数量
   注意：证据数量必须大于等于 2 才能执行

4. CHALLENGE：验证性操作，需要预测法庭连带排除的证据及最终状态
   格式：<challenge>p=顺位, system=预测的法庭排除标识码, pos=顺位1:预测标识码1,顺位2:预测标识码2</challenge>
   说明：
   - p：你要撤回的证据顺位
   - system：预测法庭将连带排除的证据标识码
   - pos：预测最终证据链中至少 2 个顺位的标识码（用逗号分隔）
   返回：Check system = Yes/No; Pos 顺位 check = Yes/No (多个); Resulting length = 新数量

5. ANSWER：满足所有条件后提交最终答案
   格式：<answer>完成</answer>
   系统会检查是否满足成功条件。

1. 至少执行过 3 次 PLUCK 操作
2. 至少一次 CHALLENGE 中：
   - 法庭排除的标识码预测正确
   - 且至少 2 个顺位的标识码预测全部正确

- 证据数量小于 2 时无法继续操作，且未满足成功条件
- 指令格式错误

请尽可能少地使用质证次数来完成推理。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's play a "Joint Evidence Exclusion" deduction game. Here are the rules:

The game sets up an ordered chain of presented evidence S, with initial ID codes [1, 2, ..., {n}]. Each evidence's ID code equals its initial ranking number. Evidence indices range from primary to secondary as 1 to the current remaining quantity L.

Core mechanism: The court's evidence admission procedure contains a hidden deterministic exclusion rule F(p, L'). Whenever you withdraw (remove) the evidence at position p, the remaining evidence count becomes L' = L - 1, and the court automatically excludes the joint evidence at position q = F(p, L') according to the rule, reducing the count by 1 again. After exclusion, the ranking of subsequent evidence automatically advances to fill gaps.

Your goal is to infer the hidden joint exclusion rule F through cross-examination interactions and prove your understanding in a verification operation.

1. COUNT: Query current remaining quantity of evidence
   Format: <count></count>
   Returns: Length = number

2. PEEK: Query the evidence ID code at a specific ranking
   Format: <peek>ranking_index</peek>
   Returns: Pos ranking = ID_code OR Invalid index

3. PLUCK: Withdraw evidence at specified ranking (triggers court's joint exclusion)
   Format: <pluck>ranking_index</pluck>
   Returns: You removed = ID_code_A; System removed = ID_code_B; New length = new_count
   Note: Evidence quantity must be at least 2 to execute

4. CHALLENGE: Verification operation, requires predicting court's joint exclusion and final state
   Format: <challenge>p=ranking, system=predicted_court_exclusion_ID_code, pos=ranking1:pred_ID_code1,ranking2:pred_ID_code2</challenge>
   Explanation:
   - p: ranking of the evidence you want to withdraw
   - system: predicted ID code of evidence the court will exclude
   - pos: predict at least 2 rankings' ID codes in final chain (comma-separated)
   Returns: Check system = Yes/No; Pos ranking check = Yes/No (multiple); Resulting length = new_count

5. ANSWER: Submit your final answer after meeting all conditions
   Format: <answer>done</answer>
   The game will check if success conditions are met.

1. At least 3 PLUCK operations executed
2. At least one CHALLENGE where:
   - Court exclusion ID code prediction is correct
   - AND at least 2 ranking ID code predictions are all correct

- Evidence quantity less than 2 prevents further operations, and success conditions not met
- Invalid command format

Please use as few operations as possible to complete the deduction.
"""

    tags = ["count", "peek", "pluck", "challenge", "answer"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 10,
                "rule_type": "constant_first",
                "rule_desc": "F(p, L') = 1"
            },
            2: {
                "n": 12,
                "rule_type": "constant_last",
                "rule_desc": "F(p, L') = L'"
            },
            3: {
                "n": 14,
                "rule_type": "same_position",
                "rule_desc": "F(p, L') = min(p, L')"
            },
            4: {
                "n": 15,
                "rule_type": "modulo",
                "rule_desc": "F(p, L') = (p % L') + 1"
            },
            5: {
                "n": 16,
                "rule_type": "mirror",
                "rule_desc": "F(p, L') = min(L' - p + 1, L')"
            },
        },
        "en": {
            1: {
                "n": 10,
                "rule_type": "constant_first",
                "rule_desc": "F(p, L') = 1"
            },
            2: {
                "n": 12,
                "rule_type": "constant_last",
                "rule_desc": "F(p, L') = L'"
            },
            3: {
                "n": 14,
                "rule_type": "same_position",
                "rule_desc": "F(p, L') = min(p, L')"
            },
            4: {
                "n": 15,
                "rule_type": "modulo",
                "rule_desc": "F(p, L') = (p % L') + 1"
            },
            5: {
                "n": 16,
                "rule_type": "mirror",
                "rule_desc": "F(p, L') = min(L' - p + 1, L')"
            },
        },
    }

    def __init__(self, config):
        self.pluck_count = 0
        self.challenge_success = False
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        
        n = cfg["n"]
        self.sequence = list(range(1, n + 1))
        
        self.rule_type = cfg["rule_type"]

        self._cf_round_counter = 0
        self._cf_correct_resp  = None
        self._cf_wrong_resp    = None

    def _apply_rule(self, p, L_prime):
        if self.rule_type == "constant_first":
            return 1
        elif self.rule_type == "constant_last":
            return L_prime
        elif self.rule_type == "same_position":
            return min(p, L_prime)
        elif self.rule_type == "modulo":
            return (p % L_prime) + 1 if L_prime > 0 else 1
        elif self.rule_type == "mirror":
            mirror_pos = L_prime - p + 1
            return max(1, min(mirror_pos, L_prime))
        else:
            raise ValueError(f"Unknown rule type: {self.rule_type}")

    def _remove_and_chain(self, p):
        if p < 1 or p > len(self.sequence):
            raise ValueError("Invalid position")
        
        removed_user = self.sequence.pop(p - 1)
        L_prime = len(self.sequence)
        
        q = self._apply_rule(p, L_prime)
        
        if q < 1 or q > L_prime:
            q = min(max(1, q), L_prime)
        removed_system = self.sequence.pop(q - 1)
        
        return removed_user, removed_system, len(self.sequence)

    def evaluate(self, parsed_info):
        return self.pluck_count >= 3 and self.challenge_success

    def produce_response(self, parsed_info):
        if self.enable_counterfactual:
            self._cf_round_counter += 1

            if self._cf_round_counter == 2:
                correct = self._cf_core_produce(parsed_info)
                self._cf_correct_resp = correct
                self._cf_wrong_resp = self._cf_make_wrong(correct)
                return self._cf_wrong_resp

            elif self._cf_round_counter == 3:
                return self._cf_correction_message()

        return self._cf_core_produce(parsed_info)

    def _cf_core_produce(self, parsed_info):
        lang = self.config.language
        
        if "count" in parsed_info:
            return f"Length = {len(self.sequence)}"
        
        elif "peek" in parsed_info:
            try:
                idx = int(parsed_info["peek"].strip())
                if idx < 1 or idx > len(self.sequence):
                    return "Invalid index" if lang == "en" else "无效索引"
                return f"Pos {idx} = {self.sequence[idx - 1]}"
            except:
                return "Invalid index" if lang == "en" else "无效索引"
        
        elif "pluck" in parsed_info:
            if len(self.sequence) < 2:
                return "Not enough elements" if lang == "en" else "元素不足"
            
            try:
                p = int(parsed_info["pluck"].strip())
                removed_user, removed_system, new_length = self._remove_and_chain(p)
                self.pluck_count += 1
                return f"You removed = {removed_user}; System removed = {removed_system}; New length = {new_length}"
            except Exception as e:
                return f"Error: {str(e)}" if lang == "en" else f"错误：{str(e)}"
        
        elif "challenge" in parsed_info:
            if len(self.sequence) < 2:
                return "Not enough elements" if lang == "en" else "元素不足"
            
            try:
                raw = parsed_info["challenge"]
                parts = {}
                p_match = re.search(r'\bp\s*=\s*(\d+)', raw)
                system_match = re.search(r'\bsystem\s*=\s*(\d+)', raw)
                pos_match = re.search(r'\bpos\s*=\s*(.+)$', raw.strip())
                
                if p_match:
                    parts["p"] = p_match.group(1).strip()
                if system_match:
                    parts["system"] = system_match.group(1).strip()
                if pos_match:
                    parts["pos"] = pos_match.group(1).strip()
                
                if "p" not in parts or "system" not in parts or "pos" not in parts:
                    return "Invalid challenge format" if lang == "en" else "挑战格式无效"
                
                p = int(parts["p"])
                system_pred = int(parts["system"])
                
                pos_preds = {}
                for pair in parts["pos"].split(","):
                    pair = pair.strip()
                    if ":" in pair:
                        pos_str, label_str = pair.split(":", 1)
                        pos_preds[int(pos_str.strip())] = int(label_str.strip())
                
                removed_user, removed_system, new_length = self._remove_and_chain(p)
                self.pluck_count += 1
                
                system_check = "Yes" if removed_system == system_pred else "No"
                
                pos_checks = []
                all_pos_correct = True
                for pos, pred_label in pos_preds.items():
                    if pos < 1 or pos > len(self.sequence):
                        pos_checks.append(f"Pos {pos} check = No")
                        all_pos_correct = False
                    else:
                        actual_label = self.sequence[pos - 1]
                        is_correct = actual_label == pred_label
                        pos_checks.append(f"Pos {pos} check = {'Yes' if is_correct else 'No'}")
                        if not is_correct:
                            all_pos_correct = False
                
                if system_check == "Yes" and all_pos_correct and len(pos_preds) >= 2:
                    self.challenge_success = True
                
                result = f"Check system = {system_check}; " + "; ".join(pos_checks) + f"; Resulting length = {new_length}"
                return result
                
            except Exception as e:
                return f"Error: {str(e)}" if lang == "en" else f"错误：{str(e)}"
        
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        lang = self.config.language
        current_len = len(self.sequence)

        q_count = "<count></count>"
        ans_count = f"Length = {current_len}"
        queries.append({"query": q_count, "answer": ans_count})

        for i in range(1, current_len + 1):
            q_peek = f"<peek>{i}</peek>"
            ans_peek = f"Pos {i} = {self.sequence[i - 1]}"
            queries.append({"query": q_peek, "answer": ans_peek})

        if current_len >= 2:
            original_sequence = list(self.sequence)

            for i in range(1, current_len + 1):
                try:
                    self.sequence = list(original_sequence)
                    
                    removed_user, removed_system, new_length = self._remove_and_chain(i)
                    
                    q_pluck = f"<pluck>{i}</pluck>"
                    ans_pluck = f"You removed = {removed_user}; System removed = {removed_system}; New length = {new_length}"
                    queries.append({"query": q_pluck, "answer": ans_pluck})
                except Exception:
                    pass
            
            self.sequence = original_sequence

        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        lang = self.config.language
        wrong = correct
        changed = False

        if lang == "zh":
            if "是" in wrong or "否" in wrong:
                wrong = wrong.replace("是", "___TEMP___").replace("否", "是").replace("___TEMP___", "否")
                changed = True
        elif lang == "en":
            def swap_match(m):
                text = m.group(0)
                if text == "Yes": return "No"
                if text == "No": return "Yes"
                if text == "yes": return "no"
                if text == "no": return "yes"
                if text == "YES": return "NO"
                if text == "NO": return "YES"
                return "No"

            if re.search(r'(?i)\b(yes|no)\b', wrong):
                wrong = re.sub(r'(?i)\b(yes|no)\b', swap_match, wrong)
                changed = True

        if not changed:
            return correct + "_WRONG"
        
        return wrong

    def _cf_correction_message(self) -> str:
        wrong = self._cf_wrong_resp
        correct = self._cf_correct_resp
        
        if self.config.language == "zh":
            return (f"【纠正】上一轮的回复有误。错误答案为：{wrong}，正确答案应为：{correct}。\n"
                    f"请基于正确信息重新开始提问。")
        else:
            return (f"[Correction] The previous response was incorrect. Wrong answer: {wrong}; Correct answer: {correct}.\n"
                    f"Please restart your questioning based on the correct information.")