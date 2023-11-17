import unittest

from lru_cache import LRUCache


class TestLRUCache(unittest.TestCase):
    def test_lru_remove_least_on_add(self):
        cache = LRUCache(2)

        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertIsNone(cache.get("k3"))
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k1"), "val1")

        cache.set("k3", "val3")

        self.assertEqual(cache.get("k3"), "val3")
        self.assertIsNone(cache.get("k2"))
        self.assertEqual(cache.get("k1"), "val1")

    def test_lru_value_update(self):
        cache = LRUCache(2)

        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertIsNone(cache.get("k3"))
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k1"), "val1")

        cache.set("k1", "val1_1")
        self.assertIsNone(cache.get("k3"))
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k1"), "val1_1")

        cache.set("k3", "val3")

        self.assertEqual(cache.get("k3"), "val3")
        self.assertIsNone(cache.get("k2"))
        self.assertEqual(cache.get("k1"), "val1_1")

    def test_lru_value_check_addition_with_out_get(self):
        cache = LRUCache(2)

        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k3", "val3")

        self.assertIsNone(cache.get("k1"))
        self.assertEqual(cache.get("k3"), "val3")
        self.assertEqual(cache.get("k2"), "val2")

    def test_lru_capacity_1_value_insert(self):
        cache = LRUCache(1)
        cache.set("k1", "val1")

        self.assertEqual(cache.get("k1"), "val1")

    def test_lru_capacity_1_item_replaced(self):
        cache = LRUCache(1)
        cache.set("k1", "val1")

        self.assertEqual(cache.get("k1"), "val1")

        cache.set("k2", "val2")
        self.assertIsNone(cache.get("k1"))
        self.assertEqual(cache.get("k2"), "val2")

    def test_lru_capacity_1_value_updated(self):
        cache = LRUCache(1)
        cache.set("k1", "val1")

        self.assertEqual(cache.get("k1"), "val1")

        cache.set("k1", "val1_1")
        self.assertEqual(cache.get("k1"), "val1_1")

    def test_lru_unupdated_replacement(self):
        cache = LRUCache(2)

        cache.set("k1", "val1")
        cache.set("k2", "val2")

        cache.set("k1", "val1_1")
        cache.set("k3", "val3")

        self.assertIsNone(cache.get("k2"))
        self.assertEqual(cache.get("k1"), "val1_1")
        self.assertEqual(cache.get("k3"), "val3")

    def test_lru_get_from_empty(self):
        cache = LRUCache(2)

        self.assertIsNone(cache.get("k1"))

    def test_create_cache_with_size_0(self):
        with self.assertRaises(ValueError) as context:
            LRUCache(0)
        self.assertTrue("greater than zero" in str(context.exception))
