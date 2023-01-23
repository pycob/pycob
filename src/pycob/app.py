import flask
from .all_components import Page
from .request import Request
from .handler import Handler
import inspect
import os
import requests
from pathlib import Path


demo_page = Page('Demo Page')
demo_page.add_header('Demo Page', "2")

class App:
    flask_app = None

    def __init__(self, name: str, app_nav=[], api_key=None):
        self.flask_app = flask.Flask(__name__)
        self.name = name
        self.nav = app_nav
        self.pages = {}
        self.api_key = api_key
        self.flask_app.add_url_rule('/favicon.ico', 'favicon.ico', redirect_to="https://cdn.pycob.com/favicon.ico")

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
            print("API request returned: " + str(json_response))
            print("Class of json_response: " + str(type(json_response)))
            return json_response
        except:
            print("API request failed to return valid JSON.")
            return {"error": "API request failed to return valid JSON."}

    def add_page(self, route: str, page_name: str, page_function, show_in_navbar=True, footer_category="All Pages"):
        endpoint_name = _strip_slashes(route)
        self.pages[endpoint_name] = {"page_name": page_name, "show_in_navbar": show_in_navbar, "footer_category": footer_category}
        self.flask_app.add_url_rule("/" + endpoint_name, endpoint_name, Handler(self, page_function), methods=["GET", "POST"])

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

