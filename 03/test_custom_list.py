import unittest

from custom_list import CustomList


class TestCustomList(unittest.TestCase):
    def test_sum_same_length_same_class(self):
        first_list = CustomList([1, 2, 3])
        second_list = CustomList([13, 2, 21])

        third_list = first_list + second_list

        self.assertEqual(list(third_list), [14, 4, 24])
        self.assertIsInstance(third_list, CustomList)
        self.assertIsNot(third_list, first_list)
        self.assertIsNot(third_list, second_list)
        self.assertEqual(list(first_list), [1, 2, 3])
        self.assertEqual(list(second_list), [13, 2, 21])

    def test_sum_same_length_with_list(self):
        first_list = CustomList([1, 2, 3])
        second_list = [13, 2, 21]

        third_list = first_list + second_list

        self.assertEqual(list(third_list), [14, 4, 24])
        self.assertIsInstance(third_list, CustomList)
        self.assertIsNot(third_list, first_list)
        self.assertIsNot(third_list, second_list)
        self.assertEqual(list(first_list), [1, 2, 3])
        self.assertEqual(list(second_list), [13, 2, 21])

    def test_sum_same_length_with_list_first(self):
        first_list = CustomList([1, 2, 3])
        second_list = [13, 2, 21]

        third_list = second_list + first_list

        self.assertEqual(list(third_list), [14, 4, 24])
        self.assertIsInstance(third_list, CustomList)
        self.assertIsNot(third_list, first_list)
        self.assertIsNot(third_list, second_list)
        self.assertEqual(list(first_list), [1, 2, 3])
        self.assertEqual(list(second_list), [13, 2, 21])

    def test_sum_different_length_shortest_first_length_same_class(self):
        first_list = CustomList([1, 2, 3])
        second_list = CustomList([3, 2, 1, 0, 1, 2, 3])

        third_list = first_list + second_list

        self.assertEqual(list(third_list), [4, 4, 4, 0, 1, 2, 3])
        self.assertIsInstance(third_list, CustomList)
        self.assertIsNot(third_list, first_list)
        self.assertIsNot(third_list, second_list)
        self.assertEqual(list(first_list), [1, 2, 3])
        self.assertEqual(list(second_list), [3, 2, 1, 0, 1, 2, 3])

    def test_sum_different_length_shortest_second_length_same_class(self):
        first_list = CustomList([1, 2, 3])
        second_list = CustomList([3, 2, 1, 0, 1, 2, 3])

        third_list = second_list + first_list

        self.assertEqual(list(third_list), [4, 4, 4, 0, 1, 2, 3])
        self.assertIsInstance(third_list, CustomList)
        self.assertIsNot(third_list, first_list)
        self.assertIsNot(third_list, second_list)
        self.assertEqual(list(first_list), [1, 2, 3])
        self.assertEqual(list(second_list), [3, 2, 1, 0, 1, 2, 3])

    def test_sum_different_length_shortest_list_first(self):
        first_list = [1, 2, 3]
        second_list = CustomList([3, 2, 1, 0, 1, 2, 3])

        third_list = first_list + second_list

        self.assertEqual(list(third_list), [4, 4, 4, 0, 1, 2, 3])
        self.assertIsInstance(third_list, CustomList)
        self.assertIsNot(third_list, first_list)
        self.assertIsNot(third_list, second_list)
        self.assertEqual(list(first_list), [1, 2, 3])
        self.assertEqual(list(second_list), [3, 2, 1, 0, 1, 2, 3])

    def test_sum_different_length_shortest_list_second(self):
        first_list = [1, 2, 3]
        second_list = CustomList([3, 2, 1, 0, 1, 2, 3])

        third_list = second_list + first_list

        self.assertEqual(list(third_list), [4, 4, 4, 0, 1, 2, 3])
        self.assertIsInstance(third_list, CustomList)
        self.assertIsNot(third_list, first_list)
        self.assertIsNot(third_list, second_list)
        self.assertEqual(list(first_list), [1, 2, 3])
        self.assertEqual(list(second_list), [3, 2, 1, 0, 1, 2, 3])

    def test_sum_different_length_longest_list_first(self):
        first_list = CustomList([1, 2, 3])
        second_list = [3, 2, 1, 0, 1, 2, 3]

        third_list = second_list + first_list

        self.assertEqual(list(third_list), [4, 4, 4, 0, 1, 2, 3])
        self.assertIsInstance(third_list, CustomList)
        self.assertIsNot(third_list, first_list)
        self.assertIsNot(third_list, second_list)
        self.assertEqual(list(first_list), [1, 2, 3])
        self.assertEqual(list(second_list), [3, 2, 1, 0, 1, 2, 3])

    def test_sum_different_length_longest_list_second(self):
        first_list = CustomList([1, 2, 3])
        second_list = [3, 2, 1, 0, 1, 2, 3]

        third_list = first_list + second_list

        self.assertEqual(list(third_list), [4, 4, 4, 0, 1, 2, 3])
        self.assertIsInstance(third_list, CustomList)
        self.assertIsNot(third_list, first_list)
        self.assertIsNot(third_list, second_list)
        self.assertEqual(list(first_list), [1, 2, 3])
        self.assertEqual(list(second_list), [3, 2, 1, 0, 1, 2, 3])

    def test_sub_same_length_same_class(self):
        first_list = CustomList([1, 2, 3])
        second_list = CustomList([3, 2, 1])

        third_list = first_list - second_list

        self.assertEqual(list(third_list), [-2, 0, 2])
        self.assertIsInstance(third_list, CustomList)
        self.assertIsNot(third_list, first_list)
        self.assertIsNot(third_list, second_list)
        self.assertEqual(list(first_list), [1, 2, 3])
        self.assertEqual(list(second_list), [3, 2, 1])

    def test_sub_same_length_with_list(self):
        first_list = CustomList([1, 2, 3])
        second_list = [3, 2, 1]

        third_list = first_list - second_list

        self.assertEqual(list(third_list), [-2, 0, 2])
        self.assertIsInstance(third_list, CustomList)
        self.assertIsNot(third_list, first_list)
        self.assertIsNot(third_list, second_list)
        self.assertEqual(list(first_list), [1, 2, 3])
        self.assertEqual(list(second_list), [3, 2, 1])

    def test_sub_same_length_with_list_first(self):
        first_list = CustomList([1, 2, 3])
        second_list = [3, 2, 1]

        third_list = second_list - first_list

        self.assertEqual(list(third_list), [2, 0, -2])
        self.assertIsInstance(third_list, CustomList)
        self.assertIsNot(third_list, first_list)
        self.assertIsNot(third_list, second_list)
        self.assertEqual(list(first_list), [1, 2, 3])
        self.assertEqual(list(second_list), [3, 2, 1])

    def test_sub_different_length_shortest_first_length_same_class(self):
        first_list = CustomList([1, 2, 3])
        second_list = CustomList([3, 2, 1, 0, 1, 2, 3])

        third_list = first_list - second_list

        self.assertEqual(list(third_list), [-2, 0, 2, 0, -1, -2, -3])
        self.assertIsInstance(third_list, CustomList)
        self.assertIsNot(third_list, first_list)
        self.assertIsNot(third_list, second_list)
        self.assertEqual(list(first_list), [1, 2, 3])
        self.assertEqual(list(second_list), [3, 2, 1, 0, 1, 2, 3])

    def test_sub_different_length_shortest_second_length_same_class(self):
        first_list = CustomList([1, 2, 3])
        second_list = CustomList([3, 2, 1, 0, 1, 2, 3])

        third_list = second_list - first_list

        self.assertEqual(list(third_list), [2, 0, -2, 0, 1, 2, 3])
        self.assertIsInstance(third_list, CustomList)
        self.assertIsNot(third_list, first_list)
        self.assertIsNot(third_list, second_list)
        self.assertEqual(list(first_list), [1, 2, 3])
        self.assertEqual(list(second_list), [3, 2, 1, 0, 1, 2, 3])

    def test_sub_different_length_shortest_list_first(self):
        first_list = [1, 2, 3]
        second_list = CustomList([3, 2, 1, 0, 1, 2, 3])

        third_list = first_list - second_list

        self.assertEqual(list(third_list), [-2, 0, 2, 0, -1, -2, -3])
        self.assertIsInstance(third_list, CustomList)
        self.assertIsNot(third_list, first_list)
        self.assertIsNot(third_list, second_list)
        self.assertEqual(list(first_list), [1, 2, 3])
        self.assertEqual(list(second_list), [3, 2, 1, 0, 1, 2, 3])

    def test_sub_different_length_shortest_list_second(self):
        first_list = [1, 2, 3]
        second_list = CustomList([3, 2, 1, 0, 1, 2, 3])

        third_list = second_list - first_list

        self.assertEqual(list(third_list), [2, 0, -2, 0, 1, 2, 3])
        self.assertIsInstance(third_list, CustomList)
        self.assertIsNot(third_list, first_list)
        self.assertIsNot(third_list, second_list)
        self.assertEqual(list(first_list), [1, 2, 3])
        self.assertEqual(list(second_list), [3, 2, 1, 0, 1, 2, 3])

    def test_sub_different_length_longest_list_first(self):
        first_list = CustomList([1, 2, 3])
        second_list = [3, 2, 1, 0, 1, 2, 3]

        third_list = second_list - first_list

        self.assertEqual(list(third_list), [2, 0, -2, 0, 1, 2, 3])
        self.assertIsInstance(third_list, CustomList)
        self.assertIsNot(third_list, first_list)
        self.assertIsNot(third_list, second_list)
        self.assertEqual(list(first_list), [1, 2, 3])
        self.assertEqual(list(second_list), [3, 2, 1, 0, 1, 2, 3])

    def test_sub_different_length_longest_list_second(self):
        first_list = CustomList([1, 2, 3])
        second_list = [3, 2, 1, 0, 1, 2, 3]

        third_list = first_list - second_list

        self.assertEqual(list(third_list), [-2, 0, 2, 0, -1, -2, -3])
        self.assertIsInstance(third_list, CustomList)
        self.assertIsNot(third_list, first_list)
        self.assertIsNot(third_list, second_list)
        self.assertEqual(list(first_list), [1, 2, 3])
        self.assertEqual(list(second_list), [3, 2, 1, 0, 1, 2, 3])

    def test_eq_as_lists(self):
        first_list = CustomList([1, 2, 3])
        second_list = CustomList([1, 2, 3])

        self.assertEqual(first_list, second_list)

    def test_eq_shuffled(self):
        first_list = CustomList([1, 2, 3])
        second_list = CustomList([1, 3, 2])

        self.assertEqual(first_list, second_list)

    def test_eq_differen_length(self):
        first_list = CustomList([1, 2, 3])
        second_list = CustomList([1, 3, 2, 0, 0, 0, 1, -1])

        self.assertEqual(first_list, second_list)

    def test_gt(self):
        first_list = CustomList([1, 2, 3])
        second_list = CustomList([4, -5, 0])

        self.assertGreater(first_list, second_list)

    def test_gt_diff_length(self):
        first_list = CustomList([1, 2, 3])
        second_list = CustomList([4, -5, 0, 40, -40, 0, 0, 1, -1])

        self.assertGreater(first_list, second_list)

    def test_lt(self):
        first_list = CustomList([1, 2, 3])
        second_list = CustomList([4, -5, 0])

        self.assertLess(second_list, first_list)

    def test_lt_diff_length(self):
        first_list = CustomList([1, 2, 3])
        second_list = CustomList([4, -5, 0, 40, -40, 0, 0, 1, -1])

        self.assertLess(second_list, first_list)

    def test_le(self):
        first_list = CustomList([1, 2, 3])
        second_list = CustomList([1, 3, 2])
        third_list = CustomList([4, -5, 0, 40, -40, 0, 0, 1, -1])

        self.assertLessEqual(first_list, second_list)
        self.assertLessEqual(third_list, first_list)

    def test_ge(self):
        first_list = CustomList([1, 2, 3])
        second_list = CustomList([1, 3, 2])
        third_list = CustomList([4, -5, 0, 40, -40, 0, 0, 1, -1])

        self.assertGreaterEqual(first_list, second_list)
        self.assertGreaterEqual(first_list, third_list)

    def test_ne_as_lists(self):
        first_list = CustomList([1, 2, 3])
        second_list = CustomList([100, 2, 3])

        self.assertNotEqual(first_list, second_list)

    def test_ne_differen_length(self):
        first_list = CustomList([1, 2, 3])
        second_list = CustomList([1, 3, 2, 0, 0, 0, 1, 1])

        self.assertNotEqual(first_list, second_list)

    def test_print(self):
        first_list = CustomList([1, 2, 3, 4])
        string = str(first_list)

        self.assertEqual(string, "List: [1, 2, 3, 4], sum: 10")
        self.assertEqual(list(first_list), [1, 2, 3, 4])
