docker build -t auto-loop .
id=$(docker create auto-loop)
docker cp $id:/app/client_pb2.py .
docker cp $id:/app/client_pb2_grpc.py .
docker rm -v $id
