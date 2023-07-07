from pydantic import BaseModel, Extra
from typing import List

class Config(BaseModel, extra=Extra.ignore):
    capoo_download: bool = False        #是否开启本地图片存储，Ture为开启本地图片存储，下载源在国内，放心使用