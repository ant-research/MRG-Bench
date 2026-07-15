from .base import Game
import random
from math import gcd

class HiddenOrderInferenceGame(Game):

    game_rule_zh = """\
我们来玩一个"隐藏顺序推理"游戏，规则如下：

游戏设定了 {n} 个互不相同的标识：{identifiers}。我已秘密地将这些标识按照某种规律排列成一条线性顺序（从位置 1 到位置 {n}），但这个顺序对你是隐藏的。这个顺序由一个固定的生成规律决定，在整个游戏过程中保持不变。

你可以反复向我提出间隔查询，询问任意两个不同标识之间的距离。每次查询时，我会告诉你在线性顺序中严格位于这两个标识之间的元素个数（如果两个标识相邻，则返回 0）。

你的目标是通过尽可能少的查询，推断出隐藏的排列规律或完整顺序，使得你能够在不再查询的情况下，正确计算任意两个标识之间的间隔数。

使用以下 XML 格式进行间隔查询（每次只能查询一对标识）：

<query>A,B</query>

其中 A 和 B 是标识集合中的两个不同标识。我会返回一个非负整数，表示在线性顺序中严格位于 A 和 B 之间的元素个数。

当你认为已经推断出隐藏的排列规律后，请提交你的归纳结果。你需要：

1. 描述你推断出的生成规律，或直接给出完整的顺序（从位置 1 到位置 {n} 依次列出标识）
2. 声明你已准备好接受检验

提交格式如下：

<infer>规律描述或完整顺序：标识1,标识2,标识3,...</infer>

注意：
- 你必须完成至少 6 次有效查询后才能提交归纳
- 查询总数不能超过 20 次，否则游戏失败
- 提交归纳后，我会给你 5 组新的标识对，你需要在不再查询的情况下计算它们的间隔数

当我给出检验标识对后，请使用以下格式提交你的答案：

<answer>d1,d2,d3,d4,d5</answer>

其中 d1 到 d5 是你计算出的 5 组标识对的间隔数（按顺序对应）。5 个答案必须全部正确才算通过。
"""

    game_rule_en = """\
Let's play a "Hidden Order Inference" game. Here are the rules:

The game has {n} distinct identifiers: {identifiers}. I have secretly arranged these identifiers in a linear order (from position 1 to position {n}) according to some fixed rule, but this order is hidden from you. The order is determined by a consistent generation rule that remains unchanged throughout the game.

You can repeatedly ask me interval queries about any two different identifiers. For each query, I will tell you the number of elements strictly between these two identifiers in the linear order (if they are adjacent, I return 0).

Your goal is to infer the hidden arrangement rule or complete order through as few queries as possible, so that you can correctly calculate the interval between any two identifiers without further queries.

Use the following XML format for interval queries (one pair per query):

<query>A,B</query>

Where A and B are two different identifiers from the set. I will return a non-negative integer indicating the number of elements strictly between A and B in the linear order.

When you believe you have inferred the hidden arrangement rule, submit your inference. You need to:

1. Describe the generation rule you inferred, or directly provide the complete order (list identifiers from position 1 to position {n})
2. Declare you are ready for verification

Submission format:

<infer>Rule description or complete order: id1,id2,id3,...</infer>

Notes:
- You must complete at least 6 valid queries before submitting inference
- Total queries cannot exceed 20, otherwise the game fails
- After submitting inference, I will give you 5 new identifier pairs, and you need to calculate their intervals without further queries

When I provide the verification pairs, submit your answers using:

<answer>d1,d2,d3,d4,d5</answer>

Where d1 to d5 are the interval numbers you calculated for the 5 pairs (in corresponding order). All 5 answers must be correct to pass.
"""

    contextualized_rule_zh_1 = """\
作为城市轨道交通规划师，你需要排查一条新线路的站点盲区。

系统录入了 {n} 个新建站点的代码：{identifiers}。系统已将这些站点按照某种特定的规律沿单向线性轨道排列（从始发站 1 到终点站 {n}），但由于图纸加密，具体站点顺序对你是隐藏的。这个站点顺序由固定的规划规律决定，在排查期间保持不变。

你可以反复向控制系统提出间隔查询，询问任意两个不同站点之间的距离。每次查询时，系统会返回在轨道线路上严格位于这两个站点之间的站点个数（如果两站相邻，则返回 0）。

你的目标是通过尽可能少的查询，推断出隐藏的站点排布规律或完整顺序，使得你能够在不再查询的情况下，正确计算任意两个站点之间的间隔站数。

使用以下 XML 格式进行间隔查询（每次只能查询一对站点）：

<query>A,B</query>

其中 A 和 B 是站点集合中的两个不同站点代码。系统会返回一个非负整数，表示在线路上严格位于 A 和 B 之间的站点个数。

当你认为已经推断出隐藏的排布规律后，请提交你的归纳结果。你需要：

1. 描述你推断出的站点生成规律，或直接给出完整的顺序（从始发站 1 到终点站 {n} 依次列出站点）
2. 声明你已准备好接受检验

提交格式如下：

<infer>规律描述或完整顺序：站点1,站点2,站点3,...</infer>

注意：
- 你必须完成至少 6 次有效查询后才能提交归纳
- 查询总数不能超过 20 次，否则排查任务失败
- 提交归纳后，系统会给你 5 组新的站点对，你需要在不再查询的情况下计算它们的间隔站数

当系统给出检验站点对后，请使用以下格式提交你的答案：

<answer>d1,d2,d3,d4,d5</answer>

其中 d1 到 d5 是你计算出的 5 组站点对的间隔站数（按顺序对应）。5 个答案必须全部正确才算通过排查。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
As an urban rail transit planner, you need to troubleshoot blind spots on a newly planned line.

The system has registered {n} new station codes: {identifiers}. These stations have been arranged in a linear, one-way sequence (from origin 1 to terminus {n}) according to a specific rule, but the exact order is hidden from you due to blueprint encryption. This sequence is determined by a consistent planning rule and remains unchanged during troubleshooting.

You can repeatedly ask the control system interval queries about any two different stations. For each query, the system will return the number of stations strictly located between these two stations on the track (if they are adjacent, it returns 0).

Your goal is to infer the hidden arrangement rule or the complete sequence through as few queries as possible, so that you can correctly calculate the interval between any two stations without further queries.

Use the following XML format for interval queries (one pair per query):

<query>A,B</query>

Where A and B are two different station codes from the set. The system will return a non-negative integer indicating the number of stations strictly between A and B.

When you believe you have inferred the hidden sequence rule, submit your inference. You need to:

1. Describe the generation rule you inferred, or directly provide the complete sequence (list station codes from origin 1 to terminus {n})
2. Declare you are ready for verification

Submission format:

<infer>Rule description or complete sequence: code1,code2,code3,...</infer>

Notes:
- You must complete at least 6 valid queries before submitting inference
- Total queries cannot exceed 20, otherwise the troubleshooting fails
- After submitting inference, the system will give you 5 new station pairs, and you need to calculate their interval stations without further queries

When the system provides the verification pairs, submit your answers using:

<answer>d1,d2,d3,d4,d5</answer>

Where d1 to d5 are the interval numbers you calculated for the 5 pairs (in corresponding order). All 5 answers must be correct to pass.
"""

    contextualized_rule_zh_2 = """\
作为临床研究员，你正在分析一种新型靶向药物在特定疗程中的激活顺序。

疗程设定了 {n} 个互不相同的治疗靶点：{identifiers}。药物作用机制已将这些靶点按照某种规律排列成一条线性的激活顺序（从阶段 1 到阶段 {n}），但这个顺序对你是隐藏的。这个顺序由一种固定的生化规律决定，在整个测试过程中保持不变。

你可以反复向分析仪提出间隔查询，询问任意两个不同靶点之间的间隔。每次查询时，分析仪会告诉你在线性激活顺序中严格位于这两个靶点之间的靶点个数（如果两个靶点相继激活，则返回 0）。

你的目标是通过尽可能少的查询，推断出隐藏的靶点激活规律或完整顺序，使得你能够在不再查询的情况下，正确计算任意两个靶点之间的间隔数。

使用以下 XML 格式进行间隔查询（每次只能查询一对靶点）：

<query>A,B</query>

其中 A 和 B 是靶点集合中的两个不同靶点。我会返回一个非负整数，表示在激活顺序中严格位于 A 和 B 之间的靶点个数。

当你认为已经推断出隐藏的激活规律后，请提交你的归纳结果。你需要：

1. 描述你推断出的生成规律，或直接给出完整的顺序（从阶段 1 到阶段 {n} 依次列出靶点）
2. 声明你已准备好接受检验

提交格式如下：

<infer>规律描述或完整顺序：靶点1,靶点2,靶点3,...</infer>

注意：
- 你必须完成至少 6 次有效查询后才能提交归纳
- 查询总数不能超过 20 次，否则研究失败
- 提交归纳后，我会给你 5 组新的靶点对，你需要在不再查询的情况下计算它们的间隔数

当我给出检验靶点对后，请使用以下格式提交你的答案：

<answer>d1,d2,d3,d4,d5</answer>

其中 d1 到 d5 是你计算出的 5 组靶点对的间隔数（按顺序对应）。5 个答案必须全部正确才算通过。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
As a clinical researcher, you are analyzing the activation sequence of a novel targeted therapy during a specific treatment course.

The treatment involves {n} distinct therapeutic targets: {identifiers}. The drug mechanism has secretly arranged these targets in a linear activation order (from stage 1 to stage {n}) according to a specific biochemical rule, but this sequence is hidden from you. The order is determined by a consistent generation rule that remains unchanged throughout the test.

You can repeatedly ask the analyzer interval queries about any two different targets. For each query, it will tell you the number of targets strictly between these two targets in the linear activation order (if they activate consecutively, it returns 0).

Your goal is to infer the hidden activation rule or complete sequence through as few queries as possible, so that you can correctly calculate the interval between any two targets without further queries.

Use the following XML format for interval queries (one pair per query):

<query>A,B</query>

Where A and B are two different targets from the set. The analyzer will return a non-negative integer indicating the number of targets strictly between A and B in the activation order.

When you believe you have inferred the hidden activation rule, submit your inference. You need to:

1. Describe the generation rule you inferred, or directly provide the complete sequence (list targets from stage 1 to stage {n})
2. Declare you are ready for verification

Submission format:

<infer>Rule description or complete sequence: target1,target2,target3,...</infer>

Notes:
- You must complete at least 6 valid queries before submitting inference
- Total queries cannot exceed 20, otherwise the research fails
- After submitting inference, I will give you 5 new target pairs, and you need to calculate their intervals without further queries

When I provide the verification pairs, submit your answers using:

<answer>d1,d2,d3,d4,d5</answer>

Where d1 to d5 are the interval numbers you calculated for the 5 pairs (in corresponding order). All 5 answers must be correct to pass.
"""

    contextualized_rule_zh_3 = """\
作为课程系统架构师，你正在测试一套全新的自适应学习系统。

系统设定了 {n} 个互不相同的核心知识模块：{identifiers}。系统底层已将这些模块按照某种规律编排成一条线性的学习路径（从节点 1 到节点 {n}），但具体的模块顺序由于权限限制对你是隐藏的。这个顺序由一个固定的认知规律决定，在整个测试过程中保持不变。

你可以反复向系统数据库提出间隔查询，询问任意两个不同模块之间的距离。每次查询时，系统会告诉你在线性学习路径中严格位于这两个模块之间的模块个数（如果两个模块相邻，则返回 0）。

你的目标是通过尽可能少的查询，推断出隐藏的路径编排规律或完整顺序，使得你能够在不再查询的情况下，正确计算任意两个模块之间的间隔数。

使用以下 XML 格式进行间隔查询（每次只能查询一对模块）：

<query>A,B</query>

其中 A 和 B 是模块集合中的两个不同模块。系统会返回一个非负整数，表示在学习路径中严格位于 A 和 B 之间的模块个数。

当你认为已经推断出隐藏的编排规律后，请提交你的归纳结果。你需要：

1. 描述你推断出的生成规律，或直接给出完整的顺序（从节点 1 到节点 {n} 依次列出模块）
2. 声明你已准备好接受检验

提交格式如下：

<infer>规律描述或完整顺序：模块1,模块2,模块3,...</infer>

注意：
- 你必须完成至少 6 次有效查询后才能提交归纳
- 查询总数不能超过 20 次，否则测试失败
- 提交归纳后，系统会给你 5 组新的模块对，你需要在不再查询的情况下计算它们的间隔数

当系统给出检验模块对后，请使用以下格式提交你的答案：

<answer>d1,d2,d3,d4,d5</answer>

其中 d1 到 d5 是你计算出的 5 组模块对的间隔数（按顺序对应）。5 个答案必须全部正确才算通过测试。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
As a curriculum system architect, you are testing a new adaptive learning system.

The system incorporates {n} distinct core knowledge modules: {identifiers}. The backend has arranged these modules in a linear learning path (from node 1 to node {n}) according to a specific rule, but this exact sequence is hidden from you due to access restrictions. The order is determined by a consistent cognitive rule that remains unchanged throughout the test.

You can repeatedly ask the system database interval queries about any two different modules. For each query, the system will tell you the number of modules strictly between these two modules in the linear learning path (if they are adjacent, it returns 0).

Your goal is to infer the hidden arrangement rule or complete path sequence through as few queries as possible, so that you can correctly calculate the interval between any two modules without further queries.

Use the following XML format for interval queries (one pair per query):

<query>A,B</query>

Where A and B are two different modules from the set. The system will return a non-negative integer indicating the number of modules strictly between A and B in the learning path.

When you believe you have inferred the hidden arrangement rule, submit your inference. You need to:

1. Describe the generation rule you inferred, or directly provide the complete sequence (list modules from node 1 to node {n})
2. Declare you are ready for verification

Submission format:

<infer>Rule description or complete sequence: mod1,mod2,mod3,...</infer>

Notes:
- You must complete at least 6 valid queries before submitting inference
- Total queries cannot exceed 20, otherwise the test fails
- After submitting inference, the system will give you 5 new module pairs, and you need to calculate their intervals without further queries

When the system provides the verification pairs, submit your answers using:

<answer>d1,d2,d3,d4,d5</answer>

Where d1 to d5 are the interval numbers you calculated for the 5 pairs (in corresponding order). All 5 answers must be correct to pass.
"""

    contextualized_rule_zh_4 = """\
作为工业互联网工程师，你需要诊断一条自动化装配流水线的拓扑结构。

该流水线包含 {n} 个互不相同的装配工位：{identifiers}。控制程序已将这些工位按照某种规律排列成一条线性的加工顺序（从工序 1 到工序 {n}），但由于图纸遗失，完整的排布对你是隐藏的。这个顺序由一个固定的工艺规律决定，在整个诊断过程中保持不变。

你可以反复向中央主板提出间隔查询，询问任意两个不同工位之间的距离。每次查询时，系统会告诉你在线性流水线中严格位于这两个工位之间的工位个数（如果两个工位相连，则返回 0）。

你的目标是通过尽可能少的查询，推断出隐藏的工位排布规律或完整顺序，使得你能够在不再查询的情况下，正确计算任意两个工位之间的间隔数。

使用以下 XML 格式进行间隔查询（每次只能查询一对工位）：

<query>A,B</query>

其中 A 和 B 是工位集合中的两个不同工位代码。系统会返回一个非负整数，表示在流水线中严格位于 A 和 B 之间的工位个数。

当你认为已经推断出隐藏的排布规律后，请提交你的归纳结果。你需要：

1. 描述你推断出的工序生成规律，或直接给出完整的顺序（从工序 1 到工序 {n} 依次列出工位）
2. 声明你已准备好接受检验

提交格式如下：

<infer>规律描述或完整顺序：工位1,工位2,工位3,...</infer>

注意：
- 你必须完成至少 6 次有效查询后才能提交归纳
- 查询总数不能超过 20 次，否则诊断失败
- 提交归纳后，系统会给你 5 组新的工位对，你需要在不再查询的情况下计算它们的间隔数

当系统给出检验工位对后，请使用以下格式提交你的答案：

<answer>d1,d2,d3,d4,d5</answer>

其中 d1 到 d5 是你计算出的 5 组工位对的间隔数（按顺序对应）。5 个答案必须全部正确才算通过诊断。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
As an industrial IoT engineer, you need to diagnose the topological structure of an automated assembly pipeline.

The pipeline consists of {n} distinct assembly stations: {identifiers}. The control program has arranged these stations in a linear processing order (from operation 1 to operation {n}) according to a specific rule, but the complete layout is hidden from you due to lost blueprints. This order is determined by a fixed process rule and remains unchanged throughout the diagnostic process.

You can repeatedly ask the central motherboard interval queries about any two different stations. For each query, the system will tell you the number of stations strictly between these two stations on the linear pipeline (if they are adjacent, it returns 0).

Your goal is to infer the hidden layout rule or complete sequence through as few queries as possible, so that you can correctly calculate the interval between any two stations without further queries.

Use the following XML format for interval queries (one pair per query):

<query>A,B</query>

Where A and B are two different station codes from the set. The system will return a non-negative integer indicating the number of stations strictly between A and B on the pipeline.

When you believe you have inferred the hidden arrangement rule, submit your inference. You need to:

1. Describe the generation rule you inferred, or directly provide the complete sequence (list stations from operation 1 to operation {n})
2. Declare you are ready for verification

Submission format:

<infer>Rule description or complete sequence: station1,station2,station3,...</infer>

Notes:
- You must complete at least 6 valid queries before submitting inference
- Total queries cannot exceed 20, otherwise the diagnosis fails
- After submitting inference, the system will give you 5 new station pairs, and you need to calculate their intervals without further queries

When the system provides the verification pairs, submit your answers using:

<answer>d1,d2,d3,d4,d5</answer>

Where d1 to d5 are the interval numbers you calculated for the 5 pairs (in corresponding order). All 5 answers must be correct to pass.
"""

    contextualized_rule_zh_5 = """\
作为合规审查系统的设计者，你正在核对一桩跨国商事仲裁案的法定程序链条。

案件包含 {n} 个互不相同的法定程序节点：{identifiers}。系统已将这些节点按照某种合规规律排列成一条线性的时间执行顺序（从步骤 1 到步骤 {n}），但这个确切的顺序因卷宗保密机制对你是隐藏的。这个顺序由一个固定的法律程序规则决定，在整个核对过程中保持不变。

你可以反复向审查系统提出质询，询问任意两个不同程序节点之间的间隔跨度。每次质询时，系统会告诉你在线性程序链条中严格位于这两个节点之间的环节个数（如果两个节点紧密相连，则返回 0）。

你的目标是通过尽可能少的质询，推断出隐藏的程序排列规律或完整顺序，使得你能够在不再质询的情况下，正确计算任意两个节点之间的间隔数。

使用以下 XML 格式进行间隔质询（每次只能质询一对节点）：

<query>A,B</query>

其中 A 和 B 是节点集合中的两个不同程序节点。系统会返回一个非负整数，表示在程序链条中严格位于 A 和 B 之间的环节个数。

当你认为已经推断出隐藏的程序排列规律后，请提交你的归纳结果。你需要：

1. 描述你推断出的程序生成规律，或直接给出完整的顺序（从步骤 1 到步骤 {n} 依次列出节点）
2. 声明你已准备好接受检验

提交格式如下：

<infer>规律描述或完整顺序：节点1,节点2,节点3,...</infer>

注意：
- 你必须完成至少 6 次有效质询后才能提交归纳
- 质询总数不能超过 20 次，否则核对任务失败
- 提交归纳后，系统会给你 5 组新的节点对，你需要在不再质询的情况下计算它们的间隔数

当系统给出检验节点对后，请使用以下格式提交你的答案：

<answer>d1,d2,d3,d4,d5</answer>

其中 d1 到 d5 是你计算出的 5 组节点对的间隔数（按顺序对应）。5 个答案必须全部正确才算通过核对。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
As the designer of a compliance review system, you are verifying the statutory procedure chain of a transnational commercial arbitration case.

The case involves {n} distinct statutory procedure nodes: {identifiers}. The system has arranged these nodes in a linear chronological execution order (from step 1 to step {n}) according to a specific compliance rule, but this exact sequence is hidden from you due to file confidentiality mechanisms. The order is determined by a fixed legal procedure rule and remains unchanged throughout the verification process.

You can repeatedly raise interval inquiries to the review system about the span between any two different procedure nodes. For each inquiry, the system will tell you the number of intermediate links strictly between these two nodes in the linear procedure chain (if they are strictly consecutive, it returns 0).

Your goal is to infer the hidden procedure arrangement rule or complete sequence through as few inquiries as possible, so that you can correctly calculate the interval between any two nodes without further inquiries.

Use the following XML format for interval inquiries (one pair per inquiry):

<query>A,B</query>

Where A and B are two different procedure nodes from the set. The system will return a non-negative integer indicating the number of intermediate links strictly between A and B in the procedure chain.

When you believe you have inferred the hidden sequence rule, submit your inference. You need to:

1. Describe the generation rule you inferred, or directly provide the complete sequence (list nodes from step 1 to step {n})
2. Declare you are ready for verification

Submission format:

<infer>Rule description or complete sequence: node1,node2,node3,...</infer>

Notes:
- You must complete at least 6 valid inquiries before submitting inference
- Total inquiries cannot exceed 20, otherwise the verification task fails
- After submitting inference, the system will give you 5 new node pairs, and you need to calculate their intervals without further inquiries

When the system provides the verification pairs, submit your answers using:

<answer>d1,d2,d3,d4,d5</answer>

Where d1 to d5 are the interval numbers you calculated for the 5 pairs (in corresponding order). All 5 answers must be correct to pass.
"""

    tags = ["query", "infer", "answer"]
    reasoning_type = "归纳推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 12,
                "identifiers": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"],
                "rule_type": "step_mod",
                "rule_params": {"step": 5},
            },
            2: {
                "n": 16,
                "identifiers": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"],
                "rule_type": "odd_even",
                "rule_params": {},
            },
            3: {
                "n": 20,
                "identifiers": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"],
                "rule_type": "block_reverse",
                "rule_params": {"block_size": 4},
            },
            4: {
                "n": 24,
                "identifiers": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X"],
                "rule_type": "group_rotate",
                "rule_params": {"num_groups": 3},
            },
            5: {
                "n": 30,
                "identifiers": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "BB", "CC", "DD"],
                "rule_type": "mirror_step",
                "rule_params": {"step": 7},
            },
        },
        "en": {
            1: {
                "n": 12,
                "identifiers": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"],
                "rule_type": "step_mod",
                "rule_params": {"step": 5},
            },
            2: {
                "n": 16,
                "identifiers": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"],
                "rule_type": "odd_even",
                "rule_params": {},
            },
            3: {
                "n": 20,
                "identifiers": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"],
                "rule_type": "block_reverse",
                "rule_params": {"block_size": 4},
            },
            4: {
                "n": 24,
                "identifiers": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X"],
                "rule_type": "group_rotate",
                "rule_params": {"num_groups": 3},
            },
            5: {
                "n": 30,
                "identifiers": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "BB", "CC", "DD"],
                "rule_type": "mirror_step",
                "rule_params": {"step": 7},
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0
        self.inferred = False
        self.verification_pairs = []
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
        self._game_info["identifiers"] = ", ".join(cfg["identifiers"])
        
        self.identifiers = cfg["identifiers"]
        self.n = cfg["n"]
        self.rule_type = cfg["rule_type"]
        self.rule_params = cfg["rule_params"]
        
        self.order = self._generate_order()
        
        self.position_to_id = {pos: id_ for id_, pos in self.order.items()}

    def _generate_order(self):
        order = {}
        
        if self.rule_type == "step_mod":
            step = self.rule_params["step"]
            assert gcd(step, self.n) == 1, f"step_mod requires gcd(step={step}, n={self.n}) == 1 for a valid permutation"
            idx = 0
            for pos in range(1, self.n + 1):
                order[self.identifiers[idx]] = pos
                idx = (idx + step) % self.n
                
        elif self.rule_type == "odd_even":
            pos = 1
            for i in range(0, self.n, 2):
                order[self.identifiers[i]] = pos
                pos += 1
            for i in range(1, self.n, 2):
                order[self.identifiers[i]] = pos
                pos += 1
                
        elif self.rule_type == "block_reverse":
            block_size = self.rule_params["block_size"]
            result = []
            for i in range(0, self.n, block_size):
                block = self.identifiers[i:i+block_size]
                result.extend(reversed(block))
            for pos, id_ in enumerate(result, 1):
                order[id_] = pos
                
        elif self.rule_type == "group_rotate":
            num_groups = self.rule_params["num_groups"]
            groups = [[] for _ in range(num_groups)]
            for i, id_ in enumerate(self.identifiers):
                groups[i % num_groups].append(id_)
            result = []
            for group in groups:
                result.extend(group)
            for pos, id_ in enumerate(result, 1):
                order[id_] = pos
                
        elif self.rule_type == "mirror_step":
            step = self.rule_params["step"]
            mid = self.n // 2
            assert gcd(step, self.n) == 1, (
                f"mirror_step requires gcd(step={step}, n={self.n}) == 1 "
                f"for full coverage traversal"
            )
            
            visited = []
            idx = 0
            for _ in range(self.n):
                visited.append(idx)
                idx = (idx + step) % self.n
            
            first_half_indices = visited[:mid]
            for pos_offset, ui in enumerate(first_half_indices):
                order[self.identifiers[ui]] = pos_offset + 1
            
            used_set = set(first_half_indices)
            remaining = [i for i in range(self.n) if i not in used_set]
            remaining.reverse()
            for pos_offset, ri in enumerate(remaining):
                order[self.identifiers[ri]] = mid + pos_offset + 1
        
        assert len(order) == self.n, f"Order generation incomplete: got {len(order)}, expected {self.n}"
        positions = sorted(order.values())
        assert positions == list(range(1, self.n + 1)), f"Order is not a valid permutation: {positions}"
        
        return order

    def _calculate_distance(self, id1, id2):
        pos1 = self.order[id1]
        pos2 = self.order[id2]
        return abs(pos1 - pos2) - 1

    def evaluate(self, parsed_info):
        if not self.inferred or len(self.verification_pairs) != 5:
            return False
            
        raw_ans = parsed_info["answer"].strip()
        try:
            distances = [int(x.strip()) for x in raw_ans.split(",")]
            if len(distances) != 5:
                return False
                
            for i, (id1, id2) in enumerate(self.verification_pairs):
                expected = self._calculate_distance(id1, id2)
                if distances[i] != expected:
                    return False
            return True
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        
        if "query" in parsed_info:
            if self.inferred:
                return "错误：已提交归纳后不能再进行查询。" if self.config.language == "zh" else "Error: Cannot query after inference submission."
            
            if self.query_count >= 20:
                raise ValueError("Query limit exceeded (max 20).")
            
            try:
                raw = parsed_info["query"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                id1, id2 = parts
                
                if id1 not in self.order or id2 not in self.order:
                    return "错误：标识不存在。" if self.config.language == "zh" else "Error: Identifier not found."
                if id1 == id2:
                    return "错误：不能查询相同的标识。" if self.config.language == "zh" else "Error: Cannot query same identifier."
                
                self.query_count += 1
                distance = self._calculate_distance(id1, id2)
                return str(distance)
                
            except Exception:
                return "错误：查询格式无效。" if self.config.language == "zh" else "Error: Invalid query format."
        
        elif "infer" in parsed_info:
            if self.query_count < 6:
                msg = f"错误：至少需要完成 6 次查询才能提交归纳（当前已查询 {self.query_count} 次）。" if self.config.language == "zh" else f"Error: At least 6 queries required before inference (current: {self.query_count})."
                return msg
            
            self.inferred = True
            
            all_pairs = []
            for i in range(len(self.identifiers)):
                for j in range(i + 1, len(self.identifiers)):
                    all_pairs.append((self.identifiers[i], self.identifiers[j]))
            
            random.seed(42 + self.config.difficulty)
            self.verification_pairs = random.sample(all_pairs, 5)
            
            pairs_str = ", ".join([f"({id1}, {id2})" for id1, id2 in self.verification_pairs])
            
            if self.config.language == "zh":
                return f"收到你的归纳。现在请计算以下 5 组标识对的间隔数（不能再查询）：\n{pairs_str}\n\n请使用 <answer>d1,d2,d3,d4,d5</answer> 格式提交答案。"
            else:
                return f"Inference received. Now calculate the intervals for these 5 pairs (no more queries allowed):\n{pairs_str}\n\nSubmit using <answer>d1,d2,d3,d4,d5</answer> format."
        
        else:
            raise ValueError("No valid tag found.")

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if "是" in correct:
            return correct.replace("是", "否")
        if "否" in correct:
            return correct.replace("否", "是")
            
        lower_correct = correct.lower()
        if "yes" in lower_correct:
            if correct.isupper(): return correct.replace("YES", "NO")
            if correct.istitle(): return correct.replace("Yes", "No")
            return correct.replace("yes", "no")
        if "no" in lower_correct:
            if correct.isupper(): return correct.replace("NO", "YES")
            if correct.istitle(): return correct.replace("No", "Yes")
            return correct.replace("no", "yes")

        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        for i in range(len(self.identifiers)):
            for j in range(i + 1, len(self.identifiers)):
                id1 = self.identifiers[i]
                id2 = self.identifiers[j]
                
                distance = self._calculate_distance(id1, id2)
                
                results.append({
                    "query": f"<query>{id1},{id2}</query>",
                    "answer": str(distance)
                })
        return results