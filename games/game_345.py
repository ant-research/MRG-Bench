# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 集合：存在一个由N个物体组成的集合，注意他们不存在位置、前后和大小关系。
# 知识点:   条件比例：满足某条件的元素占集合总数的比例
# ============================================================

from .base import Game
import re
from fractions import Fraction


class AttributeSetInferenceGame(Game):

    game_rule_zh = """\
我们来玩一个"属性集合推断"的游戏，规则如下：

游戏设定了一个有限集合 S，规模为 {n}（共 {n} 个元素）。集合中每个元素可以携带三个二值属性中的任意子集：A、B、C（可能不携带任何属性，也可能同时携带全部三个属性）。属性分配在游戏开始时已固定，不会改变。

你的目标是：推断出集合中"恰好具有两个属性"的元素数量 X（0 小于等于 X 小于等于 {n}），以及其占比 X/{n}（用最简分数表示）。

## 允许的查询类型

你只能进行"并集覆盖查询"，即查询"至少具有某些属性之一"的元素的数量或比例。

允许查询的七种属性并集为：
1. A：至少具有属性 A
2. B：至少具有属性 B
3. C：至少具有属性 C
4. A 或 B：至少具有属性 A 或属性 B（或两者都有）
5. B 或 C：至少具有属性 B 或属性 C（或两者都有）
6. C 或 A：至少具有属性 C 或属性 A（或两者都有）
7. A 或 B 或 C：至少具有属性 A、B、C 中的任意一个（或多个）

对于每次查询，你需要声明请求返回的信息类型：
- 数量（count）：返回满足条件的元素个数（整数）
- 比例（ratio）：返回满足条件的元素占比（最简分数形式）
- 两者（both）：同时返回数量和比例

## 禁止的查询

以下查询类型是不允许的，若尝试将导致游戏失败：
- 任何交集查询（例如"同时具有 A 和 B"）
- 任何"恰好 k 个""至少 k 个""至多 k 个"属性的查询
- 空集或不在上述七种之列的集合

## 查询格式（必须严格遵守）

每次只能提交一个查询，使用以下 XML 格式：

- 查询单个属性 A 的数量：
<query>A, count</query>

- 查询属性 B 或 C 的比例：
<query>B or C, ratio</query>

- 查询属性 A 或 B 或 C 的数量和比例：
<query>A or B or C, both</query>

注意：属性名称大小写敏感，连接词使用"or"，查询类型为 count、ratio 或 both。

## 提交答案格式

当你收集足够信息后，请提交最终答案，格式如下：

<answer>count=X, ratio=X/{n}</answer>

其中 X 是恰好具有两个属性的元素数量，X/{n} 是最简分数形式的比例。

请尽可能少地进行查询，高效推断出答案。
"""

    game_rule_en = """\
Let's play an "Attribute Set Inference" game. Here are the rules:

There is a finite set S with a size of {n} (containing {n} elements). Each element in the set may carry any subset of three binary attributes: A, B, C (it may carry no attributes, or all three attributes). The attribute assignments are fixed at the start and will not change.

Your goal is: to infer the count X of elements that have "exactly two attributes" (0 less than or equal to X less than or equal to {n}), and their proportion X/{n} (expressed as a simplified fraction).

## Allowed Query Types

You can only perform "union coverage queries", i.e., querying the count or proportion of elements that have "at least one of certain attributes".

The seven allowed attribute unions are:
1. A: at least has attribute A
2. B: at least has attribute B
3. C: at least has attribute C
4. A or B: at least has attribute A or attribute B (or both)
5. B or C: at least has attribute B or attribute C (or both)
6. C or A: at least has attribute C or attribute A (or both)
7. A or B or C: at least has any one (or more) of attributes A, B, C

For each query, you need to specify the type of information to return:
- count: returns the number of elements satisfying the condition (integer)
- ratio: returns the proportion of elements satisfying the condition (simplified fraction)
- both: returns both count and ratio

## Forbidden Queries

The following query types are not allowed and will cause game failure if attempted:
- Any intersection queries (e.g., "has both A and B")
- Any queries about "exactly k", "at least k", or "at most k" attributes
- Empty set or sets not among the seven types above

## Query Format (must be strictly followed)

Only one query can be submitted at a time, using the following XML format:

- Query the count of single attribute A:
<query>A, count</query>

- Query the ratio of attribute B or C:
<query>B or C, ratio</query>

- Query both count and ratio of attribute A or B or C:
<query>A or B or C, both</query>

Note: Attribute names are case-sensitive, use "or" as connector, query type is count, ratio, or both.

## Answer Submission Format

When you have collected sufficient information, submit your final answer in the following format:

<answer>count=X, ratio=X/{n}</answer>

Where X is the count of elements with exactly two attributes, and X/{n} is the proportion in simplified fraction form.

Please use as few queries as possible to efficiently infer the answer.
"""

    contextualized_rule_zh_1 = """\
智能交通系统正在进行路口监控探头的能力评估。

当前区域共有 {n} 个监控探头（集合规模为 {n}）。每个探头可以搭载三种违章抓拍功能（属性）中的任意组合：A（违停抓拍）、B（超速抓拍）、C（闯红灯抓拍）。有的探头可能没有任何抓拍功能，有的可能同时搭载了三项。探头的硬件配置在评估开始时已固定，不会改变。

你的目标是：推断出"恰好搭载了两项抓拍功能"的探头数量 X（0 小于等于 X 小于等于 {n}），以及其占探头总数的比例 X/{n}（用最简分数表示）。

## 允许的查询类型

你只能向交通数据库发起"并集覆盖查询"，即查询"至少搭载了某些抓拍功能之一"的探头的数量或比例。

允许查询的七种功能并集为：
1. A：至少具备 A（违停抓拍）
2. B：至少具备 B（超速抓拍）
3. C：至少具备 C（闯红灯抓拍）
4. A 或 B：至少具备 A 或 B（或两者都有）
5. B 或 C：至少具备 B 或 C（或两者都有）
6. C 或 A：至少具备 C 或 A（或两者都有）
7. A 或 B 或 C：至少具备 A、B、C 中的任意一项（或多项）

对于每次查询，你需要声明请求返回的系统数据类型：
- 数量（count）：返回满足条件的探头个数（整数）
- 比例（ratio）：返回满足条件的探头占比（最简分数形式）
- 两者（both）：同时返回数量和比例

## 禁止的查询

以下查询类型是不允许的，若尝试将导致系统拒绝访问（评估失败）：
- 任何交集查询（例如"同时具备 A 和 B"）
- 任何"恰好 k 项""至少 k 项""至多 k 项"功能的精确条件查询
- 空集或不在上述七种之列的组合

## 查询格式（必须严格遵守）

每次只能提交一个查询，使用以下 XML 格式：

- 查询单个功能 A 的数量：
<query>A, count</query>

- 查询功能 B 或 C 的比例：
<query>B or C, ratio</query>

- 查询功能 A 或 B 或 C 的数量和比例：
<query>A or B or C, both</query>

注意：属性名称 A、B、C 大小写敏感，连接词使用"or"，查询类型为 count、ratio 或 both。

## 提交答案格式

当你收集足够信息后，请提交最终评估报告，格式如下：

<answer>count=X, ratio=X/{n}</answer>

其中 X 是恰好具备两项抓拍功能的探头数量，X/{n} 是最简分数形式的比例。

请尽可能少地进行查询，高效推断出评估答案。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
An intelligent transportation system is evaluating the capabilities of intersection surveillance cameras.

There are currently {n} surveillance cameras in the area (a set size of {n}). Each camera may be equipped with any combination of three violation detection functions (attributes): A (Illegal Parking Detection), B (Speeding Detection), and C (Red Light Running Detection). Some cameras may have no detection functions, while others may have all three. The hardware configurations of the cameras are fixed at the start of the evaluation and will not change.

Your goal is: to infer the count X of cameras that are equipped with "exactly two detection functions" (0 less than or equal to X less than or equal to {n}), and their proportion X/{n} (expressed as a simplified fraction).

## Allowed Query Types

You can only perform "union coverage queries" to the traffic database, i.e., querying the count or proportion of cameras that have "at least one of certain detection functions".

The seven allowed function unions are:
1. A: at least has function A
2. B: at least has function B
3. C: at least has function C
4. A or B: at least has function A or B (or both)
5. B or C: at least has function B or C (or both)
6. C or A: at least has function C or A (or both)
7. A or B or C: at least has any one (or more) of functions A, B, C

For each query, you need to specify the type of system data to return:
- count: returns the number of cameras satisfying the condition (integer)
- ratio: returns the proportion of cameras satisfying the condition (simplified fraction)
- both: returns both count and ratio

## Forbidden Queries

The following query types are not allowed and will cause database access denial (evaluation failure) if attempted:
- Any intersection queries (e.g., "equipped with both A and B")
- Any exact condition queries about "exactly k", "at least k", or "at most k" functions
- Empty set or combinations not among the seven types above

## Query Format (must be strictly followed)

Only one query can be submitted at a time, using the following XML format:

- Query the count of single function A:
<query>A, count</query>

- Query the ratio of function B or C:
<query>B or C, ratio</query>

- Query both count and ratio of function A or B or C:
<query>A or B or C, both</query>

Note: Attribute names A, B, C are case-sensitive, use "or" as connector, query type is count, ratio, or both.

## Answer Submission Format

When you have collected sufficient information, submit your final evaluation report in the following format:

<answer>count=X, ratio=X/{n}</answer>

Where X is the count of cameras with exactly two detection functions, and X/{n} is the proportion in simplified fraction form.

Please use as few queries as possible to efficiently infer the evaluation answer.
"""

    contextualized_rule_zh_2 = """\
医学研究团队正在对一组临床试验患者样本进行病史分析。

本次试验共有 {n} 名患者样本（集合规模为 {n}）。每名患者可能伴有三种基础疾病史（属性）中的任意组合：A（高血压病史）、B（糖尿病史）、C（心血管疾病史）。部分患者可能没有任何此类病史，而部分患者可能同时伴有三种病史。患者的病史档案在分析开始时已固定，不会改变。

你的目标是：推断出"恰好伴有两项基础疾病史"的患者数量 X（0 小于等于 X 小于等于 {n}），以及其占样本总数的比例 X/{n}（用最简分数表示）。

## 允许的查询类型

你只能向医疗电子病历系统发起"并集覆盖查询"，即查询"至少伴有某几种病史之一"的患者数量或比例。

允许查询的七种病史并集为：
1. A：至少伴有 A（高血压病史）
2. B：至少伴有 B（糖尿病史）
3. C：至少伴有 C（心血管疾病史）
4. A 或 B：至少伴有 A 或 B（或两者皆有）
5. B 或 C：至少伴有 B 或 C（或两者皆有）
6. C 或 A：至少伴有 C 或 A（或两者皆有）
7. A 或 B 或 C：至少伴有 A、B、C 中的任意一项（或多项）

对于每次查询，你需要声明请求返回的统计数据类型：
- 数量（count）：返回满足条件的患者人数（整数）
- 比例（ratio）：返回满足条件的患者占比（最简分数形式）
- 两者（both）：同时返回数量和比例

## 禁止的查询

以下查询类型是不允许的，若尝试将导致系统报错（分析失败）：
- 任何交集查询（例如"同时伴有 A 和 B"）
- 任何"恰好 k 项""至少 k 项""至多 k 项"病史的精确条件查询
- 空集或不在上述七种之列的组合

## 查询格式（必须严格遵守）

每次只能提交一个查询，使用以下 XML 格式：

- 查询单项病史 A 的数量：
<query>A, count</query>

- 查询病史 B 或 C 的比例：
<query>B or C, ratio</query>

- 查询病史 A 或 B 或 C 的数量和比例：
<query>A or B or C, both</query>

注意：属性名称 A、B、C 大小写敏感，连接词使用"or"，查询类型为 count、ratio 或 both。

## 提交答案格式

当你收集足够信息后，请提交最终分析结论，格式如下：

<answer>count=X, ratio=X/{n}</answer>

其中 X 是恰好伴有两项基础疾病史的患者数量，X/{n} 是最简分数形式的比例。

请尽可能少地进行查询，高效推断出分析答案。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
A medical research team is conducting a medical history analysis on a cohort of clinical trial patients.

There are {n} patient samples in this trial (a set size of {n}). Each patient may have any combination of three underlying medical histories (attributes): A (Hypertension History), B (Diabetes History), and C (Cardiovascular Disease History). Some patients may have no such medical histories, while others may present all three. The patients' medical records are fixed at the start of the analysis and will not change.

Your goal is: to infer the count X of patients who have "exactly two underlying medical histories" (0 less than or equal to X less than or equal to {n}), and their proportion X/{n} (expressed as a simplified fraction).

## Allowed Query Types

You can only perform "union coverage queries" to the electronic medical record system, i.e., querying the count or proportion of patients who have "at least one of certain medical histories".

The seven allowed medical history unions are:
1. A: at least has A (Hypertension History)
2. B: at least has B (Diabetes History)
3. C: at least has C (Cardiovascular Disease History)
4. A or B: at least has A or B (or both)
5. B or C: at least has B or C (or both)
6. C or A: at least has C or A (or both)
7. A or B or C: at least has any one (or more) of histories A, B, C

For each query, you need to specify the type of statistical data to return:
- count: returns the number of patients satisfying the condition (integer)
- ratio: returns the proportion of patients satisfying the condition (simplified fraction)
- both: returns both count and ratio

## Forbidden Queries

The following query types are not allowed and will cause a system error (analysis failure) if attempted:
- Any intersection queries (e.g., "has both A and B")
- Any exact condition queries about "exactly k", "at least k", or "at most k" medical histories
- Empty set or combinations not among the seven types above

## Query Format (must be strictly followed)

Only one query can be submitted at a time, using the following XML format:

- Query the count of a single history A:
<query>A, count</query>

- Query the ratio of history B or C:
<query>B or C, ratio</query>

- Query both count and ratio of history A or B or C:
<query>A or B or C, both</query>

Note: Attribute names A, B, C are case-sensitive, use "or" as connector, query type is count, ratio, or both.

## Answer Submission Format

When you have collected sufficient information, submit your final analysis conclusion in the following format:

<answer>count=X, ratio=X/{n}</answer>

Where X is the count of patients with exactly two underlying medical histories, and X/{n} is the proportion in simplified fraction form.

Please use as few queries as possible to efficiently infer the analysis answer.
"""

    contextualized_rule_zh_3 = """\
高校科研管理处正在对校内各科研实验室的资质特征进行统计盘点。

全校共有 {n} 个受评实验室（集合规模为 {n}）。每个实验室可能具备三种科研资质（属性）中的任意组合：A（国家级基金资助）、B（跨学科研究项目）、C（产学研合作基地）。有的实验室可能正处于起步阶段，不具备任何资质；有的则可能同时囊括这三项。各实验室的资质状态在盘点开始时已锁定，不会发生改变。

你的目标是：推断出"恰好具备两项科研资质"的实验室数量 X（0 小于等于 X 小于等于 {n}），以及其占总数的比例 X/{n}（用最简分数表示）。

## 允许的查询类型

你只能向科研管理系统发起"并集覆盖查询"，即查询"至少具备某几项资质之一"的实验室数量或比例。

允许查询的七种资质并集为：
1. A：至少具备 A（国家级基金资助）
2. B：至少具备 B（跨学科研究项目）
3. C：至少具备 C（产学研合作基地）
4. A 或 B：至少具备 A 或 B（或两者皆有）
5. B 或 C：至少具备 B 或 C（或两者皆有）
6. C 或 A：至少具备 C 或 A（或两者皆有）
7. A 或 B 或 C：至少具备 A、B、C 中的任意一项（或多项）

对于每次查询，你需要声明请求返回的指标类型：
- 数量（count）：返回满足条件的实验室个数（整数）
- 比例（ratio）：返回满足条件的实验室占比（最简分数形式）
- 两者（both）：同时返回数量和比例

## 禁止的查询

以下查询类型是不允许的，若尝试将导致系统拦截（盘点失败）：
- 任何交集查询（例如"同时具备 A 和 B"）
- 任何"恰好 k 项""至少 k 项""至多 k 项"资质的精确条件查询
- 空集或不在上述七种之列的组合

## 查询格式（必须严格遵守）

每次只能提交一个查询，使用以下 XML 格式：

- 查询单项资质 A 的数量：
<query>A, count</query>

- 查询资质 B 或 C 的比例：
<query>B or C, ratio</query>

- 查询资质 A 或 B 或 C 的数量和比例：
<query>A or B or C, both</query>

注意：属性名称 A、B、C 大小写敏感，连接词使用"or"，查询类型为 count、ratio 或 both。

## 提交答案格式

当你收集足够信息后，请提交最终盘点结果，格式如下：

<answer>count=X, ratio=X/{n}</answer>

其中 X 是恰好具备两项科研资质的实验室数量，X/{n} 是最简分数形式的比例。

请尽可能少地进行查询，高效推断出盘点答案。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The university's research management office is taking an inventory of the qualification characteristics of various research laboratories on campus.

There are {n} laboratories under evaluation in total (a set size of {n}). Each laboratory may possess any combination of three research qualifications (attributes): A (National Fund Support), B (Interdisciplinary Project), and C (Industry-Academia Collaboration). Some starting labs may have no qualifications, while others may hold all three simultaneously. The qualification statuses of the laboratories are locked at the start of the inventory and will not change.

Your goal is: to infer the count X of laboratories that possess "exactly two research qualifications" (0 less than or equal to X less than or equal to {n}), and their proportion X/{n} (expressed as a simplified fraction).

## Allowed Query Types

You can only perform "union coverage queries" to the research management system, i.e., querying the count or proportion of laboratories that have "at least one of certain qualifications".

The seven allowed qualification unions are:
1. A: at least has A (National Fund Support)
2. B: at least has B (Interdisciplinary Project)
3. C: at least has C (Industry-Academia Collaboration)
4. A or B: at least has A or B (or both)
5. B or C: at least has B or C (or both)
6. C or A: at least has C or A (or both)
7. A or B or C: at least has any one (or more) of qualifications A, B, C

For each query, you need to specify the type of indicator to return:
- count: returns the number of laboratories satisfying the condition (integer)
- ratio: returns the proportion of laboratories satisfying the condition (simplified fraction)
- both: returns both count and ratio

## Forbidden Queries

The following query types are not allowed and will be intercepted by the system (inventory failure) if attempted:
- Any intersection queries (e.g., "possesses both A and B")
- Any exact condition queries about "exactly k", "at least k", or "at most k" qualifications
- Empty set or combinations not among the seven types above

## Query Format (must be strictly followed)

Only one query can be submitted at a time, using the following XML format:

- Query the count of a single qualification A:
<query>A, count</query>

- Query the ratio of qualification B or C:
<query>B or C, ratio</query>

- Query both count and ratio of qualification A or B or C:
<query>A or B or C, both</query>

Note: Attribute names A, B, C are case-sensitive, use "or" as connector, query type is count, ratio, or both.

## Answer Submission Format

When you have collected sufficient information, submit your final inventory result in the following format:

<answer>count=X, ratio=X/{n}</answer>

Where X is the count of laboratories with exactly two research qualifications, and X/{n} is the proportion in simplified fraction form.

Please use as few queries as possible to efficiently infer the inventory answer.
"""

    contextualized_rule_zh_4 = """\
智能制造工厂的质检中心正在审查批次流水线上的精密加工零件。

当前质检批次包含 {n} 个精密零件（集合规模为 {n}）。每个零件在生产过程中可能经过了三种特殊工艺（属性）中的任意组合：A（表面抛光处理）、B（热处理强化）、C（防锈涂层覆盖）。部分零件可能仅为毛坯，未经过这些特殊处理，而部分零件可能经过了全部三道工艺。各零件的工艺记录在审查开始时已封存，不会改变。

你的目标是：推断出"恰好经过两道特殊工艺处理"的零件数量 X（0 小于等于 X 小于等于 {n}），以及其占批次总数的比例 X/{n}（用最简分数表示）。

## 允许的查询类型

你只能向生产控制系统（MES）发起"并集覆盖查询"，即查询"至少经过某几道特殊工艺之一"的零件数量或比例。

允许查询的七种工艺并集为：
1. A：至少经过 A（表面抛光处理）
2. B：至少经过 B（热处理强化）
3. C：至少经过 C（防锈涂层覆盖）
4. A 或 B：至少经过 A 或 B（或两者皆有）
5. B 或 C：至少经过 B 或 C（或两者皆有）
6. C 或 A：至少经过 C 或 A（或两者皆有）
7. A 或 B 或 C：至少经过 A、B、C 中的任意一道（或多道）

对于每次查询，你需要声明请求返回的质检参数类型：
- 数量（count）：返回满足条件的零件个数（整数）
- 比例（ratio）：返回满足条件的零件占比（最简分数形式）
- 两者（both）：同时返回数量和比例

## 禁止的查询

以下查询类型是不允许的，若尝试将导致 MES 系统阻断（审查失败）：
- 任何交集查询（例如"同时经过 A 和 B"）
- 任何"恰好 k 道""至少 k 道""至多 k 道"工艺的精确条件查询
- 空集或不在上述七种之列的组合

## 查询格式（必须严格遵守）

每次只能提交一个查询，使用以下 XML 格式：

- 查询单一工艺 A 的数量：
<query>A, count</query>

- 查询工艺 B 或 C 的比例：
<query>B or C, ratio</query>

- 查询工艺 A 或 B 或 C 的数量和比例：
<query>A or B or C, both</query>

注意：属性名称 A、B、C 大小写敏感，连接词使用"or"，查询类型为 count、ratio 或 both。

## 提交答案格式

当你收集足够信息后，请提交最终质检报告，格式如下：

<answer>count=X, ratio=X/{n}</answer>

其中 X 是恰好经过两道特殊工艺处理的零件数量，X/{n} 是最简分数形式的比例。

请尽可能少地进行查询，高效推断出质检答案。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
The quality inspection center of a smart manufacturing plant is reviewing precision machined parts from an assembly line batch.

The current inspection batch contains {n} precision parts (a set size of {n}). Each part may have undergone any combination of three special processes (attributes) during production: A (Surface Polishing), B (Heat Treatment), and C (Anti-rust Coating). Some parts may be roughcast without these treatments, while others may have undergone all three processes. The process records for each part are sealed at the start of the review and will not change.

Your goal is: to infer the count X of parts that have undergone "exactly two special processes" (0 less than or equal to X less than or equal to {n}), and their proportion X/{n} (expressed as a simplified fraction).

## Allowed Query Types

You can only perform "union coverage queries" to the Manufacturing Execution System (MES), i.e., querying the count or proportion of parts that have "undergone at least one of certain special processes".

The seven allowed process unions are:
1. A: at least undergone A (Surface Polishing)
2. B: at least undergone B (Heat Treatment)
3. C: at least undergone C (Anti-rust Coating)
4. A or B: at least undergone A or B (or both)
5. B or C: at least undergone B or C (or both)
6. C or A: at least undergone C or A (or both)
7. A or B or C: at least undergone any one (or more) of processes A, B, C

For each query, you need to specify the type of quality inspection parameter to return:
- count: returns the number of parts satisfying the condition (integer)
- ratio: returns the proportion of parts satisfying the condition (simplified fraction)
- both: returns both count and ratio

## Forbidden Queries

The following query types are not allowed and will be blocked by the MES system (review failure) if attempted:
- Any intersection queries (e.g., "undergone both A and B")
- Any exact condition queries about "exactly k", "at least k", or "at most k" processes
- Empty set or combinations not among the seven types above

## Query Format (must be strictly followed)

Only one query can be submitted at a time, using the following XML format:

- Query the count of a single process A:
<query>A, count</query>

- Query the ratio of process B or C:
<query>B or C, ratio</query>

- Query both count and ratio of process A or B or C:
<query>A or B or C, both</query>

Note: Attribute names A, B, C are case-sensitive, use "or" as connector, query type is count, ratio, or both.

## Answer Submission Format

When you have collected sufficient information, submit your final inspection report in the following format:

<answer>count=X, ratio=X/{n}</answer>

Where X is the count of parts that have undergone exactly two special processes, and X/{n} is the proportion in simplified fraction form.

Please use as few queries as possible to efficiently infer the inspection answer.
"""

    contextualized_rule_zh_5 = """\
法院司法数据中心正在对一批处于审理阶段的复杂商业纠纷案件进行卷宗归类。

当前批次共有 {n} 宗案件（集合规模为 {n}）。每宗案件的诉状中可能涉及三种特定法律争议（属性）中的任意组合：A（涉及知识产权争议）、B（涉及跨国贸易条款）、C（涉及垄断经营行为）。有的案件可能仅涉及常规违约，未包含上述争议；有的重大案件则可能同时牵涉这三项争议。案卷的争议定性在归类工作开始时已固化，不会改变。

你的目标是：推断出"恰好具备两项争议特征"的案件数量 X（0 小于等于 X 小于等于 {n}），以及其占案件总数的比例 X/{n}（用最简分数表示）。

## 允许的查询类型

你只能向司法数据系统发起"并集覆盖查询"，即查询"至少涉及某几项法律争议之一"的案件数量或比例。

允许查询的七种争议并集为：
1. A：至少涉及 A（知识产权争议）
2. B：至少涉及 B（跨国贸易条款）
3. C：至少涉及 C（垄断经营行为）
4. A 或 B：至少涉及 A 或 B（或两者皆有）
5. B 或 C：至少涉及 B 或 C（或两者皆有）
6. C 或 A：至少涉及 C 或 A（或两者皆有）
7. A 或 B 或 C：至少涉及 A、B、C 中的任意一项（或多项）

对于每次查询，你需要声明请求返回的数据视图类型：
- 数量（count）：返回满足条件的案件宗数（整数）
- 比例（ratio）：返回满足条件的案件占比（最简分数形式）
- 两者（both）：同时返回数量和比例

## 禁止的查询

以下查询类型是不允许的，若尝试将导致系统驳回请求（归类失败）：
- 任何交集查询（例如"同时涉及 A 和 B"）
- 任何"恰好牵涉 k 项""至少牵涉 k 项""至多牵涉 k 项"争议的精确条件查询
- 空集或不在上述七种之列的组合

## 查询格式（必须严格遵守）

每次只能提交一个查询，使用以下 XML 格式：

- 查询单一争议 A 的数量：
<query>A, count</query>

- 查询争议 B 或 C 的比例：
<query>B or C, ratio</query>

- 查询争议 A 或 B 或 C 的数量和比例：
<query>A or B or C, both</query>

注意：属性名称 A、B、C 大小写敏感，连接词使用"or"，查询类型为 count、ratio 或 both。

## 提交答案格式

当你收集足够信息后，请提交最终的卷宗归类结论，格式如下：

<answer>count=X, ratio=X/{n}</answer>

其中 X 是恰好具备两项争议特征的案件数量，X/{n} 是最简分数形式的比例。

请尽可能少地进行查询，高效推断出归类答案。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
The court's judicial data center is classifying the dossiers of a batch of complex commercial dispute cases currently under trial.

There are {n} cases in the current batch (a set size of {n}). The complaint for each case may involve any combination of three specific legal disputes (attributes): A (Intellectual Property Dispute), B (Cross-border Trade Clause), and C (Monopoly Behavior). Some cases may only involve conventional breaches of contract without these specific disputes, while some major cases might entangle all three. The qualitative nature of the disputes in the dossiers is fixed at the start of the classification and will not change.

Your goal is: to infer the count X of cases that have "exactly two dispute characteristics" (0 less than or equal to X less than or equal to {n}), and their proportion X/{n} (expressed as a simplified fraction).

## Allowed Query Types

You can only perform "union coverage queries" to the judicial data system, i.e., querying the count or proportion of cases that "involve at least one of certain legal disputes".

The seven allowed dispute unions are:
1. A: at least involves A (Intellectual Property Dispute)
2. B: at least involves B (Cross-border Trade Clause)
3. C: at least involves C (Monopoly Behavior)
4. A or B: at least involves A or B (or both)
5. B or C: at least involves B or C (or both)
6. C or A: at least involves C or A (or both)
7. A or B or C: at least involves any one (or more) of disputes A, B, C

For each query, you need to specify the type of data view to return:
- count: returns the number of cases satisfying the condition (integer)
- ratio: returns the proportion of cases satisfying the condition (simplified fraction)
- both: returns both count and ratio

## Forbidden Queries

The following query types are not allowed and will result in the system rejecting the request (classification failure) if attempted:
- Any intersection queries (e.g., "involves both A and B")
- Any exact condition queries about "exactly involving k", "at least involving k", or "at most involving k" disputes
- Empty set or combinations not among the seven types above

## Query Format (must be strictly followed)

Only one query can be submitted at a time, using the following XML format:

- Query the count of a single dispute A:
<query>A, count</query>

- Query the ratio of dispute B or C:
<query>B or C, ratio</query>

- Query both count and ratio of dispute A or B or C:
<query>A or B or C, both</query>

Note: Attribute names A, B, C are case-sensitive, use "or" as connector, query type is count, ratio, or both.

## Answer Submission Format

When you have collected sufficient information, submit your final dossier classification conclusion in the following format:

<answer>count=X, ratio=X/{n}</answer>

Where X is the count of cases with exactly two dispute characteristics, and X/{n} is the proportion in simplified fraction form.

Please use as few queries as possible to efficiently infer the classification answer.
"""

    tags = ["answer", "query"]
    
    reasoning_type = "演绎推理"
    data_structure = "集合"

    # 难度配置：难度越高，集合规模越大，属性分配越复杂
    # 每个难度都预设了固定的属性分配，确保游戏可重现
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {  # 简单：N=5，简单分配
                "n": 5,
                # 元素1: A,B; 元素2: B,C; 元素3: A; 元素4: C; 元素5: A,B,C
                # 恰好两个属性: 1,2 => X=2
                "attributes": {
                    "1": ["A", "B"],
                    "2": ["B", "C"],
                    "3": ["A"],
                    "4": ["C"],
                    "5": ["A", "B", "C"],
                },
            },
            2: {  # 中等偏下：N=8
                "n": 8,
                # 元素1: A,B; 元素2: B,C; 元素3: C,A; 元素4: A; 
                # 元素5: B; 元素6: C; 元素7: A,B,C; 元素8: 无
                # 恰好两个属性: 1,2,3 => X=3
                "attributes": {
                    "1": ["A", "B"],
                    "2": ["B", "C"],
                    "3": ["C", "A"],
                    "4": ["A"],
                    "5": ["B"],
                    "6": ["C"],
                    "7": ["A", "B", "C"],
                    "8": [],
                },
            },
            3: {  # 中等偏上：N=10
                "n": 10,
                # 元素1-2: A,B; 元素3-4: B,C; 元素5: C,A; 元素6: A; 
                # 元素7: B; 元素8: C; 元素9: A,B,C; 元素10: 无
                # 恰好两个属性: 1,2,3,4,5 => X=5
                "attributes": {
                    "1": ["A", "B"],
                    "2": ["A", "B"],
                    "3": ["B", "C"],
                    "4": ["B", "C"],
                    "5": ["C", "A"],
                    "6": ["A"],
                    "7": ["B"],
                    "8": ["C"],
                    "9": ["A", "B", "C"],
                    "10": [],
                },
            },
            4: {  # 较难：N=12
                "n": 12,
                # 更复杂的分配
                # 元素1-3: A,B; 元素4-5: B,C; 元素6-7: C,A; 元素8: A; 
                # 元素9: B; 元素10: C; 元素11-12: A,B,C
                # 恰好两个属性: 1,2,3,4,5,6,7 => X=7
                "attributes": {
                    "1": ["A", "B"],
                    "2": ["A", "B"],
                    "3": ["A", "B"],
                    "4": ["B", "C"],
                    "5": ["B", "C"],
                    "6": ["C", "A"],
                    "7": ["C", "A"],
                    "8": ["A"],
                    "9": ["B"],
                    "10": ["C"],
                    "11": ["A", "B", "C"],
                    "12": ["A", "B", "C"],
                },
            },
            5: {  # 难：N=15
                "n": 15,
                # 最复杂的分配
                # 元素1-4: A,B; 元素5-7: B,C; 元素8-9: C,A; 元素10-11: A; 
                # 元素12: B; 元素13: C; 元素14-15: A,B,C
                # 恰好两个属性: 1,2,3,4,5,6,7,8,9 => X=9
                "attributes": {
                    "1": ["A", "B"],
                    "2": ["A", "B"],
                    "3": ["A", "B"],
                    "4": ["A", "B"],
                    "5": ["B", "C"],
                    "6": ["B", "C"],
                    "7": ["B", "C"],
                    "8": ["C", "A"],
                    "9": ["C", "A"],
                    "10": ["A"],
                    "11": ["A"],
                    "12": ["B"],
                    "13": ["C"],
                    "14": ["A", "B", "C"],
                    "15": ["A", "B", "C"],
                },
            },
        },
        "en": {
            1: {
                "n": 5,
                "attributes": {
                    "1": ["A", "B"],
                    "2": ["B", "C"],
                    "3": ["A"],
                    "4": ["C"],
                    "5": ["A", "B", "C"],
                },
            },
            2: {
                "n": 8,
                "attributes": {
                    "1": ["A", "B"],
                    "2": ["B", "C"],
                    "3": ["C", "A"],
                    "4": ["A"],
                    "5": ["B"],
                    "6": ["C"],
                    "7": ["A", "B", "C"],
                    "8": [],
                },
            },
            3: {
                "n": 10,
                "attributes": {
                    "1": ["A", "B"],
                    "2": ["A", "B"],
                    "3": ["B", "C"],
                    "4": ["B", "C"],
                    "5": ["C", "A"],
                    "6": ["A"],
                    "7": ["B"],
                    "8": ["C"],
                    "9": ["A", "B", "C"],
                    "10": [],
                },
            },
            4: {
                "n": 12,
                "attributes": {
                    "1": ["A", "B"],
                    "2": ["A", "B"],
                    "3": ["A", "B"],
                    "4": ["B", "C"],
                    "5": ["B", "C"],
                    "6": ["C", "A"],
                    "7": ["C", "A"],
                    "8": ["A"],
                    "9": ["B"],
                    "10": ["C"],
                    "11": ["A", "B", "C"],
                    "12": ["A", "B", "C"],
                },
            },
            5: {
                "n": 15,
                "attributes": {
                    "1": ["A", "B"],
                    "2": ["A", "B"],
                    "3": ["A", "B"],
                    "4": ["A", "B"],
                    "5": ["B", "C"],
                    "6": ["B", "C"],
                    "7": ["B", "C"],
                    "8": ["C", "A"],
                    "9": ["C", "A"],
                    "10": ["A"],
                    "11": ["A"],
                    "12": ["B"],
                    "13": ["C"],
                    "14": ["A", "B", "C"],
                    "15": ["A", "B", "C"],
                },
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：加载难度配置，计算真实答案"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        
        # 存储每个元素的属性集合
        self.attributes = cfg["attributes"]
        self.n = cfg["n"]
        
        # 计算真实答案：恰好两个属性的元素数量
        self.answer_count = 0
        for element_id, attrs in self.attributes.items():
            if len(attrs) == 2:  # 恰好两个属性
                self.answer_count += 1
        
        # 计算答案比例（最简分数）
        self.answer_ratio = Fraction(self.answer_count, self.n)

    def _parse_query(self, query_str):
        """
        解析查询字符串，返回 (属性集合, 查询类型)
        例如："A or B, count" -> (["A", "B"], "count")
        """
        parts = [p.strip() for p in query_str.split(",")]
        if len(parts) != 2:
            raise ValueError("Query format error: expected 'attributes, type'")
        
        attr_part = parts[0].strip()
        query_type = parts[1].strip().lower()
        
        if query_type not in ["count", "ratio", "both"]:
            raise ValueError(f"Invalid query type: {query_type}")
        
        # 解析属性部分
        attr_list = [a.strip() for a in re.split(r'\s+or\s+', attr_part, flags=re.IGNORECASE)]
        
        # 验证属性合法性
        valid_attrs = {"A", "B", "C"}
        for attr in attr_list:
            if attr not in valid_attrs:
                raise ValueError(f"Invalid attribute: {attr}")
        
        # 检查是否为允许的七种查询之一
        attr_set = frozenset(attr_list)
        allowed_sets = [
            frozenset(["A"]),
            frozenset(["B"]),
            frozenset(["C"]),
            frozenset(["A", "B"]),
            frozenset(["B", "C"]),
            frozenset(["C", "A"]),
            frozenset(["A", "B", "C"]),
        ]
        
        if attr_set not in allowed_sets:
            raise ValueError(f"Query set not allowed: {attr_list}")
        
        return attr_list, query_type

    def _compute_union_count(self, attr_list):
        """计算满足"至少具有 attr_list 中任一属性"的元素数量"""
        count = 0
        for element_id, element_attrs in self.attributes.items():
            # 检查元素是否至少具有 attr_list 中的一个属性
            if any(attr in element_attrs for attr in attr_list):
                count += 1
        return count

    def evaluate(self, parsed_info):
        """评估模型提交的答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案格式: count=X, ratio=X/N
        try:
            kv_pairs = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            for kv in kv_pairs:
                if "=" not in kv:
                    continue
                k, v = kv.split("=", 1)
                ans_dict[k.strip()] = v.strip()
            
            if "count" not in ans_dict or "ratio" not in ans_dict:
                return False
            
            # 检查数量
            model_count = int(ans_dict["count"])
            if model_count != self.answer_count:
                return False
            
            # 检查比例（解析分数）
            model_ratio_str = ans_dict["ratio"]
            # 可能的格式: "2/5" 或 "2 / 5"
            ratio_parts = model_ratio_str.replace(" ", "").split("/")
            if len(ratio_parts) != 2:
                return False
            model_ratio = Fraction(int(ratio_parts[0]), int(ratio_parts[1]))
            
            return model_ratio == self.answer_ratio
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始的响应生成逻辑"""
        if "query" not in parsed_info:
            raise ValueError("No query tag found.")
        
        query_str = parsed_info["query"]
        attr_list, query_type = self._parse_query(query_str)
        
        # 计算并集覆盖的元素数量
        count = self._compute_union_count(attr_list)
        ratio = Fraction(count, self.n)
        
        # 根据查询类型返回响应
        if query_type == "count":
            return str(count)
        elif query_type == "ratio":
            return f"{ratio.numerator}/{ratio.denominator}"
        else:  # both
            return f"count={count}, ratio={ratio.numerator}/{ratio.denominator}"

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
        
        # 允许查询的七种属性并集
        allowed_attributes = [
            "A", 
            "B", 
            "C", 
            "A or B", 
            "B or C", 
            "C or A", 
            "A or B or C"
        ]
        
        # 允许的查询类型
        allowed_types = ["count", "ratio", "both"]
        
        # 枚举所有组合
        for attr_str in allowed_attributes:
            for type_str in allowed_types:
                # 构造符合 parse 方法预期的查询字符串 "Attributes, type"
                query_content = f"{attr_str}, {type_str}"
                
                # 构造 parsed_info
                parsed_info = {"query": query_content}
                
                # 直接调用核心计算逻辑，绕过 produce_response 的计数器
                # _cf_core_produce 依赖 self.attributes (只读)
                try:
                    answer = self._cf_core_produce(parsed_info)
                    results.append({
                        "query": f"<query>{query_content}</query>",
                        "answer": answer
                    })
                except Exception:
                    # 如果发生异常（理论上不应发生，因为这里构造的都是合法查询），则跳过
                    continue
                    
        return results

    def _cf_make_wrong(self, correct):
        """根据正确答案生成一个明显不同的错误答案"""
        # 纯数字情况
        if correct.isdigit():
            val = int(correct)
            return str(val + 1)
        
        # 组合格式: "count=X, ratio=P/Q"
        if "count=" in correct and "ratio=" in correct:
            try:
                kv_pairs = [x.strip() for x in correct.split(",")]
                ans_dict = {}
                for kv in kv_pairs:
                    if "=" in kv:
                        k, v = kv.split("=", 1)
                        ans_dict[k.strip()] = v.strip()
                c = int(ans_dict["count"])
                wrong_c = c + 1
                # 构造一个错误的比例
                return f"count={wrong_c}, ratio={wrong_c}/{self.n}"
            except Exception:
                return correct + "_WRONG"
        
        # 分数格式: "P/Q"
        if "/" in correct:
            try:
                parts = correct.split("/")
                numerator = int(parts[0].strip())
                denominator = int(parts[1].strip())
                wrong_num = numerator + 1
                return f"{wrong_num}/{denominator}"
            except Exception:
                return correct + "_WRONG"
                
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        else:
            # 简单的大小写敏感替换逻辑
            lower_c = correct.lower()
            if "yes" in lower_c:
                return correct.replace("Yes", "No").replace("yes", "no").replace("YES", "NO")
            if "no" in lower_c:
                return correct.replace("No", "Yes").replace("no", "yes").replace("NO", "YES")

        return correct + "_WRONG"