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
            #portHistory = self.networkMapperRepo.getPortHistory(host)

            # #Inserting into Database        
            # self.networkMapperRepo.postPortResults(listOfOpenPortObjs)

            # build return Json Object
            returnObj = {}
            returnObj['Current'] = self.toJsonObj(OpenPortObj)
            # returnObj['History'] = self.toJsonObj(portHistory,host)

            return returnObj

        except Exception as e:
            raise e
    

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

    # def toJsonObj(self,listOfOpenPortObjs,host):
    #     data = {}
    #     data['Ip'] = host#listOfOpenPortObjs[0].ip
    #     data['Records'] = []

    #     dateHashLookUp = {}

    #     for openPortObj in listOfOpenPortObjs:
    #         date = openPortObj.date.strftime("%m/%d/%Y, %H:%M:%S")
    #         if(date not in dateHashLookUp):
    #             data['Records'].append({'Date' : date})
    #             dateHashLookUp[date] = len(data['Records'])-1
                
    #         if("Ports" not in data['Records'][dateHashLookUp[date]]):
    #             data['Records'][dateHashLookUp[date]]["Ports"] = []
            
    #         data['Records'][dateHashLookUp[date]]["Ports"].append({openPortObj.port:openPortObj.status})
            
    #     return data