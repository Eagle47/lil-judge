import unittest

from . import post, get


class LoginMethods(unittest.TestCase):

    def test_login(self):
        response = post("/login/", dict(username='test', password='test'))

        token = response.get('token')
        self.assertTrue(token is not None)

        users = get('/users/', token).json()
        self.assertGreater(len(users), 0)


if __name__ == '__main__':
    unittest.main()