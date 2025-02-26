from datetime import datetime, time, timedelta
from typing import List

class ClientLease:
    def __init__(self, lease_assign_time: time, primary_chunk: str, secondary_chunks: List[str]):
        self.lease_assign_time = lease_assign_time  # Time when lease was assigned
        self.primary_chunk = primary_chunk
        self.secondary_chunks = secondary_chunks

    def check_if_expired(self) -> bool:
        """Returns True if lease has expired (more than 60 seconds passed), else False."""
        now = datetime.now().time()  # Current time
        lease_datetime = datetime.combine(datetime.today(), self.lease_assign_time)
        now_datetime = datetime.combine(datetime.today(), now)

        # Calculate time difference
        time_difference = now_datetime - lease_datetime

        return time_difference.total_seconds() > 60

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
