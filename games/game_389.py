from .base import Game
import random
import re
from typing import List, Dict

class HiddenTreeFunctionGame(Game):
    
    reasoning_type = "归纳推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"隐藏树函数推理"游戏，规则如下：

游戏设定了一棵有根树，包含 {n} 个节点（编号 1 到 {n}），根节点为 {root}。树的结构已公开如下：
{tree_structure}

我已秘密设计了一个函数 f，它接受任意两个节点 (u, v) 作为输入，返回树中的某个唯一节点。该函数具有以下性质：
- 对于任意节点对 (u, v)，f(u, v) 返回确定的单一节点
- f(u, v) 和 f(v, u) 的结果相同（顺序无关）
- 函数在整个游戏中保持不变

游戏分为两个阶段：

**阶段1（归纳阶段）**：你最多可以进行 {Q} 次查询，每次查询可以选择以下两种方式之一：
1. 值查询：提交一对节点 (a, b)，我会告诉你 f(a, b) 的值。
2. 判定查询：提交三个节点 (a, b, c)，我会告诉你 f(a, b) 是否等于 c。

**阶段2（挑战阶段）**：我会提供 {M} 对新的节点对，你需要逐一预测每对节点的 f 值。
- 严格模式：所有 {M} 题必须全部正确才算成功。
- 宽松模式：至少答对 {pass_count} 题即可成功。

本局采用{mode_text}。

每次只能进行一个查询或提交。请使用以下 XML 格式：

- 值查询（例如查询节点 2 和 5）：
<query_value>2,5</query_value>

- 判定查询（例如询问 f(2,5) 是否等于 1）：
<query_judge>2,5,1</query_judge>

- 提交阶段1结束并进入阶段2：
<phase1_done></phase1_done>

- 挑战阶段提交答案（例如预测结果为节点 3）：
<answer>3</answer>

注意：
1. 归纳阶段的查询次数有限，请合理利用
2. 必须先提交 phase1_done 才能进入挑战阶段
3. 挑战阶段我会逐一给出节点对，你需要依次回答
"""

    game_rule_en = """\
Let's play a "Hidden Tree Function Inference" game. Here are the rules:

The game is set on a rooted tree with {n} nodes (numbered 1 to {n}), with root node {root}. The tree structure is publicly known as follows:
{tree_structure}

I have secretly designed a function f that takes any two nodes (u, v) as input and returns a unique node in the tree. This function has the following properties:
- For any node pair (u, v), f(u, v) returns a deterministic single node
- f(u, v) and f(v, u) produce the same result (order-independent)
- The function remains constant throughout the game

The game has two phases:

**Phase 1 (Induction Phase)**: You may perform up to {Q} queries, choosing one of the following types each time:
1. Value Query: Submit a pair of nodes (a, b), and I will tell you the value of f(a, b).
2. Judge Query: Submit three nodes (a, b, c), and I will tell you whether f(a, b) equals c.

**Phase 2 (Challenge Phase)**: I will provide {M} new node pairs, and you must predict the f value for each pair one by one.
- Strict mode: All {M} answers must be correct to succeed.
- Lenient mode: At least {pass_count} correct answers are required to succeed.

This round uses {mode_text}.

You can only perform one query or submission at a time. Use the following XML format:

- Value Query (e.g., query nodes 2 and 5):
<query_value>2,5</query_value>

- Judge Query (e.g., ask if f(2,5) equals 1):
<query_judge>2,5,1</query_judge>

- Submit end of Phase 1 and enter Phase 2:
<phase1_done></phase1_done>

- Challenge phase answer submission (e.g., predict result is node 3):
<answer>3</answer>

Notes:
1. The number of queries in the induction phase is limited, use them wisely
2. You must submit phase1_done before entering the challenge phase
3. In the challenge phase, I will provide node pairs one by one, and you must answer sequentially
"""

    contextualized_rule_zh_1 = """\
【交通场景】
交通枢纽调度分析系统启动。本系统记录了一个包含 {n} 个站点的层级化公共交通路网树，总枢纽站为 {root}。路网结构如下：
{tree_structure}

系统内置了一个溯源函数 f，用于查找任意两个站点 (u, v) 在向总枢纽回溯时的“最近公共换乘枢纽”。该函数具有以下性质：
- 对于任意站点对 (u, v)，f(u, v) 返回确定的单一枢纽站点编号
- 查找顺序不影响结果，即 f(u, v) 和 f(v, u) 相同
- 路网结构及枢纽层级在分析期间保持不变

