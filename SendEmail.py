# -*- coding: utf-8 -*-
# Time    : 2019/4/25 21:32
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794


import os
# 发送邮件
import smtplib
import time
# TODO 导入构造邮件模块
import traceback
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

from settings import from_addr, from_name, to_addr, to_name, smtp_server, password

__all__ = ['ConstructEmail', 'SendEmail']

if not all((from_addr, from_name, to_addr, to_name, smtp_server, password)):
    raise Exception('你必须配置好邮箱')


class ConstructEmail():
    '''
        构造邮件:
            1. 纯文本邮件, textConnent
            2. html邮件, htmlConnent
            3. 携带附件, annex
    '''

    def __init__(self):
        pass

    # TODO 处理中文字符乱码
    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    # TODO 设置联系人信息
    def _contact(self, msg, from_addr, to_addr, title):
        msg['From'] = self._format_addr('%s <%s>' % (from_name, from_addr))
        msg['To'] = self._format_addr('%s <%s>' % (to_name, to_addr))
        msg['Subject'] = Header(title, 'utf-8').encode()

    # TODO 普通邮件
    def textConnent(self, from_addr, to_addr, content, title):
        msg = MIMEText(content, 'plain', 'utf-8')
        self._contact(msg, from_addr, to_addr, title)
        return msg

    # TODO HTML邮件
    def htmlcontent(self, from_addr, to_addr, content, title):
        msg = MIMEText(content, 'html', 'utf-8')
        self._contact(msg, from_addr, to_addr, title)
        return msg

    # TODO 附件
    def annex(self, path, content, from_addr, to_addr, title):
        # 邮件对象:
        msg = MIMEMultipart()
        # 添加附件就是加上一个MIMEBase，从本地读取一个图片:
        msg.attach(content)
        self._contact(msg, from_addr, to_addr, title)
        filepath, houzui = os.path.splitext(path)  # ('imgs/336', '.jpg')
        basefilepath, filename = os.path.split(path)  # ('imgs', '336.jpg')
        with open(path, 'rb') as f:
            # 设置附件的MIME和文件名，这里是png类型:
            mime = MIMEBase('zip', houzui, filename=filename)
            # 加上必要的头信息:
            mime.add_header('Content-Disposition', 'attachment', filename=filename)
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            # 把附件的内容读进来:
            mime.set_payload(f.read())
            # 用Base64编码:
            encoders.encode_base64(mime)
            # 添加到MIMEMultipart:
            msg.attach(mime)
            return msg


class SendEmail():
    '''
        发送邮件类
    '''

    def __init__(self, emtype='textConnent', path=''):
        self.ConstructEmail = ConstructEmail()
        self.server = self.login()
        self.emtype = emtype
        self.path = path

    def __del__(self):
        print('退出成功')
        self.server.quit()

    # TODO 发送的邮件类型
    def __emailType(self):
        emtypes = {
            'textConnent': self.ConstructEmail.textConnent,
            'htmlcontent': self.ConstructEmail.htmlcontent,
        }
        return emtypes.get(self.emtype, 'textConnent')

    def login(self):
        # Ubuntu下运行好像只能走加密通道465端口, window下也可以走不加密通道25端口,https://segmentfault.com/q/1010000007661948
        server = smtplib.SMTP_SSL(smtp_server, 465)
        server.set_debuglevel(0)  # 调试等级
        server.login(from_addr, password)
        print('登录成功')
        return server

    # TODO 发送邮件
    def sendEmail(self, content='内容', title='标题', s=''):
        try:
            m = self.__emailType()
            msg = m(from_addr, to_addr, content, title)
            if self.path:
                msg = self.ConstructEmail.annex(self.path, msg, from_addr, to_addr, title)
            self.server.sendmail(from_addr, [to_addr], msg.as_string())
            print(f"{s} ---->{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 发送成功")
        except smtplib.SMTPAuthenticationError:
            print(traceback.format_exc())
        except smtplib.SMTPDataError:
            print(traceback.format_exc())


if __name__ == '__main__':
    print(password)
    content = '<h1>测试html</h1>'
    title = '测试'
    sendEmail = SendEmail('htmlcontent')
    for i in range(5):
        sendEmail.sendEmail(content, title)
        time.sleep(2 * 2)
    del sendEmail
