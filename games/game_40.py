# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   区间条件计数：某区间内满足特定条件的元素有多少个
# ============================================================

from .base import Game
import re


class BinarySequenceRangeGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "序列"

    game_rule_zh = """\
我们现在来玩一个"二值序列识别"的推理游戏，规则如下：

游戏设定了一个长度为 {n} 的二值序列（每个位置的值为 0 或 1），索引从 1 到 {n}。序列中恰好有 {k} 个位置的值为 1，其余为 0。但具体哪些位置为 1 是未知的。

你的目标是通过尽可能少的查询次数，准确识别出所有值为 1 的位置。

你可以进行区间查询：每次选择一个区间 [l, r]（l 和 r 都是 1 到 {n} 之间的整数，且 l 必须小于 r，不允许单点查询），我会告诉你该区间内有多少个位置的值为 1。

注意：每次查询都会消耗你的查询预算，请谨慎使用。

## 查询与提交答案的格式（必须严格遵守）

每次只能包含一个标签。请使用以下 XML 格式：

- 区间查询（例如查询区间 [2, 5]）：
<query_range>2,5</query_range>

提交最终答案时，列出所有你认为值为 1 的位置编号（用逗号隔开，顺序不限），格式如下：

<answer>1,3,7</answer>

注意：提交的位置数量必须恰好等于 {k} 个。
"""

    game_rule_en = """\
Let's play a "Binary Sequence Identification" deduction game. Here are the rules:

There is a binary sequence of length {n} (each position has a value of 0 or 1), indexed from 1 to {n}. Exactly {k} positions in the sequence have a value of 1, and the rest are 0. However, which positions are 1 is unknown.

Your goal is to accurately identify all positions with value 1 using as few queries as possible.

You can perform range queries: each time, select a range [l, r] (both l and r are integers between 1 and {n}, and l must be less than r; single-point queries are not allowed), and I will tell you how many positions in that range have a value of 1.

Note: Each query consumes your query budget, so use them carefully.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Range Query (e.g., querying range [2, 5]):
<query_range>2,5</query_range>

When submitting the final answer, list all position IDs you believe have a value of 1 (comma-separated, order does not matter), using this format:

<answer>1,3,7</answer>

Note: The number of submitted positions must be exactly {k}.
"""

    contextualized_rule_zh_1 = """\
在智慧交通管理系统中，有一段包含 {n} 个连续路段的高速公路（编号从 1 到 {n}）。系统检测到恰好有 {k} 个路段的监控设备发生了故障，其余路段设备正常。但具体是哪些路段发生故障尚未明确。

你的目标是通过最少的排查次数，精准定位所有发生故障的监控设备位置，以便调度维修团队。

你可以进行区间巡检：每次输入一个区间 [l, r]（l 和 r 均为 1 到 {n} 之间的整数，且 l 必须小于 r，不支持单点巡检），系统会通过无人机扫描并返回该区间内故障设备的数量。

注意：每次巡检都会消耗无人机的电量和巡检预算，请谨慎规划您的巡检范围。

## 查询与提交答案的格式（必须严格遵守）

每次只能包含一个标签。请使用以下 XML 格式：

- 区间巡检（例如巡检路段 [2, 5]）：
<query_range>2,5</query_range>

提交最终排查结果时，列出所有你认为存在故障的路段编号（用逗号隔开，顺序不限），格式如下：

<answer>1,3,7</answer>

注意：提交的故障路段数量必须恰好等于 {k} 个。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
In the smart traffic management system, there is a highway stretch consisting of {n} consecutive road segments (indexed from 1 to {n}). The system has detected that exactly {k} segments have malfunctioning surveillance cameras, while the rest are operating normally. However, the exact locations of these malfunctions are currently unknown.

Your goal is to accurately pinpoint all the malfunctioning camera locations using the minimum number of inspections to dispatch maintenance teams efficiently.

You can perform range inspections: each time, select a range [l, r] (both l and r are integers between 1 and {n}, with l less than r; single-point inspections are not supported). The system will deploy a drone scan and return the total number of malfunctioning cameras within that specific range.

Note: Each inspection consumes drone battery and inspection budget, so plan your queries carefully.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Range Inspection (e.g., inspecting segments [2, 5]):
<query_range>2,5</query_range>

When submitting the final investigation results, list all segment IDs you believe have malfunctions (comma-separated, order does not matter), using this format:

<answer>1,3,7</answer>

Note: The number of submitted segments must be exactly {k}.
"""

    contextualized_rule_zh_2 = """\
在精准医疗基因测序中，有一段包含 {n} 个连续基因位点的序列（编号从 1 到 {n}）。通过初步筛查，我们确认该片段中恰好有 {k} 个位点发生了特定的致病突变，其余位点均正常。但具体是哪些位点发生了突变尚属未知。

你的目标是通过尽可能少的批量检测次数，精准识别出所有发生突变的基因位点，以为患者制定靶向基因疗法。

你可以进行区间批量测序：每次选择一个测序区间 [l, r]（l 和 r 均为 1 到 {n} 之间的整数，且 l 必须小于 r，受技术限制不允许单点测序），实验室会返回该区间内含有突变的位点总数。

注意：每次批量测序都会消耗高昂的试剂成本和时间预算，请谨慎设计测序区间。

## 查询与提交答案的格式（必须严格遵守）

每次只能包含一个标签。请使用以下 XML 格式：

- 区间批量测序（例如测序位点 [2, 5]）：
<query_range>2,5</query_range>

提交最终诊断结果时，列出所有你认为存在突变的位点编号（用逗号隔开，顺序不限），格式如下：

<answer>1,3,7</answer>

注意：提交的突变位点数量必须恰好等于 {k} 个。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
In precision medicine gene sequencing, there is a sequence containing {n} consecutive genetic loci (indexed from 1 to {n}). Initial screening confirms that exactly {k} loci in this segment have specific pathogenic mutations, while the rest are normal. However, the exact locations of these mutated loci are still unknown.

Your goal is to accurately identify all mutated genetic loci using the minimum number of batch tests to formulate a targeted gene therapy for the patient.

You can perform range batch sequencing: each time, select a testing range [l, r] (both l and r are integers between 1 and {n}, with l less than r; due to technical limitations, single-locus testing is not permitted). The laboratory will return the total number of mutated loci within that specified range.

Note: Each batch sequencing consumes expensive reagents and time budget, so design your testing ranges carefully.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Range Batch Sequencing (e.g., testing loci [2, 5]):
<query_range>2,5</query_range>

When submitting the final diagnostic results, list all locus IDs you believe are mutated (comma-separated, order does not matter), using this format:

<answer>1,3,7</answer>

Note: The number of submitted locus IDs must be exactly {k}.
"""

    contextualized_rule_zh_3 = """\
在标准化考试质量评估中，有一份包含 {n} 道连续题目的试卷（题号从 1 到 {n}）。统计分析显示，试卷中恰好有 {k} 道题目存在异常难度（即区分度不合格），其余题目指标正常。但具体是哪几道题目出现异常尚未定位。

你的目标是通过最少的批量分析次数，准确排查出所有存在异常的题目，以便教研组进行复核。

你可以进行区间批量分析：每次选择一个题块区间 [l, r]（l 和 r 均为 1 到 {n} 之间的整数，且 l 必须小于 r，不支持单题分析），评测系统会返回该区间内存在异常的题目数量。

注意：每次区间分析都会消耗系统的算力配额，请谨慎规划您的分析范围。

## 查询与提交答案的格式（必须严格遵守）

每次只能包含一个标签。请使用以下 XML 格式：

- 区间批量分析（例如分析题目 [2, 5]）：
<query_range>2,5</query_range>

提交最终复核名单时，列出所有你认为存在异常的题目编号（用逗号隔开，顺序不限），格式如下：

<answer>1,3,7</answer>

注意：提交的异常题目数量必须恰好等于 {k} 个。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
In the quality assessment of a standardized test, there is an exam paper containing {n} consecutive questions (numbered from 1 to {n}). Statistical analysis reveals that exactly {k} questions have anomalous difficulty levels (i.e., poor discrimination indices), while the rest are normal. However, the specific questions exhibiting these anomalies have not yet been pinpointed.

Your goal is to accurately identify all anomalous questions using the minimum number of batch analyses so the curriculum board can review them.

You can perform range batch analyses: each time, select a block of questions [l, r] (both l and r are integers between 1 and {n}, with l less than r; single-question analysis is not supported). The evaluation system will return the total number of anomalous questions within that block.

Note: Each range analysis consumes system computational quotas, so plan your analysis scope carefully.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Range Batch Analysis (e.g., analyzing questions [2, 5]):
<query_range>2,5</query_range>

When submitting the final review list, list all question IDs you believe are anomalous (comma-separated, order does not matter), using this format:

<answer>1,3,7</answer>

Note: The number of submitted question IDs must be exactly {k}.
"""

    contextualized_rule_zh_4 = """\
在工业制造流水线上，刚刚生产了一批包含 {n} 个连续编号的机械零件（编号从 1 到 {n}）。质检系统初步预警，该批次中恰好有 {k} 个零件存在微观结构缺陷，其余零件为合格品。但具体是哪些零件存在缺陷尚待排查。

你的目标是通过最少的X光批量扫描次数，精准找出所有缺陷零件，以防止其流入下游供应链。

你可以进行区间批量扫描：每次将一个区间的零件 [l, r]（l 和 r 均为 1 到 {n} 之间的整数，且 l 必须小于 r，设备不支持单件扫描）送入X光机，设备会返回该区间内缺陷零件的总数。

注意：每次扫描都会消耗设备的检测寿命和排查预算，请谨慎安排扫描批次。

## 查询与提交答案的格式（必须严格遵守）

每次只能包含一个标签。请使用以下 XML 格式：

- 区间批量扫描（例如扫描零件 [2, 5]）：
<query_range>2,5</query_range>

提交最终剔除名单时，列出所有你认为存在缺陷的零件编号（用逗号隔开，顺序不限），格式如下：

<answer>1,3,7</answer>

注意：提交的缺陷零件数量必须恰好等于 {k} 个。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
On an industrial manufacturing assembly line, a batch of {n} sequentially numbered mechanical parts has just been produced (indexed from 1 to {n}). The quality control system has issued a preliminary alert that exactly {k} parts in this batch contain microscopic structural defects, while the rest are compliant. However, the specific defective parts have yet to be isolated.

Your goal is to accurately pinpoint all defective parts using the fewest number of X-ray batch scans to prevent them from entering the downstream supply chain.

You can perform range batch scans: each time, send a sequential range of parts [l, r] (both l and r are integers between 1 and {n}, with l less than r; the equipment does not support single-part scanning) through the X-ray scanner, which will return the total number of defective parts within that range.

Note: Each scan consumes equipment detection lifespan and inspection budget, so schedule your scanning batches carefully.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Range Batch Scan (e.g., scanning parts [2, 5]):
<query_range>2,5</query_range>

When submitting the final removal list, list all part IDs you believe are defective (comma-separated, order does not matter), using this format:

<answer>1,3,7</answer>

Note: The number of submitted defective part IDs must be exactly {k}.
"""

    contextualized_rule_zh_5 = """\
在一次商业欺诈审计调查中，审计团队掌握了一份包含 {n} 条连续财务账目流水（编号从 1 到 {n}）的分类账。宏观对账表明，该账本中恰好有 {k} 条流水属于伪造的欺诈交易，其余流水合法。但具体是哪几笔账目造假目前仍是盲区。

你的目标是通过最少的批量核查次数，准确锁定所有欺诈交易记录，以便将其作为证据提交法庭。

你可以进行区间账目核查：每次调取一个流水区间 [l, r]（l 和 r 均为 1 到 {n} 之间的整数，且 l 必须小于 r，合规要求不允许单笔核查），系统会自动核对凭证并返回该区间内的欺诈交易笔数。

注意：每次核查都会消耗审计时间和合规审批额度，请谨慎规划您的取证范围。

## 查询与提交答案的格式（必须严格遵守）

每次只能包含一个标签。请使用以下 XML 格式：

- 区间账目核查（例如核查账目 [2, 5]）：
<query_range>2,5</query_range>

提交最终取证结果时，列出所有你认为属于欺诈交易的账目编号（用逗号隔开，顺序不限），格式如下：

<answer>1,3,7</answer>

注意：提交的欺诈账目数量必须恰好等于 {k} 个。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
In a commercial fraud audit investigation, the auditing team has secured a ledger containing {n} consecutive financial transaction entries (numbered from 1 to {n}). Macro-reconciliation indicates that exactly {k} entries in this ledger are forged fraudulent transactions, while the rest are legitimate. However, the specific fraudulent entries remain a blind spot.

Your goal is to accurately lock down all fraudulent transaction records using the minimum number of batch audits, so they can be presented as evidence in court.

You can perform range ledger audits: each time, pull a sequence of entries [l, r] (both l and r are integers between 1 and {n}, with l less than r; compliance regulations forbid single-entry auditing). The system will automatically cross-check the vouchers and return the total number of fraudulent transactions within that specific range.

Note: Each audit consumes investigation time and compliance approval quotas, so plan your evidentiary scope carefully.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Range Ledger Audit (e.g., auditing entries [2, 5]):
<query_range>2,5</query_range>

When submitting the final evidentiary results, list all entry IDs you believe are fraudulent (comma-separated, order does not matter), using this format:

<answer>1,3,7</answer>

Note: The number of submitted fraudulent entry IDs must be exactly {k}.
"""

    tags = ["answer", "query_range"]

    # 难度配置说明：
    # 1 (简单)       - N=10, K=3, Q=15  适中的参数，查询预算充足
    # 2 (中等偏下)   - N=15, K=5, Q=20  序列更长，需要更精细的策略
    # 3 (中等偏上)   - N=20, K=6, Q=22  查询预算相对紧张
    # 4 (较难)       - N=25, K=8, Q=25  需要高效的二分或分治策略
    # 5 (难)         - N=30, K=10, Q=28 高度优化的查询策略才能成功

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 10,
                "k": 3,
                "q": 15,
                "sequence": "0,1,0,0,1,0,0,1,0,0",  # 位置 2, 5, 8
            },
            2: {
                "n": 15,
                "k": 5,
                "q": 20,
                "sequence": "1,0,0,1,0,1,0,0,0,1,0,0,1,0,0",  # 位置 1, 4, 6, 10, 13
            },
            3: {
                "n": 20,
                "k": 6,
                "q": 22,
                "sequence": "0,1,0,0,1,0,1,0,0,0,1,0,0,1,0,0,0,1,0,0",  # 位置 2, 5, 7, 11, 14, 18
            },
            4: {
                "n": 25,
                "k": 8,
                "q": 25,
                "sequence": "1,0,0,1,0,1,0,0,1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0",  # 位置 1, 4, 6, 9, 12, 16, 18, 22
            },
            5: {
                "n": 30,
                "k": 10,
                "q": 28,
                "sequence": "0,1,0,1,0,0,1,0,1,0,0,1,0,0,1,0,1,0,0,1,0,0,1,0,1,0,0,0,0,0",  # 位置 2, 4, 7, 9, 12, 15, 17, 20, 23, 25
            },
        },
        "en": {
            1: {
                "n": 10,
                "k": 3,
                "q": 15,
                "sequence": "0,1,0,0,1,0,0,1,0,0",
            },
            2: {
                "n": 15,
                "k": 5,
                "q": 20,
                "sequence": "1,0,0,1,0,1,0,0,0,1,0,0,1,0,0",
            },
            3: {
                "n": 20,
                "k": 6,
                "q": 22,
                "sequence": "0,1,0,0,1,0,1,0,0,0,1,0,0,1,0,0,0,1,0,0",
            },
            4: {
                "n": 25,
                "k": 8,
                "q": 25,
                "sequence": "1,0,0,1,0,1,0,0,1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0",
            },
            5: {
                "n": 30,
                "k": 10,
                "q": 28,
                "sequence": "0,1,0,1,0,0,1,0,1,0,0,1,0,0,1,0,1,0,0,1,0,0,1,0,1,0,0,0,0,0",
            },
        },
    }

    def __init__(self, config):
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
        self._game_info["k"] = cfg["k"]
        
        # 解析二值序列
        self.sequence = [int(x.strip()) for x in cfg["sequence"].split(",")]
        if len(self.sequence) != cfg["n"]:
            raise ValueError("Sequence length does not match n")
        
        # 计算真实答案集合（值为1的位置，索引从1开始）
        self.true_positions = set()
        for i, val in enumerate(self.sequence, start=1):
            if val == 1:
                self.true_positions.add(i)
        
        if len(self.true_positions) != cfg["k"]:
            raise ValueError("Number of 1s does not match k")
        
        # 查询计数器
        self.query_count = 0
        self.max_queries = cfg["q"]

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        try:
            # 解析提交的位置集合
            submitted_positions = set()
            if raw_ans:  # 防止空字符串
                for pos_str in raw_ans.split(","):
                    pos_str = pos_str.strip()
                    if pos_str:
                        submitted_positions.add(int(pos_str))
            
            # 检查数量是否正确
            if len(submitted_positions) != self._game_info["k"]:
                return False
            
            # 检查是否完全匹配
            return submitted_positions == self.true_positions
            
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑：处理查询并返回结果"""
        if "query_range" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        # 检查查询预算
        if self.query_count >= self.max_queries:
            if self.config.language == "zh":
                return f"查询预算已用尽（已使用 {self.max_queries}/{self.max_queries} 次）。请直接提交你的最终答案。"
            else:
                return f"Query budget exhausted ({self.max_queries}/{self.max_queries} used). Please submit your final answer now."
        
        raw_query = parsed_info["query_range"].strip()
        
        # 解析查询区间 [l, r]
        parts = [x.strip() for x in raw_query.split(",")]
        if len(parts) != 2:
            if self.config.language == "zh":
                return "错误：查询格式无效。请使用格式：<query_range>l,r</query_range>"
            else:
                return "Error: Invalid query format. Use: <query_range>l,r</query_range>"
        
        try:
            l, r = int(parts[0]), int(parts[1])
        except (ValueError, TypeError):
            if self.config.language == "zh":
                return "错误：查询格式无效。请使用格式：<query_range>l,r</query_range>"
            else:
                return "Error: Invalid query format. Use: <query_range>l,r</query_range>"
        
        # 验证查询合法性
        if l < 1 or r > self._game_info["n"]:
            if self.config.language == "zh":
                return f"错误：区间越界。有效范围是 1 到 {self._game_info['n']}。"
            else:
                return f"Error: Range out of bounds. Valid range is 1 to {self._game_info['n']}."
        
        if l >= r:
            if self.config.language == "zh":
                return "错误：必须满足 l 小于 r，不允许单点查询。"
            else:
                return "Error: l must be less than r. Single-point queries are not allowed."
        
        # 计算区间内值为1的数量
        count = sum(self.sequence[i-1] for i in range(l, r+1))
        
        # 增加查询计数
        self.query_count += 1
        
        remaining = self.max_queries - self.query_count
        if self.config.language == "zh":
            return f"区间 [{l}, {r}] 内值为 1 的数量为：{count}（剩余查询次数：{remaining}）"
        else:
            return f"The count of 1s in range [{l}, {r}] is: {count} (remaining queries: {remaining})"

    def _cf_make_wrong(self, correct: str) -> str:
        """根据正确的produce响应，生成一个数值被篡改的错误响应"""
        import re as _re
        # 尝试找到响应中的核心数值（区间内1的数量）并篡改
        # 中文格式: "...值为 1 的数量为：3（剩余..."
        # 英文格式: "...is: 3 (remaining..."
        
        if self.config.language == "zh":
            pattern = r'(数量为：\s*)(\d+)'
        else:
            pattern = r'(is:\s*)(\d+)'
        
        match = _re.search(pattern, correct)
        if match:
            original_num = int(match.group(2))
            # 生成一个不同的数值
            wrong_num = original_num + 1 if original_num == 0 else original_num - 1
            return correct[:match.start(2)] + str(wrong_num) + correct[match.end(2):]
        
        # fallback: 如果无法解析，追加 _WRONG
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        答案格式与 _cf_core_produce 返回格式保持一致。
        """
        queries = []
        n = self._game_info["n"]
        
        for l in range(1, n):
            for r in range(l + 1, n + 1):
                count = sum(self.sequence[l-1 : r])
                
                if self.config.language == "zh":
                    answer_str = f"区间 [{l}, {r}] 内值为 1 的数量为：{count}"
                else:
                    answer_str = f"The count of 1s in range [{l}, {r}] is: {count}"
                
                queries.append({
                    "query": f"<query_range>{l},{r}</query_range>",
                    "answer": answer_str
                })
                
        return queries