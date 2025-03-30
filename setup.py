import os
import setuptools
import setuptools.command
import setuptools.command.build_py
import setuptools.command.develop
import setuptools.command.install
import shutil


class BuildProtoCommand(setuptools.command.build_py.build_py):
    def run(self):
        import grpc_tools.protoc

        chunk_storage_dir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "src",
            "gfs",
            "chunk_server",
            "chunk_storage",
        )

        if not os.path.exists(chunk_storage_dir):
            os.makedirs(chunk_storage_dir)  # Create the directory if it doesn't exist
            print(f"Created directory: {chunk_storage_dir}")

        if os.path.exists(chunk_storage_dir) and os.path.isdir(chunk_storage_dir):
            for filename in os.listdir(chunk_storage_dir):
                file_path = os.path.join(chunk_storage_dir, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)  # Remove file
                    elif os.path.isdir(file_path):
                        shutil.rmtree(
                            file_path
                        )  # Remove directory (if any subdirectories exist)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

        root_dir: str = os.path.abspath(os.path.dirname(__file__))
        gfs_dir: str = os.path.join(root_dir, "src", "gfs")
        proto_path: str = os.path.join(gfs_dir, "gfs.proto")
        grpc_tools.protoc.main(
            (
                "",
                f"-I{gfs_dir}",
                f"--python_out={gfs_dir}",
                f"--grpc_python_out={gfs_dir}",
                f"{proto_path}",
            )
        )
        super().run()


class DevelopCommand(setuptools.command.develop.develop):
    def run(self):
        self.run_command("build_py")
        super().run()


class InstallCommand(setuptools.command.install.install):
    def run(self):
        self.run_command("build_py")
        super().run()


setuptools.setup(
    name="Google-File-System-Lite-Pro",
    author=[
        {"name": "Tinhang Hong", "email": "tinhangh@usc.edu"},
        {"name": "Letitia Wang", "email": "swang311@usc.edu"},
        {"name": "Jinjie Liu", "email": "jinjie.liu@usc.edu"},
    ],
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    setup_requires=[
        "grpcio-tools",
    ],
    install_requires=[
        "grpcio",
        "protobuf",
    ],
    cmdclass={
        "build_py": BuildProtoCommand,
        "develop": DevelopCommand,
        "install": InstallCommand,
    },
    entry_points={
        "console_scripts": [
            "gfs-master=gfs.master_server.master_main:serve",
            "gfs-client=gfs.client.client:main",
            "gfs-chunk=gfs.chunk_server.chunk_main:serve",
        ]
    },
)
