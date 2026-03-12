module load python/3.12
python -m venv ~/venvs/polymathic-inference-server/launcher
source ~/venvs/polymathic-inference-server/launcher/bin/activate
pip install --upgrade pip
pip install --upgrade dotenv PyYAML

module load python/3.12
source ~/venvs/polymathic-inference-server/launcher/bin/activate
cd /mnt/home/vgoudal/polymathic-inference-server/backend
python server_launcher.py