# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   前驱后继：某元素的紧邻前一个/后一个元素是什么
# ============================================================

import random
from .base import Game


class TotalOrderNeighborGame(Game):
    """
    全序邻居推理游戏
    
    游戏目标：通过有限次查询，确定目标元素在未知全序中的紧邻前驱和后继。
    """

    reasoning_type = "演绎推理"
    data_structure = "序列"

    game_rule_zh = """\
我们来玩一个"全序邻居推理"游戏，规则如下：

存在一个包含 9 个互不相同元素的集合 S = {{s1, s2, s3, s4, s5, s6, s7, s8, s9}}。这些元素按某个固定但未知的线性全序排列，用位置函数 pos 表示该全序，其中 pos(si) 属于 {{1, 2, 3, 4, 5, 6, 7, 8, 9}}。

已知目标元素为 {target_element}。你的任务是确定该目标元素的紧邻前驱和紧邻后继：
- 若目标元素位置大于 1，则前驱是位置恰好比它小 1 的元素；否则前驱为"无"。
- 若目标元素位置小于 9，则后继是位置恰好比它大 1 的元素；否则后继为"无"。

你可以通过以下三类是非问题进行查询（每次仅限一个问题）：

1. **顺序查询 BEFORE(x, y)**：询问元素 x 的位置是否小于元素 y 的位置。
   格式：<query_before>x,y</query_before>

2. **介于查询 BETWEEN(z; x, y)**：询问元素 z 的位置是否严格介于元素 x 和 y 之间（即 pos(x) 小于 pos(z) 小于 pos(y)，或 pos(y) 小于 pos(z) 小于 pos(x)）。
   格式：<query_between>z,x,y</query_between>

3. **相邻查询 ADJ(x, y)**：询问元素 x 和 y 的位置是否相邻（即位置差的绝对值等于 1）。
   格式：<query_adj>x,y</query_adj>

**查询限制**：
- 总查询次数不超过 12 次。
- 相邻查询 ADJ 最多只能使用 3 次。
- 超出限制的查询将被视为无效。

每次查询后，我会回答"是"或"否"。

当你收集到足够信息后，请提交最终答案。答案格式如下：

<answer>predecessor=元素或无, successor=元素或无</answer>

例如：<answer>predecessor=s3, successor=s7</answer> 或 <answer>predecessor=无, successor=s2</answer>

若答案错误、格式不符或超出查询限制，游戏失败。请尽可能少地使用查询次数来推断正确答案。
"""

    game_rule_en = """\
Let's play a "Total Order Neighbor Deduction" game. Here are the rules:

There exists a set S = {{s1, s2, s3, s4, s5, s6, s7, s8, s9}} containing 9 distinct elements. These elements are arranged in a fixed but unknown linear total order, represented by a position function pos, where pos(si) is in {{1, 2, 3, 4, 5, 6, 7, 8, 9}}.

The target element is {target_element}. Your task is to determine the immediate predecessor and immediate successor of the target element:
- If the target's position is greater than 1, the predecessor is the element at position exactly 1 less; otherwise, the predecessor is "none".
- If the target's position is less than 9, the successor is the element at position exactly 1 greater; otherwise, the successor is "none".

You may ask three types of yes/no questions (one question per turn):

1. **Order Query BEFORE(x, y)**: Ask if element x's position is less than element y's position.
   Format: <query_before>x,y</query_before>

2. **Between Query BETWEEN(z; x, y)**: Ask if element z's position is strictly between elements x and y (i.e., pos(x) < pos(z) < pos(y) or pos(y) < pos(z) < pos(x)).
   Format: <query_between>z,x,y</query_between>

3. **Adjacent Query ADJ(x, y)**: Ask if elements x and y are adjacent in position (i.e., the absolute difference of their positions equals 1).
   Format: <query_adj>x,y</query_adj>

**Query Limits**:
- Total number of queries cannot exceed 12.
- Adjacent queries ADJ can be used at most 3 times.
- Queries exceeding these limits will be considered invalid.

After each query, I will answer "Yes" or "No".

When you have gathered sufficient information, submit your final answer in the following format:

<answer>predecessor=element_or_none, successor=element_or_none</answer>

For example: <answer>predecessor=s3, successor=s7</answer> or <answer>predecessor=none, successor=s2</answer>

If the answer is incorrect, the format is invalid, or query limits are exceeded, the game fails. Try to infer the correct answer with as few queries as possible.
"""

    # ==========================================
    # 场景 1：交通
    # ==========================================
    contextualized_rule_zh_1 = """\
我们来执行一次"轨道交通线网排查"任务，规则如下：

存在一条单向轨道交通线，包含 9 个互不相同的站点集合 S = {{s1, s2, s3, s4, s5, s6, s7, s8, s9}}。这些站点按未知的固定线性顺序排列，用位置 pos 表示，其中 pos(si) 属于 {{1, 2, 3, 4, 5, 6, 7, 8, 9}}。

已知目标排查站点为 {target_element}。你的任务是确定该站点的上行紧邻站点（前驱）和下行紧邻站点（后继）：
- 若目标站点位置大于 1，则前驱是位置恰好比它小 1 的站点；否则前驱为"无"。
- 若目标站点位置小于 9，则后继是位置恰好比它大 1 的站点；否则后继为"无"。

你可以通过调度中心发起以下三类是非查询（每次仅限一个问题）：

1. **先后查询 BEFORE(x, y)**：询问站点 x 是否在站点 y 之前到达。
   格式：<query_before>x,y</query_before>

2. **区间查询 BETWEEN(z; x, y)**：询问站点 z 是否严格位于站点 x 和 y 之间。
   格式：<query_between>z,x,y</query_between>

3. **相邻查询 ADJ(x, y)**：询问站点 x 和 y 是否是直接相邻的站点。
   格式：<query_adj>x,y</query_adj>

**查询限制**：
- 总查询次数不超过 12 次。
- 相邻查询 ADJ 最多只能使用 3 次。
- 超出限制的查询将被系统拦截并视为无效。

每次查询后，调度系统会回答"是"或"否"。

当你收集到足够信息后，请提交最终排查报告。答案格式如下：

<answer>predecessor=站点或无, successor=站点或无</answer>

例如：<answer>predecessor=s3, successor=s7</answer> 或 <answer>predecessor=无, successor=s2</answer>

若报告错误、格式不符或超出查询限制，排查任务失败。请尽可能高效地使用查询次数来推断正确结果。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's execute a "Rail Transit Network Inspection" task. Here are the rules:

There is a one-way rail transit line containing a set S = {{s1, s2, s3, s4, s5, s6, s7, s8, s9}} of 9 distinct stations. These stations are arranged in a fixed but unknown linear sequence, represented by a position function pos, where pos(si) is in {{1, 2, 3, 4, 5, 6, 7, 8, 9}}.

The target station under inspection is {target_element}. Your task is to determine the immediate upstream station (predecessor) and immediate downstream station (successor) of this target:
- If the target's position is greater than 1, the predecessor is the station at position exactly 1 less; otherwise, the predecessor is "none".
- If the target's position is less than 9, the successor is the station at position exactly 1 greater; otherwise, the successor is "none".

You may query the dispatch center with three types of yes/no questions (one question per turn):

1. **Precedence Query BEFORE(x, y)**: Ask if station x is reached before station y.
   Format: <query_before>x,y</query_before>

2. **Interval Query BETWEEN(z; x, y)**: Ask if station z is strictly located between stations x and y.
   Format: <query_between>z,x,y</query_between>

3. **Adjacency Query ADJ(x, y)**: Ask if stations x and y are directly adjacent on the line.
   Format: <query_adj>x,y</query_adj>

**Query Limits**:
- Total number of queries cannot exceed 12.
- Adjacency queries ADJ can be used at most 3 times.
- Queries exceeding these limits will be rejected as invalid.

After each query, the dispatch system will answer "Yes" or "No".

When you have gathered sufficient information, submit your final inspection report in the following format:

<answer>predecessor=station_or_none, successor=station_or_none</answer>

For example: <answer>predecessor=s3, successor=s7</answer> or <answer>predecessor=none, successor=s2</answer>

If the report is incorrect, the format is invalid, or query limits are exceeded, the inspection task fails. Please utilize your queries as efficiently as possible.
"""

    # ==========================================
    # 场景 2：医疗
    # ==========================================
    contextualized_rule_zh_2 = """\
我们来进行一项"临床诊疗路径推断"任务，规则如下：

存在一个包含 9 个互不相同的临床诊疗阶段的集合 S = {{s1, s2, s3, s4, s5, s6, s7, s8, s9}}。这些阶段按严格的时间先后顺序排列，用阶段次序 pos 表示，其中 pos(si) 属于 {{1, 2, 3, 4, 5, 6, 7, 8, 9}}。

已知当前关注的诊疗阶段为 {target_element}。你的任务是确定该阶段的紧邻前置阶段（前驱）和紧邻后续阶段（后继）：
- 若目标阶段次序大于 1，则前驱是次序恰好比它小 1 的阶段；否则前驱为"无"。
- 若目标阶段次序小于 9，则后继是次序恰好比它大 1 的阶段；否则后继为"无"。

你可以通过医疗信息系统进行以下三类是非查询（每次仅限一个问题）：

1. **时序查询 BEFORE(x, y)**：询问阶段 x 是否在阶段 y 之前发生。
   格式：<query_before>x,y</query_before>

2. **穿插查询 BETWEEN(z; x, y)**：询问阶段 z 是否严格发生在阶段 x 和 y 的执行期间。
   格式：<query_between>z,x,y</query_between>

3. **衔接查询 ADJ(x, y)**：询问阶段 x 和 y 是否是紧密相连的两个诊疗阶段。
   格式：<query_adj>x,y</query_adj>

**查询限制**：
- 总查询次数不超过 12 次。
- 衔接查询 ADJ 最多只能使用 3 次。
- 超出限制的查询将被系统拒绝。

每次查询后，系统会回答"是"或"否"。

当你收集到足够信息后，请提交最终推断报告。答案格式如下：

<answer>predecessor=阶段或无, successor=阶段或无</answer>

例如：<answer>predecessor=s3, successor=s7</answer> 或 <answer>predecessor=无, successor=s2</answer>

若报告错误、格式不符或超出查询限制，推断任务失败。请合理规划查询路径以完成推导。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's perform a "Clinical Pathway Deduction" task. Here are the rules:

There exists a set S = {{s1, s2, s3, s4, s5, s6, s7, s8, s9}} containing 9 distinct clinical diagnosis and treatment stages. These stages are arranged in a strict chronological order, represented by a sequence function pos, where pos(si) is in {{1, 2, 3, 4, 5, 6, 7, 8, 9}}.

The target stage of interest is {target_element}. Your task is to determine the immediate preceding stage (predecessor) and immediate succeeding stage (successor) of this target:
- If the target's sequence is greater than 1, the predecessor is the stage at sequence exactly 1 less; otherwise, the predecessor is "none".
- If the target's sequence is less than 9, the successor is the stage at sequence exactly 1 greater; otherwise, the successor is "none".

You can query the medical information system with three types of yes/no questions (one question per turn):

1. **Chronology Query BEFORE(x, y)**: Ask if stage x occurs before stage y.
   Format: <query_before>x,y</query_before>

2. **Intervention Query BETWEEN(z; x, y)**: Ask if stage z occurs strictly between stages x and y.
   Format: <query_between>z,x,y</query_between>

3. **Connection Query ADJ(x, y)**: Ask if stages x and y are consecutive clinical stages.
   Format: <query_adj>x,y</query_adj>

**Query Limits**:
- Total number of queries cannot exceed 12.
- Connection queries ADJ can be used at most 3 times.
- Queries exceeding these limits will be rejected.

After each query, the system will answer "Yes" or "No".

When you have gathered sufficient information, submit your final deduction report in the following format:

<answer>predecessor=stage_or_none, successor=stage_or_none</answer>

For example: <answer>predecessor=s3, successor=s7</answer> or <answer>predecessor=none, successor=s2</answer>

If the report is incorrect, the format is invalid, or query limits are exceeded, the deduction task fails. Please plan your query path logically.
"""

    # ==========================================
    # 场景 3：教育
    # ==========================================
    contextualized_rule_zh_3 = """\
我们来制定一份"进阶课程先修链路规划"，规则如下：

存在一个包含 9 个互不相同学习模块的集合 S = {{s1, s2, s3, s4, s5, s6, s7, s8, s9}}。这些模块按难度等级构成了一条严格的单向选修链路，用等级 pos 表示，其中 pos(si) 属于 {{1, 2, 3, 4, 5, 6, 7, 8, 9}}。

已知核心关注课程为 {target_element}。你的任务是确定该课程的直接先修课程（前驱）和直接后续课程（后继）：
- 若目标课程等级大于 1，则前驱是等级恰好比它小 1 的课程；否则前驱为"无"。
- 若目标课程等级小于 9，则后继是等级恰好比它大 1 的课程；否则后继为"无"。

你可以向教务系统发起以下三类是非查询（每次仅限一个问题）：

1. **难度查询 BEFORE(x, y)**：询问课程 x 的等级是否低于课程 y（需先于 y 学习）。
   格式：<query_before>x,y</query_before>

2. **介于查询 BETWEEN(z; x, y)**：询问课程 z 的等级是否严格介于课程 x 和 y 之间。
   格式：<query_between>z,x,y</query_between>

3. **相邻查询 ADJ(x, y)**：询问课程 x 和 y 是否为难度相邻的两个模块。
   格式：<query_adj>x,y</query_adj>

**查询限制**：
- 总查询次数不超过 12 次。
- 相邻查询 ADJ 最多只能使用 3 次。
- 超出限制的查询将被记为无效操作。

每次查询后，教务系统会返回"是"或"否"。

当你收集到足够信息后，请提交最终链路规划。答案格式如下：

<answer>predecessor=课程或无, successor=课程或无</answer>

例如：<answer>predecessor=s3, successor=s7</answer> 或 <answer>predecessor=无, successor=s2</answer>

若规划错误、格式不符或超出查询限制，任务失败。请以最少的查询次数还原出正确的选修关系。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's formulate an "Advanced Course Prerequisite Pathway", following these rules:

There is a set S = {{s1, s2, s3, s4, s5, s6, s7, s8, s9}} containing 9 distinct learning modules. These modules form a strict one-way elective pathway based on difficulty level, represented by a level function pos, where pos(si) is in {{1, 2, 3, 4, 5, 6, 7, 8, 9}}.

The core course in focus is {target_element}. Your task is to determine the immediate prerequisite course (predecessor) and immediate subsequent course (successor) of this module:
- If the target's level is greater than 1, the predecessor is the course at level exactly 1 less; otherwise, the predecessor is "none".
- If the target's level is less than 9, the successor is the course at level exactly 1 greater; otherwise, the successor is "none".

You can query the academic system with three types of yes/no questions (one question per turn):

1. **Difficulty Query BEFORE(x, y)**: Ask if course x's level is lower than course y (must be studied before y).
   Format: <query_before>x,y</query_before>

2. **Intermediate Query BETWEEN(z; x, y)**: Ask if course z's level is strictly between courses x and y.
   Format: <query_between>z,x,y</query_between>

3. **Adjacency Query ADJ(x, y)**: Ask if courses x and y are two modules with adjacent difficulties.
   Format: <query_adj>x,y</query_adj>

**Query Limits**:
- Total number of queries cannot exceed 12.
- Adjacency queries ADJ can be used at most 3 times.
- Queries exceeding these limits will be recorded as invalid operations.

After each query, the academic system will return "Yes" or "No".

When you have gathered sufficient information, submit your final pathway plan in the following format:

<answer>predecessor=course_or_none, successor=course_or_none</answer>

For example: <answer>predecessor=s3, successor=s7</answer> or <answer>predecessor=none, successor=s2</answer>

If the plan is incorrect, the format is invalid, or query limits are exceeded, the task fails. Deduce the correct prerequisite relationships with minimal queries.
"""

    # ==========================================
    # 场景 4：制造业/工业
    # ==========================================
    contextualized_rule_zh_4 = """\
我们来执行一项"工业流水线工序测绘"任务，规则如下：

存在一条装配流水线，包含 9 道互不相同的加工工序集合 S = {{s1, s2, s3, s4, s5, s6, s7, s8, s9}}。这些工序按未知的严格加工顺序排列，用工位次序 pos 表示，其中 pos(si) 属于 {{1, 2, 3, 4, 5, 6, 7, 8, 9}}。

已知目标质检工序为 {target_element}。你的任务是查明该工序的上一道紧邻工序（前驱）和下一道紧邻工序（后继）：
- 若目标工序次序大于 1，则前驱是次序恰好比它小 1 的工序；否则前驱为"无"。
- 若目标工序次序小于 9，则后继是次序恰好比它大 1 的工序；否则后继为"无"。

你可以向制造执行系统（MES）发起以下三类是非查询（每次仅限一个问题）：

1. **排期查询 BEFORE(x, y)**：询问工序 x 是否在工序 y 之前执行。
   格式：<query_before>x,y</query_before>

2. **夹插查询 BETWEEN(z; x, y)**：询问工序 z 的执行时间是否严格介于工序 x 和 y 之间。
   格式：<query_between>z,x,y</query_between>

3. **上下游查询 ADJ(x, y)**：询问工序 x 和 y 是否是流水线上直接相连的两道工序。
   格式：<query_adj>x,y</query_adj>

**查询限制**：
- 总查询次数不超过 12 次。
- 上下游查询 ADJ 最多只能使用 3 次。
- 超出限制的查询指令将报错。

每次查询后，系统会反馈"是"或"否"。

当你收集到足够信息后，请提交最终工序测绘结果。答案格式如下：

<answer>predecessor=工序或无, successor=工序或无</answer>

例如：<answer>predecessor=s3, successor=s7</answer> 或 <answer>predecessor=无, successor=s2</answer>

若测绘错误、格式不符或超出查询限制，任务失败。请最优化你的查询策略。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's perform an "Industrial Assembly Line Process Mapping" task. Here are the rules:

There is an assembly line comprising a set S = {{s1, s2, s3, s4, s5, s6, s7, s8, s9}} of 9 distinct manufacturing processes. These processes are arranged in a strict but unknown processing sequence, represented by a workstation index pos, where pos(si) is in {{1, 2, 3, 4, 5, 6, 7, 8, 9}}.

The target quality inspection process is {target_element}. Your task is to identify the immediate preceding process (predecessor) and immediate succeeding process (successor) of this target:
- If the target's sequence is greater than 1, the predecessor is the process at index exactly 1 less; otherwise, the predecessor is "none".
- If the target's sequence is less than 9, the successor is the process at index exactly 1 greater; otherwise, the successor is "none".

You can query the Manufacturing Execution System (MES) with three types of yes/no questions (one question per turn):

1. **Schedule Query BEFORE(x, y)**: Ask if process x is executed before process y.
   Format: <query_before>x,y</query_before>

2. **Interleaved Query BETWEEN(z; x, y)**: Ask if process z's execution is strictly between processes x and y.
   Format: <query_between>z,x,y</query_between>

3. **Upstream/Downstream Query ADJ(x, y)**: Ask if processes x and y are directly connected processes on the assembly line.
   Format: <query_adj>x,y</query_adj>

**Query Limits**:
- Total number of queries cannot exceed 12.
- Upstream/Downstream queries ADJ can be used at most 3 times.
- Queries exceeding these limits will trigger an error.

After each query, the system will return "Yes" or "No".

When you have gathered sufficient information, submit your final mapping result in the following format:

<answer>predecessor=process_or_none, successor=process_or_none</answer>

For example: <answer>predecessor=s3, successor=s7</answer> or <answer>predecessor=none, successor=s2</answer>

If the mapping is incorrect, the format is invalid, or query limits are exceeded, the task fails. Please optimize your querying strategy.
"""

    # ==========================================
    # 场景 5：法律
    # ==========================================
    contextualized_rule_zh_5 = """\
我们来进行一项"司法诉讼法定程序梳理"任务，规则如下：

存在一个包含 9 个互不相同的法定环节的集合 S = {{s1, s2, s3, s4, s5, s6, s7, s8, s9}}。这些环节必须按法律规定的严格先后顺序进行，用程序次序 pos 表示，其中 pos(si) 属于 {{1, 2, 3, 4, 5, 6, 7, 8, 9}}。

已知当前审查的法定环节为 {target_element}。你的任务是确定该环节的上一法定环节（前置程序）和下一法定环节（后置程序）：
- 若目标环节次序大于 1，则前置程序是次序恰好比它小 1 的环节；否则前置程序为"无"。
- 若目标环节次序小于 9，则后置程序是次序恰好比它大 1 的环节；否则后置程序为"无"。

你可以查阅法典并进行以下三类是非查询（每次仅限一个问题）：

1. **顺位查询 BEFORE(x, y)**：询问环节 x 是否在环节 y 之前启动。
   格式：<query_before>x,y</query_before>

2. **穿插查询 BETWEEN(z; x, y)**：询问环节 z 是否必须在环节 x 和 y 的执行期间启动。
   格式：<query_between>z,x,y</query_between>

3. **衔接查询 ADJ(x, y)**：询问环节 x 和 y 是否是法定顺序上紧密衔接的两个程序。
   格式：<query_adj>x,y</query_adj>

**查询限制**：
- 总查询次数不超过 12 次。
- 衔接查询 ADJ 最多只能使用 3 次。
- 超出限制的查阅请求将被驳回。

每次查询后，法典检索引擎会回答"是"或"否"。

当你收集到足够信息后，请提交最终梳理结论。答案格式如下：

<answer>predecessor=环节或无, successor=环节或无</answer>

例如：<answer>predecessor=s3, successor=s7</answer> 或 <answer>predecessor=无, successor=s2</answer>

若结论错误、格式不符或超出查询限制，梳理任务失败。请严密论证并控制查询频次。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct a "Judicial Litigation Statutory Procedure Review" task. Here are the rules:

There exists a set S = {{s1, s2, s3, s4, s5, s6, s7, s8, s9}} containing 9 distinct statutory procedures. These procedures must be executed in a strict chronological order mandated by law, represented by a procedural sequence pos, where pos(si) is in {{1, 2, 3, 4, 5, 6, 7, 8, 9}}.

The target statutory procedure under review is {target_element}. Your task is to determine the previous statutory procedure (predecessor) and the next statutory procedure (successor) for this target:
- If the target's sequence is greater than 1, the predecessor is the procedure exactly 1 step prior; otherwise, the predecessor is "none".
- If the target's sequence is less than 9, the successor is the procedure exactly 1 step after; otherwise, the successor is "none".

You can consult the legal code to make three types of yes/no queries (one query per turn):

1. **Sequence Query BEFORE(x, y)**: Ask if procedure x is initiated before procedure y.
   Format: <query_before>x,y</query_before>

2. **Interim Query BETWEEN(z; x, y)**: Ask if procedure z is initiated strictly between procedures x and y.
   Format: <query_between>z,x,y</query_between>

3. **Connection Query ADJ(x, y)**: Ask if procedures x and y are strictly consecutive procedures in the statutory order.
   Format: <query_adj>x,y</query_adj>

**Query Limits**:
- Total number of queries cannot exceed 12.
- Connection queries ADJ can be used at most 3 times.
- Queries exceeding these limits will be dismissed.

After each query, the legal retrieval engine will answer "Yes" or "No".

When you have gathered sufficient information, submit your final review conclusion in the following format:

<answer>predecessor=procedure_or_none, successor=procedure_or_none</answer>

For example: <answer>predecessor=s3, successor=s7</answer> or <answer>predecessor=none, successor=s2</answer>

If the conclusion is incorrect, the format is invalid, or query limits are exceeded, the review task fails. Construct your arguments rigorously to minimize queries.
"""

    tags = ["answer", "query_before", "query_between", "query_adj"]

    # 难度配置：
    # 1 (简单)      - 目标在位置2，容易找到邻居
    # 2 (中等偏下)  - 目标在位置4，中间位置
    # 3 (中等偏上)  - 目标在位置7，需要更多推理
    # 4 (较难)      - 目标在位置1，边界情况（无前驱）
    # 5 (难)        - 目标在位置9，边界情况（无后继）

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "order": ["s5", "s2", "s8", "s1", "s6", "s4", "s9", "s3", "s7"],
                "target": "s2",  # 位置2
            },
            2: {
                "order": ["s3", "s7", "s1", "s5", "s9", "s4", "s2", "s8", "s6"],
                "target": "s5",  # 位置4
            },
            3: {
                "order": ["s4", "s9", "s2", "s6", "s1", "s8", "s3", "s5", "s7"],
                "target": "s3",  # 位置7
            },
            4: {
                "order": ["s7", "s3", "s5", "s9", "s2", "s1", "s4", "s8", "s6"],
                "target": "s7",  # 位置1，无前驱
            },
            5: {
                "order": ["s2", "s6", "s4", "s8", "s3", "s9", "s1", "s5", "s7"],
                "target": "s7",  # 位置9，无后继
            },
        },
        "en": {
            1: {
                "order": ["s5", "s2", "s8", "s1", "s6", "s4", "s9", "s3", "s7"],
                "target": "s2",  # Position 2
            },
            2: {
                "order": ["s3", "s7", "s1", "s5", "s9", "s4", "s2", "s8", "s6"],
                "target": "s5",  # Position 4
            },
            3: {
                "order": ["s4", "s9", "s2", "s6", "s1", "s8", "s3", "s5", "s7"],
                "target": "s3",  # Position 7
            },
            4: {
                "order": ["s7", "s3", "s5", "s9", "s2", "s1", "s4", "s8", "s6"],
                "target": "s7",  # Position 1, no predecessor
            },
            5: {
                "order": ["s2", "s6", "s4", "s8", "s3", "s9", "s1", "s5", "s7"],
                "target": "s7",  # Position 9, no successor
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：根据难度配置设置全序和目标元素"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 存储全序排列
        self.order = cfg["order"]  # 列表，索引0对应位置1
        
        # 目标元素
        self.target = cfg["target"]
        self._game_info["target_element"] = self.target
        
        # 构建位置映射
        self.pos_map = {elem: idx + 1 for idx, elem in enumerate(self.order)}
        
        # 计算正确答案
        target_pos = self.pos_map[self.target]
        
        if target_pos > 1:
            self.correct_predecessor = self.order[target_pos - 2]  # 位置target_pos-1对应索引target_pos-2
        else:
            self.correct_predecessor = "none" if lang == "en" else "无"
            
        if target_pos < 9:
            self.correct_successor = self.order[target_pos]  # 位置target_pos+1对应索引target_pos
        else:
            self.correct_successor = "none" if lang == "en" else "无"
        
        # 初始化查询计数器
        self.total_queries = 0
        self.adj_queries = 0
        self.max_total_queries = 12
        self.max_adj_queries = 3

    def _is_valid_element(self, elem):
        """检查元素是否在集合S中"""
        return elem in self.pos_map

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"].replace("，", ",")
        
        # 解析答案: predecessor=x, successor=y
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        
        for kv in kv_pairs:
            if "=" not in kv:
                continue
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "predecessor" not in ans_dict or "successor" not in ans_dict:
            return False
        
        # 标准化"无"的表示
        pred = ans_dict["predecessor"]
        succ = ans_dict["successor"]
        
        # 将各种"无"的表达统一
        none_values = {"none", "无", "None", "NONE"}
        if pred in none_values:
            pred = self.correct_predecessor if self.correct_predecessor in none_values else pred
        if succ in none_values:
            succ = self.correct_successor if self.correct_successor in none_values else succ
        
        # 比较答案
        pred_correct = (pred == self.correct_predecessor) or (
            pred in none_values and self.correct_predecessor in none_values
        )
        succ_correct = (succ == self.correct_successor) or (
            succ in none_values and self.correct_successor in none_values
        )
        
        return pred_correct and succ_correct

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑：根据查询类型生成响应"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_limit = "错误：已达到查询次数上限，无法继续查询。请直接提交你的最终答案。"
            error_adj_limit = "错误：相邻查询次数已达上限，该查询无效。请使用其他类型的查询或提交答案。"
            error_format = "错误：查询格式无效或元素不存在。"
        else:
            yes_res, no_res = "Yes", "No"
            error_limit = "Error: Query limit reached. No more queries allowed. Please submit your final answer."
            error_adj_limit = "Error: Adjacent query limit reached. This query is invalid. Please use other query types or submit your answer."
            error_format = "Error: Invalid query format or element does not exist."

        # 检查总查询次数 —— 不再直接设 failed，而是拒绝查询，提示提交答案
        if self.total_queries >= self.max_total_queries:
            return error_limit

        # 优先级：BEFORE > BETWEEN > ADJ
        if "query_before" in parsed_info:
            try:
                raw = parsed_info["query_before"]
                x, y = [elem.strip() for elem in raw.split(",")]
                
                if not self._is_valid_element(x) or not self._is_valid_element(y):
                    return error_format
                
                self.total_queries += 1
                result = self.pos_map[x] < self.pos_map[y]
                return yes_res if result else no_res
                
            except Exception:
                return error_format

        elif "query_between" in parsed_info:
            try:
                raw = parsed_info["query_between"]
                parts = [elem.strip() for elem in raw.split(",")]
                
                if len(parts) != 3:
                    return error_format
                
                z, x, y = parts
                
                if not all(self._is_valid_element(e) for e in [z, x, y]):
                    return error_format
                
                self.total_queries += 1
                pos_z, pos_x, pos_y = self.pos_map[z], self.pos_map[x], self.pos_map[y]
                
                result = (pos_x < pos_z < pos_y) or (pos_y < pos_z < pos_x)
                return yes_res if result else no_res
                
            except Exception:
                return error_format

        elif "query_adj" in parsed_info:
            # 检查 ADJ 查询次数限制 —— 不再设 failed，仅拒绝该查询
            if self.adj_queries >= self.max_adj_queries:
                return error_adj_limit
            
            try:
                raw = parsed_info["query_adj"]
                x, y = [elem.strip() for elem in raw.split(",")]
                
                if not self._is_valid_element(x) or not self._is_valid_element(y):
                    return error_format
                
                self.total_queries += 1
                self.adj_queries += 1
                
                result = abs(self.pos_map[x] - self.pos_map[y]) == 1
                return yes_res if result else no_res
                
            except Exception:
                return error_format

        else:
            return error_format

    def get_all_possible_queries(self) -> list[dict]:
        """
        返回一组精选的查询集合，覆盖关键推理路径，
        而非枚举所有可能的查询组合（避免查询数量爆炸）。
        
        策略：对于目标元素，返回与其他所有元素的 BEFORE 查询，
        以及目标与其他所有元素的 ADJ 查询。这足以确定目标位置及其邻居。
        """
        queries = []
        elements = sorted(list(self.pos_map.keys()))
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        # BEFORE 查询：目标与所有其他元素的比较（确定目标位置）
        for other in elements:
            if other == self.target:
                continue
            query_str = f"<query_before>{self.target},{other}</query_before>"
            result = self.pos_map[self.target] < self.pos_map[other]
            queries.append({
                "query": query_str,
                "answer": yes_res if result else no_res
            })

        # ADJ 查询：目标与其他元素的相邻关系
        for other in elements:
            if other == self.target:
                continue
            query_str = f"<query_adj>{self.target},{other}</query_adj>"
            result = abs(self.pos_map[self.target] - self.pos_map[other]) == 1
            queries.append({
                "query": query_str,
                "answer": yes_res if result else no_res
            })

        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        """根据正确答案生成一个明显不同的错误答案"""
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        else:
            # 忽略大小写进行判断，但替换时尽量保持原格式
            correct_lower = correct.lower()
            if "yes" in correct_lower:
                return correct.replace("Yes", "No").replace("yes", "no").replace("YES", "NO")
            elif "no" in correct_lower:
                return correct.replace("No", "Yes").replace("no", "yes").replace("NO", "YES")
        
        return correct + "_WRONG"