from .base import Game
import random

class BinarySequenceReconstructionGame(Game):

    game_rule_zh = """\
我们现在来玩一个"二值序列重构"的推理游戏，规则如下：

游戏设定了一个长度为 {n} 的隐藏有序二值序列，序列中每个位置的值只能是 0 或 1。序列的索引从 1 到 {n}。我会告诉你这个序列中所有 1 的总个数为 {k}。

你的目标是通过提问来推断出这个完整的隐藏序列。你可以反复向我提出以下两类问题：

1. 区间和查询：选择一个区间 [L, R]（其中 1 <= L < R <= {n}），询问该区间内有多少个 1。注意：区间长度必须大于等于 2，不允许查询单个位置。我会返回一个非负整数作为答案。

2. 最终提交：当你有足够信心时，提交你推断出的完整序列。序列必须是长度为 {n} 的 0/1 字符串。

若提交的序列完全正确，游戏成功；若错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 区间和查询（例如查询区间 [2, 5]）：
<query_range>2,5</query_range>

- 最终提交（例如提交长度为 5 的序列）：
<answer>01101</answer>

注意：
- 区间查询中，左边界必须严格小于右边界，且区间长度至少为 2
- 最终提交的序列长度必须恰好为 {n}，且只能包含字符 '0' 和 '1'
- 序列中 1 的总个数应该为 {k}
"""

    game_rule_en = """\
Let's play a "Binary Sequence Reconstruction" deduction game. Here are the rules:

There is a hidden ordered binary sequence of length {n}, where each position contains either 0 or 1. The sequence is indexed from 1 to {n}. I will tell you that the total count of 1s in this sequence is {k}.

Your goal is to infer the complete hidden sequence through queries. You can repeatedly ask me two types of questions:

1. Range Sum Query: Choose an interval [L, R] (where 1 <= L < R <= {n}) and ask how many 1s are in that range. Note: The interval length must be at least 2; single-position queries are not allowed. I will return a non-negative integer as the answer.

2. Final Submission: When you are confident, submit your inferred complete sequence. The sequence must be a 0/1 string of length {n}.

If the submitted sequence is completely correct, the game succeeds; if incorrect or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Range Sum Query (e.g., querying interval [2, 5]):
<query_range>2,5</query_range>

- Final Submission (e.g., submitting a sequence of length 5):
<answer>01101</answer>

Note:
- In range queries, the left boundary must be strictly less than the right boundary, and the interval length must be at least 2
- The final submitted sequence must be exactly {n} characters long and contain only '0' and '1'
- The total count of 1s in the sequence should be {k}
"""

    contextualized_rule_zh_1 = """\
我们现在进行“城市主干道拥堵排查”任务。在这条主干道上有 {n} 个连续的交通监控节点（编号从 1 到 {n}），每个节点的状态为 0（畅通）或 1（拥堵）。指挥中心已知该路段总共有 {k} 个节点发生拥堵。

你的目标是通过提问来推断出完整的路况序列。你可以反复向我提出以下两类问题：

1. 区间和查询：选择一个区间 [L, R]（其中 1 <= L < R <= {n}），询问该路段内有多少个拥堵节点。注意：区间长度必须大于等于 2，不允许查询单个位置。我会返回一个非负整数作为答案。

2. 最终提交：当你有足够信心时，提交你推断出的完整路况序列。序列必须是长度为 {n} 的 0/1 字符串。

若提交的序列完全正确，任务成功；若错误或格式不符，任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 区间和查询（例如查询区间 [2, 5]）：
<query_range>2,5</query_range>

- 最终提交（例如提交长度为 5 的序列）：
<answer>01101</answer>

注意：
- 区间查询中，左边界必须严格小于右边界，且区间长度至少为 2
- 最终提交的序列长度必须恰好为 {n}，且只能包含字符 '0' 和 '1'
- 序列中 1 的总个数应该为 {k}
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's conduct an "Urban Arterial Congestion Troubleshooting" task. There are {n} consecutive traffic monitoring nodes on this arterial road (indexed from 1 to {n}), where each node's status is either 0 (clear) or 1 (congested). The command center knows that the total count of congested nodes in this sequence is {k}.

Your goal is to infer the complete hidden sequence through queries. You can repeatedly ask me two types of questions:

1. Range Sum Query: Choose an interval [L, R] (where 1 <= L < R <= {n}) and ask how many 1s (congested nodes) are in that range. Note: The interval length must be at least 2; single-position queries are not allowed. I will return a non-negative integer as the answer.

2. Final Submission: When you are confident, submit your inferred complete sequence. The sequence must be a 0/1 string of length {n}.

If the submitted sequence is completely correct, the task succeeds; if incorrect or the format is invalid, the task fails.

Each query must contain only one tag. Use the following XML format:

- Range Sum Query (e.g., querying interval [2, 5]):
<query_range>2,5</query_range>

- Final Submission (e.g., submitting a sequence of length 5):
<answer>01101</answer>

Note:
- In range queries, the left boundary must be strictly less than the right boundary, and the interval length must be at least 2
- The final submitted sequence must be exactly {n} characters long and contain only '0' and '1'
- The total count of 1s in the sequence should be {k}
"""

    contextualized_rule_zh_2 = """\
我们现在进行“基因片段变异筛查”任务。在一组长度为 {n} 的连续基因序列样本中（编号从 1 到 {n}），每个位点的检测结果为 0（正常）或 1（变异）。实验室已知该样本组总共包含 {k} 个变异位点。

你的目标是通过提问来推断出完整的阴阳性序列。你可以反复向我提出以下两类问题：

1. 区间和查询：选择一个区间 [L, R]（其中 1 <= L < R <= {n}），询问该样本区间内有多少个变异位点。注意：区间长度必须大于等于 2，不允许查询单个位置。我会返回一个非负整数作为答案。

2. 最终提交：当你有足够信心时，提交你推断出的完整阴阳性序列。序列必须是长度为 {n} 的 0/1 字符串。

若提交的序列完全正确，任务成功；若错误或格式不符，任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 区间和查询（例如查询区间 [2, 5]）：
<query_range>2,5</query_range>

- 最终提交（例如提交长度为 5 的序列）：
<answer>01101</answer>

注意：
- 区间查询中，左边界必须严格小于右边界，且区间长度至少为 2
- 最终提交的序列长度必须恰好为 {n}，且只能包含字符 '0' 和 '1'
- 序列中 1 的总个数应该为 {k}
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct a "Gene Segment Mutation Screening" task. In a set of {n} consecutive gene sequence samples (indexed from 1 to {n}), each locus tests as either 0 (normal) or 1 (mutated). The laboratory knows that the total count of mutated loci in this sequence is {k}.

Your goal is to infer the complete hidden sequence through queries. You can repeatedly ask me two types of questions:

1. Range Sum Query: Choose an interval [L, R] (where 1 <= L < R <= {n}) and ask how many 1s (mutated loci) are in that range. Note: The interval length must be at least 2; single-position queries are not allowed. I will return a non-negative integer as the answer.

2. Final Submission: When you are confident, submit your inferred complete sequence. The sequence must be a 0/1 string of length {n}.

If the submitted sequence is completely correct, the task succeeds; if incorrect or the format is invalid, the task fails.

Each query must contain only one tag. Use the following XML format:

- Range Sum Query (e.g., querying interval [2, 5]):
<query_range>2,5</query_range>

- Final Submission (e.g., submitting a sequence of length 5):
<answer>01101</answer>

Note:
- In range queries, the left boundary must be strictly less than the right boundary, and the interval length must be at least 2
- The final submitted sequence must be exactly {n} characters long and contain only '0' and '1'
- The total count of 1s in the sequence should be {k}
"""

    contextualized_rule_zh_3 = """\
我们现在进行“标准化试卷精准阅卷”任务。一份试卷包含 {n} 道连续的考题（题号从 1 到 {n}），考生的每道题得分为 0（错误）或 1（正确）。系统显示该考生在这部分总共答对了 {k} 道题。

你的目标是通过提问来推断出完整的答题正误序列。你可以反复向我提出以下两类问题：

1. 区间和查询：选择一个区间 [L, R]（其中 1 <= L < R <= {n}），询问该题号区间内该考生答对了多少道题。注意：区间长度必须大于等于 2，不允许查询单个位置。我会返回一个非负整数作为答案。

2. 最终提交：当你有足够信心时，提交你推断出的完整答题正误序列。序列必须是长度为 {n} 的 0/1 字符串。

若提交的序列完全正确，任务成功；若错误或格式不符，任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 区间和查询（例如查询区间 [2, 5]）：
<query_range>2,5</query_range>

- 最终提交（例如提交长度为 5 的序列）：
<answer>01101</answer>

注意：
- 区间查询中，左边界必须严格小于右边界，且区间长度至少为 2
- 最终提交的序列长度必须恰好为 {n}，且只能包含字符 '0' 和 '1'
- 序列中 1 的总个数应该为 {k}
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a "Standardized Exam Precision Grading" task. An exam contains {n} consecutive questions (numbered 1 to {n}), and the candidate's score for each question is either 0 (incorrect) or 1 (correct). The system indicates that the candidate answered a total of {k} questions correctly.

Your goal is to infer the complete hidden sequence through queries. You can repeatedly ask me two types of questions:

1. Range Sum Query: Choose an interval [L, R] (where 1 <= L < R <= {n}) and ask how many 1s (correct answers) are in that range. Note: The interval length must be at least 2; single-position queries are not allowed. I will return a non-negative integer as the answer.

2. Final Submission: When you are confident, submit your inferred complete sequence. The sequence must be a 0/1 string of length {n}.

If the submitted sequence is completely correct, the task succeeds; if incorrect or the format is invalid, the task fails.

Each query must contain only one tag. Use the following XML format:

- Range Sum Query (e.g., querying interval [2, 5]):
<query_range>2,5</query_range>

- Final Submission (e.g., submitting a sequence of length 5):
<answer>01101</answer>

Note:
- In range queries, the left boundary must be strictly less than the right boundary, and the interval length must be at least 2
- The final submitted sequence must be exactly {n} characters long and contain only '0' and '1'
- The total count of 1s in the sequence should be {k}
"""

    contextualized_rule_zh_4 = """\
我们现在进行“流水线批量无损探伤”任务。生产线上有一批 {n} 个连续下线的精密零件（编号从 1 到 {n}），每个零件的质检状态为 0（合格）或 1（次品）。出厂检测报告显示这批零件中总共有 {k} 个次品。

你的目标是通过提问来推断出完整的质检结果序列。你可以反复向我提出以下两类问题：

1. 区间和查询：选择一个区间 [L, R]（其中 1 <= L < R <= {n}），询问该区间内有多少个次品零件。注意：区间长度必须大于等于 2，不允许查询单个位置。我会返回一个非负整数作为答案。

2. 最终提交：当你有足够信心时，提交你推断出的完整质检结果序列。序列必须是长度为 {n} 的 0/1 字符串。

若提交的序列完全正确，任务成功；若错误或格式不符，任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 区间和查询（例如查询区间 [2, 5]）：
<query_range>2,5</query_range>

- 最终提交（例如提交长度为 5 的序列）：
<answer>01101</answer>

注意：
- 区间查询中，左边界必须严格小于右边界，且区间长度至少为 2
- 最终提交的序列长度必须恰好为 {n}，且只能包含字符 '0' 和 '1'
- 序列中 1 的总个数应该为 {k}
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's conduct a "Production Line Batch Non-Destructive Testing" task. There is a batch of {n} consecutive precision parts coming off the assembly line (indexed from 1 to {n}), and the quality inspection status of each part is either 0 (qualified) or 1 (defective). The factory inspection report shows there are exactly {k} defective parts in this batch.

Your goal is to infer the complete hidden sequence through queries. You can repeatedly ask me two types of questions:

1. Range Sum Query: Choose an interval [L, R] (where 1 <= L < R <= {n}) and ask how many 1s (defective parts) are in that range. Note: The interval length must be at least 2; single-position queries are not allowed. I will return a non-negative integer as the answer.

2. Final Submission: When you are confident, submit your inferred complete sequence. The sequence must be a 0/1 string of length {n}.

If the submitted sequence is completely correct, the task succeeds; if incorrect or the format is invalid, the task fails.

Each query must contain only one tag. Use the following XML format:

- Range Sum Query (e.g., querying interval [2, 5]):
<query_range>2,5</query_range>

- Final Submission (e.g., submitting a sequence of length 5):
<answer>01101</answer>

Note:
- In range queries, the left boundary must be strictly less than the right boundary, and the interval length must be at least 2
- The final submitted sequence must be exactly {n} characters long and contain only '0' and '1'
- The total count of 1s in the sequence should be {k}
"""

    contextualized_rule_zh_5 = """\
我们现在进行“复杂案卷关键证据链梳理”任务。一份核心卷宗内包含 {n} 份连续编号的证据材料（编号从 1 到 {n}），每份材料的效力被评定为 0（无效关联）或 1（核心关键证据）。主审法官已知该卷宗中总共有 {k} 份核心关键证据。

你的目标是通过提问来推断出完整的证据有效性判定序列。你可以反复向我提出以下两类问题：

1. 区间和查询：选择一个区间 [L, R]（其中 1 <= L < R <= {n}），询问该连续卷宗区间内包含多少份核心关键证据。注意：区间长度必须大于等于 2，不允许查询单个位置。我会返回一个非负整数作为答案。

2. 最终提交：当你有足够信心时，提交你推断出的完整证据有效性判定序列。序列必须是长度为 {n} 的 0/1 字符串。

若提交的序列完全正确，任务成功；若错误或格式不符，任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 区间和查询（例如查询区间 [2, 5]）：
<query_range>2,5</query_range>

- 最终提交（例如提交长度为 5 的序列）：
<answer>01101</answer>

注意：
- 区间查询中，左边界必须严格小于右边界，且区间长度至少为 2
- 最终提交的序列长度必须恰好为 {n}，且只能包含字符 '0' 和 '1'
- 序列中 1 的总个数应该为 {k}
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct a "Complex Case File Key Evidence Chain Review" task. A core case file contains {n} consecutively numbered evidentiary materials (indexed from 1 to {n}), with the validity of each assessed as either 0 (invalid/irrelevant) or 1 (core key evidence). The presiding judge knows there are exactly {k} core key evidentiary materials in total.

Your goal is to infer the complete hidden sequence through queries. You can repeatedly ask me two types of questions:

1. Range Sum Query: Choose an interval [L, R] (where 1 <= L < R <= {n}) and ask how many 1s (core key evidences) are in that range. Note: The interval length must be at least 2; single-position queries are not allowed. I will return a non-negative integer as the answer.

2. Final Submission: When you are confident, submit your inferred complete sequence. The sequence must be a 0/1 string of length {n}.

If the submitted sequence is completely correct, the task succeeds; if incorrect or the format is invalid, the task fails.

Each query must contain only one tag. Use the following XML format:

- Range Sum Query (e.g., querying interval [2, 5]):
<query_range>2,5</query_range>

- Final Submission (e.g., submitting a sequence of length 5):
<answer>01101</answer>

Note:
- In range queries, the left boundary must be strictly less than the right boundary, and the interval length must be at least 2
- The final submitted sequence must be exactly {n} characters long and contain only '0' and '1'
- The total count of 1s in the sequence should be {k}
"""

    tags = ["answer", "query_range"]

    reasoning_type = "演绎推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "k": 2,
                "sequence": "01010",
            },
            2: {
                "n": 7,
                "k": 3,
                "sequence": "1001010",
            },
            3: {
                "n": 8,
                "k": 4,
                "sequence": "10110100",
            },
            4: {
                "n": 10,
                "k": 6,
                "sequence": "1101011010",
            },
            5: {
                "n": 12,
                "k": 5,
                "sequence": "100101010010",
            },
        },
        "en": {
            1: {
                "n": 5,
                "k": 2,
                "sequence": "01010",
            },
            2: {
                "n": 7,
                "k": 3,
                "sequence": "1001010",
            },
            3: {
                "n": 8,
                "k": 4,
                "sequence": "10110100",
            },
            4: {
                "n": 10,
                "k": 6,
                "sequence": "1101011010",
            },
            5: {
                "n": 12,
                "k": 5,
                "sequence": "100101010010",
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
        self._game_info["k"] = cfg["k"]
        
        self.hidden_sequence = cfg["sequence"]
        
        assert len(self.hidden_sequence) == cfg["n"], "Sequence length mismatch"
        assert self.hidden_sequence.count('1') == cfg["k"], "Count of 1s mismatch"
        assert all(c in '01' for c in self.hidden_sequence), "Sequence contains invalid characters"

    def evaluate(self, parsed_info):
        submitted_sequence = parsed_info["answer"].strip()
        
        if len(submitted_sequence) != len(self.hidden_sequence):
            return False
        
        if not all(c in '01' for c in submitted_sequence):
            return False
        
        return submitted_sequence == self.hidden_sequence

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            error_prefix = "错误："
            invalid_format = "区间格式无效，请使用 'L,R' 格式。"
            out_of_bounds = "区间边界超出范围。索引必须在 1 到 {n} 之间。"
            invalid_range = "区间无效。左边界必须严格小于右边界，且区间长度至少为 2。"
        else:
            error_prefix = "Error: "
            invalid_format = "Invalid range format. Please use 'L,R' format."
            out_of_bounds = "Range boundaries out of bounds. Indices must be between 1 and {n}."
            invalid_range = "Invalid range. Left boundary must be strictly less than right boundary, and range length must be at least 2."

        if "query_range" in parsed_info:
            try:
                raw = parsed_info["query_range"].strip()
                parts = [x.strip() for x in raw.split(",")]
                
                if len(parts) != 2:
                    return error_prefix + invalid_format
                
                L = int(parts[0])
                R = int(parts[1])
                
                if L < 1 or R > len(self.hidden_sequence):
                    return error_prefix + out_of_bounds.format(n=len(self.hidden_sequence))
                
                if L >= R:
                    return error_prefix + invalid_range
                
                count = sum(int(self.hidden_sequence[i]) for i in range(L-1, R))
                return str(count)
                
            except ValueError:
                return error_prefix + invalid_format
            except Exception as e:
                return error_prefix + str(e)
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        
        lower_correct = correct.lower()
        if "yes" in lower_correct:
            if correct == "Yes": return "No"
            if correct == "YES": return "NO"
            if correct == "yes": return "no"
            return correct.replace("Yes", "No").replace("yes", "no")
        elif "no" in lower_correct:
            if correct == "No": return "Yes"
            if correct == "NO": return "YES"
            if correct == "no": return "yes"
            return correct.replace("No", "Yes").replace("no", "yes")

        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        n = self._game_info["n"]
        results = []
        for L in range(1, n):
            for R in range(L + 1, n + 1):
                query_content = f"{L},{R}"
                
                count = sum(int(self.hidden_sequence[i]) for i in range(L - 1, R))
                
                results.append({
                    "query": f"<query_range>{query_content}</query_range>",
                    "answer": str(count)
                })
        
        return results