import mysql.connector
from Repository.sqlConfigFile import sqlConfigurations
from Application.nmapObj import nmapObj


class NetworkMapperRepository():
    
    def __init__(self):
        self.config = sqlConfigurations()

    def getPortHistory(self,host):
        try:
            listOfOpenPortObjs = []
            with mysql.connector.connect(host= self.config.host, user= self.config.user, passwd =  self.config.passwd,database= self.config.database) as connection:
                sql = "SELECT * FROM nmapCallHistory WHERE ip = %s"
                mycursor = connection.cursor()
                mycursor.execute(sql, (host,))
                
                for row in mycursor:
                    if(row[3] == 1):
                        status = True
                    else:
                        status = False
                    listOfOpenPortObjs.append(nmapObj(row[1],row[2],status,row[4]))

                connection.commit()
                
            return listOfOpenPortObjs
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