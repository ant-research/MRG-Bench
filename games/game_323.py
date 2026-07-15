import itertools
import random as _random
from .base import Game

class HiddenSubsetGame(Game):

    contextualized_rule_zh_1 = """\
[交通场景] 
交通指挥中心系统正面临多处隐蔽的通信节点故障。城市交通网包含编号从 1 到 {n} 的核心路段。其中有一个隐蔽的故障路段集合 A（真子集）正在引发全局性拥堵。你的目标是通过交互式查询，精准定位出所有故障路段 A 的确切内容。

你可以反复进行以下类型的查询：

**封闭测试查询**：你提出一个路段子集 R（通过列举编号进行临时封闭），诊断反馈为 0 或 1：
- 答案为 0：表示封闭 R 后，剩余路网恢复通畅（即故障路段 A 完全包含在 R 中）
- 答案为 1：表示封闭 R 后，剩余路网仍有拥堵（即故障路段 A 不完全包含在 R 中）

换句话说，这个查询等价于询问"被封闭的 R 是否包含了所有的故障路段 A"：
- 答案 0 表示"是"（R 包含了 A 的所有路段）
- 答案 1 表示"否"（R 没有包含 A 的所有路段）

当你收集到足够信息后，可以提交最终答案。若答案完全正确则排查成功，否则任务失败。

进行封闭测试查询时，列出要封闭的路段编号（用逗号隔开），使用以下 XML 格式：

<query_delete>2,5,7</query_delete>

如果查询空集（即不封闭任何路段），可以留空或写 empty：

<query_delete></query_delete>

或

<query_delete>empty</query_delete>

提交最终答案时，列出你认为存在故障的所有路段编号（用逗号隔开，顺序不限），格式如下：

<answer>1,3,6</answer>

注意：
- 每次只能进行一个查询或提交一次答案
- 请尽可能用最少的查询次数定位故障点
- 故障路段集合 A 至少包含 1 个路段
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The traffic control center is facing multiple hidden communication node failures. The urban traffic network contains core road segments numbered from 1 to {n}. A hidden set of faulty segments A (a proper subset) is causing global congestion. Your goal is to accurately locate all faulty segments A through interactive queries.

You can repeatedly perform the following type of query:

**Closure Test Query**: You propose a subset of segments R (by listing segment IDs for temporary closure), and the diagnostic system will return 0 or 1:
- Answer 0: After closing R, the remaining network flows smoothly (i.e., faulty segments A are completely contained in R)
- Answer 1: After closing R, congestion persists in the remaining network (i.e., A is not completely contained in R)

In other words, this query is equivalent to asking "Does the closed subset R contain all faulty segments A":
- Answer 0 means "Yes" (R contains all faulty segments of A)
- Answer 1 means "No" (R does not contain all faulty segments of A)

When you have gathered enough information, you can submit your final answer. If the answer is completely correct, the troubleshooting succeeds; otherwise, it fails.

To perform a closure test query, list the segment IDs to be closed (comma-separated), using the following XML format:

<query_delete>2,5,7</query_delete>

If querying the empty set (i.e., not closing any segments), you can leave it empty or write empty:

<query_delete></query_delete>

or

<query_delete>empty</query_delete>

When submitting the final answer, list all segment IDs you believe are faulty (comma-separated, order does not matter), using this format:

<answer>1,3,6</answer>

Note:
- You can only perform one query or submit one answer at a time
- Try to locate the faults with the minimum number of queries
- The faulty set A contains at least 1 segment
"""

    contextualized_rule_zh_2 = """\
[医疗场景]
疾控中心正在排查一种由多种未知病原体复合感染的病例。样本中锁定了编号从 1 到 {n} 的可疑微生物。其中有一个致病组合 A（真子集）是真正的感染源。你的目标是通过交互式靶向消除测试，推断出致病组合 A 的确切内容。

你可以反复进行以下类型的查询：

**靶向消除查询**：你提出一个微生物子集 R 并使用特效抗生素将其消除（通过列举编号），系统反馈为 0 或 1：
- 答案为 0：表示消除 R 后，剩余样本不再具备致病性（即致病组合 A 完全包含在 R 中）
- 答案为 1：表示消除 R 后，剩余样本仍有致病性（即致病组合 A 不完全包含在 R 中）

换句话说，这个查询等价于询问"被消除的 R 是否覆盖了所有的致病原 A"：
- 答案 0 表示"是"（R 包含了 A 的所有微生物）
- 答案 1 表示"否"（R 没有包含 A 的所有微生物）

当你收集到足够信息后，可以提交最终答案。若答案完全正确则排查成功，否则任务失败。

进行靶向消除查询时，列出要消除的微生物编号（用逗号隔开），使用以下 XML 格式：

<query_delete>2,5,7</query_delete>

如果查询空集（即不消除任何微生物），可以留空或写 empty：

<query_delete></query_delete>

或

<query_delete>empty</query_delete>

提交最终答案时，列出你认为属于感染源的所有微生物编号（用逗号隔开，顺序不限），格式如下：

<answer>1,3,6</answer>

注意：
- 每次只能进行一个查询或提交一次答案
- 请尽可能用最少的查询次数找到致病源
- 致病组合 A 至少包含 1 个微生物
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
The CDC is investigating a case of complex infection caused by multiple unknown pathogens. Suspicious microorganisms numbered from 1 to {n} have been isolated in the sample. A pathogenic combination A (a proper subset) is the true source of infection. Your goal is to infer the exact content of combination A through interactive targeted elimination tests.

You can repeatedly perform the following type of query:

**Targeted Elimination Query**: You propose a subset of microorganisms R to be eliminated using specific antibiotics (by listing IDs), and the system returns 0 or 1:
- Answer 0: After eliminating R, the remaining sample shows no pathogenicity (i.e., combination A is completely contained in R)
- Answer 1: After eliminating R, the remaining sample still exhibits pathogenicity (i.e., A is not completely contained in R)

In other words, this query is equivalent to asking "Does the eliminated subset R cover all pathogens A":
- Answer 0 means "Yes" (R contains all pathogens of A)
- Answer 1 means "No" (R does not contain all pathogens of A)

When you have gathered enough information, you can submit your final answer. If the answer is completely correct, the investigation succeeds; otherwise, it fails.

To perform an elimination query, list the microorganism IDs to be eliminated (comma-separated), using the following XML format:

<query_delete>2,5,7</query_delete>

If querying the empty set (i.e., not eliminating any microorganisms), you can leave it empty or write empty:

<query_delete></query_delete>

or

<query_delete>empty</query_delete>

When submitting the final answer, list all microorganism IDs you believe are the infection source (comma-separated, order does not matter), using this format:

<answer>1,3,6</answer>

Note:
- You can only perform one query or submit one answer at a time
- Try to find the source with the minimum number of queries
- Combination A contains at least 1 microorganism
"""

    contextualized_rule_zh_3 = """\
[教育场景]
自适应学习平台需要精准定位学生在某科目的核心知识盲区。本次测试覆盖了编号从 1 到 {n} 的核心知识点。某位学生存在一个未掌握的知识盲区集合 A（真子集），导致其综合测评不达标。你的目标是通过交互式强化辅导测试，精准找出盲区 A 的确切内容。

你可以反复进行以下类型的查询：

**强化辅导查询**：你选定一个知识点子集 R 对学生进行突击补习（相当于在测评中消除这些盲区），系统反馈 0 或 1：
- 答案为 0：表示补习 R 后，该生在剩余知识点上的综合测评满分通过（即盲区 A 完全包含在补习范围 R 中）
- 答案为 1：表示补习 R 后，该生仍会做错题（即盲区 A 不完全包含在补习范围 R 中）

换句话说，这个查询等价于询问"突击补习的 R 是否覆盖了所有的知识盲区 A"：
- 答案 0 表示"是"（R 包含了 A 的所有盲区）
- 答案 1 表示"否"（R 没有包含 A 的所有盲区）

当你收集到足够信息后，可以提交最终答案。若答案完全正确则定位成功，否则任务失败。

进行强化辅导查询时，列出要突击补习的知识点编号（用逗号隔开），使用以下 XML 格式：

<query_delete>2,5,7</query_delete>

如果查询空集（即不进行任何补习），可以留空或写 empty：

<query_delete></query_delete>

或

<query_delete>empty</query_delete>

提交最终答案时，列出你认为属于该生盲区的所有知识点编号（用逗号隔开，顺序不限），格式如下：

<answer>1,3,6</answer>

注意：
- 每次只能进行一个查询或提交一次答案
- 请尽可能用最少的查询次数定位盲区
- 知识盲区集合 A 至少包含 1 个知识点
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The adaptive learning platform needs to accurately pinpoint a student's core knowledge blind spots. The comprehensive assessment covers core concepts numbered from 1 to {n}. A student has a hidden set of unmastered blind spots A (a proper subset) causing them to fail the assessment. Your goal is to pinpoint the exact content of blind spots A through interactive remedial tutoring tests.

You can repeatedly perform the following type of query:

**Remedial Tutoring Query**: You select a subset of concepts R to intensively tutor the student (effectively eliminating these blind spots in the assessment), and the system returns 0 or 1:
- Answer 0: After tutoring R, the student passes the remaining assessment perfectly (i.e., blind spots A are completely contained in R)
- Answer 1: After tutoring R, the student still makes errors (i.e., A is not completely contained in R)

In other words, this query is equivalent to asking "Does the tutored subset R cover all blind spots A":
- Answer 0 means "Yes" (R contains all blind spots of A)
- Answer 1 means "No" (R does not contain all blind spots of A)

When you have gathered enough information, you can submit your final answer. If the answer is completely correct, the targeting succeeds; otherwise, it fails.

To perform a remedial tutoring query, list the concept IDs to be tutored (comma-separated), using the following XML format:

<query_delete>2,5,7</query_delete>

If querying the empty set (i.e., no tutoring), you can leave it empty or write empty:

<query_delete></query_delete>

or

<query_delete>empty</query_delete>

When submitting the final answer, list all concept IDs you believe are the student's blind spots (comma-separated, order does not matter), using this format:

<answer>1,3,6</answer>

Note:
- You can only perform one query or submit one answer at a time
- Try to locate the blind spots with the minimum number of queries
- The blind spot set A contains at least 1 concept
"""

    contextualized_rule_zh_4 = """\
[制造场景]
精密制造车间的一台核心机床发生停机故障。该设备包含编号从 1 到 {n} 的可疑功能模块。其中有一个损坏的模块集合 A（真子集）导致了系统失效。你的目标是通过交互式替换测试，揪出所有损坏模块 A 的确切内容。

你可以反复进行以下类型的查询：

**模块替换查询**：你提出一个模块子集 R 进行整体无缺陷替换下线（通过列举编号），测试运转反馈为 0 或 1：
- 答案为 0：表示替换 R 后，使用剩余原有模块开机，设备运转正常（即损坏模块 A 完全包含在替换名单 R 中）
- 答案为 1：表示替换 R 后，设备依然报错停机（即损坏模块 A 不完全包含在替换名单 R 中）

换句话说，这个查询等价于询问"被替换下线的 R 是否囊括了所有损坏模块 A"：
- 答案 0 表示"是"（R 包含了 A 的所有损坏模块）
- 答案 1 表示"否"（R 没有包含 A 的所有损坏模块）

当你收集到足够信息后，可以提交最终答案。若答案完全正确则排查成功，否则任务失败。

进行模块替换查询时，列出要替换的模块编号（用逗号隔开），使用以下 XML 格式：

<query_delete>2,5,7</query_delete>

如果查询空集（即不替换任何模块），可以留空或写 empty：

<query_delete></query_delete>

或

<query_delete>empty</query_delete>

提交最终答案时，列出你认为存在损坏的所有模块编号（用逗号隔开，顺序不限），格式如下：

<answer>1,3,6</answer>

注意：
- 每次只能进行一个查询或提交一次答案
- 请尽可能用最少的查询次数锁定损坏模块
- 损坏模块集合 A 至少包含 1 个模块
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
A core machine tool in the precision manufacturing workshop has shut down due to a fault. The equipment contains suspicious functional modules numbered from 1 to {n}. A broken module set A (a proper subset) has caused the system failure. Your goal is to find the exact content of all broken modules A through interactive replacement tests.

You can repeatedly perform the following type of query:

**Module Replacement Query**: You propose a subset of modules R to be completely replaced with known-good parts (by listing IDs), and the test run returns 0 or 1:
- Answer 0: After replacing R, the machine runs normally with the remaining original modules (i.e., broken modules A are completely contained in R)
- Answer 1: After replacing R, the machine still reports an error and halts (i.e., A is not completely contained in R)

In other words, this query is equivalent to asking "Does the replaced subset R encompass all broken modules A":
- Answer 0 means "Yes" (R contains all broken modules of A)
- Answer 1 means "No" (R does not contain all broken modules of A)

When you have gathered enough information, you can submit your final answer. If the answer is completely correct, the troubleshooting succeeds; otherwise, it fails.

To perform a module replacement query, list the module IDs to be replaced (comma-separated), using the following XML format:

<query_delete>2,5,7</query_delete>

If querying the empty set (i.e., not replacing any modules), you can leave it empty or write empty:

<query_delete></query_delete>

or

<query_delete>empty</query_delete>

When submitting the final answer, list all module IDs you believe are broken (comma-separated, order does not matter), using this format:

<answer>1,3,6</answer>

Note:
- You can only perform one query or submit one answer at a time
- Try to locate the broken modules with the minimum number of queries
- The broken module set A contains at least 1 module
"""

    contextualized_rule_zh_5 = """\
[法律场景]
合规审查系统正在评估一份长篇商业合同。该合同包含编号从 1 到 {n} 的高危条款。其中隐匿了一个违规条款集合 A（真子集），导致合同无法通过反垄断审查。你的目标是通过交互式删减测试，揪出所有违规条款 A 的确切内容。

你可以反复进行以下类型的查询：

**删减送审查询**：你提出一个条款子集 R 将其从合同中暂时剔除（通过列举编号），系统反馈审查结果为 0 或 1：
- 答案为 0：表示删减 R 后，剩余合同顺利通过合规审查（即违规条款 A 已完全包含在被删减的 R 中）
- 答案为 1：表示删减 R 后，剩余合同仍存在违规风险无法通过（即违规条款 A 不完全包含在被删减的 R 中）

换句话说，这个查询等价于询问"被剔除的条款 R 是否涵盖了所有违规条款 A"：
- 答案 0 表示"是"（R 包含了 A 的所有违规条款）
- 答案 1 表示"否"（R 没有包含 A 的所有违规条款）

当你收集到足够信息后，可以提交最终答案。若答案完全正确则审查成功，否则任务失败。

进行删减送审查询时，列出要删减的条款编号（用逗号隔开），使用以下 XML 格式：

<query_delete>2,5,7</query_delete>

如果查询空集（即不删减任何条款），可以留空或写 empty：

<query_delete></query_delete>

或

<query_delete>empty</query_delete>

提交最终答案时，列出你认为存在违规的所有条款编号（用逗号隔开，顺序不限），格式如下：

<answer>1,3,6</answer>

注意：
- 每次只能进行一个查询或提交一次答案
- 请尽可能用最少的查询次数揪出所有违规条款
- 违规条款集合 A 至少包含 1 个条款
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
The compliance review system is evaluating a lengthy commercial contract. The contract contains high-risk clauses numbered from 1 to {n}. A hidden set of illegal clauses A (a proper subset) prevents it from passing antitrust review. Your goal is to expose the exact content of all illegal clauses A through interactive redaction tests.

You can repeatedly perform the following type of query:

**Redaction Review Query**: You propose a subset of clauses R to be temporarily redacted from the contract (by listing IDs), and the review system returns 0 or 1:
- Answer 0: After redacting R, the remaining contract passes the compliance review (i.e., illegal clauses A are completely contained in R)
- Answer 1: After redacting R, the remaining contract still holds compliance risks (i.e., A is not completely contained in R)

In other words, this query is equivalent to asking "Does the redacted subset R cover all illegal clauses A":
- Answer 0 means "Yes" (R contains all illegal clauses of A)
- Answer 1 means "No" (R does not contain all illegal clauses of A)

When you have gathered enough information, you can submit your final answer. If the answer is completely correct, the review succeeds; otherwise, it fails.

To perform a redaction review query, list the clause IDs to be redacted (comma-separated), using the following XML format:

<query_delete>2,5,7</query_delete>

If querying the empty set (i.e., not redacting any clauses), you can leave it empty or write empty:

<query_delete></query_delete>

or

<query_delete>empty</query_delete>

When submitting the final answer, list all clause IDs you believe are illegal (comma-separated, order does not matter), using this format:

<answer>1,3,6</answer>

Note:
- You can only perform one query or submit one answer at a time
- Try to expose the illegal clauses with the minimum number of queries
- The illegal clause set A contains at least 1 clause
"""

    game_rule_zh = contextualized_rule_zh_1
    game_rule_en = contextualized_rule_en_1

    tags = ["answer", "query_delete"]

    reasoning_type = "演绎推理"
    data_structure = "集合"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"n": 4, "hidden_size": 1},
            2: {"n": 6, "hidden_size": 2},
            3: {"n": 8, "hidden_size": 3},
            4: {"n": 10, "hidden_size": 4},
            5: {"n": 12, "hidden_size": 5},
        },
        "en": {
            1: {"n": 4, "hidden_size": 1},
            2: {"n": 6, "hidden_size": 2},
            3: {"n": 8, "hidden_size": 3},
            4: {"n": 10, "hidden_size": 4},
            5: {"n": 12, "hidden_size": 5},
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
        hidden_size = cfg["hidden_size"]
        
        self._game_info["n"] = n
        
        rng = _random.Random(42 + diff * 1000 + n)
        all_elements = list(range(1, n + 1))
        hidden_elements = rng.sample(all_elements, hidden_size)
        
        self.hidden_subset = set(str(x) for x in hidden_elements)
        self.full_set = set(str(i) for i in range(1, n + 1))
        
        if not self.hidden_subset:
            raise ValueError("Hidden subset cannot be empty")
        if not self.hidden_subset.issubset(self.full_set):
            raise ValueError("Hidden subset must be a subset of the full set")
        if self.hidden_subset == self.full_set:
            raise ValueError("Hidden subset must be a PROPER subset of the full set (cannot equal the full set)")

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        if not raw_ans:
            return False
        
        try:
            player_subset = set(x.strip() for x in raw_ans.split(",") if x.strip())
        except:
            return False
        
        return player_subset == self.hidden_subset

    def _cf_make_wrong(self, correct: str) -> str:
        if correct == "0":
            return "1"
        elif correct == "1":
            return "0"
        else:
            return "0"

    def _cf_core_produce(self, parsed_info):
        if "query_delete" in parsed_info:
            raw_query = parsed_info["query_delete"].strip()
            
            if not raw_query or raw_query.lower() == "empty":
                R = set()
            else:
                try:
                    R = set(x.strip() for x in raw_query.split(",") if x.strip())
                except:
                    if self.config.language == "zh":
                        return "错误：查询格式无效。"
                    else:
                        return "Error: Invalid query format."
                
                if not R.issubset(self.full_set):
                    if self.config.language == "zh":
                        return "错误：查询中包含超出范围的编号。"
                    else:
                        return "Error: Query contains IDs out of range."
            
            remaining = self.full_set - R
            
            has_intersection = bool(remaining & self.hidden_subset)
            
            if has_intersection:
                return "1"
            else:
                return "0"
        else:
            if self.config.language == "zh":
                return "错误：未找到有效的查询标签。"
            else:
                return "Error: No valid query tag found."

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        sorted_elements = sorted(list(self.full_set), key=lambda x: int(x))
        n_elements = len(sorted_elements)
        
        MAX_QUERIES = 512
        
        all_subsets = []
        if 2 ** n_elements <= MAX_QUERIES:
            for r in range(n_elements + 1):
                for subset in itertools.combinations(sorted_elements, r):
                    all_subsets.append(subset)
        else:
            all_subsets.append(())
            for r in range(1, n_elements + 1):
                for subset in itertools.combinations(sorted_elements, r):
                    all_subsets.append(subset)
                    if len(all_subsets) >= MAX_QUERIES - 1:
                        break
                if len(all_subsets) >= MAX_QUERIES - 1:
                    break
            all_subsets.append(tuple(sorted_elements))
        
        for subset in all_subsets:
            R = set(subset)
            
            if not R:
                query_content = "empty"
            else:
                query_content = ",".join(subset)
            
            query_str = f"<query_delete>{query_content}</query_delete>"
            
            
            remaining = self.full_set - R
            
            has_intersection = bool(remaining & self.hidden_subset)
            
            if has_intersection:
                ans = "1"
            else:
                ans = "0"
                
            results.append({
                "query": query_str,
                "answer": ans
            })
                
        return results