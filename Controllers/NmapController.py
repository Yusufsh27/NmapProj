import sys
sys.path.append('..')

from flask_restful import Resource, Api  
from Application.networkMapper import networkMapper
from Repository.networkMapperRepoistory import sqlConnection

class Controllers(Resource):
    def get(self,host):
        networkMapperObj = networkMapper()
        thisDict = networkMapperObj.findOpenPorts(host)
        return thisDict