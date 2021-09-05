import sys
sys.path.append('..')

import unittest
from Application.NetworkMapperApp import NetworkMapperApp
from Application.NMapObj import NMapObj, Record, PortStatus
from datetime import datetime
import requests
import json

BASE = "http://127.0.0.1:5000/"

class TestEndToEnd(unittest.TestCase):

    def test_invalid_ip_address(self):
        host = "1234"
        response = requests.get(BASE + "openPorts/" + host)
        self.assertEqual(response.json()["Message"],"Invalid IP address for IP: 1234. Please Renter a valid IP Address")

    def test_invalid_ip_address_nmap_scan(self):
        host = "192.168.1.22"
        response = requests.get(BASE + "openPorts/" + host)
        self.assertEqual(response.json()["Message"],"NMap Scan resulted in no results for IP address 192.168.1.22. Please renter a valid IP Address")
    
    def test_valid_ip_address(self):
        host = "192.168.1.1"
        response = requests.get(BASE + "openPorts/" + host)
        self.assertGreater(len(response.text),1000)

if __name__ == '__main__':
    unittest.main()


################
