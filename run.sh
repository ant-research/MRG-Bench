#!/bin/bash

# 确保脚本抛出遇到的错误
set -e

# 设置 PYTHONPATH 以便 python 能找到模块
export PYTHONPATH=$PYTHONPATH:.

# 默认参数
MODEL_NAME="Ling-flash-2.0" # 这里填入你 chat_assistant.py 中实际支持的模型名称
LANGUAGE="zh" # zh 或 en
DIFFICULTY=1  # 1, 2, 3
MAX_TURNS=10

# 游戏列表
GAMES=(
    "HiddenAttrRuleGame"
    "HiddenMarkingRuleGame"
    "SetCountingGame"
    "TricolorStatsGame"
    "HiddenTreeGame"
    "HierarchicalCycleGame"
    "HiddenTreeRuleGame"
    "AbnormalTreeGame"
    "FindRootGame"
    "LcaGuessGame"
    "DistanceSearchGame"
    "GraphFaultGame"
    "GridAnomalyGame"
    "GraphMinesweeperGame"
    "PeriodicSequenceGame"
    "TransformationRuleGame"
    "SequenceRuleGame"
    "SequenceOrderGame"
    "PermutationDetectiveGame"
    "PrefixProbeGame"
    "SetOperationGame"
    "HiddenMappingGame"
    "GraphInfectionGame"
    "GraphConnectivityGame"
    "GraphReconstructionGame"
)

echo "==========================================="
echo "开始游戏评估"
echo "模型: $MODEL_NAME"
echo "语言: $LANGUAGE"
echo "难度: $DIFFICULTY"
echo "==========================================="

# 创建日志目录
mkdir -p logs

# 遍历运行每一个游戏
for GAME_NAME in "${GAMES[@]}"; do
    echo "正在运行游戏: $GAME_NAME ..."
    
    # 运行 python 脚本
    # 假设 Hydra 配置结构允许通过命令行覆盖参数
    # 如果你的 hydra config 结构不同，请相应调整下面的参数
    python main.py \
        game_name="$GAME_NAME" \
        model="$MODEL_NAME" \
        language="$LANGUAGE" \
        difficulty=$DIFFICULTY \
        max_turns=$MAX_TURNS \
        system_prompt.include_rules=False > "logs/${GAME_NAME}.log" 2>&1

    if [ $? -eq 0 ]; then
        echo "✅ $GAME_NAME 完成"
    else
        echo "❌ $GAME_NAME 失败，请查看 logs/${GAME_NAME}.log"
    fi
done

echo "所有评估已完成。"
