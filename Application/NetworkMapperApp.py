from typing import Callable
from nmap.nmap import PortScanner
from datetime import datetime
from Repository.NetworkMapperRepository import NetworkMapperRepository
from Application.NMapObj import NMapObj
from Application.Validation.InputValidation import InputValidation
import time

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

            #Get DateChecked
            date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

            #execute Nmap Scan
            #8 Seconds for 100 Ports IP
            #129 Seconds for 1000 Ports IP
            portObj = self.nMapScan(host,hostOrg,date)


            #Get History for Port
            portHistory = self.networkMapperRepo.getPortHistory(host)

            #Compare Current value vs Last Value
            #2 Seconds for 100 Records
            #2 Seconds for 1000 Records
            difference , portObj = self.compare(portObj, portHistory, date)

            #Inserting into Database      
            self.networkMapperRepo.postPortResults(portObj,date)


            # build return Json Object
            returnObj = self.buildReturnObject(portObj,portHistory,difference,date)
            

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

    def nMapScan(self,host,hostOrg, date):
        try:
            #Scan ports 1-1000 for current Host
            #8 Seconds for 100 Ports IP Address
            #120 Seconds for 1000 Ports IP
            self.portScanner.scan(host, '1-60')
            self.inputValidation.ScanOfIpAddress(self.portScanner,host,hostOrg)

            openPortObj = NMapObj(host)

            #Loop through each scanned port and build list of those that are open
            for protocols in self.portScanner[host].all_protocols():
                portList = self.portScanner[host][protocols].keys()
                for port in portList:
                    if(self.portScanner[host][protocols][port]['state'] == 'open'):
                        openPortObj.ports[port] = {}
                        openPortObj.ports[port][date] = "Open"
            
            return openPortObj

        except Exception as e:
            raise e
    
    def buildReturnObject(self,portObj,portHistory, difference,date):
        try:
            returnObj = {}
            returnObj['Current'] = self.toJsonObjForCurrent(portObj,date)
            returnObj['History'] = self.toJsonObjForHistory(portHistory)
            returnObj['Difference'] = difference
            
            return returnObj

        except Exception as e:
            raise e
    
    def compare(self,currentPortVals, lastPortVals, dateChecked):
        diff = []

        for port in currentPortVals.ports.keys():
            if(port not in lastPortVals.ports):
                diff.append(NetworkMapperApp.insertCompareVals(port,dateChecked,"Alawys"))
            else:
                largestDate = max(lastPortVals.ports[port])
                if(currentPortVals.ports[port][dateChecked] != lastPortVals.ports[port][largestDate]):
                    diff.append(NetworkMapperApp.insertCompareVals(port,dateChecked,largestDate))        
        
        #Values set to being closed
        for port in lastPortVals.ports.keys():
            largestDate = max(lastPortVals.ports[port])
            if(port not in currentPortVals.ports and lastPortVals.ports[port][largestDate] == "Open"):
                #Add the fact that it is now false
                currentPortVals.ports[port] = {dateChecked: 'Closed'}
                diff.append(NetworkMapperApp.insertCompareVals(port,largestDate,dateChecked))

        return diff, currentPortVals

    def toJsonObjForHistory(self,portObj):
        data = {}
        data['Ip'] = portObj.ip
        data['Ports'] = portObj.ports

        return data
    
    def toJsonObjForCurrent(self,portObj, date):
        data = {}
        data['Ip'] = portObj.ip
        data['Date'] = date
        data['Ports'] = {}
        for port in portObj.ports.keys():
            data['Ports'][port] = portObj.ports[port][date]

        return data
    
    def insertCompareVals(port,open,closed):
        tmp = {}
        tmp["Port"] = port
        tmp[open] = "Open"
        tmp[closed] = "Closed"
        return tmp
    
    def setupDatabaseTables(self):
        try:
            self.networkMapperRepo.setupTables()
            return {"Message" : "Success"}
        except Exception as e:
            raise e