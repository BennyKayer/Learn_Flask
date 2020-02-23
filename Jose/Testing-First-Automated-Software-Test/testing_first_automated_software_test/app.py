from testing_first_automated_software_test.blog import Blog

MENU_PROMPT = (
    "C. Create a blog\nL. List Blogs\nR. Read blog\nP. Create a Post\nQ. Quit"
)

POST_TEMPLATE = """
{} 
    
{}
    
"""

blogs = dict()


def print_blogs():
    for key, value in blogs.items():
        print(f"{key}\n {value}\n")


def menu():
    print_blogs()
    selection = input(MENU_PROMPT)
    while selection != "q":
        if selection == "c":
            ask_create_blog()
        elif selection == "l":
            print_blogs()
        elif selection == "r":
            ask_read_blog()
        elif selection == "p":
            ask_create_post()
        selection = input(MENU_PROMPT)


def ask_create_blog():
    title = input("Enter your blog title: ")
    author = input("Enter your name: ")

    blogs[title] = Blog(title, author)


def ask_read_blog():
    title = input("Enter the blog title you want to read: ")
    print_posts(blogs[title])


def print_posts(blog):
    for post in blog.posts:
        print_post(post)


def print_post(post):
    print(POST_TEMPLATE.format(post.title, post.content))


def ask_create_post():
    blog = input("Enter the blog title you want to write a post in: ")
    title = input("Enter you post title")
    content = input("Enter your post content")

    blogs[blog_name].create_post(title, content)
