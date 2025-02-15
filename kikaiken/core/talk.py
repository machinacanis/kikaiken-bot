# 提供一个talk函数接口用于封装对话功能
from nonebot import logger


async def talk(uid: int, content: str):
    logger.info(f"用户 {uid} 发送了消息：{content}")
    return content
