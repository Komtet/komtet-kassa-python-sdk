# coding: utf-8


class Intent(object):
    """Направление платежа"""

    SELL = 'sell'
    """Платёж"""

    RETURN = 'sellReturn'
    """Возврат"""


class TaxSystem(object):
    """Система налогообложения"""

    COMMON = 0
    """ОСН"""

    SIMPLIFIED_IN = 1
    """УСН доход"""

    SIMPLIFIED_IN_OUT = 2
    """УСН доход - расход"""

    UTOII = 3
    """ЕНВД"""

    UST = 4
    """ЕСН"""

    PATENT = 5
    """Патент"""


class VatRate(object):
    """Налоговая ставка"""

    RATE_NO = 'no'
    """Без НДС"""

    RATE_0 = '0'
    """НДС 0%"""

    RATE_10 = '10'
    """НДС 10%"""

    RATE_18 = '18'
    """НДС 18%"""

    RATE_110 = '110'
    """НДС 10/110"""

    RATE_118 = '118'
    """НДС 18/118"""

    @classmethod
    def parse(cls, rate):
        if not isinstance(rate, str):
            rate = str(rate)

        if rate == '10/110':
            rate = cls.RATE_110
        elif rate == '18/118':
            rate = cls.RATE_118
        else:
            rate = rate.replace('%', '')
            rate = rate.replace('0.', '')
        if rate not in cls.get_rates():
            raise ValueError('Unknown VAT rate: %s' % rate)
        return rate

    @classmethod
    def get_rates(cls):
        if not hasattr(cls, 'rates'):
            cls.rates = [value for key, value in cls.__dict__.items() if key.startswith('RATE_')]
        return cls.rates


class Check(object):
    """
    :param oid: Номер операции в магазине
    :param str email: E-Mail пользователя для отправки электронного чека
    :param str intent: Направление платежа
    :param int tax_system: Система налогообложения
    """
    def __init__(self, oid, email, intent, tax_system):
        self.__data = {
            'task_id': oid,
            'user': email,
            'print': False,
            'intent': intent,
            'sno': tax_system,
            'payments': [],
            'positions': []
        }

    def __iter__(self):
        for item in self.__data.items():
            yield item

    def __getitem__(self, item):
        return self.__data[item]

    def set_print(self, value):
        """
        :param bool value: Печатать чек или нет
        """
        self.__data['print'] = bool(value)
        return self

    def add_payment(self, amount):
        """
        :param int|float amount: Сумма платежа
        """
        self.__data['payments'].append({'sum': amount})
        return self

    def add_position(self, name, price, quantity=1, total=None, vat=VatRate.RATE_NO):
        """
        :param str name: Наименование позиции
        :param int|float price: Цена позиции в чеке
        :param int|float quantity: Количество единиц
        :param int|float total: Общая стоимость позиции
        :param str vat: Налоговая ставка
        """
        if total is None:
            total = price * quantity
        self.__data['positions'].append({
            'name': name,
            'price': price,
            'quantity': quantity,
            'total': total,
            'vat': VatRate.parse(vat)
        })
        return self
