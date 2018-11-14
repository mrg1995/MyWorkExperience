import unittest
from mathfunc import *


'''
skip装饰器一共有三个 
unittest.skip(reason)、unittest.skipIf(condition,reason)、unittest.skipUnless(condition,reason)， 
skip无条件跳过，skipIf当condition为True时跳过，skipUnless当condition为False时跳过。

每个测试方法均以 test 开头，否则是不被unittest识别的。

其实每一个test开头的方法都会加载为独立的测试用例。

在unittest.main()中加 verbosity 参数可以控制输出的错误报告的详细程度，默认是 1，如果设为 0，则不输出每一用例的执行结果。如果参数为2则表示输出详细结果。
'''

class TestMathFunc(unittest.TestCase):

    # TestCase基类方法,所有case执行之前自动执行
    @classmethod
    def setUpClass(cls):
        print("这里是所有测试用例前的准备工作")

    # TestCase基类方法,所有case执行之后自动执行
    @classmethod
    def tearDownClass(cls):
        print("这里是所有测试用例后的清理工作")

    # TestCase基类方法,每次执行case前自动执行
    def setUp(self):
        print("这里是一个测试用例前的准备工作")

    # TestCase基类方法,每次执行case后自动执行
    def tearDown(self):
        print("这里是一个测试用例后的清理工作")

    @unittest.skip("我想临时跳过这个测试用例.")
    def test_add(self):
        self.assertEqual(3, add(1, 2))
        self.assertNotEqual(3, add(2, 2))  # 测试业务方法add

    def test_minus(self):
        self.skipTest('跳过这个测试用例')
        self.assertEqual(1, minus(3, 2))  # 测试业务方法minus

    def test_multi(self):
        self.assertEqual(6, multi(2, 3))  # 测试业务方法multi

    def test_divide(self):
        self.assertEqual(2, divide(6, 3))  # 测试业务方法divide
        self.assertEqual(2.5, divide(5, 2))

if __name__ == '__main__':
    # verbosity 参数用来控制输出错误报告的详细程度
    unittest.main(verbosity=2)