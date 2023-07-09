from .config import Config, capoo_path, capoo_pic2_path, capoo_pic2
from httpx import AsyncClient
from .download import *
import asyncio
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, GROUP, MessageSegment, Message
from nonebot.plugin import on_fullmatch, on_command
from nonebot.permission import SUPERUSER
from nonebot.log import logger
from nonebot import get_driver
import random
import os
from io import BytesIO
from nonebot.plugin import PluginMetadata
from nonebot.params import Arg

__plugin_meta__ = PluginMetadata(
    name = "猫猫虫咖波图片发送",
    description = "发送capoo指令后bot会随机发出一张capoo的可爱表情包",
    usage = "使用命令：capoo",
    type="application",
    homepage="https://github.com/HuParry/nonebot-plugin-capoo",
    config=Config,
    supported_adapters = {"nonebot.adapters.onebot.v11"},
)
capoo_download = Config.parse_obj(get_driver().config.dict()).capoo_download
driver = get_driver()
@driver.on_startup
async def _():
    global capoo_download
    if capoo_download:
        logger.info("配置项选择了本地存储图片，正在检查资源文件...")
        asyncio.create_task(check_resources())
    else:
	    logger.info("配置项未选择本地存储图片，将通过url发送图片")

picture = on_fullmatch('capoo', permission=GROUP, priority=1, block=True)
@picture.handle()
async def pic():
    global capoo_download
    if capoo_download:
        conn = sqlite3.connect(capoo_path / 'md5.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Picture (
                md5 TEXT PRIMARY KEY,
                img_url TEXT
            )
        ''')
        cursor.execute('SELECT * FROM Picture ORDER BY RANDOM() limit 1')
        status = cursor.fetchone()
        if status is None:
            await picture.finish('当前还没有图片!')
        file_name = status[1]
        img = capoo_path / file_name
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

add = on_fullmatch('添加capoo', permission=SUPERUSER, priority=1, block=True)
@add.got("pic", prompt="请发送图片！")
async def add_pic(pic_list: Message = Arg('pic')):
    if capoo_download == False:
        return
    
    conn = sqlite3.connect(capoo_path / 'md5.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Picture (
            md5 TEXT PRIMARY KEY,
            img_url TEXT
        )
    ''')

    for pic in pic_list:
        if pic.type != 'image':
            await add.send(pic + MessageSegment.text("\n输入格式有误，请重新触发指令！"), at_sender=True)
            continue
        pic_url = pic.data['url']

        async with AsyncClient() as client:
            resp = await client.get(pic_url, timeout=5.0)
        
        try:
            resp.raise_for_status()
        except:
            await add.send(
                    pic +
                    MessageSegment.text('\n保存出错了，这张请重试')
                )
            continue
            
        data = resp.content
        fmd5 = hashlib.md5(data).hexdigest()

        capoo_cur_picnum = len( os.listdir(str(capoo_pic2_path)) )
        if not check_md5(conn, cursor, fmd5, capoo_pic2 + str(capoo_cur_picnum + 1)) :
            await add.send(pic + 
                            Message('\n这张已经有了，不能重复添加！')   
                        )
        else:
            capoo_cur_picnum = capoo_cur_picnum + 1
            file_name = capoo_filename.format(index=str(capoo_cur_picnum))
            file_path = capoo_pic2_path / file_name
            
            try:
                with file_path.open("wb") as f:
                    f.write(data)
                await add.send(pic + Message("\n导入成功！"), at_sender = True)
            except:
                await add.send(pic + Message("\n导入失败！"), at_sender = True)