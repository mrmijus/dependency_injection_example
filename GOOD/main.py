import string
from abc import ABC, abstractmethod
import random

from uuid import uuid4
from enum import Enum


class AuthorizationError(Exception):
    """Raised when a user is not authorized"""


class OrderStatus(str, Enum):
    OPEN = 'OPEN'
    PAID = 'PAID'
    FAILED = 'FAILED'


class Authorizer(ABC):
    # We create an Authorizer interface as an abstraction layer. Doing this gives us a dependency inversion.
    # This is useful mainly because we can now easily add a new authorizer without having
    # to change the PaymentProcessor class
    @abstractmethod
    def authorize(self):
        """Authorize a user"""

    @abstractmethod
    def is_authorized(self) -> bool:
        """Check if a user is authorized"""


class SMSAuthorizer(Authorizer):
    def __init__(self):
        self.authorized = False
        self.code = None

    def generate_sms_code(self) -> None:
        self.code = ''.join(random.choices(string.digits, k=6))
        print(f'generated SMS code: {self.code}')

    def authorize(self) -> None:
        user_input = input('Enter SMS code: ')
        self.authorized = user_input == self.code

    def is_authorized(self) -> bool:
        return self.authorized


class Order:
    def __init__(self):
        self.id = uuid4()
        self.status = OrderStatus.OPEN

    def set_status(self, status: OrderStatus):
        self.status = status


class PaymentProcessor:
    # Dependency injection: we inject the Authorizer INTERFACE dependency into the PaymentProcessor class
    # This is useful because we can now easily change the authorizer without having to change the PaymentProcessor class
    # This is also useful for testing because we can now easily mock the Authorizer class
    def __init__(self, authorizer: Authorizer):
        self.authorizer = authorizer

    def pay(self, order: Order):
        self.authorizer.authorize()
        if not self.authorizer.is_authorized():
            raise AuthorizationError('authorization failed')
        print(f'Processing payment for order {order.id}')
        order.set_status(OrderStatus.PAID)
        print(f'Order {order.id} is {order.status.value}')


def main():
    order = Order()
    authorizer = SMSAuthorizer()
    authorizer.generate_sms_code()
    payment_processor = PaymentProcessor(authorizer)
    payment_processor.pay(order)


if __name__ == '__main__':
    main()
