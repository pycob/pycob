# PyCob 
[![PyPI version](https://badge.fury.io/py/pycob.svg)](https://badge.fury.io/py/pycob)

![Screenshot of PyCob Quickstart App](https://cdn.pycob.com/quickstart_screenshot.png)

We created PyCob to let you quickly create functional apps using only python. Read more about the project goals here


## Create web apps using just Python
The app from the above screenshot can be started/created/is possible with just the following steps
### Install PyCob
```bash

git clone https://github.com/pycob/pycob
cd pycob
# activate your venv however appropriate
pip install pycob
python src/example.py
```

### Code for src/example.py
```python
import pycob as cob
import pandas as pd

# Create a PyCob app
app = cob.App('Sample App')

# Define a page
def sample_page(server_request: cob.Request) -> cob.Page:
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

# Register page functions with the app
app.register_function(sample_page)

# Run the server
server = app.run()
```
## Whos is PyCob for?

PyCob is perfect for quant and analytical developers who want to expose data analysis.  PyCob's sweetspot sits between jupyter notebooks and apps that are supported by a full frontend dev team.  


### Scaling an app
#### Jupyter notebook on your machine
build whatever you want, rearrange cells, try new stuff.  Dont expect anyone else to run or understand your code
#### Jupyter notebooks shared with other data scientists
Put your notebook into a git repo, add a `conda.yml` or `requirements.txt` get feedback on the algorithm
This works for 1-4 technically proficient data scientists and engineers

To scale beyond this step you're going to need to do something different
#### Stick with Jupyter notebooks
If you want to build an app in the jupyter notebook environment, you are going to need to buy into some infrastructure.  At this point you will want a jupyter hosting system like Domino ($100k/year) SaturnCloud ($10-20k/year) or hex (??? $20k+ / year).  This will work for 5-50 users
#### PyCob
Integrate your app into PyCob, and setup a fairly standard python hosting (please expand)

works for 5-100 non-technical users

Full scale
#### Hire a frontend dev team
Build a traditional python server and react frontend.  This is the most flexible deployment mode, and very complex.  Until you train frontend dev on the needs of quants and quant customers there will be a steep learning curve.  You will have a translation layer in between the subject matter experts and the builder of the UI.

### Learn More
[PyCob](https://www.pycob.com)
