# -*- coding: utf-8 -*-
import decimal


def to_decimal(value, rounding='.00'):
    return decimal.Decimal(value).quantize(decimal.Decimal(rounding))


def apply_discount(discount, items):
    """
    :param int|float discount: сумма скидки
    :param list items: список позиций
    """
    items_total = sum(item['total'] for item in items)

    items_count = len(items)
    accumulated_discount = 0

    for index, item in enumerate(items):
        if index < items_count - 1:
            item_price_percent = item['total'] / items_total * 100
            cur_item_discount = to_decimal(discount * item_price_percent / 100)
            accumulated_discount += cur_item_discount
        else:
            cur_item_discount = to_decimal(discount - accumulated_discount)

        item['total'] = to_decimal(item['total']) - cur_item_discount


def correction_positions(items):
    """
    Кооректировка позиций

    :param list items: список позиций
    """

    def update_item(item, data):
        """
        Обновление позиции

        :param dict item: позиция в чеке|заказе
        :param dict data: данные для обновления
        """
        item.update(data)
        return item

    new_items = []

    for item in items:
        quantity = decimal.Decimal(item['quantity'])
        price = decimal.Decimal(item['price'])
        total = decimal.Decimal(item['total'])

        has_extra_position = (total != price * quantity) and quantity > 1
        base_position_total = total

        if has_extra_position:
            quantity -= 1
            base_position_total = to_decimal(price * quantity)
            price = total - base_position_total

            new_items.append(update_item(item.copy(), {
                'price': price,
                'quantity': 1,
                'total': price
            }))

        new_items.append(update_item(item.copy(), {
            'quantity': quantity,
            'total': base_position_total
        }))

    return new_items
