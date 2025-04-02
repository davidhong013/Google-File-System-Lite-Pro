from io import TextIOWrapper
from typing import Dict, Any, List, Optional, Tuple

import json
import os

config_path: Optional[str] = os.getenv("GFS_CONFIG_PATH", None)


class ConfigImpl(object):
    def __init__(
        self,
        chunk_size: int = 3,
        master_loc: str = "localhost:50051",
        chunkserver_locs: List[str] = [
            "localhost:50052",
            "localhost:50053",
            "localhost:50054",
        ],
        chunkserver_root: str = "root_chunkserver",
        default_chunk_size: int = 1 * 1024 * 1024,
        message_options: List[Tuple[str, int]] = [
            ("grpc.max_receive_message_length", 100 * 1024 * 1024),  # 100MB limit
            ("grpc.max_send_message_length", 100 * 1024 * 1024),  # 100MB limit
        ],
        *args,
        **kwargs
    ) -> "ConfigImpl":
        super(ConfigImpl, self).__init__(*args, **kwargs)
        self.chunk_size: int = chunk_size
        self.master_loc: str = master_loc
        self.chunkserver_locs: List[str] = chunkserver_locs
        self.chunkserver_root: str = chunkserver_root
        self.default_chunk_size: int = default_chunk_size
        self.message_options: List[Tuple[str, int]] = message_options

    @staticmethod
    def load(f: TextIOWrapper) -> "ConfigImpl":
        config_json: Dict[str, Any] = json.load(f)
        return ConfigImpl(**config_json)


if config_path:
    with open(config_path, "r") as f:
        Config: ConfigImpl = ConfigImpl.load(f)
else:
    Config: ConfigImpl = ConfigImpl()


class Status(object):
    def __init__(self, v, e):
        self.v = v
        self.e = e
        if self.e:
            print(self.e)
