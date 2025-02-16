import datetime
import os

from nonebot import logger
from sqlalchemy import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine


class KikaikenDatabase:
    engine: AsyncEngine

    def set_engine(self, engine: AsyncEngine):
        self.engine = engine


kdb = KikaikenDatabase()


async def sqlite_connect():
    logger.info("- 初始化数据库连接")
    # 首先检查配置文件中是否包含对应的配置项，如果不存在则使用默认值
    sqlite_path = os.getenv("BACKUP_PATH", "")
    if not sqlite_path:  # 如果配置项不存在，尝试检测目录下的是否存在以后缀名.kbp结尾的文件，有则使用第一个
        for file in os.listdir("."):
            if file.endswith(".kbp"):
                sqlite_path = file
                break
        else:  # 如果不存在，则使用默认值
            # 将当前的日期时间格式化成文件名
            sqlite_path = f"kikaiken_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.kbp"
    # 通过SQLAlchemy连接数据库
    logger.debug(f"当前使用的数据库文件为：{sqlite_path}")
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{sqlite_path}",
        poolclass=AsyncAdaptedQueuePool,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800
    )
    kdb.set_engine(engine)
    logger.success("Done!")


def get_engine():
    return kdb.engine


async def release_engine():
    await kdb.engine.dispose()
