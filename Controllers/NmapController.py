import sys
sys.path.append('..')

from flask_restful import Resource, Api  
from flask import abort
from Application.NetworkMapperApp import NetworkMapperApp

class NMapControllers(Resource):
    
    def get(self,host):
        try:
            #Find all open ports and history of the host
            networkMapperObj = NetworkMapperApp()
            openPortWithHistory = networkMapperObj.findOpenPorts(host)
            return openPortWithHistory
        except Exception as e:
            abort(str(e))