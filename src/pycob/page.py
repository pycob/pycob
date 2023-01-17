from .component import *

class Page:
  def __init__(self, name: str):
    self.name = name
    self.html = []
    self.components = []

  def _to_html(self):
    return _tailwind_header_to_sidebar + _tailwind_sidebar_end + '\n'.join(map(lambda x: x.to_html(), self.components)) + _tailwind_footer

  def _to_json(self):
    return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

  def _repr_html_(self):
      return '\n'.join(map(lambda x: x._repr_html_(), self.components))

## Begin Generated Code

  def add_html(self, value: str):    
    self.components.append(HtmlComponent(value))
    return self


  def add_text(self, value: str):    
    self.components.append(TextComponent(value))
    return self


  def add_header(self, text: str, size: int):    
    self.components.append(HeaderComponent(text, size))
    return self


  def add_alert(self, text: str, badge: str = '', color: str = 'indigo'):    
    self.components.append(AlertComponent(text, badge, color))
    return self


  def add_hero(self, title: str, subtitle: str = '', image: str = '', color: str = 'indigo'):    
    self.components.append(HeroComponent(title, subtitle, image, color))
    return self


  def add_code(self, value: str, header: str = ''):    
    self.components.append(CodeComponent(value, header))
    return self


  def add_divider(self):    
    self.components.append(DividerComponent())
    return self


  def add_section(self, id: str, name: str, level: int = 1, icon: str = ''):    
    self.components.append(SectionComponent(id, name, level, icon))
    return self

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
        <body>
            <header class="text-white body-font"><div class="gradient-background mx-auto flex flex-wrap p-5 flex-col md:flex-row items-center"><a class="flex title-font font-bold items-center text-gray-100 mb-4 md:mb-0"><span class="ml-3 text-4xl">🌽 PyCob</span></a><nav class="md:ml-auto flex flex-wrap items-center text-base justify-center"><a class="mr-5 hover:text-gray-900">First Link</a><a class="mr-5 hover:text-gray-900">Second Link</a><a class="mr-5 hover:text-gray-900">Third Link</a><a class="mr-5 hover:text-gray-900">Fourth Link</a></nav><button class="inline-flex items-center bg-gray-100 text-black border-0 py-1 px-3 focus:outline-none hover:bg-gray-200 rounded text-base mt-4 md:mt-0">Button<svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="w-4 h-4 ml-1" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"></path></svg></button></div></header>
            <div class="flex">
                <aside class="hidden md:block flex w-72 flex-col space-y-2 bg-slate-200 p-2 h-screen sticky top-0">
'''

_tailwind_sidebar_end = '''
                </aside>            
                <div class="container px-5 py-24 mx-auto max-w-fit">
'''

_tailwind_footer = '''
                </div>
            </div>
            <footer class="text-gray-600 body-font"><div class="container px-5 py-24 mx-auto flex md:items-center lg:items-start md:flex-row md:flex-nowrap flex-wrap flex-col"><div class="w-64 flex-shrink-0 md:mx-0 mx-auto text-center md:text-left"><a class="flex title-font font-medium items-center md:justify-start justify-center text-gray-900">🌽<span class="ml-3 text-xl">PyCob</span></a><p class="mt-2 text-sm text-gray-500">Air plant banjo lyft occupy retro adaptogen indego</p></div><div class="flex-grow flex flex-wrap md:pl-20 -mb-10 md:mt-0 mt-10 md:text-left text-center"><div class="lg:w-1/4 md:w-1/2 w-full px-4"><h2 class="title-font font-medium text-gray-900 tracking-widest text-sm mb-3">CATEGORIES</h2><nav class="list-none mb-10"><li><a class="text-gray-600 hover:text-gray-800">First Link</a></li><li><a class="text-gray-600 hover:text-gray-800">Second Link</a></li><li><a class="text-gray-600 hover:text-gray-800">Third Link</a></li><li><a class="text-gray-600 hover:text-gray-800">Fourth Link</a></li></nav></div><div class="lg:w-1/4 md:w-1/2 w-full px-4"><h2 class="title-font font-medium text-gray-900 tracking-widest text-sm mb-3">CATEGORIES</h2><nav class="list-none mb-10"><li><a class="text-gray-600 hover:text-gray-800">First Link</a></li><li><a class="text-gray-600 hover:text-gray-800">Second Link</a></li><li><a class="text-gray-600 hover:text-gray-800">Third Link</a></li><li><a class="text-gray-600 hover:text-gray-800">Fourth Link</a></li></nav></div><div class="lg:w-1/4 md:w-1/2 w-full px-4"><h2 class="title-font font-medium text-gray-900 tracking-widest text-sm mb-3">CATEGORIES</h2><nav class="list-none mb-10"><li><a class="text-gray-600 hover:text-gray-800">First Link</a></li><li><a class="text-gray-600 hover:text-gray-800">Second Link</a></li><li><a class="text-gray-600 hover:text-gray-800">Third Link</a></li><li><a class="text-gray-600 hover:text-gray-800">Fourth Link</a></li></nav></div><div class="lg:w-1/4 md:w-1/2 w-full px-4"><h2 class="title-font font-medium text-gray-900 tracking-widest text-sm mb-3">CATEGORIES</h2><nav class="list-none mb-10"><li><a class="text-gray-600 hover:text-gray-800">First Link</a></li><li><a class="text-gray-600 hover:text-gray-800">Second Link</a></li><li><a class="text-gray-600 hover:text-gray-800">Third Link</a></li><li><a class="text-gray-600 hover:text-gray-800">Fourth Link</a></li></nav></div></div></div><div class="bg-gray-100"><div class="container mx-auto py-4 px-5 flex flex-wrap flex-col sm:flex-row"><p class="text-gray-500 text-sm text-center sm:text-left">© 2023 PyCob —<a href="https://twitter.com/user" rel="noopener noreferrer" class="text-gray-600 ml-1" target="_blank">@username</a></p><span class="inline-flex sm:ml-auto sm:mt-0 mt-2 justify-center sm:justify-start"><a class="text-gray-500"><svg fill="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="w-5 h-5" viewBox="0 0 24 24"><path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z"></path></svg></a><a class="ml-3 text-gray-500"><svg fill="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="w-5 h-5" viewBox="0 0 24 24"><path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2c9 5 20 0 20-11.5a4.5 4.5 0 00-.08-.83A7.72 7.72 0 0023 3z"></path></svg></a><a class="ml-3 text-gray-500"><svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="w-5 h-5" viewBox="0 0 24 24"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1112.63 8 4 4 0 0116 11.37zm1.5-4.87h.01"></path></svg></a><a class="ml-3 text-gray-500"><svg fill="currentColor" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="0" class="w-5 h-5" viewBox="0 0 24 24"><path stroke="none" d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-2-2 2 2 0 00-2 2v7h-4v-7a6 6 0 016-6zM2 9h4v12H2z"></path><circle cx="4" cy="4" r="2" stroke="none"></circle></svg></a></span></div></div></footer>
        </body>
        </html>
'''

