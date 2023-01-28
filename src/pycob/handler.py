# Inspired by https://stackoverflow.com/a/40466535/3179416
from flask import Flask, Response
import flask
from .request import Request
from .all_components import *
from werkzeug.security import generate_password_hash, check_password_hash

class LogoutHandler(object):
    def __init__(self, pycob_app):
        self.pycob_app = pycob_app
    
    def __call__(self, *args):
        flask.session.pop('username')
        return flask.redirect("/auth/login")

class LoginHandler(object):
    def __init__(self, pycob_app):
        self.pycob_app = pycob_app
    
    def __call__(self, *args):
        request = Request(flask.request, self.pycob_app)
        username = request.get_query_parameter("username")
        password = request.get_query_parameter("password")
        redirect = request.get_query_parameter("redirect")

        if redirect is None or redirect == "":
            redirect = "/auth/profile"

        user_data = self.pycob_app.retrieve_dict("users", username)

        if user_data is not None and 'password_hash' in user_data and check_password_hash(user_data['password_hash'], password):
            flask.session['username'] = username
            return flask.redirect(redirect)
        else:
            return flask.redirect("/auth/login_retry?redirect=" + redirect)

class SignupHandler(object):
    def __init__(self, pycob_app):
        self.pycob_app = pycob_app
    
    def __call__(self, *args):
        request = Request(flask.request, self.pycob_app)
        username = request.get_query_parameter("username")
        password = request.get_query_parameter("password")
        email = request.get_query_parameter("email")

        user_data = self.pycob_app.retrieve_dict("users", username)

        if user_data is not None:
            return flask.redirect("/auth/signup?message=" + "Username already exists. Please try again.")

        user_data = {
            "username": username,
            "password_hash": generate_password_hash(password),
            "email": email
        }

        self.pycob_app.store_dict("users", username, user_data)
        flask.session['username'] = username

        return flask.redirect("/auth/profile")

class PageHandler(object):
    def __init__(self, pycob_app, action, redirect_url, protect_with_code):
        self.action = action
        self.pycob_app = pycob_app
        self.redirect_url = redirect_url
        self.protect_with_code = protect_with_code
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        request = Request(flask.request, self.pycob_app)

        page = self.action(request)

        if page is None:
            raise ValueError(f'Did you forget to return the page at the end of the {self.action.__name__} function?')

        if self.redirect_url is not None:
            username = request.get_username()

            if username is None or username == "":                
                return flask.redirect("/auth/login?redirect=" + self.redirect_url)

        if self.protect_with_code is not None:
            login_code = request.get_query_parameter("login_code")
            
            if login_code is None or login_code != str(self.protect_with_code):
                page = Page("Enter Code")
                card = page.add_card()
                card.add_header("Enter Code", size=5)
                if login_code != "" and login_code != str(self.protect_with_code):
                    card.add_alert("Incorrect Code", "Error", color="red")
                card.add_text("Contact the developer of this site to give you a code for access")
                form = card.add_form(action="?")

                form.add_formtext("Code", "login_code", "Code from the developer")
                form.add_formsubmit('Enter')


        # if flask.request.accept_mimetypes['application/json'] and (not flask.request.accept_mimetypes['text/html']):
        #     json_response = page._to_json()
        #     print(json_response)
        #     return json_response, '200 OK', {'Content-Type': 'application/json'}

        html = ""

        html += _tailwind_header_to_sidebar(page.title)

        if page.auto_navbar:
            html += get_navbar_html(self.pycob_app)

        # Add a sidebar here
        sidebar = _get_sidebar(page.components)
        if len(sidebar.components) > 0:
            html += '''<div class="flex">'''
            html += sidebar.to_html()

        html += page.to_html()

        if len(sidebar.components) > 0:
            html += "</div>"

        if page.auto_footer:
            html += get_footer_html(self.pycob_app)

        html += _tailwind_body_end

        return html

