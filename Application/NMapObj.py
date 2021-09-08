class NMapObj():
    def __init__(self, ip):
        self.ip = ip
        self.ports = {}
            
    def getNumOfPorts(self):
        return len(self.ports)