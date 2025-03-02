import grpc
import os
import sys
from typing import List, Dict
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from .. import gfs_pb2, gfs_pb2_grpc
from .chunk_utils import ChunkFileObject
from ..common import Config as cfg, Status


class ChunkServerToClientServicer(gfs_pb2_grpc.ChunkServerToClientServicer):
    def __init__(self,address:str):
        self.address = address #this should be the IP address that chunk server is running on
        self.metaData: Dict[str, ChunkFileObject] = {}

    def Create(self, request, context):
        file_name =  request.chunk_id
        file_object = ChunkFileObject(file_name)
        file_object.chunks_names_array.append(file_name + '_0')
        self.metaData[file_name] = file_object
        directory = './src/gfs/chunk_server/chunk_storage/' + file_name + '_0'
        print(directory)
        with open(directory, 'w') as file:
            file.write("Initiated a file in GFS_Lite_Pro\n")
        return gfs_pb2.ChunkResponse(success = True,message = "Initiated a file",available_space = cfg.default_chunk_size)

    def __inwrite(self,file_name,content) -> bool:
        
        return False

    def Append(self, request, context):
        file_name = request.file_name
        content = request.content
        secondary_chunks = request.secondary_chunk.split('|') if request.secondary_chunk else []

