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
            raise ValueError('Invalid IP address for IP: ' + host + '. Please Renter a valid IP Address')

    def validateScanOfIpAddress(self,scanedPort,host):
        try:
            scanedPort[host]
        except:
            raise ValueError('NMap Scan resulted in no results for IP address ' + host  + '. Please renter a valid IP Address')