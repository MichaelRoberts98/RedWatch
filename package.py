# Christopher Fischer
# 5/30/2020
# Last Edit: 5/31/2020 9:18 PM
# snake case naming used for convention
# Python 3

import os

'''
"Ubuntu" - 5/30/2020 6:46 PM (Awaiting Testing)
"Centos" - TODO
Helpful Return Codes:
apt-get:
0 - Returned sucessfully
100 - Failed somehow (not sudo, not found)
130 - Operation Cancelled
'''

# TODO: Look into a safe root only operation instead of using effective id
def is_root():
    return os.geteuid() == 0

class package:
    def __init__(self, OSType):
        self.apt = {"Ubuntu": 1, "Centos": 0, "PackageNumber": 1, 100: "Error Occured", 130: "Operation was cancelled",
               0: "Successful", 25600 : "Not Found"}
        self.yum = {"Ubuntu": 0, "Centos": 1, "PackageNumber": 2}
        self.packageList = [self.apt,self.yum]
        self.OSType = OSType
        self.packageManager = None
        for i in self.packageList:
            if(i[OSType] == 1):
                self.packageManager = i

    def __does_package_exist(self):
        # With apt, this is impossible
        if(self.packageManager["PackageNumber"] == 1):
            # Easier to return True and handle errors later
            return True
        # TODO: Add check for yum!
        return False

    def __update_package(self):
        # Update the package list
        if (self.packageManager["PackageNumber"] == 1):
            return os.system("apt-get update")
        if (self.packageManager["PackageNumber"] == 2):
            # Is this the functionality we want?
            return os.system("yum upgrade")
        return False

    def __install_package(self,packageName):
        # Try to install
        if (self.packageManager["PackageNumber"] == 1):
            return os.system("apt-get -y install " + packageName)
        if (self.packageManager["PackageNumber"] == 2):
            return os.system("yum install " + packageName)
        return False

    def install(self, packageName):
        returnCode = self.__install_package(packageName)
        if (returnCode == 0):
            return True
        return_msg = self.packageManager[returnCode]
        if return_msg != None:
            print("[WARN] Class (package) function (install) message: " + return_msg)
        return False
