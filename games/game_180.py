import random
import itertools
from .base import Game

class AdjacentElementGame(Game):

    game_rule_zh = """\
我们来玩一个"相邻元素判定"的推理游戏，规则如下：

游戏设定了一个包含 {n} 个元素的集合 S = {elements}。存在一个固定但未知的线性顺序，集合中的所有元素在这个顺序中排成一列。两个元素称为"相邻"，当且仅当它们在该顺序中占据连续的两个位置，中间没有其他元素。

目标对：你需要判断元素 {target_a} 和 {target_b} 是否在未知顺序中相邻。

允许的查询：你可以反复提出以下类型的查询（每次仅限一个查询）：

- 介值查询：询问元素 Y 是否位于元素 X 和 Z 之间。
  我会回答"是"或"否"。回答"是"表示在未知顺序中，Y 位于 X 和 Z 之间（不论 X 在 Z 前还是 Z 在 X 前）；否则回答"否"。

提交答案：当你收集到足够信息后，请提交最终判定结果。

介值查询格式（询问 Y 是否位于 X 和 Z 之间）：
<query_between>Y,X,Z</query_between>

提交最终答案格式（判定是否相邻）：
<answer>adjacent=yes</answer>
或
<answer>adjacent=no</answer>

注意：
1. 每次只能提出一个查询
2. 查询中的元素必须两两不同且都在集合 S 中
3. 答案必须严格按照上述格式提交
4. 请尽可能少地使用查询次数
"""

    game_rule_en = """\
Let's play an "Adjacent Element Detection" deduction game. Here are the rules:

The game defines a set S with {n} elements: S = {elements}. There exists a fixed but unknown linear order in which all elements are arranged in a sequence. Two elements are called "adjacent" if and only if they occupy two consecutive positions in this order with no other element between them.

Target pair: You need to determine whether elements {target_a} and {target_b} are adjacent in the unknown order.

Allowed queries: You can repeatedly ask the following type of query (one query per turn):

- Between Query: Ask whether element Y is located between elements X and Z.
  I will answer "Yes" or "No". "Yes" means that in the unknown order, Y is positioned between X and Z (regardless of whether X comes before Z or Z comes before X); otherwise, the answer is "No".

Submit answer: When you have gathered enough information, submit your final determination.

Between query format (asking if Y is between X and Z):
<query_between>Y,X,Z</query_between>

Final answer submission format (determining adjacency):
<answer>adjacent=yes</answer>
or
<answer>adjacent=no</answer>

Notes:
1. Only one query can be asked per turn
2. All elements in a query must be distinct and belong to set S
3. The answer must strictly follow the format above
4. Try to use as few queries as possible
"""

    contextualized_rule_zh_1 = """\
我们正在进行一项"轨道交通线网排查"任务，规则如下：

系统设定了一条包含 {n} 个关键站点的公交线路 S = {elements}。存在一个固定但未知的线性站点顺序，集合中的所有站点在这个顺序中排成一列。两个站点称为"相邻"，当且仅当它们在该线路中占据连续的两个位置，中间没有其他站点。

目标对：你需要判断站点 {target_a} 和 {target_b} 是否在未知线路顺序中相邻。

允许的查询：你可以反复提出以下类型的查询（每次仅限一个查询）：

- 介值查询：询问站点 Y 是否位于站点 X 和 Z 之间。
  我会回答"是"或"否"。回答"是"表示在未知线路顺序中，Y 位于 X 和 Z 之间（不论 X 在 Z 前还是 Z 在 X 前）；否则回答"否"。

提交答案：当你收集到足够信息后，请提交最终判定结果。

介值查询格式（询问 Y 是否位于 X 和 Z 之间）：
<query_between>Y,X,Z</query_between>

提交最终答案格式（判定是否相邻）：
<answer>adjacent=yes</answer>
或
<answer>adjacent=no</answer>

注意：
1. 每次只能提出一个查询
2. 查询中的站点必须两两不同且都在集合 S 中
3. 答案必须严格按照上述格式提交
4. 请尽可能少地使用查询次数
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
We are conducting an "Urban Rail Network Inspection" task. Here are the rules:

The system defines a transit line with {n} key stations: S = {elements}. There exists a fixed but unknown linear order in which all stations are arranged on the line. Two stations are called "adjacent" if and only if they occupy two consecutive positions in this order with no other station between them.

Target pair: You need to determine whether stations {target_a} and {target_b} are adjacent in the unknown order.

Allowed queries: You can repeatedly ask the following type of query (one query per turn):

- Between Query: Ask whether station Y is located between stations X and Z.
  I will answer "Yes" or "No". "Yes" means that in the unknown order, Y is positioned between X and Z (regardless of whether X comes before Z or Z comes before X); otherwise, the answer is "No".

Submit answer: When you have gathered enough information, submit your final determination.

Between query format (asking if Y is between X and Z):
<query_between>Y,X,Z</query_between>

Final answer submission format (determining adjacency):
<answer>adjacent=yes</answer>
or
<answer>adjacent=no</answer>

Notes:
1. Only one query can be asked per turn
2. All stations in a query must be distinct and belong to set S
3. The answer must strictly follow the format above
4. Try to use as few queries as possible
"""

    contextualized_rule_zh_2 = """\
我们正在评估一项"临床标准治疗路径"，规则如下：

该路径包含 {n} 个特定的治疗节点 S = {elements}。这些节点按照一个固定但未知的严格线性顺序排列执行。两个治疗节点称为"相邻"，当且仅当它们在流程中紧密衔接，中间没有任何其他过渡阶段或节点。

目标对：你需要判断治疗节点 {target_a} 和 {target_b} 是否在未知流程顺序中相邻。

允许的查询：你可以反复提出以下类型的查询（每次仅限一个查询）：

- 介值查询：询问治疗节点 Y 是否发生于节点 X 和 Z 之间。
  我会回答"是"或"否"。回答"是"表示在未知流程顺序中，Y 位于 X 和 Z 之间（不论 X 在 Z 前还是 Z 在 X 前）；否则回答"否"。

提交答案：当你收集到足够信息后，请提交最终判定结果。

介值查询格式（询问 Y 是否发生于 X 和 Z 之间）：
<query_between>Y,X,Z</query_between>

提交最终答案格式（判定是否相邻）：
<answer>adjacent=yes</answer>
或
<answer>adjacent=no</answer>

注意：
1. 每次只能提出一个查询
2. 查询中的节点必须两两不同且都在集合 S 中
3. 答案必须严格按照上述格式提交
4. 请尽可能少地使用查询次数
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
We are evaluating a "Clinical Standard Treatment Pathway". Here are the rules:

The pathway includes {n} specific treatment nodes: S = {elements}. These nodes are arranged in a fixed but unknown strict linear sequence. Two treatment nodes are called "adjacent" if and only if they are closely connected in the process with no other transitional stage between them.

Target pair: You need to determine whether treatment nodes {target_a} and {target_b} are adjacent in the unknown pathway sequence.

Allowed queries: You can repeatedly ask the following type of query (one query per turn):

- Between Query: Ask whether node Y occurs between nodes X and Z.
  I will answer "Yes" or "No". "Yes" means that in the unknown pathway sequence, Y is positioned between X and Z (regardless of whether X comes before Z or Z comes before X); otherwise, the answer is "No".

Submit answer: When you have gathered enough information, submit your final determination.

Between query format (asking if Y is between X and Z):
<query_between>Y,X,Z</query_between>

Final answer submission format (determining adjacency):
<answer>adjacent=yes</answer>
or
<answer>adjacent=no</answer>

Notes:
1. Only one query can be asked per turn
2. All nodes in a query must be distinct and belong to set S
3. The answer must strictly follow the format above
4. Try to use as few queries as possible
"""

    contextualized_rule_zh_3 = """\
我们正在进行一项"核心课程体系规划"任务，规则如下：

教学大纲包含 {n} 个核心知识模块 S = {elements}。存在一个固定但未知的线性教学顺序，所有模块在这个顺序中依次教授。两个知识模块称为"相邻"，当且仅当它们在教学大纲中占据连续的两个教学单元，中间没有穿插其他模块。

目标对：你需要判断知识模块 {target_a} 和 {target_b} 是否在未知的教学顺序中相邻。

允许的查询：你可以反复提出以下类型的查询（每次仅限一个查询）：

- 介值查询：询问知识模块 Y 是否安排在模块 X 和 Z 之间。
  我会回答"是"或"否"。回答"是"表示在未知教学顺序中，Y 位于 X 和 Z 之间（不论 X 在 Z 前还是 Z 在 X 前）；否则回答"否"。

提交答案：当你收集到足够信息后，请提交最终判定结果。

介值查询格式（询问 Y 是否安排在 X 和 Z 之间）：
<query_between>Y,X,Z</query_between>

提交最终答案格式（判定是否相邻）：
<answer>adjacent=yes</answer>
或
<answer>adjacent=no</answer>

注意：
1. 每次只能提出一个查询
2. 查询中的模块必须两两不同且都在集合 S 中
3. 答案必须严格按照上述格式提交
4. 请尽可能少地使用查询次数
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
We are conducting a "Core Curriculum System Planning" task. Here are the rules:

The syllabus contains {n} core knowledge modules: S = {elements}. There exists a fixed but unknown linear teaching order in which all modules are taught sequentially. Two knowledge modules are called "adjacent" if and only if they occupy two consecutive teaching units in the syllabus with no other module interspersed between them.

Target pair: You need to determine whether knowledge modules {target_a} and {target_b} are adjacent in the unknown teaching order.

Allowed queries: You can repeatedly ask the following type of query (one query per turn):

- Between Query: Ask whether module Y is scheduled between modules X and Z.
  I will answer "Yes" or "No". "Yes" means that in the unknown teaching order, Y is positioned between X and Z (regardless of whether X comes before Z or Z comes before X); otherwise, the answer is "No".

Submit answer: When you have gathered enough information, submit your final determination.

Between query format (asking if Y is between X and Z):
<query_between>Y,X,Z</query_between>

Final answer submission format (determining adjacency):
<answer>adjacent=yes</answer>
or
<answer>adjacent=no</answer>

Notes:
1. Only one query can be asked per turn
2. All modules in a query must be distinct and belong to set S
3. The answer must strictly follow the format above
4. Try to use as few queries as possible
"""

    contextualized_rule_zh_4 = """\
我们正在优化一条"精密制造流水线"，规则如下：

该流水线包含 {n} 道关键加工工序 S = {elements}。存在一个固定但未知的线性执行顺序，所有工序在这个顺序中排成一列。两道工序称为"相邻"，当且仅当它们在流水线上紧邻、占据连续的两个加工步骤，中间没有任何其他工序。

目标对：你需要判断加工工序 {target_a} 和 {target_b} 是否在未知流水线顺序中相邻。

允许的查询：你可以反复提出以下类型的查询（每次仅限一个查询）：

- 介值查询：询问加工工序 Y 是否位于工序 X 和 Z 之间。
  我会回答"是"或"否"。回答"是"表示在未知流水线顺序中，Y 位于 X 和 Z 之间（不论 X 在 Z 前还是 Z 在 X 前）；否则回答"否"。

提交答案：当你收集到足够信息后，请提交最终判定结果。

介值查询格式（询问 Y 是否位于 X 和 Z 之间）：
<query_between>Y,X,Z</query_between>

提交最终答案格式（判定是否相邻）：
<answer>adjacent=yes</answer>
或
<answer>adjacent=no</answer>

注意：
1. 每次只能提出一个查询
2. 查询中的工序必须两两不同且都在集合 S 中
3. 答案必须严格按照上述格式提交
4. 请尽可能少地使用查询次数
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
We are optimizing a "Precision Manufacturing Assembly Line". Here are the rules:

The assembly line consists of {n} critical processing steps: S = {elements}. There exists a fixed but unknown linear execution sequence in which all steps are arranged. Two steps are called "adjacent" if and only if they occupy two consecutive processing stages on the line with no other step between them.

Target pair: You need to determine whether processing steps {target_a} and {target_b} are adjacent in the unknown assembly line sequence.

Allowed queries: You can repeatedly ask the following type of query (one query per turn):

- Between Query: Ask whether step Y is located between steps X and Z.
  I will answer "Yes" or "No". "Yes" means that in the unknown assembly line sequence, Y is positioned between X and Z (regardless of whether X comes before Z or Z comes before X); otherwise, the answer is "No".

Submit answer: When you have gathered enough information, submit your final determination.

Between query format (asking if Y is between X and Z):
<query_between>Y,X,Z</query_between>

Final answer submission format (determining adjacency):
<answer>adjacent=yes</answer>
or
<answer>adjacent=no</answer>

Notes:
1. Only one query can be asked per turn
2. All processing steps in a query must be distinct and belong to set S
3. The answer must strictly follow the format above
4. Try to use as few queries as possible
"""

    contextualized_rule_zh_5 = """\
我们正在审查一个"标准法定审理程序"，规则如下：

案件的审理过程涉及 {n} 个法定环节 S = {elements}。这些环节按照一个固定但未知的严格法定线性顺序执行。两个法定环节称为"相邻"，当且仅当它们在程序上具有直接的先后顺承关系，中间没有穿插其他法定步骤。

目标对：你需要判断法定环节 {target_a} 和 {target_b} 是否在未知的法定顺序中相邻。

允许的查询：你可以反复提出以下类型的查询（每次仅限一个查询）：

- 介值查询：询问法定环节 Y 是否必须在环节 X 和 Z 之间履行。
  我会回答"是"或"否"。回答"是"表示在未知法定顺序中，Y 位于 X 和 Z 之间（不论 X 在 Z 前还是 Z 在 X 前）；否则回答"否"。

提交答案：当你收集到足够信息后，请提交最终判定结果。

介值查询格式（询问 Y 是否位于 X 和 Z 之间）：
<query_between>Y,X,Z</query_between>

提交最终答案格式（判定是否相邻）：
<answer>adjacent=yes</answer>
或
<answer>adjacent=no</answer>

注意：
1. 每次只能提出一个查询
2. 查询中的环节必须两两不同且都在集合 S 中
3. 答案必须严格按照上述格式提交
4. 请尽可能少地使用查询次数
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
We are reviewing a "Standard Statutory Trial Procedure". Here are the rules:

The case trial process involves {n} statutory steps: S = {elements}. These steps are executed according to a fixed but unknown strict statutory linear sequence. Two statutory steps are called "adjacent" if and only if they have a direct sequential relationship in the procedure with no other statutory step in between.

Target pair: You need to determine whether statutory steps {target_a} and {target_b} are adjacent in the unknown statutory sequence.

Allowed queries: You can repeatedly ask the following type of query (one query per turn):

- Between Query: Ask whether statutory step Y must be fulfilled between steps X and Z.
  I will answer "Yes" or "No". "Yes" means that in the unknown statutory sequence, Y is positioned between X and Z (regardless of whether X comes before Z or Z comes before X); otherwise, the answer is "No".

Submit answer: When you have gathered enough information, submit your final determination.

Between query format (asking if Y is between X and Z):
<query_between>Y,X,Z</query_between>

Final answer submission format (determining adjacency):
<answer>adjacent=yes</answer>
or
<answer>adjacent=no</answer>

Notes:
1. Only one query can be asked per turn
2. All steps in a query must be distinct and belong to set S
3. The answer must strictly follow the format above
4. Try to use as few queries as possible
"""

    tags = ["answer", "query_between"]
    reasoning_type = "演绎推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "elements": ["A", "B", "C", "D"],
                "order": ["A", "B", "C", "D"],
                "target_a": "B",
                "target_b": "C",
            },
            2: {
                "n": 6,
                "elements": ["A", "B", "C", "D", "E", "F"],
                "order": ["A", "C", "E", "B", "D", "F"],
                "target_a": "A",
                "target_b": "B",
            },
            3: {
                "n": 7,
                "elements": ["A", "B", "C", "D", "E", "F", "G"],
                "order": ["D", "A", "F", "B", "G", "C", "E"],
                "target_a": "F",
                "target_b": "B",
            },
            4: {
                "n": 8,
                "elements": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "order": ["C", "E", "A", "G", "B", "F", "D", "H"],
                "target_a": "E",
                "target_b": "B",
            },
            5: {
                "n": 10,
                "elements": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                "order": ["B", "F", "D", "H", "A", "I", "C", "E", "G", "J"],
                "target_a": "B",
                "target_b": "A",
            },
        },
        "en": {
            1: {
                "n": 4,
                "elements": ["A", "B", "C", "D"],
                "order": ["A", "B", "C", "D"],
                "target_a": "B",
                "target_b": "C",
            },
            2: {
                "n": 6,
                "elements": ["A", "B", "C", "D", "E", "F"],
                "order": ["A", "C", "E", "B", "D", "F"],
                "target_a": "A",
                "target_b": "B",
            },
            3: {
                "n": 7,
                "elements": ["A", "B", "C", "D", "E", "F", "G"],
                "order": ["D", "A", "F", "B", "G", "C", "E"],
                "target_a": "F",
                "target_b": "B",
            },
            4: {
                "n": 8,
                "elements": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "order": ["C", "E", "A", "G", "B", "F", "D", "H"],
                "target_a": "E",
                "target_b": "B",
            },
            5: {
                "n": 10,
                "elements": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                "order": ["B", "F", "D", "H", "A", "I", "C", "E", "G", "J"],
                "target_a": "B",
                "target_b": "A",
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
        
        self._game_info["n"] = cfg["n"]
        self._game_info["elements"] = "{" + ", ".join(cfg["elements"]) + "}"
        self._game_info["target_a"] = cfg["target_a"]
        self._game_info["target_b"] = cfg["target_b"]
        
        self.order = cfg["order"]
        self.elements = cfg["elements"]
        self.target_a = cfg["target_a"]
        self.target_b = cfg["target_b"]
        
        self.position = {elem: idx for idx, elem in enumerate(self.order)}
        
        pos_a = self.position[self.target_a]
        pos_b = self.position[self.target_b]
        self.ground_truth_adjacent = abs(pos_a - pos_b) == 1

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip().lower()
        
        if "=" not in raw_ans:
            return False
            
        try:
            key, value = raw_ans.split("=", 1)
            key = key.strip()
            value = value.strip()
            
            if key != "adjacent":
                return False
            
            if value == "yes":
                model_answer = True
            elif value == "no":
                model_answer = False
            else:
                return False
                
            return model_answer == self.ground_truth_adjacent
            
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：查询格式无效。请使用格式 <query_between>Y,X,Z</query_between>"
            error_elements = "错误：查询中的元素必须两两不同且都在集合中。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid query format. Please use format <query_between>Y,X,Z</query_between>"
            error_elements = "Error: Query elements must be distinct and all belong to set S."

        if "query_between" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        try:
            raw = parsed_info["query_between"].strip()
            parts = [x.strip() for x in raw.split(",")]
            
            if len(parts) != 3:
                return error_format
            
            y, x, z = parts
            
            if y not in self.elements or x not in self.elements or z not in self.elements:
                return error_elements
            
            if len(set([y, x, z])) != 3:
                return error_elements
            
            pos_y = self.position[y]
            pos_x = self.position[x]
            pos_z = self.position[z]
            
            is_between = (pos_x < pos_y < pos_z) or (pos_z < pos_y < pos_x)
            
            return yes_res if is_between else no_res
            
        except Exception as e:
            return error_format

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            elif correct == "否":
                return "是"
        else:
            if correct.lower() == "yes":
                return "No"
            elif correct.lower() == "no":
                return "Yes"
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        for y, x, z in itertools.permutations(self.elements, 3):
            query_content = f"<query_between>{y},{x},{z}</query_between>"
            
            pos_y = self.position[y]
            pos_x = self.position[x]
            pos_z = self.position[z]
            
            is_between = (pos_x < pos_y < pos_z) or (pos_z < pos_y < pos_x)
            
            answer = yes_res if is_between else no_res
            
            results.append({
                "query": query_content,
                "answer": answer
            })
            
        return results