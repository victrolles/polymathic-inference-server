echo "==== Loading modules ===="
module load modules/2.4
module load python/3.12
module use ~/modulefiles
module load cuda/13.1
module load ffmpeg

echo "==== Installing dependencies for media service ===="
source ~/venvs/polymathic-inference-server/media_service/bin/activate
pip install --upgrade pip
MODELS_ROOT="/mnt/home/vgoudal/polymathic-inference-server/models"
for req in "$MODELS_ROOT"/*/requirements.txt; do
  if [ -f "$req" ]; then
    echo "pip install -r $req"
    pip install -r "$req"
  fi
done
deactivate

echo "==== Activating virtual environment for launcher ===="
source ~/venvs/polymathic-inference-server/launcher/bin/activate

echo "==== Starting servers ===="
cd /mnt/home/vgoudal/polymathic-inference-server/backend
python server_launcher.py