from unittest import TestCase
from unittest.mock import patch

from testing_first_automated_software_test import app, blog


class AppTest(TestCase):
    def test_menu_prompt(self):

        with patch("builtins.input") as mocked_input:
            app.menu()
            mocked_input.assert_called_with(
                "C. Create a blog\nL. List Blogs\nR. Read blog\nP. Create a Post"
            )

    def test_menu_calls_print_blogs(self):
        with patch("app.print_blogs") as mocked_print_blogs:
            with patch("builtins.input", return_value="q"):
                app.menu()
                mocked_print_blogs.assert_called()

    def test_print_blogs(self):
        b = blog.Blog("Test", "Test Author")
        app.blogs = {"Test": b}

        with patch("builtins.print") as mocked_print:
            app.print_blogs()
            mocked_print.assert_called_with(
                "Test\n Test by Test Author (0 posts)\n"
            )

