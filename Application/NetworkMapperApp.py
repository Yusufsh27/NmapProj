from nmap.nmap import PortScanner
from datetime import datetime
from Repository.NetworkMapperRepoistory import NetworkMapperRepository
from Application.NMapObj import NMapObj, Record, PortStatus
from Application.Validation.InputValidation import InputValidation

class NetworkMapperApp():

    def __init__(self):
        self.portScanner = PortScanner()
        self.networkMapperRepo = NetworkMapperRepository()
        self.inputValidation = InputValidation()

    def findOpenPorts(self,host):
        try:

            #Validations
            hostOrg = host
            host = self.inputValidation.Hostname(host)
            self.inputValidation.IpAddress(host,hostOrg)

            #execute Nmap Scan
            openPortObj = self.nMapScan(host,hostOrg)
            print("here")

            #Get History for Port
            portHistory = self.networkMapperRepo.getPortHistory(host)

            #Compare Current value vs Last Value
            difference = {}
            if(len(openPortObj.records) > 0 and len(portHistory.records) > 0):
                difference = self.compare(openPortObj.records[0].ports, portHistory.records[0].ports)

            #Inserting into Database        
            self.networkMapperRepo.postPortResults(openPortObj)

            # build return Json Object
            returnObj = self.buildReturnObject(openPortObj,portHistory,difference)
            

            return returnObj

        except Exception as e:
            raise e
    
    def getPortHistory(self,host):
        try:
            #Validations
            hostOrg = host
            host = self.inputValidation.Hostname(host)
            self.inputValidation.IpAddress(host,hostOrg)


            #Get History for Port
            portHistory = self.networkMapperRepo.getPortHistory(host)

            # build return Json Object
            returnObj = {}
            returnObj['History'] = self.toJsonObj(portHistory)

            return returnObj

        except Exception as e:
            raise e

    def nMapScan(self,host,hostOrg):
        try:
            #Scan ports 1-1000 for current Host
            self.portScanner.scan(host, '1-100')
            self.inputValidation.ScanOfIpAddress(self.portScanner,host,hostOrg)

            openPortObj = NMapObj(host)
            openPortObj.appendRecord(Record(datetime.now()))

            #Loop through each scanned port and build list of those that are open
            for protocols in self.portScanner[host].all_protocols():
                portList = self.portScanner[host][protocols].keys()
                for port in portList:
                    if(self.portScanner[host][protocols][port]['state'] == 'open'):
                        portStatus = PortStatus(port,True)
                        openPortObj.records[0].appendPort(portStatus)
            
            return openPortObj

        except Exception as e:
            raise e
    
    def buildReturnObject(self,openPortObj,portHistory, difference):
        try:
            returnObj = {}
            returnObj['Current'] = self.toJsonObj(openPortObj)
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
            if(key not in last):
                diff.append(NetworkMapperApp.insertCompareVals(key,"Open","Closed"))

        for key in last.keys():
            if(key not in current):
                diff.append(NetworkMapperApp.insertCompareVals(key,"Closed","Open"))
        
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
                    data['Records'][len(data['Records'])-1]["Ports"].append({port.portNum:"Open"})
            
        return data
    
    def insertCompareVals(port,current,last):
        tmp = {}
        tmp["Port"] = port
        tmp["Current"] = current
        tmp["Last"] = last
        return tmp