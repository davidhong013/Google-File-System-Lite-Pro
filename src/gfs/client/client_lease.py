from datetime import datetime, time, timedelta
from typing import List

class ClientLease:
    def __init__(self, lease_assign_time: time, primary_chunk: str, secondary_chunks: List[str],version_number:int):
        self.lease_assign_time = lease_assign_time  # Time when lease was assigned
        self.primary_chunk = primary_chunk
        self.secondary_chunks = secondary_chunks
        self.version_number = version_number

    def check_if_expired(self) -> bool:
        """Returns True if lease has expired (more than 60 seconds passed), else False."""
        now = datetime.now().time()  # Current time
        lease_datetime = datetime.combine(datetime.today(), self.lease_assign_time)
        now_datetime = datetime.combine(datetime.today(), now)

        # Calculate time difference
        time_difference = now_datetime - lease_datetime

        return time_difference.total_seconds() > 60