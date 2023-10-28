import unittest
from unittest import mock

from file_search import gen_selected_lines
import builtins


class TestGenerator(unittest.TestCase):
    def test_find_one_line(self):
        lines = ["a b", "b c", "d e"]
        text = "\n".join(lines)

        search_words = ["c"]

        with mock.patch("builtins.open", new_callable=mock.mock_open, read_data=text):
            gen = gen_selected_lines("test", search_words)

            ans = []

            for i in gen:
                ans.append(i)

            self.assertEqual(len(ans), 1)

            self.assertEqual(ans[0], "b c")

    def test_find_multiple_lines(self):
        lines = ["a b", "b c", "d e"]
        text = "\n".join(lines)

        search_words = ["b"]

        with mock.patch("builtins.open", new_callable=mock.mock_open, read_data=text):
            gen = gen_selected_lines("test", search_words)

            ans = []

            for i in gen:
                ans.append(i)

            self.assertEqual(len(ans), 2)

            self.assertEqual(ans[0], "a b")
            self.assertEqual(ans[1], "b c")

    def test_find_multiple_search_words(self):
        lines = ["a b", "b c", "d e"]
        text = "\n".join(lines)

        search_words = ["b", "e"]

        with mock.patch("builtins.open", new_callable=mock.mock_open, read_data=text):
            gen = gen_selected_lines("test", search_words)

            ans = []

            for i in gen:
                ans.append(i)

            self.assertEqual(len(ans), 3)

            self.assertEqual(ans[0], "a b")
            self.assertEqual(ans[1], "b c")
            self.assertEqual(ans[2], "d e")

    def test_find_no_lines(self):
        lines = ["a b", "b c", "d e"]
        text = "\n".join(lines)

        search_words = ["f"]

        with mock.patch("builtins.open", new_callable=mock.mock_open, read_data=text):
            gen = gen_selected_lines("test", search_words)

            ans = []

            for i in gen:
                ans.append(i)

            self.assertEqual(len(ans), 0)

    def test_find_different_cases(self):
        lines = ["a B", "B c", "d e"]
        text = "\n".join(lines)

        search_words = ["b", "E"]

        with mock.patch("builtins.open", new_callable=mock.mock_open, read_data=text):
            gen = gen_selected_lines("test", search_words)

            ans = []

            for i in gen:
                ans.append(i)

            self.assertEqual(len(ans), 3)

            self.assertEqual(ans[0], "a B")
            self.assertEqual(ans[1], "B c")
            self.assertEqual(ans[2], "d e")

    def test_find_full_match(self):
        lines = [
            "а розан упала на лапу Азора",
            "а Роза упала на лапу Азора",
            "а роз упала на лапу Азора",
        ]
        text = "\n".join(lines)

        search_words = ["роза"]

        with mock.patch("builtins.open", new_callable=mock.mock_open, read_data=text):
            gen = gen_selected_lines("test", search_words)

            ans = []

            for i in gen:
                ans.append(i)

            self.assertEqual(len(ans), 1)

            self.assertEqual(ans[0], "а Роза упала на лапу Азора")

    def test_empty_search_words(self):
        search_words = []

        gen = gen_selected_lines("test", search_words)
        with self.assertRaises(Exception) as context:
            next(gen)
        self.assertTrue(
            "No words for search have been passed" in str(context.exception)
        )

    def test_pass_number_instead_of_file(self):
        search_words = ["asd"]
        gen = gen_selected_lines(23, search_words)

        with self.assertRaises(Exception) as context:
            next(gen)
        self.assertTrue("Neither file or file object" in str(context.exception))

    def test_find_in_file_object(self):
        lines = ["a b", "b c", "d e"]
        text = "\n".join(lines)

        search_words = ["b"]

        with mock.patch("builtins.open", new_callable=mock.mock_open, read_data=text):
            with open("test", "r") as src:
                gen = gen_selected_lines(src, search_words)

                ans = []

                for i in gen:
                    ans.append(i)

                self.assertEqual(len(ans), 2)

                self.assertEqual(ans[0], "a b")
                self.assertEqual(ans[1], "b c")

    def test_find_multiple_keywords_in_one_line(self):
        lines = ["a b", "aboba boba a", "d e"]
        text = "\n".join(lines)

        search_words = ["aboba", "boba"]

        with mock.patch("builtins.open", new_callable=mock.mock_open, read_data=text):
            gen = gen_selected_lines("test", search_words)

            ans = []

            for i in gen:
                ans.append(i)

            self.assertEqual(len(ans), 1)

            self.assertEqual(ans[0], "aboba boba a")
