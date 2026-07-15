from .base import Game
import random

class LinearWeightFunctionGame(Game):
    reasoning_type = "归纳推理"
    data_structure = "图"
    
    game_rule_zh = """\
我们来玩一个"边权函数推理"游戏，规则如下：

游戏设定了一个顶点集合 V = {{0, 1, 2, ..., 10}}，共11个顶点。我已经秘密设置了一个边权函数 w，该函数为任意两个不同顶点 i 和 j 之间分配一个权重值，权重值范围是 0 到 10 的整数。

你的目标是通过尽可能少的查询来推断出这个边权函数的规律，并能对未见过的顶点对做出正确预测。

你可以进行以下操作：

1. **训练查询**（至多12次）：询问任意两个不同顶点 i 和 j 之间的边权。你需要提供顶点编号 i 和 j（均为0到10之间的整数，且 i 不等于 j）。我会返回对应的权重值。如果查询格式无效（如 i 等于 j 或越界），将返回"无效"，且不计入查询次数。

2. **进入测试阶段**：当你认为已经掌握了规律，可以宣布进入测试。我会给出5个未被查询过的顶点对，你需要预测每对的边权值。

3. **宣告规则**（可选）：你可以直接给出完整的函数规则。我会用若干未查询过的顶点对进行验证，如果全部正确则游戏胜利。

每次只能包含一个标签，使用以下 XML 格式：

- 训练查询（例如查询顶点3和7之间的边权）：
<query_train>3,7</query_train>

- 进入测试阶段：
<enter_test></enter_test>

- 测试阶段预测（例如预测顶点对 (2,5) 的边权为8）：
<predict>2,5,8</predict>

- 宣告规则（给出参数 a、b、c，表示函数为 w(i,j) = (a*i + b*j + c) mod 11）：
<declare_rule>a=3,b=5,c=2</declare_rule>

- **胜利**：测试阶段5个预测全部正确，或规则宣告验证全部通过。
- **失败**：测试阶段任一预测错误，或规则宣告验证失败，或超过12次训练查询限制。
"""

    game_rule_en = """\
Let's play a "Linear Weight Function Inference" game. Here are the rules:

The game defines a vertex set V = {{0, 1, 2, ..., 10}}, containing 11 vertices. I have secretly set up an edge weight function w that assigns a weight value to any two different vertices i and j. The weight values range from 0 to 10 (integers).

Your goal is to infer the pattern of this edge weight function through as few queries as possible, and make correct predictions on unseen vertex pairs.

You can perform the following operations:

1. **Training Query** (at most 12 times): Ask for the edge weight between any two different vertices i and j. You need to provide vertex numbers i and j (both integers from 0 to 10, and i not equal to j). I will return the corresponding weight value. If the query format is invalid (e.g., i equals j or out of bounds), "Invalid" will be returned and it won't count toward the query limit.

2. **Enter Test Phase**: When you think you have understood the pattern, you can declare to enter testing. I will give 5 vertex pairs that have not been queried, and you need to predict the edge weight for each pair.

3. **Declare Rule** (optional): You can directly give the complete function rule. I will verify it with several unqueried vertex pairs. If all are correct, you win the game.

Each time only one tag is allowed. Use the following XML format:

- Training Query (e.g., query edge weight between vertices 3 and 7):
<query_train>3,7</query_train>

- Enter Test Phase:
<enter_test></enter_test>

- Test Phase Prediction (e.g., predict edge weight of vertex pair (2,5) is 8):
<predict>2,5,8</predict>

- Declare Rule (give parameters a, b, c, representing function w(i,j) = (a*i + b*j + c) mod 11):
<declare_rule>a=3,b=5,c=2</declare_rule>

- **Victory**: All 5 predictions in test phase are correct, or rule declaration passes all verifications.
- **Failure**: Any prediction in test phase is wrong, or rule declaration verification fails, or exceeds 12 training query limit.
"""

    contextualized_rule_zh_1 = """\
我们来测试一个"物流网络运输成本分析"系统，规则如下：

我们的区域物流网络包含了由编号 0 到 10 代表的 11 个物流枢纽。系统内部使用一个隐藏的成本评估函数 w，为任意两个不同的枢纽 i 和 j 之间的单向运输路线分配一个运输成本指数，指数范围是 0 到 10 的整数。

你的目标是通过尽可能少的线路勘测来推断出这个运输成本函数的计算规律，并能对未规划过的路线做出正确的成本预测。

你可以进行以下操作：

1. **路线勘测（训练查询）**（至多12次）：指定任意两个不同的枢纽 i 和 j。你需要提供起点枢纽 i 和终点枢纽 j 的编号（均为0到10之间的整数，且 i 不等于 j）。系统会返回对应的运输成本指数。如果查询格式无效（如 i 等于 j 或越界），将返回"无效"，且不计入勘测次数。

2. **进入测试阶段**：当你认为已经掌握了成本计算规律，可以宣布进入测试。系统会给出5条未被勘测过的路线，你需要预测每条路线的成本指数。

3. **宣告规则**（可选）：你可以直接给出完整的成本计算模型。系统会用若干未勘测过的路线进行后台验证，如果全部正确则任务成功。

每次只能包含一个标签，使用以下 XML 格式：

- 路线勘测（例如勘测从枢纽3到枢纽7的路线成本）：
<query_train>3,7</query_train>

- 进入测试阶段：
<enter_test></enter_test>

- 测试阶段预测（例如预测从枢纽2到枢纽5的成本指数为8）：
<predict>2,5,8</predict>

- 宣告规则（给出参数 a、b、c，表示成本模型为 w(i,j) = (a*i + b*j + c) mod 11）：
<declare_rule>a=3,b=5,c=2</declare_rule>

- **胜利**：测试阶段5个预测全部正确，或规则宣告验证全部通过。
- **失败**：测试阶段任一预测错误，或规则宣告验证失败，或超过12次勘测查询限制。
"""

    contextualized_rule_en_1 = """\
[Traffic/Logistics Scenario]
Let's test a "Logistics Network Transport Cost Analysis" system. Here are the rules:

Our regional logistics network contains 11 hubs represented by numbers 0 to 10. The system internally uses a hidden cost evaluation function w to assign a transport cost index to any one-way route between two different hubs i and j. The cost index ranges from 0 to 10 (integers).

Your goal is to infer the calculation pattern of this transport cost function through as few route surveys as possible, and make correct cost predictions for unplanned routes.

You can perform the following operations:

1. **Route Survey (Training Query)** (at most 12 times): Specify any two different hubs i and j (both integers from 0 to 10, and i not equal to j). The system will return the corresponding transport cost index. If the query format is invalid (e.g., i equals j or out of bounds), "Invalid" will be returned and it won't count toward the survey limit.

2. **Enter Test Phase**: When you think you have understood the cost calculation pattern, you can declare to enter testing. The system will provide 5 un-surveyed routes, and you need to predict the cost index for each route.

3. **Declare Rule** (optional): You can directly provide the complete cost calculation model. The system will verify it with several un-surveyed routes in the background. If all are correct, the task is successful.

Each time only one tag is allowed. Use the following XML format:

- Route Survey (e.g., survey route cost from hub 3 to hub 7):
<query_train>3,7</query_train>

- Enter Test Phase:
<enter_test></enter_test>

- Test Phase Prediction (e.g., predict cost index from hub 2 to hub 5 is 8):
<predict>2,5,8</predict>

- Declare Rule (give parameters a, b, c, representing the cost model w(i,j) = (a*i + b*j + c) mod 11):
<declare_rule>a=3,b=5,c=2</declare_rule>

- **Victory**: All 5 predictions in the test phase are correct, or rule declaration passes all verifications.
- **Failure**: Any prediction in the test phase is wrong, or rule declaration verification fails, or exceeds the 12 survey query limit.
"""

    contextualized_rule_zh_2 = """\
我们来使用一个"药物相互作用强度评估"系统，规则如下：

我们的生化数据库包含了由编号 0 到 10 代表的 11 种核心药物成分。系统内部配置了一个隐藏的生化反应函数 w，为任意两种不同的成分 i 和 j 联合使用时分配一个相互作用强度指数（反映副作用或协同效应），指数范围是 0 到 10 的整数。

你的目标是通过尽可能少的联合测试来推断出这个生化反应函数的规律，并能对未测试过的成分组合做出正确的强度预测。

你可以进行以下操作：

1. **联合测试（训练查询）**（至多12次）：指定任意两种不同的成分 i 和 j 进行生化反应测试。你需要提供成分 i 和成分 j 的编号（均为0到10之间的整数，且 i 不等于 j）。系统会返回对应的相互作用强度指数。如果查询格式无效（如 i 等于 j 或越界），将返回"无效"，且不计入测试次数。

2. **进入测试阶段**：当你认为已经掌握了相互作用的规律，可以宣布进入测试。系统会给出5组未被测试过的成分组合，你需要预测每组的相互作用强度指数。

3. **宣告规则**（可选）：你可以直接给出完整的生化反应模型。系统会用若干未测试过的成分组合进行临床后台验证，如果全部正确则任务成功。

每次只能包含一个标签，使用以下 XML 格式：

- 联合测试（例如测试成分3和成分7的相互作用强度）：
<query_train>3,7</query_train>

- 进入测试阶段：
<enter_test></enter_test>

- 测试阶段预测（例如预测成分2和成分5的强度指数为8）：
<predict>2,5,8</predict>

- 宣告规则（给出参数 a、b、c，表示反应模型为 w(i,j) = (a*i + b*j + c) mod 11）：
<declare_rule>a=3,b=5,c=2</declare_rule>

- **胜利**：测试阶段5个预测全部正确，或规则宣告验证全部通过。
- **失败**：测试阶段任一预测错误，或规则宣告验证失败，或超过12次联合测试查询限制。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's use a "Drug Interaction Intensity Assessment" system. Here are the rules:

Our biochemical database contains 11 core drug components represented by numbers 0 to 10. The system internally configures a hidden biochemical reaction function w to assign an interaction intensity index (reflecting side effects or synergy) when any two different components i and j are used in combination. The index ranges from 0 to 10 (integers).

Your goal is to infer the pattern of this biochemical reaction function through as few joint tests as possible, and make correct intensity predictions for untested component combinations.

You can perform the following operations:

1. **Joint Test (Training Query)** (at most 12 times): Specify any two different components i and j for biochemical reaction testing. You need to provide the component numbers i and j (both integers from 0 to 10, and i not equal to j). The system will return the corresponding interaction intensity index. If the query format is invalid (e.g., i equals j or out of bounds), "Invalid" will be returned and it won't count toward the test limit.

2. **Enter Test Phase**: When you think you have understood the interaction pattern, you can declare to enter testing. The system will provide 5 untested component combinations, and you need to predict the interaction intensity index for each group.

3. **Declare Rule** (optional): You can directly provide the complete biochemical reaction model. The system will verify it with several untested combinations in the clinical background. If all are correct, the task is successful.

Each time only one tag is allowed. Use the following XML format:

- Joint Test (e.g., test the interaction intensity of component 3 and component 7):
<query_train>3,7</query_train>

- Enter Test Phase:
<enter_test></enter_test>

- Test Phase Prediction (e.g., predict the intensity index of component 2 and component 5 is 8):
<predict>2,5,8</predict>

- Declare Rule (give parameters a, b, c, representing the reaction model w(i,j) = (a*i + b*j + c) mod 11):
<declare_rule>a=3,b=5,c=2</declare_rule>

- **Victory**: All 5 predictions in the test phase are correct, or rule declaration passes all verifications.
- **Failure**: Any prediction in the test phase is wrong, or rule declaration verification fails, or exceeds the 12 joint test query limit.
"""

    contextualized_rule_zh_3 = """\
我们来进行一项"学习路径认知负荷评估"任务，规则如下：

我们的课程体系包含了由编号 0 到 10 代表的 11 个核心知识模块。系统内部采用了一个隐藏的认知评估函数 w，为学习者从任意模块 i 过渡到不同模块 j 的学习过程分配一个认知负荷指数，指数范围是 0 到 10 的整数。

你的目标是通过尽可能少的学习路径测评来推断出这个认知负荷函数的计算规律，并能对未测评过的模块衔接做出正确的负荷预测。

你可以进行以下操作：

1. **路径测评（训练查询）**（至多12次）：指定任意两个不同的知识模块 i 和 j。你需要提供前置模块 i 和后置模块 j 的编号（均为0到10之间的整数，且 i 不等于 j）。系统会返回对应的认知负荷指数。如果查询格式无效（如 i 等于 j 或越界），将返回"无效"，且不计入测评次数。

2. **进入测试阶段**：当你认为已经掌握了认知负荷规律，可以宣布进入测试。系统会给出5组未被测评过的模块衔接，你需要预测每组的认知负荷指数。

3. **宣告规则**（可选）：你可以直接给出完整的认知评估模型。系统会用若干未测评过的模块组合进行后台验证，如果全部正确则任务成功。

每次只能包含一个标签，使用以下 XML 格式：

- 路径测评（例如测评从模块3过渡到模块7的认知负荷）：
<query_train>3,7</query_train>

- 进入测试阶段：
<enter_test></enter_test>

- 测试阶段预测（例如预测从模块2过渡到模块5的负荷指数为8）：
<predict>2,5,8</predict>

- 宣告规则（给出参数 a、b、c，表示认知模型为 w(i,j) = (a*i + b*j + c) mod 11）：
<declare_rule>a=3,b=5,c=2</declare_rule>

- **胜利**：测试阶段5个预测全部正确，或规则宣告验证全部通过。
- **失败**：测试阶段任一预测错误，或规则宣告验证失败，或超过12次测评查询限制。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a "Learning Path Cognitive Load Assessment" task. Here are the rules:

Our curriculum system contains 11 core knowledge modules represented by numbers 0 to 10. The system internally uses a hidden cognitive assessment function w to assign a cognitive load index to the learning transition from any module i to a different module j. The index ranges from 0 to 10 (integers).

Your goal is to infer the calculation pattern of this cognitive load function through as few path evaluations as possible, and make correct load predictions for unevaluated module transitions.

You can perform the following operations:

1. **Path Evaluation (Training Query)** (at most 12 times): Specify any two different knowledge modules i and j. You need to provide the prerequisite module i and the subsequent module j (both integers from 0 to 10, and i not equal to j). The system will return the corresponding cognitive load index. If the query format is invalid (e.g., i equals j or out of bounds), "Invalid" will be returned and it won't count toward the evaluation limit.

2. **Enter Test Phase**: When you think you have understood the cognitive load pattern, you can declare to enter testing. The system will provide 5 unevaluated module transitions, and you need to predict the cognitive load index for each group.

3. **Declare Rule** (optional): You can directly provide the complete cognitive assessment model. The system will verify it with several unevaluated module combinations in the background. If all are correct, the task is successful.

Each time only one tag is allowed. Use the following XML format:

- Path Evaluation (e.g., evaluate the cognitive load from module 3 to module 7):
<query_train>3,7</query_train>

- Enter Test Phase:
<enter_test></enter_test>

- Test Phase Prediction (e.g., predict the load index from module 2 to module 5 is 8):
<predict>2,5,8</predict>

- Declare Rule (give parameters a, b, c, representing the cognitive model w(i,j) = (a*i + b*j + c) mod 11):
<declare_rule>a=3,b=5,c=2</declare_rule>

- **Victory**: All 5 predictions in the test phase are correct, or rule declaration passes all verifications.
- **Failure**: Any prediction in the test phase is wrong, or rule declaration verification fails, or exceeds the 12 evaluation query limit.
"""

    contextualized_rule_zh_4 = """\
我们来测试一个"工业流水线物料流转能耗分析"系统，规则如下：

我们的自动化车间包含了由编号 0 到 10 代表的 11 个关键加工工序。系统内部搭载了一个隐藏的能耗计算函数 w，为物料从任意工序 i 流转到不同工序 j 的过程分配一个能量损耗指数，指数范围是 0 到 10 的整数。

你的目标是通过尽可能少的流转测量来推断出这个能耗函数的计算规律，并能对未测量过的工序流转路径做出正确的能耗预测。

你可以进行以下操作：

1. **流转测量（训练查询）**（至多12次）：指定任意两个不同的加工工序 i 和 j。你需要提供上游工序 i 和下游工序 j 的编号（均为0到10之间的整数，且 i 不等于 j）。系统会返回对应的能量损耗指数。如果查询格式无效（如 i 等于 j 或越界），将返回"无效"，且不计入测量次数。

2. **进入测试阶段**：当你认为已经掌握了能耗计算规律，可以宣布进入测试。系统会给出5条未被测量过的流转路径，你需要预测每条路径的能量损耗指数。

3. **宣告规则**（可选）：你可以直接给出完整的能耗计算模型。系统会用若干未测量过的工序路径进行后台验证，如果全部正确则任务成功。

每次只能包含一个标签，使用以下 XML 格式：

- 流转测量（例如测量从工序3流转到工序7的能耗）：
<query_train>3,7</query_train>

- 进入测试阶段：
<enter_test></enter_test>

- 测试阶段预测（例如预测从工序2流转到工序5的能耗指数为8）：
<predict>2,5,8</predict>

- 宣告规则（给出参数 a、b、c，表示能耗模型为 w(i,j) = (a*i + b*j + c) mod 11）：
<declare_rule>a=3,b=5,c=2</declare_rule>

- **胜利**：测试阶段5个预测全部正确，或规则宣告验证全部通过。
- **失败**：测试阶段任一预测错误，或规则宣告验证失败，或超过12次测量查询限制。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's test an "Industrial Assembly Line Material Flow Energy Consumption Analysis" system. Here are the rules:

Our automated workshop contains 11 key processing workstations represented by numbers 0 to 10. The system internally features a hidden energy calculation function w to assign an energy loss index to the material flow from any workstation i to a different workstation j. The index ranges from 0 to 10 (integers).

Your goal is to infer the calculation pattern of this energy function through as few flow measurements as possible, and make correct energy predictions for unmeasured workstation flow paths.

You can perform the following operations:

1. **Flow Measurement (Training Query)** (at most 12 times): Specify any two different workstations i and j. You need to provide the upstream workstation i and the downstream workstation j (both integers from 0 to 10, and i not equal to j). The system will return the corresponding energy loss index. If the query format is invalid (e.g., i equals j or out of bounds), "Invalid" will be returned and it won't count toward the measurement limit.

2. **Enter Test Phase**: When you think you have understood the energy calculation pattern, you can declare to enter testing. The system will provide 5 unmeasured flow paths, and you need to predict the energy loss index for each path.

3. **Declare Rule** (optional): You can directly provide the complete energy calculation model. The system will verify it with several unmeasured workstation paths in the background. If all are correct, the task is successful.

Each time only one tag is allowed. Use the following XML format:

- Flow Measurement (e.g., measure the energy loss from workstation 3 to workstation 7):
<query_train>3,7</query_train>

- Enter Test Phase:
<enter_test></enter_test>

- Test Phase Prediction (e.g., predict the energy loss index from workstation 2 to workstation 5 is 8):
<predict>2,5,8</predict>

- Declare Rule (give parameters a, b, c, representing the energy model w(i,j) = (a*i + b*j + c) mod 11):
<declare_rule>a=3,b=5,c=2</declare_rule>

- **Victory**: All 5 predictions in the test phase are correct, or rule declaration passes all verifications.
- **Failure**: Any prediction in the test phase is wrong, or rule declaration verification fails, or exceeds the 12 measurement query limit.
"""

    contextualized_rule_zh_5 = """\
我们来运行一个"司法案件定罪权重分析"系统，规则如下：

我们的量刑数据库包含了由编号 0 到 10 代表的 11 种关键案情特征。系统内部运用了一个隐藏的司法评估函数 w，为任意两种不同的特征 i 和特征 j 叠加时分配一个定罪权重指数，指数范围是 0 到 10 的整数。

你的目标是通过尽可能少的特征组合质询来推断出这个定罪权重函数的规律，并能对未质询过的特征组合做出正确的权重预测。

你可以进行以下操作：

1. **特征质询（训练查询）**（至多12次）：指定任意两种不同的案情特征 i 和 j 进行量刑组合测试。你需要提供特征 i 和特征 j 的编号（均为0到10之间的整数，且 i 不等于 j）。系统会返回对应的定罪权重指数。如果查询格式无效（如 i 等于 j 或越界），将返回"无效"，且不计入质询次数。

2. **进入测试阶段**：当你认为已经掌握了权重评估规律，可以宣布进入测试。系统会给出5组未被质询过的特征组合，你需要预测每组的定罪权重指数。

3. **宣告规则**（可选）：你可以直接给出完整的司法评估模型。系统会用若干未质询过的特征组合进行后台交叉验证，如果全部正确则任务成功。

每次只能包含一个标签，使用以下 XML 格式：

- 特征质询（例如质询特征3和特征7叠加的定罪权重）：
<query_train>3,7</query_train>

- 进入测试阶段：
<enter_test></enter_test>

- 测试阶段预测（例如预测特征2和特征5的权重指数为8）：
<predict>2,5,8</predict>

- 宣告规则（给出参数 a、b、c，表示评估模型为 w(i,j) = (a*i + b*j + c) mod 11）：
<declare_rule>a=3,b=5,c=2</declare_rule>

- **胜利**：测试阶段5个预测全部正确，或规则宣告验证全部通过。
- **失败**：测试阶段任一预测错误，或规则宣告验证失败，或超过12次质询查询限制。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's run a "Judicial Case Conviction Weight Analysis" system. Here are the rules:

Our sentencing database contains 11 key case features represented by numbers 0 to 10. The system internally utilizes a hidden judicial assessment function w to assign a conviction weight index when any two different features i and j are combined. The index ranges from 0 to 10 (integers).

Your goal is to infer the pattern of this conviction weight function through as few feature combination inquiries as possible, and make correct weight predictions for uninquired feature combinations.

You can perform the following operations:

1. **Feature Inquiry (Training Query)** (at most 12 times): Specify any two different case features i and j for sentencing combination testing. You need to provide the feature numbers i and j (both integers from 0 to 10, and i not equal to j). The system will return the corresponding conviction weight index. If the query format is invalid (e.g., i equals j or out of bounds), "Invalid" will be returned and it won't count toward the inquiry limit.

2. **Enter Test Phase**: When you think you have understood the weight assessment pattern, you can declare to enter testing. The system will provide 5 uninquired feature combinations, and you need to predict the conviction weight index for each group.

3. **Declare Rule** (optional): You can directly provide the complete judicial assessment model. The system will verify it with several uninquired feature combinations via background cross-validation. If all are correct, the task is successful.

Each time only one tag is allowed. Use the following XML format:

- Feature Inquiry (e.g., inquire about the conviction weight of feature 3 and feature 7 combined):
<query_train>3,7</query_train>

- Enter Test Phase:
<enter_test></enter_test>

- Test Phase Prediction (e.g., predict the weight index of feature 2 and feature 5 is 8):
<predict>2,5,8</predict>

- Declare Rule (give parameters a, b, c, representing the assessment model w(i,j) = (a*i + b*j + c) mod 11):
<declare_rule>a=3,b=5,c=2</declare_rule>

- **Victory**: All 5 predictions in the test phase are correct, or rule declaration passes all verifications.
- **Failure**: Any prediction in the test phase is wrong, or rule declaration verification fails, or exceeds the 12 inquiry query limit.
"""

    tags = ["answer", "query_train", "enter_test", "predict", "declare_rule"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "a": 1,
                "b": 0,
                "c": 0,
                "test_pairs": [(2, 3), (4, 5), (6, 7), (8, 9), (1, 10)]
            },
            2: {
                "a": 2,
                "b": 1,
                "c": 0,
                "test_pairs": [(1, 4), (2, 6), (3, 8), (5, 9), (0, 7)]
            },
            3: {
                "a": 3,
                "b": 4,
                "c": 2,
                "test_pairs": [(0, 5), (1, 6), (2, 7), (3, 9), (4, 10)]
            },
            4: {
                "a": 5,
                "b": 7,
                "c": 3,
                "test_pairs": [(1, 3), (2, 8), (4, 9), (5, 10), (0, 6)]
            },
            5: {
                "a": 7,
                "b": 9,
                "c": 8,
                "test_pairs": [(0, 4), (1, 7), (2, 9), (3, 10), (5, 8)]
            }
        },
        "en": {
            1: {
                "a": 1,
                "b": 0,
                "c": 0,
                "test_pairs": [(2, 3), (4, 5), (6, 7), (8, 9), (1, 10)]
            },
            2: {
                "a": 2,
                "b": 1,
                "c": 0,
                "test_pairs": [(1, 4), (2, 6), (3, 8), (5, 9), (0, 7)]
            },
            3: {
                "a": 3,
                "b": 4,
                "c": 2,
                "test_pairs": [(0, 5), (1, 6), (2, 7), (3, 9), (4, 10)]
            },
            4: {
                "a": 5,
                "b": 7,
                "c": 3,
                "test_pairs": [(1, 3), (2, 8), (4, 9), (5, 10), (0, 6)]
            },
            5: {
                "a": 7,
                "b": 9,
                "c": 8,
                "test_pairs": [(0, 4), (1, 7), (2, 9), (3, 10), (5, 8)]
            }
        }
    }

    def __init__(self, config):
        self.query_count = 0
        self.queried_pairs = set()
        self.in_test_phase = False
        self.test_index = 0
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self.a = cfg["a"]
        self.b = cfg["b"]
        self.c = cfg["c"]
        
        self.test_pairs = cfg["test_pairs"]
        
        self._game_info = {}

    def _compute_weight(self, i, j):
        return (self.a * i + self.b * j + self.c) % 11

    def _validate_vertex_pair(self, i, j):
        try:
            i, j = int(i), int(j)
            if i < 0 or i > 10 or j < 0 or j > 10:
                return False, None, None
            if i == j:
                return False, None, None
            return True, i, j
        except:
            return False, None, None

    def evaluate(self, parsed_info):
        if "answer" in parsed_info:
            return self._evaluate_rule(parsed_info["answer"])
        return False

    def _evaluate_rule(self, rule_str):
        try:
            parts = [x.strip() for x in rule_str.split(",")]
            params = {}
            for part in parts:
                if "=" in part:
                    key, val = part.split("=", 1)
                    params[key.strip()] = int(val.strip())
            
            if "a" not in params or "b" not in params or "c" not in params:
                return False
            
            if params["a"] % 11 != self.a % 11 or params["b"] % 11 != self.b % 11 or params["c"] % 11 != self.c % 11:
                return False
            
            verification_pairs = []
            for i in range(11):
                for j in range(11):
                    if i != j and (i, j) not in self.queried_pairs:
                        verification_pairs.append((i, j))
                        if len(verification_pairs) >= 5:
                            break
                if len(verification_pairs) >= 5:
                    break
            
            for i, j in verification_pairs:
                predicted = (params["a"] * i + params["b"] * j + params["c"]) % 11
                actual = self._compute_weight(i, j)
                if predicted != actual:
                    return False
            
            return True
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            invalid_msg = "无效查询"
            limit_msg = f"已达到训练查询上限（12次）"
            entered_test_msg = "已进入测试阶段，第{idx}题：请预测顶点对 ({i},{j}) 的边权值"
            correct_pred_msg = "预测正确"
            wrong_pred_msg = "预测错误"
            test_complete_msg = "测试完成，但还有题目未完成"
        else:
            invalid_msg = "Invalid query"
            limit_msg = f"Training query limit reached (12 times)"
            entered_test_msg = "Entered test phase, question {idx}: Please predict the edge weight of vertex pair ({i},{j})"
            correct_pred_msg = "Prediction correct"
            wrong_pred_msg = "Prediction incorrect"
            test_complete_msg = "Test incomplete"

        if "query_train" in parsed_info:
            if self.in_test_phase:
                return "Error: Already in test phase" if self.config.language == "en" else "错误：已进入测试阶段"
            
            if self.query_count >= 12:
                self.state.set_state("failed", "exceeded training query limit")
                return limit_msg
            
            try:
                raw = parsed_info["query_train"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return invalid_msg
                
                valid, i, j = self._validate_vertex_pair(parts[0], parts[1])
                if not valid:
                    return invalid_msg
                
                self.query_count += 1
                self.queried_pairs.add((i, j))
                
                weight = self._compute_weight(i, j)
                return str(weight)
            except:
                return invalid_msg

        elif "enter_test" in parsed_info:
            if self.in_test_phase:
                return "Error: Already in test phase" if self.config.language == "en" else "错误：已在测试阶段"
            
            self.in_test_phase = True
            self.test_index = 0
            i, j = self.test_pairs[0]
            return entered_test_msg.format(idx=1, i=i, j=j)

        elif "predict" in parsed_info:
            if not self.in_test_phase:
                return "Error: Not in test phase" if self.config.language == "en" else "错误：未进入测试阶段"
            
            if self.test_index >= len(self.test_pairs):
                return test_complete_msg
            
            try:
                raw = parsed_info["predict"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 3:
                    return invalid_msg
                
                pred_i, pred_j, pred_w = int(parts[0]), int(parts[1]), int(parts[2])
                actual_i, actual_j = self.test_pairs[self.test_index]
                
                if pred_i != actual_i or pred_j != actual_j:
                    hint = f" (Expected: ({actual_i},{actual_j}))" if self.config.language == "en" else f" (期望预测: ({actual_i},{actual_j}))"
                    return invalid_msg + hint
                
                actual_weight = self._compute_weight(actual_i, actual_j)
                if pred_w != actual_weight:
                    self.state.set_state("failed", "incorrect prediction")
                    return wrong_pred_msg
                
                self.test_index += 1
                if self.test_index >= len(self.test_pairs):
                    self.state.set_state("success", "all predictions correct")
                    return correct_pred_msg + (". 所有测试通过！" if self.config.language == "zh" else ". All tests passed!")
                else:
                    next_i, next_j = self.test_pairs[self.test_index]
                    return correct_pred_msg + ". " + entered_test_msg.format(idx=self.test_index+1, i=next_i, j=next_j)
            except:
                return invalid_msg

        elif "declare_rule" in parsed_info:
            is_correct = self._evaluate_rule(parsed_info["declare_rule"])
            if is_correct:
                self.state.set_state("success", "rule declaration correct")
                return "规则验证通过！" if self.config.language == "zh" else "Rule verification passed!"
            else:
                self.state.set_state("failed", "rule declaration incorrect")
                return "规则验证失败" if self.config.language == "zh" else "Rule verification failed"

        else:
            raise ValueError("No valid query tag found")

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        for i in range(11):
            for j in range(11):
                if i == j:
                    continue
                
                query_str = f"<query_train>{i},{j}</query_train>"
                
                weight = self._compute_weight(i, j)
                answer_str = str(weight)
                
                queries.append({
                    "query": query_str,
                    "answer": answer_str
                })
        
        return queries

    def _cf_make_wrong(self, correct):
        try:
            val = int(correct)
            wrong_val = (val + 1) % 11
            return str(wrong_val)
        except ValueError:
            pass
        
        original_correct = correct
        
        if "是" in correct or "否" in correct:
            if "是" in correct:
                correct = correct.replace("是", "TEMP_YES")
            if "否" in correct:
                correct = correct.replace("否", "是")
            if "TEMP_YES" in correct:
                correct = correct.replace("TEMP_YES", "否")
        else:
            lower_correct = correct.lower()
            if "yes" in lower_correct:
                if "Yes" in correct: correct = correct.replace("Yes", "No")
                elif "YES" in correct: correct = correct.replace("YES", "NO")
                elif "yes" in correct: correct = correct.replace("yes", "no")
            elif "no" in lower_correct:
                if "No" in correct: correct = correct.replace("No", "Yes")
                elif "NO" in correct: correct = correct.replace("NO", "YES")
                elif "no" in correct: correct = correct.replace("no", "yes")

        if correct == original_correct and not correct.isdigit():
            return correct + "_WRONG"
        
        return correct