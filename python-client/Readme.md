cd ../grpc-v2
python3 -m grpc_tools.protoc -I. --python_out=../python-client/proto --grpc_python_out=../python-client/proto auth.proto stats.proto PrivateGames.proto inventory.proto
cd ../python-client/
