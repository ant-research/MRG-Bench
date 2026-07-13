# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   根节点：整棵树的根节点是哪个
# ============================================================

import random
from .base import Game


class HiddenTreeRootGame(Game):

    game_rule_zh = """\
我们现在来玩一个"隐藏树根"的推理游戏，规则如下：

游戏设定了一棵包含 {n} 个节点的有根树（连通无环图），节点名称为：{node_names}。树的根节点已被秘密选定，但不会告诉你。树中存在从根节点向外指向子节点的有向关系，形成了祖先—后代关系。

你的目标是通过询问推断出这棵树的根节点。你可以反复向我提出以下类型的问题：

- Reach 查询：询问节点 u 是否为节点 v 的祖先（包括 u 等于 v 的情况）。我会回答"是"或"否"。

你需要在收集足够信息后提交最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问使用以下 XML 格式：

- Reach 查询（例如询问节点 A 是否为节点 B 的祖先）：
<query_reach>A,B</query_reach>

提交最终答案时，指定你认为的根节点名称，格式如下：

<answer>Root=A</answer>

注意：请尽可能少地进行查询，在确定答案后即可提交。
"""

    game_rule_en = """\
Let's play a "Hidden Tree Root" deduction game. Here are the rules:

The game has set up a rooted tree (connected acyclic graph) containing {n} nodes with names: {node_names}. The root node has been secretly chosen but will not be revealed to you. The tree has directed relationships from the root outward to child nodes, forming ancestor-descendant relationships.

Your goal is to deduce the root node of this tree through queries. You can repeatedly ask me the following type of question:

- Reach Query: Ask whether node u is an ancestor of node v (including the case where u equals v). I will answer "Yes" or "No".

You need to submit your final answer after collecting enough information. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (must be strictly followed)

Each query uses the following XML format:

- Reach Query (e.g., asking if node A is an ancestor of node B):
<query_reach>A,B</query_reach>

When submitting the final answer, specify the root node name you believe is correct, using this format:

<answer>Root=A</answer>

Note: Please use as few queries as possible and submit once you are confident of the answer.
"""

    contextualized_rule_zh_1 = """\
我们在进行一项"追踪总调度中心"的交通流向排查任务。

当前交通网络包含 {n} 个路口节点，名称为：{node_names}。道路均为单向行驶，且呈现出从某一个隐藏的"总调度中心"向外发散的无环树状结构。

你的目标是通过查询上下游关系，找出这个"总调度中心"。你可以反复向我提出以下查询：

- Reach 查询：询问路口 u 是否为路口 v 的上游（即车辆能否从 u 顺向行驶到 v，包含 u 等于 v 的情况）。我会回答"是"或"否"。

你需要通过收集信息来提交最终答案。若答案错误或格式不符，任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问使用以下 XML 格式：

- Reach 查询（例如询问路口 A 是否为路口 B 的上游）：
<query_reach>A,B</query_reach>

提交最终答案时，指定你认为的总调度中心所在路口，格式如下：

<answer>Root=A</answer>

注意：请尽可能少地进行查询，在确定答案后即可提交。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
We are conducting a "Trace the Central Dispatch Station" traffic flow investigation.

The current traffic network contains {n} intersection nodes, named: {node_names}. All roads are one-way and form a directed acyclic tree structure branching out from a hidden "Central Dispatch Station".

Your goal is to identify this "Central Dispatch Station" by querying upstream-downstream relationships. You can repeatedly ask me the following type of question:

- Reach Query: Ask whether intersection u is an upstream node of intersection v (i.e., whether a vehicle can travel downstream from u to v, including the case where u equals v). I will answer "Yes" or "No".

You need to submit your final answer after collecting enough information. If the answer is wrong or the format is invalid, the task fails.

## Query and Answer Format (must be strictly followed)

Each query uses the following XML format:

- Reach Query (e.g., asking if intersection A is upstream of intersection B):
<query_reach>A,B</query_reach>

When submitting the final answer, specify the intersection you believe is the Central Dispatch Station, using this format:

<answer>Root=A</answer>

Note: Please use as few queries as possible and submit once you are confident of the answer.
"""

    contextualized_rule_zh_2 = """\
我们在进行一项"定位零号病人"的流行病学溯源任务。

已确认一个包含 {n} 名患者的传播链条，患者编号为：{node_names}。病毒由一名未知的"零号病人"开始，呈树状单向传播给了其他所有人。

你的目标是通过询问传播关系推断出这位"零号病人"。你可以反复向我提出以下类型的问题：

- Reach 查询：询问患者 u 是否为患者 v 的直接或间接感染源（包括 u 等于 v 的情况）。我会回答"是"或"否"。

你需要通过收集信息来提交最终答案。若答案错误或格式不符，排查失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问使用以下 XML 格式：

- Reach 查询（例如询问患者 A 是否为患者 B 的感染源）：
<query_reach>A,B</query_reach>

提交最终答案时，指定你认为的零号病人编号，格式如下：

<answer>Root=A</answer>

注意：请尽可能少地进行查询，在确定答案后即可提交。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
We are conducting an epidemiological tracing task to "Locate Patient Zero".

A transmission chain involving {n} patients has been confirmed, with patient IDs: {node_names}. The virus spread in a one-way tree structure starting from an unknown "Patient Zero" to all others.

Your goal is to deduce "Patient Zero" by querying transmission relationships. You can repeatedly ask me the following type of question:

- Reach Query: Ask whether patient u is a direct or indirect infection source for patient v (including the case where u equals v). I will answer "Yes" or "No".

You need to submit your final answer after collecting enough information. If the answer is wrong or the format is invalid, the tracing fails.

## Query and Answer Format (must be strictly followed)

Each query uses the following XML format:

- Reach Query (e.g., asking if patient A is an infection source for patient B):
<query_reach>A,B</query_reach>

When submitting the final answer, specify the patient ID you believe is Patient Zero, using this format:

<answer>Root=A</answer>

Note: Please use as few queries as possible and submit once you are confident of the answer.
"""

    contextualized_rule_zh_3 = """\
我们在进行一项"挖掘基石课程"的教学体系分析任务。

某专业有 {n} 门必修课程，代号为：{node_names}。这些课程之间存在严格的先修依赖关系，形成了一棵从唯一的"基石课程"发散出来的依赖树。

你的目标是通过询问先决条件来找出这门"基石课程"。你可以反复向我提出以下类型的问题：

- Reach 查询：询问课程 u 是否为课程 v 的直接或间接先修课（包括 u 等于 v 的情况）。我会回答"是"或"否"。

你需要通过收集信息来提交最终答案。若答案错误或格式不符，分析失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问使用以下 XML 格式：

- Reach 查询（例如询问课程 A 是否为课程 B 的先修课）：
<query_reach>A,B</query_reach>

提交最终答案时，指定你认为的基石课程代号，格式如下：

<answer>Root=A</answer>

注意：请尽可能少地进行查询，在确定答案后即可提交。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
We are conducting a curriculum analysis task to "Uncover the Foundational Course".

A major has {n} required courses, coded as: {node_names}. There are strict prerequisite dependencies among these courses, forming a dependency tree branching out from a single "Foundational Course".

Your goal is to identify this "Foundational Course" by querying prerequisites. You can repeatedly ask me the following type of question:

- Reach Query: Ask whether course u is a direct or indirect prerequisite for course v (including the case where u equals v). I will answer "Yes" or "No".

You need to submit your final answer after collecting enough information. If the answer is wrong or the format is invalid, the analysis fails.

## Query and Answer Format (must be strictly followed)

Each query uses the following XML format:

- Reach Query (e.g., asking if course A is a prerequisite for course B):
<query_reach>A,B</query_reach>

When submitting the final answer, specify the course code you believe is the Foundational Course, using this format:

<answer>Root=A</answer>

Note: Please use as few queries as possible and submit once you are confident of the answer.
"""

    contextualized_rule_zh_4 = """\
我们在进行一项"排查主配料中心"的工业流水线审查任务。

当前生产线包含 {n} 个加工工位，编号为：{node_names}。物料从一个隐藏的"主配料中心"流出，经过逐级分发和加工，形成了无环的树状流水线拓扑结构。

你的目标是通过查询物料的流向推断出这个"主配料中心"。你可以反复向我提出以下类型的问题：

- Reach 查询：询问工位 u 是否处于工位 v 的上游（即物料是否从 u 流向 v，包括 u 等于 v 的情况）。我会回答"是"或"否"。

你需要通过收集信息来提交最终答案。若答案错误或格式不符，审查失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问使用以下 XML 格式：

- Reach 查询（例如询问工位 A 是否为工位 B 的上游）：
<query_reach>A,B</query_reach>

提交最终答案时，指定你认为的主配料中心所在工位，格式如下：

<answer>Root=A</answer>

注意：请尽可能少地进行查询，在确定答案后即可提交。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
We are conducting an industrial pipeline audit to "Trace the Primary Distribution Point".

The current production line contains {n} processing workstations, numbered: {node_names}. Materials flow from a hidden "Primary Distribution Point", being distributed and processed step-by-step to form an acyclic tree topology.

Your goal is to deduce this "Primary Distribution Point" by querying the material flow. You can repeatedly ask me the following type of question:

- Reach Query: Ask whether workstation u is upstream of workstation v (i.e., whether materials flow from u to v, including the case where u equals v). I will answer "Yes" or "No".

You need to submit your final answer after collecting enough information. If the answer is wrong or the format is invalid, the audit fails.

## Query and Answer Format (must be strictly followed)

Each query uses the following XML format:

- Reach Query (e.g., asking if workstation A is upstream of workstation B):
<query_reach>A,B</query_reach>

When submitting the final answer, specify the workstation you believe is the Primary Distribution Point, using this format:

<answer>Root=A</answer>

Note: Please use as few queries as possible and submit once you are confident of the answer.
"""

    contextualized_rule_zh_5 = """\
我们在进行一项"追踪主源头账户"的反洗钱资金流向调查任务。

监控网络捕获了 {n} 个涉案银行账户，账号为：{node_names}。黑钱从一个神秘的"主源头账户"汇出，经过层层转账，形成了树状的资金流向网络。

你的目标是通过查询资金流向来揪出这个"主源头账户"。你可以反复向我提出以下类型的问题：

- Reach 查询：询问账户 u 的资金是否直接或间接流入了账户 v（包括 u 等于 v 的情况）。我会回答"是"或"否"。

你需要通过收集信息来提交最终答案。若答案错误或格式不符，调查失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问使用以下 XML 格式：

- Reach 查询（例如询问账户 A 的资金是否流入账户 B）：
<query_reach>A,B</query_reach>

提交最终答案时，指定你认为的主源头账户，格式如下：

<answer>Root=A</answer>

注意：请尽可能少地进行查询，在确定答案后即可提交。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
We are conducting an anti-money laundering funds flow investigation to "Trace the Primary Offshore Account".

The monitoring network has captured {n} involved bank accounts, named: {node_names}. Illicit funds were transferred from a mysterious "Primary Offshore Account" and went through multiple layers of transfers, forming a tree-like network of funds flow.

Your goal is to expose this "Primary Offshore Account" by querying the funds flow. You can repeatedly ask me the following type of question:

- Reach Query: Ask whether funds from account u flowed directly or indirectly into account v (including the case where u equals v). I will answer "Yes" or "No".

You need to submit your final answer after collecting enough information. If the answer is wrong or the format is invalid, the investigation fails.

## Query and Answer Format (must be strictly followed)

Each query uses the following XML format:

- Reach Query (e.g., asking if funds from account A flowed into account B):
<query_reach>A,B</query_reach>

When submitting the final answer, specify the account you believe is the Primary Offshore Account, using this format:

<answer>Root=A</answer>

Note: Please use as few queries as possible and submit once you are confident of the answer.
"""

    tags = ["answer", "query_reach"]
    
    reasoning_type = "归纳推理"
    data_structure = "树"

    # 难度配置说明：
    # 1 (简单)        - N=4, 线性链式结构
    # 2 (中等偏下)    - N=5, 简单分叉
    # 3 (中等偏上)    - N=6, 多层分叉
    # 4 (较难)        - N=7, 复杂分叉
    # 5 (难)          - N=8, 高度复杂结构

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "nodes": ["A", "B", "C", "D"],
                "edges": [("A", "B"), ("B", "C"), ("C", "D")],  # A->B->C->D 链式
                "root": "A"
            },
            2: {
                "n": 5,
                "nodes": ["A", "B", "C", "D", "E"],
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E")],  # A为根，两层
                "root": "A"
            },
            3: {
                "n": 6,
                "nodes": ["A", "B", "C", "D", "E", "F"],
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F")],
                "root": "A"
            },
            4: {
                "n": 7,
                "nodes": ["A", "B", "C", "D", "E", "F", "G"],
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F"), ("C", "G")],
                "root": "A"
            },
            5: {
                "n": 8,
                "nodes": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F"), ("F", "G"), ("F", "H")],
                "root": "A"
            },
        },
        "en": {
            1: {
                "n": 4,
                "nodes": ["A", "B", "C", "D"],
                "edges": [("A", "B"), ("B", "C"), ("C", "D")],
                "root": "A"
            },
            2: {
                "n": 5,
                "nodes": ["A", "B", "C", "D", "E"],
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E")],
                "root": "A"
            },
            3: {
                "n": 6,
                "nodes": ["A", "B", "C", "D", "E", "F"],
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F")],
                "root": "A"
            },
            4: {
                "n": 7,
                "nodes": ["A", "B", "C", "D", "E", "F", "G"],
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F"), ("C", "G")],
                "root": "A"
            },
            5: {
                "n": 8,
                "nodes": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F"), ("F", "G"), ("F", "H")],
                "root": "A"
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        # 防御性类型转换：确保 difficulty 为整数
        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 使用确定性种子进行随机置换，确保同一配置下每次构建结果一致
        # 用 (语言, 难度) 作为种子，保证可复现
        rng = random.Random(hash((lang, diff, "HiddenTreeRootGame")))
        
        original_nodes = cfg["nodes"][:]
        shuffled_nodes = original_nodes[:]
        rng.shuffle(shuffled_nodes)
        
        # 建立原始名称到新名称的映射
        name_map = {orig: new for orig, new in zip(original_nodes, shuffled_nodes)}
        
        self._game_info["n"] = cfg["n"]
        self.nodes = shuffled_nodes
        self._game_info["node_names"] = ", ".join(self.nodes)
        # 边也需要映射
        self.edges = [(name_map[p], name_map[c]) for p, c in cfg["edges"]]
        self.root = name_map[cfg["root"]]
        
        # 构建后代关系表
        self.descendants_map = {node: {node} for node in self.nodes}
        self.parent_map = {}
        
        # 根据边构建父子关系
        for parent, child in self.edges:
            self.parent_map[child] = parent
        
        # 使用递归计算每个节点的所有后代
        def get_all_descendants(node):
            """递归获取节点的所有后代（包括自己）"""
            descendants = {node}
            for parent, child in self.edges:
                if parent == node:
                    descendants.update(get_all_descendants(child))
            return descendants
        
        for node in self.nodes:
            self.descendants_map[node] = get_all_descendants(node)
        
        # 查询计数器
        self.query_count = 0

    def _is_ancestor(self, u, v):
        """判断 u 是否为 v 的祖先（包括 u == v）"""
        # u 是 v 的祖先，当且仅当 v 在 u 的后代集合中
        return v in self.descendants_map.get(u, set())

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        # 解析答案格式: Root=X
        raw_ans = parsed_info["answer"].strip()
        
        # 尝试解析 Root=X 格式
        if "=" not in raw_ans:
            return False
        
        try:
            parts = raw_ans.split("=", 1)
            if len(parts) != 2:
                return False
            
            key, value = parts[0].strip(), parts[1].strip()
            if key.lower() != "root":
                return False
            
            submitted_root = value.strip()
            
            # 检查提交的根节点是否在节点列表中
            if submitted_root not in self.nodes:
                return False
            
            # 检查是否与真实根节点匹配
            return submitted_root == self.root
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始的业务逻辑处理"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：查询格式无效。请使用格式 <query_reach>u,v</query_reach>"
            error_node = "错误：节点名称无效。有效节点为：{}"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid query format. Please use format <query_reach>u,v</query_reach>"
            error_node = "Error: Invalid node name. Valid nodes are: {}"

        if "query_reach" in parsed_info:
            try:
                raw = parsed_info["query_reach"].strip()
                if not raw:
                    return error_format
                
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                
                u, v = parts[0], parts[1]
                
                # 检查节点是否有效
                if u not in self.nodes or v not in self.nodes:
                    return error_node.format(", ".join(self.nodes))
                
                # 增加查询计数
                self.query_count += 1
                
                # 判断 u 是否为 v 的祖先
                result = self._is_ancestor(u, v)
                return yes_res if result else no_res
                
            except Exception:
                return error_format
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """根据正确答案生成错误答案"""
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        if correct == "Yes":
            return "No"
        if correct == "No":
            return "Yes"
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 合法的 XML 标签字符串
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        results = []
        
        # 根据语言配置确定回答
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        # 枚举所有可能的节点对 (u, v)
        for u in self.nodes:
            for v in self.nodes:
                # 构造查询内容，包裹为合法 XML 标签
                query_str = f"<query_reach>{u},{v}</query_reach>"
                
                # 直接调用内部逻辑判断是否为祖先
                # 不调用 produce_response 以避免增加 query_count 或触发反事实逻辑
                is_anc = self._is_ancestor(u, v)
                answer = yes_res if is_anc else no_res
                
                results.append({
                    "query": query_str,
                    "answer": answer
                })
                
        return results