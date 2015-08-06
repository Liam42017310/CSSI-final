#All of the imports we need in order to run data store and parse API info

import webapp2
import jinja2
import os
import json
import urllib
import logging
# from gdata.youtube.service.YouTubeService import gdata.youtube
# from gdata.youtube.service.YouTubeService import gdata.youtube.service
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from google.appengine.api import users

#loads the jinja environment
#API key: AI39si7gj4SXdD_fVcyovbJ_L7RxCLhRnsHUqVF-8Q_yhi7GLUbNXlJHtFfWEfo0MYQfkc_osqx75yiCh3RYkJfUyNyJe1NKxg
# yt_service = gdata.youtube.service.YouTubeService()
# Turn on HTTPS/SSL access.
# Note: SSL is not available at this time for uploads.
# yt_service.ssl = True
# yt_service.developer_key = 'AI39si7gj4SXdD_fVcyovbJ_L7RxCLhRnsHUqVF-8Q_yhi7GLUbNXlJHtFfWEfo0MYQfkc_osqx75yiCh3RYkJfUyNyJe1NKxg'
jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

#initializes the classes that we need to store data

class Like(ndb.Model):
    title = ndb.StringProperty(required = True)
    artist = ndb.StringProperty(required = True)
    album = ndb.StringProperty(required = True)

class Event(ndb.Model):
    concert_name = ndb.StringProperty(required = True)
    date = ndb.StringProperty(required = True)
    location = ndb.StringProperty(required = True)

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

class OtherDefaultHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/default.html')
        self.response.out.write(template.render())

class AboutUsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/aboutus.html')
        self.response.out.write(template.render())


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
                if 'collectionName' in parsed_url_dictionary['results'][index].keys():
                    search_album = parsed_url_dictionary['results'][index]['collectionName']
                    template_albums.update({'key' + str(index) : search_album})
                else:
                    template_albums.update({'key' + str(index) : ''})

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


class LikeHandler(webapp2.RequestHandler):
    def post(self):
        encoded_request = self.request.get('like')
        decoded_request = json.loads(encoded_request)
        current_song_title = decoded_request['title']
        current_artist_title = decoded_request['artist']
        current_album_title = decoded_request['album']


class EventsHandler(webapp2.RequestHandler):
    def post(self):
        template_concert_names = {}
        template_dates = {}
        template_locations = {}
        search_results = []
        # user_search = self.request.get('search')
        user_search = "beyonce"
        # http://api.bandsintown.com/artists/Skrillex/events.json?api_version=2.0&app_id=YOUR_APP_ID
        if user_search == '':
            template = jinja_environment.get_template('templates/events_error.html')
            self.response.write(template.render())
        else:
            template = jinja_environment.get_template('templates/events.html')
            # term = {'term' : user_search}
            search_term = user_search

            base_url = 'http://api.bandsintown.com/artists/'
            search_url = base_url + search_term + "/events.json?api_version=2.0&app_id=buildmymusic"
            url_content = urlfetch.fetch(search_url).content
            parsed_url_dictionary = json.loads(url_content)
            # template_vars = {"dictionary": parsed_url_dictionary}

            for index, key in enumerate(parsed_url_dictionary):
                search_title = parsed_url_dictionary[index]['title']
                template_concert_names.update({'key' + str(index) : search_title})

            for index, key in enumerate(parsed_url_dictionary):
                search_date = parsed_url_dictionary[index]['formatted_datetime']
                template_dates.update({'key' + str(index) : search_date})

            for index, key in enumerate(parsed_url_dictionary):
                search_location = parsed_url_dictionary[index]['formatted_location']
                template_locations.update({'key' + str(index) : search_location})

            for key, value in template_concert_names.iteritems():
                concert_name = value
                date = template_dates[key]
                location = template_locations[key]
                current_search_result = Event(concert_name = concert_name, date = date, location = location)
                search_results.append(current_search_result)
            passed_vars = {'concertnames': template_concert_names,
                           'dates': template_dates,
                           'locations': template_locations,
                           'searches': search_results}

            self.response.out.write(template.render(passed_vars))

# def SearchAndPrintVideosByKeywords(list_of_search_terms):
#     def get(self):
#       template = jinja_environment.get_template('templates/default.html')
#       yt_service = gdata.youtube.service.YouTubeService()
#       query = gdata.youtube.service.YouTubeVideoQuery()
#       query.orderby = 'viewCount'
#       query.racy = 'include'
#       for search_term in list_of_search_terms:
#         new_term = search_term.lower()
#         query.categories.append('/%s' % new_term)
#       feed = yt_service.YouTubeQuery(query)
#       PrintVideoFeed(feed)
#       passed_vars = {'test': feed}
#       self.response.out.write(template.render(passed_vars))



app = webapp2.WSGIApplication([

    ('/', WelcomeHandler),
    ('/default', DefaultHandler),
    ('/search', SearchHandler),
    ('/profile', ProfileHandler),
    ('/aboutus', AboutUsHandler),
    ('/likes', LikeHandler),
    ('/events', EventsHandler),
    ('/otherdefault', OtherDefaultHandler)

], debug=True)
