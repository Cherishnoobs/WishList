'''
@Description  : 公共函数
'''

from .static import ALMOST_LOWEST,OP_PATH
from os import path, makedirs, getcwd

def is_lowest(origin: int, current: int, lowest: int, cut: int) -> int :

    '''
    检查价格是否为史低

    参数:
        origin: 无折扣原价
        current: 现价
        lowest: 史低价
    返回:
        int: 1-史低,0-未达史低也不是近史低,-1-近史低
    '''

    if(cut > 0):
        if( current <= lowest): # 史低
            return 1
        elif ((current - lowest) / origin <= ALMOST_LOWEST): # 近史低
            return -1
    return 0

def is_lowest_str(r: int) ->int:
    '''
    检查价格是否为史低

    参数:
        origin: 无折扣原价
        current: 现价
        lowest: 史低价
    返回:
        str: 史低/近史低/空文本
    '''

    if (r > 0):
        return '史低'
    elif (r < 0):
        return '近史低'
    return "-"

def get_output_path(name: str) -> str:
    '''
    获取输出文件路径

    参数:
        name: 文件名
    返回:
        str: 文件路径
    '''

    if not path.exists(OP_PATH):
        makedirs(OP_PATH)
    p = path.join(getcwd(), OP_PATH, name)
    return str(p)

    