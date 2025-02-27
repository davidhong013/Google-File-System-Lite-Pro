from collections import deque
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from ..common import Config as cfg, Status


class ChunkObject:
    def __init__(self, chunk_address:str):
        self.chunk_address = chunk_address

class FileObject:
    def __init__(self, file_name: str):
        self.__file_name = file_name  # Private variable (double underscore)
        self.version_number = 0 # Private variable, this variable is mainly used to check
                                # within the heartbeat message.
                                # we need a hearbeat meassage because the master server is going to dynamically
                                # allocate chunk servers based on user needs

        ##this is the variable that records the corresponding chunk servers for a single file object
        self.__chunk_array = []  # Private variable

    # Getter for __file_name
    def get_file_name(self) -> str:
        return self.__file_name

    # Setter for __file_name
    def set_file_name(self, file_name: str):
        self.__file_name = file_name



    # Getter for __chunk_array
    def get_chunk_array(self) -> list:
        return self.__chunk_array


    def add_chunk_server(self,chunk:ChunkObject):
        self.__chunk_array.append(chunk)

