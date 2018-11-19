# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'

# 有一个函数或方法，它使用*args和**kwargs作为参数，这样使得它比较通用， 但有时候你想检查传递进来的参数是不是某个你想要的类型

# 对任何涉及到操作函数调用签名的问题，你都应该使用 inspect 模块中的签名特性。 最主要关注两个类：Signature 和 Parameter


