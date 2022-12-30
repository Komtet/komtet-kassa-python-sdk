# coding: utf-8
from komtet_kassa_sdk.v1.lib.helpers import apply_discount, correction_positions

from . import PaymentMethod, VatRate


class Order(object):
    """
    :param int order_id: Номер операции в магазине
    :param str sno: Система налогообложения
    :param str state: Статус заказа
    :param int|float prepayment: Предоплата
    :param PaymentMethod payment_type: Тип платежа
    """

    def __init__(self, order_id, sno, state=None, is_paid=False,
                 prepayment=0, payment_type=PaymentMethod.CARD):
        self.__data = {
            'order_id': order_id,
            'is_paid': is_paid,
            'description': '',
            'items': [],
            'payment_type': payment_type,
            'prepayment': prepayment,
            'sno': sno
        }

        if state:
            self.__data['state'] = state

    def __iter__(self):
        for item in self.__data.items():
            yield item

    def __getitem__(self, item):
        return self.__data[item]

    def set_client(self, address, phone, email=None, name=None, coordinate=None):
        """
        :param str client_name: Имя получателя
        :param str client_address: Адрес доставки
        :param str client_phone: Телефон получателя
        :param str client_email: Email получателя
        :param dict client_coordinate: Координата адреса получателя
        """
        self.__data['client_address'] = address
        self.__data['client_phone'] = phone

        if email:
            self.__data['client_email'] = email

        if name:
            self.__data['client_name'] = name

        if coordinate:
            self.__data['client_coordinate'] = coordinate

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
                     vat=VatRate.RATE_NO, measure_name=None, type=None, agent=None,
                     excise=None, country_code=None, declaration_number=None,
                     nomenclature_code=None, is_need_nomenclature_code=None):
        """
        :param str oid: Идентификатор позиции в заказе
        :param str type: Тип заказа
        :param str name: Наименование позиции
        :param int|float price: Цена позиции в чеке
        :param int|float quantity: Количество единиц
        :param int|float total: Общая стоимость позиции
        :param str vat: Налоговая ставка
        :param Agent agent: Экземпляр агента
        :param int|float excise: Сумма акциза
        :param str country_code: Цифровой код страны происхождения товара
        :param str declaration_number: Номер таможенной декларации
        :param str nomenclature_code: Код товара считанный с марки
        :param bool is_need_nomenclature_code: Требуется считать маркировку
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

        if agent is not None:
            position.update(dict(agent))

        if excise is not None:
            position['excise'] = excise

        if country_code is not None:
            position['country_code'] = country_code

        if declaration_number is not None:
            position['declaration_number'] = declaration_number

        if nomenclature_code is not None:
            position['nomenclature_code'] = nomenclature_code

        if is_need_nomenclature_code is not None:
            position['is_need_nomenclature_code'] = is_need_nomenclature_code

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

    def apply_discount(self, discount):
        """
        :param int|float discount: сумма скидки
        """
        apply_discount(discount, self.__data['items'])

    def apply_correction_positions(self):
        """
        Кооректировка позиций с расхождениями между price * quantity и total
        """
        self.__data['items'] = correction_positions(self.__data['items'])
