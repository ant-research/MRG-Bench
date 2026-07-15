from .base import Game
import random

class SequenceAbstractReasoningGame(Game):

    contextualized_rule_zh_1 = """\
我们来模拟一个"智能车队序列分析"场景，规则如下：

系统监控着一个由 {n} 辆自动驾驶车辆组成的车队序列 S[1..{n}]，每辆车有一个互不相同的车辆ID（整数）。有一辆VIP目标车辆，初始位于车队首位 S[1]；该车辆的位置会随着车队队形的调整而改变。

监控系统存在一个未知的传感器工作模式 M，它属于 A、B、C、D 四种之一，决定"读取ID"指令会返回车队哪一端车辆的ID。四种模式如下：
- A: 每次读取均返回当前车队首端车辆的ID。
- B: 每次读取均返回当前车队尾端车辆的ID。
- C: 读取位置在首尾间交替，首次从首端开始；之后每次读取触发一次首尾切换。
- D: 读取位置在首尾间交替，首次从尾端开始；之后每次读取触发一次首尾切换。

注意：仅"读取ID"会触发 C/D 模式的首尾切换；其他队形操作或定位查询不改变切换状态。

你可以反复进行以下队形操作与查询（每次仅限一个操作或查询）：

- RotateL(k): 将首端车辆依次循环行驶至尾部 k 次，等价于车队循环左移 k 次。
- RotateR(k): 将尾端车辆依次循环行驶至首部 k 次，等价于车队循环右移 k 次。
- Reverse(): 将整个车队反转掉头行驶。
- Pass(): 保持当前队形，不进行操作。

所有队形操作都会相应更新VIP目标车辆在序列中的位置。

- LocateMark: 返回 Front（首端）、Back（尾端）或 Middle（非端点位置），表示VIP目标车辆当前所处的位置。该查询不暴露任何车辆ID数值且不影响 C/D 的切换状态。
- Value: 返回一个整数，为当前首端或尾端车辆的ID，具体由未知模式 M 决定；若 M 为 C 或 D，则每次调用后内部首尾读取状态切换一次。

通过尽可能少的操作与查询，最终同时给出：
- 传感器工作模式 M（A、B、C 或 D）
- VIP目标车辆（即原始 S[1]）的初始车辆ID数值

两者均正确则成功；任一错误则失败。

每次只能包含一个标签。请使用以下 XML 格式：

- 循环左移（例如左移 2 次）：
<rotate_left>2</rotate_left>

- 循环右移（例如右移 1 次）：
<rotate_right>1</rotate_right>

- 反转车队：
<reverse></reverse>

- 不操作：
<pass></pass>

- 定位VIP车辆查询：
<locate_mark></locate_mark>

- 读取ID查询：
<value></value>

提交最终答案时，必须说明工作模式（A、B、C 或 D）和初始VIP车辆的ID，格式如下：
<answer>mode=A, marked_value=5</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's simulate an "Intelligent Convoy Sequence Analysis" scenario. Here are the rules:

The system monitors a convoy of {n} autonomous vehicles forming an ordered sequence S[1..{n}], each with a distinct vehicle ID (an integer). A VIP target vehicle is initially located at the front, S[1]; its position changes as the convoy formation adjusts.

There is an unknown sensor working mode M, which is one of A, B, C, or D. It determines which end of the convoy the "Read ID" command returns. The modes are:
- A: Each Read ID returns the ID of the vehicle at the current front end.
- B: Each Read ID returns the ID of the vehicle at the current back end.
- C: Read ID alternates between front and back, starting with the front; each Read ID toggles the front/back reading state.
- D: Read ID alternates between front and back, starting with the back; each Read ID toggles the front/back reading state.

Note: Only the "Read ID" command triggers the front/back toggle in modes C/D; other formation operations or location queries do not change the toggle state.

You can repeatedly perform the following formation operations and queries (one per turn):

- RotateL(k): Cycle the front vehicle to the back k times, equivalent to a cyclic left rotation by k.
- RotateR(k): Cycle the back vehicle to the front k times, equivalent to a cyclic right rotation by k.
- Reverse(): The entire convoy reverses its driving direction.
- Pass(): Maintain formation, no operation.

All formation operations update the VIP vehicle's position accordingly.

- LocateMark: Returns Front, Back, or Middle, indicating whether the VIP vehicle is currently at the front end, back end, or a non-endpoint position. This query reveals no ID values and does not affect the C/D toggle state.
- Value: Returns an integer, which is the vehicle ID at the current front or back end, determined by the unknown mode M; if M is C or D, the internal front/back reading toggles after each call.

Through as few operations and queries as possible, ultimately provide both:
- The sensor working mode M (A, B, C, or D)
- The initial VIP vehicle's ID (i.e., the original S[1])

Success requires both to be correct; failure if either is wrong.

Each turn must contain only one tag. Use the following XML format:

- Rotate left (e.g., left rotate 2 times):
<rotate_left>2</rotate_left>

- Rotate right (e.g., right rotate 1 time):
<rotate_right>1</rotate_right>

- Reverse convoy:
<reverse></reverse>

- No operation:
<pass></pass>

- Locate VIP vehicle query:
<locate_mark></locate_mark>

- Read ID query:
<value></value>

When submitting the final answer, specify the working mode (A, B, C, or D) and the VIP vehicle's initial ID, using this format:
<answer>mode=A, marked_value=5</answer>
"""

    contextualized_rule_zh_2 = """\
我们来模拟一个"自动化医疗样本检测"场景，规则如下：

离心机试管架上放置了一个长度为 {n} 的样本序列 S[1..{n}]，每支试管包含一个互不相同的样本条码（整数）。有一份危重病人的加急样本，初始位于序列首端 S[1]；该样本的位置会随试管序列的操作而移动。

自动扫描机械臂存在一个未知的工作模式 M，它属于 A、B、C、D 四种之一，决定"读取条码"指令返回试管架哪一端的样本条码。四种模式如下：
- A: 每次读取均返回当前试管架首端的样本条码。
- B: 每次读取均返回当前试管架尾端的样本条码。
- C: 读取位置在首尾间交替，首次从首端开始；之后每次读取触发一次首尾切换。
- D: 读取位置在首尾间交替，首次从尾端开始；之后每次读取触发一次首尾切换。

注意：仅"读取条码"会触发 C/D 模式的首尾切换；其他移位操作或定位查询不改变切换状态。

你可以反复进行以下操作与查询（每次仅限一个操作或查询）：

- RotateL(k): 将首端试管依次移至尾部 k 次，等价于循环左移 k 次。
- RotateR(k): 将尾端试管依次移至首部 k 次，等价于循环右移 k 次。
- Reverse(): 将试管架整体水平调转180度（序列反转）。
- Pass(): 不进行任何操作。

所有序列操作都会相应更新加急样本的位置。

- LocateMark: 返回 Front（首端）、Back（尾端）或 Middle（中间位置），表示加急样本当前所处的位置。该查询不暴露任何条码数值且不影响 C/D 的切换状态。
- Value: 返回一个整数，为当前首端或尾端的样本条码，具体由未知模式 M 决定；若 M 为 C 或 D，则每次调用后内部首尾读取状态切换一次。

通过尽可能少的操作与查询，最终同时给出：
- 机械臂工作模式 M（A、B、C 或 D）
- 加急样本（即原始 S[1]）的初始条码数值

两者均正确则成功；任一错误则失败。

每次只能包含一个标签。请使用以下 XML 格式：

- 循环左移（例如左移 2 次）：
<rotate_left>2</rotate_left>

- 循环右移（例如右移 1 次）：
<rotate_right>1</rotate_right>

- 反转试管架：
<reverse></reverse>

- 不操作：
<pass></pass>

- 定位加急样本查询：
<locate_mark></locate_mark>

- 读取条码查询：
<value></value>

提交最终答案时，必须说明工作模式（A、B、C 或 D）和初始加急样本的条码，格式如下：
<answer>mode=A, marked_value=5</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's simulate an "Automated Medical Sample Testing" scenario. Here are the rules:

A centrifuge rack holds an ordered sequence S[1..{n}] of {n} sample tubes, each with a distinct barcode number (an integer). A critical patient's expedited sample is initially located at the front, S[1]; its position changes as operations are performed on the sequence.

The automated scanning robotic arm has an unknown working mode M, one of A, B, C, or D, which determines which end of the rack the "Read Barcode" command returns. The modes are:
- A: Each Read Barcode returns the barcode of the tube at the current front end.
- B: Each Read Barcode returns the barcode of the tube at the current back end.
- C: Read Barcode alternates between front and back, starting with the front; each read toggles the front/back state.
- D: Read Barcode alternates between front and back, starting with the back; each read toggles the front/back state.

Note: Only the "Read Barcode" command triggers the front/back toggle in modes C/D; other operations or location queries do not change the toggle state.

You can repeatedly perform the following operations and queries (one per turn):

- RotateL(k): Shift the front tube to the back k times, equivalent to a cyclic left rotation by k.
- RotateR(k): Shift the back tube to the front k times, equivalent to a cyclic right rotation by k.
- Reverse(): Flip the entire rack horizontally 180 degrees.
- Pass(): Do nothing.

All sequence operations update the expedited sample's position accordingly.

- LocateMark: Returns Front, Back, or Middle, indicating whether the expedited sample is currently at the front end, back end, or a non-endpoint position. This query reveals no barcode values and does not affect the C/D toggle state.
- Value: Returns an integer, which is the barcode at the current front or back end, determined by the unknown mode M; if M is C or D, the internal front/back reading toggles after each call.

Through as few operations and queries as possible, ultimately provide both:
- The scanning arm working mode M (A, B, C, or D)
- The initial expedited sample's barcode (i.e., the original S[1])

Success requires both to be correct; failure if either is wrong.

Each turn must contain only one tag. Use the following XML format:

- Rotate left (e.g., left rotate 2 times):
<rotate_left>2</rotate_left>

- Rotate right (e.g., right rotate 1 time):
<rotate_right>1</rotate_right>

- Reverse rack:
<reverse></reverse>

- No operation:
<pass></pass>

- Locate expedited sample query:
<locate_mark></locate_mark>

- Read barcode query:
<value></value>

When submitting the final answer, specify the working mode (A, B, C, or D) and the expedited sample's initial barcode, using this format:
<answer>mode=A, marked_value=5</answer>
"""

    contextualized_rule_zh_3 = """\
我们来模拟一个"智能阅卷系统分析"场景，规则如下：

送卷器中放置了一叠厚度为 {n} 的考卷序列 S[1..{n}]，每份考卷有一个互不相同的学生学号（整数）。有一份被特别标记的班长考卷，初始位于试卷叠顶部（即首端 S[1]）；该考卷的位置会随试卷叠的操作而移动。

自动阅卷机存在一个未知的抽卷读取模式 M，它属于 A、B、C、D 四种之一，决定"读取学号"指令返回试卷叠哪一端的学号。四种模式如下：
- A: 每次读取均返回当前试卷叠顶部（首端）的学号。
- B: 每次读取均返回当前试卷叠底部（尾端）的学号。
- C: 读取位置在顶部和底部间交替，首次从顶部开始；之后每次读取触发一次切换。
- D: 读取位置在顶部和底部间交替，首次从底部开始；之后每次读取触发一次切换。

注意：仅"读取学号"会触发 C/D 模式的读取切换；其他翻页操作或定位查询不改变切换状态。

你可以反复进行以下操作与查询（每次仅限一个操作或查询）：

- RotateL(k): 将顶部考卷依次移至底部 k 次。
- RotateR(k): 将底部考卷依次抽至顶部 k 次。
- Reverse(): 将整叠试卷上下翻转。
- Pass(): 不进行任何操作。

所有操作都会相应更新班长考卷的位置。

- LocateMark: 返回 Front（顶部/首端）、Back（底部/尾端）或 Middle（中间位置），表示班长考卷当前所处的位置。该查询不暴露任何学号数值且不影响 C/D 的切换状态。
- Value: 返回一个整数，为当前顶部或底部的学号，具体由未知模式 M 决定；若 M 为 C 或 D，则每次调用后内部上下读取状态切换一次。

通过尽可能少的操作与查询，最终同时给出：
- 阅卷机读取模式 M（A、B、C 或 D）
- 班长考卷（即原始 S[1]）的初始学号数值

两者均正确则成功；任一错误则失败。

每次只能包含一个标签。请使用以下 XML 格式：

- 循环左移（例如移至底部 2 次）：
<rotate_left>2</rotate_left>

- 循环右移（例如抽至顶部 1 次）：
<rotate_right>1</rotate_right>

- 翻转试卷：
<reverse></reverse>

- 不操作：
<pass></pass>

- 定位班长考卷查询：
<locate_mark></locate_mark>

- 读取学号查询：
<value></value>

提交最终答案时，必须说明工作模式（A、B、C 或 D）和初始班长的学号，格式如下：
<answer>mode=A, marked_value=5</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's simulate an "Intelligent Grading System Analysis" scenario. Here are the rules:

A paper feeder holds a stack of {n} exam papers forming a sequence S[1..{n}], each with a distinct student ID (an integer). A specially marked class president's paper is initially at the top of the stack (the front, S[1]); its position changes as operations are performed on the stack.

The automated grading machine has an unknown drawing mode M, one of A, B, C, or D, which determines from which end of the stack the "Read Student ID" command returns a value. The modes are:
- A: Each read returns the student ID of the paper at the current top (front).
- B: Each read returns the student ID of the paper at the current bottom (back).
- C: Reading alternates between top and bottom, starting with the top; each read toggles the state.
- D: Reading alternates between top and bottom, starting with the bottom; each read toggles the state.

Note: Only the "Read Student ID" command triggers the toggle in modes C/D; other stack operations or location queries do not change the toggle state.

You can repeatedly perform the following operations and queries (one per turn):

- RotateL(k): Move the top paper to the bottom k times.
- RotateR(k): Move the bottom paper to the top k times.
- Reverse(): Flip the entire stack upside down.
- Pass(): Leave the stack as is.

All operations update the class president's paper's position accordingly.

- LocateMark: Returns Front (top), Back (bottom), or Middle, indicating whether the class president's paper is currently at the top, bottom, or a non-endpoint position. This query reveals no ID values and does not affect the C/D toggle state.
- Value: Returns an integer, which is the student ID at the current top or bottom, determined by the unknown mode M; if M is C or D, the internal top/bottom reading toggles after each call.

Through as few operations and queries as possible, ultimately provide both:
- The drawing mode M (A, B, C, or D)
- The initial class president's student ID (i.e., the original S[1])

Success requires both to be correct; failure if either is wrong.

Each turn must contain only one tag. Use the following XML format:

- Rotate left (e.g., move to bottom 2 times):
<rotate_left>2</rotate_left>

- Rotate right (e.g., move to top 1 time):
<rotate_right>1</rotate_right>

- Reverse stack:
<reverse></reverse>

- No operation:
<pass></pass>

- Locate class president's paper query:
<locate_mark></locate_mark>

- Read student ID query:
<value></value>

When submitting the final answer, specify the working mode (A, B, C, or D) and the class president's initial student ID, using this format:
<answer>mode=A, marked_value=5</answer>
"""

    contextualized_rule_zh_4 = """\
我们来模拟一个"工业流水线质检"场景，规则如下：

质检传送带上依次排列着 {n} 个工业零部件，形成序列 S[1..{n}]，每个零部件印有一个互不相同的批次流水号（整数）。有一个被标记为高风险的残次品，初始位于传送带入口端（即首端 S[1]）；该残次品的位置会随传送带的操作而移动。

视觉检测系统存在一个未知的工作模式 M，它属于 A、B、C、D 四种之一，决定"扫描流水号"指令返回传送带哪一端的号码。四种模式如下：
- A: 每次扫描均返回当前传送带入口端（首端）的流水号。
- B: 每次扫描均返回当前传送带出口端（尾端）的流水号。
- C: 扫描位置在入口和出口间交替，首次从入口端开始；之后每次扫描触发一次切换。
- D: 扫描位置在入口和出口间交替，首次从出口端开始；之后每次扫描触发一次切换。

注意：仅"扫描流水号"会触发 C/D 模式的读取切换；其他传送操作或定位查询不改变切换状态。

你可以反复进行以下操作与查询（每次仅限一个操作或查询）：

- RotateL(k): 将入口端零部件依次循环输送至出口端 k 次。
- RotateR(k): 将出口端零部件依次循环输送回入口端 k 次。
- Reverse(): 将传送带整体反向运转，序列反转。
- Pass(): 不进行任何操作。

所有操作都会相应更新残次品的位置。

- LocateMark: 返回 Front（入口/首端）、Back（出口/尾端）或 Middle（中间位置），表示残次品当前所处的位置。该查询不暴露任何流水号数值且不影响 C/D 的切换状态。
- Value: 返回一个整数，为当前入口或出口的流水号，具体由未知模式 M 决定；若 M 为 C 或 D，则每次调用后内部扫描状态切换一次。

通过尽可能少的操作与查询，最终同时给出：
- 视觉检测模式 M（A、B、C 或 D）
- 残次品（即原始 S[1]）的初始批次流水号

两者均正确则成功；任一错误则失败。

每次只能包含一个标签。请使用以下 XML 格式：

- 循环左移（例如输送至出口 2 次）：
<rotate_left>2</rotate_left>

- 循环右移（例如输送回入口 1 次）：
<rotate_right>1</rotate_right>

- 反转传送带：
<reverse></reverse>

- 不操作：
<pass></pass>

- 定位残次品查询：
<locate_mark></locate_mark>

- 扫描流水号查询：
<value></value>

提交最终答案时，必须说明工作模式（A、B、C 或 D）和初始残次品的流水号，格式如下：
<answer>mode=A, marked_value=5</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's simulate an "Industrial Assembly Line Quality Control" scenario. Here are the rules:

A quality control conveyor belt carries {n} industrial components forming a sequence S[1..{n}], each stamped with a distinct batch serial number (an integer). A flagged defective component is initially located at the entry end (the front, S[1]); its position changes as the belt is operated.

The vision inspection system has an unknown working mode M, one of A, B, C, or D, which determines from which end of the belt the "Scan Serial Number" command returns a value. The modes are:
- A: Each scan returns the serial number of the component at the current entry end (front).
- B: Each scan returns the serial number of the component at the current exit end (back).
- C: Scanning alternates between entry and exit, starting with the entry; each scan toggles the state.
- D: Scanning alternates between entry and exit, starting with the exit; each scan toggles the state.

Note: Only the "Scan Serial Number" command triggers the toggle in modes C/D; other belt operations or location queries do not change the toggle state.

You can repeatedly perform the following operations and queries (one per turn):

- RotateL(k): Cycle the entry component to the exit k times.
- RotateR(k): Cycle the exit component back to the entry k times.
- Reverse(): Reverse the conveyor belt direction entirely.
- Pass(): No belt movement.

All operations update the defective component's position accordingly.

- LocateMark: Returns Front (entry), Back (exit), or Middle, indicating whether the defective component is currently at the entry, exit, or a non-endpoint position. This query reveals no serial numbers and does not affect the C/D toggle state.
- Value: Returns an integer, which is the serial number at the current entry or exit, determined by the unknown mode M; if M is C or D, the internal scanning reading toggles after each call.

Through as few operations and queries as possible, ultimately provide both:
- The vision inspection mode M (A, B, C, or D)
- The initial defective component's serial number (i.e., the original S[1])

Success requires both to be correct; failure if either is wrong.

Each turn must contain only one tag. Use the following XML format:

- Rotate left (e.g., cycle to exit 2 times):
<rotate_left>2</rotate_left>

- Rotate right (e.g., cycle to entry 1 time):
<rotate_right>1</rotate_right>

- Reverse belt:
<reverse></reverse>

- No operation:
<pass></pass>

- Locate defective component query:
<locate_mark></locate_mark>

- Scan serial number query:
<value></value>

When submitting the final answer, specify the working mode (A, B, C, or D) and the defective component's initial serial number, using this format:
<answer>mode=A, marked_value=5</answer>
"""

    contextualized_rule_zh_5 = """\
我们来模拟一个"电子取证卷宗审查"场景，规则如下：

取证系统内存有一份包含 {n} 份证据文件的电子卷宗，形成序列 S[1..{n}]，每份文件拥有一个互不相同的案件编号（整数）。有一份极其关键的定罪证据，初始位于卷宗首部 S[1]；该文件的位置会随卷宗序列的重排而改变。

自动审查机器人存在一个未知的调阅模式 M，它属于 A、B、C、D 四种之一，决定"提取案号"指令返回卷宗哪一端的编号。四种模式如下：
- A: 每次提取均返回当前卷宗首部的案件编号。
- B: 每次提取均返回当前卷宗尾部的案件编号。
- C: 提取位置在首尾间交替，首次从首部开始；之后每次提取触发一次切换。
- D: 提取位置在首尾间交替，首次从尾部开始；之后每次提取触发一次切换。

注意：仅"提取案号"会触发 C/D 模式的调阅切换；其他重排操作或定位查询不改变切换状态。

你可以反复进行以下操作与查询（每次仅限一个操作或查询）：

- RotateL(k): 将首部文件依次移至尾部 k 次。
- RotateR(k): 将尾部文件依次调至首部 k 次。
- Reverse(): 将整份卷宗的顺序逆转。
- Pass(): 不进行任何操作。

所有操作都会相应更新定罪证据的位置。

- LocateMark: 返回 Front（首部）、Back（尾部）或 Middle（中间位置），表示定罪证据当前所处的位置。该查询不暴露任何案号数值且不影响 C/D 的切换状态。
- Value: 返回一个整数，为当前首部或尾部的案件编号，具体由未知模式 M 决定；若 M 为 C 或 D，则每次调用后内部提取状态切换一次。

通过尽可能少的操作与查询，最终同时给出：
- 调阅模式 M（A、B、C 或 D）
- 定罪证据（即原始 S[1]）的初始案件编号

两者均正确则成功；任一错误则失败。

每次只能包含一个标签。请使用以下 XML 格式：

- 循环左移（例如移至尾部 2 次）：
<rotate_left>2</rotate_left>

- 循环右移（例如调至首部 1 次）：
<rotate_right>1</rotate_right>

- 逆转卷宗：
<reverse></reverse>

- 不操作：
<pass></pass>

- 定位定罪证据查询：
<locate_mark></locate_mark>

- 提取案号查询：
<value></value>

提交最终答案时，必须说明工作模式（A、B、C 或 D）和初始定罪证据的案号，格式如下：
<answer>mode=A, marked_value=5</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's simulate an "E-Discovery Dossier Review" scenario. Here are the rules:

The forensics system holds an electronic dossier containing {n} evidence files forming a sequence S[1..{n}], each with a distinct case ID (an integer). A crucial piece of convicting evidence is initially located at the front of the dossier, S[1]; its position changes as the dossier is rearranged.

The automated review bot has an unknown retrieval mode M, one of A, B, C, or D, which determines from which end of the dossier the "Extract Case ID" command returns a value. The modes are:
- A: Each extraction returns the case ID of the file at the current front.
- B: Each extraction returns the case ID of the file at the current back.
- C: Extraction alternates between front and back, starting with the front; each extraction toggles the state.
- D: Extraction alternates between front and back, starting with the back; each extraction toggles the state.

Note: Only the "Extract Case ID" command triggers the toggle in modes C/D; other rearrangement operations or location queries do not change the toggle state.

You can repeatedly perform the following operations and queries (one per turn):

- RotateL(k): Shift the front file to the back k times.
- RotateR(k): Shift the back file to the front k times.
- Reverse(): Reverse the entire order of the dossier.
- Pass(): No action.

All operations update the convicting evidence's position accordingly.

- LocateMark: Returns Front, Back, or Middle, indicating whether the convicting evidence is currently at the front, back, or a non-endpoint position. This query reveals no case ID values and does not affect the C/D toggle state.
- Value: Returns an integer, which is the case ID at the current front or back, determined by the unknown mode M; if M is C or D, the internal extraction reading toggles after each call.

Through as few operations and queries as possible, ultimately provide both:
- The retrieval mode M (A, B, C, or D)
- The initial convicting evidence's case ID (i.e., the original S[1])

Success requires both to be correct; failure if either is wrong.

Each turn must contain only one tag. Use the following XML format:

- Rotate left (e.g., shift to back 2 times):
<rotate_left>2</rotate_left>

- Rotate right (e.g., shift to front 1 time):
<rotate_right>1</rotate_right>

- Reverse dossier:
<reverse></reverse>

- No operation:
<pass></pass>

- Locate convicting evidence query:
<locate_mark></locate_mark>

- Extract case ID query:
<value></value>

When submitting the final answer, specify the working mode (A, B, C, or D) and the convicting evidence's initial case ID, using this format:
<answer>mode=A, marked_value=5</answer>
"""

    game_rule_zh = """\
我们来玩一个"序列抽象推理"游戏，规则如下：

游戏设定了一个长度为 {n} 的有序序列 S[1..{n}]，元素为两两不同的整数。有一个标记元素，初始位于 S[1]；标记随元素在序列中的位置变化而移动。

存在一个未知工作模式 M，它属于 A、B、C、D 四种之一，决定"值查询"返回序列端点的哪一端的数。四种模式如下：
- A: 每次值查询返回当前序列首端的数。
- B: 每次值查询返回当前序列尾端的数。
- C: 值查询在首尾间交替，首次从首端开始；之后每次值查询触发一次首尾切换。
- D: 值查询在首尾间交替，首次从尾端开始；之后每次值查询触发一次首尾切换。

注意：仅"值查询"会触发 C/D 的首尾切换；其他操作或查询不改变切换状态。

你可以反复进行以下操作与查询（每次仅限一个操作或查询）：

- RotateL(k): 将首元素依次移动到尾部 k 次，等价于循环左移 k 次。
- RotateR(k): 将尾元素依次移动到首部 k 次，等价于循环右移 k 次。
- Reverse(): 将序列整体反转。
- Pass(): 不进行操作。

所有序列操作都会相应更新标记元素的位置。

- LocateMark: 返回 Front（首端）、Back（尾端）或 Middle（非端点位置），表示标记元素当前的位置。该查询不暴露任何数值且不影响 C/D 的切换状态。
- Value: 返回一个整数，为当前首端或尾端的元素值，具体由未知模式 M 决定；若 M 为 C 或 D，则每次调用后内部首尾读法切换一次。

通过尽可能少的操作与查询，最终同时给出：
- 工作模式 M（A、B、C 或 D）
- 初始标记元素（即原始 S[1]）的整数值

两者均正确则成功；任一错误则失败。

每次只能包含一个标签。请使用以下 XML 格式：

- 循环左移（例如左移 2 次）：
<rotate_left>2</rotate_left>

- 循环右移（例如右移 1 次）：
<rotate_right>1</rotate_right>

- 反转序列：
<reverse></reverse>

- 不操作：
<pass></pass>

- 位置查询：
<locate_mark></locate_mark>

- 值查询：
<value></value>

提交最终答案时，必须说明工作模式（A、B、C 或 D）和初始标记元素的整数值，格式如下：
<answer>mode=A, marked_value=5</answer>
"""

    game_rule_en = """\
Let's play a "Sequence Abstract Reasoning" game. Here are the rules:

There is an ordered sequence S[1..{n}] of length {n}, with all distinct integers. A marked element initially sits at S[1]; the mark moves as the element's position in the sequence changes.

There exists an unknown working mode M, one of A, B, C, or D, which determines which end of the sequence the "Value Query" returns. The four modes are:
- A: Each Value Query returns the element at the current front end.
- B: Each Value Query returns the element at the current back end.
- C: Value Query alternates between front and back, starting with front; each Value Query toggles the front/back reading.
- D: Value Query alternates between front and back, starting with back; each Value Query toggles the front/back reading.

Note: Only "Value Query" triggers the front/back toggle in C/D; other operations or queries do not change the toggle state.

You can repeatedly perform the following operations and queries (one per turn):

- RotateL(k): Move the front element to the back k times, equivalent to a cyclic left rotation by k.
- RotateR(k): Move the back element to the front k times, equivalent to a cyclic right rotation by k.
- Reverse(): Reverse the entire sequence.
- Pass(): No operation.

All sequence operations update the marked element's position accordingly.

- LocateMark: Returns Front, Back, or Middle, indicating whether the marked element is at the front end, back end, or a non-endpoint position. This query reveals no numerical value and does not affect the C/D toggle state.
- Value: Returns an integer, which is the element value at the current front or back end, determined by the unknown mode M; if M is C or D, the internal front/back reading toggles after each call.

Through as few operations and queries as possible, ultimately provide both:
- The working mode M (A, B, C, or D)
- The integer value of the initial marked element (i.e., the original S[1])

Success requires both to be correct; failure if either is wrong.

Each turn must contain only one tag. Use the following XML format:

- Rotate left (e.g., left rotate 2 times):
<rotate_left>2</rotate_left>

- Rotate right (e.g., right rotate 1 time):
<rotate_right>1</rotate_right>

- Reverse sequence:
<reverse></reverse>

- No operation:
<pass></pass>

- Locate mark query:
<locate_mark></locate_mark>

- Value query:
<value></value>

When submitting the final answer, specify the working mode (A, B, C, or D) and the integer value of the initial marked element, using this format:
<answer>mode=A, marked_value=5</answer>
"""

    tags = ["answer", "rotate_left", "rotate_right", "reverse", "pass", "locate_mark", "value"]
    
    reasoning_type = "溯因推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"n": 4, "sequence": [10, 20, 30, 40], "mode": "A"},
            2: {"n": 5, "sequence": [5, 15, 25, 35, 45], "mode": "B"},
            3: {"n": 6, "sequence": [2, 4, 6, 8, 10, 12], "mode": "C"},
            4: {"n": 7, "sequence": [7, 14, 21, 28, 35, 42, 49], "mode": "D"},
            5: {"n": 8, "sequence": [3, 6, 9, 12, 15, 18, 21, 24], "mode": "C"},
        },
        "en": {
            1: {"n": 4, "sequence": [10, 20, 30, 40], "mode": "A"},
            2: {"n": 5, "sequence": [5, 15, 25, 35, 45], "mode": "B"},
            3: {"n": 6, "sequence": [2, 4, 6, 8, 10, 12], "mode": "C"},
            4: {"n": 7, "sequence": [7, 14, 21, 28, 35, 42, 49], "mode": "D"},
            5: {"n": 8, "sequence": [3, 6, 9, 12, 15, 18, 21, 24], "mode": "C"},
        },
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
        n = cfg["n"]
        self._game_info["n"] = n

        self.sequence = list(cfg["sequence"])
        self.mode = cfg["mode"]

        self.initial_marked_value = self.sequence[0]

        self.marked_index = 0

        if self.mode == "C":
            self.toggle_state = True
        elif self.mode == "D":
            self.toggle_state = False
        else:
            self.toggle_state = None

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "mode" not in ans_dict or "marked_value" not in ans_dict:
            return False
        
        if ans_dict["mode"] != self.mode:
            return False
        
        try:
            model_value = int(ans_dict["marked_value"])
        except:
            return False
            
        return model_value == self.initial_marked_value

    def _cf_core_produce(self, parsed_info):

        action_tags = [t for t in ["rotate_left", "rotate_right", "reverse", "pass", "locate_mark", "value"] if t in parsed_info]
        if len(action_tags) > 1:
            if self.config.language == "en":
                return f"Error: Multiple tags detected ({', '.join(action_tags)}). Please use only one tag per turn."
            else:
                return f"错误：检测到多个标签（{', '.join(action_tags)}）。每次只能使用一个标签。"
        
        if "rotate_left" in parsed_info:
            try:
                k = int(parsed_info["rotate_left"].strip())
                if k < 0:
                    return "Error: k must be non-negative." if self.config.language == "en" else "错误：k 必须为非负整数。"
                k = k % len(self.sequence)
                for _ in range(k):
                    elem = self.sequence.pop(0)
                    self.sequence.append(elem)
                    if self.marked_index == 0:
                        self.marked_index = len(self.sequence) - 1
                    else:
                        self.marked_index -= 1
                return "OK" if self.config.language == "en" else "完成"
            except ValueError:
                return "Error: Invalid format." if self.config.language == "en" else "错误：格式无效。"
        
        elif "rotate_right" in parsed_info:
            try:
                k = int(parsed_info["rotate_right"].strip())
                if k < 0:
                    return "Error: k must be non-negative." if self.config.language == "en" else "错误：k 必须为非负整数。"
                k = k % len(self.sequence)
                for _ in range(k):
                    elem = self.sequence.pop()
                    self.sequence.insert(0, elem)
                    self.marked_index = (self.marked_index + 1) % len(self.sequence)
                return "OK" if self.config.language == "en" else "完成"
            except ValueError:
                return "Error: Invalid format." if self.config.language == "en" else "错误：格式无效。"
        
        elif "reverse" in parsed_info:
            self.sequence.reverse()
            self.marked_index = len(self.sequence) - 1 - self.marked_index
            return "OK" if self.config.language == "en" else "完成"
        
        elif "pass" in parsed_info:
            return "OK" if self.config.language == "en" else "完成"
        
        elif "locate_mark" in parsed_info:
            if self.marked_index == 0:
                return "Front"
            elif self.marked_index == len(self.sequence) - 1:
                return "Back"
            else:
                return "Middle"
        
        elif "value" in parsed_info:
            if self.mode == "A":
                result = self.sequence[0]
            elif self.mode == "B":
                result = self.sequence[-1]
            elif self.mode == "C":
                if self.toggle_state:
                    result = self.sequence[0]
                else:
                    result = self.sequence[-1]
                self.toggle_state = not self.toggle_state
            elif self.mode == "D":
                if self.toggle_state:
                    result = self.sequence[0]
                else:
                    result = self.sequence[-1]
                self.toggle_state = not self.toggle_state
            
            return str(result)
        
        else:
            raise ValueError("No valid operation or query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.lstrip('-').isdigit():
            return str(int(correct) + 1)
        if self.config.language == "zh":
            if "是" in correct: return correct.replace("是", "否")
            elif "否" in correct: return correct.replace("否", "是")
        elif self.config.language == "en":
            lower_c = correct.lower()
            if "yes" in lower_c: return correct.replace("Yes", "No").replace("yes", "no").replace("YES", "NO")
            elif "no" in lower_c: return correct.replace("No", "Yes").replace("no", "yes").replace("NO", "YES")
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        saved_sequence = list(self.sequence)
        saved_marked_index = self.marked_index
        saved_toggle_state = self.toggle_state

        possible_queries = []

        lm_query = "<locate_mark></locate_mark>"
        if self.marked_index == 0:
            lm_ans = "Front"
        elif self.marked_index == len(self.sequence) - 1:
            lm_ans = "Back"
        else:
            lm_ans = "Middle"
        possible_queries.append({"query": lm_query, "answer": lm_ans})

        val_query = "<value></value>"
        if self.mode == "A":
            result = self.sequence[0]
        elif self.mode == "B":
            result = self.sequence[-1]
        elif self.mode in ["C", "D"]:
            if self.toggle_state:
                result = self.sequence[0]
            else:
                result = self.sequence[-1]
            self.toggle_state = not self.toggle_state
        possible_queries.append({"query": val_query, "answer": str(result)})

        if self.mode == "A":
            result2 = self.sequence[0]
        elif self.mode == "B":
            result2 = self.sequence[-1]
        elif self.mode in ["C", "D"]:
            if self.toggle_state:
                result2 = self.sequence[0]
            else:
                result2 = self.sequence[-1]
            self.toggle_state = not self.toggle_state
        possible_queries.append({"query": val_query, "answer": str(result2)})

        rl_query = "<rotate_left>1</rotate_left>"
        elem = self.sequence.pop(0)
        self.sequence.append(elem)
        if self.marked_index == 0:
            self.marked_index = len(self.sequence) - 1
        else:
            self.marked_index -= 1
        possible_queries.append({"query": rl_query, "answer": "OK"})

        if self.mode == "A":
            result3 = self.sequence[0]
        elif self.mode == "B":
            result3 = self.sequence[-1]
        elif self.mode in ["C", "D"]:
            if self.toggle_state:
                result3 = self.sequence[0]
            else:
                result3 = self.sequence[-1]
            self.toggle_state = not self.toggle_state
        possible_queries.append({"query": val_query, "answer": str(result3)})

        if self.marked_index == 0:
            lm_ans2 = "Front"
        elif self.marked_index == len(self.sequence) - 1:
            lm_ans2 = "Back"
        else:
            lm_ans2 = "Middle"
        possible_queries.append({"query": lm_query, "answer": lm_ans2})

        self.sequence = saved_sequence
        self.marked_index = saved_marked_index
        self.toggle_state = saved_toggle_state

        return possible_queries

