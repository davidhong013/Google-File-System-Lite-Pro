from master_servicer import MasterServerToClientServicer
import grpc
import gfs_pb2_grpc
import gfs_pb2
from concurrent import futures
def serve():

    # Set up the server with thread pool for handling requests
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    gfs_pb2_grpc.add_MasterServerToClientServicer_to_server(MasterServerToClientServicer(), server)
    server.add_insecure_port('[::]:50051')

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

