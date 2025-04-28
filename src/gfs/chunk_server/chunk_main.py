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

    #config-based way
    argparser.add_argument(
        "--index",
        type = int,
        help = "Index of the chunk server from configuration file."
    )

    #manual type-in
    argparser.add_argument(
        "--ip",
        type = str,
        help = "Ip of the chunk server.",
    )
    argparser.add_argument(
        "--port",
        type = str,
        help = "Port of the chunk server.",
    )

    args: argparse.Namespace = argparser.parse_args()
    if args.index is not None:
        try:
            address = cfg.chunkserver_locs[args.index]
            ip, port = address.split(":")
            print(f"[ChunkServer-{args.index}] Loaded from config: {ip}:{port}")
        except (IndexError, ValueError):
            raise RuntimeError(f"Invalid index or malformed address in config: {cfg.chunkserver_locs}")
    elif args.ip and args.port:
        ip = args.ip
        port = args.port
        print(f"[ChunkServer] Using manual IP/port: {ip}:{port}")
    else:
        raise ValueError("Must provide either --index (for config-based start) or both --ip and --port (manual start)")

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
    print(f"Chunk Server started at {ip}:{port}.")

    try:
        # Keep the server running and handle requests
        server.wait_for_termination()  # This is the recommended way to keep the server running
    except KeyboardInterrupt:
        print("Shutting down server.")
        server.stop(0)  # Gracefully stop the server
