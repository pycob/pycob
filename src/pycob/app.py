import flask
from .all_components import Page
from .request import Request
from .handler import PageHandler, LoginHandler, SignupHandler, LogoutHandler
import inspect
import os
import requests
from pathlib import Path
from .auth_forms import *

demo_page = Page('Demo Page')
demo_page.add_header('Demo Page', "2")

class App:
    flask_app = None

    def __init__(self, name: str, subtitle="", app_nav=[], api_key=None, use_built_in_auth=True):
        self.flask_app = flask.Flask(__name__)
        self.name = name
        self.subtitle = subtitle
        self.nav = app_nav
        self.pages = {}
        self.api_key = api_key
        self.use_built_in_auth = use_built_in_auth
        self.flask_app.add_url_rule('/favicon.ico', 'favicon.ico', redirect_to="https://cdn.pycob.com/favicon.ico")

        if use_built_in_auth:
            if self.api_key is None:
                self.__set_api_key()

            self.flask_app.secret_key = self.api_key
            self.__add_auth_pages()

    def __add_auth_pages(self):        
        self.__add_auth_page('/auth/login', login_with_message(""))
        self.__add_auth_page('/auth/login_retry', login_with_message("Unable to verify. Please try again."))
        self.__add_auth_page('/auth/signup', signup)
        self.__add_auth_page('/auth/logout', logout)
        self.__add_auth_page('/auth/reset_password', reset_password)
        # TODO: Allow developers to use their own profile page
        self.add_page('/auth/profile', 'auth/profile', profile, show_in_navbar=False, footer_category=None, require_login=True)

        self.flask_app.add_url_rule('/auth/__handle_login', "__handle_login", view_func=LoginHandler(self), methods=["POST"])
        self.flask_app.add_url_rule('/auth/__handle_logout', "__handle_logout", view_func=LogoutHandler(self), methods=["POST"])
        self.flask_app.add_url_rule('/auth/__handle_signup', "__handle_signup", view_func=SignupHandler(self), methods=["POST"])


    def __check_login(self, redirect):
        if self.use_built_in_auth:
            if "username" not in flask.session:
                return flask.redirect("/auth/login?redirect=" + redirect)
        return None

    def __login(self, username: str):
        flask.session["username"] = username

    def __add_auth_page(self, url: str, page_function):
        self.flask_app.add_url_rule(url, url, view_func=PageHandler(self, page_function, redirect_url=None, protect_with_code=None), methods=["GET"])

    def send_email(self, from_email: str, to_email: str, subject: str, content: str):
        if self.api_key is None:
            self.__set_api_key()

        email = {
            "from_email": from_email,
            "to_email": to_email,
            "subject": subject,
            "content": content,
        }
        self.__send_api_request("send_email", email, self.api_key)

    def store_dict(self, table_id: str, object_id: str, value: dict):
        if self.api_key is None:
            self.__set_api_key()

        type_name = type(value).__name__
        print("Attempting to save a value of type = ", type_name)
        is_int = "int" in type_name
        is_float = "float" in type_name
        is_str = "str" in type_name
        is_list = "list" in type_name


        to_store = {"table_id": table_id, "object_id": object_id}

        if is_int or is_float or is_str:
            print("Saving flat value to DB")
            to_store['flat_value'] = value
        elif is_list:
            print("Saving list to DB")
            to_store['object_array'] = value
        else:
            print("Saving object to DB")
            to_store['object'] = value

        self.__send_api_request("store_object", to_store, self.api_key)

    def retrieve_dict(self, table_id: str, object_id: str) -> dict:
        if self.api_key is None:
            self.__set_api_key()

        server_response = self.__send_api_request("retrieve_object", {"object_id": object_id, "table_id": table_id}, self.api_key)

        if 'object' in server_response:
            return server_response['object']

    def query_dict(self, table_id: str, field_name: str, field_value) -> list:
        if self.api_key is None:
            self.__set_api_key()

        server_response = self.__send_api_request("query_objects", {"field_name": field_name, "table_id": table_id, "field_value": field_value}, self.api_key)

        if type(server_response) is list:
            arr = list(map(lambda x:  x['object'] if 'object' in x else None, server_response))
            print(arr)
            return arr

    def get_quota_status(self) -> dict:
        if self.api_key is None:
            self.__set_api_key()

        server_response = self.__send_api_request("get_quota_status", {}, self.api_key)

        return server_response

    def generate_text_from_ai(self, prompt: str) -> str:
        if self.api_key is None:
            self.__set_api_key()

        server_response = self.__send_api_request("generate_text_from_ai", {"userPrompt": prompt}, self.api_key)

        if 'text' in server_response:
            return server_response['text']

    def generate_image_from_ai(self, prompt: str) -> str:
        if self.api_key is None:
            self.__set_api_key()

        server_response = self.__send_api_request("generate_image_from_ai", {"userPrompt": prompt}, self.api_key)

        if 'image' in server_response:
            return server_response['image']

    def __set_api_key(self):
        if self.api_key is None:
            # Check PYCOB_API_KEY environment variable
            self.api_key = os.environ.get("PYCOB_API_KEY")

            if self.api_key is None:

                if Path("api_key.txt").is_file():
                    # Check for api_key.txt file
                    f = open("api_key.txt", "r")
                    self.api_key = f.read()

                if self.api_key is None:
                    print("No API key found. Generating a temporary one... This will be saved to api_key.txt")
                    print("Go to https://www.pycob.com to get a permanent API key.")
                    key_response = self.__generate_api_key()

                    print("API key response: " + str(key_response))

                    if 'error' in key_response:
                        print("Error generating API key: " + key_response['error'])
                    if 'key' in key_response:
                        self.api_key = key_response['key']
                        f = open("api_key.txt", "w")
                        f.write(self.api_key)
                        f.close()
                        print("API key saved to api_key.txt")

    def __generate_api_key(self) -> dict:
        return self.__send_api_request("generate_key", {"app_name": self.name}, "")

    def __send_api_request(self, endpoint: str, data: dict, api_key: str) -> dict:
        response = requests.post("https://api.pycob.com/rpc/"+endpoint, json=data, headers={"PYCOB-API-KEY": api_key})
        
        if response.status_code != 200:
            error_str = "API request failed with status code " + str(response.status_code)
            print(error_str)
            return {"error": error_str}

        try:
            json_response = response.json()
            # print("API request returned: " + str(json_response))
            # print("Class of json_response: " + str(type(json_response)))
            return json_response
        except:
            print("API request failed to return valid JSON.")
            return {"error": "API request failed to return valid JSON."}

    def add_page(self, route: str, page_name: str, page_function, show_in_navbar=True, footer_category="All Pages", require_login=False, protect_with_code=None):
        endpoint_name = _strip_slashes(route)
        self.pages[endpoint_name] = {"page_name": page_name, "show_in_navbar": show_in_navbar, "footer_category": footer_category}

        redirect_url = None
        if require_login:
            redirect_url = "/"+endpoint_name
        self.flask_app.add_url_rule("/" + endpoint_name, endpoint_name, PageHandler(self, page_function, redirect_url, protect_with_code), methods=["GET", "POST"])

    def run(self, port=8080, force_dev_mode=False):
        caller = inspect.currentframe().f_back
        called_from_module = caller.f_globals['__name__']
        print("Called from module ", called_from_module)
        if called_from_module == "__main__" or force_dev_mode:
            self.flask_app.run(debug=True, host='0.0.0.0', port=port)
            return None
        else:
            print(__name__)
            print("App is being run by a production server. Returning a runnable server object.")
            return self.flask_app


def _strip_slashes_from_pages_dict(pages_dict: dict) -> dict:
    new_pages_dict = {}
    for key, value in pages_dict.items():
        new_pages_dict[_strip_prefix_suffix(key, '/', '/')] = value
    return new_pages_dict

def _strip_slashes(text: str) -> str:
    return _strip_prefix_suffix(text, '/', '/')

def _strip_prefix(text: str, prefix: str) -> str:
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def _strip_suffix(text: str, suffix: str) -> str:
    if text.endswith(suffix):
        return text[:-len(suffix)]
    return text

def _strip_prefix_suffix(text: str, prefix: str, suffix: str) -> str:
    return _strip_suffix(_strip_prefix(text, prefix), suffix)

