from .base import Game
import random
import re

class TreeDistanceGame(Game):

    game_rule_zh = """\
我们现在来玩一个"树结构距离推理"游戏，规则如下：

游戏设定了一个包含 {N} 个不同字符串的集合 S。这些字符串编码了一个隐含的树结构关系，任意两个字符串之间存在确定的距离值。

你的目标是推断出两个特定目标字符串 "{target_a}" 和 "{target_b}" 之间的距离。

你可以进行以下两种操作：

1. 距离查询：选择集合中任意两个字符串 x 和 y（但不能是目标对本身），询问它们之间的距离。我会返回一个非负整数。
2. 提交答案：当你准备好后，提交你推断出的目标对之间的距离值。

- 你最多可以进行 {Q} 次查询（包括无效查询）。
- 你必须至少完成 {R} 次有效查询后才能提交答案。
- 以下情况会被视为无效查询（计入总次数）：
  * 查询的字符串不在集合 S 中
  * 直接查询目标对 "{target_a}" 和 "{target_b}" 之间的距离
  * 已超过最大查询次数
- 累计出现 3 次无效查询将导致游戏失败。

{string_list}

每次只能包含一个操作标签。使用以下 XML 格式：

- 距离查询（例如查询字符串 "a" 和 "ab" 的距离）：
<query>a,ab</query>

- 提交最终答案（例如答案为 5）：
<answer>5</answer>

请仔细观察查询结果中的规律，推断出目标对的距离。
"""

    game_rule_en = """\
Let's play a "Tree Distance Inference" game. Here are the rules:

The game has a set S of {N} distinct strings. These strings encode an implicit tree structure relationship, and there is a definite distance value between any two strings.

Your goal is to infer the distance between two specific target strings "{target_a}" and "{target_b}".

You can perform the following two operations:

1. Distance Query: Select any two strings x and y from the set (but not the target pair itself), and ask for the distance between them. I will return a non-negative integer.
2. Submit Answer: When you are ready, submit the distance value you inferred for the target pair.

- You can make at most {Q} queries (including invalid queries).
- You must complete at least {R} valid queries before submitting your answer.
- The following cases will be considered invalid queries (counted in total):
  * The queried strings are not in set S
  * Directly querying the distance between target pair "{target_a}" and "{target_b}"
  * Already exceeded the maximum number of queries
- Accumulating 3 invalid queries will result in game failure.

{string_list}

Each operation must contain only one tag. Use the following XML format:

- Distance Query (e.g., query distance between "a" and "ab"):
<query>a,ab</query>

- Submit Final Answer (e.g., answer is 5):
<answer>5</answer>

Please carefully observe the patterns in the query results to infer the distance of the target pair.
"""

    contextualized_rule_zh_1 = """\
欢迎使用城市轨道交通线网拓扑分析系统。

游戏设定了一个包含 {N} 个不同站点代码的集合 S。这些站点代码编码了一个隐含的树状支线路网结构，任意两个站点之间存在确定的运行区间数值。

你的目标是推断出两个特定目标站点 "{target_a}" 和 "{target_b}" 之间的运行区间数。

你可以进行以下两种操作：

1. 区间查询：选择集合中任意两个站点 x 和 y（但不能是目标对本身），询问它们之间的运行区间数。调度系统会返回一个非负整数。
2. 提交答案：当你准备好后，提交你推断出的目标对之间的运行区间数值。

- 你最多可以进行 {Q} 次查询（包括无效查询）。
- 你必须至少完成 {R} 次有效查询后才能提交答案。
- 以下情况会被视为无效查询（计入总次数）：
  * 查询的站点代码不在集合 S 中
  * 直接查询目标对 "{target_a}" 和 "{target_b}" 之间的运行区间数
  * 已超过最大查询次数
- 累计出现 3 次无效查询将导致分析系统锁定并任务失败。

{string_list}

每次只能包含一个操作标签。使用以下 XML 格式：

- 区间查询（例如查询站点 "a" 和 "ab" 的运行区间数）：
<query>a,ab</query>

- 提交最终答案（例如答案为 5）：
<answer>5</answer>

请仔细观察查询结果中的线网拓扑规律，推断出目标站点对的运行区间数。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the Urban Rail Transit Network Topology Analysis System.

The system features a set S of {N} distinct station codes. These codes encode an implicit tree-like branch network structure, and there is a definite number of operational intervals between any two stations.

Your goal is to infer the number of intervals between two specific target stations "{target_a}" and "{target_b}".

You can perform the following two operations:

1. Interval Query: Select any two stations x and y from the set (but not the target pair itself), and ask for the number of intervals between them. The dispatch system will return a non-negative integer.
2. Submit Answer: When you are ready, submit the interval value you inferred for the target pair.

- You can make at most {Q} queries (including invalid queries).
- You must complete at least {R} valid queries before submitting your answer.
- The following cases will be considered invalid queries (counted in total):
  * The queried station codes are not in set S
  * Directly querying the intervals between target pair "{target_a}" and "{target_b}"
  * Already exceeded the maximum number of queries
- Accumulating 3 invalid queries will result in system lockout and task failure.

{string_list}

Each operation must contain only one tag. Use the following XML format:

- Interval Query (e.g., query intervals between station "a" and "ab"):
<query>a,ab</query>

- Submit Final Answer (e.g., answer is 5):
<answer>5</answer>

Please carefully observe the topological patterns in the query results to infer the number of intervals for the target station pair.
"""

    contextualized_rule_zh_2 = """\
欢迎使用病毒基因谱系变异分析追踪系统。

本系统包含了一个包含 {N} 个不同毒株代号的集合 S。这些代号编码了一个隐含的树状演化谱系结构，任意两个毒株之间存在确定的基因代差步数。

你的目标是推断出两个特定目标毒株 "{target_a}" 和 "{target_b}" 之间的基因代差步数。

你可以进行以下两种操作：

1. 测序查询：选择集合中任意两个毒株 x 和 y（但不能是目标对本身），询问它们之间的基因代差步数。实验室测序系统会返回一个非负整数。
2. 提交答案：当你准备好后，提交你推断出的目标对之间的基因代差步数值。

- 你最多可以进行 {Q} 次测序查询（包括无效查询）。
- 你必须至少完成 {R} 次有效查询后才能提交最终诊断答案。
- 以下情况会被视为无效查询（计入总次数）：
  * 查询的毒株代号不在集合 S 中
  * 直接查询目标对 "{target_a}" 和 "{target_b}" 之间的基因代差步数
  * 已超过最大查询次数
- 累计出现 3 次无效查询将导致测序资源耗尽，任务失败。

{string_list}

每次只能包含一个操作标签。使用以下 XML 格式：

- 测序查询（例如查询毒株 "a" 和 "ab" 的基因代差步数）：
<query>a,ab</query>

- 提交最终答案（例如答案为 5）：
<answer>5</answer>

请仔细观察查询结果中的演化规律，推断出目标毒株对的基因代差步数。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the Viral Genomic Lineage Mutation Tracking System.

The system features a set S of {N} distinct viral strain codes. These codes encode an implicit tree-like evolutionary lineage structure, and there is a definite genetic generational difference (in steps) between any two strains.

Your goal is to infer the genetic generational difference between two specific target strains "{target_a}" and "{target_b}".

You can perform the following two operations:

1. Sequencing Query: Select any two strains x and y from the set (but not the target pair itself), and ask for the genetic generational difference between them. The laboratory sequencing system will return a non-negative integer.
2. Submit Answer: When you are ready, submit the generational difference value you inferred for the target pair.

- You can make at most {Q} sequencing queries (including invalid queries).
- You must complete at least {R} valid queries before submitting your final diagnostic answer.
- The following cases will be considered invalid queries (counted in total):
  * The queried strain codes are not in set S
  * Directly querying the difference between target pair "{target_a}" and "{target_b}"
  * Already exceeded the maximum number of queries
- Accumulating 3 invalid queries will result in depletion of sequencing resources and task failure.

{string_list}

Each operation must contain only one tag. Use the following XML format:

- Sequencing Query (e.g., query difference between strain "a" and "ab"):
<query>a,ab</query>

- Submit Final Answer (e.g., answer is 5):
<answer>5</answer>

Please carefully observe the evolutionary patterns in the query results to infer the genetic generational difference of the target strain pair.
"""

    contextualized_rule_zh_3 = """\
欢迎使用学科知识图谱先决条件评估引擎。

评估引擎载入了一个包含 {N} 个不同知识点编码的集合 S。这些知识点编码了一个隐含的树状先决条件层级结构，任意两个知识点之间存在确定的认知跨度（关联层级数）。

你的目标是推断出两个特定目标知识点 "{target_a}" 和 "{target_b}" 之间的关联层级数。

你可以进行以下两种操作：

1. 跨度查询：选择集合中任意两个知识点 x 和 y（但不能是目标对本身），询问它们之间的关联层级数。评估引擎会返回一个非负整数。
2. 提交答案：当你准备好后，提交你推断出的目标知识点对之间的关联层级数值。

- 你最多可以进行 {Q} 次跨度查询（包括无效查询）。
- 你必须至少完成 {R} 次有效查询后才能提交评估答案。
- 以下情况会被视为无效查询（计入总次数）：
  * 查询的知识点编码不在集合 S 中
  * 直接查询目标对 "{target_a}" 和 "{target_b}" 之间的关联层级数
  * 已超过最大查询次数
- 累计出现 3 次无效查询将导致评估中止，任务失败。

{string_list}

每次只能包含一个操作标签。使用以下 XML 格式：

- 跨度查询（例如查询知识点 "a" 和 "ab" 的关联层级数）：
<query>a,ab</query>

- 提交最终答案（例如答案为 5）：
<answer>5</answer>

请仔细观察查询结果中的层级结构规律，推断出目标知识点对的关联层级数。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Subject Knowledge Graph Prerequisite Assessment Engine.

The engine has loaded a set S of {N} distinct knowledge point codes. These codes encode an implicit tree-like prerequisite hierarchical structure, and there is a definite cognitive span (number of relational tiers) between any two knowledge points.

Your goal is to infer the number of relational tiers between two specific target knowledge points "{target_a}" and "{target_b}".

You can perform the following two operations:

1. Span Query: Select any two knowledge points x and y from the set (but not the target pair itself), and ask for the number of relational tiers between them. The assessment engine will return a non-negative integer.
2. Submit Answer: When you are ready, submit the tier value you inferred for the target pair.

- You can make at most {Q} span queries (including invalid queries).
- You must complete at least {R} valid queries before submitting your answer.
- The following cases will be considered invalid queries (counted in total):
  * The queried knowledge point codes are not in set S
  * Directly querying the tiers between target pair "{target_a}" and "{target_b}"
  * Already exceeded the maximum number of queries
- Accumulating 3 invalid queries will result in assessment termination and task failure.

{string_list}

Each operation must contain only one tag. Use the following XML format:

- Span Query (e.g., query tiers between point "a" and "ab"):
<query>a,ab</query>

- Submit Final Answer (e.g., answer is 5):
<answer>5</answer>

Please carefully observe the hierarchical patterns in the query results to infer the number of relational tiers of the target knowledge point pair.
"""

    contextualized_rule_zh_4 = """\
欢迎使用企业资源计划(ERP)产品物料清单(BOM)分解系统。

本系统设定了一个包含 {N} 个不同零部件编号的集合 S。这些编号编码了一个隐含的树状生产装配层级结构，任意两个零部件之间存在确定的工艺节点步数（装配层级差异）。

你的目标是推断出两个特定目标零部件 "{target_a}" 和 "{target_b}" 之间的工艺节点步数。

你可以进行以下两种操作：

1. 工艺查询：选择集合中任意两个零部件 x 和 y（但不能是目标对本身），询问它们之间的工艺节点步数。ERP系统会返回一个非负整数。
2. 提交答案：当你准备好后，提交你推断出的目标对之间的工艺节点步数值。

- 你最多可以进行 {Q} 次工艺查询（包括无效查询）。
- 你必须至少完成 {R} 次有效查询后才能提交排产答案。
- 以下情况会被视为无效查询（计入总次数）：
  * 查询的零部件编号不在物料集合 S 中
  * 直接查询目标对 "{target_a}" 和 "{target_b}" 之间的工艺节点步数
  * 已超过最大查询次数
- 累计出现 3 次无效查询将导致系统阻断排产并判定任务失败。

{string_list}

每次只能包含一个操作标签。使用以下 XML 格式：

- 工艺查询（例如查询零部件 "a" 和 "ab" 的工艺节点步数）：
<query>a,ab</query>

- 提交最终答案（例如答案为 5）：
<answer>5</answer>

请仔细观察查询结果中的装配分解规律，推断出目标零部件对的工艺节点步数。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the Enterprise Resource Planning (ERP) Bill of Materials (BOM) Decomposition System.

The system features a set S of {N} distinct part numbers. These numbers encode an implicit tree-like production assembly hierarchical structure, and there is a definite number of process node steps (assembly level difference) between any two parts.

Your goal is to infer the number of process node steps between two specific target parts "{target_a}" and "{target_b}".

You can perform the following two operations:

1. Process Query: Select any two parts x and y from the set (but not the target pair itself), and ask for the number of process node steps between them. The ERP system will return a non-negative integer.
2. Submit Answer: When you are ready, submit the process node step value you inferred for the target pair.

- You can make at most {Q} process queries (including invalid queries).
- You must complete at least {R} valid queries before submitting your scheduling answer.
- The following cases will be considered invalid queries (counted in total):
  * The queried part numbers are not in material set S
  * Directly querying the steps between target pair "{target_a}" and "{target_b}"
  * Already exceeded the maximum number of queries
- Accumulating 3 invalid queries will result in scheduling blockade and task failure.

{string_list}

Each operation must contain only one tag. Use the following XML format:

- Process Query (e.g., query steps between part "a" and "ab"):
<query>a,ab</query>

- Submit Final Answer (e.g., answer is 5):
<answer>5</answer>

Please carefully observe the assembly decomposition patterns in the query results to infer the number of process node steps for the target part pair.
"""

    contextualized_rule_zh_5 = """\
欢迎使用智能法律检索引擎与条款溯源系统。

该检索引擎包含了一个含有 {N} 个不同法典条款编号的集合 S。这些编号编码了一个隐含的树状条款引用与法条层级结构，任意两条款之间存在确定的法律层级跨度。

你的目标是推断出两个特定目标条款 "{target_a}" 和 "{target_b}" 之间的法律层级跨度。

你可以进行以下两种操作：

1. 跨度检索：选择集合中任意两条款 x 和 y（但不能是目标对本身），询问它们之间的法律层级跨度。检索引擎会返回一个非负整数。
2. 提交答案：当你准备好后，提交你推断出的目标条款对之间的法律层级跨度值。

- 你最多可以进行 {Q} 次跨度检索（包括无效检索）。
- 你必须至少完成 {R} 次有效检索后才能提交分析答案。
- 以下情况会被视为无效检索（计入总次数）：
  * 检索的条款编号不在法典集合 S 中
  * 直接检索目标对 "{target_a}" 和 "{target_b}" 之间的法律层级跨度
  * 已超过最大检索次数
- 累计出现 3 次无效检索将导致检索引擎拒绝服务及任务失败。

{string_list}

每次只能包含一个操作标签。使用以下 XML 格式：

- 跨度检索（例如检索条款 "a" 和 "ab" 的法律层级跨度）：
<query>a,ab</query>

- 提交最终答案（例如答案为 5）：
<answer>5</answer>

请仔细观察检索结果中的条款引用与层级规律，推断出目标条款对的法律层级跨度。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Intelligent Legal Retrieval Engine and Clause Tracing System.

The retrieval engine contains a set S of {N} distinct legal clause numbers. These numbers encode an implicit tree-like clause citation and hierarchical structure, and there is a definite legal hierarchical span between any two clauses.

Your goal is to infer the legal hierarchical span between two specific target clauses "{target_a}" and "{target_b}".

You can perform the following two operations:

1. Span Retrieval: Select any two clauses x and y from the set (but not the target pair itself), and ask for the legal hierarchical span between them. The retrieval engine will return a non-negative integer.
2. Submit Answer: When you are ready, submit the span value you inferred for the target pair.

- You can make at most {Q} span retrievals (including invalid retrievals).
- You must complete at least {R} valid retrievals before submitting your analytical answer.
- The following cases will be considered invalid retrievals (counted in total):
  * The retrieved clause numbers are not in the legal set S
  * Directly retrieving the span between target pair "{target_a}" and "{target_b}"
  * Already exceeded the maximum number of retrievals
- Accumulating 3 invalid retrievals will result in denial of service and task failure.

{string_list}

Each operation must contain only one tag. Use the following XML format:

- Span Retrieval (e.g., retrieve span between clause "a" and "ab"):
<query>a,ab</query>

- Submit Final Answer (e.g., answer is 5):
<answer>5</answer>

Please carefully observe the citation and hierarchical patterns in the retrieval results to infer the legal hierarchical span for the target clause pair.
"""

    tags = ["answer", "query"]
    
    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "N": 5,
                "Q": 8,
                "R": 3,
                "strings": ["a", "ab", "abc", "ad", "ade"],
                "target_a": "abc",
                "target_b": "ade",
            },
            2: {
                "N": 7,
                "Q": 10,
                "R": 4,
                "strings": ["x", "xy", "xyz", "xyw", "xa", "xab", "xac"],
                "target_a": "xyz",
                "target_b": "xac",
            },
            3: {
                "N": 10,
                "Q": 12,
                "R": 5,
                "strings": ["r", "ra", "rab", "rabc", "rad", "rb", "rba", "rbb", "rc", "rcd"],
                "target_a": "rabc",
                "target_b": "rbb",
            },
            4: {
                "N": 12,
                "Q": 15,
                "R": 6,
                "strings": ["s", "sa", "sab", "sabc", "sad", "sade", "sb", "sbc", "sbcd", "sc", "scd", "sce"],
                "target_a": "sabc",
                "target_b": "sce",
            },
            5: {
                "N": 15,
                "Q": 18,
                "R": 7,
                "strings": ["t", "ta", "tab", "tabc", "tabcd", "tad", "tade", "tb", "tbc", "tbcd", "tbce", "tc", "tcd", "tce", "tcef"],
                "target_a": "tabcd",
                "target_b": "tcef",
            },
        },
        "en": {
            1: {
                "N": 5,
                "Q": 8,
                "R": 3,
                "strings": ["a", "ab", "abc", "ad", "ade"],
                "target_a": "abc",
                "target_b": "ade",
            },
            2: {
                "N": 7,
                "Q": 10,
                "R": 4,
                "strings": ["x", "xy", "xyz", "xyw", "xa", "xab", "xac"],
                "target_a": "xyz",
                "target_b": "xac",
            },
            3: {
                "N": 10,
                "Q": 12,
                "R": 5,
                "strings": ["r", "ra", "rab", "rabc", "rad", "rb", "rba", "rbb", "rc", "rcd"],
                "target_a": "rabc",
                "target_b": "rbb",
            },
            4: {
                "N": 12,
                "Q": 15,
                "R": 6,
                "strings": ["s", "sa", "sab", "sabc", "sad", "sade", "sb", "sbc", "sbcd", "sc", "scd", "sce"],
                "target_a": "sabc",
                "target_b": "sce",
            },
            5: {
                "N": 15,
                "Q": 18,
                "R": 7,
                "strings": ["t", "ta", "tab", "tabc", "tabcd", "tad", "tade", "tb", "tbc", "tbcd", "tbce", "tc", "tcd", "tce", "tcef"],
                "target_a": "tabcd",
                "target_b": "tcef",
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0
        self.valid_query_count = 0
        self.invalid_query_count = 0
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self._game_info["N"] = cfg["N"]
        self._game_info["Q"] = cfg["Q"]
        self._game_info["R"] = cfg["R"]
        self._game_info["target_a"] = cfg["target_a"]
        self._game_info["target_b"] = cfg["target_b"]
        
        self._game_info["string_list"] = ", ".join([f'"{s}"' for s in cfg["strings"]])
        
        self.strings = set(cfg["strings"])
        self.target_a = cfg["target_a"]
        self.target_b = cfg["target_b"]
        self.Q = cfg["Q"]
        self.R = cfg["R"]
        
        self.true_distance = self._calculate_distance(self.target_a, self.target_b)

    def _calculate_distance(self, s1: str, s2: str) -> int:
        lcp_len = 0
        for i in range(min(len(s1), len(s2))):
            if s1[i] == s2[i]:
                lcp_len += 1
            else:
                break
        return len(s1) + len(s2) - 2 * lcp_len

    def _is_valid_query(self, s1: str, s2: str) -> tuple:
        if self.config.language == "zh":
            if self.query_count >= self.Q:
                return False, "错误：已超过最大查询次数。"
            
            if s1 not in self.strings:
                return False, f'错误：字符串 "{s1}" 不在集合中。'
            if s2 not in self.strings:
                return False, f'错误：字符串 "{s2}" 不在集合中。'
            
            if (s1 == self.target_a and s2 == self.target_b) or \
               (s1 == self.target_b and s2 == self.target_a):
                return False, "错误：不能直接查询目标对的距离。"
            
            return True, ""
        else:
            if self.query_count >= self.Q:
                return False, "Error: Maximum number of queries exceeded."
            
            if s1 not in self.strings:
                return False, f'Error: String "{s1}" is not in the set.'
            if s2 not in self.strings:
                return False, f'Error: String "{s2}" is not in the set.'
            
            if (s1 == self.target_a and s2 == self.target_b) or \
               (s1 == self.target_b and s2 == self.target_a):
                return False, "Error: Cannot directly query the target pair distance."
            
            return True, ""

    def step(self, response: str):
        try:
            parsed_info = self.parse(response)
            if "answer" in parsed_info:
                if self.valid_query_count < self.R:
                    if self.config.language == "zh":
                        msg = (f"错误：必须至少完成 {self.R} 次有效查询后才能提交答案。"
                               f"当前有效查询次数：{self.valid_query_count}")
                    else:
                        msg = (f"Error: Must complete at least {self.R} valid queries before submitting. "
                               f"Current valid queries: {self.valid_query_count}")
                    self.state.add_message("user", msg)
                else:
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
        try:
            submitted_distance = int(parsed_info["answer"].strip())
            return submitted_distance == self.true_distance
        except ValueError:
            return False

    def _cf_core_produce(self, parsed_info):
        if "query" not in parsed_info:
            if self.config.language == "zh":
                return "错误：无效的查询格式。"
            else:
                return "Error: Invalid query format."
        
        self.query_count += 1
        
        try:
            raw_query = parsed_info["query"].strip()
            parts = [p.strip() for p in raw_query.split(",")]
            
            if len(parts) != 2:
                self.invalid_query_count += 1
                if self.invalid_query_count >= 3:
                    self.state.set_state("failed", "too many invalid queries")
                    if self.config.language == "zh":
                        return "错误：累计 3 次无效查询，游戏失败。"
                    else:
                        return "Error: 3 invalid queries accumulated, game failed."
                
                if self.config.language == "zh":
                    return f"无效查询（{self.invalid_query_count}/3）：格式错误，应为 'x,y' 格式。"
                else:
                    return f"Invalid query ({self.invalid_query_count}/3): Format error, should be 'x,y'."
            
            s1, s2 = parts[0], parts[1]
            
            is_valid, error_msg = self._is_valid_query(s1, s2)
            
            if not is_valid:
                self.invalid_query_count += 1
                if self.invalid_query_count >= 3:
                    self.state.set_state("failed", "too many invalid queries")
                    if self.config.language == "zh":
                        return f"{error_msg}\n累计 3 次无效查询，游戏失败。"
                    else:
                        return f"{error_msg}\n3 invalid queries accumulated, game failed."
                
                if self.config.language == "zh":
                    return f"无效查询（{self.invalid_query_count}/3）：{error_msg}"
                else:
                    return f"Invalid query ({self.invalid_query_count}/3): {error_msg}"
            
            self.valid_query_count += 1
            distance = self._calculate_distance(s1, s2)
            
            if self.config.language == "zh":
                return f"距离为 {distance}。（有效查询：{self.valid_query_count}/{self.R}，总查询：{self.query_count}/{self.Q}）"
            else:
                return f"Distance is {distance}. (Valid queries: {self.valid_query_count}/{self.R}, Total queries: {self.query_count}/{self.Q})"
            
        except Exception as e:
            self.invalid_query_count += 1
            if self.invalid_query_count >= 3:
                self.state.set_state("failed", "too many invalid queries")
                if self.config.language == "zh":
                    return "错误：查询解析失败。累计 3 次无效查询，游戏失败。"
                else:
                    return "Error: Query parsing failed. 3 invalid queries accumulated, game failed."
            
            if self.config.language == "zh":
                return f"无效查询（{self.invalid_query_count}/3）：查询解析失败。"
            else:
                return f"Invalid query ({self.invalid_query_count}/3): Query parsing failed."

    def _cf_make_wrong(self, correct: str) -> str:
        if self.config.language == "zh":
            match = re.search(r'距离为\s*(\d+)', correct)
        else:
            match = re.search(r'Distance is\s*(\d+)', correct)
        
        if match:
            original_val = int(match.group(1))
            wrong_val = original_val + random.choice([1, 2, 3])
            return correct.replace(match.group(1), str(wrong_val), 1)
        
        if correct.strip().lstrip('-').isdigit():
            return str(int(correct.strip()) + 1)
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        s_list = sorted(list(self.strings))
        
        for s1 in s_list:
            for s2 in s_list:
                if s1 == s2:
                    continue
                
                if (s1 == self.target_a and s2 == self.target_b) or \
                   (s1 == self.target_b and s2 == self.target_a):
                    continue
                
                dist = self._calculate_distance(s1, s2)
                
                query_str = f"<query>{s1},{s2}</query>"
                
                if self.config.language == "zh":
                    answer_str = f"距离为 {dist}。"
                else:
                    answer_str = f"Distance is {dist}."
                
                queries.append({
                    "query": query_str,
                    "answer": answer_str
                })
        
        return queries