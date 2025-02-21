from collections import deque
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from ..common import Config as cfg, Status


class ChunkObject:
    def __init__(self, chunk_address:str):
        self.available_disk = cfg.default_chunk_size
        self.chunk_address = chunk_address

class FileObject:
    def __init__(self, file_name: str):
        self.__file_name = file_name  # Private variable (double underscore)
        self.__number_of_visits = 0  # Private variable
        self.__chunk_array = []  # Private variable

    # Getter for __file_name
    def get_file_name(self) -> str:
        return self.__file_name

    # Setter for __file_name
    def set_file_name(self, file_name: str):
        self.__file_name = file_name

    # Getter for __number_of_visits
    def get_number_of_visits(self) -> int:
        return self.__number_of_visits

    # Setter for __number_of_visits
    def increment_number_of_visits(self):
        self.__number_of_visits += 1

    # Getter for __chunk_array
    def get_chunk_array(self) -> list:
        return self.__chunk_array

    # Setter for __chunk_array
    def append_chunk_array(self):
        self.__chunk_array.append(deque())

    def add_chunk_server(self,chunk:ChunkObject, chunkId:int):
        self.__chunk_array[chunkId].append(chunk)

