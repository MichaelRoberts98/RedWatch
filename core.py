import platform
from net import *

OsType = "Linux"

def init_globals():
    global OsType
    temp_platform_var = platform.linux_distribution()[0]
    if temp_platform_var == "CentOS Linux":
        OsType = "Centos"
    if temp_platform_var == "Ubuntu":
        OsType = "Ubuntu"

init_globals()
LocalIp = get_ip()
print OsType
print LocalIp
