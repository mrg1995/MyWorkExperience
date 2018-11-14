# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'

# 有一个 出 __init__()方法 只定义了一个方法的类  为了简化代码 怎么转化为一个函数

# 大多数情况 可以使用闭包来将单个方法的类转化为函数

from urllib.request import urlopen


class UrlTemplate:
    def __init__(self, template):
        self.template = template

    def open(self, **kwargs):
        return urlopen(self.template.format_map(kwargs))
        # return self.template.format_map(kwargs)


# Example use. Download stock data from yahoo
yahoo = UrlTemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo.open(names='IBM,AAPL,FB', fields='sl1c1v'):
    print(line.decode('utf-8'))


# 这个类可以被一个更简单的函数代替  闭包方式
def urltemplate(template):
    def opener(**kwargs):
        return urlopen(template.format_map(kwargs))
    return opener

# Example use
yahoo = urltemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo(names='IBM,AAPL,FB', fields='sl1c1v'):
    print(line.decode('utf-8'))

# 任何时候只要你碰到需要给某个函数增加额外的状态信息的问题，都可以考虑使用闭包。