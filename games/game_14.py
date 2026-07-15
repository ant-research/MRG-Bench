from .base import Game
import re
import random

class HiddenInsertionGame(Game):
    tags = ["query_1", "query_2", "answer"]
    reasoning_type = "演绎推理"
    data_structure = "序列"

    game_rule_zh = """\
我们现在来玩一个"隐藏插入推理"游戏，规则如下：

游戏设定了一个初始序列，长度为 {n}，包含编号为 B1, B2, ..., B{n} 的元素，初始顺序为 [B1, B2, ..., B{n}]。

接下来，我秘密地执行了 {m} 次插入操作。每次插入会在当前序列的某个位置插入一个新元素（命名为 N1, N2, ..., N{m}），使得该位置及其右侧的所有元素索引整体加 1。所有插入操作的位置和顺序已固定，但对你不可见。

定义"时间步 r"为已完成前 r 次插入后的序列状态：
- r=0 表示初始状态，序列长度为 {n}
- r={m} 表示最终状态，序列长度为 {total}

你的目标是：推断出在最终状态（r={m}）下，第 {target} 位上的元素是什么。

你可以反复提出以下两类查询（每次仅限一项）：
1. <query_1>r, p</query_1>：查询在时间步 r 下，位置 p 上的元素是什么。
2. <query_2>r, E</query_2>：查询在时间步 r 下，元素 E 所在的位置。

注意：
- r 的范围是 0 到 {m}。
- p 的范围是 1 到 {n} + r。
- E 可以是 B1~B{n} 或 N1~N{m}。

当你得出结论后，请用 <answer>E</answer> 来提交你的最终答案，其中 E 是最终状态下第 {target} 位上的元素。
"""

    game_rule_en = """\
Let's play a "Hidden Insertion Reasoning" game. The rules are as follows:

The game sets an initial sequence of length {n}, containing elements labeled B1, B2, ..., B{n}, with the initial order being [B1, B2, ..., B{n}].

Next, I secretly performed {m} insertion operations. Each insertion places a new element (named N1, N2, ..., N{m}) at a certain position in the current sequence, shifting all elements at that position and to its right by 1 to the right. The positions and order of all insertion operations are fixed but invisible to you.

Define "time step r" as the sequence state after completing the first r insertions:
- r=0 represents the initial state, sequence length is {n}
- r={m} represents the final state, sequence length is {total}

Your goal is: deduce what element is at position {target} in the final state (r={m}).

You can repeatedly make the following two types of queries (only one per turn):
1. <query_1>r, p</query_1>: Query what element is at position p at time step r.
2. <query_2>r, E</query_2>: Query the position of element E at time step r.

Note:
- r ranges from 0 to {m}.
- p ranges from 1 to {n} + r.
- E can be B1~B{n} or N1~N{m}.

Once you have reached a conclusion, please submit your final answer using <answer>E</answer>, where E is the element at position {target} in the final state.
"""

    contextualized_rule_zh_1 = """\
【交通场景】
我们现在来进行一项“交通枢纽列车调度”推理测试。

系统设有一条主干铁路，初始长度对应 {n} 个区段，停放着列车 B1, B2, ..., B{n}，初始排列为 [B1, B2, ..., B{n}]。

在后续的调度周期中，系统自动执行了 {m} 次加塞调度。每次加塞会将一列新列车（命名为 N1, N2, ..., N{m}）插入到当前主干铁路的某个区段，使得该区段及后方的所有列车顺延退后一个区段。所有加塞调度已执行完毕且在后台固定，但对你不可见。

定义“调度阶段 r”为完成前 r 次加塞后的铁路区段状态：
- r=0 表示初始状态，占用区段数为 {n}
- r={m} 表示最终状态，占用区段数为 {total}

你的目标是：推断出在最终状态（r={m}）下，第 {target} 个区段上的列车编号是什么。

你可以反复提出以下两类查询（每次仅限一项）：
1. <query_1>r, p</query_1>：查询在调度阶段 r 下，第 p 个区段的列车编号。
2. <query_2>r, E</query_2>：查询在调度阶段 r 下，列车 E 所在的区段。

注意：
- r 的范围是 0 到 {m}。
- p 的范围是 1 到 {n} + r。
- E 可以是 B1~B{n} 或 N1~N{m}。

当你确认目标后，请用 <answer>E</answer> 来提交答案，其中 E 是最终状态下第 {target} 个区段上的列车编号。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
We are now conducting a "Traffic Hub Train Scheduling" reasoning test.

The system features a main railway initially spanning {n} segments, occupied by trains B1, B2, ..., B{n} in the initial order [B1, B2, ..., B{n}].

During subsequent dispatch cycles, the system automatically executed {m} insertion dispatchments. Each dispatch inserts a new train (named N1, N2, ..., N{m}) into a specific segment of the current main railway, causing all trains at and behind that segment to shift back by one segment. All dispatchments have been executed and fixed in the backend, but are invisible to you.

Define "dispatch phase r" as the railway segment state after completing the first r insertions:
- r=0 represents the initial state, occupied segments count is {n}
- r={m} represents the final state, occupied segments count is {total}

Your goal is: deduce the train ID at the {target}-th segment in the final state (r={m}).

You can repeatedly make the following two types of queries (only one per turn):
1. <query_1>r, p</query_1>: Query the train ID at segment p during dispatch phase r.
2. <query_2>r, E</query_2>: Query the segment occupied by train E during dispatch phase r.

Note:
- r ranges from 0 to {m}.
- p ranges from 1 to {n} + r.
- E can be B1~B{n} or N1~N{m}.

Once you confirm your target, please submit your answer using <answer>E</answer>, where E is the train ID at the {target}-th segment in the final state.
"""

    contextualized_rule_zh_2 = """\
【医疗场景】
我们现在来进行一项“基因片段拼接”推理分析。

患者样本中提取出了一段初始基因序列，长度为 {n}，包含碱基片段 B1, B2, ..., B{n}，初始序列结构为 [B1, B2, ..., B{n}]。

随后，在病毒感染模拟中，系统发生 {m} 次靶向重组插入。每次插入会将一个新的突变片段（命名为 N1, N2, ..., N{m}）嵌入到当前序列的特定位点，导致该位点及其下游的所有片段位置向后平移 1 位。所有的插入重组已发生且位置恒定，但对分析员隐蔽。

定义“重组代次 r”为发生前 r 次插入后的序列状态：
- r=0 表示野生型初始状态，片段长度为 {n}
- r={m} 表示最终感染状态，片段长度为 {total}

你的目标是：推断出在最终状态（r={m}）下，第 {target} 号位点上的片段编号是什么。

你可以反复提出以下两类查询（每次仅限一项）：
1. <query_1>r, p</query_1>：查询在重组代次 r 下，第 p 号位点的片段编号。
2. <query_2>r, E</query_2>：查询在重组代次 r 下，片段 E 所在的位点。

注意：
- r 的范围是 0 到 {m}。
- p 的范围是 1 到 {n} + r。
- E 可以是 B1~B{n} 或 N1~N{m}。

当你得出结论后，请用 <answer>E</answer> 来提交诊断结果，其中 E 是最终状态下第 {target} 号位点上的片段编号。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
We are now conducting a "Gene Fragment Splicing" reasoning analysis.

An initial gene sequence has been extracted from the patient sample, with a length of {n}, containing base fragments B1, B2, ..., B{n}, and an initial sequence structure of [B1, B2, ..., B{n}].

Subsequently, during the viral infection simulation, the system underwent {m} targeted recombination insertions. Each insertion embeds a new mutant fragment (named N1, N2, ..., N{m}) at a specific locus in the current sequence, causing all fragments at that locus and downstream to shift backwards by 1 position. All insertions have occurred and are positionally constant, but are hidden from the analyst.

Define "recombination generation r" as the sequence state after the first r insertions:
- r=0 represents the wild-type initial state, fragment length is {n}
- r={m} represents the final infected state, fragment length is {total}

Your goal is: deduce the fragment ID at the {target}-th locus in the final state (r={m}).

You can repeatedly make the following two types of queries (only one per turn):
1. <query_1>r, p</query_1>: Query the fragment ID at locus p at recombination generation r.
2. <query_2>r, E</query_2>: Query the locus of fragment E at recombination generation r.

Note:
- r ranges from 0 to {m}.
- p ranges from 1 to {n} + r.
- E can be B1~B{n} or N1~N{m}.

Once you have concluded, please submit your diagnostic result using <answer>E</answer>, where E is the fragment ID at the {target}-th locus in the final state.
"""

    contextualized_rule_zh_3 = """\
【教育场景】
我们现在来进行一项“课程大纲动态排期”逻辑推演。

本学期初拟定了一份基础教学大纲，包含 {n} 个连续的课时，授课模块为 B1, B2, ..., B{n}，初始排课顺序为 [B1, B2, ..., B{n}]。

在学期进行中，教务处秘密下达了 {m} 次知识点扩充。每次扩充会在当前排课表的某一周次插入一个新授课模块（命名为 N1, N2, ..., N{m}），使得该周次及之后的全部模块授课进度整体顺延 1 个周次。所有扩充操作的落点已在系统内锁定，但对授课教师不可见。

定义“排课迭代 r”为下达前 r 次扩充后的教学大纲状态：
- r=0 表示初始排课状态，总周次为 {n}
- r={m} 表示最终排课状态，总周次为 {total}

你的目标是：推断出在最终状态（r={m}）下，第 {target} 个周次的授课模块是什么。

你可以反复提出以下两类查询（每次仅限一项）：
1. <query_1>r, p</query_1>：查询在排课迭代 r 下，第 p 个周次的授课模块。
2. <query_2>r, E</query_2>：查询在排课迭代 r 下，模块 E 所在的周次。

注意：
- r 的范围是 0 到 {m}。
- p 的范围是 1 到 {n} + r。
- E 可以是 B1~B{n} 或 N1~N{m}。

当你推演出结果后，请用 <answer>E</answer> 提交最终大纲，其中 E 是最终状态下第 {target} 个周次对应的授课模块。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
We are now conducting a "Dynamic Curriculum Scheduling" logical deduction.

A basic teaching syllabus was formulated at the beginning of the semester, consisting of {n} consecutive lecture periods, with teaching modules B1, B2, ..., B{n}, and an initial scheduling order of [B1, B2, ..., B{n}].

As the semester progressed, the Academic Affairs Office secretly issued {m} knowledge point expansions. Each expansion inserts a new teaching module (named N1, N2, ..., N{m}) into a certain week of the current schedule, causing all modules scheduled for that week and onwards to be postponed by 1 week. All expansion placement points are locked in the system but invisible to the instructors.

Define "scheduling iteration r" as the syllabus state after issuing the first r expansions:
- r=0 represents the initial scheduling state, total weeks is {n}
- r={m} represents the final scheduling state, total weeks is {total}

Your goal is: deduce the teaching module at the {target}-th week in the final state (r={m}).

You can repeatedly make the following two types of queries (only one per turn):
1. <query_1>r, p</query_1>: Query the module at week p under scheduling iteration r.
2. <query_2>r, E</query_2>: Query the week containing module E under scheduling iteration r.

Note:
- r ranges from 0 to {m}.
- p ranges from 1 to {n} + r.
- E can be B1~B{n} or N1~N{m}.

Once deduced, please submit the final syllabus using <answer>E</answer>, where E is the teaching module corresponding to the {target}-th week in the final state.
"""

    contextualized_rule_zh_4 = """\
【制造业/工业场景】
我们现在来进行一项“流水线工序插入”检测任务。

工厂生产线上规划了一条初始装配流水线，包含 {n} 个工位，装配工序依次为 B1, B2, ..., B{n}，初始流水线布局为 [B1, B2, ..., B{n}]。

在后续工艺升级中，控制中枢自动插入了 {m} 次补充工序。每次插入会在当前的流水线某处增加一个新工序节点（命名为 N1, N2, ..., N{m}），导致该位置及后续所有的工序节点向产线后端平移 1 个工位。所有插入指令已写入 PLC 程序，但测试人员无法直接读取。

定义“工艺版本 r”为执行前 r 次插入后的流水线状态：
- r=0 表示初始产线，工位总数为 {n}
- r={m} 表示最终升级产线，工位总数为 {total}

你的目标是：推断出在最终状态（r={m}）下，第 {target} 个工位上执行的工序名称是什么。

你可以反复提出以下两类查询（每次仅限一项）：
1. <query_1>r, p</query_1>：查询在工艺版本 r 下，第 p 个工位的工序。
2. <query_2>r, E</query_2>：查询在工艺版本 r 下，工序 E 所处的工位。

注意：
- r 的范围是 0 到 {m}。
- p 的范围是 1 到 {n} + r。
- E 可以是 B1~B{n} 或 N1~N{m}。

当你验证无误后，请用 <answer>E</answer> 提交你的结论，其中 E 是最终产线上第 {target} 个工位的工序。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
We are now performing an "Assembly Line Process Insertion" testing task.

An initial assembly line is planned on the factory production floor, containing {n} workstations, with assembly processes B1, B2, ..., B{n}, and an initial line layout of [B1, B2, ..., B{n}].

During subsequent process upgrades, the control center automatically inserted {m} supplementary processes. Each insertion adds a new process node (named N1, N2, ..., N{m}) somewhere on the current line, shifting that node and all subsequent process nodes one workstation towards the end of the line. All insertion commands have been written into the PLC program but cannot be directly read by testers.

Define "process version r" as the assembly line state after executing the first r insertions:
- r=0 represents the initial line, total workstations is {n}
- r={m} represents the final upgraded line, total workstations is {total}

Your goal is: deduce the process name at the {target}-th workstation in the final state (r={m}).

You can repeatedly make the following two types of queries (only one per turn):
1. <query_1>r, p</query_1>: Query the process at workstation p under process version r.
2. <query_2>r, E</query_2>: Query the workstation of process E under process version r.

Note:
- r ranges from 0 to {m}.
- p ranges from 1 to {n} + r.
- E can be B1~B{n} or N1~N{m}.

Once verified, please submit your conclusion using <answer>E</answer>, where E is the process at the {target}-th workstation on the final production line.
"""

    contextualized_rule_zh_5 = """\
【法律场景】
我们现在来进行一项“法案修正案增补”逻辑审查。

立法委员会草拟了一份初始法案文本，由 {n} 条核心条款组成，编号为 B1, B2, ..., B{n}，初始条文顺序为 [B1, B2, ..., B{n}]。

在后续三读期间，委员会有序提出了 {m} 次修正案增补。每次增补会在当前的法案文本某处插入一条新修正案（命名为 N1, N2, ..., N{m}），导致该位置及之后的全部法案条款编号向后顺延 1 条。所有修正案的增补位置在会议记录中已确定，但对外部审查员保密。

定义“法案草案 r”为完成前 r 次增补后的法案状态：
- r=0 表示初始一读草案，条款总数为 {n}
- r={m} 表示最终通过法案，条款总数为 {total}

你的目标是：推断出在最终通过状态（r={m}）下，第 {target} 条法案的编号内容是什么。

你可以反复提出以下两类查询（每次仅限一项）：
1. <query_1>r, p</query_1>：查询在法案草案 r 下，第 p 条的内容编号。
2. <query_2>r, E</query_2>：查询在法案草案 r 下，编号为 E 的法案内容是第几条。

注意：
- r 的范围是 0 到 {m}。
- p 的范围是 1 到 {n} + r。
- E 可以是 B1~B{n} 或 N1~N{m}。

当你审查完毕后，请用 <answer>E</answer> 提交你的审核结论，其中 E 是最终通过法案中第 {target} 条的内容编号。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
We are now conducting a "Bill Amendment Addition" logical review.

The Legislative Committee drafted an initial bill text consisting of {n} core clauses, numbered B1, B2, ..., B{n}, with an initial sequence of [B1, B2, ..., B{n}].

During subsequent readings, the committee systematically proposed {m} amendment additions. Each addition inserts a new amendment (named N1, N2, ..., N{m}) into the current bill text, causing the numbering of all clauses at and after that position to be postponed by 1 clause. The addition positions of all amendments are finalized in the meeting minutes but remain confidential to external reviewers.

Define "bill draft r" as the bill state after completing the first r additions:
- r=0 represents the initial first reading draft, total clauses is {n}
- r={m} represents the final passed bill, total clauses is {total}

Your goal is: deduce the content identifier of the {target}-th clause in the final passed state (r={m}).

You can repeatedly make the following two types of queries (only one per turn):
1. <query_1>r, p</query_1>: Query the content identifier of the p-th clause under bill draft r.
2. <query_2>r, E</query_2>: Query which clause number corresponds to content identifier E under bill draft r.

Note:
- r ranges from 0 to {m}.
- p ranges from 1 to {n} + r.
- E can be B1~B{n} or N1~N{m}.

Once your review is complete, please submit your audit conclusion using <answer>E</answer>, where E is the content identifier of the {target}-th clause in the final passed bill.
"""

    def _initialize_game(self):
        difficulty = getattr(self.config, 'difficulty', 1)
        seed = getattr(self.config, 'seed', id(self))
        self.rng = random.Random(seed)
        
        difficulty_map = {
            1: (4, 3),
            2: (6, 5),
            3: (8, 7),
            4: (10, 9),
            5: (12, 11),
        }
        self.n, self.m = difficulty_map.get(int(difficulty), (4, 3))
        self.total = self.n + self.m
        
        self.initial_sequence = [f"B{i}" for i in range(1, self.n + 1)]
        self.insertions = []
        
        self.history = [self.initial_sequence.copy()]
        
        current_seq = self.initial_sequence.copy()
        for i in range(1, self.m + 1):
            insert_pos = self.rng.randint(0, len(current_seq))
            new_element = f"N{i}"
            self.insertions.append((insert_pos, new_element))
            current_seq.insert(insert_pos, new_element)
            self.history.append(current_seq.copy())
            
        self.target_position = self.rng.randint(1, self.total)
        self.correct_answer = current_seq[self.target_position - 1]
        
        self._game_info = {
            "n": self.n,
            "m": self.m,
            "total": self.total,
            "target": self.target_position
        }

    def evaluate(self, parsed_info):
        answer = parsed_info.get("answer", "")
        if answer == self.correct_answer:
            return True
        return False

    def _cf_core_produce(self, parsed_info):
        if "query_1" in parsed_info:
            query = parsed_info["query_1"]
            try:
                r_str, p_str = [x.strip() for x in query.split(",")]
                r = int(r_str)
                p = int(p_str)
                if 0 <= r <= self.m and 1 <= p <= self.n + r:
                    element = self.history[r][p - 1]
                    if self.config.language == "zh":
                        return f"在时间步 {r}，位置 {p} 的元素是 {element}。"
                    else:
                        return f"At time step {r}, the element at position {p} is {element}."
                else:
                    if self.config.language == "zh":
                        return "查询参数超出有效范围。"
                    else:
                        return "Query parameters out of valid range."
            except Exception:
                if self.config.language == "zh":
                    return "查询格式错误，请使用 r, p 格式。"
                else:
                    return "Query format error. Please use r, p format."
                    
        elif "query_2" in parsed_info:
            query = parsed_info["query_2"]
            try:
                r_str, e_str = [x.strip() for x in query.split(",")]
                r = int(r_str)
                e = e_str
                if 0 <= r <= self.m:
                    if e in self.history[r]:
                        pos = self.history[r].index(e) + 1
                        if self.config.language == "zh":
                            return f"在时间步 {r}，元素 {e} 的位置是 {pos}。"
                        else:
                            return f"At time step {r}, the position of element {e} is {pos}."
                    else:
                        if self.config.language == "zh":
                            return f"元素 {e} 不存在于时间步 {r} 的序列中。"
                        else:
                            return f"Element {e} does not exist in the sequence at time step {r}."
                else:
                    if self.config.language == "zh":
                        return "时间步超出有效范围。"
                    else:
                        return "Time step out of valid range."
            except Exception:
                if self.config.language == "zh":
                    return "查询格式错误，请使用 r, E 格式。"
                else:
                    return "Query format error. Please use r, E format."
        
        return "无法识别的查询。" if self.config.language == "zh" else "Unrecognized query."

    def get_all_possible_queries(self):
        queries = []
        for r in range(self.m + 1):
            for p in range(1, self.n + r + 1):
                q_str  = f"<query_1>{r}, {p}</query_1>"
                answer = self._cf_core_produce({"query_1": f"{r}, {p}"})
                queries.append({"query": q_str, "answer": answer})
            for e in self.history[r]:
                q_str  = f"<query_2>{r}, {e}</query_2>"
                answer = self._cf_core_produce({"query_2": f"{r}, {e}"})
                queries.append({"query": q_str, "answer": answer})
        return queries

    def _cf_make_wrong(self, correct):
        elem_match = re.search(r'(B\d+|N\d+)', correct)
        if elem_match:
            original_elem = elem_match.group(1)
            all_elements = [f"B{i}" for i in range(1, self.n + 1)] + [f"N{i}" for i in range(1, self.m + 1)]
            candidates = [e for e in all_elements if e != original_elem]
            if candidates:
                wrong_elem = self.rng.choice(candidates)
                return correct.replace(original_elem, wrong_elem, 1)
        
        pos_match = re.findall(r'(\d+)', correct)
        if pos_match:
            last_num = pos_match[-1]
            wrong_num = str(int(last_num) + 1)
            idx = correct.rfind(last_num)
            return correct[:idx] + wrong_num + correct[idx + len(last_num):]
        
        return correct + " (modified)"