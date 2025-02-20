import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add it to sys.path
sys.path.append(parent_dir)
import grpc
import gfs_pb2_grpc
import gfs_pb2

from common import Config as cfg
from common import isint

def list_files(file_path):
    try:
        master = cfg.master_loc
        with grpc.insecure_channel(master) as channel:
            stub = gfs_pb2_grpc.MasterServerToClientStub(channel)
            request = gfs_pb2.StringMessage(value=file_path)  # Make sure this matches your .proto definition
            master_response = stub.ListFiles(request).value  # Ensure this is a string returned by the method
            if master_response:
                fps = master_response.split("|")  # this is meant to be implemented in the master server later on
                print(fps)
            else:
                print("No files found.")
    except grpc.RpcError as e:
        print(f"GRPC Error: {e.code()}: {e.details()}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    try:
        while True:
            command = input("Enter command: ").strip()
            parts = command.split(maxsplit=1)  # Split into command and argument
            
            if not parts:
                continue  # Ignore empty input
            
            cmd = parts[0].lower()  # First part is the command
            arg = parts[1] if len(parts) > 1 else None  # Second part is the argument (if exists)

            if cmd == "exit":
                print("Exiting program...")
                break
            elif cmd == "list":
                if arg:
                    list_files(arg)
                    # print(arg)
                else:
                    print("Error: 'list' command requires a file path.")
            else:
                print(f"Unknown command: {cmd}")

    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")

if __name__ == "__main__":
    main()



