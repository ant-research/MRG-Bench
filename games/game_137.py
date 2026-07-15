from .base import Game

class StructureIdentificationGame(Game):
    reasoning_type = "溯因推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"交互式结构辨识"推理游戏，规则如下：

游戏设定了一个标签集合，包含 {n} 个标签：{labels}。
候选树结构如下：
{candidate_trees}

我已秘密选择了一棵有根有向树作为真实结构，该树从根节点 A 出发，每个节点可能有零个或多个直系子节点。

你的目标是通过查询推断出这棵真实树的完整结构，并最终给出：
1. 真实树的编号（T1, T2, T3 或 T4）
2. 节点 C 的全部直系子节点列表（按字母序排列）

你可以反复向我提出以下三类查询（每次仅限一个查询），我会根据真实树如实回答：

1. 子列表查询：询问某个节点的全部直系子节点。我会返回按字母序排序的列表，如果该节点没有子节点则返回空列表。
2. 子数查询：询问某个节点的直系子节点数量。我会返回一个非负整数。
3. 成员判定：询问某个节点 Y 是否为节点 X 的直系子节点。我会回答"是"或"否"。

当你确定答案后，请提交最终结论。若答案错误或格式不符，游戏失败。

每次只能提交一个查询标签。请使用以下 XML 格式：

- 子列表查询（例如查询节点 A 的子节点）：
<query_children>A</query_children>

- 子数查询（例如查询节点 B 的子节点数量）：
<query_count>B</query_count>

- 成员判定（例如询问 C 是否为 A 的直系子节点）：
<query_member>A,C</query_member>

提交最终答案时，必须说明真实树的编号和节点 C 的直系子节点列表（用逗号隔开，按字母序排列），格式如下：

<answer>tree=T1, children_of_C=G</answer>

请尽可能用少的查询次数完成推理。
"""

    game_rule_en = """\
Let's play a "Structure Identification" deduction game. Here are the rules:

The game defines a set of {n} labels: {labels}.
Candidate tree structures are as follows:
{candidate_trees}

I have secretly chosen a rooted directed tree as the true structure. The tree starts from root node A, and each node may have zero or more direct children.

Your goal is to infer the complete structure of the true tree through queries, and finally provide:
1. The ID of the true tree (T1, T2, T3, or T4)
2. The complete list of direct children of node C (sorted alphabetically)

You can repeatedly ask me three types of queries (one query per turn), and I will answer truthfully based on the true tree:

1. Children Query: Ask for all direct children of a node. I will return a list sorted alphabetically, or an empty list if the node has no children.
2. Count Query: Ask for the number of direct children of a node. I will return a non-negative integer.
3. Membership Query: Ask whether node Y is a direct child of node X. I will answer "Yes" or "No".

When you are confident about your answer, submit your final conclusion. If the answer is wrong or the format is invalid, the game fails.

Each turn you can submit only one query tag. Use the following XML format:

- Children Query (e.g., query children of node A):
<query_children>A</query_children>

- Count Query (e.g., query the number of children of node B):
<query_count>B</query_count>

- Membership Query (e.g., ask if C is a direct child of A):
<query_member>A,C</query_member>

When submitting the final answer, you must specify the true tree ID and the direct children list of node C (comma-separated, sorted alphabetically), using this format:

<answer>tree=T1, children_of_C=G</answer>

Please complete the reasoning with as few queries as possible.
"""

    contextualized_rule_zh_1 = """\
欢迎进入“交通调度层级辨识系统”。

系统已载入当前区域的公共交通网络，包含 {n} 个调度节点：{labels}。
候选系统架构如下：
{candidate_trees}

经核实，该指挥网络是一棵严格的有根有向层级树，总指挥中心为 A，每个调度中心可能直接管辖零个或多个直属下级节点。

你的任务是通过系统交互查询，推断出完整的调度拓扑结构，并最终提交：
1. 真实网络架构的系统编号（T1, T2, T3 或 T4）
2. 区域中心 C 直接管辖的所有下级节点列表（按字母序排列）

你可以反复提交以下三类查询指令（每次仅限一条），系统将基于真实网络如实返回：

1. 子列表查询：查询某中心的所有直属下级节点。系统返回按字母序排列的列表，若无则返回空列表。
2. 子数查询：查询某中心的直属下级节点数量。系统返回一个非负整数。
3. 成员判定：查询节点 Y 是否为节点 X 的直属下级。系统回答"是"或"否"。

