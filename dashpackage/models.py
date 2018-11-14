from sqlalchemy import Column, Integer, Text
from dash_package import db


#creating concert class/table
class Concert(db.Model):
    __tablename__ = 'concerts'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    date = Column(Date)
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
class Artist(db.Model):
    __tablename__ = 'artists'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    genre_id = Column(Text, ForeignKey('genres.id'))
    concerts = relationship('Concert', back_populates='artists')
    genres = relationship('Genre', back_populates='artists')



#creating genre class/table
class Genre(db.Model):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    artists = relationship('Artist', back_populates='genres')
    concerts = relationship('Concert', back_populates='genres')
    venues = relationship('Venue', back_populates='genres')

#creating venue class/table
class Venue(db.Model):
    __tablename__ = 'venues'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    city = Column(Text)
    address = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    zip = Column(Integer)
    neighborhood = Column(Text)
    borough = Column(Text)
    concerts = relationship('Concert', back_populates='venues')
    genres = relationship('Genre', back_populates='venues')
