import unittest
import app.msg_of_the_day as myapi
import json
import sys

class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        self.app = myapi.app.test_client()

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(
            json.loads(response.get_data().decode(sys.getdefaultencoding())),
            {"message": "Server Works!"}
        )

if __name__ == '__main__':
    unittest.main()
