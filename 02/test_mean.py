import unittest
from unittest.mock import patch
from unittest import mock
from unittest.mock import Mock

from io import StringIO

import time

from mean import mean


class TestMean(unittest.TestCase):
    def test_mean_for_sleepy_same_iter(self):
        @mean(5)
        def f():
            time.sleep(0.2)

        with patch("sys.stdout", new=StringIO()) as fake_out:
            for _ in range(5):
                f()
                ans = float(fake_out.getvalue().split(" ")[2])
                self.assertEqual(round(ans, 1), 0.2)

    def test_mean_for_sleepy_twice_more_iter(self):
        @mean(5)
        def f():
            time.sleep(0.2)

        with patch("sys.stdout", new=StringIO()) as fake_out:
            for _ in range(10):
                f()
                ans = float(fake_out.getvalue().split(" ")[2])
                self.assertEqual(round(ans, 1), 0.2)

    def test_with_output(self):
        @mean(5)
        def f():
            print("aboba")

        with patch("sys.stdout", new=StringIO()) as fake_out:
            for _ in range(5):
                f()
                ans = fake_out.getvalue().split("\n")
                ans2 = ans[1].split(" ")
                self.assertEqual(ans[0], "aboba")
                self.assertEqual(ans2[0], "Среднее")

    def test_decorated_function_returns_what_expected(self):
        @mean(5)
        def f(x):
            return x**2

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.assertEqual(f(2), 4)
            self.assertEqual(f(3), 9)
            self.assertEqual(f(5), 25)

    def test_decorated_function_with_few_positional_args(self):
        @mean(5)
        def f(x, y):
            return x + y

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.assertEqual(f(2, 3), 5)

    def test_decorated_function_with_few_keyword_args(self):
        @mean(5)
        def f(x=2, y=1):
            return x + y

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.assertEqual(f(x=1, y=4), 5)
            self.assertEqual(f(), 3)

    def test_decorated_function_with_keyword_and_positional_args(self):
        @mean(5)
        def f(x, y=1):
            return x * y

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.assertEqual(f(2, y=4), 8)
            self.assertEqual(f(3), 3)

    def test_exception(self):
        with self.assertRaises(Exception) as context:

            @mean(-10)
            def f(x, y=1):
                return x * y

            with patch("sys.stdout", new=StringIO()) as fake_out:
                self.assertEqual(f(2, y=4), 8)
                self.assertEqual(f(3), 3)

        self.assertTrue(
            "Decorator error, number of measures <= 0" in str(context.exception)
        )
