import re
import asyncio

from httpx import AsyncClient
from .aionet import http_get
from .static import GameType2Num, Num2Review
from .static import URLs
from .log import get_logger
from json import JSONDecodeError

logger = get_logger('steam')

PIC_URL = URLs.Steam_Game_Pic_SM


async def _get_wishlist(steamid: int, proxy: dict = None) -> dict:
    '''
    异步读取Steam愿望单

    参数:
        steamid: 64位SteamID
    返回：
        dict: {appid:{游戏详情}}
    '''
    global PIC_URL

    async with AsyncClient(proxies=proxy) as client:
        client.cookies = {
            'Cookie': f'wants_mature_content=1;Steam_Language=schinese'
        }
        try:
            count = await _get_page_count(client=client, steamid=steamid)
        except ValueError as e:
            logger.warning(f'{e}')
            return {{}}
        tasks = {
            asyncio.create_task(_get_single_page(client=client, steamid=steamid, page=p)) for p in range(0, count)
        }
        await asyncio.wait(tasks)
    wishlist = {}
    for task in tasks:
        wishlist.update(task.result())
    return (wishlist)    


async def _get_page_count(client: AsyncClient, steamid: int) -> int:
    '''
    获取steam愿望单页书

    参数:
        client: httpx异步client对象
        steamid: 64位steamid
    返回:
        int: 愿望单页数
    '''
    url = URLs.Steam_Wishlist % (steamid, 'order')
    resp = await http_get(client=client, url=url)
    if not resp:
        raise ValueError('网络错误,拉去失败')

    pattern = re.compile(r'nAdditionalPages\s=\s(\d+)')
    match_obj = pattern.search(resp.text)
    count = 0
    if match_obj:
        count = int(match_obj.group(1))
    else:
        raise ValueError(f'读取用户{steamid}的愿望单失败,请检查SteamID')
    if count == 0:
        raise ValueError(f'用户{steamid}愿望单为空,请检查是否将愿望单公开')
    return (count)

async def _get_single_page(client: AsyncClient, steamid: int, page: int = 0) ->dict:
    '''
    获取steam愿望单单页详情

    参数:
        client: httpx异步client对象
        steamid: 64位steamid
        page: 页码
    返回:
        dict: 愿望单信息字典,key:{游戏信息}
    '''
    url = URLs.Steam_Wishlist_XHR % (steamid, page)
    headers = {
        'Referer': URLs.Steam_Wishlist % (steamid, 'order')
    }
    resp = await http_get(client=client, url=url, headers=headers)
    wishlist = {}
    if resp:
        try:
            datajson = resp.json()
        except (JSONDecodeError, AttributeError):
            logger.error('Json解析失败')
            logger.error(resp.content)
            return {}

        for key in datajson.keys():
            data = datajson[key]
            review_score = int(data.get('review_score', -1))
            key = int(key)
            wishlist[key] = {
                'name': data.get('name', '【解析出错】'),
                'picture': PIC_URL % key,
                'review': {
                    'score': review_score,
                    'result': Num2Review.get(review_score, 'Error'),
                    'total': int(data.get('reviews_total', '0').replace(',', '')),
                    'percent': int(data.get('reviews_percent', 0)),
                },
                'release_date': int(data.get('release_date', 0)),
                'subs': [s['id'] for s in data.get('subs', [])],
                'free': data.get('is_free_game', False),
                'type': GameType2Num.get(data.get('type', 'Error'), 0),
                'priority': data.get('priority', 0),
                'tags': data.get('tags', []),
                'add_date': int(data.get('added', 0)),
                # 'rank': int(data.get('rank', 0)),
                'price': {},
                'platform': (
                    data.get('win', 0) == 1,
                    data.get('mac', 0) == 1,
                    data.get('linux', 0) == 1
                ),
                "card": False
            }
            if wishlist[key]['name'] == '【解析出错】':
                logger.debug(f'数据解析失败 {data}')
    return (wishlist)

# 单元测试
# steamid = 76561198323399563

# async def test():

#         try:
#             wishlist = await _get_wishlist(steamid=steamid)
#         except Exception as e:
#             logger.warning(f'{e}')

# loop = asyncio.get_event_loop()
# loop.run_until_complete(test())