from .base import Game
import math

class TreeAncestorGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"树上祖先推理"游戏，规则如下：

游戏设定了一棵有根树，共有 {n} 个节点，每个节点有唯一的编号。树的结构如下：

{tree_structure}

在这棵树中，我已经秘密选择了一个目标节点 T。祖先关系定义为：任一节点被视为其自身的祖先；根节点是所有节点的祖先。

你的目标是通过尽可能少的询问次数找到这个目标节点。你可以进行以下两类操作：

1. 祖先查询：询问某个节点 X 是否为目标节点 T 的祖先（包含自身）。我会回答"是"或"否"。
2. 提交答案：当你确定目标节点后，提交你的答案。

注意：
- 你必须进行至少 2 次祖先查询后才能提交答案。
- 如果答案错误或格式不符，游戏失败。
- 请尽可能少地使用查询次数。

祖先查询（例如询问节点 5）：
<query_ancestor>5</query_ancestor>

提交最终答案（例如目标节点为 3）：
<answer>3</answer>
"""

    game_rule_en = """\
Let's play a "Tree Ancestor Inference" game. Here are the rules:

The game is set on a rooted tree with {n} nodes, each having a unique ID. The tree structure is as follows:

{tree_structure}

In this tree, I have secretly selected a target node T. The ancestor relation is defined as: any node is considered an ancestor of itself; the root node is an ancestor of all nodes.

Your goal is to find the target node using as few queries as possible. You can perform the following two types of operations:

1. Ancestor Query: Ask whether a node X is an ancestor of the target node T (including itself). I will answer "Yes" or "No".
2. Submit Answer: When you have determined the target node, submit your answer.

Note:
- You must perform at least 2 ancestor queries before submitting an answer.
- If the answer is incorrect or the format is invalid, the game fails.
- Try to use as few queries as possible.

Ancestor Query (e.g., asking about node 5):
<query_ancestor>5</query_ancestor>

Submit final answer (e.g., target node is 3):
<answer>3</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎进入交通网层级溯源系统。我们构建了一个包含 {n} 个区域节点的交通管理路网，规则如下：

路网的层级结构如下：

{tree_structure}

在这片路网中，我已经秘密锁定了一个发生拥堵的"目标源头 T"。祖先关系在此定义为：任一区域节点被视为其自身的上级覆盖区域；总线/根节点是所有区域的上级。

你的目标是通过尽可能少的询问次数找到这个拥堵源头节点。你可以进行以下两类操作：

1. 祖先查询：询问某个节点 X 是否为目标源头 T 的上级覆盖区域（包含自身）。我会回答"是"或"否"。
2. 提交答案：当你确定目标源头节点后，提交你的答案。

注意：
- 你必须进行至少 2 次祖先查询后才能提交诊断结果。
- 如果答案错误或格式不符，排查任务失败。
- 请尽可能少地使用查询次数。

祖先查询（例如询问区域 5）：
<query_ancestor>5</query_ancestor>

提交最终答案（例如拥堵源头为 3）：
<answer>3</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Traffic Network Hierarchical Tracing System. We have built a traffic management network with {n} zone nodes. The rules are as follows:

The hierarchical structure of the network is:

{tree_structure}

In this network, I have secretly pinpointed a gridlock "target source T". The ancestor relation is defined here as: any zone node is considered its own covering area; the root node covers all zones.

Your goal is to find this target source node using as few queries as possible. You can perform the following two types of operations:

1. Ancestor Query: Ask whether a node X is a covering ancestor area of the target source T (including itself). I will answer "Yes" or "No".
2. Submit Answer: When you have determined the target source node, submit your answer.

Note:
- You must perform at least 2 ancestor queries before submitting an answer.
- If the answer is incorrect or the format is invalid, the tracing task fails.
- Try to use as few queries as possible.

Ancestor Query (e.g., asking about zone 5):
<query_ancestor>5</query_ancestor>

Submit final answer (e.g., target source is 3):
<answer>3</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用流行病学毒株溯源分析系统。系统加载了一棵包含 {n} 个毒株节点的病毒演化树，规则如下：

演化树的层级结构如下：

{tree_structure}

在这棵树中，我已隔离了一个未知的"目标毒株 T"。演化祖先关系定义为：任一毒株节点被视为其自身的演化祖先；初代零号毒株（根节点）是所有毒株的祖先。

你的目标是通过尽可能少的检测询问次数找到这个目标毒株。你可以进行以下两类操作：

