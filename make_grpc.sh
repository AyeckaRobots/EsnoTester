#!/bin/bash
folder=SystemUtils/GRpc
python -m grpc_tools.protoc -I$folder --python_out=$folder --grpc_python_out=$folder --mypy_out=$folder $folder/*.proto
