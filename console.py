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
