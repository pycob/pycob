class Builder:
  def __init__(self):
    self.html = []

  def add_header(self, text):
    self.html.append("<h1>" + text + "</h1>")
    return self

  def _repr_html_(self):
      if len(self.html) == 0:
        return "Empty Builder. Use add_ methods to add components to render. See <a href='https://pycob.com' target='_blank'>documentation</a>"

      return """
      <link rel="stylesheet" src="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css">      
      """ + self.html[-1]
