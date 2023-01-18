import flask

class Request:
    def __init__(self, flask_request: flask.Request):
        self.flask_request = flask_request
    
    def get_query_parameter(self, key: str) -> str:
        unsanitized = self.flask_request.args.get(key, '')
        return unsanitized.replace('<', '&lt;').replace('>', '&gt;').replace("'", "''").replace(";", "")