当你确信掌握了完整结构后，请提交最终结论。若答案错误或格式不符，排查任务失败。

每次只能提交一个查询标签。请严格使用以下 XML 格式：

- 子列表查询（例如查询中心 A 的下级）：
<query_children>A</query_children>

- 子数查询（例如查询中心 B 的下级数量）：
<query_count>B</query_count>

- 成员判定（例如询问中心 C 是否为 A 的直属下级）：
<query_member>A,C</query_member>

提交最终答案时，必须说明真实网络的编号和中心 C 的直属下级列表（用逗号隔开，按字母序排列），格式如下：

<answer>tree=T1, children_of_C=G</answer>

请尽可能以最少的查询次数完成架构排查。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Transit Dispatch Hierarchy Identification System."

The system has loaded the public transit network for the current region, comprising {n} dispatch nodes: {labels}.
Candidate system architectures are as follows:
{candidate_trees}

It has been verified that the command network forms a strict rooted directed tree. The Main Dispatch Center is A, and each center may directly control zero or more subordinate nodes.

Your task is to infer the complete dispatch topology through interactive queries and ultimately submit:
1. The system ID of the true network architecture (T1, T2, T3, or T4)
2. The complete list of subordinate nodes directly controlled by Regional Center C (sorted alphabetically)

You can repeatedly submit the following three types of queries (one per turn), and the system will answer truthfully based on the actual network:

1. Children Query: Ask for all direct subordinate nodes of a center. The system returns an alphabetically sorted list, or an empty list if there are none.
2. Count Query: Ask for the number of direct subordinate nodes of a center. The system returns a non-negative integer.
3. Membership Query: Ask whether node Y is a direct subordinate of node X. The system will answer "Yes" or "No".

Once you have determined the correct architecture, please submit your final conclusion. If the answer is incorrect or the format is invalid, the investigation fails.

Submit only one query tag per turn. Please strictly use the following XML format:

- Children Query (e.g., query subordinates of Center A):
<query_children>A</query_children>

- Count Query (e.g., query the number of subordinates of Center B):
<query_count>B</query_count>

- Membership Query (e.g., ask if Center C is a direct subordinate of Center A):
<query_member>A,C</query_member>

When submitting the final answer, you must specify the true network ID and the list of Center C's direct subordinates (comma-separated, sorted alphabetically), using this format:

<answer>tree=T1, children_of_C=G</answer>

Please complete the architecture investigation with as few queries as possible.
"""

    contextualized_rule_zh_2 = """\
欢迎使用“病毒传播链溯源系统”。

系统已锁定本次疫情的关联网络，包含 {n} 个确诊病例：{labels}。
候选传播链结构如下：
{candidate_trees}

流调数据显示，该传播链是一棵有根有向树，零号病人为 A，每个病例可能直接感染了零个或多个下属病例。

你的任务是通过系统核查推断出完整的传播链结构，并最终提交：
1. 真实传播链的溯源编号（T1, T2, T3 或 T4）
2. 病例 C 直接感染的所有病例列表（按字母序排列）

你可以反复向系统提出以下三类流调查询（每次仅限一个查询），系统会如实返回数据：

1. 子列表查询：查询某病例直接感染的所有病例。系统返回按字母序排列的列表，若无则返回空列表。
2. 子数查询：查询某病例直接感染的人数。系统返回一个非负整数。
3. 成员判定：查询病例 Y 是否由病例 X 直接感染。系统回答"是"或"否"。

当你确信掌握了完整传播链后，请提交最终结论。若答案错误或格式不符，溯源任务失败。

每次只能提交一个查询标签。请使用以下 XML 格式：

- 子列表查询（例如查询病例 A 的直接感染者）：
<query_children>A</query_children>

- 子数查询（例如查询病例 B 传染的人数）：
<query_count>B</query_count>

- 成员判定（例如询问病例 C 是否由病例 A 直接感染）：
<query_member>A,C</query_member>

提交最终答案时，必须说明真实传播链编号和病例 C 直接感染的病例列表（用逗号隔开，按字母序排列），格式如下：

<answer>tree=T1, children_of_C=G</answer>

