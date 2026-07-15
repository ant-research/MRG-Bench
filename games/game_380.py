from .base import Game
import re

class ShiftRuleDeductionGame(Game):

    game_rule_zh = """\
我们来玩一个"移位规则推断"游戏，规则如下：

游戏设定了一个长度为 {n} 的有序序列 S，包含 {n} 个不同的元素，分别标记为 E1, E2, ..., E{n}。序列索引从 1 到 {n}。

我设置了一个隐藏的移位规则：当你在位置 p 插入一个特殊标记 X 后，系统会对新序列（长度变为 {n_plus_1}）执行循环右移操作，右移的步数 K(p) 遵循一个线性模公式：K(p) = (a × p + b) mod {n_plus_1}，其中 a 和 b 是我预设的固定参数（范围在 0 到 {n} 之间），在整个游戏中不会改变。

你的目标是通过交互实验推断出这个移位规则，具体可以：
- 方式 A：当我给出挑战参数（插入位置 {challenge_p} 和查询位置 {challenge_q}）时，正确预测该位置的元素是什么。
- 方式 B：直接给出参数 a 和 b 的值。

1. **插入操作**：在初始序列的位置 p（范围 1 到 {n_plus_1}）插入标记 X，系统会自动对新序列执行右移，然后你可以查询移位后的结果。

2. **查询操作**：在插入后，你可以查询当前序列中某些位置的元素。每次插入后最多查询 3 个位置（可以一次查询多个位置，也可以分多次查询）。

3. **重置操作**：移除标记 X，序列恢复到初始状态，结束当前实验回合。

4. **提交预测**：在进行至少 2 次不同位置的插入实验后，你可以提交预测：
   - 方式 A：回答我给出的挑战（在位置 {challenge_p} 插入后，位置 {challenge_q} 的元素是什么）。
   - 方式 B：直接给出参数 a 和 b。

每次操作只能包含一个标签，使用以下 XML 格式：

- 插入操作（例如在位置 3 插入）：
<insert>3</insert>

- 查询单个位置（例如查询位置 5）：
<query>5</query>

- 查询多个位置（例如查询位置 1, 3, 5）：
<query>1,3,5</query>

- 重置序列：
<reset></reset>

- 提交预测方式 A（例如预测元素为 E2）：
<answer>E2</answer>

- 提交预测方式 A（预测元素为 X）：
<answer>X</answer>

- 提交预测方式 B（例如 a=2, b=3）：
<answer>a=2,b=3</answer>

1. 初始状态下，序列为 S = [E1, E2, ..., E{n}]。
2. 你可以多次执行"插入—查询—重置"的循环来收集信息。
3. 当你认为掌握了规律后，等待系统挑战或直接提交参数。
4. 如果预测错误，游戏失败；如果正确，游戏成功。

注意：
- 插入位置 p 的有效范围是 1 到 {n_plus_1}。
- 查询位置 q 的有效范围是 1 到 {n_plus_1}（在插入后）。
- 必须先执行插入操作，才能进行查询。
- 每次插入后最多查询 3 个位置。
- 必须进行至少 2 次不同位置的插入实验后才能提交预测。
"""

    game_rule_en = """\
Let's play a "Shift Rule Deduction" game. Here are the rules:

The game has an ordered sequence S of length {n}, containing {n} distinct elements labeled E1, E2, ..., E{n}. The sequence is indexed from 1 to {n}.

I have set up a hidden shift rule: when you insert a special marker X at position p, the system will perform a cyclic right shift on the new sequence (length becomes {n_plus_1}). The shift amount K(p) follows a linear modular formula: K(p) = (a × p + b) mod {n_plus_1}, where a and b are fixed parameters I preset (ranging from 0 to {n}) and will not change throughout the game.

Your goal is to deduce this shift rule through interactive experiments. You can achieve this by:
- Method A: When I provide challenge parameters (insertion position {challenge_p} and query position {challenge_q}), correctly predict what element is at that position.
- Method B: Directly provide the values of parameters a and b.

1. **Insert Operation**: Insert marker X at position p (range 1 to {n_plus_1}) in the initial sequence. The system will automatically perform a right shift on the new sequence, and then you can query the result after shifting.

2. **Query Operation**: After insertion, you can query elements at certain positions in the current sequence. You can query at most 3 positions after each insertion (you can query multiple positions at once or in separate queries).

3. **Reset Operation**: Remove marker X, restore the sequence to its initial state, and end the current experiment round.

4. **Submit Prediction**: After conducting at least 2 insertion experiments at different positions, you can submit a prediction:
   - Method A: Answer my challenge (after inserting at position {challenge_p}, what element is at position {challenge_q}).
   - Method B: Directly provide parameters a and b.

Each operation can only contain one tag. Use the following XML format:

- Insert operation (e.g., insert at position 3):
<insert>3</insert>

- Query single position (e.g., query position 5):
<query>5</query>

- Query multiple positions (e.g., query positions 1, 3, 5):
<query>1,3,5</query>

- Reset sequence:
<reset></reset>

- Submit prediction Method A (e.g., predict element E2):
<answer>E2</answer>

- Submit prediction Method A (predict element X):
<answer>X</answer>

- Submit prediction Method B (e.g., a=2, b=3):
<answer>a=2,b=3</answer>

1. Initially, the sequence is S = [E1, E2, ..., E{n}].
2. You can perform multiple "insert—query—reset" cycles to gather information.
3. When you believe you have understood the pattern, wait for the system challenge or directly submit parameters.
4. If the prediction is incorrect, the game fails; if correct, the game succeeds.

Notes:
- Valid range for insertion position p is 1 to {n_plus_1}.
- Valid range for query position q is 1 to {n_plus_1} (after insertion).
- You must perform an insert operation before querying.
- You can query at most 3 positions after each insertion.
- You must conduct at least 2 insertion experiments at different positions before submitting a prediction.
"""

    contextualized_rule_zh_1 = """\
欢迎使用“智能交通车队调度系统”。我们将进行一项调度规则推断任务，规则如下：

系统设定了一个长度为 {n} 的初始车队序列 S，包含 {n} 辆常规车辆，分别标记为 E1, E2, ..., E{n}。序列索引从 1 到 {n}。

系统中隐藏着一个紧急调度移位规则：当你在车队队列的位置 p 插入一辆特种应急车辆 X 后，系统会对新车队序列（长度变为 {n_plus_1}）执行循环右移操作，右移的步数 K(p) 遵循一个线性模公式：K(p) = (a × p + b) mod {n_plus_1}，其中 a 和 b 是系统预设的固定参数（范围在 0 到 {n} 之间），在整个调度测试中不会改变。

你的目标是通过交互实验推断出这个调度移位规则，具体可以：
- 方式 A：当系统给出挑战参数（插入位置 {challenge_p} 和查询位置 {challenge_q}）时，正确预测该位置的车辆标识是什么。
- 方式 B：直接给出系统调度参数 a 和 b 的值。

1. **插入操作**：在初始序列的位置 p（范围 1 到 {n_plus_1}）插入应急车辆 X，系统会自动对新序列执行右移调度，然后你可以查询移位后的车队排布。

2. **查询操作**：在插入后，你可以查询当前车队序列中某些位置的车辆。每次插入后最多查询 3 个位置（可以一次查询多个位置，也可以分多次查询）。

3. **重置操作**：移除应急车辆 X，序列恢复到初始状态，结束当前实验回合。

4. **提交预测**：在进行至少 2 次不同位置的插入实验后，你可以提交预测：
   - 方式 A：回答系统给出的挑战（在位置 {challenge_p} 插入后，位置 {challenge_q} 的车辆是什么）。
   - 方式 B：直接给出参数 a 和 b。

每次操作只能包含一个标签，使用以下 XML 格式：

- 插入操作（例如在位置 3 插入）：
<insert>3</insert>

- 查询单个位置（例如查询位置 5）：
<query>5</query>

- 查询多个位置（例如查询位置 1, 3, 5）：
<query>1,3,5</query>

- 重置序列：
<reset></reset>

- 提交预测方式 A（例如预测车辆为 E2）：
<answer>E2</answer>

- 提交预测方式 A（预测车辆为 X）：
<answer>X</answer>

- 提交预测方式 B（例如 a=2, b=3）：
<answer>a=2,b=3</answer>

1. 初始状态下，车队序列为 S = [E1, E2, ..., E{n}]。
2. 你可以多次执行“插入—查询—重置”的循环来收集调度信息。
3. 当你认为掌握了规律后，等待系统挑战或直接提交参数。
4. 如果预测错误，任务失败；如果正确，任务成功。

注意：
- 插入位置 p 的有效范围是 1 到 {n_plus_1}。
- 查询位置 q 的有效范围是 1 到 {n_plus_1}（在插入后）。
- 必须先执行插入操作，才能进行查询。
- 每次插入后最多查询 3 个位置。
- 必须进行至少 2 次不同位置的插入实验后才能提交预测。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Smart Traffic Convoy Scheduling System". We will conduct a scheduling rule deduction task. Here are the rules:

The system has an ordered initial convoy sequence S of length {n}, containing {n} standard vehicles labeled E1, E2, ..., E{n}. The sequence is indexed from 1 to {n}.

I have set up a hidden emergency shift rule: when you insert a special emergency vehicle X at position p in the convoy, the system will perform a cyclic right shift on the new sequence (length becomes {n_plus_1}). The shift amount K(p) follows a linear modular formula: K(p) = (a × p + b) mod {n_plus_1}, where a and b are fixed parameters I preset (ranging from 0 to {n}) and will not change throughout the test.

Your goal is to deduce this shift rule through interactive experiments. You can achieve this by:
- Method A: When I provide challenge parameters (insertion position {challenge_p} and query position {challenge_q}), correctly predict what vehicle is at that position.
- Method B: Directly provide the values of parameters a and b.

1. **Insert Operation**: Insert emergency vehicle X at position p (range 1 to {n_plus_1}) in the initial sequence. The system will automatically perform a right shift on the new sequence, and then you can query the result after shifting.

2. **Query Operation**: After insertion, you can query vehicles at certain positions in the current sequence. You can query at most 3 positions after each insertion (you can query multiple positions at once or in separate queries).

3. **Reset Operation**: Remove emergency vehicle X, restore the sequence to its initial state, and end the current experiment round.

4. **Submit Prediction**: After conducting at least 2 insertion experiments at different positions, you can submit a prediction:
   - Method A: Answer my challenge (after inserting at position {challenge_p}, what vehicle is at position {challenge_q}).
   - Method B: Directly provide parameters a and b.

Each operation can only contain one tag. Use the following XML format:

- Insert operation (e.g., insert at position 3):
<insert>3</insert>

- Query single position (e.g., query position 5):
<query>5</query>

- Query multiple positions (e.g., query positions 1, 3, 5):
<query>1,3,5</query>

- Reset sequence:
<reset></reset>

- Submit prediction Method A (e.g., predict vehicle E2):
<answer>E2</answer>

- Submit prediction Method A (predict vehicle X):
<answer>X</answer>

- Submit prediction Method B (e.g., a=2, b=3):
<answer>a=2,b=3</answer>

1. Initially, the sequence is S = [E1, E2, ..., E{n}].
2. You can perform multiple "insert—query—reset" cycles to gather information.
3. When you believe you have understood the pattern, wait for the system challenge or directly submit parameters.
4. If the prediction is incorrect, the task fails; if correct, the task succeeds.

Notes:
- Valid range for insertion position p is 1 to {n_plus_1}.
- Valid range for query position q is 1 to {n_plus_1} (after insertion).
- You must perform an insert operation before querying.
- You can query at most 3 positions after each insertion.
- You must conduct at least 2 insertion experiments at different positions before submitting a prediction.
"""

    contextualized_rule_zh_2 = """\
欢迎使用“手术室急诊插队排程系统”。我们将进行一项排程规则推断任务，规则如下：

系统设定了一个长度为 {n} 的初始手术排程序列 S，包含 {n} 名常规患者，分别标记为 E1, E2, ..., E{n}。序列索引从 1 到 {n}。

系统中隐藏着一个急诊排程移位规则：当你在排程队列的位置 p 插入一名急诊患者 X 后，系统会对新排程序列（长度变为 {n_plus_1}）执行循环右移操作，右移的步数 K(p) 遵循一个线性模公式：K(p) = (a × p + b) mod {n_plus_1}，其中 a 和 b 是系统预设的固定参数（范围在 0 到 {n} 之间），在整个排程测试中不会改变。

你的目标是通过交互实验推断出这个排程移位规则，具体可以：
- 方式 A：当系统给出挑战参数（插入位置 {challenge_p} 和查询位置 {challenge_q}）时，正确预测该位置安排的是哪位患者。
- 方式 B：直接给出系统排程参数 a 和 b 的值。

1. **插入操作**：在初始序列的位置 p（范围 1 到 {n_plus_1}）插入急诊患者 X，系统会自动对新序列执行右移排程，然后你可以查询移位后的患者安排。

2. **查询操作**：在插入后，你可以查询当前排程序列中某些位置的患者。每次插入后最多查询 3 个位置（可以一次查询多个位置，也可以分多次查询）。

3. **重置操作**：移除急诊患者 X，序列恢复到初始状态，结束当前实验回合。

4. **提交预测**：在进行至少 2 次不同位置的插入实验后，你可以提交预测：
   - 方式 A：回答系统给出的挑战（在位置 {challenge_p} 插入后，位置 {challenge_q} 的患者是谁）。
   - 方式 B：直接给出参数 a 和 b。

每次操作只能包含一个标签，使用以下 XML 格式：

- 插入操作（例如在位置 3 插入）：
<insert>3</insert>

- 查询单个位置（例如查询位置 5）：
<query>5</query>

- 查询多个位置（例如查询位置 1, 3, 5）：
<query>1,3,5</query>

- 重置序列：
<reset></reset>

- 提交预测方式 A（例如预测患者为 E2）：
<answer>E2</answer>

- 提交预测方式 A（预测患者为 X）：
<answer>X</answer>

- 提交预测方式 B（例如 a=2, b=3）：
<answer>a=2,b=3</answer>

1. 初始状态下，排程序列为 S = [E1, E2, ..., E{n}]。
2. 你可以多次执行“插入—查询—重置”的循环来收集排程信息。
3. 当你认为掌握了规律后，等待系统挑战或直接提交参数。
4. 如果预测错误，任务失败；如果正确，任务成功。

注意：
- 插入位置 p 的有效范围是 1 到 {n_plus_1}。
- 查询位置 q 的有效范围是 1 到 {n_plus_1}（在插入后）。
- 必须先执行插入操作，才能进行查询。
- 每次插入后最多查询 3 个位置。
- 必须进行至少 2 次不同位置的插入实验后才能提交预测。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Operating Room Emergency Insertion Scheduling System". We will conduct a scheduling rule deduction task. Here are the rules:

The system has an ordered initial scheduling sequence S of length {n}, containing {n} routine patients labeled E1, E2, ..., E{n}. The sequence is indexed from 1 to {n}.

I have set up a hidden emergency shift rule: when you insert an emergency patient X at position p in the schedule, the system will perform a cyclic right shift on the new sequence (length becomes {n_plus_1}). The shift amount K(p) follows a linear modular formula: K(p) = (a × p + b) mod {n_plus_1}, where a and b are fixed parameters I preset (ranging from 0 to {n}) and will not change throughout the test.

Your goal is to deduce this shift rule through interactive experiments. You can achieve this by:
- Method A: When I provide challenge parameters (insertion position {challenge_p} and query position {challenge_q}), correctly predict which patient is scheduled at that position.
- Method B: Directly provide the values of parameters a and b.

1. **Insert Operation**: Insert emergency patient X at position p (range 1 to {n_plus_1}) in the initial sequence. The system will automatically perform a right shift on the new sequence, and then you can query the result after shifting.

2. **Query Operation**: After insertion, you can query patients at certain positions in the current sequence. You can query at most 3 positions after each insertion (you can query multiple positions at once or in separate queries).

3. **Reset Operation**: Remove emergency patient X, restore the sequence to its initial state, and end the current experiment round.

4. **Submit Prediction**: After conducting at least 2 insertion experiments at different positions, you can submit a prediction:
   - Method A: Answer my challenge (after inserting at position {challenge_p}, which patient is at position {challenge_q}).
   - Method B: Directly provide parameters a and b.

Each operation can only contain one tag. Use the following XML format:

- Insert operation (e.g., insert at position 3):
<insert>3</insert>

- Query single position (e.g., query position 5):
<query>5</query>

- Query multiple positions (e.g., query positions 1, 3, 5):
<query>1,3,5</query>

- Reset sequence:
<reset></reset>

- Submit prediction Method A (e.g., predict patient E2):
<answer>E2</answer>

- Submit prediction Method A (predict patient X):
<answer>X</answer>

- Submit prediction Method B (e.g., a=2, b=3):
<answer>a=2,b=3</answer>

1. Initially, the sequence is S = [E1, E2, ..., E{n}].
2. You can perform multiple "insert—query—reset" cycles to gather information.
3. When you believe you have understood the pattern, wait for the system challenge or directly submit parameters.
4. If the prediction is incorrect, the task fails; if correct, the task succeeds.

Notes:
- Valid range for insertion position p is 1 to {n_plus_1}.
- Valid range for query position q is 1 to {n_plus_1} (after insertion).
- You must perform an insert operation before querying.
- You can query at most 3 positions after each insertion.
- You must conduct at least 2 insertion experiments at different positions before submitting a prediction.
"""

    contextualized_rule_zh_3 = """\
欢迎使用“标准化考场座位轮换系统”。我们将进行一项轮换规则推断任务，规则如下：

系统设定了一个长度为 {n} 的初始考位序列 S，包含 {n} 名常规考生，分别标记为 E1, E2, ..., E{n}。序列索引从 1 到 {n}。

系统中隐藏着一个座位移位规则：当你在考位队列的位置 p 插入一名特需考生 X 后，系统会对新考位序列（长度变为 {n_plus_1}）执行循环右移操作，右移的步数 K(p) 遵循一个线性模公式：K(p) = (a × p + b) mod {n_plus_1}，其中 a 和 b 是系统预设的固定参数（范围在 0 到 {n} 之间），在整个轮换测试中不会改变。

你的目标是通过交互实验推断出这个座位移位规则，具体可以：
- 方式 A：当系统给出挑战参数（插入位置 {challenge_p} 和查询位置 {challenge_q}）时，正确预测该位置安排的是哪位考生。
- 方式 B：直接给出系统轮换参数 a 和 b 的值。

1. **插入操作**：在初始序列的位置 p（范围 1 到 {n_plus_1}）插入特需考生 X，系统会自动对新序列执行右移操作，然后你可以查询移位后的座位排布。

2. **查询操作**：在插入后，你可以查询当前序列中某些位置的考生。每次插入后最多查询 3 个位置（可以一次查询多个位置，也可以分多次查询）。

3. **重置操作**：移除特需考生 X，序列恢复到初始状态，结束当前实验回合。

4. **提交预测**：在进行至少 2 次不同位置的插入实验后，你可以提交预测：
   - 方式 A：回答系统给出的挑战（在位置 {challenge_p} 插入后，位置 {challenge_q} 的考生是谁）。
   - 方式 B：直接给出参数 a 和 b。

每次操作只能包含一个标签，使用以下 XML 格式：

- 插入操作（例如在位置 3 插入）：
<insert>3</insert>

- 查询单个位置（例如查询位置 5）：
<query>5</query>

- 查询多个位置（例如查询位置 1, 3, 5）：
<query>1,3,5</query>

- 重置序列：
<reset></reset>

- 提交预测方式 A（例如预测考生为 E2）：
<answer>E2</answer>

- 提交预测方式 A（预测考生为 X）：
<answer>X</answer>

- 提交预测方式 B（例如 a=2, b=3）：
<answer>a=2,b=3</answer>

1. 初始状态下，序列为 S = [E1, E2, ..., E{n}]。
2. 你可以多次执行“插入—查询—重置”的循环来收集信息。
3. 当你认为掌握了规律后，等待系统挑战或直接提交参数。
4. 如果预测错误，任务失败；如果正确，任务成功。

注意：
- 插入位置 p 的有效范围是 1 到 {n_plus_1}。
- 查询位置 q 的有效范围是 1 到 {n_plus_1}（在插入后）。
- 必须先执行插入操作，才能进行查询。
- 每次插入后最多查询 3 个位置。
- 必须进行至少 2 次不同位置的插入实验后才能提交预测。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Standardized Examination Seat Rotation System". We will conduct a rotation rule deduction task. Here are the rules:

The system has an ordered initial seat sequence S of length {n}, containing {n} regular candidates labeled E1, E2, ..., E{n}. The sequence is indexed from 1 to {n}.

I have set up a hidden seat shift rule: when you insert a special needs candidate X at position p in the queue, the system will perform a cyclic right shift on the new sequence (length becomes {n_plus_1}). The shift amount K(p) follows a linear modular formula: K(p) = (a × p + b) mod {n_plus_1}, where a and b are fixed parameters I preset (ranging from 0 to {n}) and will not change throughout the test.

Your goal is to deduce this shift rule through interactive experiments. You can achieve this by:
- Method A: When I provide challenge parameters (insertion position {challenge_p} and query position {challenge_q}), correctly predict which candidate is seated at that position.
- Method B: Directly provide the values of parameters a and b.

1. **Insert Operation**: Insert special needs candidate X at position p (range 1 to {n_plus_1}) in the initial sequence. The system will automatically perform a right shift on the new sequence, and then you can query the result after shifting.

2. **Query Operation**: After insertion, you can query candidates at certain positions in the current sequence. You can query at most 3 positions after each insertion (you can query multiple positions at once or in separate queries).

3. **Reset Operation**: Remove special needs candidate X, restore the sequence to its initial state, and end the current experiment round.

4. **Submit Prediction**: After conducting at least 2 insertion experiments at different positions, you can submit a prediction:
   - Method A: Answer my challenge (after inserting at position {challenge_p}, which candidate is at position {challenge_q}).
   - Method B: Directly provide parameters a and b.

Each operation can only contain one tag. Use the following XML format:

- Insert operation (e.g., insert at position 3):
<insert>3</insert>

- Query single position (e.g., query position 5):
<query>5</query>

- Query multiple positions (e.g., query positions 1, 3, 5):
<query>1,3,5</query>

- Reset sequence:
<reset></reset>

- Submit prediction Method A (e.g., predict candidate E2):
<answer>E2</answer>

- Submit prediction Method A (predict candidate X):
<answer>X</answer>

- Submit prediction Method B (e.g., a=2, b=3):
<answer>a=2,b=3</answer>

1. Initially, the sequence is S = [E1, E2, ..., E{n}].
2. You can perform multiple "insert—query—reset" cycles to gather information.
3. When you believe you have understood the pattern, wait for the system challenge or directly submit parameters.
4. If the prediction is incorrect, the task fails; if correct, the task succeeds.

Notes:
- Valid range for insertion position p is 1 to {n_plus_1}.
- Valid range for query position q is 1 to {n_plus_1} (after insertion).
- You must perform an insert operation before querying.
- You can query at most 3 positions after each insertion.
- You must conduct at least 2 insertion experiments at different positions before submitting a prediction.
"""

    contextualized_rule_zh_4 = """\
欢迎使用“工业流水线批次调度系统”。我们将进行一项调度规则推断任务，规则如下：

系统设定了一个长度为 {n} 的初始流水线序列 S，包含 {n} 个常规生产批次，分别标记为 E1, E2, ..., E{n}。序列索引从 1 到 {n}。

系统中隐藏着一个产线移位规则：当你在流水线队列的位置 p 插入一个加急测试批次 X 后，系统会对新产线序列（长度变为 {n_plus_1}）执行循环右移操作，右移的步数 K(p) 遵循一个线性模公式：K(p) = (a × p + b) mod {n_plus_1}，其中 a 和 b 是系统预设的固定参数（范围在 0 到 {n} 之间），在整个调度测试中不会改变。

你的目标是通过交互实验推断出这个产线移位规则，具体可以：
- 方式 A：当系统给出挑战参数（插入位置 {challenge_p} 和查询位置 {challenge_q}）时，正确预测该位置流转的是哪个批次。
- 方式 B：直接给出系统调度参数 a 和 b 的值。

1. **插入操作**：在初始序列的位置 p（范围 1 到 {n_plus_1}）插入加急测试批次 X，系统会自动对新序列执行右移操作，然后你可以查询移位后的流水线排布。

2. **查询操作**：在插入后，你可以查询当前序列中某些位置的批次。每次插入后最多查询 3 个位置（可以一次查询多个位置，也可以分多次查询）。

3. **重置操作**：移除加急测试批次 X，序列恢复到初始状态，结束当前实验回合。

4. **提交预测**：在进行至少 2 次不同位置的插入实验后，你可以提交预测：
   - 方式 A：回答系统给出的挑战（在位置 {challenge_p} 插入后，位置 {challenge_q} 的批次是什么）。
   - 方式 B：直接给出参数 a 和 b。

每次操作只能包含一个标签，使用以下 XML 格式：

- 插入操作（例如在位置 3 插入）：
<insert>3</insert>

- 查询单个位置（例如查询位置 5）：
<query>5</query>

- 查询多个位置（例如查询位置 1, 3, 5）：
<query>1,3,5</query>

- 重置序列：
<reset></reset>

- 提交预测方式 A（例如预测批次为 E2）：
<answer>E2</answer>

- 提交预测方式 A（预测批次为 X）：
<answer>X</answer>

- 提交预测方式 B（例如 a=2, b=3):
<answer>a=2,b=3</answer>

1. 初始状态下，序列为 S = [E1, E2, ..., E{n}]。
2. 你可以多次执行“插入—查询—重置”的循环来收集信息。
3. 当你认为掌握了规律后，等待系统挑战或直接提交参数。
4. 如果预测错误，任务失败；如果正确，任务成功。

注意：
- 插入位置 p 的有效范围是 1 到 {n_plus_1}。
- 查询位置 q 的有效范围是 1 到 {n_plus_1}（在插入后）。
- 必须先执行插入操作，才能进行查询。
- 每次插入后最多查询 3 个位置。
- 必须进行至少 2 次不同位置的插入实验后才能提交预测。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Industrial Assembly Line Batch Scheduling System". We will conduct a scheduling rule deduction task. Here are the rules:

The system has an ordered initial assembly line sequence S of length {n}, containing {n} standard production batches labeled E1, E2, ..., E{n}. The sequence is indexed from 1 to {n}.

I have set up a hidden line shift rule: when you insert a rush test batch X at position p in the line, the system will perform a cyclic right shift on the new sequence (length becomes {n_plus_1}). The shift amount K(p) follows a linear modular formula: K(p) = (a × p + b) mod {n_plus_1}, where a and b are fixed parameters I preset (ranging from 0 to {n}) and will not change throughout the test.

Your goal is to deduce this shift rule through interactive experiments. You can achieve this by:
- Method A: When I provide challenge parameters (insertion position {challenge_p} and query position {challenge_q}), correctly predict which batch is processed at that position.
- Method B: Directly provide the values of parameters a and b.

1. **Insert Operation**: Insert rush test batch X at position p (range 1 to {n_plus_1}) in the initial sequence. The system will automatically perform a right shift on the new sequence, and then you can query the result after shifting.

2. **Query Operation**: After insertion, you can query batches at certain positions in the current sequence. You can query at most 3 positions after each insertion (you can query multiple positions at once or in separate queries).

3. **Reset Operation**: Remove rush test batch X, restore the sequence to its initial state, and end the current experiment round.

4. **Submit Prediction**: After conducting at least 2 insertion experiments at different positions, you can submit a prediction:
   - Method A: Answer my challenge (after inserting at position {challenge_p}, which batch is at position {challenge_q}).
   - Method B: Directly provide parameters a and b.

Each operation can only contain one tag. Use the following XML format:

- Insert operation (e.g., insert at position 3):
<insert>3</insert>

- Query single position (e.g., query position 5):
<query>5</query>

- Query multiple positions (e.g., query positions 1, 3, 5):
<query>1,3,5</query>

- Reset sequence:
<reset></reset>

- Submit prediction Method A (e.g., predict batch E2):
<answer>E2</answer>

- Submit prediction Method A (predict batch X):
<answer>X</answer>

- Submit prediction Method B (e.g., a=2, b=3):
<answer>a=2,b=3</answer>

1. Initially, the sequence is S = [E1, E2, ..., E{n}].
2. You can perform multiple "insert—query—reset" cycles to gather information.
3. When you believe you have understood the pattern, wait for the system challenge or directly submit parameters.
4. If the prediction is incorrect, the task fails; if correct, the task succeeds.

Notes:
- Valid range for insertion position p is 1 to {n_plus_1}.
- Valid range for query position q is 1 to {n_plus_1} (after insertion).
- You must perform an insert operation before querying.
- You can query at most 3 positions after each insertion.
- You must conduct at least 2 insertion experiments at different positions before submitting a prediction.
"""

    contextualized_rule_zh_5 = """\
欢迎使用“法院庭审排期轮转系统”。我们将进行一项排期规则推断任务，规则如下：

系统设定了一个长度为 {n} 的初始庭审序列 S，包含 {n} 个常规案件，分别标记为 E1, E2, ..., E{n}。序列索引从 1 到 {n}。

系统中隐藏着一个排期移位规则：当你在排期队列的位置 p 插入一个紧急保全案件 X 后，系统会对新庭审序列（长度变为 {n_plus_1}）执行循环右移操作，右移的步数 K(p) 遵循一个线性模公式：K(p) = (a × p + b) mod {n_plus_1}，其中 a 和 b 是系统预设的固定参数（范围在 0 到 {n} 之间），在整个轮转测试中不会改变。

你的目标是通过交互实验推断出这个排期移位规则，具体可以：
- 方式 A：当系统给出挑战参数（插入位置 {challenge_p} 和查询位置 {challenge_q}）时，正确预测该位置审理的是哪个案件。
- 方式 B：直接给出系统排期参数 a 和 b 的值。

1. **插入操作**：在初始序列的位置 p（范围 1 到 {n_plus_1}）插入紧急保全案件 X，系统会自动对新序列执行右移操作，然后你可以查询移位后的庭审排布。

2. **查询操作**：在插入后，你可以查询当前序列中某些位置的案件。每次插入后最多查询 3 个位置（可以一次查询多个位置，也可以分多次查询）。

3. **重置操作**：移除紧急保全案件 X，序列恢复到初始状态，结束当前实验回合。

4. **提交预测**：在进行至少 2 次不同位置的插入实验后，你可以提交预测：
   - 方式 A：回答系统给出的挑战（在位置 {challenge_p} 插入后，位置 {challenge_q} 的案件是什么）。
   - 方式 B：直接给出参数 a 和 b。

每次操作只能包含一个标签，使用以下 XML 格式：

- 插入操作（例如在位置 3 插入）：
<insert>3</insert>

- 查询单个位置（例如查询位置 5）：
<query>5</query>

- 查询多个位置（例如查询位置 1, 3, 5）：
<query>1,3,5</query>

- 重置序列：
<reset></reset>

- 提交预测方式 A（例如预测案件为 E2）：
<answer>E2</answer>

- 提交预测方式 A（预测案件为 X）：
<answer>X</answer>

- 提交预测方式 B（例如 a=2, b=3）：
<answer>a=2,b=3</answer>

1. 初始状态下，序列为 S = [E1, E2, ..., E{n}]。
2. 你可以多次执行“插入—查询—重置”的循环来收集信息。
3. 当你认为掌握了规律后，等待系统挑战或直接提交参数。
4. 如果预测错误，任务失败；如果正确，任务成功。

注意：
- 插入位置 p 的有效范围是 1 到 {n_plus_1}。
- 查询位置 q 的有效范围是 1 到 {n_plus_1}（在插入后）。
- 必须先执行插入操作，才能进行查询。
- 每次插入后最多查询 3 个位置。
- 必须进行至少 2 次不同位置的插入实验后才能提交预测。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Court Hearing Docket Rotation System". We will conduct a scheduling rule deduction task. Here are the rules:

The system has an ordered initial hearing sequence S of length {n}, containing {n} standard cases labeled E1, E2, ..., E{n}. The sequence is indexed from 1 to {n}.

I have set up a hidden docket shift rule: when you insert an urgent injunction case X at position p in the queue, the system will perform a cyclic right shift on the new sequence (length becomes {n_plus_1}). The shift amount K(p) follows a linear modular formula: K(p) = (a × p + b) mod {n_plus_1}, where a and b are fixed parameters I preset (ranging from 0 to {n}) and will not change throughout the test.

Your goal is to deduce this shift rule through interactive experiments. You can achieve this by:
- Method A: When I provide challenge parameters (insertion position {challenge_p} and query position {challenge_q}), correctly predict which case is heard at that position.
- Method B: Directly provide the values of parameters a and b.

1. **Insert Operation**: Insert urgent injunction case X at position p (range 1 to {n_plus_1}) in the initial sequence. The system will automatically perform a right shift on the new sequence, and then you can query the result after shifting.

2. **Query Operation**: After insertion, you can query cases at certain positions in the current sequence. You can query at most 3 positions after each insertion (you can query multiple positions at once or in separate queries).

3. **Reset Operation**: Remove urgent injunction case X, restore the sequence to its initial state, and end the current experiment round.

4. **Submit Prediction**: After conducting at least 2 insertion experiments at different positions, you can submit a prediction:
   - Method A: Answer my challenge (after inserting at position {challenge_p}, which case is at position {challenge_q}).
   - Method B: Directly provide parameters a and b.

Each operation can only contain one tag. Use the following XML format:

- Insert operation (e.g., insert at position 3):
<insert>3</insert>

- Query single position (e.g., query position 5):
<query>5</query>

- Query multiple positions (e.g., query positions 1, 3, 5):
<query>1,3,5</query>

- Reset sequence:
<reset></reset>

- Submit prediction Method A (e.g., predict case E2):
<answer>E2</answer>

- Submit prediction Method A (predict case X):
<answer>X</answer>

- Submit prediction Method B (e.g., a=2, b=3):
<answer>a=2,b=3</answer>

1. Initially, the sequence is S = [E1, E2, ..., E{n}].
2. You can perform multiple "insert—query—reset" cycles to gather information.
3. When you believe you have understood the pattern, wait for the system challenge or directly submit parameters.
4. If the prediction is incorrect, the task fails; if correct, the task succeeds.

Notes:
- Valid range for insertion position p is 1 to {n_plus_1}.
- Valid range for query position q is 1 to {n_plus_1} (after insertion).
- You must perform an insert operation before querying.
- You can query at most 3 positions after each insertion.
- You must conduct at least 2 insertion experiments at different positions before submitting a prediction.
"""

    tags = ["answer", "insert", "query", "reset"]

    reasoning_type = "归纳推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"n": 4, "a": 1, "b": 0, "challenge_p": 2, "challenge_q": 3},
            2: {"n": 5, "a": 2, "b": 1, "challenge_p": 3, "challenge_q": 4},
            3: {"n": 6, "a": 3, "b": 2, "challenge_p": 4, "challenge_q": 5},
            4: {"n": 7, "a": 4, "b": 3, "challenge_p": 5, "challenge_q": 6},
            5: {"n": 8, "a": 5, "b": 4, "challenge_p": 6, "challenge_q": 7},
        },
        "en": {
            1: {"n": 4, "a": 1, "b": 0, "challenge_p": 2, "challenge_q": 3},
            2: {"n": 5, "a": 2, "b": 1, "challenge_p": 3, "challenge_q": 4},
            3: {"n": 6, "a": 3, "b": 2, "challenge_p": 4, "challenge_q": 5},
            4: {"n": 7, "a": 4, "b": 3, "challenge_p": 5, "challenge_q": 6},
            5: {"n": 8, "a": 5, "b": 4, "challenge_p": 6, "challenge_q": 7},
        },
    }

    def __init__(self, config):
        self.initial_sequence = []
        self.current_sequence = []
        self.n = 0
        self.a = 0
        self.b = 0
        self.challenge_p = 0
        self.challenge_q = 0
        
        self.has_inserted = False
        self.query_count = 0
        self.insert_history = set()
        
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.n = cfg["n"]
        self.a = cfg["a"]
        self.b = cfg["b"]
        self.challenge_p = cfg["challenge_p"]
        self.challenge_q = cfg["challenge_q"]
        
        self.initial_sequence = [f"E{i}" for i in range(1, self.n + 1)]
        self.current_sequence = self.initial_sequence.copy()
        
        self._game_info["n"] = self.n
        self._game_info["n_plus_1"] = self.n + 1
        self._game_info["challenge_p"] = self.challenge_p
        self._game_info["challenge_q"] = self.challenge_q

    def _cycle_right_shift(self, sequence, k):
        if len(sequence) == 0:
            return sequence
        k = k % len(sequence)
        if k == 0:
            return sequence
        return sequence[-k:] + sequence[:-k]

    def _insert_at_position(self, p):
        temp_seq = self.initial_sequence.copy()
        temp_seq.insert(p - 1, "X")
        
        k = (self.a * p + self.b) % (self.n + 1)
        
        self.current_sequence = self._cycle_right_shift(temp_seq, k)
        
        return k

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        if "a=" in raw_ans and "b=" in raw_ans:
            try:
                parts = raw_ans.split(",")
                ans_dict = {}
                for part in parts:
                    k, v = part.split("=")
                    ans_dict[k.strip()] = int(v.strip())
                
                if "a" not in ans_dict or "b" not in ans_dict:
                    return False
                
                return ans_dict["a"] == self.a and ans_dict["b"] == self.b
            except:
                return False
        else:
            temp_seq = self.initial_sequence.copy()
            temp_seq.insert(self.challenge_p - 1, "X")
            k = (self.a * self.challenge_p + self.b) % (self.n + 1)
            correct_seq = self._cycle_right_shift(temp_seq, k)
            correct_answer = correct_seq[self.challenge_q - 1]
            
            return raw_ans == correct_answer

    def _cf_core_produce(self, parsed_info):
        lang = self.config.language
        
        if "insert" in parsed_info:
            try:
                p = int(parsed_info["insert"].strip())
                if p < 1 or p > self.n + 1:
                    return "无效：p 超界（应在 1 到 {} 之间）".format(self.n + 1) if lang == "zh" else f"Invalid: p out of bounds (should be 1 to {self.n + 1})"
                
                k = self._insert_at_position(p)
                self.has_inserted = True
                self.query_count = 0
                self.insert_history.add(p)
                
                return "已在位置 {} 插入 X，已执行移位".format(p) if lang == "zh" else f"Inserted X at position {p}, shift performed"
            except ValueError:
                return "无效：插入位置必须是整数" if lang == "zh" else "Invalid: insertion position must be an integer"
        
        elif "query" in parsed_info:
            if not self.has_inserted:
                return "需先执行插入操作" if lang == "zh" else "Must insert first"
            
            try:
                raw_query = parsed_info["query"].strip()
                if not raw_query:
                    return "无效：查询位置不能为空" if lang == "zh" else "Invalid: query position cannot be empty"
                
                positions = [int(q.strip()) for q in raw_query.split(",")]
                
                if self.query_count + len(positions) > 3:
                    return "本轮已达查询上限，请重置后再试" if lang == "zh" else "Query limit reached for this round, please reset"
                
                for q in positions:
                    if q < 1 or q > self.n + 1:
                        return "无效：查询位置 {} 超界（应在 1 到 {} 之间）".format(q, self.n + 1) if lang == "zh" else f"Invalid: query position {q} out of bounds (should be 1 to {self.n + 1})"
                
                results = []
                for q in positions:
                    element = self.current_sequence[q - 1]
                    results.append(f"位置 {q}: {element}" if lang == "zh" else f"Position {q}: {element}")
                
                self.query_count += len(positions)
                
                return "\n".join(results)
            except ValueError:
                return "无效：查询位置格式错误" if lang == "zh" else "Invalid: query position format error"
        
        elif "reset" in parsed_info:
            self.current_sequence = self.initial_sequence.copy()
            self.has_inserted = False
            self.query_count = 0
            return "已重置到初始序列" if lang == "zh" else "Reset to initial sequence"
        
        else:
            return "无效的操作" if lang == "zh" else "Invalid operation"

    def _cf_make_wrong(self, correct: str) -> str:
        lang = self.config.language
        
        elements = [f"E{i}" for i in range(1, self.n + 1)] + ["X"]
        
        for elem in elements:
            if elem in correct:
                for alt in elements:
                    if alt != elem:
                        return correct.replace(elem, alt, 1)
        
        if lang == "zh":
            return correct + "（数据异常）"
        else:
            return correct + " (data anomaly)"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        lang = self.config.language
        n = self.n
        n_plus_1 = n + 1

        for p in range(1, n_plus_1 + 1):
            temp_seq = self.initial_sequence.copy()
            temp_seq.insert(p - 1, "X")
            k = (self.a * p + self.b) % n_plus_1
            shifted_seq = self._cycle_right_shift(temp_seq, k)

            insert_query = f"<insert>{p}</insert>"
            if lang == "zh":
                insert_answer = f"已在位置 {p} 插入 X，已执行移位"
            else:
                insert_answer = f"Inserted X at position {p}, shift performed"
            results.append({"query": insert_query, "answer": insert_answer})

            query_positions = list(range(1, min(4, n_plus_1 + 1)))
            positions_str = ",".join(str(q) for q in query_positions)
            query_str = f"<query>{positions_str}</query>"
            
            answer_parts = []
            for q in query_positions:
                element = shifted_seq[q - 1]
                if lang == "zh":
                    answer_parts.append(f"位置 {q}: {element}")
                else:
                    answer_parts.append(f"Position {q}: {element}")
            ans = "\n".join(answer_parts)
            results.append({"query": query_str, "answer": ans})

            reset_query = "<reset></reset>"
            if lang == "zh":
                reset_answer = "已重置到初始序列"
            else:
                reset_answer = "Reset to initial sequence"
            results.append({"query": reset_query, "answer": reset_answer})

        return results