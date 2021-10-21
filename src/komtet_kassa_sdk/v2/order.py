# coding: utf-8
from komtet_kassa_sdk.v2.lib.helpers import apply_discount, correction_positions

from . import PaymentType, VatRate


class Order(object):
    """
    :param int external_id: Номер операции в магазине
    :param str sno: Система налогообложения
    :param str state: Статус заказа
    :param int|float prepayment: Предоплата
    :param PaymentType payment_type: Тип платежа
    """

    def __init__(self, external_id, state=None, is_pay_to_courier=True,
                 prepayment=0, payment_type=PaymentType.CARD):
        self.__data = {
            'external_id': external_id,
            'is_pay_to_courier': is_pay_to_courier,
            'description': '',
            'items': [],
            'payment_type': payment_type,
            'prepayment': prepayment,
        }

        if state:
            self.__data['state'] = state

    def __iter__(self):
        for item in self.__data.items():
            yield item

    def __getitem__(self, item):
        return self.__data[item]

    def set_company(self, payment_address, tax_system, inn=None, place_address=None, email=None):
        """
        :param str payment_address: Платёжный адрес компании
        :param str tax_system: Система налогообложения
        """

        self.__data['company'] = {'payment_address': payment_address, 'sno': tax_system}

        if inn:
            self.__data['company']['inn'] = inn

        if place_address:
            self.__data['company']['place_address'] = place_address

        if email:
            self.__data['company']['email'] = email

        return self

    def set_client(self, address, phone, email=None, name=None, coordinate=None, inn=None):
        """
        :param str name: Имя получателя
        :param str address: Адрес доставки
        :param str phone: Телефон получателя
        :param str email: Email получателя
        :param dict coordinate: Координата адреса получателя
        """
        self.__data['client'] = {
            'address': address,
            'phone': phone
        }

        if email:
            self.__data['client']['email'] = email

        if name:
            self.__data['client']['name'] = name

        if inn:
            self.__data['client']['inn'] = inn

        if coordinate:
            self.__data['client']['coordinate'] = coordinate

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

    def add_callback_url(self, callback_url):
        """
        :param str callback_url: URL
        """
        self.__data['callback_url'] = callback_url

    def set_courier_id(self, courier_id):
        """
        :param int courier_id: ID курьера
        """
        self.__data['courier_id'] = courier_id

    def set_additional_user_props(self, name, value):
        """
        :param str name: Наименование дополнительного реквизита пользователя
        :param str value: Значение дополнительного реквизита пользователя
        """
        self.__data['additional_user_props'] = {
            'name': name,
            'value': value
        }

    def set_additional_check_props(self, value):
        """
        :param str value: Дополнительный реквизит чека
        """
        self.__data['additional_check_props'] = value

    def add_sectoral_check_props(self, federal_id, date, number, value):
        """ Установка данных об отраслевой принадлежности
        :param str federal_id: Идентификатор ФОИВ
        :param str date: Дата нормативного акта федерального органа исполнительной власти
        :param str number: Номер нормативного акта федерального органа исполнительной власти
        :param str value: Состав значений
        """
        if not self.__data.get('sectoral_check_props'):
            self.__data['sectoral_check_props'] = []

        self.__data['sectoral_check_props'].append({
            'federal_id': federal_id,
            'date': date,
            'number': number,
            'value': value
        })

    def set_operating_check_props(self, name, value, timestamp):
        """ Условия применения и значение реквизита «операционный реквизит чека»
        :param str name: Идентификатор операции
        :param str value: Данные операции
        :param str timestamp: Дата и время операции в формате: «dd.mm.yyyy HH:MM:SS»
        """
        self.__data['operating_check_props'] = {
            'name': name,
            'value': value,
            'timestamp': timestamp
        }

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

    def add_item(self, item):
        """
        :param OrderItem item: Экземпляр позиции
        """
        self.__data['items'].append(dict(item))


class OrderItem(object):
    """
        :param int id: Идентификатор позиции в заказе
        :param int product_id: Идентификатор продукта в магазине
        :param str name: Наименование позиции
        :param str type: Тип заказа
        :param int|float price: Цена позиции в заказе
        :param int|float quantity: Количество единиц
        :param str measure: Единица измерения
        :param int|float total: Общая стоимость позиции
        :param str user_data: Дополнительный реквизит предмета расчета
        :param int|float excise: Сумма акциза
        :param str country_code: Цифровой код страны происхождения товара
        :param str declaration_number: Номер таможенной декларации
        :param str vat: Налоговая ставка
        :param bool is_need_nomenclature_code: Необходимость указания маркировки для фискализации
    """

    def __init__(self, name, price, quantity=1, measure=0, total=None, is_need_nomenclature_code=False,
                 type=None, user_data=None, excise=None, id=None, country_code=None, product_id=None,
                 declaration_number=None, vat=VatRate.RATE_NO, external_id=None):
        if total is None:
            total = price * quantity

        self.__data = {
            'name': name,
            'measure': measure,
            'price': price,
            'quantity': quantity,
            'total': total,
            'vat': VatRate.parse(vat)
        }

        if id is not None:
            self.__data['id'] = id

        if type is not None:
            self.__data['type'] = type

        if measure is not None:
            self.__data['measure'] = measure

        if product_id is not None:
            self.__data['product_id'] = product_id

        if id is not None:
            self.__data['id'] = id

        if external_id is not None:
            self.__data['external_id'] = external_id

        if excise is not None:
            self.__data['excise'] = excise

        if country_code is not None:
            self.__data['country_code'] = country_code

        if user_data is not None:
            self.__data['user_data'] = user_data

        if declaration_number is not None:
            self.__data['declaration_number'] = declaration_number

        if is_need_nomenclature_code is not None:
            self.__data['is_need_nomenclature_code'] = is_need_nomenclature_code

    def set_agent(self, agent):
        """
        :param Agent agent: агент на позицию
        """
        self.__data.update(dict(agent))

    def set_mark_code(self, type, code):
        """ Установка кода маркировки
        :param str type: Тип маркировки
        :param str code: Код маркировки
        """
        self.__data['mark_code'] = {type: code}

    def set_mark_quantity(self, numerator, denominator):
        """ Установка дробного колличества маркировки
        :param int numerator: Делимое
        :param int denominator: Делитель
        """
        self.__data['mark_quantity'] = {
            'numerator': numerator,
            'denominator': denominator
        }

    def add_sectoral_item_props(self, federal_id, date, number, value):
        """ Установка данных об отраслевой принадлежности
        :param str federal_id: Идентификатор ФОИВ
        :param int date: Дата нормативного акта федерального органа исполнительной власти
        :param str number: Номер нормативного акта федерального органа исполнительной власти
        :param str value: Состав значений
        """
        if not self.__data.get('sectoral_item_props'):
            self.__data['sectoral_item_props'] = []

        self.__data['sectoral_item_props'].append({
            'federal_id': federal_id,
            'date': date,
            'number': number,
            'value': value
        })

    def __iter__(self):
        for item in self.__data.items():
            yield item
