from komtet_kassa_sdk import constants as c


price = {
    "type": "number"
}

quantity = {
    "type": "number",
    "default": 1
}

vat_number = {
    "type": "string",
    "enum": list(c.VAT_TYPES)
}

vat = {
    "type": "object",
    "required": ["number", "sum"],
    "properties": {
        "number": vat_number,
        "sum": price
    }
}

payment_type = {
    "type": "string",
    "enum": list(c.PAYMENT_TYPES),
    "default": c.CARD
}

payment = {
    "anyOf": [price, {
        "type": "object",
        "required": ["sum"],
        "properties": {
            "type": payment_type,
            "sum": price
        }
    }]
}

position = {
    "type": "object",
    "required": ["name", "price"],
    "properties": {
        "name": {
            "type": "string"
        },
        "price": price,
        "quantity": quantity,
        "vat": vat,
        "discount": price,
        "total": price
    }
}
