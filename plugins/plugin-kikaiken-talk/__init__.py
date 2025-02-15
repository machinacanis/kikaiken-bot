from nonebot import on_type, get_driver, logger
from nonebot.adapters.onebot.v11 import PrivateMessageEvent

from kikaiken.core.connect import sqlite_connect, release_engine
from kikaiken.core.talk import talk

driver = get_driver()
private_talking = on_type(PrivateMessageEvent)


@driver.on_startup
async def _():
    logger.info("开始初始化 kikaiken 服务...")
    # 初始化数据库连接
    sqlite_connect()


@driver.on_shutdown
async def _():
    # 释放数据库连接
    release_engine()


@private_talking.handle()
async def _(event: PrivateMessageEvent):
    res = await talk(event.user_id, event.get_plaintext())
    await private_talking.finish(res)
