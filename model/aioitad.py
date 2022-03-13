'''
# @Description  : 对接ITAD的API【异步】
'''


import asyncio


from httpx import AsyncClient
from json import JSONDecodeError

from .log import get_logger
from .aionet import http_get
from .static import URLs, DB_NAME

logger  = get_logger('ITAD')

async def get_plains(ids: list, token: str, proxy: dict = None) ->dict:
    '''
    把appid或subid转换成IsThereAnyDeal使用的plainid

    参数：
        ids: appid列表,例如[730]
        token: ITAD的API token

    返回：
        dict: {id:plain} (如果id有误则返回None)
    '''

    params = {'key': token, 'shop': 'steam', 'ids': ''}
    id2pdict = {}
    ncache = ids
    async with AsyncClient(proxies=proxy) as client:
        max_ = len(ncache)
        if max_:
            tasks = set()
            for i in range(0, max_, 30):
                part = ncache[i:i+30]
                tasks.add(asyncio.create_task(
                    _get_plain(client, params, part)))
            await asyncio.wait(tasks)

            for task in tasks:
                dict = task.result()
                id2pdict.update(dict)
    return (id2pdict)

async def _get_plain(client: AsyncClient, params: dict, ids: list) -> str:
    '''
    appid2plainid

    参数:
        client: httpx Client 对象
        params: 参考 get_plain
    返回:
        dict: {id:plain} (如果id错误则返回 None)

    api: https://api.isthereanydeal.com/v01/game/plain/id/?key=&shop=&ids=
    '''
    url = URLs.ITAD_ID_To_Plain
    params['ids'] = ','.join([f'app/{x}' for x in ids])
    resp = await http_get(client=client, url=url, params=params)
    result = {}
    if resp:
        try:
            data = resp.json().get('data',{})
        except (JSONDecodeError, AttributeError) as e:
            logger.error(f'解析json出错 - {e}')
            data = {}
        for id_ in ids:
            plain = data.get(f'app/{id_}', None)
            if not plain:
                logger.warning(f'读取App{id_}出错,忽略该App')
            else:
                result[id_] = plain
    return (result)


async def get_current_price(plains: list, token: str, region: str, country: str,
                            proxy: dict = None) -> dict:
    '''
    使用plainid获取当前价格

    参数：
        plains: plain列表,例如['counterstrikeglobaloffensive']
        token: ITAD的API token
        region: 地区
        country: 国家
    返回：
        dict: 价格字典,以plain为键名,每个键是(现价,原价,折扣)
    '''

    params = {'key': token,  'plains': '', 'region': region,
              'country': country, 'shops': 'steam'}

    pricedict = {}
    if plains:
        async with AsyncClient(proxies=proxy) as client:
            max_ = len(plains)
            tasks = set()
            for i in range(0, max_ ,5):
                part = plains[i:i+5]
                tasks.add(asyncio.create_task(
                    _get_current_price(client, params, part)))
            await asyncio.wait(tasks)
        for task in tasks:
            dic = task.result()
            pricedict.update(dic)
    return (pricedict)

async def _get_current_price(client: AsyncClient, params: dict, plains: list) -> dict:
    '''
    获取Steam商店当前价格

    参数：
        client: httpx Client对象
        params: 参考get_current_price里的用法
    返回：
        dict: 价格字典,以plain为键名,每个键是(现价,原价,折扣)
    '''
    url = URLs.ITAD_Get_Current_Prices
    params['plains'] = ','.join(plains)
    resp = await http_get(client=client, url=url, params=params)
    pricedict = {}
    if resp:
        try:
            data = resp.json().get('data', {})
        except (JSONDecodeError, AttributeError):
            logger.error('json解析失败')
            data = {}
        for plain in data.keys():
            d = data[plain].get('list', None)
            if len(d) > 1:
                logger.debug(f'{plain} {d}')
            if d:
                price_new = d[0]['price_new']
                price_old = d[0]['price_old']
                price_cut = d[0]['price_cut']
            else:
                # 未发售游戏,没有价格,标记为-1
                price_new, price_old, price_cut = -1, -1, 0
            pricedict[plain] = (price_new, price_old, price_cut)
    return (pricedict)


