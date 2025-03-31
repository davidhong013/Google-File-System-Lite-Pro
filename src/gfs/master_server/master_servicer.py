import os
import sys
from .master_server_data import MasterServer

import grpc

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from .. import gfs_pb2, gfs_pb2_grpc


class MasterServerToClientServicer(gfs_pb2_grpc.MasterServerToClientServicer):
    def __init__(self, master: MasterServer, option="dynamic"):
        self.master = master

        """this initiates the dynamic allocation, if you do not want to dynamically allocate chunks, turn it off"""
        if option == "dynamic":
            self.master.start_dynamic_allocation()

    def ListFiles(self, request, context):
        """This function is used to list all the files in the file system, it simply traverses through
        the dictionary and return those who are matched"""
        file_path = request.value
        # print("Command List {}".format(file_path))
        fpls = self.master.list_files(file_path)
        st = "|".join(fpls)
        return gfs_pb2.StringMessage(value=st)

    def CreateFile(self, request, context):
        """THis function is used to create a new file in the file system. The default number of replicas
        of file chunks are two, and thus two chunk servers will be assigned. It also returns a chunk index of 0
        """
        file_path = request.filename
        answer = self.master.create_files(file_path)
        if answer[0] == "Error":
            return gfs_pb2.FileResponse(success=False, message="file creation failed")
        answer_transform = "0|" + "|".join(answer)
        return gfs_pb2.FileResponse(success=True, message=answer_transform)

    def RequestLease(self, request, context):
        """This function is used to grant lease access to clients who want to read and write to a file"""
        file_path = request.filename
        answer = self.master.request_lease(file_path)
        if answer[0] == "Error":
            return gfs_pb2.FileResponse(
                success=False, message="Lease cannot be requested"
            )
        answer_transform = "|".join(answer)
        return gfs_pb2.FileResponse(success=True, message=answer_transform)

    def VerifyLease(self, request, context):
        """This function is used to return a version number to clients in order to verify the number of chunk
        servers of a file"""
        file_path = request.filename
        answer = self.master.verify_lease(file_path)
        if answer == "Error":
            return gfs_pb2.FileResponse(
                success=False, message="Lease cannot be verified"
            )
        return gfs_pb2.FileResponse(success=True, message=answer)

    def AppendFile(self, request, context):
        file_path = request.filename
        answer = self.master.append_file(file_path)
        if answer == "Error":
            return gfs_pb2.FileResponse(
                success=False,
                message="write failed, such file does not exist the file system",
            )
        return gfs_pb2.FileResponse(success=True, message=answer)

    def AppendAck(self, request, context):
        file_path = request.filename
        answer = self.master.append_ack(file_path)
        if answer == "Error":
            return gfs_pb2.FileResponse(success=False, message="Ack failed")
        return gfs_pb2.FileResponse(success=True, message=answer)
