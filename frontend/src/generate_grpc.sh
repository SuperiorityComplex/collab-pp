protoc -I=../../backend grpc_stubs/protos/main.proto --js_out=import_style=commonjs,binary:. --grpc-web_out=import_style=commonjs,mode=grpcwebtext:.
