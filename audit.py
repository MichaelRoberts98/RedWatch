# Christopher Fischer
# 6/1/2020
# Last Edit: 6/2/2020 7:20 PM
# Python 3

import grp
import pwd
from threathunter import genMD5

# /etc/passwd files follow this format
# username:passwd:UID:GID:Extra User Info:Home directory:shell type
# Owned by root, otherwise 0644. Make sure not a link of any type
# Store MD5
def grabpasswd():
    users = []
    passwd_file_acc = open("/etc/passwd", "r")
    info = passwd_file_acc.readlines()
    for line in info:
        userdata = line.split(":")
        users.append(user(int(userdata[2])))
    passwd_file_acc.close()
    local_MD5 = genMD5("/etc/password")
    return passwd_file(users, local_MD5)

# /etc/group files follow this format
# groupname:password:groupID:usernamelist(delimited by ,)
# Owned by root, otherwise 0644. Make sure not a link of any type
# Store MD5
def grabgroup():
    groups = []
    group_file_acc = open("/etc/group", "r")
    info = group_file_acc.readlines()
    for line in info:
        userdata = line.split(":")
        groups.append(groups(int(userdata[2])))
    group_file_acc.close()
    local_MD5 = genMD5("/etc/group")
    return group_file(groups, local_MD5)


# /etc/ssh/sshd_config
# Get SSH key paths and query


class passwd_file:
    users = []
    MD5 = ""
    def __init__(self, users, MD5):
        self.users = users
        self.MD5 = MD5


class group_file:
    group_list = []
    MD5 = ""

    def __init__(self, group, MD5):
        self.group_list = group
        self.MD5 = MD5

class groups:
    def __init__(self, gid):
        group_struct = grp.getgrgid(gid)
        self.group_name = group_struct[0]
        self.group_password = group_struct[1]
        self.group_gid = gid
        self.group_mem = group_struct[3]

class user:
    def __init__(self, uid):
        struct = pwd.getpwuid(uid)
        self.UserID = uid
        self.username = struct[0]
        self.password = struct[1]
        self.GroupID = struct[3]
        self.HomeDir = struct[4]
        self.ExtraInfo = struct[5]
        self.ShellPath = struct[6]
        return
