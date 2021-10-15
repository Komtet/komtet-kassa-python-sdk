

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

    def set_paying_agent(self, operation, phones):
        """ Передача атрибутов платежного агента
        :param str oparation: Наименование операции (максимальная длина строки – 24 символа)
        :param list phones: Телефоны платежного агента
        """
        self.__data['agent_info']['paying_agent'] = {
            'operation': operation,
            'phones': phones
        }

    def set_receive_payments_operator(self, phones):
        """ Передача атрибутов оператора по приему платежей
        :param list phones: Телефоны оператора по приему платежей
        """
        self.__data['agent_info']['receive_payments_operator'] = {
            'phones': phones
        }

    def set_money_transfer_operator(self, name=None, phones=None, address=None, inn=None):
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
