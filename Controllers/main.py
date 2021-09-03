from flask import Flask, request
from flask_restful import Resource, Api 
import NmapController


app = Flask(__name__)
api = Api(app)

api.add_resource(NmapController.Controllers,"/getOpenPorts/<string:host>")

if __name__ == "__main__": 
    app.run(debug=True)