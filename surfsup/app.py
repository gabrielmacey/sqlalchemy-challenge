# Ignore SQLITE warnings related to Decimal numbers in the Chinook database
import warnings
warnings.filterwarnings('ignore')

# Import Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func

import datetime as dt

#Import Flask
from flask import Flask

# Create an engine for the chinook.sqlite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect Database into ORM classes
inspector = inspect(engine)
inspector.get_table_names()
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save a reference to the invoices table
Measurement = Base.classes.measurement
Station = Base.classes.station

#app = Flask(__name__)

#@app.route("/")
