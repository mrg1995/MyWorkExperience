# -*- utf-8 -*-
# 封装一个邮箱类
import os
import json
import configparser
import smtplib
import schedule
from email import encoders
from email.header import Header
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from collections import OrderedDict

import time


class QuickEmail:
    # 邮件信息从配置文件中读取还是使用内置的邮件配置
    # 默认使用文件配置
    _build_in_config = True
    # 协议配置文件，默认为default.ini
    _protocol_file = 'default.ini'
    # 账号配置文件，默认为account.ini
    _account_file = 'account.ini'
    # 配置文件句柄
    _config_handler = None
    # SMTP配置
    _smtp = OrderedDict({})
    _smtp_ssl = OrderedDict({})
    # POP3配置
    _pop3 = OrderedDict({})
    _pop3_ssl = OrderedDict({})
    # IMAP配置
    _imap = OrderedDict({})
    _imap_ssl = OrderedDict({})
    # 账号
    _from = OrderedDict({})
    # 发送账号集合
    _tolist = []
    # 邮件消息
    _mail_msg = None
    # 附件列表
    _attachment_list = []
    # 执行时间
    _time = None

    # 初始化
    def __init__(self, config_from='file', protocol_config=None,
                 account_config=None, protocol_file=None, account_file=None):
        if config_from == 'file':
            self._build_in_config = True
        else:
            self._build_in_config = False

        if self._build_in_config is True:
            # 设置协议配置文件
            if protocol_file is not None:
                self._protocol_file = protocol_file

            # 设置账号配置文件
            if account_file is not None:
                self._account_file = account_file

            # 初始化配置解析器
            self._config_handler = configparser.ConfigParser()
            # 读取协议配置
            self._load_config()
            # 读取账号配置
            self._read_account()
        else:
            if isinstance(protocol_config, dict) and isinstance(account_config, dict):
                if 'smtp' in protocol_config.keys():
                    self._smtp['server'] = protocol_config['smtp']['server']
                    self._smtp['port'] = protocol_config['smtp']['port']
                if 'smtp-ssl' in protocol_config.keys():
                    self._smtp_ssl['server'] = protocol_config['smtp-ssl']['server']
                    self._smtp_ssl['port'] = protocol_config['smtp-ssl']['port']
                if 'pop3' in protocol_config.keys():
                    self._pop3['server'] = protocol_config['pop3']['server']
                    self._pop3['port'] = protocol_config['pop3']['port']
                if 'pop3-ssl' in protocol_config.keys():
                    self._pop3_ssl['server'] = protocol_config['pop3-ssl']['server']
                    self._pop3_ssl['port'] = protocol_config['pop3-ssl']['port']
                if 'imap' in protocol_config.keys():
                    self._imap['server'] = protocol_config['imap']['server']
                    self._imap['port'] = protocol_config['imap']['port']
                if 'imap-ssl' in protocol_config.keys():
                    self._imap_ssl['server'] = protocol_config['imap-ssl']['server']
                    self._imap_ssl['port'] = protocol_config['imap-ssl']['port']
                if 'account' in account_config.keys():
                    self._from['account'] = account_config['account']
                if 'password' in account_config.keys():
                    self._from['password'] = account_config['password']
            else:
                raise Exception('参数不正确')

    # 获取字符型的配置
    def _get_ini_str(self, section_name, key_name):
        if self._config_handler.has_section(section_name) and self._config_handler.has_option(section_name, key_name):
            return self._config_handler.get(section_name, key_name)
        else:
            return None

    # 获取整数型的配置
    def _get_ini_int(self, section_name, key_name):
        if self._config_handler.has_section(section_name) and self._config_handler.has_option(section_name, key_name):
            return self._config_handler.getint(section_name, key_name)
        else:
            return None

    # 填充协议字段
    def _set_protocol(self, config_item, section, default_port):
        if self._get_ini_str(section, 'server'):
            config_item['server'] = self._get_ini_str(section, 'server')
            if self._get_ini_int(section, 'port'):
                config_item['port'] = self._get_ini_int(section, 'port')
            else:
                config_item['port'] = default_port

    # 读取配置
    def _load_config(self):
        if self._protocol_file is None:
            raise Exception('协议配置文件未设置')

        # 读取配置文件
        self._config_handler.read(self._protocol_file)

        # 读取smtp配置
        self._set_protocol(self._smtp, 'smtp', 25)
        # 读取smtp-ssl配置
        self._set_protocol(self._smtp_ssl, 'smtp-ssl', 465)
        # 读取pop3配置
        self._set_protocol(self._pop3, 'pop3', 110)
        # 读取pop3-ssl配置
        self._set_protocol(self._pop3_ssl, 'pop3-ssl', 995)
        # 读取imap配置
        self._set_protocol(self._imap, 'imap', 143)
        # 读取imap-ssl配置
        self._set_protocol(self._imap_ssl, 'imap-ssl', 993)

    # 读取邮箱账号
    def _read_account(self):
        if self._account_file is None:
            raise Exception('账号配置文件未设置')

        self._config_handler.read(self._account_file)

        self._from['account'] = self._get_ini_str('setting', 'account')
        self._from['password'] = self._get_ini_str('setting', 'password')

    # 设置接收邮件账户列表
    def add_tolist(self, addr):
        if isinstance(addr, str):
            self._tolist.append(addr)
        elif isinstance(addr, list) or isinstance(addr, tuple) or isinstance(addr, set):
            for x in addr:
                self._tolist.append(x)
        elif isinstance(addr, dict):
            for key, value in addr:
                self._tolist.append(value)

    # 从文件中增加to list列表
    def add_tolist_from_file(self, file):
        pass

    # 设置邮件格式
    # title  邮件标题
    # body   邮件内容
    # mail_type 邮件类型 是纯文本邮件还是带附件的邮件
    # attachment 附件文件名
    def set_mail(self, title, body, mail_type='plain'):
        """设置邮件内容"""
        if mail_type == 'plain':
            self.set_plain_mail(body)
        elif mail_type == 'html':
            self.set_html_mail(body)
        elif mail_type == 'attach':
            self.set_attach_mail(body)
            for attach in self._attachment_list:
                self._mail_msg.attach(attach)

        self._mail_msg['From'] = self._from['account']
        self._mail_msg['To'] = ', '.join(self._tolist)
        self._mail_msg['Subject'] = Header(title, 'utf-8')

    # 设置纯文本邮件
    def set_plain_mail(self, body):
        """纯文本邮件"""
        self._mail_msg = MIMEText(body, 'plain', 'utf-8')

    def set_html_mail(self, body):
        """HTML邮件"""
        self._mail_msg = MIMEText(body, 'html', 'utf-8')

    # 设置带附件邮件
    def set_attach_mail(self, body):
        """附件邮件"""
        self._mail_msg = MIMEMultipart('related')
        contents = MIMEText(body, 'html', 'utf-8')
        self._mail_msg.attach(contents)

    def add_attach(self, filename):
        """添加附件"""
        attach = MIMEBase('application', 'octet-stream')
        attach.set_payload(open(filename, 'rb').read())
        encoders.encode_base64(attach)
        attach.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(filename))

        self._attachment_list.append(attach)

    def add_attach_list(self, file_list):
        """添加附件列表"""
        if isinstance(file_list, list):
            for filename in file_list:
                self.add_attach(filename)

    def add_attach_path(self, pathname):
        """添加一个路径下的所有附件"""
        os.chdir(pathname)
        dirname = os.getcwd()

        for filename in os.listdir(dirname):
            self.add_attach(filename)

    def clear_tolist(self):
        """清空to list"""
        self._tolist.clear()

    def clear_attach(self):
        """清空附件列表"""
        self._attachment_list.clear()

    def clear_mail_msg(self):
        """清空邮件消息"""
        self._mail_msg = None

    def clear_all_setting(self):
        """清空所有设置（用户使用过程中添加的一些设置）"""
        self.clear_tolist()
        self.clear_attach()
        self.clear_mail_msg()

    # 发送邮件
    # message: 消息体，不选择则认定为是构造的邮件
    # ssl: 是否使用ssl发送
    def send_mail(self, message=None, ssl=False):
        if self._time:
            schedule.every().day.at(self._time).do(self._send_mail, message, ssl)
            while True:
                schedule.run_pending()
                time.sleep(1)
        else:
            self._send_mail(message, ssl)

    def _send_mail(self, message=None, ssl=False):
        if message is None:
            message = self._mail_msg

        if ssl is False:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self._smtp['server'], self._smtp['port'])
        else:
            smtpObj = smtplib.SMTP_SSL()
            smtpObj.connect(self._smtp_ssl['server'], self._smtp_ssl['port'])
        # 登陆邮件服务器
        smtpObj.login(self._from['account'], self._from['password'])
        # 发送邮件
        smtpObj.sendmail(self._from['account'], self._tolist, message.as_string())
        # 退出
        smtpObj.quit()
        return schedule.CancelJob

    # 接收邮件
    def recv_mail(self, protocol='pop3', ssl=False):
        pass

    # 设置定时发送时间
    def set_time(self, set_time=_time):
        self._time = set_time

    # 测试打印
    def dump_config(self):
        print('smtp     setting: ', self._smtp)
        print('smtp-ssl setting: ', self._smtp_ssl)
        print('pop3     setting: ', self._pop3)
        print('pop3-ssl setting: ', self._pop3_ssl)
        print('imap     setting: ', self._imap)
        print('imap-ssl setting: ', self._imap_ssl)
        print('==================================')
        print('account:', self._from)

    def dump_tolist(self):
        print('tolist: ', self._tolist)

    def dump_attach(self):
        print('attach list: ', self._attachment_list)
