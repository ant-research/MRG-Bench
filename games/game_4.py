# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 集合：存在一个由N个物体组成的集合，注意他们不存在位置、前后和大小关系。
# 知识点:   集合规模：集合中元素的总数量
# ============================================================

import random
from .base import Game

class NumberDeductionGame(Game):

    game_rule_zh = """\
我们现在来玩一个"数字推理"游戏，规则如下：

游戏设定了一个未知整数 N，范围为 1 到 120（包含端点）。你的目标是通过提问推断出这个数字。

你可以向我提出以下两类问题，每次仅限一个问题：

1. 余数查询：询问 N 除以某个整数 g（g 的范围为 2 到 12，包含端点）的余数是多少。我会回答一个 0 到 g 减 1 之间的整数 r，表示 N 除以 g 的余数为 r。

2. 可整除查询：询问 N 是否能被某个整数 g（g 的范围为 2 到 12，包含端点）整除。我会回答"能"或"不能"。

你需要在尽可能少的查询次数内确定 N 的值，然后提交最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 余数查询（例如询问除以 7 的余数）：
<query_mod>7</query_mod>

- 可整除查询（例如询问是否能被 5 整除）：
<query_div>5</query_div>

提交最终答案时，直接给出你推断的数字（1 到 120 之间的整数），格式如下：

<answer>42</answer>
"""

    game_rule_en = """\
Let's play a "Number Deduction" game. Here are the rules:

There is an unknown integer N in the range from 1 to 120 (inclusive). Your goal is to deduce this number through queries.

You can ask me two types of questions, one at a time:

1. Modulo Query: Ask for the remainder when N is divided by an integer g (g ranges from 2 to 12, inclusive). I will answer with an integer r between 0 and g minus 1, indicating that N modulo g equals r.

2. Divisibility Query: Ask whether N is divisible by an integer g (g ranges from 2 to 12, inclusive). I will answer "Yes" or "No".

You need to determine the value of N with as few queries as possible, then submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Modulo Query (e.g., asking for remainder when divided by 7):
<query_mod>7</query_mod>

- Divisibility Query (e.g., asking if divisible by 5):
<query_div>5</query_div>

When submitting the final answer, provide the number you deduced (an integer between 1 and 120), using this format:

<answer>42</answer>
"""

    contextualized_rule_zh_1 = """\
智能交通管理系统正在排查某一路段发生违规行为的肇事车辆。车辆编号 N 的范围为 1 到 120（包含端点）。你的目标是通过系统查询推断出这个编号。

你可以向系统提出以下两类查询，每次仅限一个查询：

1. 余数查询：询问将车辆编号 N 按 g（g 的范围为 2 到 12，包含端点）辆车一组通过收费站时的余数排位。系统会回答一个 0 到 g 减 1 之间的整数 r，表示 N 除以 g 的余数为 r。

2. 可整除查询：询问车辆编号 N 是否能被指定的通行波次参数 g（g 的范围为 2 到 12，包含端点）整除。系统会回答"能"或"不能"。

你需要在尽可能少的查询次数内确定肇事车辆编号 N 的值，然后提交最终结果。若答案错误或格式不符，排查失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 余数查询（例如询问参数 7 的余数）：
<query_mod>7</query_mod>

- 可整除查询（例如询问是否能被 5 整除）：
<query_div>5</query_div>

提交最终答案时，直接给出你推断的车辆编号（1 到 120 之间的整数），格式如下：

<answer>42</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
An intelligent traffic management system is tracking down a hit-and-run vehicle. The vehicle identification number N is between 1 and 120 (inclusive). Your goal is to deduce this number through system queries.

You can ask the system two types of queries, one at a time:

1. Modulo Query: Ask for the remainder when the vehicle number N is grouped by g vehicles (g ranges from 2 to 12, inclusive) passing a toll booth. The system will answer with an integer r between 0 and g minus 1, indicating that N modulo g equals r.

2. Divisibility Query: Ask whether the vehicle number N is divisible by a specific traffic wave parameter g (g ranges from 2 to 12, inclusive). The system will answer "Yes" or "No".

You need to determine the value of N with as few queries as possible, then submit your final answer. If the answer is wrong or the format is invalid, the investigation fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Modulo Query (e.g., asking for remainder with parameter 7):
<query_mod>7</query_mod>

- Divisibility Query (e.g., asking if divisible by 5):
<query_div>5</query_div>

When submitting the final answer, provide the vehicle number you deduced (an integer between 1 and 120), using this format:

<answer>42</answer>
"""

    contextualized_rule_zh_2 = """\
传染病防控中心正在定位一种新型病原体的专属毒株编号 N。该编号的范围为 1 到 120（包含端点）。你的目标是通过实验查询推断出这个编号。

你可以向实验系统提出以下两类查询，每次仅限一个查询：

1. 余数查询：询问该毒株在均分注入 g（g 的范围为 2 到 12，包含端点）个培养皿阵列时的残留毒株数量。系统会回答一个 0 到 g 减 1 之间的整数 r，表示 N 除以 g 的余数为 r。

2. 可整除查询：询问该毒株编号 N 是否能在 g（g 的范围为 2 到 12，包含端点）次试验周期内发生完全同构裂变（即 N 能否被 g 整除）。系统会回答"能"或"不能"。

你需要在尽可能少的查询次数内确定毒株编号 N 的值，然后提交最终结果。若答案错误或格式不符，定位失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 余数查询（例如询问注入 7 个培养皿的残留）：
<query_mod>7</query_mod>

- 可整除查询（例如询问是否能在 5 个周期内裂变）：
<query_div>5</query_div>

提交最终答案时，直接给出你推断的毒株编号（1 到 120 之间的整数），格式如下：

<answer>42</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
The Center for Disease Control is isolating a specific strain of a novel pathogen with a unique ID number N. The ID ranges from 1 to 120 (inclusive). Your goal is to deduce this ID through experimental queries.

You can submit two types of experimental queries to the system, one at a time:

1. Modulo Query: Ask for the residual strain count when the strain is equally divided into an array of g petri dishes (g ranges from 2 to 12, inclusive). The system will return an integer r between 0 and g minus 1, indicating that N modulo g equals r.

2. Divisibility Query: Ask whether the strain ID N can achieve perfect isomorphic fission over g experimental cycles (i.e., whether N is divisible by g, where g ranges from 2 to 12, inclusive). The system will answer "Yes" or "No".

You need to determine the value of N with as few queries as possible, then submit your final answer. If the answer is wrong or the format is invalid, the isolation fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Modulo Query (e.g., asking for remainder with 7 petri dishes):
<query_mod>7</query_mod>

- Divisibility Query (e.g., asking if divisible by 5 cycles):
<query_div>5</query_div>

When submitting the final answer, provide the strain ID you deduced (an integer between 1 and 120), using this format:

<answer>42</answer>
"""

    contextualized_rule_zh_3 = """\
学校档案系统崩溃，你需要找回一名失踪学生的唯一学籍档案号 N。该档案号的范围为 1 到 120（包含端点）。你的目标是通过档案检索终端推断出这个号码。

你可以向终端提出以下两类检索，每次仅限一个检索：

1. 余数查询：询问将该学籍号按 g（g 的范围为 2 到 12，包含端点）个班级进行哈希分配时，最后未能平均分配的哈希余值。终端会回答一个 0 到 g 减 1 之间的整数 r，表示 N 除以 g 的余数为 r。

2. 可整除查询：询问该档案号 N 是否能被完美映射进拥有 g（g 的范围为 2 到 12，包含端点）个课外活动小组的子系统中（即 N 能否被 g 整除）。终端会回答"能"或"不能"。

你需要在尽可能少的查询次数内确定学籍档案号 N 的值，然后提交最终结果。若答案错误或格式不符，找回失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 余数查询（例如询问分配到 7 个班级的余值）：
<query_mod>7</query_mod>

- 可整除查询（例如询问是否能映射到 5 个小组）：
<query_div>5</query_div>

提交最终答案时，直接给出你推断的学籍档案号（1 到 120 之间的整数），格式如下：

<answer>42</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The school's archive system has crashed, and you need to recover a missing student's unique enrollment ID N. The ID ranges from 1 to 120 (inclusive). Your goal is to deduce this ID through the archive retrieval terminal.

You can submit two types of retrieval queries to the terminal, one at a time:

1. Modulo Query: Ask for the hash remainder when the enrollment ID is allocated across g classes (g ranges from 2 to 12, inclusive). The terminal will return an integer r between 0 and g minus 1, indicating that N modulo g equals r.

2. Divisibility Query: Ask whether the enrollment ID N can be perfectly mapped into a subsystem with g extracurricular groups (i.e., whether N is divisible by g, where g ranges from 2 to 12, inclusive). The terminal will answer "Yes" or "No".

You need to determine the value of N with as few queries as possible, then submit your final answer. If the answer is wrong or the format is invalid, the recovery fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Modulo Query (e.g., asking for remainder across 7 classes):
<query_mod>7</query_mod>

- Divisibility Query (e.g., asking if mapped perfectly to 5 groups):
<query_div>5</query_div>

When submitting the final answer, provide the enrollment ID you deduced (an integer between 1 and 120), using this format:

<answer>42</answer>
"""

    contextualized_rule_zh_4 = """\
自动化装配线上有一批精密零件，其中有一个存在微小缺陷，你需要找出这个缺陷零件的流水线序号 N。序号范围为 1 到 120（包含端点）。你的目标是通过质检设备推断出这个序号。

你可以向质检设备输入以下两类指令，每次仅限一个指令：

1. 余数查询：设定质检抽样步长为 g（g 的范围为 2 到 12，包含端点），询问该零件在最后一次抽样批次后剩下的余数位次。设备会回答一个 0 到 g 减 1 之间的整数 r，表示 N 除以 g 的余数为 r。

2. 可整除查询：询问该缺陷零件序号 N 是否能够精准落入步长为 g（g 的范围为 2 到 12，包含端点）的均匀传送带批次中（即 N 能否被 g 整除）。设备会回答"能"或"不能"。

你需要在尽可能少的查询次数内确定缺陷零件序号 N 的值，然后提交最终结果。若答案错误或格式不符，排查失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 余数查询（例如询问步长为 7 的余数位次）：
<query_mod>7</query_mod>

- 可整除查询（例如询问是否能落入步长为 5 的批次中）：
<query_div>5</query_div>

提交最终答案时，直接给出你推断的零件序号（1 到 120 之间的整数），格式如下：

<answer>42</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
There is a batch of precision parts on an automated assembly line, and one of them has a minor defect. You need to identify the assembly line sequence number N of this defective part. The sequence number ranges from 1 to 120 (inclusive). Your goal is to deduce this number using the quality inspection equipment.

You can input two types of commands to the equipment, one at a time:

1. Modulo Query: Set the inspection sampling step size to g (g ranges from 2 to 12, inclusive), and ask for the remainder position of the part after the final sampling batch. The equipment will return an integer r between 0 and g minus 1, indicating that N modulo g equals r.

2. Divisibility Query: Ask whether the defective part sequence number N exactly falls into the uniform conveyor belt batches with a step size of g (i.e., whether N is divisible by g, where g ranges from 2 to 12, inclusive). The equipment will answer "Yes" or "No".

You need to determine the value of N with as few queries as possible, then submit your final answer. If the answer is wrong or the format is invalid, the inspection fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Modulo Query (e.g., asking for remainder with step size 7):
<query_mod>7</query_mod>

- Divisibility Query (e.g., asking if falling into batches of 5):
<query_div>5</query_div>

When submitting the final answer, provide the sequence number you deduced (an integer between 1 and 120), using this format:

<answer>42</answer>
"""

    contextualized_rule_zh_5 = """\
法院在审理一桩复杂的商业纠纷案，需要确定一份被加密隐藏的关键证据文件编号 N。编号的范围为 1 到 120（包含端点）。你的目标是通过法庭调卷系统推断出这个编号。

你可以向系统提出以下两类调卷请求，每次仅限一个请求：

1. 余数查询：询问当全部证据卷宗按 g（g 的范围为 2 到 12，包含端点）个目录柜分组存放时，该文件最后落在柜外的散页偏移量。系统会回答一个 0 到 g 减 1 之间的整数 r，表示 N 除以 g 的余数为 r。

2. 可整除查询：询问该文件编号 N 是否能完美匹配 g（g 的范围为 2 到 12，包含端点）个法庭审查周期的整除规律（即 N 能否被 g 整除）。系统会回答"能"或"不能"。

你需要在尽可能少的请求次数内确定证据文件编号 N 的值，然后提交最终结果。若答案错误或格式不符，取证失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 余数查询（例如询问 7 个目录柜的散页偏移量）：
<query_mod>7</query_mod>

- 可整除查询（例如询问是否匹配 5 个审查周期）：
<query_div>5</query_div>

提交最终答案时，直接给出你推断的文件编号（1 到 120 之间的整数），格式如下：

<answer>42</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
The court is hearing a complex commercial dispute and needs to determine the ID number N of a hidden encrypted key evidence document. The ID ranges from 1 to 120 (inclusive). Your goal is to deduce this ID through the court's document retrieval system.

You can submit two types of retrieval requests to the system, one at a time:

1. Modulo Query: Ask for the loose page offset when all evidence files are grouped into g catalog cabinets (g ranges from 2 to 12, inclusive). The system will return an integer r between 0 and g minus 1, indicating that N modulo g equals r.

2. Divisibility Query: Ask whether the document ID N perfectly matches the divisibility rule of g court review cycles (i.e., whether N is divisible by g, where g ranges from 2 to 12, inclusive). The system will answer "Yes" or "No".

You need to determine the value of N with as few requests as possible, then submit your final answer. If the answer is wrong or the format is invalid, the evidence collection fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Modulo Query (e.g., asking for the offset for 7 catalog cabinets):
<query_mod>7</query_mod>

- Divisibility Query (e.g., asking if perfectly matching 5 review cycles):
<query_div>5</query_div>

When submitting the final answer, provide the document ID you deduced (an integer between 1 and 120), using this format:

<answer>42</answer>
"""

    tags = ["answer", "query_mod", "query_div"]

    # 新增类属性
    reasoning_type = "演绎推理"
    data_structure = "集合"

    # 难度配置说明：
    # 1 (简单)         - N=12,  小数字，多个因子
    # 2 (中等偏下)     - N=35,  中等数字
    # 3 (中等偏上)     - N=77,  较大数字
    # 4 (较难)         - N=97,  质数，难以通过整除查询
    # 5 (难)           - N=119, 大数字，接近上限

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"N": 12},
            2: {"N": 35},
            3: {"N": 77},
            4: {"N": 97},
            5: {"N": 119},
        },
        "en": {
            1: {"N": 12},
            2: {"N": 35},
            3: {"N": 77},
            4: {"N": 97},
            5: {"N": 119},
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏，设置目标数字 N"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保是 int 类型

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.target_number = cfg["N"]
        self.query_count = 0  # 查询计数器
        self.max_queries = 6  # 最大查询次数
        
        # 用于填充规则模板的信息（当前为空，因为规则中不需要动态信息）
        self._game_info = {}

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        try:
            # 解析答案
            raw_ans = parsed_info["answer"].strip()
            guessed_number = int(raw_ans)
            
            # 检查范围
            if guessed_number < 1 or guessed_number > 120:
                return False
            
            # 检查是否等于目标数字
            return guessed_number == self.target_number
            
        except (ValueError, KeyError):
            return False

    def _cf_core_produce(self, parsed_info):
        """原始的产生响应业务逻辑"""
        # 设置语言相关的响应文本
        if self.config.language == "zh":
            yes_res, no_res = "能", "不能"
            error_range = "错误：g 必须在 2 到 12 之间。"
            error_format = "错误：格式无效。"
            error_multiple = "错误：每次仅限提出一个问题。"
            limit_msg = f"已达到最大查询次数限制（{self.max_queries}次）。请立即提交最终答案。"
        else:
            yes_res, no_res = "Yes", "No"
            error_range = "Error: g must be between 2 and 12."
            error_format = "Error: Invalid format."
            error_multiple = "Error: Only one query is allowed at a time."
            limit_msg = f"Maximum query limit ({self.max_queries}) reached. Please submit your final answer now."

        # 检查是否同时包含多个查询标签
        queries_found = [tag for tag in ["query_mod", "query_div"] if tag in parsed_info]
        if len(queries_found) > 1:
            return error_multiple

        # 检查是否超过最大查询次数
        if self.query_count >= self.max_queries:
            if hasattr(self, 'state'):
                self.state.set_state('failed', f'Exceeded max queries limit: {self.max_queries}')
            return limit_msg

        # 处理余数查询
        if "query_mod" in parsed_info:
            self.query_count += 1
            try:
                g = int(parsed_info["query_mod"].strip())
                if g < 2 or g > 12:
                    return error_range
                
                remainder = self.target_number % g
                return str(remainder)
                
            except ValueError:
                return error_format

        # 处理可整除查询
        elif "query_div" in parsed_info:
            self.query_count += 1
            try:
                g = int(parsed_info["query_div"].strip())
                if g < 2 or g > 12:
                    return error_range
                
                is_divisible = (self.target_number % g == 0)
                return yes_res if is_divisible else no_res
                
            except ValueError:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串，与游戏中 parsed_info["query"] 的值格式一致
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        results = []
        
        # 设定语言相关的回答
        if self.config.language == "zh":
            yes_res, no_res = "能", "不能"
        else:
            yes_res, no_res = "Yes", "No"

        # 遍历所有合法的 g 值 (2 到 12)
        # 游戏支持 query_mod 和 query_div 两种查询，这里分别为它们生成对应的条目
        for g in range(2, 13):
            g_str = str(g)
            
            # 1. 余数查询 (query_mod)
            # 逻辑：返回 target_number % g
            remainder = self.target_number % g
            results.append({
                "query": f"<query_mod>{g_str}</query_mod>",
                "answer": str(remainder)
            })
            
            # 2. 可整除查询 (query_div)
            # 逻辑：返回是否能整除
            is_divisible = (self.target_number % g == 0)
            ans_div = yes_res if is_divisible else no_res
            results.append({
                "query": f"<query_div>{g_str}</query_div>",
                "answer": ans_div
            })
            
        return results

    def _cf_make_wrong(self, correct):
        """根据正确答案生成一个明显不同的错误答案"""
        try:
            val = int(correct)
            # 对余数结果，确保生成的错误值与正确值不同
            wrong_val = val + 1 if val < 11 else val - 1
            return str(wrong_val)
        except ValueError:
            pass
        
        if self.config.language == "zh":
            if correct == "能": return "不能"
            if correct == "不能": return "能"
        
        # 英文处理，忽略大小写但保持风格
        if correct.lower() == "yes":
            return "No" if correct[0].isupper() else "no"
        if correct.lower() == "no":
            return "Yes" if correct[0].isupper() else "yes"
            
        return correct + "_WRONG"