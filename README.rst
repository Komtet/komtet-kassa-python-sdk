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

Использование
=============

.. code:: python

    from requests.exceptions import HTTPError
    from komtet_kassa_sdk import Check, Client, Intent, TaxSystem, VatRate

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
    vat_rate = VatRate.RATE_18  # НДС 18%
    # vat_rate = VatRate.RATE_NO  # Без НДС
    # vat_rate = VatRate.RATE_0  # НДС 0%
    # vat_rate = VatRate.RATE_10  # НДС 10%
    # vat_rate = VatRate.RATE_110  # НДС 10/110
    # vat_rate = VatRate.RATE_118  # НДС 18/118
    # Можно указать просто число:
    # vat_rate = 18
    # или строку:
    # vat_rate = '10'
    # или даже так:
    # vat_rate = '18%'
    # а ещё вот так:
    # vat_rate = 0.18

    # Добавление позиции
    check.add_position(
        'Наименование позиции',
        price=100,  # Цена за единицу
        quantity=2,  # Количество единиц (по умолчанию 1)
        total=200,  # Общая стоимость позиции (по умолчанию price * quantity)
        vat=vat_rate  # По умолчанию Без НДС (VatRate.RATE_NO)
    )

    # Добавление суммы расчёта
    check.add_payment(300)

    # Если нужно распечатать чек (по умолчанию False)
    check.set_print(True)

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
