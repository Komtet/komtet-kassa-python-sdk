# coding: utf-8
from . import VatRate


class Order(object):
    """
    :param int order_id: Номер операции в магазине
    :param str state: Статус заказа
    :param str sno: Система налогообложения
    """

    def __init__(self, order_id, state=None, sno=None, is_paid=False):
        self.__data = {
            'order_id': order_id,
            'is_paid': is_paid,
            'description': '',
            'items': [],
        }

        if state:
            self.__data['state'] = state

        if sno:
            self.__data['sno'] = sno

    def __iter__(self):
        for item in self.__data.items():
            yield item

    def __getitem__(self, item):
        return self.__data[item]

    def set_client(self, address, phone, email=None, name=None):
        """
        :param str client_name: Имя получателя
        :param str client_address: Адрес доставки
        :param str client_phone: Телефон получателя
        :param str client_email: Email получателя
        """
        self.__data['client_address'] = address
        self.__data['client_phone'] = phone

        if email:
            self.__data['client_email'] = email

        if name:
            self.__data['client_name'] = name

    def set_delivery_time(self, date_start, date_end):
        """
        :param datetime date_start: Начальное время доставки
        :param datetime date_end: Конечное время доставки
        """

        self.__data['date_start'] = date_start
        self.__data['date_end'] = date_end

    def set_description(self, description):
        """
        :param str description: Комментарий к заказу
        """

        self.__data['description'] = description

    def add_position(self, oid, name, price, quantity=1, total=None,
                     vat=VatRate.RATE_NO, measure_name=None, type=None):
        """
        :param str oid: Идентификатор позиции в заказе
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
            'order_item_id': oid,
            'name': name,
            'price': price,
            'quantity': quantity,
            'total': total,
            'vat': VatRate.parse(vat)
        }

        if measure_name:
            position['measure_name'] = measure_name

        if type:
            position['type'] = type

        self.__data['items'].append(position)
        return self

    def add_callback_url(self, callback_url):
        """
        :param str callback_url: URL
        """
        self.__data['callback_url'] = callback_url

    def add_courier_id(self, courier_id):
        """
        :param int courier_id: ID курьера
        """
        self.__data['courier_id'] = courier_id
