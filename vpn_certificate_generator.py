import subprocess
import smtplib
from tun_ip_generator import *
from email.message import EmailMessage


def cert_json(name, email, ip, status):
    op = {
        "imei": name,
        "email": email,
        "ip_address": ip,
        "status": status
    }
    return op


def send_mail(imei, r_mail):
    s_mail = "infantvalan02@gmail.com"
    s_pass = "pmrdsejaymicrtoj"
    message = f"Hello..User. Thank You For Registering . Find the VPN Certificate below"
    msg = EmailMessage()
    msg['Subject'] = "Mail from opencloud for VPN certificate"
    msg['From'] = "infantvalan02@gmail.com"
    msg['To'] = r_mail
    msg.set_content(message)
    with open(f"/root/{imei}.ovpn", "rb") as file:
        data = file.read()
        cert_imei = f"{imei}.ovpn"
        msg.add_attachment(data, maintype="application",
                           subtype="ovpn", filename=cert_imei)
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    try:
        server.login(s_mail, s_pass)
        print("Logged In Successfully")
        server.send_message(msg)
        print("Mail Sent")
        server.quit()
    except:
        print("Mail Not Sent")


def gen_cert(imei, email):
    imei = imei
    email = email
    lower_imei = imei.replace(" ", "").lower()
    process = subprocess.run(f"./vpn.sh {lower_imei}", shell=True)
    if process.returncode == 0:
        tun_ip = generate_tun_ip()
        process = subprocess.run(
            f"echo \"ifconfig-push {tun_ip} 255.255.255.0\" > /etc/openvpn/ccd/{lower_imei}", shell=True)
        process = subprocess.run(
            f"openssl x509 -subject -noout -in /etc/openvpn/easy-rsa/pki/issued/{lower_imei}.crt", shell=True)
        send_mail(lower_imei, email)
        op = cert_json(lower_imei, email, tun_ip, "True")
    else:
        print("Failed")
        op = cert_json(lower_imei, email, "failed", "False")
    return op