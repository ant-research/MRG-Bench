# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   排序结果：序列排序后第k位的元素是什么
# ============================================================

from .base import Game
import random
import itertools


class SymbolicSortingGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "序列"

    game_rule_zh = """\
我们来玩一个"符号序列排序推理"游戏，规则如下：

游戏设定了一个符号集，包含 {sigma_size} 个不同的符号。这些符号之间存在一个严格的全序关系（即每两个符号都有明确的大小关系），但这个全序关系对你是隐藏的。

现在有一个集合 S，包含 {n} 个长度为 {length} 的符号串，每个串都由上述符号集中的符号组成，且彼此不同。你可以看到每个串的完整内容。集合 S 如下：
{string_list}

排序规则（已知）：对于任意两个长度为 {length} 的串，按照从左到右的位置依次进行字典序比较。在第一个不相同的位置上，哪个串在该位置的符号在隐藏全序中更小，该串就更小。

你的目标：确定将集合 S 按上述规则排序后，位于第 {k} 位的元素是哪一个（请给出其在原集合中的索引，从 1 开始编号）。

你可以进行多次询问来推断隐藏的符号全序关系。每次询问只能选择以下三类之一：

1. 真实串比较（A类）：询问集合中的两个串 xi 和 xj 哪个更小。
2. 探针与真实串比较（B类）：给出一个自定义的探针串 p 和集合中的串 xi，询问谁更小（探针串必须与 xi 不同）。
3. 探针互比（C类）：给出两个自定义的探针串 p 和 q，询问谁更小（两个探针串必须不同）。

我会根据隐藏的符号全序关系如实回答每次询问。无效的询问（如索引越界、串内容非法、比较对象相同等）不会被计入有效询问次数。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- A类查询（例如比较索引 1 和 2 的串）：
<query_a>1,2</query_a>

- B类查询（例如用探针串 abc 与索引 3 的串比较）：
<query_b>abc,3</query_b>

- C类查询（例如比较探针串 abc 和 def）：
<query_c>abc,def</query_c>

提交最终答案时，必须说明排序后第 {k} 位对应的原索引（从 1 开始），格式如下：
<answer>索引数字</answer>

注：答案标签中只需填写索引数字。

请尽可能用较少的询问次数完成推理。
"""

    game_rule_en = """\
Let's play a "Symbolic Sequence Sorting Inference" game. Here are the rules:

The game has a symbol set containing {sigma_size} distinct symbols. There exists a strict total order among these symbols (i.e., any two symbols have a definite ordering relation), but this order is hidden from you.

Now there is a set S containing {n} strings, each of length {length}, composed of symbols from the symbol set, and all strings are distinct. You can see the complete content of each string. Set S is as follows:
{string_list}

Sorting Rule (known): For any two strings of length {length}, compare them lexicographically from left to right position by position. At the first differing position, whichever string has the smaller symbol at that position (according to the hidden total order) is considered smaller.

Your Goal: Determine which element is at position {k} after sorting set S by the above rule (provide its index in the original set, starting from 1).

You can make multiple queries to infer the hidden symbol order. Each query must be one of the following three types:

1. Real String Comparison (Type A): Ask which is smaller between two strings xi and xj in the set.
2. Probe vs Real String Comparison (Type B): Provide a custom probe string p and a string xi in the set, ask which is smaller (probe string must differ from xi).
3. Probe Comparison (Type C): Provide two custom probe strings p and q, ask which is smaller (the two probe strings must differ).

I will answer each query truthfully based on the hidden symbol order. Invalid queries (e.g., index out of range, illegal string content, comparing identical objects) will not count toward valid query count.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Type A Query (e.g., compare strings at index 1 and 2):
<query_a>1,2</query_a>

- Type B Query (e.g., compare probe string abc with string at index 3):
<query_b>abc,3</query_b>

- Type C Query (e.g., compare probe strings abc and def):
<query_c>abc,def</query_c>

When submitting the final answer, specify the original index (starting from 1) of the element at position {k} after sorting, using this format:
<answer>INDEX_NUMBER</answer>

Note: The answer tag should only contain the index number.

Please complete the inference with as few queries as possible.
"""

    contextualized_rule_zh_1 = """\
你是一名智能交通路网调度员。系统遇到了一批等待通过单行隧道的特种车队。

系统中存在一个车辆标识集，包含 {sigma_size} 个不同的标识符。这些标识符之间有着严格的优先通行全序关系（即每两个标识符都有明确的优先级高低），但这套关系对你是隐藏的。

现在有 {n} 个车队（集合 S），每个车队包含 {length} 个车辆标识符串联而成，且各个车队的序列彼此不同。你能看到每个车队的完整组成：
{string_list}

排序规则：对任意两个长度为 {length} 的车队，按从左到右的位置依次进行字典序比较。在第一个不相同的位置上，哪个车队在该位置的标识符在隐藏全序中更小（优先级更高），该车队就更小（排在更前面）。

你的目标：确定将集合 S 按此规则排序后，获得第 {k} 位通行权的是哪一个车队（给出其在原集合中的索引，从 1 开始）。

你可以通过系统进行多次模拟测试：
1. 真实车队比较（A类）：比较集合中的车队 xi 和 xj 哪个更小。
2. 探针车队与真实车队比较（B类）：用自定义探针车队 p 与集合中的 xi 比较（两者需不同）。
3. 探针车队互比（C类）：比较两个不同的自定义探针车队 p 和 q。

XML标签格式：
- A类：<query_a>1,2</query_a>
- B类：<query_b>abc,3</query_b>
- C类：<query_c>abc,def</query_c>

提交最终答案（排序后第 {k} 位对应的原索引）：
<answer>索引数字</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
You are an intelligent traffic network dispatcher. A batch of special convoys is waiting to pass through a one-way tunnel.

The system has a vehicle identifier set containing {sigma_size} distinct symbols. There is a strict hidden total order of right-of-way priority among these symbols.

There are {n} convoys (Set S), each represented by a sequence of {length} vehicle identifiers. All convoys are distinct. Set S is:
{string_list}

Sorting Rule: For any two convoys of length {length}, they are compared lexicographically from left to right. At the first differing position, the convoy with the smaller symbol (higher priority in the hidden order) is considered smaller (earlier in the queue).

Your Goal: Determine which convoy is at position {k} after sorting Set S (provide its original index, starting from 1).

You can run multiple simulation queries:
1. Real Convoy Comparison (Type A): Ask which is smaller between convoys xi and xj in the set.
2. Probe vs Real Convoy (Type B): Provide a custom probe convoy p and a real convoy xi to compare (must differ).
3. Probe Comparison (Type C): Compare two custom probe convoys p and q (must differ).

XML Query Formats:
- Type A: <query_a>1,2</query_a>
- Type B: <query_b>abc,3</query_b>
- Type C: <query_c>abc,def</query_c>

Submit final answer (original index of the element at position {k}):
<answer>INDEX_NUMBER</answer>
"""

    contextualized_rule_zh_2 = """\
你是一名急诊科分诊系统的架构师。

系统使用一组分诊评估指标集，包含 {sigma_size} 个不同的症状符号。这些符号间存在严格的危重程度全序关系（即明确的轻重缓急排序），但具体排序规则对你隐藏。

当前有 {n} 名候诊患者（集合 S），每名患者的病情由长度为 {length} 的症状符号串表示（代表各阶段的评估结果），且彼此不同。患者集合 S 如下：
{string_list}

排序规则：比较两名患者的症状串时，按评估阶段从左到右依次进行字典序对比。在第一个不同的评估阶段上，哪个患者的症状符号在隐藏全序中更小（代表优先级更高/更危重），该患者的排序就更小（更早接受治疗）。

你的目标：确定将集合 S 排序后，排在第 {k} 位接受治疗的患者是哪一位（给出原集合中的索引，从 1 开始）。

你可以向系统发起多次推断询问：
1. 真实患者比较（A类）：询问集合中患者 xi 和 xj 谁排序更小。
2. 虚拟病历与真实患者比较（B类）：用自定义的虚拟症状串 p 与患者 xi 比较（必须不同）。
3. 虚拟病历互比（C类）：比较两个自定义的虚拟症状串 p 和 q（必须不同）。

询问格式：
- A类：<query_a>1,2</query_a>
- B类：<query_b>abc,3</query_b>
- C类：<query_c>abc,def</query_c>

最终答案（排序后第 {k} 位的原索引）：
<answer>索引数字</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
You are an architect of an emergency triage system.

The system uses a set of {sigma_size} distinct triage assessment symbols. There is a strict hidden total order of clinical severity among them.

Currently, there are {n} patients (Set S), each represented by a symptom string of length {length} (showing sequential assessment results). All profiles are distinct. Set S is:
{string_list}

Sorting Rule: To compare two patients, their symptom strings are evaluated lexicographically from left to right. At the first differing phase, the patient with the smaller symbol in the hidden order (indicating higher severity/priority) is considered smaller (treated earlier).

Your Goal: Determine which patient will be at position {k} in the triage queue after sorting (provide original index, starting from 1).

You can make queries to infer the order:
1. Real Patient Comparison (Type A): Compare patients xi and xj.
2. Probe vs Real Patient (Type B): Compare a custom probe symptom string p and patient xi (must differ).
3. Probe Comparison (Type C): Compare two custom probe strings p and q (must differ).

Query Formats:
- Type A: <query_a>1,2</query_a>
- Type B: <query_b>abc,3</query_b>
- Type C: <query_c>abc,def</query_c>

Submit final answer (original index for position {k}):
<answer>INDEX_NUMBER</answer>
"""

    contextualized_rule_zh_3 = """\
你是一名教育评估机构的数据分析专家。

你们的素养评测系统包含 {sigma_size} 个不同的等级评定符号。这些符号间存在一个严格的全序关系（代表不同的能力权重），但该权重顺序目前对你是保密的。

现有 {n} 名考生的成绩单（集合 S），每份成绩单由 {length} 个评定符号组成（代表不同科目的表现），且各不相同。成绩单集合 S 如下：
{string_list}

排序规则：比较两份成绩单时，按照科目从左到右依次进行字典序比对。在第一个不同的科目位置上，谁的评定符号在隐藏全序中更小（代表排名更靠前），该成绩单的总体顺位就更小。

你的目标：确定将这批成绩单排序后，位列第 {k} 名的考生是哪一位（给出原集合中的索引，从 1 开始）。

你可以通过系统进行多次比对询问：
1. 真实考生比对（A类）：比较考生 xi 和 xj 谁的顺位更小。
2. 虚拟成绩单与真实考生比对（B类）：用自定义探针成绩单 p 与考生 xi 比较（必须不同）。
3. 虚拟成绩单互比（C类）：比较两个自定义成绩单 p 和 q（必须不同）。

格式要求：
- A类：<query_a>1,2</query_a>
- B类：<query_b>abc,3</query_b>
- C类：<query_c>abc,def</query_c>

最终答案提交（排名第 {k} 位的原索引）：
<answer>索引数字</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
You are a data analysis expert at an educational assessment agency.

The competency evaluation system uses {sigma_size} distinct grading symbols. A strict hidden total order (representing different capability weights) exists among them.

There are {n} student transcripts (Set S), each composed of {length} grading symbols (representing performance in sequential subjects). All transcripts are distinct. Set S is:
{string_list}

Sorting Rule: Two transcripts are compared lexicographically from left to right. At the first differing subject position, the transcript with the smaller grading symbol in the hidden order (indicating a higher rank) is considered smaller overall.

Your Goal: Determine which student ranks at position {k} after sorting (provide original index, starting from 1).

You can query the system:
1. Real Student Comparison (Type A): Compare transcripts xi and xj.
2. Probe vs Real Student (Type B): Compare a custom probe transcript p and student xi (must differ).
3. Probe Comparison (Type C): Compare two custom probe transcripts p and q (must differ).

Query Formats:
- Type A: <query_a>1,2</query_a>
- Type B: <query_b>abc,3</query_b>
- Type C: <query_c>abc,def</query_c>

Submit final answer (original index for position {k}):
<answer>INDEX_NUMBER</answer>
"""

    contextualized_rule_zh_4 = """\
你是一名智能制造工厂的品控主管。

生产线上的零部件质检评级由 {sigma_size} 个不同的质量代码符号表示。这些符号存在严格的质量优劣全序关系，但该基准排序对你隐藏。

当前有 {n} 个批次的产品（集合 S），每个批次由 {length} 个零部件的代码序列构成，且各批次序列不同。集合 S 如下：
{string_list}

排序规则：比较任意两个批次时，按装配顺序从左到右进行字典序比对。在第一个不同的零部件位置上，哪个批次的质量代码在隐藏全序中更小（代表质量更优或处理优先级更高），该批次的整体排序就更小。

你的目标：确定将集合 S 排序后，排在第 {k} 位的批次是哪一个（给出原集合中的索引，从 1 开始）。

你可以发起多次抽样测试：
1. 真实批次比较（A类）：询问集合中批次 xi 和 xj 哪个更小。
2. 探针批次与真实批次比较（B类）：用自定义探针批次序列 p 与真实批次 xi 比较（必须不同）。
3. 探针批次互比（C类）：比较两个探针序列 p 和 q（必须不同）。

查询格式：
- A类：<query_a>1,2</query_a>
- B类：<query_b>abc,3</query_b>
- C类：<query_c>abc,def</query_c>

最终答案提交（排在第 {k} 位的原索引）：
<answer>索引数字</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
You are a quality control supervisor at a smart manufacturing plant.

Component quality ratings on the assembly line are represented by {sigma_size} distinct quality codes. A strict hidden total order of quality standards exists among them.

There are {n} batches of products (Set S), each represented by a sequence of {length} component codes. All batches are distinct. Set S is:
{string_list}

Sorting Rule: When comparing two batches, their sequences are evaluated lexicographically from left to right along the assembly order. At the first differing component position, the batch with the smaller code in the hidden order (indicating superior quality or higher processing priority) is considered smaller.

Your Goal: Determine which batch sits at position {k} after sorting Set S (provide original index, starting from 1).

You can run sampling tests:
1. Real Batch Comparison (Type A): Compare batches xi and xj.
2. Probe vs Real Batch (Type B): Compare a custom probe batch sequence p and real batch xi (must differ).
3. Probe Comparison (Type C): Compare two custom probe sequences p and q (must differ).

Query Formats:
- Type A: <query_a>1,2</query_a>
- Type B: <query_b>abc,3</query_b>
- Type C: <query_c>abc,def</query_c>

Submit final answer (original index for position {k}):
<answer>INDEX_NUMBER</answer>
"""

    contextualized_rule_zh_5 = """\
你是一名高级法务合规分析师。

在复杂的案件分析引擎中，有 {sigma_size} 个不同的法条适用权重符号。这些符号间存在严格的司法量级全序关系，但该排序逻辑对前端隐藏。

目前案卷库中有 {n} 个复合案卷（集合 S），每个案卷由长度为 {length} 的权重符号串构成（代表定性事实序列），且各案卷互不相同。案卷集合 S 如下：
{string_list}

排序规则：比较两个案卷时，按事实序列从左到右依次进行字典序比对。在第一个出现不同的事实上，哪个案卷的权重符号在隐藏全序中更小（代表优先审理或量级更高），该案卷的整体排序就更小。

你的目标：确定将集合 S 排序后，位列第 {k} 审理顺位的案卷是哪一个（给出原库中的索引，从 1 开始）。

你可以向引擎发起多次逻辑推演：
1. 真实案卷比较（A类）：比较库中的案卷 xi 和 xj 谁的排序更小。
2. 假设案卷与真实案卷比较（B类）：用自定义假设案卷 p 与真实案卷 xi 比较（必须不同）。
3. 假设案卷互比（C类）：比较两个自定义假设案卷 p 和 q（必须不同）。

推演请求格式：
- A类：<query_a>1,2</query_a>
- B类：<query_b>abc,3</query_b>
- C类：<query_c>abc,def</query_c>

最终答案提交（排序第 {k} 位的原索引）：
<answer>索引数字</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
You are a senior legal compliance analyst.

In a complex case analysis engine, there are {sigma_size} distinct statutory weight symbols. A strict hidden total order of judicial magnitude exists among them.

Currently, the docket contains {n} compound cases (Set S), each formed by a string of {length} weight symbols (representing a sequence of material facts). All cases are distinct. Set S is:
{string_list}

Sorting Rule: Cases are compared lexicographically from left to right along their fact sequences. At the first differing fact, the case with the smaller weight symbol in the hidden order (indicating higher trial priority or magnitude) is considered smaller.

Your Goal: Determine which case will be at trial position {k} after sorting (provide original index, starting from 1).

You can make logical deductions by querying the engine:
1. Real Case Comparison (Type A): Compare cases xi and xj.
2. Hypothetical vs Real Case (Type B): Compare a custom hypothetical case p and real case xi (must differ).
3. Hypothetical Case Comparison (Type C): Compare two hypothetical cases p and q (must differ).

Query Formats:
- Type A: <query_a>1,2</query_a>
- Type B: <query_b>abc,3</query_b>
- Type C: <query_c>abc,def</query_c>

Submit final answer (original index for position {k}):
<answer>INDEX_NUMBER</answer>
"""

    tags = ["answer", "query_a", "query_b", "query_c"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "sigma_size": 3,
                "length": 3,
                "n": 3,
                "k": 2,
                "symbols": ["甲", "乙", "丙"],
                "order": ["甲", "乙", "丙"],  # 甲 < 乙 < 丙
                "strings": ["乙甲丙", "甲丙乙", "丙乙甲"]
            },
            2: {
                "sigma_size": 4,
                "length": 3,
                "n": 4,
                "k": 2,
                "symbols": ["α", "β", "γ", "δ"],
                "order": ["α", "β", "γ", "δ"],  # α < β < γ < δ
                "strings": ["βαγ", "αγβ", "γβα", "δαβ"]
            },
            3: {
                "sigma_size": 4,
                "length": 3,
                "n": 5,
                "k": 3,
                "symbols": ["红", "绿", "蓝", "黄"],
                "order": ["红", "黄", "绿", "蓝"],  # 红 < 黄 < 绿 < 蓝
                "strings": ["绿红蓝", "红蓝绿", "蓝绿红", "黄红绿", "绿黄蓝"]
            },
            4: {
                "sigma_size": 5,
                "length": 3,
                "n": 6,
                "k": 4,
                "symbols": ["A", "B", "C", "D", "E"],
                "order": ["C", "A", "E", "B", "D"],  # C < A < E < B < D
                "strings": ["ABE", "CAB", "DCA", "EBD", "BEC", "ADE"]
            },
            5: {
                "sigma_size": 5,
                "length": 3,
                "n": 7,
                "k": 5,
                "symbols": ["★", "◆", "■", "●", "▲"],
                "order": ["■", "●", "★", "▲", "◆"],  # ■ < ● < ★ < ▲ < ◆
                "strings": ["★◆■", "◆★●", "■▲◆", "●■★", "▲●◆", "★■▲", "◆●■"]
            }
        },
        "en": {
            1: {
                "sigma_size": 3,
                "length": 3,
                "n": 3,
                "k": 2,
                "symbols": ["X", "Y", "Z"],
                "order": ["X", "Y", "Z"],  # X < Y < Z
                "strings": ["YXZ", "XZY", "ZYX"]
            },
            2: {
                "sigma_size": 4,
                "length": 3,
                "n": 4,
                "k": 2,
                "symbols": ["α", "β", "γ", "δ"],
                "order": ["α", "β", "γ", "δ"],  # α < β < γ < δ
                "strings": ["βαγ", "αγβ", "γβα", "δαβ"]
            },
            3: {
                "sigma_size": 4,
                "length": 3,
                "n": 5,
                "k": 3,
                "symbols": ["R", "G", "B", "Y"],
                "order": ["R", "Y", "G", "B"],  # R < Y < G < B
                "strings": ["GRB", "RBG", "BGR", "YRG", "GYB"]
            },
            4: {
                "sigma_size": 5,
                "length": 3,
                "n": 6,
                "k": 4,
                "symbols": ["A", "B", "C", "D", "E"],
                "order": ["C", "A", "E", "B", "D"],  # C < A < E < B < D
                "strings": ["ABE", "CAB", "DCA", "EBD", "BEC", "ADE"]
            },
            5: {
                "sigma_size": 5,
                "length": 3,
                "n": 7,
                "k": 5,
                "symbols": ["★", "◆", "■", "●", "▲"],
                "order": ["■", "●", "★", "▲", "◆"],  # ■ < ● < ★ < ▲ < ◆
                "strings": ["★◆■", "◆★●", "■▲◆", "●■★", "▲●◆", "★■▲", "◆●■"]
            }
        }
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏状态，包括符号集、隐藏全序、字符串集合等"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 保存配置信息
        self.sigma_size = cfg["sigma_size"]
        self.length = cfg["length"]
        self.n = cfg["n"]
        self.k = cfg["k"]
        self.symbols = cfg["symbols"]
        self.order = cfg["order"]  # 隐藏的符号全序
        self.strings = cfg["strings"]  # 字符串集合
        
        # 构建符号的序关系映射（用于快速比较）
        self.symbol_rank = {sym: idx for idx, sym in enumerate(self.order)}
        
        # 计算正确答案：对字符串集合按隐藏全序排序
        indexed_strings = [(i+1, s) for i, s in enumerate(self.strings)]
        sorted_strings = sorted(indexed_strings, key=lambda x: self._string_sort_key(x[1]))
        self.correct_answer = sorted_strings[self.k - 1][0]  # 第k位的原索引
        
        # 准备展示给玩家的字符串列表
        if lang == "zh":
            string_display = "\n".join([f"  索引 {i+1}: {s}" for i, s in enumerate(self.strings)])
        else:
            string_display = "\n".join([f"  Index {i+1}: {s}" for i, s in enumerate(self.strings)])
        
        # 填充游戏信息
        self._game_info = {
            "sigma_size": self.sigma_size,
            "length": self.length,
            "n": self.n,
            "k": self.k,
            "string_list": string_display
        }

    def _string_sort_key(self, s):
        """将字符串转换为可排序的键（基于隐藏全序）"""
        return tuple(self.symbol_rank.get(c, float('inf')) for c in s)

    def _compare_strings(self, s1, s2):
        """
        比较两个字符串的大小
        返回：-1 表示s1<s2, 1表示s1>s2, 0表示相等
        """
        key1 = self._string_sort_key(s1)
        key2 = self._string_sort_key(s2)
        if key1 < key2:
            return -1
        elif key1 > key2:
            return 1
        else:
            return 0

    def _validate_string(self, s):
        """验证字符串是否合法（长度和符号都正确）"""
        if len(s) != self.length:
            return False
        for c in s:
            if c not in self.symbols:
                return False
        return True

    def evaluate(self, parsed_info):
        """评估玩家提交的答案是否正确"""
        try:
            answer = int(parsed_info["answer"].strip())
            return answer == self.correct_answer
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """原 produce_response 的核心逻辑"""
        lang = self.config.language
        first_smaller = "前者更小" if lang == "zh" else "The first is smaller"
        second_smaller = "后者更小" if lang == "zh" else "The second is smaller"
        equal_msg = "两者相等" if lang == "zh" else "They are equal"
        invalid_msg = "无效询问" if lang == "zh" else "Invalid query"

        # A类查询：比较两个真实串
        if "query_a" in parsed_info:
            try:
                raw = parsed_info["query_a"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return invalid_msg
                
                idx1, idx2 = int(parts[0]), int(parts[1])
                
                # 验证索引有效性
                if idx1 < 1 or idx1 > self.n or idx2 < 1 or idx2 > self.n:
                    return invalid_msg
                if idx1 == idx2:
                    return invalid_msg
                
                s1 = self.strings[idx1 - 1]
                s2 = self.strings[idx2 - 1]
                
                result = self._compare_strings(s1, s2)
                if result < 0:
                    return first_smaller
                elif result > 0:
                    return second_smaller
                else:
                    return equal_msg
            except:
                return invalid_msg

        # B类查询：探针串与真实串比较
        elif "query_b" in parsed_info:
            try:
                raw = parsed_info["query_b"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return invalid_msg
                
                probe = parts[0]
                idx = int(parts[1])
                
                # 验证索引有效性
                if idx < 1 or idx > self.n:
                    return invalid_msg
                
                # 验证探针串合法性
                if not self._validate_string(probe):
                    return invalid_msg
                
                real_string = self.strings[idx - 1]
                
                # 探针串必须与真实串不同
                if probe == real_string:
                    return invalid_msg
                
                result = self._compare_strings(probe, real_string)
                if result < 0:
                    return first_smaller
                elif result > 0:
                    return second_smaller
                else:
                    return equal_msg
            except:
                return invalid_msg

        # C类查询：两个探针串比较
        elif "query_c" in parsed_info:
            try:
                raw = parsed_info["query_c"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return invalid_msg
                
                probe1 = parts[0]
                probe2 = parts[1]
                
                # 验证探针串合法性
                if not self._validate_string(probe1) or not self._validate_string(probe2):
                    return invalid_msg
                
                # 两个探针串必须不同
                if probe1 == probe2:
                    return invalid_msg
                
                result = self._compare_strings(probe1, probe2)
                if result < 0:
                    return first_smaller
                elif result > 0:
                    return second_smaller
                else:
                    return equal_msg
            except:
                return invalid_msg

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """生成错误答案：将比较结果取反"""
        lang = self.config.language
        if lang == "zh":
            if correct == "前者更小":
                return "后者更小"
            elif correct == "后者更小":
                return "前者更小"
            elif correct == "两者相等":
                return "前者更小"
            elif correct == "无效询问":
                return "前者更小"
            else:
                return "后者更小"
        else:
            if correct == "The first is smaller":
                return "The second is smaller"
            elif correct == "The second is smaller":
                return "The first is smaller"
            elif correct == "They are equal":
                return "The first is smaller"
            elif correct == "Invalid query":
                return "The first is smaller"
            else:
                return "The second is smaller"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法的 A 类查询（真实串两两比较），
        以及有限的 B 类查询（按报告实为C类查询，修改自报告），避免查询数量爆炸。
        """
        queries = []
        lang = self.config.language
        first_smaller = "前者更小" if lang == "zh" else "The first is smaller"
        second_smaller = "后者更小" if lang == "zh" else "The second is smaller"

        # 1. 枚举所有 A 类查询 (Index vs Index)
        for i in range(1, self.n + 1):
            for j in range(i + 1, self.n + 1):
                s1 = self.strings[i-1]
                s2 = self.strings[j-1]
                
                res = self._compare_strings(s1, s2)
                ans = first_smaller if res < 0 else second_smaller
                
                queries.append({
                    "query": f"<query_a>{i},{j}</query_a>",
                    "answer": ans
                })

        # 2. 为每对相邻符号生成一个 C 类查询，帮助确定符号全序
        for idx in range(len(self.order) - 1):
            sym1 = self.order[idx]
            sym2 = self.order[idx + 1]
            # 构造只在第一个位置不同的探针串
            padding = self.symbols[0] * (self.length - 1)
            p1 = sym1 + padding
            p2 = sym2 + padding
            if p1 != p2:
                res = self._compare_strings(p1, p2)
                ans = first_smaller if res < 0 else second_smaller
                queries.append({
                    "query": f"<query_c>{p1},{p2}</query_c>",
                    "answer": ans
                })

        return queries