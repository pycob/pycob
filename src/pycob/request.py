import flask

class Request:
    def __init__(self, flask_request: flask.Request):
        self.flask_request = flask_request