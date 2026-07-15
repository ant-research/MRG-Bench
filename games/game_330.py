from .base import Game

class BinaryIntervalInferenceGame(Game):

    game_rule_zh = """\
我们来玩一个"二进制区间推理"游戏，规则如下：

游戏设定了一个长度为 {n} 的未知二进制序列 B[1..{n}]，其中每个位置的值为 0 或 1。已知序列中所有值为 1 的位置恰好构成 {c} 个两两不相交的连续区间（每个区间长度大于等于 1），其余位置的值为 0。

你的目标是推断出所有值为 1 的位置索引。你可以反复向我提出区间和查询（每次仅限一个查询），我会根据真实序列如实回答：

- 区间和查询：询问区间 [L, R] 内有多少个 1（即求和）。你需要提供左端点 L 和右端点 R，满足 1 小于等于 L 小于等于 R 小于等于 {n}。我会返回该区间内 1 的总数。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。请尽可能用最少的查询次数完成推理。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 区间和查询（例如查询区间 [3, 7]）：
<query_range>3,7</query_range>

提交最终答案时，必须列出所有值为 1 的位置索引（用逗号隔开，按从小到大的顺序），格式如下：

<answer>1,2,5,6,7</answer>

注意：如果没有任何位置为 1，答案格式为：

<answer></answer>
"""

    game_rule_en = """\
Let's play a "Binary Interval Inference" game. Here are the rules:

There is an unknown binary sequence B[1..{n}] of length {n}, where each position has a value of 0 or 1. It is known that all positions with value 1 form exactly {c} disjoint contiguous intervals (each interval has length greater than or equal to 1), and all other positions have value 0.

Your goal is to infer all position indices with value 1. You can repeatedly ask me range sum queries (one query per turn), and I will answer truthfully based on the real sequence:

- Range Sum Query: Ask how many 1s are in the interval [L, R] (i.e., the sum). You need to provide the left endpoint L and right endpoint R, satisfying 1 less than or equal to L less than or equal to R less than or equal to {n}. I will return the total count of 1s in that range.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game is a failure. Try to complete the inference with as few queries as possible.

Each query must contain only one tag. Use the following XML format:

- Range Sum Query (e.g., querying interval [3, 7]):
<query_range>3,7</query_range>

When submitting the final answer, list all position indices with value 1 (comma-separated, in ascending order), using this format:

<answer>1,2,5,6,7</answer>

Note: If no positions have value 1, the answer format is:

<answer></answer>
"""

    contextualized_rule_zh_1 = """\
交通管控中心发现一段长为 {n} 公里的干线公路出现了异常情况（路段从 1 到 {n} 连续编号）。经初步勘测，有 {c} 个两两不相连的连续路段发生了严重的连环拥堵（每个拥堵区间长度至少为 1 公里）。其余路段交通畅通。

你的任务是精确定位所有拥堵路段的编号。你可以调度无人机对特定路段区间进行车流密度扫描（每次仅限一个扫描指令），系统会根据真实路况如实反馈：

- 区间探测查询：扫描区间 [L, R] 内有多少个路段处于拥堵状态。你需要提供起点 L 和终点 R，满足 1 小于等于 L 小于等于 R 小于等于 {n}。我会返回该区间内拥堵的路段总数。

当你收集足够信息后，请提交最终排查报告。若答案错误或格式不符，任务失败。请尽可能用最少的探测次数找出所有拥堵路段。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 区间和查询（例如探测区间 [3, 7]）：
<query_range>3,7</query_range>

提交最终答案时，必须列出所有拥堵路段的编号（用逗号隔开，按从小到大的顺序），格式如下：

<answer>1,2,5,6,7</answer>

注意：如果没有任何路段拥堵，答案格式为：

<answer></answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The Traffic Control Center has detected anomalies on a {n}-kilometer stretch of an arterial highway (sections sequentially numbered 1 to {n}). Preliminary surveys indicate that severe traffic congestion has occurred in exactly {c} disjoint contiguous intervals of road sections (each congested interval is at least 1 kilometer long). All other sections are flowing smoothly.

Your task is to pinpoint the indices of all congested sections. You can dispatch drones to scan the traffic density over specific ranges of sections (one command per turn), and the system will report truthfully based on real conditions:

- Range Scan Query: Scan how many sections are congested in the interval [L, R]. You need to provide the starting point L and ending point R, satisfying 1 less than or equal to L less than or equal to R less than or equal to {n}. I will return the total count of congested sections within that range.

When you have enough information, submit your final diagnostic report. If the answer is wrong or the format is invalid, the task is a failure. Please locate all congested sections with the minimum number of scans.

Each query must contain only one tag. Use the following XML format:

- Range Scan Query (e.g., scanning interval [3, 7]):
<query_range>3,7</query_range>

When submitting the final answer, list all congested section indices (comma-separated, in ascending order), using this format:

<answer>1,2,5,6,7</answer>

Note: If no sections are congested, the answer format is:

<answer></answer>
"""

    contextualized_rule_zh_2 = """\
在针对某种新型遗传病的基因测序中，我们提取了一条包含 {n} 个连续片段的DNA链（片段编号 1 到 {n}）。已知该DNA链上存在 {c} 个互不重叠的连续突变基因簇（每个突变簇包含至少 1 个突变片段），其余片段均正常。

你的目标是精准定位所有突变片段的编号以用于靶向治疗。你可以使用特异性基因探针进行区间测试（每次仅限一次测试），实验室会根据真实基因序列如实反馈：

- 区间检测查询：测试区间 [L, R] 内有多少个片段发生突变。你需要提供左端点 L 和右端点 R，满足 1 小于等于 L 小于等于 R 小于等于 {n}。我会返回该提取区间内突变片段的总数。

当你收集足够信息后，请提交最终定位结果。若答案错误或格式不符，实验失败。请在有限的试剂耗材下，尽快找出所有突变的基因片段。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 区间和查询（例如测试区间 [3, 7]）：
<query_range>3,7</query_range>

提交最终答案时，必须列出所有突变片段的编号（用逗号隔开，按从小到大的顺序），格式如下：

<answer>1,2,5,6,7</answer>

注意：如果没有任何突变片段，答案格式为：

<answer></answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
In the genetic sequencing for a novel hereditary disease, we have extracted a DNA strand comprising {n} continuous segments (numbered 1 to {n}). It is established that there are exactly {c} non-overlapping contiguous clusters of mutated genes on this strand (each cluster contains at least 1 mutated segment), while all other segments are normal.

Your goal is to precisely locate the indices of all mutated segments for targeted therapy. You can use specific gene probes to test extraction intervals (one test per turn), and the laboratory will return accurate results based on the real genetic sequence:

- Range Test Query: Test how many segments are mutated in the interval [L, R]. You need to provide the left endpoint L and right endpoint R, satisfying 1 less than or equal to L less than or equal to R less than or equal to {n}. I will return the total count of mutated segments within that extracted range.

When you have enough information, submit your final localization result. If the answer is wrong or the format is invalid, the experiment fails. Please identify all mutated gene segments as efficiently as possible with limited reagents.

Each query must contain only one tag. Use the following XML format:

- Range Test Query (e.g., testing interval [3, 7]):
<query_range>3,7</query_range>

When submitting the final answer, list all mutated segment indices (comma-separated, in ascending order), using this format:

<answer>1,2,5,6,7</answer>

Note: If no segments are mutated, the answer format is:

<answer></answer>
"""

    contextualized_rule_zh_3 = """\
在学情分析系统中，有一份包含 {n} 道题目的标准化测试卷（题号从 1 到 {n}）。通过宏观数据分析发现，某学生在作答时，在 {c} 个两两不相交的连续题目区块上存在系统性的知识盲区（即连续答错，每个盲区至少包含 1 道题），其余题目均回答正确。

你的任务是推断出所有答错题目的题号，以便为其制定个性化辅导方案。你可以向数据库发起批量批改记录查询（每次仅限一个查询指令），系统将如实反馈：

- 区间核查查询：调阅题号区间 [L, R] 内有多少道题被答错。你需要提供起始题号 L 和结束题号 R，满足 1 小于等于 L 小于等于 R 小于等于 {n}。我会返回该区间内学生答错的题目总数。

当你收集足够信息后，请提交最终盲区报告。若答案错误或格式不符，分析失败。请尽量减少查询次数，快速输出所有盲区题号。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 区间和查询（例如查询区间 [3, 7]）：
<query_range>3,7</query_range>

提交最终答案时，必须列出所有答错题目的题号（用逗号隔开，按从小到大的顺序），格式如下：

<answer>1,2,5,6,7</answer>

注意：如果没有任何题目答错，答案格式为：

<answer></answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
In the academic performance analysis system, there is a standardized test paper consisting of {n} questions (numbered 1 to {n}). Macro-data analysis reveals that a student has systematic knowledge blind spots in exactly {c} disjoint contiguous blocks of questions (i.e., answering incorrectly consecutively, with each block containing at least 1 question). All other questions were answered correctly.

Your task is to infer the indices of all incorrectly answered questions to design a personalized tutoring plan. You can query the database for batch grading records (one query per turn), and the system will provide truthful feedback:

- Range Verification Query: Check how many questions were answered incorrectly in the interval [L, R]. You need to provide the starting question L and ending question R, satisfying 1 less than or equal to L less than or equal to R less than or equal to {n}. I will return the total number of incorrectly answered questions within that range.

When you have enough information, submit your final blind spot report. If the answer is wrong or the format is invalid, the analysis fails. Please minimize your queries to quickly output all blind spot question numbers.

Each query must contain only one tag. Use the following XML format:

- Range Verification Query (e.g., querying interval [3, 7]):
<query_range>3,7</query_range>

When submitting the final answer, list all incorrectly answered question indices (comma-separated, in ascending order), using this format:

<answer>1,2,5,6,7</answer>

Note: If no questions were answered incorrectly, the answer format is:

<answer></answer>
"""

    contextualized_rule_zh_4 = """\
智能工厂的一条高压输送管道被划分为 {n} 个连续的监测节点（节点编号 1 到 {n}）。传感器报警显示，整条管道存在 {c} 个相互独立的连续泄漏区域（每个泄漏区域至少覆盖 1 个节点），其余节点运行状况良好。

你的目标是查明所有发生泄漏的节点编号以引导维修机器人进行修复。你可以通过控制台对任意节点区间进行压降差分计算（每次仅限一次计算），系统将如实反馈实际的管道状态：

- 区间差分查询：测算区间 [L, R] 内有多少个节点发生泄漏。你需要提供起始节点 L 和终止节点 R，满足 1 小于等于 L 小于等于 R 小于等于 {n}。我会返回该区间内泄漏节点的总数。

当你收集足够信息后，请提交最终排故工单。若答案错误或格式不符，维修任务失败。请用最高效的排查步骤，找出所有故障节点的位置。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 区间和查询（例如测算区间 [3, 7]）：
<query_range>3,7</query_range>

提交最终答案时，必须列出所有泄漏节点的编号（用逗号隔开，按从小到大的顺序），格式如下：

<answer>1,2,5,6,7</answer>

注意：如果没有任何节点泄漏，答案格式为：

<answer></answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
A high-pressure transmission pipeline in a smart factory is divided into {n} continuous monitoring nodes (numbered 1 to {n}). Sensor alarms indicate that there are exactly {c} independent contiguous leakage areas along the pipeline (each area covering at least 1 node), while the remaining nodes are operating normally.

Your objective is to identify the indices of all leaking nodes to guide maintenance robots for repairs. You can calculate the pressure drop differential for any node interval via the control console (one calculation per turn), and the system will report the actual pipeline status truthfully:

- Range Differential Query: Measure how many nodes are leaking in the interval [L, R]. You need to provide the starting node L and ending node R, satisfying 1 less than or equal to L less than or equal to R less than or equal to {n}. I will return the total number of leaking nodes in that interval.

When you have enough information, submit your final maintenance ticket. If the answer is wrong or the format is invalid, the repair task fails. Please use the most efficient diagnostic steps to find all faulty node locations.

Each query must contain only one tag. Use the following XML format:

- Range Differential Query (e.g., measuring interval [3, 7]):
<query_range>3,7</query_range>

When submitting the final answer, list all leaking node indices (comma-separated, in ascending order), using this format:

<answer>1,2,5,6,7</answer>

Note: If no nodes are leaking, the answer format is:

<answer></answer>
"""

    contextualized_rule_zh_5 = """\
在调查一起重大财务造假案时，专案组缴获了一本包含 {n} 页记录的加密核心账本（页码 1 到 {n}）。法务审计初步断定，账本中隐藏了 {c} 个相互独立的连续违规记录区块（每个区块至少包含 1 页违规内容），其余页面的记录均合法合规。

你的任务是固定证据，找出所有违规页的准确页码。你可以向司法辅助系统提交页码核查区间（每次仅限一次核查指令），系统会利用交叉比对算法如实反馈：

- 区间比对查询：核查页码区间 [L, R] 内有多少页包含违规记录。你需要提供起始页码 L 和结束页码 R，满足 1 小于等于 L 小于等于 R 小于等于 {n}。我会返回该区间内的违规页面总数。

当你收集足够信息后，请提交最终证据清单。若答案错误或格式不符，取证失败。请以尽可能少的核查指令完成证据链闭环，提取所有目标页码。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 区间和查询（例如核查区间 [3, 7]）：
<query_range>3,7</query_range>

提交最终答案时，必须列出所有包含违规记录的页码（用逗号隔开，按从小到大的顺序），格式如下：

<answer>1,2,5,6,7</answer>

注意：如果没有任何违规记录，答案格式为：

<answer></answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
During the investigation of a major financial fraud case, the special task force seized an encrypted core ledger containing {n} pages of records (numbered 1 to {n}). Forensic auditing preliminarily determines that the ledger conceals exactly {c} independent contiguous blocks of illicit records (each block contains at least 1 illicit page), with all other pages being strictly compliant.

Your task is to secure the evidence by identifying the exact page numbers of all illicit pages. You can submit a page verification interval to the judicial support system (one command per turn), and the system will use cross-referencing algorithms to return truthful feedback:

- Range Verification Query: Check how many illicit pages exist in the interval [L, R]. You need to provide the starting page L and ending page R, satisfying 1 less than or equal to L less than or equal to R less than or equal to {n}. I will return the total number of illicit pages within that interval.

When you have enough information, submit your final evidence list. If the answer is wrong or the format is invalid, the evidence collection fails. Please complete the evidentiary chain with as few verification commands as possible to extract all target page numbers.

Each query must contain only one tag. Use the following XML format:

- Range Verification Query (e.g., verifying interval [3, 7]):
<query_range>3,7</query_range>

When submitting the final answer, list all illicit page indices (comma-separated, in ascending order), using this format:

<answer>1,2,5,6,7</answer>

Note: If no pages are illicit, the answer format is:

<answer></answer>
"""

    tags = ["answer", "query_range"]

    reasoning_type = "演绎推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 8,
                "c": 1,
                "intervals": [(3, 5)],
            },
            2: {
                "n": 16,
                "c": 2,
                "intervals": [(2, 4), (10, 13)],
            },
            3: {
                "n": 32,
                "c": 3,
                "intervals": [(5, 8), (15, 18), (25, 27)],
            },
            4: {
                "n": 64,
                "c": 4,
                "intervals": [(8, 12), (20, 25), (35, 40), (50, 56)],
            },
            5: {
                "n": 100,
                "c": 5,
                "intervals": [(5, 10), (22, 28), (45, 50), (65, 72), (85, 92)],
            },
        },
        "en": {
            1: {
                "n": 8,
                "c": 1,
                "intervals": [(3, 5)],
            },
            2: {
                "n": 16,
                "c": 2,
                "intervals": [(2, 4), (10, 13)],
            },
            3: {
                "n": 32,
                "c": 3,
                "intervals": [(5, 8), (15, 18), (25, 27)],
            },
            4: {
                "n": 64,
                "c": 4,
                "intervals": [(8, 12), (20, 25), (35, 40), (50, 56)],
            },
            5: {
                "n": 100,
                "c": 5,
                "intervals": [(5, 10), (22, 28), (45, 50), (65, 72), (85, 92)],
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
        self._game_info["c"] = cfg["c"]
        
        self.n = cfg["n"]
        self.c = cfg["c"]
        self.intervals = cfg["intervals"]
        
        self.binary_sequence = {i: 0 for i in range(1, self.n + 1)}
        
        for (left, right) in self.intervals:
            for i in range(left, right + 1):
                self.binary_sequence[i] = 1
        
        self.ground_truth = set(i for i in range(1, self.n + 1) if self.binary_sequence[i] == 1)
        
        self.query_count = 0

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        if raw_ans == "":
            model_answer = set()
        else:
            try:
                indices = [x.strip() for x in raw_ans.split(",") if x.strip()]
                model_answer = set(int(idx) for idx in indices)
            except:
                return False
        
        return model_answer == self.ground_truth

    def _cf_core_produce(self, parsed_info):
        if "query_range" in parsed_info:
            self.query_count += 1
            
            try:
                raw = parsed_info["query_range"].strip()
                parts = [x.strip() for x in raw.split(",")]
                
                if len(parts) != 2:
                    raise ValueError("Query format error")
                
                left = int(parts[0])
                right = int(parts[1])
                
                if left < 1 or right > self.n or left > right:
                    if self.config.language == "zh":
                        return f"错误：查询区间无效。L 和 R 必须满足 1 <= L <= R <= {self.n}。"
                    else:
                        return f"Error: Invalid query range. L and R must satisfy 1 <= L <= R <= {self.n}."
                
                range_sum = sum(self.binary_sequence[i] for i in range(left, right + 1))
                
                return str(range_sum)
                
            except ValueError:
                if self.config.language == "zh":
                    return "错误：查询格式无效。请使用格式 <query_range>L,R</query_range>。"
                else:
                    return "Error: Invalid query format. Please use format <query_range>L,R</query_range>."
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        try:
            val = int(correct)
            return str(val + 1)
        except ValueError:
            pass

        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        else:
            lower_c = correct.lower()
            if "yes" in lower_c:
                if correct == "Yes": return "No"
                if correct == "YES": return "NO"
                if correct == "yes": return "no"
                return correct.replace("Yes", "No").replace("yes", "no")
            elif "no" in lower_c:
                if correct == "No": return "Yes"
                if correct == "NO": return "YES"
                if correct == "no": return "yes"
                return correct.replace("No", "Yes").replace("no", "yes")
        
        return correct + "_WRONG"

    def get_all_possible_queries(self):
        possible_queries = []
        for l in range(1, self.n + 1):
            for r in range(l, self.n + 1):
                query_content = f"<query_range>{l},{r}</query_range>"
                
                range_sum = sum(self.binary_sequence[i] for i in range(l, r + 1))
                
                possible_queries.append({
                    "query": query_content,
                    "answer": str(range_sum)
                })
        
        return possible_queries