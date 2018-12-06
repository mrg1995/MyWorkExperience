# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'
import requests
import random
import json
import os
import logging.handlers

logger = logging.getLogger("kada_spider")
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s %(asctime)s %(filename)s[line:%(lineno)d] '
                              '%(levelname)s %(message)s')

handler = logging.handlers.RotatingFileHandler(
    filename=os.path.join(os.path.dirname(__file__),
                          '{name}.txt'.format(name="log")),  # 输出文件名
    maxBytes=1024 * 1024 * 5,  # 一个日志文件的大小上限 5m
    backupCount=5,  # 日志文件个数
    mode='a',  # 写日志模式
    encoding='utf-8'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


agentList = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36']

headers1 = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "cookie": "UM_distinctid=166ed38bb082a0-0657f25c656dbe-514d2f1f-144000-166ed38bb0a8a2; token=1654c18b5f7b3617d78b6e958f79fab458c824ef09b7e761795f8e40928c4ca4",
    "upgrade-insecure-requests": "1",
    "User-Agent": random.choice(agentList),
}

headers2 = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "cookie": "token=8f7f6db2e0a73f4ca0517bb5f075f28d1528db78fd472df15e8e8578bb53ad21",
    "upgrade-insecure-requests": "1",
    "user-agent": random.choice(agentList),
}

headers_list = [headers1, headers2]

proxy = None

path = './book/'

count = 0


# 获取 一本绘本的json数据
def get_json(id):
    global proxy
    retry_count = 5
    url = "https://kadateacher-service.hhdd.com/bookPage/getByBookId/{}".format(id)
    # 初始化首个代理地址
    if proxy == None:
        proxy = get_proxy()
    while retry_count > 0:
        try:
            # 当其中一个代理不能用时  更换一个代理重新下载
            if retry_count == 1:
                proxy = get_proxy()
                logger.info('原代理失效,更换新代理 {}'.format(proxy["http"]))
                retry_count = 5
            response = requests.get(url, headers=random.choice(headers_list), proxies=proxy)
            return json.loads(response.content.decode())
        except Exception:
            retry_count -= 1


# 下载绘本
def download_huiben(content):
    global count
    print(count)
    data = content["data"]
    try:
        book_id = data[0]["bookId"]
    except Exception:
        logger.info("跳过此本绘本")
        return
    mkdir(book_id)
    # logger.info('创建绘本文件夹{}'.format(book_id))
    for source in data:
        pageNumber = source["pageNumber"]
        img_url = source["backgroundUrl"]
        downloads(file_name='{}_{}.jpg'.format(book_id, pageNumber), url=img_url)
        # 获取到音频地址
        try:
            audio_url = json.loads(source["soundUrl"].replace('\\', ''))["soundUrl"]
            downloads(file_name='{}_{}.mp3'.format(book_id, pageNumber), url=audio_url)
        except Exception:
            logger.info("此页无音频文件")
    count += 1


# 下载
def downloads(file_name, url):
    global proxy
    retry_count = 5
    down_count = 0
    while retry_count > 0:
        try:
            # 当其中一个代理不能用时  更换一个代理重新下载
            if retry_count == 1:
                proxy = get_proxy()
                logger.info('原代理失效,更换新代理 {}'.format(proxy["http"]))
                retry_count = 5
            logger.info('开始下载  {}'.format(url))
            response = requests.get(url, headers=random.choice(headers_list), proxies=proxy)
            # 返回404 的话直接跳过
            if response.status_code == 404:
                logger.info('下载失败,无此资源')
                return
            # 返回其他错误 继续重试
            if response.status_code != 200:
                logger.info('下载失败,开始重试')
                retry_count -= 1
                # 增加下载次数控制  防止是咔哒服务器 资源的问题
                down_count += 1
                if down_count >= 10:
                    return
                continue

            with open(file_name, 'wb') as f:
                f.write(response.content)
            logger.info('下载成功,目前使用代理为{}'.format(proxy['http']))
            return
        except Exception:
            retry_count -= 1


# 获取代理
def get_proxy():
    return {"http": "http://{}".format(requests.get("http://123.207.35.36:5010/get/",
                                                    headers={'User-Agent': random.choice(agentList)}).content.decode())}


# 创建绘本文件夹
def mkdir(book_id):
    ab_path = path + str(book_id)
    if str(book_id) not in os.listdir(path):
        os.makedirs(ab_path)
    os.chdir(ab_path)


if __name__ == '__main__':
    if not os.path.exists(path):
        os.mkdir(path)
    for i in range(325):
        download_huiben(get_json(i))
        os.chdir(os.path.split(os.path.realpath(__file__))[0])