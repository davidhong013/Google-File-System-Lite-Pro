from collections import deque
import sys
import os
from typing import List, Dict
import threading
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from ..common import Config as cfg, Status


class ChunkObject:
    def __init__(self, chunk_address:str):
        self.chunk_address = chunk_address

class FileObject:
    def __init__(self, file_name: str):
        self.file_name = file_name  # Private variable (double underscore)
        self.version_number = 0 # Private variable, this variable is mainly used to check
                                # within the heartbeat message.
                                # we need a hearbeat meassage because the master server is going to dynamically
                                # allocate chunk servers based on user needs
                                # we might need a lock for this version number

        ##this is the variable that records the corresponding chunk servers for a single file object
        self.__chunk_array = []  # Private variable

        # we need a lock for this file object so that only one user can write to the file at a time

        """PLEASE READ!!!!!!!!!
        After talking to professor, I decided to abort concurrent write as that would create too much sync
        problems for us. In this version of GFS Lite Pro, at most one client is able to write to the file.
        Before it writes to the file, it gets the lock correspondingly to a file, mark the busy mark to be True.
        Once the master server get an ack from clients for completing write operations, the thread is going to mark 
        busy mark to be False and notify every threads(clients) who are waiting on the conditional variables to grant
        write access
        
        By doing so, we are able to make sure at most one thread/client is writing to a file at one time!!!!
        """
        self.file_lock = threading.Lock()
        self.file_wait_queue = threading.Condition(self.file_lock)
        self.is_busy = False

        self.version_lock = threading.Lock()

    # Getter for __chunk_array
    def get_chunk_array(self) -> List[ChunkObject]:
        return self.__chunk_array


    def add_chunk_server(self,chunk:ChunkObject):
        self.__chunk_array.append(chunk)

