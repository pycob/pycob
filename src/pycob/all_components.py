from __future__ import annotations
from .component_interface import *



class AlertComponent(Component):
  def __init__(self, text: str, badge: str = '', color: str = 'indigo'):    
    self.text = text
    self.badge = badge
    self.color = color
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<div class="text-center py-4 lg:px-4">
<div class="p-2 bg-''' + self.color + '''-800 items-center text-''' + self.color + '''-100 leading-none lg:rounded-full flex lg:inline-flex" role="alert">
    <span class="flex rounded-full bg-''' + self.color + '''-500 uppercase px-2 py-1 text-xs font-bold mr-3">''' + self.badge + '''</span>
    <span class="font-semibold mr-2 text-left flex-auto">''' + self.text + '''</span>            
</div>
</div>'''

class CardComponent(Component):
  def __init__(self, center_content: bool = False, classes: str = '', components: list = None):    
    self.center_content = center_content
    self.classes = classes
    # https://stackoverflow.com/questions/4841782/python-constructor-and-default-value
    self.components = components or []
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<div class="block p-6 mb-6 bg-white border border-gray-200 rounded-lg shadow-md hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700 overflow-x-auto ''' + self.classes + '''">
    <div class="flex flex-col h-full ">
        ''' + '\n'.join(map(lambda x: x.to_html(), self.components)) + ''' 
    </div>
</div>'''

  def add(self, component):
    self.components.append(component)
    return self

  def add_component(self, component):
    self.components.append(component)
    return self
  def add_html(self, value: str) -> HtmlComponent:
    new_component = HtmlComponent(value)    
    self.components.append(new_component)
    return new_component
    

  def add_text(self, value: str) -> TextComponent:
    new_component = TextComponent(value)    
    self.components.append(new_component)
    return new_component
    

  def add_link(self, text: str, url: str, classes: str = '') -> LinkComponent:
    new_component = LinkComponent(text, url, classes)    
    self.components.append(new_component)
    return new_component
    

  def add_plainlink(self, text: str, url: str, classes: str = '') -> PlainlinkComponent:
    new_component = PlainlinkComponent(text, url, classes)    
    self.components.append(new_component)
    return new_component
    

  def add_list(self, show_dots: bool = True, classes: str = '', components: list = None) -> ListComponent:
    new_component = ListComponent(show_dots, classes, components)    
    self.components.append(new_component)
    return new_component
    

  def add_image(self, url: str, alt: str, classes: str = '') -> ImageComponent:
    new_component = ImageComponent(url, alt, classes)    
    self.components.append(new_component)
    return new_component
    

  def add_header(self, text: str, size: int = 5) -> HeaderComponent:
    new_component = HeaderComponent(text, size)    
    self.components.append(new_component)
    return new_component
    

  def add_card(self, center_content: bool = False, classes: str = '', components: list = None) -> CardComponent:
    new_component = CardComponent(center_content, classes, components)    
    self.components.append(new_component)
    return new_component
    

  def add_container(self, grid_columns: int = None, classes: str = '', components: list = None) -> ContainerComponent:
    new_component = ContainerComponent(grid_columns, classes, components)    
    self.components.append(new_component)
    return new_component
    

  def add_alert(self, text: str, badge: str = '', color: str = 'indigo') -> AlertComponent:
    new_component = AlertComponent(text, badge, color)    
    self.components.append(new_component)
    return new_component
    

  def add_code(self, value: str, header: str = '', prefix: str = '>>>') -> CodeComponent:
    new_component = CodeComponent(value, header, prefix)    
    self.components.append(new_component)
    return new_component
    

  def add_divider(self) -> DividerComponent:
    new_component = DividerComponent()    
    self.components.append(new_component)
    return new_component
    

  def add_form(self, action: str, method: str = 'GET', components: list = None) -> FormComponent:
    new_component = FormComponent(action, method, components)    
    self.components.append(new_component)
    return new_component
    

  def add_rawtable(self, components: list = None) -> RawtableComponent:
    new_component = RawtableComponent(components)    
    self.components.append(new_component)
    return new_component
    


  def add_pandastable(self, dataframe):
    advanced_add_pandastable(self, dataframe)
    return self
    


  def add_datagrid(self, dataframe, action_buttons: list = None):
    advanced_add_datagrid(self, dataframe, action_buttons)
    return self
    


  def add_emgithub(self, url: str):
    advanced_add_emgithub(self, url)
    return self
    

class CodeComponent(Component):
  def __init__(self, value: str, header: str = '', prefix: str = '>>>'):    
    self.value = value
    self.header = header
    self.prefix = prefix
    # Replace < and > in prefix:
    self.prefix = self.prefix.replace("<", "&lt;").replace(">", "&gt;")

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<div class="mx-auto my-10 max-w-3xl">
    <div class="flex h-11 w-full items-center justify-start space-x-1.5 rounded-t-lg bg-gray-900 px-3">
        <span class="h-3 w-3 rounded-full bg-red-400"></span>
        <span class="h-3 w-3 rounded-full bg-yellow-400"></span>
        <span class="h-3 w-3 rounded-full bg-green-400"></span>
        <code class="pl-5 text-lime-500">''' + self.header + '''</code>
    </div>
    <div class="w-full border-t-0 bg-gray-700 pb-5 rounded-b-lg whitespace-nowrap overflow-x-scroll p-2">
        <code class="text-gray-500">''' + self.prefix + '''</code>
        <code class="text-white" style="white-space: break-spaces">''' + self.value + '''</code>
    </div>
