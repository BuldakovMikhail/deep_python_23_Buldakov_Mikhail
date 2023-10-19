import unittest

from custom_meta import CustomMeta


class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val
        self._protected = 2
        self.__private = 23
        self.post__ = 3

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"


class TestCustomMeta(unittest.TestCase):
    def test_class_attribute_changed(self):
        self.assertEqual(CustomClass.custom_x, 50)
        with self.assertRaises(Exception) as context:
            temp = CustomClass.x
        self.assertTrue("no attribute" in str(context.exception))

    def test_instance_fields_changed(self):
        inst = CustomClass()
        self.assertEqual(inst.custom_x, 50)
        self.assertEqual(inst.custom_val, 99)
        self.assertEqual(inst.custom_line(), 100)
        self.assertEqual(str(inst), "Custom_by_metaclass")

        with self.assertRaises(Exception) as context:
            temp = inst.x
        self.assertTrue("no attribute" in str(context.exception))

        with self.assertRaises(Exception) as context:
            temp = inst.val
        self.assertTrue("no attribute" in str(context.exception))

        with self.assertRaises(Exception) as context:
            temp = inst.line()
        self.assertTrue("no attribute" in str(context.exception))

        with self.assertRaises(Exception) as context:
            temp = inst.yyy
        self.assertTrue("no attribute" in str(context.exception))

    def test_added_attrs(self):
        inst = CustomClass()
        inst.dynamic = "added later"

        self.assertEqual(inst.custom_dynamic, "added later")
        with self.assertRaises(Exception) as context:
            temp = inst.dynamic
        self.assertTrue("no attribute" in str(context.exception))

    def test_magic_attrs(self):
        self.assertTrue("__init__" in CustomClass.__dict__.keys())

    def test_protected_attrs(self):
        inst = CustomClass()

        self.assertEqual(inst.custom__protected, 2)
        with self.assertRaises(Exception) as context:
            temp = inst._protected
        self.assertTrue("no attribute" in str(context.exception))

    def test_private_attrs(self):
        inst = CustomClass()
        self.assertEqual(inst.custom__CustomClass__private, 23)
        with self.assertRaises(Exception) as context:
            temp = inst._CustomClass__private
        self.assertTrue("no attribute" in str(context.exception))

    def test_post_underline(self):
        inst = CustomClass()
        self.assertEqual(inst.custom_post__, 3)
        with self.assertRaises(Exception) as context:
            temp = inst.post__
        self.assertTrue("no attribute" in str(context.exception))
