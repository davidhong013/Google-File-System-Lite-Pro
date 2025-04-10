import concurrent.futures
import os
import sys
import random
import argparse
from typing import Tuple, List

from bench_http_client import GFSBenchHttpClient
from bench import GFSBench

dir: str = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir, "..")))

#adapter
class GFSBenchHttp(GFSBench):
    def __init__(self, master_url: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._client_cli = GFSBenchHttpClient(master_url)

class ShakespearBenchHttp(GFSBenchHttp):
    def __init__(self, master_url: str, *args, **kwargs):
        super().__init__(master_url, *args, **kwargs)
        self._remeo_and_juliet = "https://www.gutenberg.org/cache/epub/1513/pg1513.txt"
        self._shakespeare_complete_work = "https://www.gutenberg.org/cache/epub/100/pg100.txt"
        self._hamlet = "https://www.gutenberg.org/cache/epub/27761/pg27761.txt"

    def impl(self, args: Tuple[str, str]):
        filename, content = args
        filepath = f"/{filename}"
        self._client_cli.run(["create", filepath])
        self._client_cli.run(["write", filepath, content])
        self._client_cli.run(["read", filepath])

    def run(self):
        inputs: List[Tuple[str, str]] = [
            (f"{name}_{counter}.txt", content)
            for name, content in [
                ("Romeo and Juliet", self.cache_get(self._remeo_and_juliet)),
                ("Complete Works", self.cache_get(self._shakespeare_complete_work)),
                ("Hamlet", self.cache_get(self._hamlet)),
            ]
            for counter in range(16)
        ]
        random.shuffle(inputs)
        with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
            for _ in executor.map(self.impl, inputs):
                pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GFS HTTP Benchmark")
    parser.add_argument("--master", type=str, required=True,
                        help="Master node URL, e.g., http://<ip>:5000")
    args = parser.parse_args()
    bench = ShakespearBenchHttp(master_url=args.master)
    bench.run()