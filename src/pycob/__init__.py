from .app import *
from .request import *
from .component_interface import *
from .all_components import *

def serve(anything):
    app = App("PyCob App")

    page = Page("Demo Page", auto_footer=False)

    if isinstance(anything, str):
        page.add_header(anything, size=9)

    app.add_page("/", "Home", lambda x: page)

    return app.run(force_dev_mode=True)