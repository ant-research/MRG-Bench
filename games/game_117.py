# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 集合：存在一个由N个物体组成的集合，注意他们不存在位置、前后和大小关系。
# 知识点:   集合规模：集合中元素的总数量
# ============================================================

from .base import Game
import random

class ModuloIdentificationGame(Game):

    game_rule_zh = """\
我们现在来玩一个"模数识别"的推理游戏，规则如下：

游戏设定了一个未知的正整数 N，范围为 1 到 {max_n}。你的目标是通过查询来确定这个数字。

你可以反复进行以下查询（每次仅限一个查询）：

**模数查询**：你可以选择一个除数 q（q 只能是 2, 3, 4, 5, 6, 7, 8, 9 中的一个），我会告诉你 N 除以 q 的余数。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 模数查询（例如询问 N 除以 5 的余数）：
<query_mod>5</query_mod>

提交最终答案时，直接给出你认为的 N 值，格式如下：

<answer>42</answer>

注意：你需要尽可能少的查询次数来确定答案。
"""

    game_rule_en = """\
Let's play a "Modulo Identification" deduction game. Here are the rules:

The game has set an unknown positive integer N, ranging from 1 to {max_n}. Your goal is to determine this number through queries.

You can repeatedly perform the following query (one query at a time):

**Modulo Query**: You can choose a divisor q (q can only be one of 2, 3, 4, 5, 6, 7, 8, 9), and I will tell you the remainder when N is divided by q.

When you have collected enough information, please submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Modulo Query (e.g., asking for the remainder when N is divided by 5):
<query_mod>5</query_mod>

When submitting the final answer, directly provide the value of N you believe is correct, in the following format:

<answer>42</answer>

Note: You should use as few queries as possible to determine the answer.
"""

    # 场景 1：交通
    contextualized_rule_zh_1 = """\
城市交通指挥中心监控到一辆违规的套牌车辆，其真实的内部识别码是一个正整数 N（范围 1 到 {max_n}）。你的目标是锁定该识别码。

你可以反复调用监控探头（每次仅限一个查询）：

**模数查询**：你可以调用特定频段的探头（探头型号代号 q，只能是 2, 3, 4, 5, 6, 7, 8, 9 中的一个），探头会返回识别码 N 除以 q 的余数。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 模数查询（例如询问代号为 5 的探头返回的余数）：
<query_mod>5</query_mod>

提交最终答案时，直接给出你认为的 N 值，格式如下：

<answer>42</answer>

注意：你需要尽可能少的查询次数来确定答案。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The city traffic command center is tracking an illegal cloned vehicle. Its true internal identification code is a positive integer N (ranging from 1 to {max_n}). Your goal is to determine this code.

You can repeatedly activate cameras (one query at a time):

**Modulo Query**: You can activate specific camera models (model code q, must be one of 2, 3, 4, 5, 6, 7, 8, 9), and the camera will return the remainder when N is divided by q.

When you have collected enough information, please submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Modulo Query (e.g., asking for the remainder from camera model 5):
<query_mod>5</query_mod>

When submitting the final answer, directly provide the value of N you believe is correct, in the following format:

<answer>42</answer>

Note: You should use as few queries as possible to determine the answer.
"""

    # 场景 2：医疗
    contextualized_rule_zh_2 = """\
疾病控制中心发现了一种未知病原体，其核心基因序列长度是一个正整数 N（范围 1 到 {max_n}）。为了合成靶向特效药，你需要确定这个序列长度。

你可以反复进行实验分析（每次仅限一个查询）：

**模数查询**：你可以使用不同长度的探针进行杂交分析（探针长度 q，只能是 2, 3, 4, 5, 6, 7, 8, 9 中的一个），系统会返回未匹配的残余碱基数（即 N 除以 q 的余数）。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 模数查询（例如询问使用长度为 5 的探针返回的余数）：
<query_mod>5</query_mod>

提交最终答案时，直接给出你认为的 N 值，格式如下：

<answer>42</answer>

注意：你需要尽可能少的实验次数来确定答案。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
The CDC has discovered an unknown pathogen. Its core gene sequence length is a positive integer N (ranging from 1 to {max_n}). To synthesize a targeted drug, you must determine this length.

You can repeatedly perform experimental analysis (one query at a time):

**Modulo Query**: You can use probes of different lengths for hybridization analysis (probe length q, must be one of 2, 3, 4, 5, 6, 7, 8, 9). The system will return the number of unmatched residual bases (i.e., the remainder when N is divided by q).

When you have collected enough information, please submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Modulo Query (e.g., asking for the remainder when using a probe of length 5):
<query_mod>5</query_mod>

When submitting the final answer, directly provide the value of N you believe is correct, in the following format:

<answer>42</answer>

Note: You should use as few experiments as possible to determine the answer.
"""

    # 场景 3：教育
    contextualized_rule_zh_3 = """\
在全国中学生数学奥林匹克竞赛的密室逃脱环节，密码锁的密码是一个正整数 N（范围 1 到 {max_n}）。学生们需要解开这个密码才能通关。

你可以反复向考官提问（每次仅限一个查询）：

**模数查询**：你可以向考官提供一个测试除数 q（只能是 2, 3, 4, 5, 6, 7, 8, 9 中的一个），考官会告诉你密码 N 除以 q 的余数作为提示。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 模数查询（例如询问 N 除以 5 的余数）：
<query_mod>5</query_mod>

提交最终答案时，直接给出你认为的 N 值，格式如下：

<answer>42</answer>

注意：你需要尽可能少的提问次数来确定答案。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
In the escape room segment of the National Middle School Math Olympiad, the combination lock password is a positive integer N (ranging from 1 to {max_n}). Students must crack this password to pass.

You can repeatedly ask the examiner questions (one query at a time):

**Modulo Query**: You can provide the examiner with a test divisor q (must be one of 2, 3, 4, 5, 6, 7, 8, 9), and the examiner will give you the remainder when password N is divided by q as a hint.

When you have collected enough information, please submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Modulo Query (e.g., asking for the remainder when N is divided by 5):
<query_mod>5</query_mod>

When submitting the final answer, directly provide the value of N you believe is correct, in the following format:

<answer>42</answer>

Note: You should use as few questions as possible to determine the answer.
"""

    # 场景 4：制造业/工业
    contextualized_rule_zh_4 = """\
在精密零件流水线上，有一批微型齿轮出现异常。异常批次的加工编号是一个正整数 N（范围 1 到 {max_n}）。为了追溯问题根源并校准机器，你需要确定这个编号。

你可以反复使用质检系统进行测试（每次仅限一个查询）：

**模数查询**：你可以使用不同规格的分组检测工具（分组大小 q，只能是 2, 3, 4, 5, 6, 7, 8, 9 中的一个），每次测试会返回该编号在分组后的位置偏移量（即 N 除以 q 的余数）。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，重新校准失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 模数查询（例如询问使用分组大小为 5 的检测工具返回的偏移量）：
<query_mod>5</query_mod>

提交最终答案时，直接给出你认为的 N 值，格式如下：

<answer>42</answer>

注意：你需要尽可能少的测试次数来确定答案。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
On a precision parts assembly line, a batch of micro gears has an anomaly. The processing serial number of the abnormal batch is a positive integer N (ranging from 1 to {max_n}). To trace the root cause and calibrate the machine, you need to determine this serial number.

You can repeatedly use the quality control system for testing (one query at a time):

**Modulo Query**: You can use different grouping inspection tools (group size q, must be one of 2, 3, 4, 5, 6, 7, 8, 9). Each test returns the positional offset of the serial number within the group (i.e., the remainder when N is divided by q).

When you have collected enough information, please submit your final answer. If the answer is wrong or the format is invalid, recalibration fails.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Modulo Query (e.g., asking for the offset using a grouping tool with size 5):
<query_mod>5</query_mod>

When submitting the final answer, directly provide the value of N you believe is correct, in the following format:

<answer>42</answer>

Note: You should use as few tests as possible to determine the answer.
"""

    # 场景 5：法律
    contextualized_rule_zh_5 = """\
在侦办一起跨国洗钱案时，金融罪案调查科截获了一个加密的离岸账户资金流转密钥，该密钥是一个正整数 N（范围 1 到 {max_n}）。为了合法冻结账户，检方必须准确提供此密钥。

你可以反复向银行合规审计系统提交传票（每次仅限一个查询）：

**模数查询**：要求用特定的合规校验码 q（q 只能是 2, 3, 4, 5, 6, 7, 8, 9 中的一个）对账户进行哈希取模审计，系统会返回密钥的取模余数（即 N 除以 q 的余数）。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 模数查询（例如要求合规校验码为 5 的审计余数）：
<query_mod>5</query_mod>

提交最终答案时，直接给出你认为的 N 值，格式如下：

<answer>42</answer>

注意：你需要尽可能少的传票次数来确定答案。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
During the investigation of a transnational money laundering case, the Financial Crimes Investigation Division intercepted an encrypted offshore account fund transfer key, which is a positive integer N (ranging from 1 to {max_n}). To legally freeze the account, prosecutors must accurately provide this key.

You can repeatedly submit subpoenas to the bank's compliance audit system (one query at a time):

**Modulo Query**: You request a hash modulo audit of the account using a specific compliance verification code q (q must be one of 2, 3, 4, 5, 6, 7, 8, 9). The system will return the modulo remainder of the key (i.e., the remainder when N is divided by q).

When you have collected enough information, please submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Modulo Query (e.g., requesting the audit remainder with compliance verification code 5):
<query_mod>5</query_mod>

When submitting the final answer, directly provide the value of N you believe is correct, in the following format:

<answer>42</answer>

Note: You should use as few subpoenas as possible to determine the answer.
"""

    tags = ["query_mod", "answer"]
    reasoning_type = "归纳推理"
    data_structure = "集合"

    def _initialize_game(self):
        difficulty = getattr(self.config, 'difficulty', 1)
        if isinstance(difficulty, str):
            difficulty = int(difficulty)
        
        difficulty_map = {
            1: 30,
            2: 100,
            3: 500,
            4: 1000,
            5: 2520,
        }
        self.max_n = difficulty_map.get(difficulty, 2520)
        
        seed = getattr(self.config, 'seed', None)
        if seed is None:
            seed = hash(('ModuloIdentificationGame', difficulty)) & 0xFFFFFFFF
        rng = random.Random(seed)
        self.target_n = rng.randint(1, self.max_n)
        self._game_info = {"max_n": self.max_n}

    def evaluate(self, parsed_info):
        try:
            return int(parsed_info.get("answer")) == self.target_n
        except (ValueError, TypeError):
            return False

    def _cf_core_produce(self, parsed_info):
        if "query_mod" in parsed_info:
            try:
                q = int(parsed_info["query_mod"])
                if q in [2, 3, 4, 5, 6, 7, 8, 9]:
                    return str(self.target_n % q)
                else:
                    return "无效的除数" if self.config.language == "zh" else "Invalid divisor"
            except ValueError:
                return "参数错误" if self.config.language == "zh" else "Parameter error"
        return "无效的查询" if self.config.language == "zh" else "Invalid query"

    def get_all_possible_queries(self) -> list:
        queries = []
        for q in range(2, 10):
            queries.append({
                "query":  f"<query_mod>{q}</query_mod>",
                "answer": str(self.target_n % q),
            })
        return queries

    def _cf_make_wrong(self, correct):
        try:
            val = int(correct)
            wrong = val + 1 if val == 0 else val - 1
            return str(wrong)
        except ValueError:
            return "0"