</div>'''

class CodeeditorComponent(Component):
  def __init__(self, value: str, language: str = 'python'):    
    self.value = value
    self.language = language
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<style type="text/css" media="screen">
#editorContainer {
    width: calc( 100vw - 40px );
    height: 500px;
    max-height: calc( 80vh - 60px );
    position: relative;
    background-color: red;
}
#editor { 
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
}
</style>

<div id="editorContainer">
    <div id="editor">''' + self.value + '''</div> 
</div>
<script src="https://cdn.jsdelivr.net/gh/ajaxorg/ace-builds/src-noconflict/ace.js" type="text/javascript" charset="utf-8"></script>
<script>
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.session.setMode("ace/mode/''' + self.language + '''");

    const savedCode = localStorage.getItem('code');

    if (savedCode) {
        editor.setValue(savedCode);
    }
</script>'''

class ContainerComponent(Component):
  def __init__(self, grid_columns: int = None, classes: str = '', components: list = None):    
    self.grid_columns = grid_columns
    self.classes = classes
    # https://stackoverflow.com/questions/4841782/python-constructor-and-default-value
    self.components = components or []
    if grid_columns is not None:
        self.classes += " grid gap-6 md:grid-cols-" + str(grid_columns)

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<div class=" ''' + self.classes + '''">
    ''' + '\n'.join(map(lambda x: x.to_html(), self.components)) + ''' 
</div>'''

  def add(self, component):
    self.components.append(component)
    return self

  def add_component(self, component):
    self.components.append(component)
    return self
  def add_html(self, value: str) -> HtmlComponent:
    new_component = HtmlComponent(value)    
    self.components.append(new_component)
    return new_component
    

  def add_text(self, value: str) -> TextComponent:
    new_component = TextComponent(value)    
    self.components.append(new_component)
    return new_component
    

  def add_link(self, text: str, url: str, classes: str = '') -> LinkComponent:
    new_component = LinkComponent(text, url, classes)    
    self.components.append(new_component)
    return new_component
    

  def add_plainlink(self, text: str, url: str, classes: str = '') -> PlainlinkComponent:
    new_component = PlainlinkComponent(text, url, classes)    
    self.components.append(new_component)
    return new_component
    

  def add_list(self, show_dots: bool = True, classes: str = '', components: list = None) -> ListComponent:
    new_component = ListComponent(show_dots, classes, components)    
    self.components.append(new_component)
    return new_component
    

  def add_image(self, url: str, alt: str, classes: str = '') -> ImageComponent:
    new_component = ImageComponent(url, alt, classes)    
    self.components.append(new_component)
    return new_component
    

  def add_header(self, text: str, size: int = 5) -> HeaderComponent:
    new_component = HeaderComponent(text, size)    
    self.components.append(new_component)
    return new_component
    

  def add_card(self, center_content: bool = False, classes: str = '', components: list = None) -> CardComponent:
    new_component = CardComponent(center_content, classes, components)    
    self.components.append(new_component)
    return new_component
    

  def add_container(self, grid_columns: int = None, classes: str = '', components: list = None) -> ContainerComponent:
    new_component = ContainerComponent(grid_columns, classes, components)    
    self.components.append(new_component)
    return new_component
    

  def add_alert(self, text: str, badge: str = '', color: str = 'indigo') -> AlertComponent:
    new_component = AlertComponent(text, badge, color)    
    self.components.append(new_component)
    return new_component
    

  def add_code(self, value: str, header: str = '', prefix: str = '>>>') -> CodeComponent:
    new_component = CodeComponent(value, header, prefix)    
    self.components.append(new_component)
    return new_component
    

  def add_form(self, action: str, method: str = 'GET', components: list = None) -> FormComponent:
    new_component = FormComponent(action, method, components)    
    self.components.append(new_component)
    return new_component
    

class DividerComponent(Component):
  def __init__(self):    
    pass
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<hr class="my-5 border-gray-300 w-full">'''

class FooterComponent(Component):
  def __init__(self, title: str, subtitle: str = '', logo: str = '', components: list = None):    
    self.title = title
    self.subtitle = subtitle
    self.logo = logo
    # https://stackoverflow.com/questions/4841782/python-constructor-and-default-value
    self.components = components or []
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<footer class="text-gray-600 body-font">
    <div class="container px-5 mx-auto flex md:items-center lg:items-start md:flex-row md:flex-nowrap flex-wrap flex-col">
        <div class="w-64 flex-shrink-0 md:mx-0 mx-auto text-center md:text-left">
            <a class="flex title-font font-medium items-center md:justify-start justify-center text-gray-900 dark:text-white"><img class="object-scale-down h-10" src="''' + self.logo + '''"><span class="ml-3 text-xl">''' + self.title + '''</span></a>
            <p class="mt-2 text-sm text-gray-500">''' + self.subtitle + '''</p>
        </div>
        <div class="flex-grow flex flex-wrap md:pl-20 -mb-10 md:mt-0 mt-10 md:text-left text-center">
            ''' + '\n'.join(map(lambda x: x.to_html(), self.components)) + ''' 
        </div>
    </div>
