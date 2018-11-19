# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'


# 定义对象间的一种一对多的依赖关系 ,当一个对象的状态发生改变时 , 所有依赖于它的对象都得到通知并被自动更新。

# 优点:  实现了结构的解耦,在运行时，订阅者/观察者的数量以及观察者可能会变化，也可以改变。



# 有一个气象站可以获取温度、湿度、氧气的数据，和一些面板，每当数据更新时候要显示在面板上

# 可观察对象，该抽象类需要实现具体的注册和删除观察者管理方法。
class AbstractObservable(object):
    def register(self):
        raise NotImplementedError(
            'register is a abstract method which must be implemente')

    def remove(self):
        raise NotImplementedError(
            'remove is a abstract method which must be implemente')


# 观察者抽象类， 需要实现 update 方法，让可观察对象可以通知观察者。
class AbstractDisplay(object):
    def update(self):
        raise NotImplementedError(
            'update is a abstract method which must be implemente')

    def display(self):
        raise NotImplementedError(
            'display is a abstract method which must be implemente')


# 实现一个 Subject 用于管理多个事件的通知，可以称作可观察对象管理者。
class Subject(object):
    def __init__(self, subject):
        self.subject = subject
        self._observers = []

    def register(self, ob):
        self._observers.append(ob)

    def remove(self, ob):
        self._observers.remove(ob)

    def notify(self, data=None):
        for ob in self._observers:
            ob.update(data)


'''
观察者模式的可观察对象实现可以分成两种实现方案：

push 模式
pull 模式

push 模式能保证所有的观察者可以接收到全部的数据，无论需要不需要，频繁更新会影响性能。
pull 模式需要观察者自己拉去数据，实现起来比较容易出错，但是能按需获取信息。
'''


class WeatherData(AbstractObservable):
    def __init__(self, *namespaces):
        self._nss = {}
        self._clock = None
        self._temperature = None
        self._humidity = None
        self._oxygen = None

        for ns in namespaces:
            self._nss[ns] = Subject(ns)

    def register(self, ns, ob):
        if ns not in self._nss:
            raise Exception('this {} is invalid namespace'.format(ns))
        self._nss[ns].register(ob)

    def remove(self, ns, ob):
        return self._nss[ns].remove(ob)

    def set_measurement(self, data):
        # 此处实现可以更加紧凑，但是为了表达更简单，采用如下方式
        self._clock = data['clock']
        self._temperature = data['temperature']
        self._humidity = data['humidity']
        self._oxygen = data['oxygen']

        for k in self._nss.keys():
            if k != 'all':
                data = self

            self._nss[k].notify(data)

    # 以下 property 为了实现 pull 模式
    @property
    def clock(self):
        return self._clock

    @property
    def temperature(self):
        return self._temperature

    @property
    def humidity(self):
        return self._humidity

    @property
    def oxygen(self):
        return self._oxygen


# 这是一个总览的 Display ，采用 push 模式更新，获取当前能获取的所有数据，并且显示出来。
class OverviewDisplay(AbstractDisplay):
    def __init__(self):
        self._data = {}

    def update(self, data):
        self._data = data
        self.display()

    def display(self):
        print(u'总览显示面板：')
        for k, v in self._data.items():
            print(k + ': ' + str(v))


# 采用 pull 模式。一个只会显示温度的 Display，能观察到时间和温度变化，由于只关心温度数据
class TemperatureDisplay(AbstractDisplay):
    def __init__(self):
        self._storage = []

    def update(self, data):
        dt = data.clock
        temperature = data.temperature
        self._storage.append((dt, temperature))
        self.display()

    def display(self):
        print(u'温度显示面板：')
        for storey in self._storage:
            print(storey[0] + ': ' + str(storey[1]))


# 被观察对象
class Be_look:
    def __init__(self, *namespaces):
        self._nss = {}
        self._age = None
        self._name = None
        # 将一些被观察的类型 初始化管理器实例
        for ns in namespaces:
            self._nss[ns] = Manager(ns)

    # 操作被观察对象 实际上在操作管理器
    def register(self, ns, ob):
        if ns not in self._nss:
            raise Exception('this {} is invalid namespace'.format(ns))
        self._nss[ns].register(ob)

    def remove(self, ns, ob):
        return self._nss[ns].remove(ob)

    def change(self, data):
        # 此处实现可以更加紧凑，但是为了表达更简单，采用如下方式
        self._name = data['name']
        self._age = data['age']
        # 发生变化时  通过以下代码块 通过管理器 向观察对象传递改变
        for k in self._nss.keys():
            if k != 'all':
                data = self
            self._nss[k].notify(data)

    # 以下 property 为了实现 pull 模式
    @property
    def name(self):
        return self._name

    @property
    def age(self):
        return self._age


# 被观察对象的属性的管理器
# 观察者订阅了某些属性(或者类型)  当被观察对象属性发生变化时  即时向观察者 进行发送变化
class Manager:
    def __init__(self, subject):
        self.subject = subject
        self._observers = []

    def register(self, ob):
        self._observers.append(ob)

    def remove(self, ob):
        self._observers.remove(ob)

    # 当发生改变时  调用 观察者对象的更新方法
    def notify(self, data=None):
        for ob in self._observers:
            ob.update(data)


# 观察者1
class Look_one:
    def __init__(self):
        self._data = {}

    def update(self, data):
        self._data = data
        self.display()

    def display(self):
        print(u'总览显示面板：')
        for k, v in self._data.items():
            print(k + ': ' + str(v))


if __name__ == '__main__':
    import time

    # 生成一个可观察对象，支持('all', 'temperature', 'humidity', 'oxygen')的数据通知
    wd = WeatherData('all', 'temperature', 'humidity', 'oxygen')

    # 两个观察者对象
    od = OverviewDisplay()
    td = TemperatureDisplay()

    # 注册到可观察对象中，能获取数据更新
    wd.register('all', od)
    wd.register('temperature', td)

    # 更新数据，可观察对象将会自动更新数据
    wd.set_measurement({
        'clock': time.strftime("%Y-%m-%d %X", time.localtime()),
        'temperature': 20,
        'humidity': 60,
        'oxygen': 10
    })

    # 一秒后再次更新数据
    time.sleep(1)
    print('\n')
    wd.set_measurement({
        'clock': time.strftime("%Y-%m-%d %X", time.localtime()),
        'temperature': 21,
        'humidity': 58,
        'oxygen': 7
    })
    '''
总览显示面板：
clock: 2018-11-19 16:46:15
temperature: 20
humidity: 60
oxygen: 10
温度显示面板：
2018-11-19 16:46:15: 20


总览显示面板：
clock: 2018-11-19 16:46:16
temperature: 21
humidity: 58
oxygen: 7
温度显示面板：
2018-11-19 16:46:15: 20
2018-11-19 16:46:16: 21
    '''
