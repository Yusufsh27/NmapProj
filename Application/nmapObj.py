class NmapObj():
    def __init__(self, ip):
        self.ip = ip
        self.records = []
    
    def appendRecord(self, record):
        self.records.append(record)
    def getNumOfRecords(self):
        return len(self.records)

class Record():
    def __init__(self, date):
        self.date = date
        self.ports = []
    
    def appendPort(self, port):
        self.ports.append(port)

class PortStatus():
    def __init__(self, portNum, status):
        self.portNum = portNum
        self.status = status



#  "History": {
#         "Ip": "192.168.1.1",
#         "Records": [
#             {
#                 "Date": "09/02/2021, 19:58:39",
#                 "Ports": [
#                     {
#                         "53": true
#                     },
#                     {
#                         "80": true
#                     }
#                 ]
#             }
#         ]
#  }