</footer>'''

  def add(self, component):
    self.components.append(component)
    return self

  def add_component(self, component):
    self.components.append(component)
    return self
  def add_footercategory(self, title: str, components: list = None) -> FootercategoryComponent:
    new_component = FootercategoryComponent(title, components)    
    self.components.append(new_component)
    return new_component
    

class FootercategoryComponent(Component):
  def __init__(self, title: str, components: list = None):    
    self.title = title
    # https://stackoverflow.com/questions/4841782/python-constructor-and-default-value
    self.components = components or []
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<div class="lg:w-1/4 md:w-1/2 w-full px-4">
    <h2 class="title-font font-medium text-gray-900 dark:text-white tracking-widest text-sm mb-3 uppercase">''' + self.title + '''</h2>
    <nav class="list-none mb-10">
        ''' + '\n'.join(map(lambda x: x.to_html(), self.components)) + ''' 
    </nav>
</div>'''

  def add(self, component):
    self.components.append(component)
    return self

  def add_component(self, component):
    self.components.append(component)
    return self
  def add_footerlink(self, title: str, url: str) -> FooterlinkComponent:
    new_component = FooterlinkComponent(title, url)    
    self.components.append(new_component)
    return new_component
    

class FooterlinkComponent(Component):
  def __init__(self, title: str, url: str):    
    self.title = title
    self.url = url
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<li><a href="''' + self.url + '''" class="text-gray-600 hover:text-gray-800 dark:hover:text-white">''' + self.title + '''</a></li>'''

class FormComponent(Component):
  def __init__(self, action: str, method: str = 'GET', components: list = None):    
    self.action = action
    self.method = method
    # https://stackoverflow.com/questions/4841782/python-constructor-and-default-value
    self.components = components or []
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<form class="max-w-full" style="width: 500px" onsubmit="setLoading()" action="''' + self.action + '''" method="''' + self.method + '''">
    ''' + '\n'.join(map(lambda x: x.to_html(), self.components)) + ''' 
</form>'''

  def add(self, component):
    self.components.append(component)
    return self

  def add_component(self, component):
    self.components.append(component)
    return self
  def add_text(self, value: str) -> TextComponent:
    new_component = TextComponent(value)    
    self.components.append(new_component)
    return new_component
    

  def add_link(self, text: str, url: str, classes: str = '') -> LinkComponent:
    new_component = LinkComponent(text, url, classes)    
    self.components.append(new_component)
    return new_component
    

  def add_list(self, show_dots: bool = True, classes: str = '', components: list = None) -> ListComponent:
    new_component = ListComponent(show_dots, classes, components)    
    self.components.append(new_component)
    return new_component
    

  def add_image(self, url: str, alt: str, classes: str = '') -> ImageComponent:
    new_component = ImageComponent(url, alt, classes)    
    self.components.append(new_component)
    return new_component
    

  def add_container(self, grid_columns: int = None, classes: str = '', components: list = None) -> ContainerComponent:
    new_component = ContainerComponent(grid_columns, classes, components)    
    self.components.append(new_component)
    return new_component
    

  def add_code(self, value: str, header: str = '', prefix: str = '>>>') -> CodeComponent:
    new_component = CodeComponent(value, header, prefix)    
    self.components.append(new_component)
    return new_component
    

  def add_formtext(self, label: str, name: str, placeholder: str = '') -> FormtextComponent:
    new_component = FormtextComponent(label, name, placeholder)    
    self.components.append(new_component)
    return new_component
    

  def add_formemail(self, label: str = 'Your E-mail', name: str = 'email', placeholder: str = 'user@example.com') -> FormemailComponent:
    new_component = FormemailComponent(label, name, placeholder)    
    self.components.append(new_component)
    return new_component
    

  def add_formpassword(self, label: str = 'Password', name: str = 'password', placeholder: str = 'password') -> FormpasswordComponent:
    new_component = FormpasswordComponent(label, name, placeholder)    
    self.components.append(new_component)
    return new_component
    

  def add_formselect(self, label: str, name: str, options) -> FormselectComponent:
    new_component = FormselectComponent(label, name, options)    
    self.components.append(new_component)
    return new_component
    

  def add_formhidden(self, name: str, value: str) -> FormhiddenComponent:
    new_component = FormhiddenComponent(name, value)    
    self.components.append(new_component)
    return new_component
    

  def add_textarea(self, label: str = 'Your Message', name: str = 'message', placeholder: str = 'Leave a comment...') -> TextareaComponent:
    new_component = TextareaComponent(label, name, placeholder)    
    self.components.append(new_component)
    return new_component
    

  def add_formsubmit(self, label: str = 'Submit') -> FormsubmitComponent:
    new_component = FormsubmitComponent(label)    
    self.components.append(new_component)
    return new_component
    

  def add_rawtable(self, components: list = None) -> RawtableComponent:
    new_component = RawtableComponent(components)    
    self.components.append(new_component)
    return new_component
    

class FormemailComponent(Component):
  def __init__(self, label: str = 'Your E-mail', name: str = 'email', placeholder: str = 'user@example.com'):    
    self.label = label
    self.name = name
    self.placeholder = placeholder
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<div class="mb-6">
    <label for="''' + self.name + '''" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">''' + self.label + '''</label>
    <input type="email" name="''' + self.name + '''" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="''' + self.placeholder + '''" required>
</div>'''

class FormhiddenComponent(Component):
  def __init__(self, name: str, value: str):    
    self.name = name
    self.value = value
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<input type="hidden" name="''' + self.name + '''" value="''' + self.value + '''">'''

class FormpasswordComponent(Component):
  def __init__(self, label: str = 'Password', name: str = 'password', placeholder: str = 'password'):    
    self.label = label
    self.name = name
    self.placeholder = placeholder
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<div class="mb-6">
    <label for="''' + self.name + '''" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">''' + self.label + '''</label>
    <input type="password" name="''' + self.name + '''" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="''' + self.placeholder + '''" required>
