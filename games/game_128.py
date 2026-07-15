from .base import Game
import re

class SequenceLockGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "序列"

    game_rule_zh = """\
我们现在来玩一个"序列解锁"的推理游戏，规则如下：

游戏设定了一个长度为 {n} 的有序符号序列（索引从 1 到 {n}），每个位置的值取自字母集合 {{A, B, C}}。我已经秘密选择了一个目标集合 S，它只可能是以下四个之一：
- {{A}}
- {{B}}
- {{C}}
- {{A, C}}

你的目标是通过查询推断出目标集合 S，并回答两个关键问题：
1. 整段序列中满足条件的元素总数
2. 满足累计计数等于常量 T={t} 的最小索引位置

你可以使用以下三种查询方式（每次只能提出一个查询）：

1. 区间计数查询：查询指定区间 [L, R] 内满足条件的元素个数。注意区间长度不能超过 {max_interval_length}。
2. 集合猜测：猜测目标集合 S 是什么。你只能进行 1 次猜测，猜错则游戏失败。
3. 最终答案：在猜对集合后，给出总数和关键索引。

请注意：
- 区间计数查询次数有限制，请尽可能少地使用
- 必须先正确猜出集合 S，才能提交最终答案
- 最终答案必须一次性给出两个值，任一错误都将失败

每次只能使用一个标签：

- 区间计数查询（例如查询区间 [3, 8]）：
<query_scan>3,8</query_scan>

- 集合猜测（例如猜测集合为 {{A}}）：
<query_guess>A</query_guess>

或猜测集合为 {{A, C}}：
<query_guess>A,C</query_guess>

- 最终答案（例如总数为 10，关键索引为 7）：
<answer>total=10, t=7</answer>

若关键索引不存在，则：
<answer>total=10, t=不存在</answer>
"""

    game_rule_en = """\
Let's play a "Sequence Lock" deduction game. Here are the rules:

There is an ordered symbol sequence of length {n} (indexed from 1 to {n}), where each position contains a letter from the set {{A, B, C}}. I have secretly chosen a target set S, which can only be one of the following four:
- {{A}}
- {{B}}
- {{C}}
- {{A, C}}

Your goal is to infer the target set S through queries, and answer two key questions:
1. The total count of elements in the entire sequence that satisfy the condition
2. The smallest index position where the cumulative count equals the constant T={t}

You can use the following three types of queries (one query per turn):

1. Interval Count Query: Query the count of qualifying elements in a specified interval [L, R]. Note that the interval length cannot exceed {max_interval_length}.
2. Set Guess: Guess what the target set S is. You can only make 1 guess; if wrong, the game fails.
3. Final Answer: After guessing the set correctly, provide the total count and key index.

Please note:
- The number of interval count queries is limited, use them as sparingly as possible
- You must correctly guess set S before submitting the final answer
- The final answer must provide both values at once; any error will result in failure

Only one tag can be used at a time:

- Interval Count Query (e.g., querying interval [3, 8]):
<query_scan>3,8</query_scan>

- Set Guess (e.g., guessing set {{A}}):
<query_guess>A</query_guess>

Or guessing set {{A, C}}:
<query_guess>A,C</query_guess>

- Final Answer (e.g., total is 10, key index is 7):
<answer>total=10, t=7</answer>

If the key index does not exist:
<answer>total=10, t=not_exist</answer>
"""

    contextualized_rule_zh_1 = """\
[交通监控溯源系统]
我们现在进行一项"违规车辆排查"的交通执法任务，规则如下：

系统记录了一段长度为 {n} 的车辆通行序列（流水号从 1 到 {n}），每辆车属于以下三种类型之一：{{A(小轿车), B(大货车), C(客车)}}。交管部门已秘密锁定了一个重点排查的违规车辆集合 S，它只可能是以下四种组合之一：
- {{A}}
- {{B}}
- {{C}}
- {{A, C}}

你的目标是通过调取监控记录推断出重点排查的车辆集合 S，并提交两项关键事实：
1. 整段通行序列中，属于排查集合的违规车辆总数
2. 当累计发现的违规车辆数刚好等于预警阈值 T={t} 时，对应的最小流水号

你可以使用以下三种系统指令（每次只能执行一个）：

1. 区间抓拍查询：查询指定流水号区间 [L, R] 内出现的违规车辆数量。注意单次查询跨度不能超过 {max_interval_length}。
2. 目标车型锁定：锁定重点排查的车辆集合 S 是什么。你只有 1 次提交结论的机会，锁定错误将导致排查任务失败。
3. 提交最终报告：在正确锁定集合后，汇报违规车辆总数和触发预警的关键流水号。

请注意：
- 区间抓拍查询次数有限制，请尽可能节约系统算力
- 必须先正确锁定集合 S，才能提交最终报告
- 最终报告必须一次性包含两个数值，任何一项错误都将被驳回

每次只能使用一个标签：

- 区间抓拍查询（例如查询流水号 [3, 8]）：
<query_scan>3,8</query_scan>

- 目标车型锁定（例如锁定重点排查的是 {{A}}）：
<query_guess>A</query_guess>

或锁定重点排查的是 {{A, C}}：
<query_guess>A,C</query_guess>

- 最终报告（例如总数为 10，触发预警的流水号为 7）：
<answer>total=10, t=7</answer>

若触发预警的流水号不存在，则：
<answer>total=10, t=不存在</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Monitoring Trace System]
We are now conducting a "Violating Vehicle Trace" traffic enforcement task. The rules are as follows:

The system has recorded a sequence of {n} passing vehicles (indexed from 1 to {n}), where each vehicle belongs to one of three types: {{A (Car), B (Truck), C (Bus)}}. The traffic management department has secretly targeted a specific set of violating vehicles S, which can only be one of the following four combinations:
- {{A}}
- {{B}}
- {{C}}
- {{A, C}}

Your goal is to deduce the target set S by querying the surveillance records, and submit two key facts:
1. The total number of violating vehicles belonging to the target set in the entire sequence.
2. The exact sequence index when the cumulative count of detected violating vehicles reaches the early-warning threshold T={t}.

You can use the following three system commands (one command per turn):

1. Interval Capture Query: Query the number of violating vehicles within a specified sequence interval [L, R]. Note that the interval span cannot exceed {max_interval_length}.
2. Target Type Lock: Identify the targeted vehicle set S. You only have 1 chance to submit your conclusion; guessing incorrectly will result in task failure.
3. Final Report Submission: After correctly identifying the target set, report the total count and the critical index that triggered the warning.

Please note:
- The number of interval queries is limited, so conserve system processing power.
- You must correctly identify set S before submitting the final report.
- The final report must provide both values simultaneously; any error will cause a rejection.

Only one tag can be used at a time:

- Interval Capture Query (e.g., querying sequence [3, 8]):
<query_scan>3,8</query_scan>

- Target Type Lock (e.g., guessing target is {{A}}):
<query_guess>A</query_guess>

Or guessing target is {{A, C}}:
<query_guess>A,C</query_guess>

- Final Report Submission (e.g., total is 10, warning triggered at index 7):
<answer>total=10, t=7</answer>

If the critical index does not exist:
<answer>total=10, t=not_exist</answer>
"""

    contextualized_rule_zh_2 = """\
[流行病原学溯源系统]
我们现在进行一项"感染病例溯源"的医疗排查任务，规则如下：

防疫系统记录了一段长度为 {n} 的门诊接诊序列（接诊编号从 1 到 {n}），每位患者呈现出一种主要临床症状，取自集合 {{A(发热), B(咳嗽), C(皮疹)}}。疾控中心已秘密锁定了一个与未知病原体相关的核心症状集合 S，它只可能是以下四种之一：
- {{A}}
- {{B}}
- {{C}}
- {{A, C}}

你的目标是通过调取病历推断出核心症状集合 S，并回答两个关键问题：
1. 整段接诊序列中，表现出核心症状的感染者总数
2. 当累计确诊的感染者达到应急响应阈值 T={t} 时，对应的最小接诊编号

你可以使用以下三种排查手段（每次只能提出一个指令）：

1. 区间病历调阅：查询指定接诊编号区间 [L, R] 内符合核心症状的患者人数。注意调阅区间跨度不能超过 {max_interval_length}。
2. 症状集合诊断：诊断核心症状集合 S 是什么。你只能进行 1 次诊断提交，误诊则导致溯源失败。
3. 最终流调报告：在正确确诊核心症状后，汇报感染总数和触发响应的关键接诊编号。

请注意：
- 区间病历调阅次数有限制，请尽可能减少医疗数据库负载
- 必须先正确诊断出症状集合 S，才能提交最终流调报告
- 最终报告必须一次性给出两个数值，任一错误都将导致失败

每次只能使用一个标签：

- 区间病历调阅（例如调阅编号 [3, 8]）：
<query_scan>3,8</query_scan>

- 症状集合诊断（例如诊断症状为 {{A}}）：
<query_guess>A</query_guess>

或诊断症状为 {{A, C}}：
<query_guess>A,C</query_guess>

- 最终流调报告（例如总数为 10，关键接诊编号为 7）：
<answer>total=10, t=7</answer>

若关键接诊编号不存在，则：
<answer>total=10, t=不存在</answer>
"""

    contextualized_rule_en_2 = """\
[Epidemiological Tracing System]
We are now conducting an "Infectious Case Trace" medical investigation task. The rules are as follows:

The epidemic prevention system has recorded a sequence of {n} outpatient admissions (indexed from 1 to {n}), where each patient exhibits one primary clinical symptom from the set {{A (Fever), B (Cough), C (Rash)}}. The CDC has secretly identified a core symptom set S associated with an unknown pathogen, which can only be one of the following four:
- {{A}}
- {{B}}
- {{C}}
- {{A, C}}

Your goal is to deduce the core symptom set S by querying medical records, and answer two key questions:
1. The total number of infected patients exhibiting the core symptoms in the entire admission sequence.
2. The exact admission index when the cumulative count of confirmed cases reaches the emergency response threshold T={t}.

You can use the following three investigation methods (one command per turn):

1. Interval Record Review: Query the number of patients with core symptoms within a specified admission interval [L, R]. Note that the interval length cannot exceed {max_interval_length}.
2. Symptom Set Diagnosis: Diagnose the core symptom set S. You can only make 1 diagnosis submission; a misdiagnosis will result in tracing failure.
3. Final Epidemiological Report: After correctly diagnosing the core symptoms, report the total infected count and the critical admission index that triggered the response.

Please note:
- The number of interval record reviews is limited, please minimize the load on the medical database.
- You must correctly diagnose the symptom set S before submitting the final epidemiological report.
- The final report must provide both values at once; any error will result in failure.

Only one tag can be used at a time:

- Interval Record Review (e.g., querying records [3, 8]):
<query_scan>3,8</query_scan>

- Symptom Set Diagnosis (e.g., diagnosing symptom as {{A}}):
<query_guess>A</query_guess>

Or diagnosing symptom as {{A, C}}:
<query_guess>A,C</query_guess>

- Final Epidemiological Report (e.g., total is 10, critical admission index is 7):
<answer>total=10, t=7</answer>

If the critical admission index does not exist:
<answer>total=10, t=not_exist</answer>
"""

    contextualized_rule_zh_3 = """\
[智能教务审核系统]
我们现在进行一项"异常试卷抽检"的教务管理任务，规则如下：

系统接收到了一段长度为 {n} 的在线提交答卷序列（提交序号从 1 到 {n}），每份答卷属于以下三个学科之一：{{A(数学), B(物理), C(化学)}}。教务处已经秘密设定了一个存在学术不端嫌疑的重点审核学科集合 S，它只可能是以下四个之一：
- {{A}}
- {{B}}
- {{C}}
- {{A, C}}

你的目标是通过抽检指令推断出重点审核集合 S，并回答两个关键问题：
1. 整段提交序列中，属于重点审核学科的答卷总数
2. 当累计拦截的嫌疑答卷数量等于人工复核阈值 T={t} 时，对应的最小提交序号

你可以使用以下三种审核指令（每次只能下达一个）：

1. 区间批量检索：检索指定序号区间 [L, R] 内属于审核集合的答卷份数。注意检索区间长度不能超过 {max_interval_length}。
2. 学科集合指认：指认重点审核的学科集合 S 是什么。你只能进行 1 次指认，指认错误则任务失败。
3. 最终审核结论：在正确指认学科后，提交审核总数和触发人工复核的关键序号。

请注意：
- 区间批量检索次数有限制，请尽可能高效使用
- 必须先正确指认出学科集合 S，才能提交最终审核结论
- 最终结论必须一次性给出两个数值，任一数据核对错误都将被驳回

每次只能使用一个标签：

- 区间批量检索（例如检索序号 [3, 8]）：
<query_scan>3,8</query_scan>

- 学科集合指认（例如指认学科为 {{A}}）：
<query_guess>A</query_guess>

或指认学科为 {{A, C}}：
<query_guess>A,C</query_guess>

- 最终审核结论（例如总数为 10，关键序号为 7）：
<answer>total=10, t=7</answer>

若关键序号不存在，则：
<answer>total=10, t=不存在</answer>
"""

    contextualized_rule_en_3 = """\
[Intelligent Academic Audit System]
We are now conducting an "Anomalous Exam Paper Sampling" academic administration task. The rules are as follows:

The system has received a sequence of {n} online exam submissions (indexed from 1 to {n}), where each submission belongs to one of three subjects: {{A (Math), B (Physics), C (Chemistry)}}. The academic affairs office has secretly targeted a specific set of subjects S suspected of academic misconduct, which can only be one of the following four:
- {{A}}
- {{B}}
- {{C}}
- {{A, C}}

Your goal is to infer the target audit set S through sampling commands, and answer two key questions:
1. The total number of submissions belonging to the audited subjects in the entire sequence.
2. The exact submission index when the cumulative count of intercepted suspicious papers reaches the manual review threshold T={t}.

You can use the following three audit commands (one command per turn):

1. Interval Batch Retrieval: Retrieve the number of audited submissions within a specified index interval [L, R]. Note that the interval length cannot exceed {max_interval_length}.
2. Subject Set Identification: Identify what the target audit set S is. You can only make 1 identification; identifying incorrectly will result in task failure.
3. Final Audit Conclusion: After correctly identifying the subjects, submit the total audited count and the critical index that triggered manual review.

Please note:
- The number of interval batch retrievals is limited, please use them as efficiently as possible.
- You must correctly identify the subject set S before submitting the final audit conclusion.
- The final conclusion must provide both values at once; any data verification error will result in rejection.

Only one tag can be used at a time:

- Interval Batch Retrieval (e.g., retrieving indices [3, 8]):
<query_scan>3,8</query_scan>

- Subject Set Identification (e.g., identifying subject as {{A}}):
<query_guess>A</query_guess>

Or identifying subject as {{A, C}}:
<query_guess>A,C</query_guess>

- Final Audit Conclusion (e.g., total is 10, critical index is 7):
<answer>total=10, t=7</answer>

If the critical index does not exist:
<answer>total=10, t=not_exist</answer>
"""

    contextualized_rule_zh_4 = """\
[工业流水线质检系统]
我们现在进行一项"缺陷零件排查"的工业生产任务，规则如下：

流水线上有一段长度为 {n} 的零件传送序列（工位批次从 1 到 {n}），每个位置上的零件属于以下三种类型之一：{{A(齿轮), B(活塞), C(阀门)}}。自动化质检探头已经秘密锁定了一个存在加工缺陷的零件集合 S，它只可能是以下四个之一：
- {{A}}
- {{B}}
- {{C}}
- {{A, C}}

你的目标是通过传感器数据推断出缺陷零件集合 S，并回答两个关键问题：
1. 整段流水线序列中，属于该缺陷集合的零件总数
2. 当累计检测出的缺陷零件达到停机整顿阈值 T={t} 时，对应的最小批次位置

你可以使用以下三种设备指令（每次只能发送一个指令）：

1. 区间探伤扫描：查询指定批次区间 [L, R] 内出现的缺陷零件数量。注意扫描跨度不能超过 {max_interval_length}。
2. 缺陷类型判定：判定存在缺陷的零件集合 S 是什么。你只有 1 次判定机会，误判将导致生产线严重事故。
3. 最终质检报告：在正确判定缺陷类型后，提交缺陷总数和触发停机的关键批次位置。

请注意：
- 区间探伤扫描次数有限制，请尽可能节省设备检测耗时
- 必须先正确判定缺陷集合 S，才能提交最终质检报告
- 最终报告必须一次性输入两个参数，任一参数录入错误都将导致排查失败

每次只能使用一个标签：

- 区间探伤扫描（例如扫描批次 [3, 8]）：
<query_scan>3,8</query_scan>

- 缺陷类型判定（例如判定缺陷为 {{A}}）：
<query_guess>A</query_guess>

或判定缺陷为 {{A, C}}：
<query_guess>A,C</query_guess>

- 最终质检报告（例如总数为 10，关键批次为 7）：
<answer>total=10, t=7</answer>

若关键批次不存在，则：
<answer>total=10, t=不存在</answer>
"""

    contextualized_rule_en_4 = """\
[Industrial Assembly Line QC System]
We are now conducting a "Defective Parts Troubleshooting" industrial production task. The rules are as follows:

There is a parts conveyor sequence of length {n} on the assembly line (batch indexed from 1 to {n}), where each position contains a part from one of three types: {{A (Gears), B (Pistons), C (Valves)}}. The automated quality control probe has secretly locked onto a set of defective parts S, which can only be one of the following four:
- {{A}}
- {{B}}
- {{C}}
- {{A, C}}

Your goal is to infer the defective parts set S using sensor data, and answer two key questions:
1. The total number of defective parts belonging to this set in the entire assembly line sequence.
2. The exact batch index when the cumulative count of detected defective parts reaches the machine-halt threshold T={t}.

You can use the following three equipment commands (one command per turn):

1. Interval Flaw Scan: Query the number of defective parts within a specified batch interval [L, R]. Note that the scanning span cannot exceed {max_interval_length}.
2. Defect Type Determination: Determine what the defective parts set S is. You only have 1 chance; a misjudgment will lead to a severe production line incident.
3. Final QC Report: After correctly determining the defect type, submit the total defective count and the critical batch index that triggered the halt.

Please note:
- The number of interval flaw scans is limited, so save equipment testing time.
- You must correctly determine the defect set S before submitting the final QC report.
- The final report must input both parameters at once; any entry error will cause the troubleshooting to fail.

Only one tag can be used at a time:

- Interval Flaw Scan (e.g., scanning batches [3, 8]):
<query_scan>3,8</query_scan>

- Defect Type Determination (e.g., determining defect as {{A}}):
<query_guess>A</query_guess>

Or determining defect as {{A, C}}:
<query_guess>A,C</query_guess>

- Final QC Report (e.g., total is 10, critical batch is 7):
<answer>total=10, t=7</answer>

If the critical batch does not exist:
<answer>total=10, t=not_exist</answer>
"""

    contextualized_rule_zh_5 = """\
[司法证据链分析系统]
我们现在进行一项"保密卷宗审查"的法律辅助任务，规则如下：

法庭取证系统录入了一段长度为 {n} 的证据提交序列（证据编号从 1 到 {n}），每份证据属于以下三种材料之一：{{A(财务记录), B(往来邮件), C(商业合同)}}。主审法官已秘密划定了一个涉及商业机密的保密材料集合 S，它只可能是以下四个之一：
- {{A}}
- {{B}}
- {{C}}
- {{A, C}}

你的目标是通过合规调卷指令推断出保密材料集合 S，并确认两个关键事实：
1. 整个证据序列中，属于保密材料的证据总数
2. 当累计审查到的保密材料达到申请封存阈值 T={t} 时，对应的最小证据编号

你可以使用以下三种法定质证指令（每次只能提交一个）：

1. 区间卷宗阅览：申请查阅指定编号区间 [L, R] 内包含的保密证据份数。注意单次阅卷跨度不能超过 {max_interval_length}。
2. 保密范围举证：举证主张保密材料的集合 S 是什么。你只有 1 次举证机会，举证失败将导致无法申请不公开审理。
3. 最终审查备忘录：在正确界定保密范围后，提交保密证据总数和触发封存申请的关键编号。

请注意：
- 区间卷宗阅览次数受法定程序限制，请谨慎行使查阅权
- 必须先正确举证保密集合 S，才能提交最终审查备忘录
- 最终备忘录必须一次性陈述两个事实，任一事实陈述错误都将面临法庭驳回

每次只能使用一个标签：

- 区间卷宗阅览（例如阅览编号 [3, 8]）：
<query_scan>3,8</query_scan>

- 保密范围举证（例如举证保密材料为 {{A}}）：
<query_guess>A</query_guess>

或举证保密材料为 {{A, C}}：
<query_guess>A,C</query_guess>

- 最终审查备忘录（例如总数为 10，关键编号为 7）：
<answer>total=10, t=7</answer>

若关键编号不存在，则：
<answer>total=10, t=不存在</answer>
"""

    contextualized_rule_en_5 = """\
[Judicial Evidence Chain Analysis System]
We are now conducting a "Confidential Dossier Review" legal assistance task. The rules are as follows:

The court's evidence collection system has recorded an evidence submission sequence of length {n} (exhibit indexed from 1 to {n}), where each exhibit belongs to one of three material types: {{A (Financial Records), B (Emails), C (Contracts)}}. The presiding judge has secretly designated a confidential material set S involving trade secrets, which can only be one of the following four:
- {{A}}
- {{B}}
- {{C}}
- {{A, C}}

Your goal is to infer the confidential material set S through compliant dossier requisition commands, and establish two key facts:
1. The total number of confidential exhibits in the entire evidence sequence.
2. The exact exhibit index when the cumulative count of reviewed confidential materials reaches the sealing-motion threshold T={t}.

You can use the following three statutory evidentiary commands (one command per turn):

1. Interval Dossier Review: Apply to review the number of confidential exhibits within a specified index interval [L, R]. Note that the review span cannot exceed {max_interval_length} per request.
2. Confidentiality Scope Burden of Proof: Assert what the confidential material set S is. You only have 1 chance to present this proof; failure will result in the inability to motion for a closed hearing.
3. Final Review Memorandum: After correctly defining the confidentiality scope, submit the total confidential count and the critical index that triggered the sealing motion.

Please note:
- The number of interval dossier reviews is limited by statutory procedures, exercise your review rights prudently.
- You must correctly assert the confidential set S before submitting the final review memorandum.
- The final memorandum must state both facts at once; any factual error will face a court dismissal.

Only one tag can be used at a time:

- Interval Dossier Review (e.g., reviewing exhibits [3, 8]):
<query_scan>3,8</query_scan>

- Confidentiality Scope Burden of Proof (e.g., asserting confidential material is {{A}}):
<query_guess>A</query_guess>

Or asserting confidential material is {{A, C}}:
<query_guess>A,C</query_guess>

- Final Review Memorandum (e.g., total is 10, critical index is 7):
<answer>total=10, t=7</answer>

If the critical index does not exist:
<answer>total=10, t=not_exist</answer>
"""

    tags = ["answer", "query_scan", "query_guess"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 25,
                "sequence": "ABCAACBBACCABABBCABCABCACB",
                "target_set": ["A"],
                "t": 5,
                "max_queries": 8,
                "max_interval_length": 6,
            },
            2: {
                "n": 25,
                "sequence": "ABCAACBBACCABABBCABCABCACB",
                "target_set": ["B"],
                "t": 5,
                "max_queries": 8,
                "max_interval_length": 6,
            },
            3: {
                "n": 25,
                "sequence": "ABCAACBBACCABABBCABCABCACB",
                "target_set": ["C"],
                "t": 5,
                "max_queries": 8,
                "max_interval_length": 6,
            },
            4: {
                "n": 25,
                "sequence": "ABCAACBBACCABABBCABCABCACB",
                "target_set": ["A", "C"],
                "t": 5,
                "max_queries": 8,
                "max_interval_length": 6,
            },
            5: {
                "n": 30,
                "sequence": "ABCAACBBACCABABBCABCABCACBACBA",
                "target_set": ["A", "C"],
                "t": 6,
                "max_queries": 10,
                "max_interval_length": 5,
            },
        },
        "en": {
            1: {
                "n": 25,
                "sequence": "ABCAACBBACCABABBCABCABCACB",
                "target_set": ["A"],
                "t": 5,
                "max_queries": 8,
                "max_interval_length": 6,
            },
            2: {
                "n": 25,
                "sequence": "ABCAACBBACCABABBCABCABCACB",
                "target_set": ["B"],
                "t": 5,
                "max_queries": 8,
                "max_interval_length": 6,
            },
            3: {
                "n": 25,
                "sequence": "ABCAACBBACCABABBCABCABCACB",
                "target_set": ["C"],
                "t": 5,
                "max_queries": 8,
                "max_interval_length": 6,
            },
            4: {
                "n": 25,
                "sequence": "ABCAACBBACCABABBCABCABCACB",
                "target_set": ["A", "C"],
                "t": 5,
                "max_queries": 8,
                "max_interval_length": 6,
            },
            5: {
                "n": 30,
                "sequence": "ABCAACBBACCABABBCABCABCACBACBA",
                "target_set": ["A", "C"],
                "t": 6,
                "max_queries": 10,
                "max_interval_length": 5,
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0
        self.has_guessed = False
        self.guess_correct = False
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
        self._game_info["t"] = cfg["t"]
        self._game_info["max_interval_length"] = cfg["max_interval_length"]
        
        self.sequence = cfg["sequence"][:cfg["n"]]
        self.target_set = set(cfg["target_set"])
        self.T = cfg["t"]
        self.max_queries = cfg["max_queries"]
        self.max_interval_length = cfg["max_interval_length"]
        
        self._compute_answers()

    def _compute_answers(self):
        self.correct_total = sum(
            1 for i in range(len(self.sequence))
            if self.sequence[i] in self.target_set
        )
        
        cumulative_count = 0
        self.correct_t = None
        for i in range(len(self.sequence)):
            if self.sequence[i] in self.target_set:
                cumulative_count += 1
            if cumulative_count == self.T:
                self.correct_t = i + 1
                break

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        n = self._game_info["n"]
        max_len = self.max_interval_length

        for L in range(1, n + 1):
            for R in range(L, n + 1):
                if (R - L + 1) > max_len:
                    continue
                
                count = 0
                for i in range(L - 1, R):
                    if self.sequence[i] in self.target_set:
                        count += 1
                
                queries.append({
                    "query": f"<query_scan>{L},{R}</query_scan>",
                    "answer": str(count)
                })
        
        correct_guess = ",".join(sorted(list(self.target_set)))
        if self.config.language == "zh":
            ans_msg = "正确！您已成功猜出目标集合，现在请提交最终答案。"
        else:
            ans_msg = "Correct! You have successfully guessed the target set. Now please submit your final answer."
            
        queries.append({
            "query": f"<query_guess>{correct_guess}</query_guess>",
            "answer": ans_msg
        })
        
        return queries

    def evaluate(self, parsed_info):
        if not self.guess_correct:
            return False
        
        raw_ans = parsed_info["answer"]
        
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        for kv in kv_pairs:
            if "=" in kv:
                k, v = kv.split("=", 1)
                ans_dict[k.strip()] = v.strip()
        
        if "total" not in ans_dict or "t" not in ans_dict:
            return False
        
        try:
            model_total = int(ans_dict["total"])
        except:
            return False
        
        if model_total != self.correct_total:
            return False
        
        t_value = ans_dict["t"]
        if self.correct_t is None:
            if self.config.language == "zh":
                return t_value in ["不存在", "无", "None", "不存在索引"]
            else:
                return t_value.lower() in ["not_exist", "none", "no", "not exist"]
        else:
            try:
                model_t = int(t_value)
                return model_t == self.correct_t
            except:
                return False

    def _cf_core_produce(self, parsed_info):
        return self._core_produce_response(parsed_info)

    def _cf_make_wrong(self, correct):
        try:
            val = int(correct)
            return str(val + 1)
        except (ValueError, TypeError):
            if self.config.language == "zh":
                return "错误的反馈信息（反事实干预）"
            else:
                return "Incorrect feedback (counterfactual intervention)"

    def _core_produce_response(self, parsed_info):
        
        if "query_scan" in parsed_info:
            if self.has_guessed:
                if self.config.language == "zh":
                    return "错误：已经进行过集合猜测，不能再进行查询。"
                else:
                    return "Error: You have already made a set guess and cannot query anymore."
            
            if self.query_count >= self.max_queries:
                if self.config.language == "zh":
                    return f"错误：已达到最大查询次数限制（{self.max_queries}次）。"
                else:
                    return f"Error: Maximum query limit ({self.max_queries}) reached."
            
            try:
                raw = parsed_info["query_scan"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                L, R = int(parts[0]), int(parts[1])
            except:
                if self.config.language == "zh":
                    return "错误：区间格式无效，请使用格式 L,R（例如：3,8）。"
                else:
                    return "Error: Invalid interval format. Use format L,R (e.g., 3,8)."
            
            if L < 1 or R > self._game_info["n"] or L > R:
                if self.config.language == "zh":
                    return f"错误：区间超出范围。索引必须在 1 到 {self._game_info['n']} 之间，且 L 不能大于 R。"
                else:
                    return f"Error: Interval out of range. Indices must be between 1 and {self._game_info['n']}, and L must not exceed R."
            
            interval_length = R - L + 1
            if interval_length > self.max_interval_length:
                if self.config.language == "zh":
                    return f"错误：区间长度超过限制。最大区间长度为 {self.max_interval_length}。"
                else:
                    return f"Error: Interval length exceeds limit. Maximum interval length is {self.max_interval_length}."
            
            count = 0
            for i in range(L - 1, R):
                if self.sequence[i] in self.target_set:
                    count += 1
            
            self.query_count += 1
            return str(count)
        
        elif "query_guess" in parsed_info:
            if self.has_guessed:
                if self.config.language == "zh":
                    return "错误：只能进行一次集合猜测，您已经使用过了。"
                else:
                    return "Error: You can only make one set guess, and you have already used it."
            
            self.has_guessed = True
            
            try:
                raw = parsed_info["query_guess"]
                guessed_set = set(x.strip().upper() for x in raw.split(",") if x.strip())
            except:
                if self.config.language == "zh":
                    return "错误：集合格式无效。"
                else:
                    return "Error: Invalid set format."
            
            if guessed_set == self.target_set:
                self.guess_correct = True
                if self.config.language == "zh":
                    return "正确！您已成功猜出目标集合，现在请提交最终答案。"
                else:
                    return "Correct! You have successfully guessed the target set. Now please submit your final answer."
            else:
                self.guess_correct = False
                self.state.set_state("failed", "incorrect set guess")
                if self.config.language == "zh":
                    return "错误：集合猜测不正确，游戏失败。"
                else:
                    return "Error: Incorrect set guess. Game failed."
        
        else:
            if self.config.language == "zh":
                return "错误：未找到有效的查询标签。"
            else:
                return "Error: No valid query tag found."