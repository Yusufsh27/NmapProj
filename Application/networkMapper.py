from nmap.nmap import PortScanner
from datetime import datetime
from Repository.networkMapperRepoistory import NetworkMapperRepository
from Application.nmapObj import NmapObj, Record, PortStatus
from Application.Validation.InputValidation import InputValidation

class NetworkMapperApp():

    def __init__(self):
        self.portScanner = PortScanner()
        self.networkMapperRepo = NetworkMapperRepository()
        self.inputValidation = InputValidation()

    def findOpenPorts(self,host):
        try:
            self.inputValidation.validateIpAddress(host)

            #Scan ports 1-1000 for current Host
            self.portScanner.scan(host, '1-100')

            self.inputValidation.validateScanOfIpAddress(self.portScanner,host)

            OpenPortObj = NmapObj(host)
            OpenPortObj.appendRecord(Record(datetime.now()))

            #Loop through each scanned port and build list of those that are open
            for protocols in self.portScanner[host].all_protocols():
                lport = self.portScanner[host][protocols].keys()
                for port in lport:
                    if(self.portScanner[host][protocols][port]['state'] == 'open'):
                        portStatus = PortStatus(port,True)
                        OpenPortObj.records[0].appendPort(portStatus)

            #Get History for Port
            portHistory = self.networkMapperRepo.getPortHistory(host)

            #Compare Current value vs Last Value

            difference = self.compare(OpenPortObj.records[0].ports, portHistory.records[0].ports)

            # #Inserting into Database        
            # self.networkMapperRepo.postPortResults(listOfOpenPortObjs)


            # build return Json Object
            returnObj = {}
            returnObj['Current'] = self.toJsonObj(OpenPortObj)
            returnObj['History'] = self.toJsonObj(portHistory)
            returnObj['Difference'] = difference



            return returnObj

        except Exception as e:
            raise e
    

    def compare(self,currentPortVals, lastPortVals):
        current = {}
        for portVal in currentPortVals:
            current[portVal.portNum] = portVal.status

        last = {}
        for portVal in lastPortVals:
            last[portVal.portNum] = portVal.status
        
        diff = []
        for key in current.keys():
            tmp = {}
            if(key not in last):
                tmp["Port"] = key
                tmp["Current"] = True
                tmp["Last"] = False
                diff.append(tmp)

        for key in last.keys():
            tmp = {}
            if(key not in current):
                tmp["Port"] = key
                tmp["Current"] = False
                tmp["Last"] = True
                diff.append(tmp)
        
        return diff

    def toJsonObj(self,OpenPortObj):
        data = {}
        data['Ip'] = OpenPortObj.ip
        data['Records'] = []

        for record in OpenPortObj.records:
            date = record.date.strftime("%m/%d/%Y, %H:%M:%S")
            data['Records'].append({'Date' : date})
            data['Records'][len(data['Records'])-1]["Ports"] = []
            for port in record.ports:
                    data['Records'][len(data['Records'])-1]["Ports"].append({port.portNum:port.status})
            
        return data