import random
import os
import requests
import win32api
import win32con
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver import ActionChains
from multiprocessing import Pool
import math


# 失败重试装饰器
def retry(tries, delay=0.2, backoff=2):
    if backoff <= 1:
        raise ValueError("backoff must be greater than 1")
    tries = math.floor(tries)
    if tries < 0:
        raise ValueError("tries must be 0 or greater")
    if delay <= 0:
        raise ValueError("delay must be greater than 0")

    def deco_retry(f):
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay  # make mutable
            rv = f(*args, **kwargs)  # first attempt
            while mtries > 0:
                if rv:  # Done on success
                    return rv
                mtries -= 1  # consume an attempt
                time.sleep(mdelay)  # wait...
                mdelay *= backoff  # make future wait longer
                rv = f(*args, **kwargs)  # Try again
            return False  # Ran out of tries :-(

        return f_retry  # true decorator -> decorated function

    return deco_retry  # @retry(arg[, ...]) -> true decorator


# 使用谷歌无头浏览器
options = webdriver.ChromeOptions()

# options.add_argument('--headless')

# options.add_argument('window-size=1200x600')
agentList = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER']


class KaDaSpider(object):

    def __init__(self, url, path):
        self.url = url
        # self.driver = webdriver.Chrome(chrome_options=options)
        self.driver = webdriver.Chrome(options=options)
        self.path = path
        self.audio = None
        self.dir_name = None
        self.position = None
        self.temp = "".split("/")[0]


    # 普通下载
    def download(self, img_url, audio_url, name):
        img = requests.get(img_url, headers={'User-Agent': random.choice(agentList)})
        with open(name + ".jpg", 'wb') as f:
            f.write(img.content)
        audio = requests.get(audio_url, headers={'User-Agent': random.choice(agentList)})
        with open(name + ".mp3", "wb") as vd:
            vd.write(audio.content)

    # 单进程抓取
    def get_kada_story(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.first_step()
        self.count = int(self.driver.find_element_by_xpath('//div[@class="book-ctrl"]/div/div[position()=2]').text[2:])
        mk = 0
        for position in range(self.count):
            try:
                img_url, audio_url, name = self.get_url(position)
            except Exception as e:
                continue
            if mk != 1:
                dir_name = name[:-2]
                os.chdir(self.path)
                if dir_name not in os.listdir(self.path):
                    os.mkdir(dir_name)
                os.chdir(self.path + dir_name)
                mk += 1
            self.audio = audio_url
            self.download(img_url, audio_url, name)
            time.sleep(0.3)
            self.change_page()
        self.driver.close()

    # 初始化   到达页面  并暂停阅读
    def first_step(self):
        try:
            if not os.path.exists(self.path):
                os.mkdir(self.path)
        except Exception:
            print("")
        self.driver.get(self.url)
        time.sleep(5)
        ac = self.driver.find_element_by_xpath("//div[@class='book-loading']/img")
        button = self.driver.find_element_by_xpath("//div[@class='book-ctrl']/button")
        ActionChains(self.driver).move_to_element(ac).click(ac).perform()
        time.sleep(0.5)
        ActionChains(self.driver).move_to_element(button).click(button).perform()

    # 从当前页面 获取图片 音频 地址
    def get_url(self, position):
        audio_url = self.driver.find_element_by_xpath("//audio").get_attribute("src")
        img = self.driver.find_element_by_xpath(
            '//div[@id="bb-bookblock"]/div[position()={}]//img'.format(position))
        img_url = img.get_attribute("src")
        name = img.get_attribute("alt")
        return img_url, audio_url, name

    # 更换页面
    def change_page(self):
        # change = self.driver.find_element_by_xpath("//div[@class='book-ctrl']//input")
        # ActionChains(self.driver).drag_and_drop_by_offset(source=change, xoffset=-15, yoffset=0).perform()
        x = random.randint(910,925)
        y = random.randint(300,600)
        duke = random.uniform(0,0.1)
        length = random.randint(-600,-400)
        win32api.SetCursorPos((x, y))
        time.sleep(0.2)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y)
        time.sleep(duke)
        # win32api.mouse_event(win32con.MOUSE_MOVED, -150, 0)
        # 先快后慢效果控制鼠标
        pyautogui.moveRel(length,0,duke,pyautogui.easeInQuad)
        time.sleep(duke)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    # 获取 最大页面数量
    def get_count(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.first_step()
        self.count = int(self.driver.find_element_by_xpath('//div[@class="book-ctrl"]/div/div[position()=2]').text[2:])

    # 获取 当前页码
    @retry(4)  # 失败重试4次
    def get_page(self):
        try:
            button = self.driver.find_element_by_xpath("//div[@class='book-ctrl']/button")
            ActionChains(self.driver).click(button).perform()
            page = self.driver.find_element_by_xpath('//div[@class="book-ctrl"]/div/div[position()=2]').text
            page = page.split("/", 1)[0]
            if page == self.temp:
                return False
        except Exception as e:
            # print(str(e))
            return False
        return int(page)

    # 创建 绘本文件夹
    def mkdir(self):
        name = self.driver.find_element_by_xpath(
            '//div[@id="bb-bookblock"]/div[position()={}]//img'.format(1)).get_attribute("alt")
        self.dir_name = name[:-2]
        self.ab_path = self.path + self.dir_name
        # os.chdir(self.path)
        if self.dir_name not in os.listdir(self.path):
            os.makedirs(self.ab_path)
        os.chdir(self.ab_path)

    # 获取所有 图片 音频 下载地址
    def get_name_url(self):
        download_url_list = []
        while True:
            time.sleep(0.6)
            page = self.get_page()
            # 当获取页码失败时
            if not page:
                print('未获取到页码')
                continue
            # 当前页码更新时
            if self.position != page:
                self.position = page
                try:
                    img_url, audio_url, name = self.get_url(str(self.position))
                except Exception as e:
                    continue
                download_url_list.append((name + ".jpg", img_url))
                download_url_list.append((name + ".mp3", audio_url))
                print(self.position, self.count)
                self.change_page()
            # 当到最后一页时
            elif int(self.position) == self.count:
                try:
                    img_url, audio_url, name = self.get_url(self.position)
                    download_url_list.append((name + ".jpg", img_url))
                    download_url_list.append((name + ".mp3", audio_url))
                except Exception as e:
                    self.driver.close()
                    break
                print(download_url_list)
                self.driver.close()
                break
            # 当页码一样时
            else:
                # print(self.position, self.count, "翻页")
                self.change_page()
        return download_url_list


def download(file_name, url):
    # 抓取速度过快会导致返回的数据有误
    time.sleep(0.2)
    print('开始下载{}'.format(file_name))
    response = requests.get(url, headers={'User-Agent': random.choice(agentList)})
    with open(file_name, 'wb') as f:
        f.write(response.content)
    return "{}下载完成".format(file_name)


def callback(result):
    print(result)


# 多进程抓取
def asy_download(download_url_list):
    pool = Pool(3)
    for name, url in download_url_list:
        pool.apply_async(func=download, args=(name, url), callback=callback)
    pool.close()
    pool.join()


if __name__ == '__main__':
    # 路径
    path = './book/'
    # 初始地址
    url = "https://cdn.hhdd.com/frontend/index.html#/single-book-info/f3dcc1592ff35c4ac7631edb38265c3f"
    # https://cdn.hhdd.com/frontend/index.html#/single-book-info/5e30bcd1f8f09b8b33ee1d57e2e0d7b1
    # https://cdn.hhdd.com/frontend/index.html#/single-book-info/f3dcc1592ff35c4ac7631edb38265c3f
    color_book = KaDaSpider(url=url, path=path)

    time.sleep(2)
    win32api.SetCursorPos((900, 300))
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 900, 300)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 900, 300)

    color_book.get_count()
    color_book.mkdir()
    url_list = color_book.get_name_url()
    di = {}
    for key, value in url_list:
        di[key] = value
    url_list.clear()
    for key, value in di.items():
        url_list.append((key, value))

    asy_download(url_list)
