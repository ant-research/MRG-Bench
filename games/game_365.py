from .base import Game
import random
import itertools

class SubsetIdentificationGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "集合"

    game_rule_zh = """\
我们现在来玩一个"隐藏子集识别"的推理游戏，规则如下：

游戏设定了一个集合 U = {{P1, P2, P3, P4, P5, P6, P7, P8}}，这是 8 个元素的有限集合。我已经秘密选定了一个目标子集 K（K 是 U 的子集，可能为空集），在整个游戏过程中 K 保持不变。

你的目标是通过多轮查询来推断出这个隐藏的子集 K。你可以进行以下两种操作：

1. **查询操作**：提交一个子集 O（O 是 U 的子集，可以为空集），我会告诉你 K 是否完全包含在 O 中。
   - 如果 K 中的所有元素都在 O 中，我会回答"True"
   - 否则回答"False"

2. **宣告操作**：当你认为已经收集到足够信息后，提交你对 K 的最终猜测。
   - 如果你的猜测完全正确，游戏成功
   - 如果猜测错误，游戏失败

- 你必须至少进行 3 次查询后才能进行宣告
- 查询次数不能超过 12 次，超过后必须进行宣告
- 请尽可能用最少的查询次数找到答案

每次只能包含一个操作标签。请使用以下 XML 格式：

- 查询操作（例如查询子集 {{P1, P3, P5}}）：
<query>P1,P3,P5</query>

- 查询空集：
<query></query>

- 宣告操作（例如宣告 K = {{P2, P5}}）：
<answer>P2,P5</answer>

- 宣告空集：
<answer></answer>

注意：元素之间用英文逗号分隔，不需要花括号，元素顺序不影响结果。
"""

    game_rule_en = """\
Let's play a "Hidden Subset Identification" deduction game. Here are the rules:

There is a set U = {{P1, P2, P3, P4, P5, P6, P7, P8}}, a finite set of 8 elements. I have secretly selected a target subset K (K is a subset of U, possibly empty), and K remains unchanged throughout the game.

Your goal is to infer this hidden subset K through multiple rounds of queries. You can perform two types of operations:

1. **Query Operation**: Submit a subset O (O is a subset of U, can be empty), and I will tell you whether K is completely contained in O.
   - If all elements in K are in O, I will answer "True"
   - Otherwise, I will answer "False"

2. **Declare Operation**: When you believe you have gathered enough information, submit your final guess for K.
   - If your guess is completely correct, the game succeeds
   - If the guess is wrong, the game fails

- You must perform at least 3 queries before making a declaration
- You cannot exceed 12 queries; after that, you must make a declaration
- Please try to find the answer with as few queries as possible

Each turn must contain only one operation tag. Use the following XML format:

- Query Operation (e.g., querying subset {{P1, P3, P5}}):
<query>P1,P3,P5</query>

- Query empty set:
<query></query>

- Declare Operation (e.g., declaring K = {{P2, P5}}):
<answer>P2,P5</answer>

- Declare empty set:
<answer></answer>

Note: Separate elements with commas, no curly braces needed, element order does not matter.
"""

    
    contextualized_rule_zh_1 = """\
交通指挥中心接到报告，城市交通网络中的 8 个关键节点（集合 U = {{P1, P2, P3, P4, P5, P6, P7, P8}}）出现异常拥堵。系统分析发现，存在一个隐藏的“核心拥堵源”集合 K（K 是 U 的子集，可能为空集），在整个排查期间 K 保持不变。

你的目标是通过多轮封锁测试来推断出这个隐藏的拥堵源集合 K。你可以进行以下两种操作：

1. **查询操作**：提交一个监控子集 O（O 是 U 的子集，可以为空集），交通中心将对 O 中的节点进行封锁排查。
   - 如果拥堵源 K 中的所有节点都在封锁范围 O 内，系统拥堵将被完全隔离，我将回答"True"
   - 否则，拥堵仍会蔓延，我将回答"False"

2. **宣告操作**：当你认为已经收集到足够信息后，提交你对拥堵源 K 的最终判定。
   - 如果你的判定完全正确，拥堵顺利解除，游戏成功
   - 如果判定错误，将导致交通瘫痪，游戏失败

- 你必须至少进行 3 次查询后才能进行宣告
- 查询次数不能超过 12 次，超过后必须进行宣告
- 请尽可能用最少的查询次数找到答案

每次只能包含一个操作标签。请使用以下 XML 格式：

- 查询操作（例如封锁节点 {{P1, P3, P5}}）：
<query>P1,P3,P5</query>

- 查询空集：
<query></query>

- 宣告操作（例如宣告拥堵源 K = {{P2, P5}}）：
<answer>P2,P5</answer>

- 宣告空集：
<answer></answer>

注意：元素之间用英文逗号分隔，不需要花括号，元素顺序不影响结果。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The traffic command center reports abnormal congestion across 8 key nodes in the city's traffic network (Universe U = {{P1, P2, P3, P4, P5, P6, P7, P8}}). System analysis reveals a hidden "core congestion source" subset K (K is a subset of U, possibly empty), which remains unchanged throughout the investigation.

Your goal is to infer this hidden source subset K through multiple rounds of lockdown tests. You can perform two types of operations:

1. **Query Operation**: Submit a monitoring subset O (O is a subset of U, can be empty), and the center will enforce a lockdown on the nodes in O.
   - If all nodes in the congestion source K are within the lockdown scope O, the congestion will be completely isolated, and I will answer "True"
   - Otherwise, the congestion will continue to spread, and I will answer "False"

2. **Declare Operation**: When you believe you have gathered enough information, submit your final judgment for K.
   - If your judgment is completely correct, the congestion is successfully cleared, and the game succeeds
   - If the judgment is wrong, it will lead to traffic paralysis, and the game fails

- You must perform at least 3 queries before making a declaration
- You cannot exceed 12 queries; after that, you must make a declaration
- Please try to find the answer with as few queries as possible

Each turn must contain only one operation tag. Use the following XML format:

- Query Operation (e.g., lockdown nodes {{P1, P3, P5}}):
<query>P1,P3,P5</query>

- Query empty set:
<query></query>

- Declare Operation (e.g., declare source K = {{P2, P5}}):
<answer>P2,P5</answer>

- Declare empty set:
<answer></answer>

Note: Separate elements with commas, no curly braces needed, element order does not matter.
"""

    contextualized_rule_zh_2 = """\
医疗中心接收到一份罕见病例，患者在 8 个生化指标（集合 U = {{P1, P2, P3, P4, P5, P6, P7, P8}}）上表现出异常波动。主治医生确信，存在一个隐藏的“核心致病”指标集合 K（K 是 U 的子集，可能为空集），在整个诊断过程中 K 保持不变。

你的目标是通过多轮靶向药物测试来推断出这个隐藏的致病集合 K。你可以进行以下两种操作：

1. **查询操作**：提交一个靶向抑制子集 O（O 是 U 的子集，可以为空集），系统将对 O 中的指标施加干预药物。
   - 如果致病集合 K 中的所有指标都在干预范围 O 内，病症将被完全抑制，我将回答"True"
   - 否则，病症依然存在，我将回答"False"

2. **宣告操作**：当你认为已经收集到足够信息后，提交你对致病集合 K 的最终确诊。
   - 如果你的确诊完全正确，患者将得到有效治疗，游戏成功
   - 如果确诊错误，将引发严重并发症，游戏失败

- 你必须至少进行 3 次查询后才能进行宣告
- 查询次数不能超过 12 次，超过后必须进行宣告
- 请尽可能用最少的查询次数找到答案

每次只能包含一个操作标签。请使用以下 XML 格式：

- 查询操作（例如抑制指标 {{P1, P3, P5}}）：
<query>P1,P3,P5</query>

- 查询空集：
<query></query>

- 宣告操作（例如确诊致病集合 K = {{P2, P5}}）：
<answer>P2,P5</answer>

- 宣告空集：
<answer></answer>

注意：元素之间用英文逗号分隔，不需要花括号，元素顺序不影响结果。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
The medical center has received a rare case where a patient exhibits abnormal fluctuations across 8 biochemical markers (Universe U = {{P1, P2, P3, P4, P5, P6, P7, P8}}). The attending physician is convinced there is a hidden "core pathogenic" marker subset K (K is a subset of U, possibly empty), which remains unchanged throughout the diagnosis.

Your goal is to infer this hidden pathogenic subset K through multiple rounds of targeted drug tests. You can perform two types of operations:

1. **Query Operation**: Submit a targeted inhibition subset O (O is a subset of U, can be empty), and the system will administer intervention drugs to the markers in O.
   - If all markers in the pathogenic subset K are within the intervention scope O, the symptoms will be completely suppressed, and I will answer "True"
   - Otherwise, the symptoms will persist, and I will answer "False"

2. **Declare Operation**: When you believe you have gathered enough information, submit your final diagnosis for K.
   - If your diagnosis is completely correct, the patient will receive effective treatment, and the game succeeds
   - If the diagnosis is wrong, severe complications will occur, and the game fails

- You must perform at least 3 queries before making a declaration
- You cannot exceed 12 queries; after that, you must make a declaration
- Please try to find the answer with as few queries as possible

Each turn must contain only one operation tag. Use the following XML format:

- Query Operation (e.g., inhibit markers {{P1, P3, P5}}):
<query>P1,P3,P5</query>

- Query empty set:
<query></query>

- Declare Operation (e.g., diagnose pathogenic subset K = {{P2, P5}}):
<answer>P2,P5</answer>

- Declare empty set:
<answer></answer>

Note: Separate elements with commas, no curly braces needed, element order does not matter.
"""

    contextualized_rule_zh_3 = """\
教育评估系统正在分析一名学生的学习情况。该核心课程包含 8 个基础知识模块（集合 U = {{P1, P2, P3, P4, P5, P6, P7, P8}}）。系统判定该学生存在一个隐藏的“认知漏洞”模块集合 K（K 是 U 的子集，可能为空集），在整个测评期间 K 保持不变。

你的目标是通过多轮强化辅导测试来推断出这个隐藏的漏洞集合 K。你可以进行以下两种操作：

1. **查询操作**：提交一个强化测试子集 O（O 是 U 的子集，可以为空集），系统将针对 O 中的模块生成专门的试卷。
   - 如果学生的认知漏洞 K 中的所有模块都在测试范围 O 内被覆盖，学生将顺利通过综合评估，我将回答"True"
   - 否则，漏洞未被完全覆盖导致评估不达标，我将回答"False"

2. **宣告操作**：当你认为已经收集到足够信息后，提交你对漏洞集合 K 的最终分析报告。
   - 如果你的分析完全正确，系统将生成精准的个性化教案，游戏成功
   - 如果分析错误，将导致辅导方向偏差，游戏失败

- 你必须至少进行 3 次查询后才能进行宣告
- 查询次数不能超过 12 次，超过后必须进行宣告
- 请尽可能用最少的查询次数找到答案

每次只能包含一个操作标签。请使用以下 XML 格式：

- 查询操作（例如测试模块 {{P1, P3, P5}}）：
<query>P1,P3,P5</query>

- 查询空集：
<query></query>

- 宣告操作（例如宣告漏洞集合 K = {{P2, P5}}）：
<answer>P2,P5</answer>

- 宣告空集：
<answer></answer>

注意：元素之间用英文逗号分隔，不需要花括号，元素顺序不影响结果。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The educational assessment system is analyzing a student's learning profile. The core curriculum consists of 8 fundamental knowledge modules (Universe U = {{P1, P2, P3, P4, P5, P6, P7, P8}}). The system determines that the student has a hidden "cognitive gap" module subset K (K is a subset of U, possibly empty), which remains unchanged throughout the evaluation.

Your goal is to infer this hidden gap subset K through multiple rounds of intensive tutoring tests. You can perform two types of operations:

1. **Query Operation**: Submit an intensive testing subset O (O is a subset of U, can be empty), and the system will generate a specialized exam for the modules in O.
   - If all modules in the cognitive gap K are covered within the testing scope O, the student will pass the comprehensive assessment smoothly, and I will answer "True"
   - Otherwise, uncovered gaps will cause the assessment to fail, and I will answer "False"

2. **Declare Operation**: When you believe you have gathered enough information, submit your final analysis report for the gap subset K.
   - If your analysis is completely correct, the system will generate a precise personalized lesson plan, and the game succeeds
   - If the analysis is wrong, it will lead to an off-target tutoring direction, and the game fails

- You must perform at least 3 queries before making a declaration
- You cannot exceed 12 queries; after that, you must make a declaration
- Please try to find the answer with as few queries as possible

Each turn must contain only one operation tag. Use the following XML format:

- Query Operation (e.g., test modules {{P1, P3, P5}}):
<query>P1,P3,P5</query>

- Query empty set:
<query></query>

- Declare Operation (e.g., declare gap subset K = {{P2, P5}}):
<answer>P2,P5</answer>

- Declare empty set:
<answer></answer>

Note: Separate elements with commas, no curly braces needed, element order does not matter.
"""

    contextualized_rule_zh_4 = """\
一条自动化生产线上部署了 8 个关键传感器（集合 U = {{P1, P2, P3, P4, P5, P6, P7, P8}}）。目前批次产品出现质量缺陷，工程师断定是由一个隐藏的“故障传感器”集合 K（K 是 U 的子集，可能为空集）导致的，在整个排查期间 K 保持不变。

你的目标是通过多轮停机排查测试来推断出这个隐藏的故障集合 K。你可以进行以下两种操作：

1. **查询操作**：提交一个停机检修子集 O（O 是 U 的子集，可以为空集），系统将对 O 中的传感器进行隔离重置。
   - 如果所有的故障传感器 K 都在排查范围 O 内，生产线警报将完全消除，我将回答"True"
   - 否则，系统依然会检测到异常信号，我将回答"False"

2. **宣告操作**：当你认为已经收集到足够信息后，提交你对故障传感器集合 K 的最终定位。
   - 如果你的定位完全正确，设备将恢复正常运转，游戏成功
   - 如果定位错误，将导致大批次产品报废，游戏失败

- 你必须至少进行 3 次查询后才能进行宣告
- 查询次数不能超过 12 次，超过后必须进行宣告
- 请尽可能用最少的查询次数找到答案

每次只能包含一个操作标签。请使用以下 XML 格式：

- 查询操作（例如检修传感器 {{P1, P3, P5}}）：
<query>P1,P3,P5</query>

- 查询空集：
<query></query>

- 宣告操作（例如定位故障集合 K = {{P2, P5}}）：
<answer>P2,P5</answer>

- 宣告空集：
<answer></answer>

注意：元素之间用英文逗号分隔，不需要花括号，元素顺序不影响结果。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
An automated production line is equipped with 8 critical sensors (Universe U = {{P1, P2, P3, P4, P5, P6, P7, P8}}). The current batch of products has quality defects, and engineers conclude that this is caused by a hidden "faulty sensor" subset K (K is a subset of U, possibly empty), which remains unchanged throughout the troubleshooting process.

Your goal is to infer this hidden faulty subset K through multiple rounds of shutdown diagnostics. You can perform two types of operations:

1. **Query Operation**: Submit a maintenance shutdown subset O (O is a subset of U, can be empty), and the system will isolate and reset the sensors in O.
   - If all faulty sensors K are within the diagnostic scope O, the production line alarms will be completely cleared, and I will answer "True"
   - Otherwise, the system will still detect abnormal signals, and I will answer "False"

2. **Declare Operation**: When you believe you have gathered enough information, submit your final localization of the faulty sensor subset K.
   - If your localization is completely correct, the equipment will resume normal operation, and the game succeeds
   - If the localization is wrong, it will result in a large batch of scrapped products, and the game fails

- You must perform at least 3 queries before making a declaration
- You cannot exceed 12 queries; after that, you must make a declaration
- Please try to find the answer with as few queries as possible

Each turn must contain only one operation tag. Use the following XML format:

- Query Operation (e.g., maintain sensors {{P1, P3, P5}}):
<query>P1,P3,P5</query>

- Query empty set:
<query></query>

- Declare Operation (e.g., locate faulty subset K = {{P2, P5}}):
<answer>P2,P5</answer>

- Declare empty set:
<answer></answer>

Note: Separate elements with commas, no curly braces needed, element order does not matter.
"""

    contextualized_rule_zh_5 = """\
在一起复杂的商业诈骗案件中，警方锁定了 8 名关键嫌疑人（集合 U = {{P1, P2, P3, P4, P5, P6, P7, P8}}）。专案组确信其中存在一个隐藏的“核心共谋者”团伙 K（K 是 U 的子集，可能为空集），在整个侦查期间 K 的成员名单保持不变。

你的目标是通过多轮隔离审讯来推断出这个隐藏的共谋者团伙 K。你可以进行以下两种操作：

1. **查询操作**：提交一个传唤审讯子集 O（O 是 U 的子集，可以为空集），警方将对 O 中的嫌疑人进行集中突击审查。
   - 如果核心团伙 K 的所有成员都在本次传唤名单 O 中，案件的逻辑链将被完全闭合，我将回答"True"
   - 否则，因有共谋者漏网导致口供存在漏洞，我将回答"False"

2. **宣告操作**：当你认为已经收集到足够信息后，提交你对共谋者团伙 K 的最终指控名单。
   - 如果你的指控完全正确，犯罪网络将被彻底摧毁，游戏成功
   - 如果指控错误，将导致真凶逍遥法外或冤假错案，游戏失败

- 你必须至少进行 3 次查询后才能进行宣告
- 查询次数不能超过 12 次，超过后必须进行宣告
- 请尽可能用最少的查询次数找到答案

每次只能包含一个操作标签。请使用以下 XML 格式：

- 查询操作（例如传唤嫌疑人 {{P1, P3, P5}}）：
<query>P1,P3,P5</query>

- 查询空集：
<query></query>

- 宣告操作（例如指控团伙 K = {{P2, P5}}）：
<answer>P2,P5</answer>

- 宣告空集：
<answer></answer>

注意：元素之间用英文逗号分隔，不需要花括号，元素顺序不影响结果。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
In a complex commercial fraud case, the police have identified 8 key suspects (Universe U = {{P1, P2, P3, P4, P5, P6, P7, P8}}). The task force is convinced there is a hidden "core conspirator" syndicate K (K is a subset of U, possibly empty), and the roster of K remains unchanged throughout the investigation.

Your goal is to infer this hidden conspirator syndicate K through multiple rounds of isolated interrogations. You can perform two types of operations:

1. **Query Operation**: Submit a subpoena and interrogation subset O (O is a subset of U, can be empty), and the police will conduct concentrated surprise interrogations on the suspects in O.
   - If all members of the core syndicate K are in the subpoena list O, the logical chain of the case will be completely closed, and I will answer "True"
   - Otherwise, loopholes will exist in the testimonies due to missing conspirators, and I will answer "False"

2. **Declare Operation**: When you believe you have gathered enough information, submit your final indictment list for the conspirator syndicate K.
   - If your indictment is completely correct, the criminal network will be thoroughly dismantled, and the game succeeds
   - If the indictment is wrong, the real culprits will remain at large or false accusations will be made, and the game fails

- You must perform at least 3 queries before making a declaration
- You cannot exceed 12 queries; after that, you must make a declaration
- Please try to find the answer with as few queries as possible

Each turn must contain only one operation tag. Use the following XML format:

- Query Operation (e.g., subpoena suspects {{P1, P3, P5}}):
<query>P1,P3,P5</query>

- Query empty set:
<query></query>

- Declare Operation (e.g., indict syndicate K = {{P2, P5}}):
<answer>P2,P5</answer>

- Declare empty set:
<answer></answer>

Note: Separate elements with commas, no curly braces needed, element order does not matter.
"""

    user_prompt_zh = "游戏开始，请进行你的第一次查询。"
    user_prompt_en = "Game started. Please make your first query."

    tags = ["query", "answer"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"target": ["P3"]},
            2: {"target": ["P2", "P7"]},
            3: {"target": ["P1", "P4", "P6"]},
            4: {"target": ["P2", "P3", "P5", "P8"]},
            5: {"target": ["P1", "P3", "P4", "P6", "P7"]},
        },
        "en": {
            1: {"target": ["P3"]},
            2: {"target": ["P2", "P7"]},
            3: {"target": ["P1", "P4", "P6"]},
            4: {"target": ["P2", "P3", "P5", "P8"]},
            5: {"target": ["P1", "P3", "P4", "P6", "P7"]},
        },
    }

    def __init__(self, config):
        self.query_count = 0
        self.min_queries_required = 3
        self.max_queries_allowed = 12
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self.universe = {"P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"}
        
        self.target_subset = set(cfg["target"])
        
        if not self.target_subset.issubset(self.universe):
            raise ValueError(f"Target subset {self.target_subset} is not a subset of universe {self.universe}")
        
        self._game_info = {}

    def evaluate(self, parsed_info):
        if self.query_count < self.min_queries_required:
            return False
            
        raw_ans = parsed_info["answer"].strip()
        
        if not raw_ans:
            model_answer = set()
        else:
            elements = [x.strip() for x in raw_ans.split(",") if x.strip()]
            model_answer = set(elements)
        
        if not model_answer.issubset(self.universe):
            return False
        
        return model_answer == self.target_subset

    def _cf_core_produce(self, parsed_info):
        if "query" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        raw_query = parsed_info["query"].strip()
        
        if not raw_query:
            query_set = set()
        else:
            elements = [x.strip() for x in raw_query.split(",") if x.strip()]
            query_set = set(elements)
        
        if not query_set.issubset(self.universe):
            raise ValueError(
                "Query contains invalid elements. "
                f"Valid elements are: {sorted(self.universe)}. "
                f"Received: {sorted(query_set - self.universe)}"
            )
        
        self.query_count += 1
        
        if self.query_count > self.max_queries_allowed:
            raise ValueError(
                f"Exceeded maximum query limit of {self.max_queries_allowed}. "
                f"You should have submitted your final answer."
            )
        
        is_subset = self.target_subset.issubset(query_set)
        
        result = "True" if is_subset else "False"
        
        return result

    def get_all_possible_queries(self) -> list[dict]:
        universe_list = sorted(list(self.universe))
        all_queries = []

        for r in range(len(universe_list) + 1):
            for subset in itertools.combinations(universe_list, r):
                query_set = set(subset)
                
                query_str = ",".join(sorted(list(subset)))
                
                is_subset = self.target_subset.issubset(query_set)
                
                answer = "True" if is_subset else "False"
                
                all_queries.append({
                    "query": f"<query>{query_str}</query>",
                    "answer": answer
                })
        
        return all_queries

    def _cf_make_wrong(self, correct: str) -> str:
        if correct == "True":
            return "False"
        if correct == "False":
            return "True"
            
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        else:
            if "Yes" in correct:
                return correct.replace("Yes", "No")
            if "No" in correct:
                return correct.replace("No", "Yes")
            if "yes" in correct:
                return correct.replace("yes", "no")
            if "no" in correct:
                return correct.replace("no", "yes")
                
        return correct + "_WRONG"