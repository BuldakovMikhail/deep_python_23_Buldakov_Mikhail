import unittest

from descriptor import Integer, String, PositiveInteger


class Inti:
    integer = Integer()

    def __init__(self, val=10):
        self.integer = val


class Stringi:
    val = String(10)

    def __init__(self, val="aboba"):
        self.val = val


class PositiveNum:
    integer = PositiveInteger()

    def __init__(self, val=10):
        self.integer = val


class TestDescriptor(unittest.TestCase):
    def test_int_field_creation(self):
        integer = Inti()
        self.assertEqual(integer.integer, 10)

        with self.assertRaises(Exception) as context:
            integer.integer = "aboba"
        self.assertTrue("Int required" in str(context.exception))

    def test_int_field_changing(self):
        integer = Inti()
        self.assertEqual(integer.integer, 10)

        integer.integer = 100
        self.assertEqual(integer.integer, 100)

        with self.assertRaises(Exception) as context:
            integer.integer = "aboba"
        self.assertTrue("Int required" in str(context.exception))

    def test_string_field_creating(self):
        string = Stringi()
        self.assertEqual(string.val, "aboba")

        with self.assertRaises(Exception) as context:
            string.val = 12.23
        self.assertTrue("String required" in str(context.exception))

    def test_string_field_changing(self):
        string = Stringi()
        self.assertEqual(string.val, "aboba")

        string.val = "a"
        self.assertEqual(string.val, "a")

        with self.assertRaises(Exception) as context:
            string.val = 12.23
        self.assertTrue("String required" in str(context.exception))

    def test_string_field_length_error(self):
        string = Stringi()
        self.assertEqual(string.val, "aboba")

        with self.assertRaises(Exception) as context:
            string.val = "abobaabobaabobaabobaabobaabobaaboba"
        self.assertTrue("String length must be" in str(context.exception))

    def test_pos_int_field_creation(self):
        integer = PositiveNum()
        self.assertEqual(integer.integer, 10)

        with self.assertRaises(Exception) as context:
            integer.integer = "aboba"
        self.assertTrue("Int required" in str(context.exception))

    def test_pos_int_field_changing(self):
        integer = PositiveNum()
        self.assertEqual(integer.integer, 10)

        integer.integer = 100
        self.assertEqual(integer.integer, 100)

        with self.assertRaises(Exception) as context:
            integer.integer = "aboba"
        self.assertTrue("Int required" in str(context.exception))

    def test_pos_int_field_try_to_set_negative(self):
        integer = PositiveNum()
        self.assertEqual(integer.integer, 10)

        integer.integer = 1
        self.assertEqual(integer.integer, 1)

        with self.assertRaises(Exception) as context:
            integer.integer = -1
        self.assertTrue("Value must be grater than 0" in str(context.exception))

    def test_pos_int_field_try_to_set_zero(self):
        integer = PositiveNum()
        self.assertEqual(integer.integer, 10)

        integer.integer = 1
        self.assertEqual(integer.integer, 1)

        with self.assertRaises(Exception) as context:
            integer.integer = 0
        self.assertTrue("Value must be grater than 0" in str(context.exception))
