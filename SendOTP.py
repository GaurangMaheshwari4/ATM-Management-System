import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

def send_otp(To,From="nirmabank@gmail.com",Password="NIRMA@BANK",Subject="OTP for resetting password",message="Your OTP is "):
    otp = ""
    for i in range(4):
        otp = otp + str(random.randint(0,9))
    message = message + otp
    msg = MIMEMultipart("alternative")
    msg["Subject"] = Subject
    msg["From"] = From
    msg["To"] = To
    part1 = MIMEText(message,'plain')
    msg.attach(part1)
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(From,Password)
    server.sendmail(From,To,msg.as_string())
    server.quit()
    return otp
