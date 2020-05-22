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
