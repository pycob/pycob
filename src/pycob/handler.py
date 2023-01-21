# Inspired by https://stackoverflow.com/a/40466535/3179416
from flask import Flask, Response
import flask
from .request import Request
from .all_components import *

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
    navbar = NavbarComponent(pycob_app.name, "https://cdn.pycob.com/pycob_transparent.png")

    for page in pycob_app.pages:
        navbar.add_link(pycob_app.pages[page], "/" + page, "mr-5 hover:text-gray-900")

    return navbar.to_html()

def get_footer_html(pycob_app):
    footer = FooterComponent(pycob_app.name, "Footer Subtitle", "https://cdn.pycob.com/pycob_hex.png")

    footercategory = FootercategoryComponent("Category 1")

    for page in pycob_app.pages:
        footercategory.add_footerlink(pycob_app.pages[page], "/" + page)
    
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
    <meta name="viewport" content="width=device-width, initial-scale=1.0"><title>''' + title + '''</title>
    <script src="https://cdn.tailwindcss.com"></script>
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
            } else {
                document.documentElement.classList.add('dark')
            }
        }
    </script>
    <style>
    .gradient-background {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
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
    </style>
    </head>
    <body class="flex flex-col h-screen dark:bg-gray-900 ">
'''
    return html



_tailwind_body_end = '''            
        </body>
        </html>
    '''