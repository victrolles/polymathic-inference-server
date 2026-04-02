import os
import yaml
import subprocess

POD = "pvc-loader"
CONTAINER = "loader"
NAMESPACE = "default"
MODELS_PATH = "/mnt/home/vgoudal/polymathic-inference-server/models"
WAIT_TIMEOUT = "120s"

def run(cmd):
    print(">", " ".join(cmd))
    subprocess.run(cmd, check=True)

def kubectl_copy(local_path, remote_dir):
    run([
        "kubectl", "exec", "-n", NAMESPACE, "-c", CONTAINER, POD,
        "--", "mkdir", "-p", remote_dir
    ])

    run([
        "kubectl", "cp",
        local_path,
        f"{NAMESPACE}/{POD}:{remote_dir}",
        "-c", CONTAINER,
    ])

def main():
    run([
        "kubectl", "wait", "--for=condition=Ready", f"pod/{POD}",
        "-n", NAMESPACE, f"--timeout={WAIT_TIMEOUT}",
    ])
    for model in os.listdir(MODELS_PATH):
        config_path = os.path.join(MODELS_PATH, model, "config.yaml")

        # Load the config
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        # Copy the weights to the PVC
        for size in config["sizes"]:
            if size.get("enabled", True):
                local_path = size["path"]
                remote_dir = os.path.join("/data/weights", model, size["id"])
                kubectl_copy(local_path, remote_dir)

        # Copy the datasets to the PVC
        for dataset in config["datasets"]:
            local_path = dataset["path"]
            remote_dir = os.path.join("/data/datasets", model)
            kubectl_copy(local_path, remote_dir)

if __name__ == "__main__":
    main()