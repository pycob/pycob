from urllib.parse import quote
import re

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
    print("Input Type = ", type(input))
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
    

def advanced_add_datagrid(page, dataframe, action_buttons):
    cols = list(map(lambda x: {'headerName': __format_column_header(x), 'field': x} , dataframe.columns.to_list()))

    datagridHtml = '''
        <script>
        var columnDefsasdf = {columns};
        '''.format(columns = cols)

    datagridHtml += '''
        var rowDataasdf = {records};
        '''.format(records = dataframe.to_json(orient='records'))

    print(dataframe.to_json(orient='records'))

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

