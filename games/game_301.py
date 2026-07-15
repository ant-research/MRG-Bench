from .base import Game
import re

class HiddenFunctionGame(Game):
    
    reasoning_type = "溯因推理"
    data_structure = "树"

    game_rule_zh = """\
我们现在来玩一个"未知刻度函数推理"游戏，规则如下：

游戏设定了一个未知的非负整数 H（目标参数）和一个未知的刻度函数 f，该函数属于以下四种模式之一：
- 模式 α：f(x) = x
- 模式 β：f(x) = x + 1
- 模式 γ：f(x) = 2x
- 模式 δ：f(x) = 2x + 1

其中 x 为非负整数输入。在整个游戏过程中，H 和函数模式保持不变。

你的目标是通过测量查询推断出函数的模式（α、β、γ 或 δ）以及目标参数 H 的准确值。

你可以进行以下两种测量查询：

1. **已知自变量查询**：给定一个非负整数 t，系统返回 f(t) 的值。
2. **隐藏自变量平移查询**：给定一个非负整数 c，系统返回 f(H + c) 的值（H 本身不变，c 仅用于该次查询）。

请尽可能少地使用查询次数来推断答案。

每次查询只能包含一个标签，使用以下 XML 格式：

- 已知自变量查询（例如查询 t=3）：
<query_known>3</query_known>

- 隐藏自变量平移查询（例如查询 c=2）：
<query_hidden>2</query_hidden>

当你收集足够信息后，提交最终答案，必须说明函数模式（α、β、γ 或 δ）和目标参数 H 的值，格式如下：

<answer>mode=α, H=5</answer>

- 所有查询的输入必须是非负整数，否则视为无效查询。
- 累计两次无效查询将导致游戏失败。
- 答案错误或格式不符将导致游戏失败。
"""

    game_rule_en = """\
Let's play a "Hidden Scale Function Deduction" game. Here are the rules:

The game has set an unknown non-negative integer H (target parameter) and an unknown scale function f, which belongs to one of the following four modes:
- Mode α: f(x) = x
- Mode β: f(x) = x + 1
- Mode γ: f(x) = 2x
- Mode δ: f(x) = 2x + 1

where x is a non-negative integer input. Throughout the game, H and the function mode remain constant.

Your goal is to infer the function mode (α, β, γ, or δ) and the exact value of the target parameter H through measurement queries.

You can perform the following two types of measurement queries:

1. **Known Argument Query**: Given a non-negative integer t, the system returns the value of f(t).
2. **Hidden Argument Shift Query**: Given a non-negative integer c, the system returns the value of f(H + c) (H itself does not change; c only affects this query).

Try to use as few queries as possible to infer the answer.

Each query must contain only one tag. Use the following XML format:

- Known Argument Query (e.g., querying t=3):
<query_known>3</query_known>

- Hidden Argument Shift Query (e.g., querying c=2):
<query_hidden>2</query_hidden>

When you have enough information, submit your final answer, specifying the function mode (α, β, γ, or δ) and the value of target parameter H, using this format:

<answer>mode=α, H=5</answer>

- All query inputs must be non-negative integers, otherwise they are considered invalid queries.
- Two cumulative invalid queries will result in game failure.
- An incorrect answer or invalid format will result in game failure.
"""

    contextualized_rule_zh_1 = """\
我们现在进行“智能交通信号灯配时算法调试”。

系统设定了某主干道未知的基准车流量 H（辆/分钟，非负整数）和一个未知的绿灯时长计算模型 f，该算法属于以下四种模式之一：
- 模式 α：时长 f(x) = x 秒
- 模式 β：时长 f(x) = x + 1 秒
- 模式 γ：时长 f(x) = 2x 秒
- 模式 δ：时长 f(x) = 2x + 1 秒

其中 x 为输入的车流量。在调试期间，基准车流量 H 和配时算法模式保持绝对不变。

你的目标是通过测试查询推断出算法模式（α、β、γ 或 δ）以及基准车流量 H 的准确值。

你可以进行以下两种系统调用：

1. **虚拟环境测试（已知自变量查询）**：给定一个测试车流 t（非负整数），系统返回算法得出的绿灯时长 f(t)。
2. **实际环境测试（隐藏自变量平移查询）**：在目标路口叠加干预车流 c（非负整数），系统会根据总车流（H + c）返回绿灯时长 f(H + c)。注意这只是一次临时干预，基准 H 本身不变。

请尽可能少地使用测试次数来锁定参数。

每次调用只能包含一个标签，使用以下 XML 格式：

- 虚拟环境测试（例如输入车流 t=3）：
<query_known>3</query_known>

- 实际环境测试（例如叠加车流 c=2）：
<query_hidden>2</query_hidden>

查明参数后，请提交最终报告，指明算法模式（α、β、γ 或 δ）和基准车流 H，格式如下：

<answer>mode=α, H=5</answer>

- 所有测试参数必须是非负整数，否则将被系统驳回。
- 累计两次错误调用将导致系统锁死，调试失败。
- 报告错误或格式不符将导致调试失败。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
We are now initiating the "Intelligent Traffic Signal Timing Algorithm Debugging".

The system has set an unknown baseline traffic flow H (vehicles/minute, non-negative integer) for a main road and an unknown green light duration calculation model f, which operates in one of the following four modes:
- Mode α: Duration f(x) = x seconds
- Mode β: Duration f(x) = x + 1 seconds
- Mode γ: Duration f(x) = 2x seconds
- Mode δ: Duration f(x) = 2x + 1 seconds

where x is the input traffic flow. During debugging, the baseline flow H and the timing algorithm mode remain strictly constant.

Your objective is to deduce the algorithm mode (α, β, γ, or δ) and the exact value of the baseline traffic flow H through test queries.

You can execute the following two system calls:

1. **Virtual Environment Test (Known Argument Query)**: Input a test flow t (non-negative integer), and the system returns the calculated green light duration f(t).
2. **Real Environment Test (Hidden Argument Shift Query)**: Add an intervention flow c (non-negative integer) at the target intersection. The system calculates the duration based on the total flow f(H + c). Note that H remains unchanged.

Minimize your queries to lock in the parameters.

Each call must contain only one tag in the following XML format:

- Virtual Environment Test (e.g., flow t=3):
<query_known>3</query_known>

- Real Environment Test (e.g., intervention flow c=2):
<query_hidden>2</query_hidden>

Once identified, submit the final report specifying the algorithm mode and baseline flow H:

<answer>mode=α, H=5</answer>

- All inputs must be non-negative integers; otherwise, the call is invalid.
- Two invalid calls will lock the system and result in failure.
- Incorrect answers or invalid formats will result in debugging failure.
"""

    contextualized_rule_zh_2 = """\
欢迎使用“靶向药物代谢剂量推演系统”。

系统已锁定某患者体内未知的靶点蛋白基础浓度 H（单位，非负整数）和一种未知的剂量推荐模型 f，代谢曲线属于以下四种模式之一：
- 模式 α：推荐剂量 f(x) = x 毫克
- 模式 β：推荐剂量 f(x) = x + 1 毫克
- 模式 γ：推荐剂量 f(x) = 2x 毫克
- 模式 δ：推荐剂量 f(x) = 2x + 1 毫克

其中 x 为蛋白浓度。在整个诊断过程中，患者的基础浓度 H 和代谢模式保持不变。

你的目标是通过临床检测推断出剂量推荐模型（α、β、γ 或 δ）以及患者的靶点蛋白浓度 H。

你可以执行以下两项检测程序：

1. **体外样本分析（已知自变量查询）**：输入一个已知的离体蛋白浓度 t，系统依据模型计算所需的剂量 f(t)。
2. **体内浓度激发（隐藏自变量平移查询）**：为患者注射激发剂，使蛋白浓度临时增加 c 个单位。系统将返回当前体内总浓度（H + c）对应的推荐剂量 f(H + c)。激发结束后 H 恢复原状。

请合理规划，以最少的检测次数完成诊断。

每次调用只能包含一个标签，使用以下 XML 格式：

- 体外样本分析（例如输入浓度 t=3）：
<query_known>3</query_known>

- 体内浓度激发（例如增加浓度 c=2）：
<query_hidden>2</query_hidden>

确诊后，请提交最终结论，指明模型模式（α、β、γ 或 δ）和基础浓度 H，格式如下：

<answer>mode=α, H=5</answer>

- 检测输入参数必须为非负整数，否则视为违规操作。
- 累计发生两次违规操作将导致推演失败。
- 诊断错误或格式不符将直接导致失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Targeted Drug Metabolism Dose Deduction System".

The system has locked onto an unknown baseline target protein concentration H (units, non-negative integer) in a patient's body and an unknown dose recommendation model f, operating in one of four metabolic modes:
- Mode α: Recommended dose f(x) = x mg
- Mode β: Recommended dose f(x) = x + 1 mg
- Mode γ: Recommended dose f(x) = 2x mg
- Mode δ: Recommended dose f(x) = 2x + 1 mg

where x is the protein concentration. Throughout the diagnosis, the baseline concentration H and the metabolic mode remain constant.

Your objective is to deduce the dose recommendation model (α, β, γ, or δ) and the exact baseline protein concentration H through clinical testing.

You may perform the following two diagnostic procedures:

1. **In Vitro Sample Analysis (Known Argument Query)**: Input a known isolated protein concentration t. The system calculates the required dose f(t).
2. **In Vivo Concentration Stimulation (Hidden Argument Shift Query)**: Administer a stimulant to temporarily increase the patient's protein concentration by c units. The system returns the dose f(H + c) for the total current concentration. H reverts afterward.

Optimize your testing to finalize the diagnosis with minimal procedures.

Each query must contain only one tag in the following XML format:

- In Vitro Sample Analysis (e.g., concentration t=3):
<query_known>3</query_known>

- In Vivo Concentration Stimulation (e.g., increase c=2):
<query_hidden>2</query_hidden>

Once confirmed, submit the final diagnosis specifying the model mode and baseline concentration H:

<answer>mode=α, H=5</answer>

- Test parameters must be non-negative integers; otherwise, they are invalid.
- Two invalid operations will terminate the deduction.
- Incorrect diagnoses or invalid formats will result in failure.
"""

    contextualized_rule_zh_3 = """\
进入“自适应学习系统评估核准”流程。

本系统为某学员设定了未知的初始知识掌握度指数 H（非负整数）以及未知的题库难度适配函数 f，该评估算法属于以下四类模式之一：
- 模式 α：难度系数 f(x) = x
- 模式 β：难度系数 f(x) = x + 1
- 模式 γ：难度系数 f(x) = 2x
- 模式 δ：难度系数 f(x) = 2x + 1

其中 x 为输入给算法的掌握度数据。核准期间，学生的初始掌握度 H 和难度适配模式不会改变。

你的任务是通过系统调测，推断出难度适配模式（α、β、γ 或 δ）以及学生的初始掌握度 H。

可使用两种系统调测探针：

1. **基准题库测算（已知自变量查询）**：输入预设的掌握度指数 t，探针将返回算法分配的难度系数 f(t)。
2. **增效干预测算（隐藏自变量平移查询）**：在学生初始水平上通过干预模块临时附加能力增量 c。系统将基于叠加后的总掌握度（H + c）返回新的难度系数 f(H + c)。干预不影响后续查询。

请用尽可能少的调测步骤完成核准。

每次探针只能包含一个标签，使用以下 XML 格式：

- 基准题库测算（例如输入掌握度 t=3）：
<query_known>3</query_known>

- 增效干预测算（例如附加能力增量 c=2）：
<query_hidden>2</query_hidden>

获取足够数据后，提交算法模式（α、β、γ 或 δ）和掌握度 H 的核准结果，格式如下：

<answer>mode=α, H=5</answer>

- 所有输入的指数必须为非负整数，否则属于非法参数。
- 累计产生两次非法参数输入将被踢出调测系统。
- 结果错误或格式不合规将导致评估失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Entering the "Adaptive Learning System Assessment Calibration" workflow.

The system has set an unknown initial knowledge mastery index H (non-negative integer) for a student and an unknown question difficulty adaptation function f, which operates under one of four modes:
- Mode α: Difficulty coefficient f(x) = x
- Mode β: Difficulty coefficient f(x) = x + 1
- Mode γ: Difficulty coefficient f(x) = 2x
- Mode δ: Difficulty coefficient f(x) = 2x + 1

where x is the input mastery data. During calibration, the initial mastery H and the adaptation mode remain unchanged.

Your task is to determine the adaptation mode (α, β, γ, or δ) and the initial mastery index H through system diagnostics.

You can utilize two diagnostic probes:

1. **Baseline Question Pool Calculation (Known Argument Query)**: Input a preset mastery index t, and the probe returns the allocated difficulty f(t).
2. **Intervention Enhancement Calculation (Hidden Argument Shift Query)**: Temporarily add an ability increment c on top of the student's initial level via an intervention module. The system returns the difficulty f(H + c) based on the combined mastery. 

Minimize the diagnostic steps required to complete the calibration.

Each probe must contain only one tag in the following XML format:

- Baseline Pool Calculation (e.g., input mastery t=3):
<query_known>3</query_known>

- Intervention Enhancement Calculation (e.g., increment c=2):
<query_hidden>2</query_hidden>

Upon gathering sufficient data, submit the finalized mode and mastery H:

<answer>mode=α, H=5</answer>

- All input indices must be non-negative integers; otherwise, they are invalid parameters.
- Two invalid parameter inputs will expel you from the diagnostic system.
- An incorrect result or invalid format will lead to assessment failure.
"""

    contextualized_rule_zh_4 = """\
正在启动“数控机床热变形补偿校准”程序。

当前机床受车间环境影响，存在一个未知的基准环境热偏置值 H（微米，非负整数）。同时，伺服电机的补偿脉冲计算曲线 f 亦处于未知状态，归属以下四种模式之一：
- 模式 α：补偿脉冲 f(x) = x 个
- 模式 β：补偿脉冲 f(x) = x + 1 个
- 模式 γ：补偿脉冲 f(x) = 2x 个
- 模式 δ：补偿脉冲 f(x) = 2x + 1 个

其中 x 为机床传感器读取的热偏置值。校准期间，基准热偏置 H 与补偿曲线模式锁定不变。

工程师的目标是通过采样获取机床真实的补偿模式（α、β、γ 或 δ）并测算出基准热偏置 H 的确切值。

提供以下两种设备校准指令：

1. **恒温舱测试（已知自变量查询）**：向数控中心直接注入标准的模拟热偏置值 t，获取系统生成的补偿脉冲数 f(t)。
2. **车间工况测试（隐藏自变量平移查询）**：在当前真实车间环境下，利用人工热源叠加附加偏置 c。系统将依据传感器感知的总热偏置（H + c）输出此时的补偿脉冲数 f(H + c)。

请运用最优策略，以最少指令得出结论。

每次指令只允许包含一个标签，使用以下 XML 格式：

- 恒温舱测试（例如输入偏置 t=3）：
<query_known>3</query_known>

- 车间工况测试（例如叠加偏置 c=2）：
<query_hidden>2</query_hidden>

确认无误后，写入补偿模式（α、β、γ 或 δ）与基准热偏置 H，格式如下：

<answer>mode=α, H=5</answer>

- 输入数据须严格遵守非负整数限制，否则判定为异常指令。
- 累计产生两次异常指令会导致保护性停机。
- 最终写入错误的参数或格式有误，校准即告失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Initiating the "CNC Machine Thermal Deformation Compensation Calibration" procedure.

Affected by the workshop environment, the machine has an unknown baseline environmental thermal bias H (microns, non-negative integer). Concurrently, the compensation pulse calculation curve f for the servo motor is unknown, matching one of four modes:
- Mode α: Compensation pulse f(x) = x
- Mode β: Compensation pulse f(x) = x + 1
- Mode γ: Compensation pulse f(x) = 2x
- Mode δ: Compensation pulse f(x) = 2x + 1

where x is the thermal bias read by sensors. During calibration, the baseline bias H and the compensation curve mode are strictly locked.

Your objective as an engineer is to deduce the machine's actual compensation mode (α, β, γ, or δ) and calculate the exact value of the baseline thermal bias H via sampling.

You can issue the following two calibration commands:

1. **Thermostatic Chamber Test (Known Argument Query)**: Inject a standard simulated thermal bias t directly into the CNC center to get the generated compensation pulse f(t).
2. **Workshop Condition Test (Hidden Argument Shift Query)**: Use an artificial heat source to superimpose an additional bias c in the real environment. The system outputs the compensation pulse f(H + c) based on the total sensed bias.

Employ the optimal strategy to conclude with minimal commands.

Each command must contain only one tag in the following XML format:

- Thermostatic Chamber Test (e.g., input bias t=3):
<query_known>3</query_known>

- Workshop Condition Test (e.g., superimposed bias c=2):
<query_hidden>2</query_hidden>

Once confirmed, write the compensation mode and the baseline thermal bias H into the system:

<answer>mode=α, H=5</answer>

- Input data must strictly be non-negative integers; otherwise, they are marked as anomalous commands.
- Two anomalous commands will trigger an emergency halt.
- Submitting incorrect parameters or invalid formats will result in calibration failure.
"""

    contextualized_rule_zh_5 = """\
欢迎接入“司法量刑辅助系统规则核查”模块。

经脱敏处理，当前卷宗中嫌疑人存在未知的犯罪涉案基准单位 H（非负整数）。同时，系统挂载的罚金附加核算模型 f 版本未知，仅确认属于以下四种法定计算指导模式之一：
- 模式 α：核算罚金 f(x) = x 万元
- 模式 β：核算罚金 f(x) = x + 1 万元
- 模式 γ：核算罚金 f(x) = 2x 万元
- 模式 δ：核算罚金 f(x) = 2x + 1 万元

其中 x 为代入计算的涉案单位数。在核查期间，卷宗基础事实 H 及指导模式将锁定不变。

稽查人员需通过系统试算，反向推断出当前采用的指导模式（α、β、γ 或 δ）以及嫌疑人的涉案基准单位 H。

系统支持两种数据探询接口：

1. **沙盒基准模拟（已知自变量查询）**：输入预设的案值单位 t，接口直接返回对应的系统建议罚金 f(t)。
2. **案情情节累加（隐藏自变量平移查询）**：基于真实案卷数据，虚拟追加 c 个单位的加重情节基数。系统将对累加后的总基数（H + c）进行量刑试算，返回建议罚金 f(H + c)。此操作不修改真实卷宗。

请规划最优的质询逻辑，精简接口调用次数。

单次请求仅限使用一个标签，参照以下 XML 格式规范：

- 沙盒基准模拟（例如输入案值 t=3）：
<query_known>3</query_known>

- 案情情节累加（例如追加情节基数 c=2）：
<query_hidden>2</query_hidden>

得出结论后，按规定格式提交指导模式（α、β、γ 或 δ）和案卷基准单位 H：

<answer>mode=α, H=5</answer>

- 所有试算输入参数必须是合规的非负整数，否则请求将被阻断。
- 累计产生两次非法阻断将被强制吊销核查权限。
- 结论数据失实或格式违规将导致本轮核查被判定无效。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Judicial Sentencing Auxiliary System Rule Verification" module.

After desensitization, the current dossier indicates an unknown baseline unit of crime involvement H (non-negative integer) for the suspect. Meanwhile, the version of the supplementary fine calculation model f attached to the system is unknown, but confirmed to follow one of four statutory sentencing guideline modes:
- Mode α: Calculated fine f(x) = x (in ten thousand yuan)
- Mode β: Calculated fine f(x) = x + 1 (in ten thousand yuan)
- Mode γ: Calculated fine f(x) = 2x (in ten thousand yuan)
- Mode δ: Calculated fine f(x) = 2x + 1 (in ten thousand yuan)

where x is the input involvement unit. During the verification, the foundational dossier fact H and the guideline mode remain firmly locked.

Auditors must utilize system trial calculations to reversely deduce the currently applied guideline mode (α, β, γ, or δ) and the suspect's baseline unit H.

The system provides two data inquiry interfaces:

1. **Sandbox Baseline Simulation (Known Argument Query)**: Input a preset case value unit t. The interface returns the corresponding suggested fine f(t).
2. **Case Circumstance Accumulation (Hidden Argument Shift Query)**: Based on the true dossier data, virtually add c units of aggravating circumstances. The system performs a sentencing trial on the accumulated total (H + c) and returns the suggested fine f(H + c). This does not modify the true dossier.

Plan the optimal inquiry logic to minimize interface calls.

A single request may only contain one tag, adhering to the following XML formatting standard:

- Sandbox Baseline Simulation (e.g., input value t=3):
<query_known>3</query_known>

- Case Circumstance Accumulation (e.g., adding circumstance base c=2):
<query_hidden>2</query_hidden>

Once derived, submit the guideline mode and the dossier baseline unit H in the prescribed format:

<answer>mode=α, H=5</answer>

- All input trial parameters must be compliant non-negative integers; otherwise, the request is blocked.
- Two illicit blocks will forcefully revoke verification access.
- Inaccurate conclusions or formatting violations will render this verification invalid.
"""

    tags = ["answer", "query_known", "query_hidden"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "mode": "α",
                "H": 3,
            },
            2: {
                "mode": "β",
                "H": 5,
            },
            3: {
                "mode": "γ",
                "H": 4,
            },
            4: {
                "mode": "δ",
                "H": 7,
            },
            5: {
                "mode": "γ",
                "H": 10,
            },
        },
        "en": {
            1: {
                "mode": "α",
                "H": 3,
            },
            2: {
                "mode": "β",
                "H": 5,
            },
            3: {
                "mode": "γ",
                "H": 4,
            },
            4: {
                "mode": "δ",
                "H": 7,
            },
            5: {
                "mode": "γ",
                "H": 10,
            },
        },
    }

    def __init__(self, config):
        self.invalid_query_count = 0
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.mode = cfg["mode"]
        self.H = cfg["H"]
        
        self._game_info = {}

    def _apply_function(self, x):
        if self.mode == "α":
            return x
        elif self.mode == "β":
            return x + 1
        elif self.mode == "γ":
            return 2 * x
        elif self.mode == "δ":
            return 2 * x + 1
        else:
            raise ValueError(f"Unknown mode: {self.mode}")

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        raw_ans = raw_ans.replace("，", ",")
        
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip().lower()] = v.strip()
        
        if "mode" not in ans_dict or "h" not in ans_dict:
            return False
        
        mode_map = {
            "α": "α", "alpha": "α", "a": "α",
            "β": "β", "beta": "β", "b": "β",
            "γ": "γ", "gamma": "γ", "c": "γ", "g": "γ",
            "δ": "δ", "delta": "δ", "d": "δ",
        }
        
        submitted_mode = ans_dict["mode"].lower().strip()
        normalized_mode = mode_map.get(submitted_mode, submitted_mode)
        
        if normalized_mode != self.mode:
            return False
        
        try:
            model_H = int(ans_dict["h"])
        except (ValueError, TypeError):
            return False
            
        return model_H == self.H

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            invalid_msg = "无效查询，请按规则输入。"
        else:
            invalid_msg = "Invalid query. Please follow the rules."

        if "query_known" in parsed_info:
            try:
                t = parsed_info["query_known"].strip()
                t_val = int(t)
                if t_val < 0:
                    self.invalid_query_count += 1
                    if self.invalid_query_count >= 2:
                        raise ValueError("Two invalid queries detected.")
                    return invalid_msg
                
                result = self._apply_function(t_val)
                return str(result)
            except ValueError as e:
                if "Two invalid queries" in str(e):
                    raise
                self.invalid_query_count += 1
                if self.invalid_query_count >= 2:
                    raise ValueError("Two invalid queries detected.")
                return invalid_msg

        elif "query_hidden" in parsed_info:
            try:
                c = parsed_info["query_hidden"].strip()
                c_val = int(c)
                if c_val < 0:
                    self.invalid_query_count += 1
                    if self.invalid_query_count >= 2:
                        raise ValueError("Two invalid queries detected.")
                    return invalid_msg
                
                result = self._apply_function(self.H + c_val)
                return str(result)
            except ValueError as e:
                if "Two invalid queries" in str(e):
                    raise
                self.invalid_query_count += 1
                if self.invalid_query_count >= 2:
                    raise ValueError("Two invalid queries detected.")
                return invalid_msg

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        try:
            val = int(correct)
            return str(val + 1)
        except ValueError:
            pass

        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        else:
            if "Yes" in correct:
                return correct.replace("Yes", "No")
            elif "yes" in correct:
                return correct.replace("yes", "no")
            elif "No" in correct:
                return correct.replace("No", "Yes")
            elif "no" in correct:
                return correct.replace("no", "yes")
        
        return correct + "_WRONG"

    def get_all_possible_queries(self):
        queries = []
        range_limit = 20

        for t in range(range_limit):
            query_content = f"<query_known>{t}</query_known>"
            ans = str(self._apply_function(t))
            queries.append({"query": query_content, "answer": ans})
        
        for c in range(range_limit):
            query_content = f"<query_hidden>{c}</query_hidden>"
            ans = str(self._apply_function(self.H + c))
            queries.append({"query": query_content, "answer": ans})

        return queries