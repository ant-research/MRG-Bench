import hydra, json
from omegaconf import DictConfig, OmegaConf
from runner import GameRunner
from chat_assistant import init_client
from dataclasses import asdict


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg):
    
    client = init_client(cfg.model)

    runner = GameRunner(cfg, client)
    game_state = runner.run()

    info = asdict(game_state)
    print(info)
    # for key, val in cfg.items():
    #     if "Config" in key and cfg.game_name not in key:
    #         pass
    #     else:
    #         if isinstance(val, DictConfig):
    #             val = OmegaConf.to_container(val, resolve=True)
    #         info[key] = val

    # with open("output.jsonl", "a", encoding="utf-8") as f:
    #     f.write(json.dumps(info, ensure_ascii=False) + "\n")

    # print(f"{info['state']}\t{info['state_reason']}\t{info['game_name']}"
    #     f"\t{info['language']}\t{info['model']}\t{info['system_prompt']['include_rules']}"
    #     f"\t{info[info['game_name']+'Config']}\t{len(info['messages'])}")


if __name__ == '__main__':
    main()



