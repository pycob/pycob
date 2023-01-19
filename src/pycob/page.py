from .component import *

class Page:
  def __init__(self, name: str, auto_navbar: bool = True, auto_footer: bool = True):
    self.name = name
    self.auto_navbar = auto_navbar
    self.auto_footer = auto_footer
    self.components = []

  def _to_html(self):
    return '''<div class="flex">''' + self.__get_sidebar() + _tailwind_sidebar_end + '\n'.join(map(lambda x: x.to_html(), self.components))

  def _to_json(self):
    return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

  def _repr_html_(self):
      return '\n'.join(map(lambda x: x._repr_html_(), self.components))

  def add(self, component: Component):
    self.components.append(component)
    return self

  def __get_sidebar(self) -> str:
    # Get all Section components from self.components
    sections = list(filter(lambda x: isinstance(x, SectionComponent), self.components))

    print("Sections: " + str(sections))

    if len(sections) == 0:
      return ""

    sidebar = '''
    <aside class="hidden md:block flex w-72 flex-col space-y-2 bg-slate-200 p-2 h-screen sticky top-0 dark:bg-gray-900 dark:text-gray-100">
    	<nav class="space-y-8 text-sm">
    '''

    last_level = 0

    for section in sections:
      if last_level != 1 and section.level == 1:
        sidebar += '''
        		<div class="space-y-2">
              <a class="text-sm font-semibold tracking-widest uppercase dark:text-gray-400" href="#''' + section.id + '''">'''+ section.name +'''</a>
              <div class="flex flex-col space-y-1">
        '''
      elif last_level == 1 and section.level == 1:
        sidebar += '''
              </div>
            </div>
            <div class="space-y-2">
              <a class="text-sm font-semibold tracking-widest uppercase dark:text-gray-400" href="#''' + section.id + '''">'''+ section.name +'''</a>
              <div class="flex flex-col space-y-1">
        '''
      elif last_level == 1 and section.level != 1:
        sidebar += '''
              </div>
            </div>
            <a rel="noopener noreferrer" href="#''' + section.id + '''">'''+ section.name +'''</a>
        '''
      elif last_level != 1 and section.level != 1:
        sidebar += '''
              <a rel="noopener noreferrer" href="#''' + section.id + '''">'''+ section.name +'''</a>
        '''
      else:
        sidebar += '''<a rel="noopener noreferrer" href="#''' + section.id + '''">'''+ section.name +'''</a>'''

    sidebar += '''
          </nav>
        </aside>
    '''

    return sidebar

  def __add_pandastable(self, df):
    # Pandas dataframe to html
    html = '''<div class="p-8">'''

    html += '''<div class="relative overflow-x-auto shadow-md sm:rounded-lg">'''

    html += '''<table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">'''

    # Pandas DataFrame columns to 
    html += '''<thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">'''

    html += "<tr>"

    # Get df index name
    if df.index.name is not None:
      html += '''<th scope="col" class="px-6 py-3">''' + df.index.name +  "</th>"

    for column in df.columns:
        html += '''<th scope="col" class="px-6 py-3">''' + column + "</th>"

    html += "</tr>"

    html += "</thead>"

    # Pandas DataFrame rows to html
    html += "<tbody>"
    i = 0
    for index, row in df.iterrows():
        if i % 2 == 0:
          html += '''<tr class="bg-white border-b dark:bg-gray-900 dark:border-gray-700">'''
        else:
          html += '''<tr class="bg-gray-50 border-b dark:bg-gray-800 dark:border-gray-700">'''

        for column in df.columns:
            html += '''<td class="px-6 py-4">''' + str(row[column]) + "</td>"
        html += "</tr>"
        i += 1

    html += "</tbody>"

    html += "</table>"

    html += "</div>"

    html += "</div>"

    self.components.append(HtmlComponent(html))
    return self

  ## Add to code generation

  def add_component(self, component: Component):
    self.components.append(component)
    return self


## Begin Generated Code

  def add_html(self, value: str):    
    self.components.append(HtmlComponent(value))
    return self


  def add_text(self, value: str):    
    self.components.append(TextComponent(value))
    return self

  def add_link(self, text: str, url: str):    
    self.components.append(LinkComponent(text, url))
    return self

  def add_image(self, url: str, alt: str):    
    self.components.append(ImageComponent(url, alt))
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


  def add_section(self, id: str, name: str, level: int = 1):    
    self.components.append(SectionComponent(id, name, level))
    return self

  def add_pandastable(self, dataframe: str):
    self.__add_pandastable(dataframe)
    return self

  def add_navbar(self, title: str, logo: str = '', components: list = None):    
    self.components.append(NavbarComponent(title, logo, components))
    return self

  def add_footer(self, title: str, subtitle: str = '', logo: str = '', components: list = None):    
    self.components.append(FooterComponent(title, subtitle, logo, components))
    return self

_tailwind_sidebar_end = '''
                <div class="container px-5 py-24 mx-auto max-w-fit">
'''