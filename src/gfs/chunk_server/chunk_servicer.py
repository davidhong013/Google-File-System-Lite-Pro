import grpc
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from .. import gfs_pb2, gfs_pb2_grpc

from ..common import Config as cfg, Status


class ChunkServerToClientServicer(gfs_pb2_grpc.ChunkServerToClientServicer):
    def __init__(self,address:str):
        self.address = address #this should be the IP address that chunk server is running on

    def Create(self, request, context):
        file_name =  request.chunk_id
        directory = './chunk_storage/' + file_name
        print(directory)
        with open(directory, 'w') as file:
            file.write("Initiated a file in GFS_Lite_Pro")
        return gfs_pb2.ChunkResponse(success = True,message = "Initiated a file",available_space = cfg.default_chunk_size)