分析分为两个阶段：

**阶段1（归纳阶段）**：你最多可以进行 {Q} 次查询，每次查询可以选择以下两种方式之一：
1. 值查询：提交一对站点 (a, b)，我会告诉你 f(a, b) 的值。
2. 判定查询：提交三个站点 (a, b, c)，我会告诉你 f(a, b) 是否等于 c。

**阶段2（挑战阶段）**：我会提供 {M} 对新的站点对，你需要逐一预测每对站点的 f 值。
- 严格模式：所有 {M} 题必须全部正确才算成功。
- 宽松模式：至少答对 {pass_count} 题即可成功。

本局采用{mode_text}。

每次只能进行一个查询或提交。请使用以下 XML 格式：

- 值查询（例如查询站点 2 和 5）：
<query_value>2,5</query_value>

- 判定查询（例如询问 f(2,5) 是否等于 1）：
<query_judge>2,5,1</query_judge>

- 提交阶段1结束并进入阶段2：
<phase1_done></phase1_done>

- 挑战阶段提交答案（例如预测结果为站点 3）：
<answer>3</answer>

注意：
1. 归纳阶段的查询次数有限，请合理利用
2. 必须先提交 phase1_done 才能进入挑战阶段
3. 挑战阶段我会逐一给出站点对，你需要依次回答
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Traffic Hub Dispatch Analysis System initiated. This system records a hierarchical public transit network tree containing {n} stations, with the main hub being {root}. The network structure is as follows:
{tree_structure}

The system has a built-in traceback function f to find the "closest common transfer hub" when tracing routes from any two stations (u, v) back to the main hub. This function has the following properties:
- For any station pair (u, v), f(u, v) returns a deterministic single hub station ID
- The lookup order does not affect the result; f(u, v) and f(v, u) are identical
- The network structure remains constant during the analysis

The analysis consists of two phases:

**Phase 1 (Induction Phase)**: You may perform up to {Q} queries, choosing one of the following types each time:
1. Value Query: Submit a pair of stations (a, b), and I will tell you the value of f(a, b).
2. Judge Query: Submit three stations (a, b, c), and I will tell you whether f(a, b) equals c.

**Phase 2 (Challenge Phase)**: I will provide {M} new station pairs, and you must predict the f value for each pair one by one.
- Strict mode: All {M} answers must be correct to succeed.
- Lenient mode: At least {pass_count} correct answers are required to succeed.

This round uses {mode_text}.

You can only perform one query or submission at a time. Use the following XML format:

- Value Query (e.g., query stations 2 and 5):
<query_value>2,5</query_value>

- Judge Query (e.g., ask if f(2,5) equals 1):
<query_judge>2,5,1</query_judge>

- Submit end of Phase 1 and enter Phase 2:
<phase1_done></phase1_done>

- Challenge phase answer submission (e.g., predict result is station 3):
<answer>3</answer>

Notes:
1. The number of queries in the induction phase is limited, use them wisely
2. You must submit phase1_done before entering the challenge phase
3. In the challenge phase, I will provide station pairs one by one, and you must answer sequentially
"""

    contextualized_rule_zh_2 = """\
【医疗场景】
病毒变异溯源分析系统启动。本系统记录了一棵包含 {n} 个毒株节点的变异演化树，零号原始毒株编号为 {root}。演化树结构如下：
{tree_structure}

系统内置了一个演化追踪函数 f，用于查找任意两个毒株 (u, v) 的“最近共同祖先毒株”。该函数具备以下特征：
- 对于任意毒株对 (u, v)，f(u, v) 返回确定的单一毒株编号
- 查找顺序不影响结果，即 f(u, v) 和 f(v, u) 相同
- 变异演化拓扑结构在整个分析流程中保持不变

系统分析分为两个阶段：

**阶段1（归纳阶段）**：你最多可以进行 {Q} 次查询，每次查询可以选择以下两种方式之一：
1. 值查询：提交一对毒株 (a, b)，我会告诉你 f(a, b) 的值。
2. 判定查询：提交三个毒株 (a, b, c)，我会告诉你 f(a, b) 是否等于 c。