请尽可能以最少的查询次数完成流调溯源。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Virus Transmission Chain Tracing System."

The system has mapped the infection network for the current outbreak, containing {n} confirmed cases: {labels}.
Candidate transmission chain structures are as follows:
{candidate_trees}

Epidemiological data shows that this transmission chain is a rooted directed tree. Patient Zero is A, and each patient may have directly infected zero or more subsequent cases.

Your task is to infer the complete structure of the transmission chain through queries and ultimately submit:
1. The exact ID of the true transmission chain (T1, T2, T3, or T4)
2. The complete list of cases directly infected by Case C (sorted alphabetically)

You can repeatedly submit the following three types of epidemiological queries (one per turn), and the system will answer truthfully:

1. Children Query: Ask for all cases directly infected by a specific patient. The system returns an alphabetically sorted list, or an empty list if there are none.
2. Count Query: Ask for the number of people directly infected by a patient. The system returns a non-negative integer.
3. Membership Query: Ask whether Case Y was directly infected by Case X. The system will answer "Yes" or "No".

Once you are confident about the complete chain, submit your final conclusion. If the answer is incorrect or the format is invalid, the tracing task fails.

Submit only one query tag per turn. Please use the following XML format:

- Children Query (e.g., query direct infectees of Case A):
<query_children>A</query_children>

- Count Query (e.g., query the number of infections caused by Case B):
<query_count>B</query_count>

- Membership Query (e.g., ask if Case C was directly infected by Case A):
<query_member>A,C</query_member>

When submitting the final answer, you must specify the true transmission chain ID and the list of Case C's direct infectees (comma-separated, sorted alphabetically), using this format:

<answer>tree=T1, children_of_C=G</answer>

Please complete the epidemiological tracing with as few queries as possible.
"""

    contextualized_rule_zh_3 = """\
欢迎访问“学术传承关系分析库”。

数据库当前载入了一个学派网络，包含 {n} 名学者：{labels}。
候选学术树结构如下：
{candidate_trees}

经考证，该学术传承图谱呈现严格的有根有向树结构，该学派的学术泰斗（祖师爷）为 A，每位导师可能直接指导零个或多个博士生。

你的目标是通过检索引擎推断出该学派完整的师承树，并最终给出：
1. 真实学术树的归档编号（T1, T2, T3 或 T4）
2. 导师 C 直接指导的所有博士生列表（按字母序排列）

你可以反复调用以下三类检索指令（每次仅限一条），系统将基于真实史料如实返回：

1. 子列表查询：检索某位导师名下直接指导的所有学生。系统返回按字母序排列的列表，若无则返回空列表。
2. 子数查询：检索某位导师直接指导的学生总数。系统返回一个非负整数。
3. 成员判定：检索学者 Y 是否为学者 X 直接指导的学生。系统回答"是"或"否"。

当你确信还原了完整的学术树后，请提交最终结论。若答案错误或格式不符，考证任务失败。

每次只能提交一个查询标签。请严格遵循以下 XML 格式：

- 子列表查询（例如查询导师 A 的所有直属学生）：
<query_children>A</query_children>

- 子数查询（例如查询导师 B 的学生数量）：
<query_count>B</query_count>

- 成员判定（例如询问学者 C 是否为导师 A 的直属学生）：
<query_member>A,C</query_member>

提交最终答案时，必须说明真实学术树的编号和导师 C 直接指导的学生列表（用逗号隔开，按字母序排列），格式如下：

<answer>tree=T1, children_of_C=G</answer>

请尽可能用最少的检索次数完成学术考证。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Academic Lineage Analysis Database."

The database has loaded an academic school network containing {n} scholars: {labels}.
Candidate academic tree structures are as follows:
{candidate_trees}

Historical research confirms that this lineage forms a strict rooted directed tree. The founding academic (Dean) is A, and each supervisor may have directly mentored zero or more PhD students.

Your goal is to infer the complete mentorship tree of this school through queries and ultimately provide:
1. The archive ID of the true academic tree (T1, T2, T3, or T4)
2. The complete list of PhD students directly supervised by Professor C (sorted alphabetically)

You can repeatedly execute the following three types of queries (one per turn), and the system will return factual historical data:

