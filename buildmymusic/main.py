
import webapp2
import jinja2
import os
import json
from google.appengine.api import urlfetch
from google.appengine.ext import ndb

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
