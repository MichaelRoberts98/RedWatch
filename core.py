import vars
import platform

def init_globals():
    temp_platform_var = platform.linux_distribution()[0]
    if temp_platform_var == "CentOS Linux"
        g_OsType = Centos
    if temp_platform_var == "Ubuntu"
        g_OsType = Ubuntu

print g_OsType