1. 祖先查询：询问某个毒株节点 X 是否为目标毒株 T 的演化祖先（包含自身）。系统会返回"是"或"否"。
2. 提交答案：当你确定目标毒株节点后，提交你的答案。

注意：
- 你必须进行至少 2 次演化祖先查询后才能提交诊断报告。
- 如果答案错误或格式不符，溯源失败。
- 请尽可能少地使用查询次数。

祖先查询（例如询问毒株 5）：
<query_ancestor>5</query_ancestor>

提交最终答案（例如目标毒株为 3）：
<answer>3</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Epidemiological Strain Tracing System. The system has loaded a virus evolution tree containing {n} strain nodes. The rules are as follows:

The structure of the evolution tree is:

{tree_structure}

In this tree, I have isolated an unknown "target strain T". The evolutionary ancestor relation is defined as: any strain node is considered an evolutionary ancestor of itself; the patient-zero strain (root node) is the ancestor of all strains.

Your goal is to identify this target strain using as few test queries as possible. You can perform the following two types of operations:

1. Ancestor Query: Ask whether a strain node X is an evolutionary ancestor of the target strain T (including itself). I will answer "Yes" or "No".
2. Submit Answer: When you have determined the target strain node, submit your answer.

Note:
- You must perform at least 2 ancestor queries before submitting an answer.
- If the answer is incorrect or the format is invalid, the tracing fails.
- Try to use as few queries as possible.

Ancestor Query (e.g., asking about strain 5):
<query_ancestor>5</query_ancestor>

Submit final answer (e.g., target strain is 3):
<answer>3</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎进入自适应学习知识溯源模块。系统构建了一个包含 {n} 个知识点的学科层级树，规则如下：

知识点的前置依赖结构如下：

{tree_structure}

在这个图谱中，我已为学生定位了一个需要强化的"目标知识点 T"。前置基础关系定义为：任一知识点被视为其自身的前置基础；学科根基节点是所有知识点的前置基础。

你的目标是通过尽可能少的测试询问次数找到这个目标知识点。你可以进行以下两类操作：

1. 祖先查询：询问某个知识点 X 是否为目标知识点 T 的前置基础节点（包含自身）。系统会回答"是"或"否"。
2. 提交答案：当你确定目标知识点后，提交你的诊断答案。

注意：
- 你必须进行至少 2 次前置基础查询后才能提交答案。
- 如果答案错误或格式不符，诊断评估失败。
- 请尽可能少地使用查询次数。

祖先查询（例如询问知识点 5）：
<query_ancestor>5</query_ancestor>

提交最终答案（例如目标知识点为 3）：
<answer>3</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Adaptive Learning Knowledge Tracing Module. The system has constructed a subject hierarchy tree with {n} knowledge nodes. The rules are as follows:

The prerequisite dependency structure is:

{tree_structure}

In this graph, I have pinpointed a "target concept T" that the student needs to reinforce. The prerequisite relation is defined as: any knowledge node is considered a prerequisite of itself; the foundational root node is the prerequisite for all nodes.

Your goal is to locate this target concept using as few diagnostic queries as possible. You can perform the following two types of operations:

1. Ancestor Query: Ask whether a knowledge node X is a prerequisite node for the target concept T (including itself). The system will answer "Yes" or "No".
2. Submit Answer: When you have determined the target concept, submit your diagnostic answer.

Note:
- You must perform at least 2 prerequisite queries before submitting an answer.
- If the answer is incorrect or the format is invalid, the diagnostic assessment fails.
- Try to use as few queries as possible.

Ancestor Query (e.g., asking about concept 5):
<query_ancestor>5</query_ancestor>

Submit final answer (e.g., target concept is 3):
<answer>3</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎启动工业装配线故障排查系统。设备由 {n} 个部件节点组成，呈树状装配结构，规则如下：

设备的BOM（物料清单）装配层级如下：

{tree_structure}

系统检测到异常，我已锁定了一个"目标故障部件 T"。装配包含关系定义为：任一部件被视为其自身的上级总成；主干设备（根节点）是所有部件的上级总成。

你的目标是通过尽可能少的探伤询问次数找到这个故障部件。你可以进行以下两类操作：

1. 祖先查询：询问某个部件 X 是否为目标故障部件 T 的所在上级总成模块（包含自身）。诊断器会回答"是"或"否"。
2. 提交答案：当你确定目标故障部件后，提交你的维修答案。

