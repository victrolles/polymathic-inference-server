module load modules/2.4
module load docker/28

cd $HOME/polymathic-inference-server

#frontend
./scripts/build/frontend.sh
./scripts/deploy/frontend.sh