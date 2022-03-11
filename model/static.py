# 网络超时时间
TIMEOUT = 10

# 每个线程的等待时间
TREAD_CD = 0.8

HEADERS = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Steam_Wishlist_Helper",
}

class URLs():
    '''
    URL常量
    '''

    Steam_Store = 'https://store.steampowered.com/'
    Steam_Wishlist = 'https://store.steampowered.com/wishlist/profiles/%s/#sort=%s'
    Steam_Wishlist_XHR = 'https://store.steampowered.com/wishlist/profiles/%s/wishlistdata/?p=%s'
    Steam_Game_Pic_SM = 'https://steamcdn-a.akamaihd.net/steam/apps/%s/capsule_sm_120.jpg'
    Steam_Game_Pic_MD = 'https://steamcdn-a.akamaihd.net/steam/apps/%s/header_292x136.jpg'

    ITAD_ID_To_Plain = 'https://api.isthereanydeal.com/v01/game/plain/id/'
    ITAD_Get_Current_Prices = 'https://api.isthereanydeal.com/v01/game/prices/'
    ITAD_Get_Lowest_Prices = 'https://api.isthereanydeal.com/v01/game/lowest/'
    ITAD_Get_Game_Info = 'https://api.isthereanydeal.com/v01/game/info/'
    ITAD_Get_Overview_Prices = 'https://api.isthereanydeal.com/v01/game/overview/'

    Keylol_Get_Game_Info = 'https://steamdb.keylol.com/app/%s/data.js?v=38'


Num2Review = {
    -1: '【解析出错】',
    0: '评测数量不足',
    1: '差评如潮',
    2: '特别差评',
    3: '差评',
    4: '多半差评',
    5: '褒贬不一',
    6: '多半好评',
    7: '好评',
    8: '特别好评',
    9: '好评如潮'
}

GameType2Num = {
    'Error': 0,
    'Game': 1,
    'Application': 2,
    'DLC': 3,
    'Video': 4
}