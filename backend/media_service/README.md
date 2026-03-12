module load modules/2.4
module load python/3.12
module use ~/modulefiles
module load cuda/13.1
module load ffmpeg
python -m venv ~/venvs/polymathic-inference-server/media-service
source ~/venvs/polymathic-inference-server/media-service/bin/activate
pip install --upgrade pip
pip install --upgrade pillow matplotlib numpy
pip install --upgrade pydantic fastapi uvicorn 
pip install torch==2.10.0 torchvision --index-url https://download.pytorch.org/whl/cu130

module load modules/2.4
module load python/3.12
module use ~/modulefiles
module load cuda/13.1
module load ffmpeg
source ~/venvs/polymathic-inference-server/media-service/bin/activate
python /mnt/home/vgoudal/polymathic-inference-server/backend/media-service/server.py