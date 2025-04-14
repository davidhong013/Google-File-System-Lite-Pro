import argparse
import grpc

from concurrent import futures
from .chunk_servicer import ChunkServerToClientServicer
from .. import gfs_pb2, gfs_pb2_grpc
from ..common import Config as cfg


def serve():
    argparser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="GFS Chunk Server"
    )
    argparser.add_argument(
        "ip",
        type=str,
        help="The ip of the chunk server.",
    )
    argparser.add_argument(
        "port",
        type=str,
        help="The port of the chunk server.",
    )

    args: argparse.Namespace = argparser.parse_args()
    ip = args.ip
    port = args.port
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=48), options=cfg.message_options
    )
    chunk_server_instance = ChunkServerToClientServicer(ip)
    gfs_pb2_grpc.add_ChunkServerToClientServicer_to_server(
        chunk_server_instance, server
    )
    gfs_pb2_grpc.add_ChunkServerToChunkServerServicer_to_server(
        chunk_server_instance, server
    )
    gfs_pb2_grpc.add_ChunkServerToMasterServerServicer_to_server(
        chunk_server_instance, server
    )

    server.add_insecure_port(f"[::]:{port}")

    # Start the server
    server.start()
    print(f"Server started on port {port}.")

    try:
        # Keep the server running and handle requests
        server.wait_for_termination()  # This is the recommended way to keep the server running
    except KeyboardInterrupt:
        print("Shutting down server.")
        server.stop(0)  # Gracefully stop the server
