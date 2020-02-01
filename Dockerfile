# Prepare grpc client per https://dev.lightning.community/guides/python-grpc/
FROM        python:3.7
WORKDIR     /app
RUN         pip install grpcio grpcio-tools googleapis-common-protos
RUN         git clone https://github.com/googleapis/googleapis.git
RUN         curl -o client.proto -s https://raw.githubusercontent.com/lightninglabs/loop/master/looprpc/client.proto
RUN         python -m grpc_tools.protoc --proto_path=googleapis:. --python_out=. --grpc_python_out=. client.proto

RUN         curl -o rpc.proto -s https://raw.githubusercontent.com/lightningnetwork/lnd/master/lnrpc/rpc.proto
RUN         curl -o invoices.proto -s https://raw.githubusercontent.com/lightningnetwork/lnd/master/lnrpc/invoicesrpc/invoices.proto
RUN         python -m grpc_tools.protoc --proto_path=googleapis:. --python_out=. --grpc_python_out=. rpc.proto

FROM        python:3.7
WORKDIR     /app
RUN         pip install pipenv
COPY        --from=0 /app/client_pb2.py /app
COPY        --from=0 /app/client_pb2_grpc.py /app
COPY        --from=0 /app/rpc_pb2.py /app
COPY        --from=0 /app/rpc_pb2_grpc.py /app
ADD         Pipfile* /tmp/
RUN         cd /tmp && pipenv install --system --deploy
COPY        . /app/
