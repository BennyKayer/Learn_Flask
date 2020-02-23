from tests.system.base_test import BaseTest
import json


class TestHome(BaseTest):
    def test_get_home(self):
        with self.app() as c:
            res = c.get("/")

            self.assertEqual(res.status_code, 200)
            self.assertEqual(
                json.loads(res.get_data()), {"message": "Hello World"}
            )

    def test_post_home(self):
        with self.app() as c:
            res = c.post("/")

            self.assertEqual(res.status_code, 405)
