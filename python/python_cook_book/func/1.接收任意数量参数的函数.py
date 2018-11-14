# 构造一个可接受任意数量参数的函数

def avg(first, *rest):
    return ((first + sum(rest)) / (1+len(rest)))


avg(1, 2) # 1.5
print(avg(1, 2, 3, 4)) # 2.5


import html
#  **attrs 是包含所有被传进来的关键字参数的字典
def make_element(name, value, **attrs):
    keyvals = [' %s="%s"' % item for item in attrs.items()]
    attr_str = ''.join(keyvals)
    element = '<{name}{attrs}>{value}</{name}>'.format(
                name=name,
                attrs=attr_str,
                value=html.escape(value))
    return element

# Example
# Creates '<item size="large" quantity="6">Albatross</item>'
make_element('item', 'Albatross', size='large', quantity=6)

# Creates '<p>&lt;spam&gt;</p>'
make_element('p', '<spam>')

# 位置参数  和  关键字参数
def anyargs(*args, **kwargs):
    print(args) # A tuple
    print(kwargs) # A dict

