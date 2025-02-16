import datetime

from nonebot import logger
from sqlalchemy import Column, Integer, String, select, insert, delete, Boolean, Date, update, DateTime, desc
from sqlalchemy.ext.declarative import declarative_base

from kikaiken.core.db_connect import get_engine

Base = declarative_base()


async def auto_create_check():
    """
    自动检查并创建表结构
    """
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class KikaikenUserRecord(Base):
    __tablename__ = "kikaiken_user_record"
    id = Column(Integer, primary_key=True, autoincrement=True)
    qid = Column(Integer, nullable=False)
    record_time = Column(DateTime, nullable=False, default=datetime.datetime.now())
    content = Column(String(255), nullable=False)


async def add_record(qid: int, content: str):
    engine = get_engine()
    add = insert(KikaikenUserRecord).values(qid=qid, content=content)
    try:
        async with engine.begin() as conn:
            await conn.execute(add)
            await conn.commit()
            return True
    except Exception as e:
        logger.error(f"添加失败：{e}")
        return False


async def query_record(qid: int, count: int):
    engine = get_engine()
    query = select(KikaikenUserRecord).where(KikaikenUserRecord.qid == qid).order_by(
        desc(KikaikenUserRecord.record_time)).limit(count)
    try:
        async with engine.begin() as conn:
            result = await conn.execute(query)
            return result.fetchall()
    except Exception as e:
        logger.error(f"查询失败：{e}")
        return False


class ConfigPersistence(Base):
    """
    配置持久化表，用于保存一些全局设置
    """
    __tablename__ = "config_persistence"
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    value = Column(String)


async def get_config(key: str):
    """
    获取配置
    """
    engine = get_engine()
    query = select(ConfigPersistence).where(ConfigPersistence.key == key)
    try:
        async with engine.begin() as conn:
            await conn.execute(query)
            result: ConfigPersistence = await conn.fetchone()
            return result
    except Exception as e:
        logger.error(f"查询失败：{e}")
        return None


async def set_config(key: str, value: str):
    """
    设置配置
    """
    engine = get_engine()
    update_query = update(ConfigPersistence).where(ConfigPersistence.key == key).values(value=value)
    try:
        async with engine.begin() as conn:
            await conn.execute(update_query)
            await conn.commit()
            return True
    except Exception as e:
        logger.error(f"设置失败：{e}")
        return False


class LLMAPIKey(Base):
    __tablename__ = "llm_apikey"
    id = Column(Integer, primary_key=True)
    model_type = Column(String)
    model_name = Column(String)
    api_key = Column(String)
    notice = Column(String)


async def list_keys():
    """
    列出所有key
    """
    engine = get_engine()
    query = select(LLMAPIKey)
    try:
        async with engine.begin() as conn:
            await conn.execute(query)
            result: list[LLMAPIKey] = await conn.fetchall()
            return result
    except Exception as e:
        logger.error(f"查询失败：{e}")
        return None


async def add_key(model_type: str, model_name: str, api_key: str, notice: str):
    """
    添加key
    """
    engine = get_engine()
    add = insert(LLMAPIKey).values(
        model_type=model_type,
        model_name=model_name,
        api_key=api_key,
        notice=notice
    )
    try:
        async with engine.begin() as conn:
            await conn.execute(add)
            await conn.commit()
            return True
    except Exception as e:
        logger.error(f"添加失败：{e}")
        return False


async def delete_key(key_id: int):
    """
    删除key
    """
    engine = get_engine()
    delete_query = delete(LLMAPIKey).where(LLMAPIKey.id == key_id)
    try:
        async with engine.begin() as conn:
            await conn.execute(delete_query)
            await conn.commit()
            return True
    except Exception as e:
        logger.error(f"删除失败：{e}")
        return False


class KikaikenUser(Base):
    __tablename__ = "kikaiken_user"
    id = Column(Integer, primary_key=True)
    qid = Column(Integer)
    nickname = Column(String)
    permission_group = Column(Integer)
    is_subscribed = Column(Boolean)  # 是否启用订阅服务
    join_date = Column(Date)
    lucky = Column(Integer)  # 幸运值，这个值也会影响一些其他的逻辑
    last_sign_date = Column(Date)
    coin = Column(Integer)
    last_activity_date = Column(Date)
    backpack = Column(String)


async def create_user(qid: int, nickname: str = None, permission_group: int = 0, is_subscribed: bool = True,
                      lucky: int = 0, last_sign_date: Date = None, coin: int = 0,
                      last_activity_date: Date = None):
    """
    创建用户
    """
    engine = get_engine()
    add = insert(KikaikenUser).values(
        qid=qid,
        nickname=nickname,
        permission_group=permission_group,
        is_subscribed=is_subscribed,
        join_date=datetime.datetime.now(),
        lucky=lucky,
        last_sign_date=last_sign_date,
        coin=coin,
        last_activity_date=last_activity_date
    )
    try:
        async with engine.begin() as conn:
            await conn.execute(add)
            await conn.commit()
            return True
    except Exception as e:
        logger.error(f"添加失败：{e}")
        return False


