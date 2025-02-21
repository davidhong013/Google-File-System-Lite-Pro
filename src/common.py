class Config(object):
    # left to be changed
    chunk_size = 5
    master_loc = "104.248.169.227:50051"
    chunkserver_locs = ["50052", "50053", "50054", "50055", "50056"]
    chunkserver_root = "root_chunkserver"
    default_chunk_size = 10  # megabytes


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
