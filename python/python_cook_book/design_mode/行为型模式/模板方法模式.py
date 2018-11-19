# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'
# 在一个方法中定义一个算法的骨架，而将一些步骤延迟到子类中。模板方法使得子类可以在不改变算法结构的情况下，重新定义算法中的某些步骤。

from abc import ABCMeta, abstractmethod

# 一部分公有的方法放在抽象基类中  不同继承该基类的子类在不改变算法结构的情况下  覆写方法
class CaffeineBeverage(metaclass=ABCMeta):
    def make_beverage(self):
        self.boil_water()
        self.brew()
        self.pour_in_cup()
        if (self.customer_want_condiments()):
            self.add_condiments()

    def boil_water(self):
        print('把水烧开')

    def pour_in_cup(self):
        print('倒入杯子中')

    def customer_want_condiments(self):
        # hook
        return False

    @abstractmethod
    def brew(self):
        pass

    @abstractmethod
    def add_condiments(self):
        pass


class Tea(CaffeineBeverage):
    def brew(self):
        print('用沸水浸泡茶叶')

    def customer_want_condiments(self):
        return True

    def add_condiments(self):
        print('添加柠檬')


class Coffee(CaffeineBeverage):
    def brew(self):
        print('用沸水冲泡咖啡')

    def customer_want_condiments(self):
        return False

    def add_condiments(self):
        print('添加牛奶和糖')


if __name__ == '__main__':
    print('制作咖啡：')
    coffee = Coffee()
    coffee.make_beverage()
    print('\n制作茶：')
    tea = Tea()
    tea.make_beverage()

