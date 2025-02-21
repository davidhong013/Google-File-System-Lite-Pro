import os
import setuptools
import setuptools.command
import setuptools.command.build_py


class BuildProtoCommand(setuptools.command.build_py.build_py):
    def run(self):
        import grpc_tools.protoc
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
        super().run(self)


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
    cmdclass={"build_py": BuildProtoCommand},
    entry_points={
        "console_scripts": [
            "gfs-master=gfs.master_server.master_main:serve",
            "gfs-client=gfs.client.client:main",
        ]
    },
)
