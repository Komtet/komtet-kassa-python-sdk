# coding: utf-8
from komtet_kassa_sdk.v2.lib.helpers import apply_discount, correction_positions


class MarkTypes(object):
    """Типы маркировок"""

    UNKNOWN = 'unknown'
    EAN8 = 'ean8'
    EAN13 = 'ean13'
    ITF14 = 'itf14'
    GS10 = 'gs10'
    GS1M = 'gs1m'
    SHORT = 'short'
    FUR = 'fur'
    EGAIS20 = 'egais20'
    EGAIS30 = 'egais30'


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


class MesureTypes(object):
    PIECE = 0
    GRAMM = 10
    KILOGRAMM = 11
    TON = 12
    CENTIMETER = 20
    DECIMETER = 21
    METER = 22
    SQUARE_CENTIMETER = 30
    SQUARE_DECIMETER = 31
    SQUARE_METER = 32
    MILLILITER = 40
    LITER = 41
    CUBIC_METER = 42
    KILOWATT_HOUR = 50
    GIGA_CALORIE = 51
    DAY = 70
    HOUR = 71
    MINUTE = 72
    SECOND = 73
    KILOBYTE = 80
    MEGABYTE = 81
    GIGABYTE = 82
    TERABYTE = 83
    OTHER_MEASURMENTS = 255


class PaymentType(object):
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

    INSTRUCTION = 'instruction'
    """По предписанию"""


class PaymentMethod(object):
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


class PaymentObject(object):
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

    DEPOSIT = 'deposit'
    """Залог"""

    CONSUMPTION = 'consumption'
    """Расход"""

    SOLE_PROPRIETOR_CPI_CONTRIBUTINS = 'sole_proprietor_cpi_contributins'
    """взносы на ОПС ИП"""

    CPI_CONTRIBUTINS = 'cpi_contributins'
    """взносы на ОПС"""

    SOLE_PROPRIETOR_CMI_CONTRIBUTINS = 'sole_proprietor_cmi_contributins'
    """взносы на ОМС ИП"""

    CMI_CONTRIBUTINS = 'cmi_contributins'
    """взносы на ОМС"""

    CSI_CONTRIBUTINS = 'csi_contributins'
    """взносы на ОСС"""

    CASINO_PAYMENT = 'casino_payment'
    """платеж казино"""

    PAYMENT_OF_THE_MONEY = 'payment_of_the_money'
    """выдача денежных средств банковским платежным агентом"""

    ATNM = 'atnm'
    """
    Реализация подакцизного товара, подлежащего маркировке средством
    идентификации, но не имеющего кода маркировки
    """

    ATM = 'atm'
    """
    Реализация подакцизного товара, подлежащего маркировке средством идентификации,
    и  имеющего код маркировки
    """

    TNM = 'tnm'
    """
    Реализация товара, подлежащего маркировке средством идентификации,
    но не имеющего кода маркировки, за исключением подакцизного товара
    """

    TM = 'tm'
    """
    Реализация товара, подлежащего маркировке средством идентификации,
    и имеющего код маркировки, за исключением подакцизного товара
    """


