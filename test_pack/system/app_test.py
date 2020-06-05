from unittest import TestCase
from unittest.mock import patch
import app
import post
from blog import Blog


class AppTest(TestCase):

    def create_test_blog(self):
        blog = Blog("My Test Blog", "Amazing Anonym Author")
        app.blogs_data = {"Test": blog}

        return blog

    def test_print_blogs(self):

        blog = self.create_test_blog()

        with patch("builtins.print") as mocked_print:   ##patches print to see if blogs are printed
            app.print_blogs()
            mocked_print.assert_called_with("- My Test Blog by Amazing Anonym Author - 0 Posts")

    def test_selection_promt(self):

        with patch("builtins.input", return_value="q") as mocked_input:
            app.main_menu()
            mocked_input.assert_called_with(app.MENU_PROMPT)

    def test_menu_calls_print_blogs(self):

        with patch("app.print_blogs") as mocked_print:  ## patches input to check if func called
            with patch("builtins.input", return_value="q"): ## builtins.input, return_value= to return value
                app.main_menu()
                mocked_print.assert_called()

    def test_create_blog(self):

        with patch("builtins.input") as mocked_input:
            mocked_input.side_effect = ("Test Blog", "Test Author")
            app.create_blog()

            self.assertIsNotNone(app.blogs_data.get("Test Blog"))

    def test_read_blogs(self):
        blog = self.create_test_blog()

        with patch("builtins.input", return_value="Test"):
            with patch("app.print_posts") as mocked_print_posts:
                app.read_blog()

                mocked_print_posts.assert_called_with(blog)

    def test_print_posts(self):
        blog = self.create_test_blog()
        blog.create_new_post("Test Post", "Some Awesome Content")

        with patch("app.print_post") as mocked_print_post:
            app.print_posts(blog)
            mocked_print_post.assert_called_with(blog.posts[0])

    def test_print_post(self):
        test_post = post.Post("Test Post Title", "Test Post Content")
        expected_print = '''
    --------------------------
    -Test Post Title
    --------------------------
    
    Test Post Content
    '''

        with patch("builtins.print") as mocked_print:
            app.print_post(test_post)

            mocked_print.assert_called_with(expected_print)
