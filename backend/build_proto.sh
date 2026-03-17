#!/bin/bash
# Build script for gRPC protocol buffers

set -e

echo "Compiling gRPC protocol buffers..."

cd backend

# Create generated directory
mkdir -p app/grpc_generated

# Compile Python gRPC code
python -m grpc_tools.protoc \
    --proto_path=protos \
    --python_out=app/grpc_generated \
    --grpc_python_out=app/grpc_generated \
    protos/ue_ai_service.proto

echo "✓ Protocol buffers compiled successfully"
echo "Generated files:"
ls -la app/grpc_generated/