**阶段2（挑战阶段）**：我会提供 {M} 对新的毒株对，你需要逐一预测每对毒株的 f 值。
- 严格模式：所有 {M} 题必须全部正确才算成功。
- 宽松模式：至少答对 {pass_count} 题即可成功。

本局采用{mode_text}。

每次只能进行一个查询或提交。请使用以下 XML 格式：

- 值查询（例如查询毒株 2 和 5）：
<query_value>2,5</query_value>

- 判定查询（例如询问 f(2,5) 是否等于 1）：
<query_judge>2,5,1</query_judge>

- 提交阶段1结束并进入阶段2：
<phase1_done></phase1_done>

- 挑战阶段提交答案（例如预测结果为毒株 3）：
<answer>3</answer>

注意：
1. 归纳阶段的查询次数有限，请合理利用
2. 必须先提交 phase1_done 才能进入挑战阶段
3. 挑战阶段我会逐一给出毒株对，你需要依次回答
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Virus Mutation Traceback Analysis System initiated. This system maps a phylogenetic tree containing {n} viral strain nodes, with the patient-zero strain being {root}. The tree structure is as follows:
{tree_structure}

The system features an evolutionary tracking function f to determine the "most recent common ancestral strain" of any two strains (u, v). This function has the following properties:
- For any strain pair (u, v), f(u, v) returns a deterministic single strain ID
- Comparison order does not affect the result; f(u, v) and f(v, u) are identical
- The mutation topology remains constant throughout the analysis

The analysis has two phases:

**Phase 1 (Induction Phase)**: You may perform up to {Q} queries, choosing one of the following types each time:
1. Value Query: Submit a pair of strains (a, b), and I will tell you the value of f(a, b).
2. Judge Query: Submit three strains (a, b, c), and I will tell you whether f(a, b) equals c.

**Phase 2 (Challenge Phase)**: I will provide {M} new strain pairs, and you must predict the f value for each pair one by one.
- Strict mode: All {M} answers must be correct to succeed.
- Lenient mode: At least {pass_count} correct answers are required to succeed.

This round uses {mode_text}.

You can only perform one query or submission at a time. Use the following XML format:

- Value Query (e.g., query strains 2 and 5):
<query_value>2,5</query_value>

- Judge Query (e.g., ask if f(2,5) equals 1):
<query_judge>2,5,1</query_judge>

- Submit end of Phase 1 and enter Phase 2:
<phase1_done></phase1_done>

- Challenge phase answer submission (e.g., predict result is strain 3):
<answer>3</answer>

Notes:
1. The number of queries in the induction phase is limited, use them wisely
2. You must submit phase1_done before entering the challenge phase
3. In the challenge phase, I will provide strain pairs one by one, and you must answer sequentially
"""

    contextualized_rule_zh_3 = """\
【教育场景】
学科知识图谱测评系统启动。本系统包含了一棵由 {n} 个知识点构成的层级树，核心基础知识点编号为 {root}。知识树结构如下：
{tree_structure}

系统设有一个前置分析函数 f，用于确定任意两个知识点 (u, v) 的“最具体公共前置知识节点”。该函数具有以下性质：
- 对于任意知识点对 (u, v)，f(u, v) 返回确定的单一前置知识点编号
- 查询次序不影响结果，即 f(u, v) 和 f(v, u) 相同
- 知识树的层级依赖关系在测评期间保持不变

测评分为两个阶段：

**阶段1（归纳阶段）**：你最多可以进行 {Q} 次查询，每次查询可以选择以下两种方式之一：
1. 值查询：提交一对知识点 (a, b)，我会告诉你 f(a, b) 的值。
2. 判定查询：提交三个知识点 (a, b, c)，我会告诉你 f(a, b) 是否等于 c。

**阶段2（挑战阶段）**：我会提供 {M} 对新的知识点对，你需要逐一预测每对知识点的 f 值。
- 严格模式：所有 {M} 题必须全部正确才算成功。
- 宽松模式：至少答对 {pass_count} 题即可成功。

本局采用{mode_text}。

每次只能进行一个查询或提交。请使用以下 XML 格式：

- 值查询（例如查询知识点 2 和 5）：
<query_value>2,5</query_value>

- 判定查询（例如询问 f(2,5) 是否等于 1）：
<query_judge>2,5,1</query_judge>

