import subprocess
import smtplib
from ip_addr import *
from email.message import EmailMessage


def cert_json(name , email , ip,status):
    op = {
        "name" : name , 
        "email" : email ,
        "ip_adress" : ip,
        "status" : status
    }
    return op


def send_mail(name,r_mail):
    s_mail = "infantvalan02@gmail.com"
    s_pass = "krttcisguxjxkror"
    message = f"Hello...{name} . Thank You For Registering . Find the VPN Certificate below"
    msg=EmailMessage()
    msg['Subject'] = "Mail From Opencloud"
    msg['From'] = "OpenCloud"
    msg['To'] = r_mail
    msg.set_content(message)
    with open(f"~/{name}.ovpn","rb") as file:
        data = file.read()
        cert_name = file.name
        msg.add_attachment(data,maintype = "application", subtype = "ovpn",filename = cert_name)
    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    try:
        server.login(s_mail,s_pass)
        print("Logged In Successfully")
        server.send_message(msg)
        print("Mail Sent")
        server.quit()
    except:
        print("Mail Not Sent")

def gen_cert(name , email):
    name = name #("Enter the Client Name > ")
    # tun_ip = input("Enter Your Desired IP > ")
    # tun_ip = str(tun_ip)
    email = email #input("Enter your Mail Address > ")
    lower_name = name.replace(" ","").lower()
    try:
        tun_ip = generate_tun_ip()
        process = subprocess.run(f"sudo bash vpn.sh {lower_name}",shell=True)
        process = subprocess.run(f"echo \"ifconfig-push {tun_ip} 255.255.255.0\" > /etc/openvpn/ccd/{lower_name}",shell=True)
        process = subprocess.run(f"openssl x509 -subject -noout -in /etc/openvpn/easy-rsa/pki/issued/{lower_name}.crt",shell=True)
        send_mail(name,email)
        op = cert_json(name , email ,tun_ip, True)
        return op
    except:
        op = cert_json(name , email ,tun_ip, False)
        return op

def bad_request(reason):
    op = {
        "status" : 200,
        "comment" : reason
    }
    return op