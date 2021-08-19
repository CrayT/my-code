##SMTP定时发送邮件
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import time
class email_time():
    def _format_addr(self,s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))
    def send(self):
        myself_emil = 'email'
        pass_word = 'password'
        sender = myself_emil
        receivers = [myself_emil]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        mail_msg = """
        这是邮件正文
        """
        message = MIMEMultipart()
        message.attach(MIMEText(mail_msg, 'plain', 'utf-8'))
        message['From'] = self._format_addr('发件人 <%s>' % sender)
        message['To'] = self._format_addr('收件人 <%s>' % receivers[0])
        message['Subject'] = Header('test', 'utf-8')
        
        file_addr = '附件地址'
        part = MIMEApplication(open(file_addr, 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename = "附件")
        message.attach(part)

        smtpObj = smtplib.SMTP() 
        smtpObj.set_debuglevel(1)
        smtpObj.connect('smtp.163.com', 25)    # 25 为 SMTP 端口号
        smtpObj.login(myself_emil, pass_word)
        smtpObj.sendmail(sender, receivers, message.as_string())
def main():
    i = 1
    while True:
        send_emial = email_time().send()
        print('已发送第%s封'%(i))
        i += 1
        time.sleep(10)
if __name__ == '__main__':
    main()