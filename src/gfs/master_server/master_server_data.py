import os
import sys
import random
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from typing import List
from ..common import Config as cfg, Status
from .master_utils import FileObject,ChunkObject
class MasterServer:
    def __init__(self):
        self.file_list = {}
        self.file_list['/'] = None

    def list_files(self, path:str) -> List[str]:
        result = []

        for file in self.file_list:
            if file.startswith(path.rstrip("/") + "/"):
                result.append(file)

        return result
    
    def create_files(self, path:str,  num_of_replicas = 2) -> List[str]:
        parent_dir = os.path.dirname(path)
        if parent_dir not in self.file_list:
            return ['Error']
        sampled_address = random.sample(cfg.chunkserver_locs,num_of_replicas)
        file_object = FileObject(path)
        for address in sampled_address:
            chunk = ChunkObject(address)
            file_object.add_chunk_server(chunk)
        self.file_list[path] = file_object
        return sampled_address

        
        
        
        
