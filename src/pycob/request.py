import flask

class Request:
    def __init__(self, flask_request: flask.Request):
        self.flask_request = flask_request
    
    def get_query_parameter(self, key: str) -> str:
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