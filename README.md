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
import pandas as pd

# Create a PyCob app
app = cob.App('Sample App')

# Define the page
def test_page(server_request: cob.Request) -> cob.Page:
    name = server_request.get_query_parameter('name')
    
    page = cob.Page('Sample Page')

    if name != "":
        page.add_header("Hello, " + name)
    else:
        page.add_header('Sample Header')

    page.add_text('Sample Text')
    page.add_alert('Sample Alert', "Sample Badge")
    
    card = page.add_card()
    card.add_header("Sample Card", size=3)

    form = card.add_form(action="/")
    form.add_formtext('Name', 'name', 'Enter your name')
    form.add_formsubmit('Submit')

    data = {
        "data_int": [420, 380, 390],
        "data_float": [50.2, 39.6, 100.3],
        "large_numbers": [123123.123, 12312512.123, 113453252334.123],
    }

    df = pd.DataFrame(data)

    page.add_pandastable(df)

    return page

# Give the page a route
app.add_page('/', "Home", test_page)

# Run the server
app.run()
```

### Quickstart
[Quickstart Template Repo](https://github.com/pycob/quickstart)

### Learn More
[PyCob](https://www.pycob.com)
