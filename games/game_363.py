import re
import itertools
from .base import Game

class EvolvingClassificationGame(Game):

    game_rule_zh = """\
我们来玩一个"演化分类推理"游戏，规则如下：

游戏设定了一个包含 N 个元素的集合，每个元素具有一个分类属性，分类只有四种：A、B、C、D。这些元素除了分类属性外没有其他区别。N 的具体值对你是未知的。

存在一个未知的基础分布 B，记为 (bA, bB, bC, bD)，其中各分量为非负整数，且四个分量之和等于 N。

系统按离散时间步演化，时间步记为 t = 1, 2, 3, ...。演化规则是公开且固定的：每次演化时，各类别的计数按照 A→B→C→D→A 的顺序进行循环右移一格。具体来说，从 t-1 步到 t 步的变化为：
- t 步的 A 类计数 = t-1 步的 D 类计数
- t 步的 B 类计数 = t-1 步的 A 类计数
- t 步的 C 类计数 = t-1 步的 B 类计数
- t 步的 D 类计数 = t-1 步的 C 类计数

第 1 步的分布等于基础分布 B 的某个循环排列（具体相位未知），随后各步按上述规则演化。

你的目标是推断出基础分布 B。

游戏从第 1 步开始。在每个时间步，你可以：

1. **提出问题**（可选）：针对当前步的分布，你可以提出以下类型的问题：
   - **定量问题**（每步最多 2 个）：
     - 单类计数：询问"当前步类别 X 的计数是多少？"（X 为 A、B、C 或 D 之一）
     - 两类总和：询问"当前步类别 X 与类别 Y 的计数之和是多少？"（X、Y 为两个不同的类别）
   - **比较问题**（每步最多 1 个）：
     - 大于比较：询问"当前步类别 X 的计数是否大于类别 Y？"
     - 等于比较：询问"当前步类别 X 的计数是否等于类别 Y？"

2. **推进时间步**（可选）：发出推进指令，系统将进入下一个时间步，并按演化规则更新分布。推进不消耗当前步的问题配额。进入新步后，问题配额重置。

3. **提交最终答案**（可选）：当你收集到足够信息后，可以选择以下两种终局方式之一：
   - **预测式终局**：请求系统给出一个你未观察过的验证步 t，你需要一次性给出该步 A、B、C、D 四个类别的完整计数。
   - **规则式终局**：直接提交你推测的基础分布 B = (bA, bB, bC, bD)。系统将根据演化规则生成各步分布，并用你已收集的所有历史反馈进行一致性检验。

每次只能提出一个问题或发出一个指令。请使用以下 XML 格式：

- 单类计数查询（例如询问类别 A）：
<query_single>A</query_single>

- 两类总和查询（例如询问 A 和 B 的总和）：
<query_sum>A,B</query_sum>

- 大于比较查询（例如询问 A 是否大于 B）：
<query_greater>A,B</query_greater>

- 等于比较查询（例如询问 A 是否等于 B）：
<query_equal>A,B</query_equal>

- 推进到下一步：
<next_step></next_step>

- 预测式终局（请求验证）：
<request_predict></request_predict>

- 预测式终局答案（例如预测 A=3, B=2, C=4, D=1）：
<answer_predict>A=3,B=2,C=4,D=1</answer_predict>

- 规则式终局（提交基础分布，例如 bA=3, bB=2, bC=4, bD=1）：
<answer_base>bA=3,bB=2,bC=4,bD=1</answer_base>

- 探索最多允许到第 10 步。
- 每步的定量问题配额为 2 个，比较问题配额为 1 个。
- 成功条件：任一终局请求判定为成功（预测正确或通过一致性检验）。
- 失败条件（任一成立即失败）：
  - 探索已达第 10 步后仍未成功提交终局请求。
  - 累计终局请求失败达到 3 次。
  - 在某个时间步超出该步的提问配额（记为一次违例），累计违例达到 2 次。
"""

    game_rule_en = """\
Let's play an "Evolving Classification Inference" game. Here are the rules:

The game involves a set of N elements. Each element has a classification attribute that can only be one of four categories: A, B, C, or D. These elements have no other distinguishing features apart from their classification. The specific value of N is unknown to you.

There exists an unknown base distribution B, denoted as (bA, bB, bC, bD), where each component is a non-negative integer and the sum of the four components equals N.

The system evolves in discrete time steps, denoted as t = 1, 2, 3, .... The evolution rule is public and fixed: at each evolution, the counts of each category undergo a cyclic right shift in the order A→B→C→D→A. Specifically, from step t-1 to step t:
- A count at step t = D count at step t-1
- B count at step t = A count at step t-1
- C count at step t = B count at step t-1
- D count at step t = C count at step t-1

The distribution at step 1 equals some cyclic permutation of the base distribution B (the specific phase is unknown), and subsequent steps evolve according to the above rule.

Your goal is to infer the base distribution B.

The game starts at step 1. At each time step, you can:

1. **Ask questions** (optional): You may ask the following types of questions about the current step's distribution:
   - **Quantitative questions** (at most 2 per step):
     - Single category count: "What is the count of category X at the current step?" (X is one of A, B, C, or D)
     - Two-category sum: "What is the sum of counts of category X and category Y at the current step?" (X and Y are two different categories)
   - **Comparison questions** (at most 1 per step):
     - Greater-than comparison: "Is the count of category X greater than category Y at the current step?"
     - Equal-to comparison: "Is the count of category X equal to category Y at the current step?"

2. **Advance time step** (optional): Issue an advance instruction, and the system will move to the next time step and update the distribution according to the evolution rule. Advancing does not consume the current step's question quota. Upon entering a new step, the question quota resets.

3. **Submit final answer** (optional): When you have collected enough information, you may choose one of the following two termination methods:
   - **Prediction termination**: Request the system to provide a verification step t that you have not observed. You must provide the complete counts for A, B, C, and D at that step in one attempt.
   - **Base distribution termination**: Directly submit your inferred base distribution B = (bA, bB, bC, bD). The system will generate the distribution at each step according to the evolution rule and perform a consistency check against all historical feedback you have collected.

You can only ask one question or issue one instruction at a time. Please use the following XML format:

- Single category count query (e.g., asking about category A):
<query_single>A</query_single>

- Two-category sum query (e.g., asking for the sum of A and B):
<query_sum>A,B</query_sum>

- Greater-than comparison query (e.g., asking if A is greater than B):
<query_greater>A,B</query_greater>

- Equal-to comparison query (e.g., asking if A equals B):
<query_equal>A,B</query_equal>

- Advance to the next step:
<next_step></next_step>

- Request prediction termination:
<request_predict></request_predict>

- Prediction termination answer (e.g., predicting A=3, B=2, C=4, D=1):
<answer_predict>A=3,B=2,C=4,D=1</answer_predict>

- Base distribution termination (e.g., submitting bA=3, bB=2, bC=4, bD=1):
<answer_base>bA=3,bB=2,bC=4,bD=1</answer_base>

- Exploration is allowed up to step 10.
- Each step has a quota of 2 quantitative questions and 1 comparison question.
- Success condition: Any termination request is judged successful (prediction correct or passes consistency check).
- Failure conditions (any one triggers failure):
  - Exploration reaches step 10 without a successful termination request.
  - Cumulative termination request failures reach 3.
  - Exceeding the question quota at any time step (counted as one violation), with cumulative violations reaching 2.
"""

    contextualized_rule_zh_1 = """\
作为智能交通调度员，你正在进行一项"枢纽流量演化推理"任务，规则如下：

系统管辖着一个包含 N 辆自动驾驶车辆的集合，每辆车被分配到四个交通枢纽之一：枢纽 A、枢纽 B、枢纽 C、枢纽 D。这些车辆除了所在枢纽属性外没有其他区别。N 的具体值对你是未知的。

存在一个未知的基础分布基准 B，记为 (bA, bB, bC, bD)，其中各分量为非负整数，且四个分量之和等于 N。

交通系统按离散时间步（调度周期）运行，时间步记为 t = 1, 2, 3, ...。调度规则是公开且固定的：每次调度时，各枢纽的车辆计数按照 A→B→C→D→A 的顺序进行循环右移一格。具体来说，从 t-1 步到 t 步的变化为：
- t 步的枢纽 A 计数 = t-1 步的枢纽 D 计数
- t 步的枢纽 B 计数 = t-1 步的枢纽 A 计数
- t 步的枢纽 C 计数 = t-1 步的枢纽 B 计数
- t 步的枢纽 D 计数 = t-1 步的枢纽 C 计数

第 1 步的分布等于基础分布 B 的某个循环排列（具体相位未知），随后各步按上述规则演化。

你的目标是推断出基础分布 B。

任务从第 1 步开始。在每个时间步，你可以：

1. **提出问题**（可选）：针对当前步的分布，你可以提出以下类型的问题：
   - **定量问题**（每步最多 2 个）：
     - 单个枢纽计数：询问"当前步枢纽 X 的车辆计数是多少？"（X 为 A、B、C 或 D 之一）
     - 两枢纽总和：询问"当前步枢纽 X 与枢纽 Y 的车辆计数之和是多少？"（X、Y 为两个不同的枢纽）
   - **比较问题**（每步最多 1 个）：
     - 大于比较：询问"当前步枢纽 X 的车辆计数是否大于枢纽 Y？"
     - 等于比较：询问"当前步枢纽 X 的车辆计数是否等于枢纽 Y？"

2. **推进时间步**（可选）：发出推进指令，系统将进入下一个时间步，并按调度规则更新分布。推进不消耗当前步的问题配额。进入新步后，问题配额重置。

3. **提交最终答案**（可选）：当你收集到足够信息后，可以选择以下两种终局方式之一：
   - **预测式终局**：请求系统给出一个你未观察过的验证步 t，你需要一次性给出该步 A、B、C、D 四个枢纽的完整车辆计数。
   - **规则式终局**：直接提交你推测的基础分布 B = (bA, bB, bC, bD)。系统将根据调度规则生成各步分布，并用你已收集的所有历史反馈进行一致性检验。

每次只能提出一个问题或发出一个指令。请使用与原版一致的 XML 格式进行查询和回答（只需将"类别"对应理解为"枢纽"）：

- 单个枢纽计数查询（例如询问枢纽 A）：
<query_single>A</query_single>

- 两枢纽总和查询（例如询问 A 和 B 的总和）：
<query_sum>A,B</query_sum>

- 大于比较查询（例如询问 A 是否大于 B）：
<query_greater>A,B</query_greater>

- 等于比较查询（例如询问 A 是否等于 B）：
<query_equal>A,B</query_equal>

- 推进到下一步：
<next_step></next_step>

- 预测式终局（请求验证）：
<request_predict></request_predict>

- 预测式终局答案（例如预测 A=3, B=2, C=4, D=1）：
<answer_predict>A=3,B=2,C=4,D=1</answer_predict>

- 规则式终局（提交基础分布，例如 bA=3, bB=2, bC=4, bD=1）：
<answer_base>bA=3,bB=2,bC=4,bD=1</answer_base>

- 探索最多允许到第 10 步。
- 每步的定量问题配额为 2 个，比较问题配额为 1 个。
- 成功条件：任一终局请求判定为成功（预测正确或通过一致性检验）。
- 失败条件（任一成立即失败）：
  - 探索已达第 10 步后仍未成功提交终局请求。
  - 累计终局请求失败达到 3 次。
  - 在某个时间步超出该步的提问配额（记为一次违例），累计违例达到 2 次。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
As a smart traffic dispatcher, you are performing a "Hub Flow Evolutionary Inference" task. Here are the rules:

The system manages a set of N autonomous vehicles. Each vehicle is assigned to one of four traffic hubs: Hub A, Hub B, Hub C, or Hub D. These vehicles have no other distinguishing features apart from their assigned Hub. The specific value of N is unknown to you.

There exists an unknown base distribution B, denoted as (bA, bB, bC, bD), where each component is a non-negative integer and the sum of the four components equals N.

The traffic system operates in discrete time steps (dispatch cycles), denoted as t = 1, 2, 3, .... The dispatch rule is public and fixed: at each cycle, the vehicles count of each Hub undergoes a cyclic right shift in the order A→B→C→D→A. Specifically, from step t-1 to step t:
- Hub A count at step t = Hub D count at step t-1
- Hub B count at step t = Hub A count at step t-1
- Hub C count at step t = Hub B count at step t-1
- Hub D count at step t = Hub C count at step t-1

The distribution at step 1 equals some cyclic permutation of the base distribution B (the specific phase is unknown), and subsequent steps evolve according to the above rule.

Your goal is to infer the base distribution B.

The task starts at step 1. At each time step, you can:

1. **Ask questions** (optional): You may ask the following types of questions about the current step's distribution:
   - **Quantitative questions** (at most 2 per step):
     - Single hub count: "What is the vehicles count of Hub X at the current step?" (X is one of A, B, C, or D)
     - Two-hub sum: "What is the sum of vehicles counts of Hub X and Hub Y at the current step?" (X and Y are two different Hubs)
   - **Comparison questions** (at most 1 per step):
     - Greater-than comparison: "Is the vehicles count of Hub X greater than Hub Y at the current step?"
     - Equal-to comparison: "Is the vehicles count of Hub X equal to Hub Y at the current step?"

2. **Advance time step** (optional): Issue an advance instruction, and the system will move to the next time step and update the distribution according to the dispatch rule. Advancing does not consume the current step's question quota. Upon entering a new step, the question quota resets.

3. **Submit final answer** (optional): When you have collected enough information, you may choose one of the following two termination methods:
   - **Prediction termination**: Request the system to provide a verification step t that you have not observed. You must provide the complete vehicles counts for Hubs A, B, C, and D at that step in one attempt.
   - **Base distribution termination**: Directly submit your inferred base distribution B = (bA, bB, bC, bD). The system will generate the distribution at each step according to the dispatch rule and perform a consistency check against all historical feedback you have collected.

You can only ask one question or issue one instruction at a time. Please use the following XML format:

- Single hub count query:
<query_single>A</query_single>

- Two-hub sum query:
<query_sum>A,B</query_sum>

- Greater-than comparison query:
<query_greater>A,B</query_greater>

- Equal-to comparison query:
<query_equal>A,B</query_equal>

- Advance to the next step:
<next_step></next_step>

- Request prediction termination:
<request_predict></request_predict>

- Prediction termination answer:
<answer_predict>A=3,B=2,C=4,D=1</answer_predict>

- Base distribution termination:
<answer_base>bA=3,bB=2,bC=4,bD=1</answer_base>

- Exploration is allowed up to step 10.
- Each step has a quota of 2 quantitative questions and 1 comparison question.
- Success condition: Any termination request is judged successful (prediction correct or passes consistency check).
- Failure conditions (any one triggers failure):
  - Exploration reaches step 10 without a successful termination request.
  - Cumulative termination request failures reach 3.
  - Exceeding the question quota at any time step (counted as one violation), with cumulative violations reaching 2.
"""

    contextualized_rule_zh_2 = """\
作为医疗实验室主管，你正在进行一项"样本流转演化推理"任务，规则如下：

实验室管辖着一个包含 N 个医疗样本的集合，每个样本被分配到四个检测区之一：检测区 A、检测区 B、检测区 C、检测区 D。这些样本除了所在检测区属性外没有其他区别。N 的具体值对你是未知的。

存在一个未知的基础分布基准 B，记为 (bA, bB, bC, bD)，其中各分量为非负整数，且四个分量之和等于 N。

实验室按离散时间步（检测批次）运行，时间步记为 t = 1, 2, 3, ...。流转规则是公开且固定的：每次流转时，各检测区的样本计数按照 A→B→C→D→A 的顺序进行循环右移一格。具体来说，从 t-1 步到 t 步的变化为：
- t 步的检测区 A 计数 = t-1 步的检测区 D 计数
- t 步的检测区 B 计数 = t-1 步的检测区 A 计数
- t 步的检测区 C 计数 = t-1 步的检测区 B 计数
- t 步的检测区 D 计数 = t-1 步的检测区 C 计数

第 1 步的分布等于基础分布 B 的某个循环排列（具体相位未知），随后各步按上述规则演化。

你的目标是推断出基础分布 B。

任务从第 1 步开始。在每个时间步，你可以：

1. **提出问题**（可选）：针对当前步的分布，你可以提出以下类型的问题：
   - **定量问题**（每步最多 2 个）：
     - 单个检测区计数：询问"当前步检测区 X 的样本计数是多少？"（X 为 A、B、C 或 D 之一）
     - 两检测区总和：询问"当前步检测区 X 与检测区 Y 的样本计数之和是多少？"（X、Y 为两个不同的检测区）
   - **比较问题**（每步最多 1 个）：
     - 大于比较：询问"当前步检测区 X 的样本计数是否大于检测区 Y？"
     - 等于比较：询问"当前步检测区 X 的样本计数是否等于检测区 Y？"

2. **推进时间步**（可选）：发出推进指令，系统将进入下一个时间步，并按流转规则更新分布。推进不消耗当前步的问题配额。进入新步后，问题配额重置。

3. **提交最终答案**（可选）：当你收集到足够信息后，可以选择以下两种终局方式之一：
   - **预测式终局**：请求系统给出一个你未观察过的验证步 t，你需要一次性给出该步 A、B、C、D 四个检测区的完整样本计数。
   - **规则式终局**：直接提交你推测的基础分布 B = (bA, bB, bC, bD)。系统将根据流转规则生成各步分布，并用你已收集的所有历史反馈进行一致性检验。

每次只能提出一个问题或发出一个指令。请使用与原版一致的 XML 格式进行查询和回答（只需将"类别"对应理解为"检测区"）：

- 单个检测区计数查询：
<query_single>A</query_single>

- 两检测区总和查询：
<query_sum>A,B</query_sum>

- 大于比较查询：
<query_greater>A,B</query_greater>

- 等于比较查询：
<query_equal>A,B</query_equal>

- 推进到下一步：
<next_step></next_step>

- 预测式终局（请求验证）：
<request_predict></request_predict>

- 预测式终局答案：
<answer_predict>A=3,B=2,C=4,D=1</answer_predict>

- 规则式终局（提交基础分布）：
<answer_base>bA=3,bB=2,bC=4,bD=1</answer_base>

- 探索最多允许到第 10 步。
- 每步的定量问题配额为 2 个，比较问题配额为 1 个。
- 成功条件：任一终局请求判定为成功（预测正确或通过一致性检验）。
- 失败条件（任一成立即失败）：
  - 探索已达第 10 步后仍未成功提交终局请求。
  - 累计终局请求失败达到 3 次。
  - 在某个时间步超出该步的提问配额（记为一次违例），累计违例达到 2 次。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
As a medical laboratory supervisor, you are performing a "Sample Flow Evolutionary Inference" task. Here are the rules:

The system manages a set of N medical samples. Each sample is assigned to one of four testing zones: Zone A, Zone B, Zone C, or Zone D. These samples have no other distinguishing features apart from their assigned Zone. The specific value of N is unknown to you.

There exists an unknown base distribution B, denoted as (bA, bB, bC, bD), where each component is a non-negative integer and the sum of the four components equals N.

The laboratory operates in discrete time steps (testing batches), denoted as t = 1, 2, 3, .... The transfer rule is public and fixed: at each cycle, the samples count of each Zone undergoes a cyclic right shift in the order A→B→C→D→A. Specifically, from step t-1 to step t:
- Zone A count at step t = Zone D count at step t-1
- Zone B count at step t = Zone A count at step t-1
- Zone C count at step t = Zone B count at step t-1
- Zone D count at step t = Zone C count at step t-1

The distribution at step 1 equals some cyclic permutation of the base distribution B (the specific phase is unknown), and subsequent steps evolve according to the above rule.

Your goal is to infer the base distribution B.

The task starts at step 1. At each time step, you can:

1. **Ask questions** (optional): You may ask the following types of questions about the current step's distribution:
   - **Quantitative questions** (at most 2 per step):
     - Single zone count: "What is the samples count of Zone X at the current step?" (X is one of A, B, C, or D)
     - Two-zone sum: "What is the sum of samples counts of Zone X and Zone Y at the current step?" (X and Y are two different Zones)
   - **Comparison questions** (at most 1 per step):
     - Greater-than comparison: "Is the samples count of Zone X greater than Zone Y at the current step?"
     - Equal-to comparison: "Is the samples count of Zone X equal to Zone Y at the current step?"

2. **Advance time step** (optional): Issue an advance instruction, and the system will move to the next time step and update the distribution according to the transfer rule. Advancing does not consume the current step's question quota. Upon entering a new step, the question quota resets.

3. **Submit final answer** (optional): When you have collected enough information, you may choose one of the following two termination methods:
   - **Prediction termination**: Request the system to provide a verification step t that you have not observed. You must provide the complete samples counts for Zones A, B, C, and D at that step in one attempt.
   - **Base distribution termination**: Directly submit your inferred base distribution B = (bA, bB, bC, bD). The system will generate the distribution at each step according to the transfer rule and perform a consistency check against all historical feedback you have collected.

(Use the same XML tags as the original game: <query_single>, <query_sum>, <query_greater>, <query_equal>, <next_step>, <request_predict>, <answer_predict>, <answer_base>)

- Exploration is allowed up to step 10.
- Each step has a quota of 2 quantitative questions and 1 comparison question.
- Success condition: Any termination request is judged successful.
- Failure conditions (any one triggers failure):
  - Exploration reaches step 10 without a successful termination request.
  - Cumulative termination request failures reach 3.
  - Exceeding the question quota at any time step, with cumulative violations reaching 2.
"""

    contextualized_rule_zh_3 = """\
作为教学教务管理者，你正在进行一项"教学模块轮转推理"任务，规则如下：

教学计划管辖着一个包含 N 名学生的集合，每名学生被分配到四个学习模块之一：模块 A、模块 B、模块 C、模块 D。这些学生除了所在模块属性外没有其他区别。N 的具体值对你是未知的。

存在一个未知的基础分布基准 B，记为 (bA, bB, bC, bD)，其中各分量为非负整数，且四个分量之和等于 N。

教学计划按离散时间步（学期周期）推进，时间步记为 t = 1, 2, 3, ...。轮转规则是公开且固定的：每次学期更替时，各模块的学生计数按照 A→B→C→D→A 的顺序进行循环右移一格。具体来说，从 t-1 步到 t 步的变化为：
- t 步的模块 A 计数 = t-1 步的模块 D 计数
- t 步的模块 B 计数 = t-1 步的模块 A 计数
- t 步的模块 C 计数 = t-1 步的模块 B 计数
- t 步的模块 D 计数 = t-1 步的模块 C 计数

第 1 步的分布等于基础分布 B 的某个循环排列（具体相位未知），随后各步按上述规则演化。

你的目标是推断出基础分布 B。

任务从第 1 步开始。在每个时间步，你可以：

1. **提出问题**（可选）：针对当前步的分布，你可以提出以下类型的问题：
   - **定量问题**（每步最多 2 个）：
     - 单个模块计数：询问"当前步模块 X 的学生计数是多少？"（X 为 A、B、C 或 D 之一）
     - 两模块总和：询问"当前步模块 X 与模块 Y 的学生计数之和是多少？"（X、Y 为两个不同的模块）
   - **比较问题**（每步最多 1 个）：
     - 大于比较：询问"当前步模块 X 的学生计数是否大于模块 Y？"
     - 等于比较：询问"当前步模块 X 的学生计数是否等于模块 Y？"

2. **推进时间步**（可选）：发出推进指令，系统将进入下一个时间步，并按轮转规则更新分布。推进不消耗当前步的问题配额。进入新步后，问题配额重置。

3. **提交最终答案**（可选）：当你收集到足够信息后，可以选择以下两种终局方式之一：
   - **预测式终局**：请求系统给出一个你未观察过的验证步 t，你需要一次性给出该步 A、B、C、D 四个模块的完整学生计数。
   - **规则式终局**：直接提交你推测的基础分布 B = (bA, bB, bC, bD)。系统将根据轮转规则生成各步分布，并用你已收集的所有历史反馈进行一致性检验。

每次只能提出一个问题或发出一个指令。请使用与原版一致的 XML 格式进行查询和回答（只需将"类别"对应理解为"模块"）：

- 单个模块计数查询：
<query_single>A</query_single>

- 两模块总和查询：
<query_sum>A,B</query_sum>

- 大于比较查询：
<query_greater>A,B</query_greater>

- 等于比较查询：
<query_equal>A,B</query_equal>

- 推进到下一步：
<next_step></next_step>

- 预测式终局（请求验证）：
<request_predict></request_predict>

- 预测式终局答案：
<answer_predict>A=3,B=2,C=4,D=1</answer_predict>

- 规则式终局（提交基础分布）：
<answer_base>bA=3,bB=2,bC=4,bD=1</answer_base>

（与原版游戏约束一致，最多探索 10 步，每步配额2定量1比较，失败条件相同）
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
As an academic administrator, you are performing a "Module Rotation Evolutionary Inference" task. Here are the rules:

The system manages a set of N students. Each student is assigned to one of four learning modules: Module A, Module B, Module C, or Module D. These students have no other distinguishing features apart from their assigned Module. The specific value of N is unknown to you.

There exists an unknown base distribution B, denoted as (bA, bB, bC, bD), where each component is a non-negative integer and the sum of the four components equals N.

The curriculum advances in discrete time steps (academic terms), denoted as t = 1, 2, 3, .... The rotation rule is public and fixed: at each term, the students count of each Module undergoes a cyclic right shift in the order A→B→C→D→A. Specifically, from step t-1 to step t:
- Module A count at step t = Module D count at step t-1
- Module B count at step t = Module A count at step t-1
- Module C count at step t = Module B count at step t-1
- Module D count at step t = Module C count at step t-1

The distribution at step 1 equals some cyclic permutation of the base distribution B (the specific phase is unknown), and subsequent steps evolve according to the above rule.

Your goal is to infer the base distribution B.

The task starts at step 1. At each time step, you can:

1. **Ask questions** (optional): You may ask the following types of questions about the current step's distribution:
   - **Quantitative questions** (at most 2 per step):
     - Single module count: "What is the students count of Module X at the current step?" (X is one of A, B, C, or D)
     - Two-module sum: "What is the sum of students counts of Module X and Module Y at the current step?" (X and Y are two different Modules)
   - **Comparison questions** (at most 1 per step):
     - Greater-than comparison: "Is the students count of Module X greater than Module Y at the current step?"
     - Equal-to comparison: "Is the students count of Module X equal to Module Y at the current step?"

2. **Advance time step** (optional): Issue an advance instruction, and the system will move to the next time step and update the distribution according to the rotation rule. Advancing does not consume the current step's question quota. Upon entering a new step, the question quota resets.

3. **Submit final answer** (optional): When you have collected enough information, you may choose one of the following two termination methods:
   - **Prediction termination**: Request the system to provide a verification step t that you have not observed. You must provide the complete students counts for Modules A, B, C, and D at that step in one attempt.
   - **Base distribution termination**: Directly submit your inferred base distribution B = (bA, bB, bC, bD). The system will generate the distribution at each step according to the rotation rule and perform a consistency check against all historical feedback you have collected.

(Use the same XML tags as the original game: <query_single>, <query_sum>, <query_greater>, <query_equal>, <next_step>, <request_predict>, <answer_predict>, <answer_base>)

- Exploration is allowed up to step 10.
- Each step has a quota of 2 quantitative questions and 1 comparison question.
- Success condition: Any termination request is judged successful.
- Failure conditions (any one triggers failure):
  - Exploration reaches step 10 without a successful termination request.
  - Cumulative termination request failures reach 3.
  - Exceeding the question quota at any time step, with cumulative violations reaching 2.
"""

    contextualized_rule_zh_4 = """\
作为工业生产线长，你正在进行一项"流水线工序演化推理"任务，规则如下：

生产线管辖着一个包含 N 个生产组件的集合，每个组件被分配到四个工作站之一：工作站 A、工作站 B、工作站 C、工作站 D。这些组件除了所在工作站属性外没有其他区别。N 的具体值对你是未知的。

存在一个未知的基础分布基准 B，记为 (bA, bB, bC, bD)，其中各分量为非负整数，且四个分量之和等于 N。

生产线按离散时间步（生产节拍）运行，时间步记为 t = 1, 2, 3, ...。工序流转规则是公开且固定的：每次流转时，各工作站的组件计数按照 A→B→C→D→A 的顺序进行循环右移一格。具体来说，从 t-1 步到 t 步的变化为：
- t 步的工作站 A 计数 = t-1 步的工作站 D 计数
- t 步的工作站 B 计数 = t-1 步的工作站 A 计数
- t 步的工作站 C 计数 = t-1 步的工作站 B 计数
- t 步的工作站 D 计数 = t-1 步的工作站 C 计数

第 1 步的分布等于基础分布 B 的某个循环排列（具体相位未知），随后各步按上述规则演化。

你的目标是推断出基础分布 B。

任务从第 1 步开始。在每个时间步，你可以：

1. **提出问题**（可选）：针对当前步的分布，你可以提出以下类型的问题：
   - **定量问题**（每步最多 2 个）：
     - 单个工作站计数：询问"当前步工作站 X 的组件计数是多少？"（X 为 A、B、C 或 D 之一）
     - 两工作站总和：询问"当前步工作站 X 与工作站 Y 的组件计数之和是多少？"（X、Y 为两个不同的工作站）
   - **比较问题**（每步最多 1 个）：
     - 大于比较：询问"当前步工作站 X 的组件计数是否大于工作站 Y？"
     - 等于比较：询问"当前步工作站 X 的组件计数是否等于工作站 Y？"

2. **推进时间步**（可选）：发出推进指令，系统将进入下一个时间步，并按工序流转规则更新分布。推进不消耗当前步的问题配额。进入新步后，问题配额重置。

3. **提交最终答案**（可选）：当你收集到足够信息后，可以选择以下两种终局方式之一：
   - **预测式终局**：请求系统给出一个你未观察过的验证步 t，你需要一次性给出该步 A、B、C、D 四个工作站的完整组件计数。
   - **规则式终局**：直接提交你推测的基础分布 B = (bA, bB, bC, bD)。系统将根据工序流转规则生成各步分布，并用你已收集的所有历史反馈进行一致性检验。

每次只能提出一个问题或发出一个指令。请使用与原版一致的 XML 格式进行查询和回答（只需将"类别"对应理解为"工作站"）：

- 单个工作站计数查询：
<query_single>A</query_single>

- 两工作站总和查询：
<query_sum>A,B</query_sum>

- 大于比较查询：
<query_greater>A,B</query_greater>

- 等于比较查询：
<query_equal>A,B</query_equal>

- 推进到下一步：
<next_step></next_step>

- 预测式终局（请求验证）：
<request_predict></request_predict>

- 预测式终局答案：
<answer_predict>A=3,B=2,C=4,D=1</answer_predict>

- 规则式终局（提交基础分布）：
<answer_base>bA=3,bB=2,bC=4,bD=1</answer_base>

（与原版游戏约束一致，最多探索 10 步，每步配额2定量1比较，失败条件相同）
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
As a production line manager, you are performing an "Assembly Line Evolutionary Inference" task. Here are the rules:

The system manages a set of N manufacturing components. Each component is assigned to one of four workstations: Station A, Station B, Station C, or Station D. These components have no other distinguishing features apart from their assigned Station. The specific value of N is unknown to you.

There exists an unknown base distribution B, denoted as (bA, bB, bC, bD), where each component is a non-negative integer and the sum of the four components equals N.

The production line operates in discrete time steps (production cycles), denoted as t = 1, 2, 3, .... The workflow rule is public and fixed: at each cycle, the components count of each Station undergoes a cyclic right shift in the order A→B→C→D→A. Specifically, from step t-1 to step t:
- Station A count at step t = Station D count at step t-1
- Station B count at step t = Station A count at step t-1
- Station C count at step t = Station B count at step t-1
- Station D count at step t = Station C count at step t-1

The distribution at step 1 equals some cyclic permutation of the base distribution B (the specific phase is unknown), and subsequent steps evolve according to the above rule.

Your goal is to infer the base distribution B.

The task starts at step 1. At each time step, you can:

1. **Ask questions** (optional): You may ask the following types of questions about the current step's distribution:
   - **Quantitative questions** (at most 2 per step):
     - Single station count: "What is the components count of Station X at the current step?" (X is one of A, B, C, or D)
     - Two-station sum: "What is the sum of components counts of Station X and Station Y at the current step?" (X and Y are two different Stations)
   - **Comparison questions** (at most 1 per step):
     - Greater-than comparison: "Is the components count of Station X greater than Station Y at the current step?"
     - Equal-to comparison: "Is the components count of Station X equal to Station Y at the current step?"

2. **Advance time step** (optional): Issue an advance instruction, and the system will move to the next time step and update the distribution according to the workflow rule. Advancing does not consume the current step's question quota. Upon entering a new step, the question quota resets.

3. **Submit final answer** (optional): When you have collected enough information, you may choose one of the following two termination methods:
   - **Prediction termination**: Request the system to provide a verification step t that you have not observed. You must provide the complete components counts for Stations A, B, C, and D at that step in one attempt.
   - **Base distribution termination**: Directly submit your inferred base distribution B = (bA, bB, bC, bD). The system will generate the distribution at each step according to the workflow rule and perform a consistency check against all historical feedback you have collected.

(Use the same XML tags as the original game: <query_single>, <query_sum>, <query_greater>, <query_equal>, <next_step>, <request_predict>, <answer_predict>, <answer_base>)

- Exploration is allowed up to step 10.
- Each step has a quota of 2 quantitative questions and 1 comparison question.
- Success condition: Any termination request is judged successful.
- Failure conditions (any one triggers failure):
  - Exploration reaches step 10 without a successful termination request.
  - Cumulative termination request failures reach 3.
  - Exceeding the question quota at any time step, with cumulative violations reaching 2.
"""

    contextualized_rule_zh_5 = """\
作为司法审查协调员，你正在进行一项"案件卷宗流转推理"任务，规则如下：

司法审查流程管辖着一个包含 N 份案件卷宗的集合，每份卷宗被分配到四个审查组之一：审查组 A、审查组 B、审查组 C、审查组 D。这些卷宗除了所在审查组属性外没有其他区别。N 的具体值对你是未知的。

存在一个未知的基础分布基准 B，记为 (bA, bB, bC, bD)，其中各分量为非负整数，且四个分量之和等于 N。

司法审查流程按离散时间步（审查周期）推进，时间步记为 t = 1, 2, 3, ...。卷宗移交规则是公开且固定的：每次移交时，各审查组的卷宗计数按照 A→B→C→D→A 的顺序进行循环右移一格。具体来说，从 t-1 步到 t 步的变化为：
- t 步的审查组 A 计数 = t-1 步的审查组 D 计数
- t 步的审查组 B 计数 = t-1 步的审查组 A 计数
- t 步的审查组 C 计数 = t-1 步的审查组 B 计数
- t 步的审查组 D 计数 = t-1 步的审查组 C 计数

第 1 步的分布等于基础分布 B 的某个循环排列（具体相位未知），随后各步按上述规则演化。

你的目标是推断出基础分布 B。

任务从第 1 步开始。在每个时间步，你可以：

1. **提出问题**（可选）：针对当前步的分布，你可以提出以下类型的问题：
   - **定量问题**（每步最多 2 个）：
     - 单个审查组计数：询问"当前步审查组 X 的卷宗计数是多少？"（X 为 A、B、C 或 D 之一）
     - 两审查组总和：询问"当前步审查组 X 与审查组 Y 的卷宗计数之和是多少？"（X、Y 为两个不同的审查组）
   - **比较问题**（每步最多 1 个）：
     - 大于比较：询问"当前步审查组 X 的卷宗计数是否大于审查组 Y？"
     - 等于比较：询问"当前步审查组 X 的卷宗计数是否等于审查组 Y？"

2. **推进时间步**（可选）：发出推进指令，系统将进入下一个时间步，并按卷宗移交规则更新分布。推进不消耗当前步的问题配额。进入新步后，问题配额重置。

3. **提交最终答案**（可选）：当你收集到足够信息后，可以选择以下两种终局方式之一：
   - **预测式终局**：请求系统给出一个你未观察过的验证步 t，你需要一次性给出该步 A、B、C、D 四个审查组的完整卷宗计数。
   - **规则式终局**：直接提交你推测的基础分布 B = (bA, bB, bC, bD)。系统将根据卷宗移交规则生成各步分布，并用你已收集的所有历史反馈进行一致性检验。

每次只能提出一个问题或发出一个指令。请使用与原版一致的 XML 格式进行查询和回答（只需将"类别"对应理解为"审查组"）：

- 单个审查组计数查询：
<query_single>A</query_single>

- 两审查组总和查询：
<query_sum>A,B</query_sum>

- 大于比较查询：
<query_greater>A,B</query_greater>

- 等于比较查询：
<query_equal>A,B</query_equal>

- 推进到下一步：
<next_step></next_step>

- 预测式终局（请求验证）：
<request_predict></request_predict>

- 预测式终局答案：
<answer_predict>A=3,B=2,C=4,D=1</answer_predict>

- 规则式终局（提交基础分布）：
<answer_base>bA=3,bB=2,bC=4,bD=1</answer_base>

（与原版游戏约束一致，最多探索 10 步，每步配额2定量1比较，失败条件相同）
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
As a judicial review coordinator, you are performing a "Case File Transfer Evolutionary Inference" task. Here are the rules:

The system manages a set of N case files. Each file is assigned to one of four review panels: Panel A, Panel B, Panel C, or Panel D. These files have no other distinguishing features apart from their assigned Panel. The specific value of N is unknown to you.

There exists an unknown base distribution B, denoted as (bA, bB, bC, bD), where each component is a non-negative integer and the sum of the four components equals N.

The judicial review process advances in discrete time steps (review cycles), denoted as t = 1, 2, 3, .... The transfer rule is public and fixed: at each cycle, the files count of each Panel undergoes a cyclic right shift in the order A→B→C→D→A. Specifically, from step t-1 to step t:
- Panel A count at step t = Panel D count at step t-1
- Panel B count at step t = Panel A count at step t-1
- Panel C count at step t = Panel B count at step t-1
- Panel D count at step t = Panel C count at step t-1

The distribution at step 1 equals some cyclic permutation of the base distribution B (the specific phase is unknown), and subsequent steps evolve according to the above rule.

Your goal is to infer the base distribution B.

The task starts at step 1. At each time step, you can:

1. **Ask questions** (optional): You may ask the following types of questions about the current step's distribution:
   - **Quantitative questions** (at most 2 per step):
     - Single panel count: "What is the files count of Panel X at the current step?" (X is one of A, B, C, or D)
     - Two-panel sum: "What is the sum of files counts of Panel X and Panel Y at the current step?" (X and Y are two different Panels)
   - **Comparison questions** (at most 1 per step):
     - Greater-than comparison: "Is the files count of Panel X greater than Panel Y at the current step?"
     - Equal-to comparison: "Is the files count of Panel X equal to Panel Y at the current step?"

2. **Advance time step** (optional): Issue an advance instruction, and the system will move to the next time step and update the distribution according to the transfer rule. Advancing does not consume the current step's question quota. Upon entering a new step, the question quota resets.

3. **Submit final answer** (optional): When you have collected enough information, you may choose one of the following two termination methods:
   - **Prediction termination**: Request the system to provide a verification step t that you have not observed. You must provide the complete files counts for Panels A, B, C, and D at that step in one attempt.
   - **Base distribution termination**: Directly submit your inferred base distribution B = (bA, bB, bC, bD). The system will generate the distribution at each step according to the transfer rule and perform a consistency check against all historical feedback you have collected.

(Use the same XML tags as the original game: <query_single>, <query_sum>, <query_greater>, <query_equal>, <next_step>, <request_predict>, <answer_predict>, <answer_base>)

- Exploration is allowed up to step 10.
- Each step has a quota of 2 quantitative questions and 1 comparison question.
- Success condition: Any termination request is judged successful.
- Failure conditions (any one triggers failure):
  - Exploration reaches step 10 without a successful termination request.
  - Cumulative termination request failures reach 3.
  - Exceeding the question quota at any time step, with cumulative violations reaching 2.
"""

    tags = ["query_single", "query_sum", "query_greater", "query_equal", 
            "next_step", "request_predict", "answer_predict", "answer_base"]

    reasoning_type = "归纳推理"
    data_structure = "集合"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"n": 4, "base": [1, 1, 1, 1], "phase": 0},
            2: {"n": 8, "base": [1, 2, 2, 3], "phase": 1},
            3: {"n": 10, "base": [1, 2, 3, 4], "phase": 0},
            4: {"n": 12, "base": [1, 2, 3, 6], "phase": 2},
            5: {"n": 15, "base": [2, 3, 4, 6], "phase": 3},
        },
        "en": {
            1: {"n": 4, "base": [1, 1, 1, 1], "phase": 0},
            2: {"n": 8, "base": [1, 2, 2, 3], "phase": 1},
            3: {"n": 10, "base": [1, 2, 3, 4], "phase": 0},
            4: {"n": 12, "base": [1, 2, 3, 6], "phase": 2},
            5: {"n": 15, "base": [2, 3, 4, 6], "phase": 3},
        },
    }

    def __init__(self, config):
        self.current_step = 1
        self.query_count_quant = 0
        self.query_count_comp = 0
        self.violation_count = 0
        self.failure_count = 0
        self.history = []
        self.in_predict_mode = False
        self.predict_step = None
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
        
        self.base_dist = cfg["base"]
        self.phase = cfg["phase"]
        
        self.initial_dist = self._cyclic_shift(self.base_dist, self.phase)

    def _cyclic_shift(self, dist, k):
        k = k % 4
        return dist[-k:] + dist[:-k] if k > 0 else dist[:]

    def _get_distribution(self, t):
        total_shifts = self.phase + (t - 1)
        return self._cyclic_shift(self.base_dist, total_shifts)

    def _reset_step_quota(self):
        self.query_count_quant = 0
        self.query_count_comp = 0

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        categories = ["A", "B", "C", "D"]
        
        current_dist = self._get_distribution(self.current_step)
        dist_dict = {"A": current_dist[0], "B": current_dist[1], 
                     "C": current_dist[2], "D": current_dist[3]}
        
        yes_res = "Yes" if self.config.language == "en" else "是"
        no_res = "No" if self.config.language == "en" else "否"

        for cat in categories:
            queries.append({
                "query": f"<query_single>{cat}</query_single>",
                "answer": str(dist_dict[cat])
            })

        for c1, c2 in itertools.combinations(categories, 2):
            val = dist_dict[c1] + dist_dict[c2]
            queries.append({
                "query": f"<query_sum>{c1},{c2}</query_sum>",
                "answer": str(val)
            })

        for c1, c2 in itertools.permutations(categories, 2):
            is_greater = dist_dict[c1] > dist_dict[c2]
            ans = yes_res if is_greater else no_res
            queries.append({
                "query": f"<query_greater>{c1},{c2}</query_greater>",
                "answer": ans
            })

        for c1, c2 in itertools.combinations(categories, 2):
            is_equal = dist_dict[c1] == dist_dict[c2]
            ans = yes_res if is_equal else no_res
            queries.append({
                "query": f"<query_equal>{c1},{c2}</query_equal>",
                "answer": ans
            })

        return queries

    def evaluate(self, parsed_info):
        if "answer_predict" in parsed_info:
            if not self.in_predict_mode or self.predict_step is None:
                return False
            
            try:
                raw_ans = parsed_info["answer_predict"]
                parts = [x.strip() for x in raw_ans.split(",")]
                ans_dict = {}
                for part in parts:
                    if "=" not in part:
                        return False
                    k, v = part.split("=", 1)
                    ans_dict[k.strip()] = int(v.strip())
                
                if set(ans_dict.keys()) != {"A", "B", "C", "D"}:
                    return False
                
                true_dist = self._get_distribution(self.predict_step)
                true_dict = {"A": true_dist[0], "B": true_dist[1], 
                           "C": true_dist[2], "D": true_dist[3]}
                
                return ans_dict == true_dict
                
            except:
                return False
        
        elif "answer_base" in parsed_info:
            try:
                raw_ans = parsed_info["answer_base"]
                parts = [x.strip() for x in raw_ans.split(",")]
                ans_dict = {}
                for part in parts:
                    if "=" not in part:
                        return False
                    k, v = part.split("=", 1)
                    ans_dict[k.strip()] = int(v.strip())
                
                if set(ans_dict.keys()) != {"bA", "bB", "bC", "bD"}:
                    return False
                
                submitted_base = [ans_dict["bA"], ans_dict["bB"], 
                                ans_dict["bC"], ans_dict["bD"]]
                
                for phase in range(4):
                    if self._cyclic_shift(submitted_base, phase) == self.base_dist:
                        return self._check_consistency(submitted_base, phase)
                
                return False
                
            except:
                return False
        
        return False

    def _check_consistency(self, submitted_base, inferred_phase):
        for step, query_type, query_content, response in self.history:
            total_shifts = inferred_phase + self.phase + (step - 1)
            dist = self._cyclic_shift(submitted_base, total_shifts)
            dist_dict = {"A": dist[0], "B": dist[1], "C": dist[2], "D": dist[3]}
            
            if query_type == "single":
                cat = query_content
                if dist_dict[cat] != response:
                    return False
                    
            elif query_type == "sum":
                cat1, cat2 = query_content
                if dist_dict[cat1] + dist_dict[cat2] != response:
                    return False
                    
            elif query_type == "greater":
                cat1, cat2 = query_content
                expected = dist_dict[cat1] > dist_dict[cat2]
                actual = (response == "Yes") if self.config.language == "en" else (response == "是")
                if expected != actual:
                    return False
                    
            elif query_type == "equal":
                cat1, cat2 = query_content
                expected = dist_dict[cat1] == dist_dict[cat2]
                actual = (response == "Yes") if self.config.language == "en" else (response == "是")
                if expected != actual:
                    return False
        
        return True

    def _cf_make_wrong(self, correct):
        try:
            val = int(correct)
            wrong_val = val + 1
            return str(wrong_val)
        except ValueError:
            pass
        
        yes_res = "Yes" if self.config.language == "en" else "是"
        no_res = "No" if self.config.language == "en" else "否"
        if correct == yes_res:
            return no_res
        elif correct == no_res:
            return yes_res
        
        return correct + " [WRONG]"

    def _cf_core_produce(self, parsed_info):
        yes_res = "Yes" if self.config.language == "en" else "是"
        no_res = "No" if self.config.language == "en" else "否"
        error_quota = "Error: Quota exceeded for this step." if self.config.language == "en" else "错误：超出本步查询配额。"
        error_format = "Error: Invalid format." if self.config.language == "en" else "错误：格式无效。"
        
        current_dist = self._get_distribution(self.current_step)
        dist_dict = {"A": current_dist[0], "B": current_dist[1], 
                    "C": current_dist[2], "D": current_dist[3]}
        
        if "next_step" in parsed_info:
            if self.current_step >= 10:
                msg = "已达到第 10 步，无法继续推进。" if self.config.language == "zh" else "Already at step 10, cannot advance further."
                return msg
            self.current_step += 1
            self._reset_step_quota()
            msg = f"已进入第 {self.current_step} 步。" if self.config.language == "zh" else f"Now at step {self.current_step}."
            return msg
        
        if "request_predict" in parsed_info:
            visited_steps = set(record[0] for record in self.history)
            for t in range(1, 11):
                if t not in visited_steps:
                    self.predict_step = t
                    self.in_predict_mode = True
                    msg = f"请预测第 {t} 步的分布。" if self.config.language == "zh" else f"Please predict the distribution at step {t}."
                    return msg
            self.predict_step = 5
            self.in_predict_mode = True
            msg = f"请预测第 {self.predict_step} 步的分布。" if self.config.language == "zh" else f"Please predict the distribution at step {self.predict_step}."
            return msg
        
        if "query_single" in parsed_info:
            if self.query_count_quant >= 2:
                self.violation_count += 1
                return error_quota
            
            cat = parsed_info["query_single"].strip().upper()
            if cat not in ["A", "B", "C", "D"]:
                return error_format
            
            self.query_count_quant += 1
            result = dist_dict[cat]
            self.history.append((self.current_step, "single", cat, result))
            return str(result)
        
        if "query_sum" in parsed_info:
            if self.query_count_quant >= 2:
                self.violation_count += 1
                return error_quota
            
            try:
                cats = [x.strip().upper() for x in parsed_info["query_sum"].split(",")]
                if len(cats) != 2 or not all(c in ["A", "B", "C", "D"] for c in cats):
                    return error_format
                if cats[0] == cats[1]:
                    return error_format
                
                self.query_count_quant += 1
                result = dist_dict[cats[0]] + dist_dict[cats[1]]
                self.history.append((self.current_step, "sum", tuple(cats), result))
                return str(result)
            except:
                return error_format
        
        if "query_greater" in parsed_info:
            if self.query_count_comp >= 1:
                self.violation_count += 1
                return error_quota
            
            try:
                cats = [x.strip().upper() for x in parsed_info["query_greater"].split(",")]
                if len(cats) != 2 or not all(c in ["A", "B", "C", "D"] for c in cats):
                    return error_format
                
                self.query_count_comp += 1
                result = yes_res if dist_dict[cats[0]] > dist_dict[cats[1]] else no_res
                self.history.append((self.current_step, "greater", tuple(cats), result))
                return result
            except:
                return error_format
        
        if "query_equal" in parsed_info:
            if self.query_count_comp >= 1:
                self.violation_count += 1
                return error_quota
            
            try:
                cats = [x.strip().upper() for x in parsed_info["query_equal"].split(",")]
                if len(cats) != 2 or not all(c in ["A", "B", "C", "D"] for c in cats):
                    return error_format
                
                self.query_count_comp += 1
                result = yes_res if dist_dict[cats[0]] == dist_dict[cats[1]] else no_res
                self.history.append((self.current_step, "equal", tuple(cats), result))
                return result
            except:
                return error_format
        
        return error_format

    def step(self, response: str) -> "GameState":
        if self.violation_count >= 2:
            self.state.set_state("failed", "cumulative violations >= 2")
            msg = "累计违例达到 2 次，游戏失败。" if self.config.language == "zh" else "Cumulative violations reached 2, game failed."
            self.state.add_message("user", msg)
            return self.state
        
        if self.failure_count >= 3:
            self.state.set_state("failed", "cumulative termination failures >= 3")
            msg = "累计终局失败达到 3 次，游戏失败。" if self.config.language == "zh" else "Cumulative termination failures reached 3, game failed."
            self.state.add_message("user", msg)
            return self.state
        
        if self.current_step > 10:
            self.state.set_state("failed", "exceeded maximum steps")
            msg = "已超过第 10 步，游戏失败。" if self.config.language == "zh" else "Exceeded step 10, game failed."
            self.state.add_message("user", msg)
            return self.state

        try:
            parsed_info = self.parse(response)
            
            if "answer_predict" in parsed_info or "answer_base" in parsed_info:
                is_success = self.evaluate(parsed_info)
                if is_success:
                    res = "答案正确，游戏成功！" if self.config.language == "zh" else "Correct answer, game succeeded!"
                    self.state.set_state("success", "success")
                    self.state.add_message("user", res)
                else:
                    self.failure_count += 1
                    if self.failure_count >= 3:
                        res = "答案错误，累计失败 3 次，游戏结束。" if self.config.language == "zh" else "Incorrect answer, 3 cumulative failures, game over."
                        self.state.set_state("failed", "cumulative termination failures >= 3")
                    else:
                        res = f"答案错误，当前失败 {self.failure_count} 次。" if self.config.language == "zh" else f"Incorrect answer, {self.failure_count} failure(s) so far."
                    self.state.add_message("user", res)
                    self.in_predict_mode = False
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
                if self.violation_count >= 2:
                    fail_msg = "累计违例达到 2 次，游戏失败。" if self.config.language == "zh" else "Cumulative violations reached 2, game failed."
                    self.state.set_state("failed", "cumulative violations >= 2")
                    self.state.add_message("user", fail_msg)
                
        except Exception as e:
            self.state.set_state("failed", f"parse error: {str(e)}")
            error_msg = f"解析错误：{str(e)}" if self.config.language == "zh" else f"Parse error: {str(e)}"
            self.state.add_message("user", error_msg)
        
        return self.state