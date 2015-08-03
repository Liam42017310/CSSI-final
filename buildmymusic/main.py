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

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

class SearchHandler(webapp2.RequestHandler):
    def get(self):
        # template = jinja_environment.get_template('templates/search.html')
        search_term = 'Kid+Cudi'
        base_url = 'https://itunes.apple.com/search?media=music&'
        search_query = 'term=' + search_term
        search_url = base_url + search_query
        url_content = urlfetch.fetch(search_url).content
        parsed_url_dictionary = json.loads(url_content)
        for index, key in enumerate(parsed_url_dictionary['results']):
            self.response.write(parsed_url_dictionary['results'][index]['trackName'])




#opens and reads the JSON at the itunes URL urlfetch.fetch(itunes.com/?+ user_artist)
#song_data=urlfetch.fetch(query).open()
#drill down to song name
# song_data[0]["name"][name]
#
# our_song_db=Like(title=song_data.title, )



app = webapp2.WSGIApplication([
    ('/', SearchHandler)
], debug=True)
