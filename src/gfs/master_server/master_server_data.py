import os
import sys
import random
import threading
import time
import grpc
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from .. import gfs_pb2, gfs_pb2_grpc
from typing import List, Dict
from ..common import Config as cfg, Status
from .master_utils import FileObject,ChunkObject
from datetime import datetime, time
class MasterServer:
    def __init__(self, portion = 0.3):
        self.file_list: Dict[str, FileObject] = {}
        self.file_list['/'] = None
        self.portion = portion

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

        with self.file_list[path].version_lock:
            answer.append(str(self.file_list[path].version_number))
        return answer

    def verify_lease(self,path) -> str:
        if path not in self.file_list:
            return 'Error'

        with self.file_list[path].version_lock:
            val = str(self.file_list[path].version_number)
        return val

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

    def __getStatistics(self) -> List[List]:
        stats_Arr = []
        for file in self.file_list:
            if file == '/':
                continue
            total_num_read = 0
            file_object = self.file_list[file]
            chunk_arr = file_object.get_chunk_array()
            for chunk_object in chunk_arr:
                chunk_address = chunk_object.chunk_address
                with grpc.insecure_channel(chunk_address) as channel:
                    stub = gfs_pb2_grpc.ChunkServerToMasterServerStub(channel)
                    request = gfs_pb2.FileRequest(filename=file)
                    response = stub.GetNumOfRead(request)
                if not response or not response.success:
                    print("something happened in dynamic allocation", file=sys.stderr)
                    sys.exit(1)
                total_num_read += int(response.message)
            stats_Arr.append([total_num_read / len(chunk_arr), file])
        sorted_stats = sorted(stats_Arr, key=lambda x: x[0], reverse=True)
        return sorted_stats

    def __allocate_helper(self,stats_arr:List[List]) -> bool:
        nums_to_deal = round(self.portion * len(stats_arr))
        for index in range(nums_to_deal):
            file = stats_arr[index][1]
            file_object = self.file_list[file]
            chunk_arr = file_object.get_chunk_array()
            #If it reaches the limit, then do not allocate more replicas to the file
            if len(chunk_arr) == cfg.chunk_size:
                continue

            
        return True

    def __dynamic_allocation(self) -> None:
        while True:
            #the task processes every 20 seconds
            time.sleep(20)
            #First Step: Get statistics for every files' read operations, and we need to lock it for sure
            stats_arr = self.__getStatistics()

            #Second Step: Allocate and Deallocate extra chunk servers based on the statistics.



        return

    def start_dynamic_allocation(self) -> None:
        daemon_thread = threading.Thread(target=self.__dynamic_allocation,daemon = True)
        daemon_thread.start()
        return




        
        
        
        
