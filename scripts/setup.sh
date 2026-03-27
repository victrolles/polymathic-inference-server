module load modules/2.4
module load docker/28
module load node-js/22
module load npm/11

cd $HOME/polymathic-inference-server

# frontend
./scripts/build/frontend.sh
./scripts/deploy/frontend.sh

minikube service frontend-service