import grpc
from .. import gfs_pb2, gfs_pb2_grpc

from ..common import Config as cfg, Status


class ChunkServerToClientServicer(gfs_pb2_grpc.ChunkServerToClientServicer):
    def __init__(self):
        pass

    def Create(self, request, context):
        pass
