from huey import RedisHuey

huey = RedisHuey()

DATABASE_URL = 'mysql://root:@127.0.0.1:3306/tiobe?charset=utf8mb4'