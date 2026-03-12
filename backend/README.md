## Launcher

```
module load python/3.12
python -m venv ~/venvs/polymathic-inference-server/launcher
source ~/venvs/polymathic-inference-server/launcher/bin/activate
pip install --upgrade pip
pip install --upgrade dotenv PyYAML
```
```
module load modules/2.4
module load python/3.12
module use ~/modulefiles
module load cuda/13.1
module load ffmpeg
source ~/venvs/polymathic-inference-server/launcher/bin/activate
cd /mnt/home/vgoudal/polymathic-inference-server/backend
python server_launcher.py
```

## Gateway

```
module load python/3.12
module use ~/modulefiles
module load cuda/13.1
python -m venv ~/venvs/polymathic-inference-server/gateway
source ~/venvs/polymathic-inference-server/gateway/bin/activate
pip install --upgrade pip
pip install --upgrade pydantic fastapi uvicorn httpx
```

## Media_service

```
module load modules/2.4
module load python/3.12
module use ~/modulefiles
module load cuda/13.1
module load ffmpeg
python -m venv ~/venvs/polymathic-inference-server/media_service
source ~/venvs/polymathic-inference-server/media_service/bin/activate
pip install --upgrade pip
pip install --upgrade pillow matplotlib numpy
pip install --upgrade pydantic fastapi uvicorn httpx
pip install torch==2.10.0 torchvision --index-url https://download.pytorch.org/whl/cu130
```