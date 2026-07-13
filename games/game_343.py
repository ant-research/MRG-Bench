# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 集合：存在一个由N个物体组成的集合，注意他们不存在位置、前后和大小关系。
# 知识点:   集合规模：集合中元素的总数量
# ============================================================

from .base import Game

class ModuloDeductionGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "集合"

    game_rule_zh = """\
我们来玩一个"取模推理"游戏，规则如下：

游戏设定了一个固定的未知正整数 N，范围在 1 到 200 之间。你的目标是通过取模查询来推断出这个数字。

你可以进行以下两种操作：

1. 取模查询：选择一个模数 k（k 必须是 3、4、5、6 或 7 中的一个），我会告诉你 N 除以 k 的余数 r。
2. 宣布答案：当你认为已经确定 N 的值时，提交你的答案。

游戏约束：
- 你最多只能进行 3 次取模查询。
- 如果查询的模数 k 不在 3、4、5、6、7 中，该查询无效但仍然计入查询次数。
- 如果宣布的答案不在 1 到 200 范围内，游戏失败。
- 你需要在尽可能少的查询次数内确定 N 并宣布答案。

## 询问与提交答案的格式（必须严格遵守）

每次操作只能包含一个标签。请使用以下 XML 格式：

- 取模查询（例如查询模数 5）：
<query_mod>5</query_mod>

- 宣布答案（例如答案是 42）：
<answer>42</answer>

注意：在宣布答案之前，请确保你已经通过取模查询收集了足够的信息。
"""

    game_rule_en = """\
Let's play a "Modulo Deduction" game. Here are the rules:

The game has set a fixed unknown positive integer N in the range from 1 to 200. Your goal is to infer this number through modulo queries.

You can perform the following two operations:

1. Modulo Query: Choose a modulus k (k must be one of 3, 4, 5, 6, or 7), and I will tell you the remainder r when N is divided by k.
2. Announce Answer: When you believe you have determined the value of N, submit your answer.

Game Constraints:
- You can perform at most 3 modulo queries.
- If the queried modulus k is not in the set {3, 4, 5, 6, 7}, the query is invalid but still counts toward the query limit.
- If the announced answer is not in the range 1 to 200, the game fails.
- You need to determine N and announce the answer with as few queries as possible.

## Query and Answer Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Modulo Query (e.g., querying modulus 5):
<query_mod>5</query_mod>

- Announce Answer (e.g., answer is 42):
<answer>42</answer>

Note: Before announcing the answer, make sure you have collected enough information through modulo queries.
"""

    contextualized_rule_zh_1 = """\
智慧交通指挥中心正在追踪一条主干道上的违章车辆总数 N（范围在 1 到 200 之间）。你的目标是通过调度抓拍探头组来推断出确切的违章车辆数。

你可以进行以下两种操作：

1. 探头分组查询（即取模查询）：选择一组探头数量 k（k 必须是 3、4、5、6 或 7 中的一个），系统会对车辆进行均分扫描，并告诉你无法被均分的剩余违章车辆数 r（即 N 除以 k 的余数）。
2. 提交调查报告（即宣布答案）：当你认为已经确定违章总数 N 的值时，提交你的最终报告。

游戏约束：
- 你最多只能进行 3 次探头分组查询。
- 如果查询的探头数量 k 不在 3、4、5、6、7 中，该查询无效但仍然计入查询次数。
- 如果提交的违章总数不在 1 到 200 范围内，任务失败。
- 你需要在尽可能少的查询次数内确定 N 并提交报告。

## 询问与提交答案的格式（必须严格遵守）

每次操作只能包含一个标签。请使用以下 XML 格式：

- 探头分组查询（例如调度 5 个探头）：
<query_mod>5</query_mod>

- 提交调查报告（例如总数是 42）：
<answer>42</answer>

注意：在提交调查报告之前，请确保你已经通过探头分组查询收集了足够的信息。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The smart traffic command center is tracking the total number of traffic violations N (ranging from 1 to 200) on a major arterial road. Your goal is to infer the exact number of violating vehicles by dispatching traffic camera groups.

You can perform the following two operations:

1. Camera Grouping Query (Modulo Query): Choose a camera group size k (k must be one of 3, 4, 5, 6, or 7). The system will scan and evenly divide the vehicles, returning the remaining number of violating vehicles r that cannot be evenly divided (i.e., the remainder when N is divided by k).
2. Submit Investigation Report (Announce Answer): When you believe you have determined the exact value of the total violations N, submit your final report.

Game Constraints:
- You can perform at most 3 camera grouping queries.
- If the queried camera size k is not in the set {3, 4, 5, 6, 7}, the query is invalid but still counts toward the query limit.
- If the submitted total violations are not in the range 1 to 200, the task fails.
- You need to determine N and submit the report with as few queries as possible.

## Query and Answer Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Camera Grouping Query (e.g., dispatching 5 cameras):
<query_mod>5</query_mod>

- Submit Investigation Report (e.g., total violations are 42):
<answer>42</answer>

Note: Before submitting the investigation report, make sure you have collected enough information through camera grouping queries.
"""

    contextualized_rule_zh_2 = """\
医学实验室中有一批未知的特定变异细胞样本，细胞总数 N 范围在 1 到 200 之间。你的目标是通过细胞阵列分配测试推断出细胞的确切数量。

你可以进行以下两种操作：

1. 阵列分配测试（即取模查询）：选择培养皿阵列的孔数 k（k 必须是 3、4、5、6 或 7 中的一个），系统会将细胞均分到各孔中，并告诉你最后剩下的游离细胞数量 r（即 N 除以 k 的余数）。
2. 录入细胞总数（即宣布答案）：当你认为已经确定细胞总数 N 的值时，提交你的检测结果。

游戏约束：
- 你最多只能进行 3 次阵列分配测试。
- 如果选择的孔数 k 不在 3、4、5、6、7 中，该测试无效但仍然计入测试次数。
- 如果录入的细胞总数不在 1 到 200 范围内，检测失败。
- 你需要在尽可能少的测试次数内确定 N 并录入总数。

## 询问与提交答案的格式（必须严格遵守）

每次操作只能包含一个标签。请使用以下 XML 格式：

- 阵列分配测试（例如选择 5 孔阵列）：
<query_mod>5</query_mod>

- 录入细胞总数（例如总数是 42）：
<answer>42</answer>

注意：在录入细胞总数之前，请确保你已经通过阵列分配测试收集了足够的信息。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
A medical laboratory holds an unknown batch of specific mutated cell samples. The total number of cells N is in the range from 1 to 200. Your goal is to infer the exact number of cells through cell array allocation tests.

You can perform the following two operations:

1. Array Allocation Test (Modulo Query): Choose the number of wells k for the culture dish array (k must be one of 3, 4, 5, 6, or 7). The system will evenly distribute the cells into the wells and tell you the number of remaining free cells r (i.e., the remainder when N is divided by k).
2. Log Total Cell Count (Announce Answer): When you believe you have determined the exact value of the total cell count N, submit your test result.

Game Constraints:
- You can perform at most 3 array allocation tests.
- If the chosen number of wells k is not in the set {3, 4, 5, 6, 7}, the test is invalid but still counts toward the test limit.
- If the logged total cell count is not in the range 1 to 200, the test fails.
- You need to determine N and log the total count with as few tests as possible.

## Query and Answer Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Array Allocation Test (e.g., choosing a 5-well array):
<query_mod>5</query_mod>

- Log Total Cell Count (e.g., total count is 42):
<answer>42</answer>

Note: Before logging the total cell count, make sure you have collected enough information through array allocation tests.
"""

    contextualized_rule_zh_3 = """\
教务系统正在统计某个神秘学术社团的报名总人数 N（范围在 1 到 200 之间）。你的目标是通过学习小组划分测试来确定确切的报名人数。

你可以进行以下两种操作：

1. 分组划分查询（即取模查询）：设定每个学习小组的人数 k（k 必须是 3、4、5、6 或 7 中的一个），系统会尝试将报名学生均分，并告诉你不足一组的剩余学生人数 r（即 N 除以 k 的余数）。
2. 确认报名人数（即宣布答案）：当你认为已经确定报名总人数 N 的值时，提交你的最终统计。

游戏约束：
- 你最多只能进行 3 次分组划分查询。
- 如果设定的小组人数 k 不在 3、4、5、6、7 中，该查询无效但仍然计入查询次数。
- 如果确认的报名人数不在 1 到 200 范围内，统计失败。
- 你需要在尽可能少的查询次数内确定 N 并确认报名人数。

## 询问与提交答案的格式（必须严格遵守）

每次操作只能包含一个标签。请使用以下 XML 格式：

- 分组划分查询（例如每组 5 人）：
<query_mod>5</query_mod>

- 确认报名人数（例如人数是 42）：
<answer>42</answer>

注意：在确认报名人数之前，请确保你已经通过分组划分查询收集了足够的信息。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The educational administration system is calculating the total number of registrations N (ranging from 1 to 200) for a mysterious academic club. Your goal is to determine the exact number of registered students through study group partitioning tests.

You can perform the following two operations:

1. Group Partitioning Query (Modulo Query): Set the number of students per study group k (k must be one of 3, 4, 5, 6, or 7). The system will attempt to evenly group the registered students and tell you the number of remaining ungrouped students r (i.e., the remainder when N is divided by k).
2. Confirm Registration Count (Announce Answer): When you believe you have determined the exact value of the total registrations N, submit your final count.

Game Constraints:
- You can perform at most 3 group partitioning queries.
- If the set group size k is not in the set {3, 4, 5, 6, 7}, the query is invalid but still counts toward the query limit.
- If the confirmed registration count is not in the range 1 to 200, the calculation fails.
- You need to determine N and confirm the registration count with as few queries as possible.

## Query and Answer Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Group Partitioning Query (e.g., 5 students per group):
<query_mod>5</query_mod>

- Confirm Registration Count (e.g., count is 42):
<answer>42</answer>

Note: Before confirming the registration count, make sure you have collected enough information through group partitioning queries.
"""

    contextualized_rule_zh_4 = """\
自动化生产线上正有一批关键零部件等待清点，零部件总数 N 范围在 1 到 200 之间。你的任务是通过启动分拣机器人组来核实确切的零部件总数。

你可以进行以下两种操作：

1. 分拣装载测试（即取模查询）：设定每组分拣机器人的装载容量 k（k 必须是 3、4、5、6 或 7 中的一个），机器满载分拣后，流水线系统会反馈未能装满的剩余散件数量 r（即 N 除以 k 的余数）。
2. 提交批次清点结果（即宣布答案）：当你认为已经确定零部件总数 N 的值时，提交你的清点数据。

游戏约束：
- 因流水线节拍限制，你最多只能进行 3 次分拣装载测试。
- 如果设定的装载容量 k 不在 3、4、5、6、7 中，该测试无效但仍然计入测试次数。
- 如果提交的清点结果不在 1 到 200 范围内，清点失败。
- 你需要在尽可能少的测试次数内确定 N 并提交清点结果。

## 询问与提交答案的格式（必须严格遵守）

每次操作只能包含一个标签。请使用以下 XML 格式：

- 分拣装载测试（例如设定容量为 5）：
<query_mod>5</query_mod>

- 提交批次清点结果（例如总数是 42）：
<answer>42</answer>

注意：在提交批次清点结果之前，请确保你已经通过分拣装载测试收集了足够的信息。
"""

    contextualized_rule_en_4 = """\
[Industry Scenario]
An automated production line is waiting to inventory a batch of critical components. The total number of components N is in the range from 1 to 200. Your task is to verify the exact total by activating automated sorting robot groups.

You can perform the following two operations:

1. Sorting Load Test (Modulo Query): Set the load capacity k for each group of sorting robots (k must be one of 3, 4, 5, 6, or 7). After fully loading and sorting, the pipeline system will report the number of remaining loose components r that couldn't fill a robot (i.e., the remainder when N is divided by k).
2. Submit Batch Inventory Result (Announce Answer): When you believe you have determined the exact value of the total components N, submit your inventory data.

Game Constraints:
- Due to assembly line rhythm limits, you can perform at most 3 sorting load tests.
- If the set load capacity k is not in the set {3, 4, 5, 6, 7}, the test is invalid but still counts toward the test limit.
- If the submitted inventory result is not in the range 1 to 200, the inventory fails.
- You need to determine N and submit the inventory result with as few tests as possible.

## Query and Answer Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Sorting Load Test (e.g., setting capacity to 5):
<query_mod>5</query_mod>

- Submit Batch Inventory Result (e.g., total count is 42):
<answer>42</answer>

Note: Before submitting the batch inventory result, make sure you have collected enough information through sorting load tests.
"""

    contextualized_rule_zh_5 = """\
法院专案组正在审查一宗复杂经济案件的涉案凭证文件，文件总数 N 范围在 1 到 200 之间。你的目标是通过指派审查配额来确切查明这些凭证的总量。

你可以进行以下两种操作：

1. 审查配额分配（即取模查询）：指定每个审查小组处理的文件配额 k（k 必须是 3、4、5、6 或 7 中的一个），系统会将文件均分发配，并向你报告留在待定区未能均分的剩余文件数 r（即 N 除以 k 的余数）。
2. 宣判文件总数（即宣布答案）：当你认为已经确凿掌握文件总数 N 的值时，正式提交你的审查结论。

游戏约束：
- 出于司法保密和效率规定，你最多只能进行 3 次审查配额分配。
- 如果指定的配额 k 不在 3、4、5、6、7 中，该分配无效但仍然计入操作次数。
- 如果宣判的文件总数不在 1 到 200 范围内，审查即告失败。
- 你需要在尽可能少的分配次数内确定 N 并宣判文件总数。

## 询问与提交答案的格式（必须严格遵守）

每次操作只能包含一个标签。请使用以下 XML 格式：

- 审查配额分配（例如指定配额 5）：
<query_mod>5</query_mod>

- 宣判文件总数（例如总数是 42）：
<answer>42</answer>

注意：在宣判文件总数之前，请确保你已经通过审查配额分配收集了足够确凿的信息。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
A special court task force is reviewing case evidentiary documents for a complex economic case. The total number of documents N ranges from 1 to 200. Your goal is to exactly ascertain the total volume of these evidences by assigning review quotas.

You can perform the following two operations:

1. Review Quota Allocation (Modulo Query): Specify the document handling quota k for each review panel (k must be one of 3, 4, 5, 6, or 7). The system will distribute the documents evenly and report back the number of remaining documents r left in the pending area that could not be evenly divided (i.e., the remainder when N is divided by k).
2. Declare Total Document Count (Announce Answer): When you believe you have conclusively determined the exact value of the total documents N, formally submit your review conclusion.

Game Constraints:
- For judicial confidentiality and efficiency, you can perform at most 3 review quota allocations.
- If the specified quota k is not in the set {3, 4, 5, 6, 7}, the allocation is invalid but still counts toward your operation limit.
- If the declared total document count is not in the range 1 to 200, the review fails.
- You need to determine N and declare the total document count with as few allocations as possible.

## Query and Answer Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Review Quota Allocation (e.g., specifying a quota of 5):
<query_mod>5</query_mod>

- Declare Total Document Count (e.g., total count is 42):
<answer>42</answer>

Note: Before declaring the total document count, make sure you have collected conclusively enough information through review quota allocations.
"""

    tags = ["answer", "query_mod"]

    # 难度配置说明：
    # 1 (简单)        - N 较小且特征明显，2次查询足够
    # 2 (中等偏下)    - N 中等，需要2-3次查询
    # 3 (中等偏上)    - N 较大，需要3次查询
    # 4 (较难)        - N 接近上限，需要精确选择模数
    # 5 (难)          - N 接近上限且需要最优策略

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"n": 23},   # 23 = 2 (mod 3), 2 (mod 7)，较小数字
            2: {"n": 87},   # 87 = 2 (mod 5), 3 (mod 6), 3 (mod 7)
            3: {"n": 142},  # 142 = 2 (mod 5), 4 (mod 6), 2 (mod 7)
            4: {"n": 177},  # 177 = 2 (mod 5), 3 (mod 6), 2 (mod 7)
            5: {"n": 197},  # 197 = 2 (mod 5), 5 (mod 6), 1 (mod 7)
        },
        "en": {
            1: {"n": 23},
            2: {"n": 87},
            3: {"n": 142},
            4: {"n": 177},
            5: {"n": 197},
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏，设置目标数字 N"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保转为整数

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.target_n = cfg["n"]  # 目标数字
        self.query_count = 0      # 已使用的查询次数
        self.max_queries = 3      # 最大查询次数
        self.valid_moduli = {3, 4, 5, 6, 7}  # 有效的模数集合
        
        # 用于显示的游戏信息
        self._game_info["n"] = "?"  # 不在规则中透露具体数字

    def evaluate(self, parsed_info):
        """评估玩家提交的答案是否正确"""
        try:
            answer = int(parsed_info["answer"].strip())
            
            # 检查答案是否在有效范围内
            if answer < 1 or answer > 200:
                return False
            
            # 检查答案是否正确
            return answer == self.target_n
        except (ValueError, KeyError):
            return False

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑：处理查询并返回读数"""
        if "query_mod" in parsed_info:
            # 检查是否超过查询次数限制
            if self.query_count >= self.max_queries:
                if self.config.language == "zh":
                    return f"查询次数已用尽（最多{self.max_queries}次）。请直接提交你的答案。"
                else:
                    return f"Query limit reached ({self.max_queries} queries used). Please submit your answer directly."
            
            try:
                k = int(parsed_info["query_mod"].strip())
            except ValueError:
                self.query_count += 1
                if self.config.language == "zh":
                    return f"错误：模数必须是整数。剩余查询次数：{self.max_queries - self.query_count}"
                else:
                    return f"Error: Modulus must be an integer. Remaining queries: {self.max_queries - self.query_count}"
            
            # 增加查询计数
            self.query_count += 1
            
            # 检查模数是否有效
            if k not in self.valid_moduli:
                if self.config.language == "zh":
                    return f"错误：模数必须是 3、4、5、6 或 7 中的一个。该查询无效但已计入次数。剩余查询次数：{self.max_queries - self.query_count}"
                else:
                    return f"Error: Modulus must be one of 3, 4, 5, 6, or 7. This invalid query still counts. Remaining queries: {self.max_queries - self.query_count}"
            
            # 计算并返回余数
            remainder = self.target_n % k
            if self.config.language == "zh":
                return f"N 除以 {k} 的余数是 {remainder}。剩余查询次数：{self.max_queries - self.query_count}"
            else:
                return f"N mod {k} = {remainder}. Remaining queries: {self.max_queries - self.query_count}"
        
        else:
            if self.config.language == "zh":
                raise ValueError("无效的查询格式。")
            else:
                raise ValueError("Invalid query format.")

    def _cf_make_wrong(self, correct: str) -> str:
        """根据正确答案生成一个错误的取模查询回复（修改余数值，保证在合法范围内）"""
        import re
        
        # 匹配中文格式: "N 除以 k 的余数是 r。..."
        zh_match = re.search(r'除以\s*(\d+)\s*的余数是\s*(\d+)', correct)
        if zh_match:
            k = int(zh_match.group(1))
            old_r = int(zh_match.group(2))
            # 在 [0, k-1] 范围内选一个不同的余数
            new_r = (old_r + 1) % k
            if new_r == old_r:
                new_r = (old_r + 2) % k
            return correct.replace(f"余数是 {old_r}", f"余数是 {new_r}")
        
        # 匹配英文格式: "N mod k = r. ..."
        en_match = re.search(r'mod\s+(\d+)\s*=\s*(\d+)', correct)
        if en_match:
            k = int(en_match.group(1))
            old_r = int(en_match.group(2))
            new_r = (old_r + 1) % k
            if new_r == old_r:
                new_r = (old_r + 2) % k
            return correct.replace(f"= {old_r}", f"= {new_r}", 1)  # 只替换第一处
        
        # 兜底
        return correct + " [WRONG]"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法的模数查询并返回对应的正确答案。
        为冗余性评估提供所有可能的信息维度，不受查询次数限制。
        """
        results = []

        for k in sorted(list(self.valid_moduli)):
            remainder = self.target_n % k
            
            query_str = f"<query_mod>{k}</query_mod>"
            
            if self.config.language == "zh":
                ans = f"N 除以 {k} 的余数是 {remainder}。"
            else:
                ans = f"N mod {k} = {remainder}."
            
            results.append({
                "query": query_str,
                "answer": ans
            })
            
        return results