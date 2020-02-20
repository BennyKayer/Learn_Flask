from unittest import TestCase
from testing_first_automated_software_test.blog import Blog


class BlogUnitTest(TestCase):
    def test_create_blog(self):
        b = Blog("Title", "author")

        self.assertEqual("Title", b.title)
        self.assertEqual("author", b.author)
        self.assertListEqual([], b.posts)

    def test_repr(self):
        b = Blog("LOTR", "Tolkien")
        b2 = Blog("C++", "Prata")

        self.assertEqual(b.__repr__(), "LOTR by Tolkien (0 posts)")
        self.assertEqual(b2.__repr__(), "C++ by Prata (0 posts)")

    def test_repr_multiple_posts(self):
        b = Blog("Test", "Test Author")
        b.posts.append("Jingle")

        self.assertEqual(b.__repr__(), "Test by Test Author (1 posts)")