</div>'''

class FormselectComponent(Component):
  def __init__(self, label: str, name: str, options):    
    self.label = label
    self.name = name
    self.options = options
    self.components = []
    for option in self.options:
        self.components.append(SelectoptionComponent(label=option['label'], value=option['value']))

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<div class="mb-6">
    <label for="''' + self.name + '''" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Select an option</label>
    <select id="''' + self.name + '''" name="''' + self.name + '''" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
        ''' + '\n'.join(map(lambda x: x.to_html(), self.components)) + ''' 
    </select>
</div>'''

  def add_selectoption(self, label: str, value: str) -> SelectoptionComponent:
    new_component = SelectoptionComponent(label, value)    
    self.components.append(new_component)
    return new_component
    

class FormsubmitComponent(Component):
  def __init__(self, label: str = 'Submit'):    
    self.label = label
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<button type="submit" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">''' + self.label + '''</button>'''

class FormtextComponent(Component):
  def __init__(self, label: str, name: str, placeholder: str = ''):    
    self.label = label
    self.name = name
    self.placeholder = placeholder
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<div class="mb-6">
    <label for="''' + self.name + '''" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">''' + self.label + '''</label>
    <input type="text" name="''' + self.name + '''" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="''' + self.placeholder + '''" required>
</div>'''

class HeaderComponent(Component):
  def __init__(self, text: str, size: int = 5):    
    self.text = text
    self.size = size
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<p class="mb-4 font-extrabold leading-none tracking-tight text-gray-900 md:text-lg lg:text-''' + str(self.size) + '''xl dark:text-white">''' + self.text + '''</p>'''

class HtmlComponent(Component):
  def __init__(self, value: str):    
    self.value = value
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''''' + self.value + ''''''

class ImageComponent(Component):
  def __init__(self, url: str, alt: str, classes: str = ''):    
    self.url = url
    self.alt = alt
    self.classes = classes
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<img class="max-w-fit h-auto rounded-lg ''' + self.classes + ''' " src="''' + self.url + '''" alt="''' + self.alt + '''">'''

class LinkComponent(Component):
  def __init__(self, text: str, url: str, classes: str = ''):    
    self.text = text
    self.url = url
    self.classes = classes
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<p class="text-gray-500 dark:text-gray-400 ''' + self.classes + '''">
    <a href="''' + self.url + '''" class="inline-flex items-center font-medium text-blue-600 dark:text-blue-500 hover:underline">
    ''' + self.text + '''
    <svg aria-hidden="true" class="w-5 h-5 ml-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
    </a>
</p>'''

class ListComponent(Component):
  def __init__(self, show_dots: bool = True, classes: str = '', components: list = None):    
    self.show_dots = show_dots
    self.classes = classes
    # https://stackoverflow.com/questions/4841782/python-constructor-and-default-value
    self.components = components or []
    if self.show_dots:
        self.classes += "list-disc"
    else:
        self.classes += "list-none"

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<ul class="max-w-md space-y-1 text-gray-500 list-inside dark:text-gray-400 ''' + self.classes + '''">
    ''' + '\n'.join(map(lambda x: x.to_html(), self.components)) + ''' 
</ul>'''

  def add(self, component):
    self.components.append(component)
    return self

  def add_component(self, component):
    self.components.append(component)
    return self
  def add_listitem(self, value: str, classes: str = '', svg: str = '', is_checked: bool = None) -> ListitemComponent:
    new_component = ListitemComponent(value, classes, svg, is_checked)    
    self.components.append(new_component)
    return new_component
    

class ListitemComponent(Component):
  def __init__(self, value: str, classes: str = '', svg: str = '', is_checked: bool = None):    
    self.value = value
    self.classes = classes
    self.svg = svg
    self.is_checked = is_checked
    if self.is_checked is not None:
        if self.is_checked:
            self.svg = '''<svg class="w-4 h-4 mr-1.5 text-green-500 dark:text-green-400 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>'''
        else:
            self.svg = '''<svg class="w-4 h-4 mr-1.5 text-gray-400 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path></svg>'''
    else:
        self.svg = ""

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<li class="flex items-center">
    ''' + self.svg + '''
    ''' + self.value + '''
