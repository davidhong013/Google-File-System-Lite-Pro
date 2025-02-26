import os
import sys
from .master_server_data import MasterServer

import grpc
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from .. import gfs_pb2, gfs_pb2_grpc
from ..common import Config as cfg, Status


class MasterServerToClientServicer(gfs_pb2_grpc.MasterServerToClientServicer):
    def __init__(self, master:MasterServer):
        self.master = master

    def ListFiles(self, request, context):
        file_path = request.value
        print("Command List {}".format(file_path))
        fpls = self.master.list_files(file_path)
        st = "|".join(fpls)
        return gfs_pb2.StringMessage(value=st)

    def CreateFile(self, request, context):
        file_path = request.filename
        answer = self.master.create_files(file_path)
        if answer[0] == 'Error':
            return gfs_pb2.FileResponse(success = False, message="file creation failed")
        answer_transform = '0|' + '|'.join(answer)
        return gfs_pb2.FileResponse(success = True, message = answer_transform)

    def RequestLease(self, request, context):
        file_path = request.filename
        answer = self.master.request_lease(file_path)
        if answer[0] == 'Error':
            return gfs_pb2.FileResponse(success = False, message="Lease cannot be requested")
        answer_transform = '|'.join(answer)
        return gfs_pb2.FileResponse(success = True, message = answer_transform)
