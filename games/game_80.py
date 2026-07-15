from .base import Game
import random
import itertools

class SubsetCountingGame(Game):

    game_rule_zh = """\
我们现在来玩一个"子集计数推理"游戏，规则如下：

游戏设定了一个标号集合 L，包含编号 1 到 {n}，以及一个特定的目标元素 T（编号为 {target}）。我已秘密选择了一个目标子集 A，A 是 L 中除 T 之外的某些元素组成的集合（A 可能为空）。

你的目标是精确识别出集合 A 中包含哪些元素。你可以反复向我提出子集计数查询：选择 L 中除 T 之外的任意若干元素组成一个子集 S，询问"S 中有多少个元素属于 A"，我会如实告诉你一个非负整数 k，表示 S 与 A 的交集大小。

当你收集到足够信息后，请提交你推断出的集合 A。若答案完全正确则游戏成功，否则游戏失败。请尽可能用较少的查询次数完成推理。

每次查询时，请使用以下 XML 格式提交一个子集 S（用逗号分隔的编号列表，编号不能包含目标元素 T）：

<query_subset>1,3,5</query_subset>

如果你想查询单个元素是否属于 A，也可以只提交一个编号：

<query_subset>7</query_subset>

提交最终答案时，请列出你认为属于 A 的所有元素编号（用逗号隔开，顺序不限）。如果你认为 A 为空集，请提交空内容：

<answer>2,4,6</answer>

或（如果 A 为空）：

<answer></answer>
"""

    game_rule_en = """\
Let's play a "Subset Counting Inference" game. Here are the rules:

The game defines a labeled set L containing numbers from 1 to {n}, and a specific target element T (numbered {target}). I have secretly selected a target subset A, which consists of some elements from L excluding T (A may be empty).

Your goal is to precisely identify which elements are in set A. You can repeatedly ask me subset counting queries: choose any subset S from L (excluding T), and ask "how many elements in S belong to A". I will truthfully tell you a non-negative integer k, representing the size of the intersection between S and A.

When you have gathered enough information, submit your inferred set A. The game succeeds if and only if your answer is completely correct; otherwise it fails. Please try to complete the inference with as few queries as possible.

For each query, use the following XML format to submit a subset S (a comma-separated list of numbers, excluding the target element T):

<query_subset>1,3,5</query_subset>

If you want to query whether a single element belongs to A, you can submit just one number:

<query_subset>7</query_subset>

When submitting your final answer, list all element numbers you believe belong to A (comma-separated, order does not matter). If you believe A is empty, submit empty content:

<answer>2,4,6</answer>

Or (if A is empty):

<answer></answer>
"""

    contextualized_rule_zh_1 = """\
[交通监控故障排查]
我们现在来玩一个"监控网络故障推理"系统，规则如下：

我们的城市路网部署了一套监控摄像头系统 L，摄像头编号从 1 到 {n}，其中包含一个已确认正常的枢纽主摄像头 T（编号为 {target}）。近期网络中出现了一些信号丢失的情况，我已秘密记录了当前发生故障的摄像头集合 A，A 是系统 L 中除 T 之外的某些摄像头组成的集合（A 可能为空，即全部正常）。

你的目标是精确识别出集合 A 中包含哪些发生故障的摄像头。你可以反复向我提出区域探查查询：选择 L 中除 T 之外的任意若干摄像头组成一个探查组 S，询问"探查组 S 中有多少个摄像头处于故障状态"，我会如实告诉你一个非负整数 k，表示 S 中发生故障的摄像头数量（即 S 与 A 的交集大小）。

当你收集到足够信息后，请提交你推断出的故障摄像头集合 A。若答案完全正确则排查成功，否则任务失败。请尽可能用较少的查询次数完成排查。

每次查询时，请使用以下 XML 格式提交一个探查组 S（用逗号分隔的编号列表，编号不能包含枢纽摄像头 T）：

<query_subset>1,3,5</query_subset>

如果你想单独查询某个监控是否故障，也可以只提交一个编号：

<query_subset>7</query_subset>

提交最终答案时，请列出你认为处于故障状态的所有摄像头编号（用逗号隔开，顺序不限）。如果你认为 A 为空集（全部正常），请提交空内容：

<answer>2,4,6</answer>

或（如果 A 为空）：

<answer></answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's operate the "Surveillance Network Fault Inference" system. Here are the rules:

Our city road network has deployed a surveillance camera system L, with cameras numbered from 1 to {n}. This includes a verified normal hub camera T (numbered {target}). Recently, there have been some signal losses. I have secretly recorded the current set of faulty cameras A, which consists of some cameras from L excluding T (A may be empty, meaning all are normal).

Your goal is to precisely identify which faulty cameras are in set A. You can repeatedly ask me regional probe queries: choose any subset of cameras S from L (excluding T), and ask "how many cameras in probe group S are in a faulty state". I will truthfully tell you a non-negative integer k, representing the number of faulty cameras in S (the size of the intersection between S and A).

When you have gathered enough information, submit your inferred faulty camera set A. The task succeeds if and only if your answer is completely correct; otherwise it fails. Please try to complete the troubleshooting with as few queries as possible.

For each query, use the following XML format to submit a probe group S (a comma-separated list of numbers, excluding the hub camera T):

<query_subset>1,3,5</query_subset>

If you want to query whether a single camera is faulty, you can submit just one number:

<query_subset>7</query_subset>

When submitting your final answer, list all camera numbers you believe are faulty (comma-separated, order does not matter). If you believe A is empty (all normal), submit empty content:

<answer>2,4,6</answer>

Or (if A is empty):

<answer></answer>
"""

    contextualized_rule_zh_2 = """\
[医疗病原体筛查]
我们现在来操作一套"致病靶点联合检测"系统，规则如下：

我们的数据库中标记了一组可能导致未知综合征的病原体 L，编号从 1 到 {n}，其中包含一种明确作为健康对照的良性变异 T（编号为 {target}）。我已秘密锁定了一组导致某患者发病的致病靶点集合 A，A 是 L 中除 T 之外的某些病原体组成的集合（A 可能为空，即患者无上述感染）。

你的目标是精确识别出集合 A 中包含哪些病原体。你可以反复向我提出联合检测查询：选择 L 中除 T 之外的任意若干病原体组成一个检测面板 S，询问"面板 S 中有多少个靶点在患者体内呈现阳性"，我会如实告诉你一个非负整数 k，表示 S 中阳性靶点的数量（即 S 与 A 的交集大小）。

当你收集到足够信息后，请提交你推断出的致病靶点集合 A。若答案完全正确则确诊成功，否则诊断失败。请尽可能用较少的检测次数完成确诊。

每次查询时，请使用以下 XML 格式提交一个检测面板 S（用逗号分隔的编号列表，编号不能包含对照变异 T）：

<query_subset>1,3,5</query_subset>

如果你想单独查询某一种病原体是否为阳性，也可以只提交一个编号：

<query_subset>7</query_subset>

提交最终答案时，请列出你认为属于致病靶点的所有病原体编号（用逗号隔开，顺序不限）。如果你认为 A 为空集（无感染），请提交空内容：

<answer>2,4,6</answer>

或（如果 A 为空）：

<answer></answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's operate a "Pathogenic Target Joint Detection" system. Here are the rules:

Our database flags a set of pathogens L suspected of causing an unknown syndrome, numbered from 1 to {n}, which includes a known benign variant T acting as a healthy control (numbered {target}). I have secretly locked onto a set of pathogenic targets A causing illness in a patient. A consists of some pathogens from L excluding T (A may be empty, meaning no such infection).

Your goal is to precisely identify which pathogens are in set A. You can repeatedly ask me joint detection queries: choose any subset of pathogens S from L (excluding T) to form a testing panel, and ask "how many targets in panel S test positive in the patient". I will truthfully tell you a non-negative integer k, representing the number of positive targets in S (the size of the intersection between S and A).

When you have gathered enough information, submit your inferred pathogenic target set A. The diagnosis succeeds if and only if your answer is completely correct; otherwise it fails. Please try to complete the diagnosis with as few queries as possible.

For each query, use the following XML format to submit a testing panel S (a comma-separated list of numbers, excluding the control variant T):

<query_subset>1,3,5</query_subset>

If you want to query whether a single pathogen is positive, you can submit just one number:

<query_subset>7</query_subset>

When submitting your final answer, list all pathogen numbers you believe are pathogenic targets (comma-separated, order does not matter). If you believe A is empty (no infection), submit empty content:

<answer>2,4,6</answer>

Or (if A is empty):

<answer></answer>
"""

    contextualized_rule_zh_3 = """\
[教育学情分析]
我们现在来操作"学生知识点薄弱项分析"系统，规则如下：

我们的课程体系中有一批知识点标签 L，编号从 1 到 {n}，其中包含一个所有学生都已掌握的通识标签 T（编号为 {target}）。我已秘密评估了某位学生，并找出了他的薄弱知识点集合 A，A 是 L 中除 T 之外的某些知识点组成的集合（A 可能为空，即该生无薄弱项）。

你的目标是精确识别出集合 A 中包含哪些薄弱知识点。你可以反复向我提出试卷测评查询：选择 L 中除 T 之外的任意若干知识点组合成一套测试卷 S，询问"测试卷 S 中有多少个知识点属于该生的薄弱项"，我会如实告诉你一个非负整数 k，表示 S 中薄弱知识点的数量（即 S 与 A 的交集大小）。

当你收集到足够信息后，请提交你推断出的薄弱知识点集合 A。若答案完全正确则学情分析成功，否则分析失败。请尽可能用较少的测评次数完成推断。

每次查询时，请使用以下 XML 格式提交一套测试卷 S（用逗号分隔的知识点编号列表，编号不能包含通识标签 T）：

<query_subset>1,3,5</query_subset>

如果你想单独测试某一个知识点是否薄弱，也可以只提交一个编号：

<query_subset>7</query_subset>

提交最终答案时，请列出你认为属于薄弱项的所有知识点编号（用逗号隔开，顺序不限）。如果你认为 A 为空集（全部掌握），请提交空内容：

<answer>2,4,6</answer>

或（如果 A 为空）：

<answer></answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's operate the "Student Weak Knowledge Point Analysis" system. Here are the rules:

Our curriculum has a batch of knowledge point tags L, numbered from 1 to {n}. This includes a general knowledge tag T (numbered {target}) that all students have mastered. I have secretly evaluated a student and identified their set of weak knowledge points A, which consists of some tags from L excluding T (A may be empty, meaning no weak points).

Your goal is to precisely identify which weak knowledge points are in set A. You can repeatedly ask me assessment queries: choose any subset of knowledge points S from L (excluding T) to form a test paper, and ask "how many knowledge points in test paper S are weak points for this student". I will truthfully tell you a non-negative integer k, representing the number of weak points in S (the size of the intersection between S and A).

When you have gathered enough information, submit your inferred set of weak knowledge points A. The analysis succeeds if and only if your answer is completely correct; otherwise it fails. Please try to complete the inference with as few test queries as possible.

For each query, use the following XML format to submit a test paper S (a comma-separated list of numbers, excluding the general tag T):

<query_subset>1,3,5</query_subset>

If you want to test whether a single knowledge point is weak, you can submit just one number:

<query_subset>7</query_subset>

When submitting your final answer, list all knowledge point numbers you believe are weak points (comma-separated, order does not matter). If you believe A is empty (all mastered), submit empty content:

<answer>2,4,6</answer>

Or (if A is empty):

<answer></answer>
"""

    contextualized_rule_zh_4 = """\
[工业流水线无损探伤]
我们现在来执行一项"流水线零部件偏差检测"任务，规则如下：

一条核心流水线上安装了一组关键零部件 L，编号从 1 到 {n}，其中包含一个已通过校准的主控台节点 T（编号为 {target}）。近期流水线良率下降，我已秘密确定了产生微小偏差的零部件集合 A，A 是 L 中除 T 之外的某些零部件组成的集合（A 可能为空，即全部合格）。

你的目标是精确识别出集合 A 中包含哪些存在偏差的零部件。你可以反复向我提出探伤扫描查询：选择 L 中除 T 之外的任意若干零部件组成一个扫描组 S，询问"扫描组 S 中有多少个零部件存在偏差"，我会如实告诉你一个非负整数 k，表示 S 中不合格零部件的数量（即 S 与 A 的交集大小）。

当你收集到足够信息后，请提交你推断出的偏差零部件集合 A。若答案完全正确则检修成功，否则任务失败。请尽可能用较少的扫描次数完成检测。

每次查询时，请使用以下 XML 格式提交一个扫描组 S（用逗号分隔的零部件编号列表，编号不能包含主控台节点 T）：

<query_subset>1,3,5</query_subset>

如果你想单独扫描某一个零部件，也可以只提交一个编号：

<query_subset>7</query_subset>

提交最终答案时，请列出你认为存在偏差的所有零部件编号（用逗号隔开，顺序不限）。如果你认为 A 为空集（全部合格），请提交空内容：

<answer>2,4,6</answer>

或（如果 A 为空）：

<answer></answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's perform an "Assembly Line Component Deviation Detection" task. Here are the rules:

A core assembly line is equipped with a set of key components L, numbered from 1 to {n}. This includes a calibrated main console node T (numbered {target}). Recently, the yield rate has dropped, and I have secretly identified a set of components A that have developed minor deviations. A consists of some components from L excluding T (A may be empty, meaning all are qualified).

Your goal is to precisely identify which defective components are in set A. You can repeatedly ask me non-destructive scanning queries: choose any subset of components S from L (excluding T) to form a scanning group, and ask "how many components in scanning group S have deviations". I will truthfully tell you a non-negative integer k, representing the number of unqualified components in S (the size of the intersection between S and A).

When you have gathered enough information, submit your inferred set of deviated components A. The maintenance succeeds if and only if your answer is completely correct; otherwise it fails. Please try to complete the detection with as few scanning queries as possible.

For each query, use the following XML format to submit a scanning group S (a comma-separated list of numbers, excluding the console node T):

<query_subset>1,3,5</query_subset>

If you want to scan a single component, you can submit just one number:

<query_subset>7</query_subset>

When submitting your final answer, list all component numbers you believe have deviations (comma-separated, order does not matter). If you believe A is empty (all qualified), submit empty content:

<answer>2,4,6</answer>

Or (if A is empty):

<answer></answer>
"""

    contextualized_rule_zh_5 = """\
[法律证据篡改查证]
我们现在来协助进行"复杂案件证据链验真"工作，规则如下：

案卷中封存了一系列相关的证据线索 L，编号从 1 到 {n}，其中包含一份已公开定性的不可篡改核心物证 T（编号为 {target}）。根据线人情报，我已掌握了被犯罪嫌疑人秘密篡改或销毁的线索集合 A，A 是 L 中除 T 之外的某些线索组成的集合（A 可能为空，即全部证据真实）。

你的目标是精确识别出集合 A 中包含哪些被篡改的证据线索。你可以反复向我提出司法比对查询：选择 L 中除 T 之外的任意若干线索组成一个送检批次 S，询问"送检批次 S 中有多少个线索是遭受篡改的"，我会如实告诉你一个非负整数 k，表示 S 中被篡改的线索数量（即 S 与 A 的交集大小）。

当你收集到足够信息后，请提交你推断出的被篡改线索集合 A。若答案完全正确则查证成功，否则调查失败。请尽可能用较少的比对次数完成查证。

每次查询时，请使用以下 XML 格式提交一个送检批次 S（用逗号分隔的证据编号列表，编号不能包含核心物证 T）：

<query_subset>1,3,5</query_subset>

如果你想单独查验某一条线索，也可以只提交一个编号：

<query_subset>7</query_subset>

提交最终答案时，请列出你认为被篡改的所有证据线索编号（用逗号隔开，顺序不限）。如果你认为 A 为空集（全部真实），请提交空内容：

<answer>2,4,6</answer>

或（如果 A 为空）：

<answer></answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's assist in the "Complex Case Evidence Chain Authentication" work. Here are the rules:

The case file seals a series of related evidence clues L, numbered from 1 to {n}. This includes an unalterable core physical evidence T (numbered {target}) that has been publicly characterized. Based on informant intelligence, I have grasped the set of clues A that were secretly tampered with or destroyed by the suspect. A consists of some clues from L excluding T (A may be empty, meaning all evidence is authentic).

Your goal is to precisely identify which tampered evidence clues are in set A. You can repeatedly ask me forensic comparison queries: choose any subset of clues S from L (excluding T) to form an inspection batch, and ask "how many clues in inspection batch S have been tampered with". I will truthfully tell you a non-negative integer k, representing the number of tampered clues in S (the size of the intersection between S and A).

When you have gathered enough information, submit your inferred set of tampered clues A. The verification succeeds if and only if your answer is completely correct; otherwise it fails. Please try to complete the authentication with as few comparison queries as possible.

For each query, use the following XML format to submit an inspection batch S (a comma-separated list of numbers, excluding the core evidence T):

<query_subset>1,3,5</query_subset>

If you want to verify a single clue, you can submit just one number:

<query_subset>7</query_subset>

When submitting your final answer, list all clue numbers you believe have been tampered with (comma-separated, order does not matter). If you believe A is empty (all authentic), submit empty content:

<answer>2,4,6</answer>

Or (if A is empty):

<answer></answer>
"""

    tags = ["answer", "query_subset"]
    reasoning_type = "演绎推理"
    data_structure = "集合"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "target": 1,
                "answer_set": "3",
            },
            2: {
                "n": 8,
                "target": 4,
                "answer_set": "2,7",
            },
            3: {
                "n": 10,
                "target": 5,
                "answer_set": "1,6,9",
            },
            4: {
                "n": 12,
                "target": 6,
                "answer_set": "2,5,8,11",
            },
            5: {
                "n": 15,
                "target": 8,
                "answer_set": "",
            },
        },
        "en": {
            1: {
                "n": 5,
                "target": 1,
                "answer_set": "3",
            },
            2: {
                "n": 8,
                "target": 4,
                "answer_set": "2,7",
            },
            3: {
                "n": 10,
                "target": 5,
                "answer_set": "1,6,9",
            },
            4: {
                "n": 12,
                "target": 6,
                "answer_set": "2,5,8,11",
            },
            5: {
                "n": 15,
                "target": 8,
                "answer_set": "",
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
        self._game_info["target"] = cfg["target"]
        
        self.target_element = str(cfg["target"])
        self.full_set = set(str(i) for i in range(1, cfg["n"] + 1))
        
        answer_str = cfg["answer_set"].strip()
        if answer_str:
            self.answer_set = set(x.strip() for x in answer_str.split(",") if x.strip())
        else:
            self.answer_set = set()
        
        if self.target_element in self.answer_set:
            raise ValueError("Answer set should not contain target element")
        if not self.answer_set.issubset(self.full_set):
            raise ValueError("Answer set contains invalid elements")

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        if raw_ans:
            try:
                model_answer = set(x.strip() for x in raw_ans.split(",") if x.strip())
            except:
                return False
        else:
            model_answer = set()
        
        if self.target_element in model_answer:
            return False
        
        if not model_answer.issubset(self.full_set):
            return False
        
        return model_answer == self.answer_set

    def _cf_core_produce(self, parsed_info):
        if "query_subset" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        raw_query = parsed_info["query_subset"].strip()
        
        if not raw_query:
            return "0"
        
        try:
            query_set = set(x.strip() for x in raw_query.split(",") if x.strip())
        except:
            if self.config.language == "zh":
                raise ValueError("错误：查询格式无效。")
            else:
                raise ValueError("Error: Invalid query format.")
        
        if self.target_element in query_set:
            if self.config.language == "zh":
                raise ValueError(f"错误：查询集合不能包含目标元素 {self.target_element}。")
            else:
                raise ValueError(f"Error: Query set cannot contain target element {self.target_element}.")
        
        if not query_set.issubset(self.full_set):
            if self.config.language == "zh":
                raise ValueError("错误：查询集合包含无效的编号。")
            else:
                raise ValueError("Error: Query set contains invalid numbers.")
        
        intersection_size = len(query_set.intersection(self.answer_set))
        
        return str(intersection_size)

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit() or (correct.startswith('-') and correct[1:].isdigit()):
            val = int(correct)
            max_possible = len(self.full_set) - 1
            if val + 1 <= max_possible:
                return str(val + 1)
            elif val - 1 >= 0:
                return str(val - 1)
            else:
                return str(val + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        elif self.config.language == "en":
            if "Yes" in correct:
                return correct.replace("Yes", "No")
            elif "No" in correct:
                return correct.replace("No", "Yes")
            elif "yes" in correct:
                return correct.replace("yes", "no")
            elif "no" in correct:
                return correct.replace("no", "yes")
        
        return correct + "_WRONG"

    def get_all_possible_queries(self):
        queries = []
        
        valid_nums = sorted([int(x) for x in self.full_set if x != self.target_element])
        
        for num in valid_nums:
            num_str = str(num)
            subset_set = {num_str}
            intersection_size = len(subset_set.intersection(self.answer_set))
            
            queries.append({
                "query": f"<query_subset>{num_str}</query_subset>",
                "answer": str(intersection_size)
            })
        
        return queries