1. Children Query: Ask for all direct students supervised by a scholar. The system returns an alphabetically sorted list, or an empty list if there are none.
2. Count Query: Ask for the total number of direct students supervised by a scholar. The system returns a non-negative integer.
3. Membership Query: Ask whether Scholar Y is a direct student of Scholar X. The system will answer "Yes" or "No".

Once you have reconstructed the complete tree, submit your final conclusion. If the answer is incorrect or the format is invalid, the research task fails.

Submit only one query tag per turn. Please strictly use the following XML format:

- Children Query (e.g., query direct students of Professor A):
<query_children>A</query_children>

- Count Query (e.g., query the number of students of Professor B):
<query_count>B</query_count>

- Membership Query (e.g., ask if Scholar C is a direct student of Professor A):
<query_member>A,C</query_member>

When submitting the final answer, you must specify the true academic tree ID and the list of Professor C's direct students (comma-separated, sorted alphabetically), using this format:

<answer>tree=T1, children_of_C=G</answer>

Please complete the lineage verification with as few queries as possible.
"""

    contextualized_rule_zh_4 = """\
欢迎进入“产品物料清单(BOM)解析仪”。

系统已读取该型装备的装配组件库，包含 {n} 个关键组件/模块：{labels}。
候选BOM图谱版本如下：
{candidate_trees}

工程设计表明，该装备的BOM构成一棵有根有向树，最终成品总成定为 A，每个组件可能由零个或多个直接子组件拼装而成。

你的任务是通过系统诊断推断出完整的装配层级，并最终提交：
1. 真实BOM图谱的版本编号（T1, T2, T3 或 T4）
2. 模块 C 所包含的所有直接子组件列表（按字母序排列）

你可以反复向解析仪输入以下三类探测指令（每次仅限一条），仪器将如实返回结构参数：

1. 子列表查询：探测某组件包含的所有直接子组件。系统返回按字母序排列的列表，若该组件为最底层零件则返回空列表。
2. 子数查询：探测某组件包含的直接子组件数量。系统返回一个非负整数。
3. 成员判定：探测组件 Y 是否直接拼装于组件 X 之中。系统回答"是"或"否"。

当你确信解析出完整的BOM结构后，请提交最终报告。若答案错误或格式不符，解析作业失败。

每次只能提交一个查询标签。请使用以下 XML 格式：

- 子列表查询（例如查询成品 A 的直接子组件）：
<query_children>A</query_children>

- 子数查询（例如查询模块 B 的直接子组件数量）：
<query_count>B</query_count>

- 成员判定（例如询问组件 C 是否为成品 A 的直接子组件）：
<query_member>A,C</query_member>

提交最终答案时，必须说明真实BOM的版本编号和模块 C 的直接子组件列表（用逗号隔开，按字母序排列），格式如下：

<answer>tree=T1, children_of_C=G</answer>

请尽可能以最少的探测指令完成结构解析。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Product Bill of Materials (BOM) Analyzer."

The system has loaded the assembly components for this equipment, containing {n} key modules/parts: {labels}.
Candidate BOM structures are as follows:
{candidate_trees}

Engineering designs indicate that this BOM forms a rooted directed tree. The Final Product is A, and each module may be directly composed of zero or more sub-components.

Your task is to infer the complete assembly hierarchy through system diagnostics and ultimately submit:
1. The version ID of the true BOM structure (T1, T2, T3, or T4)
2. The complete list of direct sub-components that make up Module C (sorted alphabetically)

You can repeatedly input the following three types of diagnostic probes (one per turn), and the analyzer will return accurate structural parameters:

1. Children Query: Ask for all direct sub-components of a given module. The system returns an alphabetically sorted list, or an empty list if it is a base part.
2. Count Query: Ask for the number of direct sub-components comprising a module. The system returns a non-negative integer.
3. Membership Query: Ask whether Component Y is directly assembled into Component X. The system will answer "Yes" or "No".

Once you have successfully parsed the complete BOM, submit your final report. If the answer is incorrect or the format is invalid, the analysis fails.

Submit only one query tag per turn. Please use the following XML format:

- Children Query (e.g., query direct sub-components of Final Product A):
<query_children>A</query_children>

- Count Query (e.g., query the number of sub-components of Module B):
<query_count>B</query_count>

- Membership Query (e.g., ask if Component C is a direct sub-component of Final Product A):
<query_member>A,C</query_member>

