import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add it to sys.path
sys.path.append(parent_dir)
import grpc
import gfs_pb2_grpc
import gfs_pb2

from common import Config as cfg
from common import Status
class ChunkServerToClientServicer(gfs_pb2_grpc.ChunkServerToClientServicer):
    def __init__(self):
        pass

    def Create(self, request, context):
        pass
