import json
from abc import ABC, abstractmethod

# Base class for all components
class Component:
    @abstractmethod
    def to_html(self) -> str:
        pass

    def _repr_html_(self):
        return self.to_html()

    def to_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

## Begin Generated Code

class HtmlComponent(Component):
  def __init__(self, value: str):
    self.value = value

  def to_html(self):
    return f'''''' + self.value + ''''''

class TextComponent(Component):
  def __init__(self, value: str):
    self.value = value

  def to_html(self):
    return f'''<p>''' + self.value + '''</p>'''

class LinkComponent(Component):
  def __init__(self, text: str, url: str):    
    self.text = text
    self.url = url

  def to_html(self):
    return f'''<a class="mr-5 hover:text-gray-900" href="''' + self.url + '''">''' + self.text + '''</a>'''

class ImageComponent(Component):
  def __init__(self, url: str, alt: str):    
    self.url = url
    self.alt = alt

  def to_html(self):
    return f'''<img class="max-w-fit" src="''' + self.url + '''" alt="''' + self.alt + '''">'''

class HeaderComponent(Component):
  def __init__(self, text: str, size: int):
    self.text = text
    self.size = size

  def to_html(self):
    return f'''<p class="title-font sm:text-''' + self.size + '''xl text-xl font-medium text-gray-900 mb-3">''' + self.text + '''</p>'''

class AlertComponent(Component):
  def __init__(self, text: str, badge: str = '', color: str = 'indigo'):
    self.text = text
    self.badge = badge
    self.color = color

  def to_html(self):
    return f'''<div class="text-center py-4 lg:px-4">
<div class="p-2 bg-''' + self.color + '''-800 items-center text-''' + self.color + '''-100 leading-none lg:rounded-full flex lg:inline-flex" role="alert">
    <span class="flex rounded-full bg-''' + self.color + '''-500 uppercase px-2 py-1 text-xs font-bold mr-3">''' + self.badge + '''</span>
    <span class="font-semibold mr-2 text-left flex-auto">''' + self.text + '''</span>            
</div>
</div>'''

class HeroComponent(Component):
  def __init__(self, title: str, subtitle: str = '', image: str = '', color: str = 'indigo'):
    self.title = title
    self.subtitle = subtitle
    self.image = image
    self.color = color

  def to_html(self):
    return f'''<section class="bg-white">
    <div class="grid max-w-screen-xl px-4 py-8 mx-auto lg:gap-8 xl:gap-0 lg:py-16 lg:grid-cols-12">
        <div class="mr-auto place-self-center lg:col-span-7">
            <h1 class="max-w-2xl mb-4 text-4xl font-extrabold tracking-tight leading-none md:text-5xl xl:text-6xl">''' + self.title + '''</h1>
            <p class="max-w-2xl mb-6 font-light text-gray-500 lg:mb-8 md:text-lg lg:text-xl">''' + self.subtitle + '''</p>
            <a href="#" class="inline-flex items-center justify-center px-5 py-3 mr-3 text-base font-medium text-center text-white rounded-lg bg-''' + self.color + '''-700 hover:bg-''' + self.color + '''-800 focus:ring-4 focus:ring-''' + self.color + '''-300">
                Button 1                        
            </a>
            <a href="#" class="inline-flex items-center justify-center px-5 py-3 text-base font-medium text-center text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-100 focus:ring-4 focus:ring-gray-100">
                Button 2
            </a> 
        </div>
        <div class="hidden lg:mt-0 lg:col-span-5 lg:flex">
            <img src="''' + self.image + '''" >
        </div>                
    </div>
</section>'''

class CodeComponent(Component):
  def __init__(self, value: str, header: str = ''):
    self.value = value
    self.header = header

  def to_html(self):
    return f'''<div class="mx-auto my-10 max-w-3xl">
    <div class="flex h-11 w-full items-center justify-start space-x-1.5 rounded-t-lg bg-gray-900 px-3">
        <span class="h-3 w-3 rounded-full bg-red-400"></span>
        <span class="h-3 w-3 rounded-full bg-yellow-400"></span>
        <span class="h-3 w-3 rounded-full bg-green-400"></span>
        <code class="pl-5 text-lime-500">''' + self.header + '''</code>
    </div>
    <div class="w-full border-t-0 bg-gray-700 pb-5">
        <code class="text-gray-500">&gt&gt&gt</code>
        <code class="text-white">''' + self.value + '''</code>
    </div>
</div>'''

class DividerComponent(Component):
  def __init__(self):
    pass

  def to_html(self):
    return f'''<hr class="my-5 border-gray-300 w-full">'''

class SectionComponent(Component):
  def __init__(self, id: str, name: str, level: int = 1):    
    self.id = id
    self.name = name
    self.level = level

  def to_html(self):
    return f'''<span id=''' + self.id + '''></span>'''

