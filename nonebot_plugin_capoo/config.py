from pydantic import BaseModel, Extra
from pathlib import Path

class Config(BaseModel, extra=Extra.ignore):
    capoo_download: bool = False        #是否开启本地图片存储，Ture为开启本地图片存储，下载源在国内，放心使用

capoo_path = Path() / "data" / "capoo"
capoo_pic = "picture"
capoo_pic2 = "your_picture"
capoo_pic_path = capoo_path / capoo_pic  #从 AC Git 下载的文件夹
capoo_pic2_path = capoo_path / capoo_pic2  #自己存储的文件夹
capoo_filename = "capoo ({index}).gif"