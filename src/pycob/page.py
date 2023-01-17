from .component import *

class Page:
  def __init__(self, name: str):
    self.name = name
    self.html = []
    self.components = []

  def _to_html(self):
    return '\n'.join(map(lambda x: x.to_html(), self.components))

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