- 提交阶段1结束并进入阶段2：
<phase1_done></phase1_done>

- 挑战阶段提交答案（例如预测结果为知识点 3）：
<answer>3</answer>

注意：
1. 归纳阶段的查询次数有限，请合理利用
2. 必须先提交 phase1_done 才能进入挑战阶段
3. 挑战阶段我会逐一给出知识点对，你需要依次回答
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Academic Knowledge Graph Assessment System initiated. This system contains a hierarchical tree composed of {n} knowledge modules, with the core foundational module being {root}. The tree structure is as follows:
{tree_structure}

The system provides a prerequisite analysis function f to identify the "most specific shared prerequisite knowledge node" for any two modules (u, v). This function has the following properties:
- For any module pair (u, v), f(u, v) returns a deterministic single prerequisite module ID
- Query order does not affect the result; f(u, v) and f(v, u) are identical
- The hierarchical dependencies of the knowledge tree remain constant during the assessment

The assessment has two phases:

**Phase 1 (Induction Phase)**: You may perform up to {Q} queries, choosing one of the following types each time:
1. Value Query: Submit a pair of modules (a, b), and I will tell you the value of f(a, b).
2. Judge Query: Submit three modules (a, b, c), and I will tell you whether f(a, b) equals c.

**Phase 2 (Challenge Phase)**: I will provide {M} new module pairs, and you must predict the f value for each pair one by one.
- Strict mode: All {M} answers must be correct to succeed.
- Lenient mode: At least {pass_count} correct answers are required to succeed.

This round uses {mode_text}.

You can only perform one query or submission at a time. Use the following XML format:

- Value Query (e.g., query modules 2 and 5):
<query_value>2,5</query_value>

- Judge Query (e.g., ask if f(2,5) equals 1):
<query_judge>2,5,1</query_judge>

- Submit end of Phase 1 and enter Phase 2:
<phase1_done></phase1_done>

- Challenge phase answer submission (e.g., predict result is module 3):
<answer>3</answer>

Notes:
1. The number of queries in the induction phase is limited, use them wisely
2. You must submit phase1_done before entering the challenge phase
3. In the challenge phase, I will provide module pairs one by one, and you must answer sequentially
"""

    contextualized_rule_zh_4 = """\
【制造业/工业场景】
工业产品装配BOM分析系统启动。本产品由 {n} 个层级化组件构成，顶层总成件编号为 {root}。装配层级树如下：
{tree_structure}

系统提供了一个模块定位函数 f，用于检索任意两个底层组件 (u, v) 所在的“最小公共装配模块”。该函数具有以下性质：
- 对于任意组件对 (u, v)，f(u, v) 返回确定的单一装配模块编号
- 检索不区分先后顺序，即 f(u, v) 和 f(v, u) 相同
- BOM装配结构在本次分析任务中保持不变

分析任务分为两个阶段：

**阶段1（归纳阶段）**：你最多可以进行 {Q} 次查询，每次查询可以选择以下两种方式之一：
1. 值查询：提交一对组件 (a, b)，我会告诉你 f(a, b) 的值。
2. 判定查询：提交三个组件 (a, b, c)，我会告诉你 f(a, b) 是否等于 c。

**阶段2（挑战阶段）**：我会提供 {M} 对新的组件对，你需要逐一预测每对组件的 f 值。
- 严格模式：所有 {M} 题必须全部正确才算成功。
- 宽松模式：至少答对 {pass_count} 题即可成功。

本局采用{mode_text}。

每次只能进行一个查询或提交。请使用以下 XML 格式：

- 值查询（例如查询组件 2 和 5）：
<query_value>2,5</query_value>

- 判定查询（例如询问 f(2,5) 是否等于 1）：
<query_judge>2,5,1</query_judge>

- 提交阶段1结束并进入阶段2：
<phase1_done></phase1_done>

- 挑战阶段提交答案（例如预测结果为模块 3）：
<answer>3</answer>

注意：
1. 归纳阶段的查询次数有限，请合理利用
2. 必须先提交 phase1_done 才能进入挑战阶段
3. 挑战阶段我会逐一给出组件对，你需要依次回答
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Industrial Product Assembly BOM Analysis System initiated. This product consists of {n} hierarchical components, with the top-level assembly being {root}. The assembly tree is as follows:
{tree_structure}

