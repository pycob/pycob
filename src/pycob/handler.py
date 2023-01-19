# Inspired by https://stackoverflow.com/a/40466535/3179416
from flask import Flask, Response
import flask
from .request import Request
from .component import NavbarComponent, FooterComponent, FootercategoryComponent, FooterlinkComponent

class Handler(object):
    def __init__(self, pycob_app, action):
        self.action = action
        self.pycob_app = pycob_app
        self.response = Response(status=200, headers={})

    def __call__(self, *args):        
        page = self.action(Request(flask.request))
        
        if flask.request.accept_mimetypes['application/json'] and (not flask.request.accept_mimetypes['text/html']):
            json_response = page._to_json()
            print(json_response)
            return json_response, '200 OK', {'Content-Type': 'application/json'}

        html = ""

        html += _tailwind_header_to_sidebar

        if page.auto_navbar:
            html += get_navbar_html(self.pycob_app)

        html += page._to_html()

        html += _tailwind_content_end

        if page.auto_footer:
            html += get_footer_html(self.pycob_app)

        html += _tailwind_body_end

        return html

def get_navbar_html(pycob_app):
    navbar = NavbarComponent(pycob_app.name, "https://pycob.com/img/pycob_transparent.png")

    for page in pycob_app.pages:
        navbar.add_link(pycob_app.pages[page], "/" + page)

    return navbar.to_html()

def get_footer_html(pycob_app):
    footer = FooterComponent(pycob_app.name, "Footer Subtitle", "https://pycob.com/img/pycob_hex.png")

    footercategory = FootercategoryComponent("Category 1")

    for page in pycob_app.pages:
        footercategory.add_footerlink(pycob_app.pages[page], "/" + page)
    
    footer.add_component(footercategory)

    return footer.to_html()

_tailwind_header_to_sidebar = '''
<!doctype html>
        <html>
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <script>
            tailwind.config = {
            theme: {
                extend: {
                colors: {
                    clifford: '#da373d',
                }
                }
            }
            }
        </script>
        <style>
        .gradient-background {
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
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
        </style>
        </head>
        <body class="flex flex-col h-screen">
'''
#            <header class="text-white body-font"><div class="gradient-background mx-auto flex flex-wrap p-5 flex-col md:flex-row items-center"><a class="flex title-font font-bold items-center text-gray-100 mb-4 md:mb-0"><span class="ml-3 text-4xl">🌽 PyCob</span></a><nav class="md:ml-auto flex flex-wrap items-center text-base justify-center"><a class="mr-5 hover:text-gray-900">First Link</a><a class="mr-5 hover:text-gray-900">Second Link</a><a class="mr-5 hover:text-gray-900">Third Link</a><a class="mr-5 hover:text-gray-900">Fourth Link</a></nav><button class="inline-flex items-center bg-gray-100 text-black border-0 py-1 px-3 focus:outline-none hover:bg-gray-200 rounded text-base mt-4 md:mt-0">Sign In<svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="w-4 h-4 ml-1" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"></path></svg></button></div></header>
#            <div class="flex">


_tailwind_content_end = '''
                </div>
            </div>
'''

_tailwind_body_end = '''
        </body>
        </html>
    '''