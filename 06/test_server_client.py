import unittest
from server import *
from unittest import mock
from queue import Queue
import urllib.request

import server
from client import *
import client

import io
import contextlib


class TestServerClient(unittest.TestCase):
    def test_most_common_words(self):
        resp = "<html> 1 2 2 3 3 , 3 , 4 4 4 4 5 5 5 5 5 6 6 6 6 6 6 </html>"
        most_common = get_most_common_words(resp, 2)

        self.assertDictEqual(most_common, {"6": 6, "5": 5})

    def test_most_common_words_on_letters(self):
        resp = "<html> a b b c c c d d d d e e e e e f f f f f f </html>"
        most_common = get_most_common_words(resp, 3)

        self.assertDictEqual(most_common, {"f": 6, "e": 5, "d": 4})

    @mock.patch("server.urlopen")
    @mock.patch("server.get_most_common_words")
    def test_scrapping_url(self, mock_most_common, mock_urlopen):
        mock_socket = mock.Mock()
        mock_socket.recv.return_value = b"111"

        queue = Queue()
        queue.put(mock_socket)
        queue.put(None)

        mock_urlopen.return_value = "aboba"
        mock_most_common.return_value = "ABOBA"
        scraping_url(queue, 2)

        self.assertEqual([mock.call("111")], mock_urlopen.mock_calls)
        self.assertEqual([mock.call("aboba", 2)], mock_most_common.mock_calls)
        self.assertEqual([mock.call(b'"ABOBA"')], mock_socket.sendall.mock_calls)

    @mock.patch("server.urlopen")
    def test_scrapping_url_with_html(self, mock_urlopen):
        mock_socket = mock.Mock()
        mock_socket.recv.return_value = b"111"

        queue = Queue()
        queue.put(mock_socket)
        queue.put(None)

        mock_urlopen.return_value = (
            "<html> a b b c c c d d d d e e e e e f f f f f f </html>"
        )
        scraping_url(queue, 2)

        self.assertEqual([mock.call("111")], mock_urlopen.mock_calls)
        self.assertEqual(
            [mock.call(b'{"f": 6, "e": 5}')], mock_socket.sendall.mock_calls
        )

    @mock.patch("server.urlopen")
    @mock.patch("server.get_most_common_words")
    def test_global_var_changing(self, mock_most_common, mock_urlopen):
        mock_socket = mock.Mock()
        mock_socket.recv.return_value = b"111"

        prev = server.GL_PROC_URL

        queue = Queue()
        queue.put(mock_socket)
        queue.put(None)

        mock_urlopen.return_value = "aboba"
        mock_most_common.return_value = "ABOBA"
        scraping_url(queue, 2)

        self.assertEqual([mock.call("111")], mock_urlopen.mock_calls)
        self.assertEqual([mock.call("aboba", 2)], mock_most_common.mock_calls)
        self.assertEqual([mock.call(b'"ABOBA"')], mock_socket.sendall.mock_calls)

        self.assertTrue((prev + 1) == server.GL_PROC_URL)

    @mock.patch("client.socket")
    def test_client(self, mock_connection):
        queue = Queue()
        queue.put("111")
        queue.put(None)

        mock_socket = mock.Mock()
        mock_socket.recv.return_value = b"aboba"

        mock_connection.create_connection.return_value.__enter__.return_value = (
            mock_socket
        )

        sa = ("0.0.0.0", "6767")

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            url_send(queue, sa)

        mock_connection.create_connection.assert_called_with(("0.0.0.0", "6767"))
        self.assertEqual(mock_socket.sendall.mock_calls, [mock.call(b"111")])
        self.assertEqual(f.getvalue(), "111: aboba\n")
