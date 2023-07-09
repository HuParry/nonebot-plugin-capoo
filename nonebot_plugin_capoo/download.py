import asyncio
import httpx

from nonebot.log import logger
from nonebot import get_driver
import sqlite3
import hashlib
import os
from .sqlite import check_md5
from .config import capoo_pic_path, capoo_path, \
    capoo_filename, capoo_pic, capoo_pic2_path, capoo_pic2

capoo_list_len = 456
async def download_url(url: str) -> bytes:
    async with httpx.AsyncClient() as client:
        for i in range(3):
            try:
                resp = await client.get(url, timeout=20)
                resp.raise_for_status()
                return resp.content
            except Exception as e:
                logger.warning(f"Error downloading {url}, retry {i}/3: {e}")
                await asyncio.sleep(3)
    raise Exception(f"{url} 下载失败！")


def resource_url(path: str) -> str:
    return f"https://git.acwing.com/HuParry/capoo/-/raw/master/{path}"

async def download_resources(path: str) -> bytes:
    return await download_url(resource_url(path))

async def check_resources():
    if not capoo_pic_path.exists():
        logger.info(f"未找到capoo文件夹，准备创建/capoo/picture文件夹...")
        capoo_pic_path.mkdir(parents=True, exist_ok=True)
    
    if not capoo_pic2_path.exists():
        logger.info(f"未找到capoo2文件夹，准备创建/capoo/your_picture文件夹...")
        capoo_pic2_path.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(capoo_path / 'md5.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Picture (
            md5 TEXT PRIMARY KEY,
            img_url TEXT
        )
    ''')
    capoo_pic2_list = os.listdir(str(capoo_pic2_path))

    for i in range(1, capoo_list_len + 1) :
        file_name = capoo_filename.format(index=str(i))
        file_path = capoo_pic_path / file_name
        if file_path.exists():
            with file_path.open("rb") as f:
                data = f.read()
            fmd5 = hashlib.md5(data).hexdigest()
            check_md5(conn, cursor, fmd5, f"{capoo_pic}/{capoo_filename.format(index=str(i))}")
            continue
        logger.info(f"Downloading {file_name} ...")
        try:
            data = await download_resources(file_name)
            fmd5 = hashlib.md5(data).hexdigest()
            
            if (not check_md5(conn, cursor, fmd5, f"{capoo_pic}/{capoo_filename.format(index=str(i))}")) :
                logger.info(f"文件夹中有相同的图片，本张照片跳过")
                continue

            with file_path.open("wb") as f:
                f.write(data)

        except Exception as e:
            logger.warning(str(e))
    
    for file_name in capoo_pic2_list:
        with file_path.open("rb") as f:
            data = f.read()
        fmd5 = hashlib.md5(data).hexdigest()
        check_md5(conn, cursor, fmd5, f"{capoo_pic2}/{file_name}")
