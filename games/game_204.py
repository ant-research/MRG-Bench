from .base import Game
import random

class SequenceFrequencyGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "序列"

    game_rule_zh = """\
我们来玩一个"序列频次推理"游戏，规则如下：

游戏设定了一个长度为 N = {n} 的有序序列 x1, x2, ..., xN，每个元素取自集合 {{A, B, C}} 中的某一个符号。

你的目标是确定指定符号 τ = "{tau}" 在整个序列中出现的总次数。

你可以向我发起查询来获取信息，每次查询只能选择以下三种类型之一：

1. **单点查询**：询问位置 i 处的元素值是什么（返回 A、B 或 C）。
2. **短段计数查询**：询问从位置 i 开始、长度为 L 的连续区间内，符号 s 出现的次数（返回一个非负整数）。
3. **同值判定查询**：询问位置 i 和位置 j 的元素是否相同（返回"是"或"否"）。

注意：
- 位置索引范围为 1 到 {n}。
- 短段计数查询中，长度 L 必须大于等于 1 且小于等于 10，并且区间不能超出序列范围。
- 你需要在尽可能少的查询次数内推断出答案。

每次查询只能包含一个标签，使用以下 XML 格式：

- 单点查询（例如询问位置 5）：
<query_value>5</query_value>

- 短段计数查询（例如询问从位置 3 开始、长度 4 的区间内符号 A 的出现次数）：
<query_count>i=3, L=4, s=A</query_count>

- 同值判定查询（例如询问位置 2 和位置 7 是否相同）：
<query_equal>2,7</query_equal>

提交最终答案时，必须给出符号 τ = "{tau}" 在序列中的总出现次数，格式如下：
<answer>T=5</answer>

其中 T 为你推断出的出现次数（整数）。
"""

    game_rule_en = """\
Let's play a "Sequence Frequency Inference" game. Here are the rules:

There is an ordered sequence x1, x2, ..., xN of length N = {n}, where each element is one of the symbols from the set {{A, B, C}}.

Your goal is to determine the total number of occurrences of the specified symbol τ = "{tau}" in the entire sequence.

You can make queries to obtain information. Each query must be one of the following three types:

1. **Value Query**: Ask for the value of the element at position i (returns A, B, or C).
2. **Segment Count Query**: Ask for the number of occurrences of symbol s in a consecutive interval starting at position i with length L (returns a non-negative integer).
3. **Equality Query**: Ask whether the elements at positions i and j are the same (returns "Yes" or "No").

Note:
- Position indices range from 1 to {n}.
- In segment count queries, length L must be greater than or equal to 1 and less than or equal to 10, and the interval must not exceed the sequence range.
- You should infer the answer using as few queries as possible.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking about position 5):
<query_value>5</query_value>

- Segment Count Query (e.g., asking for count of symbol A in interval starting at position 3 with length 4):
<query_count>i=3, L=4, s=A</query_count>

- Equality Query (e.g., asking if positions 2 and 7 are equal):
<query_equal>2,7</query_equal>

When submitting the final answer, you must provide the total count of symbol τ = "{tau}" in the sequence, using this format:
<answer>T=5</answer>

where T is the count you inferred (an integer).
"""

    contextualized_rule_zh_1 = """\
我们来玩一个"交通流量频次推理"游戏，规则如下：

智能交通监控系统记录了一段包含 N = {n} 个连续车辆通行记录的序列 x1, x2, ..., xN。每辆车被分类为集合 {{A, B, C}} 中的一种（A: 小型车, B: 大型客车, C: 货运卡车）。

你的目标是确定指定车辆类型 τ = "{tau}" 在该时段内出现的总次数。

你可以向系统发起查询来获取信息，每次查询只能选择以下三种类型之一：

1. **单点查询**：询问位置 i 处的车辆类型是什么（返回 A、B 或 C）。
2. **短段计数查询**：询问从位置 i 开始、长度为 L 的连续区间内，车辆类型 s 出现的次数（返回一个非负整数）。
3. **同值判定查询**：询问位置 i 和位置 j 的车辆类型是否相同（返回"是"或"否"）。

注意：
- 位置索引范围为 1 到 {n}。
- 短段计数查询中，长度 L 必须大于等于 1 且小于等于 10，并且区间不能超出记录范围。
- 你需要在尽可能少的查询次数内推断出答案。

每次查询只能包含一个标签，使用以下 XML 格式：

- 单点查询（例如询问位置 5）：
<query_value>5</query_value>

- 短段计数查询（例如询问从位置 3 开始、长度 4 的区间内车辆类型 A 的出现次数）：
<query_count>i=3, L=4, s=A</query_count>

- 同值判定查询（例如询问位置 2 和位置 7 是否相同）：
<query_equal>2,7</query_equal>

提交最终答案时，必须给出车辆类型 τ = "{tau}" 在序列中的总出现次数，格式如下：
<answer>T=5</answer>

其中 T 为你推断出的出现次数（整数）。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play a "Traffic Flow Frequency Inference" game. Here are the rules:

The intelligent traffic monitoring system has recorded a sequence of N = {n} consecutive vehicle passes x1, x2, ..., xN. Each vehicle is categorized into one of the types from the set {{A, B, C}} (A: Car, B: Bus, C: Truck).

Your goal is to determine the total number of occurrences of the specified vehicle type τ = "{tau}" during this period.

You can make queries to obtain information. Each query must be one of the following three types:

1. **Value Query**: Ask for the vehicle type at position i (returns A, B, or C).
2. **Segment Count Query**: Ask for the number of occurrences of vehicle type s in a consecutive interval starting at position i with length L (returns a non-negative integer).
3. **Equality Query**: Ask whether the vehicle types at positions i and j are the same (returns "Yes" or "No").

Note:
- Position indices range from 1 to {n}.
- In segment count queries, length L must be greater than or equal to 1 and less than or equal to 10, and the interval must not exceed the sequence range.
- You should infer the answer using as few queries as possible.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking about position 5):
<query_value>5</query_value>

- Segment Count Query (e.g., asking for count of type A in interval starting at position 3 with length 4):
<query_count>i=3, L=4, s=A</query_count>

- Equality Query (e.g., asking if positions 2 and 7 are equal):
<query_equal>2,7</query_equal>

When submitting the final answer, you must provide the total count of vehicle type τ = "{tau}" in the sequence, using this format:
<answer>T=5</answer>

where T is the count you inferred (an integer).
"""

    contextualized_rule_zh_2 = """\
我们来玩一个"临床基因序列频次推理"游戏，规则如下：

临床基因测序系统输出了一段长度为 N = {n} 的基因突变标记序列 x1, x2, ..., xN。每个位点的标记属于集合 {{A, B, C}} 中的一种（A: 稳定变异, B: 临界变异, C: 高危变异）。

你的目标是确定指定突变标记 τ = "{tau}" 在整个测序片段中出现的总次数。

你可以向系统发起查询来获取信息，每次查询只能选择以下三种类型之一：

1. **单点查询**：询问位置 i 处的突变标记是什么（返回 A、B 或 C）。
2. **短段计数查询**：询问从位置 i 开始、长度为 L 的连续区间内，突变标记 s 出现的次数（返回一个非负整数）。
3. **同值判定查询**：询问位置 i 和位置 j 的突变标记是否相同（返回"是"或"否"）。

注意：
- 位置索引范围为 1 到 {n}。
- 短段计数查询中，长度 L 必须大于等于 1 且小于等于 10，并且区间不能超出测序片段范围。
- 你需要在尽可能少的查询次数内推断出答案。

每次查询只能包含一个标签，使用以下 XML 格式：

- 单点查询（例如询问位置 5）：
<query_value>5</query_value>

- 短段计数查询（例如询问从位置 3 开始、长度 4 的区间内标记 A 的出现次数）：
<query_count>i=3, L=4, s=A</query_count>

- 同值判定查询（例如询问位置 2 和位置 7 是否相同）：
<query_equal>2,7</query_equal>

提交最终答案时，必须给出突变标记 τ = "{tau}" 在序列中的总出现次数，格式如下：
<answer>T=5</answer>

其中 T 为你推断出的出现次数（整数）。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Clinical Gene Sequence Frequency Inference" game. Here are the rules:

The clinical gene sequencing system has output a sequence of length N = {n} containing mutation markers x1, x2, ..., xN. Each marker belongs to one of the categories from the set {{A, B, C}} (A: Stable, B: Borderline, C: High-Risk).

Your goal is to determine the total number of occurrences of the specified mutation marker τ = "{tau}" across the entire sequence.

You can make queries to obtain information. Each query must be one of the following three types:

1. **Value Query**: Ask for the mutation marker at position i (returns A, B, or C).
2. **Segment Count Query**: Ask for the number of occurrences of marker s in a consecutive interval starting at position i with length L (returns a non-negative integer).
3. **Equality Query**: Ask whether the mutation markers at positions i and j are the same (returns "Yes" or "No").

Note:
- Position indices range from 1 to {n}.
- In segment count queries, length L must be greater than or equal to 1 and less than or equal to 10, and the interval must not exceed the sequence range.
- You should infer the answer using as few queries as possible.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking about position 5):
<query_value>5</query_value>

- Segment Count Query (e.g., asking for count of marker A in interval starting at position 3 with length 4):
<query_count>i=3, L=4, s=A</query_count>

- Equality Query (e.g., asking if positions 2 and 7 are equal):
<query_equal>2,7</query_equal>

When submitting the final answer, you must provide the total count of mutation marker τ = "{tau}" in the sequence, using this format:
<answer>T=5</answer>

where T is the count you inferred (an integer).
"""

    contextualized_rule_zh_3 = """\
我们来玩一个"标准化考试作答频次推理"游戏，规则如下：

标准化考试阅卷系统收集了一份包含 N = {n} 道单选题的答卷序列 x1, x2, ..., xN。每道题的作答选项均取自集合 {{A, B, C}} 中的某一个。

作为教学行为分析员，你的目标是确定学生选择指定选项 τ = "{tau}" 的总次数。

你可以向系统发起查询来获取作答信息，每次查询只能选择以下三种类型之一：

1. **单点查询**：询问第 i 题的作答选项是什么（返回 A、B 或 C）。
2. **短段计数查询**：询问从第 i 题开始、连续 L 道题的区间内，选项 s 被选择的次数（返回一个非负整数）。
3. **同值判定查询**：询问第 i 题和第 j 题的作答选项是否相同（返回"是"或"否"）。

注意：
- 题号索引范围为 1 到 {n}。
- 短段计数查询中，长度 L 必须大于等于 1 且小于等于 10，并且区间不能超出答卷范围。
- 你需要在尽可能少的查询次数内推断出答案。

每次查询只能包含一个标签，使用以下 XML 格式：

- 单点查询（例如询问第 5 题）：
<query_value>5</query_value>

- 短段计数查询（例如询问从第 3 题开始、连续 4 题内选项 A 的选择次数）：
<query_count>i=3, L=4, s=A</query_count>

- 同值判定查询（例如询问第 2 题和第 7 题是否相同）：
<query_equal>2,7</query_equal>

提交最终答案时，必须给出作答选项 τ = "{tau}" 在整份答卷中的总选择次数，格式如下：
<answer>T=5</answer>

其中 T 为你推断出的次数（整数）。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Standardized Test Answer Frequency Inference" game. Here are the rules:

The standardized test grading system has collected a sequence of answers for a multiple-choice test with N = {n} questions x1, x2, ..., xN. Each answer is selected from the set {{A, B, C}}.

As an educational behavior analyst, your goal is to determine the total number of times the student selected the specified option τ = "{tau}".

You can make queries to obtain information. Each query must be one of the following three types:

1. **Value Query**: Ask for the answer selected for question i (returns A, B, or C).
2. **Segment Count Query**: Ask for the number of times option s was selected in a consecutive interval starting at question i with length L (returns a non-negative integer).
3. **Equality Query**: Ask whether the answers for questions i and j are the same (returns "Yes" or "No").

Note:
- Question indices range from 1 to {n}.
- In segment count queries, length L must be greater than or equal to 1 and less than or equal to 10, and the interval must not exceed the test range.
- You should infer the answer using as few queries as possible.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking about question 5):
<query_value>5</query_value>

- Segment Count Query (e.g., asking for count of option A in interval starting at question 3 with length 4):
<query_count>i=3, L=4, s=A</query_count>

- Equality Query (e.g., asking if questions 2 and 7 are equal):
<query_equal>2,7</query_equal>

When submitting the final answer, you must provide the total count of option τ = "{tau}" selected in the test, using this format:
<answer>T=5</answer>

where T is the count you inferred (an integer).
"""

    contextualized_rule_zh_4 = """\
我们来玩一个"流水线质量评级频次推理"游戏，规则如下：

工业流水线的自动化质检系统记录了一批长度为 N = {n} 的产品质量评级序列 x1, x2, ..., xN。每个产品被评定为集合 {{A, B, C}} 中的一种等级（A: 优良, B: 合格, C: 瑕疵）。

你的目标是确定特定质量评级 τ = "{tau}" 的产品在这批记录中的总数量。

你可以向质检数据库发起查询来获取信息，每次查询只能选择以下三种类型之一：

1. **单点查询**：询问位置 i 处的产品的质量评级是什么（返回 A、B 或 C）。
2. **短段计数查询**：询问从位置 i 开始、长度为 L 的连续抽检批次内，评级 s 出现的次数（返回一个非负整数）。
3. **同值判定查询**：询问位置 i 和位置 j 的产品质量评级是否相同（返回"是"或"否"）。

注意：
- 产品位置索引范围为 1 到 {n}。
- 短段计数查询中，长度 L 必须大于等于 1 且小于等于 10，并且区间不能超出抽检批次范围。
- 你需要在尽可能少的查询次数内推断出答案。

每次查询只能包含一个标签，使用以下 XML 格式：

- 单点查询（例如询问位置 5）：
<query_value>5</query_value>

- 短段计数查询（例如询问从位置 3 开始、连续 4 个产品内评级 A 的出现次数）：
<query_count>i=3, L=4, s=A</query_count>

- 同值判定查询（例如询问位置 2 和位置 7 是否相同）：
<query_equal>2,7</query_equal>

提交最终答案时，必须给出质量评级 τ = "{tau}" 在全序列中的总出现次数，格式如下：
<answer>T=5</answer>

其中 T 为你推断出的出现次数（整数）。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's play an "Assembly Line Quality Rating Frequency Inference" game. Here are the rules:

The automated quality inspection system on the assembly line has recorded a sequence of quality ratings for N = {n} products x1, x2, ..., xN. Each product is graded into one of the categories from the set {{A, B, C}} (A: Excellent, B: Acceptable, C: Defective).

Your goal is to determine the total number of products with the specified quality rating τ = "{tau}" in this batch.

You can make queries to the inspection database to obtain information. Each query must be one of the following three types:

1. **Value Query**: Ask for the quality rating of the product at position i (returns A, B, or C).
2. **Segment Count Query**: Ask for the number of occurrences of rating s in a consecutive inspection interval starting at position i with length L (returns a non-negative integer).
3. **Equality Query**: Ask whether the quality ratings of the products at positions i and j are the same (returns "Yes" or "No").

Note:
- Product position indices range from 1 to {n}.
- In segment count queries, length L must be greater than or equal to 1 and less than or equal to 10, and the interval must not exceed the batch range.
- You should infer the answer using as few queries as possible.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking about position 5):
<query_value>5</query_value>

- Segment Count Query (e.g., asking for count of rating A in an interval starting at position 3 with length 4):
<query_count>i=3, L=4, s=A</query_count>

- Equality Query (e.g., asking if positions 2 and 7 are equal):
<query_equal>2,7</query_equal>

When submitting the final answer, you must provide the total count of quality rating τ = "{tau}" in the batch, using this format:
<answer>T=5</answer>

where T is the count you inferred (an integer).
"""

    contextualized_rule_zh_5 = """\
我们来玩一个"司法卷宗分类频次推理"游戏，规则如下：

司法档案数字化系统整理了一组包含 N = {n} 份连续编号的历史卷宗序列 x1, x2, ..., xN。每份卷宗的案件性质被标记为集合 {{A, B, C}} 中的一种（A: 民事案件, B: 刑事案件, C: 行政案件）。

你的任务是清点特定案件性质 τ = "{tau}" 在这批卷宗中的总数量。

你可以向归档系统发起查询来提取信息，每次查询只能选择以下三种类型之一：

1. **单点查询**：询问编号 i 处的卷宗案件性质是什么（返回 A、B 或 C）。
2. **短段计数查询**：询问从编号 i 开始、长度为 L 的连续调卷区间内，性质为 s 的案件数量（返回一个非负整数）。
3. **同值判定查询**：询问编号 i 和编号 j 的案件性质是否相同（返回"是"或"否"）。

注意：
- 卷宗编号索引范围为 1 到 {n}。
- 短段计数查询中，调卷长度 L 必须大于等于 1 且小于等于 10，并且区间不能超出归档序列范围。
- 你需要在尽可能少的查询次数内推断出答案。

每次查询只能包含一个标签，使用以下 XML 格式：

- 单点查询（例如询问编号 5）：
<query_value>5</query_value>

- 短段计数查询（例如询问从编号 3 开始、连续 4 份卷宗内性质 A 的案件数量）：
<query_count>i=3, L=4, s=A</query_count>

- 同值判定查询（例如询问编号 2 和编号 7 是否相同）：
<query_equal>2,7</query_equal>

提交最终答案时，必须给出案件性质 τ = "{tau}" 的卷宗总数，格式如下：
<answer>T=5</answer>

其中 T 为你推断出的卷宗数量（整数）。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "Judicial Archive Categorization Frequency Inference" game. Here are the rules:

The judicial archive digitization system has compiled a sequence of N = {n} consecutively numbered historical case files x1, x2, ..., xN. Each case file is categorized into one of the types from the set {{A, B, C}} (A: Civil Case, B: Criminal Case, C: Administrative Case).

Your task is to determine the total number of case files with the specified case type τ = "{tau}" in this compiled sequence.

You can make queries to the archiving system to extract information. Each query must be one of the following three types:

1. **Value Query**: Ask for the case type of the file at position i (returns A, B, or C).
2. **Segment Count Query**: Ask for the number of files of type s in a consecutive retrieval interval starting at position i with length L (returns a non-negative integer).
3. **Equality Query**: Ask whether the case types of the files at positions i and j are the same (returns "Yes" or "No").

Note:
- Case file position indices range from 1 to {n}.
- In segment count queries, the retrieval length L must be greater than or equal to 1 and less than or equal to 10, and the interval must not exceed the sequence range.
- You should infer the answer using as few queries as possible.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking about position 5):
<query_value>5</query_value>

- Segment Count Query (e.g., asking for count of type A in an interval starting at position 3 with length 4):
<query_count>i=3, L=4, s=A</query_count>

- Equality Query (e.g., asking if positions 2 and 7 are equal):
<query_equal>2,7</query_equal>

When submitting the final answer, you must provide the total count of case type τ = "{tau}" in the archive, using this format:
<answer>T=5</answer>

where T is the count you inferred (an integer).
"""

    tags = ["answer", "query_value", "query_count", "query_equal"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 20,
                "tau": "A",
                "f_map": {0: "A", 1: "A", 2: "B", 3: "A", 4: "C", 5: "A", 6: "B", 7: "A", 8: "C", 9: "A"},
            },
            2: {
                "n": 50,
                "tau": "B",
                "f_map": {0: "A", 1: "B", 2: "C", 3: "A", 4: "B", 5: "C", 6: "A", 7: "B", 8: "C", 9: "A"},
            },
            3: {
                "n": 80,
                "tau": "C",
                "f_map": {0: "A", 1: "B", 2: "A", 3: "B", 4: "C", 5: "A", 6: "B", 7: "A", 8: "C", 9: "B"},
            },
            4: {
                "n": 120,
                "tau": "A",
                "f_map": {0: "B", 1: "C", 2: "B", 3: "A", 4: "C", 5: "B", 6: "C", 7: "A", 8: "B", 9: "C"},
            },
            5: {
                "n": 200,
                "tau": "B",
                "f_map": {0: "A", 1: "C", 2: "A", 3: "C", 4: "B", 5: "A", 6: "C", 7: "A", 8: "C", 9: "A"},
            },
        },
        "en": {
            1: {
                "n": 20,
                "tau": "A",
                "f_map": {0: "A", 1: "A", 2: "B", 3: "A", 4: "C", 5: "A", 6: "B", 7: "A", 8: "C", 9: "A"},
            },
            2: {
                "n": 50,
                "tau": "B",
                "f_map": {0: "A", 1: "B", 2: "C", 3: "A", 4: "B", 5: "C", 6: "A", 7: "B", 8: "C", 9: "A"},
            },
            3: {
                "n": 80,
                "tau": "C",
                "f_map": {0: "A", 1: "B", 2: "A", 3: "B", 4: "C", 5: "A", 6: "B", 7: "A", 8: "C", 9: "B"},
            },
            4: {
                "n": 120,
                "tau": "A",
                "f_map": {0: "B", 1: "C", 2: "B", 3: "A", 4: "C", 5: "B", 6: "C", 7: "A", 8: "B", 9: "C"},
            },
            5: {
                "n": 200,
                "tau": "B",
                "f_map": {0: "A", 1: "C", 2: "A", 3: "C", 4: "B", 5: "A", 6: "C", 7: "A", 8: "C", 9: "A"},
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
        self._game_info["tau"] = cfg["tau"]
        
        self.f_map = cfg["f_map"]
        self.n = cfg["n"]
        self.tau = cfg["tau"]
        
        self.sequence = {}
        for i in range(1, self.n + 1):
            mod_val = (i - 1) % 10
            self.sequence[i] = self.f_map[mod_val]
        
        self.correct_count = sum(1 for v in self.sequence.values() if v == self.tau)

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        try:
            if "=" not in raw_ans:
                return False
            parts = raw_ans.strip().split("=")
            if len(parts) != 2 or parts[0].strip().upper() != "T":
                return False
            
            submitted_count = int(parts[1].strip())
            return submitted_count == self.correct_count
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_range = "错误：位置超出范围。"
            error_format = "错误：查询格式无效。"
            error_length = "错误：区间长度必须在1到10之间。"
            error_interval = "错误：查询区间超出序列范围。"
        else:
            yes_res, no_res = "Yes", "No"
            error_range = "Error: Position out of range."
            error_format = "Error: Invalid query format."
            error_length = "Error: Interval length must be between 1 and 10."
            error_interval = "Error: Query interval exceeds sequence range."

        if "query_value" in parsed_info:
            try:
                i = int(parsed_info["query_value"].strip())
                if i < 1 or i > self.n:
                    return error_range
                return self.sequence[i]
            except:
                return error_format

        elif "query_count" in parsed_info:
            try:
                raw = parsed_info["query_count"]
                params = {}
                for part in raw.split(","):
                    if "=" not in part:
                        continue
                    key, val = part.split("=", 1)
                    params[key.strip().lower()] = val.strip()
                
                if "i" not in params or "l" not in params or "s" not in params:
                    return error_format
                
                i = int(params["i"])
                L = int(params["l"])
                s = params["s"].upper()
                
                if L < 1 or L > 10:
                    return error_length
                if i < 1 or i > self.n or i + L - 1 > self.n:
                    return error_interval
                if s not in ["A", "B", "C"]:
                    return error_format
                
                count = 0
                for pos in range(i, i + L):
                    if self.sequence[pos] == s:
                        count += 1
                
                return str(count)
            except:
                return error_format

        elif "query_equal" in parsed_info:
            try:
                raw = parsed_info["query_equal"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                
                i = int(parts[0])
                j = int(parts[1])
                
                if i < 1 or i > self.n or j < 1 or j > self.n:
                    return error_range
                
                return yes_res if self.sequence[i] == self.sequence[j] else no_res
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct in ("A", "B", "C"):
            alternatives = [x for x in ("A", "B", "C") if x != correct]
            return alternatives[0]
        
        try:
            val = int(correct)
            return str(val + 1)
        except ValueError:
            pass
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
            
        if correct.lower() == "yes":
            return "No"
        if correct.lower() == "no":
            return "Yes"
            
        return f"{correct}_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        for i in range(1, self.n + 1):
            query_str = f"<query_value>{i}</query_value>"
            answer_str = self.sequence[i]
            queries.append({"query": query_str, "answer": answer_str})
            
        for L in range(1, 11):
            max_i = self.n - L + 1
            for i in range(1, max_i + 1):
                for s in ["A", "B", "C"]:
                    query_str = f"<query_count>i={i}, L={L}, s={s}</query_count>"
                    
                    count = 0
                    for pos in range(i, i + L):
                        if self.sequence[pos] == s:
                            count += 1
                    answer_str = str(count)
                    
                    queries.append({"query": query_str, "answer": answer_str})
                    
        MAX_EQUALITY_QUERIES = 500
        equality_pairs = []
        for i in range(1, self.n):
            for j in range(i + 1, self.n + 1):
                equality_pairs.append((i, j))
        
        if len(equality_pairs) > MAX_EQUALITY_QUERIES:
            rng = random.Random(42)
            equality_pairs = rng.sample(equality_pairs, MAX_EQUALITY_QUERIES)
        
        for i, j in equality_pairs:
            query_str = f"<query_equal>{i},{j}</query_equal>"
            is_equal = (self.sequence[i] == self.sequence[j])
            answer_str = yes_res if is_equal else no_res
            queries.append({"query": query_str, "answer": answer_str})
                
        return queries

