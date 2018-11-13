
from flask import render_template
from dash_package.models import Concert
from dash_package import server
import pdb

@server.route('/concerts')
def render_concerts():
    concert = Concert.query.get(1)
    return concert.name
    # return render_template('index.html', apartments = apartments)
