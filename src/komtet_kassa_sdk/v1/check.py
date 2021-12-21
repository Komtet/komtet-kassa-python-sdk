# coding: utf-8
from komtet_kassa_sdk.v1.lib.helpers import apply_discount, correction_positions


class Intent(object):
    """Направление платежа"""

    SELL = 'sell'
    """Приход"""

    RETURN = 'sellReturn'
    """Возврат прихода"""

    BUY = 'buy'
    """Расход"""

    BUY_RETURN = 'buyReturn'
    """Возврат расхода"""

    SELL_CORRECTION = 'sellCorrection'
    """Коррекция прихода"""

    BUY_CORRECTION = 'buyCorrection'
    """Коррекция расхода"""

    SELL_RETURN_CORRECTION = 'sellReturnCorrection'
    """Коррекция возврата прихода"""

    BUY_RETURN_CORRECTION = 'buyReturnCorrection'
    """Коррекция возврата расхода"""


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

    RATE_20 = '20'
    """НДС 20%"""

    RATE_110 = '110'
    """НДС 10/110"""

    RATE_120 = '120'
    """НДС 20/120"""

    @classmethod
    def parse(cls, rate):
        if isinstance(rate, float) and rate < 1:
            rate = '%.2f' % rate

        if not isinstance(rate, str):
            rate = str(rate)

        if rate == '10/110':
            rate = cls.RATE_110
        elif rate in ['20/120', '18/118']:
            rate = cls.RATE_120
        else:
            rate = rate.replace('%', '')
            rate = rate.replace('0.', '')

        if rate in ['18', 18]:
            rate = cls.RATE_20
        elif rate in ['118', 118, '18/118']:
            rate = cls.RATE_120

        if rate not in cls.get_rates():
            raise ValueError('Unknown VAT rate: %s' % rate)
        return rate

    @classmethod
    def get_rates(cls):
        if not hasattr(cls, 'rates'):
            cls.rates = [value for key, value in cls.__dict__.items() if key.startswith('RATE_')]
        return cls.rates


class PaymentMethod(object):
    """Метод оплаты"""

    CARD = 'card'
    """Электронными"""

    CASH = 'cash'
    """Наличными"""

    PREPAYMENT = 'prepayment'
    """Cумма предоплатой (зачет аванса и/или предыдущих платежей)"""

    CREDIT = 'credit'
    """Cумма постоплатой (кредит)"""

    COUNTER_PROVISIONING = 'counter_provisioning'
    """Cумма встречным предлжением"""


class CorrectionType(object):
    """Тип коррекции"""

    SELF = 'self'
    """Самостоятельно"""

    FORCED = 'forced'
    """По предписанию"""


class CalculationMethod(object):
    """Cпособ рассчета"""

    PRE_PAYMENT_FULL = 'pre_payment_full'
    """Полная предварительная оплата до момента передачи предмета расчета «ПРЕДОПЛАТА 100 %»"""

    PRE_PAYMENT_PART = 'pre_payment_part'
    """Частичная предварительная оплата до момента передачи предмета расчета - «ПРЕДОПЛАТА»"""

    FULL_PAYMENT = 'full_payment'
    """Полная оплата, в том числе с учетом аванса (предварительной оплаты) в момент передачи
       предмета расчета - «ПОЛНЫЙ РАСЧЕТ»"""

    ADVANCE = 'advance'
    """Аванс"""

    CREDIT_PART = 'credit_part'
    """Частичная оплата предмета расчета в момент его передачи с последующей оплатой в кредит -
       «ЧАСТИЧНЫЙ РАСЧЕТ И КРЕДИТ»"""

    CREDIT_PAY = 'credit_pay'
    """Оплата предмета расчета после его передачи с оплатой в кредит (оплата кредита) -
       «ОПЛАТА КРЕДИТА»"""

    CREDIT = 'credit'
    """Передача предмета расчета без его оплаты в момент его передачи с последующей оплатой в
       кредит - «ПЕРЕДАЧА В КРЕДИТ»"""


