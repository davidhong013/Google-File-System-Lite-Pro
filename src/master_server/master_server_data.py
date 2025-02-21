class MasterServer:
    def __init__(self):
        self.file_list = {}

    def list_files(self, path):
        result = []
        
        for file in self.file_list:
            if file.startswith(path.rstrip("/") + "/"): 
                result.append(file)
        
        return result
            