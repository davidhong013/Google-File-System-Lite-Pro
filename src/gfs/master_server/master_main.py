import argparse
import grpc

from concurrent import futures
from .master_servicer import MasterServerToClientServicer
from .master_server_data import MasterServer
from .. import gfs_pb2_grpc
from ..common import Config as cfg


def serve():
    argparser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="GFS Master Server"
    )
    argparser.add_argument(
        "option",
        choices=["dynamic", "static"],
        type=str,
        help="The option of the master server.",
    )
    argparser.add_argument(
        "portion",
        type=float,
        help="The portion of the master server.",
    )
    argparser.add_argument(
        "sleep_second",
        type=int,
        help="The sleep second of the master server.",
    )
    args: argparse.Namespace = argparser.parse_args()
    option = args.option
    portion = args.portion
    sleep_second = args.sleep_second
    master = MasterServer(portion=portion, sleep_second=sleep_second)
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=96), options=cfg.message_options
    )
    gfs_pb2_grpc.add_MasterServerToClientServicer_to_server(
        MasterServerToClientServicer(master=master, option=option), server
    )
    server.add_insecure_port("[::]:50051") #124.124.1251 localhost:50051

    # Start the server
    server.start()
    print("Server started on port 50051.")

    try:
        # Keep the server running and handle requests
        server.wait_for_termination()  # This is the recommended way to keep the server running
    except KeyboardInterrupt:
        print("Shutting down the server.")
        server.stop(0)  # Gracefully stop the server


if __name__ == "__main__":
    serve()