</li>'''

class NavbarComponent(Component):
  def __init__(self, title: str, logo: str = '', components: list = None):    
    self.title = title
    self.logo = logo
    # https://stackoverflow.com/questions/4841782/python-constructor-and-default-value
    self.components = components or []
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<script>
    function toggleNav() {
        var nav = document.getElementById("navbar-sticky");
        if (nav.classList.contains("hidden")) {
            nav.classList.remove("hidden");
        } else {
            nav.classList.add("hidden");
        }
    }
    function login() {
        document.location.href = "/auth" + "/login"
        console.log("login")
    }
</script>
<nav class="gradient-background top-0 left-0 z-20 w-full bg-white px-2 py-2.5 dark:border-gray-600 sm:px-4">
    <div class="container mx-auto flex flex-wrap items-center justify-between">
      <a href="/" class="flex items-center">
        <img src="''' + self.logo + '''" class="mr-3 h-6 sm:h-9" style="filter: brightness(0) invert(1);" alt="Logo" />
        <span class="self-center whitespace-nowrap md:text-4xl font-semibold text-white">''' + self.title + '''</span>
      </a>
      <div class="flex md:order-2">
        <button onclick="toggleDarkMode()" type="button" class="mx-3 px-3 py-2 text-xs font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800 bg-gradient-to-br from-purple-600 to-blue-500 group-hover:from-purple-600 group-hover:to-blue-500">
            <svg id="sun" data-toggle-icon="sun" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" fill-rule="evenodd" clip-rule="evenodd"></path></svg>
            <svg id="moon" data-toggle-icon="moon" class="w-4 h-4 hidden" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path></svg>        </button>
        <button type="button" onclick="login()" id="pycob-login-button" class="mr-3 inline-flex items-center rounded-lg bg-blue-700 px-2 py-1 text-center text-xs font-medium text-white hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 md:mr-0">
          Sign In
          <svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="ml-1 h-4 w-4" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"></path></svg>
        </button>
        <button onclick="toggleNav()" data-collapse-toggle="navbar-sticky" type="button" class="inline-flex items-center rounded-lg p-2 text-sm text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-white dark:hover:bg-gray-700 dark:focus:ring-gray-600 md:hidden" aria-controls="navbar-sticky" aria-expanded="true">
          <span class="sr-only">Open main menu</span>
          <svg class="h-6 w-6" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"></path></svg>
        </button>
      </div>
      <div class="w-full items-center justify-between md:order-1 md:flex md:w-auto hidden" id="navbar-sticky">
        <ul class="mt-4 flex flex-col rounded-lg md:mt-0 md:flex-row md:space-x-8 md:border-0 md:text-sm md:font-medium">
          ''' + '\n'.join(map(lambda x: x.to_html(), self.components)) + ''' 
        </ul>
      </div>
    </div>
  </nav>'''

  def add(self, component):
    self.components.append(component)
    return self

  def add_component(self, component):
    self.components.append(component)
    return self
  def add_link(self, text: str, url: str, classes: str = '') -> LinkComponent:
    new_component = LinkComponent(text, url, classes)    
    self.components.append(new_component)
    return new_component
    

  def add_plainlink(self, text: str, url: str, classes: str = '') -> PlainlinkComponent:
    new_component = PlainlinkComponent(text, url, classes)    
    self.components.append(new_component)
    return new_component
    

class Page(Component):
  def __init__(self, title: str, auto_navbar: bool = True, auto_footer: bool = True, components: list = None):    
    self.title = title
    self.auto_navbar = auto_navbar
    self.auto_footer = auto_footer
    # https://stackoverflow.com/questions/4841782/python-constructor-and-default-value
    self.components = components or []
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<div id="page-container" class="container px-5 my-5 mx-auto max-w-fit">
    ''' + '\n'.join(map(lambda x: x.to_html(), self.components)) + ''' 
</div>'''

  def add(self, component):
    self.components.append(component)
    return self

  def add_component(self, component):
    self.components.append(component)
    return self
  def add_html(self, value: str) -> HtmlComponent:
    new_component = HtmlComponent(value)    
    self.components.append(new_component)
    return new_component
    

  def add_text(self, value: str) -> TextComponent:
    new_component = TextComponent(value)    
    self.components.append(new_component)
    return new_component
    

  def add_link(self, text: str, url: str, classes: str = '') -> LinkComponent:
    new_component = LinkComponent(text, url, classes)    
    self.components.append(new_component)
    return new_component
    

  def add_plainlink(self, text: str, url: str, classes: str = '') -> PlainlinkComponent:
    new_component = PlainlinkComponent(text, url, classes)    
    self.components.append(new_component)
    return new_component
    

  def add_list(self, show_dots: bool = True, classes: str = '', components: list = None) -> ListComponent:
    new_component = ListComponent(show_dots, classes, components)    
    self.components.append(new_component)
    return new_component
    

  def add_image(self, url: str, alt: str, classes: str = '') -> ImageComponent:
    new_component = ImageComponent(url, alt, classes)    
    self.components.append(new_component)
    return new_component
    

  def add_header(self, text: str, size: int = 5) -> HeaderComponent:
    new_component = HeaderComponent(text, size)    
    self.components.append(new_component)
    return new_component
    

  def add_card(self, center_content: bool = False, classes: str = '', components: list = None) -> CardComponent:
    new_component = CardComponent(center_content, classes, components)    
    self.components.append(new_component)
    return new_component
    

  def add_container(self, grid_columns: int = None, classes: str = '', components: list = None) -> ContainerComponent:
    new_component = ContainerComponent(grid_columns, classes, components)    
    self.components.append(new_component)
    return new_component
    

  def add_alert(self, text: str, badge: str = '', color: str = 'indigo') -> AlertComponent:
    new_component = AlertComponent(text, badge, color)    
    self.components.append(new_component)
    return new_component
    

  def add_code(self, value: str, header: str = '', prefix: str = '>>>') -> CodeComponent:
    new_component = CodeComponent(value, header, prefix)    
    self.components.append(new_component)
    return new_component
    

  def add_divider(self) -> DividerComponent:
    new_component = DividerComponent()    
    self.components.append(new_component)
    return new_component
    

  def add_section(self, id: str, name: str, level: int = 1) -> SectionComponent:
    new_component = SectionComponent(id, name, level)    
    self.components.append(new_component)
    return new_component
    

  def add_form(self, action: str, method: str = 'GET', components: list = None) -> FormComponent:
    new_component = FormComponent(action, method, components)    
    self.components.append(new_component)
    return new_component
    

  def add_rawtable(self, components: list = None) -> RawtableComponent:
    new_component = RawtableComponent(components)    
    self.components.append(new_component)
    return new_component
    


  def add_pandastable(self, dataframe):
    advanced_add_pandastable(self, dataframe)
    return self
    


  def add_datagrid(self, dataframe, action_buttons: list = None):
    advanced_add_datagrid(self, dataframe, action_buttons)
    return self
    

  def add_navbar(self, title: str, logo: str = '', components: list = None) -> NavbarComponent:
    new_component = NavbarComponent(title, logo, components)    
    self.components.append(new_component)
    return new_component
    

  def add_footer(self, title: str, subtitle: str = '', logo: str = '', components: list = None) -> FooterComponent:
    new_component = FooterComponent(title, subtitle, logo, components)    
    self.components.append(new_component)
    return new_component
    

  def add_sidebar(self, components: list = None) -> SidebarComponent:
    new_component = SidebarComponent(components)    
    self.components.append(new_component)
    return new_component
    

  def add_codeeditor(self, value: str, language: str = 'python') -> CodeeditorComponent:
    new_component = CodeeditorComponent(value, language)    
    self.components.append(new_component)
    return new_component
    


  def add_emgithub(self, url: str):
    advanced_add_emgithub(self, url)
    return self
    

class PlainlinkComponent(Component):
  def __init__(self, text: str, url: str, classes: str = ''):    
    self.text = text
    self.url = url
    self.classes = classes
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<a class="''' + self.classes + '''" href="''' + self.url + '''">''' + self.text + '''</a>'''

