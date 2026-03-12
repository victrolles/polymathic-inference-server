module load python/3.12
module use ~/modulefiles
module load cuda/13.1
python -m venv ~/venvs/polymathic-inference-server/gateway
source ~/venvs/polymathic-inference-server/gateway/bin/activate
pip install --upgrade pip
pip install --upgrade pydantic fastapi uvicorn pillow datasets matplotlib

module load python/3.12
module use ~/modulefiles
module load cuda/13.1
source ~/venvs/polymathic-inference-server/gateway/bin/activate
python /mnt/home/vgoudal/polymathic-inference-server/backend/gateway/server.py