import os
import time

import grp
import pwd


# Extracts file information from a file
class file:
    def __init__(self, filepath):
        # Location of the file
        self.filepath = filepath

        # TODO: Extract file name from filepath
        st_mode = os.stat(filepath).st_mode

        self.md5 = os.popen("md5sum " + str(filepath)).read().split(" ")[0]

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

class watch_file():

    # importance: 0-10, 10 being the most importance files
    # 

    def __init__(self, filepath, unix_perms="644", group="", owner="", importance=5):
        self.filepath = filepath
        self.unix_perms = unix_perms

        self.file = file(filepath)

        if not group:
            self.group = self.file.group
        else:
            self.group = group

        if not owner:
            self.owner = self.file.owner
        else:
            self.owner = owner

        self.md5 = self.file.md5

    def monitor_change(self):
        file_currrently = file(self.filepath)
        if (file_currrently.owner != self.owner):
            print('[WARNING]: {0} is owned by {1}, not by {2}'.format(file_currrently.filepath, file_currrently.owner, self.owner))
        if (file_currrently.group != self.group):
            print('[WARNING]: {0} is owned by group {1}, not by group {2}'.format(file_currrently.filepath, file_currrently.group, self.group))
        if (file_currrently.unix_perms != self.unix_perms):
            print('[WARNING]: {0} is has permissions of {1}, not {2}'.format(file_currrently.filepath,
                                                                             file_currrently.unix_perms,
                                                                             self.unix_perms))
        if (file_currrently.md5 != self.md5):
            print('[WARNING]: {0} is has MD5 of {1}, not {2}'.format(file_currrently.filepath, file_currrently.md5,
                                                                     self.md5sum))
            # We're just going to update the MD5 so we don't get spammed
            self.md5 = file_currrently.md5

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
        

class watch_directory():
        
    def add_file(self, filepath):
        self.files.append(watch_file(filepath, unix_perms=self.unix_perms, group=self.group, owner=self.owner))

    def add_files(self, top, callback):
        for f in os.listdir(top):
            pathname = os.path.join(top, f)

            if os.path.isdir(pathname):
                self.add_files(pathname, callback)
            elif os.path.isfile(pathname):
                callback(pathname)
            else:
                print('Unknown filetype, skipping %s' % pathname)
    
    def monitor_directory(self):
        for f in self.files:
            f.monitor_change()

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    def __init__(self, filepath, unix_perms="644", group="", owner=""):
        self.filepath = filepath
        self.files = []
        self.unix_perms = unix_perms
        self.directory = file(filepath)

        if not group:
            self.group = self.directory.group
        else:
            self.group = group

        if not owner:
            self.owner = self.directory.owner
        else:
            self.owner = owner

        self.add_files(filepath, self.add_file)

class monitor():
    def __init__(self, wait_time=10):
        self.wait_time = wait_time
        self.files = []
        self.directories = []

    def start(self):
        self.running = True

        while self.running:
            print("Monitoring files...")

            for f in self.files:
                f.monitor_change()
            for d in self.directories:
                d.monitor_directory()

            time.sleep(self.wait_time)

    def stop(self):
        self.running = False

    def add_directory(self, *args, **kwargs):
        # Error handle the folder
        self.directories.append(watch_directory(*args, **kwargs))

    def add_file(self, *args, **kwargs):
        self.files.append(watch_file(*args, **kwargs))