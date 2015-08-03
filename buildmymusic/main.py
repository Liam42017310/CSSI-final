#All of the imports we need in order to run data store and parse API info

import webapp2
import jinja2
import os
import json
from google.appengine.api import urlfetch
from google.appengine.ext import ndb

#loads the jinja environment

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

#initializes the classes that we need to store data

class Like(ndb.Model):
    title = ndb.StringProperty(required = True)
    artist = ndb.StringProperty(required = True)
    album = ndb.StringProperty(required = True)

class User(ndb.Model):
    email = ndb.StringProperty(required = True)
    password = ndb.StringProperty(required = True)
    uname = ndb.StringProperty(required = True)
    likes = ndb.KeyProperty(Like, repeated = True)





app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
