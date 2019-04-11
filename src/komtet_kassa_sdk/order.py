# coding: utf-8
from . import VatRate


class Order(object):
    """
    :param int order_id: Номер операции в магазине
    :param str client_name: Имя получателя
    :param str client_address: Адрес доставки
    :param str client_phone: Телефон получателя
    :param str client_email: Email получателя
    :param str description: Комментарий к заказу
    :param str state: Статус заказа
    :param datetime date_start: Начальное время доставки
    :param datetime date_end: Конечное время доставки
    :param str sno: Система налогообложения
    """

    def __init__(self, order_id, client_name, client_address, client_phone, client_email,
                 description, state, sno, date_start, date_end, is_paid=False):
        self.__data = {
            'order_id': order_id,
            'client_name': client_name,
            'client_address': client_address,
            'client_phone': client_phone,
            'client_email': client_email,
            'is_paid': is_paid,
            'description': description,
            'state': state,
            'date_start': date_start,
            'date_end': date_end,
            'items': [],
            'sno': sno,
        }

    def __iter__(self):
        for item in self.__data.items():
            yield item

    def __getitem__(self, item):
        return self.__data[item]

    def add_position(self, num, type, name, price, quantity=1, total=None, vat=VatRate.RATE_NO,
                     measure_name=None):
        """
        :param int num: Номер позиции в заказе
        :param str type: Тип заказа
        :param str name: Наименование позиции
        :param int|float price: Цена позиции в чеке
        :param int|float quantity: Количество единиц
        :param int|float total: Общая стоимость позиции
        :param str vat: Налоговая ставка
        """
        if total is None:
            total = price * quantity

        position = {
            'order_item_id': num,
            'type': type,
            'name': name,
            'price': price,
            'quantity': quantity,
            'total': total,
            'vat': VatRate.parse(vat)
        }

        if measure_name is not None:
            position['measure_name'] = measure_name

        self.__data['items'].append(position)
        return self
