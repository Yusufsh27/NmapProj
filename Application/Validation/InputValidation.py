from nmap.nmap import PortScanner
import re
import ipaddress

class InputValidation():

    def __init__(self):
        self.portScanner = PortScanner()

    def validateIpAddress(self,host):
        try:
            ipaddress.ip_address(host)
        except Exception as e:
            raise e

    def validateScanOfIpAddress(self,scanedPort,host):
        try:
            scanedPort[host]
        except Exception as e:
            print("breaking")
            raise e