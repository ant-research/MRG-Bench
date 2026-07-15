from .base import Game
import random

class SubsetDeductionGame(Game):

    game_rule_zh = """\
我们来玩一个"子集推理"游戏，规则如下：

游戏设定了一个全集 Ω，包含编号从 1 到 {n} 的所有元素。我已经秘密选定了一个目标子集 U（U 是 Ω 的子集，可能为空集、全集或任意子集）。

你的目标是通过查询推断出这个目标子集 U 中包含哪些元素。你可以进行以下两种操作：

1. **差距查询**：提交一个候选子集 S（通过列举其中的元素编号），系统会返回一个非负整数 d，表示你提交的子集 S 与目标子集 U 之间的"差距大小"。具体而言，d 等于"仅在 S 中出现的元素数量"加上"仅在 U 中出现的元素数量"。
   
2. **最终答案提交**：当你确信已经推断出目标子集 U 时，提交你的答案。如果答案完全正确则游戏成功，否则游戏失败。

请尽可能用最少的查询次数找到目标子集。

- **差距查询**（例如查询子集包含元素 1, 3, 5）：
<query_diff>1,3,5</query_diff>

如果查询空集，内容留空：
<query_diff></query_diff>

- **最终答案提交**（例如目标子集为 2, 4, 6）：
<answer>2,4,6</answer>

如果答案是空集，内容留空：
<answer></answer>

注意：
- 元素编号之间用英文逗号分隔，不要有多余空格
- 编号顺序不影响结果
- 每次只能进行一个操作（查询或提交答案）
"""

    game_rule_en = """\
Let's play a "Subset Deduction" game. Here are the rules:

The game defines a universal set Ω containing all elements numbered from 1 to {n}. I have secretly selected a target subset U (U is a subset of Ω, which could be empty, the full set, or any subset in between).

Your goal is to deduce which elements are in the target subset U through queries. You can perform two types of operations:

1. **Difference Query**: Submit a candidate subset S (by listing the element IDs it contains). The system will return a non-negative integer d representing the "difference size" between your submitted subset S and the target subset U. Specifically, d equals the number of elements that appear only in S plus the number of elements that appear only in U.

2. **Final Answer Submission**: When you are confident you have deduced the target subset U, submit your answer. If the answer is completely correct, the game succeeds; otherwise, it fails.

Try to find the target subset with as few queries as possible.

- **Difference Query** (e.g., querying subset containing elements 1, 3, 5):
<query_diff>1,3,5</query_diff>

To query the empty set, leave content empty:
<query_diff></query_diff>

- **Final Answer Submission** (e.g., target subset is 2, 4, 6):
<answer>2,4,6</answer>

If the answer is the empty set, leave content empty:
<answer></answer>

Notes:
- Separate element IDs with commas, no extra spaces
- Order of IDs does not matter
- Only one operation (query or answer) per turn
"""

    contextualized_rule_zh_1 = """\
【交通网络维护系统】
市中心区域共有 {n} 个关键交通路口监控摄像头（编号从 1 到 {n}）。其中有未知数量的摄像头发生了硬件故障（目标子集 U，可能全空、全满或任意部分）。
作为交通系统调度员，你的目标是通过诊断查询推断出所有故障摄像头的编号。

你可以进行以下两种操作：
1. **诊断派单**：向维修团队提交一个排查名单 S（列出怀疑故障的摄像头编号）。系统会自动返回一个偏差值 d，代表名单的“失误总数”。具体而言，d 等于你派人排查但实际正常的摄像头数量，加上实际故障但你没有派人排查的摄像头数量。
2. **最终结案**：当你确定了所有真正故障的摄像头时，提交你的最终故障名单。如果完全正确则成功排除隐患，否则游戏失败。

请用尽可能少的派单次数找到目标子集。

- **诊断派单**（例如派单检查 1, 3, 5 号摄像头）：
<query_diff>1,3,5</query_diff>

如果提交空名单，内容留空：
<query_diff></query_diff>

- **最终结案**（例如确定 2, 4, 6 号摄像头故障）：
<answer>2,4,6</answer>

如果确定没有故障摄像头，内容留空：
<answer></answer>

注意：
- 元素编号之间用英文逗号分隔，不要有多余空格
- 编号顺序不影响结果
- 每次只能进行一个操作（查询或提交答案）
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
There are {n} critical traffic intersection cameras (numbered 1 to {n}) in the downtown area. An unknown subset of them has experienced hardware malfunctions (the target subset U, which could be any combination).
As the traffic system dispatcher, your goal is to deduce the exact subset of malfunctioning cameras through diagnostic queries.

You can perform two operations:
1. **Diagnostic Dispatch**: Submit an inspection list S (the camera IDs you suspect are faulty). The system returns a Deviation Value d, representing the total number of "errors" in your list. Specifically, d equals the number of normal cameras you unnecessarily inspected, plus the number of actually malfunctioning cameras you missed.
2. **Final Resolution**: When you are confident about the exact malfunctioning cameras, submit the final list. If completely correct, the game succeeds; otherwise, it fails.

Try to find the target subset with as few queries as possible.

- **Diagnostic Dispatch** (e.g., inspecting cameras 1, 3, 5):
<query_diff>1,3,5</query_diff>

To submit an empty list, leave content empty:
<query_diff></query_diff>

- **Final Resolution** (e.g., cameras 2, 4, 6 are faulty):
<answer>2,4,6</answer>

If no cameras are faulty, leave content empty:
<answer></answer>

Notes:
- Separate element IDs with commas, no extra spaces
- Order of IDs does not matter
- Only one operation (query or answer) per turn
"""

    contextualized_rule_zh_2 = """\
【医疗免疫系统分析】
患者暴露于环境中的 {n} 种潜在过敏原（编号从 1 到 {n}），其免疫系统对其中一个特定的过敏原组合（目标子集 U）产生了排斥反应。
作为主治医师，你的目标是通过定制靶向药物测试，精准推断出所有引发排斥的过敏原。

你可以进行以下两种操作：
1. **靶向药物测试**：提交一个针对特定过敏原的抑制药物配方 S（包含过敏原编号）。血液样本会反馈一个“不匹配指数 d”。具体而言，d 等于配方中包含了但患者实际上不过敏的成分数量（过度用药），加上患者实际过敏但配方中未包含的成分数量（治疗遗漏）。
2. **最终确诊**：当你确信找出了所有导致排斥的过敏原时，提交最终的诊断结果。如果答案完全正确则游戏成功，否则游戏失败。

请用尽可能少的测试次数找到目标子集。

- **靶向药物测试**（例如测试针对 1, 3, 5 号的药物）：
<query_diff>1,3,5</query_diff>

如果测试安慰剂（空配方），内容留空：
<query_diff></query_diff>

- **最终确诊**（例如确诊为 2, 4, 6 号过敏原）：
<answer>2,4,6</answer>

如果患者没有任何过敏原，内容留空：
<answer></answer>

注意：
- 元素编号之间用英文逗号分隔，不要有多余空格
- 编号顺序不影响结果
- 每次只能进行一个操作（查询或提交答案）
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
A patient is exposed to {n} potential environmental allergens (numbered 1 to {n}). Their immune system is reacting to a specific combination of them (the target subset U).
As the attending physician, your goal is to deduce the exact triggering allergens through customized targeted drug tests.

You can perform two operations:
1. **Targeted Drug Test**: Submit a suppressive medication formula S targeting a specific subset of allergens. The blood sample will return a "Mismatch Index" d. Specifically, d equals the number of allergens targeted by your drug that the patient is NOT allergic to (over-treatment), plus the number of actual triggering allergens your drug failed to target (under-treatment).
2. **Final Diagnosis**: When you are certain of the exact combination of allergens, submit your final diagnosis. If completely correct, the game succeeds; otherwise, it fails.

Try to find the target subset with as few queries as possible.

- **Targeted Drug Test** (e.g., testing drug for allergens 1, 3, 5):
<query_diff>1,3,5</query_diff>

To test a placebo (empty formula), leave content empty:
<query_diff></query_diff>

- **Final Diagnosis** (e.g., diagnosing allergens 2, 4, 6):
<answer>2,4,6</answer>

If no allergens are triggering, leave content empty:
<answer></answer>

Notes:
- Separate element IDs with commas, no extra spaces
- Order of IDs does not matter
- Only one operation (query or answer) per turn
"""

    contextualized_rule_zh_3 = """\
【教育自适应学习系统】
本学期的核心知识图谱包含 {n} 个关键知识点（编号从 1 到 {n}）。某位学生存在一个未掌握的知识点盲区（目标子集 U）。
作为 AI 导师，你的目标是通过推送专项练习来推断出该学生的真实薄弱环节。

你可以进行以下两种操作：
1. **推送专项练习**：为学生生成一份包含特定知识点集合 S 的测试卷。系统批改后会返回一个“低效分数 d”。具体而言，d 等于试卷中包含了但学生已经掌握的知识点数量（无效复习），加上学生尚未掌握但试卷中遗漏的知识点数量（未检测出的盲区）。
2. **生成学情报告**：当你精确定位了所有未掌握的知识点后，提交最终结论。如果答案完全正确则游戏成功，否则游戏失败。

请用尽可能少的测试次数找到目标子集。

- **推送专项练习**（例如考察 1, 3, 5 号知识点）：
<query_diff>1,3,5</query_diff>

如果不考察任何知识点，内容留空：
<query_diff></query_diff>

- **生成学情报告**（例如学生未掌握 2, 4, 6 号）：
<answer>2,4,6</answer>

如果学生已全部掌握，内容留空：
<answer></answer>

注意：
- 元素编号之间用英文逗号分隔，不要有多余空格
- 编号顺序不影响结果
- 每次只能进行一个操作（查询或提交答案）
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
This semester's core knowledge graph contains {n} key concepts (numbered 1 to {n}). A student has a specific blind spot of unmastered concepts (the target subset U).
As the AI tutor, your goal is to deduce the student's exact weaknesses by assigning targeted practice quizzes.

You can perform two operations:
1. **Assign Targeted Practice**: Generate a quiz covering a specific subset of concepts S. The system returns an "Inefficiency Score" d. Specifically, d equals the number of concepts in the quiz that the student has already mastered (redundant review), plus the number of unmastered concepts that were omitted from the quiz (missed blind spots).
2. **Generate Learning Report**: Once you have precisely identified all unmastered concepts, submit your final conclusion. If completely correct, the game succeeds; otherwise, it fails.

Try to find the target subset with as few queries as possible.

- **Assign Targeted Practice** (e.g., testing concepts 1, 3, 5):
<query_diff>1,3,5</query_diff>

For an empty quiz, leave content empty:
<query_diff></query_diff>

- **Generate Learning Report** (e.g., unmastered concepts are 2, 4, 6):
<answer>2,4,6</answer>

If all concepts are mastered, leave content empty:
<answer></answer>

Notes:
- Separate element IDs with commas, no extra spaces
- Order of IDs does not matter
- Only one operation (query or answer) per turn
"""

    contextualized_rule_zh_4 = """\
【工业产线排障系统】
一条高精度自动化装配线由 {n} 个核心工站（编号从 1 到 {n}）组成。由于未知原因，部分工站发生了隐蔽的参数偏移（目标子集 U）。
作为首席工程师，你的目标是通过局部重置来推断出所有发生偏移的工站。

你可以进行以下两种操作：
1. **局部重置诊断**：选定一个工站集合 S 并向其发送重置指令。主控台将返回一个“偏差基数 d”。具体而言，d 等于被你不必要地重置的正常工站数量，加上仍在运行且存在参数偏移的故障工站数量。
2. **提交维护工单**：在你完全确认了所有存在偏移的工站后，提交最终的工单。如果答案完全正确则游戏成功，否则游戏失败。

请用尽可能少的诊断次数找到目标子集。

- **局部重置诊断**（例如重置 1, 3, 5 号工站）：
<query_diff>1,3,5</query_diff>

如果发送空指令，内容留空：
<query_diff></query_diff>

- **提交维护工单**（例如 2, 4, 6 号工站偏移）：
<answer>2,4,6</answer>

如果没有任何工站偏移，内容留空：
<answer></answer>

注意：
- 元素编号之间用英文逗号分隔，不要有多余空格
- 编号顺序不影响结果
- 每次只能进行一个操作（查询或提交答案）
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
A high-precision automated assembly line consists of {n} core stations (numbered 1 to {n}). For unknown reasons, a subset of stations has experienced hidden parameter deviations (the target subset U).
As the chief engineer, your goal is to deduce all deviated stations through partial resets.

You can perform two operations:
1. **Partial Reset Diagnostic**: Select a subset of stations S and send a reset command. The console will return a "Variance Base d". Specifically, d equals the number of normal stations you unnecessarily reset, plus the number of deviated stations you left running.
2. **Submit Maintenance Order**: Once you have confirmed the exact deviated stations, submit the final order. If completely correct, the game succeeds; otherwise, it fails.

Try to find the target subset with as few queries as possible.

- **Partial Reset Diagnostic** (e.g., resetting stations 1, 3, 5):
<query_diff>1,3,5</query_diff>

For an empty command, leave content empty:
<query_diff></query_diff>

- **Submit Maintenance Order** (e.g., stations 2, 4, 6 are deviated):
<answer>2,4,6</answer>

If no stations are deviated, leave content empty:
<answer></answer>

Notes:
- Separate element IDs with commas, no extra spaces
- Order of IDs does not matter
- Only one operation (query or answer) per turn
"""

    contextualized_rule_zh_5 = """\
【法律卷宗审查系统】
在一起复杂的商业合同纠纷中，法典库中共有 {n} 条可能相关的法条（编号从 1 到 {n}）。实际上，只有其中一个特定的法条组合（目标子集 U）能作为最终判决的绝对依据。
作为资深律师，你的目标是通过提交初步案情分析来推导出这套关键法条。

你可以进行以下两种操作：
1. **提交初步分析**：向高级合伙人提交一份引用了特定法条集合 S 的分析报告。合伙人审阅后会给出一个“偏离指数 d”。具体而言，d 等于你引用了但实际上不适用的法条数量，加上实际适用但你未能引用的法条数量。
2. **正式出具法律意见书**：当你确切推断出所有适用的核心法条时，提交你的最终意见书。如果答案完全正确则游戏成功，否则游戏失败。

请用尽可能少的分析次数找到目标子集。

- **提交初步分析**（例如引用法条 1, 3, 5）：
<query_diff>1,3,5</query_diff>

如果不引用任何法条，内容留空：
<query_diff></query_diff>

- **正式出具法律意见书**（例如适用法条为 2, 4, 6）：
<answer>2,4,6</answer>

如果无法条适用，内容留空：
<answer></answer>

注意：
- 元素编号之间用英文逗号分隔，不要有多余空格
- 编号顺序不影响结果
- 每次只能进行一个操作（查询或提交答案）
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
In a complex commercial contract dispute, there are {n} potentially relevant legal clauses (numbered 1 to {n}). In reality, only a specific combination of them (the target subset U) serves as the absolute basis for the final ruling.
As a senior lawyer, your goal is to deduce this exact set of key clauses by submitting preliminary case analyses.

You can perform two operations:
1. **Submit Preliminary Analysis**: Submit a brief citing a specific subset of clauses S. The senior partner will provide a "Deviation Index d". Specifically, d equals the number of irrelevant clauses you cited, plus the number of applicable clauses you failed to cite.
2. **Issue Formal Legal Opinion**: When you have deduced the exact core applicable clauses, submit your final opinion. If completely correct, the game succeeds; otherwise, it fails.

Try to find the target subset with as few queries as possible.

- **Submit Preliminary Analysis** (e.g., citing clauses 1, 3, 5):
<query_diff>1,3,5</query_diff>

For an empty citation, leave content empty:
<query_diff></query_diff>

- **Issue Formal Legal Opinion** (e.g., applicable clauses are 2, 4, 6):
<answer>2,4,6</answer>

If no clauses apply, leave content empty:
<answer></answer>

Notes:
- Separate element IDs with commas, no extra spaces
- Order of IDs does not matter
- Only one operation (query or answer) per turn
"""

    tags = ["answer", "query_diff"]
    reasoning_type = "演绎推理"
    data_structure = "集合"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"n": 5, "size_range": (1, 2)},
            2: {"n": 8, "size_range": (2, 4)},
            3: {"n": 10, "size_range": (3, 5)},
            4: {"n": 12, "size_range": (4, 6)},
            5: {"n": 15, "size_range": (5, 8)},
        },
        "en": {
            1: {"n": 5, "size_range": (1, 2)},
            2: {"n": 8, "size_range": (2, 4)},
            3: {"n": 10, "size_range": (3, 5)},
            4: {"n": 12, "size_range": (4, 6)},
            5: {"n": 15, "size_range": (5, 8)},
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
        n = cfg["n"]
        self._game_info["n"] = n
        
        self.universal_set = set(str(i) for i in range(1, n + 1))
        
        lo, hi = cfg["size_range"]
        
        seed = getattr(self.config, 'seed', 42)
        rng = random.Random(seed)
        subset_size = rng.randint(lo, hi)
        elements = list(range(1, n + 1))
        chosen = rng.sample(elements, subset_size)
        self.target_subset = set(str(x) for x in chosen)

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        if raw_ans:
            try:
                submitted_set = set(x.strip() for x in raw_ans.split(",") if x.strip())
            except:
                return False
        else:
            submitted_set = set()
        
        if not submitted_set.issubset(self.universal_set):
            return False
        
        return submitted_set == self.target_subset

    def _cf_core_produce(self, parsed_info):
        if "query_diff" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        raw_query = parsed_info["query_diff"].strip()
        
        if raw_query:
            queried_set = set(x.strip() for x in raw_query.split(",") if x.strip())
            for elem in queried_set:
                if not elem.isdigit():
                    raise ValueError(f"Invalid element in query: '{elem}'")
        else:
            queried_set = set()
        
        if not queried_set.issubset(self.universal_set):
            invalid = queried_set - self.universal_set
            raise ValueError(f"Query contains element IDs out of range: {invalid}")
        
        symmetric_diff = self.target_subset.symmetric_difference(queried_set)
        diff_size = len(symmetric_diff)
        
        return str(diff_size)

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            val = int(correct)
            n = len(self.universal_set)
            if val < n:
                return str(val + 1)
            else:
                return str(val - 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        else:
            low_correct = correct.lower()
            if "yes" in low_correct:
                return correct.replace("Yes", "No").replace("yes", "no").replace("YES", "NO")
            elif "no" in low_correct:
                return correct.replace("No", "Yes").replace("no", "yes").replace("NO", "YES")
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        elements = sorted(list(self.universal_set), key=lambda x: int(x))
        results = []
        
        queried_set = set()
        diff_size = len(self.target_subset.symmetric_difference(queried_set))
        results.append({
            "query": "<query_diff></query_diff>",
            "answer": str(diff_size)
        })
        
        for elem in elements:
            queried_set = {elem}
            diff_size = len(self.target_subset.symmetric_difference(queried_set))
            results.append({
                "query": f"<query_diff>{elem}</query_diff>",
                "answer": str(diff_size)
            })
        
        return results

