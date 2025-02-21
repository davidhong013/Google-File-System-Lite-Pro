import setuptools

setuptools.setup(
    name="Google-File-System-Lite-Pro",
    author=[
        {"name": "Tinhang Hong", "email": "tinhangh@usc.edu"},
        {"name": "Letitia Wang", "email": "swang311@usc.edu"},
        {"name": "Jinjie Liu", "email": "jinjie.liu@usc.edu"},
    ],
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "grpcio",
        "grpcio-tools",
    ],
    entry_points={
        "console_scripts": [
            "gfs-master=gfs.master_server.master_main:serve",
            "gfs-client=gfs.client.client:main",
        ]
    },
)
