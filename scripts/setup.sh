module load modules/2.4
module load docker/28
module load node-js/22
module load npm/11
module load python/3.12
module use ~/modulefiles
module load cuda/13.1
module load helm/4.1


cd $HOME/polymathic-inference-server

# remove models directory in "deploy/helm/inference-platform"if it exists
if [ -e deploy/helm/inference-platform/models ]; then
  rm -rf deploy/helm/inference-platform/models
fi

# create models directory in "deploy/helm/inference-platform"
if [ ! -e deploy/helm/inference-platform/models ]; then
  mkdir -p deploy/helm/inference-platform/models
fi

# copy only config.yaml per model for Helm discovery (models/<name>/config.yaml)
for model_path in "models"/*; do
  if [ -d "$model_path" ] && [ -f "$model_path/config.yaml" ]; then
    model_name=$(basename "$model_path")
    mkdir -p "deploy/helm/inference-platform/models/$model_name"
    cp "$model_path/config.yaml" "deploy/helm/inference-platform/models/$model_name/config.yaml"
  fi
done

# kubectl delete all --all
# kubectl delete pvc --all

# build frontend
minikube image build \
  -t frontend:latest \
  -f apps/frontend/Dockerfile \
  .

# build gateway
minikube image build -t gateway:latest -f apps/gateway/Dockerfile .

# build media service and worker for each model
for model_path in "models"/*; do
  if [ -d "$model_path" ]; then
    model_name=$(basename "$model_path")

    echo "🔨 Building image media service for model: $model_name"

    minikube image build \
      -t "media-service:$model_name" \
      -f apps/media_service/Dockerfile \
      .

    echo "🔨 Building image worker for model: $model_name"

    minikube image build \
      -t "worker:$model_name" \
      -f apps/worker/Dockerfile \
      .

  fi
done

# deploy
kubectl apply -f deploy/k8s/storage/pvc-inspector.yaml
helm upgrade --install inference-platform deploy/helm/inference-platform \
  --set storage.enabled=true \
  --set pvcLoader.enabled=true \
  --set frontend.enabled=false \
  --set gateway.enabled=false \
  --set mediaService.enabled=false \
  --set worker.enabled=false

# Get the pods
kubectl get pods

# Load the datasets and weights to the PVCs
python scripts/fill_pvc.py

# Deploy
helm upgrade --install inference-platform deploy/helm/inference-platform \
  --set storage.enabled=true \
  --set pvcLoader.enabled=true \
  --set frontend.enabled=true \
  --set gateway.enabled=true \
  --set mediaService.enabled=true \
  --set worker.enabled=true

# Get the pods
kubectl get pods