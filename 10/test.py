#! /usr/bin/env python3

import json
import ujson
import cjson
import unittest


class TestCjson(unittest.TestCase):
    def test_loads_key_int_and_str(self):

        json_str = '{"hello": 10, "world": "value"}'
        json_doc = json.loads(json_str)
        ujson_doc = ujson.loads(json_str)
        cjson_doc = cjson.loads(json_str)

        self.assertTrue(json_doc == ujson_doc == cjson_doc)

    def test_loads_return_type(self):

        json_str = '{"hello": 10, "world": "value"}'
        
        cjson_doc = cjson.loads(json_str)
        self.assertIsInstance(cjson_doc, dict)

    def test_loads_and_dumps(self):
        json_str = '{"hello": 10, "world": "value"}'
        self.assertEqual(json_str, cjson.dumps(cjson.loads(json_str)))

    def test_loads_value_is_str(self):
        json_str = '{"world": "value"}'
        ujson_doc = ujson.loads(json_str)
        cjson_doc = cjson.loads(json_str)

        self.assertEqual(ujson_doc, cjson_doc)

    def test_loads_value_is_int(self):
        json_str = '{"world": 1002}'
        ujson_doc = ujson.loads(json_str)
        cjson_doc = cjson.loads(json_str)

        self.assertEqual(ujson_doc, cjson_doc)

    def test_loads_value_is_int_two_pairs(self):
        json_str = '{"world": 1002, "asd": 1}'
        ujson_doc = ujson.loads(json_str)
        cjson_doc = cjson.loads(json_str)

        self.assertEqual(ujson_doc, cjson_doc)

    def test_loads_value_is_str_two_pairs(self):
        json_str = '{"world": "1002", "asd": "asd123asd"}'
        ujson_doc = ujson.loads(json_str)
        cjson_doc = cjson.loads(json_str)

        self.assertEqual(ujson_doc, cjson_doc)

    def test_loads_digits_in_key(self):
        json_str = '{"worl23d": "1002", "asd": "asd123asd"}'
        ujson_doc = ujson.loads(json_str)
        cjson_doc = cjson.loads(json_str)

        self.assertEqual(ujson_doc, cjson_doc)

    def test_loads_empty_json(self):
        json_str = '{}'
        ujson_doc = ujson.loads(json_str)
        cjson_doc = cjson.loads(json_str)

        self.assertEqual(ujson_doc, cjson_doc)

    def test_loads_bracket_error(self):
        json_str = '{"worl23d": "1002", "asd": "asd123asd"'
        
        with self.assertRaises(Exception) as context:
            cjson_doc = cjson.loads(json_str)
        
        self.assertTrue("Expected object or value" in str(context.exception))

    def test_loads_commas_error(self):
        json_str = '{"worl23d": "1002" "asd": "asd123asd"}'
        
        with self.assertRaises(Exception) as context:
            cjson_doc = cjson.loads(json_str)
        
        self.assertTrue("Expected object or value" in str(context.exception))

    def test_loads_colon_error(self):
        json_str = '{"worl23d" "1002", "asd": "asd123asd"}'
        
        with self.assertRaises(Exception) as context:
            cjson_doc = cjson.loads(json_str)
        
        self.assertTrue("Expected object or value" in str(context.exception))

    def test_loads_quotes_error(self):
        json_str = '{"worl23d": 1002", "asd": "asd123asd"}'
        
        with self.assertRaises(Exception) as context:
            cjson_doc = cjson.loads(json_str)
        
        self.assertTrue("Expected object or value" in str(context.exception))

    def test_loads_spaces_error(self):
        json_str = '{"worl23d": "1002",    "asd": "asd123asd"}'
        
        with self.assertRaises(Exception) as context:
            cjson_doc = cjson.loads(json_str)
        
        self.assertTrue("Expected object or value" in str(context.exception))

    # ------------------- DUMPS --------------------------------------------

    def test_dumps_value_is_str(self):
        json = {"world": "value"}
        cjson_doc = cjson.dumps(json)

        self.assertEqual('{"world": "value"}', cjson_doc)

    def test_dumps_return_type(self):
        json = {"world": "value"}
        cjson_doc = cjson.dumps(json)

        self.assertIsInstance(cjson_doc, str)

    def test_dumps_value_is_int(self):
        json_str = {"world": 1002}
        cjson_doc = cjson.dumps(json_str)

        self.assertEqual('{"world": 1002}', cjson_doc)

    def test_dumps_value_is_int_two_pairs(self):
        json_str = {"world": 1002, "asd": 1}
        cjson_doc = cjson.dumps(json_str)

        self.assertEqual('{"world": 1002, "asd": 1}', cjson_doc)

    def test_dumps_value_is_str_two_pairs(self):
        json_str = {"world": "1002", "asd": "asd123asd"}
        cjson_doc = cjson.dumps(json_str)

        self.assertEqual('{"world": "1002", "asd": "asd123asd"}', cjson_doc)

    def test_dumps_digits_in_key(self):
        json_str = {"worl23d": "1002", "asd": "asd123asd"}
        
        cjson_doc = cjson.dumps(json_str)

        self.assertEqual('{"worl23d": "1002", "asd": "asd123asd"}', cjson_doc)

    def test_dumps_empty_json(self):
        json_str = {}
        cjson_doc = cjson.dumps(json_str)

        self.assertEqual('{}', cjson_doc)

    def test_dumps_error_not_dict(self):
        json_str = 12

        with self.assertRaises(Exception) as context:
            cjson_doc = cjson.dumps(json_str)
        
        self.assertTrue("Expected dict" in str(context.exception))

    def test_dumps_error_key_not_str(self):
        json_str = {1: 2, "ana": "a"}

        with self.assertRaises(Exception) as context:
            cjson_doc = cjson.dumps(json_str)
        
        self.assertTrue("Expected string as a key" in str(context.exception))

    def test_dumps_error_value_not_str_or_int(self):
        json_str = {"ana": "a", "aboba": [1, 2, 2]}

        with self.assertRaises(Exception) as context:
            cjson_doc = cjson.dumps(json_str)
        
        self.assertTrue("Expected string or num as a value" in str(context.exception))



if __name__ == "__main__":
    unittest.main()