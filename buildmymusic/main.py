#All of the imports we need in order to run data store and parse API info

import webapp2
import jinja2
import os
import json
import urllib
import logging
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

class Event(ndb.Model):
    concert_name = ndb.StringProperty(required = True)
    date = ndb.StringProperty(required = True)
    location = ndb.StringProperty(required = True)

class User(ndb.Model):
    user = ndb.StringProperty(required = True)
    uname = ndb.StringProperty(required = True)
    likes = ndb.KeyProperty(Like, repeated = True)

class LogoutHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        self.redirect(users.create_logout_url(self.request.uri))

class ReferenceHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/references.html')
        self.response.out.write(template.render())

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/welcome.html')
        self.response.out.write(template.render())

    def post(self):
        user = users.get_current_user()
        if user:
            current_user = User(user = user.user_id(), uname = user.nickname(), likes = [])
            existing_user = User.query().filter(User.user == current_user.user).fetch()
            if not existing_user:
                current_user.put()
            template = jinja_environment.get_template('templates/default.html')
            self.response.out.write(template.render())
        else:
            self.redirect(users.create_login_url(self.request.uri))

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        nickname = user.nickname()
        sent_likes = []
        user_id = users.get_current_user().user_id()
        users_list = User.query().filter(User.user == user_id).fetch()
        if not users_list:
            logging.error("Error: user is not present")
            return
        user = users_list[0]
        user_likes = user.likes
        logging.info(user_likes)
        for like in user_likes:
            like_key = ndb.Key(Like, int(like.id()))
            current_like = like_key.get()
            current_song = current_like.title
            current_artist = current_like.artist
            current_album = current_like.album
            #like_object = Like(title = current_song, artist = current_artist, album = current_album)
            sent_likes.append({
                'title' : current_song,
                'artist': current_artist,
                'album' : current_album,
            })
        logging.info(sent_likes);
        template = jinja_environment.get_template('templates/profile.html')
        template_vars = {'likes': sent_likes, 'nickname': nickname}
        self.response.out.write(template.render(template_vars))

class DefaultHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/default.html')
        sent_likes = []
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            user_id = user.user_id()
            users_list = User.query().filter(User.user == user_id).fetch()
            if not users_list:
                logging.error("Error: user is not present")
                return
            sample_artists = ['Imagine Dragons', 'Eminem', 'Led Zepplin', 'Katy Perry', 'Cold War Kids']
            for i in range(5):
                term = {'term' : sample_artists[i]}
                search_term = urllib.urlencode(term)
                base_url = 'https://itunes.apple.com/search?media=music&'
                search_url = base_url + search_term
                url_content = urlfetch.fetch(search_url).content
                parsed_url_dictionary = json.loads(url_content)
                for i in range(5):
                    search_name = parsed_url_dictionary['results'][i]['trackName']
                    search_artist = parsed_url_dictionary['results'][i]['artistName']
                    search_album = parsed_url_dictionary['results'][i]['collectionName']
                    current_suggestion = Like(title = search_name, artist = search_artist, album = search_album)
                    sent_likes.append(current_suggestion)
            template_vars = {'suggestions': sent_likes}
            self.response.out.write(template.render(template_vars))
    def post(self):
        template = jinja_environment.get_template('templates/default.html')
        sent_likes = []
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            user_id = user.user_id()
            users_list = User.query().filter(User.user == user_id).fetch()
            if not users_list:
                logging.error("Error: user is not present")
                return
            sample_artists = ['Imagine Dragons', 'Eminem', 'Led Zepplin', 'Katy Perry', 'Cold War Kids']
            for i in range(5):
                term = {'term' : sample_artists[i]}
                search_term = urllib.urlencode(term)
                base_url = 'https://itunes.apple.com/search?media=music&'
                search_url = base_url + search_term
                url_content = urlfetch.fetch(search_url).content
                parsed_url_dictionary = json.loads(url_content)
                for i in range(5):
                    search_name = parsed_url_dictionary['results'][i]['trackName']
                    search_artist = parsed_url_dictionary['results'][i]['artistName']
                    search_album = parsed_url_dictionary['results'][i]['collectionName']
                    current_suggestion = Like(title = search_name, artist = search_artist, album = search_album)
                    sent_likes.append(current_suggestion)
            template_vars = {'suggestions': sent_likes}
            self.response.out.write(template.render(template_vars))

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
        logging.info("Received like: " + current_song_title + " + " + current_artist_title + " + " + current_album_title)
        user_id = users.get_current_user().user_id()
        like = Like.query().filter(Like.title == current_song_title and
                                   Like.artist == current_artist_title and
                                   Like.album == current_album_title).fetch()
        users_list = User.query().filter(User.user == user_id).fetch()
        if not users_list:
            logging.error("Error: user is not present")
            return
        if not like:
            clicked_like = Like(title = current_song_title, artist = current_artist_title, album = current_album_title)
            clicked_like.put()
            like.append(clicked_like)
        user = users_list[0]
        if like[0] not in user.likes:
            user.likes.append(like[0].key)
            user.put()

class LikesHandler(webapp2.RequestHandler):
    def post(self):
        sent_likes = []
        user_id = users.get_current_user().user_id()
        users_list = User.query().filter(User.user == user_id).fetch()
        if not users_list:
            logging.error("Error: user is not present")
            return
        user = users_list[0]
        user_likes = user.likes
        logging.info(user_likes)
        for like in user_likes:
            like_key = ndb.Key(Like, int(like.id()))
            current_like = like_key.get()
            current_song = current_like.title
            current_artist = current_like.artist
            current_album = current_like.album
            #like_object = Like(title = current_song, artist = current_artist, album = current_album)
            sent_likes.append({
                'title' : current_song,
                'artist': current_artist,
                'album' : current_album,
            })
        logging.info(sent_likes);
        template = jinja_environment.get_template('templates/likes.html')
        template_vars = {'likes': sent_likes}
        self.response.out.write(template.render(template_vars))

class EventsHandler(webapp2.RequestHandler):
    def post(self):
        sent_likes = []
        user_id = users.get_current_user().user_id()
        users_list = User.query().filter(User.user == user_id).fetch()
        if not users_list:
            logging.error("Error: user is not present")
            return
        user = users_list[0]
        user_likes = user.likes
        logging.info(user_likes)
        if user_likes == []:
            template = jinja_environment.get_template('templates/event_error.html')
            self.response.out.write(template.render())
        template_concert_names = {}
        template_dates = {}
        template_locations = {}
        search_results = []
        for like in user_likes:
            like_key = ndb.Key(Like, int(like.id()))
            current_like = like_key.get()
            current_song = current_like.title
            current_artist = current_like.artist
            current_album = current_like.album
            like_object = Like(title = current_song, artist = current_artist, album = current_album)
            search = like_object.artist
            logging.info(sent_likes)
            user_search1 = search.replace(",", "%20")
            user_search2 = user_search1.replace("&", "%20")
            user_search = user_search2.replace(" ", "%20")

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
        template = jinja_environment.get_template('templates/events.html')
        self.response.out.write(template.render(passed_vars))

app = webapp2.WSGIApplication([

    ('/', WelcomeHandler),
    ('/default', DefaultHandler),
    ('/search', SearchHandler),
    ('/profile', ProfileHandler),
    ('/aboutus', AboutUsHandler),
    ('/like', LikeHandler),
    ('/likes', LikesHandler),
    ('/events', EventsHandler),
    ('/references', ReferenceHandler)

], debug=True)
