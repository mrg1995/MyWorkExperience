from quickmail import QuickEmail

# 创建一个qe实例
qe = QuickEmail()
# 设置邮件接收列表
qe.add_tolist(['2838654353@qq.com'])
# 设置邮件内容，邮件默认是纯文本邮件
qe.set_mail('标题：测试邮件', '这是一个纯文本邮件 sent by quickEmail', mail_type='plain')
# 设置时间
qe.set_time("16:21")
# 发送邮件
qe.send_mail(ssl=True)
