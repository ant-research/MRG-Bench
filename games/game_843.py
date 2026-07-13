# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   节点属性：某给定节点的属性值是什么
# ============================================================

from .base import Game
import random
import re


class TreePropagationGame(Game):

    game_rule_zh = """\
我们来玩一个"树传播推理"游戏，规则如下：

游戏设定了一棵有根树，包含 {n} 个节点，每个节点有唯一的ID编号。树的边从父节点指向子节点，每条边带有一个标签（0到9之间的数字）。每个节点有一个属性值（0到9之间的数字）。

关键规则：
1. 存在一个统一且稳定的传播函数 f，使得任一子节点的属性值仅由其父节点的属性值与连接该子节点的边标签决定。
2. 根节点的属性值是固定但未知的。
3. 传播函数在整棵树中保持一致，但具体形式未知。
4. 目标节点ID为 {target_id}，你需要推断出该节点的属性值。

树的结构信息：
{tree_structure}

你的目标是通过尽可能少的操作次数，推断出目标节点 {target_id} 的属性值。

## 可用操作（每次仅限一个操作）

你可以使用以下三种操作：

1. **倾听操作**：查询某个节点（目标节点除外）的属性值
   格式：<listen>节点ID</listen>
   返回：该节点的属性值（0到9之间的数字）

2. **嫁接操作**：在某个节点下新增一个叶子节点，并指定连接边的标签
   格式：<graft>父节点ID,边标签</graft>
   返回：新节点的ID和属性值

3. **提交答案**：当你准备好后，提交目标节点的属性值
   格式：<answer>数字</answer>
   返回：正确或错误

## 注意事项

- 不能对目标节点 {target_id} 使用倾听操作
- 边标签必须是0到9之间的整数
- 嫁接操作会永久添加新节点到树中
- 答案必须是0到9之间的整数
- 答案提交后游戏结束

请开始你的推理！
"""

    game_rule_en = """\
Let's play a "Tree Propagation Deduction" game. Here are the rules:

The game defines a rooted tree with {n} nodes, each with a unique ID. Tree edges point from parent to child, and each edge has a label (a digit from 0 to 9). Each node has an attribute value (a digit from 0 to 9).

Key Rules:
1. There exists a unified and stable propagation function f, such that any child node's attribute is determined solely by its parent's attribute and the edge label connecting to the child.
2. The root node's attribute is fixed but unknown.
3. The propagation function remains consistent throughout the tree, but its specific form is unknown.
4. The target node ID is {target_id}, and you need to deduce its attribute value.

Tree Structure Information:
{tree_structure}

Your goal is to deduce the attribute value of target node {target_id} using as few operations as possible.

## Available Operations (one per turn)

You can use the following three operations:

1. **Listen Operation**: Query the attribute value of a node (except the target node)
   Format: <listen>nodeID</listen>
   Returns: The node's attribute value (a digit from 0 to 9)

2. **Graft Operation**: Add a new leaf node under a specified node with a given edge label
   Format: <graft>parentID,edgeLabel</graft>
   Returns: The new node's ID and attribute value

3. **Submit Answer**: When ready, submit the target node's attribute value
   Format: <answer>digit</answer>
   Returns: Correct or incorrect

## Important Notes

- You cannot use Listen operation on target node {target_id}
- Edge labels must be integers from 0 to 9
- Graft operations permanently add new nodes to the tree
- Answer must be an integer from 0 to 9
- Game ends after answer submission

Start your deduction!
"""

    # 场景 1：交通
    contextualized_rule_zh_1 = """\
我们来协助进行"路网拥堵态势预测"，规则如下：

系统设定了一个包含 {n} 个关键路口（节点）的有向树状快速路网，每个路口有唯一的ID编号。车流从上游路口流向下游路口（父节点到子节点），每条连接路段带有一个道路特征码（0到9之间的数字）。每个路口具有一个实时的拥堵指数（0到9之间的数字）。

关键规则：
1. 存在一个统一且稳定的拥堵传导函数 f，使得任一下游路口的拥堵指数仅由其直接上游路口的拥堵指数与连接两者的道路特征码决定。
2. 源头路口（根节点）的拥堵指数固定但未知。
3. 拥堵传导函数在整个路网中保持一致，但具体公式未知。
4. 目标路口ID为 {target_id}，你需要推断出该路口的拥堵指数。

路网结构信息：
{tree_structure}

你的目标是通过尽可能少的调度操作，推断出目标路口 {target_id} 的拥堵指数。

## 可用操作（每次仅限一个操作）

你可以使用以下三种操作：

1. **监测操作**：调用摄像头查询某个路口（目标路口除外）的拥堵指数
   格式：<listen>路口ID</listen>
   返回：该路口的拥堵指数（注：系统返回文本中统称为"节点"和"属性值"）

2. **仿真操作**：在某个路口下游通过沙盘虚拟增加一个测试路口，并指定相连路段的道路特征码
   格式：<graft>父路口ID,道路特征码</graft>
   返回：新路口的ID和拥堵指数（注：系统返回文本中统称为"节点"和"属性值"）

3. **提交报告**：当你准备好后，提交目标路口的拥堵指数预测值
   格式：<answer>数字</answer>
   返回：正确或错误

## 注意事项

- 不能对目标路口 {target_id} 使用监测操作
- 道路特征码必须是0到9之间的整数
- 仿真操作会永久将新路口加入虚拟路网中
- 答案必须是0到9之间的整数
- 答案提交后评估结束

请开始你的分析！
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's assist in "Traffic Congestion Trend Prediction". Here are the rules:

The system defines a directed tree-like expressway network containing {n} key intersections (nodes), each with a unique ID. Traffic flows from upstream to downstream (parent to child), and each connecting road segment has a road characteristic code (a digit from 0 to 9). Each intersection has a real-time congestion index (a digit from 0 to 9).

Key Rules:
1. There exists a unified and stable congestion propagation function f, such that any downstream intersection's congestion index is determined solely by its direct upstream intersection's index and the connecting road's characteristic code.
2. The source intersection (root node) has a fixed but unknown congestion index.
3. The propagation function remains consistent throughout the network, but its specific formula is unknown.
4. The target intersection ID is {target_id}, and you need to deduce its congestion index.

Network Structure Information:
{tree_structure}

Your goal is to deduce the congestion index of target intersection {target_id} using as few dispatch operations as possible.

## Available Operations (one per turn)

You can use the following three operations:

1. **Monitor Operation**: Use traffic cameras to query the congestion index of an intersection (except the target)
   Format: <listen>intersectionID</listen>
   Returns: The intersection's congestion index (Note: The system returns will use the generic terms "Node" and "Attribute value")

2. **Simulate Operation**: Virtually add a test intersection downstream of an existing one in the simulator, specifying the connecting road's characteristic code
   Format: <graft>parentIntersectionID,roadCharacteristicCode</graft>
   Returns: The new intersection's ID and congestion index (Note: The system returns will use the generic terms "Node" and "Attribute value")

3. **Submit Report**: When ready, submit the predicted congestion index for the target intersection
   Format: <answer>digit</answer>
   Returns: Correct or incorrect

## Important Notes

- You cannot use Monitor operation on target intersection {target_id}
- Road characteristic codes must be integers from 0 to 9
- Simulate operations permanently add new intersections to the virtual network
- Answer must be an integer from 0 to 9
- Evaluation ends after answer submission

Start your analysis!
"""

    # 场景 2：医疗
    contextualized_rule_zh_2 = """\
我们来协助进行"病毒变异溯源分析"，规则如下：

系统记录了一棵包含 {n} 名感染者（节点）的传播链树，每个感染者有唯一的病例编号。传播方向由传染源指向被感染者（父节点到子节点），每次传播事件带有一个接触途径代码（0到9之间的数字）。每个病例体内提取的病毒株具有一个变异强度等级（0到9之间的数字）。

关键规则：
1. 存在一个统一且稳定的突变演化函数 f，使得任一被感染者的变异强度等级仅由其传染源的变异等级与两者间的接触途径代码决定。
2. 零号病人（根节点）的变异强度等级固定但未知。
3. 突变演化函数在整个传播链中保持一致，但具体机制未知。
4. 目标病例编号为 {target_id}，你需要推断出该病例的变异强度等级。

传播链结构信息：
{tree_structure}

你的目标是通过尽可能少的临床操作，推断出目标病例 {target_id} 的变异强度等级。

## 可用操作（每次仅限一个操作）

你可以使用以下三种操作：

1. **测序操作**：对某个病例（目标病例除外）提取样本查询其变异强度等级
   格式：<listen>病例编号</listen>
   返回：该病例的变异强度等级（注：系统返回文本中统称为"节点"和"属性值"）

2. **培养操作**：在实验室中利用某病例的毒株感染一个新的细胞系模型，并设定特定的接触途径代码
   格式：<graft>父病例编号,接触途径代码</graft>
   返回：新模型编号和变异强度等级（注：系统返回文本中统称为"节点"和"属性值"）

3. **提交结论**：当你准备好后，提交目标病例的变异强度等级
   格式：<answer>数字</answer>
   返回：正确或错误

## 注意事项

- 不能对目标病例 {target_id} 使用测序操作
- 接触途径代码必须是0到9之间的整数
- 培养操作会永久将新模型加入演化树中
- 答案必须是0到9之间的整数
- 答案提交后分析结束

请开始你的溯源！
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's assist in "Viral Mutation Traceback Analysis". Here are the rules:

The system has recorded a transmission chain tree containing {n} infected individuals (nodes), each with a unique case ID. Transmission flows from infector to infectee (parent to child), and each transmission event has a contact pathway code (a digit from 0 to 9). The viral strain extracted from each case has a mutation severity level (a digit from 0 to 9).

Key Rules:
1. There exists a unified and stable mutation evolution function f, such that any infectee's mutation severity level is determined solely by their infector's severity level and the contact pathway code between them.
2. Patient Zero's (root node) mutation severity level is fixed but unknown.
3. The mutation evolution function remains consistent throughout the chain, but its specific mechanism is unknown.
4. The target case ID is {target_id}, and you need to deduce its mutation severity level.

Transmission Chain Structure Information:
{tree_structure}

Your goal is to deduce the mutation severity level of target case {target_id} using as few clinical operations as possible.

## Available Operations (one per turn)

You can use the following three operations:

1. **Sequence Operation**: Extract a sample from a case (except the target) to query its mutation severity level
   Format: <listen>caseID</listen>
   Returns: The case's mutation severity level (Note: The system returns will use the generic terms "Node" and "Attribute value")

2. **Culture Operation**: Infect a new cell line model in the lab using a specific case's strain, setting a specific contact pathway code
   Format: <graft>parentCaseID,contactPathwayCode</graft>
   Returns: The new model's ID and mutation severity level (Note: The system returns will use the generic terms "Node" and "Attribute value")

3. **Submit Conclusion**: When ready, submit the predicted mutation severity level for the target case
   Format: <answer>digit</answer>
   Returns: Correct or incorrect

## Important Notes

- You cannot use Sequence operation on target case {target_id}
- Contact pathway codes must be integers from 0 to 9
- Culture operations permanently add new models to the evolution tree
- Answer must be an integer from 0 to 9
- Analysis ends after answer submission

Start your traceback!
"""

    # 场景 3：教育
    contextualized_rule_zh_3 = """\
我们来进行"认知难点传导分析"，规则如下：

教研系统生成了一棵包含 {n} 个知识点（节点）的先决条件依赖树，每个知识点有唯一的ID编号。学习路径从前置知识点指向后置知识点（父节点到子节点），每条学习路径带有一个教学策略码（0到9之间的数字）。每个知识点具有一个评估出的学习障碍指数（0到9之间的数字）。

关键规则：
1. 存在一个统一且稳定的认知负荷传导函数 f，使得任一后置知识点的学习障碍指数仅由其直接前置知识点的障碍指数与连接两者的教学策略码决定。
2. 基础知识点（根节点）的学习障碍指数固定但未知。
3. 传导函数在整个依赖树中保持一致，但具体形式未知。
4. 目标知识点ID为 {target_id}，你需要推断出该知识点的学习障碍指数。

知识依赖树结构信息：
{tree_structure}

你的目标是通过尽可能少的测评操作，推断出目标知识点 {target_id} 的学习障碍指数。

## 可用操作（每次仅限一个操作）

你可以使用以下三种操作：

1. **测评操作**：对某个知识点（目标知识点除外）进行学情摸底，查询其学习障碍指数
   格式：<listen>知识点ID</listen>
   返回：该知识点的学习障碍指数（注：系统返回文本中统称为"节点"和"属性值"）

2. **教研操作**：在某个知识点后置虚拟新增一个衍生教学模块，并指定应用的教学策略码
   格式：<graft>父知识点ID,教学策略码</graft>
   返回：新模块ID和学习障碍指数（注：系统返回文本中统称为"节点"和"属性值"）

3. **提交评估**：当你准备好后，提交目标知识点的学习障碍指数预测值
   格式：<answer>数字</answer>
   返回：正确或错误

## 注意事项

- 不能对目标知识点 {target_id} 使用测评操作
- 教学策略码必须是0到9之间的整数
- 教研操作会永久将新模块加入依赖树中
- 答案必须是0到9之间的整数
- 答案提交后分析结束

请开始你的教研分析！
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct "Cognitive Difficulty Propagation Analysis". Here are the rules:

The educational system generated a prerequisite dependency tree containing {n} knowledge concepts (nodes), each with a unique ID. Learning paths point from prerequisite concepts to advanced concepts (parent to child), and each path has an instructional strategy code (a digit from 0 to 9). Each concept has an assessed learning obstacle index (a digit from 0 to 9).

Key Rules:
1. There exists a unified and stable cognitive load propagation function f, such that any advanced concept's learning obstacle index is determined solely by its direct prerequisite's index and the instructional strategy code connecting them.
2. The foundational concept's (root node) learning obstacle index is fixed but unknown.
3. The propagation function remains consistent throughout the tree, but its specific form is unknown.
4. The target concept ID is {target_id}, and you need to deduce its learning obstacle index.

Dependency Tree Structure Information:
{tree_structure}

Your goal is to deduce the learning obstacle index of target concept {target_id} using as few assessment operations as possible.

## Available Operations (one per turn)

You can use the following three operations:

1. **Assess Operation**: Conduct a diagnostic assessment on a concept (except the target) to query its learning obstacle index
   Format: <listen>conceptID</listen>
   Returns: The concept's learning obstacle index (Note: The system returns will use the generic terms "Node" and "Attribute value")

2. **Design Operation**: Virtually add a derived learning module after a concept, specifying the applied instructional strategy code
   Format: <graft>parentConceptID,strategyCode</graft>
   Returns: The new module's ID and learning obstacle index (Note: The system returns will use the generic terms "Node" and "Attribute value")

3. **Submit Evaluation**: When ready, submit the predicted learning obstacle index for the target concept
   Format: <answer>digit</answer>
   Returns: Correct or incorrect

## Important Notes

- You cannot use Assess operation on target concept {target_id}
- Instructional strategy codes must be integers from 0 to 9
- Design operations permanently add new modules to the dependency tree
- Answer must be an integer from 0 to 9
- Analysis ends after answer submission

Start your instructional analysis!
"""

    # 场景 4：制造业/工业
    contextualized_rule_zh_4 = """\
我们来进行"装配线缺陷率传导诊断"，规则如下：

工厂质检系统监控着一棵包含 {n} 个工序（节点）的装配依赖树，每个工序有唯一的ID编号。物料从上游工序流向下游工序（父节点到子节点），每次流转加工带有一个工艺参数码（0到9之间的数字）。每个加工阶段的半成品具有一个品控缺陷等级（0到9之间的数字）。

关键规则：
1. 存在一个统一且稳定的缺陷传导函数 f，使得任一下游工序的缺陷等级仅由其直接上游工序的缺陷等级与加工流转时的工艺参数码决定。
2. 原材料供给（根节点）的缺陷等级固定但未知。
3. 缺陷传导函数在整个装配线中保持一致，但具体数学模型未知。
4. 目标工序ID为 {target_id}，你需要推断出该工序的缺陷等级。

装配线结构信息：
{tree_structure}

你的目标是通过尽可能少的检验操作，推断出目标工序 {target_id} 的缺陷等级。

## 可用操作（每次仅限一个操作）

你可以使用以下三种操作：

1. **抽检操作**：在某个工序（目标工序除外）拦截半成品并查询其缺陷等级
   格式：<listen>工序ID</listen>
   返回：该工序的缺陷等级（注：系统返回文本中统称为"节点"和"属性值"）

2. **试产操作**：在某个工序后接入一条原型测试支线，并指定应用的工艺参数码
   格式：<graft>父工序ID,工艺参数码</graft>
   返回：新支线末端的工序ID和缺陷等级（注：系统返回文本中统称为"节点"和"属性值"）

3. **提交排查**：当你准备好后，提交目标工序的缺陷等级预测值
   格式：<answer>数字</answer>
   返回：正确或错误

## 注意事项

- 不能对目标工序 {target_id} 使用抽检操作
- 工艺参数码必须是0到9之间的整数
- 试产操作会永久将新工序加入装配树中
- 答案必须是0到9之间的整数
- 答案提交后诊断结束

请开始你的质检诊断！
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's conduct "Assembly Line Defect Rate Propagation Diagnostics". Here are the rules:

The factory QA system monitors an assembly dependency tree containing {n} workstations (nodes), each with a unique ID. Materials flow from upstream to downstream workstations (parent to child), and each processing transition has a process parameter code (a digit from 0 to 9). The work-in-progress at each stage has a quality control defect level (a digit from 0 to 9).

Key Rules:
1. There exists a unified and stable defect propagation function f, such that any downstream workstation's defect level is determined solely by its direct upstream workstation's defect level and the transition's process parameter code.
2. The raw material supply's (root node) defect level is fixed but unknown.
3. The defect propagation function remains consistent throughout the assembly line, but its specific mathematical model is unknown.
4. The target workstation ID is {target_id}, and you need to deduce its defect level.

Assembly Line Structure Information:
{tree_structure}

Your goal is to deduce the defect level of target workstation {target_id} using as few inspection operations as possible.

## Available Operations (one per turn)

You can use the following three operations:

1. **Inspect Operation**: Intercept work-in-progress at a workstation (except the target) to query its defect level
   Format: <listen>workstationID</listen>
   Returns: The workstation's defect level (Note: The system returns will use the generic terms "Node" and "Attribute value")

2. **Prototype Operation**: Connect a prototype testing branch after a workstation, specifying the applied process parameter code
   Format: <graft>parentWorkstationID,parameterCode</graft>
   Returns: The new branch's workstation ID and defect level (Note: The system returns will use the generic terms "Node" and "Attribute value")

3. **Submit Audit**: When ready, submit the predicted defect level for the target workstation
   Format: <answer>digit</answer>
   Returns: Correct or incorrect

## Important Notes

- You cannot use Inspect operation on target workstation {target_id}
- Process parameter codes must be integers from 0 to 9
- Prototype operations permanently add new workstations to the assembly tree
- Answer must be an integer from 0 to 9
- Diagnostics ends after answer submission

Start your quality audit!
"""

    # 场景 5：法律
    contextualized_rule_zh_5 = """\
我们来进行"证据链采信度推演"，规则如下：

法务系统梳理出了一棵包含 {n} 个关键证据节点（节点）的证据派生树，每个证据有唯一的卷宗编号。证据衍生方向由基础证据指向派生证据（父节点到子节点），每次派生推导带有一个法理逻辑码（0到9之间的数字）。每个证据节点具有一个法庭采信权重（0到9之间的数字）。

关键规则：
1. 存在一个统一且稳定的证明力传导函数 f，使得任一派生证据的采信权重仅由其直接基础证据的采信权重与派生时的法理逻辑码决定。
2. 初始物证（根节点）的采信权重固定但未知。
3. 证明力传导函数在整条证据链中保持一致，但具体裁判倾向未知。
4. 目标证据编号为 {target_id}，你需要推断出该证据的采信权重。

证据链结构信息：
{tree_structure}

你的目标是通过尽可能少的质证操作，推断出目标证据 {target_id} 的采信权重。

## 可用操作（每次仅限一个操作）

你可以使用以下三种操作：

1. **查阅操作**：向法庭申请调取某个证据（目标证据除外）以查询其采信权重
   格式：<listen>卷宗编号</listen>
   返回：该证据的采信权重（注：系统返回文本中统称为"节点"和"属性值"）

2. **推演操作**：在模拟法庭中基于某证据提出一个假设性派生证据，并指定对应的法理逻辑码
   格式：<graft>父卷宗编号,法理逻辑码</graft>
   返回：新证据编号和采信权重（注：系统返回文本中统称为"节点"和"属性值"）

3. **提交诉状**：当你准备好后，提交目标证据的预测采信权重
   格式：<answer>数字</answer>
   返回：正确或错误

## 注意事项

- 不能对目标证据 {target_id} 使用查阅操作
- 法理逻辑码必须是0到9之间的整数
- 推演操作会永久将新假设证据加入派生树中
- 答案必须是0到9之间的整数
- 答案提交后推演结束

请开始你的法理质证！
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct a "Chain of Evidence Credibility Deduction". Here are the rules:

The legal system has structured an evidence derivation tree containing {n} key evidence items (nodes), each with a unique dossier ID. Derivation flows from foundational evidence to derived evidence (parent to child), and each logical deduction has a jurisprudential logic code (a digit from 0 to 9). Each evidence node carries a court credibility weight (a digit from 0 to 9).

Key Rules:
1. There exists a unified and stable probative value propagation function f, such that any derived evidence's credibility weight is determined solely by its direct foundational evidence's weight and the applied jurisprudential logic code.
2. The initial physical evidence's (root node) credibility weight is fixed but unknown.
3. The probative value propagation function remains consistent throughout the evidence chain, but the specific judicial tendency is unknown.
4. The target evidence ID is {target_id}, and you need to deduce its credibility weight.

Evidence Chain Structure Information:
{tree_structure}

Your goal is to deduce the credibility weight of target evidence {target_id} using as few cross-examination operations as possible.

## Available Operations (one per turn)

You can use the following three operations:

1. **Review Operation**: Motion the court to retrieve a specific piece of evidence (except the target) to query its credibility weight
   Format: <listen>dossierID</listen>
   Returns: The evidence's credibility weight (Note: The system returns will use the generic terms "Node" and "Attribute value")

2. **Moot Operation**: Introduce a hypothetical derived evidence based on an existing one in moot court, specifying the jurisprudential logic code
   Format: <graft>parentDossierID,logicCode</graft>
   Returns: The new evidence ID and credibility weight (Note: The system returns will use the generic terms "Node" and "Attribute value")

3. **Submit Pleading**: When ready, submit the predicted credibility weight for the target evidence
   Format: <answer>digit</answer>
   Returns: Correct or incorrect

## Important Notes

- You cannot use Review operation on target evidence {target_id}
- Jurisprudential logic codes must be integers from 0 to 9
- Moot operations permanently add new hypothetical evidence to the derivation tree
- Answer must be an integer from 0 to 9
- Deduction ends after answer submission

Start your legal cross-examination!
"""

    tags = ["answer", "listen", "graft"]
    
    # 新增类属性
    reasoning_type = "归纳推理"
    data_structure = "树"

    # 难度配置：
    # 1 (简单)       - 小树，浅层目标，简单参数
    # 2 (中等偏下)   - 中等树，中层目标
    # 3 (中等偏上)   - 中等树，较深目标
    # 4 (较难)       - 较大树，深层目标，复杂参数
    # 5 (难)         - 大树，深层目标，复杂参数

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "edges": [
                    (1, 2, 3),  # 父节点, 子节点, 边标签
                    (1, 3, 5),
                    (2, 4, 2)
                ],
                "root": 1,
                "target": 4,
                "a": 2, "b": 1, "c": 0, "root_value": 3
            },
            2: {
                "n": 7,
                "edges": [
                    (1, 2, 1),
                    (1, 3, 2),
                    (2, 4, 3),
                    (2, 5, 4),
                    (3, 6, 5),
                    (3, 7, 6)
                ],
                "root": 1,
                "target": 5,
                "a": 3, "b": 2, "c": 1, "root_value": 2
            },
            3: {
                "n": 10,
                "edges": [
                    (1, 2, 2),
                    (1, 3, 3),
                    (2, 4, 1),
                    (2, 5, 4),
                    (3, 6, 2),
                    (3, 7, 5),
                    (4, 8, 3),
                    (5, 9, 6),
                    (6, 10, 7)
                ],
                "root": 1,
                "target": 9,
                "a": 4, "b": 3, "c": 2, "root_value": 1
            },
            4: {
                "n": 12,
                "edges": [
                    (1, 2, 1),
                    (1, 3, 2),
                    (2, 4, 3),
                    (2, 5, 4),
                    (3, 6, 5),
                    (3, 7, 6),
                    (4, 8, 7),
                    (5, 9, 8),
                    (6, 10, 9),
                    (7, 11, 1),
                    (8, 12, 2)
                ],
                "root": 1,
                "target": 12,
                "a": 7, "b": 5, "c": 3, "root_value": 4
            },
            5: {
                "n": 15,
                "edges": [
                    (1, 2, 2),
                    (1, 3, 3),
                    (1, 4, 4),
                    (2, 5, 1),
                    (2, 6, 5),
                    (3, 7, 6),
                    (3, 8, 7),
                    (4, 9, 8),
                    (4, 10, 9),
                    (5, 11, 2),
                    (6, 12, 3),
                    (7, 13, 4),
                    (8, 14, 5),
                    (9, 15, 6)
                ],
                "root": 1,
                "target": 15,
                "a": 9, "b": 7, "c": 6, "root_value": 5
            }
        },
        "en": {
            1: {
                "n": 4,
                "edges": [
                    (1, 2, 3),
                    (1, 3, 5),
                    (2, 4, 2)
                ],
                "root": 1,
                "target": 4,
                "a": 2, "b": 1, "c": 0, "root_value": 3
            },
            2: {
                "n": 7,
                "edges": [
                    (1, 2, 1),
                    (1, 3, 2),
                    (2, 4, 3),
                    (2, 5, 4),
                    (3, 6, 5),
                    (3, 7, 6)
                ],
                "root": 1,
                "target": 5,
                "a": 3, "b": 2, "c": 1, "root_value": 2
            },
            3: {
                "n": 10,
                "edges": [
                    (1, 2, 2),
                    (1, 3, 3),
                    (2, 4, 1),
                    (2, 5, 4),
                    (3, 6, 2),
                    (3, 7, 5),
                    (4, 8, 3),
                    (5, 9, 6),
                    (6, 10, 7)
                ],
                "root": 1,
                "target": 9,
                "a": 4, "b": 3, "c": 2, "root_value": 1
            },
            4: {
                "n": 12,
                "edges": [
                    (1, 2, 1),
                    (1, 3, 2),
                    (2, 4, 3),
                    (2, 5, 4),
                    (3, 6, 5),
                    (3, 7, 6),
                    (4, 8, 7),
                    (5, 9, 8),
                    (6, 10, 9),
                    (7, 11, 1),
                    (8, 12, 2)
                ],
                "root": 1,
                "target": 12,
                "a": 7, "b": 5, "c": 3, "root_value": 4
            },
            5: {
                "n": 15,
                "edges": [
                    (1, 2, 2),
                    (1, 3, 3),
                    (1, 4, 4),
                    (2, 5, 1),
                    (2, 6, 5),
                    (3, 7, 6),
                    (3, 8, 7),
                    (4, 9, 8),
                    (4, 10, 9),
                    (5, 11, 2),
                    (6, 12, 3),
                    (7, 13, 4),
                    (8, 14, 5),
                    (9, 15, 6)
                ],
                "root": 1,
                "target": 15,
                "a": 9, "b": 7, "c": 6, "root_value": 5
            }
        }
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 初始化树结构
        self.n = cfg["n"]
        self.edges = cfg["edges"]  # [(parent, child, label), ...]
        self.root = cfg["root"]
        self.target = cfg["target"]
        
        # 传播函数参数 (对玩家隐藏)
        self.a = cfg["a"]
        self.b = cfg["b"]
        self.c = cfg["c"]
        self.root_value = cfg["root_value"]
        
        # 构建树结构：children[parent] = [(child, label), ...]
        self.children = {}
        self.parent_map = {}  # child -> (parent, label)
        for parent, child, label in self.edges:
            if parent not in self.children:
                self.children[parent] = []
            self.children[parent].append((child, label))
            self.parent_map[child] = (parent, label)
        
        # 计算所有节点的属性值
        self.node_values = {}
        self._compute_values(self.root, self.root_value)
        
        # 存储真实答案
        self.true_answer = self.node_values[self.target]
        
        # 构建树结构的文本描述
        tree_desc = self._build_tree_description()
        
        # 设置游戏信息
        self._game_info["n"] = self.n
        self._game_info["target_id"] = self.target
        self._game_info["tree_structure"] = tree_desc
        
        # 用于嫁接的新节点ID计数器
        self.next_node_id = self.n + 1

    def _compute_values(self, node, value):
        """递归计算树中所有节点的属性值"""
        self.node_values[node] = value
        if node in self.children:
            for child, label in self.children[node]:
                # 传播函数: child_value = (a * parent_value + b * edge_label + c) mod 10
                child_value = (self.a * value + self.b * label + self.c) % 10
                self._compute_values(child, child_value)

    def _build_tree_description(self):
        """构建树结构的文本描述"""
        if self.config.language == "zh":
            lines = [f"根节点: {self.root}", "边列表 (父节点 -> 子节点 [边标签]):"]
            for parent, child, label in self.edges:
                lines.append(f"  {parent} -> {child} [标签={label}]")
        else:
            lines = [f"Root node: {self.root}", "Edge list (parent -> child [edge label]):"]
            for parent, child, label in self.edges:
                lines.append(f"  {parent} -> {child} [label={label}]")
        return "\n".join(lines)

    def evaluate(self, parsed_info):
        """评估答案是否正确"""
        try:
            answer = int(parsed_info["answer"].strip())
            if answer < 0 or answer > 9:
                return False
            return answer == self.true_answer
        except (ValueError, KeyError, AttributeError):
            return False

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑"""
        is_zh = self.config.language == "zh"
        
        # 处理倾听操作
        if "listen" in parsed_info:
            try:
                node_id = int(parsed_info["listen"].strip())
                
                # 检查是否为目标节点
                if node_id == self.target:
                    return "错误：不能查询目标节点的属性值。" if is_zh else "Error: Cannot query the target node's attribute."
                
                # 检查节点是否存在
                if node_id not in self.node_values:
                    return "错误：节点不存在。" if is_zh else "Error: Node does not exist."
                
                value = self.node_values[node_id]
                return f"节点 {node_id} 的属性值为: {value}" if is_zh else f"Node {node_id} attribute value: {value}"
            except (ValueError, TypeError, AttributeError):
                return "错误：无效的节点ID格式。" if is_zh else "Error: Invalid node ID format."
        
        # 处理嫁接操作
        elif "graft" in parsed_info:
            try:
                parts = parsed_info["graft"].strip().split(",")
                if len(parts) != 2:
                    raise ValueError("Expected exactly 2 comma-separated values")
                
                parent_id = int(parts[0].strip())
                edge_label = int(parts[1].strip())
                
                # 检查父节点是否存在
                if parent_id not in self.node_values:
                    return "错误：父节点不存在。" if is_zh else "Error: Parent node does not exist."
                
                # 检查边标签范围
                if edge_label < 0 or edge_label > 9:
                    return "错误：边标签必须在0到9之间。" if is_zh else "Error: Edge label must be between 0 and 9."
                
                # 创建新节点
                new_node_id = self.next_node_id
                self.next_node_id += 1
                
                # 计算新节点的属性值
                parent_value = self.node_values[parent_id]
                new_value = (self.a * parent_value + self.b * edge_label + self.c) % 10
                
                # 更新树结构
                if parent_id not in self.children:
                    self.children[parent_id] = []
                self.children[parent_id].append((new_node_id, edge_label))
                self.parent_map[new_node_id] = (parent_id, edge_label)
                self.node_values[new_node_id] = new_value
                
                if is_zh:
                    return f"新节点已创建。节点ID: {new_node_id}, 属性值: {new_value}"
                else:
                    return f"New node created. Node ID: {new_node_id}, Attribute value: {new_value}"
            except (ValueError, TypeError, AttributeError):
                return "错误：无效的嫁接操作格式。格式应为: 父节点ID,边标签" if is_zh else "Error: Invalid graft format. Format should be: parentID,edgeLabel"
        
        else:
            raise ValueError("No valid operation tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法的无副作用查询并返回对应的正确答案。
        仅枚举 listen 操作，因为 graft 操作会修改游戏状态。
        """
        possible_queries = []
        is_zh = self.config.language == "zh"
        
        # 获取当前所有存在的节点ID并排序
        existing_nodes = sorted(self.node_values.keys())
        
        # 枚举所有倾听操作 (Listen)
        for node_id in existing_nodes:
            if node_id == self.target:
                continue
            
            query = f"<listen>{node_id}</listen>"
            value = self.node_values[node_id]
            answer = f"节点 {node_id} 的属性值为: {value}" if is_zh else f"Node {node_id} attribute value: {value}"
            
            possible_queries.append({
                "query": query,
                "answer": answer
            })

        return possible_queries

    def _cf_make_wrong(self, correct):
        """生成错误答案：篡改响应中的数字属性值"""
        import re as _re
        import random
        
        is_zh = self.config.language == "zh"
        
        # 尝试匹配 listen 响应中的属性值数字
        # 中文格式: "节点 X 的属性值为: Y"
        # 英文格式: "Node X attribute value: Y"
        pattern_listen = r'(属性值为:\s*|attribute value:\s*)(\d)'
        match = _re.search(pattern_listen, correct)
        if match:
            orig_val = int(match.group(2))
            wrong_val = (orig_val + random.randint(1, 9)) % 10
            return correct[:match.start(2)] + str(wrong_val) + correct[match.end(2):]
        
        # 尝试匹配 graft 响应中的属性值数字
        # 中文格式: "新节点已创建。节点ID: X, 属性值: Y"
        # 英文格式: "New node created. Node ID: X, Attribute value: Y"
        pattern_graft = r'(属性值:\s*|Attribute value:\s*)(\d)'
        match = _re.search(pattern_graft, correct)
        if match:
            orig_val = int(match.group(2))
            wrong_val = (orig_val + random.randint(1, 9)) % 10
            return correct[:match.start(2)] + str(wrong_val) + correct[match.end(2):]
        
        # 兜底：替换最后一个数字
        matches = list(_re.finditer(r'\d', correct))
        if matches:
            last_match = matches[-1]
            orig_val = int(last_match.group())
            wrong_val = (orig_val + random.randint(1, 9)) % 10
            return correct[:last_match.start()] + str(wrong_val) + correct[last_match.end():]
        
        return correct + "_WRONG"