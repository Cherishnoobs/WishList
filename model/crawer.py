from asyncio import Semaphore
from symtable import Symbol


from .log import get_logger
from .aiosteam import _get_wishlist
from .aioitad import get_plains, get_lowest_price, get_current_price, get_card_info
from .utils import is_lowest
from .handler import data2md
class Crawer(object):
    # {appid: {游戏详情}}
    wishdict = {} 
    # steam 账号列表
    steamids = {}

    # 索引
    index = []

    def __init__(self, token: str , steamids: list, tag: str = None) -> None:
        '''
        初始化爬虫

        参数:
            setting: 调用 modle.config.get_config()
            steamids: steamid 列表
        '''
        try:
            steamids = set(steamids)
        except TypeError:
            raise ValueError('steam ID 必须为非空')
        
        if steamids:
            self.steamids = steamids
            self.token = token
        
            self.logger = get_logger(f'Crawer _{len(steamids)}')
            self.logger.debug(f'共有{len(steamids)}个账户')
        else:
            raise ValueError('steam ID 必须为非空列表')
        
    async def start(self):
        async with Semaphore(3): # 最大并发数
            await self.get_wishlist()
            await self.add_price()
            self.output()    


    async def get_wishlist(self):
        '''
        从steam读取愿望单
        '''
        wishdict = self.wishdict
        steamids = self.steamids

        self.logger.info('开始读取愿望单,如果报错请配置proxy')

        for i, sid in enumerate(steamids, 1):
            self.logger.info(f'开始读取 {steamids} 的愿望单 {i}')
            dic = await _get_wishlist(sid)
            self.logger.info(f'读取完毕,愿望单中共有{len(dic)}个游戏')
            wishdict.update(dic)
        self.logger.info(f'愿望单读取完毕,合并后共有{len(wishdict)}个游戏')
    
    async def add_price(self):
        '''
        获取游戏价格信息
        '''
        wishlist = self.wishdict
        token = self.token
        ids = list(wishlist.keys())
        plaindict = await get_plains(ids, token)
        self.logger.info(f'游戏ID读取完毕,共{len(plaindict)}条')

        plains = list(plaindict.values())
        self.logger.info('开始获取游戏价格信息,可能会比较久')
        # 需修改
        current_dict = await get_current_price(plains, token, 'cn', 'CN')
        lowest_dict = await get_lowest_price(plains, token, 'cn', 'CN')
        card_dict = await get_card_info(plains=plains,token=token)

        self.logger.info('整理游戏价格数据')
        for key in wishlist.keys():
            try:
                plain = plaindict[key]
            except KeyError:
                self.logger.debug(f'未找到ID为{key}的plain,已忽略')
                continue

            obj = wishlist[key]

            if not obj['free']:
                try:
                    p_now, p_old, p_cut = current_dict[plain]
                except KeyError:
                    # 当前价格数据缺失
                    p_now, p_old, p_cut = -1, -1, 0
                try:
                    p_low, p_low_cut, p_low_time = lowest_dict[plain]
                except KeyError:
                    # 史低价格数据缺失
                    p_low, p_low_cut, p_low_time = -1, 0, 0
            else:
                # 免费游戏
                p_now, p_old, p_cut = 0, 0, 0
                p_low, p_low_cut, p_low_time = 0, 0, 0
            

            obj['price'] = {
                'current': p_now,
                'origin': p_old,
                'current_cut': p_cut,
                'lowest': p_low,
                'low_cut': p_low_cut,
                'low_time': p_low_time,
                'is_lowest': is_lowest(p_old, p_now, p_low, p_cut)
            }
            obj['card'] = card_dict[plain]
        
        self.logger.info('价格数据整理完成')

        
    def output(self):
        '''
        输出形成 markdown 文件
        '''
        wishdict = self.wishdict
        # 写死
        symbol = '¥'
        index = wishdict.keys()

        self.logger.info('开始输出')

        try:
            markdown.handler(wishdict, index, symbol)
        except Exception as e:
            self.logger.error(f'遇到错误: {e}')
        

        self.logger.info('输出完成')