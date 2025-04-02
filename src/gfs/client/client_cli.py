from typing import Iterator, Optional
from .client import GFSClient

import argparse


class GFSClientCli(GFSClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, argv: Optional[list[str]] = None) -> None:
        argparser: argparse.ArgumentParser = argparse.ArgumentParser(
            description="GFS Client CLI"
        )
        subparsers: Iterator[argparse.ArgumentParser] = argparser.add_subparsers(
            dest="command"
        )

        parser_create = subparsers.add_parser("exit", help="Exit the GFS client.")
        parser_create = subparsers.add_parser("list", help="List files in GFS.")
        parser_create.add_argument(
            "path", type=str, help="The path of the file to list."
        )
        parser_create = subparsers.add_parser("create", help="Create a file in GFS.")
        parser_create.add_argument(
            "filename", type=str, help="The name of the file to create."
        )
        parser_create = subparsers.add_parser("write", help="Write a file from GFS.")
        parser_create.add_argument(
            "filename", type=str, help="The name of the file to write."
        )
        parser_create.add_argument(
            "content", type=str, help="The content of the file to write."
        )
        parser_create = subparsers.add_parser("read", help="Read a file from GFS.")
        parser_create.add_argument(
            "filename", type=str, help="The name of the file to read."
        )
        args: argparse.Namespace = argparser.parse_args(argv)
        if args.command == "exit":
            print("Exiting GFS client.")
        elif args.command == "list":
            self.list_files(args.path)
        elif args.command == "create":
            self.create_file(args.filename)
        elif args.command == "write":
            self.write_to_file(args.filename, args.content)
        elif args.command == "read":
            content: str = self.read_from_file(args.filename)
            print(content)
        else:
            argparser.print_help()


def main():
    client = GFSClientCli()
    client.run()
