from os import device_encoding
from flask import *
from tun_ip_generator import *
from vpn_certificate_generator import *
from devices_available import *
from flask_deployment import *
from haproxy_conf_adder import *
from command_executor import *
from ports import *


app = Flask(__name__)


@app.after_request
def after_request_func(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


@app.route('/')
def hello_world():
    result = {
        "status": "Api is Up And Running"
    }
    return jsonify(result)


@app.route("/devices/available")
def devices_available():
    update_status()
    return jsonify(status)


@app.route("/ssh_key")
def get_sshkey():
    try:
        cmd = "cat ~/.ssh/id_rsa.pub"
        output = {
            "ssh_key": comm(cmd)
        }
        return jsonify(output)
    except:
        output = {
            "ssh_key": "failed"
        }
        return jsonify(output), 404


@app.route("/certificate")
def certificate_generation():
    if request.method == "POST" or request.method == "GET":
        if "imei" in request.args and "email" in request.args:
            empty = ""
            imei = request.args.get("imei")
            email = request.args.get("email")
            if imei != empty and email != empty:
                return jsonify(gen_cert(imei, email))
            else:
                return "Some Parameters Missing"
        else:
            result = {
                "imei": "not provided",
                "email": "not provided",
                "ip_address": "failed",
                "status": "failed"
            }
            return jsonify(result), 404
    else:
        result = {
            "imei": "not provided",
            "email": "not provided",
            "ip_address": "failed",
            "status": "method not allowed"
        }
        return jsonify(result), 404


@app.route("/deploy/sshd")
def sshd_deployment():
    if request.method == "POST" or request.method == "GET":
        if "device" in request.args and "port" in request.args:
            device = request.args.get("device")
            port = request.args.get("port")
            web_addr = write_ssh_conf(device, port)
            command = "systemctl restart haproxy"
            comm(command)
            result = {
                "status": "deployed successfully",
                "public_site": web_addr,
                "type": "ssh"
            }
            return jsonify(result)
        else:
            result = {
                "status": "parameters missing"
            }
            return jsonify(result), 404
    else:
        result = {
            "status": "method not allowed"
        }
        return jsonify(result), 404


@app.route("/deploy/flask")
def flask_deployment():
    if request.method == "POST" or request.method == "GET":
        if "giturl" in request.args and "device" in request.args:
            empty = ""
            giturl = request.args.get("giturl").replace(" ", "")
            device = request.args.get("device").replace(" ", "")
            port = request.args.get("port").replace(" ", "")
            if giturl != empty and device != empty:
                if port != empty:
                    port = port
                else:
                    port = "8022"
                command = f"cat {os.getcwd()}/flask_deployment.py | ssh {device} -p {port} python3 - {giturl}"
                output = comm(command)
                if output:
                    web_addr = write_http_conf(device, "8000")
                    command = "systemctl restart haproxy"
                    comm(command)
                    result = {
                        "status": "deployed successfully",
                        "public_site": web_addr,
                        "command": command,
                        "logs": output
                    }
                    return jsonify(result)
            else:
                result = {
                    "status": "Some Parameters Missing"
                }
            return jsonify(result), 404
        else:
            result = {
                "status": "parameters missing"
            }
            return jsonify(result), 404
    else:
        result = {
            "status": "method not allowed"
        }
        return jsonify(result), 404


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
