from .base import Game

class HiddenParameterInferenceGame(Game):

    game_rule_zh = """\
我们现在来玩一个"隐藏参数推理"游戏，规则如下：

游戏设定了两个隐藏信息：
1. 一个整数 N，范围在 0 到 59 之间（包含 0 和 59）
2. 一个映射类型 S，可能是 A、B 或 C 三种之一

每种映射类型定义了不同的计算规则：
- 类型 A：结果 r 等于 N 除以 t 的余数
- 类型 B：结果 r 等于 (N + 1) 除以 t 的余数
- 类型 C：结果 r 等于 (2 × N) 除以 t 的余数

你的目标是通过查询推断出映射类型 S 和整数 N 的具体值。

你可以反复进行查询操作：
- 每次查询需要提供一个模数参数 t，t 只能是 2、3、4 或 5
- 系统会根据隐藏的映射类型和 N 值，返回一个整数 r（0 小于等于 r 小于 t）
- 相同的 t 查询多次，结果保持一致

重要规则：
- 你必须至少进行两次查询后，才能提交最终答案
- 提交答案时需要同时给出映射类型 S 和整数 N 的猜测
- 如果猜测完全正确，游戏成功；否则游戏失败

## 查询与提交答案的格式（必须严格遵守）

每次查询使用以下格式（t 的值只能是 2、3、4 或 5）：

<query>3</query>

提交最终答案时，使用以下格式：

<answer>type=A, N=42</answer>

其中 type 的值为 A、B 或 C 之一，N 为 0 到 59 之间的整数。
"""

    game_rule_en = """\
Let's play a "Hidden Parameter Inference" game. Here are the rules:

The game has two hidden pieces of information:
1. An integer N in the range from 0 to 59 (inclusive)
2. A mapping type S, which can be A, B, or C

Each mapping type defines a different calculation rule:
- Type A: result r equals N modulo t
- Type B: result r equals (N + 1) modulo t
- Type C: result r equals (2 × N) modulo t

Your goal is to infer the exact mapping type S and integer N through queries.

You can repeatedly make queries:
- Each query requires providing a modulus parameter t, where t can only be 2, 3, 4, or 5
- The system will return an integer r (0 less than or equal to r less than t) based on the hidden mapping type and N value
- Querying the same t multiple times will yield consistent results

Important rules:
- You must make at least two queries before submitting your final answer
- When submitting your answer, you must provide both the mapping type S and integer N
- If your guess is completely correct, the game succeeds; otherwise, it fails

## Query and Answer Format (must be strictly followed)

For each query, use the following format (t can only be 2, 3, 4, or 5):

<query>3</query>

When submitting the final answer, use this format:

<answer>type=A, N=42</answer>

Where type is one of A, B, or C, and N is an integer from 0 to 59.
"""

    contextualized_rule_zh_1 = """\
欢迎进入【智能交通路网参数标定系统】。

目前，目标路段的交通控制模型存在两个隐藏的运行参数需要你进行标定：
1. 基础车流量基数 N，范围在 0 到 59 辆/周期 之间（包含 0 和 59）
2. 交通调控模式 S，可能是 A（常规通行）、B（防拥堵干预）或 C（绿波带加速）三种之一

每种调控模式对应不同的车流离散计算规则：
- 类型 A（常规通行）：相位偏移量 r 等于 N 除以 t 的余数
- 类型 B（防拥堵干预）：相位偏移量 r 等于 (N + 1) 除以 t 的余数
- 类型 C（绿波带加速）：相位偏移量 r 等于 (2 × N) 除以 t 的余数

你的目标是通过仿真查询推断出调控模式 S 和基础车流量 N 的具体值。

你可以反复执行仿真查询操作：
- 每次查询需要设定一个抽样时间窗口 t，t 的值只能是 2、3、4 或 5（分钟）
- 系统会根据隐藏的调控模式和车流量基数，返回计算出的相位偏移量整数 r（0 小于等于 r 小于 t）
- 使用相同的 t 进行多次查询，系统环境稳定，结果将保持一致

重要规则：
- 必须至少进行两次仿真查询后，才能提交最终标定结果
- 提交结果时需要同时给出调控模式 S 和基础车流量 N
- 若标定完全准确，则路网恢复通畅；否则标定失败，系统将过载

## 查询与提交答案的格式（必须严格遵守）

每次查询使用以下格式（t 的值只能是 2、3、4 或 5）：

<query>3</query>

提交最终标定结果时，使用以下格式：

<answer>type=A, N=42</answer>

其中 type 的值为 A、B 或 C 之一，N 为 0 到 59 之间的整数。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the [Intelligent Traffic Network Parameter Calibration System].

Currently, the traffic control model for the target intersection has two hidden operational parameters that require your calibration:
1. Base traffic volume N, an integer ranging from 0 to 59 vehicles/cycle (inclusive)
2. Traffic regulation mode S, which can be A (Normal Transit), B (Anti-Congestion Intervention), or C (Green Wave Acceleration)

Each regulation mode defines a different calculation rule for flow dispersion:
- Type A (Normal): phase offset r equals N modulo t
- Type B (Anti-Congestion): phase offset r equals (N + 1) modulo t
- Type C (Green Wave): phase offset r equals (2 × N) modulo t

Your goal is to infer the exact regulation mode S and base traffic volume N through simulation queries.

You can repeatedly execute simulation queries:
- Each query requires setting a sampling time window t, where t can only be 2, 3, 4, or 5 (minutes)
- The system will return a phase offset integer r (0 less than or equal to r less than t) based on the hidden mode and volume
- Querying the same t multiple times yields consistent results under stable system environments

Important rules:
- You must make at least two simulation queries before submitting your final calibration results
- When submitting, you must provide both the regulation mode S and traffic volume N
- If your calibration is completely correct, the network restores smooth flow; otherwise, it fails and causes a gridlock

## Query and Answer Format (must be strictly followed)

For each query, use the following format (t can only be 2, 3, 4, or 5):

<query>3</query>

When submitting the final answer, use this format:

<answer>type=A, N=42</answer>

Where type is one of A, B, or C, and N is an integer from 0 to 59.
"""

    contextualized_rule_zh_2 = """\
欢迎使用【靶向药物代谢动力学推演系统】。

我们正在对一位罕见病患者进行用药分析，其体内有两个隐藏的病理生理参数：
1. 靶细胞基础活性指数 N，范围在 0 到 59 之间（包含 0 和 59）
2. 药物代谢酶分型 S，可能是 A（线性代谢）、B（超速代谢）或 C（阻滞代谢）三种之一

不同的酶分型会导致不同的毒副反应残留计算规则：
- 类型 A（线性代谢）：残留指数 r 等于 N 除以 t 的余数
- 类型 B（超速代谢）：残留指数 r 等于 (N + 1) 除以 t 的余数
- 类型 C（阻滞代谢）：残留指数 r 等于 (2 × N) 除以 t 的余数

你的目标是通过临床试剂检测推断出酶分型 S 和活性指数 N。

你可以反复进行试剂检测：
- 每次检测需要注入特定浓度的标记试剂 t，浓度 t 只能是 2、3、4 或 5（单位）
- 系统会根据患者真实的酶分型和活性指数，返回残留指数整数 r（0 小于等于 r 小于 t）
- 相同浓度的试剂多次检测，结果将保持一致

重要规则：
- 你必须至少进行两次试剂检测后，才能出具最终诊断报告
- 提交报告时需要同时给出酶分型 S（A/B/C）和活性指数 N
- 如果诊断完全正确，用药方案生效；否则患者将面临风险，诊断失败

## 查询与提交答案的格式（必须严格遵守）

每次检测查询使用以下格式（t 的值只能是 2、3、4 或 5）：

<query>3</query>

提交最终诊断报告时，使用以下格式：

<answer>type=A, N=42</answer>

其中 type 的值为 A、B 或 C 之一，N 为 0 到 59 之间的整数。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the [Targeted Pharmacokinetics Inference System].

We are analyzing medication for a rare disease patient, who has two hidden pathophysiological parameters:
1. Target cell baseline activity index N, an integer ranging from 0 to 59 (inclusive)
2. Drug-metabolizing enzyme phenotype S, which can be A (Linear Metabolism), B (Rapid Metabolism), or C (Blocked Metabolism)

Different enzyme phenotypes lead to different residual toxicity calculation rules:
- Type A (Linear): residual index r equals N modulo t
- Type B (Rapid): residual index r equals (N + 1) modulo t
- Type C (Blocked): residual index r equals (2 × N) modulo t

Your goal is to infer the exact enzyme phenotype S and activity index N through clinical reagent tests.

You can repeatedly perform reagent tests:
- Each test requires injecting a specific concentration of a marker reagent t, where t can only be 2, 3, 4, or 5 (units)
- The system will return a residual index integer r (0 less than or equal to r less than t) based on the patient's true phenotype and activity index
- Testing the same concentration multiple times will yield consistent results

Important rules:
- You must perform at least two reagent tests before issuing the final diagnostic report
- When submitting your report, you must provide both the enzyme phenotype S and activity index N
- If your diagnosis is completely accurate, the treatment plan succeeds; otherwise, the patient faces severe risks, and the diagnostic fails

## Query and Answer Format (must be strictly followed)

For each query, use the following format (t can only be 2, 3, 4, or 5):

<query>3</query>

When submitting the final answer, use this format:

<answer>type=A, N=42</answer>

Where type is one of A, B, or C, and N is an integer from 0 to 59.
"""

    contextualized_rule_zh_3 = """\
欢迎进入【自适应学习认知测评系统】。

该系统正在分析一名学生的认知模型，存在两个待诊断的隐藏学习参数：
1. 核心知识点掌握度基数 N，范围在 0 到 59 之间（包含 0 和 59）
2. 认知学习风格 S，可能是 A（视觉型）、B（听觉型）或 C（动觉型）三种之一

每种学习风格在不同难度测试下表现出特定的认知负荷计算规则：
- 类型 A（视觉型）：认知负荷偏差 r 等于 N 除以 t 的余数
- 类型 B（听觉型）：认知负荷偏差 r 等于 (N + 1) 除以 t 的余数
- 类型 C（动觉型）：认知负荷偏差 r 等于 (2 × N) 除以 t 的余数

你的目标是通过派发测试题组推断出学生的学习风格 S 和掌握度 N。

你可以反复派发题组进行评估：
- 每次评估需要设定题组的难度阶层 t，t 只能是 2、3、4 或 5
- 系统会根据学生的真实学习风格和知识基数，返回认知负荷偏差整数 r（0 小于等于 r 小于 t）
- 相同难度阶层多次评估，学生的发挥保持稳定，结果一致

重要规则：
- 你必须至少进行两次难度评估后，才能提交最终的学情诊断
- 提交诊断时需要同时给出学习风格 S 和掌握度基数 N
- 如果诊断完全符合实际，系统将生成完美学案；否则诊断失败

## 查询与提交答案的格式（必须严格遵守）

每次难度评估使用以下格式（t 的值只能是 2、3、4 或 5）：

<query>3</query>

提交最终学情诊断时，使用以下格式：

<answer>type=A, N=42</answer>

其中 type 的值为 A、B 或 C 之一，N 为 0 到 59 之间的整数。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the [Adaptive Learning Cognitive Assessment System].

The system is analyzing a student's cognitive model, which contains two hidden learning parameters to be diagnosed:
1. Core knowledge mastery baseline N, an integer ranging from 0 to 59 (inclusive)
2. Cognitive learning style S, which can be A (Visual), B (Auditory), or C (Kinesthetic)

Each learning style exhibits specific cognitive load calculation rules under different test difficulties:
- Type A (Visual): cognitive load deviation r equals N modulo t
- Type B (Auditory): cognitive load deviation r equals (N + 1) modulo t
- Type C (Kinesthetic): cognitive load deviation r equals (2 × N) modulo t

Your goal is to infer the exact learning style S and mastery baseline N by distributing test item sets.

You can repeatedly distribute test sets for evaluation:
- Each evaluation requires setting a difficulty tier t for the test set, where t can only be 2, 3, 4, or 5
- The system will return a cognitive load deviation integer r (0 less than or equal to r less than t) based on the student's true learning style and knowledge baseline
- Evaluating the same difficulty tier multiple times maintains consistent student performance and yields identical results

Important rules:
- You must conduct at least two difficulty evaluations before submitting the final academic diagnosis
- When submitting your diagnosis, you must provide both the learning style S and mastery baseline N
- If your diagnosis completely matches the reality, a perfect study plan is generated; otherwise, the diagnosis fails

## Query and Answer Format (must be strictly followed)

For each query, use the following format (t can only be 2, 3, 4, or 5):

<query>3</query>

When submitting the final answer, use this format:

<answer>type=A, N=42</answer>

Where type is one of A, B, or C, and N is an integer from 0 to 59.
"""

    contextualized_rule_zh_4 = """\
欢迎使用【高精密工业设备校准检测系统】。

当前有一台核心生产设备出现了微小偏差，需要你查明两个隐藏的工程参数：
1. 核心轴承基准公差值 N，范围在 0 到 59 微米之间（包含 0 和 59）
2. 材料形变特性分型 S，可能是 A（标准刚性）、B（热膨胀性）或 C（震动复合性）三种之一

不同的形变特性会导致不同的共振偏移计算规则：
- 类型 A（标准刚性）：共振偏移量 r 等于 N 除以 t 的余数
- 类型 B（热膨胀性）：共振偏移量 r 等于 (N + 1) 除以 t 的余数
- 类型 C（震动复合性）：共振偏移量 r 等于 (2 × N) 除以 t 的余数

你的目标是通过施加测试压力推断出材料特性 S 和公差值 N。

你可以反复进行压力检测：
- 每次检测需要设定一个压力测试级别 t，t 只能是 2、3、4 或 5（MPa）
- 传感器会根据实际的材料特性和公差值，返回一个共振偏移整数 r（0 小于等于 r 小于 t）
- 相同压力的多次测试不会造成疲劳累积，结果保持一致

重要规则：
- 你必须至少进行两次压力检测后，才能提交最终的设备校准报告
- 提交报告时需要同时给出材料特性 S 和公差值 N
- 如果参数完全吻合，设备成功修复；否则设备报废，任务失败

## 查询与提交答案的格式（必须严格遵守）

每次压力检测使用以下格式（t 的值只能是 2、3、4 或 5）：

<query>3</query>

提交最终校准报告时，使用以下格式：

<answer>type=A, N=42</answer>

其中 type 的值为 A、B 或 C 之一，N 为 0 到 59 之间的整数。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the [High-Precision Industrial Equipment Calibration System].

A core production device is currently experiencing minor deviations. You need to identify two hidden engineering parameters:
1. Core bearing reference tolerance value N, an integer ranging from 0 to 59 microns (inclusive)
2. Material deformation characteristic S, which can be A (Standard Rigidity), B (Thermal Expansion), or C (Vibration Composite)

Different deformation characteristics result in different resonance offset calculation rules:
- Type A (Standard Rigidity): resonance offset r equals N modulo t
- Type B (Thermal Expansion): resonance offset r equals (N + 1) modulo t
- Type C (Vibration Composite): resonance offset r equals (2 × N) modulo t

Your goal is to infer the exact material characteristic S and tolerance value N by applying test pressures.

You can repeatedly conduct pressure tests:
- Each test requires setting a pressure test level t, where t can only be 2, 3, 4, or 5 (MPa)
- The sensor will return a resonance offset integer r (0 less than or equal to r less than t) based on the actual material characteristic and tolerance value
- Multiple tests at the same pressure level will not cause fatigue accumulation, yielding consistent results

Important rules:
- You must perform at least two pressure tests before submitting the final equipment calibration report
- When submitting the report, you must provide both the material characteristic S and tolerance value N
- If the parameters match perfectly, the equipment is successfully repaired; otherwise, it is scrapped, and the mission fails

## Query and Answer Format (must be strictly followed)

For each query, use the following format (t can only be 2, 3, 4, or 5):

<query>3</query>

When submitting the final answer, use this format:

<answer>type=A, N=42</answer>

Where type is one of A, B, or C, and N is an integer from 0 to 59.
"""

    contextualized_rule_zh_5 = """\
欢迎进入【司法判例量刑辅助推演系统】。

我们正在对一起复杂的商业纠纷案进行复盘，案件背后有两个核心隐藏要素：
1. 争议金额量刑基数 N，范围在 0 到 59 之间（包含 0 和 59）
2. 法条适用解释倾向 S，可能是 A（严格文义解释）、B（目的扩张解释）或 C（惩罚性加重解释）三种之一

不同的解释倾向会产生不同的裁量权浮动计算规则：
- 类型 A（严格解释）：裁量浮动指数 r 等于 N 除以 t 的余数
- 类型 B（扩张解释）：裁量浮动指数 r 等于 (N + 1) 除以 t 的余数
- 类型 C（惩罚性解释）：裁量浮动指数 r 等于 (2 × N) 除以 t 的余数

你的目标是通过程序审查推断出解释倾向 S 和量刑基数 N。

你可以反复进行模拟审查：
- 每次审查需要指定合议庭配置参数 t，t 只能是 2、3、4 或 5（人）
- 系统会根据隐藏的解释倾向和量刑基数，返回一个裁量浮动整数 r（0 小于等于 r 小于 t）
- 相同配置下的多次模拟审查，得出的法律意见将保持一致

重要规则：
- 你必须至少进行两次程序审查后，才能提交最终的司法判决书
- 提交判决时需要同时给出解释倾向 S 和量刑基数 N
- 如果推演结果与真实判例完全一致，则复盘成功；否则导致错判，系统推演失败

## 查询与提交答案的格式（必须严格遵守）

每次模拟审查使用以下格式（t 的值只能是 2、3、4 或 5）：

<query>3</query>

提交最终判决书时，使用以下格式：

<answer>type=A, N=42</answer>

其中 type 的值为 A、B 或 C 之一，N 为 0 到 59 之间的整数。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the [Judicial Precedent Sentencing Auxiliary Inference System].

We are reviewing a complex commercial dispute case driven by two core hidden elements:
1. Dispute amount sentencing baseline N, an integer ranging from 0 to 59 (inclusive)
2. Statutory interpretation tendency S, which can be A (Strict Literal Interpretation), B (Teleological Expansion Interpretation), or C (Punitive Aggravation Interpretation)

Different interpretation tendencies generate different discretion fluctuation calculation rules:
- Type A (Strict Literal): discretion fluctuation index r equals N modulo t
- Type B (Teleological Expansion): discretion fluctuation index r equals (N + 1) modulo t
- Type C (Punitive Aggravation): discretion fluctuation index r equals (2 × N) modulo t

Your goal is to infer the exact interpretation tendency S and sentencing baseline N through procedural reviews.

You can repeatedly conduct simulated reviews:
- Each review requires specifying a collegial panel configuration parameter t, where t can only be 2, 3, 4, or 5 (members)
- The system will return a discretion fluctuation integer r (0 less than or equal to r less than t) based on the hidden tendency and baseline
- Multiple simulated reviews under the same configuration will yield consistent legal opinions

Important rules:
- You must conduct at least two procedural reviews before submitting the final judicial ruling
- When submitting the ruling, you must provide both the interpretation tendency S and sentencing baseline N
- If your inference perfectly aligns with the actual precedent, the review succeeds; otherwise, it results in a mistrial, and the inference fails

## Query and Answer Format (must be strictly followed)

For each query, use the following format (t can only be 2, 3, 4, or 5):

<query>3</query>

When submitting the final answer, use this format:

<answer>type=A, N=42</answer>

Where type is one of A, B, or C, and N is an integer from 0 to 59.
"""

    tags = ["answer", "query"]
    
    reasoning_type = "溯因推理"
    data_structure = "集合"

    # 难度说明：
    # 1 (easy)          - 类型 A，N 较小且特征明显
    # 2 (medium_easy)   - 类型 B，N 中等
    # 3 (medium_hard)   - 类型 C，N 需要多次查询确定
    # 4 (hard)          - 类型 A，N 较大且余数模式相似
    # 5 (very_hard)     - 类型 B，N 接近边界值

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "N": 12,
                "S": "A",
            },
            2: {
                "N": 27,
                "S": "B",
            },
            3: {
                "N": 35,
                "S": "C",
            },
            4: {
                "N": 47,
                "S": "A",
            },
            5: {
                "N": 58,
                "S": "B",
            },
        },
        "en": {
            1: {
                "N": 12,
                "S": "A",
            },
            2: {
                "N": 27,
                "S": "B",
            },
            3: {
                "N": 35,
                "S": "C",
            },
            4: {
                "N": 47,
                "S": "A",
            },
            5: {
                "N": 58,
                "S": "B",
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0  # 记录查询次数
        self.query_cache = {}  # 缓存查询结果
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.N = cfg["N"]  # 隐藏的整数
        self.S = cfg["S"]  # 隐藏的映射类型
        
        # 游戏规则不需要在初始化时填充参数
        self._game_info = {}

    def _calculate_result(self, t):
        """根据映射类型计算查询结果"""
        if self.S == "A":
            return self.N % t
        elif self.S == "B":
            return (self.N + 1) % t
        elif self.S == "C":
            return (2 * self.N) % t
        else:
            raise ValueError(f"Unknown mapping type: {self.S}")

    def evaluate(self, parsed_info):
        # 检查是否至少查询了两次
        if self.query_count < 2:
            return False
            
        # 解析答案: type=X, N=Y
        raw_ans = parsed_info["answer"]
        try:
            kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
            ans_dict = {}
            for kv in kv_pairs:
                k, v = kv.split("=", 1)
                ans_dict[k.strip()] = v.strip()
            
            if "type" not in ans_dict or "N" not in ans_dict:
                return False
            
            # 检查映射类型
            guessed_type = ans_dict["type"]
            if guessed_type not in ["A", "B", "C"]:
                return False
            
            # 检查整数 N
            guessed_N = int(ans_dict["N"])
            if guessed_N < 0 or guessed_N > 59:
                return False
            
            # 判断是否完全正确
            return guessed_type == self.S and guessed_N == self.N
            
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if "query" not in parsed_info:
            if self.config.language == "zh":
                return "错误：无效的查询格式。"
            else:
                return "Error: Invalid query format."
        
        try:
            t = int(parsed_info["query"].strip())
            
            # 检查 t 是否在允许的范围内
            if t not in [2, 3, 4, 5]:
                if self.config.language == "zh":
                    return "错误：模数 t 必须是 2、3、4 或 5。"
                else:
                    return "Error: Modulus t must be 2, 3, 4, or 5."
            
            # 增加查询计数
            self.query_count += 1
            
            # 如果已经查询过这个 t，直接返回缓存结果
            if t in self.query_cache:
                return str(self.query_cache[t])
            
            # 计算结果并缓存
            result = self._calculate_result(t)
            self.query_cache[t] = result
            
            return str(result)
            
        except ValueError:
            if self.config.language == "zh":
                return "错误：查询参数必须是整数。"
            else:
                return "Error: Query parameter must be an integer."

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        本游戏的合法查询模数 t 只有 2, 3, 4, 5。
        """
        possible_queries = []
        # t 只能是 2, 3, 4, 5
        for t in [2, 3, 4, 5]:
            # 直接调用内部计算逻辑，不经过 query_count 计数和格式检查
            result = self._calculate_result(t)
            possible_queries.append({
                "query": f"<query>{t}</query>",
                "answer": str(result)
            })
        return possible_queries

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            val = int(correct)
            # 生成一个不同的数字，在 0-4 范围内（覆盖所有可能的 r 值）
            wrong_val = (val + 1) % 5
            if wrong_val == val:
                wrong_val = (val + 2) % 5
            return str(wrong_val)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        if correct.lower() == "yes":
            return "No" if correct[0].isupper() else "no"
        if correct.lower() == "no":
            return "Yes" if correct[0].isupper() else "yes"
            
        return correct + "_WRONG"