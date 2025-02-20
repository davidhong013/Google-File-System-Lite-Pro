import os
import sys

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


