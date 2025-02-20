import grpc
import gfs_pb2_grpc
import gfs_pb2

from common import Config as cfg
from common import Status
class MasterServerToClientServicer(gfs_pb2_grpc.MasterServerToClientServicer):
    # def __init__(self, master):
    #     self.master = master
    def __init__():
        pass

    def ListFiles(self, request, context):
        file_path = request.value
        print("Command List {}".format(file_path))
        # fpls = self.master.list_files(file_path)
        fpls = ['/testing1', '/testing2']
        st = "|".join(fpls)
        return gfs_pb2.StringMessage(value=st)
    