# -*- coding:utf-8 -*-

# 发送HTML文本邮件

from quickmail import QuickEmail

# 创建一个qe实例
qe = QuickEmail()
# 设置邮件接收列表
qe.add_tolist(['2838654353@qq.com'])
# 设置邮件内容，邮件默认是纯文本邮件
qe.set_mail('标题：测试邮件',
            '''
            <font style="color:red;">这是一个HTML邮件</font> sent by <b>quickEmail</b>
            ''',
            mail_type='html')
# 发送邮件
qe.send_mail(ssl=True)