rm -f *.pyc
rm -rf __pycache__
rm -f gfs_pb2_grpc.py
rm -f gfs_pb2.py
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./gfs.proto
