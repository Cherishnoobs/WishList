'''
@Description  : 公共函数
'''

from .static import ALMOST_LOWEST

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