# Google-File-System-Lite-Pro

## Setup

We recommend you use python virtual environment when developing this project. You can run this command to start a virtual environment
```bash
python3 -m venv .venv --prompt gfs
```
then run
```bash
source .venv/bin/activate
```
to enable the virtual environment. You can protect your local environment from corruption during development.

## Build and Install

Run
```bash
python3 setup.py install
```
to build necessary proto files and install this package into your python environment. If you want to develop this project instead of using it, our recommendation is to use
```bash
python3 setup.py develop
```
so your update in the source code could be synchronized automatically.

## Executable

We provide three executables currently. They're installed after you finished the above step. You can invoke them with the following command in your bash.
Note that for starting a chunk server, it requires two arguments, followed by an ip address and a port number. For starting a master server, it requires 3 arguments: dynamic or undynamic(to enable dynamic allocation), how much portion of data you want to dynamically allocate (up to 0.5), and how often you want to perform dynamic allocation(in seconds)
```bash
GFS_CONFIG_PATH=pwd (for environment variable)
gfs-master [dynamic or static] [digit from 0 to 0.49] [seconds]
gfs-chunk [ipaddress] [port number]
gfs-client
gfs-client-cli [command] [args]
```

## Notifications
This is a toy distributed file system that supports dynamic allocation based on users visits frequencies on files. Note that it does not provide any fault tolerance or back up mechanism. If a server is down, the data will be gone forever and requires restart of the entire system. Further implementations on fault tolerance will be needed if such distributed file system wants to be put into production.

## Benchmarks
We currently support four benchmarks, read heavy tasks, write heavy tasks, repetitve read on a single file, and random read and write.

## Configurations
Once configuration file is ready and env.sh is sourced, you can start your services:
```commandline
source env.sh
```
To check if you are on the right environment or path:
```commandline
python check_env.py
```

## Format Your Code

To make our directory clean, please check your commit before pushing them to the remote repo to make sure there are no side-effect artifacts like *.pyc, .DS_Store and some other products. And remember run
```bash
find benchmarks src -name "*.py" | xargs black setup.py *.py
```
to format your code so its style looks good.


