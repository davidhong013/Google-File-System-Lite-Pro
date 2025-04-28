import grpc
import os
import sys
from typing import List, Dict

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from .. import gfs_pb2, gfs_pb2_grpc
from .chunk_utils import ChunkFileObject
from ..common import Config as cfg, Status


class ChunkServerToClientServicer(
    gfs_pb2_grpc.ChunkServerToClientServicer,
    gfs_pb2_grpc.ChunkServerToChunkServerServicer,
    gfs_pb2_grpc.ChunkServerToMasterServerServicer,
):
    def __init__(self, address: str):
        self.address = (
            address  # this should be the IP address that chunk server is running on
        )
        self.metaData: Dict[str, ChunkFileObject] = {}

    def Create(self, request, context):
        file_name = request.chunk_id
        file_object = ChunkFileObject(file_name)
        file_object.chunks_names_array.append(file_name + "_0")
        self.metaData[file_name] = file_object
        directory = "./src/gfs/chunk_server/chunk_storage/" + file_name + "_0"

        try:
            with open(directory, "wb") as file:
                text = "Initiated a file in GFS_Lite_Pro\n"
                file.write(text.encode("utf-8"))
        except Exception as e:
            print(f"[ERROR] Failed to create file '{directory}': {e}")
            return gfs_pb2.ChunkResponse(success=False, message=f"Failed to initiate file: {e}")

        return gfs_pb2.ChunkResponse(success=True, message="Initiated a file")

    def __internal_create(self, file_name) -> bool:
        file_object = ChunkFileObject(file_name)
        file_object.chunks_names_array.append(file_name + "_0")
        self.metaData[file_name] = file_object
        directory = "./src/gfs/chunk_server/chunk_storage/" + file_name + "_0"
        with open(directory, "wb") as file:
            text = "Initiated a file in GFS_Lite_Pro\n"
            file.write(text.encode("utf-8"))
        return True

    def __inwrite(self, file_name, content: str) -> bool:
        file_object = self.metaData[file_name]
        content = content.encode("utf-8")
        cursor = 0
        content_length = len(content)
        chunk_index = len(file_object.chunks_names_array) - 1
        while cursor < content_length:
            available_to_write = cfg.default_chunk_size - file_object.offset
            left_to_write = content_length - cursor
            if available_to_write >= left_to_write:
                file_object.offset += left_to_write
                directory = (
                    f"./src/gfs/chunk_server/chunk_storage/{file_name}_{chunk_index}"
                )
                with open(directory, "ab") as file:
                    file.write(content[cursor : cursor + left_to_write])
                cursor += left_to_write
            else:
                bytes_to_write = available_to_write
                directory = (
                    f"./src/gfs/chunk_server/chunk_storage/{file_name}_{chunk_index}"
                )
                with open(directory, "ab") as file:
                    file.write(content[cursor : cursor + bytes_to_write])
                cursor += bytes_to_write
                chunk_index += 1
                file_object.chunks_names_array.append(
                    file_name + "_" + str(chunk_index)
                )
                file_object.offset = 0
        return True

    def Append_ChunkToChunk(self, request, context):
        file_name = request.file_name
        content = request.content
        if not self.__inwrite(file_name, content):
            return gfs_pb2.ChunkResponse(
                success=False, message="Writing to the secondary chunk failed"
            )
        return gfs_pb2.ChunkResponse(success=True, message="Write Succeeded")

    def Append(self, request, context):
        """Basic work flow:
        1. Write to the primary chunk server first
        2. Write to the secondary chunk servers
        3. Gets ack/no acks from secondary chunk servers
        4. Sends response back to clients"""
        file_name = request.file_name
        content = request.content
        secondary_chunks = (
            request.secondary_chunk.split("|") if request.secondary_chunk else []
        )
        if file_name not in self.metaData:
            return gfs_pb2.ChunkResponse(
                success=False, message="The file does not exist"
            )

        # Write to the primary chunk server's disk
        result = self.__inwrite(file_name, content)
        # print('write to the disk successfully')
        if not result:
            return gfs_pb2.ChunkResponse(
                success=False, message="Writing to the primary chunk failed"
            )

        for secondary_chunk in secondary_chunks:
            with grpc.insecure_channel(
                secondary_chunk, options=cfg.message_options
            ) as channel:
                stub = gfs_pb2_grpc.ChunkServerToChunkServerStub(channel)
                request = gfs_pb2.AppendRequest(
                    file_name=file_name, content=content, secondary_chunk=""
                )
                chunk_response = stub.Append_ChunkToChunk(request)
            if not chunk_response or not chunk_response.success:
                return gfs_pb2.ChunkResponse(
                    success=False, message="writing to the secondary chunks failed"
                )

        return gfs_pb2.ChunkResponse(success=True, message="Write Succeeded")

    def ChunkNumber(self, request, context):
        file_name = request.filename
        if file_name not in self.metaData:
            return gfs_pb2.FileResponse(
                success=False, message="The file does not exist"
            )
        return gfs_pb2.FileResponse(
            success=True, message=str(len(self.metaData[file_name].chunks_names_array))
        )

    def Read(self, request, context):
        file_name = request.filename
        chunk_index = request.chunk_index
        if file_name not in self.metaData:
            return gfs_pb2.ReadResponse(success=False)
        with self.metaData[file_name].lock:
            self.metaData[file_name].number_of_reads += 1
        directory = (
            "./src/gfs/chunk_server/chunk_storage/" + file_name + "_" + str(chunk_index)
        )
        with open(directory, "rb") as file:
            bytes = file.read()
        return gfs_pb2.ReadResponse(success=True, data=bytes)

    def GetNumOfRead(self, request, context):
        """When master server calls this function, it should reset the number of reads on a file"""

        file_name = request.filename

        if file_name not in self.metaData:
            print(
                "receieves get number of read requests from master server, and the file does not exist"
            )
            print(file_name)
            print(self.metaData)
            return gfs_pb2.ChunkResponse(
                success=False, message="The file does not exist"
            )
        num_read = self.metaData[file_name].number_of_reads
        with self.metaData[file_name].lock:
            self.metaData[file_name].number_of_reads = 0
        return gfs_pb2.ChunkResponse(success=True, message=str(num_read))

    def SyncChunkData(self, request, context):
        file_name = request.file_name
        content = request.content
        # First step, clean the old meta data and old file on disk
        if file_name in self.metaData:
            chunk_len = len(self.metaData[file_name].chunks_names_array)
            for chunk_index in range(chunk_len):
                directory = (
                    "./src/gfs/chunk_server/chunk_storage/"
                    + file_name
                    + "_"
                    + str(chunk_index)
                )
                if os.path.exists(directory):
                    try:
                        os.remove(directory)  # Delete the file
                    except OSError as e:
                        print(f"Error deleting {directory}: {e}", file=sys.stderr)
                else:
                    print(f"File not found: {directory}", file=sys.stderr)
            del self.metaData[file_name]

        # second step, recreate the file and write content to it
        if not self.__internal_create(file_name) or not self.__inwrite(
            file_name, content
        ):
            return gfs_pb2.ChunkResponse(
                success=False, message="Data Recreation failed during synchronization"
            )

        return gfs_pb2.ChunkResponse(
            success=True, message="Data Synchronization succeeded"
        )

    def DuplicateFile(self, request, context):
        source = request.source
        destination = request.destination
        file_name = request.file_name
        file_object = self.metaData[file_name]
        content = ""

        # the content of the file is stored as binary format on the disk
        for index in range(len(file_object.chunks_names_array)):
            directory = (
                "./src/gfs/chunk_server/chunk_storage/" + file_name + "_" + str(index)
            )
            with open(directory, "rb") as file:
                content += file.read().decode("utf-8")

        with grpc.insecure_channel(destination, options=cfg.message_options) as channel:
            stub = gfs_pb2_grpc.ChunkServerToChunkServerStub(channel)
            request = gfs_pb2.SyncRequest(file_name=file_name, content=content)
            response = stub.SyncChunkData(request)
        if not response or not response.success:
            return gfs_pb2.ChunkResponse(
                success=False, message="Data Synchronization failed"
            )
        return gfs_pb2.ChunkResponse(
            success=True, message="Data Synchronization Successful"
        )