class RawtableComponent(Component):
  def __init__(self, components: list = None):    
    # https://stackoverflow.com/questions/4841782/python-constructor-and-default-value
    self.components = components or []
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<div class="relative overflow-x-auto shadow-md mb-5 sm:rounded-lg">
    <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
        ''' + '\n'.join(map(lambda x: x.to_html(), self.components)) + ''' 
    </table>
</div>'''

  def add(self, component):
    self.components.append(component)
    return self

  def add_component(self, component):
    self.components.append(component)
    return self
  def add_tablehead(self, components: list = None) -> TableheadComponent:
    new_component = TableheadComponent(components)    
    self.components.append(new_component)
    return new_component
    

  def add_tablerow(self, components: list = None) -> TablerowComponent:
    new_component = TablerowComponent(components)    
    self.components.append(new_component)
    return new_component
    

  def add_tablebody(self, components: list = None) -> TablebodyComponent:
    new_component = TablebodyComponent(components)    
    self.components.append(new_component)
    return new_component
    

class Rowaction(Component):
  def __init__(self, label: str, url: str, classes: str = '', open_in_new_window: bool = True):    
    self.label = label
    self.url = url
    self.classes = classes
    self.open_in_new_window = open_in_new_window
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''TODO: Internal Component'''

class SectionComponent(Component):
  def __init__(self, id: str, name: str, level: int = 1):    
    self.id = id
    self.name = name
    self.level = level
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<span id=''' + self.id + '''></span>'''

class SelectoptionComponent(Component):
  def __init__(self, label: str, value: str):    
    self.label = label
    self.value = value
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<option value="''' + self.value + '''">''' + self.label + '''</option>'''

class SidebarComponent(Component):
  def __init__(self, components: list = None):    
    # https://stackoverflow.com/questions/4841782/python-constructor-and-default-value
    self.components = components or []
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<script>
    function smoothScrollTo(link) {
        console.log(link);
        var hashUrl = link.href;
        console.log(hashUrl);
        var hash = hashUrl.substring(hashUrl.indexOf("#") + 1);
        console.log(hash);
        var element = document.getElementById(hash);
        console.log(element);
        if (element) {
            element.scrollIntoView({behavior: "smooth", block: "start", inline: "nearest"})
        }
        return true;
    }
</script>
<aside style="min-width: 300px" class="hidden lg:block overflow-y-auto flex w-72 flex-col space-y-2 bg-gray-50 dark:bg-gray-800 p-2 h-screen sticky top-0">
    <div class="sticky top-0">
        ''' + '\n'.join(map(lambda x: x.to_html(), self.components)) + ''' 
    </div>
</aside>'''

  def add(self, component):
    self.components.append(component)
    return self

  def add_component(self, component):
    self.components.append(component)
    return self
  def add_sidebarcategory(self, title: str, components: list = None) -> SidebarcategoryComponent:
    new_component = SidebarcategoryComponent(title, components)    
    self.components.append(new_component)
    return new_component
    

class SidebarcategoryComponent(Component):
  def __init__(self, title: str, components: list = None):    
    self.title = title
    # https://stackoverflow.com/questions/4841782/python-constructor-and-default-value
    self.components = components or []
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<div class="mb-8">
    <h2 class="text-lg font-medium text-gray-500 dark:text-gray-400 tracking-wider uppercase mb-3">''' + self.title + '''</h2>
    <ul class="ml-5 list-none">
        ''' + '\n'.join(map(lambda x: x.to_html(), self.components)) + ''' 
    </ul>
</div>'''

  def add(self, component):
    self.components.append(component)
    return self

  def add_component(self, component):
    self.components.append(component)
    return self
  def add_sidebarlink(self, title: str, url: str) -> SidebarlinkComponent:
    new_component = SidebarlinkComponent(title, url)    
    self.components.append(new_component)
    return new_component
    

