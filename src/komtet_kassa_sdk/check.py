from .constants import WITHOUT_VAT, CARD, SELL
from .exc import CheckError, FormatError
from .queue import PrintQueue
from .validation import validate, ValidationError
from .validation.schemas import position as position_schema, payment as payment_schema


class CheckPosition(object):

    def __init__(self, name, price, quantity=1, total=None, discount=None, vat=None):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.total = total or price * quantity
        self.vat = vat
        self.discount = discount

    def _prepare_vat(self):
        if not self.vat:
            return {
                'number': WITHOUT_VAT,
                'sum': 0
            }

        return self.vat

    def _prepare(self):
        position = {
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'total': self.total,
            'vat': self._prepare_vat()
        }

        if self.discount:
            position['discount'] = self.discount

        return position


class Check(object):

    def __init__(self, task_id, user_email, positions=None, payment=None, payments=None,
                 is_print=False, intent=SELL):
        self.task_id = task_id
        self.user_email = user_email
        self.is_print = is_print
        self.intent = intent

        self.positions = []
        if positions:
            for position in positions:
                self.append_position(position)

        self.payments = []
        if payment:
            self.append_payment(payment)
        if payments:
            for payment in payments:
                self.append_payment(payment)

    def append_position(self, position):
        try:
            validate(position, position_schema)
        except ValidationError:
            raise FormatError('Invalid format of position', position_schema)

        self.positions.append(CheckPosition(**position))

    def append_payment(self, payment):
        try:
            validate(payment, payment_schema)
        except ValidationError as ex:
            raise FormatError('Invalid format of payment', payment_schema)

        if isinstance(payment, (int, float)):
            payment = {
                'type': CARD,
                'sum': payment
            }

        self.payments.append(payment)

    def _prepare(self):
        return {
            "task_id": self.task_id and str(self.task_id),
            "user": self.user_email,
            "print": self.is_print,
            "intent": self.intent,
            "payments": self.payments,
            "positions": [position._prepare() for position in self.positions],
        }

    def _validate(self):
        if (
            sum(map(lambda position: position.total, self.positions), 0) !=
            sum(map(lambda payment: payment['sum'], self.payments), 0)
        ):
            raise CheckError('Invalid payment sum in check')

    def print_out(self, queue_name=None, **kwargs):
        self._validate()

        PrintQueue(queue_name).put_task(self._prepare(), **kwargs)
