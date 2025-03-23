import grpc

from concurrent import futures
from .master_servicer import MasterServerToClientServicer
from .master_server_data import MasterServer
from .. import gfs_pb2_grpc
from ..common import Config as cfg
import sys

def serve():

    # Set up the server with thread pool for handling requests
    if len(sys.argv) < 4:
        print("Error: Please specify if you want to enable dynamic allocation", file=sys.stderr)
        sys.exit(1)
    option = sys.argv[1]
    if option != 'dynamic' and option != 'undynamic':
        print("Error: Please specify if you want to enable dynamic allocation, enter dynamic or undynamic", file=sys.stderr)
        sys.exit(1)
    portion = sys.argv[2]
    sleep_second = sys.argv[3]
    master = MasterServer(portion=float(portion), sleep_second=int(sleep_second))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4),options=cfg.message_options)
    gfs_pb2_grpc.add_MasterServerToClientServicer_to_server(
        MasterServerToClientServicer(master=master, option = option), server
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
