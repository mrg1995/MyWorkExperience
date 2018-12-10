from huey import crontab

from config import huey  # import the huey we instantiated in config.py
from models import database, Content, Hall, Rank
from tiobe_spider import Tiobe


# @huey.task()
@huey.periodic_task(crontab(day='*'))  # 每天爬取
def sub():
    database.create_tables([Content, Rank, Hall], safe=True)

    RSS_URL = 'https://www.tiobe.com/tiobe-index/rss.xml'
    INDEX_URL = 'https://www.tiobe.com/tiobe-index/'

    t = Tiobe(RSS_URL, INDEX_URL)
    # t.fetch(force=True)
    t.fetch()


# @huey.periodic_task(crontab(minute='*'))
# def print_time():
#     print(datetime.datetime.day)
