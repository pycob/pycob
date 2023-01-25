# PyCob 

![PyCob Logo on Hexagon](https://cdn.pycob.com/android-chrome-192x192.png)

## Create web apps using just Python

### Install PyCob
```bash
pip install pycob
```

### Use PyCob
```python
import pycob as cob

app = cob.App('Test App')

def test_page(server_request: cob.Request) -> cob.Page:
    name = server_request.get_query_parameter('name')
    page = cob.Page('Test Page')
    page.add_header('Test Header', "2")
    page.add_text('Test Text')
    page.add_alert('Test Alert')
    page.add_hero('Hello ' + name, 'Test Subtitle', 'https://source.unsplash.com/random/800x600')
    
    form = cob.FormComponent(action="/")
    form.add_formtext('Name', 'name', 'Enter your name')
    form.add_formsubmit('Submit')

    page.add_component(form)

    return page

app.add_page('/', test_page)

app.run()
```

### Quickstart
[Quickstart Template Repo](https://github.com/pycob/quickstart)

### Learn More
[PyCob](https://www.pycob.com)
