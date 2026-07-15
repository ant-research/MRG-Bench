from .base import Game
import re

class SubstringMatchingGame(Game):

    game_rule_zh = """\
我们现在来玩一个"隐藏序列匹配"的推理游戏，规则如下：

游戏设定：
- 存在一个字母表Σ（包含所有大写英文字母A到Z）。
- 有一个长度为 {n} 的隐藏序列 S，其中每个位置的字符都来自字母表Σ。序列索引从1开始，即 S[1] 到 S[{n}]。
- 有一个长度为 {m} 的公开模式串 P = "{pattern}"。

你的目标：
判断是否存在某个起点位置 j（1 小于等于 j 小于等于 {max_start}），使得模式串 P 作为连续子串完整出现在隐藏序列 S 中，即 S[j] 到 S[j+{m}-1] 与 P[1] 到 P[{m}] 完全相同。

可用的查询类型（每次只能发起一个查询）：

1. 对齐查询 Align(i)：
   - 询问从位置 i 开始，隐藏序列 S 与模式串 P 的最长前缀匹配长度。
   - 返回一个整数 L(i)，表示最大的 t（0 小于等于 t 小于等于 min({m}, {n} - i + 1)），使得 S[i] 到 S[i+t-1] 与 P[1] 到 P[t] 完全匹配。
   - 格式：<query_align>i</query_align>
   - 例如：<query_align>5</query_align>

2. 区间存在性查询 Sweep(l, r, k)：
   - 询问在起点范围 [l, r]（1 小于等于 l 小于等于 r 小于等于 {max_start}）内，是否存在某个位置 j 使得 Align(j) 大于等于 k。
   - 注意：k 必须严格小于 {m}，不能直接询问是否存在完整匹配。
   - 返回"是"或"否"。
   - 格式：<query_sweep>l,r,k</query_sweep>
   - 例如：<query_sweep>1,10,3</query_sweep>

提交答案：
当你收集到足够信息后，请提交最终判定结果：

- 若判定存在匹配，必须给出一个具体的起点位置 j，格式如下：
  <answer>存在,j={{j}}</answer>
  
- 若判定不存在匹配，格式如下：
  <answer>不存在</answer>

重要提示：
- 若判定"存在"，你必须确保该起点 j 的 Align(j) 等于 {m}（通过 Align 查询确认）。
- 若判定"不存在"，你需要通过查询证明所有可能的起点位置都不满足完整匹配。
- 请尽可能少地使用查询次数来完成判定。
- 答案错误或格式不符将导致游戏失败。
"""

    game_rule_en = """\
Let's play a "Hidden Sequence Matching" deduction game. Here are the rules:

Game Setup:
- There is an alphabet Σ (containing all uppercase English letters A to Z).
- There is a hidden sequence S of length {n}, where each position contains a character from alphabet Σ. The sequence is indexed starting from 1, i.e., S[1] to S[{n}].
- There is a public pattern string P = "{pattern}" of length {m}.

Your Goal:
Determine whether there exists a starting position j (1 less than or equal to j less than or equal to {max_start}) such that pattern P appears as a complete consecutive substring in hidden sequence S, i.e., S[j] to S[j+{m}-1] exactly matches P[1] to P[{m}].

Available Query Types (only one query per turn):

1. Align Query Align(i):
   - Ask for the longest prefix match length between hidden sequence S starting at position i and pattern P.
   - Returns an integer L(i), the maximum t (0 less than or equal to t less than or equal to min({m}, {n} - i + 1)) such that S[i] to S[i+t-1] exactly matches P[1] to P[t].
   - Format: <query_align>i</query_align>
   - Example: <query_align>5</query_align>

2. Interval Existence Query Sweep(l, r, k):
   - Ask whether there exists a position j in the range [l, r] (1 less than or equal to l less than or equal to r less than or equal to {max_start}) such that Align(j) is greater than or equal to k.
   - Note: k must be strictly less than {m}; you cannot directly ask if a complete match exists.
   - Returns "Yes" or "No".
   - Format: <query_sweep>l,r,k</query_sweep>
   - Example: <query_sweep>1,10,3</query_sweep>

Submitting Answer:
When you have gathered enough information, submit your final determination:

- If you determine a match exists, you must provide a specific starting position j in this format:
  <answer>exists,j={{j}}</answer>
  
- If you determine no match exists, use this format:
  <answer>not_exists</answer>

Important Notes:
- If you determine "exists", you must ensure that Align(j) equals {m} for the position j (confirmed via Align query).
- If you determine "not exists", you need to prove through queries that all possible starting positions do not satisfy a complete match.
- Please use as few queries as possible to complete the determination.
- Incorrect answers or invalid formats will result in game failure.
"""

    contextualized_rule_zh_1 = """\
欢迎使用智能交通调度分析系统。我们需要在庞大的车流记录中追踪一支特定的目标车队。

系统设定：
- 存在一个车辆特征编码字母表Σ（包含所有大写英文字母A到Z）。
- 存在一条长度为 {n} 的隐藏车流记录序列 S，其中每个位置的字符代表一辆经过卡口的车辆特征。序列索引从1开始，即 S[1] 到 S[{n}]。
- 我们正在追踪一支长度为 {m} 的公开目标车队特征序列 P = "{pattern}"。

你的目标：
判断是否存在某个起始卡口记录位置 j（1 小于等于 j 小于等于 {max_start}），使得目标车队 P 作为连续的车流完整出现在隐藏记录序列 S 中，即 S[j] 到 S[j+{m}-1] 与 P[1] 到 P[{m}] 完全相同。

可用的调查手段（每次只能发起一个查询）：

1. 连续追踪查询 Align(i)：
   - 询问从记录位置 i 开始，实际车流序列 S 与目标车队 P 的最长连续匹配车辆数。
   - 返回一个整数 L(i)，表示最大的 t（0 小于等于 t 小于等于 min({m}, {n} - i + 1)），使得 S[i] 到 S[i+t-1] 与 P[1] 到 P[t] 完全匹配。
   - 格式：<query_align>i</query_align>
   - 例如：<query_align>5</query_align>

2. 区间扫描查询 Sweep(l, r, k)：
   - 询问在起始记录范围 [l, r]（1 小于等于 l 小于等于 r 小于等于 {max_start}）内，是否存在某个位置 j 使得连续追踪查询 Align(j) 大于等于 k。
   - 注意：k 必须严格小于 {m}，不能直接询问是否存在完整的车队匹配。
   - 返回"是"或"否"。
   - 格式：<query_sweep>l,r,k</query_sweep>
   - 例如：<query_sweep>1,10,3</query_sweep>

提交结案报告：
当你收集到足够信息后，请提交最终判定结果：

- 若判定目标车队出现过，必须给出一个具体的起始位置 j，格式如下：
  <answer>存在,j={{j}}</answer>
  
- 若判定目标车队未出现，格式如下：
  <answer>不存在</answer>

重要提示：
- 若判定"存在"，你必须确保该起始位置 j 的 Align(j) 等于 {m}（通过连续追踪查询确认）。
- 若判定"不存在"，你需要通过调查证明所有可能的起始位置都不满足完整匹配。
- 请尽可能少地使用查询次数来完成判定。
- 答案错误或格式不符将导致追踪任务失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Intelligent Traffic Dispatch and Analysis System. We need to track a specific target convoy in a massive stream of vehicle records.

System Setup:
- There is a vehicle feature coding alphabet Σ (containing all uppercase English letters A to Z).
- There is a hidden traffic record sequence S of length {n}, where each position represents a vehicle's feature passing a checkpoint. The sequence is indexed starting from 1, i.e., S[1] to S[{n}].
- We are tracking a public target convoy signature sequence P = "{pattern}" of length {m}.

Your Goal:
Determine whether there exists a starting checkpoint record position j (1 less than or equal to j less than or equal to {max_start}) such that the target convoy P appears as a complete consecutive stream in the hidden traffic sequence S, i.e., S[j] to S[j+{m}-1] exactly matches P[1] to P[{m}].

Available Investigative Tools (only one query per turn):

1. Continuous Tracking Query Align(i):
   - Ask for the longest consecutive matching vehicle count between the hidden traffic sequence S starting at record position i and the target convoy P.
   - Returns an integer L(i), the maximum t (0 less than or equal to t less than or equal to min({m}, {n} - i + 1)) such that S[i] to S[i+t-1] exactly matches P[1] to P[t].
   - Format: <query_align>i</query_align>
   - Example: <query_align>5</query_align>

2. Interval Scan Query Sweep(l, r, k):
   - Ask whether there exists a position j in the starting record range [l, r] (1 less than or equal to l less than or equal to r less than or equal to {max_start}) such that the Continuous Tracking Query Align(j) is greater than or equal to k.
   - Note: k must be strictly less than {m}; you cannot directly ask if a complete convoy match exists.
   - Returns "Yes" or "No".
   - Format: <query_sweep>l,r,k</query_sweep>
   - Example: <query_sweep>1,10,3</query_sweep>

Submitting Final Report:
When you have gathered enough information, submit your final determination:

- If you determine the target convoy appeared, you must provide a specific starting position j in this format:
  <answer>exists,j={{j}}</answer>
  
- If you determine the convoy did not appear, use this format:
  <answer>not_exists</answer>

Important Notes:
- If you determine "exists", you must ensure that Align(j) equals {m} for the position j (confirmed via Continuous Tracking query).
- If you determine "not exists", you need to prove through investigations that all possible starting positions do not satisfy a complete match.
- Please use as few queries as possible to complete the determination.
- Incorrect answers or invalid formats will result in tracking failure.
"""

    contextualized_rule_zh_2 = """\
欢迎使用基因序列筛查系统。我们将从患者的长序列基因图谱中定位特定的致病基因片段。

系统设定：
- 存在一个基因特征字母表Σ（包含所有大写英文字母A到Z）。
- 存在一条长度为 {n} 的隐藏患者基因序列 S，其中每个位置的字符代表一个特征碱基。序列索引从1开始，即 S[1] 到 S[{n}]。
- 我们正在寻找一段已知长度为 {m} 的公开致病基因片段 P = "{pattern}"。

你的目标：
判断是否存在某个起始位点 j（1 小于等于 j 小于等于 {max_start}），使得致病基因片段 P 作为连续序列完整出现在隐藏患者序列 S 中，即 S[j] 到 S[j+{m}-1] 与 P[1] 到 P[{m}] 完全相同。

可用的筛查手段（每次只能发起一个查询）：

1. 基因表达匹配查询 Align(i)：
   - 询问从位点 i 开始，隐藏基因序列 S 与致病片段 P 的最长连续前缀匹配长度。
   - 返回一个整数 L(i)，表示最大的 t（0 小于等于 t 小于等于 min({m}, {n} - i + 1)），使得 S[i] 到 S[i+t-1] 与 P[1] 到 P[t] 完全匹配。
   - 格式：<query_align>i</query_align>
   - 例如：<query_align>5</query_align>

2. 区间筛查查询 Sweep(l, r, k)：
   - 询问在起始位点范围 [l, r]（1 小于等于 l 小于等于 r 小于等于 {max_start}）内，是否存在某个位点 j 使得基因表达匹配查询 Align(j) 大于等于 k。
   - 注意：k 必须严格小于 {m}，不能直接询问是否存在完整的基因突变匹配。
   - 返回"是"或"否"。
   - 格式：<query_sweep>l,r,k</query_sweep>
   - 例如：<query_sweep>1,10,3</query_sweep>

提交诊断报告：
当你收集到足够信息后，请提交最终判定结果：

- 若判定致病基因存在，必须给出一个具体的起始位点 j，格式如下：
  <answer>存在,j={{j}}</answer>
  
- 若判定未发现致病基因，格式如下：
  <answer>不存在</answer>

重要提示：
- 若判定"存在"，你必须确保该起始位点 j 的 Align(j) 等于 {m}（通过基因表达匹配查询确认）。
- 若判定"不存在"，你需要通过筛查证明所有可能的起始位点都不满足完整表达匹配。
- 请尽可能少地使用查询次数来完成判定。
- 答案错误或格式不符将导致诊断失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Genomic Sequence Screening System. We need to locate a specific pathogenic gene segment within a patient's extended genetic sequence map.

System Setup:
- There is a genetic feature alphabet Σ (containing all uppercase English letters A to Z).
- There is a hidden patient genomic sequence S of length {n}, where each position represents a characteristic base pair. The sequence is indexed starting from 1, i.e., S[1] to S[{n}].
- We are searching for a known public pathogenic gene segment P = "{pattern}" of length {m}.

Your Goal:
Determine whether there exists a starting loci position j (1 less than or equal to j less than or equal to {max_start}) such that the pathogenic gene segment P appears as a complete consecutive sequence in the hidden patient sequence S, i.e., S[j] to S[j+{m}-1] exactly matches P[1] to P[{m}].

Available Screening Tools (only one query per turn):

1. Gene Expression Match Query Align(i):
   - Ask for the longest consecutive prefix match length between the hidden patient sequence S starting at loci i and the pathogenic segment P.
   - Returns an integer L(i), the maximum t (0 less than or equal to t less than or equal to min({m}, {n} - i + 1)) such that S[i] to S[i+t-1] exactly matches P[1] to P[t].
   - Format: <query_align>i</query_align>
   - Example: <query_align>5</query_align>

2. Interval Screening Query Sweep(l, r, k):
   - Ask whether there exists a loci position j in the starting range [l, r] (1 less than or equal to l less than or equal to r less than or equal to {max_start}) such that the Gene Expression Match Query Align(j) is greater than or equal to k.
   - Note: k must be strictly less than {m}; you cannot directly ask if a complete gene mutation match exists.
   - Returns "Yes" or "No".
   - Format: <query_sweep>l,r,k</query_sweep>
   - Example: <query_sweep>1,10,3</query_sweep>

Submitting Diagnostic Report:
When you have gathered enough information, submit your final determination:

- If you determine the pathogenic gene exists, you must provide a specific starting loci position j in this format:
  <answer>exists,j={{j}}</answer>
  
- If you determine the pathogenic gene is not found, use this format:
  <answer>not_exists</answer>

Important Notes:
- If you determine "exists", you must ensure that Align(j) equals {m} for the loci j (confirmed via Gene Expression Match Query).
- If you determine "not exists", you need to prove through screening that all possible starting loci do not satisfy a complete expression match.
- Please use as few queries as possible to complete the determination.
- Incorrect answers or invalid formats will result in diagnostic failure.
"""

    contextualized_rule_zh_3 = """\
欢迎进入学术诚信检测系统。我们需要核查一份提交的论文中是否完整抄袭了特定的文献段落。

系统设定：
- 存在一个文本字符特征字母表Σ（包含所有大写英文字母A到Z）。
- 系统解析出一段长度为 {n} 的隐藏论文文本序列 S。序列索引从1开始，即 S[1] 到 S[{n}]。
- 我们正在核查一段疑似被抄袭的长度为 {m} 的公开文献片段 P = "{pattern}"。

你的目标：
判断是否存在某个起始字符位置 j（1 小于等于 j 小于等于 {max_start}），使得抄袭文献片段 P 作为连续的文本完整出现在隐藏论文序列 S 中，即 S[j] 到 S[j+{m}-1] 与 P[1] 到 P[{m}] 完全相同。

可用的查重手段（每次只能发起一个查询）：

1. 文本相似度比对查询 Align(i)：
   - 询问从文本位置 i 开始，隐藏论文序列 S 与疑似文献 P 的最长连续前缀匹配字符数。
   - 返回一个整数 L(i)，表示最大的 t（0 小于等于 t 小于等于 min({m}, {n} - i + 1)），使得 S[i] 到 S[i+t-1] 与 P[1] 到 P[t] 完全匹配。
   - 格式：<query_align>i</query_align>
   - 例如：<query_align>5</query_align>

2. 章节查重扫描查询 Sweep(l, r, k)：
   - 询问在起始文本范围 [l, r]（1 小于等于 l 小于等于 r 小于等于 {max_start}）内，是否存在某个位置 j 使得文本相似度比对查询 Align(j) 大于等于 k。
   - 注意：k 必须严格小于 {m}，不能直接询问是否存在完整的段落抄袭。
   - 返回"是"或"否"。
   - 格式：<query_sweep>l,r,k</query_sweep>
   - 例如：<query_sweep>1,10,3</query_sweep>

提交检测报告：
当你收集到足够信息后，请提交最终判定结果：

- 若判定存在完整抄袭行为，必须给出一个具体的起始位置 j，格式如下：
  <answer>存在,j={{j}}</answer>
  
- 若判定未发生完整抄袭，格式如下：
  <answer>不存在</answer>

重要提示：
- 若判定"存在"，你必须确保该起始位置 j 的 Align(j) 等于 {m}（通过文本相似度比对查询确认）。
- 若判定"不存在"，你需要通过扫描证明所有可能的起始位置都不满足完整相似度匹配。
- 请尽可能少地使用查询次数来完成判定。
- 答案错误或格式不符将导致查重失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Academic Integrity Detection System. We need to verify whether a submitted paper completely plagiarized a specific literature segment.

System Setup:
- There is a text character feature alphabet Σ (containing all uppercase English letters A to Z).
- The system parsed a hidden paper text sequence S of length {n}. The sequence is indexed starting from 1, i.e., S[1] to S[{n}].
- We are verifying a public suspected plagiarized literature segment P = "{pattern}" of length {m}.

Your Goal:
Determine whether there exists a starting character position j (1 less than or equal to j less than or equal to {max_start}) such that the plagiarized literature segment P appears as a complete consecutive text in the hidden paper sequence S, i.e., S[j] to S[j+{m}-1] exactly matches P[1] to P[{m}].

Available Verification Tools (only one query per turn):

1. Text Similarity Alignment Query Align(i):
   - Ask for the longest consecutive matching character count between the hidden paper sequence S starting at text position i and the literature segment P.
   - Returns an integer L(i), the maximum t (0 less than or equal to t less than or equal to min({m}, {n} - i + 1)) such that S[i] to S[i+t-1] exactly matches P[1] to P[t].
   - Format: <query_align>i</query_align>
   - Example: <query_align>5</query_align>

2. Section Plagiarism Scan Query Sweep(l, r, k):
   - Ask whether there exists a position j in the starting text range [l, r] (1 less than or equal to l less than or equal to r less than or equal to {max_start}) such that the Text Similarity Alignment Query Align(j) is greater than or equal to k.
   - Note: k must be strictly less than {m}; you cannot directly ask if a complete paragraph plagiarism exists.
   - Returns "Yes" or "No".
   - Format: <query_sweep>l,r,k</query_sweep>
   - Example: <query_sweep>1,10,3</query_sweep>

Submitting Detection Report:
When you have gathered enough information, submit your final determination:

- If you determine complete plagiarism exists, you must provide a specific starting position j in this format:
  <answer>exists,j={{j}}</answer>
  
- If you determine no complete plagiarism occurred, use this format:
  <answer>not_exists</answer>

Important Notes:
- If you determine "exists", you must ensure that Align(j) equals {m} for the position j (confirmed via Text Similarity Alignment Query).
- If you determine "not exists", you need to prove through scanning that all possible starting positions do not satisfy a complete similarity match.
- Please use as few queries as possible to complete the determination.
- Incorrect answers or invalid formats will result in verification failure.
"""

    contextualized_rule_zh_4 = """\
欢迎使用工业流水线质量质检系统。我们需要在一批流水线产品的状态代码序列中排查特定的严重缺陷特征。

系统设定：
- 存在一个产品状态特征字母表Σ（包含所有大写英文字母A到Z）。
- 存在一条长度为 {n} 的隐藏产品状态序列 S，其中每个位置的字符代表该批次某个组件的监测代码。序列索引从1开始，即 S[1] 到 S[{n}]。
- 系统载入了一条长度为 {m} 的公开严重缺陷特征序列 P = "{pattern}"。

你的目标：
判断是否存在某个起始组件位置 j（1 小于等于 j 小于等于 {max_start}），使得严重缺陷特征序列 P 作为连续的错误警报完整出现在隐藏状态序列 S 中，即 S[j] 到 S[j+{m}-1] 与 P[1] 到 P[{m}] 完全相同。

可用的质检排查手段（每次只能发起一个查询）：

1. 缺陷特征对齐查询 Align(i)：
   - 询问从组件位置 i 开始，隐藏状态序列 S 与严重缺陷特征 P 的最长连续前缀匹配长度。
   - 返回一个整数 L(i)，表示最大的 t（0 小于等于 t 小于等于 min({m}, {n} - i + 1)），使得 S[i] 到 S[i+t-1] 与 P[1] 到 P[t] 完全匹配。
   - 格式：<query_align>i</query_align>
   - 例如：<query_align>5</query_align>

2. 批次排查查询 Sweep(l, r, k)：
   - 询问在起始组件范围 [l, r]（1 小于等于 l 小于等于 r 小于等于 {max_start}）内，是否存在某个位置 j 使得缺陷特征对齐查询 Align(j) 大于等于 k。
   - 注意：k 必须严格小于 {m}，不能直接询问是否存在完整的严重缺陷链。
   - 返回"是"或"否"。
   - 格式：<query_sweep>l,r,k</query_sweep>
   - 例如：<query_sweep>1,10,3</query_sweep>

提交质检报告：
当你收集到足够信息后，请提交最终判定结果：

- 若判定出现了严重缺陷，必须给出一个具体的起始位置 j，格式如下：
  <answer>存在,j={{j}}</answer>
  
- 若判定未发现该严重缺陷，格式如下：
  <answer>不存在</answer>

重要提示：
- 若判定"存在"，你必须确保该起始位置 j 的 Align(j) 等于 {m}（通过缺陷特征对齐查询确认）。
- 若判定"不存在"，你需要通过排查证明所有可能的起始位置都不满足完整缺陷匹配。
- 请尽可能少地使用查询次数来完成判定。
- 答案错误或格式不符将导致质检评估失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Industrial Assembly Line Quality Control System. We need to detect a specific critical defect signature in a batch's status code sequence.

System Setup:
- There is a product status feature alphabet Σ (containing all uppercase English letters A to Z).
- There is a hidden product status sequence S of length {n}, where each position represents a monitoring code of a component in the batch. The sequence is indexed starting from 1, i.e., S[1] to S[{n}].
- The system loaded a public critical defect signature sequence P = "{pattern}" of length {m}.

Your Goal:
Determine whether there exists a starting component position j (1 less than or equal to j less than or equal to {max_start}) such that the critical defect signature P appears as a complete consecutive sequence of error alerts in the hidden status sequence S, i.e., S[j] to S[j+{m}-1] exactly matches P[1] to P[{m}].

Available Inspection Tools (only one query per turn):

1. Defect Signature Alignment Query Align(i):
   - Ask for the longest consecutive prefix match length between the hidden status sequence S starting at component position i and the critical defect signature P.
   - Returns an integer L(i), the maximum t (0 less than or equal to t less than or equal to min({m}, {n} - i + 1)) such that S[i] to S[i+t-1] exactly matches P[1] to P[t].
   - Format: <query_align>i</query_align>
   - Example: <query_align>5</query_align>

2. Batch Inspection Query Sweep(l, r, k):
   - Ask whether there exists a position j in the starting component range [l, r] (1 less than or equal to l less than or equal to r less than or equal to {max_start}) such that the Defect Signature Alignment Query Align(j) is greater than or equal to k.
   - Note: k must be strictly less than {m}; you cannot directly ask if a complete critical defect chain exists.
   - Returns "Yes" or "No".
   - Format: <query_sweep>l,r,k</query_sweep>
   - Example: <query_sweep>1,10,3</query_sweep>

Submitting Inspection Report:
When you have gathered enough information, submit your final determination:

- If you determine the critical defect exists, you must provide a specific starting position j in this format:
  <answer>exists,j={{j}}</answer>
  
- If you determine the critical defect is not found, use this format:
  <answer>not_exists</answer>

Important Notes:
- If you determine "exists", you must ensure that Align(j) equals {m} for the position j (confirmed via Defect Signature Alignment Query).
- If you determine "not exists", you need to prove through inspections that all possible starting positions do not satisfy a complete defect match.
- Please use as few queries as possible to complete the determination.
- Incorrect answers or invalid formats will result in quality assessment failure.
"""

    contextualized_rule_zh_5 = """\
欢迎使用金融犯罪取证系统。我们需要在庞杂的交易流水日志中，锁定一条确凿的连环欺诈证据链。

系统设定：
- 存在一个交易行为特征字母表Σ（包含所有大写英文字母A到Z）。
- 提取出一条长度为 {n} 的隐藏交易行为记录序列 S，每个位置的字符代表一条时序日志的特征。序列索引从1开始，即 S[1] 到 S[{n}]。
- 已确立了一条长度为 {m} 的公开连环欺诈特征证据链 P = "{pattern}"。

你的目标：
判断是否存在某个起始交易记录位置 j（1 小于等于 j 小于等于 {max_start}），使得连环欺诈特征 P 作为连续的交易行为完整出现在隐藏审计序列 S 中，即 S[j] 到 S[j+{m}-1] 与 P[1] 到 P[{m}] 完全相同。

可用的审计取证手段（每次只能发起一个查询）：

1. 证据链比对查询 Align(i)：
   - 询问从交易记录位置 i 开始，隐藏交易序列 S 与欺诈证据链 P 的最长连续前缀匹配长度。
   - 返回一个整数 L(i)，表示最大的 t（0 小于等于 t 小于等于 min({m}, {n} - i + 1)），使得 S[i] 到 S[i+t-1] 与 P[1] 到 P[t] 完全匹配。
   - 格式：<query_align>i</query_align>
   - 例如：<query_align>5</query_align>

2. 审计区间排查查询 Sweep(l, r, k)：
   - 询问在起始记录范围 [l, r]（1 小于等于 l 小于等于 r 小于等于 {max_start}）内，是否存在某个位置 j 使得证据链比对查询 Align(j) 大于等于 k。
   - 注意：k 必须严格小于 {m}，不能直接询问是否存在完整的连环欺诈证据链。
   - 返回"是"或"否"。
   - 格式：<query_sweep>l,r,k</query_sweep>
   - 例如：<query_sweep>1,10,3</query_sweep>

提交取证报告：
当你收集到足够信息后，请提交最终判定结果：

- 若判定该连环欺诈行为成立，必须给出一个具体的起始位置 j，格式如下：
  <answer>存在,j={{j}}</answer>
  
- 若判定缺乏确凿连环欺诈证据，格式如下：
  <answer>不存在</answer>

重要提示：
- 若判定"存在"，你必须确保该起始位置 j 的 Align(j) 等于 {m}（通过证据链比对查询确认）。
- 若判定"不存在"，你需要通过排查证明所有可能的起始位置都不满足完整证据链匹配。
- 请尽可能少地使用查询次数来完成判定。
- 答案错误或格式不符将导致取证程序失败。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Financial Crime Forensics System. We need to pinpoint a definitive serial fraud evidence chain within a massive transaction log.

System Setup:
- There is a transaction behavior feature alphabet Σ (containing all uppercase English letters A to Z).
- A hidden transaction behavior record sequence S of length {n} has been extracted, where each position represents a characteristic of a chronological log entry. The sequence is indexed starting from 1, i.e., S[1] to S[{n}].
- We have established a public serial fraud signature evidence chain P = "{pattern}" of length {m}.

Your Goal:
Determine whether there exists a starting transaction record position j (1 less than or equal to j less than or equal to {max_start}) such that the serial fraud signature P appears as a complete consecutive transaction behavior in the hidden audit sequence S, i.e., S[j] to S[j+{m}-1] exactly matches P[1] to P[{m}].

Available Forensic Tools (only one query per turn):

1. Evidence Chain Alignment Query Align(i):
   - Ask for the longest consecutive prefix match length between the hidden transaction sequence S starting at record position i and the fraud evidence chain P.
   - Returns an integer L(i), the maximum t (0 less than or equal to t less than or equal to min({m}, {n} - i + 1)) such that S[i] to S[i+t-1] exactly matches P[1] to P[t].
   - Format: <query_align>i</query_align>
   - Example: <query_align>5</query_align>

2. Audit Range Scan Query Sweep(l, r, k):
   - Ask whether there exists a position j in the starting record range [l, r] (1 less than or equal to l less than or equal to r less than or equal to {max_start}) such that the Evidence Chain Alignment Query Align(j) is greater than or equal to k.
   - Note: k must be strictly less than {m}; you cannot directly ask if a complete serial fraud evidence chain exists.
   - Returns "Yes" or "No".
   - Format: <query_sweep>l,r,k</query_sweep>
   - Example: <query_sweep>1,10,3</query_sweep>

Submitting Forensic Report:
When you have gathered enough information, submit your final determination:

- If you determine the serial fraud behavior occurred, you must provide a specific starting position j in this format:
  <answer>exists,j={{j}}</answer>
  
- If you determine there is no definitive serial fraud evidence, use this format:
  <answer>not_exists</answer>

Important Notes:
- If you determine "exists", you must ensure that Align(j) equals {m} for the position j (confirmed via Evidence Chain Alignment Query).
- If you determine "not exists", you need to prove through scanning that all possible starting positions do not satisfy a complete evidence chain match.
- Please use as few queries as possible to complete the determination.
- Incorrect answers or invalid formats will result in forensic procedure failure.
"""

    tags = ["answer", "query_align", "query_sweep"]
    reasoning_type = "演绎推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 10,
                "pattern": "ABC",
                "sequence": "XYZABCDEFG",
            },
            2: {
                "n": 15,
                "pattern": "ABCD",
                "sequence": "ABABCABCDXYZABC",
            },
            3: {
                "n": 20,
                "pattern": "HELLO",
                "sequence": "XHELHELLOHELLOXYZABC",
            },
            4: {
                "n": 23, 
                "pattern": "MATCH",
                "sequence": "MATMATCHMATCXMATCMATCHZ",
            },
            5: {
                "n": 30, 
                "pattern": "PATTERN",
                "sequence": "PATTERNXPATTERPATTERPATTERNYZX",
            },
        },
        "en": {
            1: {
                "n": 10,
                "pattern": "ABC",
                "sequence": "XYZABCDEFG",
            },
            2: {
                "n": 15,
                "pattern": "ABCD",
                "sequence": "ABABCABCDXYZABC",
            },
            3: {
                "n": 20,
                "pattern": "HELLO",
                "sequence": "XHELHELLOHELLOXYZABC",
            },
            4: {
                "n": 23, 
                "pattern": "MATCH",
                "sequence": "MATMATCHMATCXMATCMATCHZ",
            },
            5: {
                "n": 30, 
                "pattern": "PATTERN",
                "sequence": "PATTERNXPATTERPATTERPATTERNYZX",
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
        
        self.sequence = cfg["sequence"]
        self.pattern = cfg["pattern"]
        self.n = cfg["n"]
        self.m = len(self.pattern)
        
        assert len(self.sequence) == self.n, \
            f"Sequence length mismatch: declared n={self.n}, actual len={len(self.sequence)}"
        
        self.max_start = self.n - self.m + 1

        self._precompute_alignments()
        
        self._game_info = {
            "n": self.n,
            "m": self.m,
            "pattern": self.pattern,
            "max_start": self.max_start,
        }

    def _precompute_alignments(self):
        self.align_values = {}
        for i in range(1, self.n + 1):
            max_len = min(self.m, self.n - i + 1)
            match_len = 0
            for t in range(max_len):
                if self.sequence[i - 1 + t] == self.pattern[t]:
                    match_len += 1
                else:
                    break
            self.align_values[i] = match_len

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        if self.config.language == "zh":
            if raw_ans.startswith("存在"):
                match = re.search(r'j=(\d+)', raw_ans)
                if not match:
                    return False
                j = int(match.group(1))
                
                if j < 1 or j > self.max_start:
                    return False
                return self.align_values[j] == self.m
            
            elif raw_ans == "不存在":
                for j in range(1, self.max_start + 1):
                    if self.align_values[j] == self.m:
                        return False
                return True
            else:
                return False
        else:
            if raw_ans.startswith("exists"):
                match = re.search(r'j=(\d+)', raw_ans)
                if not match:
                    return False
                j = int(match.group(1))
                
                if j < 1 or j > self.max_start:
                    return False
                return self.align_values[j] == self.m
            
            elif raw_ans == "not_exists":
                for j in range(1, self.max_start + 1):
                    if self.align_values[j] == self.m:
                        return False
                return True
            else:
                return False

    def _cf_core_produce(self, parsed_info):
        is_zh = (self.config.language == "zh")
        
        if "query_align" in parsed_info:
            try:
                i = int(parsed_info["query_align"].strip())
                if i < 1 or i > self.n:
                    return "错误：位置超出范围。" if is_zh else "Error: Position out of range."
                
                align_value = self.align_values[i]
                return str(align_value)
            except ValueError:
                return "错误：无效的位置格式。" if is_zh else "Error: Invalid position format."
        
        elif "query_sweep" in parsed_info:
            try:
                raw = parsed_info["query_sweep"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 3:
                    raise ValueError
                
                l, r, k = int(parts[0]), int(parts[1]), int(parts[2])
                
                if l < 1 or r > self.max_start or l > r:
                    return "错误：区间范围无效。" if is_zh else "Error: Invalid range."
                if k < 1:
                    return "错误：k 必须为正整数。" if is_zh else "Error: k must be a positive integer."
                if k >= self.m:
                    return f"错误：k 必须严格小于 {self.m}。" if is_zh else f"Error: k must be strictly less than {self.m}."
                
                exists = False
                for j in range(l, r + 1):
                    if self.align_values[j] >= k:
                        exists = True
                        break
                
                if is_zh:
                    return "是" if exists else "否"
                else:
                    return "Yes" if exists else "No"
                    
            except (ValueError, IndexError):
                return "错误：无效的查询格式。" if is_zh else "Error: Invalid query format."
        
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        for i in range(1, self.n + 1):
            query_content = str(i)
            parsed_info = {"query_align": query_content}
            answer = self._cf_core_produce(parsed_info)
            results.append({
                "query": f"<query_align>{query_content}</query_align>",
                "answer": answer
            })
            
        for l in range(1, self.max_start + 1):
            for r in range(l, self.max_start + 1):
                for k in range(1, self.m):
                    query_content = f"{l},{r},{k}"
                    parsed_info = {"query_sweep": query_content}
                    answer = self._cf_core_produce(parsed_info)
                    results.append({
                        "query": f"<query_sweep>{query_content}</query_sweep>",
                        "answer": answer
                    })
                    
        return results

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        if correct.lower() == "yes":
            return "No" if correct[0].isupper() else "no"
        if correct.lower() == "no":
            return "Yes" if correct[0].isupper() else "yes"
            
        return correct + "_WRONG"