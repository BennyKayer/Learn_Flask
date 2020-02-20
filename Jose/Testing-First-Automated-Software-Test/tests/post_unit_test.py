from unittest import TestCase
from testing_first_automated_software_test.post import Post


class PostUnitTest(TestCase):
    def test_create_post(self):
        p = Post("Test", "testing unittest")

        self.assertEqual("Test", p.title)
        self.assertEqual("testing unittest", p.content)

    def test_json(self):
        p = Post("Test", "testing unittest")
        expected = {"title": "Test", "content": "testing unittest"}

        self.assertDictEqual(expected, p.json())

    def test_repr(self):
        p = Post("Test", "testing unittest")
        expected = "Test: testing unittest"

        self.assertEqual(expected, str(p))
