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
  def __init__(self, id: str, name: str, level: int = 1, icon: str = ''):
    self.id = id
    self.name = name
    self.level = level
    self.icon = icon

  def to_html(self):
    return f'''<span id=''' + self.id + '''></span>'''

