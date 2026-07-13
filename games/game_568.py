from .base import Game
import re
import itertools


class ParityOracleGame(Game):

    # ================= 原有基础规则 =================
    game_rule_zh = """\
我们来玩一个"奇偶反馈推理"游戏，规则如下：

游戏设定了一个集合 U = {{A, B, C, D, E, F, G, H}}，每个元素都具有三个二元属性，记为 α、β、γ，每个属性的取值为 0 或 1。具体属性如下：

- A: (0,0,0)
- B: (0,0,1)
- C: (0,1,0)
- D: (0,1,1)
- E: (1,0,0)
- F: (1,0,1)
- G: (1,1,0)
- H: (1,1,1)

我已经秘密选择了一个分类规则，该规则会将集合中的部分元素标记为"正例"。存在五种可能的规则，但我不会告诉你是哪一种。

你的目标是通过查询来推断出：
1. 当前生效的是哪一种规则
2. 根据该规则，集合中哪些元素是正例

## 查询方式

每轮你可以提交集合 U 的任意非空子集 S（可以包含 1 到 8 个元素）。我会告诉你该子集中正例个数的奇偶性（"奇数"或"偶数"），但不会告诉你具体有多少个正例。

你需要尽可能少的查询次数来确定规则和所有正例。

## 查询与提交答案的格式（必须严格遵守）

**查询格式**：使用 XML 标签 <query_subset>，内容为你想查询的元素，用逗号分隔。例如：

<query_subset>A,B,C</query_subset>

或

<query_subset>E,F,G,H</query_subset>

**提交最终答案格式**：使用 XML 标签 <answer>，需要包含规则编号和正例集合，格式如下：

<answer>rule={{rule_id}}, positive={{elements}}</answer>

其中 rule_id 为规则编号（{rule_format}），elements 为你推断的正例元素列表（用逗号分隔，顺序不限）。

例如：

<answer>rule={example_rule}, positive=A,C,E,G</answer>

如果某个规则下没有正例，则写：

<answer>rule={example_rule}, positive=</answer>

注意：答案错误或格式不符将导致游戏失败。
"""

    game_rule_en = """\
Let's play a "Parity Oracle Reasoning" game with the following rules:

There is a set U = {{A, B, C, D, E, F, G, H}}, where each element has three binary attributes α, β, γ, each taking value 0 or 1. The specific attributes are:

- A: (0,0,0)
- B: (0,0,1)
- C: (0,1,0)
- D: (0,1,1)
- E: (1,0,0)
- F: (1,0,1)
- G: (1,1,0)
- H: (1,1,1)

I have secretly selected a classification rule that marks certain elements in the set as "positive examples". There are five possible rules, but I won't tell you which one is in effect.

Your goal is to infer through queries:
1. Which rule is currently in effect
2. According to that rule, which elements in the set are positive examples

## Query Method

Each round, you can submit any non-empty subset S of U (containing 1 to 8 elements). I will tell you the parity of the number of positive examples in that subset ("odd" or "even"), but not the exact count.

You should determine the rule and all positive examples with as few queries as possible.

## Query and Answer Format (must be strictly followed)

**Query Format**: Use XML tag <query_subset>, with content being the elements you want to query, separated by commas. For example:

<query_subset>A,B,C</query_subset>

or

<query_subset>E,F,G,H</query_subset>

**Final Answer Format**: Use XML tag <answer>, including the rule number and positive example set, formatted as:

<answer>rule={{rule_id}}, positive={{elements}}</answer>

where rule_id is the rule number ({rule_format}), and elements is the list of positive elements you inferred (comma-separated, order doesn't matter).

For example:

<answer>rule={example_rule}, positive=A,C,E,G</answer>

If there are no positive examples under a rule, write:

<answer>rule={example_rule}, positive=</answer>

Note: Incorrect answer or invalid format will result in game failure.
"""

    # ================= 场景 1：交通 =================
    contextualized_rule_zh_1 = """\
[交通场景]
我们正在进行一场"城市交通路网重点排查"任务，规则如下：

城市管辖着一个核心路口集合 U = {{A, B, C, D, E, F, G, H}}，每个路口具有三个二元属性，记为 α（是否为主干道：1是/0否）、β（是否有监控盲区：1是/0否）、γ（是否处于拥堵易发区：1是/0否）。具体属性如下：

- A: (0,0,0)
- B: (0,0,1)
- C: (0,1,0)
- D: (0,1,1)
- E: (1,0,0)
- F: (1,0,1)
- G: (1,1,0)
- H: (1,1,1)

指挥中心秘密下达了一项筛查指令，该指令会将部分路口标记为"重点巡逻对象"（正例）。存在五种可能的筛查规则，但我不会直接公开。

你的目标是通过调度系统查询来推断出：
1. 当前生效的是哪一种排查规则
2. 根据该规则，集合中哪些路口是重点巡逻对象

## 查询方式

每轮你可以提交路口集合 U 的任意非空子集 S（包含 1 到 8 个路口）。出于系统安全脱敏限制，调度系统只会告诉你该子集中重点巡逻路口数量的奇偶性（"奇数"或"偶数"），但不会给出具体数量。

你需要尽可能少的查询次数来确定规则和所有重点路口。

## 查询与提交答案的格式（必须严格遵守）

**查询格式**：使用 XML 标签 <query_subset>，内容为你想查询的元素，用逗号分隔。例如：

<query_subset>A,B,C</query_subset>

或

<query_subset>E,F,G,H</query_subset>

**提交最终答案格式**：使用 XML 标签 <answer>，需要包含规则编号和正例集合，格式如下：

<answer>rule={{rule_id}}, positive={{elements}}</answer>

其中 rule_id 为规则编号（{rule_format}），elements 为你推断的正例元素列表（用逗号分隔，顺序不限）。

例如：

<answer>rule={example_rule}, positive=A,C,E,G</answer>

如果某个规则下没有正例，则写：

<answer>rule={example_rule}, positive=</answer>

注意：答案错误或格式不符将导致任务失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's engage in an "Urban Traffic Network Key Node Inspection" task with the following rules:

The city manages a set of core intersections U = {{A, B, C, D, E, F, G, H}}. Each intersection has three binary attributes α (main road: 1-yes/0-no), β (surveillance blind spot: 1-yes/0-no), γ (congestion prone: 1-yes/0-no). The specific attributes are:

- A: (0,0,0)
- B: (0,0,1)
- C: (0,1,0)
- D: (0,1,1)
- E: (1,0,0)
- F: (1,0,1)
- G: (1,1,0)
- H: (1,1,1)

The command center has secretly issued a screening directive that marks certain intersections as "priority patrol targets" (positive examples). There are five possible directives, but I won't explicitly reveal which one is active.

Your goal is to infer through the dispatch system queries:
1. Which directive rule is currently in effect
2. According to that rule, which intersections are priority patrol targets

## Query Method

Each round, you can submit any non-empty subset S of U (containing 1 to 8 intersections). Due to system permission and desensitization restrictions, the dispatch system will only tell you the parity of the number of priority patrol intersections in that subset ("odd" or "even"), but not the exact count.

You should determine the rule and all priority intersections with as few queries as possible.

## Query and Answer Format (must be strictly followed)

**Query Format**: Use XML tag <query_subset>, with content being the elements you want to query, separated by commas. For example:

<query_subset>A,B,C</query_subset>

or

<query_subset>E,F,G,H</query_subset>

**Final Answer Format**: Use XML tag <answer>, including the rule number and positive example set, formatted as:

<answer>rule={{rule_id}}, positive={{elements}}</answer>

where rule_id is the rule number ({rule_format}), and elements is the list of positive elements you inferred (comma-separated, order doesn't matter).

For example:

<answer>rule={example_rule}, positive=A,C,E,G</answer>

If there are no positive examples under a rule, write:

<answer>rule={example_rule}, positive=</answer>

Note: Incorrect answer or invalid format will result in task failure.
"""

    # ================= 场景 2：医疗 =================
    contextualized_rule_zh_2 = """\
[医疗场景]
我们正在进行一项"临床样本靶向药有效性盲测"，规则如下：

实验室准备了一个样本库 U = {{A, B, C, D, E, F, G, H}}，代表 8 批患者基因样本。每批样本具有三个二元属性，记为 α（存在基因突变X：1是/0否）、β（伴随高血压史：1是/0否）、γ（存在家族遗传史：1是/0否）。具体属性如下：

- A: (0,0,0)
- B: (0,0,1)
- C: (0,1,0)
- D: (0,1,1)
- E: (1,0,0)
- F: (1,0,1)
- G: (1,1,0)
- H: (1,1,1)

研究团队秘密确定了一项生化作用机制，该机制会将部分样本标记为"药物有效样本"（正例）。存在五种可能的机制规则，但暂未公开。

你的目标是通过盲测查询推断出：
1. 当前生效的是哪一种机制规则
2. 根据该规则，样本库中哪些样本是有效的

## 查询方式

每轮你可以提交样本库 U 的任意非空子集 S。为了保护患者隐私和控制测试成本，盲测设备只会返回该子集中有效样本数量的奇偶性（"奇数"或"偶数"），不提供具体数值。

你需要尽可能少的查询次数来确定规则和所有有效样本。

## 查询与提交答案的格式（必须严格遵守）

**查询格式**：使用 XML 标签 <query_subset>，内容为你想查询的元素，用逗号分隔。例如：

<query_subset>A,B,C</query_subset>

或

<query_subset>E,F,G,H</query_subset>

**提交最终答案格式**：使用 XML 标签 <answer>，需要包含规则编号和正例集合，格式如下：

<answer>rule={{rule_id}}, positive={{elements}}</answer>

其中 rule_id 为规则编号（{rule_format}），elements 为你推断的正例元素列表（用逗号分隔，顺序不限）。

例如：

<answer>rule={example_rule}, positive=A,C,E,G</answer>

如果某个规则下没有正例，则写：

<answer>rule={example_rule}, positive=</answer>

注意：答案错误或格式不符将导致测试失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
We are conducting a "Clinical Sample Targeted Drug Efficacy Blind Test". The rules are as follows:

The laboratory has prepared a sample library U = {{A, B, C, D, E, F, G, H}}, representing 8 batches of patient genetic samples. Each batch has three binary attributes α (gene mutation X present: 1-yes/0-no), β (history of hypertension: 1-yes/0-no), γ (family genetic history: 1-yes/0-no). The specific attributes are:

- A: (0,0,0)
- B: (0,0,1)
- C: (0,1,0)
- D: (0,1,1)
- E: (1,0,0)
- F: (1,0,1)
- G: (1,1,0)
- H: (1,1,1)

The research team has secretly identified a biochemical mechanism that marks certain samples as "drug-responsive samples" (positive examples). There are five possible mechanism rules, but they are not disclosed.

Your goal is to infer through blind test queries:
1. Which mechanism rule is currently in effect
2. According to that rule, which samples are drug-responsive

## Query Method

Each round, you can submit any non-empty subset S of U. To protect data privacy and control testing costs, the blind test equipment will only return the parity of the number of responsive samples in that subset ("odd" or "even"), without providing the exact count.

You should determine the rule and all responsive samples with as few queries as possible.

## Query and Answer Format (must be strictly followed)

**Query Format**: Use XML tag <query_subset>, with content being the elements you want to query, separated by commas. For example:

<query_subset>A,B,C</query_subset>

or

<query_subset>E,F,G,H</query_subset>

**Final Answer Format**: Use XML tag <answer>, including the rule number and positive example set, formatted as:

<answer>rule={{rule_id}}, positive={{elements}}</answer>

where rule_id is the rule number ({rule_format}), and elements is the list of positive elements you inferred (comma-separated, order doesn't matter).

For example:

<answer>rule={example_rule}, positive=A,C,E,G</answer>

If there are no positive examples under a rule, write:

<answer>rule={example_rule}, positive=</answer>

Note: Incorrect answer or invalid format will result in test failure.
"""

    # ================= 场景 3：教育 =================
    contextualized_rule_zh_3 = """\
[教育场景]
我们正在执行一项"专项拔尖人才培养计划遴选"任务，规则如下：

教务系统导出了一个候选学生画像集合 U = {{A, B, C, D, E, F, G, H}}，每个画像具有三个二元指标，记为 α（完成高阶前置课：1是/0否）、β（有省级竞赛奖项：1是/0否）、γ（绩点排名前10%：1是/0否）。具体属性如下：

- A: (0,0,0)
- B: (0,0,1)
- C: (0,1,0)
- D: (0,1,1)
- E: (1,0,0)
- F: (1,0,1)
- G: (1,1,0)
- H: (1,1,1)

评委会秘密敲定了一套选拔标准，该标准会将部分画像标记为"入选培养计划"（正例）。存在五种可能的标准规则，但处于保密阶段。

你的目标是通过系统核查推断出：
1. 当前生效的是哪一种选拔规则
2. 根据该规则，集合中哪些学生画像成功入选

## 查询方式

每轮你可以向教务系统提交候选集合 U 的任意非空子集 S。系统出于公平保护机制和防泄密策略，只会返回该子集中入选人数的奇偶性（"奇数"或"偶数"）。

你需要尽可能少的查询次数来确定规则和所有入选画像。

## 查询与提交答案的格式（必须严格遵守）

**查询格式**：使用 XML 标签 <query_subset>，内容为你想查询的元素，用逗号分隔。例如：

<query_subset>A,B,C</query_subset>

或

<query_subset>E,F,G,H</query_subset>

**提交最终答案格式**：使用 XML 标签 <answer>，需要包含规则编号和正例集合，格式如下：

<answer>rule={{rule_id}}, positive={{elements}}</answer>

其中 rule_id 为规则编号（{rule_format}），elements 为你推断的正例元素列表（用逗号分隔，顺序不限）。

例如：

<answer>rule={example_rule}, positive=A,C,E,G</answer>

如果某个规则下没有正例，则写：

<answer>rule={example_rule}, positive=</answer>

注意：答案错误或格式不符将导致遴选核查失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
We are executing a "Special Top Talent Nurturing Program Selection" task. The rules are as follows:

The academic system has exported a candidate student profile set U = {{A, B, C, D, E, F, G, H}}. Each profile has three binary indicators α (completed advanced prerequisite course: 1-yes/0-no), β (has provincial competition award: 1-yes/0-no), γ (GPA in top 10%: 1-yes/0-no). The specific attributes are:

- A: (0,0,0)
- B: (0,0,1)
- C: (0,1,0)
- D: (0,1,1)
- E: (1,0,0)
- F: (1,0,1)
- G: (1,1,0)
- H: (1,1,1)

The committee has secretly finalized a selection criterion that marks certain profiles as "selected for the nurturing program" (positive examples). There are five possible criteria rules, but they remain confidential.

Your goal is to infer through system verification:
1. Which selection rule is currently in effect
2. According to that rule, which student profiles are successfully selected

## Query Method

Each round, you can submit any non-empty subset S of candidate set U to the academic system. For fairness protection and confidentiality, the system will only return the parity of the number of selected students in that subset ("odd" or "even").

You should determine the rule and all selected profiles with as few queries as possible.

## Query and Answer Format (must be strictly followed)

**Query Format**: Use XML tag <query_subset>, with content being the elements you want to query, separated by commas. For example:

<query_subset>A,B,C</query_subset>

or

<query_subset>E,F,G,H</query_subset>

**Final Answer Format**: Use XML tag <answer>, including the rule number and positive example set, formatted as:

<answer>rule={{rule_id}}, positive={{elements}}</answer>

where rule_id is the rule number ({rule_format}), and elements is the list of positive elements you inferred (comma-separated, order doesn't matter).

For example:

<answer>rule={example_rule}, positive=A,C,E,G</answer>

If there are no positive examples under a rule, write:

<answer>rule={example_rule}, positive=</answer>

Note: Incorrect answer or invalid format will result in verification failure.
"""

    # ================= 场景 4：工业 =================
    contextualized_rule_zh_4 = """\
[工业场景]
我们正在进行一次"工业零件批量缺陷无损探伤"，规则如下：

车间生产了一个零件批次集合 U = {{A, B, C, D, E, F, G, H}}，每个批次具有三个二元制造属性，记为 α（使用新型合金：1是/0否）、β（经过深度热处理：1是/0否）、γ（表面抛光度达标：1是/0否）。具体属性如下：

- A: (0,0,0)
- B: (0,0,1)
- C: (0,1,0)
- D: (0,1,1)
- E: (1,0,0)
- F: (1,0,1)
- G: (1,1,0)
- H: (1,1,1)

质检部基于某种物理应力模型，将部分批次标记为"存在疲劳断裂风险"（正例）。存在五种可能的风险判定规则，你需要反推出来。

你的目标是通过探伤仪查询推断出：
1. 当前生效的是哪一种风险判定规则
2. 根据该规则，集合中哪些批次存在风险

## 查询方式

每轮你可以将集合 U 的任意非空子集 S 放入黑盒探伤仪中。探伤仪只会通过指示灯告诉你该子集中风险批次总数的奇偶性（"奇数"或"偶数"）。

你需要尽可能少的查询次数来确定规则和所有风险批次。

## 查询与提交答案的格式（必须严格遵守）

**查询格式**：使用 XML 标签 <query_subset>，内容为你想查询的元素，用逗号分隔。例如：

<query_subset>A,B,C</query_subset>

或

<query_subset>E,F,G,H</query_subset>

**提交最终答案格式**：使用 XML 标签 <answer>，需要包含规则编号和正例集合，格式如下：

<answer>rule={{rule_id}}, positive={{elements}}</answer>

其中 rule_id 为规则编号（{rule_format}），elements 为你推断的正例元素列表（用逗号分隔，顺序不限）。

例如：

<answer>rule={example_rule}, positive=A,C,E,G</answer>

如果某个规则下没有正例，则写：

<answer>rule={example_rule}, positive=</answer>

注意：答案错误或格式不符将导致探伤作业失败。
"""

    contextualized_rule_en_4 = """\
[Industry Scenario]
We are conducting an "Industrial Part Batch Defect Non-destructive Testing" task. The rules are as follows:

The workshop produced a part batch set U = {{A, B, C, D, E, F, G, H}}. Each batch has three binary manufacturing attributes α (uses novel alloy: 1-yes/0-no), β (underwent deep heat treatment: 1-yes/0-no), γ (surface polish meets standard: 1-yes/0-no). The specific attributes are:

- A: (0,0,0)
- B: (0,0,1)
- C: (0,1,0)
- D: (0,1,1)
- E: (1,0,0)
- F: (1,0,1)
- G: (1,1,0)
- H: (1,1,1)

The quality control department, based on a physical stress model, marks certain batches as "having fatigue fracture risk" (positive examples). There are five possible risk determination rules, which you need to reverse-engineer.

Your goal is to infer through flaw detector queries:
1. Which risk determination rule is currently in effect
2. According to that rule, which batches are at risk

## Query Method

Each round, you can place any non-empty subset S of U into the black-box flaw detector. The detector will only indicate via a light the parity of the total number of at-risk batches in that subset ("odd" or "even").

You should determine the rule and all at-risk batches with as few queries as possible.

## Query and Answer Format (must be strictly followed)

**Query Format**: Use XML tag <query_subset>, with content being the elements you want to query, separated by commas. For example:

<query_subset>A,B,C</query_subset>

or

<query_subset>E,F,G,H</query_subset>

**Final Answer Format**: Use XML tag <answer>, including the rule number and positive example set, formatted as:

<answer>rule={{rule_id}}, positive={{elements}}</answer>

where rule_id is the rule number ({rule_format}), and elements is the list of positive elements you inferred (comma-separated, order doesn't matter).

For example:

<answer>rule={example_rule}, positive=A,C,E,G</answer>

If there are no positive examples under a rule, write:

<answer>rule={example_rule}, positive=</answer>

Note: Incorrect answer or invalid format will result in testing failure.
"""

    # ================= 场景 5：法律 =================
    contextualized_rule_zh_5 = """\
[法律场景]
我们正在进行一项"企业并购案卷宗合规审查"，规则如下：

律所数据库中有一个合同卷宗集合 U = {{A, B, C, D, E, F, G, H}}，每份卷宗具有三个二元法律属性，记为 α（涉及跨境资产：1是/0否）、β（包含对赌条款：1是/0否）、γ（存在知识产权纠纷：1是/0否）。具体属性如下：

- A: (0,0,0)
- B: (0,0,1)
- C: (0,1,0)
- D: (0,1,1)
- E: (1,0,0)
- F: (1,0,1)
- G: (1,1,0)
- H: (1,1,1)

高级合伙人秘密下达了审查指导意见，将部分卷宗标记为"需召开听证会的重点卷宗"（正例）。存在五种可能的指导规则，你需要进行溯源。

你的目标是通过内网权限系统推断出：
1. 当前生效的是哪一种审查指导规则
2. 根据该规则，集合中哪些卷宗是重点卷宗

## 查询方式

每轮你可以向系统提交卷宗集合 U 的任意非空子集 S。受限于保密协议和权限隔离壁垒，系统仅会反馈该子集中重点卷宗数量的奇偶性（"奇数"或"偶数"）。

你需要尽可能少的查询次数来确定规则和所有重点卷宗。

## 查询与提交答案的格式（必须严格遵守）

**查询格式**：使用 XML 标签 <query_subset>，内容为你想查询的元素，用逗号分隔。例如：

<query_subset>A,B,C</query_subset>

或

<query_subset>E,F,G,H</query_subset>

**提交最终答案格式**：使用 XML 标签 <answer>，需要包含规则编号和正例集合，格式如下：

<answer>rule={{rule_id}}, positive={{elements}}</answer>

其中 rule_id 为规则编号（{rule_format}），elements 为你推断的正例元素列表（用逗号分隔，顺序不限）。

例如：

<answer>rule={example_rule}, positive=A,C,E,G</answer>

如果某个规则下没有正例，则写：

<answer>rule={example_rule}, positive=</answer>

注意：答案错误或格式不符将导致合规审查程序中止。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
We are conducting a "Corporate M&A Case File Compliance Review". The rules are as follows:

The law firm's database contains a contract file set U = {{A, B, C, D, E, F, G, H}}. Each file has three binary legal attributes α (involves cross-border assets: 1-yes/0-no), β (contains valuation adjustment mechanism: 1-yes/0-no), γ (has IP dispute: 1-yes/0-no). The specific attributes are:

- A: (0,0,0)
- B: (0,0,1)
- C: (0,1,0)
- D: (0,1,1)
- E: (1,0,0)
- F: (1,0,1)
- G: (1,1,0)
- H: (1,1,1)

The senior partner has secretly issued a review guideline that marks certain files as "priority files requiring a hearing" (positive examples). There are five possible guideline rules, and you need to trace them back.

Your goal is to infer through the intranet permission system:
1. Which review guideline rule is currently in effect
2. According to that rule, which files are priority files

## Query Method

Each round, you can submit any non-empty subset S of file set U to the system. Restricted by non-disclosure agreements and permission isolation barriers, the system will only feedback the parity of the number of priority files in that subset ("odd" or "even").

You should determine the rule and all priority files with as few queries as possible.

## Query and Answer Format (must be strictly followed)

**Query Format**: Use XML tag <query_subset>, with content being the elements you want to query, separated by commas. For example:

<query_subset>A,B,C</query_subset>

or

<query_subset>E,F,G,H</query_subset>

**Final Answer Format**: Use XML tag <answer>, including the rule number and positive example set, formatted as:

<answer>rule={{rule_id}}, positive={{elements}}</answer>

where rule_id is the rule number ({rule_format}), and elements is the list of positive elements you inferred (comma-separated, order doesn't matter).

For example:

<answer>rule={example_rule}, positive=A,C,E,G</answer>

If there are no positive examples under a rule, write:

<answer>rule={example_rule}, positive=</answer>

Note: Incorrect answer or invalid format will result in the suspension of the review process.
"""

    tags = ["answer", "query_subset"]
    reasoning_type = "溯因推理"
    data_structure = "集合"

    # 元素属性定义（固定）
    ELEMENTS = {
        'A': (0, 0, 0),
        'B': (0, 0, 1),
        'C': (0, 1, 0),
        'D': (0, 1, 1),
        'E': (1, 0, 0),
        'F': (1, 0, 1),
        'G': (1, 1, 0),
        'H': (1, 1, 1),
    }

    # 规则定义函数
    @staticmethod
    def rule_I(attrs):
        """规则 I：正例当且仅当 α=1"""
        return attrs[0] == 1

    @staticmethod
    def rule_II(attrs):
        """规则 II：正例当且仅当 β=1"""
        return attrs[1] == 1

    @staticmethod
    def rule_III(attrs):
        """规则 III：正例当且仅当 γ=1"""
        return attrs[2] == 1

    @staticmethod
    def rule_IV(attrs):
        """规则 IV：正例当且仅当 α+β+γ=2"""
        return sum(attrs) == 2

    @staticmethod
    def rule_V(attrs):
        """规则 V：正例当且仅当 α+β+γ 为奇数（1 或 3）"""
        return sum(attrs) % 2 == 1

    RULES = {
        'I': rule_I.__func__,
        'II': rule_II.__func__,
        'III': rule_III.__func__,
        'IV': rule_IV.__func__,
        'V': rule_V.__func__,
    }

    # 难度配置
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"rule": "I"},
            2: {"rule": "II"},
            3: {"rule": "III"},
            4: {"rule": "IV"},
            5: {"rule": "V"},
        },
        "en": {
            1: {"rule": "I"},
            2: {"rule": "II"},
            3: {"rule": "III"},
            4: {"rule": "IV"},
            5: {"rule": "V"},
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：根据难度选择规则，计算正例集合"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.rule_id = cfg["rule"]
        self.rule_func = self.RULES[self.rule_id]

        # 计算该规则下的所有正例
        self.positive_set = set()
        for elem, attrs in self.ELEMENTS.items():
            if self.rule_func(attrs):
                self.positive_set.add(elem)

        # 为游戏规则文本准备格式化信息
        self._game_info["rule_format"] = "I/II/III/IV/V"
        self._game_info["example_rule"] = "I"

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案：rule=X, positive=A,B,C
        kv_pairs = [x.strip() for x in raw_ans.split(",", 1)]
        ans_dict = {}
        
        for kv in kv_pairs:
            if "=" not in kv:
                continue
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "rule" not in ans_dict or "positive" not in ans_dict:
            return False
        
        # 1. 检查规则是否正确
        if ans_dict["rule"] != self.rule_id:
            return False
        
        # 2. 检查正例集合是否正确
        try:
            submitted_positive = ans_dict["positive"]
            if submitted_positive == "":
                model_positive_set = set()
            else:
                model_positive_set = set(x.strip().upper() for x in submitted_positive.split(",") if x.strip())
        except:
            return False
        
        return model_positive_set == self.positive_set

    def _cf_core_produce(self, parsed_info):
        """核心处理查询并返回奇偶性读数逻辑"""
        if "query_subset" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        raw_query = parsed_info["query_subset"].strip()
        
        if raw_query == "":
            raise ValueError("Query subset cannot be empty.")
        
        try:
            queried_elements = set(x.strip().upper() for x in raw_query.split(",") if x.strip())
        except:
            raise ValueError("Invalid query format.")
        
        if not queried_elements:
            raise ValueError("Query subset cannot be empty.")
        
        for elem in queried_elements:
            if elem not in self.ELEMENTS:
                raise ValueError(f"Element {elem} is not in the set.")
        
        positive_count = sum(1 for elem in queried_elements if elem in self.positive_set)
        
        if positive_count % 2 == 1:
            return "奇数" if self.config.language == "zh" else "odd"
        else:
            return "偶数" if self.config.language == "zh" else "even"

    def _cf_make_wrong(self, correct: str) -> str:
        # 处理奇偶性的反事实
        if correct == "奇数":
            return "偶数"
        if correct == "偶数":
            return "奇数"
        if correct.lower() == "odd":
            return "Even" if correct[0].isupper() else "even"
        if correct.lower() == "even":
            return "Odd" if correct[0].isupper() else "odd"
        
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        if correct.lower() == "yes":
            return "No" if correct[0].isupper() else "no"
        if correct.lower() == "no":
            return "Yes" if correct[0].isupper() else "yes"
            
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串，与游戏中 parsed_info["query"] 的值格式一致
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        results = []
        # 获取所有元素标签并排序，保证生成顺序确定
        elements = sorted(list(self.ELEMENTS.keys()))
        
        # 遍历所有非空子集 (大小 1 到 8)
        for r in range(1, len(elements) + 1):
            for combo in itertools.combinations(elements, r):
                # 构造查询字符串
                query_str = ",".join(combo)
                
                # 计算子集中正例的个数
                positive_count = 0
                for elem in combo:
                    if elem in self.positive_set:
                        positive_count += 1
                
                # 生成答案
                if positive_count % 2 == 1:
                    ans = "奇数" if self.config.language == "zh" else "odd"
                else:
                    ans = "偶数" if self.config.language == "zh" else "even"
                
                results.append({
                    "query": f"<query_subset>{query_str}</query_subset>",
                    "answer": ans
                })
        
        return results