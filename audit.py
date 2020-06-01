# Christopher Fischer
# 6/1/2020
# Last Edit: 6/1/2020 1:40 PM
# snake case naming used for convention
# Python 3


# /etc/passwd files follow this format
# username:passwd:UID:GID:Extra User Info:Home directory:shell type
# Owned by root, otherwise 0644. Make sure not a link of any type
# Store MD5

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
    extra = ""
    shell = ""
