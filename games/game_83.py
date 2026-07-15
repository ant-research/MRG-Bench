from .base import Game
import random

class SymbolDecodingGame(Game):

    game_rule_zh = """\
我们现在来玩一个"符号解码"推理游戏，规则如下：

游戏设定了一个未知的非负整数 V（目标值），以及一个固定但未知的双射编码映射 σ，它将十个十进制数字 0,1,2,3,4,5,6,7,8,9 分别对应到十个大写字母 A,B,C,D,E,F,G,H,I,J（一一对应，整个游戏过程中不变）。

游戏中有三种"数据源"可供你选择切换：

1. Star(t)：输出值为 t（t 为你指定的任意正整数）。
2. Path(t)：输出值为 1（当 t=1 时）或 2（当 t 大于等于 2 时），t 为你指定的任意正整数。
3. Target：输出值为未知的目标值 V。

当你选择某个数据源后，可以请求"报告"当前源的编码表示：系统会将该源的输出值按十进制表示，逐位数字通过 σ 映射为字母，并返回结果字符串（无前导零）。

你的目标是：

- 通过多轮切换数据源并观察编码结果，推断出完整的映射 σ；
- 解码 Target 的编码得到真实值 V；
- 最终提交你对 σ 的猜测以及 V 的猜测。

你需要尽可能少地进行询问。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 切换到 Star(t) 数据源（例如 t=123）：
<build_star>123</build_star>

- 切换到 Path(t) 数据源（例如 t=5）：
<build_path>5</build_path>

- 切换到 Target 数据源：
<reset_target></reset_target>

- 请求当前数据源的编码报告：
<report></report>

提交最终答案时，必须同时给出映射 σ 和目标值 V。格式如下：

<answer>mapping=0:A,1:B,2:C,3:D,4:E,5:F,6:G,7:H,8:I,9:J; value=12345</answer>

其中 mapping 部分列出所有十个数字到字母的对应关系（用逗号隔开，顺序不限），value 部分给出你猜测的 V 的十进制表示。
"""

    game_rule_en = """\
Let's play a "Symbol Decoding" deduction game. Here are the rules:

The game has set up an unknown non-negative integer V (the target value), and a fixed but unknown bijection encoding σ that maps the ten decimal digits 0,1,2,3,4,5,6,7,8,9 to ten uppercase letters A,B,C,D,E,F,G,H,I,J (one-to-one correspondence, unchanged throughout the game).

There are three "data sources" you can switch between:

1. Star(t): outputs the value t (t is any positive integer you specify).
2. Path(t): outputs 1 (when t=1) or 2 (when t is greater than or equal to 2), where t is any positive integer you specify.
3. Target: outputs the unknown target value V.

After selecting a data source, you can request a "report" of the current source's encoded representation: the system will take the source's output value in decimal notation, map each digit through σ to a letter, and return the result string (without leading zeros).

Your goal is:

- Infer the complete mapping σ by switching data sources and observing encoded results through multiple rounds;
- Decode Target's encoding to obtain the real value V;
- Finally submit your guess of σ and V.

You should try to minimize the number of queries.

Each query must contain only one tag. Use the following XML format:

- Switch to Star(t) data source (e.g., t=123):
<build_star>123</build_star>

- Switch to Path(t) data source (e.g., t=5):
<build_path>5</build_path>

- Switch to Target data source:
<reset_target></reset_target>

- Request the encoded report of the current data source:
<report></report>

When submitting the final answer, you must provide both the mapping σ and the target value V. Format as follows:

<answer>mapping=0:A,1:B,2:C,3:D,4:E,5:F,6:G,7:H,8:I,9:J; value=12345</answer>

Where the mapping part lists all ten digit-to-letter correspondences (comma-separated, order does not matter), and the value part gives your guessed decimal representation of V.
"""

    contextualized_rule_zh_1 = """\
【智慧交通系统排查】我们现在来玩一个"符号解码"推理游戏，规则如下：

交通管理部门正在追踪一辆肇事逃逸的车辆。系统设定了一个未知的非负整数 V（逃逸车辆的核心识别码），以及一个固定但未知的双射编码映射 σ，它将十个十进制数字 0,1,2,3,4,5,6,7,8,9 分别对应到十个大写字母 A,B,C,D,E,F,G,H,I,J（一一对应，作为加密传输协议，整个排查过程中不变）。

交管系统中有三种"数据源"可供你选择切换：

1. Star(t) [模拟车牌生成器]：输出值为 t（t 为你指定的任意正整数测试序列）。
2. Path(t) [车道状态探测器]：输出值为 1（当指定车道 t=1 时）或 2（当车道 t 大于等于 2 时），t 为你指定的任意正整数。
3. Target [嫌疑车辆追踪器]：输出值为未知的目标识别码 V。

当你选择某个数据源后，可以请求"报告"当前源的加密表示：系统会将该源的输出值按十进制表示，逐位数字通过 σ 映射为字母，并返回结果字符串（无前导零）。

你的目标是：
- 通过多轮切换数据源并观察加密结果，推推断出完整的映射 σ；
- 解码 Target 的加密数据得到真实识别码 V；
- 最终提交你对 σ 的猜测以及 V 的猜测。

你需要尽可能少地进行询问。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 切换到 Star(t) 数据源（例如 t=123）：
<build_star>123</build_star>

- 切换到 Path(t) 数据源（例如 t=5）：
<build_path>5</build_path>

- 切换到 Target 数据源：
<reset_target></reset_target>

- 请求当前数据源的编码报告：
<report></report>

提交最终答案时，必须同时给出映射 σ 和目标值 V。格式如下：

<answer>mapping=0:A,1:B,2:C,3:D,4:E,5:F,6:G,7:H,8:I,9:J; value=12345</answer>

其中 mapping 部分列出所有十个数字到字母的对应关系（用逗号隔开，顺序不限），value 部分给出你猜测的 V 的十进制表示。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's play a "Symbol Decoding" deduction game under the context of smart traffic management. Here are the rules:

The traffic authority is tracking a hit-and-run vehicle. The system has set up an unknown non-negative integer V (the target vehicle's core ID), and a fixed but unknown bijection encoding σ that maps the ten decimal digits 0,1,2,3,4,5,6,7,8,9 to ten uppercase letters A,B,C,D,E,F,G,H,I,J (one-to-one correspondence, serving as an encrypted communication protocol, unchanged throughout the game).

There are three "data sources" in the traffic system you can switch between:

1. Star(t) [Simulated ID Generator]: outputs the value t (t is any positive integer test sequence you specify).
2. Path(t) [Lane Status Detector]: outputs 1 (when lane t=1) or 2 (when lane t is greater than or equal to 2), where t is any positive integer you specify.
3. Target [Suspect Tracker]: outputs the unknown target ID V.

After selecting a data source, you can request a "report" of the current source's encrypted representation: the system will take the source's output value in decimal notation, map each digit through σ to a letter, and return the result string (without leading zeros).

Your goal is:
- Infer the complete mapping σ by switching data sources and observing encrypted results through multiple rounds;
- Decode the Target's encrypted data to obtain the real ID V;
- Finally submit your guess of σ and V.

You should try to minimize the number of queries.

Each query must contain only one tag. Use the following XML format:

- Switch to Star(t) data source (e.g., t=123):
<build_star>123</build_star>

- Switch to Path(t) data source (e.g., t=5):
<build_path>5</build_path>

- Switch to Target data source:
<reset_target></reset_target>

- Request the encrypted report of the current data source:
<report></report>

When submitting the final answer, you must provide both the mapping σ and the target value V. Format as follows:

<answer>mapping=0:A,1:B,2:C,3:D,4:E,5:F,6:G,7:H,8:I,9:J; value=12345</answer>

Where the mapping part lists all ten digit-to-letter correspondences (comma-separated, order does not matter), and the value part gives your guessed decimal representation of V.
"""

    contextualized_rule_zh_2 = """\
【传染病溯源排查】我们现在来玩一个"符号解码"推理游戏，规则如下：

疾控中心正在追踪一种未知病毒的"零号病人"。系统设定了一个未知的非负整数 V（零号病人的核心基因序列编号），以及一个固定但未知的双射编码映射 σ，它将十个十进制数字 0,1,2,3,4,5,6,7,8,9 分别对应到十个大写字母 A,B,C,D,E,F,G,H,I,J（一一对应，作为基因组脱敏算法，整个排查过程中不变）。

医疗数据库中有三种"数据源"可供你选择切换：

1. Star(t) [合成对照组]：输出值为 t（t 为你指定的任意正整数人工序列号）。
2. Path(t) [靶向药效测试]：输出值为 1（当药物剂量 t=1 时）或 2（当剂量 t 大于等于 2 时），t 为你指定的任意正整数。
3. Target [零号病人样本]：输出值为未知的目标序列编号 V。

当你选择某个数据源后，可以请求"报告"当前源的脱敏测序结果：系统会将该源的输出值按十进制表示，逐位数字通过 σ 映射为字母，并返回结果字符串（无前导零）。

你的目标是：
- 通过多轮切换数据源并观察测序结果，推断出完整的映射 σ；
- 解码 Target 的脱敏数据得到真实的序列编号 V；
- 最终提交你对 σ 的猜测以及 V 的猜测。

你需要尽可能少地进行询问。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 切换到 Star(t) 数据源（例如 t=123）：
<build_star>123</build_star>

- 切换到 Path(t) 数据源（例如 t=5）：
<build_path>5</build_path>

- 切换到 Target 数据源：
<reset_target></reset_target>

- 请求当前数据源的编码报告：
<report></report>

提交最终答案时，必须同时给出映射 σ 和目标值 V。格式如下：

<answer>mapping=0:A,1:B,2:C,3:D,4:E,5:F,6:G,7:H,8:I,9:J; value=12345</answer>

其中 mapping 部分列出所有十个数字到字母的对应关系（用逗号隔开，顺序不限），value 部分给出你猜测的 V 的十进制表示。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's play a "Symbol Decoding" deduction game under the context of infectious disease tracing. Here are the rules:

The CDC is tracking the "Patient Zero" of an unknown virus. The system has set up an unknown non-negative integer V (the core genetic sequence ID of Patient Zero), and a fixed but unknown bijection encoding σ that maps the ten decimal digits 0,1,2,3,4,5,6,7,8,9 to ten uppercase letters A,B,C,D,E,F,G,H,I,J (one-to-one correspondence, serving as a genomic desensitization algorithm, unchanged throughout the tracing process).

There are three "data sources" in the medical database you can switch between:

1. Star(t) [Synthetic Control Group]: outputs the value t (t is any positive integer artificial sequence ID you specify).
2. Path(t) [Targeted Drug Efficacy Test]: outputs 1 (when drug dose t=1) or 2 (when dose t is greater than or equal to 2), where t is any positive integer you specify.
3. Target [Patient Zero Sample]: outputs the unknown target sequence ID V.

After selecting a data source, you can request a "report" of the current source's desensitized sequencing result: the system will take the source's output value in decimal notation, map each digit through σ to a letter, and return the result string (without leading zeros).

Your goal is:
- Infer the complete mapping σ by switching data sources and observing sequencing results through multiple rounds;
- Decode the Target's desensitized data to obtain the real sequence ID V;
- Finally submit your guess of σ and V.

You should try to minimize the number of queries.

Each query must contain only one tag. Use the following XML format:

- Switch to Star(t) data source (e.g., t=123):
<build_star>123</build_star>

- Switch to Path(t) data source (e.g., t=5):
<build_path>5</build_path>

- Switch to Target data source:
<reset_target></reset_target>

- Request the encoded report of the current data source:
<report></report>

When submitting the final answer, you must provide both the mapping σ and the target value V. Format as follows:

<answer>mapping=0:A,1:B,2:C,3:D,4:E,5:F,6:G,7:H,8:I,9:J; value=12345</answer>

Where the mapping part lists all ten digit-to-letter correspondences (comma-separated, order does not matter), and the value part gives your guessed decimal representation of V.
"""

    contextualized_rule_zh_3 = """\
【考试泄密调查】我们现在来玩一个"符号解码"推理游戏，规则如下：

教育局正在调查一份严重泄露的绝密考卷。系统设定了一个未知的非负整数 V（泄密考卷的防伪特征码），以及一个固定但未知的双射编码映射 σ，它将十个十进制数字 0,1,2,3,4,5,6,7,8,9 分别对应到十个大写字母 A,B,C,D,E,F,G,H,I,J（一一对应，作为阅卷系统的盲评加密映射，整个调查过程中不变）。

阅卷系统中有三种"数据源"可供你选择切换：

1. Star(t) [提交模拟测试卷]：输出值为 t（t 为你指定的任意正整数分值）。
2. Path(t) [难度评级引擎]：输出值为 1（当题目层级 t=1 时）或 2（当题目层级 t 大于等于 2 时），t 为你指定的任意正整数。
3. Target [定位泄密考卷]：输出值为未知的防伪特征码 V。

当你选择某个数据源后，可以请求"报告"当前源的盲评加密结果：系统会将该源的输出值按十进制表示，逐位数字通过 σ 映射为字母，并返回结果字符串（无前导零）。

你的目标是：
- 通过多轮切换数据源并观察加密结果，推断出完整的映射 σ；
- 解码 Target 的盲评数据得到真实的防伪特征码 V；
- 最终提交你对 σ 的猜测以及 V 的猜测。

你需要尽可能少地进行询问。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 切换到 Star(t) 数据源（例如 t=123）：
<build_star>123</build_star>

- 切换到 Path(t) 数据源（例如 t=5）：
<build_path>5</build_path>

- 切换到 Target 数据源：
<reset_target></reset_target>

- 请求当前数据源的编码报告：
<report></report>

提交最终答案时，必须同时给出映射 σ 和目标值 V。格式如下：

<answer>mapping=0:A,1:B,2:C,3:D,4:E,5:F,6:G,7:H,8:I,9:J; value=12345</answer>

其中 mapping 部分列出所有十个数字到字母的对应关系（用逗号隔开，顺序不限），value 部分给出你猜测的 V 的十进制表示。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Symbol Decoding" deduction game under the context of an exam leak investigation. Here are the rules:

The Education Bureau is investigating a highly confidential leaked exam paper. The system has set up an unknown non-negative integer V (the anti-counterfeiting characteristic code of the leaked paper), and a fixed but unknown bijection encoding σ that maps the ten decimal digits 0,1,2,3,4,5,6,7,8,9 to ten uppercase letters A,B,C,D,E,F,G,H,I,J (one-to-one correspondence, serving as a blind-grading encryption mapping in the exam system, unchanged throughout the investigation).

There are three "data sources" in the grading system you can switch between:

1. Star(t) [Submit Mock Exam]: outputs the value t (t is any positive integer score you specify).
2. Path(t) [Difficulty Rating Engine]: outputs 1 (when question level t=1) or 2 (when question level t is greater than or equal to 2), where t is any positive integer you specify.
3. Target [Locate Leaked Exam]: outputs the unknown characteristic code V.

After selecting a data source, you can request a "report" of the current source's blind-grading encrypted result: the system will take the source's output value in decimal notation, map each digit through σ to a letter, and return the result string (without leading zeros).

Your goal is:
- Infer the complete mapping σ by switching data sources and observing encrypted results through multiple rounds;
- Decode the Target's encrypted data to obtain the real characteristic code V;
- Finally submit your guess of σ and V.

You should try to minimize the number of queries.

Each query must contain only one tag. Use the following XML format:

- Switch to Star(t) data source (e.g., t=123):
<build_star>123</build_star>

- Switch to Path(t) data source (e.g., t=5):
<build_path>5</build_path>

- Switch to Target data source:
<reset_target></reset_target>

- Request the encoded report of the current data source:
<report></report>

When submitting the final answer, you must provide both the mapping σ and the target value V. Format as follows:

<answer>mapping=0:A,1:B,2:C,3:D,4:E,5:F,6:G,7:H,8:I,9:J; value=12345</answer>

Where the mapping part lists all ten digit-to-letter correspondences (comma-separated, order does not matter), and the value part gives your guessed decimal representation of V.
"""

    contextualized_rule_zh_4 = """\
【工控设备故障诊断】我们现在来玩一个"符号解码"推理游戏，规则如下：

智能制造车间的核心工业控制器发生异常。系统设定了一个未知的非负整数 V（故障设备的内部指令序列号），以及一个固定但未知的双射编码映射 σ，它将十个十进制数字 0,1,2,3,4,5,6,7,8,9 分别对应到十个大写字母 A,B,C,D,E,F,G,H,I,J（一一对应，作为工控机串行通信的掩码协议，整个诊断过程中不变）。

诊断总线中有三种"数据源"可供你选择切换：

1. Star(t) [诊断指令注入器]：输出值为 t（t 为你指定的任意正整数测试指令）。
2. Path(t) [传动轴状态传感器]：输出值为 1（当转速档位 t=1 时）或 2（当转速档位 t 大于等于 2 时），t 为你指定的任意正整数。
3. Target [故障设备捕获]：输出值为未知的故障序列号 V。

当你选择某个数据源后，可以请求"报告"当前源的掩码输出结果：系统会将该源的输出值按十进制表示，逐位数字通过 σ 映射为字母，并返回结果字符串（无前导零）。

你的目标是：
- 通过多轮切换数据源并观察示波器上的掩码输出，推断出完整的映射 σ；
- 解码 Target 的掩码数据得到真实的指令序列号 V；
- 最终提交你对 σ 的猜测以及 V 的猜测。

你需要尽可能少地进行询问。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 切换到 Star(t) 数据源（例如 t=123）：
<build_star>123</build_star>

- 切换到 Path(t) 数据源（例如 t=5）：
<build_path>5</build_path>

- 切换到 Target 数据源：
<reset_target></reset_target>

- 请求当前数据源的编码报告：
<report></report>

提交最终答案时，必须同时给出映射 σ 和目标值 V。格式如下：

<answer>mapping=0:A,1:B,2:C,3:D,4:E,5:F,6:G,7:H,8:I,9:J; value=12345</answer>

其中 mapping 部分列出所有十个数字到字母的对应关系（用逗号隔开，顺序不限），value 部分给出你猜测的 V 的十进制表示。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's play a "Symbol Decoding" deduction game under the context of industrial control equipment troubleshooting. Here are the rules:

The core industrial controller in a smart manufacturing workshop is malfunctioning. The system has set up an unknown non-negative integer V (the internal instruction sequence number of the faulty device), and a fixed but unknown bijection encoding σ that maps the ten decimal digits 0,1,2,3,4,5,6,7,8,9 to ten uppercase letters A,B,C,D,E,F,G,H,I,J (one-to-one correspondence, serving as the mask protocol for serial communication in the IPC, unchanged throughout the diagnosis).

There are three "data sources" on the diagnostic bus you can switch between:

1. Star(t) [Diagnostic Instruction Injector]: outputs the value t (t is any positive integer test instruction you specify).
2. Path(t) [Drive Shaft Status Sensor]: outputs 1 (when speed gear t=1) or 2 (when speed gear t is greater than or equal to 2), where t is any positive integer you specify.
3. Target [Faulty Device Capture]: outputs the unknown fault sequence number V.

After selecting a data source, you can request a "report" of the current source's masked output result: the system will take the source's output value in decimal notation, map each digit through σ to a letter, and return the result string (without leading zeros).

Your goal is:
- Infer the complete mapping σ by switching data sources and observing the masked output on the oscilloscope through multiple rounds;
- Decode the Target's masked data to obtain the real instruction sequence number V;
- Finally submit your guess of σ and V.

You should try to minimize the number of queries.

Each query must contain only one tag. Use the following XML format:

- Switch to Star(t) data source (e.g., t=123):
<build_star>123</build_star>

- Switch to Path(t) data source (e.g., t=5):
<build_path>5</build_path>

- Switch to Target data source:
<reset_target></reset_target>

- Request the encoded report of the current data source:
<report></report>

When submitting the final answer, you must provide both the mapping σ and the target value V. Format as follows:

<answer>mapping=0:A,1:B,2:C,3:D,4:E,5:F,6:G,7:H,8:I,9:J; value=12345</answer>

Where the mapping part lists all ten digit-to-letter correspondences (comma-separated, order does not matter), and the value part gives your guessed decimal representation of V.
"""

    contextualized_rule_zh_5 = """\
【跨国洗钱网络追踪】我们现在来玩一个"符号解码"推理游戏，规则如下：

司法部正在调查一个复杂的跨国洗钱网络。系统设定了一个未知的非负整数 V（涉案离岸账户的隐藏资金流水号），以及一个固定但未知的双射编码映射 σ，它将十个十进制数字 0,1,2,3,4,5,6,7,8,9 分别对应到十个大写字母 A,B,C,D,E,F,G,H,I,J（一一对应，作为暗网账本的加密代换表，整个调查过程中不变）。

金融追踪系统中有三种"数据源"可供你选择切换：

1. Star(t) [设立诱饵交易]：输出值为 t（t 为你指定的任意正整数虚构金额）。
2. Path(t) [司法管辖区探针]：输出值为 1（当管辖层级 t=1 时）或 2（当管辖层级 t 大于等于 2 时），t 为你指定的任意正整数。
3. Target [涉案账户追踪]：输出值为未知的资金流水号 V。

当你选择某个数据源后，可以请求"报告"当前源的加密账本记录：系统会将该源的输出值按十进制表示，逐位数字通过 σ 映射为字母，并返回结果字符串（无前导零）。

你的目标是：
- 通过多轮切换数据源并观察暗网账本记录，推断出完整的映射 σ；
- 解码 Target 的账本数据得到真实的资金流水号 V；
- 最终提交你对 σ 的猜测以及 V 的猜测。

你需要尽可能少地进行询问。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 切换到 Star(t) 数据源（例如 t=123）：
<build_star>123</build_star>

- 切换到 Path(t) 数据源（例如 t=5）：
<build_path>5</build_path>

- 切换到 Target 数据源：
<reset_target></reset_target>

- 请求当前数据源的编码报告：
<report></report>

提交最终答案时，必须同时给出映射 σ 和目标值 V。格式如下：

<answer>mapping=0:A,1:B,2:C,3:D,4:E,5:F,6:G,7:H,8:I,9:J; value=12345</answer>

其中 mapping 部分列出所有十个数字到字母的对应关系（用逗号隔开，顺序不限），value 部分给出你猜测的 V 的十进制表示。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's play a "Symbol Decoding" deduction game under the context of tracking a transnational money laundering network. Here are the rules:

The Department of Justice is investigating a complex transnational money laundering network. The system has set up an unknown non-negative integer V (the hidden transaction flow number of the offshore account involved), and a fixed but unknown bijection encoding σ that maps the ten decimal digits 0,1,2,3,4,5,6,7,8,9 to ten uppercase letters A,B,C,D,E,F,G,H,I,J (one-to-one correspondence, serving as a cryptographic substitution table for the dark web ledger, unchanged throughout the investigation).

There are three "data sources" in the financial tracking system you can switch between:

1. Star(t) [Set up Decoy Transaction]: outputs the value t (t is any positive integer fictitious amount you specify).
2. Path(t) [Jurisdiction Probe]: outputs 1 (when jurisdiction level t=1) or 2 (when jurisdiction level t is greater than or equal to 2), where t is any positive integer you specify.
3. Target [Target Account Tracking]: outputs the unknown transaction flow number V.

After selecting a data source, you can request a "report" of the current source's encrypted ledger record: the system will take the source's output value in decimal notation, map each digit through σ to a letter, and return the result string (without leading zeros).

Your goal is:
- Infer the complete mapping σ by switching data sources and observing the dark web ledger records through multiple rounds;
- Decode the Target's ledger data to obtain the real transaction flow number V;
- Finally submit your guess of σ and V.

You should try to minimize the number of queries.

Each query must contain only one tag. Use the following XML format:

- Switch to Star(t) data source (e.g., t=123):
<build_star>123</build_star>

- Switch to Path(t) data source (e.g., t=5):
<build_path>5</build_path>

- Switch to Target data source:
<reset_target></reset_target>

- Request the encoded report of the current data source:
<report></report>

When submitting the final answer, you must provide both the mapping σ and the target value V. Format as follows:

<answer>mapping=0:A,1:B,2:C,3:D,4:E,5:F,6:G,7:H,8:I,9:J; value=12345</answer>

Where the mapping part lists all ten digit-to-letter correspondences (comma-separated, order does not matter), and the value part gives your guessed decimal representation of V.
"""

    tags = ["answer", "build_star", "build_path", "reset_target", "report"]
    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        1: {"target_value": 7, "seed": 42},
        2: {"target_value": 34, "seed": 123},
        3: {"target_value": 582, "seed": 456},
        4: {"target_value": 4096, "seed": 789},
        5: {"target_value": 73821, "seed": 1024},
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)
        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")
        cfg = self.DIFFICULTY_CONFIG[diff]
        self.target_value = cfg["target_value"]
        rng = random.Random(cfg["seed"])
        digits = list("0123456789")
        letters = list("ABCDEFGHIJ")
        rng.shuffle(letters)
        self.sigma = {digits[i]: letters[i] for i in range(10)}
        self.sigma_inv = {letters[i]: digits[i] for i in range(10)}
        self.current_source = None
        self.current_value = None
        self._game_info = {}

    def _encode_value(self, value):
        decimal_str = str(value)
        encoded = "".join(self.sigma[d] for d in decimal_str)
        return encoded

    def _parse_mapping(self, mapping_str):
        try:
            pairs = [x.strip() for x in mapping_str.split(",")]
            mapping = {}
            for pair in pairs:
                digit, letter = pair.split(":")
                mapping[digit.strip()] = letter.strip()
            return mapping
        except:
            return None

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        try:
            parts = raw_ans.split(";")
            if len(parts) != 2:
                return False
            mapping_part = parts[0].strip()
            value_part = parts[1].strip()
            if not mapping_part.startswith("mapping="):
                return False
            mapping_str = mapping_part[8:]
            user_mapping = self._parse_mapping(mapping_str)
            if user_mapping is None or len(user_mapping) != 10:
                return False
            if user_mapping != self.sigma:
                return False
            if not value_part.startswith("value="):
                return False
            value_str = value_part[6:]
            user_value = int(value_str)
            if user_value != self.target_value:
                return False
            return True
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            ok_msg = "确认"
            error_msg = "错误：无效的参数或格式。"
        else:
            ok_msg = "OK"
            error_msg = "Error: Invalid parameter or format."

        if "build_star" in parsed_info:
            try:
                t = int(parsed_info["build_star"].strip())
                if t <= 0:
                    return error_msg
                self.current_source = "star"
                self.current_value = t
                return ok_msg
            except:
                return error_msg
        elif "build_path" in parsed_info:
            try:
                t = int(parsed_info["build_path"].strip())
                if t <= 0:
                    return error_msg
                self.current_source = "path"
                if t == 1:
                    self.current_value = 1
                else:
                    self.current_value = 2
                return ok_msg
            except:
                return error_msg
        elif "reset_target" in parsed_info:
            self.current_source = "target"
            self.current_value = self.target_value
            return ok_msg
        elif "report" in parsed_info:
            if self.current_source is None:
                if self.config.language == "zh":
                    return "错误：尚未选择数据源。"
                else:
                    return "Error: No data source selected."
            encoded = self._encode_value(self.current_value)
            return encoded
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct in ("OK", "确认"):
            if self.config.language == "zh":
                return "错误：无效的参数或格式。"
            else:
                return "Error: Invalid parameter or format."
        if correct and all(c in "ABCDEFGHIJ" for c in correct):
            letters = list(correct)
            idx = random.randint(0, len(letters) - 1)
            available = [ch for ch in "ABCDEFGHIJ" if ch != letters[idx]]
            letters[idx] = random.choice(available)
            return "".join(letters)
        if correct.isdigit():
            return str(int(correct) + 1)
        if "是" in correct:
            return correct.replace("是", "否")
        if "否" in correct:
            return correct.replace("否", "是")
        if "Yes" in correct:
            return correct.replace("Yes", "No")
        if "yes" in correct:
            return correct.replace("yes", "no")
        if "No" in correct:
            return correct.replace("No", "Yes")
        if "no" in correct:
            return correct.replace("no", "yes")
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        if self.config.language == "zh":
            ok_msg = "确认"
        else:
            ok_msg = "OK"

        sample_numbers = list(range(1, 11))
        for t in sample_numbers:
            encoded = self._encode_value(t)
            queries.append({
                "query": f"<build_star>{t}</build_star>",
                "answer": f"{ok_msg}\n<report></report> → {encoded}"
            })

        path_samples = [1, 5]
        for t in path_samples:
            val = 1 if t == 1 else 2
            encoded = self._encode_value(val)
            queries.append({
                "query": f"<build_path>{t}</build_path>",
                "answer": f"{ok_msg}\n<report></report> → {encoded}"
            })

        target_encoded = self._encode_value(self.target_value)
        queries.append({
            "query": "<reset_target></reset_target>",
            "answer": f"{ok_msg}\n<report></report> → {target_encoded}"
        })

        return queries