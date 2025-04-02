from bench import GFSBench
from typing import List, Tuple

import concurrent.futures
import contextlib
import io
import os
import random
import sys

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

    def run_impl(self, args: Tuple[str, str]):
        filename, content = args
        filepath: str = f"/{filename}"
        self._client_cli.run(["create", filepath])
        self._client_cli.run(["write", filepath, content])
        with contextlib.redirect_stdout(io.StringIO()):
            self._client_cli.run(["read", filepath])
        # self._client_cli.run(["read", filepath])

    def run(self):
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
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=os.cpu_count() // 4
        ) as executor:
            for _ in executor.map(
                self.run_impl,
                inputs,
            ):
                pass


if __name__ == "__main__":
    bench: ShakespearBench = ShakespearBench()
    bench.run()
