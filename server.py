from flask import Flask, redirect, url_for, session, request, render_template, jsonify, flash
# from flask_oauthlib.client import OAuth, OAuthException
import os
# from flask_debugtoolbar import DebugToolbarExtension
import requests
import json

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'


# https://api.seatgeek.com/2/events?client_id=<CLIENT_ID>&clien‌​t_secret=<CLIENT_SECRET>&per_page=25&page‌​=3.

SEATGEEK_ID = os.environ["SEATGEEK_CLIENT_ID"]
SEATGEEK_SECRET = os.environ["SEATGEEK_CLIENT_SECRET"]
API_ENDPOINT = "https://api.seatgeek.com/2/events?performers.slug=beyonce&client_id={}".format(SEATGEEK_ID)

def get_seat_geek():
    """Tests out seatgeek's api"""

    params = {'client_id': SEATGEEK_ID}

    # my_response = requests.get("https://api.seatgeek.com/2/events?beyonce&client_id={}&clien‌​t_secret={}".format(SEATGEEK_ID, SEATGEEK_SECRET))

    # r = requests.get(url = API_ENDPOINT, params=params)

    r = requests.get(url=API_ENDPOINT)
    data = json.loads(r.text)
    return data

data = get_seat_geek()

def process_seat_geek(data):
    """parses dict from seat geek request"""

    relevent_shows = {}
    events = data['events']
    for event in events:
        relevent_shows[event['id']] = {'datetime_local': event['datetime_local'],
                                          'venue_name': event['venue']['name'],
                                          'latlong': event['venue']['location'],
                                          'city': event['venue']['city'],
                                          'state': event['venue']['state'],
                                          'url': event['url'],
                                          'title': event['title'],
                                          'avg_ticket_price': event['stats']['average_price'],
                                          'short_title': event['short_title'],
                                          }
        artists = []
        for item in event['performers']:
            artists.append({'name':item['name'],
                            'image': item['image']})
        relevent_shows[event['id']]['performers'] = artists

    return relevent_shows

# wow = process_seat_geek(data)

@app.route('/')
def display_homepage():
    """homepage"""
    wow = process_seat_geek(data)
    return render_template("homepage.html", relevent_shows=wow)




#TODO
# search paramaters - can i input a location to search around??
# batch request?? or search individually?
# can give venue parameter using following syntax
# events?venue.state=NY
# venue.city, venue.state


if __name__ == '__main__':
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    app.run(host='0.0.0.0')
