import subprocess
import os

from dotenv import load_dotenv

from utils import get_model_sizes_from_config, prints, kill_ports

MODELS_PATH = "/mnt/home/vgoudal/polymathic-inference-server/models"
MEDIA_FILES_PATH = "/mnt/home/vgoudal/polymathic-inference-server/tmp/media_files"

GATEWAY_PORT = 8000
GATEWAY_HOST = "localhost"
GATEWAY_VENV_PATH = "/mnt/home/vgoudal/venvs/polymathic-inference-server/gateway"

MEDIA_SERVICE_BASE_PORT = 6000
MEDIA_SERVICE_HOST = "localhost"
MEDIA_SERVICE_VENV_PATH = "/mnt/home/vgoudal/venvs/polymathic-inference-server/media_service"

WORKER_BASE_PORT = 7000
WORKER_HOST = "localhost"

def start_server(server_path, port, host, env_vars, venv_path):
    env = os.environ.copy()
    for name, value in env_vars.items():
        env[name] = str(value)

    python_executable_path = os.path.join(venv_path, "bin", "python")

    return subprocess.Popen([
        python_executable_path,
        "-m",
        "uvicorn",
        f"{server_path}.app:app",
        "--host", host,
        "--port", str(port),
    ], env=env, cwd=os.path.dirname(os.path.abspath(__file__)))


def start_servers():
    procs = []
    used_ports = []

    # --- GATEWAY ---
    gateway_proc = start_server(
        "gateway",
        GATEWAY_PORT,
        GATEWAY_HOST,
        {"GATEWAY_PORT": GATEWAY_PORT, "GATEWAY_HOST": GATEWAY_HOST, "MEDIA_FILES_PATH": MEDIA_FILES_PATH},
        GATEWAY_VENV_PATH
    )
    procs.append(("gateway", gateway_proc))
    used_ports.append(GATEWAY_PORT)

    models = os.listdir(MODELS_PATH)
    size_idx = 0
    for model_idx, model_id in enumerate(models):
        media_service_port = MEDIA_SERVICE_BASE_PORT + model_idx

        # --- MEDIA SERVICE ---
        media_service_proc = start_server(
            "media_service",
            media_service_port,
            MEDIA_SERVICE_HOST,
            {"MEDIA_SERVICE_PORT": media_service_port,
            "MEDIA_SERVICE_HOST": MEDIA_SERVICE_HOST,
            "MODELS_PATH": MODELS_PATH,
            "MEDIA_FILES_PATH": MEDIA_FILES_PATH,
            "GATEWAY_PORT": GATEWAY_PORT,
            "GATEWAY_HOST": GATEWAY_HOST,
            "MODEL_ID": model_id},
            MEDIA_SERVICE_VENV_PATH
        )
        procs.append((f"{model_id}-media-service", media_service_proc))
        used_ports.append(media_service_port)

        model_sizes = get_model_sizes_from_config(MODELS_PATH, model_id)
        venv_file_path = os.path.join(MODELS_PATH, model_id, "inference.env")
        load_dotenv(venv_file_path)
        worker_venv_path = os.getenv("VENV_PATH")

        for size in model_sizes:    
            worker_port = WORKER_BASE_PORT + size_idx

            # --- WORKER ---
            worker_proc = start_server(
                "worker",
                worker_port,
                WORKER_HOST,
                {"WORKER_PORT": worker_port,
                 "WORKER_HOST": WORKER_HOST,
                 "MODELS_PATH": MODELS_PATH,
                 "MEDIA_SERVICE_PORT": media_service_port,
                 "MEDIA_SERVICE_HOST": MEDIA_SERVICE_HOST,
                 "MODEL_ID": model_id,
                 "SIZE_ID": size["id"]},
                worker_venv_path
            )
            procs.append((f"{model_id}-{size['id']}-worker", worker_proc))
            used_ports.append(worker_port)
            size_idx += 1

    return procs, used_ports

if __name__ == "__main__":
    procs, used_ports = start_servers()
    try:
        prints("Starting servers...")
        for idx, (name, proc) in enumerate(procs):
            prints(f"Start {name} ({idx + 1}/{len(procs)})")
        for name, proc in procs:
            proc.wait()
    except KeyboardInterrupt:
        prints("Shutting down...")
        for idx, (name, proc) in enumerate(procs):
            prints(f"Shutdown {name} ({idx + 1}/{len(procs)})")
            proc.terminate()
        for proc in (p for _, p in procs):
            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                proc.kill()
        prints("Freeing ports...")
        kill_ports(used_ports)
        prints("All servers shutdown")