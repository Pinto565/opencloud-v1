import json


def json_data():
    with open("ip.json", 'r+') as file:
        file_data = json.load(file)
        return (file_data["ipaddr"])

def write_json(new_ip):
    with open("ip.json", 'r+') as file:
        file_data = json.load(file)
        file_data["ipaddr"].append(new_ip)
        file.seek(0)
        json.dump(file_data, file, indent=4)

def write_ipaddress(new_data):
    with open("ip.json", 'r+') as file:
        file_data = json.load(file)
        file_data["ipaddresses"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)

def generate_tun_ip():
    ip_addr = json_data()
    ip_prefix = "10.8.0.X"
    last_digit_ip = ip_addr[len(ip_addr)-1]+1
    write_json(last_digit_ip)
    new_ip = ip_prefix.replace("X", str(last_digit_ip))
    write_ipaddress(new_ip)
    return new_ip

def added_devices():
    with open("ip.json", 'r+') as file:
        file_data = json.load(file)
        return file_data["ipaddresses"]

def device_data():
    with open("ip.json", 'r+') as file:
        file_data = json.load(file)
        return file_data["ssh_command"]

def append_device_ssh(ipaddr, user):
    device = {
        "ip_address": ipaddr,
        "username": user
    }
    with open("ip.json", 'r+') as file:
        file_data = json.load(file)
        file_data["ssh_command"].append(device)
        file.seek(0)
        json.dump(file_data, file, indent=4)

def get_ssh(device):
    with open("username.json", 'r+') as file:
        file_data = json.load(file)
        return file_data[device]