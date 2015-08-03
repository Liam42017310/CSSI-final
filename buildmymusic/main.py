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


<<<<<<< HEAD
class SearchHandler(webapp2.RequestHandler):
    def get(self):
        # template = jinja_environment.get_template('templates/search.html')
        template_vars = {}
        search_term = 'Kid+Cudi'
        base_url = 'https://itunes.apple.com/search?media=music&'
        search_query = 'term=' + search_term
        search_url = base_url + search_query
        url_content = urlfetch.fetch(search_url).content
        parsed_url_dictionary = json.loads(url_content)
        for index, key in enumerate(parsed_url_dictionary['results']):
            search_name = parsed_url_dictionary['results'][index]['trackName']
            template_vars.update({'key' + str(index) : search_name})
        self.response.write(template_vars)
=======

>>>>>>> f9b8a2edea27d6346b884b55c139b7fc29f1266b


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/search', SearchHandler)
], debug=True)
