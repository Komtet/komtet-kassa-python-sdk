from .check import Check, CheckPosition
from .constants import (WITHOUT_VAT, VAT0, VAT10, VAT18, VAT110, VAT118,
                        SELL, SELL_RETURN,
                        CARD, CASH,
                        ACTIVE_QUEUE_STATE, PASSIVE_QUEUE_STATE)
from .queue import PrintQueue


__all__ = [
    'PrintQueue',
    'Check', 'CheckPosition',
    'WITHOUT_VAT', 'VAT0', 'VAT10', 'VAT18', 'VAT110', 'VAT118',
    'SELL', 'SELL_RETURN',
    'CARD', 'CASH',
    'ACTIVE_QUEUE_STATE', 'PASSIVE_QUEUE_STATE'

]


def configure(config, prefix=None):
    from . import request

    if prefix:
        config = {key[len(prefix):]: val
                  for key, val in config.items()
                  if key.startswith(prefix)}

    if 'shop_key' in config:
        request.SHOP_KEY = config['shop_key']
    if 'shop_secret' in config:
        request.SHOP_SECRET = config['shop_secret']
    if 'server' in config:
        request.API_SERVER = config['server']
    if 'path_prefix' in config:
        request.API_PATH_PREFIX = config['path_prefix']

    PrintQueue.configure(config.get('named_queues'))
