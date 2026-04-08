import math
import os
import re
import subprocess
import yaml

MODELS_PATH = "models"
VALUES_YAML = "deploy/helm/inference-platform/values.yaml"
MULTIPLIER = 1.5

def convert_to_kubernetes_size(size_bytes: int) -> str:
    size_bytes *= MULTIPLIER
    if size_bytes <= 0:
        return "0"
    if size_bytes < 1024:
        return str(size_bytes)
    if size_bytes < 1024**2:
        return f"{math.ceil(size_bytes / 1024)}Ki"
    if size_bytes < 1024**3:
        return f"{math.ceil(size_bytes / 1024**2)}Mi"
    if size_bytes < 1024**4:
        return f"{math.ceil(size_bytes / 1024**3)}Gi"
    return f"{math.ceil(size_bytes / 1024**4)}Ti"

def format_output(stdout: str) -> int:
    return int(stdout.strip().split()[0])

def update_helm_values(datasets_size: str, weights_size: str) -> None:
    with open(VALUES_YAML, "r") as f:
        values = yaml.safe_load(f)
    values["storage"]["datasets"]["size"] = datasets_size
    values["storage"]["weights"]["size"] = weights_size
    with open(VALUES_YAML, "w") as f:
        yaml.dump(values, f)
    print(f"Updated values.yaml")


def main():
    weight_size_bytes = 0
    dataset_size_bytes = 0
    for model in os.listdir(MODELS_PATH):
        config_path = os.path.join(MODELS_PATH, model, "config.yaml")

        # Load the config
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        # Copy the weights to the PVC
        for size in config["sizes"]:
            if size.get("enabled", True):
                size_path = size.get("path")
                output = subprocess.run(["du", "-B1", "-s", size_path], capture_output=True, text=True)
                weight_size_bytes += format_output(output.stdout)

        for dataset in config["datasets"]:
            dataset_path = dataset.get("path")
            output = subprocess.run(["du", "-B1", "-s", dataset_path], capture_output=True, text=True)
            dataset_size_bytes += format_output(output.stdout)

    datasets_size = convert_to_kubernetes_size(dataset_size_bytes)
    weights_size = convert_to_kubernetes_size(weight_size_bytes)
    print(f"Datasets size: {datasets_size}")
    print(f"Weights size: {weights_size}")
    update_helm_values(datasets_size, weights_size)

if __name__ == "__main__":
    main()