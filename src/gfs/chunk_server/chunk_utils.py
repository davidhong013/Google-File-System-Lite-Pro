import threading
class ChunkFileObject:
    def __init__(self, fileName:str):
        self.fileName = fileName
        self.offset = 0
        self.number_of_reads = 0
        self.lock = threading.Lock()
        self.chunks_names_array = []