注意：
- 你必须进行至少 2 次总成查询后才能生成维修单。
- 如果答案错误或格式不符，故障排查失败。
- 请尽可能少地使用查询次数。

祖先查询（例如询问部件 5）：
<query_ancestor>5</query_ancestor>

提交最终答案（例如故障部件为 3）：
<answer>3</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Industrial Assembly Line Fault Troubleshooting System. The equipment consists of {n} component nodes arranged in a tree-like assembly structure. The rules are as follows:

The BOM (Bill of Materials) assembly hierarchy of the equipment is:

{tree_structure}

The system has detected an anomaly, and I have isolated a "target faulty component T". The assembly inclusion relation is defined as: any component is considered its own parent assembly; the main equipment (root node) is the parent assembly for all components.

Your goal is to find this faulty component using as few diagnostic queries as possible. You can perform the following two types of operations:

1. Ancestor Query: Ask whether a component X is a parent assembly module of the target faulty component T (including itself). The diagnostics will answer "Yes" or "No".
2. Submit Answer: When you have identified the target faulty component, submit your maintenance answer.

Note:
- You must perform at least 2 assembly queries before submitting an answer.
- If the answer is incorrect or the format is invalid, the troubleshooting fails.
- Try to use as few queries as possible.

Ancestor Query (e.g., asking about component 5):
<query_ancestor>5</query_ancestor>

Submit final answer (e.g., faulty component is 3):
<answer>3</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用法律条文精准检索系统。我们整理了一部包含 {n} 个层级节点的法典目录树，规则如下：

法典的编、章、节、条的层级结构如下：

{tree_structure}

针对当前案件，我已秘密确定了一个最佳的"目标适用条款 T"。目录包含关系定义为：任一目录节点被视为其自身的上级；整部法典（根节点）是所有条款的上级。

你的目标是通过尽可能少的检索询问次数找到这个目标适用条款。你可以进行以下两类操作：

1. 祖先查询：询问某个目录节点 X 是否包含该目标适用条款 T（即 X 为 T 的上级层级或其自身）。系统会回答"是"或"否"。
2. 提交答案：当你确定目标适用条款后，提交你的结论。

注意：
- 你必须进行至少 2 次层级查询后才能提交最终结论。
- 如果答案错误或格式不符，案件检索失败。
- 请尽可能少地使用查询次数。

祖先查询（例如询问目录 5）：
<query_ancestor>5</query_ancestor>

提交最终答案（例如适用条款为 3）：
<answer>3</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the Legal Provision Precision Retrieval System. We have compiled a legal code directory tree containing {n} hierarchical nodes. The rules are as follows:

The hierarchical structure of the legal code's books, parts, chapters, and articles is:

{tree_structure}

For the current case, I have secretly determined the most appropriate "target applicable provision T". The directory inclusion relation is defined as: any directory node is considered its own superior level; the entire code (root node) is the superior level for all provisions.

Your goal is to pinpoint this target applicable provision using as few retrieval queries as possible. You can perform the following two types of operations:

1. Ancestor Query: Ask whether a directory node X includes the target applicable provision T (i.e., X is a superior level of T or T itself). The system will answer "Yes" or "No".
2. Submit Answer: When you have pinpointed the target applicable provision, submit your conclusion.

Note:
- You must perform at least 2 hierarchical queries before submitting an answer.
- If the answer is incorrect or the format is invalid, the case retrieval fails.
- Try to use as few queries as possible.

Ancestor Query (e.g., asking about directory 5):
<query_ancestor>5</query_ancestor>

