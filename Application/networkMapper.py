from nmap.nmap import PortScanner
from datetime import datetime
from Repository.networkMapperRepoistory import NetworkMapperRepository
from Application.nmapObj import nmapObj
from Application.Validation.InputValidation import InputValidation

class NetworkMapperApp():

    def __init__(self):
        self.portScanner = PortScanner()
        self.networkMapperRepo = NetworkMapperRepository()
        self.inputValidation = InputValidation()

    def findOpenPorts(self,host):

        self.inputValidation.validateIpAddress(host)

        #Scan ports 1-1000 for current Host
        self.portScanner.scan(host, '1-100')

        self.inputValidation.validateScanOfIpAddress(self.portScanner,host)

        listOfOpenPortObjs = []
        dateTimeChecked = datetime.now()

        #Loop through each scanned port and build list of those that are open
        for protocols in self.portScanner[host].all_protocols():
            lport = self.portScanner[host][protocols].keys()
            for port in lport:
                if(self.portScanner[host][protocols][port]['state'] == 'open'):
                    listOfOpenPortObjs.append(nmapObj(host,port,True,dateTimeChecked))


        # if(len(listOfOpenPortObjs) == 0):
            

        #Get History for Port
        portHistory = self.networkMapperRepo.getPortHistory(host)

        #Inserting into Database        
        self.networkMapperRepo.postPortResults(listOfOpenPortObjs)

        #build return Json Object
        returnObj = {}
        returnObj['Current'] = self.toJsonObj(listOfOpenPortObjs,host)
        returnObj['History'] = self.toJsonObj(portHistory,host)

        return returnObj
    
    def toJsonObj(self,listOfOpenPortObjs,host):
        data = {}
        data['Ip'] = host#listOfOpenPortObjs[0].ip
        data['Records'] = []

        dateHashLookUp = {}

        for openPortObj in listOfOpenPortObjs:
            date = openPortObj.date.strftime("%m/%d/%Y, %H:%M:%S")
            if(date not in dateHashLookUp):
                data['Records'].append({'Date' : date})
                dateHashLookUp[date] = len(data['Records'])-1
                
            if("Ports" not in data['Records'][dateHashLookUp[date]]):
                data['Records'][dateHashLookUp[date]]["Ports"] = []
            
            data['Records'][dateHashLookUp[date]]["Ports"].append({openPortObj.port:openPortObj.status})
            
        return data