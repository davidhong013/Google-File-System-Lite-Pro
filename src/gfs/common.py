class Config(object):
    # left to be changed
    chunk_size = 5
    master_loc = "165.232.154.137:50051"
    chunkserver_locs = ["104.248.169.227:50051", "104.248.169.227:50052"]
    chunkserver_root = "root_chunkserver"
    default_chunk_size = 1048576  # 8megabytes


class Status(object):
    def __init__(self, v, e):
        self.v = v
        self.e = e
        if self.e:
            print(self.e)


def isint(e):
    try:
        e = int(e)
    except:
        return False
    else:
        return True