When submitting the final answer, you must specify the true BOM version ID and the list of Module C's direct sub-components (comma-separated, sorted alphabetically), using this format:

<answer>tree=T1, children_of_C=G</answer>

Please complete the structural analysis with as few probes as possible.
"""

    contextualized_rule_zh_5 = """\
欢迎启动“企业股权穿透核查系统”。

核查库当前锁定了一个庞大的商业帝国，包含 {n} 个法人实体：{labels}。
候选股权架构如下：
{candidate_trees}

工商穿透数据确认，该财团的控制架构是一棵有根有向树，绝对控股母公司为 A，每个公司可能直接全资控股零个或多个子公司。

你的任务是通过工商调档推断出该财团真实的资本迷宫，并最终出具：
1. 真实股权架构的备案编号（T1, T2, T3 或 T4）
2. 公司 C 直接全资控股的所有子公司列表（按字母序排列）

你可以反复调用以下三类查档接口（每次仅限一次调用），系统将基于真实工商数据如实反馈：

1. 子列表查询：调取某公司名下直接全资控股的所有子公司。系统返回按字母序排列的列表，若无子公司则返回空列表。
2. 子数查询：调取某公司直接控股的子公司数量。系统返回一个非负整数。
3. 成员判定：核查公司 Y 是否为公司 X 的直接控股子公司。系统回答"是"或"否"。

当你确信理清了整个控股架构后，请提交最终结论。若核实错误或报告格式不符，穿透核查失败。

每次只能提交一个查询标签。请严格使用以下 XML 格式：

- 子列表查询（例如查询母公司 A 的直接子公司）：
<query_children>A</query_children>

- 子数查询（例如查询公司 B 的直接子公司数量）：
<query_count>B</query_count>

- 成员判定（例如询问公司 C 是否为母公司 A 的直接子公司）：
<query_member>A,C</query_member>

提交最终答案时，必须说明真实架构的备案编号和公司 C 的直接子公司列表（用逗号隔开，按字母序排列），格式如下：

<answer>tree=T1, children_of_C=G</answer>

请尽可能以最少的查档次数完成股权穿透任务。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Corporate Equity Penetration Audit System."

The audit database has isolated a massive corporate conglomerate containing {n} legal entities: {labels}.
Candidate corporate equity structures are as follows:
{candidate_trees}

Penetration data confirms that the control architecture of this syndicate is a rooted directed tree. The Ultimate Parent Company is A, and each company may directly own/control zero or more subsidiaries.

Your task is to infer the true capital labyrinth of the syndicate through corporate record retrieval and ultimately issue:
1. The filing ID of the true corporate equity structure (T1, T2, T3, or T4)
2. The complete list of direct subsidiaries wholly owned by Holding Company C (sorted alphabetically)

You can repeatedly call the following three types of record retrieval interfaces (one call per turn), and the system will provide accurate corporate registry data:

1. Children Query: Retrieve all direct subsidiaries owned by a specific company. The system returns an alphabetically sorted list, or an empty list if there are none.
2. Count Query: Retrieve the number of direct subsidiaries owned by a specific company. The system returns a non-negative integer.
3. Membership Query: Audit whether Company Y is a direct subsidiary of Company X. The system will answer "Yes" or "No".

Once you are confident you have unravelled the entire ownership structure, submit your final conclusion. If the audit is incorrect or the report format is invalid, the penetration check fails.

Submit only one query tag per turn. Please strictly use the following XML format:

- Children Query (e.g., query direct subsidiaries of Parent Company A):
<query_children>A</query_children>

- Count Query (e.g., query the number of subsidiaries of Company B):
<query_count>B</query_count>

- Membership Query (e.g., ask if Company C is a direct subsidiary of Parent Company A):
<query_member>A,C</query_member>

When submitting the final answer, you must specify the true structure filing ID and the list of Company C's direct subsidiaries (comma-separated, sorted alphabetically), using this format:

<answer>tree=T1, children_of_C=G</answer>