class SidebarlinkComponent(Component):
  def __init__(self, title: str, url: str):    
    self.title = title
    self.url = url
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<li><a href="''' + self.url + '''" onclick="event.preventDefault(); smoothScrollTo(this)" class="text-gray-900 dark:text-white hover:text-gray-800">''' + self.title + '''</a></li>'''

class TablebodyComponent(Component):
  def __init__(self, components: list = None):    
    # https://stackoverflow.com/questions/4841782/python-constructor-and-default-value
    self.components = components or []
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<tbody>
    ''' + '\n'.join(map(lambda x: x.to_html(), self.components)) + ''' 
</tbody>'''

  def add(self, component):
    self.components.append(component)
    return self

  def add_component(self, component):
    self.components.append(component)
    return self
  def add_tablerow(self, components: list = None) -> TablerowComponent:
    new_component = TablerowComponent(components)    
    self.components.append(new_component)
    return new_component
    

class TablecellComponent(Component):
  def __init__(self, value: str):    
    self.value = value
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<td class="px-6 py-4 whitespace-nowrap">
    ''' + self.value + '''
</td>'''

class TablecellheaderComponent(Component):
  def __init__(self, value: str):    
    self.value = value
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
    ''' + self.value + '''
</th>'''

class TablecolComponent(Component):
  def __init__(self, components: list = None):    
    # https://stackoverflow.com/questions/4841782/python-constructor-and-default-value
    self.components = components or []
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<td class="px-6 py-4 whitespace-nowrap">
    ''' + '\n'.join(map(lambda x: x.to_html(), self.components)) + ''' 
</td>'''

  def add(self, component):
    self.components.append(component)
    return self

  def add_component(self, component):
    self.components.append(component)
    return self
class TableheadComponent(Component):
  def __init__(self, components: list = None):    
    # https://stackoverflow.com/questions/4841782/python-constructor-and-default-value
    self.components = components or []
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<thead class="bg-gray-50 dark:bg-gray-800">
    <tr>
        ''' + '\n'.join(map(lambda x: x.to_html(), self.components)) + ''' 
    </tr>
</thead>'''

  def add(self, component):
    self.components.append(component)
    return self

  def add_component(self, component):
    self.components.append(component)
    return self
  def add_tablerow(self, components: list = None) -> TablerowComponent:
    new_component = TablerowComponent(components)    
    self.components.append(new_component)
    return new_component
    

  def add_tablecol(self, components: list = None) -> TablecolComponent:
    new_component = TablecolComponent(components)    
    self.components.append(new_component)
    return new_component
    

  def add_tablecell(self, value: str) -> TablecellComponent:
    new_component = TablecellComponent(value)    
    self.components.append(new_component)
    return new_component
    

  def add_tablecellheader(self, value: str) -> TablecellheaderComponent:
    new_component = TablecellheaderComponent(value)    
    self.components.append(new_component)
    return new_component
    

class TablerowComponent(Component):
  def __init__(self, components: list = None):    
    # https://stackoverflow.com/questions/4841782/python-constructor-and-default-value
    self.components = components or []
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<tr class="border-t border-gray-200 dark:border-gray-700">
    ''' + '\n'.join(map(lambda x: x.to_html(), self.components)) + ''' 
</tr>'''

  def add(self, component):
    self.components.append(component)
    return self

  def add_component(self, component):
    self.components.append(component)
    return self
  def add_tablecol(self, components: list = None) -> TablecolComponent:
    new_component = TablecolComponent(components)    
    self.components.append(new_component)
    return new_component
    

  def add_tablecell(self, value: str) -> TablecellComponent:
    new_component = TablecellComponent(value)    
    self.components.append(new_component)
    return new_component
    

  def add_tablecellheader(self, value: str) -> TablecellheaderComponent:
    new_component = TablecellheaderComponent(value)    
    self.components.append(new_component)
    return new_component
    

class TextComponent(Component):
  def __init__(self, value: str):    
    self.value = value
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<p class="mb-6 text-lg font-normal text-gray-500 lg:text-xl dark:text-gray-400">''' + self.value + '''</p>'''

class TextareaComponent(Component):
  def __init__(self, label: str = 'Your Message', name: str = 'message', placeholder: str = 'Leave a comment...'):    
    self.label = label
    self.name = name
    self.placeholder = placeholder
    

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def to_html(self):
    return '''<div class="mb-6">
    <label for="''' + self.name + '''" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">''' + self.label + '''</label>
    <textarea name="''' + self.name + '''" rows="4" class="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="''' + self.placeholder + '''"></textarea>
</div>'''


#
#
# Begin Manual Code
#
#
#
from urllib.parse import quote
import re
import json

def advanced_add_pandastable(self, df):
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
            html += '''<td class="px-6 py-4">''' + format_input(row[column]) + "</td>"
        html += "</tr>"
        i += 1

    html += "</tbody>"

    html += "</table>"

    html += "</div>"

    html += "</div>"

    self.components.append(HtmlComponent(html))
    return self


"""
A function that formats input into a human-readable string:
Input: An arbitrary type that could be string, integer, floating point, a numpy object, a pandas datetime, or something else
Output: String

Dates should be formatted using ISO-8601. Numbers below 10 should include 2 decimal places. Numbers between 10 and 100 should have 1 decimal place. Numbers between 100 and 1000 should have 0 decimal places. Numbers between 1000 and 1000000 should have 0 decimal places and be formatted with a comma for the thousands separator. Numbers between 1000000 and 1000000000 should be formatted as X.Y million. Numbers above 1000000000 should be formatted as X.Y billion
"""


