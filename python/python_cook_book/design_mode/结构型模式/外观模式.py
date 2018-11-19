# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'

# 提供了一个统一的接口，用来访问子系统中的一群接口。外观定义了一个高层接口，让子系统更容易使用。


class HardWare(object):
    def power_on(self):
        print('上电')

    def bootloader(self):
        print('bootloader 启动')

    def power_off(self):
        print('断电')


class OperatingSystem(object):
    def load_kernel(self):
        print('加载内核')

    def load_image(self):
        print('加载镜像')

    def exit_os(self):
        print('退出操作系统')


class SoftWare(object):
    def load_app(self):
        print('加载应用程序')

    def exit_app(self):
        print('退出应用程序')


class Computer(object):
    def __init__(self):
        self.hw = HardWare()
        self.os = OperatingSystem()
        self.sw = SoftWare()

    def boot(self):
        self.hw.power_on()
        self.hw.bootloader()
        self.os.load_kernel()
        self.os.load_image()
        self.sw.load_app()

    def shut_down(self):
        self.sw.exit_app()
        self.os.exit_os()
        self.hw.power_off()


if __name__ == '__main__':
    computer = Computer()

    print('开机')
    computer.boot()

    print('\n关机')
    computer.shut_down()
