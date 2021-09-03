import mysql.connector
from Repository.sqlConfigFile import sqlConfigurations
from Application.nmapObj import nmapObj


class sqlConnection():
    
    def __init__(self):
        self.config = sqlConfigurations()

    def getPortHistory(self,host):
        try:
            listofnmapObj = []
            with mysql.connector.connect(host= self.config.host, user= self.config.user, passwd =  self.config.passwd,database= self.config.database) as connection:
                sql = "SELECT * FROM nmapCallHistory WHERE ip = %s"
                mycursor = connection.cursor()
                mycursor.execute(sql, (host,))
                for i in mycursor:
                    if(i[3] == 1):
                        status = True
                    else:
                        status = False
                    listofnmapObj.append(nmapObj(i[1],i[2],status,i[4]))
                connection.commit()
                
            return listofnmapObj
        except Exception as e:
            print(e)

    def insertnmapresults(self,listofnmapObj):
        try:
            with mysql.connector.connect(host= self.config.host, user= self.config.user, passwd =  self.config.passwd,database= self.config.database) as connection:
                sql = "INSERT INTO nmapCallHistory (ip,portNumber,portStatus,dateChecked) VALUES (%s,%s,%s,%s)"
                mycursor = connection.cursor()
                for v in listofnmapObj:         
                    val = (v.ip,v.port,v.status,v.date)   
                    mycursor.execute(sql, val)
                connection.commit()
        except Exception as e:
            print(e)