import os
import sys
import random
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from typing import List, Dict
from ..common import Config as cfg, Status
from .master_utils import FileObject,ChunkObject
from datetime import datetime, time
class MasterServer:
    def __init__(self):
        self.file_list: Dict[str, FileObject] = {}
        self.file_list['/'] = None

    def list_files(self, path:str) -> List[str]:
        result = []

        for file in self.file_list:
            if file.startswith(path.rstrip("/") + "/"):
                result.append(file)

        return result
    
    def create_files(self, path:str,  num_of_replicas = 2) -> List[str]:
        parent_dir = os.path.dirname(path)
        if parent_dir not in self.file_list or path in self.file_list:
            return ['Error']
        sampled_address = random.sample(cfg.chunkserver_locs,num_of_replicas)
        file_object = FileObject(path)
        for address in sampled_address:
            chunk = ChunkObject(address)
            file_object.add_chunk_server(chunk)
        self.file_list[path] = file_object
        return sampled_address

    def request_lease(self, path:str) -> List[str]:
        if path not in self.file_list:
            return ['Error']
        chunk_array = self.file_list[path].get_chunk_array()
        main_chunk = random.sample(chunk_array,1)[0].chunk_address
        secondary_chunks = []
        for chunk in chunk_array:
            if chunk.chunk_address != main_chunk:
                secondary_chunks.append(chunk.chunk_address)
        now = datetime.now().time()

        # Convert datetime to string
        time_str = now.strftime('%H:%M:%S')
        answer = [time_str, main_chunk]
        answer.extend(secondary_chunks)
        answer.append(str(self.file_list[path].version_number))
        return answer

    def verify_lease(self,path) -> str:
        if path not in self.file_list:
            return 'Error'
        return str(self.file_list[path].version_number)

    def append_file(self,path) -> str:
        if path not in self.file_list:
            return 'Error'
        file_object = self.file_list[path]
        with file_object.file_lock:
            while file_object.is_busy:
                file_object.file_wait_queue.wait()
            file_object.is_busy = True
        return 'True'

    def append_ack(self,path:str) -> str:
        if path not in self.file_list:
            return 'Error'
        file_object = self.file_list[path]
        with file_object.file_lock:
            file_object.is_busy = False
            file_object.file_wait_queue.notify_all()
        return 'True'



        
        
        
        
