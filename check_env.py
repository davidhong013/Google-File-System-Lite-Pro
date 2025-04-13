# check_env.py
import os
import sys
import gfs.common

print("✅ GFS 环境检查")
print("🔍 Python interpreter:", sys.executable)
print("🔍 GFS_CONFIG_PATH:", os.getenv("GFS_CONFIG_PATH"))
print("🔍 gfs.common loaded from:", gfs.common.__file__)
print("🔍 Python version:", sys.version)