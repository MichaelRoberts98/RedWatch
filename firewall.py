# Christopher Fischer
# 5/31/2020
# Last Edit: 5/31/2020 9:30 AM
# snake case naming used for convention
# Python 3


import os
import package
import socket


# TODO: Migrate this to core.py
# TODO: Look into if we should be returning IP opjects instead of strings with IPs
# TODO: Test if we're getting IPv6. Test with multiple stuff.
def get_IP():
    # Credit:
    # Stackoverflow - 8529181 & 3503879/
    ip_addresses = os.popen("hostname -I").read()
    if (" " in ip_addresses):
        # Split by stuff
        return ip_addresses.split()
    else:
        # Return a list of the singular IP Address
        return [ip_addresses]

class firewall:
    def __init__(self, OSType):
        # This works for pretty much everything
        self.iptables = {"Ubuntu": 1, "Centos": 1, "FirewallType": 1}
        # TODO: Add support for ufw later
        self.ufw = {"Ubuntu": 1, "Centos": 1, "FirewallType": 2}
        self.firewallList = [self.iptables, self.ufw]
        self.OSType = OSType
        self.firewallUsed = None
        for i in self.firewallList:
            if(self.firewallList[i][OSType] == 1):
                self.firewallUsed = self.firewallList[i]

        # TCP Test
        def __ip_test(self, ip):
            results = []
            for port in range(0, 65534):
                test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = test.connect_ex((ip, port))
                results.append(1) if result == 1 else results.append(0)

        # UDP Test
        def __ip_test_udp(self, ip):
            # Unfortunately, the implementation of UDP for Linux doesn't allow this.
            return -1

    def __socket_test(self):
        # Idea: Look for open ports by spraying
        results = {}
        ip_addresses = get_IP()
        for ip in ip_addresses:
            # Spray ports
            ports = self.__ip_test(self, ip)
            results[ip] = ports
        # Returns a dictionary with {ip : listOfPorts} as convention
        return results

    def quickgen_rules(self):
        # Are we root?
        if not package.is_root():
            return -1000
        if self.firewallUsed is None:
            # Can't find suitable candidate
            return -1001
        if self.firewallUsed['FirewallType'] is 1:
            ports = self.__socket_test(self)
            # Let's start with a baseline
            os.system("iptables -F")
            os.system("iptables -X")
            os.system("iptables -P INPUT DROP")
            os.system("iptables -P OUTPUT ALLOW")
            os.system("iptables -P FORWARD DROP")
            for ip in ports:
                for i in range(0,65534):
                    if ports[i] is 1:
                        os.system("iptables -A INPUT -p tcp --dport "+i+" -s "+ip+ " -j ACCEPT")
            return





