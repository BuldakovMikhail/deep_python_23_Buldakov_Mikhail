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
            mock.call("Попов"),
        ]
        self.assertEqual(expected_calls, m.mock_calls)

    def test_one_key_few_fields(self):
        json_str = '{"name": "Савватий Анисимович Попов", "address": "г. Смоленск, пр. Специалистов, д. 560 стр. 5, 345113", "company": "ООО «Гришина-Панфилова»", "country": "Ливан", "text": "Темнеть бак пОпОв госпожа ведь выражаться."}'
        m = Mock()

        parse_json(json_str, m, required_fields=["name", "text"], keywords=["попов"])

        expected_calls = [
            mock.call("Попов"),
            mock.call("пОпОв"),
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
            mock.call("Попов"),
            mock.call("Савватий"),
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
            mock.call("Попов"),
            mock.call("Савватий"),
            mock.call("бак"),
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
            mock.call("Попов"),
            mock.call("Савватий"),
            mock.call("Ливан"),
            mock.call("бак"),
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
            mock.call("Савватий"),
            mock.call("Анисимович"),
            mock.call("Попов"),
            mock.call("Ливан"),
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
            mock.call("Савватий"),
            mock.call("Анисимович"),
            mock.call("Попов"),
            mock.call("Ливан"),
            mock.call("Темнеть"),
            mock.call("бак."),
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
