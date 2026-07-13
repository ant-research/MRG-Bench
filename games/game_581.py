# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 集合：存在一个由N个物体组成的集合，注意他们不存在位置、前后和大小关系。
# 知识点:   替换影响：将某元素替换为另一元素后，满足条件的元素数量如何变化
# ============================================================

from .base import Game
import re


class HiddenFunctionGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "集合"

    game_rule_zh = """\
我们现在来玩一个"隐藏函数推理"游戏，规则如下：

游戏设定了一个大小为 12 的集合，元素分属四个类型：A、B、C、D。集合中各类型的元素数量分别为 a、b、c、d，满足 a+b+c+d=12。

系统使用一个隐藏函数 f，根据当前的四个类型计数 (a, b, c, d) 计算出一个整数输出值 y（范围 0 到 12）。

你的目标是：
1. 通过交互操作推断出隐藏函数 f 的类型
2. 将输出值调整到该函数类型对应的目标值

初始状态：
- 初始四类型计数为：A={a0}, B={b0}, C={c0}, D={d0}
- 初始输出值为：y0={y0}

你可以进行以下操作：

1. 替换操作：将一个单位的类型 X 改为类型 Y（X 和 Y 必须不同，且 X 的当前计数必须大于 0）
   格式：<replace>X,Y</replace>
   示例：<replace>A,B</replace> 表示将一个 A 类型元素改为 B 类型

2. 计数查询：查询当前四类型的计数
   格式：<query_count></query_count>

3. 输出值查询：查询当前输出值 y
   格式：<query_output></query_output>

4. 宣告答案：声明你判断的函数模式及对应目标值（只能宣告一次）
   格式：<declare>模式=X</declare>
   其中 X 可以是：M、P、T4、U 之一

5. 请求验证：在宣告后，当你认为已达到目标值时请求验证
   格式：<answer>verify</answer>

注意事项：
- 每次替换操作后，系统会自动返回更新后的四类型计数和当前输出值
- 你需要在尽可能少的替换次数内完成推理和调整
- 必须先进行宣告，才能进行最终验证
- 验证时，系统会检查你宣告的模式是否正确，以及当前输出值是否等于该模式的目标值
"""

    game_rule_en = """\
Let's play a "Hidden Function Inference" game. Here are the rules:

The game involves a set of size 12, with elements belonging to four types: A, B, C, D. The counts of each type are a, b, c, d respectively, satisfying a+b+c+d=12.

The system uses a hidden function f to compute an integer output value y (range 0 to 12) based on the current four type counts (a, b, c, d).

Your goals are:
1. Infer the type of the hidden function f through interactive operations
2. Adjust the output value to the target value corresponding to that function type

Initial state:
- Initial four type counts: A={a0}, B={b0}, C={c0}, D={d0}
- Initial output value: y0={y0}

You can perform the following operations:

1. Replace operation: Change one unit of type X to type Y (X and Y must be different, and current count of X must be greater than 0)
   Format: <replace>X,Y</replace>
   Example: <replace>A,B</replace> means change one A type element to B type

2. Count query: Query the current counts of the four types
   Format: <query_count></query_count>

3. Output query: Query the current output value y
   Format: <query_output></query_output>

4. Declare answer: Declare the function mode you identified and its corresponding target value (can only declare once)
   Format: <declare>mode=X</declare>
   where X can be: M, P, T4, or U

5. Request verification: After declaration, request verification when you believe the target value is reached
   Format: <answer>verify</answer>

Notes:
- After each replace operation, the system automatically returns the updated four type counts and current output value
- You need to complete the inference and adjustment with as few replacements as possible
- You must declare before final verification
- During verification, the system checks if your declared mode is correct and if the current output value equals the target value for that mode
"""

    contextualized_rule_zh_1 = """\
欢迎接入"城市交通协同管控系统"。

系统当前调度着 12 个智能交通巡逻车队，分布在四个区域：A（主干道）、B（次干道）、C（支路）、D（商业区）。各区域的车队数量分别为 a、b、c、d，满足 a+b+c+d=12。

调度中枢使用一个隐藏算法 f，根据当前的区域车队分布 (a, b, c, d) 实时计算出一个交通流优化指数 y（整数，范围 0 到 12）。

你的目标是：
1. 通过交互操作推断出调度中枢隐藏算法 f 的运算模式
2. 将交通流优化指数调整到该算法模式对应的最佳目标值

初始状态：
- 各区域车队分布为：A={a0}, B={b0}, C={c0}, D={d0}
- 初始交通流优化指数：y0={y0}

你可以进行以下操作：

1. 跨区调度（替换操作）：将一个单位的车队从 X 区域调往 Y 区域（X 和 Y 必须不同，且 X 的当前计数必须大于 0）
   格式：<replace>X,Y</replace>
   示例：<replace>A,B</replace> 表示将一个车队从 A 区调往 B 区

2. 部署查询：查询当前四个区域的车队分布情况
   格式：<query_count></query_count>

3. 指数查询：查询当前的交通流优化指数 y
   格式：<query_output></query_output>

4. 模式判定宣告：声明你判定的核心算法模式及对应目标值（只能宣告一次）
   格式：<declare>模式=X</declare>
   其中 X 可以是：M、P、T4、U 之一

5. 请求验收：在宣告后，当你认为已达到目标指数时请求验收
   格式：<answer>verify</answer>

注意事项：
- 每次调度操作后，系统会自动返回更新后的车队分布和当前优化指数
- 你需要在尽可能少的调度次数内完成推理和调整
- 必须先进行宣告，才能进行最终验收
- 验收时，系统会检查你宣告的模式是否正确，以及当前指数是否等于该模式的目标值
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Traffic Synergistic Control System".

The system currently dispatches a fleet of 12 smart traffic patrol units distributed across four zones: A (Arterial), B (Boulevard), C (Crossroad), D (Downtown). The counts of units in each zone are a, b, c, d respectively, satisfying a+b+c+d=12.

The central dispatch uses a hidden algorithm f to compute a traffic flow optimization index y (integer, range 0 to 12) based on the current distribution (a, b, c, d).

Your goals are:
1. Infer the calculation mode of the hidden algorithm f through interactive operations
2. Adjust the traffic flow optimization index to the optimal target value corresponding to that mode

Initial state:
- Initial unit distribution: A={a0}, B={b0}, C={c0}, D={d0}
- Initial optimization index: y0={y0}

You can perform the following operations:

1. Dispatch (Replace) operation: Reassign one unit from zone X to zone Y (X and Y must be different, and the current count of X must be greater than 0)
   Format: <replace>X,Y</replace>
   Example: <replace>A,B</replace> means reassigning one unit from zone A to zone B

2. Deployment query: Query the current distribution of units in the four zones
   Format: <query_count></query_count>

3. Index query: Query the current optimization index y
   Format: <query_output></query_output>

4. Declare mode: Declare the algorithm mode you identified and its corresponding target value (can only declare once)
   Format: <declare>mode=X</declare>
   where X can be: M, P, T4, or U

5. Request verification: After declaration, request verification when you believe the target index is reached
   Format: <answer>verify</answer>

Notes:
- After each dispatch operation, the system automatically returns the updated distribution and current index
- You need to complete the inference and adjustment with as few dispatch operations as possible
- You must declare before final verification
- During verification, the system checks if your declared mode is correct and if the current index equals the target value for that mode
"""

    contextualized_rule_zh_2 = """\
欢迎登录"全院医疗资源动态调配平台"。

医院目前拥有 12 支机动专家医疗队，分配在四个核心科室：A（急诊）、B（血库）、C（门诊）、D（药房）。各科室的医疗队数量分别为 a、b、c、d，满足 a+b+c+d=12。

平台底层的评估模型 f 根据当前的专家队分布 (a, b, c, d) 动态计算出一个医疗资源能效评分 y（整数，范围 0 到 12）。

你的目标是：
1. 通过试探性调配推断出隐藏评估模型 f 的打分模式
2. 将能效评分调整到该模式对应的达标目标值

初始状态：
- 各科室医疗队分布为：A={a0}, B={b0}, C={c0}, D={d0}
- 初始能效评分：y0={y0}

你可以进行以下操作：

1. 资源调配（替换操作）：将一支医疗队从 X 科室调往 Y 科室（X 和 Y 必须不同，且 X 的当前计数必须大于 0）
   格式：<replace>X,Y</replace>
   示例：<replace>A,B</replace> 表示将一支医疗队从 A 科室调往 B 科室

2. 分布查询：查询当前四个科室的医疗队分布
   格式：<query_count></query_count>

3. 评分查询：查询当前的能效评分 y
   格式：<query_output></query_output>

4. 模式判定宣告：声明你判定的打分模式及对应目标值（只能宣告一次）
   格式：<declare>模式=X</declare>
   其中 X 可以是：M、P、T4、U 之一

5. 请求验收：在宣告后，当你认为已达到目标评分时请求验收
   格式：<answer>verify</answer>

注意事项：
- 每次调配操作后，系统会自动返回更新后的团队分布和当前评分
- 你需要在尽可能少的调配次数内完成推理和调整
- 必须先进行宣告，才能进行最终验收
- 验收时，系统会检查你宣告的模式是否正确，以及当前评分是否等于该模式的目标值
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Hospital-wide Dynamic Medical Resource Allocation Platform".

The hospital currently has 12 mobile expert medical teams distributed across four core departments: A (A&E), B (Blood Bank), C (Clinic), D (Dispensary). The number of teams in each department are a, b, c, d respectively, satisfying a+b+c+d=12.

The platform's underlying evaluation model f dynamically computes a resource efficiency score y (integer, range 0 to 12) based on the current team distribution (a, b, c, d).

Your goals are:
1. Infer the scoring mode of the hidden evaluation model f through trial allocations
2. Adjust the efficiency score to the target value corresponding to that mode

Initial state:
- Initial team distribution: A={a0}, B={b0}, C={c0}, D={d0}
- Initial efficiency score: y0={y0}

You can perform the following operations:

1. Reallocate (Replace) operation: Transfer one medical team from department X to department Y (X and Y must be different, and the current count of X must be greater than 0)
   Format: <replace>X,Y</replace>
   Example: <replace>A,B</replace> means transferring one team from A&E to Blood Bank

2. Distribution query: Query the current distribution of medical teams
   Format: <query_count></query_count>

3. Score query: Query the current efficiency score y
   Format: <query_output></query_output>

4. Declare mode: Declare the scoring mode you identified and its target value (can only declare once)
   Format: <declare>mode=X</declare>
   where X can be: M, P, T4, or U

5. Request verification: After declaration, request verification when you believe the target score is reached
   Format: <answer>verify</answer>

Notes:
- After each reallocation operation, the system automatically returns the updated distribution and current score
- You need to complete the inference and adjustment with as few reallocations as possible
- You must declare before final verification
- During verification, the system checks if your declared mode is correct and if the current score equals the target value for that mode
"""

    contextualized_rule_zh_3 = """\
欢迎进入"学区教育师资均衡发展系统"。

学区委员会拨款设置了 12 个特级教师指导组，支援四个重点学科：A（文科）、B（理科）、C（工科）、D（艺术）。各学科的指导组数量分别为 a、b、c、d，满足 a+b+c+d=12。

教育局的评估函数 f 会根据当前的师资分布 (a, b, c, d) 测算出一个教育均衡发展指数 y（整数，范围 0 到 12）。

你的目标是：
1. 通过调动指导组来推断出评估函数 f 所采用的测算模式
2. 将教育均衡发展指数调整到该测算模式下规定的目标值

初始状态：
- 各学科师资分布为：A={a0}, B={b0}, C={c0}, D={d0}
- 初始均衡发展指数：y0={y0}

你可以进行以下操作：

1. 师资调动（替换操作）：将一个指导组从 X 学科调往 Y 学科（X 和 Y 必须不同，且 X 的当前计数必须大于 0）
   格式：<replace>X,Y</replace>
   示例：<replace>A,B</replace> 表示将一个指导组从文科调往理科

2. 师资查询：查询当前四个学科的指导组分布
   格式：<query_count></query_count>

3. 指数查询：查询当前的均衡发展指数 y
   格式：<query_output></query_output>

4. 模式判定宣告：声明你判定的测算模式及对应目标值（只能宣告一次）
   格式：<declare>模式=X</declare>
   其中 X 可以是：M、P、T4、U 之一

5. 请求验收：在宣告后，当你认为已达到目标指数时请求验收
   格式：<answer>verify</answer>

注意事项：
- 每次调动操作后，系统会自动返回更新后的师资分布和当前指数
- 你需要在尽可能少的调动次数内完成推理和调整
- 必须先进行宣告，才能进行最终验收
- 验收时，系统会检查你宣告的模式是否正确，以及当前指数是否等于该模式的目标值
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "School District Faculty Balanced Development System".

The district committee has funded 12 master teacher mentoring groups to support four key disciplines: A (Arts), B (Biology/Science), C (Computer/Engineering), D (Design/Arts). The counts of mentoring groups in each discipline are a, b, c, d respectively, satisfying a+b+c+d=12.

The education bureau's evaluation function f calculates an education balanced development index y (integer, range 0 to 12) based on the current faculty distribution (a, b, c, d).

Your goals are:
1. Infer the calculation mode of the evaluation function f by transferring mentoring groups
2. Adjust the balanced development index to the target value required by that mode

Initial state:
- Initial faculty distribution: A={a0}, B={b0}, C={c0}, D={d0}
- Initial development index: y0={y0}

You can perform the following operations:

1. Transfer (Replace) operation: Move one mentoring group from discipline X to discipline Y (X and Y must be different, and current count of X must be greater than 0)
   Format: <replace>X,Y</replace>
   Example: <replace>A,B</replace> means transferring a group from Arts to Science

2. Faculty query: Query the current distribution of mentoring groups
   Format: <query_count></query_count>

3. Index query: Query the current development index y
   Format: <query_output></query_output>

4. Declare mode: Declare the calculation mode you identified and its target value (can only declare once)
   Format: <declare>mode=X</declare>
   where X can be: M, P, T4, or U

5. Request verification: After declaration, request verification when you believe the target index is reached
   Format: <answer>verify</answer>

Notes:
- After each transfer operation, the system automatically returns the updated distribution and current index
- You need to complete the inference and adjustment with as few transfers as possible
- You must declare before final verification
- During verification, the system checks if your declared mode is correct and if the current index equals the target value for that mode
"""

    contextualized_rule_zh_4 = """\
欢迎操作"柔性制造工业物联网调度台"。

工厂车间内共有 12 台全自动 AGV 搬运机器人，正在服务四个产线：A（装配线）、B（烘焙线）、C（涂装线）、D（物流线）。各产线分配的 AGV 数量分别为 a、b、c、d，满足 a+b+c+d=12。

总控中枢运行着一个隐藏逻辑 f，根据当前的机器人分布 (a, b, c, d) 运算出车间系统协同评级 y（整数，范围 0 到 12）。

你的目标是：
1. 通过重新配置 AGV 路线推断出总控中枢隐藏逻辑 f 的协同模式
2. 将车间系统协同评级提升至该模式要求的满分目标值

初始状态：
- 各产线 AGV 分布为：A={a0}, B={b0}, C={c0}, D={d0}
- 初始协同评级：y0={y0}

你可以进行以下操作：

1. 路线重配（替换操作）：将一台 AGV 从 X 产线调入 Y 产线（X 和 Y 必须不同，且 X 的当前计数必须大于 0）
   格式：<replace>X,Y</replace>
   示例：<replace>A,B</replace> 表示将一台 AGV 从装配线调往烘焙线

2. 阵列查询：查询当前四个产线的 AGV 分布
   格式：<query_count></query_count>

3. 评级查询：查询当前的系统协同评级 y
   格式：<query_output></query_output>

4. 模式判定宣告：声明你判定的协同模式及对应目标值（只能宣告一次）
   格式：<declare>模式=X</declare>
   其中 X 可以是：M、P、T4、U 之一

5. 请求验收：在宣告后，当你认为已达到目标评级时请求验收
   格式：<answer>verify</answer>

注意事项：
- 每次重配操作后，系统会自动返回更新后的 AGV 分布和当前评级
- 你需要在尽可能少的重配次数内完成推理和调整
- 必须先进行宣告，才能进行最终验收
- 验收时，系统会检查你宣告的模式是否正确，以及当前评级是否等于该模式的目标值
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Flexible Manufacturing Industrial IoT Dispatch Console".

The factory floor has a total of 12 fully automated AGV transport robots servicing four production lines: A (Assembly), B (Baking), C (Coating), D (Delivery). The counts of AGVs assigned to each line are a, b, c, d respectively, satisfying a+b+c+d=12.

The central control hub runs a hidden logic f to calculate a system synergy rating y (integer, range 0 to 12) based on the current robot distribution (a, b, c, d).

Your goals are:
1. Infer the synergy mode of the hidden logic f by reconfiguring AGV routes
2. Upgrade the system synergy rating to the perfect target value required by that mode

Initial state:
- Initial AGV distribution: A={a0}, B={b0}, C={c0}, D={d0}
- Initial synergy rating: y0={y0}

You can perform the following operations:

1. Reconfigure (Replace) operation: Reassign one AGV from line X to line Y (X and Y must be different, and current count of X must be greater than 0)
   Format: <replace>X,Y</replace>
   Example: <replace>A,B</replace> means reassigning one AGV from Assembly to Baking

2. Array query: Query the current distribution of AGVs
   Format: <query_count></query_count>

3. Rating query: Query the current synergy rating y
   Format: <query_output></query_output>

4. Declare mode: Declare the synergy mode you identified and its target value (can only declare once)
   Format: <declare>mode=X</declare>
   where X can be: M, P, T4, or U

5. Request verification: After declaration, request verification when you believe the target rating is reached
   Format: <answer>verify</answer>

Notes:
- After each reconfiguration operation, the system automatically returns the updated distribution and current rating
- You need to complete the inference and adjustment with as few reconfigurations as possible
- You must declare before final verification
- During verification, the system checks if your declared mode is correct and if the current rating equals the target value for that mode
"""

    contextualized_rule_zh_5 = """\
欢迎使用"大型律所案件效能管理系统"。

律所目前指派了 12 名高级调查专员，负责四个主要案件组：A（行政诉讼）、B（商事仲裁）、C（刑事辩护）、D（婚姻家庭）。各组专员人数分别为 a、b、c、d，满足 a+b+c+d=12。

所内效能核算函数 f 会根据当前的人员分配 (a, b, c, d) 得出一个案件结案效能指标 y（整数，范围 0 到 12）。

你的目标是：
1. 通过人员调岗操作推断出效能核算函数 f 的计算模式
2. 将案件结案效能指标调整到该模式所对应的最高目标值

初始状态：
- 各案组专员分布为：A={a0}, B={b0}, C={c0}, D={d0}
- 初始效能指标：y0={y0}

你可以进行以下操作：

1. 人员调岗（替换操作）：将一名专员从 X 组调入 Y 组（X 和 Y 必须不同，且 X 的当前人数必须大于 0）
   格式：<replace>X,Y</replace>
   示例：<replace>A,B</replace> 表示将一名专员从行政组调往商事组

2. 人事查询：查询当前四个案件组的专员分布
   格式：<query_count></query_count>

3. 效能查询：查询当前的案件结案效能指标 y
   格式：<query_output></query_output>

4. 模式判定宣告：声明你判定的计算模式及对应目标值（只能宣告一次）
   格式：<declare>模式=X</declare>
   其中 X 可以是：M、P、T4、U 之一

5. 请求验收：在宣告后，当你认为已达到目标效能时请求验收
   格式：<answer>verify</answer>

注意事项：
- 每次调岗操作后，系统会自动返回更新后的人员分布和当前效能指标
- 你需要在尽可能少的调岗次数内完成推理和调整
- 必须先进行宣告，才能进行最终验收
- 验收时，系统会检查你宣告的模式是否正确，以及当前效能指标是否等于该模式的目标值
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Large Law Firm Case Processing Efficiency Management System".

The firm has currently assigned 12 senior investigators across four major case groups: A (Administrative), B (Business), C (Criminal), D (Domestic). The counts of investigators in each group are a, b, c, d respectively, satisfying a+b+c+d=12.

The firm's efficiency accounting function f calculates a case processing efficiency metric y (integer, range 0 to 12) based on the current personnel assignment (a, b, c, d).

Your goals are:
1. Infer the calculation mode of the efficiency function f through personnel reassignment
2. Adjust the case processing efficiency metric to the target value corresponding to that mode

Initial state:
- Initial investigator distribution: A={a0}, B={b0}, C={c0}, D={d0}
- Initial efficiency metric: y0={y0}

You can perform the following operations:

1. Reassign (Replace) operation: Transfer one investigator from group X to group Y (X and Y must be different, and the current count of X must be greater than 0)
   Format: <replace>X,Y</replace>
   Example: <replace>A,B</replace> means transferring an investigator from Administrative to Business

2. Personnel query: Query the current distribution of investigators
   Format: <query_count></query_count>

3. Metric query: Query the current efficiency metric y
   Format: <query_output></query_output>

4. Declare mode: Declare the calculation mode you identified and its target value (can only declare once)
   Format: <declare>mode=X</declare>
   where X can be: M, P, T4, or U

5. Request verification: After declaration, request verification when you believe the target metric is reached
   Format: <answer>verify</answer>

Notes:
- After each reassignment operation, the system automatically returns the updated distribution and current metric
- You need to complete the inference and adjustment with as few reassignments as possible
- You must declare before final verification
- During verification, the system checks if your declared mode is correct and if the current metric equals the target value for that mode
"""

    tags = ["answer", "replace", "query_count", "query_output", "declare"]

    # 四种模式的定义和目标值
    MODE_DEFINITIONS = {
        "M": {
            "target": 6,
            "compute": lambda counts: max(counts.values()) if sum(1 for v in counts.values() if v == max(counts.values())) == 1 else 0,
            "desc_zh": "模式 M：若存在唯一计数严格最大的类型，输出为该类型的计数；否则输出 0",
            "desc_en": "Mode M: If there exists a unique type with strictly maximum count, output is that count; otherwise 0"
        },
        "P": {
            "target": 8,
            "compute": lambda counts: sum(v for v in counts.values() if v % 2 == 0),
            "desc_zh": "模式 P：输出为所有计数为偶数的类型计数之和",
            "desc_en": "Mode P: Output is the sum of all even counts"
        },
        "T4": {
            "target": 9,
            "compute": lambda counts: sum(v for v in counts.values() if v >= 4),
            "desc_zh": "模式 T4：输出为所有计数大于等于 4 的类型计数之和",
            "desc_en": "Mode T4: Output is the sum of all counts greater than or equal to 4"
        },
        "U": {
            "target": 3,
            "compute": lambda counts: sum(1 for v in counts.values() if v == 1),
            "desc_zh": "模式 U：输出为计数等于 1 的类型个数",
            "desc_en": "Mode U: Output is the number of types with count equal to 1"
        }
    }

    # 难度配置：简单、中等偏下、中等、中等偏上、困难
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {  # 简单：模式 M，初始状态不在目标值，但容易调整
                "a0": 4, "b0": 4, "c0": 2, "d0": 2,
                "mode": "M"
            },
            2: {  # 中等偏下：模式 P，需要一些调整
                "a0": 4, "b0": 4, "c0": 3, "d0": 1,
                "mode": "P"
            },
            3: {  # 中等：模式 T4，需要平衡多个类型
                "a0": 5, "b0": 4, "c0": 2, "d0": 1,
                "mode": "T4"
            },
            4: {  # 中等偏上：模式 U，需要创建多个计数为1的类型
                "a0": 9, "b0": 1, "c0": 1, "d0": 1,
                "mode": "U"
            },
            5: {  # 困难：模式 P，初始状态迷惑性强
                "a0": 3, "b0": 3, "c0": 3, "d0": 3,
                "mode": "P"
            }
        },
        "en": {
            1: {
                "a0": 4, "b0": 4, "c0": 2, "d0": 2,
                "mode": "M"
            },
            2: {
                "a0": 4, "b0": 4, "c0": 3, "d0": 1,
                "mode": "P"
            },
            3: {
                "a0": 5, "b0": 4, "c0": 2, "d0": 1,
                "mode": "T4"
            },
            4: {
                "a0": 9, "b0": 1, "c0": 1, "d0": 1,
                "mode": "U"
            },
            5: {
                "a0": 3, "b0": 3, "c0": 3, "d0": 3,
                "mode": "P"
            }
        }
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏状态"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保转为整数

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 初始化计数
        self.counts = {
            "A": cfg["a0"],
            "B": cfg["b0"],
            "C": cfg["c0"],
            "D": cfg["d0"]
        }
        
        # 隐藏的真实模式
        self.true_mode = cfg["mode"]
        self.compute_func = self.MODE_DEFINITIONS[self.true_mode]["compute"]
        self.target_value = self.MODE_DEFINITIONS[self.true_mode]["target"]
        
        # 计算初始输出值
        self.current_output = self.compute_func(self.counts)
        
        # 游戏状态跟踪
        self.replace_count = 0  # 替换次数
        self.declared_mode = None  # 玩家宣告的模式
        self.has_declared = False  # 是否已宣告
        
        # 设置游戏信息用于规则模板
        self._game_info = {
            "a0": cfg["a0"],
            "b0": cfg["b0"],
            "c0": cfg["c0"],
            "d0": cfg["d0"],
            "y0": self.current_output
        }

    def _compute_current_output(self):
        """根据当前计数计算输出值"""
        return self.compute_func(self.counts)

    def _format_counts(self):
        """格式化计数输出"""
        if self.config.language == "zh":
            return f"当前计数：A={self.counts['A']}, B={self.counts['B']}, C={self.counts['C']}, D={self.counts['D']}"
        else:
            return f"Current counts: A={self.counts['A']}, B={self.counts['B']}, C={self.counts['C']}, D={self.counts['D']}"

    def _format_output(self):
        """格式化输出值"""
        if self.config.language == "zh":
            return f"当前输出值：{self.current_output}"
        else:
            return f"Current output value: {self.current_output}"

    def evaluate(self, parsed_info):
        """评估最终答案"""
        # 如果同时包含 declare，先处理宣告
        if "declare" in parsed_info and not self.has_declared:
            raw = parsed_info["declare"].strip()
            match = re.search(r'(?:mode|模式)\s*=\s*(\w+)', raw, re.IGNORECASE)
            if match:
                mode = match.group(1).upper()
                if mode in self.MODE_DEFINITIONS:
                    self.declared_mode = mode
                    self.has_declared = True

        # 检查是否是验证请求
        if "answer" not in parsed_info:
            return False
            
        verify_content = parsed_info["answer"].strip().lower()
        if verify_content != "verify":
            return False
        
        # 检查是否已宣告
        if not self.has_declared:
            return False
        
        # 检查宣告的模式是否正确
        if self.declared_mode != self.true_mode:
            return False
        
        # 检查当前输出值是否等于目标值
        if self.current_output != self.target_value:
            return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        """处理各种查询和操作（原始业务逻辑）"""
        
        # 处理替换操作
        if "replace" in parsed_info:
            if self.replace_count >= 10:
                if self.config.language == "zh":
                    return "错误：替换次数已达到上限（10次）。"
                else:
                    return "Error: Maximum number of replacements (10) reached."
            
            raw = parsed_info["replace"].strip()
            parts = [x.strip().upper() for x in raw.split(",")]
            if len(parts) != 2:
                if self.config.language == "zh":
                    return "错误：替换格式无效。请使用格式 <replace>X,Y</replace>"
                else:
                    return "Error: Invalid replacement format. Please use format <replace>X,Y</replace>"
            
            from_type, to_type = parts
            
            # 验证类型有效性
            if from_type not in self.counts or to_type not in self.counts:
                if self.config.language == "zh":
                    return "错误：无效的类型。类型必须是 A、B、C 或 D。"
                else:
                    return "Error: Invalid type. Type must be A, B, C, or D."
            
            # 验证不能相同
            if from_type == to_type:
                if self.config.language == "zh":
                    return "错误：源类型和目标类型不能相同。"
                else:
                    return "Error: Source and target types cannot be the same."
            
            # 验证源类型计数大于0
            if self.counts[from_type] <= 0:
                if self.config.language == "zh":
                    return f"错误：类型 {from_type} 的当前计数为 0，无法替换。"
                else:
                    return f"Error: Current count of type {from_type} is 0, cannot replace."
            
            # 执行替换
            self.counts[from_type] -= 1
            self.counts[to_type] += 1
            self.replace_count += 1
            
            # 重新计算输出值
            self.current_output = self._compute_current_output()
            
            # 返回更新后的状态
            response = []
            if self.config.language == "zh":
                response.append(f"替换成功（第 {self.replace_count} 次替换）")
            else:
                response.append(f"Replacement successful (replacement #{self.replace_count})")
            response.append(self._format_counts())
            response.append(self._format_output())
            
            return "\n".join(response)
        
        # 处理计数查询
        elif "query_count" in parsed_info:
            return self._format_counts()
        
        # 处理输出值查询
        elif "query_output" in parsed_info:
            return self._format_output()
        
        # 处理宣告
        elif "declare" in parsed_info:
            if self.has_declared:
                if self.config.language == "zh":
                    return "错误：你已经进行过宣告，不能重复宣告。"
                else:
                    return "Error: You have already made a declaration. Cannot declare again."
            
            raw = parsed_info["declare"].strip()
            # 解析格式：mode=X 或 模式=X
            match = re.search(r'(?:mode|模式)\s*=\s*(\w+)', raw, re.IGNORECASE)
            if not match:
                if self.config.language == "zh":
                    return "错误：宣告格式无效。请使用格式 <declare>模式=X</declare>，其中 X 是 M、P、T4 或 U。"
                else:
                    return "Error: Invalid declaration format. Please use format <declare>mode=X</declare>, where X is M, P, T4, or U."
            
            mode = match.group(1).upper()
            
            if mode not in self.MODE_DEFINITIONS:
                if self.config.language == "zh":
                    return f"错误：无效的模式 '{mode}'。模式必须是 M、P、T4 或 U 之一。"
                else:
                    return f"Error: Invalid mode '{mode}'. Mode must be M, P, T4, or U."
            
            self.declared_mode = mode
            self.has_declared = True
            
            if self.config.language == "zh":
                return f"宣告已记录：模式 {mode}，目标输出值 {self.MODE_DEFINITIONS[mode]['target']}。你现在可以继续进行替换操作，直到达到目标值后请求验证。"
            else:
                return f"Declaration recorded: Mode {mode}, target output value {self.MODE_DEFINITIONS[mode]['target']}. You can now continue with replacement operations until reaching the target value, then request verification."
        
        else:
            if self.config.language == "zh":
                return "错误：未识别的操作。"
            else:
                return "Error: Unrecognized operation."

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有从当前初始状态出发的单步替换查询及其答案。
        注意：这些查询是互相独立的，每个都从初始状态开始。
        为了与 _run_redundancy 兼容，我们也添加 query_count 和 query_output 查询。
        """
        possible_queries = []
        types = ["A", "B", "C", "D"]
        
        # 备份原始状态
        original_counts = self.counts.copy()
        original_output = self.current_output
        original_replace_count = self.replace_count
        
        # 先添加 query_count 和 query_output 查询
        possible_queries.append({
            "query": "<query_count></query_count>",
            "answer": self._format_counts()
        })
        possible_queries.append({
            "query": "<query_output></query_output>",
            "answer": self._format_output()
        })

        # 如果替换次数已达上限，则没有合法的替换查询
        if self.replace_count >= 10:
            return possible_queries

        for from_type in types:
            for to_type in types:
                if from_type == to_type:
                    continue
                
                # 检查源类型计数是否大于 0，以确保是合法的替换
                if original_counts[from_type] > 0:
                    # 模拟执行替换
                    self.counts = original_counts.copy()
                    self.counts[from_type] -= 1
                    self.counts[to_type] += 1
                    self.replace_count = original_replace_count + 1
                    self.current_output = self._compute_current_output()
                    
                    response = []
                    if self.config.language == "zh":
                        response.append(f"替换成功（第 {self.replace_count} 次替换）")
                    else:
                        response.append(f"Replacement successful (replacement #{self.replace_count})")
                    response.append(self._format_counts())
                    response.append(self._format_output())
                    
                    possible_queries.append({
                        "query": f"<replace>{from_type},{to_type}</replace>",
                        "answer": "\n".join(response)
                    })
                        
        # 恢复状态
        self.counts = original_counts
        self.current_output = original_output
        self.replace_count = original_replace_count
                        
        return possible_queries

    def _cf_make_wrong(self, correct: str) -> str:
        """生成错误答案"""
        correct = str(correct)
        
        # 1. 纯数字：+1
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 2. 中文 是/否
        if "是" in correct or "否" in correct:
            new_val = correct.replace("是", "TEMP").replace("否", "是").replace("TEMP", "否")
            if new_val != correct:
                return new_val
        
        # 3. 英文 Yes/No (忽略大小写)
        if re.search(r'(?i)(yes|no)', correct):
            def repl(m):
                word = m.group(0)
                if word.lower() == 'yes':
                    if word.isupper(): return 'NO'
                    if word[0].isupper(): return 'No'
                    return 'no'
                else: # no
                    if word.isupper(): return 'YES'
                    if word[0].isupper(): return 'Yes'
                    return 'yes'
            
            new_val = re.sub(r'(?i)\b(yes|no)\b', repl, correct)
            if new_val != correct:
                return new_val
        
        # 4. 默认追加 _WRONG
        return correct + "_WRONG"