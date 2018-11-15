# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'

# 对不同的对象 进行不同的操作


"""访问者模式"""
# 轮子,引擎, 车身这些定义好了都不需要变动
class Wheel:
    def __init__(self, name):
        self.name = name
    def accept(self, visitor):
        # 每个visitor是同样的，但是其中的方法是不一样的，比如这里是visitWheel，
        # 然后传入了self，想想？他其实想做什么就能做什么
        visitor.visitWheel(self)

class Engine:
    def accept(self, visitor):
        visitor.visitEngine(self)

class Body:
    def accept(self, visitor):
        visitor.visitBody(self)

# 我们要组合成车
class Car:
    def __init__(self):
        self.engine = Engine()
        self.body   = Body()
        self.wheels = [ Wheel("front left"), Wheel("front right"),
                        Wheel("back left") , Wheel("back right") ]

    # 这个也不需要在动，他只是上面部件的组合，只是做了属性的委托
    def accept(self,visitor):
        visitor.visitCar(self)
        self.engine.accept(visitor)
        self.body.accept(visitor)
        for wheel in self.wheels:
            wheel.accept(visitor)

# 这个才是我们的访问者，每次的修改都在这里面
class PrintVisitor:
    def visitWheel(self, wheel):
        print ("Visiting "+wheel.name+" wheel")
    def visitEngine(self, engine):
        print ("Visiting engine")
    def visitBody(self, body):
        print ("Visiting body")
    def visitCar(self, car):
        print ("Visiting car")

if __name__ == '__main__':
    car = Car()
    visitor = PrintVisitor()
    car.accept(visitor)