import grpc

from concurrent import futures
from .chunk_servicer import ChunkServerToClientServicer
from .. import gfs_pb2, gfs_pb2_grpc

def serve():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    gfs_pb2_grpc.add_ChunkServerToClientServicer_to_server(ChunkServerToClientServicer(),server)

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