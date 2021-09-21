from flask import *
from ip_addr import *
from pyvpn import *
from available import *
from op_python import *
from haproxy_conf import *

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
        if "name"  in request.args and "email" in request.args :
            name = request.args.get("name")
            email = request.args.get("email")
            return jsonify(gen_cert(name, email))
        else:
            result = {
                "status": "parameters missing"
            }
            return jsonify(result)
    else:
        result = {
            "status": "method not allowed"
        }
        return jsonify(result)


@app.route("/deploy/sshd")
def sshd_deployment():
    if request.method == "POST" or request.method == "GET":
        if "device" in request.args and "port" in request.args:
            device = request.args.get("device")
            port = request.args.get("port")
            try:
                write_conf("8022",device,port)
                result = {
                    "status": "deployed successfully"
                }
                return jsonify(result)
            except:
                result = {
                    "status": "deployment failed"
                }
                return jsonify(result)



@app.route("/deploy/flask")
def flask_deployment():
    if request.method == "POST" or request.method == "GET":
        if "giturl" in request.args and "device" in request.args:
            giturl = request.args.get("giturl")
            device = request.args.get("device")
            try:
                command = f"cat op_python.py | ssh {device} python3 - {giturl}"
                #command = "cat op_python.py | ssh " + device + " python3 - "+ giturl
                write_conf("80",device,"8000")
                result = {
                    "status": "deployed successfully"
                }
                return jsonify(result)
            except:
                result = {
                    "status": "deployment failed"
                }
                return jsonify(result)
        else:
            result = {
                "status": "parameters missing"
            }
            return jsonify(result)
    else:
        result = {
            "status": "method not allowed"
        }
        return jsonify(result)


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
