from arclet.alconna import Alconna, Subcommand, Option, Arparma
from nonebot import on_type, get_driver, logger
from nonebot.adapters.onebot.v11 import PrivateMessageEvent
from nonebot.permission import SUPERUSER
from nonebot_plugin_alconna import on_alconna, AlconnaMatches

from kikaiken.core.data_manager import auto_create_check, list_keys
from kikaiken.core.db_connect import sqlite_connect, release_engine
from kikaiken.core.talk import talk_v1
from kikaiken.core.text import text_global_exception

driver = get_driver()
apikey_cmd = on_alconna(
    Alconna(
        "apikey",
        Subcommand(
            "list",
            Option(
                "-s|--show",
            )
        ),
    ),
    use_cmd_sep=True,
    use_cmd_start=True,
    priority=10,
    block=True,
    permission=SUPERUSER,
)
private_talking = on_type(PrivateMessageEvent)


@driver.on_startup
async def _():
    logger.info("开始初始化 kikaiken 服务...")
    # 初始化数据库连接
    await sqlite_connect()
    await auto_create_check()


@driver.on_shutdown
async def _():
    # 释放数据库连接
    await release_engine()


@apikey_cmd.handle()
async def _(event: PrivateMessageEvent, result: Arparma = AlconnaMatches()):
    if result.find("list"):
        is_shown = False
        if result.find("list.show"):
            is_shown = True
        # 获取apikey列表
        keys = await list_keys()
        if keys:
            for key in keys:
                if is_shown:
                    await apikey_cmd.send(
                        f"{key.model_type} {key.model_name} {key.api_key} {key.notice}"
                    )
                else:
                    await apikey_cmd.send(f"{key.model_type} {key.model_name}")
    await apikey_cmd.finish(text_global_exception())


@private_talking.handle()
async def _(event: PrivateMessageEvent):
    res = await talk_v1(event.user_id, event.get_plaintext())
    await private_talking.finish(res)
