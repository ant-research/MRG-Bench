# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   最近公共祖先：两个给定节点的最近公共祖先是哪个节点
# ============================================================

from .base import Game
import random


class LCAAbductionGame(Game):

    game_rule_zh = """\
我们来玩一个"未知反馈函数下的树结构推理"游戏。规则如下：

## 游戏背景

存在一棵包含 15 个节点的有根树，节点编号为 N0 到 N14，其中 N0 是根节点。树的结构如下：

- N0 的子节点：N1, N2, N3
- N1 的子节点：N4, N5
- N4 的子节点：N6, N7
- N5 的子节点：N8
- N2 的子节点：N9, N10
- N9 的子节点：N11
- N10 的子节点：N12, N13
- N3 的子节点：N14

## 游戏目标

你的最终目标是：
1. 通过提问推断出当前使用的反馈函数类型（A、B、C 或 D 中的一种）
2. 给出目标节点对 (N6, N8) 的真实最近公共祖先（LCA）

## 反馈函数说明

系统内部使用了一个固定但未知的反馈函数 f，它属于以下四种类型之一。在整个游戏过程中，该函数类型保持不变：

- **类型 A**：对于查询 (u, v)，返回 u 和 v 的真实最近公共祖先
- **类型 B**：对于查询 (u, v)，如果 LCA(u, v) 等于 u，则返回 u；否则返回从 LCA(u, v) 到 u 的路径上紧邻 LCA 的子节点
- **类型 C**：对于查询 (u, v)，如果 LCA(u, v) 的父节点存在，则返回该父节点；否则返回根节点
- **类型 D**：对于查询 (u, v)，如果 LCA(u, v) 等于 v，则返回 v；否则返回从 LCA(u, v) 到 v 的路径上紧邻 LCA 的子节点

## 交互方式

你可以通过提问来收集信息。每次提问的格式为 Query(u, v)，其中 u 和 v 是节点编号（注意顺序重要）。系统会根据当前的反馈函数返回一个节点编号。

## 格式要求

**提问格式**（查询节点对 u 和 v）：
<query>u,v</query>

**提交最终答案格式**（必须同时给出反馈函数类型和 LCA）：
<answer>function=X, lca=Ni</answer>

其中 X 为 A、B、C 或 D 之一，Ni 为节点编号（如 N1）。

## 注意事项

- 请尽可能少地进行提问以推断出反馈函数类型
- 只有在充分确信时才提交最终答案
- 答案格式必须严格符合要求，否则视为失败
"""

    game_rule_en = """\
Let's play a "Tree Structure Reasoning with Unknown Feedback Function" game. Here are the rules:

## Game Background

There is a rooted tree with 15 nodes, labeled N0 to N14, where N0 is the root. The tree structure is:

- N0's children: N1, N2, N3
- N1's children: N4, N5
- N4's children: N6, N7
- N5's children: N8
- N2's children: N9, N10
- N9's children: N11
- N10's children: N12, N13
- N3's children: N14

## Game Objective

Your ultimate goal is to:
1. Infer the type of feedback function (one of A, B, C, or D) through queries
2. Provide the true Lowest Common Ancestor (LCA) of the target node pair (N6, N8)

## Feedback Function Description

The system uses a fixed but unknown feedback function f, which is one of the following four types. The function type remains constant throughout the game:

- **Type A**: For query (u, v), returns the true lowest common ancestor of u and v
- **Type B**: For query (u, v), if LCA(u, v) equals u, returns u; otherwise returns the child of LCA(u, v) on the path to u
- **Type C**: For query (u, v), if the parent of LCA(u, v) exists, returns that parent; otherwise returns the root
- **Type D**: For query (u, v), if LCA(u, v) equals v, returns v; otherwise returns the child of LCA(u, v) on the path to v

## Interaction

You can gather information by asking queries. Each query is in the form Query(u, v), where u and v are node labels (note: order matters). The system will return a node label based on the current feedback function.

## Format Requirements

**Query format** (to query node pair u and v):
<query>u,v</query>

**Final answer format** (must provide both function type and LCA):
<answer>function=X, lca=Ni</answer>

where X is one of A, B, C, or D, and Ni is a node label (e.g., N1).

## Notes

- Try to use as few queries as possible to infer the feedback function type
- Only submit your final answer when you are confident
- Answer format must strictly comply with requirements, otherwise it will be considered a failure
"""

    contextualized_rule_zh_1 = """\
欢迎使用“城市轨道交通网络层级溯源系统”。我们来玩一个未知指令反馈机制下的层级推理游戏。

## 业务背景

存在一棵包含 15 个层级控制节点的轨道调度树，编号 N0 到 N14，N0 为总调度中心。拓扑结构如下：

- N0 的下级区域中心：N1, N2, N3
- N1 的下级枢纽：N4, N5
- N4 的下级站点：N6, N7
- N5 的下级站点：N8
- N2 的下级枢纽：N9, N10
- N9 的下级站点：N11
- N10 的下级站点：N12, N13
- N3 的下级站点：N14

## 业务目标

1. 通过提问推断出当前采用的指令下达反馈机制（A、B、C 或 D 中的一种）
2. 给出目标节点对 (N6, N8) 的真实最近公共上级调度节点（LCA）

## 反馈机制说明

系统固定使用了一种未知的反馈机制，它属于以下四种类型之一：

- **类型 A**：对于查询 (u, v)，返回 u 和 v 的真实最近公共上级节点
- **类型 B**：对于查询 (u, v)，如果 LCA(u, v) 等于 u，则返回 u；否则返回从 LCA 向 u 下达指令路径上的紧邻下级节点
- **类型 C**：对于查询 (u, v)，如果 LCA 存在更上一级监管机构，则返回该级；否则返回总调度中心（N0）
- **类型 D**：对于查询 (u, v)，如果 LCA(u, v) 等于 v，则返回 v；否则返回从 LCA 向 v 下达指令路径上的紧邻下级节点

## 交互方式

你可以通过提问探测系统。每次提问格式为 Query(u, v)，其中 u 和 v 是节点编号（顺序重要）。系统将返回一个节点编号。

## 格式要求

**提问格式**（查询节点对 u 和 v）：
<query>u,v</query>

**提交最终答案格式**：
<answer>function=X, lca=Ni</answer>

其中 X 为 A、B、C 或 D，Ni 为节点编号（如 N1）。

## 注意事项

- 请尽可能少地提问以推断机制
- 只有在充分确信时才提交最终答案
- 答案格式必须严格符合要求，否则视为失败
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Urban Rail Transit Network Hierarchy Tracing System". Let's play a hierarchy reasoning game with an unknown instruction feedback mechanism.

## Business Background

There is a rail scheduling tree with 15 hierarchical control nodes, labeled N0 to N14, where N0 is the main dispatch center. The topology is:

- N0's regional centers: N1, N2, N3
- N1's sub-hubs: N4, N5
- N4's stations: N6, N7
- N5's stations: N8
- N2's sub-hubs: N9, N10
- N9's stations: N11
- N10's stations: N12, N13
- N3's stations: N14

## Business Objective

1. Infer the current instruction dispatch feedback mechanism (Type A, B, C, or D) through queries.
2. Identify the true lowest common supervisory node (LCA) for the terminal node pair (N6, N8).

## Feedback Mechanism Description

The system uses a fixed but unknown feedback mechanism of one of four types:

- **Type A**: For query (u, v), returns the true lowest common supervisory node of u and v.
- **Type B**: For query (u, v), if LCA(u,v) is u, returns u; otherwise, returns the immediate child node of LCA on the dispatch path towards u.
- **Type C**: For query (u, v), if a higher-level supervisory authority of the LCA exists, returns it; otherwise, returns the main dispatch center (N0).
- **Type D**: For query (u, v), if LCA(u,v) is v, returns v; otherwise, returns the immediate child node of LCA on the dispatch path towards v.

## Interaction

You can gather information by asking queries. Each query is Query(u, v) (order matters). The system returns a node label.

## Format Requirements

**Query format**:
<query>u,v</query>

**Final answer format**:
<answer>function=X, lca=Ni</answer>

(X is A, B, C, or D; Ni is a node label, e.g., N1).

## Notes
- Use as few queries as possible.
- Submit final answer only when confident.
- Strictly comply with formats.
"""

    contextualized_rule_zh_2 = """\
欢迎登录“医疗机构病症溯源与科室协同平台”。我们来玩一个未知反馈机制下的科室层级推理测试。

## 业务背景

存在一棵包含 15 个科室/中心的管理架构树，编号 N0 到 N14，N0 为院级决策委员会。结构如下：

- N0 的下级分管中心：N1, N2, N3
- N1 的下属大科室：N4, N5
- N4 的下属专科：N6, N7
- N5 的下属专科：N8
- N2 的下属大科室：N9, N10
- N9 的下属专科：N11
- N10 的下属专科：N12, N13
- N3 的下属专科：N14

## 业务目标

1. 通过系统问询推断出当前的跨科室资源分配反馈协议（A、B、C 或 D）
2. 找出目标科室对 (N6, N8) 的真实最近共同主管中心（LCA）

## 反馈协议说明

系统使用未知的固定分配反馈协议：

- **类型 A**：对于查询 (u, v)，直接返回 u 和 v 的真实最近共同主管中心
- **类型 B**：对于查询 (u, v)，若 LCA 等于 u，则返回 u；否则返回从 LCA 向 u 分配资源路径上的紧邻下属中心
- **类型 C**：对于查询 (u, v)，若 LCA 存在更上级的监督机构，则返回该机构；否则返回决策委员会 N0
- **类型 D**：对于查询 (u, v)，若 LCA 等于 v，则返回 v；否则返回从 LCA 向 v 分配资源路径上的紧邻下属中心

## 交互与格式

**提问格式**：
<query>u,v</query>

**诊断报告提交格式**：
<answer>function=X, lca=Ni</answer>
（X为A/B/C/D，Ni为节点编号）

请尽量少地提问并在确信时给出规范的最终结论。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Medical Institution Disease Tracing and Department Synergy Platform". Let's conduct a department hierarchy reasoning test under an unknown feedback mechanism.

## Business Background

There is a management architecture tree of 15 departments/centers, labeled N0 to N14, where N0 is the hospital-level decision committee. The structure is:

- N0's branch centers: N1, N2, N3
- N1's main departments: N4, N5
- N4's specialized clinics: N6, N7
- N5's specialized clinics: N8
- N2's main departments: N9, N10
- N9's specialized clinics: N11
- N10's specialized clinics: N12, N13
- N3's specialized clinics: N14

## Business Objective

1. Infer the current cross-department resource allocation feedback protocol (Type A, B, C, or D).
2. Identify the true lowest common managing center (LCA) for the target department pair (N6, N8).

## Feedback Protocol Description

The system uses a fixed but unknown feedback protocol:

- **Type A**: Returns the true lowest common managing center of u and v.
- **Type B**: If LCA is u, returns u; otherwise, returns the immediate subordinate center of LCA on the resource allocation path towards u.
- **Type C**: If a higher-level supervisory institution of the LCA exists, returns it; otherwise, returns the decision committee (N0).
- **Type D**: If LCA is v, returns v; otherwise, returns the immediate subordinate center of LCA on the resource allocation path towards v.

## Interaction & Format

**Query format**:
<query>u,v</query>

**Diagnosis report submission format**:
<answer>function=X, lca=Ni</answer>
(X is A/B/C/D, Ni is a node label)

Please ask as few queries as possible and submit only when confident.
"""

    contextualized_rule_zh_3 = """\
欢迎使用“基础教育学科知识图谱分析工具”。请完成一次未知定位策略下的图谱推演。

## 业务背景

存在一棵包含 15 个知识模块的层级分类树，编号 N0 到 N14，N0 为核心素养总纲。结构如下：

- N0 的下级学科大类：N1, N2, N3
- N1 的下级主题：N4, N5
- N4 的下级知识点：N6, N7
- N5 的下级知识点：N8
- N2 的下级主题：N9, N10
- N9 的下级知识点：N11
- N10 的下级知识点：N12, N13
- N3 的下级知识点：N14

## 业务目标

1. 诊断出该图谱接口当前采用的知识模块检索策略（A、B、C 或 D 类）
2. 确诊目标知识模块对 (N6, N8) 的真实最近共同归属模块（LCA）

## 检索策略说明

- **类型 A**：对于查询 (u, v)，返回 u 和 v 的真实最近共同归属模块
- **类型 B**：若 LCA 等于 u，则返回 u；否则返回从共同模块向 u 细分延伸路径上的次级大类
- **类型 C**：若 LCA 的上位统筹模块存在，则返回该上位模块；否则返回总纲 N0
- **类型 D**：若 LCA 等于 v，则返回 v；否则返回从共同模块向 v 细分延伸路径上的次级大类

## 交互与格式

**检索调用格式**：
<query>u,v</query>

**最终分析结论**：
<answer>function=X, lca=Ni</answer>
（X为A/B/C/D，Ni为节点编号）

请保持提问精简，在确诊后提交标准格式结论。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Basic Education Subject Knowledge Graph Analysis Tool". Please complete a graph deduction task under an unknown locating strategy.

## Business Background

There is a hierarchical classification tree of 15 knowledge modules, labeled N0 to N14, with N0 as the core literacy general outline. The structure is:

- N0's subject categories: N1, N2, N3
- N1's topics: N4, N5
- N4's knowledge points: N6, N7
- N5's knowledge points: N8
- N2's topics: N9, N10
- N9's knowledge points: N11
- N10's knowledge points: N12, N13
- N3's knowledge points: N14

## Business Objective

1. Diagnose the current knowledge module retrieval strategy used by the graph interface (Type A, B, C, or D).
2. Determine the true lowest common parent module (LCA) for the target module pair (N6, N8).

## Retrieval Strategy Description

- **Type A**: Returns the true lowest common parent module of u and v.
- **Type B**: If LCA is u, returns u; otherwise, returns the immediate sub-category on the subdivision path from LCA towards u.
- **Type C**: If a higher-level coordinating module of the LCA exists, returns it; otherwise, returns the general outline (N0).
- **Type D**: If LCA is v, returns v; otherwise, returns the immediate sub-category on the subdivision path from LCA towards v.

## Interaction & Format

**Retrieval call format**:
<query>u,v</query>

**Final analysis conclusion**:
<answer>function=X, lca=Ni</answer>
(X is A/B/C/D, Ni is a node label)

Keep queries concise and submit the standard format conclusion upon confirmation.
"""

    contextualized_rule_zh_4 = """\
欢迎进入“精密机械物料装配清单(BOM)解析系统”。系统已启动未知定位算法的逆向推导环境。

## 业务背景

存在一棵包含 15 个组件的装配关系树，编号 N0 到 N14，N0 为最终成品。结构如下：

- N0 的直接装配件：N1, N2, N3
- N1 的子组件：N4, N5
- N4 的底层零件：N6, N7
- N5 的底层零件：N8
- N2 的子组件：N9, N10
- N9 的底层零件：N11
- N10 的底层零件：N12, N13
- N3 的底层零件：N14

## 业务目标

1. 逆向推导出当前工艺查询系统所使用的组件定位算法（A、B、C 或 D 类）
2. 明确零件对 (N6, N8) 的真实最小共同装配组件（LCA）

## 定位算法说明

- **类型 A**：对于查询 (u, v)，返回 u 和 v 的真实最小共同装配组件
- **类型 B**：若 LCA 等于 u，则返回 u；否则返回从共同组件沿装配树向下分解到 u 路径上的第一级子组件
- **类型 C**：若该共同组件存在上级父组件，则返回该父组件；否则返回成品 N0
- **类型 D**：若 LCA 等于 v，则返回 v；否则返回从共同组件沿装配树向下分解到 v 路径上的第一级子组件

## 交互与格式

**BOM查询接口**：
<query>u,v</query>

**工艺解析报告**：
<answer>function=X, lca=Ni</answer>
（X为A/B/C/D，Ni为节点编号）

请优化查询步数，并在确认算法后提交符合规范的解析报告。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the "Precision Machinery Bill of Materials (BOM) Analysis System". The reverse-engineering environment for the unknown locating algorithm has started.

## Business Background

There is an assembly relationship tree of 15 components, labeled N0 to N14, with N0 as the final product. The structure is:

- N0's direct assemblies: N1, N2, N3
- N1's sub-assemblies: N4, N5
- N4's base parts: N6, N7
- N5's base parts: N8
- N2's sub-assemblies: N9, N10
- N9's base parts: N11
- N10's base parts: N12, N13
- N3's base parts: N14

## Business Objective

1. Reverse-engineer the component locating algorithm currently used by the process query system (Type A, B, C, or D).
2. Clarify the true lowest common assembly component (LCA) for the part pair (N6, N8).

## Locating Algorithm Description

- **Type A**: Returns the true lowest common assembly component of u and v.
- **Type B**: If LCA is u, returns u; otherwise, returns the first-level sub-assembly on the breakdown path from LCA down to u.
- **Type C**: If a parent assembly of the LCA exists, returns it; otherwise, returns the final product (N0).
- **Type D**: If LCA is v, returns v; otherwise, returns the first-level sub-assembly on the breakdown path from LCA down to v.

## Interaction & Format

**BOM query interface**:
<query>u,v</query>

**Process analysis report**:
<answer>function=X, lca=Ni</answer>
(X is A/B/C/D, Ni is a node label)

Optimize your query steps and submit the standard report once the algorithm is confirmed.
"""

    contextualized_rule_zh_5 = """\
欢迎启动“司法判例与法源层级推演系统”。接下来将进行未知法源援引规则的质证演练。

## 业务背景

存在一棵包含 15 个条款的法律体系树，编号 N0 到 N14，N0 为基本法总则。层级结构如下：

- N0 的下位解释法：N1, N2, N3
- N1 的延伸法条：N4, N5
- N4 的具体条款：N6, N7
- N5 的具体条款：N8
- N2 的延伸法条：N9, N10
- N9 的具体条款：N11
- N10 的具体条款：N12, N13
- N3 的具体条款：N14

## 业务目标

1. 质证并推断出当前法条检索库采用的法源援引规则（A、B、C 或 D 类）
2. 裁定目标条款对 (N6, N8) 的真实最近共同上位法源（LCA）

## 援引规则说明

- **类型 A**：对于查询 (u, v)，直接返回 u 和 v 的真实最近共同上位法源
- **类型 B**：若 LCA 等于 u，则返回 u；否则返回从共同上位法向 u 解释延伸路径上的第一级下位法条
- **类型 C**：若该共同上位法存在更高阶的授权法源，则返回更高阶法源；否则返回基本法总则 N0
- **类型 D**：若 LCA 等于 v，则返回 v；否则返回从共同上位法向 v 解释延伸路径上的第一级下位法条

## 交互与格式

**法条查询申请**：
<query>u,v</query>

**最终裁判文书**：
<answer>function=X, lca=Ni</answer>
（X为A/B/C/D，Ni为条款编号）

请在证据充分前控制查询次数，一旦得出结论，务必按格式要求提交文书。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Judicial Precedent and Legal Source Hierarchy Deduction System". A cross-examination drill with unknown source citation rules will now begin.

## Business Background

There is a legal system tree of 15 clauses, labeled N0 to N14, where N0 is the general principles of the Basic Law. The hierarchy is:

- N0's subordinate interpretation laws: N1, N2, N3
- N1's extension articles: N4, N5
- N4's specific clauses: N6, N7
- N5's specific clauses: N8
- N2's extension articles: N9, N10
- N9's specific clauses: N11
- N10's specific clauses: N12, N13
- N3's specific clauses: N14

## Business Objective

1. Cross-examine and infer the legal source citation rule currently adopted by the retrieval database (Type A, B, C, or D).
2. Rule on the true lowest common superior legal source (LCA) for the target clause pair (N6, N8).

## Citation Rule Description

- **Type A**: Returns the true lowest common superior legal source of u and v.
- **Type B**: If LCA is u, returns u; otherwise, returns the first-level subordinate article on the interpretive extension path from the LCA towards u.
- **Type C**: If a higher-order authorizing source of the LCA exists, returns it; otherwise, returns the general principles (N0).
- **Type D**: If LCA is v, returns v; otherwise, returns the first-level subordinate article on the interpretive extension path from the LCA towards v.

## Interaction & Format

**Clause query application**:
<query>u,v</query>

**Final ruling document**:
<answer>function=X, lca=Ni</answer>
(X is A/B/C/D, Ni is a clause label)

Control the number of queries before sufficient evidence is gathered, and submit the document strictly in the required format once concluded.
"""

    tags = ["answer", "query"]
    
    reasoning_type = "溯因推理"
    data_structure = "树"
    enable_counterfactual = False   # 设为 True 时开启反事实干预模式

    # 难度配置说明：
    # 1 (简单)       - 函数类型 A（最直接），目标对 (N6, N8)
    # 2 (中等偏下)   - 函数类型 C（需要理解父节点关系），目标对 (N6, N8)
    # 3 (中等偏上)   - 函数类型 B（需要理解路径方向），目标对 (N6, N8)
    # 4 (较难)       - 函数类型 D（需要理解反向路径），目标对 (N6, N8)
    # 5 (难)         - 随机函数类型，目标对 (N6, N8)

    DIFFICULTY_CONFIG = {
        1: {
            "function_type": "A",
            "target_pair": ("N6", "N8"),
            "true_lca": "N1",
        },
        2: {
            "function_type": "C",
            "target_pair": ("N6", "N8"),
            "true_lca": "N1",
        },
        3: {
            "function_type": "B",
            "target_pair": ("N6", "N8"),
            "true_lca": "N1",
        },
        4: {
            "function_type": "D",
            "target_pair": ("N6", "N8"),
            "true_lca": "N1",
        },
        5: {
            "function_type": "random",  # 将在初始化时随机选择
            "target_pair": ("N6", "N8"),
            "true_lca": "N1",
        },
    }

    def __init__(self, config):
        # 树结构定义（父节点映射）
        self.parent_map = {
            "N0": None,
            "N1": "N0", "N2": "N0", "N3": "N0",
            "N4": "N1", "N5": "N1",
            "N6": "N4", "N7": "N4",
            "N8": "N5",
            "N9": "N2", "N10": "N2",
            "N11": "N9",
            "N12": "N10", "N13": "N10",
            "N14": "N3",
        }
        
        # 子节点映射
        self.children_map = {
            "N0": ["N1", "N2", "N3"],
            "N1": ["N4", "N5"],
            "N2": ["N9", "N10"],
            "N3": ["N14"],
            "N4": ["N6", "N7"],
            "N5": ["N8"],
            "N9": ["N11"],
            "N10": ["N12", "N13"],
            "N6": [], "N7": [], "N8": [],
            "N11": [], "N12": [], "N13": [], "N14": [],
        }
        
        self.query_count = 0
        super().__init__(config)

    def _initialize_game(self):
        diff = self.config.difficulty
        
        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")
        
        cfg = self.DIFFICULTY_CONFIG[diff]
        
        # 处理随机函数类型
        if cfg["function_type"] == "random":
            self.function_type = random.choice(["A", "B", "C", "D"])
        else:
            self.function_type = cfg["function_type"]
        
        self.target_pair = cfg["target_pair"]
        self.true_lca = cfg["true_lca"]
        
        # 用于规则模板的占位符（本游戏中树结构固定，无需动态填充）
        self._game_info = {}

        self._cf_round_counter = 0          # produce_response 调用轮次计数
        self._cf_correct_resp  = None       # 第 2 轮的正确答案（暂存）
        self._cf_wrong_resp    = None       # 第 2 轮注入的错误答案（暂存）

    def _get_path_to_root(self, node):
        """获取从节点到根的路径"""
        path = []
        current = node
        while current is not None:
            path.append(current)
            current = self.parent_map[current]
        return path

    def _compute_true_lca(self, u, v):
        """计算真实的最近公共祖先"""
        path_u = self._get_path_to_root(u)
        path_v = self._get_path_to_root(v)
        
        # 从根开始找第一个分叉点的前一个节点
        path_u_set = set(path_u)
        for node in path_v:
            if node in path_u_set:
                return node
        return "N0"  # 默认返回根

    def _get_child_on_path(self, lca, target):
        """获取从 LCA 到 target 路径上紧邻 LCA 的子节点"""
        path = self._get_path_to_root(target)
        path.reverse()  # 从根到目标
        
        try:
            lca_idx = path.index(lca)
            if lca_idx + 1 < len(path):
                return path[lca_idx + 1]
        except ValueError:
            pass
        return lca

    def _apply_feedback_function(self, u, v):
        """根据当前函数类型计算反馈"""
        lca = self._compute_true_lca(u, v)
        
        if self.function_type == "A":
            return lca
        
        elif self.function_type == "B":
            if lca == u:
                return u
            else:
                return self._get_child_on_path(lca, u)
        
        elif self.function_type == "C":
            parent = self.parent_map[lca]
            if parent is not None:
                return parent
            else:
                return "N0"
        
        elif self.function_type == "D":
            if lca == v:
                return v
            else:
                return self._get_child_on_path(lca, v)
        
        else:
            raise ValueError(f"Unknown function type: {self.function_type}")

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        # 检查是否至少进行了3次查询
        if self.query_count < 3:
            return False
        
        # 解析答案
        raw_ans = parsed_info["answer"]
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            parts = kv.split("=", 1)
            if len(parts) == 2:
                k, v = parts
                ans_dict[k.strip()] = v.strip()
        
        if "function" not in ans_dict or "lca" not in ans_dict:
            return False
        
        # 检查函数类型是否正确
        if ans_dict["function"] != self.function_type:
            return False
        
        # 检查 LCA 是否正确
        if ans_dict["lca"] != self.true_lca:
            return False
        
        return True

    def produce_response(self, parsed_info):
        """处理查询并返回反馈（包含反事实干预逻辑）"""
        if self.enable_counterfactual:
            self._cf_round_counter += 1

            if self._cf_round_counter == 2:
                # 先用原逻辑得到正确答案，暂存后返回错误答案
                correct = self._cf_core_produce(parsed_info)
                self._cf_correct_resp = correct
                self._cf_wrong_resp   = self._cf_make_wrong(correct)
                return self._cf_wrong_resp

            elif self._cf_round_counter == 3:
                # 本轮不执行原逻辑，只返回纠正说明
                return self._cf_correction_message()

        return self._cf_core_produce(parsed_info)

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑：处理查询并返回反馈"""
        if "query" not in parsed_info:
            raise ValueError("No valid query found.")
        
        try:
            raw = parsed_info["query"].strip()
            parts = [x.strip() for x in raw.split(",")]
            if len(parts) != 2:
                raise ValueError("Query must contain exactly two nodes.")
            
            u, v = parts[0], parts[1]
            
            # 验证节点是否有效
            if u not in self.parent_map or v not in self.parent_map:
                if self.config.language == "zh":
                    return "错误：节点编号无效。"
                else:
                    return "Error: Invalid node label."
            
            # 增加查询计数
            self.query_count += 1
            
            # 计算并返回反馈
            result = self._apply_feedback_function(u, v)
            return result
            
        except Exception as e:
            if self.config.language == "zh":
                return f"错误：查询格式无效。{str(e)}"
            else:
                return f"Error: Invalid query format. {str(e)}"

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        lower_correct = correct.lower()
        if "是" in correct:
            return correct.replace("是", "否")
        elif "否" in correct:
            return correct.replace("否", "是")
        elif "yes" in lower_correct:
            if correct.isupper(): return correct.replace("YES", "NO")
            if correct.islower(): return correct.replace("yes", "no")
            return correct.replace("Yes", "No")
        elif "no" in lower_correct:
            if correct.isupper(): return correct.replace("NO", "YES")
            if correct.islower(): return correct.replace("no", "yes")
            return correct.replace("No", "Yes")
        else:
            return correct + "_WRONG"

    def _cf_correction_message(self) -> str:
        wrong = self._cf_wrong_resp
        correct = self._cf_correct_resp
        
        if self.config.language == "zh":
            return (f"【纠正】上一轮的回复有误。错误答案为：\"{wrong}\"，正确答案应为：\"{correct}\"。\n"
                    f"请基于正确信息重新开始提问。")
        else:
            return (f"[Correction] The previous response was incorrect. Wrong answer: \"{wrong}\"; Correct answer: \"{correct}\".\n"
                    f"Please restart your questioning based on the correct information.")

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
        queries = []
        # 树中共有 15 个节点，编号 N0 到 N14
        nodes = [f"N{i}" for i in range(15)]
        
        # 遍历所有可能的 (u, v) 组合
        # 注意：根据游戏规则，Query(u, v) 中顺序重要，且 u, v 是节点编号
        # 规则并未明确禁止 u == v，且反馈函数对 u==v 也有定义（如 A类返回本身，B/D类有 LCA==u/v 的判断）
        # 因此包含所有排列
        for u in nodes:
            for v in nodes:
                # 构造查询内容，格式为 "u,v"
                query_content = f"{u},{v}"
                
                # 调用内部函数计算结果
                # 注意：_apply_feedback_function 依赖当前游戏难度配置（self.function_type）
                # 该函数无副作用，不改变游戏状态
                try:
                    ans = self._apply_feedback_function(u, v)
                    queries.append({
                        "query": query_content,
                        "answer": str(ans)
                    })
                except Exception:
                    # 忽略任何可能的异常（虽然基于固定逻辑不应发生）
                    pass
                    
        return queries