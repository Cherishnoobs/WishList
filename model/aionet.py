'''
网络请求模块
'''

from asyncio.log import logger
from os import EX_CANTCREAT
import re
import json
import asyncio
from unittest import async_case
from log import get_logger

from httpx import Response, AsyncClient, head

from static import HEADERS, TIMEOUT, TREAD_CD

logger = get_logger('Net')

async def http_get(client: AsyncClient, url: str, params: dict = None,
                    headers: dict = None, retrys: int = 3) -> Response:
    '''
    出错自动重试的请求器

    参数:
        client: httpx对象
        url: url
        params: params
        headers: headers
        [retrys]: 重试次数,默认为3
    返回:
        Response: 请求结果
    '''
    if not headers:
        headers = HEADERS
    for _ in range(0, retrys):
        try:
            resp = await client.get(url=url, params=params, headers=headers, timeout=TIMEOUT)
            print('.', end='')
            await asyncio.sleep(TREAD_CD)
            return(resp)
        except Exception:
            if _ == 0:
                logger.debug('网络错误,暂停5秒')
                await asyncio.sleep(5)
            else:
                logger.warning('网络错误,暂停15秒')
                await asyncio.sleep(15)

    logger.error('网络错误,请求失败')
    return (None)

