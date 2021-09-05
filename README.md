# NMAP Application


## Use Case:
    - Application is a backend API service used to get open ports for any provided valid IP address or Hostname

## How it Works:
    - User can input a IP address or hostname
    - The host will then be validated:
        - If a hostname is it a valid hostname
        - Convert the hostname to an IP address
        - Check if the IP address is valid
        - Perform a scan on the IP address is possible
    - Using Pythons NMAP Import we can all open ports between 1-1000 for the host provided
    - Then we check the history of that host is the database.
        - The database ONLY stores OPEN ports. It is assumed that if the port is not in the Database it is CLOSED
    -  We can then compare the MOST RECENT log of the host open ports
        - If the Datbase doesnt have a value that is was calculated from NMAP its assumed it was previously CLOSED
        - If the Datbase has a value that wasnt  calculated from NMAP its assumed it is currently CLOSED
    - Combine the Nmap calculcated ports, databse history and recent change into a return object



## How it Runs:
    - Install the necessary packages using pip
    - Go into ~/Repository/SQLConfigFile.py
    - Change the credentials to your credentials for your MYSQL
    - go into ~Controllers
    - execute python3 NMapController.py
    - Application should run on your locahost ie.(http://127.0.0.1:5000/)
    - In your browser or Postname can execute the following:
        - http://127.0.0.1:5000/ping #To see if service is running correctly
        - http://127.0.0.1:5000/openPorts/<host>  #To get Open Ports and its history for host
        - http://127.0.0.1:5000/portHistory/<host>  #To get you port history for host


## Imports Required:
Nmap: https://pypi.org/project/python-nmap/
Flask https://flask.palletsprojects.com/en/2.0.x/
FLASK_RESTFUL https://flask-restful.readthedocs.io/en/latest/
MYSQL_CONNECTOR https://dev.mysql.com/doc/connector-python/en/