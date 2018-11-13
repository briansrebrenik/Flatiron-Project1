from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import dash

server = Flask(__name__)
server.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///nycconcertdatabase.db'
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
server.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(server)

app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')

from dash_package.eventbriteapi import EventbriteConcertBuilder, EventbriteAPI, EventbriteEventsParser
from dash_package.ticketmasterapi import TicketmasterConcertBuilder, TicketMasterAPI, TicketmasterEventsParser

from dash_package.models import *
from dash_package.routes import *
from dash_package.dashboard import *
