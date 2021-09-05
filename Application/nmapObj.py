class NMapObj():
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