class CalculationSubject(object):
    """Признак рассчета"""

    PRODUCT = 'product'
    """Товар, за исключением подакцизного товара"""

    PRODUCT_PRACTICAL = 'product_practical'
    """Подакцизный товар"""

    WORK = 'work'
    """Работа"""

    SERVICE = 'service'
    """Услуга"""

    GAMBLING_BET = 'gambling_bet'
    """Прием ставок при осуществлении деятельности по проведению азартных игр"""

    GAMBLING_WIN = 'gambling_win'
    """Выплата денежных средств в виде выигрыша при осуществлении деятельности по проведению
       азартных игр"""

    LOTTERY_BET = 'lottery_bet'
    """Прием денежных средств при реализации лотерейных билетов, электронных лотерейных билетов,
       приеме лотерейных ставок при осуществлении деятельности по проведению лотерей"""

    LOTTERY_WIN = 'lottery_win'
    """Выплате денежных средств в виде выигрыша при осуществлении деятельности по проведению
       лотерей"""

    RID = 'rid'
    """Предоставление прав на использование результатов интеллектуальной деятельности или средств
       индивидуализации «ПРЕДОСТАВЛЕНИЕ РИД» или «РИД»"""

    PAYMENT = 'payment'
    """Об авансе, задатке, предоплате, кредите, взносе в счет оплаты, пени, штрафе, вознаграждении,
       бонусе и ином аналогичном предмете расчета"""

    COMMISSION = 'commission'
    """Вознаграждении пользователя, являющегося платежным агентом (субагентом), банковским
       платежным агентом (субагентом), комиссионером, поверенным или иным агентом"""

    COMPOSITE = 'composite'
    """О предмете расчета, состоящем из предметов, каждому из которых может быть присвоено
       значение от «0» до «11» (0-11 -- это вышеперечисленные)"""

    PAY = 'pay'
    """Взнос в счет оплаты пени, штрафа, вознаграждения, бонуса или
       иного аналогичного предмета расчета"""

    OTHER = 'other'
    """О предмете расчета, не относящемуся к предметам расчета, которым может быть присвоено
       значение от «0» до «12» (0-12 -- это вышеперечисленные)"""

    PROPERTY_RIGHT = 'property_right'
    """Передача имущественного права"""

    NON_OPERATING = 'non_operating'
    """Внереализационный доход"""

    INSURANCE = 'insurance'
    """Страховые взносы"""

    SALES_TAX = 'sales_tax'
    """Торговый сбор"""

    RESORT_FEE = 'resort_fee'
    """Курортный сбор"""


class AgentType(object):
    """Типы признака агента по предмету расчета"""

    BANK_PAYMENT_AGENT = 'bank_payment_agent'
    """Оказание услуг покупателю (клиенту) пользователем, являющимся банковским платежным агентом
       банковским платежным агентом"""

    BANK_PAYMENT_SUBAGENT = 'bank_payment_subagent'
    """Оказание услуг покупателю (клиенту) пользователем, являющимся банковским платежным агентом
       банковским платежным субагентом"""

    PAYMENT_AGENT = 'payment_agent'
    """Оказание услуг покупателю (клиенту) пользователем, являющимся платежным агентом"""

    PAYMENT_SUBAGENT = 'payment_subagent'
    """Оказание услуг покупателю (клиенту) пользователем, являющимся платежным субагентом"""

    SOLICITOR = 'solicitor'
    """Осуществление расчета с покупателем (клиентом) пользователем, являющимся поверенным"""

    COMMISSIONAIRE = 'commissionaire'
    """Осуществление расчета с покупателем (клиентом) пользователем, являющимся комиссионером"""

    AGENT = 'agent'
    """Осуществление расчета с покупателем (клиентом) пользователем, являющимся агентом и не
       являющимся банковским платежным агентом (субагентом), платежным агентом (субагентом),
       поверенным, комиссионером"""


class Nomenclature(object):
    """Код товара (маркировка)
    :param str code: Код маркировки
    :param str hex_code: Код маркировки в HEX представлении
    """

    def __init__(self, code=None, hex_code=None):
        self.__data = {'nomenclature_code': {}}

        if code:
            self.code = code

        if hex_code:
            self.hex_code = hex_code

    @property
    def code(self):
        return self.__data['nomenclature_code'].get('code')

    @code.setter
    def code(self, value):
        self.__data['nomenclature_code']['code'] = value

    @property
    def hex_code(self):
        return self.__data['nomenclature_code'].get('hex_code')

    @hex_code.setter
    def hex_code(self, value):
        self.__data['nomenclature_code']['hex_code'] = value

    def __iter__(self):
        for item in self.__data.items():
            yield item

    def __getitem__(self, item):
        return self.__data[item]


