# Christopher Fischer
# 5/31/2020
# Last Edit: 6/1/2020 2:00 AM
# snake case naming used for convention
# Python 3


import os
from time import sleep

import psutil
import requests

# What defines mission accomplishment
# run psutil.net_connections(), get a list of PIDS
# grab pids binary by querying proc (os.readlink)
# remove duplicates
# md5hash everything
# push to VT
# push unknown binaries back to VT for scan

# Use virustotal.com's API.
apikey = ""

class threathunterpassive:
    # Once something has been sent off to VT and confirmed to be OK, we can just add it here. :)
    whiteListedMD5 = []
    requestedScan = []
    blackListedMD5 = []
    md5dict = {}


    def __init__(self):
        # Awake
        t = 1

    # TODO: Add a hueristic element to this, sorting by lowest memory count
    def getPIDSlist(self):
        # This gets a list of sockets. That's BRUTAL
        socket_list = psutil.net_connections()
        # TODO: Find out if the PID is always in #6 in the socket.
        PID_list = []
        for socket in socket_list:
            PID_list.append(socket[6])
        # Returning as a set allows us only distinct PIDs
        return set(PID_list)

    def getBins(self, PIDS):
        # Do things
        BIN_list = []
        for entry in PIDS:
            try:
                BIN_list.append(os.readlink("/proc/"+str(entry)+"/exe"))
            except FileNotFoundError:
                print("[WARN] Class (threathunter) function (getBins) message: FileNotFoundError handled")
                continue
        return set(BIN_list)

    def whiteList(self, MD5):
        print("Found a binary to whitelist!")
        self.whiteListedMD5.append(MD5)

    def requestScan(self, MD5):
        print("Requesting Scan "+MD5)
        self.requestedScan.append(MD5)

    def genMD5(self, path):
        MD5 = os.popen("md5sum " + str(path)).read()
        return (MD5.split(" ")[0])

    def genMD5s(self, BINS):
        # Now how friggen cool is this?
        # Why work harder, we can work smarter.
        hash_dict = {}
        hash_list = []
        for file in BINS:
            MD5 = os.popen("md5sum "+str(file)).read()
            hash_dict[file] = (MD5.split(" ")[0])
            hash_list.append(MD5.split(" ")[0])
        return [hash_list, hash_dict]

    # TODO: Implement this
    def uploadBigFile(self, file):
        print("[WARN] Class (threathunter) function (uploadBigFile) message: Big Files are Unsupported!")
        return

    def maliciousBinToKill(self, BIN):
        PIDS = self.getPIDSlist()
        for entry in PIDS:
            try:
                path = (os.readlink("/proc/" + str(entry) + "/exe"))
                if path in BIN:
                    self.killPID(entry)
                    print("[WARN] Class (threathunter) function (maliciousBinToKill) message: Killed PID "+str(entry)+" due to relation with "+str(BIN))
            except FileNotFoundError:
                print("[WARN] Class (threathunter) function (getBins) message: FileNotFoundError handled")
                continue

    def killPID(self, PID):
        os.popen("kill -9 " + str(PID))

    def uploadFile(self, file):
        # Check to see if file is above 32 MB
        try:
            size = os.path.getsize(file)
            if(size > 33554432):
                self.uploadBigFile(file)
                return
            if(size < 33554432):
                # Credit: VT API Docs
                url = 'https://www.virustotal.com/vtapi/v2/file/scan'
                params = {'apikey': apikey}
                files = {'file': (file, open(file, 'rb'))}
                response = requests.post(url, files=files, params=params)

        except FileNotFoundError:
            print(file)
            print("[WARN] Class (threathunter) function (uploadFile) message: FileNotFoundError handled")
            pass

    def handleMaliciousFile(self, MD5):
        os.popen("wall Malicious File! " + MD5)
        self.maliciousBinToKill(self.md5dict[MD5])
        os.popen("wall Bad File should be dead....")
        if MD5 not in self.blackListedMD5:
            self.blackListedMD5.append(MD5)

    # Credit: VT Documentation
    def sendVTRequest(self, MD5):
        url = 'https://www.virustotal.com/vtapi/v2/file/report'
        params = {'apikey': apikey, 'resource': MD5}
        response = requests.get(url, params=params)
        processed_json = response.json()
        print(processed_json)
        if(processed_json['response_code'] == 1 and processed_json['positives'] == 0):
            self.whiteList(MD5)
        if(processed_json['response_code'] == 1 and processed_json['positives'] != 0):
            self.handleMaliciousFile(MD5)
        if(processed_json['response_code'] == 0):
            self.requestScan(MD5)
        # If it's neither found or not found, then we know it's scanning. In this case, We'll just wait.

    # Wrapper
    def pushToVT(self, MD5s):
        for MD5 in MD5s:
            print("Path - " + str(self.md5dict[MD5]))
            print("Send request for "+str(MD5))
            if MD5 in self.blackListedMD5:
                self.handleMaliciousFile(MD5)
                continue
            elif MD5 in self.whiteListedMD5:
                print("Whitelisted. Bypassing...")
                continue
            elif MD5 in self.requestedScan:
                print("Requested Scan. Bypassing...")
                self.uploadFile(self.md5dict[MD5])
                self.requestedScan.remove(MD5)
            else:
                self.sendVTRequest(MD5)
            sleep(20)
        return

    def threathunt(self):
        while(True):
            PIDS = self.getPIDSlist()
            BINS = self.getBins(PIDS)
            print("Paths to binaries with currently open network connections:")
            print(BINS)
            hashs = self.genMD5s(BINS)
            md5dict = hashs[1]
            self.md5dict = {v: k for k, v in md5dict.items()}
            print(str(hashs[1]))
            self.pushToVT(hashs[0])
