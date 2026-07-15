from .base import Game
import math

class SequenceInsertionGame(Game):

    game_rule_zh = """\
我们现在来玩一个"序列插入推理"游戏，规则如下：

游戏设定了一个长度为 {n} 的有序序列，元素标号为 1, 2, ..., {n}，初始时它们按顺序排列。我已经秘密地进行了若干次插入操作，每次在序列的某个位置插入一个占位元素（用 * 表示），得到了一个长度为 {final_length} 的最终序列。插入的次数和位置都是固定的，但你不知道。

你的目标是判定：在最终序列中，第 {target} 位是什么？
- 如果是原始元素，需要指出具体的编号 i（1 到 {n} 之间）
- 如果是占位元素，则回答"占位元素"

你可以通过以下两种查询来获取信息（每次只能查询一个）：

1. 位置查询：询问原始元素 i 在最终序列中的位置。我会返回一个整数（范围 1 到 {final_length}）。
2. 计数查询：询问原始元素 i 之前有多少个占位元素。我会返回一个整数（范围 0 到 {k}）。

注意：
- 你不能直接询问"第 r 位是什么"或"第 r 位是否为占位元素"
- 你应该尽可能少地使用查询次数
- 如果查询次数超过限制或格式错误，游戏将失败

每次查询只能包含一个标签。请使用以下 XML 格式：

- 位置查询（例如查询元素 3 的位置）：
<query_position>3</query_position>

- 计数查询（例如查询元素 5 之前的占位元素个数）：
<query_count>5</query_count>

提交最终答案时，使用以下格式：

- 如果判定为原始元素（例如元素 7）：
<answer>7</answer>

- 如果判定为占位元素：
<answer>placeholder</answer>
"""

    game_rule_en = """\
Let's play a "Sequence Insertion Deduction" game. Here are the rules:

There is an ordered sequence of length {n}, with elements labeled 1, 2, ..., {n}, initially arranged in order. I have secretly performed several insertion operations, each time inserting a placeholder element (denoted as *) at some position in the sequence, resulting in a final sequence of length {final_length}. The number and positions of insertions are fixed, but unknown to you.

Your goal is to determine: In the final sequence, what is at position {target}?
- If it is an original element, specify its ID i (between 1 and {n})
- If it is a placeholder element, answer "placeholder"

You can obtain information through the following two types of queries (one at a time):

1. Position Query: Ask for the position of original element i in the final sequence. I will return an integer (range 1 to {final_length}).
2. Count Query: Ask how many placeholder elements are before original element i. I will return an integer (range 0 to {k}).

Note:
- You cannot directly ask "what is at position r" or "is position r a placeholder"
- You should use as few queries as possible
- If the number of queries exceeds the limit or the format is invalid, the game will fail

Each query must contain only one tag. Use the following XML format:

- Position Query (e.g., querying the position of element 3):
<query_position>3</query_position>

- Count Query (e.g., querying the number of placeholders before element 5):
<query_count>5</query_count>

When submitting the final answer, use the following format:

- If determined to be an original element (e.g., element 7):
<answer>7</answer>

- If determined to be a placeholder:
<answer>placeholder</answer>
"""

    contextualized_rule_zh_1 = """\
作为铁路调度中心的首席指挥官，你需要排查一段异常的列车发车记录。

今天原计划有 {n} 趟常规图定列车（编号为 1 到 {n}），初始按序排班。但在实际运行中，调度系统秘密地在常规序列中插入了若干趟临时加开的紧急救援列车（作为占位元素，用 * 表示），最终形成了长度为 {final_length} 的实际发车序列。插入的次数和位置是固定的，但你手头没有直接记录。

你的目标是查明：在最终发车序列中，第 {target} 位发车的是什么列车？
- 如果是常规列车，需指出具体的列车编号 i（1 到 {n} 之间）
- 如果是紧急救援列车，请直接回答"placeholder"

你可以通过调度系统进行以下两种查询（每次只能查询一个）：

1. 位置查询：询问常规列车 i 实际在第几个发车。系统会返回一个整数（范围 1 到 {final_length}）。
2. 计数查询：询问在常规列车 i 发车之前，已经发出了多少趟紧急救援列车。系统会返回一个整数（范围 0 到 {k}）。

注意：
- 你不能直接询问"第 r 位发车的是什么"或"第 r 位是否为紧急救援列车"
- 你应该尽可能少地使用查询次数
- 如果查询次数超过限制或格式错误，系统判定任务失败

每次查询只能包含一个标签。请使用以下 XML 格式：

- 位置查询（例如查询常规列车 3 的实际发车位置）：
<query_position>3</query_position>

- 计数查询（例如查询常规列车 5 发车前的紧急救援列车趟数）：
<query_count>5</query_count>

提交最终答案时，使用以下格式：

- 如果判定为常规列车（例如列车 7）：
<answer>7</answer>

- 如果判定为紧急救援列车：
<answer>placeholder</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
As the chief commander of the railway dispatch center, you need to investigate an abnormal train departure record.

Today, there were originally {n} scheduled regular trains (numbered 1 to {n}), initially arranged in sequence. However, during actual operations, the dispatch system secretly inserted several emergency rescue trains (acting as placeholder elements, denoted as *) at certain positions, resulting in a final departure sequence of length {final_length}. The number and positions of these insertions are fixed but unknown to you.

Your goal is to determine: In the final departure sequence, what train departed at position {target}?
- If it is a regular train, specify its ID i (between 1 and {n})
- If it is an emergency rescue train, answer "placeholder"

You can query the dispatch system in two ways (one at a time):

1. Position Query: Ask for the actual departure position of regular train i. The system returns an integer (range 1 to {final_length}).
2. Count Query: Ask how many emergency rescue trains departed before regular train i. The system returns an integer (range 0 to {k}).

Note:
- You cannot directly ask "what train is at position r" or "is position r an emergency rescue train"
- You should use as few queries as possible
- If the number of queries exceeds the limit or the format is invalid, the mission will fail

Each query must contain only one tag. Use the following XML format:

- Position Query (e.g., querying the departure position of regular train 3):
<query_position>3</query_position>

- Count Query (e.g., querying the number of emergency rescue trains before regular train 5):
<query_count>5</query_count>

When submitting the final answer, use the following format:

- If determined to be a regular train (e.g., train 7):
<answer>7</answer>

- If determined to be an emergency rescue train:
<answer>placeholder</answer>
"""

    contextualized_rule_zh_2 = """\
作为急诊科的分诊护士长，你需要理清今日混杂的就诊顺序。

今天原计划有 {n} 名预约的常规号患者（编号 1 到 {n}），初始按挂号顺序排队。但由于突发状况，系统在队列的某些位置紧急安插了若干名急救患者（作为占位元素，用 * 表示），最终形成了一个长度为 {final_length} 的实际就诊序列。急救患者的插入次数和位置是固定的，但记录发生了损坏。

你的目标是查明：在最终就诊序列中，第 {target} 位就诊的是谁？
- 如果是常规号患者，需指出其具体的编号 i（1 到 {n} 之间）
- 如果是急救患者，请直接回答"placeholder"

你可以向分诊系统发起以下两种查询（每次只能查询一个）：

1. 位置查询：询问常规号患者 i 实际在第几个就诊。系统会返回一个整数（范围 1 到 {final_length}）。
2. 计数查询：询问在常规号患者 i 就诊之前，已经接诊了多少名急救患者。系统会返回一个整数（范围 0 到 {k}）。

注意：
- 你不能直接询问"第 r 位就诊的是谁"或"第 r 位是否为急救患者"
- 你应该尽可能少地使用查询次数
- 如果查询次数超过限制或格式错误，系统判定任务失败

每次查询只能包含一个标签。请使用以下 XML 格式：

- 位置查询（例如查询常规号患者 3 的实际就诊位置）：
<query_position>3</query_position>

- 计数查询（例如查询常规号患者 5 就诊前的急救患者人数）：
<query_count>5</query_count>

提交最终答案时，使用以下格式：

- 如果判定为常规号患者（例如患者 7）：
<answer>7</answer>

- 如果判定为急救患者：
<answer>placeholder</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
As the head triage nurse in the emergency department, you need to sort out today's mixed consultation sequence.

Today, there were originally {n} standard booked patients (numbered 1 to {n}), initially queued in order. Due to sudden emergencies, the system urgently inserted several emergency patients (acting as placeholder elements, denoted as *) at certain positions in the queue, resulting in a final consultation sequence of length {final_length}. The number and positions of these insertions are fixed, but the records have been corrupted.

Your goal is to determine: In the final consultation sequence, who is the patient at position {target}?
- If it is a standard booked patient, specify their ID i (between 1 and {n})
- If it is an emergency patient, answer "placeholder"

You can query the triage system in two ways (one at a time):

1. Position Query: Ask for the actual consultation position of standard booked patient i. The system returns an integer (range 1 to {final_length}).
2. Count Query: Ask how many emergency patients were treated before standard booked patient i. The system returns an integer (range 0 to {k}).

Note:
- You cannot directly ask "who is at position r" or "is position r an emergency patient"
- You should use as few queries as possible
- If the number of queries exceeds the limit or the format is invalid, the mission will fail

Each query must contain only one tag. Use the following XML format:

- Position Query (e.g., querying the consultation position of booked patient 3):
<query_position>3</query_position>

- Count Query (e.g., querying the number of emergency patients before booked patient 5):
<query_count>5</query_count>

When submitting the final answer, use the following format:

- If determined to be a standard booked patient (e.g., patient 7):
<answer>7</answer>

- If determined to be an emergency patient:
<answer>placeholder</answer>
"""

    contextualized_rule_zh_3 = """\
作为命题组的审核专家，你正在校验一份被动态调整过的期末试卷。

这份试卷原本设计了 {n} 道标准考题（编号为 1 到 {n}），初始按难度顺序排列。为了测试教改效果，题库系统自动在试卷的某些位置插入了若干道附加题（作为占位元素，用 * 表示），最终生成了一份包含 {final_length} 道题的实际试卷。附加题的数量和位置是固定的，但对审核端隐藏。

你的目标是判定：在最终生成的试卷中，第 {target} 题是什么？
- 如果是标准考题，需指出具体的题号 i（1 到 {n} 之间）
- 如果是附加题，请直接回答"placeholder"

你可以通过题库系统进行以下两种查询（每次只能查询一个）：

1. 位置查询：询问标准考题 i 在最终试卷中的实际题号。系统会返回一个整数（范围 1 到 {final_length}）。
2. 计数查询：询问在标准考题 i 之前，共出现了多少道附加题。系统会返回一个整数（范围 0 到 {k}）。

注意：
- 你不能直接询问"第 r 题是什么"或"第 r 题是否为附加题"
- 你应该尽可能少地使用查询次数
- 如果查询次数超过限制或格式错误，系统判定任务失败

每次查询只能包含一个标签。请使用以下 XML 格式：

- 位置查询（例如查询标准考题 3 的实际题号）：
<query_position>3</query_position>

- 计数查询（例如查询标准考题 5 之前的附加题数量）：
<query_count>5</query_count>

提交最终答案时，使用以下格式：

- 如果判定为标准考题（例如考题 7）：
<answer>7</answer>

- 如果判定为附加题：
<answer>placeholder</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
As an audit expert of the exam committee, you are verifying a dynamically adjusted final exam paper.

This paper originally designed {n} standard exam questions (numbered 1 to {n}), initially arranged by difficulty. To test teaching reforms, the system automatically inserted several bonus questions (acting as placeholder elements, denoted as *) at certain positions, generating an actual paper with a total of {final_length} questions. The number and positions of bonus questions are fixed but hidden from the audit interface.

Your goal is to determine: In the final generated paper, what is question number {target}?
- If it is a standard exam question, specify its ID i (between 1 and {n})
- If it is a bonus question, answer "placeholder"

You can query the question bank system in two ways (one at a time):

1. Position Query: Ask for the final position of standard exam question i. The system returns an integer (range 1 to {final_length}).
2. Count Query: Ask how many bonus questions appear before standard exam question i. The system returns an integer (range 0 to {k}).

Note:
- You cannot directly ask "what is question r" or "is question r a bonus question"
- You should use as few queries as possible
- If the number of queries exceeds the limit or the format is invalid, the mission will fail

Each query must contain only one tag. Use the following XML format:

- Position Query (e.g., querying the final position of standard question 3):
<query_position>3</query_position>

- Count Query (e.g., querying the number of bonus questions before standard question 5):
<query_count>5</query_count>

When submitting the final answer, use the following format:

- If determined to be a standard exam question (e.g., question 7):
<answer>7</answer>

- If determined to be a bonus question:
<answer>placeholder</answer>
"""

    contextualized_rule_zh_4 = """\
作为智能制造工厂的生产线调度员，你正在追踪一批混合生产的订单。

今天的排产计划原本包含 {n} 个标准生产批次（编号 1 到 {n}），初始按标准工序排拉。但在生产过程中，MES系统自动在流水线的某些环节插入了若干个紧急插单（作为占位元素，用 * 表示），最终形成了长度为 {final_length} 的实际加工序列。插单的次数和位置是固定的，但由于网络延迟你无法直接查看全貌。

你的目标是查明：在最终加工序列中，第 {target} 个被处理的订单是什么？
- 如果是标准生产批次，需指出具体的批次编号 i（1 到 {n} 之间）
- 如果是紧急插单，请直接回答"placeholder"

你可以通过MES系统进行以下两种查询（每次只能查询一个）：

1. 位置查询：询问标准生产批次 i 在最终流水线上的加工顺位。系统会返回一个整数（范围 1 到 {final_length}）。
2. 计数查询：询问在标准生产批次 i 加工之前，已经处理了多少个紧急插单。系统会返回一个整数（范围 0 到 {k}）。

注意：
- 你不能直接询问"第 r 顺位加工的是什么"或"第 r 顺位是否为紧急插单"
- 你应该尽可能少地使用查询次数
- 如果查询次数超过限制或格式错误，系统判定任务失败

每次查询只能包含一个标签。请使用以下 XML 格式：

- 位置查询（例如查询标准生产批次 3 的加工顺位）：
<query_position>3</query_position>

- 计数查询（例如查询标准生产批次 5 加工前的紧急插单个数）：
<query_count>5</query_count>

提交最终答案时，使用以下格式：

- 如果判定为标准生产批次（例如批次 7）：
<answer>7</answer>

- 如果判定为紧急插单：
<answer>placeholder</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
As a production line dispatcher in a smart manufacturing factory, you are tracking a mixed batch of orders.

Today's production plan originally contained {n} standard production batches (numbered 1 to {n}), initially scheduled by standard procedures. During production, the MES system automatically inserted several rush orders (acting as placeholder elements, denoted as *) at certain stages, resulting in a final processing sequence of length {final_length}. The number and positions of rush orders are fixed, but due to network latency, you cannot view the full picture directly.

Your goal is to determine: In the final processing sequence, what order is processed at sequence step {target}?
- If it is a standard production batch, specify its ID i (between 1 and {n})
- If it is a rush order, answer "placeholder"

You can query the MES system in two ways (one at a time):

1. Position Query: Ask for the actual processing position of standard production batch i. The system returns an integer (range 1 to {final_length}).
2. Count Query: Ask how many rush orders were processed before standard production batch i. The system returns an integer (range 0 to {k}).

Note:
- You cannot directly ask "what is processed at step r" or "is step r a rush order"
- You should use as few queries as possible
- If the number of queries exceeds the limit or the format is invalid, the mission will fail

Each query must contain only one tag. Use the following XML format:

- Position Query (e.g., querying the processing position of standard batch 3):
<query_position>3</query_position>

- Count Query (e.g., querying the number of rush orders before standard batch 5):
<query_count>5</query_count>

When submitting the final answer, use the following format:

- If determined to be a standard production batch (e.g., batch 7):
<answer>7</answer>

- If determined to be a rush order:
<answer>placeholder</answer>
"""

    contextualized_rule_zh_5 = """\
作为法院的排期书记员，你需要核对一份包含紧急动议的庭审排期表。

本月原计划有 {n} 宗常规诉讼案件（编号 1 到 {n}），初始按立案先后排期。然而，法官在日程的某些时段签发了若干次紧急禁令听证会（作为占位元素，用 * 表示），最终形成了一份包含 {final_length} 个庭审场次的实际排期表。紧急听证会的插入次数和位置已经排定，但你尚未拿到完整副本。

你的目标是查明：在最终排期表中，第 {target} 场庭审是什么？
- 如果是常规诉讼案件，需指出具体的案件编号 i（1 到 {n} 之间）
- 如果是紧急禁令听证会，请直接回答"placeholder"

你可以通过法院内网进行以下两种查询（每次只能查询一个）：

1. 位置查询：询问常规诉讼案件 i 实际排在第几场庭审。系统会返回一个整数（范围 1 到 {final_length}）。
2. 计数查询：询问在常规诉讼案件 i 开庭前，已经进行了多少场紧急禁令听证会。系统会返回一个整数（范围 0 到 {k}）。

注意：
- 你不能直接询问"第 r 场庭审是什么"或"第 r 场是否为紧急禁令听证会"
- 你应该尽可能少地使用查询次数
- 如果查询次数超过限制或格式错误，系统判定任务失败

每次查询只能包含一个标签。请使用以下 XML 格式：

- 位置查询（例如查询常规诉讼案件 3 的庭审场次）：
<query_position>3</query_position>

- 计数查询（例如查询常规诉讼案件 5 开庭前的紧急听证会次数）：
<query_count>5</query_count>

提交最终答案时，使用以下格式：

- 如果判定为常规诉讼案件（例如案件 7）：
<answer>7</answer>

- 如果判定为紧急禁令听证会：
<answer>placeholder</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
As a scheduling clerk at the court, you need to verify a trial schedule containing emergency motions.

This month, there were originally {n} standard litigation cases (numbered 1 to {n}), initially scheduled by filing order. However, the judge issued several emergency injunction hearings (acting as placeholder elements, denoted as *) at certain timeslots, resulting in an actual schedule containing {final_length} trial sessions. The insertions of emergency hearings are fixed, but you haven't received the full copy yet.

Your goal is to determine: In the final schedule, what is the trial session at position {target}?
- If it is a standard litigation case, specify its case ID i (between 1 and {n})
- If it is an emergency injunction hearing, answer "placeholder"

You can query the court intranet in two ways (one at a time):

1. Position Query: Ask for the actual trial session position of standard litigation case i. The system returns an integer (range 1 to {final_length}).
2. Count Query: Ask how many emergency injunction hearings were held before standard litigation case i. The system returns an integer (range 0 to {k}).

Note:
- You cannot directly ask "what case is at session r" or "is session r an emergency hearing"
- You should use as few queries as possible
- If the number of queries exceeds the limit or the format is invalid, the mission will fail

Each query must contain only one tag. Use the following XML format:

- Position Query (e.g., querying the trial session position of standard litigation case 3):
<query_position>3</query_position>

- Count Query (e.g., querying the number of emergency hearings before standard litigation case 5):
<query_count>5</query_count>

When submitting the final answer, use the following format:

- If determined to be a standard litigation case (e.g., case 7):
<answer>7</answer>

- If determined to be an emergency injunction hearing:
<answer>placeholder</answer>
"""

    tags = ["answer", "query_position", "query_count"]
    
    reasoning_type = "演绎推理"
    data_structure = "序列"
    enable_counterfactual = False

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 8,
                "k": 2,
                "insertions": [3, 6],
                "target": 4,
            },
            2: {
                "n": 16,
                "k": 3,
                "insertions": [5, 10, 15],
                "target": 11,
            },
            3: {
                "n": 32,
                "k": 5,
                "insertions": [8, 16, 24, 28, 32],
                "target": 30,
            },
            4: {
                "n": 64,
                "k": 7,
                "insertions": [10, 20, 30, 40, 50, 55, 60],
                "target": 42,
            },
            5: {
                "n": 128,
                "k": 10,
                "insertions": [15, 30, 45, 60, 75, 90, 105, 120, 125, 130],
                "target": 100,
            },
        },
        "en": {
            1: {
                "n": 8,
                "k": 2,
                "insertions": [3, 6],
                "target": 4,
            },
            2: {
                "n": 16,
                "k": 3,
                "insertions": [5, 10, 15],
                "target": 11,
            },
            3: {
                "n": 32,
                "k": 5,
                "insertions": [8, 16, 24, 28, 32],
                "target": 30,
            },
            4: {
                "n": 64,
                "k": 7,
                "insertions": [10, 20, 30, 40, 50, 55, 60],
                "target": 42,
            },
            5: {
                "n": 128,
                "k": 10,
                "insertions": [15, 30, 45, 60, 75, 90, 105, 120, 125, 130],
                "target": 100,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)
        self.query_count = 0

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.n = cfg["n"]
        self.k = cfg["k"]
        self.insertions = sorted(cfg["insertions"])
        self.target = cfg["target"]
        
        self.max_queries = math.ceil(math.log2(self.n)) + 2
        
        final_length = self.n + self.k
        
        if len(self.insertions) != self.k:
            raise ValueError(f"Number of insertions ({len(self.insertions)}) does not match k ({self.k})")
        if self.insertions and self.insertions[-1] > final_length:
            raise ValueError(f"Insertion position {self.insertions[-1]} exceeds final sequence length {final_length}")
        
        insertion_set = set(self.insertions)
        self.final_seq = []
        original_idx = 1
        
        for pos in range(1, final_length + 1):
            if pos in insertion_set:
                self.final_seq.append("placeholder")
            else:
                if original_idx <= self.n:
                    self.final_seq.append(original_idx)
                    original_idx += 1
                else:
                    self.final_seq.append("placeholder")
        
        assert original_idx == self.n + 1, \
            f"Not all original elements placed: expected {self.n}, placed {original_idx - 1}"
        
        self.f_map = {}
        self.b_map = {}
        
        for pos, elem in enumerate(self.final_seq, start=1):
            if elem != "placeholder":
                self.f_map[elem] = pos
                placeholders_before = sum(1 for x in self.final_seq[:pos-1] if x == "placeholder")
                self.b_map[elem] = placeholders_before
        
        if self.target < 1 or self.target > len(self.final_seq):
            raise ValueError(f"Target position {self.target} out of range [1, {len(self.final_seq)}]")
        
        self._game_info["n"] = self.n
        self._game_info["k"] = self.k
        self._game_info["final_length"] = len(self.final_seq)
        self._game_info["target"] = self.target

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        true_answer = self.final_seq[self.target - 1]
        
        if raw_ans.lower() == "placeholder":
            return true_answer == "placeholder"
        else:
            try:
                answer_id = int(raw_ans)
                return true_answer == answer_id
            except ValueError:
                return False

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        for i in range(1, self.n + 1):
            queries.append({
                "query": f"<query_position>{i}</query_position>",
                "answer": str(self.f_map[i])
            })
            
            queries.append({
                "query": f"<query_count>{i}</query_count>",
                "answer": str(self.b_map[i])
            })
            
        return queries

    def _cf_core_produce(self, parsed_info):
        if self.query_count >= self.max_queries:
            raise ValueError(
                f"Query limit exceeded ({self.max_queries})." 
                if self.config.language == "en" 
                else f"查询次数超过限制（{self.max_queries}）。"
            )
        
        self.query_count += 1
        
        if "query_position" in parsed_info:
            try:
                elem_id = int(parsed_info["query_position"].strip())
                if elem_id < 1 or elem_id > self.n:
                    raise ValueError
                return str(self.f_map[elem_id])
            except (ValueError, KeyError):
                return (
                    "Error: Invalid element ID." 
                    if self.config.language == "en" 
                    else "错误：无效的元素编号。"
                )
        
        elif "query_count" in parsed_info:
            try:
                elem_id = int(parsed_info["query_count"].strip())
                if elem_id < 1 or elem_id > self.n:
                    raise ValueError
                return str(self.b_map[elem_id])
            except (ValueError, KeyError):
                return (
                    "Error: Invalid element ID." 
                    if self.config.language == "en" 
                    else "错误：无效的元素编号。"
                )
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        lower_correct = correct.lower()
        if lower_correct == "yes":
            return "No" if correct[0].isupper() else "no"
        if lower_correct == "no":
            return "Yes" if correct[0].isupper() else "yes"

        return correct + "_WRONG"