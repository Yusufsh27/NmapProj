from nmap.nmap import PortScanner
from datetime import datetime
from Repository.networkMapperRepoistory import NetworkMapperRepository
from Application.nmapObj import nmapObj

class NetworkMapperApp():

    def __init__(self):
        self.portScanner = PortScanner()
        self.networkMapperRepo = NetworkMapperRepository()

    def findOpenPorts(self,host):
        #Scan ports 1-1000 for current Host
        self.portScanner.scan(host, '1-100')

        listOfOpenPortObjs = []
        dateTimeChecked = datetime.now()

        #Loop through each scanned port and build list of those that are open
        for protocols in self.portScanner[host].all_protocols():
            lport = self.portScanner[host][protocols].keys()
            for port in lport:
                if(self.portScanner[host][protocols][port]['state'] == 'open'):
                    listOfOpenPortObjs.append(nmapObj(host,port,True,dateTimeChecked))

        #Get History for Port
        portHistory = self.networkMapperRepo.getPortHistory(host)

        #Inserting into Database        
        self.networkMapperRepo.postOpenPortResults(listOfOpenPortObjs)

        #build return Json Object
        returnObj = {}
        returnObj['Current'] = self.toJsonObj(listOfOpenPortObjs)
        returnObj['History'] = self.toJsonObj(portHistory)

        return returnObj
    
    def toJsonObj(self,listOfOpenPortObjs):
        data = {}
        data['Ip'] = listOfOpenPortObjs[0].ip
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