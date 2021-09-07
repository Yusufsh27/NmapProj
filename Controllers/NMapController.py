import sys
sys.path.append('..')

from flask_restful import Resource, Api  
from flask import Flask, abort, request
from Application.NetworkMapperApp import NetworkMapperApp

app = Flask(__name__)
api = Api(app)

class NMapControllers(Resource):

    @app.route("/openPorts/<string:host>", methods=['GET'])
    def openPorts(host):
        try:
            #Find all open ports and history of the host
            networkMapper = NetworkMapperApp()
            openPortWithHistory = networkMapper.findOpenPorts(host)
            return openPortWithHistory
        except ValueError as e:
            return {"Message" : str(e)}, 400
        except Exception as e:
            return {"Message" : str(e)}, 500

    @app.route("/portHistory/<string:host>", methods=['GET'])
    def portHistory(host):
        try:
            #Find Port history of host
            networkMapperObj = NetworkMapperApp()
            #History Of IP
            portHistory = networkMapperObj.getPortHistory(host)
            return portHistory
        except ValueError as e:
            return {"Message" : str(e)}, 400
        except Exception as e:
            return {"Message" : str(e)}, 500
    
    @app.route("/setupDatabaseTables", methods=['GET'])
    def setupDatabaseTables():
        try:
            #Find all open ports and history of the host
            networkMapper = NetworkMapperApp()
            return networkMapper.setupDatabaseTables()
        except ValueError as e:
            return {"Message" : str(e)}, 400
        except Exception as e:
            return {"Message" : str(e)}, 500

    @app.route("/ping", methods=['GET'])
    def ping():
        return "Success"

if __name__ == "__main__": 
    app.run(debug=True)