from models import Base, Concert, Artist, Genre, Venue
from scraper import ConcertBuilder, TicketMasterAPI, EventsParser
import sqlalchemy
engine = sqlalchemy.create_engine('sqlite:///ticketmasterdatabase.db', echo=True)

Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()
