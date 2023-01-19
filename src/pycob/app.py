import flask
from .page import Page
from .request import Request
from .handler import Handler
import inspect

demo_page = Page('Demo Page')
demo_page.add_header('Demo Page', "2")

class App:
    flask_app = None

    def __init__(self, name: str, app_nav=[]):
        self.flask_app = flask.Flask(__name__)
        self.name = name
        self.nav = app_nav
        self.pages = {}
        self.flask_app.add_url_rule('/favicon.ico', 'favicon.ico', redirect_to="https://pycob.com/favicon.ico")

    def add_page(self, route: str, page_name: str, page_function):
        endpoint_name = _strip_slashes(route)
        self.pages[endpoint_name] = page_name
        self.flask_app.add_url_rule("/" + endpoint_name, endpoint_name, Handler(self, page_function), methods=["GET", "POST"])

    def run(self, port=8080):
        caller = inspect.currentframe().f_back
        called_from_module = caller.f_globals['__name__']
        print("Called from module ", called_from_module)
        if called_from_module == "__main__":
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
