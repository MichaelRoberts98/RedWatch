# Christopher Fischer
# 5/31/2020
# Last Edit: 5/31/2020 8:50 PM
# snake case naming used for convention
# Python 3


import os
import package
import socket


# TODO: Migrate this to core.py
# TODO: Look into if we should be returning IP opjects instead of strings with IPs
# TODO: Test if we're getting IPv6. Test with multiple stuff.
def get_IP_true():
    # Credit:
    # Stackoverflow - 8529181 & 3503879/
    ip_addresses = os.popen("hostname -I").read()
    if (" " in ip_addresses):
        # Split by stuff
        return ip_addresses.split()
    else:
        # Return a list of the singular IP Address
        return [ip_addresses]

def get_IP():
    results = get_IP_true()
    if "127.0.0.1" not in results:
        if "127.0.1.1" not in results:
            results.append("127.0.0.1")
    return results


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
            if(i[OSType] == 1):
                self.firewallUsed = i
                break

        # TCP Test
    def ip_test(self, ip):
            results = []
            for port in range(0, 32768):
                test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = test.connect_ex((ip, port))
                if result is 0:
                    # At some point, we can just use format strings but I'm lazy
                    print("[WARN] Class (firewall) function (ip_test) message:  "+str(ip)+":"+str(port)+" is open!")
                results.append(1) if result == 0 else results.append(0)
            return results

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
            ports = self.ip_test(ip)
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
            # Let's start with a baseline
            print("[INFO] Class (firewall) function (ip_test) message: Saving current IPTables rules to /etc/oldrules.ip")
            os.system("iptables-save > /etc/oldrules.ip")
            os.system("iptables -P INPUT ACCEPT")
            os.system("iptables -F")
            os.system("iptables -X")
            # Changed to accept for unit testing
            os.system("iptables -P OUTPUT ACCEPT")
            os.system("iptables -P FORWARD DROP")
            ports = self.__socket_test()
            os.system("iptables -P INPUT DROP")
            for ip in ports:
                for i in range(0,32767):
                    if ports[ip][i] is 1:
                        os.system("iptables -A INPUT -p tcp --dport "+str(i)+" -d "+str(ip)+ " -j ACCEPT")
