#   Desc    :   入口

# main.py
from gevent import monkey

monkey.patch_all()

from config import huey  # import our "huey" object
from tasks import sub  # count  import our task

if __name__ == '__main__':
    huey.flush()
    # for i in range(100):
    #     sub()
    sub()
