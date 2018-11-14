from models import Concert, Artist, Genre, Venue
from dashpackage import app, db
import sqlalchemy


#top genres in borough
def top_genres_borough(borough):
    return session.query(Genre.name, sqlalchemy.func.count(Genre.name)).join(Concert).join(Venue).group_by(Genre.name).filter(Venue.borough == borough).all()

#average minimum price by borough
def avg_price_by_borough():
    return session.query(Venue.borough, sqlalchemy.func.avg(Concert.minimum_price)).join(Concert).group_by(Venue.borough).all()

#find average minimum price for a neighborhood (lower east side in example)
def avg_price_neighborhood(neighborhood):
    return session.query(sqlalchemy.func.avg(Concert.minimum_price)).join(Venue).filter(Venue.neighborhood == neighborhood).first()

#find borough with most free concerts
def most_free_concerts():
    return session.query(Venue.borough, sqlalchemy.func.count(Concert.name)).join(Concert).group_by(Venue.borough).filter(Concert.minimum_price == 0).all()

#date queries example
import datetime
def concerts_on_this_date(year, month, day):
    return session.query(Concert.name, Concert.date).filter(Concert.date == datetime.date(year, month, day)).all()

#find average minimum price by genre
def avg_price_by_genre():
    return session.query(Genre.name, sqlalchemy.func.avg(Concert.minimum_price)).join(Concert).group_by(Genre.name).all()

#finds number of concerts in each borough at this price or less
def concerts_at_price(price):
    return session.query(Venue.borough, sqlalchemy.func.count(Concert.name)).join(Concert).group_by(Venue.borough).filter(Concert.minimum_price <= price).all()
