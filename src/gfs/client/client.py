import grpc
import os
import sys
from typing import List,Dict
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from .. import gfs_pb2, gfs_pb2_grpc
from ..common import Config as cfg, isint
from .client_lease import ClientLease



class GFSClient:
    def __init__(self):
        """Initialize the GFS Client with configuration"""
        self.master = cfg.master_loc  # Master server location
        self.fileLocationCache: Dict[str, ClientLease] = {} # maps the file names to ClientLease object

    def request_lease(self,file_path:str) -> bool:
        """communicate with master server to get a new lease for a file,
        returns false if no lease can be returned"""
        try:
            with grpc.insecure_channel(self.master) as channel:
                stub = gfs_pb2_grpc.MasterServerToClientStub(channel)
                request = gfs_pb2.FileRequest(filename=file_path)
                file_response = stub.RequestLease(request)

            if not file_response or not file_response.success:
                print("Error occurred, request Lease on file failed")
                return False

            data = file_response.message.split("|")
            secondary_chunks = None if len(data) < 4 else data[2: -1]
            client_lease = ClientLease(lease_assign_time=datetime.strptime(data[0], '%H:%M:%S').time(),
                                       primary_chunk=data[1],
                                       secondary_chunks=secondary_chunks,
                                       version_number=data[-1])
            self.fileLocationCache[file_path] = client_lease

        except grpc.RpcError as e:
            print(f"GRPC Error: {e.code()}: {e.details()}")
        except Exception as e:
            print(f"An error occurred: {e}")
        return True

    def list_files(self, file_path: str):
        """List files in the specified directory"""
        try:
            with grpc.insecure_channel(self.master) as channel:
                stub = gfs_pb2_grpc.MasterServerToClientStub(channel)
                request = gfs_pb2.StringMessage(value=file_path)
                master_response = stub.ListFiles(request).value

                if master_response:
                    fps = master_response.split("|")
                    print(fps)
                else:
                    print("No files found.")
        except grpc.RpcError as e:
            print(f"GRPC Error: {e.code()}: {e.details()}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def create_file(self, file_path: str):
        """Create a new file in GFS"""
        try:
            with grpc.insecure_channel(self.master) as channel:
                stub = gfs_pb2_grpc.MasterServerToClientStub(channel)
                request = gfs_pb2.FileRequest(filename=file_path)
                file_response = stub.CreateFile(request)

            if not file_response or not file_response.success:
                print("Error occurred, file creation failed")
                return -1

            data = file_response.message.split("|")
            chunk_index = data[0]
            print("Hi, I'm here " + chunk_index)
            file_path = file_path.replace("/", "_")  # Simplified file naming
            print(file_path)

            for chunk_server in data[1:]:
                with grpc.insecure_channel(chunk_server) as channel:
                    stub = gfs_pb2_grpc.ChunkServerToClientStub(channel)
                    chunk_request = gfs_pb2.ChunkRequest(chunk_id=file_path + "_" + chunk_index)
                    chunk_response = stub.Create(chunk_request)

                    if not chunk_response or not chunk_response.success:
                        print("Error occurred when talking to the chunk servers")
                        return -1

        except grpc.RpcError as e:
            print(f"GRPC Error: {e.code()}: {e.details()}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def run(self):
        """Main loop for client interaction"""
        try:
            while True:
                command = input("Enter command: ").strip()
                parts = command.split(maxsplit=1)

                if not parts:
                    continue  # Ignore empty input

                cmd = parts[0].lower()
                arg = parts[1] if len(parts) > 1 else None

                if cmd == "exit":
                    print("Exiting program...")
                    break
                elif cmd == "list":
                    if arg:
                        self.list_files(arg)
                    else:
                        print("Error: 'list' command requires a file path.")
                elif cmd == "create":
                    if arg:
                        self.create_file(arg)
                    else:
                        print("Error: 'create' command requires a file path.")
                else:
                    print(f"Unknown command: {cmd}")

        except KeyboardInterrupt:
            print("\nProgram interrupted. Exiting...")

def main():
    client = GFSClient()
    client.run()



