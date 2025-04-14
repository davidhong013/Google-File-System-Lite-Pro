from bench import GFSBench
from typing import List, Tuple

import concurrent.futures
import os
import random
import sys
import argparse
dir: str = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir, "..")))


class ShakespearBench(GFSBench):
    def __init__(self, *args, **kwargs) -> "ShakespearBench":
        super().__init__(*args, **kwargs)
        self._remeo_and_juliet: str = (
            "https://www.gutenberg.org/cache/epub/1513/pg1513.txt"
        )
        self._shakespeare_complete_work: str = (
            "https://www.gutenberg.org/cache/epub/100/pg100.txt"
        )
        self._hamlet: str = "https://www.gutenberg.org/cache/epub/27761/pg27761.txt"

    def random_read_write(self, args: Tuple[str, str]):
        filename, content = args
        print('hi im here')
        filepath: str = f"/{filename}"
        self._client_cli.run(["create", filepath])

        self._client_cli.run(["write", filepath, content])
        self._client_cli.run(["read", filepath])

    def read_heavy(self, args: Tuple[str, str]):
        filename, content = args
        filepath: str = f"/{filename}"
        self._client_cli.run(["create", filepath])
        self._client_cli.run(["write", filepath, content])
        self._client_cli.run(["read", filepath])
        self._client_cli.run(["read", filepath])
        self._client_cli.run(["read", filepath])
        self._client_cli.run(["read", filepath])

    def write_heavy(self, args: Tuple[str, str]):
        filename, content = args
        filepath: str = f"/{filename}"
        self._client_cli.run(["create", filepath])
        self._client_cli.run(["write", filepath, content])
        self._client_cli.run(["read", filepath])
        self._client_cli.run(["write", filepath, content])
        self._client_cli.run(["write", filepath, content])
        self._client_cli.run(["write", filepath, content])
        self._client_cli.run(["write", filepath, content])

    def run(self, task:str):
        inputs: List[Tuple[str, str]] = [
            (f"{name}_{counter}.txt", content)
            for name, content in [
                (
                    "Romeo and Juliet by William Shakespeare",
                    self.cache_get(self._remeo_and_juliet),
                ),
                (
                    "The Complete Works of William Shakespeare by William Shakespeare",
                    self.cache_get(self._shakespeare_complete_work),
                ),
                (
                    "Hamlet, Prince of Denmark by William Shakespeare",
                    self.cache_get(self._hamlet),
                ),
            ]
            for counter in range(16)
        ]
        random.shuffle(inputs)
        if task == "random_read_write":
            with concurrent.futures.ProcessPoolExecutor(
                # max_workers=os.cpu_count()
                max_workers=os.cpu_count()
            ) as executor:
                for _ in executor.map(
                    self.random_read_write,
                    inputs,
                ):
                    pass
        elif task == 'write_heavy':
            with concurrent.futures.ProcessPoolExecutor(
                max_workers=os.cpu_count()
            ) as executor:
                for _ in executor.map(
                    self.write_heavy,
                    inputs,
                ):
                    pass
        elif task == 'read_heavy':
            with concurrent.futures.ProcessPoolExecutor(
                max_workers=os.cpu_count()
            ) as executor:
                for _ in executor.map(
                    self.read_heavy,
                    inputs,
                ):
                    pass
        elif task == 'rep_read':
            rep_inputs: List[Tuple[str, str]] = [
                (f"{name}_{counter}.txt", content)
                for name, content in [
                    (
                        "Romeo and Juliet by William Shakespeare",
                        self.cache_get(self._remeo_and_juliet),
                    )
                ]
                for counter in range(16)
            ]
            with concurrent.futures.ProcessPoolExecutor(
                max_workers=os.cpu_count()
            ) as executor:
                for _ in executor.map(
                    self.read_heavy,
                    rep_inputs,
                ):
                    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GFS Lite Pro Benchmark")
    parser.add_argument(
        "--task",
        type=str,
        default = 'random_read_write',
        help = 'four options available: random_read_write, write_heavy,read_heavy, and rep_read'
    )
    args = parser.parse_args()
    bench: ShakespearBench = ShakespearBench()
    bench.run(task = args.task)
