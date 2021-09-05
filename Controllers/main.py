import sys
sys.path.append('..')

from flask import Flask, request
from flask_restful import Resource, Api 
import NmapController


app = Flask(__name__)
api = Api(app)

api.add_resource(NmapController.NMapControllers,"/getOpenPorts/<string:host>")

if __name__ == "__main__": 
    app.run(debug=True)