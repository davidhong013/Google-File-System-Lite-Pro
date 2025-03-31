class Config(object):
    # left to be changed
    chunk_size = 3
    master_loc = "35.95.188.241:50051"
    chunkserver_locs = [
        "35.95.188.241:50052",
        "35.95.188.241:50053",
        "35.95.188.241:50054",
    ]
    chunkserver_root = "root_chunkserver"
    default_chunk_size = 1 * 1024 * 1024  # 2megabytes
    message_options = [
        ("grpc.max_receive_message_length", 100 * 1024 * 1024),  # 100MB limit
        ("grpc.max_send_message_length", 100 * 1024 * 1024),  # 100MB limit
    ]


class Status(object):
    def __init__(self, v, e):
        self.v = v
        self.e = e
        if self.e:
            print(self.e)
