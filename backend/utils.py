import os
import subprocess
import yaml

def get_model_sizes_from_config(models_path: str, model_id: str):
    path_to_yaml = os.path.join(models_path, model_id, "config.yaml")
    if not os.path.exists(path_to_yaml):
        raise FileNotFoundError(f"Config file not found for model {model_id} at {path_to_yaml}")

    with open(path_to_yaml, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    return config["sizes"]

def prints(info):
    print(f"[LAUNCHER]:    {info}")

def kill_ports(ports: list[int]) -> None:
    """Force-kill any process still bound to the given ports (e.g. after terminate())."""
    for port in ports:
        try:
            subprocess.run(
                ["fuser", "-k", f"{port}/tcp"],
                capture_output=True,
                timeout=2,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        except Exception:
            pass
        