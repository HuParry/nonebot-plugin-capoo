from .config import Config, capoo_path
from httpx import AsyncClient
from .download import *
import asyncio
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11 import GROUP
from nonebot.plugin import on_fullmatch
from nonebot.log import logger
from nonebot import get_driver
import random
import os
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
	name = "猫猫虫咖波图片发送",
	description = "发送capoo指令后bot会随机发出一张capoo的可爱表情包",
	usage = "使用命令：capoo",
	type="application",
	homepage="https://github.com/HuParry/nonebot-plugin-capoo",
	config=Config,
	supported_adapters = {"nonebot.adapters.onebot.v11"},
)

driver = get_driver()
@driver.on_startup
async def _():
	logger.info("正在检查资源文件...")
	await check_resources()

picture = on_fullmatch('capoo', permission=GROUP, priority=1, block=True)
@picture.handle()
async def pic():
	capoo_pic_list = os.listdir(capoo_pic_path)
	filename = random.choice(capoo_pic_list)
	img = capoo_pic_path / filename
	try:
		await picture.send(MessageSegment.image(img))
	except Exception as e:
		logger.warning(e)
		await picture.send(f'capoo出不来了，稍后再试试吧~')