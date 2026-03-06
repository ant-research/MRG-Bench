from game import (
    HiddenAttrRuleGame,
    HiddenMarkingRuleGame,
    SetCountingGame,
    TricolorStatsGame,
    HiddenTreeGame,
    HierarchicalCycleGame,
    HiddenTreeRuleGame,
    AbnormalTreeGame,
    FindRootGame,
    LcaGuessGame,
    DistanceSearchGame,
    GraphFaultGame,
    GridAnomalyGame,
    GraphMinesweeperGame,
    PeriodicSequenceGame,
    TransformationRuleGame,
    SequenceRuleGame,
    SequenceOrderGame,
    PermutationDetectiveGame,
    PrefixProbeGame,
    SetOperationGame,
    HiddenMappingGame,
    GraphInfectionGame,
    GraphConnectivityGame,
    GraphReconstructionGame
)
from tqdm import tqdm

"""
如果失败的话，继续会怎么样呢？失败提交答案次数
如果把所有的回复拼接到一起再次询问，是否能成功呢
"""

class GameRunner:

    def __init__(self, cfg, llm_agent):
        self.llm_agent = llm_agent
        self.cfg = cfg
        self.game_classes = {
            "HiddenAttrRuleGame": HiddenAttrRuleGame,
            "HiddenMarkingRuleGame": HiddenMarkingRuleGame,
            "SetCountingGame": SetCountingGame,
            "TricolorStatsGame": TricolorStatsGame,
            "HiddenTreeGame": HiddenTreeGame,
            "HierarchicalCycleGame": HierarchicalCycleGame,
            "HiddenTreeRuleGame": HiddenTreeRuleGame,
            "AbnormalTreeGame": AbnormalTreeGame,
            "FindRootGame": FindRootGame,
            "LcaGuessGame": LcaGuessGame,
            "DistanceSearchGame": DistanceSearchGame,
            "GraphFaultGame": GraphFaultGame,
            "GridAnomalyGame": GridAnomalyGame,
            "GraphMinesweeperGame": GraphMinesweeperGame,
            "PeriodicSequenceGame": PeriodicSequenceGame,
            "TransformationRuleGame": TransformationRuleGame,
            "SequenceRuleGame": SequenceRuleGame,
            "SequenceOrderGame": SequenceOrderGame,
            "PermutationDetectiveGame": PermutationDetectiveGame,
            "PrefixProbeGame": PrefixProbeGame,
            "SetOperationGame": SetOperationGame,
            "HiddenMappingGame": HiddenMappingGame,
            "GraphInfectionGame": GraphInfectionGame,
            "GraphConnectivityGame": GraphConnectivityGame,
            "GraphReconstructionGame": GraphReconstructionGame,
        }
        self.game = self._create_game()

    def _create_game(self):
        game_name = self.cfg.game_name
        if game_name in self.game_classes:
            return self.game_classes[game_name](self.cfg)
        else:
            raise KeyError(f"不存在该游戏: {game_name}")

    def run(self):

        llm_response = ""
        game_state = self.game.state

        # 这里假设 cfg 中有 max_turns，如果没有则默认 10
        max_turns = self.cfg.get("max_turns", 99)

        for cur_turn in range(max_turns):
            try:
                # 获取llm回复
                llm_response_list = self.llm_agent.chat_messages(game_state.messages)
                if not llm_response_list:
                    game_state.set_state("failed", "LLM API returned no response")
                    break
                
                llm_response = llm_response_list[0]
                game_state.add_message("assistant", llm_response) # 添加回复到状态
                
                # 如果llm提交的是query，那么产生新的回复，否则判断答案是否正确
                self.game.step(llm_response) 

                if game_state.state != "in_progress":
                    break
            except Exception as e:
                game_state.set_state("failed", f"Runtime error: {str(e)}")
                break

        if game_state.state == "in_progress":
            game_state.set_state("over_max_turns", "Surpass max turns.")

        return game_state
