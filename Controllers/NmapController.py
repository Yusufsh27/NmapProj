import sys
sys.path.append('..')

from flask_restful import Resource, Api  
from Application.networkMapper import NetworkMapperApp
from Repository.networkMapperRepoistory import NetworkMapperRepository

class NMapControllers(Resource):
    
    def get(self,host):
        
        #Find all open ports and history of the host
        networkMapperObj = NetworkMapperApp()
        openPortWithHistory = networkMapperObj.findOpenPorts(host)
        
        return openPortWithHistory