class FormComponent(Component):
  def __init__(self, action: str, components: list = None, method: str = 'GET'):
    self.action = action
    self.components = components or []
    self.method = method

  def to_html(self):
    return f'''<form action="''' + self.action + '''" method="''' + self.method + '''">''' + ''.join(map(lambda x: x.to_html(), self.components)) + '''</form>'''

  def add_formtext(self, label: str, name: str, value: str):    
    self.components.append(FormtextComponent(label, name, value))
    return self


  def add_formsubmit(self, label: str = 'Submit'):    
    self.components.append(FormsubmitComponent(label))
    return self

class FormtextComponent(Component):
  def __init__(self, label: str, name: str, value: str):
    self.label = label
    self.name = name
    self.value = value

  def to_html(self):
    return f'''<div class="relative mb-4">
    <label for="''' + self.name + '''" class="leading-7 text-sm text-gray-600">''' + self.label + '''</label>
    <input name="''' + self.name + '''" type="text" class="w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out" id="''' + self.name + '''" placeholder="''' + self.value + '''">
</div>'''

class FormsubmitComponent(Component):
  def __init__(self, label: str = 'Submit'):
    self.label = label

  def to_html(self):
    return f'''<button type="submit" class="text-white bg-indigo-500 border-0 py-2 px-6 focus:outline-none hover:bg-indigo-600 rounded text-lg">''' + self.label + '''</button>'''


class NavbarComponent(Component):
  def __init__(self, title: str, logo: str = '', components: list = None):    
    self.logo = logo
    self.title = title
    # https://stackoverflow.com/questions/4841782/python-constructor-and-default-value
    self.components = components or []

  def to_html(self):
    return f'''<header class="text-white body-font">
    <div class="gradient-background mx-auto flex flex-wrap p-5 flex-col md:flex-row items-center">
        <a class="flex title-font font-bold items-center text-gray-100 mb-4 md:mb-0"><img class="object-scale-down h-10" src="''' + self.logo + '''"><span class="ml-3 text-4xl">''' + self.title + '''</span></a>
        <nav class="md:ml-auto flex flex-wrap items-center text-base justify-center">
            ''' + '\n'.join(map(lambda x: x.to_html(), self.components)) + ''' 
        </nav>
        <button class="inline-flex items-center bg-gray-100 text-black border-0 py-1 px-3 focus:outline-none hover:bg-gray-200 rounded text-base mt-4 md:mt-0">Sign In<svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="w-4 h-4 ml-1" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"></path></svg></button>
    </div>
</header>'''

  def add_link(self, text: str, url: str):    
    self.components.append(LinkComponent(text, url))
    return self

class FooterComponent(Component):
  def __init__(self, title: str, subtitle: str = '', logo: str = '', components: list = None):    
    self.title = title
    self.subtitle = subtitle
    self.logo = logo
    # https://stackoverflow.com/questions/4841782/python-constructor-and-default-value
    self.components = components or []

  def to_html(self):
    return f'''<footer class="text-gray-600 body-font">
    <div class="container px-5 py-24 mx-auto flex md:items-center lg:items-start md:flex-row md:flex-nowrap flex-wrap flex-col">
        <div class="w-64 flex-shrink-0 md:mx-0 mx-auto text-center md:text-left">
            <a class="flex title-font font-medium items-center md:justify-start justify-center text-gray-900"><img class="object-scale-down h-10" src="''' + self.logo + '''"><span class="ml-3 text-xl">''' + self.title + '''</span></a>
            <p class="mt-2 text-sm text-gray-500">''' + self.subtitle + '''</p>
        </div>
        <div class="flex-grow flex flex-wrap md:pl-20 -mb-10 md:mt-0 mt-10 md:text-left text-center">
            ''' + '\n'.join(map(lambda x: x.to_html(), self.components)) + ''' 
        </div>
    </div>
</footer>'''

  def add_component(self, component: Component):
    self.components.append(component)
    return self

  def add_footercategory(self, title: str, links: list = None):    
    self.components.append(FootercategoryComponent(title, links))
    return self

class FootercategoryComponent(Component):
  def __init__(self, title: str, components: list = None):    
    self.title = title
    # https://stackoverflow.com/questions/4841782/python-constructor-and-default-value
    self.components = components or []

  def to_html(self):
    return f'''<div class="lg:w-1/4 md:w-1/2 w-full px-4">
    <h2 class="title-font font-medium text-gray-900 tracking-widest text-sm mb-3 uppercase">''' + self.title + '''</h2>
    <nav class="list-none mb-10">
        ''' + '\n'.join(map(lambda x: x.to_html(), self.components)) + ''' 
    </nav>
</div>'''

  def add_component(self, component: Component):
    self.components.append(component)
    return self

  def add_footerlink(self, title: str, url: str):    
    self.components.append(FooterlinkComponent(title, url))
    return self

class FooterlinkComponent(Component):
  def __init__(self, title: str, url: str):    
    self.title = title
    self.url = url

  def to_html(self):
    return f'''<li><a href="''' + self.url + '''" class="text-gray-600 hover:text-gray-800">''' + self.title + '''</a></li>'''
