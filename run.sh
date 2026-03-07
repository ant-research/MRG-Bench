#!/bin/bash

# 确保脚本抛出遇到的错误
set -e

# 设置 PYTHONPATH 以便 python 能找到模块
export PYTHONPATH=$PYTHONPATH:.

# ================= 配置区域 ================
# 定义要评测的模型列表，可以包含多个模型
MODELS=("Ling-flash-2.0" "Ling-1T" "DeepSeek-V3.2" "Kimi-K2-Thinking")

# 定义要评测的语言列表
LANGUAGES=("zh" "en")

MAX_TURNS=999                # 单局最大轮数
REPEAT_TIMES=3              # 每个难度重复运行多少次
# ===========================================

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

# 难度列表
DIFFICULTIES=(1 2 3)

echo "==========================================="
echo "🚀 开始游戏全方位评估"
echo "模型列表: ${MODELS[*]}"
echo "语言列表: ${LANGUAGES[*]}"
echo "重复次数: $REPEAT_TIMES"
echo "结果保存至: evaluation_results.csv"
echo "==========================================="

# 创建日志目录
mkdir -p logs

# 1. 遍历模型
for MODEL in "${MODELS[@]}"; do
    echo "🤖 当前评估模型: $MODEL"

    # 2. 遍历语言
    for LANG in "${LANGUAGES[@]}"; do
        echo "🌐 当前评估语言: $LANG"

        # 3. 遍历每一个游戏
        for GAME_NAME in "${GAMES[@]}"; do
            echo "-------------------------------------------"
            echo "🎮 正在评测游戏: $GAME_NAME"
            
            # 4. 遍历难度
            for DIFF in "${DIFFICULTIES[@]}"; do
                
                # 5. 重复运行
                for ((i=1; i<=REPEAT_TIMES; i++)); do
                    # 构造日志文件名，包含模型、语言、游戏、难度、轮次
                    # 注意：如果模型名包含路径分隔符等特殊字符，建议先处理一下，这里假设模型名是安全的文件名字符
                    LOG_FILE="logs/${MODEL}_${LANG}_${GAME_NAME}_diff${DIFF}_run${i}.log"
                    
                    # 使用 main.py 运行游戏，参数通过 hydra 覆盖
                    python main.py \
                        game_name="$GAME_NAME" \
                        model="$MODEL" \
                        language="$LANG" \
                        difficulty=$DIFF \
                        max_turns=$MAX_TURNS \
                        system_prompt.include_rules=False >> "$LOG_FILE" 2>&1

                    if [ $? -eq 0 ]; then
                        echo "      [Model:$MODEL | Lang:$LANG | Diff:$DIFF | Run $i/$REPEAT_TIMES] ✅ 完成"
                    else
                        echo "      [Model:$MODEL | Lang:$LANG | Diff:$DIFF | Run $i/$REPEAT_TIMES] ❌ 失败 (查看 $LOG_FILE)"
                    fi
                done
            done
        done
    done
done

echo "==========================================="
echo "✅ 所有评估已完成。"
echo "请查看 'evaluation_results.csv' 获取详细数据。"