def format_input(input):
    is_int = "int" in type(input).__name__
    is_float = "float" in type(input).__name__

    if isinstance(input, str):
        return input
    elif is_float or is_int:
        if input < 10:
            if is_float:
                return '{:.2f}'.format(input)
            else:
                return str(input)
        elif input < 100:
            if is_float:
                return '{:.1f}'.format(input)
            else:
                return str(input)
        elif input < 1000:
            return '{:.0f}'.format(input)
        elif input < 1000000:
            return '{:,.0f}'.format(input)
        elif input < 1000000000:
            return '{:.1f} million'.format(input / 1000000)
        else:
            return '{:.1f} billion'.format(input / 1000000000)
    elif callable(getattr(input, "isoformat", None)):
        iso = input.isoformat()

        if "T00:00:00" in iso:
            return iso[0:10]

        return iso
    else:
        return str(input)

def __format_python_object_for_json(t):
    if callable(getattr(t, "isoformat", None)):
        iso = t.isoformat()

        if "T00:00:00" in iso:
            return iso[0:10]

        return iso
    
    return t

def advanced_add_emgithub(self, url):
    quoted_url = quote(url)

    emgithub = '''
    <script src="https://emgithub.com/embed-v2.js?target=''' + quoted_url +  '''&style=vs2015&type=code&showBorder=on&showLineNumbers=on&showFileMeta=on&showFullPath=on&showCopy=on&fetchFromJsDelivr=on"></script>
    '''

    self.components.append(HtmlComponent(emgithub))

def __format_column_header(x: str) -> str:
    # Insert undersore between camel case
    x = re.sub(r'(?<=[a-z])(?=[A-Z])', '_', x)

    # Capitalize the beginning of each word
    x = x.title()

    # Replace underscores with spaces
    x = x.replace('_', ' ')

    return x

def __get_action_buttons_to_add(action_buttons):
    action_buttons_to_add = []

    for action_button in action_buttons:
        # If the label is not of the form "{key}", then add it to the list of action buttons to add
        if action_button.label[0] != '{' or action_button.label[-1] != '}' and '{' not in action_button.label[1:-1]:        
            action_buttons_to_add.append(action_button)

    return action_buttons_to_add

def __find_key_in_action_buttons(key: str, action_buttons):
    for action_button in action_buttons:
        if action_button.label == '{' + key + '}' :
            return action_button

    return None

def __replace_text_with_button(record: dict, action_buttons) -> dict:
    new_record = {}

    for key in record.keys():
        action_button = __find_key_in_action_buttons(key, action_buttons)

        value = __format_python_object_for_json(record[key])

        if action_button is not None:
            hydrated_label = action_button.label.format(**record)
            hydrated_url = action_button.url.format(**record)
            if action_button.open_in_new_window:
                new_record[key] = """<a href='""" + hydrated_url + """' target="_blank" class="px-3 py-2 text-xs font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">""" + hydrated_label + """</button>"""
            else:
                new_record[key] = """<a href='""" + hydrated_url + """' class="px-3 py-2 text-xs font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">""" + hydrated_label + """</button>"""
        else:
            new_record[key] = value
    
    action_buttons_html = ''

    action_buttons_to_add = __get_action_buttons_to_add(action_buttons)
    for button_to_add in action_buttons_to_add:
        hydrated_label = button_to_add.label.format(**record)
        hydrated_url = button_to_add.url.format(**record)

        if button_to_add.open_in_new_window:
            action_buttons_html += """<a href='""" + hydrated_url + """' target="_blank" class="px-3 py-2 text-xs font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">""" + hydrated_label + """</button>"""
        else:
            action_buttons_html += """<a href='""" + hydrated_url + """' class="px-3 py-2 text-xs font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">""" + hydrated_label + """</button>"""

    new_record['Actions'] = action_buttons_html

    return new_record

def advanced_add_datagrid(page, dataframe, action_buttons):
    cols = list(map(lambda x: {'headerName': __format_column_header(x), 'field': x} , dataframe.columns.to_list()))

    if len(__get_action_buttons_to_add(action_buttons)) > 0:
        cols.append({'headerName': 'Actions', 'field': 'Actions'})

    datagridHtml = '''
        <script>
        var columnDefsasdf = {columns};
        '''.format(columns = cols)

    records = list (map(lambda x: __replace_text_with_button(x, action_buttons=action_buttons), dataframe.to_dict(orient='records')))

    datagridHtml += '''
    columnDefsasdf.forEach( (x) => { x.cellRenderer = function(params) { return params.value ? params.value : '' } } )
    '''

    datagridHtml += '''
        var rowDataasdf = {records};
        '''.format(records = json.dumps( records ) )

    datagridHtml += '''
        var gridOptionsasdf = {
            columnDefs: columnDefsasdf,
            rowData: rowDataasdf,
            defaultColDef: {
                sortable: true,
                filter: true,
                resizable: true,
                floatingFilter: true,
                autoHeight: true,
                wrapText: true,
                autoSizePadding: 10,
                cellStyle: {
                    'white-space': 'normal'
                },
            },
            pagination: true
        };
        document.addEventListener('DOMContentLoaded', function() {
            var gridDivasdf = document.querySelector('#divid_aggrid_asdf');
            new agGrid.Grid(gridDivasdf, gridOptionsasdf);
        });

        function expand(e) {
            e.parentElement.children[1].style.height = 'calc( 100vh )';
            e.scrollIntoView();
        }
        </script>
        <div>
            <button onclick="expand(this)" class="mb-4 px-3 py-2 text-xs font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Expand</button>
            <div id="divid_aggrid_asdf" style="height: 500px; max-height: calc( 100vh - 60px ); width: calc( 100vw - 50px );" class="data-grid ag-theme-alpine-dark "></div>
        </div>
    '''

    page.components.append(HtmlComponent(datagridHtml))

