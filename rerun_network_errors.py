import csv
import subprocess
import sys
import os

def rerun_failed_cases(input_file="evaluation_results_3.out"):
    """
    从指定文件中读取评估结果，提取因 'LLM API returned no response' 失败的案例，
    并调用 main.py 重新运行这些案例。
    """
    if not os.path.exists(input_file):
        print(f"[Error] Input file '{input_file}' not found.")
        print("Please ensure you are running this script in the correct directory (e.g., game_benchmark_v2).")
        return

    failed_cases = []
    
    try:
        with open(input_file, mode='r', encoding='utf-8') as f:
            # 处理可能的 BOM 头
            line = f.readline()
            if line.startswith('\ufeff'):
                line = line[1:]
            
            # 检查分隔符，虽然扩展名是 .out，但内容看起来是逗号分隔的 CSV
            if ',' in line:
                f.seek(0)
                reader = csv.DictReader(f)
                for row in reader:
                    # 检查字段是否存在，防止文件格式错误
                    if 'status' not in row or 'reason' not in row:
                        continue
                    
                    if row['status'] == 'failed' and 'LLM API returned no response' in row['reason']:
                        failed_cases.append(row)
            else:
                print("[Error] File format not recognized (expected CSV).")
                return
                
    except Exception as e:
        print(f"[Error] Failed to read input file: {e}")
        return

    print(f"===========================================")
    print(f"Found {len(failed_cases)} cases with 'LLM API returned no response'.")
    print(f"===========================================")

    # 逐个重跑
    for i, case in enumerate(failed_cases):
        print(f"[{i+1}/{len(failed_cases)}] Rerunning: Model={case['model']} | Game={case['game_name']} | Diff={case['difficulty']} | Lang={case['language']}")
        
        # 构造 hydra 参数
        # 参考 run.sh 中的配置
        cmd = [
            "python", "main.py",
            f"game_name={case['game_name']}",
            f"model={case['model']}",
            f"language={case['language']}",
            f"difficulty={case['difficulty']}",
            "max_turns=999",
            "system_prompt.include_rules=False"
        ]
        
        try:
            # 执行命令
            # stdout=None, stderr=None 表示直接输出到控制台，可以看到进度
            result = subprocess.run(cmd, text=True)
            
            if result.returncode == 0:
                print(f"  ✅ Success")
            else:
                print(f"  ❌ Failed (Return code: {result.returncode})")
                
        except KeyboardInterrupt:
            print("\n[Info] Process interrupted by user.")
            sys.exit(0)
        except Exception as e:
            print(f"  ❌ Error executing command: {e}")

    print("===========================================")
    print("All retry tasks completed.")

if __name__ == "__main__":
    # 如果命令行提供了文件名，则使用提供的文件名，否则默认为 evaluation_results.out
    target_file = sys.argv[1] if len(sys.argv) > 1 else "evaluation_results_4.out"
    rerun_failed_cases(target_file)
