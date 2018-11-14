# -*- coding:utf-8 -*-
# 发送纯文本邮件，无配置文件

from quickmail import QuickEmail

# 创建一个qe实例
qe = QuickEmail(config_from='nofile',
                protocol_config=
                {
                    "smtp-ssl": {
                        "server": "smtp.mxhichina.com",
                        "port": "465"
                    }
                },
                account_config=
                {
                    "account":"xiaodong.guo@sairobo.com",
                    "password":"19975201314aiAI"  # 阿里云邮箱登录密码直接就能用    163邮箱是开启smtp服务给的授权密码
                })

qe.dump_config()

# 设置邮件接收列表
qe.add_tolist(['2838654353@qq.com'])
# 设置邮件内容，邮件默认是纯文本邮件
qe.set_mail('标题：测试邮件', '这是一个纯文本邮件 sent by quickEmail', mail_type='plain')
# 发送邮件
qe.send_mail(ssl=True)

