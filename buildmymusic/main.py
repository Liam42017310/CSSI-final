#All of the imports we need in order to run data store and parse API info

import webapp2
import jinja2
import os
import json
import urllib
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from google.appengine.api import users

#loads the jinja environment

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

#initializes the classes that we need to store data

class Like(ndb.Model):
    title = ndb.StringProperty(required = True)
    artist = ndb.StringProperty(required = True)
    album = ndb.StringProperty(required = True)

class User(ndb.Model):
    user = ndb.StringProperty(required = True)
    uname = ndb.StringProperty(required = True)
    likes = ndb.KeyProperty(Like, repeated = True)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/welcome.html')
        self.response.out.write(template.render())
    def post(self):
        user = users.get_current_user()
        if user:
            current_user = User(user = user.user_id(), uname = user.nickname())
            existing_user = User.query().filter(User.user == current_user.user).fetch()
            if not existing_user:
                current_user.put()
            template = jinja_environment.get_template('templates/default.html')
            self.response.out.write(template.render())
        else:
            self.redirect(users.create_login_url(self.request.uri))

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/profile.html')
        self.response.out.write(template.render())

class DefaultHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/default.html')


class SearchHandler(webapp2.RequestHandler):
    def post(self):
        template_titles = {}
        template_artists = {}
        template_albums = {}
        search_results = []
        user_search = self.request.get('search')
        if user_search == '':
            template = jinja_environment.get_template('templates/search_error.html')
            self.response.write(template.render())
        else:
            template = jinja_environment.get_template('templates/search.html')
            term = {'term' : user_search}
            search_term = urllib.urlencode(term)
            base_url = 'https://itunes.apple.com/search?media=music&'
            search_url = base_url + search_term
            url_content = urlfetch.fetch(search_url).content
            parsed_url_dictionary = json.loads(url_content)

            for index, key in enumerate(parsed_url_dictionary['results']):
                search_name = parsed_url_dictionary['results'][index]['trackName']
                template_titles.update({'key' + str(index) : search_name})

            for index, key in enumerate(parsed_url_dictionary['results']):
                search_artist = parsed_url_dictionary['results'][index]['artistName']
                template_artists.update({'key' + str(index) : search_artist})

            for index, key in enumerate(parsed_url_dictionary['results']):
                search_album = parsed_url_dictionary['results'][index]['collectionName']
                template_albums.update({'key' + str(index) : search_album})

            for key, value in template_titles.iteritems():
                title = value
                artist = template_artists[key]
                album = template_albums[key]
                current_search_result = Like(title = title, artist = artist, album = album)
                search_results.append(current_search_result)
            passed_vars = {'songs': template_titles,
                           'artists': template_artists,
                           'albums': template_albums,
                           'searches': search_results}
            self.response.out.write(template.render(passed_vars))



app = webapp2.WSGIApplication([

    ('/', WelcomeHandler),
    ('/default', DefaultHandler),
    ('/search', SearchHandler),
    ('/profile', ProfileHandler)
], debug=True)
