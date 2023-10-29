import unittest
from unittest import mock
from unittest.mock import Mock


from json_parser import parse_json


class TestParseJson(unittest.TestCase):
    def test_one_key_one_field(self):
        json_str = '{"name": "Савватий Анисимович Попов", "address": "г. Смоленск, пр. Специалистов, д. 560 стр. 5, 345113", "company": "ООО «Гришина-Панфилова»", "country": "Ливан", "text": "Темнеть бак госпожа ведь выражаться."}'
        m = Mock()

        parse_json(json_str, m, required_fields=["name"], keywords=["попов"])

        expected_calls = [
            mock.call("name", "попов"),
        ]
        self.assertEqual(expected_calls, m.mock_calls)

    def test_one_key_few_fields(self):
        json_str = '{"name": "Савватий Анисимович Попов", "address": "г. Смоленск, пр. Специалистов, д. 560 стр. 5, 345113", "company": "ООО «Гришина-Панфилова»", "country": "Ливан", "text": "Темнеть бак пОпОв госпожа ведь выражаться."}'
        m = Mock()

        parse_json(json_str, m, required_fields=["name", "text"], keywords=["попов"])

        expected_calls = [
            mock.call("name", "попов"),
            mock.call("text", "попов"),
        ]
        self.assertEqual(expected_calls, m.mock_calls)

    def test_few_keys_one_field(self):
        json_str = '{"name": "Савватий Анисимович Попов", "address": "г. Смоленск, пр. Специалистов, д. 560 стр. 5, 345113", "company": "ООО «Гришина-Панфилова»", "country": "Ливан", "text": "Темнеть бак госпожа ведь выражаться."}'
        m = Mock()

        parse_json(
            json_str,
            m,
            required_fields=["name"],
            keywords=["попов", "Савватий", "абоба"],
        )

        expected_calls = [
            mock.call("name", "попов"),
            mock.call("name", "Савватий"),
        ]
        self.assertEqual(expected_calls, m.mock_calls)

    def test_few_keys_few_fields(self):
        json_str = '{"name": "Савватий Анисимович Попов", "address": "г. Смоленск, пр. Специалистов, д. 560 стр. 5, 345113", "company": "ООО «Гришина-Панфилова»", "country": "Ливан", "text": "Темнеть бак госпожа ведь выражаться."}'
        m = Mock()

        parse_json(
            json_str,
            m,
            required_fields=["name", "text"],
            keywords=["попов", "Савватий", "абоба", "бак"],
        )

        expected_calls = [
            mock.call("name", "попов"),
            mock.call("name", "Савватий"),
            mock.call("text", "бак"),
        ]
        self.assertEqual(expected_calls, m.mock_calls)

    def test_fields_on_case_sensetive(self):
        json_str = '{"name": "Савватий Анисимович Попов", "address": "г. Смоленск, пр. Специалистов, д. 560 стр. 5, 345113", "company": "ООО «Гришина-Панфилова»", "country": "Ливан", "text": "Темнеть бак госпожа ведь выражаться."}'
        m = Mock()

        parse_json(
            json_str,
            m,
            required_fields=["Country"],
            keywords=["Ливан"],
        )

        expected_calls = []
        self.assertEqual(expected_calls, m.mock_calls)

    def test_without_fields(self):
        json_str = '{"name": "Савватий Анисимович Попов", "address": "г. Смоленск, пр. Специалистов, д. 560 стр. 5, 345113", "company": "ООО «Гришина-Панфилова»", "country": "Ливан", "text": "Темнеть бак госпожа ведь выражаться."}'
        m = Mock()

        parse_json(
            json_str,
            m,
            keywords=["попов", "Савватий", "абоба", "бак", "Ливан"],
        )

        expected_calls = [
            mock.call("name", "попов"),
            mock.call("name", "Савватий"),
            mock.call("country", "Ливан"),
            mock.call("text", "бак"),
        ]
        self.assertEqual(expected_calls, m.mock_calls)

    def test_without_keys(self):
        json_str = '{"name": "Савватий Анисимович Попов", "address": "г. Смоленск, пр. Специалистов, д. 560 стр. 5, 345113", "company": "ООО «Гришина-Панфилова»", "country": "Ливан", "text": "Темнеть бак госпожа ведь выражаться."}'
        m = Mock()

        parse_json(
            json_str,
            m,
            required_fields=["name", "country"],
        )

        expected_calls = [
            mock.call("name", "Савватий"),
            mock.call("name", "Анисимович"),
            mock.call("name", "Попов"),
            mock.call("country", "Ливан"),
        ]
        self.assertEqual(expected_calls, m.mock_calls)

    def test_without_keys_and_fields(self):
        json_str = '{"name": "Савватий Анисимович Попов", "country": "Ливан", "text": "Темнеть бак."}'
        m = Mock()

        parse_json(
            json_str,
            m,
        )

        expected_calls = [
            mock.call("name", "Савватий"),
            mock.call("name", "Анисимович"),
            mock.call("name", "Попов"),
            mock.call("country", "Ливан"),
            mock.call("text", "Темнеть"),
            mock.call("text", "бак."),
        ]
        self.assertEqual(expected_calls, m.mock_calls)

    def test_fields_found_keys_not(self):
        json_str = '{"name": "Савватий Анисимович Попов", "address": "г. Смоленск, пр. Специалистов, д. 560 стр. 5, 345113", "company": "ООО «Гришина-Панфилова»", "country": "Ливан", "text": "Темнеть бак госпожа ведь выражаться."}'
        m = Mock()

        parse_json(
            json_str,
            m,
            required_fields=["country", "name"],
            keywords=["Ливанasdsaa"],
        )

        expected_calls = []
        self.assertEqual(expected_calls, m.mock_calls)

    def test_keys_found_fields_not(self):
        json_str = '{"name": "Савватий Анисимович Попов", "address": "г. Смоленск, пр. Специалистов, д. 560 стр. 5, 345113", "company": "ООО «Гришина-Панфилова»", "country": "Ливан", "text": "Темнеть бак госпожа ведь выражаться."}'
        m = Mock()

        parse_json(
            json_str,
            m,
            required_fields=["countryasd", "nameasd"],
            keywords=["Ливан"],
        )

        expected_calls = []
        self.assertEqual(expected_calls, m.mock_calls)

    def test_two_same_keys_in_one_field(self):
        json_str = '{"name": "Савватий Анисимович Попов ПопоВ", "address": "г. Смоленск, пр. Специалистов, д. 560 стр. 5, 345113", "company": "ООО «Гришина-Панфилова»", "country": "Ливан", "text": "Темнеть бак госпожа ведь выражаться."}'
        m = Mock()

        parse_json(
            json_str,
            m,
            required_fields=["name"],
            keywords=["попов"],
        )

        expected_calls = [
            mock.call("name", "попов"),
            mock.call("name", "попов"),
        ]
        self.assertEqual(expected_calls, m.mock_calls)

    def test_callback_as_none(self):
        json_str = '{"name": "Савватий Анисимович Попов ПопоВ", "address": "г. Смоленск, пр. Специалистов, д. 560 стр. 5, 345113", "company": "ООО «Гришина-Панфилова»", "country": "Ливан", "text": "Темнеть бак госпожа ведь выражаться."}'

        with self.assertRaises(ValueError) as context:
            parse_json(
                json_str,
                None,
                required_fields=["name"],
                keywords=["попов"],
            )

        self.assertTrue("must be not None" in str(context.exception))

    def test_fields_found_one_key_matches_not_in_required_field(self):
        json_str = '{"name": "Савватий Анисимович Попов", "address": "г. Смоленск, пр. Специалистов, д. 560 стр. 5, 345113", "company": "ООО «Гришина-Панфилова» Петр", "country": "Ливан", "text": "Темнеть бак госпожа ведь выражаться."}'
        m = Mock()

        parse_json(
            json_str,
            m,
            required_fields=["country", "name"],
            keywords=["Савватий", "Ливан", "Петр"],
        )

        expected_calls = [
            mock.call("country", "Ливан"),
            mock.call("name", "Савватий"),
        ]

        self.assertEqual(expected_calls, m.mock_calls)
        self.assertTrue(mock.call("company", "Петр") not in m.mock_calls)

    def test_same_keywords_but_with_diff_case(self):
        json_str = '{"name": "Савватий Анисимович Попов", "address": "г. Смоленск, пр. Специалистов, д. 560 стр. 5, 345113", "company": "ООО «Гришина-Панфилова» Петр", "country": "Ливан", "text": "Темнеть бак госпожа ведь выражаться."}'
        m = Mock()

        parse_json(
            json_str,
            m,
            required_fields=["country", "name"],
            keywords=["Савватий", "СавВаТИй", "савватий", "пОпОв"],
        )

        expected_calls = [
            mock.call("name", "Савватий"),
            mock.call("name", "СавВаТИй"),
            mock.call("name", "савватий"),
            mock.call("name", "пОпОв"),
        ]

        self.assertEqual(expected_calls, m.mock_calls)
        self.assertTrue(mock.call("company", "Петр") not in m.mock_calls)

    def test_keywords_on_case_insensitive(self):
        json_str = '{"name": "Савватий Анисимович попОВ", "address": "г. Смоленск, пр. Специалистов, д. 560 стр. 5, 345113", "company": "ООО «Гришина-Панфилова»", "country": "Ливан", "text": "Темнеть бак госпожа ведь выражаться."}'
        m = Mock()

        parse_json(
            json_str,
            m,
            required_fields=["name", "country"],
            keywords=["Попов", "Савватий", "ливан"],
        )

        expected_calls = [
            mock.call("name", "Попов"),
            mock.call("name", "Савватий"),
            mock.call("country", "ливан"),
        ]
        self.assertEqual(expected_calls, m.mock_calls)