The system provides a module localization function f to retrieve the "lowest common assembly module" that incorporates any two components (u, v). This function has the following properties:
- For any component pair (u, v), f(u, v) returns a deterministic single assembly module ID
- Retrieval is order-independent; f(u, v) and f(v, u) are identical
- The BOM assembly structure remains constant during the analysis task

The analysis task has two phases:

**Phase 1 (Induction Phase)**: You may perform up to {Q} queries, choosing one of the following types each time:
1. Value Query: Submit a pair of components (a, b), and I will tell you the value of f(a, b).
2. Judge Query: Submit three components (a, b, c), and I will tell you whether f(a, b) equals c.

**Phase 2 (Challenge Phase)**: I will provide {M} new component pairs, and you must predict the f value for each pair one by one.
- Strict mode: All {M} answers must be correct to succeed.
- Lenient mode: At least {pass_count} correct answers are required to succeed.

This round uses {mode_text}.

You can only perform one query or submission at a time. Use the following XML format:

- Value Query (e.g., query components 2 and 5):
<query_value>2,5</query_value>

- Judge Query (e.g., ask if f(2,5) equals 1):
<query_judge>2,5,1</query_judge>

- Submit end of Phase 1 and enter Phase 2:
<phase1_done></phase1_done>

- Challenge phase answer submission (e.g., predict result is module 3):
<answer>3</answer>

Notes:
1. The number of queries in the induction phase is limited, use them wisely
2. You must submit phase1_done before entering the challenge phase
3. In the challenge phase, I will provide component pairs one by one, and you must answer sequentially
"""

    contextualized_rule_zh_5 = """\
【法律场景】
司法管辖权层级核查系统启动。本系统记录了一棵由 {n} 个司法机构节点构成的层级树，最高管辖法院编号为 {root}。管辖权架构如下：
{tree_structure}

系统内置了管辖权裁定函数 f，用于裁定任意两起案件/属地 (u, v) 对应的“最低级别共同管辖法院”。该函数具有以下性质：
- 对于任意管辖节点对 (u, v)，f(u, v) 返回确定的单一法院编号
- 裁定不受参数先后影响，即 f(u, v) 和 f(v, u) 相同
- 法院层级及管辖架构在核查期间保持不变

核查流程分为两个阶段：

**阶段1（归纳阶段）**：你最多可以进行 {Q} 次查询，每次查询可以选择以下两种方式之一：
1. 值查询：提交一对管辖节点 (a, b)，我会告诉你 f(a, b) 的值。
2. 判定查询：提交三个管辖节点 (a, b, c)，我会告诉你 f(a, b) 是否等于 c。

**阶段2（挑战阶段）**：我会提供 {M} 对新的管辖节点对，你需要逐一预测每对节点的 f 值。
- 严格模式：所有 {M} 题必须全部正确才算成功。
- 宽松模式：至少答对 {pass_count} 题即可成功。

本局采用{mode_text}。

每次只能进行一个查询或提交。请使用以下 XML 格式：

- 值查询（例如查询节点 2 和 5）：
<query_value>2,5</query_value>

- 判定查询（例如询问 f(2,5) 是否等于 1）：
<query_judge>2,5,1</query_judge>

- 提交阶段1结束并进入阶段2：
<phase1_done></phase1_done>

- 挑战阶段提交答案（例如预测结果为法院 3）：
<answer>3</answer>

注意：
1. 归纳阶段的查询次数有限，请合理利用
2. 必须先提交 phase1_done 才能进入挑战阶段
3. 挑战阶段我会逐一给出案件节点对，你需要依次回答
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Judicial Jurisdiction Hierarchy Verification System initiated. This system records a hierarchical tree of {n} judicial authority nodes, with the highest supreme court being {root}. The jurisdiction architecture is as follows:
{tree_structure}

The system features a jurisdiction adjudication function f to determine the "lowest common appellate court" for any two case jurisdictions (u, v). This function has the following properties:
- For any jurisdiction node pair (u, v), f(u, v) returns a deterministic single court ID
- Adjudication is order-independent; f(u, v) and f(v, u) are identical
- The court hierarchy and jurisdiction architecture remain constant during verification

The verification process has two phases:

