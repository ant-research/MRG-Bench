from .base import Game
import random

class TreeWidthGame(Game):

    game_rule_zh = """\
我们现在来玩一个"树宽度推理"游戏，规则如下：

游戏设定了一棵未知的有根树，其层（深度）d的节点数定义为宽度W(d)。树的结构具有以下特性：

1. **层规整性**：对于每个层d，该层所有节点到下一层的子节点数相同，记为b(d)，b(d)可以是0、1、2或更大的非负整数，但该值对你不可见且在游戏全过程中固定。
2. **递推关系**：第0层（根节点层）的宽度W(0)=1；对于任意层d大于等于0，下一层的宽度W(d+1)=W(d)乘以b(d)。如果某层的b(d)=0，则从d+1层起，所有更深层的宽度W(·)恒为0。
3. **查询范围**：系统已知查询上界H_max={h_max}，你可以查询的深度d范围是0到{h_max}之间的整数。如果d超过树的真实最大深度，系统返回W(d)=0。
4. **查询预算**：你最多可以进行Q={q_max}次查询（包括数值查询和比较查询）。

你的目标是：在不超过查询预算的前提下，找出全局最大宽度所在的层号L*以及该层的宽度W*。如果有多个层的宽度达到最大值，请选择层号最小的那一层。

每次查询会消耗1点预算，你可以使用以下两种查询：

1. **数值查询**：查询指定层d的宽度W(d)。系统会返回一个非负整数。
2. **比较查询**：查询两个层d1和d2的宽度大小关系。系统会返回以下三种关系之一：
   - "小于"（W(d1) < W(d2)）
   - "等于"（W(d1) = W(d2)）
   - "大于"（W(d1) > W(d2)）

你可以重复查询同一个层或同一对层，所有回复都是确定且一致的。

每次查询只能包含一个标签。请使用以下XML格式：

- 数值查询（例如查询第5层）：
<query_value>5</query_value>

- 比较查询（例如比较第3层和第7层）：
<query_compare>3,7</query_compare>

提交最终答案时，必须给出最大宽度所在的层号L*和该层的宽度W*，格式如下：
<answer>layer=5, width=16</answer>

注意：
- 层号和宽度都必须是非负整数。
- 如果答案错误、格式不符或超过查询预算，游戏将失败。
- 请尽可能用最少的查询次数找到答案。
"""

    game_rule_en = """\
Let's play a "Tree Width Inference" game. Here are the rules:

The game has an unknown rooted tree, where the number of nodes at depth d is defined as the width W(d). The tree structure has the following properties:

1. **Layer Regularity**: For each layer d, all nodes in that layer have the same number of children in the next layer, denoted as b(d). b(d) can be 0, 1, 2, or any non-negative integer, but this value is hidden from you and remains fixed throughout the game.
2. **Recurrence Relation**: The width of layer 0 (root layer) is W(0)=1; for any layer d greater than or equal to 0, the width of the next layer is W(d+1)=W(d) multiplied by b(d). If b(d)=0 for some layer, then W(·) remains 0 for all deeper layers from d+1 onwards.
3. **Query Range**: The system has a known query upper bound H_max={h_max}. You can query depths d in the integer range from 0 to {h_max}. If d exceeds the tree's actual maximum depth, the system returns W(d)=0.
4. **Query Budget**: You can make at most Q={q_max} queries (including value queries and comparison queries).

Your goal is: within the query budget, find the layer number L* where the global maximum width occurs and the width W* of that layer. If multiple layers have the maximum width, choose the one with the smallest layer number.

Each query consumes 1 point of your budget. You can use the following two types of queries:

1. **Value Query**: Query the width W(d) of a specified layer d. The system returns a non-negative integer.
2. **Comparison Query**: Query the size relationship between the widths of two layers d1 and d2. The system returns one of the following three relationships:
   - "less than" (W(d1) < W(d2))
   - "equal" (W(d1) = W(d2))
   - "greater than" (W(d1) > W(d2))

You can repeatedly query the same layer or the same pair of layers. All responses are deterministic and consistent.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., querying layer 5):
<query_value>5</query_value>

- Comparison Query (e.g., comparing layer 3 and layer 7):
<query_compare>3,7</query_compare>

When submitting the final answer, you must provide the layer number L* where the maximum width occurs and the width W* of that layer, using this format:
<answer>layer=5, width=16</answer>

Note:
- Both layer number and width must be non-negative integers.
- The game fails if the answer is incorrect, the format is invalid, or the query budget is exceeded.
- Please try to find the answer with the minimum number of queries.
"""

    contextualized_rule_zh_1 = """\
交通路网扩张分析系统已启动。

城市中心定义为第0圈层（仅1个核心路口）。向外扩展的圈层（深度）d的路口总数定义为该圈层的容量W(d)。路网具有以下特性：

1. **圈层规整性**：对于每个圈层d，该层所有路口向下一圈层延伸出的路口数相同，记为b(d)。b(d)可能是0、1、2或更大整数，且对你不可见，但在全过程中固定不变。
2. **递推关系**：第0圈层容量W(0)=1；对于任意圈层d≥0，下一圈层容量W(d+1)=W(d)乘以b(d)。若某圈层b(d)=0，即无路向外延伸，则从d+1圈层起，所有更外围圈层容量W(·)恒为0。
3. **探查范围**：系统已知最大探查上界H_max={h_max}，你可以探查的圈层d范围是0到{h_max}之间的整数。若d超过路网的真实最大圈层，系统返回W(d)=0。
4. **探测预算**：你最多可以进行Q={q_max}次探测（包括数值探测和比较探测）。

你的目标是：在不超过探测预算的前提下，找出路口总数最多（即最容易产生环状拥堵）的圈层号L*以及该圈层的路口总数W*。如果有多个圈层的路口数达到最大值，请选择最靠近市中心（圈层号最小）的那一圈层。

每次探测消耗1点预算，你可以使用以下两种探测：

1. **数值探测**：探查指定圈层d的容量W(d)。系统会返回一个非负整数。
2. **比较探测**：探查两个圈层d1和d2的容量大小关系。系统会返回以下三种关系之一：
   - "小于"（W(d1) < W(d2)）
   - "等于"（W(d1) = W(d2)）
   - "大于"（W(d1) > W(d2)）

你可以重复探测同一圈层或同一对圈层，所有回复都是确定且一致的。

每次探测只能包含一个标签。请使用以下XML格式：

- 数值探测（例如探查第5圈层）：
<query_value>5</query_value>

- 比较探测（例如比较第3圈层和第7圈层）：
<query_compare>3,7</query_compare>

提交最终报告时，必须给出最大容量所在的圈层号L*和该层的容量W*，格式如下（必须保留layer和width字样）：
<answer>layer=5, width=16</answer>

注意：
- 圈层号和容量必须是非负整数。
- 如果报告错误、格式不符或超出探测预算，分析任务将失败。
- 请尽可能用最少的探测次数找出目标圈层。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The traffic network expansion analysis system has been activated.

The city center is defined as layer 0 (with exactly 1 core intersection). The total number of intersections at an expanding layer (depth) d is defined as the capacity W(d). The road network has the following properties:

1. **Layer Regularity**: For each layer d, all intersections in that layer branch out to the same number of intersections in the next layer, denoted as b(d). The value b(d) can be 0, 1, 2, or any non-negative integer. It is hidden from you and remains fixed throughout the process.
2. **Recurrence Relation**: The capacity of layer 0 is W(0)=1; for any layer d ≥ 0, the capacity of the next layer is W(d+1) = W(d) multiplied by b(d). If b(d)=0 for some layer (no outbound roads), then W(·) remains 0 for all deeper layers from d+1 onwards.
3. **Query Range**: The system has a known exploration upper bound H_max={h_max}. You can query depths d in the integer range from 0 to {h_max}. If d exceeds the network's actual maximum depth, the system returns W(d)=0.
4. **Detection Budget**: You can make at most Q={q_max} queries (including value queries and comparison queries).

Your goal is: within the query budget, find the layer number L* with the maximum total number of intersections (the most likely layer for circular congestion) and the capacity W* of that layer. If multiple layers reach the maximum capacity, choose the one closest to the center (the smallest layer number).

Each query consumes 1 point of your budget. You can use the following two types of queries:

1. **Value Query**: Query the capacity W(d) of a specified layer d. The system returns a non-negative integer.
2. **Comparison Query**: Query the size relationship between the capacities of two layers d1 and d2. The system returns one of the following three relationships:
   - "less than" (W(d1) < W(d2))
   - "equal" (W(d1) = W(d2))
   - "greater than" (W(d1) > W(d2))

You can repeatedly query the same layer or the same pair of layers. All responses are deterministic and consistent.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., querying layer 5):
<query_value>5</query_value>

- Comparison Query (e.g., comparing layer 3 and layer 7):
<query_compare>3,7</query_compare>

When submitting the final report, you must provide the layer number L* where the maximum capacity occurs and the capacity W* of that layer, using this format (the keywords 'layer' and 'width' must be kept):
<answer>layer=5, width=16</answer>

Note:
- Both layer number and capacity must be non-negative integers.
- The analysis task fails if the report is incorrect, the format is invalid, or the query budget is exceeded.
- Please try to identify the target layer with the minimum number of queries.
"""

    contextualized_rule_zh_2 = """\
病毒代际传播分析系统已启动。

最初的感染源（零号细胞）定义为第0代。传播代际（深度）d的受感染细胞总数定义为该代的细胞感染量W(d)。病毒的细胞间传播链具有以下特性：

1. **代际规整性**：对于每一代d，该代的所有受感染细胞会感染相同数量的下一代细胞，记为b(d)。b(d)可以是0、1、2或更大的非负整数，该值对你不可见且在分析过程中固定不变。
2. **递推关系**：第0代感染量W(0)=1；对于任意代际d≥0，下一代感染量W(d+1)=W(d)乘以b(d)。如果某代b(d)=0（病毒停止复制），则从d+1代起，所有更深代际的感染量W(·)恒为0。
3. **追踪范围**：系统已知追踪上界H_max={h_max}，你可以追踪的代际d范围是0到{h_max}之间的整数。如果d超过真实的最终传播代际，系统返回W(d)=0。
4. **检测预算**：你最多可以进行Q={q_max}次检测查询（包括数值查询和比较查询）。

你的目标是：在不超过检测预算的前提下，找出细胞感染量达到峰值的代际号L*以及该代的细胞感染量W*。如果有多个代际的感染量达到最大值，请选择最早出现（代际号最小）的那一代。

每次查询消耗1点预算，你可以使用以下两种查询：

1. **数值查询**：查询指定代际d的感染量W(d)。系统会返回一个非负整数。
2. **比较查询**：查询两个代际d1和d2的感染量大小关系。系统会返回以下三种关系之一：
   - "小于"（W(d1) < W(d2)）
   - "等于"（W(d1) = W(d2)）
   - "大于"（W(d1) > W(d2)）

你可以重复查询同一个代际或同一对代际，所有回复都是确定且一致的。

每次查询只能包含一个标签。请使用以下XML格式：

- 数值查询（例如查询第5代）：
<query_value>5</query_value>

- 比较查询（例如比较第3代和第7代）：
<query_compare>3,7</query_compare>

提交最终结果时，必须给出最大感染量所在的代际号L*和该代的感染量W*，格式如下（必须保留layer和width字样）：
<answer>layer=5, width=16</answer>

注意：
- 代际号和感染量都必须是非负整数。
- 如果结果错误、格式不符或超过检测预算，分析将失败。
- 请尽可能用最少的查询次数找到答案。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
The viral generational transmission analysis system has been activated.

The initial infection source (Patient Zero/Cell Zero) is defined as generation 0. The total number of infected cells at transmission generation (depth) d is defined as the infection volume W(d). The cell-to-cell transmission chain has the following properties:

1. **Generational Regularity**: For each generation d, all infected cells in that generation will infect the same number of cells in the next generation, denoted as b(d). b(d) can be 0, 1, 2, or any non-negative integer. This value is hidden from you and remains fixed throughout the analysis.
2. **Recurrence Relation**: The infection volume of generation 0 is W(0)=1; for any generation d ≥ 0, the infection volume of the next generation is W(d+1) = W(d) multiplied by b(d). If b(d)=0 for some generation (virus stops replicating), then W(·) remains 0 for all deeper generations from d+1 onwards.
3. **Tracking Range**: The system has a known tracking upper bound H_max={h_max}. You can track generations d in the integer range from 0 to {h_max}. If d exceeds the actual final transmission generation, the system returns W(d)=0.
4. **Testing Budget**: You can make at most Q={q_max} testing queries (including value queries and comparison queries).

Your goal is: within the testing budget, find the generation number L* where the infection volume reaches its peak and the infection volume W* of that generation. If multiple layers reach the maximum infection volume, choose the earliest one (the smallest generation number).

Each query consumes 1 point of your budget. You can use the following two types of queries:

1. **Value Query**: Query the infection volume W(d) of a specified generation d. The system returns a non-negative integer.
2. **Comparison Query**: Query the size relationship between the infection volumes of two generations d1 and d2. The system returns one of the following three relationships:
   - "less than" (W(d1) < W(d2))
   - "equal" (W(d1) = W(d2))
   - "greater than" (W(d1) > W(d2))

You can repeatedly query the same generation or the same pair of generations. All responses are deterministic and consistent.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., querying generation 5):
<query_value>5</query_value>

- Comparison Query (e.g., comparing generation 3 and generation 7):
<query_compare>3,7</query_compare>

When submitting the final result, you must provide the generation number L* where the maximum infection volume occurs and the volume W* of that generation, using this format (the keywords 'layer' and 'width' must be kept):
<answer>layer=5, width=16</answer>

Note:
- Both generation number and infection volume must be non-negative integers.
- The analysis fails if the result is incorrect, the format is invalid, or the testing budget is exceeded.
- Please try to find the answer with the minimum number of queries.
"""

    contextualized_rule_zh_3 = """\
知识点衍生图谱分析系统已准备就绪。

图谱的起点是一个核心基础概念（定义为第0层）。向下衍生的层级（深度）d的知识点总数定义为该层的衍生规模W(d)。知识图谱具有以下特性：

1. **衍生规整性**：对于每个衍生层级d，该层的所有知识点都会衍生出相同数量的下一级关联知识点，记为b(d)。b(d)可以是0、1、2或更大的非负整数，该值对你不可见且在分析过程中保持固定。
2. **递推关系**：核心概念层W(0)=1；对于任意层级d≥0，下一级的衍生规模W(d+1)=W(d)乘以b(d)。如果某层b(d)=0（知识点不再细分），则从d+1层起，所有更深层级的衍生规模W(·)恒为0。
3. **查阅范围**：教学大纲设定了查阅上界H_max={h_max}，你可以查阅的层级d范围是0到{h_max}之间的整数。如果d超过真实的图谱最大深度，系统返回W(d)=0。
4. **教研预算**：你最多可以进行Q={q_max}次图谱查询（包括数值查询和比较查询）。

你的目标是：在不超过教研预算的前提下，找出衍生知识点数量最多（即需要投入最多教学资源）的层级号L*以及该层的衍生规模W*。如果有多个层级的规模达到最大值，请选择最基础（层级号最小）的那一层。

每次查询消耗1点预算，你可以使用以下两种查询：

1. **数值查询**：查询指定层级d的衍生规模W(d)。系统会返回一个非负整数。
2. **比较查询**：查询两个层级d1和d2的规模大小关系。系统会返回以下三种关系之一：
   - "小于"（W(d1) < W(d2)）
   - "等于"（W(d1) = W(d2)）
   - "大于"（W(d1) > W(d2)）

你可以重复查询同一个层级或同一对层级，所有回复都是确定且一致的。

每次查询只能包含一个标签。请使用以下XML格式：

- 数值查询（例如查询第5层）：
<query_value>5</query_value>

- 比较查询（例如比较第3层和第7层）：
<query_compare>3,7</query_compare>

提交最终结论时，必须给出最大规模所在的层级号L*和该层的规模W*，格式如下（必须保留layer和width字样）：
<answer>layer=5, width=16</answer>

注意：
- 层级号和规模都必须是非负整数。
- 如果结论错误、格式不符或超过教研预算，分析任务将失败。
- 请尽可能用最少的查询次数找到答案。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The knowledge point derivation graph analysis system is ready.

The graph starts with a core foundational concept (defined as layer 0). The total number of knowledge points at a derived layer (depth) d is defined as the derivation scale W(d). The knowledge graph has the following properties:

1. **Derivation Regularity**: For each derivation layer d, all knowledge points in that layer will derive the same number of associated knowledge points in the next layer, denoted as b(d). b(d) can be 0, 1, 2, or any non-negative integer. This value is hidden from you and remains fixed during the analysis.
2. **Recurrence Relation**: The core concept layer W(0)=1; for any layer d ≥ 0, the derivation scale of the next layer is W(d+1) = W(d) multiplied by b(d). If b(d)=0 for some layer (no further subdivision), then W(·) remains 0 for all deeper layers from d+1 onwards.
3. **Reference Range**: The syllabus defines a reference upper bound H_max={h_max}. You can query depths d in the integer range from 0 to {h_max}. If d exceeds the actual maximum depth of the graph, the system returns W(d)=0.
4. **Research Budget**: You can make at most Q={q_max} graph queries (including value queries and comparison queries).

Your goal is: within the research budget, find the layer number L* with the largest number of derived knowledge points (requiring the most teaching resources) and the derivation scale W* of that layer. If multiple layers reach the maximum scale, choose the most foundational one (the smallest layer number).

Each query consumes 1 point of your budget. You can use the following two types of queries:

1. **Value Query**: Query the derivation scale W(d) of a specified layer d. The system returns a non-negative integer.
2. **Comparison Query**: Query the size relationship between the scales of two layers d1 and d2. The system returns one of the following three relationships:
   - "less than" (W(d1) < W(d2))
   - "equal" (W(d1) = W(d2))
   - "greater than" (W(d1) > W(d2))

You can repeatedly query the same layer or the same pair of layers. All responses are deterministic and consistent.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., querying layer 5):
<query_value>5</query_value>

- Comparison Query (e.g., comparing layer 3 and layer 7):
<query_compare>3,7</query_compare>

When submitting the final conclusion, you must provide the layer number L* where the maximum scale occurs and the scale W* of that layer, using this format (the keywords 'layer' and 'width' must be kept):
<answer>layer=5, width=16</answer>

Note:
- Both layer number and scale must be non-negative integers.
- The analysis task fails if the conclusion is incorrect, the format is invalid, or the research budget is exceeded.
- Please try to find the answer with the minimum number of queries.
"""

    contextualized_rule_zh_4 = """\
产品BOM（物料清单）拆解分析系统已启动。

最终交付的成品定义为第0层（仅1个总成）。向下拆解的层级（深度）d的子组件总数定义为该层级的物料规模W(d)。BOM树具有以下特性：

1. **拆解规整性**：对于每个拆解层级d，该层的所有组件都会拆解出相同数量的下一级子物料，记为b(d)。b(d)可以是0、1、2或更大的非负整数，该值对你不可见且在分析全过程中固定不变。
2. **递推关系**：成品层W(0)=1；对于任意层级d≥0，下一级的物料规模W(d+1)=W(d)乘以b(d)。如果某层b(d)=0（即达到不可再分的底层原材料），则从d+1层起，所有更深层级的物料规模W(·)恒为0。
3. **检索范围**：ERP系统设定了检索上界H_max={h_max}，你可以查询的拆解深度d范围是0到{h_max}之间的整数。如果d超过真实的BOM最大深度，系统返回W(d)=0。
4. **查询预算**：你最多可以进行Q={q_max}次系统查询（包括数值查询和比较查询）。

你的目标是：在不超过查询预算的前提下，找出子组件总数最多（即对仓储和分拣压力最大）的拆解层级号L*以及该层的物料规模W*。如果有多个层级的规模达到最大值，请选择最接近总成（层级号最小）的那一层。

每次查询消耗1点预算，你可以使用以下两种查询：

1. **数值查询**：查询指定层级d的物料规模W(d)。系统会返回一个非负整数。
2. **比较查询**：查询两个层级d1和d2的规模大小关系。系统会返回以下三种关系之一：
   - "小于"（W(d1) < W(d2)）
   - "等于"（W(d1) = W(d2)）
   - "大于"（W(d1) > W(d2)）

你可以重复查询同一个层级或同一对层级，所有回复都是确定且一致的。

每次查询只能包含一个标签。请使用以下XML格式：

- 数值查询（例如查询第5层级）：
<query_value>5</query_value>

- 比较查询（例如比较第3层级和第7层级）：
<query_compare>3,7</query_compare>

提交最终结果时，必须给出最大规模所在的拆解层级号L*和该层的物料规模W*，格式如下（必须保留layer和width字样）：
<answer>layer=5, width=16</answer>

注意：
- 层级号和规模都必须是非负整数。
- 如果结果错误、格式不符或超过查询预算，分析将失败。
- 请尽可能用最少的查询次数找出关键层级。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
The product BOM (Bill of Materials) breakdown analysis system has been activated.

The final assembled product is defined as layer 0 (exactly 1 top-level assembly). The total number of sub-components at a broken-down layer (depth) d is defined as the material scale W(d). The BOM tree has the following properties:

1. **Breakdown Regularity**: For each breakdown layer d, all components in that layer will be broken down into the same number of sub-materials in the next layer, denoted as b(d). b(d) can be 0, 1, 2, or any non-negative integer. This value is hidden from you and remains fixed throughout the analysis.
2. **Recurrence Relation**: The top-level assembly layer W(0)=1; for any layer d ≥ 0, the material scale of the next layer is W(d+1) = W(d) multiplied by b(d). If b(d)=0 for some layer (reaching indivisible raw materials), then W(·) remains 0 for all deeper layers from d+1 onwards.
3. **Retrieval Range**: The ERP system sets a retrieval upper bound H_max={h_max}. You can query depths d in the integer range from 0 to {h_max}. If d exceeds the actual maximum BOM depth, the system returns W(d)=0.
4. **Query Budget**: You can make at most Q={q_max} system queries (including value queries and comparison queries).

Your goal is: within the query budget, find the breakdown layer number L* with the maximum total number of sub-components (causing the highest pressure on warehousing and sorting) and the material scale W* of that layer. If multiple layers reach the maximum scale, choose the one closest to the top assembly (the smallest layer number).

Each query consumes 1 point of your budget. You can use the following two types of queries:

1. **Value Query**: Query the material scale W(d) of a specified layer d. The system returns a non-negative integer.
2. **Comparison Query**: Query the size relationship between the scales of two layers d1 and d2. The system returns one of the following three relationships:
   - "less than" (W(d1) < W(d2))
   - "equal" (W(d1) = W(d2))
   - "greater than" (W(d1) > W(d2))

You can repeatedly query the same layer or the same pair of layers. All responses are deterministic and consistent.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., querying layer 5):
<query_value>5</query_value>

- Comparison Query (e.g., comparing layer 3 and layer 7):
<query_compare>3,7</query_compare>

When submitting the final result, you must provide the layer number L* where the maximum scale occurs and the scale W* of that layer, using this format (the keywords 'layer' and 'width' must be kept):
<answer>layer=5, width=16</answer>

Note:
- Both layer number and scale must be non-negative integers.
- The analysis fails if the result is incorrect, the format is invalid, or the query budget is exceeded.
- Please try to identify the critical layer with the minimum number of queries.
"""

    contextualized_rule_zh_5 = """\
法典引用溯源分析系统已上线。

一部核心的基本法/宪法定义为第0层。向下衍生的引用层级（深度）d的法规/条款总数定义为该层的条款规模W(d)。引用网络具有以下特性：

1. **引用规整性**：对于每个引用层级d，该层的所有法规都会被相同数量的下一级具体细则所引用或细化，记为b(d)。b(d)可以是0、1、2或更大的非负整数，该值对你不可见且在整个溯源过程中固定不变。
2. **递推关系**：基本法层W(0)=1；对于任意层级d≥0，下一级的条款规模W(d+1)=W(d)乘以b(d)。如果某层b(d)=0（法规已是最底层细则，不再被引用），则从d+1层起，所有更深层级的条款规模W(·)恒为0。
3. **检索范围**：法律数据库设定了检索上界H_max={h_max}，你可以查询的层级d范围是0到{h_max}之间的整数。如果d超过真实的引用最大深度，系统返回W(d)=0。
4. **检索预算**：你最多可以进行Q={q_max}次数据库查询（包括数值查询和比较查询）。

你的目标是：在不超过检索预算的前提下，找出条款总数最多（即法律体系中最庞大复杂的部分）的引用层级号L*以及该层的条款规模W*。如果有多个层级的规模达到最大值，请选择最靠近基本法（层级号最小）的那一层。

每次查询消耗1点预算，你可以使用以下两种查询：

1. **数值查询**：查询指定层级d的条款规模W(d)。系统会返回一个非负整数。
2. **比较查询**：查询两个层级d1和d2的规模大小关系。系统会返回以下三种关系之一：
   - "小于"（W(d1) < W(d2)）
   - "等于"（W(d1) = W(d2)）
   - "大于"（W(d1) > W(d2)）

你可以重复查询同一个层级或同一对层级，所有回复都是确定且一致的。

每次查询只能包含一个标签。请使用以下XML格式：

- 数值查询（例如查询第5层级）：
<query_value>5</query_value>

- 比较查询（例如比较第3层级和第7层级）：
<query_compare>3,7</query_compare>

提交最终判定时，必须给出最大规模所在的层级号L*和该层的条款规模W*，格式如下（必须保留layer和width字样）：
<answer>layer=5, width=16</answer>

注意：
- 层级号和规模都必须是非负整数。
- 如果判定错误、格式不符或超过检索预算，分析将失败。
- 请尽可能用最少的查询次数得出判定。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
The legal code citation traceability analysis system is now online.

A core Basic Law/Constitution is defined as layer 0. The total number of regulations/clauses at a derived citation layer (depth) d is defined as the clause scale W(d). The citation network has the following properties:

1. **Citation Regularity**: For each citation layer d, all regulations in that layer will be cited or detailed by the same number of specific rules in the next layer, denoted as b(d). b(d) can be 0, 1, 2, or any non-negative integer. This value is hidden from you and remains fixed throughout the traceability process.
2. **Recurrence Relation**: The Basic Law layer W(0)=1; for any layer d ≥ 0, the clause scale of the next layer is W(d+1) = W(d) multiplied by b(d). If b(d)=0 for some layer (the regulation is at the lowest level of detail and is no longer cited), then W(·) remains 0 for all deeper layers from d+1 onwards.
3. **Retrieval Range**: The legal database sets a retrieval upper bound H_max={h_max}. You can query depths d in the integer range from 0 to {h_max}. If d exceeds the actual maximum citation depth, the system returns W(d)=0.
4. **Retrieval Budget**: You can make at most Q={q_max} database queries (including value queries and comparison queries).

Your goal is: within the retrieval budget, find the citation layer number L* with the maximum total number of clauses (the largest and most complex part of the legal system) and the clause scale W* of that layer. If multiple layers reach the maximum scale, choose the one closest to the Basic Law (the smallest layer number).

Each query consumes 1 point of your budget. You can use the following two types of queries:

1. **Value Query**: Query the clause scale W(d) of a specified layer d. The system returns a non-negative integer.
2. **Comparison Query**: Query the size relationship between the scales of two layers d1 and d2. The system returns one of the following three relationships:
   - "less than" (W(d1) < W(d2))
   - "equal" (W(d1) = W(d2))
   - "greater than" (W(d1) > W(d2))

You can repeatedly query the same layer or the same pair of layers. All responses are deterministic and consistent.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., querying layer 5):
<query_value>5</query_value>

- Comparison Query (e.g., comparing layer 3 and layer 7):
<query_compare>3,7</query_compare>

When submitting the final judgment, you must provide the layer number L* where the maximum scale occurs and the scale W* of that layer, using this format (the keywords 'layer' and 'width' must be kept):
<answer>layer=5, width=16</answer>

Note:
- Both layer number and scale must be non-negative integers.
- The analysis fails if the judgment is incorrect, the format is invalid, or the retrieval budget is exceeded.
- Please try to reach the judgment with the minimum number of queries.
"""

    tags = ["answer", "query_value", "query_compare"]

    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "h_max": 10,
                "q_max": 8,
                "b_sequence": [2, 2, 2, 1, 1, 0],
                "description": "常数分支2，然后降为1，最后为0"
            },
            2: {
                "h_max": 15,
                "q_max": 10,
                "b_sequence": [3, 3, 3, 3, 0],
                "description": "常数分支3持续4层"
            },
            3: {
                "h_max": 20,
                "q_max": 12,
                "b_sequence": [2, 3, 3, 2, 1, 1, 0],
                "description": "分支因子从2到3再到2再到1"
            },
            4: {
                "h_max": 25,
                "q_max": 15,
                "b_sequence": [2, 2, 3, 3, 2, 1, 1, 1, 0],
                "description": "变化的分支因子，峰值在中间"
            },
            5: {
                "h_max": 30,
                "q_max": 18,
                "b_sequence": [3, 2, 4, 2, 3, 1, 2, 1, 1, 0],
                "description": "复杂的分支因子模式"
            },
        },
        "en": {
            1: {
                "h_max": 10,
                "q_max": 8,
                "b_sequence": [2, 2, 2, 1, 1, 0],
                "description": "Constant branch 2, then decrease to 1, then 0"
            },
            2: {
                "h_max": 15,
                "q_max": 10,
                "b_sequence": [3, 3, 3, 3, 0],
                "description": "Constant branch 3 for 4 layers"
            },
            3: {
                "h_max": 20,
                "q_max": 12,
                "b_sequence": [2, 3, 3, 2, 1, 1, 0],
                "description": "Branch factor from 2 to 3 to 2 to 1"
            },
            4: {
                "h_max": 25,
                "q_max": 15,
                "b_sequence": [2, 2, 3, 3, 2, 1, 1, 1, 0],
                "description": "Varying branch factor, peak in the middle"
            },
            5: {
                "h_max": 30,
                "q_max": 18,
                "b_sequence": [3, 2, 4, 2, 3, 1, 2, 1, 1, 0],
                "description": "Complex branch factor pattern"
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
        self._game_info["h_max"] = cfg["h_max"]
        self._game_info["q_max"] = cfg["q_max"]
        
        self.b_sequence = cfg["b_sequence"]
        self.h_max = cfg["h_max"]
        self.q_max = cfg["q_max"]
        
        self.width_sequence = [1]
        current_width = 1
        for b in self.b_sequence:
            current_width = current_width * b
            self.width_sequence.append(current_width)
            if current_width == 0:
                break
        
        while len(self.width_sequence) <= self.h_max:
            self.width_sequence.append(0)
        
        max_width = max(self.width_sequence[:self.h_max + 1])
        for i in range(self.h_max + 1):
            if self.width_sequence[i] == max_width:
                self.answer_layer = i
                self.answer_width = max_width
                break
        
        self.query_count = 0

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "layer" not in ans_dict or "width" not in ans_dict:
            return False
        
        try:
            model_layer = int(ans_dict["layer"])
            model_width = int(ans_dict["width"])
        except:
            return False
        
        return model_layer == self.answer_layer and model_width == self.answer_width

    def _cf_core_produce(self, parsed_info):
        if self.query_count >= self.q_max:
            if self.config.language == "zh":
                raise ValueError(f"查询次数已超过预算{self.q_max}次")
            else:
                raise ValueError(f"Query count exceeded budget of {self.q_max}")
        
        if self.config.language == "zh":
            less_than, equal, greater_than = "小于", "等于", "大于"
            error_range = "错误：层号超出查询范围。"
            error_format = "错误：格式无效或层号错误。"
        else:
            less_than, equal, greater_than = "less than", "equal", "greater than"
            error_range = "Error: Layer number out of query range."
            error_format = "Error: Invalid format or layer number."
        
        if "query_value" in parsed_info:
            try:
                d = int(parsed_info["query_value"].strip())
                if d < 0 or d > self.h_max:
                    return error_range
                self.query_count += 1
                return str(self.width_sequence[d])
            except:
                return error_format
        
        elif "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                d1, d2 = int(parts[0]), int(parts[1])
                if d1 < 0 or d1 > self.h_max or d2 < 0 or d2 > self.h_max:
                    return error_range
                
                w1 = self.width_sequence[d1]
                w2 = self.width_sequence[d2]
                
                self.query_count += 1
                if w1 < w2:
                    return less_than
                elif w1 == w2:
                    return equal
                else:
                    return greater_than
            except:
                return error_format
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.startswith("错误") or correct.startswith("Error"):
            return correct

        if self.config.language == "zh":
            compare_cycle = {"小于": "大于", "大于": "等于", "等于": "小于"}
        else:
            compare_cycle = {"less than": "greater than", "greater than": "equal", "equal": "less than"}
        
        if correct in compare_cycle:
            return compare_cycle[correct]
        
        try:
            val = int(correct)
            return str(val + 1)
        except ValueError:
            pass
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        if self.config.language == "zh":
            less_str, equal_str, greater_str = "小于", "等于", "大于"
        else:
            less_str, equal_str, greater_str = "less than", "equal", "greater than"

        for d in range(self.h_max + 1):
            ans = str(self.width_sequence[d])
            queries.append({
                "query": f"<query_value>{d}</query_value>",
                "answer": ans
            })

        for d1 in range(self.h_max + 1):
            for d2 in range(d1 + 1, self.h_max + 1):
                w1 = self.width_sequence[d1]
                w2 = self.width_sequence[d2]
                
                if w1 < w2:
                    ans = less_str
                elif w1 == w2:
                    ans = equal_str
                else:
                    ans = greater_str
                
                queries.append({
                    "query": f"<query_compare>{d1},{d2}</query_compare>",
                    "answer": ans
                })
                
        return queries