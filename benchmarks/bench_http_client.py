#Adapter, based on bench.py, converting the create/write/read to http request

import requests

class GFSBenchHttpClient:
    def __init__(self, master_url: str):
        self.master_url = master_url

    def run(self, args):
        cmd = args[0]
        path = args[1].lstrip("/")
        if cmd == "create":
            r = requests.post(f"{self.master_url}/create", json={"filename": path})
            self._last_chunk_info = r.json()
        elif cmd == "write":
            content = args[2]
            chunk_id = self._last_chunk_info["chunk_id"]
            for server in self._last_chunk_info["chunk_servers"]:
                requests.post(f"{server}/write", json={"chunk_id": chunk_id, "content": content})
        elif cmd == "read":
            r = requests.get(f"{self.master_url}/read", params={"filename":path})
            chunks = r.json()
            result = ""
            for chunk in chunks:
                for server in chunk["servers"]:
                    try:
                        response = requests.get(f"{server}/read_chunk", params={"chunk_id": chunk["chunk_id"]})
                        result += response.json()["content"]
                        break
                    except:
                        continue
            return result
        else:
            raise ValueError(f"Unsupported command: {cmd}")