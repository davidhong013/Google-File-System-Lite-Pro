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

We provide two executables currently. They're installed after you finished the above step. You can invoke them with the following command in your bash
```bash
gfs-master
gfs-client
```

## Format Your Code

To make our directory clean, please check your commit before pushing them to the remote repo to make sure there are no side-effect artifacts like *.pyc, .DS_Store and some other products. And remember run
```bash
find src -name *.py | xargs black *.py
```
to format your code so its style looks good.
