from pydantic import BaseModel, Extra
from pathlib import Path
from nonebot import require, get_driver

require("nonebot_plugin_localstore")

from nonebot_plugin_localstore import get_data_dir

class Config(BaseModel, extra=Extra.ignore):
    capoo_path: str = get_data_dir("nonebot_plugin_capoo") #图片存储路径，自己指定或由localstore插件指定

capoo_path = Config.parse_obj(get_driver().config.dict()).capoo_path
capoo_path = Path(capoo_path) / 'capoo'
capoo_pic = "picture"
capoo_pic_path = capoo_path / capoo_pic  #从互联网下载的文件夹
capoo_filename = "randpic_capoo_{index}.gif"