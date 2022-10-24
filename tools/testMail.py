from operator import truediv
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText

smtpserver = "smtp.qq.com"
smtpport = 465
subject = 'XMTY 登陆验证'
from_mail = "eonboia@qq.com"
from_name = 'XMTY_Login'
_to_mail = "yby@xmtyet.com"
password = "yuglelkusmyjbdbe"   # 16位授权码

def check(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex,email):
        return True
    else:
        return False

def send_email(check_code, to_mail):
    RES = {
            'res': False,
            'mes':'Invalid email'
        }
    try:
        if not check(to_mail):
            return RES
        smtp = smtplib.SMTP_SSL(smtpserver,smtpport)
        smtp.login(from_mail,password)
        body = "hi,  验证码是：\n " + str(check_code) + "\n\n\n     ———— XMTY LoginCheck"
        msg = MIMEMultipart()
        msg["Subject"] = Header(subject, "utf-8")
        msg["From"] = Header(from_name + " <XMTY_Login_Check>", "utf-8")
        msg["To"] = Header(to_mail, "utf-8")
        msgtext = MIMEText(body, "plain", "utf-8")
        msg.attach(msgtext)
        smtp.sendmail(from_mail,to_mail,msg.as_string())
        RES['res'] = True
        RES['mes'] = 'Success'
        return RES
    except(smtplib.SMTPException) as e:
        print(e)
        RES['mes'] = 'Bug.'
        return RES
    finally:
        smtp.quit()