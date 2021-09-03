import subprocess
import smtplib
from ip_addr import generate_tun_ip
from email.message import EmailMessage

def send_mail(name,r_mail):
    s_mail = "infantvalan02@gmail.com"
    s_pass = "krttcisguxjxkror"
    message = f"Hello...{name} . Thank You For Registering . Find the VPN Certificate below"
    msg=EmailMessage()
    msg['Subject'] = "Mail From Opencloud"
    msg['From'] = "OpenCloud"
    msg['To'] = r_mail
    msg.set_content(message)
    with open(f"{name}.ovpn","rb") as file:
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

def gen_cert():
    name = input("Enter the Client Name > ")
    # tun_ip = input("Enter Your Desired IP > ")
    # tun_ip = str(tun_ip)
    tun_ip = generate_tun_ip()
    email = input("Enter your Mail Address > ")
    name = name.replace(" ","").lower()
    process = subprocess.run(f"sudo bash vpn.sh {name}",shell=True)
    process = subprocess.run(f"echo \"ifconfig-push {tun_ip} 255.255.255.0\" > /etc/openvpn/ccd/{name}",shell=True)
    process = subprocess.run(f"openssl x509 -subject -noout -in /etc/openvpn/easy-rsa/pki/issued/{name}.crt",shell=True)
    name = name.upper()
    send_mail(name,email)