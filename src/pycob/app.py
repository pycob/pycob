import flask
from .page import Page
from .request import Request
from .handler import Handler

demo_page = Page('Demo Page')
demo_page.add_header('Demo Page', "2")

class App:
    flask_app = None

    def __init__(self, name: str, app_nav=[]):
        self.flask_app = flask.Flask(__name__)
        self.name = name
        self.nav = app_nav
        self.pages = {"/": demo_page}

    def add_page(self, route: str, page_function):
        endpoint_name = _strip_slashes(route)
        self.flask_app.add_url_rule("/" + endpoint_name, endpoint_name, Handler(page_function))

    # @flask_app.route('/', defaults={'path': ''})
    # @flask_app.route('/<path:path>')
    # def index(path):        
    #     print("Page Path = ", path)
    #     print("Request = ", flask.request)
    #     page = self.__lookup_page(path)
    #     print("Page = ", page)
    #     return 'Web App with Python Flask!'

    def run(self, port=8080):
        self.flask_app.run(debug=True, host='0.0.0.0', port=port)


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