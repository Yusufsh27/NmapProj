import mysql.connector
from Repository.SQLConfigFile import SQLConfigurations
from Application.NMapObj import NMapObj, Record, PortStatus


class NetworkMapperRepository():
    
    def __init__(self):
        self.config = SQLConfigurations()

    def getPortHistory(self,host):
        try:
            with mysql.connector.connect(host= self.config.host, user= self.config.user, passwd =  self.config.passwd,database= self.config.database) as connection:
                sql = "SELECT * FROM nmapCallHistory WHERE ip = %s ORDER BY dateChecked DESC"
                mycursor = connection.cursor()
                mycursor.execute(sql, (host,))

                openPortObj = self.buildObject(mycursor,host)
                connection.commit()
                return openPortObj
            
        except Exception as e:
            print(e)

    def postPortResults(self,listOfOpenPortObjs):
        try:
            with mysql.connector.connect(host= self.config.host, user= self.config.user, passwd =  self.config.passwd,database= self.config.database) as connection:
                sql = "INSERT INTO nmapCallHistory (ip,portNumber,portStatus,dateChecked) VALUES (%s,%s,%s,%s)"
                mycursor = connection.cursor()

                for openPortObj in listOfOpenPortObjs:         
                    val = (openPortObj.ip,openPortObj.port,openPortObj.status,openPortObj.date)   
                    mycursor.execute(sql, val)

                connection.commit()
        except Exception as e:
            print(e)

    def buildObject(self, mycursor,host):
        openPortObj = NMapObj(host)
        dateHashLookUp = {}
        for row in mycursor:
            date = row[4]
            if(date not in dateHashLookUp):
                openPortObj.appendRecord(Record(date))
                dateHashLookUp[date] = openPortObj.getNumOfRecords()-1
            if(row[3] == 1):
                status = True
            else:
                status = False
            portStatus = PortStatus(row[2],status)
            openPortObj.records[dateHashLookUp[date]].appendPort(portStatus)
        
        return openPortObj

