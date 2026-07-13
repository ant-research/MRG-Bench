# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   路径存在性：某条给定的节点序列是否构成合法路径
# ============================================================

import random
import re
from .base import Game


class HiddenGraphReasoningGameTransport(Game):

    contextualized_rule_zh_1 = """\
欢迎来到"隐藏物流网络推理"系统。
【交通物流场景】
我们的物流枢纽网络由顶点集合 V = {{A, B, C, D, E, F}}（代表6个核心城市枢纽）构成。我已秘密选择了以下四种公路连通蓝图中的一种作为真实运行的物流网络：

- 蓝图 G1：直连公路为 A-B, B-C, C-F, B-E, E-F, D-E, A-D
- 蓝图 G2：直连公路为 A-C, C-D, D-F, A-B, B-E, E-F
- 蓝图 G3：直连公路为 A-D, D-B, B-F, A-E, E-C, C-F, A-C
- 蓝图 G4：直连公路为 A-B, B-C, A-C, C-F, A-D, D-B, C-D, D-F, A-E, E-C, D-E, E-F

你的目标是通过向交通控制中心查询，推断出正在运行的真实蓝图是哪一个，并规划出一条从枢纽 A 到枢纽 F 的有效运输路径。

你可以对以下八条固定的三枢纽中转序列发起连通性查询（每次查询一条）：
- R1: A-B-C
- R2: A-B-E
- R3: A-C-F
- R4: A-D-B
- R5: B-E-F
- R6: C-D-F
- R7: A-E-C
- R8: D-E-F

对于每条序列 Rk（如 A-B-C），控制中心会回答"是"或"否"：
- "是"：表示该序列的两段相邻路段（如 A-B 和 B-C）均在真实网络中直接连通
- "否"：表示至少有一段路段在真实网络中未直接连通

## 系统规则
1. 你最多可以进行 {max_queries} 次查询
2. 你必须至少进行 {min_queries} 次查询后才能提交最终的线路规划
3. 提交答案时需要包含：
   - 你认为的真实蓝图（G1/G2/G3/G4）
   - 一条从枢纽 A 到枢纽 F 的完整运输路径（路径中相邻枢纽必须在该蓝图中有直接公路连接）

## 查询与提交答案的格式
每次查询请使用以下 XML 格式（编号为 1 到 8）：
<query>1</query>

提交最终答案时，请使用以下格式：
<answer>graph=G1, path=A-B-C-F</answer>

其中 graph 为你选择的蓝图（G1/G2/G3/G4），path 为从 A 到 F 的路径，枢纽间用短横线连接。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Hidden Logistics Network Reasoning" system.

Our logistics hub network consists of a vertex set V = {{A, B, C, D, E, F}} (representing 6 core city hubs). I have secretly selected one of the following four highway connectivity blueprints as the active logistics network:

- Blueprint G1: Direct highways are A-B, B-C, C-F, B-E, E-F, D-E, A-D
- Blueprint G2: Direct highways are A-C, C-D, D-F, A-B, B-E, E-F
- Blueprint G3: Direct highways are A-D, D-B, B-F, A-E, E-C, C-F, A-C
- Blueprint G4: Direct highways are A-B, B-C, A-C, C-F, A-D, D-B, C-D, D-F, A-E, E-C, D-E, E-F

Your goal is to deduce the active blueprint through inquiries to the traffic control center, and plan a valid transport route from Hub A to Hub F.

You can query the following eight fixed three-hub transit sequences for connectivity validation (one query at a time):
- R1: A-B-C
- R2: A-B-E
- R3: A-C-F
- R4: A-D-B
- R5: B-E-F
- R6: C-D-F
- R7: A-E-C
- R8: D-E-F

For each sequence Rk (e.g., A-B-C), the control center will answer "Yes" or "No":
- "Yes": Both adjacent segments in the sequence (e.g., A-B and B-C) are directly connected in the true network.
- "No": At least one segment is not directly connected in the true network.

## System Rules
1. You can make at most {max_queries} queries.
2. You must make at least {min_queries} queries before submitting your final route plan.
3. When submitting your answer, include:
   - The true blueprint you believe is active (G1/G2/G3/G4)
   - A complete transport path from Hub A to Hub F (adjacent hubs in the path must have a direct highway connection in the blueprint)

## Query and Answer Format
For each query, use the following XML format (number from 1 to 8):
<query>1</query>

When submitting the final answer, use this format:
<answer>graph=G1, path=A-B-C-F</answer>

Where graph is your chosen blueprint (G1/G2/G3/G4), and path is the route from A to F with hubs connected by hyphens.
"""

    game_rule_zh = contextualized_rule_zh_1
    game_rule_en = contextualized_rule_en_1

    tags = ["answer", "query"]
    reasoning_type = "溯因推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"true_graph": "G1", "max_queries": 6, "min_queries": 2},
            2: {"true_graph": "G2", "max_queries": 5, "min_queries": 2},
            3: {"true_graph": "G3", "max_queries": 4, "min_queries": 2},
            4: {"true_graph": "G4", "max_queries": 4, "min_queries": 3},
            5: {"true_graph": "G3", "max_queries": 3, "min_queries": 2},
        },
        "en": {
            1: {"true_graph": "G1", "max_queries": 6, "min_queries": 2},
            2: {"true_graph": "G2", "max_queries": 5, "min_queries": 2},
            3: {"true_graph": "G3", "max_queries": 4, "min_queries": 2},
            4: {"true_graph": "G4", "max_queries": 4, "min_queries": 3},
            5: {"true_graph": "G3", "max_queries": 3, "min_queries": 2},
        },
    }

    GRAPHS = {
        "G1": {("A", "B"), ("B", "C"), ("C", "F"), ("B", "E"), ("E", "F"), ("D", "E"), ("A", "D")},
        "G2": {("A", "C"), ("C", "D"), ("D", "F"), ("A", "B"), ("B", "E"), ("E", "F")},
        "G3": {("A", "D"), ("D", "B"), ("B", "F"), ("A", "E"), ("E", "C"), ("C", "F"), ("A", "C")},
        "G4": {("A", "B"), ("B", "C"), ("A", "C"), ("C", "F"), ("A", "D"), ("D", "B"), 
               ("C", "D"), ("D", "F"), ("A", "E"), ("E", "C"), ("D", "E"), ("E", "F")},
    }

    ROUTES = {
        1: ["A", "B", "C"],
        2: ["A", "B", "E"],
        3: ["A", "C", "F"],
        4: ["A", "D", "B"],
        5: ["B", "E", "F"],
        6: ["C", "D", "F"],
        7: ["A", "E", "C"],
        8: ["D", "E", "F"],
    }

    def __init__(self, config):
        self.query_count = 0  
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保是整数

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.true_graph_name = cfg["true_graph"]
        self.max_queries = cfg["max_queries"]
        self.min_queries = cfg["min_queries"]
        
        self.true_graph_edges = self.GRAPHS[self.true_graph_name]
        
        self._game_info["max_queries"] = self.max_queries
        self._game_info["min_queries"] = self.min_queries

    def _has_edge(self, v1, v2):
        """检查两个顶点之间是否有边（无向图）"""
        return (v1, v2) in self.true_graph_edges or (v2, v1) in self.true_graph_edges

    def _is_route_valid(self, route):
        """检查一条三节点路径在真实图中是否有效"""
        if len(route) != 3:
            return False
        return self._has_edge(route[0], route[1]) and self._has_edge(route[1], route[2])

    def _is_path_valid(self, graph_name, path_nodes):
        """检查一条路径在指定图中是否合法"""
        if len(path_nodes) < 2:
            return False
        
        graph_edges = self.GRAPHS.get(graph_name, set())
        
        for i in range(len(path_nodes) - 1):
            v1, v2 = path_nodes[i], path_nodes[i + 1]
            if (v1, v2) not in graph_edges and (v2, v1) not in graph_edges:
                return False
        
        return True

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        if self.query_count < self.min_queries:
            # 不在这里设置状态，让基类统一处理
            return False
        
        raw_ans = parsed_info["answer"]
        
        try:
            parts = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            for part in parts:
                if "=" in part:
                    k, v = part.split("=", 1)
                    ans_dict[k.strip()] = v.strip()
            
            if "graph" not in ans_dict or "path" not in ans_dict:
                return False
            
            submitted_graph = ans_dict["graph"]
            submitted_path = ans_dict["path"]
            
            if submitted_graph != self.true_graph_name:
                return False
            
            path_nodes = [x.strip() for x in submitted_path.split("-")]
            
            if len(path_nodes) < 2 or path_nodes[0] != "A" or path_nodes[-1] != "F":
                return False
            
            if not self._is_path_valid(self.true_graph_name, path_nodes):
                return False
            
            return True
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_invalid = "错误：无效的查询编号，请使用 1 到 8 之间的数字。"
        else:
            yes_res, no_res = "Yes", "No"
            error_invalid = "Error: Invalid query number. Please use a number between 1 and 8."

        if "query" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        if self.query_count >= self.max_queries:
            raise ValueError(f"exceeded maximum queries ({self.max_queries})")
        
        try:
            query_num = int(parsed_info["query"].strip())
            if query_num not in self.ROUTES:
                return error_invalid
            
            self.query_count += 1
            
            route = self.ROUTES[query_num]
            is_valid = self._is_route_valid(route)
            
            return yes_res if is_valid else no_res
            
        except ValueError:
            return error_invalid

    def _cf_make_wrong(self, correct):
        """生成一个错误的查询响应用于反事实干预"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
        
        if correct == yes_res:
            return no_res
        elif correct == no_res:
            return yes_res
        else:
            return correct

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
        
        for route_num, route in self.ROUTES.items():
            is_valid = self._is_route_valid(route)
            answer = yes_res if is_valid else no_res
            results.append({
                "query": f"<query>{route_num}</query>",
                "answer": answer,
            })
        
        return results