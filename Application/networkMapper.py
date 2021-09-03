from nmap.nmap import PortScanner
from datetime import datetime
from Repository.networkMapperRepoistory import sqlConnection
from Application.nmapObj import nmapObj
import json


class networkMapper():

    def __init__(self):
        pass

    def findOpenPorts(self,host):
        nm = PortScanner()
        nm.scan(host, '1-100')
        listofnmapObj = []

        dateTimeChecked = datetime.now()
        for proto in nm[host].all_protocols():
            lport = nm[host][proto].keys()
            for port in lport:
                if(nm[host][proto][port]['state'] == 'open'):
                    listofnmapObj.append(nmapObj(host,port,True,dateTimeChecked))

        x = sqlConnection()

        #Get History for Port
        testing = x.getPortHistory(host)

        #Inserting into Database        
        x.insertnmapresults(listofnmapObj)

        data = {}
        data['curr'] = self.to_dict(listofnmapObj)
        data['history'] = self.to_dict(testing)

        return data
    
    def to_dict(self,listofnmapObj):
        data = {}
        data['Ip'] = listofnmapObj[0].ip
        data['Records'] = []

        dateHashLookUp = {}

        for mapObj in listofnmapObj:
            date = mapObj.date.strftime("%m/%d/%Y, %H:%M:%S")
            if(date not in dateHashLookUp):
                data['Records'].append({'Date' : date})
                dateHashLookUp[date] = len(data['Records'])-1
                
            if("Ports" not in data['Records'][dateHashLookUp[date]]):
                data['Records'][dateHashLookUp[date]]["Ports"] = []
            
            data['Records'][dateHashLookUp[date]]["Ports"].append({mapObj.port:mapObj.status})
            
        return data