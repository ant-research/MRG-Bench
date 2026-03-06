from .base import Game
import heapq

class GridAnomalyGame(Game):

    game_rule_zh = """\
    我们现在来玩一个“网络诊断”游戏。规则如下：

    这是一个 {rows} 行 {cols} 列的网格网络（坐标从 0-0 到 {max_r}-{max_c}）。我暗中在这个网络里设置了一种“异常”，它是以下三种情况之一：
    1. **横向断墙 (row_cut)**：在第 k 行和第 k+1 行之间，切断了所有的竖直连线。
    2. **纵向断墙 (col_cut)**：在第 k 列和第 k+1 列之间，切断了所有的水平连线。
    3. **加权路况 (weighted)**：网络全连通，但水平方向移动的代价是 wh，竖直方向移动的代价是 wv（wh 和 wv 可以在 1 到 9 之间，且可能不等）。

    除此之外，没有其他障碍。对于断墙的情况，未切断的边代价默认为 1。

    你的目标是推断出具体的异常类型及其参数（例如：哪一行被切，或者具体的权重是多少）。

    你可以向我发起查询，我会如实回答。当你收集到足够信息后，请提交你的最终判断。

    ## 询问格式

    你可以查询两点是否连通，或者两点间的最短路径长度。请严格使用以下 XML 格式，`<query>` 内容为键值对，用逗号分隔。坐标请务必使用 `行-列` 的格式（例如 `0-0`）：

    - 询问连通性 (q=connect)：
    ```xml
    <query>q=connect,p1=0-0,p2=1-2</query>
    ```

    - 询问最短距离 (q=dist)：
    ```xml
    <query>q=dist,p1=0-0,p2=1-2</query>
    ```

    ## 提交答案格式

    当你确信已找到规则时，请使用 `<answer>` 标签提交。内容必须包含异常类型 `type` 和对应的参数（`idx` 或 `wh,wv`）：

    - 如果认为是断墙 (row_cut 或 col_cut)，需指定 idx (切缝起点的行号或列号)：
    ```xml
    <answer>type=row_cut,idx=1</answer>
    ```
    (表示第1行和第2行之间断开)

    - 如果认为是加权 (weighted)，需指定 wh (水平权重) 和 wv (竖直权重)：
    ```xml
    <answer>type=weighted,wh=2,wv=5</answer>
    ```
    """

    game_rule_en = """\
    Let\'s play a "Network Diagnosis" game. Here are the rules:

    We have a grid network with {rows} rows and {cols} columns (coordinates from 0-0 to {max_r}-{max_c}). I have secretly set up an "anomaly" in this network, which is one of the following three types:
    1. **Row Cut (row_cut)**: All vertical edges between row k and row k+1 are removed.
    2. **Column Cut (col_cut)**: All horizontal edges between column k and column k+1 are removed.
    3. **Weighted (weighted)**: The network is fully connected, but the cost of moving horizontally is wh, and the cost of moving vertically is wv (wh and wv are between 1 and 9, and may differ).

    Apart from this, there are no other obstacles. For the cut scenarios, existing edges have a default cost of 1.

    Your goal is to infer the specific anomaly type and its parameters (e.g., which row is cut, or what the specific weights are).

    You can send me queries, and I will answer truthfully. When you have collected enough information, submit your final judgment.

    ## Query Format

    You can ask about connectivity or the shortest path length between two points. Strictly use the following XML format with comma-separated key-value pairs. Coordinates must be in `row-col` format (e.g., `0-0`):

    - Query Connectivity (q=connect):
    ```xml
    <query>q=connect,p1=0-0,p2=1-2</query>
    ```

    - Query Shortest Distance (q=dist):
    ```xml
    <query>q=dist,p1=0-0,p2=1-2</query>
    ```

    ## Answer Format

    When you are confident, submit your inferred rule using the `<answer>` tag. The content must include the anomaly `type` and its parameters (`idx` or `wh,wv`):

    - If it is a cut (row_cut or col_cut), specify idx (the starting index of the cut):
    ```xml
    <answer>type=row_cut,idx=1</answer>
    ```
    (Means the cut is between row 1 and row 2)

    - If it is weighted, specify wh (horizontal weight) and wv (vertical weight):
    ```xml
    <answer>type=weighted,wh=2,wv=5</answer>
    ```
    """

    tags = ["answer", "query"]

    # Difficulty Config:
    # 1 (easy)   - Small grid, simple cut
    # 2 (medium) - Medium grid, weighted or cut
    # 3 (hard)   - Larger grid, weighted or cut

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "rows": 3, "cols": 3,
                "answer": {"type": "row_cut", "idx": "1"}
            },
            2: {
                "rows": 4, "cols": 4,
                "answer": {"type": "weighted", "wh": "2", "wv": "1"}
            },
            3: {
                "rows": 5, "cols": 5,
                "answer": {"type": "col_cut", "idx": "2"}
            },
        },
        "en": {
            1: {
                "rows": 3, "cols": 3,
                "answer": {"type": "row_cut", "idx": "1"}
            },
            2: {
                "rows": 4, "cols": 4,
                "answer": {"type": "weighted", "wh": "2", "wv": "1"}
            },
            3: {
                "rows": 5, "cols": 5,
                "answer": {"type": "col_cut", "idx": "2"}
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)
        self._initialize_game()

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["rows"] = cfg["rows"]
        self._game_info["cols"] = cfg["cols"]
        self._game_info["max_r"] = cfg["rows"] - 1
        self._game_info["max_c"] = cfg["cols"] - 1
        self._game_info["answer"] = cfg["answer"]

    def evaluate(self, parsed_info):
        # Parse user answer string "key=val,key2=val2" into a dict
        user_ans_str = parsed_info["answer"]
        try:
            user_ans_dict = {}
            for item in user_ans_str.split(","):
                k, v = item.split("=")
                user_ans_dict[k.strip()] = v.strip()
            
            # Compare with true answer
            true_ans = self._game_info["answer"]
            
            # Check type
            if user_ans_dict.get("type") != true_ans["type"]:
                return False
            
            # Check params based on type
            rtype = true_ans["type"]
            if rtype in ["row_cut", "col_cut"]:
                return user_ans_dict.get("idx") == true_ans["idx"]
            elif rtype == "weighted":
                return (user_ans_dict.get("wh") == true_ans["wh"] and 
                        user_ans_dict.get("wv") == true_ans["wv"])
            return False
            
        except Exception:
            return False

    def produce_response(self, parsed_info):
        try:
            query_items = [item.strip() for item in parsed_info["query"].split(",")]
            query_dict = {}
            for item in query_items:
                k, v = item.split("=")
                query_dict[k.strip()] = v.strip()
            
            q_type = query_dict.get("q")
            p1_str = query_dict.get("p1")
            p2_str = query_dict.get("p2")

            if not (q_type and p1_str and p2_str):
                raise ValueError("Missing params")

            # Parse coordinates "r-c"
            r1, c1 = map(int, p1_str.split("-"))
            r2, c2 = map(int, p2_str.split("-"))
            
            # Validate bounds
            rows, cols = self._game_info["rows"], self._game_info["cols"]
            if not (0 <= r1 < rows and 0 <= c1 < cols and 0 <= r2 < rows and 0 <= c2 < cols):
                return "Error: Coordinates out of bounds."

            dist = self._bfs_dijkstra((r1, c1), (r2, c2))
            
            if q_type == "connect":
                if self.config.language == "zh":
                    return "是" if dist != -1 else "不是"
                else:
                    return "Yes" if dist != -1 else "No"
            elif q_type == "dist":
                if dist == -1:
                    return "不连通" if self.config.language == "zh" else "Not connected"
                return str(dist)
            else:
                return "Unknown query type."

        except Exception as e:
            return f"Invalid query format: {str(e)}"

    def _bfs_dijkstra(self, start, end):
        # Returns shortest distance or -1 if not connected
        rows, cols = self._game_info["rows"], self._game_info["cols"]
        rule = self._game_info["answer"]
        
        # Standard weights
        w_h, w_v = 1, 1
        
        # Cut config
        cut_r_idx = -1
        cut_c_idx = -1
        
        if rule["type"] == "weighted":
            w_h = int(rule["wh"])
            w_v = int(rule["wv"])
        elif rule["type"] == "row_cut":
            cut_r_idx = int(rule["idx"])
        elif rule["type"] == "col_cut":
            cut_c_idx = int(rule["idx"])

        # Dijkstra
        # heap: (cost, r, c)
        pq = [(0, start[0], start[1])]
        dists = {}
        dists[start] = 0
        
        while pq:
            d, r, c = heapq.heappop(pq)
            
            if d > dists.get((r, c), float('inf')):
                continue
            
            if (r, c) == end:
                return d
            
            # Neighbors: (dr, dc, move_cost, is_vertical)
            # Vertical: (1,0) (-1,0); Horizontal: (0,1) (0,-1)
            moves = [
                (1, 0, w_v, True), (-1, 0, w_v, True), 
                (0, 1, w_h, False), (0, -1, w_h, False)
            ]
            
            for dr, dc, weight, is_vert in moves:
                nr, nc = r + dr, c + dc
                
                # Bounds check
                if 0 <= nr < rows and 0 <= nc < cols:
                    # Check cuts
                    allowed = True
                    if rule["type"] == "row_cut" and is_vert:
                        # Moving vertically between k and k+1
                        # If moving from k down to k+1, or k+1 up to k
                        min_r = min(r, nr)
                        if min_r == cut_r_idx:
                            allowed = False
                    
                    if rule["type"] == "col_cut" and not is_vert:
                        # Moving horizontally between k and k+1
                        min_c = min(c, nc)
                        if min_c == cut_c_idx:
                            allowed = False
                    
                    if allowed:
                        new_cost = d + weight
                        if new_cost < dists.get((nr, nc), float('inf')):
                            dists[(nr, nc)] = new_cost
                            heapq.heappush(pq, (new_cost, nr, nc))
                            
        return -1
