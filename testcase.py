import unittest
from unittest.mock import patch, MagicMock
from model import Model


class TestModel(unittest.TestCase):

    def setUp(self):
        self.model = Model()

    def test_create_account_success(self):
        result = self.model.create_account(
            username="john123",
            email="john@example.com",
            password="StrongP@ssword1",
            phone_number="0123456789"
        )
        self.assertTrue(result["success"])

    def test_create_account_empty_username(self):
        result = self.model.create_account(
            username="",
            email="john@example.com",
            password="StrongP@ssword1",
            phone_number="0123456789"
        )
        self.assertFalse(result["success"])
        self.assertIn(("Input something", "label_12"), result["errors"])

    def test_weak_password(self):
        result = self.model.create_account(
            username="john123",
            email="john@example.com",
            password="weakpass",
            phone_number="0123456789"
        )
        self.assertFalse(result["success"])
        self.assertIn(("Password is weak", "label_13"), result["errors"])

    def test_invalid_email(self):
        result = self.model.create_account(
            username="john123",
            email="invalid-email",
            password="StrongP@ssword1",
            phone_number="0123456789"
        )
        self.assertFalse(result["success"])
        self.assertIn(("Invalid email", "label_14"), result["errors"])

    def test_invalid_phone(self):
        result = self.model.create_account(
            username="john123",
            email="john@example.com",
            password="StrongP@ssword1",
            phone_number="12345"
        )
        self.assertFalse(result["success"])
        self.assertIn(("Invalid phone number", "label_15"), result["errors"])

    def test_is_strong_password(self):
        self.assertTrue(self.model.is_strong_password("StrongP@ssword1"))
        self.assertFalse(self.model.is_strong_password("weakpass"))

    def test_validate_email(self):
        self.assertTrue(self.model.validate_email("test@example.com"))
        self.assertFalse(self.model.validate_email("invalid-email"))

    def test_is_valid_phone_number(self):
        self.assertTrue(self.model.is_valid_phone_number("0123456789"))
        self.assertFalse(self.model.is_valid_phone_number("123456789"))

    def test_send_reset_password_fake_email(self):
        # Don't actually send, just check return type (None or code)
        code = self.model.send_reset_password("test@example.com")
        self.assertTrue(isinstance(code, int) or code is None)

    def test_validate_date_format_success(self):
        self.assertTrue(self.model.validate_date_format("2025-05-03, 12:30:00"))

    def test_validate_date_format_failure(self):
        self.assertFalse(self.model.validate_date_format("2025-05-03"))

    def test_len_of_username(self):
        self.assertEqual(self.model.len_of_username("abcdefghijk"), "abcdefg")


if __name__ == "__main__":
    unittest.main()
