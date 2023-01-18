# Inspired by https://stackoverflow.com/a/40466535/3179416
from flask import Flask, Response
import flask
from .request import Request

class Handler(object):
    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        print("Flask Request = ", flask.request)
        print("Query Parameters = ", flask.request.args)
        print("Argument Length = ", len(args))
        for arg in args:
            print("Argument = ", arg)
        
        page = self.action(Request(flask.request))

        print("Accept mimetypes = ", flask.request.accept_mimetypes)
        print("Accept application/json = ", flask.request.accept_mimetypes['application/json'])
        print("Accept text/html = ", flask.request.accept_mimetypes['text/html'])
        
        if flask.request.accept_mimetypes['text/html']:
            return page._to_html()

        if flask.request.accept_mimetypes['application/json']:
            json_response = page._to_json()
            print(json_response)
            return json_response, '200 OK', {'Content-Type': 'application/json'}

        return page._to_html()