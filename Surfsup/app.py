# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL and ORM
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)
Base.classes.keys()

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session

session= Session(engine)
#################################################
# Flask Setup
#################################################
#from flask import Flask
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
#Start at the homepage.List all the available routes.
@app.route("/")
def home():
  
    return (
        f"Welcome to API Climate Analysis for Hawaii"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start (enter as YYYY-MM-DD)<br/>"
        f"/api/v1.0/start/end (enter as YYYY-MM-DD/YYYY-MM-DD)"

    )
#List the precipitation route.
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    one_year= dt.date(2017, 8, 23)-dt.timedelta(days=365)
    prev_last_date = dt.date(one_year.year, one_year.month, one_year.day)

    results= session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_last_date).order_by(Measurement.date.desc()).all()


    query_dict = dict(results)

    print(f"Results for Precipitation - {query_dict}")
    print("Out of Precipitation section.")
    return jsonify(query_dict) 
    session.close()



#List the station route.

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    sel = [Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation]
    queryresult = session.query(*sel).all()
    

    stations = []
    for station,name,lat,lon,el in queryresult:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Lat"] = lat
        station_dict["Lon"] = lon
        station_dict["Elevation"] = el
        stations.append(station_dict)
    return jsonify(stations)
    session.close()
#List the tobs route.
@app.route("/api/v1.0/tobs")
def tobs():
     session = Session(engine)


     queryresult = session.query( Measurement.date, Measurement.tobs).filter(Measurement.station=='USC00519281')\
     .filter(Measurement.date>='2016-08-23').all()


     tob_obs = []
     for date, tobs in queryresult:
         tobs_dict = {}
         tobs_dict["Date"] = date
         tobs_dict["Tobs"] = tobs
         tob_obs.append(tobs_dict)

     return jsonify(tob_obs)
     session.close()

#List the start route.
@app.route("/api/v1.0/<start>")

def get_temp_start(start):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
              filter(Measurement.date >= start).all()
    

    temps = []
    for TMIN, TAVG, TMAX in results:
        temps_dict = {}
        temps_dict['Minimum Temperature'] = TMIN
        temps_dict['Average Temperature'] = TAVG
        temps_dict['Maximum Temperature'] = TMAX
        temps.append(temps_dict)

    return jsonify(temps)
    session.close()
#List the end route.
@app.route("/api/v1.0/<start>/<end>")
def get_temp_end(start, end):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
              filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    

    temps = []
    for TMIN, TAVG, TMAX in results:
        temps_dict = {}
        temps_dict['Minimum Temperature'] = TMIN
        temps_dict['Average Temperature'] = TAVG
        temps_dict['Maximum Temperature'] = TMAX
        temps.append(temps_dict)

    return jsonify(temps)
    session.close()

if __name__ == '__main__':
    app.run(debug=True)
