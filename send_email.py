import json
import smtplib
from email.header import Header
from email.mime.text import MIMEText


def parse_config(file_name):
    config_file = open(file_name)
    json_config = json.load(config_file)
    config_file.close()
    return json_config


class SendEmail:
    def __init__(self):
        pass

    CONFIG_FILE = "/home/yujun/PycharmProjects/FaXuan/fx_login.conf"
    config = parse_config(CONFIG_FILE)
    email_info = config['email']
    user_name = email_info['user_name']
    user_password = email_info['password']

    subject = 'fx login'
    sender = email_info['sender']
    receiver = email_info['receiver']
    smtp_server = email_info['smtp_server']

    def send_msg(self, msg_content):
        msg = MIMEText(msg_content, 'text', 'UTF-8')
        msg['Subject'] = Header(self.subject, 'utf-8')

        smtp = smtplib.SMTP()
        smtp.connect(self.smtp_server)
        smtp.login(self.user_name, self.user_password)
        smtp.sendmail(self.sender, self.receiver, msg.as_string())
        smtp.quit()
