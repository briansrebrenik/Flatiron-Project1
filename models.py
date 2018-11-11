from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import *
from sqlalchemy.orm import relationship


#creating concert class/table
class Concert(Base):
    __tablename__ = 'concerts'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    date = Column(Text)
    minimum_price = Column(Float)
    maximumum_price = Column(Float)
    url = Column(Text)
    artist_id = Column(Integer, ForeignKey('artists.id'))
    genre_id = Column(Integer, ForeignKey('genres.id'))
    venue_id = Column(Integer, ForeignKey('venues.id'))
    artists = relationship('Artist', back_populates ='concerts')
    genres = relationship('Genre', back_populates='concerts')
    venues = relationship('Venue', back_populates='concerts')

#creating artist class/table
class Artist(Base):
    __tablename__ = 'artists'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    genre_id = Column(Text, ForeignKey('genres.id'))
    concerts = relationship('Concert', back_populates='artists')
    genres = relationship('Genre', back_populates='artists')



#creating genre class/table
class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    artists = relationship('Artist', back_populates='genres')
    concerts = relationship('Concert', back_populates='genres')

#creating venue class/table
class Venue(Base):
    __tablename__ = 'venues'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    city = Column(Text)
    address = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    concerts = relationship('Concert', back_populates='venues')
