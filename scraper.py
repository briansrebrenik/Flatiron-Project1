import requests
from models import *
import requests
import json


#ConcertBuilder class will use output from ticketmasterapi function
#and parsing functions from EventsParser class to output
#sqlalchemy objects

class ConcertBuilder:
    def __init__(self, url):
        self.url = url

    def run(self):
        all_concerts = []
        tm = TicketMasterAPI(self.url)
        for i in tm.data_pull():
            parser = EventsParser(i)
            concert = Concert(name=parser.concert_name(),
            date=parser.concert_date(), minimum_price=parser.concert_minimum_price(),
            maximumum_price=parser.concert_maximum_price(), url=parser.concert_url(),
            artists=Artist(name=parser.concert_artist()),
            genres=Genre(name=parser.concert_genre()),
            venues=Venue(name=parser.concert_venue_name(), city=parser.concert_venue_city(),
            address=parser.concert_venue_address(), latitude=parser.concert_venue_latitude(),
            longitude=parser.concert_venue_longitude()))
            all_concerts.append(concert)
        return all_concerts



#class function to pull in json event data from ticketmaster API
#output will be a list of events
#api address for first page of results: 'https://app.ticketmaster.com/discovery/v2/events.json?latlong=40.754900,-73.984000&radius=8&unit=miles&source=ticketmaster&classificationName=music&startDateTime=2018-11-09T14:00:00Z&page=0&size=200&sort=relevance,desc&apikey=rah2o9AS2HbqU4x2DwAbsRZA35MutNT4'
class TicketMasterAPI:

    def __init__(self, url):
        self.url = url

    def data_pull(self):
        r = requests.get(self.url)
        concert_data_dictionary = r.json()
        concert_list = concert_data_dictionary['_embedded']['events']
        return concert_list


#class to define parsing functions
class EventsParser:
    def __init__(self, individual_concert_data):
        self.individual_concert_data = individual_concert_data

    #retrieves concert name
    def concert_name(self):
        return self.individual_concert_data['name']

    #retrieves concert Date
    def concert_date(self):
        return self.individual_concert_data['dates']['start']['localDate']

    #retrieves minimum price
    def concert_minimum_price(self):
        try:
            return self.individual_concert_data['priceRanges'][0]['min']
        except:
            pass

    #retrieves maximumum_price
    def concert_maximum_price(self):
        try:
            return self.individual_concert_data['priceRanges'][0]['max']
        except:
            pass

    #retrieves concert URL
    def concert_url(self):
        return self.individual_concert_data['url']

    #retrieve concert artist/artists
    def concert_artist(self):
        return self.individual_concert_data['_embedded']['attractions'][0]['name']

    #retrieves genre
    def concert_genre(self):
        try:
            return self.individual_concert_data['classifications'][0]['genre']['name']
        except:
            pass

    #retrieves venue_name
    def concert_venue_name(self):
        return self.individual_concert_data['_embedded']['venues'][0]['name']

    #retrieves venue city
    def concert_venue_city(self):
        return self.individual_concert_data['_embedded']['venues'][0]['city']['name']

    #retrieves concert venue address
    def concert_venue_address(self):
        try:
            return self.individual_concert_data['_embedded']['venues'][0]['address']['line1']
        except:
            pass

    #retrieves concert latitude
    def concert_venue_latitude(self):
        return self.individual_concert_data['_embedded']['venues'][0]['location']['latitude']

    #retrieves concert longitude
    def concert_venue_longitude(self):
        return self.individual_concert_data['_embedded']['venues'][0]['location']['longitude']
