import random
from .base import Game

class ThresholdBinarySearchGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "序列"

    game_rule_zh = """\
我们现在来玩一个"阈值推理"游戏，规则如下：

游戏设定了四个参数：
- N：序列长度
- k：后缀长度
- B：序列元素的上界
- Q：最大操作次数

我已秘密生成了一个长度为 N 的有序序列 S，其中每个元素都是 0 到 B 之间的整数。你的目标是推断出一个特定的目标值 H，它等于序列 S 的最后 k 个元素之和。显然，H 的取值范围在 0 到 k·B 之间。

你可以进行以下两种操作：

1. 阈值比较查询：选择一个整数 T，我会告诉你目标值 H 是否大于等于 T。
2. 最终断言：当你认为已经收集到足够信息时，提交一个整数 V 作为你对 H 的最终判断。

注意：
- 每次查询和最终断言都会计入操作次数，总操作次数不能超过 Q 次。
- 一旦提交最终断言，游戏立即结束。
- 如果最终断言正确（V 等于 H），你获胜；否则失败。
- 如果超过 Q 次操作仍未提交最终断言，游戏失败。

当前游戏参数：
- N = {N}
- k = {k}
- B = {B}
- Q = {Q}

每次只能进行一种操作。请使用以下 XML 格式：

- 阈值比较查询（例如询问 H 是否大于等于 10）：
<query_threshold>10</query_threshold>

- 提交最终断言（例如断言 H 等于 15）：
<answer>15</answer>

请尽可能用少的操作次数找出正确答案。
"""

    game_rule_en = """\
Let's play a "Threshold Inference" game. Here are the rules:

The game has four parameters:
- N: Sequence length
- k: Suffix length
- B: Upper bound for sequence elements
- Q: Maximum number of operations

I have secretly generated an ordered sequence S of length N, where each element is an integer between 0 and B. Your goal is to infer a specific target value H, which equals the sum of the last k elements of sequence S. Clearly, H ranges from 0 to k·B.

You can perform the following two types of operations:

1. Threshold Comparison Query: Choose an integer T, and I will tell you whether the target value H is greater than or equal to T.
2. Final Assertion: When you believe you have gathered enough information, submit an integer V as your final judgment of H.

Notes:
- Each query and final assertion counts toward the operation limit, and the total cannot exceed Q operations.
- Once you submit a final assertion, the game ends immediately.
- If the final assertion is correct (V equals H), you win; otherwise, you fail.
- If you exceed Q operations without submitting a final assertion, the game fails.

Current game parameters:
- N = {N}
- k = {k}
- B = {B}
- Q = {Q}

You can only perform one operation at a time. Use the following XML format:

- Threshold Comparison Query (e.g., asking if H is greater than or equal to 10):
<query_threshold>10</query_threshold>

- Submit Final Assertion (e.g., asserting H equals 15):
<answer>15</answer>

Try to find the correct answer with as few operations as possible.
"""

    contextualized_rule_zh_1 = """\
智能交通控制中心正在运行路网拥堵评估协议。

系统已接入一条主干道的连续 {N} 个路口的流量历史数据，并重点监控末端最核心的 {k} 个路口。每个路口的拥堵指数最高为 {B}。
你的任务是推算出这 {k} 个核心路口的累计拥堵总指数 H。该指数关系到是否启动全市分流预案，显然 H 的取值范围在 0 到 {k}·{B} 之间。

为节约算力，你最多拥有 {Q} 次系统调用权限，可执行以下操作：

1. 负荷预警查询：输入一个预警阈值 T，系统会反馈累计指数 H 是否大于等于 T。
2. 最终定级报告：当你确认了 H 的精确值时，提交整数 V 作为最终的评估结果。

注意：
- 每次查询和报告提交都会消耗调用次数，上限为 {Q} 次。
- 提交报告后评估立即终止。
- 若报告的 V 等于真实指数 H，路网调度成功；否则将引发大面积拥堵，评估失败。
- 耗尽 {Q} 次权限未出结果也会导致系统超时失败。

当前评估参数：
- 监测路口总数 N = {N}
- 核心路口数 k = {k}
- 单路口指数上限 B = {B}
- 可调用次数 Q = {Q}

每次仅限执行一次指令。请使用以下 XML 格式：

- 负荷预警查询（例如查明 H 是否大于等于 10）：
<query_threshold>10</query_threshold>

- 提交最终定级报告（例如断定 H 等于 15）：
<answer>15</answer>

请以最优的策略尽快完成调度评估。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The Intelligent Traffic Control Center is running a network congestion assessment protocol.

The system has integrated historical traffic data from a sequence of {N} intersections along a main arterial road, focusing heavily on the {k} core intersections at the terminal end. The congestion index for each intersection is capped at {B}.
Your task is to deduce the cumulative congestion index H for these {k} core intersections. This index determines whether to activate the city-wide diversion contingency plan. Clearly, H ranges from 0 to {k}·{B}.

To conserve computational resources, you have a maximum of {Q} system API calls to perform the following operations:

1. Load Warning Query: Submit a warning threshold T, and the system will report whether the cumulative index H is greater than or equal to T.
2. Final Grading Report: Once you determine the exact value of H, submit an integer V as the final assessment.

Notes:
- Each query and final report submission counts towards the call limit, which cannot exceed {Q} operations.
- Once the final report is submitted, the assessment terminates immediately.
- If the submitted V equals the actual H, traffic routing succeeds; otherwise, it triggers massive gridlock, and the assessment fails.
- Exceeding {Q} calls without a result leads to a system timeout failure.

Current assessment parameters:
- Total monitored intersections N = {N}
- Core intersections k = {k}
- Single intersection index cap B = {B}
- Maximum API calls Q = {Q}

You may only execute one command at a time. Use the following XML format:

- Load Warning Query (e.g., asking if H is greater than or equal to 10):
<query_threshold>10</query_threshold>

- Submit Final Grading Report (e.g., asserting H equals 15):
<answer>15</answer>

Please complete the routing assessment efficiently.
"""

    contextualized_rule_zh_2 = """\
重症监护室(ICU)患者生命体征监测系统已启动风险排查程序。

系统连续记录了患者的 {N} 个时间节点的生理特征数据，并聚焦于近期最危险的 {k} 个观察期。每个节点的单次异常血液指标峰值上限为 {B}。
你的任务是推断这 {k} 个近期观察期内的累计异常指标总值 H，以此决定是否需要介入紧急手术。显然，H 的取值范围在 0 到 {k}·{B} 之间。

为了抢救时间，你最多只能进行 {Q} 次系统交互操作：

1. 风险阈值排查：输入一个风险阈值 T，系统会反馈累计异常总值 H 是否大于等于 T。
2. 最终病理诊断：当你确认了 H 的精确值时，提交整数 V 作为最终的风险诊断结论。

注意：
- 每次排查和诊断提交均计入操作次数，总操作不可超过 {Q} 次。
- 提交最终病理诊断后，排查程序立即结束。
- 若诊断正确（V 等于 H），患者得到有效救治；否则延误病情，排查失败。
- 若操作超过 {Q} 次仍未得出结论，患者将错过最佳干预窗口。

当前系统参数：
- 监测节点总数 N = {N}
- 关键观察期数 k = {k}
- 指标峰值上限 B = {B}
- 最大操作次数 Q = {Q}

每次仅能执行一项操作。请使用以下 XML 格式：

- 风险阈值排查（例如查明 H 是否大于等于 10）：
<query_threshold>10</query_threshold>

- 提交最终病理诊断（例如断言 H 等于 15）：
<answer>15</answer>

请尽快完成排查，锁定正确的异常总值。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
The Intensive Care Unit (ICU) patient vital signs monitoring system has initiated a risk screening procedure.

The system has continuously recorded physiological data across {N} sequential time nodes, zooming in on the {k} most critical recent observation periods. The maximum abnormal blood indicator peak for a single node is {B}.
Your objective is to infer the cumulative abnormal indicator total H during these {k} observation periods, which dictates whether emergency surgical intervention is required. Naturally, H ranges from 0 to {k}·{B}.

To save precious time, you are permitted a maximum of {Q} system interactions:

1. Risk Threshold Screening: Input a risk threshold T, and the system will verify if the cumulative total H is greater than or equal to T.
2. Final Pathological Diagnosis: When you are certain of the exact value of H, submit an integer V as the ultimate diagnostic conclusion.

Notes:
- Every screening query and diagnostic submission counts toward your limit of {Q} operations.
- Submitting the final diagnosis immediately ends the screening procedure.
- If the diagnosis is correct (V equals H), the patient receives proper care; otherwise, treatment is delayed, and the screening fails.
- Exceeding {Q} operations without a diagnosis means the optimal intervention window is lost.

Current system parameters:
- Total monitored nodes N = {N}
- Critical observation periods k = {k}
- Indicator peak upper bound B = {B}
- Maximum operations Q = {Q}

Execute only one operation at a time. Use the following XML format:

- Risk Threshold Screening (e.g., asking if H is greater than or equal to 10):
<query_threshold>10</query_threshold>

- Submit Final Pathological Diagnosis (e.g., asserting H equals 15):
<answer>15</answer>

Please complete the screening promptly and pinpoint the exact indicator total.
"""

    contextualized_rule_zh_3 = """\
自适应学习平台正在进行学情追踪与知识点漏洞分析。

系统收录了学生本学期的 {N} 次标准化测试成绩，并聚焦于期末冲刺阶段的最后 {k} 次测试。单次测试中，知识点遗漏最高数量为 {B}。
你需要计算出冲刺阶段的累计知识点遗漏总数 H，以便生成个性化的复习方案。显然，H 的取值范围在 0 到 {k}·{B} 之间。

为避免过度占用诊断资源，你最多允许进行 {Q} 次交互：

1. 短板阈值评估：输入一个评估阈值 T，平台会反馈累计遗漏总数 H 是否大于等于 T。
2. 学情定位报告：当你准确定位了 H 的数值时，提交整数 V 作为最终的知识漏洞报告。

注意：
- 每次评估查询和报告提交均计入限额，总操作不得超过 {Q} 次。
- 提交学情定位报告后，诊断会立即结束。
- 如果报告的数据准确（V 等于 H），复习方案生成成功；否则分析偏离，诊断失败。
- 若达到 {Q} 次操作仍未定位问题，分析进程将强制中止。

当前学情参数：
- 标准测试总次数 N = {N}
- 冲刺阶段测试数 k = {k}
- 单次测试遗漏上限 B = {B}
- 允许交互次数 Q = {Q}

每次仅可进行一种交互。请使用以下 XML 格式：

- 短板阈值评估（例如查明 H 是否大于等于 10）：
<query_threshold>10</query_threshold>

- 提交学情定位报告（例如断定 H 等于 15）：
<answer>15</answer>

请运用严谨的逻辑推导，找出最精确的遗漏总数。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The Adaptive Learning Platform is tracking academic progress and analyzing knowledge gaps.

The system has logged scores from {N} standardized tests taken this semester, placing particular emphasis on the final {k} tests during the sprint period. The maximum number of missing knowledge points in a single test is {B}.
You must calculate the cumulative number of missing knowledge points H during this sprint phase to generate a personalized review plan. Clearly, H ranges from 0 to {k}·{B}.

To prevent overloading the diagnostic server, you are limited to {Q} interactions:

1. Weakness Threshold Assessment: Input an evaluation threshold T, and the platform will state whether the cumulative missing points H is greater than or equal to T.
2. Academic Gap Report: Once you have pinpointed the exact value of H, submit an integer V as your final knowledge gap report.

Notes:
- Both threshold assessments and report submissions consume your interaction quota of {Q} operations.
- The diagnostic process terminates immediately after submitting the gap report.
- If the report is perfectly accurate (V equals H), the review plan is successfully generated; otherwise, the analysis derails, and the diagnosis fails.
- Failing to resolve the gap within {Q} operations forces an abort of the analysis.

Current academic parameters:
- Total standardized tests N = {N}
- Sprint phase tests k = {k}
- Missing points cap per test B = {B}
- Allowed interactions Q = {Q}

You may perform only one interaction at a time. Use the following XML format:

- Weakness Threshold Assessment (e.g., asking if H is greater than or equal to 10):
<query_threshold>10</query_threshold>

- Submit Academic Gap Report (e.g., asserting H equals 15):
<answer>15</answer>

Please employ strict deductive logic to uncover the exact total of missing points.
"""

    contextualized_rule_zh_4 = """\
自动化精密零件生产线的质量控制模块正在进行例行排查。

质检系统抽检了流水线上的 {N} 个生产批次，当前需要重点评估最新下线的 {k} 个关键批次。单批次允许的最大微小瑕疵数为 {B}。
你的任务是推算出这 {k} 个核心批次的累计瑕疵总数 H，以此决定是否需要触发停机维护程序。显然，H 的范围在 0 到 {k}·{B} 之间。

为保证生产节奏，你最多只能进行 {Q} 次检测指令下达：

1. 公差阈值检测：输入一个公差阈值 T，控制模块会反馈累计瑕疵总数 H 是否大于等于 T。
2. 批次检验结论：当你确认了 H 的精确总数时，提交整数 V 作为最终的质量检验结果。

注意：
- 每次阈值检测和结论提交都会计入指令消耗，总指令不得超过 {Q} 次。
- 提交结论后，质检流程立即终止。
- 如果检验结果吻合（V 等于 H），质检任务圆满完成；否则将引发严重良品率危机，质检失败。
- 如果超过 {Q} 次指令仍未输出结论，系统默认判定批次失效。

当前质检参数：
- 抽检批次总数 N = {N}
- 关键评估批次 k = {k}
- 单批次瑕疵上限 B = {B}
- 最大检测指令数 Q = {Q}

每次仅可下达一项指令。请使用以下 XML 格式：

- 公差阈值检测（例如查明 H 是否大于等于 10）：
<query_threshold>10</query_threshold>

- 提交批次检验结论（例如断定 H 等于 15）：
<answer>15</answer>

请用最少的操作找出真实的瑕疵数据。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
The Quality Control Module of the automated precision parts production line is conducting a routine audit.

The inspection system has sampled {N} production batches from the assembly line and now needs to evaluate the {k} most critical batches that recently rolled off. The maximum number of minor defects allowed per batch is {B}.
Your task is to deduce the cumulative total of defects H across these {k} core batches, which determines whether to trigger a halt for maintenance. Naturally, H ranges from 0 to {k}·{B}.

To maintain the production cadence, you are permitted a maximum of {Q} diagnostic commands:

1. Tolerance Threshold Check: Enter a tolerance threshold T, and the module will indicate whether the cumulative defect total H is greater than or equal to T.
2. Batch Inspection Conclusion: Upon confirming the exact value of H, submit an integer V as the final quality inspection result.

Notes:
- Both threshold checks and the conclusion submission consume your command quota of {Q} operations.
- The inspection workflow stops the moment you submit your conclusion.
- If the result matches reality (V equals H), the quality audit is a success; otherwise, it sparks a severe yield rate crisis, resulting in failure.
- Failing to output a conclusion within {Q} commands causes the system to automatically flag the batches as invalid.

Current inspection parameters:
- Total sampled batches N = {N}
- Critical evaluation batches k = {k}
- Single batch defect cap B = {B}
- Maximum diagnostic commands Q = {Q}

Issue only one command per turn. Use the following XML format:

- Tolerance Threshold Check (e.g., asking if H is greater than or equal to 10):
<query_threshold>10</query_threshold>

- Submit Batch Inspection Conclusion (e.g., asserting H equals 15):
<answer>15</answer>

Use as few operations as possible to pinpoint the true defect count.
"""

    contextualized_rule_zh_5 = """\
知识产权商业维权系统正在清算一起侵权案件的损害赔偿金。

系统追踪到侵权方的 {N} 个非法活动周期，并锁定了近期最恶劣的 {k} 个核心侵权周期。单周期内查实的非法获利指数上限为 {B}。
你的任务是推演这 {k} 个核心周期内的累计非法获利总指数 H，以此作为判定惩罚性赔偿金的法理基数。显然，H 的取值在 0 到 {k}·{B} 之间。

为了符合法定取证程序的时限要求，你最多只有 {Q} 次质证操作权限：

1. 立案标准质证：提出一个指数阈值 T，维权系统将核对累计侵权指数 H 是否大于等于 T。
2. 损害赔偿核算定论：当你掌握了 H 的确切数值时，提交整数 V 作为最终的法定索赔定论。

注意：
- 每次质证和最终定论提交都计入取证次数，总次数不得逾越 {Q} 次。
- 一旦提交定论，法庭取证环节即告结案。
- 若核算完全一致（V 等于 H），原告胜诉并获得足额赔偿；否则证据链断裂，维权败诉。
- 取证达到 {Q} 次却无法给出定论，法庭将驳回诉讼请求。

当前案件参数：
- 追踪周期总数 N = {N}
- 核心侵权周期 k = {k}
- 单周期获利指数上限 B = {B}
- 法定质证权限 Q = {Q}

每次质证环节仅限进行一种操作。请使用以下 XML 格式：

- 立案标准质证（例如查实 H 是否大于等于 10）：
<query_threshold>10</query_threshold>

- 提交损害赔偿核算定论（例如断言 H 等于 15）：
<answer>15</answer>

请步步为营，以最小的司法资源消耗完成索赔核算。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
The Intellectual Property Commercial Protection System is liquidating damages for an infringement case.

The system has tracked the infringing party's illicit activities over {N} periods, zeroing in on the {k} most egregious recent core infringement cycles. The verified illegal profit index ceiling for a single cycle is {B}.
Your task is to deduce the cumulative illegal profit index H for these {k} core cycles, which will serve as the legal baseline for punitive damages. Obviously, H falls between 0 and {k}·{B}.

To comply with the statutory time limits for evidence collection, you have a maximum of {Q} cross-examination privileges:

1. Filing Standard Cross-Examination: Propose an index threshold T, and the protection system will verify if the cumulative infringement index H is greater than or equal to T.
2. Final Damages Assessment: Once you possess the exact figure for H, submit an integer V as the definitive legal claim conclusion.

Notes:
- Every cross-examination query and the final assessment submission draws from your quota of {Q} total operations.
- The evidentiary phase closes immediately upon submitting the final assessment.
- If the calculation is perfectly accurate (V equals H), the plaintiff wins full compensation; otherwise, the chain of evidence breaks, and the lawsuit is lost.
- Exhausting all {Q} privileges without a definitive conclusion results in the court dismissing the claim.

Current case parameters:
- Total tracked periods N = {N}
- Core infringement cycles k = {k}
- Single-cycle profit index cap B = {B}
- Legal cross-examination privileges Q = {Q}

Perform only one action per evidentiary round. Use the following XML format:

- Filing Standard Cross-Examination (e.g., verifying if H is greater than or equal to 10):
<query_threshold>10</query_threshold>

- Submit Final Damages Assessment (e.g., asserting H equals 15):
<answer>15</answer>

Tread carefully and complete the damages calculation with minimal expenditure of judicial resources.
"""

    tags = ["answer", "query_threshold"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "N": 5,
                "k": 2,
                "B": 3,
                "Q": 5,
                "sequence": [1, 2, 0, 3, 2],
            },
            2: {
                "N": 8,
                "k": 3,
                "B": 5,
                "Q": 7,
                "sequence": [2, 4, 1, 3, 0, 5, 4, 2],
            },
            3: {
                "N": 10,
                "k": 4,
                "B": 7,
                "Q": 8,
                "sequence": [3, 1, 6, 2, 5, 4, 7, 3, 6, 5],
            },
            4: {
                "N": 12,
                "k": 5,
                "B": 10,
                "Q": 9,
                "sequence": [5, 8, 2, 9, 1, 6, 3, 10, 7, 4, 9, 8],
            },
            5: {
                "N": 15,
                "k": 6,
                "B": 15,
                "Q": 10,
                "sequence": [7, 12, 3, 8, 14, 5, 11, 2, 9, 13, 6, 15, 10, 8, 12],
            },
        },
        "en": {
            1: {
                "N": 5,
                "k": 2,
                "B": 3,
                "Q": 5,
                "sequence": [1, 2, 0, 3, 2],
            },
            2: {
                "N": 8,
                "k": 3,
                "B": 5,
                "Q": 7,
                "sequence": [2, 4, 1, 3, 0, 5, 4, 2],
            },
            3: {
                "N": 10,
                "k": 4,
                "B": 7,
                "Q": 8,
                "sequence": [3, 1, 6, 2, 5, 4, 7, 3, 6, 5],
            },
            4: {
                "N": 12,
                "k": 5,
                "B": 10,
                "Q": 9,
                "sequence": [5, 8, 2, 9, 1, 6, 3, 10, 7, 4, 9, 8],
            },
            5: {
                "N": 15,
                "k": 6,
                "B": 15,
                "Q": 10,
                "sequence": [7, 12, 3, 8, 14, 5, 11, 2, 9, 13, 6, 15, 10, 8, 12],
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self._game_info["N"] = cfg["N"]
        self._game_info["k"] = cfg["k"]
        self._game_info["B"] = cfg["B"]
        self._game_info["Q"] = cfg["Q"]
        
        self.sequence = cfg["sequence"]
        
        self.target_H = sum(self.sequence[-cfg["k"]:])
        
        self.N = cfg["N"]
        self.k = cfg["k"]
        self.B = cfg["B"]
        self.Q = cfg["Q"]

    def evaluate(self, parsed_info):
        self.query_count += 1

        if self.query_count > self.Q:
            return False

        try:
            answer_str = parsed_info["answer"].strip()
            submitted_value = int(answer_str)
            
            return submitted_value == self.target_H
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        self.query_count += 1
        
        if self.query_count > self.Q:
            if self.config.language == "zh":
                msg = "操作次数超限，游戏失败。"
            else:
                msg = "Exceeded maximum operations, game failed."
            self.state.set_state("failed", "exceeded maximum operations")
            return msg
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_msg = "错误：无效的阈值格式。"
        else:
            yes_res, no_res = "Yes", "No"
            error_msg = "Error: Invalid threshold format."

        if "query_threshold" in parsed_info:
            try:
                threshold = int(parsed_info["query_threshold"].strip())
                return yes_res if self.target_H >= threshold else no_res
            except:
                return error_msg
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            elif correct == "否":
                return "是"
        else:
            lower_correct = correct.lower()
            if lower_correct == "yes":
                return "No" if correct[0].isupper() else "no"
            elif lower_correct == "no":
                return "Yes" if correct[0].isupper() else "yes"

        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        max_possible_sum = self.k * self.B
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        for t in range(0, max_possible_sum + 2):
            ans = yes_res if self.target_H >= t else no_res
            results.append({
                "query": f"<query_threshold>{t}</query_threshold>",
                "answer": ans
            })
            
        return results