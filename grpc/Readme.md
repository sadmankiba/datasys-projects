# gRPC Model Server

A linear model predicts a value from input. The model uses multiple threads, and caches predictions. The model receives requests over network through gRPC.

Model functions
  - `SetCoef(float [])` returns `string`
  - `Predict(float [])` returns `tuple(float, bool, string)`

## Dependencies

```
pip3 install grpcio==1.58.0 grpcio-tools==1.58.0
```

## Run

```
python3 -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. modelserver.proto

docker build -t grpc-model .
docker run -p 127.0.0.1:54321:5440 grpc-model
```

