from unittest import TestCase
from testing_first_automated_software_test.post import Post


class PostTest(TestCase):
    def test_create_post(self):
        p = Post("Test", "testing unittest")

        self.assertEqual("Test", p.title)
        self.assertEqual("testing unittest", p.content)

