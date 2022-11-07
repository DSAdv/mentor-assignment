import unittest

from main import app


class TestLinkShortenerApp(unittest.TestCase):

    def setUp(self) -> None:
        app.config['CSRF_ENABLED'] = False
        self.client = app.test_client(use_cookies=True)

    def test_index(self):
        with self.client.session_transaction() as session:
            self.assertIsNone(session.get('user_id'))

            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn('Shorten your link', response.data.decode('utf-8'))
            self.assertIn('Set-Cookie', response.headers)
            self.assertIn('session', response.headers.get('Set-Cookie'))

            error_response = self.client.post('/')
            self.assertEqual(error_response.status_code, 200)
            self.assertIn('This field is required', error_response.data.decode('utf-8'))

            data = {'link': 'https://www.google.com/'}
            valid_post_response = self.client.post('/',
                                                   data=data,
                                                   follow_redirects=True,
                                                   headers={"Content-Type": "application/x-www-form-urlencoded"})
            self.assertEqual(valid_post_response.status_code, 200)

    def test_redirect_on_shorten_link(self):
        with self.client.session_transaction() as session:
            self.assertIsNone(session.get('user_id'))

            response = self.client.get('/123456789')
            self.assertEqual(response.status_code, 404)
            self.assertIn('Link not found!', response.data.decode('utf-8'))
            self.assertIn('Go to main page!', response.data.decode('utf-8'))

            valid_post_response = self.client.post('/',
                                                   data={'link': 'https://www.google.com/', 'submit': True},
                                                   follow_redirects=True)
            self.assertEqual(valid_post_response.status_code, 200)
