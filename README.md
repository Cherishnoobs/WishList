# WishList
Simple Steam Wishlist Crawler

## 环境要求
python 3.5 及以上

## 部署

### 安装依赖
```
$ pip3 install -r requirements.txt
```

### 配置 stemaID

将 run.py 中 STEAMID = '' 改为自己的 steam 64位 ID,可用列表传入多个 ID，实现多用户配置

## 目录

```
├── model
├── ├── __init__.py
├── ├── aionet.py   # 网络抓取模块
├── ├── aioitad.py  # 游戏额外信息抓取模块
├── ├── aiosteam.py # steam 愿望单抓取模块
├── ├── crawer.py   
├── ├── utlis.py    # 额外工具函数
├── ├── static.py   # 静态常量
├── ├── log.py      # 日志模块
├── ├── ├── Handler
├── ├── ├── __init__.py
├── ├── ├── ├── Data2Md.py  # 输出模块
├── run.py          # 程序入口
```

## 声明

- 本程序仅供学习参考
