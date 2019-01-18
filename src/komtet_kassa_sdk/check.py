# coding: utf-8


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

    RETURN_CORRECTION = 'sellReturnCorrection'
    """Коррекция расхода"""


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
        elif rate == '20/120':
            rate = cls.RATE_120
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

    OTHER = 'other'
    """О предмете расчета, не относящемуся к предметам расчета, которым может быть присвоено
       значение от «0» до «12» (0-12 -- это вышеперечисленные)"""


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
        if phone and name and inn:
            self.set_supplier_info(name, [phone], inn)

    def set_supplier_info(self, name, phones, inn):
        """ Передача атрибутов поставщика
        :param str name: Наименование поставщика
        :param list phones: Телефоны поставщика
        :param str inn: ИНН поставщика
        """
        self.__data['supplier_info'] = {
            'phones': phones,
            'name': name,
            'inn': inn
        }

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

    def set_money_transfer_operator_info(self, name, phones, address, inn):
        """ Передача атрибутов оператора перевода
        :param str name: Наименование оператора перевода
        :param list phones: Телефоны оператора по приему платежей
        :param str address: Адрес оператора перевода
        :param str inn: ИНН оператора перевода
        """
        self.__data['agent_info']['money_transfer_operator'] = {
            'name': name,
            'phones': phones,
            'address': address,
            'inn': inn
        }

    def __iter__(self):
        for item in self.__data.items():
            yield item

    def __getitem__(self, item):
        return self.__data[item]


class Check(object):
    """
    :param oid: Номер операции в магазине
    :param str email: E-Mail пользователя для отправки электронного чека
    :param str intent: Направление платежа
    :param int tax_system: Система налогообложения
    :param str payment_address: Место расчетов
    """

    def __init__(self, oid, email, intent, tax_system, payment_address=None):
        self.__data = {
            'task_id': oid,
            'user': email,
            'print': False,
            'intent': intent,
            'sno': tax_system,
            'payments': [],
            'positions': []
        }
        if payment_address:
            self.__data['payment_address'] = payment_address

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

    def add_payment(self, amount, method=PaymentMethod.CARD):
        """
        :param int|float amount: Сумма платежа
        :param str method: Метод оплаты
        """
        self.__data['payments'].append({'sum': amount,
                                        'type': method})
        return self

    def add_cashier(self, name, inn):
        """
        :param str name: Ф.И.О. кассира
        :param int inn: ИНН кассира
        """
        self.__data['cashier'] = {'name': name,
                                  'inn': inn}
        return self

    def add_position(self, name, price, quantity=1, total=None, vat=VatRate.RATE_NO,
                     measure_name=None, oid=None, calculation_method=None,
                     calculation_subject=None, agent=None):
        """
        :param str name: Наименование позиции
        :param int|float price: Цена позиции в чеке
        :param int|float quantity: Количество единиц
        :param int|float total: Общая стоимость позиции
        :param str vat: Налоговая ставка
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

        if agent is not None:
            position.update(dict(agent))

        self.__data['positions'].append(position)
        return self

    def set_callback_url(self, url):
        """
        :param str callback: URL, на который необходимо ответить после обработки чека
        """
        self.__data['callback_url'] = url
        return self


class CorrectionCheck(object):
    """
    :param oid: Номер операции в магазине
    :param str printer_number: Серийный номер принтера
    :param str intent: Тип чека коррекции
    :param int tax_system: Система налогообложения
    :param str vat: Налоговая ставка
    """

    def __init__(self, oid, printer_number, intent, tax_system=None):

        self.__data = {
            'task_id': oid,
            'printer_number': printer_number,
            'intent': intent,
            'payments': [],
            'positions': [],
            'correction': None
        }
        if tax_system is not None:
            self.__data['sno'] = tax_system

    def __iter__(self):
        for item in self.__data.items():
            yield item

    def __getitem__(self, item):
        return self.__data[item]

    def set_correction_data(self, type, date, document_number, description):
        """
        :param int type: Тип коррекции
        :param str date: Дата документа коррекции
        :param str document_number: № документа коррекции
        :param str description: Описание коррекции
        """

        self.__data['correction'] = {
            'type': type,
            'date': date,
            'document': document_number,
            'description': description
        }
        return self

    def set_payment(self, amount, vat, method=PaymentMethod.CARD):
        """
        :param int|float amount: Сумма платежа
        :param str vat: Налоговая ставка
        :param str method: Метод оплаты
        """
        self.__data['payments'] = [{'sum': amount,
                                    'type': method}]
        self.__data['positions'] = [{
            'name': ('Коррекция прихода'
                     if self.__data['intent'] == Intent.SELL_CORRECTION else
                     'Коррекция расхода'),
            'price': amount,
            'quantity': 1,
            'total': amount,
            'vat': vat
        }]
        return self

    def set_authorised_person(self, name, inn):
        """
        :param str name: Ф.И.О. кассира
        :param int inn: ИНН кассира
        """
        self.__data['authorised_person'] = {
            'name': name,
            'inn': inn
        }
        return self

    def set_callback_url(self, url):
        """
        :param str callback: URL, на который необходимо ответить после обработки чека
        """
        self.__data['callback_url'] = url
        return self
