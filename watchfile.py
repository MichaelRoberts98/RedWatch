import os
import pwd
import grp

class WatchFile:
    def __init__(self, filepath):
        # Location of the file
        self.filepath = filepath

        # TODO: Extract file name from filepath

        st_mode = os.stat(filepath).st_mode

        # Permission in unix form
        # Example:
        # unix_perms = 644
        self.unix_perms = oct(st_mode)[-3:]

        # Possible speedup by implementing dec to oct
        # Permission variables seperated
        # Example:
        # owner_perm = 6
        # group_perm = 4
        # other_perm = 4
        self.owner_perm = self.unix_perms[0]
        self.group_perm = self.unix_perms[1]
        self.other_perm = self.unix_perms[2]
        
        # Group variables
        # Example:
        # groupGID = 42
        # group = "shadow"
        self.groupGID = os.stat(filepath).st_gid
        self.group = grp.getgrgid(self.groupGID).gr_name
        
        # Owner variables
        # Example:
        # ownerUID = 0
        # owner = "root"
        self.ownerUID = os.stat(filepath).st_uid
        self.owner = pwd.getpwuid(self.ownerUID).pw_name

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)