async def find_user_by_qid(qid: int):
    """
    通过qq号查找用户
    """
    engine = get_engine()
    query = select(KikaikenUser).where(KikaikenUser.qid == qid)
    try:
        async with engine.begin() as conn:
            await conn.execute(query)
            result: KikaikenUser = await conn.fetchone()
            return result
    except Exception as e:
        logger.error(f"查询失败：{e}")
        return None


async def set_nickname(qid: int, nickname: str):
    """
    设置用户昵称
    """
    engine = get_engine()
    update_query = update(KikaikenUser).where(KikaikenUser.qid == qid).values(nickname=nickname)
    try:
        async with engine.begin() as conn:
            await conn.execute(update_query)
            await conn.commit()

            await add_record(qid, f"修改昵称为：{nickname}")

            return True
    except Exception as e:
        logger.error(f"更新失败：{e}")
        return False


async def set_permission_group(qid: int, permission_group: int):
    """
    设置用户权限组
    """
    engine = get_engine()
    update_query = update(KikaikenUser).where(KikaikenUser.qid == qid).values(permission_group=permission_group)
    try:
        async with engine.begin() as conn:
            await conn.execute(update_query)
            await conn.commit()

            await add_record(qid, f"权限组被修改为：{permission_group}")

            return True
    except Exception as e:
        logger.error(f"更新失败：{e}")
        return False


async def enable_subscribe(qid: int):
    """
    启用订阅服务
    """
    engine = get_engine()
    update_query = update(KikaikenUser).where(KikaikenUser.qid == qid).values(is_subscribed=True)
    try:
        async with engine.begin() as conn:
            await conn.execute(update_query)
            await conn.commit()

            await add_record(qid, "订阅服务已启用")

            return True
    except Exception as e:
        logger.error(f"更新失败：{e}")
        return False


async def disable_subscribe(qid: int):
    """
    禁用订阅服务
    """
    engine = get_engine()
    update_query = update(KikaikenUser).where(KikaikenUser.qid == qid).values(is_subscribed=False)
    try:
        async with engine.begin() as conn:
            await conn.execute(update_query)
            await conn.commit()

            await add_record(qid, "订阅服务已禁用")

            return True
    except Exception as e:
        logger.error(f"更新失败：{e}")
        return False


async def set_lucky(qid: int, lucky: int):
    """
    设置用户幸运值
    """
    engine = get_engine()
    update_query = update(KikaikenUser).where(KikaikenUser.qid == qid).values(lucky=lucky)
    try:
        async with engine.begin() as conn:
            await conn.execute(update_query)
            await conn.commit()
            return True
    except Exception as e:
        logger.error(f"更新失败：{e}")
        return False


async def set_sign_date(qid: int, sign_date: Date):
    """
    设置用户签到日期
    """
    engine = get_engine()
    update_query = update(KikaikenUser).where(KikaikenUser.qid == qid).values(last_sign_date=sign_date)
    try:
        async with engine.begin() as conn:
            await conn.execute(update_query)
            await conn.commit()
            return True
    except Exception as e:
        logger.error(f"更新失败：{e}")
        return False


async def set_coin(qid: int, coin: int):
    """
    设置用户硬币
    """
    engine = get_engine()
    update_query = update(KikaikenUser).where(KikaikenUser.qid == qid).values(coin=coin)
    try:
        async with engine.begin() as conn:
            await conn.execute(update_query)
            await conn.commit()
            return True
    except Exception as e:
        logger.error(f"更新失败：{e}")
        return False


async def add_coin(qid: int, coin: int):
    """
    增加用户硬币
    """
    engine = get_engine()
    update_query = update(KikaikenUser).where(KikaikenUser.qid == qid).values(coin=KikaikenUser.coin + coin)
    try:
        async with engine.begin() as conn:
            await conn.execute(update_query)
            await conn.commit()

            await add_record(qid, f"获得硬币：{coin}")

            return True
    except Exception as e:
        logger.error(f"更新失败：{e}")
        return False


async def delete_coin(qid: int, coin: int):
    """
    删除用户硬币
    """
    engine = get_engine()
    update_query = update(KikaikenUser).where(KikaikenUser.qid == qid).values(coin=KikaikenUser.coin - coin)
    try:
        async with engine.begin() as conn:
            await conn.execute(update_query)
            await conn.commit()

            await add_record(qid, f"失去硬币：{coin}")

            return True
    except Exception as e:
        logger.error(f"更新失败：{e}")
        return False


async def consume_coin(qid: int, coin: int):
    """
    消费用户硬币
    """
    engine = get_engine()
    update_query = update(KikaikenUser).where(KikaikenUser.qid == qid).values(coin=KikaikenUser.coin - coin)
    try:
        async with engine.begin() as conn:
            await conn.execute(update_query)
            await conn.commit()

            await add_record(qid, f"消费硬币：{coin}")

            return True
    except Exception as e:
        logger.error(f"更新失败：{e}")
        return False


async def update_last_activity_date(qid: int):
    """
    更新用户最后活跃时间
    """
    engine = get_engine()
    update_query = update(KikaikenUser).where(KikaikenUser.qid == qid).values(
        last_activity_date=datetime.datetime.now())
    try:
        async with engine.begin() as conn:
            await conn.execute(update_query)
            await conn.commit()
            return True
    except Exception as e:
        logger.error(f"更新失败：{e}")
        return False