**Phase 1 (Induction Phase)**: You may perform up to {Q} queries, choosing one of the following types each time:
1. Value Query: Submit a pair of jurisdiction nodes (a, b), and I will tell you the value of f(a, b).
2. Judge Query: Submit three jurisdiction nodes (a, b, c), and I will tell you whether f(a, b) equals c.

**Phase 2 (Challenge Phase)**: I will provide {M} new jurisdiction node pairs, and you must predict the f value for each pair one by one.
- Strict mode: All {M} answers must be correct to succeed.
- Lenient mode: At least {pass_count} correct answers are required to succeed.

This round uses {mode_text}.

You can only perform one query or submission at a time. Use the following XML format:

- Value Query (e.g., query jurisdictions 2 and 5):
<query_value>2,5</query_value>

- Judge Query (e.g., ask if f(2,5) equals 1):
<query_judge>2,5,1</query_judge>

- Submit end of Phase 1 and enter Phase 2:
<phase1_done></phase1_done>

- Challenge phase answer submission (e.g., predict result is court 3):
<answer>3</answer>

Notes:
1. The number of queries in the induction phase is limited, use them wisely
2. You must submit phase1_done before entering the challenge phase
3. In the challenge phase, I will provide jurisdiction node pairs one by one, and you must answer sequentially
"""

    tags = ["query_value", "query_judge", "phase1_done", "answer"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"n": 6, "root": 1, "edges": [(1,2), (1,3), (2,4), (2,5), (3,6)], "Q": 10, "M": 3, "strict": False, "challenges": [(4,5), (4,6), (5,6)]},
            2: {"n": 9, "root": 1, "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (4,8), (5,9)], "Q": 12, "M": 4, "strict": False, "challenges": [(8,9), (6,7), (4,6), (8,7)]},
            3: {"n": 10, "root": 1, "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (5,8), (6,9), (7,10)], "Q": 15, "M": 5, "strict": True, "challenges": [(8,9), (8,10), (4,10), (9,10), (4,6)]},
            4: {"n": 12, "root": 1, "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (4,8), (5,9), (6,10), (7,11), (8,12)], "Q": 12, "M": 6, "strict": True, "challenges": [(12,10), (9,11), (8,9), (10,11), (12,11), (4,10)]},
            5: {"n": 15, "root": 1, "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (4,8), (4,9), (5,10), (6,11), (6,12), (7,13), (9,14), (10,15)], "Q": 10, "M": 8, "strict": True, "challenges": [(14,15), (8,10), (11,13), (14,12), (15,11), (8,13), (9,15), (12,14)]},
        },
        "en": {
            1: {"n": 6, "root": 1, "edges": [(1,2), (1,3), (2,4), (2,5), (3,6)], "Q": 10, "M": 3, "strict": False, "challenges": [(4,5), (4,6), (5,6)]},
            2: {"n": 9, "root": 1, "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (4,8), (5,9)], "Q": 12, "M": 4, "strict": False, "challenges": [(8,9), (6,7), (4,6), (8,7)]},
            3: {"n": 10, "root": 1, "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (5,8), (6,9), (7,10)], "Q": 15, "M": 5, "strict": True, "challenges": [(8,9), (8,10), (4,10), (9,10), (4,6)]},
            4: {"n": 12, "root": 1, "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (4,8), (5,9), (6,10), (7,11), (8,12)], "Q": 12, "M": 6, "strict": True, "challenges": [(12,10), (9,11), (8,9), (10,11), (12,11), (4,10)]},
            5: {"n": 15, "root": 1, "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (4,8), (4,9), (5,10), (6,11), (6,12), (7,13), (9,14), (10,15)], "Q": 10, "M": 8, "strict": True, "challenges": [(14,15), (8,10), (11,13), (14,12), (15,11), (8,13), (9,15), (12,14)]},
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
        
        self._game_info["n"] = cfg["n"]
        self._game_info["root"] = cfg["root"]
        self._game_info["Q"] = cfg["Q"]
        self._game_info["M"] = cfg["M"]
        
        self.edges = cfg["edges"]
        self.root = cfg["root"]
        self.n = cfg["n"]
        
        self.tree = {i: [] for i in range(1, self.n + 1)}
        for u, v in self.edges:
            self.tree[u].append(v)
            self.tree[v].append(u)
        
        self.parent = {}
        self.depth = {}
        self._build_tree_info(self.root, None, 0)
        
        self._game_info["tree_structure"] = self._format_tree_structure()
        
        self.challenges = cfg["challenges"]
        self.strict_mode = cfg["strict"]
        self.pass_count = cfg["M"] if self.strict_mode else max(1, int(0.8 * cfg["M"]))
        
        self._game_info["pass_count"] = self.pass_count
        self._game_info["mode_text"] = "严格模式" if self.strict_mode else "宽松模式"
        if lang == "en":
            self._game_info["mode_text"] = "strict mode" if self.strict_mode else "lenient mode"
        
        self.phase = 1
        self.query_count = 0
        self.challenge_index = 0
        self.challenge_results = []

    def _build_tree_info(self, node, par, dep):
        self.parent[node] = par
        self.depth[node] = dep
        for child in self.tree[node]:
            if child != par:
                self._build_tree_info(child, node, dep + 1)

    def _format_tree_structure(self):
        if self.config.language == "zh":
            lines = [f"根节点：{self.root}"]
            lines.append("边（父→子）：" + ", ".join(f"{u}→{v}" for u, v in self.edges))
        else:
            lines = [f"Root: {self.root}"]
            lines.append("Edges (parent→child): " + ", ".join(f"{u}→{v}" for u, v in self.edges))
        return "\n".join(lines)

    def _lca(self, u, v):
        while self.depth[u] > self.depth[v]:
            u = self.parent[u]
        while self.depth[v] > self.depth[u]:
            v = self.parent[v]
        
        while u != v:
            u = self.parent[u]
            v = self.parent[v]
        
        return u

    def _validate_node(self, node_str):
        try:
            node = int(node_str)
            return 1 <= node <= self.n
        except:
            return False

    def evaluate(self, parsed_info):
        if self.phase != 2:
            return False
        
        if self.challenge_index >= len(self.challenges):
            return False
        
        try:
            answer = int(str(parsed_info.get("answer", "")).strip())
        except (ValueError, TypeError):
            return False
        
        u, v = self.challenges[self.challenge_index]
        correct_answer = self._lca(u, v)
        
        return answer == correct_answer

    def _cf_core_produce(self, parsed_info):
        is_zh = (self.config.language == "zh")
        
        if "phase1_done" in parsed_info:
            if self.phase != 1:
                return "错误：已经在挑战阶段。" if is_zh else "Error: Already in challenge phase."
            
            self.phase = 2
            self.challenge_index = 0
            self.challenge_results = []
            
            u, v = self.challenges[0]
            if is_zh:
                return f"归纳阶段结束，你共使用了 {self.query_count} 次查询。\n现在进入挑战阶段，请依次预测以下节点对的 f 值。\n第 1 题：f({u}, {v}) = ?"
            else:
                return f"Induction phase ended. You used {self.query_count} queries.\nNow entering challenge phase. Predict the f value for the following node pairs.\nQuestion 1: f({u}, {v}) = ?"
        
        if self.phase == 1:
            if self.query_count >= self._game_info["Q"]:
                return "错误：已达到最大查询次数限制。" if is_zh else "Error: Maximum query limit reached."
            
            if "query_value" in parsed_info:
                try:
                    raw = parsed_info["query_value"].strip()
                    parts = [x.strip() for x in raw.split(",")]
                    if len(parts) != 2:
                        raise ValueError
                    
                    u_str, v_str = parts
                    if not self._validate_node(u_str) or not self._validate_node(v_str):
                        raise ValueError
                    
                    u, v = int(u_str), int(v_str)
                    result = self._lca(u, v)
                    self.query_count += 1
                    
                    if is_zh:
                        return f"节点：{result}"
                    else:
                        return f"Node: {result}"
                    
                except:
                    return "无效请求：格式错误或节点不存在。" if is_zh else "Invalid request: format error or node does not exist."
            
            elif "query_judge" in parsed_info:
                try:
                    raw = parsed_info["query_judge"].strip()
                    parts = [x.strip() for x in raw.split(",")]
                    if len(parts) != 3:
                        raise ValueError
                    
                    u_str, v_str, c_str = parts
                    if not all(self._validate_node(x) for x in [u_str, v_str, c_str]):
                        raise ValueError
                    
                    u, v, c = int(u_str), int(v_str), int(c_str)
                    result = self._lca(u, v)
                    self.query_count += 1
                    
                    if result == c:
                        return "是" if is_zh else "Yes"
                    else:
                        return "否" if is_zh else "No"
                    
                except:
                    return "无效请求：格式错误或节点不存在。" if is_zh else "Invalid request: format error or node does not exist."
        
        elif self.phase == 2:
            if self.challenge_index < len(self.challenges):
                u, v = self.challenges[self.challenge_index]
                if is_zh:
                    return f"第 {self.challenge_index + 1} 题：f({u}, {v}) = ?"
                else:
                    return f"Question {self.challenge_index + 1}: f({u}, {v}) = ?"
            else:
                correct_count = sum(self.challenge_results)
                if is_zh:
                    return f"挑战阶段完成！正确数：{correct_count}/{len(self.challenges)}"
                else:
                    return f"Challenge phase completed! Correct: {correct_count}/{len(self.challenges)}"
        
        return "无效请求。" if is_zh else "Invalid request."

    def _cf_make_wrong(self, correct: str) -> str:
        match = re.search(r'\d+', correct)
        if match:
            num = int(match.group())
            wrong_num = num + 1 if num < self.n else num - 1
            if wrong_num < 1:
                wrong_num = 2
            return correct[:match.start()] + str(wrong_num) + correct[match.end():]
        
        if "是" in correct:
            return correct.replace("是", "否")
        if "否" in correct:
            return correct.replace("否", "是")
            
        if "Yes" in correct: return correct.replace("Yes", "No")
        if "No" in correct: return correct.replace("No", "Yes")
        if "yes" in correct: return correct.replace("yes", "no")
        if "no" in correct: return correct.replace("no", "yes")

        return correct + "_WRONG"
    
    def get_all_possible_queries(self) -> List[Dict[str, str]]:
        queries = []
        is_zh = self.config.language == "zh"
        
        for u in range(1, self.n + 1):
            for v in range(u, self.n + 1):
                res = self._lca(u, v)
                
                query_content = f"<query_value>{u},{v}</query_value>"
                
                if is_zh:
                    answer = f"节点：{res}"
                else:
                    answer = f"Node: {res}"
                
                queries.append({
                    "query": query_content,
                    "answer": answer
                })
        
        return queries

    def step(self, response: str):
        try:
            parsed_info = self.parse(response)
            
            if "answer" in parsed_info:
                if self.phase != 2:
                    res = "错误：当前不在挑战阶段，无法提交答案。" if self.config.language == "zh" else "Error: Not in challenge phase, cannot submit answer."
                    self.state.add_message("user", res)
                    self.state.set_state("failed", "answer submitted in wrong phase")
                else:
                    is_correct = self.evaluate(parsed_info)
                    
                    self.challenge_results.append(is_correct)
                    self.challenge_index += 1
                    
                    if is_correct:
                        res = "正确！" if self.config.language == "zh" else "Correct!"
                    else:
                        u, v = self.challenges[self.challenge_index - 1]
                        correct_ans = self._lca(u, v)
                        if self.config.language == "zh":
                            res = f"错误！正确答案是 {correct_ans}。"
                        else:
                            res = f"Incorrect! The correct answer is {correct_ans}."
                    
                    if self.challenge_index < len(self.challenges):
                        u, v = self.challenges[self.challenge_index]
                        if self.config.language == "zh":
                            res += f"\n第 {self.challenge_index + 1} 题：f({u}, {v}) = ?"
                        else:
                            res += f"\nQuestion {self.challenge_index + 1}: f({u}, {v}) = ?"
                        self.state.add_message("user", res)
                    else:
                        correct_count = sum(self.challenge_results)
                        if self.config.language == "zh":
                            res += f"\n挑战阶段完成！正确数：{correct_count}/{len(self.challenges)}"
                        else:
                            res += f"\nChallenge phase completed! Correct: {correct_count}/{len(self.challenges)}"
                        
                        self.state.add_message("user", res)
                        
                        if correct_count >= self.pass_count:
                            self.state.set_state("success", "challenge completed")
                        else:
                            self.state.set_state("failed", f"only {correct_count}/{len(self.challenges)} correct")
                    
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            if self.config.language == "zh":
                self.state.add_message("user", f"解析失败：{str(e)}")
            else:
                self.state.add_message("user", f"Parse failed: {str(e)}")
            self.state.set_state("failed", str(e))
        
        return self.state