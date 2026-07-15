from .base import Game
import re

def lcs_length(s1: str, s2: str) -> int:
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]

class LCSDeductionGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "序列"

    game_rule_zh = """\
我们现在来玩一个"最长公共子序列推理"游戏，规则如下：

游戏设定了一个字母表，以及三个符号序列：A、B、K。你可以看到这三个序列的具体内容和长度：
- 序列 A：{seq_a}
- 序列 B：{seq_b}
- 序列 K：{seq_k}

我已秘密选定了一个参考序列 R，它是从以下四个候选序列中选择的一个，并在整个游戏过程中保持不变：
1. A 本身
2. A 的反序
3. B 本身
4. B 的反序

你的目标是：
1. 通过查询推断出参考序列 R 是哪一个
2. 计算序列 K 与参考序列 R 的最长公共子序列长度

你可以反复向我提交查询序列 S（任意符号序列），我会返回 S 与参考序列 R 的最长公共子序列长度。你必须至少进行两次查询后才能提交最终答案。

每次查询时，提交一个序列：
<query>你的查询序列</query>

提交最终答案时，必须指定你判定的参考序列类型（使用 A、reverse_A、B、reverse_B 之一），以及你计算出的 K 与 R 的最长公共子序列长度：
<answer>reference=A, lcs_length=5</answer>

注意：reference 的值必须是 A、reverse_A、B、reverse_B 中的一个。
"""

    game_rule_en = """\
Let's play a "Longest Common Subsequence (LCS) Deduction" game. Here are the rules:

The game has defined an alphabet and three symbol sequences: A, B, and K. You can see the specific content and length of these three sequences:
- Sequence A: {seq_a}
- Sequence B: {seq_b}
- Sequence K: {seq_k}

I have secretly selected a reference sequence R from the following four candidates, which will remain constant throughout the game:
1. A itself
2. Reverse of A
3. B itself
4. Reverse of B

Your goals are:
1. Infer which candidate is the reference sequence R through queries
2. Calculate the LCS length between sequence K and reference sequence R

You can repeatedly submit query sequences S (any symbol sequence), and I will return the LCS length between S and the reference sequence R. You must perform at least two queries before submitting your final answer.

To make a query, submit a sequence:
<query>your query sequence</query>

To submit the final answer, specify the reference sequence type you determined (use one of A, reverse_A, B, reverse_B) and the LCS length you calculated between K and R:
<answer>reference=A, lcs_length=5</answer>

Note: The value of reference must be one of A, reverse_A, B, or reverse_B.
"""

    contextualized_rule_zh_1 = """\
我们现在来进行一项“最优通行路径对齐”测试。你是一套智能交通系统的调度终端。
系统中录入了两个标准的干线路径节点序列：A线 和 B线，以及一辆目标车辆的实际行驶轨迹 K。
- A线节点序列：{seq_a}
- B线节点序列：{seq_b}
- 目标车辆轨迹 K：{seq_k}

系统后台已锁定了一条“当前执行的管制路线”R，它必然是以下四种情况之一，且在测试期间不发生改变：
1. A线正向 (A)
2. A线反向 (reverse_A)
3. B线正向 (B)
4. B线反向 (reverse_B)

你的目标是：
1. 通过探测推断出当前执行的管制路线 R 究竟是哪一条。
2. 计算出车辆轨迹 K 与 管制路线 R 的最大有效匹配节点数（即两者的最长公共子序列长度）。

你可以反复提交探测路径 S（任意节点序列），我会反馈 S 与 R 的最大有效匹配节点数。你必须至少进行两次探测后才能提交最终报告。

每次探测时，提交一个路径序列：
<query>你的探测路径序列</query>

提交最终报告时，必须指定你推断出的管制路线类型（使用 A、reverse_A、B、reverse_B 之一），以及计算出的 K 与 R 的最大有效匹配节点数：
<answer>reference=A, lcs_length=5</answer>
注意：reference 的值必须严格限定在 A、reverse_A、B、reverse_B 之中。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
We are now conducting an "Optimal Route Alignment" test. You are the dispatch terminal of an intelligent traffic management system.
The system has recorded two standard arterial route node sequences: Route A and Route B, along with the actual driving trajectory K of a target vehicle.
- Route A Sequence: {seq_a}
- Route B Sequence: {seq_b}
- Target Vehicle Trajectory K: {seq_k}

The system backend has locked in a "currently enforced control route" R, which is secretly selected from one of the following four configurations and remains unchanged during the test:
1. Forward Route A (A)
2. Reverse Route A (reverse_A)
3. Forward Route B (B)
4. Reverse Route B (reverse_B)

Your objectives are:
1. Infer which configuration is the enforced control route R through probing.
2. Calculate the maximum number of sequentially matching nodes (i.e., the Longest Common Subsequence length) between trajectory K and control route R.

You can repeatedly submit probe routes S (any node sequence), and I will return the maximum effectively matched nodes between S and R. You must perform at least two probes before submitting your final report.

To make a probe, submit a sequence:
<query>your probe route sequence</query>

To submit the final report, specify the control route type you deduced (use one of A, reverse_A, B, reverse_B) and the maximum sequential matching nodes calculated between K and R:
<answer>reference=A, lcs_length=5</answer>
Note: The value of reference must be exactly one of A, reverse_A, B, or reverse_B.
"""

    contextualized_rule_zh_2 = """\
我们现在来进行一项“靶向基因图谱比对”任务。你是一套临床医学辅助诊断系统的分析引擎。
系统中记录了两种标准靶向药物的分子作用位点序列：方案A 和 方案B，以及一名患者样本中提取出的突变靶点序列 K。
- 方案A序列：{seq_a}
- 方案B序列：{seq_b}
- 患者样本序列 K：{seq_k}

系统底层已暗中确定了一组“基准抗性图谱” R，它是从以下四组候选图谱中选择其一，并在整个分析过程中保持不变：
1. 方案A本身 (A)
2. 方案A的逆向序列 (reverse_A)
3. 方案B本身 (B)
4. 方案B的逆向序列 (reverse_B)

你的目标是：
1. 通过模拟检验，推断出基准抗性图谱 R 是哪一种。
2. 计算出患者样本 K 与 基准图谱 R 的最大保守同源长度（即两者的最长公共子序列长度）。

你可以反复提交试验序列 S（任意位点序列），我会反馈 S 与 R 的同源长度。你必须至少进行两次检验后才能出具最终诊断。

每次检验时，提交一个试验序列：
<query>你的试验序列</query>

出具最终诊断时，必须指定你推断出的基准抗性图谱类型（使用 A、reverse_A、B、reverse_B 之一），以及你计算出的 K 与 R 的最大保守同源长度：
<answer>reference=A, lcs_length=5</answer>
注意：reference 的值必须严格限定在 A、reverse_A、B、reverse_B 之中。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
We are now conducting a "Targeted Genomic Mapping" task. You are the analysis engine of a clinical medical diagnosis system.
The system records the molecular binding site sequences of two standard targeted therapies: Protocol A and Protocol B, as well as a mutated target sequence K extracted from a patient's sample.
- Protocol A Sequence: {seq_a}
- Protocol B Sequence: {seq_b}
- Patient Sample Sequence K: {seq_k}

The system backend has secretly determined a "baseline resistance profile" R, selected from one of the following four candidates, which remains constant throughout the analysis:
1. Protocol A itself (A)
2. Reverse of Protocol A (reverse_A)
3. Protocol B itself (B)
4. Reverse of Protocol B (reverse_B)

Your objectives are:
1. Infer which candidate is the baseline resistance profile R through simulation queries.
2. Calculate the maximum conserved homologous length (i.e., the Longest Common Subsequence length) between sample K and baseline R.

You can repeatedly submit test sequences S (any binding site sequence), and I will return the homologous length between S and R. You must perform at least two simulations before issuing the final diagnosis.

To make a simulation query, submit a sequence:
<query>your test sequence</query>

To issue the final diagnosis, specify the baseline resistance profile type you inferred (use one of A, reverse_A, B, reverse_B) and the maximum conserved homologous length calculated between K and R:
<answer>reference=A, lcs_length=5</answer>
Note: The value of reference must be exactly one of A, reverse_A, B, or reverse_B.
"""

    contextualized_rule_zh_3 = """\
我们现在来进行一项“自适应学习路径对齐”测试。你是一个教育AI系统中的学情分析模块。
平台中预设了两个标准课程模块的学习序列：大纲A 和 大纲B，并记录了一名学生的实际学习轨迹 K。
- 大纲A序列：{seq_a}
- 大纲B序列：{seq_b}
- 学生轨迹 K：{seq_k}

底层系统已经为该学生秘密指派了一个“最优认知基准线” R，它是从以下四个候选项中确定的一个，且在测试期间保持不变：
1. 大纲A正序 (A)
2. 大纲A逆序（通常用于复习或溯源） (reverse_A)
3. 大纲B正序 (B)
4. 大纲B逆序 (reverse_B)

你的目标是：
1. 通过测试推测出系统指派的认知基准线 R 是哪一个。
2. 计算学生的实际学习轨迹 K 与 基准线 R 的最大顺位契合度（即两者的最长公共子序列长度）。

你可以反复提交假设轨迹 S（任意学习序列），我会反馈 S 与 R 的最大顺位契合度。你必须至少进行两次测试后才能提交最终评估。

每次测试时，提交一个假设轨迹序列：
<query>你的假设轨迹序列</query>

提交最终评估时，必须指定你推断出的认知基准线类型（使用 A、reverse_A、B、reverse_B 之一），以及你计算出的 K 与 R 的最大顺位契合度：
<answer>reference=A, lcs_length=5</answer>
注意：reference 的值必须严格限定在 A、reverse_A、B、reverse_B 之中。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
We are now conducting an "Adaptive Learning Path Alignment" test. You are a learning analytics module in an educational AI system.
The platform has preset two standard curriculum module learning sequences: Syllabus A and Syllabus B, and recorded a student's actual learning trajectory K.
- Syllabus A Sequence: {seq_a}
- Syllabus B Sequence: {seq_b}
- Student Trajectory K: {seq_k}

The underlying system has secretly assigned an "optimal cognitive baseline" R for this student, chosen from the following four candidates, which remains unchanged during the test:
1. Forward Syllabus A (A)
2. Reverse Syllabus A (often used for review or tracing) (reverse_A)
3. Forward Syllabus B (B)
4. Reverse Syllabus B (reverse_B)

Your objectives are:
1. Infer which candidate is the assigned cognitive baseline R through testing.
2. Calculate the maximum sequential alignment score (i.e., the Longest Common Subsequence length) between the student's trajectory K and baseline R.

You can repeatedly submit hypothetical trajectories S (any learning sequence), and I will return the alignment score between S and R. You must perform at least two tests before submitting the final assessment.

To make a test query, submit a trajectory sequence:
<query>your hypothetical trajectory sequence</query>

To submit the final assessment, specify the cognitive baseline type you inferred (use one of A, reverse_A, B, reverse_B) and the maximum sequential alignment score calculated between K and R:
<answer>reference=A, lcs_length=5</answer>
Note: The value of reference must be exactly one of A, reverse_A, B, or reverse_B.
"""

    contextualized_rule_zh_4 = """\
我们现在来进行一项“自动化装配工序核验”测试。你是一套工业质检系统的控制逻辑单元。
流水线上定义了两种标准装配工艺指令集：工艺A 和 工艺B，同时捕获到一件异常产品的实际加工日志 K。
- 工艺A指令序列：{seq_a}
- 工艺B指令序列：{seq_b}
- 异常加工日志 K：{seq_k}

系统主控板内部固化了一个“标准参照指令流” R，它来自于以下四种配置之一，并在核验全程中保持不变：
1. 工艺A正向装配 (A)
2. 工艺A逆向拆解 (reverse_A)
3. 工艺B正向装配 (B)
4. 工艺B逆向拆解 (reverse_B)

你的目标是：
1. 通过向主控板发送探测指令推断出标准参照指令流 R 是哪一种配置。
2. 计算异常加工日志 K 与 参照指令流 R 的最大连续合规指令数（即两者的最长公共子序列长度）。

你可以反复发送测试指令序列 S（任意操作序列），我会返回 S 与 R 的连续合规指令数。你必须至少发送两次探测指令后才能提交最终报告。

每次发送探测指令时，提交一个操作序列：
<query>你的测试指令序列</query>

提交最终报告时，必须指定你推测出的标准参照配置（使用 A、reverse_A、B、reverse_B 之一），以及你计算出的 K 与 R 的最大连续合规指令数：
<answer>reference=A, lcs_length=5</answer>
注意：reference 的值必须严格限定在 A、reverse_A、B、reverse_B 之中。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
We are now conducting an "Automated Assembly Verification" test. You are the control logic unit of an industrial quality inspection system.
The assembly line defines two standard operational instruction sets: Process A and Process B, and has captured the actual processing log K of an anomalous product.
- Process A Sequence: {seq_a}
- Process B Sequence: {seq_b}
- Anomalous Processing Log K: {seq_k}

The system's main control board has internally hardcoded a "standard reference instruction stream" R, derived from one of the following four configurations, which remains constant throughout the verification:
1. Forward Assembly Process A (A)
2. Reverse Teardown Process A (reverse_A)
3. Forward Assembly Process B (B)
4. Reverse Teardown Process B (reverse_B)

Your objectives are:
1. Infer which configuration is the standard reference instruction stream R by sending probe instructions to the control board.
2. Calculate the maximum number of sequentially compliant instructions (i.e., the Longest Common Subsequence length) between processing log K and reference stream R.

You can repeatedly send test instruction sequences S (any operational sequence), and I will return the sequentially compliant instruction count between S and R. You must send at least two probes before submitting the final report.

To send a probe instruction, submit an operational sequence:
<query>your test instruction sequence</query>

To submit the final report, specify the standard reference configuration you deduced (use one of A, reverse_A, B, reverse_B) and the maximum sequentially compliant instruction count calculated between K and R:
<answer>reference=A, lcs_length=5</answer>
Note: The value of reference must be exactly one of A, reverse_A, B, or reverse_B.
"""

    contextualized_rule_zh_5 = """\
我们现在来进行一项“司法程序合规性审查”工作。你是一款法律AI助手的法理逻辑分析模块。
案卷中记载了两个历史判例的标准程序步骤序列：判例A 和 判例B，以及当前待审理案件的实际执行程序记录 K。
- 判例A步骤序列：{seq_a}
- 判例B步骤序列：{seq_b}
- 当前案件执行记录 K：{seq_k}

主审法官在心中已确立了一条“法定审理基准线” R，它选自以下四种法理情形之一，并在本次审查期间不作变更：
1. 参照判例A的顺位程序 (A)
2. 参照判例A的权利回溯程序 (reverse_A)
3. 参照判例B的顺位程序 (B)
4. 参照判例B的权利回溯程序 (reverse_B)

你的目标是：
1. 通过向系统质询，推断出法官确立的法定审理基准线 R 是哪一种情形。
2. 计算案件记录 K 与 基准线 R 的最大合法程序顺位重合度（即两者的最长公共子序列长度）。

你可以反复提交模拟案件程序 S（任意步骤序列），我会返回 S 与 R 的程序顺位重合度。你必须至少进行两次质询后才能提交终局审查意见。

每次质询时，提交一个模拟程序序列：
<query>你的模拟程序序列</query>

提交终局审查意见时，必须指定你推断出的基准法理情形（使用 A、reverse_A、B、reverse_B 之一），以及你计算出的 K 与 R 的最大程序顺位重合度：
<answer>reference=A, lcs_length=5</answer>
注意：reference 的值必须严格限定在 A、reverse_A、B、reverse_B 之中。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
We are now conducting a "Procedural Compliance Review" task. You are the jurisprudential logic analysis module of a legal AI assistant.
The case files document standard procedural step sequences from two historical precedents: Precedent A and Precedent B, alongside the actual executed procedure record K for the current pending case.
- Precedent A Step Sequence: {seq_a}
- Precedent B Step Sequence: {seq_b}
- Current Case Record K: {seq_k}

The presiding judge has mentally established a "statutory adjudication baseline" R, selected from one of the following four jurisprudential scenarios, which will not change during this review:
1. Forward procedure based on Precedent A (A)
2. Retroactive rights procedure based on Precedent A (reverse_A)
3. Forward procedure based on Precedent B (B)
4. Retroactive rights procedure based on Precedent B (reverse_B)

Your objectives are:
1. Infer which jurisprudential scenario is the established statutory adjudication baseline R by querying the system.
2. Calculate the maximum sequential procedural compliance score (i.e., the Longest Common Subsequence length) between case record K and baseline R.

You can repeatedly submit hypothetical procedure sequences S (any step sequence), and I will return the procedural compliance score between S and R. You must perform at least two queries before submitting your final review opinion.

To make a query, submit a hypothetical procedure sequence:
<query>your hypothetical procedure sequence</query>

To submit the final review opinion, specify the baseline jurisprudential scenario you inferred (use one of A, reverse_A, B, reverse_B) and the maximum sequential procedural compliance score calculated between K and R:
<answer>reference=A, lcs_length=5</answer>
Note: The value of reference must be exactly one of A, reverse_A, B, or reverse_B.
"""

    user_prompt_zh = "你可以开始第一次查询了。注意：必须至少进行两次查询后才能提交答案。"
    user_prompt_en = "You can start your first query now. Note: You must perform at least two queries before submitting an answer."

    tags = ["answer", "query"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "seq_a": "ABCD",
                "seq_b": "EFGH",
                "seq_k": "ACEG",
                "reference_type": "A",
            },
            2: {
                "seq_a": "ABCDEF",
                "seq_b": "GHIJKL",
                "seq_k": "BDFHJL",
                "reference_type": "reverse_B",
            },
            3: {
                "seq_a": "ABCDEFGH",
                "seq_b": "IJKLMNOP",
                "seq_k": "ACEGIKMO",
                "reference_type": "B",
            },
            4: {
                "seq_a": "ABCDEFGHIJ",
                "seq_b": "KLMNOPQRST",
                "seq_k": "BDFHJLNPRT",
                "reference_type": "reverse_A",
            },
            5: {
                "seq_a": "ABCDEFGHIJKLM",
                "seq_b": "NOPQRSTUVWXYZ",
                "seq_k": "ACEGIKMOQSUWY",
                "reference_type": "B",
            },
        },
        "en": {
            1: {
                "seq_a": "ABCD",
                "seq_b": "EFGH",
                "seq_k": "ACEG",
                "reference_type": "A",
            },
            2: {
                "seq_a": "ABCDEF",
                "seq_b": "GHIJKL",
                "seq_k": "BDFHJL",
                "reference_type": "reverse_B",
            },
            3: {
                "seq_a": "ABCDEFGH",
                "seq_b": "IJKLMNOP",
                "seq_k": "ACEGIKMO",
                "reference_type": "B",
            },
            4: {
                "seq_a": "ABCDEFGHIJ",
                "seq_b": "KLMNOPQRST",
                "seq_k": "BDFHJLNPRT",
                "reference_type": "reverse_A",
            },
            5: {
                "seq_a": "ABCDEFGHIJKLM",
                "seq_b": "NOPQRSTUVWXYZ",
                "seq_k": "ACEGIKMOQSUWY",
                "reference_type": "B",
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
        
        self._game_info["seq_a"] = cfg["seq_a"]
        self._game_info["seq_b"] = cfg["seq_b"]
        self._game_info["seq_k"] = cfg["seq_k"]
        
        self.seq_a = cfg["seq_a"]
        self.seq_b = cfg["seq_b"]
        self.seq_k = cfg["seq_k"]
        
        self.seq_a_reverse = self.seq_a[::-1]
        self.seq_b_reverse = self.seq_b[::-1]
        
        reference_type = cfg["reference_type"]
        if reference_type == "A":
            self.reference_seq = self.seq_a
            self.reference_name = "A"
        elif reference_type == "reverse_A":
            self.reference_seq = self.seq_a_reverse
            self.reference_name = "reverse_A"
        elif reference_type == "B":
            self.reference_seq = self.seq_b
            self.reference_name = "B"
        elif reference_type == "reverse_B":
            self.reference_seq = self.seq_b_reverse
            self.reference_name = "reverse_B"
        else:
            raise ValueError(f"Unknown reference type: {reference_type}")
        
        self.ground_truth_lcs = lcs_length(self.seq_k, self.reference_seq)
        
        self.query_count = 0

    def evaluate(self, parsed_info):
        if self.query_count < 2:
            return False
        
        raw_ans = parsed_info["answer"]
        
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        for kv in kv_pairs:
            if "=" in kv:
                k, v = kv.split("=", 1)
                ans_dict[k.strip()] = v.strip()
        
        if "reference" not in ans_dict or "lcs_length" not in ans_dict:
            return False
        
        if ans_dict["reference"] != self.reference_name:
            return False
        
        try:
            model_lcs = int(ans_dict["lcs_length"])
        except:
            return False
            
        return model_lcs == self.ground_truth_lcs

    def _cf_core_produce(self, parsed_info):
        if "query" in parsed_info:
            query_seq = parsed_info["query"].strip()
            
            lcs_len = lcs_length(query_seq, self.reference_seq)
            
            self.query_count += 1
            
            return str(lcs_len)
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        c_lower = correct.lower()
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        elif self.config.language == "en":
            if "yes" in c_lower:
                if "Yes" in correct: return correct.replace("Yes", "No")
                if "yes" in correct: return correct.replace("yes", "no")
                if "YES" in correct: return correct.replace("YES", "NO")
                return correct.lower().replace("yes", "no")
            if "no" in c_lower:
                if "No" in correct: return correct.replace("No", "Yes")
                if "no" in correct: return correct.replace("no", "yes")
                if "NO" in correct: return correct.replace("NO", "YES")
                return correct.lower().replace("no", "yes")
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        potential_queries = [
            self.seq_a,
            self.seq_a_reverse,
            self.seq_b,
            self.seq_b_reverse,
            self.seq_k
        ]

        unique_queries = []
        seen = set()
        for q in potential_queries:
            if q not in seen:
                unique_queries.append(q)
                seen.add(q)

        results = []
        for q in unique_queries:
            ans_val = lcs_length(q, self.reference_seq)
            results.append({
                "query": f"<query>{q}</query>",
                "answer": str(ans_val)
            })

        return results