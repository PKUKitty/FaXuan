import smtplib
from email.header import Header
from email.mime.text import MIMEText


class SendEmail:
    def __init__(self):
        pass

    user_name = 'yujun@travelsky.com'
    user_password = 'Yj1314520'

    subject = 'fx login'
    sender = 'yujun@travelsky.com'
    receiver = 'yujun@travelsky.com'
    smtp_server = 'smtpav.travelsky.com'

    def send_msg(self, msg_content):
        msg = MIMEText(msg_content, 'text', 'UTF-8')
        msg['Subject'] = Header(self.subject, 'utf-8')

        smtp = smtplib.SMTP()
        smtp.connect(self.smtp_server)
        smtp.login(self.user_name, self.user_password)
        smtp.sendmail(self.sender, self.receiver, msg.as_string())
        smtp.quit()
