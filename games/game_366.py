import random
import itertools
from .base import Game

class EquivalenceRelationGame(Game):

    game_rule_zh = """\
我们现在来玩一个"等价类推理"游戏，规则如下：

游戏设定了一个包含 {n} 个对象的集合，对象编号为 1 到 {n}。我已秘密地将这些对象划分成若干个等价类（至少 2 个），每个等价类包含一个或多个对象。同一等价类内的对象彼此等价，不同等价类的对象不等价。

你的目标是判断两个指定的目标对象（编号 {target_x} 和 {target_y}）是否属于同一个等价类。

为了帮助你推理，你可以向我提出"三元查询"。每次查询需要指定三个不同的对象编号 a, b, c，我会根据它们在等价类中的关系返回以下三种结果之一：

1. 返回"1"：三个对象 a, b, c 属于同一个等价类。
2. 返回"2"：三个对象中恰有两个属于同一等价类，另一个属于不同的等价类。
3. 返回"3"：三个对象 a, b, c 分别属于三个不同的等价类。

你应该尽可能少地使用查询次数，收集足够信息后提交最终答案。若答案错误或格式不符，游戏失败。

每次询问必须包含恰好三个不同的对象编号，使用以下 XML 格式：

- 三元查询（例如查询编号 1, 3, 5 的关系）：
<query>1,3,5</query>

提交最终答案时，必须说明目标对象 {target_x} 和 {target_y} 的关系，使用以下格式：

- 如果判断它们属于同一等价类：
<answer>SAME</answer>

- 如果判断它们属于不同等价类：
<answer>DIFFERENT</answer>
"""

    game_rule_en = """\
Let's play an "Equivalence Class Reasoning" game. Here are the rules:

There is a set of {n} objects, numbered from 1 to {n}. I have secretly partitioned these objects into several equivalence classes (at least 2 classes). Each equivalence class contains one or more objects. Objects within the same equivalence class are equivalent to each other, while objects in different equivalence classes are not equivalent.

Your goal is to determine whether two specified target objects (ID {target_x} and ID {target_y}) belong to the same equivalence class.

To help you reason, you can ask me "ternary queries". Each query specifies three distinct object IDs a, b, c, and I will return one of the following three results based on their equivalence class relationships:

1. Return "1": All three objects a, b, c belong to the same equivalence class.
2. Return "2": Exactly two of the three objects belong to the same equivalence class, and the third belongs to a different equivalence class.
3. Return "3": The three objects a, b, c belong to three different equivalence classes.

You should use as few queries as possible, collect enough information, and then submit your final answer. If the answer is wrong or the format is invalid, the game is a failure.

Each query must contain exactly three distinct object IDs, using the following XML format:

- Ternary Query (e.g., querying the relationship among IDs 1, 3, 5):
<query>1,3,5</query>

When submitting the final answer, specify the relationship between target objects {target_x} and {target_y}, using the following format:

- If you determine they belong to the same equivalence class:
<answer>SAME</answer>

- If you determine they belong to different equivalence classes:
<answer>DIFFERENT</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用城市轨道交通网络票务稽查系统。

系统当前载入了包含 {n} 个独立站点的路网数据，站点编号为 1 到 {n}。出于计费目的，这些站点已被秘密划分到若干个“票价计费区”（至少 2 个），每个计费区包含一个或多个站点。同属一个计费区的站点之间属于平级换乘（即视为同区），而跨越不同计费区的站点则属于不同的票价梯度。

你的目标是核查：目标站点（编号 {target_x}）和目标站点（编号 {target_y}）是否被归入同一个票价计费区。

为了排查系统配置，你可以发起“三站比对查询”。每次查询需提供三个不同的站点编号 a, b, c，系统将根据它们的区划关系返回以下三种稽查结果之一：

1. 返回"1"：三个站点均同属一个票价计费区。
2. 返回"2"：三个站点中有恰好两个同属一个计费区，另一个在不同计费区。
3. 返回"3"：三个站点分别处于三个完全不同的计费区。

你应以最少的查询次数完成信息收集，并提交最终稽查结论。若结论错误或格式不符，稽查任务失败。

每次询问必须包含恰好三个不同的站点编号，使用以下 XML 格式：

- 三元查询（例如比对编号 1, 3, 5 站点的关系）：
<query>1,3,5</query>

提交最终答案时，必须说明目标站点 {target_x} 和 {target_y} 的区划关系：

- 如果判断它们同属一个计费区：
<answer>SAME</answer>

- 如果判断它们分属不同计费区：
<answer>DIFFERENT</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the Urban Rail Transit Fare Zone Auditing System.

The system has loaded network data comprising {n} independent stations, numbered 1 to {n}. For billing purposes, these stations have been secretly partitioned into several "fare zones" (at least 2). Each fare zone contains one or more stations. Stations within the same fare zone allow flat-rate transfers (equivalent), while stations in different fare zones incur gradient pricing.

Your goal is to verify whether Target Station {target_x} and Target Station {target_y} are classified into the same fare zone.

To troubleshoot the configuration, you can initiate "Ternary Station Queries". Each query requires three distinct station IDs (a, b, c), and the system will return one of the following three audit results based on their zone relationship:

1. Return "1": All three stations belong to the same fare zone.
2. Return "2": Exactly two of the three stations belong to the same fare zone, while the third is in a different zone.
3. Return "3": All three stations belong to three entirely different fare zones.

You should collect enough information using as few queries as possible, then submit your final audit conclusion. Incorrect answers or invalid formats will result in a failed audit.

Each query must contain exactly three distinct station IDs, using the following XML format:

- Ternary Query (e.g., comparing relationship among stations 1, 3, 5):
<query>1,3,5</query>

When submitting your final answer, specify the zoning relationship between target stations {target_x} and {target_y}:

- If you determine they belong to the same fare zone:
<answer>SAME</answer>

- If you determine they belong to different fare zones:
<answer>DIFFERENT</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用临床病原体基因组同源性分析系统。

我们当前收集了 {n} 份未知病原体样本，样本编号为 1 到 {n}。经过初步测序，这些样本被划分成了若干个独立的“基因簇”（至少 2 个簇）。同属一个基因簇的样本代表它们来自同一变异株（同源等价），而属于不同基因簇的样本则代表不同的变异株。

你的目标是鉴定：核心目标样本 {target_x} 和 {target_y} 是否属于同一个基因簇。

为了进行溯源，你可以向系统提交“三样本交叉测定”。每次测定需要指定三个不同的样本编号 a, b, c，系统会反馈以下三种同源性分析结果之一：

1. 返回"1"：三个样本均同属一个基因簇。
2. 返回"2"：三个样本中有恰好两个属于同一基因簇，另一个属于不同基因簇。
3. 返回"3"：三个样本分别属于三个完全不同的基因簇。

请尽可能高效地使用测定次数，查明变异情况并提交最终报告。如果判断错误或格式违规，分析任务将判定失败。

每次询问必须包含恰好三个不同的样本编号，使用以下 XML 格式：

- 三元查询（例如测定样本 1, 3, 5 的关系）：
<query>1,3,5</query>

提交最终答案时，必须说明目标样本 {target_x} 和 {target_y} 的同源关系：

- 如果判断它们属于同一个基因簇：
<answer>SAME</answer>

- 如果判断它们属于不同基因簇：
<answer>DIFFERENT</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the Clinical Pathogen Genomic Homology Analysis System.

We have collected {n} unknown pathogen samples, numbered 1 to {n}. Through preliminary sequencing, these samples have been secretly partitioned into several independent "genomic clusters" (at least 2 clusters). Samples within the same cluster represent the same variant strain (homologously equivalent), whereas samples in different clusters represent different variant strains.

Your goal is to determine whether core Target Sample {target_x} and Target Sample {target_y} belong to the same genomic cluster.

To trace the source, you can submit "Ternary Sample Cross-tests". Each test requires three distinct sample IDs (a, b, c), and the system will return one of the following three homology results:

1. Return "1": All three samples belong to the same genomic cluster.
2. Return "2": Exactly two of the three samples belong to the same genomic cluster, while the third belongs to a different cluster.
3. Return "3": All three samples belong to three entirely different genomic clusters.

Please use testing efficiently, identify the variant mapping, and submit your final report. Incorrect judgments or formatting violations will lead to a failed analysis.

Each test must contain exactly three distinct sample IDs, using the following XML format:

- Ternary Query (e.g., testing the relationship among samples 1, 3, 5):
<query>1,3,5</query>

When submitting the final answer, specify the homologous relationship between target samples {target_x} and {target_y}:

- If you determine they belong to the same genomic cluster:
<answer>SAME</answer>

- If you determine they belong to different genomic clusters:
<answer>DIFFERENT</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用标准化考试盲评防弊核查系统。

系统数据库中目前存有 {n} 份已批改的匿名答卷，试卷编号为 1 到 {n}。为了防止阅卷偏差，这些试卷在后台被秘密分配给了若干个不同的“阅卷组”（至少 2 个组），每个阅卷组负责批改一份或多份试卷。同一阅卷组批改的试卷遵循完全相同的评分尺度（等价），而不同阅卷组批改的试卷评分尺度不同。

你的目标是核对：重点抽检试卷 {target_x} 和 试卷 {target_y} 是否是由同一个阅卷组进行批改的。

你可以向考务系统发起“三卷横评查询”。每次查询提供三个不同的试卷编号 a, b, c，系统将校验它们的批改记录并返回以下三种结果之一：

1. 返回"1"：三份试卷均由同一个阅卷组批改。
2. 返回"2"：三份试卷中恰有两份由同一个阅卷组批改，另一份由其他阅卷组批改。
3. 返回"3"：三份试卷分别由三个完全不同的阅卷组进行批改。

请以最少的查询次数查明评分分布，并提交你的最终核查结论。若提交错误或格式不符，防弊核查将被判定失败。

每次询问必须包含恰好三个不同的试卷编号，使用以下 XML 格式：

- 三元查询（例如抽查试卷 1, 3, 5 的阅卷组关系）：
<query>1,3,5</query>

提交最终答案时，必须说明目标试卷 {target_x} 和 {target_y} 的批改关系：

- 如果判断它们由同一个阅卷组批改：
<answer>SAME</answer>

- 如果判断它们由不同阅卷组批改：
<answer>DIFFERENT</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Standardized Exam Blind-Marking Anti-Bias Verification System.

The system database currently holds {n} graded anonymous examination papers, numbered 1 to {n}. To prevent grading bias, these papers were secretly assigned to several different "marking panels" (at least 2 panels) in the backend. Papers marked by the same panel are subject to an identical scoring rubric (equivalent), while papers marked by different panels have divergent rubrics.

Your goal is to verify whether Spotlight Paper {target_x} and Paper {target_y} were marked by the exact same marking panel.

You can initiate "Ternary Paper Cross-reviews" with the exam system. Each review requires three distinct paper IDs (a, b, c). The system will check their grading records and return one of the following three results:

1. Return "1": All three papers were marked by the same marking panel.
2. Return "2": Exactly two of the three papers were marked by the same marking panel, while the third was marked by a different panel.
3. Return "3": All three papers were marked by three entirely different marking panels.

Please utilize your queries efficiently to map out the grading distribution and submit your final verification conclusion. If the conclusion is wrong or incorrectly formatted, the anti-bias audit fails.

Each review must contain exactly three distinct paper IDs, using the following XML format:

- Ternary Query (e.g., cross-reviewing papers 1, 3, 5):
<query>1,3,5</query>

When submitting your final answer, specify the grading relationship between target papers {target_x} and {target_y}:

- If you determine they were marked by the same marking panel:
<answer>SAME</answer>

- If you determine they were marked by different marking panels:
<answer>DIFFERENT</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎使用精密制造产线质量溯源系统。

目前质检台上放置了 {n} 个同批次生产的机械零件，零件编号为 1 到 {n}。由于生产负荷，这些零件实际上是由若干个不同的“成型模具”（至少 2 个）并行压铸出来的。由同一个模具压铸出来的零件具有极高的公差一致性（视为等价），而不同模具出来的零件则存在微小的特征差异。

你的任务是进行质量溯源，判断：抽样零件 {target_x} 和 零件 {target_y} 是否由同一个成型模具压铸而成。

在不破坏零件的前提下，你可以向光学检测仪下达“三件干涉扫描”指令。每次指令需放入三个不同的零件编号 a, b, c，仪器将计算它们的表面干涉条纹并返回三种结果之一：

1. 返回"1"：三个零件均由同一个模具压铸而成。
2. 返回"2"：三个零件中恰有两个来自同一个模具，另一个来自不同的模具。
3. 返回"3"：三个零件分别来自三个完全不同的模具。

请尽量减少扫描仪的占用次数，分析出模具的对应关系并提交最终的溯源结论。结论错误或输入格式不规范将导致溯源流程中断。

每次询问必须包含恰好三个不同的零件编号，使用以下 XML 格式：

- 三元查询（例如扫描零件 1, 3, 5 的模具关系）：
<query>1,3,5</query>

提交最终答案时，必须说明目标零件 {target_x} 和 {target_y} 的制造关系：

- 如果判断它们由同一个模具压铸而成：
<answer>SAME</answer>

- 如果判断它们由不同模具压铸而成：
<answer>DIFFERENT</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the Precision Manufacturing Production Line Quality Traceability System.

There are currently {n} mechanical parts from the same production batch placed on the inspection bench, numbered 1 to {n}. Due to production loads, these parts were actually die-cast in parallel by several different "forming molds" (at least 2 molds). Parts cast by the same mold share extremely high tolerance consistency (equivalent), while parts from different molds possess microscopic feature discrepancies.

Your task is to conduct quality traceability and determine whether Sample Part {target_x} and Part {target_y} were die-cast by the exact same forming mold.

Without performing destructive testing, you can issue a "Ternary Interference Scan" command to the optical inspector. Each command requires three distinct part IDs (a, b, c). The instrument will calculate their surface interference fringes and return one of the following three results:

1. Return "1": All three parts were cast by the same mold.
2. Return "2": Exactly two of the three parts come from the same mold, and the third from a different mold.
3. Return "3": All three parts come from three entirely different molds.

Please minimize scanner usage, analyze the mold correspondences, and submit your final traceability conclusion. An incorrect conclusion or improper input format will cause the traceability process to abort.

Each scan command must contain exactly three distinct part IDs, using the following XML format:

- Ternary Query (e.g., scanning parts 1, 3, 5):
<query>1,3,5</query>

When submitting your final answer, specify the manufacturing relationship between target parts {target_x} and {target_y}:

- If you determine they were cast by the same mold:
<answer>SAME</answer>

- If you determine they were cast by different molds:
<answer>DIFFERENT</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用反洗钱与企业穿透式股权审计系统。

案卷中列出了 {n} 家存在资金往来的可疑注册企业，代号为 1 到 {n}。审计局初步查明，这些空壳公司背后实际上是被若干个隐藏的“最终实际控制人”（至少 2 个实控人）所分别操纵的。受同一个实际控制人操纵的企业在资本运作上互为关联方（视为等价实体），而受不同控制人操纵的企业则属于独立的利益集团。

你的审计目标是穿透公司外壳，查明：目标企业 {target_x} 和 目标企业 {target_y} 是否受同一个最终实际控制人操纵。

为了收集证据，你可以向金融数据中心提交“三方资金链路排查”。每次排查需提交三个不同的企业代号 a, b, c，系统会根据底层流水关系返回以下三种审计反馈：

1. 返回"1"：三家企业均受同一个实际控制人操纵。
2. 返回"2"：三家企业中恰有两家受同一个实控人操纵，另一家受不同实控人操纵。
3. 返回"3"：三家企业分别受三个完全不同的实际控制人操纵。

你必须利用最少的排查额度拼凑出资本控制网络，并提交最终的审计判定。若判定失误或格式有误，结案将被驳回。

每次询问必须包含恰好三个不同的企业代号，使用以下 XML 格式：

- 三元查询（例如排查企业 1, 3, 5 的实控关系）：
<query>1,3,5</query>

提交最终答案时，必须说明目标企业 {target_x} 和 {target_y} 的关联关系：

- 如果判断它们受同一个实际控制人操纵：
<answer>SAME</answer>

- 如果判断它们受不同实际控制人操纵：
<answer>DIFFERENT</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the Anti-Money Laundering and Corporate Veil Piercing Audit System.

The case file lists {n} suspicious registered shell companies with mutual fund transfers, codenamed 1 to {n}. The audit bureau has preliminarily determined that these companies are actually manipulated by several hidden "Ultimate Beneficial Owners" (UBOs, at least 2). Companies manipulated by the same UBO are affiliated parties in capital operations (equivalent entities), whereas companies manipulated by different UBOs belong to independent interest groups.

Your audit objective is to pierce the corporate veil and determine whether Target Company {target_x} and Company {target_y} are manipulated by the exact same UBO.

To gather evidence, you can submit a "Ternary Financial Linkage Probe" to the financial data center. Each probe requires three distinct company codes (a, b, c), and the system will return one of the following three audit feedbacks based on underlying transaction flows:

1. Return "1": All three companies are manipulated by the same UBO.
2. Return "2": Exactly two of the three companies are manipulated by the same UBO, while the third is controlled by a different UBO.
3. Return "3": All three companies are manipulated by three completely different UBOs.

You must utilize your limited probe quota to piece together the capital control network and submit your final audit ruling. If the ruling is inaccurate or improperly formatted, the case closure will be rejected.

Each probe must contain exactly three distinct company codes, using the following XML format:

- Ternary Query (e.g., probing the control relationship of companies 1, 3, 5):
<query>1,3,5</query>

When submitting your final answer, specify the affiliation between target companies {target_x} and {target_y}:

- If you determine they are manipulated by the same UBO:
<answer>SAME</answer>

- If you determine they are manipulated by different UBOs:
<answer>DIFFERENT</answer>
"""

    tags = ["answer", "query"]
    
    reasoning_type = "归纳推理"
    data_structure = "集合"

    DIFFICULTY_CONFIG = {
        1: {
            "n": 5,
            "partition": [[1, 2, 3], [4, 5]],
            "target_x": 1,
            "target_y": 4,
        },
        2: {
            "n": 7,
            "partition": [[1, 2], [3, 4, 5], [6, 7]],
            "target_x": 3,
            "target_y": 5,
        },
        3: {
            "n": 9,
            "partition": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            "target_x": 2,
            "target_y": 8,
        },
        4: {
            "n": 10,
            "partition": [[1, 2], [3, 4], [5, 6, 7], [8, 9, 10]],
            "target_x": 5,
            "target_y": 7,
        },
        5: {
            "n": 12,
            "partition": [[1, 2, 3], [4, 5], [6, 7, 8], [9, 10, 11, 12]],
            "target_x": 2,
            "target_y": 10,
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["target_x"] = cfg["target_x"]
        self._game_info["target_y"] = cfg["target_y"]
        
        self.obj_to_class = {}
        for class_idx, members in enumerate(cfg["partition"]):
            for obj_id in members:
                self.obj_to_class[obj_id] = class_idx
        
        self.target_x = cfg["target_x"]
        self.target_y = cfg["target_y"]
        
        self.correct_answer = "SAME" if self.obj_to_class[self.target_x] == self.obj_to_class[self.target_y] else "DIFFERENT"

    def _check_same_class(self, a, b):
        return self.obj_to_class[a] == self.obj_to_class[b]

    def _query_ternary(self, a, b, c):
        class_a = self.obj_to_class[a]
        class_b = self.obj_to_class[b]
        class_c = self.obj_to_class[c]
        
        unique_classes = len(set([class_a, class_b, class_c]))
        
        if unique_classes == 1:
            return "1"
        elif unique_classes == 2:
            return "2"
        else:
            return "3"

    def evaluate(self, parsed_info):
        answer = parsed_info["answer"].strip().upper()
        
        if answer not in ["SAME", "DIFFERENT"]:
            return False
        
        return answer == self.correct_answer

    def _cf_core_produce(self, parsed_info):
        if "query" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        raw_query = parsed_info["query"].strip()
        
        try:
            ids = [int(x.strip()) for x in raw_query.split(",")]
            
            if len(ids) != 3:
                if self.config.language == "zh":
                    return "错误：查询必须包含恰好三个对象编号。"
                else:
                    return "Error: Query must contain exactly three object IDs."
            
            if len(set(ids)) != 3:
                if self.config.language == "zh":
                    return "错误：查询的三个对象编号必须两两不同。"
                else:
                    return "Error: The three object IDs must be distinct."
            
            a, b, c = ids
            
            n = self._game_info["n"]
            if not all(1 <= obj_id <= n for obj_id in [a, b, c]):
                if self.config.language == "zh":
                    return f"错误：对象编号必须在 1 到 {n} 之间。"
                else:
                    return f"Error: Object IDs must be between 1 and {n}."
            
            result = self._query_ternary(a, b, c)
            return result
            
        except ValueError:
            if self.config.language == "zh":
                return "错误：查询格式无效，请使用逗号分隔的三个整数编号。"
            else:
                return "Error: Invalid query format. Please use three comma-separated integer IDs."
        except Exception as e:
            if self.config.language == "zh":
                return f"错误：{str(e)}"
            else:
                return f"Error: {str(e)}"

    def _cf_make_wrong(self, correct):
        possible = ["1", "2", "3"]
        wrong_choices = [v for v in possible if v != correct]
        return random.choice(wrong_choices)

    def get_all_possible_queries(self) -> list[dict]:
        n = self._game_info["n"]
        results = []
        
        for combo in itertools.combinations(range(1, n + 1), 3):
            a, b, c = combo
            ans = self._query_ternary(a, b, c)
            
            results.append({
                "query": f"<query>{a},{b},{c}</query>",
                "answer": ans
            })
            
        return results