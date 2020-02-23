from unittest import TestCase
from src.app import app
import json


class TestHome(TestCase):
    def test_get_home(self):
        with app.test_client() as c:
            res = c.get("/")

            self.assertEqual(res.status_code, 200)
            self.assertEqual(
                json.loads(res.get_data()), {"message": "Hello World"}
            )

    def test_post_home(self):
        with app.test_client() as c:
            res = c.post("/")

            self.assertEqual(res.status_code, 405)
