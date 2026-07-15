import random
from .base import Game

class PermutationDeductionGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "序列"

    game_rule_zh = """\
我们现在来玩一个"置换推理"游戏，规则如下：

游戏设定了一个长度为 {n} 的有序序列 T，编号从 1 到 {n}。每个位置 i 都有：
- 名称 name[i]（已公开，见下方）
- 二值属性 b[i]（已公开，见下方）

序列信息：
{sequence_info}

我已秘密选择了四种置换规则之一，并将其应用于序列 T 得到真实顺序 S，但你无法直接看到 S。四种置换规则为：
- A（恒等）：保持原序列不变
- B（反转）：将序列完全反转
- C（循环右移一格）：最后一个元素移到开头
- D（循环左移一格）：第一个元素移到末尾

你的目标是推断出我使用的置换规则类型以及在真实顺序 S 中第 {k} 位的元素名称。

你可以反复向我提出以下查询（每次仅限一个问题）：

1. 探测查询：询问真实顺序 S 中第 i 位的二值属性是多少。我会返回 0 或 1。
2. 检索查询：询问真实顺序 S 中第 j 位的元素名称是什么。我会返回对应名称。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签，使用以下 XML 格式：

- 探测查询（例如询问第 3 位）：
<query_probe>3</query_probe>

- 检索查询（例如询问第 5 位）：
<query_retrieve>5</query_retrieve>

提交最终答案时，必须说明置换类型（A、B、C 或 D）并给出第 {k} 位的元素名称，格式如下：

<answer>type=B, name=元素名</answer>
"""

    game_rule_en = """\
Let's play a "Permutation Deduction" game. Here are the rules:

There is an ordered sequence T of length {n}, indexed from 1 to {n}. Each position i has:
- A name name[i] (publicly known, see below)
- A binary attribute b[i] (publicly known, see below)

Sequence information:
{sequence_info}

I have secretly selected one of four permutation rules and applied it to sequence T to get the true order S, but you cannot see S directly. The four permutation rules are:
- A (Identity): Keep the original sequence unchanged
- B (Reverse): Completely reverse the sequence
- C (Cyclic right shift by 1): Move the last element to the front
- D (Cyclic left shift by 1): Move the first element to the end

Your goal is to deduce which permutation rule I used and the name of the element at position {k} in the true order S.

You can repeatedly ask me the following queries (one per turn):

1. Probe Query: Ask for the binary attribute at position i in the true order S. I will return 0 or 1.
2. Retrieve Query: Ask for the element name at position j in the true order S. I will return the corresponding name.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Probe Query (e.g., asking about position 3):
<query_probe>3</query_probe>

- Retrieve Query (e.g., asking about position 5):
<query_retrieve>5</query_retrieve>

When submitting the final answer, specify the permutation type (A, B, C, or D) and the name of the element at position {k}, using this format:

<answer>type=B, name=ElementName</answer>
"""

    contextualized_rule_zh_1 = """\
智能交通调度中心正在处理一个包含 {n} 个班次列车的预定发车序列 T，编号从 1 到 {n}。每个发车位 i 包含：
- 列车代号 name[i]（已公开，见下方）
- 是否载客的二值属性 b[i]（已公开，见下方）

序列信息：
{sequence_info}

由于临时管制，调度系统隐秘使用了四种调度策略之一，将其应用于预定发车序列 T 得到实际发车顺序 S，但你无法直接看到 S。四种调度策略为：
- A（原样放行）：保持原发车序列不变
- B（完全倒序）：将发车序列完全反转
- C（末班提首）：最后一个列车移到首位发车
- D（首班延后）：第一个列车移到末尾发车

你的目标是推断出系统使用的调度策略类型，以及在实际发车顺序 S 中第 {k} 位发车的列车代号。

你可以反复向我提出以下查询（每次仅限一个问题）：
1. 探测查询：询问实际发车顺序 S 中第 i 位的载客属性是多少。我会返回 0 或 1。
2. 检索查询：询问实际发车顺序 S 中第 j 位的列车代号是什么。我会返回对应代号。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，调度任务失败。

每次询问只能包含一个标签，使用以下 XML 格式：
- 探测查询（例如询问实际第 3 位）：
<query_probe>3</query_probe>
- 检索查询（例如询问实际第 5 位）：
<query_retrieve>5</query_retrieve>

提交最终答案时，必须说明调度策略（A、B、C 或 D）并给出第 {k} 位的列车代号，格式如下：
<answer>type=B, name=列车代号</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The intelligent traffic dispatch center is processing a scheduled departure sequence T of {n} trains, indexed from 1 to {n}. Each slot i has:
- A Train ID name[i] (publicly known, see below)
- A binary passenger-carrying attribute b[i] (publicly known, see below)

Sequence information:
{sequence_info}

Due to temporary control, the system secretly applied one of four dispatch strategies to sequence T to get the actual departure order S, which you cannot see directly. The four strategies are:
- A (Identity): Keep the original sequence unchanged
- B (Reverse): Completely reverse the departure sequence
- C (Last to Front): Move the last train to the front
- D (First to End): Move the first train to the end

Your goal is to deduce the dispatch strategy used and the Train ID at position {k} in the actual departure order S.

You can repeatedly ask the following queries (one per turn):
1. Probe Query: Ask for the binary passenger attribute at position i in the actual order S. I will return 0 or 1.
2. Retrieve Query: Ask for the Train ID at position j in the actual order S. I will return the corresponding ID.

When you have enough information, submit your final answer. Incorrect answers or formats result in task failure.

Each query must contain only one tag. Use the following XML format:
- Probe Query (e.g., asking about position 3):
<query_probe>3</query_probe>
- Retrieve Query (e.g., asking about position 5):
<query_retrieve>5</query_retrieve>

When submitting the final answer, specify the strategy type (A, B, C, or D) and the Train ID at position {k}, formatted as:
<answer>type=B, name=TrainID</answer>
"""

    contextualized_rule_zh_2 = """\
医院检验科收到了一批包含 {n} 个样本的初始上机队列 T，编号从 1 到 {n}。每个样本位 i 包含：
- 样本编号 name[i]（已公开，见下方）
- 是否加急的二值属性 b[i]（已公开，见下方）

序列信息：
{sequence_info}

为了优化机器运转，生化分析仪自动选用了四种混匀重排规则之一，将初始队列 T 转换为实际上机测试队列 S，但你无法直接查阅 S。四种重排规则为：
- A（原序测试）：保持初始队列不变
- B（完全倒序）：将测试队列完全反转
- C（尾管优先）：最后一管样本移到首位测试
- D（首管延后）：第一管样本移到末尾测试

你的目标是推断出仪器使用的重排规则类型，以及在实际测试队列 S 中第 {k} 个被测试的样本编号。

你可以反复向我提出以下查询（每次仅限一个问题）：
1. 探测查询：询问实际测试队列 S 中第 i 位的加急属性是多少。我会返回 0 或 1。
2. 检索查询：询问实际测试队列 S 中第 j 位的样本编号是什么。我会返回对应编号。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，检验流程失败。

每次询问只能包含一个标签，使用以下 XML 格式：
- 探测查询（例如询问实际第 3 位）：
<query_probe>3</query_probe>
- 检索查询（例如询问实际第 5 位）：
<query_retrieve>5</query_retrieve>

提交最终答案时，必须说明重排规则（A、B、C 或 D）并给出第 {k} 位的样本编号，格式如下：
<answer>type=B, name=样本编号</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
The hospital lab received an initial testing queue T of {n} samples, indexed from 1 to {n}. Each sample position i has:
- A Sample ID name[i] (publicly known, see below)
- A binary urgent-status attribute b[i] (publicly known, see below)

Sequence information:
{sequence_info}

To optimize machine operation, the biochemical analyzer automatically applied one of four rearrangement rules to queue T to form the actual testing queue S, which is hidden from you. The four rules are:
- A (Original order): Keep the initial queue unchanged
- B (Reverse order): Completely reverse the testing queue
- C (Tail to Front): Test the last sample first
- D (Head to Tail): Test the first sample last

Your goal is to deduce the rearrangement rule used and the Sample ID at position {k} in the actual testing queue S.

You can repeatedly ask the following queries (one per turn):
1. Probe Query: Ask for the urgent-status attribute at position i in the actual queue S. I will return 0 or 1.
2. Retrieve Query: Ask for the Sample ID at position j in the actual queue S. I will return the corresponding ID.

When you have enough information, submit your final answer. Incorrect answers or formats result in process failure.

Each query must contain only one tag. Use the following XML format:
- Probe Query (e.g., asking about position 3):
<query_probe>3</query_probe>
- Retrieve Query (e.g., asking about position 5):
<query_retrieve>5</query_retrieve>

When submitting the final answer, specify the rule type (A, B, C, or D) and the Sample ID at position {k}, formatted as:
<answer>type=B, name=SampleID</answer>
"""

    contextualized_rule_zh_3 = """\
考务中心整理了一叠包含 {n} 份试卷的初始阅卷序列 T，编号从 1 到 {n}。每个试卷位 i 记录了：
- 考生考号 name[i]（已公开，见下方）
- 客观题是否满分的二值属性 b[i]（已公开，见下方）

序列信息：
{sequence_info}

为防止阅卷疲劳，分发系统采用四种盲排策略之一，对初始序列 T 进行了置换，生成了实际分发给阅卷人的序列 S，你无法直接看到 S。四种盲排策略为：
- A（保持原样）：阅卷顺序不变
- B（完全倒序）：将试卷堆完全翻转
- C（底卷置顶）：最底下的试卷移到最上面
- D（顶卷沉底）：最上面的试卷移到最底下

你的目标是推断出系统采用的盲排策略类型，以及实际分发序列 S 中第 {k} 份试卷的考生考号。

你可以反复向我提出以下查询（每次仅限一个问题）：
1. 探测查询：询问实际分发序列 S 中第 i 份试卷的满分属性是多少。我会返回 0 或 1。
2. 检索查询：询问实际分发序列 S 中第 j 份试卷的考生考号是什么。我会返回对应考号。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，阅卷质检失败。

每次询问只能包含一个标签，使用以下 XML 格式：
- 探测查询（例如询问实际第 3 份）：
<query_probe>3</query_probe>
- 检索查询（例如询问实际第 5 份）：
<query_retrieve>5</query_retrieve>

提交最终答案时，必须说明盲排策略（A、B、C 或 D）并给出第 {k} 份的考生考号，格式如下：
<answer>type=B, name=考生考号</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The examination center compiled an initial grading stack T of {n} exam papers, indexed from 1 to {n}. Each position i logs:
- A Candidate ID name[i] (publicly known, see below)
- A binary perfect-score attribute for objective questions b[i] (publicly known, see below)

Sequence information:
{sequence_info}

To prevent grading fatigue, the distribution system applied one of four blind-shuffling strategies to sequence T to generate the actual distribution sequence S, which is hidden from you. The four strategies are:
- A (Unchanged): Keep the grading order unchanged
- B (Completely reversed): Completely reverse the stack
- C (Bottom to Top): Move the bottom paper to the top
- D (Top to Bottom): Move the top paper to the bottom

Your goal is to deduce the blind-shuffling strategy used and the Candidate ID at position {k} in the actual distribution sequence S.

You can repeatedly ask the following queries (one per turn):
1. Probe Query: Ask for the perfect-score attribute at position i in the actual sequence S. I will return 0 or 1.
2. Retrieve Query: Ask for the Candidate ID at position j in the actual sequence S. I will return the corresponding ID.

When you have enough information, submit your final answer. Incorrect answers or formats result in quality assurance failure.

Each query must contain only one tag. Use the following XML format:
- Probe Query (e.g., asking about position 3):
<query_probe>3</query_probe>
- Retrieve Query (e.g., asking about position 5):
<query_retrieve>5</query_retrieve>

When submitting the final answer, specify the strategy type (A, B, C, or D) and the Candidate ID at position {k}, formatted as:
<answer>type=B, name=CandidateID</answer>
"""

    contextualized_rule_zh_4 = """\
自动化流水线上的机械臂正面临一组包含 {n} 个工件的初始加工序列 T，编号从 1 到 {n}。每个工位 i 包含：
- 工件批号 name[i]（已公开，见下方）
- 是否需要深加工的二值属性 b[i]（已公开，见下方）

序列信息：
{sequence_info}

主控 PLC 随机执行了四种进料置换算法之一，将初始序列 T 转化为实际执行的加工序列 S，但你无法读取 S 的明文。四种置换算法为：
- A（直通进料）：保持原加工序列不变
- B（反转进料）：将加工序列完全倒序
- C（尾件循环）：最后一个工件循环至首部加工
- D（首件循环）：第一个工件循环至尾部加工

你的任务是破解主控执行的置换算法类型，并查明实际加工序列 S 中第 {k} 个被加工的工件批号。

你可以反复向我提出以下诊断查询（每次仅限一个问题）：
1. 探测查询：询问实际加工序列 S 中第 i 位的深加工属性是多少。我会返回 0 或 1。
2. 检索查询：询问实际加工序列 S 中第 j 位的工件批号是什么。我会返回对应批号。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，流水线将急停报警。

每次询问只能包含一个标签，使用以下 XML 格式：
- 探测查询（例如询问实际第 3 位）：
<query_probe>3</query_probe>
- 检索查询（例如询问实际第 5 位）：
<query_retrieve>5</query_retrieve>

提交最终答案时，必须说明置换算法（A、B、C 或 D）并给出第 {k} 位的工件批号，格式如下：
<answer>type=B, name=工件批号</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
The robotic arm on the automated assembly line faces an initial processing sequence T of {n} workpieces, indexed from 1 to {n}. Each station i contains:
- A Batch ID name[i] (publicly known, see below)
- A binary deep-processing attribute b[i] (publicly known, see below)

Sequence information:
{sequence_info}

The main PLC randomly executed one of four feeding permutation algorithms to convert sequence T into the actual executed processing sequence S, which is encrypted. The four algorithms are:
- A (Direct feed): Keep the original processing sequence unchanged
- B (Reverse feed): Completely reverse the processing sequence
- C (Tail cycle): Cycle the last workpiece to the front
- D (Head cycle): Cycle the first workpiece to the tail

Your task is to crack the permutation algorithm used by the PLC and identify the Batch ID at position {k} in the actual processing sequence S.

You can repeatedly ask the following diagnostic queries (one per turn):
1. Probe Query: Ask for the deep-processing attribute at position i in the actual sequence S. I will return 0 or 1.
2. Retrieve Query: Ask for the Batch ID at position j in the actual sequence S. I will return the corresponding ID.

When you have enough information, submit your final answer. Incorrect answers or formats will trigger an emergency stop alarm.

Each query must contain only one tag. Use the following XML format:
- Probe Query (e.g., asking about position 3):
<query_probe>3</query_probe>
- Retrieve Query (e.g., asking about position 5):
<query_retrieve>5</query_retrieve>

When submitting the final answer, specify the algorithm type (A, B, C, or D) and the Batch ID at position {k}, formatted as:
<answer>type=B, name=BatchID</answer>
"""

    contextualized_rule_zh_5 = """\
法院书记员排列了一份包含 {n} 份证据的初始质证清单 T，编号从 1 到 {n}。每个序号 i 对应：
- 证据卷宗号 name[i]（已公开，见下方）
- 是否属于核心物证的二值属性 b[i]（已公开，见下方）

序列信息：
{sequence_info}

为了进行交叉检验，主审法官秘密选用了四种出示规则之一，将初始清单 T 调整为实际的庭审质证顺序 S，双方代理人无法直接看到 S。四种出示规则为：
- A（按原清单）：保持初始顺序出示
- B（完全倒序）：将质证清单完全倒序出示
- C（压轴先验）：最后一份证据最先出示
- D（首件后置）：第一份证据留到最后出示

你需要推断出法官使用的出示规则，并指出实际质证顺序 S 中第 {k} 个出示的证据卷宗号。

你可以反复向法庭提出以下查询（每次仅限一个问题）：
1. 探测查询：询问实际质证顺序 S 中第 i 位证据的核心物证属性是多少。法庭会返回 0 或 1。
2. 检索查询：询问实际质证顺序 S 中第 j 位的证据卷宗号是什么。法庭会返回对应卷宗号。

当你收集足够信息后，请提交最终代理意见。若答案错误或格式不符，法庭质证失败。

每次询问只能包含一个标签，使用以下 XML 格式：
- 探测查询（例如询问实际第 3 位）：
<query_probe>3</query_probe>
- 检索查询（例如询问实际第 5 位）：
<query_retrieve>5</query_retrieve>

提交最终答案时，必须说明出示规则（A、B、C 或 D）并给出第 {k} 位的证据卷宗号，格式如下：
<answer>type=B, name=卷宗号</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
The court clerk arranged an initial cross-examination list T of {n} pieces of evidence, indexed from 1 to {n}. Each index i corresponds to:
- An Evidence File ID name[i] (publicly known, see below)
- A binary core-evidence attribute b[i] (publicly known, see below)

Sequence information:
{sequence_info}

For cross-validation, the presiding judge secretly selected one of four presentation rules to adjust the initial list T into the actual trial cross-examination sequence S, which the agents cannot see directly. The four rules are:
- A (Original list): Present in the initial order
- B (Reversed order): Present the list in completely reversed order
- C (Finale first): Present the last piece of evidence first
- D (First to last): Leave the first piece of evidence to be presented last

You must deduce the presentation rule used by the judge and identify the Evidence File ID presented at position {k} in the actual sequence S.

You can repeatedly ask the court the following queries (one per turn):
1. Probe Query: Ask for the core-evidence attribute at position i in the actual sequence S. The court will return 0 or 1.
2. Retrieve Query: Ask for the Evidence File ID at position j in the actual sequence S. The court will return the corresponding File ID.

When you have enough information, submit your final agency opinion. Incorrect answers or formats result in cross-examination failure.

Each query must contain only one tag. Use the following XML format:
- Probe Query (e.g., asking about position 3):
<query_probe>3</query_probe>
- Retrieve Query (e.g., asking about position 5):
<query_retrieve>5</query_retrieve>

When submitting the final answer, specify the presentation rule (A, B, C, or D) and the Evidence File ID at position {k}, formatted as:
<answer>type=B, name=FileID</answer>
"""

    tags = ["answer", "query_probe", "query_retrieve"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "k": 2,
                "names": ["苹果", "香蕉", "橙子", "葡萄"],
                "bits": [0, 1, 0, 1],
                "perm_type": "B",
            },
            2: {
                "n": 6,
                "k": 3,
                "names": ["猫", "狗", "兔", "鸟", "鱼", "鼠"],
                "bits": [1, 0, 1, 0, 1, 0],
                "perm_type": "C",
            },
            3: {
                "n": 8,
                "k": 5,
                "names": ["春", "夏", "秋", "冬", "风", "雨", "雪", "云"],
                "bits": [0, 1, 1, 0, 1, 0, 0, 1],
                "perm_type": "D",
            },
            4: {
                "n": 10,
                "k": 7,
                "names": ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"],
                "bits": [1, 0, 1, 1, 0, 0, 1, 0, 1, 0],
                "perm_type": "A",
            },
            5: {
                "n": 12,
                "k": 9,
                "names": ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"],
                "bits": [0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1],
                "perm_type": "C",
            },
        },
        "en": {
            1: {
                "n": 4,
                "k": 2,
                "names": ["Apple", "Banana", "Orange", "Grape"],
                "bits": [0, 1, 0, 1],
                "perm_type": "B",
            },
            2: {
                "n": 6,
                "k": 3,
                "names": ["Cat", "Dog", "Rabbit", "Bird", "Fish", "Mouse"],
                "bits": [1, 0, 1, 0, 1, 0],
                "perm_type": "C",
            },
            3: {
                "n": 8,
                "k": 5,
                "names": ["Spring", "Summer", "Autumn", "Winter", "Wind", "Rain", "Snow", "Cloud"],
                "bits": [0, 1, 1, 0, 1, 0, 0, 1],
                "perm_type": "D",
            },
            4: {
                "n": 10,
                "k": 7,
                "names": ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta", "Iota", "Kappa"],
                "bits": [1, 0, 1, 1, 0, 0, 1, 0, 1, 0],
                "perm_type": "A",
            },
            5: {
                "n": 12,
                "k": 9,
                "names": ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"],
                "bits": [0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1],
                "perm_type": "C",
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
        
        self.n = cfg["n"]
        self.k = cfg["k"]
        self.names = cfg["names"]
        self.bits = cfg["bits"]
        self.perm_type = cfg["perm_type"]
        
        self._game_info["n"] = self.n
        self._game_info["k"] = self.k
        
        if lang == "zh":
            seq_lines = [f"位置 {i+1}: 名称=\"{self.names[i]}\", 二值属性={self.bits[i]}" 
                        for i in range(self.n)]
        else:
            seq_lines = [f"Position {i+1}: name=\"{self.names[i]}\", binary_attribute={self.bits[i]}" 
                        for i in range(self.n)]
        self._game_info["sequence_info"] = "\n".join(seq_lines)
        
        self.true_order = self._apply_permutation()

    def _apply_permutation(self):
        n = self.n
        true_order = []
        
        for i in range(1, n + 1):
            if self.perm_type == "A":
                p_i = i
            elif self.perm_type == "B":
                p_i = n + 1 - i
            elif self.perm_type == "C":
                p_i = ((i - 2) % n) + 1
            elif self.perm_type == "D":
                p_i = (i % n) + 1
            else:
                raise ValueError(f"Unknown permutation type: {self.perm_type}")
            
            true_order.append({
                "name": self.names[p_i - 1],
                "bit": self.bits[p_i - 1]
            })
        
        return true_order

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        parts = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        
        for part in parts:
            if "=" in part:
                k, v = part.split("=", 1)
                ans_dict[k.strip()] = v.strip()
        
        if "type" not in ans_dict or "name" not in ans_dict:
            return False
        
        if ans_dict["type"] != self.perm_type:
            return False
        
        correct_name = self.true_order[self.k - 1]["name"]
        
        return ans_dict["name"] == correct_name

    def _cf_core_produce(self, parsed_info):
        
        if "query_probe" in parsed_info:
            try:
                idx = int(parsed_info["query_probe"].strip())
                if idx < 1 or idx > self.n:
                    if self.config.language == "zh":
                        return "错误：位置超出范围。"
                    else:
                        return "Error: Position out of range."
                
                bit_value = self.true_order[idx - 1]["bit"]
                return str(bit_value)
            
            except ValueError:
                if self.config.language == "zh":
                    return "错误：位置必须是整数。"
                else:
                    return "Error: Position must be an integer."
        
        elif "query_retrieve" in parsed_info:
            try:
                idx = int(parsed_info["query_retrieve"].strip())
                if idx < 1 or idx > self.n:
                    if self.config.language == "zh":
                        return "错误：位置超出范围。"
                    else:
                        return "Error: Position out of range."
                
                name = self.true_order[idx - 1]["name"]
                return name
            
            except ValueError:
                if self.config.language == "zh":
                    return "错误：位置必须是整数。"
                else:
                    return "Error: Position must be an integer."
        
        else:
            if self.config.language == "zh":
                return "错误：未找到有效的查询标签。"
            else:
                return "Error: No valid query tag found."

    def _cf_make_wrong(self, correct):
        if correct in ("0", "1"):
            return "1" if correct == "0" else "0"
        for name in self.names:
            if name != correct:
                return name
        return correct + "_wrong"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        for i in range(1, self.n + 1):
            query_str = f"<query_probe>{i}</query_probe>"
            ans = str(self.true_order[i - 1]["bit"])
            results.append({
                "query": query_str,
                "answer": ans
            })

        for i in range(1, self.n + 1):
            query_str = f"<query_retrieve>{i}</query_retrieve>"
            ans = self.true_order[i - 1]["name"]
            results.append({
                "query": query_str,
                "answer": ans
            })
            
        return results