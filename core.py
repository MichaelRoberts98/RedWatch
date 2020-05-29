import platform

def init_globals():
    temp_platform_var = platform.linux_distribution()[0]
    if temp_platform_var == "CentOS Linux":
        OsType = Centos
    if temp_platform_var == "Ubuntu":
        OsType = Ubuntu

print OsType