from models import Base, Concert, Artist, Genre, Venue
from ticketmasterscraper import TicketMasterAPI, TicketmasterEventsParser
from ticketwebparser import TicketWebParser
from eventbritescraper import EventbriteAPI, EventbriteEventsParser
from bs4 import BeautifulSoup
import sqlalchemy
engine = sqlalchemy.create_engine('sqlite:///nycconcertdatabase.db', echo=True)

Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

from sqlalchemy.orm.exc import NoResultFound



#goc = "get one or create" queries databse to check to make sure object has not already been initialized
def goc(session, model,**kwargs):
   try:
       return session.query(model).filter_by(**kwargs).one()
   except NoResultFound:
       return model(**kwargs)


#ConcertBuilder class will use output from ticketmasterapi function
#and parsing functions from EventsParser class to output
#sqlalchemy objects


class TicketmasterConcertBuilder:
    def __init__(self, url):
        self.url = url

    def run(self):
        all_concerts = []
        tm = TicketMasterAPI(self.url)
        for i in tm.data_pull():
            parser = TicketmasterEventsParser(i)
            concert = Concert(name=parser.concert_name(),
            date=parser.concert_date(), minimum_price=parser.concert_minimum_price(),
            maximumum_price=parser.concert_maximum_price(), url=parser.concert_url(),
            artists=goc(session, Artist, name=parser.concert_artist()),
            genres=goc(session, Genre, name=parser.concert_genre()),
            venues=goc(session, Venue,name=parser.concert_venue_name(), city=parser.concert_venue_city(),
            address=parser.concert_venue_address(), latitude=parser.concert_venue_latitude(),
            longitude=parser.concert_venue_longitude()))
            session.add(concert)
            session.commit()

# Ticketmaster API addresses
# page0 = 'https://app.ticketmaster.com/discovery/v2/events.json?latlong=40.754900,-73.984000&radius=8&unit=miles&source=ticketmaster&classificationName=music&startDateTime=2018-11-09T14:00:00Z&page=0&size=200&sort=relevance,desc&apikey=rah2o9AS2HbqU4x2DwAbsRZA35MutNT4'
# page1 = 'https://app.ticketmaster.com/discovery/v2/events.json?latlong=40.754900,-73.984000&radius=8&unit=miles&source=ticketmaster&classificationName=music&startDateTime=2018-11-09T14:00:00Z&page=1&size=200&sort=relevance,desc&apikey=rah2o9AS2HbqU4x2DwAbsRZA35MutNT4'
# page2 = 'https://app.ticketmaster.com/discovery/v2/events.json?latlong=40.754900,-73.984000&radius=8&unit=miles&source=ticketmaster&classificationName=music&startDateTime=2018-11-09T14:00:00Z&page=2&size=200&sort=relevance,desc&apikey=rah2o9AS2HbqU4x2DwAbsRZA35MutNT4'
# page3 = 'https://app.ticketmaster.com/discovery/v2/events.json?latlong=40.754900,-73.984000&radius=8&unit=miles&source=ticketmaster&classificationName=music&startDateTime=2018-11-09T14:00:00Z&page=3&size=200&sort=relevance,desc&apikey=rah2o9AS2HbqU4x2DwAbsRZA35MutNT4'
# page4 = 'https://app.ticketmaster.com/discovery/v2/events.json?latlong=40.754900,-73.984000&radius=8&unit=miles&source=ticketmaster&classificationName=music&startDateTime=2018-11-09T14:00:00Z&page=4&size=200&sort=relevance,desc&apikey=rah2o9AS2HbqU4x2DwAbsRZA35MutNT4'
# page5 = 'https://app.ticketmaster.com/discovery/v2/events.json?latlong=40.754900,-73.984000&radius=8&unit=miles&source=ticketmaster&classificationName=music&startDateTime=2018-11-09T14:00:00Z&page=0&size=200&sort=relevance,asc&apikey=rah2o9AS2HbqU4x2DwAbsRZA35MutNT4'


#function to add ticketweb prices
def add_ticket_web_prices():
    concerts = session.query(Concert).filter(Concert.minimum_price == None).all()
    for concert in concerts:
        if "ticketweb" in concert.url:
            try:
                parser = TicketWebParser(concert.url)
                concert.minimum_price = parser.get_price()
                session.add(concert)
                session.commit()
            except:
                pass



#ConcertBuilder class will use output from eventbriteapi function
#and parsing functions from EventsParser class to output
#sqlalchemy objects


class EventbriteConcertBuilder:
    def __init__(self, url):
        self.url = url

    def run(self):
        all_concerts = []
        tm = EventbriteAPI(self.url)
        for i in tm.data_pull():
            parser = EventbriteEventsParser(i)
            concert = Concert(name=parser.concert_name(),
            date=parser.concert_date(), minimum_price=parser.concert_minimum_price(),
            maximumum_price=parser.concert_maximum_price(), url=parser.concert_url(),
            genres=goc(session, Genre, name=parser.concert_genre()),
            venues=goc(session, Venue,name=parser.concert_venue_name(), city=parser.concert_venue_city(),
            address=parser.concert_venue_address(), latitude=parser.concert_venue_latitude(),
            longitude=parser.concert_venue_longitude()))
            session.add(concert)
            session.commit()



#function to cycle through all eventbrite addresses
def parse_through_apis():
    for i in range(1, 28):
        url = f"https://www.eventbriteapi.com/v3/events/search/?page={i}&categories=103&start_date.range_start=2018-11-08T00:00:00Z&price=paid&location.latitude=40.7549&location.longitude=-73.9840&location.within=8mi&expand=venue,subcategory,ticket_availability&token=XZYQ3WKQV5AWJJSDWP5L"
        builder = EventbriteConcertBuilder(url)
        builder.run()
