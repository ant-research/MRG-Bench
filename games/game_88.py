from .base import Game
import random

class TreeParameterInferenceGame(Game):

    contextualized_rule_zh_1 = """\
欢迎使用“交通网络客流推断系统”。规则如下：

管辖的交通网络设定为一棵有根树结构，共 {n} 个站点，编号从 1 到 {n}。总枢纽（根节点）为 {root}。每个站点的下级站点列表已经确定（无环状线路）。

定义：
- 深度：从总枢纽出发到该站点的线路段数（即换乘次数），总枢纽深度为 0。
- 终端站（叶子节点）：没有下级站点的站点。
- 中转枢纽（内部节点）：有至少一个下级站点的站点。

每个站点都有一个客流量基数，其取值由四个隐藏的系统常量决定：EI、OI、EL、OL（均为 1 到 9 之间的正整数）。

站点客流量取值规则：
- 如果站点是中转枢纽且深度为偶数，其值为 EI
- 如果站点是中转枢纽且深度为奇数，其值为 OI
- 如果站点是终端站且深度为偶数，其值为 EL
- 如果站点是终端站且深度为奇数，其值为 OL

你的目标分为两步：
1. 通过查询推断出 EI、OI、EL、OL 四个参数的准确值
2. 当你推断正确后，系统会指定一个从未被查询过的目标站点 t，你需要在不再查询的情况下给出该站点及其所有下级站点构成的子网路客流总和

你可以进行以下两类查询：

类型 A - 子网路客流求和查询（最多 12 次）：
- 指定一个站点编号 u
- 系统会返回该站点及其所有下级站点中所有客流量基数的总和

类型 B - 网络结构查询（不限次数）：
- 查询交通网络的拓扑结构信息
- 系统会返回各站点的下级列表等结构信息（不包含数值）

每次只能进行一个操作。使用以下 XML 格式：

- 子网路客流求和查询（例如查询站点 5）：
<query_sum>5</query_sum>

- 网络结构查询：
<query_structure></query_structure>

- 提交四个参数的推断（例如 EI=3, OI=5, EL=7, OL=2）：
<submit_params>EI=3, OI=5, EL=7, OL=2</submit_params>

- 提交最终答案（当系统给出目标站点 t 后，预测其子网路客流和，例如预测为 42）：
<answer>42</answer>

注意：
- 求和查询次数有限，请谨慎使用
- 必须先正确推断出四个参数，才能进入最终预测阶段
- 最终预测时不能再进行任何查询
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Traffic Network Flow Inference System". Here are the rules:

The managed traffic network is modeled as a rooted tree with {n} stations, numbered from 1 to {n}. The central hub (root node) is {root}. Each station's list of subordinate stations is predetermined (acyclic).

Definitions:
- Depth: The number of transit segments from the central hub; the central hub has a depth of 0.
- Terminal station (Leaf node): A station with no subordinate stations.
- Transfer hub (Internal node): A station with at least one subordinate station.

Each station has a base passenger flow determined by four hidden system constants: EI, OI, EL, OL (all positive integers between 1 and 9).

Station flow value rules:
- If the station is a transfer hub with even depth, its value is EI
- If the station is a transfer hub with odd depth, its value is OI
- If the station is a terminal station with even depth, its value is EL
- If the station is a terminal station with odd depth, its value is OL

Your goal has two steps:
1. Infer the exact values of EI, OI, EL, OL through queries
2. After correct inference, the system will specify a target station t that has never been queried, and you need to predict the total passenger flow of its sub-network (itself and all subordinate stations) without further queries

You can perform two types of queries:

Type A - Sub-network Flow Sum Query (at most 12 times):
- Specify a station number u
- The system will return the sum of all base passenger flows in that station's sub-network

Type B - Network Structure Query (unlimited):
- Query the topological structure information of the traffic network
- The system will return the subordinate list and other structural info (no values)

Each turn allows only one operation. Use the following XML format:

- Sub-network flow sum query (e.g., querying station 5):
<query_sum>5</query_sum>

- Network structure query:
<query_structure></query_structure>

- Submit parameter inference (e.g., EI=3, OI=5, EL=7, OL=2):
<submit_params>EI=3, OI=5, EL=7, OL=2</submit_params>

- Submit final answer (after the system gives you target station t, predict its sub-network flow sum, e.g., 42):
<answer>42</answer>

Note:
- Flow sum queries are limited, use them wisely
- You must correctly infer all four parameters before entering the final prediction phase
- No queries are allowed during the final prediction
"""

    contextualized_rule_zh_2 = """\
我们来进行一项“医疗卫生资源配置推断”任务。规则如下：

医疗管辖网络设定为一棵有根树，共 {n} 个医疗机构，编号从 1 到 {n}。总医院（根节点）为 {root}。每个机构的下级机构列表已经确定（无环）。

定义：
- 深度：从总医院出发到该机构的管理层级数，总医院深度为 0。
- 基层诊所（叶子节点）：没有下级机构的医疗单位。
- 区域中心（内部节点）：有至少一个下级机构的医疗单位。

每个机构都有一个资源配置基数，其取值由四个隐藏的常量决定：EI、OI、EL、OL（均为 1 到 9 之间的正整数）。

机构资源取值规则：
- 如果机构是区域中心且深度为偶数，其值为 EI
- 如果机构是区域中心且深度为奇数，其值为 OI
- 如果机构是基层诊所且深度为偶数，其值为 EL
- 如果机构是基层诊所且深度为奇数，其值为 OL

你的目标分为两步：
1. 通过查询推断出 EI、OI、EL、OL 四个参数的准确值
2. 当你推断正确后，系统会指定一个从未被查询过的机构 t，你需要在不再查询的情况下给出该机构及其所有下辖单位的资源总和

你可以进行以下两类查询：

类型 A - 管辖区资源求和查询（最多 12 次）：
- 指定一个机构编号 u
- 系统会返回该机构及其下辖网络中所有机构资源配置基数的总和

类型 B - 组织结构查询（不限次数）：
- 查询医疗网络的层级结构信息
- 系统会返回树状管理架构的下级列表等信息（不包含数值）

每次只能进行一个操作。使用以下 XML 格式：

- 管辖区资源求和查询（例如查询机构 5）：
<query_sum>5</query_sum>

- 组织结构查询：
<query_structure></query_structure>

- 提交四个参数的推断（例如 EI=3, OI=5, EL=7, OL=2）：
<submit_params>EI=3, OI=5, EL=7, OL=2</submit_params>

- 提交最终答案（当系统给出目标机构 t 后，预测其管辖区资源总和，例如预测为 42）：
<answer>42</answer>

注意：
- 资源求和查询次数有限，请谨慎使用
- 必须先正确推断出四个参数，才能进入最终预测阶段
- 最终预测时不能再进行任何查询
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's conduct a "Healthcare Resource Allocation Inference" task. Here are the rules:

The medical administrative network is set as a rooted tree with {n} healthcare facilities, numbered from 1 to {n}. The Main Hospital (root node) is {root}. Each facility's list of subordinate facilities is predetermined (acyclic).

Definitions:
- Depth: The number of administrative tiers from the Main Hospital; Main Hospital has a depth of 0.
- Local Clinic (Leaf node): A facility with no subordinate facilities.
- Regional Center (Internal node): A facility with at least one subordinate facility.

Each facility has a resource allocation baseline determined by four hidden constants: EI, OI, EL, OL (all positive integers between 1 and 9).

Facility resource rules:
- If the facility is a Regional Center with even depth, its value is EI
- If the facility is a Regional Center with odd depth, its value is OI
- If the facility is a Local Clinic with even depth, its value is EL
- If the facility is a Local Clinic with odd depth, its value is OL

Your goal has two steps:
1. Infer the exact values of EI, OI, EL, OL through queries
2. After correct inference, the system will specify a target facility t that has never been queried, and you need to predict the total resource sum of its jurisdiction (itself and all subordinate units) without further queries

You can perform two types of queries:

Type A - Jurisdiction Resource Sum Query (at most 12 times):
- Specify a facility number u
- The system will return the sum of all resource baselines in that facility's jurisdiction network

Type B - Organization Structure Query (unlimited):
- Query the hierarchical structure information of the medical network
- The system will return the subordinate list and other structural info (no values)

Each turn allows only one operation. Use the following XML format:

- Jurisdiction resource sum query (e.g., querying facility 5):
<query_sum>5</query_sum>

- Organization structure query:
<query_structure></query_structure>

- Submit parameter inference (e.g., EI=3, OI=5, EL=7, OL=2):
<submit_params>EI=3, OI=5, EL=7, OL=2</submit_params>

- Submit final answer (after the system gives you target facility t, predict its jurisdiction resource sum, e.g., 42):
<answer>42</answer>

Note:
- Resource sum queries are limited, use them wisely
- You must correctly infer all four parameters before entering the final prediction phase
- No queries are allowed during the final prediction
"""

    contextualized_rule_zh_3 = """\
我们来执行一项“教育经费指标推导”任务。规则如下：

教育行政系统设定为一棵有根树，共 {n} 个教育机构，编号从 1 到 {n}。最高教育局（根节点）为 {root}。每个机构的直属下级列表已经确定（无交叉管辖）。

定义：
- 深度：从最高教育局到该机构的行政级别落差，最高教育局深度为 0。
- 一线学校（叶子节点）：没有下级管理单位的实体学校。
- 中层教育局（内部节点）：有至少一个直属下级机构的管理单位。

每个教育机构都有一项经费划拨基数，取值由四个隐藏的政策常量决定：EI、OI、EL、OL（均为 1 到 9 之间的正整数）。

机构经费取值规则：
- 如果机构是中层教育局且深度为偶数，其值为 EI
- 如果机构是中层教育局且深度为奇数，其值为 OI
- 如果机构是一线学校且深度为偶数，其值为 EL
- 如果机构是一线学校且深度为奇数，其值为 OL

你的目标分为两步：
1. 通过查询推断出 EI、OI、EL、OL 四个参数的准确值
2. 当你推断正确后，系统会指定一个从未被查核过的机构 t，你需要在不再查询的情况下给出该机构及其所有下辖单位的经费总和

你可以进行以下两类查询：

类型 A - 辖区经费求和查询（最多 12 次）：
- 指定一个机构编号 u
- 系统会返回该机构及其整个下辖网络中所有节点经费基数的总和

类型 B - 行政结构查询（不限次数）：
- 查询教育系统的行政隶属关系
- 系统会返回各机构的下属列表等结构信息（不包含财务数值）

每次只能进行一个操作。使用以下 XML 格式：

- 辖区经费求和查询（例如查询机构 5）：
<query_sum>5</query_sum>

- 行政结构查询：
<query_structure></query_structure>

- 提交四个参数的推断（例如 EI=3, OI=5, EL=7, OL=2）：
<submit_params>EI=3, OI=5, EL=7, OL=2</submit_params>

- 提交最终答案（当系统给出目标机构 t 后，预测其辖区经费和，例如预测为 42）：
<answer>42</answer>

注意：
- 经费求和查询次数有限，请谨慎使用
- 必须先正确推断出四个参数，才能进入最终预测阶段
- 最终预测时不能再进行任何查询
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's perform an "Education Funding Metric Inference" task. Here are the rules:

The education administrative system is set as a rooted tree with {n} institutions, numbered from 1 to {n}. The Supreme Education Board (root node) is {root}. Each institution's direct subordinate list is predetermined (no overlapping jurisdiction).

Definitions:
- Depth: The administrative tier gap from the Supreme Board; the Supreme Board has a depth of 0.
- Frontline School (Leaf node): An actual school with no subordinate units.
- Intermediate Board (Internal node): An administrative unit with at least one subordinate institution.

Each institution has a funding allocation baseline determined by four hidden policy constants: EI, OI, EL, OL (all positive integers between 1 and 9).

Institution funding rules:
- If the institution is an Intermediate Board with even depth, its value is EI
- If the institution is an Intermediate Board with odd depth, its value is OI
- If the institution is a Frontline School with even depth, its value is EL
- If the institution is a Frontline School with odd depth, its value is OL

Your goal has two steps:
1. Infer the exact values of EI, OI, EL, OL through queries
2. After correct inference, the system will specify a target institution t that has never been audited, and you need to predict the total funding sum of its jurisdiction without further queries

You can perform two types of queries:

Type A - Jurisdiction Funding Sum Query (at most 12 times):
- Specify an institution number u
- The system will return the sum of all funding baselines in that institution's jurisdiction network

Type B - Administrative Structure Query (unlimited):
- Query the administrative hierarchy of the education system
- The system will return the subordinate list and other structural info (no financial values)

Each turn allows only one operation. Use the following XML format:

- Jurisdiction funding sum query (e.g., querying institution 5):
<query_sum>5</query_sum>

- Administrative structure query:
<query_structure></query_structure>

- Submit parameter inference (e.g., EI=3, OI=5, EL=7, OL=2):
<submit_params>EI=3, OI=5, EL=7, OL=2</submit_params>

- Submit final answer (after the system gives you target institution t, predict its jurisdiction funding sum, e.g., 42):
<answer>42</answer>

Note:
- Funding sum queries are limited, use them wisely
- You must correctly infer all four parameters before entering the final prediction phase
- No queries are allowed during the final prediction
"""

    contextualized_rule_zh_4 = """\
欢迎进入“工业制造BOM成本解析”环节。规则如下：

产品的物料清单（BOM）设定为一棵有根树，共包含 {n} 个组件/零件，编号从 1 到 {n}。最终成品（根节点）为 {root}。每个组件的子项构成列表已经确定（无循环依赖）。

定义：
- 深度：从最终成品向下拆解的层级数，最终成品的深度为 0。
- 基础原料（叶子节点）：不需要进一步拆解的底层零件。
- 子装配体（内部节点）：由至少一个子项构成的中间组件。

每个节点（组件或原料）都有一个加工碳排放基数，取值由四个隐藏的工艺常量决定：EI、OI、EL、OL（均为 1 到 9 之间的正整数）。

节点排碳取值规则：
- 如果节点是子装配体且深度为偶数，其值为 EI
- 如果节点是子装配体且深度为奇数，其值为 OI
- 如果节点是基础原料且深度为偶数，其值为 EL
- 如果节点是基础原料且深度为奇数，其值为 OL

你的目标分为两步：
1. 通过查询推断出 EI、OI、EL、OL 四个参数的准确值
2. 当你推断正确后，系统会指定一个从未被检测过的节点 t，你需要在不再查询的情况下给出该组件及其所有底层子项的累计碳排放总和

你可以进行以下两类查询：

类型 A - 累计排碳求和查询（最多 12 次）：
- 指定一个节点编号 u
- 系统会返回该组件及其BOM分支下所有节点的排碳基数总和

类型 B - BOM结构查询（不限次数）：
- 查询产品的物料清单层级关系
- 系统会返回各组件的构成列表等结构信息（不包含数值）

每次只能进行一个操作。使用以下 XML 格式：

- 累计排碳求和查询（例如查询组件 5）：
<query_sum>5</query_sum>

- BOM结构查询：
<query_structure></query_structure>

- 提交四个参数的推断（例如 EI=3, OI=5, EL=7, OL=2）：
<submit_params>EI=3, OI=5, EL=7, OL=2</submit_params>

- 提交最终答案（当系统给出目标节点 t 后，预测其累计排碳总和，例如预测为 42）：
<answer>42</answer>

注意：
- 求和查询次数有限，请谨慎优化查询策略
- 必须先正确推断出四个参数，才能进入最终预测阶段
- 最终预测时不能再进行任何查询
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Industrial BOM Cost Parsing" phase. Here are the rules:

The product's Bill of Materials (BOM) is modeled as a rooted tree with {n} components/parts, numbered from 1 to {n}. The Final Product (root node) is {root}. Each component's sub-item list is predetermined (no cyclic dependencies).

Definitions:
- Depth: The number of breakdown levels from the Final Product; the Final Product has a depth of 0.
- Base Material (Leaf node): A bottom-level part that requires no further breakdown.
- Sub-assembly (Internal node): An intermediate component composed of at least one sub-item.

Each node (component or material) has a base carbon emission factor determined by four hidden process constants: EI, OI, EL, OL (all positive integers between 1 and 9).

Node emission rules:
- If the node is a Sub-assembly with even depth, its value is EI
- If the node is a Sub-assembly with odd depth, its value is OI
- If the node is a Base Material with even depth, its value is EL
- If the node is a Base Material with odd depth, its value is OL

Your goal has two steps:
1. Infer the exact values of EI, OI, EL, OL through queries
2. After correct inference, the system will specify a target node t that has never been tested, and you need to predict the cumulative carbon emission sum of that component and all its underlying sub-items without further queries

You can perform two types of queries:

Type A - Cumulative Emission Sum Query (at most 12 times):
- Specify a node number u
- The system will return the sum of all base carbon emission factors in that component's BOM branch

Type B - BOM Structure Query (unlimited):
- Query the hierarchical relationships of the Bill of Materials
- The system will return the composition list and other structural info (no values)

Each turn allows only one operation. Use the following XML format:

- Cumulative emission sum query (e.g., querying component 5):
<query_sum>5</query_sum>

- BOM structure query:
<query_structure></query_structure>

- Submit parameter inference (e.g., EI=3, OI=5, EL=7, OL=2):
<submit_params>EI=3, OI=5, EL=7, OL=2</submit_params>

- Submit final answer (after the system gives you target node t, predict its cumulative emission sum, e.g., 42):
<answer>42</answer>

Note:
- Emission sum queries are limited, optimize your query strategy carefully
- You must correctly infer all four parameters before entering the final prediction phase
- No queries are allowed during the final prediction
"""

    contextualized_rule_zh_5 = """\
我们来推进一项“法律条款效力溯源”任务。规则如下：

法典结构设定为一棵有根树，共 {n} 个法律节点，编号从 1 到 {n}。根本大法（根节点）为 {root}。每个法律条款的衍生细则列表已经确定（无循环引用）。

定义：
- 深度：从根本大法向下衍生的层级数，根本大法深度为 0。
- 具体细则（叶子节点）：没有进一步衍生条款的底层规定。
- 综合编章（内部节点）：包含至少一项衍生条款的框架性条文。

每个节点都有一个法理权重指数，取值由四个隐藏的司法常量决定：EI、OI、EL、OL（均为 1 到 9 之间的正整数）。

条款权重取值规则：
- 如果节点是综合编章且深度为偶数，其值为 EI
- 如果节点是综合编章且深度为奇数，其值为 OI
- 如果节点是具体细则且深度为偶数，其值为 EL
- 如果节点是具体细则且深度为奇数，其值为 OL

你的目标分为两步：
1. 通过查询推断出 EI、OI、EL、OL 四个参数的准确值
2. 当你推断正确后，系统会指定一个从未被查阅过的节点 t，你需要在不再查询的情况下给出该编章及其所有衍生细则的累计权重总和

你可以进行以下两类查询：

类型 A - 法系权重求和查询（最多 12 次）：
- 指定一个节点编号 u
- 系统会返回该条款及其分支下所有衍生条款的法理权重总和

类型 B - 法典结构查询（不限次数）：
- 查询法律条文的派生关系
- 系统会返回各条款的衍生列表等结构信息（不包含权重数值）

每次只能进行一个操作。使用以下 XML 格式：

- 法系权重求和查询（例如查询条款 5）：
<query_sum>5</query_sum>

- 法典结构查询：
<query_structure></query_structure>

- 提交四个参数的推断（例如 EI=3, OI=5, EL=7, OL=2）：
<submit_params>EI=3, OI=5, EL=7, OL=2</submit_params>

- 提交最终答案（当系统给出目标节点 t 后，预测其法系权重总和，例如预测为 42）：
<answer>42</answer>

注意：
- 权重求和查询次数有限，请谨慎使用
- 必须先正确推断出四个参数，才能进入最终预测阶段
- 最终预测时不能再进行任何查询
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's advance a "Legal Statute Efficacy Tracing" task. Here are the rules:

The legal code structure is modeled as a rooted tree with {n} legal nodes, numbered from 1 to {n}. The Basic Law (root node) is {root}. Each legal statute's list of derivative clauses is predetermined (no circular references).

Definitions:
- Depth: The number of derivation levels from the Basic Law; the Basic Law has a depth of 0.
- Specific Clause (Leaf node): A bottom-level provision with no further derivative clauses.
- Comprehensive Chapter (Internal node): A framework provision containing at least one derivative clause.

Each node has a legal weight index determined by four hidden judicial constants: EI, OI, EL, OL (all positive integers between 1 and 9).

Statute weight rules:
- If the node is a Comprehensive Chapter with even depth, its value is EI
- If the node is a Comprehensive Chapter with odd depth, its value is OI
- If the node is a Specific Clause with even depth, its value is EL
- If the node is a Specific Clause with odd depth, its value is OL

Your goal has two steps:
1. Infer the exact values of EI, OI, EL, OL through queries
2. After correct inference, the system will specify a target node t that has never been reviewed, and you need to predict the cumulative weight sum of that chapter and all its derivative clauses without further queries

You can perform two types of queries:

Type A - Legal System Weight Sum Query (at most 12 times):
- Specify a node number u
- The system will return the sum of all legal weight indices in that statute's derivative branch

Type B - Legal Code Structure Query (unlimited):
- Query the derivation relationships of the legal provisions
- The system will return the derivative list and other structural info (no weight values)

Each turn allows only one operation. Use the following XML format:

- Legal system weight sum query (e.g., querying statute 5):
<query_sum>5</query_sum>

- Legal code structure query:
<query_structure></query_structure>

- Submit parameter inference (e.g., EI=3, OI=5, EL=7, OL=2):
<submit_params>EI=3, OI=5, EL=7, OL=2</submit_params>

- Submit final answer (after the system gives you target node t, predict its legal system weight sum, e.g., 42):
<answer>42</answer>

Note:
- Weight sum queries are limited, use them wisely
- You must correctly infer all four parameters before entering the final prediction phase
- No queries are allowed during the final prediction
"""

    game_rule_zh = """\
我们来玩一个"树参数推理"游戏。规则如下：

游戏设定了一棵有根树，共 {n} 个节点，编号从 1 到 {n}。根节点为 {root}。每个节点的子节点列表已经确定（无环）。

定义：
- 深度：从根节点出发到该节点的边数，根节点深度为 0。
- 叶子节点：没有子节点的节点。
- 内部节点：有至少一个子节点的节点。

每个节点都有一个取值，取值规则由四个隐藏的常量决定：EI、OI、EL、OL（均为 1 到 9 之间的正整数）。

节点取值规则：
- 如果节点是内部节点且深度为偶数，其值为 EI
- 如果节点是内部节点且深度为奇数，其值为 OI
- 如果节点是叶子节点且深度为偶数，其值为 EL
- 如果节点是叶子节点且深度为奇数，其值为 OL

你的目标分为两步：
1. 通过查询推断出 EI、OI、EL、OL 四个参数的准确值
2. 当你推断正确后，我会指定一个从未被查询过的节点 t，你需要在不再查询的情况下给出该节点子树的总和

你可以进行以下两类查询：

类型 A - 子树求和查询（最多 12 次）：
- 指定一个节点编号 u
- 我会返回该节点子树中所有节点值的总和

类型 B - 结构查询（不限次数）：
- 查询树的结构信息
- 我会返回树的孩子列表等结构信息（不包含数值）

每次只能进行一个操作。使用以下 XML 格式：

- 子树求和查询（例如查询节点 5）：
<query_sum>5</query_sum>

- 结构查询：
<query_structure></query_structure>

- 提交四个参数的推断（例如 EI=3, OI=5, EL=7, OL=2）：
<submit_params>EI=3, OI=5, EL=7, OL=2</submit_params>

- 提交最终答案（当我给出目标节点 t 后，预测其子树和，例如预测为 42）：
<answer>42</answer>

注意：
- 子树求和查询次数有限，请谨慎使用
- 必须先正确推断出四个参数，才能进入最终预测阶段
- 最终预测时不能再进行任何查询
"""

    game_rule_en = """\
Let's play a "Tree Parameter Inference" game. Here are the rules:

The game is set on a rooted tree with {n} nodes, numbered from 1 to {n}. The root node is {root}. Each node's children list is predetermined (acyclic).

Definitions:
- Depth: The number of edges from the root to the node; root has depth 0.
- Leaf node: A node with no children.
- Internal node: A node with at least one child.

Each node has a value determined by four hidden constants: EI, OI, EL, OL (all positive integers between 1 and 9).

Node value rules:
- If the node is internal with even depth, its value is EI
- If the node is internal with odd depth, its value is OI
- If the node is a leaf with even depth, its value is EL
- If the node is a leaf with odd depth, its value is OL

Your goal has two steps:
1. Infer the exact values of EI, OI, EL, OL through queries
2. After correct inference, I will specify a node t that has never been queried, and you need to predict its subtree sum without further queries

You can perform two types of queries:

Type A - Subtree Sum Query (at most 12 times):
- Specify a node number u
- I will return the sum of all node values in that node's subtree

Type B - Structure Query (unlimited):
- Query the tree structure information
- I will return the children list and other structural information (no values)

Each turn allows only one operation. Use the following XML format:

- Subtree sum query (e.g., querying node 5):
<query_sum>5</query_sum>

- Structure query:
<query_structure></query_structure>

- Submit parameter inference (e.g., EI=3, OI=5, EL=7, OL=2):
<submit_params>EI=3, OI=5, EL=7, OL=2</submit_params>

- Submit final answer (after I give you target node t, predict its subtree sum, e.g., 42):
<answer>42</answer>

Note:
- Subtree sum queries are limited, use them wisely
- You must correctly infer all four parameters before entering the final prediction phase
- No queries are allowed during final prediction
"""

    tags = ["answer", "query_sum", "query_structure", "submit_params"]
    
    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        1: {
            "n": 7,
            "root": 1,
            "children": {
                1: [2, 3],
                2: [4, 5],
                3: [6, 7],
                4: [],
                5: [],
                6: [],
                7: []
            },
            "params": {"EI": 3, "OI": 5, "EL": 7, "OL": 2}
        },
        2: {
            "n": 10,
            "root": 1,
            "children": {
                1: [2, 3, 4],
                2: [5, 6],
                3: [7],
                4: [8, 9, 10],
                5: [],
                6: [],
                7: [],
                8: [],
                9: [],
                10: []
            },
            "params": {"EI": 4, "OI": 6, "EL": 2, "OL": 8}
        },
        3: {
            "n": 13,
            "root": 1,
            "children": {
                1: [2, 3],
                2: [4, 5, 6],
                3: [7, 8],
                4: [9, 10],
                5: [11],
                6: [],
                7: [12],
                8: [13],
                9: [],
                10: [],
                11: [],
                12: [],
                13: []
            },
            "params": {"EI": 5, "OI": 3, "EL": 8, "OL": 1}
        },
        4: {
            "n": 18,
            "root": 1,
            "children": {
                1: [2, 3, 4],
                2: [5, 6],
                3: [7, 8, 9],
                4: [10, 11],
                5: [12, 13],
                6: [14],
                7: [],
                8: [15],
                9: [16],
                10: [],
                11: [17, 18],
                12: [],
                13: [],
                14: [],
                15: [],
                16: [],
                17: [],
                18: []
            },
            "params": {"EI": 7, "OI": 4, "EL": 3, "OL": 9}
        },
        5: {
            "n": 25,
            "root": 1,
            "children": {
                1: [2, 3, 4, 5],
                2: [6, 7, 8],
                3: [9, 10],
                4: [11, 12, 13],
                5: [14],
                6: [15, 16],
                7: [17],
                8: [],
                9: [18, 19],
                10: [20],
                11: [],
                12: [21, 22],
                13: [],
                14: [23, 24, 25],
                15: [],
                16: [],
                17: [],
                18: [],
                19: [],
                20: [],
                21: [],
                22: [],
                23: [],
                24: [],
                25: []
            },
            "params": {"EI": 6, "OI": 2, "EL": 9, "OL": 4}
        }
    }

    def __init__(self, config):
        self.query_count = 0
        self.max_queries = 12
        self.params_guessed = False
        self.queried_nodes = set()
        self.target_node = None
        self.param_submit_count = 0
        self.max_param_submits = 3
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        
        self._game_info["n"] = cfg["n"]
        self._game_info["root"] = cfg["root"]
        
        self.children = cfg["children"]
        self.root = cfg["root"]
        self.n = cfg["n"]
        
        seed = getattr(self.config, 'seed', None)
        if seed is not None:
            rng = random.Random(seed)
            self.true_params = {
                "EI": rng.randint(1, 9),
                "OI": rng.randint(1, 9),
                "EL": rng.randint(1, 9),
                "OL": rng.randint(1, 9),
            }
        else:
            self.true_params = cfg["params"].copy()
        
        self.depth = {}
        self._compute_depth(self.root, 0)
        
        self.node_values = {}
        for node in range(1, self.n + 1):
            is_leaf = len(self.children[node]) == 0
            is_even_depth = self.depth[node] % 2 == 0
            
            if is_leaf:
                self.node_values[node] = self.true_params["EL"] if is_even_depth else self.true_params["OL"]
            else:
                self.node_values[node] = self.true_params["EI"] if is_even_depth else self.true_params["OI"]

        seed_val = seed if seed is not None else 0
        rng_target = random.Random(42 + self.n + diff + seed_val)
        all_nodes = list(range(1, self.n + 1))
        rng_target.shuffle(all_nodes)
        self._predetermined_target = all_nodes[0]

    def _compute_depth(self, node, d):
        self.depth[node] = d
        for child in self.children[node]:
            self._compute_depth(child, d + 1)

    def _compute_subtree_sum(self, node):
        total = self.node_values[node]
        for child in self.children[node]:
            total += self._compute_subtree_sum(child)
        return total

    def _get_subtree_coefficients(self, node):
        counts = {"a": 0, "b": 0, "c": 0, "d": 0}
        
        def dfs(n):
            is_leaf = len(self.children[n]) == 0
            is_even = self.depth[n] % 2 == 0
            
            if is_leaf:
                if is_even:
                    counts["c"] += 1
                else:
                    counts["d"] += 1
            else:
                if is_even:
                    counts["a"] += 1
                else:
                    counts["b"] += 1
            
            for child in self.children[n]:
                dfs(child)
        
        dfs(node)
        return counts

    def _format_tree_structure(self):
        if self.config.language == "zh":
            result = f"根节点: {self.root}\n子节点列表:\n"
            for node in sorted(self.children.keys()):
                children_str = ", ".join(map(str, self.children[node])) if self.children[node] else "无"
                result += f"  节点 {node}: [{children_str}]\n"
        else:
            result = f"Root: {self.root}\nChildren list:\n"
            for node in sorted(self.children.keys()):
                children_str = ", ".join(map(str, self.children[node])) if self.children[node] else "None"
                result += f"  Node {node}: [{children_str}]\n"
        return result.strip()

    def evaluate(self, parsed_info):
        if not self.params_guessed or self.target_node is None:
            return False
        
        try:
            predicted_sum = int(parsed_info["answer"].strip())
            actual_sum = self._compute_subtree_sum(self.target_node)
            return predicted_sum == actual_sum
        except (ValueError, TypeError, KeyError):
            return False

    def _cf_core_produce(self, parsed_info):
        lang = self.config.language

        if self.params_guessed and self.target_node is not None:
            if "query_structure" in parsed_info or "query_sum" in parsed_info or "submit_params" in parsed_info:
                return "错误：最终预测阶段不能再进行任何查询或提交参数。请直接提交答案。" if lang == "zh" else "Error: No queries or parameter submissions allowed during the final prediction phase. Please submit your answer directly."

        if "query_structure" in parsed_info:
            return self._format_tree_structure()
        
        if "query_sum" in parsed_info:
            if self.query_count >= self.max_queries:
                return "错误：已达到最大查询次数限制。" if lang == "zh" else "Error: Maximum query limit reached."
            
            if self.params_guessed:
                return "错误：参数已确认后不能再进行查询。" if lang == "zh" else "Error: Cannot query after parameters are confirmed."
            
            try:
                node = int(parsed_info["query_sum"].strip())
                if node < 1 or node > self.n:
                    return "错误：节点编号超出范围。" if lang == "zh" else "Error: Node number out of range."
                
                self.query_count += 1
                self.queried_nodes.add(node)
                subtree_sum = self._compute_subtree_sum(node)
                return str(subtree_sum)
            except (ValueError, TypeError):
                return "错误：无效的节点编号。" if lang == "zh" else "Error: Invalid node number."
        
        if "submit_params" in parsed_info:
            self.param_submit_count += 1
            if self.param_submit_count > self.max_param_submits:
                if lang == "zh":
                    msg = "错误：参数提交次数已用完，游戏失败。"
                else:
                    msg = "Error: Parameter submission attempts exhausted, game over."
                self.state.set_state("failed", "parameter submission attempts exhausted")
                return msg
            try:
                raw = parsed_info["submit_params"]
                kv_pairs = [x.strip() for x in raw.split(",")]
                params = {}
                for kv in kv_pairs:
                    k, v = kv.split("=")
                    params[k.strip()] = int(v.strip())
                
                if set(params.keys()) != {"EI", "OI", "EL", "OL"}:
                    return "错误：必须提交所有四个参数 EI、OI、EL、OL。" if lang == "zh" else "Error: Must submit all four parameters EI, OI, EL, OL."
                
                if params == self.true_params:
                    self.params_guessed = True
                    available_nodes = [n for n in range(1, self.n + 1) if n not in self.queried_nodes]
                    if not available_nodes:
                        available_nodes = list(range(1, self.n + 1))
                    
                    if self._predetermined_target in available_nodes:
                        self.target_node = self._predetermined_target
                    else:
                        self.target_node = available_nodes[0]
                    
                    if lang == "zh":
                        return f"参数推断正确！\n现在请预测节点 {self.target_node} 的子树和（不能再进行查询）。"
                    else:
                        return f"Parameters correct!\nNow predict the subtree sum of node {self.target_node} (no more queries allowed)."
                else:
                    if lang == "zh":
                        return f"参数推断错误。剩余查询次数：{self.max_queries - self.query_count}"
                    else:
                        return f"Parameters incorrect. Remaining queries: {self.max_queries - self.query_count}"
            except (ValueError, TypeError, KeyError, AttributeError, IndexError):
                return "错误：无效的参数格式。" if lang == "zh" else "Error: Invalid parameter format."
        
        return "错误：无法识别的操作。" if lang == "zh" else "Error: Unrecognized operation."

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        for node in range(1, self.n + 1):
            queries.append({
                "query": f"<query_sum>{node}</query_sum>",
                "answer": str(self._compute_subtree_sum(node))
            })
        queries.append({
            "query": "<query_structure></query_structure>",
            "answer": self._format_tree_structure()
        })
        
        submit_msg = f"<submit_params>EI={self.true_params['EI']}, OI={self.true_params['OI']}, EL={self.true_params['EL']}, OL={self.true_params['OL']}</submit_params>"
        
        if self.target_node is None:
            available_nodes = [n for n in range(1, self.n + 1) if n not in self.queried_nodes]
            if not available_nodes:
                available_nodes = list(range(1, self.n + 1))
            
            if self._predetermined_target in available_nodes:
                self.target_node = self._predetermined_target
            else:
                self.target_node = available_nodes[0]
            self.params_guessed = True

        if self.config.language == "zh":
            ans_msg = f"参数推断正确！\n现在请预测节点 {self.target_node} 的子树和（不能再进行查询）。"
        else:
            ans_msg = f"Parameters correct!\nNow predict the subtree sum of node {self.target_node} (no more queries allowed)."

        queries.append({
            "query": submit_msg,
            "answer": ans_msg
        })
        
        return queries

    def _cf_make_wrong(self, correct):
        if correct.isdigit() or (correct.startswith('-') and correct[1:].isdigit()):
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        else:
            lower_correct = correct.lower()
            if "yes" in lower_correct:
                if "Yes" in correct: return correct.replace("Yes", "No")
                if "YES" in correct: return correct.replace("YES", "NO")
                return correct.replace("yes", "no")
            if "no" in lower_correct:
                if "No" in correct: return correct.replace("No", "Yes")
                if "NO" in correct: return correct.replace("NO", "YES")
                return correct.replace("no", "yes")
        
        return correct + "_WRONG"