Submit final answer (e.g., applicable provision is 3):
<answer>3</answer>
"""

    tags = ["answer", "query_ancestor"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 7,
                "tree": {
                    "1": [],
                    "2": ["1"],
                    "3": ["1"],
                    "4": ["2"],
                    "5": ["2"],
                    "6": ["3"],
                    "7": ["3"],
                },
                "target": "5",
            },
            2: {
                "n": 15,
                "tree": {
                    "1": [],
                    "2": ["1"], "3": ["1"],
                    "4": ["2"], "5": ["2"], "6": ["3"], "7": ["3"],
                    "8": ["4"], "9": ["4"], "10": ["5"], "11": ["5"],
                    "12": ["6"], "13": ["6"], "14": ["7"], "15": ["7"],
                },
                "target": "11",
            },
            3: {
                "n": 31,
                "tree": {
                    "1": [],
                    "2": ["1"], "3": ["1"],
                    "4": ["2"], "5": ["2"], "6": ["3"], "7": ["3"],
                    "8": ["4"], "9": ["4"], "10": ["5"], "11": ["5"],
                    "12": ["6"], "13": ["6"], "14": ["7"], "15": ["7"],
                    "16": ["8"], "17": ["8"], "18": ["9"], "19": ["9"],
                    "20": ["10"], "21": ["10"], "22": ["11"], "23": ["11"],
                    "24": ["12"], "25": ["12"], "26": ["13"], "27": ["13"],
                    "28": ["14"], "29": ["14"], "30": ["15"], "31": ["15"],
                },
                "target": "23",
            },
            4: {
                "n": 50,
                "tree": {
                    "1": [],
                    "2": ["1"], "3": ["1"], "4": ["1"],
                    "5": ["2"], "6": ["2"], "7": ["3"],
                    "8": ["4"], "9": ["4"], "10": ["4"], "11": ["5"],
                    "12": ["5"], "13": ["6"], "14": ["7"], "15": ["7"],
                    "16": ["8"], "17": ["9"], "18": ["9"], "19": ["10"],
                    "20": ["11"], "21": ["11"], "22": ["12"], "23": ["13"],
                    "24": ["13"], "25": ["14"], "26": ["15"], "27": ["15"],
                    "28": ["16"], "29": ["17"], "30": ["18"], "31": ["18"],
                    "32": ["19"], "33": ["19"], "34": ["20"], "35": ["21"],
                    "36": ["22"], "37": ["23"], "38": ["24"], "39": ["25"],
                    "40": ["26"], "41": ["27"], "42": ["28"], "43": ["29"],
                    "44": ["30"], "45": ["31"], "46": ["32"], "47": ["33"],
                    "48": ["34"], "49": ["35"], "50": ["36"],
                },
                "target": "47",
            },
            5: {
                "n": 100,
                "tree": {
                    "1": [],
                    "2": ["1"], "3": ["1"], "4": ["1"], "5": ["1"],
                    "6": ["2"], "7": ["2"], "8": ["3"], "9": ["3"],
                    "10": ["4"], "11": ["4"], "12": ["5"], "13": ["5"],
                    "14": ["6"], "15": ["6"], "16": ["7"], "17": ["8"],
                    "18": ["8"], "19": ["9"], "20": ["10"], "21": ["10"],
                    "22": ["11"], "23": ["12"], "24": ["12"], "25": ["13"],
                    "26": ["14"], "27": ["14"], "28": ["15"], "29": ["16"],
                    "30": ["17"], "31": ["17"], "32": ["18"], "33": ["19"],
                    "34": ["19"], "35": ["20"], "36": ["21"], "37": ["21"],
                    "38": ["22"], "39": ["23"], "40": ["24"], "41": ["25"],
                    "42": ["25"], "43": ["26"], "44": ["27"], "45": ["28"],
                    "46": ["29"], "47": ["30"], "48": ["31"], "49": ["32"],
                    "50": ["33"], "51": ["34"], "52": ["35"], "53": ["36"],
                    "54": ["37"], "55": ["38"], "56": ["39"], "57": ["40"],
                    "58": ["41"], "59": ["42"], "60": ["43"], "61": ["44"],
                    "62": ["45"], "63": ["46"], "64": ["47"], "65": ["48"],
                    "66": ["49"], "67": ["50"], "68": ["51"], "69": ["52"],
                    "70": ["53"], "71": ["54"], "72": ["55"], "73": ["56"],
                    "74": ["57"], "75": ["58"], "76": ["59"], "77": ["60"],
                    "78": ["61"], "79": ["62"], "80": ["63"], "81": ["64"],
                    "82": ["65"], "83": ["66"], "84": ["67"], "85": ["68"],
                    "86": ["69"], "87": ["70"], "88": ["71"], "89": ["72"],
                    "90": ["73"], "91": ["74"], "92": ["75"], "93": ["76"],
                    "94": ["77"], "95": ["78"], "96": ["79"], "97": ["80"],
                    "98": ["81"], "99": ["82"], "100": ["83"],
                },
                "target": "87",
            },
        },
        "en": {
            1: {
                "n": 7,
                "tree": {
                    "1": [],
                    "2": ["1"],
                    "3": ["1"],
                    "4": ["2"],
                    "5": ["2"],
                    "6": ["3"],
                    "7": ["3"],
                },
                "target": "5",
            },
            2: {
                "n": 15,
                "tree": {
                    "1": [],
                    "2": ["1"], "3": ["1"],
                    "4": ["2"], "5": ["2"], "6": ["3"], "7": ["3"],
                    "8": ["4"], "9": ["4"], "10": ["5"], "11": ["5"],
                    "12": ["6"], "13": ["6"], "14": ["7"], "15": ["7"],
                },
                "target": "11",
            },
            3: {
                "n": 31,
                "tree": {
                    "1": [],
                    "2": ["1"], "3": ["1"],
                    "4": ["2"], "5": ["2"], "6": ["3"], "7": ["3"],
                    "8": ["4"], "9": ["4"], "10": ["5"], "11": ["5"],
                    "12": ["6"], "13": ["6"], "14": ["7"], "15": ["7"],
                    "16": ["8"], "17": ["8"], "18": ["9"], "19": ["9"],
                    "20": ["10"], "21": ["10"], "22": ["11"], "23": ["11"],
                    "24": ["12"], "25": ["12"], "26": ["13"], "27": ["13"],
                    "28": ["14"], "29": ["14"], "30": ["15"], "31": ["15"],
                },
                "target": "23",
            },
            4: {
                "n": 50,
                "tree": {
                    "1": [],
                    "2": ["1"], "3": ["1"], "4": ["1"],
                    "5": ["2"], "6": ["2"], "7": ["3"],
                    "8": ["4"], "9": ["4"], "10": ["4"], "11": ["5"],
                    "12": ["5"], "13": ["6"], "14": ["7"], "15": ["7"],
                    "16": ["8"], "17": ["9"], "18": ["9"], "19": ["10"],
                    "20": ["11"], "21": ["11"], "22": ["12"], "23": ["13"],
                    "24": ["13"], "25": ["14"], "26": ["15"], "27": ["15"],
                    "28": ["16"], "29": ["17"], "30": ["18"], "31": ["18"],
                    "32": ["19"], "33": ["19"], "34": ["20"], "35": ["21"],
                    "36": ["22"], "37": ["23"], "38": ["24"], "39": ["25"],
                    "40": ["26"], "41": ["27"], "42": ["28"], "43": ["29"],
                    "44": ["30"], "45": ["31"], "46": ["32"], "47": ["33"],
                    "48": ["34"], "49": ["35"], "50": ["36"],
                },
                "target": "47",
            },
            5: {
                "n": 100,
                "tree": {
                    "1": [],
                    "2": ["1"], "3": ["1"], "4": ["1"], "5": ["1"],
                    "6": ["2"], "7": ["2"], "8": ["3"], "9": ["3"],
                    "10": ["4"], "11": ["4"], "12": ["5"], "13": ["5"],
                    "14": ["6"], "15": ["6"], "16": ["7"], "17": ["8"],
                    "18": ["8"], "19": ["9"], "20": ["10"], "21": ["10"],
                    "22": ["11"], "23": ["12"], "24": ["12"], "25": ["13"],
                    "26": ["14"], "27": ["14"], "28": ["15"], "29": ["16"],
                    "30": ["17"], "31": ["17"], "32": ["18"], "33": ["19"],
                    "34": ["19"], "35": ["20"], "36": ["21"], "37": ["21"],
                    "38": ["22"], "39": ["23"], "40": ["24"], "41": ["25"],
                    "42": ["25"], "43": ["26"], "44": ["27"], "45": ["28"],
                    "46": ["29"], "47": ["30"], "48": ["31"], "49": ["32"],
                    "50": ["33"], "51": ["34"], "52": ["35"], "53": ["36"],
                    "54": ["37"], "55": ["38"], "56": ["39"], "57": ["40"],
                    "58": ["41"], "59": ["42"], "60": ["43"], "61": ["44"],
                    "62": ["45"], "63": ["46"], "64": ["47"], "65": ["48"],
                    "66": ["49"], "67": ["50"], "68": ["51"], "69": ["52"],
                    "70": ["53"], "71": ["54"], "72": ["55"], "73": ["56"],
                    "74": ["57"], "75": ["58"], "76": ["59"], "77": ["60"],
                    "78": ["61"], "79": ["62"], "80": ["63"], "81": ["64"],
                    "82": ["65"], "83": ["66"], "84": ["67"], "85": ["68"],
                    "86": ["69"], "87": ["70"], "88": ["71"], "89": ["72"],
                    "90": ["73"], "91": ["74"], "92": ["75"], "93": ["76"],
                    "94": ["77"], "95": ["78"], "96": ["79"], "97": ["80"],
                    "98": ["81"], "99": ["82"], "100": ["83"],
                },
                "target": "87",
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0
        self.max_queries = 0
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
        
        self.tree = cfg["tree"]
        self.target = cfg["target"]
        
        self.max_queries = math.ceil(math.log2(cfg["n"])) + 2
        
        self._build_subtree_map()
        
        self._game_info["tree_structure"] = self._generate_tree_description()

    def _build_subtree_map(self):
        self.children = {node: [] for node in self.tree.keys()}
        self.parent = {}
        
        for node, parents in self.tree.items():
            if parents:
                parent = parents[0]
                self.children[parent].append(node)
                self.parent[node] = parent
        
        self.subtree = {}
        
        def dfs(node):
            subtree_nodes = {node}
            for child in self.children[node]:
                subtree_nodes.update(dfs(child))
            self.subtree[node] = subtree_nodes
            return subtree_nodes
        
        root = None
        for node in self.tree.keys():
            if not self.tree[node]:
                root = node
                break
        
        if root:
            dfs(root)

    def _generate_tree_description(self):
        lines = []
        
        if self.config.language == "zh":
            for node, parents in sorted(self.tree.items(), key=lambda x: int(x[0])):
                if not parents:
                    lines.append(f"节点 {node}：根节点")
                else:
                    parent = parents[0]
                    lines.append(f"节点 {node}：父节点为 {parent}")
        else:
            for node, parents in sorted(self.tree.items(), key=lambda x: int(x[0])):
                if not parents:
                    lines.append(f"Node {node}: root node")
                else:
                    parent = parents[0]
                    lines.append(f"Node {node}: parent is {parent}")
        
        return "\n".join(lines)

    def step(self, response: str):
        try:
            parsed_info = self.parse(response)
            if "answer" in parsed_info:
                if self.query_count < 2:
                    if self.config.language == "zh":
                        res = "错误：你必须进行至少 2 次祖先查询后才能提交答案。请继续查询。"
                    else:
                        res = "Error: You must perform at least 2 ancestor queries before submitting an answer. Please continue querying."
                    self.state.add_message("user", res)
                    return self.state
                
                is_success = self.evaluate(parsed_info)
                if is_success:
                    res = "答案正确" if self.config.language == "zh" else "Correct answer."
                    self.state.set_state("success", "success")
                    self.state.add_message("user", res)
                else:
                    res = "答案错误" if self.config.language == "zh" else "Incorrect answer."
                    self.state.set_state("failed", "incorrect answer")
                    self.state.add_message("user", res)
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
        except Exception as e:
            self.state.set_state("failed", str(e))
        
        return self.state

    def evaluate(self, parsed_info):
        answer = parsed_info["answer"].strip()
        
        return answer == self.target

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_out_of_range = "错误：节点编号不存在。"
            error_exceed_limit = f"错误：已超过最大查询次数限制（{self.max_queries}次）。请直接提交你的答案。"
        else:
            yes_res, no_res = "Yes", "No"
            error_out_of_range = "Error: Node ID does not exist."
            error_exceed_limit = f"Error: Exceeded maximum query limit ({self.max_queries} queries). Please submit your answer directly."

        if "query_ancestor" in parsed_info:
            if self.query_count >= self.max_queries:
                return error_exceed_limit
            
            query_node = parsed_info["query_ancestor"].strip()
            
            if query_node not in self.tree:
                return error_out_of_range
            
            self.query_count += 1
            
            if self.target in self.subtree.get(query_node, set()):
                return yes_res
            else:
                return no_res
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        for node in self.tree.keys():
            if self.target in self.subtree.get(node, set()):
                ans = yes_res
            else:
                ans = no_res
            
            results.append({
                "query": f"<query_ancestor>{node}</query_ancestor>",
                "answer": ans
            })
            
        return results

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            if correct == "否":
                return "是"
        else:
            lower_correct = correct.lower()
            if lower_correct == "yes":
                return "No" if correct[0].isupper() else "no"
            if lower_correct == "no":
                return "Yes" if correct[0].isupper() else "yes"
        
        return f"{correct}_WRONG"