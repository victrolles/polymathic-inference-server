module load modules/2.4
module load docker/28
module load node-js/22
module load npm/11
module load python/3.12

cd $HOME/polymathic-inference-server

kubectl delete all --all

# build
./scripts/build/frontend.sh
./scripts/build/gateway.sh

# deploy
./scripts/deploy/storage.sh
./scripts/deploy/frontend.sh
./scripts/deploy/gateway.sh

# start
# minikube service frontend-service
# minikube service gateway-service