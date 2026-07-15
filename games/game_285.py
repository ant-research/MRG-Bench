from .base import Game

class PartitionDeductionGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "集合"
    enable_counterfactual = False

    game_rule_zh = """\
我们来玩一个"二分划分推理"游戏，规则如下：

游戏设定了一个包含 8 个元素的集合 S = {{A, B, C, D, E, F, G, H}}。

系统已秘密选定了唯一的一个二分划分方案（将 8 个元素分为两组，每组 4 个元素）。你的目标是推断出这个划分方案，并正确判断元素 B 与 C 是否在同一组。

你可以反复向我提出以下两类问题（每次仅限一个问题）：

1. 同类判定查询：询问任意两个不同的元素 X 和 Y 是否在同一组。我会回答"同类"或"异类"。注意：此类查询次数有限制，请尽可能高效地使用。

2. 剩余可能性查询：询问当前仍有多少种划分方案与已有信息一致。我会回答一个非负整数。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 同类判定查询（例如询问 A 和 B）：
<query_pair>A,B</query_pair>

- 剩余可能性查询（内容为空）：
<query_remaining></query_remaining>

提交最终答案时，必须说明划分方案编号（partition_id）以及 B 与 C 的关系（same_group 为 true 或 false），格式如下：

<answer>partition_id={{partition_id}}, same_group={{same_group}}</answer>

其中 partition_id 为整数（{partition_id_range}），same_group 为 true 或 false。
"""

    game_rule_en = """\
Let's play a "Partition Deduction" game. Here are the rules:

The game uses a set S = {{A, B, C, D, E, F, G, H}} containing 8 elements.

The system has secretly selected a unique binary partition (dividing the 8 elements into two groups of 4 elements each). Your goal is to deduce this partition and correctly determine whether elements B and C are in the same group.

You can repeatedly ask me the following two types of questions (one per turn):

1. Pair Query: Ask whether any two distinct elements X and Y are in the same group. I will answer "same" or "different". Note: This type of query has a limited number of uses, so please use them efficiently.

2. Remaining Possibilities Query: Ask how many partition schemes are still consistent with the information obtained so far. I will answer with a non-negative integer.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Pair Query (e.g., asking about A and B):
<query_pair>A,B</query_pair>

- Remaining Possibilities Query (empty content):
<query_remaining></query_remaining>

When submitting the final answer, specify the partition ID (partition_id) and the relationship between B and C (same_group as true or false), using this format:

<answer>partition_id={{partition_id}}, same_group={{same_group}}</answer>

Where partition_id is an integer ({partition_id_range}), and same_group is either true or false.
"""

    contextualized_rule_zh_1 = """\
[交通场景]
我们来协助进行"交通网络规划分析"，规则如下：

城市规划局选定了包含 8 个交通枢纽的集合 S = {{A, B, C, D, E, F, G, H}}。

系统已秘密制定了唯一的一个交通网络二分规划方案（将 8 个枢纽分为两个独立运营的交通网络，每个网络包含 4 个枢纽）。你的目标是推断出这个规划方案，并正确判断枢纽 B 与 C 是否属于同一交通网络。

你可以反复向我提出以下两类问题（每次仅限一个问题）：

1. 同网络判定查询：询问任意两个不同的枢纽 X 和 Y 是否在同一网络。我会回答"同类"或"异类"。注意：此类查询次数有限制，请尽可能高效地使用。

2. 剩余可能性查询：询问当前仍有多少种规划方案与已有信息一致。我会回答一个非负整数。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，分析失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 同网络判定查询（例如询问枢纽 A 和 B）：
<query_pair>A,B</query_pair>

- 剩余可能性查询（内容为空）：
<query_remaining></query_remaining>

提交最终答案时，必须说明规划方案编号（partition_id）以及枢纽 B 与 C 的关系（same_group 为 true 或 false），格式如下：

<answer>partition_id={{partition_id}}, same_group={{same_group}}</answer>

其中 partition_id 为整数（{partition_id_range}），same_group 为 true 或 false。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's assist with a "Transit Network Planning Analysis". Here are the rules:

The city planning bureau has selected a set of 8 traffic hubs S = {{A, B, C, D, E, F, G, H}}.

The system has secretly devised a unique binary transit planning scheme (dividing the 8 hubs into two independently operated transit networks, each containing 4 hubs). Your goal is to deduce this planning scheme and correctly determine whether hubs B and C belong to the same transit network.

You can repeatedly ask me the following two types of questions (one per turn):

1. Same-Network Query: Ask whether any two distinct hubs X and Y are in the same network. I will answer "same" or "different". Note: This type of query has a limited number of uses, so please use them efficiently.

2. Remaining Possibilities Query: Ask how many planning schemes are still consistent with the information obtained so far. I will answer with a non-negative integer.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the analysis fails.

Each query must contain only one tag. Use the following XML format:

- Same-Network Query (e.g., asking about hubs A and B):
<query_pair>A,B</query_pair>

- Remaining Possibilities Query (empty content):
<query_remaining></query_remaining>

When submitting the final answer, specify the planning scheme ID (partition_id) and the relationship between hubs B and C (same_group as true or false), using this format:

<answer>partition_id={{partition_id}}, same_group={{same_group}}</answer>

Where partition_id is an integer ({partition_id_range}), and same_group is either true or false.
"""

    contextualized_rule_zh_2 = """\
[医疗场景]
我们来进行"临床试验分组分析"，规则如下：

研究团队选定了包含 8 名参与试验患者的集合 S = {{A, B, C, D, E, F, G, H}}。

系统已秘密制定了唯一的一个患者二分盲测方案（将 8 名患者分为两个对照组，每组 4 名患者）。你的目标是推断出这个分组方案，并正确判断患者 B 与 C 是否在同一个对照组。

你可以反复向我提出以下两类问题（每次仅限一个问题）：

1. 同组判定查询：询问任意两名不同的患者 X 和 Y 是否在同一组。我会回答"同类"或"异类"。注意：此类查询次数有限制，请尽可能高效地使用。

2. 剩余可能性查询：询问当前仍有多少种分组方案与已有信息一致。我会回答一个非负整数。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，分析失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 同组判定查询（例如询问患者 A 和 B）：
<query_pair>A,B</query_pair>

- 剩余可能性查询（内容为空）：
<query_remaining></query_remaining>

提交最终答案时，必须说明分组方案编号（partition_id）以及患者 B 与 C 的关系（same_group 为 true 或 false），格式如下：

<answer>partition_id={{partition_id}}, same_group={{same_group}}</answer>

其中 partition_id 为整数（{partition_id_range}），same_group 为 true 或 false。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct a "Clinical Trial Grouping Analysis". Here are the rules:

The research team has selected a set of 8 trial patients S = {{A, B, C, D, E, F, G, H}}.

The system has secretly devised a unique binary blind-test scheme (dividing the 8 patients into two control groups, each with 4 patients). Your goal is to deduce this grouping scheme and correctly determine whether patients B and C are in the same control group.

You can repeatedly ask me the following two types of questions (one per turn):

1. Same-Group Query: Ask whether any two distinct patients X and Y are in the same group. I will answer "same" or "different". Note: This type of query has a limited number of uses, so please use them efficiently.

2. Remaining Possibilities Query: Ask how many grouping schemes are still consistent with the information obtained so far. I will answer with a non-negative integer.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the analysis fails.

Each query must contain only one tag. Use the following XML format:

- Same-Group Query (e.g., asking about patients A and B):
<query_pair>A,B</query_pair>

- Remaining Possibilities Query (empty content):
<query_remaining></query_remaining>

When submitting the final answer, specify the grouping scheme ID (partition_id) and the relationship between patients B and C (same_group as true or false), using this format:

<answer>partition_id={{partition_id}}, same_group={{same_group}}</answer>

Where partition_id is an integer ({partition_id_range}), and same_group is either true or false.
"""

    contextualized_rule_zh_3 = """\
[教育场景]
我们来协助进行"学科竞赛队伍组建分析"，规则如下：

学校选定了包含 8 名候选学生的集合 S = {{A, B, C, D, E, F, G, H}}。

系统已秘密制定了唯一的一个竞赛队伍二分编排方案（将 8 名学生分为两支参赛队伍，每队 4 名学生）。你的目标是推断出这个编排方案，并正确判断学生 B 与 C 是否属于同一支队伍。

你可以反复向我提出以下两类问题（每次仅限一个问题）：

1. 同队判定查询：询问任意两名不同的学生 X 和 Y 是否在同一队伍。我会回答"同类"或"异类"。注意：此类查询次数有限制，请尽可能高效地使用。

2. 剩余可能性查询：询问当前仍有多少种编排方案与已有信息一致。我会回答一个非负整数。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，分析失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 同队判定查询（例如询问学生 A 和 B）：
<query_pair>A,B</query_pair>

- 剩余可能性查询（内容为空）：
<query_remaining></query_remaining>

提交最终答案时，必须说明编排方案编号（partition_id）以及学生 B 与 C 的关系（same_group 为 true 或 false），格式如下：

<answer>partition_id={{partition_id}}, same_group={{same_group}}</answer>

其中 partition_id 为整数（{partition_id_range}），same_group 为 true 或 false。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's assist with an "Academic Competition Team Formation Analysis". Here are the rules:

The school has selected a set of 8 candidate students S = {{A, B, C, D, E, F, G, H}}.

The system has secretly devised a unique binary team arrangement scheme (dividing the 8 students into two competing teams, each with 4 students). Your goal is to deduce this arrangement scheme and correctly determine whether students B and C belong to the same team.

You can repeatedly ask me the following two types of questions (one per turn):

1. Same-Team Query: Ask whether any two distinct students X and Y are in the same team. I will answer "same" or "different". Note: This type of query has a limited number of uses, so please use them efficiently.

2. Remaining Possibilities Query: Ask how many arrangement schemes are still consistent with the information obtained so far. I will answer with a non-negative integer.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the analysis fails.

Each query must contain only one tag. Use the following XML format:

- Same-Team Query (e.g., asking about students A and B):
<query_pair>A,B</query_pair>

- Remaining Possibilities Query (empty content):
<query_remaining></query_remaining>

When submitting the final answer, specify the arrangement scheme ID (partition_id) and the relationship between students B and C (same_group as true or false), using this format:

<answer>partition_id={{partition_id}}, same_group={{same_group}}</answer>

Where partition_id is an integer ({partition_id_range}), and same_group is either true or false.
"""

    contextualized_rule_zh_4 = """\
[制造业/工业场景]
我们来进行"供电回路排查分析"，规则如下：

工厂选定了包含 8 台关键生产设备的集合 S = {{A, B, C, D, E, F, G, H}}。

系统已秘密制定了唯一的一个设备供电二分接入方案（将 8 台设备接入两个独立的供电回路，每个回路连接 4 台设备）。你的目标是推断出这个接入方案，并正确判断设备 B 与 C 是否连接在同一个回路上。

你可以反复向我提出以下两类问题（每次仅限一个问题）：

1. 同回路判定查询：询问任意两台不同的设备 X 和 Y 是否在同一供电回路。我会回答"同类"或"异类"。注意：此类查询次数有限制，请尽可能高效地使用。

2. 剩余可能性查询：询问当前仍有多少种接入方案与已有信息一致。我会回答一个非负整数。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，排查失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 同回路判定查询（例如询问设备 A 和 B）：
<query_pair>A,B</query_pair>

- 剩余可能性查询（内容为空）：
<query_remaining></query_remaining>

提交最终答案时，必须说明接入方案编号（partition_id）以及设备 B 与 C 的关系（same_group 为 true 或 false），格式如下：

<answer>partition_id={{partition_id}}, same_group={{same_group}}</answer>

其中 partition_id 为整数（{partition_id_range}），same_group 为 true 或 false。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's conduct a "Power Circuit Troubleshooting Analysis". Here are the rules:

The factory has selected a set of 8 critical production machines S = {{A, B, C, D, E, F, G, H}}.

The system has secretly devised a unique binary power connection scheme (connecting the 8 machines to two independent power circuits, each powering 4 machines). Your goal is to deduce this connection scheme and correctly determine whether machines B and C are connected to the same circuit.

You can repeatedly ask me the following two types of questions (one per turn):

1. Same-Circuit Query: Ask whether any two distinct machines X and Y are on the same power circuit. I will answer "same" or "different". Note: This type of query has a limited number of uses, so please use them efficiently.

2. Remaining Possibilities Query: Ask how many connection schemes are still consistent with the information obtained so far. I will answer with a non-negative integer.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the troubleshooting fails.

Each query must contain only one tag. Use the following XML format:

- Same-Circuit Query (e.g., asking about machines A and B):
<query_pair>A,B</query_pair>

- Remaining Possibilities Query (empty content):
<query_remaining></query_remaining>

When submitting the final answer, specify the connection scheme ID (partition_id) and the relationship between machines B and C (same_group as true or false), using this format:

<answer>partition_id={{partition_id}}, same_group={{same_group}}</answer>

Where partition_id is an integer ({partition_id_range}), and same_group is either true or false.
"""

    contextualized_rule_zh_5 = """\
[法律场景]
我们来协助进行"证据链归类分析"，规则如下：

专案组整理了包含 8 份核心证据材料的集合 S = {{A, B, C, D, E, F, G, H}}。

系统已秘密查明了唯一的一个证据二分归类方案（将 8 份证据分为两条截然不同的证据链，每条证据链包含 4 份材料）。你的目标是推断出这个归类方案，并正确判断证据 B 与 C 是否属于同一条证据链。

你可以反复向我提出以下两类问题（每次仅限一个问题）：

1. 同链判定查询：询问任意两份不同的证据 X 和 Y 是否属于同一证据链。我会回答"同类"或"异类"。注意：此类查询次数有限制，请尽可能高效地使用。

2. 剩余可能性查询：询问当前仍有多少种归类方案与已有证据信息一致。我会回答一个非负整数。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，分析失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 同链判定查询（例如询问证据 A 和 B）：
<query_pair>A,B</query_pair>

- 剩余可能性查询（内容为空）：
<query_remaining></query_remaining>

提交最终答案时，必须说明归类方案编号（partition_id）以及证据 B 与 C 的关系（same_group 为 true 或 false），格式如下：

<answer>partition_id={{partition_id}}, same_group={{same_group}}</answer>

其中 partition_id 为整数（{partition_id_range}），same_group 为 true 或 false。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's assist with an "Evidence Chain Categorization Analysis". Here are the rules:

The task force has organized a set of 8 core evidence materials S = {{A, B, C, D, E, F, G, H}}.

The system has secretly identified a unique binary categorization scheme (dividing the 8 pieces of evidence into two distinct evidence chains, each containing 4 materials). Your goal is to deduce this categorization scheme and correctly determine whether evidence B and C belong to the same evidence chain.

You can repeatedly ask me the following two types of questions (one per turn):

1. Same-Chain Query: Ask whether any two distinct pieces of evidence X and Y belong to the same evidence chain. I will answer "same" or "different". Note: This type of query has a limited number of uses, so please use them efficiently.

2. Remaining Possibilities Query: Ask how many categorization schemes are still consistent with the evidence information obtained so far. I will answer with a non-negative integer.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the analysis fails.

Each query must contain only one tag. Use the following XML format:

- Same-Chain Query (e.g., asking about evidence A and B):
<query_pair>A,B</query_pair>

- Remaining Possibilities Query (empty content):
<query_remaining></query_remaining>

When submitting the final answer, specify the categorization scheme ID (partition_id) and the relationship between evidence B and C (same_group as true or false), using this format:

<answer>partition_id={{partition_id}}, same_group={{same_group}}</answer>

Where partition_id is an integer ({partition_id_range}), and same_group is either true or false.
"""

    tags = ["answer", "query_pair", "query_remaining"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "max_queries": 6,
                "partitions": {
                    1: [["A", "C", "E", "G"], ["B", "D", "F", "H"]],
                    2: [["A", "B", "E", "F"], ["C", "D", "G", "H"]],
                    3: [["A", "B", "C", "D"], ["E", "F", "G", "H"]],
                    4: [["A", "D", "F", "G"], ["B", "C", "E", "H"]],
                },
                "true_partition_id": 2,
            },
            2: {
                "max_queries": 5,
                "partitions": {
                    1: [["A", "C", "E", "G"], ["B", "D", "F", "H"]],
                    2: [["A", "B", "E", "F"], ["C", "D", "G", "H"]],
                    3: [["A", "B", "C", "D"], ["E", "F", "G", "H"]],
                    4: [["A", "D", "F", "G"], ["B", "C", "E", "H"]],
                    5: [["A", "C", "F", "H"], ["B", "D", "E", "G"]],
                    6: [["A", "B", "G", "H"], ["C", "D", "E", "F"]],
                },
                "true_partition_id": 4,
            },
            3: {
                "max_queries": 5,
                "partitions": {
                    1: [["A", "C", "E", "G"], ["B", "D", "F", "H"]],
                    2: [["A", "B", "E", "F"], ["C", "D", "G", "H"]],
                    3: [["A", "B", "C", "D"], ["E", "F", "G", "H"]],
                    4: [["A", "D", "F", "G"], ["B", "C", "E", "H"]],
                    5: [["A", "C", "F", "H"], ["B", "D", "E", "G"]],
                    6: [["A", "B", "G", "H"], ["C", "D", "E", "F"]],
                    7: [["A", "D", "E", "H"], ["B", "C", "F", "G"]],
                    8: [["A", "C", "D", "F"], ["B", "E", "G", "H"]],
                },
                "true_partition_id": 7,
            },
            4: {
                "max_queries": 4,
                "partitions": {
                    1: [["A", "C", "E", "G"], ["B", "D", "F", "H"]],
                    2: [["A", "B", "E", "F"], ["C", "D", "G", "H"]],
                    3: [["A", "B", "C", "D"], ["E", "F", "G", "H"]],
                    4: [["A", "D", "F", "G"], ["B", "C", "E", "H"]],
                    5: [["A", "C", "F", "H"], ["B", "D", "E", "G"]],
                    6: [["A", "B", "G", "H"], ["C", "D", "E", "F"]],
                    7: [["A", "D", "E", "H"], ["B", "C", "F", "G"]],
                    8: [["A", "C", "D", "F"], ["B", "E", "G", "H"]],
                    9: [["A", "E", "F", "G"], ["B", "C", "D", "H"]],
                    10: [["A", "C", "D", "H"], ["B", "E", "F", "G"]],
                },
                "true_partition_id": 5,
            },
            5: {
                "max_queries": 4,
                "partitions": {
                    1: [["A", "C", "E", "G"], ["B", "D", "F", "H"]],
                    2: [["A", "B", "E", "F"], ["C", "D", "G", "H"]],
                    3: [["A", "B", "C", "D"], ["E", "F", "G", "H"]],
                    4: [["A", "D", "F", "G"], ["B", "C", "E", "H"]],
                    5: [["A", "C", "F", "H"], ["B", "D", "E", "G"]],
                    6: [["A", "B", "G", "H"], ["C", "D", "E", "F"]],
                    7: [["A", "D", "E", "H"], ["B", "C", "F", "G"]],
                    8: [["A", "C", "D", "F"], ["B", "E", "G", "H"]],
                    9: [["A", "E", "F", "G"], ["B", "C", "D", "H"]],
                    10: [["A", "C", "D", "H"], ["B", "E", "F", "G"]],
                    11: [["A", "B", "D", "F"], ["C", "E", "G", "H"]],
                    12: [["A", "C", "E", "H"], ["B", "D", "F", "G"]],
                },
                "true_partition_id": 11,
            },
        },
        "en": {
            1: {
                "max_queries": 6,
                "partitions": {
                    1: [["A", "C", "E", "G"], ["B", "D", "F", "H"]],
                    2: [["A", "B", "E", "F"], ["C", "D", "G", "H"]],
                    3: [["A", "B", "C", "D"], ["E", "F", "G", "H"]],
                    4: [["A", "D", "F", "G"], ["B", "C", "E", "H"]],
                },
                "true_partition_id": 2,
            },
            2: {
                "max_queries": 5,
                "partitions": {
                    1: [["A", "C", "E", "G"], ["B", "D", "F", "H"]],
                    2: [["A", "B", "E", "F"], ["C", "D", "G", "H"]],
                    3: [["A", "B", "C", "D"], ["E", "F", "G", "H"]],
                    4: [["A", "D", "F", "G"], ["B", "C", "E", "H"]],
                    5: [["A", "C", "F", "H"], ["B", "D", "E", "G"]],
                    6: [["A", "B", "G", "H"], ["C", "D", "E", "F"]],
                },
                "true_partition_id": 4,
            },
            3: {
                "max_queries": 5,
                "partitions": {
                    1: [["A", "C", "E", "G"], ["B", "D", "F", "H"]],
                    2: [["A", "B", "E", "F"], ["C", "D", "G", "H"]],
                    3: [["A", "B", "C", "D"], ["E", "F", "G", "H"]],
                    4: [["A", "D", "F", "G"], ["B", "C", "E", "H"]],
                    5: [["A", "C", "F", "H"], ["B", "D", "E", "G"]],
                    6: [["A", "B", "G", "H"], ["C", "D", "E", "F"]],
                    7: [["A", "D", "E", "H"], ["B", "C", "F", "G"]],
                    8: [["A", "C", "D", "F"], ["B", "E", "G", "H"]],
                },
                "true_partition_id": 7,
            },
            4: {
                "max_queries": 4,
                "partitions": {
                    1: [["A", "C", "E", "G"], ["B", "D", "F", "H"]],
                    2: [["A", "B", "E", "F"], ["C", "D", "G", "H"]],
                    3: [["A", "B", "C", "D"], ["E", "F", "G", "H"]],
                    4: [["A", "D", "F", "G"], ["B", "C", "E", "H"]],
                    5: [["A", "C", "F", "H"], ["B", "D", "E", "G"]],
                    6: [["A", "B", "G", "H"], ["C", "D", "E", "F"]],
                    7: [["A", "D", "E", "H"], ["B", "C", "F", "G"]],
                    8: [["A", "C", "D", "F"], ["B", "E", "G", "H"]],
                    9: [["A", "E", "F", "G"], ["B", "C", "D", "H"]],
                    10: [["A", "C", "D", "H"], ["B", "E", "F", "G"]],
                },
                "true_partition_id": 5,
            },
            5: {
                "max_queries": 4,
                "partitions": {
                    1: [["A", "C", "E", "G"], ["B", "D", "F", "H"]],
                    2: [["A", "B", "E", "F"], ["C", "D", "G", "H"]],
                    3: [["A", "B", "C", "D"], ["E", "F", "G", "H"]],
                    4: [["A", "D", "F", "G"], ["B", "C", "E", "H"]],
                    5: [["A", "C", "F", "H"], ["B", "D", "E", "G"]],
                    6: [["A", "B", "G", "H"], ["C", "D", "E", "F"]],
                    7: [["A", "D", "E", "H"], ["B", "C", "F", "G"]],
                    8: [["A", "C", "D", "F"], ["B", "E", "G", "H"]],
                    9: [["A", "E", "F", "G"], ["B", "C", "D", "H"]],
                    10: [["A", "C", "D", "H"], ["B", "E", "F", "G"]],
                    11: [["A", "B", "D", "F"], ["C", "E", "G", "H"]],
                    12: [["A", "C", "E", "H"], ["B", "D", "F", "G"]],
                },
                "true_partition_id": 11,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self.max_queries = cfg["max_queries"]
        self.all_partitions = cfg["partitions"]
        self.true_partition_id = cfg["true_partition_id"]
        
        self.true_partition = self.all_partitions[self.true_partition_id]
        
        self.element_to_group = {}
        for group_idx, group in enumerate(self.true_partition):
            for element in group:
                self.element_to_group[element] = group_idx
        
        self.query_count = 0
        
        self.possible_partitions = set(self.all_partitions.keys())
        
        partition_ids = sorted(self.all_partitions.keys())
        if lang == "zh":
            self._game_info["partition_id_range"] = f"{partition_ids[0]} 到 {partition_ids[-1]}"
        else:
            self._game_info["partition_id_range"] = f"{partition_ids[0]} to {partition_ids[-1]}"

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        for kv in kv_pairs:
            if "=" not in kv:
                continue
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "partition_id" not in ans_dict or "same_group" not in ans_dict:
            return False
        
        try:
            predicted_id = int(ans_dict["partition_id"])
        except Exception:
            return False
        
        if predicted_id != self.true_partition_id:
            return False
        
        predicted_same = ans_dict["same_group"].lower() in ["true", "是"]
        
        b_group = self.element_to_group.get("B")
        c_group = self.element_to_group.get("C")
        actual_same = (b_group == c_group)
        
        return predicted_same == actual_same

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            same_res, diff_res = "同类", "异类"
            error_limit = f"错误：已超过最大查询次数限制（{self.max_queries}次）。"
            error_format = "错误：格式无效或元素不存在。"
        else:
            same_res, diff_res = "same", "different"
            error_limit = f"Error: Maximum query limit ({self.max_queries}) exceeded."
            error_format = "Error: Invalid format or element does not exist."

        if "query_pair" in parsed_info:
            if self.query_count >= self.max_queries:
                raise RuntimeError(error_limit)
            
            try:
                raw = parsed_info["query_pair"]
                elements = [x.strip().upper() for x in raw.split(",")]
                
                if len(elements) != 2:
                    raise ValueError("Must query exactly two elements")
                
                elem1, elem2 = elements[0], elements[1]
                
                if elem1 not in self.element_to_group or elem2 not in self.element_to_group:
                    return error_format
                
                if elem1 == elem2:
                    return error_format
                
                self.query_count += 1
                
                is_same_group = (self.element_to_group[elem1] == self.element_to_group[elem2])
                
                self._update_possible_partitions(elem1, elem2, is_same_group)
                
                return same_res if is_same_group else diff_res
                
            except Exception:
                return error_format

        elif "query_remaining" in parsed_info:
            return str(len(self.possible_partitions))

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        elements = ["A", "B", "C", "D", "E", "F", "G", "H"]
        
        if self.config.language == "zh":
            same_res, diff_res = "同类", "异类"
        else:
            same_res, diff_res = "same", "different"
        
        for i in range(len(elements)):
            for j in range(i + 1, len(elements)):
                elem1 = elements[i]
                elem2 = elements[j]
                
                is_same_group = (self.element_to_group[elem1] == self.element_to_group[elem2])
                ans = same_res if is_same_group else diff_res
                
                results.append({
                    "query": f"<query_pair>{elem1},{elem2}</query_pair>",
                    "answer": ans
                })

        return results

    def _update_possible_partitions(self, elem1, elem2, is_same_group):
        to_remove = set()
        
        for partition_id in self.possible_partitions:
            partition = self.all_partitions[partition_id]
            
            elem_to_group = {}
            for group_idx, group in enumerate(partition):
                for element in group:
                    elem_to_group[element] = group_idx
            
            predicted_same = (elem_to_group.get(elem1) == elem_to_group.get(elem2))
            
            if predicted_same != is_same_group:
                to_remove.add(partition_id)
        
        self.possible_partitions -= to_remove

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "同类":
            return "异类"
        if correct == "异类":
            return "同类"
        
        lower_correct = correct.lower()
        if lower_correct == "same":
            return "different"
        if lower_correct == "different":
            return "same"
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
            
        if lower_correct == "yes":
            return "No" if correct[0].isupper() else "no"
        if lower_correct == "no":
            return "Yes" if correct[0].isupper() else "yes"
            
        return correct + "_WRONG"