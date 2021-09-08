import mysql.connector
from Repository.SQLConfigFile import SQLConfigurations
from Application.NMapObj import NMapObj
from datetime import datetime


class NetworkMapperRepository():
    
    def __init__(self):
        self.config = SQLConfigurations()

    def getPortHistory(self,host):
        try:
            with mysql.connector.connect(host= self.config.host, user= self.config.user, passwd =  self.config.passwd,database= self.config.database) as connection:
                sql = "SELECT * FROM nmapCallHistory USE INDEX (idx_ip_dateChecked_portNumber) WHERE ip = %s ORDER BY dateChecked DESC"
                mycursor = connection.cursor()
                mycursor.execute(sql, (host,))

                openPortObj = self.buildObject(mycursor,host)
                connection.commit()
                return openPortObj
            
        except Exception as e:
            print(e)

    def postPortResults(self,portObj, date):
        try:
            with mysql.connector.connect(host= self.config.host, user= self.config.user, passwd =  self.config.passwd,database= self.config.database) as connection:
                sql = "INSERT INTO nmapCallHistory (ip,portNumber,portStatus,dateChecked) VALUES (%s,%s,%s,%s)"
                mycursor = connection.cursor()

                IPAddress = portObj.ip
                dateDB = datetime.strptime(date, '%m/%d/%Y, %H:%M:%S')
                for port in portObj.ports.keys():
                    status = True if portObj.ports[port][date] == "Open" else False
                    val = (IPAddress,port,status,dateDB)   
                    mycursor.execute(sql, val)
                
                connection.commit()
        except Exception as e:
            print(e)

    
    def setupTables(self):
        try:
            with mysql.connector.connect(host= self.config.host, user= self.config.user, passwd = self.config.passwd,database= self.config.database) as connection:
                mycursor = connection.cursor()
                sql = "CREATE TABLE nmapCallHistory (id int AUTO_INCREMENT, ip varchar(20), portNumber int, portStatus tinyint(1), dateChecked datetime, PRIMARY KEY(id))"
                mycursor.execute(sql, ())
                sql = "CREATE UNIQUE INDEX idx_ip_dateChecked_portNumber ON nmapCallHistory (ip,dateChecked,portNumber)"
                mycursor.execute(sql, ())
                connection.commit()
            
        except Exception as e:
            print(e)
    
    def buildObject(self, mycursor,host):
        portStatusObj = NMapObj(host)
        for row in mycursor:     
            port = row[2]
            if(port not in portStatusObj.ports):
                portStatusObj.ports[port] = {}

            status = "Open" if row[3] == 1 else "Closed"
            portStatusObj.ports[port][row[4].strftime("%m/%d/%Y, %H:%M:%S")] = status
        
        return portStatusObj

