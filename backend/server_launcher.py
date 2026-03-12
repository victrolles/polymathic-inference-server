import subprocess
import os

from dotenv import load_dotenv

from utils import get_model_sizes_from_config, prints

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

    # --- GATEWAY ---
    gateway_proc = start_server(
        "gateway",
        GATEWAY_PORT,
        GATEWAY_HOST,
        {"GATEWAY_PORT": GATEWAY_PORT, "GATEWAY_HOST": GATEWAY_HOST},
        GATEWAY_VENV_PATH
    )
    procs.append(("gateway", gateway_proc))

    models = os.listdir(MODELS_PATH)
    idx = 0
    for model_name in models:
        model_sizes = get_model_sizes_from_config(MODELS_PATH, model_name)
        venv_file_path = os.path.join(MODELS_PATH, model_name, "inference.env")
        load_dotenv(venv_file_path)
        worker_venv_path = os.getenv("VENV_PATH")
        for model_size in model_sizes:
            media_service_port = MEDIA_SERVICE_BASE_PORT + idx
            worker_port = WORKER_BASE_PORT + idx

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
                "WORKER_PORT": worker_port,
                "WORKER_HOST": WORKER_HOST,
                "MODEL_NAME": model_name,
                "MODEL_SIZE": model_size["id"]},
                MEDIA_SERVICE_VENV_PATH
            )
            procs.append((f"{model_name}-{model_size['id']}-media-service", media_service_proc))

            # --- WORKER ---
            worker_proc = start_server(
                "worker",
                worker_port,
                WORKER_HOST,
                {"WORKER_PORT": worker_port,"WORKER_HOST": WORKER_HOST},
                worker_venv_path
            )
            procs.append((f"{model_name}-{model_size['id']}-worker", worker_proc))
            idx += 1

    return procs

if __name__ == "__main__":
    procs = start_servers()
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
        prints("All servers shutdown")