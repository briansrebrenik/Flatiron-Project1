#top genres in Queens
session.query(Genre.name, sqlalchemy.func.count(Genre.name)).join(Concert).join(Venue).group_by(Genre.name).filter(Venue.borough == "Queens").all()

#top genres in Manhattan
session.query(Genre.name, sqlalchemy.func.count(Genre.name)).join(Concert).join(Venue).group_by(Genre.name).filter(Venue.borough == "Manhattan").all()

#top genres in Brooklyn
session.query(Genre.name, sqlalchemy.func.count(Genre.name)).join(Concert).join(Venue).group_by(Genre.name).filter(Venue.borough == "Brooklyn").all()

#top genres in Bronx
session.query(Genre.name, sqlalchemy.func.count(Genre.name)).join(Concert).join(Venue).group_by(Genre.name).filter(Venue.borough == "Bronx").all()

#top genres in Staten Island
#None

#average minimum price by borough
session.query(Venue.borough, sqlalchemy.func.avg(Concert.minimum_price)).join(Concert).group_by(Venue.borough).all()

#find average minimum price for a neighborhood (lower east side in example)
session.query(sqlalchemy.func.avg(Concert.minimum_price)).join(Venue).filter(Venue.neighborhood == "Lower East Side").first()

#find borough with most free concerts
session.query(Venue.borough, sqlalchemy.func.count(Concert.name)).join(Concert).group_by(Venue.borough).filter(Concert.minimum_price == 0).all()
