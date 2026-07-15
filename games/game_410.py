import re
from .base import Game

class HiddenGraphThresholdGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "图"

    game_rule_zh = """\
我们现在来玩一个"隐藏图阈值"推理游戏，规则如下：

游戏设定了一个包含 {n} 个节点的集合（编号为 1 到 {n}），这些节点之间存在一个隐藏的无向连通图。图中每条边都有一个权重，权重取值为 1 到 9 之间的整数。

我已经指定了两个目标节点 S={source} 和 T={target}。

你的任务是：
1. 通过试验查询推断出图中隐藏的判定规则。
2. 确定从节点 S 到节点 T 的最小可行阈值 L*（这是一个 1 到 9 之间的整数）。

你可以反复向我提出试验查询（请尽可能少地使用查询次数）：

**试验查询**：给定两个不同的节点 u 和 v，以及一个阈值 L（L 为 1 到 9 之间的整数），询问在阈值 L 下从 u 到 v 是否成功。我会回答"成功"或"失败"。

注意：对于固定的节点对 (u,v)，如果某个阈值 L 判定为"成功"，则任何大于等于 L 的阈值也必定判定为"成功"。

当你收集足够信息后，请提交最终答案，包括：
- 你推断出的判定规则（用清晰的文字描述）
- 从 S 到 T 的最小可行阈值 L*

每次试验查询使用以下格式（u、v、L 用逗号分隔）：
<query_test>u,v,L</query_test>

例如，查询从节点 1 到节点 3 在阈值 5 下是否成功：
<query_test>1,3,5</query_test>

提交最终答案时，使用以下格式：
<answer>rule=你的规则描述, L_star=数值</answer>

例如：
<answer>rule=判定成功当且仅当阈值大于等于从u到v所有路径中最大边权的最小值, L_star=4</answer>
"""

    game_rule_en = """\
Let's play a "Hidden Graph Threshold" deduction game. Here are the rules:

The game has a set of {n} nodes (numbered from 1 to {n}), connected by a hidden undirected graph. Each edge in the graph has a weight, which is an integer between 1 and 9.

I have specified two target nodes S={source} and T={target}.

Your tasks are:
1. Infer the hidden decision rule through test queries.
2. Determine the minimum feasible threshold L* from node S to node T (an integer between 1 and 9).

You can repeatedly ask me test queries (please use as few queries as possible):

**Test Query**: Given two different nodes u and v, and a threshold L (an integer between 1 and 9), ask whether the connection from u to v succeeds under threshold L. I will answer "Success" or "Failure".

Note: For a fixed node pair (u,v), if a threshold L is judged as "Success", then any threshold greater than or equal to L must also be judged as "Success".

When you have collected enough information, submit your final answer including:
- The decision rule you inferred (described in clear text)
- The minimum feasible threshold L* from S to T

For each test query, use the following format (u, v, L separated by commas):
<query_test>u,v,L</query_test>

For example, to query whether the connection from node 1 to node 3 succeeds under threshold 5:
<query_test>1,3,5</query_test>

When submitting the final answer, use the following format:
<answer>rule=your rule description, L_star=value</answer>

For example:
<answer>rule=Success if and only if threshold is greater than or equal to the minimum bottleneck value among all paths from u to v, L_star=4</answer>
"""

    contextualized_rule_zh_1 = """\
背景：我们现在来解决一个区域物流网的“运输能力”规划问题。
网络包含 {n} 个物流节点（编号 1 到 {n}），节点间通过未知的道路网相连。每条道路都有一个“通行难度”指数（1 到 9 之间的整数）。
你的任务是从起点枢纽 S={source} 将重要物资安全运送到终点枢纽 T={target}。

你的任务是：
1. 通过试验推断出隐藏的路线可行性判定规则。
2. 确定从 S 到 T 所需的最低车辆性能阈值 L*（这是一个 1 到 9 之间的整数）。

你可以反复向我提出试验查询（请尽可能少地使用查询次数）：
**试验查询**：给定两个节点 u 和 v，以及车辆性能 L（1 到 9 的整数），询问车辆能否成功从 u 抵达 v。我会回答"成功"或"失败"。
注意：对于固定的节点对 (u,v)，如果性能 L 判定为"成功"，则任何大于等于 L 的性能也必定"成功"。

提交答案时，请包括：
- 你推断出的判定规则（用清晰的文字描述）
- 最小可行性能阈值 L*

每次试验查询使用以下格式（u、v、L 用逗号分隔）：
<query_test>u,v,L</query_test>

提交最终答案时，使用以下格式：
<answer>rule=你的规则描述, L_star=数值</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Background: Let's solve a "transport capacity" planning problem for a regional logistics network.
The network contains {n} logistics nodes (numbered 1 to {n}), connected by an unknown road network. Each road has a "terrain difficulty" index (an integer between 1 and 9).
Your task is to safely transport critical supplies from the source hub S={source} to the target hub T={target}.

Your tasks are:
1. Infer the hidden route feasibility decision rule through testing.
2. Determine the minimum required vehicle capability threshold L* from S to T (an integer between 1 and 9).

You can repeatedly ask me test queries (please use as few queries as possible):
**Test Query**: Given two nodes u and v, and a vehicle capability L (1 to 9), ask whether the vehicle can successfully reach v from u. I will answer "Success" or "Failure".
Note: For a fixed node pair (u,v), if capability L is judged as "Success", any capability greater than or equal to L will also succeed.

When submitting the final answer, please include:
- The decision rule you inferred (described in clear text)
- The minimum feasible capability threshold L*

For each test query, use the following format (u, v, L separated by commas):
<query_test>u,v,L</query_test>

When submitting the final answer, use the following format:
<answer>rule=your rule description, L_star=value</answer>
"""

    contextualized_rule_zh_2 = """\
背景：我们现在来解决一个医院内跨科室“病患转移”的安全评估问题。
医院包含 {n} 个科室节点（编号 1 到 {n}），由隐藏的转移通道网连接。每条通道都有一个“暴露风险”指数（1 到 9 之间的整数）。
你需要将患者从起点科室 S={source} 安全转移到终点科室 T={target}。

你的任务是：
1. 通过试验推断出隐藏的转移通道安全判定规则。
2. 确定从 S 到 T 所需的最低防护服等级阈值 L*（这是一个 1 到 9 之间的整数）。

你可以反复向我提出试验查询（请尽可能少地使用查询次数）：
**试验查询**：给定两个科室 u 和 v，以及防护等级 L（1 到 9 的整数），询问在防护等级 L 下转移能否成功保障安全。我会回答"成功"或"失败"。
注意：对于固定的科室对 (u,v)，如果防护等级 L 判定为"成功"，则任何大于等于 L 的等级也必定"成功"。

提交答案时，请包括：
- 你推断出的判定规则（用清晰的文字描述）
- 最小安全防护等级阈值 L*

每次试验查询使用以下格式（u、v、L 用逗号分隔）：
<query_test>u,v,L</query_test>

提交最终答案时，使用以下格式：
<answer>rule=你的规则描述, L_star=数值</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Background: Let's solve a cross-department "patient transfer" safety assessment problem.
The hospital contains {n} department nodes (numbered 1 to {n}), connected by a hidden transfer corridor network. Each corridor has an "exposure risk" index (an integer between 1 and 9).
You need to safely transfer a patient from the source department S={source} to the target department T={target}.

Your tasks are:
1. Infer the hidden transfer safety decision rule through testing.
2. Determine the minimum PPE (Personal Protective Equipment) level threshold L* required from S to T (an integer between 1 and 9).

You can repeatedly ask me test queries (please use as few queries as possible):
**Test Query**: Given two departments u and v, and a PPE level L (1 to 9), ask whether the transfer succeeds safely under level L. I will answer "Success" or "Failure".
Note: For a fixed node pair (u,v), if level L is judged as "Success", any level greater than or equal to L will also succeed.

When submitting the final answer, please include:
- The decision rule you inferred (described in clear text)
- The minimum safe PPE level threshold L*

For each test query, use the following format (u, v, L separated by commas):
<query_test>u,v,L</query_test>

When submitting the final answer, use the following format:
<answer>rule=your rule description, L_star=value</answer>
"""

    contextualized_rule_zh_3 = """\
背景：我们现在来规划一个“认知图谱”的学习路径探索问题。
知识库包含 {n} 个核心概念（编号 1 到 {n}），由隐藏的认知关联图连接。每两个相关概念间的“学习跨度”指数（认知难度）为 1 到 9 之间的整数。
你需要引导学生从起点概念 S={source} 逐步学习理解至终点概念 T={target}。

你的任务是：
1. 通过试验推断出隐藏的学习路径连通规则。
2. 确定从掌握 S 到掌握 T 所需的学生最低认知能力阈值 L*（这是一个 1 到 9 之间的整数）。

你可以反复向我提出试验查询（请尽可能少地使用查询次数）：
**试验查询**：给定概念 u 和 v，以及认知能力 L（1 到 9 的整数），询问在该能力 L 下能否成功跨越理解。我会回答"成功"或"失败"。
注意：对于固定的概念对 (u,v)，如果认知能力 L 判定为"成功"，则任何大于等于 L 的能力也必定"成功"。

提交答案时，请包括：
- 你推断出的判定规则（用清晰的文字描述）
- 最小认知能力阈值 L*

每次试验查询使用以下格式（u、v、L 用逗号分隔）：
<query_test>u,v,L</query_test>

提交最终答案时，使用以下格式：
<answer>rule=你的规则描述, L_star=数值</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Background: Let's map out a "cognitive graph" learning path exploration problem.
The knowledge base contains {n} core concepts (numbered 1 to {n}), connected by a hidden cognitive association graph. The "learning leap" index (cognitive difficulty) between related concepts is an integer between 1 and 9.
You need to guide a student to gradually learn and comprehend from the source concept S={source} to the target concept T={target}.

Your tasks are:
1. Infer the hidden learning path connectivity rule through testing.
2. Determine the minimum cognitive ability threshold L* required to master T starting from S (an integer between 1 and 9).

You can repeatedly ask me test queries (please use as few queries as possible):
**Test Query**: Given concepts u and v, and cognitive ability L (1 to 9), ask whether the comprehension leap succeeds under ability L. I will answer "Success" or "Failure".
Note: For a fixed concept pair (u,v), if ability L is judged as "Success", any ability greater than or equal to L will also succeed.

When submitting the final answer, please include:
- The decision rule you inferred (described in clear text)
- The minimum cognitive ability threshold L*

For each test query, use the following format (u, v, L separated by commas):
<query_test>u,v,L</query_test>

When submitting the final answer, use the following format:
<answer>rule=your rule description, L_star=value</answer>
"""

    contextualized_rule_zh_4 = """\
背景：我们现在来解决一个工业管网的“流体输送”瓶颈分析问题。
化工厂包含 {n} 个加工节点（编号 1 到 {n}），由隐藏的管道网连接。每段管道都有一个“阻力/压力”要求（1 到 9 之间的整数）。
你需要将流体从源节点 S={source} 泵送到目标节点 T={target}。

你的任务是：
1. 通过试验推断出隐藏的管网导通判定规则。
2. 确定从 S 到 T 所需的最低泵浦压力阈值 L*（这是一个 1 到 9 之间的整数）。

你可以反复向我提出试验查询（请尽可能少地使用查询次数）：
**试验查询**：给定节点 u 和 v，以及泵浦压力 L（1 到 9 的整数），询问在压力 L 下流体能否成功输送。我会回答"成功"或"失败"。
注意：对于固定的节点对 (u,v)，如果压力 L 判定为"成功"，则任何大于等于 L 的压力也必定"成功"。

提交答案时，请包括：
- 你推断出的判定规则（用清晰的文字描述）
- 最小泵浦压力阈值 L*

每次试验查询使用以下格式（u、v、L 用逗号分隔）：
<query_test>u,v,L</query_test>

提交最终答案时，使用以下格式：
<answer>rule=你的规则描述, L_star=数值</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Background: Let's solve a "fluid transport" bottleneck analysis problem in an industrial pipeline network.
The chemical plant contains {n} processing nodes (numbered 1 to {n}), connected by a hidden pipeline network. Each pipeline segment has a "resistance/pressure" requirement (an integer between 1 and 9).
You need to pump fluid from the source node S={source} to the target node T={target}.

Your tasks are:
1. Infer the hidden pipeline conductivity decision rule through testing.
2. Determine the minimum pump pressure threshold L* required from S to T (an integer between 1 and 9).

You can repeatedly ask me test queries (please use as few queries as possible):
**Test Query**: Given nodes u and v, and pump pressure L (1 to 9), ask whether the fluid transport succeeds under pressure L. I will answer "Success" or "Failure".
Note: For a fixed node pair (u,v), if pressure L is judged as "Success", any pressure greater than or equal to L will also succeed.

When submitting the final answer, please include:
- The decision rule you inferred (described in clear text)
- The minimum pump pressure threshold L*

For each test query, use the following format (u, v, L separated by commas):
<query_test>u,v,L</query_test>

When submitting the final answer, use the following format:
<answer>rule=your rule description, L_star=value</answer>
"""

    contextualized_rule_zh_5 = """\
背景：我们现在来构建一个法庭辩论的“证据链”推导问题。
案件卷宗包含 {n} 个证据节点（编号 1 到 {n}），由隐藏的逻辑关联图连接。每步推导都有一个“证明责任”难度（1 到 9 之间的整数）。
你需要通过源头证据 S={source} 最终推导并证实结论 T={target}。

你的任务是：
1. 通过试验推断出隐藏的逻辑链有效性判定规则。
2. 确定从 S 证出 T 所需的最低论证力度阈值 L*（这是一个 1 到 9 之间的整数）。

你可以反复向我提出试验查询（请尽可能少地使用查询次数）：
**试验查询**：给定节点 u 和 v，以及论证力度 L（1 到 9 的整数），询问在论证力度 L 下逻辑推导能否被采信（成功）。我会回答"成功"或"失败"。
注意：对于固定的节点对 (u,v)，如果论证力度 L 判定为"成功"，则任何大于等于 L 的力度也必定"成功"。

提交答案时，请包括：
- 你推断出的判定规则（用清晰的文字描述）
- 最小论证力度阈值 L*

每次试验查询使用以下格式（u、v、L 用逗号分隔）：
<query_test>u,v,L</query_test>

提交最终答案时，使用以下格式：
<answer>rule=你的规则描述, L_star=数值</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Background: Let's construct an "evidence chain" derivation problem for a court trial.
The case file contains {n} evidentiary nodes (numbered 1 to {n}), connected by a hidden logical association graph. Each deductive step has a "burden of proof" difficulty (an integer between 1 and 9).
You need to ultimately derive and prove the conclusion T={target} starting from the source evidence S={source}.

Your tasks are:
1. Infer the hidden logical chain validity decision rule through testing.
2. Determine the minimum argumentation strength threshold L* required to prove T from S (an integer between 1 and 9).

You can repeatedly ask me test queries (please use as few queries as possible):
**Test Query**: Given nodes u and v, and argumentation strength L (1 to 9), ask whether the logical deduction is accepted (succeeds) under strength L. I will answer "Success" or "Failure".
Note: For a fixed node pair (u,v), if strength L is judged as "Success", any strength greater than or equal to L will also succeed.

When submitting the final answer, please include:
- The decision rule you inferred (described in clear text)
- The minimum argumentation strength threshold L*

For each test query, use the following format (u, v, L separated by commas):
<query_test>u,v,L</query_test>

When submitting the final answer, use the following format:
<answer>rule=your rule description, L_star=value</answer>
"""

    tags = ["answer", "query_test"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "edges": "1-2:3,2-3:2,3-4:4,1-4:5",
                "source": 1,
                "target": 4,
                "expected_L_star": 4,
            },
            2: {
                "n": 5,
                "edges": "1-2:5,2-3:3,3-4:2,4-5:6,1-3:7,2-4:4",
                "source": 1,
                "target": 5,
                "expected_L_star": 6,
            },
            3: {
                "n": 6,
                "edges": "1-2:4,2-3:5,3-4:3,4-6:7,1-5:6,5-6:2,2-5:3,3-6:8",
                "source": 1,
                "target": 6,
                "expected_L_star": 4,
            },
            4: {
                "n": 7,
                "edges": "1-2:5,2-3:4,3-4:6,4-7:3,1-5:7,5-6:2,6-7:5,2-6:8,3-5:3,5-4:4",
                "source": 1,
                "target": 7,
                "expected_L_star": 5,
            },
            5: {
                "n": 8,
                "edges": "1-2:6,2-3:5,3-4:7,4-8:4,1-5:8,5-6:3,6-7:2,7-8:6,2-5:4,3-6:5,4-7:8,5-8:9,2-6:7,3-7:6",
                "source": 1,
                "target": 8,
                "expected_L_star": 6,
            },
        },
        "en": {
            1: {
                "n": 4,
                "edges": "1-2:3,2-3:2,3-4:4,1-4:5",
                "source": 1,
                "target": 4,
                "expected_L_star": 4,
            },
            2: {
                "n": 5,
                "edges": "1-2:5,2-3:3,3-4:2,4-5:6,1-3:7,2-4:4",
                "source": 1,
                "target": 5,
                "expected_L_star": 6,
            },
            3: {
                "n": 6,
                "edges": "1-2:4,2-3:5,3-4:3,4-6:7,1-5:6,5-6:2,2-5:3,3-6:8",
                "source": 1,
                "target": 6,
                "expected_L_star": 4,
            },
            4: {
                "n": 7,
                "edges": "1-2:5,2-3:4,3-4:6,4-7:3,1-5:7,5-6:2,6-7:5,2-6:8,3-5:3,5-4:4",
                "source": 1,
                "target": 7,
                "expected_L_star": 5,
            },
            5: {
                "n": 8,
                "edges": "1-2:6,2-3:5,3-4:7,4-8:4,1-5:8,5-6:3,6-7:2,7-8:6,2-5:4,3-6:5,4-7:8,5-8:9,2-6:7,3-7:6",
                "source": 1,
                "target": 8,
                "expected_L_star": 6,
            },
        },
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
        self._game_info["source"] = cfg["source"]
        self._game_info["target"] = cfg["target"]
        
        self.graph = {}
        for i in range(1, cfg["n"] + 1):
            self.graph[i] = []
        
        for edge_spec in cfg["edges"].split(","):
            nodes, weight = edge_spec.split(":")
            u, v = map(int, nodes.split("-"))
            w = int(weight)
            self.graph[u].append((v, w))
            self.graph[v].append((u, w))
        
        self.source = cfg["source"]
        self.target = cfg["target"]
        self.expected_L_star = cfg["expected_L_star"]
        
        self._precompute_bottleneck_values()

    def _precompute_bottleneck_values(self):
        self.bottleneck = {}
        
        n = self._game_info["n"]
        for start in range(1, n + 1):
            dist = {i: float('inf') for i in range(1, n + 1)}
            dist[start] = 0
            visited = set()
            
            while len(visited) < n:
                u = None
                min_dist = float('inf')
                for node in range(1, n + 1):
                    if node not in visited and dist[node] < min_dist:
                        min_dist = dist[node]
                        u = node
                
                if u is None:
                    break
                    
                visited.add(u)
                
                for v, weight in self.graph[u]:
                    if v not in visited:
                        new_dist = max(dist[u], weight)
                        if new_dist < dist[v]:
                            dist[v] = new_dist
            
            for end in range(1, n + 1):
                if start != end:
                    self.bottleneck[(start, end)] = dist[end]

    def _check_threshold(self, u, v, L):
        if (u, v) not in self.bottleneck:
            return False
        return L >= self.bottleneck[(u, v)]

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        try:
            l_star_match = re.search(r'L_star\s*=\s*(\d+)', raw_ans)
            if not l_star_match:
                return False
            
            L_star = int(l_star_match.group(1))
            
            if L_star != self.expected_L_star:
                return False
            
            rule_match = re.search(r'rule\s*=\s*(.+?)(?:,\s*L_star|$)', raw_ans, re.DOTALL)
            if not rule_match or not rule_match.group(1).strip():
                return False
            
            return True
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            success_res, fail_res = "成功", "失败"
            error_format = "错误：查询格式无效。请使用格式：u,v,L"
            error_range = "错误：节点编号或阈值超出范围。"
            error_same = "错误：节点 u 和 v 必须不同。"
        else:
            success_res, fail_res = "Success", "Failure"
            error_format = "Error: Invalid query format. Please use format: u,v,L"
            error_range = "Error: Node ID or threshold out of range."
            error_same = "Error: Nodes u and v must be different."
        
        if "query_test" in parsed_info:
            try:
                raw = parsed_info["query_test"].strip()
                parts = [x.strip() for x in raw.split(",")]
                
                if len(parts) != 3:
                    return error_format
                
                u, v, L = int(parts[0]), int(parts[1]), int(parts[2])
                
                n = self._game_info["n"]
                if u < 1 or u > n or v < 1 or v > n:
                    return error_range
                
                if L < 1 or L > 9:
                    return error_range
                
                if u == v:
                    return error_same
                
                result = self._check_threshold(u, v, L)
                return success_res if result else fail_res
                
            except ValueError:
                return error_format
            except Exception as e:
                return error_format
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct == "成功":
            return "失败"
        if correct == "失败":
            return "成功"
        
        low = correct.lower()
        if low == "success":
            if correct.isupper(): return "FAILURE"
            if correct.istitle(): return "Failure"
            return "failure"
        if low == "failure":
            if correct.isupper(): return "SUCCESS"
            if correct.istitle(): return "Success"
            return "success"
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        if low == "yes":
            if correct.isupper(): return "NO"
            if correct.istitle(): return "No"
            return "no"
        if low == "no":
            if correct.isupper(): return "YES"
            if correct.istitle(): return "Yes"
            return "yes"
        
        if correct.isdigit():
            return str(int(correct) + 1)
            
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        n = self._game_info["n"]
        
        if self.config.language == "zh":
            success_res, fail_res = "成功", "失败"
        else:
            success_res, fail_res = "Success", "Failure"
        
        for u in range(1, n + 1):
            for v in range(1, n + 1):
                if u == v:
                    continue
                for L in range(1, 10):
                    query_str = f"<query_test>{u},{v},{L}</query_test>"
                    
                    is_success = self._check_threshold(u, v, L)
                    answer = success_res if is_success else fail_res
                    
                    results.append({
                        "query": query_str,
                        "answer": answer
                    })
                    
        return results