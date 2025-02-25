import grpc
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from .. import gfs_pb2, gfs_pb2_grpc
from ..common import Config as cfg, isint


def list_files(file_path):
    try:
        master = cfg.master_loc
        with grpc.insecure_channel(master) as channel:
            stub = gfs_pb2_grpc.MasterServerToClientStub(channel)
            request = gfs_pb2.StringMessage(
                value=file_path
            )  # Make sure this matches your .proto definition
            master_response = stub.ListFiles(
                request
            ).value  # Ensure this is a string returned by the method
            if master_response:
                fps = master_response.split(
                    "|"
                )  # this is meant to be implemented in the master server later on
                print(fps)
            else:
                print("No files found.")
    except grpc.RpcError as e:
        print(f"GRPC Error: {e.code()}: {e.details()}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return 0


def create_file(file_path:str):
    try:
        master = cfg.master_loc
        file_response = None
        with grpc.insecure_channel(master) as channel:
            stub = gfs_pb2_grpc.MasterServerToClientStub(channel)
            request = gfs_pb2.FileRequest(
                filename=file_path
            )  # Make sure this matches your .proto definition
            file_response = stub.CreateFile(
                request
            )  # Ensure this is a string returned by the method

        if not file_response or not file_response.success:
            print("Error occured, file creation failed")
            return -1

        data = file_response.message.split("|")
        chunk_index = data[0]
        print("Hi im here" + chunk_index)
        file_path = file_path.replace("/", "_")
        # this is because we are not going to implement a rigorous file system path name using trees
        print(file_path)
        for chunk_servers in data[1:]:
            with grpc.insecure_channel(chunk_servers) as channel:
                stub = gfs_pb2_grpc.ChunkServerToClientStub(channel)
                chunk_request = gfs_pb2.ChunkRequest(
                    chunk_id=file_path + "_" + chunk_index
                )
                chunk_response = stub.Create(chunk_request)
                if not chunk_response or not chunk_response.success:
                    print("Error occured when talking to the chunk servers")
                    return -1

    except grpc.RpcError as e:
        print(f"GRPC Error: {e.code()}: {e.details()}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return 0


def main():
    try:
        while True:
            command = input("Enter command: ").strip()
            parts = command.split(maxsplit=1)  # Split into command and argument

            if not parts:
                continue  # Ignore empty input

            cmd = parts[0].lower()  # First part is the command
            arg = (
                parts[1] if len(parts) > 1 else None
            )  # Second part is the argument (if exists)

            if cmd == "exit":
                print("Exiting program...")
                break
            elif cmd == "list":
                if arg:
                    list_files(arg)
                    # print(arg)
                else:
                    print("Error: 'list' command requires a file path.")
            elif cmd == "create":
                if arg:
                    create_file(arg)
                else:
                    print("Error: 'create' command requires a file path.")
            else:
                print(f"Unknown command: {cmd}")

    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")


if __name__ == "__main__":
    main()
