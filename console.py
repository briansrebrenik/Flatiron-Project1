from models import Base, Concert, Artist, Genre, Venue
from scraper import TicketMasterAPI, EventsParser
import sqlalchemy
engine = sqlalchemy.create_engine('sqlite:///ticketmasterdatabase.db', echo=True)

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
            artists=goc(session, Artist, name=parser.concert_artist()),
            genres=goc(session, Genre, name=parser.concert_genre()),
            venues=goc(session, Venue,name=parser.concert_venue_name(), city=parser.concert_venue_city(),
            address=parser.concert_venue_address(), latitude=parser.concert_venue_latitude(),
            longitude=parser.concert_venue_longitude()))
            session.add(concert)
            session.commit()

page0 = 'https://app.ticketmaster.com/discovery/v2/events.json?latlong=40.754900,-73.984000&radius=8&unit=miles&source=ticketmaster&classificationName=music&startDateTime=2018-11-09T14:00:00Z&page=0&size=200&sort=relevance,desc&apikey=rah2o9AS2HbqU4x2DwAbsRZA35MutNT4'
page1 = 'https://app.ticketmaster.com/discovery/v2/events.json?latlong=40.754900,-73.984000&radius=8&unit=miles&source=ticketmaster&classificationName=music&startDateTime=2018-11-09T14:00:00Z&page=1&size=200&sort=relevance,desc&apikey=rah2o9AS2HbqU4x2DwAbsRZA35MutNT4'
page2 = 'https://app.ticketmaster.com/discovery/v2/events.json?latlong=40.754900,-73.984000&radius=8&unit=miles&source=ticketmaster&classificationName=music&startDateTime=2018-11-09T14:00:00Z&page=2&size=200&sort=relevance,desc&apikey=rah2o9AS2HbqU4x2DwAbsRZA35MutNT4'
page3 = 'https://app.ticketmaster.com/discovery/v2/events.json?latlong=40.754900,-73.984000&radius=8&unit=miles&source=ticketmaster&classificationName=music&startDateTime=2018-11-09T14:00:00Z&page=3&size=200&sort=relevance,desc&apikey=rah2o9AS2HbqU4x2DwAbsRZA35MutNT4'
page4 = 'https://app.ticketmaster.com/discovery/v2/events.json?latlong=40.754900,-73.984000&radius=8&unit=miles&source=ticketmaster&classificationName=music&startDateTime=2018-11-09T14:00:00Z&page=4&size=200&sort=relevance,desc&apikey=rah2o9AS2HbqU4x2DwAbsRZA35MutNT4'
page5 = 'https://app.ticketmaster.com/discovery/v2/events.json?latlong=40.754900,-73.984000&radius=8&unit=miles&source=ticketmaster&classificationName=music&startDateTime=2018-11-09T14:00:00Z&page=0&size=200&sort=relevance,asc&apikey=rah2o9AS2HbqU4x2DwAbsRZA35MutNT4'
