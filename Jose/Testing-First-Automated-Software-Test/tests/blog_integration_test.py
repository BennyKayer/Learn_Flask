from unittest import TestCase
from testing_first_automated_software_test.blog import Blog


class BlogIntegrationTest(TestCase):
    def test_create_post_in_blog(self):
        b = Blog("Test", "Test Author")
        b.create_post("Test Post", "Test Content")

        self.assertEqual(len(b.posts), 1)
        self.assertEqual(b.posts[0].title, "Test Post")
        self.assertEqual(b.posts[0].content, "Test Content")

    def test_json(self):
        b = Blog("Test", "Test Author")
        b2 = Blog("Testina", "Testalon")

        expected_b = {"title": "Test", "author": "Test Author", "posts": []}
        expected_b2 = {"title": "Testina", "author": "Testalon", "posts": []}

        self.assertDictEqual(expected_b, b.json())
        self.assertDictEqual(expected_b2, b2.json())
