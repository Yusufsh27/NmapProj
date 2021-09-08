import sys
sys.path.append('..')

import unittest
from Application.NetworkMapperApp import NetworkMapperApp
from Application.NMapObj import NMapObj
from datetime import datetime
import requests
import json

BASE = "http://127.0.0.1:5000/"

class TestEndToEnd(unittest.TestCase):

    def test_invalid_ip_address(self):
        host = "1234"
        response = requests.get(BASE + "openPorts/" + host)
        self.assertEqual(response.json()["Message"],"NMap Scan resulted in no results for IP address: (1234) 0.0.4.210. Please re-enter a valid IP Address")

    def test_invalid_ip_address_nmap_scan(self):
        host = "192.168.1.38"
        response = requests.get(BASE + "openPorts/" + host)
        self.assertEqual(response.json()["Message"],"NMap Scan resulted in no results for IP address: (192.168.1.38) 192.168.1.38. Please re-enter a valid IP Address")
    
    def test_valid_ip_address(self):
        host = "192.168.1.1"
        response = requests.get(BASE + "openPorts/" + host)
        self.assertGreater(len(response.text),1000)

    def test_invalid_hostname(self):
        host = "blahblah"
        response = requests.get(BASE + "openPorts/" + host)
        self.assertEqual(response.json()["Message"],"Invalid Hostname: blahblah. Please re-enter a valid Hostname or IP")

    def test_valid_hostname_google(self):
        host = "google.com"
        response = requests.get(BASE + "openPorts/" + host)
        self.assertGreater(len(response.text),200)

    def test_valid_hostname_localhost(self):
        host = "localhost"
        response = requests.get(BASE + "openPorts/" + host)
        self.assertGreater(len(response.text),200)

if __name__ == '__main__':
    unittest.main()


################
