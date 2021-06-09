# coding: utf-8

class EmployeeType(object):
    """Тип Сотрудника"""

    COURIER = 'courier'
    """Курьер"""

    CASHIER = 'cashier'
    """Кассир"""

    DRIVER = 'driver'
    """Водитель"""


class Employee(object):
    """
    :param EmployeeType type: Тип сотрудника
    :param str name: ФИО сотрудника
    :param str login: Логин сотрудника
    :param str password: Пароль сотрудника
    :param str pos_id: ID кассы
    :param str inn: ИНН сотрудника
    :param str phone: Телефон сотрудника
    :param str email: Email сотрудника
    """

    def __init__(self, type, name, login, password, pos_id, inn=None, phone=None, email=None):
        self.__data = {
            'type': type,
            'name': name,
            'login': login,
            'password': password,
            'pos_id': pos_id
        }
        if inn:
            self.__data['inn'] = inn

        if phone:
            self.__data['phone'] = phone

        if email:
            self.__data['email'] = email

    def __iter__(self):
        for item in self.__data.items():
            yield item

    def __getitem__(self, item):
        return self.__data[item]

    def set_payment_address(self, payment_address):
        """
        Установка адреса места рассчета
        :param str payment_address: Адрес места рассчета
        """
        self.__data['payment_address'] = payment_address

    def set_access_settings(self, is_manager=None, is_can_assign_order=None,
                            is_app_fast_basket=None):
        """
        Установка настроек доступа
        :param bool is_manager: Разрешить в приложении редактировать и создавать заказы
        :param bool is_can_assign_order: Разрешить просматривать весь список свободных заказов и
                                         выбирать из него
        :param bool is_app_fast_basket: Переходить в корзину сразу после выбора товара
        """
        if is_manager:
            self.__data['is_manager'] = is_manager

        if is_can_assign_order:
            self.__data['is_can_assign_order'] = is_can_assign_order

        if is_app_fast_basket:
            self.__data['is_app_fast_basket'] = is_app_fast_basket