class Check(object):
    """
    :param oid: Номер операции в магазине
    :param str intent: Направление платежа
    """

    def __init__(self, oid, intent):
        self.__data = {
            'external_id': oid,
            'client': {},
            'company': {},
            'print': False,
            'intent': intent,
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

    def add_payment(self, amount, method=PaymentType.CARD):
        """
        :param int|float amount: Сумма платежа
        :param str method: Метод оплаты
        """
        self.__data['payments'].append({'sum': amount,
                                        'type': method})
        return self

    def set_client(self, email=None, phone=None, name=None, inn=None, birthdate=None, citizenship=None, document_code=None, document_data=None, address=None):
        """
        :param str email: Email покупателя
        :param str phone: Телефон покупателя
        :param str name: Наименование покупателя
        :param str inn: ИНН покупателя
        :param str birthdate: Дата рождения покупателя
        :param str citizenship: Код города покупателя
        :param str document_code: Код документа покупателя
        :param str document_data: Даннае документа покупателя
        :param str address: Адрес покупателя
        """

        if email:
            self.__data['client']['email'] = email

        if name:
            self.__data['client']['name'] = name

        if phone:
            self.__data['client']['phone'] = phone

        if inn:
            self.__data['client']['inn'] = inn

        if birthdate:
            self.__data['client']['birthdate'] = birthdate

        if citizenship:
            self.__data['client']['citizenship'] = citizenship

        if document_code:
            self.__data['client']['document_code'] = document_code

        if document_data:
            self.__data['client']['document_data'] = document_data

        if address:
            self.__data['client']['address'] = address

        return self

    def set_company(self, payment_address, tax_system, inn=None, place_address=None):
        """
        :param str payment_address: Платёжный адрес компании
        :param str tax_system: Система налогообложения
        """

        self.__data['company'] = {'payment_address': payment_address, 'sno': tax_system}

        if inn:
            self.__data['company']['inn'] = inn

        if place_address:
            self.__data['company']['place_address'] = place_address

        return self

    def set_cashier(self, name, inn=None):
        """
        :param str name: Ф.И.О. кассира
        :param str inn: ИНН кассира
        """
        self.__data['cashier'] = {'name': name}

        if inn:
            self.__data['cashier']['inn'] = inn

        return self

    def set_additional_check_props(self, value):
        """
        :param str value: Дополнительный реквизит чека
        """
        self.__data['additional_check_props'] = value

    def set_additional_user_props(self, name, value):
        """
        :param str name: Наименование дополнительного реквизита пользователя
        :param str value: Значение дополнительного реквизита пользователя
        """
        self.__data['additional_user_props'] = {
            'name': name,
            'value': value
        }

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

    def add_position(self, position):
        """
        :param Position position: Экземпляр позиции
        """
        self.__data['positions'].append(dict(position))

    def set_callback_url(self, url):
        """
        :param str callback: URL, на который необходимо ответить после обработки чека
        """
        self.__data['callback_url'] = url
        return self

    def apply_discount(self, discount):
        """
        :param int|float discount: сумма скидки
        """
        apply_discount(discount, self.__data['positions'])

    def apply_correction_positions(self):
        """
        Кооректировка позиций с расхождениями между price * quantity и total
        """
        self.__data['positions'] = correction_positions(self.__data['positions'])


class CorrectionCheck(object):
    """
    :param oid: Номер операции в магазине
    :param str intent: Тип чека коррекции
    """

    def __init__(self, oid, intent):

        self.__data = {
            'external_id': oid,
            'intent': intent,
            'client': {},
            'payments': [],
            'positions': [],
        }

    def __iter__(self):
        for item in self.__data.items():
            yield item

    def __getitem__(self, item):
        return self.__data[item]

    def set_client(self, email=None, phone=None, name=None, inn=None, birthdate=None, citizenship=None,
                   document_code=None, document_data=None, address=None):
        """
        :param str email: Email покупателя
        :param str phone: Телефон покупателя
        :param str name: Наименование покупателя
        :param str inn: ИНН покупателя
        :param str birthdate: Дата рождения покупателя
        :param str citizenship: Код города покупателя
        :param str document_code: Код документа покупателя
        :param str document_data: Даннае документа покупателя
        :param str address: Адрес покупателя
        """

        if email:
            self.__data['client']['email'] = email

        if name:
            self.__data['client']['name'] = name

        if phone:
            self.__data['client']['phone'] = phone

        if inn:
            self.__data['client']['inn'] = inn

        if birthdate:
            self.__data['client']['birthdate'] = birthdate

        if citizenship:
            self.__data['client']['citizenship'] = citizenship

        if document_code:
            self.__data['client']['document_code'] = document_code

        if document_data:
            self.__data['client']['document_data'] = document_data

        if address:
            self.__data['client']['address'] = address

        return self

    def set_cashier(self, name, inn=None):
        """
        :param str name: Ф.И.О. кассира
        :param str inn: ИНН кассира
        """
        self.__data['cashier'] = {'name': name}

        if inn:
            self.__data['cashier']['inn'] = inn

        return self

    def set_additional_check_props(self, value):
        """
        :param str value: Дополнительный реквизит чека
        """
        self.__data['additional_check_props'] = value

    def set_additional_user_props(self, name, value):
        """
        :param str name: Наименование дополнительного реквизита пользователя
        :param str value: Значение дополнительного реквизита пользователя
        """
        self.__data['additional_user_props'] = {
            'name': name,
            'value': value
        }

    def set_correction_info(self, type, base_date, base_number, base_name=''):
        """
        :param int type: Тип коррекции
        :param str base_date: Дата документа коррекции
        :param str base_number: № документа коррекции
        :param str base_name: Описание коррекции
        """

        self.__data['correction_info'] = {
            'type': type,
            'base_date': base_date,
            'base_number': base_number,
            'base_name': base_name
        }
        return self

    def set_company(self, payment_address, tax_system):
        """
        :param str payment_address: Платёжный адрес компании
        :param str tax_system: Система налогообложения
        """

        self.__data['company'] = {'payment_address': payment_address, 'sno': tax_system}

        return self

    def add_payment(self, amount, method=PaymentType.CARD):
        """
        :param int|float amount: Сумма платежа
        :param str method: Метод оплаты
        """
        self.__data['payments'].append({'sum': amount,
                                        'type': method})
        return self

    def set_authorised_person(self, name, inn=None):
        """
        :param str name: Ф.И.О. кассира
        :param str inn: ИНН кассира
        """
        self.__data['authorised_person'] = {'name': name}

        if inn:
            self.__data['authorised_person']['inn'] = inn

        return self

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

    def set_callback_url(self, url):
        """
        :param str callback: URL, на который необходимо ответить после обработки чека
        """
        self.__data['callback_url'] = url
        return self

    def add_position(self, position):
        """
        :param Position position: Экземпляр позиции
        """
        self.__data['positions'].append(dict(position))


class Position(object):
    """
        :param str name: Наименование позиции
        :param int|float price: Цена позиции в чеке
        :param int|float quantity: Количество единиц
        :param str measure: Единица измерения
        :param str payment_method: Cпособ рассчета
        :param str payment_subject: Признак рассчета
        :param int|float total: Общая стоимость позиции
        :param str user_data: Дополнительный реквизит предмета расчета
        :param int|float excise: Сумма акциза
        :param str id: Идентификатор позиции в магазине
        :param str country_code: Цифровой код страны происхождения товара
        :param str declaration_number: Номер таможенной декларации
        :param str vat: Налоговая ставка
    """

    def __init__(self, name, price, quantity, measure, payment_object, payment_method, total=None,
                 user_data=None, excise=None, id=None, country_code=None, declaration_number=None,
                 vat=VatRate.RATE_NO):
        if total is None:
            total = price * quantity

        self.__data = {
            'name': name,
            'measure': measure,
            'price': price,
            'quantity': quantity,
            'payment_object': payment_object,
            'payment_method': payment_method,
            'total': total,
            'vat': VatRate.parse(vat)
        }

        if measure is not None:
            self.__data['measure'] = measure

        if id is not None:
            self.__data['id'] = id

        if excise is not None:
            self.__data['excise'] = excise

        if country_code is not None:
            self.__data['country_code'] = country_code

        if user_data is not None:
            self.__data['user_data'] = user_data

        if declaration_number is not None:
            self.__data['declaration_number'] = declaration_number

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
