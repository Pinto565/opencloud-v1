import subprocess
import os
from datetime import datetime
import pytz
from tun_ip_generator import *


def time():
    IST = pytz.timezone('Asia/Kolkata')
    update_time = (datetime.now(IST).strftime(
        '%Y:%m:%d %H:%M:%S %Z %z')).replace(" +0530", "")
    return update_time


hosts = added_devices()  # "vpn.opencloud.pattarai.in"

status = {
    "updated_time": time(),
    "device_status": []
}


def pinghost(host):
    cmd = f"ping {host} -c 1"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    result_text = (result.stdout)
    if "Request timed out" in result_text:
        return "offline"
    elif "Destination Host Unreachable" in result_text:
        return "offline"
    elif "100% packet loss" in result_text:
        return "offline"
    else:
        return "online"


def update_status():
    status["device_status"] = []
    status["updated_time"] = time()
    for host in hosts:
        try:
            devicestatus = {
                "host": host,
                "status": pinghost(host)
            }
        except:
            devicestatus = {
                "host": host,
                "status": "offline"
            }
        status["device_status"].append(devicestatus)
