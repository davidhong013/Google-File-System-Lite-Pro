from master_servicer import MasterServerToClientServicer
from master_server_data import MasterServer
from concurrent import futures
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add it to sys.path
sys.path.append(parent_dir)
import grpc
import gfs_pb2_grpc
import gfs_pb2


def serve():

    # Set up the server with thread pool for handling requests
    master = MasterServer()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    gfs_pb2_grpc.add_MasterServerToClientServicer_to_server(
        MasterServerToClientServicer(master=master), server
    )
    server.add_insecure_port("[::]:50051")

    # Start the server
    server.start()
    print("Server started on port 50051.")

    try:
        # Keep the server running and handle requests
        server.wait_for_termination()  # This is the recommended way to keep the server running
    except KeyboardInterrupt:
        print("Shutting down server.")
        server.stop(0)  # Gracefully stop the server


if __name__ == "__main__":
    serve()
