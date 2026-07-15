from .base import Game
import random

class TreeHeightQueryGame(Game):

    game_rule_zh = """\
我们现在来玩一个"树高度推理"游戏，规则如下：

游戏设定了一棵固定的有根树，包含 {n} 个互不相同的节点，节点编号为 {node_list}。每条边长度为 1。这棵树的结构对你不可见，但树的根和边的连接关系是固定的。

1. 叶子节点：没有子节点的节点。
2. 节点高度 H(u)：从节点 u 出发，向下到达其子树中某个叶子的最长路径的边数。例如，叶子节点的高度为 0。

你需要推断出目标节点集合 {target_nodes} 中每个节点的精确高度值 H(u)，并提交最终答案。你应该用尽可能少的查询次数完成推理。

你可以反复向我提出以下查询（每次仅限一个查询），我会根据真实的树结构如实回答：

{query_types_description}

每次查询只能包含一个标签。请使用以下 XML 格式：

- 阈值查询（例如询问节点 5 的高度是否大于等于 3）：
<query_threshold>5,3</query_threshold>

{additional_query_formats}

当你收集足够信息后，请提交最终答案。答案格式为节点编号和对应高度的配对，用分号分隔：

<answer>1=2;3=0;5=1</answer>

注意：答案中必须包含所有目标节点 {target_nodes} 的高度值。若答案错误或格式不符，游戏失败。
"""

    game_rule_en = """\
Let's play a "Tree Height Inference" game. Here are the rules:

There is a fixed rooted tree with {n} distinct nodes, numbered as {node_list}. Each edge has length 1. The tree structure is hidden from you, but the root and edge connections are fixed.

1. Leaf node: A node with no children.
2. Node height H(u): The maximum number of edges from node u downward to any leaf in its subtree. For example, a leaf node has height 0.

You need to infer the exact height value H(u) for each node in the target set {target_nodes} and submit your final answer. You should complete the inference using as few queries as possible.

You can repeatedly ask me the following queries (one query per turn), and I will answer truthfully based on the real tree structure:

{query_types_description}

Each query must contain only one tag. Use the following XML format:

- Threshold Query (e.g., asking if node 5's height is greater than or equal to 3):
<query_threshold>5,3</query_threshold>

{additional_query_formats}

When you have enough information, submit your final answer. The format is node ID paired with its height, separated by semicolons:

<answer>1=2;3=0;5=1</answer>

Note: The answer must include height values for all target nodes {target_nodes}. If the answer is wrong or the format is invalid, the game fails.
"""

    contextualized_rule_zh_1 = """\
我们现在来玩一个"路网层级推理"系统，规则如下：

[交通运输场景] 这是一个区域公路网的层级分析任务。网络由核心枢纽向外辐射，直到各个无路可走的末端小镇。
游戏设定了一棵固定的有根树（代表路网拓扑），包含 {n} 个互不相同的节点（代表路网交汇点），节点编号为 {node_list}。每条边长度为 1（代表一段公路）。这棵树的结构对你不可见，但路网的起点枢纽和连接关系是固定的。

1. 叶子节点（末端小镇）：没有下级公路连接的交汇点。
2. 节点高度 H(u)（最远可达深度）：从交汇点 u 出发，向下到达其覆盖范围中某个末端小镇的最长路径的公路段数。例如，末端小镇的高度为 0。

你需要推断出目标节点集合 {target_nodes} 中每个节点（交汇点）的精确高度值 H(u)，并提交最终答案。你应该用尽可能少的查询次数完成推理。

你可以反复向我提出以下查询（每次仅限一个查询），我会根据真实的路网结构如实回答：

{query_types_description}

每次查询只能包含一个标签。请使用以下 XML 格式：

- 阈值查询（例如询问节点 5 的高度是否大于等于 3）：
<query_threshold>5,3</query_threshold>

{additional_query_formats}

当你收集足够信息后，请提交最终答案。答案格式为节点编号和对应高度的配对，用分号分隔：

<answer>1=2;3=0;5=1</answer>

注意：答案中必须包含所有目标节点 {target_nodes} 的高度值。若答案错误或格式不符，系统验证失败。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's play a "Road Network Hierarchy Inference" game. Here are the rules:

This is a hierarchical analysis task for a regional road network. The network radiates from a central hub down to various dead-end towns.
There is a fixed rooted tree representing the road network topology with {n} distinct nodes (intersections), numbered as {node_list}. Each edge has length 1 (representing a road segment). The network structure is hidden from you, but the root hub and connections are fixed.

1. Leaf node (Dead-end town): An intersection with no further downward road connections.
2. Node height H(u) (Max route depth): The maximum number of road segments from intersection u downward to any dead-end town in its coverage. For example, a dead-end town has a height of 0.

You need to infer the exact height value H(u) for each node in the target set {target_nodes} and submit your final answer. You should complete the inference using as few queries as possible.

You can repeatedly ask me the following queries (one query per turn), and I will answer truthfully based on the real network structure:

{query_types_description}

Each query must contain only one tag. Use the following XML format:

- Threshold Query (e.g., asking if node 5's height is greater than or equal to 3):
<query_threshold>5,3</query_threshold>

{additional_query_formats}

When you have enough information, submit your final answer. The format is node ID paired with its height, separated by semicolons:

<answer>1=2;3=0;5=1</answer>

Note: The answer must include height values for all target nodes {target_nodes}. If the answer is wrong or the format is invalid, the system verification fails.
"""

    contextualized_rule_zh_2 = """\
我们现在来玩一个"传播链层级推理"系统，规则如下：

[医疗场景] 这是一个病毒传播链的溯源与分析任务。网络由零号病人/原始毒株开始，向下不断传播突变，直到不再引发感染的末端病例。
游戏设定了一棵固定的有根树（代表传播链条），包含 {n} 个互不相同的节点（代表病例/毒株），节点编号为 {node_list}。每条边长度为 1（代表一次传染代际）。这棵树的结构对你不可见，但传播源头和感染路径是固定的。

1. 叶子节点（末端病例）：没有造成进一步二次感染的病例。
2. 节点高度 H(u)（最远传播深度）：从病例 u 出发，向下追踪到达其传播分支中某个末端病例的最大代际数。例如，末端病例的高度为 0。

你需要推断出目标节点集合 {target_nodes} 中每个节点（病例）的精确高度值 H(u)，并提交最终答案。你应该用尽可能少的查询次数完成推理。

你可以反复向我提出以下查询（每次仅限一个查询），我会根据真实的传播链结构如实回答：

{query_types_description}

每次查询只能包含一个标签。请使用以下 XML 格式：

- 阈值查询（例如询问节点 5 的高度是否大于等于 3）：
<query_threshold>5,3</query_threshold>

{additional_query_formats}

当你收集足够信息后，请提交最终答案。答案格式为节点编号和对应高度的配对，用分号分隔：

<answer>1=2;3=0;5=1</answer>

注意：答案中必须包含所有目标节点 {target_nodes} 的高度值。若答案错误或格式不符，溯源任务失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Transmission Chain Hierarchy Inference" game. Here are the rules:

This is a traceability and analysis task for a viral transmission chain. The network starts from patient zero / original strain and spreads downwards until reaching terminal cases with no further infections.
There is a fixed rooted tree representing the transmission chain with {n} distinct nodes (cases/strains), numbered as {node_list}. Each edge has length 1 (representing one transmission generation). The chain structure is hidden from you, but the source and transmission paths are fixed.

1. Leaf node (Terminal case): A case that caused no further secondary infections.
2. Node height H(u) (Max transmission depth): The maximum number of generations from case u downward to any terminal case in its transmission branch. For example, a terminal case has a height of 0.

You need to infer the exact height value H(u) for each node in the target set {target_nodes} and submit your final answer. You should complete the inference using as few queries as possible.

You can repeatedly ask me the following queries (one query per turn), and I will answer truthfully based on the real transmission structure:

{query_types_description}

Each query must contain only one tag. Use the following XML format:

- Threshold Query (e.g., asking if node 5's height is greater than or equal to 3):
<query_threshold>5,3</query_threshold>

{additional_query_formats}

When you have enough information, submit your final answer. The format is node ID paired with its height, separated by semicolons:

<answer>1=2;3=0;5=1</answer>

Note: The answer must include height values for all target nodes {target_nodes}. If the answer is wrong or the format is invalid, the traceability task fails.
"""

    contextualized_rule_zh_3 = """\
我们现在来玩一个"知识图谱层级推理"系统，规则如下：

[教育场景] 这是一个学科知识依赖体系的解析任务。体系由基础核心概念发散，不断细分延伸，直到无需进一步前置学习的专业末端课题。
游戏设定了一棵固定的有根树（代表课程依赖图谱），包含 {n} 个互不相同的节点（代表知识点），节点编号为 {node_list}。每条边长度为 1（代表一阶前置依赖）。这棵树的结构对你不可见，但核心起点和依赖关系是固定的。

1. 叶子节点（末端课题）：没有衍生出更高级知识点的内容。
2. 节点高度 H(u)（最深延展深度）：从知识点 u 出发，向下延展到达其后续体系中某个末端课题的最长前置路径步数。例如，末端课题的高度为 0。

你需要推断出目标节点集合 {target_nodes} 中每个节点（知识点）的精确高度值 H(u)，并提交最终答案。你应该用尽可能少的查询次数完成推理。

你可以反复向我提出以下查询（每次仅限一个查询），我会根据真实的知识图谱结构如实回答：

{query_types_description}

每次查询只能包含一个标签。请使用以下 XML 格式：

- 阈值查询（例如询问节点 5 的高度是否大于等于 3）：
<query_threshold>5,3</query_threshold>

{additional_query_formats}

当你收集足够信息后，请提交最终答案。答案格式为节点编号和对应高度的配对，用分号分隔：

<answer>1=2;3=0;5=1</answer>

注意：答案中必须包含所有目标节点 {target_nodes} 的高度值。若答案错误或格式不符，解析任务失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Knowledge Graph Hierarchy Inference" game. Here are the rules:

This is an analysis task for a subject knowledge dependency structure. The structure stems from foundational concepts and branches out into highly specialized end-topics requiring no further prerequisites.
There is a fixed rooted tree representing the curriculum dependency graph with {n} distinct nodes (knowledge points), numbered as {node_list}. Each edge has length 1 (representing a single-step prerequisite). The graph structure is hidden from you, but the foundation and dependencies are fixed.

1. Leaf node (End-topic): A knowledge point that does not act as a prerequisite for any advanced topics.
2. Node height H(u) (Max study depth): The maximum number of prerequisite steps from knowledge point u downward to any end-topic in its derivative branches. For example, an end-topic has a height of 0.

You need to infer the exact height value H(u) for each node in the target set {target_nodes} and submit your final answer. You should complete the inference using as few queries as possible.

You can repeatedly ask me the following queries (one query per turn), and I will answer truthfully based on the real curriculum structure:

{query_types_description}

Each query must contain only one tag. Use the following XML format:

- Threshold Query (e.g., asking if node 5's height is greater than or equal to 3):
<query_threshold>5,3</query_threshold>

{additional_query_formats}

When you have enough information, submit your final answer. The format is node ID paired with its height, separated by semicolons:

<answer>1=2;3=0;5=1</answer>

Note: The answer must include height values for all target nodes {target_nodes}. If the answer is wrong or the format is invalid, the analysis task fails.
"""

    contextualized_rule_zh_4 = """\
我们现在来玩一个"BOM(物料清单)层级推理"系统，规则如下：

[制造业/工业场景] 这是一个复杂产品的组件拆解分析任务。结构由最终主干产品向下按层级拆解，直到不可分割的基础原材料。
游戏设定了一棵固定的有根树（代表产品BOM结构），包含 {n} 个互不相同的节点（代表组件/物料），节点编号为 {node_list}。每条边长度为 1（代表一层装配关系）。这棵树的结构对你不可见，但总成件与子件的构成关系是固定的。

1. 叶子节点（基础原材料）：不可再向下拆分出子组件的底层物料。
2. 节点高度 H(u)（最大拆解深度）：从组件 u 出发，向下按层级拆解到达其分支中某个基础原材料所需的最大装配层次数。例如，基础原材料的高度为 0。

你需要推断出目标节点集合 {target_nodes} 中每个节点（组件）的精确高度值 H(u)，并提交最终答案。你应该用尽可能少的查询次数完成推理。

你可以反复向我提出以下查询（每次仅限一个查询），我会根据真实的BOM层级如实回答：

{query_types_description}

每次查询只能包含一个标签。请使用以下 XML 格式：

- 阈值查询（例如询问节点 5 的高度是否大于等于 3）：
<query_threshold>5,3</query_threshold>

{additional_query_formats}

当你收集足够信息后，请提交最终答案。答案格式为节点编号和对应高度的配对，用分号分隔：

<answer>1=2;3=0;5=1</answer>

注意：答案中必须包含所有目标节点 {target_nodes} 的高度值。若答案错误或格式不符，拆解分析失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's play a "BOM (Bill of Materials) Hierarchy Inference" game. Here are the rules:

This is a component breakdown analysis task for a complex product. The structure breaks down hierarchically from the final main assembly down to indivisible base raw materials.
There is a fixed rooted tree representing the BOM structure with {n} distinct nodes (components/materials), numbered as {node_list}. Each edge has length 1 (representing one level of assembly). The structure is hidden from you, but the main assembly and component relationships are fixed.

1. Leaf node (Base raw material): A low-level material that cannot be broken down into further sub-components.
2. Node height H(u) (Max breakdown depth): The maximum number of assembly levels required to break down component u into any base raw material in its sub-assemblies. For example, a base raw material has a height of 0.

You need to infer the exact height value H(u) for each node in the target set {target_nodes} and submit your final answer. You should complete the inference using as few queries as possible.

You can repeatedly ask me the following queries (one query per turn), and I will answer truthfully based on the real BOM hierarchy:

{query_types_description}

Each query must contain only one tag. Use the following XML format:

- Threshold Query (e.g., asking if node 5's height is greater than or equal to 3):
<query_threshold>5,3</query_threshold>

{additional_query_formats}

When you have enough information, submit your final answer. The format is node ID paired with its height, separated by semicolons:

<answer>1=2;3=0;5=1</answer>

Note: The answer must include height values for all target nodes {target_nodes}. If the answer is wrong or the format is invalid, the breakdown analysis fails.
"""

    contextualized_rule_zh_5 = """\
我们现在来玩一个"股权穿透层级推理"系统，规则如下：

[法律场景] 这是一个企业股权结构的穿透调查任务。架构由顶层控股母公司向下延伸，通过层层全资控股，直到无对外投资的底层壳公司。
游戏设定了一棵固定的有根树（代表股权架构），包含 {n} 个互不相同的节点（代表公司实体），节点编号为 {node_list}。每条边长度为 1（代表一层控股关系）。这棵树的结构对你不可见，但母公司和下属投资关系是固定的。

1. 叶子节点（底层壳公司）：没有任何对外下级投资的实体。
2. 节点高度 H(u)（最大穿透深度）：从公司 u 出发，向下层层穿透到达其控制链中某个底层壳公司的最大控股层次数。例如，底层壳公司的高度为 0。

你需要推断出目标节点集合 {target_nodes} 中每个节点（公司实体）的精确高度值 H(u)，并提交最终答案。你应该用尽可能少的查询次数完成推理。

你可以反复向我提出以下查询（每次仅限一个查询），我会根据真实的股权架构如实回答：

{query_types_description}

每次查询只能包含一个标签。请使用以下 XML 格式：

- 阈值查询（例如询问节点 5 的高度是否大于等于 3）：
<query_threshold>5,3</query_threshold>

{additional_query_formats}

当你收集足够信息后，请提交最终答案。答案格式为节点编号和对应高度的配对，用分号分隔：

<answer>1=2;3=0;5=1</answer>

注意：答案中必须包含所有目标节点 {target_nodes} 的高度值。若答案错误或格式不符，穿透调查失败。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's play an "Equity Penetration Hierarchy Inference" game. Here are the rules:

This is a penetration investigation task into corporate equity structures. The architecture extends downward from the top holding parent company through layers of wholly-owned subsidiaries, until reaching ultimate shell companies with no outbound investments.
There is a fixed rooted tree representing the equity architecture with {n} distinct nodes (corporate entities), numbered as {node_list}. Each edge has length 1 (representing one layer of holding relationship). The architecture is hidden from you, but the parent company and investment relationships are fixed.

1. Leaf node (Ultimate shell company): An entity that has no outbound lower-level investments.
2. Node height H(u) (Max penetration depth): The maximum number of holding layers from entity u downward to penetrate to any ultimate shell company in its control chain. For example, an ultimate shell company has a height of 0.

You need to infer the exact height value H(u) for each node in the target set {target_nodes} and submit your final answer. You should complete the inference using as few queries as possible.

You can repeatedly ask me the following queries (one query per turn), and I will answer truthfully based on the real equity architecture:

{query_types_description}

Each query must contain only one tag. Use the following XML format:

- Threshold Query (e.g., asking if node 5's height is greater than or equal to 3):
<query_threshold>5,3</query_threshold>

{additional_query_formats}

When you have enough information, submit your final answer. The format is node ID paired with its height, separated by semicolons:

<answer>1=2;3=0;5=1</answer>

Note: The answer must include height values for all target nodes {target_nodes}. If the answer is wrong or the format is invalid, the penetration investigation fails.
"""

    tags = ["answer", "query_threshold", "query_compare", "query_count"]
    
    reasoning_type = "演绎推理"
    data_structure = "树"

    _BASE_CONFIG = {
        1: {
            "n": 5,
            "tree_edges": "1-2,1-3,2-4,2-5",
            "root": 1,
            "target_nodes": [2],
            "enable_compare": False,
            "enable_count": False,
        },
        2: {
            "n": 7,
            "tree_edges": "1-2,1-3,2-4,3-5,3-6,5-7",
            "root": 1,
            "target_nodes": [1, 3],
            "enable_compare": False,
            "enable_count": False,
        },
        3: {
            "n": 8,
            "tree_edges": "1-2,1-3,2-4,2-5,3-6,5-7,5-8",
            "root": 1,
            "target_nodes": [1, 2, 5],
            "enable_compare": True,
            "enable_count": False,
        },
        4: {
            "n": 10,
            "tree_edges": "1-2,1-3,2-4,2-5,3-6,3-7,5-8,6-9,6-10",
            "root": 1,
            "target_nodes": [1, 2, 3, 6],
            "enable_compare": True,
            "enable_count": False,
        },
        5: {
            "n": 12,
            "tree_edges": "1-2,1-3,2-4,2-5,3-6,3-7,5-8,5-9,6-10,7-11,7-12",
            "root": 1,
            "target_nodes": [1, 2, 3, 5, 7],
            "enable_compare": True,
            "enable_count": True,
        },
    }

    DIFFICULTY_CONFIG = {
        "zh": _BASE_CONFIG,
        "en": _BASE_CONFIG,
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
        n = cfg["n"]
        self._game_info["n"] = n
        self._game_info["node_list"] = ", ".join(str(i) for i in range(1, n + 1))
        self._game_info["target_nodes"] = ", ".join(str(t) for t in cfg["target_nodes"])
        
        self.target_nodes = cfg["target_nodes"]
        self.enable_compare = cfg["enable_compare"]
        self.enable_count = cfg["enable_count"]
        self.root = cfg["root"]
        
        self.children = {i: [] for i in range(1, n + 1)}
        for edge in cfg["tree_edges"].split(","):
            parent, child = map(int, edge.split("-"))
            self.children[parent].append(child)
        
        self.node_heights = {}
        self._compute_heights(self.root)
        
        self._prepare_query_descriptions()

    def _compute_heights(self, node):
        if not self.children[node]:
            self.node_heights[node] = 0
            return 0
        
        max_height = 0
        for child in self.children[node]:
            child_height = self._compute_heights(child)
            max_height = max(max_height, child_height + 1)
        
        self.node_heights[node] = max_height
        return max_height

    def _prepare_query_descriptions(self):
        if self.config.language == "zh":
            threshold_desc = "1. 阈值查询：询问节点 u 的高度是否大于等于 d。格式：Threshold(u, d)。回答是或否。"
            compare_desc = "2. 比较查询：询问节点 u 和节点 v 的高度大小关系。格式：Compare(u, v)。回答u大于v、u等于v或u小于v。"
            count_desc = "3. 计数查询：询问从节点 u 向下恰好距离 d 处的叶子个数。格式：Count(u, d)。回答一个非负整数。"
            
            compare_format = """- 比较查询（例如比较节点 5 和节点 3）：
<query_compare>5,3</query_compare>
"""
            count_format = """- 计数查询（例如询问节点 5 向下距离 2 处的叶子个数）：
<query_count>5,2</query_count>
"""
        else:
            threshold_desc = "1. Threshold Query: Ask if node u's height is greater than or equal to d. Format: Threshold(u, d). Answer \"Yes\" or \"No\"."
            compare_desc = "2. Comparison Query: Ask about the height relationship between node u and node v. Format: Compare(u, v). Answer \"u>v\", \"u=v\", or \"u<v\"."
            count_desc = "3. Count Query: Ask for the number of leaves at exactly distance d downward from node u. Format: Count(u, d). Answer a non-negative integer."
            
            compare_format = """- Comparison Query (e.g., comparing node 5 and node 3):
<query_compare>5,3</query_compare>
"""
            count_format = """- Count Query (e.g., asking for the number of leaves at distance 2 from node 5):
<query_count>5,2</query_count>
"""
        
        descriptions = [threshold_desc]
        formats = []
        
        if self.enable_compare:
            descriptions.append(compare_desc)
            formats.append(compare_format)
        
        if self.enable_count:
            descriptions.append(count_desc)
            formats.append(count_format)
        
        self._game_info["query_types_description"] = "\n".join(descriptions)
        self._game_info["additional_query_formats"] = "\n".join(formats) if formats else ""

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        try:
            pairs = [x.strip() for x in raw_ans.split(";") if "=" in x]
            ans_dict = {}
            for pair in pairs:
                node, height = pair.split("=")
                ans_dict[int(node.strip())] = int(height.strip())
        except:
            return False
        
        if set(ans_dict.keys()) != set(self.target_nodes):
            return False
        
        for node in self.target_nodes:
            if ans_dict[node] != self.node_heights[node]:
                return False
        
        return True

    def _cf_make_wrong(self, correct):
        lang = self.config.language
        if lang == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
        
        if correct == yes_res:
            return no_res
        elif correct == no_res:
            return yes_res
        
        if lang == "zh":
            if "大于" in correct:
                return correct.replace("大于", "小于")
            elif "小于" in correct:
                return correct.replace("小于", "大于")
            elif "等于" in correct:
                return correct.replace("等于", "大于")
        else:
            if ">" in correct and "=" not in correct:
                return correct.replace(">", "<")
            elif "<" in correct:
                return correct.replace("<", ">")
            elif "=" in correct:
                return correct.replace("=", ">")
        
        try:
            val = int(correct)
            return str(val + 1)
        except ValueError:
            pass
        
        return correct + " [wrong]"

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_node = "错误：节点编号无效。"
            error_format = "错误：查询格式无效。"
            error_disabled = "错误：该查询类型在当前难度下不可用。"
        else:
            yes_res, no_res = "Yes", "No"
            error_node = "Error: Invalid node ID."
            error_format = "Error: Invalid query format."
            error_disabled = "Error: This query type is not available at current difficulty."
        
        if "query_threshold" in parsed_info:
            try:
                raw = parsed_info["query_threshold"]
                node, threshold = [x.strip() for x in raw.split(",")]
                node, threshold = int(node), int(threshold)
                
                if node < 1 or node > self._game_info["n"]:
                    return error_node
                
                return yes_res if self.node_heights[node] >= threshold else no_res
            except:
                return error_format
        
        elif "query_compare" in parsed_info:
            if not self.enable_compare:
                return error_disabled
            
            try:
                raw = parsed_info["query_compare"]
                node1, node2 = [x.strip() for x in raw.split(",")]
                node1, node2 = int(node1), int(node2)
                
                if node1 < 1 or node1 > self._game_info["n"] or node2 < 1 or node2 > self._game_info["n"]:
                    return error_node
                
                h1, h2 = self.node_heights[node1], self.node_heights[node2]
                
                if self.config.language == "zh":
                    if h1 > h2:
                        return f"H({node1})大于H({node2})"
                    elif h1 == h2:
                        return f"H({node1})等于H({node2})"
                    else:
                        return f"H({node1})小于H({node2})"
                else:
                    if h1 > h2:
                        return f"H({node1})>H({node2})"
                    elif h1 == h2:
                        return f"H({node1})=H({node2})"
                    else:
                        return f"H({node1})<H({node2})"
            except:
                return error_format
        
        elif "query_count" in parsed_info:
            if not self.enable_count:
                return error_disabled
            
            try:
                raw = parsed_info["query_count"]
                node, distance = [x.strip() for x in raw.split(",")]
                node, distance = int(node), int(distance)
                
                if node < 1 or node > self._game_info["n"]:
                    return error_node
                
                count = self._count_leaves_at_distance(node, distance)
                return str(count)
            except:
                return error_format
        
        else:
            raise ValueError("No valid query tag found.")

    def _count_leaves_at_distance(self, node, distance):
        if distance == 0:
            return 1 if not self.children[node] else 0
        
        count = 0
        for child in self.children[node]:
            count += self._count_leaves_at_distance(child, distance - 1)
        
        return count

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        n = self._game_info["n"]
        lang = self.config.language
        
        if lang == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        for u in range(1, n + 1):
            for d in range(0, n + 1):
                query_content = f"{u},{d}"
                query_xml = f"<query_threshold>{query_content}</query_threshold>"
                ans = yes_res if self.node_heights[u] >= d else no_res
                queries.append({"query": query_xml, "answer": ans})

        if self.enable_compare:
            for u in range(1, n + 1):
                for v in range(1, n + 1):
                    query_content = f"{u},{v}"
                    query_xml = f"<query_compare>{query_content}</query_compare>"
                    h1 = self.node_heights[u]
                    h2 = self.node_heights[v]
                    if lang == "zh":
                        if h1 > h2:
                            ans = f"H({u})大于H({v})"
                        elif h1 == h2:
                            ans = f"H({u})等于H({v})"
                        else:
                            ans = f"H({u})小于H({v})"
                    else:
                        if h1 > h2:
                            ans = f"H({u})>H({v})"
                        elif h1 == h2:
                            ans = f"H({u})=H({v})"
                        else:
                            ans = f"H({u})<H({v})"
                    queries.append({"query": query_xml, "answer": ans})

        if self.enable_count:
            for u in range(1, n + 1):
                for d in range(0, n + 1):
                    query_content = f"{u},{d}"
                    query_xml = f"<query_count>{query_content}</query_count>"
                    count = self._count_leaves_at_distance(u, d)
                    ans = str(count)
                    queries.append({"query": query_xml, "answer": ans})
                    
        return queries