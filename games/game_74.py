from .base import Game
import re

class InteractiveSuffixCountingGame(Game):

    game_rule_zh = """\
我们来玩一个"交互式后缀计数同定问题"游戏，规则如下：

游戏设定了一个字母表 Σ = {{a, b, c}}（三个符号）。我已秘密选择了两个隐藏参数：
1. 目标符号 c*，它是 a、b、c 中的某一个；
2. 窗口长度 K，它是一个固定的正整数。

游戏维护一个有序序列 S，初始为空。你可以通过交互操作来推断这两个隐藏参数。

你可以执行以下操作（每次只能执行一个操作）：

1. **追加操作**：在序列尾部追加一个符号（a、b 或 c），系统会返回当前后缀窗口中目标符号的出现次数。
   - 后缀窗口定义：取序列 S 的最后 min(K, 当前序列长度) 个符号。
   - 格式：
   <append>a</append>
   或
   <append>b</append>
   或
   <append>c</append>

2. **查询长度**：查询当前序列的总长度。
   - 格式：
   <query_length></query_length>

3. **预测验证**：提交一个追加计划及其对应的计数预测，系统会逐步验证。若计划长度大于等于 6 且所有预测完全匹配，则游戏胜利。
   - 格式：
   <predict>s1,s2,...,sT|L1,L2,...,LT</predict>
   - 说明：竖线前为追加符号序列，竖线后为预测的计数序列。例如：
   <predict>a,b,c,a,b,c|1,1,2,2,2,3</predict>

4. **最终宣告**：直接提交你推断的目标符号和窗口长度。若正确则游戏胜利。
   - 格式：
   <answer>c*=a, K=3</answer>
   - 说明：c* 为目标符号（a、b 或 c），K 为窗口长度。

- **胜利条件 A**：提交最终宣告，且参数完全正确。
- **胜利条件 B**：提交预测验证，计划长度大于等于 6，且所有计数预测完全匹配。
- **失败条件**：
  - 连续两次最终宣告均错误，或
  - 总追加步数超过 30 步且未满足任一胜利条件。

- 每次只能提交一个操作标签。
- 追加操作会改变序列状态并返回计数反馈。
- 预测验证会实际执行追加操作，因此会改变序列状态。
- 你的目标是通过尽可能少的交互次数同定隐藏参数。
"""

    game_rule_en = """\
Let's play an "Interactive Suffix Counting Identification" game. Here are the rules:

The game uses an alphabet Σ = {{a, b, c}} (three symbols). I have secretly chosen two hidden parameters:
1. Target symbol c*, which is one of a, b, or c;
2. Window length K, which is a fixed positive integer.

The game maintains an ordered sequence S, initially empty. You can infer these two hidden parameters through interactive operations.

You can perform the following operations (one operation per turn):

1. **Append Operation**: Append a symbol (a, b, or c) to the end of the sequence. The system returns the count of the target symbol in the current suffix window.
   - Suffix window definition: Take the last min(K, current sequence length) symbols of sequence S.
   - Format:
   <append>a</append>
   or
   <append>b</append>
   or
   <append>c</append>

2. **Length Query**: Query the total length of the current sequence.
   - Format:
   <query_length></query_length>

3. **Prediction Verification**: Submit an append plan with corresponding count predictions. The system will verify step by step. If the plan length is at least 6 and all predictions match perfectly, you win.
   - Format:
   <predict>s1,s2,...,sT|L1,L2,...,LT</predict>
   - Note: Before the vertical bar is the append symbol sequence, after is the predicted count sequence. Example:
   <predict>a,b,c,a,b,c|1,1,2,2,2,3</predict>

4. **Final Declaration**: Directly submit your inferred target symbol and window length. If correct, you win.
   - Format:
   <answer>c*=a, K=3</answer>
   - Note: c* is the target symbol (a, b, or c), K is the window length.

- **Victory Condition A**: Submit a final declaration with completely correct parameters.
- **Victory Condition B**: Submit a prediction verification with plan length at least 6 and all count predictions matching perfectly.
- **Failure Conditions**:
  - Two consecutive incorrect final declarations, or
  - Total append steps exceed 30 without meeting any victory condition.

- Only one operation tag can be submitted per turn.
- Append operations change the sequence state and return count feedback.
- Prediction verification actually executes append operations, thus changing the sequence state.
- Your goal is to identify the hidden parameters with as few interactions as possible.
"""

    contextualized_rule_zh_1 = """\
【智慧交通监控系统场景】
我们来执行"交通流量后缀计数监控"任务，规则如下：

系统监控了三种类型的车辆：轿车(a)、货车(b)、客车(c)。我已秘密选择了两个隐藏参数：
1. 重点监测车型 c*，它是 a、b、c 中的某一个；
2. 缓存容量 K，它是一个固定的正整数。

系统维护一个有序的过车记录序列 S，初始为空。你可以通过交互操作来推断这两个隐藏参数。

你可以执行以下操作（每次只能执行一个操作）：

1. **追加记录**：在序列尾部追加一条过车记录（a、b 或 c），系统会返回当前缓存窗口中重点监测车型的出现次数。
   - 缓存窗口定义：取序列 S 的最后 min(K, 当前记录总数) 辆车。
   - 格式：
   <append>a</append>
   或
   <append>b</append>
   或
   <append>c</append>

2. **查询总数**：查询当前记录的总长度。
   - 格式：
   <query_length></query_length>

3. **预测验证**：提交一个连续过车计划及其对应的监控计数预测，系统会逐步验证。若计划长度大于等于 6 且所有预测完全匹配，则任务成功。
   - 格式：
   <predict>s1,s2,...,sT|L1,L2,...,LT</predict>
   - 说明：竖线前为车辆类型序列，竖线后为预测的计数序列。例如：
   <predict>a,b,c,a,b,c|1,1,2,2,2,3</predict>

4. **最终宣告**：直接提交你推断的重点监测车型和缓存容量。若正确则任务成功。
   - 格式：
   <answer>c*=a, K=3</answer>
   - 说明：c* 为目标车型（a、b 或 c），K 为缓存容量。

- **胜利条件 A**：提交最终宣告，且参数完全正确。
- **胜利条件 B**：提交预测验证，计划长度大于等于 6，且所有计数预测完全匹配。
- **失败条件**：
  - 连续两次最终宣告均错误，或
  - 总追加步数超过 30 步且未满足任一胜利条件。

- 每次只能提交一个操作标签。
- 追加操作会改变序列状态并返回计数反馈。
- 预测验证会实际执行追加操作，因此会改变序列状态。
- 你的目标是通过尽可能少的交互次数同定隐藏参数。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's execute a "Traffic Flow Suffix Counting Monitoring" task. Here are the rules:

The system monitors three types of vehicles: Car (a), Truck (b), and Bus (c). I have secretly chosen two hidden parameters:
1. Target vehicle type c*, which is one of a, b, or c;
2. Cache window size K, which is a fixed positive integer.

The system maintains an ordered sequence of vehicle passing records S, initially empty. You can infer these two hidden parameters through interactive operations.

You can perform the following operations (one operation per turn):

1. **Append Record**: Append a vehicle passing record (a, b, or c) to the end of the sequence. The system returns the count of the target vehicle type in the current cache window.
   - Cache window definition: Take the last min(K, current total records) vehicles of sequence S.
   - Format:
   <append>a</append>
   or
   <append>b</append>
   or
   <append>c</append>

2. **Length Query**: Query the total length of the current sequence.
   - Format:
   <query_length></query_length>

3. **Prediction Verification**: Submit a continuous vehicle passing plan with corresponding count predictions. The system will verify step by step. If the plan length is at least 6 and all predictions match perfectly, you win.
   - Format:
   <predict>s1,s2,...,sT|L1,L2,...,LT</predict>
   - Note: Before the vertical bar is the vehicle type sequence, after is the predicted count sequence. Example:
   <predict>a,b,c,a,b,c|1,1,2,2,2,3</predict>

4. **Final Declaration**: Directly submit your inferred target vehicle type and cache window size. If correct, you win.
   - Format:
   <answer>c*=a, K=3</answer>
   - Note: c* is the target vehicle (a, b, or c), K is the cache window size.

- **Victory Condition A**: Submit a final declaration with completely correct parameters.
- **Victory Condition B**: Submit a prediction verification with plan length at least 6 and all count predictions matching perfectly.
- **Failure Conditions**:
  - Two consecutive incorrect final declarations, or
  - Total append steps exceed 30 without meeting any victory condition.

- Only one operation tag can be submitted per turn.
- Append operations change the sequence state and return count feedback.
- Prediction verification actually executes append operations, thus changing the sequence state.
- Your goal is to identify the hidden parameters with as few interactions as possible.
"""

    contextualized_rule_zh_2 = """\
【流行病学监控系统场景】
我们来执行"流行病学后缀计数监控"任务，规则如下：

系统录入了三种典型症状病例：发热(a)、咳嗽(b)、乏力(c)。我已秘密选择了两个隐藏参数：
1. 核心症状 c*，它是 a、b、c 中的某一个；
2. 观察窗口 K，它是一个固定的正整数。

系统维护一个有序的病例录入序列 S，初始为空。你可以通过交互操作来推断这两个隐藏参数。

你可以执行以下操作（每次只能执行一个操作）：

1. **录入病例**：在序列尾部录入一个病例的症状（a、b 或 c），系统会返回当前观察窗口中表现出核心症状的病例数量。
   - 观察窗口定义：取序列 S 的最后 min(K, 当前记录总数) 个病例。
   - 格式：
   <append>a</append>
   或
   <append>b</append>
   或
   <append>c</append>

2. **查询总数**：查询当前记录的总病例数。
   - 格式：
   <query_length></query_length>

3. **预测验证**：提交一个连续病例录入计划及其对应的核心症状计数预测，系统会逐步验证。若计划长度大于等于 6 且所有预测完全匹配，则任务成功。
   - 格式：
   <predict>s1,s2,...,sT|L1,L2,...,LT</predict>
   - 说明：竖线前为病例症状序列，竖线后为预测的计数序列。例如：
   <predict>a,b,c,a,b,c|1,1,2,2,2,3</predict>

4. **最终宣告**：直接提交你推断的核心症状和观察窗口。若正确则任务成功。
   - 格式：
   <answer>c*=a, K=3</answer>
   - 说明：c* 为核心症状（a、b 或 c），K 为观察窗口大小。

- **胜利条件 A**：提交最终宣告，且参数完全正确。
- **胜利条件 B**：提交预测验证，计划长度大于等于 6，且所有计数预测完全匹配。
- **失败条件**：
  - 连续两次最终宣告均错误，或
  - 总追加步数超过 30 步且未满足任一胜利条件。

- 每次只能提交一个操作标签。
- 追加操作会改变序列状态并返回计数反馈。
- 预测验证会实际执行追加操作，因此会改变序列状态。
- 你的目标是通过尽可能少的交互次数同定隐藏参数。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's execute an "Epidemiological Suffix Counting Identification" task. Here are the rules:

The system records three types of symptoms: Fever (a), Cough (b), and Fatigue (c). I have secretly chosen two hidden parameters:
1. Primary symptom c*, which is one of a, b, or c;
2. Observation window K, which is a fixed positive integer.

The system maintains an ordered sequence of case symptom records S, initially empty. You can infer these two hidden parameters through interactive operations.

You can perform the following operations (one operation per turn):

1. **Append Record**: Enter a new case symptom (a, b, or c) to the end of the sequence. The system returns the count of the primary symptom in the current observation window.
   - Observation window definition: Take the last min(K, current total records) cases of sequence S.
   - Format:
   <append>a</append>
   or
   <append>b</append>
   or
   <append>c</append>

2. **Length Query**: Query the total length of the current sequence.
   - Format:
   <query_length></query_length>

3. **Prediction Verification**: Submit a continuous case entry plan with corresponding count predictions. The system will verify step by step. If the plan length is at least 6 and all predictions match perfectly, you win.
   - Format:
   <predict>s1,s2,...,sT|L1,L2,...,LT</predict>
   - Note: Before the vertical bar is the case symptom sequence, after is the predicted count sequence. Example:
   <predict>a,b,c,a,b,c|1,1,2,2,2,3</predict>

4. **Final Declaration**: Directly submit your inferred primary symptom and observation window size. If correct, you win.
   - Format:
   <answer>c*=a, K=3</answer>
   - Note: c* is the primary symptom (a, b, or c), K is the observation window size.

- **Victory Condition A**: Submit a final declaration with completely correct parameters.
- **Victory Condition B**: Submit a prediction verification with plan length at least 6 and all count predictions matching perfectly.
- **Failure Conditions**:
  - Two consecutive incorrect final declarations, or
  - Total append steps exceed 30 without meeting any victory condition.

- Only one operation tag can be submitted per turn.
- Append operations change the sequence state and return count feedback.
- Prediction verification actually executes append operations, thus changing the sequence state.
- Your goal is to identify the hidden parameters with as few interactions as possible.
"""

    contextualized_rule_zh_3 = """\
【自适应学习评估系统场景】
我们来执行"学习行为后缀计数评估"任务，规则如下：

系统记录了学生的三种答题表现：优(a)、良(b)、待改进(c)。我已秘密选择了两个隐藏参数：
1. 重点追踪行为 c*，它是 a、b、c 中的某一个；
2. 滑动评估窗口 K，它是一个固定的正整数。

系统维护一个有序的答题表现序列 S，初始为空。你可以通过交互操作来推断这两个隐藏参数。

你可以执行以下操作（每次只能执行一个操作）：

1. **录入表现**：在序列尾部录入一次表现（a、b 或 c），系统会返回当前评估窗口中重点追踪行为的出现次数。
   - 评估窗口定义：取序列 S 的最后 min(K, 当前记录总数) 次表现。
   - 格式：
   <append>a</append>
   或
   <append>b</append>
   或
   <append>c</append>

2. **查询总数**：查询当前记录的总长度。
   - 格式：
   <query_length></query_length>

3. **预测验证**：提交一个连续答题表现计划及其对应的追踪计数预测，系统会逐步验证。若计划长度大于等于 6 且所有预测完全匹配，则任务成功。
   - 格式：
   <predict>s1,s2,...,sT|L1,L2,...,LT</predict>
   - 说明：竖线前为表现类型序列，竖线后为预测的计数序列。例如：
   <predict>a,b,c,a,b,c|1,1,2,2,2,3</predict>

4. **最终宣告**：直接提交你推断的重点追踪行为和评估窗口长度。若正确则任务成功。
   - 格式：
   <answer>c*=a, K=3</answer>
   - 说明：c* 为目标表现行为（a、b 或 c），K 为评估窗口长度。

- **胜利条件 A**：提交最终宣告，且参数完全正确。
- **胜利条件 B**：提交预测验证，计划长度大于等于 6，且所有计数预测完全匹配。
- **失败条件**：
  - 连续两次最终宣告均错误，或
  - 总追加步数超过 30 步且未满足任一胜利条件。

- 每次只能提交一个操作标签。
- 追加操作会改变序列状态并返回计数反馈。
- 预测验证会实际执行追加操作，因此会改变序列状态。
- 你的目标是通过尽可能少的交互次数同定隐藏参数。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's execute a "Learning Behavior Suffix Counting Evaluation" task. Here are the rules:

The system evaluates three types of student performance: Excellent (a), Good (b), and Needs Improvement (c). I have secretly chosen two hidden parameters:
1. Target behavior c*, which is one of a, b, or c;
2. Evaluation window K, which is a fixed positive integer.

The system maintains an ordered sequence of answer performance records S, initially empty. You can infer these two hidden parameters through interactive operations.

You can perform the following operations (one operation per turn):

1. **Append Record**: Enter a student's answer performance (a, b, or c) to the end of the sequence. The system returns the count of the target behavior in the current evaluation window.
   - Evaluation window definition: Take the last min(K, current total records) performances of sequence S.
   - Format:
   <append>a</append>
   or
   <append>b</append>
   or
   <append>c</append>

2. **Length Query**: Query the total length of the current sequence.
   - Format:
   <query_length></query_length>

3. **Prediction Verification**: Submit a continuous performance entry plan with corresponding count predictions. The system will verify step by step. If the plan length is at least 6 and all predictions match perfectly, you win.
   - Format:
   <predict>s1,s2,...,sT|L1,L2,...,LT</predict>
   - Note: Before the vertical bar is the performance sequence, after is the predicted count sequence. Example:
   <predict>a,b,c,a,b,c|1,1,2,2,2,3</predict>

4. **Final Declaration**: Directly submit your inferred target behavior and evaluation window size. If correct, you win.
   - Format:
   <answer>c*=a, K=3</answer>
   - Note: c* is the target behavior (a, b, or c), K is the evaluation window size.

- **Victory Condition A**: Submit a final declaration with completely correct parameters.
- **Victory Condition B**: Submit a prediction verification with plan length at least 6 and all count predictions matching perfectly.
- **Failure Conditions**:
  - Two consecutive incorrect final declarations, or
  - Total append steps exceed 30 without meeting any victory condition.

- Only one operation tag can be submitted per turn.
- Append operations change the sequence state and return count feedback.
- Prediction verification actually executes append operations, thus changing the sequence state.
- Your goal is to identify the hidden parameters with as few interactions as possible.
"""

    contextualized_rule_zh_4 = """\
【智能制造质检流水线场景】
我们来执行"工业良率后缀计数抽检"任务，规则如下：

流水线产出了三种品质级别的产品：一等品(a)、二等品(b)、三等品(c)。我已秘密选择了两个隐藏参数：
1. 核心质检等级 c*，它是 a、b、c 中的某一个；
2. 抽样批次容量 K，它是一个固定的正整数。

系统维护一个有序的产出记录序列 S，初始为空。你可以通过交互操作来推断这两个隐藏参数。

你可以执行以下操作（每次只能执行一个操作）：

1. **记录产品**：在序列尾部记录一件刚下线的产品等级（a、b 或 c），系统会返回当前抽样批次中属于核心质检等级的数量。
   - 抽样批次定义：取序列 S 的最后 min(K, 当前记录总数) 件产品。
   - 格式：
   <append>a</append>
   或
   <append>b</append>
   或
   <append>c</append>

2. **查询总数**：查询当前记录的总产量。
   - 格式：
   <query_length></query_length>

3. **预测验证**：提交一个连续产线出货计划及其对应的抽检计数预测，系统会逐步验证。若计划长度大于等于 6 且所有预测完全匹配，则任务成功。
   - 格式：
   <predict>s1,s2,...,sT|L1,L2,...,LT</predict>
   - 说明：竖线前为产品等级序列，竖线后为预测的计数序列。例如：
   <predict>a,b,c,a,b,c|1,1,2,2,2,3</predict>

4. **最终宣告**：直接提交你推断的核心质检等级和抽样批次容量。若正确则任务成功。
   - 格式：
   <answer>c*=a, K=3</answer>
   - 说明：c* 为目标品质等级（a、b 或 c），K 为抽样批次容量。

- **胜利条件 A**：提交最终宣告，且参数完全正确。
- **胜利条件 B**：提交预测验证，计划长度大于等于 6，且所有计数预测完全匹配。
- **失败条件**：
  - 连续两次最终宣告均错误，或
  - 总追加步数超过 30 步且未满足任一胜利条件。

- 每次只能提交一个操作标签。
- 追加操作会改变序列状态并返回计数反馈。
- 预测验证会实际执行追加操作，因此会改变序列状态。
- 你的目标是通过尽可能少的交互次数同定隐藏参数。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's execute an "Industrial Quality Suffix Counting Inspection" task. Here are the rules:

The assembly line produces three quality grades of products: First-class (a), Second-class (b), and Third-class (c). I have secretly chosen two hidden parameters:
1. Key quality grade c*, which is one of a, b, or c;
2. Sampling batch size K, which is a fixed positive integer.

The system maintains an ordered sequence of product output records S, initially empty. You can infer these two hidden parameters through interactive operations.

You can perform the following operations (one operation per turn):

1. **Append Record**: Output a product grade (a, b, or c) from the assembly line and record it. The system returns the count of the key quality grade in the current sampling batch.
   - Sampling batch definition: Take the last min(K, current total output) products of sequence S.
   - Format:
   <append>a</append>
   or
   <append>b</append>
   or
   <append>c</append>

2. **Length Query**: Query the total length of the current sequence.
   - Format:
   <query_length></query_length>

3. **Prediction Verification**: Submit a continuous product output plan with corresponding count predictions. The system will verify step by step. If the plan length is at least 6 and all predictions match perfectly, you win.
   - Format:
   <predict>s1,s2,...,sT|L1,L2,...,LT</predict>
   - Note: Before the vertical bar is the product grade sequence, after is the predicted count sequence. Example:
   <predict>a,b,c,a,b,c|1,1,2,2,2,3</predict>

4. **Final Declaration**: Directly submit your inferred key quality grade and sampling batch size. If correct, you win.
   - Format:
   <answer>c*=a, K=3</answer>
   - Note: c* is the key quality grade (a, b, or c), K is the sampling batch size.

- **Victory Condition A**: Submit a final declaration with completely correct parameters.
- **Victory Condition B**: Submit a prediction verification with plan length at least 6 and all count predictions matching perfectly.
- **Failure Conditions**:
  - Two consecutive incorrect final declarations, or
  - Total append steps exceed 30 without meeting any victory condition.

- Only one operation tag can be submitted per turn.
- Append operations change the sequence state and return count feedback.
- Prediction verification actually executes append operations, thus changing the sequence state.
- Your goal is to identify the hidden parameters with as few interactions as possible.
"""

    contextualized_rule_zh_5 = """\
【司法卷宗自动审查系统场景】
我们来执行"司法督察后缀计数审阅"任务，规则如下：

系统对归档的三类卷宗进行审查：民事(a)、刑事(b)、行政(c)。我已秘密选择了两个隐藏参数：
1. 重点督察类型 c*，它是 a、b、c 中的某一个；
2. 审阅队列容量 K，它是一个固定的正整数。

系统维护一个有序的案件归档序列 S，初始为空。你可以通过交互操作来推断这两个隐藏参数。

你可以执行以下操作（每次只能执行一个操作）：

1. **归档卷宗**：在序列尾部归档一份案件（a、b 或 c），系统会返回当前审阅队列中属于重点督察类型的卷宗数量。
   - 审阅队列定义：取序列 S 的最后 min(K, 当前记录总数) 份归档卷宗。
   - 格式：
   <append>a</append>
   或
   <append>b</append>
   或
   <append>c</append>

2. **查询总数**：查询当前归档案件的总长度。
   - 格式：
   <query_length></query_length>

3. **预测验证**：提交一个连续归档计划及其对应的审阅计数预测，系统会逐步验证。若计划长度大于等于 6 且所有预测完全匹配，则任务成功。
   - 格式：
   <predict>s1,s2,...,sT|L1,L2,...,LT</predict>
   - 说明：竖线前为案件类型序列，竖线后为预测的计数序列。例如：
   <predict>a,b,c,a,b,c|1,1,2,2,2,3</predict>

4. **最终宣告**：直接提交你推断的重点督察类型和审阅队列容量。若正确则任务成功。
   - 格式：
   <answer>c*=a, K=3</answer>
   - 说明：c* 为目标卷宗类型（a、b 或 c），K 为审阅队列容量。

- **胜利条件 A**：提交最终宣告，且参数完全正确。
- **胜利条件 B**：提交预测验证，计划长度大于等于 6，且所有计数预测完全匹配。
- **失败条件**：
  - 连续两次最终宣告均错误，或
  - 总追加步数超过 30 步且未满足任一胜利条件。

- 每次只能提交一个操作标签。
- 追加操作会改变序列状态并返回计数反馈。
- 预测验证会实际执行追加操作，因此会改变序列状态。
- 你的目标是通过尽可能少的交互次数同定隐藏参数。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's execute a "Judicial Case Suffix Counting Review" task. Here are the rules:

The system reviews three types of archived cases: Civil (a), Criminal (b), and Administrative (c). I have secretly chosen two hidden parameters:
1. Target case type c*, which is one of a, b, or c;
2. Review queue capacity K, which is a fixed positive integer.

The system maintains an ordered sequence of case archive records S, initially empty. You can infer these two hidden parameters through interactive operations.

You can perform the following operations (one operation per turn):

1. **Append Record**: Archive a case record (a, b, or c) to the end of the sequence. The system returns the count of the target case type in the current review queue.
   - Review queue definition: Take the last min(K, current total records) archived cases of sequence S.
   - Format:
   <append>a</append>
   or
   <append>b</append>
   or
   <append>c</append>

2. **Length Query**: Query the total length of the current sequence.
   - Format:
   <query_length></query_length>

3. **Prediction Verification**: Submit a continuous case archiving plan with corresponding count predictions. The system will verify step by step. If the plan length is at least 6 and all predictions match perfectly, you win.
   - Format:
   <predict>s1,s2,...,sT|L1,L2,...,LT</predict>
   - Note: Before the vertical bar is the case type sequence, after is the predicted count sequence. Example:
   <predict>a,b,c,a,b,c|1,1,2,2,2,3</predict>

4. **Final Declaration**: Directly submit your inferred target case type and review queue capacity. If correct, you win.
   - Format:
   <answer>c*=a, K=3</answer>
   - Note: c* is the target case type (a, b, or c), K is the review queue capacity.

- **Victory Condition A**: Submit a final declaration with completely correct parameters.
- **Victory Condition B**: Submit a prediction verification with plan length at least 6 and all count predictions matching perfectly.
- **Failure Conditions**:
  - Two consecutive incorrect final declarations, or
  - Total append steps exceed 30 without meeting any victory condition.

- Only one operation tag can be submitted per turn.
- Append operations change the sequence state and return count feedback.
- Prediction verification actually executes append operations, thus changing the sequence state.
- Your goal is to identify the hidden parameters with as few interactions as possible.
"""

    tags = ["answer", "append", "query_length", "predict"]
    
    reasoning_type = "归纳推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"K": 2, "c_star": "a"},
            2: {"K": 3, "c_star": "b"},
            3: {"K": 4, "c_star": "c"},
            4: {"K": 5, "c_star": "a"},
            5: {"K": 7, "c_star": "b"},
        },
        "en": {
            1: {"K": 2, "c_star": "a"},
            2: {"K": 3, "c_star": "b"},
            3: {"K": 4, "c_star": "c"},
            4: {"K": 5, "c_star": "a"},
            5: {"K": 7, "c_star": "b"},
        },
    }

    def __init__(self, config):
        self.sequence = []
        self.K = 0
        self.c_star = ""
        self.append_count = 0
        self.wrong_answer_count = 0
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.K = cfg["K"]
        self.c_star = cfg["c_star"]
        
        self.sequence = []
        self.append_count = 0
        self.wrong_answer_count = 0
        
        self._game_info = {}

    def _compute_count(self):
        window_size = min(self.K, len(self.sequence))
        if window_size == 0:
            return 0
        suffix_window = self.sequence[-window_size:]
        return suffix_window.count(self.c_star)

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        for kv in kv_pairs:
            if "=" not in kv:
                continue
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "c*" not in ans_dict or "K" not in ans_dict:
            return False
        
        try:
            submitted_c_star = ans_dict["c*"]
            submitted_K = int(ans_dict["K"])
            
            if submitted_c_star == self.c_star and submitted_K == self.K:
                return True
            else:
                self.wrong_answer_count += 1
                return False
        except:
            self.wrong_answer_count += 1
            return False

    def _cf_core_produce(self, parsed_info):
        is_zh = self.config.language == "zh"
        
        if "append" in parsed_info:
            symbol = parsed_info["append"].strip().lower()
            
            if symbol not in ['a', 'b', 'c']:
                return "错误：符号必须是 a、b 或 c。" if is_zh else "Error: Symbol must be a, b, or c."
            
            self.sequence.append(symbol)
            self.append_count += 1
            
            if self.append_count > 30:
                self.state.set_state("failed", "exceeded maximum append operations")
                return "失败：追加操作超过 30 次。" if is_zh else "Failed: Append operations exceeded 30."
            
            count = self._compute_count()
            return f"计数：{count}" if is_zh else f"Count: {count}"
        
        elif "query_length" in parsed_info:
            length = len(self.sequence)
            return f"长度：{length}" if is_zh else f"Length: {length}"
        
        elif "predict" in parsed_info:
            raw_predict = parsed_info["predict"].strip()
            
            saved_sequence = list(self.sequence)
            saved_append_count = self.append_count
            
            try:
                if "|" not in raw_predict:
                    raise ValueError("Invalid format")
                
                symbols_part, counts_part = raw_predict.split("|", 1)
                symbols = [s.strip().lower() for s in symbols_part.split(",") if s.strip()]
                counts = [int(c.strip()) for c in counts_part.split(",") if c.strip()]
                
                if len(symbols) != len(counts):
                    raise ValueError("Length mismatch")
                
                if len(symbols) < 6:
                    return "错误：预测序列长度必须大于等于 6。" if is_zh else "Error: Prediction sequence length must be at least 6."
                
                for sym in symbols:
                    if sym not in ['a', 'b', 'c']:
                        raise ValueError("Invalid symbol")
                
                response_parts = []
                all_match = True
                mismatch_step = -1
                
                for i, (sym, predicted_count) in enumerate(zip(symbols, counts)):
                    self.sequence.append(sym)
                    self.append_count += 1
                    
                    if self.append_count > 30:
                        self.state.set_state("failed", "exceeded maximum append operations during prediction")
                        return "失败：追加操作超过 30 次。" if is_zh else "Failed: Append operations exceeded 30."
                    
                    actual_count = self._compute_count()
                    
                    step_result = f"步骤 {i+1}：真实计数 = {actual_count}" if is_zh else f"Step {i+1}: Actual count = {actual_count}"
                    response_parts.append(step_result)
                    
                    if actual_count != predicted_count:
                        all_match = False
                        mismatch_step = i + 1
                        break
                
                if all_match:
                    self.state.set_state("success", "prediction verified")
                    verdict = "预测判定：通过。游戏胜利！" if is_zh else "Prediction Verdict: Passed. You win!"
                else:
                    verdict = f"预测判定：未通过（第 {mismatch_step} 步不匹配）。" if is_zh else f"Prediction Verdict: Failed (mismatch at step {mismatch_step})."
                
                response_parts.append(verdict)
                return "\n".join(response_parts)
                
            except Exception as e:
                self.sequence = saved_sequence
                self.append_count = saved_append_count
                return "错误：预测格式无效。正确格式为 <predict>s1,s2,...|L1,L2,...</predict>" if is_zh else "Error: Invalid prediction format. Correct format: <predict>s1,s2,...|L1,L2,...</predict>"
        
        else:
            raise ValueError("No valid operation tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        is_zh = self.config.language == "zh"
        
        saved_sequence = list(self.sequence)
        saved_append_count = self.append_count
        
        symbols_cycle = ['a', 'b', 'c']
        num_appends = max(self.K + 2, 6)
        
        for i in range(num_appends):
            sym = symbols_cycle[i % 3]
            
            self.sequence.append(sym)
            count = self._compute_count()
            ans_str = f"计数：{count}" if is_zh else f"Count: {count}"
            
            queries.append({
                "query": f"<append>{sym}</append>",
                "answer": ans_str
            })
        
        length = len(self.sequence)
        len_str = f"长度：{length}" if is_zh else f"Length: {length}"
        queries.append({
            "query": "<query_length></query_length>",
            "answer": len_str
        })
        
        self.sequence = saved_sequence
        self.append_count = saved_append_count
        
        return queries

    def step(self, response: str):
        try:
            parsed_info = self.parse(response)
            
            if "answer" in parsed_info:
                is_success = self.evaluate(parsed_info)
                is_zh = self.config.language == "zh"
                
                if is_success:
                    res = "判定：正确。游戏胜利！" if is_zh else "Verdict: Correct. You win!"
                    self.state.set_state("success", "correct answer")
                    self.state.add_message("user", res)
                else:
                    if self.wrong_answer_count >= 2:
                        res = "判定：错误。连续两次错误，游戏失败。" if is_zh else "Verdict: Incorrect. Two consecutive errors, game failed."
                        self.state.set_state("failed", "two consecutive incorrect answers")
                    else:
                        res = f"判定：错误。这是第 {self.wrong_answer_count} 次错误宣告。" if is_zh else f"Verdict: Incorrect. This is error #{self.wrong_answer_count}."
                    self.state.add_message("user", res)
            
            else:
                self.wrong_answer_count = 0
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))
        
        return self.state

    def _cf_make_wrong(self, correct: str) -> str:
        import re as _re
        is_zh = self.config.language == "zh"

        if is_zh:
            m = _re.match(r'^计数：(\d+)$', correct)
            if m:
                wrong_val = int(m.group(1)) + 1
                return f"计数：{wrong_val}"
            m = _re.match(r'^长度：(\d+)$', correct)
            if m:
                wrong_val = int(m.group(1)) + 1
                return f"长度：{wrong_val}"
        else:
            m = _re.match(r'^Count:\s*(\d+)$', correct)
            if m:
                wrong_val = int(m.group(1)) + 1
                return f"Count: {wrong_val}"
            m = _re.match(r'^Length:\s*(\d+)$', correct)
            if m:
                wrong_val = int(m.group(1)) + 1
                return f"Length: {wrong_val}"

        return correct