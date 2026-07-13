# -*- coding: utf-8 -*-

from .base import Game
import random
import re

class TreeDeletionRuleGame(Game):

    tags = ["query_inspect", "query_verify", "query_position", "query_symbol", "answer"]
    reasoning_type = "归纳推理"
    data_structure = "树"

    # ================= 场景1：交通（物流网络路线溯源） =================
    contextualized_rule_zh_1 = """\
欢迎使用智能物流网络路线溯源系统。我们需要排查一条异常路线的衍生来源。规则如下：

系统记录了有限集合的单向递进路线网络，共有 {n} 个路线节点。每个节点有唯一路线ID和一个站点序列（由代表中转站的字母表 {alphabet} 中的字符组成）。源头路线的序列为空串，非源头路线的序列长度在1到6之间。

路线的衍生关系由一个隐藏但全局一致的站点削减策略 R 决定：对任意非源头路线，其上游基准路线的站点序列等于从当前路线序列中削减恰好一个中转站点后得到的结果。削减策略 R 只依赖路线自身的序列，是确定且一致的（包含固定的并列打破规则），使得每个非源头路线的上游基准路线唯一。

在排查开始时，你可以看到所有路线的ID和序列信息：
{nodes_info}

目标排查路线为：ID={target_id}, 站点序列="{target_label}"

你的任务是：在不直接查询目标路线的前提下，通过对其他路线的交互查询，推断出站点削减策略 R，并据此确定目标路线的上游基准路线。

## 可用查询类型

你可以对非目标路线进行以下查询（每次只能提出一个查询）：

1. **完整查询（Inspect）**：询问某路线的上游基准路线ID和基准序列
   - 此类查询有次数上限 {inspect_limit} 次
   
2. **验证查询（Verify）**：验证某路线的上游基准序列是否为指定值
   - 返回"是"或"否"
   
3. **位置查询（RemovedPosition）**：询问某路线由基准衍生时被削减的站点位置（1表示最左侧）
   
4. **符号查询（RemovedSymbol）**：询问某路线由基准衍生时被削减的具体站点代号

所有查询（除最终排查报告外）的总次数不得超过 {max_queries} 次。

## 查询格式（严格要求）

每次只能包含一个查询标签，使用以下XML格式：

- 完整查询（例如查询ID为2的路线）：
<query_inspect>2</query_inspect>

- 验证查询（例如验证ID为3的路线，上游基准序列是否为"ABC"）：
<query_verify>3,ABC</query_verify>

- 位置查询（例如查询ID为4的路线）：
<query_position>4</query_position>

- 符号查询（例如查询ID为5的路线）：
<query_symbol>5</query_symbol>

## 提交最终排查报告

当你收集了足够信息后（至少完成3次有效查询），请提交目标路线的上游基准路线信息。你可以提交基准ID或基准序列（或两者都提交）：

提交上游基准ID（例如基准ID为1）：
<answer>parent_id=1</answer>

提交上游基准序列（例如基准序列为"AB"）：
<answer>parent_label=AB</answer>

同时提交（推荐）：
<answer>parent_id=1, parent_label=AB</answer>

注意：
- 不能对目标路线进行任何查询
- 必须完成至少3次有效查询才能提交排查报告
- 查询总次数（不含最终报告）不得超过上限
- 报告错误或格式不符将导致排查失败
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Smart Logistics Network Route Tracing System. We need to trace the origin of an anomalous route. Here are the rules:

The system records a finite set of unidirectional progressive route network paths, consisting of {n} route nodes. Each node has a unique route ID and a waypoint sequence composed of characters from the transit station alphabet {alphabet}. The source route has an empty sequence, and non-source routes have sequences of length 1 to 6.

The derivation relationship between routes is determined by a hidden but globally consistent waypoint reduction policy R: for any non-source route, its upstream base route's sequence equals the result of deleting exactly one transit station from that route's sequence. Policy R depends only on the route's own sequence, is deterministic and consistent (including fixed tie-breaking rules), ensuring each non-source route has a unique upstream base route.

At the start of the tracing, you can see all routes' IDs and sequences:
{nodes_info}

Target route to trace: ID={target_id}, Waypoint Sequence="{target_label}"

Your task: Without directly querying the target route, infer the waypoint reduction policy R through interactive queries on other routes, and determine the target route's upstream base route.

## Available Query Types

You can perform the following queries on non-target routes (one query at a time):

1. **Inspect Query**: Ask for a route's upstream base route ID and base sequence
   - Limited to {inspect_limit} uses
   
2. **Verify Query**: Verify if a route's upstream base sequence equals a proposed value
   - Returns "Yes" or "No"
   
3. **Position Query (RemovedPosition)**: Ask which position's transit station was reduced during derivation (1 = leftmost)
   
4. **Symbol Query (RemovedSymbol)**: Ask which specific transit station code was reduced

Total queries (excluding the final tracing report) cannot exceed {max_queries}.

## Query Format (strictly required)

Each query must contain only one tag, using XML format:

- Inspect query (e.g., query route ID 2):
<query_inspect>2</query_inspect>

- Verify query (e.g., verify if route ID 3's upstream base sequence is "ABC"):
<query_verify>3,ABC</query_verify>

- Position query (e.g., query route ID 4):
<query_position>4</query_position>

- Symbol query (e.g., query route ID 5):
<query_symbol>5</query_symbol>

## Submit Final Tracing Report

After collecting sufficient information (at least 3 valid queries), submit the target route's upstream base route information. You can submit base route ID or base sequence (or both):

Submit base route ID (e.g., base ID is 1):
<answer>parent_id=1</answer>

Submit base sequence (e.g., base sequence is "AB"):
<answer>parent_label=AB</answer>

Submit both (recommended):
<answer>parent_id=1, parent_label=AB</answer>

Notes:
- Cannot query the target route
- Must complete at least 3 valid queries before submitting the report
- Total queries (excluding final report) cannot exceed limit
- Wrong report or invalid format leads to tracing failure
"""

    # ================= 场景2：医疗（病毒变异谱系分析） =================
    contextualized_rule_zh_2 = """\
欢迎使用病毒变异谱系分析系统。我们需要追溯一种新型变异株的变异来源。规则如下：

系统内收录了有限集合的毒株样本网络，共有 {n} 个毒株节点。每个毒株有唯一编号和一个由碱基序列（字母表 {alphabet} 中的字符）组成的基因片段。原始毒株的基因序列为空串，非原始毒株的序列长度在1到6之间。

毒株的突变关系由一个隐藏且全局一致的基因溯源逆推法则 R 决定：对任意衍生毒株，其上游变异母体的基因片段等于从当前毒株序列中移除恰好一个突变碱基后得到的结果。逆推法则 R 只依赖毒株自身的序列，是确定且一致的（包含固定的并列打破规则），使得每个衍生毒株的上游变异母体唯一。

在分析开始时，你可以看到所有毒株的编号和基因片段信息：
{nodes_info}

目标分析毒株为：编号={target_id}, 基因片段="{target_label}"

你的任务是：在不直接查询目标毒株的前提下，通过对其他毒株的交互查询，推断出基因溯源逆推法则 R，并据此确定目标毒株的上游变异母体。

## 可用查询类型

你可以对非目标毒株进行以下查询（每次只能提出一个查询）：

1. **完整查询（Inspect）**：询问某毒株的变异母体编号和母体基因片段
   - 此类查询有次数上限 {inspect_limit} 次
   
2. **验证查询（Verify）**：验证某毒株的母体基因片段是否为指定值
   - 返回"是"或"否"
   
3. **位置查询（RemovedPosition）**：询问某毒株在逆推母体时被移除的碱基位置（1表示最左侧）
   
4. **符号查询（RemovedSymbol）**：询问某毒株在逆推母体时被移除的具体碱基代号

所有查询（除最终分析报告外）的总次数不得超过 {max_queries} 次。

## 查询格式（严格要求）

每次只能包含一个查询标签，使用以下XML格式：

- 完整查询（例如查询编号为2的毒株）：
<query_inspect>2</query_inspect>

- 验证查询（例如验证编号为3的毒株，母体基因片段是否为"ABC"）：
<query_verify>3,ABC</query_verify>

- 位置查询（例如查询编号为4的毒株）：
<query_position>4</query_position>

- 符号查询（例如查询编号为5的毒株）：
<query_symbol>5</query_symbol>

## 提交最终分析报告

当你收集了足够信息后（至少完成3次有效查询），请提交目标毒株的变异母体信息。你可以提交母体编号或母体基因片段（或两者都提交）：

提交变异母体编号（例如母体编号为1）：
<answer>parent_id=1</answer>

提交变异母体片段（例如母体片段为"AB"）：
<answer>parent_label=AB</answer>

同时提交（推荐）：
<answer>parent_id=1, parent_label=AB</answer>

注意：
- 不能对目标毒株进行任何查询
- 必须完成至少3次有效查询才能提交报告
- 查询总次数（不含最终报告）不得超过上限
- 报告错误或格式不符将导致溯源失败
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Viral Mutation Lineage Analysis System. We need to trace the mutation origin of a novel strain. Here are the rules:

The system contains a finite network of strain samples, with {n} strain nodes in total. Each strain has a unique ID and a gene segment composed of nucleotide sequences (characters from the alphabet {alphabet}). Patient Zero's gene sequence is an empty string, while derived strains have sequences of length 1 to 6.

The mutation lineage is determined by a hidden but globally consistent Genetic Traceback Reversion Rule R: for any derived strain, its parent strain's gene segment equals the result of removing exactly one mutated nucleotide from the current strain's sequence. Rule R depends only on the strain's own sequence, is deterministic and consistent (including fixed tie-breaking rules), ensuring each derived strain has a unique parent strain.

At the start of the analysis, you can see all strains' IDs and gene segments:
{nodes_info}

Target strain for analysis: ID={target_id}, Gene Segment="{target_label}"

Your task: Without directly querying the target strain, infer the Genetic Traceback Reversion Rule R through interactive queries on other strains, and determine the target strain's parent strain.

## Available Query Types

You can perform the following queries on non-target strains (one query at a time):

1. **Inspect Query**: Ask for a strain's parent strain ID and parent gene segment
   - Limited to {inspect_limit} uses
   
2. **Verify Query**: Verify if a strain's parent gene segment equals a proposed value
   - Returns "Yes" or "No"
   
3. **Position Query (RemovedPosition)**: Ask which position's nucleotide was removed during traceback (1 = leftmost)
   
4. **Symbol Query (RemovedSymbol)**: Ask which specific nucleotide code was removed

Total queries (excluding the final analysis report) cannot exceed {max_queries}.

## Query Format (strictly required)

Each query must contain only one tag, using XML format:

- Inspect query (e.g., query strain ID 2):
<query_inspect>2</query_inspect>

- Verify query (e.g., verify if strain ID 3's parent gene segment is "ABC"):
<query_verify>3,ABC</query_verify>

- Position query (e.g., query strain ID 4):
<query_position>4</query_position>

- Symbol query (e.g., query strain ID 5):
<query_symbol>5</query_symbol>

## Submit Final Analysis Report

After collecting sufficient information (at least 3 valid queries), submit the target strain's parent strain information. You can submit parent strain ID or parent gene segment (or both):

Submit parent strain ID (e.g., parent ID is 1):
<answer>parent_id=1</answer>

Submit parent gene segment (e.g., parent segment is "AB"):
<answer>parent_label=AB</answer>

Submit both (recommended):
<answer>parent_id=1, parent_label=AB</answer>

Notes:
- Cannot query the target strain
- Must complete at least 3 valid queries before submitting the report
- Total queries (excluding final report) cannot exceed limit
- Wrong report or invalid format leads to tracing failure
"""

    # ================= 场景3：教育（认知概念前置路径分析） =================
    contextualized_rule_zh_3 = """\
欢迎使用认知概念前置路径分析系统。我们需要排查一个高阶知识点的基础衍生来源。规则如下：

系统记录了有限集合的递进式知识网络，共有 {n} 个概念节点。每个节点有唯一概念ID和一个由技能标签（代表不同技能模块的字母表 {alphabet} 中的字符）组成的学习序列。最基础的起点概念序列为空串，衍生概念的序列长度在1到6之间。

概念间的衍生关系由一个隐藏但全局一致的前置概念逆推法则 R 决定：对任意衍生概念，其直接前置概念的学习序列等于从当前概念序列中移除恰好一个技能标签后得到的结果。逆推法则 R 只依赖概念自身的序列，是确定且一致的（包含固定的并列打破规则），使得每个衍生概念的直接前置概念唯一。

在分析开始时，你可以看到所有概念的ID和学习序列信息：
{nodes_info}

目标分析概念为：ID={target_id}, 学习序列="{target_label}"

你的任务是：在不直接查询目标概念的前提下，通过对其他概念的交互查询，推断出前置概念逆推法则 R，并据此确定目标概念的直接前置概念。

## 可用查询类型

你可以对非目标概念进行以下查询（每次只能提出一个查询）：

1. **完整查询（Inspect）**：询问某概念的直接前置概念ID和前置序列
   - 此类查询有次数上限 {inspect_limit} 次
   
2. **验证查询（Verify）**：验证某概念的前置序列是否为指定值
   - 返回"是"或"否"
   
3. **位置查询（RemovedPosition）**：询问某概念在逆推前置概念时被移除的技能标签位置（1表示最左侧）
   
4. **符号查询（RemovedSymbol）**：询问某概念在逆推前置概念时被移除的具体技能标签代号

所有查询（除最终分析报告外）的总次数不得超过 {max_queries} 次。

## 查询格式（严格要求）

每次只能包含一个查询标签，使用以下XML格式：

- 完整查询（例如查询ID为2的概念）：
<query_inspect>2</query_inspect>

- 验证查询（例如验证ID为3的概念，前置序列是否为"ABC"）：
<query_verify>3,ABC</query_verify>

- 位置查询（例如查询ID为4的概念）：
<query_position>4</query_position>

- 符号查询（例如查询ID为5的概念）：
<query_symbol>5</query_symbol>

## 提交最终分析报告

当你收集了足够信息后（至少完成3次有效查询），请提交目标概念的直接前置概念信息。你可以提交前置概念ID或前置序列（或两者都提交）：

提交前置概念ID（例如前置ID为1）：
<answer>parent_id=1</answer>

提交前置序列（例如前置序列为"AB"）：
<answer>parent_label=AB</answer>

同时提交（推荐）：
<answer>parent_id=1, parent_label=AB</answer>

注意：
- 不能对目标概念进行任何查询
- 必须完成至少3次有效查询才能提交报告
- 查询总次数（不含最终报告）不得超过上限
- 报告错误或格式不符将导致分析失败
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Cognitive Concept Prerequisite Path Analysis System. We need to trace the foundational derivation of an advanced knowledge concept. Here are the rules:

The system records a finite progressive knowledge network, consisting of {n} concept nodes. Each node has a unique concept ID and a learning sequence composed of skill tags (characters from the alphabet {alphabet}). The most foundational starting concept has an empty sequence, while derived concepts have sequences of length 1 to 6.

The derivation relationship between concepts is determined by a hidden but globally consistent Prerequisite Concept Traceback Rule R: for any derived concept, its direct prerequisite concept's learning sequence equals the result of removing exactly one skill tag from the current concept's sequence. Rule R depends only on the concept's own sequence, is deterministic and consistent (including fixed tie-breaking rules), ensuring each derived concept has a unique direct prerequisite concept.

At the start of the analysis, you can see all concepts' IDs and learning sequences:
{nodes_info}

Target concept for analysis: ID={target_id}, Learning Sequence="{target_label}"

Your task: Without directly querying the target concept, infer the Prerequisite Concept Traceback Rule R through interactive queries on other concepts, and determine the target concept's direct prerequisite concept.

## Available Query Types

You can perform the following queries on non-target concepts (one query at a time):

1. **Inspect Query**: Ask for a concept's direct prerequisite concept ID and prerequisite sequence
   - Limited to {inspect_limit} uses
   
2. **Verify Query**: Verify if a concept's prerequisite sequence equals a proposed value
   - Returns "Yes" or "No"
   
3. **Position Query (RemovedPosition)**: Ask which position's skill tag was removed during traceback (1 = leftmost)
   
4. **Symbol Query (RemovedSymbol)**: Ask which specific skill tag code was removed

Total queries (excluding the final analysis report) cannot exceed {max_queries}.

## Query Format (strictly required)

Each query must contain only one tag, using XML format:

- Inspect query (e.g., query concept ID 2):
<query_inspect>2</query_inspect>

- Verify query (e.g., verify if concept ID 3's prerequisite sequence is "ABC"):
<query_verify>3,ABC</query_verify>

- Position query (e.g., query concept ID 4):
<query_position>4</query_position>

- Symbol query (e.g., query concept ID 5):
<query_symbol>5</query_symbol>

## Submit Final Analysis Report

After collecting sufficient information (at least 3 valid queries), submit the target concept's direct prerequisite concept information. You can submit prerequisite concept ID or prerequisite sequence (or both):

Submit prerequisite concept ID (e.g., prerequisite ID is 1):
<answer>parent_id=1</answer>

Submit prerequisite sequence (e.g., prerequisite sequence is "AB"):
<answer>parent_label=AB</answer>

Submit both (recommended):
<answer>parent_id=1, parent_label=AB</answer>

Notes:
- Cannot query the target concept
- Must complete at least 3 valid queries before submitting the report
- Total queries (excluding final report) cannot exceed limit
- Wrong report or invalid format leads to analysis failure
"""

    # ================= 场景4：制造业/工业（组件装配溯源） =================
    contextualized_rule_zh_4 = """\
欢迎使用工业组件装配溯源系统。我们需要排查一个缺陷组件的初始加工来源。规则如下：

系统记录了有限集合的单向递进装配网络，共有 {n} 个装配节点。每个节点有唯一批次ID和一个由工艺代码（代表操作指令的字母表 {alphabet} 中的字符）组成的指令序列。基础底座的序列为空串，衍生组件的序列长度在1到6之间。

组件间的装配衍生关系由一个隐藏但全局一致的逆向拆解法则 R 决定：对任意衍生组件，其上游基准组件的指令序列等于从当前组件序列中撤销恰好一个工艺代码后得到的结果。拆解法则 R 只依赖组件自身的序列，是确定且一致的（包含固定的并列打破规则），使得每个衍生组件的上游基准组件唯一。

在溯源开始时，你可以看到所有组件的批次ID和指令序列信息：
{nodes_info}

目标排查组件为：批次ID={target_id}, 指令序列="{target_label}"

你的任务是：在不直接查询目标组件的前提下，通过对其他组件的交互查询，推断出逆向拆解法则 R，并据此确定目标组件的上游基准组件。

## 可用查询类型

你可以对非目标组件进行以下查询（每次只能提出一个查询）：

1. **完整查询（Inspect）**：询问某组件的上游基准组件ID和基准序列
   - 此类查询有次数上限 {inspect_limit} 次
   
2. **验证查询（Verify）**：验证某组件的基准序列是否为指定值
   - 返回"是"或"否"
   
3. **位置查询（RemovedPosition）**：询问某组件在逆向拆解时被撤销的工艺代码位置（1表示最左侧）
   
4. **符号查询（RemovedSymbol）**：询问某组件在逆向拆解时被撤销的具体工艺代码

所有查询（除最终排查报告外）的总次数不得超过 {max_queries} 次。

## 查询格式（严格要求）

每次只能包含一个查询标签，使用以下XML格式：

- 完整查询（例如查询ID为2的组件）：
<query_inspect>2</query_inspect>

- 验证查询（例如验证ID为3的组件，基准序列是否为"ABC"）：
<query_verify>3,ABC</query_verify>

- 位置查询（例如查询ID为4的组件）：
<query_position>4</query_position>

- 符号查询（例如查询ID为5的组件）：
<query_symbol>5</query_symbol>

## 提交最终排查报告

当你收集了足够信息后（至少完成3次有效查询），请提交目标组件的上游基准组件信息。你可以提交基准ID或基准序列（或两者都提交）：

提交上游基准ID（例如基准ID为1）：
<answer>parent_id=1</answer>

提交上游基准序列（例如基准序列为"AB"）：
<answer>parent_label=AB</answer>

同时提交（推荐）：
<answer>parent_id=1, parent_label=AB</answer>

注意：
- 不能对目标组件进行任何查询
- 必须完成至少3次有效查询才能提交排查报告
- 查询总次数（不含最终报告）不得超过上限
- 报告错误或格式不符将导致溯源失败
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Industrial Component Assembly Traceback System. We need to trace the initial processing origin of a defective component. Here are the rules:

The system records a finite unidirectional progressive assembly network, consisting of {n} assembly nodes. Each node has a unique batch ID and an instruction sequence composed of process codes (characters from the alphabet {alphabet}). The base frame has an empty sequence, while derived components have sequences of length 1 to 6.

The assembly derivation relationship is determined by a hidden but globally consistent Reverse Disassembly Rule R: for any derived component, its upstream base component's instruction sequence equals the result of revoking exactly one process code from the current component's sequence. Rule R depends only on the component's own sequence, is deterministic and consistent (including fixed tie-breaking rules), ensuring each derived component has a unique upstream base component.

At the start of the traceback, you can see all components' batch IDs and instruction sequences:
{nodes_info}

Target component to trace: Batch ID={target_id}, Instruction Sequence="{target_label}"

Your task: Without directly querying the target component, infer the Reverse Disassembly Rule R through interactive queries on other components, and determine the target component's upstream base component.

## Available Query Types

You can perform the following queries on non-target components (one query at a time):

1. **Inspect Query**: Ask for a component's upstream base component ID and base sequence
   - Limited to {inspect_limit} uses
   
2. **Verify Query**: Verify if a component's base sequence equals a proposed value
   - Returns "Yes" or "No"
   
3. **Position Query (RemovedPosition)**: Ask which position's process code was revoked during disassembly (1 = leftmost)
   
4. **Symbol Query (RemovedSymbol)**: Ask which specific process code was revoked

Total queries (excluding the final traceback report) cannot exceed {max_queries}.

## Query Format (strictly required)

Each query must contain only one tag, using XML format:

- Inspect query (e.g., query component ID 2):
<query_inspect>2</query_inspect>

- Verify query (e.g., verify if component ID 3's base sequence is "ABC"):
<query_verify>3,ABC</query_verify>

- Position query (e.g., query component ID 4):
<query_position>4</query_position>

- Symbol query (e.g., query component ID 5):
<query_symbol>5</query_symbol>

## Submit Final Traceback Report

After collecting sufficient information (at least 3 valid queries), submit the target component's upstream base component information. You can submit base component ID or base sequence (or both):

Submit upstream base ID (e.g., base ID is 1):
<answer>parent_id=1</answer>

Submit upstream base sequence (e.g., base sequence is "AB"):
<answer>parent_label=AB</answer>

Submit both (recommended):
<answer>parent_id=1, parent_label=AB</answer>

Notes:
- Cannot query the target component
- Must complete at least 3 valid queries before submitting the report
- Total queries (excluding final report) cannot exceed limit
- Wrong report or invalid format leads to traceback failure
"""

    # ================= 场景5：法律（文书条款演变溯源） =================
    contextualized_rule_zh_5 = """\
欢迎使用法律文书条款演变溯源系统。我们需要排查一份争议合同的历史版本来源。规则如下：

系统记录了有限集合的递进式文书演变网络，共有 {n} 个文书版本。每个版本有唯一档案编号和一个由条款代码（代表各类条款的字母表 {alphabet} 中的字符）组成的条款序列。原始模板的序列为空串，衍生版本的序列长度在1到6之间。

版本间的演变关系由一个隐藏但全局一致的条款删减法则 R 决定：对任意衍生版本，其直接前置版本的条款序列等于从当前版本序列中删去恰好一个条款代码后得到的结果。删减法则 R 只依赖文书自身的序列，是确定且一致的（包含固定的并列打破规则），使得每个衍生版本的直接前置版本唯一。

在排查开始时，你可以看到所有版本的档案编号和条款序列信息：
{nodes_info}

目标争议版本为：档案编号={target_id}, 条款序列="{target_label}"

你的任务是：在不直接查询目标版本的前提下，通过对其他版本的交互查询，推断出条款删减法则 R，并据此确定目标争议版本的直接前置版本。

## 可用查询类型

你可以对非目标版本进行以下查询（每次只能提出一个查询）：

1. **完整查询（Inspect）**：询问某版本的直接前置版本编号和前置条款序列
   - 此类查询有次数上限 {inspect_limit} 次
   
2. **验证查询（Verify）**：验证某版本的前置条款序列是否为指定值
   - 返回"是"或"否"
   
3. **位置查询（RemovedPosition）**：询问某版本在逆推前置版本时被删去的条款代码位置（1表示最左侧）
   
4. **符号查询（RemovedSymbol）**：询问某版本在逆推前置版本时被删去的具体条款代码

所有查询（除最终排查报告外）的总次数不得超过 {max_queries} 次。

## 查询格式（严格要求）

每次只能包含一个查询标签，使用以下XML格式：

- 完整查询（例如查询编号为2的版本）：
<query_inspect>2</query_inspect>

- 验证查询（例如验证编号为3的版本，前置序列是否为"ABC"）：
<query_verify>3,ABC</query_verify>

- 位置查询（例如查询编号为4的版本）：
<query_position>4</query_position>

- 符号查询（例如查询编号为5的版本）：
<query_symbol>5</query_symbol>

## 提交最终排查报告

当你收集了足够信息后（至少完成3次有效查询），请提交目标版本的直接前置版本信息。你可以提交前置版本编号或前置条款序列（或两者都提交）：

提交前置版本编号（例如前置编号为1）：
<answer>parent_id=1</answer>

提交前置条款序列（例如前置序列为"AB"）：
<answer>parent_label=AB</answer>

同时提交（推荐）：
<answer>parent_id=1, parent_label=AB</answer>

注意：
- 不能对目标争议版本进行任何查询
- 必须完成至少3次有效查询才能提交排查报告
- 查询总次数（不含最终报告）不得超过上限
- 报告错误或格式不符将导致溯源失败
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the Legal Document Clause Evolution Traceback System. We need to trace the historical version origin of a disputed contract. Here are the rules:

The system records a finite progressive document evolution network, consisting of {n} document versions. Each version has a unique archive ID and a clause sequence composed of clause codes (characters from the alphabet {alphabet}). The original template has an empty sequence, while derived versions have sequences of length 1 to 6.

The evolution relationship between versions is determined by a hidden but globally consistent Clause Reduction Traceback Rule R: for any derived version, its direct predecessor version's clause sequence equals the result of deleting exactly one clause code from the current version's sequence. Rule R depends only on the document's own sequence, is deterministic and consistent (including fixed tie-breaking rules), ensuring each derived version has a unique direct predecessor version.

At the start of the traceback, you can see all versions' archive IDs and clause sequences:
{nodes_info}

Target disputed version: Archive ID={target_id}, Clause Sequence="{target_label}"

Your task: Without directly querying the target version, infer the Clause Reduction Traceback Rule R through interactive queries on other versions, and determine the target version's direct predecessor version.

## Available Query Types

You can perform the following queries on non-target versions (one query at a time):

1. **Inspect Query**: Ask for a version's direct predecessor version ID and predecessor clause sequence
   - Limited to {inspect_limit} uses
   
2. **Verify Query**: Verify if a version's predecessor clause sequence equals a proposed value
   - Returns "Yes" or "No"
   
3. **Position Query (RemovedPosition)**: Ask which position's clause code was deleted during traceback (1 = leftmost)
   
4. **Symbol Query (RemovedSymbol)**: Ask which specific clause code was deleted

Total queries (excluding the final traceback report) cannot exceed {max_queries}.

## Query Format (strictly required)

Each query must contain only one tag, using XML format:

- Inspect query (e.g., query version ID 2):
<query_inspect>2</query_inspect>

- Verify query (e.g., verify if version ID 3's predecessor sequence is "ABC"):
<query_verify>3,ABC</query_verify>

- Position query (e.g., query version ID 4):
<query_position>4</query_position>

- Symbol query (e.g., query version ID 5):
<query_symbol>5</query_symbol>

## Submit Final Traceback Report

After collecting sufficient information (at least 3 valid queries), submit the target version's direct predecessor version information. You can submit predecessor version ID or predecessor sequence (or both):

Submit predecessor version ID (e.g., predecessor ID is 1):
<answer>parent_id=1</answer>

Submit predecessor clause sequence (e.g., predecessor sequence is "AB"):
<answer>parent_label=AB</answer>

Submit both (recommended):
<answer>parent_id=1, parent_label=AB</answer>

Notes:
- Cannot query the target version
- Must complete at least 3 valid queries before submitting the report
- Total queries (excluding final report) cannot exceed limit
- Wrong report or invalid format leads to traceback failure
"""

    def _initialize_game(self):
        self.alphabet = random.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 5)
        self.n = 20
        self.inspect_limit = 3
        self.max_queries = 15

        def rule_R(seq: str):
            if not seq:
                return "", 0, ""
            target_char = max(list(seq))
            idx = seq.find(target_char)
            return seq[:idx] + seq[idx+1:], idx, target_char
            
        self.rule_R = rule_R

        self.nodes = {1: ""}
        self.label_to_id = {"": 1}
        current_id = 2

        while current_id <= self.n:
            valid_candidates = set()
            for p_label in list(self.label_to_id.keys()):
                if len(p_label) >= 6: 
                    continue
                for char in self.alphabet:
                    for i in range(len(p_label) + 1):
                        c_label = p_label[:i] + char + p_label[i:]
                        if c_label not in self.label_to_id:
                            parent_label, _, _ = self.rule_R(c_label)
                            if parent_label == p_label:
                                valid_candidates.add(c_label)
            
            if not valid_candidates: 
                break
                
            chosen = random.choice(list(valid_candidates))
            self.nodes[current_id] = chosen
            self.label_to_id[chosen] = current_id
            current_id += 1

        self.n = len(self.nodes)

        longer_nodes = [k for k in self.nodes if k != 1 and len(self.nodes[k]) >= 2]
        if longer_nodes:
            self.target_id = random.choice(longer_nodes)
        else:
            self.target_id = random.choice(list(self.nodes.keys())[1:])
        self.target_label = self.nodes[self.target_id]
        
        nodes_info = "\n".join([f"ID: {k}, Sequence: '{v}'" for k, v in self.nodes.items()])
        self._game_info = {
            "n": self.n,
            "alphabet": "".join(self.alphabet),
            "nodes_info": nodes_info,
            "target_id": self.target_id,
            "target_label": self.target_label,
            "inspect_limit": self.inspect_limit,
            "max_queries": self.max_queries
        }

        self.query_count = 0
        self.inspect_count = 0
        self.valid_queries = 0

    def evaluate(self, parsed_info):
        if self.valid_queries < 3:
            raise ValueError(
                "至少需要完成3次有效查询才能提交答案。" 
                if self.config.language == "zh" 
                else "At least 3 valid queries must be completed before submitting an answer."
            )
        
        ans_str = parsed_info.get("answer", "")
        ans_id_match = re.search(r"parent_id=(\d+)", ans_str)
        ans_label_match = re.search(r"parent_label=([A-Z]*)", ans_str)
        
        if not ans_id_match and not ans_label_match:
            return False
            
        correct_p_label, _, _ = self.rule_R(self.target_label)
        correct_p_id = self.label_to_id[correct_p_label]
        
        if ans_id_match and int(ans_id_match.group(1)) != correct_p_id:
            return False
        if ans_label_match and ans_label_match.group(1) != correct_p_label:
            return False
            
        return True

    def _cf_core_produce(self, parsed_info):
        is_zh = (self.config.language == "zh")

        if self.query_count >= self.max_queries:
            if is_zh:
                return "达到最大查询次数限制，请直接提交你的最终答案。"
            else:
                return "Max queries reached. Please submit your final answer now."

        if "query_inspect" in parsed_info:
            try:
                q_id = int(parsed_info["query_inspect"])
            except ValueError:
                return "Invalid ID."
            if q_id == self.target_id:
                return "不能直接查询目标。" if is_zh else "Cannot query the target."
            if q_id not in self.nodes:
                return "ID不存在。" if is_zh else "ID does not exist."
            if self.nodes[q_id] == "":
                self.query_count += 1
                self.valid_queries += 1
                return "该节点是源头节点，没有上游。" if is_zh else "This is the root node, it has no parent."
            if self.inspect_count >= self.inspect_limit:
                return "完整查询次数已用尽。" if is_zh else "Inspect limit reached."
            
            self.inspect_count += 1
            self.query_count += 1
            self.valid_queries += 1
            
            child_label = self.nodes[q_id]
            p_label, _, _ = self.rule_R(child_label)
            p_id = self.label_to_id[p_label]
            return f"parent_id={p_id}, parent_label={p_label}"

        elif "query_verify" in parsed_info:
            try:
                parts = parsed_info["query_verify"].split(",", 1)
                q_id_str = parts[0].strip()
                q_id = int(q_id_str)
                q_label = parts[1].strip() if len(parts) > 1 else ""
            except (ValueError, IndexError):
                return "Format error."
            if q_id == self.target_id:
                return "不能直接查询目标。" if is_zh else "Cannot query the target."
            if q_id not in self.nodes:
                return "ID不存在。" if is_zh else "ID does not exist."
            if self.nodes[q_id] == "":
                self.query_count += 1
                self.valid_queries += 1
                return "该节点是源头节点，没有上游。" if is_zh else "This is the root node, it has no parent."
            
            self.query_count += 1
            self.valid_queries += 1
            child_label = self.nodes[q_id]
            p_label, _, _ = self.rule_R(child_label)
            if is_zh:
                return "是" if p_label == q_label else "否"
            else:
                return "Yes" if p_label == q_label else "No"

        elif "query_position" in parsed_info:
            try:
                q_id = int(parsed_info["query_position"])
            except ValueError:
                return "Invalid ID."
            if q_id == self.target_id:
                return "不能直接查询目标。" if is_zh else "Cannot query the target."
            if q_id not in self.nodes:
                return "ID不存在。" if is_zh else "ID does not exist."
            if self.nodes[q_id] == "":
                self.query_count += 1
                self.valid_queries += 1
                return "该节点是源头节点，没有上游。" if is_zh else "This is the root node, it has no parent."
            
            self.query_count += 1
            self.valid_queries += 1
            child_label = self.nodes[q_id]
            _, idx, _ = self.rule_R(child_label)
            return str(idx + 1)

        elif "query_symbol" in parsed_info:
            try:
                q_id = int(parsed_info["query_symbol"])
            except ValueError:
                return "Invalid ID."
            if q_id == self.target_id:
                return "不能直接查询目标。" if is_zh else "Cannot query the target."
            if q_id not in self.nodes:
                return "ID不存在。" if is_zh else "ID does not exist."
            if self.nodes[q_id] == "":
                self.query_count += 1
                self.valid_queries += 1
                return "该节点是源头节点，没有上游。" if is_zh else "This is the root node, it has no parent."
            
            self.query_count += 1
            self.valid_queries += 1
            child_label = self.nodes[q_id]
            _, _, char = self.rule_R(child_label)
            return char

        return "Unknown query."

    def get_all_possible_queries(self):
        results = []
        for node_id, label in self.nodes.items():
            if node_id == self.target_id:
                continue
            if label == "":
                continue
            p_label, idx, char = self.rule_R(label)
            p_id = self.label_to_id[p_label]
            
            results.append({
                "query": f"<query_inspect>{node_id}</query_inspect>",
                "answer": f"parent_id={p_id}, parent_label={p_label}"
            })
            results.append({
                "query": f"<query_position>{node_id}</query_position>",
                "answer": str(idx + 1)
            })
            results.append({
                "query": f"<query_symbol>{node_id}</query_symbol>",
                "answer": char
            })
        return results

    def _cf_make_wrong(self, correct):
        return correct + " (False)"