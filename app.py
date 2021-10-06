from flask import *
from ip_addr import *
from pyvpn import *
from available import *
from op_python import *
from haproxy_conf import *
from exec_comm import *
# from ports import *


app = Flask(__name__)

@app.after_request
def after_request_func(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

@app.route('/')
def hello_world():
    return "Opencloud API is up and running"


@app.route("/devices/available")
def devices_available():
    update_status()
    return jsonify(status)


@app.route("/ssh_key")
def get_sshkey():
    try:
        cmd = "cat /root/.ssh/id_rsa.pub"
        output = {
            "ssh_key" : comm(cmd)
        }
        return jsonify(output)
    except:
        output = {
            "ssh_key" : "failed"
        }
        return jsonify(output)


@app.route("/certificate")
def certificate_generation():
    if request.method == "POST" or request.method == "GET":
        if "imei"  in request.args and "email" in request.args :
            imei = request.args.get("imei")
            email = request.args.get("email")
            return jsonify(gen_cert(imei, email))
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
            web_addr = write_ssh_conf(device,port)
            command = "systemctl restart haproxy"
            #comm(command)
            result = {
                "status": "deployed successfully",
                "public_site" : web_addr,
                "type" : "ssh"
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


@app.route("/deploy/flask")
def flask_deployment():
    if request.method == "POST" or request.method == "GET":
        if "giturl" in request.args and "device" in request.args:
            giturl = request.args.get("giturl")
            device = request.args.get("device")
            port = request.args.get("port")
            if port:
                port = port
            else:
                port = "8022"
            command = f"cat /root/opencloud_be/op_python.py | ssh {device} -p {port} python3 - {giturl}"
            output = comm(command)
            web_addr = write_http_conf(device,"8000")
            command = "systemctl restart haproxy"
            comm(command)
            result = {
                "status": "deployed successfully",
                "public_site" : web_addr,
                "command" : command ,
                "logs": output
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