import requests
from models import *
import requests
import json


#class function to pull in json event data from eventbrite API
#output will be a list of events

class EventbriteAPI:

    def __init__(self, url):
        self.url = url

    def data_pull(self):
        r = requests.get(self.url)
        concert_data_dictionary = r.json()
        concert_list = concert_data_dictionary['events']
        return concert_list

#class to define parsing functions
class EventbriteEventsParser:

    def __init__(self, individual_concert_data):
        self.individual_concert_data = individual_concert_data


    #retrieves concert name
    def concert_name(self):
        return self.individual_concert_data['name']['text']

    #retrieves concert Date
    def concert_date(self):
        return self.individual_concert_data['start']['local'][:10]

    #retrieves minimum price
    def concert_minimum_price(self):
        try:
            return float(self.individual_concert_data['ticket_availability']['minimum_ticket_price']['major_value'])
        except:
            pass

    #retrieves maximumum_price
    def concert_maximum_price(self):
        try:
            return float(self.individual_concert_data['ticket_availability']['maximum_ticket_price']['major_value'])
        except:
            pass

    #retrieves concert URL
    def concert_url(self):
        return self.individual_concert_data['url']

    #retrieve concert artist/artists
    def concert_artist(self):
        try:
            pass
        except:
            pass

    #retrieves genre
    def concert_genre(self):
        try:
            return self.individual_concert_data['subcategory']['name']
        except:
            pass

    #retrieves venue_name
    def concert_venue_name(self):
        return self.individual_concert_data['venue']['name']

    #retrieves venue city
    def concert_venue_city(self):
        return self.individual_concert_data['venue']['address']['city']

    #retrieves concert venue address
    def concert_venue_address(self):
        try:
            return self.individual_concert_data['venue']['address']['address_1']
        except:
            pass

    #retrieves concert latitude
    def concert_venue_latitude(self):
        return self.individual_concert_data['venue']['latitude']

    #retrieves concert longitude
    def concert_venue_longitude(self):
        return self.individual_concert_data['venue']['longitude']
