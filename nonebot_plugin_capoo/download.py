import asyncio
import httpx
from pathlib import Path
from nonebot.log import logger
from nonebot import get_driver

capoo_path = Path() / "data" / "capoo"
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
    if capoo_path.exists():
        return
    logger.info(f"未找到capoo文件夹，准备创建/data/capoo文件夹...")
    capoo_path.mkdir(parents=True, exist_ok=True)
    for i in range(1, capoo_list_len + 1) :
        file_name = f"capoo ({i}).gif"
        file_path = capoo_path / file_name
        if file_path.exists():
            continue
        logger.info(f"Downloading {file_name} ...")
        try:
            data = await download_resources(file_name)
            with file_path.open("wb") as f:
                f.write(data)
        except Exception as e:
            logger.warning(str(e))