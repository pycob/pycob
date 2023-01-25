from .request import Request
from .all_components import Page

def profile(server_request: Request) -> Page:
    page = Page("User Profile")

    username = server_request.get_username()

    if username is None or username == "":
        page.add_header("Not Logged In")
        page.add_link("Sign In", "/auth/login")
        return page

    card = page.add_card()

    card.add_header("User Profile")
    card.add_image("https://loremflickr.com/320/240", "User Profile Picture")
    card.add_header(username, size=2)

    form = page.add_form("/auth/__handle_logout", "POST")
    form.add_formsubmit("Sign Out")

    return page

# TODO: Put these functions inside closures that take a message parameter

def login_with_message(message: str):
    def login(server_request: Request) -> Page:
        redirect = server_request.get_query_parameter("redirect")

        page = Page("Sign In")

        card = page.add_card()

        card.add_header("Sign In")

        if message != "":
            card.add_alert(message, badge='Error', color='red')

        form = card.add_form("/auth/__handle_login", "POST")

        form.add_formtext("Username", "username", "username")
        form.add_formpassword()

        if redirect is not None and redirect != "":
            form.add_formhidden("redirect", redirect)

        form.add_formsubmit("Sign In")

        page.add_text("")
        page.add_link("Don't have an account? Sign Up", "/auth/signup")
        page.add_link("Forgot password?", "/auth/reset_password")

        return page
    
    return login

def signup(server_request: Request) -> Page:
    message = server_request.get_query_parameter("message")
    redirect = server_request.get_query_parameter("redirect")

    page = Page("Sign Up")    

    card = page.add_card()

    card.add_header("Sign Up")

    if message != "":
        card.add_alert(message, badge='Error', color='red')

    form = card.add_form("/auth/__handle_signup", "POST")

    form.add_formtext("New Username", "username", "username")
    form.add_formemail()
    form.add_formpassword()
    if redirect is not None and redirect != "":
        form.add_formhidden("redirect", redirect)

    form.add_formsubmit("Sign Up")

    page.add_text("")
    page.add_text("Already have an account?")
    page.add_link("Sign In", "/auth/login")

    return page

def logout(server_request: Request) -> Page:
    page = Page("Sign Out")

    page.add_header("You have been signed out.")

    page.add_link("Sign In", "/auth/login")

    return page

def reset_password(server_request: Request) -> Page:
    page = Page("Reset Password")

    card = page.add_card()

    card.add_header("Reset Password")

    form = card.add_form("/auth/__handle_reset_password", "POST")

    form.add_formtext("Your Username", "username", "username")
    form.add_formemail()

    form.add_formsubmit("Reset Password")

    page.add_text("")
    page.add_link("Sign In", "/auth/login")

    return page

def check_email(server_request: Request) -> Page:
    page = Page("Check Your Email")

    page.add_header("Thank you! Please check your e-mail for next steps.")

    return page

def change_password(server_request: Request) -> Page:
    page = Page("Change Password")

    return page

def forgot_password(server_request: Request) -> Page:
    page = Page("Forgot Password")

    return page

def update_email(server_request: Request) -> Page:
    page = Page("Update Email")

    return page

def verify_email(server_request: Request) -> Page:
    page = Page("Verify Email")

    return page

def verify_email_change(server_request: Request) -> Page:
    page = Page("Verify Email Change")

    return page

