# Christopher Fischer
# 6/1/2020
# Last Edit: 6/2/2020 12:40 AM
# snake case naming used for convention
# Python 3

import pwd

# /etc/passwd files follow this format
# username:passwd:UID:GID:Extra User Info:Home directory:shell type
# Owned by root, otherwise 0644. Make sure not a link of any type
# Store MD5

def grabpasswd():
    users = []
    passwd = open("/etc/passwd", "r")
    info = passwd.readlines()
    for line in info:
        userdata = line.split(":")
        users.append(user(int(userdata[2])))

# /etc/group files follow this format
# groupname:password:groupID:usernamelist(delimited by ,)
# Owned by root, otherwise 0644. Make sure not a link of any type
# Store MD5

# /etc/ssh/sshd_config
# Get SSH key paths and query

class user:
    user = ""
    passwd = ""
    UID = ""
    GID = ""
    dir = ""
    extra = ""
    shell = ""

    def __init__(self, uid):
        struct = pwd.getpwuid(uid)
        UID = uid
        user = struct[0]
        passwd = struct[1]
        GID = struct[3]
        dir = struct[4]
        extra = struct[5]
        shell = struct[6]
        return
