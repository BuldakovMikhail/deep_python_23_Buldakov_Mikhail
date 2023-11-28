from fetcher import get_most_common_words, fetch_url, batch_fetch, fetch_worker

from unittest import IsolatedAsyncioTestCase
from unittest import mock
import aiohttp
import asyncio as aio

import io
import contextlib


class TestFetcher(IsolatedAsyncioTestCase):
    def test_most_common_words(self):
        resp = "<html> 1 2 2 3 3 , 3 , 4 4 4 4 5 5 5 5 5 6 6 6 6 6 6 </html>"
        most_common = get_most_common_words(resp, 2)

        self.assertDictEqual(most_common, {"6": 6, "5": 5})

    def test_most_common_words_on_letters(self):
        resp = "<html> a b b c c c d d d d e e e e e f f f f f f </html>"
        most_common = get_most_common_words(resp, 3)

        self.assertDictEqual(most_common, {"f": 6, "e": 5, "d": 4})

    @mock.patch("aiohttp.ClientSession.get")
    async def test_fetch_url(self, mock_get):
        mock_get.return_value.__aenter__.return_value.read.return_value = "test text"

        val = await fetch_url("test url")

        self.assertEqual(val, "test text")
        self.assertTrue(mock.call("test url") in mock_get.mock_calls)

    @mock.patch("aiohttp.ClientSession.get")
    async def test_batch_fetch_one_worker(self, mock_get):
        mock_get.return_value.__aenter__.return_value.read.return_value = (
            "<html> a b b c c c d d d d e e e e e f f f f f f </html>"
        )

        lines = ["tu1", "tu2", "tu3\n"]
        text = "\n".join(lines)

        mock_open = mock.AsyncMock()
        mock_open.return_value.__aenter__.return_value.readline = "test url"

        res = [
            ("tu1\n", {"f": 6, "e": 5, "d": 4, "c": 3, "b": 2}),
            ("tu2\n", {"f": 6, "e": 5, "d": 4, "c": 3, "b": 2}),
            ("tu3\n", {"f": 6, "e": 5, "d": 4, "c": 3, "b": 2}),
        ]
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            with mock.patch(
                "builtins.open", new_callable=mock.mock_open, read_data=text
            ):
                val = await batch_fetch("aboba", 1)

                self.assertEqual(val, res)
                self.assertTrue(mock.call("tu1\n") in mock_get.mock_calls)
                self.assertTrue(mock.call("tu2\n") in mock_get.mock_calls)
                self.assertTrue(mock.call("tu3\n") in mock_get.mock_calls)

    @mock.patch("aiohttp.ClientSession.get")
    async def test_batch_fetch_workers_count_equal_lines(self, mock_get):
        mock_get.return_value.__aenter__.return_value.read.return_value = (
            "<html> a b b c c c d d d d e e e e e f f f f f f </html>"
        )

        lines = ["tu1", "tu2", "tu3\n"]
        text = "\n".join(lines)

        mock_open = mock.AsyncMock()
        mock_open.return_value.__aenter__.return_value.readline = "test url"

        res = [
            ("tu1\n", {"f": 6, "e": 5, "d": 4, "c": 3, "b": 2}),
            ("tu2\n", {"f": 6, "e": 5, "d": 4, "c": 3, "b": 2}),
            ("tu3\n", {"f": 6, "e": 5, "d": 4, "c": 3, "b": 2}),
        ]
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            with mock.patch(
                "builtins.open", new_callable=mock.mock_open, read_data=text
            ):
                val = await batch_fetch("aboba", 3)

                self.assertEqual(val, res)
                self.assertTrue(mock.call("tu1\n") in mock_get.mock_calls)
                self.assertTrue(mock.call("tu2\n") in mock_get.mock_calls)
                self.assertTrue(mock.call("tu3\n") in mock_get.mock_calls)

    @mock.patch("aiohttp.ClientSession.get")
    async def test_batch_fetch_more_workers_that_lines(self, mock_get):
        mock_get.return_value.__aenter__.return_value.read.return_value = (
            "<html> a b b c c c d d d d e e e e e f f f f f f </html>"
        )

        lines = ["tu1", "tu2", "tu3\n"]
        text = "\n".join(lines)

        mock_open = mock.AsyncMock()
        mock_open.return_value.__aenter__.return_value.readline = "test url"

        res = [
            ("tu1\n", {"f": 6, "e": 5, "d": 4, "c": 3, "b": 2}),
            ("tu2\n", {"f": 6, "e": 5, "d": 4, "c": 3, "b": 2}),
            ("tu3\n", {"f": 6, "e": 5, "d": 4, "c": 3, "b": 2}),
        ]
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            with mock.patch(
                "builtins.open", new_callable=mock.mock_open, read_data=text
            ):
                val = await batch_fetch("aboba", 10)

                self.assertEqual(val, res)
                self.assertTrue(mock.call("tu1\n") in mock_get.mock_calls)
                self.assertTrue(mock.call("tu2\n") in mock_get.mock_calls)
                self.assertTrue(mock.call("tu3\n") in mock_get.mock_calls)

    @mock.patch("aiohttp.ClientSession.get")
    async def test_batch_fetch_less_workers_than_lines(self, mock_get):
        mock_get.return_value.__aenter__.return_value.read.return_value = (
            "<html> a b b c c c d d d d e e e e e f f f f f f </html>"
        )

        lines = ["tu1", "tu2", "tu3\n"]
        text = "\n".join(lines)

        mock_open = mock.AsyncMock()
        mock_open.return_value.__aenter__.return_value.readline = "test url"

        res = [
            ("tu1\n", {"f": 6, "e": 5, "d": 4, "c": 3, "b": 2}),
            ("tu2\n", {"f": 6, "e": 5, "d": 4, "c": 3, "b": 2}),
            ("tu3\n", {"f": 6, "e": 5, "d": 4, "c": 3, "b": 2}),
        ]
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            with mock.patch(
                "builtins.open", new_callable=mock.mock_open, read_data=text
            ):
                val = await batch_fetch("aboba", 2)

                self.assertEqual(val, res)
                self.assertTrue(mock.call("tu1\n") in mock_get.mock_calls)
                self.assertTrue(mock.call("tu2\n") in mock_get.mock_calls)
                self.assertTrue(mock.call("tu3\n") in mock_get.mock_calls)

    @mock.patch("fetcher.fetch_url", side_effect=Exception)
    async def test_fetch_worker_fail(self, mock_get):
        mock_get.return_value.__aenter__.return_value.read.return_value = (
            "<html> a b b c c c d d d d e e e e e f f f f f f </html>"
        )

        lines = ["tu1\n"]
        text = "\n".join(lines)

        mock_open = mock.AsyncMock()
        mock_open.return_value.__aenter__.return_value.readline = "test url"

        res = [
            ("tu1\n", {}),
        ]
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            with mock.patch(
                "builtins.open", new_callable=mock.mock_open, read_data=text
            ):
                val = await batch_fetch("aboba", 1)

                self.assertEqual(val, res)
                self.assertTrue(mock.call("tu1\n") in mock_get.mock_calls)

        stdout = f.getvalue()
        self.assertTrue("Undefined error occured" in stdout)
