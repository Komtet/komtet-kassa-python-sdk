=======================
komtet-kassa-python-sdk
=======================

Библиотека для интеграции вашего сайта с с облачным сервисом распределенной печати чеков `КОМТЕТ Касса <http://kassa.komtet.ru>`_

.. image:: https://img.shields.io/travis/Komtet/komtet-kassa-python-sdk.svg?style=flat-square
  :target: https://travis-ci.org/Komtet/komtet-kassa-python-sdk

Установка
=========

С помощью pip:

.. code:: bash

    # pip install komtet_kassa_sdk

Вручную:

.. code:: bash

    $ git clone https://github.com/Komtet/komtet-kassa-python-sdk
    $ cd komtet-kassa-python-sdk
    # python setup.py install


Использование v2
================

.. code:: python

    from requests.exceptions import HTTPError
    from komtet_kassa_sdk.v2 import (
        Check, CorrectionCheck, Client, Intent, TaxSystem, VatRate, CorrectionType, PaymentMethod,
        Agent, AgentType, PaymentType, PaymentObject, MarkTypes,
    )

    shop_id = 'идентификатор магазина'
    secret_key = 'секретный ключ'
    client = Client(shop_id, secret_key)

    oid = 'номер операции в вашем магазине'
    intent = Intent.SELL  # Направление платежа
    # Используйте Intent.RETURN для оформления возврата

    check = Check(oid, intent)

    email = 'client@client.ru'   # E-Mail пользователя для отправки электронного чека
    phone = '+79992400041'       # Телефон пользователя
    name = 'Иванов Иван'         # Имя пользователя
    inn = '516954782202'         # Инн пользователя

    check.set_client(email=email, phone=phone, name=name, inn=inn)

    payment_address = 'www.shop.com'   # Платёжный адрес организации

    # Система налогооблажения
    tax_system = TaxSystem.COMMON  # ОСН
    # tax_system = TaxSystem.SIMPLIFIED_IN  # УСН доход
    # tax_system = TaxSystem.SIMPLIFIED_IN_OUT  # УСН доход - расход
    # tax_system = TaxSystem.UTOII  # ЕНВД
    # tax_system = TaxSystem.UST  # ЕСН
    # tax_system = TaxSystem.PATENT  # Патент

    check.set_company(payment_address=payment_address, tax_system=tax_system)

    position_name = 'Наименование позиции'
    position_price = 100  # Цена позиции

    # Единицы измерений
    measure = MesureTypes.PIECE
    # measure = MesureTypes.PIECE
    # measure = MesureTypes.GRAMM
    # measure = MesureTypes.KILOGRAMM
    # measure = MesureTypes.TON
    # measure = MesureTypes.CENTIMETER
    # measure = MesureTypes.DECIMETER
    # measure = MesureTypes.METER
    # measure = MesureTypes.SQUARE_CENTIMETER
    # measure = MesureTypes.SQUARE_DECIMETER
    # measure = MesureTypes.SQUARE_METER
    # measure = MesureTypes.MILLILITER
    # measure = MesureTypes.LITER
    # measure = MesureTypes.CUBIC_METER
    # measure = MesureTypes.KILOWATT_HOUR
    # measure = MesureTypes.GIGA_CALORIE
    # measure = MesureTypes.DAY
    # measure = MesureTypes.HOUR
    # measure = MesureTypes.MINUTE
    # measure = MesureTypes.SECOND
    # measure = MesureTypes.KILOBYTE
    # measure = MesureTypes.MEGABYTE
    # measure = MesureTypes.GIGABYTE
    # measure = MesureTypes.TERABYTE
    # measure = MesureTypes.OTHER_MEASURMENTS

    # Налоговая ставка
    vat_rate = VatRate.RATE_NO  # Без НДС
    # vat_rate = VatRate.RATE_20  # НДС 20%
    # vat_rate = VatRate.RATE_0  # НДС 0%
    # vat_rate = VatRate.RATE_10  # НДС 10%
    # vat_rate = VatRate.RATE_110  # НДС 10/110
    # vat_rate = VatRate.RATE_120  # НДС 20/120

    #Способ расчёта
    payment_method = PaymentMethod.PRE_PAYMENT_FULL
    # payment_method = PaymentMethod.PRE_PAYMENT_PART
    # payment_method = PaymentMethod.FULL_PAYMENT
    # payment_method = PaymentMethod.ADVANCE
    # payment_method = PaymentMethod.CREDIT_PART
    # payment_method = PaymentMethod.CREDIT_PAY
    # payment_method = PaymentMethod.CREDIT


    # Признак рассчета
    payment_object = PaymentObject.PRODUCT
    # payment_object = PaymentObject.PRODUCT_PRACTICAL
    # payment_object = PaymentObject.WORK
    # payment_object = PaymentObject.SERVICE
    # payment_object = PaymentObject.GAMBLING_BET
    # payment_object = PaymentObject.GAMBLING_WIN
    # payment_object = PaymentObject.LOTTERY_BET
    # payment_object = PaymentObject.LOTTERY_WIN
    # payment_object = PaymentObject.RID
    # payment_object = PaymentObject.PAYMENT
    # payment_object = PaymentObject.COMMISSION
    # payment_object = PaymentObject.COMPOSITE
    # payment_object = PaymentObject.PAY
    # payment_object = PaymentObject.OTHER
    # payment_object = PaymentObject.PROPERTY_RIGHT
    # payment_object = PaymentObject.NON_OPERATING
    # payment_object = PaymentObject.INSURANCE
    # payment_object = PaymentObject.SALES_TAX
    # payment_object = PaymentObject.RESORT_FEE
    # payment_object = PaymentObject.DEPOSIT
    # payment_object = PaymentObject.CONSUMPTION
    # payment_object = PaymentObject.SOLE_PROPRIETOR_CPI_CONTRIBUTINS
    # payment_object = PaymentObject.CPI_CONTRIBUTINS
    # payment_object = PaymentObject.SOLE_PROPRIETOR_CMI_CONTRIBUTINS
    # payment_object = PaymentObject.CMI_CONTRIBUTINS
    # payment_object = PaymentObject.CSI_CONTRIBUTINS
    # payment_object = PaymentObject.CASINO_PAYMENT
    # payment_object = PaymentObject.PAYMENT_OF_THE_MONEY
    # payment_object = PaymentObject.ATHM
    # payment_object = PaymentObject.ATM
    # payment_object = PaymentObject.THM
    # payment_object = PaymentObject.TM

    # Создание позиции
    position = Position(id=1,  # Идентификатор позиции в магазине
                        name='Наименование позиции',
                        price=10, # Цена за единицу
                        quantity=1,  # Количество единиц
                        total=10, # Общая стоимость позиции
                        excise=10, # Акциз
                        measure=measure, # Единица измерения
                        user_data='Дополнительный реквизит предмета расчета',
                        payment_method=payment_method, # Метод расчёта
                        vat=vat_rate,  # Тип налога
                        payment_object=payment_object # Объект расчёта
    )

    # Типы маркировок
    mark_type = MarkTypes.EAN13
    # mark_type = MarkTypes.UNKNOWN
    # mark_type = MarkTypes.EAN8
    # mark_type = MarkTypes.ITF14
    # mark_type = MarkTypes.GS10
    # mark_type = MarkTypes.GS1M
    # mark_type = MarkTypes.SHORT
    # mark_type = MarkTypes.FUR
    # mark_type = MarkTypes.EGAIS20
    # mark_type = MarkTypes.EGAIS30

    # Добавление кода маркировки в позицию
    position.set_mark_code(type=mark_type, code='1234567890123')

    # Установка дробности маркированного товара
    position.set_mark_quantity(numerator=1, denominator=2)

    # Если нужна информация о агенте

    # Создание агента
    agent_info = Agent(agent_type=AgentType.AGENT, phone='+79998887766',
                        name='Названиепоставщика', inn='287381373424')

    # Если нужно, установка платёжного агента
    agent_info.set_paying_agent(operation='Операция1', phones=['+79998887766'])

    # Если нужно, установка оператора приёма платежей
    agent_info.set_receive_payments_operator(phones=['+79998887766'])

    # Если нужно, установка оператора перевода средств
    agent_info.set_money_transfer_operator(phones=['+79998887766'], name='Операторперевода',
                                            address='г. Москва, ул. Складочная д.3',
                                            inn='8634330204')

    # Добавление агента в позицию
    position.set_agent(agent_info)

    # Добавление позиции
    check.add_position(position)

    # Добавление суммы расчёта
    check.add_payment(300)

    # Если нужно распечатать чек (по умолчанию False)
    check.set_print(True)

    # Если нужно задать данные по кассиру, по умолчанию возьмутся с ФН
    check.set_cashier('Иваров И.П.', '1234567890123')

    # Если нужно установить дополнительные параметры чека
    check.set_additional_check_props('445334544')

    # Если нужно получитиь отчёт об успешной фискализации
    check.set_callback_url('http://shop.pro/fiscal_check/callback')

    # Отправка запроса
    try:
        task = client.create_task(check, 'идентификатор очереди')
    except HTTPError as exc:
        print(exc.response.text)
    else:
        print(task)
    # Task(id=1, external_id=2, print_queue_id=3, state='new')
    # id - идентификатор задачи
    # external_id - идентификатор операции в магазине
    # print_queue_id - идентификатор очереди
    # state - состояние задачи


    # Создание чека коррекции

    intent = Intent.SELL_CORRECTION  # Коррекция прихода
    # intent = Intent.BUY_CORRECTION # Коррекция расхода
    # intent = Intent.SELL_RETURN_CORRECTION # Коррекция возврата прихода
    # intent = Intent.BUY_RETURN_CORRECTION # Коррекция возврата расхода

    check = CorrectionCheck(oid, intent, sno)

    # Установка данных компании
    check.set_company(payment_address=payment_address, tax_system=tax_system)

    payment_type = PaymentType.CARD # Тип оплаты, корректирующей суммы
    # payment_method = PaymentType.CARD # электронные
    # payment_method = PaymentType.CASH # наличные

    # Установка суммы коррекции
    check.add_payment(12, payment_type)

    correction_type = CorrectionType.SELF # Тип коррекции
    # correction_type = CorrectionType.SELF # Самостоятельно
    # correction_type = CorrectionType.FORCED # По предписанию

    # Установка данных коррекции
    check.set_correction_info(correction_type,
                                '2017-09-28', # Дата документа коррекции в формате 'yyyy-mm-dd'
                                'K11',        # Номер документа коррекции
                                'Отключение электричества'     # Описание коррекции
    )

    # Создаём позицию коррекции
    position = Position(name='Товар', price=10, quantity=5, total=50,
                        measure=measure_type, payment_method=payment_method,
                        payment_object=payment_object, vat=vat_rate)

    # Добавляем позицию коррекции
    check.add_position(position)

    # Указание уполномоченного лица
    check.set_authorised_person(
        name='Иванов И.И',
        inn='123456789012'
    )

    # Если нужно получитиь отчёт об успешной фискализации
    check.set_callback_url('http://shop.pro/fiscal_check/callback')

    # Отправка запроса
    try:
        task = client.create_task(check, 'идентификатор очереди')
    except HTTPError as exc:
        print(exc.response.text)
    else:
        print(task)
    # Task(id=1, external_id=2, print_queue_id=3, state='new')
    # id - идентификатор задачи
    # external_id - идентификатор операции в магазине
    # print_queue_id - идентификатор очереди
    # state - состояние задачи

    # Получение информации о поставленной на фискализацию задаче:
    try:
        task_info = client.get_task_info('идентификатор задачи')
    except HTTPError as exc:
        print(exc.response.text)
    else:
        print(task_info)
    # TaskInfo(id=234, external_id='4321', state='done', error_description=None,
    #          fiscal_data={'i': '111',
    #                       'fn': '2222222222222222',
    #                       't': '3333333333333',
    #                       'n': 4,
    #                       'fp': '555555555',
    #                       's': '6666.77'})
    # id - идентификатор задачи
    # external_id - идентификатор операции в магазине
    # state - состояние задачи
    # error_description - описание возникшей ошибки, когда state=='error'
    # fiscal_data - фискальные данные



    # Чтобы проверить, является ли очередь активной, выполните:
    client.is_queue_active('идентификатор очереди')

    # Вы можете указать идентификатор очереди по умолчанию с помощью:
    client.set_default_queue('идентификатор очереди по умолчанию')
    # В этом случае можно не указывать идентификатор очереди всякий раз,
    # когда нужно распечатать чек или проверить состояние очереди:
    assert client.is_queue_active() is True
    try:
        task = client.create_task(check)
    except HTTPError as exc:
        print(exc.response.text)
    else:
        print(task)


