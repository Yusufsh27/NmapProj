from nmap.nmap import PortScanner
import re
import ipaddress

class InputValidation():

    def __init__(self):
        self.portScanner = PortScanner()

    def validateIpAddress(self,host):
        try:
            ipaddress.ip_address(host)
        except:
            raise Exception("Invalid IP address for IP: " + host)

    def validateScanOfIpAddress(self,scanedPort,host):
        try:
            scanedPort[host]
        except:
            raise Exception("No Scan Results for IP:" + host)