class Agent(object):
    """Агент по предмету расчета
    :param srt agent_type: Типы признака агента по предмету расчета
    :param str phone: Телефон агента
    :param str name: Название агента (пример:"OOO 'Лютик'")
    :param str inn: ИНН Агента
    """

    def __init__(self, agent_type, phone=None, name=None, inn=None):
        self.__data = {
            'agent_info': {
                'type': agent_type
            }
        }
        self.set_supplier_info(name, phone and [phone], inn)

    def set_supplier_info(self, name=None, phones=None, inn=None):
        """ Передача атрибутов поставщика
        :param str name: Наименование поставщика
        :param list phones: Телефоны поставщика
        :param str inn: ИНН поставщика
        """
        if name or phones or inn:
            self.__data['supplier_info'] = {}
            if name:
                self.__data['supplier_info']['name'] = name
            if phones:
                self.__data['supplier_info']['phones'] = phones
            if inn:
                self.__data['supplier_info']['inn'] = inn

    def set_paying_agent_info(self, operation, phones):
        """ Передача атрибутов платежного агента
        :param str oparation: Наименование операции (максимальная длина строки – 24 символа)
        :param list phones: Телефоны платежного агента
        """
        self.__data['agent_info']['paying_agent'] = {
            'operation': operation,
            'phones': phones
        }

    def set_receive_payments_operator_info(self, phones):
        """ Передача атрибутов оператора по приему платежей
        :param list phones: Телефоны оператора по приему платежей
        """
        self.__data['agent_info']['receive_payments_operator'] = {
            'phones': phones
        }

    def set_money_transfer_operator_info(self, name=None, phones=None, address=None, inn=None):
        """ Передача атрибутов оператора перевода
        :param str name: Наименование оператора перевода
        :param list phones: Телефоны оператора по приему платежей
        :param str address: Адрес оператора перевода
        :param str inn: ИНН оператора перевода
        """
        self.__data['agent_info']['money_transfer_operator'] = {}

        if name is not None:
            self.__data['agent_info']['money_transfer_operator']['name'] = name

        if phones is not None:
            self.__data['agent_info']['money_transfer_operator']['phones'] = phones

        if address is not None:
            self.__data['agent_info']['money_transfer_operator']['address'] = address

        if inn is not None:
            self.__data['agent_info']['money_transfer_operator']['inn'] = inn

    def __iter__(self):
        for item in self.__data.items():
            yield item

    def __getitem__(self, item):
        return self.__data[item]


