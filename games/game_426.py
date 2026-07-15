from .base import Game
import random
import re

class SequenceMappingGame(Game):

    game_rule_zh = """\
我们来玩一个"序列映射推理"游戏，规则如下：

游戏设定了一个长度为 {n} 的序列 S，序列中每个位置的元素都来自字母表 {alphabet_str}。同时指定了一个目标符号 {target_symbol}。

在游戏开始前，我已经秘密地对序列的下标进行了重映射。重映射方式只有以下四种之一：
- A（恒等映射）：标号 i 对应原序列的第 i 位
- B（反转映射）：标号 i 对应原序列的第 (N+1-i) 位
- C（循环左移 1 位）：标号 i 对应原序列的第 (i+1) 位，其中标号 N 对应第 1 位
- D（循环右移 1 位）：标号 i 对应原序列的第 (i-1) 位，其中标号 1 对应第 N 位

你的目标是通过查询推断出：
1. 真实采用的映射方案（A、B、C 或 D）
2. 目标符号 {target_symbol} 在原始序列中的所有出现位置（升序排列）

你可以通过以下两种方式进行查询：

1. 观测查询：询问标号 i 位置的符号是什么，系统会返回该位置的符号
2. 判定查询：询问标号 i 位置的符号是否等于目标符号 {target_symbol}，系统会回答"是"或"否"

当你收集到足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次只能提出一个查询。请使用以下 XML 格式：

- 观测查询（例如查询标号 3）：
<query_observe>3</query_observe>

- 判定查询（例如判定标号 5）：
<query_judge>5</query_judge>

提交最终答案时，必须说明映射方案（A、B、C 或 D）并列出目标符号在原始序列中的所有位置（用逗号隔开，严格升序），格式如下：

<answer>mapping=A, positions=1,3,5</answer>

注意：请尽可能用较少的查询次数完成推理。
"""

    game_rule_en = """\
Let's play a "Sequence Mapping Inference" game. Here are the rules:

A sequence S of length {n} has been set up, where each element comes from the alphabet {alphabet_str}. A target symbol {target_symbol} has also been specified.

Before the game starts, I have secretly remapped the indices of the sequence. There are only four possible remapping schemes:
- A (Identity): Index i corresponds to position i in the original sequence
- B (Reversal): Index i corresponds to position (N+1-i) in the original sequence
- C (Cyclic Left Shift by 1): Index i corresponds to position (i+1), where index N corresponds to position 1
- D (Cyclic Right Shift by 1): Index i corresponds to position (i-1), where index 1 corresponds to position N

Your goal is to infer through queries:
1. The actual mapping scheme used (A, B, C, or D)
2. All positions where the target symbol {target_symbol} appears in the original sequence (in ascending order)

You can make queries in two ways:

1. Observation Query: Ask what symbol is at index i, and the system will return the symbol at that position
2. Judgment Query: Ask whether the symbol at index i equals the target symbol {target_symbol}, and the system will answer "Yes" or "No"

When you have gathered enough information, submit your final answer. If the answer is incorrect or the format is invalid, the game fails.

You can only make one query at a time. Use the following XML format:

- Observation Query (e.g., querying index 3):
<query_observe>3</query_observe>

- Judgment Query (e.g., judging index 5):
<query_judge>5</query_judge>

When submitting the final answer, specify the mapping scheme (A, B, C, or D) and list all positions of the target symbol in the original sequence (comma-separated, strictly ascending order), using this format:

<answer>mapping=A, positions=1,3,5</answer>

Note: Try to complete the inference with as few queries as possible.
"""

    contextualized_rule_zh_1 = """\
您好，交通调度中心。目前城市核心干线的路网监控系统出现异常，请协助排查。

我们有一条包含 {n} 个关键路口的干线，其真实的路况状态构成序列 S，每个路口的交通状态标识均来自以下代码：{alphabet_str}。目前指挥部需要特别关注状态为 {target_symbol}（重度拥堵）的路口以进行疏导。

由于光纤接口维护时发生故障，传感器前端的端口标号与实际路口的物理对应关系发生了重置。经运维工程师评估，接线错位只可能是以下四种情况之一：
- A（正常直连）：端口 i 直接读取干线上第 i 个路口的状态
- B（线路反接）：端口 i 错误读取了第 (N+1-i) 个路口的状态
- C（总线错位前移）：端口 i 读取了第 (i+1) 个路口，且末端端口 N 串线到了第 1 个路口
- D（总线错位后移）：端口 i 读取了第 (i-1) 个路口，且首端端口 1 串线到了第 N 个路口

你的任务是通过系统诊断指令完成推理：
1. 查明当前传感器网络的物理接线映射方案（A、B、C 或 D）
2. 找出所有真实状态为 {target_symbol} 的路口物理编号（严格按升序排列）

你可以执行两种诊断查询：
1. 观测查询：读取端口 i 当前反馈的状态代码
2. 判定查询：校验端口 i 是否反馈了目标状态 {target_symbol}（系统会返回"是"或"否"）

每次只能发送一个诊断指令。请使用以下 XML 格式：

- 观测查询（例如查询端口 3）：
<query_observe>3</query_observe>

- 判定查询（例如判定端口 5）：
<query_judge>5</query_judge>

提交最终诊断报告时，必须说明接线方案并列出目标路口的物理编号（用逗号隔开，严格升序），格式如下：

<answer>mapping=A, positions=1,3,5</answer>

注意：请尽可能用较少的通信次数完成诊断。
"""

    contextualized_rule_en_1 = """\
[Traffic Control Scenario]
Hello, Traffic Dispatch Center. The road network monitoring system for the city's main arterial road is malfunctioning. Please assist in troubleshooting.

We have a key arterial sequence S consisting of {n} intersections. The traffic status code of each intersection is from the set {alphabet_str}. The command center currently needs to focus on intersections with status {target_symbol} (Severe Congestion) for immediate traffic diversion.

Following a fiber-optic maintenance failure, the port indices on the sensor frontend have lost their correct physical mapping to the intersections. Engineers assess that the miswiring must be one of four specific scenarios:
- A (Normal Connection): Port i reads the status of the i-th physical intersection
- B (Reversed Wiring): Port i reads the status of the (N+1-i)-th intersection
- C (Bus Forward Shift): Port i reads the (i+1)-th intersection, with port N wired to the 1st intersection
- D (Bus Backward Shift): Port i reads the (i-1)-th intersection, with port 1 wired to the N-th intersection

Your objective is to deduce the following via system diagnostic commands:
1. Identify the current physical wiring scheme (A, B, C, or D)
2. Locate the true physical indices of all intersections exhibiting the {target_symbol} status (in strict ascending order)

You can issue two types of diagnostic queries:
1. Observation Query: Retrieve the exact status code returned by port i
2. Judgment Query: Check if port i reports the target status {target_symbol} (system answers "Yes" or "No")

Submit only one diagnostic command at a time. Use the following XML format:

- Observation Query (e.g., query port 3):
<query_observe>3</query_observe>

- Judgment Query (e.g., judge port 5):
<query_judge>5</query_judge>

When submitting your final diagnostic report, state the mapping scheme and list the true physical indices of the target intersections (comma-separated, strictly ascending order), like this:

<answer>mapping=A, positions=1,3,5</answer>

Note: Please complete the troubleshooting with the minimum necessary communication attempts.
"""

    contextualized_rule_zh_2 = """\
欢迎使用全自动高通量基因检测流水线管控系统。当前批次检测遇到对齐异常，需人工介入。

当前流水线载入了一个长度为 {n} 的样本槽位序列 S，每个样本经过初步筛查被标记为 {alphabet_str} 中的一种分型。临床医生急需确认携带特定病灶标记 {target_symbol} 的所有真实样本来源。

由于进样器传送带刚刚经历过一次紧急复位，检测通道标号与物理托盘上样本的真实排列可能不再对齐。根据设备操作手册，偏移状态仅有以下四种情况：
- A（标准对齐）：通道 i 精准检测托盘上的第 i 个样本
- B（托盘反向放置）：通道 i 检测了托盘上第 (N+1-i) 个样本
- C（左旋偏移一格）：通道 i 检测了第 (i+1) 个样本，且末端通道 N 绕回检测第 1 个样本
- D（右旋偏移一格）：通道 i 检测了第 (i-1) 个样本，且首端通道 1 绕回检测第 N 个样本

你需要通过控制台探针推断出：
1. 传送带当前的真实偏移方案（A、B、C 或 D）
2. 目标病灶 {target_symbol} 所在的托盘原始物理位置（严格按升序排列）

你可以通过以下两种探针指令进行检视：
1. 观测查询：启动通道 i 的光谱分析，获取该通道的病灶分型
2. 判定查询：使用通道 i 的靶向试剂，确认其是否为目标病灶 {target_symbol}（返回"是"或"否"）

每次只能下达一个探针指令。请使用以下 XML 格式：

- 观测查询（例如探伤通道 3）：
<query_observe>3</query_observe>

- 判定查询（例如靶向判定通道 5）：
<query_judge>5</query_judge>

提交最终病理报告时，必须标明设备的偏移方案并列出目标病灶的真实托盘位置（用逗号隔开，严格升序），格式如下：

<answer>mapping=A, positions=1,3,5</answer>

注意：试剂成本高昂，请以最少的检测次数完成诊断。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Fully Automated High-Throughput Genomic Testing Pipeline Control System. The current batch has encountered an alignment anomaly requiring manual intervention.

The pipeline is processing a sequence S of {n} sample slots. Each sample is classified into one of the genotypes in {alphabet_str}. Clinicians urgently need to identify the exact origin of all samples carrying the specific pathogenic marker {target_symbol}.

Due to a recent emergency reset of the auto-sampler conveyor, the sensing channel indices may no longer align with the true physical arrangement of samples on the tray. According to the equipment manual, the misalignment can only be one of the following four conditions:
- A (Standard Alignment): Channel i accurately scans the i-th sample on the tray
- B (Reversed Tray): Channel i scans the (N+1-i)-th sample
- C (Left Shift by One): Channel i scans the (i+1)-th sample, with channel N looping to scan the 1st sample
- D (Right Shift by One): Channel i scans the (i-1)-th sample, with channel 1 looping to scan the N-th sample

Your objective is to infer the following via console probes:
1. The actual conveyor offset scheme (A, B, C, or D)
2. The original physical positions on the tray containing the target marker {target_symbol} (strictly ascending)

You can inspect the batch using two types of probe commands:
1. Observation Query: Activate spectral analysis on channel i to retrieve the genotype
2. Judgment Query: Apply targeted reagents on channel i to check for the marker {target_symbol} (returns "Yes" or "No")

Issue only one probe command per step. Use the following XML format:

- Observation Query (e.g., probe channel 3):
<query_observe>3</query_observe>

- Judgment Query (e.g., targeted judgment on channel 5):
<query_judge>5</query_judge>

When submitting the final pathology report, specify the offset scheme and list the true tray positions of the target markers (comma-separated, strictly ascending order):

<answer>mapping=A, positions=1,3,5</answer>

Note: Reagents are costly. Please deduce the answers with the minimum possible tests.
"""

    contextualized_rule_zh_3 = """\
欢迎登录省级考试阅卷中心调度系统。

目前有一批包含 {n} 份试卷的考场封袋序列 S 正在进行扫描流转。系统中每份试卷的当前评卷状态代码记录为 {alphabet_str} 中的一种。督导组急需定位状态代码为 {target_symbol}（需专家复核）的所有试卷的真实考场座号。

因为扫描仪进纸口发生过临时卡纸重置，系统入库的“电子卷宗号”与试卷原本的“物理座号”对应关系被打乱。阅卷组排查后确认，乱序情况只属于以下四种之一：
- A（原序录入）：电子卷宗号 i 对应真实座号 i
- B（倒序录入）：整袋试卷放反，卷宗号 i 对应真实座号 (N+1-i)
- C（首份卷置尾）：卡纸导致第 1 份卷子最后扫入，卷宗号 i 对应座号 (i+1)，卷宗号 N 对应座号 1
- D（末份卷置首）：卡纸导致最后 1 份卷子最先扫入，卷宗号 i 对应座号 (i-1)，卷宗号 1 对应座号 N

你需要通过抽查校验推断出：
1. 扫描入库时发生的实际乱序规则（A、B、C 或 D）
2. 需要复核的目标试卷 {target_symbol} 在考场中的真实座号（严格按升序排列）

你可以通过以下两种指令进行系统查卷：
1. 观测查询：调阅电子卷宗号 i 的评卷状态代码
2. 判定查询：比对电子卷宗号 i 是否属于目标复核状态 {target_symbol}（系统回答"是"或"否"）

每次只能发起一次查卷请求。请使用以下 XML 格式：

- 观测查询（例如调阅卷宗 3）：
<query_observe>3</query_observe>

- 判定查询（例如比对卷宗 5）：
<query_judge>5</query_judge>

提交最终督导报告时，必须写明乱序规则并列出目标试卷的真实座号（用逗号隔开，严格升序），格式如下：

<answer>mapping=A, positions=1,3,5</answer>

注意：为了减少系统负载，请尽可能减少查卷次数。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Provincial Examination Grading Center Dispatch System.

A batch consisting of {n} examination papers from a sealed classroom sequence S is currently being scanned and routed. The grading status code of each paper is recorded in the system as one of {alphabet_str}. The supervisory team urgently needs to locate the true desk numbers of all papers with status {target_symbol} (Requires Expert Review).

Due to a temporary paper jam at the scanner feeder, the mapping between the system's "Electronic Document Index" and the "Physical Desk Number" of the papers has been scrambled. Technicians confirmed that the misordering follows exactly one of these four patterns:
- A (Sequential Entry): Document Index i corresponds to true Desk i
- B (Reversed Entry): The entire stack was flipped; Index i corresponds to true Desk (N+1-i)
- C (First Paper Last): The first paper was scanned last; Index i corresponds to Desk (i+1), and Index N corresponds to Desk 1
- D (Last Paper First): The last paper was scanned first; Index i corresponds to Desk (i-1), and Index 1 corresponds to Desk N

Your objective is to deduce the following through spot checks:
1. The actual scrambling pattern occurred during scanning (A, B, C, or D)
2. The true physical desk numbers of all target papers {target_symbol} requiring review (strictly ascending)

You can audit the system using two types of queries:
1. Observation Query: Retrieve the grading status code of Electronic Document Index i
2. Judgment Query: Check whether Electronic Document Index i has the target status {target_symbol} (answers "Yes" or "No")

Submit only one audit request at a time. Use the following XML format:

- Observation Query (e.g., retrieve Document 3):
<query_observe>3</query_observe>

- Judgment Query (e.g., check Document 5):
<query_judge>5</query_judge>

When submitting the final supervisory report, declare the scrambling pattern and list the true desk numbers of the target papers (comma-separated, strictly ascending order):

<answer>mapping=A, positions=1,3,5</answer>

Note: Please minimize the number of queries to reduce system overhead.
"""

    contextualized_rule_zh_4 = """\
欢迎接入高精度工业质检中心总控平台。

目前质检流水线上正运行着长度为 {n} 的零部件批次 S。探针组传回的每个零部件表面特征码属于 {alphabet_str} 之一。品控主管要求立刻截获含有 {target_symbol}（致命结构缺陷）的所有零部件。

然而，机械臂固件升级导致探针逻辑通道与生产线物理工位的相位匹配丢失。系统日志表明，当前的相位偏差必然是以下四种情况之一：
- A（精准校准）：逻辑通道 i 读数对应物理工位 i 上的零部件
- B（通道镜像反转）：逻辑通道 i 对应倒数排列，即物理工位 (N+1-i)
- C（相位超前一格）：逻辑通道 i 读取了物理工位 (i+1)，且通道 N 读取工位 1
- D（相位滞后一格）：逻辑通道 i 读取了物理工位 (i-1)，且通道 1 读取工位 N

你需要通过发送测试指令，推断出：
1. 探针当前的真实相位偏差情况（A、B、C 或 D）
2. 含有致命缺陷 {target_symbol} 的真实物理工位编号（严格按升序排列）

你可以执行两种测试指令：
1. 观测查询：获取逻辑通道 i 返回的表面特征码
2. 判定查询：触发逻辑通道 i 的警报模块，确认其是否检测到缺陷 {target_symbol}（返回"是"或"否"）

每次只能发送一条指令。请使用以下 XML 格式：

- 观测查询（例如读取通道 3）：
<query_observe>3</query_observe>

- 判定查询（例如触发通道 5 警报）：
<query_judge>5</query_judge>

提交截获指令时，必须包含相位偏差代码并列出目标缺陷的真实物理工位（用逗号隔开，严格升序），格式如下：

<answer>mapping=A, positions=1,3,5</answer>

注意：请利用最少的指令周期完成排查，以免流水线停机时间过长。
"""

    contextualized_rule_en_4 = """\
[Manufacturing / Industrial Scenario]
Welcome to the High-Precision Quality Inspection Assembly Line Control Platform.

A component batch sequence S of length {n} is currently running on the inspection line. The surface feature code for each component reported by the probes belongs to {alphabet_str}. The Quality Control Supervisor demands the immediate interception of all components showing {target_symbol} (Fatal Structural Defect).

However, a firmware update of the robotic arms has caused the logical channels of the probes to lose phase synchronization with the physical stations on the assembly line. System logs indicate the phase deviation must be one of these four configurations:
- A (Precise Calibration): Logical channel i reads the component at physical station i
- B (Mirrored Channels): Logical channel i reads in reverse, scanning physical station (N+1-i)
- C (Phase Lead by One): Logical channel i reads physical station (i+1), with channel N wrapping to station 1
- D (Phase Lag by One): Logical channel i reads physical station (i-1), with channel 1 wrapping to station N

You must deduce the following via test commands:
1. The actual phase deviation configuration of the probes (A, B, C, or D)
2. The exact physical station numbers containing the fatal defect {target_symbol} (strictly ascending)

You can execute two types of test commands:
1. Observation Query: Retrieve the surface feature code from logical channel i
2. Judgment Query: Trigger the alarm module on logical channel i to verify if it detects defect {target_symbol} (returns "Yes" or "No")

Send only one command per cycle. Use the following XML format:

- Observation Query (e.g., read channel 3):
<query_observe>3</query_observe>

- Judgment Query (e.g., trigger alarm on channel 5):
<query_judge>5</query_judge>

When submitting the interception order, include the phase deviation code and list the true physical stations of the defects (comma-separated, strictly ascending order):

<answer>mapping=A, positions=1,3,5</answer>

Note: Please resolve this using the minimum number of command cycles to avoid prolonged downtime on the assembly line.
"""

    contextualized_rule_zh_5 = """\
系统提示：您已登入 e-Discovery 电子证据验证与审计网络。

当前案件包含一系列长度为 {n} 的物证清单 S，每份物证经过AI审查被打上了安全级别与内容标签，取值范围为 {alphabet_str}。法庭现急需调取标签为 {target_symbol}（具有决定性证明效力）的所有原始物证以进行庭审质证。

由于昨夜遭到恶意骇客入侵，当前数字档案系统中的“检索索引”与物证库中“真实存档编号”之间的映射关系被秘密篡改。安全取证小组分析指出，骇客所使用的篡改手法仅有以下四种：
- A（未被篡改）：检索索引 i 依然对应真实存档编号 i
- B（时间戳反转）：检索索引 i 被倒置为真实编号 (N+1-i)
- C（索引整体前移）：检索索引 i 指向了真实编号 (i+1)，且末尾索引 N 被重定向到了编号 1
- D（索引整体后移）：检索索引 i 指向了真实编号 (i-1)，且首位索引 1 被重定向到了编号 N

作为审计员，你必须通过接口查证：
1. 骇客实际采用的系统篡改手法（A、B、C 或 D）
2. 决定性物证 {target_symbol} 在物证库中的真实存档编号（严格按升序排列）

系统允许你调用两种取证接口：
1. 观测查询：读取检索索引 i 下当前指向的物证内容标签
2. 判定查询：验证检索索引 i 指向的物证是否带有 {target_symbol} 标签（系统返回"是"或"否"）

每次请求仅限调用一个接口。请使用以下 XML 格式：

- 观测查询（例如查询索引 3）：
<query_observe>3</query_observe>

- 判定查询（例如验证索引 5）：
<query_judge>5</query_judge>

提交最终审计恢复结果时，必须定性篡改手法并列出目标物证的真实存档编号（用逗号隔开，严格升序），格式如下：

<answer>mapping=A, positions=1,3,5</answer>

注意：取证调用会产生不可逆的系统追踪日志，请用最少的查询次数完成证据还原。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
System Prompt: You have logged into the e-Discovery Evidence Verification and Auditing Network.

The current case involves a material evidence inventory sequence S of length {n}. Each piece of evidence has been AI-reviewed and assigned a security and content tag from the set {alphabet_str}. The court urgently requires the extraction of all original physical evidence tagged with {target_symbol} (Decisive Probative Value) for cross-examination.

Due to a malicious cyber intrusion last night, the mapping between the digital system's "Search Index" and the "True Archive Number" in the evidence vault was covertly tampered with. The digital forensics team concludes that the hackers employed one of only four specific tampering methods:
- A (Untampered): Search Index i continues to point to True Archive i
- B (Timestamp Reversal): Search Index i has been inverted to point to True Archive (N+1-i)
- C (Index Forward Shift): Search Index i points to True Archive (i+1), with Index N redirected to Archive 1
- D (Index Backward Shift): Search Index i points to True Archive (i-1), with Index 1 redirected to Archive N

As an auditor, you must verify via API calls:
1. The exact tampering method used by the hackers (A, B, C, or D)
2. The true archive numbers of the decisive evidence {target_symbol} in the physical vault (strictly ascending)

The system allows you to invoke two forensic endpoints:
1. Observation Query: Read the content tag of the evidence currently pointed to by Search Index i
2. Judgment Query: Verify if the evidence at Search Index i carries the tag {target_symbol} (system returns "Yes" or "No")

You may call only one endpoint per request. Use the following XML format:

- Observation Query (e.g., query Index 3):
<query_observe>3</query_observe>

- Judgment Query (e.g., verify Index 5):
<query_judge>5</query_judge>

When submitting your final audit recovery report, qualify the tampering method and list the true archive numbers of the target evidence (comma-separated, strictly ascending order):

<answer>mapping=A, positions=1,3,5</answer>

Note: Forensic calls generate irreversible tracking logs. Please reconstruct the evidence sequence with the minimum possible queries.
"""

    tags = ["answer", "query_observe", "query_judge"]
    
    reasoning_type = "溯因推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "alphabet": ["X", "Y", "Z"],
                "sequence": ["X", "Y", "X", "Z", "Y"],
                "target": "X",
                "mapping": "A",
            },
            2: {
                "n": 6,
                "alphabet": ["W", "X", "Y", "Z"],
                "sequence": ["W", "X", "Y", "Z", "W", "X"],
                "target": "X",
                "mapping": "B",
            },
            3: {
                "n": 7,
                "alphabet": ["V", "W", "X", "Y", "Z"],
                "sequence": ["V", "W", "X", "Y", "Z", "V", "W"],
                "target": "V",
                "mapping": "C",
            },
            4: {
                "n": 8,
                "alphabet": ["U", "V", "W", "X", "Y", "Z"],
                "sequence": ["U", "V", "W", "X", "Y", "Z", "U", "V"],
                "target": "V",
                "mapping": "D",
            },
            5: {
                "n": 10,
                "alphabet": ["P", "Q", "R", "S", "T", "U", "V"],
                "sequence": ["P", "Q", "R", "S", "T", "U", "V", "P", "Q", "R"],
                "target": "R",
                "mapping": "C",
            },
        },
        "en": {
            1: {
                "n": 5,
                "alphabet": ["X", "Y", "Z"],
                "sequence": ["X", "Y", "X", "Z", "Y"],
                "target": "X",
                "mapping": "A",
            },
            2: {
                "n": 6,
                "alphabet": ["W", "X", "Y", "Z"],
                "sequence": ["W", "X", "Y", "Z", "W", "X"],
                "target": "X",
                "mapping": "B",
            },
            3: {
                "n": 7,
                "alphabet": ["V", "W", "X", "Y", "Z"],
                "sequence": ["V", "W", "X", "Y", "Z", "V", "W"],
                "target": "V",
                "mapping": "C",
            },
            4: {
                "n": 8,
                "alphabet": ["U", "V", "W", "X", "Y", "Z"],
                "sequence": ["U", "V", "W", "X", "Y", "Z", "U", "V"],
                "target": "V",
                "mapping": "D",
            },
            5: {
                "n": 10,
                "alphabet": ["P", "Q", "R", "S", "T", "U", "V"],
                "sequence": ["P", "Q", "R", "S", "T", "U", "V", "P", "Q", "R"],
                "target": "R",
                "mapping": "C",
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
        self.n = cfg["n"]
        self.alphabet = cfg["alphabet"]
        self.sequence = cfg["sequence"]
        self.target = cfg["target"]
        self.mapping_type = cfg["mapping"]
        
        self._game_info["alphabet_str"] = "{" + ", ".join(self.alphabet) + "}"
        self._game_info["target_symbol"] = self.target
        
        self._build_mapping()
        
        self.true_positions = []
        for i in range(1, self.n + 1):
            if self.sequence[i - 1] == self.target:
                self.true_positions.append(i)

    def _build_mapping(self):
        self.index_map = {}
        
        if self.mapping_type == "A":
            for i in range(1, self.n + 1):
                self.index_map[i] = i
                
        elif self.mapping_type == "B":
            for i in range(1, self.n + 1):
                self.index_map[i] = self.n + 1 - i
                
        elif self.mapping_type == "C":
            for i in range(1, self.n + 1):
                if i == self.n:
                    self.index_map[i] = 1
                else:
                    self.index_map[i] = i + 1
                    
        elif self.mapping_type == "D":
            for i in range(1, self.n + 1):
                if i == 1:
                    self.index_map[i] = self.n
                else:
                    self.index_map[i] = i - 1

    def _get_symbol_at_index(self, index):
        if index < 1 or index > self.n:
            return None
        original_pos = self.index_map[index]
        return self.sequence[original_pos - 1]

    def evaluate(self, parsed_info):
        try:
            raw_ans = parsed_info["answer"].strip()
            
            mapping_match = re.search(r'mapping\s*=\s*([A-Da-d])', raw_ans)
            positions_match = re.search(r'positions\s*=\s*([\d,\s]+)', raw_ans)

            if not mapping_match or not positions_match:
                return False

            mapping_part = mapping_match.group(1).strip().upper()
            positions_str = positions_match.group(1).strip()

            if mapping_part != self.mapping_type:
                return False

            try:
                model_positions = [int(x.strip()) for x in positions_str.split(",") if x.strip()]
                if model_positions != sorted(model_positions):
                    return False
                return model_positions == self.true_positions
            except:
                return False
                
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_range = "错误：标号超出范围。"
            error_format = "错误：格式无效。"
        else:
            yes_res, no_res = "Yes", "No"
            error_range = "Error: Index out of range."
            error_format = "Error: Invalid format."

        if "query_observe" in parsed_info:
            try:
                index = int(parsed_info["query_observe"].strip())
                if index < 1 or index > self.n:
                    return error_range
                symbol = self._get_symbol_at_index(index)
                return symbol
            except:
                return error_format

        elif "query_judge" in parsed_info:
            try:
                index = int(parsed_info["query_judge"].strip())
                if index < 1 or index > self.n:
                    return error_range
                symbol = self._get_symbol_at_index(index)
                return yes_res if symbol == self.target else no_res
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        if correct == yes_res:
            return no_res
        if correct == no_res:
            return yes_res

        if correct in self.alphabet:
            candidates = [s for s in self.alphabet if s != correct]
            if candidates:
                return random.choice(candidates)

        return self.alphabet[0] if correct != self.alphabet[0] else self.alphabet[-1]

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        for i in range(1, self.n + 1):
            symbol = self._get_symbol_at_index(i)
            query_obs = f"<query_observe>{i}</query_observe>"
            results.append({
                "query": query_obs,
                "answer": symbol
            })

            query_judge = f"<query_judge>{i}</query_judge>"
            ans_judge = yes_res if symbol == self.target else no_res
            results.append({
                "query": query_judge,
                "answer": ans_judge
            })
            
        return results