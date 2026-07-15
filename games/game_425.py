from .base import Game
import random

class SymbolicPeakSearch(Game):

    game_rule_zh = """\
我们现在来玩一个"符号峰值搜索"的推理游戏，规则如下：

游戏设定了一个有序索引集合 1 到 {n}。在这个集合中，存在且仅存在一个未知索引 M，它是序列中唯一极大值的位置。

我使用了一个固定的符号反馈系统。游戏中有三个符号：{symbol1}、{symbol2}、{symbol3}。当你探测一个位置 k 时，我会根据 M 和 k 的相对关系返回一个符号：
- 如果 M 小于 k，返回某个特定符号
- 如果 M 等于 k，返回某个特定符号
- 如果 M 大于 k，返回某个特定符号

但是，符号与相对关系的对应方式有四种可能的方案（方案 A、B、C、D），我在游戏开始时已秘密选定了其中一种，并且在整局游戏中保持不变。你需要通过探测来推断出使用的是哪种方案，以及极大值的具体位置 M。

你的目标是用尽可能少的探测次数，同时正确确定：
1. 使用的映射方案（A、B、C 或 D）
2. 极大值位置 M

每次探测时，使用以下 XML 格式指定一个索引位置：

<query_position>k</query_position>

其中 k 是你要探测的位置编号（1 到 {n} 之间的整数）。

提交最终答案时，必须同时给出方案编号和极大值位置，格式如下：

<answer>scheme=A, position=5</answer>

其中 scheme 可以是 A、B、C 或 D，position 是你推断的极大值位置编号。
"""

    game_rule_en = """\
Let's play a "Symbolic Peak Search" deduction game. Here are the rules:

There is an ordered index set from 1 to {n}. In this set, there exists exactly one unknown index M, which is the position of the unique maximum value in the sequence.

I use a fixed symbolic feedback system. There are three symbols in the game: {symbol1}, {symbol2}, {symbol3}. When you probe a position k, I will return a symbol based on the relative relationship between M and k:
- If M is less than k, return a specific symbol
- If M equals k, return a specific symbol
- If M is greater than k, return a specific symbol

However, there are four possible schemes (scheme A, B, C, D) for the correspondence between symbols and relative relationships. I have secretly selected one at the start of the game, and it remains fixed throughout. You need to infer which scheme is being used and the exact position M through probing.

Your goal is to correctly determine both, using as few probes as possible:
1. The mapping scheme being used (A, B, C, or D)
2. The maximum value position M

For each probe, use the following XML format to specify an index position:

<query_position>k</query_position>

where k is the position number you want to probe (an integer between 1 and {n}).

When submitting the final answer, you must provide both the scheme identifier and the maximum position, using this format:

<answer>scheme=A, position=5</answer>

where scheme can be A, B, C, or D, and position is your inferred maximum value position.
"""

    contextualized_rule_zh_1 = """\
欢迎进入智能交通流量监控系统。

在核心高速公路的某路段上，我们划分了从 1 到 {n} 依次排列的监测站。其中仅存在一个监测站 M，它是当前整条公路的唯一拥堵峰值（车流量极大值）位置。

系统配备了一套加密的无人机侦测系统。共有三种状态符号：{symbol1}、{symbol2}、{symbol3}。当你向监测站 k 发送侦测指令时，无人机会根据拥堵峰值 M 与 k 的相对位置返回一个加密符号：
- 如果拥堵峰值 M 在当前站点的上游（M 小于 k），返回某个特定符号
- 如果拥堵峰值 M 正好在当前站点（M 等于 k），返回某个特定符号
- 如果拥堵峰值 M 在当前站点的下游（M 大于 k），返回某个特定符号

由于系统固件的随机初始化，符号与相对位置关系的加密映射方案共有四种（方案 A、B、C、D）。系统在启动时已秘密选定了一种方案，并在当前调度周期内保持不变。你需要通过试探性侦测，推断出使用的是哪种加密方案，以及拥堵峰值的确切监测站 M。

你的目标是用尽可能少的侦测次数，同时正确确定：
1. 系统使用的加密映射方案（A、B、C 或 D）
2. 拥堵峰值的监测站位置 M

每次侦测时，使用以下 XML 格式指定一个监测站编号：

<query_position>k</query_position>

其中 k 是你要探测的监测站编号（1 到 {n} 之间的整数）。

提交最终分析报告时，必须同时给出方案编号和峰值位置，格式如下：

<answer>scheme=A, position=5</answer>

其中 scheme 可以是 A、B、C 或 D，position 是你推断的拥堵峰值监测站编号。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the Intelligent Traffic Flow Monitoring System.

On a core highway segment, we have designated sequentially ordered monitoring stations from 1 to {n}. There is exactly one station M which is the unique congestion peak (maximum traffic volume) of this segment.

The system is equipped with an encrypted drone reconnaissance system. There are three status symbols: {symbol1}, {symbol2}, {symbol3}. When you dispatch a drone to probe station k, it returns an encrypted symbol based on the relative position of the congestion peak M to k:
- If the congestion peak M is upstream of the current station (M is less than k), it returns a specific symbol
- If the congestion peak M is exactly at the current station (M equals k), it returns a specific symbol
- If the congestion peak M is downstream of the current station (M is greater than k), it returns a specific symbol

Due to random firmware initialization, there are four possible encrypted mapping schemes (schemes A, B, C, D) corresponding to these relationships. The system secretly selected one scheme at startup, which remains fixed during the current dispatch cycle. You need to infer which encryption scheme is active and the exact station M of the congestion peak through probing.

Your goal is to correctly determine both, using as few drone probes as possible:
1. The active encrypted mapping scheme (A, B, C, or D)
2. The congestion peak station position M

For each probe, use the following XML format to specify a station number:

<query_position>k</query_position>

where k is the station number you want to probe (an integer between 1 and {n}).

When submitting the final analysis report, you must provide both the scheme identifier and the peak position, using this format:

<answer>scheme=A, position=5</answer>

where scheme can be A, B, C, or D, and position is your inferred congestion peak station number.
"""

    contextualized_rule_zh_2 = """\
欢迎使用基因突变靶向检测平台。

在我们正在分析的 DNA 序列中，存在从 1 到 {n} 的有序基因片段。生化分析表明，在此区间内存在且仅存在一个片段 M，它是唯一的高频突变表达峰值位置。

系统采用了一套基于生化试剂显色的反馈机制。显色结果有三种特定符号：{symbol1}、{symbol2}、{symbol3}。当你对片段 k 进行靶向检测时，试剂会根据突变峰值 M 与 k 的相对生化距离返回一个符号：
- 如果突变峰值 M 在当前片段的 5' 端方向（M 小于 k），返回某个特定符号
- 如果突变峰值 M 恰好位于当前片段（M 等于 k），返回某个特定符号
- 如果突变峰值 M 在当前片段的 3' 端方向（M 大于 k），返回某个特定符号

由于各批次试剂的感光特性差异，显色符号与相对位置的对应法则共有四种可能的方案（方案 A、B、C、D）。检验开始前已固定选用了其中一个批次，因此对应方案保持不变。你需要通过靶向检测来推断出使用的是哪种试剂方案，以及突变峰值的具体片段 M。

你的目标是用尽可能少的检测次数，同时正确确定：
1. 试剂的显色映射方案（A、B、C 或 D）
2. 突变峰值的基因片段位置 M

每次靶向检测时，使用以下 XML 格式指定一个基因片段编号：

<query_position>k</query_position>

其中 k 是你要检测的片段编号（1 到 {n} 之间的整数）。

提交最终诊断结果时，必须同时给出方案编号和突变峰值位置，格式如下：

<answer>scheme=A, position=5</answer>

其中 scheme 可以是 A、B、C 或 D，position 是你推断的突变峰值片段编号。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the Genomic Mutation Targeted Detection Platform.

In the DNA sequence we are analyzing, there are ordered gene segments from 1 to {n}. Biochemical profiling indicates that within this interval, there exists exactly one segment M, which is the unique high-frequency mutation expression peak.

The system utilizes a reagent-based colorimetric feedback mechanism yielding three specific symbols: {symbol1}, {symbol2}, {symbol3}. When you run a targeted test on segment k, the reagent returns a symbol based on the relative biochemical distance between the mutation peak M and k:
- If the mutation peak M is towards the 5' end of the current segment (M is less than k), it returns a specific symbol
- If the mutation peak M is exactly at the current segment (M equals k), it returns a specific symbol
- If the mutation peak M is towards the 3' end of the current segment (M is greater than k), it returns a specific symbol

Due to batch variations in reagent photosensitivity, there are four possible schemes mapping colorimetric symbols to relative positions (schemes A, B, C, D). A specific batch was selected before the assay began, so the scheme remains fixed. You need to infer which reagent scheme is being used and the exact mutation peak segment M through testing.

Your goal is to correctly determine both, using as few tests as possible:
1. The reagent's colorimetric mapping scheme (A, B, C, or D)
2. The mutation peak gene segment position M

For each targeted test, use the following XML format to specify a gene segment number:

<query_position>k</query_position>

where k is the segment number you want to test (an integer between 1 and {n}).

When submitting the final diagnostic result, you must provide both the scheme identifier and the mutation peak position, using this format:

<answer>scheme=A, position=5</answer>

where scheme can be A, B, C, or D, and position is your inferred mutation peak segment number.
"""

    contextualized_rule_zh_3 = """\
欢迎使用自适应学习认知评估系统。

本课程依据难度递进被划分为从 1 到 {n} 的有序知识模块。在这些模块中，存在且仅存在一个未知模块 M，它是该评估对象（学生）的最佳认知挑战峰值（即心流状态的最大值位置）。

系统使用一套行为观测标签来进行反馈。评估系统提供三个观测符号：{symbol1}、{symbol2}、{symbol3}。当你向学生推送模块 k 的测试时，系统会根据其最佳挑战峰值 M 与 k 的相对难度差异返回一个符号：
- 如果最佳挑战峰值 M 属于较低难度的模块（M 小于 k），返回某个特定符号
- 如果最佳挑战峰值 M 正好是当前模块（M 等于 k），返回某个特定符号
- 如果最佳挑战峰值 M 属于较高难度的模块（M 大于 k），返回某个特定符号

根据不同的学生认知模型类型，系统在底层配置了四种可能的标签映射方案（方案 A、B、C、D）。在评估开始时，系统已秘密锁定了该学生的模型方案且整局保持不变。你需要通过推送测试，推断出该学生的标签映射方案，以及确切的最佳挑战模块 M。

你的目标是用尽可能少的测试推送次数，同时正确确定：
1. 使用的认知标签映射方案（A、B、C 或 D）
2. 最佳认知挑战峰值模块 M

每次推送测试时，使用以下 XML 格式指定一个知识模块编号：

<query_position>k</query_position>

其中 k 是你要测试的模块编号（1 到 {n} 之间的整数）。

提交最终评估报告时，必须同时给出方案编号和挑战峰值位置，格式如下：

<answer>scheme=A, position=5</answer>

其中 scheme 可以是 A、B、C 或 D，position 是你推断的最佳挑战峰值模块编号。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Adaptive Learning Cognitive Assessment System.

This curriculum is divided into sequentially ordered knowledge modules from 1 to {n} based on increasing difficulty. Within these modules, there exists exactly one unknown module M, which represents the optimal cognitive challenge peak (the maximum state of flow) for the assessed student.

The system uses an observational behavioral tagging feedback loop. It outputs three observational symbols: {symbol1}, {symbol2}, {symbol3}. When you push a test from module k to the student, the system returns a symbol based on the relative difficulty difference between their optimal challenge peak M and k:
- If the optimal peak M is at a lower difficulty module (M is less than k), it returns a specific symbol
- If the optimal peak M is exactly at the current module (M equals k), it returns a specific symbol
- If the optimal peak M is at a higher difficulty module (M is greater than k), it returns a specific symbol

Depending on the student's cognitive model typology, the system configures one of four possible tag mapping schemes (schemes A, B, C, D). At the start of the assessment, the system secretly locked into one scheme which remains fixed throughout. You need to infer the student's mapping scheme and their exact optimal challenge module M through testing.

Your goal is to correctly determine both, using as few test pushes as possible:
1. The cognitive tag mapping scheme used (A, B, C, or D)
2. The optimal cognitive challenge peak module M

For each test push, use the following XML format to specify a module number:

<query_position>k</query_position>

where k is the module number you want to test (an integer between 1 and {n}).

When submitting the final assessment report, you must provide both the scheme identifier and the challenge peak position, using this format:

<answer>scheme=A, position=5</answer>

where scheme can be A, B, C, or D, and position is your inferred optimal challenge peak module number.
"""

    contextualized_rule_zh_4 = """\
欢迎进入工业管网热力临界点寻迹系统。

在核心热力管线中，装配有从 1 到 {n} 顺序排列的增压阀门。在当前工况下，存在且仅存在一个特定阀门 M，它是管网中唯一的极限压力峰值（绝对极大值）所在处。

系统的传感器网络会反馈一种状态代码。代码库中包含三种状态符号：{symbol1}、{symbol2}、{symbol3}。当你读取阀门 k 的传感器数据时，系统会根据极限压力峰值 M 与 k 的相对位置返回一个符号：
- 如果极限压力峰值 M 位于当前阀门的上游（M 小于 k），返回某个特定符号
- 如果极限压力峰值 M 恰好位于当前阀门（M 等于 k），返回某个特定符号
- 如果极限压力峰值 M 位于当前阀门的下游（M 大于 k），返回某个特定符号

由于系统传感器固件存在不同的版本，状态符号与相对位置的映射机制分为四种可能的方案（方案 A、B、C、D）。系统启动时已默认加载了其中一种方案并全程保持锁定。你需要通过多次读取传感器，推断出当前生效的映射方案，并精确定位极限压力峰值 M。

你的目标是用尽可能少的数据读取次数，同时正确确定：
1. 传感器固件的映射方案（A、B、C 或 D）
2. 极限压力峰值所在的阀门编号 M

每次读取数据时，使用以下 XML 格式指定一个阀门编号：

<query_position>k</query_position>

其中 k 是你要读取数据的阀门编号（1 到 {n} 之间的整数）。

提交最终巡检结论时，必须同时给出方案编号和峰值阀门位置，格式如下：

<answer>scheme=A, position=5</answer>

其中 scheme 可以是 A、B、C 或 D，position 是你推断的压力峰值阀门编号。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Industrial Thermal Pipeline Critical Point Tracking System.

Along the core thermal pipeline, there are sequentially ordered pressure valves numbered from 1 to {n}. Under the current operating conditions, there exists exactly one specific valve M, which is the unique critical pressure peak (absolute maximum) in the pipeline network.

The system's sensor network feeds back a status code. The code repository contains three status symbols: {symbol1}, {symbol2}, {symbol3}. When you read the sensor data at valve k, the system returns a symbol based on the relative physical position of the critical pressure peak M to k:
- If the critical pressure peak M is upstream of the current valve (M is less than k), it returns a specific symbol
- If the critical pressure peak M is exactly at the current valve (M equals k), it returns a specific symbol
- If the critical pressure peak M is downstream of the current valve (M is greater than k), it returns a specific symbol

Due to varying sensor firmware versions, the mapping mechanism between status symbols and relative positions falls into four possible schemes (schemes A, B, C, D). A specific scheme was loaded by default at system startup and remains locked throughout. You need to infer the active mapping scheme and precisely locate the critical pressure peak M through sensor readings.

Your goal is to correctly determine both, using as few data readings as possible:
1. The sensor firmware's mapping scheme (A, B, C, or D)
2. The critical pressure peak valve position M

For each data reading, use the following XML format to specify a valve number:

<query_position>k</query_position>

where k is the valve number you want to read (an integer between 1 and {n}).

When submitting the final inspection conclusion, you must provide both the scheme identifier and the peak valve position, using this format:

<answer>scheme=A, position=5</answer>

where scheme can be A, B, C, or D, and position is your inferred critical pressure peak valve number.
"""

    contextualized_rule_zh_5 = """\
欢迎使用智能合同链合规审计系统。

在本次审查的商业案件中，有一批按时间顺序排列的连环交易记录，编号从 1 到 {n}。系统初审判定，在这批记录中，存在且仅存在一条交易 M，它是整个合同链條中的核心欺诈异常峰值（风险极值）。

审计系统内置了一个智能探针反馈引擎。反馈引擎输出三种审计标签符号：{symbol1}、{symbol2}、{symbol3}。当你审查交易记录 k 时，引擎会根据核心异常峰值 M 的发生时间与 k 的先后关系返回一个符号：
- 如果核心异常峰值 M 发生在审查记录之前（M 小于 k），返回某个特定符号
- 如果核心异常峰值 M 正好是当前审查的记录（M 等于 k），返回某个特定符号
- 如果核心异常峰值 M 发生在审查记录之后（M 大于 k），返回某个特定符号

由于系统底层合规算法库的迭代差异，审计标签与时间先后的映射规则共有四种方案（方案 A、B、C、D）。本案审计立卷时随机固定了一种方案。你需要通过调阅记录来推断出该案采用的算法映射方案，并锁定核心异常峰值的交易编号 M。

你的目标是用尽可能少的审查次数，同时正确确定：
1. 审计引擎使用的映射方案（A、B、C 或 D）
2. 核心欺诈异常峰值交易位置 M

每次审查时，使用以下 XML 格式指定一条交易记录编号：

<query_position>k</query_position>

其中 k 是你要审查的记录编号（1 到 {n} 之间的整数）。

提交最终取证结论时，必须同时给出方案编号和异常交易位置，格式如下：

<answer>scheme=A, position=5</answer>

其中 scheme 可以是 A、B、C 或 D，position 是你推断的核心异常峰值交易编号。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the Smart Contract Chain Compliance Audit System.

In the commercial case currently under review, there is a chronologically ordered chain of transaction records numbered from 1 to {n}. Initial audits dictate that within these records, there exists exactly one transaction M, representing the core fraudulent anomaly peak (risk maximum) of the entire contract chain.

The audit system incorporates a smart probe feedback engine yielding three audit tag symbols: {symbol1}, {symbol2}, {symbol3}. When you audit transaction record k, the engine returns a symbol based on the chronological sequence of the core anomaly peak M relative to k:
- If the core anomaly peak M occurred before the audited record (M is less than k), it returns a specific symbol
- If the core anomaly peak M is exactly the current audited record (M equals k), it returns a specific symbol
- If the core anomaly peak M occurred after the audited record (M is greater than k), it returns a specific symbol

Due to iterations in the system's underlying compliance algorithm library, there are four schemes for mapping audit tags to chronological sequences (schemes A, B, C, D). A specific scheme was randomly locked in when this case file was opened. You need to infer the algorithmic mapping scheme used for this case and pinpoint the core anomaly peak transaction M through record queries.

Your goal is to correctly determine both, using as few audits as possible:
1. The mapping scheme used by the audit engine (A, B, C, or D)
2. The core fraudulent anomaly peak transaction position M

For each audit query, use the following XML format to specify a transaction record number:

<query_position>k</query_position>

where k is the transaction record number you want to audit (an integer between 1 and {n}).

When submitting your final evidentiary conclusion, you must provide both the scheme identifier and the anomalous transaction position, using this format:

<answer>scheme=A, position=5</answer>

where scheme can be A, B, C, or D, and position is your inferred core anomaly peak transaction number.
"""

    tags = ["answer", "query_position"]
    
    reasoning_type = "溯因推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "symbols": ["L", "R", "E"],
                "M": 3,
                "scheme": "A",
            },
            2: {
                "n": 8,
                "symbols": ["α", "β", "γ"],
                "M": 6,
                "scheme": "B",
            },
            3: {
                "n": 12,
                "symbols": ["△", "▽", "◇"],
                "M": 7,
                "scheme": "C",
            },
            4: {
                "n": 15,
                "symbols": ["↓", "↑", "○"],
                "M": 10,
                "scheme": "D",
            },
            5: {
                "n": 20,
                "symbols": ["1", "2", "3"],
                "M": 13,
                "scheme": "A",
            },
        },
        "en": {
            1: {
                "n": 5,
                "symbols": ["L", "R", "E"],
                "M": 3,
                "scheme": "A",
            },
            2: {
                "n": 8,
                "symbols": ["α", "β", "γ"],
                "M": 6,
                "scheme": "B",
            },
            3: {
                "n": 12,
                "symbols": ["△", "▽", "◇"],
                "M": 7,
                "scheme": "C",
            },
            4: {
                "n": 15,
                "symbols": ["↓", "↑", "○"],
                "M": 10,
                "scheme": "D",
            },
            5: {
                "n": 20,
                "symbols": ["1", "2", "3"],
                "M": 13,
                "scheme": "A",
            },
        },
    }

    SCHEMES = {
        "A": {"less": 0, "greater": 1, "equal": 2},
        "B": {"less": 1, "greater": 0, "equal": 2},
        "C": {"less": 2, "greater": 1, "equal": 0},
        "D": {"less": 0, "greater": 2, "equal": 1},
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
        
        n = cfg["n"]
        self.M = cfg["M"]
        self.scheme = cfg["scheme"]
        
        self._game_info["n"] = n
        self.symbols = cfg["symbols"]
        self._game_info["symbol1"] = self.symbols[0]
        self._game_info["symbol2"] = self.symbols[1]
        self._game_info["symbol3"] = self.symbols[2]
        
        if not (1 <= self.M <= n):
            raise ValueError(f"Invalid M position: {self.M}")

    def _get_symbol_for_relation(self, relation):
        symbol_idx = self.SCHEMES[self.scheme][relation]
        return self.symbols[symbol_idx]

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        for kv in kv_pairs:
            if "=" not in kv:
                continue
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "scheme" not in ans_dict or "position" not in ans_dict:
            return False
        
        if ans_dict["scheme"].upper() != self.scheme:
            return False
        
        try:
            predicted_M = int(ans_dict["position"])
        except ValueError:
            return False
            
        return predicted_M == self.M

    def _cf_core_produce(self, parsed_info):
        if "query_position" not in parsed_info:
            if self.config.language == "zh":
                return "错误：无效的查询标签。"
            else:
                return "Error: Invalid query tag."
        
        try:
            k = int(parsed_info["query_position"].strip())
        except ValueError:
            if self.config.language == "zh":
                return "错误：位置必须是整数。"
            else:
                return "Error: Position must be an integer."
        
        if not (1 <= k <= self._game_info["n"]):
            if self.config.language == "zh":
                return f"错误：位置必须在 1 到 {self._game_info['n']} 之间。"
            else:
                return f"Error: Position must be between 1 and {self._game_info['n']}."
        
        if self.M < k:
            relation = "less"
        elif self.M == k:
            relation = "equal"
        else:
            relation = "greater"
        
        symbol = self._get_symbol_for_relation(relation)
        return symbol

    def _cf_make_wrong(self, correct: str) -> str:
        for s in self.symbols:
            if s != correct:
                return s
        return f"{correct}_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        n = self._game_info["n"]
        for k in range(1, n + 1):
            if self.M < k:
                relation = "less"
            elif self.M == k:
                relation = "equal"
            else:
                relation = "greater"
            
            symbol = self._get_symbol_for_relation(relation)
            
            results.append({
                "query": f"<query_position>{k}</query_position>",
                "answer": symbol
            })
        return results