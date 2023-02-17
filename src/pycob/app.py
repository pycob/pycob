import flask
from .all_components import Page
from .request import Request
from .handler import PageHandler, LoginHandler, SignupHandler, LogoutHandler
import inspect
import os
import requests
from pathlib import Path
from .auth_forms import *
import sys
import string
import random
import pickle

demo_page = Page('Demo Page')
demo_page.add_header('Demo Page', 2)

class App:
    flask_app = None

    def __init__(self, name: str, subtitle="", app_nav=[], api_key=None, use_built_in_auth=False, profile_page=profile):
        self.flask_app = flask.Flask(__name__)
        self.name = name
        self.subtitle = subtitle
        self.nav = app_nav
        self.pages = {}
        self.api_key = api_key
        self.use_built_in_auth = use_built_in_auth
        self.profile_page = profile_page
        self.flask_app.add_url_rule('/favicon.ico', 'favicon.ico', redirect_to="https://cdn.pycob.com/favicon.ico")
        self.temp_dir = os.getcwd() + '/tmp/' + ''.join(random.choices(string.ascii_uppercase, k=5))
        self.error = None
        self.home_page_registered = False

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
        self.add_page('/auth/profile', 'auth/profile', self.profile_page, show_in_navbar=False, footer_category=None, require_login=True)

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

    def start_script(self, script_name: str, script_args: dict) -> str:
        if self.api_key is None:
            self.__set_api_key()

        script = {
            "script_name": script_name,
            "args": script_args,
        }
        rv = self.__send_api_request("run_job", script, self.api_key)

        if 'job_id' in rv:
            return rv['job_id']
        
        return ""

    def to_cloud_pickle(self, data, filename: str):
        # Turn data into a pickle with the given filename

        Path(self.temp_dir).mkdir(parents=True, exist_ok=True)

        file = open(self.temp_dir + "/" + filename, 'wb')    
        pickle.dump(data, file)
        file.close()

        url = self._url_for_file_storage(filename)

        if url == "":
            print("Error: Unable to store file")
            return
        
        # Put file with Content-Type: application/octet-stream
        file = open(self.temp_dir + "/" + filename, 'rb')
        requests.put(url, data=file, headers={'Content-Type': 'application/octet-stream'})
        file.close()

    def from_cloud_pickle(self, filename: str):
        try:
            with open(self.temp_dir + "/" + filename, 'rb') as existing_file:
                data = pickle.load(existing_file)
                existing_file.close()
                return data
        except:
            pass

        # Get the pickle with the given filename

        url = self._url_for_file_retrieval(filename)

        if url == "":
            print("Error: Unable to retrieve file")
            return

        # Get file with Accept: application/octet-stream
        rv = requests.get(url, headers={'Accept': 'application/octet-stream'})
        Path(self.temp_dir).mkdir(parents=True, exist_ok=True)
        file = open(self.temp_dir + "/" + filename, 'wb')
        file.write(rv.content)
        file.close()

        file = open(self.temp_dir + "/" + filename, 'rb')
        data = pickle.load(file)
        file.close()

        return data


    def _url_for_file_storage(self, file_name: str) -> str:
        if self.api_key is None:
            self.__set_api_key()

        file = {
            "filename": file_name,
        }
        rv = self.__send_api_request("store_file", file, self.api_key)

        if 'url' in rv:
            return rv['url']

        return ""
    
    def _url_for_file_retrieval(self, file_name: str) -> str:
        if self.api_key is None:
            self.__set_api_key()

        file = {
            "filename": file_name,
        }
        rv = self.__send_api_request("retrieve_file", file, self.api_key)

        if 'url' in rv:
            return rv['url']

        return ""

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

    def delete_dict(self, table_id: str, object_id: str):
        if self.api_key is None:
            self.__set_api_key()

        self.__send_api_request("delete_object", {"object_id": object_id, "table_id": table_id}, self.api_key)        

    def query_dict(self, table_id: str, field_name: str, field_value) -> list:
        if self.api_key is None:
            self.__set_api_key()

        server_response = self.__send_api_request("query_objects", {"field_name": field_name, "table_id": table_id, "field_value": field_value}, self.api_key)

        if type(server_response) is list:
            arr = list(map(lambda x:  x['object'] if 'object' in x else None, server_response))
            num_items = len(arr)
            print(f"Got {num_items} items from the database table {table_id} where {field_name} == {field_value}")
            return arr

    def list_objects(self, table_id: str) -> list:
        if self.api_key is None:
            self.__set_api_key()

        server_response = self.__send_api_request("list_objects", {"table_id": table_id}, self.api_key)

        if type(server_response) is list:
            arr = list(map(lambda x:  x['object'] if 'object' in x else None, server_response))
            num_items = len(arr)
            print(f"Got {num_items} total items from the database table {table_id}")
            return arr

    def list_object_ids(self, table_id: str) -> list:
        if self.api_key is None:
            self.__set_api_key()

        server_response = self.__send_api_request("list_object_ids", {"table_id": table_id}, self.api_key)

        if server_response is not None and 'object_ids' in server_response:
            return server_response['object_ids']

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

                if Path("pycob_api_key.txt").is_file():
                    # Check for api_key.txt file
                    f = open("pycob_api_key.txt", "r")
                    self.api_key = f.read()

                if self.api_key is None:
                    print("No API key found. ")
                    print("Go to https://www.pycob.com to get an API key.")
                    # Exit
                    self.error = 'No API key found. Go to <a href="https://www.pycob.com">https://www.pycob.com</a> to get an API key.'

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
        print("Warning: add_page() is deprecated. Use register_function() instead.")
        endpoint_name = _strip_slashes(route)
        self.pages[endpoint_name] = {"page_name": page_name, "show_in_navbar": show_in_navbar, "footer_category": footer_category}

        redirect_url = None
        if require_login:
            if not self.use_built_in_auth:
                self.error = "You must set use_built_in_auth=True to use the require_login parameter."                
            redirect_url = "/"+endpoint_name

        self.flask_app.add_url_rule("/" + endpoint_name, endpoint_name, PageHandler(self, page_function, redirect_url, protect_with_code), methods=["GET", "POST"])

    def register_function(self, function, show_in_navbar=True, footer_category="All Pages", require_login=False, protect_with_code=None):
        endpoint_name = function.__name__
        self.pages[endpoint_name] = {"page_name": endpoint_name.replace("_", " ").title(), "show_in_navbar": show_in_navbar, "footer_category": footer_category}

        redirect_url = None
        if require_login:
            if not self.use_built_in_auth:
                self.error = "You must set use_built_in_auth=True to use the require_login parameter."                
            redirect_url = "/"+endpoint_name

        self.flask_app.add_url_rule("/" + endpoint_name, endpoint_name, PageHandler(self, function, redirect_url, protect_with_code), methods=["GET", "POST"])

        if not self.home_page_registered:
            self.home_page_registered = True
            self.flask_app.add_url_rule("/", "_home", PageHandler(self, function, redirect_url, protect_with_code), methods=["GET", "POST"])

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

