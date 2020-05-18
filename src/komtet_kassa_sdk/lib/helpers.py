import decimal


def to_decimal(value, rounding='.00'):
    return decimal.Decimal(value).quantize(decimal.Decimal(rounding))
