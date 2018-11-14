###  常见的断言方法

```
assertEqual(a, b) a == b 
assertNotEqual(a, b) a != b 
assertTrue(x) bool(x) is True 
assertFalse(x) bool(x) is False 
assertIs(a, b) a is b 
assertIsNot(a, b) a is not b 
assertIsNone(x) x is None 
assertIsNotNone(x) x is not None 
assertIn(a, b) a in b 
assertNotIn(a, b) a not in b 
assertIsInstance(a, b) isinstance(a, b) 
assertNotIsInstance(a, b) not isinstance(a, b) 
assertAlmostEqual(a, b) round(a-b, 7) == 0 
assertNotAlmostEqual(a, b) round(a-b, 7) != 0 
assertGreater(a, b) a > b 2.7 
assertGreaterEqual(a, b) a >= b 2.7 
assertLess(a, b) a < b 2.7 
assertLessEqual(a, b) a <= b 2.7 
assertRegexpMatches(s, re) regex.search(s) 2.7 
assertNotRegexpMatches(s, re) not regex.search(s) 2.7 
assertItemsEqual(a, b) sorted(a) == sorted(b) and works with unhashable objs 2.7 
assertDictContainsSubset(a, b) all the key/value pairs in a exist in b 2.7 
assertMultiLineEqual(a, b) strings 2.7 
assertSequenceEqual(a, b) sequences 2.7 
assertListEqual(a, b) lists 2.7 
assertTupleEqual(a, b) tuples 2.7 
assertSetEqual(a, b) sets or frozensets 2.7 
assertDictEqual(a, b) dicts 2.7 
assertMultiLineEqual(a, b) strings 2.7 
assertSequenceEqual(a, b) sequences 2.7 
assertListEqual(a, b) lists 2.7 
assertTupleEqual(a, b) tuples 2.7 
assertSetEqual(a, b) sets or frozensets 2.7 
assertDictEqual(a, b) dicts 2.7 
```

#### 基本使用流程

1. 用import unittest导入unittest模块 
2. 定义一个继承自unittest.TestCase的测试用例类，如 class abcd(unittest.TestCase): 
3. 定义setUp和tearDown，这两个方法与junit相同，即如果定义了则会在每个测试case执行前先执行setUp方法，执行完毕后执行tearDown方法。 
4. 定义测试用例，名字以test开头，unittest会自动将test开头的方法放入测试用例集中。 
5. 一个测试用例应该只测试一个方面，测试目的和测试内容应很明确。主要是调用assertEqual、assertRaises等断言方法判断程序执行结果和预期值是否相符。 
6. 调用unittest.main()启动测试 
7. 如果测试未通过，则会显示e，并给出具体的错误（此处为程序问题导致）。如果测试失败则显示为f，测试通过为，如有多个testcase，则结果依次显示。