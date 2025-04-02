import hashlib
import os
import requests
import tempfile

import gfs.client.client_cli


class GFSBench(object):
    def __init__(self, *args, **kwargs) -> "GFSBench":
        super().__init__(*args, **kwargs)
        self._client_cli: gfs.client.client_cli.GFSClientCli = (
            gfs.client.client_cli.GFSClientCli()
        )

    def cache_get(self, url: str) -> str:
        filename: str = f"{hashlib.md5(url.encode()).hexdigest()}.txt"
        dir: str = tempfile.gettempdir()
        filepath: str = os.path.join(dir, filename)
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                return f.read()
        else:
            response: requests.Response = requests.get(url)
            if response.status_code == 200:
                with open(filepath, "w") as temp_file:
                    temp_file.write(response.text)
                    return response.text
            else:
                raise RuntimeError(
                    f"Failed to download file with status code: {response.status_code}"
                )
