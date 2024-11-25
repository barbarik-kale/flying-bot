from unittest import TestCase

from dotenv import load_dotenv

from src.common import util
from src.common.util import get, post, put, delete


class TestCommon(TestCase):
    def setUp(self):
        load_dotenv()

    def test_get_headers(self):
        headers = util.get_headers(None)
        self.assertIsNotNone(headers.get('Authorization'))

        headers = util.get_headers({
            'header1': 'value1',
            'header2': 'value2'
        })
        self.assertIsNotNone(headers.get('Authorization'))
        self.assertEqual(headers.get('header1'), 'value1')
        self.assertEqual(headers.get('header2'), 'value2')

    def test_get(self):
        url = 'https://google.com'

        response = get(url)
        self.assertTrue('status' in response)
        self.assertTrue('body' in response)
        self.assertTrue('error' in response)

    def test_post(self):
        url = 'https://google.com'

        response = post(url)
        self.assertTrue('status' in response)
        self.assertTrue('body' in response)
        self.assertTrue('error' in response)

    def test_put(self):
        url = 'https://google.com'

        response = put(url)
        self.assertTrue('status' in response)
        self.assertTrue('body' in response)
        self.assertTrue('error' in response)

    def test_delete(self):
        url = 'https://google.com'

        response = delete(url)
        self.assertTrue('status' in response)
        self.assertTrue('body' in response)
        self.assertTrue('error' in response)

