import hydra
import json
import csv
import os
import sys
from datetime import datetime
from omegaconf import DictConfig, OmegaConf
from runner import GameRunner
from chat_assistant import init_client
from dataclasses import asdict

@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg):
    
    # 初始化客户端
    try:
        client = init_client(cfg.model)
    except Exception as e:
        print(f"[Error] Client initialization failed: {e}")
        sys.exit(1)

    # 初始化 Runner
    try:
        runner = GameRunner(cfg, client)
    except KeyError as e:
        print(f"[Error] Game initialization failed: {e}")
        sys.exit(1)

    # 记录开始时间
    start_time = datetime.now()
    
    # 运行游戏
    game_state = runner.run()
    
    # 记录结束时间
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    info = asdict(game_state)
    
    # 计算使用的轮数 (Assistant 的回复次数)
    assistant_moves = len([m for m in info['messages'] if m['role'] == 'assistant'])
    
    # 准备记录的数据字典
    result_data = {
        "timestamp": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "model": cfg.model,
        "game_name": cfg.game_name,
        "difficulty": cfg.get("difficulty", 1),
        "language": cfg.get("language", "zh"),
        "status": info['state'],
        "reason": info['state_reason'],
        "turns_used": assistant_moves,
        "max_turns": cfg.get("max_turns", 99999),
        "duration_seconds": round(duration, 2),
        "history_length": len(info['messages'])
    }

    # 打印简要结果到控制台
    print(f"[Result] Game: {cfg.game_name} | Diff: {cfg.get('difficulty')} | Status: {info['state']} | Turns: {assistant_moves}/{cfg.get('max_turns', 99)}")

    # 将结果写入 CSV 文件
    output_file = "evaluation_results.csv"
    file_exists = os.path.isfile(output_file)
    
    try:
        with open(output_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=result_data.keys())
            # 如果文件不存在，先写入表头
            if not file_exists:
                writer.writeheader()
            writer.writerow(result_data)
    except Exception as e:
        print(f"[Error] Failed to write results to CSV: {e}")

if __name__ == '__main__':
    main()
