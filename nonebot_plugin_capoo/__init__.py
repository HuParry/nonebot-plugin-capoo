from .config import Config
from httpx import AsyncClient
from .download import *
import asyncio
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, GROUP, MessageSegment, Message
from nonebot.plugin import on_fullmatch
from nonebot.permission import SUPERUSER
from nonebot.log import logger
from nonebot import get_driver
import random
import os
from io import BytesIO
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name = "猫猫虫咖波图片发送",
    description = "发送capoo指令后bot会随机发出一张capoo的可爱表情包",
    usage = "使用命令：capoo",
    type="application",
    homepage="https://github.com/HuParry/nonebot-plugin-capoo",
    config=Config,
    supported_adapters = {"nonebot.adapters.onebot.v11"},
    extra = {
        "unique_name": "capoo",
        "example": "capoo",
        "author": "HuParry <huparry@outlook.com>",
        "version": "0.0.5",
    }
)
capoo_download = bool
driver = get_driver()
@driver.on_startup
async def _():
    global capoo_download
    capoo_download = Config.parse_obj(get_driver().config.dict()).capoo_download
    if capoo_download:
        logger.info("配置项选择了本地存储图片，正在检查资源文件...")
        asyncio.create_task(check_resources())
    else:
	    logger.info("配置项未选择本地存储图片，将通过url发送图片")

all_file_name = []

picture = on_fullmatch('capoo', permission=GROUP, priority=1, block=True)
@picture.handle()
async def pic():
    global capoo_download
    if capoo_download:
        global all_file_name
        if len(all_file_name) != capoo_list_len:
            all_file_name = os.listdir(str(capoo_path))
        img = capoo_path / random.choice(all_file_name)
        try:
            await picture.send(MessageSegment.image(img))
        except:
            await picture.send(f'capoo出不来了，稍后再试试吧~')
    else:
        async with AsyncClient() as client:
            resp = await client.get(f"https://git.acwing.com/HuParry/capoo/-/raw/master/capoo ({random.randint(1, capoo_list_len)}).gif", timeout=5.0)
        picbytes = BytesIO(resp.content).getvalue()
        try:
            await picture.send(MessageSegment.image(picbytes))
        except:
            await picture.send(f'capoo出不来了，稍后再试试吧~')