async def get_lowest_price(plains: list, token: str, region: str, country: str,
                           proxy: dict = None) -> dict:
    
    '''
    获取Steam商店史低价格

    参数:
        plains: plain列表,例如['counterstrikeglobaloffensive']
        token: ITAD的API token
        region: 地区
        country: 国家
    返回:
        dict: 价格字典,以plain为键名,每个键是(史低,史低折扣,史低时间)
    '''
    params = {'key': token,  'plains': '', 'region': region,
              'country': country, 'shops': 'steam'}
    pricedict = {}
    if plains:
        async with AsyncClient(proxies=proxy) as client:
            max_ = len(plains)
            tasks = set()
            for i in range(0, max_, 5):
                part = plains[i:i+5]
                tasks.add(asyncio.create_task(
                    _get_lowest_price(client, params, part)))
                await asyncio.wait(tasks)
        for task in tasks:
            dic = task.result()
            pricedict.update(dic)
    return (pricedict)

async def _get_lowest_price(client: AsyncClient, params: dict, plains: list) -> dict:
    '''
    获取Steam商店史低价格

    参数：
        client: httpx Client对象
        params: 参考get_lowest_price里的用法
        plains: plains列表
    返回：
        dict: 价格字典,以plain为键名,每个键是(史低,史低折扣,史低时间)
    '''
    url = URLs.ITAD_Get_Lowest_Prices
    params['plains'] = ','.join(plains)
    resp = await http_get(client=client, url=url, params=params)
    pricedict = {}
    if resp:
        try:
            data = resp.json().get('data', {})
        except (JSONDecodeError, AttributeError):
            logger.error('json解析失败')
            data = {}
        for plain in data.keys():
            d = data[plain]
            if 'price' in d:
                price_low = d['price']
                price_cut = d['cut']
                price_time = d['added']
            else:
                # 未发售游戏,没有价格,标记为-1
                price_low, price_cut, price_time = -1, 0, 0
            pricedict[plain] = (price_low, price_cut, price_time)
    return (pricedict)

async def get_card_info(plains: list, token: str, proxy: dict = None) -> dict:
    '''
    获取Steam商店游戏信息【只能获取2个属性】

    参数:
        plains: plain列表,例如['counterstrikeglobaloffensive']
        token: ITAD的API token
    返回:
        dict: 游戏信息字典,(有成就,有卡牌)
    '''
    params = {'key': token,  'plains': ''}
    infodict = {}
    if plains:
        async with AsyncClient(proxies=proxy) as client:
            max_ = len(plains)
            tasks = set()
            for i in range(0, max_, 5):
                part = plains[i:i+5]
                tasks.add(asyncio.create_task(
                    _get_card_info(client, params, part)))
            await asyncio.wait(tasks)
        for task in tasks:
            dic = task.result()
            infodict.update(dic)
    return (infodict)


async def _get_card_info(client: AsyncClient, params: dict, plains: list) -> dict:
    '''
    获取Steam商店史低价格

    参数：
        client: httpx Client对象
        params: 参考get_base_info里的用法
        plains: plains列表
    返回：
        dict: 游戏信息字典
    '''
    url = URLs.ITAD_Get_Game_Info
    params['plains'] = ','.join(plains)
    resp = await http_get(client=client, url=url, params=params)
    infodict = {}
    if resp:
        try:
            data = resp.json().get('data', {})
        except (JSONDecodeError, AttributeError):
            logger.error(f'json解析失败')
            data = {}
        for plain in data.keys():
            d = data[plain]
            has_achi = d.get('achievements', False)
            has_card = d.get('trading_cards', False)
            infodict[plain] = [has_achi,has_card]
    return (infodict)



# 单元测试

# ids = [4000,3000]
# token = '71a7d4524266563df456abdede7f7145683d649e'
# async def test():
#         try:
#             # 获取ID
#             result = await get_plains(ids=ids, token=token)
#             plains = list(result.values())
#             current_dict = await get_current_price(plains, token, 'cn', 'CN')
#             lowest_dict = await get_lowest_price(plains, token, 'cn', 'CN')
#             card_dict = await get_card_info(plains, token)
#             print(current_dict)
#             print(lowest_dict)
#             print(card_dict)
#         except Exception as e:
#             logger.warning(f'{e}')
# loop = asyncio.get_event_loop()
# loop.run_until_complete(test())