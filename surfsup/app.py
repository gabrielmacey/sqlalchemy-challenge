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
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save a reference to the invoices table
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    return(
    f"/api/v1.0/precipitation"
    f"/api/v1.0/stations"
    f"/api/v1.0/tobs"
    f"/api/v1.0/<start>"
    f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    closed_date = session.query(Measurement.date).order_by((Measurement.date).desc()).first()
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()
    session.close()
    precipitation = list(np.ravel(precipitation))
    return jsonify(
    precipitation
    )

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    number_of_stations = session.query(func.count(Station.id)).all()
    active_station = (session.query(Measurement.station, func.count(Measurement.station))
            .group_by(Measurement.station)
            .order_by(func.count(Measurement.station).desc())
            .all())
    session.close()
    active_station = list(np.ravel(active_station))
    return jsonify(
    active_station
    )

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    low_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.station == "USC00519281").all()
    high_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.station == "USC00519281").all()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.station == "USC00519281").all()
    session.close()
    low_temp = list(np.ravel(low_temp))
    high_temp = list(np.ravel(high_temp))
    avg_temp = list(np.ravel(avg_temp))
    return jsonify(
    low_temp,
    high_temp,
    avg_temp
    )

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def begin_n_end(start,end = None):
    session = Session(engine)
    Date = start
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        start_no_end=session.query(*sel).filter(func.strftime("%m-%d", Measurement.date) == Date).all()
        start_no_end=list(np.ravel(start_no_end))
        return jsonify(start_no_end)
    start_yes_end=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    start_yes_end=list(np.ravel(start_yes_end))
    return jsonify(start_yes_end)
