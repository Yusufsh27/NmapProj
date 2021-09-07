from nmap.nmap import PortScanner
import ipaddress
import socket

class InputValidation():

    def __init__(self):
        self.portScanner = PortScanner()

    def IpAddress(self,host,hostOrg):
        try:
            ipaddress.ip_address(host)
        except:
            raise ValueError('Invalid IP address for IP: (' + hostOrg + ') ' + host + '. Please re-enter a valid IP Address')

    def Hostname(self,host):
        try:
            ipAddress = socket.gethostbyname(host)
            return ipAddress
        except:
            raise ValueError('Invalid Hostname: ' + host + '. Please re-enter a valid Hostname or IP')

    def ScanOfIpAddress(self,scanedPort,host,hostOrg):
        try:
            scanedPort[host]
        except:
            raise ValueError('NMap Scan resulted in no results for IP address: (' + hostOrg + ') ' + host  + '. Please re-enter a valid IP Address')