Please complete the equity penetration audit with as few record retrievals as possible.
"""

    tags = ["answer", "query_children", "query_count", "query_member"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 10,
                "labels": "A, B, C, D, E, F, G, H, I, J",
                "tree_id": "T1",
                "tree_structure": {
                    "A": ["B", "C", "D"],
                    "B": ["E", "F"],
                    "C": ["G"],
                    "D": ["H", "I"],
                    "G": ["J"],
                    "E": [], "F": [], "H": [], "I": [], "J": []
                }
            },
            2: {
                "n": 10,
                "labels": "A, B, C, D, E, F, G, H, I, J",
                "tree_id": "T2",
                "tree_structure": {
                    "A": ["B", "C", "D"],
                    "B": ["E"],
                    "C": ["F", "G"],
                    "D": ["H"],
                    "F": ["I"],
                    "H": ["J"],
                    "E": [], "G": [], "I": [], "J": []
                }
            },
            3: {
                "n": 10,
                "labels": "A, B, C, D, E, F, G, H, I, J",
                "tree_id": "T3",
                "tree_structure": {
                    "A": ["B", "C"],
                    "B": ["D", "E"],
                    "C": ["F", "G"],
                    "D": ["H"],
                    "E": ["I"],
                    "F": [],
                    "G": ["J"],
                    "H": [], "I": [], "J": []
                }
            },
            4: {
                "n": 10,
                "labels": "A, B, C, D, E, F, G, H, I, J",
                "tree_id": "T4",
                "tree_structure": {
                    "A": ["B"],
                    "B": ["C", "D", "E"],
                    "C": ["F", "G"],
                    "D": ["H"],
                    "E": ["I"],
                    "F": [],
                    "G": ["J"],
                    "H": [], "I": [], "J": []
                }
            },
            5: {
                "n": 10,
                "labels": "A, B, C, D, E, F, G, H, I, J",
                "tree_id": "T1",
                "tree_structure": {
                    "A": ["B", "C", "D"],
                    "B": ["E"],
                    "C": ["F", "G"],
                    "D": ["H", "I"],
                    "E": ["J"],
                    "F": [], "G": [], "H": [], "I": [], "J": []
                }
            },
        },
        "en": {
            1: {
                "n": 10,
                "labels": "A, B, C, D, E, F, G, H, I, J",
                "tree_id": "T1",
                "tree_structure": {
                    "A": ["B", "C", "D"],
                    "B": ["E", "F"],
                    "C": ["G"],
                    "D": ["H", "I"],
                    "G": ["J"],
                    "E": [], "F": [], "H": [], "I": [], "J": []
                }
            },
            2: {
                "n": 10,
                "labels": "A, B, C, D, E, F, G, H, I, J",
                "tree_id": "T2",
                "tree_structure": {
                    "A": ["B", "C", "D"],
                    "B": ["E"],
                    "C": ["F", "G"],
                    "D": ["H"],
                    "F": ["I"],
                    "H": ["J"],
                    "E": [], "G": [], "I": [], "J": []
                }
            },
            3: {
                "n": 10,
                "labels": "A, B, C, D, E, F, G, H, I, J",
                "tree_id": "T3",
                "tree_structure": {
                    "A": ["B", "C"],
                    "B": ["D", "E"],
                    "C": ["F", "G"],
                    "D": ["H"],
                    "E": ["I"],
                    "F": [],
                    "G": ["J"],
                    "H": [], "I": [], "J": []
                }
            },
            4: {
                "n": 10,
                "labels": "A, B, C, D, E, F, G, H, I, J",
                "tree_id": "T4",
                "tree_structure": {
                    "A": ["B"],
                    "B": ["C", "D", "E"],
                    "C": ["F", "G"],
                    "D": ["H"],
                    "E": ["I"],
                    "F": [],
                    "G": ["J"],
                    "H": [], "I": [], "J": []
                }
            },
            5: {
                "n": 10,
                "labels": "A, B, C, D, E, F, G, H, I, J",
                "tree_id": "T1",
                "tree_structure": {
                    "A": ["B", "C", "D"],
                    "B": ["E"],
                    "C": ["F", "G"],
                    "D": ["H", "I"],
                    "E": ["J"],
                    "F": [], "G": [], "H": [], "I": [], "J": []
                }
            },
        }
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty
        
        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self._game_info["n"] = cfg["n"]
        self._game_info["labels"] = cfg["labels"]
        
        candidate_descriptions = []
        for tid_num in range(1, 5):
            tid = f"T{tid_num}"
            for d, dcfg in self.DIFFICULTY_CONFIG[lang].items():
                if dcfg["tree_id"] == tid:
                    tree_desc = "; ".join(
                        f"{node} -> [{', '.join(children)}]" if children else f"{node} -> []"
                        for node, children in sorted(dcfg["tree_structure"].items())
                    )
                    candidate_descriptions.append(f"{tid}: {tree_desc}")
                    break
        
        self._game_info["candidate_trees"] = "\n".join(candidate_descriptions)
        
        self.true_tree_id = cfg["tree_id"]
        self.tree_structure = cfg["tree_structure"]

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        import re
        
        ans_dict = {}
        
        tree_match = re.search(r'tree\s*=\s*(\S+)', raw_ans)
        if tree_match:
            tree_val = tree_match.group(1).rstrip(',').strip()
            ans_dict["tree"] = tree_val
        
        children_match = re.search(r'children_of_C\s*=\s*(.*)', raw_ans)
        if children_match:
            ans_dict["children_of_C"] = children_match.group(1).strip()
        
        if "tree" not in ans_dict or "children_of_C" not in ans_dict:
            return False
        
        if ans_dict["tree"] != self.true_tree_id:
            return False
        
        try:
            true_children_of_c = sorted(self.tree_structure.get("C", []))
            
            model_children_str = ans_dict["children_of_C"].strip()
            if model_children_str == "":
                model_children = []
            else:
                model_children = sorted([x.strip() for x in model_children_str.split(",") if x.strip()])
            
            return model_children == true_children_of_c
            
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_invalid_node = "错误：节点不存在。"
            error_invalid_format = "错误：格式无效。"
        else:
            yes_res, no_res = "Yes", "No"
            error_invalid_node = "Error: Node does not exist."
            error_invalid_format = "Error: Invalid format."

        if "query_children" in parsed_info:
            node = parsed_info["query_children"].strip().upper()
            
            if node not in self.tree_structure:
                return error_invalid_node
            
            children = self.tree_structure[node]
            if not children:
                return "[]"
            else:
                return "[" + ", ".join(children) + "]"

        elif "query_count" in parsed_info:
            node = parsed_info["query_count"].strip().upper()
            
            if node not in self.tree_structure:
                return error_invalid_node
            
            count = len(self.tree_structure[node])
            return str(count)

        elif "query_member" in parsed_info:
            try:
                raw = parsed_info["query_member"]
                parts = [x.strip().upper() for x in raw.split(",")]
                
                if len(parts) != 2:
                    return error_invalid_format
                
                parent, child = parts[0], parts[1]
                
                if parent not in self.tree_structure or child not in self.tree_structure:
                    return error_invalid_node
                
                is_child = child in self.tree_structure[parent]
                return yes_res if is_child else no_res
                
            except:
                return error_invalid_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            val = int(correct)
            return str(val + 1) if val > 0 else "1"
        
        if self.config.language == "zh":
            if correct == "是": return "否"
            if correct == "否": return "是"
        else:
            lower_c = correct.lower()
            if lower_c == "yes": return "No"
            if lower_c == "no": return "Yes"
        
        if correct.startswith("[") and correct.endswith("]"):
            inner = correct[1:-1].strip()
            if inner == "":
                return "[Z]"
            else:
                items = [x.strip() for x in inner.split(",") if x.strip()]
                if len(items) > 1:
                    return "[" + ", ".join(items[:-1]) + "]"
                else:
                    all_labels = list(self.tree_structure.keys())
                    for label in all_labels:
                        if label != items[0]:
                            return "[" + label + "]"
                    return "[]"
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        raw_labels = self._game_info.get("labels", "")
        labels = [x.strip() for x in raw_labels.split(",") if x.strip()]
        
        for node in labels:
            parsed_info = {"query_children": node}
            answer = self._cf_core_produce(parsed_info)
            queries.append({
                "query": f"<query_children>{node}</query_children>",
                "answer": answer
            })
            
        for node in labels:
            parsed_info = {"query_count": node}
            answer = self._cf_core_produce(parsed_info)
            queries.append({
                "query": f"<query_count>{node}</query_count>",
                "answer": answer
            })
            
        for parent in labels:
            for child in labels:
                content = f"{parent},{child}"
                parsed_info = {"query_member": content}
                answer = self._cf_core_produce(parsed_info)
                queries.append({
                    "query": f"<query_member>{content}</query_member>",
                    "answer": answer
                })
                
        return queries