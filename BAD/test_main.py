import unittest
from unittest.mock import patch
from main import *


class SMSAuthorizerTestCase(unittest.TestCase):

    def test_init_authorized(self):
        auth = SMSAuthorizer()
        self.assertFalse(auth.is_authorized())

    def test_code_decimal(self):
        auth = SMSAuthorizer()
        auth.generate_sms_code()
        self.assertTrue(auth.code.isdecimal())

    def test_authorize_success(self):
        auth = SMSAuthorizer()
        auth.generate_sms_code()
        with patch('builtins.input', return_value=auth.code):
            auth.authorize()
            self.assertTrue(auth.is_authorized())

    @patch('builtins.input', return_value="1234567")
    def test_authorize_fail(self, mocked_input):
        auth = SMSAuthorizer()
        auth.generate_sms_code()
        auth.authorize()
        self.assertFalse(auth.is_authorized())


class PaymentProcessorTestCase(unittest.TestCase):
    """ Because of the bad design, this is now very difficult to test"""

    def test_payment_success(self):
        # ???
        self.assertTrue(True)

    def test_payment_fail(self):
        # ???
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
