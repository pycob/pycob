# PyCob 

![PyCob Logo on Hexagon](https://cdn.pycob.com/pycob_with_text_256.png)

## Create web apps using just Python

### Install PyCob
```bash
pip install pycob
```


```python
import pycob as pc

app = pc.App('Test App')

def test_page(server_request: pc.Request) -> pc.Page:
    name = server_request.get_query_parameter('name')
    page = pc.Page('Test Page')
    page.add_header('Test Header', "2")
    page.add_text('Test Text')
    page.add_alert('Test Alert')
    page.add_hero('Hello ' + name, 'Test Subtitle', 'https://source.unsplash.com/random/800x600')
    
    form = pc.FormComponent(action="/")
    form.add_formtext('Name', 'name', 'Enter your name')
    form.add_formsubmit('Submit')

    page.add_component(form)

    return page

app.add_page('/', test_page)

app.run()
```

[Quickstart Template Repo](https://github.com/pycob/quickstart)
