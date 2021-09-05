import sys
sys.path.append('..')

import unittest
from Application.NetworkMapperApp import NetworkMapperApp
from Application.NMapObj import NMapObj, Record, PortStatus
from datetime import datetime

class TestHelperMethods(unittest.TestCase):

    def test_diffence_function_has_diff(self):
        currTest = []
        portStatus1 = PortStatus(1,True)
        portStatus2 = PortStatus(3,True)
        portStatus3 = PortStatus(5,True)
        currTest.append(portStatus1)
        currTest.append(portStatus2)
        currTest.append(portStatus3)

        lastTest = []
        portStatus4 = PortStatus(3,True)
        portStatus5 = PortStatus(6,True)
        portStatus6 = PortStatus(10,True)
        lastTest.append(portStatus4)
        lastTest.append(portStatus5)
        lastTest.append(portStatus6)

        networkMapperApp = NetworkMapperApp
        difference = networkMapperApp.compare(self,currTest, lastTest)

        self.assertEqual(4, len(difference))
        self.assertTrue(any(x["Port"] == 1 for x in difference))
        self.assertTrue(any(x["Port"] == 6 for x in difference))
        self.assertTrue(any(x["Port"] == 5 for x in difference))
        self.assertTrue(any(x["Port"] == 10 for x in difference))

        self.assertTrue(any(x["Port"] == 1 and x["Current"] == "Open" and x["Last"] == "Closed" for x in difference))
        self.assertTrue(any(x["Port"] == 6 and x["Current"] == "Closed" and x["Last"] == "Open" for x in difference))

    def test_diffence_function_has_no_diff(self):
        currTest = []
        portStatus1 = PortStatus(1,True)
        portStatus2 = PortStatus(3,True)
        portStatus3 = PortStatus(5,True)
        currTest.append(portStatus1)
        currTest.append(portStatus2)
        currTest.append(portStatus3)

        lastTest = []
        portStatus4 = PortStatus(1,True)
        portStatus5 = PortStatus(3,True)
        portStatus6 = PortStatus(5,True)
        lastTest.append(portStatus4)
        lastTest.append(portStatus5)
        lastTest.append(portStatus6)
        test = NetworkMapperApp

        difference = test.compare(self,currTest, lastTest)

        self.assertEqual(0, len(difference))

    def test_toJsonObj_function(self):
        ##Create
        openPortObj = NMapObj("192.168.1.1")
        openPortObj.appendRecord(Record(datetime.now()))
        port1 = PortStatus(1,True)
        port2 = PortStatus(2,True)
        openPortObj.records[0].appendPort(port1)
        openPortObj.records[0].appendPort(port2)
        openPortObj.appendRecord(Record(datetime.now()))
        port3 = PortStatus(2,True)
        port4 = PortStatus(3,True)
        openPortObj.records[1].appendPort(port3)
        openPortObj.records[1].appendPort(port4)

        networkMapperApp = NetworkMapperApp
        jsonObj = networkMapperApp.toJsonObj(self,openPortObj)
        
        self.assertEqual(len(jsonObj['Records']), len(openPortObj.records))
        self.assertEqual(len(jsonObj['Records'][0]['Ports']), len(openPortObj.records[0].ports))
        self.assertEqual(jsonObj['Records'][0]['Ports'][0][1], openPortObj.records[0].ports[0].status)

if __name__ == '__main__':
    unittest.main()