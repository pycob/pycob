class Builder:
  def __init__(self):
    self.html = []

  def _repr_html_(self):
      if len(self.html) == 0:
        return "Empty Builder. Use add_ methods to add components to render. See <a href='https://pycob.com' target='_blank'>documentation</a>"

      return """
      <link rel="stylesheet" src="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css">      
      """ + self.html[-1]

  def add_html(self, value: str):
    temp = f'''''' + value + ''''''
    self.html.append(temp)
    return self


  def add_text(self, value: str):
    temp = f'''<p>''' + value + '''</p>'''
    self.html.append(temp)
    return self


  def add_header(self, text: str, size: int):
    temp = f'''<p class="title-font sm:text-''' + size + '''xl text-xl font-medium text-gray-900 mb-3">''' + text + '''</p>'''
    self.html.append(temp)
    return self


  def add_alert(self, text: str, badge: str = '', color: str = 'indigo'):
    temp = f'''<div class="text-center py-4 lg:px-4">
<div class="p-2 bg-''' + color + '''-800 items-center text-''' + color + '''-100 leading-none lg:rounded-full flex lg:inline-flex" role="alert">
    <span class="flex rounded-full bg-''' + color + '''-500 uppercase px-2 py-1 text-xs font-bold mr-3">''' + badge + '''</span>
    <span class="font-semibold mr-2 text-left flex-auto">''' + text + '''</span>            
</div>
</div>'''
    self.html.append(temp)
    return self


  def add_hero(self, title: str, subtitle: str = '', image: str = '', color: str = 'indigo'):
    temp = f'''<section class="bg-white">
    <div class="grid max-w-screen-xl px-4 py-8 mx-auto lg:gap-8 xl:gap-0 lg:py-16 lg:grid-cols-12">
        <div class="mr-auto place-self-center lg:col-span-7">
            <h1 class="max-w-2xl mb-4 text-4xl font-extrabold tracking-tight leading-none md:text-5xl xl:text-6xl">''' + title + '''</h1>
            <p class="max-w-2xl mb-6 font-light text-gray-500 lg:mb-8 md:text-lg lg:text-xl">''' + subtitle + '''</p>
            <a href="#" class="inline-flex items-center justify-center px-5 py-3 mr-3 text-base font-medium text-center text-white rounded-lg bg-''' + color + '''-700 hover:bg-''' + color + '''-800 focus:ring-4 focus:ring-''' + color + '''-300">
                Button 1                        
            </a>
            <a href="#" class="inline-flex items-center justify-center px-5 py-3 text-base font-medium text-center text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-100 focus:ring-4 focus:ring-gray-100">
                Button 2
            </a> 
        </div>
        <div class="hidden lg:mt-0 lg:col-span-5 lg:flex">
            <img src="''' + image + '''" >
        </div>                
    </div>
</section>'''
    self.html.append(temp)
    return self


  def add_code(self, value: str, header: str = ''):
    temp = f'''<div class="mx-auto my-10 max-w-3xl">
    <div class="flex h-11 w-full items-center justify-start space-x-1.5 rounded-t-lg bg-gray-900 px-3">
        <span class="h-3 w-3 rounded-full bg-red-400"></span>
        <span class="h-3 w-3 rounded-full bg-yellow-400"></span>
        <span class="h-3 w-3 rounded-full bg-green-400"></span>
        <code class="pl-5 text-lime-500">''' + header + '''</code>
    </div>
    <div class="w-full border-t-0 bg-gray-700 pb-5">
        <code class="text-gray-500">&gt&gt&gt</code>
        <code class="text-white">''' + value + '''</code>
    </div>
</div>'''
    self.html.append(temp)
    return self


  def add_divider(self, ):
    temp = f'''<hr class="my-5 border-gray-300 w-full">'''
    self.html.append(temp)
    return self


  def add_section(self, id: str, name: str, level: int = 1, icon: str = ''):
    temp = f'''<span id=''' + id + '''></span>'''
    self.html.append(temp)
    return self