def get_navbar_html(pycob_app):
    navbar = NavbarComponent(pycob_app.name, "https://cdn.pycob.com/pycob_hex.png")

    for page_path, page_dict in pycob_app.pages.items():
        if page_dict['show_in_navbar']:
            navbar.add_plainlink(page_dict['page_name'], "/" + page_path, "block rounded-lg py-2 pl-3 pr-4 text-white hover:bg-blue-800 md:p-2")

    return navbar.to_html()

def get_footer_html(pycob_app):
    footer = FooterComponent(pycob_app.name, pycob_app.subtitle, "https://cdn.pycob.com/pycob_hex.png")

    categorized = {}

    for page_path, page_dict in pycob_app.pages.items():
        if page_dict['footer_category'] is not None:
            if page_dict['footer_category'] in categorized:
                categorized[page_dict['footer_category']].append( FooterlinkComponent(page_dict['page_name'], "/" + page_path) )
            else:
                categorized[page_dict['footer_category']] = [ FooterlinkComponent(page_dict['page_name'], "/" + page_path) ]

    for category_name, footerlinks in categorized.items():
        footercategory = FootercategoryComponent(category_name, components=footerlinks)
        footer.add_component(footercategory)

    return footer.to_html()

def _get_sidebar(components) -> SidebarComponent:
    sidebar = SidebarComponent()

    sections = list(filter(lambda x: isinstance(x, SectionComponent), components))

    current_category = None

    for section in sections:
        if section.level == 1:
            if current_category is not None:
                sidebar.add_component(current_category)

            current_category = SidebarcategoryComponent(section.name)
        else:
            current_category.add_sidebarlink(section.name, "#" + section.id)
    
    if current_category is not None:
        sidebar.add_component(current_category)

    return sidebar

def _tailwind_header_to_sidebar(title: str) -> str:
    html = '''
    <!doctype html>
    <html>
    <head>
    <meta charset="UTF-8">
    <link rel="apple-touch-icon" sizes="180x180" href="https://cdn.pycob.com/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="https://cdn.pycob.com/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="https://cdn.pycob.com/favicon-16x16.png">
    <link rel="mask-icon" href="https://cdn.pycob.com/safari-pinned-tab.svg" color="#5bbad5">
    <link rel="shortcut icon" href="https://cdn.pycob.com/favicon.ico">
    <meta name="msapplication-TileColor" content="#603cba">
    <meta name="msapplication-config" content="https://cdn.pycob.com/browserconfig.xml">
    <meta name="theme-color" content="#ffffff">
    <meta name="viewport" content="width=device-width, initial-scale=1.0"><title>''' + title + '''</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/ag-grid-community/dist/ag-grid-community.min.js"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        clifford: '#da373d',
                    }
                }
            },
            darkMode: 'class'
        }
    </script>
    <script>
        function toggleDarkMode() {
            if (document.documentElement.classList.contains('dark')) {
                document.documentElement.classList.remove('dark')
                document.getElementById("moon").classList.add("hidden")
                document.getElementById("sun").classList.remove("hidden")
            } else {
                document.documentElement.classList.add('dark')
                document.getElementById("sun").classList.add("hidden")
                document.getElementById("moon").classList.remove("hidden")
            }
        }

        function setLoading() {
            document.querySelectorAll("button[type=submit]").forEach((button) => {
                button.innerHTML = '<svg aria-hidden="true" role="status" class="inline w-4 h-4 mr-3 text-white animate-spin" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="#E5E7EB"/><path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentColor"/></svg>Loading...';
                button.disabled = true;
            });

            setTimeout(() => {
                document.querySelectorAll("button[type=submit]").forEach((button) => {
                    button.innerHTML = 'Try Again';
                    button.disabled = false;
                });
            }, "10000")
        }
    </script>
    <style>
    .gradient-background {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 180s ease infinite;
    }

    .gradient-text {
        color: transparent;
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-clip: text;
        -webkit-background-clip: text;
        animation: gradient 2s ease infinite;
    }

    @keyframes gradient {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }

    @media (min-width: 1024px) {
        #page-container {
            max-width: calc( 100vw - 320px );
        }
    }
    </style>
    </head>
    <body class="flex flex-col h-screen dark:bg-gray-900 ">
'''
    return html



_tailwind_body_end = '''            
        </body>
        </html>
    '''