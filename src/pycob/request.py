import flask
from typing import Union

class Request:
    def __init__(self, flask_request: flask.Request, app):
        self.flask_request = flask_request
        self.app = app
    
    def get_query_parameter(self, key: str) -> str:
        """Deprecated. Use params() instead."""
        print("WARNING: get_query_parameter() is deprecated. Use params() instead.")
        return self.params(key)

    def store_dict(self, table_id: str, object_id: str, value: dict):
        return self.app.store_dict(table_id, object_id, value)
    
    def retrieve_dict(self, table_id: str, object_id: str) -> dict:
        return self.app.retrieve_dict(table_id, object_id)
    
    def query_dict(self, table_id: str, field_name: str, field_value) -> list:
        return self.app.query_dict(table_id, field_name, field_value)

    def list_object_ids(self, table_id: str) -> list:
        return self.app.list_object_ids(table_id)

    def params(self, key: str = "") -> Union[str, dict]:
        """Returns the value of the query parameter with the given key. If no key is given, returns a dictionary of all query parameters."""
        if key == "":
            d = self.flask_request.args.to_dict()
            # print("d = ", d)

            if d:
                return {k: _sanitize(v) for k, v in d.items()}
            
            d = self.flask_request.form.to_dict()
            # print("d = ", d)

            if d:
                return {k: _sanitize(v) for k, v in d.items()}
            
            d = self.flask_request.values.to_dict()
            # print("d = ", d)

            if d:
                return {k: _sanitize(v) for k, v in d.items()}

        unsanitized = self.flask_request.args.get(key, '')

        if unsanitized is None or unsanitized == '':
            unsanitized = self.flask_request.form.get(key, '')

        if unsanitized is None or unsanitized == '':
            unsanitized = self.flask_request.values.get(key, '')

        # if unsanitized is None or unsanitized == '':
        #     unsanitized = self.flask_request.json.__getattribute__(key)

        return unsanitized.replace('<', '&lt;').replace('>', '&gt;') #.replace("'", "''").replace(";", "")

    def get_username(self) -> str:
        return flask.session.get('username')
    
def _sanitize(unsanitized: str) -> str:
    return unsanitized.replace('<', '&lt;').replace('>', '&gt;')