class BaseCheck(object):
    """ Базовый класс операций для обычного чека и чека коррекции """
    def __iter__(self):
        for item in self._data.items():
            yield item

    def __getitem__(self, item):
        return self._data[item]

    def set_print(self, value):
        """
        :param bool value: Печатать чек или нет
        """
        self._data['print'] = bool(value)
        return self

    def add_payment(self, amount, method=PaymentMethod.CARD):
        """
        :param int|float amount: Сумма платежа
        :param str method: Метод оплаты
        """
        self._data['payments'].append({'sum': amount, 'type': method})
        return self

    def set_cashier(self, name, inn=None):
        """
        :param str name: Ф.И.О. кассира
        :param str inn: ИНН кассира
        """
        self._data['cashier'] = {'name': name}

        if inn:
            self._data['cashier']['inn'] = inn

        return self

    def set_additional_check_props(self, value):
        """
        :param str value: Дополнительный реквизит чека
        """
        self._data['additional_check_props'] = value

    def set_additional_user_props(self, name, value):
        """
        :param str name: Наименование дополнительного реквизита пользователя
        :param str value: Значение дополнительного реквизита пользователя
        """
        self._data['additional_user_props'] = {
            'name': name,
            'value': value
        }

    # Deprecated
    def add_cashier(self, name, inn=None):
        return self.set_cashier(name, inn)

    def add_position(self, name, price, quantity=1, total=None, vat=VatRate.RATE_NO,
                     measure_name=None, oid=None, calculation_method=None,
                     calculation_subject=None, excise=None, country_code=None,
                     declaration_number=None, agent=None, nomenclature=None, user_data=None):
        """
        :param str name: Наименование позиции
        :param int|float price: Цена позиции в чеке
        :param int|float quantity: Количество единиц
        :param int|float total: Общая стоимость позиции
        :param str vat: Налоговая ставка
        :param str measure_name: Единица измерения
        :param str oid: Идентификатор позиции в магазине
        :param str calculation_method: Cпособ рассчета
        :param str calculation_subject: Признак рассчета
        :param int|float excise: Сумма акциза
        :param str country_code: Цифровой код страны происхождения товара
        :param str declaration_number: Номер таможенной декларации
        :param Agent agent: Экземпляр агента
        :param Nomenclature nomenclature: Экземпляр кода номенклатуры (маркировки)
        :param str user_data: Дополнительный предмет расчёта
        """
        if total is None:
            total = price * quantity

        position = {
            'name': name,
            'price': price,
            'quantity': quantity,
            'total': total,
            'vat': VatRate.parse(vat)
        }

        if measure_name is not None:
            position['measure_name'] = measure_name

        if oid is not None:
            position['id'] = oid

        if calculation_method is not None:
            position['calculation_method'] = calculation_method

        if calculation_subject is not None:
            position['calculation_subject'] = calculation_subject

        if excise is not None:
            position['excise'] = excise

        if country_code is not None:
            position['country_code'] = country_code

        if declaration_number is not None:
            position['declaration_number'] = declaration_number

        if agent is not None:
            position.update(dict(agent))

        if nomenclature is not None:
            position.update(dict(nomenclature))

        if user_data is not None:
            position['user_data'] = user_data

        self._data['positions'].append(position)
        return self

    def set_callback_url(self, url):
        """
        :param str callback: URL, на который необходимо ответить после обработки чека
        """
        self._data['callback_url'] = url
        return self


class Check(BaseCheck):
    """
    :param oid: Номер операции в магазине
    :param str email: E-Mail пользователя для отправки электронного чека
    :param str intent: Направление платежа
    :param int tax_system: Система налогообложения
    :param str payment_address: Место расчетов
    """

    def __init__(self, oid, email, intent, tax_system, payment_address=None):
        self._data = {
            'external_id': oid,
            'user': email,
            'print': False,
            'intent': intent,
            'sno': tax_system,
            'payments': [],
            'positions': []
        }
        if payment_address:
            self._data['payment_address'] = payment_address

    def set_client(self, name=None, inn=None):
        """
        :param str name: Наименование покупателя
        :param str inn: ИНН покупателя
        """

        self._data['client'] = {}

        if name:
            self._data['client']['name'] = name

        if inn:
            self._data['client']['inn'] = inn

        if not self._data['client']:
            del self._data['client']

        return self

    def set_agent(self, agent):
        """
        :param Agent agent: агент на чек
        """
        self._data.update(dict(agent))

    def apply_discount(self, discount):
        """
        :param int|float discount: сумма скидки
        """
        apply_discount(discount, self._data['positions'])

    def apply_correction_positions(self):
        """
        Кооректировка позиций с расхождениями между price * quantity и total
        """
        self._data['positions'] = correction_positions(self._data['positions'])


class CorrectionCheck(BaseCheck):
    """
    :param oid: Номер операции в магазине
    :param str intent: Тип чека коррекции
    :param int sno: Система налогообложения
    """

    def __init__(self, oid, intent, sno):

        self._data = {
            'external_id': oid,
            'intent': intent,
            'sno': sno,
            'print': False,
            'payments': [],
            'positions': [],
            'correction': None
        }

    def set_correction_data(self, type, date, document_number, description):
        """
        :param int type: Тип коррекции
        :param str date: Дата документа коррекции
        :param str document_number: № документа коррекции
        :param str description: Описание коррекции
        """

        self._data['correction'] = {
            'type': type,
            'date': date,
            'document': document_number,
            'description': description
        }
        return self

    def set_authorised_person(self, name, inn=None):
        """
        :param str name: Ф.И.О. кассира
        :param str inn: ИНН кассира
        """
        self._data['authorised_person'] = {'name': name}

        if inn:
            self._data['authorised_person']['inn'] = inn

        return self
