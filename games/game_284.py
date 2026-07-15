from .base import Game
import re
import itertools

class FieldMatchingGame(Game):

    game_rule_zh = """\
我们来玩一个"数据字段映射推理"游戏，规则如下：

游戏设定了一个包含15个对象的数据集，每个对象有三个离散字段F1、F2、F3，取值域分别为：
• F1 ∈ {{赤, 青, 白}}
• F2 ∈ {{条, 点, 环}}
• F3 ∈ {{甲, 乙, 丙}}

对象列表（编号: (F1, F2, F3)）：
1:(赤,条,甲)   2:(赤,点,甲)   3:(赤,环,乙)   4:(青,条,乙)   5:(青,点,丙)
6:(青,环,甲)   7:(白,条,丙)   8:(白,点,乙)   9:(白,环,丙)   10:(赤,条,乙)
11:(青,点,甲)  12:(白,点,甲)  13:(赤,环,丙)  14:(青,条,丙)  15:(白,条,乙)

现在有一个文本配方，包含三栏L1、L2、L3及其对应的值词：
• L1 = {recipe_L1}
• L2 = {recipe_L2}
• L3 = {recipe_L3}

存在六种可能的解释方案，用于将配方的字段名与值词映射到实际字段F1/F2/F3及其取值：

• S1（恒等映射）：
  - L1→F1，值映射：赤→赤，青→青，白→白
  - L2→F2，值映射：条→条，点→点，环→环
  - L3→F3，值映射：甲→甲，乙→乙，丙→丙

• S2（F1与F2互换）：
  - L1→F2，值映射：赤→条，青→点，白→环
  - L2→F1，值映射：条→赤，点→青，环→白
  - L3→F3，值映射：甲→甲，乙→乙，丙→丙

• S3（F1与F3互换）：
  - L1→F3，值映射：赤→甲，青→乙，白→丙
  - L2→F2，值映射：条→条，点→点，环→环
  - L3→F1，值映射：甲→赤，乙→青，丙→白

• S4（F2与F3互换）：
  - L1→F1，值映射：赤→赤，青→青，白→白
  - L2→F3，值映射：条→甲，点→乙，环→丙
  - L3→F2，值映射：甲→条，乙→点，丙→环

• S5（循环：L1→F2, L2→F3, L3→F1）：
  - L1→F2，值映射：赤→条，青→点，白→环
  - L2→F3，值映射：条→甲，点→乙，环→丙
  - L3→F1，值映射：甲→赤，乙→青，丙→白

• S6（循环：L1→F3, L2→F1, L3→F2）：
  - L1→F3，值映射：赤→甲，青→乙，白→丙
  - L2→F1，值映射：条→赤，点→青，环→白
  - L3→F2，值映射：甲→条，乙→点，丙→环

在某一真实方案下，文本配方被解释为对实际字段的并发筛选（交集），从而定义目标子集T。

你的任务是通过查询推理出真实的解释方案和目标子集T。

- 查询格式：每次选择一个对象子集Q提交，返回计数c（Q与T的交集大小）。
- 约束条件：
  • 第1次查询必须为全体{{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}}
  • 至少完成2次查询后，方可提交最终判断
  • 查询应尽可能少

查询格式（提交子集编号，用逗号分隔）：
<query>1,2,3,4,5,6,7,8,9,10,11,12,13,14,15</query>

最终判断格式（方案编号和目标子集编号）：
<answer>scheme=S1, target=1,2,3</answer>

注意：编号顺序不限，但内容必须完全正确。
"""

    game_rule_en = """\
Let's play a "Field Mapping Reasoning" game with the following rules:

The game has a dataset of 15 objects, each with three discrete fields F1, F2, F3, with value domains:
• F1 ∈ {{Red, Blue, White}}
• F2 ∈ {{Bar, Dot, Ring}}
• F3 ∈ {{Alpha, Beta, Gamma}}

Object list (ID: (F1, F2, F3)):
1:(Red,Bar,Alpha)     2:(Red,Dot,Alpha)     3:(Red,Ring,Beta)    4:(Blue,Bar,Beta)     5:(Blue,Dot,Gamma)
6:(Blue,Ring,Alpha)   7:(White,Bar,Gamma)   8:(White,Dot,Beta)   9:(White,Ring,Gamma) 10:(Red,Bar,Beta)
11:(Blue,Dot,Alpha)  12:(White,Dot,Alpha)  13:(Red,Ring,Gamma)  14:(Blue,Bar,Gamma)  15:(White,Bar,Beta)

There is a text recipe with three columns L1, L2, L3 and their values:
• L1 = {recipe_L1}
• L2 = {recipe_L2}
• L3 = {recipe_L3}

There are six possible interpretation schemes that map recipe field names and values to actual fields F1/F2/F3:

• S1 (Identity mapping):
  - L1→F1, value mapping: Red→Red, Blue→Blue, White→White
  - L2→F2, value mapping: Bar→Bar, Dot→Dot, Ring→Ring
  - L3→F3, value mapping: Alpha→Alpha, Beta→Beta, Gamma→Gamma

• S2 (F1 and F2 swapped):
  - L1→F2, value mapping: Red→Bar, Blue→Dot, White→Ring
  - L2→F1, value mapping: Bar→Red, Dot→Blue, Ring→White
  - L3→F3, value mapping: Alpha→Alpha, Beta→Beta, Gamma→Gamma

• S3 (F1 and F3 swapped):
  - L1→F3, value mapping: Red→Alpha, Blue→Beta, White→Gamma
  - L2→F2, value mapping: Bar→Bar, Dot→Dot, Ring→Ring
  - L3→F1, value mapping: Alpha→Red, Beta→Blue, Gamma→White

• S4 (F2 and F3 swapped):
  - L1→F1, value mapping: Red→Red, Blue→Blue, White→White
  - L2→F3, value mapping: Bar→Alpha, Dot→Beta, Ring→Gamma
  - L3→F2, value mapping: Alpha→Bar, Beta→Dot, Gamma→Ring

• S5 (Cycle: L1→F2, L2→F3, L3→F1):
  - L1→F2, value mapping: Red→Bar, Blue→Dot, White→Ring
  - L2→F3, value mapping: Bar→Alpha, Dot→Beta, Ring→Gamma
  - L3→F1, value mapping: Alpha→Red, Beta→Blue, Gamma→White

• S6 (Cycle: L1→F3, L2→F1, L3→F2):
  - L1→F3, value mapping: Red→Alpha, Blue→Beta, White→Gamma
  - L2→F1, value mapping: Bar→Red, Dot→Blue, Ring→White
  - L3→F2, value mapping: Alpha→Bar, Beta→Dot, Gamma→Ring

Under a true scheme, the text recipe is interpreted as concurrent filtering (intersection) on actual fields, defining target subset T.

Your task is to infer the true interpretation scheme and target subset T through queries.

- Query format: Submit an object subset Q each time, receive count c (size of Q intersection T).
- Constraints:
  • First query must be the full set {{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}}
  • At least 2 queries must be completed before final submission
  • Queries should be minimized

Query format (submit subset IDs, comma-separated):
<query>1,2,3,4,5,6,7,8,9,10,11,12,13,14,15</query>

Final answer format (scheme ID and target subset IDs):
<answer>scheme=S1, target=1,2,3</answer>

Note: Order doesn't matter, but content must be completely correct.
"""

    contextualized_rule_zh_1 = """\
我们来处理一项"智慧交通路网事件协同排查"任务，规则如下：

交警指挥系统记录了15个交通事故档案，每个档案由三个离散特征字段F1、F2、F3构成，取值域分别为：
• F1(事件预警级别) ∈ {{赤, 青, 白}}
• F2(事发路段拓扑) ∈ {{条, 点, 环}}
• F3(处理管辖大队) ∈ {{甲, 乙, 丙}}

档案列表（编号: (F1, F2, F3)）：
1:(赤,条,甲)   2:(赤,点,甲)   3:(赤,环,乙)   4:(青,条,乙)   5:(青,点,丙)
6:(青,环,甲)   7:(白,条,丙)   8:(白,点,乙)   9:(白,环,丙)   10:(赤,条,乙)
11:(青,点,甲)  12:(白,点,甲)  13:(赤,环,丙)  14:(青,条,丙)  15:(白,条,乙)

交管中心下发了一份联动指令配方，包含三栏检索字段L1、L2、L3及其对应的值词：
• L1 = {recipe_L1}
• L2 = {recipe_L2}
• L3 = {recipe_L3}

由于新老系统协议不兼容，存在六种可能的网关路由解释方案，将指令字段名与值词映射到实际底层字段F1/F2/F3及其取值：

• S1（恒等映射）：
  - L1→F1，值映射：赤→赤，青→青，白→白
  - L2→F2，值映射：条→条，点→点，环→环
  - L3→F3，值映射：甲→甲，乙→乙，丙→丙

• S2（F1与F2互换）：
  - L1→F2，值映射：赤→条，青→点，白→环
  - L2→F1，值映射：条→赤，点→青，环→白
  - L3→F3，值映射：甲→甲，乙→乙，丙→丙

• S3（F1与F3互换）：
  - L1→F3，值映射：赤→甲，青→乙，白→丙
  - L2→F2，值映射：条→条，点→点，环→环
  - L3→F1，值映射：甲→赤，乙→青，丙→白

• S4（F2与F3互换）：
  - L1→F1，值映射：赤→赤，青→青，白→白
  - L2→F3，值映射：条→甲，点→乙，环→丙
  - L3→F2，值映射：甲→条，乙→点，丙→环

• S5（循环：L1→F2, L2→F3, L3→F1）：
  - L1→F2，值映射：赤→条，青→点，白→环
  - L2→F3，值映射：条→甲，点→乙，环→丙
  - L3→F1，值映射：甲→赤，乙→青，丙→白

• S6（循环：L1→F3, L2→F1, L3→F2）：
  - L1→F3，值映射：赤→甲，青→乙，白→丙
  - L2→F1，值映射：条→赤，点→青，环→白
  - L3→F2，值映射：甲→条，乙→点，丙→环

在某一真实路由方案下，联动指令配方被解释为对实际特征的并发筛选（交集），从而定义目标排查子集T。

你的任务是通过试探性查询，推理出真实的解释方案和目标档案子集T。

- 查询格式：每次选择一个对象子集Q提交，返回计数c（Q与T的交集大小）。
- 约束条件：
  • 第1次查询必须为全体{{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}}
  • 至少完成2次查询后，方可提交最终判断
  • 查询应尽可能少

查询格式（提交子集编号，用逗号分隔）：
<query>1,2,3,4,5,6,7,8,9,10,11,12,13,14,15</query>

最终判断格式（方案编号和目标子集编号）：
<answer>scheme=S1, target=1,2,3</answer>

注意：编号顺序不限，但内容必须完全正确。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's process a "Smart Traffic Network Event Collaborative Screening" task with the following rules:

The traffic command system has a dataset of 15 traffic accident archives, each with three discrete feature fields F1, F2, F3, with value domains:
• F1 (Warning Level) ∈ {{Red, Blue, White}}
• F2 (Road Topology) ∈ {{Bar, Dot, Ring}}
• F3 (Jurisdiction Brigade) ∈ {{Alpha, Beta, Gamma}}

Object list (ID: (F1, F2, F3)):
1:(Red,Bar,Alpha)     2:(Red,Dot,Alpha)     3:(Red,Ring,Beta)    4:(Blue,Bar,Beta)     5:(Blue,Dot,Gamma)
6:(Blue,Ring,Alpha)   7:(White,Bar,Gamma)   8:(White,Dot,Beta)   9:(White,Ring,Gamma) 10:(Red,Bar,Beta)
11:(Blue,Dot,Alpha)  12:(White,Dot,Alpha)  13:(Red,Ring,Gamma)  14:(Blue,Bar,Gamma)  15:(White,Bar,Beta)

The command center issued a coordinated screening recipe with three columns L1, L2, L3 and their values:
• L1 = {recipe_L1}
• L2 = {recipe_L2}
• L3 = {recipe_L3}

Due to protocol incompatibilities between legacy and new systems, there are six possible gateway routing interpretation schemes that map recipe field names and values to actual fields F1/F2/F3:

• S1 (Identity mapping):
  - L1→F1, value mapping: Red→Red, Blue→Blue, White→White
  - L2→F2, value mapping: Bar→Bar, Dot→Dot, Ring→Ring
  - L3→F3, value mapping: Alpha→Alpha, Beta→Beta, Gamma→Gamma

• S2 (F1 and F2 swapped):
  - L1→F2, value mapping: Red→Bar, Blue→Dot, White→Ring
  - L2→F1, value mapping: Bar→Red, Dot→Blue, Ring→White
  - L3→F3, value mapping: Alpha→Alpha, Beta→Beta, Gamma→Gamma

• S3 (F1 and F3 swapped):
  - L1→F3, value mapping: Red→Alpha, Blue→Beta, White→Gamma
  - L2→F2, value mapping: Bar→Bar, Dot→Dot, Ring→Ring
  - L3→F1, value mapping: Alpha→Red, Beta→Blue, Gamma→White

• S4 (F2 and F3 swapped):
  - L1→F1, value mapping: Red→Red, Blue→Blue, White→White
  - L2→F3, value mapping: Bar→Alpha, Dot→Beta, Ring→Gamma
  - L3→F2, value mapping: Alpha→Bar, Beta→Dot, Gamma→Ring

• S5 (Cycle: L1→F2, L2→F3, L3→F1):
  - L1→F2, value mapping: Red→Bar, Blue→Dot, White→Ring
  - L2→F3, value mapping: Bar→Alpha, Dot→Beta, Ring→Gamma
  - L3→F1, value mapping: Alpha→Red, Beta→Blue, Gamma→White

• S6 (Cycle: L1→F3, L2→F1, L3→F2):
  - L1→F3, value mapping: Red→Alpha, Blue→Beta, White→Gamma
  - L2→F1, value mapping: Bar→Red, Dot→Blue, Ring→White
  - L3→F2, value mapping: Alpha→Bar, Beta→Dot, Gamma→Ring

Under a true routing scheme, the screening recipe is interpreted as concurrent filtering (intersection) on actual fields, defining target subset T.

Your task is to infer the true interpretation scheme and target subset T through queries.

- Query format: Submit an object subset Q each time, receive count c (size of Q intersection T).
- Constraints:
  • First query must be the full set {{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}}
  • At least 2 queries must be completed before final submission
  • Queries should be minimized

Query format (submit subset IDs, comma-separated):
<query>1,2,3,4,5,6,7,8,9,10,11,12,13,14,15</query>

Final answer format (scheme ID and target subset IDs):
<answer>scheme=S1, target=1,2,3</answer>

Note: Order doesn't matter, but content must be completely correct.
"""

    contextualized_rule_zh_2 = """\
我们来执行一项"临床电子病历数据提取与清洗"任务，规则如下：

医院数据库中封存了15份疑难病例，每个病例含有三个离散体征字段F1、F2、F3，取值域分别为：
• F1(分诊优先级) ∈ {{赤, 青, 白}}
• F2(病灶形态学) ∈ {{条, 点, 环}}
• F3(首诊责任科室) ∈ {{甲, 乙, 丙}}

病例列表（编号: (F1, F2, F3)）：
1:(赤,条,甲)   2:(赤,点,甲)   3:(赤,环,乙)   4:(青,条,乙)   5:(青,点,丙)
6:(青,环,甲)   7:(白,条,丙)   8:(白,点,乙)   9:(白,环,丙)   10:(赤,条,乙)
11:(青,点,甲)  12:(白,点,甲)  13:(赤,环,丙)  14:(青,条,丙)  15:(白,条,乙)

现有一份跨院区联合会诊的筛查配方，包含三栏检索指标L1、L2、L3及其对应的值词：
• L1 = {recipe_L1}
• L2 = {recipe_L2}
• L3 = {recipe_L3}

由于医疗系统存在HIS与PACS数据字典映射混乱，存在六种可能的解析方案，将配方的字段与值词映射到实际存储字段F1/F2/F3及其取值：

• S1（恒等映射）：
  - L1→F1，值映射：赤→赤，青→青，白→白
  - L2→F2，值映射：条→条，点→点，环→环
  - L3→F3，值映射：甲→甲，乙→乙，丙→丙

• S2（F1与F2互换）：
  - L1→F2，值映射：赤→条，青→点，白→环
  - L2→F1，值映射：条→赤，点→青，环→白
  - L3→F3，值映射：甲→甲，乙→乙，丙→丙

• S3（F1与F3互换）：
  - L1→F3，值映射：赤→甲，青→乙，白→丙
  - L2→F2，值映射：条→条，点→点，环→环
  - L3→F1，值映射：甲→赤，乙→青，丙→白

• S4（F2与F3互换）：
  - L1→F1，值映射：赤→赤，青→青，白→白
  - L2→F3，值映射：条→甲，点→乙，环→丙
  - L3→F2，值映射：甲→条，乙→点，丙→环

• S5（循环：L1→F2, L2→F3, L3→F1）：
  - L1→F2，值映射：赤→条，青→点，白→环
  - L2→F3，值映射：条→甲，点→乙，环→丙
  - L3→F1，值映射：甲→赤，乙→青，丙→白

• S6（循环：L1→F3, L2→F1, L3→F2）：
  - L1→F3，值映射：赤→甲，青→乙，白→丙
  - L2→F1，值映射：条→赤，点→青，环→白
  - L3→F2，值映射：甲→条，乙→点，丙→环

在某一真实的数据解析方案下，会诊筛查配方被解释为对实际病征的并发筛选（交集），从而锁定目标病例集T。

你的任务是通过查询系统的反馈，推理出真实的解析方案和目标病例集T。

- 查询格式：每次选择一个对象子集Q提交，返回计数c（Q与T的交集大小）。
- 约束条件：
  • 第1次查询必须为全体{{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}}
  • 至少完成2次查询后，方可提交最终判断
  • 查询应尽可能少

查询格式（提交子集编号，用逗号分隔）：
<query>1,2,3,4,5,6,7,8,9,10,11,12,13,14,15</query>

最终判断格式（方案编号和目标子集编号）：
<answer>scheme=S1, target=1,2,3</answer>

注意：编号顺序不限，但内容必须完全正确。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's execute a "Clinical EMR Data Extraction and Cleansing" task with the following rules:

The hospital database archives 15 complex medical cases, each with three discrete clinical fields F1, F2, F3, with value domains:
• F1 (Triage Priority) ∈ {{Red, Blue, White}}
• F2 (Lesion Morphology) ∈ {{Bar, Dot, Ring}}
• F3 (Primary Department) ∈ {{Alpha, Beta, Gamma}}

Object list (ID: (F1, F2, F3)):
1:(Red,Bar,Alpha)     2:(Red,Dot,Alpha)     3:(Red,Ring,Beta)    4:(Blue,Bar,Beta)     5:(Blue,Dot,Gamma)
6:(Blue,Ring,Alpha)   7:(White,Bar,Gamma)   8:(White,Dot,Beta)   9:(White,Ring,Gamma) 10:(Red,Bar,Beta)
11:(Blue,Dot,Alpha)  12:(White,Dot,Alpha)  13:(Red,Ring,Gamma)  14:(Blue,Bar,Gamma)  15:(White,Bar,Beta)

There is a cross-campus joint consultation screening recipe with three columns L1, L2, L3 and their values:
• L1 = {recipe_L1}
• L2 = {recipe_L2}
• L3 = {recipe_L3}

Due to data dictionary mapping confusion between HIS and PACS systems, there are six possible parsing schemes that map recipe field names and values to actual fields F1/F2/F3:

• S1 (Identity mapping):
  - L1→F1, value mapping: Red→Red, Blue→Blue, White→White
  - L2→F2, value mapping: Bar→Bar, Dot→Dot, Ring→Ring
  - L3→F3, value mapping: Alpha→Alpha, Beta→Beta, Gamma→Gamma

• S2 (F1 and F2 swapped):
  - L1→F2, value mapping: Red→Bar, Blue→Dot, White→Ring
  - L2→F1, value mapping: Bar→Red, Dot→Blue, Ring→White
  - L3→F3, value mapping: Alpha→Alpha, Beta→Beta, Gamma→Gamma

• S3 (F1 and F3 swapped):
  - L1→F3, value mapping: Red→Alpha, Blue→Beta, White→Gamma
  - L2→F2, value mapping: Bar→Bar, Dot→Dot, Ring→Ring
  - L3→F1, value mapping: Alpha→Red, Beta→Blue, Gamma→White

• S4 (F2 and F3 swapped):
  - L1→F1, value mapping: Red→Red, Blue→Blue, White→White
  - L2→F3, value mapping: Bar→Alpha, Dot→Beta, Ring→Gamma
  - L3→F2, value mapping: Alpha→Bar, Beta→Dot, Gamma→Ring

• S5 (Cycle: L1→F2, L2→F3, L3→F1):
  - L1→F2, value mapping: Red→Bar, Blue→Dot, White→Ring
  - L2→F3, value mapping: Bar→Alpha, Dot→Beta, Ring→Gamma
  - L3→F1, value mapping: Alpha→Red, Beta→Blue, Gamma→White

• S6 (Cycle: L1→F3, L2→F1, L3→F2):
  - L1→F3, value mapping: Red→Alpha, Blue→Beta, White→Gamma
  - L2→F1, value mapping: Bar→Red, Dot→Blue, Ring→White
  - L3→F2, value mapping: Alpha→Bar, Beta→Dot, Gamma→Ring

Under a true parsing scheme, the screening recipe is interpreted as concurrent filtering (intersection) on actual clinical features, defining target case subset T.

Your task is to infer the true interpretation scheme and target subset T through queries.

- Query format: Submit an object subset Q each time, receive count c (size of Q intersection T).
- Constraints:
  • First query must be the full set {{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}}
  • At least 2 queries must be completed before final submission
  • Queries should be minimized

Query format (submit subset IDs, comma-separated):
<query>1,2,3,4,5,6,7,8,9,10,11,12,13,14,15</query>

Final answer format (scheme ID and target subset IDs):
<answer>scheme=S1, target=1,2,3</answer>

Note: Order doesn't matter, but content must be completely correct.
"""

    contextualized_rule_zh_3 = """\
我们来进行一项"学情特征图谱数据映射"分析，规则如下：

教务系统抽样了15个学生画像档案，每个档案具备三个离散行为字段F1、F2、F3，取值域分别为：
• F1(学业预警状态) ∈ {{赤, 青, 白}}
• F2(知识盲点结构) ∈ {{条, 点, 环}}
• F3(所属教学班组) ∈ {{甲, 乙, 丙}}

档案列表（编号: (F1, F2, F3)）：
1:(赤,条,甲)   2:(赤,点,甲)   3:(赤,环,乙)   4:(青,条,乙)   5:(青,点,丙)
6:(青,环,甲)   7:(白,条,丙)   8:(白,点,乙)   9:(白,环,丙)   10:(赤,条,乙)
11:(青,点,甲)  12:(白,点,甲)  13:(赤,环,丙)  14:(青,条,丙)  15:(白,条,乙)

系统生成了一份精准辅导筛查配方，包含三栏干预维度L1、L2、L3及其对应的值词：
• L1 = {recipe_L1}
• L2 = {recipe_L2}
• L3 = {recipe_L3}

由于中台标签体系重构，存在六种可能的规则解释方案，用于将配方的字段与值词映射到实际画像字段F1/F2/F3及其取值：

• S1（恒等映射）：
  - L1→F1，值映射：赤→赤，青→青，白→白
  - L2→F2，值映射：条→条，点→点，环→环
  - L3→F3，值映射：甲→甲，乙→乙，丙→丙

• S2（F1与F2互换）：
  - L1→F2，值映射：赤→条，青→点，白→环
  - L2→F1，值映射：条→赤，点→青，环→白
  - L3→F3，值映射：甲→甲，乙→乙，丙→丙

• S3（F1与F3互换）：
  - L1→F3，值映射：赤→甲，青→乙，白→丙
  - L2→F2，值映射：条→条，点→点，环→环
  - L3→F1，值映射：甲→赤，乙→青，丙→白

• S4（F2与F3互换）：
  - L1→F1，值映射：赤→赤，青→青，白→白
  - L2→F3，值映射：条→甲，点→乙，环→丙
  - L3→F2，值映射：甲→条，乙→点，丙→环

• S5（循环：L1→F2, L2→F3, L3→F1）：
  - L1→F2，值映射：赤→条，青→点，白→环
  - L2→F3，值映射：条→甲，点→乙，环→丙
  - L3→F1，值映射：甲→赤，乙→青，丙→白

• S6（循环：L1→F3, L2→F1, L3→F2）：
  - L1→F3，值映射：赤→甲，青→乙，白→丙
  - L2→F1，值映射：条→赤，点→青，环→白
  - L3→F2，值映射：甲→条，乙→点，丙→环

在某一真实的规则方案下，辅导配方被解释为对实际画像的并发筛选（交集），从而圈定目标辅导群体T。

你的任务是通过试探查询推理出真实的规则解释方案和目标群体T。

- 查询格式：每次选择一个对象子集Q提交，返回计数c（Q与T的交集大小）。
- 约束条件：
  • 第1次查询必须为全体{{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}}
  • 至少完成2次查询后，方可提交最终判断
  • 查询应尽可能少

查询格式（提交子集编号，用逗号分隔）：
<query>1,2,3,4,5,6,7,8,9,10,11,12,13,14,15</query>

最终判断格式（方案编号和目标子集编号）：
<answer>scheme=S1, target=1,2,3</answer>

注意：编号顺序不限，但内容必须完全正确。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a "Learning Profile Data Mapping" analysis with the following rules:

The academic system sampled 15 student profiles, each with three discrete behavioral fields F1, F2, F3, with value domains:
• F1 (Academic Alert Status) ∈ {{Red, Blue, White}}
• F2 (Knowledge Gap Structure) ∈ {{Bar, Dot, Ring}}
• F3 (Teaching Cohort) ∈ {{Alpha, Beta, Gamma}}

Object list (ID: (F1, F2, F3)):
1:(Red,Bar,Alpha)     2:(Red,Dot,Alpha)     3:(Red,Ring,Beta)    4:(Blue,Bar,Beta)     5:(Blue,Dot,Gamma)
6:(Blue,Ring,Alpha)   7:(White,Bar,Gamma)   8:(White,Dot,Beta)   9:(White,Ring,Gamma) 10:(Red,Bar,Beta)
11:(Blue,Dot,Alpha)  12:(White,Dot,Alpha)  13:(Red,Ring,Gamma)  14:(Blue,Bar,Gamma)  15:(White,Bar,Beta)

The system generated a precise tutoring screening recipe with three intervention dimensions L1, L2, L3 and their values:
• L1 = {recipe_L1}
• L2 = {recipe_L2}
• L3 = {recipe_L3}

Due to the refactoring of the middle-tier tagging system, there are six possible rule interpretation schemes that map recipe field names and values to actual fields F1/F2/F3:

• S1 (Identity mapping):
  - L1→F1, value mapping: Red→Red, Blue→Blue, White→White
  - L2→F2, value mapping: Bar→Bar, Dot→Dot, Ring→Ring
  - L3→F3, value mapping: Alpha→Alpha, Beta→Beta, Gamma→Gamma

• S2 (F1 and F2 swapped):
  - L1→F2, value mapping: Red→Bar, Blue→Dot, White→Ring
  - L2→F1, value mapping: Bar→Red, Dot→Blue, Ring→White
  - L3→F3, value mapping: Alpha→Alpha, Beta→Beta, Gamma→Gamma

• S3 (F1 and F3 swapped):
  - L1→F3, value mapping: Red→Alpha, Blue→Beta, White→Gamma
  - L2→F2, value mapping: Bar→Bar, Dot→Dot, Ring→Ring
  - L3→F1, value mapping: Alpha→Red, Beta→Blue, Gamma→White

• S4 (F2 and F3 swapped):
  - L1→F1, value mapping: Red→Red, Blue→Blue, White→White
  - L2→F3, value mapping: Bar→Alpha, Dot→Beta, Ring→Gamma
  - L3→F2, value mapping: Alpha→Bar, Beta→Dot, Gamma→Ring

• S5 (Cycle: L1→F2, L2→F3, L3→F1):
  - L1→F2, value mapping: Red→Bar, Blue→Dot, White→Ring
  - L2→F3, value mapping: Bar→Alpha, Dot→Beta, Ring→Gamma
  - L3→F1, value mapping: Alpha→Red, Beta→Blue, Gamma→White

• S6 (Cycle: L1→F3, L2→F1, L3→F2):
  - L1→F3, value mapping: Red→Alpha, Blue→Beta, White→Gamma
  - L2→F1, value mapping: Bar→Red, Dot→Blue, Ring→White
  - L3→F2, value mapping: Alpha→Bar, Beta→Dot, Gamma→Ring

Under a true rule scheme, the tutoring recipe is interpreted as concurrent filtering (intersection) on actual profiles, defining target student subset T.

Your task is to infer the true interpretation scheme and target subset T through queries.

- Query format: Submit an object subset Q each time, receive count c (size of Q intersection T).
- Constraints:
  • First query must be the full set {{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}}
  • At least 2 queries must be completed before final submission
  • Queries should be minimized

Query format (submit subset IDs, comma-separated):
<query>1,2,3,4,5,6,7,8,9,10,11,12,13,14,15</query>

Final answer format (scheme ID and target subset IDs):
<answer>scheme=S1, target=1,2,3</answer>

Note: Order doesn't matter, but content must be completely correct.
"""

    contextualized_rule_zh_4 = """\
我们来解决一项"工业物联网质检信号解析"难题，规则如下：

数字孪生系统监测到15个疑似缺陷的工件，每个工件带有三个离散传感器读数字段F1、F2、F3，取值域分别为：
• F1(光电警示级别) ∈ {{赤, 青, 白}}
• F2(物理瑕疵形态) ∈ {{条, 点, 环}}
• F3(流转加工产线) ∈ {{甲, 乙, 丙}}

工件列表（编号: (F1, F2, F3)）：
1:(赤,条,甲)   2:(赤,点,甲)   3:(赤,环,乙)   4:(青,条,乙)   5:(青,点,丙)
6:(青,环,甲)   7:(白,条,丙)   8:(白,点,乙)   9:(白,环,丙)   10:(赤,条,乙)
11:(青,点,甲)  12:(白,点,甲)  13:(赤,环,丙)  14:(青,条,丙)  15:(白,条,乙)

质检中控机下发了一份瑕疵排查配方，包含三栏遥测信号L1、L2、L3及其对应的值词：
• L1 = {recipe_L1}
• L2 = {recipe_L2}
• L3 = {recipe_L3}

由于PLC控制器的寄存器地址错位，存在六种可能的解码解释方案，将排查配方的信号域与值词映射到实际物理字段F1/F2/F3及其取值：

• S1（恒等映射）：
  - L1→F1，值映射：赤→赤，青→青，白→白
  - L2→F2，值映射：条→条，点→点，环→环
  - L3→F3，值映射：甲→甲，乙→乙，丙→丙

• S2（F1与F2互换）：
  - L1→F2，值映射：赤→条，青→点，白→环
  - L2→F1，值映射：条→赤，点→青，环→白
  - L3→F3，值映射：甲→甲，乙→乙，丙→丙

• S3（F1与F3互换）：
  - L1→F3，值映射：赤→甲，青→乙，白→丙
  - L2→F2，值映射：条→条，点→点，环→环
  - L3→F1，值映射：甲→赤，乙→青，丙→白

• S4（F2与F3互换）：
  - L1→F1，值映射：赤→赤，青→青，白→白
  - L2→F3，值映射：条→甲，点→乙，环→丙
  - L3→F2，值映射：甲→条，乙→点，丙→环

• S5（循环：L1→F2, L2→F3, L3→F1）：
  - L1→F2，值映射：赤→条，青→点，白→环
  - L2→F3，值映射：条→甲，点→乙，环→丙
  - L3→F1，值映射：甲→赤，乙→青，丙→白

• S6（循环：L1→F3, L2→F1, L3→F2）：
  - L1→F3，值映射：赤→甲，青→乙，白→丙
  - L2→F1，值映射：条→赤，点→青，环→白
  - L3→F2，值映射：甲→条，乙→点，丙→环

在某一真实的解码方案下，排查配方被解释为对实际工件属性的并发筛选（交集），从而隔离出目标废品集合T。

你的任务是通过发送测试查询，推理出真实的解码解释方案和目标废品集合T。

- 查询格式：每次选择一个对象子集Q提交，返回计数c（Q与T的交集大小）。
- 约束条件：
  • 第1次查询必须为全体{{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}}
  • 至少完成2次查询后，方可提交最终判断
  • 查询应尽可能少

查询格式（提交子集编号，用逗号分隔）：
<query>1,2,3,4,5,6,7,8,9,10,11,12,13,14,15</query>

最终判断格式（方案编号和目标子集编号）：
<answer>scheme=S1, target=1,2,3</answer>

注意：编号顺序不限，但内容必须完全正确。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's solve an "Industrial IoT Quality Inspection Signal Parsing" challenge with the following rules:

The digital twin system monitors 15 suspected defective workpieces, each with three discrete sensor readings F1, F2, F3, with value domains:
• F1 (Photoelectric Warning Level) ∈ {{Red, Blue, White}}
• F2 (Physical Defect Morphology) ∈ {{Bar, Dot, Ring}}
• F3 (Processing Production Line) ∈ {{Alpha, Beta, Gamma}}

Object list (ID: (F1, F2, F3)):
1:(Red,Bar,Alpha)     2:(Red,Dot,Alpha)     3:(Red,Ring,Beta)    4:(Blue,Bar,Beta)     5:(Blue,Dot,Gamma)
6:(Blue,Ring,Alpha)   7:(White,Bar,Gamma)   8:(White,Dot,Beta)   9:(White,Ring,Gamma) 10:(Red,Bar,Beta)
11:(Blue,Dot,Alpha)  12:(White,Dot,Alpha)  13:(Red,Ring,Gamma)  14:(Blue,Bar,Gamma)  15:(White,Bar,Beta)

The QA central controller issued a defect screening recipe with three telemetry signals L1, L2, L3 and their values:
• L1 = {recipe_L1}
• L2 = {recipe_L2}
• L3 = {recipe_L3}

Due to misaligned register addresses in the PLC controller, there are six possible decoding interpretation schemes that map recipe field names and values to actual fields F1/F2/F3:

• S1 (Identity mapping):
  - L1→F1, value mapping: Red→Red, Blue→Blue, White→White
  - L2→F2, value mapping: Bar→Bar, Dot→Dot, Ring→Ring
  - L3→F3, value mapping: Alpha→Alpha, Beta→Beta, Gamma→Gamma

• S2 (F1 and F2 swapped):
  - L1→F2, value mapping: Red→Bar, Blue→Dot, White→Ring
  - L2→F1, value mapping: Bar→Red, Dot→Blue, Ring→White
  - L3→F3, value mapping: Alpha→Alpha, Beta→Beta, Gamma→Gamma

• S3 (F1 and F3 swapped):
  - L1→F3, value mapping: Red→Alpha, Blue→Beta, White→Gamma
  - L2→F2, value mapping: Bar→Bar, Dot→Dot, Ring→Ring
  - L3→F1, value mapping: Alpha→Red, Beta→Blue, Gamma→White

• S4 (F2 and F3 swapped):
  - L1→F1, value mapping: Red→Red, Blue→Blue, White→White
  - L2→F3, value mapping: Bar→Alpha, Dot→Beta, Ring→Gamma
  - L3→F2, value mapping: Alpha→Bar, Beta→Dot, Gamma→Ring

• S5 (Cycle: L1→F2, L2→F3, L3→F1):
  - L1→F2, value mapping: Red→Bar, Blue→Dot, White→Ring
  - L2→F3, value mapping: Bar→Alpha, Dot→Beta, Ring→Gamma
  - L3→F1, value mapping: Alpha→Red, Beta→Blue, Gamma→White

• S6 (Cycle: L1→F3, L2→F1, L3→F2):
  - L1→F3, value mapping: Red→Alpha, Blue→Beta, White→Gamma
  - L2→F1, value mapping: Bar→Red, Dot→Blue, Ring→White
  - L3→F2, value mapping: Alpha→Bar, Beta→Dot, Gamma→Ring

Under a true decoding scheme, the screening recipe is interpreted as concurrent filtering (intersection) on actual workpiece attributes, isolating target scrap subset T.

Your task is to infer the true interpretation scheme and target subset T through queries.

- Query format: Submit an object subset Q each time, receive count c (size of Q intersection T).
- Constraints:
  • First query must be the full set {{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}}
  • At least 2 queries must be completed before final submission
  • Queries should be minimized

Query format (submit subset IDs, comma-separated):
<query>1,2,3,4,5,6,7,8,9,10,11,12,13,14,15</query>

Final answer format (scheme ID and target subset IDs):
<answer>scheme=S1, target=1,2,3</answer>

Note: Order doesn't matter, but content must be completely correct.
"""

    contextualized_rule_zh_5 = """\
我们来推演一项"类案卷宗交叉检索与证据链重构"任务，规则如下：

司法大数据库中提取了15宗指导性案例，每个案例标注了三个离散案情字段F1、F2、F3，取值域分别为：
• F1(卷宗解密授权) ∈ {{赤, 青, 白}}
• F2(关联证据结构) ∈ {{条, 点, 环}}
• F3(管辖审理法庭) ∈ {{甲, 乙, 丙}}

案卷列表（编号: (F1, F2, F3)）：
1:(赤,条,甲)   2:(赤,点,甲)   3:(赤,环,乙)   4:(青,条,乙)   5:(青,点,丙)
6:(青,环,甲)   7:(白,条,丙)   8:(白,点,乙)   9:(白,环,丙)   10:(赤,条,乙)
11:(青,点,甲)  12:(白,点,甲)  13:(赤,环,丙)  14:(青,条,丙)  15:(白,条,乙)

专案组出具了一份证据摸排配方，包含三栏检索关键字L1、L2、L3及其对应的值词：
• L1 = {recipe_L1}
• L2 = {recipe_L2}
• L3 = {recipe_L3}

因多地内网数据汇聚时的表结构冲突，存在六种可能的司法解释方案，用于将配方的关键字与值词映射到实际案情字段F1/F2/F3及其取值：

• S1（恒等映射）：
  - L1→F1，值映射：赤→赤，青→青，白→白
  - L2→F2，值映射：条→条，点→点，环→环
  - L3→F3，值映射：甲→甲，乙→乙，丙→丙

• S2（F1与F2互换）：
  - L1→F2，值映射：赤→条，青→点，白→环
  - L2→F1，值映射：条→赤，点→青，环→白
  - L3→F3，值映射：甲→甲，乙→乙，丙→丙

• S3（F1与F3互换）：
  - L1→F3，值映射：赤→甲，青→乙，白→丙
  - L2→F2，值映射：条→条，点→点，环→环
  - L3→F1，值映射：甲→赤，乙→青，丙→白

• S4（F2与F3互换）：
  - L1→F1，值映射：赤→赤，青→青，白→白
  - L2→F3，值映射：条→甲，点→乙，环→丙
  - L3→F2，值映射：甲→条，乙→点，丙→环

• S5（循环：L1→F2, L2→F3, L3→F1）：
  - L1→F2，值映射：赤→条，青→点，白→环
  - L2→F3，值映射：条→甲，点→乙，环→丙
  - L3→F1，值映射：甲→赤，乙→青，丙→白

• S6（循环：L1→F3, L2→F1, L3→F2）：
  - L1→F3，值映射：赤→甲，青→乙，白→丙
  - L2→F1，值映射：条→赤，点→青，环→白
  - L3→F2，值映射：甲→条，乙→点，丙→环

在某一真实的司法解释方案下，摸排配方被解析为对实际案例要素的并发筛选（交集），从而锁定目标并案集合T。

你的任务是通过模拟检索引擎反馈，推理出真实的司法解释方案和目标案例集合T。

- 查询格式：每次选择一个对象子集Q提交，返回计数c（Q与T的交集大小）。
- 约束条件：
  • 第1次查询必须为全体{{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}}
  • 至少完成2次查询后，方可提交最终判断
  • 查询应尽可能少

查询格式（提交子集编号，用逗号分隔）：
<query>1,2,3,4,5,6,7,8,9,10,11,12,13,14,15</query>

最终判断格式（方案编号和目标子集编号）：
<answer>scheme=S1, target=1,2,3</answer>

注意：编号顺序不限，但内容必须完全正确。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's deduce a "Precedent Case Cross-Retrieval and Evidence Chain Reconstruction" task with the following rules:

The judicial big data repository extracted 15 guiding cases, each annotated with three discrete case fields F1, F2, F3, with value domains:
• F1 (Dossier Clearance Level) ∈ {{Red, Blue, White}}
• F2 (Correlated Evidence Structure) ∈ {{Bar, Dot, Ring}}
• F3 (Jurisdictional Court) ∈ {{Alpha, Beta, Gamma}}

Object list (ID: (F1, F2, F3)):
1:(Red,Bar,Alpha)     2:(Red,Dot,Alpha)     3:(Red,Ring,Beta)    4:(Blue,Bar,Beta)     5:(Blue,Dot,Gamma)
6:(Blue,Ring,Alpha)   7:(White,Bar,Gamma)   8:(White,Dot,Beta)   9:(White,Ring,Gamma) 10:(Red,Bar,Beta)
11:(Blue,Dot,Alpha)  12:(White,Dot,Alpha)  13:(Red,Ring,Gamma)  14:(Blue,Bar,Gamma)  15:(White,Bar,Beta)

The special task force issued an evidence screening recipe with three retrieval keywords L1, L2, L3 and their values:
• L1 = {recipe_L1}
• L2 = {recipe_L2}
• L3 = {recipe_L3}

Due to table structure conflicts during multi-regional intranet data aggregation, there are six possible judicial interpretation schemes that map recipe field names and values to actual fields F1/F2/F3:

• S1 (Identity mapping):
  - L1→F1, value mapping: Red→Red, Blue→Blue, White→White
  - L2→F2, value mapping: Bar→Bar, Dot→Dot, Ring→Ring
  - L3→F3, value mapping: Alpha→Alpha, Beta→Beta, Gamma→Gamma

• S2 (F1 and F2 swapped):
  - L1→F2, value mapping: Red→Bar, Blue→Dot, White→Ring
  - L2→F1, value mapping: Bar→Red, Dot→Blue, Ring→White
  - L3→F3, value mapping: Alpha→Alpha, Beta→Beta, Gamma→Gamma

• S3 (F1 and F3 swapped):
  - L1→F3, value mapping: Red→Alpha, Blue→Beta, White→Gamma
  - L2→F2, value mapping: Bar→Bar, Dot→Dot, Ring→Ring
  - L3→F1, value mapping: Alpha→Red, Beta→Blue, Gamma→White

• S4 (F2 and F3 swapped):
  - L1→F1, value mapping: Red→Red, Blue→Blue, White→White
  - L2→F3, value mapping: Bar→Alpha, Dot→Beta, Ring→Gamma
  - L3→F2, value mapping: Alpha→Bar, Beta→Dot, Gamma→Ring

• S5 (Cycle: L1→F2, L2→F3, L3→F1):
  - L1→F2, value mapping: Red→Bar, Blue→Dot, White→Ring
  - L2→F3, value mapping: Bar→Alpha, Dot→Beta, Ring→Gamma
  - L3→F1, value mapping: Alpha→Red, Beta→Blue, Gamma→White

• S6 (Cycle: L1→F3, L2→F1, L3→F2):
  - L1→F3, value mapping: Red→Alpha, Blue→Beta, White→Gamma
  - L2→F1, value mapping: Bar→Red, Dot→Blue, Ring→White
  - L3→F2, value mapping: Alpha→Bar, Beta→Dot, Gamma→Ring

Under a true judicial scheme, the screening recipe is interpreted as concurrent filtering (intersection) on actual case elements, defining target consolidated case subset T.

Your task is to infer the true interpretation scheme and target subset T through queries.

- Query format: Submit an object subset Q each time, receive count c (size of Q intersection T).
- Constraints:
  • First query must be the full set {{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}}
  • At least 2 queries must be completed before final submission
  • Queries should be minimized

Query format (submit subset IDs, comma-separated):
<query>1,2,3,4,5,6,7,8,9,10,11,12,13,14,15</query>

Final answer format (scheme ID and target subset IDs):
<answer>scheme=S1, target=1,2,3</answer>

Note: Order doesn't matter, but content must be completely correct.
"""

    tags = ["answer", "query"]

    reasoning_type = "溯因推理"
    data_structure = "集合"

    DATASET = [
        (1, ("赤", "条", "甲"), ("Red", "Bar", "Alpha")),
        (2, ("赤", "点", "甲"), ("Red", "Dot", "Alpha")),
        (3, ("赤", "环", "乙"), ("Red", "Ring", "Beta")),
        (4, ("青", "条", "乙"), ("Blue", "Bar", "Beta")),
        (5, ("青", "点", "丙"), ("Blue", "Dot", "Gamma")),
        (6, ("青", "环", "甲"), ("Blue", "Ring", "Alpha")),
        (7, ("白", "条", "丙"), ("White", "Bar", "Gamma")),
        (8, ("白", "点", "乙"), ("White", "Dot", "Beta")),
        (9, ("白", "环", "丙"), ("White", "Ring", "Gamma")),
        (10, ("赤", "条", "乙"), ("Red", "Bar", "Beta")),
        (11, ("青", "点", "甲"), ("Blue", "Dot", "Alpha")),
        (12, ("白", "点", "甲"), ("White", "Dot", "Alpha")),
        (13, ("赤", "环", "丙"), ("Red", "Ring", "Gamma")),
        (14, ("青", "条", "丙"), ("Blue", "Bar", "Gamma")),
        (15, ("白", "条", "乙"), ("White", "Bar", "Beta")),
    ]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"recipe": ("赤", "点", "甲"), "scheme": "S1"},
            2: {"recipe": ("白", "环", "乙"), "scheme": "S2"},
            3: {"recipe": ("青", "点", "丙"), "scheme": "S4"},
            4: {"recipe": ("赤", "条", "乙"), "scheme": "S5"},
            5: {"recipe": ("白", "点", "甲"), "scheme": "S6"},
        },
        "en": {
            1: {"recipe": ("Red", "Dot", "Alpha"), "scheme": "S1"},
            2: {"recipe": ("White", "Ring", "Beta"), "scheme": "S2"},
            3: {"recipe": ("Blue", "Dot", "Gamma"), "scheme": "S4"},
            4: {"recipe": ("Red", "Bar", "Beta"), "scheme": "S5"},
            5: {"recipe": ("White", "Dot", "Alpha"), "scheme": "S6"},
        },
    }

    def __init__(self, config):
        self.query_count = 0  
        self.first_query_valid = False  
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self._game_info["recipe_L1"] = cfg["recipe"][0]
        self._game_info["recipe_L2"] = cfg["recipe"][1]
        self._game_info["recipe_L3"] = cfg["recipe"][2]
        
        self.true_scheme = cfg["scheme"]
        self.recipe = cfg["recipe"]
        
        lang_idx = 1 if lang == "zh" else 2
        self.objects = {obj[0]: obj[lang_idx] for obj in self.DATASET}
        
        self.target_set = self._compute_target_set()

    def _compute_target_set(self):
        scheme = self.true_scheme
        recipe_L1, recipe_L2, recipe_L3 = self.recipe
        
        def get_scheme_conditions(lang):
            if lang == "zh":
                f1_values = {"赤": "赤", "青": "青", "白": "白"}
                f2_values = {"条": "条", "点": "点", "环": "环"}
                f3_values = {"甲": "甲", "乙": "乙", "丙": "丙"}
                l1_to_f2 = {"赤": "条", "青": "点", "白": "环"}
                l2_to_f1 = {"条": "赤", "点": "青", "环": "白"}
                l1_to_f3 = {"赤": "甲", "青": "乙", "白": "丙"}
                l3_to_f1 = {"甲": "赤", "乙": "青", "丙": "白"}
                l2_to_f3 = {"条": "甲", "点": "乙", "环": "丙"}
                l3_to_f2 = {"甲": "条", "乙": "点", "丙": "环"}
            else:
                f1_values = {"Red": "Red", "Blue": "Blue", "White": "White"}
                f2_values = {"Bar": "Bar", "Dot": "Dot", "Ring": "Ring"}
                f3_values = {"Alpha": "Alpha", "Beta": "Beta", "Gamma": "Gamma"}
                l1_to_f2 = {"Red": "Bar", "Blue": "Dot", "White": "Ring"}
                l2_to_f1 = {"Bar": "Red", "Dot": "Blue", "Ring": "White"}
                l1_to_f3 = {"Red": "Alpha", "Blue": "Beta", "White": "Gamma"}
                l3_to_f1 = {"Alpha": "Red", "Beta": "Blue", "Gamma": "White"}
                l2_to_f3 = {"Bar": "Alpha", "Dot": "Beta", "Ring": "Gamma"}
                l3_to_f2 = {"Alpha": "Bar", "Beta": "Dot", "Gamma": "Ring"}
            
            schemes = {
                "S1": (
                    lambda obj: obj[0] == f1_values.get(recipe_L1),
                    lambda obj: obj[1] == f2_values.get(recipe_L2),
                    lambda obj: obj[2] == f3_values.get(recipe_L3),
                ),
                "S2": (
                    lambda obj: obj[1] == l1_to_f2.get(recipe_L1),
                    lambda obj: obj[0] == l2_to_f1.get(recipe_L2),
                    lambda obj: obj[2] == f3_values.get(recipe_L3),
                ),
                "S3": (
                    lambda obj: obj[2] == l1_to_f3.get(recipe_L1),
                    lambda obj: obj[1] == f2_values.get(recipe_L2),
                    lambda obj: obj[0] == l3_to_f1.get(recipe_L3),
                ),
                "S4": (
                    lambda obj: obj[0] == f1_values.get(recipe_L1),
                    lambda obj: obj[2] == l2_to_f3.get(recipe_L2),
                    lambda obj: obj[1] == l3_to_f2.get(recipe_L3),
                ),
                "S5": (
                    lambda obj: obj[1] == l1_to_f2.get(recipe_L1),
                    lambda obj: obj[2] == l2_to_f3.get(recipe_L2),
                    lambda obj: obj[0] == l3_to_f1.get(recipe_L3),
                ),
                "S6": (
                    lambda obj: obj[2] == l1_to_f3.get(recipe_L1),
                    lambda obj: obj[0] == l2_to_f1.get(recipe_L2),
                    lambda obj: obj[1] == l3_to_f2.get(recipe_L3),
                ),
            }
            return schemes[scheme]
        
        conditions = get_scheme_conditions(self.config.language)
        
        target = set()
        for obj_id, obj_attrs in self.objects.items():
            if all(cond(obj_attrs) for cond in conditions):
                target.add(obj_id)
        
        return target

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        try:
            parts = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            
            for part in parts:
                if "=" in part:
                    k, v = part.split("=", 1)
                    k = k.strip()
                    v = v.strip()
                    if k == "scheme":
                        ans_dict["scheme"] = v
                    elif k == "target":
                        ans_dict["target"] = v
                    else:
                        if "target" in ans_dict:
                            ans_dict["target"] += "," + part
            
            if "scheme" not in ans_dict or "target" not in ans_dict:
                return False
            
            if ans_dict["scheme"] != self.true_scheme:
                return False
            
            target_str = ans_dict["target"]
            model_target = set(int(x.strip()) for x in target_str.split(",") if x.strip().isdigit())
            
            return model_target == self.target_set
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        if "query" not in parsed_info:
            if self.config.language == "zh":
                return "错误：未识别到有效查询标签。"
            else:
                return "Error: No valid query tag found."
        
        self.query_count += 1
        
        try:
            query_str = parsed_info["query"].strip()
            query_ids = set(int(x.strip()) for x in query_str.split(",") if x.strip())
            
            if self.query_count == 1:
                full_set = set(range(1, 16))
                if query_ids == full_set:
                    self.first_query_valid = True
                else:
                    self.state.set_state("failed", "first query must be full set")
                    if self.config.language == "zh":
                        return "错误：第1次查询必须为全体{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}。"
                    else:
                        return "Error: First query must be the full set {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}."
            
            if self.query_count > 8:
                self.state.set_state("failed", "exceeded max query count")
                if self.config.language == "zh":
                    return "错误：查询次数超过上限。"
                else:
                    return "Error: Exceeded maximum query count."
            
            if not all(1 <= qid <= 15 for qid in query_ids):
                if self.config.language == "zh":
                    return "错误：对象编号必须在1到15之间。"
                else:
                    return "Error: Object IDs must be between 1 and 15."
            
            intersection_count = len(query_ids & self.target_set)
            
            return str(intersection_count)
            
        except ValueError:
            if self.config.language == "zh":
                return "错误：查询格式无效，请使用逗号分隔的编号列表。"
            else:
                return "Error: Invalid query format, use comma-separated ID list."

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if "是" in correct:
            return correct.replace("是", "否")
        if "否" in correct:
            return correct.replace("否", "是")
            
        lower_correct = correct.lower()
        if "yes" in lower_correct:
            if correct == "Yes": return "No"
            if correct == "YES": return "NO"
            if correct == "yes": return "no"
            return re.sub(r'Yes', 'No', correct, flags=re.IGNORECASE)
        if "no" in lower_correct:
            if correct == "No": return "Yes"
            if correct == "NO": return "YES"
            if correct == "no": return "yes"
            return re.sub(r'No', 'Yes', correct, flags=re.IGNORECASE)

        return correct + "_WRONG"

    def step(self, response: str):
        try:
            parsed_info = self.parse(response)
            
            if "answer" in parsed_info:
                if self.query_count < 2:
                    self.state.set_state("failed", "need at least 2 queries before answer")
                    if self.config.language == "zh":
                        res = "错误：至少需要完成2次查询后才能提交最终判断。"
                    else:
                        res = "Error: At least 2 queries must be completed before final submission."
                    self.state.add_message("user", res)
                else:
                    is_success = self.evaluate(parsed_info)
                    if is_success:
                        res = "答案正确" if self.config.language == "zh" else "Correct answer."
                        self.state.set_state("success", "success")
                        self.state.add_message("user", res)
                    else:
                        res = "答案错误" if self.config.language == "zh" else "Incorrect answer."
                        self.state.set_state("failed", "incorrect answer")
                        self.state.add_message("user", res)
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))
        
        return self.state

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        all_ids = range(1, 16)
        
        for r in range(1, 16):
            for combo in itertools.combinations(all_ids, r):
                query_str = ",".join(map(str, combo))
                
                intersection_count = sum(1 for qid in combo if qid in self.target_set)
                
                queries.append({
                    "query": query_str,
                    "answer": str(intersection_count)
                })
        
        return queries