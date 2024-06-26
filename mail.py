#!/usr/bin/python
# -*- coding:utf-8 -*-
import smtplib
import email
import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.header import Header


class Mail:
    def __init__(self):
        # 构建alternative结构
        self.msg = MIMEMultipart('alternative')
        self.msg['From'] = '%s <%s>' % (Header(settings.From).encode(), settings.UserName)
        self.msg['To'] = str(settings.To)
        self.msg['message_id'] = email.utils.make_msgid()
        self.msg['Date'] = email.utils.formatdate()

    def send(self, subject, content):
        self.msg['Subject'] = subject
        # 构建alternative的text/plain部分
        textplain = MIMEText(content, _subtype='plain', _charset='UTF-8')
        self.msg.attach(textplain)
        if settings.UserName is None :
            return
        # 发送邮件
        try:
            if settings.Port == 80:
                client = smtplib.SMTP()
            else:
                client = smtplib.SMTP_SSL(settings.Host)
            # SMTP普通端口为25或80
            client.connect(settings.Host, settings.Port)
            # 开启DEBUG模式
            client.set_debuglevel(0)
            client.login(settings.UserName, settings.PassWord)
            # 发件人和认证地址必须一致
            # 备注：若想取到DATA命令返回值,可参考 smtplib 的 sendmaili 封装方法:
            #      使用SMTP.mail/SMTP.rcpt/SMTP.data方法
            client.sendmail(settings.UserName, settings.To, self.msg.as_string())
            client.quit()
            print('邮件发送成功！')
        except smtplib.SMTPConnectError as e:
            print('邮件发送失败，连接失败:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPAuthenticationError as e:
            print('邮件发送失败，认证错误:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPSenderRefused as e:
            print('邮件发送失败，发件人被拒绝:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPRecipientsRefused as e:
            print('邮件发送失败，收件人被拒绝:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPDataError as e:
            print('邮件发送失败，数据接收拒绝:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPException as e:
            print('邮件发送失败, ', e.message)
        except Exception as e:
            print('邮件发送异常, ', str(e))
