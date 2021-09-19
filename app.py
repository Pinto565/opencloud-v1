from flask import *
from ip_addr import *
from pyvpn import *
from available import *
from op_python import *

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Welcome to OpenCloud"

@app.route("/devices/available")
def devices_available():
    update_status()
    return jsonify(status)

@app.route("/certificate")
def certificate_generation():
    if request.method == "POST" or request.method == "GET":
        if "name" and "email" in request.args:
            name = request.args.get("name")
            email = request.args.get("email") 
            return jsonify(gen_cert(name, email))
        else:
            return "Invalid Request"
    else:
        return "Invalid Request"

@app.route("/deploy/flask")
def flask_deployment():
    if request.method == "POST" or request.method == "GET":
        if "giturl" and "device" in request.args:
            giturl = request.args.get("giturl")
            device = request.args.get("device")
            command = f"cat op_python.py | ssh {device} python3 - {giturl}"
            return command
        else:
            return "Invalid Request"
    else:
        return "Invalid Request"

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")