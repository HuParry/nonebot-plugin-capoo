<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-capoo

_✨ 一个发送指令就能让你的 bot 发出可爱的 capoo 的图片的插件 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/HuParry/nonebot-plugin-capoo.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-capoo">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-capoo.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>

## 📖 介绍

capoo 实在是太可爱了，所以我收集了几百张 capoo 的表情包。这个插件用于让 bot 发送 capoo 的表清包。

## 💿 安装

<details>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-capoo

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-capoo
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-capoo
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-capoo
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-capoo
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_capoo"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| capoo_download | 否 | False | 是否开启本地图片存储，True为开启本地图片存储 |

图源在 AC Git 上，是国内的远程代码库站点，所以不用担心被墙了而发不出图片。 


## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| `capoo` | 群员 | 否 | 群聊 | 随机发送一张 capoo 的表情包 |

### 效果图
<img src="./docs/preview.jpg" style="zoom:30%;" />

## TODO
- [x] 指令触发 bot 发送图片
- [ ] 在 QQ 上让 bot 存储 capoo 图片
- [ ] 每次存储图片，判断图片是否已经存在，避免重复加入