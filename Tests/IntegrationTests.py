import sys
sys.path.append('..')

import unittest
from Application.NetworkMapperApp import NetworkMapperApp
from Application.NMapObj import NMapObj, Record, PortStatus
from datetime import datetime
import requests

class TestEndToEnd(unittest.TestCase):

    def __init__(self):
        BASE = "http://127.0.0.1:5000/"

    def test_diffence_function_has_diff(self):
        response = requests.get(self.BASE + "")
        print(response.json())

if __name__ == '__main__':
    unittest.main()


################