Использование v1
================

.. code:: python

    from requests.exceptions import HTTPError
    from komtet_kassa_sdk.v1 import (
        Check, CorrectionCheck, Client, Intent, TaxSystem, VatRate, CorrectionType, PaymentMethod,
        Agent, AgentType, CalculationSubject, CalculationMethod
    )

    shop_id = 'идентификатор магазина'
    secret_key = 'секретный ключ'
    client = Client(shop_id, secret_key)

    oid = 'номер операции в вашем магазине'
    email = 'E-Mail пользователя для отправки электронного чека'

    intent = Intent.SELL  # Направление платежа
    # Используйте Intent.RETURN для оформления возврата

    # Система налогооблажения
    tax_system = TaxSystem.COMMON  # ОСН
    # tax_system = TaxSystem.SIMPLIFIED_IN  # УСН доход
    # tax_system = TaxSystem.SIMPLIFIED_IN_OUT  # УСН доход - расход
    # tax_system = TaxSystem.UTOII  # ЕНВД
    # tax_system = TaxSystem.UST  # ЕСН
    # tax_system = TaxSystem.PATENT  # Патент

    check = Check(oid, email, intent, tax_system)

    position_name = 'Наименование позиции'
    position_price = 100  # Цена позиции
    check.add_position(position_name, position_price)

    # Налоговая ставка
    vat_rate = VatRate.RATE_20  # НДС 20%
    # vat_rate = VatRate.RATE_NO  # Без НДС
    # vat_rate = VatRate.RATE_0  # НДС 0%
    # vat_rate = VatRate.RATE_10  # НДС 10%
    # vat_rate = VatRate.RATE_110  # НДС 10/110
    # vat_rate = VatRate.RATE_120  # НДС 20/120
    # Можно указать просто число:
    # vat_rate = 20
    # или строку:
    # vat_rate = '10'
    # или даже так:
    # vat_rate = '20%'
    # а ещё вот так:
    # vat_rate = 0.20

    # Добавление позиции
    check.add_position(
        'Наименование позиции',
        oid=123,  # Идентификатор позиции в магазине
        price=100,  # Цена за единицу
        quantity=2,  # Количество единиц (по умолчанию 1)
        total=200,  # Общая стоимость позиции (по умолчанию price * quantity)
        vat=vat_rate  # По умолчанию Без НДС (VatRate.RATE_NO),

        calculation_method=CalculationMethod.FULL_PAYMENT, # По умолчанию FULL_PAYMENT
        calculation_subject=CalculationSubject.PRODUCT, # По умолчанию PRODUCT

        # Необязательный атрибут, указывается только при продаже комиссионером собственных и
        # комиссионных товаров
        agent = Agent(AgentType.COMMISSIONAIRE, '+77777777777', 'ООО "Лютик"', '12345678901')
    )

    # Добавление суммы расчёта
    check.add_payment(300)

    # Если нужно распечатать чек (по умолчанию False)
    check.set_print(True)

    # Если нужно задать данные по кассиру, по умолчанию возьмутся с ФН
    check.set_cashier('Иваров И.П.', '1234567890123')

    # Если нужно нужно передать данные клиента для фискализации
    check.set_client('Пупкин П.П.', '123412341234')

    # Отправка запроса
    try:
        task = client.create_task(check, 'идентификатор очереди')
    except HTTPError as exc:
        print(exc.response.text)
    else:
        print(task)
    # Task(id=1, external_id=2, print_queue_id=3, state='new')
    # id - идентификатор задачи
    # external_id - идентификатор операции в магазине
    # print_queue_id - идентификатор очереди
    # state - состояние задачи


    # Создание чека коррекции

    intent = Intent.SELL_CORRECTION  # Коррекция прихода
    # intent = Intent.BUY_CORRECTION # Коррекция расхода
    # intent = Intent.SELL_RETURN_CORRECTION # Коррекция возврата прихода
    # intent = Intent.BUY_RETURN_CORRECTION # Коррекция возврата расхода

    check = CorrectionCheck(oid, intent, sno)

    payment_method = PaymentMethod.CARD # Метод оплаты, корректирующей суммы
    # payment_method = PaymentMethod.CARD # электронные
    # payment_method = PaymentMethod.CASH # наличные

    # Установка суммы коррекции
    check.add_payment(
      correction_sum=12, # Сумма
      payment_method=payment_method
    )

    correction_type = CorrectionType.SELF # Тип коррекции
    # correction_type = CorrectionType.SELF # Самостоятельно
    # correction_type = CorrectionType.FORCED # По предписанию

    # Установка данных коррекции
    check.set_correction_data(
        type=correction_type,
        data='2017-09-28', # Дата документа коррекции в формате 'yyyy-mm-dd'
        document='К111', # Номер документа коррекции
        description='Отключение электричества' # Описание коррекции
    )
    # Указание уполномоченного лица
    check.set_authorised_person(
        name='Иванов И.И',
        inn='123456789012'
    )

    # Отправка запроса
    try:
        task = client.create_task(check, 'идентификатор очереди')
    except HTTPError as exc:
        print(exc.response.text)
    else:
        print(task)
    # Task(id=1, external_id=2, print_queue_id=3, state='new')
    # id - идентификатор задачи
    # external_id - идентификатор операции в магазине
    # print_queue_id - идентификатор очереди
    # state - состояние задачи

    # Получение информации о поставленной на фискализацию задаче:
    try:
        task_info = client.get_task_info('идентификатор задачи')
    except HTTPError as exc:
        print(exc.response.text)
    else:
        print(task_info)
    # TaskInfo(id=234, external_id='4321', state='done', error_description=None,
    #          fiscal_data={'i': '111',
    #                       'fn': '2222222222222222',
    #                       't': '3333333333333',
    #                       'n': 4,
    #                       'fp': '555555555',
    #                       's': '6666.77'})
    # id - идентификатор задачи
    # external_id - идентификатор операции в магазине
    # state - состояние задачи
    # error_description - описание возникшей ошибки, когда state=='error'
    # fiscal_data - фискальные данные



    # Чтобы проверить, является ли очередь активной, выполните:
    client.is_queue_active('идентификатор очереди')

    # Вы можете указать идентификатор очереди по умолчанию с помощью:
    client.set_default_queue('идентификатор очереди по умолчанию')
    # В этом случае можно не указывать идентификатор очереди всякий раз,
    # когда нужно распечатать чек или проверить состояние очереди:
    assert client.is_queue_active() is True
    try:
        task = client.create_task(check)
    except HTTPError as exc:
        print(exc.response.text)
    else:
        print(task)
