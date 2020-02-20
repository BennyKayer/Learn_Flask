MENU_PROMPT = "C. Create a blog\nL. List Blogs\nR. Read blog\nP. Create a Post"

blogs = dict()


def print_blogs():
    for key, value in blogs.items():
        print(f"{key}\n {value}\n")


def menu():
    print_blogs()
    selection = input(MENU_PROMPT)

